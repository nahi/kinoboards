# $Id: cgi.pl,v 1.22 1997-11-26 12:05:41 nakahiro Rel $


# Small CGI tool package(use this with jcode.pl-2.0).
# Copyright (C) 1995, 96, 97 NAKAMURA Hiroshi.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or any
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


# CAUTION
#
#	歌代さんによる日本語漢字コード変換ユーティリティ，jcode.plの
#	v2.0以降が必要です．以下のURLから入手してください．
#	<URL:ftp://ftp.sra.co.jp/pub/lang/perl/sra-scripts/>
#
#
#
# INTERFACE
#
#
# $cgi'SERVER_NAME;
#	CGIが稼働しているWWWサーバのFQDN
#	（ただし最後の「.」は無し; 以下同様）が設定されます．
#	ex. → www.foo.bar.jp
#
# $cgi'SERVER_PORT;
#	WWWサーバで稼働しているhttpdの占有ポート番号が設定されます．
#	ex. → 80
#
# $cgi'REMOTE_HOST;
#	CGIを起動したWWWクライアント（ブラウザ）のFQDN，
#	もしくはIPアドレス（WWWサーバの設定次第）が設定されます．
#	ex. → ika.tako.jp
#
# $cgi'SCRIPT_NAME;
#	起動されたCGIのサイト中相対URLが設定されます．
#	ex. → /cgi-bin/foo/bar.cgi
#
# $cgi'CGIPROG_NAME;
#	起動されたCGIのファイル名（パス名を除く）が設定されます．
#	ex. → bar.cgi
#
# $cgi'SYSDIR_NAME;
#	起動したCGIのパス名（ファイル名を除く）が設定されます．
#	ex. → /cgi-bin/foo/
#
# $cgi'PATH_INFO;
#	CGIに付加されたパス情報が設定されます．
#	ex. /foo.cgi/bar/baz → '/bar/baz'
#
# $cgi'PATH_TRANSLATED;
#	CGIに付加されたパス情報を，
#	実際のマシン上のパスに変換した文字列が設定されます．
#	ex. /foo.cgi/~foo → '/usr/local/etc/httpd/htdocs/foo'
#
# $cgi'PROGRAM;
#	CGI中，actionで呼び出すべきプログラム名が設定されます．
#	ex. → /cgi-bin/foo.cgi
#	ex. → foo.cgi
#
# &cgi'lock( $file );
#	$fileで指定されたファイル名を使い，perl programを排他ロックします．
#	$mail'ARCHの値に応じ，用いるロック手法が異なります．
#		UNIX	シンボリックリンクによるロック
#		WinNT	flockによるロック
#		Win95	flockによるロック
#		Mac	ロックの必要がないので（ほんと?）なにもしません
#	メンテナンスロック中なら
#	（実行ユーザで削除できないロックファイルが既に存在するなら），
#	2を，通常のロックが無事行えれば1を，
#	なんらかの理由で行えなければ0を返します．
#
# &cgi'unlock( $file );
#	$fileで指定されたファイル名を使ってかけられた排他ロックを外します．
#	返り値はありません．
#
# &cgi'Header( $utcFlag, $utcStr, $cookieFlag, $cookieStr );
#	標準出力に対し，CGIプログラムが送信すべきHTTPヘッダを出力します．
#	$utcFlagが0以外の場合，$utcStrで指定されたUTC時間が，
#	プログラムの最終更新時間になります．$utcStrが空の場合は現在時です．
#	$cookieFlagが0以外の場合，$cookieStrで指定された文字列が，
#	HTTP Cookiesとして相手ブラウザに送られます．
#	返り値はありません．
#
# &cgi'GetHttpDateTimeFromUtc( $utc );
#	$utcで指定されたUTC時間から，HTTP Date/Timeフォーマットの時間文字列を
#	作り出します．返り値はその文字列です．
#
# &cgi'Decode;
#	ブラウザからCGIプログラムに送信されたフォームの入力内容，
#	あるいはURLのサーチパート(「〜.cgi?foo=bar」の，「?」以降の部分)を
#	解析し，%cgi'TAGSに格納します．
#	例えば'name'というフォームへの入力内容は$cgi'TAGS{'name'}で，
#	「〜.cgi?foo=bar」というURLのfooの値は$cgi'TAGS{'foo'}で，
#	参照することができます．
#	%cgi'TAGSを破壊します．返り値はありません．
#
# &cgi'Cookie;
#	ブラウザからCGIプログラムに送信されたHTTP Cookiesを解析し，
#	%cgi'COOKIESに格納します．
#	例えばHTTP Cookiesが'foo=bar'という文字列であれば，
#	$cgi'COOKIES{'foo'}に'bar'が格納されます．
#	%cgi'COOKIESを破壊します．返り値はありません．
#
# &cgi'SendMail( $fromName, $fromEmail, $subject, $extension, $message, @to );
#	メイルを送信します．
#		$fromName: 送り主の名前(日本語を入れないでください)
#		$fromEmail: 送り主のE-Mail addr.
#		$subject: メイルのsubject文字列(日本語を入れないでください)
#		$extension: メイルのextension header文字列
#		$message: 本文である文字列
#		@to: 宛先のE-Mail addr.のリスト
#	$ARCHの値に応じ，用いるメイル送信手法が異なります．
#		UNIX	$MAIL2で指定したsendmailコマンド
#			(例えば'/usr/lib/sendmail -oi -t')を使って送信します．
#		WinNT	UNIX以外ではメイル送信はできません．$MAIL2で
#		Win95	指定したファイルに書き出します．
#		Mac	perl5専用のcgi.pl.libnetを使い，
#			MacPerl5とlibnet for Macの組み合わせで，
#			メイル送信を行います．$SERVER_NAMEにCGIを起動した
#			ホスト名を，$MAIL2にメイルサーバのホスト名を
#			指定してください．
#	送信が無事行えれば1を，なんらかの理由で行えなければ0を返します．
#
# &cgi'SecureHtml( *string );
#	*stringで指定された文字列のうち，指定した安全なタグのみを残し，
#	あとはHTML encodeしてしまいます．
#	使用を許可するタグおよびフィーチャは，@cgi'HTML_TAGSで指定します．
#	返り値はありません．
#
# &cgiprint'Init;
# &cgiprint'Cache( $string );
# &cgiprint'Flush;
#	CGIプログラムからブラウザに送信する文字列の日本語漢字コードを変換し，
#	標準出力に吐き出します．
#	高速化のためにキャッシュ機能を持っており，
#	Initはキャッシュのクリアを，
#	Cacheは表示文字列のキャッシュを，
#	Flushはキャッシュされている文字列の送信を行います．
#	キャッシュが適当なサイズになったら自動的にFlushされるので，
#	キャッシュした文字列の大きさを気にする必要はありません．
#	'<html><title>...</title>'のキャッシュの前に一度&cgiprint'Initして，
#	後はすべてのprintを&cgiprint'Cache($string)にし，
#	'</html>'の後で&cgiprint'Flushするとよいでしょう．
#	返り値はありません．


