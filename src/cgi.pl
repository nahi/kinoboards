# $Id: cgi.pl,v 1.62 1998-06-19 07:46:50 nakahiro Exp $


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


# INTERFACE
#
#
# $cgi'SERVER_NAME;
#	CGI����Ư���Ƥ���WWW�����Ф�FQDN
#	�ʤ������Ǹ�Ρ�.�פ�̵��; �ʲ�Ʊ�͡ˤ����ꤵ��ޤ���
#	ex. �� www.foo.bar.jp
#
# $cgi'SERVER_PORT;
#	WWW�����Фǲ�Ư���Ƥ���httpd����ͭ�ݡ����ֹ椬���ꤵ��ޤ���
#	ex. �� 80
#
# $cgi'REMOTE_HOST;
#	CGI��ư����WWW���饤����ȡʥ֥饦���ˤ�FQDN��
#	�⤷����IP���ɥ쥹��WWW�����Ф����꼡��ˤ����ꤵ��ޤ���
#	ex. �� ika.tako.jp
#
# $cgi'SCRIPT_NAME;
#	��ư���줿CGI�Υ�����������URL�����ꤵ��ޤ���
#	ex. �� /cgi-bin/foo/bar.cgi
#
# $cgi'CGIDIR_NAME;
#	��ư���줿CGI���֤���Ƥ���ǥ��쥯�ȥ������URL�����ꤵ��ޤ���
#	ex. �� /cgi-bin/foo
#
# $cgi'CGIPROG_NAME;
#	��ư���줿CGI�Υե�����̾�ʥѥ�̾������ˤ����ꤵ��ޤ���
#	ex. �� bar.cgi
#
# $cgi'SYSDIR_NAME;
#	��ư����CGI�Υѥ�̾�ʥե�����̾������ˤ����ꤵ��ޤ���
#	ex. �� /cgi-bin/foo/
#
# $cgi'PATH_INFO;
#	CGI���ղä��줿�ѥ��������ꤵ��ޤ���
#	ex. /foo.cgi/bar/baz �� '/bar/baz'
#
# $cgi'PATH_TRANSLATED;
#	CGI���ղä��줿�ѥ������
#	�ºݤΥޥ����Υѥ����Ѵ�����ʸ�������ꤵ��ޤ���
#	ex. /foo.cgi/~foo �� '/usr/local/etc/httpd/htdocs/foo'
#
# $cgi'PROGRAM;
#	CGI�桤action�ǸƤӽФ��٤��ץ����̾�����ꤵ��ޤ���
#	ex. �� /cgi-bin/foo.cgi
#	ex. �� foo.cgi
#
# &cgi'lock( $file );
#	$file�ǻ��ꤵ�줿��å��ե�����̾��Ȥ���
#	perl program����¾Ū�˥�å����ޤ���
#	�ʥ�å�����ե��������ꤹ��ΤǤϤʤ����Ȥ���աˡ�
#	���ƥʥ󥹥�å���ʤ�
#	�ʼ¹ԥ桼���Ǻ���Ǥ��ʤ���å��ե����뤬����¸�ߤ���ʤ�ˡ�
#	2���̾�Υ�å���̵���Ԥ����1��
#	�ʤ�餫����ͳ�ǹԤ��ʤ����0���֤��ޤ���
#
#	��Win95��Mac�ǤϤ��δؿ���ƤФʤ��褦�ˤ��Ƥ���������
#	  ��å��Ǥ��ޤ���(��)��
#
# &cgi'unlock( $file );
#	$file�ǻ��ꤵ�줿��å��ե�����̾��Ȥ���
#	������줿��¾��å��򳰤��ޤ���
#	�֤��ͤϤ���ޤ���
#
# &cgi'Header( $utcFlag, $utcStr, $cookieFlag, $cookieStr );
#	ɸ����Ϥ��Ф���CGI�ץ���ब�������٤�HTTP�إå�����Ϥ��ޤ���
#	$utcFlag��0�ʳ��ξ�硤$utcStr�ǻ��ꤵ�줿UTC���֤���
#	�ץ����κǽ��������֤ˤʤ�ޤ���$utcStr�����ξ��ϸ��߻��Ǥ���
#	$cookieFlag��0�ʳ��ξ�硤$cookieStr�ǻ��ꤵ�줿ʸ���󤬡�
#	HTTP Cookies�Ȥ������֥饦���������ޤ���
#	�֤��ͤϤ���ޤ���
#
# &cgi'GetHttpDateTimeFromUtc( $utc );
#	$utc�ǻ��ꤵ�줿UTC���֤��顤HTTP Date/Time�ե����ޥåȤλ���ʸ�����
#	���Ф��ޤ����֤��ͤϤ���ʸ����Ǥ���
#	�����Ǥʤ�ʸ�����Ϳ����ȡ�
#	UNIX origin time��HTTP Date/Time�ե����ޥåȤ��֤��ޤ���
#
# &cgi'Decode;
#	�֥饦������CGI�ץ������������줿�ե�������������ơ�
#	���뤤��URL�Υ������ѡ���(�֡�.cgi?foo=bar�פΡ���?�װʹߤ���ʬ)��
#	���Ϥ���%cgi'TAGS�˳�Ǽ���ޤ���
#	�㤨��'name'�Ȥ����ե�����ؤ��������Ƥ�$cgi'TAGS{'name'}�ǡ�
#	�֡�.cgi?foo=bar�פȤ���URL��foo���ͤ�$cgi'TAGS{'foo'}�ǡ�
#	���Ȥ��뤳�Ȥ��Ǥ��ޤ���
#	%cgi'TAGS���˲����ޤ����֤��ͤϤ���ޤ���
#
# &cgi'Cookie;
#	�֥饦������CGI�ץ������������줿HTTP Cookies����Ϥ���
#	%cgi'COOKIES�˳�Ǽ���ޤ���
#	�㤨��HTTP Cookies��'foo=bar'�Ȥ���ʸ����Ǥ���С�
#	$cgi'COOKIES{'foo'}��'bar'����Ǽ����ޤ���
#	%cgi'COOKIES���˲����ޤ����֤��ͤϤ���ޤ���
#
# &cgi'sendMail( $fromName, $fromEmail, $subject, $extension, $message,
#		$labelTo, @to );
#	�ᥤ����������ޤ���
#		$fromName: ������̾��
#		$fromEmail: ������E-Mail addr.
#		$subject: �ᥤ���subjectʸ����
#		$extension: �ᥤ���extension headerʸ����
#		$message: ��ʸ�Ǥ���ʸ����
#		$labelTo: ��To:�ץإå��˻Ȥ�ʸ���󡥤�������ˤ���ȡ�
#			��To:�ץإå��ˤϡ�@to�ǻ��ꤷ�����ɥ쥹���¤Ӥޤ���
#		@to: �����E-Mail addr.�Υꥹ��
#	������̵���Ԥ����1�򡤤ʤ�餫����ͳ�ǹԤ��ʤ����0���֤��ޤ���
#	$SMTP_SERVER�˥����ФΥۥ���̾��
#	�⤷����IP���ɥ쥹����ꤷ�Ƥ����Ƥ���������
#	OS�ˤ�äƤϡ�$AF_INET��$SOCK_STREAM���ͤ��ѹ�����ɬ�פ�����ޤ���
#	$AF_INET = 2, $SOCK_STREAM = 2	... SonOS 5.*(Solaris 2.*)
#	$AF_INET = 2, $SOCK_STREAM = 1	... SunOS 4.*, HP-UX, AIX, Linux,
#					    FreeBSD, IRIX, WinNT, Mac
#
# &cgi'SecureHtml( *string );
#	*string�ǻ��ꤵ�줿ʸ����Τ��������ꤷ�������ʥ����Τߤ�Ĥ���
#	���Ȥ�HTML encode���Ƥ��ޤ��ޤ���
#	���Ѥ���Ĥ��륿������ӥե�������ϡ�@cgi'HTML_TAGS�ǻ��ꤷ�ޤ���
#	�֤��ͤϤ���ޤ���
#
# &cgiprint'Init;
# &cgiprint'Cache( $string );
# &cgiprint'Flush;
#	CGI�ץ���फ��֥饦������������ʸ�����
#	ISO-2022-jp�ʤ�����JIS�ˤ��Ѵ�����ɸ����Ϥ��Ǥ��Ф��ޤ���
#	��®���Τ���˥���å������äƤ��ޤ���
#	Init�ϥ���å���Υ��ꥢ��
#	Cache��ɽ��ʸ����Υ���å����
#	Flush�ϥ���å��夵��Ƥ���ʸ�����������Ԥ��ޤ���
#	����å��夬Ŭ���ʥ������ˤʤä��鼫ưŪ��Flush�����Τǡ�
#	����å��夷��ʸ������礭���򵤤ˤ���ɬ�פϤ���ޤ���
#	'<html><title>...</title>'�Υ���å�������˰���&cgiprint'Init���ơ�
#	��Ϥ��٤Ƥ�print��&cgiprint'Cache($string)�ˤ���
#	'</html>'�θ��&cgiprint'Flush����Ȥ褤�Ǥ��礦��
#	�֤��ͤϤ���ޤ���


