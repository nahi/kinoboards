#!/usr/local/bin/perl
#
# $Id: kb.cgi,v 4.8 1996-04-30 17:40:18 nakahiro Exp $


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
$CGIDIR_NAME = $1;
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
# default http port
#
$DEFAULT_HTTP_PORT = 80;

#
# ���ɽ��
#
$ADDRESS = "KINOBOARDS: Copyright (C) 1995, 96 <a href=\"http://www.kinotrope.co.jp/~nakahiro/\">NAKAMURA Hiroshi</a>.";

#
# �ե�����
#
# �����ֹ�ե�����
$ARTICLE_NUM_FILE_NAME = ".articleid";
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
# prefix of quote file.
#
$QUOTE_PREFIX = ".q";

#
# ��������ǥ��쥯�ȥ�
# (��������ȥ�����������ե�����������ǥ��쥯�ȥ�̾)
#
$ICON_DIR = "icons";

#
# ������������ե�����Υݥ��ȥե�����
# ������������ե����롢��(�ܡ��ɥǥ��쥯�ȥ�̾).(���ꤷ��ʸ����)�פˤʤ롣
#
$ICONDEF_POSTFIX = "idef";

#
# �����ѥ�����ʸ
#
$COM_ARTICLE_BEGIN = "<!-- Article Begin -->";
$COM_ARTICLE_END = "<!-- Article End -->";
$COM_FMAIL_BEGIN = "<!-- Follow Mail Begin";
$COM_FMAIL_END = "Follow Mail End -->";

#
# Permission of Title File.
#
$TITLE_FILE_PERMISSION = "0666";

#
# ��å��Υ�����
#
$LOCK_SH = 1;
$LOCK_EX = 2;
$LOCK_NB = 4;
$LOCK_UN = 8;

#
# ���ѥե饰
#
$QUOTE_ON = 1;
$NO_QUOTE = 0;

#
# ���ԥޡ���
#
$NULL_LINE = "__br__";

#
# ���֥륯������
#
$DOUBLE_QUOTE = "__dq__";
$GREATER_THAN = '__gt__';
$LESSER_THAN = '__lt__';
$AND_MARK = '__amp__';


###
## �ᥤ��
#

# ���ޥ��ʬ��:			c=m

# ������ɽ��(�����Τ�):		c=e&id={[1-9][0-9]*}
# ���ε�����ɽ��(�����Τ�):	c=en&id={[1-9][0-9]*}
# ������ɽ��(ȿ����ޤȤ��):	c=t&id={[1-9][0-9]*}

# �������:			c=n
# ���ѤĤ��ե���:		c=q&id={[1-9][0-9]*}
# ���Ѥʤ��ե���:		c=f&id={[1-9][0-9]*}
# URL���ѥե���:		c=q/f&url={URL}
# �����Υץ�ӥ塼:		c=p&(��)....
# ��ǧ�Ѥ߲���:			c=x&id={[1-9][0-9]*(���ѤǤʤ���id=0)}

# �����ȥ�ꥹ��(thread):	c=v&num={[1-9][0-9]*}
# �����ȥ�ꥹ��(����):		c=r&num={[1-9][0-9]*}
# �ǿ��ε���:			c=l&num={[1-9][0-9]*}

# �����θ���:			c=s
# ��������ɽ��:			c=i

# �����ꥢ����Ͽ����:		c=an
# �����ꥢ����Ͽ:		c=am&alias=..&name=..&email=..&url=..
# �����ꥢ�����:		c=ad&alias=...
# �����ꥢ������:		c=as

MAIN: {

    # ɸ������(POST)�ޤ��ϴĶ��ѿ�(GET)�Υǥ����ɡ�
    &cgi'decode;

    # ���ˤ˻Ȥ��Τ�����ѿ�
    $BOARD = $cgi'TAGS{'b'};

    # �Ǽ��ĸ�ͭ���åƥ��󥰤��ɤ߹���
    require("$BOARD/$CONF_FILE_NAME") if (-s "$BOARD/$CONF_FILE_NAME");

    # �ͤ����
    local($Command) = $cgi'TAGS{'c'};
    local($Com) = $cgi'TAGS{'com'};
    local($Id) = $cgi'TAGS{'id'};
    local($Num) = $cgi'TAGS{'num'};
    local($Alias) = $cgi'TAGS{'alias'};
    local($Name) = $cgi'TAGS{'name'};
    local($Email) = $cgi'TAGS{'email'};
    local($URL) = $cgi'TAGS{'url'};

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
	$Id ? &Entry($NO_QUOTE, $Id) : &URLEntry($NO_QUOTE, $URL);
    } elsif (($Command eq "q")
	     || (($Command eq "m") && ($Com eq $H_REPLYTHISARTICLEQUOTE))) {
	$Id ? &Entry($QUOTE_ON, $Id) : &URLEntry($QUOTE_ON, $URL);
    } elsif (($Command eq "p") && ($Com ne "x")) {
	&Preview();
    } elsif (($Command eq "x")
	     || (($Command eq "p") && ($Com eq "x"))) {
	&Thanks();

    } elsif ($Command eq "v") {
	&ViewTitle($Num);
    } elsif ($Command eq "r") {
	&SortArticle($Num);
    } elsif ($Command eq "l") {
	&NewArticle($Num);

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

}


###
## �����ޤ�
#
exit 0;


#/////////////////////////////////////////////////////////////////////
# �񤭹��߲��̴�Ϣ


###
## �񤭹��߲���
#
sub Entry {

    # ���Ѥ���/�ʤ��ȡ����Ѥ�����Ϥ���Id(���Ѥ��ʤ�����0)
    local($QuoteFlag, $Id) = @_;

    # Board̾�Τμ���
    local($BoardName) = &GetBoardInfo($BOARD);

    # ɽ�����̤κ���
    &MsgHeader("$BoardName: $ENTRY_MSG");

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

    # Board̾�Τμ���
    local($BoardName) = &GetBoardInfo($BOARD);

    # ����«
    print("<form action=\"$PROGRAM\" method=\"POST\">\n");
    print("<input name=\"c\" type=\"hidden\" value=\"p\">\n");
    print("<input name=\"b\" type=\"hidden\" value=\"$BOARD\">\n");
    
    # ����Id; ���ѤǤʤ��ʤ�0��
    print("<input name=\"id\" type=\"hidden\" value=\"$Id\">\n");

    # ������ʸ
    print("<p>$H_AORI</p>\n");

    # Board̾
    print("$H_BOARD $BoardName<br>\n");

    # �������������
    if ($SYS_ICON) {
	print("$H_ICON\n");
	print("<SELECT NAME=\"icon\">\n");
	print("<OPTION SELECTED>$H_NOICON\n");

	# ��İ��ɽ��
	open(ICON, "$ICON_DIR/$BOARD.$ICONDEF_POSTFIX")
	    || (open(ICON, "$ICON_DIR/$DEFAULT_ICONDEF")
		|| &MyFatal(1, "$ICON_DIR/$DEFAULT_ICONDEF"));
	while(<ICON>) {
	    chop;
	    ($FileName, $Title) = split(/\t/, $_, 2);
	    print("<OPTION>$Title\n");
	}
	close(ICON);
	print("</SELECT>\n");
	print("(<a href=\"$PROGRAM?b=$BOARD&c=i\">$H_SEEICON</a>)<BR>\n");
    }

    # Subject(�ե����ʤ鼫ưŪ��ʸ����������)
    printf("%s <input name=\"subject\" type=\"text\" value=\"%s\" size=\"%s\"><br>\n",
	   $H_SUBJECT, $Subject, $SUBJECT_LENGTH);

    # TextType
    if ($SYS_TEXTTYPE) {
	print("$H_TEXTTYPE\n");
	print("<SELECT NAME=\"texttype\">\n");
	print("<OPTION SELECTED>$H_PRE\n");
	print("<OPTION>$H_HTML\n");
	print("</SELECT><BR>\n");
    }

}


