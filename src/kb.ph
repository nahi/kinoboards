# This file implements Site Specific Definitions of KINOBOARDS.

###
## ○管理者のユーザ名，E-Mailアドレス，ウェブページURL，システムの名前
#
# 例:
# $MAINT_NAME = 'KinoboardsAdmin';
# $MAINT = 'nahi@keynauts.com';
# $MAINT_URL = 'http://www.jin.gr.jp/~nahi/';
# $SYSTEM_NAME = 'KINOBOARDS/1.0';
#
$MAINT_NAME = 'YourName';
$MAINT = 'yourname@your.e-mail.domain';
$MAINT_URL = '';		# 空でも可
$SYSTEM_NAME = 'YourSystemName';

###
## ○ユーザ認証機能
#
# 認証を行いますか?
#   0: 行わない（管理者権限の必要な各種機能が使えなくなります）
#   1: HTTP-Cookiesによる認証を行う
#   2: HTTPサーバによる認証を使う
#   3: URLによる認証を行う
$SYS_AUTH = 1;  # 現在は2を指定することができません．．．

  # 認証を行なうように指定した場合，以下も指定してください．
  # 認証用ファイル（kb.user）を置くディレクトリを指定してください．
  # デフォルト設定のままだとkbディレクトリに置かれます．
  # これだと直接URLを入力すればダイジェスト化されたパスワードが見えてしまい，
  # オフラインブルートフォースアタックに使われてしまいます．
  # 極力，ウェブに公開されていないディレクトリを設定してください．
  #   $AUTH_DIR = '/home/nahi/etc';
  $AUTH_DIR = '.';

  # 一般登録ユーザの権限は? 以下からどれか一つを選んでください．
  #   $USER_POLICY = 0 + 0;       # 読み×・書き×←たぶん意味なし(^_^;
  #   $USER_POLICY = 1 + 0;       # 読み○・書き×
  #   $USER_POLICY = 0 + 2;       # 読み×・書き○←たぶん意味なし(^_^;
  #   $USER_POLICY = 1 + 2;       # 読み○・書き○
  $USER_POLICY = 1 + 2;

  # ゲストユーザの権限は? 以下からどれか一つを選んでください．
  #   $GUEST_POLICY = 0 + 0;      # 読み×・書き×
  #   $GUEST_POLICY = 1 + 0;      # 読み○・書き×
  #   $GUEST_POLICY = 0 + 2;      # 読み×・書き○←たぶん意味なし(^_^;
  #   $GUEST_POLICY = 1 + 2;      # 読み○・書き○
  $GUEST_POLICY = 1 + 2;

  # 先に「1: HTTP-Cookiesによる認証を行う」に設定した場合，
  # 以下も設定してください．
  # HTTP-Cookiesの有効期間をどのように設定しますか?
  #   0: ブラウザ終了時まで
  #   1: 無制限
  #   2: n日後まで（nは下で設定します）．
  #   3: 指定日まで（指定日は以下で設定します）．
  $SYS_COOKIE_EXPIRE = 1;

    # 上で「2: n日後まで」に設定した場合は日数を，
    # 「3: 指定日まで」に設定した場合は指定日（時間も）を設定してください．
    # 0もしくは1を選んだ場合はそのままで結構です（指定しても無視されます）．
    $SYS_COOKIE_VALUE = 0;
    # 日数の場合．例えば30日間．
    #   $SYS_COOKIE_VALUE = 30;
    # 指定日の場合．例えば1998年年末まで．
    #   $SYS_COOKIE_VALUE = 'Thursday, 31-Dec-98 23:59:59 GMT';

  # ユーザによる，本人が書き込んだメッセージの訂正/削除を許可しますか?
  #   0: 許可しない．
  #   1: リプライがついてなければ許可する．
  #   2: リプライがついていても訂正/削除でき（お勧めしません）
  $SYS_OVERWRITE = 1;

  # メッセージ修正時，修正元メッセージ内のタグを残しますか?
  #   0: 残さない
  #   1: 残す
  $SYS_TAGINSUPERSEDE = 1;

  # 「新着メッセージ」を書き込めるのは管理者だけ，にもできます．
  # 「リプライメッセージ」の書き込み権限には影響を与えません．
  #   0: そのまま
  #   1: 管理者のみが「新着」を書き込める
  $SYS_NEWART_ADMINONLY = 0;

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

