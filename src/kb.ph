# $Id: kb.ph,v 4.17 1997-03-13 15:18:21 nakahiro Exp $


# KINOBOARDS: Kinoboards Is Network Opened BOARD System
# Copyright (C) 1995, 96, 97 NAKAMURA Hiroshi.
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
# メイル送信に使うため，「$MAINT_NAME」はアルファベットのみで指定してください．
#
$MAINT_NAME = 'KinoAdmin';
$MAINT = 'nakahiro@kinotrope.co.jp';

#
# サーバが動いているマシンはどれですか?
# 該当する1行を残してコメントアウトしてください．
#
 $ARCH = 'UNIX';			# UNIX + Perl4/5
# $ARCH = 'WinNT';			# WinNT + Perl5
# $ARCH = 'Win95';			# Win95 + Perl5
# $ARCH = 'Mac';			# Mac + MacPerl

#
# UNIXの場合はsendmailのパスとオプションを，
# Macの場合はSMTP serverの動いているマシンのホスト名を，
# Winの場合はメイルを放り込むファイルを，
# 指定してください．
#
$MAIL2 = '/usr/lib/sendmail -oi -t'	if ($ARCH eq 'UNIX');
$MAIL2 = 'SendMail'			if ($ARCH eq 'WinNT');
$MAIL2 = 'SendMail'			if ($ARCH eq 'Win95');
$MAIL2 = 'foo.bar.baz.co.jp'		if ($ARCH eq 'Mac');
#
# MacPerlでメイル送信機能を用いるには，
# <URL:ftp://mors.gsfc.nasa.gov/pub/MacPerl/Scripts/>
# に置かれている，MacPerl用のlibnetが必要です．
# 詳しくはdoc/INSTALL.htmlを御覧ください．
#
# Winの場合，今のところメイル送信機能がありません．
# メイルはすべて，上で指定した名前のファイルに書き出されます．
# 一応，1日1回，そのファイルを適当に分割し，
# 手動で送信するという手もありますね．(^_^;
# WinNTにはsendmailがあるはずなので，いつかは対応したい……
#

#
# スクリプトのメインの漢字コード(EUCじゃなきゃ動きません)
#
$SCRIPT_KCODE = 'euc';

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

# 記事アイコンを利用するか否か
#   0: 利用しない
#   1: 利用する
$SYS_ICON = 1;

# コマンドアイコンを利用するか否か
#   0: 利用しない
#   1: 利用する
$SYS_COMICON = 1;

# 新規投稿記事が，上に増えていくか，下に増えていくか(タイトル一覧の時)
#   0: 上
#   1: 下
$SYS_BOTTOMTITLE = 0;

# 新規投稿記事が，上に増えていくか，下に増えていくか(記事一覧の時)
#   0: 上
#   1: 下
$SYS_BOTTOMARTICLE = 1;

# 自動メイル配信サービスを利用するか否か
#   0: 利用しない
#   1: 利用する
$SYS_MAIL = 1;

# 記事のヘッダにマシン名を表示するか否か
#   0: 表示しない
#   1: 表示する
$SYS_SHOWHOST = 0;

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

# 記事投稿時、メイルアドレスの入力を必須とするか
#   0: 必須としない
#   1: 必須とする
$SYS_POSTERMAIL = 1;

#
# 引用マーク
#
#	「>」や「&gt;」を引用マークにするのは避けて下さい．
#	トラブルを起こすブラウザが存在します．
#
$DEFAULT_QMARK = ' ] ';

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
# URLとして許可するscheme
#
@URL_SCHEME = ('http', 'ftp', 'gopher');

#
# メッセージの宣言
#
$SYSTEM_NAME = "きのぼーず";

$H_BOARD = "掲示板";
$H_ICON = "アイコン";
$H_SUBJECT = "タイトル";
$H_MESG = "メッセージ";
$H_ALIAS = "エイリアス";
$H_FROM = "お名前";
$H_MAIL = "メイル";
$H_HOST = "マシン";
$H_URL = "URL";
$H_URL_S = "URL(省略可)";
$H_DATE = "投稿日";
$H_REPLY = "リプライ";
$H_ORIG = "$H_REPLY元";
$H_ORIG_TOP = "オリジナル";

$ENTRY_MSG = "$H_MESGの書き込み";
$SHOWICON_MSG = "アイコンの説明";
$PREVIEW_MSG = "書き込みの内容を確認してください";
$THANKS_MSG = "書き込みありがとうございました";
$VIEW_MSG = "$H_SUBJECT一覧($H_REPLY順)";
$SORT_MSG = "$H_SUBJECT一覧(日付順)";
$NEWARTICLE_MSG = "最近の$H_MESGをまとめ読み";
$THREADARTICLE_MSG = "$H_REPLYをまとめ読み";
$SEARCHARTICLE_MSG = "$H_MESGの検索";
$ALIASNEW_MSG = "$H_ALIASの登録/変更/削除";
$ALIASMOD_MSG = "$H_ALIASが設定されました";
$ALIASDEL_MSG = "$H_ALIASが削除されました";
$ALIASSHOW_MSG = "$H_ALIASの参照";
$ERROR_MSG   = "$SYSTEM_NAME: ERROR!";

