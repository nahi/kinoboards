# $Id: cgi.pl,v 2.7 1998-10-22 08:22:59 nakahiro Exp $


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


require( 'jcode.pl' );
require( 'mimew.pl' );


###
## cgiデータ入出力パッケージ
#
package cgi;


$SMTP_SERVER = 'localhost';
# $SMTP_SERVER = 'mailhost';
# or
# $SMTP_SERVER = 'mailhost.foo.bar.baz.jp';
# or
# $SMTP_SERVER = '123.123.123.123';

$AF_INET = 2; $SOCK_STREAM = 1;
# AF_INET = 2, SOCK_STREAM = 1 ... SunOS 4.*, HP-UX, AIX, IRIX, Linux, FreeBSD,
#					WinNT, Mac
# AF_INET = 2, SOCK_STREAM = 2 ... SonOS 5.*(Solaris 2.*)

$CRLF = "\xd\xa";		# cannot use \r\n
				# because of MacPerl's !ox#*& behavior...

$HTTP_COOKIES_NEVER_EXPIRED = 1704067199;
				# Thursday, 31-Dec-2029 23:59:59 GMT

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

%CHARSET_MAP = ( 'euc', 'EUC-JP', 'jis', 'ISO-2022-JP', 'sjis', 'Shift_JIS' );
$CHARSET = 'jis';

$SERVER_NAME = $ENV{'SERVER_NAME'};
$SERVER_PORT = $ENV{'SERVER_PORT'};
$REMOTE_HOST = $ENV{'REMOTE_HOST'};
$REMOTE_USER = $ENV{'REMOTE_USER'};
$SCRIPT_NAME = $ENV{'SCRIPT_NAME'};
$PATH_INFO = $ENV{'PATH_INFO'};
$PATH_TRANSLATED = $ENV{'PATH_TRANSLATED'};

if (( $ENV{'SERVER_SOFTWARE'} =~ /IIS/ ) && ( $SCRIPT_NAME eq $PATH_INFO ))
{
    $PATH_INFO = '';
    $PATH_TRANSLATED = '';
}

( $CGIDIR_NAME, $CGIPROG_NAME ) = $SCRIPT_NAME =~ m!^(..*)/([^/]*)$!o;
$SYSDIR_NAME = ( $PATH_INFO ? "$PATH_INFO/" : "$CGIDIR_NAME/" );
$PROGRAM = ( $PATH_INFO ? "$SCRIPT_NAME$PATH_INFO" : "$CGIPROG_NAME" );


###
## ロック関係
#

# ロック
sub lock
{
    local( $lockFile ) = @_;

    if ( $] =~ /^5/o )
    {
	# for perl5
	return &lock_flock( $lockFile );
    }
    else
    {
	# for perl4
	return &lock_link( $lockFile );
    }
}

# アンロック
sub unlock
{
    if ( $] =~ /^5/o )
    {
	# for perl5
	&unlock_flock;
    }
    else
    {
	# for perl4
	&unlock_link( @_ );
    }
}

# lock with symlink
sub lock_link
{
    local( $lockFile ) = @_;

    local( $lockWait ) = 10;		# [sec]
    local( $lockFileTimeout ) = .004;	# 5.76 [min]
    local( $lockFlag ) = 0;
    local( $timeOut );

    # locked for maintenance by admin.
    return 2 if (( -e $lockFile ) && ( ! -w $lockFile ));

    unlink( $lockFile ) if ( -M "$lockFile" > $lockFileTimeout );

    for ( $timeOut = 0; $timeOut < $lockWait; $timeOut++ )
    {
	open( LOCKORG, ">$lockFile.org" ) || return( 0 );
	close( LOCKORG );
	$lockFlag = 1, last if ( link( "$lockFile.org", $lockFile ));
	unlink( "$lockFile.org" );
	sleep 1;
    }

    $lockFlag;
}

sub unlock_link
{
    local( $lockFile ) = @_;
    unlink( $lockFile );
}

# lock with flock.
sub lock_flock
{
    local( $lockFile ) = @_;
    local( $LockEx, $LockUn ) = ( 2, 8 );
    open( LOCK, ">>$lockFile" ) || return 2;
    flock( LOCK, $LockEx ) || return 0;
    1;
}
sub unlock_flock
{
    local( $LockEx, $LockUn ) = ( 2, 8 );
    flock( LOCK, $LockUn );
    close( LOCK );
}


