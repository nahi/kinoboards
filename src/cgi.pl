# $Id: cgi.pl,v 2.37 1999-10-20 14:30:10 nakahiro Exp $


# Small CGI tool package(use this with jcode.pl-2.0).
# Copyright (C) 1995-99 NAKAMURA Hiroshi.
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
## Small CGI tool package.
#
package cgi;


$SMTP_SERVER = 'localhost';
#    $SMTP_SERVER = 'mailhost';
# or $SMTP_SERVER = 'mailhost.foo.bar.baz.jp';
# or $SMTP_SERVER = '123.123.123.123';

$AF_INET = 2; $SOCK_STREAM = ( $^O eq 'solaris' )? 2 : 1;
# AF_INET = 2, SOCK_STREAM = 1 ... SunOS 4.*, HP-UX, AIX, IRIX, Linux, FreeBSD,
#					WinNT, Mac
# AF_INET = 2, SOCK_STREAM = 2 ... SonOS 5.*(Solaris 2.*)

$CRLF = "\x0d\x0a";		# cannot use \r\n
				# because of MacPerl's !ox#*& behavior...

@TAG_ALLOWED = ();		# CGI variables which is allowed to use <>.

%CHARSET_MAP = ( 'euc', 'EUC-JP', 'jis', 'ISO-2022-JP', 'sjis', 'Shift_JIS' );
$CHARSET = 'euc';

$SERVER_NAME = $ENV{'SERVER_NAME'};
$SERVER_PORT = $ENV{'SERVER_PORT'};
$REMOTE_HOST = $ENV{'REMOTE_HOST'};
$REMOTE_ADDR = $ENV{'REMOTE_ADDR'};
$REMOTE_USER = $ENV{'REMOTE_USER'};
$REQUEST_URI = $ENV{'REQUEST_URI'};
$SCRIPT_NAME = $ENV{'SCRIPT_NAME'};
$QUERY_STRING = $ENV{'QUERY_STRING'};
$PATH_INFO = $ENV{'PATH_INFO'};

if (( $ENV{'SERVER_SOFTWARE'} =~ /IIS/ ) && ( $SCRIPT_NAME eq $PATH_INFO ))
{
    # for IIS...
    $PATH_INFO = '';
    $PROGRAM = $REQUEST_URI = $SCRIPT_NAME;
    $REQUEST_URI .= '?' . $QUERY_STRING if $QUERY_STRING;
}
else
{
    # for not IIS...

    # It seems that only Apache support REQUEST_URI...
    unless ( $REQUEST_URI )
    {
	$REQUEST_URI = "$SCRIPT_NAME$PATH_INFO";
	$REQUEST_URI .= "?$QUERY_STRING" if $QUERY_STRING;
    }
    ( $PROGRAM = $REQUEST_URI ) =~ s/\?.*$//o;
}

# Locking
sub lock_file
{
    local( $lockFile ) = @_;

    if ( $] =~ /^5/o )
    {
	# for perl5
	return &lock_file_flock( $lockFile );
    }
    else
    {
	# for perl4
	return &lock_file_link( $lockFile );
    }
}

# Unlocking
sub unlock_file
{
    if ( $] =~ /^5/o )
    {
	# for perl5
	&unlock_file_flock;
    }
    else
    {
	# for perl4
	&unlock_file_link;
    }
}

# For backward compatibility...
sub lock { &lock_file; }
sub unlock { &unlock_file; }

# lock with symlink
sub lock_file_link
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
	open( LOCKORG, ">$lockFile.org" ) || return 0;
	close LOCKORG;
	$lockFlag = 1, last if ( link( "$lockFile.org", $lockFile ));
	unlink( "$lockFile.org" );
	sleep 1;
    }

    $lockFlag;
}

sub unlock_file_link
{
    local( $lockFile ) = @_;
    unlink( $lockFile );
}

# lock with flock.
sub lock_file_flock
{
    local( $lockFile ) = @_;
    local( $LockEx ) = 2;	# magic number for exclusive lock.
    open( LOCK, ">>$lockFile" ) || return 2;
    flock( LOCK, $LockEx ) || return 0;
    1;
}
sub unlock_file_flock
{
    close LOCK;		# automatic unlock.
}


