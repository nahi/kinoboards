#!/usr/local/bin/perl
#
# $Id: kb.cgi,v 0.1 1995-10-22 08:57:35 nakahiro Exp $
#
# $Log: kb.cgi,v $
# Revision 0.1  1995-10-22 08:57:35  nakahiro
# alpha.
#


# kinoBoards: Kinoboard Is Network Opened BOARD System


#/////////////////////////////////////////////////////////////////////


# ToDo:
#	��Subject��Re:�ˤ���
#	��In-Reply-To:��Ĥ���
#	�ߡ֡��˥ե�������Ƥ��ޤ��פ�Ĥ��롣
#	user alias
#	newsgroup alias
#	indent
#	indent���¤��ؤ�
#	Error�ؿ�


###
## �桼��������������(ư�������˥����å�����!)
#

#
# ���Υץ�����̾��
#
$PROGRAM_NAME = "kb.cgi";

#
# �ץ���ब¸�ߤ���ǥ��쥯�ȥ��URLɽ��
#
$PROGRAM_DIR_URL = "/~nakahiro";

#
# �����Υץ�ե�����
# �����ե����뤬����(���ꤷ��ʸ����).(�����ֹ�).html�פˤʤ롣
#
$ARTICLE_PREFIX = "kb";

#
# ��å����������
#
$ENTRY_MSG   = "kinoBoards�ؤν񤭹���";
$PREVIEW_MSG = "�񤭹��ߤ����Ƥ��ǧ���Ʋ�����";
$THANKS_MSG  = "�񤭹��ߤ��꤬�Ȥ��������ޤ���";
$ERROR_MSG   = "ERROR!";

$ADDRESS = "Copyright 1995 <a href=\"http://www.kinotrope.co.jp/\">kinotrope Co.,Ltd.</a> &amp; <a href=\"http://www.ohara.info.waseda.ac.jp/person/nakahiro/nakahiro.html\">nakahiro</a> // ��̵��ž��";

$H_BOARD = "�ܡ���:";
$H_SUBJECT = "���ꡡ:";
$H_FROM = "�ʤޤ�:";
$H_MAIL = "�᡼��:";
$H_HOST = "�ޥ���:";
$H_DATE = "�����:";
$H_REPLY = "������:";

#
# �����Ϲ��ܤ��礭��
#
$SUBJECT_LENGTH = 45;
$TEXT_ROWS      = 15;
$TEXT_COLS      = 50;
$NAME_LENGTH    = 45;
$MAIL_LENGTH    = 37;
$URL_LENGTH     = 37;


#/////////////////////////////////////////////////////////////////////


###
## ����¾�����(����������Ϥ��¤�ɬ�פϤʤ����Ϥ� ^^;)
#

#
# ���Υץ�����URL
#
$PROGRAM = $PROGRAM_DIR_URL . "/" . $PROGRAM_NAME;