require( 'jcode.pl' );
require( 'mimew.pl' );


###
## cgi�ǡ��������ϥѥå�����
#
package cgi;


$SMTP_SERVER = 'localhost';
# $SMTP_SERVER = 'mailhost';
# or
# $SMTP_SERVER = 'mailhost.foo.bar.baz.jp';
# or
# $SMTP_SERVER = '123.123.123.123';

$AF_INET = 2; $SOCK_STREAM = 1;
# AF_INET = 2, SOCK_STREAM = 1 ... SunOS 4.*, HP-UX, AIX, Linux, FreeBSD,
#					IRIX, WinNT, Mac
# AF_INET = 2, SOCK_STREAM = 2 ... SonOS 5.*(Solaris 2.*)

@HTML_TAGS = (
     # ����̾, �Ĥ�ɬ�ܤ��ݤ�, ���Ѳ�ǽ��feature
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

if (( $ENV{'SERVER_SOFTWARE'} =~ /IIS/ ) && ( $SCRIPT_NAME eq $PATH_INFO )) {
    $PATH_INFO = '';
    $PATH_TRANSLATED = '';
}

( $CGIDIR_NAME, $CGIPROG_NAME ) = $SCRIPT_NAME =~ m!^(..*)/([^/]*)$!o;
$SYSDIR_NAME = ( $PATH_INFO ? "$PATH_INFO/" : "$CGIDIR_NAME/" );
$PROGRAM = ( $PATH_INFO ? "$SCRIPT_NAME$PATH_INFO" : "$CGIPROG_NAME" );


###
## ��å��ط�
#

# ��å�
sub lock {
    local( $lockFile ) = @_;

    if ( $] =~ /^5/o ) {
	# for perl5
	return &lock_flock( $lockFile );
    }
    else {
	# for perl4
	return &lock_link( $lockFile );
    }
}

