#!/usr/local/bin/perl
#!/usr/local/bin/perl5.00503-debug -d:DProf
#!/usr/local/bin/perl4.036


# このファイルの変更は最低2箇所，最大4箇所です（環境次第です）．
#
# 1. ↑の先頭行で，Perlのパスを指定します．「#!」に続けて指定してください．

# 2. kbディレクトリのフルパスを指定してください（URLではなく，パスです）．
#    !! KB/1.0R6.4以降，この設定は必須となりました !!
#
$KBDIR_PATH = '';
# $KBDIR_PATH = '/home/nahi/public_html';
# $KBDIR_PATH = 'd:\inetpub\wwwroot\kb';	# WinNT/Win9xの場合
# $KBDIR_PATH = 'foo:bar:kb';			# Macの場合?

# 3. サーバが動いているマシンがWin95/Macの場合，
#    $PCを1に設定してください．そうでない場合，この設定は不要です．
#
$PC = 0;	# for UNIX / WinNT
# $PC = 1;	# for Win95 / Mac

# 4. サーバがCGIWRAPを利用している場合，以下のコメントを外し，
#    kbディレクトリのURLを指定してください（今度はパスではなく，URLです）．
#    そうでない人は，変更の必要はありません．コメントのままでOKです．
#
# $ENV{'PATH_INFO'} = '/~nahi/kb';


# 以下は書き換えの必要はありません．


######################################################################


# $Id: kb.cgi,v 5.52 1999-10-20 14:40:43 nakahiro Exp $

# KINOBOARDS: Kinoboards Is Network Opened BOARD System
# Copyright (C) 1995-99 NAKAMURA Hiroshi.
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
$KB_RELEASE = '7β1';		# release
$CHARSET = 'euc';		# 漢字コード変換は行なわない
$ADMIN = 'admin';		# デフォルト設定
$GUEST = 'guest';		# デフォルト設定

# ディレクトリ
$ICON_DIR = 'icons';				# アイコンディレクトリ
$UI_DIR = 'UI';					# UIディレクトリ
$LOG_DIR = 'log';				# ログディレクトリ
$BOARDSRC_DIR = 'board';			# 掲示板ソースディレクトリ

# ファイル
$BOARD_FILE = 'kinoboards';			# 掲示板DB
$CONF_FILE_NAME = 'kb.conf';			# 掲示板別configuratinファイル
$ARRIVEMAIL_FILE_NAME = 'kb.mail';		# 掲示板別新規メイル送信先DB
$HEADER_FILE_NAME = 'kb.board';			# タイトルリストヘッダDB
$DB_FILE_NAME = 'kb.db';			# 記事DB
$ARTICLE_NUM_FILE_NAME = 'kb.aid';		# 記事番号DB
$CSS_FILE = 'kbStyle.css';			# スタイルシートファイル
$USER_FILE = 'kb.user';				# ユーザ用DB
$DEFAULT_ICONDEF = 'all.idef';			# アイコンDB
$LOCK_FILE = 'kb.lock';				# ロックファイル
$LOCK_FILE_B = '';				# 掲示板別ロックファイル
$ACCESS_LOG = 'access_log';			# アクセスログファイル
$ERROR_LOG = 'error_log';			# エラーログファイル
# Suffix
$TMPFILE_SUFFIX = 'tmp';			# DBテンポラリファイルのSuffix
$ICONDEF_POSTFIX = 'idef';			# アイコンDBファイルのSuffix

# CGIと同一ディレクトリにあるヘッダファイルの読み込み
require( $HEADER_FILE ) if ( -s "$HEADER_FILE" );

# メインのヘッダファイルの読み込み
if ( !$KBDIR_PATH || !chdir( $KBDIR_PATH ))
{
    print "Content-Type: text/plain; charset=EUC-JP\n\n";
    print "エラー．管理者様へ:\n";
    print "$0の先頭部分に置かれている\$KBDIR_PATHが，\n";
    print "正しく設定されていません\n";
    print "（R6.4以降，この変数の設定が必須となりました）．\n";
    print "設定してから再度試してみてください．";
    exit 0;
}
# chdir先のkb.phを読む．ただし上でrequire済みの場合は読まない（Perlの言語仕様）
require( $HEADER_FILE ) if ( -s "$HEADER_FILE" );

# インクルードファイルの読み込み
require( 'cgi.pl' );
require( 'kinologue.pl' );
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

if ( $cgi'PATH_INFO )
{
    $BASE_URL = "http://$cgi'SERVER_NAME$SERVER_PORT_STRING$cgi'PATH_INFO/";
}
else
{
    local( $cgidir ) = substr( $cgi'SCRIPT_NAME, 0, rindex( $cgi'SCRIPT_NAME,
	'/' ));
    $BASE_URL = "http://$cgi'SERVER_NAME$SERVER_PORT_STRING$cgidir/";
}

$SCRIPT_URL = "http://$cgi'SERVER_NAME$SERVER_PORT_STRING$PROGRAM";
$MACPERL = ( $^O eq 'MacOS' );  # isMacPerl?
$PROGNAME = "KINOBOARDS/$KB_VERSION R$KB_RELEASE";
$ENV{'TZ'} = $TIME_ZONE if $TIME_ZONE;

# 許可タグのベース
$HTML_TAGS_COREATTRS = 'ID/CLASS/STYLE/TITLE';
$HTML_TAGS_I18NATTRS = 'LANG/DIR';
$HTML_TAGS_GENATTRS = "$HTML_TAGS_COREATTRS/$HTML_TAGS_I18NATTRS";

# アイコンファイル相対URL
$ICON_BLIST = "$ICON_DIR/blist.gif";		# 掲示板一覧へ
$ICON_TLIST = "$ICON_DIR/tlist.gif";		# タイトル一覧へ
$ICON_PREV = "$ICON_DIR/prev.gif";		# 前の記事へ
$ICON_NEXT = "$ICON_DIR/next.gif";		# 次の記事へ
$ICON_WRITENEW = "$ICON_DIR/writenew.gif";	# 新規書き込み
$ICON_FOLLOW = "$ICON_DIR/follow.gif";		# リプライ
$ICON_QUOTE = "$ICON_DIR/quote.gif";		# 引用してリプライ
$ICON_THREAD = "$ICON_DIR/thread.gif";		# まとめ読み
$ICON_HELP = "$ICON_DIR/help.gif";		# ヘルプ
$ICON_DELETE = "$ICON_DIR/delete.gif";		# 削除
$ICON_SUPERSEDE = "$ICON_DIR/supersede.gif";	# 訂正
$ICON_NEW = "$ICON_DIR/listnew.gif";		# 新着

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

# 改行タグ，水平線タグ: XHTMLでは<br />や<hr />になります．
$HTML_BR = "<br>\n";
$HTML_HR = "<hr>\n";

# ローカルカウンタ・フラグ
$gLinkNum = 0;
$gTabIndex = 0;
$gBoardDbCached = 0;
$gIconDbCached = '';


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
	    $modTime = &GetModifiedTime( $DB_FILE_NAME, $cgi'TAGS{'b'} );
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
	$c = $BOARD? 'v' : 'bl';
    }

    if ( $BOARD )
    {
	local( $boardConfFileP );
	( $BOARDNAME, $boardConfFileP ) = &GetBoardInfo( $BOARD );
	$LOCK_FILE_B = $LOCK_FILE . ".$BOARD";

	# 掲示板固有セッティングを読み込む
	if ( $boardConfFileP )
	{
	    local( $boardConfFile ) = &GetPath( $BOARD, $CONF_FILE_NAME );
	    require( $boardConfFile ) if ( -s "$boardConfFile" );
	}
    }

    # 全てのrequireが終わったあと．．．

    # 認証情報の初期化
    $cgiauth'GUEST = $GUEST;
    $cgiauth'ADMIN = $ADMIN;
    $USER_AUTH_FILE = &GetPath( $AUTH_DIR, $USER_FILE );

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
	( $err, $UNAME, $PASSWD, @userInfo ) = &cgiauth'CheckUser(
	    $USER_AUTH_FILE );
	    
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
	    # 日付順にソート
	    &UISortTitle();
	    last;
	}
	elsif ( $c eq 'l' )
	{
	    # 新しい記事を日付順に表示
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
	if  ( $c eq 'ct' )
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
    # ユーザ情報をクリア
    if ( $SYS_AUTH == 1 )
    {
	$UNAME = $cgiauth'F_COOKIE_RESET;
    }
    else
    {
	$UNAME = '';
    }
    &htmlGen( 'Login.html' );
}

sub hgLoginForm
{
    &Fatal( 18, "$_[0]/LoginForm" ) if ( $_[0] ne 'Login.html' );

    local( %tags, $msg );
    $msg = &TagLabel( $H_FROM, 'kinoU', 'N' ) . ': ' . &TagInputText( 'text',
	'kinoU', '', $NAME_LENGTH ) . $HTML_BR;
    $msg .= &TagLabel( $H_PASSWD, 'kinoP', 'P' ) . ': ' . &TagInputText(
	'password', 'kinoP', '', $PASSWD_LENGTH ) . $HTML_BR;
    if ( $SYS_AUTH_DEFAULT == 1 )
    {
	$msg .= &TagInputRadio( 'kinoA_url', 'kinoA', '3', 1 ) . ":\n" .
	    &TagLabel( 'クッキー(HTTP-Cookies)を使わずに認証する', 'kinoA_url',
	    'U' ) . $HTML_BR;
	$msg .= &TagInputRadio( 'kinoA_cookies', 'kinoA', '1', 0 ) . "\n" .
	    &TagLabel( 'クッキーを使ってこのブラウザに情報を覚えさせる',
	   'kinoA_cookies', 'C' ) . $HTML_BR;
    }

    %tags = ( 'c', 'bl', 'kinoT', 'plain' );
    &DumpForm( *tags, '実行', 'リセット', *msg, 1 );
}


###
## 管理者パスワードの設定画面
#
sub UIAdminConfig
{
    &htmlGen( 'AdminConfig.html' );
}

sub hgAdminConfigForm
{
    &Fatal( 18, "$_[0]/AdminConfigForm" ) if ( $_[0] ne 'AdminConfig.html' );

    local( %tags, $msg );
    $msg = &TagLabel( $H_PASSWD, 'confP', 'P' ) . ': ' . &TagInputText(
	'password', 'confP', '', $PASSWD_LENGTH ) . $HTML_BR;
    $msg .= &TagLabel( $H_PASSWD, 'confP2', 'C' ) . ': ' . &TagInputText(
	'password', 'confP2', '', $PASSWD_LENGTH ) .
	'（念のため，もう一度お願いします）' . $HTML_BR;
    %tags = ( 'c', 'acx' );
    &DumpForm( *tags, '設定', 'リセット', *msg, 1 );
}


###
## 管理者パスワード設定の実施
#
sub UIAdminConfigExec
{
    local( $p1 ) = $cgi'TAGS{'confP'};
    local( $p2 ) = $cgi'TAGS{'confP2'};

    # adminのみ
    &Fatal( 44, '' ) unless ( &IsUser( $ADMIN ));

    # lock system.
    &LockAll();

    if ( !$p2 || ( $p1 ne $p2 ))
    {
	&Fatal( 42, $H_PASSWD );
    }
    
    if ( !&cgiauth'SetUserPasswd( $USER_AUTH_FILE , $ADMIN, $p1 ))
    {
	&Fatal( 41, $ADMIN );
    }

    # unlock system
    &UnlockAll();

    # ユーザ情報をクリア
    &UILogin();
}


###
## ユーザ登録画面
#
sub UIUserEntry
{
    # ユーザ情報をクリア
    $UNAME = $cgiauth'F_COOKIE_RESET if ( $SYS_AUTH == 1 );
    &htmlGen( 'UserEntry.html' );
}

sub hgUserEntryForm
{
    &Fatal( 18, "$_[0]/UserEntryForm" ) if ( $_[0] ne 'UserEntry.html' );

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
	    
    # lock system
    &LockAll();

    # 新規登録する
    local( $res ) = &cgiauth'AddUser( $USER_AUTH_FILE, $user, $p1, $mail,
	$url );

    # unlock system
    &UnlockAll();

    if ( $res == 1 )
    {
	&Fatal( 6, $user );
    }
    elsif ( $res == 2 )
    {
	&Fatal( 998, 'Must not reach here(UserEntryExec).' );
    }

    # ログイン画面へ
    &UILogin();
}


###
## ユーザ設定変更
#
sub UIUserConfig
{
    &htmlGen( 'UserConfig.html' );
}

