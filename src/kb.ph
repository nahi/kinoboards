# $Id: kb.ph,v 5.2 1997-11-26 09:39:13 nakahiro Rel $


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
# 管理者の名前，E-Mailアドレス，システムの名前
#
# メイル送信にも使います．
# 「$MAINT_NAME」はアルファベットのみで指定してください．
# メイルが文字化けするようなら，
# 「$SYSTEM_NAME」もアルファベットのみにしてください．
#
# 例:
#$MAINT_NAME = 'KinoboardsAdmin';
#$MAINT = 'nakahiro@kinotrope.co.jp';
#$SYSTEM_NAME = "(c)KINOBOARDS";
#
$MAINT_NAME = 'YourName';
$MAINT = 'yourname@your.e-mail.domain';
$SYSTEM_NAME = "YourSystemName";

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
# タイムゾーン
#
#   'GMT', 'GMT+9'，'GMT-7'などを指定します．
#
#   Perlインストール時のデフォルトのタイムゾーンをそのまま使う場合は，
#   このまま空('')を指定しておいてください．
#
#   サーバマシンが日本国内に置かれている場合，通常の設定であれば，
#   デフォルトで日本時間用のタイムゾーンになっているはずです．
#
#   サーバマシンが海外にあり，しかし利用者のほとんどは国内ユーザ，
#   のような場合には，'GMT+9'を指定して使うと便利でしょう．
#
$TIME_ZONE = '';

#
# システムの設定
#
# CGIの実行ログを取るか（インストール直後はログを取るようにしてください）
#   0: 取らない
#   1: 取る（kb.klgというファイルにログが書かれます）
$SYS_LOG = 1;

# 入力文書タイプ(HTML or PLAIN)の選択を行うか否か(行なわないとPREのみ)
#   0: 行わない
#   1: 行う
$SYS_TEXTTYPE = 1;

# エイリアスを利用するか否か
#   0: 利用しない
#   1: 利用する
#   2: エイリアスを登録しなければ，記事を投稿できないようにする
$SYS_ALIAS = 1;

# 記事アイコンを利用するか否か
#   0: 利用しない
#   1: 利用する
$SYS_ICON = 1;

# コマンドアイコンを利用するか否か
#   0: 利用しない(コマンドはテキストで表示する)
#   1: 利用する
#   2: コマンドアイコンと同時にテキストも表示する
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

# 記事の許容最大サイズ（バイト数で指定してください; 50K → 51200）
#   0は「記事サイズの制限なし」を意味します．
$SYS_MAXARTSIZE = 0;

# ネットスケープ拡張に基づく字色とバックグラウンドイメージを使うか否か
#   0: 使わない
#   1: 使う
$SYS_NETSCAPE_EXTENSION = 1;

# 記事投稿時、メイルアドレスの入力を必須とするか
#   0: 必須としない
#   1: 必須とする
$SYS_POSTERMAIL = 1;

# サーバのポート番号を表示するか否か
#   0: 表示しない
#   1: (必要ならば)表示する
#      HTTPのデフォルトである80番ポートの場合，1に設定しても表示しません
$SYS_PORTNO = 1;

# 各機能を利用可能とするか否か
#   0: 利用できない
#   1: 利用できる
$SYS_F_T = 1;			# リプライ記事のまとめ読みの表示
$SYS_F_N = 1;			# 記事の投稿
$SYS_F_R = 1;			# タイトル一覧(日付順)の表示
$SYS_F_L = 1;			# 最近の記事一覧の表示
$SYS_F_S = 1;			# 記事の検索
$SYS_F_B = 1;			# 掲示板一覧の表示
#
# これ以下のコマンドは必ず，
# 「正しくアクセス制限をかけた上で」利用してください．
# でないと破壊的な悪戯を匿名でやられ放題ですからね．
#
# [注意] スクリプトの名前を変えたくらいじゃ絶対に駄目です．
#
$SYS_F_D = 0;			# 記事の削除，訂正
$SYS_F_MV = 0;			# 記事の「前後順序/元記事-リプライ関係」の変更
$SYS_F_AM = 0;			# 新着記事到着時のメイル送信先の設定