# �����å�
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
    local( $lockFlag ) = 0;
    local( $timeOut );

    # locked for maintenance by admin.
    return 2 if (( -e $lockFile ) && ( ! -w $lockFile ));

    unlink( $lockFile ) if ( -M "$lockFile" > $lockFileTimeout );

    for ( $timeOut = 0; $timeOut < $lockWait; $timeOut++ ) {
	open( LOCKORG, ">$lockFile.org" ) || return( 0 );
	close( LOCKORG );
	$lockFlag = 1, last if ( link( "$lockFile.org", $lockFile ));
	unlink( "$lockFile.org" );
	sleep 1;
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
    open( LOCK, ">>$lockFile" ) || return 2;
    flock( LOCK, $LockEx ) || return 0;

    1;
}
sub unlock_flock {

    local( $LockEx, $LockUn ) = ( 2, 8 );
    flock( LOCK, $LockUn );
    close( LOCK );
}


###
## HTML�إå�������
#
# $ENV{'SERVER_PROTOCOL'} 200 OK
# Server: $ENV{'SERVER_SOFTWARE'}
sub Header {
    local( $utcFlag, $utcStr, $cookieFlag, $cookieStr ) = @_;

    print( "Content-type: text/html\n" );

    # Header for HTTP Cookies.
    printf( "Set-Cookie: $cookieStr; domain=%s; path=%s\n", $SERVER_NAME,
	$CGIDIR_NAME ) if ( $cookieFlag );

    # Header for Last-Modified.
    printf( "Last-Modified: %s\n", &GetHttpDateTimeFromUtc( $utcStr || $^T ))
	if ( $utcFlag );

    # now, the end of Head Block.
    print( "\n" );

}


