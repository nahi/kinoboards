#!/usr/local/bin/perl5
#
# $Id: kb.cgi,v 4.43 1997-06-24 15:57:35 nakahiro Exp $


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
$TIME = time;			# �ץ���൯ư����
$SERVER_NAME = $ENV{'SERVER_NAME'};
$SERVER_PORT = $ENV{'SERVER_PORT'};
$SERVER_PORT_STRING = (($SERVER_PORT == 80) || ($SYS_PORTNO == 0)) ? '' : ":$SERVER_PORT";
$SCRIPT_NAME = $ENV{'SCRIPT_NAME'};
$REMOTE_HOST = $ENV{'REMOTE_HOST'};
$PATH_INFO = $ENV{'PATH_INFO'};
$PATH_TRANSLATED = $ENV{'PATH_TRANSLATED'};
($CGIPROG_NAME = $SCRIPT_NAME) =~ s!^(.*/)!!o;
$SYSDIR_NAME = (($PATH_INFO) ? "$PATH_INFO/" : "$1");
$SCRIPT_URL = "http://$SERVER_NAME$SERVER_PORT_STRING$SCRIPT_NAME$PATH_INFO";
$PROGRAM = (($PATH_INFO) ? "$SCRIPT_NAME$PATH_INFO" : $CGIPROG_NAME);

# ���󥯥롼�ɥե�������ɤ߹���
if ($PATH_INFO && (-s 'kb.ph')) { require('kb.ph'); }
if ($PATH_TRANSLATED ne '') { chdir($PATH_TRANSLATED); }
require('kb.ph');
require('cgi.pl');
require('jcode.pl');

