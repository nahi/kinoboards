#!/usr/local/bin/GNU/perl
#
# $Id: kb.cgi,v 5.0 1997-07-03 09:58:00 nakahiro Exp $


# KINOBOARDS: Kinoboards Is Network Opened BOARD System
# Copyright (C) 1995, 96, 97 NAKAMURA Hiroshi.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PRATICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.


# This file implements main functions of KINOBOARDS.


# �Ķ��ѿ��򽦤�
$TIME = time;			# �ץ���൯ư����(UTC)
$SERVER_NAME = $ENV{'SERVER_NAME'};
$SERVER_PORT = $ENV{'SERVER_PORT'};
$REMOTE_HOST = $ENV{'REMOTE_HOST'};
$SCRIPT_NAME = $ENV{'SCRIPT_NAME'};
$PATH_INFO = $ENV{'PATH_INFO'};
$PATH_TRANSLATED = $ENV{'PATH_TRANSLATED'};

# ����ѿ������
$[ = 0;				# zero origined
$| = 1;				# pipe flushed
($CGIPROG_NAME = $SCRIPT_NAME) =~ s!^(.*/)!!o;
$SYSDIR_NAME = (($PATH_INFO) ? "$PATH_INFO/" : "$1");
$HEADER_FILE = ($CGIPROG_NAME =~ m/^(.*)\..*$/o) ? "$1.ph" : 'kb.ph';
$SCRIPT_URL = "http://$SERVER_NAME$SERVER_PORT_STRING$SCRIPT_NAME$PATH_INFO";
$PROGRAM = (($PATH_INFO) ? "$SCRIPT_NAME$PATH_INFO" : "$CGIPROG_NAME");
$SERVER_PORT_STRING = '';
$KB_VERSION = '1.0';
$KB_RELEASE = '4.1pre';

# �ǥ��쥯�ȥ�
$ICON_DIR = 'icons';				# ��������ǥ��쥯�ȥ�
# �ե�����
$BOARD_ALIAS_FILE = 'kinoboards';		# �Ǽ���DB
$CONF_FILE_NAME = '.kbconf';			# �Ǽ�����configuratin�ե�����
$ARRIVEMAIL_FILE_NAME = '.kbmail';		# �Ǽ����̿����ᥤ��������DB
$BOARD_FILE_NAME = '.board';			# �����ȥ�ꥹ�ȥإå�DB
$DB_FILE_NAME = '.db';				# ����DB
$ARTICLE_NUM_FILE_NAME = '.articleid';		# �����ֹ�DB
$USER_ALIAS_FILE = 'kinousers';			# �桼��DB
$DEFAULT_ICONDEF = 'all.idef';			# ��������DB
$LOCK_FILE = '.lock.kb';			# ��å��ե�����
# Suffix
$TMPFILE_SUFFIX = 'tmp';			# DB�ƥ�ݥ��ե������Suffix
$ICONDEF_POSTFIX = 'idef';			# ��������DB�ե������Suffix

# ��������ե���������URL
$ICON_BLIST = "$ICON_DIR/blist.gif";		# �Ǽ��İ�����
$ICON_TLIST = "$ICON_DIR/tlist.gif";		# �����ȥ������
$ICON_PREV = "$ICON_DIR/prev.gif";		# ���ε�����
$ICON_NEXT = "$ICON_DIR/next.gif";		# ���ε�����
$ICON_WRITENEW = "$ICON_DIR/writenew.gif";	# �����񤭹���
$ICON_FOLLOW = "$ICON_DIR/follow.gif";		# ��ץ饤
$ICON_QUOTE = "$ICON_DIR/quote.gif";		# ���Ѥ��ƥ�ץ饤
$ICON_THREAD = "$ICON_DIR/thread.gif";		# �ޤȤ��ɤ�
$ICON_HELP = "$ICON_DIR/help.gif";		# �إ��
$ICON_DELETE = "$ICON_DIR/delete.gif";		# ���
$ICON_SUPERSEDE = "$ICON_DIR/supersede.gif";	# ����

# ���󥯥롼�ɥե�������ɤ߹���
if ($PATH_INFO && (-s "$HEADER_FILE")) { require($HEADER_FILE); }
if ($PATH_TRANSLATED ne '') { chdir($PATH_TRANSLATED); }
if (-s "$HEADER_FILE") {
    require($HEADER_FILE);
} else {
    die("cannot find configuration file: `$HEADER_FILE'");
}
require('cgi.pl');
require('jcode.pl');

# ���󥯥롼�ɥե����������˱���������ѿ�������
$SYS_F_MT = ($SYS_F_D || $SYS_F_AM || $SYS_F_LI || $SYS_F_MV);
if (($SERVER_PORT != 80) && ($SYS_PORTNO == 1)) {
    $SERVER_PORT_STRING = ":$SERVER_PORT";
}
if ($TIME_ZONE) { $ENV{'TZ'} = $TIME_ZONE; }
if ($BOARDLIST_URL eq '-') { $BOARDLIST_URL = "$PROGRAM?c=bl"; }
$ADDRESS = sprintf("Maintenance: <a href=\"mailto:%s\">%s</a><br><a href=\"http://www.kinotrope.co.jp/~nakahiro/kb10.shtml\">KINOBOARDS/%s R%s</a>: Copyright (C) 1995, 96, 97 <a href=\"http://www.kinotrope.co.jp/~nakahiro/\">NAKAMURA Hiroshi</a>.", $MAINT, $MAINT_NAME, $KB_VERSION, $KB_RELEASE);

# �����ʥ�ϥ�ɥ�
$SIG{'HUP'} = $SIG{'INT'} = $SIG{'QUIT'} = $SIG{'TERM'} = $SIG{'TSTP'} = 'DoKill';
sub DoKill { &cgi'unlock($LOCK_FILE); exit(1); }


######################################################################


###
## MAIN - �ᥤ��֥�å�
#
# - SYNOPSIS
#	kb.cgi
#
# - ARGS
#	�ʤ�
#
# - DESCRIPTION
#	��ư���˰��٤������Ȥ���롥
#	�������Ϥʤ������Ķ��ѿ�QUERY_STRING��REQUEST_METHOD��
#	�⤷����ɸ�����Ϸ�ͳ���ͤ��Ϥ��ʤ��ȡ�������ư��ʤ���
#
# - RETURN
#	�ʤ�
#
&cgi'lock($LOCK_FILE) || &Fatal(999, '');

MAIN: {

    local($BoardConfFile, $Command, $Com);

    # ɸ������(POST)�ޤ��ϴĶ��ѿ�(GET)�Υǥ����ɡ�
    &cgi'Decode;

    # ���ˤ˻Ȥ��Τ�����ѿ���Ȥ�(���ʤ�)
    $BOARDNAME = &GetBoardInfo($BOARD = $cgi'TAGS{'b'});
    # ������͡�
    if ($BOARDNAME =~ m!/!o) { &Fatal(11, $BOARDNAME); }

    # �Ǽ��ĸ�ͭ���åƥ��󥰤��ɤ߹���
    $BoardConfFile = &GetPath($BOARD, $CONF_FILE_NAME);
    if (-s "$BoardConfFile") { require("$BoardConfFile"); }

    # DB������ѿ��˥���å���
    if ($BOARD) { &DbCash($BOARD); }

    # �ͤ����
    $Command = $cgi'TAGS{'c'};
    $Com = $cgi'TAGS{'com'};

    # ���ޥ�ɥ����פˤ��ʬ��
    &ShowArticle,	last if ($SYS_F_E  && ($Command eq 'e'));
    &ThreadArticle,	last if ($SYS_F_T  && ($Command eq 't'));
    &Entry(0),		last if ($SYS_F_N  && ($Command eq 'n'));
    &Entry(1),		last if ($SYS_F_FQ && ($Command eq 'f'));
    &Entry(2),		last if ($SYS_F_FQ && ($Command eq 'q'));
    &Preview,		last if (($SYS_F_N || $SYS_F_FQ) && ($Command eq 'p') && ($Com ne 'x'));
    &Thanks,		last if (($SYS_F_N || $SYS_F_FQ) && ($Command eq 'x'));
    &Thanks,		last if (($SYS_F_N || $SYS_F_FQ) && ($Command eq 'p') && ($Com eq 'x'));
    &ViewTitle,		last if ($SYS_F_V  && ($Command eq 'v'));
    &SortArticle,	last if ($SYS_F_R  && ($Command eq 'r'));
    &NewArticle,	last if ($SYS_F_L  && ($Command eq 'l'));
    &SearchArticle,	last if ($SYS_F_S  && ($Command eq 's'));
    &ShowIcon,		last if ($Command eq 'i');
    &AliasNew,		last if ($SYS_ALIAS && ($Command eq 'an'));
    &AliasMod,		last if ($SYS_ALIAS && ($Command eq 'am'));
    &AliasDel,		last if ($SYS_ALIAS && ($Command eq 'ad'));
    &AliasShow,		last if ($SYS_ALIAS && ($Command eq 'as'));

    # �ʲ��ϴ�����
    &ViewTitle('maint'),	last if ($SYS_F_MT && ($Command eq 'vm'));
    &DeletePreview,	last if ($SYS_F_D  && ($Command eq 'dp'));
    &DeleteExec(0),	last if ($SYS_F_D  && ($Command eq 'de'));
    &DeleteExec(1),	last if ($SYS_F_D  && ($Command eq 'det'));
    &ArriveMailEntry,   last if ($SYS_F_AM && ($Command eq 'mp'));
    &ArriveMailExec,    last if ($SYS_F_AM && ($Command eq 'me'));
    &ViewTitle('linkto'),	last if ($SYS_F_LI && ($Command eq 'ct'));
    &ViewTitle('linkexec'),	last if ($SYS_F_LI && ($Command eq 'ce'));
    &ViewTitle('moveto'),	last if ($SYS_F_MV && ($Command eq 'mvt'));
    &ViewTitle('moveexec'),	last if ($SYS_F_MV && ($Command eq 'mve'));

    # �ǥե����
    &BoardList,		last if ($SYS_F_B  && ($Command eq 'bl'));

    if ($Command ne '') {
	&Fatal(99, '');
    } else {
	print("huh... what's up? running under any shell?\n");
    }

}


&cgi'unlock($LOCK_FILE);
exit(0);


######################################################################
# �桼�����󥿥ե���������ץ���ơ������(����)
#
# �Ȥ�ʤ���ǽ���б�����ؿ��ϡ����ʧ�äƤ�ư���ġĤϤ��Ǥ�
# (�����ƥ��ȤϤ��Ƥޤ��� ^_^;)��


###
## BoardList - �Ǽ��İ�����ɽ��
#
# - SYNOPSIS
#	BoardList;
#
# - ARGS
#	�ʤ�
#
# - DESCRIPTION
#	�Ǽ��İ�����ɽ�����롥
#
# - RETURN
#	�ʤ�
#
sub BoardList {

    local(%BoardList, %BoardInfo, $Key, $Value, $ModTime, $NumOfArticle);

    # ���Ǽ��Ĥξ������Ф�
    &getAllBoardInfo(*BoardList, *BoardInfo);

    &MsgHeader("Board List", "$SYSTEM_NAME");

    &cgiprint'Cache(<<__EOF__);
<p>
<a href="http://www.kinotrope.co.jp/~nakahiro/kb10.shtml">KINOBOARDS/1.0</a>
�Ǳ��Ĥ���Ƥ��륷���ƥ�Ǥ���
</p><p>
$SYSTEM_NAME�Ǥϡ����ߡ��ʲ���$H_BOARD���Ѱդ���Ƥ��ޤ���
</p>
__EOF__

    &cgiprint'Cache("<dl>\n");
    while(($Key, $Value) = each(%BoardList)) {
	$ModTime = &GetDateTimeFormatFromUtc(&GetModifiedTime($DB_FILE_NAME, $Key));
	$NumOfArticle = &getArticleId($Key);
	&cgiprint'Cache("<p>\n<dt><a href=\"$PROGRAM?b=$Key&c=v&num=$DEF_TITLE_NUM\">$Value</a>\n");
	&cgiprint'Cache("[�ǿ�: $ModTime, ������: $NumOfArticle]\n");
	&cgiprint'Cache("<dd>$BoardInfo{$Key}\n</p>\n");
    }

    &cgiprint'Cache("</dl>\n</p>\n");

    &MsgFooter;

}


###
## Entry - �񤭹��߲��̤�ɽ��
#
# - SYNOPSIS
#	Entry($QuoteFlag);
#
# - ARGS
#	$QuoteFlag	0 ... ����
#			1 ... ���Ѥʤ��Υ�ץ饤
#			2 ... ���Ѥ���Υ�ץ饤
#
# - DESCRIPTION
#	�񤭹��߲��̤�ɽ������
#	����ѿ��Ǥ��롤CGI�ѿ��򻲾Ȥ��롥
#
# - RETURN
#	�ʤ�
#
sub Entry {
    local($QuoteFlag) = @_;
    local($Id, $Supersede, $IconTitle, $Key, $Value, $Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail, $DefSubject, $DefName, $DefEmail, $DefUrl, $DefFmail);

    $Id = $cgi'TAGS{'id'};
    $Supersede = $cgi'TAGS{'s'}; # ����?
    if ($QuoteFlag != 0) {
	($Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail) = &GetArticlesInfo($Id);
    }
    $Icon = $Icon || $H_NOICON;
    $DefSubject = ($Supersede ? $Subject : (($QuoteFlag == 0) ? '' : &GetReplySubject($Id)));
    $DefName = ($Supersede ? $Name : '');
    $DefEmail = ($Supersede ? $Email : '');
    $DefUrl = ($Supersede ? $Url : 'http://');
    $DefFmail = ($Supersede ? $Fmail : '');

    # ɽ�����̤κ���
    if ($Supersede && $SYS_F_SS) {
	&MsgHeader('Supersede entry', "$BOARDNAME: $H_MESG������");
    } else {
	&MsgHeader('Message entry', "$BOARDNAME: $H_MESG�ν񤭹���");
    }

    # �ե����ξ��
    if ($QuoteFlag != 0) {
	# ������ɽ��(���ޥ��̵��, ����������)
	&ViewOriginalArticle($Id, 0, 1);
	if ($Supersede && $SYS_F_SS) {
	    &cgiprint'Cache("<hr>\n<h2>���$H_MESG����������</h2>");
	} else {
	    &cgiprint'Cache("<hr>\n<h2>���$H_MESG�ؤ�$H_REPLY��񤭹���</h2>");
	}
    }

    # ����«
    &cgiprint'Cache(<<__EOF__);
<form action="$PROGRAM" method="POST">
<input name="c" type="hidden" value="p">
<input name="b" type="hidden" value="$BOARD">
<input name="id" type="hidden" value="$Id">
<input name="s" type="hidden" value="$Supersede">
<p>
__EOF__
    if ($Supersede && $SYS_F_SS) {
	&cgiprint'Cache(<<__EOF__);
���$H_MESG�����촹����$H_MESG��񤭹���Ǥ���������
__EOF__
    } else {
	&cgiprint'Cache(<<__EOF__);
$H_SUBJECT��$H_MESG��$H_FROM��$H_MAIL������˥����֥ڡ����򤪻��������ϡ�
�ۡ���ڡ�����$H_URL��񤭹���Ǥ�������(�����󡤤ʤ��Ƥ⹽���ޤ���)��
__EOF__
    }

    # HTML�Ǥ�񤱤���
    if ($SYS_TEXTTYPE) {
	&cgiprint'Cache(<<__EOF__);
HTML��¸�������ϡ���$H_TEXTTYPE�פ��$H_HTML�פˤ��ơ�
$H_MESG��HTML�Ȥ��ƽ񤤤�ĺ���ȡ�ɽ���λ���HTML������Ԥʤ��ޤ���
__EOF__
    }

    &cgiprint'Cache(<<__EOF__);
</p>
<p>
$H_BOARD: $BOARDNAME<br>
__EOF__

    # �������������
    if ($SYS_ICON) {
	&cashIconDB($BOARD);	# ��������DB�򥭥�å���
	&cgiprint'Cache("$H_ICON:\n<SELECT NAME=\"icon\">\n<OPTION SELECTED>$H_NOICON\n");
	foreach $IconTitle (sort keys(%ICON_FILE)) {
	    &cgiprint'Cache("<OPTION>$IconTitle\n");
	}
	&cgiprint'Cache("</SELECT>\n");

	&cgiprint'Cache("(<a href=\"$PROGRAM?b=$BOARD&c=i&type=entry\">�������������</a>)<BR>\n");

    }

    # Subject(�ե����ʤ鼫ưŪ��ʸ����������)
    &cgiprint'Cache(sprintf("%s: <input name=\"subject\" type=\"text\" value=\"%s\" size=\"%s\"><br>\n", $H_SUBJECT, $DefSubject, $SUBJECT_LENGTH));

    # TextType
    if ($SYS_TEXTTYPE) {
	&cgiprint'Cache(<<__EOF__);
$H_TEXTTYPE:
<SELECT NAME="texttype">
<OPTION SELECTED>$H_PRE
<OPTION>$H_HTML
</SELECT>
</p>
__EOF__

    }

    # ��ʸ(���Ѥ���ʤ鸵����������)
    &cgiprint'Cache("<p><textarea name=\"article\" rows=\"$TEXT_ROWS\" cols=\"$TEXT_COLS\">");
    if ($Supersede && $SYS_F_SS) {
	&QuoteOriginalArticleWithoutQMark($Id);
    } elsif ($QuoteFlag == 2) {
	&QuoteOriginalArticle($Id);
    }

    &cgiprint'Cache("</textarea></p>\n");

    # �եå���ʬ��ɽ��
    # ̾���ȥᥤ�륢�ɥ쥹��URL��
    &cgiprint'Cache(<<__EOF__);
<p>
$H_MESG��˴�Ϣ�����֥ڡ����ؤΥ�󥯤�ĥ����ϡ�
��&lt;URL:http://��&gt;�פΤ褦�ˡ�URL���&lt;URL:�פȡ�&gt;�פǰϤ��
�񤭹���Ǥ�����������ưŪ�˥�󥯤�ĥ���ޤ���
</p>
__EOF__

    if ($SYS_ALIAS == 0) {

	# �����ꥢ���ϻȤ�ʤ�
	&cgiprint'Cache(<<__EOF__);
<p>
$H_FROM: <input name="name" type="text" value="$DefName" size="$NAME_LENGTH"><br>
$H_MAIL: <input name="mail" type="text" value="$DefEmail" size="$MAIL_LENGTH"><br>
$H_URL_S: <input name="url" type="text" value="$DefUrl" size="$URL_LENGTH"><br>
</p>
__EOF__

    } elsif ($SYS_ALIAS == 1) {

	# �����ꥢ����Ȥ�
	&cgiprint'Cache(<<__EOF__);
<p>
$H_FROM: <input name="name" type="text" value="$DefName" size="$NAME_LENGTH"><br>
$H_MAIL: <input name="mail" type="text" value="$DefEmail" size="$MAIL_LENGTH"><br>
$H_URL_S: <input name="url" type="text" value="$DefUrl" size="$URL_LENGTH">
</p>
__EOF__

	&cgiprint'Cache(<<__EOF__);
<p>
��$H_ALIAS�פˡ�$H_FROM��$H_MAIL��$H_URL����Ͽ�ʤ��äƤ������ϡ�
��$H_FROM�פˡ�#...�פȤ�����Ͽ̾��񤤤Ƥ���������
��ưŪ��$H_FROM��$H_MAIL��$H_URL������ޤ���
(<a href="$PROGRAM?c=as">$H_ALIAS�ΰ���</a> //
 <a href="$PROGRAM?c=an">$H_ALIAS����Ͽ</a>)
</p>
__EOF__

    } else {

	# �����ꥢ������Ͽ���ʤ���н񤭹��ߤǤ��ʤ�

	# �����ꥢ�����ɤ߹���
	&CashAliasData;

	&cgiprint'Cache(<<__EOF__);
<p>
$H_USER:
<SELECT NAME="name">
<OPTION SELECTED>$H_FROM����Ͽ����$H_ALIAS������Ǥ�������
__EOF__

	while (($Key, $Value) = each %Name) {
	    &cgiprint'Cache("<OPTION>$Key\n");
	}
	&cgiprint'Cache(<<__EOF__);
</SELECT>
</p>
__EOF__

	&cgiprint'Cache(<<__EOF__);
<p>
ͽ���$H_ALIAS�פˡ�$H_FROM��$H_MAIL��$H_URL����Ͽ���ʤ��Ƚ񤭹���ޤ���
��Ͽ�����塤��#...�פȤ�����Ͽ̾����ꤷ�Ƥ���������
(<a href="$PROGRAM?c=as">$H_ALIAS�ΰ���</a> //
 <a href="$PROGRAM?c=an">$H_ALIAS����Ͽ</a>)<br>
��Ͽ����$H_ALIAS��ɽ������ʤ�(����Ǥ��ʤ�)��硤
���Υڡ�������ɤ߹��ߤ��Ƥ���������
</p>
__EOF__

    }

    if ($SYS_MAIL) {
	&cgiprint'Cache("<p>$H_REPLY�����ä����˥ᥤ����Τ餻�ޤ���? <input name=\"fmail\" type=\"checkbox\" value=\"on\"></p>\n");
    }
    
    # �ܥ���
    &cgiprint'Cache(<<__EOF__);
<p>
�񤭹�������Ƥ�<br>
<input type="radio" name="com" value="p" CHECKED>: ���ɽ�����Ƥߤ�(�ޤ���Ƥ��ޤ���)<br>
__EOF__

    if ($Supersede && $SYS_F_SS) {
	&cgiprint'Cache("<input type=\"radio\" name=\"com\" value=\"x\">: �������ޤ�<br>\n");
    } else {
	&cgiprint'Cache("<input type=\"radio\" name=\"com\" value=\"x\">: $H_MESG����Ƥ���<br>\n");
    }

    &cgiprint'Cache(<<__EOF__);
<input type="submit" value="�¹�">
</p>
</form>
__EOF__

    &MsgFooter;

}


###
## Preview - �ץ�ӥ塼���̤�ɽ��
#
# - SYNOPSIS
#	Preview;
#
# - ARGS
#	�ʤ�
#
# - DESCRIPTION
#	�ץ�ӥ塼���̤�ɽ�����롥
#	����ѿ��Ǥ��롤CGI�ѿ��򻲾Ȥ��롥
#
# - RETURN
#	�ʤ�
#
sub Preview {

    local($Supersede, $Id, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail, $rFid);

    # ���Ϥ��줿��������
    $Supersede = $cgi'TAGS{'s'};
    $Id = $cgi'TAGS{'id'};
    $TextType = $cgi'TAGS{'texttype'};
    $Name = $cgi'TAGS{'name'};
    $Email = $cgi'TAGS{'mail'};
    $Url = $cgi'TAGS{'url'};
    $Icon = $cgi'TAGS{'icon'};
    $Subject = $cgi'TAGS{'subject'};
    $Article = $cgi'TAGS{'article'};
    $Fmail = $cgi'TAGS{'fmail'};
    if ($Id ne '') { $rFid = &GetArticlesInfo($Id); }

    # ���Ϥ��줿��������Υ����å�
    $Article = &CheckArticle($BOARD, $TextType, *Name, *Email, *Url, *Subject, *Icon, $Article);

    # ��ǧ���̤κ���
    &MsgHeader('Message preview', "$BOARDNAME: �񤭹��ߤ����Ƥ��ǧ���Ƥ�������");

    # ����«
    &cgiprint'Cache(<<__EOF__);
<form action="$PROGRAM" method="POST">
<input name="c"        type="hidden" value="x">
<input name="b"        type="hidden" value="$BOARD">
<input name="id"       type="hidden" value="$Id">
<input name="texttype" type="hidden" value="$TextType">
<input name="name"     type="hidden" value="$Name">
<input name="mail"     type="hidden" value="$Email">
<input name="url"      type="hidden" value="$Url">
<input name="icon"     type="hidden" value="$Icon">
<input name="subject"  type="hidden" value="$Subject">
<input name="article"  type="hidden" value="$Article">
<input name="fmail"    type="hidden" value="$Fmail">
<input name="s"        type="hidden" value="$Supersede">

__EOF__

    if ($Supersede && $SYS_F_SS) {
	&cgiprint'Cache(<<__EOF__);
<p>
���$H_MESG���ؤ��ˡ�����$H_MESG��񤭹��ߤޤ���
ɬ�פǤ���С��֥饦����BACK�ܥ������äơ��񤭹��ߤ������Ƥ���������
�������Хܥ���򲡤����������ޤ��礦��
<input type="submit" value="�������ޤ�">
</p>
</form>
__EOF__
	&ViewOriginalArticle($Id, 0, 1);
	&cgiprint'Cache("<hr>\n");
    } else {
	&cgiprint'Cache(<<__EOF__);
<p>
ɬ�פǤ���С��֥饦����BACK�ܥ������äơ��񤭹��ߤ������Ƥ���������
�������Хܥ���򲡤��ƽ񤭹��ߤޤ��礦��
<input type="submit" value="��Ƥ���">
</p>
</form>
__EOF__
    }

    &cgiprint'Cache("<p>\n");

    # ��
    (($Icon eq $H_NOICON) || (! $Icon))
        ? &cgiprint'Cache("<strong>$H_SUBJECT</strong>: $Subject")
            : &cgiprint'Cache(sprintf("<strong>$H_SUBJECT</strong>: <img src=\"%s\" alt=\"$Icon \" width=\"$MSGICON_WIDTH\" height=\"$MSGICON_HEIGHT\">$Subject", &GetIconURLFromTitle($Icon, $BOARD)));

    # ��̾��
    if ($Url ne '') {
        # URL��������
        &cgiprint'Cache("<br>\n<strong>$H_FROM</strong>: <a href=\"$Url\">$Name</a>");
    } else {
        # URL���ʤ����
        &cgiprint'Cache("<br>\n<strong>$H_FROM</strong>: $Name");
    }

    # �ᥤ��
    if ($Email ne '') {
	&cgiprint'Cache(" <a href=\"mailto:$Email\">&lt;$Email&gt;</a>");
    }

    # ȿ����(���Ѥξ��)
    if (defined($rFid)) {
	if ($rFid ne '') {
	    &ShowLinksToFollowedArticle(($Id, split(/,/, $rFid)));
	} else {
	    &ShowLinksToFollowedArticle($Id);
	}
    }

    # �ڤ���
    &cgiprint'Cache("</p>\n$H_LINE\n");

    # TextType��������
    if ((! $SYS_TEXTTYPE) || ($TextType eq $H_PRE)) {
	&cgiprint'Cache("<p><pre>");
    }

    # ����
    $Article = &DQDecode($Article);
    $Article = &ArticleEncode($Article);
    &cgiprint'Cache("$Article\n");

    # TextType�Ѹ����
    if ((! $SYS_TEXTTYPE) || ($TextType eq $H_PRE)) {
	&cgiprint'Cache("</pre></p>\n");
    }

    &MsgFooter;
}


###
## Thanks - ��Ͽ����̤�ɽ��
#
# - SYNOPSIS
#	Thanks;
#
# - ARGS
#	�ʤ�
#
# - DESCRIPTION
#	�񤭹��߸�β��̤�ɽ������
#	����ѿ��Ǥ��롤CGI�ѿ��򻲾Ȥ��롥
#
# - RETURN
#	�ʤ�
#
sub Thanks {

    local($Supersede, $Id, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail, $ArticleId);

    # ���Ϥ��줿��������
    $Supersede = $cgi'TAGS{'s'};
    $Id = $cgi'TAGS{'id'};
    $TextType = $cgi'TAGS{'texttype'};
    $Name = $cgi'TAGS{'name'};
    $Email = $cgi'TAGS{'mail'};
    $Url = $cgi'TAGS{'url'};
    $Icon = $cgi'TAGS{'icon'};
    $Subject = $cgi'TAGS{'subject'};
    $Article = $cgi'TAGS{'article'};
    $Fmail = $cgi'TAGS{'fmail'};

    if ($Supersede && $SYS_F_SS) {

	# �������� 
	&SupersedeArticle($BOARD, $Id, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail);

	# ɽ�����̤κ���
	&MsgHeader('Message superseded', "$BOARDNAME: $H_MESG����������ޤ���");

    } else {

	# �����κ���
	&MakeNewArticle($BOARD, $Id, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail);

	# ɽ�����̤κ���
	&MsgHeader('Message entried', "$BOARDNAME: �񤭹��ߤ��꤬�Ȥ��������ޤ���");

    }

    if ($SYS_F_V) {
	&cgiprint'Cache(<<__EOF__);
<form action="$PROGRAM" method="POST">
<input name="b" type="hidden" value="$BOARD">
<input name="c" type="hidden" value="v">
<input name="num" type="hidden" value="$DEF_TITLE_NUM">
<input type="submit" value="$H_BACKTITLE">
</form>
__EOF__
    }

    if ($SYS_F_E && ($Id ne '')) {
	&cgiprint'Cache(<<__EOF__);
<form action="$PROGRAM" method="POST">
<input name="b" type="hidden" value="$BOARD">
<input name="c" type="hidden" value="e">
<input name="id" type="hidden" value="$Id">
<input type="submit" value="$H_ORIG��$H_MESG��">
</form>
__EOF__
    }

    &MsgFooter;

}


###
## ShowArticle - ñ�쵭����ɽ��
#
# - SYNOPSIS
#	ShowArticle;
#
# - ARGS
#	�ʤ�
#
# - DESCRIPTION
#	ñ��ε�����ɽ�����롥
#       ����ѿ��Ǥ��롤CGI�ѿ��򻲾Ȥ��롥
#
# - RETURN
#	�ʤ�
#
sub ShowArticle {

    local($Id, $Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $DateUtc, $Aid, @AidList, @FollowIdTree);

    $Id = $cgi'TAGS{'id'};
    ($Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url) = &GetArticlesInfo($Id);
    $DateUtc = &GetUtcFromOldDateTimeFormat($Date);
    @AidList = split(/,/, $Aids);

    # ̤��Ƶ������ɤ�ʤ�
    if ($Name eq '') { &Fatal(8, ''); }

    # ɽ�����̤κ���
    &MsgHeader('Message view', "$BOARDNAME: $Subject", $DateUtc);
    &ViewOriginalArticle($Id, 1, 1);

    # article end
    &cgiprint'Cache("$H_LINE\n<p>\n");

    # ȿ������
    &cgiprint'Cache("��$H_REPLY\n");
    if ($Aids ne '') {

	# ȿ������������ʤ��
	foreach $Aid (@AidList) {

	    # �ե����������ڹ�¤�μ���
	    # ex. '( a ( b ( c d ) ) ( e ) ( f ( g ) ) )'�Ȥ����ꥹ��
	    @FollowIdTree = &GetFollowIdTree($Aid);

	    # �ᥤ��ؿ��θƤӽФ�(��������)
	    &ThreadArticleMain('subject only', @FollowIdTree);

	}

    } else {

	# ȿ������̵��
	&cgiprint'Cache("<ul>\n<li>$H_REPLY�Ϥ���ޤ���\n</ul>\n");

    }

    &cgiprint'Cache("</p>\n");

    # ����«
    &MsgFooter;

}


###
## ThreadArticle - �ե�������������ɽ����
#
# - SYNOPSIS
#	ThreadArticle;
#
# - ARGS
#	�ʤ�
#
# - DESCRIPTION
#	���뵭���ȡ����ε����ؤΥ�ץ饤������ޤȤ��ɽ�����롥
#       ����ѿ��Ǥ��롤CGI�ѿ��򻲾Ȥ��롥
#
# - RETURN
#	�ʤ�
#
sub ThreadArticle {

    local($Id, @FollowIdTree);

    $Id = $cgi'TAGS{'id'};

    # �ե����������ڹ�¤�μ���
    # ex. '( a ( b ( c d ) ) ( e ) ( f ( g ) ) )'�Ȥ����ꥹ��
    @FollowIdTree = &GetFollowIdTree($Id);

    # ɽ�����̤κ���
    &MsgHeader('Message view (threaded)', "$BOARDNAME: $H_REPLY��ޤȤ��ɤ�");

    # �ᥤ��ؿ��θƤӽФ�(��������)
    &ThreadArticleMain('subject only', @FollowIdTree);

    # �ᥤ��ؿ��θƤӽФ�(����)
    &ThreadArticleMain('', @FollowIdTree);

    &MsgFooter;

}

sub ThreadArticleMain {
    local($SubjectOnly, $Head, @Tail) = @_;

    # �������פ����������Τ�Τ���
    if ($SubjectOnly) {

	if ($Head eq '(') {
	    &cgiprint'Cache("<ul>\n");
	} elsif ($Head eq ')') {
	    &cgiprint'Cache("</ul>\n");
	} else {
	    local($dFid, $dAids, $dDate, $dSubject, $dIcon, $dRemoteHost, $dName) = &GetArticlesInfo($Head);
	    &cgiprint'Cache("<li>" . &GetFormattedTitle($Head, $BOARD, $dAids, $dIcon, $dSubject, $dName, $dDate) . "\n");
	}

    } else {

	if (($Head ne '(') && ($Head ne ')')) {
	    # ��������ɽ��(���ޥ���դ�, �������ʤ�)
	    &cgiprint'Cache("<hr>\n");
	    &ViewOriginalArticle($Head, 1, 0);
	}

    }

    # �Ƶ�
    if (@Tail) {
	&ThreadArticleMain($SubjectOnly, @Tail);
    }

}


###
## ShowIcon - ��������ɽ������
#
# - SYNOPSIS
#	ShowIcon;
#
# - ARGS
#	�ʤ�
#
# - DESCRIPTION
#	��������ɽ�����̤�ɽ�����롥
#	����ѿ��Ǥ��롤CGI�ѿ��򻲾Ȥ��롥
#
# - RETURN
#	�ʤ�
#
sub ShowIcon {

    local($IconTitle, $Type);

    # �����פ򽦤�
    $Type = $cgi'TAGS{'type'};

    # ɽ�����̤κ���
    &MsgHeader('Icon show', "$BOARDNAME: �������������");

    if ($Type eq 'article') {

	&cgiprint'Cache(<<__EOF__);
<p>
�ƥ�������ϼ��ε�ǽ��ɽ���Ƥ��ޤ���
</p>
<ul>
<p>
<li><img src="$ICON_BLIST" alt="$H_BACKBOARD" height="$COMICON_HEIGHT" width="$COMICON_WIDTH"> : $H_BACKBOARD
<li><img src="$ICON_TLIST" alt="$H_BACKTITLE" height="$COMICON_HEIGHT" width="$COMICON_WIDTH"> : $H_BACKTITLE
<li><img src="$ICON_PREV" alt="$H_PREVARTICLE" height="$COMICON_HEIGHT" width="$COMICON_WIDTH"> : $H_PREVARTICLE
<li><img src="$ICON_NEXT" alt="$H_NEXTARTICLE" height="$COMICON_HEIGHT" width="$COMICON_WIDTH"> : $H_NEXTARTICLE
<li><img src="$ICON_THREAD" alt="$H_READREPLYALL" height="$COMICON_HEIGHT" width="$COMICON_WIDTH"> : $H_READREPLYALL
</p><p>
<li><img src="$ICON_WRITENEW" alt="$H_POSTNEWARTICLE" height="$COMICON_HEIGHT" width="$COMICON_WIDTH"> : $H_POSTNEWARTICLE
<li><img src="$ICON_FOLLOW" alt="$H_REPLYTHISARTICLE" height="$COMICON_HEIGHT" width="$COMICON_WIDTH"> : $H_REPLYTHISARTICLE
<li><img src="$ICON_QUOTE" alt="$H_REPLYTHISARTICLEQUOTE" height="$COMICON_HEIGHT" width="$COMICON_WIDTH"> : $H_REPLYTHISARTICLEQUOTE
</p>
</ul>
__EOF__

    } else {

	&cashIconDB($BOARD);	# ��������DB�Υ���å���

	&cgiprint'Cache(<<__EOF__);
<p>
�ƥ�������ϼ��ε�ǽ��ɽ���Ƥ��ޤ���
<p>
<ul>
<li>$H_THREAD : ����$H_MESG��$H_REPLY��ޤȤ���ɤ�
</ul>
</p>
<p>
$H_BOARD��$BOARDNAME�פǤϡ����Υ��������Ȥ����Ȥ��Ǥ��ޤ���
</p>
<p>
<ul>
__EOF__
	foreach $IconTitle (sort keys(%ICON_FILE)) {
	    &cgiprint'Cache(sprintf("<li><img src=\"%s\" alt=\"$IconTitle\" height=\"$MSGICON_HEIGHT\" width=\"$MSGICON_WIDTH\"> : %s\n", &GetIconURLFromTitle($IconTitle, $BOARD), ($ICON_HELP{$IconTitle} || $IconTitle)));
	}
	&cgiprint'Cache("</ul>\n</p>\n");

    }

    &MsgFooter;

}


###
## SortArticle - ���ս�˥�����
#
# - SYNOPSIS
#	SortArticle;
#
# - ARGS
#	�ʤ�
#
# - DESCRIPTION
#	�����ȥ���������ս�˥����Ȥ���ɽ�����롥
#	����ѿ��Ǥ��롤CGI�ѿ��򻲾Ȥ��롥
#
# - RETURN
#	�ʤ�
#
sub SortArticle {

    local($Num, $Old, $NextOld, $BackOld, $To, $From, $IdNum, $Id);

    # ɽ������Ŀ������
    $Num = $cgi'TAGS{'num'};
    $Old = $cgi'TAGS{'old'};
    $NextOld = ($Old > $Num) ? ($Old - $Num) : 0;
    $BackOld = ($Old + $Num);
    $To = $#DB_ID - $Old;
    $From = $To - $Num + 1; $From = 0 if (($From < 0) || ($Num == 0));

    # ɽ�����̤κ���
    &MsgHeader('Title view (sorted)', "$BOARDNAME: $H_SUBJECT����(���ս�)");

    &BoardHeader('normal');

    &cgiprint'Cache("<hr>\n");

    if ($SYS_BOTTOMTITLE) {
	&cgiprint'Cache("<p>$H_TOP<a href=\"$PROGRAM?b=$BOARD&c=r&num=$Num&old=$BackOld\">$H_BACKART</a></p>\n") if ($From > 0);
    } else {
	&cgiprint'Cache("<p>$H_TOP<a href=\"$PROGRAM?b=$BOARD&c=r&num=$Num&old=$NextOld\">$H_NEXTART</a></p>\n") if ($Old);
    }

    &cgiprint'Cache("<p><ul>\n");

    # ������ɽ��
    if ($#DB_ID == -1) {

	# �����ä��ġ�
	&cgiprint'Cache("<li>$H_NOARTICLE\n");

    } else {

	if ($SYS_BOTTOMTITLE) {
	    for ($IdNum = $From; $IdNum <= $To; $IdNum++) {
		$Id = $DB_ID[$IdNum];
		&cgiprint'Cache("<li>" . &GetFormattedTitle($Id, $BOARD, $DB_AIDS{$Id}, $DB_ICON{$Id}, $DB_TITLE{$Id}, $DB_NAME{$Id}, $DB_DATE{$Id}) . "\n");
	    }
	} else {
	    for ($IdNum = $To; $IdNum >= $From; $IdNum--) {
		$Id = $DB_ID[$IdNum];
		&cgiprint'Cache("<li>" . &GetFormattedTitle($Id, $BOARD, $DB_AIDS{$Id}, $DB_ICON{$Id}, $DB_TITLE{$Id}, $DB_NAME{$Id}, $DB_DATE{$Id}) . "\n");
	    }
	}
    }

    &cgiprint'Cache("</ul></p>\n");

    if ($SYS_BOTTOMTITLE) {
	&cgiprint'Cache("<p>$H_BOTTOM<a href=\"$PROGRAM?b=$BOARD&c=r&num=$Num&old=$NextOld\">$H_NEXTART</a></p>\n") if ($Old);
    } else {
	&cgiprint'Cache("<p>$H_BOTTOM<a href=\"$PROGRAM?b=$BOARD&c=r&num=$Num&old=$BackOld\">$H_BACKART</a></p>\n") if ($From > 0);
    }

    &MsgFooter;

}


###
## ViewTitle - ����å���ɽ��
#
# - SYNOPSIS
#	ViewTitle($ComType);
#
# - ARGS
#	$ComType	ɽ�����̤Υ�����
#				����ʤ� ... �������Ȳ���
#				maint ...... ������������
#				linkto ..... ��󥯤���������������
#				linkexec ... ��󥯤��������»�
#				moveto ..... ��ư��������
#				moveexec ... ��ư�»�
#
# - DESCRIPTION
#	�����������Υ����ȥ�򥹥�å��̤˥����Ȥ���ɽ����
#	����ѿ��Ǥ��롤CGI�ѿ��򻲾Ȥ��롥
#	����ѿ�ADDFLAG(����ɽ�����Ƥ��ޤä����ݤ���ɽ�魯�ե饰)���˲����롥
#
# - RETURN
#	�ʤ�
#
sub ViewTitle {
    local($ComType) = @_;
    local($Num, $Old, $NextOld, $BackOld, $To, $From, $IdNum, $Id, $Fid, $IdNum, $Id, $NextCommand, $FirstFlag, $Key, $Value, $AddNum);
    %ADDFLAG = ();		# it's static.

    if ($ComType eq 'linkexec') {
	# ��󥯤��������μ»�
	&ReLinkExec($cgi'TAGS{'rfid'}, $cgi'TAGS{'rtid'}, $BOARD);
    } elsif ($ComType eq 'moveexec') {
	# ��ư�μ»�
	&ReOrderExec($cgi'TAGS{'rfid'}, $cgi'TAGS{'rtid'}, $BOARD);
    }

    # ɽ������Ŀ������
    $Num = $cgi'TAGS{'num'};
    $Old = $cgi'TAGS{'old'};
    $NextOld = ($Old > $Num) ? ($Old - $Num) : 0;
    $BackOld = ($Old + $Num);
    $To = $#DB_ID - $Old;
    $From = $To - $Num + 1; $From = 0 if (($From < 0) || ($Num == 0));

    # �����Ѥߥե饰
    # 0 ... �����оݳ�
    # 1 ... �����Ѥ�
    # 2 ... ̤����
    for($IdNum = $From; $IdNum <= $To; $IdNum++) { $ADDFLAG{$DB_ID[$IdNum]} = 2; }

    # ��/����ޥ��
    $FirstFlag = 1;
    $NextCommand = '?';
    while (($Key, $Value) = each %cgi'TAGS) {
	# ����Ϣ�ϥ��å�
	next if (($Key eq 'num') || ($Key eq 'old'));
	if ($FirstFlag) { $FirstFlag = 0; } else { $NextCommand .= "&"; }
	$NextCommand .= "$Key=$Value";
    }

    # �ڡ�������ʸ����
    $AddNum = "&num=" . $cgi'TAGS{'num'} . "&old=" . $cgi'TAGS{'old'};

    # ɽ�����̤κ���
    if ($ComType eq 'linkto') {
	&MsgHeader('Title view (threaded)', "$BOARDNAME: �����ʥ�ץ饤��λ���");
    } elsif ($ComType eq 'linkexec') {
	&MsgHeader('Title view (threaded)', "$BOARDNAME: ���ꤵ�줿$H_MESG�Υ�ץ饤����ѹ����ޤ���");
    } elsif ($ComType eq 'moveto') {
	&MsgHeader('Title view (threaded)', "$BOARDNAME: ��ư��λ���");
    } elsif ($ComType eq 'moveexec') {
	&MsgHeader('Title view (threaded)', "$BOARDNAME: ���ꤵ�줿$H_MESG���ư���ޤ���");
    } else {
	&MsgHeader('Title view (threaded)', "$BOARDNAME: $H_SUBJECT����($H_REPLY��)");
    }

    if ($ComType) {
	&BoardHeader('maint');
    } else {
	&BoardHeader('normal');
    }

    &cgiprint'Cache("<p>\n<ul>\n<li><a href=\"$PROGRAM?b=$BOARD&c=ce&rtid=" . $cgi'TAGS{'roid'} . "&rfid=" . $cgi'TAGS{'rfid'} . "\">�����ѹ��򸵤��᤹</a>\n</ul>\n</p>") if ($ComType eq 'linkexec');

    if ($ComType) {
	&cgiprint'Cache(<<__EOF__);
<p>�ƥ�������ϡ����Τ褦�ʰ�̣��ɽ���Ƥ��ޤ���
<dl compact>
<dt>$H_RELINKFROM_MARK
<dd>����$H_MESG��$H_REPLY����ѹ����ޤ���$H_REPLY�����ꤹ����̤����Ӥޤ���
<dt>$H_REORDERFROM_MARK
<dd>����$H_MESG�ν�����ѹ����ޤ�����ư�����ꤹ����̤����Ӥޤ���
<dt>$H_DELETE_ICON
<dd>����$H_MESG�������ޤ���
<dt>$H_SUPERSEDE_ICON
<dd>����$H_MESG���������ޤ���
<dt>$H_RELINKTO_MARK
<dd>��˻��ꤷ��$H_MESG��$H_REPLY��򡤤���$H_MESG�ˤ��ޤ���
<dt>$H_REORDERTO_MARK
<dd>��˻��ꤷ��$H_MESG�򡤤���$H_MESG�β��˰�ư���ޤ���
</dl></p>
__EOF__
    }

    if ($ComType eq 'linkto') {
	&cgiprint'Cache("<p>" . $cgi'TAGS{'rfid'} . "�򡤤ɤ�$H_MESG�ؤΥ�ץ饤�ˤ��ޤ���? ��ץ饤���$H_MESG��$H_RELINKTO_MARK�򥯥�å����Ƥ���������</p>\n");
    } elsif ($ComType eq 'moveto') {
	&cgiprint'Cache("<p>" . $cgi'TAGS{'rfid'} . "�򡤤ɤ�$H_MESG�β��˰�ư���ޤ���? $H_MESG��$H_REORDERTO_MARK�򥯥�å����Ƥ���������</p>\n");
    }

    &cgiprint'Cache("<hr>\n");

    if ($SYS_BOTTOMTITLE) {
	&cgiprint'Cache("<p>$H_TOP<a href=\"$PROGRAM?b=$BOARD&c=v&num=$Num&old=$BackOld\">$H_BACKART</a></p>\n") if ($From > 0);
    } else {
	&cgiprint'Cache("<p>$H_TOP<a href=\"$PROGRAM?b=$BOARD&c=v&num=$Num&old=$NextOld\">$H_NEXTART</a></p>\n") if ($Old);
    }

    &cgiprint'Cache("<p><ul>\n");

    if ($To < $From) {

	# �����ä��ġ�
	&cgiprint'Cache("<li>$H_NOARTICLE\n");

    } elsif ($SYS_BOTTOMTITLE) {

	# �Ť��Τ������
	&cgiprint'Cache("<li><a href=\"$PROGRAM?b=$BOARD&c=ce&rtid=&rfid=" . $cgi'TAGS{'rfid'} . "&roid=" . $cgi'TAGS{'roid'} . "$AddNum\">[�ɤ�$H_MESG�ؤΥ�ץ饤�Ǥ�ʤ�������$H_MESG�ˤ���]</a>\n") if (($ComType eq 'linkto') && ($DB_FID{$cgi'TAGS{'rfid'}} ne ''));
	&cgiprint'Cache("<li><a href=\"$PROGRAM?b=$BOARD&c=mve&rtid=&rfid=" . $cgi'TAGS{'rfid'} . "&roid=" . $cgi'TAGS{'roid'} . "$AddNum\">[����������Ƭ�˰�ư����(���Υڡ�������Ƭ���ǤϤ���ޤ���)]</a>\n") if ($ComType eq 'moveto');

	for($IdNum = $From; $IdNum <= $To; $IdNum++) {

	    # ����������ID����Ф�
	    $Id = $DB_ID[$IdNum];
	    ($Fid = $DB_FID{$Id}) =~ s/,.*$//o;
	    # �������Ȥϸ�󤷡�
	    next if (($Fid ne '') && ($ADDFLAG{$Fid} == 2));
	    # �Ρ��ɤ�ɽ��
	    if ($ComType) {
		&ViewTitleNodeMaint($Id, $ComType, $AddNum);
	    } else {
		&ViewTitleNode($Id);
	    }
	}
    } else {

	# �������Τ������
	&cgiprint'Cache("<li><a href=\"$PROGRAM?b=$BOARD&c=ce&rtid=&rfid=" . $cgi'TAGS{'rfid'} . "&roid=" . $cgi'TAGS{'roid'} . "$AddNum\">[�ɤ�$H_MESG�ؤΥ�ץ饤�Ǥ�ʤ�������$H_MESG�ˤ���]</a>\n") if (($ComType eq 'linkto') && ($DB_FID{$cgi'TAGS{'rfid'}} ne ''));
	&cgiprint'Cache("<li><a href=\"$PROGRAM?b=$BOARD&c=mve&rtid=&rfid=" . $cgi'TAGS{'rfid'} . "&roid=" . $cgi'TAGS{'roid'} . "$AddNum\">[����������Ƭ�˰�ư����(���Υڡ�������Ƭ���ǤϤ���ޤ���)]</a>\n") if ($ComType eq 'moveto');

	for($IdNum = $To; $IdNum >= $From; $IdNum--) {
	    # ���Ʊ��
	    $Id = $DB_ID[$IdNum];
	    ($Fid = $DB_FID{$Id}) =~ s/,.*$//o;
	    next if (($Fid ne '') && ($ADDFLAG{$Fid} == 2));
	    if ($ComType) {
		&ViewTitleNodeMaint($Id, $ComType, $AddNum);
	    } else {
		&ViewTitleNode($Id);
	    }
	}
    }

    &cgiprint'Cache("</ul></p>\n");

    if ($SYS_BOTTOMTITLE) {
	&cgiprint'Cache("<p>$H_BOTTOM<a href=\"$PROGRAM?b=$BOARD&c=v&num=$Num&old=$NextOld\">$H_NEXTART</a></p>\n") if ($Old);
    } else {
	&cgiprint'Cache("<p>$H_BOTTOM<a href=\"$PROGRAM?b=$BOARD&c=v&num=$Num&old=$BackOld\">$H_BACKART</a></p>\n") if ($From > 0);
    }

    &MsgFooter;

    undef(%ADDFLAG);

}