#
# 掲示板一覧の相対URL
#
#  「掲示板一覧へ」でリンクする先を，kbディレクトリからの相対URLで指定します．
#  空ならkbディレクトリへ(よって，一般的にはindex.htmlやindex.shtmlへ)，
#  '-'を指定すると，自分で用意したファイルでなくCGIが自動生成する掲示板一覧へ，
#  それぞれリンクされます．
#
# $BOARDLIST_URL = '';			# kbディレクトリへ
# $BOARDLIST_URL = '-';			# CGIが自動生成する掲示板一覧へ
$BOARDLIST_URL = 'kb10.shtml';		# kb/kb10.shtmlへ

#
# 引用マーク
#
#	「>」や「&gt;」を引用マークにするのは避けて下さい．
#	トラブルを起こすブラウザが存在します．
#
$DEFAULT_QMARK = ' ] ';

#
# アイコンの大きさ
# 一部のブラウザでは，この数値を適当に指定すると，
# 勝手にアイコンの拡大縮小を行なってくれるようです．
#
# コマンドアイコン(次へ，等)
$COMICON_HEIGHT = 20;
$COMICON_WIDTH = 20;
# メッセージアイコン(喜怒哀楽，等)
$MSGICON_HEIGHT = 20;
$MSGICON_WIDTH = 20;

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

# タイトル一覧に表示するタイトルの数
# 0にすると全記事を表示するようになります．
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
$H_BOARD = "掲示板";
$H_ICON = "アイコン";
$H_SUBJECT = "タイトル";
$H_MESG = "メッセージ";
$H_ALIAS = "エイリアス";
$H_FROM = "お名前";
$H_MAIL = "メイル";
$H_HOST = "マシン";
$H_USER = "投稿者";		# エイリアス登録でないと書き込みできない場合
$H_URL = "URL";
$H_URL_S = "URL(省略可)";
$H_DATE = "投稿日";
$H_REPLY = "リプライ";
$H_ORIG = "$H_REPLY元";
$H_ORIG_TOP = "オリジナル";
$H_LINE = "<p>------------------------------</p>";
$H_THREAD = "▼";
$H_TEXTTYPE = "表示形式";
$H_HTML = "HTMLとして表示する";
$H_PLAIN = "そのまま表示する";
$H_NOICON = "なし";
$H_BACKBOARD = "$H_BOARD一覧へ";
$H_BACKTITLE = "$H_SUBJECT一覧へ";
$H_PREVARTICLE = "前の$H_MESGへ";
$H_NEXTARTICLE = "次の$H_MESGへ";
$H_POSTNEWARTICLE = "新規に書き込む";
$H_REPLYTHISARTICLE = "$H_REPLYを書き込む";
$H_REPLYTHISARTICLEQUOTE = "引用して$H_REPLYを書き込む";
$H_READREPLYALL = "$H_REPLYをまとめ読み";
$H_DELETE_TITLE = "削除する";
$H_SUPERSEDE_TITLE = "訂正する";
$H_BACKART = "以前に書き込まれた$H_MESGへ";
$H_NEXTART = "以降に書き込まれた$H_MESGへ";
$H_TOP = "↑";
$H_BOTTOM = "↓";
$H_NOARTICLE = "該当する$H_MESGがありません．";
$H_SUPERSEDE_ICON = "[※]";
$H_DELETE_ICON = "[×]";
$H_RELINKFROM_MARK = "[←]";
$H_RELINKTO_MARK = "[◎]";
$H_REORDERFROM_MARK = "[△]";
$H_REORDERTO_MARK = "[▽]";


#/////////////////////////////////////////////////////////////////////
1;