sub hgUserConfigForm
{
    &Fatal( 18, "$_[0]/UserConfigForm" ) if ( $_[0] ne 'UserConfig.html' );

    if ( $POLICY & 8 )
    {
	local( %tags, $msg );
	$msg = &TagLabel( "変更する$H_USERの$H_FROM", 'confUser', 'N' ) .
	    ': ' . &TagInputText( 'text', 'confUser', '', $NAME_LENGTH ) .
	    "（管理者は全$H_USERの設定を変更できます）" . $HTML_BR . $HTML_BR;
	$msg .= &TagLabel( $H_MAIL, 'confMail', 'M' ) . ': ' . &TagInputText(
	    'text', 'confMail', '', $MAIL_LENGTH ) . $HTML_BR;
	$msg .= &TagLabel( $H_URL, 'confUrl', 'U' ) . ': ' . &TagInputText(
	    'text', 'confUrl', 'http://', $URL_LENGTH ) . $HTML_BR . $HTML_BR;
	$msg .= &TagLabel( $H_PASSWD, 'confP', 'P' ) . ': ' . &TagInputText(
	    'password', 'confP', '', $PASSWD_LENGTH ) . $HTML_BR;
	$msg .= &TagLabel( $H_PASSWD, 'confP2', 'C' ) . ': ' . &TagInputText(
	    'password', 'confP2', '', $PASSWD_LENGTH ) .
	    '（念のため，もう一度お願いします）' . $HTML_BR;
	%tags = ( 'c', 'ucx' );
	&DumpForm( *tags, '設定', 'リセット', *msg );
    }
    else
    {
	$UURL = $UURL || 'http://';

	local( %tags, $msg );
	$msg = &TagLabel( $H_MAIL, 'confMail', 'M' ) . ': ' . &TagInputText(
	    'text', 'confMail', $UMAIL, $MAIL_LENGTH ) . $HTML_BR;
	$msg .= &TagLabel( $H_URL, 'confUrl', 'U' ) . ': ' . &TagInputText(
	    'text', 'confUrl', $UURL, $URL_LENGTH ) . $HTML_BR . $HTML_BR;
	$msg .= &TagLabel( $H_PASSWD, 'confP', 'P' ) . ': ' . &TagInputText(
	    'password', 'confP', '', $PASSWD_LENGTH ) . $HTML_BR;
	$msg .= &TagLabel( $H_PASSWD, 'confP2', 'C' ) . ': ' . &TagInputText(
	    'password', 'confP2', '', $PASSWD_LENGTH ) .
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
    local( $p1 ) = $cgi'TAGS{'confP'};
    local( $p2 ) = $cgi'TAGS{'confP2'};
    local( $user ) = $cgi'TAGS{'confUser'};
    local( $mail ) = $cgi'TAGS{'confMail'};
    local( $url ) = $cgi'TAGS{'confUrl'};

    $user = $UNAME unless ( $POLICY & 8 );

    &CheckName( *user );
    &CheckEmail( *mail );
    &CheckURL( *url );
		
    # lock system
    &LockAll();

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

    # unlock system
    &UnlockAll();

    &UIBoardList();
}


###
## 掲示板登録画面
#
sub UIBoardEntry
{
    &htmlGen( 'BoardEntry.html' );
}

sub hgBoardEntryForm
{
    &Fatal( 18, "$_[0]/BoardEntryForm" ) if ( $_[0] ne 'BoardEntry.html' );

    local( %tags, $msg );
    $msg = &TagLabel( "$H_BOARD略称", 'name', 'B' ) . ': ' . &TagInputText(
	'text', 'name', '', $BOARDNAME_LENGTH ) . $HTML_BR;
    $msg .= &TagLabel( "$H_BOARD名称", 'intro', 'N' ) . ': ' . &TagInputText(
	'text', 'intro', '', $BOARDNAME_LENGTH ) . $HTML_BR . $HTML_BR;
    $msg .= &TagLabel( "$H_BOARDの自動メイル配信先", 'armail', 'M' ) .
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

    &LockAll();
    &AddBoardDb( $name, $intro, 0, *arriveMail, *header );
    &UnlockAll();

    &UIBoardList();
}


###
## 掲示板設定変更画面
#
sub UIBoardConfig
{
    &LockAll();
    &LockBoard();

    # 全掲示板の情報を取り出す
    @gArriveMail = ();
    &GetArriveMailTo(1, $BOARD, *gArriveMail); # 宛先とコメントを取り出す
    $gHeader = "";
    &GetHeaderDb( $BOARD, *gHeader ); # ヘッダ文字列を取り出す

    # unlock system
    &UnlockBoard();
    &UnlockAll();

    &htmlGen( 'BoardConfig.html' );
}

sub hgBoardConfigForm
{
    &Fatal( 18, "$_[0]/BoardConfigForm" ) if ( $_[0] ne 'BoardConfig.html' );

    local( %tags, $msg );
    $msg = &TagLabel( "「$BOARD」$H_BOARDを利用", 'valid', 'V' ) . ': ' .
	&TagInputCheck( 'valid', 1 ) . $HTML_BR . $HTML_BR;
    $msg .= &TagLabel( "「$BOARD」名称", 'intro', 'N' ) . ': ' .
	&TagInputText( 'text', 'intro', $BOARDNAME, $BOARDNAME_LENGTH ) .
	$HTML_BR . $HTML_BR;
    local( $all );
    foreach ( @gArriveMail ) { $all .= $_ . "\n"; }
    $msg .= &TagLabel( "「$BOARD」の自動メイル配信先", 'armail', 'M' ) .
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
    local( $valid ) = $cgi'TAGS{'valid'};
    local( $intro ) = $cgi'TAGS{'intro'};
    local( $armail ) = $cgi'TAGS{'armail'};
    local( $header ) = $cgi'TAGS{'article'};

    &CheckBoardName( *intro );
    &CheckBoardHeader( *header );
    &secureSubject( *intro );
    &secureArticle( *header, $H_TTLABEL[2] );
    local( @arriveMail ) = split( /\n/, $armail );

    &LockAll();
    &UpdateBoardDb( $BOARD, $valid, $intro, 0, *arriveMail, *header );
    &UnlockAll();

    &UIBoardList();
}


###
## 掲示板一覧
#
sub UIBoardList
{
    &htmlGen( 'BoardList.html' );
}


###
## メッセージ新規登録のエントリ
## リプライメッセージ登録のエントリ
## メッセージ訂正のエントリ
#
sub UIPostNewEntry
{
    if ( $SYS_NEWART_ADMINONLY && !( $POLICY & 8 ))
    {
	&Fatal( 99, $cgi'TAGS{'c'} );
    }

    local( $back ) = @_;

    $gId = '';			# 0ではダメ．そういうファイル名もあるかも．
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
    &htmlGen( 'PostNewEntry.html' );
}

sub UIPostReplyEntry
{
    local( $back, $quoteFlag ) = @_;

    &LockBoard();
    &DbCache( $BOARD ) if $BOARD;

    $gId = $cgi'TAGS{'id'};
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
	if ( $DefSubject eq '' )
	{
	    local( $tmp );
	    ( $tmp, $tmp, $tmp, $gDefSubject ) = &GetArticlesInfo( $gId );
	    &GetReplySubject( *gDefSubject );
	}
    }
    else
    {
	if ( $gDefSubject eq '' )
	{
	    local( $tmp );
	    ( $tmp, $tmp, $tmp, $gDefSubject ) = &GetArticlesInfo( $gId );
	    &GetReplySubject( *gDefSubject );
	}
	&QuoteOriginalArticle( $gId, *gDefArticle );
    }

    &UnlockBoard();

    $gEntryType = 'reply';		# リプライ
    &htmlGen( 'PostReplyEntry.html' );
}

sub UISupersedeEntry
{
    if ( !( $POLICY & 8 ) && ( $SYS_OVERWRITE == 0 ))
    {
	&Fatal( 99, $cgi'TAGS{'c'} );
    }

    local( $back ) = @_;

    &LockBoard();
    &DbCache( $BOARD ) if $BOARD;

    $gId = $cgi'TAGS{'id'};
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
	local( $tmp );
	( $tmp, $tmp, $tmp, $gDefSubject, $gDefIcon , $tmp, $gDefName,
	    $gDefEmail, $gDefUrl ) = &GetArticlesInfo( $gId );
	&QuoteOriginalArticleWithoutQMark( $gId, *gDefArticle );
    }

    &UnlockBoard();

    $gEntryType = 'supersede';		# 修正
    &htmlGen( 'SupersedeEntry.html' );
}

sub hgPostReplyEntryOrigArticle
{
    if ( $_[0] ne 'PostReplyEntry.html' )
    {
	&Fatal( 18, "$_[0]/PostReplyEntryOrigArticle" );
    }

    &DumpArtBody( $gId, 0, 1 );
}

sub hgSupersedeEntryOrigArticle
{
    if ( $_[0] ne 'SupersedeEntry.html' )
    {
	&Fatal( 18, "$_[0]/SupersedeEntryOrigArticle" );
    }

    &DumpArtBody( $gId, 0, 1 );
}


###
## メッセージ登録のプレビュー
## メッセージ訂正のプレビュー
#
sub UIPostPreview
{
    &UIPostPreviewMain( 'post' );
    &htmlGen( 'PostPreview.html' );
}

sub UISupersedePreview
{
    if ( !( $POLICY & 8 ) && ( $SYS_OVERWRITE == 0 ))
    {
	&Fatal( 99, $cgi'TAGS{'c'} );
    }

    &UIPostPreviewMain( 'supersede' );
    &htmlGen( 'SupersedePreview.html' );
}

sub UIPostPreviewMain
{
    local( $type ) = @_;

    # 入力された記事情報
    $gOrigId = $cgi'TAGS{'id'};
    $gSubject = $cgi'TAGS{'subject'};
    $gIcon = $cgi'TAGS{'icon'};
    $gArticle = $cgi'TAGS{'article'};
    $gTextType = $cgi'TAGS{'texttype'};

    &LockAll();
    &LockBoard();
    &DbCache( $BOARD ) if $BOARD;

    ( $gO2Id ) = &GetArticlesInfo( $gOrigId ) if ( $gOrigId ne '' );

    # ユーザ情報の取得
    if ( &IsUser( $ADMIN ))
    {
	$gName = $MAINT_NAME;
	$gEmail = $MAINT;
	$gUrl = $MAINT_URL;
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

    # 入力された記事情報のチェック
    &CheckArticle( $BOARD, *gName, *gEmail, *gUrl, *gSubject, *gIcon,
	*gArticle );

    &UnlockBoard();
    &UnlockAll();
}

sub hgPostPreviewForm
{
    &Fatal( 18, "$_[0]/PostPreviewForm" ) if ( $_[0] ne 'PostPreview.html' );

    require( 'mimer.pl' );

    local( $supersede ) = $_[1];

    local( %tags, $msg );
    $msg = &TagInputRadio( 'com_e', 'com', 'e', 0 ) . ":\n" . &TagLabel(
	'戻ってやりなおす', 'com_e', 'P' ) . $HTML_BR;
    $msg .= &TagInputRadio( 'com_x', 'com', 'x', 1 ) . "\n" . &TagLabel(
	'登録する', 'com_x', 'X' ) . $HTML_BR;
    %tags = ( 'corig', $cgi'TAGS{'corig'}, 'c', 'x', 'b', $BOARD,
	     'id', $gOrigId, 'texttype', $gTextType, 'name', $gName,
	     'mail', $gEmail, 'url', $gUrl, 'icon', $gIcon,
	     'subject', $gEncSubject, 'article', $gEncArticle,
	     'fmail', $cgi'TAGS{'fmail'}, 's', $supersede,
	     'op', $cgi'TAGS{'op'} );

    &DumpForm( *tags, '実行', '', *msg );
}

sub hgSupersedePreviewForm
{
    if ( $_[0] ne 'SupersedePreview.html' )
    {
	&Fatal( 18, "$_[0]/SupersedePreviewForm" );
    }

    &hgPostPreviewForm( 'PostPreview.html', 1 );
}

sub hgPostPreviewBody
{
    &Fatal( 18, "$_[0]/PostPreviewBody" ) if ( $_[0] ne 'PostPreview.html' );
    &DumpArtBody( '', 0, 1, $gOrigId, 0, $^T, $gSubject, $gIcon, 0, $gName,
	$gEmail, $gUrl, $gArticle );
}

sub hgSupersedePreviewBody
{
    if ( $_[0] ne 'SupersedePreview.html' )
    {
	&Fatal( 18, "$_[0]/SupersedePreviewBody" );
    }

    &hgPostPreviewBody( 'PostPreview.html' );
}

sub hgSupersedePreviewOrigArticle
{
    if ( $_[0] ne 'SupersedePreview.html' )
    {
	&Fatal( 18, "$_[0]/SupersedePreviewOrigArticle" );
    }

    &DumpArtBody( $gOrigId, 0, 1 );
}


###
## 記事の登録
## 記事の訂正
#
sub UIPostExec
{
    local( $previewFlag ) = @_;
    &UIPostExecMain( $previewFlag, 'post' );
    &htmlGen( 'PostExec.html' );
}

sub UISupersedeExec
{
    if ( !( $POLICY & 8 ) && ( $SYS_OVERWRITE == 0 ))
    {
	&Fatal( 99, $cgi'TAGS{'c'} );
    }

    local( $previewFlag ) = @_;
    &UIPostExecMain( $previewFlag, 'supersede' );
    &htmlGen( 'SupersedeExec.html' );
}

sub UIPostExecMain
{
    require( 'mimer.pl' );

    local( $previewFlag, $type ) = @_;

    # 入力された記事情報
    $gOrigId = $cgi'TAGS{'id'};
    local( $TextType ) = $cgi'TAGS{'texttype'};
    local( $Icon ) = $cgi'TAGS{'icon'};
    local( $Subject ) = $cgi'TAGS{'subject'};
    local( $Article ) = $cgi'TAGS{'article'};
    local( $Fmail ) = $cgi'TAGS{'fmail'};
    local( $op ) = $cgi'TAGS{'op'};

    &LockAll();
    &LockBoard();
    &DbCache( $BOARD ) if $BOARD;

    # ユーザ情報の取得
    local( $Name, $Email, $Url );
    if ( &IsUser( $ADMIN ))
    {
	$Name = $MAINT_NAME;
	$Email = $MAINT;
	$Url = $MAINT_URL;
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

    # ここ半日の間に生成されたフォームからしか投稿を許可しない．
    local( $base ) = ( -M &GetPath( $BOARD, $DB_FILE_NAME ));
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

    &secureSubject( *Subject );
    &secureArticle( *Article, $TextType );

    if ( $type eq 'post' )
    {
	# 記事の作成
	$gNewArtId = &MakeNewArticle( $BOARD, $gOrigId, $op, $TextType, $Name,
	    $Email, $Url, $Icon, $Subject, $Article, $Fmail, 1 );
    }
    elsif ( $type eq 'supersede' )
    {
	# 記事の訂正
	local( $tmp, $aids, $name );
	( $tmp, $aids, $tmp, $tmp, $tmp, $tmp, $name ) = &GetArticlesInfo(
	    $gOrigId );
	&Fatal( 44, '' ) if ( !&IsUser( $name ) && !( $POLICY & 8 ));
	&Fatal( 19, '' ) if ( $aids && ( $SYS_OVERWRITE == 1 ));

	$gNewArtId = &SupersedeArticle( $BOARD, $gOrigId, $TextType, $Name,
	    $Email, $Url, $Icon, $Subject, $Article, $Fmail );
    }
    else
    {
	&Fatal( 998, 'Must not reache here(UIPostExecMain).' );
    }

    &UnlockBoard();
    &UnlockAll();
}

sub hgPostExecJumpToNewArticle
{
    if ( $_[0] ne 'PostExec.html' )
    {
	&Fatal( 18, "$_[0]/PostExecJumpToNewArticle" );
    }

    &DumpButtonToArticle( $BOARD, $gNewArtId, "書き込んだ$H_MESGへ" );
}

sub hgSupersedeExecJumpToNewArticle
{
    if ( $_[0] ne 'SupersedeExec.html' )
    {
	&Fatal( 18, "$_[0]/SupersedeExecJumpToNewArticle" );
    }

    &DumpButtonToArticle( $BOARD, $gNewArtId, "訂正した$H_MESGへ" );
}

sub hgPostExecJumpToOrigArticle
{
    if ( $_[0] ne 'PostExec.html' )
    {
	&Fatal( 18, "$_[0]/PostExecJumpToOrigArticle" );
    }

    if ( $gOrigId ne '' )
    {
	&DumpButtonToArticle( $BOARD, $gOrigId, "$H_ORIGの$H_MESGへ" );
    }
}


###
## スレッド別タイトルおよび記事一覧
#
sub UIThreadArticle
{
    %gADDFLAG = ();
    @gIDLIST = ();

    &LockBoard();
    &DbCache( $BOARD ) if $BOARD;
    &UnlockBoard();

    # 表示する個数を取得
    $gNum = $cgi'TAGS{'num'};
    if ( defined( $cgi'TAGS{'id'} ))
    {
	$gOld = $#DB_ID - int( $cgi'TAGS{'id'} + $gNum/2 );
	$gOld = 0 if ( $gOld < 0 );
    }
    else
    {
	$gOld = $cgi'TAGS{'old'};
    }
    $gRev = $cgi'TAGS{'rev'};
    $gFold = $cgi'TAGS{'fold'} || 0;
    $gVRev = $gRev? 1-$SYS_BOTTOMTITLE : $SYS_BOTTOMTITLE;
    $gTo = $#DB_ID - $gOld;
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
	$gADDFLAG{$DB_ID[$IdNum]} = 2;
    }

    &htmlGen( 'ThreadArticle.html' );
}

sub hgThreadArticleTree
{
    if ( $_[0] ne 'ThreadArticle.html' )
    {
	&Fatal( 18, "$_[0]/ThreadArticleTree" );
    }

    $gHgStr .= $HTML_HR . "<ul>\n";
    
    local( $AddNum ) = "&num=$gNum&old=$gOld&rev=$gRev";

    local( $Id, $IdNum, $Fid );
    if ($gTo < $gFrom)
    {
	# 空だった……
	$gHgStr .= "<li>$H_NOARTICLE</li>\n";
    }
    elsif ( $gVRev )
    {
	for( $IdNum = $gFrom; $IdNum <= $gTo; $IdNum++ )
	{
	    # 該当記事のIDを取り出す
	    $Id = $DB_ID[$IdNum];
	    ($Fid = $DB_FID{$Id}) =~ s/,.*$//o;
	    # 後方参照は後回し．
	    next if ((( $Fid ne '' ) && ( $SYS_THREAD_FORMAT == 2 )) ||
		( $gADDFLAG{$Fid} == 2 ));
	    # ノードを表示
	    if ( !$gExapand )
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
	    # &cgiprint'Cache( $gHgStr ); $gHgStr = '';
	}
    }
    else
    {
	for( $IdNum = $gTo; $IdNum >= $gFrom; $IdNum-- )
	{
	    $Id = $DB_ID[$IdNum];
	    ($Fid = $DB_FID{$Id}) =~ s/,.*$//o;
	    next if ((( $Fid ne '' ) && ( $SYS_THREAD_FORMAT == 2 )) ||
		( $gADDFLAG{$Fid} == 2 ));

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
	    # &cgiprint'Cache( $gHgStr ); $gHgStr = '';
	}
    }
    $gHgStr .= "</ul>\n";
}

sub hgThreadArticleBody
{
    if ( $_[0] ne 'ThreadArticle.html' )
    {
	&Fatal( 18, "$_[0]/ThreadArticleBody" );
    }

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
    ( $gComType ) = @_;
    
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

    &LockBoard();
    &DbCache( $BOARD ) if $BOARD;

    if ( $gComType == 3 )
    {
	# リンクかけかえの実施
	&ReLinkExec( $cgi'TAGS{'rfid'}, $cgi'TAGS{'rtid'}, $BOARD );
    }
    elsif ( $gComType == 5 )
    {
	# 移動の実施
	&ReOrderExec( $cgi'TAGS{'rfid'}, $cgi'TAGS{'rtid'}, $BOARD );
    }

    &UnlockBoard();

    # 表示する個数を取得
    $gNum = $cgi'TAGS{'num'};
    if ( defined( $cgi'TAGS{'id'} ))
    {
	$gOld = $#DB_ID - int( $cgi'TAGS{'id'} + $gNum/2 );
	$gOld = 0 if ( $gOld < 0 );
    }
    else
    {
	$gOld = $cgi'TAGS{'old'};
    }
    $gRev = $cgi'TAGS{'rev'};
    $gFold = $cgi'TAGS{'fold'} || 0;
    $gVRev = $gRev? 1-$SYS_BOTTOMTITLE : $SYS_BOTTOMTITLE;
    $gTo = $#DB_ID - $gOld;
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
	$gADDFLAG{$DB_ID[$IdNum]} = 2;
    }

    &htmlGen( 'ThreadTitle.html' );
}

sub hgThreadTitleBoardHeader
{
    if ( $_[0] ne 'ThreadTitle.html' )
    {
	&Fatal( 18, "$_[0]/ThreadTitleBoardHeader" )
	}

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
	    $gHgStr .= "<ul>\n<li>" . &LinkP( "b=$BOARD&c=ce&rtid=" .
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
<li>$H_DELETE_ICON:
この$H_MESGを削除します．</li>
<li>$H_SUPERSEDE_ICON:
この$H_MESGを訂正します．</li>
<li>$H_RELINKTO_MARK:
先に指定した$H_MESGの$H_REPLY先を，この$H_MESGにします．</li>
<li>$H_REORDERTO_MARK:
先に指定した$H_MESGを，この$H_MESGの下に移動します．</li>
</ul>
EOS
    }
}

sub hgThreadTitleTree
{
    &Fatal( 18, "$_[0]/ThreadTitleTree" ) if ( $_[0] ne 'ThreadTitle.html' );

    $gHgStr .= "<ul>\n";

    local( $AddNum ) = "&num=$gNum&old=$gOld&rev=$gRev";

    local( $IdNum, $Id, $Fid );
    if ( $gTo < $gFrom )
    {
	# 空だった……
	$gHgStr .= "<li>$H_NOARTICLE</li>\n";
    }
    elsif ( $gVRev )
    {
	# 古いのから処理
	if (( $gComType == 2 ) && ( $DB_FID{$cgi'TAGS{'rfid'}} ne '' ))
	{
	    $gHgStr .= '<li>' . &LinkP( "b=$BOARD&c=ce&rtid=&rfid=" .
		$cgi'TAGS{'rfid'} . '&roid=' . $cgi'TAGS{'roid'} . $AddNum,
		"[どの$H_MESGへの$H_REPLYでもなく，新着$H_MESGにする]" ) .
		"</li>\n";
	}
	elsif ( $gComType == 4 )
	{
	    $gHgStr .= '<li>' . &LinkP( "b=$BOARD&c=mve&rtid=&rfid=" .
		$cgi'TAGS{'rfid'} . "&roid=" . $cgi'TAGS{'roid'} . $AddNum,
		"[全記事の先頭に移動する(このページの，ではありません)]" ) .
		"</li>\n";
	}

	for( $IdNum = $gFrom; $IdNum <= $gTo; $IdNum++ )
	{
	    # 該当記事のIDを取り出す
	    $Id = $DB_ID[$IdNum];
	    ($Fid = $DB_FID{$Id}) =~ s/,.*$//o;
	    # 後方参照は後回し．
	    next if ((( $Fid ne '' ) && ( $SYS_THREAD_FORMAT == 2 )) ||
		( $gADDFLAG{$Fid} == 2 ));
	    # ノードを表示
	    if ( $POLICY & 8 )
	    {
		&ThreadTitleNodeMaint( $Id, $gComType, $AddNum, 1 );
	    }
	    else
	    {
		if ( $gFold )
		{
		    &ThreadTitleNodeNoThread( $Id, 1 );
		}
		elsif ( $SYS_THREAD_FORMAT == 0 )
		{
		    &ThreadTitleNodeThread( $Id, 1 );
		}
		elsif ( $SYS_THREAD_FORMAT == 1 )
		{
		    &ThreadTitleNodeAllThread( $Id, 1 );
		}
		else
		{
		    &ThreadTitleNodeNoThread( $Id, 1 );
		}
	    }
	    # &cgiprint'Cache( $gHgStr ); $gHgStr = '';
	}
    }
    else
    {
	# 新しいのから処理
	if (( $gComType == 2 ) && ( $DB_FID{$cgi'TAGS{'rfid'}} ne '' ))
	{
	    $gHgStr .= '<li>' . &LinkP( "b=$BOARD&c=ce&rtid=&rfid=" .
		$cgi'TAGS{'rfid'} . "&roid=" . $cgi'TAGS{'roid'} . $AddNum,
		"[どの$H_MESGへの$H_REPLYでもなく，新着$H_MESGにする]" ) .
		"</li>\n";
	}
	elsif ( $gComType == 4 )
	{
	    $gHgStr .= '<li>' . &LinkP( "b=$BOARD&c=mve&rtid=&rfid=" .
		$cgi'TAGS{'rfid'} . "&roid=" . $cgi'TAGS{'roid'} . $AddNum,
		"[全記事の先頭に移動する(このページの，ではありません)]" ) .
		"</li>\n";
	}

	for( $IdNum = $gTo; $IdNum >= $gFrom; $IdNum-- )
	{
	    # 後は同じ
	    $Id = $DB_ID[$IdNum];
	    ($Fid = $DB_FID{$Id}) =~ s/,.*$//o;
	    next if ((( $Fid ne '' ) && ( $SYS_THREAD_FORMAT == 2 )) ||
		( $gADDFLAG{$Fid} == 2 ));

	    if ( $POLICY & 8 )
	    {
		&ThreadTitleNodeMaint( $Id, $gComType, $AddNum, 1 );
	    }
	    else
	    {
		if ( $gFold )
		{
		    &ThreadTitleNodeNoThread( $Id, 1 );
		}
		elsif ( $SYS_THREAD_FORMAT == 0 )
		{
		    &ThreadTitleNodeThread( $Id, 1 );
		}
		elsif ( $SYS_THREAD_FORMAT == 1 )
		{
		    &ThreadTitleNodeAllThread( $Id, 1 );
		}
		else
		{
		    &ThreadTitleNodeNoThread( $Id, 1 );
		}
	    }
	    # &cgiprint'Cache( $gHgStr ); $gHgStr = '';
	}
    }
    $gHgStr .= "</ul>\n";
}

# 新着ノードのみ表示
sub ThreadTitleNodeNoThread
{
    local( $Id, $flag ) = @_;
    &DumpArtSummaryItem( $Id, $DB_AIDS{$Id}, $DB_ICON{$Id}, $DB_TITLE{$Id},
	$DB_NAME{$Id}, $DB_DATE{$Id}, $flag );
    $flag &= 6; # 110
    push( @gIDLIST, $Id );
    $gHgStr .= "</li>\n";
}

# ページ内スレッドのみ表示
sub ThreadTitleNodeThread
{
    local( $Id, $flag ) = @_;

    # ページ外ならおしまい．
    return if ( $gADDFLAG{$Id} != 2 );

    &DumpArtSummaryItem( $Id, $DB_AIDS{$Id}, $DB_ICON{$Id}, $DB_TITLE{$Id},
	$DB_NAME{$Id}, $DB_DATE{$Id}, $flag );
    $flag &= 6; # 110

    $gADDFLAG{$Id} = 1;		# 整形済み
    push( @gIDLIST, $Id );

    # 娘が居れば……
    if ( $DB_AIDS{$Id} )
    {
	$gHgStr .= "<ul>\n";
	grep( &ThreadTitleNodeThread( $_, $flag ), split( /,/,
	    $DB_AIDS{$Id} ));
	$gHgStr .= "</ul>\n";
    }
    $gHgStr .= "</li>\n";
}

# 全スレッドの表示
sub ThreadTitleNodeAllThread
{
    local( $Id, $flag ) = @_;

    # 表示済みならおしまい．
    return if ( $gADDFLAG{$Id} == 1 );

    &DumpArtSummaryItem( $Id, $DB_AIDS{$Id}, $DB_ICON{$Id}, $DB_TITLE{$Id},
	$DB_NAME{$Id}, $DB_DATE{$Id}, $flag );
    $flag &= 6; # 110
    $gADDFLAG{$Id} = 1;		# 整形済み
    push( @gIDLIST, $Id );

    # 娘が居れば……
    if ( $DB_AIDS{$Id} )
    {
	$gHgStr .= "<ul>\n";
	grep( &ThreadTitleNodeAllThread( $_, $flag ),
	     split( /,/, $DB_AIDS{$Id} ));
	$gHgStr .= "</ul>\n";
    }
    $gHgStr .= "</li>\n";
}

# 管理者用のスレッド表示
sub ThreadTitleNodeMaint
{
    local( $Id, $ComType, $AddNum, $flag ) = @_;

    return if ( $gADDFLAG{$Id} != 2 );

    local($FromId) = $cgi'TAGS{'rfid'};

    &DumpArtSummaryItem( $Id, $DB_AIDS{$Id}, $DB_ICON{$Id}, $DB_TITLE{$Id},
	$DB_NAME{$Id}, $DB_DATE{$Id}, $flag );
    $flag &= 6; # 110
    $gHgStr .= " .......... \n";

    # リンク先変更コマンド(From)
    # 移動コマンド(From)
    $gHgStr .= &LinkP( "b=$BOARD&c=ct&rfid=$Id&roid=" . $DB_FID{$Id} . $AddNum,
	$H_RELINKFROM_MARK, '', $H_RELINKFROM_MARK_L ) . "\n";
    if ($DB_FID{$Id} eq '')
    {
	$gHgStr .= &LinkP( "b=$BOARD&c=mvt&rfid=$Id&roid=" . $DB_FID{$Id} .
	    $AddNum, $H_REORDERFROM_MARK, '', $H_REORDERFROM_MARK_L ) . "\n";
    }

    # 削除コマンド
    $gHgStr .= &LinkP( "b=$BOARD&c=dp&id=$Id", $H_DELETE_ICON, '',
	$H_DELETE_ICON_L ) . "\n";
    $gHgStr .= &LinkP( "b=$BOARD&c=f&s=on&id=$Id", $H_SUPERSEDE_ICON, '',
	$H_SUPERSEDE_ICON_L ) . "\n";

    # 移動コマンド(To)
    if (( $ComType == 4 ) && ( $FromId ne $Id ) && ( $DB_FID{$Id} eq '' ) &&
	( $FromId ne $Id ))
    {
	$gHgStr .= &LinkP( "b=$BOARD&c=mve&rtid=$Id&rfid=$FromId&roid=" .
	    $cgi'TAGS{'roid'} . $AddNum, $H_REORDERTO_MARK, '',
	    $H_REORDERTO_MARK_L ) . "\n";
    }

    # リンク先変更コマンド(To)
    if (( $ComType == 2 ) && ( $FromId ne $Id ) && ( !grep( /^$FromId$/,
	split( /,/, $DB_AIDS{$Id} ))) && ( !grep( /^$FromId$/, split( /,/,
	$DB_FID{$Id} ))))
    {
	$gHgStr .= &LinkP( "b=$BOARD&c=ce&rtid=$Id&rfid=$FromId&roid=" .
	    $cgi'TAGS{'roid'} . $AddNum, $H_RELINKTO_MARK, '',
	    $H_RELINKTO_MARK_L ) . "\n";
    }

    $gADDFLAG{$Id} = 1;		# 整形済み

    # 娘が居れば……
    if ($DB_AIDS{$Id})
    {
	$gHgStr .= "<ul>\n";
	grep( &ThreadTitleNodeMaint( $_, $ComType, $AddNum, $flag ),
	     split( /,/, $DB_AIDS{$Id} ));
	$gHgStr .= "</ul>\n";
    }

    $gHgStr .= "</li>\n";
}


###
## 日付順タイトル一覧
#
sub UISortTitle
{
    &LockBoard();
    &DbCache( $BOARD ) if $BOARD;
    &UnlockBoard();

    # 表示する個数を取得
    local( $Num ) = $cgi'TAGS{'num'};
    local( $Old );
    if ( defined( $cgi'TAGS{'id'} ))
    {
	$Old = $#DB_ID - int( $cgi'TAGS{'id'} + $Num/2 );
	$Old = 0 if ( $Old < 0 );
    }
    else
    {
	$Old = $cgi'TAGS{'old'};
    }
    local( $Rev ) = $cgi'TAGS{'rev'};
    $gFold = $cgi'TAGS{'fold'} || 0;
    $gVRev = $Rev? 1-$SYS_BOTTOMTITLE : $SYS_BOTTOMTITLE;
    $gTo = $#DB_ID - $Old;
    $gFrom = $gTo - $Num + 1;
    $gFrom = 0 if (( $gFrom < 0 ) || ( $Num == 0 ));

    $gPageLinkStr = &PageLink( 'r', $Num, $Old, $Rev, '' );

    &htmlGen( 'SortTitle.html' );
}

sub hgSortTitleTree
{
    &Fatal( 18, "$_[0]/SortTitleTree" ) if ( $_[0] ne 'SortTitle.html' );

    $gHgStr .= "<ul>\n";

    # 記事の表示
    local( $IdNum, $Id );
    if ( $#DB_ID == -1 )
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
		$Id = $DB_ID[$IdNum];
		&DumpArtSummaryItem( $Id, $DB_AIDS{$Id}, $DB_ICON{$Id},
		    $DB_TITLE{$Id}, $DB_NAME{$Id}, $DB_DATE{$Id}, 1 );
		$gHgStr .= "</li>\n";
	    }
	}
	else
	{
	    for ($IdNum = $gTo; $IdNum >= $gFrom; $IdNum--)
	    {
		$Id = $DB_ID[$IdNum];
		&DumpArtSummaryItem( $Id, $DB_AIDS{$Id}, $DB_ICON{$Id},
		    $DB_TITLE{$Id}, $DB_NAME{$Id}, $DB_DATE{$Id}, 1 );
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
    &LockBoard();
    &DbCache( $BOARD ) if $BOARD;
    &UnlockBoard();

    local( $id ) = $cgi'TAGS{'id'};

    # フォロー記事の木構造の取得
    # ex. '( a ( b ( c d ) ) ( e ) ( f ( g ) ) )'というリスト
    @gFollowIdTree = ();
    &GetFollowIdTree( $id, *gFollowIdTree );

    &htmlGen( 'ShowThread.html' );
}

sub hgShowThreadTitle
{
    &Fatal( 18, "$_[0]/ShowThreadTitle" ) if ( $_[0] ne 'ShowThread.html' );

    local( $tmp, $subject );
    ( $tmp, $tmp, $tmp, $subject ) = &GetTreeTopArticlesInfo( *gFollowIdTree );
    $gHgStr .= $subject;
}

sub hgShowThreadTitleTree
{
    if ( $_[0] ne 'ShowThread.html' )
    {
	&Fatal( 18, "$_[0]/ShowThreadTitleTree" );
    }

    &DumpArtThread( 7, @gFollowIdTree );
}

sub hgShowThreadMsgBody
{
    if ( $_[0] ne 'ShowThread.html' )
    {
	&Fatal( 18, "$_[0]/ShowThreadMsgBody" );
    }

    &DumpArtThread( 2, @gFollowIdTree );
}

sub hgShowThreadBackToTitleButton
{
    if ( $_[0] ne 'ShowThread.html' )
    {
	&Fatal( 18, "$_[0]/ShowThreadBackToTitleButton" );
    }

    &DumpButtonToTitleList( $BOARD, $cgi'TAGS{'id'} );
}


###
## 日付順メッセージ一覧
#
sub UISortArticle
{
    &LockBoard();
    &DbCache( $BOARD ) if $BOARD;
    &UnlockBoard();

    $gNum = $cgi'TAGS{'num'};
    $gOld = $cgi'TAGS{'old'};
    $gRev = $cgi'TAGS{'rev'};
    $gFold = $cgi'TAGS{'fold'} || 0;

    $gPageLinkStr = &PageLink( 'l', $gNum, $gOld, $gRev, '' );

    &htmlGen( 'SortArticle.html' );
}

sub hgSortArticleBody
{
    &Fatal( 18, "$_[0]/SortArticleBody" ) if ( $_[0] ne 'SortArticle.html' );

    local( $vRev ) = $gRev? 1-$SYS_BOTTOMARTICLE : $SYS_BOTTOMARTICLE;
    local( $To ) = $#DB_ID - $gOld;
    local( $From ) = $To - $gNum + 1; $From = 0 if (( $From < 0 ) ||
	( $gNum == 0 ));

    $gHgStr .= $HTML_HR;

    if (! $#DB_ID == -1)
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
		$Id = $DB_ID[$IdNum];
		&DumpArtBody( $Id, $SYS_COMMAND_EACH, 1 );
		$gHgStr .= $HTML_HR;
	    }
	}
	else
	{
	    for ( $IdNum = $To; $IdNum >= $From; $IdNum-- )
	    {
		$Id = $DB_ID[$IdNum];
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
    &LockBoard();
    &DbCache( $BOARD ) if $BOARD;
    &UnlockBoard();

    local( $tmp );
    ( $tmp, $gAids, $tmp, $gSubject ) = &GetArticlesInfo( $cgi'TAGS{'id'} );

    # 未投稿記事は読めない
    &Fatal( 8, '' ) if ( $gSubject eq '' );

    &htmlGen( 'ShowArticle.html' );
}

sub hgShowArticleTitle
{
    &Fatal( 18, "$_[0]/ShowArticleTitle" ) if ( $_[0] ne 'ShowArticle.html' );

    $gHgStr .= $gSubject;
}

sub hgShowArticleBody
{
    &Fatal( 18, "$_[0]/ShowArticleBody" ) if ( $_[0] ne 'ShowArticle.html' );

    &DumpArtBody( $cgi'TAGS{'id'}, 1, 1 );
}

sub hgShowArticleReply
{
    &Fatal( 18, "$_[0]/ShowArticleReply" ) if ( $_[0] ne 'ShowArticle.html' );

    &DumpReplyArticles( split( /,/, $gAids ));
}


###
## 記事の検索(表示画面の作成)
#
sub UISearchArticle
{
    &htmlGen( 'SearchArticle.html' );
}

sub hgSearchArticleResult
{
    if ( $_[0] ne 'SearchArticle.html' )
    {
	&Fatal( 18, "$_[0]/SearchArticleResult" );
    }

    &LockBoard();
    &DbCache( $BOARD ) if $BOARD;
    &UnlockBoard();

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
    if ( !( $POLICY & 8 ) && ( $SYS_OVERWRITE == 0 ))
    {
	&Fatal( 99, $cgi'TAGS{'c'} );
    }

    &LockBoard();
    &DbCache( $BOARD ) if $BOARD;
    &UnlockBoard();

    $gId = $cgi'TAGS{'id'};
    local( $tmp, $subject );
    ( $tmp, $gAids, $tmp, $subject ) = &GetArticlesInfo( $gId );

    # 未投稿記事は読めない
    &Fatal( 8, '' ) if ( $subject eq '' );

    &htmlGen( 'DeletePreview.html' );
}

sub hgDeletePreviewForm
{
    if ( $_[0] ne 'DeletePreview.html' )
    {
	&Fatal( 18, "$_[0]/DeletePreviewForm" );
    }

    local( %tags );
    %tags = ( 'c', 'de', 'b', $BOARD, 'id', $gId );
    &DumpForm( *tags, 'このメッセージを削除します', '', '' );

    if ( $gAids )
    {
	%tags = ( 'c', 'det', 'b', $BOARD, 'id', $gId );
	&DumpForm( *tags, "$H_REPLYメッセージもまとめて削除します", '', '' );
    }
}

sub hgDeletePreviewBody
{
    if ( $_[0] ne 'DeletePreview.html' )
    {
	&Fatal( 18, "$_[0]/DeletePreviewBody" );
    }

    &DumpArtBody( $gId, 0, 1 );
}

sub hgDeletePreviewReply
{
    if ( $_[0] ne 'DeletePreview.html' )
    {
	&Fatal( 18, "$_[0]/DeletePreviewReply" );
    }

    &DumpReplyArticles( split( /,/, $gAids ));
}


###
## 記事の削除
#
sub UIDeleteExec
{
    if ( !( $POLICY & 8 ) && ( $SYS_OVERWRITE == 0 ))
    {
	&Fatal( 99, $cgi'TAGS{'c'} );
    }

    local( $threadFlag ) = @_;

    &LockBoard();
    &DbCache( $BOARD ) if $BOARD;

    $gId = $cgi'TAGS{'id'};

    local( $tmp, $aids, $name );
    ( $tmp, $aids, $tmp, $tmp, $tmp, $tmp, $name ) = &GetArticlesInfo( $gId );
    &Fatal( 44, '' ) if ( !&IsUser( $name ) && !( $POLICY & 8 ));
    &Fatal( 19, '' ) if ( $aids && ( $SYS_OVERWRITE == 1 ));

    # 削除実行
    &DeleteArticle( $gId, $BOARD, $threadFlag );

    &UnlockBoard();

    &htmlGen( 'DeleteExec.html' );
}

sub hgDeleteExecBackToTitleButton
{
    if ( $_[0] ne 'DeleteExec.html' )
    {
	&Fatal( 18, "$_[0]/DeleteExecBackToTitleButton" );
    }

    &DumpButtonToTitleList( $BOARD, $gId );
}


###
## アイコン表示
#
sub UIShowIcon
{
    &htmlGen( 'ShowIcon.html' );
}


###
## ヘルプ表示
#
sub UIHelp
{
    &htmlGen( 'Help.html' );
}


###
## エラー表示
#
sub UIFatal
{
    ( $gMsg ) = @_;
    &htmlGen( 'Fatal.html' );
}

sub hgFatalMsg
{
    $gHgStr .= $gMsg;
}


###
## 汎用hg関数群
#
sub hgsTitle
{
    $gHgStr .=<<EOS;
<meta http-equiv="Content-Type" content="text/html; charset=EUC-JP">
<meta http-equiv="Content-Style-Type" content="text/css">
<base href="$BASE_URL">
<link rev="MADE" href="mailto:$MAINT">
EOS
    if ( $BOARD && ( -s &GetPath( $BOARD, $CSS_FILE )))
    {
	$gHgStr .= qq(<link rel="StyleSheet" href="$BOARD/$CSS_FILE" type="text/css" media="screen">);
    }
    else
    {
	$gHgStr .= qq(<link rel="StyleSheet" href="$CSS_FILE" type="text/css" media="screen">);
    }
}

sub hgsAddress
{
    $gHgStr .= "<address>\nMaintenance: " .
	&TagA( $MAINT_NAME, "mailto:$MAINT" ) . $HTML_BR .
	&TagA( $PROGNAME, "http://www.jin.gr.jp/~nahi/kb/" ) .
	": Copyright (C) 1995-99 " .
	&TagA( "NAKAMURA, Hiroshi", "http://www.jin.gr.jp/~nahi/" ) .
	".\n</address>\n";
}

sub hgcStatus
{
    $gHgStr .= qq(<p class="kbStatus">[);
    if ( $UNAME && ( $UNAME ne $GUEST ) && ( $UNAME ne
	$cgiauth'F_COOKIE_RESET ))
    {
	$gHgStr .= "$H_USER: $UNAME -- \n";
    }
    $gHgStr .= "$H_BOARD: $BOARDNAME -- \n" if ( $BOARDNAME ne '' );
    $gHgStr .= "最新${H_MESG}ID: " . $DB_ID[$#DB_ID] . " // \n" if @DB_ID;
    $gHgStr .= "時刻: " . &GetDateTimeFormatFromUtc( $^T );
    $gHgStr .= "]</p>\n";
}

sub hgcTopMenu
{
    $gHgStr .= qq(<div class="kbTopMenu">\n);
    local( $select, $contents );
    $select = &TagLabel( "表示画面", 'c', 'W' ) . ": \n";

    if ( $BOARD )
    {
	$contents .= sprintf( qq[<option%s value="v">最新$H_SUBJECT一覧(スレッド)\n], ( $cgi'TAGS{'c'} eq 'v' )? ' selected' : '' );
	$contents .= sprintf( qq[<option%s value="r">最新$H_SUBJECT一覧(日付順)\n], ( $cgi'TAGS{'c'} eq 'r' )? ' selected' : '' );
	$contents .= sprintf( qq[<option%s value="vt">最新$H_MESG一覧(スレッド)\n], ( $cgi'TAGS{'c'} eq 'vt' )? ' selected' : '' );
	$contents .= sprintf( qq[<option%s value="l">最新$H_MESG一覧(日付順)\n], ( $cgi'TAGS{'c'} eq 'l' )? ' selected' : '' );
	$contents .= sprintf( qq(<option%s value="s">$H_MESGの検索\n), ( $cgi'TAGS{'c'} eq 's' )? ' selected' : '' ) if $SYS_F_S;
	$contents .= sprintf( qq(<option%s value="n">$H_POSTNEWARTICLE\n), ( $cgi'TAGS{'c'} eq 'n' )? ' selected' : '' ) if (( $POLICY & 2 ) && ( !$SYS_NEWART_ADMINONLY || ( $POLICY & 8 )));
	$contents .= sprintf( qq(<option%s value="i">使える$H_ICON一覧\n), ( $cgi'TAGS{'c'} eq 'i' )? ' selected' : '' ) if $SYS_ICON;
    }

    $contents .= sprintf( qq(<option%s value="bl">$H_BOARD一覧\n),
	( $cgi'TAGS{'c'} eq 'bl' )? ' selected' : '' );
    $contents .= sprintf( qq(<option%s value="lo">$H_USER情報の呼び出し\n),
	( $cgi'TAGS{'c'} eq 'lo' )? ' selected' : '' ) if $SYS_AUTH;

    $select .= &TagSelect( 'c', $contents ) . "\n // " .
	&TagLabel( "表示件数", 'num', 'Y' ) . ': ' .
	&TagInputText( 'text', 'num', ( $cgi'TAGS{'num'} || $DEF_TITLE_NUM ),
	3 );
    local( %tags ) = ( 'b', $BOARD );
    &DumpForm( *tags, '表示(V)', '', *select );
    $gHgStr .= "</div>\n";
}

sub hgcHelp
{
    local( $var ) = $_[1];
    $gHgStr .= &LinkP( "b=$BOARD&c=h", &TagComImg( $ICON_HELP, 'ヘルプ' ), 'H',
	'', '', $var );
}

sub hgcSiteName
{
    $gHgStr .= $SYSTEM_NAME;
}

sub hgcFuncLink
{
    return unless $SYS_AUTH;

    $gHgStr .= "<dl>\n";

    $gHgStr .= "<dt>「新しく$H_USER情報をサーバに記憶させる」</dt>\n";
    $gHgStr .= '<dd>→' . &LinkP( 'c=ue', "$H_USER情報の新規登録" .
	&TagAccessKey( 'E' ), 'E' ) . "</dd>\n";

    if ( $UNAME )
    {
	$gHgStr .= "<dt>「別の$H_USER情報を呼び出す」（現在利用中の$H_USER情報は，$UNAMEのものです）</dt>\n";
	$gHgStr .= '<dd>→' . &LinkP( 'c=lo', "$H_USER情報の呼び出し" .
	    &TagAccessKey( 'L' ), 'L' ) . "</dd>\n";
    }

    if ( $POLICY & 4 )
    {
	$gHgStr .= "<dt>「$UNAMEについて登録した$H_USER情報を変更する」</dt>\n";
	$gHgStr .= '<dd>→' . &LinkP( 'c=uc', "$H_USER情報の変更" .
	    &TagAccessKey( 'C' ), 'C' ) . "</dd>\n";
    }

    if ( $POLICY & 8 )
    {
	$gHgStr .= "<dt>「新規に$H_BOARDを作りたい」</dt>\n";
	$gHgStr .= '<dd>→' . &LinkP( 'c=be', "$H_BOARDの新規作成" .
	    &TagAccessKey( 'A' ), 'A' ) . "</dd>\n";
    }

    $gHgStr .= "</dl>\n";
}

sub hgcPageLink
{
    $gHgStr .= $gPageLinkStr;
}

sub hgcBoardLinkAll
{
    # 全掲示板の情報を取り出す
    local( @board, %boardName, %boardInfo );
    &GetAllBoardInfo( *board, *boardName, *boardInfo );

    $gHgStr .= "<ul>\n";

    local( $newIcon, $modTimeUtc, $modTime, $nofArticle );
    foreach ( @board )
    {
	$modTimeUtc = &GetModifiedTime( $DB_FILE_NAME, $_ );
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

	$gHgStr .= '<li>' .
	    &LinkP( "b=$_&c=v&num=$DEF_TITLE_NUM", $boardName{$_} ) .
	    "$newIcon\n[最新: $modTime, 記事数: $nofArticle]\n";
	if ( $POLICY & 8 )
	{
	    $gHgStr .= &LinkP( "b=$_&c=bc", "←設定変更" ) . "\n";
	}

	$gHgStr .= $HTML_BR . $HTML_BR . "</li>\n";
    }
    $gHgStr .= "</ul>\n";
}

sub hgcBoardLink
{
    local( $var ) = $_[1];
    local( $com, $board ) = split( ':', $var );
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

    $modTimeUtc = &GetModifiedTime( $DB_FILE_NAME, $board );
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

    $gHgStr .= &LinkP( "b=$board&c=$com&num=$num", $gBoardName{$board} ) . "$newIcon\n[最新: $modTime, 記事数: $nofArticle]\n";
    if ( $POLICY & 8 )
    {
	$gHgStr .= &LinkP( "b=$board&c=bc", "←設定変更" ) . "\n";
    }
}

sub hgbBoardName
{
    $gHgStr .= $BOARDNAME if $BOARD;
}

sub hgbBoardHeader
{
    &DumpBoardHeader() if $BOARD;
}

sub hgbPostEntryForm
{
    if ( $POLICY & 2 )
    {
	&DumpArtEntry( $gDefIcon, $gEntryType, $gId, $gDefSubject,
	    $gDefTextType, $gDefArticle, $gDefName, $gDefEmail, $gDefUrl,
	    $gDefFmail );
    }
}

sub hgbSearchArticleForm
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

    local( $msg );
    $msg .= &TagInputCheck( 'searchsubject', $SearchSubject ) . ': ' . &TagLabel( $H_SUBJECT, 'searchsubject', 'T' ) . $HTML_BR;

    $msg .= &TagInputCheck( 'searchperson', $SearchPerson ) . ': ' . &TagLabel( "名前", 'searchperson', 'N' ) . $HTML_BR;

    $msg .= &TagInputCheck( 'searcharticle', $SearchArticle ) . ': ' . &TagLabel( $H_MESG, 'searcharticle', 'A' ) . $HTML_BR;

    local( $sec, $min, $hour, $mday, $mon, $year, $nowStr );
    if ( !$SearchPostTime )
    {
	( $sec, $min, $hour, $mday, $mon, $year, $nowStr ) = localtime( $^T );
	$nowStr = sprintf( "%04d/%02d/%02d", $year+1900, $mon+1, $mday );
    }
    $msg .= &TagInputCheck( 'searchposttime', $SearchPostTime ) . ': ' . &TagLabel( $H_DATE, 'searchposttime', 'D' ) . " // \n";
    $msg .= &TagInputText( 'text', 'searchposttimefrom', ( $SearchPostTimeFrom || '' ), 11 ) . ' ' . &TagLabel( '〜', 'searchposttimefrom', 'S' ) . " \n";
    $msg .= &TagInputText( 'text', 'searchposttimeto', ( $Searchposttimeto || '' ), 11 ) . &TagLabel( 'の間', 'searchposttimeto', 'E' ) . $HTML_BR;

    if ( $SYS_ICON )
    {
	$msg .= &TagInputCheck( 'searchicon', $SearchIcon ) . ': ' . &TagLabel( $H_ICON, 'searchicon', 'I' ) . " // \n";

	# アイコンの選択
	&CacheIconDb( $BOARD );

	local( $contents, $IconTitle );
	$contents = sprintf( qq(<option%s>$H_NOICON\n), ( $Icon &&
	    ( $Icon ne $H_NOICON ))? '' : ' selected' );
	foreach $IconTitle ( sort keys( %ICON_FILE ))
	{
	    $contents .= sprintf( "<option%s>$IconTitle\n",
	    	( $Icon eq $IconTitle )? ' selected' : '' );
	}
	$msg .= &TagSelect( 'icon', $contents ) . "\n";

	# アイコン一覧
	$msg .= '(' . &LinkP( "b=$BOARD&c=i", "使える$H_ICON一覧" .
	    &TagAccessKey( 'H' ), 'H' ) . ')\n' . $HTML_BR . $HTML_BR;
    }

    $msg .= &TagLabel( 'キーワード', 'key', 'K' ) . ': ' . &TagInputText(
	'text', 'key', $Key, $KEYWORD_LENGTH ) . $HTML_BR;
    %tags = ( 'c', 's', 'b', $BOARD );
    &DumpForm( *tags, '検索', 'リセット', *msg );
}

sub hgbAllIcon
{
    return unless $BOARD;
    &CacheIconDb( $BOARD );
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
    &GetBoardHeader( $BOARD, *msg );
    $gHgStr .= $msg;
}


###
## DumpArtEntry - メッセージ入力フォームの表示
#
# - SYNOPSIS
#	DumpArtEntry( $icon, $type, $id, $title, $texttype, $article, $name, $eMail, $url, $fMail );
#
# - ARGS
#	$icon		アイコン
#	$type		メッセージタイプ( 'supersede', and so )
#	$id		リプライ/修正元メッセージID
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

    &CacheIconDb( $BOARD );
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
    local( $icon, $type, $id, $title, $texttype, $article, $name, $eMail, $url, $fMail ) = @_;

    local( $msg );

    # アイコンの選択
    if ( $SYS_ICON )
    {
	&CacheIconDb( $BOARD );
	$msg .= &TagLabel( $H_ICON, 'icon', 'I' ) . " :\n";
	local( $contents );
	$contents = sprintf( "<option%s>$H_NOICON\n", (( $icon eq '' )?
	    ' selected' : '' ));
	foreach ( @ICON_TITLE )
	{
	    $contents .= sprintf( "<option%s>$_\n", ( $_ eq $icon )?
		' selected' : '' );
	}
	$msg .= &TagSelect( 'icon', $contents ) . "\n";

	$msg .= '(' . &LinkP( "b=$BOARD&c=i", "使える$H_ICON一覧" .
	    &TagAccessKey( 'H' ), 'H' ) . ')' . $HTML_BR;
    }

    $msg .= &TagLabel( $H_SUBJECT, 'subject', 'T' ) . ': ' . &TagInputText(
	'text', 'subject', $title, $SUBJECT_LENGTH ) . $HTML_BR;
    
    local( $ttFlag ) = 0;
    local( $ttBit ) = 0;
    
    foreach ( @H_TTLABEL )
    {
	if (( $SYS_TEXTTYPE & ( 2 ** $ttBit )) &&
	    ( $SYS_TEXTTYPE ^ ( 2 ** $ttBit )))
	{
	    $ttFlag = 1;	# 後で使う．きたない．．．
	}
	$ttBit++;
    }

    # 書き込み形式
    if ( $ttFlag )
    {
	$ttFlag = 0 if $texttype;
	$msg .= &TagLabel( $H_TEXTTYPE, 'texttype', 'Z' ) . ":\n";
	local( $contents );
	$ttBit = 0;
	foreach ( @H_TTLABEL )
	{
	    if ( $SYS_TEXTTYPE & ( 2 ** $ttBit ))
	    {
		if ( $ttFlag )
		{
		    $ttFlag = 0;	# now, using for a flag for the first.
		    $contents .= "<option selected>" . $H_TTLABEL[$ttBit] .
			"\n";
		}
		else
		{
		    $contents .= sprintf( "<option%s>" . $H_TTLABEL[$ttBit] .
			"\n", ( $H_TTLABEL[$ttBit] eq $texttype )?
			' selected' : '' );
		}
	    }
	    $ttBit++;
	}
	$msg .= &TagSelect( 'texttype', $contents ) . $HTML_BR;
    }
    else
    {
	$msg .= sprintf( qq(<input name="texttype" type="hidden" value="%s">),
	    $H_TTLABEL[(( log $SYS_TEXTTYPE ) / ( log 2 ))] ) . $HTML_BR;
    }

    $msg .= &TagLabel( $H_MESG, 'article', 'A' ) . ':' . $HTML_BR .
	&TagTextarea( 'article', $article, $TEXT_ROWS, $TEXT_COLS ) . $HTML_BR;

    if ( $POLICY & 4 )
    {
	# 登録済みの場合，名前，メイル，URLの入力は，無し．
    }
    else
    {
	$msg .= &TagLabel( $H_FROM, 'name', 'N' ) . ': ' . &TagInputText(
	    'text', 'name', $name, $NAME_LENGTH ) . $HTML_BR;
	$msg .= &TagLabel( $H_MAIL, 'mail', 'M' ) . ': ' . &TagInputText(
	    'text', 'mail', $eMail, $MAIL_LENGTH ) . $HTML_BR;
	$msg .= &TagLabel( $H_URL, 'url', 'U' ) . ': ' . &TagInputText( 'text',
	    'url', ( $url || 'http://' ), $URL_LENGTH ) . $HTML_BR;
    }

    if ( $SYS_MAIL & 2 )
    {
	$msg .= &TagLabel( 'リプライがあった時にメイルで連絡', 'fmail', 'F' ) .
	    ': ' . &TagInputCheck( 'fmail', $fMail ) . "\n";
    }
    $msg .= "</p>\n<p>\n";

    $msg .= &TagInputRadio( 'com_p', 'com', 'p', 1 ) . ":\n" . &TagLabel(
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
    $msg .= &TagInputRadio( 'com_x', 'com', 'x', 0 ) . ":\n" . &TagLabel(
	$doLabel, 'com_x', 'X' ) . $HTML_BR;

    local( $op ) = ( -M &GetPath( $BOARD, $DB_FILE_NAME ));
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
	( $fid, $aids, $date, $title, $icon, $host, $name, $eMail, $url ) = &GetArticlesInfo( $id );
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

    if ( $commandFlag && $SYS_COMMAND )
    {
	local( $num );
	foreach ( 0 .. $#DB_ID ) { $num = $_, last if ( $DB_ID[$_] eq $id ); }
	local( $prevId ) = $DB_ID[$num - 1] if ( $num > 0 );
	local( $nextId ) = $DB_ID[$num + 1];
	&DumpArtCommand( $id, $prevId, $nextId, ( $aids ne '' ), ( &IsUser(
	    $name ) && (( $aids eq '' ) || ( $SYS_OVERWRITE == 2 ))));
    }

    local( @origIdList );
    if ( $origFlag && ( $fid ne '' ))
    {
	@origIdList = split( /,/, $fid );
    }

    # ヘッダ（ユーザ情報とリプライ元: タイトルは除く）
    &DumpArtHeader( $name, $eMail, $url, $host, $date, @origIdList );

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
	    local( $dFid, $dAids, $dDate, $dSubject, $dIcon, $dRemoteHost,
		$dName ) = &GetArticlesInfo( $Head );
	    &DumpArtSummaryItem( $Head, $dAids, $dIcon, $dSubject, $dName,
		$dDate, $State&3 );
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
#	DumpSearchResult( $Key, $Subject, $Person, $Article, $PostTime, $PostTimeFrom, $PostTimeTo, $Icon, $IconType );
#
# - ARGS
#	$Key		キーワード
#	$Subject	タイトルを検索するか否か
#	$Person		投稿者を検索するか否か
#	$Article	本文を検索するか否か
#	$PostTime	日付を検索するか否か
#	$PostTimeFrom	開始日付
#	$PostTimeTo	終了日付
#	$Icon		アイコンを検索するか否か
#	$IconType	アイコン
#
# - DESCRIPTION
#	記事を検索して表示する
#
sub DumpSearchResult
{
    local( $Key, $Subject, $Person, $Article, $PostTime, $PostTimeFrom,
	$PostTimeTo, $Icon, $IconType ) = @_;

    local( @KeyList ) = split(/\s+/, $Key);

    # リスト開く
    $gHgStr .= "<ul>\n";

    local( $dId, $dAids, $dDate, $dTitle, $dIcon, $dName, $dEmail );
    local( $SubjectFlag, $PersonFlag, $PostTimeFlag, $ArticleFlag );
    local( $HitNum, $Line, $FromUtc, $ToUtc );
    foreach ($[ .. $#DB_ID)
    {
	# 記事情報
	$dId = $DB_ID[$_];
	$dIcon = $DB_ICON{$dId};
	$dTitle = $DB_TITLE{$dId};
	$dName = $DB_NAME{$dId};
	$dEmail = $DB_EMAIL{$dId};
	$dAids = $DB_AIDS{$dId};
	$dDate = $DB_DATE{$dId};

	# 変数のリセット
	$SubjectFlag = $PersonFlag = $PostTimeFlag = $ArticleFlag = 0;
	$Line = '';

	# アイコンチェック
	next if ( $Icon && ( $dIcon ne $IconType ));

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
	    &DumpArtSummaryItem( $dId, $dAids, $dIcon, $dTitle, $dName, $dDate,
		1 );

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
	$gHgStr .= "</ul>\n<ul>";
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
## DumpReplyArticles - リプライ記事へのリンクの表示
#
# - SYNOPSIS
#	DumpReplyArticles( @_ );
#
# - ARGS
#	@_	リプライ記事IDのリスト
#
# - DESCRIPTION
#	リプライ記事へのリンクを表示する．
#
sub DumpReplyArticles
{
    $gHgStr .= "$H_LINE\n<p>\n▼$H_REPLY\n";

    if ( @_ )
    {
	# 反応記事があるなら…
	local( $id, @tree );
	foreach $id ( @_ )
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

    $gHgStr .= "</p>\n";
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
#	DumpArtCommand( $id, $prevId, $nextId, $reply, $delete );
#
# - ARGS
#	$id	記事ID
#	$prevId	前記事ID
#	$nextId	次記事ID
#	$reply	リプライ記事があるか
#	$delete	削除・訂正が可能か
#
sub DumpArtCommand
{
    local( $id, $prevId, $nextId, $reply, $delete ) = @_;

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

    local( $old ) = &GetTitleOldIndex( $id );

    $gHgStr .= &LinkP( 'c=bl', &TagComImg( $ICON_BLIST, $H_BACKBOARD ), 'B' ) .
	"\n";

    $gHgStr .= $dlmtS . &LinkP( "b=$BOARD&c=v&num=$DEF_TITLE_NUM&old=$old",
	&TagComImg( $ICON_TLIST, $H_BACKTITLEREPLY ), 'T' ) . "\n";
	
    if ( $prevId ne '' )
    {
	$gHgStr .= $dlmtS . &LinkP( "b=$BOARD&c=e&id=$prevId", &TagComImg(
	    $ICON_PREV, $H_PREVARTICLE ), 'P' ) . "\n";
    }
    else
    {
	$gHgStr .= $dlmtS . &TagComImg( $ICON_PREV, $H_PREVARTICLE, ) . "\n";
    }
	
    if ( $nextId ne '' )
    {
	$gHgStr .= $dlmtS . &LinkP( "b=$BOARD&c=e&id=$nextId", &TagComImg(
	    $ICON_NEXT, $H_NEXTARTICLE ), 'N' ) . "\n";
    }
    else
    {
	$gHgStr .= $dlmtS . &TagComImg( $ICON_NEXT, $H_NEXTARTICLE, ) . "\n";
    }

    if ( $reply )
    {
	$gHgStr .= $dlmtS . &LinkP( "b=$BOARD&c=t&id=$id", &TagComImg(
	    $ICON_THREAD, $H_READREPLYALL ), 'M' ) . "\n";
    }
    else
    {
	$gHgStr .= $dlmtS . &TagComImg( $ICON_THREAD, $H_READREPLYALL ) . "\n";
    }

    $gHgStr .= $dlmtL;

    if ( $POLICY & 2 )
    {
	$gHgStr .= $dlmtS . &LinkP( "b=$BOARD&c=f&id=$id", &TagComImg(
	    $ICON_FOLLOW, $H_REPLYTHISARTICLE ), 'R' ) . "\n" . $dlmtS .
	    &LinkP( "b=$BOARD&c=q&id=$id", &TagComImg( $ICON_QUOTE,
	    $H_REPLYTHISARTICLEQUOTE ), 'Q' ) . "\n";
    }
    else
    {
	$gHgStr .= $dlmtS . &TagComImg( $ICON_FOLLOW, $H_REPLYTHISARTICLE ) .
	    "\n" . $dlmtS . &TagComImg( $ICON_QUOTE,
	    $H_REPLYTHISARTICLEQUOTE ) . "\n";
    }

    if ( $SYS_AUTH )
    {
	$gHgStr .= $dlmtL;

	if ( $delete )
	{
	    $gHgStr .= $dlmtS . &LinkP( "b=$BOARD&c=f&s=on&id=$id", &TagComImg(
		$ICON_SUPERSEDE, $H_SUPERSEDE ), 'S' ) . "\n" . $dlmtS .
		&LinkP( "b=$BOARD&c=dp&id=$id", &TagComImg( $ICON_DELETE,
	    	$H_DELETE ), 'D' ) . "\n";
	}
	else
	{
	    $gHgStr .= $dlmtS . &TagComImg( $ICON_SUPERSEDE, $H_SUPERSEDE ) .
	    	"\n" . $dlmtS . &TagComImg( $ICON_DELETE, $H_DELETE ) . "\n";
	}
    }

    if ( $SYS_COMICON == 1 )
    {
	$gHgStr .= $dlmtL;
	$gHgStr .= $dlmtS . &LinkP( "b=$BOARD&c=h", &TagComImg( $ICON_HELP,
	    'ヘルプ' ), 'H', '', '', 'list' ) . "\n";
    }
    $gHgStr .= qq(</p>\n);
}


###
## DumpArtHeader - 記事ヘッダ（タイトル除く）の表示
#
# - SYNOPSIS
#	DumpArtHeader( $name, $eMail, $url, $host, $date, @origIdList );
#
# - ARGS
#	$name		ユーザ名
#	$eMail		メイルアドレス
#	$url		URL
#	$host		Remote Host名
#	$date		日付（UTC）
#	@origIdList	リプライ元記事ID
#
sub DumpArtHeader
{
    local( $name, $eMail, $url, $host, $date, @origIdList ) = @_;

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
    if ( @origIdList )
    {
	# オリジナル記事
	local( $dId, $dFid, $dAids, $dDate, $dTitle, $dIcon, $dHost, $dName );
	if ( $#origIdList > 0 )
	{
	    $dId = $origIdList[$#origIdList];
	    ( $dFid, $dAids, $dDate, $dTitle, $dIcon, $dHost, $dName ) =
		&GetArticlesInfo( $dId );
	    $gHgStr .= "<strong>$H_ORIG_TOP:</strong> ";
	    &DumpArtSummary( $dId, $dAids, $dIcon, $dTitle, $dName, $dDate,
		0 );
	    $gHgStr .= $HTML_BR;
	}

	# 元記事
	$dId = $origIdList[0];
	( $dFid, $dAids, $dDate, $dTitle, $dIcon, $dHost, $dName ) =
	    &GetArticlesInfo( $dId );
	$gHgStr .= "<strong>$H_ORIG:</strong> ";
	&DumpArtSummary( $dId, $dAids, $dIcon, $dTitle, $dName, $dDate, 0 );
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
	$gHgStr .= "<p>" . &LinkP( "b=$board&c=v&num=$DEF_TITLE_NUM&old=$old",
	    $H_BACKTITLEREPLY . &TagAccessKey( 'B' ), 'B' ) . "</p>\n";
	$gHgStr .= "<p>" . &LinkP( "b=$board&c=r&num=$DEF_TITLE_NUM&old=$old",
	    $H_BACKTITLEDATE ) . "</p>\n";
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
	$gHgStr .= "<p>" . &LinkP( "b=$board&c=e&id=$id", $msg .
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
	$gHgStr .= qq(<input name="$_" type="hidden" value="$tags{$_}">\n);
    }
    if ( !$noAuth && ( $SYS_AUTH == 3 ))
    {
	$gHgStr .= qq(<input name="kinoU" type="hidden" value="$UNAME">\n);
	$gHgStr .= qq(<input name="kinoP" type="hidden" value="$PASSWD">\n);
	$gHgStr .= qq(<input name="kinoA" type="hidden" value="3">\n);
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
#	DumpArtSummary( $id, $aids, $icon, $title, $name, $origDate, $flag);
#
# - ARGS
#	$id		記事ID
#	$aids		リプライ記事があるか否か
#	$icon		記事アイコンID
#	$title		記事のSubject
#	$name		記事の投稿者名
#	$origDate	記事の投稿日付(UTC)
#	$flag		表示カスタマイズフラグ
#	    2^0 ... スレッドの先頭であるか（▲が付く）
#	    2^1 ... 同一ページfragmentリンクを利用するか（#記事番号でリンク）
#
# - DESCRIPTION
#	ある記事をタイトルリスト表示用にフォーマットする．
#
sub DumpArtSummary
{
    local( $id, $aids, $icon, $title, $name, $origDate,	$flag ) = @_;

    $gHgStr .= qq(<span class="kbTitle">$id.);	# 初期化

    if ( $flag&1 && $DB_FID{$id} )
    {
	local( $fId ) = $DB_FID{$id};
	$fId =~ s/^.*,//o;
	$gHgStr .= ' ' . &LinkP( "b=$BOARD&c=t&id=$fId", $H_THREAD_ALL, '',
	    $H_THREAD_ALL_L );
    }

    $gHgStr .= ' ' . &TagMsgImg( $icon ) . ' ' .
	(( $flag&2 )? &TagA( $title || $id, "$cgi'REQUEST_URI#a$id" ) :
	&LinkP( "b=$BOARD&c=e&id=$id", $title || $id ));

    if ( $aids )
    {
	$gHgStr .= ' ' . &LinkP( "b=$BOARD&c=t&id=$id", $H_THREAD, '',
	    $H_THREAD_L );
    }

    $gHgStr .= ' [' . ( $name || $MAINT_NAME ) . '] ' .
	&GetDateTimeFormatFromUtc( $origDate || &GetModifiedTime( $id,
	$BOARD));

    if ( $DB_NEW{$id} )
    {
	$gHgStr .= ' ' . &TagMsgImg( $H_NEWARTICLE );
    }
    $gHgStr .= '</span>';
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
#	for each `<KB:foobar>' LINE in the source file,
#	the function `foobar' was called.
#
# - RETURN
#	1 if succeed, 0 if failed.
#
sub htmlGen
{
    local( $source ) = @_;

    local( $file ) = &GetPath( $UI_DIR, $source );

    $gHgStr = "";
    open( SRC, "<$file" ) || &Fatal( 1, $file );

    if ( $SYS_COOKIE_EXPIRE == 1 )
    {
	$cookieExpire = 'Thursday, 31-Dec-2029 23:59:59 GMT';
    }
    elsif ( $SYS_COOKIE_EXPIRE == 2 )
    {
	$cookieExpire = $^T + ( $SYS_COOKIE_VALUE * 86400 );
	# 86400 = 24 * 60 * 60
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

    while( <SRC> )
    {
	LINE: while ( 1 )
	{
	    if ( s/<KB:(\w+)(\s*var="([^"]*)")?>//o )
	    {
		$gHgStr .= $`;
		eval( '&hg' . $1 . '( "' . $source . '", "' . $3 . '" );' );
		&Fatal( 998, "$file : $@" ) if $@;
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
#	$Subject	新規記事Subject
#	$Icon		新規記事アイコン
#	$Id		新規記事ID
#	@To		送信先E-Mail addrリスト
#
# - DESCRIPTION
#	記事が到着したことをメイルする．
#
sub ArriveMail
{
    local( $Name, $Email, $Subject, $Icon, $Id, @To ) = @_;

    local( $StrSubject, $MailSubject, $StrFrom, $Message );
    $StrSubject = ( !$SYS_ICON || ( $Icon eq $H_NOICON ))? $Subject :
	"($Icon) $Subject";
    $StrSubject =~ s/<[^>]*>//go;
    $StrSubject = &HTMLDecode( $StrSubject );
    $MailSubject = &GetMailSubjectPrefix( $BOARDNAME, $Id ) . $StrSubject;
    $StrFrom = $Email? "$Name <$Email>" : "$Name";

    $Message = "$SYSTEM_NAMEからのお知らせです．

「$BOARDNAME」に対して「$StrFrom」さんから，
「$StrSubject」という題での書き込みがありました．

お時間のある時に
$SCRIPT_URL?b=$BOARD&c=e&id=$Id
を御覧下さい．

では失礼します．";

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
sub FollowMail
{
    local( $Name, $Email, $Date, $Subject, $Icon, $Id, $Fname, $Femail, $Fsubject, $Ficon, $Fid, @To ) = @_;
    
    local( $InputDate, $StrSubject, $FstrSubject, $MailSubject, $StrFrom, $FstrFrom, $Message );

    $InputDate = &GetDateTimeFormatFromUtc( $Date );
    $StrSubject = ( !$SYS_ICON || ( $Icon eq $H_NOICON ))? "$Subject" :
	"($Icon) $Subject";
    $StrSubject =~ s/<[^>]*>//go;
    $StrSubject = &HTMLDecode( $StrSubject );
    $FstrSubject = ( $Ficon eq $H_NOICON )? $Fsubject : "($Ficon) $Fsubject";
    $FstrSubject =~ s/<[^>]*>//go;
    $FstrSubject = &HTMLDecode( $FstrSubject );
    $MailSubject = &GetMailSubjectPrefix( $BOARDNAME, $Fid ) . $FstrSubject;
    $StrFrom = $Email? "$Name <$Email>" : "$Name";
    $FstrFrom = $Femail? "$Fname <$Femail>" : "$Fname";

    $Message = "$SYSTEM_NAMEからのお知らせです．

$InputDateに「$BOARDNAME」に対して「$StrFrom」さんが書いた，
「$StrSubject」
$SCRIPT_URL?b=$BOARD&c=e&id=$Id
に対して，
「$FstrFrom」さんから
「$FstrSubject」という題での反応がありました．

お時間のある時に
$SCRIPT_URL?b=$BOARD&c=e&id=$Fid
を御覧下さい．

では失礼します．";

    # メイル送信
    &SendArticleMail( $Fname, $Femail, $MailSubject, $Message, $Fid, @To );
}


###
## MakeNewArticle - 新たに投稿された記事の生成
#
# - SYNOPSIS
#	MakeNewArticle($Board, $Id, $artKey, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail);
#
# - ARGS
#	$Board		作成する記事が入る掲示板のID
#	$Id		リプライ元記事のID
#	$artKey		多重書き込み防止用キー
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
#
sub MakeNewArticle
{
    local( $Board, $Id, $artKey, $TextType, $Name, $Email, $Url, $Icon,
	$Subject, $Article, $Fmail, $MailRelay ) = @_;

    local( $ArticleId );

    &CheckArticle( $Board, *Name, *Email, *Url, *Subject, *Icon, *Article );

    # 新しい記事番号を取得(まだ記事番号は増えてない)
    $ArticleId = &GetNewArticleId( $Board );

    # 正規のファイルの作成
    &MakeArticleFile( $TextType, $Article, $ArticleId, $Board );

    # 新しい記事番号を書き込む
    &WriteArticleId( $ArticleId, $Board, $artKey );

    # DBファイルに投稿された記事を追加
    # 通常の記事引用ならID
    &AddDBFile( $ArticleId, $Board, $Id, $^T, $Subject, $Icon,
	( $SYS_LOGHOST? $REMOTE_INFO : '' ), $Name, $Email, $Url, $Fmail,
	$MailRelay );

    $ArticleId;
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

    local( $Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $dId, @Target, $TargetId );

    # 記事情報の取得
    ( $Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url ) = &GetArticlesInfo( $Id );

    # データの書き換え(必要なら娘も)
    @Target = ( $Id );
    foreach $TargetId ( @Target )
    {
	foreach ( 0 .. $#DB_ID )
	{
	    # IDを取り出す
	    $dId = $DB_ID[$_];
	    # フォロー記事リストの中から，削除する記事のIDを取り除く
	    $DB_AIDS{$dId} = join( ',', grep(( !/^$TargetId$/o ), split( /,/, $DB_AIDS{$dId} )));
	    # 元記事から削除記事のIDを取り除く
	    $DB_FID{$dId} = '' if ( $DB_FID{$dId} eq $TargetId );
	    $DB_FID{$dId} =~ s/,$TargetId,.*$//;
	    $DB_FID{$dId} =~ s/^$TargetId,.*$//;
	    $DB_FID{$dId} =~ s/,$TargetId$//;
	    # 娘も対象とする
	    push( @Target, split( /,/, $DB_AIDS{$dId} )) if ( $ThreadFlag && ( $dId eq $TargetId ));
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
    local( $Board, $Id, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail ) = @_;

    local( $SupersedeId, $File, $SupersedeFile );

    # 入力された記事情報のチェック
    &CheckArticle( $Board, *Name, *Email, *Url, *Subject, *Icon, *Article );

    # DBファイルを訂正
    $SupersedeId = &SupersedeDbFile( $Board, $Id, $^T, $Subject, $Icon, ( $SYS_LOGHOST? $REMOTE_INFO : '' ), $Name, $Email, $Url, $Fmail );

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
    &FatalPriv( 50, '' ) if ( grep( /^$FromId$/, split( /,/, $DB_FID{$ToId} )));

    # データ書き換え
    foreach ( 0 .. $#DB_ID )
    {
	# IDを取り出す
	$dId = $DB_ID[$_];
	# フォロー記事リストの中から，移動する記事のIDを取り除く
	$DB_AIDS{$dId} = join( ',', grep(( !/^$FromId$/o ), split( /,/, $DB_AIDS{$dId} )));
    }

    # 必要なら娘をとりだしておく
    @Daughters = split( /,/, $DB_AIDS{$FromId} ) if $DB_FID{$FromId};

    # 該当記事のリプライ先を変更する
    if ( $ToId eq '' )
    {
	$DB_FID{$FromId} = '';
    }
    elsif ( $DB_FID{$ToId} eq '' )
    {
	$DB_FID{$FromId} = "$ToId";
    }
    else
    {
	$DB_FID{$FromId} = "$ToId,$DB_FID{$ToId}";
    }

    # 該当記事の娘についても，リプライ先を変更する
    while ( $DaughterId = shift( @Daughters ))
    {
	# 孫娘も……
	push( @Daughters, split( /,/, $DB_AIDS{$DaughterId} ));
	# 書き換え
	if (( $DB_FID{$DaughterId} eq $FromId )
	    || ( $DB_FID{$DaughterId} =~ /^$FromId,/ ))
	{
	    $DB_FID{$DaughterId} = $DB_FID{$FromId} ? "$FromId,$DB_FID{$FromId}" : "$FromId";
	}
	elsif (( $DB_FID{$DaughterId} =~ /^(.*),$FromId$/ )
	       || ( $DB_FID{$DaughterId} =~ /^(.*),$FromId,/ ))
	{
	    $DB_FID{$DaughterId} = $DB_FID{$FromId} ? "$1,$FromId,$DB_FID{$FromId}" : "$1,$FromId";
	}
    }

    # リプライ先になった記事のフォロー記事群に追加する
    $DB_AIDS{$ToId} = ( $DB_AIDS{$ToId} ne '' ) ? "$DB_AIDS{$ToId},$FromId" : "$FromId";

    # 記事DBを更新する
    &UpdateArticleDb( $Board );

    # DB書き換えたので，キャッシュし直す
    &DbCache( $Board );
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

    # DB書き換えたので，キャッシュし直す
    &DbCache( $Board );
}


###
## CheckArticle - 入力された記事情報のチェック
#
# - SYNOPSIS
#	CheckArticle($board, *name, *eMail, *url, *subject, *icon, *article);
#
# - ARGS
#	$board		掲示板ID
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
    local( $board, *name, *eMail, *url, *subject, *icon, *article ) = @_;

    &CheckName( *name );
    &CheckEmail( *eMail );
    &CheckURL( *url );
    &CheckSubject( *subject );
    &CheckIcon( *icon, $board ) if $SYS_ICON;

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
	'B',	1,	$HTML_TAGS_GENATTRS,
	'BIG',	1,	$HTML_TAGS_GENATTRS,
	'CITE',	1,	$HTML_TAGS_GENATTRS,
	'CODE',	1,	$HTML_TAGS_GENATTRS,
	'DEL',	1,	"$HTML_TAGS_GENATTRS/CITE/DATETIME",
	'EM',	1,	$HTML_TAGS_GENATTRS,
	'I',	1,	$HTML_TAGS_GENATTRS,
	'IMG',	0,	"$HTML_TAGS_GENATTRS/ALT/HEIGHT/LONGDESC/SRC/WIDTH",
	'INS',	1,	"$HTML_TAGS_GENATTRS/CITE/DATETIME",
	'KBD',	1,	$HTML_TAGS_GENATTRS,
	'SAMP',	1,	$HTML_TAGS_GENATTRS,
	'SMALL',1,	$HTML_TAGS_GENATTRS,
	'SPAN',	1,	$HTML_TAGS_GENATTRS,
	'STRONG',1,	$HTML_TAGS_GENATTRS,
	'STYLE',1,	"$HTML_TAGS_I18NATTRS/MEDIA/TITLE/TYPE",
	'SUB',	1,	$HTML_TAGS_GENATTRS,
	'SUP',	1,	$HTML_TAGS_GENATTRS,
	'TT',	1,	$HTML_TAGS_GENATTRS,
	'VAR',	1,	$HTML_TAGS_GENATTRS,
	);
	
	local( %sNeedVec, %sFeatureVec, $tag );
	while( @subjectTags )
	{
	    $tag = shift( @subjectTags );
	    $sNeedVec{ $tag } = shift( @subjectTags );
	    $sFeatureVec{ $tag } = shift( @subjectTags );
	}

	# secrurity check
	&cgi'SecureHtmlEx( *subject, *sNeedVec, *sFeatureVec );
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
	'A',	1,	"$HTML_TAGS_GENATTRS/CHARSET/HREF/HREFLANG/NAME/REL/REV/TABINDEX/TARGET/TYPE",
	'ABBR',	1,	$HTML_TAGS_GENATTRS,
	'ADDRESS',1,	$HTML_TAGS_GENATTRS,
	'B',	1,	$HTML_TAGS_GENATTRS,
	'BIG',	1,	$HTML_TAGS_GENATTRS,
	'BLOCKQUOTE',1,	"$HTML_TAGS_GENATTRS/CITE",
	'BR',	0,	$HTML_TAGS_COREATTRS,
	'CITE',	1,	$HTML_TAGS_GENATTRS,
	'CODE',	1,	$HTML_TAGS_GENATTRS,
	'DD',	0,	$HTML_TAGS_GENATTRS,
	'DEL',	1,	"$HTML_TAGS_GENATTRS/CITE/DATETIME",
	'DFN',	1,	$HTML_TAGS_GENATTRS,
	'DIV',	1,	$HTML_TAGS_GENATTRS,
	'DL',	1,	$HTML_TAGS_GENATTRS,
	'DT',	0,	$HTML_TAGS_GENATTRS,
	'EM',	1,	$HTML_TAGS_GENATTRS,
	'H1',	1,	$HTML_TAGS_GENATTRS,
	'H2',	1,	$HTML_TAGS_GENATTRS,
	'H3',	1,	$HTML_TAGS_GENATTRS,
	'H4',	1,	$HTML_TAGS_GENATTRS,
	'H5',	1,	$HTML_TAGS_GENATTRS,
	'H6',	1,	$HTML_TAGS_GENATTRS,
	'HR',	0,	$HTML_TAGS_COREATTRS,
	'I',	1,	$HTML_TAGS_GENATTRS,
	'IMG',	0,	"$HTML_TAGS_GENATTRS/ALT/HEIGHT/LONGDESC/SRC/WIDTH",
	'INS',	1,	"$HTML_TAGS_GENATTRS/CITE/DATETIME",
	'KBD',	1,	$HTML_TAGS_GENATTRS,
	'LI',	0,	$HTML_TAGS_GENATTRS,
	'OL',	1,	$HTML_TAGS_GENATTRS,
	'P',	1,	$HTML_TAGS_GENATTRS,
	'PRE',	1,	$HTML_TAGS_GENATTRS,
	'Q',	1,	"$HTML_TAGS_GENATTRS/CITE",
	'SAMP',	1,	$HTML_TAGS_GENATTRS,
	'SMALL',1,	$HTML_TAGS_GENATTRS,
	'SPAN',	1,	$HTML_TAGS_GENATTRS,
	'STRONG',1,	$HTML_TAGS_GENATTRS,
	'STYLE',1,	"$HTML_TAGS_I18NATTRS/MEDIA/TITLE/TYPE",
	'SUB',	1,	$HTML_TAGS_GENATTRS,
	'SUP',	1,	$HTML_TAGS_GENATTRS,
	'TT',	1,	$HTML_TAGS_GENATTRS,
	'UL',	1,	$HTML_TAGS_GENATTRS,
	'VAR',	1,	$HTML_TAGS_GENATTRS,
# 色やサイズはstyleで指定すべきなので，今後絶滅必至のFONTタグなわけですが，
# それでもどーしても使いたいというあなたは，
# ↓の行の先頭の「#」を消してください．^^;
#	'FONT',	1,	"$HTML_TAGS_GENATTRS/SIZE/COLOR",
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
	&cgi'SecureHtmlEx( *article, *aNeedVec, *aFeatureVec );
    }
    elsif ( $textType eq $H_TTLABEL[2] )
    {
	# secrurity check
	&cgi'SecureHtmlEx( *article, *aNeedVec, *aFeatureVec );
    }
    else
    {
	&Fatal( 0, 'must not be reached...' );
    }
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
#	CheckIcon( *str, $board );
#
# - ARGS
#	*str		Icon文字列
#	$board		掲示板ID
#
# - DESCRIPTION
#	Iconの文字列チェックを行なう．
#	不正な文字列だったらエラー表示ルーチンへ．
#
sub CheckIcon
{
    local( *str, $board ) = @_;

    # アイコンのチェック; おかしけりゃ「無し」に設定．
    $str = $H_NOICON if ( !&GetIconUrlFromTitle( $str, $board ));

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
    &Fatal( 6, $String ) if ( $String =~ /^\d+$/ );
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

    local( @aidList ) = split( /,/, $DB_AIDS{$id} );

    push( @tree, '(', $id );
    foreach ( @aidList ) { &GetFollowIdTree( $_, *tree ); }
    push( @tree, ')' );
}


###
## GetTreeTopArticlesInfo - 木構造のトップ記事の情報を取得
#
# - SYNOPSIS
#	GetTreeTopArticlesInfo	( *tree );
#
# - ARGS
#	*tree	木構造が格納済みのリスト
#
# - DESCRIPTION
#	木構造の詳細については&GetFollowIdTree()を参照のこと．
#
# - RETURN
#	記事情報のリスト
#		リプライ元記事ID
#		この記事にリプライした記事のIDのリスト(「,」区切り)
#		投稿時間(UTC)
#		Subject
#		アイコンID
#		投稿ホスト
#		投稿者名
#		投稿者E-Mail
#		投稿者URL
#		リプライがあった時に投稿者にメイルを送るか否か
#
sub GetTreeTopArticlesInfo
{
    local( *tree ) = @_;
    &GetArticlesInfo( $tree[1] );
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
#	古いバージョンのKINOBOARDSでは，
#	DB中に時刻を表す文字列(not UTC)がそのまま入っているが，
#	それが渡された場合(UTCでなかった場合)は，そのまま返す．
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
#	UTC
#
sub GetUtcFromYYYY_MM_DD
{
    local( $str ) = shift;
    return -1 if ( length( $str ) != 10 );

    local( $year, $month, $mday ) = unpack( "a4 x a2 x a2", $str );
    if (( $year < 1970 ) ||
	( $year > 2037 ) ||
	( $month < 1 ) ||
	( $month > 12 ) ||
	( $mday < 1 ) ||
	( $mday > 31 ))
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
## DQEncode/DQDecode - 特殊文字のEncodeとDecode
#
# - SYNOPSIS
#	DQEncode($Str);
#	DQDecode($Str);
#
# - ARGS
#	$Str	Encode/Decodeする文字列
#
# - DESCRIPTION
#	HTMLの特殊文字(", >, <, &)をEncode/Decodeする．
#
# - RETURN
#	Encode/Decodeした文字列
#
sub DQEncode
{
    local( $Str ) = @_;
    $Str =~ s/\"/__dq__/go;
    $Str =~ s/\>/__gt__/go;
    $Str =~ s/\</__lt__/go;
    $Str =~ s/\&/__amp__/go;
    $Str;
}

sub DQDecode
{
    local( $Str ) = @_;
    $Str =~ s/__dq__/\"/go;
    $Str =~ s/__gt__/\>/go;
    $Str =~ s/__lt__/\</go;
    $Str =~ s/__amp__/\&/go;
    $Str;
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
## TAGEncode - 特殊文字のTAG埋め込み用Encode
#
# - SYNOPSIS
#	TAGEncode( *str );
#
# - ARGS
#	*str	TAG埋め込み用Encodeする文字列
#
# - DESCRIPTION
#	TAG埋め込み（<input value="ここの文字列">）用に，"と&を取り除く．
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
		local( $boardInfo ) = &GetBoardInfo( $1 );
		$tagStr = &LinkP( "b=$1&c=e&id=$2", $quoteStr ) if $boardInfo;
	    }
	    else
	    {
		$tagStr = &LinkP( "b=$BOARD&c=e&id=$artStr", $quoteStr );
	    }
	}
	elsif ( &IsUrl( $urlMatch ))
	{
	    $tagStr = &TagA( $quoteStr, $url, '', '', '', $SYS_LINK_TARGET );
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

    local( $t );

    # 元記事情報の取得
    local( $Fid, $Date, $Title, $Name );
    ( $Fid, $t, $Date, $Title, $t, $t, $Name ) = &GetArticlesInfo( $Id );

    # 元記事のさらに元記事情報
    local( $pName ) = '';
    if ( $Fid )
    {
	$Fid =~ s/,.*$//o;
	( $t, $t, $t, $t, $t, $t, $pName ) = &GetArticlesInfo( $Fid );
    }

    # 引用
    local( @ArticleBody );
    &GetArticleBody( $Id, $BOARD, *ArticleBody );

    if ( $SYS_QUOTEMSG )
    {
	local( $premsg ) = $SYS_QUOTEMSG;
	$premsg =~ s/__LINK__/[url:kb:$Id]/i;
	$premsg =~ s/__TITLE__/$Title/;
	$premsg =~ s/__DATE__/&GetDateTimeFormatFromUtc( $Date )/e;
	$premsg =~ s/__NAME__/$Name/;
	$msg .= $premsg;
    }
    local( $QMark, $line );
    foreach $line ( @ArticleBody )
    {
	&TAGEncode( *line );

	$QMark = $DEFAULT_QMARK;
	$QMark = $Name . ' ' . $QMark if $SYS_QUOTENAME;

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
	$str .= &LinkP(
	    "b=$BOARD&c=$com&num=$num&old=0&fold=$fold&rev=$rev",
	    $H_TOP . &TagAccessKey( 'T' ), 'T' );
	$str .= ' | ' . &LinkP(
	    "b=$BOARD&c=$com&num=$num&old=$nextOld&fold=$fold&rev=$rev",
	    $H_UP . &TagAccessKey( 'N' ), 'N' );
    }
    else
    {
	$str .= $H_TOP . &TagAccessKey( 'T' ) . ' | ' . $H_UP .
	    &TagAccessKey( 'N' );
    }

    if ( $SYS_REVERSE )
    {
	$str .= ' | ' .
	    &LinkP( "b=$BOARD&c=$com&num=$num&old=$old&fold=$fold&rev=" .
	    ( 1-$rev ), $H_REVERSE[ 1-$rev ] . &TagAccessKey( 'R' ), 'R',
	    $H_REVERSE_L );
    }

    if ( $SYS_EXPAND && ( $fold ne '' ))
    {
	$str .= ' | ' .
	    &LinkP( "b=$BOARD&c=$com&num=$num&old=$old&rev=$rev&fold=" .
	    ( 1-$fold ), $H_EXPAND[ 1-$fold ] . &TagAccessKey( 'E' ), 'E',
	    $H_EXPAND_L );
    }

    $str .= ' | ';

    if ( $num && ( $#DB_ID - $backOld >= 0 ))
    {
	$str .= &LinkP(
	    "b=$BOARD&c=$com&num=$num&old=$backOld&fold=$fold&rev=$rev",
	    $H_DOWN . &TagAccessKey( 'P' ), 'P' );
	$str .= ' | ' . &LinkP(
	    "b=$BOARD&c=$com&num=$num&old=" . ( $#DB_ID - $backOld + 1) .
	    "&fold=$fold&rev=$rev", $H_BOTTOM . &TagAccessKey( 'B' ),
	    'B' );
    }
    else
    {
	$str .= $H_DOWN . &TagAccessKey( 'P' ) . ' | ' . $H_BOTTOM .
	    &TagAccessKey( 'B' );
    }

    $str .= "</p>\n";

    $str;
}

sub ShowPageLinkEachPage	# not used.
{
    local( $com, $num, $old, $rev, $vRev ) = @_;

    local( $nextOld ) = ( $old > $num )? ( $old - $num ) : 0;
    local( $backOld ) = ( $old + $num );

    local( $str ) = '<p>';

    $MAX_PAGELINK = 5;

    if ( $SYS_REVERSE )
    {
	$str .= &LinkP( "b=$BOARD&c=$com&num=$num&old=$old&rev=" . ( 1-$rev ),
	    $H_REVERSE[ 1-$rev ] . &TagAccessKey( 'R' ), 'R', $H_REVERSE_L ) .
	    ' ';
    }

    if ( $SYS_EXPAND )
    {
	$str .= &LinkP( "b=$BOARD&c=$com&num=$num&old=$old&rev=$rev&fold=" .
	    ( 1-$fold ), $H_EXPAND[ 1-$fold ] . &TagAccessKey( 'E' ), 'E',
	    $H_EXPAND_L );
    }

    if ( $vRev )
    {
	if ( $num && ( $#DB_ID - $backOld > 0 ))
	{
	    $str .= &LinkP( "b=$BOARD&c=$com&num=$num&old=0&rev=$rev",
		$H_TOP );
	    $str .= &LinkP( "b=$BOARD&c=$com&num=$num&old=$backOld&rev=$rev",
		$H_UP );
	}
	else
	{
	    $str .= $H_TOP . $H_UP;
	}

	local( $i );
	for ( $i = -$MAX_PAGELINK; $i <= +$MAX_PAGELINK; $i++ )
	{
	    $str .= ' ';
	    if ( $old - $i * $num <= $#DB_ID )
	    {
		$str .= &LinkP( "b=$BOARD&c=$com&num=$num&old=" . ( $i*$num ) .
		    "&rev=$rev", $i );
	    }
	    else
	    {
		$str .= $i;
	    }
	}
	$str .= ' ';

	if ( $old )
	{
	    $str .= &LinkP( "b=$BOARD&c=$com&num=$num&old=$nextOld&rev=$rev",
		$H_DOWN );
	}
	else
	{
	    $str .= $H_DOWN;
	}
    }
    else
    {
	if ( $old )
	{
	    $str .= &LinkP( "b=$BOARD&c=$com&num=$num&old=0&rev=$rev",
		$H_TOP );
	    $str .= &LinkP( "b=$BOARD&c=$com&num=$num&old=$nextOld&rev=$rev",
		$H_UP );
	}
	else
	{
	    $str .= $H_TOP . $H_UP;
	}

	local( $i );
	$MAX_PAGELINK = 5;
	for ( $i = $MAX_PAGELINK; $i >= -$MAX_PAGELINK; $i-- )
	{
	    $str .= ' ';
	    if ( $old - $i * $num <= $#DB_ID )
	    {
		$str .= &LinkP( "b=$BOARD&c=$com&num=$num&old=" . ( $i*$num ) .
		    "&rev=$rev", $i );
	    }
	    else
	    {
		$str .= $i;
	    }
	}
	$str .= ' ';

	if ( $num && ( $#DB_ID - $backOld > 0 ))
	{
	    $str .= &LinkP( "b=$BOARD&c=$com&num=$num&old=$backOld&rev=$rev",
		$H_DOWN );
	}
	else
	{
	    $str .= $H_DOWN;
	}
    }

    $str .= "</p>\n";

    $str;
}

sub ShowPageLinkTop		# not used
{
    local( $com, $num, $old, $rev, $vRev ) = @_;

    local( $nextOld ) = ( $old > $num )? ( $old - $num ) : 0;
    local( $backOld ) = ( $old + $num );

    local( $str ) = '<p>';

    if ( $vRev )
    {
	if ( $num && ( $#DB_ID - $backOld > 0 ))
	{
	    $str .= &LinkP( "b=$BOARD&c=$com&num=$num&old=$backOld&rev=$rev",
		$H_DOWN );
	}
	else
	{
	    $str .= $H_DOWN;
	}
    }
    else
    {
	if ( $old )
	{
	    $str .= &LinkP( "b=$BOARD&c=$com&num=$num&old=0&rev=$rev",
		$H_TOP );
	    $str .= &LinkP( "b=$BOARD&c=$com&num=$num&old=$nextOld&rev=$rev",
		$H_UP );
	}
	else
	{
	    $str .= $H_TOP . $H_UP;
	}
    }

    if ( $SYS_REVERSE )
    {
	$str .= ' // ' . &LinkP( "b=$BOARD&c=$com&num=$num&old=$old&rev=" .
		( 1-$rev ), $H_REVERSE[ 1-$rev ], &TagAccessKey( 'R' ), 'R',
		$H_REVERSE_L );
    }

    if ( $SYS_EXPAND )
    {
	$str .= &LinkP( "b=$BOARD&c=$com&num=$num&old=$old&rev=$rev&fold=" .
	    ( 1-$fold ), $H_EXPAND[ 1-$fold ] . &TagAccessKey( 'E' ), 'E',
	    $H_EXPAND_L );
    }

    $str .= "</p>\n";

    $str;
}

sub ShowPageLinkBottom		# not used.
{
    local( $com, $num, $old, $rev, $vRev ) = @_;

    local( $nextOld ) = ( $old > $num )? ( $old - $num ) : 0;
    local( $backOld ) = ( $old + $num );

    local( $str ) = '<p>';

    if ( $SYS_REVERSE )
    {
	$str .= &LinkP( "b=$BOARD&c=$com&num=$num&old=$old&rev=" . ( 1-$rev ),
	    $H_REVERSE[ 1-$rev ] . &TagAccessKey( 'R' ), 'R', $H_REVERSE_L );
    }

    if ( $SYS_EXPAND )
    {
	$str .= ' ' .
	    &LinkP( "b=$BOARD&c=$com&num=$num&old=$old&rev=$rev&fold=" .
	    ( 1-$fold ), $H_EXPAND[ 1-$fold ] . &TagAccessKey( 'E' ), 'E',
	    $H_EXPAND_L ) . ' // ';
    }

    if ( $vRev )
    {
	if ( $old )
	{
	    $str .= &LinkP( "b=$BOARD&c=$com&num=$num&old=0&rev=$rev",
		$H_TOP );
	    $str .= &LinkP( "b=$BOARD&c=$com&num=$num&old=$nextOld&rev=$rev",
		$H_UP );
	}
	else
	{
	    $str .= $H_TOP . $H_UP;
	}
    }
    else
    {
	if ( $num && ( $#DB_ID - $backOld > 0 ))
	{
	    $str .= &LinkP( "b=$BOARD&c=$com&num=$num&old=$backOld&rev=$rev",
		$H_DOWN );
	}
	else
	{
	    $str .= $H_DOWN;
	}
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
	qq(<img src="$src" alt="$alt" width="$COMICON_WIDTH" height="$COMICON_HEIGHT" class="kbComIcon">);
    }
    elsif ( $SYS_COMICON == 2 )
    {
	qq(<img src="$src" alt="$alt" width="$COMICON_WIDTH" height="$COMICON_HEIGHT" class="kbComIcon">$alt);
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
	local( $src ) = &GetIconUrlFromTitle( $icon, $BOARD );
	qq(<img src="$src" alt="[$icon]" width="$MSGICON_WIDTH" height="$MSGICON_HEIGHT" class="kbMsgIcon">);
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

    $href =~ s/&/&amp;/go;
    if ( $key eq '' )
    {
	$key = sprintf( "%d", $gLinkNum );
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
    qq[<label for="$label" accesskey="$accessKey">$markUp] . &TagAccessKey( $accessKey ) . "</label>";
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
	qq(<input type="reset" value="$value" accesskey="$key" tabindex="$gTabIndex">);
    }
    else
    {
	qq(<input type="submit" value="$value" accesskey="$key" tabindex="$gTabIndex">);
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
    qq(<input type="$type" id="$id" name="$id" value="$value" size="$size" tabindex="$gTabIndex">);
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
	qq(<input type="checkbox" id="$id" name="$id" value="on" tabindex="$gTabIndex" checked>);
    }
    else
    {
	qq(<input type="checkbox" id="$id" name="$id" value="$value" tabindex="$gTabIndex">);
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
	qq(<input type="radio" id="$id" name="$name" value="$value" tabindex="$gTabIndex" checked>);
    }
    else
    {
	qq(<input type="radio" id="$id" name="$name" value="$value" tabindex="$gTabIndex">);
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
    $comm .= "&kinoA=3&kinoU=$UNAME&kinoP=$PASSWD" if ( $SYS_AUTH == 3 );
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
    foreach ( split(/,/, $DB_AIDS{$Id} ))
    {
	push( @Return, $_ );
	push( @Return, &CollectDaughters( $_ )) if ( $DB_AIDS{$_} ne '' );
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
    local( $old ) = $#DB_ID - int( $id + $DEF_TITLE_NUM/2 );
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
}

sub UnlockAll
{
    &cgi'unlock_file( $LOCK_FILE ) unless $PC;
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

    $ExtHeader = "X-Kb-System: $SYSTEM_NAME\n";
    if (( ! $SYS_MAILHEADBRACKET ) && $BOARDNAME && ($Id ne '' ))
    {
	$ExtHeader .= "X-Kb-Board: $BOARDNAME\nX-Kb-Articleid: $Id\n";
    }

    # 引用記事
    if ( $Id ne '' ) {
	$Message .= "\n--------------------\n";
	&GetArticleBody($Id, $BOARD, *ArticleBody);
	foreach ( @ArticleBody )
	{
	    s/<[^>]*>//go;	# タグは要らない
	    $Message .= &HTMLDecode( $_ ) if ( $_ ne '' );
	}
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
	&UnlockBoard();
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
    elsif ( $errno == 6)
    {
	$severity = $kinologue'SEV_INFO;
	$msg = "「$errInfo」という$H_FROMは使えません．戻って別の$H_FROMを指定してください．";
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
	$msg .= "大変お手数ですが，このメッセージ全文のコピーと，エラーが生じた状況を，" . &TagA( $MAINT, "mailto:$MAINT" ) . "までお知らせ頂けると助かります．";
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
	$DB_DATE{$dId} = $dDate || &GetModifiedTime($dId, $Board);
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
## GetArticlesInfo - 記事DBの読み込み
#
# - SYNOPSIS
#	GetArticlesInfo($Id);
#
# - ARGS
#	$Id	記事ID
#
# - DESCRIPTION
#	記事DBを読み込んで，情報を取り出す．
#	実際はキャッシュから読み出すだけ．
#
# - RETURN
#	記事情報のリスト
#		リプライ元記事ID
#		この記事にリプライした記事のIDのリスト(「,」区切り)
#		投稿時間(UTC)
#		Subject
#		アイコンID
#		投稿ホスト
#		投稿者名
#		投稿者E-Mail
#		投稿者URL
#		リプライがあった時に投稿者にメイルを送るか否か
#
sub GetArticlesInfo
{
    local( $Id ) = @_;
    ( $DB_FID{$Id}, $DB_AIDS{$Id}, $DB_DATE{$Id}, $DB_TITLE{$Id}, $DB_ICON{$Id}, $DB_REMOTEHOST{$Id}, $DB_NAME{$Id}, $DB_EMAIL{$Id}, $DB_URL{$Id}, $DB_FMAIL{$Id} );
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

    local( $dId, $dFid, $dAids, $dInputDate, $dSubject, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail, $mdName, $mdEmail, $mdInputDate, $mdSubject, $mdIcon, $mdId, $FidList, $FFid, @FollowMailTo, @FFid, @ArriveMail );

    # リプライ元のリプライ元，を取ってくる
    if ( $Fid ne '' )
    {
	( $FFid ) = &GetArticlesInfo( $Fid );
	@FFid = split( /,/, $FFid );
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
		push( @FollowMailTo, $dEmail ) if $dFmail;
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
	&GetArriveMailTo( 0, $Board, *ArriveMail );
	&ArriveMail( $Name, $Email, $Subject, $Icon, $Id, @ArriveMail ) if @ArriveMail;
    }

    # 必要なら反応があったことをメイルする
    if ( $MailRelay && ( $SYS_MAIL & 2 ) && @FollowMailTo )
    {
	&FollowMail( $mdName, $mdEmail, $mdInputDate, $mdSubject, $mdIcon, $mdId, $Name, $Email, $Subject, $Icon, $Id, @FollowMailTo );
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

    # スタイルシートファイルの作成（コピー）
    $src = &GetPath( $BOARDSRC_DIR, $CSS_FILE );
    $dest = &GetPath( $name, $CSS_FILE );
    &CopyDb( $src, $dest ) || &Fatal( 20, "$src -&gt; $dest" );

    # 自動送信メイルDBの作成
    &UpdateArriveMailDb( $name, *arriveMail );

    # ヘッダファイルの作成
    &UpdateHeaderDb( $name, *header );

    # 最後に，掲示板DBを更新する
    local( $file ) = $BOARD_FILE;
    local( $tmpFile ) = "$BOARD_FILE.$TMPFILE_SUFFIX$$";
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

    local( $file ) = $BOARD_FILE;
    local( $tmpFile ) = "$BOARD_FILE.$TMPFILE_SUFFIX$$";
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
    &UpdateArriveMailDb( $board, *arriveMail );

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
    local( $dbFile ) = $BOARD_FILE;
    open( DB, "<$dbFile" ) || &Fatal( 1, $dbFile );
    while ( <DB> )
    {
	next if ( /^\#/o || /^$/o );
	chop;
	( $bId, $bName, $bInfo ) = split( /\t/, $_, 3 );
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
#	掲示板名
#
sub GetBoardInfo
{
    local( $board ) = @_;

    local( $dBoard, $dBoardName, $dBoardConf );

    local( $dbFile ) = $BOARD_FILE;
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
    return if ( $gIconDbCached eq $board );

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

    $gIconDbCached = $board;		# cached
}


###
## GetBoardHeader - 掲示板ヘッダDBの読み込み
#
# - SYNOPSIS
#	GetBoardHeader($Board, *BoardHeader);
#
# - ARGS
#	$BoardId	掲示板ID
#	*BoardHeader	本文各行を入れる文字列へのリファレンス
#
# - DESCRIPTION
#	掲示板ディレクトリの中の，掲示板ヘッダファイルを読み出す．
#
sub GetBoardHeader
{
    local( $Board, *BoardHeader ) = @_;

    local( $File ) = &GetPath( $Board, $HEADER_FILE_NAME );
    open( HEADER, "<$File" ) || &Fatal( 1, $File );
    while ( <HEADER> )
    {
	s/__PROGRAM__/$PROGRAM/go;
	s/__BOARD__/$Board/go;
	s/__TITLE_NUM__/$DEF_TITLE_NUM/go;
	s/__ARTICLE_NUM__/$DEF_ARTICLE_NUM/go;
	$BoardHeader .= $_;
    }
    close HEADER;
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
## GetIconUrlFromTitle - アイコンgifのURLの取得
#
# - SYNOPSIS
#	GetIconUrlFromTitle($Icon, $Board);
#
# - ARGS
#	$icon		アイコンID
#	$board		掲示板ID
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
    local( $icon, $board ) = @_;
    return $ICON_NEW if ( $icon eq $H_NEWARTICLE );

    # prepare
    &CacheIconDb( $board );

    # check
    return '' unless $ICON_FILE{ $icon };

    # return
    "$ICON_DIR/" . $ICON_FILE{$icon};
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