sub ViewTitleNode {
    local($Id) = @_;

    if ($ADDFLAG{$Id} != 2) { return; }

    &cgiprint'Cache("<li>" . &GetFormattedTitle($Id, $BOARD, $DB_AIDS{$Id}, $DB_ICON{$Id}, $DB_TITLE{$Id}, $DB_NAME{$Id}, $DB_DATE{$Id}) . "\n");
    $ADDFLAG{$Id} = 1;		# �����Ѥ�

    # ̼�����Сġ�
    if ($DB_AIDS{$Id}) {
	&cgiprint'Cache("<ul>\n");
	foreach (split(/,/, $DB_AIDS{$Id})) { &ViewTitleNode($_); }
	&cgiprint'Cache("</ul>\n");
    }
}

sub ViewTitleNodeMaint {

    local($Id, $ComType, $AddNum) = @_;

    return if ($ADDFLAG{$Id} != 2);

    local($FromId) = $cgi'TAGS{'rfid'};

    &cgiprint'Cache("<li>" . &GetFormattedTitle($Id, $BOARD, $DB_AIDS{$Id}, $DB_ICON{$Id}, $DB_TITLE{$Id}, $DB_NAME{$Id}, $DB_DATE{$Id})); #'

    &cgiprint'Cache(" .......... \n");

    # ������ѹ����ޥ��(From)
    if ($SYS_F_LI) {
	&cgiprint'Cache("<a href=\"$PROGRAM?b=$BOARD&c=ct&rfid=$Id&roid=" . $DB_FID{$Id} . "$AddNum\">$H_RELINKFROM_MARK</a>\n");
    }

    # ��ư���ޥ��(From)
    if ($SYS_F_MV) {
	&cgiprint'Cache("<a href=\"$PROGRAM?b=$BOARD&c=mvt&rfid=$Id&roid=" . $DB_FID{$Id} . "$AddNum\">$H_REORDERFROM_MARK</a>\n") if ($DB_FID{$Id} eq '');
    }

    # ������ޥ��
    if ($SYS_F_D) {
	&cgiprint'Cache("<a href=\"$PROGRAM?b=$BOARD&c=dp&id=$Id\">$H_DELETE_ICON</a>\n");
    }

    # �������ޥ��
    if ($SYS_F_SS) {
	&cgiprint'Cache("<a href=\"$PROGRAM?b=$BOARD&c=f&s=on&id=$Id\">$H_SUPERSEDE_ICON</a>\n");
    }

    # ��ư���ޥ��(To)
    if ($SYS_F_MV && ($ComType eq 'moveto') && ($FromId ne $Id) && ($DB_FID{$Id} eq '') && ($FromId ne $Id)) {
	&cgiprint'Cache("<a href=\"$PROGRAM?b=$BOARD&c=mve&rtid=$Id&rfid=$FromId&roid=" . $cgi'TAGS{'roid'} . "$AddNum\">$H_REORDERTO_MARK</a>\n");
    }

    # ������ѹ����ޥ��(To)
    if ($SYS_F_LI && ($ComType eq 'linkto') && ($FromId ne $Id) && (! grep(/^$FromId$/, split(/,/, $DB_AIDS{$Id}))) && (! grep(/^$FromId$/, split(/,/, $DB_FID{$Id})))) {
	&cgiprint'Cache("<a href=\"$PROGRAM?b=$BOARD&c=ce&rtid=$Id&rfid=$FromId&roid=" . $cgi'TAGS{'roid'} . "$AddNum\">$H_RELINKTO_MARK</a>\n");
    }

    $ADDFLAG{$Id} = 1;		# �����Ѥ�

    # ̼�����Сġ�
    if ($DB_AIDS{$Id}) {
	&cgiprint'Cache("<ul>\n");
	foreach (split(/,/, $DB_AIDS{$Id})) { &ViewTitleNodeMaint($_, $ComType, $AddNum); }
	&cgiprint'Cache("</ul>\n");
    }
}


