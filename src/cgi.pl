# $Id: cgi.pl,v 1.28 1998-02-21 17:21:14 nakahiro Exp $


# Small CGI tool package(use this with jcode.pl-2.0).
# Copyright (C) 1995-98 NAKAMURA Hiroshi.
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
#	<URL:ftp://ftp.iij.ad.jp/pub/IIJ/dist/utashiro/perl/>
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
# $cgi'CGIDIR_NAME;
#	起動されたCGIが置かれているディレクトリの相対URLが設定されます．
#	ex. → /cgi-bin/foo
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
#	$fileで指定されたロックファイル名を使い，
#	perl programを排他的にロックします．
#	（ロックするファイルを指定するのではないことに注意）．
#	メンテナンスロック中なら
#	（実行ユーザで削除できないロックファイルが既に存在するなら），
#	2を，通常のロックが無事行えれば1を，
#	なんらかの理由で行えなければ0を返します．
#
#	※Win95やMacではこの関数を呼ばないようにしてください．
#	  ロックできません(涙)．
#
# &cgi'unlock( $file );
#	$fileで指定されたロックファイル名を使い，
#	かけられた排他ロックを外します．
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
#	数字でない文字列を与えると，
#	UNIX origin timeのHTTP Date/Timeフォーマットを返します．
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
#	$SMTP_SERVERにサーバのホスト名，
#	もしくはIPアドレスを指定しておいてください．
#	OSによっては，$AF_INETと$SOCK_STREAMの値も変更する必要があります．
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
#	CGIプログラムからブラウザに送信する文字列を，
#	ISO-2022-jp（いわゆるJIS）に変換し，標準出力に吐き出します．
#	高速化のためにキャッシュを持っています．
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


$SMTP_SERVER = 'localhost';
# $SMTP_SERVER = 'mailsvr';
# or
# $SMTP_SERVER = 'mailsvr.foo.bar.baz.jp';
# or
# $SMTP_SERVER = '123.123.123.123';

$AF_INET = 2; $SOCK_STREAM = 1;
# AF_INET = 2, SOCK_STREAM = 1 ... SunOS 4.*, HP-UX, AIX, Linux, FreeBSD
# AF_INET = 2, SOCK_STREAM = 2 ... SonOS 5.*

$SMTP_PORT = 'smtp';
srand( $^T|$$ );

@HTML_TAGS = (
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

$SERVER_NAME = $ENV{'SERVER_NAME'};
$SERVER_PORT = $ENV{'SERVER_PORT'};
$REMOTE_HOST = $ENV{'REMOTE_HOST'};
$REMOTE_USER = $ENV{'REMOTE_USER'};
$SCRIPT_NAME = $ENV{'SCRIPT_NAME'};
$PATH_INFO = $ENV{'PATH_INFO'};
$PATH_TRANSLATED = $ENV{'PATH_TRANSLATED'};

($CGIDIR_NAME, $CGIPROG_NAME) = $SCRIPT_NAME =~ m!^(..*)/([^/]*)$!o;
$SYSDIR_NAME = (($PATH_INFO) ? "$PATH_INFO/" : "$CGIDIR_NAME/");
$PROGRAM = (($PATH_INFO) ? "$SCRIPT_NAME$PATH_INFO" : "$CGIPROG_NAME");


###
## ロック関係
#

# ロック
sub lock {
    local( $lockFile ) = @_;
    if ( $] =~ /^5/o ) {
	# for perl5
	return( &lock_flock( $lockFile ));
    }
    else {
	# for perl4
	return( &lock_link( $lockFile ));
    }
}

# アンロック
sub unlock {
    if ( $] =~ /^5/o ) {
	# for perl5
	&unlock_flock;
    }
    else {
	# for perl4
	&unlock_link( @_ );
    }
}

# lock with symlink
sub lock_link {
    local( $lockFile ) = @_;
    local( $lockWait ) = 10;		# [sec]
    local( $lockFileTimeout ) = .004;	# 5.76 [min]
    local( $timeOut ) = 0;
    local( $lockFlag ) = 0;

    # locked for maintenance by admin.
    return( 2 ) if (( -e $lockFile ) && ( ! -w $lockFile ));

    if ( -M "$lockFile" > $lockFileTimeout ) { unlink( $lockFile ); }
    for( $timeOut = 0; $timeOut < $lockWait; $timeOut++ ) {
	open( LOCKORG, ">$lockFile.org" ) || return( 0 );
	close( LOCKORG );
	$lockFlag = 1, last if ( link( "$lockFile.org", $lockFile ));
	unlink( "$lockFile.org" );
	sleep( 1 );
    }
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
    open( LOCK, ">>$lockFile" ) || return( 2 );
    flock( LOCK, $LockEx ) || return( 0 );
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
	printf( "Last-Modified: %s\n", &GetHttpDateTimeFromUtc( $utcStr || $^T ));
    }

    print( "\n" );

}


