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
#	×	SubjectをRe:にする
#	×	In-Reply-To:をつける
#	×	「〜にフォローされています」をつける。
#	×	user alias
#	×	board-name alias
#	×	indent
#	×	indentの並べ替え
#	×	Error関数
#	×	タイトルリストのフォーマット
#	×	「上の記事に反応する」なんか変。
#	×	HTML or Plain Text
#	×	^Mを取り除く
#	×	最新の記事n個!
#	×	まとめ読み(thread)
#	×	指定した日記を引用する。
#	×	指定した日記へのReferenceをつける
#	×	部分日付ソート
#	×	記事中に'を入れられるようにする
#	×	記事検索機能
#	×	まとめ読みの時、threadをわかりやすくする工夫を
#	×	安全なタグのみ投稿を許す(→あみさんのtag_secure.plをinclude)
#	×	aliasの登録機能
#	×	フォローがついた際の通知機能
#		メールのFromは$MAINTの方が良い
#		Preview画面で相対リンクが外れる
#		「上へ」「下へ」のリンク機能の追加(次/前は廃止?)
#		中身はEUC、ファイルはJISで
#		Subjectの先頭にIconをつけたい
#		Boardを自由に選択する
#		他人でも通知をもらいたい
#		新しい記事n個にマークをつける(aging機能との兼ね合いでつらい)
#		記事のキャンセル機能(aging機能との兼ね合いでつらい)


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
#	ファイル引用フォロー:	c=q/f&file={filename}
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
	local($File) = $cgi'TAGS{'file'};
	local($Num) = $cgi'TAGS{'num'};
	local($Type) = $cgi'TAGS{'type'};
	local($Key) = $cgi'TAGS{'key'};
	local($Alias) = $cgi'TAGS{'alias'};
	local($Name) = $cgi'TAGS{'name'};
	local($Email) = $cgi'TAGS{'email'};
	local($URL) = $cgi'TAGS{'url'};

	# コマンドタイプによる分岐
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

	# 選択されたBoardの取得
	local($Board) = substr($ENV{'PATH_INFO'}, $[ + 1);
	# Board名称の取得
	local($BoardName) = &GetBoardInfo($Board);

	# 表示画面の作成
	&MsgHeader($ENTRY_MSG);

	# フォローの場合
	if ($Id != 0) {
		&ViewOriginalArticle($Id, $Board);
		print("<hr>\n");
		print("<h2>上の記事に反応する</h2>");
	}

	# お約束
	print("<form action=\"$PROGRAM\" method =\"POST\">\n");
	print("<input name=\"c\" type=\"hidden\" value=\"p\">\n");
	print("<input name=\"board\" type=\"hidden\" value=\"$Board\">\n");

	# 引用Id; 引用でないなら0。
	print("<input name=\"id\" type=\"hidden\" value=\"$Id\">\n");

	# あおり文、TextType、Board名
	&EntryHeader($BoardName);

	# Subject(フォローなら自動的に文字列を入れる)
	printf("%s <input name=\"subject\" type=\"text\" value=\"%s\" size=\"%s\"><br>\n",
		$H_SUBJECT,
		(($Id !=0 ) ? &GetReplySubject($Id, $Board) : ""),
		$SUBJECT_LENGTH);

	# 本文(引用ありなら元記事を挿入)
	print("<textarea name=\"article\" rows=\"$TEXT_ROWS\" cols=\"$TEXT_COLS\">\n");
	&QuoteOriginalArticle($Id, $Board)
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
## 書き込み画面(ファイルから引用)
#
sub FileEntry {

	# 引用あり/なしと、引用するファイル(kb.cgiから相対)
	local($QuoteFlag, $File) = @_;

	# 選択されたBoardの取得
	local($Board) = substr($ENV{'PATH_INFO'}, $[ + 1);
	# Board名称の取得
	local($BoardName) = &GetBoardInfo($Board);

	# 表示画面の作成
	&MsgHeader($ENTRY_MSG);

	# 引用ファイルの表示
	&ViewOriginalFile($File);
	print("<hr>\n");
	print("<h2>上の記事に反応する</h2>");

	# お約束
	print("<form action=\"$PROGRAM\" method =\"POST\">\n");
	print("<input name=\"c\" type=\"hidden\" value=\"p\">\n");
	print("<input name=\"board\" type=\"hidden\" value=\"$Board\">\n");

	# 引用Id; 正規の引用でないので0。
	print("<input name=\"id\" type=\"hidden\" value=\"0\">\n");

	# 引用ファイル
	print("<input name=\"file\" type=\"hidden\" value=\"$File\">\n");

	# あおり文、TextType、Board名
	&EntryHeader($BoardName);

	# Subject
	printf("%s <input name=\"subject\" type=\"text\" value=\"%s\" size=\"%s\"><br>\n",
		$H_SUBJECT, &GetReplySubjectFromFile($File), $SUBJECT_LENGTH);

	# 本文(引用ありなら元記事を挿入)
	print("<textarea name=\"article\" rows=\"$TEXT_ROWS\" cols=\"$TEXT_COLS\">\n");
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

	# ボード名
	local($Board) = @_;

	# あおり文
	print("<p>$H_AORI</p>\n");

	# TextType
	print("$H_TEXTTYPE\n");
	print("<SELECT NAME=\"texttype\">\n");
	print("<OPTION SELECTED>$H_PRE\n");
	print("<OPTION>$H_HTML\n");
	print("</SELECT><BR>\n");

	# Board名; 本当は自由に選択できるようにしたい。
	print("$H_BOARD $Board<br>\n");

}


###
## 書き込み画面のうち、名前、e-mail addr.、URL入力部を表示。
#
sub EntryUserInformation {

	# 名前とメールアドレス、URL。
	print("$H_FROM <input name=\"name\" type=\"text\" size=\"$NAME_LENGTH\"><br>\n");
	print("$H_MAIL <input name=\"mail\" type=\"text\" size=\"$MAIL_LENGTH\"><br>\n");
	print("$H_URL <input name=\"url\" type=\"text\" value=\"http://\" size=\"$URL_LENGTH\"><br>\n");
	print("$H_FMAIL <input name=\"fmail\" type=\"checkbox\" value=\"on\"><br>\n");

	print("<p><a href=\"$PROGRAM?c=as\">ここ</a>に登録されている方は、「$H_FROM」に「#...」と書くと、自動的に補完されます。<a href=\"$PROGRAM?c=an\">登録はこちら</a>。</p>\n");

}


###
## 書き込み画面のうち、ボタンを表示。
#
sub EntrySubmitButton {

	print("<p>入力できましたら、\n");
	print("<input type=\"submit\" value=\"ここ\">\n");
	print("を押して記事を確認しましょう(まだ投稿しません)。</p>\n");

}


###
## あるIdの記事からSubjectを取ってきて、先頭に「Re: 」を1つだけつけて返す。
#
sub GetReplySubject {

	# IdとBoard
	local($Id, $Board) = @_;

	# 取り出したSubject
	local($Subject) = '';

	# Subjectを取りだし、先頭に「Re: 」がくっついてたら取り除く。
	$_ = &GetSubject($Id, $Board);

	$Subject = (/^Re: (.*)/) ? $1 : $_;

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

	open(TMP, "$KC2IN $QuoteFile |") || &MyFatal(1, $QuoteFile);
	while(<TMP>) {

		# 引用終了の判定
		$QuoteFlag = 0 if (/^$COM_ARTICLE_END$/);

		# 引用文字列の表示
		if ($QuoteFlag == 1) {
			s/&/&amp;/go;
			s/\"//go;
			s/<//go;
			s/>//go;
			print($DEFAULT_QMARK, $_);
		}

		# 引用開始の判定
		$QuoteFlag = 1 if (/^$COM_ARTICLE_BEGIN$/);

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

	open(TMP, "$KC2IN $File |") || &MyFatal(1, $File);
	while(<TMP>) {

		# 引用終了の判定
		$QuoteFlag = 0 if (/^$COM_ARTICLE_END$/);

		# 引用文字列の表示
		if ($QuoteFlag == 1) {
			s/&/&amp;/go;
			s/\"//go;
			s/<//go;
			s/>//go;
			print($DEFAULT_QMARK, $_);
		}

		# 引用開始の判定
		$QuoteFlag = 1 if (/^$COM_ARTICLE_BEGIN$/);

	}
	close(TMP);

}


#/////////////////////////////////////////////////////////////////////
# プレビュー画面関連


###
## プレビュー画面
## (ここだけはcgi'を変数に落してない。汚い。数が多いので…… ^^;)
#
sub Preview {

	# Boardの取得
	local($Board) = $cgi'TAGS{'board'};

	# TextTypeの取得
	local($TextType) = $cgi'TAGS{'texttype'};

	# テンポラリファイルの作成
	local($TmpFile) = &MakeTemporaryFile($Board, $TextType);

	# 表示画面の作成
	&MsgHeader($PREVIEW_MSG);

	# お約束
	print("<form action=\"$PROGRAM/$Board\" method =\"GET\">\n");
	print("<input name=\"file\" type=\"hidden\" value=\"$TmpFile\">\n");
	print("<input name=\"c\" type=\"hidden\" value=\"x\">\n");
	printf("<input name=\"id\" type=\"hidden\" value=\"%d\">\n",
		$cgi'TAGS{'id'});

	# あおり文
	print("<p>以下の記事を確認したら、");
	print("<input type=\"submit\" value=\"ここ\">");
	print("を押して書き込んで下さい。</p>\n");

	# 確認する記事の表示
	open(TMP, "$TmpFile");
	while(<TMP>) {
		print($_);
	}

	# お約束
	print("</form>\n");

	&MsgFooter;

}


###
## 確認用テンポラリファイルを作成してファイル名を返す。
#
sub MakeTemporaryFile {

	# BoardとTextTypeの取得
	local($Board, $TextType) = @_;

	# Board名称の取得
	local($BoardName) = &GetBoardInfo($Board);

	# テンポラリファイル名の取得
	local($TmpFile) = &GetPath($Board, ".$ARTICLE_PREFIX.$$");

	# 日付を取り出す。
	local($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst)
		= localtime(time);
	local($InputDate)
		= sprintf("%d月%d日%02d時%02d分", $mon + 1, $mday, $hour, $min);
	# 本文と名前
	local($Text, $Name) = ($cgi'TAGS{'article'}, $cgi'TAGS{'name'});

	# ホスト名を取り出す。
	local($RemoteHost) = $ENV{ 'REMOTE_HOST' };

	# 引用ファイル、そのSubject
	local($ReplyArticleFile, $ReplyArticleSubject);

	# もし引用なら引用ファイル名を取得
	if ($cgi'TAGS{'id'} != 0) {
		$ReplyArticleFile = &GetArticleFileName($cgi'TAGS{'id'}, '');
		$ReplyArticleSubject = &GetSubject($cgi'TAGS{'id'}, $Board);
	} elsif ($cgi'TAGS{'file'} ne '') {
		$ReplyArticleFile = "../" . $cgi'TAGS{'file'};
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
	printf(TMP "<strong>$H_SUBJECT</strong> %s<br>\n", $cgi'TAGS{'subject'});

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
	print(TMP "<strong>$H_HOST</strong> $RemoteHost<br>\n");

	# 投稿日
	print(TMP "<strong>$H_DATE</strong> $InputDate<br>\n");

	# ▼反応(引用の場合)
	if ($cgi'TAGS{'id'} != 0) {
		printf(TMP "<strong>$H_REPLY</strong> [$BoardName: %d] <a href=\"$ReplyArticleFile\">$ReplyArticleSubject</a><br>\n", $cgi'TAGS{'id'});
	} elsif ($cgi'TAGS{'file'} ne '') {
		printf(TMP "<strong>$H_REPLY</strong> <a href=\"$ReplyArticleFile\">$ReplyArticleSubject</a><br>\n");
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
	print(TMP "<pre>\n") if ($TextType eq $H_PRE);

	# 記事
	$Text = &tag_secure'decode($Text);
	printf(TMP "%s\n", $Text);

	# TextType用後処理
	print(TMP "</pre>\n") if ($TextType eq $H_PRE);

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

	# 選択されたBoardの取得
	local($Board) = substr($ENV{'PATH_INFO'}, $[ + 1);

	# 登録ファイルのURL
	local($TitleFileURL) = &GetURL($Board, $TITLE_FILE_NAME);

	# 新たに記事を生成し、フォローされた記事にその旨書き込む。
	&MakeNewArticle($TmpFile, $Board, $Id);

	# 表示画面の作成
	&MsgHeader($THANKS_MSG);

	print("<p>書き込みの訂正、取消などはメールでお願いいたします。</p>");
	print("<form action=\"$TitleFileURL\">\n");
	print("<input type=\"submit\" value=\"リストを見る\">\n");
	print("</form>\n");

	&MsgFooter;
}


###
## 新たに投稿された記事の生成
#
sub MakeNewArticle {

	# テンポラリファイル名、Board、引用した記事のId
	local($TmpFile, $Board, $Id) = @_;

	# Board名称の取得
	local($BoardName) = &GetBoardInfo($Board);

	# 記事番号を収めるファイル
	local($ArticleNumFile) = &GetPath($Board, $ARTICLE_NUM_FILE_NAME);

	# 新規の記事番号とファイル名
	local($ArticleId, $ArticleFile);

	# サブジェクト、入力日、名前
	local($Subject, $InputDate, $Name);

	# テンポラリファイルからSubject等を取り出す
	open(TMP, "$TmpFile") || &MyFatal(1, $TmpFile);
	while(<TMP>) {

		# subjectを取り出す。
		if (/^<strong>$H_SUBJECT<\/strong> (.*)<br>$/) {$Subject = $1; }

		# 日付を取り出す。
		if (/^<strong>$H_DATE<\/strong> (.*)<br>$/) {$InputDate = $1; }

		# 名前を取り出す。
		if (/^<strong>$H_FROM<\/strong> <a[^>]*>(.*)<\/a><br>$/) {
			$Name = $1;
		} elsif (/^<strong>$H_FROM<\/strong> (.*)<br>$/) {
			$Name = $1;
		}

	}
	close(TMP);

	# ロックファイルを開く
	open(LOCK, "$LOCK_FILE") || &MyFatal(1, $LOCK_FILE);

	# ロックをかける
	&lock;

	# 記事番号を取得
	$ArticleId = &GetandAddArticleId($ArticleNumFile);

	# 正規のファイル名を取得
	$ArticleFile = &GetArticleFileName($ArticleId, $Board);

	# 正規のファイルにヘッダ部分を書き込む
	open(ART, ">$ArticleFile") || &MyFatal(1, $ArticleFile);

	# 記事ヘッダの作成
	printf(ART "<title>[$BoardName: %d] $Subject</title>\n", $ArticleId);
	print(ART "<body>\n");
	print(ART "<a href=\"$TITLE_FILE_NAME\">戻る</a> // ");
	printf(ART "<a href=\"%s\">前へ</a> // ",
		&GetArticleFileName(($ArticleId - 1), ''));
	printf(ART "<a href=\"%s\">次へ</a> // ",
		&GetArticleFileName(($ArticleId + 1), ''));
	print(ART "反応 ( <a href=\"$PROGRAM/$Board?c=q&id=$ArticleId\">引用有り</a> / ");
	print(ART "<a href=\"$PROGRAM/$Board?c=f&id=$ArticleId\">無し</a> ) // ");
	print(ART "<a href=\"$PROGRAM/$Board?c=t&id=$ArticleId\">まとめ読み</a>\n");
	print(ART "<hr>\n");

	# 記事ヘッダの始まり
	print(ART "$COM_HEADER_BEGIN\n");

	# ボディの先頭にボード名と記事番号、題を入れる
	printf(ART "<strong>$H_SUBJECT</strong> [$BoardName: %d] $Subject<br>\n", $ArticleId);

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
		&ArticleWasFollowed($Id, $Board, $ArticleId, $Subject, $Name);

		# タイトルファイルに投稿された記事を追加
		&AddTitleFollow($ArticleId, $Board, $Id, $Name, $Subject, $InputDate);
	} else {
		# フォローでなく、新規の場合

		# タイトルファイルに投稿された記事を追加
		&AddTitleNormal($ArticleId, $Board, $Name, $Subject, $InputDate);
	}

	# allファイルに投稿された記事を追加
	&AddAllFile($ArticleId, $Board, $Name, $Subject, $InputDate);

	# ロックを外す。
	&unlock;
	close(LOCK);

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
	local($Id, $Board, $FollowArticleId, $Fsubject, $Fname) = @_;

	# フォローされた記事ファイル
	local($ArticleFile) = &GetArticleFileName($Id, $Board);

	# フォローした記事ファイル
	local($FollowArticleFile) = &GetArticleFileName($FollowArticleId, '');

	# 反応メールのフラグ
	local(@Fmail) = ();

	# 元ファイルから反応メールの宛先を取り出す
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

	# 必要ならメールを送る。
	&FollowMail(&GetURL($Board, &GetArticleFileName($Id, '')),
		&GetURL($Board, &GetArticleFileName($FollowArticleId, '')),
		$Name, @Fmail) if (@Fmail[0] ne "");

	# 後ろにフォロー情報を追加
	open(FART, ">>$ArticleFile") || &MyFatal(1, $ArticleFile);
	print(FART "<li><a href=\"$FollowArticleFile\">$Fsubject</a> ← $Fname さん\n");
	close(FART);
}


###
## タイトルリストに書き込む(新規)
#
sub AddTitleNormal {

	# 記事Id、Board, 名前、題、日付
	local($Id, $Board, $Name, $Subject, $InputDate) = @_;

	# 登録ファイル
	local($File) = &GetPath($Board, $TITLE_FILE_NAME);

	# 追加するファイルの名前
	local($ArticleFile) = &GetArticleFileName($Id, '');

	# タイトルファイルに追加
	open(TITLE, ">>$File") || &MyFatal(1, $File);
	printf(TITLE "<li><strong>$Id .</strong> <a href=\"%s\">$Subject</a> [$Name] $InputDate\n\n", $ArticleFile);
	close(TITLE);
}


###
## タイトルリストに書き込む(フォロー)
#
sub AddTitleFollow {

	# 記事Id、Board, フォロー記事Id、名前、題、日付
	local($Id, $Board, $Fid, $Name, $Subject, $InputDate) = @_;

	# 登録ファイル
	local($File) = &GetPath($Board, $TITLE_FILE_NAME);

	# 追加するファイルの名前
	local($ArticleFile) = &GetArticleFileName($Id, '');

	# Followed Article File Name
	local($FollowedArticleFile) = &GetArticleFileName($Fid, '');

	# TmpFile
	local($TmpFile) = &GetPath($Board, $TTMP_FILE_NAME);

	# Follow Flag
	local($AddFlag, $Nest, $NextLine) = (0, 0, ''); 

	# タイトルファイルに追加
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
## allリストに書き込む
#
sub AddAllFile {

	# 記事Id、Board, 名前、題、日付
	local($Id, $Board, $Name, $Subject, $InputDate) = @_;

	# 登録ファイル
	local($File) = &GetPath($Board, $ALL_FILE_NAME);

	# 追加するファイルの名前
	local($ArticleFile) = &GetArticleFileName($Id, '');

	# Add to 'All' file
	open(ALL, ">>$File") || &MyFatal(1, $File);
	printf(ALL "<li><strong>$Id .</strong> <a href=\"%s\">$Subject</a> [$Name] $InputDate\n\n", $ArticleFile);
	close(TITLE);
}


###
## 反応があったことをメールする。
#
sub FollowMail {

	# 宛先
	local($URL, $FollowURL, $Name, @To) = @_;

	# Subject
	local($Subject) = "Your article was followed.";

	# Message
	local($Message) = "あなたがきのぼーずに書き込んだ記事、\n$URL\nに対して、$Nameさんから反応がありました。\nお時間のある時に\n$FollowURL\nを御覧下さい。\n\nでは。";

	# メール送信
	&SendMail($Subject, $Message, @To);
}


###
## ログファイルのロック関係
#

# ロック
sub lock {
	flock(LOCK, $LOCK_EX);
}

# アンロック
sub unlock {
	flock(LOCK, $LOCK_UN);
}


#/////////////////////////////////////////////////////////////////////
# 日付順ソート関連


###
## 日付順にソート。新しいものが上。
#
sub SortArticle {

	# タイプ(all / new)
	local($Type) = @_;

	# 選択されたBoardの取得
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

	# 表示画面の作成
	&MsgHeader($SORT_MSG);
	print("<ol>\n");
	foreach (reverse sort MyArticleSort @lines) {
		print $_;
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

	# 選択されたBoardの取得
	local($Board) = substr($ENV{'PATH_INFO'}, $[ + 1);

	# 記事番号を収めるファイル
	local($ArticleNumFile) = &GetPath($Board, $ARTICLE_NUM_FILE_NAME);

	# 最新記事番号を取得
	local($ArticleToId) = &GetArticleId($ArticleNumFile);

	# 記事数が足りない場合の調整
	$Num = $ArticleToId if ($ArticleToId < $Num);

	# 取ってくる最初の記事番号を取得
	local($ArticleFromId) = $ArticleToId - $Num + 1;
	local($i, $File);

	# 表示画面の作成
	&MsgHeader("$NEWARTICLE_MSG: $Num");

	print("<p>記事数: $Num ($ArticleToId 〜 $ArticleFromId)</p>");

	# nameへのリンクを表示
	print("<p> //\n");
	for ($i = $ArticleToId; ($i >= $ArticleFromId); $i--) {
		print("<a href=\"\#$i\">$i</a> //\n");
	}
	print("</p><p>\n");
	print("↑の数字をクリックすると、そのIDの記事に飛びます。\n");
	print("新しい記事ほど上の方にあります。\n");
	print("</p>\n");

	for ($i = $ArticleToId; ($i >= $ArticleFromId); $i--) {
		print("<a name=\"$i\">　</a><br>\n");
		print("<hr>\n");
		&ViewOriginalArticle($i, $Board);
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

	# 選択されたBoardの取得
	local($Board) = substr($ENV{'PATH_INFO'}, $[ + 1);

	# 表示画面の作成
	&MsgHeader($THREADARTICLE_MSG);

	# メイン関数の呼び出し(記事概要)
	print("<ul>\n");
	&ThreadArticleMain('subject only', $Id, $Board);
	print("</ul>\n");

	# メイン関数の呼び出し(記事)
	&ThreadArticleMain('', $Id, $Board);

	&MsgFooter;
}


###
## 再帰的にその記事のフォローを表示する。
#
sub ThreadArticleMain {

	# IdとBoardの取得
	local($SubjectOnly, $Id, $Board) = @_;

	# フォロー記事のIdの取得
	local(@FollowIdList) = &GetFollowIdList($Id, $Board);

	# 記事概要か、記事そのものか。
	if ($SubjectOnly) {

		# 記事概要の表示
		&PrintAbstract($Id, $Board);

	} else {

		# 元記事の表示
		print("<a name=\"$Id\">　</a><br>\n");
		print("<hr>\n");
		&ViewOriginalArticle($Id, $Board);

	}

	# フォロー記事の表示
	foreach (@FollowIdList) {

		# 記事概要なら箇条書
		print("<ul>\n") if ($SubjectOnly);

		# 再帰
		&ThreadArticleMain($SubjectOnly, $_, $Board);

		# 記事概要なら箇条書閉じ
		print("</ul>\n") if ($SubjectOnly);

	}
}


###
## フォロー記事のIdの配列を取り出す。
#
sub GetFollowIdList {

	# IdとBoard
	local($Id, $Board) = @_;

	# 元ファイル
	local($File) = &GetArticleFileName($Id, $Board);

	# フォロー部分を判断するフラグ
	local($FollowFlag) = 0;

	# リスト
	local(@Result) = ();

	open(TMP, "$KC2IN $File |") || &MyFatal(1, $File);
	while(<TMP>) {

		# フォロー部分開始の判定
		$QuoteFlag = 1 if (/^$COM_ARTICLE_END$/);

		# フォローIdの取得
		if (($QuoteFlag == 1) &&
		(/^<li><a href=\"$ARTICLE_PREFIX\.([^\.]*)\.html\">/)) {
			push(@Result, $1);
		}
	}
	close(TMP);

	return(@Result);
}


###
## 記事の概要の表示
#
sub PrintAbstract {

	# IdとBoard
	local($Id, $Board) = @_;

	# 引用するファイル
	local($File) = &GetArticleFileName($Id, $Board);

	# 題、日付、名前
	local($Subject, $InputDate, $Name);

	# 記事ファイルからSubject等を取り出す
	open(TMP, "$KC2IN $File |") || &MyFatal(1, $File);
	while(<TMP>) {

		# subjectを取り出す。
		if (/^<strong>$H_SUBJECT<\/strong> (.*)<br>$/) {$Subject = $1; }
		# 日付を取り出す。
		if (/^<strong>$H_DATE<\/strong> (.*)<br>$/) {$InputDate = $1; }
		# 名前を取り出す。
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
# 記事検索関連


###
## 記事の検索(表示画面作成)
#
sub SearchArticle {

	# all/new、キーワード
	local($Type, $Key) = @_;

	# 選択されたBoardの取得
	local($Board) = substr($ENV{'PATH_INFO'}, $[ + 1);

	# 表示画面の作成
	&MsgHeader($SEARCHARTICLE_MSG);

	# お約束
	print("<form action=\"$PROGRAM/$Board\" method =\"GET\">\n");
	print("<input name=\"c\" type=\"hidden\" value=\"s\">\n");
	print("<input name=\"type\" type=\"hidden\" value=\"$Type\">\n");

	# キーワード入力部
	print("<p>キーワードを入力したら、");
	print("<input type=\"submit\" value=\"ここ\">");
	print("を押して下さい。</p>\n");
	print("<p>検索するキーワード:\n");
	print("<input name=\"key\" size=\"$KEYWORD_LENGTH\"></p>\n");
	print("<hr>\n");

	# キーワードが空でなければ、そのキーワードを含む記事のリストを表示
	&SearchArticleList($Board, $Type, $Key) unless ($Key eq "");

	&MsgFooter;
}


###
## 記事の検索(検索結果の表示)
#
sub SearchArticleList {

	# ボード名、all/new、キーワード
	local($Board, $Type, $Key) = @_;

	# 検索対象ファイル
	local($File) = &GetPath($Board,
			(($Type eq 'new')
				? $TITLE_FILE_NAME
				: $ALL_FILE_NAME));
	local($Title, $ArticleFile, $HitFlag, $Line);
	$HitFlag = 0;

	# リスト開く
	print("<dl>\n");

	# ファイルを開く
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

	# ヒットしなかったら
	print("<dt>該当する記事は見つかりませんでした。\n")
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
	open(ARTICLE, "$KC2IN $File |") || &MyFatal(1, $File);
	while(<ARTICLE>) {
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
	&MsgHeader($ALIASNEW_MSG);

	# 新規登録/登録内容の変更
	print("<p>新規登録/登録内容の変更</p>\n");
	print("<p>\n");
	print("<form action=\"$PROGRAM\" method =\"POST\">\n");
	print("<input name=\"c\" type=\"hidden\" value=\"am\">\n");
	print("$H_ALIAS <input name=\"alias\" type=\"text\" value=\"#\" size=\"$NAME_LENGTH\"><br>\n");
	print("$H_FROM <input name=\"name\" type=\"text\" size=\"$NAME_LENGTH\"><br>\n");
	print("$H_MAIL <input name=\"email\" type=\"text\" size=\"$MAIL_LENGTH\"><br>\n");
	print("$H_URL <input name=\"url\" type=\"text\" value=\"http://\" size=\"$URL_LENGTH\"><br>\n");
	print("<input type=\"submit\" value=\"ここ\">を押すと、\n");
	print("エイリアスの新規登録/登録内容の変更が行なわれます。\n");
	print("ただし変更は、登録の際と同じマシンでなければできません。\n");
	print("変更できない場合は、\n");
	print("<a href=\"mailto:$MAINT\">$MAINT</a>までメールでお願いします。\n");
	print("</form></p>\n");

	print("<hr>\n");

	# 削除
	print("<p>削除</p>\n");
	print("<p>\n");
	print("<form action=\"$PROGRAM\" method =\"POST\">\n");
	print("<input name=\"c\" type=\"hidden\" value=\"ad\">\n");
	print("$H_ALIAS <input name=\"alias\" type=\"text\" size=\"$NAME_LENGTH\"><br>\n");
	print("<input type=\"submit\" value=\"ここ\">を押すと、\n");
	print("上記エイリアスが削除されます。\n");
	print("同じく登録の際と同じマシンでなければ削除できません。\n");
	print("</form></p>\n");

	print("<hr>\n");

	# 参照
	print("<p>\n");
	print("<form action=\"$PROGRAM\" method =\"POST\">\n");
	print("<input name=\"c\" type=\"hidden\" value=\"as\">\n");
	print("<input type=\"submit\" value=\"ここ\">を押すと、\n");
	print("エイリアスを参照できます。\n");
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

	# ホスト名を取り出す。
	local($RemoteHost) = $ENV{ 'REMOTE_HOST' };

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
		$HitFlag = (($RemoteHost eq $Host{$Alias}) ? 2 : 1);
	}

	# ホスト名が合わない!
	&MyFatal(6, '') if ($HitFlag == 1);

	# データの登録
	$Name{$Alias} = $N;
	$Email{$Alias} = $E;
	$Host{$Alias} = $RemoteHost;
	$URL{$Alias} = $U;

	# エイリアスファイルに書き出し
	&WriteAliasData($USER_ALIAS_FILE);

	# 表示画面の作成
	&MsgHeader($ALIASMOD_MSG);
	print("<p>$H_ALIAS <strong>$A</strong>のデータを\n");
	if ($HitFlag == 2) {
		print("変更しました。</p>\n");
	} else {
		print("登録しました。</p>\n");
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

	# ホスト名を取り出す。
	local($RemoteHost) = $ENV{ 'REMOTE_HOST' };

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
		$HitFlag = (($RemoteHost eq $Host{$Alias}) ? 2 : 1);
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
	&MsgHeader($ALIASDEL_MSG);
	print("<p>$H_ALIAS <strong>$A</strong>のデータを消去しました。</p>\n");
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
	&MsgHeader($ALIASSHOW_MSG);
	# あおり文
	print("<p>$H_AORI_ALIAS</p>\n");
	print("<p><a href=\"$PROGRAM?c=an\">エイリアスの新規登録/変更/削除を行なう。</a></p>\n");

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
## エイリアスファイルにデータを書き出す。
## CAUTION: %Name, %Email, %Host, %URLを必要とします。
##          $Nameが体と書き込まない。
#
sub WriteAliasData {

	# ファイル
	local($File) = @_;
	local($Alias);

	# ロックファイルを開く
	open(LOCK, "$LOCK_FILE") || &MyFatal(1, $LOCK_FILE);

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
	close(LOCK);

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
	open(ALIAS, "$KC2IN $USER_ALIAS_FILE |")
		# ファイルがないらしいのでさようなら。
		|| return('', '', '');

	# 1つ1つチェック。
	while(<ALIAS>) {
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

	open(ALIAS, "$KC2IN $BOARD_ALIAS_FILE |")
		|| &MyFatal(1, $BOARD_ALIAS_FILE);
	while(<ALIAS>) {

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
## 元記事の表示
#
sub ViewOriginalArticle {

	# IdとBoard
	local($Id, $Board) = @_;

	# 引用するファイル
	local($QuoteFile) = &GetArticleFileName($Id, $Board);

	# 引用部分を判断するフラグ
	local($QuoteFlag) = 0;

	open(TMP, "$KC2IN $QuoteFile |") || &MyFatal(1, $QuoteFile);
	while(<TMP>) {

		# 引用終了の判定
		$QuoteFlag = 0 if (/^$COM_ARTICLE_END$/);

		# 引用文字列の表示
		if ($QuoteFlag == 1) {
			print(&URLConvert($Board, $_));
		}

		# 引用開始の判定
		$QuoteFlag = 1 if ((/^$COM_HEADER_BEGIN$/) ||
					(/^$COM_ARTICLE_BEGIN$/));

	}
	close(TMP);

}


###
## 文字列中に<a href="$ARTICLE_PREFIX.??.html">があったら、
## 相対を絶対URLに書き換えてから返す。
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
## 元記事の表示(ファイル)
#
sub ViewOriginalFile {

	# ファイル名
	local($File) = @_;

	# 引用部分を判断するフラグ
	local($QuoteFlag) = 0;

	open(TMP, "$KC2IN $File |") || &MyFatal(1, $File);
	while(<TMP>) {

		# 引用終了の判定
		$QuoteFlag = 0 if (/^$COM_ARTICLE_END$/);

		# 引用文字列の表示
		if ($QuoteFlag == 1) {
			print($_);
		}

		# 引用開始の判定
		$QuoteFlag = 1 if (/^$COM_ARTICLE_BEGIN$/);

	}
	close(TMP);

}


###
## 記事のヘッダの表示
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
## ボード名称とIdからファイルのパス名を作り出す。
#
sub GetArticleFileName {

	# IdとBoard
	local($Id, $Board) = @_;

	# Boardが空ならBoardディレクトリ内から相対、
	# 空でなければシステムから相対
	$Board
		? return("$SYSTEM_DIR/$Board/$ARTICLE_PREFIX.$Id.html")
		: return("$ARTICLE_PREFIX.$Id.html");
}


###
## ボード名称とファイル名から、そのファイルのパス名を作り出す。
#
sub GetPath {

	# BoardとFile
	local($Board, $File) = @_;

	# 返す
	return("$SYSTEM_DIR/$Board/$File");

}


###
## ボード名称とファイル名から、そのファイルのURLを作り出す。
#
sub GetURL {

	# BoardとFile
	local($Board, $File) = @_;

	# 返す
	return("$SYSTEM_DIR_URL/$Board/$File");

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
	local($Subject) = '';

	# 該当ファイルからSubject文字列を取り出す。
	open(TMP, "$KC2IN $ArticleFile |") || &MyFatal(1, $ArticleFile);
	while(<TMP>) {
		if (/^<strong>$H_SUBJECT<\/strong> \[[^\]]*\] (.*)<br>$/) {
			$Subject = $1;
		}
	}
	close(TMP);

	# 返す
	return($Subject);
}


###
## あるファイルからTitleを取ってくる
#
sub GetSubjectFromFile {

	# ファイル
	local($File) = @_;

	# 取り出したSubject
	local($Title) = '';

	open(TMP, "$KC2IN $File |") || &MyFatal(1, $File);
	while(<TMP>) {

		if (/^<[Tt][Ii][Tt][Ll][Ee]>(.*)<\/[Tt][Ii][Tt][Ll][Ee]>$/) {
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
	local($File4Mail) = "$TMPDIR/tmp.kb.$$";

	# メール用ファイルを開く
	open(MAIL, "| $KC2OUT > $File4Mail") || &MyFatal(1, $File4Mail);

	# Toヘッダ
	foreach (@To) {
		print(MAIL "To: $_\n");
	}

	# Ccヘッダ
	# さすがにうざったかろう。^^;
	# print(MAIL "Cc: ", $MAINT, "\n");

	# Subjectヘッダ
	print(MAIL "Subject: $Subject\n\n");

	# 本文
	print(MAIL "$Message\n");

	# 閉じる
	close(MAIL);

	# メール送信
	system("$MAIL2 < $File4Mail");

	# ファイル消去
	unlink("$File4Mail");
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

	&MsgHeader($ERROR_MSG);

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
	} else {
		print("<p>エラー番号不定: お手数ですが、");
		print("このエラーが生じた状況を");
		print("<a href=\"mailto:$MAINT\">$MAINT</a>まで");
		print("お知らせ下さい。</p>\n");
	}

	&MsgFooter;
	exit 0;
}
