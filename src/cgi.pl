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
#	���夵��ˤ�����ܸ�����������Ѵ��桼�ƥ���ƥ���jcode.pl��
#	v2.0�ʹߤ�ɬ�פǤ����ʲ���URL�������ꤷ�Ƥ���������
#	<URL:ftp://ftp.iij.ad.jp/pub/IIJ/dist/utashiro/perl/>
#
#
#
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
# &cgi'SendMail( $fromName, $fromEmail, $subject, $extension, $message, @to );
#	�ᥤ����������ޤ���
#		$fromName: ������̾��(���ܸ������ʤ��Ǥ�������)
#		$fromEmail: ������E-Mail addr.
#		$subject: �ᥤ���subjectʸ����(���ܸ������ʤ��Ǥ�������)
#		$extension: �ᥤ���extension headerʸ����
#		$message: ��ʸ�Ǥ���ʸ����
#		@to: �����E-Mail addr.�Υꥹ��
#	$SMTP_SERVER�˥����ФΥۥ���̾��
#	�⤷����IP���ɥ쥹����ꤷ�Ƥ����Ƥ���������
#	OS�ˤ�äƤϡ�$AF_INET��$SOCK_STREAM���ͤ��ѹ�����ɬ�פ�����ޤ���
#	������̵���Ԥ����1�򡤤ʤ�餫����ͳ�ǹԤ��ʤ����0���֤��ޤ���
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


require('jcode.pl');


###
## cgi�ǡ��������ϥѥå�����
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

($CGIDIR_NAME, $CGIPROG_NAME) = $SCRIPT_NAME =~ m!^(..*)/([^/]*)$!o;
$SYSDIR_NAME = (($PATH_INFO) ? "$PATH_INFO/" : "$CGIDIR_NAME/");
$PROGRAM = (($PATH_INFO) ? "$SCRIPT_NAME$PATH_INFO" : "$CGIPROG_NAME");


###
## ��å��ط�
#

# ��å�
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
## HTML�إå�������
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

	$TAGS{ $key } =~ s/\0x0d\0x0a/\0x0a/go;
	$TAGS{ $key } =~ s/\0x0d/\0x0a/go;
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
    local( $srcString ) = '';
    local( $tag, $need, $feature, $markuped );

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
## Feature�ϰ�����?
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
