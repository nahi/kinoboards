#!/usr/local/bin/perl
#
# $Id: kb.cgi,v 1.10 1995-12-15 14:21:37 nakahiro Exp $
#
# $Log: kb.cgi,v $
# Revision 1.10  1995-12-15 14:21:37  nakahiro
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
#	��	��ʬ���ե�����
#	��	�������'���������褦�ˤ���
#	��	����������ǽ
#	��	�ޤȤ��ɤߤλ���thread��狼��䤹�����빩�פ�
#		�־�ءסֲ��ءפΥ�󥯵�ǽ���ɲ�(��/�����ѻ�?)
#		��Ȥ�EUC���ե������JIS��
#		alias����Ͽ��ǽ
#		Subject����Ƭ��Icon��Ĥ�����
#		Board��ͳ�����򤹤�
#		����������n�Ĥ˥ޡ�����Ĥ���(aging��ǽ�Ȥη�͹礤�ǤĤ餤)
#		�����Υ���󥻥뵡ǽ(aging��ǽ�Ȥη�͹礤�ǤĤ餤)


#/////////////////////////////////////////////////////////////////////


###
## �إå��ե�������ɤ߹���
#
require('kb.ph');


###
## �ᥤ��
#

MAIN: {

	local($Command, $Id, $File, $Num, $Type, $Key);

	# ɸ������(POST)�ޤ��ϴĶ��ѿ�(GET)�Υǥ����ɡ�
	&cgi'decode;
	$Command = $cgi'tags{'c'};
	$Id = $cgi'tags{'id'};
	$File = $cgi'tags{'file'};
	$Num = $cgi'tags{'num'};
	$Type = $cgi'tags{'type'};
	$Key = $cgi'tags{'key'};

	#	����:			c=n
	#	���ѤĤ��ե���:	c=q&id={[1-9][0-9]*}
	#	���Ѥʤ��ե���:	c=f&id={[1-9][0-9]*}
	#	�ե�������ѥե���:	c=q/f&file={filename}
	#	�����Υץ�ӥ塼:	c=p&(��)....
	#	��ǧ�Ѥ߲���:		c=x&id={[1-9][0-9]*(���ѤǤʤ���id=0)}
	#	���ս祽����:		c=r&type=all|new
	#	�ǿ��ε���n��:		c=l&num={[1-9][0-9]*}
	#	thread�ޤȤ��ɤ�:	c=t&id={[1-9][0-9]*}
	#	����:			c=s&type=all|new&key={keyword}

	&Entry($NO_QUOTE, 0),			last MAIN if ($Command eq "n");
	$Id ? &Entry($QUOTE_ON, $Id) : &FileEntry($QUOTE_ON, $File),
						last MAIN if ($Command eq "q");
	$Id ? &Entry($NO_QUOTE, $Id) : &FileEntry($NO_QUOTE, $File),
						last MAIN if ($Command eq "f");
	&Thanks($File, $Id),			last MAIN if ($Command eq "x");
	&Preview,				last MAIN if ($Command eq "p");
	&SortArticle($Type),			last MAIN if ($Command eq "r");
	&NewArticle($Num),			last MAIN if ($Command eq "l");
	&ThreadArticle($Id),			last MAIN if ($Command eq "t");
	&SearchArticle($Type, $Key),		last MAIN if ($Command eq "s");

	print("something illegal\n");
}