###
## HTMLヘッダの生成
#
# $ENV{'SERVER_PROTOCOL'} 200 OK
# Server: $ENV{'SERVER_SOFTWARE'}
sub Header
{
    local( $utcFlag, $utcStr, $cookieFlag, *cookieStr, $cookieExpire ) = @_;
    print( "Content-type: text/html; charset=" . $CHARSET_MAP{ $CHARSET } . "\n" );
    $cgiprint'CHARSET = $CHARSET;

    # Header for HTTP Cookies.
    if ( $cookieFlag )
    {
	foreach ( @cookieStr )
	{
	    print( "Set-Cookie: $_;" );
	    if ( $cookieExpire )
	    {
		print( " expires=", &GetHttpDateTimeFromUtc( ( $cookieExpire == -1 )? $HTTP_COOKIES_NEVER_EXPIRED : $^T+$cookieExpire ), ";\n" );
	    }
	}
    }

    # Header for Last-Modified.
    if ( $utcFlag )
    {
	print( "Last-Modified: ", &GetHttpDateTimeFromUtc( $utcStr || $^T ), "\n" );
    }

    # now, the end of Head Block.
    print( "\n" );

}


###
## format as HTTP Date/Time
#
sub GetHttpDateTimeFromUtc
{
    local( $utc ) = @_;
    $utc = 0 if ( $utc !~ /^\d+$/ );
    local( $sec, $min, $hour, $mday, $mon, $year, $wday ) = gmtime( $utc );
    sprintf( "%s, %02d-%s-%02d %02d:%02d:%02d GMT", ( 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday' )[ $wday ], $mday, ( 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec' )[ $mon ], ( $year%100 ), $hour, $min, $sec );
}


###
## CGI変数のデコード
## CAUTION! functioon decode sets global variable, TAGS.
#
sub Decode
{
    local( $args, $readSize, $key, $term, $value, $encode );
    if ( $ENV{ 'REQUEST_METHOD' } eq "POST" )
    {
	$readSize = read( STDIN, $args, $ENV{ 'CONTENT_LENGTH' } );
	$args = '' if ( $readSize != $ENV{ 'CONTENT_LENGTH' } );
    }
    else
    {
	$args = $ENV{ 'QUERY_STRING' };
    }

    foreach $term ( split( '&', $args ))
    {
	( $key, $value ) = split( /=/, $term, 2 );
	$value =~ tr/+/ /;
	$value =~ s/%([0-9A-Fa-f][0-9A-Fa-f])/pack( "C", hex( $1 ))/ge;
	$encode = &jcode'getcode( *value );

	if ( !defined( $encode ))
	{
	    $TAGS{ $key } = $value;
	}
	else
	{
	    &jcode'convert( *value, 'euc', $encode, "z" );
	    $TAGS{ $key } = $value;
	}

	$TAGS{ $key } =~ s/\xd\xa/\xa/go;
	$TAGS{ $key } =~ s/\xd/\xa/go;
    }
}


###
## HTTP Cookiesのデコード
#
sub Cookie
{
    local( $key, $value, $term );
    foreach $term ( split( /;\s*/, $ENV{ 'HTTP_COOKIE' }))
    {
	( $key, $value ) = split( /=/, $term, 2 );
	$COOKIES{ $key } = $value;
    }
}


###
## SendMail - sending mail [ old style before cgi.pl/1.60 ]
#
#
# - SYNOPSIS
#	require( 'cgi.pl' );
#	&cgi'SendMail( $fromName, $fromEmail, $subject, $extension, $message,
#	    @to );
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
#	Send a mail with smtp.
#	This function is used before cgi.pl/1.60.
#	Use &sendMail though it's only for backward compatibility.
#
# - RETURN
#	1 if succeed, 0 if failed.
#
sub SendMail
{
    local( $fromName, $fromEmail, $subject, $extension, $message, @to ) = @_;
    local( $labelTo ) = '';
    local( $header, $body );

    return 0 if ( !( $fromEmail && $subject && $message && @to ));

    # creating header
    $header = &smtpHeader( *fromName, *fromEmail, *subject, *extension,
	*labelTo, *to );

    # creating body
    $body = &smtpBody( *message );

    # initialize connection
    &smtpInit( "S" ) || return 0;

    # helo!
    &smtpMsg( "S", "helo $SERVER_NAME$CRLF" ) || return 0;
    # from
    &smtpMsg( "S", "mail from: <$fromEmail>$CRLF" ) || return 0;
    # rcpt to
    foreach ( @to )
    {
	&smtpMsg( "S", "rcpt to: <$_>$CRLF" ) || return 0;
    }
    # data block
    &smtpMsg( "S", "data$CRLF" ) || return 0;
    # mail header and body
    &smtpMsg( "S", "$header$CRLF$body" . ".$CRLF" ) || return 0;
    # quit
    &smtpMsg( "S", "quit$CRLF" ) || return 0;

    # success!
    1;
}


