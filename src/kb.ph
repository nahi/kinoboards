# $Id: kb.ph,v 4.12 1996-11-19 12:08:22 nakahiro Exp $


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
#   0: リプライも含めてすべて
#   1: 新規投稿記事のみ
$SYS_NEWARTICLEONLY = 0;

# ネットスケープ拡張に基づく字色とバックグラウンドイメージを使うか否か
#   0: 使わない
#   1: 使う
$SYS_NETSCAPE_EXTENSION = 1;

# 記事投稿時、メールアドレスの入力を必須とするか
#   0: 必須としない
#   1: 必須とする
$SYS_POSTERMAIL = 1;

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
# Netscape Extensionの指定
#
$BG_IMG = "";
$BG_COLOR = "#66CCCC";
$TEXT_COLOR = "#000000";
$LINK_COLOR = "#0000AA";
$ALINK_COLOR = "#FF0000";
$VLINK_COLOR = "#00AA00";

#
# メッセージの宣言
#
$SYSTEM_NAME = "きのぼーず";

$H_BOARD = "掲示板";
$H_ICON = "アイコン";
$H_SUBJECT = "題";
$H_MESG = "メッセージ";
$H_ALIAS = "エイリアス";
$H_FROM = "お名前";
$H_MAIL = "メールアドレス";
$H_HOST = "マシン";
$H_URL = "URL(省略可)";
$H_DATE = "投稿日";
$H_REPLY = "リプライ";
$H_ORIG = "$H_REPLY元";

$ENTRY_MSG = "$H_MESGの書き込み";
$SHOWICON_MSG = "アイコンの説明";
$PREVIEW_MSG = "書き込みの内容を確認してください";
$THANKS_MSG = "書き込みありがとうございました";
$VIEW_MSG = "タイトル一覧($H_REPLY順)";
$SORT_MSG = "タイトル一覧(日付順)";
$NEWARTICLE_MSG = "最近の$H_MESGをまとめ読み";
$THREADARTICLE_MSG = "$H_REPLYをまとめ読み";
$SEARCHARTICLE_MSG = "$H_MESGの検索";
$ALIASNEW_MSG = "エイリアスの登録/変更/削除";
$ALIASMOD_MSG = "エイリアスが変更されました";
$ALIASDEL_MSG = "エイリアスが削除されました";
$ALIASSHOW_MSG = "エイリアスの参照";
$ERROR_MSG   = "$SYSTEM_NAME: ERROR!";

$H_LINE = "------------------------------";
$H_THREAD = "▼";
$H_FOLLOW = "▼$H_REPLY";
$H_FMAIL = "$H_REPLYがあった時にメールで知らせますか?";

$H_TEXTTYPE = "表示形式";
$H_HTML = "HTMLとして表示する";
$H_PRE = "そのまま表示する";

$H_NOICON = "なし";

# あおり文
$H_REPLYMSG = "上の$H_MESGへの$H_REPLYを書き込む";
$H_AORI = ($SYS_TEXTTYPE)
    ? "$H_SUBJECT，$H_MESG，$H_FROM，$H_MAIL，さらにホームページをお持ちの方は$H_URLを書き込んでください．<strong>$H_MESGはメールと同じように，そのまま書いてくださればOKです</strong>．<br>
ただしHTMLをご存じの方は，「$H_TEXTTYPE」を「$H_HTML」にして，$H_MESGをHTMLとして書いて頂くと，HTML整形を行ないます．"
    : "$H_SUBJECT，$H_MESG，$H_FROM，$H_MAIL，さらにホームページをお持ちの方は$H_URLを書き込んでください．<strong>$H_MESGはメールと同じように，そのまま書いてくださればOKです</strong>．";