require('jcode.pl');


###
## cgiデータ入出力パッケージ
#
package cgi;


$ARCH = 'UNIX';
$MAIL2 = '/usr/lib/sendmail -oi -t';
$JPOUT_SCHEME = 'jis';
$WAITPID_BLOCK = 0;	# OS dependent.

$SERVER_NAME = $ENV{'SERVER_NAME'};
$SERVER_PORT = $ENV{'SERVER_PORT'};
$REMOTE_HOST = $ENV{'REMOTE_HOST'};
$SCRIPT_NAME = $ENV{'SCRIPT_NAME'};
$PATH_INFO = $ENV{'PATH_INFO'};
$PATH_TRANSLATED = $ENV{'PATH_TRANSLATED'};

($CGIPROG_NAME = $SCRIPT_NAME) =~ s!^(.*/)!!o;
$SYSDIR_NAME = (($PATH_INFO) ? "$PATH_INFO/" : "$1");
$PROGRAM = (($PATH_INFO) ? "$SCRIPT_NAME$PATH_INFO" : "$CGIPROG_NAME");


###
## ロック関係
#

# ロック
sub lock {
    local( $lockFile ) = @_;

    # locked for maintenance by admin.
    return( 2 ) if (( -e $lockFile ) && ( ! -w $lockFile ));

    return( &lock_link( $lockFile )) if ( $ARCH eq 'UNIX' );
    return( &lock_flock( $lockFile )) if ( $ARCH eq 'WinNT' || $ARCH eq 'Win95' );
    return( 1 ) if ( $ARCH eq 'Mac' );
}

