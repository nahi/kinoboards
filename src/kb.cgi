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
#		「上へ」「下へ」のリンク機能の追加(次/前は廃止?)
#		まとめ読みの時、threadをわかりやすくする工夫を
#		部分日付ソート
#		aliasの登録機能
#		Subjectの先頭にIconをつけたい
#		Boardを自由に選択する


###
## ユーザが定義する宣言(動かす前に必ず変更して!)
#

#
# 管理者のe-mail addr.
#
$Maint = "nakahiro@ohara.info.waseda.ac.jp";

#
# プログラムが存在するディレクトリのURL表示
#
$PROGRAM_DIR_URL = "/~nakahiro";


###
## ユーザが定義する宣言(特に変更しないでもOK)
#

#
# このプログラムの名前
#
$PROGRAM_NAME = "kb.cgi";

#
# 記事のプレフィクス
# 記事ファイルが、「(指定した文字列).(記事番号).html」になる。
#
$ARTICLE_PREFIX = "kb";

#
# メッセージの宣言
#
$ENTRY_MSG = "きのぼーずへの書き込み";
$PREVIEW_MSG = "書き込みの内容を確認して下さい";
$THANKS_MSG = "書き込みありがとうございました";
$SORT_MSG = "日付順ソート";
$NEWARTICLE_MSG = "最近の記事";
$THREADARTICLE_MSG = "反応まとめ読み";
$ERROR_MSG   = "ERROR!";

$ADDRESS = "Copyright 1995 <a href=\"http://www.kinotrope.co.jp/\">kinotrope Co.,Ltd.</a> &amp; <a href=\"http://www.ohara.info.waseda.ac.jp/person/nakahiro/nakahiro.html\">nakahiro</a> // 禁無断転載";

$H_BOARD = "ボード:";
$H_SUBJECT = "　題　:";
$H_FROM = "お名前:";
$H_MAIL = "メール:";
$H_HOST = "マシン:";
$H_DATE = "投稿日:";
$H_REPLY = "元記事:";
$H_FOLLOW = "▼反応";

$H_TEXTTYPE = "入力形式:";
$H_HTML = "HTML文書";
$H_PRE = "整形済み文書";

$H_AORI = "普通に書き込んで下さい。自動的な折り返しは行なわず、書いたまま表示されます。ただし、&lt; &gt; &amp; &quot; は、そのままでは使えません。代わりにそれぞれ、 &amp;lt; &amp;gt; &amp;amp; &amp;quot; と書くと、正しく表示されます。<br>HTMLのわかる方は、「$H_TEXTTYPE」を「$H_HTML」にしてHTMLとして書いて頂くと、HTML整形を行ないます。";

#
# 引用マーク
#
$DEFAULT_QMARK = " ] ";

#
# 各入力項目の大きさ
#
$SUBJECT_LENGTH = 45;
$TEXT_ROWS      = 15;
$TEXT_COLS      = 50;
$NAME_LENGTH    = 45;
$MAIL_LENGTH    = 45;
$URL_LENGTH     = 37;


#/////////////////////////////////////////////////////////////////////


###
## その他の宣言(ここから先は変更しないでね)
#

#
# このプログラムのURL
#
$PROGRAM = $PROGRAM_DIR_URL . "/" . $PROGRAM_NAME;

#
# Permission of Title File.
#
$TITLE_FILE_PERMISSION = "0666";

#
# ファイル
#
# ロックファイル
$LOCK_FILE = ".lock.kb";
# 記事番号ファイル
$ARTICLE_NUM_FILE_NAME = ".articleid";
# タイトルファイル
$TITLE_FILE_NAME = "index.html";
# allファイル
$ALL_FILE_NAME = "all.html";
# タイトルtmporaryファイル
$TTMP_FILE_NAME = "index.tmp";
# ユーザエイリアスファイル
$USER_ALIAS_FILE = "kinousers";
# ボードエイリアスファイル
$BOARD_ALIAS_FILE = "kinoboards";

#
# ロックのタイプ
#
$LOCK_SH = 1;
$LOCK_EX = 2;
$LOCK_NB = 4;
$LOCK_UN = 8;

