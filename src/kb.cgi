#!/usr/local/bin/GNU/perl
#
# $Id: kb.cgi,v 1.4 1995-11-08 09:18:22 nakahiro Exp $
#
# $Log: kb.cgi,v $
# Revision 1.4  1995-11-08 09:18:22  nakahiro
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


# ToDo:
#	��	Subject��Re:�ˤ���
#	��	In-Reply-To:��Ĥ���
#	��	�֡��˥ե�������Ƥ��ޤ��פ�Ĥ��롣
#	��	user alias
#	��	board-name alias
#	��	indent
#	��	indent���¤��ؤ�
#	��	Error�ؿ�
#	��	�����ȥ�ꥹ�ȤΥե����ޥå�
#	��	�־�ε�����ȿ������פʤ��ѡ�
#	��	HTML or Plain Text
#	��	^M�������
#	��	�ǿ��ε���n��!
#	��	�ޤȤ��ɤ�(thread)
#	��	���ꤷ����������Ѥ��롣
#	��	���ꤷ�������ؤ�Reference��Ĥ���
#		�־�ءסֲ��ءפΥ�󥯵�ǽ���ɲ�(��/�����ѻ�?)
#		�ޤȤ��ɤߤλ���thread��狼��䤹�����빩�פ�
#		��ʬ���ե�����
#		alias����Ͽ��ǽ
#		Subject����Ƭ��Icon��Ĥ�����
#		Board��ͳ�����򤹤�


###
## �桼��������������(ư��������ɬ���ѹ�����!)
#

#
# �����Ԥ�e-mail addr.
#
$Maint = "nakahiro@ohara.info.waseda.ac.jp";

#
# �ץ���ब¸�ߤ���ǥ��쥯�ȥ��URLɽ��
#
$PROGRAM_DIR_URL = "/~nakahiro";


###
## �桼��������������(�ä��ѹ����ʤ��Ǥ�OK)
#

#
# ���Υץ�����̾��
#
$PROGRAM_NAME = "kb.cgi";

#
# �����Υץ�ե�����
# �����ե����뤬����(���ꤷ��ʸ����).(�����ֹ�).html�פˤʤ롣
#
$ARTICLE_PREFIX = "kb";

#
# ��å����������
#
$ENTRY_MSG = "���Τܡ����ؤν񤭹���";
$PREVIEW_MSG = "�񤭹��ߤ����Ƥ��ǧ���Ʋ�����";
$THANKS_MSG = "�񤭹��ߤ��꤬�Ȥ��������ޤ���";
$SORT_MSG = "���ս祽����";
$NEWARTICLE_MSG = "�Ƕ�ε���";
$THREADARTICLE_MSG = "ȿ���ޤȤ��ɤ�";
$ERROR_MSG   = "ERROR!";

$ADDRESS = "Copyright 1995 <a href=\"http://www.kinotrope.co.jp/\">kinotrope Co.,Ltd.</a> &amp; <a href=\"http://www.ohara.info.waseda.ac.jp/person/nakahiro/nakahiro.html\">nakahiro</a> // ��̵��ž��";

$H_BOARD = "�ܡ���:";
$H_SUBJECT = "���ꡡ:";
$H_FROM = "��̾��:";
$H_MAIL = "�᡼��:";
$H_HOST = "�ޥ���:";
$H_DATE = "�����:";
$H_REPLY = "������:";
$H_FOLLOW = "��ȿ��";

$H_TEXTTYPE = "���Ϸ���:";
$H_HTML = "HTMLʸ��";
$H_PRE = "�����Ѥ�ʸ��";

$H_AORI = "���̤˽񤭹���ǲ���������ưŪ���ޤ��֤��ϹԤʤ鷺���񤤤��ޤ�ɽ������ޤ�����������&lt; &gt; &amp; &quot; �ϡ����ΤޤޤǤϻȤ��ޤ�������ˤ��줾�졢 &amp;lt; &amp;gt; &amp;amp; &amp;quot; �Ƚ񤯤ȡ�������ɽ������ޤ���<br>HTML�Τ狼�����ϡ���$H_TEXTTYPE�פ��$H_HTML�פˤ���HTML�Ȥ��ƽ񤤤�ĺ���ȡ�HTML������Ԥʤ��ޤ���";

#
# ���ѥޡ���
#
$DEFAULT_QMARK = " ] ";

#
# �����Ϲ��ܤ��礭��
#
$SUBJECT_LENGTH = 45;
$TEXT_ROWS      = 15;
$TEXT_COLS      = 50;
$NAME_LENGTH    = 45;
$MAIL_LENGTH    = 45;
$URL_LENGTH     = 37;


#/////////////////////////////////////////////////////////////////////


###
## ����¾�����(������������ѹ����ʤ��Ǥ�)
#

#
# ���Υץ�����URL
#
$PROGRAM = $PROGRAM_DIR_URL . "/" . $PROGRAM_NAME;

#
# Permission of Title File.
#
$TITLE_FILE_PERMISSION = "0666";

#
# �ե�����
#
# ��å��ե�����
$LOCK_FILE = ".lock.kb";
# �����ֹ�ե�����
$ARTICLE_NUM_FILE_NAME = ".articleid";
# �����ȥ�ե�����
$TITLE_FILE_NAME = "index.html";
# all�ե�����
$ALL_FILE_NAME = "all.html";
# �����ȥ�tmporary�ե�����
$TTMP_FILE_NAME = "index.tmp";
# �桼�������ꥢ���ե�����
$USER_ALIAS_FILE = "kinousers";
# �ܡ��ɥ����ꥢ���ե�����
$BOARD_ALIAS_FILE = "kinoboards";

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


###
## �ᥤ��
#