# アンロック
sub unlock {
    &unlock_link( @_ ) if ( $ARCH eq 'UNIX' );
    &unlock_flock if ( $ARCH eq 'WinNT' || $ARCH eq 'Win95' );
    return if ( $ARCH eq 'Mac' );
}

# lock with symlink
sub lock_link {
    local( $lockFile ) = @_;
    local( $lockWait ) = 10;		# [sec]
    local( $lockFileTimeout ) = .004;	# 5.76 [min]
    local( $timeOut ) = 0;
    local( $lockFlag ) = 0;

    srand( time|$$ );
    if ( -M "$lockFile" > $lockFileTimeout ) { unlink( $lockFile ); }
    open( LOCKORG, ">$lockFile.org" ) || &Fatal( 1 );
    for( $timeOut = 0; $timeOut < $lockWait; $timeOut++ ) {
	$lockFlag = 1, last if ( link( "$lockFile.org", $lockFile ));
	sleep( 1 );
    }
    unlink( "$lockFile.org" );
    close( LOCKORG );
    $lockFlag;
}

sub unlock_link {
    local( $lockFile ) = @_;
    unlink( $lockFile );
}

# lock with flock.
sub lock_flock {
    local( $lockFile ) = @_;
    local( $LockEx, $LockUn ) = ( 2, 8 );
    open( LOCK, "$lockFile" ) || return( 0 );
    flock( LOCK, $LockEx );
    1;
}
sub unlock_flock {
    local( $LockEx, $LockUn ) = ( 2, 8 );
    flock( LOCK, $LockUn );
    close( LOCK );
}


###
## HTMLヘッダの生成
#
# $ENV{'SERVER_PROTOCOL'} 200 OK
# Server: $ENV{'SERVER_SOFTWARE'}
sub Header {
    local( $utcFlag, $utcStr, $cookieFlag, $cookieStr ) = @_;

    print( "Content-type: text/html\n" );

    # Header for HTTP Cookies.
    if ( $cookieFlag ) {
	printf( "Set-Cookie: $cookieStr; domain=%s; path=%s\n", $SERVER_NAME, $CGIDIR_NAME );
    }

    # Header for Last-Modified.
    if ( $utcFlag ) {
	printf( "Last-Modified: %s\n", &GetHttpDateTimeFromUtc( $utcStr || time ));
    }

    print( "\n" );

}


###
## format as HTTP Date/Time
#
sub GetHttpDateTimeFromUtc {
    local( $utc ) = @_;
    local( $sec, $min, $hour, $mday, $mon, $year, $wday ) = gmtime( $utc );

    sprintf( "%s, %02d-%s-%02d %02d:%02d:%02d GMT", ( 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday' )[ $wday ], $mday, ( 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec' )[ $mon ], $year, $hour, $min, $sec );
}