#
# 引用フラグ
#
$QUOTE_ON = 1;
$NO_QUOTE = 0;


###
## メイン
#

MAIN: {

	local($Command, $Id, $File, $Num);

	# 標準入力(POST)または環境変数(GET)のデコード。
	&cgi'decode;

	# REQUEST_METHODがPOSTならPreview画面へ、GETなら場合に応じて分岐する。
	#
	#	新規:			c=n
	#
	#	引用つきフォロー:	c=q&id=[1-9][0-9]*
	#	引用なしフォロー:	c=f&id=[1-9][0-9]*
	#	ファイル引用フォロー:	c=q/f&file=filename
	#
	#	確認済み:		c=x&id=[1-9][0-9]*(引用でない時はid=0)
	#
	#	日付順ソート:		c=r
	#	最新の記事n個:		c=l&num=[1-9][0-9]*
	#	threadまとめ読み:	c=t&id=[1-9][0-9]*
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

# おしまい
exit 0;


#/////////////////////////////////////////////////////////////////////


#
# サブルーチン
#


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
	print("<input name=\"board\" type=\"hidden\" value=\"$Board\">\n");

	# 引用Id; 引用でないなら0。
	print("<input name=\"id\" type=\"hidden\" value=\"$Id\">\n");

	# あおり文
	print("<p>$H_AORI</p>\n");

	# TextType
	print("$H_TEXTTYPE\n");
	print("<SELECT NAME=\"texttype\">\n");
	print("<OPTION SELECTED>$H_PRE\n");
	print("<OPTION>$H_HTML\n");
	print("</SELECT><BR>\n");

	# Board名; 本当は自由に選択できるようにしたい。
	print("$H_BOARD $BoardName<br>\n");

	# Subject(フォローなら自動的に文字列を入れる)
	if ($Id != 0) {
		printf("$H_SUBJECT <input name=\"subject\" value=\"%s\" size=\"$SUBJECT_LENGTH\"><br>\n", &GetReplySubject($Id, $Board));
	} else {
		print("$H_SUBJECT <input name=\"subject\" value=\"\" size=\"$SUBJECT_LENGTH\"><br>\n");
	}

	# 本文(引用ありなら元記事を挿入)
	print("<textarea name=\"article\" rows=\"$TEXT_ROWS\" cols=\"$TEXT_COLS\">\n");
	&QuoteOriginalArticle($Id, $Board)
		if ($Id != 0 && $QuoteFlag == $QUOTE_ON);
	print("</textarea><br>\n");

	# 名前とメールアドレス、URL。
	print("$H_FROM <input name=\"name\" size=\"$NAME_LENGTH\"><br>\n");
	print("$H_MAIL <input name=\"mail\" size=\"$MAIL_LENGTH\"><br>\n");
	print("URL(空でもOK):<input name=\"url\" value=\"http://\" size=\"$URL_LENGTH\"><br>\n");

	print("<p>入力できましたら、\n");
	print("<input type=\"submit\" value=\"ここ\">\n");
	print("を押して記事を確認しましょう(まだ投稿しません)。</p>\n");

	# お約束
	print("</form>\n");

	&MsgFooter;
}