###
## NewArticle - ������������ޤȤ��ɽ��
#
# - SYNOPSIS
#	NewArticle;
#
# - ARGS
#	�ʤ�
#
# - DESCRIPTION
#	������������ޤȤ��ɽ����
#	����ѿ��Ǥ��롤CGI�ѿ��򻲾Ȥ��롥
#
# - RETURN
#	�ʤ�
#
sub NewArticle {

    local($Num, $Old, $NextOld, $BackOld, $To, $From, $Id);

    # ɽ������Ŀ������
    $Num = $cgi'TAGS{'num'};
    $Old = $cgi'TAGS{'old'};
    $NextOld = ($Old > $Num) ? ($Old - $Num) : 0;
    $BackOld = ($Old + $Num);
    $To = $#DB_ID - $Old;
    $From = $To - $Num + 1; $From = 0 if (($From < 0) || ($Num == 0));

    # ɽ�����̤κ���
    &MsgHeader('Message view (sorted)', "$BOARDNAME: �Ƕ��$H_MESG��ޤȤ��ɤ�");

    if ($SYS_BOTTOMARTICLE) {
	&cgiprint'Cache("<p>$H_TOP<a href=\"$PROGRAM?b=$BOARD&c=l&num=$Num&old=$BackOld\">$H_BACKART</a></p>\n") if ($From > 0);
    } else {
	&cgiprint'Cache("<p>$H_TOP<a href=\"$PROGRAM?b=$BOARD&c=l&num=$Num&old=$NextOld\">$H_NEXTART</a></p>\n") if ($Old);
    }

    if (! $#DB_ID == -1) {

	# �����ä��ġ�
	&cgiprint'Cache("<p>$H_NOARTICLE</p>\n");

    } else {

	if ($SYS_BOTTOMARTICLE) {
	    for ($IdNum = $From; $IdNum <= $To; $IdNum++) {
		$Id = $DB_ID[$IdNum];
		&ViewOriginalArticle($Id, 1, 1);
		&cgiprint'Cache("<hr>\n");
	    }
	} else {
	    for ($IdNum = $To; $IdNum >= $From; $IdNum--) {
		$Id = $DB_ID[$IdNum];
		&ViewOriginalArticle($Id, 1, 1);
		&cgiprint'Cache("<hr>\n");
	    }
	}

    }

    if ($SYS_BOTTOMARTICLE) {
	&cgiprint'Cache("<p>$H_BOTTOM<a href=\"$PROGRAM?b=$BOARD&c=l&num=$Num&old=$NextOld\">$H_NEXTART</a></p>\n") if ($Old);
    } else {
	&cgiprint'Cache("<p>$H_BOTTOM<a href=\"$PROGRAM?b=$BOARD&c=l&num=$Num&old=$BackOld\">$H_BACKART</a></p>\n") if ($From > 0);
    }

    if ($SYS_F_V) {
	&cgiprint'Cache(<<__EOF__);
<form action="$PROGRAM" method="POST">
<input name="b" type="hidden" value="$BOARD">
<input name="c" type="hidden" value="v">
<input name="num" type="hidden" value="$DEF_TITLE_NUM">
<input type="submit" value="$H_BACKTITLE">
</form>
__EOF__
    }

    &MsgFooter;

}


###
## SearchArticle - �����θ���(ɽ�����̤κ���)
#
# - SYNOPSIS
#	SearchArticle;
#
# - ARGS
#	�ʤ�
#
# - DESCRIPTION
#	�����򸡺�����(������ɽ�����̤κ�����ʬ)��
#	����ѿ��Ǥ��롤CGI�ѿ��򻲾Ȥ��롥
#
# - RETURN
#	�ʤ�
#
sub SearchArticle {

    local($Key, $SearchSubject, $SearchPerson, $SearchArticle, $SearchIcon, $Icon, $IconTitle);

    $Key = $cgi'TAGS{'key'};
    $SearchSubject = $cgi'TAGS{'searchsubject'};
    $SearchPerson = $cgi'TAGS{'searchperson'};
    $SearchArticle = $cgi'TAGS{'searcharticle'};
    $SearchIcon = $cgi'TAGS{'searchicon'};
    $Icon = $cgi'TAGS{'icon'};

    # ɽ�����̤κ���
    &MsgHeader('Message search', "$BOARDNAME: $H_MESG�θ���");

    # ����«
    &cgiprint'Cache(<<__EOF__);
<form action="$PROGRAM\" method="POST">
<input name="c" type="hidden" value="s">
<input name="b" type="hidden" value="$BOARD">
 
<p>
<ul>
<li>��$H_SUBJECT�ס���̾���ס���$H_MESG�פ��椫�顤���������ϰϤ�����å����Ƥ���������
���ꤵ�줿�ϰϤǡ�������ɤ�ޤ�$H_MESG�����ɽ�����ޤ���
<li>������ɤˤϡ���ʸ����ʸ���ζ��̤Ϥ���ޤ���
<li>������ɤ�Ⱦ�ѥ��ڡ����Ƕ��ڤäơ�ʣ���Υ�����ɤ���ꤹ��ȡ�
��������Ƥ�ޤ�$H_MESG�Τߤ򸡺����뤳�Ȥ��Ǥ��ޤ���
<li>��������Ǹ���������ϡ�
�֥�������פ�����å������塤õ������$H_MESG�Υ������������Ǥ���������
</ul>
</p>
<input type="submit" value="��������">
<input type="reset" value="�ꥻ�åȤ���">

<p>�������:
<input name="key" type="text" size="$KEYWORD_LENGTH" value="$Key">
</p>

<p>�����ϰ�:
<ul>
__EOF__

    &cgiprint'Cache(sprintf("<li><input name=\"searchsubject\" type=\"checkbox\" value=\"on\" %s>: $H_SUBJECT\n", (($SearchSubject) ? 'CHECKED' : '')));
    &cgiprint'Cache(sprintf("<li><input name=\"searchperson\" type=\"checkbox\" value=\"on\" %s>: ̾��\n", (($SearchPerson) ? 'CHECKED' : '')));
    &cgiprint'Cache(sprintf("<li><input name=\"searcharticle\" type=\"checkbox\" value=\"on\" %s>: $H_MESG", (($SearchArticle) ? 'CHECKED' : '')));

    &cgiprint'Cache(sprintf("<li><input name=\"searchicon\" type=\"checkbox\" value=\"on\" %s>: $H_ICON // ", (($SearchIcon) ? 'CHECKED' : '')));

    # �������������
    &cashIconDB($BOARD);	# ��������DB�Υ���å���
    &cgiprint'Cache(sprintf("<SELECT NAME=\"icon\">\n<OPTION%s>$H_NOICON\n", (($Icon && ($Icon ne $H_NOICON)) ? '' : ' SELECTED')));
    foreach $IconTitle (sort keys(%ICON_FILE)) {
	&cgiprint'Cache(sprintf("<OPTION%s>$IconTitle\n", (($Icon eq $IconTitle) ? ' SELECTED' : '')));
    }
    &cgiprint'Cache("</SELECT>\n");

    # �����������
    &cgiprint'Cache(<<__EOF__);
(<a href="$PROGRAM?b=$BOARD&c=i&type=entry">�������������</a>)<BR>
</ul>
</p>
</form>
<hr>
__EOF__

    # ������ɤ����Ǥʤ���С����Υ�����ɤ�ޤ൭���Υꥹ�Ȥ�ɽ��
    if (($SearchIcon ne '') || (($Key ne '') && ($SearchSubject || ($SearchPerson || $SearchArticle)))) {
	&SearchArticleList($Key, $SearchSubject, $SearchPerson, $SearchArticle, $SearchIcon, $Icon);
    }

    &MsgFooter;

}

