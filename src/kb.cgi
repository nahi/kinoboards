#!/usr/local/bin/perl

# このファイルの変更は最低2箇所，最大4箇所です（環境次第です）．
#
# 1. ↑の先頭行で，Perlのパスを指定します．「#!」に続けて指定してください．

# 2. kbディレクトリのフルパスを指定してください（URLではなく，パスです）．
#    !! KB/1.0R6.4以降，この設定は必須となりました !!
#
$KBDIR_PATH = '';
# $KBDIR_PATH = '/home/nahi/public_html/kb/';
# $KBDIR_PATH = 'd:\inetpub\wwwroot\kb\';	# WinNT/Win9xの場合
# $KBDIR_PATH = 'foo:bar:kb:';			# Macの場合?

# 3. サーバが動いているマシンがWin95/Macの場合，
#    $PCを1に設定してください．そうでない場合，この設定は不要です．
#
$PC = 0;	# for UNIX / WinNT
# $PC = 1;	# for Win95 / Mac

# 4. サーバがCGIWRAPを利用している場合，以下のコメントを外し，
#    kbディレクトリのURLを指定してください（今度はパスではなく，URLです）．
#    そうでない人は，変更の必要はありません．コメントのままでOKです．
#
# $KB_RESOURCE_URL = '/~nahi/kb/';


# 以下は書き換えの必要はありません．


######################################################################


# $Id: kb.cgi,v 5.43.2.6 2000-04-05 14:44:22 nakahiro Exp $

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

# 大域変数の定義
$HEADER_FILE = 'kb.ph';		# header file
$KB_VERSION = '1.0';		# version
$KB_RELEASE = '6.10';		# release

# ディレクトリ
$ICON_DIR = 'icons';				# アイコンディレクトリ
$UI_DIR = 'UI';					# UIディレクトリ
$LOG_DIR = 'log';				# ログディレクトリ

# ファイル
$BOARD_ALIAS_FILE = 'kinoboards';		# 掲示板DB
$CONF_FILE_NAME = 'kb.conf';			# 掲示板別configuratinファイル
$ARRIVEMAIL_FILE_NAME = 'kb.mail';		# 掲示板別新規メイル送信先DB
$BOARD_FILE_NAME = 'kb.board';			# タイトルリストヘッダDB
$DB_FILE_NAME = 'kb.db';			# 記事DB
$ARTICLE_NUM_FILE_NAME = 'kb.aid';		# 記事番号DB
$USER_ALIAS_FILE = 'kinousers';			# ユーザエイリアス用DB
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
$KB_RESOURCE_URL = $KB_RESOURCE_URL || $cgi'PATH_INFO;
$KB_RESOURCE_URL .= '/' if ( $KB_RESOURCE_URL && $KB_RESOURCE_URL !~ m!/$!o );
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
$HTML_TAGS_COREATTRS = 'ID/CLASS/STYLE/TITLE';
$HTML_TAGS_I18NATTRS = 'LANG/DIR';
$HTML_TAGS_GENATTRS = "$HTML_TAGS_COREATTRS/$HTML_TAGS_I18NATTRS";

# アイコンファイル相対URL
$ICON_BLIST = &GetIconURL( 'blist.gif' );		# 掲示板一覧へ
$ICON_TLIST = &GetIconURL( 'tlist.gif' );		# タイトル一覧へ
$ICON_PREV = &GetIconURL( 'prev.gif' );			# 前の記事へ
$ICON_NEXT = &GetIconURL( 'next.gif' );			# 次の記事へ
$ICON_WRITENEW = &GetIconURL( 'writenew.gif' );		# 新規書き込み
$ICON_FOLLOW = &GetIconURL( 'follow.gif' );		# リプライ
$ICON_QUOTE = &GetIconURL( 'quote.gif' );		# 引用してリプライ
$ICON_THREAD = &GetIconURL( 'thread.gif' );		# まとめ読み
$ICON_HELP = &GetIconURL( 'help.gif' );			# ヘルプ
$ICON_DELETE = &GetIconURL( 'delete.gif' );		# 削除
$ICON_SUPERSEDE = &GetIconURL( 'supersede.gif' );	# 訂正
$ICON_NEW = &GetIconURL( 'listnew.gif' );		# 新着

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


######################################################################


