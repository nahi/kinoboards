#!/usr/local/bin/perl5
#
# $Id: kb.cgi,v 3.3 1996-02-11 06:53:43 nakahiro Exp $
#
# $Log: kb.cgi,v $
# Revision 3.3  1996-02-11 06:53:43  nakahiro
# the 1st test version for my homepage.
#
# Revision 3.2  1996/02/08 07:11:04  nakahiro
# Bulletin board for KINOTROPE Inc.
#
# Revision 3.1  1996/01/26 07:33:18  nakahiro
# release version for OOW96.
#
# Revision 3.0  1996/01/20 14:01:13  nakahiro
# oow1
#
# Revision 2.1  1995/12/19 18:46:12  nakahiro
# send mail
#
# Revision 2.0  1995/12/19 14:26:56  nakahiro
# user writable alias file.
#
# Revision 1.11  1995/12/19 05:00:54  nakahiro
# cgi and tag_secure packaging.
#
# Revision 1.10  1995/12/15 14:21:37  nakahiro
# keyword search routine.
#
# Revision 1.9  1995/12/13 17:08:19  nakahiro
# '(single-quote)-char escape routine.
#
# Revision 1.8  1995/12/04 11:44:31  nakahiro
# articles can include ' char.
#
# Revision 1.7  1995/11/24 17:29:00  nakahiro
# title list of picked articles.
#
# Revision 1.6  1995/11/22 13:01:39  nakahiro
# partial sort by date.
#
# Revision 1.5  1995/11/15 11:39:16  nakahiro
# show user-alias information when posting.
#
# Revision 1.4  1995/11/08 09:18:22  nakahiro
# Add reference to Original File when Quoting local file.
#
# Revision 1.3  1995/11/02 05:50:48  nakahiro
# New Feature: quote a local file.
#
# Revision 1.2  1995/11/02 04:59:44  nakahiro
# A bug in SortArticle was fixed.
#
# Revision 1.1  1995/11/01 06:27:56  nakahiro
# many many changes and fixed bugs from ver 1.0.
#
# Revision 1.0  1995/10/22  08:59:03  nakahiro
# beta version.
# released on MAGARI page in kinotrope.
#


# kinoBoards: Kinoboards Is Network Opened BOARD System


#/////////////////////////////////////////////////////////////////////


###
## �إå��ե�������ɤ߹���
#
require('kb.ph');


#/////////////////////////////////////////////////////////////////////


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
# �ե�����
#
# ��å��ե�����
$LOCK_FILE = ".lock.kb";
# �����ֹ�ե�����
$ARTICLE_NUM_FILE_NAME = ".articleid";
# DB�ե�����
$BOARD_FILE_NAME = ".board";
# all�ե�����
$DB_FILE_NAME = ".db";
# �桼�������ꥢ���ե�����
$USER_ALIAS_FILE = "kinousers";
# �ܡ��ɥ����ꥢ���ե�����
$BOARD_ALIAS_FILE = "kinoboards";
# �ǥե���ȤΥ�����������ե�����
$DEFAULT_ICONDEF = "all.idef";

#
# �����Υץ�ե�����
#
$ARTICLE_PREFIX = "kb";

