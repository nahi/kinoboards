#!/usr/local/bin/perl5
#
# $Id: kb.cgi,v 4.38 1997-02-14 11:41:00 nakahiro Exp $


# KINOBOARDS: Kinoboards Is Network Opened BOARD System
# Copyright (C) 1995, 96 NAKAMURA Hiroshi.
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


###
## �Ķ��ѿ��򽦤�
#
$SERVER_NAME = $ENV{'SERVER_NAME'};
$SERVER_PORT = $ENV{'SERVER_PORT'};
$SCRIPT_NAME = $ENV{'SCRIPT_NAME'};
$REMOTE_HOST = $ENV{'REMOTE_HOST'};
$PATH_INFO = $ENV{'PATH_INFO'};
$PATH_TRANSLATED = $ENV{'PATH_TRANSLATED'};
($CGIPROG_NAME = $SCRIPT_NAME) =~ s!^(.*/)!!o;
$SYSDIR_NAME = (($PATH_INFO) ? "$PATH_INFO/" : "$1");
$SCRIPT_URL = "http://$SERVER_NAME:$SERVER_PORT$SCRIPT_NAME$PATH_INFO";
$PROGRAM = (($PATH_INFO) ? "$SCRIPT_NAME$PATH_INFO" : $CGIPROG_NAME);


###
## ���󥯥롼�ɥե�������ɤ߹���
#
chdir($PATH_TRANSLATED) if ($PATH_TRANSLATED ne '');
require('kb.ph');
require('cgi.pl');
require('tag_secure.pl');
require('jcode.pl');


###
## ����ѿ������
#