###
## MAIN - メインブロック
#
# - SYNOPSIS
#	kb.cgi
#
# - ARGS
#	なし
#
# - DESCRIPTION
#	起動時に一度だけ参照される．
#	引き数はないが，環境変数QUERY_STRINGとREQUEST_METHOD，
#	もしくは標準入力経由で値を渡さないと，正しく動作しない．
#
# - RETURN
#	なし
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
	$modTime = &GetModifiedTime( $DB_FILE_NAME, $cgi'TAGS{'b'} )
	    if $cgi'TAGS{'b'};
	&cgi'Header( 1, $modTime, 0, (), 0 );
	last;
    }

    local( $c ) = $cgi'TAGS{'c'};
    local( $com ) = $cgi'TAGS{'com'};
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
            $c = 'v';
        }
        elsif ( $SYS_F_B )
        {
            $c = 'bl';
        }
        else
        {
            $c = 'v';
            $BOARD = 'test';
        }
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
	    eval( "require( \"$boardConfFile\" );" ) ||
		&Fatal( 1, $boardConfFile );
	}
    }

    if ( $BOARDLIST_URL eq '-' ) { $BOARDLIST_URL = "$PROGRAM?c=bl"; }
    $SYS_F_MT = ( $SYS_F_D || $SYS_F_AM || $SYS_F_MV );

    if ( $c eq 'e' )
    {
	### ShowArticle - 単一記事の表示
	require( &GetPath( $UI_DIR, 'ShowArticle.pl' ));
	last;
    }
    elsif ( $SYS_F_T && ( $c eq 't' ))
    {
	### ThreadArticle - フォロー記事を全て表示．
	require( &GetPath( $UI_DIR, 'ThreadArticle.pl' ));
	last;
    }

    if ( $SYS_F_N )
    {
	if (( $c eq 'x' ) && ( $com ne 'x' ))
	{
	    # previewからの戻りなので，コマンド書き換え．
	    $gVarBack = 1;
	    $cgi'TAGS{'c'} = $cgi'TAGS{'corig'};
	    $c = $cgi'TAGS{'c'};
	}

	### Entry - 書き込み画面の表示
	if ( $c eq 'n' )
	{
	    # 新規
	    $gVarEntryType = 0;
	    require( &GetPath( $UI_DIR, 'Entry.pl' ));
	    last;
	}
	elsif (( $c eq 'f' ) && !$cgi'TAGS{'s'} )
	{
	    # リプライ
	    $gVarEntryType = 1;
	    require( &GetPath( $UI_DIR, 'Entry.pl' ));
	    last;
	}
	elsif ( $c eq 'q' )
	{
	    # 引用リプライ
	    $gVarEntryType = 2;
	    require( &GetPath( $UI_DIR, 'Entry.pl' ));
	    last;
	}
	elsif ( $SYS_F_D && ( $c eq 'f' ) && $cgi'TAGS{'s'} )
	{
	    # 訂正
	    $gVarEntryType = 3;
	    require( &GetPath( $UI_DIR, 'Entry.pl' ));
	    last;
	}
	elsif (( $c eq 'p' ) && ( $com ne 'x' ))
	{
	    ### Preview - プレビュー画面の表示
	    require( &GetPath( $UI_DIR, 'Preview.pl' ));
	    last;
	}
	elsif (( $c eq 'p' ) && ( $com eq 'x' ))
	{
	    ### Thanks - 登録後画面の表示（直接）
	    $gVarPreviewFlag = 0;
	    require( &GetPath( $UI_DIR, 'Thanks.pl' ));
	    last;
	}
	elsif (( $c eq 'x' ) && ( $com eq 'x' ))
	{
	    ### Thanks - 登録後画面の表示（プレビュー経由）
	    $gVarPreviewFlag = 1;
	    require( &GetPath( $UI_DIR, 'Thanks.pl' ));
	    last;
	}
    }

    if ( $c eq 'v' )
    {
	### ThreadTitle - スレッド別タイトル一覧
	$gVarComType = 0;
	require( &GetPath( $UI_DIR, 'ThreadTitle.pl' ));
	last;
    }
    elsif ( $c eq 'vt' )
    {
	### ThreadExt - スレッド別タイトルおよび記事一覧
	require( &GetPath( $UI_DIR, 'ThreadExt.pl' ));
	last;
    }
    elsif ( $SYS_F_R && ( $c eq 'r' ))
    {
	### SortTitle - 日付順にソート
	require( &GetPath( $UI_DIR, 'SortTitle.pl' ));
	last;
    }
    elsif ( $SYS_F_L && ( $c eq 'l' ))
    {
	### SortArticle - 新しい記事をまとめて表示
	require( &GetPath( $UI_DIR, 'SortArticle.pl' ));
	last;
    }
    elsif ( $SYS_F_S && ( $c eq 's' ))
    {
	### SearchArticle - 記事の検索(表示画面の作成)
	require( &GetPath( $UI_DIR, 'SearchArticle.pl' ));
	last;
    }
    elsif ( $SYS_ICON && ( $c eq 'i' ))
    {
	### ShowIcon - アイコン表示画面
	require( &GetPath( $UI_DIR, 'ShowIcon.pl' ));
	last;
    }

    if ( $SYS_ALIAS )
    {
	if ( $c eq 'an' )
	{
	    ### AliasNew - エイリアスの登録と変更画面の表示
	    require( &GetPath( $UI_DIR, 'AliasNew.pl' ));
	    last;
	}
	elsif ( $c eq 'am' )
	{
	    ### AliasMod - ユーザエイリアスの登録/変更
	    require( &GetPath( $UI_DIR, 'AliasMod.pl' ));
	    last;
	}
	elsif ( $c eq 'ad' )
	{
	    ### AliasDel - ユーザエイリアスの削除
	    require( &GetPath( $UI_DIR, 'AliasDel.pl' ));
	    last;
	}
	elsif ( $c eq 'as' )
	{
	    ### AliasShow - ユーザエイリアス参照画面の表示
	    require( &GetPath( $UI_DIR, 'AliasShow.pl' ));
	    last;
	}
    }

    if ( $SYS_F_B && ( $c eq 'bl' ))
    {
	### BoardList - 掲示板一覧の表示
	require( &GetPath( $UI_DIR, 'BoardList.pl' ));
	last;
    }

    # 以下は管理用
    if ( $SYS_F_MV )
    {
	if  ( $c eq 'ct' )
	{
	    $gVarComType = 2;
	    require( &GetPath( $UI_DIR, 'ThreadTitle.pl' ));
	    last;
	}
	elsif ( $c eq 'ce' )
	{
	    $gVarComType = 3;
	    require( &GetPath( $UI_DIR, 'ThreadTitle.pl' ));
	    last;
	}
	elsif ( $c eq 'mvt' )
	{
	    $gVarComType = 4;
	    require( &GetPath( $UI_DIR, 'ThreadTitle.pl' ));
	    last;
	}
	elsif ( $c eq 'mve' )
	{
	    $gVarComType = 5;
	    require( &GetPath( $UI_DIR, 'ThreadTitle.pl' ));
	    last;
	}
    }

    if ( $SYS_F_D )
    {
	if ( $c eq 'dp' )
	{
	    ### DeletePreview - 削除記事の確認
	    require( &GetPath( $UI_DIR, 'DeletePreview.pl' ));
	    last;
	}
	elsif ( $c eq 'de' )
	{
	    ### DeleteExec - 記事の削除
	    $gVarThreadFlag = 0;
	    require( &GetPath( $UI_DIR, 'DeleteExec.pl' ));
	    last;
	}
	elsif ( $c eq 'det' ) {
	    $gVarThreadFlag = 1;
	    require( &GetPath( $UI_DIR, 'DeleteExec.pl' ));
	    last;
	}
    }

    if ( $SYS_F_AM )
    {
	if ( $c eq 'mp' )
	{
	    ### ArriveMailEntry - メイル自動配信先の指定
	    require( &GetPath( $UI_DIR, 'ArriveMailEntry.pl' ));
	    last;
	}
	elsif ( $c eq 'me' )
	{
	    ### ArriveMailExec - メイル自動配信先の設定
	    require( &GetPath( $UI_DIR, 'ArriveMailExec.pl' ));
	    last;
	}
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
# ユーザインタフェイスインプリメンテーション(個別)


###
## Fatal - エラー表示
#
# - SYNOPSIS
#	Fatal($errno, $errInfo);
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
    ( $gVarFatalNo, $gVarFatalInfo ) = @_;
    require( &GetPath( $UI_DIR, 'Fatal.pl' ));
}


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
    &SendMail( $Name, $Email, $MailSubject, $Message, $Id, @To );
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
    
    local( $StrSubject, $FstrSubject, $MailSubject, $StrFrom, $FstrFrom, $Message );

    $StrSubject = ( !$SYS_ICON || ( $Icon eq $H_NOICON ))? "$Subject" :
	"($Icon) $Subject";
    $StrSubject =~ s/<[^>]*>//go;	# タグは要らない
    $StrSubject = &HTMLDecode( $StrSubject );
    $FstrSubject = ( $Ficon eq $H_NOICON )? $Fsubject : "($Ficon) $Fsubject";
    $FstrSubject =~ s/<[^>]*>//go;	# タグは要らない
    $FstrSubject = &HTMLDecode( $FstrSubject );
    $MailSubject = &GetMailSubjectPrefix( $BOARDNAME, $Fid ) . $FstrSubject;
    $StrFrom = $Email? "$Name <$Email>" : "$Name";

    local( $ffIds ) = &GetArticlesInfo( $Id );
    local( $topId ) = ( $ffIds =~ m/([^,]+)$/o );

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
    &SendMail( $Fname, $Femail, $MailSubject, $Message, $Fid, @To );
}


######################################################################
# ユーザインタフェイスインプリメンテーション(共通部)


###
## ViewOriginalArticle - 元記事の表示
#
# - SYNOPSIS
#	ViewOriginalArticle($Id, $CommandFlag, $OriginalFlag);
#
# - ARGS
#	$Id			記事ID
#	$CommandFlag		コマンドを表示するか否か(表示する=1)
#	$OriginalFlag		その記事中に，(あれば)元記事へのリンクを
#				表示するか否か(表示する=1)
#
# - DESCRIPTION
#	元記事を表示する．
#
# - RETURN
#	なし
#
sub ViewOriginalArticle
{
    local( $Id, $CommandFlag, $OriginalFlag ) = @_;

    local( $Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url ) = &GetArticlesInfo( $Id );

    # 未投稿記事は読めない
    &Fatal( 8, '' ) if ( $Subject eq '' );

    local( $Num );
    foreach ( 0 .. $#DB_ID ) { $Num = $_, last if ( $DB_ID[$_] eq $Id ); }
    local( $PrevId ) = $DB_ID[$Num - 1] if ( $Num > 0 );
    local( $NextId ) = $DB_ID[$Num + 1];

    local( $msg );

    $msg .= "<p><a name=\"a$Id\"> </a>\n";
    # $msg .= "<p id=\"a$Id\">"; # NC/4.5 does not follows this style... (-_-

    if ( $CommandFlag && $SYS_COMMAND )
    {
	# コマンド表示
	if ( $SYS_COMICON == 1 )
	{
	    $DlmtS = "";
	    $DlmtL = " // ";
	}
	elsif ( $SYS_COMICON == 2 )
	{
	    $DlmtS = " | ";
	    $DlmtL = "";
	}
	else
	{
	    $DlmtS = " | ";
	    $DlmtL = "";
	}

	local( $Old ) = &GetTitleOldIndex( $Id );

	$msg .= &TagA( $BOARDLIST_URL, &TagComImg( $ICON_BLIST, $H_BACKBOARD,
	    $SYS_COMICON )) . "\n" if $SYS_F_B;

	$msg .= $DlmtS .
	    &TagA( "$PROGRAM?b=$BOARD&c=v&num=$DEF_TITLE_NUM&old=$Old",
	    &TagComImg( $ICON_TLIST, $H_BACKTITLEREPLY, $SYS_COMICON )) . "\n";
	
	local( $TagTmp ) = &TagComImg( $ICON_PREV, $H_PREVARTICLE, $SYS_COMICON );
	if ( $PrevId ne '' )
	{
	    $msg .= $DlmtS .
		&TagA( "$PROGRAM?b=$BOARD&c=e&id=$PrevId", $TagTmp ) . "\n";
	}
	else
	{
	    $msg .= "$DlmtS$TagTmp\n";
	}
	
	$TagTmp = &TagComImg( $ICON_NEXT, $H_NEXTARTICLE, $SYS_COMICON );
	if ( $NextId ne '' )
	{
	    $msg .= $DlmtS .
		&TagA( "$PROGRAM?b=$BOARD&c=e&id=$NextId", $TagTmp ) . "\n";
	}
	else
	{
	    $msg .= "$DlmtS$TagTmp\n";
	}
	
	if ( $SYS_F_T )
	{
	    $TagTmp = &TagComImg( $ICON_THREAD, $H_READREPLYALL, $SYS_COMICON );
	    if ( $Aids ne '' )
	    {
		$msg .= $DlmtS .
		    &TagA( "$PROGRAM?b=$BOARD&c=t&id=$Id", $TagTmp ) . "\n";
	    }
	    else
	    {
		$msg .= "$DlmtS$TagTmp\n";
	    }
	}

	$msg .= "$DlmtL\n" if $DlmtL;

	if ( $SYS_F_N )
	{
	    $msg .= $DlmtS . &TagA( "$PROGRAM?b=$BOARD&c=n",
		&TagComImg( $ICON_WRITENEW, $H_POSTNEWARTICLE, $SYS_COMICON ))
		. "\n" .
		$DlmtS . &TagA( "$PROGRAM?b=$BOARD&c=f&id=$Id",
		&TagComImg( $ICON_FOLLOW, $H_REPLYTHISARTICLE, $SYS_COMICON ))
		. "\n" .
		$DlmtS . &TagA( "$PROGRAM?b=$BOARD&c=q&id=$Id",
		&TagComImg( $ICON_QUOTE, $H_REPLYTHISARTICLEQUOTE,
		$SYS_COMICON )) . "\n";
	}

	$msg .= "$DlmtL\n" if $DlmtL;

	if ( $SYS_COMICON == 1 )
	{
	    $msg .= $DlmtS . &TagA( "$PROGRAM?b=$BOARD&c=i&type=article",
		&TagComImg( $ICON_HELP, "ヘルプ", $SYS_COMICON )) . "\n";
	}
	$msg .= "</p>\n<p>\n";
    }

    # 記事番号，題
    $msg .= "<strong>$H_SUBJECT</strong>: <strong>$Id .</strong> ";
    $msg .= &TagMsgImg( $Icon ) . $Subject;

    # お名前
    if ( $Url eq '' )
    {
	$msg .= "<br>\n<strong>$H_FROM</strong>: $Name";
    }
    else
    {
	$msg .=  "<br>\n<strong>$H_FROM</strong>: " . &TagA( $Url, $Name );
    }

    # メイル
    $msg .= ' ' . &TagA( "mailto:$Email" , "&lt;$Email&gt;" )
	if ( $SYS_SHOWMAIL && $Email );

    # マシン
    $msg .= "<br>\n<strong>$H_HOST</strong>: $RemoteHost" if $SYS_SHOWHOST;

    # 投稿日
    $msg .= "<br>\n<strong>$H_DATE</strong>: " .
	&GetDateTimeFormatFromUtc( $Date );

    # 反応元(引用の場合)
    &ShowLinksToFollowedArticle( *msg, split( /,/, $Fid ))
	if ( $OriginalFlag && ( $Fid ne '' ));

    # 切れ目
    $msg .= "</p>\n$H_LINE\n";

    &cgiprint'Cache( $msg );
    $msg = '';

    # 記事の中身
    local( @ArticleBody );
    &GetArticleBody( $Id, $BOARD, *ArticleBody );
    &cgiprint'Cache( @ArticleBody );
}


###
## ThreadArticleMain - フォロー記事を全て表示．
#
# - SYNOPSIS
#	ThreadArticle($SubjectOnly, $Head, @Tail);
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
# - RETURN
#	なし
#
sub ThreadArticleMain
{
    local( $State, $Head, @Tail ) = @_;

    # 記事概要か，記事そのものか．
    if ( $State&4 )
    {
	if ( $Head eq '(' )
	{
	    &cgiprint'Cache( "<ul>\n" );
	}
	elsif ( $Head eq ')' )
        {
	    &cgiprint'Cache( "</ul>\n" );
	}
	else
	{
	    local( $dFid, $dAids, $dDate, $dSubject, $dIcon, $dRemoteHost, $dName ) = &GetArticlesInfo( $Head );
	    &cgiprint'Cache( "<li>", &GetFormattedTitle( $Head, $dAids, $dIcon, $dSubject, $dName, $dDate, $State&3 ), "\n" );
	    $State ^= 1 if ( $State&1 );
	}
    }
    elsif (( $Head ne '(' ) && ( $Head ne ')' ))
    {
	# 元記事の表示(コマンド付き, 元記事なし)
	&cgiprint'Cache( "$H_HR\n" );
	&ViewOriginalArticle( $Head, $SYS_COMMAND_EACH, 0 );
    }

    # tail recuresive.
    &ThreadArticleMain( $State, @Tail ) if @Tail;
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
# - RETURN
#	なし
#
sub QuoteOriginalArticle
{
    local( $Id, *msg ) = @_;

    local( $Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $pFid, $pAids, $pDate, $pSubject, $pIcon, $pRemoteHost, $pName, $QMark, $line, @ArticleBody );

    # 元記事情報の取得
    ( $Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name ) = &GetArticlesInfo( $Id );

    # 元記事のさらに元記事情報
    if ( $Fid )
    {
	$Fid =~ s/,.*$//o;
	( $pFid, $pAids, $pDate, $pSubject, $pIcon, $pRemoteHost, $pName ) = &GetArticlesInfo( $Fid );
    }

    # 引用
    &GetArticleBody( $Id, $BOARD, *ArticleBody );
    foreach $line ( @ArticleBody )
    {
	&TAGEncode( *line );

	$QMark = $DEFAULT_QMARK;
	$QMark = $Name . $QMark if $SYS_QUOTENAME;

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
# - RETURN
#	なし
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
## ReplyArticles - リプライ記事へのリンクの表示
#
# - SYNOPSIS
#	ReplyArticles( @_ );
#
# - ARGS
#	@_	リプライ記事IDのリスト
#
# - DESCRIPTION
#	リプライ記事へのリンクを表示する．
#
# - RETURN
#	なし
#
sub ReplyArticles
{
    &cgiprint'Cache( "$H_LINE\n<p>\n" );

    # 反応記事
    &cgiprint'Cache( "▼$H_REPLY\n" );

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
	    &ThreadArticleMain( 4, @tree );
	}
    }
    else
    {
	# 反応記事無し
	&cgiprint'Cache( "<ul>\n<li>現在，この$H_MESGへの$H_REPLYはありません\n</ul>\n" );
    }

    &cgiprint'Cache( "</p>\n" );
}


###
## BoardHeader - 掲示板ヘッダの表示
#
# - SYNOPSIS
#	BoardHeader();
#
# - ARGS
#	なし
#
# - DESCRIPTION
#	掲示板のヘッダを表示する．
#
# - RETURN
#	なし
#
sub BoardHeader
{
    local( $msg );
    &GetBoardHeader( $BOARD, *msg );
    &cgiprint'Cache( $msg );

    if ( $SYS_F_MT )
    {
	&cgiprint'Cache( "<p>\n<ul>\n" );
	&cgiprint'Cache( "<li>", &TagA( "$PROGRAM?c=mp&b=$BOARD", "自動$H_MAIL配信先を設定する" ), "\n" ) if $SYS_F_AM;
	&cgiprint'Cache( "</ul>\n</p>\n" );
    }
}


###
## ShowPageLinkTop - ページヘッダ/フッタの表示
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
#
# - DESCRIPTION
#	ページヘッダ/フッタのリンク群文字列を取得する．
#
# - RETURN
#	なし
#
sub PageLink
{
    local( $com, $num, $old, $rev ) = @_;

    local( $nextOld ) = ( $old > $num )? ( $old - $num ) : 0;
    local( $backOld ) = ( $old + $num );

    local( $str );
    $str = '<p>';

    if ( $old )
    {
	$str .= &TagA( "$PROGRAM?b=$BOARD&c=$com&num=$num&old=$nextOld&rev=$rev", "$H_TOP$H_NEXTART" );
    }
    else
    {
	$str .= $H_NONEXTART;
    }

    if ( $SYS_REVERSE )
    {
	$str .= ' // ' . &TagA( "$PROGRAM?b=$BOARD&c=$com&num=$num&old=$old&rev=" . ( 1-$rev ), $H_REVERSE );
    }

    $str .= ' // ';

    if ( $num && ( $#DB_ID - $old - $num >= 0 ))
    {
	$str .= &TagA( "$PROGRAM?b=$BOARD&c=$com&num=$num&old=$backOld&rev=$rev", "$H_BACKART$H_BOTTOM" );
    }
    else
    {
	$str .= $H_NOBACKART;
    }

    $str .= "</p>\n";

    $str;
}

sub ShowPageLinkEachPage	# not used.
{
    local( $com, $num, $old, $rev, $vRev ) = @_;

    local( $nextOld ) = ( $old > $num )? ( $old - $num ) : 0;
    local( $backOld ) = ( $old + $num );

    local( $str );
    $str = '<p>';

    $MAX_PAGELINK = 5;

    if ( $SYS_REVERSE )
    {
	$str .= &TagA( "$PROGRAM?b=$BOARD&c=$com&num=$num&old=$old&rev=" . ( 1-$rev ), $H_REVERSE ) . ' ';
    }

    if ( $vRev )
    {
	if ( $num && ( $#DB_ID - $old - $num > 0 ))
	{
	    $str .= &TagA( "$PROGRAM?b=$BOARD&c=$com&num=$num&old=$backOld&rev=$rev", $H_TOP );
	}
	else
	{
	    $str .= $H_TOP;
	}

	local( $i );
	for ( $i = -$MAX_PAGELINK; $i <= +$MAX_PAGELINK; $i++ )
	{
	    $str .= ' ';
	    if ( $old - $i * $num <= $#DB_ID )
	    {
		$str .= &TagA( "$PROGRAM?b=$BOARD&c=$com&num=$num&old=" . ( $i*$num ) . "&rev=$rev", $i );
	    }
	    else
	    {
		$str .= $i;
	    }
	}
	$str .= ' ';

	if ( $old )
	{
	    $str .= &TagA( "$PROGRAM?b=$BOARD&c=$com&num=$num&old=$nextOld&rev=$rev", $H_BOTTOM );
	}
	else
	{
	    $str .= $H_BOTTOM;
	}
    }
    else
    {
	if ( $old )
	{
	    $str .= &TagA( "$PROGRAM?b=$BOARD&c=$com&num=$num&old=$nextOld&rev=$rev", $H_TOP );
	}
	else
	{
	    $str .= $H_TOP;
	}

	local( $i );
	$MAX_PAGELINK = 5;
	for ( $i = $MAX_PAGELINK; $i >= -$MAX_PAGELINK; $i-- )
	{
	    $str .= ' ';
	    if ( $old - $i * $num <= $#DB_ID )
	    {
		$str .= &TagA( "$PROGRAM?b=$BOARD&c=$com&num=$num&old=" . ( $i*$num ) . "&rev=$rev", $i );
	    }
	    else
	    {
		$str .= $i;
	    }
	}
	$str .= ' ';

	if ( $num && ( $#DB_ID - $old - $num > 0 ))
	{
	    $str .= &TagA( "$PROGRAM?b=$BOARD&c=$com&num=$num&old=$backOld&rev=$rev", $H_BOTTOM );
	}
	else
	{
	    $str .= $H_BOTTOM;
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

    local( $str );
    $str = '<p>';

    if ( $vRev )
    {
	if ( $num && ( $#DB_ID - $old - $num > 0 ))
	{
	    $str .= &TagA( "$PROGRAM?b=$BOARD&c=$com&num=$num&old=$backOld&rev=$rev", "$H_TOP$H_BACKART" );
	}
	else
	{
	    $str .= $H_NOBACKART;
	}
    }
    else
    {
	if ( $old )
	{
	    $str .= &TagA( "$PROGRAM?b=$BOARD&c=$com&num=$num&old=$nextOld&rev=$rev", "$H_TOP$H_NEXTART" );
	}
	else
	{
	    $str .= $H_NONEXTART;
	}
    }

    if ( $SYS_REVERSE )
    {
	$str .= ' // ' . &TagA( "$PROGRAM?b=$BOARD&c=$com&num=$num&old=$old&rev=" . ( 1-$rev ), $H_REVERSE );
    }

    $str .= "</p>\n";

    &cgiprint'Cache( $str );
}

sub ShowPageLinkBottom		# not used.
{
    local( $com, $num, $old, $rev, $vRev ) = @_;

    local( $nextOld ) = ( $old > $num )? ( $old - $num ) : 0;
    local( $backOld ) = ( $old + $num );

    local( $str );
    $str = '<p>';

    if ( $SYS_REVERSE )
    {
	$str .= &TagA( "$PROGRAM?b=$BOARD&c=$com&num=$num&old=$old&rev=" . ( 1-$rev ), $H_REVERSE ) . ' // ';
    }

    if ( $vRev )
    {
	if ( $old )
	{
	    $str .= &TagA( "$PROGRAM?b=$BOARD&c=$com&num=$num&old=$nextOld&rev=$rev", "$H_NEXTART$H_BOTTOM" );
	}
	else
	{
	    $str .= $H_NONEXTART;
	}
    }
    else
    {
	if ( $num && ( $#DB_ID - $old - $num > 0 ))
	{
	    $str .= &TagA( "$PROGRAM?b=$BOARD&c=$com&num=$num&old=$backOld&rev=$rev", "$H_BACKART$H_BOTTOM" );
	}
	else
	{
	    $str .= $H_NOBACKART;
	}
    }

    $str .= "</p>\n";

    &cgiprint'Cache( $str );
}



###
## ShowLinksToFollowedArticle - 元記事情報の表示
#
# - SYNOPSIS
#	ShowLinksToFollowedArticle( *msg, @IdList );
#
# - ARGS
#	$msg		生成文字列
#	@IdList		リプライ記事IDのリスト(古いリプライほど末尾にくる)
#
# - DESCRIPTION
#	元記事情報を生成する．
#
# - RETURN
#	なし
#
sub ShowLinksToFollowedArticle
{
    local( *msg, @IdList ) = @_;

    local( $Id, $Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name );

    # オリジナル記事
    if ( $#IdList > 0 )
    {
	$Id = $IdList[$#IdList];
	( $Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name ) = &GetArticlesInfo( $Id );
	$msg .= "<br>\n<strong>$H_ORIG_TOP:</strong> " .
	    &GetFormattedTitle( $Id, $Aids, $Icon, $Subject, $Name, $Date, 0 );
    }

    # 元記事
    $Id = $IdList[0];
    ( $Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name ) = &GetArticlesInfo( $Id );
    $msg .= "<br>\n<strong>$H_ORIG:</strong> " .
	&GetFormattedTitle( $Id, $Aids, $Icon, $Subject, $Name, $Date, 0 );
}


###
## PrintButtonToTitleList - タイトル一覧へ戻るボタンの表示
#
# - SYNOPSIS
#	PrintButtonToTitleList($Board);
#
# - ARGS
#	$Board		掲示板ID
#
# - DESCRIPTION
#	タイトル一覧に戻るためのボタンを表示する
#
# - RETURN
#	なし
#
sub PrintButtonToTitleList
{
    local( $board, $id ) = @_;
    local( $old ) = $id? &GetTitleOldIndex( $id ) : 0;

    if  ( $SYS_COMMAND_BUTTON )
    {
	local( %tags ) = ( 'b', $board, 'c', 'v', 'num', $DEF_TITLE_NUM, 'old',
	    $old );
	local( $str );
	&TagForm( *str, *tags, "$H_BACKTITLEREPLY", '', '' );
	&cgiprint'Cache( $str );

	if ( $SYS_F_R )
	{
	    %tags = ( 'b', $board, 'c', 'r', 'num', $DEF_TITLE_NUM, 'old',
		$old );
	    &TagForm( *str, *tags, "$H_BACKTITLEDATE", '', '' );
	    &cgiprint'Cache( $str );
	}
    }
    else
    {
	&cgiprint'Cache( "<p>", &TagA( "$PROGRAM?b=$board&c=v&num=$DEF_TITLE_NUM&old=$old", $H_BACKTITLEREPLY ), "</p>\n" );
	&cgiprint'Cache( "<p>", &TagA( "$PROGRAM?b=$board&c=r&num=$DEF_TITLE_NUM&old=$old", $H_BACKTITLEDATE ), "</p>\n" ) if ( $SYS_F_R );
    }
}


###
## PrintButtonToBoardList - 掲示板一覧へ戻るボタンの表示
#
# - SYNOPSIS
#	PrintButtonToBoardList;
#
# - ARGS
#	なし
#
# - DESCRIPTION
#	掲示板一覧に戻るためのボタンを表示する
#
# - RETURN
#	なし
#
sub PrintButtonToBoardList
{
    if ( $SYS_COMMAND_BUTTON && $BOARDLIST_URL =~ /$PROGRAM/ )
    {
	local( %tags ) = ( 'c', 'bl' );
	local( $str );
	&TagForm( *str, *tags, $H_BACKBOARD, '', '' );
	&cgiprint'Cache( $str );
    }
    else
    {
	&cgiprint'Cache( "<p>", &TagA( $BOARDLIST_URL, $H_BACKBOARD ), "</p>\n" );
    }
}


###
## MsgHeader - HTML文書のヘッダ部分の表示
#
# - SYNOPSIS
#	MsgHeader($Title, $Message, $LastModified);
#
# - ARGS
#	$Title		HTML文書のTITLE(titleタグに入れるので，今のところ，
#			US-ASCIIのみしておいたほうが無難)
#	$Message	HTML文書のタイトル(本文内に表示する文字列)
#	$LastModified	最終更新時間
#
# - DESCRIPTION
#	HTML文書のヘッダ部分を表示する．
#
# - RETURN
#	なし
#
sub MsgHeader
{
    local( $Title, $Message, $LastModified ) = @_;
    
    if (( $SYS_ALIAS == 3 ) && ( $cgi'TAGS{'cookies'} eq 'on' ))
    {
	local( @cookieStr ) = ( "kb10info=" . join( $COLSEP, $cgi'TAGS{'name'},
	    $cgi'TAGS{'mail'}, $cgi'TAGS{'url'} ));
	local( $cookieExpire );
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
	&cgi'Header( 0, 0, 1, *cookieStr, $cookieExpire );
    }
    else
    {
	# Last-Modifiedは空．Cookiesも空．
	&cgi'Header( 0, 0, 0, 0, 0 );
    }

    local( $titleString ) = $BOARDNAME? "$SYSTEM_NAME - $BOARDNAME - $Title" :
	"$SYSTEM_NAME - $Title";
    local( $headerString ) = $BOARDNAME || $SYSTEM_NAME;

    local( $msg );
    $msg .= <<__EOF__;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN">
<html lang="ja">
<head>
<link rev="MADE" href="mailto:$MAINT">
<title>$titleString</title>
</head>
__EOF__

    $msg .= '<body';
    if ( $SYS_NETSCAPE_EXTENSION )
    {
	$msg .= " background=\"$BG_IMG\"" if $BG_IMG;
	$msg .= " bgcolor=\"$BG_COLOR\"" if $BG_COLOR;
	$msg .= " TEXT=\"$TEXT_COLOR\"" if $TEXT_COLOR;
	$msg .= " LINK=\"$LINK_COLOR\"" if $LINK_COLOR;
	$msg .= " ALINK=\"$ALINK_COLOR\"" if $ALINK_COLOR;
	$msg .= " VLINK=\"$VLINK_COLOR\"" if $VLINK_COLOR;
    }
    $msg .= ">\n";

    $msg .= <<__EOF__;
<h1>$headerString</h1>

<p>[
__EOF__

    $msg .= "$Message // \n";
    $msg .= "最新${H_MESG}ID: " . $DB_ID[$#DB_ID] . " // \n" if @DB_ID;
    $msg .= "時刻: " . &GetDateTimeFormatFromUtc( $^T );
    $msg .= <<__EOF__;
]</p>

__EOF__

    if ( $SYS_HEADER_MENU && ( $SYS_F_B || $BOARD ))
    {
	local( $select );
	$select .= "表示画面: \n<select name=\"c\">\n";
	$select .= sprintf( "<option %s value=\"bl\">$H_BOARD一覧\n", ( $cgi'TAGS{'c'} eq 'bl' )? 'selected' : '' ) if $SYS_F_B;
	if ( $BOARD )
	{
	    $select .= sprintf( "<option %s value=\"v\">最新$H_SUBJECT一覧($H_REPLY順)\n", ( $cgi'TAGS{'c'} eq 'v' )? 'selected' : '' );
	    $select .= sprintf( "<option %s value=\"r\">最新$H_SUBJECT一覧(日付順)\n", ( $cgi'TAGS{'c'} eq 'r' )? 'selected' : '' ) if $SYS_F_R;
	    $select .= sprintf( "<option %s value=\"vt\">最新$H_MESG一覧($H_REPLY順)\n", ( $cgi'TAGS{'c'} eq 'vt' )? 'selected' : '' );
	    $select .= sprintf( "<option %s value=\"l\">最新$H_MESG一覧(日付順)\n", ( $cgi'TAGS{'c'} eq 'l' )? 'selected' : '' ) if $SYS_F_L;
	    $select .= sprintf( "<option %s value=\"s\">$H_MESGの検索\n", ( $cgi'TAGS{'c'} eq 's' )? 'selected' : '' ) if $SYS_F_S;
	    $select .= sprintf( "<option %s value=\"n\">新規書き込み\n", ( $cgi'TAGS{'c'} eq 'n' )? 'selected' : '' ) if $SYS_F_N;
	    $select .= sprintf( "<option %s value=\"i\">使える$H_ICON一覧\n", ( $cgi'TAGS{'c'} eq 'i' )? 'selected' : '' ) if $SYS_ICON;
	}
	$select .= "</select>\n // 表示件数: <input name=\"num\" type=\"text\" size=\"3\" value=\"" . ( $cgi'TAGS{'num'} || $DEF_TITLE_NUM ) . "\"> ";
	local( %tags ) = ( 'b', $BOARD );
	local( $str );
	&TagForm( *str, *tags, "表示", 0, *select );
	$msg .= $str;
    }

    $msg .= "$H_HR\n";

    &cgiprint'Init;
    &cgiprint'Cache( $msg );
}


###
## MsgFooter - HTML文書のフッタ部分の表示
#
# - SYNOPSIS
#	MsgFooter;
#
# - ARGS
#	なし
#
# - DESCRIPTION
#	HTML文書のフッタ部分を表示する．
#
# - RETURN
#	なし
#
sub MsgFooter
{
    # ↓この部分を変更するのも「自由」です．消しても全く問題ありません．
    local( $addr ) = "Maintenance: " . &TagA( "mailto:$MAINT", $MAINT_NAME ) . "<br>" . &TagA( "http://www.jin.gr.jp/~nahi/kb/", $PROGNAME ) . ": Copyright (C) 1995-2000 " . &TagA( "http://www.jin.gr.jp/~nahi/", "NAKAMURA Hiroshi" ) . ".";
    # ただし「俺が作ったんだ」とか書くと，なひの権利を侵害して，
    # GPL2に違反することになっちゃうので気をつけてね．(^_^;

    &cgiprint'Cache(<<__EOF__);
$H_HR
<address>
$addr
</address>
</body>
</html>
__EOF__

    &cgiprint'Flush();
}


###
## GetFormattedTitle - タイトルリストのフォーマット
#
# - SYNOPSIS
#	GetFormattedTitle( $id, $aids, $icon, $title, $name, $origDate, $flag);
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
#	$G_TITLE_STRを破壊する．何度も使われるので，localを減らすため．．．
#	かなりパフォーマンスに効く．
#
# - RETURN
#	フォーマットした文字列
#
sub GetFormattedTitle
{
    local( $id, $aids, $icon, $title, $name, $origDate,	$flag ) = @_;

    $G_TITLE_STR = '';	# 初期化

    if ( $SYS_F_T && $flag&1 && $DB_FID{$id} )
    {
	local( $fId ) = $DB_FID{$id};
	$fId =~ s/^.*,//o;
	$G_TITLE_STR .= &TagA( "$PROGRAM?b=$BOARD&c=t&id=$fId",
	    $H_THREAD_ALL ) . ' ';
    }

    $G_TITLE_STR .= &TagMsgImg( $icon ) . " <small>$id.</small> " .
	&TagA( ( $flag&2 )? "$cgi'REQUEST_URI#a$id" :
	"$PROGRAM?b=$BOARD&c=e&id=$id",	$title || $id );

    if ( $SYS_F_T && $aids )
    {
	$G_TITLE_STR .= ' ' . &TagA( "$PROGRAM?b=$BOARD&c=t&id=$id",
	    $H_THREAD );
    }

    $G_TITLE_STR .= ' [' . ( $name || $MAINT_NAME ) . '] ' .
	&GetDateTimeFormatFromUtc( $origDate || &GetModifiedTime( $id,$BOARD));

    if ( $DB_NEW{$id} )
    {
	$G_TITLE_STR .= ' ' . &TagMsgImg( $H_NEWARTICLE );
    }

    $G_TITLE_STR;
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
#	$type		表示タイプ
#				1 ... アイコンの後ろに文字列を追加しない
#				2 ... アイコンの後ろに文字列を追加しない
#				0/others ... アイコンなしでテキストだけ
#
# - DESCRIPTION
#	イメージを表示用タグにフォーマットする．
#
# - RETURN
#	フォーマットした文字列
#
sub TagComImg
{
    local( $src, $alt, $type ) = @_;
    if ( $type == 1 )
    {
	"<img src=\"$src\" alt=\"$alt\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\">";
    }
    elsif ( $type == 2 )
    {
	"<img src=\"$src\" alt=\"$alt\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\">$alt";
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
# - RETURN
#	フォーマットした文字列
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
	return "<img src=\"$src\" alt=\"[$icon]\" width=\"$MSGICON_WIDTH\" height=\"$MSGICON_HEIGHT\" BORDER=\"0\">";
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
#	TagA( $href, $markUp );
#
# - ARGS
#	$href		リンク先URL
#	$markUp		マークアップ文字列
#
# - DESCRIPTION
#	リンクをリンクタグにフォーマットする．
#
# - RETURN
#	フォーマットした文字列
#
sub TagA
{
    local( $href, $markUp ) = @_;
    $href =~ s/&/&amp;/go;
    "<a href=\"$href\">$markUp</a>";
}


###
## TagForm - フォームタグのフォーマット
#
# - SYNOPSIS
#	TagForm( *str, *hiddenTags, $submit, $reset, *contents );
#
# - ARGS
#	*str		生成文字列の格納先
#	*tags		追加するhiddenタグを収めた連想配列
#	*submit		submitボタン文字列
#	*reset		resetボタン文字列
#	*contents	</form>の前までに挿入する文字列
#
# - DESCRIPTION
#	Formタグのフォーマット
#
sub TagForm
{
    local( *str, *tags, $submit, $reset, *contents ) = @_;

    $str = "<form action=\"$PROGRAM\" method=\"POST\">\n<p>\n";
    foreach ( keys( %tags ))
    {
	$str .= "<input name=\"$_\" type=\"hidden\" value=\"$tags{$_}\">\n";
    }
    $str .= $contents;
    $str .= "<input type=\"submit\" value=\"$submit\">\n";
    $str .= "<input type=\"reset\" value=\"$reset\">\n" if $reset;
    $str .= "</p>\n</form>\n";
}


###
## SendMail - メイル送信
#
# - SYNOPSIS
#	SendMail(
#	    $Name,	メイル送信者名
#	    $EMail,	メイル送信者メイルアドレス
#	    $Subject,	メイルのSubject文字列
#	    $Message,	本文
#	    $Id,	引用するなら記事ID; 空なら引用ナシ
#	    @To		宛先E-Mail addr.のリスト
#	)
#
# - DESCRIPTION
#	メイルを送信する．
#
# - RETURN
#	なし
#
sub SendMail
{
    local( $Name, $EMail, $Subject, $Message, $Id, @To ) = @_;

    local( $ExtensionHeader, @ArticleBody );

    $ExtensionHeader = "X-MLServer: $PROGNAME\n";
    $ExtensionHeader .= "X-Kb-System: $SYSTEM_NAME\n";
    if (( ! $SYS_MAILHEADBRACKET ) && $BOARDNAME && ($Id ne '' ))
    {
	$ExtensionHeader .= "X-Kb-Board: $BOARDNAME\nX-Kb-Articleid: $Id\n";
    }

    if ( $EMail eq '' )
    {
	# メイルアドレス未入力につき，管理者名義で出す．
	$Name = ( $MAILFROM_LABEL || $MAINT_NAME );
	$EMail = $MAINT;
    }

    local( $SenderFrom, $SenderAddr ) = (( $MAILFROM_LABEL || $MAINT_NAME ),
	$MAINT );
    local( $stat, $errstr ) = &cgi'sendMail( $Name, $EMail, $SenderFrom,
	$SenderAddr, $Subject, $ExtensionHeader, $Message, $MAILTO_LABEL,
	@To );
    &Fatal( 9, "$BOARDNAME/$Id/$errstr" ) if ( !$stat );
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
## KbLog - log a log
#
# - SYNOPSIS
#	&KbLog( $kinologue'severity, *msg );
#
# - ARGS
#	$kinologue'severity	severity id defined in kinologue.pl.
#	*msg			reference to msg string.
#
# - DESCRIPTION
#	log a log using kinologue.
#	exit program(not function) if failed to write log.
#
# - RETURN
#	returns nothing.
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


######################################################################
# ロジックインプリメンテーション


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
# - RETURN
#	なし
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
# - RETURN
#	なし
#
sub CheckArticle
{
    local( $board, *name, *eMail, *url, *subject, *icon, *article ) = @_;

    local( $Tmp );

    if ( $name =~ /^\#.*$/o )
    {
        ( $Tmp, $eMail, $url ) = &GetUserInfo( $name );
	&Fatal( 6, $name ) if ( $Tmp eq '' );
	$name = $Tmp;
    }
    elsif ( $SYS_ALIAS == 2 )
    {
	# 必須のはずなのに，指定されたエイリアスが登録されていない
	&Fatal( 6, $name );
    }

    &CheckName( *name );
    &CheckEmail( *eMail );
    &CheckURL( *url );
    &CheckSubject( *subject );
    &CheckIcon( *icon, $board ) if $SYS_ICON;

    # 本文の空チェック．
    &Fatal( 2, '' ) if ( $article eq '' );

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
# それでもどーーしても使いたいというあなたは，
# ↓の行の先頭の「#」を消してください．(^_^;
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
	# <URL:>の処理
	$article = &ArticleEncode( $article );
	$article =~ s/<URL:([^>][^>]*)>/&lt;URL:$1&gt;/gi;
    }
    elsif ( $textType eq $H_TTLABEL[1] )
    {
	# convert to html
	&PlainArticleToHtml( *article );
	# <URL:>の処理
	$article = &ArticleEncode( $article );
	# secrurity check
	&cgi'SecureHtmlEx( *article, *aNeedVec, *aFeatureVec );
    }
    elsif ( $textType eq $H_TTLABEL[2] )
    {
	# <URL:>の処理
	$article = &ArticleEncode( $article );
	# secrurity check
	&cgi'SecureHtmlEx( *article, *aNeedVec, *aFeatureVec );
    }
    else
    {
	&Fatal( 0, 'must not be reached...' );
    }
}


###
## AliasCheck - ユーザエイリアスのチェック
#
# - SYNOPSIS
#	AliasCheck($A, $N, $E, $U);
#
# - ARGS
#	$A	エイリアス名
#	$N	名前
#	$E	E-Mail addr.
#	$U	URL
#
# - DESCRIPTION
#	ユーザエイリアスのデータ(エイリアス名，名前，E-Mail，URL)
#	をチェックする．
#
# - RETURN
#	なし
#
sub AliasCheck
{
    local( $A, $N, $E, $U ) = @_;
    &CheckAlias( *A );
    &CheckName( *N );
    &CheckEmail( *E );
    &CheckURL( *U );
}


###
## CheckAlias - 文字列チェック: エイリアス
#
# - SYNOPSIS
#	CheckAlias(*String);
#
# - ARGS
#	*String		エイリアス文字列
#
# - DESCRIPTION
#	エイリアスの文字列チェックを行なう．
#	不正な文字列だったらエラー表示ルーチンへ．
#	(アプリケーション/UIを分離したほうがいいかな?)
#
# - RETURN
#	なし
#
sub CheckAlias
{
    local( *String ) = @_;

    &Fatal( 2, '' ) if ( !$String );
    &Fatal( 7, $H_ALIAS ) if ( $String !~ ( /^\#/ ));

    # 1文字じゃだめ
    &Fatal( 7, $H_ALIAS ) if ( length( $String ) < 2 );

    &Fatal( 3, '' ) if ( $String =~ m/[\t\n]/o );
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
# - RETURN
#	なし
#
sub CheckSubject
{
    local( *String ) = @_;

    &Fatal( 2, '' ) unless $String;
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

    &Fatal( 2, '' ) if ( !$SYS_ALLOWNOICON && ( $str eq $H_NOICON ));
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
# - RETURN
#	なし
#
sub CheckName
{
    local( *String ) = @_;

    &Fatal( 2, '' ) if ( !$String );
    &Fatal( 3, '' ) if ( $String =~ m/[\t\n]/o );
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
# - RETURN
#	なし
#
sub CheckEmail
{
    local( *String ) = @_;

    if ( $SYS_POSTERMAIL ) {
	&Fatal( 2, '' ) if ( !$String );
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
# - RETURN
#	なし
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
# - RETURN
#	なし
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
# - RETURN
#	なし
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
###
## ArticleEncode - 記事のEncode
#
# - SYNOPSIS
#	ArticleEncode($Article);
#
# - ARGS
#	$Article	Encodeする記事本文
#
# - DESCRIPTION
#	記事中のURL(<URL:〜>)を，リンクに変換する．
#
# - RETURN
#	Encodeされた文字列
#
sub ArticleEncode
{
    local( $article ) = @_;

    local( $retArticle ) = $article;

    local( $url, $urlMatch, @cache );
    local( $tagStr, $quoteStr );
    while ( $article =~ m/<URL:([^>][^>]*)>/gi )
    {
	$url = $1;
	( $urlMatch = $url ) =~ s/([?+*^\\\[\]\|()])/\\$1/go;
	next if ( grep( /^$urlMatch$/, @cache ));
	push( @cache, $url );
	$quoteStr = "<URL:$url>";

	if ( $urlMatch =~ m/^kb:(.*)$/ )
	{
	    local( $artStr ) = $1;
	    if ( $artStr =~ m!^//.*$! )
	    {
		# not implemented now...
	    }
	    elsif ( $artStr =~ m!^([^/][^/]*)/(.*)$! )
	    {
		local( $boardInfo ) = &GetBoardInfo( $1 );
		$tagStr = &TagA( "$PROGRAM?b=$1&c=e&id=$2", $quoteStr )
		    if $boardInfo;
	    }
	    else
	    {
		$tagStr = &TagA( "$PROGRAM?b=$BOARD&c=e&id=$artStr",
		    $quoteStr );
	    }
	}
	elsif ( &IsUrl( $urlMatch ))
	{
	    $tagStr = &TagA( $url, $quoteStr );
	}
	else
	{
	    next;
	}

	$retArticle =~ s/<URL:$urlMatch>/$tagStr/gi;
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
# - RETURN
#	なし
#
sub PlainArticleToPreFormatted
{
    local( *Article ) = @_;
    $Article =~ s/\n*$//o;
    $Article =~ s/<URL:([^>][^>]*)>/__URL__$COLSEP$1$COLSEP/gi;
    $Article = &HTMLEncode( $Article );	# no tags are allowed.
    $Article =~ s/__URL__$COLSEP([^$COLSEP][^$COLSEP]*)$COLSEP/"<URL:" . &HTMLDecode( $1 ) . ">"/gie;
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
# - RETURN
#	なし
#
sub PlainArticleToHtml
{
    local( *Article ) = @_;
    $Article =~ s/^\n*//o;
    $Article =~ s/\n*$//o;
    $Article =~ s/\n/<br>\n/go;
    $Article =~ s/<br>\n<br>\n(<br>\n)*/<\/p>\n\n<p>/go;
    $Article = "<p>$Article</p>";
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
# - RETURN
#	なし
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
# - ARGS
#	なし
#
# - DESCRIPTION
#	記事を訂正する．
#
# - RETURN
#	なし
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
# - RETURN
#	なし
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
# - RETURN
#	なし
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
#	LockAll;
#	UnlockAll;
#	LockBoard;
#	UnlockBoard;
#
# - ARGS
#	なし
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


######################################################################
# データインプリメンテーション


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
# - RETURN
#	なし
#
$BOARD_DB_CACHE = 0;

sub DbCache
{
    return if $BOARD_DB_CACHE;

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

    $BOARD_DB_CACHE = 1;		# cached
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
# - RETURN
#	なし
#
sub AddDBFile
{
    local( $Id, $Board, $Fid, $InputDate, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail, $MailRelay ) = @_;

    local( $dId, $dFid, $dAids, $dInputDate, $dSubject, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail, $mdName, $mdEmail, $mdInputDate, $mdSubject, $mdIcon, $mdId, $FidList, $FFid, @FollowMailTo, @FFid );

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
# - RETURN
#	なし
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
# - RETURN
#	なし
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
# - RETURN
#	なし
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
# - RETURN
#	なし
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
# - RETURN
#	なし
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
# - RETURN
#	なし
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
# - RETURN
#	なし
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
# - RETURN
#	なし
#
sub UpdateArriveMailDb
{
    local( $Board, *ArriveMail ) = @_;

    local( $File ) = &GetPath( $Board, $ARRIVEMAIL_FILE_NAME );
    local( $TmpFile ) = &GetPath( $Board, $ARRIVEMAIL_FILE_NAME );
    open( DBTMP, ">$TmpFile" ) || &Fatal( 1, $TmpFile );
    foreach ( @ArriveMail )
    {
	print( DBTMP "$_\n" ) || &Fatal( 13, $TmpFile );
    }
    close DBTMP || &Fatal( 13, $TmpFile );
    rename( $TmpFile, $File ) || &Fatal( 14, "$TmpFile -&gt; $File" );
}


###
## CacheAliasData - ユーザDBの全読み込み
#
# - SYNOPSIS
#	CacheAliasData;
#
# - ARGS
#	なし
#
# - DESCRIPTION
#	ユーザエイリアスファイルを読み込んで連想配列に放り込む．
#	大域変数，%Name, %Email, %Host, %URLを破壊する．
#
# - RETURN
#	なし
#
sub CacheAliasData
{
    local( $A, $N, $E, $H, $U );

    # 放り込む．
    open( ALIAS, "<$USER_ALIAS_FILE" ) || &Fatal( 1, $USER_ALIAS_FILE );
    while ( <ALIAS> )
    {
	next if ( /^$/o || /^[^#]/ );
	chop;

	( $A, $N, $E, $H, $U ) = split( /\t/, $_ );

	$Name{$A} = $N;
	$Email{$A} = $E;
	$Host{$A} = $H;
	$URL{$A} = $U;
    }
    close ALIAS;
}


###
## GetUserInfo - ユーザDBの読み込み
#
# - SYNOPSIS
#	GetUserInfo($Alias);
#
# - ARGS
#	$Alias		検索するユーザID(エイリアス)
#
# - DESCRIPTION
#	ユーザDBから，ユーザの名前，メイル，URLを取ってくる．
#
# - RETURN
#	ユーザの名前，メイル，URLの順のリスト．
#
sub GetUserInfo
{
    local( $Alias ) = @_;

    local( $A, $N, $E, $H, $U, $rN, $rE, $rU );
    open( ALIAS, "<$USER_ALIAS_FILE" ) || &Fatal( 1, $USER_ALIAS_FILE );
    while ( <ALIAS> )
    {
	next if (/^$/o);
	chop;
	
	# 分割
	( $A, $N, $E, $H, $U ) = split( /\t/, $_ );
	
	# マッチしなきゃ次へ．
	next if ( $A ne $Alias );
	
	$rN = $N;
	$rE = $E;
	$rU = $U;
    }
    close ALIAS;

    ( $rN, $rE, $rU );
}


###
## WriteAliasData - ユーザDBの更新/追加
#
# - SYNOPSIS
#	WriteAliasData;
#
# - ARGS
#	なし
#
# - DESCRIPTION
#	ユーザエイリアスファイルにデータを書き出す．
#	%Name, %Email, %Host, %URLを必要とする．
#	$Nameが空だと書き込まない．
#
# - RETURN
#	なし
#
sub WriteAliasData
{
    local( $TmpFile ) = "$USER_ALIAS_FILE.$TMPFILE_SUFFIX$$";

    open( ALIAS, ">$TmpFile" ) || &Fatal( 1, $TmpFile );
    printf( ALIAS "<!-- Kb-System-Id: %s/%s -->\n", $KB_VERSION, $KB_RELEASE )
	|| &Fatal( 13, $TmpFile );

    local( $Alias, $dbLine );
    foreach $Alias ( sort keys( %Name ))
    {
	if ( $Name{$Alias} )
	{
	    &GenTSV( *dbLine, ( $Alias, $Name{$Alias}, $Email{$Alias}, $Host{$Alias}, $URL{$Alias} ));
	    print( ALIAS "$dbLine\n" ) || &Fatal( 13, $TmpFile );
	}
    }
    close ALIAS || &Fatal( 13, $TmpFile );

    rename( $TmpFile, $USER_ALIAS_FILE )
	|| &Fatal( 14, "$TmpFile -&gt; $USER_ALIAS_FILE" );
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
# - RETURN
#	なし
#
sub GetAllBoardInfo
{
    local( *board, *boardName, *boardInfo ) = @_;

    local( $bId, $bName, $bInfo );
    open( ALIAS, "<$BOARD_ALIAS_FILE" ) || &Fatal( 1, $BOARD_ALIAS_FILE );
    while ( <ALIAS> )
    {
	next if ( /^\#/o || /^$/o );
	chop;
	( $bId, $bName, $bInfo ) = split( /\t/, $_, 3 );
	push( @board, $bId );
	$boardName{ $bId } = $bName;
	$boardInfo{ $bId } = $bInfo;
    }
    close ALIAS;
}


###
## GetBoardInfo - 掲示板DBの読み込み
#
# - SYNOPSIS
#	GetBoardInfo($Alias);
#
# - ARGS
#	$Alias		掲示板ID
#
# - DESCRIPTION
#	掲示板DBから，掲示板情報を取ってくる．
#
# - RETURN
#	掲示板名
#
sub GetBoardInfo
{
    local( $alias ) = @_;

    local( $dAlias, $dBoardName, $dBoardConf );

    open( ALIAS, "<$BOARD_ALIAS_FILE" ) || &Fatal( 1, $BOARD_ALIAS_FILE );
    while ( <ALIAS> )
    {
	next if ( /^\#/o || /^$/o );
	chop;
	( $dAlias, $dBoardName, $dBoardConf ) = split( /\t/, $_, 4 );
	if ( $alias eq $dAlias )
	{
	    close ALIAS;
	    return( $dBoardName, $dBoardConf );
	}
    }
    close ALIAS;

    &Fatal( 11, $alias );
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
# - RETURN
#	なし
#
$ICON_DB_CACHE = '';

sub CacheIconDb
{
    local( $board ) = @_;
    return if ( $ICON_DB_CACHE eq $board );

    local( $FileName, $IconTitle, $IconHelp );

    @ICON_TITLE = %ICON_FILE = %ICON_HELP = ();
    open( ICON, &GetIconPath( "$board.$ICONDEF_POSTFIX" ))
	|| ( open( ICON, &GetIconPath( "$DEFAULT_ICONDEF" ))
	    || &Fatal( 1, &GetIconPath( "$DEFAULT_ICONDEF" )));
    while ( <ICON> )
    {
	next if ( /^\#/o || /^$/o );
	chop;
	( $FileName, $IconTitle, $IconHelp ) = split( /\t/, $_, 3 );

	push( @ICON_TITLE, $IconTitle );
	$ICON_FILE{$IconTitle} = $FileName;
	$ICON_HELP{$IconTitle} = $IconHelp;
    }
    close ICON;

    $ICON_DB_CACHE = $board;		# cached
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
# - RETURN
#	なし
#
sub GetBoardHeader
{
    local( $Board, *BoardHeader ) = @_;

    local( $File ) = &GetPath( $Board, $BOARD_FILE_NAME );
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
    $KB_RESOURCE_URL? "$KB_RESOURCE_URL$ICON_DIR/$file" : "$ICON_DIR/$file";
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
    &CacheIconDb( $board ) if ( $ICON_DB_CACHE ne $board );

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
