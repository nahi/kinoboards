# $Id: cgi.pl,v 1.18 1997-04-02 07:30:09 nakahiro Exp $


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
# &cgi'lock($file);
#
#	$file�ǻ��ꤵ�줿�ե�����̾��Ȥ���perl program����¾��å����ޤ���
#	$mail'ARCH���ͤ˱������Ѥ����å���ˡ���ۤʤ�ޤ���
#		UNIX	����ܥ�å���󥯤ˤ���å�
#		WinNT	flock�ˤ���å�
#		Win95	��å�ɬ�פ��ʤ��ΤǤʤˤ⤷�ޤ���
#		Mac	��å�ɬ�פ��ʤ��ΤǤʤˤ⤷�ޤ���
#	��å���̵���Ԥ����1�򡤤ʤ�餫����ͳ�ǹԤ��ʤ����0���֤��ޤ���
#
#
# &cgi'unlock($file);
#
#	$file�ǻ��ꤵ�줿�ե�����̾��ȤäƤ�����줿��¾��å��򳰤��ޤ���
#	�֤��ͤϤ���ޤ���
#
#
# &cgi'Header($utc);
#
#	ɸ����Ϥ��Ф���CGI�ץ���ब�������٤�HTTP�إå�����Ϥ��ޤ���
#	$utc�ǻ��ꤵ�줿UTC���֤����ץ����κǽ��������֤ˤʤ�ޤ���
#	$utc����ά���줿���ϸ��߻��Ǥ���
#	�֤��ͤϤ���ޤ���
#
#
# &cgi'GetHttpDateTimeFromUtc($utc);
#
#	$utc�ǻ��ꤵ�줿UTC���֤��顤HTTP Date/Time�ե����ޥåȤλ���ʸ�����
#	���Ф��ޤ����֤��ͤϤ���ʸ����Ǥ���
#
#
# &cgi'Decode;
#
#	�֥饦������CGI�ץ������������줿�ե�������������ơ�
#	���뤤��URL�Υ������ѡ���(�֡�.cgi?foo=bar�פΡ���?�װʹߤ���ʬ)��
#	���Ϥ���%cgi'TAGS�˳�Ǽ���ޤ���
#	�㤨��'name'�Ȥ����ե�����ؤ��������Ƥ�$cgi'TAGS{'name'}�ǡ�
#	�֡�.cgi?foo=bar�פȤ���URL��foo���ͤ�$cgi'TAGS{'foo'}�ǡ�
#	���Ȥ��뤳�Ȥ��Ǥ��ޤ���
#	%cgi'TAGS���˲����ޤ����֤��ͤϤ���ޤ���
#
#
# &cgi'Cookie;
#
#	�֥饦������CGI�ץ������������줿HTTP Cookies����Ϥ���
#	%cgi'COOKIES�˳�Ǽ���ޤ���
#	�㤨��HTTP Cookies��'foo=bar'�Ȥ���ʸ����Ǥ���С�
#	$cgi'COOKIES{'foo'}��'bar'����Ǽ����ޤ���
#	%cgi'COOKIES���˲����ޤ����֤��ͤϤ���ޤ���
#
#
# &cgi'SendMail($fromName, $fromEmail, $subject, $extension, $message, @to);
#
#	�ᥤ����������ޤ���
#		$fromName: ������̾��(���ܸ������ʤ��Ǥ�������)
#		$fromEmail: ������E-Mail addr.
#		$subject: �ᥤ���subjectʸ����(���ܸ������ʤ��Ǥ�������)
#		$extension: �ᥤ���extension headerʸ����
#		$message: ��ʸ�Ǥ���ʸ����
#		@to: �����E-Mail addr.�Υꥹ��
#	$main'ARCH���ͤ˱������Ѥ���ᥤ��������ˡ���ۤʤ�ޤ���
#		UNIX	$main'MAIL2�ǻ��ꤷ��sendmail���ޥ��
#			(�㤨��'/usr/lib/sendmail -oi -t')��Ȥä��������ޤ���
#		WinNT	UNIX�ʳ��Ǥϥᥤ�������ϤǤ��ޤ���$main'MAIL2��
#		Win95	���ꤷ���ե�����˽񤭽Ф��ޤ���������Mac�Ǥʤ顤
#		Mac	perl5���Ѥ�cgi.pl.libnet��Ȥ��Хᥤ���������Ǥ��ޤ���
#	������̵���Ԥ����1�򡤤ʤ�餫����ͳ�ǹԤ��ʤ����0���֤��ޤ���
#
#
# &cgi'SecureHtml(*string);
#
#	*string�ǻ��ꤵ�줿ʸ����Τ��������ꤷ�������ʥ����Τߤ�Ĥ���
#	���Ȥ�HTML encode���Ƥ��ޤ��ޤ���
#	���Ѥ���Ĥ��륿������ӥե�������ϡ�@cgi'HTML_TAGS�ǻ��ꤷ�ޤ���
#	�֤��ͤϤ���ޤ���
#
#
# &cgiprint'Init;
# &cgiprint'Cache($string);
# &cgiprint'Flush;
#
#	CGI�ץ���फ��֥饦������������ʸ��������ܸ���������ɤ��Ѵ�����
#	ɸ����Ϥ��Ǥ��Ф��ޤ�����®���Τ���˥���å��嵡ǽ����äƤ��ꡤ
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


