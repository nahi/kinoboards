#!/usr/local/bin/perl5
#
# $Id: kb.cgi,v 4.20 1996-08-16 17:11:43 nakahiro Exp $


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
($CGIPROG_NAME = $SCRIPT_NAME) =~ s#^(.*/)##;
$SYSDIR_NAME = (($PATH_INFO) ? "$PATH_INFO/" : "$1");
$SCRIPT_URL = "http://$SERVER_NAME:$SERVER_PORT$SCRIPT_NAME";
$PROGRAM = (($PATH_INFO) ? "$SCRIPT_NAME$PATH_INFO" : $CGIPROG_NAME);


###
## ���󥯥롼�ɥե�������ɤ߹���
#
chdir($PATH_TRANSLATED) if ($PATH_TRANSLATED);
require('kb.ph');
require('jcode.pl');
require('cgi.pl');
require('tag_secure.pl');


###
## ����ѿ������
#

#
# �����default
#
$[ = 0;

#
# ���ɽ��
#
$ADDRESS = "KINOBOARDS/1.0 R2.2: Copyright (C) 1995, 96 <a href=\"http://www.kinotrope.co.jp/~nakahiro/\">NAKAMURA Hiroshi</a>.";

#
# �ե�����
#
# �����ֹ�ե�����
$ARTICLE_NUM_FILE_NAME = ".articleid";
# �����ֹ�ƥ�ݥ��ե�����
$ARTICLE_NUM_TMP_FILE_NAME = ".articleid.tmp";
# �Ǽ�����configuratin�ե�����
$CONF_FILE_NAME = ".kbconf";
# �����ȥ�ꥹ�ȥإå��ե�����
$BOARD_FILE_NAME = ".board";
# DB�ե�����
$DB_FILE_NAME = ".db";
# DB�ƥ�ݥ��ե�����
$DB_TMP_FILE_NAME = ".db.tmp";
# �桼�������ꥢ���ե�����
$USER_ALIAS_FILE = "kinousers";
# �桼�������ꥢ���ƥ�ݥ��ե�����
$USER_ALIAS_TMP_FILE = "kinousers.tmp";
# �ܡ��ɥ����ꥢ���ե�����
$BOARD_ALIAS_FILE = "kinoboards";
# �ǥե���ȤΥ�����������ե�����
$DEFAULT_ICONDEF = "all.idef";
# ��å��ե�����
$LOCK_FILE = ".lock.kb";
# ��å����ե�����
$LOCK_ORG = ".lock.kb.org";
# ��å����Υ�ȥ饤���
$LOCK_WAIT = 10;

#
# ��������ǥ��쥯�ȥ�
# (��������ȥ�����������ե�����������ǥ��쥯�ȥ�̾)
#
$ICON_DIR = "icons";

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
$ICONDEF_POSTFIX = "idef";
$ICON_HEIGHT = 20;
$ICON_WIDTH = 20;

#
# ���ѥե饰
#
$QUOTE_ON = 1;
$NO_QUOTE = 0;

#
# ���������ץ�����
#
$NULL_LINE = "__br__";
$DOUBLE_QUOTE = "__dq__";
$GREATER_THAN = '__gt__';
$LESSER_THAN = '__lt__';
$AND_MARK = '__amp__';


# �ȥ�å�
$SIG{'HUP'} = $SIG{'INT'} = $SIG{'QUIT'} = $SIG{'TERM'} = 'DoKill';
sub DoKill {
    &unlock();			# unlock
    exit(1);			# error exit.
}


###
## �ᥤ��
#
MAIN: {

    # ɸ������(POST)�ޤ��ϴĶ��ѿ�(GET)�Υǥ����ɡ�
    &cgi'decode;

    # ���ˤ˻Ȥ��Τ�����ѿ�
    $BOARD = $cgi'TAGS{'b'};
    $BOARDNAME = &GetBoardInfo($BOARD);

    # �Ǽ��ĸ�ͭ���åƥ��󥰤��ɤ߹���
    local($BoardConfFile) = &GetPath($BOARD, $CONF_FILE_NAME);
    require("$BoardConfFile") if (-s "$BoardConfFile");

    # �ͤ����
    local($Command) = $cgi'TAGS{'c'};
    local($Com) = $cgi'TAGS{'com'};
    local($Id) = $cgi'TAGS{'id'};
    local($Alias) = $cgi'TAGS{'alias'};
    local($Name) = $cgi'TAGS{'name'};
    local($Email) = $cgi'TAGS{'email'};
    local($URL) = $cgi'TAGS{'url'};

    # �ޤ��ϥ�å�
    &lock;

    # ���ޥ�ɥ����פˤ��ʬ��
    if ($Command eq "e") {
	&ShowArticle($Id);
    } elsif (($Command eq "en")
	     || (($Command eq "m") && ($Com eq $H_NEXTARTICLE))) {
	&ShowArticle($Id + 1);
    } elsif (($Command eq "t")
	     || (($Command eq "m") && ($Com eq $H_READREPLYALL))) {
	&ThreadArticle($Id);

    } elsif (($Command eq "n")
	     || (($Command eq "m") && ($Com eq $H_POSTNEWARTICLE))) {
	&Entry($NO_QUOTE, 0);
    } elsif (($Command eq "f")
	     || (($Command eq "m") && ($Com eq $H_REPLYTHISARTICLE))) {
	&Entry($NO_QUOTE, $Id);
    } elsif (($Command eq "q")
	     || (($Command eq "m") && ($Com eq $H_REPLYTHISARTICLEQUOTE))) {
	&Entry($QUOTE_ON, $Id);
    } elsif (($Command eq "p") && ($Com ne "x")) {
	&Preview();
    } elsif (($Command eq "x")
	     || (($Command eq "p") && ($Com eq "x"))) {
	&Thanks();

    } elsif ($Command eq "v") {
	&ViewTitle();
    } elsif ($Command eq "r") {
	&SortArticle();
    } elsif ($Command eq "l") {
	&NewArticle();

    } elsif ($Command eq "s") {
	&SearchArticle();
    } elsif ($Command eq "i") {
	&ShowIcon();

    } elsif ($Command eq "an") {
	&AliasNew();
    } elsif ($Command eq "am") {
	&AliasMod($Alias, $Name, $Email, $URL);
    } elsif ($Command eq "ad") {
	&AliasDel($Alias);
    } elsif ($Command eq "as") {
	&AliasShow();

    } else {
	print("illegal command was given.\n");
    }

    # ��å��򳰤�
    &unlock;

}


###
## �����ޤ�
#
exit 0;


###
## �񤭹��߲���
#
sub Entry {

    # ���Ѥ���/�ʤ��ȡ����Ѥ�����Ϥ���Id(���Ѥ��ʤ�����0)
    local($QuoteFlag, $Id) = @_;

    # ɽ�����̤κ���
    &MsgHeader("$BOARDNAME: $ENTRY_MSG");

    # �ե����ξ��
    if ($Id != 0) {
	# ������ɽ��(���ޥ��̵��)
	&ViewOriginalArticle($Id, 0);
	print("<hr>\n");
	print("<h2>$H_REPLYMSG</h2>");
    }

    # �إå���ʬ��ɽ��
    &EntryHeader((($Id !=0 ) ? &GetReplySubject($Id, $BOARDDIR) : ''), $Id);

    # ��ʸ(���Ѥ���ʤ鸵����������)
    print("<textarea name=\"article\" rows=\"$TEXT_ROWS\" cols=\"$TEXT_COLS\">");
    &QuoteOriginalArticle($Id, $BOARD)
	if (($Id != 0) && ($QuoteFlag == $QUOTE_ON));
    print("</textarea><br>\n");

    # �եå���ʬ��ɽ��
    &EntryFooter();

}


###
## �񤭹��߲��̤Τ�����������ʸ��TextType��Board̾��ɽ����
#
sub EntryHeader {

    local($Subject, $Id) = @_;

    # ����«
    print(<<__EOF__);
<p>
<form action="$PROGRAM" method="POST">
<input name="c" type="hidden" value="p">
<input name="b" type="hidden" value="$BOARD">
<input name="id" type="hidden" value="$Id">
</p>
<p>
$H_AORI
</p>
$H_BOARD $BOARDNAME<br>
__EOF__

    # �������������
    if ($SYS_ICON) {
	print("$H_ICON\n");
	print("<SELECT NAME=\"icon\">\n");
	print("<OPTION SELECTED>$H_NOICON\n");

	# ��İ��ɽ��
	open(ICON, &GetIconPath("$BOARD.$ICONDEF_POSTFIX"))
	    || (open(ICON, &GetIconPath("$DEFAULT_ICONDEF"))
		|| &Fatal(1, &GetIconPath("$DEFAULT_ICONDEF")));
	while(<ICON>) {
	    # ������ʸ�ϥ���󥻥�
	    next if (/^\#/o);
	    next if (/^$/o);
	    chop;
	    ($FileName, $Title) = split(/\t/, $_, 3);
	    print("<OPTION>$Title\n");
	}
	close(ICON);
	print("</SELECT>\n");
	print("(<a href=\"$PROGRAM?b=$BOARD&c=i&type=entry\">$H_SEEICON</a>)<BR>\n");
    }

    # Subject(�ե����ʤ鼫ưŪ��ʸ����������)
    printf("%s <input name=\"subject\" type=\"text\" value=\"%s\" size=\"%s\"><br>\n",
	   $H_SUBJECT, $Subject, $SUBJECT_LENGTH);

    # TextType
    if ($SYS_TEXTTYPE) {
	print(<<__EOF__);
$H_TEXTTYPE
<SELECT NAME="texttype">
<OPTION SELECTED>$H_PRE
<OPTION>$H_HTML
</SELECT><BR>
__EOF__

    }

}


###
## �եå���ʬ��ɽ��
#
sub EntryFooter {

    # ̾���ȥ᡼�륢�ɥ쥹��URL��
    print(<<__EOF__);
$H_FROM <input name="name" type="text" size="$NAME_LENGTH"><br>
$H_MAIL <input name="mail" type="text" size="$MAIL_LENGTH"><br>
$H_URL <input name="url" type="text" value="http://" size="$URL_LENGTH"><br>
__EOF__

    ($SYS_FOLLOWMAIL) && print("$H_FMAIL <input name=\"fmail\" type=\"checkbox\" value=\"on\"><br>\n");
    
    if ($SYS_ALIAS) {
	print(<<__EOF__);
<p>
$H_ALIASINFO
(<a href="$PROGRAM?c=as">$H_SEEALIAS</a> //
 <a href="$PROGRAM?c=an">$H_ALIASENTRY</a>)
</p>
__EOF__

    }

    # �ܥ���
    print(<<__EOF__);
<input type="radio" name="com" value="p" CHECKED>: $H_PREVIEW<br>
<input type="radio" name="com" value="x">: $H_ENTRY<br>
<input type="submit" value="$H_PUSHHERE">
</p>
</form>
__EOF__

    &MsgFooter();
}


###
## ����Id�ε�������Subject���äƤ��ơ���Ƭ�ˡ�Re: �פ�1�Ĥ����Ĥ����֤���
#
sub GetReplySubject {

    # Id��Board
    local($Id, $Board) = @_;

    # ��������
    local($dFid, $dAids, $dDate, $dSubject, $dIcon, $dRemoteHost, $dName,
	  $dEmail, $dUrl, $dFmail) = &GetArticlesInfo($Id);

    # ��Ƭ�ˡ�Re: �פ����äĤ��Ƥ����������
    $dSubject =~ s/^Re: //o;

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
    local($Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name)
	= &GetArticlesInfo($Id);

    # �ե�����򳫤�
    open(TMP, "<$QuoteFile") || &Fatal(1, $QuoteFile);
    while(<TMP>) {

	# ���ѤΤ�����Ѵ�
	s/\&//go;
	s/\"//go;
	s/<[^>]*>//go;

	# ����ʸ�����ɽ��
	printf("%s%s%s", $Name, $DEFAULT_QMARK, $_);
	
    }

    # �Ĥ���
    close(TMP);

}


###
## �ץ�ӥ塼����
#
sub Preview {

    # ���Ϥ��줿��������
    local($Id, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article,
	  $Qurl, $Fmail)
	= ($cgi'TAGS{'id'}, $cgi'TAGS{'texttype'}, $cgi'TAGS{'name'},
	   $cgi'TAGS{'mail'}, $cgi'TAGS{'url'}, $cgi'TAGS{'icon'},
	   $cgi'TAGS{'subject'}, $cgi'TAGS{'article'},
	   $cgi'TAGS{'qurl'}, $cgi'TAGS{'fmail'});

    # ���ѵ�����URL
    local($rFile) = '';

    # ���ѵ����ε�������
    local($rFid, $rAids, $rDate, $rSubject, $rIcon, $rRemoteHost, $rName,
	  $rEmail, $rUrl, $rFmail) = ('', '', '', '', '', '', '', '', '', '');

    # �⤷���Ѥʤ�ġġ�
    if ($Id) {

	# �̾ﵭ���ΰ��Ѥʤ�ġ�
	$rFile = "$PROGRAM?b=$BOARD&c=e&id=$Id";

	# ���ѵ����ε�����������
	($rFid, $rAids, $rDate, $rSubject, $rIcon, $rRemoteHost, $rName,
	 $rEmail, $rUrl, $rFmail) = &GetArticlesInfo($Id);

    }

    # ���Ϥ��줿��������Υ����å�
    ($Name, $Email, $Url, $Icon, $Article)
	= &CheckArticle($Name, $Email, $Url, $Subject, $Icon, $Article);

    # ��ǧ���̤κ���
    &MsgHeader($PREVIEW_MSG);

    # ����«
    print(<<__EOF__);
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
<input type="submit" value="$H_PUSHHERE">
</p>
__EOF__

    # ��
    (($Icon eq $H_NOICON) || (! $Icon))
        ? print("<strong>$H_SUBJECT</strong> $Subject<br>\n")
            : printf("<strong>$H_SUBJECT</strong> <img src=\"%s\" alt=\"$Icon\" width=\"$ICON_WIDTH\" height=\"$ICON_HEIGHT\"> $Subject<br>\n", &GetIconURLFromTitle($Icon));

    # ��̾��
    if ($Url eq "http://" || $Url eq '') {
        # URL���ʤ����
        print("<strong>$H_FROM</strong> $Name<br>\n");
    } else {
        # URL��������
        print("<strong>$H_FROM</strong> <a href=\"$Url\">$Name</a><br>\n");
    }

    # �᡼��
    print("<strong>$H_MAIL</strong> <a href=\"mailto:$Email\">&lt;$Email&gt;</a><br>\n");

    # ȿ����(���Ѥξ��)
    &ShowFormattedLinkToFollowedArticle($Id, $rIcon, $rSubject);

    # �ڤ���
    print("$H_LINE<br>\n");

    # TextType��������
    print("<pre>\n") if ((! $SYS_TEXTTYPE) || ($TextType eq $H_PRE));

    # ����
    $Article = &DQDecode($Article);
    $Article = &tag_secure'decode($Article);
    print("$Article\n");

    # TextType�Ѹ����
    print("</pre>\n") if ((! $SYS_TEXTTYPE) || ($TextType eq $H_PRE));
    
    # ����«
    print("</form>\n");

    &MsgFooter();
}


###
## ���Ϥ��줿��������Υ����å�
#
sub CheckArticle {

    # �������󤤤���
    local($Name, $Email, $Url, $Subject, $Icon, $Article) = @_;
    local($Tmp) = '';

    # �����ꥢ�������å�
    $_ = $Name;
    if (/^#.*$/) {
        ($Tmp, $Email, $Url) = &GetUserInfo($_);
	&Fatal(7, $Name) if ($Tmp eq '');
	$Name = $Tmp;
    }

    # ʸ��������å�
    &CheckName($Name);
    &CheckEmail($Email);
    &CheckURL($Url);
    &CheckSubject($Subject);

    # ��������Υ����å�; ������������̵���פ����ꡥ
    $Icon = $H_NOICON unless (&GetIconURLFromTitle($Icon));

    # �������"�򥨥󥳡���
    $Article = &DQEncode($Article);

    # ̾����e-mail��URL���֤���
    return($Name, $Email, $Url, $Icon, $Article);
}


###
## ��Ͽ�����
#
sub Thanks {

    # �����˵�������������
    &MakeNewArticle();

    # ɽ�����̤κ���
    &MsgHeader($THANKS_MSG);

    print(<<__EOF__);
<p>
$H_THANKSMSG
</p>
<form action="$PROGRAM" method="POST">
<input name="b" type="hidden" value="$BOARD">
<input name="c" type="hidden" value="v">
<input name="num" type="hidden" value="$DEF_TITLE_NUM">
<input type="submit" value="$H_BACK">
</form>
__EOF__

    &MsgFooter();
}


###
## ��������Ƥ��줿����������
#
sub MakeNewArticle {

    # ���դ���Ф���
    local($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst)
	= localtime(time);
    local($InputDate) = sprintf("%d/%d(%02d:%02d)", $mon + 1, $mday, $hour, $min);

    # ���Ϥ��줿��������
    local($Id, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article,
	  $Qurl, $Fmail)
	= ($cgi'TAGS{'id'}, $cgi'TAGS{'texttype'}, $cgi'TAGS{'name'},
	   $cgi'TAGS{'mail'}, $cgi'TAGS{'url'}, $cgi'TAGS{'icon'},
	   $cgi'TAGS{'subject'}, $cgi'TAGS{'article'},
	   $cgi'TAGS{'qurl'}, $cgi'TAGS{'fmail'});

    # ���Ϥ��줿��������Υ����å�
    ($Name, $Email, $Url, $Icon, $Article)
	= &CheckArticle($Name, $Email, $Url, $Subject, $Icon, $Article);

    # �����������ֹ�����(�ޤ������ֹ�������Ƥʤ�)
    local($ArticleId) = &GetNewArticleId();

    # �����Υե�����κ���
    &MakeArticleFile($TextType, $Article, $ArticleId);

    # DB�ե��������Ƥ��줿�������ɲ�
    # �̾�ε������Ѥʤ�ID
    &AddDBFile($ArticleId, $Id, $InputDate, $Subject, $Icon, $REMOTE_HOST,
	       $Name, $Email, $Url, $Fmail);

    # �����������ֹ��񤭹���
    &AddArticleId();

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
    open(TMP, ">$File") || &Fatal(1, $File);

    # TextType��������
    print(TMP "<pre>\n") if ((! $SYS_TEXTTYPE) || ($TextType eq $H_PRE));

    # ����; "��ǥ����ɤ����������ƥ������å�
    $Article = &DQDecode($Article);
    $Article = &tag_secure'decode($Article);
    print(TMP "$Article\n");

    # TextType�Ѹ����
    print(TMP "</pre>\n") if ((! $SYS_TEXTTYPE) || ($TextType eq $H_PRE));
    
    # ��λ
    close(TMP);

}


###
## "��encode and decode
#
sub DQEncode {
    local($_) = @_;
    s/\"/$DOUBLE_QUOTE/g;
    s/\>/$GREATER_THAN/g;
    s/\</$LESSER_THAN/g;
    s/\&/$AND_MARK/g;
    return($_);
}

sub DQDecode {
    local($_) = @_;
    s/$DOUBLE_QUOTE/\"/g;
    s/$GREATER_THAN/\>/g;
    s/$LESSER_THAN/\</g;
    s/$AND_MARK/\&/g;
    return($_);
}


###
## �����ֹ�����䤹��
#
sub AddArticleId {

    # �����ֹ������ե�����
    local($File) = &GetPath($BOARD, $ARTICLE_NUM_FILE_NAME);
    local($TmpFile) = &GetPath($BOARD, $ARTICLE_NUM_TMP_FILE_NAME);

    # �����������ֹ�
    local($ArticleId) = &GetNewArticleId();

    # Open Tmp File
    open(AID, ">$TmpFile") || &Fatal(1, $TmpFile);
    print(AID $ArticleId, "\n");
    close(AID);

    # ����
    rename($TmpFile, $File);

}


###
## DB�ե�����˽񤭹���
#
sub AddDBFile {

    # ����Id��̾�������������ꡤ����
    local($Id, $Fid, $InputDate, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail) = @_;
    local($dId, $dFid, $dAids, $dInputDate, $dSubject, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail);
    
    # ��Ͽ�ե�����
    local($File) = &GetPath($BOARD, $DB_FILE_NAME);
    local($TmpFile) = &GetPath($BOARD, $DB_TMP_FILE_NAME);

    # Open Tmp File
    open(DBTMP, ">$TmpFile") || &Fatal(1, $TmpFile);
    # Open DB File
    open(DB, "<$File") || &Fatal(1, $File);

    while(<DB>) {

	print(DBTMP "$_"), next if (/^\#/);
	print(DBTMP "$_"), next if (/^$/);
	chop;

	($dId, $dFid, $dAids, $dInputDate, $dSubject, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail) = split(/\t/, $_);
	
	# �ե����赭�������Ĥ��ä��顤
	if ($dId == $Fid) {

	    # ���ε����Υե�������ID�ꥹ�Ȥ˲ä���(����޶��ڤ�)
	    if ($dAids) {$dAids .= ",$Id";} else {$dAids = $Id;}

	    # ɬ�פʤ�ȿ�������ä����Ȥ�᡼�뤹��
	    &FollowMail($dEmail, $dName, $dInputDate, $dSubject, $dId, $Name,
			$Subject, $Id) if (($SYS_FOLLOWMAIL) && ($dFmail));

	}

	# DB�˽񤭲ä���
	printf(DBTMP "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n",
	       $dId, $dFid, $dAids, $dInputDate, $dSubject, $dIcon,
	       $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail);
    }

    # �����������Υǡ�����񤭲ä��롥
    printf(DBTMP "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n",
	   $Id, $Fid, '', $InputDate, $Subject, $Icon,
	   $RemoteHost, $Name, $Email, $Url, $Fmail);

    # close Files.
    close(DB);
    close(DBTMP);

    # DB�򹹿�����
    rename($TmpFile, $File);

}


###
## ñ��ε�����ɽ����
#
sub ShowArticle {

    # ������Id�����
    local($Id) = @_;

    # �����Υե�����̾�����
    local($File) = &GetArticleFileName($Id, $BOARD);

    # ���ѵ����ξ���
    local($rFid, $rAids, $rDate, $rSubject, $rIcon, $rRemoteHost, $rName, $rEmail, $rUrl, $rFmail);

    # ȿ�������ξ���
    local($aFid, $aAids, $aDate, $aSubject, $aIcon, $aRemoteHost, $aName, $aEmail, $aUrl, $aFmail);

    # ��������μ���
    local($Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail) = &GetArticlesInfo($Id);
    local(@AidList) = split(/,/, $Aids);
    local($Aid) = '';

    # ̤��Ƶ������ɤ�ʤ�
    &Fatal(11, '') unless ($Name);

    # ���ѵ�����������
    ($rFid, $rAids, $rDate, $rSubject, $rIcon, $rRemoteHost, $rName, $rEmail,
     $rUrl, $rFmail) = &GetArticlesInfo($Fid) if ($Fid != 0);

    # ɽ�����̤κ���
    &MsgHeader("[$BOARDNAME: $Id] $Subject");

    # ����«
    if ($SYS_COMMAND) {
	print(<<__EOF__);
<form action="$PROGRAM" method="POST">
<input name="c" type="hidden" value="m">
<input name="b" type="hidden" value="$BOARD">
<input name="id" type="hidden" value="$Id">
<p>
<a href="$PROGRAM?b=$BOARD&c=en&id=$Id"><img src="$ICON_NEXT" alt="$H_NEXTARTICLE" width="$ICON_WIDTH" height="$ICON_HEIGHT" BORDER="0"></a>
<a href="$PROGRAM?b=$BOARD&c=f&id=$Id"><img src="$ICON_FOLLOW" alt="$H_REPLYTHISARTICLE" width="$ICON_WIDTH" height="$ICON_HEIGHT" BORDER="0"></a>
<a href="$PROGRAM?b=$BOARD&c=q&id=$Id"><img src="$ICON_QUOTE" alt="$H_REPLYTHISARTICLEQUOTE" width="$ICON_WIDTH" height="$ICON_HEIGHT" BORDER="0"></a>
<a href="$PROGRAM?b=$BOARD&c=t&id=$Id"><img src="$ICON_THREAD" alt="$H_READREPLYALL" width="$ICON_WIDTH" height="$ICON_HEIGHT" BORDER="0"></a>
<a href="$PROGRAM?b=$BOARD&c=i&type=article"><img src="$ICON_HELP" alt="?" width="$ICON_WIDTH" height="$ICON_HEIGHT" BORDER="0"></a>
</p>
</form>
__EOF__
    }

    # �ܡ���̾�ȵ����ֹ桤��
    if (($Icon eq $H_NOICON) || (! $Icon)) {
	print("<strong>$H_SUBJECT</strong> [$BOARDNAME: $Id] $Subject<br>\n");
    } else {
	printf("<strong>$H_SUBJECT</strong> [$BOARDNAME: $Id] <img src=\"%s\" alt=\"$Icon\" width=\"$ICON_WIDTH\" height=\"$ICON_HEIGHT\">$Subject<br>\n", &GetIconURLFromTitle($Icon));
    }

    # ��̾��
    if ((! $Url) || ($Url eq 'http://')) {
        # URL���ʤ����
        print("<strong>$H_FROM</strong> $Name<br>\n");
    } else {
        # URL��������
        print("<strong>$H_FROM</strong> <a href=\"$Url\">$Name</a><br>\n");
    }

    # �᡼��
    print("<strong>$H_MAIL</strong> <a href=\"mailto:$Email\">&lt;$Email&gt;</a><br>\n");

    # �ޥ���
    print("<strong>$H_HOST</strong> $RemoteHost<br>\n") if $SYS_SHOWHOST;

    # �����
    print("<strong>$H_DATE</strong> $Date<br>\n");

    # ȿ����(���Ѥξ��)
    &ShowFormattedLinkToFollowedArticle($Fid, $rIcon, $rSubject);

    # �ڤ���
    print("$H_LINE<br>\n");

    # ����
    open(TMP, "<$File") || &Fatal(1, $File);
    while(<TMP>) {print($_);}
    close(TMP);

    # article end
    print("<hr>\n");

    # ȿ������
    print("$H_FOLLOW<br>\n");

    if ($Aids) {

	# ȿ������������ʤ��
	print("<ul>\n");

	foreach $Aid (@AidList) {

	    # ȿ��������������
	    ($aFid, $aAids, $aDate, $aSubject, $aIcon, $aRemoteHost, $aName,
	     $aEmail, $aUrl, $aFmail) = &GetArticlesInfo($Aid);

	    # ɽ��
	    printf("<li>%s\n", &GetFormattedTitle($Aid, $aAids, $aIcon, $aSubject, $aName, $aDate));
	}

	print("</ul>\n");

    } else {

	# ȿ������̵��
	print("$H_NOTHING\n");

    }

    # ����«
    &MsgFooter();

}


###
## �ե�������������ɽ����
#
sub ThreadArticle {

    # ��������Id�����
    local($Id) = @_;

    # ɽ�����̤κ���
    &MsgHeader("$BOARDNAME: $THREADARTICLE_MSG");

    # �ᥤ��ؿ��θƤӽФ�(��������)
    print("<ul>\n");
    &ThreadArticleMain('subject only', $Id);
    print("</ul>\n");

    print("<hr>\n");

    # �ᥤ��ؿ��θƤӽФ�(����)
    &ThreadArticleMain('', $Id);

    &MsgFooter();
}


###
## �Ƶ�Ū�ˤ��ε����Υե�����ɽ�����롥
#
sub ThreadArticleMain {

    # Id�μ���
    local($SubjectOnly, $Id) = @_;

    # �ե���������Id�μ���
    local(@FollowIdList) = &GetFollowIdList($Id);

    # �������פ����������Τ�Τ���
    if ($SubjectOnly) {

	# �������פ�ɽ��
	&PrintAbstract($Id);

    } else {

	# ��������ɽ��(���ޥ���դ�)
	&ViewOriginalArticle($Id, 1);

    }

    # �ե���������ɽ��
    foreach (@FollowIdList) {

	# ���ڤ�
	print("<hr>\n") unless ($SubjectOnly);

	# �������פʤ�վ��
	print("<ul>\n") if ($SubjectOnly);
	
	# �Ƶ�
	&ThreadArticleMain($SubjectOnly, $_, $BOARD);

	# �������פʤ�վ���Ĥ�
	print("</ul>\n") if ($SubjectOnly);

    }
}


###
## �ե���������Id���������Ф���
#
sub GetFollowIdList {

    # Id
    local($Id) = @_;

    # DB�ե�����
    local($DBFile) = &GetPath($BOARD, $DB_FILE_NAME);

    # �ꥹ��
    local(@Result) = ();

    # ��������
    local($dId, $dFid, $dAids, $dDate, $dTitle, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail);

    # ������
    open(DB, "<$DBFile") || &Fatal(1, $DBFile);
    while(<DB>) {

	next if (/^\#/);
	next if (/^$/);
	chop;

	($dId, $dFid, $dAids, $dDate, $dTitle, $dIcon, $dRemoteHost, $dName,
	 $dEmail, $dUrl, $dFmail) = split(/\t/, $_);

	# ���Ĥ��ä�!
	@Result = split(/,/, $dAids) if ($Id == $dId);

    }
    close(DB);

    # �֤�
    return(@Result);
}


###
## �����γ��פ�ɽ��
#
sub PrintAbstract {

    # Id
    local($Id) = @_;

    # �����������Ф���
    local($dFid, $dAids, $dDate, $dSubject, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail) = &GetArticlesInfo($Id);

    printf("%s\n", &GetFormattedAbstract($Id, $dIcon, $dSubject, $dName, $dDate));

}


###
## �桼�������ꥢ������桼����̾�����᡼�롤URL���äƤ��롥
#
sub GetUserInfo {

    # �������륨���ꥢ��̾
    local($Alias) = @_;

    # �����ꥢ����̾�����᡼�롤�ۥ��ȡ�URL
    local($A, $N, $E, $H, $U);

    # �����ꥢ����̾�����᡼�롤�ۥ��ȡ�URL
    local($rN, $rE, $rU) = ('', '', '');

    # �ե�����򳫤�
    open(ALIAS, "<$USER_ALIAS_FILE") || &Fatal(1, $USER_ALIAS_FILE);
    
    # 1��1�ĥ����å���
    while(<ALIAS>) {
	
	chop;
	
	# ʬ��
	($A, $N, $E, $H, $U) = split(/\t/, $_);
	
	# �ޥå����ʤ��㼡�ء�
	next unless ($A eq $Alias);
	
	$rN = $N;
	$rE = $E;
	$rU = $U;

    }
    close(ALIAS);

    # ����ˤ����֤�
    return($rN, $rE, $rU);
}


###
## ȿ�������ä����Ȥ�᡼�뤹�롥
#
sub FollowMail {

    # ���褤����
    local($To, $Name, $Date, $Subject, $Id, $Fname, $Fsubject, $Fid) = @_;

    local($URL) = "$SCRIPT_URL?b=$BOARD&c=e&id=$Id";
    local($FURL) = "$SCRIPT_URL?b=$BOARD&c=e&id=$Fid";
    
    # Subject
    local($MailSubject) = "The article was followed.";

    # Message
    local($Message) = "$SYSTEM_NAME����Τ��Τ餻�Ǥ���\n\n$Date�ˡ�$BOARDNAME�פ��Ф��ơ�$Name�פ��󤬽񤤤���\n��$Subject��\n$URL\n���Ф��ơ�\n��$Fname�פ��󤫤�\n��$Fsubject�פȤ�����Ǥ�ȿ��������ޤ�����\n\n�����֤Τ������\n$FURL\n�������������\n\n�Ǥϼ��餷�ޤ���";

    # �᡼������
    &SendMail($MailSubject, $Message, $Fid, $To);
}


###
## �᡼������
#
sub SendMail {

    # subject���᡼��Υե�����̾�����ѵ���(0�ʤ�̵��)������
    local($Subject, $Message, $Id, @To) = @_;

    # ���ѵ���
    if ($Id) {

	# ���Ѥ���ե�����
	local($QuoteFile) = &GetArticleFileName($Id, $BOARD);

	# ���ڤ���
	$Message .= "\n$H_LINE\n";

	# ����
	open(TMP, "<$QuoteFile") || &Fatal(1, $QuoteFile);
	while(<TMP>) {
	    s/<[^>]*>//go;	# �������פ�ʤ�
	    $Message .= &HTMLDecode($_) if ($_);
	}
	close(TMP);

    }

    # ��������
    &Fatal(9, '') unless (&cgi'SendMail($MAINT_NAME, $MAINT, $Subject, $Message, @To));

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
    &MsgHeader($SHOWICON_MSG);

    if ($Type eq 'article') {

	print(<<__EOF__);
<p>
$H_ICONINTRO_ARTICLE
</p>
<p>
<ul>
<li><img src="$ICON_NEXT" alt="$H_NEXTARTICLE" height="$ICON_HEIGHT" width="$ICON_WIDTH"> : $H_NEXTARTICLE
<li><img src="$ICON_FOLLOW" alt="$H_REPLYTHISARTICLE" height="$ICON_HEIGHT" width="$ICON_WIDTH"> : $H_REPLYTHISARTICLE
<li><img src="$ICON_QUOTE" alt="$H_REPLYTHISARTICLEQUOTE" height="$ICON_HEIGHT" width="$ICON_WIDTH"> : $H_REPLYTHISARTICLEQUOTE
<li><img src="$ICON_THREAD" alt="$H_READREPLYALL" height="$ICON_HEIGHT" width="$ICON_WIDTH"> : $H_READREPLYALL
</ul>
</p>
__EOF__

    } else {

	print(<<__EOF__);
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
		|| &Fatal(1, &GetIconPath("$DEFAULT_ICONDEF")));
	while(<ICON>) {
	    # ������ʸ�ϥ���󥻥�
	    next if (/^\#/o);
	    next if (/^$/o);
	    chop;
	    ($FileName, $Title, $Help) = split(/\t/, $_, 3);
	    printf("<li><img src=\"%s\" alt=\"$Title\" height=\"$ICON_HEIGHT\" width=\"$ICON_WIDTH\"> : %s\n", &GetIconURL($FileName), ($Help || $Title));
	}
	close(ICON);

	print("</ul>\n</p>\n");

    }

    &MsgFooter();

}


###
## ���ս�˥����ȡ�
#
sub SortArticle {

    # ɽ������Ŀ������
    local($Num, $Old) = ($cgi'TAGS{'num'}, $cgi'TAGS{'old'});
    local($NextOld) = ($Old > $Num) ? ($Old - $Num) : 0;
    local($BackOld) = ($Old + $Num);

    # ɽ������ʬ�������Ф�
    local(@Lines) = ();
    &GetTitle($Num, $Old, *Lines);

    # ��������
    local($Id, $Fid, $Aids, $Date, $Title, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail);

    # ɽ�����̤κ���
    &MsgHeader("$BOARDNAME: $SORT_MSG");

    &BoardHeader;

    print("<hr>\n");

    if ($SYS_BOTTOMTITLE) {
	print("<p>$H_TOP<a href=\"$PROGRAM?b=$BOARD&c=r&num=$Num&old=$BackOld\">$H_BACKART</a></p>\n") if (@Lines && (($#Lines + 1) == $Num));
    } else {
	print("<p>$H_TOP<a href=\"$PROGRAM?b=$BOARD&c=r&num=$Num&old=$NextOld\">$H_NEXTART</a></p>\n") if ($Old);
    }

    print("<ul>\n");

    # ������ɽ��
    if (! @Lines) {

	# �����ä��ġ�
	print("<li>$H_NOARTICLE\n");

    } else {

	@Lines = reverse(@Lines) unless ($SYS_BOTTOMTITLE);

	foreach (@Lines) {

	    # ��������μ��Ф�
	    ($Id, $Fid, $Aids, $Date, $Title, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail) = split(/\t/, $_, 11);
	    print("<li>" . &GetFormattedTitle($Id, $Aids, $Icon, $Title, $Name, $Date) . "\n");
	}
    }

    print("</ul>\n");

    if ($SYS_BOTTOMTITLE) {
	print("<p>$H_BOTTOM<a href=\"$PROGRAM?b=$BOARD&c=r&num=$Num&old=$NextOld\">$H_NEXTART</a></p>\n") if ($Old);
    } else {
	print("<p>$H_BOTTOM<a href=\"$PROGRAM?b=$BOARD&c=r&num=$Num&old=$BackOld\">$H_BACKART</a></p>\n") if (@Lines && (($#Lines + 1) == $Num));
    }

    &MsgFooter();

}


###
## ����n�Ĥ�DB������Ф���DB�ιԤ򤽤Τޤޥꥹ�Ȥˤ����֤���
#
sub GetTitle {

    # ������
    local($Num, $Old, *Lines) = @_;

    # DB�ե�����
    local($DBFile) = &GetPath($BOARD, $DB_FILE_NAME);

    # ��������
    local($Id, $Fid) = (0, '');

    # �桼������
    local($Name, $Passwd) = ('', '');

    # �����ߡ�DB�ե����뤬�ʤ���в���ɽ�����ʤ���
    open(DB, "<$DBFile") || &Fatal(1, $DBFile);

    while(<DB>) {

	# ������ʸ�ϥ���󥻥�
	next if (/^\#/o);
	next if (/^$/o);
	chop;

	# ��������μ��Ф�
	($Id, $Fid) = split(/\t/, $_, 3);

	# ���������Τ�ɽ�����ξ��ϥ���󥻥롥
	push(Lines, $_) unless (($SYS_NEWARTICLEONLY) && ($Fid != 0));

    }

    close(DB);

    # ɬ�פ���ʬ�����ڤ�Ф���
    if ($Old) {
	if (($#Lines + 1) > $Old) {
	    splice(@Lines, -$Old);
	} else {
	    @Lines = ();
	}
    }
    if ($Num && (($#Lines + 1) > $Num)) {
	@Lines = splice(@Lines, -$Num);
    }
}


###
## �����������Υ����ȥ��thread�̤�n�Ĥ�ɽ����
#
sub ViewTitle {

    # ɽ������Ŀ������
    local($Num, $Old) = ($cgi'TAGS{'num'}, $cgi'TAGS{'old'});
    local($NextOld) = ($Old > $Num) ? ($Old - $Num) : 0;
    local($BackOld) = ($Old + $Num);

    # �ե����ޥåȤ��������ȥ�
    local($Line) = '';

    # �ե����ޥåȤ��������ȥ�������ꥹ��
    local(@NewLines) = ();

    # ��������
    local($Id, $Fid, $Aids, $Date, $Title, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail);

    # ɽ������ʬ�������Ф�
    local(@Lines) = ();
    &GetTitle($Num, $Old, *Lines);

    # �����򥤥�ǥ�Ȥ��롥
    foreach (@Lines) {
    
	# �����������Ф���
	($Id, $Fid, $Aids, $Date, $Title, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail) = split(/\t/, $_);

	# �����ȥ��ե����ޥå�
	$Line = "<!--$Id-->" . &GetFormattedTitle($Id, $Aids, $Icon, $Title, $Name, $Date);

	# �ɲ�
	@NewLines = ($Fid)
	    ? &AddTitleFollow($Fid, $Line, @NewLines)
		: &AddTitleNormal($Line, @NewLines);

    }

    # ɽ�����̤κ���
    &MsgHeader("$BOARDNAME: $VIEW_MSG");

    &BoardHeader;

    print("<hr>\n");

    if ($SYS_BOTTOMTITLE) {
	print("<p>$H_TOP<a href=\"$PROGRAM?b=$BOARD&c=v&num=$Num&old=$BackOld\">$H_BACKART</a></p>\n") if (@Lines && (($#Lines + 1) == $Num));
    } else {
	print("<p>$H_TOP<a href=\"$PROGRAM?b=$BOARD&c=v&num=$Num&old=$NextOld\">$H_NEXTART</a></p>\n") if ($Old);
    }

    print("<ul>\n");

    # ������ɽ��
    if (! @NewLines) {

	# �����ä��ġ�
	print("<li>$H_NOARTICLE\n");

    } else {

	foreach (@NewLines) {
	    if (! /^${NULL_LINE}$/o) {
		if ((m!^<ul>$!io) || (m!^</ul>$!io)) {
		    print("$_\n");
		} else {
		    print("<li>$_");
		}
	    }
	}
    }

    print("</ul>\n");

    if ($SYS_BOTTOMTITLE) {
	print("<p>$H_BOTTOM<a href=\"$PROGRAM?b=$BOARD&c=v&num=$Num&old=$NextOld\">$H_NEXTART</a></p>\n") if ($Old);
    } else {
	print("<p>$H_BOTTOM<a href=\"$PROGRAM?b=$BOARD&c=v&num=$Num&old=$BackOld\">$H_BACKART</a></p>\n") if (@Lines && (($#Lines + 1) == $Num));
    }

    &MsgFooter();

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

	    if (/^<ul>/) {
		$Nest = 1;
		do {
		    push(NewLines, $_);
		    $_ = shift(Lines);
		    $Nest++ if (/^<ul>/);
		    $Nest-- if (/^<\/ul>/);
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

    # ɽ������ʬ���������ȥ�����
    local(@Lines) = ();
    &GetTitle($Num, $Old, *Lines);

    # ��������
    local($Id) = (0);

    # ɽ�����̤κ���
    &MsgHeader("$BOARDNAME: $NEWARTICLE_MSG");

    if ($SYS_BOTTOMARTICLE) {
	print("<p>$H_TOP<a href=\"$PROGRAM?b=$BOARD&c=l&num=$Num&old=$BackOld\">$H_BACKART</a></p>\n") if (@Lines && (($#Lines + 1) == $Num));
    } else {
	print("<p>$H_TOP<a href=\"$PROGRAM?b=$BOARD&c=l&num=$Num&old=$NextOld\">$H_NEXTART</a></p>\n") if ($Old);
    }

    if (! @Lines) {

	# �����ä��ġ�
	print("<p>$H_NOARTICLE</p>\n");

    } else {

	@Lines = reverse(@Lines) unless ($SYS_BOTTOMARTICLE);

	foreach (@Lines) {

	    # ��������μ��Ф�
	    ($Id) = split(/\t/, $_, 2);

	    # ������ɽ��(���ޥ���դ�)
	    &ViewOriginalArticle($Id, 'command');
	    print("<hr>\n");

	}

    }

    if ($SYS_BOTTOMARTICLE) {
	print("<p>$H_BOTTOM<a href=\"$PROGRAM?b=$BOARD&c=l&num=$Num&old=$NextOld\">$H_NEXTART</a></p>\n") if ($Old);
    } else {
	print("<p>$H_BOTTOM<a href=\"$PROGRAM?b=$BOARD&c=l&num=$Num&old=$BackOld\">$H_BACKART</a></p>\n") if (@Lines && (($#Lines + 1) == $Num));
    }

    print(<<__EOF__);
<form action="$PROGRAM" method="POST">
<input name="b" type="hidden" value="$BOARD">
<input name="c" type="hidden" value="v">
<input name="num" type="hidden" value="$DEF_TITLE_NUM">
<input type="submit" value="$H_BACK">
</form>
__EOF__

    &MsgFooter();

}


###
## �����θ���(ɽ�����̺���)
#
sub SearchArticle {

    # ������ɡ������ϰϤ򽦤�
    local($Key, $SearchSubject, $SearchPerson, $SearchArticle, $SearchIcon, $Icon)
	= ($cgi'TAGS{'key'}, $cgi'TAGS{'searchsubject'},
	   $cgi'TAGS{'searchperson'}, $cgi'TAGS{'searcharticle'},
	   $cgi'TAGS{'searchicon'}, $cgi'TAGS{'icon'});

    # ɽ�����̤κ���
    &MsgHeader("$BOARDNAME: $SEARCHARTICLE_MSG");

    # ����«
    print(<<__EOF__);
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
__EOF__

    printf("<li>$H_SEARCHTARGETSUBJECT: <input name=\"searchsubject\" type=\"checkbox\" value=\"on\" %s>\n", (($SearchSubject) ? 'CHECKED' : ''));
    printf("<li>$H_SEARCHTARGETPERSON: <input name=\"searchperson\" type=\"checkbox\" value=\"on\" %s>\n", (($SearchPerson) ? 'CHECKED' : ''));
    printf("<li>$H_SEARCHTARGETARTICLE: <input name=\"searcharticle\" type=\"checkbox\" value=\"on\" %s>", (($SearchArticle) ? 'CHECKED' : ''));

    printf("<li>$H_ICON: <input name=\"searchicon\" type=\"checkbox\" value=\"on\" %s> // ", (($SearchIcon) ? 'CHECKED' : ''));

    # �������������
    print("<SELECT NAME=\"icon\">\n");
    printf("<OPTION%s>$H_NOICON\n",
	   (($Icon && ($Icon ne $H_NOICON)) ? '' : ' SELECTED'));
	
    # ��İ��ɽ��
    open(ICON, &GetIconPath("$BOARDDIR.$ICONDEF_POSTFIX"))
	|| (open(ICON, &GetIconPath("$DEFAULT_ICONDEF"))
	    || &Fatal(1, &GetIconPath("$DEFAULT_ICONDEF")));
    while(<ICON>) {
	# ������ʸ�ϥ���󥻥�
	next if (/^\#/o);
	next if (/^$/o);
	chop;
	($FileName, $IconTitle) = split(/\t/, $_, 3);
	printf("<OPTION%s>$IconTitle\n",
	       (($Icon eq $IconTitle) ? ' SELECTED' : ''));
    }
    close(ICON);
    print("</SELECT>\n");

    # �����������
    print(<<__EOF__);
(<a href="$PROGRAM?b=$BOARD&c=i&type=entry">$H_SEEICON</a>)<BR>
</p>
</ul>
</form>
<hr>
__EOF__

    # ������ɤ����Ǥʤ���С����Υ�����ɤ�ޤ൭���Υꥹ�Ȥ�ɽ��
    if (($SearchIcon)
	|| (($Key) && ($SearchSubject || ($SearchPerson || $SearchArticle)))) {
	&SearchArticleList($Key, $SearchSubject, $SearchPerson, $SearchArticle,
			   $SearchIcon, $Icon);
    }

    &MsgFooter();

}


###
## �����θ���(������̤�ɽ��)
#
sub SearchArticleList {

    # ������ɡ������ϰ�
    local($Key, $Subject, $Person, $Article, $Icon, $IconType) = @_;

    # DB�ե�����
    local($DBFile) = &GetPath($BOARD, $DB_FILE_NAME);

    local($dId, $dFid, $dAids, $dDate, $dTitle, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail);

    local($ArticleFile, $HitFlag) = ('', 0);
    local($Line) = '';
    local($SubjectFlag, $PersonFlag, $ArticleFlag);
    local(@KeyList) = split(/ +/, $Key);

    # �ꥹ�ȳ���
    print("<ul>\n");

    # �ե�����򳫤���DB�ե����뤬�ʤ����not found.
    open(DB, "<$DBFile") || &Fatal(1, $DBFile);
    while(<DB>) {

	next if (/^\#/);
	next if (/^$/);

	# �ѿ��Υꥻ�å�
	$SubjectFlag = $PersonFlag = $ArticleFlag = 0;
	$Line = '';

	# ��������
	($dId, $dFid, $dAids, $dDate, $dTitle, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail) = split(/\t/, $_);

	# ������������å�
	next if (($Icon) && ($dIcon ne $IconType));

	if ($Key) {

	    # �����ȥ�򸡺�
	    if ($Subject) {
		$SubjectFlag = 1;
		foreach (@KeyList) {
		    $SubjectFlag = 0 unless ($dTitle =~ /$_/i);
		}
	    }

	    # ��Ƽ�̾�򸡺�
	    if ($Person) {
		$PersonFlag = 1;
		foreach (@KeyList) {
		    $PersonFlag = 0 unless ($dName =~ /$_/i);
		}
	    }

	    # ��ʸ�򸡺�
	    $ArticleFile = &GetArticleFileName($dId, $BOARD);
	    $ArticleFlag = 1 if ($Article && ($Line = &SearchArticleKeyword($ArticleFile, @KeyList)));

	} else {

	    # ̵���ǰ���
	    $SubjectFlag = 1;

	}

	if ($SubjectFlag || $PersonFlag || $ArticleFlag) {

	    # ����1�ĤϹ��פ���
	    $HitFlag = 1;

	    # �����ؤΥ�󥯤�ɽ��
	    print("<li>" . &GetFormattedTitle($dId, $dAids, $dIcon, $dTitle, $dName, $dDate));

	    # ��ʸ�˹��פ���������ʸ��ɽ��
	    if ($ArticleFlag) {
		$Line =~ s/<[^>]*>//go;
		print("<blockquote>$Line</blockquote>\n");
	    }
	}
    }
    close(DB);

    # �ҥåȤ��ʤ��ä���
    print("<li>$H_NOTFOUND\n") unless ($HitFlag == 1);

    # �ꥹ���Ĥ���
    print("</ul>\n");
}


###
## �����θ���(��ʸ)
#
sub SearchArticleKeyword {

    # �ե�����̾�ȥ������
    local($File, @KeyList) = @_;
    local(@NewKeyList);
    local($Line, $Return) = ('', '');

    # ��������
    open(ARTICLE, "<$File") || &Fatal(1, $File);
    while($Line = <ARTICLE>) {

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
    &MsgHeader($ALIASNEW_MSG);

    # ������Ͽ/��Ͽ���Ƥ��ѹ�
    print(<<__EOF__);
<p>
$H_ALIASTITLE
</p>
<p>
<form action="$PROGRAM" method="POST">
<input name="c" type="hidden" value="am">
$H_ALIAS <input name="alias" type="text" value="#" size="$NAME_LENGTH"><br>
$H_FROM <input name="name" type="text" size="$NAME_LENGTH"><br>
$H_MAIL <input name="email" type="text" size="$MAIL_LENGTH"><br>
$H_URL <input name="url" type="text" value="http://" size="$URL_LENGTH"><br>
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
$H_ALIAS <input name="alias" type="text" size="$NAME_LENGTH"><br>
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
    &MsgFooter();

}


###
## ��Ͽ/�ѹ�
#
sub AliasMod {

    # �����ꥢ����̾�����᡼�롤URL
    local($A, $N, $E, $U) = @_;
    
    # �ۥ��Ȥ��ޥå�������
    #	0 ... �����ꥢ�����ޥå����ʤ�
    #	1 ... �����ꥢ���ϥޥå��������ۥ���̾���ޥå����ʤ�
    #	2 ... �ޥå����ƥǡ������ѹ�����
    local($HitFlag) = 0;
    
    # ʸ��������å�
    &AliasCheck($A, $N, $E, $U);
    
    # �����ꥢ�����ɤ߹���
    &CashAliasData($USER_ALIAS_FILE);
    
    # 1�Ԥ��ĥ����å�
    foreach $Alias (sort keys(%Name)) {
	next unless ($A eq $Alias);
	
	# �ۥ���̾����ä���2�����ʤ���1��
	$HitFlag = (($REMOTE_HOST eq $Host{$Alias}) ? 2 : 1);
    }
    
    # �ۥ���̾�����ʤ�!
    &Fatal(6, '') if ($HitFlag == 1);
    
    # �ǡ�������Ͽ
    $Name{$Alias} = $N;
    $Email{$Alias} = $E;
    $Host{$Alias} = $REMOTE_HOST;
    $URL{$Alias} = $U;
    
    # �����ꥢ���ե�����˽񤭽Ф�
    &WriteAliasData($USER_ALIAS_FILE);
    
    # ɽ�����̤κ���
    &MsgHeader($ALIASMOD_MSG);
    print("<p>$H_ALIAS <strong>$A</strong>:\n");
    if ($HitFlag == 2) {
	print("$H_ALIASCHANGED</p>\n");
    } else {
	print("$H_ALIASENTRIED</p>\n");
    }
    &MsgFooter();
    
}


###
## �����ꥢ�������å�
#
sub AliasCheck {

    local($A, $N, $E, $U) = @_;

    &CheckAlias($A);
    &CheckName($N);
    &CheckEmail($E);
    &CheckURL($U);
    
}


###
## ���
#
sub AliasDel {

    # �����ꥢ��
    local($A) = @_;

    # �ۥ��Ȥ��ޥå�������
    #	0 ... �����ꥢ�����ޥå����ʤ�
    #	1 ... �����ꥢ���ϥޥå��������ۥ���̾���ޥå����ʤ�
    #	2 ... �ޥå����ƥǡ������ѹ�����
    local($HitFlag) = 0;
    
    # �����ꥢ�����ɤ߹���
    &CashAliasData($USER_ALIAS_FILE);
    
    # 1�Ԥ��ĥ����å�
    foreach $Alias (sort keys(%Name)) {
	next unless ($A eq $Alias);
	
	# �ۥ���̾����ä���2�����ʤ���1��
	$HitFlag = (($REMOTE_HOST eq $Host{$Alias}) ? 2 : 1);
    }
    
    # �ۥ���̾�����ʤ�!
    &Fatal(6, '') if ($HitFlag == 1);
    
    # �����ꥢ�����ʤ�!
    &Fatal(7, $A) if ($HitFlag == 0);
    
    # ̾����ä�
    $Name{$A} = '';
    
    # �����ꥢ���ե�����˽񤭽Ф�
    &WriteAliasData($USER_ALIAS_FILE);
    
    # ɽ�����̤κ���
    &MsgHeader($ALIASDEL_MSG);
    print("<p>$H_ALIAS <strong>$A</strong>: $H_ALIASDELETED</p>\n");
    &MsgFooter();

}


###
## ����
#
sub AliasShow {

    # �����ꥢ�����ɤ߹���
    &CashAliasData($USER_ALIAS_FILE);
    local($Alias);
    
    # ɽ�����̤κ���
    &MsgHeader($ALIASSHOW_MSG);
    # ������ʸ
    print("<p>$H_AORI_ALIAS</p>\n");
    print("<p><a href=\"$PROGRAM?c=an\">$H_ALIASTITLE</a></p>\n");
    
    # �ꥹ�ȳ���
    print("<dl>\n");
    
    # 1�Ĥ���ɽ��
    foreach $Alias (sort keys(%Name)) {
	print(<<__EOF__);
<p>
<dt><strong>$Alias</strong>
<dd>$H_FROM $Name{$Alias}
<dd>$H_MAIL $Email{$Alias}
<dd>$H_HOST $Host{$Alias}
<dd>$H_URL $URL{$Alias}
</p>
__EOF__

    }

    # �ꥹ���Ĥ���
    print("</dl>\n");
    
    &MsgFooter();

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
    open(ALIAS, "<$File") || &Fatal(1, $File);
    while(<ALIAS>) {
	
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
    open(ALIAS, ">$TmpFile") || &Fatal(1, $TmpFile);
    foreach $Alias (sort keys(%Name)) {
	($Name{$Alias}) && printf(ALIAS "%s\t%s\t%s\t%s\t%s\n",
				  $Alias, $Name{$Alias}, $Email{$Alias},
				  $Host{$Alias}, $URL{$Alias});
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

    open(HEADER, "<$File") || &Fatal(1, $File);
    while(<HEADER>){
        print("$_");
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
    local($ArticleId) = 0;

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
## �����ֹ���äƤ���(�ֹ�������ʤ�)��
#
sub GetArticleId {

    # �ե�����̾�����
    local($ArticleNumFile) = @_;

    # �����ֹ�
    local($ArticleId);

    open(AID, "$ArticleNumFile") || &Fatal(1, $ArticleNumFile);
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
    local($BoardName);

    open(ALIAS, "<$BOARD_ALIAS_FILE")
	|| &Fatal(1, $BOARD_ALIAS_FILE);
    while(<ALIAS>) {
	
	chop;
	next unless (/^$Alias\t(.*)$/);

	$BoardName = $1;
	return($BoardName);
    }
    close(ALIAS);

    # �ҥåȤ���
    return('');
}


###
## �����ȥ�ꥹ�ȤΥե����ޥå�
#
sub GetFormattedTitle {

    local($Id, $Aids, $Icon, $Title, $Name, $Date) = @_;
    local($String, $Fnum) = ('', 0);

    # ���ʸ����
    local($Link) = "<a href=\"$PROGRAM?b=$BOARD&c=e&id=$Id\">$Title</a>";

    # �ޤȤ��ɤߥ����ʸ����
    local($Thread) = (($Aids) ? " <a href=\"$PROGRAM?b=$BOARD&c=t&id=$Id\">$H_THREAD</a>" : '');

    if (($Icon eq $H_NOICON) || (! $Icon)) {
	$String = sprintf("<strong>$Id .</strong> $Link$Thread [$Name] $Date");
    } else {
	$String = sprintf("<strong>$Id .</strong> <img src=\"%s\" alt=\"$Icon\" width=\"$ICON_WIDTH\" height=\"$ICON_HEIGHT\">$Link$Thread [$Name] $Date", &GetIconURLFromTitle($Icon));
    }

    return($String);

}


###
## �����ȥ�ꥹ�ȤΥե����ޥå�(��ά��)
#
sub GetFormattedAbstract {

    local($Id, $Icon, $Title, $Name, $Date) = @_;
    local($String) = '';

    if (($Icon eq $H_NOICON) || (! $Icon)) {
	$String = sprintf("<li><strong>$Id .</strong> $Title [$Name] $Date", &GetIconURLFromTitle($Icon));
    } else {
	$String = sprintf("<li><strong>$Id .</strong> <img src=\"%s\" alt=\"$Icon\" width=\"$ICON_WIDTH\" height=\"$ICON_HEIGHT\">$Title [$Name] $Date", &GetIconURLFromTitle($Icon));
    }

    return($String);
}


###
## �����������ɽ��
#
sub ShowFormattedLinkToFollowedArticle {

    local($Src, $Icon, $Subject) = @_;

    # ������μ���
    local($Link) = ($Src =~ /^http:/) ? $Src : "$PROGRAM?b=$BOARD&c=e&id=$Src";

    if ($Src != 0) {
	if (($Icon eq $H_NOICON) || (! $Icon)) {
	    print("<strong>$H_REPLY</strong> [$BOARDNAME: $Src] <a href=\"$Link\">$Subject</a><br>\n");
	} else {
	    printf("<strong>$H_REPLY</strong> [$BOARDNAME: $Src] <img src=\"%s\" alt=\"$Icon\" width=\"$ICON_WIDTH\" height=\"$ICON_HEIGHT\"><a href=\"$Link\">$Subject</a><br>\n", &GetIconURLFromTitle($Icon));
	}
    } elsif ($Src =~ /^http:/) {
	print("<strong>$H_REPLY</strong> <a href=\"$Link\">$Link</a><br>\n");
    }
}


###
## ʸ��������å�: �����ꥢ��
#
sub CheckAlias {

    local($String) = @_;

    # �������å�
    ($String eq '') && &Fatal(2, '');

    # `#'�ǻϤޤäƤ�?
    ($String =~ (/^#/)) || &Fatal(8, 'alias');

    # 1ʸ���������
    (length($String) > 1) || &Fatal(8, 'alias');

}


###
## ʸ��������å�: �����ȥ�
#
sub CheckSubject {

    local($String) = @_;

    # �������å�
    ($String eq '') && &Fatal(2, '');

    # ����������å�
    ($String =~ /</o) && &Fatal(4, '');

    # ���ԥ����ɤ�����å�
    ($String =~ /\n/o) && &Fatal(3, '');

}


###
## ʸ��������å�: ̾��
#
sub CheckName {

    local($String) = @_;

    # �������å�
    ($String eq '') && &Fatal(2, '');

    # ���ԥ����ɤ�����å�
    ($String =~ /\n/o) && &Fatal(3, '');

}


###
## ʸ��������å�: �᡼��
#
sub CheckEmail {

    local($String) = @_;

    # �������å�
    ($String eq '') && &Fatal(2, '');

    # `@'�����äƤʤ��㥢����
    ($String =~ (/@/)) || &Fatal(8, 'E-Mail');

    # ���ԥ����ɤ�����å�
    ($String =~ /\n/o) && &Fatal(3, '');

}


###
## ʸ��������å�: URL
#
sub CheckURL {

    local($String) = @_;

    ($String =~ m#^http://.*$#) || ($String =~ m#^http://$#)
	|| ($String eq '') || &Fatal(8, 'URL');

}


###
## �����Υإå���ɽ��
#
sub MsgHeader {

    # message and board
    local($Message) = @_;
    
    &cgi'header;
    print(<<__EOF__);
<html>
<head>
<!--� (0xF0A1): cool idea to euc decode error protection; thanks to faichan\@kt.rim.or.jp-->
<title>$Message</title>
<base href="http://$SERVER_NAME:$SERVER_PORT$SYSDIR_NAME">
</head>
<body bgcolor="$BG_COLOR" TEXT="$TEXT_COLOR" LINK="$LINK_COLOR" ALINK="$ALINK_COLOR" VLINK="$VLINK_COLOR">
<h1>$Message</h1>
<hr>
__EOF__

}


###
## �����Υեå���ɽ��
#
sub MsgFooter {

    print(<<__EOF__);
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

    local($TimeOut) = 0;
    local($Flag) = 0;

    srand(time|$$);

    open(LOCKORG, ">$LOCK_ORG") || &Fatal(1, $LOCK_ORG);
    close(LOCKORG);

    for($TimeOut = 0; $TimeOut < $LOCK_WAIT; $TimeOut++) {
	$Flag = 1, last if link($LOCK_ORG, $LOCK_FILE);
	select(undef, undef, undef, (rand(6)+5)/10);
    }

    unlink($LOCK_ORG);
    &Fatal(999, $TimeOut) unless ($Flag);

}

# �����å�
sub unlock {
    unlink($LOCK_FILE);
}


###
## ��������ɽ��
#
sub ViewOriginalArticle {

    # Id�����ޥ�ɤ�ɽ�����뤫�ݤ�
    local($Id, $Flag) = @_;

    # ���Ѥ���ե�����
    local($QuoteFile) = &GetArticleFileName($Id, $BOARD);

    # ���ѵ����ξ���
    local($rFid, $rAids, $rDate, $rSubject, $rIcon, $rRemoteHost, $rName, $rEmail, $rUrl, $rFmail);

    # ��������μ���
    local($Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail) = &GetArticlesInfo($Id);

    # ���ѵ�����������
    ($rFid, $rAids, $rDate, $rSubject, $rIcon, $rRemoteHost, $rName, $rEmail, $rUrl, $rFmail) = &GetArticlesInfo($Fid) if ($Fid != 0);

    # ���ޥ��ɽ��?
    if ($Flag && $SYS_COMMAND) {

	print(<<__EOF__);
<p>
<a href="$PROGRAM?b=$BOARD&c=f&id=$Id"><img src="$ICON_FOLLOW" alt="$H_REPLYTHISARTICLE" width="$ICON_WIDTH" height="$ICON_HEIGHT" BORDER="0"></a>
<a href="$PROGRAM?b=$BOARD&c=q&id=$Id"><img src="$ICON_QUOTE" alt="$H_REPLYTHISARTICLEQUOTE" width="$ICON_WIDTH" height="$ICON_HEIGHT" BORDER="0"></a>
<a href="$PROGRAM?b=$BOARD&c=t&id=$Id"><img src="$ICON_THREAD" alt="$H_READREPLYALL" width="$ICON_WIDTH" height="$ICON_HEIGHT" BORDER="0"></a>
<a href="$PROGRAM?b=$BOARD&c=i&type=article"><img src="$ICON_HELP" alt="?" width="$ICON_WIDTH" height="$ICON_HEIGHT" BORDER="0"></a>
</p>
__EOF__

    }

    # �ܡ���̾�ȵ����ֹ桤��
    if (($Icon eq $H_NOICON) || (! $Icon)) {
	print("<strong>$H_SUBJECT</strong> [$BOARDNAME: $Id] $Subject<br>\n");
    } else {
	printf("<strong>$H_SUBJECT</strong> [$BOARDNAME: $Id] <img src=\"%s\" alt=\"$Icon\" width=\"$ICON_WIDTH\" height=\"$ICON_HEIGHT\">$Subject<br>\n", &GetIconURLFromTitle($Icon));
    }

    # ��̾��
    if ((! $Url) || ($Url eq 'http://')) {
        # URL���ʤ����
        print("<strong>$H_FROM</strong> $Name<br>\n");
    } else {
        # URL��������
        print("<strong>$H_FROM</strong> <a href=\"$Url\">$Name</a><br>\n");
    }

    # �᡼��
    print("<strong>$H_MAIL</strong> <a href=\"mailto:$Email\">&lt;$Email&gt;</a><br>\n");

    # �ޥ���
    print("<strong>$H_HOST</strong> $RemoteHost<br>\n") if $SYS_SHOWHOST;

    # �����
    print("<strong>$H_DATE</strong> $Date<br>\n");

    # ȿ����(���Ѥξ��)
    &ShowFormattedLinkToFollowedArticle($Fid, $rIcon, $rSubject);

    # �ڤ���
    print("$H_LINE<br>\n");

    # ���������
    open(TMP, "<$QuoteFile") || &Fatal(1, $QuoteFile);
    while(<TMP>) { print("$_"); }
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
    # (MacPerl�Ǥϡ�:$Borad:$Id�פȤ��٤��餷��)
    return(($Board) ? "$Board/$Id" : "$Id");

}


###
## �ܡ���̾�Τȥե�����̾���顤���Υե�����Υѥ�̾����Ф���
#
sub GetPath {

    # Board��File
    local($Board, $File) = @_;

    # �֤�(MacPerl�Ǥϡ�:$Board:$File�פȤ��٤��餷��)
    return("$Board/$File");

}


###
## ��������ե�����̾���顤���Υե�����Υѥ�̾����Ф���
#
sub GetIconPath {

    # Board��File
    local($File) = @_;

    # �֤�(MacPerl�Ǥϡ�:$ICON_DIR:$File�פȤ��٤��餷��)
    return("$ICON_DIR/$File");

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

    local($FileName, $Title, $TargetFile) = ('', '', '');

    # ��İ��ɽ��
    open(ICON, &GetIconPath("$BOARD.$ICONDEF_POSTFIX"))
	|| (open(ICON, &GetIconPath("$DEFAULT_ICONDEF"))
	    || &Fatal(1, &GetIconPath("$DEFAULT_ICONDEF")));
    while(<ICON>) {
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

    # DB�ե�����
    local($DBFile) = &GetPath($BOARD, $DB_FILE_NAME);

    local($dId, $dFid, $dAids, $dDate, $dTitle, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail);

    local($rFid, $rAids, $rDate, $rTitle, $rIcon, $rRemoteHost, $rName, $rEmail, $rUrl, $rFmail) = ('', '', '', '', '', '', '', '', '', '');

    # �����ߡ�DB�ե����뤬�ʤ����0/''���֤���
    open(DB, "<$DBFile");
    while(<DB>) {

	next if (/^\#/);
	next if (/^$/);
	chop;

	($dId, $dFid, $dAids, $dDate, $dTitle, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail) = split(/\t/, $_);

	if ($Id == $dId) {
	    $rFid = $dFid;
	    $rAids = $dAids;
	    $rDate = $dDate;
	    $rTitle = $dTitle;
	    $rIcon = $dIcon;
	    $rRemoteHost = $dRemoteHost;
	    $rName = $dName;
	    $rEmail = $dEmail;
	    $rUrl = $dUrl;
	    $rFmail = $dFmail;
	}    
    }
    close(DB);

    return($rFid, $rAids, $rDate, $rTitle, $rIcon, $rRemoteHost, $rName, $rEmail, $rUrl, $rFmail);

}


###
## ���顼ɽ��
#
sub Fatal {

    # ���顼�ֹ�ȥ��顼����μ���
    local($FatalNo, $FatalInfo) = @_;

    # �۾ｪλ�β�ǽ��������Τǡ��Ȥꤢ����lock�򳰤�
    # (��å��μ��Ԥλ��ʳ�)
    &unlock if ($FatalNo != 999);

    &MsgHeader($ERROR_MSG);
    
    if ($FatalNo == 1) {

	print("<p>
File: $FatalInfo��¸�ߤ��ʤ���
���뤤��permission�����꤬�ְ�äƤ��ޤ���
������Ǥ�����<a href=\"mailto:$MAINT\">$MAINT</a>�ޤǡ�
�嵭�ե�����̾���Τ餻��������
</p>\n");

    } elsif ($FatalNo == 2) {

	print("<p>
���Ϥ���Ƥ��ʤ����ܤ�����ޤ�����äƤ⤦���٤��ľ���ƤߤƤ���������
</p>\n");

    } elsif ($FatalNo == 3) {

	print("<p>
���̾�����᡼�륢�ɥ쥹�ˡ����Ԥ����äƤ��ޤäƤ��ޤ���
��äƤ⤦���٤��ľ���ƤߤƤ���������
</p>\n");

    } elsif ($FatalNo == 4) {

	print("<p>
�����HTML����������뤳�Ȥ϶ؤ����Ƥ��ޤ���
��äư㤦��˽񤭴����Ƥ���������
</p>\n");

    } elsif ($FatalNo == 6) {

	print("<p>
��Ͽ����Ƥ��륨���ꥢ���Τ�Τȡ��ۥ���̾�����פ��ޤ���
������Ǥ�����<a href=\"mailto:$MAINT\">$MAINT</a>�ޤǸ�Ϣ����������
</p>\n");

    } elsif ($FatalNo == 7) {

	print("<p>
$FatalInfo�Ȥ��������ꥢ���ϡ���Ͽ����Ƥ��ޤ���
</p>\n");

    } elsif ($FatalNo == 8) {

	print("<p>
$FatalInfo��������������ޤ���? ��äƤ⤦���٤��ľ���ƤߤƤ���������
</p>\n");

    } elsif ($FatalNo == 9) {

	print("<p>
�᡼�뤬�����Ǥ��ޤ���Ǥ�����������Ǥ��������Υ��顼��������������
<a href=\"mailto:$MAINT\">$MAINT</a>�ޤǤ��Τ餻����������
</p>\n");

    } elsif ($FatalNo == 11) {

	print("<p>
���ε����Ϥޤ���Ƥ���Ƥ��ޤ���
</p>\n");

    } elsif ($FatalNo == 999) {

	print("<p>
�����ƥ�Υ�å��˼��Ԥ��ޤ�����
���߹�äƤ���褦�Ǥ��Τǡ����Ф餯�ԤäƤ���⤦���٥����������Ƥ���������
</p>\n");

    } else {

	print("<p>
���顼�ֹ�����: ������Ǥ��������Υ��顼��������������
<a href=\"mailto:$MAINT\">$MAINT</a>�ޤǤ��Τ餻����������
</p>\n");

    }
    
    &MsgFooter();
    exit 0;
}