#
# �ե�����
#
# ��å��ե�����
$LOCK_FILE = ".lock.kb";
# �����ֹ�ե�����
$ARTICLE_NUM_FILE_NAME = ".articleid";
# �����ȥ�ե�����
$TITLE_FILE_NAME = "index.html";
# �桼�������ꥢ���ե�����
$USER_ALIAS_FILE = "aliases";
# �˥塼�����롼�ץ����ꥢ���ե�����
$NG_ALIAS_FILE = "newsgroups";

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

	local($Command, $id);

	# ɸ������(POST)�ޤ��ϴĶ��ѿ�(GET)�Υǥ����ɡ�
	&cgi'decode;

	# REQUEST_METHOD��POST�ʤ�Preview���̤ء�GET�ʤ���˱�����ʬ�����롣
	#
	#	����:				c=n
	#	���ѤĤ��ե���:	c=q&id=[1-9][0-9]*
	#	���Ѥʤ��ե���:	c=f&id=[1-9][0-9]*
	#
	#	��ǧ�Ѥ�:			c=x&id=[1-9][0-9]*(���ѤǤʤ�����id=0)
	#

	&Preview, last MAIN if ($ENV{'REQUEST_METHOD'} eq "POST");

	$Command = $cgi'tags{'c'};
	$Id = $cgi'tags{'id'};

	&Entry($NO_QUOTE, 0),            last MAIN if ($Command eq "n");
	&Entry($QUOTE_ON, $Id),          last MAIN if ($Command eq "q");
	&Entry($NO_QUOTE, $Id),          last MAIN if ($Command eq "f");
	&Thanks($cgi'tags{'file'}, $Id), last MAIN if ($Command eq "x");

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

	# ɽ�����̤κ���
	&MsgHeader($ENTRY_MSG);

	# �ե����ξ��
	if ($Id != 0) {
		print("<pre>\n");
		&Quote($Id, $Board);
		print("</pre>\n<hr>\n");
		print("<h2>��ε�����ȿ������</h2>");
	}

	# ����«
	print("<form action=\"$PROGRAM\" method =\"POST\">\n");
	print("<input name=\"board\" type=\"hidden\" value=\"$Board\">\n");

	# ����Id; ���ѤǤʤ��ʤ�0��
	print("<input name=\"id\" type=\"hidden\" value=\"$Id\">\n");

	# ������ʸ
	print("<p>����Ū��HTML�Ȥ��ƽ񤭹���ǲ�������HTML���狼��ʤ����ϡ����̤�ʸ�ϤȤ����Ǥ�����ǤߤƲ�����������櫓���ϤǤ��ޤ��󤬡��ޤ��������餤�ʤ鲿�Ȥ��ʤ�Ȼפ��ޤ���^^;</p>\n");

	# Subject(�ե����ʤ鼫ưŪ��ʸ����������)
	if ($Id != 0) {
		printf("$H_SUBJECT <input name=\"subject\" value=\"%s\" size=\"$SUBJECT_LENGTH\"><br>\n", &GetReplySubject($Id, $Board));
	} else {
		print("$H_SUBJECT <input name=\"subject\" value=\"\" size=\"$SUBJECT_LENGTH\"><br>\n");
	}

	# ��ʸ(���Ѥ���ʤ鸵����������)
	print("<textarea name=\"article\" rows=\"$TEXT_ROWS\" cols=\"$TEXT_COLS\">\n");
	&Quote($Id, $Board) if ($Id != 0 && $QuoteFlag == $QUOTE_ON);
	print("</textarea><br>\n");

	# ̾���ȥ᡼�륢�ɥ쥹��URL��
	print("$H_NAME <input name=\"name\" size=\"$NAME_LENGTH\"><br>\n");
	print("$H_MAIL <input name=\"mail\" size=\"$MAIL_LENGTH\"><br>\n");
	print("URL(���Ǥ�OK):<input name=\"url\" value=\"http://\" size=\"$URL_LENGTH\"><br>\n");

	print("<p>���ϤǤ��ޤ����顢\n");
	print("<input type=\"submit\" value=\"�������ǧ����\">\n");
	print("�ܥ���򲡤��Ƥ���������</p>\n");

	# ����«
	print("</form>\n");

	&MsgFooter;
}