$ARCH = $main'ARCH;
$MAIL2 = $main'MAIL2;
$SERVER_NAME = $main'SERVER_NAME;
$SCRIPT_KCODE = ($main'SCRIPT_KCODE || 'euc');
$JPOUT_SCHEME = ($main'JPOUT_SCHEME || 'jis');
$WAITPID_BLOCK = ($main'WAITPID_BLOCK || 0);
$LOCK_WAIT = 10;
$LOCKFILE_TIMEOUT = .004;	# 5.76 [min]

@MONTH = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec');
@WEEK_LABEL = ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday');

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
	'FONT',		1,	'SIZE/COLOR', # Netscape Extension
	'H1',		1,	'ALIGN',
	'H2',		1,	'ALIGN',
	'H3',		1,	'ALIGN',
	'H4',		1,	'ALIGN',
	'H5',		1,	'ALIGN',
	'H6',		1,	'ALIGN',
	'HR',		0,	'SIZE/WIDTH/ALIGN', # Netscape Extension
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


###
## �͡���Initialize
#
%NEED = %FEATURE = ();

sub Init {

    # HTML_TAGS�β���
    local($Tag);
    while(@HTML_TAGS) {
	$Tag = shift(@HTML_TAGS);
	$NEED{$Tag} = shift(@HTML_TAGS);
	$FEATURE{$Tag} = shift(@HTML_TAGS);
    }

}
&Init;


###
## ��å��ط�
#

# ��å�
sub lock {
    return(&lock_UNIX(@_)) if ($ARCH eq 'UNIX');
    return(&lock_WinNT(@_)) if ($ARCH eq 'WinNT');
    return(1) if ($ARCH eq 'Win95');
    return(1) if ($ARCH eq 'Mac');
}

# �����å�
sub unlock {
    &unlock_UNIX(@_) if ($ARCH eq 'UNIX');
    &unlock_WinNT if ($ARCH eq 'WinNT');
    return if ($ARCH eq 'Win95');
    return if ($ARCH eq 'Mac');
}

# UNIX + Perl4/5
sub lock_UNIX {
    local($LockFile) = @_;
    local($TimeOut) = 0;
    local($Flag) = 0;
    srand(time|$$);
    unlink($LockFile) if (-M "$LockFile" > $LOCKFILE_TIMEOUT);
    open(LOCKORG, ">$LockFile.org") || &Fatal(1);
    for($TimeOut = 0; $TimeOut < $LOCK_WAIT; $TimeOut++) {
	$Flag = 1, last if link("$LockFile.org", $LockFile);
	select(undef, undef, undef, (rand(6)+5)/10);
    }
    unlink("$LockFile.org");
    close(LOCKORG);
    $Flag;
}

sub unlock_UNIX {
    local($LockFile) = @_;
    unlink($LockFile);
}

# WinNT + Perl5(use flock)
sub lock_WinNT {
    local($LockFile) = @_;
    local($LockEx, $LockUn) = (2, 8);
    open(LOCK, "$LockFile") || return(0);
    flock(LOCK, $LockEx);
    1;
}
sub unlock_WinNT {
    local($LockEx, $LockUn) = (2, 8);
    flock(LOCK, $LockUn);
    close(LOCK);
}


###
## HTML�إå�������
#
sub Header {

    local($Utc) = @_;

    local($LastModified) = &GetHttpDateTimeFromUtc($Utc || time);

# $ENV{'SERVER_PROTOCOL'} 200 OK
# Server: $ENV{'SERVER_SOFTWARE'}

    print(<<__EOF__);
Content-type: text/html
Last-Modified: $LastModified

__EOF__

}


###
## format as HTTP Date/Time
#
sub GetHttpDateTimeFromUtc {

    local($Utc) = @_;
    local($Sec, $Min, $Hour, $Mday, $Mon, $Year, $Wday, $Yday, $Isdst) = gmtime($Utc);
    return(sprintf("%s, %02d-%s-%02d %02d:%02d:%02d GMT", $WEEK_LABEL[$Wday], $Mday, $MONTH[$Mon], $Year, $Hour, $Min, $Sec));

}


###
## CGI�ѿ��Υǥ�����
## CAUTION! functioon decode sets global variable, TAGS.
#
sub Decode {

    local($Args, $Nread, $Tag, $Term, $Value, $Code) = ();

    ($ENV{'REQUEST_METHOD'} eq "POST")
	? ($Nread = read(STDIN, $Args, $ENV{'CONTENT_LENGTH'}))
	    : ($Args = $ENV{'QUERY_STRING'});

    foreach $Term (split('&', $Args)) {
	($Tag, $Value) = split(/=/, $Term, 2);
	$Value =~ tr/+/ /;
	$Value =~ s/%([0-9A-Fa-f][0-9A-Fa-f])/pack("C", hex($1))/ge;
	$Code = &jcode'getcode(*Value); #'
	if ($Code eq 'undef') {
	    $TAGS{$Tag} = $Value;
	} else {
	    &jcode'convert(*Value, $SCRIPT_KCODE, $Code, "z"); #'
	    $TAGS{$Tag} = $Value;
	}

        if ($ARCH eq 'Mac') {
            $TAGS{$Tag} =~ s/\xd\xa/\n/go;
            $TAGS{$Tag} =~ s/\xa/\n/go;
        } else {
	    $TAGS{$Tag} =~ s/\r\n/\n/go;
	    $TAGS{$Tag} =~ s/\r/\n/go;
	}

    }
}


###
## HTTP Cookies�Υǥ�����
#
sub Cookie {
    local($Term, $Tag, $Value);
    foreach $Term (split(";\s*", $ENV{'HTTP_COOKIE'})) {
	($Tag, $Value) = split(/=/, $Term, 2);
	$COOKIES{$Tag} = $Value;
    }
}


###
## �᡼������
#
sub SendMail {

    return(&SendMailSendmail(@_)) if ($ARCH eq 'UNIX');
    return(&SendMailFile(@_)) if ($ARCH eq 'WinNT');
    return(&SendMailFile(@_)) if ($ARCH eq 'Win95');
    return(&SendMailFile(@_)) if ($ARCH eq 'Mac');

}


###
## �᡼������(UNIX��)
#
sub SendMailSendmail {

    # �����̾���������ᥤ�륢�ɥ쥹��Subject���ղåإå���
    # ���ѵ���(0�ʤ�̵��)������ꥹ��
    # ��ʸ�ʳ��ˤ����ܸ������ʤ��褦��!
    local($FromName, $FromEmail, $Subject, $Extension, $Message, @To) = @_;
    local($Pid);

    # �����Τ��ᡤfork����
    unless ($Pid = fork()) {

	local($ToFirst) = 1;

	# �᡼���ѥե�����򳫤�
	open(MAIL, "| $MAIL2") || &Fatal(2);

	# To�إå�
	foreach (@To) {

	    if ($ToFirst) {
		print(MAIL "To: $_");
		$ToFirst = 0;
	    } else {
		print(MAIL ",\n\t$_");
	    }

	}
	print(MAIL "\n");

	# From�إå���Errors-To�إå�
	$_ = "$FromName <$FromEmail>";
	print(MAIL "From: $_\n");
	print(MAIL "Errors-To: $_\n");

	# Subject�إå�
	print(MAIL "Subject: $Subject\n");

	# �ղåإå�
	if ($Extension) {
	    &jcode'convert(*Extension, 'jis');
	    print(MAIL $Extension);
	}

	# �إå������
	print(MAIN "\n");

	# ��ʸ
	&jcode'convert(*Message, 'jis');
	print(MAIL "$Message\n");

	# ��������
	close(MAIL);
	exit(0);

    }
    waitpid($Pid, $WAITPID_BLOCK);

    # ��������
    return(! $?);

}


###
## �᡼������(Mac, Win��)
#
sub SendMailFile {

    # �����̾���������ᥤ�륢�ɥ쥹��Subject���ղåإå���
    # ���ѵ���(0�ʤ�̵��)������ꥹ��
    # ��ʸ�ʳ��ˤ����ܸ������ʤ��褦��!
    local($FromName, $FromEmail, $Subject, $Extension, $Message, @To) = @_;

    local($ToFirst) = 1;

    # �᡼���ѥե�����򳫤�
    open(MAIL, ">> $MAIL2") || &Fatal(2);

    # To�إå�
    foreach (@To) {

	if ($ToFirst) {
	    print(MAIL "To: $_");
	    $ToFirst = 0;
	} else {
	    print(MAIL ",\n\t$_");
	}

    }
    print(MAIL "\n");
    
    # From�إå���Errors-To�إå�
    $_ = "$FromName <$FromEmail>";
    print(MAIL "From: $_\n");
    print(MAIL "Errors-To: $_\n");

    # Subject�إå�
    print(MAIL "Subject: $Subject\n");

    # �ղåإå�
    if ($Extension) {
	&jcode'convert(*Extension, 'jis'); #'
	print(MAIL $Extension);
    }

    # �إå������
    print(MAIN "\n");

    # ��ʸ
    &jcode'convert(*Message, 'jis'); #'
    print(MAIL "$Message\n");

    # ���ڤ���
    print(MAIL "-------------------------------------------------------------------------------\n");

    # ��������
    close(MAIL);

    # ��������
    return(1);

}


###
## secure�ʥ����Τߤ�Ĥ�������¾��encode���롥
#
# known bugs:
#  ����������Ҥ��θ���Ƥ��ʤ�(��: <i><b>foo</i></b>)
#  Feature����Ρ�>�פ��θ���Ƥ��ʤ�(��: ALT=">")
#
sub SecureHtml {

    local(*String) = @_;
    local($SrcString) = '';
    local($Count, $BackupString, $Before, $After);
    local($Tag, $Need, $Features, $Markuped);

    $String =~ s/\\>/__EscapedGt\376__/go;
    while (($Tag, $Need) = each(%NEED)) {
	$SrcString = $String;
	$String = '';
	while (($SrcString =~ m!<$Tag\s+([^>]*)>!i) || ($SrcString =~ m!<$Tag()>!i)) {
	    $SrcString = $';
	    $String .= $`;
	    ($1) ? ($Features = " $1") =~ s/\\"/__EscapedQuote\376__/go : ($Features = '');
	    if (&SecureFeature($Tag, $Features)) {
		if ($SrcString =~ m!</$Tag>!i) {
		    $SrcString = $';
		    $Markuped = $`;
		    $Features =~ s/&/__amp\377__/go;
		    $Features =~ s/"/__quot\378__/go;
		    $String .= "__$Tag Open$Features\376__" . $Markuped . "__$Tag Close\376__";
		} elsif (! $Need) {
		    $Features =~ s/&/__amp\377__/go;
		    $Features =~ s/"/__quot\378__/go;
		    $String .= "__$Tag Open$Features\376__";
		} else {
		    $String .= "<$Tag$Features>" . $SrcString;
		    last;
		}
	    } else {
		$String .= "<$Tag$Features>";
	    }
	}
	$String .= $SrcString;
    }
    $String =~ s/__EscapedGt\376__/\\>/go;
    $String =~ s/__EscapedQuote\376__/\\"/go;
    $String =~ s/&/&amp;/g;
    $String =~ s/"/&quot;/g;
    $String =~ s/</&lt;/g;
    $String =~ s/>/&gt;/g;
    while (($Tag, $Need) = each(%NEED)) {
        $String =~ s!__$Tag Open([^\376]*)\376__!<$Tag$1>!g;
        $String =~ s!__$Tag Close\376__!</$Tag>!g;
	$String =~ s!__amp\377__!&!go;
	$String =~ s!__quot\378__!"!go;
    }
}


###
## Feature�ϰ�����?
#
sub SecureFeature {

    local($Tag, $Features) = @_;
    return(1) unless ($Features);
    local(@Allowed) = split(/\//, $FEATURE{$Tag});
    local($Ret) = 1;
    while ($Features) {
	$Feature = &GetFeatureName(*Features);
	$Value = &GetFeatureValue(*Features);
	if (! $Value) {
	    $Value = $Features;
	    $Features = '';
	}
	$Ret = 0 if (! $Feature) || (! grep(/$Feature/i, @Allowed));
    }
    $Ret;
}


###
## Feature̾�����
#
sub GetFeatureName {
    local(*String) = @_;
    $String = '' unless ($String =~ s/^\s*([^=\s]*)\s*=\s*"//);
    $1;
}


###
## Feature���ͤ����
#
sub GetFeatureValue {
    local(*String) = @_;
    $String = '' unless ($String =~ s/^([^"]*)"//);
    $1;
}


###
## ���顼ɽ��
#
sub Fatal {

    # ���顼�ֹ�ȥ��顼����μ���
    local($FatalNo) = @_;

    # ���顼��å�����
    local($ErrString);

    if ($FatalNo == 1) {

	$ErrString = "�������ͤ�: File: $LOCK_ORG��������뤳�Ȥ��Ǥ��ޤ��󡥥����ƥ�ǥ��쥯�ȥ�Υѡ��ߥå�����777�ˤʤäƤ��ޤ���?";

    } elsif ($FatalNo == 2) {

	$ErrString = "�������ͤ�: �ᥤ����������뤳�Ȥ��Ǥ��ޤ���\$MAIL2����(���ߤϡ�$MAIL2��)�����꤬������������ޤ���?";

    } else {

	$ErrString = '���顼�ֹ�����: ������Ǥ��������Υ��顼��å�����(�֥��顼�ֹ������)�Ȥ��Υڡ�����URL���ޤ����顼��������������<a href="mailto:nakahiro@kinotrope.co.jp">nakahiro@kinotrope.co.jp</a>�ޤǤ��Τ餻����������';

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
<p>$ErrString</p>
</body>
</html>
__EOF__

    &cgiprint'Flush;
    exit(0);
}


###
## ���ܸ��ɽ���ѥå�����
#
package cgiprint;

$STR = '';
$BUFLIMIT = 2048;

sub Init { $STR = ''; }

sub Cache {
    local($Str) = @_;
    $STR .= $Str;
    &Flush if (length($STR) > $BUFLIMIT);
}

sub Flush {
    &jcode'convert(*STR, $JPOUT_SCHEME);
    print($STR);
    &Init;
}


#/////////////////////////////////////////////////////////////////////
1;
