# $Id: kb.ph,v 3.3 1996-02-11 06:54:09 nakahiro Exp $
#
# $Log: kb.ph,v $
# Revision 3.3  1996-02-11 06:54:09  nakahiro
# the 1st test version for my homepage.
#
# Revision 3.2  1996/02/08 07:11:04  nakahiro
# Bulletin board for KINOTROPE Inc.
#
# Revision 3.0  1996/01/20 14:01:35  nakahiro
# oow1
#
# Revision 2.1  1995/12/19 18:46:21  nakahiro
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
## ユーザが定義する宣言(動かす前に必ず変更する必要があります)
#


##
# 管理者のe-mail addr.
$MAINT = "nakahiro\@kinotrope.co.jp";

##
# where is this program?
# `relative' or the others (ex. `absolutive').
#
# CAUTION: this option does not work now...
#
$SYS_SCRIPTPATH = 'relative';

##
# sendmailのパスとオプション
$MAIL2 = "/usr/lib/sendmail -oi -t";

##
# 著作権表示
$ADDRESS = "Copyright 1996 <a href=\"http://www.kinotrope.co.jp/\">KINOTROPE Inc.</a> &amp; <a href=\"http://www.kinotrope.co.jp/~nakahiro/\">HiNa</a> // 禁無断転載";


#/////////////////////////////////////////////////////////////////////


###
## ユーザが定義する宣言(特に変更しないでもOK)
#

#
# システムの設定
#
# 入力文書タイプ(HTML or PRE)の選択を行うか否か(行なわないとPREのみ)
#   0: 行わない
#   1: 行う
$SYS_TEXTTYPE = 1;

# エイリアスを利用するか否か
#   0: 利用しない
#   1: 利用する
$SYS_ALIAS = 1;

# 引用時にタグを残すか否か
#   0: 残さない
#   1: 残す
$SYS_TAGINQUOTE = 1;

# 新規投稿記事が、上に増えていくか、下に増えていくか
#   0: 上
#   1: 下
$SYS_BOTTOMTITLE = 0;

# メール送信サービスを利用するか否か(日本語のみ)
#   0: 利用しない
#   1: 利用する
$SYS_FOLLOWMAIL = 1;

#
# 色の指定
#
$BG_COLOR = "#66CCCC";
$TEXT_COLOR = "#000000";
$LINK_COLOR = "#0000AA";
$ALINK_COLOR = "#FF0000";
$VLINK_COLOR = "#00AA00";

#
# メッセージの宣言
#
$SYSTEM_NAME = "きのぼーず";

$ENTRY_MSG = "$SYSTEM_NAME への書き込み";
$SHOWICON_MSG = "アイコンの説明";
$PREVIEW_MSG = "書き込みの内容を確認して下さい";
$THANKS_MSG = "書き込みありがとうございました";
$VIEW_MSG = "タイトル一覧";
$SORT_MSG = "タイトル一覧(日付順)";
$NEWARTICLE_MSG = "記事をまとめて読む";
$THREADARTICLE_MSG = "反応まとめ読み";
$SEARCHARTICLE_MSG = "記事の検索";
$ALIASNEW_MSG = "エイリアスの登録/変更/削除";
$ALIASMOD_MSG = "エイリアスが変更されました";
$ALIASDEL_MSG = "エイリアスが削除されました";
$ALIASSHOW_MSG = "エイリアスの参照";
$ERROR_MSG   = "$SYSTEM_NAME: ERROR!";

$H_BOARD = "掲示板:";
$H_ICON = "アイコン:";
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

$H_NOICON = "なし";

# あおり文
$H_REPLYMSG = "上の記事に反応する";
$H_AORI = "題、記事、お名前、メールアドレス、さらにホームページをお持ちの方はURL(省略可)を書き込んでください。記事は、1行をあまり長くせず、適当に折り返して書いて頂くと読み易くなります。<br>HTMLをご存じの方は、「$H_TEXTTYPE」を「$H_HTML」にしてHTMLとして書いて頂くと、HTML整形を行ないます。";
$H_SEEICON = "アイコンを見る";
$H_SEEALIAS = "エイリアスを見る";
$H_ALIASENTRY = "登録する";
$H_ALIASINFO = "エイリアスに登録されている方は、「$H_FROM」に「#...」と書くと、自動的に補完されます。";
$H_ENTRYINFO = "入力できましたら、記事を確認しましょう(まだ投稿しません)。";
$H_PUSHHERE = "ここを押してください";
$H_ICONINTRO = "「$BoardName」では次のアイコンを使うことができます。";
$H_POSTINFO = "以下の記事を確認したら、書き込みましょう。";
$H_THANKSMSG = "書き込みの訂正、取消などはメールでお願いいたします。";
$H_BACK = "戻る";
$H_NEXTARTICLE = "次の記事へ";
$H_REPLYTHISARTICLE = "記事に反応";
$H_REPLYTHISARTICLEQUOTE = "引用して反応";
$H_READREPLYALL = "反応をまとめ読み";
$H_REPLYNOTE = " ← %s さん";
$H_ARTICLES = "記事数";
$H_JUMPID = "↑の数字をクリックすると、そのIDの記事に飛びます。新しい記事ほど上の方にあります。";
$H_KEYWORD = "キーワード";
$H_INPUTKEYWORD = "$H_KEYWORD を入力してくたら、";
$H_NOTFOUND = "該当する記事は見つかりませんでした。";
$H_ALIASTITLE = "新規登録/登録内容の変更";
$H_ALIASNEWCOM = "エイリアスの新規登録/登録内容の変更が行なわれます。ただし変更は、登録の際と同じマシンでなければできません。変更できない場合は、<a href=\"mailto:$MAINT\">$MAINT</a>までメールでお願いします。";
$H_ALIASDELETE = "削除";
$H_ALIASDELETECOM = "上記エイリアスが削除されます。同じく登録の際と同じマシンでなければ削除できません。";
$H_ALIASREFERCOM = "エイリアスを参照できます。";
$H_ALIASCHANGED = "変更しました。";
$H_ALIASENTRIED = "登録しました。";
$H_ALIASDELETED = "消去しました。";
$H_AORI_ALIAS = "投稿の際、「お名前」の部分に以下の「#....」を入力すると、登録されているお名前とe-mail addr.、URLが自動的に補われます。";
$H_CANNOTQUOTE = "cannot quote specified file";

#
# 引用マーク
#
#	「>」や「&gt;」を引用マークにするのは避けて下さい。
#	トラブルを起こすブラウザが存在します。
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
1;