###
## format as HTTP Date/Time
#
sub GetHttpDateTimeFromUtc {
    local( $utc ) = @_;
    if ( $utc !~ /^\d+$/ ) { $utc = 0; }
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
	$args = '' if ( $readSize != $ENV{ 'CONTENT_LENGTH' } );
    }
    else {
	$args = $ENV{ 'QUERY_STRING' };
    }

    foreach $term ( split( '&', $args )) {
	( $key, $value ) = split( /=/, $term, 2 );
	$value =~ tr/+/ /;
	$value =~ s/%([0-9A-Fa-f][0-9A-Fa-f])/pack( "C", hex( $1 ))/ge;
	$encode = &jcode'getcode( *value );

	if ( !defined( $encode )) {
	    $TAGS{ $key } = $value;
	}
	else {
	    &jcode'convert( *value, 'euc', $encode, "z" );
	    $TAGS{ $key } = $value;
	}

	$TAGS{ $key } =~ s/\0x0d\0x0a/\0x0a/go;
	$TAGS{ $key } =~ s/\0x0d/\0x0a/go;
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
## SendMail - sending mail
#
#
# - SYNOPSIS
#	require( 'cgi.pl' );
#	&cgi'SendMail( $fromName, $fromEmail, $subject, $extension, $message,
#		@to );
#
# - ARGS
#	$fromName	from name
#	$fromEmail	from e-mail addr.
#	$subject	subject
#	$extension	extension header
#	$message	message
#	@to		list of recipients
#
# - DESCRIPTION
#	send a mail with smtp.
#
# - RETURN
#	1 if succeed, 0 if failed.
#
sub SendMail {
    local( $fromName, $fromEmail, $subject, $extension, $message, @to ) = @_;
    local( $from ) = "$fromName <$fromEmail>";
    local( $sockAddr ) = 'S n a4 x8';
    local( $port, $smtpAddr, $sock, $oldStream, $back, $toFirst );

    return( 0 ) if ( !( $fromEmail && $subject && $message && @to ));

    # preparing for smtp connection...
    $proto = (getprotobyname( 'tcp' ))[2];
    $port = ( $SMTP_PORT =~ /^\d+$/ ) ? $SMTP_PORT : (getservbyname( $SMTP_PORT, 'tcp' ))[2];
    if ( $SMTP_SERVER =~ /^(\d+)\.(\d+)\.(\d+)\.(\d+)$/ ) {
	$smtpAddr = pack( 'C4', $1, $2, $3, $4 );
    }
    else {
	$smtpAddr = (gethostbyname( $SMTP_SERVER ))[4];
    }
    return( 0 ) if ( !$smtpAddr );

    $sock = pack( $sockAddr, $AF_INET, $port, $smtpAddr );

    # create connection...
    socket( S, $AF_INET, $SOCK_STREAM, $proto ) || return( 0 );
    connect( S, $sock ) || return( 0 );
    $oldStream = select( S ); $| = 1; select( $oldStream );
    $back = <S>;
    if ( !&checkSmtpResult( $back )) {
	close( S );
	return( 0 );
    }

    # helo!
    print( S "helo $SERVER_NAME\r\n" );
    $back = <S>;
    if ( !&checkSmtpResult( $back )) {
	close( S );
	return( 0 );
    }

    # from
    print( S "mail from: <$fromEmail>\r\n" );
    $back = <S>;
    if ( !&checkSmtpResult( $back )) {
	close( S );
	return( 0 );
    }

    # rcpt to
    foreach ( @to ) {
	print( S "rcpt to: <$_>\r\n" );
	$back = <S>;
	if ( !&checkSmtpResult( $back )) {
	    close( S );
	    return( 0 );
	}
    }

    # data block
    print( S "data\r\n" );
    $back = <S>;
    if ( !&checkSmtpResult( $back )) {
	close( S );
	return( 0 );
    }

    # mail header
    $toFirst = 1;
    foreach ( @to ) {
	if ( $toFirst ) {
	    print( S "To: $_" );
	    $toFirst = 0;
	}
	else {
	    print( S ",\r\n\t$_" );
	}
    }
    print( S "\r\n" );
    print( S "From: $from\r\n" );
    print( S "Reply-To: $from\r\n" );# block replying to all rcps...
    print( S "Errors-To: $from\r\n" );
    print( S "Subject: $subject\r\n" );
    print( S "Content-type: text/plain; charset=ISO-2022-JP\r\n" );
    if ( $extension ) {
	foreach ( split( /\n/, $extension )) {
	    print( S "$_\r\n" );
	}
    }
    print( S "\r\n" );

    # mail body
    &jcode'convert( *message, 'jis' );
    foreach ( split( /\n/, $message )) {
	s/^\.$/\.\./o;		# `.' is the end of the message.
	print( S "$_\r\n" );
    }

    # end of the body
    print( S ".\r\n" );		# `.' is the e... yes, you know. :)
    $back = <S>;
    if ( !&checkSmtpResult( $back )) {
	close( S );
	return( 0 );
    }

    # quit
    print( S "quit\r\n" );
    $back = <S>;

    # success!
    1;
}

sub checkSmtpResult {
    local( $str ) = @_;
    $str !~ /^[45]/o;
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
	while( @HTML_TAGS ) {
	    $tag = shift( @HTML_TAGS );
	    $NEED{ $tag } = shift( @HTML_TAGS );
	    $FEATURE{ $tag } = shift( @HTML_TAGS );
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
		    $feature =~ s/&/__amp\376__/go;
		    $feature =~ s/"/__quot\376__/go;
		    $string .= "__$tag Open$feature\376__" . $markuped . "__$tag Close\376__";
		}
		elsif ( !$need ) {
		    $feature =~ s/&/__amp\376__/go;
		    $feature =~ s/"/__quot\376__/go;
		    $string .= "__$tag Open$feature\376__";
		}
		else {
		    $string .= "<$tag$feature>" . $srcString;
		    last;
		}
	    }
	    else {
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
	$string =~ s!__amp\376__!&!go;
	$string =~ s!__quot\376__!"!go;
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
## 日本語の表示パッケージ
#
package cgiprint;

$STR = '';
$BUFLIMIT = 4096;

sub Init { $STR = ''; }

sub Cache {
    local( $str ) = @_;
    $STR .= $str;
    if ( length( $STR ) > $BUFLIMIT ) { &Flush; }
}

sub Flush {
    &jcode'convert( *STR, 'jis' );
    print( $STR );
    &Init;
}


#/////////////////////////////////////////////////////////////////////
1;
