# This file implements Site Specific Definitions of KINOBOARDS.

###
## ○管理者の名前，E-Mailアドレス，システムの名前
#
# 例:
# $MAINT_NAME = 'KinoboardsAdmin';
# $MAINT = 'nahi@keynauts.com';
# $SYSTEM_NAME = 'KINOBOARDS/1.0';
#
$MAINT_NAME = 'YourName';
$MAINT = 'yourname@your.e-mail.domain';
$SYSTEM_NAME = 'YourSystemName';

###
## ○タイムゾーン
#
#   'GMT', 'GMT+9'，'GMT-7'などを指定します．
#   通常は後ろ2文字しか意味がないので，'JST+9'でもいいかもしれません．
#   （'JST+9'でないと駄目な環境もあるようです）
#
#   サーバ上のPerlのデフォルトのタイムゾーンをそのまま使う場合は，
#   このまま空('')を指定しておいてください．
#
#   サーバマシンが日本国内に置かれている場合，通常の設定であれば，
#   デフォルトで日本時間用のタイムゾーンになっているはずです．
#   サーバマシンが海外にあり，しかし利用者のほとんどは国内ユーザ，
#   のような場合には，'GMT+9'や'JST+9'を指定して使うと便利でしょう．
#
$TIME_ZONE = '';

###
## ○システム機能の設定
#
# 実行ログのフォーマットを指定してください．
# ログはlogディレクトリに書き出されます．
#   1: 取る（HTMLフォーマット）
#   2: 取る（プレインテキストフォーマット）
#   0: 取らない（推奨しません）
$SYS_LOG = 1;

  # 上でログを取るように設定した場合，以下も設定してください．
  # ログレベルを指定してください．
  #   2: エラーが生じた場合のみ（log/error_logに書き出されます）
  #   1: 通常時もログを取る（log/access_logに書き出されます）
  #   0: 詳細なログを取る（デバッグ時のみ利用してください）
  $SYS_LOGLEVEL = 2;

# アクセス元ホスト名を，記事DBおよび実行ログに残しますか?
#   0: 残さない．
#   1: 残す．
$SYS_LOGHOST = 1;

  # 上で「1: 残す」に設定した場合，以下も設定してください．
  # 記事のヘッダにマシン名を表示しますか?
  #   0: 表示しない
  #   1: 表示する
  $SYS_SHOWHOST = 0;

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
  #   1: 無制限
  #   2: n日後まで（nは下で設定します）．
  #   3: 指定日まで（指定日は以下で設定します）．
  $SYS_COOKIE_EXPIRE = 1;

    # 上で「2: n日後まで」に設定した場合は日数を，
    # 「3: 指定日まで」に設定した場合は指定日（時間も）を設定してください．
    # 0もしくは1を選んだ場合はそのままで結構です（指定しても無視されます）．
    $SYS_COOKIE_VALUE = 'Thursday, 31-Dec-99 23:59:59 GMT';
    # 日数の場合．例えば30日間．
    #   $SYS_COOKIE_VALUE = 30;
    # 指定日の場合．例えば1998年年末まで．
    #   $SYS_COOKIE_VALUE = 'Thursday, 31-Dec-98 23:59:59 GMT';

# 記事アイコンを利用しますか?
#   0: 利用しない
#   1: 利用する
$SYS_ICON = 1;

  # 上で「1: 利用する」に設定した場合は以下も設定してください．
  # アイコン指定を必須にしますか?
  #   0: 必須にする
  #   1: 必須にしない（指定しなくてもよい）
  $SYS_ALLOWNOICON = 1;
  
# 最近の記事に，[new!]アイコン（黄色の旗）をつけますか?
#   0: つけない．
#   1: 最近の記事n個に[new!]アイコンをつける．
#   2: 最近n日間の記事に[new!]アイコンをつける
# 2を指定すると，タイトル表示にかかる時間が他よりほんのり長くなります
# （全実行時間の比較で5%前後）．
$SYS_NEWICON = 2;

  # 上で「1: 最近の記事n個」に設定した場合は記事の個数を，
  # 「2: 最近n日間の記事」に設定した場合は日数を設定してください．
  # 0を選んだ場合はそのままで結構です（指定しても無視されます）．
  $SYS_NEWICON_VALUE = 7;	# [個数] or [日数]

