#!/usr/local/bin/perl
#
# $Id: kb.cgi,v 1.0 1995-10-22 08:59:03 nakahiro Exp $
#
# $Log: kb.cgi,v $
# Revision 1.0  1995-10-22 08:59:03  nakahiro
# beta version.
# released on MAGARI page in kinotrope.
#


# kinoBoards: Kinoboards Is Network Opened BOARD System


#/////////////////////////////////////////////////////////////////////


# ToDo:
#	×SubjectをRe:にする
#	×In-Reply-To:をつける
#	×「〜にフォローされています」をつける。
#	×user alias
#	×board-name alias
#	Boardを自由に選択する。
#	×indent
#	×indentの並べ替え
#	×Error関数
#	Subjectの先頭にIconを!


###
## ユーザが定義する宣言(動かす前にチェックして!)
#

#
# Maintenance
#
$Maint = "nakahiro@ohara.info.waseda.ac.jp";

#
# このプログラムの名前
#
$PROGRAM_NAME = "kb.cgi";

#
# プログラムが存在するディレクトリのURL表示
#
$PROGRAM_DIR_URL = "/~nakahiro";

#
# 記事のプレフィクス
# 記事ファイルが、「(指定した文字列).(記事番号).html」になる。
#
$ARTICLE_PREFIX = "kb";

#
# メッセージの宣言
#
$ENTRY_MSG   = "kinoBoardsへの書き込み";
$PREVIEW_MSG = "書き込みの内容を確認して下さい";
$THANKS_MSG  = "書き込みありがとうございました";
$SORT_MSG    = "Sort Articles.";
$ERROR_MSG   = "ERROR!";

$ADDRESS = "Copyright 1995 <a href=\"http://www.kinotrope.co.jp/\">kinotrope Co.,Ltd.</a> &amp; <a href=\"http://www.ohara.info.waseda.ac.jp/person/nakahiro/nakahiro.html\">nakahiro</a> // 禁無断転載";