# ����ѿ������
$[ = 0; $| = 1;

# Version��Release�ֹ�
$KB_VERSION = '1.0';
$KB_RELEASE = '4.0pre';

# ���ɽ��ʸ����
$ADDRESS = sprintf("Maintenance: <a href=\"mailto:%s\">%s</a><br><a href=\"http://www.kinotrope.co.jp/~nakahiro/kb10.shtml\">KINOBOARDS/%s R%s</a>: Copyright (C) 1995, 96, 97 <a href=\"http://www.kinotrope.co.jp/~nakahiro/\">NAKAMURA Hiroshi</a>.", $MAINT, $MAINT_NAME, $KB_VERSION, $KB_RELEASE);

# �ե�����
$BOARD_ALIAS_FILE = 'kinoboards';		# �Ǽ���DB
$CONF_FILE_NAME = '.kbconf';			# �Ǽ�����configuratin�ե�����
$ARRIVEMAIL_FILE_NAME = '.kbmail';		# �Ǽ����̿����ᥤ��������DB
$BOARD_FILE_NAME = '.board';			# �����ȥ�ꥹ�ȥإå�
$DB_FILE_NAME = '.db';				# ����DB
$DB_TMP_FILE_NAME = '.db.tmp';			# ����DB�ƥ�ݥ��
$ARTICLE_NUM_FILE_NAME = '.articleid';		# �����ֹ�DB
$ARTICLE_NUM_TMP_FILE_NAME = '.articleid.tmp';	# �����ֹ�DB�ƥ�ݥ��
$USER_ALIAS_FILE = 'kinousers';			# �桼��DB
$USER_ALIAS_TMP_FILE = 'kinousers.tmp';		# �桼��DB�ƥ�ݥ��
$DEFAULT_ICONDEF = 'all.idef';			# ��������DB
$LOCK_FILE = '.lock.kb';			# ��å��ե�����

# ��������ǥ��쥯�ȥ�
# (��������ȥ�����������ե�����������ǥ��쥯�ȥ�̾)
$ICON_DIR = 'icons';
# ������������ե�����Υݥ��ȥե�����
# ������������ե����롤��(�ܡ��ɥǥ��쥯�ȥ�̾).(���ꤷ��ʸ����)�פˤʤ롥
$ICONDEF_POSTFIX = 'idef';

# ��������ե���������URL
$ICON_TLIST = "$ICON_DIR/tlist.gif";		# �����ȥ������
$ICON_PREV = "$ICON_DIR/prev.gif";		# ���ε�����
$ICON_NEXT = "$ICON_DIR/next.gif";		# ���ε�����
$ICON_WRITENEW = "$ICON_DIR/writenew.gif";	# �����񤭹���
$ICON_FOLLOW = "$ICON_DIR/follow.gif";		# ��ץ饤
$ICON_QUOTE = "$ICON_DIR/quote.gif";		# ���Ѥ��ƥ�ץ饤
$ICON_THREAD = "$ICON_DIR/thread.gif";		# �ޤȤ��ɤ�
$ICON_HELP = "$ICON_DIR/help.gif";		# �إ��

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
#
# - RETURN
#	�ʤ�
#
&cgi'lock($LOCK_FILE) || &Fatal(999, '');

MAIN: {

    local($BoardConfFile, $Command, $Com, $Id);

    # ɸ������(POST)�ޤ��ϴĶ��ѿ�(GET)�Υǥ����ɡ�
    &cgi'Decode;

    # ���ˤ˻Ȥ��Τ�����ѿ���Ȥ�(���ʤ�)
    $BOARDNAME = &GetBoardInfo($BOARD = $cgi'TAGS{'b'});
    # ������͡�
    if ($BOARDNAME =~ m!/!o) { &Fatal(11, $BOARDNAME); }

    # �Ǽ��ĸ�ͭ���åƥ��󥰤��ɤ߹���
    $BoardConfFile = &GetPath($BOARD, $CONF_FILE_NAME);
    if (-s "$BoardConfFile") {
	require("$BoardConfFile");
    }

    # DB������ѿ��˥���å���
    if ($BOARD) { &DbCash; }

    # �ͤ����
    $Command = $cgi'TAGS{'c'};
    $Com = $cgi'TAGS{'com'};
    $Id = $cgi'TAGS{'id'};

    # ���ޥ�ɥ����פˤ��ʬ��
    &ShowArticle($Id),	last if ($SYS_F_E && ($Command eq 'e'));
    &ThreadArticle($Id),last if ($SYS_F_T && ($Command eq 't'));
    &Entry('', ''),	last if ($SYS_F_N && ($Command eq 'n'));
    &Entry('', $Id),	last if ($SYS_F_FQ && ($Command eq 'f'));
    &Entry('quote', $Id),last if ($SYS_F_FQ && ($Command eq 'q'));
    &Preview,		last if (($SYS_F_N || $SYS_F_FQ) && ($Command eq 'p') && ($Com ne 'x'));
    &Thanks,		last if (($SYS_F_N || $SYS_F_FQ) && ($Command eq 'x'));
    &Thanks,		last if (($SYS_F_N || $SYS_F_FQ) && ($Command eq 'p') && ($Com eq 'x'));
    &ViewTitle,		last if ($SYS_F_V && ($Command eq 'v'));
    &SortArticle,	last if ($SYS_F_R && ($Command eq 'r'));
    &NewArticle,	last if ($SYS_F_L && ($Command eq 'l'));
    &SearchArticle,	last if ($SYS_F_S && ($Command eq 's'));
    &ShowIcon,		last if ($SYS_F_I && ($Command eq 'i'));
    &AliasNew,		last if ($SYS_ALIAS && ($Command eq 'an'));
    &AliasMod,		last if ($SYS_ALIAS && ($Command eq 'am'));
    &AliasDel,		last if ($SYS_ALIAS && ($Command eq 'ad'));
    &AliasShow,		last if ($SYS_ALIAS && ($Command eq 'as'));

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
# �ȤϤ�������®���Τ��ᡤDB��ľ�ܤ����äƤ���⥸�塼��⤢��ޤ���
# �Ȥ�ʤ���ǽ���б�����ؿ��ϡ����ʧ�äƤ�ư���ġĤϤ��Ǥ�
# (�����ƥ��ȤϤ��Ƥޤ��� ^_^;)��


###
## Entry - �񤭹��߲��̤�ɽ��
#
# - SYNOPSIS
#	Entry($QuoteFlag, $Id);
#
# - ARGS
#	$QuoteFlag	���Ѥ���/�ʤ�
#	$Id		���Ѥ�����Ϥ���Id(���Ѥ��ʤ����϶�)
#
# - DESCRIPTION
#	�񤭹��߲��̤�ɽ������
#
# - RETURN
#	�ʤ�
#
sub Entry {
    local($QuoteFlag, $Id) = @_;

    # ɽ�����̤κ���
    &MsgHeader('Message entry', "$BOARDNAME: $H_MESG�ν񤭹���");

    # �ե����ξ��
    if ($Id ne '') {
	# ������ɽ��(���ޥ��̵��, ����������)
	&ViewOriginalArticle($Id, 0, 1);
	&cgiprint'Cache("<hr>\n<h2>���$H_MESG�ؤ�$H_REPLY��񤭹���</h2>");
    }

    # ����«
    &cgiprint'Cache(<<__EOF__);
<form action="$PROGRAM" method="POST">
<input name="c" type="hidden" value="p">
<input name="b" type="hidden" value="$BOARD">
<input name="id" type="hidden" value="$Id">
<p>
$H_SUBJECT��$H_MESG��$H_FROM��$H_MAIL������˥����֥ڡ����򤪻��������ϡ�
�ۡ���ڡ�����$H_URL��񤭹���Ǥ�������(�����󡤤ʤ��Ƥ⹽���ޤ���)��
__EOF__

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
	&cgiprint'Cache(<<__EOF__);
$H_ICON:
<SELECT NAME="icon">
<OPTION SELECTED>$H_NOICON
__EOF__

	# ��İ��ɽ��
	open(ICON, &GetIconPath("$BOARD.$ICONDEF_POSTFIX"))
	    || (open(ICON, &GetIconPath("$DEFAULT_ICONDEF"))
		|| &Fatal(1, &GetIconPath("$DEFAULT_ICONDEF")));
	while(<ICON>) {

	    # Version Check
	    &VersionCheck('Icon', $1), next if (m/^\# Kb-System-Id: ([^\/]*\/.*)$/o);
	    next if (/^\#/o || /^$/o);

	    # ɽ��
	    chop;
	    ($FileName, $Title) = split(/\t/, $_, 3);
	    &cgiprint'Cache("<OPTION>$Title\n");

	}
	close(ICON);
	&cgiprint'Cache("</SELECT>\n");

	if ($SYS_F_I) {
	    &cgiprint'Cache("(<a href=\"$PROGRAM?b=$BOARD&c=i&type=entry\">�������������</a>)<BR>\n");
	}

    }

    # Subject(�ե����ʤ鼫ưŪ��ʸ����������)
    &cgiprint'Cache(sprintf("%s: <input name=\"subject\" type=\"text\" value=\"%s\" size=\"%s\"><br>\n", $H_SUBJECT, (($Id eq '') ? '' : &GetReplySubject($Id)), $SUBJECT_LENGTH));

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
    if (($Id ne '') && ($QuoteFlag eq 'quote')) {
	&QuoteOriginalArticle($Id, $BOARD);
    }
    &cgiprint'Cache("</textarea></p>\n");

    # �եå���ʬ��ɽ��
    # ̾���ȥᥤ�륢�ɥ쥹��URL��
    &cgiprint'Cache(<<__EOF__);
<p>
$H_MESG��˴�Ϣ�����֥ڡ����ؤΥ�󥯤�ĥ����ϡ�
��&lt;URL:http://��&gt;�פΤ褦�ˡ�URL���&lt;URL:�פȡ�&gt;�פǰϤ��
�񤭹���Ǥ�����������ưŪ�˥�󥯤�ĥ���ޤ���
</p><p>
$H_FROM: <input name="name" type="text" size="$NAME_LENGTH"><br>
$H_MAIL: <input name="mail" type="text" size="$MAIL_LENGTH"><br>
$H_URL_S: <input name="url" type="text" value="http://" size="$URL_LENGTH"><br>
__EOF__

    if ($SYS_MAIL) {
	&cgiprint'Cache("$H_REPLY�����ä����˥ᥤ����Τ餻�ޤ���? <input name=\"fmail\" type=\"checkbox\" value=\"on\"><br>\n");
    }
    
    if ($SYS_ALIAS) {
	&cgiprint'Cache(<<__EOF__);
</p><p>
��$H_ALIAS�פˡ�$H_FROM��$H_MAIL��$H_URL����Ͽ�ʤ��äƤ������ϡ�
��$H_FROM�פˡ�#...�פȤ�����Ͽ̾��񤤤Ƥ���������
��ưŪ��$H_FROM��$H_MAIL��$H_URL������ޤ���
(<a href="$PROGRAM?c=as">$H_ALIAS�ΰ���</a> //
 <a href="$PROGRAM?c=an">$H_ALIAS����Ͽ</a>)
__EOF__

    }

    # �ܥ���
    &cgiprint'Cache(<<__EOF__);
</p><p>
�񤭹�������Ƥ�<br>
<input type="radio" name="com" value="p" CHECKED>: ���ɽ�����Ƥߤ�(�ޤ���Ƥ��ޤ���)<br>
<input type="radio" name="com" value="x">: $H_MESG����Ƥ���<br>
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

    local($Id, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail, $rFid);

    # ���Ϥ��줿��������
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
    $Article = &CheckArticle($TextType, *Name, *Email, *Url, *Subject, *Icon, $Article);

    # ��ǧ���̤κ���
    &MsgHeader('Message preview', "�񤭹��ߤ����Ƥ��ǧ���Ƥ�������");

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

<p>
ɬ�פǤ���С��֥饦����BACK�ܥ������äơ��񤭹��ߤ������Ƥ���������
�������Хܥ���򲡤��ƽ񤭹��ߤޤ��礦��
<input type="submit" value="��Ƥ���">
</p><p>
__EOF__

    # ��
    (($Icon eq $H_NOICON) || (! $Icon))
        ? &cgiprint'Cache("<strong>$H_SUBJECT</strong>: $Subject")
            : &cgiprint'Cache(sprintf("<strong>$H_SUBJECT</strong>: <img src=\"%s\" alt=\"$Icon \" width=\"$MSGICON_WIDTH\" height=\"$MSGICON_HEIGHT\">$Subject", &GetIconURLFromTitle($Icon)));

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

    # ����«
    &cgiprint'Cache("</form>\n");

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

    local($Id, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail, $ArticleId);

    # ���Ϥ��줿��������
    $Id = $cgi'TAGS{'id'};
    $TextType = $cgi'TAGS{'texttype'};
    $Name = $cgi'TAGS{'name'};
    $Email = $cgi'TAGS{'mail'};
    $Url = $cgi'TAGS{'url'};
    $Icon = $cgi'TAGS{'icon'};
    $Subject = $cgi'TAGS{'subject'};
    $Article = $cgi'TAGS{'article'};
    $Fmail = $cgi'TAGS{'fmail'};

    # �����κ���
    &MakeNewArticle($Id, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail);

    # ɽ�����̤κ���
    &MsgHeader('Message entried', "�񤭹��ߤ��꤬�Ȥ��������ޤ���");

    &cgiprint'Cache(<<__EOF__);
<p>
�񤭹��ߤ���������äʤɤϡ�
�ᥤ���<a href=\"mailto:$MAINT\">$MAINT</a>�ޤǸ�Ϣ����������
</p>
__EOF__

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
#	ShowArticle($Id);
#
# - ARGS
#	$Id	����ID
#
# - DESCRIPTION
#	ñ��ε�����ɽ�����롥
#
# - RETURN
#	�ʤ�
#
sub ShowArticle {
    local($Id) = @_;
    local($Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $DateUtc, $Aid, @AidList, @FollowIdTree);

    ($Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url) = &GetArticlesInfo($Id);
    $DateUtc = &GetUtcFromOldDateTimeFormat($Date);
    @AidList = split(/,/, $Aids);

    # ̤��Ƶ������ɤ�ʤ�
    if ($Name eq '') { &Fatal(8, ''); }

    # ɽ�����̤κ���
    &MsgHeader('Message view', "$Subject", $DateUtc);
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
#	ThreadArticle($Id);
#
# - ARGS
#	$Id	����ID
#
# - DESCRIPTION
#	���뵭���ȡ����ε����ؤΥ�ץ饤������ޤȤ��ɽ�����롥
#
# - RETURN
#	�ʤ�
#
sub ThreadArticle {
    local($Id) = @_;
    local(@FollowIdTree);

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
	    &cgiprint'Cache("<li>" . &GetFormattedTitle($Head, $dAids, $dIcon, $dSubject, $dName, $dDate) . "\n");
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

    local($FileName, $Title, $Help, $Type);

    # �����פ򽦤�
    $Type = $cgi'TAGS{'type'};

    # ɽ�����̤κ���
    &MsgHeader('Icon show', "�������������");

    if ($Type eq 'article') {

	&cgiprint'Cache(<<__EOF__);
<p>
�ƥ�������ϼ��ε�ǽ��ɽ���Ƥ��ޤ���
</p>
<p>
<ul>
<li><img src="$ICON_TLIST" alt="$H_BACKTITLE" height="$COMICON_HEIGHT" width="$COMICON_WIDTH"> : $H_BACKTITLE
<li><img src="$ICON_PREV" alt="$H_PREVARTICLE" height="$COMICON_HEIGHT" width="$COMICON_WIDTH"> : $H_PREVARTICLE
<li><img src="$ICON_NEXT" alt="$H_NEXTARTICLE" height="$COMICON_HEIGHT" width="$COMICON_WIDTH"> : $H_NEXTARTICLE
<li><img src="$ICON_THREAD" alt="$H_READREPLYALL" height="$COMICON_HEIGHT" width="$COMICON_WIDTH"> : $H_READREPLYALL
<li><img src="$ICON_WRITENEW" alt="$H_POSTNEWARTICLE" height="$COMICON_HEIGHT" width="$COMICON_WIDTH"> : $H_POSTNEWARTICLE
<li><img src="$ICON_FOLLOW" alt="$H_REPLYTHISARTICLE" height="$COMICON_HEIGHT" width="$COMICON_WIDTH"> : $H_REPLYTHISARTICLE
<li><img src="$ICON_QUOTE" alt="$H_REPLYTHISARTICLEQUOTE" height="$COMICON_HEIGHT" width="$COMICON_WIDTH"> : $H_REPLYTHISARTICLEQUOTE
</ul>
</p>
__EOF__

    } else {

	&cgiprint'Cache(<<__EOF__);
<p>
�ƥ�������ϼ��ε�ǽ��ɽ���Ƥ��ޤ���
<p>
<ul>
<li>$H_THREAD : ����$H_MESG��$H_REPLY��ޤȤ���ɤ�
</ul>
</p>
<p>
�Ǽ��ġ�$BOARDNAME�פǤϡ����Υ��������Ȥ����Ȥ��Ǥ��ޤ���
</p>
<p>
<ul>
__EOF__

	# ��İ��ɽ��
	open(ICON, &GetIconPath("$BOARD.$ICONDEF_POSTFIX"))
	    || (open(ICON, &GetIconPath("$DEFAULT_ICONDEF"))
		|| &Fatal(1, &GetIconPath("$DEFAULT_ICONDEF")));
	while(<ICON>) {

	    # Version Check
	    &VersionCheck('Icon', $1), next if (m/^\# Kb-System-Id: ([^\/]*\/.*)$/o);
	    next if (/^\#/o || /^$/o);
	    chop;
	    ($FileName, $Title, $Help) = split(/\t/, $_, 3);

	    # ɽ��
	    &cgiprint'Cache(sprintf("<li><img src=\"$ICON_DIR/$FileName\" alt=\"$Title\" height=\"$MSGICON_HEIGHT\" width=\"$MSGICON_WIDTH\"> : %s\n", ($Help || $Title)));
	}
	close(ICON);

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

    &BoardHeader;

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
		&cgiprint'Cache("<li>" . &GetFormattedTitle($Id, $DB_AIDS{$Id}, $DB_ICON{$Id}, $DB_TITLE{$Id}, $DB_NAME{$Id}, $DB_DATE{$Id}) . "\n");
	    }
	} else {
	    for ($IdNum = $To; $IdNum >= $From; $IdNum--) {
		$Id = $DB_ID[$IdNum];
		&cgiprint'Cache("<li>" . &GetFormattedTitle($Id, $DB_AIDS{$Id}, $DB_ICON{$Id}, $DB_TITLE{$Id}, $DB_NAME{$Id}, $DB_DATE{$Id}) . "\n");
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
#	ViewTitle;
#
# - ARGS
#	�ʤ�
#
# - DESCRIPTION
#	�����������Υ����ȥ�򥹥�å��̤˥����Ȥ���ɽ����
#	����ѿ��Ǥ��롤CGI�ѿ��򻲾Ȥ��롥
#
# - RETURN
#	�ʤ�
#
sub ViewTitle {

    local($Num, $Old, $NextOld, $BackOld, $To, $From, $IdNum, $Id, $Fid, %AddFlag);

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
    for($IdNum = $From; $IdNum <= $To; $IdNum++) { $AddFlag{$DB_ID[$IdNum]} = 2; }

    # ɽ�����̤κ���
    &MsgHeader('Title view (threaded)', "$BOARDNAME: $H_SUBJECT����($H_REPLY��)");

    &BoardHeader;

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
	for($IdNum = $From; $IdNum <= $To; $IdNum++) {

	    # ����������ID����Ф�
	    $Id = $DB_ID[$IdNum];
	    ($Fid = $DB_FID{$Id}) =~ s/,.*$//o;
	    # �������Ȥϸ�󤷡�
	    next if (($Fid ne '') && ($AddFlag{$Fid} == 2));
	    # �Ρ��ɤ�ɽ��
	    &ViewTitleNode($Id, *AddFlag);

	}
    } else {

	# �������Τ������
	for($IdNum = $To; $IdNum >= $From; $IdNum--) {
	    # ���Ʊ��
	    $Id = $DB_ID[$IdNum];
	    ($Fid = $DB_FID{$Id}) =~ s/,.*$//o;
	    next if (($Fid ne '') && ($AddFlag{$Fid} == 2));
	    &ViewTitleNode($Id, *AddFlag);
	}
    }

    &cgiprint'Cache("</ul></p>\n");

    if ($SYS_BOTTOMTITLE) {
	&cgiprint'Cache("<p>$H_BOTTOM<a href=\"$PROGRAM?b=$BOARD&c=v&num=$Num&old=$NextOld\">$H_NEXTART</a></p>\n") if ($Old);
    } else {
	&cgiprint'Cache("<p>$H_BOTTOM<a href=\"$PROGRAM?b=$BOARD&c=v&num=$Num&old=$BackOld\">$H_BACKART</a></p>\n") if ($From > 0);
    }

    &MsgFooter;

}

sub ViewTitleNode {
    local($Id, *AddFlag) = @_;

    if ($AddFlag{$Id} != 2) { return; }

    &cgiprint'Cache("<li>" . &GetFormattedTitle($Id, $DB_AIDS{$Id}, $DB_ICON{$Id}, $DB_TITLE{$Id}, $DB_NAME{$Id}, $DB_DATE{$Id}) . "\n");
    $AddFlag{$Id} = 1;		# �����Ѥ�

    # ̼�����Сġ�
    if ($DB_AIDS{$Id}) {
	&cgiprint'Cache("<ul>\n");
	foreach (split(/,/, $DB_AIDS{$Id})) { &ViewTitleNode($_, *AddFlag); }
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

    local($Key, $SearchSubject, $SearchPerson, $SearchArticle, $SearchIcon, $Icon);

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
    &cgiprint'Cache(sprintf("<SELECT NAME=\"icon\">\n<OPTION%s>$H_NOICON\n", (($Icon && ($Icon ne $H_NOICON)) ? '' : ' SELECTED')));
	
    # ��İ��ɽ��
    open(ICON, &GetIconPath("$BOARD.$ICONDEF_POSTFIX"))
	|| (open(ICON, &GetIconPath("$DEFAULT_ICONDEF"))
	    || &Fatal(1, &GetIconPath("$DEFAULT_ICONDEF")));
    while(<ICON>) {

	# Version Check
	&VersionCheck('Icon', $1), next if (m/^\# Kb-System-Id: ([^\/]*\/.*)$/o);
	next if (/^\#/o || /^$/o);
	chop;
	($FileName, $IconTitle) = split(/\t/, $_, 3);

	# ɽ��
	&cgiprint'Cache(sprintf("<OPTION%s>$IconTitle\n", (($Icon eq $IconTitle) ? ' SELECTED' : '')));
    }
    close(ICON);
    &cgiprint'Cache("</SELECT>\n");

    # �����������
    if ($SYS_F_I) {
	&cgiprint'Cache(<<__EOF__);
(<a href="$PROGRAM?b=$BOARD&c=i&type=entry">�������������</a>)
__EOF__
    }

    &cgiprint'Cache(<<__EOF__);
<BR>
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
	    if (($Article ne '') && ($Line = &SearchArticleKeyword($dId, @KeyList))) {
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
	    &cgiprint'Cache("<li>" . &GetFormattedTitle($dId, $dAids, $dIcon, $dTitle, $dName, $dDate) . "\n");

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
    &CashAliasData($USER_ALIAS_FILE);
    
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
    &WriteAliasData($USER_ALIAS_FILE);

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
    &CashAliasData($USER_ALIAS_FILE);
    
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
    &WriteAliasData($USER_ALIAS_FILE);
    
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
    &CashAliasData($USER_ALIAS_FILE);
    
    # ɽ�����̤κ���
    &MsgHeader('Alias view', "$H_ALIAS�λ���");
    # ������ʸ
    &cgiprint'Cache(<<__EOF__);
<p>
��Ƥκݡ���$H_FROM�פ���ʬ�˰ʲ�����Ͽ̾(��#....��)�����Ϥ���ȡ�
��Ͽ����Ƥ���$H_FROM��$H_MAIL��$H_URL����ưŪ������ޤ���
</p><p>
<a href="$PROGRAM?c=an">������Ͽ/��Ͽ���Ƥ��ѹ�</a>
</p>
__EOF__
    
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


######################################################################
# �桼�����󥿥ե���������ץ���ơ������(������)
#
# �ȤϤ�������®���Τ��ᡤDB��ľ�ܤ����äƤ���⥸�塼��⤢��ޤ���


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

	$ErrString = "$FatalInfo�Ȥ��������ꥢ���ϡ���Ͽ����Ƥ��ޤ���";

    } elsif ($FatalNo == 7) {

	$ErrString = "$FatalInfo��������������ޤ���? ��äƤ⤦���٤��ľ���ƤߤƤ���������";

    } elsif ($FatalNo == 8) {

	$ErrString = "���ε����Ϥޤ���Ƥ���Ƥ��ޤ���";

    } elsif ($FatalNo == 9) {

	$ErrString = "�ᥤ�뤬�����Ǥ��ޤ���Ǥ�����������Ǥ��������Υ��顼��å������ȡ����顼��������������<a href=\"mailto:$MAINT\">$MAINT</a>�ޤǤ��Τ餻����������";

    } elsif ($FatalNo == 10) {

	$ErrString = ".db��.articleid�������������Ƥ��ޤ��󡥤�����Ǥ��������Υ��顼��å������ȡ����顼��������������<a href=\"mailto:$MAINT\">$MAINT</a>�ޤǤ��Τ餻����������";

    } elsif ($FatalNo == 11) {

	$ErrString = "$FatalInfo�Ȥ����Ǽ���ID���б�����Ǽ��Ĥϡ�¸�ߤ��ޤ���";

    } elsif ($FatalNo == 99) {

	$ErrString ="���ηǼ��ĤǤϡ����Υ��ޥ�ɤϼ¹ԤǤ��ޤ���";

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
    local($QuoteFile, $Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $PrevId, $NextId, $Num, $InputDate);

    $QuoteFile = &GetArticleFileName($Id, $BOARD);
    ($Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url) = &GetArticlesInfo($Id);

    foreach ($[ .. $#DB_ID) { $Num = $_, last if ($DB_ID[$_] eq $Id); }
    $PrevId = $DB_ID[$Num - 1] if ($Num > $[);
    $NextId = $DB_ID[$Num + 1];

    # ���ޥ��ɽ��?
    if ($CommandFlag && $SYS_COMMAND) {

	&cgiprint'Cache("<p>\n");

	if ($SYS_COMICON == 2) {

	    if ($SYS_F_V) {
		&cgiprint'Cache("<a href=\"$PROGRAM?b=$BOARD&c=v&num=$DEF_TITLE_NUM\"><img src=\"$ICON_TLIST\" alt=\"$H_BACKTITLE\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\">$H_BACKTITLE</a>\n");
	    }

	    if ($SYS_F_E) {
		if ($PrevId ne '') {
		    &cgiprint'Cache(" // <a href=\"$PROGRAM?b=$BOARD&c=e&id=$PrevId\"><img src=\"$ICON_PREV\" alt=\"$H_PREVARTICLE\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\">$H_PREVARTICLE</a>\n");
		} else {
		    &cgiprint'Cache(" // <img src=\"$ICON_PREV\" alt=\"$H_PREVARTICLE\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\">$H_PREVARTICLE\n");
		}

		if ($NextId ne '') {
		    &cgiprint'Cache(" // <a href=\"$PROGRAM?b=$BOARD&c=e&id=$NextId\"><img src=\"$ICON_NEXT\" alt=\"$H_NEXTARTICLE\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\">$H_NEXTARTICLE</a>\n");
		} else {
		    &cgiprint'Cache(" // <img src=\"$ICON_NEXT\" alt=\"$H_NEXTARTICLE\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\">$H_NEXTARTICLE\n");
		}
	    }

	    if ($SYS_F_T) {
		if ($Aids ne '') {
		    &cgiprint'Cache(" // <a href=\"$PROGRAM?b=$BOARD&c=t&id=$Id\"><img src=\"$ICON_THREAD\" alt=\"$H_READREPLYALL\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\">$H_READREPLYALL</a>\n");
		} else {
		    &cgiprint'Cache(" // <img src=\"$ICON_THREAD\" alt=\"$H_READREPLYALL\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\">$H_READREPLYALL\n");
		}
	    }

	    if ($SYS_F_N) {
		&cgiprint'Cache(" // <a href=\"$PROGRAM?b=$BOARD&c=n\"><img src=\"$ICON_WRITENEW\" alt=\"$H_POSTNEWARTICLE\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\">$H_POSTNEWARTICLE</a>\n");
	    }    

	    if ($SYS_F_FQ) {
		&cgiprint'Cache(<<__EOF__);
 // <a href="$PROGRAM?b=$BOARD&c=f&id=$Id"><img src="$ICON_FOLLOW" alt="$H_REPLYTHISARTICLE" width="$COMICON_WIDTH" height="$COMICON_HEIGHT" BORDER="0">$H_REPLYTHISARTICLE</a>
 // <a href="$PROGRAM?b=$BOARD&c=q&id=$Id"><img src="$ICON_QUOTE" alt="$H_REPLYTHISARTICLEQUOTE" width="$COMICON_WIDTH" height="$COMICON_HEIGHT" BORDER="0">$H_REPLYTHISARTICLEQUOTE</a>
__EOF__
	    }

	    if ($SYS_F_I) {
		&cgiprint'Cache(" // <a href=\"$PROGRAM?b=$BOARD&c=i&type=article\"><img src=\"$ICON_HELP\" alt=\"?\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\">?</a>\n");
	    }

	} elsif ($SYS_COMICON == 1) {

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

	    if ($SYS_F_I) {
		&cgiprint'Cache("<a href=\"$PROGRAM?b=$BOARD&c=i&type=article\"><img src=\"$ICON_HELP\" alt=\"?\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\"></a>\n");
	    }

	} else {

	    if ($SYS_F_V) {
		&cgiprint'Cache("<a href=\"$PROGRAM?b=$BOARD&c=v&num=$DEF_TITLE_NUM\">$H_BACKTITLE</a>\n");
	    }

	    if ($SYS_F_E) {
		if ($PrevId ne '') {
		    &cgiprint'Cache(" // <a href=\"$PROGRAM?b=$BOARD&c=e&id=$PrevId\">$H_PREVARTICLE</a>\n");
		} else {
		    &cgiprint'Cache(" // $H_PREVARTICLE\n");
		}

		if ($NextId ne '') {
		    &cgiprint'Cache(" // <a href=\"$PROGRAM?b=$BOARD&c=e&id=$NextId\">$H_NEXTARTICLE</a>\n");
		} else {
		    &cgiprint'Cache(" // $H_NEXTARTICLE\n");
		}
	    }

	    if ($SYS_F_T) {
		if ($Aids ne '') {
		    &cgiprint'Cache(" // <a href=\"$PROGRAM?b=$BOARD&c=t&id=$Id\">$H_READREPLYALL</a>");
		} else {
		    &cgiprint'Cache(" // $H_READREPLYALL");
		}
	    }

	    if ($SYS_F_N) {
		&cgiprint'Cache(" // <a href=\"$PROGRAM?b=$BOARD&c=n\">$H_POSTNEWARTICLE</a>\n");
	    }

	    if ($SYS_F_FQ) {
		&cgiprint'Cache(<<__EOF__);
 // <a href="$PROGRAM?b=$BOARD&c=f&id=$Id">$H_REPLYTHISARTICLE</a>
 // <a href="$PROGRAM?b=$BOARD&c=q&id=$Id">$H_REPLYTHISARTICLEQUOTE</a>
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
	&cgiprint'Cache(sprintf("<strong>$H_SUBJECT</strong>: <strong>$Id .</strong> <img src=\"%s\" alt=\"$Icon \" width=\"$MSGICON_WIDTH\" height=\"$MSGICON_HEIGHT\">$Subject", &GetIconURLFromTitle($Icon)));
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
    open(TMP, "<$QuoteFile") || &Fatal(1, $QuoteFile);
    while(<TMP>) {

	# Version Check
	&VersionCheck('Article', $1), next if (m/^<!-- Kb-System-Id: ([^\/]*\/.*) -->$/o);

	# ɽ��
	&cgiprint'Cache("$_");

    }
    close(TMP);

}


###
## QuoteOriginalArticle - ���Ѥ���
#
# - SYNOPSIS
#	QuoteOriginalArticle($Id, $Board);
#
# - ARGS
#	$Id		����ID
#	$Board		�Ǽ���ID
#
# - DESCRIPTION
#	��������Ѥ���ɽ������
#
# - RETURN
#	�ʤ�
#
sub QuoteOriginalArticle {
    local($Id, $Board) = @_;
    local($QuoteFile, $Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name);

    # ����������μ���
    $QuoteFile = &GetArticleFileName($Id, $Board);
    ($Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name) = &GetArticlesInfo($Id);

    # �ե�����򳫤�
    open(TMP, "<$QuoteFile") || &Fatal(1, $QuoteFile);
    while(<TMP>) {

	# Version Check
	&VersionCheck('Article', $1), next if (m/^<!-- Kb-System-Id: ([^\/]*\/.*) -->$/o);

	# ���ѤΤ�����Ѵ�
	s/[\&\"]//go;
	s/<[^>]*>//go;

	# ����ʸ�����ɽ��
	&cgiprint'Cache(sprintf("%s%s%s", $Name, $DEFAULT_QMARK, $_));
	
    }

    # �Ĥ���
    close(TMP);

}


###
## BoardHeader - �Ǽ��ĥإå���ɽ��
#
# - SYNOPSIS
#	BoardHeader;
#
# - ARGS
#	�ʤ�
#
# - DESCRIPTION
#	�Ǽ��ĤΥإå���ɽ�����롥
#
# - RETURN
#	�ʤ�
#
sub BoardHeader {

    local($File) = &GetPath($BOARD, $BOARD_FILE_NAME);

    open(HEADER, "<$File") || &Fatal(1, $File);
    while(<HEADER>){
	# Version Check
	&VersionCheck('Header', $1), next if (m/^<!-- Kb-System-Id: ([^\/]*\/.*) -->$/o);
	# ɽ������
	&cgiprint'Cache("$_");
    }
    close(HEADER);

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
	&cgiprint'Cache("<br>\n<strong>$H_ORIG_TOP:</strong> " . &GetFormattedTitle($Id, $Aids, $Icon, $Subject, $Name, $Date));
    }

    # ������
    $Id = $IdList[0];
    ($Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name) = &GetArticlesInfo($Id);
    &cgiprint'Cache("<br>\n<strong>$H_ORIG:</strong> " . &GetFormattedTitle($Id, $Aids, $Icon, $Subject, $Name, $Date));

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


######################################################################
# ���ץꥱ��������ǥ륤��ץ���ơ������


###
## MakeNewArticle - ��������Ƥ��줿����������
#
# - SYNOPSIS
#	MakeNewArticle($Id, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail);
#
# - ARGS
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
    local($Id, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail) = @_;
    local($ArticleId);

    # ���Ϥ��줿��������Υ����å�
    $Article = &CheckArticle($TextType, *Name, *Email, *Url, *Subject, *Icon, $Article);

    # �����������ֹ�����(�ޤ������ֹ�������Ƥʤ�)
    $ArticleId = &GetNewArticleId;

    # �����Υե�����κ���
    &MakeArticleFile($TextType, $Article, $ArticleId);

    # �����������ֹ��񤭹���
    &WriteArticleId($ArticleId);

    # DB�ե��������Ƥ��줿�������ɲ�
    # �̾�ε������Ѥʤ�ID
    &AddDBFile($ArticleId, $Id, $TIME, $Subject, $Icon, $REMOTE_HOST, $Name, $Email, $Url, $Fmail);

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
    local($ExtensionHeader, $QuoteFile);

    # �ղåإå�������
    $ExtensionHeader = "X-Kb-System: $SYSTEM_NAME\n";
    if ($BOARDNAME && ($Id ne '')) {
	$ExtensionHeader .= "X-Kb-Board: $BOARDNAME\nX-Kb-Articleid: $Id\n";
    }

    # ���ѵ���
    if ($Id ne '') {

	# ���Ѥ���ե�����
	$QuoteFile = &GetArticleFileName($Id, $BOARD);

	# ���ڤ���
	$Message .= "\n--------------------\n";

	# ����
	open(TMP, "<$QuoteFile") || &Fatal(1, $QuoteFile);
	while(<TMP>) {

	    # Version Check
	    &VersionCheck('Article', $1), next if (m/^<!-- Kb-System-Id: ([^\/]*\/.*) -->$/o);

	    # �������פ�ʤ�
	    s/<[^>]*>//go;
	    if ($_ ne '') {
		$Message .= &HTMLDecode($_);
	    }

	}
	close(TMP);

    }

    # ��������
    &Fatal(9, '') unless (&cgi'SendMail($MAINT_NAME, $MAINT, $Subject, $ExtensionHeader, $Message, @To));

}


###
## SearchArticleKeyword - �����θ���(��ʸ)
#
# - SYNOPSIS
#	SearchArticleKeyword($Id, @KeyList);
#
# - ARGS
#	$Id		��ʸ�򸡺����뵭����ID
#	@KeyList	������ɥꥹ��
#
# - DESCRIPTION
#	���ꤵ�줿��������ʸ�򡤥�����ɤ�AND�������롥
#
# - RETURN
#	�ǽ�˥�����ɤȥޥå������ԡ��ޥå����ʤ��ä�������֤���
#
sub SearchArticleKeyword {
    local($Id, @KeyList) = @_;
    local(@NewKeyList, $Line, $Return, $Code, $File, $ConvFlag);

    $ConvFlag = ($Id !~ /^\d+$/);

    $File = &GetArticleFileName($Id, $BOARD);
    open(ARTICLE, "<$File") || &Fatal(1, $File);
    while($Line = <ARTICLE>) {

	# Version Check
	&VersionCheck('Article', $1), next if (m/^<!-- Kb-System-Id: ([^\/]*\/.*) -->$/o);

	# �������Ѵ�
	if ($ConvFlag) {
	    $Code = &jcode'getcode(*Line);
	    &jcode'convert(*Line, 'euc', $Code, 'z');
	}

	# ���ꥢ
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
    close(ARTICLE);

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
#	CheckArticle($TextType, *Name, *Email, *Url, *Subject, *Icon, $Article);
#
# - ARGS
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
    local($TextType, *Name, *Email, *Url, *Subject, *Icon, $Article) = @_;
    local($Tmp);

    # �����ꥢ�������å�
    $_ = $Name;
    if (/^\#.*$/o) {
        ($Tmp, $Email, $Url) = &GetUserInfo($_);
	if ($Tmp eq '') {
	    &Fatal(6, $Name);
	}
	$Name = $Tmp;
    }

    # ʸ��������å�
    &CheckName(*Name);
    &CheckEmail(*Email);
    &CheckURL(*Url);
    &CheckSubject(*Subject);

    # �������å�
    (! $Article) && &Fatal(2, '');

    # ��������Υ����å�; ������������̵���פ����ꡥ
    $Icon = $H_NOICON unless (&GetIconURLFromTitle($Icon));

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
    (! $String) && &Fatal(2, '');

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
    (! $String) && &Fatal(2, '');

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
    (! $String) && &Fatal(2, '');

    # ���ԥ����ɤ�����å�
    ($String =~ /[\t\n]/o) && &Fatal(3, '');

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
    ($String =~ /[\t\n]/o) && &Fatal(3, '');

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
    ($String ne '') && (! &IsUrl($String)) && &Fatal(7, 'URL');

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
#	GetFormattedTitle($Id, $Aids, $Icon, $Title, $Name, $Date);
#
# - ARGS
#	$Id		����ID
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
    local($Id, $Aids, $Icon, $Title, $Name, $Date) = @_;
    local($String, $InputDate, $IdStr, $Link, $Thread);

    $InputDate = &GetDateTimeFormatFromUtc(($Date || &GetModifiedTime($Id)));
    # �����ȥ뤬�Ĥ��Ƥʤ��ä��顤Id�򤽤Τޤޥ����ȥ�ˤ��롥
    $Title = $Title || $Id;

    # �̾ﵭ��
    $IdStr = "<strong>$Id.</strong> ";

    if ($SYS_F_E) {
	$Link = "<a href=\"$PROGRAM?b=$BOARD&c=e&id=$Id\">$Title</a>";
    } else {
	$Link = "$Title";
    }

    $Thread = (($SYS_F_T && $Aids) ? " <a href=\"$PROGRAM?b=$BOARD&c=t&id=$Id\">$H_THREAD</a>" : '');

    if (($Icon eq $H_NOICON) || ($Icon eq '')) {
	$String = sprintf("$IdStr$Link$Thread [%s] $InputDate", ($Name || $MAINT_NAME));
    } else {
	$String = sprintf("$IdStr<img src=\"%s\" alt=\"$Icon \" width=\"$MSGICON_WIDTH\" height=\"$MSGICON_HEIGHT\">$Link$Thread [%s] $InputDate", &GetIconURLFromTitle($Icon), ($Name || $MAINT_NAME));
    }

    return($String);

}


###
## GetModifiedTime - ���뵭���κǽ���������(UTC)�����
#
# - SYNOPSIS
#	GetModifiedTime($Id);
#
# - ARGS
#	$Id	����ID
#
# - DESCRIPTION
#	����ID�ε������顤�ǽ�����UTC���äƤ��롥
#
# - RETURN
#	���ε����ե�����κǽ���������(UTC)
#
sub GetModifiedTime {
    local($Id) = @_;

    return($TIME - (-M &GetArticleFileName($Id, $BOARD)) * 86400);
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


######################################################################
# �ǡ�������ץ���ơ������


###
## DbCash - ����DB�����ɤ߹���
#
# - SYNOPSIS
#	DbCash;
#
# - ARGS
#	�ʤ�
#
# - DESCRIPTION
#	��˵�ư���˸ƤӽФ��졤����DB�����Ƥ�����ѿ��˥���å��夹�롥
#
# - RETURN
#	�ʤ�
#
sub DbCash {

    local($DBFile, $dId, $dFid, $dAids, $dDate, $dTitle, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail, $Count);

    # ���ꥢ
    @DB_ID = %DB_FID = %DB_AIDS = %DB_DATE = %DB_TITLE = %DB_ICON = %DB_REMOTEHOST = %DB_NAME = %DB_EMAIL = %DB_URL = %DB_FMAIL = ();

    $DBFile = &GetPath($BOARD, $DB_FILE_NAME);

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
	$DB_DATE{$dId} = $dDate || &GetModifiedTime($dId);
	$DB_TITLE{$dId} = $dTitle || $dId;
	$DB_ICON{$dId} = $dIcon;
	$DB_REMOTEHOST{$dId} = $dRemoteHost;
	$DB_NAME{$dId} = $dName || $MAINT_NAME;
	$DB_EMAIL{$dId} = $dEmail;
	$DB_URL{$dId} = $dUrl;
	$DB_FMAIL{$dId} = $dFmail;

    }
    close(DB);

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
#	�����������Ф���
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
#	AddDBFile($Id, $Fid, $InputDate, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail);
#
# - ARGS
#	$Id		����ID
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
    local($Id, $Fid, $InputDate, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail) = @_;
    local($dId, $dFid, $dAids, $dInputDate, $dSubject, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail, $mdName, $mdInputDate, $mdSubject, $mdId, $mName, $mSubject, $mId, $FidList, $FFid, $File, $TmpFile, @FollowMailTo, @FFid);

    # ��ץ饤���Υ�ץ饤�������äƤ���
    if ($Fid ne '') {
	($FFid) = &GetArticlesInfo($Fid);
	@FFid = split(/,/, $FFid);
    }

    $FidList = $Fid;

    $File = &GetPath($BOARD, $DB_FILE_NAME);
    $TmpFile = &GetPath($BOARD, $DB_TMP_FILE_NAME);
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
    if (@ARRIVE_MAIL = &GetArriveMailTo) {
	&ArriveMail($Name, $Subject, $Id, @ARRIVE_MAIL);
    }

    # ɬ�פʤ�ȿ�������ä����Ȥ�ᥤ�뤹��
    if (@FollowMailTo) {
	&FollowMail($mdName, $mdInputDate, $mdSubject, $mdId, $mName, $mSubject, $mId, @FollowMailTo);
    }

}


###
## MakeArticleFile - ������ʸDB�ؤ��ɲ�
#
# - SYNOPSIS
#	MakeArticleFile($TextType, $Article, $Id);
#
# - ARGS
#	$TextType	ʸ�񥿥���
#	$Article	��ʸ
#	$Id		����ID
#
# - DESCRIPTION
#	������ʸDB(�Ǽ���ID��Ʊ��̾���Υǥ��쥯�ȥ�)����ˡ�
#	ID��Ʊ��̾���Υե�����Ȥ��ơ�������ʸ����¸���롥
#
# - RETURN
#	�ʤ�
#
sub MakeArticleFile {
    local($TextType, $Article, $Id) = @_;
    local($File) = &GetArticleFileName($Id, $BOARD);

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
    $Article = &ArticleEncode($TextType, $Article);
    print(TMP "$Article\n");

    # TextType�Ѹ����
    if ((! $SYS_TEXTTYPE) || ($TextType eq $H_PRE)) {
	print(TMP "</pre></p>\n");
    }

    # ��λ
    close(TMP);

}


###
## GetNewArticleId - �����ֹ�DB���ɤ߹���
#
# - SYNOPSIS
#	GetNewArticleId;
#
# - ARGS
#	�ʤ�
#
# - DESCRIPTION
#	����κǿ�����ID��1���䤷���������������ֹ���֤���
#	���ץꥱ��������ǥ�ȥǡ�����ǥ뤬ʬΥ����Ƥʤ���
#
# - RETURN
#	����������ID
#
sub GetNewArticleId {

    local($ArticleNumFile, $ArticleId);

    $ArticleNumFile = &GetPath($BOARD, $ARTICLE_NUM_FILE_NAME);
    open(AID, "<$ArticleNumFile") || &Fatal(1, $ArticleNumFile);
    while(<AID>) {
	chop;
	$ArticleId = $_;
    }
    close(AID);

    # 1���䤷���֤�
    return($ArticleId + 1);

}


###
## WriteArticleId - �����ֹ�DB�ι���
#
# - SYNOPSIS
#	WriteArticleId($Id);
#
# - ARGS
#	$Id	�����˽񤭹��൭���ֹ�
#
# - DESCRIPTION
#	�����ֹ�DB�ι���
#
# - RETURN
#	�ʤ�
#
sub WriteArticleId {
    local($Id) = @_;
    local($File, $TmpFile, $OldArticleId);
    
    # �����Τ����˸Ť����ͤ��㤤! (��������ʤ���OK)
    $OldArticleId = &GetNewArticleId;
    if (($Id =~ /^\d+$/) && ($Id < $OldArticleId)) {
	&Fatal(10, '');
    }

    $File = &GetPath($BOARD, $ARTICLE_NUM_FILE_NAME);
    $TmpFile = &GetPath($BOARD, $ARTICLE_NUM_TMP_FILE_NAME);
    open(AID, ">$TmpFile") || &Fatal(1, $TmpFile);
    print(AID "$Id\n");
    close(AID);

    # ����
    rename($TmpFile, $File);

}


###
## GetArriveMailTo - �Ǽ����̿����ᥤ��������DB�����ɤ߹���
#
# - SYNOPSIS
#	GetArriveMailTo;
#
# - ARGS
#	�ʤ�
#
# - DESCRIPTION
#	�Ǽ����̿����ᥤ��������DB���ɤ߹��ࡥ
#
# - RETURN
#	����E-Mail�Υꥹ��
#
sub GetArriveMailTo {

    local($ArriveMailFile, @To);

    $ArriveMailFile = &GetPath($BOARD, $ARRIVEMAIL_FILE_NAME);
    # �ե����뤬�ʤ�������ʤ���
    open(ARMAIL, "<$ArriveMailFile") || return();
    while(<ARMAIL>) {

    	# Version Check
	&VersionCheck('ARRIVEMAIL', $1), next if (m/^\# Kb-System-Id: ([^\/]*\/.*)$/o);
	next if (/^\#/o || /^$/o);
	chop;

	push(@To, $_);

    }
    close(ARMAIL);

    @To;
}


###
## CashAliasData - �桼��DB�����ɤ߹���
#
# - SYNOPSIS
#	CashAliasData($File);
#
# - ARGS
#	$File		�桼��DB
#
# - DESCRIPTION
#	�桼�������ꥢ���ե�������ɤ߹����Ϣ�������������ࡥ
#	����ѿ���%Name, %Email, %Host, %URL���˲����롥
#
# - RETURN
#	�ʤ�
#
sub CashAliasData {
    local($File) = @_;
    local($A, $N, $E, $H, $U);

    # ������ࡥ
    open(ALIAS, "<$File") || &Fatal(1, $File);
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
#	WriteAliasData($File);
#
# - ARGS
#	$File		�桼��DB
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
    local($File) = @_;
    local($Alias, $TmpFile);

    $TmpFile = $USER_ALIAS_TMP_FILE;
    open(ALIAS, ">$TmpFile") || &Fatal(1, $TmpFile);

    # �С����������񤭽Ф�
    printf(ALIAS "<!-- Kb-System-Id: %s/%s -->\n", $KB_VERSION, $KB_RELEASE);

    # ��ˡ�
    foreach $Alias (sort keys(%Name)) {
	($Name{$Alias}) && printf(ALIAS "%s\t%s\t%s\t%s\t%s\n", $Alias, $Name{$Alias}, $Email{$Alias}, $Host{$Alias}, $URL{$Alias});
    }
    close(ALIAS);

    # ����
    rename($TmpFile, $File);
    
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
    local($BoardName);

    open(ALIAS, "<$BOARD_ALIAS_FILE") || &Fatal(1, $BOARD_ALIAS_FILE);
    while(<ALIAS>) {

	# Version Check
	&VersionCheck('Board', $1), next if (m/^\# Kb-System-Id: ([^\/]*\/.*)$/o);
	next if (/^\#/o || /^$/o);
	chop;
	next unless (/^$Alias\t(.*)$/);
	$BoardName = $1;
    }
    close(ALIAS);

    return($BoardName);

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
#	GetIconURLFromTitle($Icon);
#
# - ARGS
#	$Icon		��������ID
#
# - DESCRIPTION
#	��������ID���顤���Υ���������б�����gif�ե������URL�������
#
# - RETURN
#	URL��ɽ��ʸ����
#
sub GetIconURLFromTitle {
    local($Icon) = @_;
    local($FileName, $Title, $TargetFile);

    # ��İ��ɽ��
    open(ICON, &GetIconPath("$BOARD.$ICONDEF_POSTFIX"))
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