###
## �����ޤ�
#
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
	print("<input name=\"c\" type=\"hidden\" value=\"p\">\n");
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

	print("<p><a href=\"$USER_ALIAS_FILE_URL\">����</a>����Ͽ����Ƥ������ϡ���$H_FROM�פˡ�#...�פȽ񤯤ȡ���ưŪ���䴰����ޤ�����Ͽ��<a href=\"mailto:$Maint\">$Maint</a>�ޤǡ��᡼��ˤƸ�Ϣ��������</p>\n");
	print("<p>���ϤǤ��ޤ����顢\n");
	print("<input type=\"submit\" value=\"����\">\n");
	print("�򲡤��Ƶ������ǧ���ޤ��礦(�ޤ���Ƥ��ޤ���)��</p>\n");

	# ����«
	print("</form>\n");

	&MsgFooter;
}


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
	print("<input name=\"c\" type=\"hidden\" value=\"p\">\n");
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

	print("<p><a href=\"$USER_ALIAS_FILE_URL\">����</a>����Ͽ����Ƥ������ϡ���$H_FROM�פˡ�#...�פȽ񤯤ȡ���ưŪ���䴰����ޤ�����Ͽ��<a href=\"mailto:$Maint\">$Maint</a>�ޤǡ��᡼��ˤƸ�Ϣ��������</p>\n");
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

	# ������(all / new)
	local($Type) = @_;

	# ���򤵤줿Board�μ���
	local($Board) = substr($ENV{'PATH_INFO'}, $[ + 1);
	# file
	local($File) = ($Type eq 'new')
			? "$Board/$TITLE_FILE_NAME"
			: "$Board/$ALL_FILE_NAME";

	local(@lines);

	open(ALL, "$File") || &MyFatal(1, $File);
	while(<ALL>) {
		(/^<li>/) && (s/href=\"/href=\"$PROGRAM_DIR_URL\/$Board\//)
			&& push(@lines, $_);
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

	# �ᥤ��ؿ��θƤӽФ�(��������)
	print("<ul>\n");
	&ThreadArticleMain('subject only', $Id, $Board);
	print("</ul>\n");

	# �ᥤ��ؿ��θƤӽФ�(����)
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

	# �������פ����������Τ�Τ���
	if ($SubjectOnly) {

		# �������פ�ɽ��
		&PrintAbstract($Id, $Board);

	} else {

		# ���ڤ�
		print("<hr>\n");

		# ��������ɽ��
		print("<strong><a name=\"$Id\">ID = $Id</a></strong><br>\n");
		&ViewOriginalArticle($Id, $Board);

	}

	# �ե���������ɽ��
	foreach (@FollowIdList) {

		# �������פʤ�վ��
		print("<ul>\n") if ($SubjectOnly);

		# �Ƶ�
		&ThreadArticleMain($SubjectOnly, $_, $Board);

		# �������פʤ�վ���Ĥ�
		print("</ul>\n") if ($SubjectOnly);

	}
}


###
## �����γ��פ�ɽ��
#
sub PrintAbstract {

	# Id��Board
	local($Id, $Board) = @_;

	# ���Ѥ���ե�����
	local($File) = &GetArticleFileName($Id, $Board);

	# �ꡢ���ա�̾��
	local($Subject, $InputDate, $Name);

	# �����ե����뤫��Subject������Ф�
	open(TMP, "$File") || &MyFatal(1, $File);
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

	print("<li><strong>$Id .</strong> <a href=\"\#$Id\">$Subject</a> [$Name] $InputDate\n");

}


###
## �����θ���(ɽ�����̺���)
#
sub SearchArticle {

	# all/new���������
	local($Type, $Key) = @_;

	# ���򤵤줿Board�μ���
	local($Board) = substr($ENV{'PATH_INFO'}, $[ + 1);

	# ɽ�����̤κ���
	&MsgHeader($SEARCHARTICLE_MSG);

	# ����«
	print("<form action=\"$PROGRAM/$Board\" method =\"GET\">\n");
	print("<input name=\"c\" type=\"hidden\" value=\"s\">\n");
	print("<input name=\"type\" type=\"hidden\" value=\"$Type\">\n");

	# �������������
	print("<p>������ɤ����Ϥ����顢");
	print("<input type=\"submit\" value=\"����\">");
	print("�򲡤��Ʋ�������</p>\n");
	print("<p>�������륭�����:\n");
	print("<input name=\"key\" size=\"$KEYWORD_LENGTH\"></p>\n");
	print("<hr>\n");

	# ������ɤ����Ǥʤ���С����Υ�����ɤ�ޤ൭���Υꥹ�Ȥ�ɽ��
	&SearchArticleList($Board, $Type, $Key) unless ($Key eq "");

	&MsgFooter;
}


###
## �����θ���(������̤�ɽ��)
#
sub SearchArticleList {

	# �ܡ���̾��all/new���������
	local($Board, $Type, $Key) = @_;

	# �����оݥե�����
	local($File) = ($Type eq 'new')
			? "$Board/$TITLE_FILE_NAME"
			: "$Board/$ALL_FILE_NAME";
	local($Title, $ArticleFile, $HitFlag, $Line);
	$HitFlag = 0;

	# �ꥹ�ȳ���
	print("<dl>\n");

	# �ե�����򳫤�
	open(TITLE, "$File") || &MyFatal(1, $File);
	while(<TITLE>) {
		$Title = $_;
		next unless (/^<li>.*href=\"([^\"]*)\"/);
		$ArticleFile = "$Board/$1";
		$Line = &SearchArticleKeyword($ArticleFile, $Key);
		if ($Line ne "") {
			$Title =~ s/^<li>//go;
			$Title =~ s/href=\"/href=\"$PROGRAM_DIR_URL\/$Board\//;
			$Line =~ s/<[^>]*>//go;
			$Line =~ s/&/&amp;/go;
			$Line =~ s/\"/&quot;/go;
			print("<dt>$Title\n");
			print("<dd>$Line\n");
			$HitFlag = 1;
		}
	}
	close(TITLE);

	# �ҥåȤ��ʤ��ä���
	print("<dt>�������뵭���ϸ��Ĥ���ޤ���Ǥ�����\n")
		unless ($HitFlag = 1);

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
	open(ARTICLE, "$File") || &MyFatal(1, $File);
	while(<ARTICLE>) {
		# �ҥå�?
		(/$Key/) && return($_);
	}

	# �ҥåȤ���
	return("");
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
## ����ե����뤫��Title���äƤ���
#
sub GetSubjectFromFile {

	# �ե�����
	local($File) = @_;

	# ���Ф���Subject
	local($Title) = '';

	open(TMP, "cat $File | /usr/local/bin/nkf -e |") || &MyFatal(1, $File);
	while(<TMP>) {

		if (/^<[Tt][Ii][Tt][Ll][Ee]>(.*)<\/[Tt][Ii][Tt][Ll][Ee]>$/) {
			$Title = $1;
		}
	}
	close TMP;

	# �֤���
	return($Title);

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
		print("������Ǥ�����<a href=\"mailto:$Maint\"</a>$Maint</a>�ޤ�\n");
		print("�嵭�ե�����̾���Τ餻��������</p>\n");
	} elsif ($MyFatalNo == 2) {
		print("<p>�ꡢ��������̾�����᡼�륢�ɥ쥹��\n");
		print("�����줫�����Ϥ���Ƥ��ޤ���\n");
		print("��äƤ⤦���١�</p>\n");
	} elsif ($MyFatalNo == 3) {
		print("<p>Title File is illegal.\n");
		print("������Ǥ�����<a href=\"mailto:$Maint\"</a>$Maint</a>�ޤ�\n");
		print("���Τ餻��������</p>\n");
	} elsif ($MyFatalNo == 4) {
		print("<p>�����ʤ����������HTML����������뤳�Ȥ�\n");
		print("�ؤ����Ƥ��ޤ�����äƤ⤦���١�</a>\n");
	} else {
		print("<p>���顼�ֹ�����: ������Ǥ�����");
		print("���Υ��顼��������������");
		print("<a href=\"mailto:$Maint\"</a>$Maint</a>�ޤǤ��Τ餻��������</p>\n");
	}

	&MsgFooter;
	exit 0;
}


#/////////////////////////////////////////////////////////////////////


###
## cgi�ѥѥå�����
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
		$value =~ s/'/'\\''/go;
		$tags{$tag} = `echo -n '$value' | /usr/local/bin/nkf -e`;
		$tags{$tag} =~ s///ge;
        }
}


#/////////////////////////////////////////////////////////////////////