###
## CGI変数のデコード
## CAUTION! functioon decode sets global variable, TAGS.
#
sub Decode {
    local( $args, $readSize, $key, $term, $value, $encode );

    if ( $ENV{ 'REQUEST_METHOD' } eq "POST" ) {
	$readSize = read( STDIN, $args, $ENV{ 'CONTENT_LENGTH' } );
    } else {
	$args = $ENV{ 'QUERY_STRING' };
    }

    foreach $term ( split( '&', $args )) {
	( $key, $value ) = split( /=/, $term, 2 );
	$value =~ tr/+/ /;
	$value =~ s/%([0-9A-Fa-f][0-9A-Fa-f])/pack( "C", hex( $1 ))/ge;
	$encode = &jcode'getcode( *value );

	if ( $encode eq 'undef' ) {
	    $TAGS{ $key } = $value;
	} else {
	    &jcode'convert( *value, 'euc', $encode, "z" );
	    $TAGS{ $key } = $value;
	}

        if ( $ARCH eq 'Mac' ) {
            $TAGS{ $key } =~ s/\xd\xa/\n/go;
            $TAGS{ $key } =~ s/\xa/\n/go;
        } else {
	    $TAGS{ $key } =~ s/\r\n/\n/go;
	    $TAGS{ $key } =~ s/\r/\n/go;
	}
    }
}


###
## HTTP Cookiesのデコード
#
sub Cookie {
    local( $key, $value, $term );
    foreach $term ( split( ";\s*", $ENV{ 'HTTP_COOKIE' })) {
	( $key, $value ) = split( /=/, $term, 2 );
	$COOKIES{ $key } = $value;
    }
}


###
## メール送信
#
sub SendMail {

    return( &SendMailSendmail( @_ )) if ( $ARCH eq 'UNIX' );
    return( &SendMailFile( @_ )) if ( $ARCH eq 'WinNT' );
    return( &SendMailFile( @_ )) if ( $ARCH eq 'Win95' );
    return( &SendMailFile( @_ )) if ( $ARCH eq 'Mac' );

}


###
## メール送信(UNIX用)
#
# 本文以外には日本語を入れないように!
sub SendMailSendmail {
    local( $fromName, $fromEmail, $subject, $extension, $message, @to ) = @_;
    local( $pid );
    local( $toFirst ) = 1;
    local( $from ) = "$fromName <$fromEmail>";

    # 安全のため，forkする
    unless ( $pid = fork() ) {

	open( MAIL, "| $MAIL2" ) || &Fatal( 2 );

	# Toヘッダ
	foreach ( @to ) {
	    if ( $toFirst ) {
		print( MAIL "To: $_" );
		$toFirst = 0;
	    } else {
		print( MAIL ",\n\t$_" );
	    }

	}
	print( MAIL "\n" );

	# Fromヘッダ，Errors-Toヘッダ
	print( MAIL "From: $from\n" );
	print( MAIL "Errors-To: $from\n" );

	# Subjectヘッダ
	print( MAIL "Subject: $subject\n" );

	# 付加ヘッダ
	if ( $extension ) {
	    &jcode'convert( *extension, 'jis' );
	    print( MAIL $extension );
	}

	# ヘッダ終わり
	print( MAIN "\n" );

	# 本文
	&jcode'convert( *message, 'jis' );
	print( MAIL "$message\n" );

	# 送信する
	close( MAIL );
	exit( 0 );

    }
    waitpid( $pid, $WAITPID_BLOCK );

    # 送信した
    !$?;

}


###
## メール送信(Mac, Win用)
#
# 本文以外には日本語を入れないように!
sub SendMailFile {
    local( $fromName, $fromEmail, $subject, $extension, $message, @to) = @_;
    local( $toFirst ) = 1;
    local( $from ) = "$fromName <$fromEmail>";

    # メール用ファイルを開く
    &Fatal( 2 ) if ( $MAIL2 eq '' );
    open( MAIL, ">> $MAIL2" ) || &Fatal( 2 );

    # Toヘッダ
    foreach ( @to ) {
	if ( $toFirst ) {
	    print( MAIL "To: $_" );
	    $toFirst = 0;
	} else {
	    print( MAIL ",\n\t$_" );
	}
    }
    print(MAIL "\n");
    
    # Fromヘッダ，Errors-Toヘッダ
    print( MAIL "From: $from\n" );
    print( MAIL "Errors-To: $from\n" );

    # Subjectヘッダ
    print( MAIL "Subject: $subject\n" );

    # 付加ヘッダ
    if ( $extension ) {
	&jcode'convert( *extension, 'jis' );
	print( MAIL $extension );
    }

    # ヘッダ終わり
    print( MAIN "\n" );

    # 本文
    &jcode'convert( *message, 'jis' );
    print( MAIL "$message\n" );

    # 区切り線
    print( MAIL "-------------------------------------------------------------------------------\n" );

    # 送信する
    close( MAIL );

    # 送信した
    1;

}