# アクセス元ホスト名を，メッセージDBおよび実行ログに残しますか?
#   0: 残さない．
#   1: 残す．
$SYS_LOGHOST = 1;

  # 上で「1: 残す」に設定した場合，以下も設定してください．
  # メッセージのヘッダにマシン名を表示しますか?
  #   0: 表示しない
  #   1: 表示する
  $SYS_SHOWHOST = 0;

# 書き込み文書タイプとして，どれを許しますか?
# 「そのまま表示」...入力したメッセージはPREタグで囲まれて表示されます．
# 「HTMLに変換」.....入力したメッセージはHTMLに変換されて表示されます．
# 「HTMLで入力」.....入力したメッセージはそのままHTMLとして表示されます．
# 以下からどれか一つを選んでください．
#   $SYS_TEXTTYPE = 1 + 0 + 0;	# 「そのまま表示」
#   $SYS_TEXTTYPE = 0 + 2 + 0;	# 「HTMLに変換」
#   $SYS_TEXTTYPE = 0 + 0 + 4;	# 「HTMLで入力」
#   $SYS_TEXTTYPE = 1 + 2 + 0;	# 「そのまま表示」「HTMLに変換」
#   $SYS_TEXTTYPE = 1 + 0 + 4;	# 「そのまま表示」「HTMLで入力」
#   $SYS_TEXTTYPE = 0 + 2 + 4;	# 「HTMLに変換」「HTMLで入力」
#   $SYS_TEXTTYPE = 1 + 2 + 4;	# 「そのまま表示」「HTMLに変換」「HTMLで入力」
$SYS_TEXTTYPE = 1 + 2 + 4;

# メッセージ検索機能を利用可能としますか?
#   0: 利用できない
#   1: 利用できる
$SYS_F_S = 1;

# Subjectにタグの入力を許しますか?
# タグの入力を許しても，安全なタグしか入力できません．
#   0: 許さない
#   1: 許す
$SYS_TAGINSUBJECT = 1;

# メッセージ投稿時、メイルアドレスの入力を必須としますか?
#   0: 必須としない
#   1: 必須とする
$SYS_POSTERMAIL = 0;

# メッセージの許容最大サイズ（バイト数で指定してください; 50K → 51200）
#   0は「メッセージサイズの制限なし」を意味します．
$SYS_MAXARTSIZE = 51200;

# 同一書き込みフォームからの連続書き込みを禁止しますか?
#   0: 許可する
#   1: 禁止する
$SYS_DENY_FORM_RECYCLE = 1;

# 半日以上前に生成されたフォームからの書き込みを禁止しますか?
#   0: 許可する
#   1: 禁止する
$SYS_DENY_FORM_OLD = 1;

# メッセージアイコンを利用しますか?
#   0: 利用しない
#   1: 利用する
$SYS_ICON = 1;

# コマンドアイコンを利用しますか?
#   0: 利用しない(コマンドはテキストで表示する)
#   1: 利用する
#   2: コマンドアイコンと同時にテキストも表示する
$SYS_COMICON = 1;

# 最近のメッセージに，[new!]アイコン（黄色の旗）をつけますか?
#   0: つけない．
#   1: 最近のメッセージn個に[new!]アイコンをつける．
#   2: 最近n日間のメッセージに[new!]アイコンをつける
$SYS_NEWICON = 2;

  # 上で「1: 最近のメッセージn個」に設定した場合はメッセージの個数を，
  # 「2: 最近n日間のメッセージ」に設定した場合は日数を設定してください．
  # 0を選んだ場合はそのままで結構です（指定しても無視されます）．
  $SYS_NEWICON_VALUE = 7;	# [個数] or [日数]

# 新規投稿メッセージが，デフォルトで上に増えていくか，下に増えていくか
# （タイトル一覧画面）
#   0: 上
#   1: 下
$SYS_BOTTOMTITLE = 0;

