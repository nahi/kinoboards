# $Id: kb.ph,v 4.7 1996-08-05 18:41:44 nakahiro Exp $


# KINOBOARDS: Kinoboards Is Network Opened BOARD System
# Copyright (C) 1995, 96 NAKAMURA Hiroshi.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PRATICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.


# This file implements Site Specific Definitions of KINOBOARDS.


#
# 管理者の名前とe-mail addr.
#
$MAINT_NAME = 'KinoAdmin';
$MAINT = 'nakahiro@kinotrope.co.jp';

#
# sendmailのパスとオプション
#
$MAIL2 = '/usr/lib/sendmail -oi -t';

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

# アイコンを利用するか否か
#   0: 利用しない
#   1: 利用する
$SYS_ICON = 1;

# 新規投稿記事が，上に増えていくか，下に増えていくか(タイトル一覧の時)
#   0: 上
#   1: 下
$SYS_BOTTOMTITLE = 0;

# 新規投稿記事が，上に増えていくか，下に増えていくか(記事一覧の時)
#   0: 上
#   1: 下
$SYS_BOTTOMARTICLE = 1;

# メール送信サービスを利用するか否か(日本語のみ)
#   0: 利用しない
#   1: 利用する
$SYS_FOLLOWMAIL = 1;

# 記事のヘッダにマシン名を表示するか否か
#   0: 表示しない
#   1: 表示する
$SYS_SHOWHOST = 1;

# 記事のヘッダにコマンド群を表示するか否か
#   0: 表示しない
#   1: 表示する
$SYS_COMMAND = 1;

# タイトルリストに新規投稿記事のみを表示するか否か
#   0: 反応も含めてすべて
#   1: 新規投稿記事のみ
$SYS_NEWARTICLEONLY = 0;

#
# 引用マーク
#
#	「>」や「&gt;」を引用マークにするのは避けて下さい．
#	トラブルを起こすブラウザが存在します．
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
# タイトル一覧に表示するタイトルの数
#
$DEF_TITLE_NUM = 20;

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

$ENTRY_MSG = "記事の書き込み";
$SHOWICON_MSG = "アイコンの説明";
$PREVIEW_MSG = "書き込みの内容を確認して下さい";
$THANKS_MSG = "書き込みありがとうございました";
$VIEW_MSG = "タイトル一覧(応答順)";
$SORT_MSG = "タイトル一覧(日付順)";
$NEWARTICLE_MSG = "記事をまとめて読む";
$THREADARTICLE_MSG = "反応をまとめて読む";
$SEARCHARTICLE_MSG = "記事の検索";
$ALIASNEW_MSG = "エイリアスの登録/変更/削除";
$ALIASMOD_MSG = "エイリアスが変更されました";
$ALIASDEL_MSG = "エイリアスが削除されました";
$ALIASSHOW_MSG = "エイリアスの参照";
$DELETE_ENTRY_MSG = "記事の削除";
$DELETE_PREVIEW_MSG = "削除する記事の確認";
$DELETE_THANKS_MSG = "記事の削除";
$ERROR_MSG   = "$SYSTEM_NAME: ERROR!";

$H_LINE = "------------------------------";
$H_THREAD = "▼";
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
$H_ID = "記事番号:";
$H_FOLLOW = "▼反応";
$H_FMAIL = "反応がついた時にメールで知らせる:";

$H_TEXTTYPE = "表示形式:";
$H_HTML = "HTMLとして表示する";
$H_PRE = "そのまま表示する";

$H_NOICON = "なし";

