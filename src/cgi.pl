# $Id: cgi.pl,v 1.12 1996-11-19 12:06:35 nakahiro Exp $


# Small CGI tool package
# Copyright (C) 1995, 96 NAKAMURA Hiroshi.
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


###
## cgi�ѥѥå�����
#
package cgi;

$MAIL2 = ((defined $'MAIL2) ? $'MAIL2 : "/usr/lib/sendmail -oi -t");
$JPOUT_SCHEME = ((defined $'JPOUT_SCHEME) ? $'JPOUT_SCHEME : 'jis');
$WAITPID_BLOCK = ((defined $'WAITPID_BLOCK) ? $'WAITPID_BLOCK : 0);


###
## HTML�إå�������
#
sub header {
    print "Content-type: text/html\n\n";
}


###
## CGI�ѿ��Υǥ�����
## CAUTION! functioon decode sets global variable, TAGS.
#
sub decode {

    local($Args, $Nread, $Tag, $Term, $Value) = ('', '', '', '', '');

    ($ENV{'REQUEST_METHOD'} eq "POST")
	? ($Nread = read(STDIN, $Args, $ENV{'CONTENT_LENGTH'}))
	    : ($Args = $ENV{'QUERY_STRING'});

    foreach $Term (split('&', $Args)) {
	($Tag, $Value) = split(/=/, $Term, 2);
	$Value =~ tr/+/ /;
	$Value =~ s/%([0-9A-Fa-f][0-9A-Fa-f])/pack("C", hex($1))/ge;
	unless ($Value =~ /[\033\200-\377]/) {
	    $TAGS{$Tag} = $Value;
	} else {
	    &jcode'convert(*Value, 'euc');
	    $TAGS{$Tag} = $Value;
	}
	$TAGS{$Tag} =~ s/\r\n/\n/go;
	$TAGS{$Tag} =~ s/\r/\n/go;
    }
}


###
## Cookie�ѿ��Υǥ�����
#
sub cookie {

    local(@QUERY, $Tag, $Value);
    @QUERY = split(";\s*", $ENV{'HTTP_COOKIE'});
    foreach (@QUERY) {
	($Tag, $Value) = split(/=/, $_, 2);
	eval("\$$Tag = \"$Value\";");
    }
}


###
## ���ܸ��ɽ��
#
sub KPrint {

    local($String) = @_;
    &jcode'convert(*String, $JPOUT_SCHEME);
    print($String);

}


###
## �᡼������(���������1�����Ԥ����0���֤�)
#
sub SendMail {

    # �����̾���������ᥤ�륢�ɥ쥹��Subject���ղåإå���
    # ���ѵ���(0�ʤ�̵��)������ꥹ��
    # ��ʸ�ʳ��ˤ����ܸ������ʤ��褦��!
    local($FromName, $FromEmail, $Subject, $Extension, $Message, @To) = @_;

    local($Pid);

    # �����Τ��ᡤfork����
    unless ($Pid = fork()) {

	local($ToFirst) = 1;

	# �᡼���ѥե�����򳫤�
	open(MAIL, "| $MAIL2") || die;

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


#/////////////////////////////////////////////////////////////////////
1;
