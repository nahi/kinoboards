#!/usr/local/bin/perl


# このファイルの変更は最低2箇所，最大4箇所です（環境次第です）．


# 1. このファイルの先頭行（↑）で，Perlのパスを指定します．
#    「#!」に続けて指定してください．

# 2. kbdataディレクトリのフルパスを指定してください（URLではなく，パスです）．
#    ブラウザからアクセス可能なディレクトリでなくてもかまいません．
#
$KBDIR_PATH = '/home/achilles/nakahiro/cvs_work/KB/tst/';
# $KBDIR_PATH = '/home/nahi/kbdata/';
# $KBDIR_PATH = 'd:\securedata\kbdata\';	# WinNT/Win9xの場合
# $KBDIR_PATH = 'foo:bar:kb:';			# Macの場合?

# 3. サーバが動いているマシンがWin95/Macの場合，
#    $PCを1に設定してください．そうでない場合，この設定は不要です．
#
$PC = 0;	# for UNIX / WinNT
# $PC = 1;	# for Win95 / Mac

# 4. アイコンおよびスタイルシートファイルを，このファイルと別のディレクトリに
#    置く場合は，その別ディレクトリのURLを指定してください（パスではなく，
#    URLです）．指定するURLは，ブラウザからアクセス可能でなければいけません．
#    本ファイルと同じディレクトリにicon，styleディレクトリを置く場合は，
#    特に指定しなくてもかまいません（このまま書き換えなくて構いません）．
#
#    指定したURL以下に置かれている，
#      icon/*がアイコンファイルとして，
#      style/kbStyle.cssがスタイルシートファイルとして，
#    それぞれ参照されます．
#
# $KB_RESOURCE_URL = '/~nahi/kb/';


# 以下は書き換えの必要はありません．


######################################################################


# $Id: kb.cgi,v 5.73 2000-05-05 06:01:37 nakahiro Exp $

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
$KB_RELEASE = '7.0';		# release
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
$RESOURCE_IMG = 'img';			# イメージディレクトリ
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
$H_TOP = '最新';
$H_BOTTOM = '先頭';
$H_UP = '次';
$H_DOWN = '前';
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
$ICON_UP = &getIconURL( 'org_tlist.gif' );		# 上へ
$ICON_UP_X = &getIconURL( 'org_tlist_x.gif' );		# 上へ
$ICON_PREV = &getIconURL( 'org_prev.gif' );		# 前へ
$ICON_PREV_X = &getIconURL( 'org_prev_x.gif' );		# 前へ
$ICON_NEXT = &getIconURL( 'org_next.gif' );		# 次へ
$ICON_NEXT_X = &getIconURL( 'org_next_x.gif' );		# 次へ
$ICON_DOWN = &getIconURL( 'org_thread.gif' );		# 下へ
$ICON_DOWN_X = &getIconURL( 'org_thread_x.gif' );	# 下へ
$ICON_FOLLOW = &getIconURL( 'org_follow.gif' );		# リプライ
$ICON_FOLLOW_X = &getIconURL( 'org_follow_x.gif' );	# リプライ
$ICON_QUOTE = &getIconURL( 'org_quote.gif' );		# 引用してリプライ
$ICON_QUOTE_X = &getIconURL( 'org_quote_x.gif' );	# 引用してリプライ
$ICON_SUPERSEDE = &getIconURL( 'org_supersede.gif' );	# 訂正
$ICON_SUPERSEDE_X = &getIconURL( 'org_supersede_x.gif' );	# 訂正
$ICON_DELETE = &getIconURL( 'org_delete.gif' );		# 削除
$ICON_DELETE_X = &getIconURL( 'org_delete_x.gif' );	# 削除
$ICON_HELP = &getIconURL( 'org_help.gif' );		# ヘルプ
$ICON_NEW = &getIconURL( 'org_listnew.gif' );		# 新着

# 改行タグ，水平線タグ
$HTML_BR = "<br />\n";
$HTML_HR = "<hr />\n";

# ローカルカウンタ・フラグ
$gLinkNum = 0;
$gTabIndex = 0;

$gDumpedHTTPHeader = 0;

# シグナルハンドラ
$SIG{'QUIT'} = 'IGNORE';
$SIG{'INT'} = $SIG{'HUP'} = $SIG{'TERM'} = $SIG{'TSTP'} = 'doKill';


######################################################################