###
## sendMail - sending mail [ new style after cgi.pl/1.61 ]
#
#
# - SYNOPSIS
#	require( 'cgi.pl' );
#	&cgi'sendMail( $fromName, $fromEmail, $subject, $extension, $message,
#		$labelTo, @to );
#
# - ARGS
#	$fromName	from name
#	$fromEmail	from e-mail addr.
#	$subject	subject
#	$extension	extension header
#	$message	message
#	$labelTo	recipients label for `To: '.
#			@to is used if omitted $labelTo.
#	@to		list of recipients
#
# - DESCRIPTION
#	send a mail with smtp.
#
# - RETURN
#	1 if succeed, 0 if failed.
#
$SMTP_ERRSTR = '';
sub sendMail
{
    local( $fromName, $fromEmail, $subject, $extension, $message, $labelTo,
	@to ) = @_;
    local( $header, $body );

    return( 0, '' ) if ( !( $fromEmail && $subject && $message && @to ));

    # creating header
    $header = &smtpHeader( *fromName, *fromEmail, *subject, *extension,
	*labelTo, *to );

    # creating body
    $body = &smtpBody( *message );

    # initialize connection
    &smtpInit( "S" ) || return( 0, $SMTP_ERRSTR );

    # helo!
    &smtpMsg( "S", "helo $SERVER_NAME$CRLF" ) || return( 0, $SMTP_ERRSTR );
    # from
    &smtpMsg( "S", "mail from: <$fromEmail>$CRLF" ) || return( 0, $SMTP_ERRSTR );
    # rcpt to
    foreach ( @to )
    {
	&smtpMsg( "S", "rcpt to: <$_>$CRLF" ) || return( 0, $SMTP_ERRSTR );
    }
    # data block
    &smtpMsg( "S", "data$CRLF" ) || return( 0, $SMTP_ERRSTR );
    # mail header and body
    &smtpMsg( "S", "$header$CRLF$body" . ".$CRLF" ) || return( 0, $SMTP_ERRSTR );
    # quit
    &smtpMsg( "S", "quit$CRLF" ) || return( 0, $SMTP_ERRSTR );

    # success!
    1;
}


###
## smtpHeader - create smtp header
#
#
# - SYNOPSIS
#	&smtpHeader( $fromName, $fromEmail, $subject, $extension, $labelTo,
#	    @to );
#
# - ARGS
#	same as &sendMail.
#
# - DESCRIPTION
#	create smtp header.
#
# - RETURN
#	header string.
#
sub smtpHeader
{
    local( *fromName, *fromEmail, *subject, *extension, *labelTo, *to ) = @_;

    local( $header, $from, $encode );

    # mime encoding of Japanese multi-byte char in header.
    $encode = &jcode'getcode( *fromName );
    $fromName = &main'mimeencode( $fromName ) if ( defined( $encode ));
    $from = "$fromName <$fromEmail>";

    $encode = &jcode'getcode( *subject );
    $subject = &main'mimeencode( $subject ) if ( defined( $encode ));

    $encode = &jcode'getcode( *extension );
    $extension = &main'mimeencode( $extension ) if ( defined( $encode ));

    # creating header
    $header = "To: ";
    if ( $labelTo )
    {
	$encode = &jcode'getcode( *labelTo );
	$labelTo = &main'mimeencode( $labelTo ) if ( defined( $encode ));
	$header .= "$labelTo$CRLF";
    }
    else
    {
	# should we encode those with MIME Base64?
	$header .= join( ",$CRLF\t", @to );
	$header .= $CRLF;
    }
    $header .= "From: $from$CRLF";
    $header .= "Reply-To: $from$CRLF";
    $header .= "Sendar: $from$CRLF";
    $header .= "Subject: $subject$CRLF";
    $header .= "Content-type: text/plain; charset=ISO-2022-JP$CRLF";
    if ( $extension )
    {
	$header .= join( $CRLF, split( /\n/, $extension ));
	$header .= $CRLF;
    }

    $header;
}


