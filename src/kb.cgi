#!/usr/local/bin/perl
#
# $Id: kb.cgi,v 2.1 1995-12-19 18:46:12 nakahiro Exp $
#
# $Log: kb.cgi,v $
# Revision 2.1  1995-12-19 18:46:12  nakahiro
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
#	��	�����ʥ����Τ���Ƥ����(�����ߤ����tag_secure.pl��include)
#	��	alias����Ͽ��ǽ
#	��	�ե������Ĥ����ݤ����ε�ǽ
#		�᡼���From��$MAINT�������ɤ�
#		Preview���̤����Х�󥯤������
#		�־�ءסֲ��ءפΥ�󥯵�ǽ���ɲ�(��/�����ѻ�?)
#		��Ȥ�EUC���ե������JIS��
#		Subject����Ƭ��Icon��Ĥ�����
#		Board��ͳ�����򤹤�
#		¾�ͤǤ����Τ��餤����
#		����������n�Ĥ˥ޡ�����Ĥ���(aging��ǽ�Ȥη�͹礤�ǤĤ餤)
#		�����Υ���󥻥뵡ǽ(aging��ǽ�Ȥη�͹礤�ǤĤ餤)


#/////////////////////////////////////////////////////////////////////


###
## �إå��ե�������ɤ߹���
#
require('kb.ph');
require('cgi.pl');
require('tag_secure.pl');


###
## �ᥤ��
#

# ���ޥ��ɽ:
#	�������:		c=n
#	���ѤĤ��ե���:	c=q&id={[1-9][0-9]*}
#	���Ѥʤ��ե���:	c=f&id={[1-9][0-9]*}
#	�ե�������ѥե���:	c=q/f&file={filename}
#	�����Υץ�ӥ塼:	c=p&(��)....
#	��ǧ�Ѥ߲���:		c=x&id={[1-9][0-9]*(���ѤǤʤ���id=0)}
#	���ս祽����:		c=r&type=all|new
#	�ǿ��ε���n��:		c=l&num={[1-9][0-9]*}
#	thread�ޤȤ��ɤ�:	c=t&id={[1-9][0-9]*}
#	����:			c=s&type=all|new&key={keyword}
#	�����ꥢ����Ͽ����:	c=an
#	�����ꥢ����Ͽ:		c=am&alias=..&name=..&email=..&url=..
#	�����ꥢ�����:		c=ad&alias=...
#	�����ꥢ������:		c=as

MAIN: {

	# ɸ������(POST)�ޤ��ϴĶ��ѿ�(GET)�Υǥ����ɡ�
	&cgi'decode;

	# �ͤ����
	local($Command) = $cgi'TAGS{'c'};
	local($Id) = $cgi'TAGS{'id'};
	local($File) = $cgi'TAGS{'file'};
	local($Num) = $cgi'TAGS{'num'};
	local($Type) = $cgi'TAGS{'type'};
	local($Key) = $cgi'TAGS{'key'};
	local($Alias) = $cgi'TAGS{'alias'};
	local($Name) = $cgi'TAGS{'name'};
	local($Email) = $cgi'TAGS{'email'};
	local($URL) = $cgi'TAGS{'url'};

	# ���ޥ�ɥ����פˤ��ʬ��
	&Entry($NO_QUOTE, 0),		last MAIN if ($Command eq "n");
	$Id ? &Entry($QUOTE_ON, $Id) : &FileEntry($QUOTE_ON, $File),
					last MAIN if ($Command eq "q");
	$Id ? &Entry($NO_QUOTE, $Id) : &FileEntry($NO_QUOTE, $File),
					last MAIN if ($Command eq "f");
	&Thanks($File, $Id),		last MAIN if ($Command eq "x");
	&Preview,			last MAIN if ($Command eq "p");
	&SortArticle($Type),		last MAIN if ($Command eq "r");
	&NewArticle($Num),		last MAIN if ($Command eq "l");
	&ThreadArticle($Id),		last MAIN if ($Command eq "t");
	&SearchArticle($Type, $Key),	last MAIN if ($Command eq "s");
	&AliasNew,			last MAIN if ($Command eq "an");
	&AliasMod($Alias, $Name, $Email, $URL),
					last MAIN if ($Command eq "am");
	&AliasDel($Alias),		last MAIN if ($Command eq "ad");
	&AliasShow,			last MAIN if ($Command eq "as");

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

	# ������ʸ��TextType��Board̾
	&EntryHeader($BoardName);

	# Subject(�ե����ʤ鼫ưŪ��ʸ����������)
	printf("%s <input name=\"subject\" type=\"text\" value=\"%s\" size=\"%s\"><br>\n",
		$H_SUBJECT,
		(($Id !=0 ) ? &GetReplySubject($Id, $Board) : ""),
		$SUBJECT_LENGTH);

	# ��ʸ(���Ѥ���ʤ鸵����������)
	print("<textarea name=\"article\" rows=\"$TEXT_ROWS\" cols=\"$TEXT_COLS\">\n");
	&QuoteOriginalArticle($Id, $Board)
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
## �񤭹��߲���(�ե����뤫�����)
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

	# ������ʸ��TextType��Board̾
	&EntryHeader($BoardName);

	# Subject
	printf("%s <input name=\"subject\" type=\"text\" value=\"%s\" size=\"%s\"><br>\n",
		$H_SUBJECT, &GetReplySubjectFromFile($File), $SUBJECT_LENGTH);

	# ��ʸ(���Ѥ���ʤ鸵����������)
	print("<textarea name=\"article\" rows=\"$TEXT_ROWS\" cols=\"$TEXT_COLS\">\n");
	&QuoteOriginalFile($File) if ($QuoteFlag == $QUOTE_ON);
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

	# �ܡ���̾
	local($Board) = @_;

	# ������ʸ
	print("<p>$H_AORI</p>\n");

	# TextType
	print("$H_TEXTTYPE\n");
	print("<SELECT NAME=\"texttype\">\n");
	print("<OPTION SELECTED>$H_PRE\n");
	print("<OPTION>$H_HTML\n");
	print("</SELECT><BR>\n");

	# Board̾; �����ϼ�ͳ������Ǥ���褦�ˤ�������
	print("$H_BOARD $Board<br>\n");

}