###
## secureなタグのみを残し，その他をencodeする．
#
# known bugs:
#  タグの入れ子を考慮していない(例: <i><b>foo</i></b>)
#  Featureの中の「>」を考慮していない(例: ALT=">")
#
$F_HTML_TAGS_PARSED = 0;
%NEED = %FEATURE = ();

sub SecureHtml {
    local( *string ) = @_;
    local( $srcString ) = '';
    local( $tag, $need, $feature, $markuped );

    # HTML_TAGSの解析（一度だけ実施）
    if ( $F_HTML_TAGS_PARSED != 1 ) {
	local( @htmlTags ) =
	    (
	     # タグ名, 閉じ必須か否か, 使用可能なfeature
	     'A',		1,	'HREF/NAME',
	     'ADDRESS',	1,	'',
	     'B',		1,	'',
	     'BLOCKQUOTE',	1,	'',
	     'BR',		0,	'',
	     'CITE',		1,	'',
	     'CODE',		1,	'',
	     'DD',		0,	'',
	     'DIR',		1,	'',
	     'DL',		1,	'COMPACT',
	     'DT',		0,	'',
	     'EM',		1,	'',
	     'FONT',		1,	'SIZE/COLOR',
	     'H1',		1,	'ALIGN',
	     'H2',		1,	'ALIGN',
	     'H3',		1,	'ALIGN',
	     'H4',		1,	'ALIGN',
	     'H5',		1,	'ALIGN',
	     'H6',		1,	'ALIGN',
	     'HR',		0,	'SIZE/WIDTH/ALIGN',
	     'I',		1,	'',
	     'IMG',		0,	'SRC/ALT/ALIGN/WIDTH/HEIGHT/BORDER',
	     'KBD',		1,	'',
	     'LI',		0,	'TYPE/VALUE',
	     'LISTING',	1,	'',
	     'MENU',		1,	'',
	     'OL',		1,	'START',
	     'P',		0,	'ALIGN',
	     'PRE',		1,	'',
	     'SAMP',		1,	'',
	     'STRONG',	1,	'',
	     'TT',		1,	'',
	     'UL',		1,	'',
	     'VAR',		1,	'',
	     'XMP',		1,	'',
	     );
	local( $tag );
	while( @htmlTags ) {
	    $tag = shift( @htmlTags );
	    $NEED{ $tag } = shift( @htmlTags );
	    $FEATURE{ $tag } = shift( @htmlTags );
	}
	$F_HTML_TAGS_PARSED = 1;
    }

    $string =~ s/\\>/__EscapedGt\376__/go;
    while (( $tag, $need ) = each( %NEED )) {
	$srcString = $string;
	$string = '';
	while (( $srcString =~ m!<$tag\s+([^>]*)>!i ) || ( $srcString =~ m!<$tag()>!i) ) {
	    $srcString = $';
	    $string .= $`;
	    $1 ? ( $feature = " $1" ) =~ s/\\"/__EscapedQuote\376__/go : ( $feature = '' );
	    if ( &SecureFeature( $tag, $FEATURE{ $tag }, $feature )) {
		if ( $srcString =~ m!</$tag>!i ) {
		    $srcString = $';
		    $markuped = $`;
		    $feature =~ s/&/__amp\377__/go;
		    $feature =~ s/"/__quot\378__/go;
		    $string .= "__$tag Open$feature\376__" . $markuped . "__$tag Close\376__";
		} elsif ( !$need ) {
		    $feature =~ s/&/__amp\377__/go;
		    $feature =~ s/"/__quot\378__/go;
		    $string .= "__$tag Open$feature\376__";
		} else {
		    $string .= "<$tag$feature>" . $srcString;
		    last;
		}
	    } else {
		$string .= "<$tag$feature>";
	    }
	}
	$string .= $srcString;
    }
    $string =~ s/__EscapedGt\376__/\\>/go;
    $string =~ s/__EscapedQuote\376__/\\"/go;
    $string =~ s/&/&amp;/g;
    $string =~ s/"/&quot;/g;
    $string =~ s/</&lt;/g;
    $string =~ s/>/&gt;/g;
    while (( $tag, $need ) = each( %NEED )) {
        $string =~ s!__$tag Open([^\376]*)\376__!<$tag$1>!g;
        $string =~ s!__$tag Close\376__!</$tag>!g;
	$string =~ s!__amp\377__!&!go;
	$string =~ s!__quot\378__!"!go;
    }
}