###
## Creating HTML header
#
sub Header
{
    local( $utcFlag, $utcStr, $cookieFlag, *cookieList, $cookieExpire ) = @_;
    print( "Content-type: text/html; charset=" . $CHARSET_MAP{ $CHARSET } . "\n" );
    $cgiprint'CHARSET = $CHARSET;

    # Header for HTTP Cookies.
    if ( $cookieFlag )
    {
	local( $key, $value, %urlEscapeCache );
	foreach ( @cookieList )
	{
	    # Escape unexpected chars in data.
	    ( $key, $value ) = split( /=/, $_, 2 );
	    $value =~ s/(\W)/$urlEscapeCache{$1} ||= sprintf( "%%%02X",
		ord( $1 ))/eg;
	    print( "Set-Cookie: $key=$value;" );
	    if ( $cookieExpire eq '' )
	    {
		# continue
	    }
	    elsif ( $cookieExpire =~ /^\d+$/ )
	    {
		# called by UTC.
		print( " expires=", &GetHttpDateTimeFromUtc( $cookieExpire ), ";" );
	    }
	    else
	    {
		# called by string.
		print( " expires=$cookieExpire;" );
	    }

	    print( "\n" );
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
    local( $sec, $min, $hour, $mday, $mon, $year, $wday ) = gmtime( $utc );

    # rfc1123-date
    sprintf( "%s, %02d %s %04d %02d:%02d:%02d GMT", ( 'Sun', 'Mon', 'Tue',
	'Wed', 'Thu', 'Fri', 'Sat' )[$wday], $mday, ( 'Jan', 'Feb', 'Mar',
	'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec' )[$mon],
	$year+1900, $hour, $min, $sec );
}


###
## Decoding CGI variables
## CAUTION! function decode sets global variable, TAGS.
#
sub Decode
{
    local( $args );
    if ( $ENV{ 'REQUEST_METHOD' } eq 'POST' )
    {
	local( $readSize ) = read( STDIN, $args, $ENV{ 'CONTENT_LENGTH' } );
	$args = '' if ( $readSize != $ENV{ 'CONTENT_LENGTH' } );
    }
    else			# GET, HEAD, PUT, OPTIONS, DELETE, TRACE?
    {
	$args = $QUERY_STRING;
    }

    foreach ( split( '&', $args ))
    {
	local( $key, $value ) = split( /=/, $_, 2 );
	$value =~ tr/+/ /;
	$value =~ s/%([0-9A-Fa-f][0-9A-Fa-f])/pack( "C", hex( $1 ))/ge;
	local( $encode ) = &jcode'getcode( *value );

	&jcode'convert( *value, 'euc', $encode, "z" ) if ( defined( $encode ));

	if ( @TAG_ALLOWED && !grep( /^$key$/, @TAG_ALLOWED ))
	{
	    $value = 'Tags are not allowed here...' if ( $value =~ m/[<>]/o );
	}
	    
	$value =~ s/\x0d\x0a/\x0a/go;
	$value =~ s/\x0d/\x0a/go;

	$TAGS{ $key } = $value;
    }
}


###
## Decoding HTTP-Cookies
#
sub Cookie
{
    local( $key, $value );
    foreach ( split( /;\s*/, $ENV{ 'HTTP_COOKIE' }))
    {
	( $key, $value ) = split( /=/, $_, 2 );
	$value =~ s/%([0-9A-Fa-f][0-9A-Fa-f])/pack( "C", hex( $1 ))/ge;
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
    $header = &smtpHeader( *fromName, *fromEmail, *fromName, *fromEmail,
	*subject, *extension, *labelTo, *to );

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
#	&cgi'sendMail( $fromName, $fromEmail, $senderName, $senderEmail,
#	    $subject, $extension, $message, $labelTo, @to );
#
# - ARGS
#	$fromName	from name
#	$fromEmail	from e-mail addr.
#	$senderName	sender name
#	$senderEmail	sender e-mail addr.
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
    local( $fromName, $fromEmail, $senderName, $senderEmail, $subject,
	$extension, $message, $labelTo,	@to ) = @_;
    local( $header, $body );

    return ( 0, '' ) if ( !( $fromEmail && $senderEmail && $subject &&
	$message && @to ));

    # creating header
    $header = &smtpHeader( *fromName, *fromEmail, *senderName, *senderEmail,
	*subject, *extension, *labelTo, *to );

    # creating body
    $body = &smtpBody( *message );

    # initialize connection
    &smtpInit( "S" ) || return ( 0, $SMTP_ERRSTR );

    # helo!
    &smtpMsg( "S", "helo $SERVER_NAME$CRLF" ) || return ( 0, $SMTP_ERRSTR );
    # from
    &smtpMsg( "S", "mail from: <$fromEmail>$CRLF" ) ||
	return ( 0, $SMTP_ERRSTR );
    # rcpt to
    foreach ( @to )
    {
	&smtpMsg( "S", "rcpt to: <$_>$CRLF" ) || return ( 0, $SMTP_ERRSTR );
    }
    # data block
    &smtpMsg( "S", "data$CRLF" ) || return ( 0, $SMTP_ERRSTR );
    # mail header and body
    &smtpMsg( "S", "$header$CRLF$body" . ".$CRLF" ) ||
	return ( 0, $SMTP_ERRSTR );
    # quit
    &smtpMsg( "S", "quit$CRLF" ) || return ( 0, $SMTP_ERRSTR );

    # success!
    1;
}


###
## smtpHeader - create smtp header
#
#
# - SYNOPSIS
#	&smtpHeader
#	(
#	    $fromName,		From string
#	    $fromEmail,		From addr.
#	    $senderName,	Sender string
#	    $senderEmail,	Sender addr.
#	    $subject,		Subject string
#	    $extension,		Extension-header string
#	    $labelTo,		To string
#	    @to			Recipients
#	);
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
    local( *fromName, *fromEmail, *senderName, *senderEmail, *subject,
	*extension, *labelTo, *to ) = @_;

    # mime encoding of Japanese multi-byte char in header.
    local( $encode ) = &jcode'getcode( *fromName );
    if ( defined( $encode ))
    {
	$fromName = join( $CRLF, split( /\n/, &main'mimeencode( $fromName )));
    }
    local( $from ) = "$fromName <$fromEmail>";

    $encode = &jcode'getcode( *senderName );
    if ( defined( $encode ))
    {
	$senderName = join( $CRLF, split( /\n/, &main'mimeencode( $senderName )));
    }
    local( $sender ) = "$senderName <$senderEmail>";

    $encode = &jcode'getcode( *subject );
    if ( defined( $encode ))
    {
	$subject = join( $CRLF, split( /\n/, &main'mimeencode( $subject )));
    }

    $encode = &jcode'getcode( *extension );
    if ( defined( $encode ))
    {
	$extension = join( $CRLF, split( /\n/, &main'mimeencode( $extension )));
    }

    # creating header
    local( $header ) = "To: ";
    if ( $labelTo )
    {
	$encode = &jcode'getcode( *labelTo );
	if ( defined( $encode ))
	{
	    $labelTo = join( $CRLF, split( /\n/, &main'mimeencode( $labelTo )));
	}
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
    $header .= "Sender: $sender$CRLF";
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
	close $sh;
	$SMTP_ERRSTR = $back;
	return 0;
    }
    else
    {
	return 1;
    }
}


###
## Secure TAG filter
#
# 2.16以降，SecureHtmlは解析をせず，ただタグを殺すだけにした．
# 替わりにSecureHtmlExを使う．
#
# known bugs:
#  タグの入れ子を考慮していない(例: <i><b>foo</i></b>)
#  Featureの中の「>」を考慮していない(例: ALT=">")
#
%NEED = %FEATURE = ();

sub SecureHtml
{
    local( *string ) = @_;

    $string =~ s/&/&amp;/g;
    $string =~ s/"/&quot;/g;
    $string =~ s/</&lt;/g;
    $string =~ s/>/&gt;/g;
}


sub SecureHtmlEx
{
    local( *string, *nVec, *fVec ) = @_;
    local( $srcString, $tag, $need, $feature, $markuped );

    $string =~ s/\\>/__EscapedGt\377__/go;
    $string =~ s/&amp;?/&/g;
    $string =~ s/&quot;?/"/g;
    $string =~ s/&lt;?/</g;
    $string =~ s/&gt;?/>/g;
    TAGS: while (( $tag, $need ) = each( %nVec ))
    {
	$srcString = $string;
	$string = '';
	while (( $srcString =~ m!<$tag(\s+([^>]*))?>!i ))
	{
	    $srcString = $';
	    $string .= $`;
	    if ( $2 )
	    {
		( $feature = " $2" ) =~ s/\\"/__EscapedQuote\377__/go;
	    }
	    else
	    {
		$feature = '';
	    }
	    if ( &SecureFeature( $tag, $fVec{ $tag }, $feature ))
	    {
		if ( $srcString =~ m!</$tag>!i )
		{
		    $srcString = $';
		    $markuped = $`;
		    $feature =~ s/&/__amp\377__/go;
		    $feature =~ s/"/__quot\377__/go;
		    $string .= "__$tag Open$feature\377__" . $markuped .
			"__$tag Close\377__";
		}
		elsif ( !$need )
		{
		    $feature =~ s/&/__amp\377__/go;
		    $feature =~ s/"/__quot\377__/go;
		    $string .= "__$tag Open$feature\377__";
		}
		else
		{
		    $string .= "<$tag$feature>" . $srcString;
		    # We must reset the iterator for %nVec before leaving...
		    keys( %nVec ), last TAGS;
		}
	    }
	    else
	    {
		$string .= "<$tag$feature>";
	    }
	}
	$string .= $srcString;
    }
    $string =~ s/__EscapedGt\377__/\\>/go;
    $string =~ s/__EscapedQuote\377__/\\"/go;
    $string =~ s/&/&amp;/g;
    $string =~ s/"/&quot;/g;
    $string =~ s/</&lt;/g;
    $string =~ s/>/&gt;/g;
    while (( $tag, $need ) = each( %nVec ))
    {
	$string =~ s!__$tag Open([^\377]*)\377__!<$tag$1>!g;
	$string =~ s!__$tag Close\377__!</$tag>!g;
	$string =~ s!__amp\377__!&!go;
	$string =~ s!__quot\377__!"!go;
    }
}


###
## Featureは安全か?
#
sub SecureFeature
{
    local( $tag, $allowedFeatures, $features ) = @_;

    return 1 unless $features;

    local( @allowed ) = split( /\//, $allowedFeatures );
    while ( $features =~ m/^\s*([^=\s]+)\s*=\s*('|")([^'"]*)\2/go )#'
    {
	return 0 if (( !$3 ) || ( !grep( /^$1$/i, @allowed )));
    }
    1;
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
$COLSEP = "\377";


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
#		$cgi'TAGS{'kinoT'} = 0 ... plain passwd / 1 ... encrypted
#		$cgi'TAGS{'kinoU'} = user's name
#		$cgi'TAGS{'kinoP'} = user's passwd
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
#		9 ... $ADMIN passwd is null.
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
	    return &CheckUserPasswd( $userdb, 0, $cgi'TAGS{'kinoU'},
		$cgi'TAGS{'kinoP'} );
	}
	elsif ( $cgi'COOKIES{'kinoauth'} )
	{
	    # authentication succeed if HTTP-Cookie was set.
	    local( $kinoU, $kinoP ) = split( /$COLSEP/,
		$cgi'COOKIES{'kinoauth'}, 2 );
	    if ( $kinoU ne '' )
	    {
		return &CheckUserPasswd( $userdb, 1, $kinoU, $kinoP );
	    }
	}
    }
    elsif (( $AUTH_TYPE == 2 ) && $cgi'REMOTE_USER )
    {
	# with Server Authentication

	# authentication successes if REMOTE_USER was set.
	return &CheckUserPasswd( $userdb, 2, $cgi'REMOTE_USER );
    }
    elsif (( $AUTH_TYPE == 3 ) && $cgi'TAGS{'kinoU'} )
    {
	# with direct URL Authentication

	# authentication data in TAGS.
	return &CheckUserPasswd( $userdb, ( $cgi'TAGS{'kinoT'} eq '' )? 1 : 0,
	    $cgi'TAGS{'kinoU'}, $cgi'TAGS{'kinoP'} );
    }

    # default authentication.
    return &CheckUserPasswd( $userdb, 2, $GUEST );
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
    return 0 if ( -e "$userdb" );

    # create
    open( USERDB, ">$userdb" ) || return 0;
    close USERDB;

    # add guest user with no passwd.
    if ( !defined( &AddUser( $userdb, $ADMIN, '', ())) ||
	!defined( &AddUser( $userdb, $GUEST, '', ())))
    {
	unlink( $userdb );
	return 0;
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
    while ( <USERDB> )
    {
	( $dId, $dUser ) = split( /\t/, $_, 3 );
	if ( $dUser eq $user )
	{
	    close USERDB;
	    return 1;
	}
    }
    close USERDB;

    $id = &NewId( $userdb );
    local( $salt ) = &NewSalt();
    $newLine = sprintf( "%s\t%s\t%s\t%s\t%s\t%s", $id, $user, $salt,
	substr( crypt( $passwd, $salt ), 2 ), $^T,
	( $cgi'REMOTE_HOST || $cgi'REMOTE_ADDR )); 
    foreach ( @userInfo ) { $newLine .= "\t" . $_; }
    open( USERDB, ">>$userdb" ) || return 2;
    print( USERDB $newLine . "\n" ) || return 2;
    close USERDB || return 2;

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
    local( $dId, $dUser, $dSalt, $dPasswd, $dTime, $dAddr, $dInfo );

    local( $salt ) = &NewSalt();
    open( USERDBTMP, ">$tmpFile" ) || return 0;
    open( USERDB, "<$userdb" ) || return 0;
    while ( <USERDB> )
    {
	if ( /^\#/o || /^$/o )
	{
	    print( USERDBTMP $_ ) || return 0;
	    next;
	}
	chop;
	( $dId, $dUser, $dSalt, $dPasswd, $dTime, $dAddr, $dInfo ) = split( /\t/, $_, 7 );

	if ( $dUser eq $user )
	{
	    printf( USERDBTMP "%s\t%s\t%s\t%s\t%s\t%s\t%s\n", $dId, $dUser,
		$salt, substr( crypt( $passwd, $salt ), 2 ), $^T,
		( $cgi'REMOTE_HOST || $cgi'REMOTE_ADDR ), $dInfo ) || return 0;
	    $found = 1;
	}
	else
	{
	    print( USERDBTMP $_, "\n" ) || return 0;
	}
    }
    close USERDB;
    close USERDBTMP || return 0;

    rename( $tmpFile, $userdb ) || return 0;

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
    local( $dId, $dUser, $dSalt, $dPasswd, $dTime, $dAddr );

    open( USERDBTMP, ">$tmpFile" ) || return 0;
    open( USERDB, "<$userdb" ) || return 0;
    while ( <USERDB> )
    {
	if ( /^\#/o || /^$/o )
	{
	    print( USERDBTMP $_ ) || return 0;
	    next;
	}
	chop;
	( $dId, $dUser, $dSalt, $dPasswd ) = split( /\t/, $_, 7 );

	if ( $dUser eq $user )
	{
	    printf( USERDBTMP "%s\t%s\t%s\t%s\t%s\t%s\t%s\n", $dId, $dUser,
		$dSalt, $dPasswd, $^T,
		( $cgi'REMOTE_HOST || $cgi'REMOTE_ADDR ),
		join( "\t", @userInfo )) || return 0;
	    $found = 1;
	}
	else
	{
	    print( USERDBTMP $_, "\n" ) || return 0;
	}
    }
    close USERDB;
    close USERDBTMP || return 0;

    rename( $tmpFile, $userdb ) || return 0;

    $found;
}


###
## Header - header print
#
# - SYNOPSIS
#	&cgiauth'Header( $lastModifiedP, $lastModifiedTime, $type, $expire );
#
# - ARGS
#	$lastModifiedP		print last-modified header or not.
#	$lastModifiedTime	time for last-modified header.
#				if null, now is the time for last-modified.
#	$type			not send auth-Cookies if 0.
#				send auth-Cookies if 1.
#				reset auth-Cookies if 2.
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
    local( $lastModifiedP, $lastModifiedTime, $type, $expire ) = @_;

    local( $cookieFlag, @cookieList );

    $cookieFlag = 0;

    if ( $AUTH_TYPE == 1 )
    {
	if ( $type == 0 )
	{
	    # not send
	}
	elsif (( $type == 1 ) &&
	       ( $cgi'COOKIES{'kinoauth'} ne "$UID$COLSEP$PASSWD" ))
	{
	    # set
	    push( @cookieList, "kinoauth=$UID$COLSEP$PASSWD" );
	    $cookieFlag = 1;
	}
	elsif (( $type == 2 ) && ( $cgi'COOKIES{'kinoauth'} ne '' ))
	{
	    # reset.
	    push( @cookieList, 'kinoauth=' );
	    $cookieFlag = 1;
	}
    }
	
    if ( $cookieFlag )
    {
	&cgi'Header( $lastModifiedP, $lastModifiedTime, 1, *cookieList,
	    $expire );
    }
    else
    {
	&cgi'Header( $lastModifiedP, $lastModifiedTime, 0, undef, 0 );
    }
}


###
## CheckUserPasswd - check user's name and password.
#
# - SYNOPSIS
#	&CheckUserPasswd( $userdb, $user, $passwd );
#
# - ARGS
#	$userdb		user db.
#	$checkType	0 ... plain passwd / 1 ... encrypted / 2 ... no-check
#	$user		user entry.
#	$passwd		password.
#
# - DESCRIPTION
#	check user's name and password.
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
#		9 ... $ADMIN passwd is null.
#
sub CheckUserPasswd
{
    local( $userdb, $checkType, $user, $passwd ) = @_;

    return ( 1 ) unless $user;

    return ( &UpdateUserPasswd( $userdb, $user, $passwd )) if ( $checkType == 0 );

    local( $retCode, $retUser, $retPasswd, $retRest );
    $retCode = 3;		# Means `not found'.

    local( $dId, $dUser, $dSalt, $dPasswd, $dRest );
    open( USERDB, "<$userdb" ) || return ( 2 );
    while ( <USERDB> )
    {
	next if (( $retCode != 3 ) || /^\#/o || /^$/o );
	chop;
	( $dId, $dUser, $dSalt, $dPasswd, $dRest ) = split( /\t/, $_, 5 );

	if (( $dUser eq $ADMIN ) && ( $dPasswd eq '' ))
	{
	    $retCode = 9;
	    $retUser = $dUser;
	    $retPasswd = $dPasswd;
	    $retRest = $dRest;
	    last;
	}
	elsif ( $dUser eq $user )
	{
	    if (
		# No check.
		( $checkType == 2 ) ||
		# Encrypted passwd.
		(( $checkType == 1 ) && ( $passwd eq $dPasswd )) ||
		# Plain passwd.
		(( $checkType == 0 ) &&
		 ( substr( crypt( $passwd, $dSalt ), 2 ) eq $dPasswd ))
	    )
	    {
		# authentication succeeded!
		$UID = $dUser;
		$PASSWD = $dPasswd;
		$retCode = 0;
		$retUser = $dUser;
		$retPasswd = $dPasswd;
		$retRest = $dRest;
		last;
	    }
	    else
	    {
		# authentication failed...
		$retCode = 4;
		last;
	    }
	}
    }
    close USERDB;

    return ( $retCode, $retUser, $retPasswd, split( /\t/, $retRest ));
}


###
## UpdateUserPasswd - update user's salt.
#
# - SYNOPSIS
#	&UpdateUserPasswd( $userdb, $user, $passwd );
#
# - ARGS
#	$userdb		user db.
#	$user		user entry.
#	$passwd		password.
#
# - DESCRIPTION
#	update user's salt.
#
# - RETURN
#	update user's salt and returns status, user entry, encrypted password.
#
#	status
#		0 ... succeed authentication.
#		1 ... $user is null.
#		2 ... cannot open DB file.
#		3 ... $user was not found in DB.
#		4 ... password incorrect.
#		9 ... $ADMIN passwd is null.
#
sub UpdateUserPasswd
{
    local( $userdb, $user, $passwd ) = @_;

    return ( 1 ) unless $user;

    local( $tmpFile ) = "$userdb.tmp.$$";
    local( $found ) = 0;
    local( $dId, $dUser, $dSalt, $dPasswd );

    local( $retCode, $retUser, $retPasswd, $retRest );
    $retCode = 3;		# Means `not found'.

    local( $dId, $dUser, $dSalt, $dPasswd, $dRest );
    open( USERDBTMP, ">$tmpFile" ) || return ( 2 );
    open( USERDB, "<$userdb" ) || return ( 2 );
    while ( <USERDB> )
    {
	if (( $retCode != 3 ) || /^\#/o || /^$/o )
	{
	    print( USERDBTMP $_ ) || return ( 2 );
	    next;
	}
	chop;
	( $dId, $dUser, $dSalt, $dPasswd, $dRest ) = split( /\t/, $_, 5 );

	if (( $dUser eq $ADMIN ) && ( $dPasswd eq '' ))
	{
	    $retCode = 9;
	    $retUser = $dUser;
	    $retPasswd = $dPasswd;
	    $retRest = $dRest;
	    print( USERDBTMP $_, "\n" ) || return ( 2 );
	}
	elsif ( $dUser eq $user )
	{
	    if ( substr( crypt( $passwd, $dSalt ), 2 ) eq $dPasswd )
	    {
		$dSalt = &NewSalt();
		$dPasswd = substr( crypt( $passwd, $dSalt ), 2 );
		$UID = $dUser;
		$PASSWD = $dPasswd;
		$retCode = 0;
		$retUser = $dUser;
		$retPasswd = $dPasswd;
		$retRest = $dRest;
	    }
	    else
	    {
		# authentication failed.
		$retCode = 4;
	    }
	    printf( USERDBTMP "%s\t%s\t%s\t%s\t%s\n", $dId, $dUser, $dSalt,
		$dPasswd, $dRest ) || return ( 2 );
	    $found = 1;
	}
	else
	{
	    print( USERDBTMP $_, "\n" ) || return ( 2 );
	}
    }
    close USERDB;
    close USERDBTMP || return ( 2 );

    rename( $tmpFile, $userdb ) || return ( 2 );

    return ( $retCode, $retUser, $retPasswd, split( /\t/, $retRest ));
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
    open( USERDB, "<$userdb" ) || return undef;
    while ( <USERDB> )
    {
	next if ( /^\#/o || /^$/o );
	chop;
	( $dId = $_ ) =~ s/\t.*$//o;
	$maxId = $dId if ( $dId > $maxId ) ;
    }

    ++$maxId;
}


###
## NewSalt - get new salt.
#
# - SYNOPSIS
#	&NewSalt();
#
# - DESCRIPTION
#	get new salt.
#
# - RETURN
#	returns generated new salt.
#
@SALT_STR = ( 'a' .. 'z', 'A' .. 'Z', 0 .. 9, '.', '/' );
sub NewSalt
{
    $SALT_STR[ int( rand( $#SALT_STR + 1 ))] . 
	$SALT_STR[ int( rand( $#SALT_STR + 1 ))];
}


###
## CreateNewPasswd - create password
#
# - SYNOPSIS
#	&CreateNewPasswd();
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

    while ( --$i >= 0 )
    {
	$n = 97 + int( rand( 36 ));
	$n = $n - 75 if ( $n >= 123 );
	$passwd .= sprintf( "%c", $n );
    }
    
    $passwd;
}


###
## Japanese KANJI Characters output package
#
package cgiprint;

$STR = '';
$BUFLIMIT = 4096;
$CHARSET = 'euc';

sub Init { $STR = ''; }

sub Cache
{
    for ( @_ ) { $STR .= $_; }
    &Flush() if ( length( $STR ) > $BUFLIMIT );
}

sub Flush
{
    &jcode'convert( *STR, $CHARSET ) if ( $CHARSET ne 'euc' );
    print( $STR );
    &Init();
}


#/////////////////////////////////////////////////////////////////////
1;