###
## �񤭹��߲��̤Τ�����̾����e-mail addr.��URL��������ɽ����
#
sub EntryUserInformation {

	# ̾���ȥ᡼�륢�ɥ쥹��URL��
	print("$H_FROM <input name=\"name\" type=\"text\" size=\"$NAME_LENGTH\"><br>\n");
	print("$H_MAIL <input name=\"mail\" type=\"text\" size=\"$MAIL_LENGTH\"><br>\n");
	print("$H_URL <input name=\"url\" type=\"text\" value=\"http://\" size=\"$URL_LENGTH\"><br>\n");
	print("$H_FMAIL <input name=\"fmail\" type=\"checkbox\" value=\"on\"><br>\n");

	print("<p><a href=\"$PROGRAM?c=as\">����</a>����Ͽ����Ƥ������ϡ���$H_FROM�פˡ�#...�פȽ񤯤ȡ���ưŪ���䴰����ޤ���<a href=\"$PROGRAM?c=an\">��Ͽ�Ϥ�����</a>��</p>\n");

}


###
## �񤭹��߲��̤Τ������ܥ����ɽ����
#
sub EntrySubmitButton {

	print("<p>���ϤǤ��ޤ����顢\n");
	print("<input type=\"submit\" value=\"����\">\n");
	print("�򲡤��Ƶ������ǧ���ޤ��礦(�ޤ���Ƥ��ޤ���)��</p>\n");

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
## ���Ѥ���
#
sub QuoteOriginalArticle {

	# Id��Board
	local($Id, $Board) = @_;

	# ���Ѥ���ե�����
	local($QuoteFile) = &GetArticleFileName($Id, $Board);

	# ������ʬ��Ƚ�Ǥ���ե饰
	local($QuoteFlag) = 0;

	open(TMP, "$KC2IN $QuoteFile |") || &MyFatal(1, $QuoteFile);
	while(<TMP>) {

		# ���ѽ�λ��Ƚ��
		$QuoteFlag = 0 if (/^$COM_ARTICLE_END$/);

		# ����ʸ�����ɽ��
		if ($QuoteFlag == 1) {
			s/&/&amp;/go;
			s/\"//go;
			s/<//go;
			s/>//go;
			print($DEFAULT_QMARK, $_);
		}

		# ���ѳ��Ϥ�Ƚ��
		$QuoteFlag = 1 if (/^$COM_ARTICLE_BEGIN$/);

	}
	close(TMP);

}


###
## ���Ѥ���(�ե�����)
#
sub QuoteOriginalFile {

	# �ե�����̾
	local($File) = @_;

	# ������ʬ��Ƚ�Ǥ���ե饰
	local($QuoteFlag) = 0;

	open(TMP, "$KC2IN $File |") || &MyFatal(1, $File);
	while(<TMP>) {

		# ���ѽ�λ��Ƚ��
		$QuoteFlag = 0 if (/^$COM_ARTICLE_END$/);

		# ����ʸ�����ɽ��
		if ($QuoteFlag == 1) {
			s/&/&amp;/go;
			s/\"//go;
			s/<//go;
			s/>//go;
			print($DEFAULT_QMARK, $_);
		}

		# ���ѳ��Ϥ�Ƚ��
		$QuoteFlag = 1 if (/^$COM_ARTICLE_BEGIN$/);

	}
	close(TMP);

}


#/////////////////////////////////////////////////////////////////////
# �ץ�ӥ塼���̴�Ϣ


###
## �ץ�ӥ塼����
## (����������cgi'���ѿ�����Ƥʤ�������������¿���Τǡġ� ^^;)
#
sub Preview {

	# Board�μ���
	local($Board) = $cgi'TAGS{'board'};

	# TextType�μ���
	local($TextType) = $cgi'TAGS{'texttype'};

	# �ƥ�ݥ��ե�����κ���
	local($TmpFile) = &MakeTemporaryFile($Board, $TextType);

	# ɽ�����̤κ���
	&MsgHeader($PREVIEW_MSG);

	# ����«
	print("<form action=\"$PROGRAM/$Board\" method =\"GET\">\n");
	print("<input name=\"file\" type=\"hidden\" value=\"$TmpFile\">\n");
	print("<input name=\"c\" type=\"hidden\" value=\"x\">\n");
	printf("<input name=\"id\" type=\"hidden\" value=\"%d\">\n",
		$cgi'TAGS{'id'});

	# ������ʸ
	print("<p>�ʲ��ε������ǧ�����顢");
	print("<input type=\"submit\" value=\"����\">");
	print("�򲡤��ƽ񤭹���ǲ�������</p>\n");

	# ��ǧ���뵭����ɽ��
	open(TMP, "$TmpFile");
	while(<TMP>) {
		print($_);
	}

	# ����«
	print("</form>\n");

	&MsgFooter;

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
	local($TmpFile) = &GetPath($Board, ".$ARTICLE_PREFIX.$$");

	# ���դ���Ф���
	local($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst)
		= localtime(time);
	local($InputDate)
		= sprintf("%d��%d��%02d��%02dʬ", $mon + 1, $mday, $hour, $min);
	# ��ʸ��̾��
	local($Text, $Name) = ($cgi'TAGS{'article'}, $cgi'TAGS{'name'});

	# �ۥ���̾����Ф���
	local($RemoteHost) = $ENV{ 'REMOTE_HOST' };

	# ���ѥե����롢����Subject
	local($ReplyArticleFile, $ReplyArticleSubject);

	# �⤷���Ѥʤ���ѥե�����̾�����
	if ($cgi'TAGS{'id'} != 0) {
		$ReplyArticleFile = &GetArticleFileName($cgi'TAGS{'id'}, '');
		$ReplyArticleSubject = &GetSubject($cgi'TAGS{'id'}, $Board);
	} elsif ($cgi'TAGS{'file'} ne '') {
		$ReplyArticleFile = "../" . $cgi'TAGS{'file'};
		$ReplyArticleSubject = &GetSubjectFromFile($cgi'TAGS{'file'});
	}

	# �����ꥢ�������å�
	$_ = $Name;
	if (/^#.*$/) {
		($Name, $cgi'TAGS{'mail'}, $cgi'TAGS{'url'})
			= &GetUserInfo($_);
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
	printf(TMP "<strong>$H_SUBJECT</strong> %s<br>\n", $cgi'TAGS{'subject'});

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
	print(TMP "<strong>$H_HOST</strong> $RemoteHost<br>\n");

	# �����
	print(TMP "<strong>$H_DATE</strong> $InputDate<br>\n");

	# ��ȿ��(���Ѥξ��)
	if ($cgi'TAGS{'id'} != 0) {
		printf(TMP "<strong>$H_REPLY</strong> [$BoardName: %d] <a href=\"$ReplyArticleFile\">$ReplyArticleSubject</a><br>\n", $cgi'TAGS{'id'});
	} elsif ($cgi'TAGS{'file'} ne '') {
		printf(TMP "<strong>$H_REPLY</strong> <a href=\"$ReplyArticleFile\">$ReplyArticleSubject</a><br>\n");
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
	print(TMP "<pre>\n") if ($TextType eq $H_PRE);

	# ����
	$Text = &tag_secure'decode($Text);
	printf(TMP "%s\n", $Text);

	# TextType�Ѹ����
	print(TMP "</pre>\n") if ($TextType eq $H_PRE);

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

	# ���򤵤줿Board�μ���
	local($Board) = substr($ENV{'PATH_INFO'}, $[ + 1);

	# ��Ͽ�ե������URL
	local($TitleFileURL) = &GetURL($Board, $TITLE_FILE_NAME);

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
## ��������Ƥ��줿����������
#
sub MakeNewArticle {

	# �ƥ�ݥ��ե�����̾��Board�����Ѥ���������Id
	local($TmpFile, $Board, $Id) = @_;

	# Board̾�Τμ���
	local($BoardName) = &GetBoardInfo($Board);

	# �����ֹ������ե�����
	local($ArticleNumFile) = &GetPath($Board, $ARTICLE_NUM_FILE_NAME);

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
	close(TMP);

	# ��å��ե�����򳫤�
	open(LOCK, "$LOCK_FILE") || &MyFatal(1, $LOCK_FILE);

	# ��å��򤫤���
	&lock;

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
	print(ART "$COM_HEADER_BEGIN\n");

	# �ܥǥ�����Ƭ�˥ܡ���̾�ȵ����ֹ桢��������
	printf(ART "<strong>$H_SUBJECT</strong> [$BoardName: %d] $Subject<br>\n", $ArticleId);

	# �ƥ�ݥ��ե����뤫��ε����Υ��ԡ�
	open(TMP, "$TmpFile") || &MyFatal(1, $TmpFile);

	# Subject�Ԥ������ѤߤʤΤ�1�����Ф���
	$Dust = <TMP>;

	while(<TMP>) {
		print(ART $_)
	}
	close(TMP);

	# �ƥ�ݥ��ե�����κ��
	unlink("$TmpFile");

	# �����եå��κ���
	print(ART "$H_FOLLOW\n<ol>\n");
	close(ART);

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
	&unlock;
	close(LOCK);

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
	local($Id, $Board, $FollowArticleId, $Fsubject, $Fname) = @_;

	# �ե������줿�����ե�����
	local($ArticleFile) = &GetArticleFileName($Id, $Board);

	# �ե������������ե�����
	local($FollowArticleFile) = &GetArticleFileName($FollowArticleId, '');

	# ȿ���᡼��Υե饰
	local(@Fmail) = ();

	# ���ե����뤫��ȿ���᡼��ΰ������Ф�
	open(FART, "$ArticleFile") || &MyFatal(1, $ArticleFile);
	while(<FART>) {
		if (/^$COM_FMAIL_BEGIN$/) {
			while(<FART>) {
				chop;
				last if (/^$COM_FMAIL_END$/);
				push(@Fmail, $_);
			}
		}
	}
	close(FART);

	# ɬ�פʤ�᡼������롣
	&FollowMail(&GetURL($Board, &GetArticleFileName($Id, '')),
		&GetURL($Board, &GetArticleFileName($FollowArticleId, '')),
		$Name, @Fmail) if (@Fmail[0] ne "");

	# ���˥ե���������ɲ�
	open(FART, ">>$ArticleFile") || &MyFatal(1, $ArticleFile);
	print(FART "<li><a href=\"$FollowArticleFile\">$Fsubject</a> �� $Fname ����\n");
	close(FART);
}


###
## �����ȥ�ꥹ�Ȥ˽񤭹���(����)
#
sub AddTitleNormal {

	# ����Id��Board, ̾�����ꡢ����
	local($Id, $Board, $Name, $Subject, $InputDate) = @_;

	# ��Ͽ�ե�����
	local($File) = &GetPath($Board, $TITLE_FILE_NAME);

	# �ɲä���ե������̾��
	local($ArticleFile) = &GetArticleFileName($Id, '');

	# �����ȥ�ե�������ɲ�
	open(TITLE, ">>$File") || &MyFatal(1, $File);
	printf(TITLE "<li><strong>$Id .</strong> <a href=\"%s\">$Subject</a> [$Name] $InputDate\n\n", $ArticleFile);
	close(TITLE);
}


###
## �����ȥ�ꥹ�Ȥ˽񤭹���(�ե���)
#
sub AddTitleFollow {

	# ����Id��Board, �ե�������Id��̾�����ꡢ����
	local($Id, $Board, $Fid, $Name, $Subject, $InputDate) = @_;

	# ��Ͽ�ե�����
	local($File) = &GetPath($Board, $TITLE_FILE_NAME);

	# �ɲä���ե������̾��
	local($ArticleFile) = &GetArticleFileName($Id, '');

	# Followed Article File Name
	local($FollowedArticleFile) = &GetArticleFileName($Fid, '');

	# TmpFile
	local($TmpFile) = &GetPath($Board, $TTMP_FILE_NAME);

	# Follow Flag
	local($AddFlag, $Nest, $NextLine) = (0, 0, ''); 

	# �����ȥ�ե�������ɲ�
	open(TTMP, ">$TmpFile") || &MyFatal(1, $TmpFile);
	open(TITLE, "$KC2IN $File |") || &MyFatal(1, $File);

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

	close(TITLE);
	close(TTMP);

	# Copy to Title File
	open(TITLE, ">$File") || &MyFatal(1, $File);
	open(TTMP, "$TmpFile") || &MyFatal(1, $TmpFile);
	while(<TTMP>) {
		print(TITLE $_);
	}
	close(TTMP);
	close(TITLE);

	# Chmod
	chmod($TITLE_FILE_PERMISSION, $File);

	# Delete Temporary File
	unlink("$TmpFile");
}


###
## all�ꥹ�Ȥ˽񤭹���
#
sub AddAllFile {

	# ����Id��Board, ̾�����ꡢ����
	local($Id, $Board, $Name, $Subject, $InputDate) = @_;

	# ��Ͽ�ե�����
	local($File) = &GetPath($Board, $ALL_FILE_NAME);

	# �ɲä���ե������̾��
	local($ArticleFile) = &GetArticleFileName($Id, '');

	# Add to 'All' file
	open(ALL, ">>$File") || &MyFatal(1, $File);
	printf(ALL "<li><strong>$Id .</strong> <a href=\"%s\">$Subject</a> [$Name] $InputDate\n\n", $ArticleFile);
	close(TITLE);
}


###
## ȿ�������ä����Ȥ�᡼�뤹�롣
#
sub FollowMail {

	# ����
	local($URL, $FollowURL, $Name, @To) = @_;

	# Subject
	local($Subject) = "Your article was followed.";

	# Message
	local($Message) = "���ʤ������Τܡ����˽񤭹����������\n$URL\n���Ф��ơ�$Name���󤫤�ȿ��������ޤ�����\n�����֤Τ������\n$FollowURL\n�������������\n\n�Ǥϡ�";

	# �᡼������
	&SendMail($Subject, $Message, @To);
}


###
## ���ե�����Υ�å��ط�
#

# ��å�
sub lock {
	flock(LOCK, $LOCK_EX);
}

# �����å�
sub unlock {
	flock(LOCK, $LOCK_UN);
}


#/////////////////////////////////////////////////////////////////////
# ���ս祽���ȴ�Ϣ


###
## ���ս�˥����ȡ���������Τ��塣
#
sub SortArticle {

	# ������(all / new)
	local($Type) = @_;

	# ���򤵤줿Board�μ���
	local($Board) = substr($ENV{'PATH_INFO'}, $[ + 1);
	# file
	local($File) = &GetPath($Board,
			(($Type eq 'new')
				? $TITLE_FILE_NAME
				: $ALL_FILE_NAME));
	local(@lines);

	open(ALL, "$KC2IN $File |") || &MyFatal(1, $File);
	while(<ALL>) {
		(/^<li>/) && (s/href=\"/href=\"$SYSTEM_DIR_URL\/$Board\//)
			&& push(@lines, $_);
	}
	close(ALL);

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
## �桼����������ȴؿ�
#
sub MyArticleSort {
	local($MyA, $MyB) = ($a, $b);
	$MyA =~ s/<li><strong>([0-9]*) .*$/$1/;
	$MyB =~ s/<li><strong>([0-9]*) .*$/$1/;
	return($MyA <=> $MyB);
}


#/////////////////////////////////////////////////////////////////////
# ���嵭��ɽ����Ϣ


###
## ��������������n�Ĥ�ɽ����
#
sub NewArticle {

	# ɽ������Ŀ������
	local($Num) = @_;

	# ���򤵤줿Board�μ���
	local($Board) = substr($ENV{'PATH_INFO'}, $[ + 1);

	# �����ֹ������ե�����
	local($ArticleNumFile) = &GetPath($Board, $ARTICLE_NUM_FILE_NAME);

	# �ǿ������ֹ�����
	local($ArticleToId) = &GetArticleId($ArticleNumFile);

	# ��������­��ʤ�����Ĵ��
	$Num = $ArticleToId if ($ArticleToId < $Num);

	# ��äƤ���ǽ�ε����ֹ�����
	local($ArticleFromId) = $ArticleToId - $Num + 1;
	local($i, $File);

	# ɽ�����̤κ���
	&MsgHeader("$NEWARTICLE_MSG: $Num");

	print("<p>������: $Num ($ArticleToId �� $ArticleFromId)</p>");

	# name�ؤΥ�󥯤�ɽ��
	print("<p> //\n");
	for ($i = $ArticleToId; ($i >= $ArticleFromId); $i--) {
		print("<a href=\"\#$i\">$i</a> //\n");
	}
	print("</p><p>\n");
	print("���ο����򥯥�å�����ȡ�����ID�ε��������Ӥޤ���\n");
	print("�����������ۤɾ�����ˤ���ޤ���\n");
	print("</p>\n");

	for ($i = $ArticleToId; ($i >= $ArticleFromId); $i--) {
		print("<a name=\"$i\">��</a><br>\n");
		print("<hr>\n");
		&ViewOriginalArticle($i, $Board);
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

	open(AID, "$ArticleNumFile") || &MyFatal(1, $ArticleNumFile);
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

		# ��������ɽ��
		print("<a name=\"$Id\">��</a><br>\n");
		print("<hr>\n");
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

	open(TMP, "$KC2IN $File |") || &MyFatal(1, $File);
	while(<TMP>) {

		# �ե�����ʬ���Ϥ�Ƚ��
		$QuoteFlag = 1 if (/^$COM_ARTICLE_END$/);

		# �ե���Id�μ���
		if (($QuoteFlag == 1) &&
		(/^<li><a href=\"$ARTICLE_PREFIX\.([^\.]*)\.html\">/)) {
			push(@Result, $1);
		}
	}
	close(TMP);

	return(@Result);
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
	open(TMP, "$KC2IN $File |") || &MyFatal(1, $File);
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
	close(TMP);

	print("<li><strong>$Id .</strong> <a href=\"\#$Id\">$Subject</a> [$Name] $InputDate\n");

}


#/////////////////////////////////////////////////////////////////////
# ����������Ϣ


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
	local($File) = &GetPath($Board,
			(($Type eq 'new')
				? $TITLE_FILE_NAME
				: $ALL_FILE_NAME));
	local($Title, $ArticleFile, $HitFlag, $Line);
	$HitFlag = 0;

	# �ꥹ�ȳ���
	print("<dl>\n");

	# �ե�����򳫤�
	open(TITLE, "$KC2IN $File |") || &MyFatal(1, $File);
	while(<TITLE>) {
		$Title = $_;
		next unless (/^<li>.*href=\"([^\"]*)\"/);
		$ArticleFile = &GetPath($Board, $1);
		$Line = &SearchArticleKeyword($ArticleFile, $Key);
		if ($Line ne "") {
			$Title =~ s/^<li>//go;
			$Title =~ s/href=\"/href=\"$SYSTEM_DIR_URL\/$Board\//;
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
	open(ARTICLE, "$KC2IN $File |") || &MyFatal(1, $File);
	while(<ARTICLE>) {
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
	print("<p>������Ͽ/��Ͽ���Ƥ��ѹ�</p>\n");
	print("<p>\n");
	print("<form action=\"$PROGRAM\" method =\"POST\">\n");
	print("<input name=\"c\" type=\"hidden\" value=\"am\">\n");
	print("$H_ALIAS <input name=\"alias\" type=\"text\" value=\"#\" size=\"$NAME_LENGTH\"><br>\n");
	print("$H_FROM <input name=\"name\" type=\"text\" size=\"$NAME_LENGTH\"><br>\n");
	print("$H_MAIL <input name=\"email\" type=\"text\" size=\"$MAIL_LENGTH\"><br>\n");
	print("$H_URL <input name=\"url\" type=\"text\" value=\"http://\" size=\"$URL_LENGTH\"><br>\n");
	print("<input type=\"submit\" value=\"����\">�򲡤��ȡ�\n");
	print("�����ꥢ���ο�����Ͽ/��Ͽ���Ƥ��ѹ����Ԥʤ��ޤ���\n");
	print("�������ѹ��ϡ���Ͽ�κݤ�Ʊ���ޥ���Ǥʤ���ФǤ��ޤ���\n");
	print("�ѹ��Ǥ��ʤ����ϡ�\n");
	print("<a href=\"mailto:$MAINT\">$MAINT</a>�ޤǥ᡼��Ǥ��ꤤ���ޤ���\n");
	print("</form></p>\n");

	print("<hr>\n");

	# ���
	print("<p>���</p>\n");
	print("<p>\n");
	print("<form action=\"$PROGRAM\" method =\"POST\">\n");
	print("<input name=\"c\" type=\"hidden\" value=\"ad\">\n");
	print("$H_ALIAS <input name=\"alias\" type=\"text\" size=\"$NAME_LENGTH\"><br>\n");
	print("<input type=\"submit\" value=\"����\">�򲡤��ȡ�\n");
	print("�嵭�����ꥢ�����������ޤ���\n");
	print("Ʊ������Ͽ�κݤ�Ʊ���ޥ���Ǥʤ���к���Ǥ��ޤ���\n");
	print("</form></p>\n");

	print("<hr>\n");

	# ����
	print("<p>\n");
	print("<form action=\"$PROGRAM\" method =\"POST\">\n");
	print("<input name=\"c\" type=\"hidden\" value=\"as\">\n");
	print("<input type=\"submit\" value=\"����\">�򲡤��ȡ�\n");
	print("�����ꥢ���򻲾ȤǤ��ޤ���\n");
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

	# �ۥ���̾����Ф���
	local($RemoteHost) = $ENV{ 'REMOTE_HOST' };

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
		$HitFlag = (($RemoteHost eq $Host{$Alias}) ? 2 : 1);
	}

	# �ۥ���̾�����ʤ�!
	&MyFatal(6, '') if ($HitFlag == 1);

	# �ǡ�������Ͽ
	$Name{$Alias} = $N;
	$Email{$Alias} = $E;
	$Host{$Alias} = $RemoteHost;
	$URL{$Alias} = $U;

	# �����ꥢ���ե�����˽񤭽Ф�
	&WriteAliasData($USER_ALIAS_FILE);

	# ɽ�����̤κ���
	&MsgHeader($ALIASMOD_MSG);
	print("<p>$H_ALIAS <strong>$A</strong>�Υǡ�����\n");
	if ($HitFlag == 2) {
		print("�ѹ����ޤ�����</p>\n");
	} else {
		print("��Ͽ���ޤ�����</p>\n");
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

	# �ۥ���̾����Ф���
	local($RemoteHost) = $ENV{ 'REMOTE_HOST' };

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
		$HitFlag = (($RemoteHost eq $Host{$Alias}) ? 2 : 1);
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
	print("<p>$H_ALIAS <strong>$A</strong>�Υǡ�����õ�ޤ�����</p>\n");
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
	print("<p><a href=\"$PROGRAM?c=an\">�����ꥢ���ο�����Ͽ/�ѹ�/�����Ԥʤ���</a></p>\n");

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
	open(ALIAS, "$KC2IN $File |") || &MyFatal(1, $File);
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
##          $Name���ΤȽ񤭹��ޤʤ���
#
sub WriteAliasData {

	# �ե�����
	local($File) = @_;
	local($Alias);

	# ��å��ե�����򳫤�
	open(LOCK, "$LOCK_FILE") || &MyFatal(1, $LOCK_FILE);

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
	close(LOCK);

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
	open(ALIAS, "$KC2IN $USER_ALIAS_FILE |")
		# �ե����뤬�ʤ��餷���ΤǤ��褦�ʤ顣
		|| return('', '', '');

	# 1��1�ĥ����å���
	while(<ALIAS>) {
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

	open(ALIAS, "$KC2IN $BOARD_ALIAS_FILE |")
		|| &MyFatal(1, $BOARD_ALIAS_FILE);
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


#/////////////////////////////////////////////////////////////////////
# ����¾���̴ؿ�


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
## ��������ɽ��
#
sub ViewOriginalArticle {

	# Id��Board
	local($Id, $Board) = @_;

	# ���Ѥ���ե�����
	local($QuoteFile) = &GetArticleFileName($Id, $Board);

	# ������ʬ��Ƚ�Ǥ���ե饰
	local($QuoteFlag) = 0;

	open(TMP, "$KC2IN $QuoteFile |") || &MyFatal(1, $QuoteFile);
	while(<TMP>) {

		# ���ѽ�λ��Ƚ��
		$QuoteFlag = 0 if (/^$COM_ARTICLE_END$/);

		# ����ʸ�����ɽ��
		if ($QuoteFlag == 1) {
			print(&URLConvert($Board, $_));
		}

		# ���ѳ��Ϥ�Ƚ��
		$QuoteFlag = 1 if ((/^$COM_HEADER_BEGIN$/) ||
					(/^$COM_ARTICLE_BEGIN$/));

	}
	close(TMP);

}


###
## ʸ�������<a href="$ARTICLE_PREFIX.??.html">�����ä��顢
## ���Ф�����URL�˽񤭴����Ƥ����֤���
#
sub URLConvert {

	# string
	local($Board, $String) = @_;
	local($File, $URL);

	($String =~ m/<a href=\"($ARTICLE_PREFIX\.[^\.]*\.html)\">/)
		|| return($String);

	$File = $1;
	$URL = &GetURL($Board, $File);

	$String =~ s/<a href=\"$File\">/<a href=\"$URL\">/g;

	return($String);

}


###
## ��������ɽ��(�ե�����)
#
sub ViewOriginalFile {

	# �ե�����̾
	local($File) = @_;

	# ������ʬ��Ƚ�Ǥ���ե饰
	local($QuoteFlag) = 0;

	open(TMP, "$KC2IN $File |") || &MyFatal(1, $File);
	while(<TMP>) {

		# ���ѽ�λ��Ƚ��
		$QuoteFlag = 0 if (/^$COM_ARTICLE_END$/);

		# ����ʸ�����ɽ��
		if ($QuoteFlag == 1) {
			print($_);
		}

		# ���ѳ��Ϥ�Ƚ��
		$QuoteFlag = 1 if (/^$COM_ARTICLE_BEGIN$/);

	}
	close(TMP);

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
## �ܡ���̾�Τ�Id����ե�����Υѥ�̾����Ф���
#
sub GetArticleFileName {

	# Id��Board
	local($Id, $Board) = @_;

	# Board�����ʤ�Board�ǥ��쥯�ȥ��⤫�����С�
	# ���Ǥʤ���Х����ƥफ������
	$Board
		? return("$SYSTEM_DIR/$Board/$ARTICLE_PREFIX.$Id.html")
		: return("$ARTICLE_PREFIX.$Id.html");
}


###
## �ܡ���̾�Τȥե�����̾���顢���Υե�����Υѥ�̾����Ф���
#
sub GetPath {

	# Board��File
	local($Board, $File) = @_;

	# �֤�
	return("$SYSTEM_DIR/$Board/$File");

}


###
## �ܡ���̾�Τȥե�����̾���顢���Υե������URL����Ф���
#
sub GetURL {

	# Board��File
	local($Board, $File) = @_;

	# �֤�
	return("$SYSTEM_DIR_URL/$Board/$File");

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
	open(TMP, "$KC2IN $ArticleFile |") || &MyFatal(1, $ArticleFile);
	while(<TMP>) {
		if (/^<strong>$H_SUBJECT<\/strong> \[[^\]]*\] (.*)<br>$/) {
			$Subject = $1;
		}
	}
	close(TMP);

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

	open(TMP, "$KC2IN $File |") || &MyFatal(1, $File);
	while(<TMP>) {

		if (/^<[Tt][Ii][Tt][Ll][Ee]>(.*)<\/[Tt][Ii][Tt][Ll][Ee]>$/) {
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
	local($File4Mail) = "$TMPDIR/tmp.kb.$$";

	# �᡼���ѥե�����򳫤�
	open(MAIL, "| $KC2OUT > $File4Mail") || &MyFatal(1, $File4Mail);

	# To�إå�
	foreach (@To) {
		print(MAIL "To: $_\n");
	}

	# Cc�إå�
	# �������ˤ����ä�������^^;
	# print(MAIL "Cc: ", $MAINT, "\n");

	# Subject�إå�
	print(MAIL "Subject: $Subject\n\n");

	# ��ʸ
	print(MAIL "$Message\n");

	# �Ĥ���
	close(MAIL);

	# �᡼������
	system("$MAIL2 < $File4Mail");

	# �ե�����õ�
	unlink("$File4Mail");
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
	} else {
		print("<p>���顼�ֹ�����: ������Ǥ�����");
		print("���Υ��顼��������������");
		print("<a href=\"mailto:$MAINT\">$MAINT</a>�ޤ�");
		print("���Τ餻��������</p>\n");
	}

	&MsgFooter;
	exit 0;
}