# あおり文
$H_REPLYMSG = "上の記事に反応する";
$H_AORI = "題，記事，お名前，メールアドレス，さらにホームページをお持ちの方はURL(省略可)を書き込んでください．<strong>記事はそのまま，メールと同じように書いてくださればOKです</strong>．<br>ただし，HTMLをご存じの方は，「$H_TEXTTYPE」を「$H_HTML」にしてHTMLとして書いて頂くと，HTML整形を行ないます．";
$H_SEEICON = "アイコンの説明";
$H_SEEALIAS = "エイリアスを見る";
$H_ALIASENTRY = "登録する";
$H_ALIASINFO = "エイリアスに登録されている方は，「$H_FROM」に「#...」と書けば，名前やメール，URLを省略できます．";
$H_PREVIEW_OR_ENTRY = "書き込んだ内容を，";
$H_PREVIEW = "試しに表示してみる(まだ投稿しません)";
$H_ENTRY = "記事として投稿する";
$H_PUSHHERE = "ここを押してください";
$H_NOTHING = "ありません";
$H_ICONINTRO_ENTRY = "では，次の記事アイコンを使うことができます．";
$H_ICONINTRO_ARTICLE = "各アイコンは次の機能を表しています．";
$H_POSTINFO = "必要であれば，戻って書き込みを修正して下さい．よろしければボタンを押して書き込みましょう．";
$H_THANKSMSG = "書き込みの訂正，取消などはメールでお願いいたします．";
$H_BACK = "戻る";
$H_COMMAND = "実行";
$H_TITLELIST = "記事一覧へ";
$H_NEXTARTICLE = "次の記事へ";
$H_POSTNEWARTICLE = "新規に投稿する";
$H_REPLYTHISARTICLE = "この記事に反応する";
$H_REPLYTHISARTICLEQUOTE = "引用して反応する";
$H_READREPLYALL = "これまでの反応を見る";
$H_ARTICLES = "記事数";
$H_JUMPID = "↑の数字をクリックすると，そのIDの記事に飛びます．新しい記事ほど上の方にあります．";
$H_KEYWORD = "キーワード";
$H_INPUTKEYWORD = "<p>
<ul>
<li>「題」，「名前」，「本文」の中から，検索する範囲をチェックしてください．
指定された範囲で，$H_KEYWORDを含む記事を一覧表示します．
<li>$H_KEYWORDには，大文字小文字の区別はありません．
<li>$H_KEYWORDを半角スペースで区切って，複数の$H_KEYWORDを指定すると，
それら全てを含む記事のみを検索することができます．
<li>アイコンで検索する場合は，
「アイコン」をチェックした後，探したい記事のアイコンを選んでください．
</ul>
</p>";
$H_SEARCHKEYWORD = "検索する";
$H_RESETKEYWORD = "リセットする";
$H_SEARCHTARGET = "検索範囲";
$H_SEARCHTARGETSUBJECT = "題";
$H_SEARCHTARGETPERSON = "名前";
$H_SEARCHTARGETARTICLE = "本文";
$H_NOTFOUND = "該当する記事は見つかりませんでした．";
$H_ALIASTITLE = "新規登録/登録内容の変更";
$H_ALIASNEWCOM = "エイリアスの新規登録/登録内容の変更を行ないます．ただし変更は，登録の際と同じマシンでなければできません．変更できない場合は，<a href=\"mailto:$MAINT\">$MAINT</a>までメールでお願いします．";
$H_ALIASNEWPUSH = "登録/変更する";
$H_ALIASDELETE = "削除";
$H_ALIASDELETECOM = "上記エイリアスを削除します．同じく登録の際と同じマシンでなければ削除できません．";
$H_ALIASDELETEPUSH = "削除する";
$H_ALIASREFERPUSH = "エイリアスを参照する";
$H_ALIASCHANGED = "変更しました．";
$H_ALIASENTRIED = "登録しました．";
$H_ALIASDELETED = "消去しました．";
$H_DELETE_ENTRY_TITLE = "削除する記事の記事番号を入力して下さい";
$H_DELETE_COM = "記事の削除は，投稿したマシンと同じマシンからでないとできません．";
$H_DELETE_PREVIEW_COM = "削除する記事を確認して下さい．ボタンを押すと削除します．";
$H_AORI_ALIAS = "投稿の際，「お名前」の部分に以下の「#....」を入力すると，登録されているお名前とe-mail addr.，URLが自動的に補われます．";
$H_CANNOTQUOTE = "指定された記事は引用できません．";
$H_BACKART = "以前に書き込まれた記事へ";
$H_NEXTART = "以降に書き込まれた記事へ";
$H_TOP = "↑";
$H_BOTTOM = "↓";
$H_NOARTICLE = "該当する記事がありません．";


#/////////////////////////////////////////////////////////////////////
1;