#
# �����default
#
$[ = 0;
$| = 1;

#
# Version��Release�ֹ�
#
$KB_VERSION = '1.0';
$KB_RELEASE = '3.3pre';

#
# ���ɽ��
#
$ADDRESS = sprintf("Maintenance: <a href=\"mailto:%s\">%s</a><br>
<a href=\"http://www.kinotrope.co.jp/~nakahiro/kb10.shtml\">KINOBOARDS/%s R%s</a>: Copyright (C) 1995, 96, 97 <a href=\"http://www.kinotrope.co.jp/~nakahiro/\">NAKAMURA Hiroshi</a>.", $MAINT, $MAINT_NAME, $KB_VERSION, $KB_RELEASE);

#
# �ե�����
#
# �����ֹ�ե�����
$ARTICLE_NUM_FILE_NAME = '.articleid';
# �����ֹ�ƥ�ݥ��ե�����
$ARTICLE_NUM_TMP_FILE_NAME = '.articleid.tmp';
# �Ǽ�����configuratin�ե�����
$CONF_FILE_NAME = '.kbconf';
# �����ȥ�ꥹ�ȥإå��ե�����
$BOARD_FILE_NAME = '.board';
# DB�ե�����
$DB_FILE_NAME = '.db';
# DB�ƥ�ݥ��ե�����
$DB_TMP_FILE_NAME = '.db.tmp';
# �桼�������ꥢ���ե�����
$USER_ALIAS_FILE = 'kinousers';
# �桼�������ꥢ���ƥ�ݥ��ե�����
$USER_ALIAS_TMP_FILE = 'kinousers.tmp';
# �ܡ��ɥ����ꥢ���ե�����
$BOARD_ALIAS_FILE = 'kinoboards';
# �ǥե���ȤΥ�����������ե�����
$DEFAULT_ICONDEF = 'all.idef';
# ��å��ե�����
$LOCK_FILE = '.lock.kb';
# ��å����ե�����
$LOCK_ORG = '.lock.kb.org';
# ��å����Υ�ȥ饤���
$LOCK_WAIT = 10;

#
# ��������ǥ��쥯�ȥ�
# (��������ȥ�����������ե�����������ǥ��쥯�ȥ�̾)
#
$ICON_DIR = 'icons';

# ��������ե�����
$ICON_TLIST = &GetIconURL('tlist.gif');
$ICON_NEXT = &GetIconURL('next.gif');
$ICON_WRITENEW = &GetIconURL('writenew.gif');
$ICON_FOLLOW = &GetIconURL('follow.gif');
$ICON_QUOTE = &GetIconURL('quote.gif');
$ICON_THREAD = &GetIconURL('thread.gif');
$ICON_HELP = &GetIconURL('q.gif');

#
# ������������ե�����Υݥ��ȥե�����
# ������������ե����롤��(�ܡ��ɥǥ��쥯�ȥ�̾).(���ꤷ��ʸ����)�פˤʤ롥
$ICONDEF_POSTFIX = 'idef';
$ICON_HEIGHT = 20;
$ICON_WIDTH = 20;

#
# ���������ץ�����
#
$NULL_LINE = '__br__';
$DOUBLE_QUOTE = '__dq__';
$GREATER_THAN = '__gt__';
$LESSER_THAN = '__lt__';
$AND_MARK = '__amp__';

#
# �ե饰
#
$F_FALSE = 0;
$F_TRUE = 1;

#
# ���顼������
#
$ERR_FILE = 1;
$ERR_NOTFILLED = 2;
$ERR_CRINDATA = 3;
$ERR_TAGCRINDATA = 4;
$ERR_CANNOTGRANT = 5;
$ERR_UNKNOWNALIAS = 6;
$ERR_ILLEGALSTRING = 7;
$ERR_NONEXTARTICLE = 8;
$ERR_CANNOTSENDMAIL = 9;
$ERR_F_CANNOTLOCK = 999;

#
# 1��
#
$SECINDAY = 24 * 60 * 60;
$TIME = time;
$PROGTIME = ($TIME - (-M "$CGIPROG_NAME") * $SECINDAY);

# �ȥ�å�
$SIG{'HUP'} = $SIG{'INT'} = $SIG{'QUIT'} = $SIG{'TERM'} = $SIG{'TSTP'} = 'DoKill';
sub DoKill {
    &unlock;
    exit(1);
}


###
## �ᥤ��
#

&lock;

MAIN: {

    # ɸ������(POST)�ޤ��ϴĶ��ѿ�(GET)�Υǥ����ɡ�
    &cgi'decode;

    # ���ˤ˻Ȥ��Τ�����ѿ�
    $BOARD = $cgi'TAGS{'b'};
    $BOARDNAME = &GetBoardInfo($BOARD);

    # �Ǽ��ĸ�ͭ���åƥ��󥰤��ɤ߹���
    local($BoardConfFile) = &GetPath($BOARD, $CONF_FILE_NAME);
    require("$BoardConfFile") if (-s "$BoardConfFile");

    # DB������ѿ��˥���å���
    &DbCash if $BOARD;

    # �ͤ����
    local($Command) = $cgi'TAGS{'c'};
    local($Com) = $cgi'TAGS{'com'};
    local($Id) = $cgi'TAGS{'id'};

    # ���ޥ�ɥ����פˤ��ʬ��
    &ShowArticle($Id),		last if ($Command eq 'e');
    &NextArticle($Id),		last if ($Command eq 'en');
    &ThreadArticle($Id),	last if ($Command eq 't');
    &Entry('', ''),		last if ($Command eq 'n');
    &Entry('', $Id),		last if ($Command eq 'f');
    &Entry('quote', $Id),	last if ($Command eq 'q');
    &Preview,			last if (($Command eq 'p') && ($Com ne 'x'));
    &Thanks,			last if ($Command eq 'x');
    &Thanks,			last if (($Command eq 'p') && ($Com eq 'x'));
    &ViewTitle,			last if ($Command eq 'v');
    &SortArticle,		last if ($Command eq 'r');
    &NewArticle,		last if ($Command eq 'l');
    &SearchArticle,		last if ($Command eq 's');
    &ShowIcon,			last if ($Command eq 'i');
    &AliasNew,			last if ($Command eq 'an');
    &AliasMod,			last if ($Command eq 'am');
    &AliasDel,			last if ($Command eq 'ad');
    &AliasShow,			last if ($Command eq 'as');

    print("huh... what's up? running under any shell?\n");

}


###
## �����ޤ�
#
&unlock;
exit(0);


###
## DB�Υ���å���
#
sub DbCash {

    # ��ư��������DB�����Ƥ�����ѿ��˥���å��夹�롥
    @DB_ID = ();
    %DB_FID = ();
    %DB_AIDS = ();
    %DB_DATE = ();
    %DB_TITLE = ();
    %DB_ICON = ();
    %DB_REMOTEHOST = ();
    %DB_NAME = ();
    %DB_EMAIN = ();
    %DB_URL = ();
    %DB_FMAIL = ();

    local($DBFile) = &GetPath($BOARD, $DB_FILE_NAME);

    local($dId, $dFid, $dAids, $dDate, $dTitle, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail);
    local($Count) = 0;

    # �����ߡ�
    open(DB, "<$DBFile") || &Fatal($ERR_FILE, $DBFile);
    while(<DB>) {

	# Version Check
	&VersionCheck('DB', $1), next if (m/^\# Kb-System-Id: ([^\/]*\/.*)$/o);

	next if (/^\#/o);
	next if (/^$/o);
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
## �񤭹��߲���
#
sub Entry {

    # ���Ѥ���/�ʤ��ȡ����Ѥ�����Ϥ���Id(���Ѥ��ʤ����϶�)
    local($QuoteFlag, $Id) = @_;

    # ɽ�����̤κ���
    &MsgHeader('Message entry', "$BOARDNAME: $ENTRY_MSG", $PROGTIME);

    # �ե����ξ��
    if ($Id ne '') {
	# ������ɽ��(���ޥ��̵��, ����������)
	&ViewOriginalArticle($Id, $F_FALSE, $F_TRUE);
	print("<hr>\n");
	&cgi'KPrint("<h2>$H_REPLYMSG</h2>");
    }

    # �إå���ʬ��ɽ��
    &EntryHeader((($Id eq '') ? '' : &GetReplySubject($Id)), $Id);

    # ��ʸ(���Ѥ���ʤ鸵����������)
    print("<p><textarea name=\"article\" rows=\"$TEXT_ROWS\" cols=\"$TEXT_COLS\">");
    &QuoteOriginalArticle($Id, $BOARD) if (($Id ne '') && ($QuoteFlag eq 'quote'));
    print("</textarea></p>\n");

    # �եå���ʬ��ɽ��
    &EntryFooter;

}


###
## �񤭹��߲��̤Τ�����������ʸ��TextType��Board̾��ɽ����
#
sub EntryHeader {

    local($Subject, $Id) = @_;

    # ����«
    &cgi'KPrint(<<__EOF__);
<form action="$PROGRAM" method="POST">
<input name="c" type="hidden" value="p">
<input name="b" type="hidden" value="$BOARD">
<input name="id" type="hidden" value="$Id">
<p>
$H_AORI_1
__EOF__
    &cgi'KPrint("$H_AORI_2\n") if ($SYS_TEXTTYPE);
    &cgi'KPrint(<<__EOF__);
</p>
<p>
$H_BOARD: $BOARDNAME<br>
__EOF__

    # �������������
    if ($SYS_ICON) {
	&cgi'KPrint(<<__EOF__);
$H_ICON:
<SELECT NAME="icon">
<OPTION SELECTED>$H_NOICON
__EOF__

	# ��İ��ɽ��
	open(ICON, &GetIconPath("$BOARD.$ICONDEF_POSTFIX"))
	    || (open(ICON, &GetIconPath("$DEFAULT_ICONDEF"))
		|| &Fatal($ERR_FILE, &GetIconPath("$DEFAULT_ICONDEF")));
	while(<ICON>) {

	    # Version Check
	    &VersionCheck('Icon', $1), next if (m/^\# Kb-System-Id: ([^\/]*\/.*)$/o);

	    # ������ʸ�ϥ���󥻥�
	    next if (/^\#/o);
	    next if (/^$/o);

	    # ɽ��
	    chop;
	    ($FileName, $Title) = split(/\t/, $_, 3);
	    &cgi'KPrint("<OPTION>$Title\n");

	}
	close(ICON);
	print("</SELECT>\n");
	&cgi'KPrint("(<a href=\"$PROGRAM?b=$BOARD&c=i&type=entry\">$H_SEEICON</a>)<BR>\n");
    }

    # Subject(�ե����ʤ鼫ưŪ��ʸ����������)
    &cgi'KPrint(sprintf("%s: <input name=\"subject\" type=\"text\" value=\"%s\" size=\"%s\"><br>\n", $H_SUBJECT, $Subject, $SUBJECT_LENGTH));

    # TextType
    if ($SYS_TEXTTYPE) {
	&cgi'KPrint(<<__EOF__);
$H_TEXTTYPE:
<SELECT NAME="texttype">
<OPTION SELECTED>$H_PRE
<OPTION>$H_HTML
</SELECT>
</p>
__EOF__

    }

}


###
## �եå���ʬ��ɽ��
#
sub EntryFooter {

    # ̾���ȥᥤ�륢�ɥ쥹��URL��
    &cgi'KPrint(<<__EOF__);
<p>
$H_LINK
</p><p>
$H_FROM: <input name="name" type="text" size="$NAME_LENGTH"><br>
$H_MAIL: <input name="mail" type="text" size="$MAIL_LENGTH"><br>
$H_URL_S: <input name="url" type="text" value="http://" size="$URL_LENGTH"><br>
__EOF__

    ($SYS_FOLLOWMAIL) && &cgi'KPrint("$H_FMAIL <input name=\"fmail\" type=\"checkbox\" value=\"on\"><br>\n");
    
    if ($SYS_ALIAS) {
	&cgi'KPrint(<<__EOF__);
</p><p>
$H_ALIASINFO
(<a href="$PROGRAM?c=as">$H_SEEALIAS</a> //
 <a href="$PROGRAM?c=an">$H_ALIASENTRY</a>)
__EOF__

    }

    # �ܥ���
    &cgi'KPrint(<<__EOF__);
</p><p>
<input type="radio" name="com" value="p" CHECKED>: $H_PREVIEW<br>
<input type="radio" name="com" value="x">: $H_ENTRY<br>
<input type="submit" value="$H_PUSHHERE_POST">
</p>
</form>
__EOF__

    &MsgFooter;
}


###
## ����Id�ε�������Subject���äƤ��ơ���Ƭ�ˡ�Re:�פ�1�Ĥ����Ĥ����֤���
#
sub GetReplySubject {

    # Id��Board
    local($Id) = @_;

    # ��������
    local($dFid, $dAids, $dDate, $dSubject) = &GetArticlesInfo($Id);

    # ��Ƭ�ˡ�Re:�פ����äĤ��Ƥ����������
    $dSubject =~ s/^Re:\s*//oi;

    # ��Ƭ�ˡ�Re: �פ򤯤äĤ����֤���
    return("Re: $dSubject");

}


###
## ���Ѥ���
#
sub QuoteOriginalArticle {

    # Id��Board
    local($Id, $Board) = @_;

    # ���Ѥ���ե�����
    local($QuoteFile) = &GetArticleFileName($Id, $Board);

    # ����������μ���
    local($Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name) = &GetArticlesInfo($Id);

    # �ե�����򳫤�
    open(TMP, "<$QuoteFile") || &Fatal($ERR_FILE, $QuoteFile);
    while(<TMP>) {

	# Version Check
	&VersionCheck('Article', $1), next if (m/^<!-- Kb-System-Id: ([^\/]*\/.*) -->$/o);

	# ���ѤΤ�����Ѵ�
	s/\&//go;
	s/\"//go;
	s/<[^>]*>//go;

	# ����ʸ�����ɽ��
	&cgi'KPrint(sprintf("%s%s%s", $Name, $DEFAULT_QMARK, $_));
	
    }

    # �Ĥ���
    close(TMP);

}


###
## �ץ�ӥ塼����
#
sub Preview {

    # ���Ϥ��줿��������
    local($Id) = $cgi'TAGS{'id'};
    local($TextType) = $cgi'TAGS{'texttype'};
    local($Name) = $cgi'TAGS{'name'};
    local($Email) = $cgi'TAGS{'mail'};
    local($Url) = $cgi'TAGS{'url'};
    local($Icon) = $cgi'TAGS{'icon'};
    local($Subject) = $cgi'TAGS{'subject'};
    local($Article) = $cgi'TAGS{'article'};
    local($Qurl) = $cgi'TAGS{'qurl'};
    local($Fmail) = $cgi'TAGS{'fmail'};

    # ���ѵ����ε�������
    local($rFid) = &GetArticlesInfo($Id) if ($Id ne '');

    # ���Ϥ��줿��������Υ����å�
    $Article = &CheckArticle($TextType, *Name, *Email, *Url, *Subject, *Icon, $Article);

    # ��ǧ���̤κ���
    &MsgHeader('Message preview', $PREVIEW_MSG, $TIME);

    # ����«
    &cgi'KPrint(<<__EOF__);
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
<input name="qurl"     type="hidden" value="$Qurl">
<input name="fmail"    type="hidden" value="$Fmail">

<p>
$H_POSTINFO
<input type="submit" value="$H_PUSHHERE_PREVIEW">
</p><p>
__EOF__

    # ��
    (($Icon eq $H_NOICON) || (! $Icon))
        ? &cgi'KPrint("<strong>$H_SUBJECT</strong>: $Subject")
            : &cgi'KPrint(sprintf("<strong>$H_SUBJECT</strong>: <img src=\"%s\" alt=\"$Icon \" width=\"$ICON_WIDTH\" height=\"$ICON_HEIGHT\">$Subject", &GetIconURLFromTitle($Icon)));

    # ��̾��
    if ($Url ne '') {
        # URL��������
        &cgi'KPrint("<br>\n<strong>$H_FROM</strong>: <a href=\"$Url\">$Name</a>");
    } else {
        # URL���ʤ����
        &cgi'KPrint("<br>\n<strong>$H_FROM</strong>: $Name");
    }

    # �ᥤ��
    &cgi'KPrint(" <a href=\"mailto:$Email\">&lt;$Email&gt;</a>") if ($Email ne '');

    # ȿ����(���Ѥξ��)
    if (defined($rFid)) {
	if ($rFid ne '') {
	    &ShowLinksToFollowedArticle(($Id, split(/,/, $rFid)));
	} else {
	    &ShowLinksToFollowedArticle($Id);
	}
    }

    # �ڤ���
    &cgi'KPrint("</p>\n$H_LINE<br>\n");

    # TextType��������
    print("<p><pre>") if ((! $SYS_TEXTTYPE) || ($TextType eq $H_PRE));

    # ����
    $Article = &DQDecode($Article);
    $Article = &ArticleEncode($TextType, $Article);
    &cgi'KPrint("$Article\n");

    # TextType�Ѹ����
    print("</pre></p>\n") if ((! $SYS_TEXTTYPE) || ($TextType eq $H_PRE));

    # ����«
    print("</form>\n");

    &MsgFooter;
}


###
## ��Ͽ�����
#
sub Thanks {

    # �����˵�������������
    local($Id) = &MakeNewArticle;

    # ɽ�����̤κ���
    &MsgHeader('Message entried', $THANKS_MSG, $TIME);

    &cgi'KPrint(<<__EOF__);
<p>
$H_THANKSMSG
</p>
<form action="$PROGRAM" method="POST">
<input name="b" type="hidden" value="$BOARD">
<input name="c" type="hidden" value="v">
<input name="num" type="hidden" value="$DEF_TITLE_NUM">
<input type="submit" value="$H_BACKTITLE">
</form>
__EOF__

    if ($Id ne '') {
	&cgi'KPrint(<<__EOF__);
<form action="$PROGRAM" method="POST">
<input name="b" type="hidden" value="$BOARD">
<input name="c" type="hidden" value="e">
<input name="id" type="hidden" value="$Id">
<input type="submit" value="$H_BACKORG">
</form>
__EOF__
    }

    &MsgFooter;

}


###
## ��������Ƥ��줿����������
#
sub MakeNewArticle {

    # ���Ϥ��줿��������
    local($Id) = $cgi'TAGS{'id'};
    local($TextType) = $cgi'TAGS{'texttype'};
    local($Name) = $cgi'TAGS{'name'};
    local($Email) = $cgi'TAGS{'mail'};
    local($Url) = $cgi'TAGS{'url'};
    local($Icon) = $cgi'TAGS{'icon'};
    local($Subject) = $cgi'TAGS{'subject'};
    local($Article) = $cgi'TAGS{'article'};
    local($Qurl) = $cgi'TAGS{'qurl'};
    local($Fmail) = $cgi'TAGS{'fmail'};

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

    # �������ؤΥ�󥯤Τ����
    return($Id);

}


###
## ���Ϥ��줿��������Υ����å�
#
sub CheckArticle {

    # �������󤤤���
    local($TextType, *Name, *Email, *Url, *Subject, *Icon, $Article) = @_;
    local($Tmp) = '';

    # �����ꥢ�������å�
    $_ = $Name;
    if (/^\#.*$/o) {
        ($Tmp, $Email, $Url) = &GetUserInfo($_);
	&Fatal($ERR_UNKNOWNALIAS, $Name) if ($Tmp eq '');
	$Name = $Tmp;
    }

    # ʸ��������å�
    &CheckName(*Name);
    &CheckEmail(*Email);
    &CheckURL(*Url);
    &CheckSubject(*Subject);

    # �������å�
    (! $Article) && &Fatal($ERR_NOTFILLED, '');

    # ��������Υ����å�; ������������̵���פ����ꡥ
    $Icon = $H_NOICON unless (&GetIconURLFromTitle($Icon));

    # �������"�򥨥󥳡���
    $Article = &DQEncode($Article);

    return($Article);

}


###
## ������񤭽Ф���
#
sub MakeArticleFile {

    # TextType�ȵ������Τ�Ρ�Id
    local($TextType, $Article, $Id) = @_;

    # �ե�����̾�����
    local($File) = &GetArticleFileName($Id, $BOARD);

    # �ե�����򳫤�
    open(TMP, ">$File") || &Fatal($ERR_FILE, $File);

    # �С����������񤭽Ф�
    printf(TMP "<!-- Kb-System-Id: %s/%s -->\n", $KB_VERSION, $KB_RELEASE);

    # TextType��������
    print(TMP "<p><pre>") if ((! $SYS_TEXTTYPE) || ($TextType eq $H_PRE));

    # ����; "��ǥ����ɤ����������ƥ������å�
    $Article = &DQDecode($Article);
    $Article = &ArticleEncode($TextType, $Article);
    print(TMP "$Article\n");

    # TextType�Ѹ����
    print(TMP "</pre></p>\n") if ((! $SYS_TEXTTYPE) || ($TextType eq $H_PRE));

    # ��λ
    close(TMP);

}


###
## �ü�ʸ����encode and decode
#
sub DQEncode {
    local($Str) = @_;
    $Str =~ s/\"/$DOUBLE_QUOTE/go;
    $Str =~ s/\>/$GREATER_THAN/go;
    $Str =~ s/\</$LESSER_THAN/go;
    $Str =~ s/\&/$AND_MARK/go;
    return($Str);
}

sub DQDecode {
    local($Str) = @_;
    $Str =~ s/$DOUBLE_QUOTE/\"/go;
    $Str =~ s/$GREATER_THAN/\>/go;
    $Str =~ s/$LESSER_THAN/\</go;
    $Str =~ s/$AND_MARK/\&/go;
    return($Str);
}


###
## ������encode and decode
#
sub ArticleEncode {

    local($TestType, $Article) = @_;
    local($Return) = $Article;
    local(@Cash) = ();
    local($Url, $Str);

    while ($Article =~ m/<URL:([^>]*)>/g) {
	$Url = $1;
	next if (grep(/^$Url$/, @Cash));
	push(Cash, $Url);
	if (&IsUrl($Url)) {
	    $Str = "<a href=\"$Url\"><URL:$Url></a>";
	}
	$Return =~ s/<URL:$Url>/$Str/g;
    }

    &tag_secure'decode(*Return); #'

    return($Return);

}


###
## �����ֹ�����䤹��
#
sub WriteArticleId {

    local($Id) = @_;

    # �����ֹ������ե�����
    local($File) = &GetPath($BOARD, $ARTICLE_NUM_FILE_NAME);
    local($TmpFile) = &GetPath($BOARD, $ARTICLE_NUM_TMP_FILE_NAME);

    # �����Τ����˸Ť����ͤ��㤤!
    local($OldArticleId) = &GetNewArticleId;
    &Fatal($ERR_ILLEGALARTICLEID, '') if (($Id =~ /^\d+$/) && ($Id < $OldArticleId));

    # Open Tmp File
    open(AID, ">$TmpFile") || &Fatal($ERR_FILE, $TmpFile);
    # ����ID
    print(AID "$Id\n");
    close(AID);

    # ����
    rename($TmpFile, $File);

}


###
## DB�ե�����˽񤭹���
#
sub AddDBFile {

    # ����Id��̾�������������ꡤ����
    local($Id, $Fid, $InputDate, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail, $ArticleNullFlag) = @_;

    local($dId, $dFid, $dAids, $dInputDate, $dSubject, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail);
    local($mdName, $mdInputDate, $mdSubject, $mdId, $mName, $mSubject, $mId, @To) = ();
    local($FidList) = $Fid;
    local($FFid, @FFid) = ();

    # ��ץ饤���Υ�ץ饤�������äƤ���(DB�ؤΥ���������������ġ�)
    if ($Fid ne '') {
	($FFid) = &GetArticlesInfo($Fid);
	@FFid = split(/,/, $FFid);
    }
    
    # ��Ͽ�ե�����
    local($File) = &GetPath($BOARD, $DB_FILE_NAME);
    local($TmpFile) = &GetPath($BOARD, $DB_TMP_FILE_NAME);

    # Open Tmp File
    open(DBTMP, ">$TmpFile") || &Fatal($ERR_FILE, $TmpFile);
    # Open DB File
    open(DB, "<$File") || &Fatal($ERR_FILE, $File);

    while(<DB>) {

	# Version Check
	&VersionCheck('DB', $1) if (m/^\# Kb-System-Id: ([^\/]*\/.*)$/o);

	print(DBTMP "$_"), next if (/^\#/o);
	print(DBTMP "$_"), next if (/^$/o);
	chop;

	($dId, $dFid, $dAids, $dInputDate, $dSubject, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail) = split(/\t/, $_);
	
	# �ե����赭�������Ĥ��ä��顤
	if (($dId ne '') && ($dId eq $Fid)) {

	    # ���ε����Υե�������ID�ꥹ�Ȥ˲ä���(����޶��ڤ�)
	    if ($dAids ne '') {$dAids .= ",$Id";} else {$dAids = $Id;}

	    # �������Υե�����ꥹ�Ȥ��äƤ��Ƹ�������ä���
	    # �������Υե�����ꥹ�Ȥ���
	    $FidList = "$dId,$dFid" if ($dFid ne '');

	    if ($SYS_FOLLOWMAIL) {
		# �ᥤ�������Τ���˥���å���
		$mdName = $dName;
		$mdInputDate = $dInputDate;
		$mdSubject = $dSubject;
		$mdId = $dId;
		$mName = $Name;
		$mSubject = $Subject;
		$mId = $Id;
		push(To, $dEmail) if ($dFmail ne '');
	    }
	}

	# DB�˽񤭲ä���
	printf(DBTMP "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n", $dId, $dFid, $dAids, $dInputDate, $dSubject, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail);

	# ��ץ饤���Υ�ץ饤�������ĥᥤ��������ɬ�פ�����С��������¸
	push(To, $dEmail) if ($SYS_FOLLOWMAIL && (@FFid) && $dFmail && $dEmail && (grep(/^$dId$/, @FFid)) && (! grep(/^$dEmail$/, @To)));

    }

    # �����������Υǡ�����񤭲ä��롥
    printf(DBTMP "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n", $Id, $FidList, '', $InputDate, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail);

    # close Files.
    close(DB);
    close(DBTMP);

    # DB�򹹿�����
    rename($TmpFile, $File);

    # ɬ�פʤ�ȿ�������ä����Ȥ�ᥤ�뤹��
    &FollowMail($mdName, $mdInputDate, $mdSubject, $mdId, $mName, $mSubject, $mId, @To) if (@To);

}


###
## ñ��ε�����ɽ����
#
sub ShowArticle {

    # ������Id�����
    local($Id) = @_;

    # ��������μ���
    local($Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url) = &GetArticlesInfo($Id);
    local($DateUtc) = &GetUtcFromOldDateTimeFormat($Date);
    local(@AidList) = split(/,/, $Aids);
    local($Aid);

    # ̤��Ƶ������ɤ�ʤ�
    &Fatal($ERR_NONEXTARTICLE, '') if ($Name eq '');

    # ɽ�����̤κ���
    &MsgHeader('Message view', "$Subject", $DateUtc);
    &ViewOriginalArticle($Id, $F_TRUE, $F_TRUE);

    # article end
    &cgi'KPrint("$H_LINE<br>\n<p>\n");

    # ȿ������
    &cgi'KPrint("$H_FOLLOW\n");
    if ($Aids ne '') {

	# ȿ������������ʤ��
	foreach $Aid (@AidList) {

	    # �ե����������ڹ�¤�μ���
	    # ex. '( a ( b ( c d ) ) ( e ) ( f ( g ) ) )'�Ȥ����ꥹ��
	    local(@FollowIdTree) = &GetFollowIdTree($Aid);

	    # �ᥤ��ؿ��θƤӽФ�(��������)
	    &ThreadArticleMain('subject only', @FollowIdTree);

	}

    } else {

	# ȿ������̵��
	&cgi'KPrint("<ul>\n<li>$H_NOTHING\n</ul>\n");

    }

    print("</p>\n");

    # ����«
    &MsgFooter;

}


###
## ���ε�����ɽ����
#
sub NextArticle {

    local($Id) = @_;

    local($Num) = '';
    local($Key, $Value);

    foreach ($[ .. $#DB_ID) {
	$Num = $_, last if ($DB_ID[$_] eq $Id);
    }

    &ShowArticle($DB_ID[++$Num]);

}


###
## �ե�������������ɽ����
#
sub ThreadArticle {

    # ��������Id�����
    local($Id) = @_;

    # �ե����������ڹ�¤�μ���
    # ex. '( a ( b ( c d ) ) ( e ) ( f ( g ) ) )'�Ȥ����ꥹ��
    local(@FollowIdTree) = &GetFollowIdTree($Id);

    # ɽ�����̤κ���
    &MsgHeader('Message view (threaded)', "$BOARDNAME: $THREADARTICLE_MSG", $TIME);

    # �ᥤ��ؿ��θƤӽФ�(��������)
    &ThreadArticleMain('subject only', @FollowIdTree);

    # �ᥤ��ؿ��θƤӽФ�(����)
    &ThreadArticleMain('', @FollowIdTree);

    &MsgFooter;

}


###
## �Ƶ�Ū�ˤ��ε����Υե�����ɽ�����롥
#
sub ThreadArticleMain {

    # Id�μ���
    local($SubjectOnly, $Head, @Tail) = @_;

    # �������פ����������Τ�Τ���
    if ($SubjectOnly) {

	if ($Head eq '(') {
	    print("<ul>\n");
	} elsif ($Head eq ')') {
	    print("</ul>\n");
	} else {
	    &PrintAbstract($Head);
	}

    } else {

	if (($Head ne '(') && ($Head ne ')')) {
	    # ��������ɽ��(���ޥ���դ�, �������ʤ�)
	    print("<hr>\n");
	    &ViewOriginalArticle($Head, $F_TRUE, $F_FALSE);
	}

    }

    # �Ƶ�
    &ThreadArticleMain($SubjectOnly, @Tail) if @Tail;

}


###
## �ե���������Id���ڹ�¤����Ф���
##
## ex. '( a ( b ( c d ) e ( f ) ) g ( h ) )'�Ȥ����ꥹ��
##
## a - b - c
##       - d
##     e - f
## g - h
##
#
sub GetFollowIdTree {

    # Id
    local($Id) = @_;

    # �Ƶ�Ū���ڹ�¤����Ф���
    return('(', &GetFollowIdTreeMain($Id), ')');

}

sub GetFollowIdTreeMain {

    # Id
    local($Id) = @_;

    # �Ƶ���߾��
    return() if ($Id eq '');

    # �ե����������Ф�
    local(@AidList) = split(/,/, $DB_AIDS{$Id});

    # �ʤ�������
    return($Id) unless @AidList;

    # �Ƶ�
    local(@Result) = ($Id, '(');
    local(@ChildResult) = ();
    foreach (@AidList) {
	@ChildResult = &GetFollowIdTreeMain($_);
	push(Result, @ChildResult) if @ChildResult;
    }
    return(@Result, ')');

}


###
## �����γ��פ�ɽ��
#
sub PrintAbstract {

    # Id
    local($Id) = @_;

    # �����������Ф���
    local($dFid, $dAids, $dDate, $dSubject, $dIcon, $dRemoteHost, $dName) = &GetArticlesInfo($Id);
    &cgi'KPrint(sprintf("<li>" . &GetFormattedTitle($Id, $dAids, $dIcon, $dSubject, $dName, $dDate) . "\n"));
}


###
## �桼�������ꥢ������桼����̾�����ᥤ�롤URL���äƤ��롥
#
sub GetUserInfo {

    # �������륨���ꥢ��̾
    local($Alias) = @_;

    # �����ꥢ����̾�����ᥤ�롤�ޥ���URL
    local($A, $N, $E, $H, $U);

    # �����ꥢ����̾�����ᥤ�롤�ޥ���URL
    local($rN, $rE, $rU) = ();

    # �ե�����򳫤�
    open(ALIAS, "<$USER_ALIAS_FILE") || &Fatal($ERR_FILE, $USER_ALIAS_FILE);
    
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
## ȿ�������ä����Ȥ�ᥤ�뤹�롥
#
sub FollowMail {

    # ���褤����
    local($Name, $Date, $Subject, $Id, $Fname, $Fsubject, $Fid, @To) = @_;

    local($URL) = "$SCRIPT_URL?b=$BOARD&c=e&id=$Id";
    local($FURL) = "$SCRIPT_URL?b=$BOARD&c=e&id=$Fid";
    
    # Subject
    local($MailSubject) = "The article was followed.";

    # Date
    local($InputDate) = &GetDateTimeFormatFromUtc($Date);

    # Message
    local($Message) = "$SYSTEM_NAME����Τ��Τ餻�Ǥ���

$InputDate�ˡ�$BOARDNAME�פ��Ф��ơ�$Name�פ��󤬽񤤤���
��$Subject��
$URL
���Ф��ơ�
��$Fname�פ��󤫤�
��$Fsubject�פȤ�����Ǥ�ȿ��������ޤ�����

�����֤Τ������
$FURL
�������������

�Ǥϼ��餷�ޤ���";

    # �ᥤ������
    &SendMail($MailSubject, $Message, $Fid, @To);
}


###
## �ᥤ������
#
sub SendMail {

    # subject���ᥤ��Υե�����̾�����ѵ���(���ʤ�̵��)������
    local($Subject, $Message, $Id, @To) = @_;

    # �ղåإå�������
    local($ExtensionHeader) = "X-Kb-System: $SYSTEM_NAME\n";
    $ExtensionHeader .= "X-Kb-Board: $BOARDNAME\nX-Kb-Articleid: $Id\n" if ($BOARDNAME && ($Id ne ''));

    # ���ѵ���
    if ($Id ne '') {

	# ���Ѥ���ե�����
	local($QuoteFile) = &GetArticleFileName($Id, $BOARD);

	# ���ڤ���
	$Message .= "\n$H_LINE\n";

	# ����
	open(TMP, "<$QuoteFile") || &Fatal($ERR_FILE, $QuoteFile);
	while(<TMP>) {

	    # Version Check
	    &VersionCheck('Article', $1), next if (m/^<!-- Kb-System-Id: ([^\/]*\/.*) -->$/o);

	    # �������פ�ʤ�
	    s/<[^>]*>//go;
	    $Message .= &HTMLDecode($_) if ($_ ne '');

	}
	close(TMP);

    }

    # ��������
    &Fatal($ERR_CANNOTSENDMAIL, '') unless (&cgi'SendMail($MAINT_NAME, $MAINT, $Subject, $ExtensionHeader, $Message, @To));

}

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
## ��������ɽ������
#
sub ShowIcon {

    local($FileName, $Title, $Help);

    # �����פ򽦤�
    local($Type) = $cgi'TAGS{'type'};

    # ɽ�����̤κ���
    &MsgHeader('Icon show', $SHOWICON_MSG, $PROGTIME);

    if ($Type eq 'article') {

	&cgi'KPrint(<<__EOF__);
<p>
$H_ICONINTRO_ARTICLE
</p>
<p>
<ul>
<li><img src="$ICON_TLIST" alt="$H_BACKTITLE" height="$ICON_HEIGHT" width="$ICON_WIDTH"> : $H_BACKTITLE
<li><img src="$ICON_NEXT" alt="$H_NEXTARTICLE" height="$ICON_HEIGHT" width="$ICON_WIDTH"> : $H_NEXTARTICLE
<li><img src="$ICON_FOLLOW" alt="$H_REPLYTHISARTICLE" height="$ICON_HEIGHT" width="$ICON_WIDTH"> : $H_REPLYTHISARTICLE
<li><img src="$ICON_QUOTE" alt="$H_REPLYTHISARTICLEQUOTE" height="$ICON_HEIGHT" width="$ICON_WIDTH"> : $H_REPLYTHISARTICLEQUOTE
<li><img src="$ICON_THREAD" alt="$H_READREPLYALL" height="$ICON_HEIGHT" width="$ICON_WIDTH"> : $H_READREPLYALL
</ul>
</p>
__EOF__

    } else {

	&cgi'KPrint(<<__EOF__);
<p>
$H_ICONINTRO_ARTICLE
<p>
<ul>
<li>$H_THREAD : $THREADARTICLE_MSG
</ul>
</p>
<p>
"$BOARDNAME"$H_ICONINTRO_ENTRY
</p>
<p>
<ul>
__EOF__

	# ��İ��ɽ��
	open(ICON, &GetIconPath("$BOARD.$ICONDEF_POSTFIX"))
	    || (open(ICON, &GetIconPath("$DEFAULT_ICONDEF"))
		|| &Fatal($ERR_FILE, &GetIconPath("$DEFAULT_ICONDEF")));
	while(<ICON>) {

	    # Version Check
	    &VersionCheck('Icon', $1), next if (m/^\# Kb-System-Id: ([^\/]*\/.*)$/o);

	    # ������ʸ�ϥ���󥻥�
	    next if (/^\#/o);
	    next if (/^$/o);
	    chop;
	    ($FileName, $Title, $Help) = split(/\t/, $_, 3);

	    # ɽ��
	    &cgi'KPrint(sprintf("<li><img src=\"%s\" alt=\"$Title\" height=\"$ICON_HEIGHT\" width=\"$ICON_WIDTH\"> : %s\n", &GetIconURL($FileName), ($Help || $Title)));
	}
	close(ICON);

	print("</ul>\n</p>\n");

    }

    &MsgFooter;

}


###
## ���ս�˥����ȡ�
#
sub SortArticle {

    # ɽ������Ŀ������
    local($Num, $Old) = ($cgi'TAGS{'num'}, $cgi'TAGS{'old'});
    local($NextOld) = ($Old > $Num) ? ($Old - $Num) : 0;
    local($BackOld) = ($Old + $Num);
    local($To) = $#DB_ID - $Old;
    local($From) = $To - $Num + 1; $From = 0 if (($From < 0) || ($Num == 0));
    
    # ��������
    local($IdNum, $Id);

    # ɽ�����̤κ���
    &MsgHeader('Title view (sorted)', "$BOARDNAME: $SORT_MSG", $TIME);

    &BoardHeader;

    print("<hr>\n");

    if ($SYS_BOTTOMTITLE) {
	&cgi'KPrint("<p>$H_TOP<a href=\"$PROGRAM?b=$BOARD&c=r&num=$Num&old=$BackOld\">$H_BACKART</a></p>\n") if ($From > 0);
    } else {
	&cgi'KPrint("<p>$H_TOP<a href=\"$PROGRAM?b=$BOARD&c=r&num=$Num&old=$NextOld\">$H_NEXTART</a></p>\n") if ($Old);
    }

    print("<p><ul>\n");

    # ������ɽ��
    if ($#DB_ID == -1) {

	# �����ä��ġ�
	&cgi'KPrint("<li>$H_NOARTICLE\n");

    } else {

	if ($SYS_BOTTOMTITLE) {
	    for ($IdNum = $From; $IdNum <= $To; $IdNum++) {
		$Id = $DB_ID[$IdNum];
		&cgi'KPrint("<li>" . &GetFormattedTitle($Id, $DB_AIDS{$Id}, $DB_ICON{$Id}, $DB_TITLE{$Id}, $DB_NAME{$Id}, $DB_DATE{$Id}) . "\n");
	    }
	} else {
	    for ($IdNum = $To; $IdNum >= $From; $IdNum--) {
		$Id = $DB_ID[$IdNum];
		&cgi'KPrint("<li>" . &GetFormattedTitle($Id, $DB_AIDS{$Id}, $DB_ICON{$Id}, $DB_TITLE{$Id}, $DB_NAME{$Id}, $DB_DATE{$Id}) . "\n");
	    }
	}
    }

    print("</ul></p>\n");

    if ($SYS_BOTTOMTITLE) {
	&cgi'KPrint("<p>$H_BOTTOM<a href=\"$PROGRAM?b=$BOARD&c=r&num=$Num&old=$NextOld\">$H_NEXTART</a></p>\n") if ($Old);
    } else {
	&cgi'KPrint("<p>$H_BOTTOM<a href=\"$PROGRAM?b=$BOARD&c=r&num=$Num&old=$BackOld\">$H_BACKART</a></p>\n") if ($From > 0);
    }

    &MsgFooter;

}


###
## �����������Υ����ȥ��thread�̤�n�Ĥ�ɽ����
#
sub ViewTitle {

    # ɽ������Ŀ������
    local($Num, $Old) = ($cgi'TAGS{'num'}, $cgi'TAGS{'old'});
    local($NextOld) = ($Old > $Num) ? ($Old - $Num) : 0;
    local($BackOld) = ($Old + $Num);
    local($To) = $#DB_ID - $Old;
    local($From) = $To - $Num + 1; $From = 0 if (($From < 0) || ($Num == 0));

    # ��������
    local($IdNum, $Id, $Line);

    # �ե����ޥåȤ��������ȥ�������ꥹ��
    local(@NewLines) = ();

    # �����򥤥�ǥ�Ȥ��롥
    for ($IdNum = $From; $IdNum <= $To; $IdNum++) {
    
	# �����������Ф���
	$Id = $DB_ID[$IdNum];

	# �����ȥ��ե����ޥå�
	$Line = "<!--$Id-->" . &GetFormattedTitle($Id, $DB_AIDS{$Id}, $DB_ICON{$Id}, $DB_TITLE{$Id}, $DB_NAME{$Id}, $DB_DATE{$Id});

	# �ɲ�
	@NewLines = $DB_FID{$Id}
	    ? &AddTitleFollow((split(/,/, $DB_FID{$Id}))[0], $Line, @NewLines)
		: &AddTitleNormal($Line, @NewLines);

    }

    # ɽ�����̤κ���
    &MsgHeader('Title view (threaded)', "$BOARDNAME: $VIEW_MSG", $TIME);

    &BoardHeader;

    print("<hr>\n");

    if ($SYS_BOTTOMTITLE) {
	&cgi'KPrint("<p>$H_TOP<a href=\"$PROGRAM?b=$BOARD&c=v&num=$Num&old=$BackOld\">$H_BACKART</a></p>\n") if ($From > 0);
    } else {
	&cgi'KPrint("<p>$H_TOP<a href=\"$PROGRAM?b=$BOARD&c=v&num=$Num&old=$NextOld\">$H_NEXTART</a></p>\n") if ($Old);
    }

    print("<p><ul>\n");

    # ������ɽ��
    if (! @NewLines) {

	# �����ä��ġ�
	&cgi'KPrint("<li>$H_NOARTICLE\n");

    } else {

	foreach (@NewLines) {
	    if (! /^${NULL_LINE}$/o) {
		if ((m!^<ul>$!io) || (m!^</ul>$!io)) {
		    &cgi'KPrint("$_\n");
		} else {
		    &cgi'KPrint("<li>$_");
		}
	    }
	}
    }

    print("</ul></p>\n");

    if ($SYS_BOTTOMTITLE) {
	&cgi'KPrint("<p>$H_BOTTOM<a href=\"$PROGRAM?b=$BOARD&c=v&num=$Num&old=$NextOld\">$H_NEXTART</a></p>\n") if ($Old);
    } else {
	&cgi'KPrint("<p>$H_BOTTOM<a href=\"$PROGRAM?b=$BOARD&c=v&num=$Num&old=$BackOld\">$H_BACKART</a></p>\n") if ($From > 0);
    }

    &MsgFooter;

}


###
## �����ȥ�ꥹ�Ȥ˽񤭹���(����)
#
sub AddTitleNormal {

    # ��Ǽ�ԡ���Ǽ��
    local($Line, @Lines) = @_;

    # �ե饰�˱����ơġ�
    if ($SYS_BOTTOMTITLE) {

	# �������ɲ�
	push(Lines, $Line, $NULL_LINE);
    } else {

	# ��Ƭ���ɲ�
	unshift(Lines, $Line, $NULL_LINE);
    }

    # �֤�
    return(@Lines);

}


###
## �����ȥ�ꥹ�Ȥ˽񤭹���(�ե���)
#
sub AddTitleFollow {

    # �ե�������ID����Ǽ�ԡ���Ǽ��
    local($Fid, $AddLine, @Lines) = @_;
    local(@NewLines) = ();

    # Follow Flag
    local($AddFlag, $Nest, $NextLine) = (0, 0, ''); 

    # �����ȥ�ꥹ�ȤΥե饰
    local($TitleListFlag) = 0;

    while($_ = shift(Lines)) {

	# ���Τޤ޽񤭽Ф���
	push(NewLines, $_);

	# �����ȥ�ꥹ���桤�������Ƥε������褿�顤
	if (/<!--$Fid-->/) {

	    # 1�Զ��ɤ�
	    $_ = shift(Lines);

	    if (/^<ul>/o) {
		$Nest = 1;
		do {
		    push(NewLines, $_);
		    $_ = shift(Lines);
		    $Nest++ if (/^<ul>/o);
		    $Nest-- if (/^<\/ul>/o);
		} until ($Nest == 0);
		
		push(NewLines, $AddLine, $NULL_LINE);
		push(NewLines, $_);
		
	    } else {

		push(NewLines, "<ul>");
		push(NewLines, $AddLine, $NULL_LINE);
		push(NewLines, "</ul>");

	    }

	    $AddFlag = 1;
	}
    }

    # ����������������ʤ��ʤ�ġ�
    if (! $AddFlag) {

	# �ե饰�˱����ơġ�
	if ($SYS_BOTTOMTITLE) {
	    
	    # �������ɲ�
	    push(NewLines, $AddLine, $NULL_LINE);
	} else {

	    # ��Ƭ���ɲ�
	    unshift(NewLines, $AddLine, $NULL_LINE);
	}
    }

    return(@NewLines);

}


###
## ��������������n�Ĥ�ɽ����
#
sub NewArticle {

    # ɽ������Ŀ������
    local($Num, $Old) = ($cgi'TAGS{'num'}, $cgi'TAGS{'old'});
    local($NextOld) = ($Old > $Num) ? ($Old - $Num) : 0;
    local($BackOld) = ($Old + $Num);
    local($To) = $#DB_ID - $Old;
    local($From) = $To - $Num + 1; $From = 0 if (($From < 0) || ($Num == 0));

    # ��������
    local($Id) = ();

    # ɽ�����̤κ���
    &MsgHeader('Message view (sorted)', "$BOARDNAME: $NEWARTICLE_MSG", $TIME);

    if ($SYS_BOTTOMARTICLE) {
	&cgi'KPrint("<p>$H_TOP<a href=\"$PROGRAM?b=$BOARD&c=l&num=$Num&old=$BackOld\">$H_BACKART</a></p>\n") if ($From > 0);
    } else {
	&cgi'KPrint("<p>$H_TOP<a href=\"$PROGRAM?b=$BOARD&c=l&num=$Num&old=$NextOld\">$H_NEXTART</a></p>\n") if ($Old);
    }

    if (! $#DB_ID == -1) {

	# �����ä��ġ�
	&cgi'KPrint("<p>$H_NOARTICLE</p>\n");

    } else {

	if ($SYS_BOTTOMARTICLE) {
	    for ($IdNum = $From; $IdNum <= $To; $IdNum++) {
		$Id = $DB_ID[$IdNum];
		&ViewOriginalArticle($Id, $F_TRUE, $F_TRUE);
		print("<hr>\n");
	    }
	} else {
	    for ($IdNum = $To; $IdNum >= $From; $IdNum--) {
		$Id = $DB_ID[$IdNum];
		&ViewOriginalArticle($Id, $F_TRUE, $F_TRUE);
		print("<hr>\n");
	    }
	}

    }

    if ($SYS_BOTTOMARTICLE) {
	&cgi'KPrint("<p>$H_BOTTOM<a href=\"$PROGRAM?b=$BOARD&c=l&num=$Num&old=$NextOld\">$H_NEXTART</a></p>\n") if ($Old);
    } else {
	&cgi'KPrint("<p>$H_BOTTOM<a href=\"$PROGRAM?b=$BOARD&c=l&num=$Num&old=$BackOld\">$H_BACKART</a></p>\n") if ($From > 0);
    }

    &cgi'KPrint(<<__EOF__);
<form action="$PROGRAM" method="POST">
<input name="b" type="hidden" value="$BOARD">
<input name="c" type="hidden" value="v">
<input name="num" type="hidden" value="$DEF_TITLE_NUM">
<input type="submit" value="$H_BACKTITLE">
</form>
__EOF__

    &MsgFooter;

}


###
## �����θ���(ɽ�����̺���)
#
sub SearchArticle {

    # ������ɡ������ϰϤ򽦤�
    local($Key, $SearchSubject, $SearchPerson, $SearchArticle, $SearchIcon, $Icon) = ($cgi'TAGS{'key'}, $cgi'TAGS{'searchsubject'}, $cgi'TAGS{'searchperson'}, $cgi'TAGS{'searcharticle'}, $cgi'TAGS{'searchicon'}, $cgi'TAGS{'icon'});

    # ɽ�����̤κ���
    &MsgHeader('Message search', "$BOARDNAME: $SEARCHARTICLE_MSG", $TIME);

    # ����«
    &cgi'KPrint(<<__EOF__);
<form action="$PROGRAM\" method="POST">
<input name="c" type="hidden" value="s">
<input name="b" type="hidden" value="$BOARD">
 
$H_INPUTKEYWORD
<input type="submit" value="$H_SEARCHKEYWORD">
<input type="reset" value="$H_RESETKEYWORD">

<p>$H_KEYWORD:
<input name="key" type="text" size="$KEYWORD_LENGTH" value="$Key">
</p>

<p>$H_SEARCHTARGET:
<ul>
__EOF__

    &cgi'KPrint(sprintf("<li><input name=\"searchsubject\" type=\"checkbox\" value=\"on\" %s>: $H_SEARCHTARGETSUBJECT\n", (($SearchSubject) ? 'CHECKED' : '')));
    &cgi'KPrint(sprintf("<li><input name=\"searchperson\" type=\"checkbox\" value=\"on\" %s>: $H_SEARCHTARGETPERSON\n", (($SearchPerson) ? 'CHECKED' : '')));
    &cgi'KPrint(sprintf("<li><input name=\"searcharticle\" type=\"checkbox\" value=\"on\" %s>: $H_SEARCHTARGETARTICLE", (($SearchArticle) ? 'CHECKED' : '')));

    &cgi'KPrint(sprintf("<li><input name=\"searchicon\" type=\"checkbox\" value=\"on\" %s>: $H_ICON // ", (($SearchIcon) ? 'CHECKED' : '')));

    # �������������
    print("<SELECT NAME=\"icon\">\n");
    &cgi'KPrint(sprintf("<OPTION%s>$H_NOICON\n", (($Icon && ($Icon ne $H_NOICON)) ? '' : ' SELECTED')));
	
    # ��İ��ɽ��
    open(ICON, &GetIconPath("$BOARD.$ICONDEF_POSTFIX"))
	|| (open(ICON, &GetIconPath("$DEFAULT_ICONDEF"))
	    || &Fatal($ERR_FILE, &GetIconPath("$DEFAULT_ICONDEF")));
    while(<ICON>) {

	# Version Check
	&VersionCheck('Icon', $1), next if (m/^\# Kb-System-Id: ([^\/]*\/.*)$/o);

	# ������ʸ�ϥ���󥻥�
	next if (/^\#/o);
	next if (/^$/o);
	chop;
	($FileName, $IconTitle) = split(/\t/, $_, 3);

	# ɽ��
	&cgi'KPrint(sprintf("<OPTION%s>$IconTitle\n", (($Icon eq $IconTitle) ? ' SELECTED' : '')));
    }
    close(ICON);
    print("</SELECT>\n");

    # �����������
    &cgi'KPrint(<<__EOF__);
(<a href="$PROGRAM?b=$BOARD&c=i&type=entry">$H_SEEICON</a>)<BR>
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


###
## �����θ���(������̤�ɽ��)
#
sub SearchArticleList {

    # ������ɡ������ϰ�
    local($Key, $Subject, $Person, $Article, $Icon, $IconType) = @_;

    local($dId, $dAids, $dDate, $dTitle, $dIcon, $dName, $dEmail);

    local($HitFlag) = 0;
    local($Line) = ();
    local($SubjectFlag, $PersonFlag, $ArticleFlag);
    local(@KeyList) = split(/ +/, $Key);
    local($Num);

    # �ꥹ�ȳ���
    print("<p><ul>\n");

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
		    $SubjectFlag = 0 if ($dTitle !~ /$_/i);
		}
	    }

	    # ��Ƽ�̾�򸡺�
	    if (($Person ne '') && ($dName ne '')) {
		$PersonFlag = 1;
		foreach (@KeyList) {
		    $PersonFlag = 0 if (($dName !~ /$_/i) && ($dEmail !~ /$_/i));
		}
	    }

	    # ��ʸ�򸡺�
	    if ($Article ne '') {
		$ArticleFlag = 1 if ($Line = &SearchArticleKeyword($dId, @KeyList));
	    }

	} else {

	    # ̵���ǰ���
	    $SubjectFlag = 1;

	}

	if ($SubjectFlag || $PersonFlag || $ArticleFlag) {

	    # ����1�ĤϹ��פ���
	    $HitFlag = 1;

	    # �����ؤΥ�󥯤�ɽ��
	    &cgi'KPrint("<li>" . &GetFormattedTitle($dId, $dAids, $dIcon, $dTitle, $dName, $dDate));

	    # ��ʸ�˹��פ���������ʸ��ɽ��
	    if ($ArticleFlag) {
		$Line =~ s/<[^>]*>//go;
		&cgi'KPrint("<blockquote>$Line</blockquote>\n");
	    }
	}
    }

    # �ҥåȤ��ʤ��ä���
    &cgi'KPrint("<li>$H_NOTFOUND\n") if ($HitFlag != 1);

    # �ꥹ���Ĥ���
    print("</ul></p>\n");
}


###
## �����θ���(��ʸ)
#
sub SearchArticleKeyword {

    # ID�ȥ������
    local($Id, @KeyList) = @_;
    local(@NewKeyList);
    local($Line, $Return, $Code) = ();

    local($File) = &GetArticleFileName($Id, $BOARD);
    local($ConvFlag) = ($Id !~ /^\d+$/);

    # ��������
    open(ARTICLE, "<$File") || &Fatal($ERR_FILE, $File);
    while($Line = <ARTICLE>) {

	# Version Check
	&VersionCheck('Article', $1), next if (m/^<!-- Kb-System-Id: ([^\/]*\/.*) -->$/o);

	# �������Ѵ�
	if ($ConvFlag) {
	    $Code = &jcode'getcode(*Line);
	    &jcode'convert(*Line, $SCRIPT_KCODE, $Code, "z");
	}

	# ���ꥢ
	@NewKeyList = ();

	foreach (@KeyList) {

	    if ($Line =~ /$_/i) {

		# �ޥå�����! 1���ܤʤ�Ф��Ȥ�
		$Return = $Line unless $Return;

	    } else {

		# �ޤ�õ���ʤ���ġ�
		push(NewKeyList, $_);

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
## �����ꥢ������Ͽ���ѹ�
#
sub AliasNew {

    # ɽ�����̤κ���
    &MsgHeader('Alias entry/edit', $ALIASNEW_MSG, $PROGTIME);

    # ������Ͽ/��Ͽ���Ƥ��ѹ�
    &cgi'KPrint(<<__EOF__);
<p>
$H_ALIASTITLE
</p>
<p>
<form action="$PROGRAM" method="POST">
<input name="c" type="hidden" value="am">
$H_ALIAS: <input name="alias" type="text" value="#" size="$NAME_LENGTH"><br>
$H_FROM: <input name="name" type="text" size="$NAME_LENGTH"><br>
$H_MAIL: <input name="email" type="text" size="$MAIL_LENGTH"><br>
$H_URL_S: <input name="url" type="text" value="http://" size="$URL_LENGTH"><br>
$H_ALIASNEWCOM<br>
<input type="submit" value="$H_ALIASNEWPUSH">
</form>
</p>
<hr>
<p>
$H_ALIASDELETE
</p>
<p>
<form action="$PROGRAM" method="POST">
<input name="c" type="hidden" value="ad">
$H_ALIAS: <input name="alias" type="text" size="$NAME_LENGTH"><br>
$H_ALIASDELETECOM<br>
<input type="submit" value="$H_ALIASDELETEPUSH">
</form>
</p>
<hr>
<p>
<form action="$PROGRAM" method="POST">
<input name="c" type="hidden" value="as">
<input type="submit" value="$H_ALIASREFERPUSH">
</form>
</p>
__EOF__
    
    # ����«
    &MsgFooter;

}


###
## ��Ͽ/�ѹ�
#
sub AliasMod {

    # �����ꥢ����̾�����ᥤ�롤URL
    local($A) = $cgi'TAGS{'alias'};
    local($N) = $cgi'TAGS{'name'};
    local($E) = $cgi'TAGS{'email'};
    local($U) = $cgi'TAGS{'url'};
    
    # �ޥ��󤬥ޥå�������
    #	0 ... �����ꥢ�����ޥå����ʤ�
    #	1 ... �����ꥢ���ϥޥå��������ޥ���̾���ޥå����ʤ�
    #	2 ... �ޥå����ƥǡ������ѹ�����
    local($HitFlag) = 0;
    local($Alias);

    # ʸ��������å�
    &AliasCheck($A, $N, $E, $U);
    
    # �����ꥢ�����ɤ߹���
    &CashAliasData($USER_ALIAS_FILE);
    
    # 1�Ԥ��ĥ����å�
    foreach $Alias (sort keys(%Name)) {
	next if ($A ne $Alias);
	
	# �ޥ���̾����ä���2�����ʤ���1��
	$HitFlag = (($REMOTE_HOST eq $Host{$Alias}) ? 2 : 1);
    }
    
    # �ޥ���̾�����ʤ�!
    &Fatal($ERR_CANNOTGRANT, '') if ($HitFlag == 1);

    # ������Ͽ
    $Alias = $A if ($HitFlag == 0);
    
    # �ǡ�������Ͽ
    $Name{$Alias} = $N;
    $Email{$Alias} = $E;
    $Host{$Alias} = $REMOTE_HOST;
    $URL{$Alias} = $U;
    
    # �����ꥢ���ե�����˽񤭽Ф�
    &WriteAliasData($USER_ALIAS_FILE);

    # ɽ�����̤κ���
    &MsgHeader('Alias modified', $ALIASMOD_MSG, $TIME);
    &cgi'KPrint("<p>$H_ALIAS: <strong>$A</strong>:\n");
    if ($HitFlag == 2) {
	&cgi'KPrint("$H_ALIASCHANGED</p>\n");
    } else {
	&cgi'KPrint("$H_ALIASENTRIED</p>\n");
    }
    &MsgFooter;
    
}


###
## �����ꥢ�������å�
#
sub AliasCheck {

    local($A, $N, $E, $U) = @_;

    &CheckAlias(*A);
    &CheckName(*N);
    &CheckEmail(*E);
    &CheckURL(*U);
    
}


###
## ���
#
sub AliasDel {

    # �����ꥢ��
    local($A) = $cgi'TAGS{'alias'};

    # �ޥ��󤬥ޥå�������
    #	0 ... �����ꥢ�����ޥå����ʤ�
    #	1 ... �����ꥢ���ϥޥå��������ޥ���̾���ޥå����ʤ�
    #	2 ... �ޥå����ƥǡ������ѹ�����
    local($HitFlag) = 0;
    local($Alias);

    # �����ꥢ�����ɤ߹���
    &CashAliasData($USER_ALIAS_FILE);
    
    # 1�Ԥ��ĥ����å�
    foreach $Alias (sort keys(%Name)) {
	next if ($A ne $Alias);
	
	# �ޥ���̾����ä���2�����ʤ���1��
	$HitFlag = (($REMOTE_HOST eq $Host{$Alias}) ? 2 : 1);
    }
    
    # �ޥ���̾�����ʤ�!
    &Fatal($ERR_CANNOTGRANT, '') if ($HitFlag == 1);
    
    # �����ꥢ�����ʤ�!
    &Fatal($ERR_UNKNOWNALIAS, $A) if ($HitFlag == 0);
    
    # ̾����ä�
    $Name{$A} = '';
    
    # �����ꥢ���ե�����˽񤭽Ф�
    &WriteAliasData($USER_ALIAS_FILE);
    
    # ɽ�����̤κ���
    &MsgHeader('Alias deleted', $ALIASDEL_MSG, $TIME);
    &cgi'KPrint("<p>$H_ALIAS: <strong>$A</strong>: $H_ALIASDELETED</p>\n");
    &MsgFooter;

}


###
## ����
#
sub AliasShow {

    # �����ꥢ�����ɤ߹���
    &CashAliasData($USER_ALIAS_FILE);
    local($Alias);
    
    # ɽ�����̤κ���
    &MsgHeader('Alias view', $ALIASSHOW_MSG, $TIME);
    # ������ʸ
    &cgi'KPrint(<<__EOF__);
<p>
$H_AORI_ALIAS
</p><p>
<a href="$PROGRAM?c=an">$H_ALIASTITLE</a>
</p>
__EOF__
    
    # �ꥹ�ȳ���
    print("<dl>\n");
    
    # 1�Ĥ���ɽ��
    foreach $Alias (sort keys(%Name)) {
	&cgi'KPrint(<<__EOF__);
<p>
<dt><strong>$Alias</strong>
<dd>$H_FROM: $Name{$Alias}
<dd>$H_MAIL: $Email{$Alias}
<dd>$H_HOST: $Host{$Alias}
<dd>$H_URL: $URL{$Alias}
</p>
__EOF__

    }

    # �ꥹ���Ĥ���
    print("</dl>\n");
    
    &MsgFooter;

}


###
## �����ꥢ���ե�������ɤ߹����Ϣ�������������ࡥ
## CAUTION: %Name, %Email, %Host, %URL������ޤ���
#
sub CashAliasData {

    # �ե�����
    local($File) = @_;
    
    local($A, $N, $E, $H, $U);

    # ������ࡥ
    open(ALIAS, "<$File") || &Fatal($ERR_FILE, $File);
    while(<ALIAS>) {

	# Version Check
	&VersionCheck('Alias', $1), next
	    if (m/^<!-- Kb-System-Id: ([^\/]*\/.*) -->$/o);

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
## �����ꥢ���ե�����˥ǡ�����񤭽Ф���
## CAUTION: %Name, %Email, %Host, %URL��ɬ�פȤ��ޤ���
##          $Name�������Ƚ񤭹��ޤʤ���
#
sub WriteAliasData {

    # �ե�����
    local($File) = @_;
    local($Alias);
    local($TmpFile) = $USER_ALIAS_TMP_FILE;

    # �񤭽Ф�
    open(ALIAS, ">$TmpFile") || &Fatal($ERR_FILE, $TmpFile);

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
## �Ǽ��ĤΥإå���ɽ������
#
sub BoardHeader {

    local($File) = &GetPath($BOARD, $BOARD_FILE_NAME);

    open(HEADER, "<$File") || &Fatal($ERR_FILE, $File);
    while(<HEADER>){
	# Version Check
	&VersionCheck('Header', $1), next if (m/^<!-- Kb-System-Id: ([^\/]*\/.*) -->$/o);
	# ɽ������
	&cgi'KPrint("$_");
    }
    close(HEADER);

}


###
## �����������ֹ���֤�
#
sub GetNewArticleId {

    # �����ֹ������ե�����
    local($ArticleNumFile) = &GetPath($BOARD, $ARTICLE_NUM_FILE_NAME);

    # �����ֹ�
    local($ArticleId);

    open(AID, "<$ArticleNumFile") || &Fatal($ERR_FILE, $ArticleNumFile);
    while(<AID>) {
	chop;
	$ArticleId = $_;
    }
    close(AID);

    # 1���䤷���֤�
    return($ArticleId + 1);

}


###
## �����ֹ���äƤ���(�ֹ�������ʤ�)��
#
sub GetArticleId {

    # �ե�����̾�����
    local($ArticleNumFile) = @_;

    # �����ֹ�
    local($ArticleId);

    open(AID, "<$ArticleNumFile") || &Fatal($ERR_FILE, $ArticleNumFile);
    while(<AID>) {
	chop;
	$ArticleId = $_;
    }
    close(AID);

    # �����ֹ���֤���
    return($ArticleId);
}


###
## �ܡ��ɥ����ꥢ������ܡ��ɥ����ꥢ��̾���äƤ��롥
#
sub GetBoardInfo {

    # �����ꥢ��̾
    local($Alias) = @_;

    # �ܡ���̾
    local($BoardName) = ();

    open(ALIAS, "<$BOARD_ALIAS_FILE") || &Fatal($ERR_FILE, $BOARD_ALIAS_FILE);
    while(<ALIAS>) {

	# Version Check
	&VersionCheck('Board', $1), next if (m/^\# Kb-System-Id: ([^\/]*\/.*)$/o);

	next if (/^\#/o);
	next if (/^$/o);
	chop;
	next unless (/^$Alias\t(.*)$/);
	$BoardName = $1;
    }
    close(ALIAS);

    return($BoardName);

}


###
## �����ȥ�ꥹ�ȤΥե����ޥå�
#
sub GetFormattedTitle {

    local($Id, $Aids, $Icon, $Title, $Name, $Date) = @_;
    local($String, $Fnum) = ('', 0);
    local($InputDate) = &GetDateTimeFormatFromUtc(($Date || &GetModifiedTime($Id)));
    local($IdStr, $Link, $Thread);

    # �����ȥ뤬�Ĥ��Ƥʤ��ä��顤Id�򤽤Τޤޥ����ȥ�ˤ��롥
    $Title = $Title || $Id;

    # �̾ﵭ��
    $IdStr = "<strong>$Id.</strong> ";
    $Link = "<a href=\"$PROGRAM?b=$BOARD&c=e&id=$Id\">$Title</a>";
    $Thread = (($Aids) ? " <a href=\"$PROGRAM?b=$BOARD&c=t&id=$Id\">$H_THREAD</a>" : '');

    if (($Icon eq $H_NOICON) || ($Icon eq '')) {
	$String = sprintf("$IdStr$Link$Thread [%s] $InputDate", ($Name || $MAINT_NAME));
    } else {
	$String = sprintf("$IdStr<img src=\"%s\" alt=\"$Icon \" width=\"$ICON_WIDTH\" height=\"$ICON_HEIGHT\">$Link$Thread [%s] $InputDate", &GetIconURLFromTitle($Icon), ($Name || $MAINT_NAME));
    }

    return($String);

}


###
## �����������ɽ��
#
sub ShowLinksToFollowedArticle {

    local(@IdList) = @_;

    local($Id);
    local($Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name);

    # ���ꥸ�ʥ뵭��
    if ($#IdList > 0) {
	$Id = @IdList[$#IdList];
	($Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name) = &GetArticlesInfo($Id);
	&cgi'KPrint("<br>\n<strong>$H_ORIG_TOP:</strong> " . &GetFormattedTitle($Id, $Aids, $Icon, $Subject, $Name, $Date));
    }

    # ������
    $Id = @IdList[0];
    ($Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name) = &GetArticlesInfo($Id);
    &cgi'KPrint("<br>\n<strong>$H_ORIG:</strong> " . &GetFormattedTitle($Id, $Aids, $Icon, $Subject, $Name, $Date));

}


###
## ʸ��������å�: �����ꥢ��
#
sub CheckAlias {

    local(*String) = @_;

    # �������å�
    (! $String) && &Fatal($ERR_NOTFILLED, '');

    # `#'�ǻϤޤäƤ�?
    ($String =~ (/^\#/)) || &Fatal($ERR_ILLEGALSTRING, $H_ALIAS);

    # 1ʸ���������
    (length($String) > 1) || &Fatal($ERR_ILLEGALSTRING, $H_ALIAS);

}


###
## ʸ��������å�: �����ȥ�
#
sub CheckSubject {

    local(*String) = @_;

    # �������å�
    (! $String) && &Fatal($ERR_NOTFILLED, '');

    # ����������å�
    &Fatal($ERR_TAGCRINDATA, '') if ($String =~ m/[<>\t\n]/o);

}


###
## ʸ��������å�: ̾��
#
sub CheckName {

    local(*String) = @_;

    # �������å�
    (! $String) && &Fatal($ERR_NOTFILLED, '');

    # ���ԥ����ɤ�����å�
    ($String =~ /[\t\n]/o) && &Fatal($ERR_CRINDATA, '');

}


###
## ʸ��������å�: �ᥤ��
#
sub CheckEmail {

    local(*String) = @_;

    if ($SYS_POSTERMAIL) {

	# �������å�
	&Fatal($ERR_NOTFILLED, '') if ($String eq '');

	# `@'�����äƤʤ��㥢����
	&Fatal($ERR_ILLEGALSTRING, 'E-Mail') if ($String !~ (/@/));

    }

    # ���ԥ����ɤ�����å�
    ($String =~ /[\t\n]/o) && &Fatal($ERR_CRINDATA, '');

}


###
## ʸ��������å�: URL
#
sub CheckURL {

    local(*String) = @_;

    # http://�����ξ��϶��ˤ��Ƥ��ޤ���
    $String = '' if ($String =~ m!^http://$!oi);

    # ������줿scheme + '://'�ǻϤޤ뤫�ɤ��������������å����롥�Ť�?
    ($String ne '') && (! &IsUrl($String)) && &Fatal($ERR_ILLEGALSTRING, 'URL');

}


###
## URL��?
#
sub IsUrl {

    local($String) = @_;
    local($Scheme);
    local($IsUrl) = 0;
    foreach $Scheme (@URL_SCHEME) {
	$IsUrl = 1 if ($String =~ m!^$Scheme://!i);
    }

    return($IsUrl);

}


###
## �����Υإå���ɽ��
#
sub MsgHeader {

    # message and board
    local($Title, $Message, $LastModified) = @_;
    
    &cgi'header($LastModified);
    &cgi'KPrint(<<__EOF__);
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML i18n//EN">
<html>
<head>
<title>$Title</title>
<base href="http://$SERVER_NAME:$SERVER_PORT$SYSDIR_NAME">
</head>
__EOF__

    print("<body");
    if ($SYS_NETSCAPE_EXTENSION) {
	print(" background=\"$BG_IMG\"") if $BG_IMG;
	print(" bgcolor=\"$BG_COLOR\"") if $BG_COLOR;
	print(" TEXT=\"$TEXT_COLOR\"") if $TEXT_COLOR;
	print(" LINK=\"$LINK_COLOR\"") if $LINK_COLOR;
	print(" ALINK=\"$ALINK_COLOR\"") if $ALINK_COLOR;
	print(" VLINK=\"$VLINK_COLOR\"") if $VLINK_COLOR;
    }
    print(">\n");

    &cgi'KPrint(<<__EOF__);
<h1>$Message</h1>
<hr>
__EOF__

}


###
## �����Υեå���ɽ��
#
sub MsgFooter {

    &cgi'KPrint(<<__EOF__);
<hr>
<address>
$ADDRESS
</address>
</body>
</html>
__EOF__

}


###
## ��å��ط�
#

# ��å�
sub lock {
    &lock_UNIX if ($ARCH eq 'UNIX');
    &lock_WinNT if ($ARCH eq 'WinNT');
    &lock_Win95 if ($ARCH eq 'Win95');
    &lock_Mac if ($ARCH eq 'Mac');
}

# �����å�
sub unlock {
    &unlock_UNIX if ($ARCH eq 'UNIX');
    &unlock_WinNT if ($ARCH eq 'WinNT');
    &unlock_Win95 if ($ARCH eq 'Win95');
    &unlock_Mac if ($ARCH eq 'Mac');
}

# UNIX + Perl4/5
sub lock_UNIX {
    local($TimeOut) = 0;
    local($Flag) = 0;
    srand($TIME|$$);
    open(LOCKORG, ">$LOCK_ORG") || &Fatal($ERR_FILE, $LOCK_ORG);
    close(LOCKORG);
    for($TimeOut = 0; $TimeOut < $LOCK_WAIT; $TimeOut++) {
	$Flag = 1, last if link($LOCK_ORG, $LOCK_FILE);
	select(undef, undef, undef, (rand(6)+5)/10);
    }
    unlink($LOCK_ORG);
    &Fatal($ERR_F_CANNOTLOCK, $TimeOut) unless ($Flag);
}

sub unlock_UNIX {
    unlink($LOCK_FILE);
}

# WinNT + Perl5(use flock)
sub lock_WinNT {
    local($LockEx, $LockUn) = (2, 8);
    open(LOCK, "$LOCK_FILE") || &Fatal($ERR_FILE, $LOCK_FILE);
    flock(LOCK, $LockEx);
}
sub unlock_WinNT {
    local($LockEx, $LockUn) = (2, 8);
    flock(LOCK, $LockUn);
    close(LOCK);
}

# Win95 + Perl5
sub lock_Win95 {
    # how can i lock a Win95?
    # somebody please solve this problem...
}

sub unlock_Win95 {
}

# Mac + MacPerl
sub lock_Mac {
    # how can i lock a Mac?
    # i don't know MacPerl well...
    # somebody please solve this problem...
}

sub unlock_Mac {
}


###
## ��������ɽ��
#
sub ViewOriginalArticle {

    # Id�����ޥ�ɤ�ɽ�����뤫�ݤ�����������ɽ�����뤫�ݤ�
    local($Id, $CommandFlag, $OriginalFlag) = @_;

    # ���Ѥ���ե�����
    local($QuoteFile) = &GetArticleFileName($Id, $BOARD);

    # ��������μ���
    local($Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url) = &GetArticlesInfo($Id);

    # ���ޥ��ɽ��?
    if (($CommandFlag == $F_TRUE) && $SYS_COMMAND) {

	&cgi'KPrint(<<__EOF__);
<p>
<a href="$PROGRAM?b=$BOARD&c=v&num=$DEF_TITLE_NUM"><img src="$ICON_TLIST" alt="$H_BACKTITLE" width="$ICON_WIDTH" height="$ICON_HEIGHT" BORDER="0"></a>
<a href="$PROGRAM?b=$BOARD&c=en&id=$Id"><img src="$ICON_NEXT" alt="$H_NEXTARTICLE" width="$ICON_WIDTH" height="$ICON_HEIGHT" BORDER="0"></a>
<a href="$PROGRAM?b=$BOARD&c=f&id=$Id"><img src="$ICON_FOLLOW" alt="$H_REPLYTHISARTICLE" width="$ICON_WIDTH" height="$ICON_HEIGHT" BORDER="0"></a>
<a href="$PROGRAM?b=$BOARD&c=q&id=$Id"><img src="$ICON_QUOTE" alt="$H_REPLYTHISARTICLEQUOTE" width="$ICON_WIDTH" height="$ICON_HEIGHT" BORDER="0"></a>
__EOF__
	if ($Aids ne '') {
	    &cgi'KPrint("<a href=\"$PROGRAM?b=$BOARD&c=t&id=$Id\"><img src=\"$ICON_THREAD\" alt=\"$H_READREPLYALL\" width=\"$ICON_WIDTH\" height=\"$ICON_HEIGHT\" BORDER=\"0\"></a>");
	} else {
	    &cgi'KPrint("<img src=\"$ICON_THREAD\" alt=\"$H_READREPLYALL\" width=\"$ICON_WIDTH\" height=\"$ICON_HEIGHT\" BORDER=\"0\">");
	}
	&cgi'KPrint("<a href=\"$PROGRAM?b=$BOARD&c=i&type=article\"><img src=\"$ICON_HELP\" alt=\"?\" width=\"$ICON_WIDTH\" height=\"$ICON_HEIGHT\" BORDER=\"0\"></a>\n</p>\n");

    }

    print("<p>\n");

    # �ܡ���̾�ȵ����ֹ桤��
    if (($Icon eq $H_NOICON) || ($Icon eq '')) {
	&cgi'KPrint("<strong>$H_SUBJECT</strong>: <strong>$Id .</strong> $Subject");
    } else {
	&cgi'KPrint(sprintf("<strong>$H_SUBJECT</strong>: <strong>$Id .</strong> <img src=\"%s\" alt=\"$Icon \" width=\"$ICON_WIDTH\" height=\"$ICON_HEIGHT\">$Subject", &GetIconURLFromTitle($Icon)));
    }

    # ��̾��
    if (($Url eq '') || ($Url eq 'http://')) {
	# ��http://���ä���פȤ����Τϵ�С������ؤ��н补���Τ����������ͽ�ꡥ
        # URL���ʤ����
        &cgi'KPrint("<br>\n<strong>$H_FROM</strong>: $Name");
    } else {
        # URL��������
        &cgi'KPrint("<br>\n<strong>$H_FROM</strong>: <a href=\"$Url\">$Name</a>");
    }

    # �ᥤ��
    &cgi'KPrint(" <a href=\"mailto:$Email\">&lt;$Email&gt;</a>") if ($Email ne '');

    # �ޥ���
    &cgi'KPrint("<br>\n<strong>$H_HOST</strong>: $RemoteHost") if $SYS_SHOWHOST;

    # �����
    local($InputDate) = &GetDateTimeFormatFromUtc($Date);
    &cgi'KPrint("<br>\n<strong>$H_DATE</strong>: $InputDate");

    # ȿ����(���Ѥξ��)
    &ShowLinksToFollowedArticle(split(/,/, $Fid)) if (($OriginalFlag == $F_TRUE) && ($Fid ne ''));

    # �ڤ���
    &cgi'KPrint("</p>\n$H_LINE<br>\n");

    # ���������
    open(TMP, "<$QuoteFile") || &Fatal($ERR_FILE, $QuoteFile);
    while(<TMP>) {

	# Version Check
	&VersionCheck('Article', $1), next if (m/^<!-- Kb-System-Id: ([^\/]*\/.*) -->$/o);

	# ɽ��
	&cgi'KPrint("$_");

    }
    close(TMP);

}


###
## �ܡ���̾�Τ�Id����ե�����Υѥ�̾����Ф���
#
sub GetArticleFileName {

    # Id��Board
    local($Id, $Board) = @_;

    # Board�����ʤ�Board�ǥ��쥯�ȥ��⤫�����С�
    # ���Ǥʤ���Х����ƥफ������
    return(($Board) ? "$Board/$Id" : "$Id") if ($ARCH eq 'UNIX');
    return(($Board) ? "$Board/$Id" : "$Id") if ($ARCH eq 'WinNT');
    return(($Board) ? "$Board/$Id" : "$Id") if ($ARCH eq 'Win95');
    return(($Board) ? ":$Board:$Id" : "$Id") if ($ARCH eq 'Mac');

}


###
## �ܡ���̾�Τȥե�����̾���顤���Υե�����Υѥ�̾����Ф���
#
sub GetPath {

    # Board��File
    local($Board, $File) = @_;

    # �֤�
    return("$Board/$File") if ($ARCH eq 'UNIX');
    return("$Board/$File") if ($ARCH eq 'WinNT');
    return("$Board/$File") if ($ARCH eq 'Win95');
    return(":$Board:$File") if ($ARCH eq 'Mac');

}


###
## ��������ե�����̾���顤���Υե�����Υѥ�̾����Ф���
#
sub GetIconPath {

    # Board��File
    local($File) = @_;

    # �֤�
    return("$ICON_DIR/$File") if ($ARCH eq 'UNIX');
    return("$ICON_DIR/$File") if ($ARCH eq 'WinNT');
    return("$ICON_DIR/$File") if ($ARCH eq 'Win95');
    return(":$ICON_DIR:$File") if ($ARCH eq 'Mac');

}


###
## ��������ե�����̾���顤���Υե������URL̾����Ф���
#
sub GetIconURL {

    # Board��File
    local($File) = @_;

    # �֤�
    return("$ICON_DIR/$File");

}


###
## ��������̾���顤���������URL�����
#
sub GetIconURLFromTitle {

    # ��������̾
    local($Icon) = @_;

    local($FileName, $Title, $TargetFile) = ();

    # ��İ��ɽ��
    open(ICON, &GetIconPath("$BOARD.$ICONDEF_POSTFIX"))
	|| (open(ICON, &GetIconPath("$DEFAULT_ICONDEF"))
	    || &Fatal($ERR_FILE, &GetIconPath("$DEFAULT_ICONDEF")));
    while(<ICON>) {

	# Version Check
	&VersionCheck('Icon', $1), next if (m/^\# Kb-System-Id: ([^\/]*\/.*)$/o);

	# ������ʸ�ϥ���󥻥�
	next if (/^\#/o);
	next if (/^$/o);
	chop;
	($FileName, $Title) = split(/\t/, $_, 3);
	$TargetFile = $FileName if ($Title eq $Icon);
    }
    close(ICON);

    return(($TargetFile) ? &GetIconURL($TargetFile) : '');

}


###
## ���뵭���ξ������Ф���
#
sub GetArticlesInfo {

    # �оݵ�����ID
    local($Id) = @_;

    return($DB_FID{$Id}, $DB_AIDS{$Id}, $DB_DATE{$Id}, $DB_TITLE{$Id}, $DB_ICON{$Id}, $DB_REMOTEHOST{$Id}, $DB_NAME{$Id}, $DB_EMAIL{$Id}, $DB_URL{$Id}, $DB_FMAIL{$Id});

}


###
## ����ID�ε������顤�ǽ�����UTC���äƤ���
#
sub GetModifiedTime {
    local($Id) = @_;
    return($TIME - (-M &GetArticleFileName($Id, $BOARD)) * $SECINDAY);
}


###
## UTC���顤���֤�ɽ��ʸ�������Ф�
## �Ť��С������Ǥϡ�DB��˻����ɽ��ʸ����(not UTC)�����Τޤ����äƤ��롥
#
sub GetDateTimeFormatFromUtc {

    local($Utc) = @_;

    # �Ť�����Τ�Τ餷����
    return($Utc) if ($Utc !~ m/^\d+$/);

    # �Ѵ�
    local($Sec, $Min, $Hour, $Mday, $Mon, $Year, $Wday, $Yday, $Isdst) = localtime($Utc);
    return(sprintf("%d/%d(%02d:%02d)", $Mon + 1, $Mday, $Hour, $Min));

}


###
## UTC����Ф�
## �Ť��С������Ǥϡ�DB��˻����ɽ��ʸ����(not UTC)�����Τޤ����äƤ��롥
#
sub GetUtcFromOldDateTimeFormat {

    local($Time) = @_;

    # �����餷��
    return($Time) if ($Time =~ m/^\d+$/);

    # Ŭ��
    return(854477921);

}


###
## Version Check
#
sub VersionCheck {

    local($FileType, $VersionString) = @_;

    local($VersionId, $ReleaseId) = split(/\//, $VersionString);

    # no check now...

}


###
## ���顼ɽ��
#
sub Fatal {

    # ���顼�ֹ�ȥ��顼����μ���
    local($FatalNo, $FatalInfo) = @_;

    # ���顼��å�����
    local($ErrString);

    if ($FatalNo == $ERR_FILE) {

	$ErrString = "File: $FatalInfo��¸�ߤ��ʤ������뤤��permission�����꤬�ְ�äƤ��ޤ���������Ǥ�����<a href=\"mailto:$MAINT\">$MAINT</a>�ޤǡ��嵭�ե�����̾���Τ餻��������";

    } elsif ($FatalNo == $ERR_NOTFILLED) {

	$ErrString = "���Ϥ���Ƥ��ʤ����ܤ�����ޤ�����äƤ⤦���٤��ľ���ƤߤƤ���������";

    } elsif ($FatalNo == $ERR_CRINDATA) {

	$ErrString = "���̾�����ᥤ�륢�ɥ쥹�ˡ�����ʸ�������Ԥ����äƤ��ޤäƤ��ޤ�����äƤ⤦���٤��ľ���ƤߤƤ���������";

    } elsif ($FatalNo == $ERR_TAGCRINDATA) {

	$ErrString = "�����HTML����������ʸ��������ʸ��������뤳�Ȥ϶ؤ����Ƥ��ޤ�����äư㤦��˽񤭴����Ƥ���������";

    } elsif ($FatalNo == $ERR_CANNOTGRANT) {

	$ErrString = "��Ͽ����Ƥ��륨���ꥢ���Τ�Τȡ��ޥ���̾�����פ��ޤ��󡥤�����Ǥ�����<a href=\"mailto:$MAINT\">$MAINT</a>�ޤǸ�Ϣ����������";

    } elsif ($FatalNo == $ERR_UNKNOWNALIAS) {

	$ErrString = "$FatalInfo�Ȥ��������ꥢ���ϡ���Ͽ����Ƥ��ޤ���";

    } elsif ($FatalNo == $ERR_ILLEGALSTRING) {

	$ErrString = "$FatalInfo��������������ޤ���? ��äƤ⤦���٤��ľ���ƤߤƤ���������";

    } elsif ($FatalNo == $ERR_NONEXTARTICLE) {

	$ErrString = "���ε����Ϥޤ���Ƥ���Ƥ��ޤ���";

    } elsif ($FatalNo == $ERR_CANNOTSENDMAIL) {

	$ErrString = "�ᥤ�뤬�����Ǥ��ޤ���Ǥ�����������Ǥ��������Υ��顼��������������<a href=\"mailto:$MAINT\">$MAINT</a>�ޤǤ��Τ餻����������";

    } elsif ($FatalNo == $ERR_F_CANNOTLOCK) {

	$ErrString ="�����ƥ�Υ�å��˼��Ԥ��ޤ��������߹�äƤ���褦�Ǥ��Τǡ���ʬ�ԤäƤ���⤦���٥����������Ƥ������������٥����������Ƥ��å�����Ƥ����硤���ƥʥ���Ǥ����ǽ���⤢��ޤ���";

    } else {

	$ErrString = "���顼�ֹ�����: $FatalInfo<br>������Ǥ��������Υ��顼��������������<a href=\"mailto:$mEmail\">$mEmail</a>�ޤǤ��Τ餻����������";

    }

    # �۾ｪλ�β�ǽ��������Τǡ��Ȥꤢ����lock�򳰤�
    # (��å��μ��Ԥλ��ʳ�)
    &unlock if ($FatalNo != $ERR_F_CANNOTLOCK);

    # ɽ�����̤κ���
    &MsgHeader('Error!', $ERROR_MSG, $TIME);

    &cgi'KPrint("<p>$ErrString</p>\n");

    if ($BOARD ne '') {
	&cgi'KPrint(<<__EOF__);
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
