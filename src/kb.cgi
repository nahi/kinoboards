#!/usr/local/bin/perl
#!/usr/local/bin/perl5.00503-debug -d:DProf
#!/usr/local/bin/perl4.036


# このファイルの変更は最低2箇所，最大4箇所です（環境次第です）．
#
# 1. ↑の先頭行で，Perlのパスを指定します．「#!」に続けて指定してください．

# 2. kbディレクトリのフルパスを指定してください（URLではなく，パスです）．
#    ブラウザからアクセス可能なディレクトリでなくてもかまいません
#
$KBDIR_PATH = '/home/achilles/nakahiro/cvs_work/KB/tst/';
# $KBDIR_PATH = '/home/nahi/public_html';
# $KBDIR_PATH = 'd:\inetpub\wwwroot\kb';	# WinNT/Win9xの場合
# $KBDIR_PATH = 'foo:bar:kb';			# Macの場合?

# 3. サーバが動いているマシンがWin95/Macの場合，
#    $PCを1に設定してください．そうでない場合，この設定は不要です．
#
$PC = 0;	# for UNIX / WinNT
# $PC = 1;	# for Win95 / Mac

# 4. アイコンおよびスタイルシートファイルを，このファイルと別のディレクトリに
#    置く場合は，その別ディレクトリのURLを指定してください（パスではなく，
#    URLです）．指定するURLは，ブラウザからアクセス可能でなければいけません．
#    本ファイルと同じディレクトリにicon，styleディレクトリを置く場合は，
#    特に指定しなくてもかまいません（このままでOKです）．
#
#    指定したURLのディレクトリに置かれている，
#      icon/*.gifがアイコンファイルとして，
#      style/kbStyle.cssがスタイルシートファイルとして，
#    それぞれ参照されます．
#
# $KB_RESOURCE_URL = '/~nahi/kb/';


# 以下は書き換えの必要はありません．


######################################################################


# $Id: kb.cgi,v 5.63 2000-03-03 14:26:41 nakahiro Exp $

# KINOBOARDS: Kinoboards Is Network Opened BOARD System
# Copyright (C) 1995-2000 NAKAMURA Hiroshi.
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

# This file implements main functions of KINOBOARDS.