# 新規投稿記事が，デフォルトで上に増えていくか，下に増えていくか
# （タイトル一覧画面）
#   0: 上
#   1: 下
$SYS_BOTTOMTITLE = 0;

# 新規投稿記事が，デフォルトで上に増えていくか，下に増えていくか
# （記事一覧画面）
#   0: 上
#   1: 下
$SYS_BOTTOMARTICLE = 1;

# Subjectにタグの入力を許しますか?
# タグの入力を許しても，安全なタグしか入力できません．
#   0: 許さない
#   1: 許す
$SYS_TAGINSUBJECT = 1;

# 記事投稿時、メイルアドレスの入力を必須としますか?
#   0: 必須としない
#   1: 必須とする
$SYS_POSTERMAIL = 0;

# 記事の許容最大サイズ（バイト数で指定してください; 50K → 51200）
#   0は「記事サイズの制限なし」を意味します．
$SYS_MAXARTSIZE = 51200;

# 同一書き込みフォームからの連続書き込みを禁止しますか?
#   0: 許可する
#   1: 禁止する
$SYS_DENY_FORM_RECYCLE = 1;

# 半日以上前に生成されたフォームからの書き込みを禁止しますか?
#   0: 許可する
#   1: 禁止する
$SYS_DENY_FORM_OLD = 1;

# サーバのポート番号を表示しますか?
#   0: 表示しない
#   1: (必要ならば)表示する
#      HTTPのデフォルトである80番ポートの場合，1に設定しても表示しません
$SYS_PORTNO = 1;

# 記事の上下逆順表示用のリンクを使いますか?
#   0: 表示しない
#   1: 表示する
$SYS_REVERSE = 1;

# 記事のヘッダにコマンド群を表示しますか?
#   0: 表示しない
#   1: 表示する
$SYS_COMMAND = 1;

  # 上で「0: 表示しない」を設定した場合，以下の設定は意味がありません．

  # コマンドアイコンを利用しますか?
  #   0: 利用しない(コマンドはテキストで表示する)
  #   1: 利用する
  #   2: コマンドアイコンと同時にテキストも表示する
  $SYS_COMICON = 1;

  # まとめ読みの際は，各記事のヘッダにコマンド群を表示しますか?
  # 表示しないと見た目はすっきりしますが，
  # 例えば「最近の記事まとめ読み」から直接リプライすることができなくなる，
  # 等の弊害があります．
  #   0: 表示しない
  #   1: 表示する
  $SYS_COMMAND_EACH = 1;

# 書き込み後，まとめ読み時などに表示される移動のためのリンクは，
# リンクで表示しますか? それともボタンで表示しますか?
#   0: リンクで表示する
#   1: ボタンで表示する
$SYS_COMMAND_BUTTON = 1;

# 記事のヘッダにメイルアドレスを表示しますか?
#   0: 表示しない
#   1: （あれば）表示する
$SYS_SHOWMAIL = 1;

# 字色とバックグラウンドイメージを使いますか?
#   0: 使わない
#   1: 使う
$SYS_NETSCAPE_EXTENSION = 1;

  # 上で「1: 使う」に設定した場合は，以下も指定してください．
  $BG_IMG = "";
  $BG_COLOR = "#EEEEEE";
  $TEXT_COLOR = "#000000";
  $LINK_COLOR = "";
  $ALINK_COLOR = "";
  $VLINK_COLOR = "";

# タイトル一覧における，スレッドの表示形式を選んでください．
#
#   0: 1ページに表示するメッセージ数が一定になるように適当にスレッドを切る．
#
#   1: 存在するリプライは全て表示する．
#
#   2: リプライは一切表示せず，先頭のメッセージのみ表示する．
#
$SYS_THREAD_FORMAT = 0;

# 全ページのヘッダに，プルダウンコンボ形式のジャンプメニューを表示しますか?
#   0: 表示しない
#   1: 表示する
$SYS_HEADER_MENU = 1;