#
# prefix of quote file.
#
$QUOTE_PREFIX = "q";

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
# �Ķ��ѿ��򽦤�
#
$SERVER_NAME = $ENV{'SERVER_NAME'};
$SERVER_PORT = $ENV{'SERVER_PORT'};
$SCRIPT_NAME = $ENV{'SCRIPT_NAME'};
$PATH_INFO = $ENV{'PATH_INFO'};
$REMOTE_HOST = $ENV{'REMOTE_HOST'};
$BOARD = substr($PATH_INFO, $[ + 1);
($CGIPROG_NAME = $SCRIPT_NAME) =~ s#^(.*/)##;
$CGIDIR_NAME = $1;
$SCRIPT_URL = "http://$SERVER_NAME:$SERVER_PORT$SCRIPT_NAME";
$DIR_URL = "http://$SERVER_NAME:$SERVER_PORT$CGIDIR_NAME";
$PROGRAM = (($SYS_SCRIPTPATH == 'relative') ? $CGIPROG_NAME : $SCRIPT_NAME);
$PROGRAM_FROM_BOARD =
    (($SYS_SCRIPTPATH == 'relative') ? "../$PROGRAM" : $PROGRAM);

#
# �����ѥ�����ʸ
#
$COM_ARTICLE_BEGIN = "<!-- Article Begin -->";
$COM_ARTICLE_END = "<!-- Article End -->";
$COM_HEADER_BEGIN = "<!-- Header Begin -->";
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


###
## ���󥯥롼�ɥե�������ɤ߹���
#
require('cgi.pl');
require('tag_secure.pl');


###
## �ᥤ��
#


# �ǿ��ε���n��(�����ȥ�):c=v&num={[1-9][0-9]*}
# ���ս祽����:		c=r&num={[1-9][0-9]*}
# �ǿ��ε���n��(����):	c=l&num={[1-9][0-9]*}
# �������:		c=n
# ���ѤĤ��ե���:	c=q&id={[1-9][0-9]*}
# ���Ѥʤ��ե���:	c=f&id={[1-9][0-9]*}
# URL���ѥե���:	c=q/f&url={URL}
# ��������ɽ��:		c=i
# �����Υץ�ӥ塼:	c=p&(��)....
# ��ǧ�Ѥ߲���:		c=x&id={[1-9][0-9]*(���ѤǤʤ���id=0)}
# thread�ޤȤ��ɤ�:	c=t&id={[1-9][0-9]*}
# ����:			c=s
# �����ꥢ����Ͽ����:	c=an
# �����ꥢ����Ͽ:	c=am&alias=..&name=..&email=..&url=..
# �����ꥢ�����:	c=ad&alias=...
# �����ꥢ������:	c=as

MAIN: {

    # ɸ������(POST)�ޤ��ϴĶ��ѿ�(GET)�Υǥ����ɡ�
    &cgi'decode;

    # �ͤ����
    local($Command) = $cgi'TAGS{'c'};
    local($Id) = $cgi'TAGS{'id'};
    local($Num) = $cgi'TAGS{'num'};
    local($Key) = $cgi'TAGS{'key'};
    local($Alias) = $cgi'TAGS{'alias'};
    local($Name) = $cgi'TAGS{'name'};
    local($Email) = $cgi'TAGS{'email'};
    local($File) = $cgi'TAGS{'file'};
    local($URL) = $cgi'TAGS{'url'};

    # ���ޥ�ɥ����פˤ��ʬ��
    &Entry($NO_QUOTE, 0),		last MAIN if ($Command eq "n");
    $Id ? &Entry($QUOTE_ON, $Id) : &URLEntry($QUOTE_ON, $URL),
					last MAIN if ($Command eq "q");
    $Id ? &Entry($NO_QUOTE, $Id) : &URLEntry($NO_QUOTE, $URL),
					last MAIN if ($Command eq "f");
    &ShowIcon,				last MAIN if ($Command eq "i");
    &Preview,				last MAIN if ($Command eq "p");
    &Thanks($File, $Id),		last MAIN if ($Command eq "x");

    &ViewTitle($Num),			last MAIN if ($Command eq "v");
    &NewArticle($Num),			last MAIN if ($Command eq "l");
    &SortArticle($Num),			last MAIN if ($Command eq "r");
#	&ThreadArticle($Id),		last MAIN if ($Command eq "t");
    &SearchArticle($Key),		last MAIN if ($Command eq "s");
    &FollowMailEntry($Id),		last MAIN if ($Command eq "me");
    &FollowMailAdd($Id, $Email),	last MAIN if ($Command eq "ma");
    &AliasNew,				last MAIN if ($Command eq "an");
    &AliasMod($Alias, $Name, $Email, $URL),
					last MAIN if ($Command eq "am");
    &AliasDel($Alias),			last MAIN if ($Command eq "ad");
    &AliasShow,				last MAIN if ($Command eq "as");

    print("illegal command was given.\n");
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

    # ɽ�����̤κ���
    &MsgHeader($ENTRY_MSG, $BOARD);

    # �ե����ξ��
    if ($Id != 0) {
	&ViewOriginalArticle($Id);
	print("<hr>\n");
	print("<h2>$H_REPLYMSG</h2>");
    }

    # ����«
    print("<form action=\"$PROGRAM_FROM_BOARD/$BOARD\" method =\"POST\">\n");
    print("<input name=\"c\" type=\"hidden\" value=\"p\">\n");
    
    # ����Id; ���ѤǤʤ��ʤ�0��
    print("<input name=\"id\" type=\"hidden\" value=\"$Id\">\n");

    # ������ʸ��Board̾����������
    &EntryHeader;

    # Subject(�ե����ʤ鼫ưŪ��ʸ����������)
    printf("%s <input name=\"subject\" type=\"text\" value=\"%s\" size=\"%s\"><br>\n",
	   $H_SUBJECT,
	   (($Id !=0 ) ? &GetReplySubject($Id, $BOARD) : ""),
	   $SUBJECT_LENGTH);

    # TextType
    if ($SYS_TEXTTYPE) {
	print("$H_TEXTTYPE\n");
	print("<SELECT NAME=\"texttype\">\n");
	print("<OPTION SELECTED>$H_PRE\n");
	print("<OPTION>$H_HTML\n");
	print("</SELECT><BR>\n");
    }

    # ��ʸ(���Ѥ���ʤ鸵����������)
    print("<textarea name=\"article\" rows=\"$TEXT_ROWS\" cols=\"$TEXT_COLS\">");
    &QuoteOriginalArticle($Id, $BOARD)
	if ($Id != 0 && $QuoteFlag == $QUOTE_ON);
    print("</textarea><br>\n");

    # ̾���ȥ᡼�륢�ɥ쥹��URL��ɽ����
    &EntryUserInformation;

    # �ܥ���
    &EntrySubmitButton;

    # ����«
    print("</form>\n");

    &MsgFooter;
}


###
## �񤭹��߲���(URL)
#
sub URLEntry {

    # ���Ѥ���/�ʤ��ȡ�URL
    local($QuoteFlag, $URL) = @_;

    # file
    local($File) = &GetPath($BOARD, ".$QUOTE_PREFIX.$$");
    local($Server, $HttpPort, $Resource, $Name) = ("", "", "", "");
    local($PlainURL) = "";

    # split
    $Name = (($PlainURL = $URL) =~ s/\#(.*)$//o) ? $1 : "";

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
    &MsgHeader($ENTRY_MSG, $BOARD);

    # ���ѥե������ɽ��
    &ViewOriginalFile($File, $Name);
    print("<hr>\n");
    print("<h2>$H_REPLYMSG</h2>");
    
    # ����«
    print("<form action=\"$PROGRAM_FROM_BOARD/$BOARD\" method =\"POST\">\n");
    print("<input name=\"c\" type=\"hidden\" value=\"p\">\n");

    # ����Id; �����ΰ��ѤǤʤ��Τ�0��
    print("<input name=\"id\" type=\"hidden\" value=\"0\">\n");

    # ���ѥե�����
    print("<input name=\"qurl\" type=\"hidden\" value=\"$URL\">\n");
    print("<input name=\"file\" type=\"hidden\" value=\"$File\">\n");

    # ������ʸ��Board̾����������
    &EntryHeader;

    # Subject
    printf("%s <input name=\"subject\" type=\"text\" value=\"%s\" size=\"%s\"><br>\n",
	   $H_SUBJECT, &GetReplySubjectFromFile($File), $SUBJECT_LENGTH);
    
    # TextType
    if ($SYS_TEXTTYPE) {
	print("$H_TEXTTYPE\n");
	print("<SELECT NAME=\"texttype\">\n");
	print("<OPTION SELECTED>$H_PRE\n");
	print("<OPTION>$H_HTML\n");
	print("</SELECT><BR>\n");
    }
    
    # ��ʸ(���Ѥ���ʤ鸵����������)
    print("<textarea name=\"article\" rows=\"$TEXT_ROWS\" cols=\"$TEXT_COLS\">");
    &QuoteOriginalFile($File, $Name) if ($QuoteFlag == $QUOTE_ON);
    print("</textarea><br>\n");

    # ̾���ȥ᡼�륢�ɥ쥹��URL��ɽ����
    &EntryUserInformation;

    # �ܥ���
    &EntrySubmitButton;

    # ����«
    print("</form>\n");

    &MsgFooter;
}


###
## �񤭹��߲��̤Τ�����������ʸ��TextType��Board̾��ɽ����
#
sub EntryHeader {

    # Board̾�Τμ���
    local($BoardName) = &GetBoardInfo($BOARD);

    # ������ʸ
    print("<p>$H_AORI</p>\n");

    # Board̾; �����ϼ�ͳ������Ǥ���褦�ˤ�������
    print("$H_BOARD $BoardName<br>\n");

    # �������������
    &EntryIcon;

}


###
## �񤭹��߲��̤Τ�������������������ʬ��ɽ����
#
sub EntryIcon {

    local($FileName, $Title);

    print("$H_ICON\n");
    print("<SELECT NAME=\"icon\">\n");
    print("<OPTION SELECTED>$H_NOICON\n");

    # ��İ��ɽ��
    open(ICON, "$ICON_DIR/$BOARD.$ICONDEF_POSTFIX")
	|| (open(ICON, "$ICON_DIR/$DEFAULT_ICONDEF")
	    || &MyFatal(1, "$ICON_DIR/$DEFAULT_ICONDEF"));
    while(<ICON>) {
	chop;
	($FileName, $Title) = split(/\t/, $_);
	print("<OPTION>$Title\n");
    }
    close(ICON);
    print("</SELECT>\n");
    print("(<a href=\"$PROGRAM_FROM_BOARD/$BOARD?c=i\">$H_SEEICON</a>)<BR>\n");

}


###
## �񤭹��߲��̤Τ�����̾����e-mail addr.��URL��������ɽ����
#
sub EntryUserInformation {

    # ̾���ȥ᡼�륢�ɥ쥹��URL��
    print("$H_FROM <input name=\"name\" type=\"text\" size=\"$NAME_LENGTH\"><br>\n");
    print("$H_MAIL <input name=\"mail\" type=\"text\" size=\"$MAIL_LENGTH\"><br>\n");
    print("$H_URL <input name=\"url\" type=\"text\" value=\"http://\" size=\"$URL_LENGTH\"><br>\n");
    print("$H_FMAIL <input name=\"fmail\" type=\"checkbox\" value=\"on\"><br>\n")
	if ($SYS_FOLLOWMAIL);
    
    if ($SYS_ALIAS) {
	print("<p><a href=\"$PROGRAM_FROM_BOARD?c=as\">$H_SEEALIAS</a> // \n");
	print("<a href=\"$PROGRAM_FROM_BOARD?c=an\">$H_ALIASENTRY</a></p>\n");
	print("<p>$H_ALIASINFO</p>\n");
    }
}


###
## �񤭹��߲��̤Τ������ܥ����ɽ����
#
sub EntrySubmitButton {

    print("<p>$H_ENTRYINFO\n");
    print("<input type=\"submit\" value=\"$H_PUSHHERE\">\n");
    print("</p>\n");

}


###
## ����Id�ε�������Subject���äƤ��ơ���Ƭ�ˡ�Re: �פ�1�Ĥ����Ĥ����֤���
#
sub GetReplySubject {

    # Id��Board
    local($Id, $Board) = @_;

    # ���Ф���Subject
    local($Icon, $Subject) = '';

    # Subject�����������Ƭ�ˡ�Re: �פ����äĤ��Ƥ����������
    ($Icon, $Subject) = &GetSubject($Id, $Board);
    $Subject =~ s/^Re: //o;

    # ��Ƭ�ˡ�Re: �פ򤯤äĤ����֤���
    return("Re: $Subject");

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
## ���Ѥ���
#
sub QuoteOriginalArticle {

    # Id��Board
    local($Id, $Board) = @_;

    # ���Ѥ���ե�����
    local($QuoteFile) = &GetArticleFileName($Id, $Board);

    # ������ʬ��Ƚ�Ǥ���ե饰
    local($QuoteFlag) = 0;

    open(TMP, "<$QuoteFile") || &MyFatal(1, $QuoteFile);
    while(<TMP>) {

	# �������Ѵ�
	&jcode'convert(*_, 'euc');

	# ���ѽ�λ��Ƚ��
	$QuoteFlag = 0 if (/$COM_ARTICLE_END/);

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
	
	# ���ѳ��Ϥ�Ƚ��
	$QuoteFlag = 1 if (/$COM_ARTICLE_BEGIN/);

    }

    close(TMP);

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
	    s/<//go;
	    s/>//go;
	    print($DEFAULT_QMARK, $_);
	}

	# name tag?
	$NameFlag = 1 if (/<a\s+name\s*=\s*\"$Name/i);

	# ���ѳ��Ϥ�Ƚ��
	$QuoteFlag = 1 if (($NameFlag) && (/$COM_ARTICLE_BEGIN/));
	
    }
    close(TMP);

}


#/////////////////////////////////////////////////////////////////////
# ��������ɽ�����̴�Ϣ


###
## ��������ɽ������
#
sub ShowIcon {

    local($BoardName) = &GetBoardInfo($BOARD);
    local($FileName, $Title);

    # ɽ�����̤κ���
    &MsgHeader($SHOWICON_MSG);
    print("<p>$H_ICONINTRO</p>\n");
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

    &MsgFooter;

}


#/////////////////////////////////////////////////////////////////////
# �ץ�ӥ塼���̴�Ϣ


###
## �ץ�ӥ塼����
## (����������cgi'���ѿ�����Ƥʤ����������ɡ�����¿���Τǡġ� ^^;)
#
sub Preview {

    # TextType�μ���
    local($TextType) = $cgi'TAGS{'texttype'};

    # �ƥ�ݥ��ե�����κ���
    local($TmpFile) = &MakeTemporaryFile($TextType);

    # ɽ�����̤κ���
    &MsgHeader($PREVIEW_MSG, $BOARD);

    # ����«
    print("<form action=\"$PROGRAM_FROM_BOARD/$BOARD\" method =\"POST\">\n");
    print("<input name=\"file\" type=\"hidden\" value=\"$TmpFile\">\n");
    print("<input name=\"c\" type=\"hidden\" value=\"x\">\n");
    printf("<input name=\"id\" type=\"hidden\" value=\"%d\">\n",
	   $cgi'TAGS{'id'});

    # ������ʸ
    print("<p>$H_POSTINFO");
    print("<input type=\"submit\" value=\"$H_PUSHHERE\"></p>\n");

    # ��ǧ���뵭����ɽ��
    open(TMP, "$TmpFile");
    while(<TMP>) {
	print("$_");
    }

    # ����«
    print("</form>\n");

    &MsgFooter;

}


###
## ��ǧ�ѥƥ�ݥ��ե������������ƥե�����̾���֤���
#
sub MakeTemporaryFile {

    # TextType�μ���
    local($TextType) = @_;

    # Board̾�Τμ���
    local($BoardName) = &GetBoardInfo($BOARD);

    # �ƥ�ݥ��ե�����̾�μ���
    local($TmpFile) = &GetPath($BOARD, ".$ARTICLE_PREFIX.$$");

    # ���դ���Ф���
    local($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst)
	= localtime(time);
    local($InputDate)
	= sprintf("%d/%d(%02d:%02d)", $mon + 1, $mday, $hour, $min);
    # ��ʸ��̾��
    local($Text, $Name) = ($cgi'TAGS{'article'}, $cgi'TAGS{'name'});
    
    # ���ѥե����롢����Subject
    local($ReplyArticleFile, $ReplyArticleIcon, $ReplyArticleSubject)
	= ('', '', '');

    # �⤷���Ѥʤ���ѥե�����̾�����
    if ($cgi'TAGS{'id'} != 0) {
	$ReplyArticleFile = &GetArticleFileName($cgi'TAGS{'id'}, '');
        ($ReplyArticleIcon, $ReplyArticleSubject)
	    = &GetSubject($cgi'TAGS{'id'}, $BOARD);
    } elsif ($cgi'TAGS{'file'} ne '') {
        $ReplyArticleFile = $cgi'TAGS{'file'};
        $ReplyArticleSubject = &GetSubjectFromFile($cgi'TAGS{'file'});
    }

    # �����ꥢ�������å�
    $_ = $Name;
    if (/^#.*$/) {
        ($Name, $cgi'TAGS{'mail'}, $cgi'TAGS{'url'}) = &GetUserInfo($_);
	&MyFatal(7, $cgi'TAGS{'name'}) if ($Name eq "");
    }

    # �������å�
    &MyFatal(2, '') if ($cgi'TAGS{'subject'} eq "")
	|| ($cgi'TAGS{'article'} eq "")
	    || ($Name eq "")
		|| ($cgi'TAGS{'mail'} eq "");

    # ʸ��������å�
    &CheckName($Name);
    &CheckEmail($cgi'TAGS{'mail'});
    &CheckURL($cgi'TAGS{'url'});

    # ���֥������ȤΥ��������å�
    $_ = $cgi'TAGS{'subject'};
    &MyFatal(4, '') if (/</);

    # �ƥ�ݥ��ե�����˽񤭽Ф���
    open(TMP, ">$TmpFile") || &MyFatal(1, $TmpFile);

    # ��
    ($cgi'TAGS{'icon'} eq $H_NOICON)	
        ? printf(TMP "<strong>$H_SUBJECT</strong> %s<br>\n", $cgi'TAGS{'subject'})
            : printf(TMP "<strong>$H_SUBJECT</strong> <img src=\"%s\" alt=\"%s\"> %s<br>\n",
	        &GetIconURL($cgi'TAGS{'icon'}),
		$cgi'TAGS{'icon'},
		$cgi'TAGS{'subject'});

    # ��̾��
    if ($cgi'TAGS{'url'} eq "http://" || $cgi'TAGS{'url'} eq "") {
        # URL���ʤ����
        printf(TMP "<strong>$H_FROM</strong> %s<br>\n", $Name);
    } else {
        # URL��������
        printf(TMP "<strong>$H_FROM</strong> <a href=\"%s\">%s</a><br>\n", $cgi'TAGS{'url'}, $Name);
    }

	# �᡼��
	printf(TMP "<strong>$H_MAIL</strong> <a href=\"mailto:%s\">&lt;%s&gt;</a><br>\n",
		$cgi'TAGS{'mail'}, $cgi'TAGS{'mail'});

	# �ޥ���
	print(TMP "<strong>$H_HOST</strong> $REMOTE_HOST<br>\n");

	# �����
	print(TMP "<strong>$H_DATE</strong> $InputDate<br>\n");

	# ��ȿ��(���Ѥξ��)
	if ($cgi'TAGS{'id'} != 0) {
		printf(TMP "<strong>$H_REPLY</strong> [$BoardName: %d] $ReplyArticleIcon<a href=\"$ReplyArticleFile\">$ReplyArticleSubject</a><br>\n", $cgi'TAGS{'id'});
	} elsif ($cgi'TAGS{'qurl'} ne '') {
		printf(TMP "<strong>$H_REPLY</strong> <a href=\"%s\">$ReplyArticleSubject</a><br>\n", $cgi'TAGS{'qurl'});
	}

	# ȿ�������ä���᡼��
	print(TMP "$COM_FMAIL_BEGIN\n");
	printf(TMP "%s\n", $cgi'TAGS{'mail'}) if ($cgi'TAGS{'fmail'} eq "on");
	print(TMP "$COM_FMAIL_END\n");

	# �ڤ���
	print(TMP "------------------------<br>\n");

	# article begin
	print(TMP "$COM_ARTICLE_BEGIN\n");

	# TextType��������
	print(TMP "<pre>\n") if ((! $SYS_TEXTTYPE) || ($TextType eq $H_PRE));

	# ����
	$Text = &tag_secure'decode($Text);
	printf(TMP "%s\n", $Text);

	# TextType�Ѹ����
	print(TMP "</pre>\n") if ((! $SYS_TEXTTYPE) || ($TextType eq $H_PRE));

	# article end
	print(TMP "$COM_ARTICLE_END\n");
	print(TMP "<hr>\n");
	close(TMP);

	# �ե�����̾���֤���
	return($TmpFile);
}


#/////////////////////////////////////////////////////////////////////
# ��Ͽ����̴�Ϣ


###
## ��Ͽ�����
#
sub Thanks {

    # �ƥ�ݥ��ե�����̾�Ȱ��Ѥ���������Id
    local($TmpFile, $Id) = @_;

    # �����˵��������������ե������줿�����ˤ��λݽ񤭹��ࡣ
    &MakeNewArticle($TmpFile, $Id);# 

    # ɽ�����̤κ���
    &MsgHeader($THANKS_MSG, $BOARD);

    print("<p>$H_THANKSMSG</p>");
    print("<form action=\"$PROGRAM_FROM_BOARD/$BOARD\" method =\"POST\">\n");
    print("<input name=\"c\" type=\"hidden\" value=\"l\">\n");
    print("<input name=\"num\" type=\"hidden\" value=\"1\">\n");
    print("<input type=\"submit\" value=\"$H_BACK\">\n");
    print("</form>\n");

    &MsgFooter;
}


###
## ��������Ƥ��줿����������
#
sub MakeNewArticle {

    # �ƥ�ݥ��ե�����̾�����Ѥ���������Id
    local($TmpFile, $Id) = @_;

    # Board̾�Τμ���
    local($BoardName) = &GetBoardInfo($BOARD);

    # �����ֹ������ե�����
    local($ArticleNumFile) = &GetPath($BOARD, $ARTICLE_NUM_FILE_NAME);

    # �����ε����ֹ�ȥե�����̾
    local($ArticleId, $ArticleFile);

    # ���֥������ȡ���������̾��
    local($Icon, $Subject, $InputDate, $Name, $Title);

    # �ƥ�ݥ��ե����뤫��Subject������Ф�
    ($Icon, $Subject, $InputDate, $Name) = &GetHeader($TmpFile);

    # ��å��򤫤���
    &lock;

    # �����ֹ�����
    $ArticleId = &GetandAddArticleId($ArticleNumFile);

    # �����Υե�����̾�����
    $ArticleFile = &GetArticleFileName($ArticleId, $BOARD);

    # �����Υե�����˥إå���ʬ��񤭹���
    open(ART, ">$ArticleFile") || &MyFatal(1, $ArticleFile);

    # �����إå��κ���
    printf(ART "<title>[$BoardName: %d] $Subject</title>\n", $ArticleId);
    print(ART "<body bgcolor=\"$BG_COLOR\" TEXT=\"$TEXT_COLOR\" LINK=\"$LINK_COLOR\" ALINK=\"$ALINK_COLOR\" VLINK=\"$VLINK_COLOR\">\n");
    printf(ART "<a href=\"%s\">$H_NEXTARTICLE</a> // ",
	   &GetArticleFileName(($ArticleId + 1), ''));
    print(ART "<a href=\"$PROGRAM_FROM_BOARD/$BOARD?c=f&id=$ArticleId\">$H_REPLYTHISARTICLE</a> // ");
    print(ART "<a href=\"$PROGRAM_FROM_BOARD/$BOARD?c=q&id=$ArticleId\">$H_REPLYTHISARTICLEQUOTE</a> // ");
    print(ART "<a href=\"$PROGRAM_FROM_BOARD/$BOARD?c=t&id=$ArticleId\">$H_READREPLYALL</a>\n");
    print(ART "<hr>\n");

    # �����إå��λϤޤ�
    print(ART "$COM_HEADER_BEGIN\n");

    # �ܥǥ�����Ƭ�ˤܡ���̾�ȵ����ֹ桢��������
    printf(ART "<strong>$H_SUBJECT</strong> [$BoardName: %d] $Icon$Subject<br>\n", $ArticleId);
    
    # �ƥ�ݥ��ե����뤫��ε����Τ��ԡ�
    open(TMP, "$TmpFile") || &MyFatal(1, $TmpFile);

    # Subject�Ԥ������ѤߤʤΤ�1�����Ф���
    $Dust = <TMP>;

    while(<TMP>) {
	print(ART $_);
    }
    close(TMP);

    # �ƥ�ݥ��ե�����κ��
    unlink("$TmpFile");

    # �����դä��κ���
    print(ART "$H_FOLLOW\n<ol>\n");
    close(ART);

    # �ե������줿�����˥ե������줿���Ȥ�񤭹��ࡣ
    &ArticleWasFollowed($Id, $ArticleId, $Icon, $Subject, $Name)
	if ($Id != 0);

    # DB�ե��������Ƥ��줿�������ɲ�
    &AddDBFile($ArticleId, $Id, $Name, $InputDate, $Subject, $Icon);

    # ��å��򳰤���
    &unlock;

}


###
## ������Ѥ�ʸ���󤫤�Title����(<img...>�������)
#
sub MakeTitleFromSubject {

    # ��
    local($Subject) = @_;

    $Subject =~ m/^<img src=\"[^>]*> (.*)$/o;
    return($1);

}


###
## �����ֹ���äƤ���(�ֹ��1������)��
#
sub GetandAddArticleId {

    # �ե�����̾�����
    local($ArticleNumFile) = @_;

    # �����ֹ�
    local($ArticleId) = 0;

    # �����ֹ��ե����뤫���ɤ߹��ࡣ�ɤ�ʤ��ä���0�ΤޤޡġĤΤϤ���
    open(AID, "$ArticleNumFile");
    while(<AID>) {
	chop;
	$ArticleId = $_;
    }
    close(AID);

    # 1���䤷�ƽ񤭹��ࡣ
    open(AID, ">$ArticleNumFile") || &MyFatal(1, $ArticleNumFile);
    print(AID $ArticleId + 1, "\n");
    close(AID);

    # �����������ֹ���֤���
    return($ArticleId + 1);
}


###
## �ե������줿�����Υեå��˥ե������줿���Ȥ�񤭹��ࡣ
#
sub ArticleWasFollowed {

    # �ե������줿������Id���ܡ��ɤ�̾�Ρ�
    # �ե�������������Id�����֥������ȡ�̾��
    local($Id, $FollowArticleId, $Ficon, $Fsubject, $Fname) = @_;

    # �ե������줿�����ե�����
    local($ArticleFile) = &GetArticleFileName($Id, $BOARD);
    
    # �ե������������ե�����
    local($FollowArticleFile) = &GetArticleFileName($FollowArticleId, '');
    
    # ���ե����뤫��ȿ���᡼��ΰ���������Ф�
    local($Icon, $Subject, $Date, $Name, @Fmail)
	= &GetHeader($ArticleFile);
    
    # ɬ�פʤ�᡼������롣
    &FollowMail($Name, $Date, $Subject, $Id, $Fname, $Fsubject,
		$FollowArticleId, @Fmail)
			    if (($SYS_FOLLOWMAIL) && (@Fmail[0] ne ""));
    
    # ���˥ե���������ɲ�
    open(FART, ">>$ArticleFile") || &MyFatal(1, $ArticleFile);
    printf(FART "<li>$Ficon<a href=\"$FollowArticleFile\">$Fsubject</a> $H_REPLYNOTE\n", $Fname);
    close(FART);
}


###
## DB�ե�����˽񤭹���
#
sub AddDBFile {

    # ����Id��̾�������������ꡢ����
    local($Id, $Fid, $Name, $InputDate, $Subject, $Icon) = @_;
    
    # ��Ͽ�ե�����
    local($File) = &GetPath($BOARD, $DB_FILE_NAME);
    
    # Add to DB file
    open(DB, ">>$File") || &MyFatal(1, $File);
    printf(DB "%s\t%s\t%s\t%s\t%s\t%s\n",
	   $Id, $Fid, $Name, $InputDate, $Subject, $Icon);
    close(DB);
}


#/////////////////////////////////////////////////////////////////////
# ���ս祽���ȴ�Ϣ


###
## ���ս�˥����ȡ�
#
sub SortArticle {

    # ɽ������Ŀ������
    local($Num) = @_;

    # �����ֹ������ե�����
    local($ArticleNumFile) = &GetPath($BOARD, $ARTICLE_NUM_FILE_NAME);

    # DB�ե�����
    local($DBFile) = &GetPath($BOARD, $DB_FILE_NAME);

    # �ǿ������ֹ�����
    local($ArticleToId) = &GetArticleId($ArticleNumFile);

    # ��������­��ʤ�����Ĵ��
    $Num = $ArticleToId if ($ArticleToId < $Num);

    # Board̾�Τμ���
    local($BoardName) = &GetBoardInfo($BOARD);

    # ��äƤ���ǽ�ε����ֹ�����
    local($ArticleFromId) = $ArticleToId - $Num + 1;
    local($ListFlag) = 0;
    local(@Lines) = ();
    local($Id, $Fid, $Name, $Date, $Title, $Icon) = ("", "", "", "", "", "");
    local($ArticleFile) = "";

    # �����ߡ�DB�ե����뤬�ʤ���в���ɽ�����ʤ���
    open(DB, "<$DBFile");
    while(<DB>) {
	chop;

	next if (/^\#/);

	($Id, $Fid, $Name, $Date, $Title, $Icon) = split(/\t/, $_);
	$ListFlag = 1 if ($ArticleFromId <= $Id);

	if ($ListFlag) {
	    # �ɲä���ե������̾��
	    $ArticleFile = &GetArticleFileName($Id, '');

	    push(Lines, sprintf("<li><strong>$Id .</strong> $Icon<a href=\"%s\">$Title</a> [$Name] $Date\n", $ArticleFile));
	}
    }

    # ɽ�����̤κ���
    &MsgHeader("$BoardName: $SORT_MSG", $BOARD);

    &BoardHeader;

    print("<hr>\n");
    print("<ul>\n");

    # ������ɽ��
    if ($SYS_BOTTOMTITLE) {
	# ��������������
	foreach (@Lines) {print("$_");}
    } else {
	# ��������������
	foreach (reverse @Lines) {print("$_");}
    }

    print("</ul>\n");
    &MsgFooter;

}


#/////////////////////////////////////////////////////////////////////
# thread�̥����ȥ�ɽ����Ϣ


###
## �����������Υ����ȥ��thread�̤�n�Ĥ�ɽ����
#
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
    local($Line) = "";
    local($Id, $Fid, $Name, $Date, $Title, $Icon) = ("", "", "", "", "", "");
    local($ArticleFile) = "";

    # ������0�ʤ�ǽ餫������
    if ($Num == 0) {
	$ArticleFromId = 1;
    } else {
	# ��������­��ʤ�����Ĵ��
	$Num = $ArticleToId if ($ArticleToId < $Num);

	# ��äƤ���ǽ�ε����ֹ�����
	$ArticleFromId = $ArticleToId - $Num + 1;
    }

    # �����ߡ�DB�ե����뤬�ʤ���в���ɽ�����ʤ���
    open(DB, "<$DBFile");
    while(<DB>) {
	chop;

	next if (/^\#/);

	($Id, $Fid, $Name, $Date, $Title, $Icon) = split(/\t/, $_);
	$ListFlag = 1 if ($ArticleFromId <= $Id);

	if ($ListFlag) {

	    # �ɲä���ե������̾��
	    $ArticleFile = &GetArticleFileName($Id, '');

	    # �ɲä����
	    $Line = ($Icon)
		? sprintf("<li><strong>$Id .</strong> $Icon<a href=\"%s\">$Title</a> [$Name] $Date", $ArticleFile)
		    : sprintf("<li><strong>$Id .</strong> <a href=\"%s\">$Title</a> [$Name] $Date", $ArticleFile);

	    # �ɲ�
	    @Lines = ($Fid)
		? &AddTitleFollow($Fid, $Line, @Lines)
		    : &AddTitleNormal($Line, @Lines);
	}
    }
    close(DB);

    # ɽ�����̤κ���
    &MsgHeader("$BoardName: $VIEW_MSG", $BOARD);

    &BoardHeader;

    print("<hr>\n");
    print("<ul>\n");

    # ������ɽ��
    foreach (@Lines) {
	s/$NULL_LINE//o;
	print("$_\n");
	    
    }

    print("</ul>\n");
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

    # �ե��������ե�����
    local($FollowedArticleFile) = &GetArticleFileName($Fid, '');

    # Follow Flag
    local($AddFlag, $Nest, $NextLine) = (0, 0, ''); 

    # �����ȥ�ꥹ�ȤΥե饰
    local($TitleListFlag) = 0;

    while($_ = shift(Lines)) {

	# ���Τޤ޽񤭽Ф���
	push(NewLines, $_);

	# �����ȥ�ꥹ���桢�������Ƥε������褿�顢
	if (/$FollowedArticleFile/) {

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
#
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
    &MsgHeader("$BoardName: $NEWARTICLE_MSG", $BOARD);

    &BoardHeader;

    print("<hr>\n");

    if ($SYS_BOTTOMTITLE) {

	# ����
	for ($i = $ArticleFromId; ($i <= $ArticleToId); $i++) {
	    &ViewOriginalArticle($i);
		print("<hr>\n");
	}
	
    } else {

	# ���
	for ($i = $ArticleToId; ($i >= $ArticleFromId); $i--) {
	    &ViewOriginalArticle($i);
		print("<hr>\n");
	}

    }

    &MsgFooter;
}


###
## �����ֹ���äƤ���(�ֹ�������ʤ�)��
#
sub GetArticleId {

    # �ե�����̾�����
    local($ArticleNumFile) = @_;

    # �����ֹ�
    local($ArticleId);

    # �ʤ��ä���0���֤�(�����Τ�?)
    open(AID, "$ArticleNumFile") || return(0);
    while(<AID>) {
	chop;
	$ArticleId = $_;
    }
    close(AID);

    # �����ֹ���֤���
    return($ArticleId);
}


#/////////////////////////////////////////////////////////////////////
# �ե����ޤȤ��ɤߴ�Ϣ


###
## �ե�������������ɽ����
#
sub ThreadArticle {

    # ��������Id�����
    local($Id) = @_;

    # Board̾�Τμ���
    local($BoardName) = &GetBoardInfo($BOARD);

    # ɽ�����̤κ���
    &MsgHeader("$BoardName: $THREADARTICLE_MSG", $BOARD);

    # �ᥤ��ؿ��θƤӽФ�(��������)
    print("<ul>\n");
    &ThreadArticleMain('subject only', $Id);
    print("</ul>\n");

    # �ᥤ��ؿ��θƤӽФ�(����)
    &ThreadArticleMain('', $Id);

    &MsgFooter;
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

	# ��������ɽ��
	print("<a name=\"$Id\">��</a><br>\n");
	print("<hr>\n");
	&ViewOriginalArticle($Id);

    }

    # �ե���������ɽ��
    foreach (@FollowIdList) {

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

    # ���ե�����
    local($File) = &GetArticleFileName($Id, $BOARD);

    # �ե�����ʬ��Ƚ�Ǥ���ե饰
    local($QuoteFlag) = 0;

    # �ꥹ��
    local(@Result) = ();

    open(TMP, "<$File") || &MyFatal(1, $File);
    while(<TMP>) {

	# �������Ѵ�
	&jcode'convert(*_, 'euc');

	# �ե�����ʬ���Ϥ�Ƚ��
	$QuoteFlag = 1 if (/$COM_ARTICLE_END/);

	# �ե���Id�μ���
	($QuoteFlag == 1) || next;
	push(Result, $1)
	    if (/<a href=\"$ARTICLE_PREFIX\.([0-9]*)\.html\">/);
    }
    close(TMP);
    
    return(@Result);
}


###
## �����γ��פ�ɽ��
#
sub PrintAbstract {

    # Id
    local($Id) = @_;

    # ���Ѥ���ե�����
    local($File) = &GetArticleFileName($Id, $BOARD);

    # �ꡢ���ա�̾��
    local($Icon, $Subject, $InputDate, $Name);

    # �����ե����뤫��Subject������Ф�
    ($Icon, $Subject, $InputDate, $Name) = &GetHeader("$File");

    printf("<li><strong>$Id .</strong> %s<a href=\"\#$Id\">$Subject</a> [$Name] $InputDate\n", $Icon);

}


#/////////////////////////////////////////////////////////////////////
# ����������Ϣ


###
## �����θ���(ɽ�����̺���)
#
sub SearchArticle {

    # �������
    local($Key) = @_;

    # Board̾�Τμ���
    local($BoardName) = &GetBoardInfo($BOARD);

    # ɽ�����̤κ���
    &MsgHeader("$BoardName: $SEARCHARTICLE_MSG", $BOARD);

    # ����«
    print("<form action=\"$PROGRAM_FROM_BOARD/$BOARD\" method =\"POST\">\n");
    print("<input name=\"c\" type=\"hidden\" value=\"s\">\n");

    # �������������
    print("<p>$H_INPUTKEYWORD");
    print("<input type=\"submit\" value=\"$H_PUSHHERE\"></p>\n");
    print("<p>$H_KEYWORD:\n");
    print("<input name=\"key\" size=\"$KEYWORD_LENGTH\"></p>\n");
    print("<hr>\n");

    # ������ɤ����Ǥʤ���С����Υ�����ɤ�ޤ൭���Υꥹ�Ȥ�ɽ��
    &SearchArticleList($Key) unless ($Key eq "");

    &MsgFooter;
}


###
## �����θ���(������̤�ɽ��)
#
sub SearchArticleList {

    # �������
    local($Key) = @_;

    # DB�ե�����
    local($DBFile) = &GetPath($BOARD, $DB_FILE_NAME);

    local($Id, $Fid, $Name, $Date, $Title, $Icon) = ("", "", "", "", "", "");
    local($ArticleFile, $ArticleFilePath, $HitFlag, $Line) = ("", "", 0, "");

    # �ꥹ�ȳ���
    print("<dl>\n");

    # �ե�����򳫤���DB�ե����뤬�ʤ����not found.
    open(DB, "<$DBFile");
    while(<DB>) {

	next if (/^\#/);

	($Id, $Fid, $Name, $Date, $Title, $Icon) = split(/\t/, $_);
	$ArticleFile = &GetArticleFileName($Id, '');
	$ArticleFilePath = &GetArticleFileName($Id, $BOARD);

	# �ե�����򸡺�
	$Line = &SearchArticleKeyword($ArticleFilePath, $Key);

	if ($Line ne "") {
	    $Line =~ s/<[^>]*>//go;
	    $Line =~ s/&/&amp;/go;
	    $Line =~ s/\"/&quot;/go;
	    print("<dt><strong>$Id .</strong> $Icon<a href=\"%s\">$Title</a> [$Name] $Date\n", $ArticleFile);
	    print("<dd>$Line\n");
	    $HitFlag = 1;
	}
    }
    close(DB);

    # �ҥåȤ��ʤ��ä���
    print("<dt>$H_NOTFOUND\n") unless ($HitFlag = 1);

    # �ꥹ���Ĥ���
    print("</dl>\n");
}


###
## �����θ���(������̥ᥤ��)
#
sub SearchArticleKeyword {

    # �ե�����̾�ȥ������
    local($File, $Key) = @_;

    # ��������
    open(ARTICLE, "<$File") || &MyFatal(1, $File);
    while(<ARTICLE>) {

	# �������Ѵ�
	&jcode'convert(*_, 'euc');

	# TAG�������
	s/<[^>]*>//go;

	# �ҥå�?
	(/$Key/) && return($_);
    }

    # �ҥåȤ���
    return("");
}


#/////////////////////////////////////////////////////////////////////
# �����ꥢ����Ϣ


###
## �����ꥢ������Ͽ���ѹ�
#
sub AliasNew {

    # ɽ�����̤κ���
    &MsgHeader($ALIASNEW_MSG);

    # ������Ͽ/��Ͽ���Ƥ��ѹ�
    print("<p>$H_ALIASTITLE</p>\n");
    print("<p>\n");
    print("<form action=\"$PROGRAM\" method =\"POST\">\n");
    print("<input name=\"c\" type=\"hidden\" value=\"am\">\n");
    print("$H_ALIAS <input name=\"alias\" type=\"text\" value=\"#\" size=\"$NAME_LENGTH\"><br>\n");
    print("$H_FROM <input name=\"name\" type=\"text\" size=\"$NAME_LENGTH\"><br>\n");
    print("$H_MAIL <input name=\"email\" type=\"text\" size=\"$MAIL_LENGTH\"><br>\n");
    print("$H_URL <input name=\"url\" type=\"text\" value=\"http://\" size=\"$URL_LENGTH\"><br>\n");
    print("<input type=\"submit\" value=\"$H_PUSHHERE\">\n");
    print("$H_ALIASNEWCOM\n");
    print("</form></p>\n");
    
    print("<hr>\n");
    
    # ���
    print("<p>$H_ALIASDELETE</p>\n");
    print("<p>\n");
    print("<form action=\"$PROGRAM\" method =\"POST\">\n");
    print("<input name=\"c\" type=\"hidden\" value=\"ad\">\n");
    print("$H_ALIAS <input name=\"alias\" type=\"text\" size=\"$NAME_LENGTH\"><br>\n");
    print("<input type=\"submit\" value=\"$H_PUSHHERE\">\n");
    print("$H_ALIASDELETECOM\n");
    print("</form></p>\n");
    
    print("<hr>\n");
    
    # ����
    print("<p>\n");
    print("<form action=\"$PROGRAM\" method =\"POST\">\n");
    print("<input name=\"c\" type=\"hidden\" value=\"as\">\n");
    print("<input type=\"submit\" value=\"$H_PUSHHERE\">\n");
    print("$H_ALIASREFERCOM\n");
    print("</form></p>\n");
    
    # ����«
    &MsgFooter;

}


###
## ��Ͽ/�ѹ�
#
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
    &MsgFooter;
    
}


###
## �����ꥢ�������å�
#
sub AliasCheck {

    local($A, $N, $E, $U) = @_;

    # �������å�
    &MyFatal(2, '') if ($A eq "")
	|| ($N eq "")
	    || ($E eq "");

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
    
    &MsgFooter;

}


###
## �����ꥢ���ե�������ɤ߹����Ϣ�������������ࡣ
## CAUTION: %Name, %Email, %Host, %URL������ޤ���
#
sub CashAliasData {

    # �ե�����
    local($File) = @_;
    
    local($A, $N, $E, $H, $U);
    
    # ������ࡣ
    open(ALIAS, "<$File") || &MyFatal(1, $File);
    while(<ALIAS>) {
	
	# �������Ѵ�
	&jcode'convert(*_, 'euc');

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
##          $Name���ΤȽ񤭹��ޤʤ���
#
sub WriteAliasData {

    # �ե�����
    local($File) = @_;
    local($Alias);

    # ��å��򤫤���
    &lock;

    # �񤭽Ф�
    open(ALIAS, ">$File") || &MyFatal(1, $File);
    foreach $Alias (sort keys(%Name)) {
	($Name{$Alias}) && printf(ALIAS "%s\t%s\t%s\t%s\t%s\n",
				  $Alias, $Name{$Alias}, $Email{$Alias},
				  $Host{$Alias}, $URL{$Alias});
    }
    close(ALIAS);
    
    # ��å��򳰤���
    &unlock;

}


###
## �桼�������ꥢ������桼����̾�����᡼�롢URL���äƤ��롣
#
sub GetUserInfo {

    # �������륨���ꥢ��̾
    local($Alias) = @_;

    # �����ꥢ����̾�����᡼�롢�ۥ��ȡ�URL
    local($A, $N, $E, $H, $U);

    # �ե�����򳫤�
    open(ALIAS, "<$USER_ALIAS_FILE")
	# �ե����뤬�ʤ��餷���ΤǤ��褦�ʤ顣
	|| return('', '', '');
    
    # 1��1�ĥ����å���
    while(<ALIAS>) {
	
	# �������Ѵ�
	&jcode'convert(*_, 'euc');

	chop;
	
	# ʬ��
	($A, $N, $E, $H, $U) = split(/\t/, $_);
	
	# �ޥå����ʤ��㼡�ء�
	next unless ($A eq $Alias);
	
	# ����ˤ����֤�
	return($N, $E, $U);
    }
    
    # �ҥåȤ���
    return('', '', '');
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
	
	# �������Ѵ�
	&jcode'convert(*_, 'euc');

	chop;
	# �ޥå����ʤ��㼡�ء�
	next unless (/^$Alias\t(.*)$/);
	$BoardName = $1;
	return($BoardName);
    }

    # �ҥåȤ���
    return('');
}


#/////////////////////////////////////////////////////////////////////
# ����¾���̴ؿ�


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
    ($String =~ (/^http:\/\/.*/)) || ($String =~ (/^http:\/\/$/))
	|| ($String eq "") || &MyFatal(8, 'URL');

}


###
## �����Υإå���ɽ��
#
sub MsgHeader {

    # message and board
    local($Message, $Board) = @_;
    
    &cgi'header;
    print("<html>", "\n");
    print("<head>", "\n");
    print("<title>$Message</title>", "\n");
    if (! $Board) {
	print("<base href=\"$SCRIPT_URL\">\n");
    } else {
	print("<base href=\"$DIR_URL$Board/\">\n");
    }
    print("</head>", "\n");
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
    print("</body>");
    print("</html>");

}


###
## ��å��ط�
#

# ��å�
sub lock {

    # ��å��ե�����򳫤�
    open(LOCK, "$LOCK_FILE") || &MyFatal(1, $LOCK_FILE);

    # ��å��򤫤���
    flock(LOCK, $LOCK_EX);
}

# �����å�
sub unlock {

    # ��å�����
    flock(LOCK, $LOCK_UN);

    # ��å��ե�������Ĥ���
    close(LOCK);
}


###
## ��������ɽ��
#
sub ViewOriginalArticle {

    # Id
    local($Id) = @_;

    # ���Ѥ���ե�����
    local($QuoteFile) = &GetArticleFileName($Id, $BOARD);

    # ������ʬ��Ƚ�Ǥ���ե饰
    local($QuoteFlag) = 0;

    open(TMP, "<$QuoteFile") || &MyFatal(1, $QuoteFile);
    while(<TMP>) {

	# �������Ѵ�
	&jcode'convert(*_, 'euc');

	# ���ѽ�λ��Ƚ��
	$QuoteFlag = 0 if (/$COM_ARTICLE_END/);

	# ����ʸ�����ɽ��
	if ($QuoteFlag == 1) {
	    print("$_");
	}

	# ���ѳ��Ϥ�Ƚ��
	$QuoteFlag = 1 if ((/$COM_HEADER_BEGIN/) ||
			   (/$COM_ARTICLE_BEGIN/));

    }
    close(TMP);

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
## ʸ�������<a href="$ARTICLE_PREFIX.??.html">�����ä��顢
## BoardName�򤨤Ƥ����֤���
#
sub URLConvert {

    # string
    local($String) = @_;
    local($File, $URL);

    $String =~ s#href=\"../#href=\"#gio;
    $String =~ s#src=\"../#src=\"#gio;
    ($String =~ m/<a href=\"($ARTICLE_PREFIX\.[^\.]*\.html)\">/)
	|| return($String);

    $File = $1;
    $URL = &GetURL($BOARD, $File);

    $String =~ s/<a href=\"$File\">/<a href=\"$URL\">/g;

    return($String);

}


###
## ȿ�������ä����Ȥ�᡼�뤹�롣
#
sub FollowMail {

    # ���褤����
    local($Name, $Date, $Subject, $Id, $Fname, $Fsubject, $Fid, @To) = @_;

    local($BoardName) = &GetBoardInfo($BOARD);
    local($URL) = $DIR_URL . &GetURL($BOARD, &GetArticleFileName($Id, ''));
    local($FURL) = $DIR_URL . &GetURL($BOARD, &GetArticleFileName($Fid, ''));
    
    # Subject
    local($MailSubject) = "The article was followed.";

    # Message
    local($Message) = "$SYSTEM_NAME����Τ��Τ餻�Ǥ���\n\n$Date�ˡ�$BoardName�פ��Ф��ơ�$Name�פ��󤬽񤤤���\n��$Subject��\n$URL\n���Ф��ơ�\n��$Fname�פ��󤫤�\n��$Fsubject�פȤ�����Ǥ�ȿ��������ޤ�����\n\n�����֤Τ������\n$FURL\n�������������\n\n�Ǥϼ��餷�ޤ���";

    # �᡼������
    &SendMail($MailSubject, $Message, @To);
}


###
## �ܡ���̾�Τ�Id����ե�����Υѥ�̾����Ф���
#
sub GetArticleFileName {

    # Id��Board
    local($Id, $Board) = @_;

    # Board�����ʤ�Board�ǥ��쥯�ȥ��⤫�����С�
    # ���Ǥʤ���Х����ƥफ������
    $Board
	? return("$Board/$ARTICLE_PREFIX.$Id.html")
	    : return("$ARTICLE_PREFIX.$Id.html");
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
## �ܡ���̾�Τȥե�����̾���顢���Υե������URL����Ф���
#
sub GetURL {

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

    local($FileName, $Title);
    local($TargetFile) = "";

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

    return("../$ICON_DIR/$TargetFile");
}


###
## ���������URL���顢��������̾�����
#
sub GetIconName {

    # ���������URL
    local($IconURL) = @_;

    $IconURL =~ s!^.*/!!o;
    
    local($FileName, $Title) = ("", "");
    local($TargetName) = "";

    # ��İ��ɽ��
    open(ICON, "$ICON_DIR/$BOARD.$ICONDEF_POSTFIX")
	|| (open(ICON, "$ICON_DIR/$DEFAULT_ICONDEF")
	    || &MyFatal(1, "$ICON_DIR/$DEFAULT_ICONDEF"));
    while(<ICON>) {
	chop;
	($FileName, $Title) = split(/\t/, $_);
	$TargetName = $Title if ($FileName eq $IconURL);
    }
    close(ICON);

    return("$TargetName");
}


###
## ����Id�ε�������Subject���äƤ��롣
#
sub GetSubject {

    # Id��Board
    local($Id, $Board) = @_;

    # Subject����Ф��ե�����
    local($ArticleFile) = &GetArticleFileName($Id, $Board);

    # ���Ф���Subject
    local($Icon, $Subject) = ('', '');

    # �����ե����뤫��Subjectʸ�������Ф���
    open(TMP, "<$ArticleFile") || &MyFatal(1, $ArticleFile);
    while(<TMP>) {

	# �������Ѵ�
	&jcode'convert(*_, 'euc');

	if (/^<strong>$H_SUBJECT<\/strong> \[[^\]]*\] (<img src=[^>]*> )(.*)<br>$/) {
	    $Icon = $1;
	    $Subject = $2;
	} elsif (/^<strong>$H_SUBJECT<\/strong> \[[^\]]*\] (.*)<br>$/) {
	    $Subject = $1;
	}
    }
    close(TMP);
    
    # �֤�
    return($Icon, $Subject);
}


###
## ���뵭�����饢�������ꡢ���ա�̾������Ф���
#
sub GetHeader {

    # �ե�����̾
    local($File) = @_;
    # �ꡢ���ա�̾��
    local($Icon, $Subject, $Date, $Name, @Fmail) = ('', '', '', '', ());

    # �ե�����򳫤���
    open(TMP, "<$File") || &MyFatal(1, $File);
    while(<TMP>) {

	# subject����Ф���
	if (/^<strong>$H_SUBJECT<\/strong> \[[^\]]*\] (<img src=[^>]*> )(.*)<br>$/) {
	    $Icon = $1;
	    $Subject = $2;
	} elsif (/^<strong>$H_SUBJECT<\/strong> (<img src=[^>]*> )(.*)<br>$/) {
	    $Icon = $1;
	    $Subject = $2;
	} elsif (/^<strong>$H_SUBJECT<\/strong> \[[^\]]*\] (.*)<br>$/) {
	    $Subject = $1;
	} elsif (/^<strong>$H_SUBJECT<\/strong> (.*)<br>$/) {
	    $Subject = $1;
	}
	
	# ���դ���Ф���
	if (/^<strong>$H_DATE<\/strong> (.*)<br>$/) {$Date = $1;}
	
	# ̾������Ф���
	if (/^<strong>$H_FROM<\/strong> <a[^>]*>(.*)<\/a><br>$/) {
	    $Name = $1;
	} elsif (/^<strong>$H_FROM<\/strong> (.*)<br>$/) {
	    $Name = $1;
	}
	
	# ȿ���᡼��ΰ������Ф���
	if (/^$COM_FMAIL_BEGIN$/) {
	    while(<TMP>) {
		chop;
		last if (/^$COM_FMAIL_END$/);
		push(Fmail, $_);
	    }
	}
    }
    close(TMP);
    
    # �֤�
    return($Icon, $Subject, $Date, $Name, @Fmail);
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

    # subject���᡼��Υե�����̾������Υꥹ��
    local($Subject, $Message, @To) = @_;

    # �᡼���ѥե�����򳫤�
    open(MAIL, "| $MAIL2") || &MyFatal(9, '');

    # To�إå�
    foreach (@To) {

	# �������Ѵ�
	&jcode'convert(*_, 'jis');

	print(MAIL "To: $_\n");
    }
    
    # From�إå�
    # Errors-To�إå�
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

    open(LOCAL, ">$LocalFile") || die "Can't open $LocalFile.\n";
    while (<S>) {

	# �������Ѵ�
	&jcode'convert(*_, 'euc');

	# �񤭹���
	print(LOCAL $_);
    }
    
    close(LOCAL);
    return(1);
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
    } else {
	print("<p>���顼�ֹ�����: ������Ǥ�����");
	print("���Υ��顼��������������");
	print("<a href=\"mailto:$MAINT\">$MAINT</a>�ޤ�");
	print("���Τ餻��������</p>\n");
    }
    
    &MsgFooter;
    exit 0;
}
