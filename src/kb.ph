# $Id: kb.ph,v 1.2 1995-12-15 14:20:24 nakahiro Exp $
#
# $Log: kb.ph,v $
# Revision 1.2  1995-12-15 14:20:24  nakahiro
# String for Header of Search Module.
#
# Revision 1.1  1995/12/15 12:38:44  nakahiro
# Initial revision
#


# kinoBoards: Kinoboards Is Network Opened BOARD System

#/////////////////////////////////////////////////////////////////////


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

#
# 著作権表示
#
$ADDRESS = "Copyright 1995 <a href=\"http://www.kinotrope.co.jp/\">kinotrope Co.,Ltd.</a> &amp; <a href=\"http://www.kinotrope.co.jp/~nakahiro/\">nakahiro</a> // 禁無断転載";


#/////////////////////////////////////////////////////////////////////


###
## ユーザが定義する宣言(特に変更しないでもOK)
#

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
$SEARCHARTICLE_MSG = "記事の検索";
$ERROR_MSG   = "ERROR!";

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
# ※「>」や「&gt;」を引用マークにするのは避けて下さい。
#   トラブルを起こすブラウザが存在します。
#
$DEFAULT_QMARK = " ] ";

#
# 各入力項目の大きさ
#
# 題
$SUBJECT_LENGTH = 45;
# 記事行数
$TEXT_ROWS = 15;
# 記事幅
$TEXT_COLS = 50;
# 名前幅
$NAME_LENGTH = 45;
# E-mail幅
$MAIL_LENGTH = 45;
# URL幅
$URL_LENGTH = 37;
# 検索キーワード幅
$KEYWORD_LENGTH = 40;


#/////////////////////////////////////////////////////////////////////


###
## その他の宣言(ここから先は変更しないでね)
#

#
# このプログラムの名前
#
$PROGRAM_NAME = "kb.cgi";
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
# ユーザエイリアスファイルURL
$USER_ALIAS_FILE_URL = $PROGRAM_DIR_URL . "/" . $USER_ALIAS_FILE;
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
$NO_QUOTE = 0;
$QUOTE_ON = 1;


#/////////////////////////////////////////////////////////////////////