MAIN: {

	local($Command, $Id, $File, $Num);

	# ɸ������(POST)�ޤ��ϴĶ��ѿ�(GET)�Υǥ����ɡ�
	&cgi'decode;

	# REQUEST_METHOD��POST�ʤ�Preview���̤ء�GET�ʤ���˱�����ʬ�����롣
	#
	#	����:			c=n
	#
	#	���ѤĤ��ե���:	c=q&id=[1-9][0-9]*
	#	���Ѥʤ��ե���:	c=f&id=[1-9][0-9]*
	#	�ե�������ѥե���:	c=q/f&file=filename
	#
	#	��ǧ�Ѥ�:		c=x&id=[1-9][0-9]*(���ѤǤʤ�����id=0)
	#
	#	���ս祽����:		c=r
	#	�ǿ��ε���n��:		c=l&num=[1-9][0-9]*
	#	thread�ޤȤ��ɤ�:	c=t&id=[1-9][0-9]*
	#

	&Preview, last MAIN if ($ENV{'REQUEST_METHOD'} eq "POST");

	$Command = $cgi'tags{'c'};
	$Id = $cgi'tags{'id'};
	$File = $cgi'tags{'file'};
	$Num = $cgi'tags{'num'};

	&Entry($NO_QUOTE, 0),			last MAIN if ($Command eq "n");
	$Id ? &Entry($QUOTE_ON, $Id) : &FileEntry($QUOTE_ON, $File),
						last MAIN if ($Command eq "q");
	$Id ? &Entry($NO_QUOTE, $Id) : &FileEntry($NO_QUOTE, $File),
						last MAIN if ($Command eq "f");
	&Thanks($File, $Id),			last MAIN if ($Command eq "x");
	&SortArticle,				last MAIN if ($Command eq "r");
	&NewArticle($Num),			last MAIN if ($Command eq "l");
	&ThreadArticle($Id),			last MAIN if ($Command eq "t");

	print("illegal\n");
}

# �����ޤ�
exit 0;


#/////////////////////////////////////////////////////////////////////


#
# ���֥롼����
#