# perlの設定
push( @INC, '.' );
$[ = 0;				# zero origined
$| = 1;				# pipe flushed
$COLSEP = "\377";
srand( $^T ^ ( $$ + ( $$ << 15 )));

# 大域変数の定義
$HEADER_FILE = 'kb.ph';		# header file
$KB_VERSION = '1.0';		# version
$KB_RELEASE = '7β5';		# release
$CHARSET = 'euc';		# 漢字コード変換は行なわない
$ADMIN = 'admin';		# デフォルト設定
$GUEST = 'guest';		# デフォルト設定

# ディレクトリ
$SYS_DIR = '.';				# システムディレクトリ
$ICON_DIR = 'idef';			# アイコン定義ディレクトリ
$UI_DIR = 'UI';				# UIディレクトリ
$LOG_DIR = 'log';			# ログディレクトリ
$BOARDSRC_DIR = 'board';		# 掲示板ソースディレクトリ

# ファイル
$BOARD_FILE = 'kinoboards';		# 掲示板DB
$CONF_FILE_NAME = 'kb.conf';		# 掲示板別configuratinファイル
$ARRIVEMAIL_FILE_NAME = 'kb.mail';	# 掲示板別新規メイル送信先DB
$HEADER_FILE_NAME = 'kb.board';		# タイトルリストヘッダDB
$DB_FILE_NAME = 'kb.db';		# 記事DB
$ARTICLE_NUM_FILE_NAME = 'kb.aid';	# 記事番号DB
$USER_FILE = 'kb.user';			# ユーザ用DB
$DEFAULT_ICONDEF = 'all.idef';		# アイコンDB
$LOCK_FILE = 'kb.lock';			# ロックファイル
$LOCK_FILE_B = '';			# 掲示板別ロックファイル
$ACCESS_LOG = 'access_log';		# アクセスログファイル
$ERROR_LOG = 'error_log';		# エラーログファイル
# Suffix
$TMPFILE_SUFFIX = 'tmp';		# DBテンポラリファイルのSuffix
$ICONDEF_POSTFIX = 'idef';		# アイコンDBファイルのSuffix

# リソースURL
$RESOURCE_ICON = 'icon';		# アイコンディレクトリ
$RESOURCE_STYLE = 'style';		# スタイルシートディレクトリ
# 今後は他に，音，背景用画像など．．．?

# CGIと同一ディレクトリにあるヘッダファイルの読み込み
require( $HEADER_FILE ) if ( -s "$HEADER_FILE" );

# メインのヘッダファイルの読み込み
if ( !$KBDIR_PATH || !chdir( $KBDIR_PATH ))
{
    print "Content-Type: text/plain; charset=EUC-JP\n\n";
    print "エラー．管理者様へ:\n";
    print "$0の先頭部分に置かれている\$KBDIR_PATHが，\n";
    print "正しく設定されていません\n";
    print "設定してから再度試してみてください．";
    exit 0;
}

# chdir先のkb.phを読む．ただし上でrequire済みの場合は読まない（Perlの言語仕様）
require( $HEADER_FILE ) if ( -s "$HEADER_FILE" );

# インクルードファイルの読み込み
require( 'cgi.pl' );
require( 'kinologue.pl' );
$KB_RESOURCE_URL = $KB_RESOURCE_URL || $cgi'PATH_INFO;
$REMOTE_INFO = $cgi'REMOTE_HOST || $cgi'REMOTE_ADDR || '(unknown)';
$REMOTE_INFO .= '-' . $cgi'REMOTE_USER if $cgi'REMOTE_USER; # in BasicAuth
$PROGRAM = $cgi'PROGRAM;

$kinologue'SEV_THRESHOLD = $SYS_LOGLEVEL;

$cgi'SMTP_SERVER = $SMTP_SERVER;
$cgi'AF_INET = $AF_INET;
$cgi'SOCK_STREAM = $SOCK_STREAM;
$cgi'CHARSET = $CHARSET;
@cgi'TAG_ALLOWED = ( 'article', 'subject', 'key' );

if (( $cgi'SERVER_PORT != 80 ) && ( $SYS_PORTNO == 1 ))
{
    $SERVER_PORT_STRING = ":$cgi'SERVER_PORT";
}
else
{
    $SERVER_PORT_STRING = '';
}

$SCRIPT_URL = "http://$cgi'SERVER_NAME$SERVER_PORT_STRING$PROGRAM";
$MACPERL = ( $^O eq 'MacOS' );  # isMacPerl?
$PROGNAME = "KINOBOARDS/$KB_VERSION R$KB_RELEASE";
$ENV{'TZ'} = $TIME_ZONE if $TIME_ZONE;

# 許可タグのベース
$HTML_TAGS_COREATTRS = 'id/class/style/title';
$HTML_TAGS_I18NATTRS = 'lang/dir';
$HTML_TAGS_GENATTRS = "$HTML_TAGS_COREATTRS/$HTML_TAGS_I18NATTRS";

# 各種キャラクタアイコン
$H_TOP = '&lt;&lt;最新';
$H_BOTTOM = '先頭&gt;&gt;';
$H_UP = '&lt;次';
$H_DOWN = '前&gt;';
$H_THREAD_ALL = '▲';
$H_THREAD = '▼';
@H_REVERSE = ( '△', '▽' );
@H_EXPAND = ( '↓', '↑' );
$H_SUPERSEDE_ICON = '[※]';
$H_DELETE_ICON = '[×]';
$H_RELINKFROM_MARK = '[←]';
$H_RELINKTO_MARK = '[◎]';
$H_REORDERFROM_MARK = '[△]';
$H_REORDERTO_MARK = '[▽]';

# 外部リンクを張ることを許可するURL scheme
@URL_SCHEME = ( 'http', 'ftp', 'gopher', 'mailto' );

# 各種画像アイコンファイル相対URL
$ICON_UP = &GetIconURL( 'org_tlist.gif' );		# 上へ
$ICON_UP_X = &GetIconURL( 'org_tlist_x.gif' );		# 上へ
$ICON_PREV = &GetIconURL( 'org_prev.gif' );		# 前へ
$ICON_PREV_X = &GetIconURL( 'org_prev_x.gif' );		# 前へ
$ICON_NEXT = &GetIconURL( 'org_next.gif' );		# 次へ
$ICON_NEXT_X = &GetIconURL( 'org_next_x.gif' );		# 次へ
$ICON_DOWN = &GetIconURL( 'org_thread.gif' );		# 下へ
$ICON_DOWN_X = &GetIconURL( 'org_thread_x.gif' );	# 下へ
$ICON_FOLLOW = &GetIconURL( 'org_follow.gif' );		# リプライ
$ICON_FOLLOW_X = &GetIconURL( 'org_follow_x.gif' );	# リプライ
$ICON_QUOTE = &GetIconURL( 'org_quote.gif' );		# 引用してリプライ
$ICON_QUOTE_X = &GetIconURL( 'org_quote_x.gif' );	# 引用してリプライ
$ICON_SUPERSEDE = &GetIconURL( 'org_supersede.gif' );	# 訂正
$ICON_SUPERSEDE_X = &GetIconURL( 'org_supersede_x.gif' );	# 訂正
$ICON_DELETE = &GetIconURL( 'org_delete.gif' );		# 削除
$ICON_DELETE_X = &GetIconURL( 'org_delete_x.gif' );	# 削除
$ICON_HELP = &GetIconURL( 'org_help.gif' );		# ヘルプ
$ICON_NEW = &GetIconURL( 'org_listnew.gif' );		# 新着

# シグナルハンドラ
$SIG{'QUIT'} = 'IGNORE';
$SIG{'INT'} = $SIG{'HUP'} = $SIG{'TERM'} = $SIG{'TSTP'} = 'DoKill';
sub DoKill
{
    local( $sig ) = @_;
    if ( !$PC )
    {
	&cgi'unlock_file( $LOCK_FILE );
	&cgi'unlock_file( $LOCK_FILE_B ) if $LOCK_FILE_B;
    }
    &KbLog( $kinologue'SEV_WARN, "Caught a SIG$sig - shutting down..." );
    exit( 1 );
}

# 改行タグ，水平線タグ
$HTML_BR = "<br />\n";
$HTML_HR = "<hr />\n";

# ローカルカウンタ・フラグ
$gLinkNum = 0;
$gTabIndex = 0;
$gBoardDbCached = 0;


######################################################################


###
## MAIN - メインブロック
#
# - SYNOPSIS
#	kb.cgi
#
# - DESCRIPTION
#	起動時に一度だけ参照される．
#	引き数はないが，環境変数QUERY_STRINGとREQUEST_METHOD，
#	もしくは標準入力経由で値を渡さないと，正しく動作しない．
#
&KbLog( $kinologue'SEV_INFO, 'Exec started.' );
MAIN:
{
    &cgi'Decode();

    if ( $kinologue'SEV_THRESHOLD == $kinologue'SEV_DEBUG )
    {
	local( $key, $value, $msg );
	while (( $key, $value ) = each %cgi'TAGS )
	{
	    $msg .= '&' if $msg;
	    $msg .= "$key=$value";
	}
	&KbLog( $kinologue'SEV_DEBUG, "Command executed with ... " . $msg );
    }

    # HEADリクエストに対する特別処理
    if ( $ENV{ 'REQUEST_METHOD' } eq 'HEAD' )
    {
	local( $modTime ) = 0;
	if ( $cgi'TAGS{'b'} ne '' )
	{
	    $modTime = &getBoardLastmod( $cgi'TAGS{'b'} );
	}
	&cgi'Header( 1, $modTime, 0, (), 0 );
	last;
    }

    local( $c ) = $cgi'TAGS{'c'};
    local( $com ) = $cgi'TAGS{'com'};
    local( $s ) = $cgi'TAGS{'s'};
    $BOARD = $cgi'TAGS{'b'};
    if ( $#ARGV >= 0 )
    {
	# from command line.
	$BOARD = shift;
    }
    elsif ( $c eq '' )
    {
	if ( $BOARD )
	{
	    $c = $SYS_TITLE_FORMAT? 'r' : 'v';
	}
	else
	{
	    $c = 'bl';
	}
    }

    if ( $BOARD )
    {
	$BOARD_ESC = &URIEscape( $BOARD );	# リンク用にescape

	local( $boardConfFileP );
	( $BOARDNAME, $boardConfFileP ) = &GetBoardInfo( $BOARD );
	$LOCK_FILE_B = $LOCK_FILE . ".$BOARD";

	# 掲示板固有セッティングを読み込む
	if ( $boardConfFileP )
	{
	    local( $boardConfFile ) = &GetPath( $BOARD, $CONF_FILE_NAME );
	    require( $boardConfFile ) if ( -s "$boardConfFile" );
	}

	# アイコンDBも読み込む（R7以降）
	&CacheIconDb( $BOARD ) if $SYS_ICON;
    }

    # 全てのrequireが終わったあと．．．

    # 認証情報の初期化
    $cgiauth'GUEST = $GUEST;
    $cgiauth'ADMIN = $ADMIN;
    $USER_AUTH_FILE = &GetPath( $SYS_DIR, $USER_FILE );

    # 一部システム設定の補正
    $SYS_EXPAND = $SYS_EXPAND && ( $SYS_THREAD_FORMAT != 2 );
    $POLICY = $GUEST_POLICY;	# Policy by default.

    if ( $SYS_AUTH )
    {
	$SYS_AUTH_DEFAULT = $SYS_AUTH;
	$SYS_AUTH = 3 if ( $cgi'TAGS{ 'kinoA' } == 3 );
	if ( $c eq 'lo' )
	{
	    # ログイン
	    &UILogin();
	    last;
	}
	elsif ( $c eq 'ue' )
	{
	    # ユーザ新規登録
	    &UIUserEntry();
	    last;
	}
	elsif ( $c eq 'uex' )
	{
	    # ユーザ新規登録実施
	    &UIUserEntryExec();
	    last;
	}

	$cgiauth'AUTH_TYPE = $SYS_AUTH;
	&cgi'Cookie() if ( $SYS_AUTH == 1 );
	    
	local( $err, @userInfo );
	( $err, $UNAME, $PASSWD, @userInfo ) = &cgiauth'CheckUser( $USER_AUTH_FILE );
	    
	if ( $err == 3 )
	{
	    # ユーザ名がみつからない
	    &Fatal( 40, $cgi'TAGS{'kinoU'} );# 本当は41だけどセキュリティ優先
	}
	elsif ( $err == 4 )
	{
	    # パスワードが間違っている
	    &Fatal( 40, '' );
	}
	elsif ( $err == 9 )
	{
	    if ( $c eq 'acx' )
	    {
		# 管理者パスワード変更の実施
		&UIAdminConfigExec();
		last;
	    }
	    # 管理者パスワードが空の場合，ユーザを管理者扱いしてから．．．
	    $cgiauth'UID = $UNAME;
	    $cgiauth'PASSWD = $PASSWD;

	    # 管理者パスワード変更
	    &UIAdminConfig();
	    last;
	}
	elsif ( $err != 0 )
	{
	    # not reached...
	    &Fatal( 998, "Must not reach here(MAIN: $err)." );
	}
	    
	# 認証成功
	$UNAME_ESC = &URIEscape( $UNAME ) if ( $SYS_AUTH == 3 );
	$UMAIL = $userInfo[2];
	$UURL = $userInfo[3];

	# user policyの決定
	#   1 ... 読み
	#   2 ... 書き
	#   4 ... 登録（ユーザ情報をサーバに残す）
	#   8 ... 管理
	if ( &IsUser( $ADMIN ))
	{
	    # 管理者
	    $POLICY = 1 + 2 + 4 + 8;
	}
	elsif ( !&IsUser( $GUEST ))
	{
	    # 登録ユーザ
	    # $POLICY = ( $USER_POLICY & 1 ) + ( $USER_POLICY & 2 ) + 4;
	    $POLICY = $USER_POLICY + 4;
	}
	else
	{
	    # ゲストユーザ
	    # $POLICY = ( $GUEST_POLICY & 1 ) + ( $USER_POLICY & 2 );
	    $POLICY = $GUEST_POLICY;
	}
    }

    ###
    ## コマンドの振り分け
    #

    # 参照系
    if ( $POLICY & 1 )
    {
	if ( $c eq 'e' )
	{
	    # 単一記事の表示
	    &UIShowArticle();
	    last;
	}
	elsif ( $c eq 't' )
	{
	    # フォロー記事を全て表示．
	    &UIShowThread();
	    last;
	}
	elsif ( $c eq 'v' )
	{
	    # スレッド別タイトル一覧
	    &UIThreadTitle( 0 );
	    last;
	}
	elsif ( $c eq 'vt' )
	{
	    # スレッド別タイトルおよび記事一覧
	    &UIThreadArticle();
	    last;
	}
	elsif ( $c eq 'r' )
	{
	    # 書き込み順にソート
	    &UISortTitle();
	    last;
	}
	elsif ( $c eq 'l' )
	{
	    # 新しい記事を書き込み順に表示
	    &UISortArticle();
	    last;
	}
	elsif ( $SYS_F_S && ( $c eq 's' ))
	{
	    # 記事の検索
	    &UISearchArticle();
	    last;
	}
	elsif ( $SYS_ICON && ( $c eq 'i' ))
	{
	    # アイコン表示画面
	    &UIShowIcon();
	    last;
	}
	elsif ( $c eq 'h' )
	{
	    # ヘルプ画面
	    &UIHelp();
	    last;
	}
    }

    # 書き込み系
    local( $varBack ) = 0;
    if ( $POLICY & 2 )
    {
	if (( $c eq 'x' ) && ( $com ne 'x' ))
	{
	    # previewからの戻りなので，コマンド書き換え．
	    $varBack = 1;
	    $cgi'TAGS{'c'} = $cgi'TAGS{'corig'};
	    $c = $cgi'TAGS{'c'};
	}

	if ( $c eq 'n' )
	{
	    # 新規投稿
	    &UIPostNewEntry( $varBack );
	    last;
	}
	elsif ( !$s && ( $c eq 'f' ))
	{
	    # リプライ投稿
	    &UIPostReplyEntry( $varBack, 0 );
	    last;
	}
	elsif ( $c eq 'q' )
	{
	    # 引用リプライ投稿
	    &UIPostReplyEntry( $varBack, 1 );
	    last;
	}
	elsif ( !$s && ( $c eq 'p' ) && ( $com ne 'x' ))
	{
	    # 投稿プレビュー
	    &UIPostPreview( 0 );
	    last;
	}
	elsif ( !$s && ( $c eq 'p' ) && ( $com eq 'x' ))
	{
	    # 登録後画面の表示（直接）
	    &UIPostExec( 0 );
	    last;
	}
	elsif ( !$s && ( $c eq 'x' ) && ( $com eq 'x' ))
	{
	    # 登録後画面の表示（プレビュー経由）
	    &UIPostExec( 1 );
	    last;
	}
    }

    # 登録系
    if ( $POLICY & 4 )
    {
	# 「訂正」と「削除」が「書き込み系」でなく「登録系」なのは，
	# 登録してない人に消されちゃかなわないからさ．:-)

        if ( $c eq 'uc' )
        {
            # ユーザ情報設定
	    &UIUserConfig();
            last;
        }
        elsif ( $c eq 'ucx' )
        {
            # ユーザ情報設定の実施
	    &UIUserConfigExec();
	    last;
        }
	elsif ( $s && ( $c eq 'f' ))
	{
	    # 記事訂正
	    &UISupersedeEntry( $varBack );
	    last;
	}
	elsif ( $s && ( $c eq 'p' ) && ( $com ne 'x' ))
	{
	    # 記事訂正プレビュー
	    &UISupersedePreview( 0 );
	    last;
	}
	elsif ( $s && ( $c eq 'p' ) && ( $com eq 'x' ))
	{
	    # 記事訂正実施（直接）
	    &UISupersedeExec( 0 );
	    last;
	}
	elsif ( $s && ( $c eq 'x' ) && ( $com eq 'x' ))
	{
	    # 記事訂正実施（プレビュー経由）
	    &UISupersedeExec( 1 );
	    last;
	}
        elsif ( $c eq 'dp' )
        {
	    # 削除プレビュー
	    &UIDeletePreview();
	    last;
        }
        elsif ( $c eq 'de' )
        {
	    # 削除実施
            &UIDeleteExec( 0 );
	    last;
	}
        elsif ($c eq 'det' )
        {
	    # 削除実施（リプライも）
            &UIDeleteExec( 1 );
	    last;
        }
    }

    # 管理系
    if ( $POLICY & 8 )
    {
	if ( $c eq 'ct' )
	{
	    &UIThreadTitle( 2 );
	    last;
	}
	elsif ( $c eq 'ce' )
	{
	    &UIThreadTitle( 3 );
	    last;
	}
	elsif ( $c eq 'mvt' )
	{
	    &UIThreadTitle( 4 );
	    last;
	}
	elsif ( $c eq 'mve' )
	{
	    &UIThreadTitle( 5 );
	    last;
	}
        elsif ( $c eq 'bc' )
        {
            # 掲示板設定
	    &UIBoardConfig();
            last;
        }
        elsif ( $c eq 'bcx' )
        {
	    # 掲示板設定の実施
	    &UIBoardConfigExec();
	    last;
        }
        elsif ( $c eq 'be' )
        {
            # 掲示板新設
            &UIBoardEntry();
            last;
        }
        elsif ( $c eq 'bex' )
        {
	    # 掲示板新設の実施
	    &UIBoardEntryExec();
	    last;
        }
    }

    if ( $c eq 'bl' )
    {
	# 掲示板一覧の表示
	&UIBoardList();
	last;
    }

    # from command line?
    if ( $#ARGV >= 0 )
    {
	$c = shift;		# Command.
	local( $body, $code );
	while ( <> )
	{
	    $body .= $_;
	    last if ( $SYS_MAXARTSIZE &&
	        ( length( $body ) > $SYS_MAXARTSIZE ));
	}
	$code = &jcode'getcode( *body );
	&jcode'convert( *body, 'euc', $code, 'z' ) if ( defined( $code ));
	$body =~ s/\x0d\x0a/\x0a/go;
	$body =~ s/\x0d/\x0a/go;

	if ( $SYS_F_POST_STDIN )
	{
	    if ( $c eq 'POST' )
	    {
		*gVarBody = *body;
		$gVarForce = 1;
		do( &GetPath( $UI_DIR, 'Post.pl' ));
		last;
	    }
	    elsif ( $c eq 'POST_IF' )
	    {
		*gVarBody = *body;
		$gVarForce = 0;
		do( &GetPath( $UI_DIR, 'Post.pl' ));
		last;
	    }
	}
    }

    # どのコマンドでもない．エラー．
    &Fatal( 99, $c );
}
&KbLog( $kinologue'SEV_INFO, 'Exec finished.' );
exit( 0 );


######################################################################
# ユーザインタフェイスインプリメンテーション


###
## サインオン画面
#
sub UILogin
{
    # Isolation level: CHAOS.

    # ユーザ情報をクリア
    if ( $SYS_AUTH == 1 )
    {
	$UNAME = $cgiauth'F_COOKIE_RESET;
    }
    else
    {
	$UNAME = '';
    }
    &htmlGen( 'Login.xml' );
}

sub hg_login_form
{
    &Fatal( 18, "$_[0]/LoginForm" ) if ( $_[0] ne 'Login.xml' );

    local( %tags, $msg );
    $msg = &TagLabel( $H_FROM, 'kinoU', 'N' ) . ': ' . &TagInputText( 'text', 'kinoU', '', $NAME_LENGTH ) . $HTML_BR;
    $msg .= &TagLabel( $H_PASSWD, 'kinoP', 'P' ) . ': ' . &TagInputText( 'password', 'kinoP', '', $PASSWD_LENGTH ) . $HTML_BR;
    if ( $SYS_AUTH_DEFAULT == 1 )
    {
	local( $contents );
	$contents = &TagInputRadio( 'kinoA_url', 'kinoA', '3', 0 ) . ":\n" .
	    &TagLabel( 'クッキー(HTTP-Cookies)を使わずに認証する', 'kinoA_url', 'U' ) . $HTML_BR;
	$contents .= &TagInputRadio( 'kinoA_cookies', 'kinoA', '1', 1 ) .
	    "\n" . &TagLabel( 'クッキーを使ってこのブラウザに情報を覚えさせる', 'kinoA_cookies', 'C' ) . $HTML_BR;
	$msg .= &TagFieldset( "クッキー:$HTML_BR", $contents );
    }

    %tags = ( 'c', 'bl', 'kinoT', 'plain' );
    &DumpForm( *tags, '実行', 'リセット', *msg, 1 );
}


###
## 管理者パスワードの設定画面
#
sub UIAdminConfig
{
    # Isolation level: CHAOS.
    &htmlGen( 'AdminConfig.xml' );
}

sub hg_admin_config_form
{
    &Fatal( 18, "$_[0]/AdminConfigForm" ) if ( $_[0] ne 'AdminConfig.xml' );

    local( %tags, $msg );
    $msg = &TagLabel( $H_PASSWD, 'confP', 'P' ) . ': ' .
	&TagInputText( 'password', 'confP', '', $PASSWD_LENGTH ) . $HTML_BR;
    $msg .= &TagLabel( $H_PASSWD, 'confP2', 'C' ) . ': ' .
	&TagInputText( 'password', 'confP2', '', $PASSWD_LENGTH ) .
	'（念のため，もう一度お願いします）' . $HTML_BR;
    %tags = ( 'c', 'acx' );
    &DumpForm( *tags, '設定', 'リセット', *msg, 1 );
}


###
## 管理者パスワード設定の実施
#
sub UIAdminConfigExec
{
    # Isolation level: SERIALIZABLE.
    &LockAll();

    local( $p1 ) = $cgi'TAGS{'confP'};
    local( $p2 ) = $cgi'TAGS{'confP2'};

    # adminのみ
    &Fatal( 44, '' ) unless ( $POLICY & 8 );

    if ( !$p2 || ( $p1 ne $p2 ))
    {
	&Fatal( 42, $H_PASSWD );
    }
    
    if ( !&cgiauth'SetUserPasswd( $USER_AUTH_FILE , $ADMIN, $p1 ))
    {
	&Fatal( 41, $ADMIN );
    }

    &UnlockAll();

    # ユーザ情報をクリア
    &UILogin();
}


###
## ユーザ登録画面
#
sub UIUserEntry
{
    # Isolation level: CHAOS.

    # ユーザ情報をクリア
    $UNAME = $cgiauth'F_COOKIE_RESET if ( $SYS_AUTH == 1 );
    &htmlGen( 'UserEntry.xml' );
}

sub hg_user_entry_form
{
    &Fatal( 18, "$_[0]/UserEntryForm" ) if ( $_[0] ne 'UserEntry.xml' );

    local( %tags, $msg );
    $msg = &TagLabel( $H_FROM, 'kinoU', 'N' ) . ': ' . &TagInputText( 'text',
	'kinoU', '', $NAME_LENGTH ) . $HTML_BR;
    $msg .= &TagLabel( $H_MAIL, 'mail', 'M' ) . ': ' . &TagInputText( 'text',
	'mail', '', $MAIL_LENGTH ) . $HTML_BR;
    $msg .= &TagLabel( $H_PASSWD, 'kinoP', 'P' ) . ': ' . &TagInputText(
	'password', 'kinoP', '', $PASSWD_LENGTH ) . $HTML_BR;
    $msg .= &TagLabel( $H_PASSWD, 'kinoP2', 'C' ) . ': ' . &TagInputText(
	'password', 'kinoP2', '', $PASSWD_LENGTH ) .
	'（念のため，もう一度お願いします）' . $HTML_BR;
    $msg .= &TagLabel( $H_URL, 'url', 'U' ) . ': ' . &TagInputText( 'text',
	'url', 'http://', $URL_LENGTH ) . '（省略してもかまいません）' .
	$HTML_BR;

    %tags = ( 'c', 'uex' );
    &DumpForm( *tags, '登録', 'リセット', *msg, 1 );
}


###
## ユーザ登録の実施
#
sub UIUserEntryExec
{
    # Isolation level: SERIALIZABLE.
    &LockAll();

    local( $user ) = $cgi'TAGS{'kinoU'};
    local( $p1 ) = $cgi'TAGS{'kinoP'};
    local( $p2 ) = $cgi'TAGS{'kinoP2'};
    local( $mail ) = $cgi'TAGS{'mail'};
    local( $url ) = $cgi'TAGS{'url'};

    &CheckName( *user );
    &CheckEmail( *mail );
    &CheckURL( *url );
    &CheckPasswd( *p1 );

    if ( !$p2 || ( $p1 ne $p2 ))
    {
	&Fatal( 42, $H_PASSWD );
    }
	    
    # 登録済みユーザの検索
    if ( $SYS_POSTERMAIL && &cgiauth'SearchUserInfo( $USER_AUTH_FILE, $mail, undef ))
    {
	&Fatal( 6, $mail );
    }

    # 新規登録する
    local( $res ) = &cgiauth'AddUser( $USER_AUTH_FILE, $user, $p1, $mail, $url );

    if ( $res == 1 )
    {
	&Fatal( 5, $user );
    }
    elsif ( $res == 2 )
    {
	&Fatal( 998, 'Must not reach here(UserEntryExec).' );
    }

    &UnlockAll();

    # ログイン画面へ
    &UILogin();
}


###
## ユーザ設定変更
#
sub UIUserConfig
{
    # Isolation level: CHAOS.

    &htmlGen( 'UserConfig.xml' );
}

sub hg_user_config_form
{
    &Fatal( 18, "$_[0]/UserConfigForm" ) if ( $_[0] ne 'UserConfig.xml' );

    if ( $POLICY & 8 )
    {
	local( %tags, $msg );
	$msg .= &TagLabel( "変更する$H_USERの$H_FROM", 'confUser', 'N' ) .
	    ': ' . &TagInputText( 'text', 'confUser', '', $NAME_LENGTH ) .
	    "（管理者は全$H_USERの設定を変更できます）" . $HTML_BR . $HTML_BR;
	$msg .= &TagLabel( $H_MAIL, 'confMail', 'M' ) . ': ' .
	    &TagInputText( 'text', 'confMail', '', $MAIL_LENGTH ) . $HTML_BR;
	$msg .= &TagLabel( $H_URL, 'confUrl', 'U' ) . ': ' .
	    &TagInputText( 'text', 'confUrl', 'http://', $URL_LENGTH ) . $HTML_BR . $HTML_BR;
	$msg .= &TagLabel( $H_PASSWD, 'confP', 'P' ) . ': ' .
	    &TagInputText( 'password', 'confP', '', $PASSWD_LENGTH ) . $HTML_BR;
	$msg .= &TagLabel( $H_PASSWD, 'confP2', 'C' ) . ': ' .
	    &TagInputText( 'password', 'confP2', '', $PASSWD_LENGTH ) .
	    '（念のため，もう一度お願いします）' . $HTML_BR;
	%tags = ( 'c', 'ucx' );
	&DumpForm( *tags, '設定', 'リセット', *msg );
    }
    else
    {
	$UURL = $UURL || 'http://';

	local( %tags, $msg );
	$msg .= $H_FROM . ': ' . $UNAME . $HTML_BR . $HTML_BR;
	$msg .= &TagLabel( $H_MAIL, 'confMail', 'M' ) . ': ' .
	    &TagInputText( 'text', 'confMail', $UMAIL, $MAIL_LENGTH ) . $HTML_BR;
	$msg .= &TagLabel( $H_URL, 'confUrl', 'U' ) . ': ' .
	    &TagInputText( 'text', 'confUrl', $UURL, $URL_LENGTH ) . $HTML_BR . $HTML_BR;
	$msg .= &TagLabel( $H_PASSWD, 'confP', 'P' ) . ': ' .
	    &TagInputText( 'password', 'confP', '' , $PASSWD_LENGTH ) . $HTML_BR;
	$msg .= &TagLabel( $H_PASSWD, 'confP2', 'C' ) . ': ' .
	    &TagInputText( 'password', 'confP2', '', $PASSWD_LENGTH ) .
	    '（念のため，もう一度お願いします）' . $HTML_BR;
	%tags = ( 'c', 'ucx' );
	&DumpForm( *tags, '設定', 'リセット', *msg );
    }
}


###
## ユーザ設定の実施
#
sub UIUserConfigExec
{
    # Isolation level: SERIALIZABLE.
    &LockAll();

    local( $p1 ) = $cgi'TAGS{'confP'};
    local( $p2 ) = $cgi'TAGS{'confP2'};
    local( $user ) = $cgi'TAGS{'confUser'};
    local( $mail ) = $cgi'TAGS{'confMail'};
    local( $url ) = $cgi'TAGS{'confUrl'};

    $user = $UNAME unless ( $POLICY & 8 );

    &CheckName( *user );
    &CheckEmail( *mail );
    &CheckURL( *url );
		
    # （必要なら）パスワード変更
    if ( $p1 || $p2 )
    {
	&CheckPasswd( *p1 );

	if ( !$p2 || ( $p1 ne $p2 ))
	{
	    &Fatal( 42, $H_PASSWD );
	}

	if ( !&cgiauth'SetUserPasswd( $USER_AUTH_FILE, $user, $p1 ))
	{
	    &Fatal( 41, $user );
	}
    }

    # ユーザ情報更新
    if ( !&cgiauth'SetUserInfo( $USER_AUTH_FILE, $user, ( $mail, $url )))
    {
	&Fatal( 41, '' );
    }

    &UnlockAll();

    &UIBoardList();
}


###
## 掲示板登録画面
#
sub UIBoardEntry
{
    # Isolation level: CHAOS.

    &htmlGen( 'BoardEntry.xml' );
}

sub hg_board_entry_form
{
    &Fatal( 18, "$_[0]/BoardEntryForm" ) if ( $_[0] ne 'BoardEntry.xml' );

    local( %tags, $msg );
    $msg = &TagLabel( "$H_BOARD略称", 'name', 'B' ) . ': ' . &TagInputText(
	'text', 'name', '', $BOARDNAME_LENGTH ) . $HTML_BR;
    $msg .= &TagLabel( "$H_BOARD名称", 'intro', 'N' ) . ': ' . &TagInputText(
	'text', 'intro', '', $BOARDNAME_LENGTH ) . $HTML_BR . $HTML_BR;
    $msg .= &TagLabel( "$H_BOARDの自動$H_MAIL配信先", 'armail', 'M' ) .
	$HTML_BR . &TagTextarea( 'armail', '', $TEXT_ROWS, $MAIL_LENGTH ) .
	$HTML_BR . $HTML_BR;
    $msg .= &TagLabel( "$H_BOARDヘッダ部分", 'article', 'H' ) . $HTML_BR .
	&TagTextarea( 'article', '', $TEXT_ROWS, $TEXT_COLS ) . $HTML_BR;
    %tags = ( 'c', 'bex' );
    &DumpForm( *tags, '登録', 'リセット', *msg );
}


###
## 掲示板登録の実施
#
sub UIBoardEntryExec
{
    # Isolation level: SERIALIZABLE.
    &LockAll();

    local( $name ) = $cgi'TAGS{'name'};
    local( $intro ) = $cgi'TAGS{'intro'};
    local( $armail ) = $cgi'TAGS{'armail'};
    local( $header ) = $cgi'TAGS{'article'};

    &CheckBoardDir( *name );
    &CheckBoardName( *intro );
    &CheckBoardHeader( *header );
    &secureSubject( *intro );
    &secureArticle( *header, $H_TTLABEL[2] );
    local( @arriveMail ) = split( /\n/, $armail );

    &AddBoardDb( $name, $intro, 0, *arriveMail, *header );

    &UnlockAll();

    &UIBoardList();
}


###
## 掲示板設定変更画面
#
sub UIBoardConfig
{
    # Isolation level: SERIALIZABLE.
    &LockAll();

    # 全掲示板の情報を取り出す
    @gArriveMail = ();
    &GetArriveMailTo(1, $BOARD, *gArriveMail); # 宛先とコメントを取り出す
    $gHeader = "";
    &GetHeaderDb( $BOARD, *gHeader ); # ヘッダ文字列を取り出す

    &htmlGen( 'BoardConfig.xml' );

    &UnlockAll();
}

sub hg_board_config_form
{
    &Fatal( 18, "$_[0]/BoardConfigForm" ) if ( $_[0] ne 'BoardConfig.xml' );

    local( %tags, $msg );
    $msg = &TagLabel( "「$BOARD」$H_BOARDを利用", 'valid', 'V' ) . ': ' .
	&TagInputCheck( 'valid', 1 ) . $HTML_BR . $HTML_BR;
    $msg .= &TagLabel( "「$BOARD」名称", 'intro', 'N' ) . ': ' .
	&TagInputText( 'text', 'intro', $BOARDNAME, $BOARDNAME_LENGTH ) .
	$HTML_BR . $HTML_BR;
    local( $all );
    foreach ( @gArriveMail ) { $all .= $_ . "\n"; }
    $msg .= &TagLabel( "「$BOARD」の自動$H_MAIL配信先", 'armail', 'M' ) .
	$HTML_BR . &TagTextarea( 'armail', $all, $TEXT_ROWS, $MAIL_LENGTH ) .
	$HTML_BR . $HTML_BR;
    $msg .= &TagLabel( "「$BOARD」の$H_BOARDヘッダ部分", 'article', 'H' ) .
	$HTML_BR . &TagTextarea( 'article', $gHeader, $TEXT_ROWS,
	$TEXT_COLS ) . $HTML_BR;
    %tags = ( 'c', 'bcx', 'b', $BOARD );
    &DumpForm( *tags, '変更', 'リセット', *msg );
}


###
## 掲示板設定の実施
#
sub UIBoardConfigExec
{
    # Isolation level: SERIALIZABLE.
    &LockAll();

    local( $valid ) = $cgi'TAGS{'valid'};
    local( $intro ) = $cgi'TAGS{'intro'};
    local( $armail ) = $cgi'TAGS{'armail'};
    local( $header ) = $cgi'TAGS{'article'};

    &CheckBoardName( *intro );
    &CheckBoardHeader( *header );
    &secureSubject( *intro );
    &secureArticle( *header, $H_TTLABEL[2] );
    local( @arriveMail ) = split( /\n/, $armail );

    &UpdateBoardDb( $BOARD, $valid, $intro, 0, *arriveMail, *header );

    &UnlockAll();

    &UIBoardList();
}


###
## 掲示板一覧
#
sub UIBoardList
{
    # Isolation level: CHAOS.

    &htmlGen( 'BoardList.xml' );
}


###
## メッセージ新規登録のエントリ
## リプライメッセージ登録のエントリ
## メッセージ訂正のエントリ
#
sub UIPostNewEntry
{
    # Isolation level: CHAOS.

    if ( $SYS_NEWART_ADMINONLY && !( $POLICY & 8 ))
    {
	&Fatal( 99, $cgi'TAGS{'c'} );
    }

    local( $back ) = @_;

    $gId = '';			# 0ではダメ．そういうファイル名もあるかも．
    $gDefPostDateStr = $cgi'TAGS{'postdate'};
    $gDefSubject = $cgi'TAGS{'subject'};
    $gDefName = $cgi'TAGS{'name'};
    $gDefEmail = $cgi'TAGS{'mail'};
    $gDefUrl = $cgi'TAGS{'url'};
    $gDefTextType = $cgi'TAGS{'texttype'};
    $gDefIcon = $cgi'TAGS{'icon'};
    $gDefArticle = $cgi'TAGS{'article'};
    $gDefFmail = $cgi'TAGS{'fmail'};

    if ( $back )
    {
	require( 'mimer.pl' );
	$gDefSubject = &MIME'base64decode( $gDefSubject );
	$gDefArticle = &MIME'base64decode( $gDefArticle );
    }
    else
    {
    }

    $gEntryType = 'normal';		# 新規
    &htmlGen( 'PostNewEntry.xml' );
}

sub UIPostReplyEntry
{
    # Isolation level: SERIALIZABLE.
    &LockBoard();
    &DbCache( $BOARD ) if $BOARD;

    local( $back, $quoteFlag ) = @_;

    $gId = $cgi'TAGS{'id'};
    $gDefPostDateStr = $cgi'TAGS{'postdate'};
    $gDefSubject = $cgi'TAGS{'subject'};
    $gDefName = $cgi'TAGS{'name'};
    $gDefEmail = $cgi'TAGS{'mail'};
    $gDefUrl = $cgi'TAGS{'url'};
    $gDefTextType = $cgi'TAGS{'texttype'};
    $gDefIcon = $cgi'TAGS{'icon'};
    $gDefArticle = $cgi'TAGS{'article'};
    $gDefFmail = $cgi'TAGS{'fmail'};

    if ( $back )
    {
	require( 'mimer.pl' );
	$gDefSubject = &MIME'base64decode( $gDefSubject );
	$gDefArticle = &MIME'base64decode( $gDefArticle );
    }
    elsif ( $quoteFlag == 0 )
    {
	if ( $gDefSubject eq '' )
	{
	    local( $tmp );
	    $gDefSubject = &getMsgSubject( $gId );
	    &GetReplySubject( *gDefSubject );
	}
    }
    else
    {
	if ( $gDefSubject eq '' )
	{
	    local( $tmp );
	    $gDefSubject = &getMsgSubject( $gId );
	    &GetReplySubject( *gDefSubject );
	}
	&QuoteOriginalArticle( $gId, *gDefArticle );
    }

    $gEntryType = 'reply';		# リプライ
    &htmlGen( 'PostReplyEntry.xml' );

    &UnlockBoard();
}

sub UISupersedeEntry
{
    # Isolation level: SERIALIZABLE.
    &LockBoard();
    &DbCache( $BOARD ) if $BOARD;

    local( $back ) = @_;

    if ( !( $POLICY & 8 ) && ( $SYS_OVERWRITE == 0 ))
    {
	&Fatal( 99, $cgi'TAGS{'c'} );
    }

    $gId = $cgi'TAGS{'id'};
    $gDefPostDateStr = $cgi'TAGS{'postdate'};
    $gDefSubject = $cgi'TAGS{'subject'};
    $gDefName = $cgi'TAGS{'name'};
    $gDefEmail = $cgi'TAGS{'mail'};
    $gDefUrl = $cgi'TAGS{'url'};
    $gDefTextType = $cgi'TAGS{'texttype'};	# 訂正時はXHTML入力のほうがいいかも 
    $gDefIcon = $cgi'TAGS{'icon'};
    $gDefArticle = $cgi'TAGS{'article'};
    $gDefFmail = $cgi'TAGS{'fmail'};

    if ( $back )
    {
	require( 'mimer.pl' );
	$gDefSubject = &MIME'base64decode( $gDefSubject );
	$gDefArticle = &MIME'base64decode( $gDefArticle );
    }
    else
    {
	local( $tmp, $postDate );
	( $tmp, $tmp, $postDate, $gDefSubject, $gDefIcon, $tmp, $gDefName, $gDefEmail, $gDefUrl ) = &getMsgInfo( $gId );
	$gDefPostDateStr = &GetYYYY_MM_DD_HH_MM_SSFromUtc( $postDate );
	&QuoteOriginalArticleWithoutQMark( $gId, *gDefArticle );
    }

    $gEntryType = 'supersede';		# 修正
    &htmlGen( 'SupersedeEntry.xml' );

    &UnlockBoard();
}

sub hg_post_reply_entry_orig_article
{
    &Fatal( 18, "$_[0]/PostReplyEntryOrigArticle" ) if ( $_[0] ne 'PostReplyEntry.xml' );
    &DumpArtBody( $gId, 0, 1 );
}

sub hg_supersede_entry_orig_article
{
    &Fatal( 18, "$_[0]/SupersedeEntryOrigArticle" ) if ( $_[0] ne 'SupersedeEntry.xml' );
    &DumpArtBody( $gId, 0, 1 );
}


###
## メッセージ登録のプレビュー
## メッセージ訂正のプレビュー
#
sub UIPostPreview
{
    # Isolation level: SERIALIZABLE.
    &LockAll();
    &DbCache( $BOARD ) if $BOARD;

    &UIPostPreviewMain( 'post' );
    &htmlGen( 'PostPreview.xml' );

    &UnlockAll();
}

sub UISupersedePreview
{
    # Isolation level: READ UNCOMITTED.
    &LockAll();
    &DbCache( $BOARD ) if $BOARD;
    &UnlockAll();

    if ( !( $POLICY & 8 ) && ( $SYS_OVERWRITE == 0 ))
    {
	&Fatal( 99, $cgi'TAGS{'c'} );
    }

    &UIPostPreviewMain( 'supersede' );
    &htmlGen( 'SupersedePreview.xml' );
}

sub UIPostPreviewMain
{
    local( $type ) = @_;

    # 入力された記事情報
    $gOrigId = $cgi'TAGS{'id'};
    $gPostDateStr = $cgi'TAGS{'postdate'};
    $gSubject = $cgi'TAGS{'subject'};
    $gIcon = $cgi'TAGS{'icon'};
    $gArticle = $cgi'TAGS{'article'};
    $gTextType = $cgi'TAGS{'texttype'};

    # 各種情報の取得
    if ( $POLICY & 8 )
    {
	if ( $cgi'TAGS{'name'} eq '' )
	{
	    $gName = $MAINT_NAME;
	    $gEmail = $MAINT;
	    $gUrl = $MAINT_URL;
	}
	else
	{
	    $gName = $cgi'TAGS{'name'};
	    $gEmail = $cgi'TAGS{'mail'};
	    $gUrl = $cgi'TAGS{'url'};
	}
    }
    elsif ( $POLICY & 4 )
    {
	$gName = $UNAME;
	$gEmail = $UMAIL;
	$gUrl = $UURL;
    }
    else
    {
	$gName = $cgi'TAGS{'name'};
	$gEmail = $cgi'TAGS{'mail'};
	$gUrl = $cgi'TAGS{'url'};
    }

    $gEncSubject = &MIME'base64encode( $gSubject );
    $gEncArticle = &MIME'base64encode( $gArticle );

    &secureSubject( *gSubject );
    &secureArticle( *gArticle, $gTextType );

    local( $postDate ) = $^T;
    $postDate = &GetUtcFromYYYY_MM_DD_HH_MM_SS( $gPostDateStr ) if ( $gPostDateStr ne '' );

    # 入力された記事情報のチェック
    &CheckArticle( $BOARD, *postDate, *gName, *gEmail, *gUrl, *gSubject, *gIcon, *gArticle );
}

sub hg_post_preview_form
{
    &Fatal( 18, "$_[0]/PostPreviewForm" ) if ( $_[0] ne 'PostPreview.xml' );

    require( 'mimer.pl' );

    local( $supersede ) = $_[1];

    local( %tags, $msg, $contents );
    $contents = &TagInputRadio( 'com_e', 'com', 'e', 0 ) . ":\n" . &TagLabel( '戻ってやりなおす', 'com_e', 'P' ) . $HTML_BR;
    $contents .= &TagInputRadio( 'com_x', 'com', 'x', 1 ) . "\n" . &TagLabel( '登録する', 'com_x', 'X' ) . $HTML_BR;
    $msg = &TagFieldset( "コマンド:$HTML_BR", $contents );
    %tags = ( 'corig', $cgi'TAGS{'corig'}, 'c', 'x', 'b', $BOARD,
	     'id', $gOrigId, 'postdate', $gPostDateStr, 'texttype', $gTextType,
	     'name', $gName, 'mail', $gEmail, 'url', $gUrl, 'icon', $gIcon,
	     'subject', $gEncSubject, 'article', $gEncArticle,
	     'fmail', $cgi'TAGS{'fmail'}, 's', $supersede,
	     'op', $cgi'TAGS{'op'} );

    &DumpForm( *tags, '実行', '', *msg );
}

sub hg_supersede_preview_form
{
    &Fatal( 18, "$_[0]/SupersedePreviewForm" ) if ( $_[0] ne 'SupersedePreview.xml' );
    &hg_post_preview_form( 'PostPreview.xml', 1 );
}

sub hg_post_preview_body
{
    &Fatal( 18, "$_[0]/PostPreviewBody" ) if ( $_[0] ne 'PostPreview.xml' );

    local( $postDate ) = $^T;
    $postDate = &GetUtcFromYYYY_MM_DD_HH_MM_SS( $gPostDateStr ) if ( $gPostDateStr ne '' );
    &DumpArtBody( '', 0, 1, $gOrigId, '', $postDate, $gSubject, $gIcon, 0, $gName, $gEmail, $gUrl, $gArticle );
}

sub hg_supersede_preview_body
{
    &Fatal( 18, "$_[0]/SupersedePreviewBody" ) if ( $_[0] ne 'SupersedePreview.xml' );

    local( $postDate ) = $^T;
    $postDate = &GetUtcFromYYYY_MM_DD_HH_MM_SS( $gPostDateStr ) if ( $gPostDateStr ne '' );

    # hg_post_preview_bodyとは異なり，fidが空（リプライ元ではない）．
    &DumpArtBody( '', 0, 1, '', '', $postDate, $gSubject, $gIcon, 0, $gName, $gEmail, $gUrl, $gArticle );
}

sub hg_supersede_preview_orig_article
{
    &Fatal( 18, "$_[0]/SupersedePreviewOrigArticle" ) if ( $_[0] ne 'SupersedePreview.xml' );
    &DumpArtBody( $gOrigId, 0, 1 );
}


###
## 記事の登録
## 記事の訂正
#
sub UIPostExec
{
    # Isolation level: SERIALIZABLE.
    &LockAll();
    &DbCache( $BOARD ) if $BOARD;

    local( $previewFlag ) = @_;

    &UIPostExecMain( $previewFlag, 'post' );
    &htmlGen( 'PostExec.xml' );

    &UnlockAll();
}

sub UISupersedeExec
{
    # Isolation level: SERIALIZABLE.
    &LockAll();
    &DbCache( $BOARD ) if $BOARD;

    if ( !( $POLICY & 8 ) && ( $SYS_OVERWRITE == 0 ))
    {
	&Fatal( 99, $cgi'TAGS{'c'} );
    }

    local( $previewFlag ) = @_;
    &UIPostExecMain( $previewFlag, 'supersede' );
    &htmlGen( 'SupersedeExec.xml' );

    &UnlockAll();
}

sub UIPostExecMain
{
    require( 'mimer.pl' );

    local( $previewFlag, $type ) = @_;

    # 入力された記事情報
    $gOrigId = $cgi'TAGS{'id'};
    local( $postDateStr ) = $cgi'TAGS{'postdate'};
    local( $TextType ) = $cgi'TAGS{'texttype'};
    local( $Icon ) = $cgi'TAGS{'icon'};
    local( $Subject ) = $cgi'TAGS{'subject'};
    local( $Article ) = $cgi'TAGS{'article'};
    local( $Fmail ) = $cgi'TAGS{'fmail'};
    local( $op ) = $cgi'TAGS{'op'};

    # ここ半日の間に生成されたフォームからしか投稿を許可しない．
    local( $base ) = ( -M &GetPath( $SYS_DIR, $BOARD_FILE ));
    if ( $SYS_DENY_FORM_OLD && (( $op == 0 ) || ( $base - $op > .5 )))
    {
	&Fatal( 15, '' );
    }

    # フォーム再利用の禁止
    if ( $SYS_DENY_FORM_RECYCLE )
    {
	local( $dId, $dKey );
	&GetArticleId( $BOARD, *dId, *dKey );
	&Fatal( 16, '' ) if ( $dKey && ( $dKey == $op ));
    }

    # 各種情報の取得
    local( $Name, $Email, $Url, $postDate );
    $postDate = $^T;
    if ( $POLICY & 8 )
    {
	if ( $cgi'TAGS{'name'} eq '' )
	{
	    $Name = $MAINT_NAME;
	    $Email = $MAINT;
	    $Url = $MAINT_URL;
	}
	else
	{
	    $Name = $cgi'TAGS{'name'};
	    $Email = $cgi'TAGS{'mail'};
	    $Url = $cgi'TAGS{'url'};
	}
	if ( $postDateStr ne '' )
	{
	    $postDate = &GetUtcFromYYYY_MM_DD_HH_MM_SS( $postDateStr );
	}
    }
    elsif ( $POLICY & 4 )
    {
	$Name = $UNAME;
	$Email = $UMAIL;
	$Url = $UURL;
    }
    else
    {
	$Name = $cgi'TAGS{'name'};
	$Email = $cgi'TAGS{'mail'};
	$Url = $cgi'TAGS{'url'};
    }

    $Subject = &MIME'base64decode( $Subject ) if $previewFlag;
    $Article = &MIME'base64decode( $Article ) if $previewFlag;
    &secureSubject( *Subject );
    &secureArticle( *Article, $TextType );

    if ( $type eq 'post' )
    {
	# 記事の作成
	$gNewArtId = &MakeNewArticleEx( $BOARD, $gOrigId, $op, $postDate, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail, 1 );
    }
    elsif ( $type eq 'supersede' )
    {
	# 記事の訂正
	local( $name ) = &getMsgAuthor( $gOrigId );
	&Fatal( 44, '' ) if ( !&IsUser( $name ) && !( $POLICY & 8 ));
	&Fatal( 19, '' ) if (( &getMsgDaughters( $gOrigId ) ne '' ) && !( $POLICY & 8 ) && ( $SYS_OVERWRITE == 1 ));

	$gNewArtId = &SupersedeArticle( $BOARD, $gOrigId, $postDate, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail );
    }
    else
    {
	&Fatal( 998, 'Must not reache here(UIPostExecMain).' );
    }
}

sub hg_post_exec_jump_to_new_article
{
    &Fatal( 18, "$_[0]/PostExecJumpToNewArticle" ) if ( $_[0] ne 'PostExec.xml' );
    &DumpButtonToArticle( $BOARD, $gNewArtId, "書き込んだ$H_MESGへ" );
}

sub hg_supersede_exec_jump_to_new_article
{
    &Fatal( 18, "$_[0]/SupersedeExecJumpToNewArticle" ) if ( $_[0] ne 'SupersedeExec.xml' );
    &DumpButtonToArticle( $BOARD, $gNewArtId, "訂正した$H_MESGへ" );
}

sub hg_post_exec_jump_to_orig_article
{
    &Fatal( 18, "$_[0]/PostExecJumpToOrigArticle" ) if ( $_[0] ne 'PostExec.xml' );
    &DumpButtonToArticle( $BOARD, $gOrigId, "$H_ORIGの$H_MESGへ" ) if ( $gOrigId ne '' );
}


###
## スレッド別タイトルおよび記事一覧
#
sub UIThreadArticle
{
    # Isolation level: READ UNCOMITTED.
    &LockBoard();
    &DbCache( $BOARD ) if $BOARD;
    &UnlockBoard();

    %gADDFLAG = ();
    @gIDLIST = ();

    local( $nofMsg ) = &getNofMsg();

    # 表示する個数を取得
    $gNum = $cgi'TAGS{'num'};
    if ( defined( $cgi'TAGS{'id'} ))
    {
	$gOld = $nofMsg - int( $cgi'TAGS{'id'} + $gNum/2 );
	$gOld = 0 if ( $gOld < 0 );
    }
    else
    {
	$gOld = $cgi'TAGS{'old'};
    }
    $gRev = $cgi'TAGS{'rev'};
    $gFold = (( $SYS_THREAD_FORMAT == 2 ) || $cgi'TAGS{'fold'} )? 1 : 0;
    $gVRev = $gRev? 1-$SYS_BOTTOMTITLE : $SYS_BOTTOMTITLE;
    $gTo = $nofMsg - $gOld;
    $gFrom = $gTo - $gNum + 1;
    $gFrom = 0 if (( $gFrom < 0 ) || ( $gNum == 0 ));

    $gPageLinkStr = &PageLink( 'vt', $gNum, $gOld, $gRev, $gFold );

    # 整形済みフラグ
    # 0 ... 整形対象外
    # 1 ... 整形済み
    # 2 ... 未整形
    local( $IdNum, $Id );
    for ( $IdNum = $gFrom; $IdNum <= $gTo; $IdNum++ )
    {
	$gADDFLAG{ &getMsgId( $IdNum ) } = 2;
    }

    &htmlGen( 'ThreadArticle.xml' );
}

sub hg_thread_article_tree
{
    &Fatal( 18, "$_[0]/ThreadArticleTree" ) if ( $_[0] ne 'ThreadArticle.xml' );

    $gHgStr .= $HTML_HR;

    local( $AddNum ) = "&num=$gNum&old=$gOld&rev=$gRev";

    local( $Id, $IdNum, $Fid );
    if ( $gTo < $gFrom )
    {
	# 空だった……
	$gHgStr .= "<ul>\n<li>$H_NOARTICLE</li>\n</ul>\n";
    }
    elsif ( $gVRev )
    {
	$gHgStr .= "<ul>\n" if $gFold;

	for( $IdNum = $gFrom; $IdNum <= $gTo; $IdNum++ )
	{
	    # 該当記事のIDを取り出す
	    $Id = &getMsgId( $IdNum );
	    ( $Fid = &getMsgParents( $Id )) =~ s/,.*$//o;
	    # 後方参照は後回し．
	    next if (( $Fid ne '' ) && (( $gADDFLAG{$Fid} == 2 ) || ( $SYS_THREAD_FORMAT == 2 )));

	    # ノードを表示
	    $gHgStr .= "<ul>\n" unless $gFold;
	    if ( $gFold )
	    {
		&ThreadTitleNodeNoThread( $Id, 3 );
	    }
	    elsif ( $SYS_THREAD_FORMAT == 0 )
	    {
		&ThreadTitleNodeThread( $Id, 3 );
	    }
	    elsif ( $SYS_THREAD_FORMAT == 1 )
	    {
		&ThreadTitleNodeAllThread( $Id, 3 );
	    }
	    else
	    {
		&ThreadTitleNodeNoThread( $Id, 3 );
	    }
	    $gHgStr .= "</ul>\n" unless $gFold;
	    &cgiprint'Cache( $gHgStr ); $gHgStr = '';
	}
	$gHgStr .= "</ul>\n" if $gFold;
    }
    else
    {
	$gHgStr .= "<ul>\n" if $gFold;

	for( $IdNum = $gTo; $IdNum >= $gFrom; $IdNum-- )
	{
	    $Id = &getMsgId( $IdNum );
	    ( $Fid = &getMsgParents( $Id )) =~ s/,.*$//o;
	    next if (( $Fid ne '' ) && (( $gADDFLAG{$Fid} == 2 ) || ( $SYS_THREAD_FORMAT == 2 )));

	    $gHgStr .= "<ul>\n" unless $gFold;
	    if ( $gFold )
	    {
		&ThreadTitleNodeNoThread( $Id, 3 );
	    }
	    elsif ( $SYS_THREAD_FORMAT == 0 )
	    {
		&ThreadTitleNodeThread( $Id, 3 );
	    }
	    elsif ( $SYS_THREAD_FORMAT == 1 )
	    {
		&ThreadTitleNodeAllThread( $Id, 3 );
	    }
	    else
	    {
		&ThreadTitleNodeNoThread( $Id, 3 );
	    }
	    $gHgStr .= "</ul>\n" unless $gFold;
	    &cgiprint'Cache( $gHgStr ); $gHgStr = '';
	}
	$gHgStr .= "</ul>\n" if $gFold;
    }
}

sub hg_thread_article_body
{
    &Fatal( 18, "$_[0]/ThreadArticleBody" ) if ( $_[0] ne 'ThreadArticle.xml' );

    local( $id );
    if ( $#gIDLIST >= 0 )
    {
	$gHgStr .= $HTML_HR;
	while ( $id = shift( @gIDLIST ))
	{
	    &DumpArtBody( $id, $SYS_COMMAND_EACH, 1 );
	    $gHgStr .= $HTML_HR;
	}
    }
}


###
## スレッド別タイトル一覧
#
sub UIThreadTitle
{
    # Isolation level: READ UNCOMITTED.
    &LockBoard();
    &DbCache( $BOARD ) if $BOARD;

    ( $gComType ) = @_;

    if ( $gComType == 3 )
    {
	# リンクかけかえの実施
	&ReLinkExec( $cgi'TAGS{'rfid'}, $cgi'TAGS{'rtid'}, $BOARD );

	# DB書き換えたので，キャッシュし直す
	&DbCache( $BOARD );
    }
    elsif ( $gComType == 5 )
    {
	# 移動の実施
	&ReOrderExec( $cgi'TAGS{'rfid'}, $cgi'TAGS{'rtid'}, $BOARD );

	# DB書き換えたので，キャッシュし直す
	&DbCache( $BOARD );
    }

    &UnlockBoard();

    local( $vCom, $vStr );

    if ( $ComType == 0 )
    {
	$vCom = 'v';
	$vStr = '';
    }
    elsif ( $ComType == 2 )
    {
	$vCom = 'ct';
	$vStr = '&rtid=' . $cgi'TAGS{'roid'} . '&rfid=' . $cgi'TAGS{'rfid'} .
	    '&rtid=' . $cgi'TAGS{'rtid'};
    }
    elsif ( $gComType == 3 )
    {
	$vCom = 'v';
	$vStr = '';
    }
    elsif ( $gComType == 4 )
    {
	$vCom = 'mvt';
	$vStr = '&rtid=' . $cgi'TAGS{'roid'} . '&rfid=' . $cgi'TAGS{'rfid'} .
	    '&rtid=' . $cgi'TAGS{'rtid'};
    }
    elsif ( $gComType == 5 )
    {
	$vCom = 'v';
	$vStr = '';
    }

    %gADDFLAG = ();
    @gIDLIST = ();		# Not used here. It's for ThreadArticle.

    local( $nofMsg ) = &getNofMsg();

    # 表示する個数を取得
    $gNum = $cgi'TAGS{'num'};
    if ( defined( $cgi'TAGS{'id'} ))
    {
	$gOld = $nofMsg - int( $cgi'TAGS{'id'} + $gNum/2 );
	$gOld = 0 if ( $gOld < 0 );
    }
    else
    {
	$gOld = $cgi'TAGS{'old'};
    }
    $gRev = $cgi'TAGS{'rev'};
    $gFold = (( $SYS_THREAD_FORMAT == 2 ) || $cgi'TAGS{'fold'} )? 1 : 0;
    $gVRev = $gRev? 1-$SYS_BOTTOMTITLE : $SYS_BOTTOMTITLE;
    $gTo = $nofMsg - $gOld;
    $gFrom = $gTo - $gNum + 1;
    $gFrom = 0 if (( $gFrom < 0 ) || ( $gNum == 0 ));

    $gPageLinkStr = &PageLink( "$vCom$vStr", $gNum, $gOld, $gRev, $gFold );

    # 整形済みフラグ
    # 0 ... 整形対象外
    # 1 ... 整形済み
    # 2 ... 未整形
    local( $IdNum );
    for ( $IdNum = $gFrom; $IdNum <= $gTo; $IdNum++ )
    {
	$gADDFLAG{ &getMsgId( $IdNum ) } = 2;
    }

    &htmlGen( 'ThreadTitle.xml' );
}

sub hg_thread_title_board_header
{
    &Fatal( 18, "$_[0]/ThreadTitleBoardHeader" ) if ( $_[0] ne 'ThreadTitle.xml' );

    if ( $gComType == 2 )
    {
	$gHgStr .= "<p>新たな$H_REPLY先を指定します．\n";
	$gHgStr .= "$H_MESG「#" . $cgi'TAGS{'rfid'} . "」を，どの$H_MESGへの$H_REPLYにしますか? $H_REPLY先の$H_MESGの$H_RELINKTO_MARKをクリックしてください．</p>\n";
    }
    elsif ( $gComType == 3 )
    {
	$gHgStr .= "<p>指定された$H_MESGの$H_REPLY先を変更しました．</p>\n";
    }
    elsif ( $gComType == 4 )
    {
	$gHgStr .= "<p>移動先を指定します．\n";
	$gHgStr .= "$H_MESG「#" . $cgi'TAGS{'rfid'} . "」を，どの$H_MESGの下に移動しますか? $H_MESGの$H_REORDERTO_MARKをクリックしてください．</p>\n";
    }
    elsif ( $gComType == 5 )
    {
	$gHgStr .= "<p>指定された$H_MESGを移動しました．</p>\n";
    }

    &DumpBoardHeader();

    if ( $POLICY & 8 )
    {
	if ( $gComType == 3 )
	{
	    $gHgStr .= "<ul>\n<li>" . &LinkP( "b=$BOARD_ESC&c=ce&rtid=" .
		$cgi'TAGS{'roid'} . "&rfid=" . $cgi'TAGS{'rfid'},
		'今の変更を元に戻す' ) . "</li>\n</ul>\n";
	}

	$gHgStr .= <<EOS;
<p>各$H_ICONは，次のような意味を表しています．</p>
<ul>
<li>$H_RELINKFROM_MARK:
この$H_MESGの$H_REPLY先を変更します．$H_REPLY先を指定する画面に飛びます．</li>
<li>$H_REORDERFROM_MARK:
この$H_MESGの順序を変更します．移動先を指定する画面に飛びます．</li>
<li>$H_SUPERSEDE_ICON:
この$H_MESGを訂正します．</li>
<li>$H_DELETE_ICON:
この$H_MESGを削除します．</li>
<li>$H_RELINKTO_MARK:
先に指定した$H_MESGの$H_REPLY先を，この$H_MESGにします．</li>
<li>$H_REORDERTO_MARK:
先に指定した$H_MESGを，この$H_MESGの下に移動します．</li>
</ul>
EOS
    }
}

sub hg_thread_title_tree
{
    &Fatal( 18, "$_[0]/ThreadTitleTree" ) if ( $_[0] ne 'ThreadTitle.xml' );

    local( $AddNum ) = "&num=$gNum&old=$gOld&rev=$gRev";

    local( $IdNum, $Id, $Fid );
    if ( $gTo < $gFrom )
    {
	# 空だった……
	$gHgStr .= "<ul>\n<li>$H_NOARTICLE</li>\n</ul>\n";
    }
    elsif ( $gVRev )
    {
	# 古いのから処理
	if (( $gComType == 2 ) && ( &getMsgParents( $cgi'TAGS{'rfid'} ) ne '' ))
	{
	    $gHgStr .= '<ul><li>' . &LinkP( "b=$BOARD_ESC&c=ce&rtid=&rfid=" .
		$cgi'TAGS{'rfid'} . '&roid=' . $cgi'TAGS{'roid'} . $AddNum,
		"[どの$H_MESGへの$H_REPLYでもなく，新着$H_MESGにする]" ) .
		"</li></ul>\n";
	}
	elsif ( $gComType == 4 )
	{
	    $gHgStr .= '<ul><li>' . &LinkP( "b=$BOARD_ESC&c=mve&rtid=&rfid=" .
		$cgi'TAGS{'rfid'} . "&roid=" . $cgi'TAGS{'roid'} . $AddNum,
		"[全記事の先頭に移動する(このページの，ではありません)]" ) .
		"</li></ul>\n";
	}

	$gHgStr .= "<ul>\n" if $gFold;

	for( $IdNum = $gFrom; $IdNum <= $gTo; $IdNum++ )
	{
	    # 該当記事のIDを取り出す
	    $Id = &getMsgId( $IdNum );
	    ( $Fid = &getMsgParents( $Id )) =~ s/,.*$//o;
	    # 後方参照は後回し．
	    next if (( $Fid ne '' ) && (( $gADDFLAG{$Fid} == 2 ) ||
		( $SYS_THREAD_FORMAT == 2 )));

	    # ノードを表示
	    $gHgStr .= "<ul>\n" unless $gFold;
	    if ( $gFold )
	    {
		&ThreadTitleNodeNoThread( $Id, 1, $AddNum, ( $POLICY & 8 ));
	    }
	    elsif ( $SYS_THREAD_FORMAT == 0 )
	    {
		&ThreadTitleNodeThread( $Id, 1, $AddNum, ( $POLICY & 8 ));
	    }
	    elsif ( $SYS_THREAD_FORMAT == 1 )
	    {
		&ThreadTitleNodeAllThread( $Id, 1, $AddNum, ( $POLICY & 8 ));
	    }
	    else
	    {
		&ThreadTitleNodeNoThread( $Id, 1, $AddNum, ( $POLICY & 8 ));
	    }
	    $gHgStr .= "</ul>\n" unless $gFold;
	    &cgiprint'Cache( $gHgStr ); $gHgStr = '';
	}
	$gHgStr .= "</ul>\n" if $gFold;
    }
    else
    {
	# 新しいのから処理
	if (( $gComType == 2 ) && ( &getMsgParents( $cgi'TAGS{'rfid'} ) ne '' ))
	{
	    $gHgStr .= '<ul><li>' . &LinkP( "b=$BOARD_ESC&c=ce&rtid=&rfid=" .
		$cgi'TAGS{'rfid'} . "&roid=" . $cgi'TAGS{'roid'} . $AddNum,
		"[どの$H_MESGへの$H_REPLYでもなく，新着$H_MESGにする]" ) .
		"</li></ul>\n";
	}
	elsif ( $gComType == 4 )
	{
	    $gHgStr .= '<ul><li>' . &LinkP( "b=$BOARD_ESC&c=mve&rtid=&rfid=" .
		$cgi'TAGS{'rfid'} . "&roid=" . $cgi'TAGS{'roid'} . $AddNum,
		"[全記事の先頭に移動する(このページの，ではありません)]" ) .
		"</li></ul>\n";
	}

	$gHgStr .= "<ul>\n" if $gFold;

	for( $IdNum = $gTo; $IdNum >= $gFrom; $IdNum-- )
	{
	    # 後は同じ
	    $Id = &getMsgId( $IdNum );
	    ( $Fid = &getMsgParents( $Id )) =~ s/,.*$//o;
	    next if (( $Fid ne '' ) && (( $gADDFLAG{$Fid} == 2 ) ||
		( $SYS_THREAD_FORMAT == 2 )));

	    $gHgStr .= "<ul>\n" unless $gFold;
	    if ( $gFold )
	    {
		&ThreadTitleNodeNoThread( $Id, 1, $AddNum, ( $POLICY & 8 ));
	    }
	    elsif ( $SYS_THREAD_FORMAT == 0 )
	    {
		&ThreadTitleNodeThread( $Id, 1, $AddNum, ( $POLICY & 8 ));
	    }
	    elsif ( $SYS_THREAD_FORMAT == 1 )
	    {
		&ThreadTitleNodeAllThread( $Id, 1, $AddNum, ( $POLICY & 8 ));
	    }
	    else
	    {
		&ThreadTitleNodeNoThread( $Id, 1, $AddNum, ( $POLICY & 8 ));
	    }
	    $gHgStr .= "</ul>\n" unless $gFold;
	    &cgiprint'Cache( $gHgStr ); $gHgStr = '';
	}
	$gHgStr .= "</ul>\n" if $gFold;
    }
}

# 新着ノードのみ表示
sub ThreadTitleNodeNoThread
{
    local( $id, $flag, $addNum, $maint ) = @_;

    local( $fid, $aids, $date, $title, $icon, $host, $name ) = &getMsgInfo( $id );
    &DumpArtSummaryItem( $id, $aids, $date, $title, $icon, $name, $flag );

    $flag &= 6; # 110
    push( @gIDLIST, $id );

    &ThreadTitleMaintIcon( $id, $addNum ) if $maint;

    $gHgStr .= "</li>\n";
}

# ページ内スレッドのみ表示
sub ThreadTitleNodeThread
{
    local( $id, $flag, $addNum, $maint ) = @_;

    # ページ外ならおしまい．
    return if ( $gADDFLAG{ $id } != 2 );

    local( $fid, $aids, $date, $title, $icon, $host, $name ) = &getMsgInfo( $id );
    &DumpArtSummaryItem( $id, $aids, (( !$SYS_COMPACTTHREAD || $flag&1 )? $date : 0 ), $title, $icon, $name, $flag );

    $flag &= 6; # 110
    $gADDFLAG{ $id } = 1;		# 整形済み
    push( @gIDLIST, $id );

    &ThreadTitleMaintIcon( $id, $addNum ) if $maint;

    # 娘が居れば……
    if ( $aids )
    {
	$gHgStr .= "<ul>\n";
	foreach ( split( /,/, $aids ))
	{
	    &ThreadTitleNodeThread( $_, $flag, $addNum, $maint );
	}
	$gHgStr .= "</ul>\n";
    }
    $gHgStr .= "</li>\n";
}

# 全スレッドの表示
sub ThreadTitleNodeAllThread
{
    local( $id, $flag, $addNum, $maint ) = @_;

    # 表示済みならおしまい．
    return if ( $gADDFLAG{ $id } == 1 );

    local( $fid, $aids, $date, $title, $icon, $host, $name ) = &getMsgInfo( $id );
    &DumpArtSummaryItem( $id, $aids, (( !$SYS_COMPACTTHREAD || $flag&1 )? $date : 0 ), $title, $icon, $name, $flag );

    $flag &= 6; # 110
    $gADDFLAG{ $id } = 1;		# 整形済み
    push( @gIDLIST, $id );

    &ThreadTitleMaintIcon( $id, $addNum ) if $maint;

    # 娘が居れば……
    if ( $aids )
    {
	$gHgStr .= "<ul>\n";
	foreach ( split( /,/, $aids ))
	{
	    &ThreadTitleNodeAllThread( $_, $flag, $addNum, $maint );
	}
	$gHgStr .= "</ul>\n";
    }
    $gHgStr .= "</li>\n";
}

# 管理者用のアイコン表示
sub ThreadTitleMaintIcon
{
    local( $id, $addNum ) = @_;

    $gHgStr .= " .......... \n";

    local( $fromId ) = $cgi'TAGS{'rfid'};
    local( $oldId ) = $cgi'TAGS{'roid'};

    local( $parents ) = &getMsgParents( $id );

    # リンク先変更コマンド(From)
    $gHgStr .= &LinkP( "b=$BOARD_ESC&c=ct&rfid=$id&roid=" . $parents . $addNum,
	$H_RELINKFROM_MARK, '', $H_RELINKFROM_MARK_L ) . "\n";

    if ( $parents eq '' )
    {
	# 移動コマンド(From)
	$gHgStr .= &LinkP( "b=$BOARD_ESC&c=mvt&rfid=$id&roid=" . $parents .
	    $addNum, $H_REORDERFROM_MARK, '', $H_REORDERFROM_MARK_L ) . "\n";
    }

    # 削除・訂正コマンド
    $gHgStr .= &LinkP( "b=$BOARD_ESC&c=f&s=on&id=$id", $H_SUPERSEDE_ICON, '',
	$H_SUPERSEDE_ICON_L ) . "\n";
    $gHgStr .= &LinkP( "b=$BOARD_ESC&c=dp&id=$id", $H_DELETE_ICON, '',
	$H_DELETE_ICON_L ) . "\n";

    # 移動コマンド(To)
    if (( $gComType == 4 ) && ( $fromId ne $id ) && ( $parents eq '' ) && ( $fromId ne $id ))
    {
	$gHgStr .= &LinkP(
	    "b=$BOARD_ESC&c=mve&rtid=$id&rfid=$fromId&roid=$oldId" .
	    $addNum, $H_REORDERTO_MARK, '', $H_REORDERTO_MARK_L ) . "\n";
    }

    # リンク先変更コマンド(To)
    if (( $gComType == 2 ) && ( $fromId ne $id ) &&
	( !grep( /^$fromId$/, split( /,/, &getMsgDaughters( $id )))) &&
	( !grep( /^$fromId$/, split( /,/, $parents ))))
    {
	$gHgStr .= &LinkP( "b=$BOARD_ESC&c=ce&rtid=$id&rfid=$fromId&roid=$oldId" . $addNum, $H_RELINKTO_MARK, '', $H_RELINKTO_MARK_L ) . "\n";
    }
}


###
## 書き込み順タイトル一覧
#
sub UISortTitle
{
    # Isolation level: READ UNCOMITTED.
    &LockBoard();
    &DbCache( $BOARD ) if $BOARD;
    &UnlockBoard();

    local( $nofMsg ) = &getNofMsg();

    # 表示する個数を取得
    local( $Num ) = $cgi'TAGS{'num'};
    local( $Old );
    if ( defined( $cgi'TAGS{'id'} ))
    {
	$Old = $nofMsg - int( $cgi'TAGS{'id'} + $Num/2 );
	$Old = 0 if ( $Old < 0 );
    }
    else
    {
	$Old = $cgi'TAGS{'old'};
    }
    local( $Rev ) = $cgi'TAGS{'rev'};
    $gFold = (( $SYS_THREAD_FORMAT == 2 ) || $cgi'TAGS{'fold'} )? 1 : 0;
    $gVRev = $Rev? 1-$SYS_BOTTOMTITLE : $SYS_BOTTOMTITLE;
    $gTo = $nofMsg - $Old;
    $gFrom = $gTo - $Num + 1;
    $gFrom = 0 if (( $gFrom < 0 ) || ( $Num == 0 ));

    $gPageLinkStr = &PageLink( 'r', $Num, $Old, $Rev, '' );

    &htmlGen( 'SortTitle.xml' );
}

sub hg_sort_title_tree
{
    &Fatal( 18, "$_[0]/SortTitleTree" ) if ( $_[0] ne 'SortTitle.xml' );

    $gHgStr .= "<ul>\n";

    # 記事の表示
    local( $IdNum, $Id, $fid, $aids, $date, $title, $icon, $host, $name );

    local( $nofMsg ) = &getNofMsg();
    if ( $nofMsg == -1 )
    {
	# 空だった……
	$gHgStr .= "<li>$H_NOARTICLE</li>\n";
    }
    else
    {
	if ( $gVRev )
	{
	    for ($IdNum = $gFrom; $IdNum <= $gTo; $IdNum++)
	    {
		$Id = &getMsgId( $IdNum );
		( $fid, $aids, $date, $title, $icon, $host, $name ) = &getMsgInfo( $Id );
		&DumpArtSummaryItem( $Id, $aids, $date, $title, $icon, $name, 1 );
		$gHgStr .= "</li>\n";
	    }
	}
	else
	{
	    for ($IdNum = $gTo; $IdNum >= $gFrom; $IdNum--)
	    {
		$Id = &getMsgId( $IdNum );
		( $fid, $aids, $date, $title, $icon, $host, $name ) = &getMsgInfo( $Id );
		&DumpArtSummaryItem( $Id, $aids, $date, $title, $icon, $name, 1 );
		$gHgStr .= "</li>\n";
	    }
	}
    }
    $gHgStr .= "</ul>\n";
}


###
## スレッド別記事一覧
#
sub UIShowThread
{
    # Isolation level: READ UNCOMITTED.
    &LockBoard();
    &DbCache( $BOARD ) if $BOARD;
    &UnlockBoard();

    $gId = $cgi'TAGS{'id'};

    $gFids = &getMsgParents( $gId );

    # フォロー記事の木構造の取得
    # ex. '( a ( b ( c d ) ) ( e ) ( f ( g ) ) )'というリスト
    @gFollowIdTree = ();
    &GetFollowIdTree( $gId, *gFollowIdTree );

    &htmlGen( 'ShowThread.xml' );
}

sub hg_show_thread_title
{
    &Fatal( 18, "$_[0]/ShowThreadTitle" ) if ( $_[0] ne 'ShowThread.xml' );
    $gHgStr .= &getMsgSubject( &GetTreeTopArticle( *gFollowIdTree ));
}

sub hg_show_thread_title_tree
{
    &Fatal( 18, "$_[0]/ShowThreadTitleTree" ) if ( $_[0] ne 'ShowThread.xml' );

    &DumpOriginalArticles( $gFids );
    &DumpArtThread( 6, @gFollowIdTree );
}

sub hg_show_thread_msg_body
{
    &Fatal( 18, "$_[0]/ShowThreadMsgBody" ) if ( $_[0] ne 'ShowThread.xml' );
    &DumpArtThread( 2, @gFollowIdTree );
}

sub hg_show_thread_back_to_title_button
{
    &Fatal( 18, "$_[0]/ShowThreadBackToTitleButton" ) if ( $_[0] ne 'ShowThread.xml' );
    &DumpButtonToTitleList( $BOARD, $gId );
}


###
## 書き込み順メッセージ一覧
#
sub UISortArticle
{
    # Isolation level: READ UNCOMITTED.
    &LockBoard();
    &DbCache( $BOARD ) if $BOARD;
    &UnlockBoard();

    $gNum = $cgi'TAGS{'num'};
    $gOld = $cgi'TAGS{'old'};
    $gRev = $cgi'TAGS{'rev'};
    $gFold = (( $SYS_THREAD_FORMAT == 2 ) || $cgi'TAGS{'fold'} )? 1 : 0;

    $gPageLinkStr = &PageLink( 'l', $gNum, $gOld, $gRev, '' );

    &htmlGen( 'SortArticle.xml' );
}

sub hg_sort_article_body
{
    &Fatal( 18, "$_[0]/SortArticleBody" ) if ( $_[0] ne 'SortArticle.xml' );

    local( $vRev ) = $gRev? 1-$SYS_BOTTOMARTICLE : $SYS_BOTTOMARTICLE;
    local( $nofMsg ) = &getNofMsg();
    local( $To ) = $nofMsg - $gOld;
    local( $From ) = $To - $gNum + 1; $From = 0 if (( $From < 0 ) || ( $gNum == 0 ));

    $gHgStr .= $HTML_HR;

    if ( $nofMsg == -1 )
    {
	# 空だった……
	$gHgStr .= "<p>$H_NOARTICLE</p>\n";
    }
    else
    {
	local( $IdNum, $Id );
	if ( $vRev )
	{
	    for ( $IdNum = $From; $IdNum <= $To; $IdNum++ )
	    {
		$Id = &getMsgId( $IdNum );
		&DumpArtBody( $Id, $SYS_COMMAND_EACH, 1 );
		$gHgStr .= $HTML_HR;
	    }
	}
	else
	{
	    for ( $IdNum = $To; $IdNum >= $From; $IdNum-- )
	    {
		$Id = &getMsgId( $IdNum );
		&DumpArtBody( $Id, $SYS_COMMAND_EACH, 1 );
		$gHgStr .= $HTML_HR;
	    }
	}
    }
}


###
## 単一記事の表示
#
sub UIShowArticle
{
    # Isolation level: READ UNCOMITTED.
    &LockBoard();
    &DbCache( $BOARD ) if $BOARD;
    &UnlockBoard();

    $gId = $cgi'TAGS{'id'};

    # 未投稿記事は読めない
    &Fatal( 8, '' ) if ( &getMsgSubject( $gId ) eq '' );

    &htmlGen( 'ShowArticle.xml' );
}

sub hg_show_article_title
{
    &Fatal( 18, "$_[0]/ShowArticleTitle" ) if ( $_[0] ne 'ShowArticle.xml' );
    $gHgStr .= &getMsgSubject( $gId );
}

sub hg_show_article_body
{
    &Fatal( 18, "$_[0]/ShowArticleBody" ) if ( $_[0] ne 'ShowArticle.xml' );
    &DumpArtBody( $gId, 1, 1 );
}

sub hg_show_article_original
{
    &Fatal( 18, "$_[0]/ShowArticleOriginal" ) if ( $_[0] ne 'ShowArticle.xml' );
    local( $fids ) = &getMsgParents( $gId );
    if ( $fids ne '' )
    {
	$gHgStr .= "<p>▼$H_ORIG</p>\n";
	&DumpOriginalArticles( $fids );
    }
}

sub hg_show_article_reply
{
    &Fatal( 18, "$_[0]/ShowArticleReply" ) if ( $_[0] ne 'ShowArticle.xml' );

    $gHgStr .= "<p>▼$H_REPLY</p>\n";
    &DumpReplyArticles( &getMsgDaughters( $gId ));
}


###
## 記事の検索(表示画面の作成)
#
sub UISearchArticle
{
    # Isolation level: READ UNCOMITTED.
    &LockBoard();
    &DbCache( $BOARD ) if $BOARD;
    &UnlockBoard();

    &htmlGen( 'SearchArticle.xml' );
}

sub hg_search_article_result
{
    &Fatal( 18, "$_[0]/SearchArticleResult" ) if ( $_[0] ne 'SearchArticle.xml' );

    local( $Key ) = $cgi'TAGS{'key'};
    local( $SearchSubject ) = $cgi'TAGS{'searchsubject'};
    local( $SearchPerson ) = $cgi'TAGS{'searchperson'};
    local( $SearchArticle ) = $cgi'TAGS{'searcharticle'};
    local( $SearchPostTime ) = $cgi'TAGS{'searchposttime'};
    local( $SearchPostTimeFrom ) = $cgi'TAGS{'searchposttimefrom'};
    local( $SearchPostTimeTo ) = $cgi'TAGS{'searchposttimeto'};
    local( $SearchIcon ) = $cgi'TAGS{'searchicon'};
    local( $Icon ) = $cgi'TAGS{'icon'};

    # キーワードが空でなければ，そのキーワードを含む記事のリストを表示
    if ( $SearchIcon || ( $SearchPostTime && ( $SearchPostTimeFrom ||
	$SearchPostTimeTo )) || (( $Key ne '' ) && ( $SearchSubject ||
	$SearchPerson || $SearchArticle )))
    {
	&DumpSearchResult( $Key, $SearchSubject, $SearchPerson,
	    $SearchArticle, $SearchPostTime, $SearchPostTimeFrom,
	    $SearchPostTimeTo, $SearchIcon, $Icon );
    }
}


###
## 削除記事の確認
#
sub UIDeletePreview
{
    # Isolation level: READ UNCOMITTED.
    &LockBoard();
    &DbCache( $BOARD ) if $BOARD;
    &UnlockBoard();

    if ( !( $POLICY & 8 ) && ( $SYS_OVERWRITE == 0 ))
    {
	&Fatal( 99, $cgi'TAGS{'c'} );
    }

    $gId = $cgi'TAGS{'id'};
    $gAids = &getMsgDaughters( $gId );

    # 未投稿記事は読めない
    &Fatal( 8, '' ) if ( &getMsgSubject( $gId ) eq '' );

    &htmlGen( 'DeletePreview.xml' );
}

sub hg_delete_preview_form
{
    &Fatal( 18, "$_[0]/DeletePreviewForm" ) if ( $_[0] ne 'DeletePreview.xml' );

    local( %tags );
    %tags = ( 'c', 'de', 'b', $BOARD, 'id', $gId );
    &DumpForm( *tags, 'このメッセージを削除します', '', '' );

    if ( $gAids )
    {
	%tags = ( 'c', 'det', 'b', $BOARD, 'id', $gId );
	&DumpForm( *tags, "$H_REPLYメッセージもまとめて削除します", '', '' );
    }
}

sub hg_delete_preview_body
{
    &Fatal( 18, "$_[0]/DeletePreviewBody" ) if ( $_[0] ne 'DeletePreview.xml' );
    &DumpArtBody( $gId, 0, 1 );
}

sub hg_delete_preview_reply
{
    &Fatal( 18, "$_[0]/DeletePreviewReply" ) if ( $_[0] ne 'DeletePreview.xml' );

    $gHgStr .= "<p>▼$H_REPLY</p>\n";
    &DumpReplyArticles( $gAids );
}


###
## 記事の削除
#
sub UIDeleteExec
{
    # Isolation level: SERIALIZABLE.
    &LockBoard();
    &DbCache( $BOARD ) if $BOARD;

    if ( !( $POLICY & 8 ) && ( $SYS_OVERWRITE == 0 ))
    {
	&Fatal( 99, $cgi'TAGS{'c'} );
    }

    local( $threadFlag ) = @_;

    $gId = $cgi'TAGS{'id'};

    local( $name ) = &getMsgAuthor( $gId );
    &Fatal( 44, '' ) if ( !&IsUser( $name ) && !( $POLICY & 8 ));
    &Fatal( 19, '' ) if (( &getMsgDaughters( $gId ) ne '' ) && ( $SYS_OVERWRITE == 1 ));

    # 削除実行
    &DeleteArticle( $gId, $BOARD, $threadFlag );

    &htmlGen( 'DeleteExec.xml' );

    &UnlockBoard();
}

sub hg_delete_exec_back_to_title_button
{
    &Fatal( 18, "$_[0]/DeleteExecBackToTitleButton" ) if ( $_[0] ne 'DeleteExec.xml' );
    &DumpButtonToTitleList( $BOARD, $gId );
}


###
## アイコン表示
#
sub UIShowIcon
{
    # Isolation level: CHAOS.

    &htmlGen( 'ShowIcon.xml' );
}


###
## ヘルプ表示
#
sub UIHelp
{
    # Isolation level: CHAOS.

    &htmlGen( 'Help.xml' );
}


###
## エラー表示
#
sub UIFatal
{
    # Isolation level: CHAOS.

    ( $gMsg ) = @_;
    &htmlGen( 'Fatal.xml' );
}

sub hg_fatal_msg
{
    $gHgStr .= $gMsg;
}


###
## 汎用hg関数群
#
sub hg_s_title
{
    $gHgStr .= <<EOS;
<meta http-equiv="Content-Type" content='text/html; charset="EUC-JP"' />
<meta http-equiv="Content-Style-Type" content="text/css" />
<link rev="MADE" href="mailto:$MAINT" />
EOS

    $gHgStr .= sprintf( qq(<link rel="StyleSheet" href="%s" type="text/css" media="screen" />), &GetStyleSheetURL( $STYLE_FILE )) if $STYLE_FILE;
}

sub hg_s_address
{
    $gHgStr .= "<address>\nMaintenance: " .
	&TagA( $MAINT_NAME, "mailto:$MAINT" ) . $HTML_BR .
	&TagA( $PROGNAME, 'http://www.jin.gr.jp/~nahi/kb/' ) .
	": Copyright &copy; 1995-2000 " .
	&TagA( 'NAKAMURA, Hiroshi', 'http://www.jin.gr.jp/~nahi/' ) .
	".\n</address>\n";
}

sub hg_c_status
{
    $gHgStr .= qq(<p class="kbStatus">[);
    if ( $UNAME && ( $UNAME ne $GUEST ) && ( $UNAME ne $cgiauth'F_COOKIE_RESET ))
    {
	$gHgStr .= "$H_USER: $UNAME -- \n";
    }
    $gHgStr .= "$H_BOARD: $BOARDNAME -- \n" if ( $BOARDNAME ne '' );
    $gHgStr .= "時刻: " . &GetDateTimeFormatFromUtc( $^T );
    $gHgStr .= "]</p>\n";
}

sub hg_c_remote_info
{
    $gHgStr .= $REMOTE_INFO;
}

sub hg_c_auth_user
{
    if ( $UNAME && ( $UNAME ne $GUEST ) && ( $UNAME ne $cgiauth'F_COOKIE_RESET ))
    {
	$gHgStr .= $UNAME;
    }
    else
    {
	$gHgStr .= $GUEST;
    }
}

sub hg_c_exec_date_time
{
    $gHgStr .= &GetDateTimeFormatFromUtc( $^T );
}

sub hg_c_top_menu
{
    $gHgStr .= qq(<div class="kbTopMenu">\n);
    local( $formStr, $contents );

    if ( $SYS_AUTH )
    {
	$formStr .= &LinkP( 'c=bl', 'TOP', 'J' ) . "\n";
#	$formStr .= ' ' . &LinkP( 'c=ue', 'OPEN', 'O' ) . "\n";
	$formStr .= ' ' . &LinkP( 'c=lo', 'LOGIN', 'L' ) . "\n";
	if ( $UNAME && ( $UNAME ne $GUEST ) && ( $UNAME ne $cgiauth'F_COOKIE_RESET ))
	{
	    $formStr .= ' ' . &LinkP( 'c=uc', 'INFO', 'C' ) . "\n";
	}
	$formStr .= "&nbsp;&nbsp;&nbsp;\n";
    }

    $formStr .= &TagLabel( "表示画面", 'c', 'W' ) . ": \n";

    if ( $BOARD )
    {
	$contents .= sprintf( qq[<option%s value="v">最新$H_SUBJECT一覧(スレッド)</option>\n], ( $SYS_TITLE_FORMAT == 0 )? ' selected="selected"' : '' );
	$contents .= sprintf( qq[<option%s value="r">最新$H_SUBJECT一覧(書き込み順)</option>\n], ( $SYS_TITLE_FORMAT == 1 )? ' selected="selected"' : '' );
	$contents .= qq[<option value="vt">最新$H_MESG一覧(スレッド)</option>\n];
	$contents .= qq[<option value="l">最新$H_MESG一覧(書き込み順)</option>\n];
	$contents .= qq(<option value="v">--------</option>\n);
	$contents .= qq(<option value="s">$H_MESGの検索</option>\n);
	$contents .= qq(<option value="i">使える$H_ICON一覧</option>\n) if $SYS_ICON;
	if (( $POLICY & 2 ) && ( !$SYS_NEWART_ADMINONLY || ( $POLICY & 8 )))
	{
	    $contents .= qq(<option value="v">--------</option>\n);
	    $contents .= qq(<option value="n">$H_POSTNEWARTICLE</option>\n);
	}
    }
    else
    {
	$contents .= qq(<option selected="selected" value="bl">$H_BOARD一覧</option>\n);
    }

    $formStr .= &TagSelect( 'c', $contents ) . "\n&nbsp;&nbsp;&nbsp;" .
	&TagLabel( "表示件数", 'num', 'Y' ) . ': ' .
	&TagInputText( 'text', 'num', (( $cgi'TAGS{'num'} ne '' )? $cgi'TAGS{'num'} : $DEF_TITLE_NUM ),	3 );

    local( %tags ) = ( 'b', $BOARD );
    $tags{ 'old' } = $cgi'TAGS{'old'} if ( defined $cgi'TAGS{'old'} );
    $tags{ 'rev' } = $cgi'TAGS{'rev'} if ( defined $cgi'TAGS{'rev'} );
    $tags{ 'fold' } = $cgi'TAGS{'fold'} if ( defined $cgi'TAGS{'fold'} );
    &DumpForm( *tags, '表示(V)', '', *formStr );
    $gHgStr .= "</div>\n";
}

sub hg_c_help
{
    $gHgStr .= &LinkP( "b=$BOARD_ESC&c=h", &TagComImg( $ICON_HELP, 'ヘルプ' ), 'H', '', '', $_[1] );
}

sub hg_c_site_name
{
    $gHgStr .= $SYSTEM_NAME;
}

sub hg_c_func_link
{
    return unless $SYS_AUTH;

    $gHgStr .= "<dl>\n";

    $gHgStr .= "<dt>「新規に$H_USER情報をサーバに登録する」</dt>\n";
    $gHgStr .= '<dd>→' . &LinkP( 'c=ue', "$H_USERアカウント作成ページ" .
	&TagAccessKey( 'O' ), 'O' ) . "</dd>\n";

    if ( $UNAME )
    {
	$gHgStr .= "<dt>「別の$H_USER情報を呼び出す」（現在利用中の$H_USER情報は，$UNAMEのものです）</dt>\n";
	$gHgStr .= '<dd>→' . &LinkP( 'c=lo', "ログインページ" . &TagAccessKey( 'L' ), 'L' ) . "</dd>\n";
    }

    if ( $POLICY & 4 )
    {
	$gHgStr .= "<dt>「$UNAMEについて登録した$H_USER情報を変更する」</dt>\n";
	$gHgStr .= '<dd>→' . &LinkP( 'c=uc', "$H_USER情報ページ" . &TagAccessKey( 'C' ), 'C' ) . "</dd>\n";
    }

    if ( $POLICY & 8 )
    {
	$gHgStr .= "<dt>「新規に$H_BOARDを作りたい」</dt>\n";
	$gHgStr .= '<dd>→' . &LinkP( 'c=be', "$H_BOARDの新規作成" .
	    &TagAccessKey( 'A' ), 'A' ) . "</dd>\n";
    }

    $gHgStr .= "</dl>\n";
}

sub hg_c_page_link
{
    $gHgStr .= $gPageLinkStr;
}

sub hg_c_board_link_all
{
    # 全掲示板の情報を取り出す
    local( @board, %boardName, %boardInfo );
    &GetAllBoardInfo( *board, *boardName, *boardInfo );

    $gHgStr .= "<ul>\n";

    local( $newIcon, $modTimeUtc, $modTime, $nofArticle, $boardEsc );
    foreach ( @board )
    {
	$modTimeUtc = &getBoardLastmod( $_ );
	$modTime = &GetDateTimeFormatFromUtc( $modTimeUtc );
	if ( $SYS_BLIST_NEWICON_DATE &&
	    (( $^T - $modTimeUtc ) < $SYS_BLIST_NEWICON_DATE * 86400 ))
	{
	    $newIcon = " " . &TagMsgImg( $H_NEWARTICLE );
	}
	else
	{
	    $newIcon = '';
	}
	&GetArticleId( $_, *nofArticle ) || 0;

	$boardEsc = &URIEscape( $_ );
	$gHgStr .= '<li>' .
	    &LinkP( "b=$boardEsc&c=" . ( $SYS_TITLE_FORMAT? 'r' : 'v' ) .
	    "&num=$DEF_TITLE_NUM", $boardName{$_} ) .
	    "$newIcon\n[最新: $modTime, 最新${H_MESG}ID: $nofArticle]\n";
	if ( $POLICY & 8 )
	{
	    $gHgStr .= &LinkP( "b=$boardEsc&c=bc", "←設定変更" ) . "\n";
	}

	$gHgStr .= $HTML_BR . $HTML_BR . "</li>\n";
    }
    $gHgStr .= "</ul>\n";
}

sub hg_c_board_link
{
    local( $com, $board ) = split( ',', $_[1], 2 );
    local( $num );
    return unless $board;
    if ( $com eq 'title-thread' )
    {
	$com = 'v';
	$num = $DEF_TITLE_NUM;
    }
    elsif ( $com eq 'title-bydate' )
    {
	$com = 'r';
	$num = $DEF_TITLE_NUM;
    }
    elsif ( $com eq 'message-thread' )
    {
	$com = 'vt';
	$num = $DEF_ARTICLE_NUM;
    }
    elsif ( $com eq 'message-bydate' )
    {
	$com = 'l';
	$num = $DEF_ARTICLE_NUM;
    }
    else
    {
	return;
    }

    if ( !$gBoardInfoDbCached )
    {
	local( $tmp );
	&GetAllBoardInfo( *tmp, *gBoardName, *tmp );
	$gBoardInfoDbCached = 1;
    }

    $modTimeUtc = &getBoardLastmod( $board );
    $modTime = &GetDateTimeFormatFromUtc( $modTimeUtc );
    if ( $SYS_BLIST_NEWICON_DATE &&
	(( $^T - $modTimeUtc ) < $SYS_BLIST_NEWICON_DATE * 86400 ))
    {
	$newIcon = " " . &TagMsgImg( $H_NEWARTICLE );
    }
    else
    {
	$newIcon = '';
    }
    &GetArticleId( $board, *nofArticle ) || 0;

    local( $boardEsc ) = &URIEscape( $board );
    $gHgStr .= &LinkP( "b=$boardEsc&c=$com&num=$num", $gBoardName{$board} ) .
	"$newIcon\n[最新: $modTime, 最新${H_MESG}ID: $nofArticle]\n";
    if ( $POLICY & 8 )
    {
	$gHgStr .= &LinkP( "b=$boardEsc&c=bc", "←設定変更" ) . "\n";
    }
}

sub hg_c_anchor
{
    $gHgStr .= &TagA( split( ',', $_[1] ));
}

sub hg_c_icon_msg
{
    $gHgStr .= &TagMsgImg( $_[1] );
}

sub hg_c_icon
{
    local( $src, $alt ) = split( ',', $_[1], 2 );
    $gHgStr .= &TagComImg( &GetIconURL( $src ), $alt );
}

sub hg_b_board_name
{
    $gHgStr .= $BOARDNAME if $BOARD;
}

sub hg_b_board_header
{
    &DumpBoardHeader() if $BOARD;
}

sub hg_b_post_entry_form
{
    if ( $POLICY & 2 )
    {
	&DumpArtEntry( $gDefIcon, $gEntryType, $gId, $gDefPostDateStr, $gDefSubject, $gDefTextType, $gDefArticle, $gDefName, $gDefEmail, $gDefUrl, $gDefFmail );
    }
}

sub hg_b_search_article_form
{
    local( $Key ) = $cgi'TAGS{'key'};
    local( $SearchSubject ) = $cgi'TAGS{'searchsubject'};
    local( $SearchPerson ) = $cgi'TAGS{'searchperson'};
    local( $SearchArticle ) = $cgi'TAGS{'searcharticle'};
    local( $SearchPostTime ) = $cgi'TAGS{'searchposttime'};
    local( $SearchPostTimeFrom ) = $cgi'TAGS{'searchposttimefrom'};
    local( $SearchPostTimeTo ) = $cgi'TAGS{'searchposttimeto'};
    local( $SearchIcon ) = $cgi'TAGS{'searchicon'};
    local( $Icon ) = $cgi'TAGS{'icon'};

    local( $msg, $contents );
    $contents = &TagInputCheck( 'searchsubject', $SearchSubject ) . ': ' . &TagLabel( $H_SUBJECT, 'searchsubject', 'T' ) . $HTML_BR;

    $contents .= &TagInputCheck( 'searchperson', $SearchPerson ) . ': ' . &TagLabel( "名前", 'searchperson', 'N' ) . $HTML_BR;

    $contents .= &TagInputCheck( 'searcharticle', $SearchArticle ) . ': ' . &TagLabel( $H_MESG, 'searcharticle', 'A' ) . $HTML_BR;

    local( $sec, $min, $hour, $mday, $mon, $year, $nowStr );
    if ( !$SearchPostTime )
    {
	( $sec, $min, $hour, $mday, $mon, $year, $nowStr ) = localtime( $^T );
	$nowStr = sprintf( "%04d/%02d/%02d", $year+1900, $mon+1, $mday );
    }
    $contents .= &TagInputCheck( 'searchposttime', $SearchPostTime ) . ': ' . &TagLabel( $H_DATE, 'searchposttime', 'D' ) . " // \n";
    $contents .= &TagInputText( 'text', 'searchposttimefrom', ( $SearchPostTimeFrom || '' ), 11 ) . ' ' . &TagLabel( '〜', 'searchposttimefrom', 'S' ) . " \n";
    $contents .= &TagInputText( 'text', 'searchposttimeto', ( $SearchPostTimeTo || '' ), 11 ) . &TagLabel( 'の間', 'searchposttimeto', 'E' ) . $HTML_BR;

    if ( $SYS_ICON )
    {
	$contents .= $HTML_BR . &TagLabel( $H_ICON, 'icon', 'I' ) . ": \n";

	# アイコンの選択
	local( $selContents, $IconTitle );
	$selContents = sprintf( qq(<option%s>$H_NOICON</option>\n), ( $Icon &&
	    ( $Icon ne $H_NOICON ))? '' : ' selected="selected"' );
	foreach $IconTitle ( sort keys( %ICON_FILE ))
	{
	    $selContents .= sprintf( "<option%s>$IconTitle</option>\n",
	    	( $Icon eq $IconTitle )? ' selected="selected"' : '' );
	}
	$contents .= &TagSelect( 'icon', $selContents ) . "\n";

	$contents .= "という$H_ICON\n";

	$selContents = sprintf( qq[<option%s value="0">(アイコン検索をしない)</option>\n], ( $SearchIcon == 0 )? ' selected="selected"' : '' );

	$selContents .= qq(<option value="0">----------------</option>\n);
	$selContents .= sprintf( qq[<option%s value="1">を持つ$H_MESGを探す</option>\n], ( $SearchIcon == 1 )? ' selected="selected"' : '' );
	$selContents .= sprintf( qq[<option%s value="1001">を持たない$H_MESGを探す</option>\n], ( $SearchIcon == 1001 )? ' selected="selected"' : '' );

	$selContents .= qq(<option value="0">----------------</option>\n);
	$selContents .= sprintf( qq[<option%s value="11">が直接の$H_REPLYにある$H_MESGを探す</option>\n], ( $SearchIcon == 11 )? ' selected="selected"' : '' );
	$selContents .= sprintf( qq[<option%s value="1011">が直接の$H_REPLYに *ない* $H_MESGを探す</option>\n], ( $SearchIcon == 1011 )? ' selected="selected"' : '' );

	$selContents .= qq(<option value="0">--------</option>\n);
	$selContents .= sprintf( qq[<option%s value="12">が$H_REPLYの中にある$H_MESGを探す</option>\n], ( $SearchIcon == 12 )? ' selected="selected"' : '' );
	$selContents .= sprintf( qq[<option%s value="1012">が$H_REPLYの中に *ない* $H_MESGを探す</option>\n], ( $SearchIcon == 1012 )? ' selected="selected"' : '' );

	$selContents .= qq(<option value="0">--------</option>\n);
	$selContents .= sprintf( qq[<option%s value="13">が$H_REPLYの末端にある$H_MESGを探す</option>\n], ( $SearchIcon == 13 )? ' selected="selected"' : '' );
	$selContents .= sprintf( qq[<option%s value="1013">が$H_REPLYの末端に *ない* $H_MESGを探す</option>\n], ( $SearchIcon == 1013 )? ' selected="selected"' : '' );

	$selContents .= qq(<option value="0">----------------</option>\n);
	$selContents .= sprintf( qq[<option%s value="21">が直接の$H_ORIGである$H_MESGを探す</option>\n], ( $SearchIcon == 21 )? ' selected="selected"' : '' );
	$selContents .= sprintf( qq[<option%s value="1021">が直接の$H_ORIGで *ない* $H_MESGを探す</option>\n], ( $SearchIcon == 1021 )? ' selected="selected"' : '' );

	$selContents .= qq(<option value="0">--------</option>\n);
	$selContents .= sprintf( qq[<option%s value="22">が$H_ORIGの中にある$H_MESGを探す</option>\n], ( $SearchIcon == 22 )? ' selected="selected"' : '' );
	$selContents .= sprintf( qq[<option%s value="1022">が$H_ORIGの中に *ない* $H_MESGを探す</option>\n], ( $SearchIcon == 1022 )? ' selected="selected"' : '' );

	$selContents .= qq(<option value="0">--------</option>\n);
	$selContents .= sprintf( qq[<option%s value="23">が$H_ORIG_TOPにある$H_MESGを探す</option>\n], ( $SearchIcon == 23 )? ' selected="selected"' : '' );
	$selContents .= sprintf( qq[<option%s value="1023">が$H_ORIG_TOPに *ない* $H_MESGを探す</option>\n], ( $SearchIcon == 1023 )? ' selected="selected"' : '' );

	$contents .= &TagSelect( 'searchicon', $selContents );

	# アイコン一覧
	$contents .= ' (' . &LinkP( "b=$BOARD_ESC&c=i", "使える$H_ICON一覧" .
	    &TagAccessKey( 'H' ), 'H' ) . ')';

#	$contents .= &TagInputCheck( 'searchicon', $SearchIcon ) . ': ' . &TagLabel( $H_ICON, 'searchicon', 'I' ) . " // \n";

    }
    $msg .= &TagFieldset( "検索条件$HTML_BR", $contents ) . $HTML_BR;

    $msg .= &TagLabel( 'キーワード', 'key', 'K' ) . ': ' . &TagInputText(
	'text', 'key', $Key, $KEYWORD_LENGTH ) . $HTML_BR;

    %tags = ( 'c', 's', 'b', $BOARD );
    &DumpForm( *tags, '検索', 'リセット', *msg );
}

sub hg_b_all_icon
{
    return unless $BOARD;
    $gHgStr .= "<ul>\n";
    foreach ( @ICON_TITLE )
    {
	$gHgStr .= '<li>' . &TagMsgImg( $_ ) . " : [$_] " . ( $ICON_HELP{$_} ||
	    $_ ) . "</li>\n";
    }
    $gHgStr .= "</ul>\n";
}


###
## DumpBoardHeader - 掲示板ヘッダの表示
#
# - SYNOPSIS
#	DumpBoardHeader();
#
# - DESCRIPTION
#	掲示板のヘッダを表示する．
#
sub DumpBoardHeader
{
    local( $msg );
    &GetHeaderDb( $BOARD, *msg );
    
    LINE: while ( 1 )
    {
	if (( index( $msg, '<kb' ) >= 0 ) &&
	    ( $msg =~ s!<kb:(\w+)(\s*var="([^"]*)")?\s+/>!!o ))
	{
	    $gHgStr .= $`;
	    eval( '&hg_' . $1 . '( "' . $source . '", "' . $3 . '" );' );
	    &Fatal( 998, "$file : $@" ) if $@;
	    $msg = $';
	}
	else
	{
	    $gHgStr .= $msg;
	    last LINE;
	}
    }
}


###
## DumpArtEntry - メッセージ入力フォームの表示
#
# - SYNOPSIS
#	DumpArtEntry( $icon, $type, $id, $postDateStr, $title, $texttype, $article, $name, $eMail, $url, $fMail );
#
# - ARGS
#	$icon		アイコン
#	$type		メッセージタイプ( 'supersede', and so )
#	$id		リプライ/修正元メッセージID
#	$postDateStr	デフォルト投稿日（yyyy/mm/dd(HH:MM:SS)）
#	$title		デフォルトタイトル（プレビューからの戻りなどで使う）
#	$texttype	デフォルト書き込み形式
#	$article	デフォルトメッセージ本文
#	$name		デフォルトユーザ名
#	$eMail		デフォルトメイルアドレス
#	$url		デフォルトURL
#	$fMail		デフォルトメイル配信チェック
#
sub DumpArtEntry
{
    local( $icon ) = @_;

#    if ( $ICON_TYPE{ $icon } eq 'cfv' )
#    {
#	# TBD
#    }
#    elsif ( $ICON_TYPE{ $icon } eq 'vote' )
#    {
#	# TBD
#    }
#    else
#    {
	&DumpArtEntryNormal( @_ );
#    }
}


# 通常メッセージ
sub DumpArtEntryNormal
{
    local( $icon, $type, $id, $postDateStr, $title, $texttype, $article, $name, $eMail, $url, $fMail ) = @_;

    $texttype = $texttype || $H_TTLABEL[ $SYS_TT_DEFAULT ];
    $icon = $icon || $SYS_ICON_DEFAULT;

    local( $msg );
    local( $contents ) = '';

    # アイコンの選択
    if ( $SYS_ICON )
    {
	$msg .= &TagLabel( $H_ICON, 'icon', 'I' ) . " :\n";
	$contents = sprintf( "<option%s>$H_NOICON</option>\n",
	    (( $icon eq $H_NOICON )? ' selected="selected"' : '' ));
	foreach ( @ICON_TITLE )
	{
	    $contents .= sprintf( "<option%s>$_</option>\n", ( $_ eq $icon )? ' selected="selected"' : '' );
	}
	$msg .= &TagSelect( 'icon', $contents ) . "\n";

	$msg .= '(' . &LinkP( "b=$BOARD_ESC&c=i", "使える$H_ICON一覧" .
	    &TagAccessKey( 'H' ), 'H' ) . ')' . $HTML_BR;
    }

    $msg .= &TagLabel( $H_SUBJECT, 'subject', 'T' ) . ': ' .
	&TagInputText( 'text', 'subject', $title, $SUBJECT_LENGTH ) . $HTML_BR;
    
    local( $ttFlag ) = 0;
    local( $ttBit ) = 0;
    
    foreach ( @H_TTLABEL )
    {
	if (( $SYS_TEXTTYPE & ( 2 ** $ttBit )) && ( $SYS_TEXTTYPE ^ ( 2 ** $ttBit )))
	{
	    $ttFlag = 1;	# 後で使う．きたない．．．
	}
	$ttBit++;
    }

    # 書き込み形式
    if ( $ttFlag )
    {
	$ttBit = 0;
	local( $firstFlag ) = 1;
	local( $labelTarget );
	$contents = '';
	foreach ( @H_TTLABEL )
	{
	    if ( $SYS_TEXTTYPE & ( 2 ** $ttBit ))
	    {
		if ( $firstFlag )
		{
		    $firstFlag = 0;
		}
		else
		{
		    $contents .= '&nbsp;&nbsp;';
		}
		if ( $texttype eq $H_TTLABEL[$ttBit] )
		{
		    $contents .= &TagInputRadio( 'texttype_' . $ttBit, 'texttype', $H_TTLABEL[$ttBit], 1 );
		    $labelTarget = 'texttype_' . $ttBit;
		}
		else
		{
		    $contents .= &TagInputRadio( 'texttype_' . $ttBit, 'texttype', $H_TTLABEL[$ttBit], 0 );
		}
		$contents .= &TagLabel( $H_TTLABEL[$ttBit], 'texttype_' . $ttBit, '' );
	    }
	    $ttBit++;
	}
	$msg .= &TagFieldset( &TagLabel( $H_TEXTTYPE, $labelTarget, 'Z' ) . ': ', $contents );
    }
    else
    {
	$msg .= sprintf( qq(<input name="texttype" type="hidden" value="%s" />), $H_TTLABEL[(( log $SYS_TEXTTYPE ) / ( log 2 ))] ) . $HTML_BR;
    }

    $msg .= &TagLabel( $H_MESG, 'article', 'A' ) . ':' . $HTML_BR .
	&TagTextarea( 'article', $article, $TEXT_ROWS, $TEXT_COLS ) . $HTML_BR;

    if ( $POLICY & 8 )
    {
	# 管理権限は特別扱い
	$msg .= &TagLabel( $H_DATE, 'postdate', 'T' ) . ': ' .
	    &TagInputText( 'text', 'postdate', $postDateStr, 20 ) .
	    qq[('yyyy/mm/dd(HH:MM:SS)'の形式で指定)] . $HTML_BR;
	$msg .= &TagLabel( $H_FROM, 'name', 'N' ) . ': ' .
	    &TagInputText( 'text', 'name', $name, $NAME_LENGTH ) . $HTML_BR;
	$msg .= &TagLabel( $H_MAIL, 'mail', 'M' ) . ': ' .
	    &TagInputText( 'text', 'mail', $eMail, $MAIL_LENGTH ) . $HTML_BR;
	$msg .= &TagLabel( $H_URL, 'url', 'U' ) . ': ' .
	    &TagInputText( 'text', 'url', ( $url || 'http://' ), $URL_LENGTH ) . $HTML_BR;
    }
    elsif ( $POLICY & 4 )
    {
	# 登録済みの場合，名前，メイル，URLの入力は，無し．
	$msg .= $H_FROM . ": $UNAME" . $HTML_BR;
	$msg .= $H_MAIL . ": $UMAIL" . $HTML_BR if ( $SYS_SHOWMAIL && $UMAIL );
	$msg .= $H_URL . ": $UURL" . $HTML_BR if $UURL;
    }
    else
    {
	$msg .= &TagLabel( $H_FROM, 'name', 'N' ) . ': ' .
	    &TagInputText( 'text', 'name', $name, $NAME_LENGTH ) . $HTML_BR;
	$msg .= &TagLabel( $H_MAIL, 'mail', 'M' ) . ': ' .
	    &TagInputText( 'text', 'mail', $eMail, $MAIL_LENGTH ) . $HTML_BR;
	$msg .= &TagLabel( $H_URL, 'url', 'U' ) . ': ' .
	    &TagInputText( 'text', 'url', ( $url || 'http://' ), $URL_LENGTH ) . $HTML_BR;
    }

    if ( $SYS_MAIL & 2 )
    {
	$msg .= &TagLabel( "リプライがあった時に$H_MAILで連絡", 'fmail', 'F'
	    ) . ': ' . &TagInputCheck( 'fmail', $fMail ) . "\n";
    }
    $msg .= "</p>\n<p>\n";

    $contents = &TagInputRadio( 'com_p', 'com', 'p', 1 ) . ":\n" . &TagLabel(
	'試しに表示してみる(まだ投稿しません)', 'com_p', 'P' ) . $HTML_BR;
    local( $doLabel );
    if ( $type eq 'supersede' )
    {
	$doLabel = '訂正する';
    }
    else
    {
	$doLabel = "$H_MESGを投稿する";
    }
    $contents .= &TagInputRadio( 'com_x', 'com', 'x', 0 ) . ":\n" . &TagLabel(
	$doLabel, 'com_x', 'X' ) . $HTML_BR;
    $msg .= &TagFieldset( "コマンド$HTML_BR", $contents );

    local( $op ) = ( -M &GetPath( $SYS_DIR, $BOARD_FILE ));
    local( %tags ) = ( 'corig', $cgi'TAGS{'c'}, 'b', $BOARD, 'c', 'p',
	'id', $id, 's', ( $type eq 'supersede' ), 'op', $op );

    &DumpForm( *tags, '実行', '', *msg );
}


###
## DumpArtBody - メッセージ本体の表示
#
# - SYNOPSIS
#	DumpArtBody( $Id, $CommandFlag, $OriginalFlag, @articleInfo );
#
# - ARGS
#	$Id			メッセージID
#	$CommandFlag		コマンドを表示するか否か(表示する=1)
#	$OriginalFlag		その記事中に，(あれば)元記事へのリンクを
#				表示するか否か(表示する=1)
#	@articleInfo		$Idが''だった時に使われるメッセージ情報
#
# - DESCRIPTION
#	メッセージを表示する．$Idが''でなければ，メッセージDBから取得した
#	情報を元に表示する．$Idが''の場合，かわりに@articleInfoを用いる．
#
sub DumpArtBody
{
    local( $id, $commandFlag, $origFlag, @articleInfo ) = @_;

    local( $fid, $aids, $date, $title, $icon, $host, $name, $eMail, $url );

    local( $body ) = '';
    if ( $id ne '' )
    {
	( $fid, $aids, $date, $title, $icon, $host, $name, $eMail, $url ) = &getMsgInfo( $id );
	local( @articleBody );
	&GetArticleBody( $id, $BOARD, *articleBody );
	$body = join( '', @articleBody );
    }
    else
    {
	( $fid, $aids, $date, $title, $icon, $host, $name, $eMail, $url, $body ) = @articleInfo;
    }

    # 未投稿記事は読めない
    &Fatal( 8, '' ) if ( $title eq '' );

    $gHgStr .= qq(<div class="kbArticle">\n);

    # タイトル
    &DumpArtTitle( $id, $title, $icon );

    local( $origId );
    if ( $fid ne '' )
    {
	( $origId = $fid ) =~ s/,.*$//o;
    }

    if ( $commandFlag && $SYS_COMMAND )
    {
	local( $num );
	foreach ( 0 .. &getNofMsg() )
	{
	    $num = $_, last if ( &getMsgId( $_ ) eq $id );
	}
	local( $prevId ) = &getMsgId( $num - 1 ) if ( $num > 0 );
	local( $nextId ) = &getMsgId( $num + 1 );
	&DumpArtCommand( $id, $origId, $prevId, $nextId, ( $aids ne '' ),
	    (( &IsUser( $name ) && (( $aids eq '' ) || ( $SYS_OVERWRITE == 2 ))) || ( $POLICY & 8 )));
    }

    # ヘッダ（ユーザ情報とリプライ元: タイトルは除く）
    &DumpArtHeader( $name, $eMail, $url, $host, $date, ( $origFlag? $origId : '' ));

    # 切れ目
    $gHgStr .= $H_LINE;

#    if ( $ICON_TYPE{ $icon } eq 'cfv' )
#    {
#	# TBD
#    }
#    elsif ( $ICON_TYPE{ $icon } eq 'vote' )
#    {
#	# TBD
#    }
#    else
#    {
	&DumpArtBodyNormal( *body );
#    }

    $gHgStr .= "</div>\n";

    &cgiprint'Cache( $gHgStr ); $gHgStr = '';
}


# 通常メッセージ
sub DumpArtBodyNormal
{
    local( *body ) = @_;
    $gHgStr .= qq(<div class="body">) . &ArticleEncode( *body ) . "</div>\n";
}


###
## DumpArtThread - フォロー記事を全て表示．
#
# - SYNOPSIS
#	DumpArtThread( $State, $Head, @Tail );
#
# - ARGS
#	$State		表示制御フラグ
#	    2^0 ... スレッドの先頭であるか（▲が付く）
#	    2^1 ... 同一ページfragmentリンクを利用するか（#記事番号でリンク）
#	    2^2 ... タイトルを表示する(4), 記事本文を表示する(0)
#	$Head		木構造のヘッドノード
#	@Tail		木構造の娘ノード群
#
# - DESCRIPTION
#	ある記事と，その記事へのリプライ記事をまとめて表示する．
#	元の木構造は，
#		( a ( b ( c d ) ) ( e ) ( f ( g ) ) )
#	のようなリストである．
#	詳細は&GetFollowIdTreeのインプリメント部分を参照のこと．
#
sub DumpArtThread
{
    local( $State, $Head, @Tail ) = @_;

    # 記事概要か，記事そのものか．
    if ( $State&4 )
    {
	if ( $Head eq '(' )
	{
	    $gHgStr .= "<ul>\n";
	}
	elsif ( $Head eq ')' )
        {
	    $gHgStr .= "</ul>\n";
	}
	else
	{
	    local( $dFid, $dAids, $dDate, $dSubject, $dIcon, $dRemoteHost, $dName ) = &getMsgInfo( $Head );
	    &DumpArtSummaryItem( $Head, $dAids, $dDate, $dSubject, $dIcon, $dName, $State&3 );
	    $gHgStr .= "</li>\n";
	    $State ^= 1 if ( $State&1 );
	}
    }
    elsif (( $Head ne '(' ) && ( $Head ne ')' ))
    {
	# 元記事の表示(コマンド付き, 元記事なし)
	$gHgStr .= $HTML_HR;
	&DumpArtBody( $Head, $SYS_COMMAND_EACH, 0 );
    }

    # &cgiprint'Cache( $gHgStr ); $gHgStr = '';
    # tail recuresive.
    &DumpArtThread( $State, @Tail ) if @Tail;
}


###
## DumpSearchResult - 記事検索
#
# - SYNOPSIS
#	DumpSearchResult( $Key, $Subject, $Person, $Article, $PostTime, $PostTimeFrom, $PostTimeTo, $IconType, $Icon );
#
# - ARGS
#	$Key		キーワード
#	$Subject	タイトルを検索するか否か
#	$Person		投稿者を検索するか否か
#	$Article	本文を検索するか否か
#	$PostTime	日付を検索するか否か
#	$PostTimeFrom	開始日付
#	$PostTimeTo	終了日付
#	$IconType	アイコンの検索手法
#	$Icon		アイコン
#
# - DESCRIPTION
#	記事を検索して表示する
#
sub DumpSearchResult
{
    local( $Key, $Subject, $Person, $Article, $PostTime, $PostTimeFrom, $PostTimeTo, $IconType, $Icon ) = @_;

    local( @KeyList ) = split( /\s+/, $Key );

    # リスト開く
    $gHgStr .= "<ul>\n";

    local( $dId, $dFid, $dAids, $dDate, $dTitle, $dIcon, $dRemoteHost, $dName, $dEmail );
    local( $SubjectFlag, $PersonFlag, $PostTimeFlag, $ArticleFlag );
    local( $HitNum, $Line, $FromUtc, $ToUtc );
    foreach ( $[ .. &getNofMsg() )
    {
	# 記事情報
	$dId = &getMsgId( $_ );
	( $dFid, $dAids, $dDate, $dTitle, $dIcon, $dRemoteHost, $dName, $dEmail ) = &getMsgInfo( $dId );

	# 変数のリセット
	$SubjectFlag = $PersonFlag = $PostTimeFlag = $ArticleFlag = 0;
	$Line = '';

	# アイコンチェック
	next unless &SearchArticleIcon( $dId, $Icon, $IconType );

	# 投稿時刻を検索
	if ( $PostTime )
	{
	    $FromUtc = $ToUtc = -1;
	    $FromUtc = &GetUtcFromYYYY_MM_DD( $PostTimeFrom )
		if $PostTimeFrom;
	    $ToUtc = &GetUtcFromYYYY_MM_DD( $PostTimeTo )
		if $PostTimeTo;
	    $ToUtc += 86400 if ( $ToUtc >= 0 );
	    next if !&CheckSearchTime( $dDate, $FromUtc, $ToUtc );
	}

	if ( $Key ne '' )
	{
	    # タイトルを検索
	    if ( $Subject && ( $dTitle ne '' ))
	    {
		$SubjectFlag = 1;
		foreach ( @KeyList )
		{
		    $SubjectFlag = 0 if ( $dTitle !~ /$_/i );
		}
	    }

	    # 投稿者名を検索
	    if ( $Person && !$SubjectFlag && ( $dName ne '' ))
	    {
		$PersonFlag = 1;
		foreach ( @KeyList )
		{
		    if (( $dName !~ /$_/i ) && ( $dEmail !~ /$_/i ))
		    {
			$PersonFlag = 0;
		    }
		}
	    }

	    # 本文を検索
	    if ( $Article && !$SubjectFlag && !$PersonFlag )
	    {
		if ( $Line = &SearchArticleKeyword( $dId, $BOARD, @KeyList ))
		{
		    $ArticleFlag = 1;
		}
	    }
	}
	else
	{
	    # 無条件で一致
	    $SubjectFlag = 1;
	}

	if ( $SubjectFlag || $PersonFlag || $ArticleFlag )
	{
	    # 最低1つは合致した
	    $HitNum++;

	    # 記事へのリンクを表示
	    &DumpArtSummaryItem( $dId, $dAids, $dDate, $dTitle, $dIcon, $dName, 1 );

	    # 本文に合致した場合は本文も表示
	    if ( $ArticleFlag )
	    {
		$Line =~ s/<[^>]*>//go;
		$gHgStr .= "<blockquote>$Line</blockquote>\n";
	    }
	    $gHgStr .= "</li>\n";
	}
    }

    # ヒットしたら
    if ( $HitNum )
    {
	$gHgStr .= "</ul>\n<ul>\n";
	$gHgStr .= "<li>$HitNum件の$H_MESGが見つかりました．</li>\n";
    }
    else
    {
	$gHgStr .= "<li>該当する$H_MESGは見つかりませんでした．</li>\n";
    }

    # リスト閉じる
    $gHgStr .= "</ul>\n";
}


###
## DumpOriginalArticles - オリジナル記事へのリンクの表示
#
# - SYNOPSIS
#	DumpOriginalArticles( $fids );
#
# - ARGS
#	$fids	オリジナル記事IDデータ
#
# - DESCRIPTION
#	オリジナル記事へのリンクを表示する．
#
sub DumpOriginalArticles
{
    if ( $_[0] ne '' )
    {
	# オリジナル記事があるなら…

	$gHgStr .= "<ul>\n";

	local( $dId, $dFid, $dAids, $dDate, $dTitle, $dIcon, $dHost, $dName );
	foreach $dId ( reverse( split( /,/, $_[0] )))
	{
	    ( $dFid, $dAids, $dDate, $dTitle, $dIcon, $dHost, $dName ) = &getMsgInfo( $dId );
	    &DumpArtSummaryItem( $dId, $dAids, $dDate, $dTitle, $dIcon, $dName, 0 );
	}
	$gHgStr .= "</ul>\n";
    }
    else
    {
	# なにも表示しない．
    }
}


###
## DumpReplyArticles - リプライ記事へのリンクの表示
#
# - SYNOPSIS
#	DumpReplyArticles( $aids );
#
# - ARGS
#	$aids	リプライ記事IDデータ
#
# - DESCRIPTION
#	リプライ記事へのリンクを表示する．
#
sub DumpReplyArticles
{
    if ( $_[0] ne '' )
    {
	# 反応記事があるなら…

	local( $id, @tree );
	foreach $id ( split( /,/, $_[0] ))
	{
	    # フォロー記事の木構造の取得
	    # ex. '( a ( b ( c d ) ) ( e ) ( f ( g ) ) )'というリスト
	    @tree = ();
	    &GetFollowIdTree( $id, *tree );
	    
	    # メイン関数の呼び出し(記事概要)
	    &DumpArtThread( 4, @tree );
	}
    }
    else
    {
	# 反応記事無し

	$gHgStr .= "<ul>\n<li>現在，この$H_MESGへの$H_REPLYはありません</li>\n</ul>\n";
    }
}


###
## DumpArtTitle - 記事タイトルの表示
#
# - SYNOPSIS
#	DumpArtTitle( $id, $title, $icon );
#
# - ARGS
#	$id	記事ID
#	$title	タイトル
#	$icon	アイコン
#
sub DumpArtTitle
{
    local( $id, $title, $icon ) = @_;
    local( $markUp );
    $markUp .= "$id. " if ( $id ne '' );
    $markUp .= &TagMsgImg( $icon ) . $title;
    $gHgStr .= '<h2>' . &TagA( $markUp, '', '', '', "a$id" ) . "</h2>\n";
}


###
## DumpArtCommand - 記事コマンドの表示
#
# - SYNOPSIS
#	DumpArtCommand( $id, $upId, $prevId, $nextId, $reply, $delete );
#
# - ARGS
#	$id	記事ID
#	$upId	上記事ID
#	$prevId	前記事ID
#	$nextId	次記事ID
#	$reply	リプライ記事があるか
#	$delete	削除・訂正が可能か
#
sub DumpArtCommand
{
    local( $id, $upId, $prevId, $nextId, $reply, $delete ) = @_;

    $gHgStr .= qq(<p class="command">\n);

    local( $dlmtS, $dlmtL );
    if ( $SYS_COMICON == 1 )
    {
	$dlmtS = '';
	$dlmtL = ' // ';
    }
    elsif ( $SYS_COMICON == 2 )
    {
	$dlmtS = ' | ';
	$dlmtL = '';
    }
    else
    {
	$dlmtS = ' | ';
	$dlmtL = '';
    }

    if ( $upId ne '' )
    {
	$gHgStr .= &LinkP( "b=$BOARD_ESC&c=e&id=$upId", &TagComImg( $ICON_UP, $H_UPARTICLE ), 'U' ) . "\n";
    }
    else
    {
	$gHgStr .= &TagComImg( $ICON_UP_X, $H_UPARTICLE, ) . "\n";
    }
	
    if ( $prevId ne '' )
    {
	$gHgStr .= $dlmtS . &LinkP( "b=$BOARD_ESC&c=e&id=$prevId", &TagComImg(
	    $ICON_PREV, $H_PREVARTICLE ), 'P' ) . "\n";
    }
    else
    {
	$gHgStr .= $dlmtS . &TagComImg( $ICON_PREV_X, $H_PREVARTICLE, ) . "\n";
    }
	
    if ( $nextId ne '' )
    {
	$gHgStr .= $dlmtS . &LinkP( "b=$BOARD_ESC&c=e&id=$nextId", &TagComImg(
	    $ICON_NEXT, $H_NEXTARTICLE ), 'N' ) . "\n";
    }
    else
    {
	$gHgStr .= $dlmtS . &TagComImg( $ICON_NEXT_X, $H_NEXTARTICLE, ) . "\n";
    }

    if ( $reply )
    {
	$gHgStr .= $dlmtS . &LinkP( "b=$BOARD_ESC&c=t&id=$id", &TagComImg(
	    $ICON_DOWN, $H_READREPLYALL ), 'M' ) . "\n";
    }
    else
    {
	$gHgStr .= $dlmtS . &TagComImg( $ICON_DOWN_X, $H_READREPLYALL ) . "\n";
    }

    $gHgStr .= $dlmtL;

    if ( $POLICY & 2 )
    {
	$gHgStr .= $dlmtS . &LinkP( "b=$BOARD_ESC&c=f&id=$id",
	    &TagComImg( $ICON_FOLLOW, $H_REPLYTHISARTICLE ), 'R' ) . "\n" .
	    $dlmtS . &LinkP( "b=$BOARD_ESC&c=q&id=$id",
	    &TagComImg( $ICON_QUOTE, $H_REPLYTHISARTICLEQUOTE ), 'Q' ) . "\n";
    }
    else
    {
	$gHgStr .= $dlmtS . &TagComImg( $ICON_FOLLOW_X, $H_REPLYTHISARTICLE ) .
	    "\n" . $dlmtS . &TagComImg( $ICON_QUOTE_X, $H_REPLYTHISARTICLEQUOTE ) . "\n";
    }

    if ( $SYS_AUTH )
    {
	$gHgStr .= $dlmtL;

	if ( $delete )
	{
	    $gHgStr .= $dlmtS . &LinkP( "b=$BOARD_ESC&c=f&s=on&id=$id",
		&TagComImg( $ICON_SUPERSEDE, $H_SUPERSEDE ), 'S' ) . "\n" .
		$dlmtS . &LinkP( "b=$BOARD&c=dp&id=$id",
		&TagComImg( $ICON_DELETE, $H_DELETE ), 'D' ) . "\n";
	}
	else
	{
	    $gHgStr .= $dlmtS . &TagComImg( $ICON_SUPERSEDE_X, $H_SUPERSEDE ) .
	    	"\n" . $dlmtS . &TagComImg( $ICON_DELETE_X, $H_DELETE ) . "\n";
	}
    }

    if ( $SYS_COMICON == 1 )
    {
	$gHgStr .= $dlmtL;
	$gHgStr .= $dlmtS . &LinkP( "b=$BOARD_ESC&c=h", &TagComImg( $ICON_HELP,
	    'ヘルプ' ), 'H', '', '', 'list' ) . "\n";
    }
    $gHgStr .= qq(</p>\n);
}


###
## DumpArtHeader - 記事ヘッダ（タイトル除く）の表示
#
# - SYNOPSIS
#	DumpArtHeader( $name, $eMail, $url, $host, $date, $origId );
#
# - ARGS
#	$name		ユーザ名
#	$eMail		メイルアドレス
#	$url		URL
#	$host		Remote Host名
#	$date		日付（UTC）
#	$origId		リプライ元記事ID
#
sub DumpArtHeader
{
    local( $name, $eMail, $url, $host, $date, $origId ) = @_;

    $gHgStr .= qq(<p class="header">\n);

    # お名前
    if ( $url eq '' )
    {
	$gHgStr .= "<strong>$H_FROM</strong>: $name";
    }
    else
    {
	$gHgStr .= "<strong>$H_FROM</strong>: " . &TagA( $name, $url );
    }

    # メイル
    if ( $SYS_SHOWMAIL && $eMail )
    {
	$gHgStr .= ' ' . &TagA( "&lt;$eMail&gt;", "mailto:$eMail" );
    }
    $gHgStr .= $HTML_BR;

    # マシン
    $gHgStr .= "<strong>$H_HOST</strong>: $host" . $HTML_BR if $SYS_SHOWHOST;

    # 投稿日
    $gHgStr .= "<strong>$H_DATE</strong>: " . &GetDateTimeFormatFromUtc( $date ) . $HTML_BR;

    # リプライ元へのリンク
    if ( $origId )
    {
	( $dFid, $dAids, $dDate, $dTitle, $dIcon, $dHost, $dName ) = &getMsgInfo( $origId );
	$gHgStr .= "<strong>$H_ORIG:</strong> ";
	&DumpArtSummary( $origId, $dAids, $dDate, $dTitle, $dIcon, $dName, 0 );
	$gHgStr .= $HTML_BR;
    }

    # 切れ目
    $gHgStr .= "</p>\n";
}


###
## DumpButtonToTitleList - タイトル一覧ボタンの表示
#
# - SYNOPSIS
#	DumpButtonToTitleList($Board);
#
# - ARGS
#	$Board		掲示板ID
#
# - DESCRIPTION
#	タイトル一覧へジャンプするためのボタンを表示する
#
sub DumpButtonToTitleList
{
    local( $board, $id ) = @_;
    local( $old ) = $id? &GetTitleOldIndex( $id ) : 0;

    if  ( $SYS_COMMAND_BUTTON )
    {
	local( %tags ) = ( 'b', $board, 'c', 'v', 'num', $DEF_TITLE_NUM, 'old',
	    $old );
	&DumpForm( *tags, "$H_BACKTITLEREPLY(B)", '', '' );

	%tags = ( 'b', $board, 'c', 'r', 'num', $DEF_TITLE_NUM, 'old', $old );
	&DumpForm( *tags, $H_BACKTITLEDATE, '', '' );
    }
    else
    {
	local( $boardEsc ) = &URIEscape( $board );
	$gHgStr .= "<p>" . &LinkP( "b=$boardEsc&c=v&num=$DEF_TITLE_NUM&old=$old", $H_BACKTITLEREPLY . &TagAccessKey( 'B' ), 'B' ) . "</p>\n";
	$gHgStr .= "<p>" . &LinkP( "b=$boardEsc&c=r&num=$DEF_TITLE_NUM&old=$old", $H_BACKTITLEDATE ) .
	    "</p>\n";
    }
}


###
## DumpButtonToArticle - メッセージへジャンプするボタンの表示
#
# - SYNOPSIS
#	DumpButtonToArticle( $board, $id, $msg );
#
# - ARGS
#	$board	掲示板ID
#	$id	メッセージID
#	$msg	リンク文字列
#
# - DESCRIPTION
#	メッセージへジャンプするためのボタンを表示する
#
sub DumpButtonToArticle
{
    local( $board, $id, $msg ) = @_;

    if  ( $SYS_COMMAND_BUTTON )
    {
	local( %tags ) = ( 'b', $board, 'c', 'e', 'id', $id );
	&DumpForm( *tags, "$msg(N)", '', '' );
    }
    else
    {
	local( $boardEsc ) = &URIEscape( $board );
	$gHgStr .= "<p>" . &LinkP( "b=$boardEsc&c=e&id=$id", $msg .
	    &TagAccessKey( 'N' ), 'N' ) . "</p>\n";
    }
}


###
## DumpForm - フォームタグのフォーマット
#
# - SYNOPSIS
#	DumpForm( *hiddenTags, $submit, $reset, *contents );
#
# - ARGS
#	*tags		追加するhiddenタグを収めた連想配列
#	*submit		submitボタン文字列
#	*reset		resetボタン文字列
#	*contents	</form>の前までに挿入する文字列
#	$noAuth		認証用情報を入れないためのフラグ	
#
# - DESCRIPTION
#	Formタグのフォーマット
#
sub DumpForm
{
    local( *tags, $submit, $reset, *contents, $noAuth ) = @_;

    $gHgStr .= qq(<form action="$PROGRAM" method="POST">\n);

    $gHgStr .= "<p>\n";
    foreach ( keys( %tags ))
    {
	$gHgStr .= qq(<input name="$_" type="hidden" value="$tags{$_}" />\n);
    }
    if ( !$noAuth && ( $SYS_AUTH == 3 ))
    {
	$gHgStr .= qq(<input name="kinoU" type="hidden" value="$UNAME" />\n);
	$gHgStr .= qq(<input name="kinoP" type="hidden" value="$PASSWD" />\n);
	$gHgStr .= qq(<input name="kinoA" type="hidden" value="3" />\n);
    }
    local( $accessKey );
    if ( $submit =~ /\((\w)\)$/o )
    {
	$accessKey = $1;
    }
    else
    {
	$submit .= "(G)";
	$accessKey = 'G';
    }
    $gHgStr .= "$contents\n" . &TagInputSubmit( 'submit', $submit, $accessKey );
    if ( $reset )
    {
	if ( $reset =~ /\((\w)\)$/o )
	{
	    $accessKey = $1;
	}
	else
	{
	    $reset .= "(R)";
	    $accessKey = 'R';
	}
	$accessKey = 'R';
	$gHgStr .= ' ' . &TagInputSubmit( 'reset', $reset, $accessKey ) . "\n";
    }
    $gHgStr .= "</p>\n</form>\n";
}


###
## DumpArtSummary - タイトルリストのフォーマット
#
# - SYNOPSIS
#	DumpArtSummary( $id, $aids, $date, $subject, $icon, $name, $flag);
#
# - ARGS
#	$id		記事ID
#	$aids		リプライ記事があるか否か
#	$date		記事の投稿日付(UTC)
#			  省略時（0など）は表示されない．
#	$subject	記事のSubject
#	$icon		記事アイコンID
#	$name		記事の投稿者名
#	$flag		表示カスタマイズフラグ
#	    2^0 ... スレッドの先頭であるか（▲が付く）
#	    2^1 ... 同一ページfragmentリンクを利用するか（#記事番号でリンク）
#
# - DESCRIPTION
#	ある記事をタイトルリスト表示用にフォーマットする．
#
sub DumpArtSummary
{
    local( $id, $aids, $date, $subject, $icon, $name, $flag ) = @_;

    $subject = $subject || $id;
    $name = $name || $MAINT_NAME;

    $gHgStr .= qq(<span class="kbTitle">);	# 初期化

    if ( $flag&1 && ( &getMsgParents( $id ) ne '' ))
    {
	local( $fId );
	( $fId = &getMsgParents( $id )) =~ s/^.*,//o;
	$gHgStr .= ' ' . &LinkP( "b=$BOARD_ESC&c=t&id=$fId", $H_THREAD_ALL, '',
	    $H_THREAD_ALL_L ) . ' ';
    }

    $gHgStr .= &TagMsgImg( $icon ) . " <small>$id.</small> " .
	(( $flag&2 )? &TagA( $subject, "$cgi'REQUEST_URI#a$id" ) :
	&LinkP( "b=$BOARD_ESC&c=e&id=$id", $subject ));

    if ( $aids )
    {
	$gHgStr .= ' ' . &LinkP( "b=$BOARD_ESC&c=t&id=$id", $H_THREAD, '',
	    $H_THREAD_L );
    }

    $gHgStr .= " [$name] ";
    $gHgStr .= &GetDateTimeFormatFromUtc( $date ) if $date;

    $gHgStr .= ' ' . &TagMsgImg( $H_NEWARTICLE ) if &getMsgNewP( $id );
    $gHgStr .= "</span>\n";
}


###
## DumpArtSummaryItem - タイトルリストのフォーマット（<li>つき）
#
# - SYNOPSIS
#	DumpArtSummaryItem(同上);
#
# - ARGS
#	同上
#
# - DESCRIPTION
#	ある記事をタイトルリスト表示用にフォーマットする．<li>つき
#
sub DumpArtSummaryItem
{
    $gHgStr .= '<li>';
    &DumpArtSummary;
}


###
## htmlGen - HTML generator from source file
#
# - SYNOPSIS
#	htmlGen( $source );
#
# - ARGS
#	$source		const val.	filename of HTML source in UI dir.
#
# - DESCRIPTION
#	generate HTML output from source file named $source.
#	for each `<kb:foobar>' LINE in the source file,
#	the function `foobar' was called.
#
# - RETURN
#	1 if succeed, 0 if failed.
#
sub htmlGen
{
    local( $source ) = @_;

    local( $file ) = &GetPath( $UI_DIR, $source );

    open( SRC, "<$file" ) || &Fatal( 1, $file );

    if ( $SYS_COOKIE_EXPIRE == 1 )
    {
	$cookieExpire = 'Thursday, 31-Dec-2029 23:59:59 GMT';
    }
    elsif ( $SYS_COOKIE_EXPIRE == 2 )
    {
	# 86400 = 24 * 60 * 60
	$cookieExpire = $^T + ( $SYS_COOKIE_VALUE * 86400 );
    }
    elsif ( $SYS_COOKIE_EXPIRE == 3 )
    {
	$cookieExpire = $SYS_COOKIE_VALUE;
    }
    else
    {
	$cookieExpire = '';
    }
    &cgiauth'Header( 0, 0, 1, $cookieExpire );
    &cgiprint'Init();

    $gHgStr = '';

    # Work around for MSIE 4.5(Macintosh IE).
    #   cf. <URL:http://kanzaki.com/docs//html/xhtml1.html>
    if ( $ENV{'HTTP_USER_AGENT'} =~ /MSIE 4.5/o )
    {
	$gHgStr .= "<!-- dummy comment -->\n";
    }

    while( <SRC> )
    {
	LINE: while ( 1 )
	{
	    if (( index( $_, '<kb' ) >= 0 ) &&
		( s!<kb:(\w+)(\s*var="([^"]*)")?\s+/>!!o ))
	    {
		$gHgStr .= $`;
		eval( '&hg_' . $1 . '( "' . $source . '", "' . $3 . '" );' );
		if ( $@ )
		{
		    if ( $source != $file )
		    {
			&Fatal( 998, "$file : $@" );
		    }
		    else
		    {
			print "Error -- $file : $@\n";
		    }
		}
		$_ = $';
	    }
	    else
	    {
		$gHgStr .= $_;
		last LINE;
	    }
	}
    }
    &cgiprint'Cache( $gHgStr );

    &cgiprint'Flush();
}


######################################################################
# ロジックインプリメンテーション


###
## ArriveMail - 記事が到着したことをメイル
#
# - SYNOPSIS
#	ArriveMail( $Name, $Email, $Subject, $Icon, $Id, @To );
#
# - ARGS
#	$Name		新規記事投稿者名
#	$Email		新規記事投稿者メイルアドレス
#	$Date		新規記事投稿時刻
#	$Subject	新規記事Subject
#	$Icon		新規記事アイコン
#	$Id		新規記事ID
#	@To		送信先E-Mail addrリスト
#
# - DESCRIPTION
#	記事が到着したことをメイルする．
#
# - RETURN
#	なし
#
sub ArriveMail
{
    local( $Name, $Email, $Date, $Subject, $Icon, $Id, @To ) = @_;

    local( $StrSubject, $MailSubject, $StrFrom, $Message );
    $StrSubject = ( !$SYS_ICON || ( $Icon eq $H_NOICON ))? $Subject :
	"($Icon) $Subject";
    $StrSubject =~ s/<[^>]*>//go;	# タグは要らない
    $StrSubject = &HTMLDecode( $StrSubject );
    $MailSubject = &GetMailSubjectPrefix( $BOARDNAME, $Id ) . $StrSubject;
    $StrFrom = $Email? "$Name <$Email>" : "$Name";

    $Message = <<__EOF__;
$SYSTEM_NAMEからのお知らせです．
$H_BOARD「$BOARDNAME」に対して書き込みがありました．

新着$H_MESG:
  → $SCRIPT_URL?b=$BOARD&c=e&id=$Id

__EOF__

    $Message .= &GetArticlePlainText( $Id, $Name, $Email, $Subject, $Icon,
	$Date );

    # メイル送信
    &SendArticleMail( $Name, $Email, $MailSubject, $Message, $Id, @To );
}


###
## FollowMail - 反応があったことをメイル
#
# - SYNOPSIS
#	FollowMail( $Name, $Email, $Date, $Subject, $Icon, $Id, $Fname, $Femail, $Fsubject, $Ficon, $Fid, @To );
#
# - ARGS
#	$Name		新規記事投稿者名
#	$Email		新規記事投稿者メイルアドレス
#	$Date		リプライされた記事の書き込み時間
#	$Subject	新規記事Subject
#	$Icon		新規記事アイコン
#	$Id		新規記事ID
#	$Fname		リプライされた記事の投稿者名
#	$Femail		リプライされた記事の投稿者メイルアドレス
#	$Fsubject	リプライされた記事のSubject
#	$Ficon		リプライされた記事のアイコン
#	$Fid		リプライされた記事ID
#	@To		送信先E-Mail addrリスト
#
# - DESCRIPTION
#	リプライがあったことをメイルする．
#
# - RETURN
#	なし
#
sub FollowMail
{
    local( $Name, $Email, $Date, $Subject, $Icon, $Id, $Fname, $Femail, $Fdate, $Fsubject, $Ficon, $Fid, @To ) = @_;
    
    local( $StrSubject, $FstrSubject, $MailSubject, $StrFrom, $Message );

    $StrSubject = ( !$SYS_ICON || ( $Icon eq $H_NOICON ))? "$Subject" :
	"($Icon) $Subject";
    $StrSubject =~ s/<[^>]*>//go;	# タグは要らない
    $StrSubject = &HTMLDecode( $StrSubject );
    $FstrSubject = ( $Ficon eq $H_NOICON )? $Fsubject : "($Ficon) $Fsubject";
    $FstrSubject =~ s/<[^>]*>//go;	# タグは要らない
    $FstrSubject = &HTMLDecode( $FstrSubject );
    $MailSubject = &GetMailSubjectPrefix( $BOARDNAME, $Fid ) . $FstrSubject;
    $StrFrom = $Email? "$Name <$Email>" : "$Name";

    local( $topId );
    ( $topId = &getMsgParents( $Id )) =~ m/([^,]+)$/o;

    $Message = <<__EOF__;
$SYSTEM_NAMEからのお知らせです．

$H_BOARD「$BOARDNAME」に
「$StrFrom」さんが書いた
「$StrSubject」に
$H_REPLYがありました．

新着$H_MESG:
  → $SCRIPT_URL?b=$BOARD&c=e&id=$Fid
$H_ORIG_TOPからまとめ読み:
  → $SCRIPT_URL?b=$BOARD&c=t&id=$topId

__EOF__

    $Message .= &GetArticlePlainText( $Fid, $Fname, $Femail, $Fsubject, $Ficon,
	$Fdate );

    # メイル送信
    &SendArticleMail( $Fname, $Femail, $MailSubject, $Message, $Fid, @To );
}


###
## GetArticlePlainText - メッセージをplain textで取得
#
# - SYNOPSIS
#	GetArticlePlainText(
#	    $id,	メッセージID
#	    $name,	投稿者名
#	    $mail,	投稿者メイルアドレス
#	    $subject,	タイトル
#	    $icon,	アイコン
#	    $date	日付(UTC)
#	)
#
# - DESCRIPTION
#	メイル送信用に，メッセージをplain textで取得する．
#
# - RETURN
#	文字列
#
sub GetArticlePlainText
{
    local( $id, $name, $mail, $subject, $icon, $date ) = @_;

    local( $strSubject ) = ( !$SYS_ICON || ( $icon eq $H_NOICON ))? $subject :
	"($icon) $subject";
    $strSubject =~ s/<[^>]*>//go;	# タグは要らない
    $strSubject = &HTMLDecode( $strSubject );
    local( $strFrom ) = $mail? "$name <$mail>" : $name;
    local( $strDate ) = &GetDateTimeFormatFromUtc( $date );

    local( @body );
    &GetArticleBody( $id, $BOARD, *body );

    $msg = <<__EOF__;
$H_SUBJECT: $strSubject
$H_FROM: $strFrom
$H_DATE: $strDate

--------------------

__EOF__

    local( $str );
    foreach ( @body )
    {
	s/<[^>]*>//go;
	$str .= &HTMLDecode( $_ );
    }

    # 先頭と末尾の改行を切り飛ばす．
    $str =~ s/^\n*//o;
    $str =~ s/\n*$//o;

    $msg . $str;
}


###
## MakeNewArticle, MakeNewArticleEx - 新たに投稿された記事の生成
#
# - SYNOPSIS
#	MakeNewArticleEx( $Board, $Id, $artKey, $postDate, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail, $MailRelay );
#	MakeNewArticle( $Board, $Id, $artKey, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail, $MailRelay );
#
# - ARGS
#	$Board		作成する記事が入る掲示板のID
#	$Id		リプライ元記事のID
#	$artKey		多重書き込み防止用キー
#	$postDate	投稿時刻（UTCからの経過秒数）
#	$TextType	文書タイプ
#	$Name		投稿者名
#	$Email		投稿者E-Mail addr.
#	$Url		投稿者URL
#	$Icon		アイコンID
#	$Subject	Subject文字列
#	$Article	本文文字列
#	$Fmail		リプライがあった時にメイルで知らせるか否か('on'/'')
#
# - DESCRIPTION
#	投稿された記事を記事DBに整理する．
#	&MakeNewArticleには$postDate引数がない．
#	今後（R7以後）は極力&MakeNewArticleExの方を使うように．
#
sub MakeNewArticle
{
    local( $Board, $Id, $artKey, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail, $MailRelay ) = @_;
    &MakeNewArticleEx( $Board, $Id, $artKey, $^T, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail, $MailRelay );
}

sub MakeNewArticleEx
{
    local( $Board, $Id, $artKey, $postDate, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail, $MailRelay ) = @_;

    local( $ArticleId );
    &CheckArticle( $Board, *postDate, *Name, *Email, *Url, *Subject, *Icon, *Article );

    # 新しい記事番号を取得(まだ記事番号は増えてない)
    $ArticleId = &GetNewArticleId( $Board );

    # 正規のファイルの作成
    &MakeArticleFile( $TextType, $Article, $ArticleId, $Board );

    # 新しい記事番号を書き込む
    &WriteArticleId( $ArticleId, $Board, $artKey );

    # DBファイルに投稿された記事を追加
    # 通常の記事引用ならID
    &AddDBFile( $ArticleId, $Board, $Id, $postDate, $Subject, $Icon, ( $SYS_LOGHOST? $REMOTE_INFO : '' ), $Name, $Email, $Url, $Fmail, $MailRelay );

    $ArticleId;
}


###
## SearchArticleIcon - 記事の検索(アイコン)
#
# - SYNOPSIS
#	SearchArticleIcon( $id, $icon, $type );
#
# - ARGS
#	$id		アイコンを検索する記事のID
#	$icon		検索するアイコン
#	$type		検索タイプ
#			  1 ... 本人
#			  11 ... 直接の娘にある
#			  12 ... 娘，孫，…の任意にある
#			  13 ... リーフの娘にある
#			  21 ... 直接の親にある
#			  22 ... 親，その親，…の任意にある
#			  23 ... 新規の親にある
#			  1011 ... 直接の娘にない
#			  1012 ... 娘，孫，…の任意にない
#			  1013 ... リーフの娘にない
#			  1021 ... 直接の親にない
#			  1022 ... 親，その親，…の任意にない
#			  1023 ... 新規の親にない
#
# - DESCRIPTION
#	指定された記事のアイコンを検索する．
#
# - RETURN
#	1 if match, 0 if not.
#
sub SearchArticleIcon
{
    local( $id, $icon, $type ) = @_;

    local( $not ) = 0;
    if ( $type > 1000 )
    {
	$type -= 1000;
	$not = 1;
    }

    # 0は後方互換性のため．'on'が渡されるかもしれない．
    local( $result );
    if (( $type == 1 ) || ( $type == 0 ))
    {
	$result = 1 if ( &getMsgIcon( $id ) eq $icon );
    }
    elsif (( $type == 11 ) || ( $type == 12 ) || ( $type == 13 ))
    {
	local( @daughters ) = split( /,/, &getMsgDaughters( $id ));
	$result = $not unless @daughters;
	local( $dId );
	while ( $dId = shift( @daughters ))
	{
	    if ( &getMsgIcon( $dId ) eq $icon )
	    {
		$result = 1 if (( $type == 11 ) || ( $type == 12 ));
		$result = 1 if (( $type == 13 ) && ( &getMsgDaughters( $dId ) eq '' ));
	    }
	    if ( $type != 11 )
	    {
		# Search recursively...
		push( @daughters, split( /,/, &getMsgDaughters( $dId )));
	    }
	}
	return $not - $result;
    }
    elsif (( $type == 21 ) || ( $type == 22 ) || ( $type == 23 ))
    {
	local( @parents ) = split( /,/, &getMsgParents( $id ));
	$result = $not unless @daughters;
	local( $dId );
	while ( $dId = shift( @parents ))
	{
	    if ( &getMsgIcon( $dId ) eq $icon )
	    {
		$result = 1 if (( $type == 21 ) || ( $type == 22 ));
		$result = 1 if (( $type == 23 ) && ( $#parents == -1 ));
	    }
	    last if ( $type == 21 );
	}
    }
    
    return $not - $result;
}


###
## SearchArticleKeyword - 記事の検索(本文)
#
# - SYNOPSIS
#	SearchArticleKeyword($Id, $Board, @KeyList);
#
# - ARGS
#	$Id		本文を検索する記事のID
#	$Board		掲示板ID
#	@KeyList	キーワードリスト
#
# - DESCRIPTION
#	指定された記事の本文を，キーワードでAND検索する．
#
# - RETURN
#	最初にキーワードとマッチした行．マッチしなかったら空を返す．
#
sub SearchArticleKeyword
{
    local( $Id, $Board, @KeyList ) = @_;

    local( @NewKeyList, $Line, $Return, $Code, $ConvFlag, @ArticleBody );

    $ConvFlag = ( $Id !~ /^\d+$/ );

    &GetArticleBody( $Id, $Board, *ArticleBody );
    foreach ( @ArticleBody )
    {
	$Line = $_;
	if ( $ConvFlag )
	{
	    $Code = &jcode'getcode( *Line );
	    &jcode'convert( *Line, 'euc', $Code, 'z' );
	}

	# 検索
	@NewKeyList = ();
	foreach ( @KeyList )
	{
	    if ( $Line =~ /$_/i )
	    {
		# マッチした! 1行目なら覚えとく
		$Return = $Line unless $Return;
	    }
	    else
	    {
		# まだ探さなきゃ……
		push( @NewKeyList, $_ );
	    }
	}
	# 空なら抜け．
	@KeyList = @NewKeyList;
	last unless @KeyList;
    }

    # まだ残ってたらアウト．空なら最初のマッチした行を返す．
    @KeyList ? '' : $Return;
}


###
## CheckSearchTime - 検索日付のチェック
#
# - SYNOPSIS
#	CheckSearchTime( $target, $from, $to );
#
# - ARGS
#	$target		判断対象
#	$from		範囲開始日付
#	$to		範囲終了日付
#
# - DESCRIPTION
#	記事検索の際，日付の期間判断を行なう．
# 
# - RETURN
#	true if on time.
#
sub CheckSearchTime
{
    local( $target, $from, $to ) = @_;

    return 0 if (( $from >= 0 ) && ( $target < $from ));
    return 0 if (( $to >= 0 ) && ( $target > $to ));
    1;
}


###
## DeleteArticle - 記事の削除
#
# - SYNOPSIS
#	DeleteArticle($Id, $ThreadFlag);
#
# - ARGS
#	$Id		削除記事ID
#	$Board		掲示板ID
#	$ThreadFlag	リプライも消すか否か
#
# - DESCRIPTION
#	削除すべき記事IDを収集した後，DBを更新する．
#
sub DeleteArticle
{
    local( $Id, $Board, $ThreadFlag ) = @_;

    local( $Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $dId, @Target, $TargetId, $parents );

    # 記事情報の取得
    ( $Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url ) = &getMsgInfo( $Id );

    # データの書き換え(必要なら娘も)
    @Target = ( $Id );
    foreach $TargetId ( @Target )
    {
	foreach ( 0 .. &getNofMsg() )
	{
	    # IDを取り出す
	    $dId = &getMsgId( $_ );
	    # フォロー記事リストの中から，削除する記事のIDを取り除く
	    &setMsgDaughters( $dId, join( ',', grep(( !/^$TargetId$/o ),
		split( /,/, &getMsgDaughters( $dId )))));
	    # 元記事から削除記事のIDを取り除く
	    $parents = &getMsgParents( $dId );
	    if ( $parents eq $TargetId )
	    {
		$parents = '';
	    }
	    else
	    {
		$parents =~ s/,$TargetId,.*$//;
		$parents =~ s/^$TargetId,.*$//;
		$parents =~ s/,$TargetId$//;
	    }
	    &setMsgParents( $dId, $parents );
	    # 娘も対象とする
	    push( @Target, split( /,/, &getMsgDaughters( $dId ))) if ( $ThreadFlag && ( $dId eq $TargetId ));
	}
    }

    # DBを更新する．
    &DeleteArticleFromDbFile( $Board, *Target );
}


###
## SupersedeArticle - 記事を訂正する
#
# - SYNOPSIS
#	SupersedeArticle;
#
# - DESCRIPTION
#	記事を訂正する．
#
sub SupersedeArticle
{
    local( $Board, $Id, $postDate, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail ) = @_;

    local( $SupersedeId, $File, $SupersedeFile );

    # 入力された記事情報のチェック．投稿日は
    &CheckArticle( $Board, $postDate, *Name, *Email, *Url, *Subject, *Icon, *Article );

    # DBファイルを訂正
    $SupersedeId = &SupersedeDbFile( $Board, $Id, $postDate, $Subject, $Icon, ( $SYS_LOGHOST? $REMOTE_INFO : '' ), $Name, $Email, $Url, $Fmail );

    # ex. 「100」→「100_5」
    $File = &GetArticleFileName( $Id, $Board );
    $SupersedeFile = &GetArticleFileName( sprintf( "%s_%s", $Id, $SupersedeId ), $Board );
    rename( $File, $SupersedeFile ) || &Fatal( 14, "$File -&gt; $SupersedeFile" );

    # 正規のファイルの作成
    &MakeArticleFile( $TextType, $Article, $Id, $Board );

    $Id;
}


###
## ReLinkExec - 記事のかけかえ実施
#
# - SYNOPSIS
#	ReLinkExec($FromId, $ToId, $Board);
#
# - ARGS
#	$FromId		かけかえ元記事ID
#	$ToId		かけかえ先記事ID
#	$Board		掲示板ID
#
# - DESCRIPTION
#	記事をリプライ-元記事関係をかけかえる．
#
sub ReLinkExec
{
    local( $FromId, $ToId, $Board ) = @_;

    local( $dId, @Daughters, $DaughterId );

    # 循環記事の禁止
    &Fatal( 50, '' ) if ( grep( /^$FromId$/, split( /,/, &getMsgParents( $ToId ))));

    # データ書き換え
    foreach ( 0 .. &getNofMsg() )
    {
	# IDを取り出す
	$dId = &getMsgId( $_ );
	# フォロー記事リストの中から，移動する記事のIDを取り除く
	&setMsgDaughters( $dId, join( ',', grep(( !/^$FromId$/o ), split( /,/, &getMsgDaughters( $dId )))));
    }

    # スレッドの途中を切る場合は，後で娘たちの書き換えも必要になる．
    @Daughters = split( /,/, &getMsgDaughters( $FromId )) if ( &getMsgParents( $FromId ) ne '' );

    # 該当記事のリプライ先を変更する
    if ( $ToId eq '' )
    {
	&setMsgParents( $FromId, '' );
    }
    elsif ( &getMsgParents( $ToId ) eq '' )
    {
	&setMsgParents( $FromId, "$ToId" );
    }
    else
    {
	&setMsgParents( $FromId, "$ToId," . &getMsgParents( $ToId ));
    }

    # 該当記事の娘についても，リプライ先を変更する
    while ( $DaughterId = shift( @Daughters ))
    {
	# 孫娘も……
	push( @Daughters, split( /,/, &getMsgDaughters( $DaughterId )));
	# 書き換え
	if (( &getMsgParents( $DaughterId ) eq $FromId )
	    || ( &getMsgParents( $DaughterId ) =~ /^$FromId,/ ))
	{
	    &setMsgParents( $DaughterId, ( &getMsgParents( $FromId ) ne '' )? "$FromId," . &getMsgParents( $FromId ) : "$FromId" );
	}
	elsif (( &getMsgParents( $DaughterId ) =~ /^(.*),$FromId$/ )
	       || ( &getMsgParents( $DaughterId ) =~ /^(.*),$FromId,/ ))
	{
	    &setMsgParents( $DaughterId, ( &getMsgParents( $FromId ) ne '' )? "$1,$FromId," . &getMsgParents( $FromId ) : "$1,$FromId" );
	}
    }

    # リプライ先になった記事のフォロー記事群に追加する
    &setMsgDaughters( $ToId, ( &getMsgDaughters( $ToId ) ne '' ) ? &getMsgDaughters( $ToId ) . ",$FromId" : "$FromId" );

    # 記事DBを更新する
    &UpdateArticleDb( $Board );
}


###
## ReOrderExec - 記事の移動実施
#
# - SYNOPSIS
#	ReOrderExec($FromId, $ToId, $Board);
#
# - ARGS
#	$FromId		移動元記事ID
#	$ToId		移動先記事ID
#	$Board		掲示板ID
#
# - DESCRIPTION
#	指定された記事を，指定された記事の次に移動する．
#
sub ReOrderExec
{
    local( $FromId, $ToId, $Board ) = @_;

    local( @Move );

    # 移動する記事たちを集める
    @Move = ( $FromId, &CollectDaughters( $FromId ));

    # 移動させる
    &ReOrderArticleDb( $Board, $ToId, *Move );
}


###
## CheckArticle - 入力された記事情報のチェック
#
# - SYNOPSIS
#	CheckArticle( $board, *postDate, *name, *eMail, *url, *subject, *icon, *article );
#
# - ARGS
#	$board		掲示板ID
#	*postDate	投稿日（空でもOK）
#	*name		投稿者名
#	*eMail		メイルアドレス
#	*url		URL
#	*subject	Subject
#	*icon		アイコンID
#	*article	本文
#
# - DESCRIPTION
#	入力された記事をチェックする
#
sub CheckArticle
{
    local( $board, *postDate, *name, *eMail, *url, *subject, *icon, *article ) = @_;

    &CheckPostDate( *postDate );
    &CheckName( *name );
    &CheckEmail( *eMail );
    &CheckURL( *url );
    &CheckSubject( *subject );
    &CheckIcon( *icon ) if $SYS_ICON;

    # 本文の空チェック．
    &Fatal( 2, $H_MESG ) if ( $article eq '' );

    if ( $SYS_MAXARTSIZE != 0 )
    {
	local( $length ) = length( $article );
	&Fatal( 12, $length ) if ( $length > $SYS_MAXARTSIZE );
    }
}


###
## secureSubject - 安全なSubjectを作り出す
## secureArticle - 安全なArticleを作り出す
#
# - SYNOPSIS
#	secureSubject( *subject );
#	secureArticle( *article, $textType );
#
# - ARGS
#	*subject	Subject文字列
#	*article	Article文字列
#	$textType	入力形式
#
# - DESCRIPTION
#	$subjectを安全な文字列に変換する．
#	$articleを安全な文字列に変換する．
#
sub secureSubject
{
    local( *subject ) = @_;

    if ( $SYS_TAGINSUBJECT )
    {
	local( @subjectTags ) = (
	'b',	1,	$HTML_TAGS_GENATTRS,
	'big',	1,	$HTML_TAGS_GENATTRS,
	'cite',	1,	$HTML_TAGS_GENATTRS,
	'code',	1,	$HTML_TAGS_GENATTRS,
	'del',	1,	"$HTML_TAGS_GENATTRS/cite/datetime",
	'em',	1,	$HTML_TAGS_GENATTRS,
	'i',	1,	$HTML_TAGS_GENATTRS,
	'img',	0,	"$HTML_TAGS_GENATTRS/alt/height/longdesc/src/width",
	'ins',	1,	"$HTML_TAGS_GENATTRS/cite/datetime",
	'kbd',	1,	$HTML_TAGS_GENATTRS,
	'samp',	1,	$HTML_TAGS_GENATTRS,
	'small',1,	$HTML_TAGS_GENATTRS,
	'span',	1,	$HTML_TAGS_GENATTRS,
	'strong',1,	$HTML_TAGS_GENATTRS,
	'style',1,	"$HTML_TAGS_I18NATTRS/media/title/type",
	'sub',	1,	$HTML_TAGS_GENATTRS,
	'sup',	1,	$HTML_TAGS_GENATTRS,
	'tt',	1,	$HTML_TAGS_GENATTRS,
	'var',	1,	$HTML_TAGS_GENATTRS,
	);
	
	local( %sNeedVec, %sFeatureVec, $tag );
	while( @subjectTags )
	{
	    $tag = shift( @subjectTags );
	    $sNeedVec{ $tag } = shift( @subjectTags );
	    $sFeatureVec{ $tag } = shift( @subjectTags );
	}

	# secrurity check
	&cgi'SecureXHTML( *subject, *sNeedVec, *sFeatureVec );
    }
    else
    {
	$subject = &HTMLEncode( $subject );	# no tags are allowed.
    }
}

sub secureArticle
{
    local( *article, $textType ) = @_;

    local( @articleTags ) = (
	# タグ名, 閉じ必須か否か, 使用可能なfeature
	'a',	1,	"$HTML_TAGS_GENATTRS/charset/href/hreflang/name/rel/rev/tabindex/target/type",
	'abbr',	1,	$HTML_TAGS_GENATTRS,
	'address',1,	$HTML_TAGS_GENATTRS,
	'b',	1,	$HTML_TAGS_GENATTRS,
	'big',	1,	$HTML_TAGS_GENATTRS,
	'blockquote',1,	"$HTML_TAGS_GENATTRS/cite",
	'br',	0,	$HTML_TAGS_COREATTRS,
	'cite',	1,	$HTML_TAGS_GENATTRS,
	'code',	1,	$HTML_TAGS_GENATTRS,
	'dd',	0,	$HTML_TAGS_GENATTRS,
	'del',	1,	"$HTML_TAGS_GENATTRS/cite/datetime",
	'dfn',	1,	$HTML_TAGS_GENATTRS,
	'div',	1,	$HTML_TAGS_GENATTRS,
	'dl',	1,	$HTML_TAGS_GENATTRS,
	'dt',	0,	$HTML_TAGS_GENATTRS,
	'em',	1,	$HTML_TAGS_GENATTRS,
	'h1',	1,	$HTML_TAGS_GENATTRS,
	'h2',	1,	$HTML_TAGS_GENATTRS,
	'h3',	1,	$HTML_TAGS_GENATTRS,
	'h4',	1,	$HTML_TAGS_GENATTRS,
	'h5',	1,	$HTML_TAGS_GENATTRS,
	'h6',	1,	$HTML_TAGS_GENATTRS,
	'hr',	0,	$HTML_TAGS_COREATTRS,
	'i',	1,	$HTML_TAGS_GENATTRS,
	'img',	0,	"$HTML_TAGS_GENATTRS/alt/height/longdesc/src/width",
	'ins',	1,	"$HTML_TAGS_GENATTRS/cite/datetime",
	'kbd',	1,	$HTML_TAGS_GENATTRS,
	'li',	0,	$HTML_TAGS_GENATTRS,
	'ol',	1,	$HTML_TAGS_GENATTRS,
	'p',	1,	$HTML_TAGS_GENATTRS,
	'pre',	1,	$HTML_TAGS_GENATTRS,
	'q',	1,	"$HTML_TAGS_GENATTRS/cite",
	'samp',	1,	$HTML_TAGS_GENATTRS,
	'small',1,	$HTML_TAGS_GENATTRS,
	'span',	1,	$HTML_TAGS_GENATTRS,
	'strong',1,	$HTML_TAGS_GENATTRS,
	'style',1,	"$HTML_TAGS_I18NATTRS/media/title/type",
	'sub',	1,	$HTML_TAGS_GENATTRS,
	'sup',	1,	$HTML_TAGS_GENATTRS,
	'tt',	1,	$HTML_TAGS_GENATTRS,
	'ul',	1,	$HTML_TAGS_GENATTRS,
	'var',	1,	$HTML_TAGS_GENATTRS,
# 色やサイズはstyleで指定すべきなので，今後絶滅必至のFONTタグなわけですが，
# それでもどーしても使いたいというあなたは，
# ↓の行の先頭の「#」を消してください．^^;
#	'font',	1,	"$HTML_TAGS_GENATTRS/size/color",
    );
	
    local( %aNeedVec, %aFeatureVec, $tag );
    while( @articleTags )
    {
	$tag = shift( @articleTags );
	$aNeedVec{ $tag } = shift( @articleTags );
	$aFeatureVec{ $tag } = shift( @articleTags );
    }
    
    if (( !$SYS_TEXTTYPE ) || ( $textType eq $H_TTLABEL[0] ))
    {
	# pre-formatted
	&PlainArticleToPreFormatted( *article );
    }
    elsif ( $textType eq $H_TTLABEL[1] )
    {
	# convert to html
	&PlainArticleToHtml( *article );
	# secrurity check
	&cgi'SecureXHTML( *article, *aNeedVec, *aFeatureVec );
    }
    elsif ( $textType eq $H_TTLABEL[2] )
    {
	# secrurity check
	&cgi'SecureXHTML( *article, *aNeedVec, *aFeatureVec );
    }
    else
    {
	# Not selected... pre-formatted
	&PlainArticleToPreFormatted( *article );
    }
}


###
## CheckPostDate - 投稿日チェック
#
# - SYNOPSIS
#	CheckPostDate( *str );
#
# - ARGS
#	*str		投稿日（UTCからの経過秒数）
#
# - DESCRIPTION
#	投稿日のチェックを行なう．
#
sub CheckPostDate
{
    local( *str ) = @_;

    # 空でもOK
    return if ( $str eq '' );

    # 不正な値になってないか?（解析に失敗してたら-1になってるはず）
    &Fatal( 21, '' ) if ( $str < 0 );
}


###
## CheckSubject - 文字列チェック: Subject
#
# - SYNOPSIS
#	CheckSubject(*String);
#
# - ARGS
#	*String		Subject文字列
#
# - DESCRIPTION
#	Subjectの文字列チェックを行なう．
#	不正な文字列だったらエラー表示ルーチンへ．
#	(アプリケーション/UIを分離したほうがいいかな?)
#
sub CheckSubject
{
    local( *String ) = @_;

    &Fatal( 2, $H_SUBJECT ) unless $String;
    &Fatal( 3, '' ) if ( $String =~ m/[\t\n]/o );

    if ( !$SYS_TAGINSUBJECT )
    {
	&Fatal( 4, '' ) if ( $String =~ m/[<>]/o );
    }
}


###
## CheckIcon - 文字列チェック: Icon
#
# - SYNOPSIS
#	CheckIcon( *str );
#
# - ARGS
#	*str		Icon文字列
#
# - DESCRIPTION
#	Iconの文字列チェックを行なう．
#	不正な文字列だったらエラー表示ルーチンへ．
#
sub CheckIcon
{
    local( *str ) = @_;

    # アイコンのチェック; おかしけりゃ「無し」に設定．
    $str = $H_NOICON if ( !&GetIconUrlFromTitle( $str ));

    &Fatal( 2, $H_ICON ) if ( !$SYS_ALLOWNOICON && ( $str eq $H_NOICON ));
}


###
## CheckName - 文字列チェック: 投稿者名
#
# - SYNOPSIS
#	CheckName(*String);
#
# - ARGS
#	*String		投稿者名文字列
#
# - DESCRIPTION
#	投稿者名の文字列チェックを行なう．
#	不正な文字列だったらエラー表示ルーチンへ．
#	(アプリケーション/UIを分離したほうがいいかな?)
#
sub CheckName
{
    local( *String ) = @_;

    &Fatal( 2, $H_FROM ) if ( !$String );
    &Fatal( 3, '' ) if ( $String =~ m/[\t\n]/o );

    # 数字だけじゃ駄目．
    &Fatal( 5, $String ) if ( $String =~ /^\d+$/ );
}


###
## CheckPasswd - 文字列チェック: パスワード
#
# - SYNOPSIS
#	CheckPasswd(*String);
#
# - ARGS
#	*String		パスワード文字列
#
# - DESCRIPTION
#	パスワードの文字列チェックを行なう．
#
# - RETURN
#	1 ... エラー（空）
#	2 ... エラー（タブor改行）
#	0 ... OK
#
sub CheckPasswd {
    local( *String ) = @_;

    &Fatal( 2, $H_PASSWD ) if ( !$String );
    &Fatal( 3, $H_PASSWD ) if ( $String =~ /[\t\n]/o );

    return 0;
}


###
## CheckEmail - 文字列チェック: E-Mail addr.
#
# - SYNOPSIS
#	CheckEmail(*String);
#
# - ARGS
#	*String		E-Mail addr.文字列
#
# - DESCRIPTION
#	E-Mail addr.の文字列チェックを行なう．
#	不正な文字列だったらエラー表示ルーチンへ．
#	(アプリケーション/UIを分離したほうがいいかな?)
#
sub CheckEmail
{
    local( *String ) = @_;

    if ( $SYS_POSTERMAIL )
    {
	&Fatal( 2, $H_MAIL ) if ( !$String );
	# `@'が入ってなきゃアウト
	&Fatal( 7, 'E-Mail' ) if ( $String !~ /@/ );
    }
    &Fatal( 3, '' ) if ( $String =~ m/[\t\n]/o );
}


###
## CheckURL - 文字列チェック: URL
#
# - SYNOPSIS
#	CheckURL(*String);
#
# - ARGS
#	*String		URL文字列
#
# - DESCRIPTION
#	URLの文字列チェックを行なう．ただし空チェックだけ．
#	中身のチェックにはIsUrlを呼び出す．
#	不正な文字列だったらエラー表示ルーチンへ．
#	(アプリケーション/UIを分離したほうがいいかな?)
#
sub CheckURL
{
    local( *String ) = @_;

    # http://だけの場合は空にしてしまう．
    $String = '' if ( $String =~ m!^http://$!oi );
    &Fatal( 7, 'URL' ) if (( $String ne '' ) && ( !&IsUrl( $String )));
    &Fatal( 3, '' ) if ( $String =~ m/[\t\n]/o );
}


###
## CheckBoardDir - 文字列チェック: 掲示板ディレクトリ
#
# - SYNOPSIS
#	CheckBoardDir( *name );
#
# - ARGS
#	*name		掲示板ディレクトリ名
#
sub CheckBoardDir
{
    local( *name ) = @_;
    &Fatal( 52, '' ) unless (( $name =~ /\w+/o ) || ( $name =~ /\//o ));
    &Fatal( 2, "$H_BOARD略称" ) if ( $name eq '' );
}

###
## CheckBoardName - 文字列チェック: 掲示板名
#
# - SYNOPSIS
#	CheckBoardDir( *intro );
#
# - ARGS
#	*intro		掲示板名
#
sub CheckBoardName
{
    local( *intro ) = @_;
    &Fatal( 2, "$H_BOARD名称" ) if ( $intro eq '' );
}

###
## CheckBoardHeader - 文字列チェック: 掲示板ヘッダ
#
# - SYNOPSIS
#	CheckBoardHeader( *header );
#
# - ARGS
#	*header		掲示板ヘッダ
#
sub CheckBoardHeader
{
    local( *header ) = @_;
    # 空でもOK
}

###
## IsUrl - URLの構造をチェック
#
# - SYNOPSIS
#	IsUrl($String);
#
# - ARGS
#	$String		URL文字列
#
# - DESCRIPTION
#	URLの文字列チェックを行なう．
#	予め指定された(@URL_SCHEME)Schemeのものであるか否かをチェック．
#	telnet接続等は，しない．
#
# - RETURN
#	正しいURLであれば1，そうでなければ0
#
sub IsUrl
{
    local( $String ) = @_;

    local( $IsUrl ) = 0;
    local( $Scheme );
    foreach $Scheme ( @URL_SCHEME )
    {
	$IsUrl = 1 if ( $String =~ m!^$Scheme:!i );
    }
    $IsUrl;
}


###
## GetFollowIdTree - リプライ記事の木構造を取得
#
# - SYNOPSIS
#	GetFollowIdTree($id, *tree);
#
# - ARGS
#	$id	記事ID
#	*tree	木構造を格納するリスト
#
# - DESCRIPTION
#	指定された記事のリプライ記事を，そのIDの木構造フォーマットで取り出す．
#
#	例: * (←指定された記事)
#	    +--a
#	    |  +--b
#	    |  |  +--c
#	    |  |  +--d
#	    |  |
#	    |  +--e
#	    |     +--f
#	    +--g
#	       +--h
#
#	→ ( a ( b ( c d ) e ( f ) ) g ( h ) )
#
sub GetFollowIdTree
{
    local( $id, *tree ) = @_;

    # 安全のため，再帰停止条件（データが正常ならここは通らない）
    return if ( $id eq '' );

    local( @aidList ) = split( /,/, &getMsgDaughters( $id ));

    push( @tree, '(', $id );
    foreach ( @aidList ) { &GetFollowIdTree( $_, *tree ); }
    push( @tree, ')' );
}


###
## GetTreeTopArticle - 木構造のトップ記事を取得
#
# - SYNOPSIS
#	GetTreeTopArticle( *tree );
#
# - ARGS
#	*tree	木構造が格納済みのリスト
#
# - DESCRIPTION
#	木構造の詳細については&GetFollowIdTree()を参照のこと．
#
# - RETURN
#	記事ID
#
sub GetTreeTopArticle
{
    local( *tree ) = @_;
    $tree[1];
}


###
## GetReplySubject - リプライSubjectの生成
#
# - SYNOPSIS
#	GetReplySubject( *subjectStr );
#
# - ARGS
#	$subjectStr	Subject文字列
#
# - DESCRIPTION
#	先頭に「Re:」を1つだけつける．
#
sub GetReplySubject
{
    local( *subjectStr ) = @_;

    # Re:を取り除き，
    $subjectStr =~ s/^Re:\s*//oi;

    # TAG用エンコードして，
    &TAGEncode( *subjectStr );

    # 先頭に「Re: 」をくっつけて返す．
    $subjectStr = "Re: $subjectStr";
}


###
## GetMailSubjectPrefix - メイル用Subjectのprefixを取得
#
# - SYNOPSIS
#	GetMailSubjectPrefix( $board, $id );
#
# - ARGS
#	$board	掲示板ID
#	$id	記事ID
#
# - DESCRIPTION
#	[foo: 1]を返す．
#
# - RETURN
#	prefix文字列
#
sub GetMailSubjectPrefix
{
    local( $board, $id ) = @_;
    return "[$board: $id] " if $SYS_MAILHEADBRACKET;
    "";
}


###
## GetModifiedTime - ある記事の最終更新時刻(UTC)を取得
#
# - SYNOPSIS
#	GetModifiedTime($Id, $Board);
#
# - ARGS
#	$Id		記事ID
#	$Board		掲示板ID
#
# - DESCRIPTION
#	あるIDの記事から，最終更新UTCを取ってくる．
#
# - RETURN
#	その記事ファイルの最終更新時刻(UTC)
#
sub GetModifiedTime
{
    local( $Id, $Board ) = @_;

    # 86400 = 24 * 60 * 60
    $^T - ( -M &GetArticleFileName( $Id, $Board )) * 86400;
}


###
## GetDateTimeFormatFromUtc - UTCから時間を表す文字列を取得
#
# - SYNOPSIS
#	GetDateTimeFormatFromUtc($Utc);
#
# - ARGS
#	$Utc		時刻(UTC)
#
# - DESCRIPTION
#	UTCを時分秒に分割し，フォーマットして文字列として返す．
#
# - RETURN
#	時刻を表わす文字列
#
sub GetDateTimeFormatFromUtc
{
    local( $utc ) = @_;
    local( $sec, $min, $hour, $mDay, $mon, $year ) = localtime( $utc );
    sprintf( "%d/%d/%d(%02d:%02d)", $year+1900, $mon+1, $mDay, $hour, $min );
}


###
## GetYYYY_MM_DD_HH_MM_SSFromUtc - UTCからYYYY/MM/DD(HH:MM:SS)を取得
#
# - SYNOPSIS
#	GetYYYY_MM_DD_HH_MM_SSFromUtc( $utc );
#
# - ARGS
#	$utc		時刻（UTCからの経過秒数）
#
# - DESCRIPTION
#	UTCを時分秒に分割し，YYYY/MM/DD(HH:MM:SS)の形にフォーマットして
#	文字列として返す．
#
#	GetDateTimeFormatFromUtcと似ているが，これは，
#	GetYYYY_MM_DD_HH_MM_SSFromUtcとGetUtcFromYYYY_MM_DD_HH_MM_SSが
#	対応している必要があるため．GetDateTimeFormatFromUtcは無関係なので，
#	自由に変更して構わない．
#
# - RETURN
#	YYYY/MM/DD(HH:MM:SS)
#
sub GetYYYY_MM_DD_HH_MM_SSFromUtc
{
    local( $utc ) = @_;
    local( $sec, $min, $hour, $mDay, $mon, $year ) = localtime( $utc );
    sprintf( "%d/%d/%d(%02d:%02d:%02d)", $year+1900, $mon+1, $mDay, $hour, $min, $sec );
}


###
## GetUtcFromYYYY_MM_DD_HH_MM_SS - YYYY/MM/DD(HH:MM:SS)からUTCを取得
#
# - SYNOPSIS
#	&GetUtcFromYYYY_MM_DD_HH_MM_SS
#	(
#	    $str	時刻を表す文字列
#	);
#
# - DESCRIPTION
#	YYYY/MM/DD(HH:MM:SS)の文字列を分解してUTCを計算．
#
# - RETURN
#	UTCからの経過秒数
#
sub GetUtcFromYYYY_MM_DD_HH_MM_SS
{
    local( $str ) = shift;

    $str =~ m!^(\d+)/(\d+)/(\d+)\((\d\d):(\d\d):(\d\d)\)$!o;
    local( $year, $month, $mday, $hour, $min, $sec ) = ( $1, $2, $3, $4, $5, $6 );
    if (( $year < 1970 )
	|| ( $year > 2037 )
	|| ( $month < 1 )
	|| ( $month > 12 )
	|| ( $mday < 1 )
	|| ( $mday > 31 )
	|| ( $hour < 0 )
	|| ( $hour > 23 )
	|| ( $min < 0 )
	|| ( $min > 59 )
	|| ( $sec < 0 )
	|| ( $sec > 60 ))
    {
	# can't exec timegm/timelocal...
	return -1;
    }

    require( 'timelocal.pl' );
    $year -= 1900;
    $month--;
    &timelocal( $sec, $min, $hour, $mday, $month, $year );
}


###
## GetUtcFromYYYY_MM_DD - YYYY/MM/DDからUTCを取得
#
# - SYNOPSIS
#	GetUtcFromYYYY_MM_DD
#	(
#	    $str	時刻を表す文字列
#	);
#
# - DESCRIPTION
#	YYYY/MM/DDの文字列を分解してUTCを計算．
#
# - RETURN
#	UTCからの経過秒数
#
sub GetUtcFromYYYY_MM_DD
{
    local( $str ) = shift;
    return -1 if ( length( $str ) != 10 );

    local( $year, $month, $mday ) = unpack( "a4 x a2 x a2", $str );
    if (( $year < 1970 )
	|| ( $year > 2037 )
	|| ( $month < 1 )
	|| ( $month > 12 )
	|| ( $mday < 1 )
	|| ( $mday > 31 ))
    {
	# can't exec timegm/timelocal...
	return -1;
    }

    require( 'timelocal.pl' );
    $year -= 1900;
    $month--;
    &timelocal( 0, 0, 0, $mday, $month, $year );
}


###
## HTMLEncode/HTMLDecode - 特殊文字のHTML用EncodeとDecode
#
# - SYNOPSIS
#	HTMLEncode($Str);
#	HTMLDecode($Str);
#
# - ARGS
#	$Str	HTML用Encode/Decodeする文字列
#
# - DESCRIPTION
#	HTMLの特殊文字(", >, <, &)をHTML用にEncode/Decodeする．
#
# - RETURN
#	Encode/Decodeした文字列
#
sub HTMLEncode
{
    local( $_ ) = @_;
    s/\&/&amp;/go;
    s/\"/&quot;/go;
    s/\>/&gt;/go;
    s/\</&lt;/go;
    $_;
}

sub HTMLDecode
{
    local( $_ ) = @_;
    s/&quot;/\"/gio;
    s/&gt;/\>/gio;
    s/&lt;/\</gio;
    s/&amp;/\&/gio;
    $_;
}


###
## URIEscape - URIのescape
#
# - SYNOPSIS
#	URIEscape( $str );
#
# - ARGS
#	$str	URI escapeする文字列
#
# - DESCRIPTION
#	URI escapeを行なう．
#
# - RETURN
#	URI escapeした文字列
#
sub URIEscape
{
    local( $_ ) = @_;
    s/([^A-Za-z0-9\\\-_\.!~*'() ])/sprintf( "%%%02X", ord( $1 ))/eg;
    s/ /+/go;
    $_;
}


###
## TAGEncode - 特殊文字のTAG埋め込み用Encode
#
# - SYNOPSIS
#	TAGEncode( *str );
#
# - ARGS
#	*str	TAG埋め込み用Encodeする文字列
#
# - DESCRIPTION
#	TAG埋め込み（<input value="ここの文字列" />）用に，"と&を取り除く．
#	Encodeと言いながら，今のところDecodeすることはできず，
#	ただ削除するのみ
#
# - RETURN
#	Encodeした文字列
#
sub TAGEncode
{
    local( *str ) = @_;
#    $str =~ s/[\&\"]//go;
    $str =~ s/<[^>]*>//go;
}


###
## ArticleEncode - 記事のEncode
#
# - SYNOPSIS
#	ArticleEncode( *article );
#
# - ARGS
#	$article	Encodeする記事本文
#
# - DESCRIPTION
#	記事中のURL([URL:kb:〜])を，リンクに変換する．
#
# - RETURN
#	Encodeされた文字列
#
sub ArticleEncode
{
    local( *article ) = @_;

    local( $retArticle ) = $article;

    local( $url, $urlMatch, @cache );
    local( $tagStr, $quoteStr );
    while ( $article =~ m/\[url:([^\]]+)\]/gi )
    {
	$tagStr = '';
	$url = $1;
	( $urlMatch = $url ) =~ s/([?+*^\\\[\]\|()])/\\$1/go;
	next if ( grep( /^$urlMatch$/, @cache ));
	push( @cache, $url );
	$quoteStr = "[URL:$url]";

	if ( $urlMatch =~ m/^kb:(.*)$/ )
	{
	    local( $artStr ) = $1;
	    if ( $artStr =~ m!^//.*$! )
	    {
		# not implemented now...
	    }
	    elsif ( $artStr =~ m!^([^/]+)/(.*)$! )
	    {
		local( $boardEsc ) = &GetBoardInfo( $1 );
		$tagStr = &LinkP( "b=$boardEsc&c=e&id=$2", $quoteStr );
	    }
	    else
	    {
		$tagStr = &LinkP( "b=$BOARD_ESC&c=e&id=$artStr", $quoteStr );
	    }
	}
	elsif ( &IsUrl( &HTMLDecode( $urlMatch )))
	{
	    $tagStr = &TagA( $quoteStr, &HTMLDecode( $url ), '', '', '',
		$SYS_LINK_TARGET );
	}
	else
	{
	    next;
	}

	$retArticle =~ s/\[url:$urlMatch\]/$tagStr/gi;
    }

    $retArticle;
}


###
## PlainArticleToPreFormatted - Plain記事をpre formatted textに変換
#
# - SYNOPSIS
#	PlainArticleToPreFormatted(*Article);
#
# - ARGS
#	*Article	変換する記事本文
#
# - DESCRIPTION
#	記事先頭と末尾の無意味な改行を取り除く．
#	タグはHTML encodeする．
#	全体を<pre>と</pre>で囲む．
#	*Articleを破壊する．
#
sub PlainArticleToPreFormatted
{
    local( *Article ) = @_;
    $Article =~ s/\n*$//o;
    $Article = &HTMLEncode( $Article );	# no tags are allowed.
    $Article = "<pre>\n" . $Article . "</pre>";
}


###
## PlainArticleToHtml - Plain記事をHTMLに変換
#
# - SYNOPSIS
#	PlainArticleToHtml(*Article);
#
# - ARGS
#	*Article	変換する記事本文
#
# - DESCRIPTION
#	記事末尾の無意味な改行を取り除く．
#	各段落を<p>で囲む．
#	*Articleを破壊する．
#
sub PlainArticleToHtml
{
    local( *Article ) = @_;
    $Article =~ s/^\n*//o;
    $Article =~ s/\n*$//o;
    $Article =~ s/\n/$HTML_BR/go;
    $Article =~ s/$HTML_BR($HTML_BR)+/<\/p>\n\n<p>/go;
    $Article = "<p>$Article</p>";
}


###
## QuoteOriginalArticle - 引用する(引用符あり)
#
# - SYNOPSIS
#	QuoteOriginalArticle($Id);
#
# - ARGS
#	$Id		記事ID
#
# - DESCRIPTION
#	記事を引用して表示する
#
sub QuoteOriginalArticle
{
    local( $Id, *msg ) = @_;

    # 元記事情報の取得
    local( $fid, $aids, $date, $subject, $icon, $remoteHost, $name, $eMail, $url ) = &getMsgInfo( $Id );

    # 元記事のさらに元記事情報
    local( $pName ) = '';
    if ( $fid )
    {
	local( $pId );
	( $pId = $fid ) =~ s/,.*$//o;
	( $pName ) = &getMsgAuthor( $pId );
    }

    # 引用
    local( @ArticleBody );
    &GetArticleBody( $Id, $BOARD, *ArticleBody );

    if ( $SYS_QUOTEMSG )
    {
	local( $premsg ) = $SYS_QUOTEMSG;
	$premsg =~ s/__LINK__/[url:kb:$Id]/i;
	$premsg =~ s/__TITLE__/$subject/;
	$premsg =~ s/__DATE__/&GetDateTimeFormatFromUtc( $date )/e;
	$premsg =~ s/__NAME__/$name/;
	$msg .= $premsg;
    }
    local( $QMark, $line );
    foreach $line ( @ArticleBody )
    {
	&TAGEncode( *line );

	$QMark = $DEFAULT_QMARK;
	$QMark = $name . ' ' . $QMark if $SYS_QUOTENAME;

	# 元文のうち，引用部分には，新たに引用文字列を重ねない
	# 空行にも要らない
	if (( $line =~ /^$/o ) || ( $line =~ /^$pName\s*$DEFAULT_QMARK/ ))
	{
	    $QMark = '';
	}

	# 引用文字列の表示
	$msg .= "$QMark$line";
    }
}


###
## QuoteOriginalArticleWithoutQMark - 引用する(引用符なし)
#
# - SYNOPSIS
#	QuoteOriginalArticleWithoutQMark($Id);
#
# - ARGS
#	$Id		記事ID
#
# - DESCRIPTION
#	記事を引用して表示する
#
sub QuoteOriginalArticleWithoutQMark
{
    local( $Id, *msg ) = @_;

    local( @ArticleBody, $line );
    &GetArticleBody( $Id, $BOARD, *ArticleBody );
    foreach $line ( @ArticleBody )
    {
	if ( $SYS_TAGINSUPERSEDE )
	{
	    $line = &HTMLEncode( $line );
	}
	else
	{
	    &TAGEncode( *line );
	}
	$msg .= $line;
    }
}


###
## PageLink - ページヘッダ/フッタの表示
#
# - SYNOPSIS
#	ShowPageLinkTop( $com, $num, $old, $rev, $vRev );
#	ShowPageLinkBottom( $com, $num, $old, $rev, $vRev );
#
# - ARGS
#	$com	リンクするコマンド文字列
#	$num	'num'指定
#	$old	'old'指定
#	$rev	'rev'指定
#	$fold	'fold'指定
#		'': 展開リンクなし
#		0, 1: 展開状態
#
# - DESCRIPTION
#	ページヘッダ/フッタのリンク群文字列を取得する．
#
sub PageLink
{
    local( $com, $num, $old, $rev, $fold ) = @_;

    local( $nextOld ) = ( $old > $num )? ( $old - $num ) : 0;
    local( $backOld ) = ( $old + $num );

    local( $str );
    $str = '<p class="kbPageLink">';

    if ( $old )
    {
	$str .= &LinkP( "b=$BOARD_ESC&c=$com&num=$num&old=0&fold=$fold&rev=$rev", $H_TOP . &TagAccessKey( 'T' ), 'T' );
	$str .= ' | ' . &LinkP( "b=$BOARD_ESC&c=$com&num=$num&old=$nextOld&fold=$fold&rev=$rev", $H_UP . &TagAccessKey( 'N' ), 'N' );
    }
    else
    {
	$str .= $H_TOP . &TagAccessKey( 'T' ) . ' | ' . $H_UP . &TagAccessKey( 'N' );
    }

    if ( $SYS_REVERSE )
    {
	$str .= ' | ' .
	    &LinkP( "b=$BOARD_ESC&c=$com&num=$num&old=$old&fold=$fold&rev=" . ( 1-$rev ), $H_REVERSE[ 1-$rev ] . &TagAccessKey( 'R' ), 'R', $H_REVERSE_L );
    }

    if ( $SYS_EXPAND && ( $fold ne '' ))
    {
	$str .= ' | ' . &LinkP( "b=$BOARD_ESC&c=$com&num=$num&old=$old&rev=$rev&fold=" . ( 1-$fold ), $H_EXPAND[ 1-$fold ] . &TagAccessKey( 'E' ), 'E', $H_EXPAND_L );
    }

    $str .= ' | ';

    local( $nofMsg ) = &getNofMsg();
    if ( $num && ( $nofMsg - $backOld >= 0 ))
    {
	$str .= &LinkP( "b=$BOARD_ESC&c=$com&num=$num&old=$backOld&fold=$fold&rev=$rev", $H_DOWN . &TagAccessKey( 'P' ), 'P' );
	$str .= ' | ' . &LinkP( "b=$BOARD_ESC&c=$com&num=$num&old=" . ( $nofMsg - $num + 1) . "&fold=$fold&rev=$rev", $H_BOTTOM . &TagAccessKey( 'B' ), 'B' );
    }
    else
    {
	$str .= $H_DOWN . &TagAccessKey( 'P' ) . ' | ' . $H_BOTTOM . &TagAccessKey( 'B' );
    }

    $str .= "</p>\n";

    $str;
}


###
## TagComImg - コマンドアイコン用イメージタグのフォーマット
#
# - SYNOPSIS
#	TagComImg( $src, $alt, $textP );
#
# - ARGS
#	$src		ソースイメージのURL
#	$alt		altタグ用の文字列
#
# - DESCRIPTION
#	イメージを表示用タグにフォーマットする．
#
#	$SYS_COMICON:
#		1 ... アイコンの後ろに文字列を追加しない
#		2 ... アイコンの後ろに文字列を追加しない
#		0/others ... アイコンなしでテキストだけ
#
sub TagComImg
{
    local( $src, $alt ) = @_;
    if ( $SYS_COMICON == 1 )
    {
	qq(<img src="$src" alt="$alt" width="$COMICON_WIDTH" height="$COMICON_HEIGHT" class="kbComIcon" />);
    }
    elsif ( $SYS_COMICON == 2 )
    {
	qq(<img src="$src" alt="$alt" width="$COMICON_WIDTH" height="$COMICON_HEIGHT" class="kbComIcon" />$alt);
    }
    else
    {
	$alt;
    }
}


###
## TagMsgImg - 記事アイコン用イメージタグのフォーマット
#
# - SYNOPSIS
#	TagMsgImg( $icon );
#
# - ARGS
#	$icon		アイコンタイプ
#
# - DESCRIPTION
#	イメージを表示用タグにフォーマットする．
#
sub TagMsgImg
{
    local( $icon ) = @_;

    if ( !$icon || $icon eq $H_NOICON )
    {
	return "";
    }
    elsif ( $SYS_ICON )
    {
	local( $src ) = &GetIconUrlFromTitle( $icon );
	qq(<img src="$src" alt="[$icon]" width="$MSGICON_WIDTH" height="$MSGICON_HEIGHT" class="kbMsgIcon" />);
    }
    else
    {
	return "[$icon]";
    }
}


###
## TagA - リンクタグのフォーマット
#
# - SYNOPSIS
#	TagA();
#
# - ARGS
#	$markUp		マークアップ文字列
#	$href		リンク先URL（省略可）
#	$key		アクセスキー（省略可）
#	$title		タイトル文字列（省略可）
#	$name		アンカ名（省略可）
#	$target		ターゲットフレーム（省略可）
#
# - DESCRIPTION
#	リンクをリンクタグにフォーマットする．
#
sub TagA
{
    local( $markUp, $href, $key, $title, $name, $target ) = @_;

    if ( $key eq '' )
    {
	$key = $gLinkNum;
	$gLinkNum = 0 if ( ++$gLinkNum > 9 );
    }
    local( $str ) = qq(<a accesskey="$key");
    $str .= qq( href="$href") if ( $href ne '' );
    $str .= qq( title="$title") if ( $title ne '' );
    $str .= qq( name="$name") if ( $name ne '' );
    $str .= qq( target="$target") if ( $target ne '' );
    $str .= ">$markUp</a>";
    $str;
}


###
## TagAccessKey - アクセスキーラベルのフォーマット
#
# - SYNOPSIS
#	TagAccessKey( $key );
#
# - ARGS
#	$key		キー1文字
#
sub TagAccessKey
{
    qq{(<span class="kbAccessKey">$_[0]</span>)};
}


###
## TagLabel - ラベルタグのフォーマット
#
# - SYNOPSIS
#	TagLabel( $markUp, $label, $accessKey );
#
# - ARGS
#	$markUp		マークアップ文字列
#	$label		ラベル対象コントロール
#	$accessKey	アクセスキー
#
sub TagLabel
{
    local( $markUp, $label, $accessKey ) = @_;
    if ( $accessKey )
    {
	qq[<label for="$label" accesskey="$accessKey">$markUp] . &TagAccessKey( $accessKey ) . "</label>";
    }
    else
    {
	qq[<label for="$label">$markUp</label>];
    }
}


###
## TagInputSubmit - submit/resetボタンタグのフォーマット
#
# - SYNOPSIS
#	TagInputSubmit( $type, $value, $key );
#
# - ARGS
#	$type	submit/reset
#	$value	ラベルに使われる
#	$key	accesskeyに使われる
#
sub TagInputSubmit
{
    local( $type, $value, $key ) = @_;
    $gTabIndex++;
    if ( $type eq 'reset' )
    {
	qq(<input type="reset" value="$value" accesskey="$key" tabindex="$gTabIndex" />);
    }
    else
    {
	qq(<input type="submit" value="$value" accesskey="$key" tabindex="$gTabIndex" />);
    }
}


###
## TagInputText - 入力タグのフォーマット
#
# - SYNOPSIS
#	TagInputText( $type, $id, $value, $size );
#
# - ARGS
#	$type	text/password
#	$id	idとnameに使われる
#	$value	デフォルト値に使われる
#	$size	sizeに使われる
#
sub TagInputText
{
    local( $type, $id, $value, $size ) = @_;
    $gTabIndex++;
    qq(<input type="$type" id="$id" name="$id" value="$value" size="$size" tabindex="$gTabIndex" />);
}


###
## TagInputCheck - チェックボックスタグのフォーマット
#
# - SYNOPSIS
#	TagInputCheck( $id, $checked );
#
# - ARGS
#	$id		idとnameに使われる
#	$checked	trueならcheckedが付く
#
# - DESCRIPTION
#	valueは"on"固定．
#
sub TagInputCheck
{
    local( $id, $checked ) = @_;
    $gTabIndex++;
    if ( $checked )
    {
	qq(<input type="checkbox" id="$id" name="$id" value="on" tabindex="$gTabIndex" checked="checked" />);
    }
    else
    {
	qq(<input type="checkbox" id="$id" name="$id" value="on" tabindex="$gTabIndex" />);
    }
}


###
## TagInputRadio - ラジオボタンタグのフォーマット
#
# - SYNOPSIS
#	TagInputRadio( $id, $name, $value, $checked );
#
# - ARGS
#	$id		idに使われる
#	$name		nameに使われる
#	$value		デフォルト値に使われる
#	$checked	trueならcheckedが付く
#
sub TagInputRadio
{
    local( $id, $name, $value, $checked ) = @_;
    $gTabIndex++;
    if ( $checked )
    {
	qq(<input type="radio" id="$id" name="$name" value="$value" tabindex="$gTabIndex" checked="checked" />);
    }
    else
    {
	qq(<input type="radio" id="$id" name="$name" value="$value" tabindex="$gTabIndex" />);
    }
}


###
## TagTextarea - textareaタグのフォーマット
#
# - SYNOPSIS
#	TagTextarea( $id, $value, $rows, $cols );
#
# - ARGS
#	$id	idとnameに使われる
#	$value	デフォルト値に使われる
#	$rows	rowsに使われる
#	$cols	colsに使われる
#
sub TagTextarea
{
    local( $id, $value, $rows, $cols ) = @_;
    $gTabIndex++;
    qq(<textarea id="$id" name="$id" rows="$rows" cols="$cols" tabindex="$gTabIndex">$value</textarea>);
}


###
## TagSelect - selectタグのフォーマット
#
# - SYNOPSIS
#	TagSelect( $id, $contents );
#
# - ARGS
#	$id		idとnameに使われる
#	$contents	選択肢用コンテンツ
#
sub TagSelect
{
    local( $id, $contents ) = @_;
    $gTabIndex++;
    qq(<select id="$id" name="$id" tabindex="$gTabIndex">$contents</select>);
}


###
## TagFieldset - fieldsetタグのフォーマット
#
# - SYNOPSIS
#	TagFieldset( $title, $contents );
#
# - ARGS
#	$title		legendに使われる
#	$contents	fieldsetのコンテンツ
#
sub TagFieldset
{
    local( $title, $contents ) = @_;
    qq(<fieldset>\n<legend>$title</legend>\n$contents</fieldset>\n);
}


###
## LinkP - 自プログラム向けリンクの生成
#
# - SYNOPSIS
#	LinkP( $href, $markUp );
#
# - ARGS
#	$comm		リンク先コマンド部（〜?以降）
#	$markUp		マークアップ文字列
#	$key		アクセスキー（省略可）
#	$title		タイトル文字列（省略可）
#	$name		アンカ名（省略可）
#	$fragment	#以降に使う（省略可）
#
# - DESCRIPTION
#	自プログラムへのリンクを生成する
#
sub LinkP
{
    local( $comm, $markUp, $key, $title, $name, $fragment ) = @_;
    $comm .= "&kinoA=3&kinoU=$UNAME_ESC&kinoP=$PASSWD" if ( $SYS_AUTH == 3 );
    $comm =~ s/&/&amp;/go;
    $comm .= "#$fragment" if ( $fragment ne '' );
    &TagA( $markUp, "$PROGRAM?$comm", $key, $title, $name );
}


###
## CollectDaughters - 娘ノードのリストを集める
#
# - SYNOPSIS
#	CollectDaughters($Id);
#
# - ARGS
#	$Id		記事ID
#
# - DESCRIPTION
#	娘ノードのリストを集める
#
# - RETURN
#	娘ノード集合のリスト
#
sub CollectDaughters
{
    local( $Id ) = @_;
    local( @Return );
    foreach ( split(/,/, &getMsgDaughters( $Id )))
    {
	push( @Return, $_ );
	push( @Return, &CollectDaughters( $_ )) if ( &getMsgDaughters( $_ ) ne '' );
    }
    @Return;
}


###
## GetNewArticleId - 新着記事IDの決定
#
# - SYNOPSIS
#	GetNewArticleId($Board);
#
# - ARGS
#	$Board		掲示板ID
#
# - DESCRIPTION
#	従来の最新記事IDを1増やした，新しい記事番号を返す．
#
# - RETURN
#	新着記事のID
#
sub GetNewArticleId
{
    local( $Board ) = @_;
    local( $id, $artKey );
    &GetArticleId( $Board, *id, *artKey );
    $id + 1;
}


###
## GetTitleOldIndex - 'old'値の取得
#
# - SYNOPSIS
#	GetTitleOldIndex( $id );
#
# - ARGS
#	$id	記事番号
#
# - DESCRIPTION
#	指定したIDの記事を含むようなold値を計算する．
#	DbCacheが呼び出し済みでなければならない．
#
# - RETURN
#	old値
#
sub GetTitleOldIndex
{
    local( $id ) = @_;
    local( $old ) = &getNofMsg() - int( $id + $DEF_TITLE_NUM/2 );
    ( $old >= 0 )? $old : 0;
}


###
## LockAll/UnlockAll - システムのロック/アンロック
## LockBoard/UnlockBoard - 掲示板のロック/アンロック
#
# - SYNOPSIS
#	LockAll();
#	UnlockAll();
#	LockBoard();
#	UnlockBoard();
#
# - DESCRIPTION
#	システム/掲示板をロック/アンロックする．
#	ロックに使うファイルは$LOCK_FILE/$LOCK_FILE_B．
#
# - RETURN
#	なし．戻れば成功．失敗すればエラーページへ．
#
sub LockAll
{
    local( $lockResult ) = $PC ? 1 : &cgi'lock_file( $LOCK_FILE );
    &Fatal( 1001, '' ) if ( $lockResult == 2 );
    &Fatal( 999, '' ) if ( $lockResult != 1 );
    &LockBoard() if $LOCK_FILE_B;
}

sub UnlockAll
{
    &cgi'unlock_file( $LOCK_FILE ) unless $PC;
    &UnlockBoard() if $LOCK_FILE_B;
}

sub LockBoard
{
    local( $lockResult ) = $PC ? 1 : &cgi'lock_file( $LOCK_FILE_B );
    &Fatal( 1001, '' ) if ( $lockResult == 2 );
    &Fatal( 999, '' ) if ( $lockResult != 1 );
}

sub UnlockBoard
{
    &cgi'unlock_file( $LOCK_FILE_B ) unless $PC;
}


###
## IsUser - ユーザのチェック
#        
# - SYNOPSIS
#       IsUser( $name );
#
# - ARGS
#       $name           ユーザ名
#
# - DESCRIPTION
#       現在の利用ユーザが$nameかどうか確かめる．
#	権限チェックは$POLICYにまとめている．
#	権限チェックに関することは，この関数に依存しないようにすべきである．
#   
# - RETURN
#       true/false
#
sub IsUser
{
    local( $name ) = @_;
    ( $SYS_AUTH && (( $UNAME eq $name ) || (( $UNAME eq $ADMIN ) && ( $name eq $MAINT_NAME ))));
}


###
## SendArticleMail - メイル送信
#
# - SYNOPSIS
#	SendArticleMail(
#	    $FromName,	メイル送信者名
#	    $FromAddr,	メイル送信者メイルアドレス
#	    $Subject,	メイルのSubject文字列
#	    $Message,	本文
#	    $Id,	引用するなら記事ID; 空なら引用ナシ
#	    @To		宛先E-Mail addr.のリスト
#	)
#
# - DESCRIPTION
#	メイルを送信する．
#
sub SendArticleMail
{
    local( $FromName, $FromAddr, $Subject, $Message, $Id, @To ) = @_;

    local( $ExtHeader, @ArticleBody );

    $ExtHeader = "X-MLServer: $PROGNAME\n";
    $ExtHeader .= "X-Kb-System: $SYSTEM_NAME\n";
    if (( ! $SYS_MAILHEADBRACKET ) && $BOARDNAME && ($Id ne '' ))
    {
	$ExtHeader .= "X-Kb-Board: $BOARDNAME\nX-Kb-Articleid: $Id\n";
    }

    local( $stat, $errstr ) = &SendMail( $FromName, $FromAddr, $Subject, $ExtHeader, $Message, @To );
    &Fatal( 9, "$BOARDNAME/$Id/$errstr" ) unless $stat;
}


###
## SendMail - メイル送信
#
# - SYNOPSIS
#	SendMail(
#	    $FromName,	メイル送信者名
#	    $FromAddr,	メイル送信者メイルアドレス
#	    $Subject,	メイルのSubject文字列
#	    $ExtHeader,	追加ヘッダ
#	    $Message,	本文
#	    @To		宛先E-Mail addr.のリスト
#	)
#
# - DESCRIPTION
#	メイルを送信する．
#
# - RETURN
#	( $status, $errstr )
#		$status		0 if succeeded, errCode if failed.
#		$errstr		errstr if failed.
#
sub SendMail
{
    local( $FromName, $FromAddr, $Subject, $ExtHeader, $Message, @To ) = @_;

    if ( !$FromAddr )
    {
	# メイルアドレス未入力につき，管理者名義で出す．
	$FromName = ( $MAILFROM_LABEL || $MAINT_NAME );
	$FromAddr = $MAINT;
    }

    local( $SenderFrom, $SenderAddr ) = (( $MAILFROM_LABEL || $MAINT_NAME ),
	$MAINT );
    &cgi'sendMail( $FromName, $FromAddr, $SenderFrom, $SenderAddr, $Subject,
 	$ExtHeader, $Message, $MAILTO_LABEL, @To );
}


###
## KbLog - ログ処理
#
# - SYNOPSIS
#	KbLog( $kinologue'severity, *msg );
#
# - ARGS
#	$kinologue'severity	severity id defined in kinologue.pl.
#	*msg			reference to msg string.
#
# - DESCRIPTION
#	log a log using kinologue.
#	exit program(not function) if failed to write log.
#
sub KbLog
{
    local( $severity, $msg ) = @_;

    if ( $SYS_LOG )
    {
	$msg .= "(Remote host:$REMOTE_INFO)" if $SYS_LOGHOST;
	local( $logfile ) = ( $severity >= $kinologue'SEV_ERROR )?
	    "$LOG_DIR/$ERROR_LOG" :
	    "$LOG_DIR/$ACCESS_LOG";
	$logfile .= ( $SYS_LOG == 1 )? '.html' : '.txt';

	&kinologue'KlgLog( $severity, $msg, $PROGNAME, $logfile,
	    ( $SYS_LOG == 1 )? $kinologue'FF_HTML : $kinologue'FF_PLAIN )
	    || &Fatal( 1000, '' );
    }
}


###
## Fatal - エラー処理
#
# - SYNOPSIS
#	Fatal( $errno, $errInfo );
#
# - ARGS
#	$errno	エラー番号(詳しくは関数内部を参照のこと)
#	$errInfo	エラー情報
#
# - DESCRIPTION
#	エラーを表す画面をブラウザに送信する．
#
# - RETURN
#	なし
#
sub Fatal
{
    local( $errno, $errInfo ) = @_;

    local( $severity, $msg ) = &FatalStr( $errno, $errInfo );

    # 異常終了の可能性があるので，とりあえずlockを外す
    # (ロックの失敗の時以外)
    if ( !$PC && ( $errno != 999 ) && ( $errno != 1001 ))
    {
	&UnlockAll();
    }

    # log a log(except logging failure).
    &KbLog( $severity, $msg ) if ( $errno != 1000 );
    &UIFatal( $msg );
    &KbLog( $kinologue'SEV_INFO, 'Exec finished.' ) if ( $errno != 1000 );
    exit( 0 );
}


###
## FatalStr - エラーコードから重要度とエラーメッセージを取得
#        
# - SYNOPSIS
#	FatalStr( $errno, $errInfo );
#
# - ARGS
#	$errno		エラーコード
#	$errInfo	付加情報
#
# - DESCRIPTION
#	エラーコードから重要度とエラーメッセージを取得する．
#   
# - RETURN
#	( $severity, $mst )
#
sub FatalStr
{
    local( $errno, $errInfo ) = @_;

    local( $severity, $msg );
    if ( $errno == 1 )
    {
	$severity = $kinologue'SEV_CAUTION;
	$msg = "File: $errInfoが存在しない，あるいはpermissionの設定が間違っています．";
    }
    elsif ( $errno == 2 )
    {
	$severity = $kinologue'SEV_INFO;
	$msg = "「$errInfo」が入力されていません．戻ってもう一度やり直してみてください．";
    }
    elsif ( $errno == 3 )
    {
	$severity = $kinologue'SEV_INFO;
	$msg = "$H_SUBJECTや$H_FROM，$H_MAILに，タブ文字か改行が入ってしまっています．戻ってもう一度やり直してみてください．";
    }
    elsif ( $errno == 4 )
    {
	$severity = $kinologue'SEV_INFO;
	$msg = "題中にHTMLタグを入れることは禁じられています．戻って違う題に書き換えてください．";
    }
    elsif ( $errno == 5 )
    {
	$severity = $kinologue'SEV_INFO;
	$msg = "「$errInfo」という$H_FROMは使えません．戻って別の$H_FROMを指定してください．";
    }
    elsif ( $errno == 6 )
    {
	$severity = $kinologue'SEV_WARN;
	$msg = "「$errInfo」という$H_MAILは登録済みです．";
    }
    elsif ( $errno == 7 )
    {
	$severity = $kinologue'SEV_INFO;
	$msg = "$errInfoがおかしくありませんか? 戻ってもう一度やり直してみてください．";
    }
    elsif ( $errno == 8 )
    {
	$severity = $kinologue'SEV_INFO;
	$msg = "次の$H_MESGはまだ投稿されていません．";
    }
    elsif ( $errno == 9 )
    {
	local( $board, $id, $info ) = split( /\//, $errInfo, 3 );
	$severity = $kinologue'SEV_ERROR;
	$msg = "ホストマシンの過剰負荷，メイルアドレスの誤記等の理由により，$H_MESGのメイルでの配信が失敗しました（$H_BOARD: $board，ID: $id，原因: $info）．$H_MESGは正しく書き込まれましたので，再度書き込みの必要はありません．";
    }
    elsif ( $errno == 10 )
    {
	$severity = $kinologue'SEV_CAUTION;
	$msg = "kb.dbとkb.aidの整合性が取れていません．";
    }
    elsif ( $errno == 11 )
    {
	$severity = $kinologue'SEV_ERROR;
	$msg = "$errInfoというIDに対応する$H_BOARDは，存在しません．";
    }
    elsif ( $errno == 12 )
    {
	$severity = $kinologue'SEV_WARN;
	$msg = "この$H_BOARDでは，$H_MESGの最大サイズは$SYS_MAXARTSIZEバイトということになっています（あなたの$H_MESGは$errInfoバイトです）．";
    }
    elsif ( $errno == 13 )
    {
	$severity = $kinologue'SEV_FATAL;
	$msg = "$errInfoへの書き込みに失敗しました．ファイルシステムに空き容量がない可能性があります．";
    }
    elsif ( $errno == 14 )
    {
	$severity = $kinologue'SEV_FATAL;
	$msg = "次のrenameに失敗しました（$errInfo）．ファイルパーミッションの設定ミスの可能性があります．";
    }
    elsif ( $errno == 15 )
    {
	$severity = $kinologue'SEV_ERROR;
	$msg = "書き込み元の入力フォームが古過ぎます．．．";
    }
    elsif ( $errno == 16 )
    {
	$severity = $kinologue'SEV_ERROR;
	$msg = "同一書き込みフォームからの連続書き込みは禁止されています．連続して$H_MESGを書き込む場合は，書き込みフォームも再度読み込み直してからにしてください．";
    }
    elsif ( $errno == 17 )
    {
	$severity = $kinologue'SEV_ERROR;
	$msg = "現在，$H_ICONが使える設定になっていません．$H_ICONを使える設定に変更してから再度やり直してください．";
    }
    elsif ( $errno == 18 )
    {
	local( $file, $func ) = split( /\//, $errInfo, 2 );
	$severity = $kinologue'SEV_ERROR;
	$msg = "$fileの中で$funcを利用することはできません．．．";
    }
    elsif ( $errno == 19 )
    {
	$severity = $kinologue'SEV_WARN;
	$msg = "$H_REPLYのある$H_MESGは訂正/削除できません．．．";
    }
    elsif ( $errno == 20 )
    {
	$severity = $kinologue'SEV_FATAL;
	$msg = "次のcopyに失敗しました（$errInfo）．ファイルパーミッションの設定ミスの可能性があります．";
    }
    elsif ( $errno == 21 )
    {
	$severity = $kinologue'SEV_INFO;
	$msg = "$H_DATEのフォーマットが'yyyy/mm/dd(HH:MM:SS)'ではありません．戻ってもう一度やり直してみてください．";
    }
    elsif ( $errno == 40 )
    {
	$severity = $kinologue'SEV_WARN;
	$msg = "$H_PASSWDを間違えていませんか? $H_FROMと$H_PASSWDを確認し，戻ってやり直してみてください．" . &LinkP( "c=lo", "ユーザ設定の呼び出し" . &TagAccessKey( 'L' ), 'L' );
    }
    elsif ( $errno == 41 )
    {
	$severity = $kinologue'SEV_WARN;
	$msg = "「$errInfo」という$H_FROMは登録されていないようです．．．";
    }
    elsif ( $errno == 42 )
    {
	$severity = $kinologue'SEV_INFO;
	$msg = "2つの$H_PASSWDが異なっているようです．ミス防止のため，$H_PASSWDは同じものを2度入力します．戻ってやり直してみてください．";
    }
    elsif ( $errno == 44 )
    {
	$severity = $kinologue'SEV_WARN;
	$msg = "ごめんなさい，この機能は利用できません．．．";
    }
    elsif ( $errno == 50 )
    {
	$severity = $kinologue'SEV_INFO;
	$msg = "$H_REPLY関係が循環してしまいます．どうしても$H_REPLY先を変更したい場合，$H_REPLY先を一度新着扱いにしてから，$H_REPLYをかけかえてください．";
    }
    elsif ( $errno == 51 )
    {
	$severity = $kinologue'SEV_INFO;
	$msg = "「$errInfo」という$H_BOARDは既に存在します．．．";
    }
    elsif ( $errno == 52 )
    {
	$severity = $kinologue'SEV_INFO;
	$msg = "$H_BOARD略称は，半角のアルファベットもしくは数字にしてください．";
    }
    elsif ( $errno == 99 )
    {
	$severity = $kinologue'SEV_WARN;
	$msg ="この$H_BOARDでは，このコマンド（$errInfo）は実行できません．";
    }
    elsif ( $errno == 998 )
    {
	$severity = $kinologue'SEV_FATAL;
	$msg = "不明なエラー（$errInfo）．";
    }
    elsif ( $errno == 999 )
    {
	$severity = $kinologue'SEV_WARN;
	$msg ="システムのロックに失敗しました．混み合っているようですので，数分待ってからもう一度アクセスしてください．";
    }
    elsif ( $errno == 1000 )
    {
	$severity = $kinologue'SEV_FATAL;
	$msg ="ログファイルへの書き込みに失敗しました．";
    }
    elsif ( $errno == 1001 )
    {
	$severity = $kinologue'SEV_WARN;
	$msg ="現在管理者によるメンテナンス中です．しばらくお待ちください．";
    }
    else
    {
	$severity = $kinologue'SEV_ANY;
	$msg = "エラー番号不定（$errInfo）";
    }

    if ( $severity >= $kinologue'SEV_CAUTION )
    {
	$msg .= "大変お手数ですが，このページのURL（" . $cgi'REQUEST_URI . "），このメッセージ全文のコピーと，エラーが生じた状況を，" . &TagA( $MAINT, "mailto:$MAINT" ) . "までお知らせ頂けると助かります．";
    }

    return ( $severity, $msg );
}


######################################################################
# データインプリメンテーション


###
## CopyDb - DBのコピー
#
# - SYNOPSIS
#	CopyDb( $src, $dest );
#
# - ARGS
#	$src	コピー元
#	$dest	コピー先
#
# - DESCRIPTION
#	$src, $destをファイル名と見倣してDBをコピーする．
#	$destは上書きされるので注意．
#
# - RETURN
#	true if succeeded.
#
sub CopyDb
{
    local( $src, $dest ) = @_;
    open( SRC, "<$src" ) || return 0;
    open( DEST, ">$dest" ) || return 0;
    while ( <SRC> )
    {
	print( DEST $_ ) || return 0;
    }
    close DEST || return 0;
    close SRC;

    1;
}


###
## GenTSV - タブ区切り文字列の作成
#
# - SYNOPSIS
#	GenTSV( *line, @data );
#
# - ARGS
#	$line	タブ区切りのデータを格納する文字列
#	@data	データ
#
# - DESCRIPTION
#	データをTSVフォーマットに整形する．
#	データは改行を含んではならない．
#
sub GenTSV
{
    local( *line, @data ) = @_;
    grep( s/\t/$COLSEP/go, @data );
    $line = join( "\t", @data );
}


###
## GenCSV - カンマ区切り文字列の作成
#
# - SYNOPSIS
#	GenCSV( *line, @data );
#
# - ARGS
#	$line	タブ区切りのデータを格納する文字列
#	@data	データ
#
# - DESCRIPTION
#	データをCSVフォーマットに整形する．
#
sub GenCSV
{
    local( *line, @data ) = @_;
    grep((( s/\"/\"\"/go || m/,/o || m/\n/o ) && ( $_ = "\"$_\"" )), @data );
    $line = join( ',', @data );
}


###
## ParseTSV - タブ区切り文字列の解析
#
# - SYNOPSIS
#	ParseTSV( *src, *dataArray );
#
# - ARGS
#	$src		解析元データ
#	@dataArray	解析したデータを格納するリスト
#
# - DESCRIPTION
#	データをTSVフォーマットに整形する．
#
sub ParseTSV
{
    local( *src, *dataArray ) = @_;
    @dataArray = split( /\t/, $src );
}


###
## DbCache - 記事DBの全読み込み
#
# - SYNOPSIS
#	DbCache($Board);
#
# - ARGS
#	$Board		掲示板ID
#
# - DESCRIPTION
#	主に起動時に呼び出され，記事DBの内容を大域変数にキャッシュする．
#
sub DbCache
{
    return if $gBoardDbCached;

    local( $Board ) = @_;

    local( $dId, $dFid, $dAids, $dDate, $dTitle, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail );

    @DB_ID = %DB_FID = %DB_AIDS = %DB_DATE = %DB_TITLE = %DB_ICON = %DB_REMOTEHOST = %DB_NAME = %DB_EMAIL = %DB_URL = %DB_FMAIL = %DB_NEW = ();

    local( $newIconLimit );
    $newIconLimit = $^T - $SYS_NEWICON_VALUE * 24 * 60 * 60
	if ( $SYS_NEWICON == 2 );
    
    local( $i ) = 0;
    local( @data, $dId );
    local( $DBFile ) = &GetPath( $Board, $DB_FILE_NAME );
    open( DB, "<$DBFile" ) || &Fatal( 1, $DBFile );
    while ( <DB> )
    {
	next if (/^\#/o || /^$/o);
	chop;
	( $dId, $dFid, $dAids, $dDate, $dTitle, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail ) = split( /\t/, $_, 11 );
	$DB_ID[$i++] = $dId;
	$DB_FID{$dId} = $dFid;
	$DB_AIDS{$dId} = $dAids;
	$DB_DATE{$dId} = $dDate || &GetModifiedTime( $dId, $Board );
	$DB_TITLE{$dId} = $dTitle || $dId;
	$DB_ICON{$dId} = $dIcon;
	$DB_REMOTEHOST{$dId} = $dRemoteHost;
	$DB_NAME{$dId} = $dName || $MAINT_NAME;
	$DB_EMAIL{$dId} = $dEmail;
	$DB_URL{$dId} = $dUrl;
	$DB_FMAIL{$dId} = $dFmail;

	if (( $SYS_NEWICON == 2 ) && ( $newIconLimit < $DB_DATE{$dId} ))
	{
	    $DB_NEW{$dId} = 1
	}
    }
    close DB;

    if ( $SYS_NEWICON == 1 )
    {
	local( $from ) = ( $#DB_ID >= $SYS_NEWICON_VALUE )?
	    $#DB_ID - $SYS_NEWICON_VALUE + 1 : 0;
	foreach ( $from .. $#DB_ID ) { $DB_NEW{ $DB_ID[$_] } = 1; }
    }

    $gBoardDbCached = 1;		# cached
}


###
## getBoardLastmod - ある掲示板の最終更新時刻を取得
#
# - SYNOPSIS
#	getBoardLastmod( $board );
#
# - ARGS
#	$board		掲示板ID
#
# - DESCRIPTION
#	掲示板用のメッセージDBファイルの最終更新時刻を計算し，
#	その掲示板の最終更新時刻として返す．
#
# - RETURN
#	UTCからの経過秒数
#
sub getBoardLastmod
{
    local( $board ) = @_;

    # 86400 = 24 * 60 * 60
    $^T - ( -M &GetPath( $board, $DB_FILE_NAME )) * 86400;
}


###
## getNofMsg - メッセージ数の取得
#
# - SYNOPSIS
#	getNofMsg();
#
# - DESCRIPTION
#	全メッセージ数を取得する．削除済みメッセージは数に入らない．
#
# - RETURN
#	メッセージ数
#
sub getNofMsg
{
    $#DB_ID;
}


###
## getMsgId - メッセージIDの取得
#
# - SYNOPSIS
#	getMsgId( $num );
#
# - ARGS
#	$num	メッセージ番号
#
# - DESCRIPTION
#	メッセージ番号からメッセージIDを取得する．
#
# - RETURN
#	メッセージID
#
sub getMsgId
{
    $DB_ID[ $_[0] ];
}


###
## getMsgNewP - メッセージが新しいか否か
#
# - SYNOPSIS
#	getMsgNewP( $id );
#
# - ARGS
#	$id	メッセージID
#
# - DESCRIPTION
#	メッセージが新しいか否かを返す．
#
# - RETURN
#	1 if true, 0 if false.
#
sub getMsgNewP
{
    $DB_NEW{ $_[0] };
}


###
## getMsgInfo - メッセージ情報の取得
#
# - SYNOPSIS
#	getMsgInfo( $id );
#
# - ARGS
#	$id	メッセージID
#
# - DESCRIPTION
#	メッセージ情報を取得する．
#
# - RETURN
#	メッセージ情報のリスト
#		親メッセージIDのリスト(「,」区切り)
#		このメッセージにリプライしたメッセージのIDのリスト(「,」区切り)
#		投稿時間（UTCからの経過秒数）
#		Subject
#		アイコンID
#		投稿ホスト
#		投稿者名
#		投稿者E-Mail
#		投稿者URL
#		リプライがあった時に投稿者にメイルを送るか否か
#
sub GetArticlesInfo { &getMsgInfo; }
sub getMsgInfo
{
    local( $id ) = @_;
    ( $DB_FID{$id}, $DB_AIDS{$id}, $DB_DATE{$id}, $DB_TITLE{$id}, $DB_ICON{$id}, $DB_REMOTEHOST{$id}, $DB_NAME{$id}, $DB_EMAIL{$id}, $DB_URL{$id}, $DB_FMAIL{$id} );
}


###
## getMsgParents - メッセージ親情報の取得
## getMsgDaughters - メッセージ娘情報の取得
## getMsgSubject - メッセージタイトルの取得
## getMsgIcon - メッセージアイコンの取得
## setMsgParents - メッセージ親情報の設定
## setMsgDaughters - メッセージ娘情報の設定
#
# - SYNOPSIS
#	getMsgParents( $id );
#	getMsgDaughters( $id );
#	getMsgSubject( $id );
#	getMsgIcon( $id );
#
#	setMsgParents( $id, $value );
#	setMsgDaughters( $id, $value );
#
# - ARGS
#	$id	メッセージID
#	$value	メッセージIDのリスト（「,」区切り）
#
# - DESCRIPTION
#	メッセージ親/娘情報を取得する．
#
# - RETURN
#	get*
#		親メッセージIDのリスト（「,」区切り）
#		娘メッセージIDのリスト（「,」区切り）
#	set*
#		なし
#
sub getMsgParents { $DB_FID{ $_[0] }; }
sub getMsgDaughters { $DB_AIDS{ $_[0] }; }
sub getMsgSubject { $DB_TITLE{ $_[0] }; }
sub getMsgIcon { $DB_ICON{ $_[0] }; }

sub setMsgParents { $DB_FID{ $_[0] } = $_[1]; }
sub setMsgDaughters { $DB_AIDS{ $_[0] } = $_[1]; }


###
## getMsgAuthor - メッセージ投稿者情報の取得
#
# - SYNOPSIS
#	getMsgAuthor( $id );
#
# - ARGS
#	$id	メッセージID
#
# - DESCRIPTION
#	メッセージ投稿者情報を取得する．
#
# - RETURN
#	メッセージ投稿者情報のリスト
#		投稿者名
#		投稿者E-Mail
#		投稿者URL
#		リプライがあった時に投稿者にメイルを送るか否か
#		投稿ホスト
#
sub getMsgAuthor
{
    ( $DB_NAME{ $_[0] }, $DB_EMAIL{ $_[0] }, $DB_URL{ $_[0] }, $DB_FMAIL{ $_[0] }, $DB_REMOTEHOST{ $_[0] } );
}


###
## AddDBFile - 記事DBへの追加
#
# - SYNOPSIS
#	AddDBFile($Id, $Board, $Fid, $InputDate, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail);
#
# - ARGS
#	$Id		記事ID
#	$Board		掲示板ID
#	$Fid		リプライ元の記事ID
#	$InputDate	書き込み日付(UTC)
#	$Subject	Subject
#	$Icon		アイコンID
#	$RemoteHost	書き込みホスト(IP addr.かFQDNかはhttpサーバ次第)
#	$Name		投稿者名
#	$Email		投稿者E-Mail addr.
#	$Url		投稿者URL
#	$Fmail		リプライ時にメイルを送るか否か(''/'on')
#	$MailRelay	追加した記事をメイルとして流すかどうか
#
# - DESCRIPTION
#	記事DBに記事を追加する．
#
sub AddDBFile
{
    local( $Id, $Board, $Fid, $InputDate, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail, $MailRelay ) = @_;

    local( $dId, $dFid, $dAids, $dInputDate, $dSubject, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail, $mdName, $mdEmail, $mdInputDate, $mdSubject, $mdIcon, $mdId, $FidList, @FollowMailTo, @FFid );

    # メイル送信用に，リプライ元のリプライ元，を取ってくる
    if ( $Fid ne '' )
    {
	@FFid = split( /,/, &getMsgParents( $Fid ));
    }

    $FidList = $Fid;

    local( $File ) = &GetPath( $Board, $DB_FILE_NAME );
    local( $TmpFile ) = &GetPath( $Board, "$DB_FILE_NAME.$TMPFILE_SUFFIX$$" );
    local( $dbLine );
    open( DBTMP, ">$TmpFile" ) || &Fatal( 1, $TmpFile );
    open( DB, "<$File" ) || &Fatal( 1, $File );
    while ( <DB> )
    {
	if ( /^\#/o || /^$/o )
	{
	    print( DBTMP "$_" ) || &Fatal( 13, $TmpFile );
	    next;
	}

	chop;

	( $dId, $dFid, $dAids, $dInputDate, $dSubject, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail ) = split( /\t/, $_ );
	
	# フォロー先記事が見つかったら，
	if (( $dId ne '' ) && ( $dId eq $Fid ))
	{
	    # その記事のフォロー記事IDリストに加える(カンマ区切り)
	    if ( $dAids ne '' )
	    {
		$dAids .= ",$Id";
	    }
	    else
	    {
		$dAids = $Id;
	    }

	    # 元記事のフォロー先リストを取ってきて元記事を加え，
	    # 新記事のフォロー先リストを作る
	    if ( $dFid ne '' )
	    {
		$FidList = "$dId,$dFid";
	    }

	    if ( $MailRelay && ( $SYS_MAIL & 2 ))
	    {
		# メイル送信のためにキャッシュ
		$mdName = $dName;
		$mdEmail = $dEmail;
		$mdInputDate = $dInputDate;
		$mdSubject = $dSubject;
		$mdIcon = $dIcon;
		$mdId = $dId;
		push( @FollowMailTo, $dEmail ) if $dFmail && $dEmail;
	    }
	}

	# DBに書き加える
	&GenTSV( *dbLine, ( $dId, $dFid, $dAids, $dInputDate, $dSubject, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail ));
	print( DBTMP "$dbLine\n" ) || &Fatal( 13, $TmpFile );

	# リプライ元のリプライ元，かつメイル送信の必要があれば，宛先を保存
	if ( $MailRelay && ( $SYS_MAIL & 2 ) && @FFid && $dFmail && $dEmail && ( grep( /^$dId$/, @FFid )) && ( !grep( /^$dEmail$/, @FollowMailTo )))
	{
	    push( @FollowMailTo, $dEmail );
	}
    }

    # 新しい記事のデータを書き加える．
    &GenTSV( *dbLine, ( $Id, $FidList, '', $InputDate, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail ));
    print( DBTMP "$dbLine\n" ) || &Fatal( 13, $TmpFile );

    # close Files.
    close DB;
    close DBTMP || &Fatal( 13, $TmpFile );

    # DBを更新する
    rename( $TmpFile, $File ) || &Fatal( 14, "$TmpFile -&gt; $File" );

    # 必要なら投稿があったことをメイルする
    if ( $MailRelay && $SYS_MAIL & 1 )
    {
	local( @ArriveMailTo );
	&GetArriveMailTo( 0, $Board, *ArriveMailTo );
	&ArriveMail( $Name, $Email, $InputDate, $Subject, $Icon, $Id, @ArriveMailTo ) if @ArriveMailTo;
    }

    # 必要なら反応があったことをメイルする
    if ( $MailRelay && ( $SYS_MAIL & 2 ) && @FollowMailTo )
    {
	&FollowMail( $mdName, $mdEmail, $mdInputDate, $mdSubject, $mdIcon, $mdId, $Name, $Email, $InputDate, $Subject, $Icon, $Id, @FollowMailTo );
    }
}


###
## UpdateArticleDb - 記事DBの全更新
#
# - SYNOPSIS
#	UpdateArticleDb($Board);
#
# - ARGS
#	$Board		掲示板ID
#
# - DESCRIPTION
#	記事DBを，新たな記事データで全更新する．
#	書き込む記事データはキャッシュされているもの．
#
sub UpdateArticleDb
{
    local( $Board ) = @_;

    local( $dId, $dbLine );
    local( $File ) = &GetPath($Board, $DB_FILE_NAME);
    local( $TmpFile ) = &GetPath( $Board, "$DB_FILE_NAME.$TMPFILE_SUFFIX$$" );
    open( DBTMP, ">$TmpFile" ) || &Fatal( 1, $TmpFile );
    open( DB, "<$File" ) || &Fatal( 1, $File );
    while ( <DB> )
    {
	if ( /^\#/o || /^$/o )
	{
	    print( DBTMP "$_" ) || &Fatal( 13, $TmpFile );
	    next;
	}

	# Idを取り出す
	chop;
	( $dId = $_ ) =~ s/\t.*$//;

	# DBに書き加える
	&GenTSV( *dbLine, ( $dId, $DB_FID{$dId}, $DB_AIDS{$dId}, $DB_DATE{$dId}, $DB_TITLE{$dId}, $DB_ICON{$dId}, $DB_REMOTEHOST{$dId}, $DB_NAME{$dId}, $DB_EMAIL{$dId}, $DB_URL{$dId}, $DB_FMAIL{$dId} ));
	print( DBTMP "$dbLine\n" ) || &Fatal( 13, $TmpFile );
    }

    # close Files.
    close DB;
    close DBTMP || &Fatal( 13, $TmpFile );

    # DBを更新する
    rename( $TmpFile, $File ) || &Fatal( 14, "$TmpFile -&gt; $File" );
}


###
## DeleteArticleFromDbFile - 記事DBの更新
#
# - SYNOPSIS
#	DeleteArticleFromDbFile($Board, *Target);
#
# - ARGS
#	$Board		掲示板ID
#	*Target		削除する記事IDのリスト
#
# - DESCRIPTION
#	記事DBから指定された記事群のエントリを削除する．
#
sub DeleteArticleFromDbFile
{
    local( $Board, *Target ) = @_;

    local( $dId, $dbLine );
    local( $File ) = &GetPath( $Board, $DB_FILE_NAME );
    local( $TmpFile ) = &GetPath( $Board, "$DB_FILE_NAME.$TMPFILE_SUFFIX$$" );
    open( DBTMP, ">$TmpFile" ) || &Fatal( 1, $TmpFile );
    open( DB, "<$File" ) || &Fatal( 1, $File );
    while ( <DB> )
    {
	if ( /^\#/o || /^$/o )
	{
	    print( DBTMP "$_" ) || &Fatal( 13, $TmpFile );
	    next;
	}

	# Idを取り出す
	chop;
	( $dId = $_ ) =~ s/\t.*$//;

	# 該当記事はコメントアウト
	if ( grep( /^$dId$/, @Target ))
	{
	    print( DBTMP "#" ) || &Fatal( 13, $TmpFile );
	}

	&GenTSV( *dbLine, ( $dId, $DB_FID{$dId}, $DB_AIDS{$dId}, $DB_DATE{$dId}, $DB_TITLE{$dId}, $DB_ICON{$dId}, $DB_REMOTEHOST{$dId}, $DB_NAME{$dId}, $DB_EMAIL{$dId}, $DB_URL{$dId}, $DB_FMAIL{$dId} ));
	print( DBTMP "$dbLine\n" ) || &Fatal( 13, $TmpFile );
    }

    # close Files.
    close DB;
    close DBTMP || &Fatal( 13, $TmpFile );

    # DBを更新する
    rename( $TmpFile, $File ) || &Fatal( 14, "$TmpFile -&gt; $File" );
}


###
## ReOrderArticleDb - 記事DBの順序変更
#
# - SYNOPSIS
#	ReOrderArticleDb($Board, $Id, *Move);
#
# - ARGS
#	$Board		掲示板ID
#	$Id		移動先記事ID
#	*Move		移動する記事群のリストへのリファレンス
#
# - DESCRIPTION
#	指定された記事群を，指定された記事の下に移動する．
#	「下」がDB中で先か後かは，新着が上か下か，に依り異なる．
#
sub ReOrderArticleDb
{
    local( $Board, $Id, *Move ) = @_;

    # 先頭フラグ
    local( $TopFlag ) = 1;

    local( $dId, $dbLine );
    local( $File ) = &GetPath( $Board, $DB_FILE_NAME );
    local( $TmpFile ) = &GetPath( $Board, "$DB_FILE_NAME.$TMPFILE_SUFFIX$$" );
    open( DBTMP, ">$TmpFile" ) || &Fatal( 1, $TmpFile );
    open( DB, "<$File" ) || &Fatal( 1, $File );
    while ( <DB> )
    {
	if ( /^\#/o || /^$/o )
	{
	    print( DBTMP "$_" ) || &Fatal( 13, $TmpFile );
	    next;
	}

	# Idを取り出す
	chop;
	( $dId = $_ ) =~ s/\t.*$//;

	# 移動する奴は取り除く
	next if ( grep( /^$dId$/, @Move ));

	# 先頭にする時の処理(新着が下，の場合)
	if (( $Id eq '' ) && ( $SYS_BOTTOMTITLE == 1 ) && ( $TopFlag == 1 ))
	{
	    $TopFlag = 0;
	    foreach ( @Move )
	    {
		&GenTSV( *dbLine, ( $_, $DB_FID{$_}, $DB_AIDS{$_}, $DB_DATE{$_}, $DB_TITLE{$_}, $DB_ICON{$_}, $DB_REMOTEHOST{$_}, $DB_NAME{$_}, $DB_EMAIL{$_}, $DB_URL{$_}, $DB_FMAIL{$_} ));
		print( DBTMP "$dbLine\n" ) || &Fatal( 13, $TmpFile );
	    }
	}

	# 移動先がきたら，先に書き込む(新着が上，の場合)
	if (( $SYS_BOTTOMTITLE == 0 ) && ( $dId eq $Id ))
	{
	    foreach ( @Move )
	    {
		&GenTSV( *dbLine, ( $_, $DB_FID{$_}, $DB_AIDS{$_}, $DB_DATE{$_}, $DB_TITLE{$_}, $DB_ICON{$_}, $DB_REMOTEHOST{$_}, $DB_NAME{$_}, $DB_EMAIL{$_}, $DB_URL{$_}, $DB_FMAIL{$_} ));
		print( DBTMP "$dbLine\n" ) || &Fatal( 13, $TmpFile );
	    }
	}

	# DBに書き加える
	&GenTSV( *dbLine, ( $dId, $DB_FID{$dId}, $DB_AIDS{$dId}, $DB_DATE{$dId}, $DB_TITLE{$dId}, $DB_ICON{$dId}, $DB_REMOTEHOST{$dId}, $DB_NAME{$dId}, $DB_EMAIL{$dId}, $DB_URL{$dId}, $DB_FMAIL{$dId} ));
	print( DBTMP "$dbLine\n" ) || &Fatal( 13, $TmpFile );

	# 移動先がきたら，続けて書き込む(新着が下，の場合)
	if (( $SYS_BOTTOMTITLE == 1 ) && ( $dId eq $Id ))
	{
	    foreach ( @Move )
	    {
		&GenTSV( *dbLine, ( $_, $DB_FID{$_}, $DB_AIDS{$_}, $DB_DATE{$_}, $DB_TITLE{$_}, $DB_ICON{$_}, $DB_REMOTEHOST{$_}, $DB_NAME{$_}, $DB_EMAIL{$_}, $DB_URL{$_}, $DB_FMAIL{$_} ));
		print( DBTMP "$dbLine\n" ) || &Fatal( 13, $TmpFile );
	    }
	}
    }

    # 先頭にする時の処理(新着が上，の場合)
    if (( $Id eq '' ) && ( $SYS_BOTTOMTITLE == 0 ))
    {
	foreach ( @Move )
	{
	    &GenTSV( *dbLine, ( $_, $DB_FID{$_}, $DB_AIDS{$_}, $DB_DATE{$_}, $DB_TITLE{$_}, $DB_ICON{$_}, $DB_REMOTEHOST{$_}, $DB_NAME{$_}, $DB_EMAIL{$_}, $DB_URL{$_}, $DB_FMAIL{$_} ));
	    print( DBTMP "$dbLine\n" ) || &Fatal( 13, $TmpFile );
	}
    }

    # close Files.
    close DB;
    close DBTMP || &Fatal( 13, $TmpFile );

    # DBを更新する
    rename( $TmpFile, $File ) || &Fatal( 14, "$TmpFile -&gt; $File" );
}


###
## MakeArticleFile - 記事本文DBへの追加
#
# - SYNOPSIS
#	MakeArticleFile($TextType, $Article, $Id, $Board);
#
# - ARGS
#	$TextType	文書タイプ
#	$Article	本文
#	$Id		記事ID
#	$Board		掲示板ID
#
# - DESCRIPTION
#	記事本文DB(掲示板IDと同じ名前のディレクトリ)の中に，
#	IDと同じ名前のファイルとして，記事本文を保存する．
#
sub MakeArticleFile
{
    local( $TextType, $Article, $Id, $Board ) = @_;

    local( $File ) = &GetArticleFileName( $Id, $Board );

    open( TMP, ">$File" ) || &Fatal( 1, $File );
    printf( TMP "<!-- Kb-System-Id: %s/%s -->\n", $KB_VERSION, $KB_RELEASE)
	|| &Fatal( 13, $File );
    print( TMP "$Article\n" ) || &Fatal( 13, $File );
    close TMP || &Fatal( 13, $File );
}


###
## GetArticleBody - 記事本文DBの読み込み
#
# - SYNOPSIS
#	GetArticleBody($Id, $Board, *ArticleBody);
#
# - ARGS
#	$Id		記事ID
#	$BoardId	掲示板ID
#	*ArticleBody	本文各行を入れる配列変数へのリファレンス
#
# - DESCRIPTION
#	記事本文DB(掲示板IDと同じ名前のディレクトリ)の中の，
#	IDと同じ名前のファイルを読み出す．
#
sub GetArticleBody
{
    local( $Id, $Board, *ArticleBody ) = @_;

    local( $QuoteFile ) = &GetArticleFileName( $Id, $Board );
    open( TMP, "<$QuoteFile" ) || &Fatal( 1, $QuoteFile );
    while ( <TMP> )
    {
	push( @ArticleBody, $_ );
    }
    close TMP;
}


###
## GetArticleId - 記事番号DBの読み込み
#
# - SYNOPSIS
#	GetArticleId($Board);
#
# - ARGS
#	$Board		掲示板ID
#
# - DESCRIPTION
#	従来の最新記事IDを読み出す．
#
# - RETURN
#	最新記事のID
#
sub GetArticleId
{
    local( $Board, *id, *artKey ) = @_;

    local( $ArticleNumFile ) = &GetPath( $Board, $ARTICLE_NUM_FILE_NAME );
    open( AID, "<$ArticleNumFile" ) || &Fatal( 1, $ArticleNumFile );
    chop( $id = <AID> );
    chop( $artKey = <AID> );
    close AID;
}


###
## WriteArticleId - 記事番号DBの更新
#
# - SYNOPSIS
#	WriteArticleId($Id, $Board, $artKey);
#
# - ARGS
#	$Id		新規に書き込む記事番号
#	$Board		掲示板ID
#	$artKey		多重書き込み防止用キー
#
# - DESCRIPTION
#	記事番号DBの更新
#
sub WriteArticleId
{
    local( $Id, $Board, $artKey ) = @_;

    local( $File, $TmpFile, $OldArticleId );
    
    # 数字のくせに古い数値より若い! (数字じゃなきゃOK)
    $OldArticleId = &GetNewArticleId( $Board );
    &Fatal( 10, '' ) if (( $Id =~ /^\d+$/ ) && ( $Id < $OldArticleId ));

    $File = &GetPath( $Board, $ARTICLE_NUM_FILE_NAME );
    $TmpFile = &GetPath( $Board, "$ARTICLE_NUM_FILE_NAME.$TMPFILE_SUFFIX$$" );
    open( AID, ">$TmpFile" ) || &Fatal( 1, $TmpFile );
    print( AID "$Id\n" ) || &Fatal( 13, $TmpFile );
    print( AID "$artKey\n" ) || &Fatal( 13, $TmpFile );
    close AID || &Fatal( 13, $TmpFile );

    rename( $TmpFile, $File ) || &Fatal( 14, "$TmpFile -&gt; $File" );
}


###
## GetArriveMailTo - 掲示板別新規メイル送信先DBの全読み込み
#
# - SYNOPSIS
#	GetArriveMailTo($CommentFlag, $Board, *ArriveMail);
#
# - ARGS
#	$CommentFlag	コメント行を含むか否か(0: 含まない, 1: 含む)
#	$Board		掲示板ID
#	*ArriveMail	送信先のメイルアドレスのリストのリファレンス
#
# - DESCRIPTION
#	掲示板別新規メイル送信先DBを，読み込む．
#	メイルアドレスが正しいか否か等のチェックは，一切行なわない．
#
sub GetArriveMailTo
{
    local($CommentFlag, $Board, *ArriveMail) = @_;
    local($ArriveMailFile);

    $ArriveMailFile = &GetPath( $Board, $ARRIVEMAIL_FILE_NAME );
    # ファイルがなきゃ空のまま
    open( ARMAIL, "<$ArriveMailFile" ) || return;
    while ( <ARMAIL> )
    {
	next if ((! $CommentFlag) && (/^\#/o || /^$/o));
	chop;
	push(@ArriveMail, $_);
    }
    close ARMAIL;
}


###
## UpdateArriveMailDb - 掲示板別新規メイル送信先DBの全更新
#
# - SYNOPSIS
#	UpdateArriveMailDb($Board, *ArriveMail);
#
# - ARGS
#	$Board		掲示板ID
#	*ArriveMail	送信先のメイルアドレスのリストのリファレンス
#			(コメント，空行も含まれる)
#
# - DESCRIPTION
#	掲示板別新規メイル送信先DBを，新たな送信先リストで一新する．
#	メイルアドレスが正しいか否か等のチェックは，一切行なわない．
#
sub UpdateArriveMailDb
{
    local( $Board, *ArriveMail ) = @_;

    local( $File ) = &GetPath( $Board, $ARRIVEMAIL_FILE_NAME );
    local( $TmpFile ) = &GetPath( $Board, $ARRIVEMAIL_FILE_NAME );
    open( DBTMP, ">$TmpFile" ) || &Fatal( 1, $TmpFile );
    local( $line );
    foreach ( @ArriveMail )
    {
	( $line = $_ ) =~ s/\s*$//o;
	print( DBTMP "$line\n" ) || &Fatal( 13, $TmpFile );
    }
    close DBTMP || &Fatal( 13, $TmpFile );
    rename( $TmpFile, $File ) || &Fatal( 14, "$TmpFile -&gt; $File" );
}


###
## GetHeaderDb - 掲示板別ヘッダDBの全読み込み
#
# - SYNOPSIS
#	GetHeaderDb( $board, *header );
#
# - ARGS
#	$board		掲示板ID
#	*header		ヘッダ文字列
#
sub GetHeaderDb
{
    local( $board, *header ) = @_;

    local( $file ) = &GetPath( $board, $HEADER_FILE_NAME );
    # ファイルがなきゃ空のまま
    open( DB, "<$file" ) || return;
    while ( <DB> )
    {
	$header .= $_;
    }
    close DB;
}


###
## UpdateHeaderDb - 掲示板別ヘッダDBの全更新
#
# - SYNOPSIS
#	UpdateHeaderDb( $board, *header );
#
# - ARGS
#	$board		掲示板ID
#	*header		ヘッダ文字列
#
sub UpdateHeaderDb
{
    local( $board, *header ) = @_;

    local( $file ) = &GetPath( $board, $HEADER_FILE_NAME );
    local( $tmpFile ) = &GetPath( $board, $HEADER_FILE_NAME );
    open( DBTMP, ">$tmpFile" ) || &Fatal( 1, $tmpFile );
    print( DBTMP $header ) || &Fatal( 13, $tmpFile );
    close DBTMP || &Fatal( 13, $tmpFile );
    rename( $tmpFile, $file ) || &Fatal( 14, "$tmpFile -&gt; $file" );
}


###
## AddBoardDb - 掲示板DBへの追加
#
# - SYNOPSIS
#	AddBoardDb( $name, $intro, $conf, *arriveMail, *header );
#
# - ARGS
#	$name		掲示板名
#	$intro		紹介文
#	$conf		掲示板固有設定ファイルを利用するか否か(0/1)
#	*arriveMail	自動送信メイルのメイル先リスト
#	*header		ヘッダ文字列
#
# - DESCRIPTION
#	掲示板DBに掲示板を追加する．
#
# - RETURN
#	作成した掲示板のID
#
sub AddBoardDb
{
    local( $name, $intro, $conf, *arriveMail, *header ) = @_;

    # 掲示板ディレクトリの作成
    mkdir( $name, 0777 ) || &Fatal( 1, $name );

    local( $src, $dest );

    # 記事DBの作成（コピー）
    $src = &GetPath( $BOARDSRC_DIR, $DB_FILE_NAME );
    $dest = &GetPath( $name, $DB_FILE_NAME );
    &CopyDb( $src, $dest ) || &Fatal( 20, "$src -&gt; $dest" );

    # 記事数DBの作成（コピー）
    $src = &GetPath( $BOARDSRC_DIR, $ARTICLE_NUM_FILE_NAME );
    $dest = &GetPath( $name, $ARTICLE_NUM_FILE_NAME );
    &CopyDb( $src, $dest ) || &Fatal( 20, "$src -&gt; $dest" );

    # 自動送信メイルDBの作成
    &UpdateArriveMailDb( $name, *arriveMail );

    # ヘッダファイルの作成
    &UpdateHeaderDb( $name, *header );

    # 最後に，掲示板DBを更新する
    local( $file ) = &GetPath( $SYS_DIR, $BOARD_FILE );
    local( $tmpFile ) = &GetPath( $SYS_DIR, "$BOARD_FILE.$TMPFILE_SUFFIX$$" );
    local( $dbLine );
    open( DBTMP, ">$tmpFile" ) || &Fatal( 1, $tmpFile );
    open( DB, "<$file" ) || &Fatal( 1, $file );

    local( $dName, $dIntro, $dConf );
    while ( <DB> )
    {
	if ( /^\#/o || /^$/o )
	{
	    print( DBTMP "$_" ) || &Fatal( 13, $tmpFile );
	    next;
	}
	chop;

	( $dName, $dIntro, $dConf ) = split( /\t/, $_, 3 );
	&Fatal( 51, $name ) if ( $name eq $dName );

	&GenTSV( *dbLine, ( $dName, $dIntro, $dConf ));
	print( DBTMP "$dbLine\n" ) || &Fatal( 13, $tmpFile );
    }

    # 新しい記事のデータを書き加える．
    &GenTSV( *dbLine, ( $name, $intro, $conf ));
    print( DBTMP "$dbLine\n" ) || &Fatal( 13, $tmpFile );

    # close Files.
    close DB;
    close DBTMP || &Fatal( 13, $tmpFile );

    rename( $tmpFile, $file ) || &Fatal( 14, "$tmpFile -&gt; $file" );
}


###
## UpdateBoardDb - 掲示板DBの更新
#
# - SYNOPSIS
#	UpdateBoardDb( $board, $valid, $intro, $conf, *arriveMail, *header );
#
# - ARGS
#	$board		掲示板ID
#	$valid		この掲示板を利用するか否か
#	$intro		掲示板名
#	$conf		設定ファイルを読むか否か
#	*arriveMail	自動送信メイルのメイル先リスト
#	*header		ヘッダ文字列
#
# - DESCRIPTION
#	掲示板DBを更新する．
#
sub UpdateBoardDb
{
    local( $name, $valid, $intro, $conf, *arriveMail, *header ) = @_;

    local( $file ) = &GetPath( $SYS_DIR, $BOARD_FILE );
    local( $tmpFile ) = &GetPath( $SYS_DIR, "$BOARD_FILE.$TMPFILE_SUFFIX$$" );
    open( DBTMP, ">$tmpFile" ) || &Fatal( 1, $tmpFile );
    open( DB, "<$file" ) || &Fatal( 1, $file );

    local( $dbLine, $dName, $dIntro, $dConf );
    while ( <DB> ) {

	if ( /^\#/o || /^$/o )
	{
	    print( DBTMP "$_" ) || &Fatal( 13, $tmpFile );
	    next;
	}
	chop;

	( $dName, $dIntro, $dConf ) = split( /\t/, $_, 3 );
	if ( $name eq $dName )
	{
	    $dName = '#' . $dName unless $valid;
	    $dIntro = $intro;
	    $dConf = $conf;
	}

	# DBに書き加える
	&GenTSV( *dbLine, ( $dName, $dIntro, $dConf ));
	print( DBTMP "$dbLine\n" ) || &Fatal( 13, $tmpFile );
    }

    # close Files.
    close DB;
    close DBTMP || &Fatal( 13, $tmpFile );

    # DBを更新する
    rename( $tmpFile, $file ) || &Fatal( 14, "$tmpFile -&gt; $file" );

    # 自動送信メイルDBも更新する．
    &UpdateArriveMailDb( $BOARD, *arriveMail );

    # ヘッダファイルも更新する．
    &UpdateHeaderDb( $name, *header );
}


###
## GetAllBoardInfo - 掲示板DBの全読み込み
#
# - SYNOPSIS
#	GetAllBoardInfo( *board, *boardName, *boardInfo );
#
# - ARGS
#	*board		掲示板IDの配列のリファレンス
#	*boardName	掲示板ID-掲示板名の連想配列のリファレンス
#	*boardInfo	掲示板ID-掲示板情報の連想配列のリファレンス
#
# - DESCRIPTION
#	掲示板DBから，掲示板情報を取ってくる．
#
sub GetAllBoardInfo
{
    local( *board, *boardName, *boardInfo ) = @_;

    local( $bId, $bName, $bInfo );
    local( $dbFile ) = &GetPath( $SYS_DIR, $BOARD_FILE );
    open( DB, "<$dbFile" ) || &Fatal( 1, $dbFile );
    while ( <DB> )
    {
	next if ( /^\#/o || /^$/o );
	chop;
	( $bId, $bName, $bInfo ) = split( /\t/, $_, 4 );
	push( @board, $bId );
	$boardName{ $bId } = $bName;
	$boardInfo{ $bId } = $bInfo;
    }
    close DB;
}


###
## GetBoardInfo - 掲示板DBの読み込み
#
# - SYNOPSIS
#	GetBoardInfo( $board );
#
# - ARGS
#	$board		掲示板ID
#
# - DESCRIPTION
#	掲示板DBから，掲示板情報を取ってくる．
#
# - RETURN
#	掲示板名，固有設定の有無，のリスト
#
sub GetBoardInfo
{
    local( $board ) = @_;

    local( $dBoard, $dBoardName, $dBoardConf );

    local( $dbFile ) = &GetPath( $SYS_DIR, $BOARD_FILE );
    open( DB, "<$dbFile" ) || &Fatal( 1, $dbFile );
    while ( <DB> )
    {
	next if ( /^\#/o || /^$/o );
	chop;
	( $dBoard, $dBoardName, $dBoardConf ) = split( /\t/, $_, 4 );
	if ( $board eq $dBoard )
	{
	    close DB;
	    return( $dBoardName, $dBoardConf );
	}
    }
    close DB;

    &Fatal( 11, $board );
}


###
## CacheIconDb - アイコンDBの全読み込み
#
# - SYNOPSIS
#	CacheIconDb($board);
#
# - ARGS
#	$board		掲示板ID
#
# - DESCRIPTION
#	アイコンDBを読み込んで連想配列に放り込む．
#	大域変数，@ICON_TITLE，%ICON_FILE，%ICON_HELPを破壊する．
#
sub CacheIconDb
{
    local( $board ) = @_;
    local( $fileName, $title, $help, $type );

    @ICON_TITLE = %ICON_FILE = %ICON_HELP = %ICON_TYPE = ();
    open( ICON, &GetIconPath( "$board.$ICONDEF_POSTFIX" ))
	|| ( open( ICON, &GetIconPath( "$DEFAULT_ICONDEF" ))
	    || &Fatal( 1, &GetIconPath( "$DEFAULT_ICONDEF" )));
    while ( <ICON> )
    {
	next if ( /^\#/o || /^$/o );
	chop;
	( $fileName, $title, $help, $type ) = split( /\t/, $_, 4 );

	push( @ICON_TITLE, $title );
	$ICON_FILE{$title} = $fileName;
	$ICON_HELP{$title} = $help;
	$ICON_TYPE{$title} = $type || 'article';
    }
    close ICON;
}


###
## GetArticleFileName - 記事本文DBファイルのパス名の取得
#
# - SYNOPSIS
#	GetArticleFileName($Id, $Board);
#
# - ARGS
#	$Id		記事ID
#	$Board		掲示板ID
#
# - DESCRIPTION
#	掲示板IDと記事IDから，記事DB中の，記事ファイルのパス名を作り出す．
#	大域変数$MACPERLを参照し，MacPerlに対応．
#
# - RETURN
#	パスを表す文字列
#
sub GetArticleFileName
{
    local( $Id, $Board ) = @_;

    # Boardが空ならBoardディレクトリ内から相対，
    # 空でなければシステムから相対
    if ( $MACPERL )
    {
	$Board? ":$Board:$Id" : "$Id";
    }
    else
    {
	$Board? "$Board/$Id" : "$Id";
    }
}


###
## GetPath - DBファイルのパス名の取得
#
# - SYNOPSIS
#	GetPath($DbDir, $File);
#
# - ARGS
#	$DbDir		DBディレクトリ(掲示板ID, etc.)
#	$File		ファイル名
#
# - DESCRIPTION
#	DBディレクトリ名とファイル名から，DBファイルのパス名を作り出す．
#	大域変数$MACPERLを参照し，MacPerlに対応．
#
# - RETURN
#	パスを表す文字列
#
sub GetPath
{
    local( $DbDir, $File ) = @_;

    if ( $MACPERL )
    {
	":$DbDir:$File";
    }
    else
    {
	"$DbDir/$File";
    }
}


###
## GetIconPath - アイコンgifDBファイルのパス名の取得
#
# - SYNOPSIS
#	GetIconPath($File);
#
# - ARGS
#	$File		アイコンgifファイル名
#
# - DESCRIPTION
#	アイコンgifファイルのパス名を作り出す．
#	大域変数$MACPERLを参照し，MacPerlに対応．
#
# - RETURN
#	パスを表す文字列
#
sub GetIconPath
{
    local( $File ) = @_;

    if ( $MACPERL )
    {
	":$ICON_DIR:$File";
    }
    else
    {
	"$ICON_DIR/$File";
    }
}


###
## GetStyleSheetURL - スタイルシートファイルのURLの取得
#
# - SYNOPSIS
#	&GetStyleSheetURL( $name );
#
# - ARGS
#	$name		スタイルシートファイルの名前
#
# - DESCRIPTION
#	スタイルシートファイルのURLを作り出す．
#
# - RETURN
#	URLを表す文字列
#
sub GetStyleSheetURL
{
    local( $name ) = @_;
    $KB_RESOURCE_URL? "$KB_RESOURCE_URL$RESOURCE_STYLE/$name" : "$RESOURCE_STYLE/$name";
}


###
## GetIconURL - アイコンgifのURLの取得
#
# - SYNOPSIS
#	GetIconURL( $file );
#
# - ARGS
#	$file		アイコンgifファイル名
#
# - DESCRIPTION
#	アイコンgifファイルのURL名を作り出す．
#
# - RETURN
#	URLを表す文字列
#
sub GetIconURL
{
    local( $file ) = @_;
    $KB_RESOURCE_URL? "$KB_RESOURCE_URL$RESOURCE_ICON/$file" : "$RESOURCE_ICON/$file";
}


###
## GetIconUrlFromTitle - アイコンgifのURLの取得
#
# - SYNOPSIS
#	GetIconUrlFromTitle( $icon );
#
# - ARGS
#	$icon		アイコンID
#
# - DESCRIPTION
#	アイコンIDから，そのアイコンに対応するgifファイルのURLを取得．
#	新着アイコンも記事アイコン扱い．
#
# - RETURN
#	URLを表す文字列
#
sub GetIconUrlFromTitle
{
    local( $icon ) = @_;
    return $ICON_NEW if ( $icon eq $H_NEWARTICLE );

    # check
    return '' unless $ICON_FILE{ $icon };

    # return
    &GetIconURL( $ICON_FILE{ $icon } );
}


###
## SupersedeDbFile - 訂正記事の記事DBへの書き込み
#
# - SYNOPSIS
#	SupersedeDbFile($Board, $Id, $InputDate, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail);
#
# - ARGS
#	$Board		訂正する記事が含まれる掲示板のID
#	$Id		訂正する記事のID
#	$InputDate	訂正時間(UTC)
#	$Subject	訂正記事Subject
#	$Icon		訂正記事アイコン
#	$RemoteHost	訂正記事書き込みホスト名
#	$Name		訂正記事書き込みユーザ名
#	$Email		訂正記事書き込みユーザメイルアドレス
#	$Url		訂正記事書き込みユーザURL
#	$Fmail		リプライ時にメイルを送信するか否か
#
# - DESCRIPTION
#	訂正記事をDBファイルに書き込み，agingした記事のIDを返す．
#
# - RETURN
#	agingした記事のID．
#
sub SupersedeDbFile
{
    local( $Board, $Id, $InputDate, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail ) = @_;

    local( $SupersedeId, $dId, $dFid, $dAids, $dInputDate, $dSubject, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail );
    
    # initial versionは1で，1ずつ増えていく．1，2，…9，10，11，…
    # later versionはDB中で必ず，younger versionよりも下に出現する．
    # すなわち10_2，10，10_1は，10_1，10_2，10の順に並ぶものとする．
    $SupersedeId = 1;

    local( $dbLine );
    local( $File ) = &GetPath( $Board, $DB_FILE_NAME );
    local( $TmpFile ) = &GetPath( $Board, "$DB_FILE_NAME.$TMPFILE_SUFFIX$$" );
    open( DBTMP, ">$TmpFile" ) || &Fatal( 1, $TmpFile );
    open( DB, "<$File" ) || &Fatal( 1, $File );
    while ( <DB> )
    {
	if ( /^\#/o || /^$/o )
	{
	    print( DBTMP "$_" ) || &Fatal( 13, $TmpFile );
	    next;
	}

	chop;

	( $dId, $dFid, $dAids, $dInputDate, $dSubject, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail ) = split( /\t/, $_ );

	# later versionが見つかったら，versionを先読みしておく．
	if ( "$dId" eq ( sprintf( "#-%s_%s", $Id, $SupersedeId )))
	{
	    $SupersedeId++;
	}

	# 訂正記事の最新版が見つかったら，
	if ( $dId eq $Id )
	{
	    # agingしてしまう
	    &GenTSV( *dbLine, ( sprintf( "-%s_%s", $dId, $SupersedeId ), $dFid, $dAids, $dInputDate, $dSubject, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail ));
	    print( DBTMP "#$dbLine\n" ) || &Fatal( 13, $TmpFile );

	    # 続いて新しい記事を書き加える
	    &GenTSV( *dbLine, ( $Id, $dFid, $dAids, $InputDate, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail ));
	    print( DBTMP "$dbLine\n" ) || &Fatal( 13, $TmpFile );
	}
	else
	{
	    # DBに書き加える
	    print( DBTMP "$_\n" ) || &Fatal( 13, $TmpFile );
	}
    }

    # close Files.
    close DB;
    close DBTMP || &Fatal( 13, $TmpFile );

    # DBを更新する
    rename( $TmpFile, $File ) || &Fatal( 14, "$TmpFile -&gt; $File" );

    # 返す
    $SupersedeId;
}