# 新規投稿メッセージが，デフォルトで上に増えていくか，下に増えていくか
# （メッセージ一覧画面）
#   0: 上
#   1: 下
$SYS_BOTTOMARTICLE = 1;

# サーバのポート番号を表示しますか?
#   0: 表示しない
#   1: (必要ならば)表示する
#      HTTPのデフォルトである80番ポートの場合，1に設定しても表示しません
$SYS_PORTNO = 1;

# メッセージの上下逆順表示用のリンクを使いますか?
#   0: 表示しない
#   1: 表示する
$SYS_REVERSE = 1;

# メッセージのヘッダにコマンド群を表示しますか?
#   0: 表示しない
#   1: 表示する
$SYS_COMMAND = 1;

  # 上で「0: 表示しない」を設定した場合，以下の設定は意味がありません．
  # まとめ読みの際は，各メッセージのヘッダにコマンド群を表示しますか?
  # 表示しないと見た目はすっきりしますが，
  # 例えば「最近のメッセージまとめ読み」から
  # 直接リプライすることができなくなる，等の弊害があります．
  #   0: 表示しない
  #   1: 表示する
  $SYS_COMMAND_EACH = 1;

# 書き込み後，まとめ読み時などに表示される移動のためのリンクは，
# リンクで表示しますか? それともボタンで表示しますか?
#   0: リンクで表示する
#   1: ボタンで表示する
$SYS_COMMAND_BUTTON = 1;

# メッセージのヘッダにメイルアドレスを表示しますか?
#   0: 表示しない
#   1: （あれば）表示する
$SYS_SHOWMAIL = 1;

# タイトル一覧(リプライ順)における，スレッドの表示形式を選んでください．
#   管理者用のタイトル一覧の表示形式は変更されません．
#   タイトル一覧(日付順)の表示形式は変更されません．
#
#   0: 1ページに表示するメッセージ数が一定になるように適当にスレッドを切る
#      （これがR5.*以前までの形式です）．
#
#   1: 存在するリプライは全て表示する．
#
#   2: リプライは一切表示せず，新着メッセージのみ表示する．
#
$SYS_THREAD_FORMAT = 0;

# 掲示板一覧で，最近書き込まれた掲示板に[new!]アイコンをつけることができます．
# 何日以内に書き込まれたらアイコンを付けますか?
# 0を指定するとアイコンを付けません．
$SYS_BLIST_NEWICON_DATE = 7;	# [日]

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
  #   0: 補わない → 「Subject: 題」（掲示板とメッセージIDはX-Kb-*に入ります）
  #   1: 補う     → 「Subject: [掲示板: メッセージID] 題」
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
  # R6.4以降，「From:」ヘッダには投稿者が入ります．
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
  # $AF_INET = 2; $SOCK_STREAM = 1;	# SunOS 4.*
  # $AF_INET = 2; $SOCK_STREAM = 2;	# SunOS 5.*(Solaris 2.*)
  # $AF_INET = 2; $SOCK_STREAM = 1;	# HP-UX
  # $AF_INET = 2; $SOCK_STREAM = 1;	# AIX
  # $AF_INET = 2; $SOCK_STREAM = 2;	# Cobalt OS 2.2(Linux 2.0.33)
  $AF_INET = 2; $SOCK_STREAM = 1;	# Linux
  # $AF_INET = 2; $SOCK_STREAM = 1;	# FreeBSD
  # $AF_INET = 2; $SOCK_STREAM = 1;	# IRIX
  # $AF_INET = 2; $SOCK_STREAM = 1;	# WinNT/95
  # $AF_INET = 2; $SOCK_STREAM = 1;	# Mac
  # この他の組み合わせを御存知の方がありましたら，
  # なひ(nahi@keynauts.com)まで御連絡ください．

###
## ○メイル投稿機能の設定
#
# メイル投稿機能を利用しますか? 利用するためには他にも設定が必要です．
# インストールマニュアルをよく読んでくださいね．
#   0: 利用しない
#   1: 利用する
$SYS_F_POST_STDIN = 0;

