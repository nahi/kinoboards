# This file implements Site Specific Definitions of KINOBOARDS.

###
## ○管理者の名前，E-Mailアドレス，システムの名前
#
# 例:
# $MAINT_NAME = 'KinoboardsAdmin';
# $MAINT = 'nakahiro@sarion.co.jp';
# $SYSTEM_NAME = "KINOBOARDS/1.0";
#
$MAINT_NAME = 'YourName';
$MAINT = 'yourname@your.e-mail.domain';
$SYSTEM_NAME = "YourSystemName";

###
## ○タイムゾーン
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

###
## ○システム機能の設定
#
# CGIの実行ログを取りますか?
# インストール直後はログを取ってください．kb.klgに書き出されます．
#   0: 取らない
#   1: 取る（HTMLフォーマット）
#   2: 取る（プレインテキストフォーマット）
$SYS_LOG = 1;

# 書き込み文書タイプとして，どれを許しますか?
# 「そのまま表示」...入力した記事はPREタグで囲まれて表示されます．
# 「HTMLに変換」.....入力した記事はHTMLに変換されて表示されます．
# 「HTMLで入力」.....入力した記事はそのままHTMLとして表示されます．
# 以下からどれか一つを選んでください．
#   $SYS_TEXTTYPE = 1 + 0 + 0;	# 「そのまま表示」
#   $SYS_TEXTTYPE = 0 + 2 + 0;	# 「HTMLに変換」
#   $SYS_TEXTTYPE = 0 + 0 + 4;	# 「HTMLで入力」
#   $SYS_TEXTTYPE = 1 + 2 + 0;	# 「そのまま表示」「HTMLに変換」
#   $SYS_TEXTTYPE = 1 + 0 + 4;	# 「そのまま表示」「HTMLで入力」
#   $SYS_TEXTTYPE = 0 + 2 + 4;	# 「HTMLに変換」「HTMLで入力」
#   $SYS_TEXTTYPE = 1 + 2 + 4;	# 「そのまま表示」「HTMLに変換」「HTMLで入力」
$SYS_TEXTTYPE = 1 + 2 + 4;

# エイリアスを利用しますか?
#   0: 利用しない
#   1: 利用する
#   2: エイリアスを登録しなければ，記事を投稿できないようにする
#   3: HTTP-Cookiesを使う（ユーザ情報をブラウザに覚えさせる）
$SYS_ALIAS = 3;

  # 上で「3: HTTP-Cookiesを使う」に設定した場合，以下も設定してください．
  # HTTP-Cookiesの有効期間をどのように設定しますか?
  #   0: ブラウザ終了時まで
  #   1: 無制限（実際にはThursday, 31-Dec-2029 23:59:59 GMT）
  #   2: n日後まで（nは下で設定します）．
  #   3: 指定日まで（指定日は以下で設定します）．
  $SYS_COOKIE_EXPIRE = 3;

    # 上で「2: n日後まで」に設定した場合は日数を，
    # 「3: 指定日まで」に設定した場合は指定日（時間も）を設定してください．
    # 0もしくは1を選んだ場合はそのままで結構です（指定しても無視されます）．
    $SYS_COOKIE_VALUE = 'Thursday, 31-Dec-98 23:59:59 GMT';
    # 日数の場合．例えば30日間．
    #   $SYS_COOKIE_VALUE = 30;
    # 指定日の場合．例えば1998年年末まで．
    #   $SYS_COOKIE_VALUE = 'Thursday, 31-Dec-98 23:59:59 GMT';

# 記事アイコンを利用しますか?
#   0: 利用しない
#   1: 利用する
$SYS_ICON = 1;

# コマンドアイコンを利用しますか?
#   0: 利用しない(コマンドはテキストで表示する)
#   1: 利用する
#   2: コマンドアイコンと同時にテキストも表示する
$SYS_COMICON = 1;

# 最新の記事いくつに，[new]アイコン（黄色の旗）をつけますか?
# 0を指定すると，この機能を利用しません（[new]アイコンはつかない）
$SYS_NEWICON = 10;		# [記事]

# 新規投稿記事が，上に増えていくか，下に増えていくか(タイトル一覧の時)
#   0: 上
#   1: 下
$SYS_BOTTOMTITLE = 0;

# 新規投稿記事が，上に増えていくか，下に増えていくか(記事一覧の時)
#   0: 上
#   1: 下
$SYS_BOTTOMARTICLE = 1;

# 記事のヘッダにマシン名を表示しますか?
#   0: 表示しない
#   1: 表示する
$SYS_SHOWHOST = 0;

# 記事のヘッダにコマンド群を表示しますか?
#   0: 表示しない
#   1: 表示する
$SYS_COMMAND = 1;

# Subjectに（安全な）タグの入力を許しますか?
#   0: 許さない
#   1: 許す
$SYS_TAGINSUBJECT = 1;

# 記事の許容最大サイズ（バイト数で指定してください; 50K → 51200）
#   0は「記事サイズの制限なし」を意味します．
$SYS_MAXARTSIZE = 0;