sub SearchArticleList {
    local($Key, $Subject, $Person, $Article, $Icon, $IconType) = @_;
    local($dId, $dAids, $dDate, $dTitle, $dIcon, $dName, $dEmail, $HitNum, $Line, $SubjectFlag, $PersonFlag, $ArticleFlag, @KeyList);

    @KeyList = split(/ +/, $Key);

    # �ꥹ�ȳ���
    &cgiprint'Cache("<p><ul>\n");

    foreach ($[ .. $#DB_ID) {

	# ��������
	$dId = $DB_ID[$_];
	$dIcon = $DB_ICON{$dId};
	$dTitle = $DB_TITLE{$dId};
	$dName = $DB_NAME{$dId};
	$dEmail = $DB_EMAIL{$dId};
	$dAids = $DB_AIDS{$dId};
	$dDate = $DB_DATE{$dId};

	# �ѿ��Υꥻ�å�
	$SubjectFlag = $PersonFlag = $ArticleFlag = 0;
	$Line = '';

	# URL�����å�
	next if (&IsUrl($dId));

	# ������������å�
	next if (($Icon ne '') && ($dIcon ne $IconType));

	if ($Key ne '') {

	    # �����ȥ�򸡺�
	    if (($Subject ne '') && ($dTitle ne '')) {
		$SubjectFlag = 1;
		foreach (@KeyList) {
		    if ($dTitle !~ /$_/i) {
			$SubjectFlag = 0;
		    }
		}
	    }

	    # ��Ƽ�̾�򸡺�
	    if (($Person ne '') && ($dName ne '')) {
		$PersonFlag = 1;
		foreach (@KeyList) {
		    if (($dName !~ /$_/i) && ($dEmail !~ /$_/i)) {
			$PersonFlag = 0;
		    }
		}
	    }

	    # ��ʸ�򸡺�
	    if (($Article ne '') && ($Line = &SearchArticleKeyword($dId, $BOARD, @KeyList))) {
		$ArticleFlag = 1;
	    }

	} else {

	    # ̵���ǰ���
	    $SubjectFlag = 1;

	}

	if ($SubjectFlag || $PersonFlag || $ArticleFlag) {

	    # ����1�ĤϹ��פ���
	    $HitNum++;

	    # �����ؤΥ�󥯤�ɽ��
	    &cgiprint'Cache("<li>" . &GetFormattedTitle($dId, $BOARD, $dAids, $dIcon, $dTitle, $dName, $dDate) . "\n");

	    # ��ʸ�˹��פ���������ʸ��ɽ��
	    if ($ArticleFlag) {
		$Line =~ s/<[^>]*>//go;
		&cgiprint'Cache("<blockquote>$Line</blockquote>\n");
	    }
	}
    }

    # �ҥåȤ��ʤ��ä���
    if ($HitNum) {
	&cgiprint'Cache("</ul>\n</p><p>\n<ul>");
	&cgiprint'Cache("<li>$HitNum���$H_MESG�����Ĥ���ޤ�����\n");
    } else {
	&cgiprint'Cache("<li>��������$H_MESG�ϸ��Ĥ���ޤ���Ǥ�����\n");
    }

    # �ꥹ���Ĥ���
    &cgiprint'Cache("</ul></p>\n");
}


###
## AliasNew - �����ꥢ������Ͽ���ѹ����̤�ɽ��
#
# - SYNOPSIS
#	AliasNew;
#
# - ARGS
#	�ʤ�
#
# - DESCRIPTION
#	�����ꥢ������Ͽ���ѹ����̤�ɽ������(ɽ���������)��
#
# - RETURN
#	�ʤ�
#
sub AliasNew {

    # ɽ�����̤κ���
    &MsgHeader('Alias entry/edit', "$H_ALIAS����Ͽ/�ѹ�/���");

    # ������Ͽ/��Ͽ���Ƥ��ѹ�
    &cgiprint'Cache(<<__EOF__);
<p>
������Ͽ/��Ͽ���Ƥ��ѹ�
</p>
<p>
<form action="$PROGRAM" method="POST">
<input name="c" type="hidden" value="am">
$H_ALIAS: <input name="alias" type="text" value="#" size="$NAME_LENGTH"><br>
$H_FROM: <input name="name" type="text" size="$NAME_LENGTH"><br>
$H_MAIL: <input name="email" type="text" size="$MAIL_LENGTH"><br>
$H_URL_S: <input name="url" type="text" value="http://" size="$URL_LENGTH"><br>
$H_ALIAS�ο�����Ͽ/��Ͽ���Ƥ��ѹ���Ԥʤ��ޤ���
�����ꥢ����(���ʤ��ʳ���!)ï�ˤǤ�񤭴����뤳�Ȥ��Ǥ��ޤ���
��Ͽ���Ƥ��ѹ�����Ƥ��ʤ����ɤ�����
�񤭹�����Ρֻ��ɽ������ײ��̤���դ��ƥ����å����Ƥ���������
�ޤ����ְ�ä�Ʊ�������ꥢ������Ͽ����Ƥ��ޤ�ʤ��褦�ˡ�
���ޤ�˴�ñ�ʡ֥����ꥢ���פ��򤱤Ƥ��������͡�<br>
<input type="submit" value="��Ͽ/�ѹ�����">
</form>
</p>
<hr>
<p>
���
</p>
<p>
<form action="$PROGRAM" method="POST">
<input name="c" type="hidden" value="ad">
$H_ALIAS: <input name="alias" type="text" size="$NAME_LENGTH"><br>
�嵭$H_ALIAS�������ޤ���<br>
<input type="submit" value="�������">
</form>
</p>
<hr>
<p>
<form action="$PROGRAM" method="POST">
<input name="c" type="hidden" value="as">
<input type="submit" value="$H_ALIAS�����򻲾Ȥ���">
</form>
</p>
__EOF__
    
    # ����«
    &MsgFooter;

}


###
## AliasMod - �桼�������ꥢ������Ͽ/�ѹ�
#
# - SYNOPSIS
#	AliasMod;
#
# - ARGS
#	�ʤ�
#
# - DESCRIPTION
#	�桼�������ꥢ������Ͽ/�ѹ��������η�̤��Τ餻����̤�ɽ�����롥
#	����ѿ��Ǥ��롤CGI�ѿ��򻲾Ȥ��롥
#	���ץꥱ��������ǥ�Ȥ⡤GUI�Ȥ����ġ�ʬΥ�Ǥ��Ƥʤ���
#
# - RETURN
#	�ʤ�
#
sub AliasMod {

    local($A, $N, $E, $U, $HitFlag, $Alias);

    $A = $cgi'TAGS{'alias'};
    $N = $cgi'TAGS{'name'};
    $E = $cgi'TAGS{'email'};
    $U = $cgi'TAGS{'url'};
    
    # �ޥ��󤬥ޥå�������
    #	0 ... �����ꥢ�����ޥå����ʤ�
    #	2 ... �ޥå����ƥǡ������ѹ�����
    $HitFlag = 0;

    # ʸ��������å�
    &AliasCheck($A, $N, $E, $U);
    
    # �����ꥢ�����ɤ߹���
    &CashAliasData;
    
    # 1�Ԥ��ĥ����å�
    foreach $Alias (sort keys(%Name)) {
	next if ($A ne $Alias);
	$HitFlag = 2;		# ��ä���2�����ꡥ�ޥ���̾��̵�롥
    }
    
    # ������Ͽ
    if ($HitFlag == 0) {
	$Alias = $A;
    }
    
    # �ǡ�������Ͽ
    $Name{$Alias} = $N;
    $Email{$Alias} = $E;
    $Host{$Alias} = $REMOTE_HOST;
    $URL{$Alias} = $U;
    
    # �����ꥢ���ե�����˽񤭽Ф�
    &WriteAliasData;

    # ɽ�����̤κ���
    &MsgHeader('Alias modified', "$H_ALIAS�����ꤵ��ޤ���");
    &cgiprint'Cache("<p>$H_ALIAS: <strong>$A</strong>:\n");
    if ($HitFlag == 2) {
	&cgiprint'Cache("���ꤷ�ޤ�����</p>\n");
    } else {
	&cgiprint'Cache("��Ͽ���ޤ�����</p>\n");
    }
    &MsgFooter;
    
}


###
## AliasDel - �桼�������ꥢ���κ��
#
# - SYNOPSIS
#	AliasDel;
#
# - ARGS
#	�ʤ�
#
# - DESCRIPTION
#	�桼�������ꥢ���������롥��Ͽ�ۥ��Ȥ�Ʊ��Ǥʤ�����Բġ�
#	���θ塤���η�̤��Τ餻����̤�ɽ�����롥
#	����ѿ��Ǥ��롤CGI�ѿ��򻲾Ȥ��롥
#	���ץꥱ��������ǥ�Ȥ⡤GUI�Ȥ���롥ʬΥ�Ǥ��Ƥʤ���
#
# - RETURN
#	�ʤ�
#
sub AliasDel {

    local($A, $HitFlag, $Alias);

    # �����ꥢ��
    $A = $cgi'TAGS{'alias'};

    # �ޥ��󤬥ޥå�������
    #	0 ... �����ꥢ�����ޥå����ʤ�
    #	2 ... �ޥå����ƥǡ������ѹ�����
    $HitFlag = 0;

    # �����ꥢ�����ɤ߹���
    &CashAliasData;
    
    # 1�Ԥ��ĥ����å�
    foreach $Alias (sort keys(%Name)) {
	next if ($A ne $Alias);
	$HitFlag = 2;		# �ҥåȤ�����2�����ꡥ�ޥ���̾��̵�롥
    }
    
    # �����ꥢ�����ʤ�!
    if ($HitFlag == 0) { &Fatal(6, $A); }
    
    # ̾����ä�
    $Name{$A} = '';
    
    # �����ꥢ���ե�����˽񤭽Ф�
    &WriteAliasData;
    
    # ɽ�����̤κ���
    &MsgHeader('Alias deleted', "$H_ALIAS���������ޤ���");
    &cgiprint'Cache("<p>$H_ALIAS: <strong>$A</strong>: �õ�ޤ�����</p>\n");
    &MsgFooter;

}


###
## AliasShow - �桼�������ꥢ�����Ȳ��̤�ɽ��
#
# - SYNOPSIS
#	AliasShow;
#
# - ARGS
#	�ʤ�
#
# - DESCRIPTION
#	�桼�������ꥢ���ΰ�����ɽ��������̤�������롥
#
# - RETURN
#	�ʤ�
#
sub AliasShow {

    local($Alias);

    # �����ꥢ�����ɤ߹���
    &CashAliasData;
    
    # ɽ�����̤κ���
    &MsgHeader('Alias view', "$H_ALIAS�λ���");

    # ������ʸ
    if ($SYS_ALIAS == 1) {
	&cgiprint'Cache(<<__EOF__);
<p>
��Ƥκݡ���$H_FROM�פ���ʬ�˰ʲ�����Ͽ̾(��#....��)�����Ϥ���ȡ�
��Ͽ����Ƥ���$H_FROM��$H_MAIL��$H_URL����ưŪ������ޤ���
</p><p>
<a href="$PROGRAM?c=an">������Ͽ/��Ͽ���Ƥ��ѹ�</a>
</p>
__EOF__

    } elsif ($SYS_ALIAS == 2) {
					  
	&cgiprint'Cache(<<__EOF__);
<p>
��Ƥκݡ���$H_USER�פǰʲ�����Ͽ̾(��#....��)����ꤹ��ȡ�
��Ͽ����Ƥ���$H_FROM��$H_MAIL��$H_URL����ưŪ������ޤ���
</p><p>
<a href="$PROGRAM?c=an">������Ͽ/��Ͽ���Ƥ��ѹ�</a>
</p>
__EOF__

    } else {
	# ���ꤨ�ʤ����Ϥ�
	&Fatal(9999, '');
    }

    # �ꥹ�ȳ���
    &cgiprint'Cache("<dl>\n");
    
    # 1�Ĥ���ɽ��
    foreach $Alias (sort keys(%Name)) {
	&cgiprint'Cache(<<__EOF__);
<p>
<dt><strong>$Alias</strong>
<dd>$H_FROM: $Name{$Alias}
<dd>$H_MAIL: $Email{$Alias}
<dd>$H_URL: $URL{$Alias}
</p>
__EOF__

    }

    # �ꥹ���Ĥ���
    &cgiprint'Cache("</dl>\n");
    
    &MsgFooter;

}


###
## DeletePreview - ��������γ�ǧ
#
# - SYNOPSIS
#	DeletePreview;
#
# - ARGS
#	�ʤ�
#
# - DESCRIPTION
#	��������γ�ǧ���̤�ɽ������
#       ����ѿ��Ǥ��롤CGI�ѿ��򻲾Ȥ��롥
#
# - RETURN
#	�ʤ�
#
sub DeletePreview {

    local($Id);

    $Id = $cgi'TAGS{'id'};

    # ɽ�����̤κ���
    &MsgHeader("Delete Article", "$BOARDNAME: $H_MESG�κ��");

    &cgiprint'Cache(<<__EOF__);
<p>
�����ˤ���$H_MESG��������ΤǤ���? �������Хܥ���򲡤��Ƥ���������
</p>
__EOF__

    # ����«
    &cgiprint'Cache(<<__EOF__);
<form action="$PROGRAM" method="POST">
<input name="c" type="hidden" value="de">
<input name="b" type="hidden" value="$BOARD">
<input name="id" type="hidden" value="$Id">
<input type="submit" value="���ε����������ޤ�">
</form>
<form action="$PROGRAM" method="POST">
<input name="c" type="hidden" value="det">
<input name="b" type="hidden" value="$BOARD">
<input name="id" type="hidden" value="$Id">
<input type="submit" value="��ץ饤������ޤȤ�ƺ�����ޤ�">
</form>
</p>
<hr>
__EOF__

    # ����ե������ɽ��
    &ViewOriginalArticle($Id, 0, 1);

    # ����«
    &MsgFooter;

}


###
## DeleteExec - �����κ��
#
# - SYNOPSIS
#	DeleteExec($ThreadFlag);
#
# - ARGS
#	$ThreadFlag	��ץ饤��ä����ݤ�
#
# - DESCRIPTION
#	�����κ����¹Ԥ��������β��̤�ɽ�����롥
#       ����ѿ��Ǥ��롤CGI�ѿ��򻲾Ȥ��롥
#
# - RETURN
#	�ʤ�
#
sub DeleteExec {
    local($ThreadFlag) = @_;
    local($Id);

    $Id = $cgi'TAGS{'id'};

    # ����¹�
    &DeleteArticle($Id, $ThreadFlag);

    # ɽ�����̤κ���
    &MsgHeader('Message deleted', "$BOARDNAME: $H_MESG���������ޤ���");

    &cgiprint'Cache(<<__EOF__);
<form action="$PROGRAM" method="POST">
<input name="b" type="hidden" value="$BOARD">
<input name="c" type="hidden" value="v">
<input name="num" type="hidden" value="$DEF_TITLE_NUM">
<input type="submit" value="$H_BACKTITLE">
</form>
__EOF__

    # ����«
    &MsgFooter;

}


###
## ArriveMailEntry - �ᥤ�뼫ư�ۿ���λ���
#
# - SYNOPSIS
#	ArriveMailEntry;
#
# - ARGS
#	�ʤ�
#
# - DESCRIPTION
#	�ᥤ�뼫ư�ۿ���λ�����̤�ɽ�����롥
#
# - RETURN
#	�ʤ�
#
sub ArriveMailEntry {

    local(@ArriveMail);

    &getArriveMailTo(1, $BOARD, *ArriveMail); # ����ȥ����Ȥ���Ф�

    &MsgHeader("ArriveMail Entry", "$BOARDNAME: ��ư�ᥤ���ۿ��������");

    &cgiprint'Cache(<<__EOF__);
<p>
����$H_BOARD��$H_MESG���񤭹��ޤ줿���ˡ�
��ư�ǥᥤ����ۿ����밸��Υᥤ�륢�ɥ쥹�����ꤷ�ޤ���
1�Ԥ�1�ᥤ�륢�ɥ쥹���Ľ񤭹���Ǥ���������
��Ƭ�ˡ�#�פ�Ĥ���Ȥ��ιԤ�̵�뤵���Τǡ�
#��³���ƥ����Ȥ�񤭹��ळ�Ȥ�Ǥ��ޤ���
</p><p>
�ä˼³��Ϥ���ޤ��󤬡�̵��̣�ʶ��Ԥ����ꤹ���ʤ��褦����դ��ޤ��礦��
</p><p>
<form action="$PROGRAM" method="POST">
<input name="c" type="hidden" value="me">
<input name="b" type="hidden" value="$BOARD">
<textarea name="armail" rows="$TEXT_ROWS" cols="$MAIL_LENGTH">
__EOF__

    foreach(@ArriveMail) { &cgiprint'Cache($_); }

    &cgiprint'Cache(<<__EOF__);
</textarea><br>
<input type="submit" value="���ꤷ�ޤ�">
<input type="reset" value="�ꥻ�åȤ���">
</form>
</p>
__EOF__

    &MsgFooter;

}



###
## ArriveMailExec - �ᥤ�뼫ư�ۿ��������
#
# - SYNOPSIS
#	ArriveMailExec;
#
# - ARGS
#	�ʤ�
#
# - DESCRIPTION
#	�ᥤ�뼫ư�ۿ�������ꤹ�롥
#	����ѿ��Ǥ��롤CGI�ѿ��򻲾Ȥ��롥
#
# - RETURN
#	�ʤ�
#
sub ArriveMailExec {

    local(@ArriveMail);

    @ArriveMail = split(/\n/, $cgi'TAGS{'armail'}); # ����ꥹ�Ȥ���Ф�
    &updateArriveMailDb($BOARD, *ArriveMail); # DB�򹹿�����

    &MsgHeader("ArriveMail Changed", "$BOARDNAME: ��ư�ᥤ���ۿ�������ꤷ�ޤ���");

    &cgiprint'Cache(<<__EOF__);
<p>
����$H_BOARD��$H_MESG���񤭹��ޤ줿���ˡ���ư�ǥᥤ����ۿ����밸���
�ʲ��Τ褦�����ꤷ�ޤ�����
</p><p>
<pre>
--------------------
__EOF__

    foreach(@ArriveMail) { &cgiprint'Cache("$_\n"); }

    &cgiprint'Cache(<<__EOF__);
--------------------
</pre></p>
<form action="$PROGRAM" method="POST">
<input name="b" type="hidden" value="$BOARD">
<input name="c" type="hidden" value="v">
<input name="num" type="hidden" value="$DEF_TITLE_NUM">
<input type="submit" value="$H_BACKTITLE">
</form>
__EOF__

    &MsgFooter;

}


######################################################################
# �桼�����󥿥ե���������ץ���ơ������(������)


###
## Fatal - ���顼ɽ��
#
# - SYNOPSIS
#	Fatal($FatalNo, $FatalInfo);
#
# - ARGS
#	$FatalNo	���顼�ֹ�(�ܤ����ϴؿ������򻲾ȤΤ���)
#	$FatalInfo	���顼����
#
# - DESCRIPTION
#	���顼��ɽ�����̤�֥饦�����������롥
#
# - RETURN
#	�ʤ�
#
sub Fatal {
    local($FatalNo, $FatalInfo) = @_;
    local($ErrString);

    if ($FatalNo == 1) {

	$ErrString = "File: $FatalInfo��¸�ߤ��ʤ������뤤��permission�����꤬�ְ�äƤ��ޤ���������Ǥ�����<a href=\"mailto:$MAINT\">$MAINT</a>�ޤǡ��嵭�ե�����̾���Τ餻��������";

    } elsif ($FatalNo == 2) {

	$ErrString = "���Ϥ���Ƥ��ʤ����ܤ�����ޤ�����äƤ⤦���٤��ľ���ƤߤƤ���������";

    } elsif ($FatalNo == 3) {

	$ErrString = "���̾�����ᥤ�륢�ɥ쥹�ˡ�����ʸ�������Ԥ����äƤ��ޤäƤ��ޤ�����äƤ⤦���٤��ľ���ƤߤƤ���������";

    } elsif ($FatalNo == 4) {

	$ErrString = "�����HTML����������ʸ��������ʸ��������뤳�Ȥ϶ؤ����Ƥ��ޤ�����äư㤦��˽񤭴����Ƥ���������";

    } elsif ($FatalNo == 5) {

	$ErrString = "��Ͽ����Ƥ��륨���ꥢ���Τ�Τȡ��ޥ���̾�����פ��ޤ��󡥤�����Ǥ�����<a href=\"mailto:$MAINT\">$MAINT</a>�ޤǸ�Ϣ����������";

    } elsif ($FatalNo == 6) {

	$ErrString = "��$FatalInfo�פȤ��������ꥢ���ϡ���Ͽ����Ƥ��ޤ���";

    } elsif ($FatalNo == 7) {

	$ErrString = "$FatalInfo��������������ޤ���? ��äƤ⤦���٤��ľ���ƤߤƤ���������";

    } elsif ($FatalNo == 8) {

	$ErrString = "���ε����Ϥޤ���Ƥ���Ƥ��ޤ���";

    } elsif ($FatalNo == 9) {

	$ErrString = "�ᥤ�뤬�����Ǥ��ޤ���Ǥ�����������Ǥ��������Υ��顼��å������ȡ����顼��������������<a href=\"mailto:$MAINT\">$MAINT</a>�ޤǤ��Τ餻����������";

    } elsif ($FatalNo == 10) {

	$ErrString = ".db��.articleid�������������Ƥ��ޤ��󡥤�����Ǥ��������Υ��顼��å������ȡ����顼��������������<a href=\"mailto:$MAINT\">$MAINT</a>�ޤǤ��Τ餻����������";

    } elsif ($FatalNo == 11) {

	$ErrString = "$FatalInfo�Ȥ���ID���б�����$H_BOARD�ϡ�¸�ߤ��ޤ���";

    } elsif ($FatalNo == 50) {

	$ErrString = "��ץ饤�ط����۴Ĥ��Ƥ��ޤ��ޤ����ɤ����Ƥ��ץ饤����ѹ���������硤��ץ饤�����ٿ��尷���ˤ��Ƥ��顤��ץ饤�򤫤������Ƥ���������";

    } elsif ($FatalNo == 99) {

	$ErrString ="����$H_BOARD�Ǥϡ����Υ��ޥ�ɤϼ¹ԤǤ��ޤ���";

    } elsif ($FatalNo == 999) {

	$ErrString ="�����ƥ�Υ�å��˼��Ԥ��ޤ��������߹�äƤ���褦�Ǥ��Τǡ���ʬ�ԤäƤ���⤦���٥����������Ƥ������������٥����������Ƥ��å�����Ƥ����硤���ƥʥ���Ǥ����ǽ���⤢��ޤ���";

    } else {

	$ErrString = "���顼�ֹ�����: $FatalInfo<br>������Ǥ��������Υ��顼��å������ȡ����顼��������������<a href=\"mailto:$mEmail\">$mEmail</a>�ޤǤ��Τ餻����������";

    }

    # �۾ｪλ�β�ǽ��������Τǡ��Ȥꤢ����lock�򳰤�
    # (��å��μ��Ԥλ��ʳ�)
    if ($FatalNo != 999) { &cgi'unlock($LOCK_FILE); }

    # ɽ�����̤κ���
    &MsgHeader('Error!', "$SYSTEM_NAME: ERROR!");

    &cgiprint'Cache("<p>$ErrString</p>\n");

    if ($SYS_F_V && ($BOARD ne '')) {
	&cgiprint'Cache(<<__EOF__);
<form action="$PROGRAM" method="POST">
<input name="b" type="hidden" value="$BOARD">
<input name="c" type="hidden" value="v">
<input name="num" type="hidden" value="$DEF_TITLE_NUM">
<input type="submit" value="$H_BACKTITLE">
</form>
__EOF__
    }

    &MsgFooter;
    exit(0);
}


###
## ViewOriginalArticle - ��������ɽ��
#
# - SYNOPSIS
#	ViewOriginalArticle($Id, $CommandFlag, $OriginalFlag);
#
# - ARGS
#	$Id			����ID
#	$CommandFlag		���ޥ�ɤ�ɽ�����뤫�ݤ�(ɽ������=1)
#	$OriginalFlag		���ε�����ˡ�(�����)�������ؤΥ�󥯤�
#				ɽ�����뤫�ݤ�(ɽ������=1)
#
# - DESCRIPTION
#	��������ɽ�����롥
#
# - RETURN
#	�ʤ�
#
sub ViewOriginalArticle {
    local($Id, $CommandFlag, $OriginalFlag) = @_;
    local($Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $PrevId, $NextId, $Num, $InputDate, @ArticleBody);

    ($Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url) = &GetArticlesInfo($Id);

    foreach ($[ .. $#DB_ID) { $Num = $_, last if ($DB_ID[$_] eq $Id); }
    $PrevId = $DB_ID[$Num - 1] if ($Num > $[);
    $NextId = $DB_ID[$Num + 1];

    # ���ޥ��ɽ��?
    if ($CommandFlag && $SYS_COMMAND) {

	&cgiprint'Cache("<p>\n");

	if ($SYS_COMICON == 2) {

	    if ($SYS_F_B) {
		&cgiprint'Cache("<a href=\"$BOARDLIST_URL\"><img src=\"$ICON_BLIST\" alt=\"$H_BACKBOARD\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\">$H_BACKBOARD</a>\n");
	    }

	    if ($SYS_F_V) {
		&cgiprint'Cache(" | <a href=\"$PROGRAM?b=$BOARD&c=v&num=$DEF_TITLE_NUM\"><img src=\"$ICON_TLIST\" alt=\"$H_BACKTITLE\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\">$H_BACKTITLE</a>\n");
	    }

	    if ($SYS_F_E) {
		if ($PrevId ne '') {
		    &cgiprint'Cache(" | <a href=\"$PROGRAM?b=$BOARD&c=e&id=$PrevId\"><img src=\"$ICON_PREV\" alt=\"$H_PREVARTICLE\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\">$H_PREVARTICLE</a>\n");
		} else {
		    &cgiprint'Cache(" | <img src=\"$ICON_PREV\" alt=\"$H_PREVARTICLE\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\">$H_PREVARTICLE\n");
		}

		if ($NextId ne '') {
		    &cgiprint'Cache(" | <a href=\"$PROGRAM?b=$BOARD&c=e&id=$NextId\"><img src=\"$ICON_NEXT\" alt=\"$H_NEXTARTICLE\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\">$H_NEXTARTICLE</a>\n");
		} else {
		    &cgiprint'Cache(" | <img src=\"$ICON_NEXT\" alt=\"$H_NEXTARTICLE\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\">$H_NEXTARTICLE\n");
		}
	    }

	    if ($SYS_F_T) {
		if ($Aids ne '') {
		    &cgiprint'Cache(" | <a href=\"$PROGRAM?b=$BOARD&c=t&id=$Id\"><img src=\"$ICON_THREAD\" alt=\"$H_READREPLYALL\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\">$H_READREPLYALL</a>\n");
		} else {
		    &cgiprint'Cache(" | <img src=\"$ICON_THREAD\" alt=\"$H_READREPLYALL\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\">$H_READREPLYALL\n");
		}
	    }

	    if ($SYS_F_N) {
		&cgiprint'Cache(" | <a href=\"$PROGRAM?b=$BOARD&c=n\"><img src=\"$ICON_WRITENEW\" alt=\"$H_POSTNEWARTICLE\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\">$H_POSTNEWARTICLE</a>\n");
	    }    

	    if ($SYS_F_FQ) {
		&cgiprint'Cache(<<__EOF__);
 | <a href="$PROGRAM?b=$BOARD&c=f&id=$Id"><img src="$ICON_FOLLOW" alt="$H_REPLYTHISARTICLE" width="$COMICON_WIDTH" height="$COMICON_HEIGHT" BORDER="0">$H_REPLYTHISARTICLE</a>
 | <a href="$PROGRAM?b=$BOARD&c=q&id=$Id"><img src="$ICON_QUOTE" alt="$H_REPLYTHISARTICLEQUOTE" width="$COMICON_WIDTH" height="$COMICON_HEIGHT" BORDER="0">$H_REPLYTHISARTICLEQUOTE</a>
__EOF__
	    }

	    &cgiprint'Cache(" | <a href=\"$PROGRAM?b=$BOARD&c=i&type=article\"><img src=\"$ICON_HELP\" alt=\"?\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\">?</a>\n");

	} elsif ($SYS_COMICON == 1) {

	    if ($SYS_F_B) {
		&cgiprint'Cache("<a href=\"$BOARDLIST_URL\"><img src=\"$ICON_BLIST\" alt=\"$H_BACKBOARD\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\"></a>\n");
	    }

	    if ($SYS_F_V) {
		&cgiprint'Cache("<a href=\"$PROGRAM?b=$BOARD&c=v&num=$DEF_TITLE_NUM\"><img src=\"$ICON_TLIST\" alt=\"$H_BACKTITLE\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\"></a>\n");
	    }

	    if ($SYS_F_E) {
		if ($PrevId ne '') {
		    &cgiprint'Cache("<a href=\"$PROGRAM?b=$BOARD&c=e&id=$PrevId\"><img src=\"$ICON_PREV\" alt=\"$H_PREVARTICLE\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\"></a>\n");
		} else {
		    &cgiprint'Cache("<img src=\"$ICON_PREV\" alt=\"$H_PREVARTICLE\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\">\n");
		}

		if ($NextId ne '') {
		    &cgiprint'Cache("<a href=\"$PROGRAM?b=$BOARD&c=e&id=$NextId\"><img src=\"$ICON_NEXT\" alt=\"$H_NEXTARTICLE\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\"></a>\n");
		} else {
		    &cgiprint'Cache("<img src=\"$ICON_NEXT\" alt=\"$H_NEXTARTICLE\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\">\n");
		}
	    }

	    if ($SYS_F_T) {
		if ($Aids ne '') {
		    &cgiprint'Cache("<a href=\"$PROGRAM?b=$BOARD&c=t&id=$Id\"><img src=\"$ICON_THREAD\" alt=\"$H_READREPLYALL\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\"></a>\n");
		} else {
		    &cgiprint'Cache("<img src=\"$ICON_THREAD\" alt=\"$H_READREPLYALL\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\">\n");
		}
	    }

	    &cgiprint'Cache(" // \n");

	    if ($SYS_F_N) {
		&cgiprint'Cache(<<__EOF__);
<a href="$PROGRAM?b=$BOARD&c=n"><img src="$ICON_WRITENEW" alt="$H_POSTNEWARTICLE" width="$COMICON_WIDTH" height="$COMICON_HEIGHT" BORDER="0"></a>
__EOF__
	    }    

	    if ($SYS_F_FQ) {
		&cgiprint'Cache(<<__EOF__);
<a href="$PROGRAM?b=$BOARD&c=f&id=$Id"><img src="$ICON_FOLLOW" alt="$H_REPLYTHISARTICLE" width="$COMICON_WIDTH" height="$COMICON_HEIGHT" BORDER="0"></a>
<a href="$PROGRAM?b=$BOARD&c=q&id=$Id"><img src="$ICON_QUOTE" alt="$H_REPLYTHISARTICLEQUOTE" width="$COMICON_WIDTH" height="$COMICON_HEIGHT" BORDER="0"></a>
__EOF__
	    }

	    &cgiprint'Cache(" // \n");

	    &cgiprint'Cache("<a href=\"$PROGRAM?b=$BOARD&c=i&type=article\"><img src=\"$ICON_HELP\" alt=\"?\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\"></a>\n");

	} else {

	    if ($SYS_F_B) {
		&cgiprint'Cache("<a href=\"$BOARDLIST_URL\">$H_BACKBOARD</a>\n");
	    }

	    if ($SYS_F_V) {
		&cgiprint'Cache(" | <a href=\"$PROGRAM?b=$BOARD&c=v&num=$DEF_TITLE_NUM\">$H_BACKTITLE</a>\n");
	    }

	    if ($SYS_F_E) {
		if ($PrevId ne '') {
		    &cgiprint'Cache(" | <a href=\"$PROGRAM?b=$BOARD&c=e&id=$PrevId\">$H_PREVARTICLE</a>\n");
		} else {
		    &cgiprint'Cache(" | $H_PREVARTICLE\n");
		}

		if ($NextId ne '') {
		    &cgiprint'Cache(" | <a href=\"$PROGRAM?b=$BOARD&c=e&id=$NextId\">$H_NEXTARTICLE</a>\n");
		} else {
		    &cgiprint'Cache(" | $H_NEXTARTICLE\n");
		}
	    }

	    if ($SYS_F_T) {
		if ($Aids ne '') {
		    &cgiprint'Cache(" | <a href=\"$PROGRAM?b=$BOARD&c=t&id=$Id\">$H_READREPLYALL</a>");
		} else {
		    &cgiprint'Cache(" | $H_READREPLYALL");
		}
	    }

	    if ($SYS_F_N) {
		&cgiprint'Cache(" | <a href=\"$PROGRAM?b=$BOARD&c=n\">$H_POSTNEWARTICLE</a>\n");
	    }

	    if ($SYS_F_FQ) {
		&cgiprint'Cache(<<__EOF__);
 | <a href="$PROGRAM?b=$BOARD&c=f&id=$Id">$H_REPLYTHISARTICLE</a>
 | <a href="$PROGRAM?b=$BOARD&c=q&id=$Id">$H_REPLYTHISARTICLEQUOTE</a>
__EOF__
	    }

	}

	&cgiprint'Cache("</p>\n");

    }

    &cgiprint'Cache("<p>\n");

    # �ܡ���̾�ȵ����ֹ桤��
    if (($Icon eq $H_NOICON) || ($Icon eq '')) {
	&cgiprint'Cache("<strong>$H_SUBJECT</strong>: <strong>$Id .</strong> $Subject");
    } else {
	&cgiprint'Cache(sprintf("<strong>$H_SUBJECT</strong>: <strong>$Id .</strong> <img src=\"%s\" alt=\"$Icon \" width=\"$MSGICON_WIDTH\" height=\"$MSGICON_HEIGHT\">$Subject", &GetIconURLFromTitle($Icon, $BOARD)));
    }

    # ��̾��
    if (($Url eq '') || ($Url eq 'http://')) {
	# ��http://���ä���פȤ����Τϵ�С������ؤ��н补���Τ����������ͽ�ꡥ
        # URL���ʤ����
        &cgiprint'Cache("<br>\n<strong>$H_FROM</strong>: $Name");
    } else {
        # URL��������
        &cgiprint'Cache("<br>\n<strong>$H_FROM</strong>: <a href=\"$Url\">$Name</a>");
    }

    # �ᥤ��
    if ($Email ne '') {
	&cgiprint'Cache(" <a href=\"mailto:$Email\">&lt;$Email&gt;</a>");
    }

    # �ޥ���
    if ($SYS_SHOWHOST) {
	&cgiprint'Cache("<br>\n<strong>$H_HOST</strong>: $RemoteHost");
    }

    # �����
    $InputDate = &GetDateTimeFormatFromUtc($Date);
    &cgiprint'Cache("<br>\n<strong>$H_DATE</strong>: $InputDate");

    # ȿ����(���Ѥξ��)
    if ($OriginalFlag && ($Fid ne '')) {
	&ShowLinksToFollowedArticle(split(/,/, $Fid));
    }

    # �ڤ���
    &cgiprint'Cache("</p>\n$H_LINE\n");

    # ���������
    &getArticleBody($Id, $BOARD, *ArticleBody);
    foreach(@ArticleBody) { &cgiprint'Cache($_); }

}


###
## QuoteOriginalArticle - ���Ѥ���(�����䤢��)
#
# - SYNOPSIS
#	QuoteOriginalArticle($Id);
#
# - ARGS
#	$Id		����ID
#
# - DESCRIPTION
#	��������Ѥ���ɽ������
#
# - RETURN
#	�ʤ�
#
sub QuoteOriginalArticle {
    local($Id) = @_;
    local($Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $pFid, $pAids, $pDate, $pSubject, $pIcon, $pRemoteHost, $pName, $QMark, @ArticleBody);

    # ����������μ���
    ($Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name) = &GetArticlesInfo($Id);

    # �������Τ���˸���������
    if ($Fid) {
	$Fid =~ s/,.*$//o;
	($pFid, $pAids, $pDate, $pSubject, $pIcon, $pRemoteHost, $pName) = &GetArticlesInfo($Fid);
    }

    # ����
    &getArticleBody($Id, $BOARD, *ArticleBody);
    foreach(@ArticleBody) {
	s/[\&\"]//go;		# ���ѤΤ�����Ѵ�
	s/<[^>]*>//go;		# ���ѤΤ�����Ѵ�

	# �ǥե���Ȥΰ���ʸ����ϡ�̾���� + �� ] ��
	$QMark = "${Name}$DEFAULT_QMARK";

	# ��ʸ�Τ�����������ʬ�ˤϡ������˰���ʸ�����Ťͤʤ�
	# ���Ԥˤ��פ�ʤ�
	if ((/^$/o) || (/^$pName\s*$DEFAULT_QMARK/)) { $QMark = ''; }

	# ����ʸ�����ɽ��
	&cgiprint'Cache(sprintf("%s%s", $QMark, $_));
    }
}


###
## QuoteOriginalArticleWithoutQMark - ���Ѥ���(������ʤ�)
#
# - SYNOPSIS
#	QuoteOriginalArticleWithoutQMark($Id);
#
# - ARGS
#	$Id		����ID
#
# - DESCRIPTION
#	��������Ѥ���ɽ������
#
# - RETURN
#	�ʤ�
#
sub QuoteOriginalArticleWithoutQMark {
    local($Id) = @_;
    local(@ArticleBody);

    &getArticleBody($Id, $BOARD, *ArticleBody);
    foreach(@ArticleBody) {
	s/[\&\"]//go;		# ���ѤΤ�����Ѵ�
	s/<[^>]*>//go;		# ���ѤΤ�����Ѵ�
	&cgiprint'Cache($_);
    }
}


###
## BoardHeader - �Ǽ��ĥإå���ɽ��
#
# - SYNOPSIS
#	BoardHeader($Type);
#
# - ARGS
#	$Type	�Ǽ��ĥإå��Υ�����
#			'normal' ... �̾�
#			'maint' .... ������
#
# - DESCRIPTION
#	�Ǽ��ĤΥإå���ɽ�����롥
#
# - RETURN
#	�ʤ�
#
sub BoardHeader {
    local($Type) = @_;
    local(@BoardHeader);

    &getBoardHeader($BOARD, *BoardHeader);
    foreach(@BoardHeader) { &cgiprint'Cache($_); }

    if ($SYS_F_MT && ($Type eq 'normal')) {
	&cgiprint'Cache(<<__EOF__);
<p>
<ul>
<li><a href="$PROGRAM?c=vm&b=$BOARD&num=$DEF_TITLE_NUM">�����ѤΥ����ȥ�������̤�</a>
</ul>
</p>
__EOF__
    } elsif ($Type eq 'maint') {
	&cgiprint'Cache("<p>\n<ul>\n");
	if ($SYS_F_AM) {
	    &cgiprint'Cache("<li><a href=\"$PROGRAM?c=mp&b=$BOARD\">��ư�ᥤ���ۿ�������ꤹ��</a>\n");
	}
	&cgiprint'Cache("<li><a href=\"$PROGRAM?c=v&b=$BOARD&num=$DEF_TITLE_NUM\">�̾�Υ����ȥ������</a>\n</ul>\n</p>\n");
    }
}


###
## ShowLinksToFollowedArticle - �����������ɽ��
#
# - SYNOPSIS
#	ShowLinksToFollowedArticle(@IdList);
#
# - ARGS
#	@IdList		��ץ饤����ID�Υꥹ��(�Ť���ץ饤�ۤ������ˤ���)
#
# - DESCRIPTION
#	�����������ɽ�����롥
#
# - RETURN
#	�ʤ�
#
sub ShowLinksToFollowedArticle {
    local(@IdList) = @_;
    local($Id, $Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name);

    # ���ꥸ�ʥ뵭��
    if ($#IdList > 0) {
	$Id = $IdList[$#IdList];
	($Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name) = &GetArticlesInfo($Id);
	&cgiprint'Cache("<br>\n<strong>$H_ORIG_TOP:</strong> " . &GetFormattedTitle($Id, $BOARD, $Aids, $Icon, $Subject, $Name, $Date));
    }

    # ������
    $Id = $IdList[0];
    ($Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name) = &GetArticlesInfo($Id);
    &cgiprint'Cache("<br>\n<strong>$H_ORIG:</strong> " . &GetFormattedTitle($Id, $BOARD, $Aids, $Icon, $Subject, $Name, $Date));

}


###
## MsgHeader - HTMLʸ��Υإå���ʬ��ɽ��
#
# - SYNOPSIS
#	MsgHeader($Title, $Message, $LastModified);
#
# - ARGS
#	$Title		HTMLʸ���TITLE(title�����������Τǡ����ΤȤ���
#			US-ASCII�Τߤ��Ƥ������ۤ���̵��)
#	$Message	HTMLʸ��Υ����ȥ�(��ʸ���ɽ������ʸ����)
#	$LastModified	�ǽ���������
#
# - DESCRIPTION
#	HTMLʸ��Υإå���ʬ��ɽ�����롥
#
# - RETURN
#	�ʤ�
#
sub MsgHeader {
    local($Title, $Message, $LastModified) = @_;
    
    &cgi'Header($LastModified);

    &cgiprint'Init;
    &cgiprint'Cache(<<__EOF__);
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML i18n//EN">
<html>
<head>
<title>$Title</title>
<base href="http://$SERVER_NAME$SERVER_PORT_STRING$SYSDIR_NAME">
</head>
__EOF__

    &cgiprint'Cache("<body");
    if ($SYS_NETSCAPE_EXTENSION) {
	&cgiprint'Cache(" background=\"$BG_IMG\"") if $BG_IMG;
	&cgiprint'Cache(" bgcolor=\"$BG_COLOR\"") if $BG_COLOR;
	&cgiprint'Cache(" TEXT=\"$TEXT_COLOR\"") if $TEXT_COLOR;
	&cgiprint'Cache(" LINK=\"$LINK_COLOR\"") if $LINK_COLOR;
	&cgiprint'Cache(" ALINK=\"$ALINK_COLOR\"") if $ALINK_COLOR;
	&cgiprint'Cache(" VLINK=\"$VLINK_COLOR\"") if $VLINK_COLOR;
    }
    &cgiprint'Cache(">\n");

    &cgiprint'Cache(<<__EOF__);
<h1>$Message</h1>
<hr>
__EOF__

}


###
## MsgFooter - HTMLʸ��Υեå���ʬ��ɽ��
#
# - SYNOPSIS
#	MsgFooter;
#
# - ARGS
#	�ʤ�
#
# - DESCRIPTION
#	HTMLʸ��Υեå���ʬ��ɽ�����롥
#
# - RETURN
#	�ʤ�
#
sub MsgFooter {

    &cgiprint'Cache(<<__EOF__);
<hr>
<address>
$ADDRESS
</address>
</body>
</html>
__EOF__

    &cgiprint'Flush;

}


###
## ArriveMail - ���������夷�����Ȥ�ᥤ��
#
# - SYNOPSIS
#	ArriveMail($Name, $Subject, $Id, @To);
#
# - ARGS
#	$Name		����������Ƽ�̾
#	$Subject	��������Subject
#	$Id		��������ID
#	@To		������E-Mail addr�ꥹ��
#
# - DESCRIPTION
#	���������夷�����Ȥ�ᥤ�뤹�롥
#
# - RETURN
#	�ʤ�
#
sub ArriveMail {
    local($Name, $Subject, $Id, @To) = @_;
    local($MailSubject, $Message);

    $MailSubject = "An article was arrived.";

    $Message = "$SYSTEM_NAME����Τ��Τ餻�Ǥ���

��$BOARDNAME�פ��Ф��ơ�$Name�פ��󤫤顤
��$Subject�פȤ�����Ǥν񤭹��ߤ�����ޤ�����

";

    if ($SYS_F_E) {
	$Message .= "�����֤Τ������
$SCRIPT_URL?b=$BOARD&c=e&id=$Id
�������������

";
    }

    $Message .= "�Ǥϼ��餷�ޤ���";

    # �ᥤ������
    &SendMail($MailSubject, $Message, $Id, @To);

}


###
## FollowMail - ȿ�������ä����Ȥ�ᥤ��
#
# - SYNOPSIS
#	FollowMail($Name, $Date, $Subject, $Id, $Fname, $Fsubject, $Fid, @To);
#
# - ARGS
#	$Name		����������Ƽ�̾
#	$Date		��ץ饤���줿�����ν񤭹��߻���
#	$Subject	��������Subject
#	$Id		��������ID
#	$Fname		��ץ饤���줿��������Ƽ�̾
#	$Fsubject	��ץ饤���줿������Subject
#	$Fid		��ץ饤���줿����ID
#	@To		������E-Mail addr�ꥹ��
#
# - DESCRIPTION
#	��ץ饤�����ä����Ȥ�ᥤ�뤹�롥
#
# - RETURN
#	�ʤ�
#
sub FollowMail {
    local($Name, $Date, $Subject, $Id, $Fname, $Fsubject, $Fid, @To) = @_;
    local($MailSubject, $InputDate, $Message);
    
    $MailSubject = "The article was followed.";

    $InputDate = &GetDateTimeFormatFromUtc($Date);

    $Message = "$SYSTEM_NAME����Τ��Τ餻�Ǥ���

$InputDate�ˡ�$BOARDNAME�פ��Ф��ơ�$Name�פ��󤬽񤤤���
��$Subject��
";

    if ($SYS_F_E) {
	$Message .= "$SCRIPT_URL?b=$BOARD&c=e&id=$Id
";
    }

    $Message .= "���Ф��ơ�
��$Fname�פ��󤫤�
��$Fsubject�פȤ�����Ǥ�ȿ��������ޤ�����

";

    if ($SYS_F_E) {
	$Message .= "�����֤Τ������
$SCRIPT_URL?b=$BOARD&c=e&id=$Fid
�������������

";
    }

    $Message .= "�Ǥϼ��餷�ޤ���";

    # �ᥤ������
    &SendMail($MailSubject, $Message, $Fid, @To);

}


###
## SendMail - �ᥤ������
#
# - SYNOPSIS
#	SendMail($Subject, $Message, $Id, @To);
#
# - ARGS
#	$Subject	�ᥤ���Subjectʸ����(���ܸ������ʤ��褦��!)
#	$Message	��ʸ
#	$Id		���Ѥ���ʤ鵭��ID; �ʤ���а��ѤϤʤ�
#	@To		����E-Mail addr.�Υꥹ��
#
# - DESCRIPTION
#	�ᥤ����������롥
#
# - RETURN
#	�ʤ�
#
sub SendMail {
    local($Subject, $Message, $Id, @To) = @_;
    local($ExtensionHeader, @ArticleBody);

    # �ղåإå�������
    $ExtensionHeader = "X-Kb-System: $SYSTEM_NAME\n";
    if ($BOARDNAME && ($Id ne '')) {
	$ExtensionHeader .= "X-Kb-Board: $BOARDNAME\nX-Kb-Articleid: $Id\n";
    }

    # ���ѵ���
    if ($Id ne '') {

	# ���ڤ���
	$Message .= "\n--------------------\n";

	# ����
	&getArticleBody($Id, $BOARD, *ArticleBody);
	foreach(@ArticleBody) {
	    s/<[^>]*>//go;	# �������פ�ʤ�
	    if ($_ ne '') { $Message .= &HTMLDecode($_); }
	}
    }

    # ��������
    &Fatal(9, '') unless (&cgi'SendMail($MAINT_NAME, $MAINT, $Subject, $ExtensionHeader, $Message, @To));

}


######################################################################
# ���ץꥱ��������ǥ륤��ץ���ơ������


###
## MakeNewArticle - ��������Ƥ��줿����������
#
# - SYNOPSIS
#	MakeNewArticle($Board, $Id, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail);
#
# - ARGS
#	$Board		�������뵭��������Ǽ��Ĥ�ID
#	$Id		��ץ饤��������ID
#	$TextType	ʸ�񥿥���
#	$Name		��Ƽ�̾
#	$Email		��Ƽ�E-Mail addr.
#	$Url		��Ƽ�URL
#	$Icon		��������ID
#	$Subject	Subjectʸ����
#	$Article	��ʸʸ����
#	$Fmail		��ץ饤�����ä����˥ᥤ����Τ餻�뤫�ݤ�('on'/'')
#
# - DESCRIPTION
#	��Ƥ��줿�����򵭻�DB���������롥
#
# - RETURN
#	�ʤ�
#
sub MakeNewArticle {
    local($Board, $Id, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail) = @_;
    local($ArticleId);

    # ���Ϥ��줿��������Υ����å�
    $Article = &CheckArticle($Board, $TextType, *Name, *Email, *Url, *Subject, *Icon, $Article);

    # �����������ֹ�����(�ޤ������ֹ�������Ƥʤ�)
    $ArticleId = &GetNewArticleId($Board);

    # �����Υե�����κ���
    &MakeArticleFile($TextType, $Article, $ArticleId, $Board);

    # �����������ֹ��񤭹���
    &WriteArticleId($ArticleId, $Board);

    # DB�ե��������Ƥ��줿�������ɲ�
    # �̾�ε������Ѥʤ�ID
    &AddDBFile($ArticleId, $Board, $Id, $TIME, $Subject, $Icon, $REMOTE_HOST, $Name, $Email, $Url, $Fmail);

}


###
## SearchArticleKeyword - �����θ���(��ʸ)
#
# - SYNOPSIS
#	SearchArticleKeyword($Id, $Board, @KeyList);
#
# - ARGS
#	$Id		��ʸ�򸡺����뵭����ID
#	$Board		�Ǽ���ID
#	@KeyList	������ɥꥹ��
#
# - DESCRIPTION
#	���ꤵ�줿��������ʸ�򡤥�����ɤ�AND�������롥
#
# - RETURN
#	�ǽ�˥�����ɤȥޥå������ԡ��ޥå����ʤ��ä�������֤���
#
sub SearchArticleKeyword {
    local($Id, $Board, @KeyList) = @_;
    local(@NewKeyList, $Line, $Return, $Code, $ConvFlag, @ArticleBody);

    $ConvFlag = ($Id !~ /^\d+$/);

    &getArticleBody($Id, $Board, *ArticleBody);
    foreach(@ArticleBody) {
	$Line = $_;

	# �������Ѵ�
	if ($ConvFlag) {
	    $Code = &jcode'getcode(*Line);
	    &jcode'convert(*Line, 'euc', $Code, 'z');
	}

	# ����
	@NewKeyList = ();
	foreach (@KeyList) {
	    if ($Line =~ /$_/i) {
		# �ޥå�����! 1���ܤʤ�Ф��Ȥ�
		$Return = $Line unless $Return;
	    } else {
		# �ޤ�õ���ʤ���ġ�
		push(@NewKeyList, $_);
	    }
	}
	# ���ʤ�ȴ����
	last unless (@KeyList = @NewKeyList);
    }

    # �ޤ��ĤäƤ��饢���ȡ����ʤ�ǽ�Υޥå������Ԥ��֤���
    return((@KeyList) ? '' : $Return);

}


###
## Version Check - KINOBOARDS��DB�ե�����Υ��������������å�
#
# - SYNOPSIS
#	VersionCheck($FileType, $VersionString);
#
# - ARGS
#	$FileType		�����å��оݤ�DB�ե�����Υ�����
#	$VersionString		������������ɽ�魯ʸ����
#
# - DESCRIPTION
#	KINOBOARDS�ǻȤ��Ƥ���DB�ե�����Υ��������������å���Ԥʤ���
#	�����礬����줿���ˤ��ͤ��֤������֥饦���˥��顼��ɽ�����̤��֤���
#	���ΤȤ����ä˥����å����Ƥ��ʤ�
#	(��������DB�ե�����Υե����ޥåȤ��Ѳ����Ƥ��ʤ�����)��
#
# - RETURN
#	�ʤ�
#
sub VersionCheck {
    local($FileType, $VersionString) = @_;
    local($VersionId, $ReleaseId) = split(/\//, $VersionString);

    # no check now...

}


###
## CheckArticle - ���Ϥ��줿��������Υ����å�
#
# - SYNOPSIS
#	CheckArticle($Board, $TextType, *Name, *Email, *Url, *Subject, *Icon, $Article);
#
# - ARGS
#	$Board		�Ǽ���ID
#	$TextType	ʸ�񥿥���
#	*Name		��Ƽ�̾
#	*Email		�ᥤ�륢�ɥ쥹
#	*Url		URL
#	*Subject	Subject
#	*Icon		��������ID
#	$Article	��ʸ
#
# - DESCRIPTION
#	���Ϥ��줿����������å�����
#
# - RETURN
#	��ʸ
#
sub CheckArticle {
    local($Board, $TextType, *Name, *Email, *Url, *Subject, *Icon, $Article) = @_;
    local($Tmp);

    # �����ꥢ�������å�
    if ($Name =~ /^\#.*$/o) {
        ($Tmp, $Email, $Url) = &GetUserInfo($Name);
	if ($Tmp eq '') { &Fatal(6, $Name); }
	$Name = $Tmp;
    } elsif ($SYS_ALIAS == 2) {
	# ɬ�ܤΤϤ��ʤΤˡ����ꤵ�줿�����ꥢ������Ͽ����Ƥ��ʤ�
	&Fatal(6, $Name);
    }

    # ʸ��������å�
    &CheckName(*Name);
    &CheckEmail(*Email);
    &CheckURL(*Url);
    &CheckSubject(*Subject);

    # �������å�
    if ($Article eq '') { &Fatal(2, ''); }

    # ��������Υ����å�; ������������̵���פ����ꡥ
    if (&GetIconURLFromTitle($Icon, $Board)) { $Icon = $H_NOICON; }

    # �������"�򥨥󥳡���
    $Article = &DQEncode($Article);

    return($Article);

}


###
## AliasCheck - �桼�������ꥢ���Υ����å�
#
# - SYNOPSIS
#	AliasCheck($A, $N, $E, $U);
#
# - ARGS
#	$A	�����ꥢ��̾
#	$N	̾��
#	$E	E-Mail addr.
#	$U	URL
#
# - DESCRIPTION
#	�桼�������ꥢ���Υǡ���(�����ꥢ��̾��̾����E-Mail��URL)
#	������å����롥
#
# - RETURN
#	�ʤ�
#
sub AliasCheck {
    local($A, $N, $E, $U) = @_;

    &CheckAlias(*A);
    &CheckName(*N);
    &CheckEmail(*E);
    &CheckURL(*U);
    
}


###
## CheckAlias - ʸ��������å�: �����ꥢ��
#
# - SYNOPSIS
#	CheckAlias(*String);
#
# - ARGS
#	*String		�����ꥢ��ʸ����
#
# - DESCRIPTION
#	�����ꥢ����ʸ��������å���Ԥʤ���
#	������ʸ������ä��饨�顼ɽ���롼����ء�
#	(���ץꥱ�������/GUI��ʬΥ�����ۤ�����������?)
#
# - RETURN
#	�ʤ�
#
sub CheckAlias {
    local(*String) = @_;

    # �������å�
    if (! $String) { &Fatal(2, ''); }

    # `#'�ǻϤޤäƤ�?
    ($String =~ (/^\#/)) || &Fatal(7, $H_ALIAS);

    # 1ʸ���������
    (length($String) > 1) || &Fatal(7, $H_ALIAS);

}


###
## CheckSubject - ʸ��������å�: Subject
#
# - SYNOPSIS
#	CheckSubject(*String);
#
# - ARGS
#	*String		Subjectʸ����
#
# - DESCRIPTION
#	Subject��ʸ��������å���Ԥʤ���
#	������ʸ������ä��饨�顼ɽ���롼����ء�
#	(���ץꥱ�������/GUI��ʬΥ�����ۤ�����������?)
#
# - RETURN
#	�ʤ�
#
sub CheckSubject {
    local(*String) = @_;

    # �������å�
    if (! $String) { &Fatal(2, ''); }

    # ����������å�
    if ($String =~ m/[<>\t\n]/o) { &Fatal(4, ''); }

}


###
## CheckName - ʸ��������å�: ��Ƽ�̾
#
# - SYNOPSIS
#	CheckName(*String);
#
# - ARGS
#	*String		��Ƽ�̾ʸ����
#
# - DESCRIPTION
#	��Ƽ�̾��ʸ��������å���Ԥʤ���
#	������ʸ������ä��饨�顼ɽ���롼����ء�
#	(���ץꥱ�������/GUI��ʬΥ�����ۤ�����������?)
#
# - RETURN
#	�ʤ�
#
sub CheckName {
    local(*String) = @_;

    # �������å�
    if (! $String) { &Fatal(2, ''); }

    # ���ԥ����ɤ�����å�
    if ($String =~ /[\t\n]/o) { &Fatal(3, ''); }

}


###
## CheckEmail - ʸ��������å�: E-Mail addr.
#
# - SYNOPSIS
#	CheckEmail(*String);
#
# - ARGS
#	*String		E-Mail addr.ʸ����
#
# - DESCRIPTION
#	E-Mail addr.��ʸ��������å���Ԥʤ���
#	������ʸ������ä��饨�顼ɽ���롼����ء�
#	(���ץꥱ�������/GUI��ʬΥ�����ۤ�����������?)
#
# - RETURN
#	�ʤ�
#
sub CheckEmail {
    local(*String) = @_;

    if ($SYS_POSTERMAIL) {

	# �������å�
	if ($String eq '') { &Fatal(2, ''); }

	# `@'�����äƤʤ��㥢����
	if ($String !~ (/@/)) { &Fatal(7, 'E-Mail'); }

    }

    # ���ԥ����ɤ�����å�
    if ($String =~ /[\t\n]/o) { &Fatal(3, ''); }

}


###
## CheckURL - ʸ��������å�: URL
#
# - SYNOPSIS
#	CheckURL(*String);
#
# - ARGS
#	*String		URLʸ����
#
# - DESCRIPTION
#	URL��ʸ��������å���Ԥʤ����������������å�������
#	��ȤΥ����å��ˤ�IsUrl��ƤӽФ���
#	������ʸ������ä��饨�顼ɽ���롼����ء�
#	(���ץꥱ�������/GUI��ʬΥ�����ۤ�����������?)
#
# - RETURN
#	�ʤ�
#
sub CheckURL {
    local(*String) = @_;

    # http://�����ξ��϶��ˤ��Ƥ��ޤ���
    if ($String =~ m!^http://$!oi) { $String = ''; }

    # URL����ȤΥ����å�
    if (($String ne '') && (! &IsUrl($String))) { &Fatal(7, 'URL'); }

}


###
## IsUrl - URL�ι�¤������å�
#
# - SYNOPSIS
#	IsUrl($String);
#
# - ARGS
#	$String		URLʸ����
#
# - DESCRIPTION
#	URL��ʸ��������å���Ԥʤ���
#	ͽ����ꤵ�줿(@URL_SCHEME)Scheme�Τ�ΤǤ��뤫�ݤ�������å���
#	telnet��³���ϡ����ʤ���
#
# - RETURN
#	������URL�Ǥ����1�������Ǥʤ����0
#
sub IsUrl {
    local($String) = @_;
    local($Scheme, $IsUrl);

    $IsUrl = 0;
    foreach $Scheme (@URL_SCHEME) {
	if ($String =~ m!^$Scheme://!i) { $IsUrl = 1; }
    }

    return($IsUrl);

}


###
## GetFollowIdTree - ��ץ饤�������ڹ�¤�����
#
# - SYNOPSIS
#	GetFollowIdTree($Id);
#
# - ARGS
#	$Id	����ID
#
# - DESCRIPTION
#	���ꤵ�줿�����Υ�ץ饤�����򡤤���ID���ڹ�¤�ե����ޥåȤǼ��Ф���
#
#	��: * (�����ꤵ�줿����)
#	    +--a
#	    |  +--b
#	    |  |  +--c
#	    |  |  +--d
#	    |  |
#	    |  +--e
#	    |     +--f
#	    +--g
#	       +--h
#
#	�� ( a ( b ( c d ) e ( f ) ) g ( h ) )
#
# - RETURN
#	�ڹ�¤��ɽ���ꥹ��
#
sub GetFollowIdTree {
    local($Id) = @_;

    # �Ƶ�Ū���ڹ�¤����Ф���
    return('(', &GetFollowIdTreeMain($Id), ')');

}

sub GetFollowIdTreeMain {
    local($Id) = @_;
    local(@AidList, @Result, @ChildResult);

    # �Ƶ���߾��
    if ($Id eq '') { return(); }

    # �ե����������Ф�
    @AidList = split(/,/, $DB_AIDS{$Id});

    # �ʤ�������
    return($Id) unless @AidList;

    # �Ƶ�
    @Result = ($Id, '(');
    @ChildResult = ();
    foreach (@AidList) {
	@ChildResult = &GetFollowIdTreeMain($_);
	if (@ChildResult) {
	    push(@Result, @ChildResult);
	}
    }
    return(@Result, ')');

}


###
## GetReplySubject - ��ץ饤Subject������
#
# - SYNOPSIS
#	GetReplySubject($Id);
#
# - ARGS
#	$Id	����ID
#
# - DESCRIPTION
#	����Id�ε�������Subject���äƤ��ơ���Ƭ�ˡ�Re:�פ�1�Ĥ����Ĥ����֤���
#
# - RETURN
#	��������Subjectʸ����
#
sub GetReplySubject {
    local($Id) = @_;
    local($dFid, $dAids, $dDate, $dSubject) = &GetArticlesInfo($Id);

    # ��Ƭ�ˡ�Re:�פ����äĤ��Ƥ����������
    $dSubject =~ s/^Re:\s*//oi;
    # ��Ƭ�ˡ�Re: �פ򤯤äĤ����֤���
    return("Re: $dSubject");

}


###
## GetFormattedTitle - �����ȥ�ꥹ�ȤΥե����ޥå�
#
# - SYNOPSIS
#	GetFormattedTitle($Id, $Board, $Aids, $Icon, $Title, $Name, $Date);
#
# - ARGS
#	$Id		����ID
#	$Board		�Ǽ���ID
#	$Aids		��ץ饤���������뤫�ݤ�
#	$Icon		������������ID
#	$Title		������Subject
#	$Name		��������Ƽ�̾
#	$Date		�������������(UTC)
#
# - DESCRIPTION
#	���뵭���򥿥��ȥ�ꥹ��ɽ���Ѥ˥ե����ޥåȤ��롥
#
# - RETURN
#	�ե����ޥåȤ���ʸ����
#
sub GetFormattedTitle {
    local($Id, $Board, $Aids, $Icon, $Title, $Name, $Date) = @_;
    local($String, $InputDate, $IdStr, $Link, $Thread);

    $InputDate = &GetDateTimeFormatFromUtc(($Date || &GetModifiedTime($Id, $Board)));
    # �����ȥ뤬�Ĥ��Ƥʤ��ä��顤Id�򤽤Τޤޥ����ȥ�ˤ��롥
    $Title = $Title || $Id;

    # �̾ﵭ��
    $IdStr = "<strong>$Id.</strong> ";

    if ($SYS_F_E) {
	$Link = "<a href=\"$PROGRAM?b=$Board&c=e&id=$Id\">$Title</a>";
    } else {
	$Link = "$Title";
    }

    $Thread = (($SYS_F_T && $Aids) ? " <a href=\"$PROGRAM?b=$Board&c=t&id=$Id\">$H_THREAD</a>" : '');

    if (($Icon eq $H_NOICON) || ($Icon eq '')) {
	$String = sprintf("$IdStr$Link$Thread [%s] $InputDate", ($Name || $MAINT_NAME));
    } else {
	$String = sprintf("$IdStr<img src=\"%s\" alt=\"$Icon \" width=\"$MSGICON_WIDTH\" height=\"$MSGICON_HEIGHT\">$Link$Thread [%s] $InputDate", &GetIconURLFromTitle($Icon, $Board), ($Name || $MAINT_NAME));
    }

    return($String);

}


###
## GetModifiedTime - ���뵭���κǽ���������(UTC)�����
#
# - SYNOPSIS
#	GetModifiedTime($Id, $Board);
#
# - ARGS
#	$Id		����ID
#	$Board		�Ǽ���ID
#
# - DESCRIPTION
#	����ID�ε������顤�ǽ�����UTC���äƤ��롥
#
# - RETURN
#	���ε����ե�����κǽ���������(UTC)
#
sub GetModifiedTime {
    local($Id, $Board) = @_;

    return($TIME - (-M &GetArticleFileName($Id, $Board)) * 86400);
    # 86400 = 24 * 60 * 60
}


###
## GetDateTimeFormatFromUtc - UTC������֤�ɽ��ʸ��������
#
# - SYNOPSIS
#	GetDateTimeFormatFromUtc($Utc);
#
# - ARGS
#	$Utc		����(UTC)
#
# - DESCRIPTION
#	UTC���ʬ�ä�ʬ�䤷���ե����ޥåȤ���ʸ����Ȥ����֤���
#	�Ť��С�������KINOBOARDS�Ǥϡ�
#	DB��˻����ɽ��ʸ����(not UTC)�����Τޤ����äƤ��뤬��
#	���줬�Ϥ��줿���(UTC�Ǥʤ��ä����)�ϡ����Τޤ��֤���
#
# - RETURN
#	�����ɽ�魯ʸ����
#
sub GetDateTimeFormatFromUtc {
    local($Utc) = @_;
    local($Sec, $Min, $Hour, $Mday, $Mon, $Year, $Wday, $Yday, $Isdst);

    # �Ť�����Τ�Τ餷����
    if ($Utc !~ m/^\d+$/) { return($Utc); }

    # �Ѵ�
    ($Sec, $Min, $Hour, $Mday, $Mon, $Year, $Wday, $Yday, $Isdst) = localtime($Utc);
    return(sprintf("%d/%d(%02d:%02d)", $Mon + 1, $Mday, $Hour, $Min));

}


###
## GetUtcFromOldDateTimeFormat - �����UTC�ؤ�������
#
# - SYNOPSIS
#	GetUtcFromOldDateTimeFormat($Time);
#
# - ARGS
#	$Time		���֤�ɽ�魯ʸ����
#
# - DESCRIPTION
#	�Ť��С�������KINOBOARDS�Ǥϡ�
#	DB��˻����ɽ��ʸ���󤬤��Τޤ�(UTC�Ǥʤ�)���äƤ��롥
#	���줬�Ϥ��줿����Ŭ����UTC(854477921 = 97/01/29 03:58)���֤���
#	UTC���Ϥ��줿�餽�Τޤޤ���UTC���֤���
#
# - RETURN
#	����(UTC)
#
sub GetUtcFromOldDateTimeFormat {
    local($Time) = @_;

    # �����餷��
    if ($Time =~ m/^\d+$/) { return($Time); }

    # Ŭ��
    return(854477921);

}


###
## DQEncode/DQDecode - �ü�ʸ����Encode��Decode
#
# - SYNOPSIS
#	DQEncode($Str);
#	DQDecode($Str);
#
# - ARGS
#	$Str	Encode/Decode����ʸ����
#
# - DESCRIPTION
#	HTML���ü�ʸ��(", >, <, &)��Encode/Decode���롥
#
# - RETURN
#	Encode/Decode����ʸ����
#
sub DQEncode {
    local($Str) = @_;

    $Str =~ s/\"/__dq__/go;
    $Str =~ s/\>/__gt__/go;
    $Str =~ s/\</__lt__/go;
    $Str =~ s/\&/__amp__/go;
    return($Str);
}

sub DQDecode {
    local($Str) = @_;

    $Str =~ s/__dq__/\"/go;
    $Str =~ s/__gt__/\>/go;
    $Str =~ s/__lt__/\</go;
    $Str =~ s/__amp__/\&/go;
    return($Str);
}


###
## HTMLEncode/HTMLDecode - �ü�ʸ����HTML��Encode��Decode
#
# - SYNOPSIS
#	HTMLEncode($Str);
#	HTMLDecode($Str);
#
# - ARGS
#	$Str	HTML��Encode/Decode����ʸ����
#
# - DESCRIPTION
#	HTML���ü�ʸ��(", >, <, &)��HTML�Ѥ�Encode/Decode���롥
#
# - RETURN
#	Encode/Decode����ʸ����
#
sub HTMLEncode {
    local($_) = @_;

    s/\&/&amp;/go;
    s/\"/&quot;/go;
    s/\>/&gt;/go;
    s/\</&lt;/go;
    return($_);
}

sub HTMLDecode {
    local($_) = @_;

    s/&quot;/\"/gio;
    s/&gt;/\>/gio;
    s/&lt;/\</gio;
    s/&amp;/\&/gio;
    return($_);
}


###
## ArticleEncode - ������Encode
#
# - SYNOPSIS
#	ArticleEncode($Article);
#
# - ARGS
#	$Article	Encode���뵭����ʸ
#
# - DESCRIPTION
#	�������URL(<URL:��>)�򡤥�󥯤��Ѵ����롥
#
# - RETURN
#	Encode���줿ʸ����
#
sub ArticleEncode {
    local($Article) = @_;
    local($Return, $Url, $UrlMatch, $Str, @Cash);

    $Return = $Article;
    while ($Article =~ m/<URL:([^>]*)>/g) {
	$Url = $1;
	($UrlMatch = $Url) =~ s/\?/\\?/go;
	next if (grep(/^$UrlMatch$/, @Cash));
	push(@Cash, $Url);
	if (&IsUrl($UrlMatch)) {
	    $Str = "<a href=\"$Url\"><URL:$Url></a>";
	}
	$Return =~ s/<URL:$UrlMatch>/$Str/g;
    }

    &cgi'SecureHtml(*Return);

    return($Return);

}


###
## DeleteArticle - �����κ��
#
# - SYNOPSIS
#	DeleteArticle($Id, $ThreadFlag);
#
# - ARGS
#	$Id		�������ID
#	$ThreadFlag	��ץ饤��ä����ݤ�
#
# - DESCRIPTION
#	������٤�����ID����������塤DB�򹹿����롥
#
# - RETURN
#	�ʤ�
#
sub DeleteArticle {
    local($Id, $ThreadFlag) = @_;
    local($Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $dId, @Target, $TargetId);

    # ��������μ���
    ($Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url) = &GetArticlesInfo($Id);

    # �ǡ����ν񤭴���(ɬ�פʤ�̼��)
    @Target = ($Id);
    foreach $TargetId (@Target) {
	foreach ($[ .. $#DB_ID) {
	    # ID����Ф�
	    $dId = $DB_ID[$_];
	    # �ե��������ꥹ�Ȥ��椫�顤������뵭����ID�������
	    $DB_AIDS{$dId} = join(',', grep((! /^$TargetId$/o), split(/,/, $DB_AIDS{$dId})));
	    # ������������������ID�������
	    $DB_FID{$dId} = '' if ($DB_FID{$dId} eq $TargetId);
	    $DB_FID{$dId} =~ s/,$TargetId,.*$//;
	    $DB_FID{$dId} =~ s/^$TargetId,.*$//;
	    $DB_FID{$dId} =~ s/,$TargetId$//;
	    # ̼���оݤȤ���
	    if ($ThreadFlag && ($dId eq $TargetId)) {
		push(Target, split(/,/, $DB_AIDS{$dId}));
	    }
	}
    }

    # DB�򹹿����롥
    &deleteArticleFromDbFile($Board, *Target);
}


###
## SupersedeArticle - ��������������
#
# - SYNOPSIS
#	SupersedeArticle;
#
# - ARGS
#	�ʤ�
#
# - DESCRIPTION
#	�������������롥
#
# - RETURN
#	�ʤ�
#
sub SupersedeArticle {
    local($Board, $Id, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail) = @_;
    local($SupersedeId, $File, $SupersedeFile);

    # ���Ϥ��줿��������Υ����å�
    $Article = &CheckArticle($Board, $TextType, *Name, *Email, *Url, *Subject, *Icon, $Article);

    # DB�ե����������
    $SupersedeId = &SupersedeDBFile($Board, $Id, $TIME, $Subject, $Icon, $REMOTE_HOST, $Name, $Email, $Url, $Fmail);

    # ex. ��100�ע���100_5��
    $File = &GetArticleFileName($Id, $Board);
    $SupersedeFile = &GetArticleFileName(sprintf("%s_%s", $Id, $SupersedeId), $Board);
    rename($File, $SupersedeFile);

    # �����Υե�����κ���
    &MakeArticleFile($TextType, $Article, $Id, $Board);
}


###
## ReLinkExec - �����Τ��������»�
#
# - SYNOPSIS
#	ReLinkExec($FromId, $ToId, $Board);
#
# - ARGS
#	$FromId		��������������ID
#	$ToId		���������赭��ID
#	$Board		�Ǽ���ID
#
# - DESCRIPTION
#	�������ץ饤-�������ط��򤫤������롥
#
# - RETURN
#	�ʤ�
#
sub ReLinkExec {
    local($FromId, $ToId, $Board) = @_;
    local($dId, @Daughters, $DaughterId);

    # �۴ĵ����ζػ�
    &FatalPriv(50, '') if (grep(/^$FromId$/, split(/,/, $DB_FID{$ToId})));

    # �ǡ����񤭴���
    foreach ($[ .. $#DB_ID) {
	# ID����Ф�
	$dId = $DB_ID[$_];
	# �ե��������ꥹ�Ȥ��椫�顤��ư���뵭����ID�������
	$DB_AIDS{$dId} = join(',', grep((! /^$FromId$/o), split(/,/, $DB_AIDS{$dId})));
    }

    # ɬ�פʤ�̼��Ȥ�����Ƥ���
    @Daughters = split(/,/, $DB_AIDS{$FromId}) if ($DB_FID{$FromId});

    # ���������Υ�ץ饤����ѹ�����
    if ($ToId eq '') {
	$DB_FID{$FromId} = '';
    } elsif ($DB_FID{$ToId} eq '') {
	$DB_FID{$FromId} = "$ToId";
    } else {
	$DB_FID{$FromId} = "$ToId,$DB_FID{$ToId}";
    }

    # ����������̼�ˤĤ��Ƥ⡤��ץ饤����ѹ�����
    while($DaughterId = shift(@Daughters)) {
	# ¹̼��ġ�
	push(Daughters, split(/,/, $DB_AIDS{$DaughterId}));
	# �񤭴���
	if (($DB_FID{$DaughterId} eq $FromId) || ($DB_FID{$DaughterId} =~ /^$FromId,/)) {
	    $DB_FID{$DaughterId} = $DB_FID{$FromId} ? "$FromId,$DB_FID{$FromId}" : "$FromId";
	} elsif (($DB_FID{$DaughterId} =~ /^(.*),$FromId$/) || ($DB_FID{$DaughterId} =~ /^(.*),$FromId,/)) {
	    $DB_FID{$DaughterId} = $DB_FID{$FromId} ? "$1,$FromId,$DB_FID{$FromId}" : "$1,$FromId";
	}
    }

    # ��ץ饤��ˤʤä������Υե������������ɲä���
    $DB_AIDS{$ToId} = ($DB_AIDS{$ToId} ne '') ? "$DB_AIDS{$ToId},$FromId" : "$FromId";

    # ����DB�򹹿�����
    &updateArticleDb($Board);
}


###
## ReOrderExec - �����ΰ�ư�»�
#
# - SYNOPSIS
#	ReOrderExec($FromId, $ToId, $Board);
#
# - ARGS
#	$FromId		��ư������ID
#	$ToId		��ư�赭��ID
#	$Board		�Ǽ���ID
#
# - DESCRIPTION
#	���ꤵ�줿�����򡤻��ꤵ�줿�����μ��˰�ư���롥
#
# - RETURN
#	�ʤ�
#
sub ReOrderExec {
    local($FromId, $ToId, $Board) = @_;
    local(@Move);

    # ��ư���뵭�������򽸤��
    @Move = ($FromId, &CollectDaughters($FromId));

    # ��ư������
    &reOrderArticleDb($Board, $ToId, *Move);

    # DB�񤭴������Τǡ�����å��夷ľ��
    &DbCash($Board);
}


###
## CollectDaughters - ̼�Ρ��ɤΥꥹ�Ȥ򽸤��
#
# - SYNOPSIS
#	CollectDaughters($Id);
#
# - ARGS
#	$Id		����ID
#
# - DESCRIPTION
#	̼�Ρ��ɤΥꥹ�Ȥ򽸤��
#
# - RETURN
#	̼�Ρ��ɽ���Υꥹ��
#
sub CollectDaughters {
    local($Id) = @_;
    local(@Return);

    foreach (split(/,/, $DB_AIDS{$Id})) {
	push(Return, $_);
	push(Return, &CollectDaughters($_)) if ($DB_AIDS{$_} ne '');
    }
    @Return;
}


###
## GetNewArticleId - ���嵭��ID�η���
#
# - SYNOPSIS
#	GetNewArticleId($Board);
#
# - ARGS
#	$Board		�Ǽ���ID
#
# - DESCRIPTION
#	����κǿ�����ID��1���䤷���������������ֹ���֤���
#
# - RETURN
#	���嵭����ID
#
sub GetNewArticleId {
    local($Board) = @_;

    &getArticleId($Board) + 1;
}


######################################################################
# �ǡ�������ץ���ơ������


###
## DbCash - ����DB�����ɤ߹���
#
# - SYNOPSIS
#	DbCash($Board);
#
# - ARGS
#	$Board		�Ǽ���ID
#
# - DESCRIPTION
#	��˵�ư���˸ƤӽФ��졤����DB�����Ƥ�����ѿ��˥���å��夹�롥
#
# - RETURN
#	�ʤ�
#
$BOARD_DB_CASH = 0;

sub DbCash {
    return if $BOARD_DB_CASH;

    local($Board) = @_;
    local($DBFile, $dId, $dFid, $dAids, $dDate, $dTitle, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail, $Count);

    # ���ꥢ
    @DB_ID = %DB_FID = %DB_AIDS = %DB_DATE = %DB_TITLE = %DB_ICON = %DB_REMOTEHOST = %DB_NAME = %DB_EMAIL = %DB_URL = %DB_FMAIL = ();

    $DBFile = &GetPath($Board, $DB_FILE_NAME);

    # �����ߡ�
    open(DB, "<$DBFile") || &Fatal(1, $DBFile);
    while(<DB>) {

	# Version Check
	&VersionCheck('DB', $1), next if (m/^\# Kb-System-Id: ([^\/]*\/.*)$/o);
	next if (/^\#/o || /^$/o);
	chop;

	($dId, $dFid, $dAids, $dDate, $dTitle, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail) = split(/\t/, $_, 11);
	next if ($dId eq '');

	$DB_ID[$Count++] = $dId;
	$DB_FID{$dId} = $dFid;
	$DB_AIDS{$dId} = $dAids;
	$DB_DATE{$dId} = $dDate || &GetModifiedTime($dId, $Board);
	$DB_TITLE{$dId} = $dTitle || $dId;
	$DB_ICON{$dId} = $dIcon;
	$DB_REMOTEHOST{$dId} = $dRemoteHost;
	$DB_NAME{$dId} = $dName || $MAINT_NAME;
	$DB_EMAIL{$dId} = $dEmail;
	$DB_URL{$dId} = $dUrl;
	$DB_FMAIL{$dId} = $dFmail;

    }
    close(DB);

    $BOARD_DB_CASH = 1;		# cashed

}


###
## GetArticlesInfo - ����DB���ɤ߹���
#
# - SYNOPSIS
#	GetArticlesInfo($Id);
#
# - ARGS
#	$Id	����ID
#
# - DESCRIPTION
#	����DB���ɤ߹���ǡ��������Ф���
#	�ºݤϥ���å��夫���ɤ߽Ф�������
#
# - RETURN
#	��������Υꥹ��
#		��ץ饤������ID
#		���ε����˥�ץ饤����������ID�Υꥹ��(��,�׶��ڤ�)
#		��ƻ���(UTC)
#		Subject
#		��������ID
#		��ƥۥ���
#		��Ƽ�̾
#		��Ƽ�E-Mail
#		��Ƽ�URL
#		��ץ饤�����ä�������ƼԤ˥ᥤ������뤫�ݤ�
#
sub GetArticlesInfo {
    local($Id) = @_;

    return($DB_FID{$Id}, $DB_AIDS{$Id}, $DB_DATE{$Id}, $DB_TITLE{$Id}, $DB_ICON{$Id}, $DB_REMOTEHOST{$Id}, $DB_NAME{$Id}, $DB_EMAIL{$Id}, $DB_URL{$Id}, $DB_FMAIL{$Id});

}


###
## AddDBFile - ����DB�ؤ��ɲ�
#
# - SYNOPSIS
#	AddDBFile($Id, $Board, $Fid, $InputDate, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail);
#
# - ARGS
#	$Id		����ID
#	$Board		�Ǽ���ID
#	$Fid		��ץ饤���ε���ID
#	$InputDate	�񤭹�������(UTC)
#	$Subject	Subject
#	$Icon		��������ID
#	$RemoteHost	�񤭹��ߥۥ���(IP addr.��FQDN����http�����м���)
#	$Name		��Ƽ�̾
#	$Email		��Ƽ�E-Mail addr.
#	$Url		��Ƽ�URL
#	$Fmail		��ץ饤���˥ᥤ������뤫�ݤ�(''/'on')
#
# - DESCRIPTION
#	����DB�˵������ɲä��롥
#
# - RETURN
#	�ʤ�
#
sub AddDBFile {
    local($Id, $Board, $Fid, $InputDate, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail) = @_;
    local($dId, $dFid, $dAids, $dInputDate, $dSubject, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail, $mdName, $mdInputDate, $mdSubject, $mdId, $mName, $mSubject, $mId, $FidList, $FFid, $File, $TmpFile, @FollowMailTo, @FFid, @ArriveMail);

    # ��ץ饤���Υ�ץ饤�������äƤ���
    if ($Fid ne '') {
	($FFid) = &GetArticlesInfo($Fid);
	@FFid = split(/,/, $FFid);
    }

    $FidList = $Fid;

    $File = &GetPath($Board, $DB_FILE_NAME);
    $TmpFile = &GetPath($Board, "$DB_FILE_NAME.$TMPFILE_SUFFIX");
    open(DBTMP, ">$TmpFile") || &Fatal(1, $TmpFile);
    open(DB, "<$File") || &Fatal(1, $File);
    while(<DB>) {

	# Version Check
	&VersionCheck('DB', $1) if (m/^\# Kb-System-Id: ([^\/]*\/.*)$/o);
	print(DBTMP "$_"), next if (/^\#/o || /^$/o);
	chop;

	($dId, $dFid, $dAids, $dInputDate, $dSubject, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail) = split(/\t/, $_);
	
	# �ե����赭�������Ĥ��ä��顤
	if (($dId ne '') && ($dId eq $Fid)) {

	    # ���ε����Υե�������ID�ꥹ�Ȥ˲ä���(����޶��ڤ�)
	    if ($dAids ne '') {$dAids .= ",$Id";} else {$dAids = $Id;}

	    # �������Υե�����ꥹ�Ȥ��äƤ��Ƹ�������ä���
	    # �������Υե�����ꥹ�Ȥ���
	    if ($dFid ne '') {
		$FidList = "$dId,$dFid";
	    }

	    if ($SYS_MAIL) {
		# �ᥤ�������Τ���˥���å���
		$mdName = $dName;
		$mdInputDate = $dInputDate;
		$mdSubject = $dSubject;
		$mdId = $dId;
		$mName = $Name;
		$mSubject = $Subject;
		$mId = $Id;
		if ($dFmail ne '') {
		    push(@FollowMailTo, $dEmail);
		}
	    }
	}

	# DB�˽񤭲ä���
	printf(DBTMP "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n", $dId, $dFid, $dAids, $dInputDate, $dSubject, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail);

	# ��ץ饤���Υ�ץ饤�������ĥᥤ��������ɬ�פ�����С��������¸
	if ($SYS_MAIL && (@FFid) && $dFmail && $dEmail && (grep(/^$dId$/, @FFid)) && (! grep(/^$dEmail$/, @FollowMailTo))) {
	    push(@FollowMailTo, $dEmail);
	}
    }

    # �����������Υǡ�����񤭲ä��롥
    printf(DBTMP "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n", $Id, $FidList, '', $InputDate, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail);

    # close Files.
    close(DB);
    close(DBTMP);

    # DB�򹹿�����
    rename($TmpFile, $File);

    # ɬ�פʤ���Ƥ����ä����Ȥ�ᥤ�뤹��
    &getArriveMailTo(0, $Board, *ArriveMail);
    if (@ArriveMail) {
	&ArriveMail($Name, $Subject, $Id, @ArriveMail);
    }

    # ɬ�פʤ�ȿ�������ä����Ȥ�ᥤ�뤹��
    if (@FollowMailTo) {
	&FollowMail($mdName, $mdInputDate, $mdSubject, $mdId, $mName, $mSubject, $mId, @FollowMailTo);
    }

}


###
## updateArticleDb - ����DB��������
#
# - SYNOPSIS
#	updateArticleDb($Board);
#
# - ARGS
#	$Board		�Ǽ���ID
#
# - DESCRIPTION
#	����DB�򡤿����ʵ����ǡ��������������롥
#	�񤭹��൭���ǡ����ϥ���å��夵��Ƥ����Ρ�
#
# - RETURN
#	�ʤ�
#
sub updateArticleDb {
    local($Board) = @_;
    local($File, $TmpFile, $dId);

    $File = &GetPath($Board, $DB_FILE_NAME);
    $TmpFile = &GetPath($Board, "$DB_FILE_NAME.$TMPFILE_SUFFIX");
    open(DBTMP, ">$TmpFile") || &Fatal(1, $TmpFile);
    open(DB, "<$File") || &Fatal(1, $File);

    while(<DB>) {

	# Version Check
	&VersionCheck('DB', $1) if (m/^\# Kb-System-Id: ([^\/]*\/.*)$/o);

	print(DBTMP "$_"), next if (/^\#/o || /^$/o);

	# Id����Ф�
	chop; ($dId = $_) =~ s/\t.*$//;

	# DB�˽񤭲ä���
	printf(DBTMP "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n", $dId, $DB_FID{$dId}, $DB_AIDS{$dId}, $DB_DATE{$dId}, $DB_TITLE{$dId}, $DB_ICON{$dId}, $DB_REMOTEHOST{$dId}, $DB_NAME{$dId}, $DB_EMAIL{$dId}, $DB_URL{$dId}, $DB_FMAIL{$dId});
    }

    # close Files.
    close(DB);
    close(DBTMP);

    # DB�򹹿�����
    rename($TmpFile, $File);
}


###
## deleteArticleFromDbFile - ����DB�ι���
#
# - SYNOPSIS
#	deleteArticleFromDbFile($Board, *Target);
#
# - ARGS
#	$Board		�Ǽ���ID
#	*Target		������뵭��ID�Υꥹ��
#
# - DESCRIPTION
#	����DB������ꤵ�줿�������Υ���ȥ�������롥
#
# - RETURN
#	�ʤ�
#
sub deleteArticleFromDbFile {
    local($Board, *Target) = @_;
    local($File, $TmpFile, $dId);

    $File = &GetPath($Board, $DB_FILE_NAME);
    $TmpFile = &GetlPath($Board, "$DB_FILE_NAME.$TMPFILE_SUFFIX");
    open(DBTMP, ">$TmpFile") || &Fatal(1, $TmpFile);
    open(DB, "<$File") || &Fatal(1, $File);

    while(<DB>) {

	# Version Check
	&VersionCheck('DB', $1) if (m/^\# Kb-System-Id: ([^\/]*\/.*)$/o);

	print(DBTMP "$_"), next if (/^\#/o || /^$/o);

	# Id����Ф�
	chop; ($dId = $_) =~ s/\t.*$//;

	# ���������ϥ����ȥ�����
	print(DBTMP "#") if (grep(/^$dId$/, @Target));
	printf(DBTMP "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n", $dId, $DB_FID{$dId}, $DB_AIDS{$dId}, $DB_DATE{$dId}, $DB_TITLE{$dId}, $DB_ICON{$dId}, $DB_REMOTEHOST{$dId}, $DB_NAME{$dId}, $DB_EMAIL{$dId}, $DB_URL{$dId}, $DB_FMAIL{$dId});

    }

    # close Files.
    close(DB);
    close(DBTMP);

    # DB�򹹿�����
    rename($TmpFile, $File);
}


###
## reOrderArticleDb - ����DB�ν���ѹ�
#
# - SYNOPSIS
#	reOrderArticleDb($Board, $Id, *Move);
#
# - ARGS
#	$Board		�Ǽ���ID
#	$Id		��ư�赭��ID
#	*Move		��ư���뵭�����Υꥹ�ȤؤΥ�ե����
#
# - DESCRIPTION
#	���ꤵ�줿�������򡤻��ꤵ�줿�����β��˰�ư���롥
#	�ֲ��פ�DB����褫�夫�ϡ����夬�夫�������˰ͤ�ۤʤ롥
#
# - RETURN
#	�ʤ�
#
sub reOrderArticleDb {
    local($Board, $Id, *Move) = @_;
    local($File, $TmpFile, $dId, $TopFlag);

    # ��Ƭ�ե饰
    $TopFlag = 1;

    $File = &GetPath($Board, $DB_FILE_NAME);
    $TmpFile = &GetPath($Board, "$DB_FILE_NAME.$TMPFILE_SUFFIX");
    open(DBTMP, ">$TmpFile") || &Fatal(1, $TmpFile);
    open(DB, "<$File") || &Fatal(1, $File);

    while(<DB>) {

	# Version Check
	&VersionCheck('DB', $1) if (m/^\# Kb-System-Id: ([^\/]*\/.*)$/o);

	print(DBTMP "$_"), next if (/^\#/o);
	print(DBTMP "$_"), next if (/^$/o);

	# Id����Ф�
	chop; ($dId = $_) =~ s/\t.*$//;

	# ��ư�����ۤϼ�����
	next if (grep(/^$dId$/, @Move));

	# ��Ƭ�ˤ�����ν���(���夬�����ξ��)
	if (($Id eq '') && ($SYS_BOTTOMTITLE == 1) && ($TopFlag == 1)) {
	    $TopFlag = 0;
	    foreach (@Move) {
		printf(DBTMP "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n", $_, $DB_FID{$_}, $DB_AIDS{$_}, $DB_DATE{$_}, $DB_TITLE{$_}, $DB_ICON{$_}, $DB_REMOTEHOST{$_}, $DB_NAME{$_}, $DB_EMAIL{$_}, $DB_URL{$_}, $DB_FMAIL{$_});
	    }
	}

	# ��ư�褬�����顤��˽񤭹���(���夬�塤�ξ��)
	if (($SYS_BOTTOMTITLE == 0) && ($dId eq $Id)) {
	    foreach (@Move) {
		printf(DBTMP "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n", $_, $DB_FID{$_}, $DB_AIDS{$_}, $DB_DATE{$_}, $DB_TITLE{$_}, $DB_ICON{$_}, $DB_REMOTEHOST{$_}, $DB_NAME{$_}, $DB_EMAIL{$_}, $DB_URL{$_}, $DB_FMAIL{$_});
	    }
	}

	# DB�˽񤭲ä���
	printf(DBTMP "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n", $dId, $DB_FID{$dId}, $DB_AIDS{$dId}, $DB_DATE{$dId}, $DB_TITLE{$dId}, $DB_ICON{$dId}, $DB_REMOTEHOST{$dId}, $DB_NAME{$dId}, $DB_EMAIL{$dId}, $DB_URL{$dId}, $DB_FMAIL{$dId});

	# ��ư�褬�����顤³���ƽ񤭹���(���夬�����ξ��)
	if (($SYS_BOTTOMTITLE == 1) && ($dId eq $Id)) {
	    foreach (@Move) {
		printf(DBTMP "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n", $_, $DB_FID{$_}, $DB_AIDS{$_}, $DB_DATE{$_}, $DB_TITLE{$_}, $DB_ICON{$_}, $DB_REMOTEHOST{$_}, $DB_NAME{$_}, $DB_EMAIL{$_}, $DB_URL{$_}, $DB_FMAIL{$_});
	    }
	}

    }

    # ��Ƭ�ˤ�����ν���(���夬�塤�ξ��)
    if (($Id eq '') && ($SYS_BOTTOMTITLE == 0)) {
	foreach (@Move) {
	    printf(DBTMP "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n", $_, $DB_FID{$_}, $DB_AIDS{$_}, $DB_DATE{$_}, $DB_TITLE{$_}, $DB_ICON{$_}, $DB_REMOTEHOST{$_}, $DB_NAME{$_}, $DB_EMAIL{$_}, $DB_URL{$_}, $DB_FMAIL{$_});
	}
    }

    # close Files.
    close(DB);
    close(DBTMP);

    # DB�򹹿�����
    rename($TmpFile, $File);
}


###
## MakeArticleFile - ������ʸDB�ؤ��ɲ�
#
# - SYNOPSIS
#	MakeArticleFile($TextType, $Article, $Id, $Board);
#
# - ARGS
#	$TextType	ʸ�񥿥���
#	$Article	��ʸ
#	$Id		����ID
#	$Board		�Ǽ���ID
#
# - DESCRIPTION
#	������ʸDB(�Ǽ���ID��Ʊ��̾���Υǥ��쥯�ȥ�)����ˡ�
#	ID��Ʊ��̾���Υե�����Ȥ��ơ�������ʸ����¸���롥
#
# - RETURN
#	�ʤ�
#
sub MakeArticleFile {
    local($TextType, $Article, $Id, $Board) = @_;
    local($File) = &GetArticleFileName($Id, $Board);

    # �ե�����򳫤�
    open(TMP, ">$File") || &Fatal(1, $File);

    # �С����������񤭽Ф�
    printf(TMP "<!-- Kb-System-Id: %s/%s -->\n", $KB_VERSION, $KB_RELEASE);

    # TextType��������
    if ((! $SYS_TEXTTYPE) || ($TextType eq $H_PRE)) {
	print(TMP "<p><pre>");
    }

    # ����; "��ǥ����ɤ����������ƥ������å�
    $Article = &DQDecode($Article);
    $Article = &ArticleEncode($Article);
    print(TMP "$Article\n");

    # TextType�Ѹ����
    if ((! $SYS_TEXTTYPE) || ($TextType eq $H_PRE)) {
	print(TMP "</pre></p>\n");
    }

    # ��λ
    close(TMP);

}


###
## getArticleBody - ������ʸDB���ɤ߹���
#
# - SYNOPSIS
#	getArticleBody($Id, $Board, *ArticleBody);
#
# - ARGS
#	$Id		����ID
#	$BoardId	�Ǽ���ID
#	*ArticleBody	��ʸ�ƹԤ�����������ѿ��ؤΥ�ե����
#
# - DESCRIPTION
#	������ʸDB(�Ǽ���ID��Ʊ��̾���Υǥ��쥯�ȥ�)����Ρ�
#	ID��Ʊ��̾���Υե�������ɤ߽Ф���
#
# - RETURN
#	�ʤ�
#
sub getArticleBody {
    local($Id, $Board, *ArticleBody) = @_;
    local($QuoteFile);

    $QuoteFile = &GetArticleFileName($Id, $Board);
    open(TMP, "<$QuoteFile") || &Fatal(1, $QuoteFile);
    while(<TMP>) {
	&VersionCheck('Article', $1), next if (m/^<!-- Kb-System-Id: ([^\/]*\/.*) -->$/o);
	push(@ArticleBody, $_);
    }
    close(TMP);
    
}


###
## getArticleId - �����ֹ�DB���ɤ߹���
#
# - SYNOPSIS
#	getArticleId($Board);
#
# - ARGS
#	$Board		�Ǽ���ID
#
# - DESCRIPTION
#	����κǿ�����ID���ɤ߽Ф���
#
# - RETURN
#	�ǿ�������ID
#
sub getArticleId {
    local($Board) = @_;
    local($ArticleNumFile, $ArticleId);

    $ArticleNumFile = &GetPath($Board, $ARTICLE_NUM_FILE_NAME);
    open(AID, "<$ArticleNumFile") || &Fatal(1, $ArticleNumFile);
    chop($ArticleId = <AID>);
    close(AID);
    $ArticleId;
}


###
## WriteArticleId - �����ֹ�DB�ι���
#
# - SYNOPSIS
#	WriteArticleId($Id, $Board);
#
# - ARGS
#	$Id		�����˽񤭹��൭���ֹ�
#	$Board		�Ǽ���ID
#
# - DESCRIPTION
#	�����ֹ�DB�ι���
#
# - RETURN
#	�ʤ�
#
sub WriteArticleId {
    local($Id, $Board) = @_;
    local($File, $TmpFile, $OldArticleId);
    
    # �����Τ����˸Ť����ͤ��㤤! (��������ʤ���OK)
    $OldArticleId = &GetNewArticleId($Board);
    if (($Id =~ /^\d+$/) && ($Id < $OldArticleId)) {
	&Fatal(10, '');
    }

    $File = &GetPath($Board, $ARTICLE_NUM_FILE_NAME);
    $TmpFile = &GetPath($Board, "$ARTICLE_NUM_FILE_NAME.$TMPFILE_SUFFIX");
    open(AID, ">$TmpFile") || &Fatal(1, $TmpFile);
    print(AID "$Id\n");
    close(AID);

    # ����
    rename($TmpFile, $File);

}


###
## getArriveMailTo - �Ǽ����̿����ᥤ��������DB�����ɤ߹���
#
# - SYNOPSIS
#	getArriveMailTo($CommentFlag, $Board, *ArriveMail);
#
# - ARGS
#	$CommentFlag	�����ȹԤ�ޤफ�ݤ�(0: �ޤޤʤ�, 1: �ޤ�)
#	$Board		�Ǽ���ID
#	*ArriveMail	������Υᥤ�륢�ɥ쥹�Υꥹ�ȤΥ�ե����
#
# - DESCRIPTION
#	�Ǽ����̿����ᥤ��������DB���ɤ߹��ࡥ
#	�ᥤ�륢�ɥ쥹�����������ݤ����Υ����å��ϡ����ڹԤʤ�ʤ���
#
# - RETURN
#	�ʤ�
#
sub getArriveMailTo {
    local($CommentFlag, $Board, *ArriveMail) = @_;
    local($ArriveMailFile);

    $ArriveMailFile = &GetPath($Board, $ARRIVEMAIL_FILE_NAME);
    # �ե����뤬�ʤ�����Τޤ�
    open(ARMAIL, "<$ArriveMailFile") || return;
    while(<ARMAIL>) {
    	# Version Check
	&VersionCheck('ARRIVEMAIL', $1), next if (m/^\# Kb-System-Id: ([^\/]*\/.*)$/o);
	next if ((! $CommentFlag) && (/^\#/o || /^$/o));
	chop;
	push(@ArriveMail, $_);
    }
    close(ARMAIL);
}


###
## updateArriveMailDb - �Ǽ����̿����ᥤ��������DB��������
#
# - SYNOPSIS
#	updateArriveMailDb($Board, *ArriveMail);
#
# - ARGS
#	$Board		�Ǽ���ID
#	*ArriveMail	������Υᥤ�륢�ɥ쥹�Υꥹ�ȤΥ�ե����
#			(�����ȡ����Ԥ�ޤޤ��)
#
# - DESCRIPTION
#	�Ǽ����̿����ᥤ��������DB�򡤿�����������ꥹ�Ȥǰ쿷���롥
#	�ᥤ�륢�ɥ쥹�����������ݤ����Υ����å��ϡ����ڹԤʤ�ʤ���
#
# - RETURN
#	�ʤ�
#
sub updateArriveMailDb {
    local($Board, *ArriveMail) = @_;
    local($File, $TmpFile);

    $File = &GetPath($Board, $ARRIVEMAIL_FILE_NAME);
    $TmpFile = &GetPath($Board, $ARRIVEMAIL_FILE_NAME);
    open(DBTMP, ">$TmpFile") || &Fatal(1, $TmpFile);
    foreach (@ArriveMail) { print(DBTMP "$_\n"); }
    close(DBTMP);
    rename($TmpFile, $File);
}


###
## CashAliasData - �桼��DB�����ɤ߹���
#
# - SYNOPSIS
#	CashAliasData;
#
# - ARGS
#	�ʤ�
#
# - DESCRIPTION
#	�桼�������ꥢ���ե�������ɤ߹����Ϣ�������������ࡥ
#	����ѿ���%Name, %Email, %Host, %URL���˲����롥
#
# - RETURN
#	�ʤ�
#
sub CashAliasData {

    local($A, $N, $E, $H, $U);

    # ������ࡥ
    open(ALIAS, "<$USER_ALIAS_FILE") || &Fatal(1, $USER_ALIAS_FILE);
    while(<ALIAS>) {

	# Version Check
	&VersionCheck('Alias', $1), next if (m/^<!-- Kb-System-Id: ([^\/]*\/.*) -->$/o);
	next if (/^$/o);
	chop;

	($A, $N, $E, $H, $U) = split(/\t/, $_);

	$Name{$A} = $N;
	$Email{$A} = $E;
	$Host{$A} = $H;
	$URL{$A} = $U;
    }
    close(ALIAS);

}


###
## GetUserInfo - �桼��DB���ɤ߹���
#
# - SYNOPSIS
#	GetUserInfo($Alias);
#
# - ARGS
#	$Alias		��������桼��ID(�����ꥢ��)
#
# - DESCRIPTION
#	�桼��DB���顤�桼����̾�����ᥤ�롤URL���äƤ��롥
#
# - RETURN
#	�桼����̾�����ᥤ�롤URL�ν�Υꥹ�ȡ�
#
sub GetUserInfo {
    local($Alias) = @_;
    local($A, $N, $E, $H, $U, $rN, $rE, $rU);

    # �ե�����򳫤�
    open(ALIAS, "<$USER_ALIAS_FILE") || &Fatal(1, $USER_ALIAS_FILE);
    
    # 1��1�ĥ����å���
    while(<ALIAS>) {
	
	# Version Check
	&VersionCheck('Alias', $1), next if (m/^<!-- Kb-System-Id: ([^\/]*\/.*) -->$/o);
	next if (/^$/o);
	chop;
	
	# ʬ��
	($A, $N, $E, $H, $U) = split(/\t/, $_);
	
	# �ޥå����ʤ��㼡�ء�
	next if ($A ne $Alias);
	
	$rN = $N;
	$rE = $E;
	$rU = $U;

    }
    close(ALIAS);

    # �ꥹ�Ȥˤ����֤�
    return($rN, $rE, $rU);
}


###
## WriteAliasData - �桼��DB�ι���/�ɲ�
#
# - SYNOPSIS
#	WriteAliasData;
#
# - ARGS
#	�ʤ�
#
# - DESCRIPTION
#	�桼�������ꥢ���ե�����˥ǡ�����񤭽Ф���
#	%Name, %Email, %Host, %URL��ɬ�פȤ��롥
#	$Name�������Ƚ񤭹��ޤʤ���
#
# - RETURN
#	�ʤ�
#
sub WriteAliasData {

    local($Alias, $TmpFile);

    $TmpFile = "$USER_ALIAS_FILE.$TMPFILE_SUFFIX";
    open(ALIAS, ">$TmpFile") || &Fatal(1, $TmpFile);

    # �С����������񤭽Ф�
    printf(ALIAS "<!-- Kb-System-Id: %s/%s -->\n", $KB_VERSION, $KB_RELEASE);

    # ��ˡ�
    foreach $Alias (sort keys(%Name)) {
	if ($Name{$Alias}) {
	    printf(ALIAS "%s\t%s\t%s\t%s\t%s\n", $Alias, $Name{$Alias}, $Email{$Alias}, $Host{$Alias}, $URL{$Alias});
	}
    }
    close(ALIAS);

    # ����
    rename($TmpFile, $USER_ALIAS_FILE);
    
}


###
## getAllBoardInfo - �Ǽ���DB�����ɤ߹���
#
# - SYNOPSIS
#	getAllBoardInfo(*BoardList, *BoardInfo);
#
# - ARGS
#	*BoardList	�Ǽ���ID-�Ǽ���̾��Ϣ������Υ�ե����
#	*BoardInfo	�Ǽ���ID-�Ǽ��ľ����Ϣ������Υ�ե����
#
# - DESCRIPTION
#	�Ǽ���DB���顤�Ǽ��ľ�����äƤ��롥
#
# - RETURN
#	�ʤ�
#
sub getAllBoardInfo {
    local(*BoardList, *BoardInfo) = @_;
    local($BoardId, $BName, $BInfo);

    open(ALIAS, "<$BOARD_ALIAS_FILE") || &Fatal(1, $BOARD_ALIAS_FILE);
    while(<ALIAS>) {

	# Version Check
	&VersionCheck('Board', $1), next if (m/^\# Kb-System-Id: ([^\/]*\/.*)$/o);
	next if (/^\#/o || /^$/o);
	chop;
	($BoardId, $BName, $BInfo) = split(/\t/, $_, 3);
	$BoardList{$BoardId} = $BName;
	$BoardInfo{$BoardId} = $BInfo;
    }
    close(ALIAS);
}


###
## GetBoardInfo - �Ǽ���DB���ɤ߹���
#
# - SYNOPSIS
#	GetBoardInfo($Alias);
#
# - ARGS
#	$Alias		�Ǽ���ID
#
# - DESCRIPTION
#	�Ǽ���DB���顤�Ǽ��ľ�����äƤ��롥
#
# - RETURN
#	�Ǽ���̾
#
sub GetBoardInfo {
    local($Alias) = @_;
    local($BoardName, $dAlias, $dBoardName);

    open(ALIAS, "<$BOARD_ALIAS_FILE") || &Fatal(1, $BOARD_ALIAS_FILE);
    while(<ALIAS>) {

	# Version Check
	&VersionCheck('Board', $1), next if (m/^\# Kb-System-Id: ([^\/]*\/.*)$/o);
	next if (/^\#/o || /^$/o);
	chop;
	($dAlias, $dBoardName) = split(/\t/, $_, 3);
	if ($Alias eq $dAlias) { $BoardName = $dBoardName; }
    }
    close(ALIAS);

    return($BoardName);

}


###
## cashIconDB - ��������DB�����ɤ߹���
#
# - SYNOPSIS
#	cashIconDB($Board);
#
# - ARGS
#	$Board		�Ǽ���ID
#
# - DESCRIPTION
#	��������DB���ɤ߹����Ϣ�������������ࡥ
#	����ѿ���%ICON_FILE��%ICON_HELP���˲����롥
#
# - RETURN
#	�ʤ�
#
$ICON_DB_CASH = 0;

sub cashIconDB {
    return if $ICON_DB_CASH;

    local($Board) = @_;
    local($FileName, $IconTitle, $IconHelp);

    # ����å���Υ��ꥢ
    %ICON_FILE = %ICON_HELP = ();

    # ��İ��ɽ��
    open(ICON, &GetIconPath("$Board.$ICONDEF_POSTFIX"))
	|| (open(ICON, &GetIconPath("$DEFAULT_ICONDEF"))
	    || &Fatal(1, &GetIconPath("$DEFAULT_ICONDEF")));
    while(<ICON>) {

	# Version Check
	&VersionCheck('Icon', $1), next if (m/^\# Kb-System-Id: ([^\/]*\/.*)$/o);
	next if (/^\#/o || /^$/o);
	chop;
	($FileName, $IconTitle, $IconHelp) = split(/\t/, $_, 3);

	# ������
	$ICON_FILE{$IconTitle} = $FileName;
	$ICON_HELP{$IconTitle} = $IconHelp;
    }
    close(ICON);

    $ICON_DB_CASH = 1;		# cashed

}


###
## getBoardHeader - �Ǽ��ĥإå�DB���ɤ߹���
#
# - SYNOPSIS
#	getBoardHeader($Board, *BoardHeader);
#
# - ARGS
#	$BoardId	�Ǽ���ID
#	*BoardHeader	��ʸ�ƹԤ�����������ѿ��ؤΥ�ե����
#
# - DESCRIPTION
#	�Ǽ��ĥǥ��쥯�ȥ����Ρ��Ǽ��ĥإå��ե�������ɤ߽Ф���
#
# - RETURN
#	�ʤ�
#
sub getBoardHeader {
    local($Board, *BoardHeader) = @_;
    local($File);

    $File = &GetPath($Board, $BOARD_FILE_NAME);
    open(HEADER, "<$File") || &Fatal(1, $File);
    while(<HEADER>){
	# Version Check
	&VersionCheck('Header', $1), next if (m/^<!-- Kb-System-Id: ([^\/]*\/.*) -->$/o);
	push(@BoardHeader, $_);
    }
    close(HEADER);
    
}


###
## GetArticleFileName - ������ʸDB�ե�����Υѥ�̾�μ���
#
# - SYNOPSIS
#	GetArticleFileName($Id, $Board);
#
# - ARGS
#	$Id		����ID
#	$Board		�Ǽ���ID
#
# - DESCRIPTION
#	�Ǽ���ID�ȵ���ID���顤����DB��Ρ������ե�����Υѥ�̾����Ф���
#	����ѿ�$ARCH�򻲾Ȥ���Mac/Win/UNIX���б���
#
# - RETURN
#	�ѥ���ɽ��ʸ����
#
sub GetArticleFileName {
    local($Id, $Board) = @_;

    # Board�����ʤ�Board�ǥ��쥯�ȥ��⤫�����С�
    # ���Ǥʤ���Х����ƥफ������
    return(($Board) ? "$Board/$Id" : "$Id") if ($ARCH eq 'UNIX');
    return(($Board) ? "$Board/$Id" : "$Id") if ($ARCH eq 'WinNT');
    return(($Board) ? "$Board/$Id" : "$Id") if ($ARCH eq 'Win95');
    return(($Board) ? ":$Board:$Id" : "$Id") if ($ARCH eq 'Mac');

}


###
## GetPath - DB�ե�����Υѥ�̾�μ���
#
# - SYNOPSIS
#	GetPath($Board, $File);
#
# - ARGS
#	$Board		�Ǽ���ID
#	$File		�ե�����̾
#
# - DESCRIPTION
#	�Ǽ���ID�ȥե�����̾���顤���ηǼ����Ѥ�DB�ե�����Υѥ�̾����Ф���
#	����ѿ�$ARCH�򻲾Ȥ���Mac/Win/UNIX���б���
#
# - RETURN
#	�ѥ���ɽ��ʸ����
#
sub GetPath {
    local($Board, $File) = @_;

    # �֤�
    return("$Board/$File") if ($ARCH eq 'UNIX');
    return("$Board/$File") if ($ARCH eq 'WinNT');
    return("$Board/$File") if ($ARCH eq 'Win95');
    return(":$Board:$File") if ($ARCH eq 'Mac');

}


###
## GetIconPath - ��������gifDB�ե�����Υѥ�̾�μ���
#
# - SYNOPSIS
#	GetIconPath($File);
#
# - ARGS
#	$File		��������gif�ե�����̾
#
# - DESCRIPTION
#	��������gif�ե�����Υѥ�̾����Ф���
#	����ѿ�$ARCH�򻲾Ȥ���Mac/Win/UNIX���б���
#
# - RETURN
#	�ѥ���ɽ��ʸ����
#
sub GetIconPath {
    local($File) = @_;

    # �֤�
    return("$ICON_DIR/$File") if ($ARCH eq 'UNIX');
    return("$ICON_DIR/$File") if ($ARCH eq 'WinNT');
    return("$ICON_DIR/$File") if ($ARCH eq 'Win95');
    return(":$ICON_DIR:$File") if ($ARCH eq 'Mac');

}


###
## GetIconURLFromTitle - ��������gif��URL�μ���
#
# - SYNOPSIS
#	GetIconURLFromTitle($Icon, $Board);
#
# - ARGS
#	$Icon		��������ID
#	$Board		�Ǽ���ID
#
# - DESCRIPTION
#	��������ID���顤���Υ���������б�����gif�ե������URL�������
#
# - RETURN
#	URL��ɽ��ʸ����
#
sub GetIconURLFromTitle {
    local($Icon, $Board) = @_;
    local($FileName, $Title, $TargetFile);

    # ��İ��ɽ��
    open(ICON, &GetIconPath("$Board.$ICONDEF_POSTFIX"))
	|| (open(ICON, &GetIconPath("$DEFAULT_ICONDEF"))
	    || &Fatal(1, &GetIconPath("$DEFAULT_ICONDEF")));
    while(<ICON>) {

	# Version Check
	&VersionCheck('Icon', $1), next if (m/^\# Kb-System-Id: ([^\/]*\/.*)$/o);
	next if (/^\#/o || /^$/o);
	chop;
	($FileName, $Title) = split(/\t/, $_, 3);
	if ($Title eq $Icon) { $TargetFile = $FileName;	}
    }
    close(ICON);

    return(($TargetFile) ? "$ICON_DIR/$TargetFile" : '');

}


###
## SupersedeDBFile - ���������ε���DB�ؤν񤭹���
#
# - SYNOPSIS
#	SupersedeDBFile($Board, $Id, $InputDate, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail);
#
# - ARGS
#	$Board		�������뵭�����ޤޤ��Ǽ��Ĥ�ID
#	$Id		�������뵭����ID
#	$InputDate	��������(UTC)
#	$Subject	��������Subject
#	$Icon		����������������
#	$RemoteHost	���������񤭹��ߥۥ���̾
#	$Name		���������񤭹��ߥ桼��̾
#	$Email		���������񤭹��ߥ桼���ᥤ�륢�ɥ쥹
#	$Url		���������񤭹��ߥ桼��URL
#	$Fmail		��ץ饤���˥ᥤ����������뤫�ݤ�
#
# - DESCRIPTION
#	����������DB�ե�����˽񤭹��ߡ�aging����������ID���֤���
#
# - RETURN
#	aging����������ID��
#
sub SupersedeDBFile {
    local($Board, $Id, $InputDate, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail) = @_;
    local($SupersedeId, $dId, $dFid, $dAids, $dInputDate, $dSubject, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail, $File, $TmpFile);
    
    # initial version��1�ǡ�1���������Ƥ�����1��2����9��10��11����
    # later version��DB���ɬ����younger version���Ⲽ�˽и����롥
    # ���ʤ��10_2��10��10_1�ϡ�10_1��10_2��10�ν���¤֤�ΤȤ��롥
    $SupersedeId = 1;

    $File = &GetPath($Board, $DB_FILE_NAME);
    $TmpFile = &GetPath($Board, "$DB_FILE_NAME.$TMPFILE_SUFFIX");
    open(DBTMP, ">$TmpFile") || &Fatal(1, $TmpFile);
    open(DB, "<$File") || &Fatal(1, $File);

    while(<DB>) {

	# Version Check
	&VersionCheck('DB', $1) if (m/^\# Kb-System-Id: ([^\/]*\/.*)$/o);

	print(DBTMP "$_"), next if (/^\#/o || /^$/o);
	chop;

	($dId, $dFid, $dAids, $dInputDate, $dSubject, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail) = split(/\t/, $_);

	# later version�����Ĥ��ä��顤version�����ɤߤ��Ƥ�����
	$SupersedeId++ if ("$dId" eq (sprintf("#-%s_%s", $Id, $SupersedeId)));

	# ���������κǿ��Ǥ����Ĥ��ä��顤
	if ($dId eq $Id) {

	    # aging���Ƥ��ޤ�
	    printf(DBTMP "#-%s_%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n", $dId, $SupersedeId, $dFid, $dAids, $dInputDate, $dSubject, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail);

	    # ³���ƿ�����������񤭲ä���
	    printf(DBTMP "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n", $Id, $dFid, $dAids, $InputDate, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail);

	} else {

	    # DB�˽񤭲ä���
	    print(DBTMP "$_\n");

	}

    }

    # close Files.
    close(DB);
    close(DBTMP);

    # DB�򹹿�����
    rename($TmpFile, $File);

    # �֤�
    return($SupersedeId);

}
