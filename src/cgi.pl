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
#	���夵��ˤ�����ܸ�����������Ѵ��桼�ƥ���ƥ���jcode.pl��
#	v2.0�ʹߤ�ɬ�פǤ����ʲ���URL�������ꤷ�Ƥ���������
#	<URL:ftp://ftp.sra.co.jp/pub/lang/perl/sra-scripts/>
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
#	$file�ǻ��ꤵ�줿�ե�����̾��Ȥ���perl program����¾��å����ޤ���
#	$mail'ARCH���ͤ˱������Ѥ����å���ˡ���ۤʤ�ޤ���
#		UNIX	����ܥ�å���󥯤ˤ���å�
#		WinNT	flock�ˤ���å�
#		Win95	flock�ˤ���å�
#		Mac	��å���ɬ�פ��ʤ��Τǡʤۤ��?�ˤʤˤ⤷�ޤ���
#	���ƥʥ󥹥�å���ʤ�
#	�ʼ¹ԥ桼���Ǻ���Ǥ��ʤ���å��ե����뤬����¸�ߤ���ʤ�ˡ�
#	2���̾�Υ�å���̵���Ԥ����1��
#	�ʤ�餫����ͳ�ǹԤ��ʤ����0���֤��ޤ���
#
# &cgi'unlock( $file );
#	$file�ǻ��ꤵ�줿�ե�����̾��ȤäƤ�����줿��¾��å��򳰤��ޤ���
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
#	$ARCH���ͤ˱������Ѥ���ᥤ��������ˡ���ۤʤ�ޤ���
#		UNIX	$MAIL2�ǻ��ꤷ��sendmail���ޥ��
#			(�㤨��'/usr/lib/sendmail -oi -t')��Ȥä��������ޤ���
#		WinNT	UNIX�ʳ��Ǥϥᥤ�������ϤǤ��ޤ���$MAIL2��
#		Win95	���ꤷ���ե�����˽񤭽Ф��ޤ���
#		Mac	perl5���Ѥ�cgi.pl.libnet��Ȥ���
#			MacPerl5��libnet for Mac���Ȥ߹�碌�ǡ�
#			�ᥤ��������Ԥ��ޤ���$SERVER_NAME��CGI��ư����
#			�ۥ���̾��$MAIL2�˥ᥤ�륵���ФΥۥ���̾��
#			���ꤷ�Ƥ���������
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
#	CGI�ץ���फ��֥饦������������ʸ��������ܸ���������ɤ��Ѵ�����
#	ɸ����Ϥ��Ǥ��Ф��ޤ���
#	��®���Τ���˥���å��嵡ǽ����äƤ��ꡤ
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
## ��å��ط�
#

# ��å�
sub lock {
    local( $lockFile ) = @_;

    # locked for maintenance by admin.
    return( 2 ) if (( -e $lockFile ) && ( ! -w $lockFile ));

    return( &lock_link( $lockFile )) if ( $ARCH eq 'UNIX' );
    return( &lock_flock( $lockFile )) if ( $ARCH eq 'WinNT' || $ARCH eq 'Win95' );
    return( 1 ) if ( $ARCH eq 'Mac' );
}

# �����å�
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
## CGI�ѿ��Υǥ�����
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
## �᡼������
#
sub SendMail {

    return( &SendMailSendmail( @_ )) if ( $ARCH eq 'UNIX' );
    return( &SendMailFile( @_ )) if ( $ARCH eq 'WinNT' );
    return( &SendMailFile( @_ )) if ( $ARCH eq 'Win95' );
    return( &SendMailFile( @_ )) if ( $ARCH eq 'Mac' );

}