# 記事投稿時、メイルアドレスの入力を必須としますか?
#   0: 必須としない
#   1: 必須とする
$SYS_POSTERMAIL = 1;

# サーバのポート番号を表示しますか?
#   0: 表示しない
#   1: (必要ならば)表示する
#      HTTPのデフォルトである80番ポートの場合，1に設定しても表示しません
$SYS_PORTNO = 1;

# 字色とバックグラウンドイメージを使いますか?
#   0: 使わない
#   1: 使う
$SYS_NETSCAPE_EXTENSION = 1;

  # 上で「1: 使う」に設定した場合は，以下も指定してください．
  $BG_IMG = "";
  $BG_COLOR = "#CCCCCC";
  $TEXT_COLOR = "#000000";
  $LINK_COLOR = "#0000AA";
  $ALINK_COLOR = "#FF0000";
  $VLINK_COLOR = "#00AA00";

# 以下の各機能を利用可能としますか?
#   0: 利用できない
#   1: 利用できる
$SYS_F_T = 1;	# リプライ記事のまとめ読みの表示
$SYS_F_N = 1;	# 記事の投稿
$SYS_F_R = 1;	# タイトル一覧(日付順)の表示
$SYS_F_L = 1;	# 最近の記事一覧の表示
$SYS_F_S = 1;	# 記事の検索
$SYS_F_B = 1;	# 掲示板一覧の表示
  #
  # これ以下のコマンドは必ず，
  # 「正しくアクセス制限をかけた上で」利用してください
  # （詳しくはインストレーションマニュアルを参照してください）．
  # でないと破壊的な悪戯を匿名でやられ放題ですからね．
  # [注意] スクリプトの名前を変えたくらいじゃ駄目ですよ．(^_^;
  #
  #   0: 利用できない
  #   1: 利用できる
  $SYS_F_D = 0;	# 記事の削除，訂正
  $SYS_F_MV = 0;	# 記事の「前後順序/元記事-リプライ関係」の変更
  $SYS_F_AM = 0;	# 新着記事到着時のメイル送信先の設定

###
## ○メイル回りの設定
#
# メイル配信サービスを利用しますか? 以下からどれか一つを選んでください．
#   $SYS_MAIL = 0 + 0;		# 利用しない．
#   $SYS_MAIL = 1 + 0;		# 配信メイルのみ使う．
#   $SYS_MAIL = 0 + 2;		# リプライメイルのみ使う．
#   $SYS_MAIL = 1 + 2;		# 配信メイルとリプライメイルの両方を使う．
$SYS_MAIL = 1 + 2;

  # ↑で「利用しない」を指定した場合は，以下は設定の必要はありません．

  # メイルサーバを指定してください．
  #   例: $SMTP_SERVER = 'mail.foo.bar.ne.jp';
  #       $SMTP_SERVER = '123.456.78.90';
  $SMTP_SERVER = 'localhost';

  # 送信するメイルのSubjectに「[掲示板: 番号]」を補いますか?
  #   0: 補わない → 「Subject: 題」（掲示板と記事番号はX-Kb-*に入ります）
  #   1: 補う     → 「Subject: [掲示板: 記事番号] 題」
  $SYS_MAILHEADBRACKET = 1;

  # 送信するメイルのヘッダ「To:」に書かれる宛先を指定してください．
  # 省略すると，送信する相手のメイルアドレスがずらずら並びます．
  # 自動配信機能をメイリングリストのようにして使うなら，
  # $MAILTO_LABEL = 'なひきのぼずユーザ <nakahiro@sarion.co.jp>';
  # などとするといいかもしれません．
  $MAILTO_LABEL = '';

  # 送信するメイルのヘッダ「From:」に書かれる名前を，
  # システム管理者の名前とは変えたい場合に指定してください．
  # 省略すると，このファイルの先頭で設定した$MAINT_NAMEが使われます．
  # $MAILFROM_LABEL = 'Kinoboards Mail Daemon';
  # など．
  $MAILFROM_LABEL = '';

  # CGIが動くサーバ（普通はWWWサーバです．メイルサーバじゃありません）
  # の，OSのタイプに合致する行だけ，先頭の「#」を取り除いてください．
  # OSのタイプは，telnetして「uname -sr」というコマンドでわかります．
  # telnetできない場合，プロバイダもしくは管理者さんに問い合わせてください．
  #
  # 以下を見て頂ければわかる通り，
  # 多くのOSで，$AF_INETを2，$SOCK_STREAMを1に設定します．
  # サーバがSolaris/2.*の人だけ，$SOCK_STREMを2に設定してください．
  #
  $AF_INET = 2; $SOCK_STREAM = 1;	# SunOS 4.*
  # $AF_INET = 2; $SOCK_STREAM = 2;	# SunOS 5.*(Solaris 2.*)
  # $AF_INET = 2; $SOCK_STREAM = 1;	# HP-UX
  # $AF_INET = 2; $SOCK_STREAM = 1;	# AIX
  # $AF_INET = 2; $SOCK_STREAM = 1;	# Linux
  # $AF_INET = 2; $SOCK_STREAM = 1;	# FreeBSD
  # $AF_INET = 2; $SOCK_STREAM = 1;	# IRIX
  # $AF_INET = 2; $SOCK_STREAM = 1;	# WinNT/95
  # $AF_INET = 2; $SOCK_STREAM = 1;	# Mac

  # この他の組み合わせを御存知の方がありましたら，
  # なひ(nakahiro@sarion.co.jp)まで御連絡ください．