$H_LINE = "------------------------------";
$H_THREAD = "▼";
$H_FOLLOW = "▼$H_REPLY";
$H_TEXTTYPE = "表示形式";
$H_HTML = "HTMLとして表示する";
$H_PRE = "そのまま表示する";
$H_NOICON = "なし";

# あおり文
$H_REPLYMSG = "上の$H_MESGへの$H_REPLYを書き込む";
$H_AORI_1 = "$H_SUBJECT，$H_MESG，$H_FROM，$H_MAIL，さらにウェブページをお持ちの方は，ホームページの$H_URLを書き込んでください．";
$H_AORI_2 = "HTMLをご存じの方は，「$H_TEXTTYPE」を「$H_HTML」にして，$H_MESGをHTMLとして書いて頂くと，表示の時にHTML整形を行ないます．";
$H_SEEICON = "アイコンの説明";
$H_SEEALIAS = "$H_ALIASの一覧";
$H_ALIASENTRY = "登録する";
$H_ALIASINFO = "「$H_ALIAS」に，$H_FROMと$H_MAIL，$H_URLを登録なさっている方は，「$H_FROM」に「#...」という登録名を書いてください．自動的に$H_FROMと$H_MAIL，$H_URLが補われます．";
$H_FMAIL = "$H_REPLYがあった時にメイルで知らせますか?";
$H_LINK = "$H_MESG中に関連ウェブページへのリンクを張る場合は，「&lt;URL:http://〜&gt;」のように，URLを「&lt;URL:」と「&gt;」で囲んで書き込んでください．自動的にリンクが張られます．";
$H_PREVIEW_OR_ENTRY = "書き込んだ内容を，";
$H_PREVIEW = "試しに表示してみる(まだ投稿しません)";
$H_ENTRY = "$H_MESGを投稿する";
$H_PUSHHERE_POST = "コマンド実行";
$H_NOTHING = "ありません";
$H_ICONINTRO_ENTRY = "では，次のアイコンを使うことができます．";
$H_ICONINTRO_ARTICLE = "各アイコンは次の機能を表しています．";
$H_POSTINFO = "必要であれば，ブラウザのBACKボタンで戻って，書き込みを修正してください．よろしければボタンを押して書き込みましょう．";
$H_DIRECTLINK = "($H_MESGはありません．$H_SUBJECT一覧からは，直接以下のURLにリンクが張られます．リンク先が正しいことを確認してください．)";
$H_PUSHHERE_PREVIEW = "投稿する";
$H_THANKSMSG = "書き込みの訂正，取消などは，メイルで<a href=\"mailto:$MAINT\">$MAINT</a>まで御連絡ください．";
$H_BACKTITLE = "$H_SUBJECT一覧へ";
$H_BACKORG = "$H_ORIGの$H_MESGへ";
$H_PREVARTICLE = "前の$H_MESGへ";
$H_NEXTARTICLE = "次の$H_MESGへ";
$H_POSTNEWARTICLE = "新規に書き込む";
$H_REPLYTHISARTICLE = "$H_REPLYを書き込む";
$H_REPLYTHISARTICLEQUOTE = "引用して$H_REPLYを書き込む";
$H_READREPLYALL = "$H_REPLYをまとめ読み";
$H_ARTICLES = "$H_MESG数";
$H_KEYWORD = "キーワード";
$H_SEARCHKEYWORD = "検索する";
$H_RESET = "リセットする";
$H_SEARCHTARGET = "検索範囲";
$H_SEARCHTARGETSUBJECT = "$H_SUBJECT";
$H_SEARCHTARGETPERSON =  "名前";
$H_SEARCHTARGETARTICLE = "$H_MESG";
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
$H_FOUNDNO = "件の$H_MESGが見つかりました．";
$H_ALIASTITLE = "新規登録/登録内容の変更";
$H_ALIASNEWCOM = "$H_ALIASの新規登録/登録内容の変更を行ないます．ただし悪戯防止のため，変更は，登録の際と同じマシンでなければできません．変更できない場合は，<a href=\"mailto:$MAINT\">$MAINT</a>までメイルでお願いします．";
$H_ALIASNEWPUSH = "登録/変更する";
$H_ALIASDELETE = "削除";
$H_ALIASDELETECOM = "上記$H_ALIASを削除します．同じく登録の際と同じマシンでなければ削除できません．";
$H_ALIASDELETEPUSH = "削除する";
$H_ALIASREFERPUSH = "$H_ALIAS一覧を参照する";
$H_ALIASCHANGED = "設定しました．";
$H_ALIASENTRIED = "登録しました．";
$H_ALIASDELETED = "消去しました．";
$H_AORI_ALIAS = "投稿の際，「$H_FROM」の部分に以下の登録名(「#....」)を入力すると，登録されている$H_FROMと$H_MAIL，$H_URLが自動的に補われます．";
$H_BACKART = "以前に書き込まれた$H_MESGへ";
$H_NEXTART = "以降に書き込まれた$H_MESGへ";
$H_TOP = "↑";
$H_BOTTOM = "↓";
$H_NOARTICLE = "該当する$H_MESGがありません．";


#/////////////////////////////////////////////////////////////////////
1;
