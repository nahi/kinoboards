#!/usr/local/bin/perl5
#
# $Id: kb.cgi,v 3.1 1996-01-26 07:33:18 nakahiro Exp $
#
# $Log: kb.cgi,v $
# Revision 3.1  1996-01-26 07:33:18  nakahiro
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
## ヘッダファイルの読み込み
#
require('kb.ph');
require('cgi.pl');
require('tag_secure.pl');


###
## メイン
#

# コマンド表:
#	新規投稿:		c=n
#	引用つきフォロー:	c=q&id={[1-9][0-9]*}
#	引用なしフォロー:	c=f&id={[1-9][0-9]*}
#	URL引用フォロー:	c=q/f&url={URL}
#	アイコン表示:		c=i
#	記事のプレビュー:	c=p&(空)....
#	確認済み画面:		c=x&id={[1-9][0-9]*(引用でない時id=0)}
#	日付順ソート:		c=r&type=all|new
#	最新の記事n個:		c=l&num={[1-9][0-9]*}
#	threadまとめ読み:	c=t&id={[1-9][0-9]*}
#	検索:			c=s&type=all|new&key={keyword}
#	エイリアス登録画面:	c=an
#	エイリアス登録:		c=am&alias=..&name=..&email=..&url=..
#	エイリアス削除:		c=ad&alias=...
#	エイリアス参照:		c=as

MAIN: {

	# 標準入力(POST)または環境変数(GET)のデコード。
	&cgi'decode;

	# 値の抽出
	local($Command) = $cgi'TAGS{'c'};
	local($Id) = $cgi'TAGS{'id'};
	local($Num) = $cgi'TAGS{'num'};
	local($Type) = $cgi'TAGS{'type'};
	local($Key) = $cgi'TAGS{'key'};
	local($Alias) = $cgi'TAGS{'alias'};
	local($Name) = $cgi'TAGS{'name'};
	local($Email) = $cgi'TAGS{'email'};
	local($File) = $cgi'TAGS{'file'};
	local($URL) = $cgi'TAGS{'url'};

	# コマンドタイプによる分岐
	&Entry($NO_QUOTE, 0),		last MAIN if ($Command eq "n");
	$Id ? &Entry($QUOTE_ON, $Id) : &URLEntry($QUOTE_ON, $URL),
					last MAIN if ($Command eq "q");
	$Id ? &Entry($NO_QUOTE, $Id) : &URLEntry($NO_QUOTE, $URL),
					last MAIN if ($Command eq "f");
	&ShowIcon,			last MAIN if ($Command eq "i");
	&Preview,			last MAIN if ($Command eq "p");
	&Thanks($File, $Id),		last MAIN if ($Command eq "x");
	&SortArticle($Type),		last MAIN if ($Command eq "r");
	&NewArticle($Num),		last MAIN if ($Command eq "l");
	&ThreadArticle($Id),		last MAIN if ($Command eq "t");
	&SearchArticle($Type, $Key),	last MAIN if ($Command eq "s");
	&FollowMailEntry($Id),		last MAIN if ($Command eq "me");
	&FollowMailAdd($Id, $Email),	last MAIN if ($Command eq "ma");
	&AliasNew,			last MAIN if ($Command eq "an");
	&AliasMod($Alias, $Name, $Email, $URL),
					last MAIN if ($Command eq "am");
	&AliasDel($Alias),		last MAIN if ($Command eq "ad");
	&AliasShow,			last MAIN if ($Command eq "as");

	print("illegal command was given.\n");
}


###
## おしまい
#
exit 0;


#/////////////////////////////////////////////////////////////////////
# 書き込み画面関連


###
## 書き込み画面
#
sub Entry {

	# 引用あり/なしと、引用する場合はそのId(引用しない時は0)
	local($QuoteFlag, $Id) = @_;

	# 表示画面の作成
	&MsgHeader($ENTRY_MSG, $BOARD);

	# フォローの場合
	if ($Id != 0) {
		&ViewOriginalArticle($Id);
		print("<hr>\n");
		print("<h2>$H_REPLYMSG</h2>");
	}

	# お約束
	print("<form action=\"$PROGRAM_FROM_BOARD/$BOARD\" method =\"POST\">\n");
	print("<input name=\"c\" type=\"hidden\" value=\"p\">\n");

	# 引用Id; 引用でないなら0。
	print("<input name=\"id\" type=\"hidden\" value=\"$Id\">\n");

	# あおり文、Board名、アイコン
	&EntryHeader;

	# Subject(フォローなら自動的に文字列を入れる)
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

	# 本文(引用ありなら元記事を挿入)
	print("<textarea name=\"article\" rows=\"$TEXT_ROWS\" cols=\"$TEXT_COLS\">");
	&QuoteOriginalArticle($Id, $BOARD)
		if ($Id != 0 && $QuoteFlag == $QUOTE_ON);
	print("</textarea><br>\n");

	# 名前とメールアドレス、URLを表示。
	&EntryUserInformation;

	# ボタン
	&EntrySubmitButton;

	# お約束
	print("</form>\n");

	&MsgFooter;
}


###
## 書き込み画面(URL)
#
sub URLEntry {

	# 引用あり/なしと、URL
	local($QuoteFlag, $URL) = @_;

	# file
	local($File) = &GetPath($BOARD, ".$QUOTE_PREFIX.$$");
	local($Server, $HttpPort, $Resource);

	# split
	if ($URL =~ m#http://([^:]*):([0-9]*)(/.*)$#io) {
	    $Server = $1;
	    $HttpPort = $2;
	    $Resource = $3;
	} elsif ($URL =~ m#http://([^/]*)(/.*)$#io) {
	    $Server = $1;
	    $HttpPort = $DEFAULT_HTTP_PORT;
	    $Resource = $2;
	} else {
	    &MyFatal(10, $URL);
	}

	# connect
	&HttpConnect($Server, $HttpPort, $Resource, $File)
	    || &MyFatal(10, $URL);

	# 表示画面の作成
	&MsgHeader($ENTRY_MSG, $BOARD);

	# 引用ファイルの表示
	&ViewOriginalFile($File);
	print("<hr>\n");
	print("<h2>$H_REPLYMSG</h2>");

	# お約束
	print("<form action=\"$PROGRAM_FROM_BOARD/$BOARD\" method =\"POST\">\n");
	print("<input name=\"c\" type=\"hidden\" value=\"p\">\n");

	# 引用Id; 正規の引用でないので0。
	print("<input name=\"id\" type=\"hidden\" value=\"0\">\n");

	# 引用ファイル
	print("<input name=\"qurl\" type=\"hidden\" value=\"$URL\">\n");
	print("<input name=\"file\" type=\"hidden\" value=\"$File\">\n");

	# あおり文、Board名、アイコン
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

	# 本文(引用ありなら元記事を挿入)
	print("<textarea name=\"article\" rows=\"$TEXT_ROWS\" cols=\"$TEXT_COLS\">");
	&QuoteOriginalFile($File) if ($QuoteFlag == $QUOTE_ON);
	print("</textarea><br>\n");

	# 名前とメールアドレス、URLを表示。
	&EntryUserInformation;

	# ボタン
	&EntrySubmitButton;

	# お約束
	print("</form>\n");

	&MsgFooter;
}


###
## 書き込み画面のうち、あおり文、TextType、Board名を表示。
#
sub EntryHeader {

	# Board名称の取得
	local($BoardName) = &GetBoardInfo($BOARD);

	# あおり文
	print("<p>$H_AORI</p>\n");

	# Board名; 本当は自由に選択できるようにしたい。
	print("$H_BOARD <a href=\"$TITLE_FILE_NAME\">$BoardName</a><br>\n");

	# アイコンの選択
	&EntryIcon;

}