###
## smtpBody - create smtp body
#
#
# - SYNOPSIS
#	&smtpBody( *message );
#
# - ARGS
#	$message	message body.
#
# - DESCRIPTION
#	create smtp body.
#
# - RETURN
#	body string.
#
sub smtpBody
{
    local( *message ) = @_;
    local( $body ) = '';
    &jcode'convert( *message, 'jis' );
    foreach ( split( /\n/, $message ))
    {
	s/^\.$/\.\./o;		# `.' is the end of the message.
	$body .= "$_$CRLF";
    }

    $body;
}


###
## smtpInit - initialize a connection with MTA
#
#
# - SYNOPSIS
#	&smtpInit( $sh );
#
# - ARGS
#	$sh		socket handle's name.
#
# - DESCRIPTION
#	initialize a connection with MTA and check the result.
#
# - RETURN
#	1 if succeed, 0 if failed.
#
sub smtpInit
{
    local( $sh ) = @_;
    local( $sockAddr ) = 'S n a4 x8';
#    local( $smtpPort ) = 'smtp';	# 25
    local( $smtpPort ) = '25';		# smtp
    local( $proto, $port, $smtpAddr, $sock, $oldStream );

    # preparing for smtp connection...
    $proto = ( getprotobyname( 'tcp' ))[2];
    $port = ( $smtpPort =~ /^\d+$/ ) ? $smtpPort : ( getservbyname( $smtpPort,
	'tcp' ))[2];
    if ( $SMTP_SERVER =~ /^(\d+)\.(\d+)\.(\d+)\.(\d+)$/ )
    {
	$smtpAddr = pack( 'C4', $1, $2, $3, $4 );
    }
    else
    {
	$smtpAddr = ( gethostbyname( $SMTP_SERVER ))[4];
    }
    if ( !$smtpAddr )
    {
	$SMTP_ERRSTR = 'cannot find IP addr of my smtp server.';
	return 0;
    }
    $sock = pack( $sockAddr, $AF_INET, $port, $smtpAddr );

    # create connection...
    if ( !socket( $sh, $AF_INET, $SOCK_STREAM, $proto ))
    {
	$SMTP_ERRSTR = 'create socket failed.';
	return 0;
    }
    if ( !connect( $sh, $sock ))
    {
	$SMTP_ERRSTR = 'create connection failed.';
	return 0;
    }
    $oldStream = select( $sh ); $| = 1; select( $oldStream );

    # check the result code of the connection
    &smtpMsg( $sh, "" ) || return 0;

    # initialize succeed!
    return 1;
}