###
## �եå���ʬ��ɽ��
#
sub EntryFooter {

    # ̾���ȥ᡼�륢�ɥ쥹��URL��
    print("$H_FROM <input name=\"name\" type=\"text\" size=\"$NAME_LENGTH\"><br>\n");
    print("$H_MAIL <input name=\"mail\" type=\"text\" size=\"$MAIL_LENGTH\"><br>\n");
    print("$H_URL <input name=\"url\" type=\"text\" value=\"http://\" size=\"$URL_LENGTH\"><br>\n");
    print("$H_FMAIL <input name=\"fmail\" type=\"checkbox\" value=\"on\"><br>\n")
	if ($SYS_FOLLOWMAIL);
    
    if ($SYS_ALIAS) {
	print("<p>$H_ALIASINFO\n");
	print("(<a href=\"$PROGRAM?c=as\">$H_SEEALIAS</a> // \n");
	print("<a href=\"$PROGRAM?c=an\">$H_ALIASENTRY</a>)</p>\n");
    }

    # �ܥ���
    print("<p>\n");
    print("<input type=\"radio\" name=\"com\" value=\"p\" CHECKED>: $H_PREVIEW<br>\n");
    print("<input type=\"radio\" name=\"com\" value=\"x\">: $H_ENTRY<br>\n");
    print("<input type=\"submit\" value=\"$H_PUSHHERE\">\n");
    print("</p>\n");

    # ����«
    print("</form>\n");

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

    # �ե�����򳫤�
    open(TMP, "<$QuoteFile") || &MyFatal(1, $QuoteFile);
    while(<TMP>) {

	# ���ѤΤ�����Ѵ�
	s/&/&amp;/go;
	s/\"//go;
	if ($SYS_TAGINQUOTE) {
	    s/<//go;
	    s/>//go;
	} else {
	    s/<[^>]*>//go;
	}

	# ����ʸ�����ɽ��
	print($DEFAULT_QMARK, $_);
	
    }

    # �Ĥ���
    close(TMP);

}


#/////////////////////////////////////////////////////////////////////
# �ץ�ӥ塼���̴�Ϣ


###
## �ץ�ӥ塼����
#
sub Preview {

    # Board̾�Τμ���
    local($BoardName) = &GetBoardInfo($BOARD);

    # ���Ϥ��줿��������
    local($Id, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article,
	  $File, $Qurl, $Fmail)
	= ($cgi'TAGS{'id'}, $cgi'TAGS{'texttype'}, $cgi'TAGS{'name'},
	   $cgi'TAGS{'mail'}, $cgi'TAGS{'url'}, $cgi'TAGS{'icon'},
	   $cgi'TAGS{'subject'}, $cgi'TAGS{'article'}, $cgi'TAGS{'file'},
	   $cgi'TAGS{'qurl'}, $cgi'TAGS{'fmail'});

    # ���ѵ�����URL
    local($rFile) = '';

    # ���ѵ����ε�������
    local($rFid, $rAids, $rDate, $rSubject, $rIcon, $rRemoteHost, $rName,
	  $rEmail, $rUrl, $rFmail) = ('', '', '', '', '', '', '', '', '', '');

    # �⤷���Ѥʤ�ġġ�
    if ($File) {

	# local file����ΰ��Ѥʤ�ġ�
        $rFile = $File;
        $rSubject = &GetSubjectFromFile($File);

    } elsif ($Id) {

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
    print("<form action=\"$PROGRAM\" method=\"POST\">\n");
    print("<input name=\"c\"        type=\"hidden\" value=\"x\">\n");
    print("<input name=\"b\"        type=\"hidden\" value=\"$BOARD\">\n");
    print("<input name=\"id\"       type=\"hidden\" value=\"$Id\">\n");
    print("<input name=\"texttype\" type=\"hidden\" value=\"$TextType\">\n");
    print("<input name=\"name\"     type=\"hidden\" value=\"$Name\">\n");
    print("<input name=\"mail\"     type=\"hidden\" value=\"$Email\">\n");
    print("<input name=\"url\"      type=\"hidden\" value=\"$Url\">\n");
    print("<input name=\"icon\"     type=\"hidden\" value=\"$Icon\">\n");
    print("<input name=\"subject\"  type=\"hidden\" value=\"$Subject\">\n");
    print("<input name=\"article\"  type=\"hidden\" value=\"$Article\">\n");
    print("<input name=\"file\"     type=\"hidden\" value=\"$File\">\n");
    print("<input name=\"qurl\"     type=\"hidden\" value=\"$Qurl\">\n");
    print("<input name=\"fmail\"    type=\"hidden\" value=\"$Fmail\">\n");

    # ������ʸ
    print("<p>$H_POSTINFO");
    print("<input type=\"submit\" value=\"$H_PUSHHERE\"></p>\n");

    # ��
    (($Icon eq $H_NOICON) || (! $Icon))
        ? print("<strong>$H_SUBJECT</strong> $Subject<br>\n")
            : printf("<strong>$H_SUBJECT</strong> <img src=\"%s\" alt=\"$Icon\"> $Subject<br>\n", &GetIconURL($Icon));

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
	&MyFatal(7, $Name) if ($Tmp eq '');
	$Name = $Tmp;
    }

    # �������å�
    &MyFatal(2, '') if ($Subject eq '') || ($Article eq '') || ($Name eq '')
	|| ($Email eq '');

    # ʸ��������å�
    &CheckName($Name);
    &CheckEmail($Email);
    &CheckURL($Url);

    # ���֥������ȤΥ��������å�
    $_ = $Subject;
    &MyFatal(4, '') if (/</);

    # ��������Υ����å�; ������������̵���פ����ꡣ
    $Icon = $H_NOICON unless (&GetIconURL($Icon));

    # �������"�򥨥󥳡���
    $Article = &DQEncode($Article);

    # ̾����e-mail��URL���֤���
    return($Name, $Email, $Url, $Icon, $Article);
}


#/////////////////////////////////////////////////////////////////////
# ��Ͽ����̴�Ϣ


###
## ��Ͽ�����
#
sub Thanks {

    # �����˵�������������
    &MakeNewArticle();

    # ɽ�����̤κ���
    &MsgHeader($THANKS_MSG);

    print("<p>$H_THANKSMSG</p>");
    print("<form action=\"$PROGRAM\" method=\"POST\">\n");
    print("<input name=\"b\" type=\"hidden\" value=\"$BOARD\">\n");
    print("<input name=\"c\" type=\"hidden\" value=\"v\">\n");
    print("<input name=\"num\" type=\"hidden\" value=\"40\">\n");
    print("<input type=\"submit\" value=\"$H_BACK\">\n");
    print("</form>\n");

    &MsgFooter();
}


###
## ��������Ƥ��줿����������
#
sub MakeNewArticle {

    # Board̾�Τμ���
    local($BoardName) = &GetBoardInfo($BOARD);

    # ���դ���Ф���
    local($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst)
	= localtime(time);
    local($InputDate) = sprintf("%d/%d(%02d:%02d)",
				$mon + 1, $mday, $hour, $min);

    # ���Ϥ��줿��������
    local($Id, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article,
	  $File, $Qurl, $Fmail)
	= ($cgi'TAGS{'id'}, $cgi'TAGS{'texttype'}, $cgi'TAGS{'name'},
	   $cgi'TAGS{'mail'}, $cgi'TAGS{'url'}, $cgi'TAGS{'icon'},
	   $cgi'TAGS{'subject'}, $cgi'TAGS{'article'}, $cgi'TAGS{'file'},
	   $cgi'TAGS{'qurl'}, $cgi'TAGS{'fmail'});

    # ���Ϥ��줿��������Υ����å�
    ($Name, $Email, $Url, $Icon, $Article)
	= &CheckArticle($Name, $Email, $Url, $Subject, $Icon, $Article);

    # ��å��򤫤���
    &lock();

    # �����������ֹ�����(�ޤ������ֹ�������Ƥʤ�)
    local($ArticleId) = &GetNewArticleId();

    # �����Υե�����κ���
    &MakeArticleFile($TextType, $Article, $ArticleId);

    # DB�ե��������Ƥ��줿�������ɲ�
    if ($File) {

	# URL���Ѥʤ�URL
	&AddDBFile($ArticleId, $Qurl, $InputDate, $Subject, $Icon,
		   $REMOTE_HOST, $Name, $Email, $Url, $Fmail);

    } else {

	# �̾�ε������Ѥʤ�ID
	&AddDBFile($ArticleId, $Id, $InputDate, $Subject, $Icon,
		   $REMOTE_HOST, $Name, $Email, $Url, $Fmail);

    }

    # �����������ֹ��񤭹���
    &AddArticleId();

    # ��å��򳰤���
    &unlock();

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
    open(TMP, ">$File") || &MyFatal(1, $File);

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
    local($ArticleNumFile) = &GetPath($BOARD, $ARTICLE_NUM_FILE_NAME);

    # �����������ֹ�
    local($ArticleId) = &GetNewArticleId();

    # �񤭹��ࡣ
    open(AID, ">$ArticleNumFile") || &MyFatal(1, $ArticleNumFile);
    print(AID $ArticleId, "\n");
    close(AID);

}