###
## 書き込み画面のうち、アイコン選択部分を表示。
#
sub EntryIcon {

	local($FileName, $Title);

	print("$H_ICON\n");
	print("<SELECT NAME=\"icon\">\n");
	print("<OPTION SELECTED>$H_NOICON\n");

	# 一つ一つ表示
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
## 書き込み画面のうち、名前、e-mail addr.、URL入力部を表示。
#
sub EntryUserInformation {

	# 名前とメールアドレス、URL。
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
## 書き込み画面のうち、ボタンを表示。
#
sub EntrySubmitButton {

	print("<p>$H_ENTRYINFO\n");
	print("<input type=\"submit\" value=\"$H_PUSHHERE\">\n");
	print("</p>\n");

}


###
## あるIdの記事からSubjectを取ってきて、先頭に「Re: 」を1つだけつけて返す。
#
sub GetReplySubject {

	# IdとBoard
	local($Id, $Board) = @_;

	# 取り出したSubject
	local($Icon, $Subject) = '';

	# Subjectを取りだし、先頭に「Re: 」がくっついてたら取り除く。
	($Icon, $Subject) = &GetSubject($Id, $Board);
	$Subject =~ s/^Re: //;

	# 先頭に「Re: 」をくっつけて返す。
	return("Re: $Subject");

}


###
## あるファイルからTitleを取ってきて、先頭に「Re: 」をつけて返す。
#
sub GetReplySubjectFromFile {

	# ファイル
	local($File) = @_;

	# 取り出したSubject
	local($Title) = &GetSubjectFromFile($File);

	# 先頭に「Re: 」をくっつけて返す。
	return("Re: $Title");

}


###
## 引用する
#
sub QuoteOriginalArticle {

	# IdとBoard
	local($Id, $Board) = @_;

	# 引用するファイル
	local($QuoteFile) = &GetArticleFileName($Id, $Board);

	# 引用部分を判断するフラグ
	local($QuoteFlag) = 0;

	open(TMP, "<$QuoteFile") || &MyFatal(1, $QuoteFile);
	while(<TMP>) {

		# コード変換
		&jcode'convert(*_, 'euc');

		# 引用終了の判定
		$QuoteFlag = 0 if (/$COM_ARTICLE_END/);

		# 引用文字列の表示
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

		# 引用開始の判定
		$QuoteFlag = 1 if (/$COM_ARTICLE_BEGIN/);

	}

	close(TMP);

}


###
## 引用する(ファイル)
#
sub QuoteOriginalFile {

	# ファイル名
	local($File) = @_;

	# 引用部分を判断するフラグ
	local($QuoteFlag) = 0;

	open(TMP, "<$File") || &MyFatal(1, $File);
	while(<TMP>) {

		# コード変換
		&jcode'convert(*_, 'euc');

		# 引用終了の判定
		$QuoteFlag = 0 if (/$COM_ARTICLE_END/);

		# 引用文字列の表示
		if ($QuoteFlag == 1) {
			s/&/&amp;/go;
			s/\"//go;
			s/<//go;
			s/>//go;
			print($DEFAULT_QMARK, $_);
		}

		# 引用開始の判定
		$QuoteFlag = 1 if (/$COM_ARTICLE_BEGIN/);

	}
	close(TMP);

}


#/////////////////////////////////////////////////////////////////////
# アイコン表示画面関連


###
## アイコン表示画面
#
sub ShowIcon {

	local($BoardName) = &GetBoardInfo($BOARD);
	local($FileName, $Title);

	# 表示画面の作成
	&MsgHeader("$SHOWICON_MSG");
	print("<p>$H_ICONINTRO</p>\n");
	print("<p><dl>\n");

	# 一つ一つ表示
	open(ICON, "$ICON_DIR/$BOARD.$ICONDEF_POSTFIX")
		|| (open(ICON, "$ICON_DIR/$DEFAULT_ICONDEF")
		|| &MyFatal(1, "$ICON_DIR/$DEFAULT_ICONDEF"));
	while(<ICON>) {
		chop;
		($FileName, $Title) = split(/\t/, $_);
		print("<dt><img src=\"$ICON_DIR/$FileName\"> : $Title\n");
	}
	close(ICON);

	print("</dl></p>\n");

	&MsgFooter;

}


#/////////////////////////////////////////////////////////////////////
# プレビュー画面関連


###
## プレビュー画面
## (ここだけはcgi'を変数に落してない。汚いけど、数が多いので…… ^^;)
#
sub Preview {

	# TextTypeの取得
	local($TextType) = $cgi'TAGS{'texttype'};

	# テンポラリファイルの作成
	local($TmpFile) = &MakeTemporaryFile($TextType);

	# 表示画面の作成
	&MsgHeader("$PREVIEW_MSG", $BOARD);

	# お約束
	print("<form action=\"$PROGRAM_FROM_BOARD/$BOARD\" method =\"GET\">\n");
	print("<input name=\"file\" type=\"hidden\" value=\"$TmpFile\">\n");
	print("<input name=\"c\" type=\"hidden\" value=\"x\">\n");
	printf("<input name=\"id\" type=\"hidden\" value=\"%d\">\n",
		$cgi'TAGS{'id'});

	# あおり文
	print("<p>$H_POSTINFO");
	print("<input type=\"submit\" value=\"$H_PUSHHERE\"></p>\n");

	# 確認する記事の表示
	open(TMP, "$TmpFile");
	while(<TMP>) {
		print("$_");
	}

	# お約束
	print("</form>\n");

	&MsgFooter;

}


###
## 確認用テンポラリファイルを作成してファイル名を返す。
#
sub MakeTemporaryFile {

	# TextTypeの取得
	local($TextType) = @_;

	# Board名称の取得
	local($BoardName) = &GetBoardInfo($BOARD);

	# テンポラリファイル名の取得
	local($TmpFile) = &GetPath($BOARD, ".$ARTICLE_PREFIX.$$");

	# 日付を取り出す。
	local($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst)
		= localtime(time);
	local($InputDate)
		= sprintf("%d/%d(%02d:%02d)", $mon + 1, $mday, $hour, $min);
	# 本文と名前
	local($Text, $Name) = ($cgi'TAGS{'article'}, $cgi'TAGS{'name'});

	# 引用ファイル、そのSubject
	local($ReplyArticleFile, $ReplyArticleIcon, $ReplyArticleSubject)
		= ('', '', '');

	# もし引用なら引用ファイル名を取得
	if ($cgi'TAGS{'id'} != 0) {
		$ReplyArticleFile = &GetArticleFileName($cgi'TAGS{'id'}, '');
		($ReplyArticleIcon, $ReplyArticleSubject)
			= &GetSubject($cgi'TAGS{'id'}, $BOARD);
	} elsif ($cgi'TAGS{'file'} ne '') {
		$ReplyArticleFile = $cgi'TAGS{'file'};
		$ReplyArticleSubject = &GetSubjectFromFile($cgi'TAGS{'file'});
	}

	# エイリアスチェック
	$_ = $Name;
	if (/^#.*$/) {
		($Name, $cgi'TAGS{'mail'}, $cgi'TAGS{'url'})
			= &GetUserInfo($_);
		&MyFatal(7, $cgi'TAGS{'name'}) if ($Name eq "");
	}

	# 空チェック
	&MyFatal(2, '') if ($cgi'TAGS{'subject'} eq "")
		|| ($cgi'TAGS{'article'} eq "")
		|| ($Name eq "")
		|| ($cgi'TAGS{'mail'} eq "");

	# 文字列チェック
	&CheckName($Name);
	&CheckEmail($cgi'TAGS{'mail'});
	&CheckURL($cgi'TAGS{'url'});

	# サブジェクトのタグチェック
	$_ = $cgi'TAGS{'subject'};
	&MyFatal(4, '') if (/</);

	# テンポラリファイルに書き出す。
	open(TMP, ">$TmpFile") || &MyFatal(1, $TmpFile);

	# 題
	($cgi'TAGS{'icon'} eq $H_NOICON)	
	? printf(TMP "<strong>$H_SUBJECT</strong> %s<br>\n",
		$cgi'TAGS{'subject'})
	: printf(TMP "<strong>$H_SUBJECT</strong> <img src=\"%s\"> %s<br>\n",
		&GetIconURL($cgi'TAGS{'icon'}),
		$cgi'TAGS{'subject'});

	# お名前
	if ($cgi'TAGS{'url'} eq "http://" || $cgi'TAGS{'url'} eq "") {
		# URLがない場合
		printf(TMP "<strong>$H_FROM</strong> %s<br>\n", $Name);
	} else {
		# URLがある場合
		printf(TMP "<strong>$H_FROM</strong> <a href=\"%s\">%s</a><br>\n", $cgi'TAGS{'url'}, $Name);
	}

	# メール
	printf(TMP "<strong>$H_MAIL</strong> <a href=\"mailto:%s\">&lt;%s&gt;</a><br>\n",
		$cgi'TAGS{'mail'}, $cgi'TAGS{'mail'});

	# マシン
	print(TMP "<strong>$H_HOST</strong> $REMOTE_HOST<br>\n");

	# 投稿日
	print(TMP "<strong>$H_DATE</strong> $InputDate<br>\n");

	# ▼反応(引用の場合)
	if ($cgi'TAGS{'id'} != 0) {
		printf(TMP "<strong>$H_REPLY</strong> [$BoardName: %d] $ReplyArticleIcon<a href=\"$ReplyArticleFile\">$ReplyArticleSubject</a><br>\n", $cgi'TAGS{'id'});
	} elsif ($cgi'TAGS{'qurl'} ne '') {
		printf(TMP "<strong>$H_REPLY</strong> <a href=\"%s\">$ReplyArticleSubject</a><br>\n", $cgi'TAGS{'qurl'});
	}

	# 反応があったらメール
	print(TMP "$COM_FMAIL_BEGIN\n");
	printf(TMP "%s\n", $cgi'TAGS{'mail'}) if ($cgi'TAGS{'fmail'} eq "on");
	print(TMP "$COM_FMAIL_END\n");

	# 切れ目
	print(TMP "------------------------<br>\n");

	# article begin
	print(TMP "$COM_ARTICLE_BEGIN\n");

	# TextType用前処理
	print(TMP "<pre>\n") if ((! $SYS_TEXTTYPE) || ($TextType eq $H_PRE));

	# 記事
	$Text = &tag_secure'decode($Text);
	printf(TMP "%s\n", $Text);

	# TextType用後処理
	print(TMP "</pre>\n") if ((! $SYS_TEXTTYPE) || ($TextType eq $H_PRE));

	# article end
	print(TMP "$COM_ARTICLE_END\n");
	print(TMP "<hr>\n");
	close(TMP);

	# ファイル名を返す。
	return($TmpFile);
}


#/////////////////////////////////////////////////////////////////////
# 登録後画面関連


###
## 登録後画面
#
sub Thanks {

	# テンポラリファイル名と引用した記事のId
	local($TmpFile, $Id) = @_;

	# 登録ファイルのURL
	local($TitleFileURL) = &GetURL($BOARD, $TITLE_FILE_NAME);

	# 新たに記事を生成し、フォローされた記事にその旨書き込む。
	&MakeNewArticle($TmpFile, $Id);

	# 表示画面の作成
	&MsgHeader("$THANKS_MSG");

	print("<p>$H_THANKSMSG</p>");
	print("<form action=\"$TitleFileURL\">\n");
	print("<input type=\"submit\" value=\"$H_BACK\">\n");
	print("</form>\n");

	&MsgFooter;
}


###
## 新たに投稿された記事の生成
#
sub MakeNewArticle {

	# テンポラリファイル名、引用した記事のId
	local($TmpFile, $Id) = @_;

	# Board名称の取得
	local($BoardName) = &GetBoardInfo($BOARD);

	# 記事番号を収めるファイル
	local($ArticleNumFile) = &GetPath($BOARD, $ARTICLE_NUM_FILE_NAME);

	# 新規の記事番号とファイル名
	local($ArticleId, $ArticleFile);

	# サブジェクト、入力日、名前
	local($Icon, $Subject, $InputDate, $Name, $Title);

	# テンポラリファイルからSubject等を取り出す
	($Icon, $Subject, $InputDate, $Name) = &GetHeader($TmpFile);

	# ロックをかける
	&lock;

	# 記事番号を取得
	$ArticleId = &GetandAddArticleId($ArticleNumFile);

	# 正規のファイル名を取得
	$ArticleFile = &GetArticleFileName($ArticleId, $BOARD);

	# 正規のファイルにヘッダ部分を書き込む
	open(ART, ">$ArticleFile") || &MyFatal(1, $ArticleFile);

	# 記事ヘッダの作成
	printf(ART "<title>[$BoardName: %d] $Subject</title>\n", $ArticleId);
	print(ART "<body bgcolor=\"$BG_COLOR\" TEXT=\"$TEXT_COLOR\" LINK=\"$LINK_COLOR\" ALINK=\"$ALINK_COLOR\" VLINK=\"$VLINK_COLOR\">\n");
	print(ART "<a href=\"$TITLE_FILE_NAME\">$H_BACK</a> // ");
	printf(ART "<a href=\"%s\">$H_NEXTARTICLE</a> // ",
		&GetArticleFileName(($ArticleId + 1), ''));
	print(ART "<a href=\"$PROGRAM_FROM_BOARD/$BOARD?c=f&id=$ArticleId\">$H_REPLYTHISARTICLE</a> // ");
	print(ART "<a href=\"$PROGRAM_FROM_BOARD/$BOARD?c=q&id=$ArticleId\">$H_REPLYTHISARTICLEQUOTE</a> // ");
	print(ART "<a href=\"$PROGRAM_FROM_BOARD/$BOARD?c=t&id=$ArticleId\">$H_READREPLYALL</a>\n");
	print(ART "<hr>\n");

	# 記事ヘッダの始まり
	print(ART "$COM_HEADER_BEGIN\n");

	# ボディの先頭にボード名と記事番号、題を入れる
	printf(ART "<strong>$H_SUBJECT</strong> [$BoardName: %d] $Icon$Subject<br>\n", $ArticleId);

	# テンポラリファイルからの記事のコピー
	open(TMP, "$TmpFile") || &MyFatal(1, $TmpFile);

	# Subject行は挿入済みなので1行飛ばす。
	$Dust = <TMP>;

	while(<TMP>) {
		print(ART $_)
	}
	close(TMP);

	# テンポラリファイルの削除
	unlink("$TmpFile");

	# 記事フッタの作成
	print(ART "$H_FOLLOW\n<ol>\n");
	close(ART);

	if ($Id != 0) {
		# フォローの場合

		# フォローされた記事にフォローされたことを書き込む。
		# フォローした記事ファイル名を直接渡さないのは、
		# 相対の起点が異なるため。
		&ArticleWasFollowed($Id, $ArticleId, $Icon, $Subject, $Name);

		# タイトルファイルに投稿された記事を追加
		&AddTitleFollow($ArticleId, $Id, $Name, $Icon, $Subject, $InputDate);
	} else {
		# フォローでなく、新規の場合

		# タイトルファイルに投稿された記事を追加
		&AddTitleNormal($ArticleId, $Name, $Icon, $Subject, $InputDate);
	}

	# allファイルに投稿された記事を追加
	&AddAllFile($ArticleId, $Name, $Icon, $Subject, $InputDate);

	# ロックを外す。
	&unlock;

}


###
## 「題」用の文字列からTitleを作る(<img...>を取り除く)
#
sub MakeTitleFromSubject {

	# 題
	local($Subject) = @_;

	$Subject =~ /^<img src=\"[^>]*> (.*)$/;
	return($1);

}


###
## 記事番号を取ってくる(番号は1増える)。
#
sub GetandAddArticleId {

	# ファイル名を取得
	local($ArticleNumFile) = @_;

	# 記事番号
	local($ArticleId) = 0;

	# 記事番号をファイルから読み込む。読めなかったら0のまま……のはず。
	open(AID, "$ArticleNumFile");
	while(<AID>) {
		chop;
		$ArticleId = $_;
	}
	close(AID);

	# 1増やして書き込む。
	open(AID, ">$ArticleNumFile") || &MyFatal(1, $ArticleNumFile);
	print(AID $ArticleId + 1, "\n");
	close(AID);

	# 新しい記事番号を返す。
	return($ArticleId + 1);
}


###
## フォローされた記事のフッタにフォローされたことを書き込む。
#
sub ArticleWasFollowed {

	# フォローされた記事のId、ボードの名称、
	# フォローした記事のId、サブジェクト、名前
	local($Id, $FollowArticleId, $Ficon, $Fsubject, $Fname) = @_;

	# フォローされた記事ファイル
	local($ArticleFile) = &GetArticleFileName($Id, $BOARD);

	# フォローした記事ファイル
	local($FollowArticleFile) = &GetArticleFileName($FollowArticleId, '');

	# 元ファイルから反応メールの宛先等を取り出す
	local($Icon, $Subject, $Date, $Name, @Fmail)
		= &GetHeader($ArticleFile);

	# 必要ならメールを送る。
	&FollowMail($Name, $Date, $Subject, $Id, $Fname, $Fsubject,
			$FollowArticleId, @Fmail)
		if (($SYS_FOLLOWMAIL) && (@Fmail[0] ne ""));

	# 後ろにフォロー情報を追加
	open(FART, ">>$ArticleFile") || &MyFatal(1, $ArticleFile);
	printf(FART "<li>$Ficon<a href=\"$FollowArticleFile\">$Fsubject</a> $H_REPLYNOTE\n", $Fname);
	close(FART);
}


###
## タイトルリストに書き込む(新規)
#
sub AddTitleNormal {

	# 記事Id、名前、アイコン、題、日付
	local($Id, $Name, $Icon, $Subject, $InputDate) = @_;

	# 登録ファイル
	local($File) = &GetPath($BOARD, $TITLE_FILE_NAME);

	# 追加するファイルの名前
	local($ArticleFile) = &GetArticleFileName($Id, '');

	# TmpFile
	local($TmpFile) = &GetPath($BOARD, $TTMP_FILE_NAME);

	# タイトルファイルに追加
	open(TTMP, ">$TmpFile") || &MyFatal(1, $TmpFile);
	open(TITLE, "<$File") || &MyFatal(1, $File);

	while(<TITLE>) {

		# コード変換
		&jcode'convert(*_, 'euc');

		# 上に追加指定で、タイトルリスト開始なら追加
		printf(TTMP "<li><strong>$Id .</strong> $Icon<a href=\"%s\">$Subject</a> [$Name] $InputDate\n\n", $ArticleFile)
		    if ((! $SYS_BOTTOMTITLE) && (/$COM_TITLE_BEGIN/));

		# 下に追加指定で、タイトルリスト終了なら追加
		printf(TTMP "<li><strong>$Id .</strong> $Icon<a href=\"%s\">$Subject</a> [$Name] $InputDate\n\n", $ArticleFile)
		    if (($SYS_BOTTOMTITLE) && (/$COM_TITLE_END/));

		# そのまま書き出す。
		print(TTMP $_);
	}

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
## タイトルリストに書き込む(フォロー)
#
sub AddTitleFollow {

	# 記事Id、フォロー記事Id、名前、アイコン、題、日付
	local($Id, $Fid, $Name, $Icon, $Subject, $InputDate) = @_;

	# 登録ファイル
	local($File) = &GetPath($BOARD, $TITLE_FILE_NAME);

	# 追加するファイルの名前
	local($ArticleFile) = &GetArticleFileName($Id, '');

	# Followed Article File Name
	local($FollowedArticleFile) = &GetArticleFileName($Fid, '');

	# TmpFile
	local($TmpFile) = &GetPath($BOARD, $TTMP_FILE_NAME);

	# Follow Flag
	local($AddFlag, $Nest, $NextLine) = (0, 0, ''); 

	# タイトルリストのフラグ
	local($TitleListFlag) = 0;

	# タイトルファイルに追加
	open(TTMP, ">$TmpFile") || &MyFatal(1, $TmpFile);
	open(TITLE, "<$File") || &MyFatal(1, $File);

	while(<TITLE>) {

		# コード変換
		&jcode'convert(*_, 'euc');

		# タイトルリスト終了?
		if (/$COM_TITLE_END/) {
			$TitleListFlag = 0;

			# 見つかんなかったということは、
			# エージングされてるらしいので、単に追加。
			# これも$SYS_TITLEBOTTOMに従ったほうがいいのかなぁ。
			printf(TTMP "<li><strong>$Id .</strong> $Icon<a href=\"%s\">$Subject</a> [$Name] $InputDate\n\n", $ArticleFile) if (! $AddFlag);
		}

		# そのまま書き出す。
		print(TTMP $_);

		# タイトルリスト開始?
		$TitleListFlag = 1 if (/$COM_TITLE_BEGIN/);

		# タイトルリスト中、お目当ての記事が来たら、
		if (($TitleListFlag == 1) && (/$FollowedArticleFile/)) {

			# 1行空読み
			&MyFatal(3, '') unless ($_ = <TITLE>);

			if (/^<ul>/) {
				$Nest = 1;
				do {
					print(TTMP $_);
					$_ = <TITLE>;
					$Nest++ if (/^<ul>/);
					$Nest-- if (/^<\/ul>/);
				} until ($Nest == 0);

				printf(TTMP "<li><strong>$Id .</strong> $Icon<a href=\"%s\">$Subject</a> [$Name] $InputDate\n\n", $ArticleFile);
				printf(TTMP $_);

			} else {

				print(TTMP "<ul>\n");
				printf(TTMP "<li><strong>$Id .</strong> $Icon<a href=\"%s\">$Subject</a> [$Name] $InputDate\n\n", $ArticleFile);
				print(TTMP "</ul>\n");

			}

			$AddFlag = "True";
		}
	}


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
## allリストに書き込む
#
sub AddAllFile {

	# 記事Id、名前、アイコン、題、日付
	local($Id, $Name, $Icon, $Subject, $InputDate) = @_;

	# 登録ファイル
	local($File) = &GetPath($BOARD, $ALL_FILE_NAME);

	# 追加するファイルの名前
	local($ArticleFile) = &GetArticleFileName($Id, '');

	# Add to 'All' file
	open(ALL, ">>$File") || &MyFatal(1, $File);
	printf(ALL "<li><strong>$Id .</strong> $Icon<a href=\"%s\">$Subject</a> [$Name] $InputDate\n\n", $ArticleFile);
	close(TITLE);
}


#/////////////////////////////////////////////////////////////////////
# 日付順ソート関連


###
## 日付順にソート。新しいものが上。
#
sub SortArticle {

	# タイプ(all / new)
	local($Type) = @_;

	# file
	local($File) = &GetPath($BOARD,
			(($Type eq 'new')
				? $TITLE_FILE_NAME
				: $ALL_FILE_NAME));
	local(@lines);

	open(ALL, "<$File") || &MyFatal(1, $File);
	while(<ALL>) {

		# コード変換
		&jcode'convert(*_, 'euc');

		(/^<li>/) && push(@lines, $_);
	}
	close(ALL);

	# 表示画面の作成
	&MsgHeader($SORT_MSG, $BOARD);
	print("<ol>\n");
	foreach (reverse sort MyArticleSort @lines) {
		print("$_");
	}
	print("</ol>\n");
	&MsgFooter;
}


###
## ユーザ定義ソート関数
#
sub MyArticleSort {
	local($MyA, $MyB) = ($a, $b);
	$MyA =~ s/<li><strong>([0-9]*) .*$/$1/;
	$MyB =~ s/<li><strong>([0-9]*) .*$/$1/;
	return($MyA <=> $MyB);
}


#/////////////////////////////////////////////////////////////////////
# 新着記事表示関連


###
## 新しい記事からn個を表示。
#
sub NewArticle {

	# 表示する個数を取得
	local($Num) = @_;

	# 記事番号を収めるファイル
	local($ArticleNumFile) = &GetPath($BOARD, $ARTICLE_NUM_FILE_NAME);

	# 最新記事番号を取得
	local($ArticleToId) = &GetArticleId($ArticleNumFile);

	# 記事数が足りない場合の調整
	$Num = $ArticleToId if ($ArticleToId < $Num);

	# 取ってくる最初の記事番号を取得
	local($ArticleFromId) = $ArticleToId - $Num + 1;
	local($i, $File);

	# 表示画面の作成
	&MsgHeader("$NEWARTICLE_MSG: $Num ($ArticleToId - $ArticleFromId)", $BOARD);

	print("<p>$H_ARTICLES: $Num </p>");

	# nameへのリンクを表示
	print("<p> //\n");
	for ($i = $ArticleToId; ($i >= $ArticleFromId); $i--) {
		print("<a href=\"\#$i\">$i</a> //\n");
	}
	print("</p><p>$H_JUMPID</p>\n");

	for ($i = $ArticleToId; ($i >= $ArticleFromId); $i--) {
		print("<a name=\"$i\">　</a><br>\n");
		&ViewOriginalArticle($i);
 		print("<hr>\n");
	}

	&MsgFooter;
}


###
## 記事番号を取ってくる(番号は増えない)。
#
sub GetArticleId {

	# ファイル名を取得
	local($ArticleNumFile) = @_;

	# 記事番号
	local($ArticleId);

	open(AID, "$ArticleNumFile") || &MyFatal(1, $ArticleNumFile);
	while(<AID>) {
		chop;
		$ArticleId = $_;
	}
	close(AID);

	# 記事番号を返す。
	return($ArticleId);
}


#/////////////////////////////////////////////////////////////////////
# フォローまとめ読み関連


###
## フォロー記事を全て表示。
#
sub ThreadArticle {

	# 元記事のIdを取得
	local($Id) = @_;

	# 表示画面の作成
	&MsgHeader($THREADARTICLE_MSG, $BOARD);

	# メイン関数の呼び出し(記事概要)
	print("<ul>\n");
	&ThreadArticleMain('subject only', $Id);
	print("</ul>\n");

	# メイン関数の呼び出し(記事)
	&ThreadArticleMain('', $Id);

	&MsgFooter;
}


###
## 再帰的にその記事のフォローを表示する。
#
sub ThreadArticleMain {

	# Idの取得
	local($SubjectOnly, $Id) = @_;

	# フォロー記事のIdの取得
	local(@FollowIdList) = &GetFollowIdList($Id);

	# 記事概要か、記事そのものか。
	if ($SubjectOnly) {

		# 記事概要の表示
		&PrintAbstract($Id);

	} else {

		# 元記事の表示
		print("<a name=\"$Id\">　</a><br>\n");
		print("<hr>\n");
		&ViewOriginalArticle($Id);

	}

	# フォロー記事の表示
	foreach (@FollowIdList) {

		# 記事概要なら箇条書
		print("<ul>\n") if ($SubjectOnly);

		# 再帰
		&ThreadArticleMain($SubjectOnly, $_, $BOARD);

		# 記事概要なら箇条書閉じ
		print("</ul>\n") if ($SubjectOnly);

	}
}


###
## フォロー記事のIdの配列を取り出す。
#
sub GetFollowIdList {

	# Id
	local($Id) = @_;

	# 元ファイル
	local($File) = &GetArticleFileName($Id, $BOARD);

	# フォロー部分を判断するフラグ
	local($QuoteFlag) = 0;

	# リスト
	local(@Result) = ();

	open(TMP, "<$File") || &MyFatal(1, $File);
	while(<TMP>) {

		# コード変換
		&jcode'convert(*_, 'euc');

		# フォロー部分開始の判定
		$QuoteFlag = 1 if (/$COM_ARTICLE_END/);

		# フォローIdの取得
		($QuoteFlag == 1) || next;
		push(@Result, $1)
			if (/<a href=\"$ARTICLE_PREFIX\.([0-9]*)\.html\">/);
	}
	close(TMP);

	return(@Result);
}


###
## 記事の概要の表示
#
sub PrintAbstract {

	# Id
	local($Id) = @_;

	# 引用するファイル
	local($File) = &GetArticleFileName($Id, $BOARD);

	# 題、日付、名前
	local($Icon, $Subject, $InputDate, $Name);

	# 記事ファイルからSubject等を取り出す
	($Icon, $Subject, $InputDate, $Name) = &GetHeader("$File");

	printf("<li><strong>$Id .</strong> %s<a href=\"\#$Id\">$Subject</a> [$Name] $InputDate\n", $Icon);

}


#/////////////////////////////////////////////////////////////////////
# 記事検索関連


###
## 記事の検索(表示画面作成)
#
sub SearchArticle {

	# all/new、キーワード
	local($Type, $Key) = @_;

	# 表示画面の作成
	&MsgHeader($SEARCHARTICLE_MSG, $BOARD);

	# お約束
	print("<form action=\"$PROGRAM_FROM_BOARD/$BOARD\" method =\"GET\">\n");
	print("<input name=\"c\" type=\"hidden\" value=\"s\">\n");
	print("<input name=\"type\" type=\"hidden\" value=\"$Type\">\n");

	# キーワード入力部
	print("<p>$H_INPUTKEYWORD");
	print("<input type=\"submit\" value=\"$H_PUSHHERE\"></p>\n");
	print("<p>$H_KEYWORD:\n");
	print("<input name=\"key\" size=\"$KEYWORD_LENGTH\"></p>\n");
	print("<hr>\n");

	# キーワードが空でなければ、そのキーワードを含む記事のリストを表示
	&SearchArticleList($Type, $Key) unless ($Key eq "");

	&MsgFooter;
}


###
## 記事の検索(検索結果の表示)
#
sub SearchArticleList {

	# all/new、キーワード
	local($Type, $Key) = @_;

	# 検索対象ファイル
	local($File) = &GetPath($BOARD,
			(($Type eq 'new')
				? $TITLE_FILE_NAME
				: $ALL_FILE_NAME));
	local($Title, $ArticleFile, $HitFlag, $Line);
	$HitFlag = 0;

	# リスト開く
	print("<dl>\n");

	# ファイルを開く
	open(TITLE, "<$File") || &MyFatal(1, $File);
	while(<TITLE>) {

		# コード変換
		&jcode'convert(*_, 'euc');

		$Title = $_;
		next unless (/^<li>.*href=\"([^\"]*)\"/);
		$ArticleFile = &GetPath($BOARD, $1);
		$Line = &SearchArticleKeyword($ArticleFile, $Key);
		if ($Line ne "") {
			$Title =~ s/^<li>//go;
			$Line =~ s/<[^>]*>//go;
			$Line =~ s/&/&amp;/go;
			$Line =~ s/\"/&quot;/go;
			print("<dt>$Title\n");
			print("<dd>$Line\n");
			$HitFlag = 1;
		}
	}
	close(TITLE);

	# ヒットしなかったら
	print("<dt>$H_NOTFOUND\n")
		unless ($HitFlag = 1);

	# リスト閉じる
	print("</dl>\n");
}


###
## 記事の検索(検索結果メイン)
#
sub SearchArticleKeyword {

	# ファイル名とキーワード
	local($File, $Key) = @_;

	# 検索する
	open(ARTICLE, "<$File") || &MyFatal(1, $File);
	while(<ARTICLE>) {

		# コード変換
		&jcode'convert(*_, 'euc');

		# TAGを取り除く
		s/<[^>]*>//go;

		# ヒット?
		(/$Key/) && return($_);
	}

	# ヒットせず
	return("");
}


#/////////////////////////////////////////////////////////////////////
# エイリアス関連


###
## エイリアスの登録と変更
#
sub AliasNew {

	# 表示画面の作成
	&MsgHeader("$ALIASNEW_MSG");

	# 新規登録/登録内容の変更
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

	# 削除
	print("<p>$H_ALIASDELETE</p>\n");
	print("<p>\n");
	print("<form action=\"$PROGRAM\" method =\"POST\">\n");
	print("<input name=\"c\" type=\"hidden\" value=\"ad\">\n");
	print("$H_ALIAS <input name=\"alias\" type=\"text\" size=\"$NAME_LENGTH\"><br>\n");
	print("<input type=\"submit\" value=\"$H_PUSHHERE\">\n");
	print("$H_ALIASDELETECOM\n");
	print("</form></p>\n");

	print("<hr>\n");

	# 参照
	print("<p>\n");
	print("<form action=\"$PROGRAM\" method =\"POST\">\n");
	print("<input name=\"c\" type=\"hidden\" value=\"as\">\n");
	print("<input type=\"submit\" value=\"$H_PUSHHERE\">\n");
	print("$H_ALIASREFERCOM\n");
	print("</form></p>\n");

	# お約束
	&MsgFooter;

}


###
## 登録/変更
#
sub AliasMod {

	# エイリアス、名前、メール、URL
	local($A, $N, $E, $U) = @_;

	# ホストがマッチしたか
	#	0 ... エイリアスがマッチしない
	#	1 ... エイリアスはマッチしたがホスト名がマッチしない
	#	2 ... マッチしてデータを変更した
	local($HitFlag) = 0;

	# 文字列チェック
	&AliasCheck($A, $N, $E, $U);

	# エイリアスの読み込み
	&CashAliasData($USER_ALIAS_FILE);

	# 1行ずつチェック
	foreach $Alias (sort keys(%Name)) {
		next unless ($A eq $Alias);

		# ホスト名が合ったら2、合わなきゃ1。
		$HitFlag = (($REMOTE_HOST eq $Host{$Alias}) ? 2 : 1);
	}

	# ホスト名が合わない!
	&MyFatal(6, '') if ($HitFlag == 1);

	# データの登録
	$Name{$Alias} = $N;
	$Email{$Alias} = $E;
	$Host{$Alias} = $REMOTE_HOST;
	$URL{$Alias} = $U;

	# エイリアスファイルに書き出し
	&WriteAliasData($USER_ALIAS_FILE);

	# 表示画面の作成
	&MsgHeader("$ALIASMOD_MSG");
	print("<p>$H_ALIAS <strong>$A</strong>:\n");
	if ($HitFlag == 2) {
		print("$H_ALIASCHANGED</p>\n");
	} else {
		print("$H_ALIASENTRIED</p>\n");
	}
	&MsgFooter;

}


###
## エイリアスチェック
#
sub AliasCheck {

	local($A, $N, $E, $U) = @_;

	# 空チェック
	&MyFatal(2, '') if ($A eq "")
		|| ($N eq "")
		|| ($E eq "");

	&CheckAlias($A);
	&CheckName($N);
	&CheckEmail($E);
	&CheckURL($U);

}


###
## 削除
#
sub AliasDel {

	# エイリアス
	local($A) = @_;

	# ホストがマッチしたか
	#	0 ... エイリアスがマッチしない
	#	1 ... エイリアスはマッチしたがホスト名がマッチしない
	#	2 ... マッチしてデータを変更した
	local($HitFlag) = 0;

	# エイリアスの読み込み
	&CashAliasData($USER_ALIAS_FILE);

	# 1行ずつチェック
	foreach $Alias (sort keys(%Name)) {
		next unless ($A eq $Alias);

		# ホスト名が合ったら2、合わなきゃ1。
		$HitFlag = (($REMOTE_HOST eq $Host{$Alias}) ? 2 : 1);
	}

	# ホスト名が合わない!
	&MyFatal(6, '') if ($HitFlag == 1);

	# エイリアスがない!
	&MyFatal(7, $A) if ($HitFlag == 0);

	# 名前を消す
	$Name{$A} = '';

	# エイリアスファイルに書き出し
	&WriteAliasData($USER_ALIAS_FILE);

	# 表示画面の作成
	&MsgHeader("$ALIASDEL_MSG");
	print("<p>$H_ALIAS <strong>$A</strong>: $H_ALIASDELETED</p>\n");
	&MsgFooter;

}


###
## 参照
#
sub AliasShow {

	# エイリアスの読み込み
	&CashAliasData($USER_ALIAS_FILE);
	local($Alias);

	# 表示画面の作成
	&MsgHeader("$ALIASSHOW_MSG");
	# あおり文
	print("<p>$H_AORI_ALIAS</p>\n");
	print("<p><a href=\"$PROGRAM?c=an\">$H_ALIASTITLE</a></p>\n");

	# リスト開く
	print("<dl>\n");

	# 1つずつ表示
	foreach $Alias (sort keys(%Name)) {
		print("<p>\n");
		print("<dt><strong>$Alias</strong>\n");
		print("<dd>$H_FROM $Name{$Alias}\n");
		print("<dd>$H_MAIL $Email{$Alias}\n");
		print("<dd>$H_HOST $Host{$Alias}\n");
		print("<dd>$H_URL $URL{$Alias}\n");
		print("</p>\n");
	}

	# リスト閉じる
	print("</dl>\n");

	&MsgFooter;

}


###
## エイリアスファイルを読み込んで連想配列に放り込む。
## CAUTION: %Name, %Email, %Host, %URLを壊します。
#
sub CashAliasData {

	# ファイル
	local($File) = @_;

	local($A, $N, $E, $H, $U);

	# 放り込む。
	open(ALIAS, "<$File") || &MyFatal(1, $File);
	while(<ALIAS>) {

		# コード変換
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
## エイリアスファイルにデータを書き出す。
## CAUTION: %Name, %Email, %Host, %URLを必要とします。
##          $Nameが体と書き込まない。
#
sub WriteAliasData {

	# ファイル
	local($File) = @_;
	local($Alias);

	# ロックをかける
	&lock;

	# 書き出す
	open(ALIAS, ">$File") || &MyFatal(1, $File);
	foreach $Alias (sort keys(%Name)) {
		($Name{$Alias}) && printf(ALIAS "%s\t%s\t%s\t%s\t%s\n",
			$Alias, $Name{$Alias}, $Email{$Alias},
			$Host{$Alias}, $URL{$Alias});
	}
	close(ALIAS);

	# ロックを外す。
	&unlock;

}


###
## ユーザエイリアスからユーザの名前、メール、URLを取ってくる。
#
sub GetUserInfo {

	# 検索するエイリアス名
	local($Alias) = @_;

	# エイリアス、名前、メール、ホスト、URL
	local($A, $N, $E, $H, $U);

	# ファイルを開く
	open(ALIAS, "<$USER_ALIAS_FILE")
		# ファイルがないらしいのでさようなら。
		|| return('', '', '');

	# 1つ1つチェック。
	while(<ALIAS>) {

		# コード変換
		&jcode'convert(*_, 'euc');

		chop;

		# 分割
		($A, $N, $E, $H, $U) = split(/\t/, $_);

		# マッチしなきゃ次へ。
		next unless ($A eq $Alias);

		# 配列にして返す
		return($N, $E, $U);
	}

	# ヒットせず
	return('', '', '');
}


###
## ボードエイリアスからボードエイリアス名を取ってくる。
#
sub GetBoardInfo {

	# エイリアス名
	local($Alias) = @_;

	# ボード名
	local($BoardName);

	open(ALIAS, "<$BOARD_ALIAS_FILE")
		|| &MyFatal(1, $BOARD_ALIAS_FILE);
	while(<ALIAS>) {

		# コード変換
		&jcode'convert(*_, 'euc');

		chop;
		# マッチしなきゃ次へ。
		next unless (/^$Alias\t(.*)$/);
		$BoardName = $1;
		return($BoardName);
	}

	# ヒットせず
	return('');
}


#/////////////////////////////////////////////////////////////////////
# その他共通関数


###
## 文字列チェック: エイリアス
#
sub CheckAlias {

	local($String) = @_;
	($String =~ (/^#/)) || &MyFatal(8, 'alias');
	(length($String) > 1) || &MyFatal(8, 'alias');

}


###
## 文字列チェック: 名前
#
sub CheckName {

	local($String) = @_;

}


###
## 文字列チェック: メール
#
sub CheckEmail {

	local($String) = @_;
	($String =~ (/@/)) || &MyFatal(8, 'E-Mail');

}


###
## 文字列チェック: URL
#
sub CheckURL {

	local($String) = @_;
	($String =~ (/^http:\/\/.*/)) || ($String =~ (/^http:\/\/$/))
		|| ($String eq "") || &MyFatal(8, 'URL');

}


###
## 記事のヘッダの表示
#
sub MsgHeader {

	# message and board
	local($Message, $Board) = @_;

	&cgi'header;
	print("<title>$Message</title>", "\n");
	if (! $Board) {
		print("<base href=\"$SCRIPT_URL\">\n");
	} else {
		print("<base href=\"$DIR_URL$Board/\">\n");
	}
	print("<body bgcolor=\"$BG_COLOR\" TEXT=\"$TEXT_COLOR\" LINK=\"$LINK_COLOR\" ALINK=\"$ALINK_COLOR\" VLINK=\"$VLINK_COLOR\">\n");
	print("<h1>$Message</h1>\n");
	print("<hr>\n");
}


###
## 記事のフッタの表示
#
sub MsgFooter {
	print("<hr>\n");
	print("<address>\n");
	print("$ADDRESS\n");
	print("</address>\n");
	print("</body>");
}


###
## ロック関係
#

# ロック
sub lock {

	# ロックファイルを開く
	open(LOCK, "$LOCK_FILE") || &MyFatal(1, $LOCK_FILE);

	# ロックをかける
	flock(LOCK, $LOCK_EX);
}

# アンロック
sub unlock {

	# ロック外す
	flock(LOCK, $LOCK_UN);

	# ロックファイルを閉じる
	close(LOCK);
}


###
## 元記事の表示
#
sub ViewOriginalArticle {

	# Id
	local($Id) = @_;

	# 引用するファイル
	local($QuoteFile) = &GetArticleFileName($Id, $BOARD);

	# 引用部分を判断するフラグ
	local($QuoteFlag) = 0;

	open(TMP, "<$QuoteFile") || &MyFatal(1, $QuoteFile);
	while(<TMP>) {

		# コード変換
		&jcode'convert(*_, 'euc');

		# 引用終了の判定
		$QuoteFlag = 0 if (/$COM_ARTICLE_END/);

		# 引用文字列の表示
		if ($QuoteFlag == 1) {
			print("$_");
		}

		# 引用開始の判定
		$QuoteFlag = 1 if ((/$COM_HEADER_BEGIN/) ||
					(/$COM_ARTICLE_BEGIN/));

	}
	close(TMP);

}


###
## 元記事の表示(ファイル)
#
sub ViewOriginalFile {

	# ファイル名
	local($File) = @_;

	# 引用部分を判断するフラグ
	# 0 ... before
	# 1 ... quote
	# 2 ... after
	local($QuoteFlag) = 0;

	open(TMP, "<$File") || &MyFatal(1, $File);
	while(<TMP>) {

		# コード変換
		&jcode'convert(*_, 'euc');

		# 引用終了の判定
		$QuoteFlag = 2 if (/$COM_ARTICLE_END/);

		# 引用文字列の表示
		print($_) if ($QuoteFlag == 1);

		# 引用開始の判定
		$QuoteFlag = 1 if (/$COM_ARTICLE_BEGIN/);

	}
	close(TMP);

	# cannot quote specified file.
	print($H_CANNOTQUOTE) if ($QuoteFlag == 0);
}


###
## 文字列中に<a href="$ARTICLE_PREFIX.??.html">があったら、
## BoardNameをえてから返す。
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
## 反応があったことをメールする。
#
sub FollowMail {

	# 宛先いろいろ
	local($Name, $Date, $Subject, $Id, $Fname, $Fsubject, $Fid, @To) = @_;

	local($BoardName) = &GetBoardInfo($BOARD);
	local($URL) = $DIR_URL . &GetURL($BOARD, &GetArticleFileName($Id, ''));
	local($FURL) = $DIR_URL . &GetURL($BOARD, &GetArticleFileName($Fid, ''));

	# Subject
	local($MailSubject) = "The article was followed.";

	# Message
	local($Message) = "$SYSTEM_NAMEからのお知らせです。\n\n$Dateに「$BoardName」に対して「$Name」さんが書いた、\n「$Subject」\n$URL\nに対して、\n「$Fname」さんから\n「$Fsubject」という題での反応がありました。\n\nお時間のある時に\n$FURL\nを御覧下さい。\n\nでは失礼します。";

	# メール送信
	&SendMail($MailSubject, $Message, @To);
}


###
## ボード名称とIdからファイルのパス名を作り出す。
#
sub GetArticleFileName {

	# IdとBoard
	local($Id, $Board) = @_;

	# Boardが空ならBoardディレクトリ内から相対、
	# 空でなければシステムから相対
	$Board
		? return("$Board/$ARTICLE_PREFIX.$Id.html")
		: return("$ARTICLE_PREFIX.$Id.html");
}


###
## ボード名称とファイル名から、そのファイルのパス名を作り出す。
#
sub GetPath {

	# BoardとFile
	local($Board, $File) = @_;

	# 返す
	return("$Board/$File");

}


###
## ボード名称とファイル名から、そのファイルのURLを作り出す。
#
sub GetURL {

	# BoardとFile
	local($Board, $File) = @_;

	# 返す
	return("$Board/$File");

}


###
## アイコン名から、アイコンのURLを取得
#
sub GetIconURL {

	# アイコン名
	local($Icon) = @_;

	local($FileName, $Title);
	local($TargetFile) = "";

	# 一つ一つ表示
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
## あるIdの記事からSubjectを取ってくる。
#
sub GetSubject {

	# IdとBoard
	local($Id, $Board) = @_;

	# Subjectを取り出すファイル
	local($ArticleFile) = &GetArticleFileName($Id, $Board);

	# 取り出したSubject
	local($Icon, $Subject) = ('', '');

	# 該当ファイルからSubject文字列を取り出す。
	open(TMP, "<$ArticleFile") || &MyFatal(1, $ArticleFile);
	while(<TMP>) {

		# コード変換
		&jcode'convert(*_, 'euc');

		if (/^<strong>$H_SUBJECT<\/strong> \[[^\]]*\] (<img src=[^>]*> )(.*)<br>$/) {
			$Icon = $1;
			$Subject = $2;
		} elsif (/^<strong>$H_SUBJECT<\/strong> \[[^\]]*\] (.*)<br>$/) {
			$Subject = $1;
		}
	}
	close(TMP);

	# 返す
	return($Icon, $Subject);
}


###
## ある記事からアイコン、題、日付、名前を取り出す。
#
sub GetHeader {

	# ファイル名
	local($File) = @_;
	# 題、日付、名前
	local($Icon, $Subject, $Date, $Name, @Fmail) = ('', '', '', '', ());

	# ファイルを開く。
	open(TMP, "<$File") || &MyFatal(1, $File);
	while(<TMP>) {

		# subjectを取り出す。
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

		# 日付を取り出す。
		if (/^<strong>$H_DATE<\/strong> (.*)<br>$/) {$Date = $1;}

		# 名前を取り出す。
		if (/^<strong>$H_FROM<\/strong> <a[^>]*>(.*)<\/a><br>$/) {
			$Name = $1;
		} elsif (/^<strong>$H_FROM<\/strong> (.*)<br>$/) {
			$Name = $1;
		}

		# 反応メールの宛先を取り出す。
		if (/^$COM_FMAIL_BEGIN$/) {
			while(<TMP>) {
				chop;
				last if (/^$COM_FMAIL_END$/);
				push(@Fmail, $_);
			}
		}
	}
	close(TMP);

	# 返す
	return($Icon, $Subject, $Date, $Name, @Fmail);
}


###
## あるファイルからTitleを取ってくる
#
sub GetSubjectFromFile {

	# ファイル
	local($File) = @_;

	# 取り出したSubject
	local($Title) = '';

	open(TMP, "<$File") || &MyFatal(1, $File);
	while(<TMP>) {

		# コード変換
		&jcode'convert(*_, 'euc');

		if (/^<title>(.*)<\/title>$/i) {
			$Title = $1;
		}
	}
	close(TMP);

	# 返す。
	return($Title);

}


###
## メール送信
#
sub SendMail {

	# subject、メールのファイル名、宛先のリスト
	local($Subject, $Message, @To) = @_;

	# メール用ファイルを開く
	open(MAIL, "| $MAIL2") || &MyFatal(9, '');

	# Toヘッダ
	foreach (@To) {

		# コード変換
		&jcode'convert(*_, 'jis');

		print(MAIL "To: $_\n");
	}

	# Fromヘッダ
	# Errors-Toヘッダ
	$_ = $MAINT;
	&jcode'convert(*_, 'jis');
	print(MAIL "From: $_\n");
	print(MAIL "Errors-To: $_\n");

	# Subjectヘッダ
	$_ = $Subject;
	&jcode'convert(*_, 'jis');
	print(MAIL "Subject: $_\n\n");

	# 本文
	$_ = $Message;
	&jcode'convert(*_, 'jis');
	print(MAIL "$_\n");

	# 送信する
	close(MAIL);

}


###
## http connectionを張ってリソースを取ってきて、ローカルのファイルに落す。
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
	print(LOCAL $_);
    }
    
    close(LOCAL);
    return(1);
}


###
## エラー表示
#
sub MyFatal {

	# エラー番号とエラー情報の取得
	local($MyFatalNo, $MyFatalInfo) = @_;
	#
	# 1 ... File関連
	# 2 ... 投稿の際の、必須項目の欠如
	# 3 ... タイトルリストファイルのフォーマットがおかしい
	# 4 ... タイトルにhtmlタグが入っている
	# 5 ... プログラムの制御がおかしい
	# 6 ... エイリアスかホストが一致せず、エイリアスの変更ができない
	# 7 ... エイリアスが登録されていない。
	# 8 ... エイリアスに登録する文字列が正しくない。
	# 9 ... メールが送れなかった
	# 10 ... cannot connect to specified URL.

	&MsgHeader("$ERROR_MSG");

	if ($MyFatalNo == 1) {
		print("<p>File: $MyFatalInfoが存在しない、\n");
		print("あるいはpermissionの設定が間違っています。\n");
		print("お手数ですが、<a href=\"mailto:$MAINT\">$MAINT</a>まで\n");
		print("上記ファイル名をお知らせ下さい。</p>\n");
	} elsif ($MyFatalNo == 2) {
		print("<p>入力されていない項目があります。\n");
		print("戻ってもう一度。</p>\n");
	} elsif ($MyFatalNo == 3) {
		print("<p>Title File is illegal.\n");
		print("お手数ですが、<a href=\"mailto:$MAINT\">$MAINT</a>\n");
		print("までお知らせ下さい。</p>\n");
	} elsif ($MyFatalNo == 4) {
		print("<p>ごめんなさい、題中にHTMLタグを入れることは\n");
		print("禁じられています。戻ってもう一度。</a>\n");
	} elsif ($MyFatalNo == 5) {
		print("<p>関数$MyFatalInfoにおいて、ありえない位置に\n");
		print("プログラムの制御が移動しました。");
		print("このエラーが生じた状況を");
		print("<a href=\"mailto:$MAINT\">$MAINT</a>まで");
		print("お知らせ下さい。</p>\n");
	} elsif ($MyFatalNo == 6) {
		print("<p>登録されているエイリアスのものと、\n");
		print("ホスト名が一致しません。\n");
		print("戻ってもう一度。</p>\n");
	} elsif ($MyFatalNo == 7) {
		print("<p>$MyFatalInfoというエイリアスは\n");
		print("登録されていません。\n");
		print("戻ってもう一度。</p>\n");
	} elsif ($MyFatalNo == 8) {
		print("<p>$MyFatalInfoがおかしくありませんか?\n");
		print("戻ってもう一度。</p>\n");
	} elsif ($MyFatalNo == 9) {
		print("<p>メールが送信できませんでした。\n");
		print("このエラーが生じた状況を");
		print("<a href=\"mailto:$MAINT\">$MAINT</a>まで");
		print("お知らせ下さい。</p>\n");
	} elsif ($MyFatalNo == 10) {
		print("<p>Cannot Connect to $URL.\n");
		print("Try later.</p>\n");
	} else {
		print("<p>エラー番号不定: お手数ですが、");
		print("このエラーが生じた状況を");
		print("<a href=\"mailto:$MAINT\">$MAINT</a>まで");
		print("お知らせ下さい。</p>\n");
	}

	&MsgFooter;
	exit 0;
}