###
## プレビュー画面
#
sub Preview {

	# Boardの取得
	local($Board) = $cgi'tags{'board'};

	# TextTypeの取得
	local($TextType) = $cgi'tags{'texttype'};

	# テンポラリファイルの作成
	local($TmpFile) = &MakeTemporaryFile($Board, $TextType);

	# 表示画面の作成
	&MsgHeader($PREVIEW_MSG);

	# お約束
	print("<form action=\"$PROGRAM/$Board\" method =\"GET\">\n");
	print("<input name=\"file\" type=\"hidden\" value=\"$TmpFile\">\n");
	print("<input name=\"c\" type=\"hidden\" value=\"x\">\n");
	printf("<input name=\"id\" type=\"hidden\" value=\"%d\">\n",
		$cgi'tags{'id'});

	# あおり文
	print("<p>以下の記事を確認したら、");
	print("<input type=\"submit\" value=\"ここ\">");
	print("を押して書き込んで下さい。</p>\n");

	# 確認する記事の表示
	open(TMP, "<$TmpFile");
	while(<TMP>) {
		print($_);
	}

	# お約束
	print("</form>\n");

	&MsgFooter;

}


###
## 登録後画面
#
sub Thanks {

	# テンポラリファイル名と引用した記事のId
	local($TmpFile, $Id) = @_;

	# 選択されたBoardの取得
	local($Board) = substr($ENV{'PATH_INFO'}, $[ + 1);

	# 登録ファイルのURL
	local($TitleFileURL)
		= $PROGRAM_DIR_URL . "/" . $Board . "/" . $TITLE_FILE_NAME;

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
## 日付順にソート。新しいものが上。
#
sub SortArticle {

	# 選択されたBoardの取得
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
## 新しい記事からn個を表示。
#
sub MyArticleSort {
	local($MyA, $MyB) = ($a, $b);
	$MyA =~ s/<li><strong>([0-9]*) .*$/$1/;
	$MyB =~ s/<li><strong>([0-9]*) .*$/$1/;
	return($MyA <=> $MyB);
}

###
## 新しい記事からn個を表示。
#
sub NewArticle {

	# 表示する個数を取得
	local($Num) = @_;

	# 選択されたBoardの取得
	local($Board) = substr($ENV{'PATH_INFO'}, $[ + 1);

	# 記事番号を収めるファイル
	local($ArticleNumFile) = $Board . "/" . $ARTICLE_NUM_FILE_NAME;

	# 最新記事番号を取得
	$ArticleToId = &GetArticleId($ArticleNumFile);

	# 取ってくる最初の記事番号を取得
	$ArticleFromId = $ArticleToId - $Num + 1;

	local($i, $File);

	# 表示画面の作成
	&MsgHeader($NEWARTICLE_MSG);

	print("<p>記事数: $Num ($ArticleToId 〜 $ArticleFromId)</p>");

	# nameへのリンクを表示
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
## フォロー記事を全て表示。
#
sub ThreadArticle {

	# 元記事のIdを取得
	local($Id) = @_;

	# 選択されたBoardの取得
	local($Board) = substr($ENV{'PATH_INFO'}, $[ + 1);

	# 表示画面の作成
	&MsgHeader($THREADARTICLE_MSG);

	# メイン関数の呼び出し(subject)
#	&ThreadArticleMain('subject only', $Id, $Board);

	# メイン関数の呼び出し
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

	# 区切り
	print("<hr>\n");

	if ($SubjectOnly) {
		&MyFatal(999, 'unknown');
	} else {
		# 元記事の表示
		&ViewOriginalArticle($Id, $Board);
	}

	# フォロー記事の表示
	foreach (@FollowIdList) {
		# 再帰
		&ThreadArticleMain($SubjectOnly, $_, $Board);
	}
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
	local($TmpFile) = "$Board/.$ARTICLE_PREFIX.$$";

	# 日付を取り出す。
	local($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst)
		= localtime(time);
	local($InputDate)
		= sprintf("%d月%d日%02d時%02d分", $mon + 1, $mday, $hour, $min);

	# ホスト名を取り出す。
	local($RemoteHost) = $ENV{ 'REMOTE_HOST' };

	# 引用ファイル、そのSubject
	local($ReplyArticleFile, $ReplyArticleSubject);

	# もし引用なら引用ファイル名を取得
	if ($cgi'tags{'id'} != 0) {
		$ReplyArticleFile = &GetArticleFileName($cgi'tags{'id'}, '');
		$ReplyArticleSubject = &GetSubject($cgi'tags{'id'}, $Board);
	} elsif ($cgi'tags{'file'} ne '') {
		$ReplyArticleFile = "../" . $cgi'tags{'file'};
		$ReplyArticleSubject = &GetSubjectFromFile($cgi'tags{'file'});
	}

	# エイリアスチェック
	$_ = $cgi'tags{'name'};
	if (/^#.*$/) {
		($cgi'tags{'name'}, $cgi'tags{'mail'}, $cgi'tags{'url'})
			= &GetUserInfo($_);
		if ($cgi'tags{'name'} eq "") {
			&MsgHeader($ERROR_MSG);
			print("<H2>$_はエイリアスに登録されていません</h2>");
			print("<p>戻ってもう一度。</p>");
			&MsgFooter;
			exit 0;
		}
	}

	# 空チェック
	&MyFatal(2, '') if ($cgi'tags{'subject'} eq "")
		|| ($cgi'tags{'article'} eq "")
		|| ($cgi'tags{'name'} eq "")
		|| ($cgi'tags{'mail'} eq "");

	# サブジェクトのタグチェック
	$_ = $cgi'tags{'subject'};
	&MyFatal(4, '') if (/</);

	# テンポラリファイルに書き出す。
	open(TMP, ">$TmpFile") || &MyFatal(1, $TmpFile);

	# まずヘッダ。
	printf(TMP "<strong>$H_SUBJECT</strong> %s<br>\n", $cgi'tags{'subject'});

	if ($cgi'tags{'url'} eq "http://" || $cgi'tags{'url'} eq "") {
		# URLがない場合
		printf(TMP "<strong>$H_FROM</strong> %s<br>\n", $cgi'tags{'name'});
	} else {
		# URLがある場合
		printf(TMP "<strong>$H_FROM</strong> <a href=\"%s\">%s</a><br>\n", $cgi'tags{'url'}, $cgi'tags{'name'});
	}

	printf(TMP "<strong>$H_MAIL</strong> <a href=\"mailto:%s\">&lt;%s&gt;</a><br>\n",
		$cgi'tags{'mail'}, $cgi'tags{'mail'});
#	print(TMP "<strong>$H_HOST</strong> $RemoteHost<br>\n");
# kinotropeではgethostbyaddrも使えないようなので、現状でホスト名は省略
	print(TMP "<strong>$H_DATE</strong> $InputDate<br>\n");

	# 引用の場合
	if ($cgi'tags{'id'} != 0) {
		printf(TMP "<strong>$H_REPLY</strong> [$BoardName: %d] <a href=\"$ReplyArticleFile\">$ReplyArticleSubject</a><br>\n", $cgi'tags{'id'});
	} elsif ($cgi'tags{'file'} ne '') {
		printf(TMP "<strong>$H_REPLY</strong> <a href=\"$ReplyArticleFile\">$ReplyArticleSubject</a><br>\n");
	}

	print(TMP "------------------------<br>\n");

	# article begin
	print(TMP "<!-- Article Begin -->\n");

	# TextType用前処理
	print(TMP "<pre>\n") if ($TextType eq $H_PRE);

	# 記事
	printf(TMP "%s\n", $cgi'tags{'article'});

	# TextType用後処理
	print(TMP "</pre>\n") if ($TextType eq $H_PRE);

	# article end
	print(TMP "<!-- Article End -->\n");
	print(TMP "<hr>\n");
	close TMP;

	# ファイル名を返す。
	return($TmpFile);
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
	local($ArticleNumFile) = $Board . "/" . $ARTICLE_NUM_FILE_NAME;

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
	close TMP;

	# ロックファイルを開く
	open(LOCK, "$LOCK_FILE")
		# 開けなきゃ作る
		|| (&MakeLockFile($LOCK_FILE) && open(LOCK, "$LOCK_FILE"))
		# 作れなきゃエラー
		|| &MyFatal(1, $LOCK_FILE);

	# ロックをかける
	&lock();

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
	print(ART "<!-- Header Begin -->\n");

	# ボディの先頭にボード名と記事番号、題を入れる
	printf(ART "<strong>$H_SUBJECT</strong> [$BoardName: %d] $Subject<br>\n", $ArticleId);

	# テンポラリファイルからの記事のコピー
	open(TMP, "$TmpFile") || &MyFatal(1, $TmpFile);

	# Subject行は挿入済みなので1行飛ばす。
	$Dust = <TMP>;

	while(<TMP>) {
		print(ART $_)
	}
	close TMP;

	# テンポラリファイルの削除
	unlink("$TmpFile");

	# 記事フッタの作成
	print(ART "$H_FOLLOW\n<ol>\n");
	close ART;

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
	&unlock();
	close LOCK;

}


###
## allリストに書き込む
#
sub AddAllFile {

	# 記事Id、Board, 名前、題、日付
	local($Id, $Board, $Name, $Subject, $InputDate) = @_;

	# 登録ファイル
	local($File) = $Board . "/" . $ALL_FILE_NAME;

	# 追加するファイルの名前
	local($ArticleFile) = &GetArticleFileName($Id, '');

	# Add to 'All' file
	open(ALL, ">>$File") || &MyFatal(1, $File);
	printf(ALL "<li><strong>$Id .</strong> <a href=\"%s\">$Subject</a> [$Name] $InputDate\n\n", $ArticleFile);
	close TITLE;
}
###
## タイトルリストに書き込む(新規)
#
sub AddTitleNormal {

	# 記事Id、Board, 名前、題、日付
	local($Id, $Board, $Name, $Subject, $InputDate) = @_;

	# 登録ファイル
	local($File) = $Board . "/" . $TITLE_FILE_NAME;

	# 追加するファイルの名前
	local($ArticleFile) = &GetArticleFileName($Id, '');

	# タイトルファイルに追加
	open(TITLE, ">>$File") || &MyFatal(1, $File);
	printf(TITLE "<li><strong>$Id .</strong> <a href=\"%s\">$Subject</a> [$Name] $InputDate\n\n", $ArticleFile);
	close TITLE;
}


###
## タイトルリストに書き込む(フォロー)
#
sub AddTitleFollow {

	# 記事Id、Board, フォロー記事Id、名前、題、日付
	local($Id, $Board, $Fid, $Name, $Subject, $InputDate) = @_;

	# 登録ファイル
	local($File) = $Board . "/" . $TITLE_FILE_NAME;

	# 追加するファイルの名前
	local($ArticleFile) = &GetArticleFileName($Id, '');

	# Followed Article File Name
	local($FollowedArticleFile) = &GetArticleFileName($Fid, '');

	# TmpFile
	local($TmpFile) = "$Board/$TTMP_FILE_NAME";

	# Follow Flag
	local($AddFlag, $Nest, $NextLine) = (0, 0, ''); 

	# タイトルファイルに追加
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

	# 追加
	open(FART, ">>$ArticleFile") || &MyFatal(1, $ArticleFile);
	print(FART "<li><a href=\"$FollowArticleFile\">$Fsubject</a> ← $Fname さん\n");
	close FART;
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

	open(TMP, "$File") || &MyFatal(1, $File);
	while(<TMP>) {

		# フォロー部分開始の判定
		$QuoteFlag = 1 if (/^<!-- Article End -->$/);

		# フォローIdの取得
		if (($QuoteFlag == 1) &&
		(/^<li><a href=\"$ARTICLE_PREFIX\.([^\.]*)\.html\">/)) {
			push(@Result, $1);
		}
	}
	close TMP;

	return(@Result);
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

	open(TMP, "$QuoteFile") || &MyFatal(1, $QuoteFile);
	while(<TMP>) {

		# 引用終了の判定
		$QuoteFlag = 0 if (/^<!-- Article End -->$/);

		# 引用文字列の表示
		if ($QuoteFlag == 1) {
			print($_);
		}

		# 引用開始の判定
		$QuoteFlag = 1 if ((/^<!-- Header Begin -->$/) ||
					(/^<!-- Article Begin -->$/));

	}
	close TMP;

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

	open(TMP, "$QuoteFile") || &MyFatal(1, $QuoteFile);
	while(<TMP>) {

		# 引用終了の判定
		$QuoteFlag = 0 if (/^<!-- Article End -->$/);

		# 引用文字列の表示
		if ($QuoteFlag == 1) {
			s/&/&amp;/go;
			s/\"//go;
			s/<//go;
			s/>//go;
			print($DEFAULT_QMARK, $_);
		}

		# 引用開始の判定
		$QuoteFlag = 1 if (/^<!-- Article Begin -->$/);

	}
	close TMP;

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
	close AID;

	# 1増やして書き込む。
	open(AID, ">$ArticleNumFile") || &MyFatal(1, $ArticleNumFile);
	print(AID $ArticleId + 1, "\n");
	close AID;

	# 新しい記事番号を返す。
	return($ArticleId + 1);
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
	close AID;

	# 記事番号を返す。
	return($ArticleId);
}


###
## ユーザエイリアスからユーザの名前、メール、URLを取ってくる。
#
sub GetUserInfo {

	# エイリアス名
	local($Alias) = @_;

	# 名前、メール、URL
	local($Name, $Mail, $URL);

	open(ALIAS, "$USER_ALIAS_FILE") || &MyFatal(1, $USER_ALIAS_FILE);
	while(<ALIAS>) {

		# マッチしなきゃ次へ。
		next unless (/^$Alias$/);

		$Name = <ALIAS>;
		chop($Name);
		$Mail = <ALIAS>;
		chop($Mail);
		$URL = <ALIAS>;
		chop($URL);

		# 配列にして返す
		return($Name, $Mail, $URL);
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

	open(ALIAS, "$BOARD_ALIAS_FILE") || &MyFatal(1, $BOARD_ALIAS_FILE);
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
	open(TMP, "$ArticleFile") || &MyFatal(1, $ArticleFile);
	while(<TMP>) {
		if (/^<strong>$H_SUBJECT<\/strong> \[[^\]]*\] (.*)<br>$/) {
			$Subject = $1;
		}
	}
	close TMP;

	# 返す
	return($Subject);
}


###
## ボード名称とIdからファイル名を作り出す。
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
## ログファイルのロック関係
#
sub MakeLockFile {
	# ファイル名
	local($File) = @_;

	open(MAKELOCK, ">$File") || return(0);
	close MAKELOCK;
	return(1);
}

sub lock {
	# ロック
	flock(LOCK, $LOCK_EX);
	# おなじない
	seek(AID, 0, 2);
	seek(ART, 0, 2);
	seek(TITLE, 0, 2);
	seek(FART, 0, 2);
	seek(ALL, 0, 2);
}

sub unlock {
	# アンロック
	flock(LOCK, $LOCK_UN);
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
## エラー表示
#
sub MyFatal {

	# エラー番号とエラー情報の取得
	local($MyFatalNo, $MyFatalInfo) = @_;
	#
	# 1 ... File関連
	# 2 ... 投稿の際の、必須項目の欠如
	#

	&MsgHeader($ERROR_MSG);

	if ($MyFatalNo == 1) {
		print("<p>File: $MyFatalInfoが存在しない、\n");
		print("あるいはpermissionの設定が間違っています。\n");
		print("お手数ですが、<a href=\"$Maint\"</a>$Maint</a>まで\n");
		print("上記ファイル名をお知らせ下さい。</p>\n");
	} elsif ($MyFatalNo == 2) {
		print("<p>題、記事、お名前、メールアドレス、\n");
		print("いずれかが入力されていません。\n");
		print("戻ってもう一度。</p>\n");
	} elsif ($MyFatalNo == 3) {
		print("<p>Title File is illegal.\n");
		print("お手数ですが、<a href=\"$Maint\"</a>$Maint</a>まで\n");
		print("お知らせ下さい。</p>\n");
	} elsif ($MyFatalNo == 4) {
		print("<p>ごめんなさい、題中にHTMLタグを入れることは\n");
		print("禁じられています。戻ってもう一度。</a>\n");
	} else {
		print("<p>エラー番号不定: お手数ですが、");
		print("このエラーが生じた状況を");
		print("<a href=\"$Maint\"</a>$Maint</a>までお知らせ下さい。</p>\n");
	}

	&MsgFooter;
	exit 0;
}


#/////////////////////////////////////////////////////////////////////
# なかひろ用オプション


###
## 書き込み画面(option: ファイルから引用)
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
	print("<input name=\"board\" type=\"hidden\" value=\"$Board\">\n");

	# 引用Id; 正規の引用でないので0。
	print("<input name=\"id\" type=\"hidden\" value=\"0\">\n");

	# 引用ファイル
	print("<input name=\"file\" type=\"hidden\" value=\"$File\">\n");

	# あおり文
	print("<p>$H_AORI</p>\n");

	# TextType
	print("$H_TEXTTYPE\n");
	print("<SELECT NAME=\"texttype\">\n");
	print("<OPTION SELECTED>$H_PRE\n");
	print("<OPTION>$H_HTML\n");
	print("</SELECT><BR>\n");

	# Board名; 本当は自由に選択できるようにしたい。
	print("$H_BOARD $BoardName<br>\n");

	# Subject
	printf("$H_SUBJECT <input name=\"subject\" value=\"%s\" size=\"$SUBJECT_LENGTH\"><br>\n", &GetReplySubjectFromFile($File));

	# 本文(引用ありなら元記事を挿入)
	print("<textarea name=\"article\" rows=\"$TEXT_ROWS\" cols=\"$TEXT_COLS\">\n");
	&QuoteOriginalFile($File) if ($QuoteFlag == $QUOTE_ON);
	print("</textarea><br>\n");

	# 名前とメールアドレス、URL。
	print("$H_FROM <input name=\"name\" size=\"$NAME_LENGTH\"><br>\n");
	print("$H_MAIL <input name=\"mail\" size=\"$MAIL_LENGTH\"><br>\n");
	print("URL(空でもOK):<input name=\"url\" value=\"http://\" size=\"$URL_LENGTH\"><br>\n");

	print("<p>入力できましたら、\n");
	print("<input type=\"submit\" value=\"ここ\">\n");
	print("を押して記事を確認しましょう(まだ投稿しません)。</p>\n");

	# お約束
	print("</form>\n");

	&MsgFooter;
}


###
## 元記事の表示(ファイル)
#
sub ViewOriginalFile {

	# ファイル名
	local($File) = @_;

	# 引用部分を判断するフラグ
	local($QuoteFlag) = 0;

	open(TMP, "cat $File | /usr/local/bin/nkf -e |") || &MyFatal(1, $File);
	while(<TMP>) {

		# 引用終了の判定
		$QuoteFlag = 0 if (/^<!-- Article End -->$/);

		# 引用文字列の表示
		if ($QuoteFlag == 1) {
			print($_);
		}

		# 引用開始の判定
		$QuoteFlag = 1 if (/^<!-- Article Begin -->$/);

	}
	close TMP;

}


###
## 引用する(ファイル)
#
sub QuoteOriginalFile {

	# ファイル名
	local($File) = @_;

	# 引用部分を判断するフラグ
	local($QuoteFlag) = 0;

	open(TMP, "cat $File | /usr/local/bin/nkf -e |") || &MyFatal(1, $File);
	while(<TMP>) {

		# 引用終了の判定
		$QuoteFlag = 0 if (/^<!-- Article End -->$/);

		# 引用文字列の表示
		if ($QuoteFlag == 1) {
			s/&/&amp;/go;
			s/\"//go;
			s/<//go;
			s/>//go;
			print($DEFAULT_QMARK, $_);
		}

		# 引用開始の判定
		$QuoteFlag = 1 if (/^<!-- Article Begin -->$/);

	}
	close TMP;

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
## あるファイルからTitleを取ってくる
#
sub GetSubjectFromFile {

	# ファイル
	local($File) = @_;

	# 取り出したSubject
	local($Title) = '';

	open(TMP, "$File") || &MyFatal(1, $File);
	while(<TMP>) {

		if (/^<[Tt][Ii][Tt][Ll][Ee]>(.*)<\/[Tt][Ii][Tt][Ll][Ee]>$/) {
			$Title = $1;
		}
	}
	close TMP;

	# 返す。
	return($Title);

}


#/////////////////////////////////////////////////////////////////////

#
# cgi用パッケージ
#
package cgi;


###
## HTMLヘッダの生成
#
sub header {print "Content-type: text/html\n\n";}


###
## デコード
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