###
## �ץ�ӥ塼����
#
sub Preview {

	# Board̾�μ���
	local($Board) = $cgi'tags{'board'};

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

	# ����
	local($name, $mail, $url, $subject, $article)
		= $cgi'

HERE!

	# �⤷���Ѥʤ���ѥե�����̾�����
	if ($cgi'tags{'id'} != 0) {
		$ReplyArticleFile = &GetArticleFileName($cgi'tags{'id'}, '');
		$ReplyArticleSubject = &GetSubject($cgi'tags{'id'}, $Board);
	}

	# �����ꥢ�������å�
	$_ = $cgi'tags{'name'};
	($cgi'tags{'name'}, $cgi'tags{'mail'}, $cgi'tags{'url'}) = &GetUserInfo($_)
		if (/^#.*$/);

	# �������å�
	if ($cgi'tags{'subject'} eq "") {
		&MsgHeader($ERROR_MSG);
		print("<H2>Subject������ޤ���</h2>");
		print("<p>��äƤ⤦���١�</p>");
		&MsgFooter;
		exit 0;
	} elsif ($cgi'tags{'article'} eq "") {
		&MsgHeader($ERROR_MSG);
		print("<H2>����������ޤ���</h2>");
		print("<p>��äƤ⤦���١�</p>");
		&MsgFooter;
		exit 0;
	} elsif ($cgi'tags{'name'} eq "") {
		&MsgHeader($ERROR_MSG);
		print("<H2>��̾��������ޤ���</h2>");
		print("<p>���뤤�ϡ������ꥢ����Ͽ���ְ�äƤ��ޤ���</p>");
		print("<p>��äƤ⤦���١�</p>");
		&MsgFooter;
		exit 0;
	} elsif ($cgi'tags{'mail'} eq "") {
		&MsgHeader($ERROR_MSG);
		print("<H2>�᡼�륢�ɥ쥹������ޤ���</h2>");
		print("<p>��äƤ⤦���١�</p>");
		&MsgFooter;
		exit 0;
	}

	# �ƥ�ݥ��ե�����˽񤭽Ф���
	open(TMP, ">$TmpFile") || die "Can't open $TmpFile .";

	# �ޤ��إå���
	printf(TMP "<b>$H_SUBJECT</b> %s<br>\n", $cgi'tags{'subject'});

	if ($cgi'tags{'url'} eq "http://" || $cgi'tags{'url'} eq "") {
		# URL���ʤ����
		printf(TMP "<b>$H_FROM</b> %s<br>\n", $cgi'tags{'name'});
	} else {
		# URL��������
		printf(TMP "<b>$H_FROM</b> <a href=\"%s\">%s</a><br>\n", $cgi'tags{'url'}, $cgi'tags{'name'});
	}

	printf(TMP "<b>$H_MAIL</b> <a href=\"mailto:%s\">&lt; %s &gt;</a><br>\n",
		$cgi'tags{'mail'}, $cgi'tags{'mail'});
	print(TMP "<b>$H_HOST</b> $RemoteHost<br>\n");
	print(TMP "<b>$H_DATE</b> $InputDate<br>\n");

	# ���Ѥξ��
	if ($cgi'tags{'id'} != 0) {
		printf(TMP "<b>$H_REPLY</b> <a href=\"$ReplyArticleFile\">$ReplyArticleSubject</a><br>\n");
	}

	print(TMP "----<br>\n");

	# article begin
	print(TMP "<!-- Article Begin -->\n");

	# ����
	printf(TMP "%s\n", $cgi'tags{'article'});

	# article end
	print(TMP "<!-- Article End -->\n");
	print(TMP "<hr>\n");
	close TMP;

	# ɽ�����̤κ���
	&MsgHeader($PREVIEW_MSG);

	# ����«
	print("<form action=\"$PROGRAM/$Board\" method =\"GET\">\n");
	print("<input name=\"file\" type=\"hidden\" value=\"$TmpFile\">\n");
	print("<input name=\"c\" type=\"hidden\" value=\"x\">\n");
	printf("<input name=\"id\" type=\"hidden\" value=\"%d\">\n",
		$cgi'tags{'id'});

	# ������ʸ
	print("<p>�ʲ��ε������ǧ���ơ�");
	print("<input type=\"submit\" value=\"�񤭹���\">");
	print("�ܥ���򲡤��Ƥ���������</p>\n");

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
## ��������Ƥ��줿����������
#
sub MakeNewArticle {

	# �ƥ�ݥ��ե�����̾��Board��̾�Ρ����Ѥ���������Id
	local($TmpFile, $Board, $Id) = @_;

	# �����ֹ������ե�����
	local($ArticleNumFile) = $Board . "/" . $ARTICLE_NUM_FILE_NAME;

	# ��Ͽ�ե�����
	local($TitleFile) = $Board . "/" . $TITLE_FILE_NAME;

	# �����ε����ֹ�ȥե�����̾
	local($ArticleId, $ArticleFile);

	# ���֥������ȡ���������̾��
	local($Subject, $InputDate, $Name);

	# �ƥ�ݥ��ե����뤫��Subject������Ф�
	open(TMP, "$TmpFile") || die "Can't open $TmpFile .";
	while(<TMP>) {

		# subject����Ф���
		if (/^<b>$H_SUBJECT<\/b> (.*)<br>$/) {$Subject = $1; }
		# ���դ���Ф���
		if (/^<b>$H_DATE<\/b> (.*)<br>$/) {$InputDate = $1; }
		# ̾������Ф���
		if (/^<b>$H_FROM<\/b> <a[^>]*>(.*)<\/a><br>$/) {
			$Name = $1;
		} elsif (/^<b>$H_FROM<\/b> (.*)<br>$/) {
			$Name = $1;
		}

	}
	close TMP;

	# ��å��ե�����򳫤�
	open(LOCK, "$LOCK_FILE") || die "Can't open $LOCK_FILE .";
	# ��å��򤫤���
	&lock();
	# ���ʤ��ʤ�
	seek(ART, 0, 2);
	seek(TITLE, 0, 2);

	# �����ֹ�����
	open(AID, "$ArticleNumFile") || die "Can't open $ArticleNumFile .";
	while(<AID>) {
		$ArticleId = unpack("A5", $_);
	}
	close AID;

	# �����Υե�����̾�����
	$ArticleFile = &GetArticleFileName($ArticleId, $Board);

	# ������ƥ�ݥ��ե����뤫�������Υե������
	open(TMP, "$TmpFile") || die "Can't open $TmpFile .";
	open(ART, ">$ArticleFile") || die "Can't open $ArticleFile .";

	# �����إå��κ���
	printf(ART "<title>[$Board: %05d] $Subject</title>\n", $ArticleId);
	print(ART "<body>\n");
	print(ART "<a href=\"index.html\">���</a> // ");
	printf(ART "<a href=\"%s\">����</a> // ",
		&GetArticleFileName(($ArticleId - 1), ''));
	printf(ART "<a href=\"%s\">����</a> // ",
		&GetArticleFileName(($ArticleId + 1), ''));
	print(ART "ȿ�� ( <a href=\"$PROGRAM/$Board?c=q&id=$ArticleId\">����ͭ��</a> / ");
	print(ART "<a href=\"$PROGRAM/$Board?c=f&id=$ArticleId\">̵��</a> )\n");
	print(ART "<hr>\n");

	# �ܥǥ�����Ƭ�˥ܡ���̾�ȵ����ֹ�������
	printf(ART "<b>$H_BOARD</b> [$Board: %05d]<br>\n", $ArticleId);

	# �ƥ�ݥ��ե����뤫��ε����Υ��ԡ�
	while(<TMP>) {
		print(ART $_)
	}

	# �����եå��κ���
	# �ե���������
	print(ART "��ȿ��\n<ol>\n");

	close ART;
	close TMP;

	# �ƥ�ݥ��ե�����κ��
	unlink("$TmpFile");

	# �����ȥ�ե�������ɲ�
	open(TITLE, ">>$TitleFile") || die "Can't open $TitleFile .";
	printf(TITLE "<li><i>$InputDate</i> <a href=\"%s\">$Subject</a> [$Name]\n",
		&GetArticleFileName($ArticleId, ''));
	close TITLE;

	# �����ֹ���ɲ�
	$NextArticleId = $ArticleId + 1;
	`echo $NextArticleId > $ArticleNumFile`;

	# ��å��򳰤���
	&unlock();
	close LOCK;

	# �ե������줿�����˥ե������줿���Ȥ�񤭹��ࡣ
	# �ե������������ե�����̾��ľ���Ϥ��ʤ��Τϡ�
	# ���Фε������ۤʤ뤿�ᡣ
	&ArticleWasFollowed($Id, $Board, $ArticleId, $Subject, $Name);
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

	# ��å��ե�����򳫤�
	open(LOCK, "$LOCK_FILE") || die "Can't open $LOCK_FILE .";
	# ��å��򤫤���
	&lock();
	# ���ʤ��ʤ�
	seek(ART, 0, 2);

	# �ɲ�
	open(ART, ">>$ArticleFile") || die "Can't open $ArticleFile .";
	print(ART "<li><a href=\"$FollowArticleFile\">$Fsubject</a> �� $Fname ����\n");
	close ART;

	# ��å��򳰤���
	&unlock();
	close LOCK;
}


###
## ���ե�����Υ�å��ط�
#
sub lock {
	# ��å�
	flock(LOCK, $LOCK_EX);
}

sub unlock {
	# �����å�
	flock(LOCK, $LOCK_UN);
}


###
## ���Ѥ���
#
sub Quote {

	# Id��Board��̾��
	local($Id, $Board) = @_;

	# ���Ѥ���ե�����
	local($QuoteFile) = &GetArticleFileName($Id, $Board);

	# ������ʬ��Ƚ�Ǥ���ե饰
	local($QuoteFlag) = 0;

	open(TMP, "$QuoteFile") || die "Can't open $QuoteFile .";
	while(<TMP>) {

		# ���ѽ�λ��Ƚ��
		$QuoteFlag = 0 if (/^<!-- Article End -->$/);

		# ����ʸ�����ɽ��
		if ($QuoteFlag == 1) {
			s/&/&amp;/go;
			s/\"//go;
			s/<//go;
			s/>//go;
			print(" &gt; ", $_);
		}

		# ���ѳ��Ϥ�Ƚ��
		$QuoteFlag = 1 if (/^<!-- Article Begin -->$/);

	}
	close TMP;

}


###
## �����ꥢ������桼����̾�����᡼�롢URL���äƤ��롣
#
sub GetUserInfo {

	# �����ꥢ��̾
	local($Alias) = @_;

	# ̾�����᡼�롢URL
	local($Name, $Mail, $URL);

	open(ALIAS, "$USER_ALIAS_FILE") || die "Can't open $USER_ALIAS_FILE .";
	while(<ALIAS>) {

		# �ޥå����ʤ��㼡�ء�
		next unless (/^$Alias:([^:]*):([^:]*):(.*)$/);

		chop;
		$Name = $1;
		$Mail = $2;
		$URL = $3;

		# ����ˤ����֤�
		return($Name, $Mail, $URL);
	}

	# �ҥåȤ���
	return('', '', '');
}


###
## ����Id�ε�������Subject���äƤ��ơ���Ƭ�ˡ�Re: �פ�1�Ĥ����Ĥ����֤���
#
sub GetReplySubject {

	# Id��Board��̾��
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

	# Id��Board��̾��
	local($Id, $Board) = @_;

	# Subject����Ф��ե�����
	local($ArticleFile) = &GetArticleFileName($Id, $Board);

	# ���Ф���Subject
	local($Subject) = '';

	# �����ե����뤫��Subjectʸ�������Ф���
	open(TMP, "$ArticleFile") || die "Can't open $ArticleFile .";
	while(<TMP>) {
		if (/^<b>$H_SUBJECT<\/b> (.*)<br>$/) {
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

	# Id��Board��̾��
	local($Id, $Board) = @_;

	# Board̾�Τ����ʤ�Board�ǥ��쥯�ȥ��⤫�����С�
	# ���Ǥʤ���Х����ƥफ������
	$Board
		? return("$Board/$ARTICLE_PREFIX.$Id.html")
		: return("$ARTICLE_PREFIX.$Id.html");
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
        }
}

#/////////////////////////////////////////////////////////////////////