###
## maiN - メインブロック
#
# - SYNOPSIS
#	kb.cgi
#
# - DESCRIPTION
#	起動時に一度だけ参照される．
#	引き数はないが，環境変数QUERY_STRINGとREQUEST_METHOD，
#	もしくは標準入力経由で値を渡さないと，正しく動作しない．
#
&kbLog( $kinologue'SEV_INFO, 'Exec started.' );
MAIN:
{
    &cgi'decode();

    if ( $kinologue'SEV_THRESHOLD == $kinologue'SEV_DEBUG )
    {
	local( $key, $value, $msg );
	while (( $key, $value ) = each %cgi'TAGS )
	{
	    $msg .= '&' if $msg;
	    $msg .= "$key=$value";
	}
	&kbLog( $kinologue'SEV_DEBUG, "Command executed with ... " . $msg );
    }

    # HEADリクエストに対する特別処理
    if ( $ENV{ 'REQUEST_METHOD' } eq 'HEAD' )
    {
	local( $modTime ) = 0;
	if ( &cgi'tag( 'b' ) ne '' )
	{
	    $modTime = &getBoardLastmod( scalar( &cgi'tag( 'b' )));
	}
	&cgi'header( 1, $modTime, 0, (), 0 );
	last;
    }

    local( $c ) = &cgi'tag( 'c' );
    local( $com ) = &cgi'tag( 'com' );
    local( $s ) = &cgi'tag( 's' );
    $BOARD = &cgi'tag( 'b' );
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

    # ロックしないでいいの?
    &cacheBoard();

    if ( $BOARD )
    {
	$BOARD_ESC = &uriEscape( $BOARD );	# リンク用にescape
	$BOARDNAME = &getBoardName( $BOARD );
	$LOCK_FILE_B = $LOCK_FILE . ".$BOARD";

	# 掲示板固有セッティングを読み込む
	if ( &getBoardInfo( $BOARD ))
	{
	    local( $boardConfFile ) = &getPath( $BOARD, $CONF_FILE_NAME );
	    require( $boardConfFile ) if ( -s "$boardConfFile" );
	}

	# アイコンDBも読み込む（R7以降）
	&cacheBoardIcon( $BOARD ) if $SYS_ICON;
    }

    # 全てのrequireが終わったあと．．．

    # 認証情報の初期化
    $cgiauth'GUEST = $GUEST;
    $cgiauth'ADMIN = $ADMIN;
    $USER_AUTH_FILE = &getPath( $SYS_DIR, $USER_FILE );

    # 一部システム設定の補正
    $SYS_EXPAND = $SYS_EXPAND && ( $SYS_THREAD_FORMAT != 2 );
    $POLICY = $GUEST_POLICY;	# Policy by default.

    if ( $SYS_AUTH )
    {
	$SYS_AUTH_DEFAULT = $SYS_AUTH;
	$SYS_AUTH = 3 if ( &cgi'tag( 'kinoA' ) == 3 );
	if ( $c eq 'lo' )
	{
	    # ログイン
	    &uiLogin();
	    last;
	}
	elsif ( $c eq 'ue' )
	{
	    # ユーザ新規登録
	    &uiUserEntry();
	    last;
	}
	elsif ( $c eq 'uex' )
	{
	    # ユーザ新規登録実施
	    &uiUserEntryExec();
	    last;
	}

	$cgiauth'AUTH_TYPE = $SYS_AUTH;
	&cgi'cookie() if ( $SYS_AUTH == 1 );
	    
	local( $err, @userInfo );
	( $err, $UNAME, $PASSWD, @userInfo ) = &cgiauth'checkUser( $USER_AUTH_FILE );
	    
	if ( $err == 3 )
	{
	    # ユーザ名がみつからない
	    # 本当は41だけどセキュリティ優先
	    &fatal( 40, scalar( &cgi'tag( 'kinoU' )));
	}
	elsif ( $err == 4 )
	{
	    # パスワードが間違っている
	    &fatal( 40, '' );
	}
	elsif ( $err == 9 )
	{
	    if ( $c eq 'acx' )
	    {
		# 管理者パスワード変更の実施
		&uiAdminConfigExec();
		last;
	    }
	    # 管理者パスワードが空の場合，ユーザを管理者扱いしてから．．．
	    $cgiauth'UID = $UNAME;
	    $cgiauth'PASSWD = $PASSWD;

	    # 管理者パスワード変更
	    &uiAdminConfig();
	    last;
	}
	elsif ( $err != 0 )
	{
	    # not reached...
	    &fatal( 998, "Must not reach here(MAIN: $err)." );
	}
	    
	# 認証成功
	$UNAME_ESC = &uriEscape( $UNAME ) if ( $SYS_AUTH == 3 );
	$UMAIL = $userInfo[2];
	$UURL = $userInfo[3];

	# user policyの決定
	#   1 ... 読み
	#   2 ... 書き
	#   4 ... 登録（ユーザ情報をサーバに残す）
	#   8 ... 管理
	if ( &isUser( $ADMIN ))
	{
	    # 管理者
	    $POLICY = 1 + 2 + 4 + 8;
	}
	elsif ( !&isUser( $GUEST ))
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
	    &uiShowArticle();
	    last;
	}
	elsif ( $c eq 't' )
	{
	    # フォロー記事を全て表示．
	    &uiShowThread();
	    last;
	}
	elsif ( $c eq 'v' )
	{
	    # スレッド別タイトル一覧
	    &uiThreadTitle( 0 );
	    last;
	}
	elsif ( $c eq 'vt' )
	{
	    # スレッド別タイトルおよび記事一覧
	    &uiThreadArticle();
	    last;
	}
	elsif ( $c eq 'r' )
	{
	    # 書き込み順にソート
	    &uiSortTitle();
	    last;
	}
	elsif ( $c eq 'l' )
	{
	    # 新しい記事を書き込み順に表示
	    &uiSortArticle();
	    last;
	}
	elsif ( $SYS_F_S && ( $c eq 's' ))
	{
	    # 記事の検索
	    &uiSearchArticle();
	    last;
	}
	elsif ( $SYS_ICON && ( $c eq 'i' ))
	{
	    # アイコン表示画面
	    &uiShowIcon();
	    last;
	}
	elsif ( $c eq 'h' )
	{
	    # ヘルプ画面
	    &uiHelp();
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
	    &cgi'setTag( 'c', scalar( &cgi'tag( 'corig' )));
	    $c = &cgi'tag( 'c' );
	}

	if ( $c eq 'n' )
	{
	    # 新規投稿
	    &uiPostNewEntry( $varBack );
	    last;
	}
	elsif ( !$s && ( $c eq 'f' ))
	{
	    # リプライ投稿
	    &uiPostReplyEntry( $varBack, 0 );
	    last;
	}
	elsif ( $c eq 'q' )
	{
	    # 引用リプライ投稿
	    &uiPostReplyEntry( $varBack, 1 );
	    last;
	}
	elsif ( !$s && ( $c eq 'p' ) && ( $com ne 'x' ))
	{
	    # 投稿プレビュー
	    &uiPostPreview( 0 );
	    last;
	}
	elsif ( !$s && ( $c eq 'p' ) && ( $com eq 'x' ))
	{
	    # 登録後画面の表示（直接）
	    &uiPostExec( 0 );
	    last;
	}
	elsif ( !$s && ( $c eq 'x' ) && ( $com eq 'x' ))
	{
	    # 登録後画面の表示（プレビュー経由）
	    &uiPostExec( 1 );
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
	    &uiUserConfig();
            last;
        }
        elsif ( $c eq 'ucx' )
        {
            # ユーザ情報設定の実施
	    &uiUserConfigExec();
	    last;
        }
	elsif ( $s && ( $c eq 'f' ))
	{
	    # 記事訂正
	    &uiSupersedeEntry( $varBack );
	    last;
	}
	elsif ( $s && ( $c eq 'p' ) && ( $com ne 'x' ))
	{
	    # 記事訂正プレビュー
	    &uiSupersedePreview( 0 );
	    last;
	}
	elsif ( $s && ( $c eq 'p' ) && ( $com eq 'x' ))
	{
	    # 記事訂正実施（直接）
	    &uiSupersedeExec( 0 );
	    last;
	}
	elsif ( $s && ( $c eq 'x' ) && ( $com eq 'x' ))
	{
	    # 記事訂正実施（プレビュー経由）
	    &uiSupersedeExec( 1 );
	    last;
	}
        elsif ( $c eq 'dp' )
        {
	    # 削除プレビュー
	    &uiDeletePreview();
	    last;
        }
        elsif ( $c eq 'de' )
        {
	    # 削除実施
            &uiDeleteExec( 0 );
	    last;
	}
        elsif ($c eq 'det' )
        {
	    # 削除実施（リプライも）
            &uiDeleteExec( 1 );
	    last;
        }
    }

    # 管理系
    if ( $POLICY & 8 )
    {
	if ( $c eq 'ct' )
	{
	    &uiThreadTitle( 2 );
	    last;
	}
	elsif ( $c eq 'ce' )
	{
	    &uiThreadTitle( 3 );
	    last;
	}
	elsif ( $c eq 'mvt' )
	{
	    &uiThreadTitle( 4 );
	    last;
	}
	elsif ( $c eq 'mve' )
	{
	    &uiThreadTitle( 5 );
	    last;
	}
        elsif ( $c eq 'bc' )
        {
            # 掲示板設定
	    &uiBoardConfig();
            last;
        }
        elsif ( $c eq 'bcx' )
        {
	    # 掲示板設定の実施
	    &uiBoardConfigExec();
	    last;
        }
        elsif ( $c eq 'be' )
        {
            # 掲示板新設
            &uiBoardEntry();
            last;
        }
        elsif ( $c eq 'bex' )
        {
	    # 掲示板新設の実施
	    &uiBoardEntryExec();
	    last;
        }
    }

    if ( $c eq 'bl' )
    {
	# 掲示板一覧の表示
	&uiBoardList();
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
		do( &getPath( $UI_DIR, 'Post.pl' ));
		last;
	    }
	    elsif ( $c eq 'POST_IF' )
	    {
		*gVarBody = *body;
		$gVarForce = 0;
		do( &getPath( $UI_DIR, 'Post.pl' ));
		last;
	    }
	}
    }

    # どのコマンドでもない．エラー．
    &fatal( 99, $c );
}
&kbLog( $kinologue'SEV_INFO, 'Exec finished.' );
exit( 0 );


######################################################################
# ベースインプリメンテーション


###
## doKill - システムのシャットダウン
#
# - SYNOPSIS
#	&doKill();
#
# - DESCRIPTION
#	必要な処理を行なった後，システムのシャットダウンを行なう．
#	ロックの解除およびログファイルへの書き出しを行なう．
#
sub doKill
{
    local( $sig ) = @_;
    if ( !$PC )
    {
	&cgi'unlock_file( $LOCK_FILE );
	&cgi'unlock_file( $LOCK_FILE_B ) if $LOCK_FILE_B;
    }
    &kbLog( $kinologue'SEV_WARN, "Caught a SIG$sig - shutting down..." );
    exit( 1 );
}


###
## lockAll/unlockAll - システムのロック/アンロック
## lockBoard/unlockBoard - 掲示板のロック/アンロック
#
# - SYNOPSIS
#	&lockAll();
#	&unlockAll();
#	&lockBoard();
#	&unlockBoard();
#
# - DESCRIPTION
#	システム/掲示板をロック/アンロックする．
#	ロックに使うファイルは$LOCK_FILE/$LOCK_FILE_B．
#
# - RETURN
#	なし．戻れば成功．失敗すればエラーページへ．
#
sub LockAll { &lockAll; }
sub lockAll
{
    local( $lockResult ) = $PC ? 1 : &cgi'lock_file( $LOCK_FILE );
    &fatal( 1001, '' ) if ( $lockResult == 2 );
    &fatal( 999, '' ) if ( $lockResult != 1 );
    &lockBoard() if $LOCK_FILE_B;
}

sub UnlockAll { &unlockAll; }
sub unlockAll
{
    &cgi'unlock_file( $LOCK_FILE ) unless $PC;
    &unlockBoard() if $LOCK_FILE_B;
}

sub LockBoard { &lockBoard; }
sub lockBoard
{
    local( $lockResult ) = $PC ? 1 : &cgi'lock_file( $LOCK_FILE_B );
    &fatal( 1001, '' ) if ( $lockResult == 2 );
    &fatal( 999, '' ) if ( $lockResult != 1 );
}

sub UnlockBoard { &unlockBoard; }
sub unlockBoard
{
    &cgi'unlock_file( $LOCK_FILE_B ) unless $PC;
}


###
## fatal - エラー処理
#
# - SYNOPSIS
#	&fatal( $errno, $errInfo );
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
sub fatal
{
    local( $errno, $errInfo ) = @_;

    local( $severity, $msg ) = &fatalStr( $errno, $errInfo );

    # 異常終了の可能性があるので，とりあえずlockを外す
    # (ロックの失敗の時以外)
    if ( !$PC && ( $errno != 999 ) && ( $errno != 1001 ))
    {
	&unlockAll();
    }

    # log a log(except logging failure).
    &kbLog( $severity, $msg ) if ( $errno != 1000 );
    &uiFatal( $msg );
    &kbLog( $kinologue'SEV_INFO, 'Exec finished.' ) if ( $errno != 1000 );
    exit( 0 );
}


###
## fatalStr - エラーコードから重要度とエラーメッセージを取得
#        
# - SYNOPSIS
#	&fatalStr( $errno, $errInfo );
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
sub fatalStr
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
	$msg = "$H_PASSWDを間違えていませんか? $H_FROMと$H_PASSWDを確認し，戻ってやり直してみてください．" . &linkP( "c=lo", "ユーザ設定の呼び出し" . &tagAccessKey( 'L' ), 'L' );
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
	$msg .= "大変お手数ですが，このページのURL（" . $cgi'REQUEST_URI . "），このメッセージ全文のコピーと，エラーが生じた状況を，" . &tagA( $MAINT, "mailto:$MAINT" ) . "までお知らせ頂けると助かります．";
    }

    return ( $severity, $msg );
}


###
## kbLog - ログ処理
#
# - SYNOPSIS
#	&kbLog( $kinologue'severity, *msg );
#
# - ARGS
#	$kinologue'severity	severity id defined in kinologue.pl.
#	*msg			reference to msg string.
#
# - DESCRIPTION
#	log a log using kinologue.
#	exit program(not function) if failed to write log.
#
sub KbLog { &kbLog; }
sub kbLog
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
	    || &fatal( 1000, '' );
    }
}


######################################################################
# ユーザインタフェイスインプリメンテーション


###
## htmlGen - HTML generator from source file
#
# - SYNOPSIS
#	&htmlGen( $source );
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

    local( $file ) = &getPath( $UI_DIR, $source );

    open( SRC, "<$file" ) || &fatal( 1, $file );

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
    &cgiauth'header( 0, 0, 1, $cookieExpire ) unless $gDumpedHTTPHeader;
    $gDumpedHTTPHeader = 1;
    &cgiprint'init();

    $gHgStr = '';

    # Workaround for MSIE 4.5(Macintosh IE).
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
			&fatal( 998, "$file : $@" );
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
    &cgiprint'cache( $gHgStr );

    &cgiprint'flush();
}


###
## サインオン画面
#
sub uiLogin
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
    &fatal( 18, "$_[0]/LoginForm" ) if ( $_[0] ne 'Login.xml' );

    local( %tags, $msg );
    $msg = &tagLabel( $H_FROM, 'kinoU', 'N' ) . ': ' . &tagInputText( 'text', 'kinoU', '', $NAME_LENGTH ) . $HTML_BR;
    $msg .= &tagLabel( $H_PASSWD, 'kinoP', 'P' ) . ': ' . &tagInputText( 'password', 'kinoP', '', $PASSWD_LENGTH ) . $HTML_BR;
    if ( $SYS_AUTH_DEFAULT == 1 )
    {
	local( $contents );
	$contents = &tagInputRadio( 'kinoA_url', 'kinoA', '3', 0 ) . ":\n" .
	    &tagLabel( 'クッキー(HTTP-Cookies)を使わずに認証する', 'kinoA_url', 'U' ) . $HTML_BR;
	$contents .= &tagInputRadio( 'kinoA_cookies', 'kinoA', '1', 1 ) . "\n" .
	    &tagLabel( 'クッキーを使ってこのブラウザに情報を覚えさせる', 'kinoA_cookies', 'C' ) . $HTML_BR;
	$msg .= &tagFieldset( "クッキー:$HTML_BR", $contents );
    }

    %tags = ( 'c', 'bl', 'kinoT', 'plain' );
    &dumpForm( *tags, '実行', 'リセット', *msg, 1 );
}


###
## 管理者パスワードの設定画面
#
sub uiAdminConfig
{
    # Isolation level: CHAOS.
    &htmlGen( 'AdminConfig.xml' );
}

sub hg_admin_config_form
{
    &fatal( 18, "$_[0]/AdminConfigForm" ) if ( $_[0] ne 'AdminConfig.xml' );

    local( %tags, $msg );
    $msg = &tagLabel( $H_PASSWD, 'confP', 'P' ) . ': ' .
	&tagInputText( 'password', 'confP', '', $PASSWD_LENGTH ) . $HTML_BR;
    $msg .= &tagLabel( $H_PASSWD, 'confP2', 'C' ) . ': ' .
	&tagInputText( 'password', 'confP2', '', $PASSWD_LENGTH ) .
	'（念のため，もう一度お願いします）' . $HTML_BR;
    %tags = ( 'c', 'acx' );
    &dumpForm( *tags, '設定', 'リセット', *msg, 1 );
}


###
## 管理者パスワード設定の実施
#
sub uiAdminConfigExec
{
    # Isolation level: SERIALIZABLE.
    &lockAll();

    local( $p1 ) = &cgi'tag( 'confP' );
    local( $p2 ) = &cgi'tag( 'confP2' );

    # adminのみ
    &fatal( 44, '' ) unless &isUser( $ADMIN );

    if ( !$p2 || ( $p1 ne $p2 ))
    {
	&fatal( 42, $H_PASSWD );
    }
    
    if ( !&cgiauth'setUserPasswd( $USER_AUTH_FILE , $ADMIN, $p1 ))
    {
	&fatal( 41, $ADMIN );
    }

    &unlockAll();

    # ユーザ情報をクリア
    &uiLogin();
}


###
## ユーザ登録画面
#
sub uiUserEntry
{
    # Isolation level: CHAOS.

    # ユーザ情報をクリア
    $UNAME = $cgiauth'F_COOKIE_RESET if ( $SYS_AUTH == 1 );
    &htmlGen( 'UserEntry.xml' );
}

sub hg_user_entry_form
{
    &fatal( 18, "$_[0]/UserEntryForm" ) if ( $_[0] ne 'UserEntry.xml' );

    local( %tags, $msg );
    $msg = &tagLabel( $H_FROM, 'kinoU', 'N' ) . ': ' .
	&tagInputText( 'text', 'kinoU', '', $NAME_LENGTH ) . $HTML_BR;
    $msg .= &tagLabel( $H_MAIL, 'mail', 'M' ) . ': ' .
	&tagInputText( 'text', 'mail', '', $MAIL_LENGTH ) . $HTML_BR;
    $msg .= &tagLabel( $H_PASSWD, 'kinoP', 'P' ) . ': ' .
	&tagInputText( 'password', 'kinoP', '', $PASSWD_LENGTH ) . $HTML_BR;
    $msg .= &tagLabel( $H_PASSWD, 'kinoP2', 'C' ) . ': ' .
	&tagInputText( 'password', 'kinoP2', '', $PASSWD_LENGTH ) .
	'（念のため，もう一度お願いします）' . $HTML_BR;
    $msg .= &tagLabel( $H_URL, 'url', 'U' ) . ': ' .
	&tagInputText( 'text', 'url', 'http://', $URL_LENGTH ) .
	'（省略してもかまいません）' . $HTML_BR;

    %tags = ( 'c', 'uex' );
    &dumpForm( *tags, '登録', 'リセット', *msg, 1 );
}


###
## ユーザ登録の実施
#
sub uiUserEntryExec
{
    # Isolation level: SERIALIZABLE.
    &lockAll();

    local( $user ) = &cgi'tag( 'kinoU' );
    local( $p1 ) = &cgi'tag( 'kinoP' );
    local( $p2 ) = &cgi'tag( 'kinoP2' );
    local( $mail ) = &cgi'tag( 'mail' );
    local( $url ) = &cgi'tag( 'url' );

    &checkName( *user );
    &checkEmail( *mail );
    &checkURL( *url );
    &checkPasswd( *p1 );

    if ( !$p2 || ( $p1 ne $p2 ))
    {
	&fatal( 42, $H_PASSWD );
    }
	    
    # 登録済みユーザの検索
    if ( $SYS_POSTERMAIL && &cgiauth'searchUserInfo( $USER_AUTH_FILE, $mail, undef ))
    {
	&fatal( 6, $mail );
    }

    # 新規登録する
    local( $res ) = &cgiauth'addUser( $USER_AUTH_FILE, $user, $p1, $mail, $url );

    if ( $res == 1 )
    {
	&fatal( 5, $user );
    }
    elsif ( $res == 2 )
    {
	&fatal( 998, 'Must not reach here(UserEntryExec).' );
    }

    &unlockAll();

    # ログイン画面へ
    &uiLogin();
}


###
## ユーザ設定変更
#
sub uiUserConfig
{
    # Isolation level: CHAOS.

    &htmlGen( 'UserConfig.xml' );
}

sub hg_user_config_form
{
    &fatal( 18, "$_[0]/UserConfigForm" ) if ( $_[0] ne 'UserConfig.xml' );

    if ( $POLICY & 8 )
    {
	local( %tags, $msg );
	$msg .= &tagLabel( "変更する$H_USERの$H_FROM", 'confUser', 'N' ) .
	    ': ' . &tagInputText( 'text', 'confUser', '', $NAME_LENGTH ) .
	    "（管理者は全$H_USERの設定を変更できます）" . $HTML_BR . $HTML_BR;
	$msg .= &tagLabel( $H_MAIL, 'confMail', 'M' ) . ': ' .
	    &tagInputText( 'text', 'confMail', '', $MAIL_LENGTH ) . $HTML_BR;
	$msg .= &tagLabel( $H_URL, 'confUrl', 'U' ) . ': ' .
	    &tagInputText( 'text', 'confUrl', 'http://', $URL_LENGTH ) . $HTML_BR . $HTML_BR;
	$msg .= &tagLabel( $H_PASSWD, 'confP', 'P' ) . ': ' .
	    &tagInputText( 'password', 'confP', '', $PASSWD_LENGTH ) . $HTML_BR;
	$msg .= &tagLabel( $H_PASSWD, 'confP2', 'C' ) . ': ' .
	    &tagInputText( 'password', 'confP2', '', $PASSWD_LENGTH ) .
	    '（念のため，もう一度お願いします）' . $HTML_BR;
	%tags = ( 'c', 'ucx' );
	&dumpForm( *tags, '設定', 'リセット', *msg );
    }
    else
    {
	$UURL = $UURL || 'http://';

	local( %tags, $msg );
	$msg .= $H_FROM . ': ' . $UNAME . $HTML_BR . $HTML_BR;
	$msg .= &tagLabel( $H_MAIL, 'confMail', 'M' ) . ': ' .
	    &tagInputText( 'text', 'confMail', $UMAIL, $MAIL_LENGTH ) . $HTML_BR;
	$msg .= &tagLabel( $H_URL, 'confUrl', 'U' ) . ': ' .
	    &tagInputText( 'text', 'confUrl', $UURL, $URL_LENGTH ) . $HTML_BR . $HTML_BR;
	$msg .= &tagLabel( $H_PASSWD, 'confP', 'P' ) . ': ' .
	    &tagInputText( 'password', 'confP', '' , $PASSWD_LENGTH ) . $HTML_BR;
	$msg .= &tagLabel( $H_PASSWD, 'confP2', 'C' ) . ': ' .
	    &tagInputText( 'password', 'confP2', '', $PASSWD_LENGTH ) .
	    '（念のため，もう一度お願いします）' . $HTML_BR;
	%tags = ( 'c', 'ucx' );
	&dumpForm( *tags, '設定', 'リセット', *msg );
    }
}


###
## ユーザ設定の実施
#
sub uiUserConfigExec
{
    # Isolation level: SERIALIZABLE.
    &lockAll();

    local( $p1 ) = &cgi'tag( 'confP' );
    local( $p2 ) = &cgi'tag( 'confP2' );
    local( $user ) = &cgi'tag( 'confUser' );
    local( $mail ) = &cgi'tag( 'confMail' );
    local( $url ) = &cgi'tag( 'confUrl' );

    $user = $UNAME unless ( $POLICY & 8 );

    &checkName( *user );
    &checkEmail( *mail );
    &checkURL( *url );
		
    # （必要なら）パスワード変更
    if ( $p1 || $p2 )
    {
	&checkPasswd( *p1 );

	if ( !$p2 || ( $p1 ne $p2 ))
	{
	    &fatal( 42, $H_PASSWD );
	}

	if ( !&cgiauth'setUserPasswd( $USER_AUTH_FILE, $user, $p1 ))
	{
	    &fatal( 41, $user );
	}
    }

    # ユーザ情報更新
    if ( !&cgiauth'setUserInfo( $USER_AUTH_FILE, $user, ( $mail, $url )))
    {
	&fatal( 41, '' );
    }

    &unlockAll();

    &uiBoardList();
}


###
## 掲示板登録画面
#
sub uiBoardEntry
{
    # Isolation level: CHAOS.

    &htmlGen( 'BoardEntry.xml' );
}

sub hg_board_entry_form
{
    &fatal( 18, "$_[0]/BoardEntryForm" ) if ( $_[0] ne 'BoardEntry.xml' );

    local( %tags, $msg );
    $msg = &tagLabel( "$H_BOARD略称", 'name', 'B' ) . ': ' .
	&tagInputText( 'text', 'name', '', $BOARDNAME_LENGTH ) . $HTML_BR;
    $msg .= &tagLabel( "$H_BOARD名称", 'intro', 'N' ) . ': ' .
	&tagInputText( 'text', 'intro', '', $BOARDNAME_LENGTH ) . $HTML_BR . $HTML_BR;
    $msg .= &tagLabel( "$H_BOARDの自動$H_MAIL配信先", 'armail', 'M' ) .
	$HTML_BR . &tagTextarea( 'armail', '', $TEXT_ROWS, $MAIL_LENGTH ) .
	$HTML_BR . $HTML_BR;
    $msg .= &tagLabel( "$H_BOARDヘッダ部分", 'article', 'H' ) . $HTML_BR .
	&tagTextarea( 'article', '', $TEXT_ROWS, $TEXT_COLS ) . $HTML_BR;
    %tags = ( 'c', 'bex' );
    &dumpForm( *tags, '登録', 'リセット', *msg );
}


###
## 掲示板登録の実施
#
sub uiBoardEntryExec
{
    # Isolation level: SERIALIZABLE.
    &lockAll();

    local( $name ) = &cgi'tag( 'name' );
    local( $intro ) = &cgi'tag( 'intro' );
    local( $armail ) = &cgi'tag( 'armail' );
    local( $header ) = &cgi'tag( 'article' );

    &checkBoardDir( *name );
    &checkBoardName( *intro );
    &checkBoardHeader( *header );
    &secureSubject( *intro );
    &secureArticle( *header, $H_TTLABEL[2] );
    local( @arriveMail ) = split( /\n/, $armail );

    &insertBoard( $name, $intro, 0, *arriveMail, *header );

    &unlockAll();

    &uiBoardList();
}


###
## 掲示板設定変更画面
#
sub uiBoardConfig
{
    # Isolation level: SERIALIZABLE.
    &lockAll();

    # 全掲示板の情報を取り出す
    @gArriveMail = ();
    &getBoardSubscriber(1, $BOARD, *gArriveMail); # 宛先とコメントを取り出す
    $gHeader = "";
    &getBoardHeader( $BOARD, *gHeader ); # ヘッダ文字列を取り出す

    &htmlGen( 'BoardConfig.xml' );

    &unlockAll();
}

sub hg_board_config_form
{
    &fatal( 18, "$_[0]/BoardConfigForm" ) if ( $_[0] ne 'BoardConfig.xml' );

    local( %tags, $msg );
    $msg = &tagLabel( "「$BOARD」$H_BOARDを利用", 'valid', 'V' ) . ': ' .
	&tagInputCheck( 'valid', 1 ) . $HTML_BR . $HTML_BR;
    $msg .= &tagLabel( "「$BOARD」名称", 'intro', 'N' ) . ': ' .
	&tagInputText( 'text', 'intro', $BOARDNAME, $BOARDNAME_LENGTH ) .
	$HTML_BR . $HTML_BR;
    local( $all );
    foreach ( @gArriveMail ) { $all .= $_ . "\n"; }
    $msg .= &tagLabel( "「$BOARD」の自動$H_MAIL配信先", 'armail', 'M' ) .
	$HTML_BR . &tagTextarea( 'armail', $all, $TEXT_ROWS, $MAIL_LENGTH ) .
	$HTML_BR . $HTML_BR;
    $msg .= &tagLabel( "「$BOARD」の$H_BOARDヘッダ部分", 'article', 'H' ) .
	$HTML_BR . &tagTextarea( 'article', $gHeader, $TEXT_ROWS, $TEXT_COLS ) . $HTML_BR;
    %tags = ( 'c', 'bcx', 'b', $BOARD );
    &dumpForm( *tags, '変更', 'リセット', *msg );
}


###
## 掲示板設定の実施
#
sub uiBoardConfigExec
{
    # Isolation level: SERIALIZABLE.
    &lockAll();

    local( $valid ) = &cgi'tag( 'valid' );
    local( $intro ) = &cgi'tag( 'intro' );
    local( $armail ) = &cgi'tag( 'armail' );
    local( $header ) = &cgi'tag( 'article' );

    &checkBoardName( *intro );
    &checkBoardHeader( *header );
    &secureSubject( *intro );
    &secureArticle( *header, $H_TTLABEL[2] );
    local( @arriveMail ) = split( /\n/, $armail );

    &updateBoard( $BOARD, $valid, $intro, 0, *arriveMail, *header );

    &unlockAll();

    &uiBoardList();
}


###
## 掲示板一覧
#
sub uiBoardList
{
    # Isolation level: CHAOS.

    &htmlGen( 'BoardList.xml' );
}


###
## メッセージ新規登録のエントリ
## リプライメッセージ登録のエントリ
## メッセージ訂正のエントリ
#
sub uiPostNewEntry
{
    # Isolation level: CHAOS.

    if ( $SYS_NEWART_ADMINONLY && !( $POLICY & 8 ))
    {
	&fatal( 99, scalar( &cgi'tag( 'c' )));
    }

    local( $back ) = @_;

    $gId = '';			# 0ではダメ．そういうファイル名もあるかも．
    $gDefPostDateStr = &cgi'tag( 'postdate' );
    $gDefSubject = &cgi'tag( 'subject' );
    $gDefName = &cgi'tag( 'name' );
    $gDefEmail = &cgi'tag( 'mail' );
    $gDefUrl = &cgi'tag( 'url' );
    $gDefTextType = &cgi'tag( 'texttype' );
    $gDefIcon = &cgi'tag( 'icon' );
    $gDefArticle = &cgi'tag( 'article' );
    $gDefFmail = &cgi'tag( 'fmail' );

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

sub uiPostReplyEntry
{
    # Isolation level: SERIALIZABLE.
    &lockBoard();
    &cacheArt( $BOARD );

    local( $back, $quoteFlag ) = @_;

    $gId = &cgi'tag( 'id' );
    $gDefPostDateStr = &cgi'tag( 'postdate' );
    $gDefSubject = &cgi'tag( 'subject' );
    $gDefName = &cgi'tag( 'name' );
    $gDefEmail = &cgi'tag( 'mail' );
    $gDefUrl = &cgi'tag( 'url' );
    $gDefTextType = &cgi'tag( 'texttype' );
    $gDefIcon = &cgi'tag( 'icon' );
    $gDefArticle = &cgi'tag( 'article' );
    $gDefFmail = &cgi'tag( 'fmail' );

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
	    $gDefSubject = &getArtSubject( $gId );
	    &getReplySubject( *gDefSubject );
	}
    }
    else
    {
	if ( $gDefSubject eq '' )
	{
	    local( $tmp );
	    $gDefSubject = &getArtSubject( $gId );
	    &getReplySubject( *gDefSubject );
	}
	&quoteOriginalArticle( $gId, *gDefArticle );
    }

    $gEntryType = 'reply';		# リプライ
    &htmlGen( 'PostReplyEntry.xml' );

    &unlockBoard();
}

sub uiSupersedeEntry
{
    # Isolation level: SERIALIZABLE.
    &lockBoard();
    &cacheArt( $BOARD );

    local( $back ) = @_;

    if ( !( $POLICY & 8 ) && ( $SYS_OVERWRITE == 0 ))
    {
	&fatal( 99, scalar( &cgi'tag( 'c' )));
    }

    $gId = &cgi'tag( 'id' );
    $gDefPostDateStr = &cgi'tag( 'postdate' );
    $gDefSubject = &cgi'tag( 'subject' );
    $gDefName = &cgi'tag( 'name' );
    $gDefEmail = &cgi'tag( 'mail' );
    $gDefUrl = &cgi'tag( 'url' );
    $gDefTextType = &cgi'tag( 'texttype' );	# 訂正時はXHTML入力のほうがいいかも 
    $gDefIcon = &cgi'tag( 'icon' );
    $gDefArticle = &cgi'tag( 'article' );
    $gDefFmail = &cgi'tag( 'fmail' );

    if ( $back )
    {
	require( 'mimer.pl' );
	$gDefSubject = &MIME'base64decode( $gDefSubject );
	$gDefArticle = &MIME'base64decode( $gDefArticle );
    }
    else
    {
	local( $tmp, $postDate );
	( $tmp, $tmp, $postDate, $gDefSubject, $gDefIcon, $tmp, $gDefName, $gDefEmail, $gDefUrl ) = &getArtInfo( $gId );
	$gDefPostDateStr = &getYYYY_MM_DD_HH_MM_SSFromUtc( $postDate );
	&quoteOriginalArticleWithoutQMark( $gId, *gDefArticle );
    }

    $gEntryType = 'supersede';		# 修正
    &htmlGen( 'SupersedeEntry.xml' );

    &unlockBoard();
}

sub hg_post_reply_entry_orig_article
{
    &fatal( 18, "$_[0]/PostReplyEntryOrigArticle" ) if ( $_[0] ne 'PostReplyEntry.xml' );
    &dumpArtBody( $gId, 0, 1 );
}

sub hg_supersede_entry_orig_article
{
    &fatal( 18, "$_[0]/SupersedeEntryOrigArticle" ) if ( $_[0] ne 'SupersedeEntry.xml' );
    &dumpArtBody( $gId, 0, 1 );
}


###
## メッセージ登録のプレビュー
## メッセージ訂正のプレビュー
#
sub uiPostPreview
{
    # Isolation level: SERIALIZABLE.
    &lockAll();
    &cacheArt( $BOARD );

    &uiPostPreviewMain( 'post' );
    &htmlGen( 'PostPreview.xml' );

    &unlockAll();
}

sub uiSupersedePreview
{
    # Isolation level: READ UNCOMITTED.
    &lockAll();
    &cacheArt( $BOARD );
    &unlockAll();

    if ( !( $POLICY & 8 ) && ( $SYS_OVERWRITE == 0 ))
    {
	&fatal( 99, scalar( &cgi'tag( 'c' )));
    }

    &uiPostPreviewMain( 'supersede' );
    &htmlGen( 'SupersedePreview.xml' );
}

sub uiPostPreviewMain
{
    local( $type ) = @_;

    # 入力された記事情報
    $gOrigId = &cgi'tag( 'id' );
    $gPostDateStr = &cgi'tag( 'postdate' );
    $gSubject = &cgi'tag( 'subject' );
    $gIcon = &cgi'tag( 'icon' );
    $gArticle = &cgi'tag( 'article' );
    $gTextType = &cgi'tag( 'texttype' );

    # 各種情報の取得
    if ( $POLICY & 8 )
    {
	if ( &cgi'tag( 'name' ) eq '' )
	{
	    $gName = $MAINT_NAME;
	    $gEmail = $MAINT;
	    $gUrl = $MAINT_URL;
	}
	else
	{
	    $gName = &cgi'tag( 'name' );
	    $gEmail = &cgi'tag( 'mail' );
	    $gUrl = &cgi'tag( 'url' );
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
	$gName = &cgi'tag( 'name' );
	$gEmail = &cgi'tag( 'mail' );
	$gUrl = &cgi'tag( 'url' );
    }

    $gEncSubject = &MIME'base64encode( $gSubject );
    $gEncArticle = &MIME'base64encode( $gArticle );

    &secureSubject( *gSubject );
    &secureArticle( *gArticle, $gTextType );

    local( $postDate ) = $^T;
    $postDate = &getUtcFromYYYY_MM_DD_HH_MM_SS( $gPostDateStr ) if ( $gPostDateStr ne '' );

    # 入力された記事情報のチェック
    &checkArticle( $BOARD, *postDate, *gName, *gEmail, *gUrl, *gSubject, *gIcon, *gArticle );
}

sub hg_post_preview_form
{
    &fatal( 18, "$_[0]/PostPreviewForm" ) if ( $_[0] ne 'PostPreview.xml' );

    require( 'mimer.pl' );

    local( $supersede ) = $_[1];

    local( %tags, $msg, $contents );
    $contents = &tagInputRadio( 'com_e', 'com', 'e', 0 ) . ":\n" . &tagLabel( '戻ってやりなおす', 'com_e', 'P' ) . $HTML_BR;
    $contents .= &tagInputRadio( 'com_x', 'com', 'x', 1 ) . "\n" . &tagLabel( '登録する', 'com_x', 'X' ) . $HTML_BR;
    $msg = &tagFieldset( "コマンド:$HTML_BR", $contents );
    %tags = ( 'corig', scalar( &cgi'tag( 'corig' )), 'c', 'x', 'b', $BOARD,
	     'id', $gOrigId, 'postdate', $gPostDateStr, 'texttype', $gTextType,
	     'name', $gName, 'mail', $gEmail, 'url', $gUrl, 'icon', $gIcon,
	     'subject', $gEncSubject, 'article', $gEncArticle,
	     'fmail', scalar( &cgi'tag( 'fmail' )), 's', $supersede,
	     'op', scalar( &cgi'tag( 'op' )));

    &dumpForm( *tags, '実行', '', *msg );
}

sub hg_supersede_preview_form
{
    &fatal( 18, "$_[0]/SupersedePreviewForm" ) if ( $_[0] ne 'SupersedePreview.xml' );
    &hg_post_preview_form( 'PostPreview.xml', 1 );
}

sub hg_post_preview_body
{
    &fatal( 18, "$_[0]/PostPreviewBody" ) if ( $_[0] ne 'PostPreview.xml' );

    local( $postDate ) = $^T;
    $postDate = &getUtcFromYYYY_MM_DD_HH_MM_SS( $gPostDateStr ) if ( $gPostDateStr ne '' );
    &dumpArtBody( '', 0, 1, $gOrigId, '', $postDate, $gSubject, $gIcon, 0, $gName, $gEmail, $gUrl, $gArticle );
}

sub hg_supersede_preview_body
{
    &fatal( 18, "$_[0]/SupersedePreviewBody" ) if ( $_[0] ne 'SupersedePreview.xml' );

    local( $postDate ) = $^T;
    $postDate = &getUtcFromYYYY_MM_DD_HH_MM_SS( $gPostDateStr ) if ( $gPostDateStr ne '' );

    # hg_post_preview_bodyとは異なり，fidが空（リプライ元ではない）．
    &dumpArtBody( '', 0, 1, '', '', $postDate, $gSubject, $gIcon, 0, $gName, $gEmail, $gUrl, $gArticle );
}

sub hg_supersede_preview_orig_article
{
    &fatal( 18, "$_[0]/SupersedePreviewOrigArticle" ) if ( $_[0] ne 'SupersedePreview.xml' );
    &dumpArtBody( $gOrigId, 0, 1 );
}


###
## 記事の登録
## 記事の訂正
#
sub uiPostExec
{
    # Isolation level: SERIALIZABLE.
    &lockAll();
    &cacheArt( $BOARD );

    local( $previewFlag ) = @_;

    &uiPostExecMain( $previewFlag, 'post' );
    &htmlGen( 'PostExec.xml' );

    &unlockAll();
}

sub uiSupersedeExec
{
    # Isolation level: SERIALIZABLE.
    &lockAll();
    &cacheArt( $BOARD );

    if ( !( $POLICY & 8 ) && ( $SYS_OVERWRITE == 0 ))
    {
	&fatal( 99, scalar( &cgi'tag( 'c' )));
    }

    local( $previewFlag ) = @_;
    &uiPostExecMain( $previewFlag, 'supersede' );
    &htmlGen( 'SupersedeExec.xml' );

    &unlockAll();
}

sub uiPostExecMain
{
    require( 'mimer.pl' );

    local( $previewFlag, $type ) = @_;

    # 入力された記事情報
    $gOrigId = &cgi'tag( 'id' );
    local( $postDateStr ) = &cgi'tag( 'postdate' );
    local( $TextType ) = &cgi'tag( 'texttype' );
    local( $Icon ) = &cgi'tag( 'icon' );
    local( $Subject ) = &cgi'tag( 'subject' );
    local( $Article ) = &cgi'tag( 'article' );
    local( $Fmail ) = &cgi'tag( 'fmail' );
    local( $op ) = &cgi'tag( 'op' );

    # ここ半日の間に生成されたフォームからしか投稿を許可しない．
    local( $base ) = ( -M &getPath( $SYS_DIR, $BOARD_FILE ));
    if ( $SYS_DENY_FORM_OLD && (( $op == 0 ) || ( $base - $op > .5 )))
    {
	&fatal( 15, '' );
    }

    # フォーム再利用の禁止
    if ( $SYS_DENY_FORM_RECYCLE )
    {
	local( $dKey ) = &getBoardKey( $BOARD );
	&fatal( 16, '' ) if ( $dKey && ( $dKey == $op ));
    }

    # 各種情報の取得
    local( $Name, $Email, $Url, $postDate );
    $postDate = $^T;
    if ( $POLICY & 8 )
    {
	if ( &cgi'tag( 'name' ) eq '' )
	{
	    $Name = $MAINT_NAME;
	    $Email = $MAINT;
	    $Url = $MAINT_URL;
	}
	else
	{
	    $Name = &cgi'tag( 'name' );
	    $Email = &cgi'tag( 'mail' );
	    $Url = &cgi'tag( 'url' );
	}
	if ( $postDateStr ne '' )
	{
	    $postDate = &getUtcFromYYYY_MM_DD_HH_MM_SS( $postDateStr );
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
	$Name = &cgi'tag( 'name' );
	$Email = &cgi'tag( 'mail' );
	$Url = &cgi'tag( 'url' );
    }

    $Subject = &MIME'base64decode( $Subject ) if $previewFlag;
    $Article = &MIME'base64decode( $Article ) if $previewFlag;
    &secureSubject( *Subject );
    &secureArticle( *Article, $TextType );

    if ( $type eq 'post' )
    {
	# 記事の作成
	$gNewArtId = &makeNewArticleEx( $BOARD, $gOrigId, $op, $postDate, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail, 1 );
    }
    elsif ( $type eq 'supersede' )
    {
	# 記事の訂正
	local( $name ) = &getArtAuthor( $gOrigId );
	&fatal( 44, '' ) if ( !&isUser( $name ) && !( $POLICY & 8 ));
	&fatal( 19, '' ) if (( &getArtDaughters( $gOrigId ) ne '' ) && !( $POLICY & 8 ) && ( $SYS_OVERWRITE == 1 ));

	$gNewArtId = &supersedeArticle( $BOARD, $gOrigId, $postDate, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail );
    }
    else
    {
	&fatal( 998, 'Must not reache here(UIPostExecMain).' );
    }
}

sub hg_post_exec_jump_to_new_article
{
    &fatal( 18, "$_[0]/PostExecJumpToNewArticle" ) if ( $_[0] ne 'PostExec.xml' );
    &dumpButtonToArticle( $BOARD, $gNewArtId, "書き込んだ$H_MESGへ" );
}

sub hg_supersede_exec_jump_to_new_article
{
    &fatal( 18, "$_[0]/SupersedeExecJumpToNewArticle" ) if ( $_[0] ne 'SupersedeExec.xml' );
    &dumpButtonToArticle( $BOARD, $gNewArtId, "訂正した$H_MESGへ" );
}

sub hg_post_exec_jump_to_orig_article
{
    &fatal( 18, "$_[0]/PostExecJumpToOrigArticle" ) if ( $_[0] ne 'PostExec.xml' );
    &dumpButtonToArticle( $BOARD, $gOrigId, "$H_PARENTへ" ) if ( $gOrigId ne '' );
}


###
## スレッド別タイトルおよび記事一覧
#
sub uiThreadArticle
{
    # Isolation level: READ UNCOMITTED.
    &lockBoard();
    &cacheArt( $BOARD );
    &unlockBoard();

    %gADDFLAG = ();
    @gIDLIST = ();

    local( $nofMsg ) = &getNofArt();

    # 表示する個数を取得
    $gNum = &cgi'tag( 'num' );
    if ( defined( &cgi'tag( 'id' )))
    {
	$gOld = $nofMsg - int( &cgi'tag( 'id' ) + $gNum/2 );
	$gOld = 0 if ( $gOld < 0 );
    }
    else
    {
	$gOld = &cgi'tag( 'old' );
    }
    $gRev = &cgi'tag( 'rev' );
    $gFold = (( $SYS_THREAD_FORMAT == 2 ) || &cgi'tag( 'fold' ))? 1 : 0;
    $gVRev = $gRev? 1-$SYS_BOTTOMTITLE : $SYS_BOTTOMTITLE;
    $gTo = $nofMsg - $gOld;
    $gFrom = $gTo - $gNum + 1;
    $gFrom = 0 if (( $gFrom < 0 ) || ( $gNum == 0 ));

    $gPageLinkStr = &pageLink( 'vt', $gNum, $gOld, $gRev, $gFold );

    # 整形済みフラグ
    # 0 ... 整形対象外
    # 1 ... 整形済み
    # 2 ... 未整形
    local( $IdNum, $Id );
    for ( $IdNum = $gFrom; $IdNum <= $gTo; $IdNum++ )
    {
	$gADDFLAG{ &getArtId( $IdNum ) } = 2;
    }

    &htmlGen( 'ThreadArticle.xml' );
}

sub hg_thread_article_tree
{
    &fatal( 18, "$_[0]/ThreadArticleTree" ) if ( $_[0] ne 'ThreadArticle.xml' );

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
	    $Id = &getArtId( $IdNum );
	    $Fid = &getArtParent( $Id );
	    # 後方参照は後回し．
	    next if (( $Fid ne '' ) && (( $gADDFLAG{$Fid} == 2 ) || ( $SYS_THREAD_FORMAT == 2 )));

	    # ノードを表示
	    $gHgStr .= "<ul>\n" unless $gFold;
	    if ( $gFold )
	    {
		&threadTitleNodeNoThread( $Id, 3 );
	    }
	    elsif ( $SYS_THREAD_FORMAT == 0 )
	    {
		&threadTitleNodeThread( $Id, 3 );
	    }
	    elsif ( $SYS_THREAD_FORMAT == 1 )
	    {
		&threadTitleNodeAllThread( $Id, 3 );
	    }
	    else
	    {
		&threadTitleNodeNoThread( $Id, 3 );
	    }
	    $gHgStr .= "</ul>\n" unless $gFold;
	    &cgiprint'cache( $gHgStr ); $gHgStr = '';
	}
	$gHgStr .= "</ul>\n" if $gFold;
    }
    else
    {
	$gHgStr .= "<ul>\n" if $gFold;

	for( $IdNum = $gTo; $IdNum >= $gFrom; $IdNum-- )
	{
	    $Id = &getArtId( $IdNum );
	    $Fid = &getArtParent( $Id );
	    next if (( $Fid ne '' ) && (( $gADDFLAG{$Fid} == 2 ) || ( $SYS_THREAD_FORMAT == 2 )));

	    $gHgStr .= "<ul>\n" unless $gFold;
	    if ( $gFold )
	    {
		&threadTitleNodeNoThread( $Id, 3 );
	    }
	    elsif ( $SYS_THREAD_FORMAT == 0 )
	    {
		&threadTitleNodeThread( $Id, 3 );
	    }
	    elsif ( $SYS_THREAD_FORMAT == 1 )
	    {
		&threadTitleNodeAllThread( $Id, 3 );
	    }
	    else
	    {
		&threadTitleNodeNoThread( $Id, 3 );
	    }
	    $gHgStr .= "</ul>\n" unless $gFold;
	    &cgiprint'cache( $gHgStr ); $gHgStr = '';
	}
	$gHgStr .= "</ul>\n" if $gFold;
    }
}

sub hg_thread_article_body
{
    &fatal( 18, "$_[0]/ThreadArticleBody" ) if ( $_[0] ne 'ThreadArticle.xml' );

    local( $id );
    if ( $#gIDLIST >= 0 )
    {
	$gHgStr .= $HTML_HR;
	while ( $id = shift( @gIDLIST ))
	{
	    &dumpArtBody( $id, $SYS_COMMAND_EACH, 1 );
	    $gHgStr .= $HTML_HR;
	}
    }
}


###
## スレッド別タイトル一覧
#
sub uiThreadTitle
{
    # Isolation level: READ UNCOMITTED.
    &lockBoard();
    &cacheArt( $BOARD );

    ( $gComType ) = @_;

    if ( $gComType == 3 )
    {
	# リンクかけかえの実施
	&reLinkExec( scalar( &cgi'tag( 'rfid' )), scalar( &cgi'tag( 'rtid' )), $BOARD );
    }
    elsif ( $gComType == 5 )
    {
	# 移動の実施
	&reOrderExec( scalar( &cgi'tag( 'rfid' )), scalar( &cgi'tag( 'rtid' )), $BOARD );
    }

    &unlockBoard();

    local( $vCom, $vStr );

    if ( $ComType == 0 )
    {
	$vCom = 'v';
	$vStr = '';
    }
    elsif ( $ComType == 2 )
    {
	$vCom = 'ct';
	$vStr = '&rtid=' . &cgi'tag( 'roid' ) . '&rfid=' . &cgi'tag( 'rfid' ) .
	    '&rtid=' . &cgi'tag( 'rtid' );
    }
    elsif ( $gComType == 3 )
    {
	$vCom = 'v';
	$vStr = '';
    }
    elsif ( $gComType == 4 )
    {
	$vCom = 'mvt';
	$vStr = '&rtid=' . &cgi'tag( 'roid' ) . '&rfid=' . &cgi'tag( 'rfid' ) .
	    '&rtid=' . &cgi'tag( 'rtid' );
    }
    elsif ( $gComType == 5 )
    {
	$vCom = 'v';
	$vStr = '';
    }

    %gADDFLAG = ();
    @gIDLIST = ();		# Not used here. It's for ThreadArticle.

    local( $nofMsg ) = &getNofArt();

    # 表示する個数を取得
    $gNum = &cgi'tag( 'num' );
    if ( defined( &cgi'tag( 'id' )))
    {
	$gOld = $nofMsg - int( &cgi'tag( 'id' ) + $gNum/2 );
	$gOld = 0 if ( $gOld < 0 );
    }
    else
    {
	$gOld = &cgi'tag( 'old' );
    }
    $gRev = &cgi'tag( 'rev' );
    $gFold = (( $SYS_THREAD_FORMAT == 2 ) || &cgi'tag( 'fold' ))? 1 : 0;
    $gVRev = $gRev? 1-$SYS_BOTTOMTITLE : $SYS_BOTTOMTITLE;
    $gTo = $nofMsg - $gOld;
    $gFrom = $gTo - $gNum + 1;
    $gFrom = 0 if (( $gFrom < 0 ) || ( $gNum == 0 ));

    $gPageLinkStr = &pageLink( "$vCom$vStr", $gNum, $gOld, $gRev, $gFold );

    # 整形済みフラグ
    # 0 ... 整形対象外
    # 1 ... 整形済み
    # 2 ... 未整形
    local( $IdNum );
    for ( $IdNum = $gFrom; $IdNum <= $gTo; $IdNum++ )
    {
	$gADDFLAG{ &getArtId( $IdNum ) } = 2;
    }

    &htmlGen( 'ThreadTitle.xml' );
}

sub hg_thread_title_board_header
{
    &fatal( 18, "$_[0]/ThreadTitleBoardHeader" ) if ( $_[0] ne 'ThreadTitle.xml' );

    if ( $gComType == 2 )
    {
	$gHgStr .= "<p>新たな$H_REPLY先を指定します．\n";
	$gHgStr .= "$H_MESG「#" . &cgi'tag( 'rfid' ) . "」を，どの$H_MESGへの$H_REPLYにしますか? $H_REPLY先の$H_MESGの$H_RELINKTO_MARKをクリックしてください．</p>\n";
    }
    elsif ( $gComType == 3 )
    {
	$gHgStr .= "<p>指定された$H_MESGの$H_REPLY先を変更しました．</p>\n";
    }
    elsif ( $gComType == 4 )
    {
	$gHgStr .= "<p>移動先を指定します．\n";
	$gHgStr .= "$H_MESG「#" . &cgi'tag( 'rfid' ) . "」を，どの$H_MESGの下に移動しますか? $H_MESGの$H_REORDERTO_MARKをクリックしてください．</p>\n";
    }
    elsif ( $gComType == 5 )
    {
	$gHgStr .= "<p>指定された$H_MESGを移動しました．</p>\n";
    }

    &dumpBoardHeader();

    if ( $POLICY & 8 )
    {
	if ( $gComType == 3 )
	{
	    $gHgStr .= "<ul>\n<li>" . &linkP( "b=$BOARD_ESC&c=ce&rtid=" .
		&cgi'tag( 'roid' ) . "&rfid=" . &cgi'tag( 'rfid' ),
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
    &fatal( 18, "$_[0]/ThreadTitleTree" ) if ( $_[0] ne 'ThreadTitle.xml' );

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
	if (( $gComType == 2 ) && ( &getArtParents( scalar( &cgi'tag( 'rfid' ))) ne '' ))
	{
	    $gHgStr .= '<ul><li>' . &linkP( "b=$BOARD_ESC&c=ce&rtid=&rfid=" .
		&cgi'tag( 'rfid' ) . '&roid=' . &cgi'tag( 'roid' ) . $AddNum,
		"[どの$H_MESGへの$H_REPLYでもなく，新着$H_MESGにする]" ) .
		"</li></ul>\n";
	}
	elsif ( $gComType == 4 )
	{
	    $gHgStr .= '<ul><li>' . &linkP( "b=$BOARD_ESC&c=mve&rtid=&rfid=" .
		&cgi'tag( 'rfid' ) . "&roid=" . &cgi'tag( 'roid' ) . $AddNum,
		"[全記事の先頭に移動する(このページの，ではありません)]" ) .
		"</li></ul>\n";
	}

	$gHgStr .= "<ul>\n" if $gFold;

	for( $IdNum = $gFrom; $IdNum <= $gTo; $IdNum++ )
	{
	    # 該当記事のIDを取り出す
	    $Id = &getArtId( $IdNum );
	    $Fid = &getArtParent( $Id );
	    # 後方参照は後回し．
	    next if (( $Fid ne '' ) && (( $gADDFLAG{$Fid} == 2 ) ||
		( $SYS_THREAD_FORMAT == 2 )));

	    # ノードを表示
	    $gHgStr .= "<ul>\n" unless $gFold;
	    if ( $gFold )
	    {
		&threadTitleNodeNoThread( $Id, 1, $AddNum, ( $POLICY & 8 ));
	    }
	    elsif ( $SYS_THREAD_FORMAT == 0 )
	    {
		&threadTitleNodeThread( $Id, 1, $AddNum, ( $POLICY & 8 ));
	    }
	    elsif ( $SYS_THREAD_FORMAT == 1 )
	    {
		&threadTitleNodeAllThread( $Id, 1, $AddNum, ( $POLICY & 8 ));
	    }
	    else
	    {
		&threadTitleNodeNoThread( $Id, 1, $AddNum, ( $POLICY & 8 ));
	    }
	    $gHgStr .= "</ul>\n" unless $gFold;
	    &cgiprint'cache( $gHgStr ); $gHgStr = '';
	}
	$gHgStr .= "</ul>\n" if $gFold;
    }
    else
    {
	# 新しいのから処理
	if (( $gComType == 2 ) && ( &getArtParents( scalar( &cgi'tag( 'rfid' ))) ne '' ))
	{
	    $gHgStr .= '<ul><li>' . &linkP( "b=$BOARD_ESC&c=ce&rtid=&rfid=" .
		&cgi'tag( 'rfid' ) . "&roid=" . &cgi'tag( 'roid' ) . $AddNum,
		"[どの$H_MESGへの$H_REPLYでもなく，新着$H_MESGにする]" ) .
		"</li></ul>\n";
	}
	elsif ( $gComType == 4 )
	{
	    $gHgStr .= '<ul><li>' . &linkP( "b=$BOARD_ESC&c=mve&rtid=&rfid=" .
		&cgi'tag( 'rfid' ) . "&roid=" . &cgi'tag( 'roid' ) . $AddNum,
		"[全記事の先頭に移動する(このページの，ではありません)]" ) .
		"</li></ul>\n";
	}

	$gHgStr .= "<ul>\n" if $gFold;

	for( $IdNum = $gTo; $IdNum >= $gFrom; $IdNum-- )
	{
	    # 後は同じ
	    $Id = &getArtId( $IdNum );
	    $Fid = &getArtParent( $Id );
	    next if (( $Fid ne '' ) && (( $gADDFLAG{$Fid} == 2 ) ||
		( $SYS_THREAD_FORMAT == 2 )));

	    $gHgStr .= "<ul>\n" unless $gFold;
	    if ( $gFold )
	    {
		&threadTitleNodeNoThread( $Id, 1, $AddNum, ( $POLICY & 8 ));
	    }
	    elsif ( $SYS_THREAD_FORMAT == 0 )
	    {
		&threadTitleNodeThread( $Id, 1, $AddNum, ( $POLICY & 8 ));
	    }
	    elsif ( $SYS_THREAD_FORMAT == 1 )
	    {
		&threadTitleNodeAllThread( $Id, 1, $AddNum, ( $POLICY & 8 ));
	    }
	    else
	    {
		&threadTitleNodeNoThread( $Id, 1, $AddNum, ( $POLICY & 8 ));
	    }
	    $gHgStr .= "</ul>\n" unless $gFold;
	    &cgiprint'cache( $gHgStr ); $gHgStr = '';
	}
	$gHgStr .= "</ul>\n" if $gFold;
    }
}

# 新着ノードのみ表示
sub threadTitleNodeNoThread
{
    local( $id, $flag, $addNum, $maint ) = @_;

    local( $fid, $aids, $date, $title, $icon, $host, $name ) = &getArtInfo( $id );
    &dumpArtSummaryItem( $id, $aids, $date, $title, $icon, $name, $flag );

    $flag &= 6; # 110
    push( @gIDLIST, $id );

    &threadTitleMaintIcon( $id, $addNum ) if $maint;

    $gHgStr .= "</li>\n";
}

# ページ内スレッドのみ表示
sub threadTitleNodeThread
{
    local( $id, $flag, $addNum, $maint ) = @_;

    # ページ外ならおしまい．
    return if ( $gADDFLAG{ $id } != 2 );

    local( $fid, $aids, $date, $title, $icon, $host, $name ) = &getArtInfo( $id );
    &dumpArtSummaryItem( $id, $aids, (( !$SYS_COMPACTTHREAD || $flag&1 )? $date : 0 ), $title, $icon, $name, $flag );

    $flag &= 6; # 110
    $gADDFLAG{ $id } = 1;		# 整形済み
    push( @gIDLIST, $id );

    &threadTitleMaintIcon( $id, $addNum ) if $maint;

    # 娘が居れば……
    if ( $aids )
    {
	$gHgStr .= "<ul>\n";
	foreach ( split( /,/, $aids ))
	{
	    &threadTitleNodeThread( $_, $flag, $addNum, $maint );
	}
	$gHgStr .= "</ul>\n";
    }
    $gHgStr .= "</li>\n";
}

# 全スレッドの表示
sub threadTitleNodeAllThread
{
    local( $id, $flag, $addNum, $maint ) = @_;

    # 表示済みならおしまい．
    return if ( $gADDFLAG{ $id } == 1 );

    local( $fid, $aids, $date, $title, $icon, $host, $name ) = &getArtInfo( $id );
    &dumpArtSummaryItem( $id, $aids, (( !$SYS_COMPACTTHREAD || $flag&1 )? $date : 0 ), $title, $icon, $name, $flag );

    $flag &= 6; # 110
    $gADDFLAG{ $id } = 1;		# 整形済み
    push( @gIDLIST, $id );

    &threadTitleMaintIcon( $id, $addNum ) if $maint;

    # 娘が居れば……
    if ( $aids )
    {
	$gHgStr .= "<ul>\n";
	foreach ( split( /,/, $aids ))
	{
	    &threadTitleNodeAllThread( $_, $flag, $addNum, $maint );
	}
	$gHgStr .= "</ul>\n";
    }
    $gHgStr .= "</li>\n";
}

# 管理者用のアイコン表示
sub threadTitleMaintIcon
{
    local( $id, $addNum ) = @_;

    $gHgStr .= " .......... \n";

    local( $fromId ) = &cgi'tag( 'rfid' );
    local( $oldId ) = &cgi'tag( 'roid' );

    local( $parents ) = &getArtParents( $id );

    # リンク先変更コマンド(From)
    $gHgStr .= &linkP( "b=$BOARD_ESC&c=ct&rfid=$id&roid=" . $parents . $addNum,
	$H_RELINKFROM_MARK, '', $H_RELINKFROM_MARK_L ) . "\n";

    if ( $parents eq '' )
    {
	# 移動コマンド(From)
	$gHgStr .= &linkP( "b=$BOARD_ESC&c=mvt&rfid=$id&roid=" . $parents .
	    $addNum, $H_REORDERFROM_MARK, '', $H_REORDERFROM_MARK_L ) . "\n";
    }

    # 削除・訂正コマンド
    $gHgStr .= &linkP( "b=$BOARD_ESC&c=f&s=on&id=$id", $H_SUPERSEDE_ICON, '',
	$H_SUPERSEDE_ICON_L ) . "\n";
    $gHgStr .= &linkP( "b=$BOARD_ESC&c=dp&id=$id", $H_DELETE_ICON, '',
	$H_DELETE_ICON_L ) . "\n";

    # 移動コマンド(To)
    if (( $gComType == 4 ) && ( $fromId ne $id ) && ( $parents eq '' ) && ( $fromId ne $id ))
    {
	$gHgStr .= &linkP( "b=$BOARD_ESC&c=mve&rtid=$id&rfid=$fromId&roid=$oldId" . $addNum, $H_REORDERTO_MARK, '', $H_REORDERTO_MARK_L ) . "\n";
    }

    # リンク先変更コマンド(To)
    if (( $gComType == 2 ) && ( $fromId ne $id ) &&
	( !grep( /^$fromId$/, split( /,/, &getArtDaughters( $id )))) &&
	( !grep( /^$fromId$/, split( /,/, $parents ))))
    {
	$gHgStr .= &linkP( "b=$BOARD_ESC&c=ce&rtid=$id&rfid=$fromId&roid=$oldId" . $addNum, $H_RELINKTO_MARK, '', $H_RELINKTO_MARK_L ) . "\n";
    }
}


###
## 書き込み順タイトル一覧
#
sub uiSortTitle
{
    # Isolation level: READ UNCOMITTED.
    &lockBoard();
    &cacheArt( $BOARD );
    &unlockBoard();

    local( $nofMsg ) = &getNofArt();

    # 表示する個数を取得
    local( $Num ) = &cgi'tag( 'num' );
    local( $Old );
    if ( defined( &cgi'tag( 'id' )))
    {
	$Old = $nofMsg - int( &cgi'tag( 'id' ) + $Num/2 );
	$Old = 0 if ( $Old < 0 );
    }
    else
    {
	$Old = &cgi'tag( 'old' );
    }
    local( $Rev ) = &cgi'tag( 'rev' );
    $gFold = (( $SYS_THREAD_FORMAT == 2 ) || &cgi'tag( 'fold' ))? 1 : 0;
    $gVRev = $Rev? 1-$SYS_BOTTOMTITLE : $SYS_BOTTOMTITLE;
    $gTo = $nofMsg - $Old;
    $gFrom = $gTo - $Num + 1;
    $gFrom = 0 if (( $gFrom < 0 ) || ( $Num == 0 ));

    $gPageLinkStr = &pageLink( 'r', $Num, $Old, $Rev, '' );

    &htmlGen( 'SortTitle.xml' );
}

sub hg_sort_title_tree
{
    &fatal( 18, "$_[0]/SortTitleTree" ) if ( $_[0] ne 'SortTitle.xml' );

    $gHgStr .= "<ul>\n";

    # 記事の表示
    local( $IdNum, $Id, $fid, $aids, $date, $title, $icon, $host, $name );

    local( $nofMsg ) = &getNofArt();
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
		$Id = &getArtId( $IdNum );
		( $fid, $aids, $date, $title, $icon, $host, $name ) = &getArtInfo( $Id );
		&dumpArtSummaryItem( $Id, $aids, $date, $title, $icon, $name, 1 );
		$gHgStr .= "</li>\n";
	    }
	}
	else
	{
	    for ($IdNum = $gTo; $IdNum >= $gFrom; $IdNum--)
	    {
		$Id = &getArtId( $IdNum );
		( $fid, $aids, $date, $title, $icon, $host, $name ) = &getArtInfo( $Id );
		&dumpArtSummaryItem( $Id, $aids, $date, $title, $icon, $name, 1 );
		$gHgStr .= "</li>\n";
	    }
	}
    }
    $gHgStr .= "</ul>\n";
}


###
## スレッド別記事一覧
#
sub uiShowThread
{
    # Isolation level: READ UNCOMITTED.
    &lockBoard();
    &cacheArt( $BOARD );
    &unlockBoard();

    $gId = &cgi'tag( 'id' );

    $gFids = &getArtParents( $gId );

    # フォロー記事の木構造の取得
    # ex. '( a ( b ( c d ) ) ( e ) ( f ( g ) ) )'というリスト
    @gFollowIdTree = ();
    &getFollowIdTree( $gId, *gFollowIdTree );

    &htmlGen( 'ShowThread.xml' );
}

sub hg_show_thread_title
{
    &fatal( 18, "$_[0]/ShowThreadTitle" ) if ( $_[0] ne 'ShowThread.xml' );
    $gHgStr .= &getArtSubject( &getTreeTopArticle( *gFollowIdTree ));
}

sub hg_show_thread_title_tree
{
    &fatal( 18, "$_[0]/ShowThreadTitleTree" ) if ( $_[0] ne 'ShowThread.xml' );

    &dumpOriginalArticles( $gFids );
    &dumpArtThread( 6, @gFollowIdTree );
}

sub hg_show_thread_msg_body
{
    &fatal( 18, "$_[0]/ShowThreadMsgBody" ) if ( $_[0] ne 'ShowThread.xml' );
    &dumpArtThread( 2, @gFollowIdTree );
}

sub hg_show_thread_back_to_title_button
{
    &fatal( 18, "$_[0]/ShowThreadBackToTitleButton" ) if ( $_[0] ne 'ShowThread.xml' );
    &dumpButtonToTitleList( $BOARD, $gId );
}


###
## 書き込み順メッセージ一覧
#
sub uiSortArticle
{
    # Isolation level: READ UNCOMITTED.
    &lockBoard();
    &cacheArt( $BOARD );
    &unlockBoard();

    $gNum = &cgi'tag( 'num' );
    $gOld = &cgi'tag( 'old' );
    $gRev = &cgi'tag( 'rev' );
    $gFold = (( $SYS_THREAD_FORMAT == 2 ) || &cgi'tag( 'fold' ))? 1 : 0;

    $gPageLinkStr = &pageLink( 'l', $gNum, $gOld, $gRev, '' );

    &htmlGen( 'SortArticle.xml' );
}

sub hg_sort_article_body
{
    &fatal( 18, "$_[0]/SortArticleBody" ) if ( $_[0] ne 'SortArticle.xml' );

    local( $vRev ) = $gRev? 1-$SYS_BOTTOMARTICLE : $SYS_BOTTOMARTICLE;
    local( $nofMsg ) = &getNofArt();
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
		$Id = &getArtId( $IdNum );
		&dumpArtBody( $Id, $SYS_COMMAND_EACH, 1 );
		$gHgStr .= $HTML_HR;
	    }
	}
	else
	{
	    for ( $IdNum = $To; $IdNum >= $From; $IdNum-- )
	    {
		$Id = &getArtId( $IdNum );
		&dumpArtBody( $Id, $SYS_COMMAND_EACH, 1 );
		$gHgStr .= $HTML_HR;
	    }
	}
    }
}


###
## 単一記事の表示
#
sub uiShowArticle
{
    # Isolation level: READ UNCOMITTED.
    &lockBoard();
    &cacheArt( $BOARD );
    &unlockBoard();

    $gId = &cgi'tag( 'id' );

    # 未投稿記事は読めない
    &fatal( 8, '' ) if ( &getArtSubject( $gId ) eq '' );

    &htmlGen( 'ShowArticle.xml' );
}

sub hg_show_article_title
{
    &fatal( 18, "$_[0]/ShowArticleTitle" ) if ( $_[0] ne 'ShowArticle.xml' );
    $gHgStr .= &getArtSubject( $gId );
}

sub hg_show_article_body
{
    &fatal( 18, "$_[0]/ShowArticleBody" ) if ( $_[0] ne 'ShowArticle.xml' );
    &dumpArtBody( $gId, 1, 1 );
}

sub hg_show_article_original
{
    &fatal( 18, "$_[0]/ShowArticleOriginal" ) if ( $_[0] ne 'ShowArticle.xml' );
    local( $fids ) = &getArtParents( $gId );
    if ( $fids ne '' )
    {
	$gHgStr .= "<p>$H_THREAD_ALL$H_PARENT</p>\n";
	&dumpOriginalArticles( $fids );
    }
}

sub hg_show_article_reply
{
    &fatal( 18, "$_[0]/ShowArticleReply" ) if ( $_[0] ne 'ShowArticle.xml' );

    $gHgStr .= "<p>$H_THREAD$H_REPLY</p>\n";
    &dumpReplyArticles( &getArtDaughters( $gId ));
}


###
## 記事の検索(表示画面の作成)
#
sub uiSearchArticle
{
    # Isolation level: READ UNCOMITTED.
    &lockBoard();
    &cacheArt( $BOARD );
    &unlockBoard();

    &htmlGen( 'SearchArticle.xml' );
}

sub hg_search_article_result
{
    &fatal( 18, "$_[0]/SearchArticleResult" ) if ( $_[0] ne 'SearchArticle.xml' );

    local( $SearchView ) = &cgi'tag( 'searchthread' )? 1 : 0;
    local( $Key ) = &cgi'tag( 'key' );
    local( $SearchSubject ) = &cgi'tag( 'searchsubject' );
    local( $SearchPerson ) = &cgi'tag( 'searchperson' );
    local( $SearchArticle ) = &cgi'tag( 'searcharticle' );
    local( $SearchPostTimeFrom ) = &cgi'tag( 'searchposttimefrom' );
    local( $SearchPostTimeTo ) = &cgi'tag( 'searchposttimeto' );
    local( $SearchIcon ) = &cgi'tag( 'searchicon' );

    local( %iconHash );
    foreach ( &cgi'tag( 'icon' ))
    {
	next if ( $_ eq $H_NOICON );
	$iconHash{ $_ } = 1;
    }

    # キーワード関連検索対象が指定されなかった場合は，キーワードは空扱い．
    $Key = '' unless ( $SearchSubject || $SearchPerson || $SearchArticle );

    # 対象があれば検索
    if (( $Key ne '' ) || ( $SearchPostTimeFrom || $SearchPostTimeTo ) || $SearchIcon )
    {
	&dumpSearchResult( $SearchView, $Key, $SearchSubject, $SearchPerson,
	    $SearchArticle, $SearchPostTimeFrom, $SearchPostTimeTo,
	    $SearchIcon, *iconHash );
    }
}


###
## 削除記事の確認
#
sub uiDeletePreview
{
    # Isolation level: READ UNCOMITTED.
    &lockBoard();
    &cacheArt( $BOARD );
    &unlockBoard();

    if ( !( $POLICY & 8 ) && ( $SYS_OVERWRITE == 0 ))
    {
	&fatal( 99, scalar( &cgi'tag( 'c' )));
    }

    $gId = &cgi'tag( 'id' );
    $gAids = &getArtDaughters( $gId );

    # 未投稿記事は読めない
    &fatal( 8, '' ) if ( &getArtSubject( $gId ) eq '' );

    &htmlGen( 'DeletePreview.xml' );
}

sub hg_delete_preview_form
{
    &fatal( 18, "$_[0]/DeletePreviewForm" ) if ( $_[0] ne 'DeletePreview.xml' );

    local( %tags );
    %tags = ( 'c', 'de', 'b', $BOARD, 'id', $gId );
    &dumpForm( *tags, 'このメッセージを削除します', '', '' );

    if ( $gAids )
    {
	%tags = ( 'c', 'det', 'b', $BOARD, 'id', $gId );
	&dumpForm( *tags, "$H_REPLYメッセージもまとめて削除します", '', '' );
    }
}

sub hg_delete_preview_body
{
    &fatal( 18, "$_[0]/DeletePreviewBody" ) if ( $_[0] ne 'DeletePreview.xml' );
    &dumpArtBody( $gId, 0, 1 );
}

sub hg_delete_preview_reply
{
    &fatal( 18, "$_[0]/DeletePreviewReply" ) if ( $_[0] ne 'DeletePreview.xml' );

    $gHgStr .= "<p>$H_THREAD$H_REPLY</p>\n";
    &dumpReplyArticles( $gAids );
}


###
## 記事の削除
#
sub uiDeleteExec
{
    # Isolation level: SERIALIZABLE.
    &lockBoard();
    &cacheArt( $BOARD );

    if ( !( $POLICY & 8 ) && ( $SYS_OVERWRITE == 0 ))
    {
	&fatal( 99, scalar( &cgi'tag( 'c' )));
    }

    local( $threadFlag ) = @_;

    $gId = &cgi'tag( 'id' );

    local( $name ) = &getArtAuthor( $gId );
    &fatal( 44, '' ) if ( !&isUser( $name ) && !( $POLICY & 8 ));
    &fatal( 19, '' ) if (( &getArtDaughters( $gId ) ne '' ) && !( $POLICY & 8 ) && ( $SYS_OVERWRITE == 1 ));

    # 削除実行
    &deleteArticle( $gId, $BOARD, $threadFlag );

    &htmlGen( 'DeleteExec.xml' );

    &unlockBoard();
}

sub hg_delete_exec_back_to_title_button
{
    &fatal( 18, "$_[0]/DeleteExecBackToTitleButton" ) if ( $_[0] ne 'DeleteExec.xml' );
    &dumpButtonToTitleList( $BOARD, $gId );
}


###
## アイコン表示
#
sub uiShowIcon
{
    # Isolation level: CHAOS.

    &htmlGen( 'ShowIcon.xml' );
}


###
## ヘルプ表示
#
sub uiHelp
{
    # Isolation level: CHAOS.

    &htmlGen( 'Help.xml' );
}


###
## エラー表示
#
sub uiFatal
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

    $gHgStr .= sprintf( qq(<link rel="StyleSheet" href="%s" type="text/css" media="screen" />), &getStyleSheetURL( $STYLE_FILE )) if $STYLE_FILE;
}

sub hg_s_address
{
    $gHgStr .= "<address>\nMaintenance: " .
	&tagA( $MAINT_NAME, "mailto:$MAINT" ) . $HTML_BR .
	&tagA( $PROGNAME, 'http://www.jin.gr.jp/~nahi/kb/' ) .
	": Copyright &copy; 1995-2000 " .
	&tagA( 'NAKAMURA, Hiroshi', 'http://www.jin.gr.jp/~nahi/' ) .
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
    $gHgStr .= "時刻: " . &getDateTimeFormatFromUtc( $^T );
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
    $gHgStr .= &getDateTimeFormatFromUtc( $^T );
}

sub hg_c_top_menu
{
    $gHgStr .= qq(<div class="kbTopMenu">\n);
    local( $formStr );

    local( %tags );
    if ( $SYS_AUTH )
    {
	$formStr .= &linkP( 'c=bl', 'TOP', 'J' ) . "\n";
#	$formStr .= ' ' . &linkP( 'c=ue', 'OPEN', 'O' ) . "\n";
	$formStr .= ' ' . &linkP( 'c=lo', 'LOGIN', 'L' ) . "\n";
	if ( $UNAME && ( $UNAME ne $GUEST ) && ( $UNAME ne $cgiauth'F_COOKIE_RESET ))
	{
	    $formStr .= ' ' . &linkP( 'c=uc', 'INFO', 'C' ) . "\n";
	}
	$formStr .= "&nbsp;&nbsp;&nbsp;\n";
    }

    if ( $BOARD )
    {
	$tags{ 'b' } = $BOARD;
	$formStr .= &tagLabel( "表示画面", 'c', 'W' ) . ": \n";

	local( $contents );
	$contents .= sprintf( qq[<option%s value="v">最新$H_SUBJECT一覧(スレッド)</option>\n], ( $SYS_TITLE_FORMAT == 0 )? ' selected="selected"' : '' );
	$contents .= sprintf( qq[<option%s value="r">最新$H_SUBJECT一覧(書き込み順)</option>\n], ( $SYS_TITLE_FORMAT == 1 )? ' selected="selected"' : '' );
	$contents .= qq[<option value="vt">最新$H_MESG一覧(スレッド)</option>\n];
	$contents .= qq[<option value="l">最新$H_MESG一覧(書き込み順)</option>\n];
	$contents .= qq(<option value="v">&nbsp;</option>\n);
	$contents .= qq(<option value="s">$H_MESGの検索</option>\n);
	$contents .= qq(<option value="i">使える$H_ICON一覧</option>\n) if $SYS_ICON;
	if (( $POLICY & 2 ) && ( !$SYS_NEWART_ADMINONLY || ( $POLICY & 8 )))
	{
	    $contents .= qq(<option value="v">&nbsp;</option>\n);
	    $contents .= qq(<option value="n">$H_POSTNEWARTICLE</option>\n);
	}

	$formStr .= &tagSelect( 'c', $contents );
    }
    else
    {
	$tags{ 'c' } = $SYS_TITLE_FORMAT? 'r' : 'v';
	$formStr .= &tagLabel( "表示画面", 'b', 'W' ) . ": \n";

	local( $contents, $boardId );
	$boardId = &getBoardId( 0 );
	$contents .= qq(<option selected="selected" value="$boardId">) . &getBoardName( $boardId ) . "</option>\n";
	foreach ( 1 .. &getNofBoard() )
	{
	    $boardId = &getBoardId( $_ );
	    $contents .= qq(<option value="$boardId">) . &getBoardName( $boardId ) . "</option>\n";
	}

	$formStr .= &tagSelect( 'b', $contents );
    }

    $formStr .= "\n&nbsp;&nbsp;&nbsp;" .
	&tagLabel( "表示件数", 'num', 'Y' ) . ': ' .
	&tagInputText( 'text', 'num', (( &cgi'tag( 'num' ) ne '' )? scalar( &cgi'tag( 'num' )) : $DEF_TITLE_NUM ),	3 );

    $tags{ 'old' } = &cgi'tag( 'old' ) if ( defined &cgi'tag( 'old' ));
    $tags{ 'rev' } = &cgi'tag( 'rev' ) if ( defined &cgi'tag( 'rev' ));
    $tags{ 'fold' } = &cgi'tag( 'fold' ) if ( defined &cgi'tag( 'fold' ));
    &dumpForm( *tags, '表示(V)', '', *formStr );
    $gHgStr .= "</div>\n";
}

sub hg_c_help
{
    $gHgStr .= &linkP( "b=$BOARD_ESC&c=h", &tagComImg( $ICON_HELP, 'ヘルプ' ), 'H', '', '', $_[1] );
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
    $gHgStr .= '<dd>→' . &linkP( 'c=ue', "$H_USERアカウント作成ページ" .
	&tagAccessKey( 'O' ), 'O' ) . "</dd>\n";

    if ( $UNAME )
    {
	$gHgStr .= "<dt>「別の$H_USER情報を呼び出す」（現在利用中の$H_USER情報は，$UNAMEのものです）</dt>\n";
	$gHgStr .= '<dd>→' . &linkP( 'c=lo', "ログインページ" . &tagAccessKey( 'L' ), 'L' ) . "</dd>\n";
    }

    if ( $POLICY & 4 )
    {
	$gHgStr .= "<dt>「$UNAMEについて登録した$H_USER情報を変更する」</dt>\n";
	$gHgStr .= '<dd>→' . &linkP( 'c=uc', "$H_USER情報ページ" . &tagAccessKey( 'C' ), 'C' ) . "</dd>\n";
    }

    if ( $POLICY & 8 )
    {
	$gHgStr .= "<dt>「新規に$H_BOARDを作りたい」</dt>\n";
	$gHgStr .= '<dd>→' . &linkP( 'c=be', "$H_BOARDの新規作成" .
	    &tagAccessKey( 'A' ), 'A' ) . "</dd>\n";
    }

    $gHgStr .= "</dl>\n";
}

sub hg_c_page_link
{
    $gHgStr .= $gPageLinkStr;
}

sub hg_c_board_link_all
{
    $gHgStr .= "<ul>\n";

    local( $board, $newIcon, $modTimeUtc, $modTime, $boardEsc );
    foreach ( 0 .. &getNofBoard() )
    {
	$board = &getBoardId( $_ );
	$modTimeUtc = &getBoardLastmod( $board );
	$modTime = &getDateTimeFormatFromUtc( $modTimeUtc );
	if ( $SYS_BLIST_NEWICON_DATE &&
	    (( $^T - $modTimeUtc ) < $SYS_BLIST_NEWICON_DATE * 86400 ))
	{
	    $newIcon = " " . &tagArtImg( $H_NEWARTICLE );
	}
	else
	{
	    $newIcon = '';
	}

	$boardEsc = &uriEscape( $board );
	$gHgStr .= '<li>' .
	    &linkP( "b=$boardEsc&c=" . ( $SYS_TITLE_FORMAT? 'r' : 'v' ) .
	    "&num=$DEF_TITLE_NUM", &getBoardName( $board )) .
	    "$newIcon\n[最新: $modTime]\n";
	if ( $POLICY & 8 )
	{
	    $gHgStr .= &linkP( "b=$boardEsc&c=bc", "←設定変更" ) . "\n";
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

    $modTimeUtc = &getBoardLastmod( $board );
    $modTime = &getDateTimeFormatFromUtc( $modTimeUtc );
    if ( $SYS_BLIST_NEWICON_DATE &&
	(( $^T - $modTimeUtc ) < $SYS_BLIST_NEWICON_DATE * 86400 ))
    {
	$newIcon = " " . &tagArtImg( $H_NEWARTICLE );
    }
    else
    {
	$newIcon = '';
    }

    local( $boardEsc ) = &uriEscape( $board );
    $gHgStr .= &linkP( "b=$boardEsc&c=$com&num=$num", &getBoardName( $board )) . "$newIcon\n[最新: $modTime]\n";
    if ( $POLICY & 8 )
    {
	$gHgStr .= &linkP( "b=$boardEsc&c=bc", "←設定変更" ) . "\n";
    }
}

sub hg_c_anchor
{
    $gHgStr .= &tagA( split( ',', $_[1] ));
}

sub hg_c_icon_msg
{
    $gHgStr .= &tagArtImg( $_[1] );
}

sub hg_c_icon
{
    local( $src, $alt ) = split( ',', $_[1], 2 );
    $gHgStr .= &tagComImg( &getIconURL( $src ), $alt );
}

sub hg_c_img
{
    local( $src, $alt, $width, $height ) = split( ',', $_[1], 4 );
    $gHgStr .= &tagImg( &getImgURL( $src ), $alt, $width, $height, 'kbImg' );
}

sub hg_b_board_name
{
    $gHgStr .= $BOARDNAME if $BOARD;
}

sub hg_b_board_header
{
    &dumpBoardHeader() if $BOARD;
}

sub hg_b_post_entry_form
{
    if ( $POLICY & 2 )
    {
	&dumpArtEntry( $gDefIcon, $gEntryType, $gId, $gDefPostDateStr, $gDefSubject, $gDefTextType, $gDefArticle, $gDefName, $gDefEmail, $gDefUrl, $gDefFmail );
    }
}

sub hg_b_search_article_form
{
    local( $SearchThread ) = &cgi'tag( 'searchthread' );
    local( $Key ) = &cgi'tag( 'key' );
    local( $SearchSubject ) = &cgi'tag( 'searchsubject' );
    local( $SearchPerson ) = &cgi'tag( 'searchperson' );
    local( $SearchArticle ) = &cgi'tag( 'searcharticle' );
    local( $SearchPostTimeFrom ) = &cgi'tag( 'searchposttimefrom' );
    local( $SearchPostTimeTo ) = &cgi'tag( 'searchposttimeto' );
    local( $SearchIcon ) = &cgi'tag( 'searchicon' );

    local( %iconHash );
    foreach ( &cgi'tag( 'icon' ))
    {
	next if ( $_ eq $H_NOICON );
	$iconHash{ $_ } = 1;
    }

    local( $msg, $contents );
    $contents = &tagInputCheck( 'searchsubject', $SearchSubject ) . ': ' . &tagLabel( $H_SUBJECT, 'searchsubject', 'T' ) . $HTML_BR;

    $contents .= &tagInputCheck( 'searchperson', $SearchPerson ) . ': ' . &tagLabel( "名前", 'searchperson', 'N' ) . $HTML_BR;

    $contents .= &tagInputCheck( 'searcharticle', $SearchArticle ) . ': ' . &tagLabel( $H_MESG, 'searcharticle', 'A' ) . $HTML_BR;

    $contents .= &tagLabel( 'キーワード', 'key', 'K' ) . ': ' . &tagInputText( 'text', 'key', $Key, $KEYWORD_LENGTH ) . $HTML_BR . $HTML_BR;

    $contents .= $H_DATE . ': ' . &tagInputText( 'text', 'searchposttimefrom', ( $SearchPostTimeFrom || '' ), 11 ) . ' ' .
	&tagLabel( 'から', 'searchposttimefrom', 'S' ) .
	"&nbsp;&nbsp;&nbsp;\n" .
	&tagInputText( 'text', 'searchposttimeto', ( $SearchPostTimeTo || '' ), 11 ) . &tagLabel( 'の間', 'searchposttimeto', 'E' ) . $HTML_BR;

    if ( $SYS_ICON )
    {
	$contents .= $HTML_BR . &tagLabel( $H_ICON, 'icon', 'I' ) . ": \n";

	# アイコンの選択
	local( $selContents, $iconId );
	foreach ( 0 .. &getNofBoardIcon() )
	{
	    $iconId = &getBoardIconId( $_ );
	    $selContents .= sprintf( "<option%s>$iconId</option>\n", ( $iconHash{ $iconId } )? ' selected="selected"' : '' );
	}
	$contents .= &tagSelect( 'icon', $selContents, $SELECT_ROWS, 1 ) . "\n";

	$contents .= "という$H_ICON\n";

	$selContents = sprintf( qq[<option%s value="0">&nbsp;</option>\n], ( $SearchIcon == 0 )? ' selected="selected"' : '' );
	$selContents .= sprintf( qq[<option%s value="1">である</option>\n], ( $SearchIcon == 1 )? ' selected="selected"' : '' );
	$selContents .= sprintf( qq[<option%s value="3">が$H_PARENTである</option>\n], ( $SearchIcon == 3 )? ' selected="selected"' : '' );
	$selContents .= sprintf( qq[<option%s value="2">という$H_REPLYを持つ</option>\n], ( $SearchIcon == 2 )? ' selected="selected"' : '' );
	$selContents .= qq(<option value="0">&nbsp;</option>\n);
	$selContents .= sprintf( qq[<option%s value="11">をスレッド中に含む</option>\n], ( $SearchIcon == 11 )? ' selected="selected"' : '' );
	$selContents .= sprintf( qq[<option%s value="12">がスレッドの先頭にある</option>\n], ( $SearchIcon == 12 )? ' selected="selected"' : '' );
	$selContents .= sprintf( qq[<option%s value="13">がスレッドの末端にある</option>\n], ( $SearchIcon == 13 )? ' selected="selected"' : '' );

	$contents .= &tagSelect( 'searchicon', $selContents );

	# アイコン一覧
	$contents .= ' (' . &linkP( "b=$BOARD_ESC&c=i", "使える$H_ICON一覧" .
	    &tagAccessKey( 'H' ), 'H' ) . ')' . $HTML_BR;

#	$contents .= &tagInputCheck( 'searchicon', $SearchIcon ) . ': ' . &tagLabel( $H_ICON, 'searchicon', 'I' ) . " // \n";

    }
    $contents .= $HTML_BR . &tagInputCheck( 'searchthread', $SearchThread ) . ': ' . &tagLabel( 'スレッドを検索する', 'searchthread', 'Z' ) . $HTML_BR;

    $msg .= &tagFieldset( "検索対象$HTML_BR", $contents ) . $HTML_BR;

    %tags = ( 'c', 's', 'b', $BOARD );
    &dumpForm( *tags, '検索', 'リセット', *msg );
}

sub hg_b_all_icon
{
    return unless $BOARD;
    $gHgStr .= "<ul>\n";

    local( $id );
    foreach ( 0 .. &getNofBoardIcon() )
    {
	$id = &getBoardIconId( $_ );
	$gHgStr .= '<li>' . &tagArtImg( $id ) . " : [$id] " . ( &getBoardIconHelp( $id ) || $id ) . "</li>\n";
    }
    $gHgStr .= "</ul>\n";
}


###
## dumpBoardHeader - 掲示板ヘッダの表示
#
# - SYNOPSIS
#	&dumpBoardHeader();
#
# - DESCRIPTION
#	掲示板のヘッダを表示する．
#
sub dumpBoardHeader
{
    local( $msg );
    &getBoardHeader( $BOARD, *msg );
    
    LINE: while ( 1 )
    {
	if (( index( $msg, '<kb' ) >= 0 ) &&
	    ( $msg =~ s!<kb:(\w+)(\s*var="([^"]*)")?\s+/>!!o ))
	{
	    $gHgStr .= $`;
	    eval( '&hg_' . $1 . '( "' . $source . '", "' . $3 . '" );' );
	    &fatal( 998, "$file : $@" ) if $@;
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
## dumpArtEntry - メッセージ入力フォームの表示
#
# - SYNOPSIS
#	&dumpArtEntry( $icon, $type, $id, $postDateStr, $title, $texttype, $article, $name, $eMail, $url, $fMail );
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
sub dumpArtEntry
{
    local( $icon ) = @_;

#    if ( &getBoardIconType( $icon ) eq 'cfv' )
#    {
#	# TBD
#    }
#    elsif ( &getBoardIconType( $icon ) eq 'vote' )
#    {
#	# TBD
#    }
#    else
#    {
	&dumpArtEntryNormal( @_ );
#    }
}


# 通常メッセージ
sub dumpArtEntryNormal
{
    local( $icon, $type, $id, $postDateStr, $title, $texttype, $article, $name, $eMail, $url, $fMail ) = @_;

    $texttype = $texttype || $H_TTLABEL[ $SYS_TT_DEFAULT ];
    $icon = $icon || $SYS_ICON_DEFAULT;

    local( $msg, $iconId );
    local( $contents ) = '';

    # アイコンの選択
    if ( $SYS_ICON )
    {
	$msg .= &tagLabel( $H_ICON, 'icon', 'I' ) . " :\n";
	$contents = sprintf( "<option%s>$H_NOICON</option>\n", (( $icon eq $H_NOICON )? ' selected="selected"' : '' ));
	foreach ( 0 .. &getNofBoardIcon() )
	{
	    $iconId = &getBoardIconId( $_ );
	    $contents .= sprintf( "<option%s>$iconId</option>\n", ( $iconId eq $icon )? ' selected="selected"' : '' );
	}
	$msg .= &tagSelect( 'icon', $contents ) . "\n";

	$msg .= '(' . &linkP( "b=$BOARD_ESC&c=i", "使える$H_ICON一覧" .
	    &tagAccessKey( 'H' ), 'H' ) . ')' . $HTML_BR;
    }

    $msg .= &tagLabel( $H_SUBJECT, 'subject', 'T' ) . ': ' .
	&tagInputText( 'text', 'subject', $title, $SUBJECT_LENGTH ) . $HTML_BR;
    
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
		    $contents .= &tagInputRadio( 'texttype_' . $ttBit, 'texttype', $H_TTLABEL[$ttBit], 1 );
		    $labelTarget = 'texttype_' . $ttBit;
		}
		else
		{
		    $contents .= &tagInputRadio( 'texttype_' . $ttBit, 'texttype', $H_TTLABEL[$ttBit], 0 );
		}
		$contents .= &tagLabel( $H_TTLABEL[$ttBit], 'texttype_' . $ttBit, '' );
	    }
	    $ttBit++;
	}
	$contents .= $HTML_BR;
	$msg .= &tagFieldset( &tagLabel( $H_TEXTTYPE, $labelTarget, 'Z' ) . ': ', $contents );
    }
    else
    {
	$msg .= sprintf( qq(<input name="texttype" type="hidden" value="%s" />), $H_TTLABEL[(( log $SYS_TEXTTYPE ) / ( log 2 ))] ) . $HTML_BR;
    }

    $msg .= &tagLabel( $H_MESG, 'article', 'A' ) . ':' . $HTML_BR .
	&tagTextarea( 'article', $article, $TEXT_ROWS, $TEXT_COLS ) . $HTML_BR;

    if ( $POLICY & 8 )
    {
	# 管理権限は特別扱い
	$msg .= &tagLabel( $H_DATE, 'postdate', 'T' ) . ': ' .
	    &tagInputText( 'text', 'postdate', $postDateStr, 20 ) .
	    qq[('yyyy/mm/dd(HH:MM:SS)'の形式で指定)] . $HTML_BR;
	$msg .= &tagLabel( $H_FROM, 'name', 'N' ) . ': ' .
	    &tagInputText( 'text', 'name', $name, $NAME_LENGTH ) . $HTML_BR;
	$msg .= &tagLabel( $H_MAIL, 'mail', 'M' ) . ': ' .
	    &tagInputText( 'text', 'mail', $eMail, $MAIL_LENGTH ) . $HTML_BR;
	$msg .= &tagLabel( $H_URL, 'url', 'U' ) . ': ' .
	    &tagInputText( 'text', 'url', ( $url || 'http://' ), $URL_LENGTH ) . $HTML_BR;
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
	$msg .= &tagLabel( $H_FROM, 'name', 'N' ) . ': ' .
	    &tagInputText( 'text', 'name', $name, $NAME_LENGTH ) . $HTML_BR;
	$msg .= &tagLabel( $H_MAIL, 'mail', 'M' ) . ': ' .
	    &tagInputText( 'text', 'mail', $eMail, $MAIL_LENGTH ) . $HTML_BR;
	$msg .= &tagLabel( $H_URL, 'url', 'U' ) . ': ' .
	    &tagInputText( 'text', 'url', ( $url || 'http://' ), $URL_LENGTH ) . $HTML_BR;
    }

    if (( $SYS_MAIL & 2 ) && ( $UMAIL ne '' ))
    {
	$msg .= &tagLabel( "リプライがあった時に$H_MAILで連絡", 'fmail', 'F' ) . ': ' . &tagInputCheck( 'fmail', $fMail ) . "\n";
    }
    $msg .= "</p>\n<p>\n";

    $contents = &tagInputRadio( 'com_p', 'com', 'p', 1 ) . ":\n" .
	&tagLabel( '試しに表示してみる(まだ登録しません)', 'com_p', 'P' ) .
	$HTML_BR;
    local( $doLabel );
    if ( $type eq 'supersede' )
    {
	$doLabel = '訂正する';
    }
    else
    {
	$doLabel = "$H_MESGを登録する";
    }
    $contents .= &tagInputRadio( 'com_x', 'com', 'x', 0 ) . ":\n" .
	&tagLabel( $doLabel, 'com_x', 'X' ) . $HTML_BR;
    $msg .= &tagFieldset( "コマンド$HTML_BR", $contents );

    local( $op ) = ( -M &getPath( $SYS_DIR, $BOARD_FILE ));
    local( %tags ) = ( 'corig', scalar( &cgi'tag( 'c' )), 'b', $BOARD, 'c', 'p', 'id', $id, 's', ( $type eq 'supersede' ), 'op', $op );

    &dumpForm( *tags, '実行', '', *msg );
}


###
## dumpArtBody - メッセージ本体の表示
#
# - SYNOPSIS
#	&dumpArtBody( $Id, $CommandFlag, $OriginalFlag, @articleInfo );
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
sub dumpArtBody
{
    local( $id, $commandFlag, $origFlag, @articleInfo ) = @_;

    local( $fid, $aids, $date, $title, $icon, $host, $name, $eMail, $url );

    local( $body ) = '';
    if ( $id ne '' )
    {
	( $fid, $aids, $date, $title, $icon, $host, $name, $eMail, $url ) = &getArtInfo( $id );
	local( @articleBody );
	&getArtBody( $id, $BOARD, *articleBody );
	$body = join( '', @articleBody );
    }
    else
    {
	( $fid, $aids, $date, $title, $icon, $host, $name, $eMail, $url, $body ) = @articleInfo;
    }

    # 未投稿記事は読めない
    &fatal( 8, '' ) if ( $title eq '' );

    $gHgStr .= qq(<div class="kbArticle">\n);

    # タイトル
    &dumpArtTitle( $id, $title, $icon );

    local( $origId );
    if ( $fid ne '' )
    {
	( $origId = $fid ) =~ s/,.*$//o;
    }

    if ( $commandFlag && $SYS_COMMAND )
    {
	local( $num ) = &getArtNum( $id );
	local( $prevId ) = &getArtId( $num - 1 );
	local( $nextId ) = &getArtId( $num + 1 );
	&dumpArtCommand( $id, $origId, $prevId, $nextId, ( $aids ne '' ),
	    (( &isUser( $name ) && (( $aids eq '' ) || ( $SYS_OVERWRITE == 2 ))) || ( $POLICY & 8 )));
    }

    # ヘッダ（ユーザ情報とリプライ元: タイトルは除く）
    &dumpArtHeader( $name, $eMail, $url, $host, $date, ( $origFlag? $origId : '' ));

    # 切れ目
    $gHgStr .= $H_LINE;

#    if ( &getBoardIconType( $icon ) eq 'cfv' )
#    {
#	# TBD
#    }
#    elsif ( &getBoardIconType( $icon ) eq 'vote' )
#    {
#	# TBD
#    }
#    else
#    {
	&dumpArtBodyNormal( *body );
#    }

    $gHgStr .= "</div>\n";

    &cgiprint'cache( $gHgStr ); $gHgStr = '';
}


# 通常メッセージ
sub dumpArtBodyNormal
{
    local( *body ) = @_;
    $gHgStr .= qq(<div class="body">) . &articleEncode( *body ) . "</div>\n";
}


###
## dumpArtThread - フォロー記事を全て表示．
#
# - SYNOPSIS
#	&dumpArtThread( $State, $Head, @Tail );
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
#	詳細は&getFollowIdTreeのインプリメント部分を参照のこと．
#
sub dumpArtThread
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
	    local( $dFid, $dAids, $dDate, $dSubject, $dIcon, $dRemoteHost, $dName ) = &getArtInfo( $Head );
	    &dumpArtSummaryItem( $Head, $dAids, $dDate, $dSubject, $dIcon, $dName, $State&3 );
	    $gHgStr .= "</li>\n";
	    $State ^= 1 if ( $State&1 );
	}
    }
    elsif (( $Head ne '(' ) && ( $Head ne ')' ))
    {
	# 元記事の表示(コマンド付き, 元記事なし)
	$gHgStr .= $HTML_HR;
	&dumpArtBody( $Head, $SYS_COMMAND_EACH, 0 );
    }

    &cgiprint'cache( $gHgStr ); $gHgStr = '';
    # tail recuresive.
    &dumpArtThread( $State, @Tail ) if @Tail;
}


###
## dumpSearchResult - 記事検索
#
# - SYNOPSIS
#	&dumpSearchResult( $type, $Key, $Subject, $Person, $Article, $PostTimeFrom, $PostTimeTo, $IconType, *iconHash );
#
# - ARGS
#	$type		表示形式
#			  0 ... メッセージ表示
#			  1 ... スレッド表示
#	$Key		キーワード
#	$Subject	タイトルを検索するか否か
#	$Person		投稿者を検索するか否か
#	$Article	本文を検索するか否か
#	$PostTimeFrom	開始日付
#	$PostTimeTo	終了日付
#	$IconType	アイコンの検索手法
#	%iconHash	検索アイコン用ハッシュ．
#			  $iconHash{ 'アイコン' }が真のアイコンが検索される．
#
# - DESCRIPTION
#	記事を検索して表示する
#
sub dumpSearchResult
{
    local( $type, $Key, $Subject, $Person, $Article, $PostTimeFrom, $PostTimeTo, $IconType, *iconHash ) = @_;

    local( @KeyList ) = split( /\s+/, $Key );
    local( $postTime ) = ( $PostTimeTo || $PostTimeFrom );

    # リスト開く
    $gHgStr .= "<ul>\n";

    # アイコン検索のキャッシュをクリア
    %gSearchIconResult = ();

    # スレッド表示用キャッシュ
    local( %dumpThread );

    local( $dId, $dFid, $dAids, $dDate, $dTitle, $dIcon, $dRemoteHost, $dName, $dEmail );
    local( $SubjectFlag, $PersonFlag, $PostTimeFlag, $ArticleFlag );
    local( $HitNum, $Line, $FromUtc, $ToUtc );
    foreach ( $[ .. &getNofArt() )
    {
	# 記事情報
	$dId = &getArtId( $_ );
	( $dFid, $dAids, $dDate, $dTitle, $dIcon, $dRemoteHost, $dName, $dEmail ) = &getArtInfo( $dId );

	# 変数のリセット
	$SubjectFlag = $PersonFlag = $PostTimeFlag = $ArticleFlag = 0;
	$Line = '';

	# アイコンチェック
	next if ( $IconType && !&searchArticleIcon( $dId, $IconType, *iconHash ));

	# 投稿時刻を検索
	if ( $postTime )
	{
	    $FromUtc = $ToUtc = -1;
	    $FromUtc = &getUtcFromYYYY_MM_DD( $PostTimeFrom ) if $PostTimeFrom;
	    $ToUtc = &getUtcFromYYYY_MM_DD( $PostTimeTo ) if $PostTimeTo;
	    $ToUtc += 86400 if ( $ToUtc >= 0 );
	    next if !&checkSearchTime( $dDate, $FromUtc, $ToUtc );
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
		if ( $Line = &searchArticleKeyword( $dId, $BOARD, @KeyList ))
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

	next unless ( $SubjectFlag || $PersonFlag || $ArticleFlag );

	# スレッド表示の場合
	if ( $type == 1 )
	{
	    next if ( defined( $dumpThread[ &getArtParentTop( $dId ) ] ));

	    # スレッド先頭記事が合致したものとする．
	    $dId = &getArtParentTop( $dId );
	    $dumpThread[ $dId ] = 1;
	    ( $dFid, $dAids, $dDate, $dTitle, $dIcon, $dRemoteHost, $dName, $dEmail ) = &getArtInfo( $dId );
	}

	# 合致件数のカウント
	$HitNum++;

	# 記事へのリンクを表示
	&dumpArtSummaryItem( $dId, $dAids, $dDate, $dTitle, $dIcon, $dName, 1 );

	# 本文に合致した場合は本文も表示
	if ( $ArticleFlag )
	{
	    $Line =~ s/<[^>]*>//go;
	    $gHgStr .= "<blockquote>$Line</blockquote>\n";
	}
	$gHgStr .= "</li>\n";
    }

    # 検索対象を表す文字列
    local( $target );
    if ( $type == 0 )
    {
	$target = $H_MESG;
    }
    elsif ( $type == 1 )
    {
	$target = 'スレッド';
    }

    if ( $HitNum )
    {
	$gHgStr .= "</ul>\n<ul>\n";
	$gHgStr .= "<li>$HitNum件の$targetが見つかりました．</li>\n";
    }
    else
    {
	$gHgStr .= "<li>該当する$targetは見つかりませんでした．</li>\n";
    }

    # リスト閉じる
    $gHgStr .= "</ul>\n";
}


###
## dumpOriginalArticles - オリジナル記事へのリンクの表示
#
# - SYNOPSIS
#	&dumpOriginalArticles( $fids );
#
# - ARGS
#	$fids	オリジナル記事IDデータ
#
# - DESCRIPTION
#	オリジナル記事へのリンクを表示する．
#
sub dumpOriginalArticles
{
    if ( $_[0] ne '' )
    {
	# オリジナル記事があるなら…

	$gHgStr .= "<ul>\n";

	local( $dId, $dFid, $dAids, $dDate, $dTitle, $dIcon, $dHost, $dName );
	foreach $dId ( reverse( split( /,/, $_[0] )))
	{
	    ( $dFid, $dAids, $dDate, $dTitle, $dIcon, $dHost, $dName ) = &getArtInfo( $dId );
	    &dumpArtSummaryItem( $dId, $dAids, $dDate, $dTitle, $dIcon, $dName, 0 );
	}
	$gHgStr .= "</ul>\n";
    }
    else
    {
	# なにも表示しない．
    }
}


###
## dumpReplyArticles - リプライ記事へのリンクの表示
#
# - SYNOPSIS
#	&dumpReplyArticles( $aids );
#
# - ARGS
#	$aids	リプライ記事IDデータ
#
# - DESCRIPTION
#	リプライ記事へのリンクを表示する．
#
sub dumpReplyArticles
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
	    &getFollowIdTree( $id, *tree );
	    
	    # メイン関数の呼び出し(記事概要)
	    &dumpArtThread( 4, @tree );
	}
    }
    else
    {
	# 反応記事無し

	$gHgStr .= "<ul>\n<li>現在，この$H_MESGへの$H_REPLYはありません</li>\n</ul>\n";
    }
}


###
## dumpArtTitle - 記事タイトルの表示
#
# - SYNOPSIS
#	&dumpArtTitle( $id, $title, $icon );
#
# - ARGS
#	$id	記事ID
#	$title	タイトル
#	$icon	アイコン
#
sub dumpArtTitle
{
    local( $id, $title, $icon ) = @_;
    local( $markUp );

    if ( $id ne '' )
    {
	$markUp .= &tagArtImg( $icon ) . " <small>$id.</small> " . $title;
    }
    else
    {
	$markUp .= &tagArtImg( $icon ) . ' ' . $title;
    }
    $gHgStr .= '<h2>' . &tagA( $markUp, '', '', '', "a$id" ) . "</h2>\n";
}


###
## dumpArtCommand - 記事コマンドの表示
#
# - SYNOPSIS
#	&dumpArtCommand( $id, $upId, $prevId, $nextId, $reply, $delete );
#
# - ARGS
#	$id	記事ID
#	$upId	上記事ID
#	$prevId	前記事ID
#	$nextId	次記事ID
#	$reply	リプライ記事があるか
#	$delete	削除・訂正が可能か
#
sub dumpArtCommand
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
	$gHgStr .= &linkP( "b=$BOARD_ESC&c=e&id=$upId", &tagComImg( $ICON_UP, $H_UPARTICLE ), 'U' ) . "\n";
    }
    else
    {
	$gHgStr .= &tagComImg( $ICON_UP_X, $H_UPARTICLE, ) . "\n";
    }
	
    if ( $prevId ne '' )
    {
	$gHgStr .= $dlmtS . &linkP( "b=$BOARD_ESC&c=e&id=$prevId", &tagComImg( $ICON_PREV, $H_PREVARTICLE ), 'P' ) . "\n";
    }
    else
    {
	$gHgStr .= $dlmtS . &tagComImg( $ICON_PREV_X, $H_PREVARTICLE, ) . "\n";
    }
	
    if ( $nextId ne '' )
    {
	$gHgStr .= $dlmtS . &linkP( "b=$BOARD_ESC&c=e&id=$nextId", &tagComImg( $ICON_NEXT, $H_NEXTARTICLE ), 'N' ) . "\n";
    }
    else
    {
	$gHgStr .= $dlmtS . &tagComImg( $ICON_NEXT_X, $H_NEXTARTICLE, ) . "\n";
    }

    if ( $reply )
    {
	$gHgStr .= $dlmtS . &linkP( "b=$BOARD_ESC&c=t&id=$id", &tagComImg( $ICON_DOWN, $H_THREAD_L ), 'M' ) . "\n";
    }
    else
    {
	$gHgStr .= $dlmtS . &tagComImg( $ICON_DOWN_X, $H_THREAD_L ) . "\n";
    }

    $gHgStr .= $dlmtL;

    if ( $POLICY & 2 )
    {
	if ( $SYS_REPLYQUOTE )
	{
	    $gHgStr .= $dlmtS . &linkP( "b=$BOARD_ESC&c=q&id=$id", &tagComImg( $ICON_QUOTE, $H_REPLYTHISARTICLE ), 'Q' ) . "\n";
	}
	else
	{
	    $gHgStr .= $dlmtS . &linkP( "b=$BOARD_ESC&c=f&id=$id", &tagComImg( $ICON_FOLLOW, $H_REPLYTHISARTICLE ), 'R' ) . "\n";
	}
    }
    else
    {
	if ( $SYS_REPLYQUOTE )
	{
	    $gHgStr .= $dlmtS . &tagComImg( $ICON_QUOTE_X, $H_REPLYTHISARTICLE ) . "\n";
	}
	else
	{
	    $gHgStr .= $dlmtS . &tagComImg( $ICON_FOLLOW_X, $H_REPLYTHISARTICLE ) . "\n";
	}
    }

    if ( $SYS_AUTH )
    {
	$gHgStr .= $dlmtL;

	if ( $delete )
	{
	    $gHgStr .= $dlmtS . &linkP( "b=$BOARD_ESC&c=f&s=on&id=$id",
		&tagComImg( $ICON_SUPERSEDE, $H_SUPERSEDE ), 'S' ) . "\n" .
		$dlmtS . &linkP( "b=$BOARD&c=dp&id=$id",
		&tagComImg( $ICON_DELETE, $H_DELETE ), 'D' ) . "\n";
	}
	else
	{
	    $gHgStr .= $dlmtS . &tagComImg( $ICON_SUPERSEDE_X, $H_SUPERSEDE ) .
	    	"\n" . $dlmtS . &tagComImg( $ICON_DELETE_X, $H_DELETE ) . "\n";
	}
    }

    if ( $SYS_COMICON == 1 )
    {
	$gHgStr .= $dlmtL;
	$gHgStr .= $dlmtS . &linkP( "b=$BOARD_ESC&c=h", &tagComImg( $ICON_HELP, 'ヘルプ' ), 'H', '', '', 'message' ) . "\n";
    }
    $gHgStr .= qq(</p>\n);
}


###
## dumpArtHeader - 記事ヘッダ（タイトル除く）の表示
#
# - SYNOPSIS
#	&dumpArtHeader( $name, $eMail, $url, $host, $date, $origId );
#
# - ARGS
#	$name		ユーザ名
#	$eMail		メイルアドレス
#	$url		URL
#	$host		Remote Host名
#	$date		日付（UTC）
#	$origId		リプライ元記事ID
#
sub dumpArtHeader
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
	$gHgStr .= "<strong>$H_FROM</strong>: " . &tagA( $name, $url );
    }

    # メイル
    if ( $SYS_SHOWMAIL && $eMail )
    {
	$gHgStr .= ' ' . &tagA( "&lt;$eMail&gt;", "mailto:$eMail" );
    }
    $gHgStr .= $HTML_BR;

    # マシン
    $gHgStr .= "<strong>$H_HOST</strong>: $host" . $HTML_BR if $SYS_SHOWHOST;

    # 投稿日
    $gHgStr .= "<strong>$H_DATE</strong>: " . &getDateTimeFormatFromUtc( $date ) . $HTML_BR;

    # リプライ元へのリンク
    if ( $origId )
    {
	( $dFid, $dAids, $dDate, $dTitle, $dIcon, $dHost, $dName ) = &getArtInfo( $origId );
	$gHgStr .= "<strong>$H_PARENT:</strong> ";
	&dumpArtSummary( $origId, $dAids, $dDate, $dTitle, $dIcon, $dName, 0 );
	$gHgStr .= $HTML_BR;
    }

    # 切れ目
    $gHgStr .= "</p>\n";
}


###
## dumpButtonToTitleList - タイトル一覧ボタンの表示
#
# - SYNOPSIS
#	&dumpButtonToTitleList( $board, $id );
#
# - ARGS
#	$board		掲示板ID
#	$id		ジャンプ先メッセージID
#			このメッセージIDを含むタイトル一覧にジャンプする．
#
# - DESCRIPTION
#	タイトル一覧へジャンプするためのボタンを表示する
#
sub dumpButtonToTitleList
{
    local( $board, $id ) = @_;
    local( $old ) = $id? &getTitleOldIndex( $id ) : 0;

    if  ( $SYS_COMMAND_BUTTON )
    {
	local( %tags ) = ( 'b', $board, 'c', 'v', 'num', $DEF_TITLE_NUM, 'old',
	    $old );
	&dumpForm( *tags, "$H_BACKTITLEREPLY(B)", '', '' );

	%tags = ( 'b', $board, 'c', 'r', 'num', $DEF_TITLE_NUM, 'old', $old );
	&dumpForm( *tags, $H_BACKTITLEDATE, '', '' );
    }
    else
    {
	local( $boardEsc ) = &uriEscape( $board );
	$gHgStr .= "<p>" . &linkP( "b=$boardEsc&c=v&num=$DEF_TITLE_NUM&old=$old", $H_BACKTITLEREPLY . &tagAccessKey( 'B' ), 'B' ) . "</p>\n";
	$gHgStr .= "<p>" . &linkP( "b=$boardEsc&c=r&num=$DEF_TITLE_NUM&old=$old", $H_BACKTITLEDATE ) .
	    "</p>\n";
    }
}


###
## dumpButtonToArticle - メッセージへジャンプするボタンの表示
#
# - SYNOPSIS
#	&dumpButtonToArticle( $board, $id, $msg );
#
# - ARGS
#	$board	掲示板ID
#	$id	メッセージID
#	$msg	リンク文字列
#
# - DESCRIPTION
#	メッセージへジャンプするためのボタンを表示する
#
sub dumpButtonToArticle
{
    local( $board, $id, $msg ) = @_;

    if  ( $SYS_COMMAND_BUTTON )
    {
	local( %tags ) = ( 'b', $board, 'c', 'e', 'id', $id );
	&dumpForm( *tags, "$msg(N)", '', '' );
    }
    else
    {
	local( $boardEsc ) = &uriEscape( $board );
	$gHgStr .= "<p>" . &linkP( "b=$boardEsc&c=e&id=$id", $msg .
	    &tagAccessKey( 'N' ), 'N' ) . "</p>\n";
    }
}


###
## dumpForm - フォームタグのフォーマット
#
# - SYNOPSIS
#	&dumpForm( *hiddenTags, $submit, $reset, *contents );
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
sub dumpForm
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
    $gHgStr .= "$contents\n" . &tagInputSubmit( 'submit', $submit, $accessKey );
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
	$gHgStr .= ' ' . &tagInputSubmit( 'reset', $reset, $accessKey ) . "\n";
    }
    $gHgStr .= "</p>\n</form>\n";
}


###
## dumpArtSummary - タイトルリストのフォーマット
#
# - SYNOPSIS
#	&dumpArtSummary( $id, $aids, $date, $subject, $icon, $name, $flag);
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
sub dumpArtSummary
{
    local( $id, $aids, $date, $subject, $icon, $name, $flag ) = @_;

    $subject = $subject || $id;
    $name = $name || $MAINT_NAME;

    $gHgStr .= qq(<span class="kbTitle">);	# 初期化

    if ( $flag&1 && ( &getArtParents( $id ) ne '' ))
    {
	local( $fId );
	$fId = &getArtParentTop( $id );
	$gHgStr .= ' ' . &linkP( "b=$BOARD_ESC&c=t&id=$fId", $H_THREAD_ALL, '', $H_THREAD_ALL_L ) . ' ';
    }

    $gHgStr .= &tagArtImg( $icon ) . " <small>$id.</small> " .
	(( $flag&2 )? &tagA( $subject, "$cgi'REQUEST_URI#a$id" ) :
	&linkP( "b=$BOARD_ESC&c=e&id=$id", $subject ));

    if ( $aids )
    {
	$gHgStr .= ' ' . &linkP( "b=$BOARD_ESC&c=t&id=$id", $H_THREAD, '', $H_THREAD_L );
    }

    $gHgStr .= " [$name] ";
    $gHgStr .= &getDateTimeFormatFromUtc( $date ) if $date;

    $gHgStr .= ' ' . &tagArtImg( $H_NEWARTICLE ) if &getArtNewP( $id );
    $gHgStr .= "</span>\n";
}


###
## dumpArtSummaryItem - タイトルリストのフォーマット（<li>つき）
#
# - SYNOPSIS
#	&dumpArtSummaryItem(同上);
#
# - ARGS
#	同上
#
# - DESCRIPTION
#	ある記事をタイトルリスト表示用にフォーマットする．<li>つき
#
sub dumpArtSummaryItem
{
    $gHgStr .= '<li>';
    &dumpArtSummary;
}


######################################################################
# ロジックインプリメンテーション


#### 表示関連ロジック


###
## htmlEncode/htmlDecode - 特殊文字のHTML用EncodeとDecode
#
# - SYNOPSIS
#	&htmlEncode($Str);
#	&htmlDecode($Str);
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
sub htmlEncode
{
    local( $_ ) = @_;
    s/\&/&amp;/go;
    s/\"/&quot;/go;
    s/\>/&gt;/go;
    s/\</&lt;/go;
    $_;
}

sub htmlDecode
{
    local( $_ ) = @_;
    s/&quot;/\"/gio;
    s/&gt;/\>/gio;
    s/&lt;/\</gio;
    s/&amp;/\&/gio;
    $_;
}


###
## uriEscape - URIのescape
#
# - SYNOPSIS
#	&uriEscape( $str );
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
sub uriEscape
{
    local( $_ ) = @_;
    s/([^A-Za-z0-9\\\-_\.!~*'() ])/sprintf( "%%%02X", ord( $1 ))/eg;
    s/ /+/go;
    $_;
}


###
## tagEncode - 特殊文字のTAG埋め込み用Encode
#
# - SYNOPSIS
#	&tagEncode( *str );
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
sub tagEncode
{
    local( *str ) = @_;
#    $str =~ s/[\&\"]//go;
    $str =~ s/<[^>]*>//go;
}


###
## articleEncode - 記事のEncode
#
# - SYNOPSIS
#	&articleEncode( *article );
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
sub articleEncode
{
    local( *article ) = @_;

    local( $retArticle ) = $article;

    local( $url, $urlMatch, @cache );
    local( $tagStr, $quoteStr );
    while ( $article =~ m/\[url:([^\]]+)\]/gio )
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
		local( $boardEsc ) = &uriEscape( $1 );
		$tagStr = &linkP( "b=$boardEsc&c=e&id=$2", $quoteStr );
	    }
	    else
	    {
		$tagStr = &linkP( "b=$BOARD_ESC&c=e&id=$artStr", $quoteStr );
	    }
	}
	elsif ( &isUrl( &htmlDecode( $urlMatch )))
	{
	    $tagStr = &tagA( $quoteStr, &htmlDecode( $url ), '', '', '', $SYS_LINK_TARGET );
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
## plainArticleToPreFormatted - Plain記事をpre formatted textに変換
#
# - SYNOPSIS
#	&plainArticleToPreFormatted(*Article);
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
sub plainArticleToPreFormatted
{
    local( *Article ) = @_;
    $Article =~ s/\n*$//o;
    $Article = &htmlEncode( $Article );	# no tags are allowed.
    $Article = "<pre>\n" . $Article . "</pre>";
}


###
## plainArticleToHtml - Plain記事をHTMLに変換
#
# - SYNOPSIS
#	&plainArticleToHtml(*Article);
#
# - ARGS
#	*Article	変換する記事本文
#
# - DESCRIPTION
#	記事末尾の無意味な改行を取り除く．
#	各段落を<p>で囲む．
#	*Articleを破壊する．
#
sub plainArticleToHtml
{
    local( *Article ) = @_;
    $Article =~ s/^\n*//o;
    $Article =~ s/\n*$//o;
    $Article =~ s/\n/$HTML_BR/go;
    $Article =~ s/$HTML_BR($HTML_BR)+/<\/p>\n\n<p>/go;
    $Article = "<p>$Article</p>";
}


###
## quoteOriginalArticle - 引用する(引用符あり)
#
# - SYNOPSIS
#	&quoteOriginalArticle($Id);
#
# - ARGS
#	$Id		記事ID
#
# - DESCRIPTION
#	記事を引用して表示する
#
sub quoteOriginalArticle
{
    local( $Id, *msg ) = @_;

    # 元記事情報の取得
    local( $fid, $aids, $date, $subject, $icon, $remoteHost, $name, $eMail, $url ) = &getArtInfo( $Id );

    # 元記事のさらに元記事情報
    local( $pName ) = '';
    if ( $fid )
    {
	local( $pId );
	( $pId = $fid ) =~ s/,.*$//o;
	( $pName ) = &getArtAuthor( $pId );
    }

    # 引用
    local( @ArticleBody );
    &getArtBody( $Id, $BOARD, *ArticleBody );

    if ( $SYS_QUOTEMSG )
    {
	local( $premsg ) = $SYS_QUOTEMSG;
	$premsg =~ s/__LINK__/[url:kb:$Id]/i;
	$premsg =~ s/__TITLE__/$subject/;
	$premsg =~ s/__DATE__/&getDateTimeFormatFromUtc( $date )/e;
	$premsg =~ s/__NAME__/$name/;
	$msg .= $premsg;
    }
    local( $QMark, $line );
    foreach $line ( @ArticleBody )
    {
	&tagEncode( *line );

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
## quoteOriginalArticleWithoutQMark - 引用する(引用符なし)
#
# - SYNOPSIS
#	&quoteOriginalArticleWithoutQMark($Id);
#
# - ARGS
#	$Id		記事ID
#
# - DESCRIPTION
#	記事を引用して表示する
#
sub quoteOriginalArticleWithoutQMark
{
    local( $Id, *msg ) = @_;

    local( @ArticleBody, $line );
    &getArtBody( $Id, $BOARD, *ArticleBody );
    foreach $line ( @ArticleBody )
    {
	if ( $SYS_TAGINSUPERSEDE )
	{
	    $line = &htmlEncode( $line );
	}
	else
	{
	    &tagEncode( *line );
	}
	$msg .= $line;
    }
}


###
## pageLink - ページヘッダ/フッタの表示
#
# - SYNOPSIS
#	&pageLink( $com, $num, $old, $rev, $fold );
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
sub pageLink
{
    local( $com, $num, $old, $rev, $fold ) = @_;

    local( $nextOld ) = ( $old > $num )? ( $old - $num ) : 0;
    local( $backOld ) = ( $old + $num );

    local( $str );
    $str = '<p class="kbPageLink">';

    if ( $old )
    {
	$str .= &linkP( "b=$BOARD_ESC&c=$com&num=$num&old=0&fold=$fold&rev=$rev", '&lt;&lt;' . $H_TOP . &tagAccessKey( 'T' ), 'T', $H_TOP );
	$str .= ' | ' . &linkP( "b=$BOARD_ESC&c=$com&num=$num&old=$nextOld&fold=$fold&rev=$rev", '&lt;' . $H_UP . &tagAccessKey( 'N' ), 'N', $H_UP );
    }
    else
    {
	$str .= '&lt;&lt;' . $H_TOP . &tagAccessKey( 'T' ) . ' | ' . '&lt;' . $H_UP . &tagAccessKey( 'N' );
    }

    if ( $SYS_REVERSE )
    {
	$str .= ' | ' .
	    &linkP( "b=$BOARD_ESC&c=$com&num=$num&old=$old&fold=$fold&rev=" . ( 1-$rev ), $H_REVERSE[ 1-$rev ] . &tagAccessKey( 'R' ), 'R', $H_REVERSE_L );
    }

    if ( $SYS_EXPAND && ( $fold ne '' ))
    {
	$str .= ' | ' . &linkP( "b=$BOARD_ESC&c=$com&num=$num&old=$old&rev=$rev&fold=" . ( 1-$fold ), $H_EXPAND[ 1-$fold ] . &tagAccessKey( 'E' ), 'E', $H_EXPAND_L );
    }

    $str .= ' | ';

    local( $nofMsg ) = &getNofArt();
    if ( $num && ( $nofMsg - $backOld >= 0 ))
    {
	$str .= &linkP( "b=$BOARD_ESC&c=$com&num=$num&old=$backOld&fold=$fold&rev=$rev", $H_DOWN . &tagAccessKey( 'P' ) . '&gt;', 'P', $H_DOWN );
	$str .= ' | ' . &linkP( "b=$BOARD_ESC&c=$com&num=$num&old=" . ( $nofMsg - $num + 1 ) . "&fold=$fold&rev=$rev", $H_BOTTOM . &tagAccessKey( 'B' ) . '&gt;&gt;' , 'B', $H_BOTTOM );
    }
    else
    {
	$str .= $H_DOWN . &tagAccessKey( 'P' ) . '&gt;' . ' | ' . $H_BOTTOM . &tagAccessKey( 'B' ) . '&gt;&gt;';
    }

    $str .= "</p>\n";

    $str;
}


###
## tagImg - イメージタグのフォーマット
#
# - SYNOPSIS
#	&tagImg( $src, $alt, $width, $height, $class );
#
# - ARGS
#	$src		ソースイメージのURL
#	$alt		altタグ用の文字列
#	$width		width
#	$height		height
#	$class		class用文字列
#
# - DESCRIPTION
#	イメージを表示用タグにフォーマットする．
#
sub tagImg
{
    local( $src, $alt, $width, $height, $class ) = @_;
    qq(<img src="$src" alt="$alt" width="$width" height="$height" class="$class" />);
}


###
## tagComImg - コマンドアイコン用イメージタグのフォーマット
#
# - SYNOPSIS
#	&tagComImg( $src, $alt );
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
sub tagComImg
{
    local( $src, $alt ) = @_;
    if ( $SYS_COMICON == 1 )
    {
	&tagImg( $src, $alt, $COMICON_WIDTH, $COMICON_HEIGHT, 'kbComIcon' );
    }
    elsif ( $SYS_COMICON == 2 )
    {
	&tagImg( $src, $alt, $COMICON_WIDTH, $COMICON_HEIGHT, 'kbComIcon' ) . $alt;
    }
    else
    {
	$alt;
    }
}


###
## tagArtImg - 記事アイコン用イメージタグのフォーマット
#
# - SYNOPSIS
#	&tagArtImg( $icon );
#
# - ARGS
#	$icon		アイコンタイプ
#
# - DESCRIPTION
#	イメージを表示用タグにフォーマットする．
#
sub tagArtImg
{
    local( $icon ) = @_;

    if ( !$icon || $icon eq $H_NOICON )
    {
	return "";
    }
    elsif ( $SYS_ICON )
    {
	local( $src ) = &getIconUrlFromTitle( $icon );
	&tagImg( $src, "[$icon]", $MSGICON_WIDTH, $MSGICON_HEIGHT, 'kbMsgIcon' );
    }
    else
    {
	return "[$icon]";
    }
}


###
## tagA - リンクタグのフォーマット
#
# - SYNOPSIS
#	&tagA();
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
sub tagA
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
## tagAccessKey - アクセスキーラベルのフォーマット
#
# - SYNOPSIS
#	&tagAccessKey( $key );
#
# - ARGS
#	$key		キー1文字
#
sub tagAccessKey
{
    qq{(<span class="kbAccessKey">$_[0]</span>)};
}


###
## tagLabel - ラベルタグのフォーマット
#
# - SYNOPSIS
#	&tagLabel( $markUp, $label, $accessKey );
#
# - ARGS
#	$markUp		マークアップ文字列
#	$label		ラベル対象コントロール
#	$accessKey	アクセスキー
#
sub tagLabel
{
    local( $markUp, $label, $accessKey ) = @_;
    if ( $accessKey )
    {
	qq[<label for="$label" accesskey="$accessKey">$markUp] . &tagAccessKey( $accessKey ) . "</label>";
    }
    else
    {
	qq[<label for="$label">$markUp</label>];
    }
}


###
## tagInputSubmit - submit/resetボタンタグのフォーマット
#
# - SYNOPSIS
#	&tagInputSubmit( $type, $value, $key );
#
# - ARGS
#	$type	submit/reset
#	$value	ラベルに使われる
#	$key	accesskeyに使われる
#
sub tagInputSubmit
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
## tagInputText - 入力タグのフォーマット
#
# - SYNOPSIS
#	&tagInputText( $type, $id, $value, $size );
#
# - ARGS
#	$type	text/password
#	$id	idとnameに使われる
#	$value	デフォルト値に使われる
#	$size	sizeに使われる
#
sub tagInputText
{
    local( $type, $id, $value, $size ) = @_;
    $gTabIndex++;
    qq(<input type="$type" id="$id" name="$id" value="$value" size="$size" tabindex="$gTabIndex" />);
}


###
## tagInputCheck - チェックボックスタグのフォーマット
#
# - SYNOPSIS
#	&tagInputCheck( $id, $checked );
#
# - ARGS
#	$id		idとnameに使われる
#	$checked	trueならcheckedが付く
#
# - DESCRIPTION
#	valueは"on"固定．
#
sub tagInputCheck
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
## tagInputRadio - ラジオボタンタグのフォーマット
#
# - SYNOPSIS
#	&tagInputRadio( $id, $name, $value, $checked );
#
# - ARGS
#	$id		idに使われる
#	$name		nameに使われる
#	$value		デフォルト値に使われる
#	$checked	trueならcheckedが付く
#
sub tagInputRadio
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
## tagTextarea - textareaタグのフォーマット
#
# - SYNOPSIS
#	&tagTextarea( $id, $value, $rows, $cols );
#
# - ARGS
#	$id	idとnameに使われる
#	$value	デフォルト値に使われる
#	$rows	rowsに使われる
#	$cols	colsに使われる
#
sub tagTextarea
{
    local( $id, $value, $rows, $cols ) = @_;
    $gTabIndex++;
    qq(<textarea id="$id" name="$id" rows="$rows" cols="$cols" tabindex="$gTabIndex">$value</textarea>);
}


###
## tagSelect - selectタグのフォーマット
#
# - SYNOPSIS
#	&tagSelect( $id, $contents, $size, $multiple );
#
# - ARGS
#	$id		idとnameに使われる
#	$contents	選択肢用コンテンツ
#	$size		sizeに使われる．省略時は1
#	$multiple	trueなら複数選択可
#
sub tagSelect
{
    local( $id, $contents, $size, $multiple ) = @_;
    $gTabIndex++;
    $size = 1 unless $size;
    if ( $multiple )
    {
	qq(<select id="$id" name="$id" size="$size" multiple="multiple" tabindex="$gTabIndex">$contents</select>);
    }
    else
    {
	qq(<select id="$id" name="$id" size="$size" tabindex="$gTabIndex">$contents</select>);
    }
}


###
## tagFieldset - fieldsetタグのフォーマット
#
# - SYNOPSIS
#	&tagFieldset( $title, $contents );
#
# - ARGS
#	$title		legendに使われる
#	$contents	fieldsetのコンテンツ
#
sub tagFieldset
{
    local( $title, $contents ) = @_;
    qq(<fieldset>\n<legend>$title</legend>\n$contents</fieldset>\n);
}


###
## linkP - 自プログラム向けリンクの生成
#
# - SYNOPSIS
#	&linkP( $href, $markUp );
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
sub linkP
{
    local( $comm, $markUp, $key, $title, $name, $fragment ) = @_;
    $comm .= "&kinoA=3&kinoU=$UNAME_ESC&kinoP=$PASSWD" if ( $SYS_AUTH == 3 );
    $comm =~ s/&/&amp;/go;
    $comm .= "#$fragment" if ( $fragment ne '' );
    &tagA( $markUp, "$PROGRAM?$comm", $key, $title, $name );
}


#### びう関連ロジック


###
## makeNewArticle, MakeNewArticleEx - 新たに投稿された記事の生成
#
# - SYNOPSIS
#	&MakeNewArticleEx( $Board, $Id, $artKey, $postDate, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail, $MailRelay );
#	&makeNewArticle( $Board, $Id, $artKey, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail, $MailRelay );
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
#	今後（R7以後）は極力&makeNewArticleExの方を使うように．
#
sub MakeNewArticle
{
    local( $Board, $Id, $artKey, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail, $MailRelay ) = @_;
    &makeNewArticleEx( $Board, $Id, $artKey, $^T, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail, $MailRelay );
}

sub makeNewArticleEx
{
    local( $Board, $Id, $artKey, $postDate, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail, $MailRelay ) = @_;

    &checkArticle( $Board, *postDate, *Name, *Email, *Url, *Subject, *Icon, *Article );

    # DBファイルに投稿された記事を追加
    local( $ArticleId ) = &insertArt( $Board, $Id, $artKey, $postDate, $Subject, $Icon, ( $SYS_LOGHOST? $REMOTE_INFO : '' ), $Name, $Email, $Url, $Fmail, $MailRelay, $TextType, $Article );

    $ArticleId;
}


###
## searchArticleIcon - 記事の検索(アイコン)
#
# - SYNOPSIS
#	&searchArticleIcon( $id, $type, const *iconHash );
#
# - ARGS
#	$id		アイコンを検索する記事のID
#	$type		検索タイプ
#			  1 ... である
#			  2 ... 直接の娘である
#			  3 ... 直接の親である
#			  11 ... スレッド中に含む
#			  12 ... スレッドの先頭にある
#			  13 ... スレッドの末端にある
#	%iconHash	検索アイコン用ハッシュ．
#			  $iconHash{ 'アイコン' }が真のアイコンが検索される．
#
# - DESCRIPTION
#	指定された記事のアイコンを検索する．
#
# - RETURN
#	1 if match, 0 if not.
#
%gSearchIconResult = ();
sub searchArticleIcon
{
    local( $id, $type, *iconHash ) = @_;
    local( $result ) = 0;

    # 検索結果がキャッシュしてあるかどうかをチェック．あればそちらを優先．
    if ( defined( $gSearchIconResult{ $id } ))
    {
	return $gSearchIconResult{ $id };
    }

    # 0は後方互換性のため．'on'が渡されるかもしれない．
    if (( $type == 1 ) || ( $type == 0 ))
    {
	$result = 1 if ( $iconHash{ &getArtIcon( $id ) } );
	$gSearchIconResult{ $id } = $result;
    }
    elsif ( $type == 2 )
    {
	local( @daughters ) = split( /,/, &getArtDaughters( $id ));
	if ( !@daughters )
	{
	    $result = 0;
	}
	else
	{
	    foreach ( @daughters )
	    {
		$result = 1, last if ( $iconHash{ &getArtIcon( $_ ) } );
	    }
	}
	$gSearchIconResult{ $id } = $result;
    }
    elsif ( $type == 3 )
    {
	local( $parent ) = &getArtParent( $id );
	if ( $parent eq '' )
	{
	    $result = $gSearchIconResult{ $id } = 0;
	}
	elsif ( $iconHash{ &getArtIcon( $parent ) } )
	{
	    local( @daughters ) = split( /,/, &getArtDaughters( $parent ));
	    foreach ( @daughters )
	    {
		$result = $gSearchIconResult{ $_ } = 1;
	    }
	}
	else
	{
	    local( @daughters ) = split( /,/, &getArtDaughters( $parent ));
	    foreach ( @daughters )
	    {
		$result = $gSearchIconResult{ $_ } = 0;
	    }
	}
    }
    elsif ( $type == 11 )
    {
	local( $topId ) = &getArtParentTop( $id );

	# トップから検索していく．
	local( @daughters ) = ( $topId );
	local( $dId );
	while ( $dId = shift( @daughters ))
	{
	    $result = 1, last if ( $iconHash{ &getArtIcon( $dId ) } );
	    push( @daughters, split( /,/, &getArtDaughters( $dId )));
	}
    }
    elsif ( $type == 12 )
    {
	local( $topId ) = &getArtParentTop( $id );
	$result = 1 if ( $iconHash{ &getArtIcon( $topId ) } );
    }
    elsif ( $type == 13 )
    {
	local( @daughters ) = ( $id );
	local( $dId, $dDaughters );
	while ( $dId = shift( @daughters ))
	{
	    $dDaughters = &getArtDaughters( $dId );
	    if ( $dDaughters eq '' )
	    {
		$result = 1, last if ( $iconHash{ &getArtIcon( $dId ) } );
	    }
	    else
	    {
		push( @daughters, split( /,/, $dDaughters ));
	    }
	}
    }

    # スレッド検索の場合
    if ( int( $type / 10 ) == 1 )
    {
	# 検索結果をキャッシュに反映させる: トップからたどれる全ての娘へ
	local( $topId ) = &getArtParentTop( $id );

	# トップから検索していく．
	local( @daughters ) = ( $topId );
	local( $dId );
	while ( $dId = shift( @daughters ))
	{
	    $gSearchIconResult{ $dId } = $result;
	    push( @daughters, split( /,/, &getArtDaughters( $dId )));
	}
    }

    return $result;
}


###
## searchArticleKeyword - 記事の検索(本文)
#
# - SYNOPSIS
#	&searchArticleKeyword($Id, $Board, @KeyList);
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
sub searchArticleKeyword
{
    local( $Id, $Board, @KeyList ) = @_;

    local( @NewKeyList, $Line, $Return, $Code, $ConvFlag, @ArticleBody );

    $ConvFlag = ( $Id !~ /^\d+$/ );

    &getArtBody( $Id, $Board, *ArticleBody );
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
## checkSearchTime - 検索日付のチェック
#
# - SYNOPSIS
#	&checkSearchTime( $target, $from, $to );
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
sub checkSearchTime
{
    local( $target, $from, $to ) = @_;

    if ( $from >= 0 )
    {
	return 0 if ( $target < $from );
    }
    elsif ( $to >= 0 )
    {
	return 0 if ( $target > $to );
    }
    else
    {
	return 0;
    }

    1;
}


###
## deleteArticle - 記事の削除
#
# - SYNOPSIS
#	&deleteArticle($Id, $ThreadFlag);
#
# - ARGS
#	$Id		削除記事ID
#	$Board		掲示板ID
#	$ThreadFlag	リプライも消すか否か
#
# - DESCRIPTION
#	削除すべき記事IDを収集した後，DBを更新する．
#
sub deleteArticle
{
    local( $Id, $Board, $ThreadFlag ) = @_;

    local( $Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $dId, @Target, $TargetId, $parents );

    # 記事情報の取得
    ( $Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url ) = &getArtInfo( $Id );

    # データの書き換え(必要なら娘も)
    @Target = ( $Id );
    foreach $TargetId ( @Target )
    {
	foreach ( 0 .. &getNofArt() )
	{
	    # IDを取り出す
	    $dId = &getArtId( $_ );
	    # フォロー記事リストの中から，削除する記事のIDを取り除く
	    &setArtDaughters( $dId, join( ',', grep(( !/^$TargetId$/o ),
		split( /,/, &getArtDaughters( $dId )))));
	    # 元記事から削除記事のIDを取り除く
	    $parents = &getArtParents( $dId );
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
	    &setArtParents( $dId, $parents );
	    # 娘も対象とする
	    push( @Target, split( /,/, &getArtDaughters( $dId ))) if ( $ThreadFlag && ( $dId eq $TargetId ));
	}
    }

    # DBを更新する．
    &deleteArt( $Board, *Target );
}


###
## supersedeArticle - 記事を訂正する
#
# - SYNOPSIS
#	&supersedeArticle;
#
# - DESCRIPTION
#	記事を訂正する．
#
sub supersedeArticle
{
    local( $Board, $Id, $postDate, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail ) = @_;

    # 入力された記事情報のチェック．投稿日は
    &checkArticle( $Board, $postDate, *Name, *Email, *Url, *Subject, *Icon, *Article );

    # DBファイルを訂正
    &updateArt( $Board, $Id, $postDate, $Subject, $Icon, ( $SYS_LOGHOST? $REMOTE_INFO : '' ), $Name, $Email, $Url, $Fmail, $TextType, $Article );

    $Id;
}


###
## reLinkExec - 記事のかけかえ実施
#
# - SYNOPSIS
#	&reLinkExec($FromId, $ToId, $Board);
#
# - ARGS
#	$FromId		かけかえ元記事ID
#	$ToId		かけかえ先記事ID
#	$Board		掲示板ID
#
# - DESCRIPTION
#	記事をリプライ-元記事関係をかけかえる．
#
sub reLinkExec
{
    local( $FromId, $ToId, $Board ) = @_;

    local( $dId, @Daughters, $DaughterId );

    # 循環記事の禁止
    &fatal( 50, '' ) if ( grep( /^$FromId$/, split( /,/, &getArtParents( $ToId ))));

    # データ書き換え
    foreach ( 0 .. &getNofArt() )
    {
	# IDを取り出す
	$dId = &getArtId( $_ );
	# フォロー記事リストの中から，移動する記事のIDを取り除く
	&setArtDaughters( $dId, join( ',', grep(( !/^$FromId$/o ), split( /,/, &getArtDaughters( $dId )))));
    }

    # 後で娘たちの書き換えも必要になる．
    @Daughters = split( /,/, &getArtDaughters( $FromId ));

    # 該当記事のリプライ先を変更する
    if ( $ToId eq '' )
    {
	&setArtParents( $FromId, '' );
    }
    elsif ( &getArtParents( $ToId ) eq '' )
    {
	&setArtParents( $FromId, "$ToId" );
    }
    else
    {
	&setArtParents( $FromId, "$ToId," . &getArtParents( $ToId ));
    }

    # 上で変更した「該当記事のリプライ先」を，娘に反映させる
    while ( $DaughterId = shift( @Daughters ))
    {
	# 孫娘も……
	push( @Daughters, split( /,/, &getArtDaughters( $DaughterId )));

	# 書き換え
	if (( &getArtParents( $DaughterId ) eq $FromId ) || ( &getArtParents( $DaughterId ) =~ /^$FromId,/ ))
	{
	    &setArtParents( $DaughterId, ( &getArtParents( $FromId ) ne '' )? "$FromId," . &getArtParents( $FromId ) : "$FromId" );
	}
	elsif (( &getArtParents( $DaughterId ) =~ /^(.*),$FromId$/ ) || ( &getArtParents( $DaughterId ) =~ /^(.*),$FromId,/ ))
	{
	    &setArtParents( $DaughterId, ( &getArtParents( $FromId ) ne '' )? "$1,$FromId," . &getArtParents( $FromId ) : "$1,$FromId" );
	}
    }

    # リプライ先になった記事のフォロー記事群に追加する
    &setArtDaughters( $ToId, ( &getArtDaughters( $ToId ) ne '' ) ? &getArtDaughters( $ToId ) . ",$FromId" : "$FromId" );

    # 記事DBを更新する
    &flushArt( $Board );
}


###
## reOrderExec - 記事の移動実施
#
# - SYNOPSIS
#	&reOrderExec($FromId, $ToId, $Board);
#
# - ARGS
#	$FromId		移動元記事ID
#	$ToId		移動先記事ID
#	$Board		掲示板ID
#
# - DESCRIPTION
#	指定された記事を，指定された記事の次に移動する．
#
sub reOrderExec
{
    local( $FromId, $ToId, $Board ) = @_;

    local( @Move );

    # 移動する記事たちを集める
    @Move = ( $FromId, &getFollowIdSet( $FromId ));

    # 移動させる
    &reOrderArt( $Board, $ToId, *Move );
}


#### メイル関連ロジック


###
## arriveMail - 記事が到着したことをメイル
#
# - SYNOPSIS
#	&arriveMail( $Name, $Email, $Date, $Subject, $Icon, $Id, @To );
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
sub arriveMail
{
    local( $Name, $Email, $Date, $Subject, $Icon, $Id, @To ) = @_;

    local( $StrSubject, $MailSubject, $StrFrom, $Message );
    $StrSubject = ( !$SYS_ICON || ( $Icon eq $H_NOICON ))? $Subject : "($Icon) $Subject";
    $StrSubject =~ s/<[^>]*>//go;	# タグは要らない
    $StrSubject = &htmlDecode( $StrSubject );
    $MailSubject = &getMailSubjectPrefix( $BOARDNAME, $Id ) . $StrSubject;
    $StrFrom = $Email? "$Name <$Email>" : "$Name";

    $Message = <<__EOF__;
$SYSTEM_NAMEからのお知らせです．
$H_BOARD「$BOARDNAME」に対して書き込みがありました．

新着$H_MESG:
  → $SCRIPT_URL?b=$BOARD&c=e&id=$Id

__EOF__

    $Message .= &getArticlePlainText( $Id, $Name, $Email, $Subject, $Icon, $Date );

    # メイル送信
    &sendArticleMail( $Name, $Email, $MailSubject, $Message, $Id, @To );
}


###
## followMail - 反応があったことをメイル
#
# - SYNOPSIS
#	&followMail( $Name, $Email, $Date, $Subject, $Icon, $Id, $Fname, $Femail, $Fsubject, $Ficon, $Fid, @To );
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
sub followMail
{
    local( $Name, $Email, $Date, $Subject, $Icon, $Id, $Fname, $Femail, $Fdate, $Fsubject, $Ficon, $Fid, @To ) = @_;
    
    local( $StrSubject, $FstrSubject, $MailSubject, $StrFrom, $Message );

    $StrSubject = ( !$SYS_ICON || ( $Icon eq $H_NOICON ))? "$Subject" : "($Icon) $Subject";
    $StrSubject =~ s/<[^>]*>//go;	# タグは要らない
    $StrSubject = &htmlDecode( $StrSubject );
    $FstrSubject = ( $Ficon eq $H_NOICON )? $Fsubject : "($Ficon) $Fsubject";
    $FstrSubject =~ s/<[^>]*>//go;	# タグは要らない
    $FstrSubject = &htmlDecode( $FstrSubject );
    $MailSubject = &getMailSubjectPrefix( $BOARDNAME, $Fid ) . $FstrSubject;
    $StrFrom = $Email? "$Name <$Email>" : "$Name";

    local( $topId ) = &getArtParentTop( $Id );

    $Message = <<__EOF__;
$SYSTEM_NAMEからのお知らせです．

$H_BOARD「$BOARDNAME」に
「$StrFrom」さんが書いた
「$StrSubject」に
$H_REPLYがありました．

新着$H_MESG:
  → $SCRIPT_URL?b=$BOARD&c=e&id=$Fid
スレッドの先頭からまとめ読み:
  → $SCRIPT_URL?b=$BOARD&c=t&id=$topId

__EOF__

    $Message .= &getArticlePlainText( $Fid, $Fname, $Femail, $Fsubject, $Ficon, $Fdate );

    # メイル送信
    &sendArticleMail( $Fname, $Femail, $MailSubject, $Message, $Fid, @To );
}


###
## sendArticleMail - メイル送信
#
# - SYNOPSIS
#	&sendArticleMail( $FromName, $FromAddr, $Subject, $Message, $Id, @To );
#
# - ARGS
#	$FromName	メイル送信者名
#	$FromAddr	メイル送信者メイルアドレス
#	$Subject	メイルのSubject文字列
#	$Message	本文
#	$Id		引用するなら記事ID; 空なら引用ナシ
#	@To		宛先E-Mail addr.のリスト
#
# - DESCRIPTION
#	メイルを送信する．
#
sub sendArticleMail
{
    local( $FromName, $FromAddr, $Subject, $Message, $Id, @To ) = @_;

    local( $ExtHeader, @ArticleBody );

    $ExtHeader = "X-MLServer: $PROGNAME\n";
    $ExtHeader .= "X-Kb-System: $SYSTEM_NAME\n";
    if (( ! $SYS_MAILHEADBRACKET ) && $BOARDNAME && ($Id ne '' ))
    {
	$ExtHeader .= "X-Kb-Board: $BOARDNAME\nX-Kb-Articleid: $Id\n";
    }

    local( $stat, $errstr ) = &sendMail( $FromName, $FromAddr, $Subject, $ExtHeader, $Message, @To );
    &fatal( 9, "$BOARDNAME/$Id/$errstr" ) unless $stat;
}


###
## sendMail - メイル送信
#
# - SYNOPSIS
#	&sendMail( $FromName, $FromAddr, $Subject, $ExtHeader, $Message, @To );
#
# - ARGS
#	$FromName	メイル送信者名
#	$FromAddr	メイル送信者メイルアドレス
#	$Subject	メイルのSubject文字列
#	$ExtHeader	追加ヘッダ
#	$Message	本文
#	@To		宛先E-Mail addr.のリスト
#
# - DESCRIPTION
#	メイルを送信する．
#
# - RETURN
#	( $status, $errstr )
#		$status		0 if succeeded, errCode if failed.
#		$errstr		errstr if failed.
#
sub sendMail
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
## getArticlePlainText - メッセージをplain textで取得
#
# - SYNOPSIS
#	&getArticlePlainText( $id, $name, $mail, $subject, $icon, $date );
#
# - ARGS
#	$id		メッセージID
#	$name		投稿者名
#	$mail		投稿者メイルアドレス
#	$subject	タイトル
#	$icon		アイコン
#	$date		日付(UTC)
#
# - DESCRIPTION
#	メイル送信用に，メッセージをplain textで取得する．
#
# - RETURN
#	文字列
#
sub getArticlePlainText
{
    local( $id, $name, $mail, $subject, $icon, $date ) = @_;

    local( $strSubject ) = ( !$SYS_ICON || ( $icon eq $H_NOICON ))? $subject :
	"($icon) $subject";
    $strSubject =~ s/<[^>]*>//go;	# タグは要らない
    $strSubject = &htmlDecode( $strSubject );
    local( $strFrom ) = $mail? "$name <$mail>" : $name;
    local( $strDate ) = &getDateTimeFormatFromUtc( $date );

    local( @body );
    &getArtBody( $id, $BOARD, *body );

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
	$str .= &htmlDecode( $_ );
    }

    # 先頭と末尾の改行を切り飛ばす．
    $str =~ s/^\n*//o;
    $str =~ s/\n*$//o;

    $msg . $str;
}


#### 共通ロジック


###
## checkArticle - 入力された記事情報のチェック
#
# - SYNOPSIS
#	&checkArticle( $board, *postDate, *name, *eMail, *url, *subject, *icon, *article );
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
sub checkArticle
{
    local( $board, *postDate, *name, *eMail, *url, *subject, *icon, *article ) = @_;

    &checkPostDate( *postDate );
    &checkName( *name );
    &checkEmail( *eMail );
    &checkURL( *url );
    &checkSubject( *subject );
    &checkIcon( *icon ) if $SYS_ICON;

    # 本文の空チェック．
    &fatal( 2, $H_MESG ) if ( $article eq '' );

    if ( $SYS_MAXARTSIZE != 0 )
    {
	local( $length ) = length( $article );
	&fatal( 12, $length ) if ( $length > $SYS_MAXARTSIZE );
    }
}


###
## secureSubject - 安全なSubjectを作り出す
## secureArticle - 安全なArticleを作り出す
#
# - SYNOPSIS
#	&secureSubject( *subject );
#	&secureArticle( *article, $textType );
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
	&cgi'secureXHTML( *subject, *sNeedVec, *sFeatureVec );
    }
    else
    {
	$subject = &htmlEncode( $subject );	# no tags are allowed.
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
	&plainArticleToPreFormatted( *article );
    }
    elsif ( $textType eq $H_TTLABEL[1] )
    {
	# convert to html
	&plainArticleToHtml( *article );
	# secrurity check
	&cgi'secureXHTML( *article, *aNeedVec, *aFeatureVec );
    }
    elsif ( $textType eq $H_TTLABEL[2] )
    {
	# secrurity check
	&cgi'secureXHTML( *article, *aNeedVec, *aFeatureVec );
    }
    else
    {
	# Not selected... pre-formatted
	&plainArticleToPreFormatted( *article );
    }
}


###
## checkPostDate - 投稿日チェック
#
# - SYNOPSIS
#	&checkPostDate( *str );
#
# - ARGS
#	*str		投稿日（UTCからの経過秒数）
#
# - DESCRIPTION
#	投稿日のチェックを行なう．
#
sub checkPostDate
{
    local( *str ) = @_;

    # 空でもOK
    return if ( $str eq '' );

    # 不正な値になってないか?（解析に失敗してたら-1になってるはず）
    &fatal( 21, '' ) if ( $str < 0 );
}


###
## checkSubject - 文字列チェック: Subject
#
# - SYNOPSIS
#	&checkSubject(*String);
#
# - ARGS
#	*String		Subject文字列
#
# - DESCRIPTION
#	Subjectの文字列チェックを行なう．
#	不正な文字列だったらエラー表示ルーチンへ．
#	(アプリケーション/UIを分離したほうがいいかな?)
#
sub checkSubject
{
    local( *String ) = @_;

    &fatal( 2, $H_SUBJECT ) unless $String;
    &fatal( 3, '' ) if ( $String =~ m/[\t\n]/o );

    if ( !$SYS_TAGINSUBJECT )
    {
	&fatal( 4, '' ) if ( $String =~ m/[<>]/o );
    }
}


###
## checkIcon - 文字列チェック: Icon
#
# - SYNOPSIS
#	&checkIcon( *str );
#
# - ARGS
#	*str		Icon文字列
#
# - DESCRIPTION
#	Iconの文字列チェックを行なう．
#	不正な文字列だったらエラー表示ルーチンへ．
#
sub checkIcon
{
    local( *str ) = @_;

    # アイコンのチェック; おかしけりゃ「無し」に設定．
    $str = $H_NOICON if ( !&getIconUrlFromTitle( $str ));

    &fatal( 2, $H_ICON ) if ( !$SYS_ALLOWNOICON && ( $str eq $H_NOICON ));
}


###
## checkName - 文字列チェック: 投稿者名
#
# - SYNOPSIS
#	&checkName(*String);
#
# - ARGS
#	*String		投稿者名文字列
#
# - DESCRIPTION
#	投稿者名の文字列チェックを行なう．
#	不正な文字列だったらエラー表示ルーチンへ．
#	(アプリケーション/UIを分離したほうがいいかな?)
#
sub checkName
{
    local( *String ) = @_;

    &fatal( 2, $H_FROM ) if ( !$String );
    &fatal( 3, '' ) if ( $String =~ m/[\t\n]/o );

    # 数字だけじゃ駄目．
    &fatal( 5, $String ) if ( $String =~ /^\d+$/ );
}


###
## checkPasswd - 文字列チェック: パスワード
#
# - SYNOPSIS
#	&checkPasswd(*String);
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
sub checkPasswd {
    local( *String ) = @_;

    &fatal( 2, $H_PASSWD ) if ( !$String );
    &fatal( 3, $H_PASSWD ) if ( $String =~ /[\t\n]/o );

    return 0;
}


###
## checkEmail - 文字列チェック: E-Mail addr.
#
# - SYNOPSIS
#	&checkEmail(*String);
#
# - ARGS
#	*String		E-Mail addr.文字列
#
# - DESCRIPTION
#	E-Mail addr.の文字列チェックを行なう．
#	不正な文字列だったらエラー表示ルーチンへ．
#	(アプリケーション/UIを分離したほうがいいかな?)
#
sub checkEmail
{
    local( *String ) = @_;

    if ( $SYS_POSTERMAIL )
    {
	&fatal( 2, $H_MAIL ) if ( !$String );
	# `@'が入ってなきゃアウト
	&fatal( 7, 'E-Mail' ) if ( $String !~ /@/ );
    }
    &fatal( 3, '' ) if ( $String =~ m/[\t\n]/o );
}


###
## checkURL - 文字列チェック: URL
#
# - SYNOPSIS
#	&checkURL(*String);
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
sub checkURL
{
    local( *String ) = @_;

    # http://だけの場合は空にしてしまう．
    $String = '' if ( $String =~ m!^http://$!oi );
    &fatal( 7, 'URL' ) if (( $String ne '' ) && ( !&isUrl( $String )));
    &fatal( 3, '' ) if ( $String =~ m/[\t\n]/o );
}


###
## checkBoardDir - 文字列チェック: 掲示板ディレクトリ
#
# - SYNOPSIS
#	&checkBoardDir( *name );
#
# - ARGS
#	*name		掲示板ディレクトリ名
#
sub checkBoardDir
{
    local( *name ) = @_;
    &fatal( 52, '' ) unless (( $name =~ /\w+/o ) || ( $name =~ /\//o ));
    &fatal( 2, "$H_BOARD略称" ) if ( $name eq '' );
}

###
## checkBoardName - 文字列チェック: 掲示板名
#
# - SYNOPSIS
#	&checkBoardDir( *intro );
#
# - ARGS
#	*intro		掲示板名
#
sub checkBoardName
{
    local( *intro ) = @_;
    &fatal( 2, "$H_BOARD名称" ) if ( $intro eq '' );
}

###
## checkBoardHeader - 文字列チェック: 掲示板ヘッダ
#
# - SYNOPSIS
#	&checkBoardHeader( *header );
#
# - ARGS
#	*header		掲示板ヘッダ
#
sub checkBoardHeader
{
    local( *header ) = @_;
    # 空でもOK
}


###
## isUser - ユーザのチェック
#        
# - SYNOPSIS
#       &isUser( $name );
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
sub isUser
{
    local( $name ) = @_;
    ( $SYS_AUTH && (( $UNAME eq $name ) || (( $UNAME eq $ADMIN ) && ( $name eq $MAINT_NAME ))));
}


###
## isUrl - URLの構造をチェック
#
# - SYNOPSIS
#	&isUrl($String);
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
sub isUrl
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
## getFollowIdTree - リプライ記事の木構造を取得
#
# - SYNOPSIS
#	&getFollowIdTree($id, *tree);
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
sub getFollowIdTree
{
    local( $id, *tree ) = @_;

    # 安全のため，再帰停止条件（データが正常ならここは通らない）
    return if ( $id eq '' );

    local( @aidList ) = split( /,/, &getArtDaughters( $id ));

    push( @tree, '(', $id );
    foreach ( @aidList ) { &getFollowIdTree( $_, *tree ); }
    push( @tree, ')' );
}


###
## getFollowIdSet - 娘ノードのリストを集める
#
# - SYNOPSIS
#	&getFollowIdSet($Id);
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
sub getFollowIdSet
{
    local( $Id ) = @_;
    local( @Return );
    foreach ( split(/,/, &getArtDaughters( $Id )))
    {
	push( @Return, $_ );
	push( @Return, &getFollowIdSet( $_ )) if ( &getArtDaughters( $_ ) ne '' );
    }
    @Return;
}


###
## getTreeTopArticle - 木構造のトップ記事を取得
#
# - SYNOPSIS
#	&getTreeTopArticle( *tree );
#
# - ARGS
#	*tree	木構造が格納済みのリスト
#
# - DESCRIPTION
#	木構造の詳細については&getFollowIdTree()を参照のこと．
#
# - RETURN
#	記事ID
#
sub getTreeTopArticle
{
    local( *tree ) = @_;
    $tree[1];
}


###
## getReplySubject - リプライSubjectの生成
#
# - SYNOPSIS
#	&getReplySubject( *subjectStr );
#
# - ARGS
#	$subjectStr	Subject文字列
#
# - DESCRIPTION
#	先頭に「Re:」を1つだけつける．
#
sub getReplySubject
{
    local( *subjectStr ) = @_;

    # Re:を取り除き，
    $subjectStr =~ s/^Re:\s*//oi;

    # TAG用エンコードして，
    &tagEncode( *subjectStr );

    # 先頭に「Re: 」をくっつけて返す．
    $subjectStr = "Re: $subjectStr";
}


###
## getMailSubjectPrefix - メイル用Subjectのprefixを取得
#
# - SYNOPSIS
#	&getMailSubjectPrefix( $board, $id );
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
sub getMailSubjectPrefix
{
    local( $board, $id ) = @_;
    return "[$board: $id] " if $SYS_MAILHEADBRACKET;
    "";
}


###
## getDateTimeFormatFromUtc - UTCから時間を表す文字列を取得
#
# - SYNOPSIS
#	&getDateTimeFormatFromUtc($Utc);
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
sub getDateTimeFormatFromUtc
{
    local( $utc ) = @_;
    local( $sec, $min, $hour, $mDay, $mon, $year ) = localtime( $utc );
    sprintf( "%d/%d/%d(%02d:%02d)", $year+1900, $mon+1, $mDay, $hour, $min );
}


###
## getYYYY_MM_DD_HH_MM_SSFromUtc - UTCからYYYY/MM/DD(HH:MM:SS)を取得
#
# - SYNOPSIS
#	&getYYYY_MM_DD_HH_MM_SSFromUtc( $utc );
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
sub getYYYY_MM_DD_HH_MM_SSFromUtc
{
    local( $utc ) = @_;
    local( $sec, $min, $hour, $mDay, $mon, $year ) = localtime( $utc );
    sprintf( "%d/%d/%d(%02d:%02d:%02d)", $year+1900, $mon+1, $mDay, $hour, $min, $sec );
}


###
## getUtcFromYYYY_MM_DD_HH_MM_SS - YYYY/MM/DD(HH:MM:SS)からUTCを取得
#
# - SYNOPSIS
#	&getUtcFromYYYY_MM_DD_HH_MM_SS
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
sub getUtcFromYYYY_MM_DD_HH_MM_SS
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
## getUtcFromYYYY_MM_DD - YYYY/MM/DDからUTCを取得
#
# - SYNOPSIS
#	&getUtcFromYYYY_MM_DD
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
sub getUtcFromYYYY_MM_DD
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
## getPath - DBファイルのパス名の取得
#
# - SYNOPSIS
#	&getPath($DbDir, $File);
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
sub getPath
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
## getStyleSheetURL - スタイルシートファイルのURLの取得
#
# - SYNOPSIS
#	&getStyleSheetURL( $name );
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
sub getStyleSheetURL
{
    local( $name ) = @_;
    $KB_RESOURCE_URL? "$KB_RESOURCE_URL$RESOURCE_STYLE/$name" : "$RESOURCE_STYLE/$name";
}


###
## getIconURL - アイコンファイルのURLの取得
#
# - SYNOPSIS
#	&getIconURL( $file );
#
# - ARGS
#	$file		アイコンファイル名
#
# - DESCRIPTION
#	アイコンファイルのURL名を作り出す．
#
# - RETURN
#	URLを表す文字列
#
sub getIconURL
{
    local( $file ) = @_;
    $KB_RESOURCE_URL? "$KB_RESOURCE_URL$RESOURCE_ICON/$file" : "$RESOURCE_ICON/$file";
}


###
## getImgURL - イメージ用URLの取得
#
# - SYNOPSIS
#	&getImgURL( $file );
#
# - ARGS
#	$file		イメージファイル名
#
# - DESCRIPTION
#	イメージファイルのURL名を作り出す．
#
# - RETURN
#	URLを表す文字列
#
sub getImgURL
{
    local( $file ) = @_;
    $KB_RESOURCE_URL? "$KB_RESOURCE_URL$RESOURCE_IMG/$file" : "$RESOURCE_IMG/$file";
}


###
## getIconUrlFromTitle - アイコンファイルURLの取得
#
# - SYNOPSIS
#	&getIconUrlFromTitle( $icon );
#
# - ARGS
#	$icon		アイコンID
#
# - DESCRIPTION
#	アイコンIDから，そのIDに対応するアイコンファイルのURLを取得．
#	新着アイコンも記事アイコン扱い．
#
# - RETURN
#	URLを表す文字列
#
sub getIconUrlFromTitle
{
    local( $icon ) = @_;
    return $ICON_NEW if ( $icon eq $H_NEWARTICLE );

    local( $file ) = &getBoardIconFile( $icon );

    # check
    return '' unless $file;

    # return
    &getIconURL( $file );
}


###
## getTitleOldIndex - 'old'値の取得
#
# - SYNOPSIS
#	&getTitleOldIndex( $id );
#
# - ARGS
#	$id	記事番号
#
# - DESCRIPTION
#	指定したIDの記事を含むようなold値を計算する．
#	&cacheArtが呼び出し済みでなければならない．
#
# - RETURN
#	old値
#
sub getTitleOldIndex
{
    local( $id ) = @_;
    local( $old ) = &getNofArt() - int( $id + $DEF_TITLE_NUM/2 );
    ( $old >= 0 )? $old : 0;
}


######################################################################
# データインプリメンテーション


#### 掲示板関連


###
## getNofBoard - 掲示板数の取得
## getBoardId - 掲示板IDの取得
## getBoardNum - 掲示板番号の取得
#
# - SYNOPSIS
#	&getNofBoard();
#	&getBoardId( $num );
#	&getBoardNum( $id );
#
# - ARGS
#	$num	掲示板番号
#	$id	掲示板ID
#
# - DESCRIPTION
#	掲示板数を取得する．
#	掲示板番号/掲示板IDから，ID/番号を取得する．
#
# - RETURN
#	掲示板数
#	掲示板ID/掲示板番号
#
sub getNofBoard
{
    $#BOARD_ID;
}
sub getBoardId
{
    return '' if ( $_[0] < 0 );
    $BOARD_ID[ $_[0] ];
}
sub getBoardNum
{
    local( $id ) = $_[0];
    foreach ( 0 .. &getNofBoard() )
    {
	return $_ if ( &getBoardId( $_ ) eq $id );
    }
    return -1;
}


###
## getBoardName - 掲示板名の取得
## getBoardInfo - 掲示板情報の取得
## getBoardKey - 掲示板ガードキーの取得
#
# - SYNOPSIS
#	&getBoardName( $id );
#	&getBoardInfo( $id );
#	&getBoardKey( $id );
#
# - ARGS
#	$id	掲示板ID
#
# - DESCRIPTION
#	掲示板情報を取得する．
#
# - RETURN
#	get*
#
sub getBoardName { $BOARD_NAME{ $_[0] }; }
sub getBoardInfo { $BOARD_INFO{ $_[0] }; }
sub getBoardKey
{
    local( $board ) = @_;

    local( $id, $artKey );
    local( $file ) = &getPath( $board, $ARTICLE_NUM_FILE_NAME );
    open( AID, "<$file" ) || &fatal( 1, $file );
    chop( $id = <AID> );
    chop( $artKey = <AID> );
    close AID;
    $artKey;
}


###
## getNofBoardIcon - アイコン数の取得
## getBoardIconId - アイコンIDの取得
## getBoardIconNum - アイコン番号の取得
#
# - SYNOPSIS
#	&getNofBoardIcon();
#	&getBoardIconId( $num );
#	&getBoardIconNum( $id );
#
# - ARGS
#	$num	アイコン番号
#	$id	アイコンID
#
# - DESCRIPTION
#	アイコン数を取得する．
#	アイコン番号/アイコンIDから，ID/番号を取得する．
#
# - RETURN
#	アイコン数
#	アイコンID/アイコン番号
#
sub getNofBoardIcon
{
    $#ICON_ID;
}
sub getBoardIconId
{
    return '' if ( $_[0] < 0 );
    $ICON_ID[ $_[0] ];
}
sub getBoardIconNum
{
    local( $id ) = $_[0];
    foreach ( 0 .. &getNofBoardIcon() )
    {
	return $_ if ( &getBoardIconId( $_ ) eq $id );
    }
    return -1;
}


###
## getBoardIconFile - アイコンファイル名の取得
## getBoardIconHelp - アイコンヘルプの取得
## getBoardIconType - アイコンタイプの取得
#
# - SYNOPSIS
#	&getBoardIconFile( $id );
#	&getBoardIconHelp( $id );
#	&getBoardIconType( $id );
#
# - ARGS
#	$id	アイコンID
#
# - DESCRIPTION
#	アイコン情報を取得する．
#
sub getBoardIconFile { $ICON_FILE{ $_[0] }; }
sub getBoardIconHelp { $ICON_HELP{ $_[0] }; }
sub getBoardIconType { $ICON_TYPE{ $_[0] }; }


###
## getBoardLastmod - ある掲示板の最終更新時刻を取得
#
# - SYNOPSIS
#	&getBoardLastmod( $board );
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
    $^T - ( -M &getPath( $board, $DB_FILE_NAME )) * 86400;
}


###
## getBoardHeader - 掲示板別ヘッダDBの全読み込み
#
# - SYNOPSIS
#	&getBoardHeader( $board, *header );
#
# - ARGS
#	$board		掲示板ID
#	*header		ヘッダ文字列
#
sub getBoardHeader
{
    local( $board, *header ) = @_;

    local( $file ) = &getPath( $board, $HEADER_FILE_NAME );
    # ファイルがなきゃ空のまま
    open( DB, "<$file" ) || return;
    while ( <DB> )
    {
	$header .= $_;
    }
    close DB;
}


###
## getBoardSubscriber - 掲示板講読者の取得
#
# - SYNOPSIS
#	&getBoardSubscriber( $CommentFlag, $Board, *ArriveMail );
#
# - ARGS
#	$CommentFlag	コメント行を含むか否か(0: 含まない, 1: 含む)
#	$Board		掲示板ID
#	*ArriveMail	送信先のメイルアドレスのリストのリファレンス
#
# - DESCRIPTION
#	掲示板講読者を取得する．
#	メイルアドレスが正しいか否か等のチェックは，一切行なわない．
#
sub getBoardSubscriber
{
    local($CommentFlag, $Board, *ArriveMail) = @_;
    local($ArriveMailFile);

    $ArriveMailFile = &getPath( $Board, $ARRIVEMAIL_FILE_NAME );
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
## cacheBoard - 掲示板DBの読み込み
#
# - SYNOPSIS
#	&cacheBoard();
#
# - DESCRIPTION
#	掲示板DBから，掲示板情報を取ってくる．
#
sub cacheBoard
{
    local( $i ) = 0;
    local( $bId, $bName, $bInfo );
    local( $dbFile ) = &getPath( $SYS_DIR, $BOARD_FILE );
    open( DB, "<$dbFile" ) || &fatal( 1, $dbFile );
    while ( <DB> )
    {
	next if ( /^\#/o || /^$/o );
	chop;
	( $bId, $bName, $bInfo ) = split( /\t/, $_, 3 );
	$BOARD_ID[$i++] = $bId;
	$BOARD_NAME{$bId} = $bName;
	$BOARD_INFO{$bId} = $bInfo;
    }
    close DB;
}


###
## cacheBoardIcon - アイコンDBの全読み込み
#
# - SYNOPSIS
#	&cacheBoardIcon($board);
#
# - ARGS
#	$board		掲示板ID
#
# - DESCRIPTION
#	アイコンDBを読み込んで連想配列に放り込む．
#	大域変数，@ICON_ID，%ICON_FILE，%ICON_HELPを破壊する．
#
sub cacheBoardIcon
{
    local( $board ) = @_;
    local( $fileName, $title, $help, $type );

    @ICON_ID = %ICON_FILE = %ICON_HELP = %ICON_TYPE = ();

    local( $i ) = 0;
    open( ICON, &getIconPath( "$board.$ICONDEF_POSTFIX" ))
	|| ( open( ICON, &getIconPath( "$DEFAULT_ICONDEF" ))
	    || &fatal( 1, &getIconPath( "$DEFAULT_ICONDEF" )));
    while ( <ICON> )
    {
	next if ( /^\#/o || /^$/o );
	chop;
	( $fileName, $title, $help, $type ) = split( /\t/, $_, 4 );

	$ICON_ID[$i++] = $title;
	$ICON_FILE{$title} = $fileName;
	$ICON_HELP{$title} = $help;
	$ICON_TYPE{$title} = $type || 'article';
    }
    close ICON;
}


###
## getIconPath - アイコンDBファイルのパス名の取得
#
sub getIconPath
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
## updateBoardSubscriber - 掲示板別新規メイル送信先DBの全更新
#
# - SYNOPSIS
#	&updateBoardSubscriber($Board, *ArriveMail);
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
sub updateBoardSubscriber
{
    local( $Board, *ArriveMail ) = @_;

    local( $File ) = &getPath( $Board, $ARRIVEMAIL_FILE_NAME );
    local( $TmpFile ) = &getPath( $Board, $ARRIVEMAIL_FILE_NAME );
    open( DBTMP, ">$TmpFile" ) || &fatal( 1, $TmpFile );
    local( $line );
    foreach ( @ArriveMail )
    {
	( $line = $_ ) =~ s/\s*$//o;
	print( DBTMP "$line\n" ) || &fatal( 13, $TmpFile );
    }
    close DBTMP || &fatal( 13, $TmpFile );
    rename( $TmpFile, $File ) || &fatal( 14, "$TmpFile -&gt; $File" );
}


###
## updateBoardHeader - 掲示板別ヘッダDBの全更新
#
# - SYNOPSIS
#	&updateBoardHeader( $board, *header );
#
# - ARGS
#	$board		掲示板ID
#	*header		ヘッダ文字列
#
sub updateBoardHeader
{
    local( $board, *header ) = @_;

    local( $file ) = &getPath( $board, $HEADER_FILE_NAME );
    local( $tmpFile ) = &getPath( $board, $HEADER_FILE_NAME );
    open( DBTMP, ">$tmpFile" ) || &fatal( 1, $tmpFile );
    print( DBTMP $header ) || &fatal( 13, $tmpFile );
    close DBTMP || &fatal( 13, $tmpFile );
    rename( $tmpFile, $file ) || &fatal( 14, "$tmpFile -&gt; $file" );
}


###
## insertBoard - 掲示板DBへの追加
#
# - SYNOPSIS
#	&insertBoard( $name, $intro, $conf, *arriveMail, *header );
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
sub insertBoard
{
    local( $name, $intro, $conf, *arriveMail, *header ) = @_;

    # 掲示板ディレクトリの作成
    mkdir( $name, 0777 ) || &fatal( 1, $name );

    local( $src, $dest );

    # 記事DBの作成（コピー）
    $src = &getPath( $BOARDSRC_DIR, $DB_FILE_NAME );
    $dest = &getPath( $name, $DB_FILE_NAME );
    &copyDb( $src, $dest ) || &fatal( 20, "$src -&gt; $dest" );

    # 記事数DBの作成（コピー）
    $src = &getPath( $BOARDSRC_DIR, $ARTICLE_NUM_FILE_NAME );
    $dest = &getPath( $name, $ARTICLE_NUM_FILE_NAME );
    &copyDb( $src, $dest ) || &fatal( 20, "$src -&gt; $dest" );

    # 自動送信メイルDBの作成
    &updateBoardSubscriber( $name, *arriveMail );

    # ヘッダファイルの作成
    &updateBoardHeader( $name, *header );

    # 最後に，掲示板DBを更新する
    local( $file ) = &getPath( $SYS_DIR, $BOARD_FILE );
    local( $tmpFile ) = &getPath( $SYS_DIR, "$BOARD_FILE.$TMPFILE_SUFFIX$$" );
    local( $dbLine );
    open( DBTMP, ">$tmpFile" ) || &fatal( 1, $tmpFile );
    open( DB, "<$file" ) || &fatal( 1, $file );

    local( $dName, $dIntro, $dConf );
    while ( <DB> )
    {
	if ( /^\#/o || /^$/o )
	{
	    print( DBTMP "$_" ) || &fatal( 13, $tmpFile );
	    next;
	}
	chop;

	( $dName, $dIntro, $dConf ) = split( /\t/, $_, 3 );
	&fatal( 51, $name ) if ( $name eq $dName );

	&genTSV( *dbLine, ( $dName, $dIntro, $dConf ));
	print( DBTMP "$dbLine\n" ) || &fatal( 13, $tmpFile );
    }

    # 新しい記事のデータを書き加える．
    &genTSV( *dbLine, ( $name, $intro, $conf ));
    print( DBTMP "$dbLine\n" ) || &fatal( 13, $tmpFile );

    # close Files.
    close DB;
    close DBTMP || &fatal( 13, $tmpFile );

    rename( $tmpFile, $file ) || &fatal( 14, "$tmpFile -&gt; $file" );
}


###
## updateBoard - 掲示板DBの更新
#
# - SYNOPSIS
#	&updateBoard( $board, $valid, $intro, $conf, *arriveMail, *header );
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
sub updateBoard
{
    local( $name, $valid, $intro, $conf, *arriveMail, *header ) = @_;

    local( $file ) = &getPath( $SYS_DIR, $BOARD_FILE );
    local( $tmpFile ) = &getPath( $SYS_DIR, "$BOARD_FILE.$TMPFILE_SUFFIX$$" );
    open( DBTMP, ">$tmpFile" ) || &fatal( 1, $tmpFile );
    open( DB, "<$file" ) || &fatal( 1, $file );

    local( $dbLine, $dName, $dIntro, $dConf );
    while ( <DB> ) {

	if ( /^\#/o || /^$/o )
	{
	    print( DBTMP "$_" ) || &fatal( 13, $tmpFile );
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
	&genTSV( *dbLine, ( $dName, $dIntro, $dConf ));
	print( DBTMP "$dbLine\n" ) || &fatal( 13, $tmpFile );
    }

    # close Files.
    close DB;
    close DBTMP || &fatal( 13, $tmpFile );

    # DBを更新する
    rename( $tmpFile, $file ) || &fatal( 14, "$tmpFile -&gt; $file" );

    # 自動送信メイルDBも更新する．
    &updateBoardSubscriber( $BOARD, *arriveMail );

    # ヘッダファイルも更新する．
    &updateBoardHeader( $name, *header );
}


###
## getBoardStatus - 掲示板状態DBの読み込み
#
# - SYNOPSIS
#	&getBoardStatus( $Board, *id, *artKey );
#
# - ARGS
#	$Board		掲示板ID
#	$id		最新メッセージID
#	$artKey		キー
#
# - DESCRIPTION
#	従来の最新記事IDを読み出す．
#
sub getBoardStatus
{
    local( $Board, *id, *artKey ) = @_;

    local( $ArticleNumFile ) = &getPath( $Board, $ARTICLE_NUM_FILE_NAME );
    open( AID, "<$ArticleNumFile" ) || &fatal( 1, $ArticleNumFile );
    chop( $id = <AID> );
    chop( $artKey = <AID> );
    close AID;
}


###
## updateBoardStatus - 掲示板状態DBの更新
#
# - SYNOPSIS
#	&updateBoardStatus( $Board, $Id, $artKey );
#
# - ARGS
#	$Board		掲示板ID
#	$Id		新規に書き込む記事番号
#	$artKey		多重書き込み防止用キー
#
# - DESCRIPTION
#	記事番号DBの更新
#
sub updateBoardStatus
{
    local( $Board, $Id, $artKey ) = @_;

    local( $File, $TmpFile, $OldArticleId );
    
    # 数字のくせに古い数値より若い! (数字じゃなきゃOK)
    $OldArticleId = &getNewArtId( $Board );
    &fatal( 10, '' ) if (( $Id =~ /^\d+$/ ) && ( $Id < $OldArticleId ));

    $File = &getPath( $Board, $ARTICLE_NUM_FILE_NAME );
    $TmpFile = &getPath( $Board, "$ARTICLE_NUM_FILE_NAME.$TMPFILE_SUFFIX$$" );
    open( AID, ">$TmpFile" ) || &fatal( 1, $TmpFile );
    print( AID "$Id\n" ) || &fatal( 13, $TmpFile );
    print( AID "$artKey\n" ) || &fatal( 13, $TmpFile );
    close AID || &fatal( 13, $TmpFile );

    rename( $TmpFile, $File ) || &fatal( 14, "$TmpFile -&gt; $File" );
}


#### メッセージ関連


###
## getNofArt - メッセージ数の取得
## getArtId - メッセージIDの取得
## getArtNum - メッセージ番号の取得
#
# - SYNOPSIS
#	&getNofArt();
#	&getArtId( $num );
#	&getArtNum( $id );
#
# - ARGS
#	$num	メッセージ番号
#	$id	メッセージID
#
# - DESCRIPTION
#	全メッセージ数を取得する．削除済みメッセージは数に入らない．
#	メッセージ番号/メッセージIDから，ID/番号を取得する．
#
# - RETURN
#	メッセージ数
#	メッセージID/メッセージ番号
#
sub getNofArt
{
    $#DB_ID;
}
sub getArtId
{
    return '' if ( $_[0] < 0 );
    $DB_ID[ $_[0] ];
}
sub getArtNum
{
    local( $id ) = $_[0];
    foreach ( 0 .. &getNofArt() )
    {
#	return $_ if ( &getArtId( $_ ) eq $id );
	return $_ if ( $DB_ID[$_] eq $id );
    }
    return -1;
}


###
## getArtNewP - メッセージが新しいか否か
#
# - SYNOPSIS
#	&getArtNewP( $id );
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
sub getArtNewP
{
    $DB_NEW{ $_[0] };
}


###
## getArtInfo - メッセージ情報の取得
#
# - SYNOPSIS
#	&getArtInfo( $id );
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
sub getArticlesInfo { &getArtInfo; }
sub getArtInfo
{
    local( $id ) = @_;
    ( $DB_FID{$id}, $DB_AIDS{$id}, $DB_DATE{$id}, $DB_TITLE{$id}, $DB_ICON{$id}, $DB_REMOTEHOST{$id}, $DB_NAME{$id}, $DB_EMAIL{$id}, $DB_URL{$id}, $DB_FMAIL{$id} );
}


###
## getArtParents - メッセージ親情報の取得
## getArtParent - メッセージ親情報の取得
## getArtParentTop - メッセージ親情報の取得
## getArtDaughters - メッセージ娘情報の取得
## getArtSubject - メッセージタイトルの取得
## getArtIcon - メッセージアイコンの取得
## setArtParents - メッセージ親情報の設定
## setArtDaughters - メッセージ娘情報の設定
#
# - SYNOPSIS
#	&getArtParents( $id );
#	&getArtParent( $id );
#	&getArtParentTop( $id );
#	&getArtDaughters( $id );
#	&getArtSubject( $id );
#	&getArtIcon( $id );
#
#	&setArtParents( $id, $value );
#	&setArtDaughters( $id, $value );
#
# - ARGS
#	$id	メッセージID
#	$value	メッセージIDのリスト（「,」区切り）
#
# - DESCRIPTION
#	メッセージ親/娘情報を取得する．
#
sub getArtParents { $DB_FID{ $_[0] }; }
sub getArtDaughters { $DB_AIDS{ $_[0] }; }
sub getArtSubject { $DB_TITLE{ $_[0] }; }
sub getArtIcon { $DB_ICON{ $_[0] }; }
sub getArtParent
{
    local( $parent );
    ( $parent = $DB_FID{ $_[0] } ) =~ s/,.*$//o;
    $parent;
}
sub getArtParentTop
{
    local( $top );
    ( $top = $DB_FID{ $_[0] } ) =~ s/^.*,//o;
    $top || $_[0];
}

sub setArtParents { $DB_FID{ $_[0] } = $_[1]; }
sub setArtDaughters { $DB_AIDS{ $_[0] } = $_[1]; }


###
## getArtAuthor - メッセージ投稿者情報の取得
#
# - SYNOPSIS
#	&getArtAuthor( $id );
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
sub getArtAuthor
{
    ( $DB_NAME{ $_[0] }, $DB_EMAIL{ $_[0] }, $DB_URL{ $_[0] }, $DB_FMAIL{ $_[0] }, $DB_REMOTEHOST{ $_[0] } );
}


###
## getArtBody - メッセージ本文の取得
#
# - SYNOPSIS
#	&getArtBody( $id, $board, *articleBody );
#
# - ARGS
#	$id		メッセージID
#	$board		掲示板ID
#	*articleBody	本文各行を入れる配列変数へのリファレンス
#
# - DESCRIPTION
#	メッセージ本文を取得する．
#
sub getArtBody
{
    local( $id, $board, *articleBody ) = @_;

    local( $file ) = &getArtFileName( $id, $board );
    open( TMP, "<$file" ) || &fatal( 1, $file );
    while ( <TMP> )
    {
	push( @articleBody, $_ );
    }
    close TMP;
}


###
## getArtModifiedTime - ある記事の最終更新時刻(UTC)を取得
#
# - SYNOPSIS
#	&getArtModifiedTime($Id, $Board);
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
sub getArtModifiedTime
{
    local( $Id, $Board ) = @_;

    # 86400 = 24 * 60 * 60
    $^T - ( -M &getArtFileName( $Id, $Board )) * 86400;
}


###
## cacheArt - 記事DBの全読み込み
#
# - SYNOPSIS
#	&cacheArt( $board );
#
# - ARGS
#	$board		掲示板ID
#
# - DESCRIPTION
#	主に起動時に呼び出され，記事DBの内容を大域変数にキャッシュする．
#
sub DbCache { &cacheArt; }
sub cacheArt
{
    local( $board ) = @_;

    return unless $board;

    local( $dId, $dFid, $dAids, $dDate, $dTitle, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail );

    @DB_ID = %DB_FID = %DB_AIDS = %DB_DATE = %DB_TITLE = %DB_ICON = %DB_REMOTEHOST = %DB_NAME = %DB_EMAIL = %DB_URL = %DB_FMAIL = %DB_NEW = ();

    local( $newIconLimit );
    $newIconLimit = $^T - $SYS_NEWICON_VALUE * 24 * 60 * 60
	if ( $SYS_NEWICON == 2 );
    
    local( $i ) = 0;
    local( @data, $dId );
    local( $DBFile ) = &getPath( $board, $DB_FILE_NAME );
    open( DB, "<$DBFile" ) || &fatal( 1, $DBFile );
    while ( <DB> )
    {
	next if (/^\#/o || /^$/o);
	chop;
	( $dId, $dFid, $dAids, $dDate, $dTitle, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail ) = split( /\t/, $_, 11 );
	$DB_ID[$i++] = $dId;
	$DB_FID{$dId} = $dFid;
	$DB_AIDS{$dId} = $dAids;
	$DB_DATE{$dId} = $dDate || &getArtModifiedTime( $dId, $board );
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
}


###
## insertArt - 記事DBへの追加
#
# - SYNOPSIS
#      &insertArt( $Board, $Fid, $InputDate, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail );
#
# - ARGS
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
sub insertArt
{
    local( $Board, $Fid, $artKey, $InputDate, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail, $MailRelay, $TextType, $Article ) = @_;

    # 新しい記事番号を取得(まだ記事番号は増えてない)
    local( $newArtId ) = &getNewArtId( $Board );

    # 正規のファイルの作成
    &makeArtFile( $TextType, $Article, $newArtId, $Board );

    # 掲示板状態DBの更新
    &updateBoardStatus( $Board, $newArtId, $artKey );

    local( $dId, $dFid, $dAids, $dInputDate, $dSubject, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail, $mdName, $mdEmail, $mdInputDate, $mdSubject, $mdIcon, $mdId, $FidList, @FollowMailTo, @FFid );

    # メイル送信用に，リプライ元のリプライ元，を取ってくる
    if ( $Fid ne '' )
    {
	@FFid = split( /,/, &getArtParents( $Fid ));
    }

    $FidList = $Fid;

    local( $File ) = &getPath( $Board, $DB_FILE_NAME );
    local( $TmpFile ) = &getPath( $Board, "$DB_FILE_NAME.$TMPFILE_SUFFIX$$" );
    local( $dbLine );
    open( DBTMP, ">$TmpFile" ) || &fatal( 1, $TmpFile );
    open( DB, "<$File" ) || &fatal( 1, $File );
    while ( <DB> )
    {
	if ( /^\#/o || /^$/o )
	{
	    print( DBTMP "$_" ) || &fatal( 13, $TmpFile );
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
		$dAids .= ",$newArtId";
	    }
	    else
	    {
		$dAids = $newArtId;
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
	&genTSV( *dbLine, ( $dId, $dFid, $dAids, $dInputDate, $dSubject, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail ));
	print( DBTMP "$dbLine\n" ) || &fatal( 13, $TmpFile );

	# リプライ元のリプライ元，かつメイル送信の必要があれば，宛先を保存
	if ( $MailRelay && ( $SYS_MAIL & 2 ) && @FFid && $dFmail && $dEmail && ( grep( /^$dId$/, @FFid )) && ( !grep( /^$dEmail$/, @FollowMailTo )))
	{
	    push( @FollowMailTo, $dEmail );
	}
    }

    # 新しい記事のデータを書き加える．
    &genTSV( *dbLine, ( $newArtId, $FidList, '', $InputDate, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail ));
    print( DBTMP "$dbLine\n" ) || &fatal( 13, $TmpFile );

    # close Files.
    close DB;
    close DBTMP || &fatal( 13, $TmpFile );

    # DBを更新する
    rename( $TmpFile, $File ) || &fatal( 14, "$TmpFile -&gt; $File" );

    # 必要なら投稿があったことをメイルする
    if ( $MailRelay && $SYS_MAIL & 1 )
    {
	local( @ArriveMailTo );
	&getBoardSubscriber( 0, $Board, *ArriveMailTo );
	&arriveMail( $Name, $Email, $InputDate, $Subject, $Icon, $newArtId, @ArriveMailTo ) if @ArriveMailTo;
    }

    # 必要なら反応があったことをメイルする
    if ( $MailRelay && ( $SYS_MAIL & 2 ) && @FollowMailTo )
    {
	&followMail( $mdName, $mdEmail, $mdInputDate, $mdSubject, $mdIcon, $mdId, $Name, $Email, $InputDate, $Subject, $Icon, $newArtId, @FollowMailTo );
    }

    $newArtId;
}


###
## updateArt - 訂正記事の記事DBへの書き込み
#
# - SYNOPSIS
#	&updateArt($Board, $Id, $InputDate, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail);
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
sub updateArt
{
    local( $Board, $Id, $InputDate, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail, $TextType, $Article ) = @_;

    local( $SupersedeId, $dId, $dFid, $dAids, $dInputDate, $dSubject, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail );
    
    # initial versionは1で，1ずつ増えていく．1，2，…9，10，11，…
    # later versionはDB中で必ず，younger versionよりも下に出現する．
    # すなわち10_2，10，10_1は，10_1，10_2，10の順に並ぶものとする．
    $SupersedeId = 1;

    local( $dbLine );
    local( $File ) = &getPath( $Board, $DB_FILE_NAME );
    local( $TmpFile ) = &getPath( $Board, "$DB_FILE_NAME.$TMPFILE_SUFFIX$$" );
    open( DBTMP, ">$TmpFile" ) || &fatal( 1, $TmpFile );
    open( DB, "<$File" ) || &fatal( 1, $File );
    while ( <DB> )
    {
	if ( /^\#/o || /^$/o )
	{
	    print( DBTMP "$_" ) || &fatal( 13, $TmpFile );
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
	    &genTSV( *dbLine, ( sprintf( "-%s_%s", $dId, $SupersedeId ), $dFid, $dAids, $dInputDate, $dSubject, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail ));
	    print( DBTMP "#$dbLine\n" ) || &fatal( 13, $TmpFile );

	    # 続いて新しい記事を書き加える
	    &genTSV( *dbLine, ( $Id, $dFid, $dAids, $InputDate, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail ));
	    print( DBTMP "$dbLine\n" ) || &fatal( 13, $TmpFile );
	}
	else
	{
	    # DBに書き加える
	    print( DBTMP "$_\n" ) || &fatal( 13, $TmpFile );
	}
    }

    # close Files.
    close DB;
    close DBTMP || &fatal( 13, $TmpFile );

    # DBを更新する
    rename( $TmpFile, $File ) || &fatal( 14, "$TmpFile -&gt; $File" );

    # ex. 「100」→「100_5」
    local( $oldFile ) = &getArtFileName( $Id, $Board );
    local( $supersedeFile ) = &getArtFileName( sprintf( "%s_%s", $Id, $SupersedeId ), $Board );
    rename( $oldFile, $supersedeFile ) || &fatal( 14, "$File -&gt; $supersedeFile" );

    # 正規のファイルの作成
    &makeArtFile( $TextType, $Article, $Id, $Board );
}


###
## flushArt - 記事DBの全更新
#
# - SYNOPSIS
#	&flushArt( $Board );
#
# - ARGS
#	$Board		掲示板ID
#
# - DESCRIPTION
#	記事DBを，新たな記事データで全更新する．
#	書き込む記事データはキャッシュされているもの．
#
sub flushArt
{
    local( $Board ) = @_;

    local( $dId, $dbLine );
    local( $File ) = &getPath($Board, $DB_FILE_NAME);
    local( $TmpFile ) = &getPath( $Board, "$DB_FILE_NAME.$TMPFILE_SUFFIX$$" );
    open( DBTMP, ">$TmpFile" ) || &fatal( 1, $TmpFile );
    open( DB, "<$File" ) || &fatal( 1, $File );
    while ( <DB> )
    {
	if ( /^\#/o || /^$/o )
	{
	    print( DBTMP "$_" ) || &fatal( 13, $TmpFile );
	    next;
	}

	# Idを取り出す
	chop;
	( $dId = $_ ) =~ s/\t.*$//;

	# DBに書き加える
	&genTSV( *dbLine, ( $dId, $DB_FID{$dId}, $DB_AIDS{$dId}, $DB_DATE{$dId}, $DB_TITLE{$dId}, $DB_ICON{$dId}, $DB_REMOTEHOST{$dId}, $DB_NAME{$dId}, $DB_EMAIL{$dId}, $DB_URL{$dId}, $DB_FMAIL{$dId} ));
	print( DBTMP "$dbLine\n" ) || &fatal( 13, $TmpFile );
    }

    # close Files.
    close DB;
    close DBTMP || &fatal( 13, $TmpFile );

    # DBを更新する
    rename( $TmpFile, $File ) || &fatal( 14, "$TmpFile -&gt; $File" );

    # DB書き換えたので，キャッシュし直す
    &cacheArt( $Board );
}


###
## deleteArt - 記事DBの更新
#
# - SYNOPSIS
#	&deleteArt( $Board, *Target );
#
# - ARGS
#	$Board		掲示板ID
#	*Target		削除する記事IDのリスト
#
# - DESCRIPTION
#	記事DBから指定された記事群のエントリを削除する．
#
sub deleteArt
{
    local( $Board, *Target ) = @_;

    local( $dId, $dbLine );
    local( $File ) = &getPath( $Board, $DB_FILE_NAME );
    local( $TmpFile ) = &getPath( $Board, "$DB_FILE_NAME.$TMPFILE_SUFFIX$$" );
    open( DBTMP, ">$TmpFile" ) || &fatal( 1, $TmpFile );
    open( DB, "<$File" ) || &fatal( 1, $File );
    while ( <DB> )
    {
	if ( /^\#/o || /^$/o )
	{
	    print( DBTMP "$_" ) || &fatal( 13, $TmpFile );
	    next;
	}

	# Idを取り出す
	chop;
	( $dId = $_ ) =~ s/\t.*$//;

	# 該当記事はコメントアウト
	if ( grep( /^$dId$/, @Target ))
	{
	    print( DBTMP "#" ) || &fatal( 13, $TmpFile );
	}

	&genTSV( *dbLine, ( $dId, $DB_FID{$dId}, $DB_AIDS{$dId}, $DB_DATE{$dId}, $DB_TITLE{$dId}, $DB_ICON{$dId}, $DB_REMOTEHOST{$dId}, $DB_NAME{$dId}, $DB_EMAIL{$dId}, $DB_URL{$dId}, $DB_FMAIL{$dId} ));
	print( DBTMP "$dbLine\n" ) || &fatal( 13, $TmpFile );
    }

    # close Files.
    close DB;
    close DBTMP || &fatal( 13, $TmpFile );

    # DBを更新する
    rename( $TmpFile, $File ) || &fatal( 14, "$TmpFile -&gt; $File" );
}


###
## reOrderArt - 記事DBの順序変更
#
# - SYNOPSIS
#	&reOrderArt( $Board, $Id, *Move );
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
sub reOrderArt
{
    local( $Board, $Id, *Move ) = @_;

    # 先頭フラグ
    local( $TopFlag ) = 1;

    local( $dId, $dbLine );
    local( $File ) = &getPath( $Board, $DB_FILE_NAME );
    local( $TmpFile ) = &getPath( $Board, "$DB_FILE_NAME.$TMPFILE_SUFFIX$$" );
    open( DBTMP, ">$TmpFile" ) || &fatal( 1, $TmpFile );
    open( DB, "<$File" ) || &fatal( 1, $File );
    while ( <DB> )
    {
	if ( /^\#/o || /^$/o )
	{
	    print( DBTMP "$_" ) || &fatal( 13, $TmpFile );
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
		&genTSV( *dbLine, ( $_, $DB_FID{$_}, $DB_AIDS{$_}, $DB_DATE{$_}, $DB_TITLE{$_}, $DB_ICON{$_}, $DB_REMOTEHOST{$_}, $DB_NAME{$_}, $DB_EMAIL{$_}, $DB_URL{$_}, $DB_FMAIL{$_} ));
		print( DBTMP "$dbLine\n" ) || &fatal( 13, $TmpFile );
	    }
	}

	# 移動先がきたら，先に書き込む(新着が上，の場合)
	if (( $SYS_BOTTOMTITLE == 0 ) && ( $dId eq $Id ))
	{
	    foreach ( @Move )
	    {
		&genTSV( *dbLine, ( $_, $DB_FID{$_}, $DB_AIDS{$_}, $DB_DATE{$_}, $DB_TITLE{$_}, $DB_ICON{$_}, $DB_REMOTEHOST{$_}, $DB_NAME{$_}, $DB_EMAIL{$_}, $DB_URL{$_}, $DB_FMAIL{$_} ));
		print( DBTMP "$dbLine\n" ) || &fatal( 13, $TmpFile );
	    }
	}

	# DBに書き加える
	&genTSV( *dbLine, ( $dId, $DB_FID{$dId}, $DB_AIDS{$dId}, $DB_DATE{$dId}, $DB_TITLE{$dId}, $DB_ICON{$dId}, $DB_REMOTEHOST{$dId}, $DB_NAME{$dId}, $DB_EMAIL{$dId}, $DB_URL{$dId}, $DB_FMAIL{$dId} ));
	print( DBTMP "$dbLine\n" ) || &fatal( 13, $TmpFile );

	# 移動先がきたら，続けて書き込む(新着が下，の場合)
	if (( $SYS_BOTTOMTITLE == 1 ) && ( $dId eq $Id ))
	{
	    foreach ( @Move )
	    {
		&genTSV( *dbLine, ( $_, $DB_FID{$_}, $DB_AIDS{$_}, $DB_DATE{$_}, $DB_TITLE{$_}, $DB_ICON{$_}, $DB_REMOTEHOST{$_}, $DB_NAME{$_}, $DB_EMAIL{$_}, $DB_URL{$_}, $DB_FMAIL{$_} ));
		print( DBTMP "$dbLine\n" ) || &fatal( 13, $TmpFile );
	    }
	}
    }

    # 先頭にする時の処理(新着が上，の場合)
    if (( $Id eq '' ) && ( $SYS_BOTTOMTITLE == 0 ))
    {
	foreach ( @Move )
	{
	    &genTSV( *dbLine, ( $_, $DB_FID{$_}, $DB_AIDS{$_}, $DB_DATE{$_}, $DB_TITLE{$_}, $DB_ICON{$_}, $DB_REMOTEHOST{$_}, $DB_NAME{$_}, $DB_EMAIL{$_}, $DB_URL{$_}, $DB_FMAIL{$_} ));
	    print( DBTMP "$dbLine\n" ) || &fatal( 13, $TmpFile );
	}
    }

    # close Files.
    close DB;
    close DBTMP || &fatal( 13, $TmpFile );

    # DBを更新する
    rename( $TmpFile, $File ) || &fatal( 14, "$TmpFile -&gt; $File" );

    # DB書き換えたので，キャッシュし直す
    &cacheArt( $Board );
}


###
## getNewArtId - 新着記事IDの決定
#
# - SYNOPSIS
#	&getNewArtId($Board);
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
sub getNewArtId
{
    local( $Board ) = @_;
    local( $id, $artKey );
    &getBoardStatus( $Board, *id, *artKey );
    $id + 1;
}


###
## makeArtFile - 記事本文DBへの追加
#
# - SYNOPSIS
#	&makeArtFile($TextType, $Article, $Id, $Board);
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
sub makeArtFile
{
    local( $TextType, $Article, $Id, $Board ) = @_;

    local( $File ) = &getArtFileName( $Id, $Board );

    open( TMP, ">$File" ) || &fatal( 1, $File );
    printf( TMP "<!-- Kb-System-Id: %s/%s -->\n", $KB_VERSION, $KB_RELEASE)
	|| &fatal( 13, $File );
    print( TMP "$Article\n" ) || &fatal( 13, $File );
    close TMP || &fatal( 13, $File );
}


###
## getArtFileName - 記事本文DBファイルのパス名の取得
#
# - SYNOPSIS
#	&getArtFileName($Id, $Board);
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
sub getArtFileName
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
## copyDb - DBのコピー
#
# - SYNOPSIS
#	&copyDb( $src, $dest );
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
sub copyDb
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
## genTSV - タブ区切り文字列の作成
#
# - SYNOPSIS
#	&genTSV( *line, @data );
#
# - ARGS
#	$line	タブ区切りのデータを格納する文字列
#	@data	データ
#
# - DESCRIPTION
#	データをTSVフォーマットに整形する．
#	データは改行を含んではならない．
#
sub genTSV
{
    local( *line, @data ) = @_;
    grep( s/\t/$COLSEP/go, @data );
    $line = join( "\t", @data );
}