###
## DB�ե�����˽񤭹���
#
sub AddDBFile {

    # ����Id��̾�������������ꡢ����
    local($Id, $Fid, $InputDate, $Subject, $Icon,
	  $RemoteHost, $Name, $Email, $Url, $Fmail) = @_;
    local($dId, $dFid, $dAids, $dInputDate, $dSubject, $dIcon,
	  $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail)
		   = ('', '', '', '', '', '', '', '', '', '', ());
    
    # ��Ͽ�ե�����
    local($File) = &GetPath($BOARD, $DB_FILE_NAME);
    local($TmpFile) = &GetPath($BOARD, $DB_TMP_FILE_NAME);

    # Open Tmp File
    open(DBTMP, ">$TmpFile") || &MyFatal(1, $TmpFile);
    # Open DB File
    open(DB, "<$File") || &MyFatal(1, $File);

    while(<DB>) {

	printf(DBTMP "$_"), next if (/^\#/);
	chop;

	($dId, $dFid, $dAids, $dInputDate, $dSubject, $dIcon,
	 $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail) = split(/\t/, $_);
	
	# �ե����赭�������Ĥ��ä��顢
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

    # �����������Υǡ�����񤭲ä��롣
    printf(DBTMP "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n",
	   $Id, $Fid, '', $InputDate, $Subject, $Icon,
	   $RemoteHost, $Name, $Email, $Url, $Fmail);

    # close Files.
    close(DB);
    close(DBTMP);

    # DB�򹹿�����
    rename($TmpFile, $File);

}


#/////////////////////////////////////////////////////////////////////
# ����ɽ����Ϣ


###
## ñ��ε�����ɽ����
#
sub ShowArticle {

    # ������Id�����
    local($Id) = @_;

    # �����Υե�����̾�����
    local($File) = &GetArticleFileName($Id, $BOARD);

    # Board̾�Τμ���
    local($BoardName) = &GetBoardInfo($BOARD);

    # ���ѵ����ξ���
    local($rFid, $rAids, $rDate, $rSubject, $rIcon, $rRemoteHost, $rName,
	  $rEmail, $rUrl, $rFmail) = ('', '', '', '', '', '', '', '', '', '');

    # ȿ�������ξ���
    local($aFid, $aAids, $aDate, $aSubject, $aIcon, $aRemoteHost, $aName,
	  $aEmail, $aUrl, $aFmail) = ('', '', '', '', '', '', '', '', '', '');

    # ��������μ���
    local($Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $Email,
	  $Url, $Fmail) = &GetArticlesInfo($Id);
    local(@AidList) = split(/,/, $Aids);
    local($Aid) = '';

    # ̤��Ƶ������ɤ�ʤ�
    &MyFatal(11, '') unless ($Name);

    # ���ѵ�����������
    ($rFid, $rAids, $rDate, $rSubject, $rIcon, $rRemoteHost, $rName, $rEmail,
     $rUrl, $rFmail) = &GetArticlesInfo($Fid) if ($Fid != 0);

    # ɽ�����̤κ���
    &MsgHeader("[$BoardName: $Id] $Subject");

    # ����«
    print("<form action=\"$PROGRAM\" method=\"POST\">\n");
    print("<input name=\"c\" type=\"hidden\" value=\"m\">\n");
    print("<input name=\"b\" type=\"hidden\" value=\"$BOARD\">\n");
    print("<input name=\"id\" type=\"hidden\" value=\"$Id\">\n");

    # ���ޥ����ʬ��ɽ��
    print("<p>\n");
    print("<a href=\"$PROGRAM?b=$BOARD&c=v&num=40\">$H_TITLELIST</a> // \n");
    print("<a href=\"$PROGRAM?b=$BOARD&c=en&id=$Id\">$H_NEXTARTICLE</a> // \n");
    print("<a href=\"$PROGRAM?b=$BOARD&c=n\">$H_POSTNEWARTICLE</a> // \n");
    print("<a href=\"$PROGRAM?b=$BOARD&c=f&id=$Id\">$H_REPLYTHISARTICLE</a> // \n");
    print("<a href=\"$PROGRAM?b=$BOARD&c=q&id=$Id\">$H_REPLYTHISARTICLEQUOTE</a> // \n");
    print("<a href=\"$PROGRAM?b=$BOARD&c=t&id=$Id\">$H_READREPLYALL</a>\n");
    print("</p>\n");

    # �ܡ���̾�ȵ����ֹ桢��
    if (($Icon eq $H_NOICON) || (! $Icon)) {
	print("<strong>$H_SUBJECT</strong> [$BoardName: $Id] $Subject<br>\n");
    } else {
	printf("<strong>$H_SUBJECT</strong> [$BoardName: $Id] <img src=\"%s\" alt=\"$Icon\">$Subject<br>\n", &GetIconURL($Icon));
    }

    # ��̾��
    if (! $Url) {
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
    open(TMP, "<$File") || &MyFatal(1, $File);
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
	    printf("%s\n", &GetFormattedTitle($Aid, $aIcon, $aSubject, $aName, $aDate));
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

    # Board̾�Τμ���
    local($BoardName) = &GetBoardInfo($BOARD);

    # ɽ�����̤κ���
    &MsgHeader("$BoardName: $THREADARTICLE_MSG");

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
## �Ƶ�Ū�ˤ��ε����Υե�����ɽ�����롣
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
    local($dId, $dFid, $dAids, $dDate, $dTitle, $dIcon, $dRemoteHost, $dName,
	  $dEmail, $dUrl, $dFmail)
	= (0, '', '', '', '', '', '', '', '', '', '');

    # lock�򤫤���
    &lock();

    # ������
    open(DB, "<$DBFile") || &MyFatal(1, $DBFile);
    while(<DB>) {

	next if (/^\#/);
	chop;

	($dId, $dFid, $dAids, $dDate, $dTitle, $dIcon, $dRemoteHost, $dName,
	 $dEmail, $dUrl, $dFmail) = split(/\t/, $_);

	# ���Ĥ��ä�!
	@Result = split(/,/, $dAids) if ($Id == $dId);

    }
    close(DB);

    # lock��Ϥ���
    &unlock();

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
    local($dFid, $dAids, $dDate, $dSubject, $dIcon, $dRemoteHost, $dName,
	  $dEmail, $dUrl, $dFmail) = &GetArticlesInfo($Id);

    printf("%s\n",
	   &GetFormattedAbstract($Id, $dIcon, $dSubject, $dName, $dDate));

}


###
## �桼�������ꥢ������桼����̾�����᡼�롢URL���äƤ��롣
#
sub GetUserInfo {

    # �������륨���ꥢ��̾
    local($Alias) = @_;

    # �����ꥢ����̾�����᡼�롢�ۥ��ȡ�URL
    local($A, $N, $E, $H, $U);

    # �����ꥢ����̾�����᡼�롢�ۥ��ȡ�URL
    local($rN, $rE, $rU) = ('', '', '');

    # lock�򤫤���
    &lock();

    # �ե�����򳫤�
    open(ALIAS, "<$USER_ALIAS_FILE") || &MyFatal(1, $USER_ALIAS_FILE);
    
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

    # lock��Ϥ���
    &unlock();
    
    # ����ˤ����֤�
    return($rN, $rE, $rU);
}


###
## ȿ�������ä����Ȥ�᡼�뤹�롣
#
sub FollowMail {

    # ���褤����
    local($To, $Name, $Date, $Subject, $Id, $Fname, $Fsubject, $Fid) = @_;

    local($BoardName) = &GetBoardInfo($BOARD);
    local($URL) = "$SCRIPT_URL?b=$BOARD&c=e&id=$Id";
    local($FURL) = "$SCRIPT_URL?b=$BOARD&c=e&id=$Fid";
    
    # Subject
    local($MailSubject) = "The article was followed.";

    # Message
    local($Message) = "$SYSTEM_NAME����Τ��Τ餻�Ǥ���\n\n$Date�ˡ�$BoardName�פ��Ф��ơ�$Name�פ��󤬽񤤤���\n��$Subject��\n$URL\n���Ф��ơ�\n��$Fname�פ��󤫤�\n��$Fsubject�פȤ�����Ǥ�ȿ��������ޤ�����\n\n�����֤Τ������\n$FURL\n�������������\n\n�Ǥϼ��餷�ޤ���";

    # �᡼������
    &SendMail($MailSubject, $Message, $To);
}


###
## ����ե����뤫��Title���äƤ���
#
sub GetSubjectFromFile {

    # �ե�����
    local($File) = @_;

    # ���Ф���Subject
    local($Title) = '';

    open(TMP, "<$File") || &MyFatal(1, $File);
    while(<TMP>) {
	
	# �������Ѵ�
	&jcode'convert(*_, 'euc');

	if (/<title>(.*)<\/title>/i) {
	    $Title = $1;
	}
    }
    close(TMP);
    
    # �֤���
    return($Title);

}


###
## �᡼������
#
sub SendMail {

    # subject���᡼��Υե�����̾������
    local($Subject, $Message, $To) = @_;

    # �᡼���ѥե�����򳫤�
    open(MAIL, "| $MAIL2") || &MyFatal(9, '');

    # To�إå�
    $_ = $To;
    &jcode'convert(*_, 'jis');
    print(MAIL "To: $_\n");
    
    # From�إå���Errors-To�إå�
    $_ = $MAINT;
    &jcode'convert(*_, 'jis');
    print(MAIL "From: $_\n");
    print(MAIL "Errors-To: $_\n");

    # Subject�إå�
    $_ = $Subject;
    &jcode'convert(*_, 'jis');
    print(MAIL "Subject: $_\n\n");

    # ��ʸ
    $_ = $Message;
    &jcode'convert(*_, 'jis');
    print(MAIL "$_\n");

    # ��������
    close(MAIL);

}


#/////////////////////////////////////////////////////////////////////
# URL���Ѵ�Ϣ


###
## �񤭹��߲���(URL)
#
sub URLEntry {

    # ���Ѥ���/�ʤ��ȡ�URL
    local($QuoteFlag, $Url) = @_;

    # Board̾�Τμ���
    local($BoardName) = &GetBoardInfo($BOARD);

    # file
    local($File) = &GetPath($BOARD, "$QUOTE_PREFIX.$$");
    local($Server, $HttpPort, $Resource, $Name) = ('', '', '', '');
    local($PlainURL) = '';

    # split
    $Name = (($PlainURL = $Url) =~ s/\#(.*)$//o) ? $1 : '';

    if ($PlainURL =~ m!http://([^:]*):([0-9]*)(/.*)$!io) {
	$Server = $1;
	$HttpPort = $2;
	$Resource = $3;
    } elsif ($PlainURL =~ m!http://([^/]*)(/.*)$!io) {
	$Server = $1;
	$HttpPort = $DEFAULT_HTTP_PORT;
	$Resource = $2;
    } else {
	&MyFatal(10, $PlainURL);
    }
    
    # connect
    &HttpConnect($Server, $HttpPort, $Resource, $File)
	|| &MyFatal(10, $PlainURL);

    # ɽ�����̤κ���
    &MsgHeader("$BoardName: $ENTRY_MSG");

    # ���ѥե������ɽ��
    &ViewOriginalFile($File, $Name);
    print("<hr>\n");
    print("<h2>$H_REPLYMSG</h2>");

    # �إå���ʬ��ɽ��(�����ΰ��ѤǤʤ��Τ�Id=0)
    &EntryHeader(&GetReplySubjectFromFile($File), 0);

    # ��ʸ(���Ѥ���ʤ鸵����������)
    print("<textarea name=\"article\" rows=\"$TEXT_ROWS\" cols=\"$TEXT_COLS\">");
    &QuoteOriginalFile($File, $Name) if ($QuoteFlag == $QUOTE_ON);
    print("</textarea><br>\n");

    # ���ѥե�����
    print("<input name=\"qurl\" type=\"hidden\" value=\"$Url\">\n");
    print("<input name=\"file\" type=\"hidden\" value=\"$File\">\n");

    # �եå���ʬ��ɽ��
    &EntryFooter();

}


###
## ��������ɽ��(�ե�����)
#
sub ViewOriginalFile {

    # �ե�����̾��name tag
    local($File, $Name) = @_;

    # name tag���褿��?
    local($NameFlag) = ($Name) ? 0 : 1;

    # ������ʬ��Ƚ�Ǥ���ե饰
    # 0 ... before
    # 1 ... quote
    # 2 ... after
    local($QuoteFlag) = 0;

    open(TMP, "<$File") || &MyFatal(1, $File);
    while(<TMP>) {

	# �������Ѵ�
	&jcode'convert(*_, 'euc');

	# ���ѽ�λ��Ƚ��
	$QuoteFlag = 2, last
	    if (($QuoteFlag == 1) && (/$COM_ARTICLE_END/));

	# ����ʸ�����ɽ��
	print($_) if ($QuoteFlag == 1);

	# name tag?
	$NameFlag = 1 if (/<a\s+name\s*=\s*\"$Name/i);

	# ���ѳ��Ϥ�Ƚ��
	$QuoteFlag = 1 if (($NameFlag) && (/$COM_ARTICLE_BEGIN/));

    }
    close(TMP);

    # cannot quote specified file.
    print($H_CANNOTQUOTE) if ($QuoteFlag == 0);
}


###
## ���Ѥ���(�ե�����)
#
sub QuoteOriginalFile {

    # �ե�����̾
    local($File, $Name) = @_;

    # name tag���褿��?
    local($NameFlag) = ($Name) ? 0 : 1;

    # ������ʬ��Ƚ�Ǥ���ե饰
    local($QuoteFlag) = 0;

    open(TMP, "<$File") || &MyFatal(1, $File);
    while(<TMP>) {

	# �������Ѵ�
	&jcode'convert(*_, 'euc');

	# ���ѽ�λ��Ƚ��
	$QuoteFlag = 0, last
	    if (($QuoteFlag == 1) && (/$COM_ARTICLE_END/));

	# ����ʸ�����ɽ��
	if ($QuoteFlag == 1) {
	    s/&/&amp;/go;
	    s/\"//go;
	    if ($SYS_TAGINQUOTE) {
		s/<//go;
		s/>//go;
	    } else {
		s/<[^>]*>//go;
	    }
	    print($DEFAULT_QMARK, $_);
	}

	# name tag?
	$NameFlag = 1 if (/<a\s+name\s*=\s*\"$Name/i);

	# ���ѳ��Ϥ�Ƚ��
	$QuoteFlag = 1 if (($NameFlag) && (/$COM_ARTICLE_BEGIN/));
	
    }
    close(TMP);

}


###
## ����ե����뤫��Title���äƤ��ơ���Ƭ�ˡ�Re: �פ�Ĥ����֤���
#
sub GetReplySubjectFromFile {

    # �ե�����
    local($File) = @_;

    # ���Ф���Subject
    local($Title) = &GetSubjectFromFile($File);

    # ��Ƭ�ˡ�Re: �פ򤯤äĤ����֤���
    return("Re: $Title");

}


###
## http connection��ĥ�äƥ꥽�������äƤ��ơ�������Υե���������
#
sub HttpConnect {

    local($Server, $HttpPort, $RemoteFile, $LocalFile) = @_;
    local($Sockaddr) = "S n a4 x8";
    local($Name, $Aliases, $Proto) = getprotobyname('tcp');
    local($Name, $Aliases, $Type, $Len, $Hostaddr) = gethostbyname($Server);
    local($Sock) = pack($Sockaddr, 2, $HttpPort, $Hostaddr);

    socket(S, 2, 1, $Proto) || die $!;
    connect(S, $Sock) || return(0);
    select(S); $| = 1; select(STDOUT);
    print(S "GET $RemoteFile HTTP/1.0\n\n");

    open(LOCAL, ">$LocalFile") || &MyFatal(1, "$LocalFile");
    while (<S>) {

	# �������Ѵ�
	&jcode'convert(*_, 'euc');

	# �񤭹���
	print(LOCAL $_);
    }
    
    close(LOCAL);
    return(1);
}


#/////////////////////////////////////////////////////////////////////
# ��������ɽ�����̴�Ϣ


###
## ��������ɽ������
#*
sub ShowIcon {

    local($BoardName) = &GetBoardInfo($BOARD);
    local($FileName, $Title);

    # ɽ�����̤κ���
    &MsgHeader($SHOWICON_MSG);
    print("<p>\"$BoardName\"$H_ICONINTRO</p>\n");
    print("<p><dl>\n");

    # ��İ��ɽ��
    open(ICON, "$ICON_DIR/$BOARD.$ICONDEF_POSTFIX")
	|| (open(ICON, "$ICON_DIR/$DEFAULT_ICONDEF")
	    || &MyFatal(1, "$ICON_DIR/$DEFAULT_ICONDEF"));
    while(<ICON>) {
	chop;
	($FileName, $Title) = split(/\t/, $_);
	print("<dt><img src=\"$ICON_DIR/$FileName\" alt=\"$Title\"> : $Title\n");
    }
    close(ICON);

    print("</dl></p>\n");

    &MsgFooter();

}


#/////////////////////////////////////////////////////////////////////
# ���ս祽���ȴ�Ϣ


###
## ���ս�˥����ȡ�
#*
sub SortArticle {

    # ɽ������Ŀ������
    local($Num) = @_;

    # DB�ե�����
    local($DBFile) = &GetPath($BOARD, $DB_FILE_NAME);

    # �����ֹ������ե�����
    local($ArticleNumFile) = &GetPath($BOARD, $ARTICLE_NUM_FILE_NAME);

    # Board̾�Τμ���
    local($BoardName) = &GetBoardInfo($BOARD);

    # �ǿ������ֹ�����
    local($ArticleToId) = &GetArticleId($ArticleNumFile);
    local($ArticleFromId) = 0;

    local($ListFlag) = 0;
    local(@Lines) = ();
    local($Id, $Fid, $Aids, $Date, $Title, $Icon, $RemoteHost, $Name, $Email,
	  $Url, $Fmail) = (0, '', '', '', '', '', '', '', '', '', '');

    # ������0�ʤ�ǽ餫������
    if ($Num == 0) {
	$ArticleFromId = 1;
    } else {
	# ��������­��ʤ�����Ĵ��
	$Num = $ArticleToId if ($ArticleToId < $Num);

	# ��äƤ���ǽ�ε����ֹ�����
	$ArticleFromId = $ArticleToId - $Num + 1;
    }

    # lock�򤫤���
    &lock();

    # �����ߡ�DB�ե����뤬�ʤ���в���ɽ�����ʤ���
    open(DB, "<$DBFile") || &MyFatal(1, $DBFile);

    while(<DB>) {

	next if (/^\#/);
	chop;

	($Id, $Fid, $Aids, $Date, $Title, $Icon, $RemoteHost, $Name, $Email,
	 $Url, $Fmail) = split(/\t/, $_);
	$ListFlag = 1 if ($ArticleFromId <= $Id);

	# ���������Τ�ɽ�����ξ��ϥ���󥻥롣
	$ListFlag = 0 if ($SYS_NEWARTICLEONLY && ($Fid != 0));

	push(Lines, &GetFormattedTitle($Id, $Icon, $Title, $Name, $Date))
	    if ($ListFlag);

    }
    close(DB);

    # lock��Ϥ���
    &unlock();

    # ɽ�����̤κ���
    &MsgHeader("$BoardName: $SORT_MSG");

    &BoardHeader;

    print("<hr>\n");
    print("<ul>\n");

    # ������ɽ��
    if ($SYS_BOTTOMTITLE) {
	# ��������������
	foreach (@Lines) {print("$_\n");}
    } else {
	# ��������������
	foreach (reverse @Lines) {print("$_\n");}
    }

    print("</ul>\n");
    &MsgFooter();

}


#/////////////////////////////////////////////////////////////////////
# thread�̥����ȥ�ɽ����Ϣ


###
## �����������Υ����ȥ��thread�̤�n�Ĥ�ɽ����
#*
sub ViewTitle {

    # ɽ������Ŀ������
    local($Num) = @_;

    # DB�ե�����
    local($DBFile) = &GetPath($BOARD, $DB_FILE_NAME);

    # �����ֹ������ե�����
    local($ArticleNumFile) = &GetPath($BOARD, $ARTICLE_NUM_FILE_NAME);

    # Board̾�Τμ���
    local($BoardName) = &GetBoardInfo($BOARD);

    # �ǿ������ֹ�����
    local($ArticleToId) = &GetArticleId($ArticleNumFile);
    local($ArticleFromId) = 0;

    local($ListFlag) = 0;
    local(@Lines) = ();
    local($Line) = '';
    local($Id, $Fid, $Aids, $Date, $Title, $Icon, $RemoteHost, $Name, $Email,
	  $Url, $Fmail) = (0, '', '', '', '', '', '', '', '', '', '');

    # ������0�ʤ�ǽ餫������
    if ($Num == 0) {
	$ArticleFromId = 1;
    } else {
	# ��������­��ʤ�����Ĵ��
	$Num = $ArticleToId if ($ArticleToId < $Num);

	# ��äƤ���ǽ�ε����ֹ�����
	$ArticleFromId = $ArticleToId - $Num + 1;
    }

    # lock�򤫤���
    &lock();

    # �����ߡ�DB�ե����뤬�ʤ���в���ɽ�����ʤ���
    open(DB, "<$DBFile") || &MyFatal(1, $DBFile);
    while(<DB>) {

	next if (/^\#/);
	chop;

	($Id, $Fid, $Aids, $Date, $Title, $Icon, $RemoteHost, $Name, $Email,
	 $Url, $Fmail) = split(/\t/, $_);
	$ListFlag = 1 if ($ArticleFromId <= $Id);

	# ���������Τ�ɽ�����ξ��ϥ���󥻥롣
	$ListFlag = 0 if ($SYS_NEWARTICLEONLY && ($Fid != 0));

	if ($ListFlag) {

	    # �ɲä����
	    $Line = &GetFormattedTitle($Id, $Icon, $Title, $Name, $Date);

	    # �ɲ�
	    @Lines = ($Fid)
		? &AddTitleFollow($Fid, $Line, @Lines)
		    : &AddTitleNormal($Line, @Lines);
	}
    }
    close(DB);

    # lock��Ϥ�����
    &unlock();

    # ɽ�����̤κ���
    &MsgHeader("$BoardName: $VIEW_MSG");

    &BoardHeader;

    print("<hr>\n");
    print("<ul>\n");

    # ������ɽ��
    foreach (@Lines) {
	if (! /^$NULL_LINE$/) {
	    print("$_\n");
	}
    }

    print("</ul>\n");

    &MsgFooter();

}


###
## �����ȥ�ꥹ�Ȥ˽񤭹���(����)
#*
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
#*
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

	# �����ȥ�ꥹ���桢�������Ƥε������褿�顢
	if (/id=$Fid/) {

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


#/////////////////////////////////////////////////////////////////////
# ���嵭��ɽ����Ϣ


###
## ��������������n�Ĥ�ɽ����
#*
sub NewArticle {

    # ɽ������Ŀ������
    local($Num) = @_;

    # �����ֹ������ե�����
    local($ArticleNumFile) = &GetPath($BOARD, $ARTICLE_NUM_FILE_NAME);

    # Board̾�Τμ���
    local($BoardName) = &GetBoardInfo($BOARD);

    # �ǿ������ֹ�����
    local($ArticleToId) = &GetArticleId($ArticleNumFile);
    local($ArticleFromId) = 0;
    local($i, $File);

    # ������0�ʤ�ǽ餫������
    if ($Num == 0) {
	$ArticleFromId = 1;
    } else {
	# ��������­��ʤ�����Ĵ��
	$Num = $ArticleToId if ($ArticleToId < $Num);

	# ��äƤ���ǽ�ε����ֹ�����
	$ArticleFromId = $ArticleToId - $Num + 1;
    }

    # ɽ�����̤κ���
    &MsgHeader("$BoardName: $NEWARTICLE_MSG");

    &BoardHeader;

    print("<hr>\n");

    if ($SYS_BOTTOMTITLE) {

	# ����
	for ($i = $ArticleFromId; ($i <= $ArticleToId); $i++) {
	    # ������ɽ��(���ޥ���դ�)
	    &ViewOriginalArticle($i, 1);
	    print("<hr>\n");
	}
	
    } else {

	# ���
	for ($i = $ArticleToId; ($i >= $ArticleFromId); $i--) {
	    # ������ɽ��(���ޥ���դ�)
	    &ViewOriginalArticle($i, 1);
	    print("<hr>\n");
	}

    }

    &MsgFooter();
}



#/////////////////////////////////////////////////////////////////////
# ����������Ϣ


###
## �����θ���(ɽ�����̺���)
#*
sub SearchArticle {

    # ������ɡ������ϰϤ򽦤�
    local($Key, $SearchSubject, $SearchPerson, $SearchArticle)
	= ($cgi'TAGS{'key'}, $cgi'TAGS{'searchsubject'},
	   $cgi'TAGS{'searchperson'}, $cgi'TAGS{'searcharticle'});

    # Board̾�Τμ���
    local($BoardName) = &GetBoardInfo($BOARD);

    # ɽ�����̤κ���
    &MsgHeader("$BoardName: $SEARCHARTICLE_MSG");

    # ����«
    print("<form action=\"$PROGRAM\" method=\"POST\">\n");
    print("<input name=\"c\" type=\"hidden\" value=\"s\">\n");
    print("<input name=\"b\" type=\"hidden\" value=\"$BOARD\">\n");

    # �ܥ���
    print("<p>$H_INPUTKEYWORD</p>\n");
    print("<input type=\"submit\" value=\"$H_SEARCHKEYWORD\">\n");
    print("<input type=\"reset\" value=\"$H_RESETKEYWORD\">\n");

    # �������������
    print("<p>$H_KEYWORD:\n");
    print("<input name=\"key\" size=\"$KEYWORD_LENGTH\" value=\"$Key\">");
    print("</p>\n");

    # �����ϰ�������
    print("<p>$H_SEARCHTARGET:\n");
    if ($SearchSubject) {
	print("<input name=\"searchsubject\" type=\"checkbox\" value=\"on\" CHECKED> $H_SEARCHTARGETSUBJECT / \n");
    } else {
	print("<input name=\"searchsubject\" type=\"checkbox\" value=\"on\"> $H_SEARCHTARGETSUBJECT / \n");
    }

    if ($SearchPerson) {
	print("<input name=\"searchperson\" type=\"checkbox\" value=\"on\" CHECKED> $H_SEARCHTARGETPERSON / \n");
    } else {
	print("<input name=\"searchperson\" type=\"checkbox\" value=\"on\"> $H_SEARCHTARGETPERSON / \n");
    }

    if ($SearchArticle) {
	print("<input name=\"searcharticle\" type=\"checkbox\" value=\"on\" CHECKED> $H_SEARCHTARGETARTICLE");
    } else {
	print("<input name=\"searcharticle\" type=\"checkbox\" value=\"on\"> $H_SEARCHTARGETARTICLE");
    }

    print("</p>\n");

    print("<hr>\n");

    # ������ɤ����Ǥʤ���С����Υ�����ɤ�ޤ൭���Υꥹ�Ȥ�ɽ��
    &SearchArticleList($Key, $SearchSubject, $SearchPerson, $SearchArticle)
	if (($Key) && ($SearchSubject || ($SearchPerson || $SearchArticle)));

    &MsgFooter();
}


###
## �����θ���(������̤�ɽ��)
#*
sub SearchArticleList {

    # ������ɡ������ϰ�
    local($Key, $Subject, $Person, $Article) = @_;

    # DB�ե�����
    local($DBFile) = &GetPath($BOARD, $DB_FILE_NAME);

    local($Id, $Fid, $Aids, $Date, $Title, $Icon, $RemoteHost, $Name, $Email,
	  $Url, $Fmail) = (0, '', '', '', '', '', '', '', '', '', '');
    local($ArticleFile, $ArticleFilePath, $HitFlag) = ('', '', 0);
    local($Line, $Flag) = ('', 0);

    # �ꥹ�ȳ���
    print("<ul>\n");

    # lock�򤫤���
    &lock();

    # �ե�����򳫤���DB�ե����뤬�ʤ����not found.
    open(DB, "<$DBFile") || &MyFatal(1, $DBFile);
    while(<DB>) {

	next if (/^\#/);

	# �ѿ��Υꥻ�å�
	$Flag = 0;
	$Line = '';

	($Id, $Fid, $Aids, $Date, $Title, $Icon, $RemoteHost, $Name, $Email,
	 $Url, $Fmail) = split(/\t/, $_);
	$ArticleFile = &GetArticleFileName($Id, '');
	$ArticleFilePath = &GetArticleFileName($Id, $BOARD);

	# �����ȥ�򸡺�
	$Flag = 1 if ($Subject && ($Title =~ /$Key/));

	# ��Ƽ�̾�򸡺�
	$Flag = 1 if ($Person && (($Name =~ /$Key/)));

	# ��ʸ�򸡺�
	$Flag = 1 if ($Article && ($Line = &SearchArticleKeyword($ArticleFilePath, $Key)));

	if ($Flag) {

	    # ����1�ĤϹ��פ���
	    $HitFlag = 1;

	    # �����ؤΥ�󥯤�ɽ��
	    print(&GetFormattedTitle($Id, $Icon, $Title, $Name, $Date));

	    # ��ʸ�˹��פ���������ʸ��ɽ��
	    if ($Article && ($Line ne '')) {
		$Line =~ s/<[^>]*>//go;
		$Line =~ s/&/&amp;/go;
		$Line =~ s/\"/&quot;/go;
		print("<blockquote>$Line</blockquote>\n");
	    }
	}
    }
    close(DB);

    # lock��Ϥ���
    &unlock();

    # �ҥåȤ��ʤ��ä���
    print("<dt>$H_NOTFOUND\n") unless ($HitFlag = 1);

    # �ꥹ���Ĥ���
    print("</dl>\n");
}


###
## �����θ���(��ʸ)
#*
sub SearchArticleKeyword {

    # �ե�����̾�ȥ������
    local($File, $Key) = @_;

    # ��������
    # SearchArticleList��lock���Ƥ�Τ�lock����ɬ�פʤ�
    open(ARTICLE, "<$File") || &MyFatal(1, $File);
    while(<ARTICLE>) {

	# TAG�������
	s/<[^>]*>//go;

	# �ҥå�?
	(/$Key/) && return($_);
    }

    # �ҥåȤ���
    return('');
}


#/////////////////////////////////////////////////////////////////////
# �����ꥢ����Ϣ


###
## �����ꥢ������Ͽ���ѹ�
#*
sub AliasNew {

    # ɽ�����̤κ���
    &MsgHeader($ALIASNEW_MSG);

    # ������Ͽ/��Ͽ���Ƥ��ѹ�
    print("<p>$H_ALIASTITLE</p>\n");
    print("<p>\n");
    print("<form action=\"$PROGRAM\" method=\"POST\">\n");
    print("<input name=\"c\" type=\"hidden\" value=\"am\">\n");
    print("$H_ALIAS <input name=\"alias\" type=\"text\" value=\"#\" size=\"$NAME_LENGTH\"><br>\n");
    print("$H_FROM <input name=\"name\" type=\"text\" size=\"$NAME_LENGTH\"><br>\n");
    print("$H_MAIL <input name=\"email\" type=\"text\" size=\"$MAIL_LENGTH\"><br>\n");
    print("$H_URL <input name=\"url\" type=\"text\" value=\"http://\" size=\"$URL_LENGTH\"><br>\n");
    print("$H_ALIASNEWCOM<br>\n");
    print("<input type=\"submit\" value=\"$H_ALIASNEWPUSH\">\n");
    print("</form></p>\n");
    
    print("<hr>\n");
    
    # ���
    print("<p>$H_ALIASDELETE</p>\n");
    print("<p>\n");
    print("<form action=\"$PROGRAM\" method=\"POST\">\n");
    print("<input name=\"c\" type=\"hidden\" value=\"ad\">\n");
    print("$H_ALIAS <input name=\"alias\" type=\"text\" size=\"$NAME_LENGTH\"><br>\n");
    print("$H_ALIASDELETECOM<br>\n");
    print("<input type=\"submit\" value=\"$H_ALIASDELETEPUSH\">\n");
    print("</form></p>\n");
    
    print("<hr>\n");
    
    # ����
    print("<p>\n");
    print("<form action=\"$PROGRAM\" method=\"POST\">\n");
    print("<input name=\"c\" type=\"hidden\" value=\"as\">\n");
    print("<input type=\"submit\" value=\"$H_ALIASREFERPUSH\">\n");
    print("</form></p>\n");
    
    # ����«
    &MsgFooter();

}


###
## ��Ͽ/�ѹ�
#*
sub AliasMod {

    # �����ꥢ����̾�����᡼�롢URL
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
    &MyFatal(6, '') if ($HitFlag == 1);
    
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
#*
sub AliasCheck {

    local($A, $N, $E, $U) = @_;

    # �������å�
    &MyFatal(2, '') if ($A eq '') || ($N eq '') || ($E eq '');

    &CheckAlias($A);
    &CheckName($N);
    &CheckEmail($E);
    &CheckURL($U);
    
}


###
## ���
#*
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
    &MyFatal(6, '') if ($HitFlag == 1);
    
    # �����ꥢ�����ʤ�!
    &MyFatal(7, $A) if ($HitFlag == 0);
    
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
#*
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
	print("<p>\n");
	print("<dt><strong>$Alias</strong>\n");
	print("<dd>$H_FROM $Name{$Alias}\n");
	print("<dd>$H_MAIL $Email{$Alias}\n");
	print("<dd>$H_HOST $Host{$Alias}\n");
	print("<dd>$H_URL $URL{$Alias}\n");
	print("</p>\n");
    }

    # �ꥹ���Ĥ���
    print("</dl>\n");
    
    &MsgFooter();

}


###
## �����ꥢ���ե�������ɤ߹����Ϣ�������������ࡣ
## CAUTION: %Name, %Email, %Host, %URL������ޤ���
#*
sub CashAliasData {

    # �ե�����
    local($File) = @_;
    
    local($A, $N, $E, $H, $U) = ('', '', '', '', '');

    # lock�򤫤���
    &lock();

    # ������ࡣ
    open(ALIAS, "<$File") || &MyFatal(1, $File);
    while(<ALIAS>) {
	
	chop;

	($A, $N, $E, $H, $U) = split(/\t/, $_);

	$Name{$A} = $N;
	$Email{$A} = $E;
	$Host{$A} = $H;
	$URL{$A} = $U;
    }
    close(ALIAS);

    # lock��Ϥ���
    &unlock();

}


###
## �����ꥢ���ե�����˥ǡ�����񤭽Ф���
## CAUTION: %Name, %Email, %Host, %URL��ɬ�פȤ��ޤ���
##          $Name���ΤȽ񤭹��ޤʤ���
#*
sub WriteAliasData {

    # �ե�����
    local($File) = @_;
    local($Alias);

    # ��å��򤫤���
    &lock();

    # �񤭽Ф�
    open(ALIAS, ">$File") || &MyFatal(1, $File);
    foreach $Alias (sort keys(%Name)) {
	($Name{$Alias}) && printf(ALIAS "%s\t%s\t%s\t%s\t%s\n",
				  $Alias, $Name{$Alias}, $Email{$Alias},
				  $Host{$Alias}, $URL{$Alias});
    }
    close(ALIAS);
    
    # ��å��򳰤���
    &unlock();

}


###
## �Ǽ��ĤΥإå���ɽ������
#
sub BoardHeader {

    local($File) = &GetPath($BOARD, $BOARD_FILE_NAME);

    open(HEADER, "<$File") || &MyFatal(1, $File);
    while(<HEADER>){
        print("$_");
    }
    close(HEADER);

}


#/////////////////////////////////////////////////////////////////////
# ���̴ؿ�


###
## �����������ֹ���֤�
#
sub GetNewArticleId {

    # �����ֹ������ե�����
    local($ArticleNumFile) = &GetPath($BOARD, $ARTICLE_NUM_FILE_NAME);

    # �����ֹ�
    local($ArticleId) = 0;

    open(AID, "<$ArticleNumFile") || &MyFatal(1, $ArticleNumFile);
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

    # lock�򤫤���
    &lock();

    open(AID, "$ArticleNumFile") || &MyFatal(1, $ArticleNumFile);
    while(<AID>) {
	chop;
	$ArticleId = $_;
    }
    close(AID);

    # lock��Ϥ���
    &unlock();

    # �����ֹ���֤���
    return($ArticleId);
}


###
## �ܡ��ɥ����ꥢ������ܡ��ɥ����ꥢ��̾���äƤ��롣
#
sub GetBoardInfo {

    # �����ꥢ��̾
    local($Alias) = @_;

    # �ܡ���̾
    local($BoardName);

    open(ALIAS, "<$BOARD_ALIAS_FILE")
	|| &MyFatal(1, $BOARD_ALIAS_FILE);
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
    local($Id, $Icon, $Title, $Name, $Date) = @_;
    local($String, $Fnum) = ('', 0);

    if (($Icon eq $H_NOICON) || (! $Icon)) {
	$String = sprintf("<li><strong>$Id .</strong> <a href=\"$PROGRAM?b=$BOARD&c=e&id=$Id\">$Title</a> [$Name] $Date");
    } else {
	$String = sprintf("<li><strong>$Id .</strong> <img src=\"%s\" alt=\"$Icon\"><a href=\"$PROGRAM?b=$BOARD&c=e&id=$Id\">$Title</a> [$Name] $Date", &GetIconURL($Icon));
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
	$String = sprintf("<li><strong>$Id .</strong> $Title [$Name] $Date", &GetIconURL($Icon));
    } else {
	$String = sprintf("<li><strong>$Id .</strong> <img src=\"%s\" alt=\"$Icon\">$Title [$Name] $Date", &GetIconURL($Icon));
    }

    return($String);
}


###
## �����������ɽ��
#
sub ShowFormattedLinkToFollowedArticle {

    local($Src, $Icon, $Subject) = @_;

    # Board̾�Τμ���
    local($BoardName) = &GetBoardInfo($BOARD);

    # ������μ���
    local($Link) = ($Src =~ /^http:/) ? $Src : "$PROGRAM?b=$BOARD&c=e&id=$Src";

    if ($Src != 0) {
	if (($Icon eq $H_NOICON) || (! $Icon)) {
	    print("<strong>$H_REPLY</strong> [$BoardName: $Src] <a href=\"$Link\">$Subject</a><br>\n");
	} else {
	    printf("<strong>$H_REPLY</strong> [$BoardName: $Src] <img src=\"%s\" alt=\"$Icon\"><a href=\"$Link\">$Subject</a><br>\n", &GetIconURL($Icon));
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
    ($String =~ (/^#/)) || &MyFatal(8, 'alias');
    (length($String) > 1) || &MyFatal(8, 'alias');

}


###
## ʸ��������å�: ̾��
#
sub CheckName {

    local($String) = @_;

}


###
## ʸ��������å�: �᡼��
#
sub CheckEmail {

    local($String) = @_;
    ($String =~ (/@/)) || &MyFatal(8, 'E-Mail');

}


###
## ʸ��������å�: URL
#
sub CheckURL {

    local($String) = @_;
    ($String =~ m#^http://.*$#) || ($String =~ m#^http://$#)
	|| ($String eq '') || &MyFatal(8, 'URL');

}


###
## �����Υإå���ɽ��
#
sub MsgHeader {

    # message and board
    local($Message) = @_;
    
    &cgi'header;
    print("<html>\n");
    print("<head>\n");
    print("<title>$Message</title>\n");
    print("</head>\n");
    print("<body bgcolor=\"$BG_COLOR\" TEXT=\"$TEXT_COLOR\" LINK=\"$LINK_COLOR\" ALINK=\"$ALINK_COLOR\" VLINK=\"$VLINK_COLOR\">\n");
    print("<h1>$Message</h1>\n");
    print("<hr>\n");

}


###
## �����Υեå���ɽ��
#
sub MsgFooter {

    print("<hr>\n");
    print("<address>\n");
    print("$ADDRESS\n");
    print("</address>\n");
    print("</body>\n");
    print("</html>\n");

}


###
## ��å��ط�
#

# ��å�
sub lock {

    local($TimeOut) = 0;
    local(*LOCKORG);

    srand(time|$$);

    open(LOCKORG, ">$LOCK_ORG") || &MyFatal(1, $LOCK_ORG);
    close(LOCKORG);

    for($TimeOut = 0; $TimeOut < $LOCK_WAIT; $TimeOut++) {
	last if link($LOCK_ORG, $LOCK_FILE);
	select(undef, undef, undef, (rand(6)+5)/10);
    }

    unlink($LOCK_ORG);

    &MyFatal(80, $TimeOut) unless ($TimeOut < $LOCK_WAIT);

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

    # Board̾�Τμ���
    local($BoardName) = &GetBoardInfo($BOARD);

    # ���Ѥ���ե�����
    local($QuoteFile) = &GetArticleFileName($Id, $BOARD);

    # ���ѵ����ξ���
    local($rFid, $rAids, $rDate, $rSubject, $rIcon, $rRemoteHost, $rName,
	  $rEmail, $rUrl, $rFmail) = ('', '', '', '', '', '', '', '', '', '');

    # ��������μ���
    local($Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $Email,
	  $Url, $Fmail) = &GetArticlesInfo($Id);

    # ���ѵ�����������
    ($rFid, $rAids, $rDate, $rSubject, $rIcon, $rRemoteHost, $rName, $rEmail,
     $rUrl, $rFmail) = &GetArticlesInfo($Fid) if ($Fid != 0);

    # ���ޥ��ɽ��?
    if ($Flag) {

	print("<p>\n");

	# �ޤȤ��ɤ߷ϤʤΤǡ��ּ��ε����ץ�󥯤�̵����
	# print("<a href=\"$PROGRAM?b=$BOARD&c=en&id=$Id\">$H_NEXTARTICLE</a> // \n");
	print("<a href=\"$PROGRAM?b=$BOARD&c=n\">$H_POSTNEWARTICLE</a> // \n");
	print("<a href=\"$PROGRAM?b=$BOARD&c=f&id=$Id\">$H_REPLYTHISARTICLE</a> // \n");
	print("<a href=\"$PROGRAM?b=$BOARD&c=q&id=$Id\">$H_REPLYTHISARTICLEQUOTE</a> // \n");
	print("<a href=\"$PROGRAM?b=$BOARD&c=t&id=$Id\">$H_READREPLYALL</a>\n");
	print("</p>\n");

    }

    # �ܡ���̾�ȵ����ֹ桢��
    if (($Icon eq $H_NOICON) || (! $Icon)) {
	print("<strong>$H_SUBJECT</strong> [$BoardName: $Id] $Subject<br>\n");
    } else {
	printf("<strong>$H_SUBJECT</strong> [$BoardName: $Id] <img src=\"%s\" alt=\"$Icon\">$Subject<br>\n", &GetIconURL($Icon));
    }

    # ��̾��
    if (! $Url) {
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
    open(TMP, "<$QuoteFile") || &MyFatal(1, $QuoteFile);
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
    return(($Board) ? "$Board/$Id" : "$Id");

}


###
## �ܡ���̾�Τȥե�����̾���顢���Υե�����Υѥ�̾����Ф���
#
sub GetPath {

    # Board��File
    local($Board, $File) = @_;

    # �֤�
    return("$Board/$File");

}


###
## ��������̾���顢���������URL�����
#
sub GetIconURL {

    # ��������̾
    local($Icon) = @_;

    local($FileName, $Title, $TargetFile) = ('', '', '');

    # ��İ��ɽ��
    open(ICON, "$ICON_DIR/$BOARD.$ICONDEF_POSTFIX")
	|| (open(ICON, "$ICON_DIR/$DEFAULT_ICONDEF")
	    || &MyFatal(1, "$ICON_DIR/$DEFAULT_ICONDEF"));
    while(<ICON>) {
	chop;
	($FileName, $Title) = split(/\t/, $_);
	$TargetFile = $FileName if ($Title eq $Icon);
    }
    close(ICON);

    return(($TargetFile) ? "$ICON_DIR/$TargetFile" : '');

}


###
## ���뵭���ξ������Ф���
#
sub GetArticlesInfo {

    # �оݵ�����ID
    local($Id) = @_;

    # DB�ե�����
    local($DBFile) = &GetPath($BOARD, $DB_FILE_NAME);

    local($dId, $dFid, $dAids, $dDate, $dTitle, $dIcon, $dRemoteHost, $dName,
	  $dEmail, $dUrl, $dFmail)
			 = (0, '', '', '', '', '', '', '', '', '', '');

    local($rFid, $rAids, $rDate, $rTitle, $rIcon, $rRemoteHost, $rName,
	  $rEmail, $rUrl, $rFmail)
			 = ('', '', '', '', '', '', '', '', '', '');

    # lock�򤫤���
    &lock();

    # �����ߡ�DB�ե����뤬�ʤ����0/''���֤���
    open(DB, "<$DBFile");
    while(<DB>) {

	next if (/^\#/);
	chop;

	($dId, $dFid, $dAids, $dDate, $dTitle, $dIcon, $dRemoteHost, $dName,
	 $dEmail, $dUrl, $dFmail) = split(/\t/, $_);

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

    # lock��Ϥ���
    &unlock();

    return($rFid, $rAids, $rDate, $rTitle, $rIcon, $rRemoteHost, $rName,
	   $rEmail, $rUrl, $rFmail);

}


###
## ���顼ɽ��
#
sub MyFatal {

    # ���顼�ֹ�ȥ��顼����μ���
    local($MyFatalNo, $MyFatalInfo) = @_;
    #
    # 1 ... File��Ϣ
    # 2 ... ��ƤκݤΡ�ɬ�ܹ��ܤη�ǡ
    # 3 ... �����ȥ�ꥹ�ȥե�����Υե����ޥåȤ���������
    # 4 ... �����ȥ��html���������äƤ���
    # 5 ... �ץ��������椬��������
    # 6 ... �����ꥢ�����ۥ��Ȥ����פ����������ꥢ�����ѹ����Ǥ��ʤ�
    # 7 ... �����ꥢ������Ͽ����Ƥ��ʤ���
    # 8 ... �����ꥢ������Ͽ����ʸ�����������ʤ���
    # 9 ... �᡼�뤬����ʤ��ä�
    # 10 ... cannot connect to specified URL.

    # �Ȥꤢ���������å�
    &unlock();

    &MsgHeader($ERROR_MSG);
    
    if ($MyFatalNo == 1) {
	print("<p>File: $MyFatalInfo��¸�ߤ��ʤ���\n");
	print("���뤤��permission�����꤬�ְ�äƤ��ޤ���\n");
	print("������Ǥ�����<a href=\"mailto:$MAINT\">$MAINT</a>�ޤ�\n");
	print("�嵭�ե�����̾���Τ餻��������</p>\n");
    } elsif ($MyFatalNo == 2) {
	print("<p>���Ϥ���Ƥ��ʤ����ܤ�����ޤ���\n");
	print("��äƤ⤦���١�</p>\n");
    } elsif ($MyFatalNo == 3) {
	print("<p>Title File is illegal.\n");
	print("������Ǥ�����<a href=\"mailto:$MAINT\">$MAINT</a>\n");
	print("�ޤǤ��Τ餻��������</p>\n");
    } elsif ($MyFatalNo == 4) {
	print("<p>�����ʤ����������HTML����������뤳�Ȥ�\n");
	print("�ؤ����Ƥ��ޤ�����äƤ⤦���١�</a>\n");
    } elsif ($MyFatalNo == 5) {
	print("<p>�ؿ�$MyFatalInfo�ˤ����ơ����ꤨ�ʤ����֤�\n");
	print("�ץ��������椬��ư���ޤ�����");
	print("���Υ��顼��������������");
	print("<a href=\"mailto:$MAINT\">$MAINT</a>�ޤ�");
	print("���Τ餻��������</p>\n");
    } elsif ($MyFatalNo == 6) {
	print("<p>��Ͽ����Ƥ��륨���ꥢ���Τ�Τȡ�\n");
	print("�ۥ���̾�����פ��ޤ���\n");
	print("��äƤ⤦���١�</p>\n");
    } elsif ($MyFatalNo == 7) {
	print("<p>$MyFatalInfo�Ȥ��������ꥢ����\n");
	print("��Ͽ����Ƥ��ޤ���\n");
	print("��äƤ⤦���١�</p>\n");
    } elsif ($MyFatalNo == 8) {
	print("<p>$MyFatalInfo��������������ޤ���?\n");
	print("��äƤ⤦���١�</p>\n");
    } elsif ($MyFatalNo == 9) {
	print("<p>�᡼�뤬�����Ǥ��ޤ���Ǥ�����\n");
	print("���Υ��顼��������������");
	print("<a href=\"mailto:$MAINT\">$MAINT</a>�ޤ�");
	print("���Τ餻��������</p>\n");
    } elsif ($MyFatalNo == 10) {
	print("<p>$URL�˥��������Ǥ��ޤ���.\n");
	print("Try later.</p>\n");
    } elsif ($MyFatalNo == 11) {
	print("<p>���ε����Ϥޤ���Ƥ���Ƥ��ޤ���</p>\n");
    } elsif ($MyFatalNo == 80) {
	print("<p>�����ƥ�Υ�å��˼��Ԥ��ޤ�����</p>\n");
	print("<p>���߹�äƤ���褦�Ǥ�����äƤ⤦���١�</p>\n");
    } else {
	print("<p>���顼�ֹ�����: ������Ǥ�����");
	print("���Υ��顼��������������");
	print("<a href=\"mailto:$MAINT\">$MAINT</a>�ޤ�");
	print("���Τ餻��������</p>\n");
    }
    
    &MsgFooter();
    exit 0;
}