###
## ○各入力項目の大きさ
#
$SUBJECT_LENGTH = 60;	# 題
$TEXT_ROWS = 8;		# メッセージ行数
$TEXT_COLS = 70;	# メッセージ幅
$NAME_LENGTH = 60;	# 名前幅
$MAIL_LENGTH = 60;	# E-mail幅
$URL_LENGTH = 72;	# URL幅
$KEYWORD_LENGTH = 60;	# 検索キーワード幅
$BOARDNAME_LENGTH = 20;	# 掲示板名幅
$DEF_TITLE_NUM = 30;	# タイトル一覧に表示するタイトルの数
			# 0にすると全メッセージを表示するようになります．
$DEF_ARTICLE_NUM = 15;	# まとめ読みするメッセージの数

###
## ○引用の形態
#
# 引用時，元メッセージの作者名をつけますか?
#   0: つけない		 ] 引用元メッセージ．．．
#			 ] 引用元メッセージ．．．
#   1: つける		なひ ] 引用元メッセージ．．．
#			なひ ] 引用元メッセージ．．．
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
$H_LOGIN = 'ログイン';
$H_BOARD = '掲示板';
$H_ICON = 'アイコン';
$H_SUBJECT = 'タイトル';
$H_MESG = 'メッセージ';
$H_FROM = 'ユーザ名';
$H_MAIL = 'メイル';
$H_HOST = 'マシン';
$H_USER = 'ユーザ';
$H_PASSWD = 'パスワード';
$H_URL = 'URL';
$H_DATE = '投稿日';
$H_REPLY = 'リプライ';
$H_ORIG = 'リプライ元';
$H_ORIG_TOP = 'オリジナル';
$H_LINE = '<p>------------------------------</p>';
$H_NEWARTICLE = 'new!';
$H_HR = '<hr>';
$H_TEXTTYPE = '書き込み形式';
@H_TTLABEL = ( 'そのまま表示', 'HTMLに変換', 'HTMLで入力' );
$H_NOICON = 'なし';
$H_BACKBOARD = '掲示板一覧へ';
$H_BACKTITLEREPLY = 'タイトル一覧へ(スレッド)';
$H_BACKTITLEDATE = 'タイトル一覧へ(日付順)';
$H_PREVARTICLE = '前へ';
$H_NEXTARTICLE = '次へ';
$H_POSTNEWARTICLE = '新規に書き込む';
$H_REPLYTHISARTICLE = 'リプライを書き込む';
$H_REPLYTHISARTICLEQUOTE = '引用してリプライを書き込む';
$H_READREPLYALL = 'リプライをまとめ読み';
$H_DELETE = '削除する';
$H_SUPERSEDE = '訂正する';
$H_NOBACKART = '前のページはありません．';
$H_NONEXTART = '次のページはありません．';
$H_NOARTICLE = '該当するメッセージがありません．';

$H_TOP = '←';
$H_BOTTOM = '→';
$H_BACKART = '前ページへ';
$H_NEXTART = '次ページへ';

$H_THREAD_ALL = '▲';
$H_THREAD_ALL_L = 'スレッド全て';
$H_THREAD = '▼';
$H_THREAD_L = 'リプライ全て';
$H_REVERSE = '△▽';
$H_REVERSE_L = '逆順表示';
$H_SUPERSEDE_ICON = '[※]';
$H_SUPERSEDE_ICON_L = '訂正';
$H_DELETE_ICON = '[×]';
$H_DELETE_ICON_L = '削除';
$H_RELINKFROM_MARK = '[←]';
$H_RELINKFROM_MARK_L = 'リプライ先を変更';
$H_RELINKTO_MARK = '[◎]';
$H_RELINKTO_MARK_L = 'リプライ先に指定';
$H_REORDERFROM_MARK = '[△]';
$H_REORDERFROM_MARK_L = '順序を変更';
$H_REORDERTO_MARK = '[▽]';
$H_REORDERTO_MARK_L = '移動先に指定';


#/////////////////////////////////////////////////////////////////////
# $Id: kb.ph,v 5.25 1999-08-28 08:56:50 nakahiro Exp $
1;