# 以下の各機能を利用可能としますか?
#   0: 利用できない
#   1: 利用できる
$SYS_F_T = 1;	# リプライ記事のまとめ読みの表示
$SYS_F_N = 1;	# 記事の投稿
$SYS_F_R = 1;	# タイトル一覧(日付順)の表示
$SYS_F_L = 1;	# 最近の記事一覧の表示
$SYS_F_S = 1;	# 記事の検索
$SYS_F_B = 0;	# 掲示板一覧の表示

  # これ以下のコマンドは必ず，
  # 「正しくアクセス制限をかけた上で」利用してください
  # （詳しくはインストレーションマニュアルを参照してください）．
  # でないと破壊的な悪戯を匿名でやられ放題ですからね．
  # [注意] スクリプトの名前を変えたくらいじゃ駄目ですよ．(^_^;
  #
  #   0: 利用できない
  #   1: 利用できる
  $SYS_F_D = 0;		# 記事の削除，訂正
  $SYS_F_MV = 0;	# 記事の「前後順序/元記事-リプライ関係」の変更
  $SYS_F_AM = 0;	# 新着記事到着時のメイル送信先の設定
  #
  # 記事修正時，修正元記事内のタグを残しますか?
  #   0: 残さない
  #   1: 残す		ブラウザに依っては誤動作するかも．．．
  $SYS_TAGINSUPERSEDE = 1;

###
## ○メイル機能の設定
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
  # $MAILTO_LABEL = 'なひきのぼずユーザ <nahi@keynauts.com>';
  # などとするといいかもしれません．
  $MAILTO_LABEL = '';

  # 送信するメイルのヘッダ「Sender:」に書かれる名前を，
  # システム管理者の名前とは変えたい場合に指定してください．
  # 省略すると，このファイルの先頭で設定した$MAINT_NAMEが使われます．
  # $MAILFROM_LABEL = 'Kinoboards Mail Daemon';
  # など．
  # V1.0R6.3以前は，この値が「From:」に入りましたが，
  # R6.4以降，「From:」ヘッダには記事投稿者が入ります．
  $MAILFROM_LABEL = '';

  # CGIが動くサーバ（普通はWWWサーバです．メイルサーバのことではありません）
  # に合わせて，$AF_INETと$SOCK_STREAMを設定してください．
  # OSのタイプは，telnetして「uname -sr」というコマンドでわかります．
  # telnetできない場合，プロバイダもしくは管理者さんに問い合わせてください．
  #
  # 各OSにおける設定値は，以下を参照してください．
  #   $AF_INET = 2; $SOCK_STREAM = 1;	# SunOS 4.*
  #   $AF_INET = 2; $SOCK_STREAM = 2;	# SunOS 5.*(Solaris 2.*)
  #   $AF_INET = 2; $SOCK_STREAM = 1;	# HP-UX
  #   $AF_INET = 2; $SOCK_STREAM = 1;	# AIX
  #   $AF_INET = 2; $SOCK_STREAM = 2;	# Cobalt OS 2.2(Linux 2.0.33)
  #   $AF_INET = 2; $SOCK_STREAM = 1;	# Linux
  #   $AF_INET = 2; $SOCK_STREAM = 1;	# FreeBSD
  #   $AF_INET = 2; $SOCK_STREAM = 1;	# IRIX
  #   $AF_INET = 2; $SOCK_STREAM = 1;	# WinNT/95
  #   $AF_INET = 2; $SOCK_STREAM = 1;	# Mac with MacPerl
  # この他の組み合わせを御存知の方がありましたら，
  # なひ(nahi@keynauts.com)まで御連絡ください．
  #
  # 上記の通り，多くのOSで，$AF_INETを2，$SOCK_STREAMを1に設定します．
  # サーバがSolaris/2.*もしくはCobaltの人だけ，
  # $SOCK_STREMを2に設定してください．
  #
  $AF_INET = 2;
  $SOCK_STREAM = 1;

###
## ○メイル投稿機能の設定
#
# メイル投稿機能を利用しますか? 利用するためには他にも設定が必要です．
# インストールマニュアルをよく読んでくださいね．
#   0: 利用しない
#   1: 利用する
$SYS_F_POST_STDIN = 0;

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

  # ↑で'-'を指定した場合は，以下も設定してください．

  # 最近書き込まれた掲示板に[new!]アイコンをつけることができます．
  # 何日以内に書き込まれたらアイコンを付けますか?
  # 0を指定するとアイコンを付けません．
  $SYS_BLIST_NEWICON_DATE = 7;	# [日]


