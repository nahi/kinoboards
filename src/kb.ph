# $Id: kb.ph,v 2.1 1995-12-19 18:46:21 nakahiro Exp $
#
# $Log: kb.ph,v $
# Revision 2.1  1995-12-19 18:46:21  nakahiro
# send mail
#
# Revision 2.0  1995/12/19 14:27:25  nakahiro
# user writable alias file.
#
# Revision 1.3  1995/12/19 07:24:49  nakahiro
# MAINT
#
# Revision 1.1  1995/12/15 12:38:44  nakahiro
# Initial revision
#


# kinoBoards: Kinoboards Is Network Opened BOARD System


#/////////////////////////////////////////////////////////////////////


###
## ユーザが定義する宣言(動かす前に必ず変更する必要がある)
#

#
# 管理者のe-mail addr.
#
$MAINT = "nakahiro@kinotrope.co.jp";
### $MAINT = "nakahiro@ohara.info.waseda.ac.jp";

#
# プログラムが存在するディレクトリのURL表示
#
# 自分のディレクトリに置く場合
$PROGRAM_DIR_URL = "http://www.kinotrope.co.jp/~nakahiro";
# 共用のディレクトリに置く(置かねばならない)場合
### $PROGRAM_DIR_URL = "http://www.ohara.info.waseda.ac.jp/cgi-bin";

#
# システムが存在するディレクトリのURL表示
#
$SYSTEM_DIR_URL = "http://www.kinotrope.co.jp/~nakahiro";
### $SYSTEM_DIR_URL = "http://www.ohara.info.waseda.ac.jp/person/nakahiro/kb";

# システムが存在するディレクトリ
$SYSTEM_DIR = "/home/nakahiro/public_html";
### $SYSTEM_DIR = "/home/common/WWW/DocumentRoot/person/nakahiro/kb";

#
# 漢字コードコンバータ(入力はUJISへ、出力はJISへ)のパスとオプション
#
$KC2IN = "/usr/local/bin/nkf -e";
$KC2OUT = "/usr/local/bin/nkf -j";
### $KC2IN = "/usr/local/bin/kc -e";
### $KC2OUT = "/usr/local/bin/kc -j";

#
# sendmailのパスとオプション
#
$MAIL2 = "/usr/lib/sendmail -oi -t";

#
# テンポラリファイルを置くディレクトリ
#
$TMPDIR = "/var/tmp";

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
$ALIASNEW_MSG = "エイリアスの登録/変更/削除";
$ALIASMOD_MSG = "エイリアスが変更されました";
$ALIASDEL_MSG = "エイリアスが削除されました";
$ALIASSHOW_MSG = "エイリアスの参照";
$ERROR_MSG   = "ERROR!";

$H_BOARD = "ボード:";
$H_SUBJECT = "　題　:";
$H_ALIAS = "エイリアス:";
$H_FROM = "お名前:";
$H_MAIL = "メール:";
$H_HOST = "マシン:";
$H_URL = "URL(省略可):";
$H_DATE = "投稿日:";
$H_REPLY = "元記事:";
$H_FOLLOW = "▼反応";
$H_FMAIL = "反応がついた時にメールで知らせる:";

$H_TEXTTYPE = "入力形式:";
$H_HTML = "HTML文書";
$H_PRE = "整形済み文書";

# あおり文
$H_AORI = "普通に書き込んで下さい。自動的な折り返しは行なわず、書いたまま表示されます。ただし、&lt; &gt; &amp; &quot; は、そのままでは使えません。代わりにそれぞれ、 &amp;lt; &amp;gt; &amp;amp; &amp;quot; と書くと、正しく表示されます。<br>HTMLのわかる方は、「$H_TEXTTYPE」を「$H_HTML」にしてHTMLとして書いて頂くと、HTML整形を行ないます。";

# エイリアス参照の際のヘッダ
$H_AORI_ALIAS = "投稿の際、「お名前」の部分に以下の「#....」を入力すると、登録されているお名前とe-mail addr.、URLが自動的に補われます。";

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

#
# ファイル
#
# このプログラム
$PROGRAM_NAME = "kb.cgi";
# ロックファイル
$LOCK_FILE_NAME = ".lock.kb";
# 記事番号ファイル
$ARTICLE_NUM_FILE_NAME = ".articleid";
# タイトルファイル
$TITLE_FILE_NAME = "index.html";
# allファイル
$ALL_FILE_NAME = "all.html";
# タイトルtmporaryファイル
$TTMP_FILE_NAME = "index.tmp";
# ユーザエイリアスファイル
$USER_ALIAS_FILE_NAME = "kinousers";
# ボードエイリアスファイル
$BOARD_ALIAS_FILE_NAME = "kinoboards";


#/////////////////////////////////////////////////////////////////////


###
## その他の宣言(ここから先は変更しないでね)
#

#
# URL
#
# このプログラム
$PROGRAM = "$PROGRAM_DIR_URL/$PROGRAM_NAME";
# ユーザエイリアスファイル
$USER_ALIAS_FILE_URL = "$SYSTEM_DIR_URL/$USER_ALIAS_FILE_NAME";

#
# ファイル
#
# このプログラム
$PROGRAM_NAME = "kb.cgi";
# ロックファイル
$LOCK_FILE = "$SYSTEM_DIR/$LOCK_FILE_NAME";
# ユーザエイリアスファイル
$USER_ALIAS_FILE = "$SYSTEM_DIR/$USER_ALIAS_FILE_NAME";
# ボードエイリアスファイル
$BOARD_ALIAS_FILE = "$SYSTEM_DIR/$BOARD_ALIAS_FILE_NAME";

#
# 制御用コメント文
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

#
# 配列のdefault
#
$[ = 0;


#/////////////////////////////////////////////////////////////////////
1;