$H_BOARD = "ボード:";
$H_SUBJECT = "　題　:";
$H_FROM = "なまえ:";
$H_MAIL = "メール:";
$H_HOST = "マシン:";
$H_DATE = "投稿日:";
$H_REPLY = "元記事:";
$H_FOLLOW = "▼反応";

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
## その他の宣言(ここから先はいぢる必要はない、はず ^^;)
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

	local($Command, $id);

	# 標準入力(POST)または環境変数(GET)のデコード。
	&cgi'decode;

	# REQUEST_METHODがPOSTならPreview画面へ、GETなら場合に応じて分岐する。
	#
	#	新規:			c=n
	#	引用つきフォロー:	c=q&id=[1-9][0-9]*
	#	引用なしフォロー:	c=f&id=[1-9][0-9]*
	#	確認済み:		c=x&id=[1-9][0-9]*(引用でない場合はid=0)
	#	Sort Articles:		c=r
	#

	&Preview, last MAIN if ($ENV{'REQUEST_METHOD'} eq "POST");

	$Command = $cgi'tags{'c'};
	$Id = $cgi'tags{'id'};

	&Entry($NO_QUOTE, 0),			last MAIN if ($Command eq "n");
	&Entry($QUOTE_ON, $Id),			last MAIN if ($Command eq "q");
	&Entry($NO_QUOTE, $Id),			last MAIN if ($Command eq "f");
	&Thanks($cgi'tags{'file'}, $Id),	last MAIN if ($Command eq "x");
	&SortArticle,				last MAIN if ($Command eq "r");

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
		print("<pre>\n");
		&Quote($Id, $Board);
		print("</pre>\n<hr>\n");
		print("<h2>上の記事に反応する</h2>");
	}

	# お約束
	print("<form action=\"$PROGRAM\" method =\"POST\">\n");
	print("<input name=\"board\" type=\"hidden\" value=\"$Board\">\n");

	# 引用Id; 引用でないなら0。
	print("<input name=\"id\" type=\"hidden\" value=\"$Id\">\n");

	# あおり文
	print("<p>基本的にHTMLとして書き込んで下さい。HTMLがわからない場合は、普通の文章として打ち込んでみて下さい。段落わけ等はできませんが、まぁ伝言くらいなら何とかなると思います。^^;</p>\n");

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
	&Quote($Id, $Board) if ($Id != 0 && $QuoteFlag == $QUOTE_ON);
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

	# テンポラリファイルの作成
	local($TmpFile) = &MakeTemporaryFile($Board);

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
## Sort Articles
#
sub SortArticle {

	# 選択されたBoardの取得
	local($Board) = substr($ENV{'PATH_INFO'}, $[ + 1);
	# All file
	local($AllFile) = "$Board/$ALL_FILE_NAME";

	local(@lines);

	open(ALL, "$AllFile") || &MyFatal(1, $AllFile);
	while(<ALL>) {
		push(@lines, $_);
	}
	close ALL;

	# 表示画面の作成
	&MsgHeader($SORT_MSG);
	print("<ol>\n");
	foreach (reverse sort @lines) {
		print $_;
	}
	print("</ol>\n");
	&MsgFooter;
}


###
## 確認用テンポラリファイルを作成してファイル名を返す。
#
sub MakeTemporaryFile {

	# Boardの取得
	local($Board) = @_;

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

	# テンポラリファイルに書き出す。
	open(TMP, ">$TmpFile") || &MyFatal(1, $TmpFile);

	# まずヘッダ。
	printf(TMP "<b>$H_SUBJECT</b> %s<br>\n", $cgi'tags{'subject'});

	if ($cgi'tags{'url'} eq "http://" || $cgi'tags{'url'} eq "") {
		# URLがない場合
		printf(TMP "<b>$H_FROM</b> %s<br>\n", $cgi'tags{'name'});
	} else {
		# URLがある場合
		printf(TMP "<b>$H_FROM</b> <a href=\"%s\">%s</a><br>\n", $cgi'tags{'url'}, $cgi'tags{'name'});
	}

	printf(TMP "<b>$H_MAIL</b> <a href=\"mailto:%s\">&lt; %s &gt;</a><br>\n",
		$cgi'tags{'mail'}, $cgi'tags{'mail'});
	print(TMP "<b>$H_HOST</b> $RemoteHost<br>\n");
	print(TMP "<b>$H_DATE</b> $InputDate<br>\n");

	# 引用の場合
	if ($cgi'tags{'id'} != 0) {
		printf(TMP "<b>$H_REPLY</b> [$BoardName: %d] <a href=\"$ReplyArticleFile\">$ReplyArticleSubject</a><br>\n", $cgi'tags{'id'});
	}

	print(TMP "----<br>\n");

	# article begin
	print(TMP "<!-- Article Begin -->\n");

	# 記事
	printf(TMP "%s\n", $cgi'tags{'article'});

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
		if (/^<b>$H_SUBJECT<\/b> (.*)<br>$/) {$Subject = $1; }
		# 日付を取り出す。
		if (/^<b>$H_DATE<\/b> (.*)<br>$/) {$InputDate = $1; }
		# 名前を取り出す。
		if (/^<b>$H_FROM<\/b> <a[^>]*>(.*)<\/a><br>$/) {
			$Name = $1;
		} elsif (/^<b>$H_FROM<\/b> (.*)<br>$/) {
			$Name = $1;
		}

	}
	close TMP;

	# ロックファイルを開く
	open(LOCK, "$LOCK_FILE") || &MyFatal(1, $LOCK_FILE);
	# ロックをかける
	&lock();

	# 記事番号を取得
	$ArticleId = &GetArticleId($ArticleNumFile);

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
	print(ART "<a href=\"$PROGRAM/$Board?c=f&id=$ArticleId\">無し</a> )\n");
	print(ART "<hr>\n");

	# ボディの先頭にボード名と記事番号を入れる
	printf(ART "<b>$H_BOARD</b> [$BoardName: %d]<br>\n", $ArticleId);

	# テンポラリファイルからの記事のコピー
	open(TMP, "$TmpFile") || &MyFatal(1, $TmpFile);
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
	printf(ALL "<li><i>$InputDate</i> <a href=\"%s\">$Subject</a> [$Name]\n\n", $ArticleFile);
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
	printf(TITLE "<li><i>$InputDate</i> <a href=\"%s\">$Subject</a> [$Name]\n\n", $ArticleFile);
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

				printf(TTMP "<li><i>$InputDate</i> <a href=\"%s\">$Subject</a> [$Name]\n\n", $ArticleFile);

			} else {

				print(TTMP "<ul>\n");
				printf(TTMP "<li><i>$InputDate</i> <a href=\"%s\">$Subject</a> [$Name]\n\n", $ArticleFile);
				print(TTMP "</ul>\n");

			}

			$AddFlag = "True";
		}
	}

	# If not found, followed Article must be old one.
	printf(TTMP "<li><i>$InputDate</i> <a href=\"%s\">$Subject</a> [$Name]\n\n", $ArticleFile) if (! $AddFlag);

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
## 引用する
#
sub Quote {

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
			print(" ] ", $_);
		}

		# 引用開始の判定
		$QuoteFlag = 1 if (/^<!-- Article Begin -->$/);

	}
	close TMP;

}


###
## 記事番号を取ってくる(番号は1増える)。
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

	open(AID, ">$ArticleNumFile") || &MyFatal(1, $ArticleNumFile);
	print(AID $ArticleId + 1, "\n");
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
		if (/^<b>$H_SUBJECT<\/b> (.*)<br>$/) {
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
	} else {
		print("<p>エラー番号不定: お手数ですが、");
		print("このエラーが生じた状況を");
		print("<a href=\"$Maint\"</a>$Maint</a>までお知らせ下さい。</p>\n");
	}

	&MsgFooter;
	exit 0;
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
        }
}

#/////////////////////////////////////////////////////////////////////0> 