###
## format as HTTP Date/Time
#
sub GetHttpDateTimeFromUtc {
    local( $utc ) = @_;

    $utc = 0 if ( $utc !~ /^\d+$/ );
    local( $sec, $min, $hour, $mday, $mon, $year, $wday ) = gmtime( $utc );

    sprintf( "%s, %02d-%s-%02d %02d:%02d:%02d GMT", ( 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday' )[ $wday ], $mday, ( 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec' )[ $mon ], $year, $hour, $min, $sec );
}


###
## CGI�ѿ��Υǥ�����
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

	$TAGS{ $key } =~ s/\xd\xa/\xa/go;
	$TAGS{ $key } =~ s/\xd/\xa/go;
    }
}


###
## HTTP Cookies�Υǥ�����
#
sub Cookie {

    local( $key, $value, $term );
    foreach $term ( split( ";\s*", $ENV{ 'HTTP_COOKIE' })) {
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
sub SendMail {
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
    &smtpMsg( "S", "helo $SERVER_NAME\r\n" ) || return 0;
    # from
    &smtpMsg( "S", "mail from: <$fromEmail>\r\n" ) || return 0;
    # rcpt to
    foreach ( @to ) {
	&smtpMsg( "S", "rcpt to: <$_>\r\n" ) || return 0;
    }
    # data block
    &smtpMsg( "S", "data\r\n" ) || return 0;
    # mail header and body
    &smtpMsg( "S", "$header" . "\r\n" . "$body" . "." . "\r\n" ) || return 0;
    # quit
    &smtpMsg( "S", "quit\r\n" ) || return 0;

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
sub sendMail {
    local( $fromName, $fromEmail, $subject, $extension, $message, $labelTo,
	@to ) = @_;

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
    &smtpMsg( "S", "helo $SERVER_NAME\r\n" ) || return 0;
    # from
    &smtpMsg( "S", "mail from: <$fromEmail>\r\n" ) || return 0;
    # rcpt to
    foreach ( @to ) {
	&smtpMsg( "S", "rcpt to: <$_>\r\n" ) || return 0;
    }
    # data block
    &smtpMsg( "S", "data\r\n" ) || return 0;
    # mail header and body
    &smtpMsg( "S", "$header" . "\r\n" . "$body" . "." . "\r\n" ) || return 0;
    # quit
    &smtpMsg( "S", "quit\r\n" ) || return 0;

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
sub smtpHeader {
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
    if ( $labelTo ) {
	$encode = &jcode'getcode( *labelTo );
	$labelTo = &main'mimeencode( $labelTo ) if ( defined( $encode ));
	$header .= "$labelTo\r\n";
    }
    else {
	# should we encode those with MIME Base64?
	$header .= join( ",\r\n\t", @to );
	$header .= "\r\n";
    }
    $header .= "From: $from\r\n";
    $header .= "Reply-To: $from\r\n";
    $header .= "Sendar: $from\r\n";
    $header .= "Subject: $subject\r\n";
    $header .= "Content-type: text/plain; charset=ISO-2022-JP\r\n";
    if ( $extension ) {
	$header .= join( "\r\n", split( /\n/, $extension ));
	$header .= "\r\n";
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
sub smtpBody {
    local( *message ) = @_;

    local( $body ) = '';

    &jcode'convert( *message, 'jis' );
    foreach ( split( /\n/, $message )) {
	s/^\.$/\.\./o;		# `.' is the end of the message.
	$body .= "$_\r\n";
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
sub smtpInit {
    local( $sh ) = @_;

    local( $sockAddr ) = 'S n a4 x8';
    local( $smtpPort ) = 'smtp';		# 25
    local( $proto, $port, $smtpAddr, $sock, $oldStream );

    # preparing for smtp connection...
    $proto = ( getprotobyname( 'tcp' ))[2];
    $port = ( $smtpPort =~ /^\d+$/ ) ? $smtpPort : ( getservbyname( $smtpPort,
	'tcp' ))[2];
    if ( $SMTP_SERVER =~ /^(\d+)\.(\d+)\.(\d+)\.(\d+)$/ ) {
	$smtpAddr = pack( 'C4', $1, $2, $3, $4 );
    }
    else {
	$smtpAddr = ( gethostbyname( $SMTP_SERVER ))[4];
    }
    return 0 if ( !$smtpAddr );
    $sock = pack( $sockAddr, $AF_INET, $port, $smtpAddr );

    # create connection...
    socket( $sh, $AF_INET, $SOCK_STREAM, $proto ) || return 0;
    connect( $sh, $sock ) || return 0;
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
#	$message	message with \r\n
#
# - DESCRIPTION
#	send a message to MTA and check the result.
#
# - RETURN
#	1 if succeed, 0 if failed.
#
sub smtpMsg {
    local( $sh, $message ) = @_;

    local( $back );

    print( $sh $message ) if $message;
    $back = <${sh}>;
    if ( $back =~ /^[45]/o ) {
	close( $sh );
	return 0;
    }
    else {
	return 1;
    }
}


###
## secure�ʥ����Τߤ�Ĥ�������¾��encode���롥
#
# known bugs:
#  ����������Ҥ��θ���Ƥ��ʤ�(��: <i><b>foo</i></b>)
#  Feature����Ρ�>�פ��θ���Ƥ��ʤ�(��: ALT=">")
#
$F_HTML_TAGS_PARSED = 0;
%NEED = %FEATURE = ();

sub SecureHtml {
    local( *string ) = @_;

    local( $srcString, $tag, $need, $feature, $markuped );

    # HTML_TAGS�β��ϡʰ��٤����»ܡ�
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
	while (( $srcString =~ m!<$tag\s+([^>]*)>!i ) || ( $srcString =~
		m!<$tag()>!i) ) {
	    $srcString = $';
	    $string .= $`;
	    if ( $1 ) {
		( $feature = " $1" ) =~ s/\\"/__EscapedQuote\376__/go;
	    }
	    else {
		$feature = '';
	    }
	    if ( &SecureFeature( $tag, $FEATURE{ $tag }, $feature )) {
		if ( $srcString =~ m!</$tag>!i ) {
		    $srcString = $';
		    $markuped = $`;
		    $feature =~ s/&/__amp\376__/go;
		    $feature =~ s/"/__quot\376__/go;
		    $string .= "__$tag Open$feature\376__" . $markuped .
			"__$tag Close\376__";
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
## Feature�ϰ�����?
#
sub SecureFeature {
    local( $tag, $allowedFeatures, $features ) = @_;

    local( @allowed, $feature, $ret );

    return 1 unless ( $features );
    @allowed = split( /\//, $allowedFeatures );
    $ret = 1;

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
## Feature̾�����
#
sub GetFeatureName {
    local( *string ) = @_;
    $string = '' unless ( $string =~ s/^\s*([^=\s]*)\s*=\s*"// );
    $1;
}


###
## Feature���ͤ����
#
sub GetFeatureValue {
    local( *string ) = @_;
    $string = '' unless ( $string =~ s/^([^"]*)"// );
    $1;
}


###
## ���ܸ��ɽ���ѥå�����
#
package cgiprint;

$STR = '';
$BUFLIMIT = 4096;

sub Init { $STR = ''; }

sub Cache {
    $STR .= shift;
    &Flush if ( length( $STR ) > $BUFLIMIT );
}

sub Flush {
    &jcode'convert( *STR, 'jis' );
    print( $STR );
    &Init;
}


#/////////////////////////////////////////////////////////////////////
1;