###
## Featureは安全か?
#
sub SecureFeature {
    local( $tag, $allowedFeatures, $features ) = @_;
    return( 1 ) unless ( $features );
    local( @allowed ) = split( /\//, $allowedFeatures );
    local( $feature );
    local( $ret ) = 1;
    while ( $features ) {
	$feature = &GetFeatureName( *features );
	$value = &GetFeatureValue( *features );
	if ( !$value ) {
	    $value = $features;
	    $features = '';
	}
	$ret = 0 if ( !$feature ) || ( !grep( /$feature/i, @allowed ));
    }
    $ret;
}


###
## Feature名を取得
#
sub GetFeatureName {
    local( *string ) = @_;
    $string = '' unless ( $string =~ s/^\s*([^=\s]*)\s*=\s*"// );
    $1;
}


###
## Featureの値を取得
#
sub GetFeatureValue {
    local( *string ) = @_;
    $string = '' unless ( $string =~ s/^([^"]*)"// );
    $1;
}


###
## エラー表示
#
sub Fatal {

    # エラー番号とエラー情報の取得
    local( $errno ) = @_;

    # エラーメッセージ
    local( $errString );

    if ( $errno == 1 ) {

	$errString = "管理者様へ: File: $LOCK_ORGを作成することができません．システムディレクトリのパーミッションは777になっていますか?";

    } elsif ( $errno == 2 ) {

	$errString = "管理者様へ: メイルを送信することができません．\$MAIL2の値(現在は「$MAIL2」)の設定がおかしくありませんか?";

    } else {

	$errString = 'エラー番号不定: お手数ですが，このエラーメッセージ(「エラー番号不定」)とこのページのURL，またエラーが生じた状況を，<a href="mailto:nakahiro@kinotrope.co.jp">nakahiro@kinotrope.co.jp</a>までお知らせください．';

    }

    # 表示画面の作成
    &Header;

    &cgiprint'Init;
    &cgiprint'Cache(<<__EOF__);
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML i18n//EN">
<html>
<head>
<title>Error!</title>
</head>
<body>
<h1>Error!</h1>
<hr>
<p>$errString</p>
</body>
</html>
__EOF__

    &cgiprint'Flush;
    exit( 0 );
}


###
## 日本語の表示パッケージ
#
package cgiprint;

$STR = '';
$BUFLIMIT = 2048;

sub Init { $STR = ''; }

sub Cache {
    local( $str ) = @_;
    $STR .= $str;
    if ( length( $STR ) > $BUFLIMIT ) { &Flush; }
}

sub Flush {
    &jcode'convert( *STR, $JPOUT_SCHEME );
    print( $STR );
    &Init;
}


#/////////////////////////////////////////////////////////////////////
1;