###
## �񤭹��߲���
#
sub Entry {

	# ���Ѥ���/�ʤ��ȡ����Ѥ�����Ϥ���Id(���Ѥ��ʤ�����0)
	local($QuoteFlag, $Id) = @_;

	# ���򤵤줿Board�μ���
	local($Board) = substr($ENV{'PATH_INFO'}, $[ + 1);
	# Board̾�Τμ���
	local($BoardName) = &GetBoardInfo($Board);

	# ɽ�����̤κ���
	&MsgHeader($ENTRY_MSG);

	# �ե����ξ��
	if ($Id != 0) {
		&ViewOriginalArticle($Id, $Board);
		print("<hr>\n");
		print("<h2>��ε�����ȿ������</h2>");
	}

	# ����«
	print("<form action=\"$PROGRAM\" method =\"POST\">\n");
	print("<input name=\"board\" type=\"hidden\" value=\"$Board\">\n");

	# ����Id; ���ѤǤʤ��ʤ�0��
	print("<input name=\"id\" type=\"hidden\" value=\"$Id\">\n");

	# ������ʸ
	print("<p>$H_AORI</p>\n");

	# TextType
	print("$H_TEXTTYPE\n");
	print("<SELECT NAME=\"texttype\">\n");
	print("<OPTION SELECTED>$H_PRE\n");
	print("<OPTION>$H_HTML\n");
	print("</SELECT><BR>\n");

	# Board̾; �����ϼ�ͳ������Ǥ���褦�ˤ�������
	print("$H_BOARD $BoardName<br>\n");

	# Subject(�ե����ʤ鼫ưŪ��ʸ����������)
	if ($Id != 0) {
		printf("$H_SUBJECT <input name=\"subject\" value=\"%s\" size=\"$SUBJECT_LENGTH\"><br>\n", &GetReplySubject($Id, $Board));
	} else {
		print("$H_SUBJECT <input name=\"subject\" value=\"\" size=\"$SUBJECT_LENGTH\"><br>\n");
	}

	# ��ʸ(���Ѥ���ʤ鸵����������)
	print("<textarea name=\"article\" rows=\"$TEXT_ROWS\" cols=\"$TEXT_COLS\">\n");
	&QuoteOriginalArticle($Id, $Board)
		if ($Id != 0 && $QuoteFlag == $QUOTE_ON);
	print("</textarea><br>\n");

	# ̾���ȥ᡼�륢�ɥ쥹��URL��
	print("$H_FROM <input name=\"name\" size=\"$NAME_LENGTH\"><br>\n");
	print("$H_MAIL <input name=\"mail\" size=\"$MAIL_LENGTH\"><br>\n");
	print("URL(���Ǥ�OK):<input name=\"url\" value=\"http://\" size=\"$URL_LENGTH\"><br>\n");

	print("<p>���ϤǤ��ޤ����顢\n");
	print("<input type=\"submit\" value=\"����\">\n");
	print("�򲡤��Ƶ������ǧ���ޤ��礦(�ޤ���Ƥ��ޤ���)��</p>\n");

	# ����«
	print("</form>\n");

	&MsgFooter;
}


###
## �ץ�ӥ塼����
#
sub Preview {

	# Board�μ���
	local($Board) = $cgi'tags{'board'};

	# TextType�μ���
	local($TextType) = $cgi'tags{'texttype'};

	# �ƥ�ݥ��ե�����κ���
	local($TmpFile) = &MakeTemporaryFile($Board, $TextType);

	# ɽ�����̤κ���
	&MsgHeader($PREVIEW_MSG);

	# ����«
	print("<form action=\"$PROGRAM/$Board\" method =\"GET\">\n");
	print("<input name=\"file\" type=\"hidden\" value=\"$TmpFile\">\n");
	print("<input name=\"c\" type=\"hidden\" value=\"x\">\n");
	printf("<input name=\"id\" type=\"hidden\" value=\"%d\">\n",
		$cgi'tags{'id'});

	# ������ʸ
	print("<p>�ʲ��ε������ǧ�����顢");
	print("<input type=\"submit\" value=\"����\">");
	print("�򲡤��ƽ񤭹���ǲ�������</p>\n");

	# ��ǧ���뵭����ɽ��
	open(TMP, "<$TmpFile");
	while(<TMP>) {
		print($_);
	}

	# ����«
	print("</form>\n");

	&MsgFooter;

}


###
## ��Ͽ�����
#
sub Thanks {

	# �ƥ�ݥ��ե�����̾�Ȱ��Ѥ���������Id
	local($TmpFile, $Id) = @_;

	# ���򤵤줿Board�μ���
	local($Board) = substr($ENV{'PATH_INFO'}, $[ + 1);

	# ��Ͽ�ե������URL
	local($TitleFileURL)
		= $PROGRAM_DIR_URL . "/" . $Board . "/" . $TITLE_FILE_NAME;

	# �����˵��������������ե������줿�����ˤ��λݽ񤭹��ࡣ
	&MakeNewArticle($TmpFile, $Board, $Id);

	# ɽ�����̤κ���
	&MsgHeader($THANKS_MSG);

	print("<p>�񤭹��ߤ���������äʤɤϥ᡼��Ǥ��ꤤ�������ޤ���</p>");
	print("<form action=\"$TitleFileURL\">\n");
	print("<input type=\"submit\" value=\"�ꥹ�Ȥ򸫤�\">\n");
	print("</form>\n");

	&MsgFooter;
}


###
## ���ս�˥����ȡ���������Τ��塣
#
sub SortArticle {

	# ���򤵤줿Board�μ���
	local($Board) = substr($ENV{'PATH_INFO'}, $[ + 1);
	# All file
	local($AllFile) = "$Board/$ALL_FILE_NAME";

	local(@lines);

	open(ALL, "$AllFile") || &MyFatal(1, $AllFile);
	while(<ALL>) {
		s/href=\"/href=\"$PROGRAM_DIR_URL\/$Board\//;
		push(@lines, $_);
	}
	close ALL;

	# ɽ�����̤κ���
	&MsgHeader($SORT_MSG);
	print("<ol>\n");
	foreach (reverse sort MyArticleSort @lines) {
		print $_;
	}
	print("</ol>\n");
	&MsgFooter;
}


###
## ��������������n�Ĥ�ɽ����
#
sub MyArticleSort {
	local($MyA, $MyB) = ($a, $b);
	$MyA =~ s/<li><strong>([0-9]*) .*$/$1/;
	$MyB =~ s/<li><strong>([0-9]*) .*$/$1/;
	return($MyA <=> $MyB);
}

###
## ��������������n�Ĥ�ɽ����
#
sub NewArticle {

	# ɽ������Ŀ������
	local($Num) = @_;

	# ���򤵤줿Board�μ���
	local($Board) = substr($ENV{'PATH_INFO'}, $[ + 1);

	# �����ֹ������ե�����
	local($ArticleNumFile) = $Board . "/" . $ARTICLE_NUM_FILE_NAME;

	# �ǿ������ֹ�����
	$ArticleToId = &GetArticleId($ArticleNumFile);

	# ��äƤ���ǽ�ε����ֹ�����
	$ArticleFromId = $ArticleToId - $Num + 1;

	local($i, $File);

	# ɽ�����̤κ���
	&MsgHeader($NEWARTICLE_MSG);

	print("<p>������: $Num ($ArticleToId �� $ArticleFromId)</p>");

	# name�ؤΥ�󥯤�ɽ��
	print("<p> //\n");
	for ($i = $ArticleToId; ($i >= $ArticleFromId); $i--) {
		print("<a href=\"\#$i\">$i</a> //\n");
	}
	print("</p>\n");

	for ($i = $ArticleToId; ($i >= $ArticleFromId); $i--) {
		print("<br><hr><br>\n");
		print("<strong><a name=\"$i\">ID = $i</a></strong><br>\n");
		&ViewOriginalArticle($i, $Board);
	}

	&MsgFooter;
}


###
## �ե�������������ɽ����
#
sub ThreadArticle {

	# ��������Id�����
	local($Id) = @_;

	# ���򤵤줿Board�μ���
	local($Board) = substr($ENV{'PATH_INFO'}, $[ + 1);

	# ɽ�����̤κ���
	&MsgHeader($THREADARTICLE_MSG);

	# �ᥤ��ؿ��θƤӽФ�(subject)
#	&ThreadArticleMain('subject only', $Id, $Board);

	# �ᥤ��ؿ��θƤӽФ�
	&ThreadArticleMain('', $Id, $Board);

	&MsgFooter;
}


###
## �Ƶ�Ū�ˤ��ε����Υե�����ɽ�����롣
#
sub ThreadArticleMain {

	# Id��Board�μ���
	local($SubjectOnly, $Id, $Board) = @_;

	# �ե���������Id�μ���
	local(@FollowIdList) = &GetFollowIdList($Id, $Board);

	# ���ڤ�
	print("<hr>\n");

	if ($SubjectOnly) {
		&MyFatal(999, 'unknown');
	} else {
		# ��������ɽ��
		&ViewOriginalArticle($Id, $Board);
	}

	# �ե���������ɽ��
	foreach (@FollowIdList) {
		# �Ƶ�
		&ThreadArticleMain($SubjectOnly, $_, $Board);
	}
}


###
## ��ǧ�ѥƥ�ݥ��ե������������ƥե�����̾���֤���
#
sub MakeTemporaryFile {

	# Board��TextType�μ���
	local($Board, $TextType) = @_;

	# Board̾�Τμ���
	local($BoardName) = &GetBoardInfo($Board);

	# �ƥ�ݥ��ե�����̾�μ���
	local($TmpFile) = "$Board/.$ARTICLE_PREFIX.$$";

	# ���դ���Ф���
	local($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst)
		= localtime(time);
	local($InputDate)
		= sprintf("%d��%d��%02d��%02dʬ", $mon + 1, $mday, $hour, $min);

	# �ۥ���̾����Ф���
	local($RemoteHost) = $ENV{ 'REMOTE_HOST' };

	# ���ѥե����롢����Subject
	local($ReplyArticleFile, $ReplyArticleSubject);

	# �⤷���Ѥʤ���ѥե�����̾�����
	if ($cgi'tags{'id'} != 0) {
		$ReplyArticleFile = &GetArticleFileName($cgi'tags{'id'}, '');
		$ReplyArticleSubject = &GetSubject($cgi'tags{'id'}, $Board);
	} elsif ($cgi'tags{'file'} ne '') {
		$ReplyArticleFile = "../" . $cgi'tags{'file'};
		$ReplyArticleSubject = &GetSubjectFromFile($cgi'tags{'file'});
	}

	# �����ꥢ�������å�
	$_ = $cgi'tags{'name'};
	if (/^#.*$/) {
		($cgi'tags{'name'}, $cgi'tags{'mail'}, $cgi'tags{'url'})
			= &GetUserInfo($_);
		if ($cgi'tags{'name'} eq "") {
			&MsgHeader($ERROR_MSG);
			print("<H2>$_�ϥ����ꥢ������Ͽ����Ƥ��ޤ���</h2>");
			print("<p>��äƤ⤦���١�</p>");
			&MsgFooter;
			exit 0;
		}
	}

	# �������å�
	&MyFatal(2, '') if ($cgi'tags{'subject'} eq "")
		|| ($cgi'tags{'article'} eq "")
		|| ($cgi'tags{'name'} eq "")
		|| ($cgi'tags{'mail'} eq "");

	# ���֥������ȤΥ��������å�
	$_ = $cgi'tags{'subject'};
	&MyFatal(4, '') if (/</);

	# �ƥ�ݥ��ե�����˽񤭽Ф���
	open(TMP, ">$TmpFile") || &MyFatal(1, $TmpFile);

	# �ޤ��إå���
	printf(TMP "<strong>$H_SUBJECT</strong> %s<br>\n", $cgi'tags{'subject'});

	if ($cgi'tags{'url'} eq "http://" || $cgi'tags{'url'} eq "") {
		# URL���ʤ����
		printf(TMP "<strong>$H_FROM</strong> %s<br>\n", $cgi'tags{'name'});
	} else {
		# URL��������
		printf(TMP "<strong>$H_FROM</strong> <a href=\"%s\">%s</a><br>\n", $cgi'tags{'url'}, $cgi'tags{'name'});
	}

	printf(TMP "<strong>$H_MAIL</strong> <a href=\"mailto:%s\">&lt;%s&gt;</a><br>\n",
		$cgi'tags{'mail'}, $cgi'tags{'mail'});
#	print(TMP "<strong>$H_HOST</strong> $RemoteHost<br>\n");
# kinotrope�Ǥ�gethostbyaddr��Ȥ��ʤ��褦�ʤΤǡ������ǥۥ���̾�Ͼ�ά
	print(TMP "<strong>$H_DATE</strong> $InputDate<br>\n");

	# ���Ѥξ��
	if ($cgi'tags{'id'} != 0) {
		printf(TMP "<strong>$H_REPLY</strong> [$BoardName: %d] <a href=\"$ReplyArticleFile\">$ReplyArticleSubject</a><br>\n", $cgi'tags{'id'});
	} elsif ($cgi'tags{'file'} ne '') {
		printf(TMP "<strong>$H_REPLY</strong> <a href=\"$ReplyArticleFile\">$ReplyArticleSubject</a><br>\n");
	}

	print(TMP "------------------------<br>\n");

	# article begin
	print(TMP "<!-- Article Begin -->\n");

	# TextType��������
	print(TMP "<pre>\n") if ($TextType eq $H_PRE);

	# ����
	printf(TMP "%s\n", $cgi'tags{'article'});

	# TextType�Ѹ����
	print(TMP "</pre>\n") if ($TextType eq $H_PRE);

	# article end
	print(TMP "<!-- Article End -->\n");
	print(TMP "<hr>\n");
	close TMP;

	# �ե�����̾���֤���
	return($TmpFile);
}


###
## ��������Ƥ��줿����������
#
sub MakeNewArticle {

	# �ƥ�ݥ��ե�����̾��Board�����Ѥ���������Id
	local($TmpFile, $Board, $Id) = @_;

	# Board̾�Τμ���
	local($BoardName) = &GetBoardInfo($Board);

	# �����ֹ������ե�����
	local($ArticleNumFile) = $Board . "/" . $ARTICLE_NUM_FILE_NAME;

	# �����ε����ֹ�ȥե�����̾
	local($ArticleId, $ArticleFile);

	# ���֥������ȡ���������̾��
	local($Subject, $InputDate, $Name);

	# �ƥ�ݥ��ե����뤫��Subject������Ф�
	open(TMP, "$TmpFile") || &MyFatal(1, $TmpFile);
	while(<TMP>) {

		# subject����Ф���
		if (/^<strong>$H_SUBJECT<\/strong> (.*)<br>$/) {$Subject = $1; }
		# ���դ���Ф���
		if (/^<strong>$H_DATE<\/strong> (.*)<br>$/) {$InputDate = $1; }
		# ̾������Ф���
		if (/^<strong>$H_FROM<\/strong> <a[^>]*>(.*)<\/a><br>$/) {
			$Name = $1;
		} elsif (/^<strong>$H_FROM<\/strong> (.*)<br>$/) {
			$Name = $1;
		}

	}
	close TMP;

	# ��å��ե�����򳫤�
	open(LOCK, "$LOCK_FILE")
		# �����ʤ�����
		|| (&MakeLockFile($LOCK_FILE) && open(LOCK, "$LOCK_FILE"))
		# ���ʤ��㥨�顼
		|| &MyFatal(1, $LOCK_FILE);

	# ��å��򤫤���
	&lock();

	# �����ֹ�����
	$ArticleId = &GetandAddArticleId($ArticleNumFile);

	# �����Υե�����̾�����
	$ArticleFile = &GetArticleFileName($ArticleId, $Board);

	# �����Υե�����˥إå���ʬ��񤭹���
	open(ART, ">$ArticleFile") || &MyFatal(1, $ArticleFile);

	# �����إå��κ���
	printf(ART "<title>[$BoardName: %d] $Subject</title>\n", $ArticleId);
	print(ART "<body>\n");
	print(ART "<a href=\"$TITLE_FILE_NAME\">���</a> // ");
	printf(ART "<a href=\"%s\">����</a> // ",
		&GetArticleFileName(($ArticleId - 1), ''));
	printf(ART "<a href=\"%s\">����</a> // ",
		&GetArticleFileName(($ArticleId + 1), ''));
	print(ART "ȿ�� ( <a href=\"$PROGRAM/$Board?c=q&id=$ArticleId\">����ͭ��</a> / ");
	print(ART "<a href=\"$PROGRAM/$Board?c=f&id=$ArticleId\">̵��</a> ) // ");
	print(ART "<a href=\"$PROGRAM/$Board?c=t&id=$ArticleId\">�ޤȤ��ɤ�</a>\n");
	print(ART "<hr>\n");

	# �����إå��λϤޤ�
	print(ART "<!-- Header Begin -->\n");

	# �ܥǥ�����Ƭ�˥ܡ���̾�ȵ����ֹ桢��������
	printf(ART "<strong>$H_SUBJECT</strong> [$BoardName: %d] $Subject<br>\n", $ArticleId);

	# �ƥ�ݥ��ե����뤫��ε����Υ��ԡ�
	open(TMP, "$TmpFile") || &MyFatal(1, $TmpFile);

	# Subject�Ԥ������ѤߤʤΤ�1�����Ф���
	$Dust = <TMP>;

	while(<TMP>) {
		print(ART $_)
	}
	close TMP;

	# �ƥ�ݥ��ե�����κ��
	unlink("$TmpFile");

	# �����եå��κ���
	print(ART "$H_FOLLOW\n<ol>\n");
	close ART;

	if ($Id != 0) {
		# �ե����ξ��

		# �ե������줿�����˥ե������줿���Ȥ�񤭹��ࡣ
		# �ե������������ե�����̾��ľ���Ϥ��ʤ��Τϡ�
		# ���Фε������ۤʤ뤿�ᡣ
		&ArticleWasFollowed($Id, $Board, $ArticleId, $Subject, $Name);

		# �����ȥ�ե��������Ƥ��줿�������ɲ�
		&AddTitleFollow($ArticleId, $Board, $Id, $Name, $Subject, $InputDate);
	} else {
		# �ե����Ǥʤ��������ξ��

		# �����ȥ�ե��������Ƥ��줿�������ɲ�
		&AddTitleNormal($ArticleId, $Board, $Name, $Subject, $InputDate);
	}

	# all�ե��������Ƥ��줿�������ɲ�
	&AddAllFile($ArticleId, $Board, $Name, $Subject, $InputDate);

	# ��å��򳰤���
	&unlock();
	close LOCK;

}


###
## all�ꥹ�Ȥ˽񤭹���
#
sub AddAllFile {

	# ����Id��Board, ̾�����ꡢ����
	local($Id, $Board, $Name, $Subject, $InputDate) = @_;

	# ��Ͽ�ե�����
	local($File) = $Board . "/" . $ALL_FILE_NAME;

	# �ɲä���ե������̾��
	local($ArticleFile) = &GetArticleFileName($Id, '');

	# Add to 'All' file
	open(ALL, ">>$File") || &MyFatal(1, $File);
	printf(ALL "<li><strong>$Id .</strong> <a href=\"%s\">$Subject</a> [$Name] $InputDate\n\n", $ArticleFile);
	close TITLE;
}
###
## �����ȥ�ꥹ�Ȥ˽񤭹���(����)
#
sub AddTitleNormal {

	# ����Id��Board, ̾�����ꡢ����
	local($Id, $Board, $Name, $Subject, $InputDate) = @_;

	# ��Ͽ�ե�����
	local($File) = $Board . "/" . $TITLE_FILE_NAME;

	# �ɲä���ե������̾��
	local($ArticleFile) = &GetArticleFileName($Id, '');

	# �����ȥ�ե�������ɲ�
	open(TITLE, ">>$File") || &MyFatal(1, $File);
	printf(TITLE "<li><strong>$Id .</strong> <a href=\"%s\">$Subject</a> [$Name] $InputDate\n\n", $ArticleFile);
	close TITLE;
}


###
## �����ȥ�ꥹ�Ȥ˽񤭹���(�ե���)
#
sub AddTitleFollow {

	# ����Id��Board, �ե�������Id��̾�����ꡢ����
	local($Id, $Board, $Fid, $Name, $Subject, $InputDate) = @_;

	# ��Ͽ�ե�����
	local($File) = $Board . "/" . $TITLE_FILE_NAME;

	# �ɲä���ե������̾��
	local($ArticleFile) = &GetArticleFileName($Id, '');

	# Followed Article File Name
	local($FollowedArticleFile) = &GetArticleFileName($Fid, '');

	# TmpFile
	local($TmpFile) = "$Board/$TTMP_FILE_NAME";

	# Follow Flag
	local($AddFlag, $Nest, $NextLine) = (0, 0, ''); 

	# �����ȥ�ե�������ɲ�
	open(TTMP, ">$TmpFile") || &MyFatal(1, $TmpFile);
	open(TITLE, "$File") || &MyFatal(1, $File);

	while(<TITLE>) {
		print(TTMP $_);

		if (/$FollowedArticleFile/) {
			&MyFatal(3, '') unless ($_ = <TITLE>);

			if (/^<ul>/) {
				$Nest = 1;
				do {
					print(TTMP $_);
					$_ = <TITLE>;
					$Nest++ if (/^<ul>/);
					$Nest-- if (/^<\/ul>/);
				} until ($Nest == 0);

				printf(TTMP "<li><strong>$Id .</strong> <a href=\"%s\">$Subject</a> [$Name] $InputDate\n\n", $ArticleFile);
				printf(TTMP $_);

			} else {

				print(TTMP "<ul>\n");
				printf(TTMP "<li><strong>$Id .</strong> <a href=\"%s\">$Subject</a> [$Name] $InputDate\n\n", $ArticleFile);
				print(TTMP "</ul>\n");

			}

			$AddFlag = "True";
		}
	}

	# If not found, followed Article must be old one.
	printf(TTMP "<li><strong>$Id .</strong> <a href=\"%s\">$Subject</a> [$Name] $InputDate\n\n", $ArticleFile) if (! $AddFlag);

	close TITLE;
	close TTMP;

	# Copy to Title File
	open(TITLE, ">$File") || &MyFatal(1, $File);
	open(TTMP, "$TmpFile") || &MyFatal(1, $TmpFile);
	while(<TTMP>) {
		print(TITLE $_);
	}
	close TTMP;
	close TITLE;

	# Chmod
	chmod($TITLE_FILE_PERMISSION, $File);

	# Delete Temporary File
	unlink("$TmpFile");
}


###
## �ե������줿�����Υեå��˥ե������줿���Ȥ�񤭹��ࡣ
#
sub ArticleWasFollowed {

	# �ե������줿������Id���ܡ��ɤ�̾�Ρ�
	# �ե�������������Id�����֥������ȡ�̾��
	local($Id, $Board, $FollowArticleId, $Fsubject, $Fname) = @_;

	# �ե������줿�����ե�����
	local($ArticleFile) = &GetArticleFileName($Id, $Board);

	# �ե������������ե�����
	local($FollowArticleFile) = &GetArticleFileName($FollowArticleId, '');

	# �ɲ�
	open(FART, ">>$ArticleFile") || &MyFatal(1, $ArticleFile);
	print(FART "<li><a href=\"$FollowArticleFile\">$Fsubject</a> �� $Fname ����\n");
	close FART;
}


###
## �ե���������Id���������Ф���
#
sub GetFollowIdList {

	# Id��Board
	local($Id, $Board) = @_;

	# ���ե�����
	local($File) = &GetArticleFileName($Id, $Board);

	# �ե�����ʬ��Ƚ�Ǥ���ե饰
	local($FollowFlag) = 0;

	# �ꥹ��
	local(@Result) = ();

	open(TMP, "$File") || &MyFatal(1, $File);
	while(<TMP>) {

		# �ե�����ʬ���Ϥ�Ƚ��
		$QuoteFlag = 1 if (/^<!-- Article End -->$/);

		# �ե���Id�μ���
		if (($QuoteFlag == 1) &&
		(/^<li><a href=\"$ARTICLE_PREFIX\.([^\.]*)\.html\">/)) {
			push(@Result, $1);
		}
	}
	close TMP;

	return(@Result);
}


###
## ��������ɽ��
#
sub ViewOriginalArticle {

	# Id��Board
	local($Id, $Board) = @_;

	# ���Ѥ���ե�����
	local($QuoteFile) = &GetArticleFileName($Id, $Board);

	# ������ʬ��Ƚ�Ǥ���ե饰
	local($QuoteFlag) = 0;

	open(TMP, "$QuoteFile") || &MyFatal(1, $QuoteFile);
	while(<TMP>) {

		# ���ѽ�λ��Ƚ��
		$QuoteFlag = 0 if (/^<!-- Article End -->$/);

		# ����ʸ�����ɽ��
		if ($QuoteFlag == 1) {
			print($_);
		}

		# ���ѳ��Ϥ�Ƚ��
		$QuoteFlag = 1 if ((/^<!-- Header Begin -->$/) ||
					(/^<!-- Article Begin -->$/));

	}
	close TMP;

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

	open(TMP, "$QuoteFile") || &MyFatal(1, $QuoteFile);
	while(<TMP>) {

		# ���ѽ�λ��Ƚ��
		$QuoteFlag = 0 if (/^<!-- Article End -->$/);

		# ����ʸ�����ɽ��
		if ($QuoteFlag == 1) {
			s/&/&amp;/go;
			s/\"//go;
			s/<//go;
			s/>//go;
			print($DEFAULT_QMARK, $_);
		}

		# ���ѳ��Ϥ�Ƚ��
		$QuoteFlag = 1 if (/^<!-- Article Begin -->$/);

	}
	close TMP;

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
	close AID;

	# 1���䤷�ƽ񤭹��ࡣ
	open(AID, ">$ArticleNumFile") || &MyFatal(1, $ArticleNumFile);
	print(AID $ArticleId + 1, "\n");
	close AID;

	# �����������ֹ���֤���
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

	open(AID, "$ArticleNumFile") || &MyFatal(1, $ArticleNumFile);
	while(<AID>) {
		chop;
		$ArticleId = $_;
	}
	close AID;

	# �����ֹ���֤���
	return($ArticleId);
}


###
## �桼�������ꥢ������桼����̾�����᡼�롢URL���äƤ��롣
#
sub GetUserInfo {

	# �����ꥢ��̾
	local($Alias) = @_;

	# ̾�����᡼�롢URL
	local($Name, $Mail, $URL);

	open(ALIAS, "$USER_ALIAS_FILE") || &MyFatal(1, $USER_ALIAS_FILE);
	while(<ALIAS>) {

		# �ޥå����ʤ��㼡�ء�
		next unless (/^$Alias$/);

		$Name = <ALIAS>;
		chop($Name);
		$Mail = <ALIAS>;
		chop($Mail);
		$URL = <ALIAS>;
		chop($URL);

		# ����ˤ����֤�
		return($Name, $Mail, $URL);
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

	open(ALIAS, "$BOARD_ALIAS_FILE") || &MyFatal(1, $BOARD_ALIAS_FILE);
	while(<ALIAS>) {

		chop;
		# �ޥå����ʤ��㼡�ء�
		next unless (/^$Alias\t(.*)$/);
		$BoardName = $1;
		return($BoardName);
	}

	# �ҥåȤ���
	return('');
}


###
## ����Id�ε�������Subject���äƤ��ơ���Ƭ�ˡ�Re: �פ�1�Ĥ����Ĥ����֤���
#
sub GetReplySubject {

	# Id��Board
	local($Id, $Board) = @_;

	# ���Ф���Subject
	local($Subject) = '';

	# Subject�����������Ƭ�ˡ�Re: �פ����äĤ��Ƥ����������
	$_ = &GetSubject($Id, $Board);

	$Subject = (/^Re: (.*)/) ? $1 : $_;

	# ��Ƭ�ˡ�Re: �פ򤯤äĤ����֤���
	return("Re: $Subject");

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
	local($Subject) = '';

	# �����ե����뤫��Subjectʸ�������Ф���
	open(TMP, "$ArticleFile") || &MyFatal(1, $ArticleFile);
	while(<TMP>) {
		if (/^<strong>$H_SUBJECT<\/strong> \[[^\]]*\] (.*)<br>$/) {
			$Subject = $1;
		}
	}
	close TMP;

	# �֤�
	return($Subject);
}


###
## �ܡ���̾�Τ�Id����ե�����̾����Ф���
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
## ���ե�����Υ�å��ط�
#
sub MakeLockFile {
	# �ե�����̾
	local($File) = @_;

	open(MAKELOCK, ">$File") || return(0);
	close MAKELOCK;
	return(1);
}

sub lock {
	# ��å�
	flock(LOCK, $LOCK_EX);
	# ���ʤ��ʤ�
	seek(AID, 0, 2);
	seek(ART, 0, 2);
	seek(TITLE, 0, 2);
	seek(FART, 0, 2);
	seek(ALL, 0, 2);
}

sub unlock {
	# �����å�
	flock(LOCK, $LOCK_UN);
}


###
## �����Υإå���ɽ��
#
sub MsgHeader {
	local($Message) = @_;

	&cgi'header;
	print("<title>$Message</title>", "\n");
	print("<body>\n");
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
	#

	&MsgHeader($ERROR_MSG);

	if ($MyFatalNo == 1) {
		print("<p>File: $MyFatalInfo��¸�ߤ��ʤ���\n");
		print("���뤤��permission�����꤬�ְ�äƤ��ޤ���\n");
		print("������Ǥ�����<a href=\"$Maint\"</a>$Maint</a>�ޤ�\n");
		print("�嵭�ե�����̾���Τ餻��������</p>\n");
	} elsif ($MyFatalNo == 2) {
		print("<p>�ꡢ��������̾�����᡼�륢�ɥ쥹��\n");
		print("�����줫�����Ϥ���Ƥ��ޤ���\n");
		print("��äƤ⤦���١�</p>\n");
	} elsif ($MyFatalNo == 3) {
		print("<p>Title File is illegal.\n");
		print("������Ǥ�����<a href=\"$Maint\"</a>$Maint</a>�ޤ�\n");
		print("���Τ餻��������</p>\n");
	} elsif ($MyFatalNo == 4) {
		print("<p>�����ʤ����������HTML����������뤳�Ȥ�\n");
		print("�ؤ����Ƥ��ޤ�����äƤ⤦���١�</a>\n");
	} else {
		print("<p>���顼�ֹ�����: ������Ǥ�����");
		print("���Υ��顼��������������");
		print("<a href=\"$Maint\"</a>$Maint</a>�ޤǤ��Τ餻��������</p>\n");
	}

	&MsgFooter;
	exit 0;
}


#/////////////////////////////////////////////////////////////////////
# �ʤ��Ҥ��ѥ��ץ����


###
## �񤭹��߲���(option: �ե����뤫�����)
#
sub FileEntry {

	# ���Ѥ���/�ʤ��ȡ����Ѥ���ե�����(kb.cgi��������)
	local($QuoteFlag, $File) = @_;

	# ���򤵤줿Board�μ���
	local($Board) = substr($ENV{'PATH_INFO'}, $[ + 1);
	# Board̾�Τμ���
	local($BoardName) = &GetBoardInfo($Board);

	# ɽ�����̤κ���
	&MsgHeader($ENTRY_MSG);

	# ���ѥե������ɽ��
	&ViewOriginalFile($File);
	print("<hr>\n");
	print("<h2>��ε�����ȿ������</h2>");

	# ����«
	print("<form action=\"$PROGRAM\" method =\"POST\">\n");
	print("<input name=\"board\" type=\"hidden\" value=\"$Board\">\n");

	# ����Id; �����ΰ��ѤǤʤ��Τ�0��
	print("<input name=\"id\" type=\"hidden\" value=\"0\">\n");

	# ���ѥե�����
	print("<input name=\"file\" type=\"hidden\" value=\"$File\">\n");

	# ������ʸ
	print("<p>$H_AORI</p>\n");

	# TextType
	print("$H_TEXTTYPE\n");
	print("<SELECT NAME=\"texttype\">\n");
	print("<OPTION SELECTED>$H_PRE\n");
	print("<OPTION>$H_HTML\n");
	print("</SELECT><BR>\n");

	# Board̾; �����ϼ�ͳ������Ǥ���褦�ˤ�������
	print("$H_BOARD $BoardName<br>\n");

	# Subject
	printf("$H_SUBJECT <input name=\"subject\" value=\"%s\" size=\"$SUBJECT_LENGTH\"><br>\n", &GetReplySubjectFromFile($File));

	# ��ʸ(���Ѥ���ʤ鸵����������)
	print("<textarea name=\"article\" rows=\"$TEXT_ROWS\" cols=\"$TEXT_COLS\">\n");
	&QuoteOriginalFile($File) if ($QuoteFlag == $QUOTE_ON);
	print("</textarea><br>\n");

	# ̾���ȥ᡼�륢�ɥ쥹��URL��
	print("$H_FROM <input name=\"name\" size=\"$NAME_LENGTH\"><br>\n");
	print("$H_MAIL <input name=\"mail\" size=\"$MAIL_LENGTH\"><br>\n");
	print("URL(���Ǥ�OK):<input name=\"url\" value=\"http://\" size=\"$URL_LENGTH\"><br>\n");

	print("<p>���ϤǤ��ޤ����顢\n");
	print("<input type=\"submit\" value=\"����\">\n");
	print("�򲡤��Ƶ������ǧ���ޤ��礦(�ޤ���Ƥ��ޤ���)��</p>\n");

	# ����«
	print("</form>\n");

	&MsgFooter;
}


###
## ��������ɽ��(�ե�����)
#
sub ViewOriginalFile {

	# �ե�����̾
	local($File) = @_;

	# ������ʬ��Ƚ�Ǥ���ե饰
	local($QuoteFlag) = 0;

	open(TMP, "cat $File | /usr/local/bin/nkf -e |") || &MyFatal(1, $File);
	while(<TMP>) {

		# ���ѽ�λ��Ƚ��
		$QuoteFlag = 0 if (/^<!-- Article End -->$/);

		# ����ʸ�����ɽ��
		if ($QuoteFlag == 1) {
			print($_);
		}

		# ���ѳ��Ϥ�Ƚ��
		$QuoteFlag = 1 if (/^<!-- Article Begin -->$/);

	}
	close TMP;

}


###
## ���Ѥ���(�ե�����)
#
sub QuoteOriginalFile {

	# �ե�����̾
	local($File) = @_;

	# ������ʬ��Ƚ�Ǥ���ե饰
	local($QuoteFlag) = 0;

	open(TMP, "cat $File | /usr/local/bin/nkf -e |") || &MyFatal(1, $File);
	while(<TMP>) {

		# ���ѽ�λ��Ƚ��
		$QuoteFlag = 0 if (/^<!-- Article End -->$/);

		# ����ʸ�����ɽ��
		if ($QuoteFlag == 1) {
			s/&/&amp;/go;
			s/\"//go;
			s/<//go;
			s/>//go;
			print($DEFAULT_QMARK, $_);
		}

		# ���ѳ��Ϥ�Ƚ��
		$QuoteFlag = 1 if (/^<!-- Article Begin -->$/);

	}
	close TMP;

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
## ����ե����뤫��Title���äƤ���
#
sub GetSubjectFromFile {

	# �ե�����
	local($File) = @_;

	# ���Ф���Subject
	local($Title) = '';

	open(TMP, "$File") || &MyFatal(1, $File);
	while(<TMP>) {

		if (/^<[Tt][Ii][Tt][Ll][Ee]>(.*)<\/[Tt][Ii][Tt][Ll][Ee]>$/) {
			$Title = $1;
		}
	}
	close TMP;

	# �֤���
	return($Title);

}


#/////////////////////////////////////////////////////////////////////

#
# cgi�ѥѥå�����
#
package cgi;


###
## HTML�إå�������
#
sub header {print "Content-type: text/html\n\n";}


###
## �ǥ�����
#
sub decode {
        local($args, $n_read, *terms, $tag, $value);

        $ENV{'REQUEST_METHOD'} eq "POST" ?
        ($n_read = read(STDIN, $args, $ENV{'CONTENT_LENGTH'})):
        ($args = $ENV{'QUERY_STRING'});

        @terms = split('&', $args);

        foreach (@terms) {
                ($tag, $value) = split(/=/, $_, 2);
                $value =~ tr/+/ /;
                $value =~ s/%([0-9A-Fa-f][0-9A-Fa-f])/pack("C", hex($1))/ge;
		$tags{$tag} = `echo -n '$value' | /usr/local/bin/nkf -e`;
		$tags{$tag} =~ s///ge;
        }
}

#/////////////////////////////////////////////////////////////////////