###
## ○各入力項目の大きさ
#
$SUBJECT_LENGTH = 60;	# 題
$TEXT_ROWS = 15;	# 記事行数
$TEXT_COLS = 72;	# 記事幅
$NAME_LENGTH = 60;	# 名前幅
$MAIL_LENGTH = 60;	# E-mail幅
$URL_LENGTH = 72;	# URL幅
$KEYWORD_LENGTH = 60;	# 検索キーワード幅
$DEF_TITLE_NUM = 30;	# タイトル一覧に表示するタイトルの数
			# 0にすると全記事を表示するようになります．
$DEF_ARTICLE_NUM = 15;	# まとめ読みする記事の数

###
## ○出力ページの漢字コード
#
$CHARSET = 'euc';	# EUCの場合は漢字コード変換を行ないません．
			# きのぼずがcoreを吐く時には，これに設定してください．
# $CHARSET = 'jis';
# $CHARSET = 'sjis';

###
## ○引用の形態
#
# 引用時，元記事の作者名をつけますか?
#   0: つけない		 ] 引用元記事．．．
#			 ] 引用元記事．．．
#   1: つける		なひ ] 引用元記事．．．
#			なひ ] 引用元記事．．．
$SYS_QUOTENAME = 1;
#
# 引用マーク
#   「>」や「&gt;」を引用マークにするのは避けて下さい．
#   トラブルを起こすブラウザが存在します．
$DEFAULT_QMARK = ' ] ';

###
## ○アイコンの大きさ
#
# IE4やMozillaでは，この数値を指定することにより，
# アイコンの拡大縮小ができます．
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
@URL_SCHEME = ( 'http', 'ftp', 'gopher', 'mailto', 'kb' );

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
$H_THREAD_ALL = "▲";
$H_THREAD = "▼";
$H_NEWARTICLE = "new!";
$H_HR = "<hr>";

$H_TEXTTYPE = "書き込み形式";
@H_TTLABEL = ( "そのまま表示（要改行）", "HTMLに変換（段落タグ挿入）", "HTMLで入力" );
@H_TTMSG = ( "「$H_TEXTTYPE」を「$H_TTLABEL[0]」にして$H_MESGを書くと，表示の際にそのまま表示されます．", "「$H_TTLABEL[1]」にすると，空行を段落の区切としてHTMLに自動変換します．", "「$H_TTLABEL[2]」にしてHTMLとして書くと，表示の時にHTML整形されます．" );

$H_NOICON = "なし";
$H_BACKBOARD = "$H_BOARD一覧へ";
$H_BACKTITLEREPLY = "$H_SUBJECT一覧へ($H_REPLY順)";
$H_BACKTITLEDATE = "$H_SUBJECT一覧へ(日付順)";
$H_PREVARTICLE = "前の$H_MESGへ";
$H_NEXTARTICLE = "次の$H_MESGへ";
$H_POSTNEWARTICLE = "新規に書き込む";
$H_REPLYTHISARTICLE = "$H_REPLYを書き込む";
$H_REPLYTHISARTICLEQUOTE = "引用して$H_REPLYを書き込む";
$H_READREPLYALL = "$H_REPLYをまとめ読み";
$H_DELETE_TITLE = "削除する";
$H_SUPERSEDE_TITLE = "訂正する";
$H_BACKART = "前ページへ";
$H_NEXTART = "次ページへ";
$H_NOBACKART = "前のページはありません．";
$H_NONEXTART = "次のページはありません．";
$H_TOP = "←";
$H_BOTTOM = "→";
$H_REVERSE = "△▽";
$H_NOARTICLE = "該当する$H_MESGがありません．";
$H_SUPERSEDE_ICON = "[※]";
$H_DELETE_ICON = "[×]";
$H_RELINKFROM_MARK = "[←]";
$H_RELINKTO_MARK = "[◎]";
$H_REORDERFROM_MARK = "[△]";
$H_REORDERTO_MARK = "[▽]";


#/////////////////////////////////////////////////////////////////////
1;


# $Id: kb.ph,v 5.21.2.2 2000-02-14 18:22:52 nakahiro Exp $


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