$H_SEEICON = "アイコンの説明";
$H_SEEALIAS = "エイリアスの一覧";
$H_ALIASENTRY = "登録する";
$H_ALIASINFO = "「エイリアス」に，$H_FROMと$H_MAIL，$H_URLを登録なさっている方は，「$H_FROM」に「#...」という登録名を書いてください．自動的に$H_FROMと$H_MAIL，$H_URLが補われます．";
$H_PREVIEW_OR_ENTRY = "書き込んだ内容を，";
$H_PREVIEW = "試しに表示してみる(まだ投稿しません)";
$H_ENTRY = "$H_MESGを投稿する";
$H_PUSHHERE_POST = "コマンド実行";
$H_NOTHING = "ありません";
$H_ICONINTRO_ENTRY = "では，次のアイコンを使うことができます．";
$H_ICONINTRO_ARTICLE = "各アイコンは次の機能を表しています．";
$H_POSTINFO = "必要であれば，戻って書き込みを修正してください．よろしければボタンを押して書き込みましょう．";
$H_PUSHHERE_PREVIEW = "投稿する";
$H_THANKSMSG = "書き込みの訂正，取消などは，メールで<a href=\"mailto:$MAINT\">$MAINT</a>まで御連絡ください．";
$H_BACK = "タイトル一覧に戻ります";
$H_NEXTARTICLE = "次の$H_MESGへ";
$H_POSTNEWARTICLE = "新規に投稿する";
$H_REPLYTHISARTICLE = "$H_REPLYを書き込む";
$H_REPLYTHISARTICLEQUOTE = "引用して$H_REPLYを書き込む";
$H_READREPLYALL = "$H_REPLYをまとめ読み";
$H_ARTICLES = "$H_MESG数";
$H_KEYWORD = "キーワード";
$H_SEARCHKEYWORD = "検索する";
$H_RESETKEYWORD = "リセットする";
$H_SEARCHTARGET = "検索範囲";
$H_SEARCHTARGETSUBJECT = "題";
$H_SEARCHTARGETPERSON = "名前";
$H_SEARCHTARGETARTICLE = "メッセージ";
$H_INPUTKEYWORD = "<p>
<ul>
<li>「$H_SEARCHTARGETSUBJECT」，「$H_SEARCHTARGETPERSON」，「$H_SEARCHTARGETARTICLE」の中から，検索する範囲をチェックしてください．
指定された範囲で，$H_KEYWORDを含む$H_MESGを一覧表示します．
<li>$H_KEYWORDには，大文字小文字の区別はありません．
<li>$H_KEYWORDを半角スペースで区切って，複数の$H_KEYWORDを指定すると，
それら全てを含む$H_MESGのみを検索することができます．
<li>アイコンで検索する場合は，
「アイコン」をチェックした後，探したい$H_MESGのアイコンを選んでください．
</ul>
</p>";
$H_NOTFOUND = "該当する$H_MESGは見つかりませんでした．";
$H_ALIASTITLE = "新規登録/登録内容の変更";
$H_ALIASNEWCOM = "エイリアスの新規登録/登録内容の変更を行ないます．ただし悪戯防止のため，変更は，登録の際と同じマシンでなければできません．変更できない場合は，<a href=\"mailto:$MAINT\">$MAINT</a>までメールでお願いします．";
$H_ALIASNEWPUSH = "登録/変更する";
$H_ALIASDELETE = "削除";
$H_ALIASDELETECOM = "上記エイリアスを削除します．同じく登録の際と同じマシンでなければ削除できません．";
$H_ALIASDELETEPUSH = "削除する";
$H_ALIASREFERPUSH = "エイリアス一覧を参照する";
$H_ALIASCHANGED = "変更しました．";
$H_ALIASENTRIED = "登録しました．";
$H_ALIASDELETED = "消去しました．";
$H_AORI_ALIAS = "投稿の際，「$H_FROM」の部分に以下の登録名(「#....」)を入力すると，登録されている$H_FROMと$H_MAIL，$H_URLが自動的に補われます．";
$H_BACKART = "以前に書き込まれた$H_MESGへ";
$H_NEXTART = "以降に書き込まれた$H_MESGへ";
$H_TOP = "↑";
$H_BOTTOM = "↓";
$H_NOARTICLE = "該当する記事がありません．";


#/////////////////////////////////////////////////////////////////////
1;