###
## �᡼������(UNIX��)
#
# ��ʸ�ʳ��ˤ����ܸ������ʤ��褦��!
sub SendMailSendmail {
    local( $fromName, $fromEmail, $subject, $extension, $message, @to ) = @_;
    local( $pid );
    local( $toFirst ) = 1;
    local( $from ) = "$fromName <$fromEmail>";

    # �����Τ��ᡤfork����
    unless ( $pid = fork() ) {

	open( MAIL, "| $MAIL2" ) || &Fatal( 2 );

	# To�إå�
	foreach ( @to ) {
	    if ( $toFirst ) {
		print( MAIL "To: $_" );
		$toFirst = 0;
	    } else {
		print( MAIL ",\n\t$_" );
	    }

	}
	print( MAIL "\n" );

	# From�إå���Errors-To�إå�
	print( MAIL "From: $from\n" );
	print( MAIL "Errors-To: $from\n" );

	# Subject�إå�
	print( MAIL "Subject: $subject\n" );

	# �ղåإå�
	if ( $extension ) {
	    &jcode'convert( *extension, 'jis' );
	    print( MAIL $extension );
	}

	# �إå������
	print( MAIN "\n" );

	# ��ʸ
	&jcode'convert( *message, 'jis' );
	print( MAIL "$message\n" );

	# ��������
	close( MAIL );
	exit( 0 );

    }
    waitpid( $pid, $WAITPID_BLOCK );

    # ��������
    !$?;

}


###
## �᡼������(Mac, Win��)
#
# ��ʸ�ʳ��ˤ����ܸ������ʤ��褦��!
sub SendMailFile {
    local( $fromName, $fromEmail, $subject, $extension, $message, @to) = @_;
    local( $toFirst ) = 1;
    local( $from ) = "$fromName <$fromEmail>";

    # �᡼���ѥե�����򳫤�
    &Fatal( 2 ) if ( $MAIL2 eq '' );
    open( MAIL, ">> $MAIL2" ) || &Fatal( 2 );

    # To�إå�
    foreach ( @to ) {
	if ( $toFirst ) {
	    print( MAIL "To: $_" );
	    $toFirst = 0;
	} else {
	    print( MAIL ",\n\t$_" );
	}
    }
    print(MAIL "\n");
    
    # From�إå���Errors-To�إå�
    print( MAIL "From: $from\n" );
    print( MAIL "Errors-To: $from\n" );

    # Subject�إå�
    print( MAIL "Subject: $subject\n" );

    # �ղåإå�
    if ( $extension ) {
	&jcode'convert( *extension, 'jis' );
	print( MAIL $extension );
    }

    # �إå������
    print( MAIN "\n" );

    # ��ʸ
    &jcode'convert( *message, 'jis' );
    print( MAIL "$message\n" );

    # ���ڤ���
    print( MAIL "-------------------------------------------------------------------------------\n" );

    # ��������
    close( MAIL );

    # ��������
    1;

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
	local( @htmlTags ) =
	    (
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
## ���顼ɽ��
#
sub Fatal {

    # ���顼�ֹ�ȥ��顼����μ���
    local( $errno ) = @_;

    # ���顼��å�����
    local( $errString );

    if ( $errno == 1 ) {

	$errString = "�������ͤ�: File: $LOCK_ORG��������뤳�Ȥ��Ǥ��ޤ��󡥥����ƥ�ǥ��쥯�ȥ�Υѡ��ߥå�����777�ˤʤäƤ��ޤ���?";

    } elsif ( $errno == 2 ) {

	$errString = "�������ͤ�: �ᥤ����������뤳�Ȥ��Ǥ��ޤ���\$MAIL2����(���ߤϡ�$MAIL2��)�����꤬������������ޤ���?";

    } else {

	$errString = '���顼�ֹ�����: ������Ǥ��������Υ��顼��å�����(�֥��顼�ֹ������)�Ȥ��Υڡ�����URL���ޤ����顼��������������<a href="mailto:nakahiro@kinotrope.co.jp">nakahiro@kinotrope.co.jp</a>�ޤǤ��Τ餻����������';

    }

    # ɽ�����̤κ���
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
## ���ܸ��ɽ���ѥå�����
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