###
## ○掲示板一覧の相対URL
#
#  「掲示板一覧へ」でリンクする先を，kbディレクトリからの相対URLで指定します．
#  空ならkbディレクトリへ(よって，一般的にはindex.htmlやindex.shtmlへ)，
#  '-'を指定すると，自分で用意したファイルでなくCGIが自動生成する掲示板一覧へ，
#  それぞれリンクされます．
#
$BOARDLIST_URL = './';			# kbディレクトリへ
# $BOARDLIST_URL = '-';			# CGIが自動生成する掲示板一覧へ
# $BOARDLIST_URL = 'kb10.shtml';	# kb/kb10.shtmlへ

###
## ○各入力項目の大きさ
#
$SUBJECT_LENGTH = 60;		# 題
$TEXT_ROWS = 15;		# 記事行数
$TEXT_COLS = 72;		# 記事幅
$NAME_LENGTH = 60;		# 名前幅
$MAIL_LENGTH = 60;		# E-mail幅
$URL_LENGTH = 72;		# URL幅
$KEYWORD_LENGTH = 60;		# 検索キーワード幅
$DEF_TITLE_NUM = 20;		# タイトル一覧に表示するタイトルの数
				# 0にすると全記事を表示するようになります．
###
## ○出力ページの漢字コード
#
$CHARSET = 'euc';		# 漢字コード変換を行ないません．きのぼずが
				# coreを吐く時には，これに設定してください．
# $CHARSET = 'jis';
# $CHARSET = 'sjis';

###
## ○引用の形態
#
# 引用時，元記事の作者名をつけますか?
#   0: つけない		「 ] 引用元記事．．．」
#   1: つける		「なひ ] 引用元記事．．．」
$SYS_QUOTENAME = 1;
#
# 引用マーク
#   「>」や「&gt;」を引用マークにするのは避けて下さい．
#   トラブルを起こすブラウザが存在します．
$DEFAULT_QMARK = ' ] ';

###
## ○アイコンの大きさ
#
# 一部のブラウザでは，この数値を適当に指定すると，
# 勝手にアイコンの拡大縮小を行なってくれます．
#
# コマンドアイコン(次へ，等)
$COMICON_HEIGHT = 20;		# 高さ[dot]
$COMICON_WIDTH = 20;		# 幅[dot]
# メッセージアイコン(喜怒哀楽，等)
$MSGICON_HEIGHT = 20;		# 高さ[dot]
$MSGICON_WIDTH = 20;		# 幅[dot]

###
## ○URLとして許可するscheme
#
@URL_SCHEME = ('http', 'ftp', 'gopher');

# ○メッセージの宣言
#
$H_BOARD = "掲示板";
$H_ICON = "アイコン";
$H_SUBJECT = "タイトル";
$H_MESG = "メッセージ";
$H_ALIAS = "エイリアス";
$H_FROM = "お名前";
$H_MAIL = "メイル";
$H_HOST = "マシン";
$H_USER = "ユーザ";
$H_URL = "URL";
$H_URL_S = "ホームページのURL(お名前からリンクを張ります; 省略しても構いません)";
$H_DATE = "投稿日";
$H_REPLY = "リプライ";
$H_ORIG = "$H_REPLY元";
$H_ORIG_TOP = "オリジナル";
$H_LINE = "<p>------------------------------</p>";
$H_THREAD = "▼";
$H_NEWARTICLE = "[new!]";

$H_TEXTTYPE = "書き込み形式";
@H_TTLABEL = ( "そのまま表示", "HTMLに変換", "HTMLで入力" );
@H_TTMSG = ( "「$H_TEXTTYPE」を「$H_TTLABEL[0]」にして$H_MESGを書くと，表示の際にそのまま表示されます．", "「$H_TTLABEL[1]」にすると，空行を段落の区切としてHTMLに自動変換します．", "「$H_TTLABEL[2]」にしてHTMLとして書くと，表示の時にHTML整形されます．" );

$H_NOICON = "なし";
$H_BACKBOARD = "$H_BOARD一覧へ";
$H_BACKTITLEREPLY = "$H_SUBJECT一覧へ($H_REPLY順)";
$H_BACKTITLEDATE = "$H_SUBJECT一覧へ(日付順)";	# 空にすると表示されません
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


# $Id: kb.ph,v 5.9 1998-10-22 15:55:52 nakahiro Exp $


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