###
## smtpMsg - send a message to MTA
#
#
# - SYNOPSIS
#	&smtpMsg( $sh, $message );
#
# - ARGS
#	$sh		socket handle's name
#	$message	message with CRLF
#
# - DESCRIPTION
#	send a message to MTA and check the result.
#
# - RETURN
#	1 if succeed, 0 if failed.
#
sub smtpMsg
{
    local( $sh, $message ) = @_;
    local( $back );
    print( $sh $message ) if $message;
    $back = <$sh>;
    if ( $back =~ /^[45]/o )
    {
	close( $sh );
	$SMTP_ERRSTR = $back;
	return 0;
    }
    else
    {
	return 1;
    }
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

sub SecureHtml
{
    local( *string ) = @_;
    local( $srcString, $tag, $need, $feature, $markuped );

    # HTML_TAGSの解析（一度だけ実施）
    if ( $F_HTML_TAGS_PARSED != 1 )
    {
	while( @HTML_TAGS )
	{
	    $tag = shift( @HTML_TAGS );
	    $NEED{ $tag } = shift( @HTML_TAGS );
	    $FEATURE{ $tag } = shift( @HTML_TAGS );
	}
	$F_HTML_TAGS_PARSED = 1;
    }

    $string =~ s/\\>/__EscapedGt\376__/go;
    while (( $tag, $need ) = each( %NEED ))
    {
	$srcString = $string;
	$string = '';
	while (( $srcString =~ m!<$tag\s+([^>]*)>!i ) || ( $srcString =~ m!<$tag()>!i) )
	{
	    $srcString = $';
	    $string .= $`;
	    if ( $1 )
	    {
		( $feature = " $1" ) =~ s/\\"/__EscapedQuote\376__/go;
	    }
	    else
	    {
		$feature = '';
	    }
	    if ( &SecureFeature( $tag, $FEATURE{ $tag }, $feature ))
	    {
		if ( $srcString =~ m!</$tag>!i )
		    {
		    $srcString = $';
		    $markuped = $`;
		    $feature =~ s/&/__amp\376__/go;
		    $feature =~ s/"/__quot\376__/go;
		    $string .= "__$tag Open$feature\376__" . $markuped .
			"__$tag Close\376__";
		}
		elsif ( !$need )
		{
		    $feature =~ s/&/__amp\376__/go;
		    $feature =~ s/"/__quot\376__/go;
		    $string .= "__$tag Open$feature\376__";
		}
		else
		{
		    $string .= "<$tag$feature>" . $srcString;
		    last;
		}
	    }
	    else
	    {
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
    while (( $tag, $need ) = each( %NEED ))
    {
        $string =~ s!__$tag Open([^\376]*)\376__!<$tag$1>!g;
        $string =~ s!__$tag Close\376__!</$tag>!g;
	$string =~ s!__amp\376__!&!go;
	$string =~ s!__quot\376__!"!go;
    }
}


###
## Featureは安全か?
#
sub SecureFeature
{
    local( $tag, $allowedFeatures, $features ) = @_;
    local( @allowed, $feature, $ret );

    return 1 unless ( $features );
    @allowed = split( /\//, $allowedFeatures );
    $ret = 1;

    while ( $features )
    {
	$feature = &GetFeatureName( *features );
	$value = &GetFeatureValue( *features );
	if ( !$value )
	{
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
sub GetFeatureName
{
    local( *string ) = @_;
    $string = '' unless ( $string =~ s/^\s*([^=\s]*)\s*=\s*"// );
    $1;
}


###
## Featureの値を取得
#
sub GetFeatureValue
{
    local( *string ) = @_;
    $string = '' unless ( $string =~ s/^([^"]*)"// );
    $1;
}


###
## CGI authentication package
#
package cgiauth;

$GUEST = 'guest';
$ADMIN = 'admin';
$DEFAULT_PASSWD_LENGTH = 6;
$AUTH_TYPE = 1;			# 1 ... use HTTP-Cookies
				# 2 ... use Server Authentication
				# 3 ... use direct URL Authentication
$F_COOKIE_RESET = "CookieReset\376";


###
## CheckUser - user authentication
#
# - SYNOPSIS
#	with HTTP-Cookies,
#		require( 'cgi.pl' );
#		&cgi'Decode;
#		&cgi'Cookie;
#		$cgiauth'AUTH_TYPE = 1;
#		( $status, $uid, $passwd, @userInfo ) = &cgiauth'CheckUser( $userdb );
#
#	with Server Authentication
#		require( 'cgi.pl' );
#		$cgiauth'AUTH_TYPE = 2;
#		( $status, $uid, $passwd, @userInfo ) = &cgiauth'CheckUser( $userdb );
#
#	with direct URL Authentication
#		require( 'cgi.pl' );
#		&cgi'Decode;
#		$cgiauth'AUTH_TYPE = 3;
#		( $status, $uid, $passwd, @userInfo ) = &cgiauth'CheckUser( $userdb );
#
# - ARGS
#	$userdb		user db.
#
# - DESCRIPTION
#	check user's name and password.
#
# - RETURN
#	returns status, user entry, encrypted password,
#	and listed user's info.
#
#	status:
#		0 ... succeed authentication.
#		1 ... $user is null.
#		2 ... cannot open DB file.
#		3 ... $user was not found in DB.
#		4 ... password incorrect.
#
sub CheckUser
{
    local( $userdb ) = @_;
    if ( $AUTH_TYPE == 1 )
    {
	# with HTTP-Cookies

	if ( $cgi'TAGS{'kinoU'} )
	{
	    # authentication data in TAGS.
	    return( &CheckUserPasswd( $userdb, $cgi'TAGS{'kinoU'}, $cgi'TAGS{'kinoP'} ));
	}
	elsif ( $cgi'COOKIES{'kinoauth'} )
	{
	    # authentication succeed if HTTP-Cookie was set.
	    return( &GetUserInfo( $userdb, $cgi'COOKIES{'kinoauth'} ));
	}
    }
    elsif (( $AUTH_TYPE == 2 ) && $cgi'REMOTE_USER )
    {
	# with Server Authentication

	# authentication successes if REMOTE_USER was set.
	return( &GetUserInfo( $userdb, $cgi'REMOTE_USER ));
    }
    elsif ( $cgi'TAGS{'kinoU'} )
    {
	# with direct URL Authentication

	# authentication data in TAGS.
	return( &CheckUserPasswd( $userdb, $cgi'TAGS{'kinoU'}, $cgi'TAGS{'kinoP'} ));
    }

    # default authentication.
    return( &CheckUserPasswd( $userdb, $GUEST, '' ));
}


###
## GetUserInfo - get user's info.
#
# - SYNOPSIS
#	&GetUserInfo( $userdb, $uid );
#
# - ARGS
#	$userdb		user db.
#	$uid		user id / user entry.
#
# - DESCRIPTION
#	get specified user's info.
#
# - RETURN
#	returns status, user entry, encrypted password,
#	and listed user's info.
#
#	status
#		0 ... entry found.
#		1 ... $uid is null.
#		2 ... cannot open DB file.
#		3 ... $uid was not found in DB.
#
sub GetUserInfo
{
    local( $userdb, $user ) = @_;

    # no password check.
    &CheckUserPasswd( $userdb, $user, undef );
}


###
## CreateUserDb - create new user db.
#
# - SYNOPSIS
#	&cgiauth'CreateUesrDb( $userdb );
#
# - ARGS
#	$userdb		new user db.
#
# - DESCRIPTION
#	create new user db.
#
# - RETURN
#	1 if succeed. 0 if failed.
#
sub CreateUserDb
{
    local( $userdb ) = @_;

    # already exists.
    return( 0 ) if ( -e "$userdb" );

    # create
    open( USERDB, ">$userdb" ) || return( 0 );
    close( USERDB );

    # add guest user with no passwd.
    if ( !defined( &AddUser( $userdb, $ADMIN, '', ())) || !defined( &AddUser( $userdb, $GUEST, '', ())))
    {
	unlink( $userdb );
	return( 0 );
    }

    1;
}


###
## AddUser - add new user.
#
# - SYNOPSIS
#	&cgiauth'AddUser( $userdb, $user, $passwd, @userInfo );
#
# - ARGS
#	$userdb		user db.
#	$user		user entry.
#	$passwd		password.
#	@userInfo	user's info.
#
# - DESCRIPTION
#	add new user to DB.
#
# - RETURN
#	0 if succeed.
#	1 if failed ( user entry duplicated ).
#	2 if failed ( unknown ).
#
sub AddUser
{
    local( $userdb, $user, $passwd, @userInfo ) = @_;
    local( $id, $newLine );
    local( $dId, $dUser );

    open( USERDB, "<$userdb" ) || return 2;
    while( <USERDB> )
    {
	( $dId, $dUser ) = split( /\t/, $_, 3 );
	if ( $dUser eq $user )
	{
	    close( USERDB );
	    return 1;
	}
    }
    close( USERDB );

    $id = &NewId( $userdb );
    $newLine = sprintf( "%s\t%s\t%s\t%s\t%s", $id, $user, $^T, $cgi'REMOTE_HOST, ( substr( crypt( $passwd, $id ), 2 )));
    foreach ( @userInfo ) { $newLine .= "\t" . $_; }
    open( USERDB, ">>$userdb" ) || return 2;
    print( USERDB $newLine . "\n" );
    close( USERDB );

    0;
}


###
## SetUserPasswd - set user passwd.
#
# - SYNOPSIS
#	&cgiauth'SetUserPasswd( $userdb, $user, $passwd );
#
# - ARGS
#	$userdb		user db.
#	$user		user entry.
#	$passwd		user's password.
#
# - DESCRIPTION
#	set user's password.
#
# - RETURN
#	returns 1 if succeed.
#	0 if failed.
#
sub SetUserPasswd
{
    local( $userdb, $user, $passwd ) = @_;
    local( $tmpFile ) = "$userdb.tmp.$$";
    local( $found ) = 0;
    local( $dId, $dUser, $dAddTime, $dAddHost, $dPasswd, $dInfo );

    open( USERDBTMP, ">$tmpFile" ) || return( 0 );
    open( USERDB, "<$userdb" ) || return( 0 );
    while( <USERDB> )
    {
	print( USERDBTMP $_ ), next if ( /^\#/o || /^$/o );
	chop;
	( $dId, $dUser, $dAddTime, $dAddHost, $dPasswd, $dInfo ) = split( /\t/, $_ );

	if ( $dUser eq $user )
	{
	    printf( USERDBTMP "%s\t%s\t%s\t%s\t%s\t%s\n", $dId, $dUser, $dAddTime, $dAddHost, ( substr( crypt( $passwd, $dId ), 2 )), $dInfo );
	    $found = 1;
	}
	else
	{
	    print( USERDBTMP $_ . "\n" );
	}
    }
    close( USERDB );
    close( USERDBTMP );

    rename( $tmpFile, $userdb ) || return( 0 );

    $found;
}


###
## SetUserInfo - set user info.
#
# - SYNOPSIS
#	&cgiauth'SetUserInfo( $userdb, $user, @userInfo );
#
# - ARGS
#	$userdb		user db.
#	$user		user entry.
#	@userInfo	user's info.
#
# - DESCRIPTION
#	set user info.
#
# - RETURN
#	returns 1 if succeed.
#	0 if failed.
#
sub SetUserInfo
{
    local( $userdb, $user, @userInfo ) = @_;
    local( $tmpFile ) = "$userdb.tmp.$$";
    local( $found ) = 0;
    local( $dId, $dUser, $dAddTime, $dAddHost, $dPasswd, @dInfo, $newLine );

    open( USERDBTMP, ">$tmpFile" ) || return( 0 );
    open( USERDB, "<$userdb" ) || return( 0 );
    while( <USERDB> )
    {
	print( USERDBTMP $_ ), next if ( /^\#/o || /^$/o );
	chop;
	( $dId, $dUser, $dAddTime, $dAddHost, $dPasswd, @dInfo ) = split( /\t/, $_ );

	if ( $dUser eq $user )
	{
	    printf( USERDBTMP "%s\t%s\t%s\t%s\t%s\t%s\n", $dId, $dUser, $dAddTime, $dAddHost, $dPasswd, join( "\t", @userInfo ));
	    $found = 1;
	}
	else
	{
	    print( USERDBTMP $_ . "\n" );
	}
    }
    close( USERDB );
    close( USERDBTMP );

    rename( $tmpFile, $userdb ) || return( 0 );

    $found;
}


###
## Header - header print
#
# - SYNOPSIS
#	&cgiauth'Header( $lastModifiedP, $lastModifiedTime, $user, $cookieExpire );
#
# - ARGS
#	$lastModifiedP		print last-modified header or not.
#	$lastModifiedTime	time for last-modified header.
#				if null, now is the time for last-modified.
#	$user			user id.
#				does not send HTTP Cookies if $user is null.
#				reset HTTP Cookies if $user is $cgiauth'F_COOKIE_RESET.
#	$cookieExpire		expires HTTP Cookies or not.
#
# - DESCRIPTION
#	exec cgi.pl's Header function to set HTTP-Cookies header.
#
# - RETURN
#	nothing.
#
sub Header
{
    local( $lastModifiedP, $lastModifiedTime, $user, $cookieExpire ) = @_;

    if ( $user eq '' )
    {
	# no cookies
	&cgi'Header( $lastModifiedP, $lastModifiedTime, 0 );
    }
    elsif ( $user eq $F_COOKIE_RESET )
    {
	# not numeric. reset.
	&cgi'Header( $lastModifiedP, $lastModifiedTime, 1, "kinoauth=", $cookieExpire );
    }
    elsif ( $UID eq $cgi'COOKIES{'kinoauth'} )
    {
	# no cookies
	&cgi'Header( $lastModifiedP, $lastModifiedTime, 0 );
    }
    else
    {
	# set
	&cgi'Header( $lastModifiedP, $lastModifiedTime, 1, "kinoauth=$UID", $cookieExpire );
    }
}


###
## LinkTagWithAuth - create A tag format.
#
# - SYNOPSIS
#	LinkTagWithAuth( $url, $markUp, $uid, $passwd );
#
# - ARGS
#	$url		URL.
#	$markUp		markup-ed text.
#	$uid		user id; must be NUMERIC.
#	$passwd		password; must be encrypted.
#
# - DESCRIPTION
#	create A tag format from given data.
#	for authentication, 'kinoU=$uid' and 'kinoP=$passwd' is added.
#
# - RETURN
#	formatted string.
#
sub LinkTagWithAuth
{
    local( $url, $markUp, $uid, $passwd ) = @_;
    local( $urlStr ) = $url . ( grep( /\?/, $url ) ? '&' : '?' ) .
	"kinoU=$uid&kinoP=$passwd";
    "<a href=\"$urlStr\">$markUp</a>";
}


###
## CheckUserPasswd - check user's name and password.
#
# - SYNOPSIS
#	&CheckUserPasswd( $userdb, $user, $passwd );
#
# - ARGS
#	$userdb		user db.
#	$user		user entry.
#	$passwd		password.
#
# - DESCRIPTION
#	check user's name and password.
#	password will not be checked if undefined value.
#
# - RETURN
#	returns status, user entry, encrypted password,
#	and listed user's info.
#
#	status
#		0 ... succeed authentication.
#		1 ... $user is null.
#		2 ... cannot open DB file.
#		3 ... $user was not found in DB.
#		4 ... password incorrect.
#
sub CheckUserPasswd
{
    local( $userdb, $user, $passwd ) = @_;
    local( $dId, $dUser, $dAddTime, $dAddHost, $dPasswd, @dInfo );

    return( 1 ) if ( !$user );

    open( USERDB, "<$userdb" ) || return( 2 );
    while( <USERDB> )
    {
	next if ( /^\#/o || /^$/o );
	chop;
	( $dId, $dUser, $dAddTime, $dAddHost, $dPasswd, @dInfo ) = split( /\t/, $_ );

	if ( $dUser eq $user )
	{
	    close( USERDB );
	    if (( $passwd eq $dPasswd ) || ( substr( crypt( $passwd, $dId ), 2 ) eq $dPasswd ))
	    {
		$UID = $dId;
		return( 0, $dUser, $dPasswd, @dInfo );
	    }
	    return( 4 );
	}

	if ( $dId eq $user )
	{
	    close( USERDB );
	    if ( !defined( $passwd ))
	    {
		$UID = $dId;
		return( 0, $dUser, $dPasswd, @dInfo );
	    }
	    return( 4 );
	}
    }
    close( USERDB );
    return( 3 );
}


###
## NewId - get new user's id.
#
# - SYNOPSIS
#	&NewId( $userdb );
#
# - ARGS
#	$userdb		user db.
#
# - DESCRIPTION
#	get new user id which is not used before.
#	at first get maximum id from DB,
#	increment it, then return as new id.
#
# - RETURN
#	returns generated new user id.
#	undef if failed.
#
sub NewId
{
    local( $userdb ) = @_;
    local( $dId, $maxId );
    $maxId = 0;
    open( USERDB, "<$userdb" ) || return( undef );
    while( <USERDB> )
    {
	next if ( /^\#/o || /^$/o );
	chop;
	( $dId = $_ ) =~ s/\t.*$//o;
	$maxId = $dId if ( $dId > $maxId ) ;
    }

    ++$maxId;
}


###
## CreateNewPasswd - create password
#
# - SYNOPSIS
#	&CreateNewPasswd;
#
# - ARGS
#	nothing
#
# - DESCRIPTION
#	create new password for new user.
#
# - RETURN
#	returns created password.
#
sub CreateNewPasswd
{
    local( $passwd, $n );
    local( $i ) = $DEFAULT_PASSWD_LENGTH;

    while( --$i >= 0 )
    {
	$n = 97 + int( rand( 36 ));
	$n = $n - 75 if ( $n >= 123 );
	$passwd .= sprintf( "%c", $n );
    }
    
    $passwd;
}


###
## 日本語の表示パッケージ
#
package cgiprint;

$STR = '';
$BUFLIMIT = 4096;
$CHARSET = 'jis';

sub Init { $STR = ''; }

sub Cache
{
    $STR .= shift;
    &Flush if ( length( $STR ) > $BUFLIMIT );
}

sub Flush
{
    &jcode'convert( *STR, $CHARSET ) if ( $CHARSET ne 'euc' );
    print( $STR );
    &Init;
}


#/////////////////////////////////////////////////////////////////////
1;
