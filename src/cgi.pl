# $Id: cgi.pl,v 1.16 1997-02-14 11:44:04 nakahiro Exp $


# Small CGI tool package(use this with jcode.pl-2.0).
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
## cgi用パッケージ
#
package cgi;

require('jcode.pl');

$ARCH = $main'ARCH;
$MAIL2 = $main'MAIL2;
$MAILHOST = $main'MAILHOST;
$MAILTOUT = $main'MAILTOUT;
$SCRIPT_KCODE = ($main'SCRIPT_KCODE || 'euc');
$JPOUT_SCHEME = ($main'JPOUT_SCHEME || 'jis');
$WAITPID_BLOCK = ($main'WAITPID_BLOCK || 0);

@MONTH = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec');
@WEEK_LABEL = ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday');


###
## HTMLヘッダの生成
#
sub header {

    local($Utc) = @_;

    local($LastModified) = &GetHttpDateTimeFromUtc($Utc);

    print(<<__EOF__);
Content-type: text/html

__EOF__

#    print(<<__EOF__);
#Content-type: text/html
#Last-Modified: $LastModified
#
#__EOF__

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
## CGI変数のデコード
## CAUTION! functioon decode sets global variable, TAGS.
#
sub decode {

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
## Cookie変数のデコード
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
## 日本語の表示
#
sub KPrint {

    local($String) = @_;
    &jcode'convert(*String, $JPOUT_SCHEME);
    print($String);

}


###
## メール送信
#
sub SendMail {

    return(&SendMailSendmail(@_)) if ($ARCH eq 'UNIX');
    return(&SendMailFile(@_)) if ($ARCH eq 'WinNT');
    return(&SendMailFile(@_)) if ($ARCH eq 'Win95');
    return(&SendMailFile(@_)) if ($ARCH eq 'Mac');

}


###
## メール送信(UNIX用)
#
sub SendMailSendmail {

    # 送り主名前，送り主メイルアドレス，Subject，付加ヘッダ，
    # 引用記事(0なら無し)，宛先リスト
    # 本文以外には日本語を入れないように!
    local($FromName, $FromEmail, $Subject, $Extension, $Message, @To) = @_;
    local($Pid);

    # 安全のため，forkする
    unless ($Pid = fork()) {

	local($ToFirst) = 1;

	# メール用ファイルを開く
	open(MAIL, "| $MAIL2") || die;

	# Toヘッダ
	foreach (@To) {

	    if ($ToFirst) {
		print(MAIL "To: $_");
		$ToFirst = 0;
	    } else {
		print(MAIL ",\n\t$_");
	    }

	}
	print(MAIL "\n");

	# Fromヘッダ，Errors-Toヘッダ
	$_ = "$FromName <$FromEmail>";
	print(MAIL "From: $_\n");
	print(MAIL "Errors-To: $_\n");

	# Subjectヘッダ
	print(MAIL "Subject: $Subject\n");

	# 付加ヘッダ
	if ($Extension) {
	    &jcode'convert(*Extension, 'jis');
	    print(MAIL $Extension);
	}

	# ヘッダ終わり
	print(MAIN "\n");

	# 本文
	&jcode'convert(*Message, 'jis');
	print(MAIL "$Message\n");

	# 送信する
	close(MAIL);
	exit(0);

    }
    waitpid($Pid, $WAITPID_BLOCK);

    # 送信した
    return(! $?);

}


###
## メール送信(Mac, Win用)
#
sub SendMailFile {

    # 送り主名前，送り主メイルアドレス，Subject，付加ヘッダ，
    # 引用記事(0なら無し)，宛先リスト
    # 本文以外には日本語を入れないように!
    local($FromName, $FromEmail, $Subject, $Extension, $Message, @To) = @_;

    local($ToFirst) = 1;

    # メール用ファイルを開く
    open(MAIL, ">> $MAIL2") || die;

    # Toヘッダ
    foreach (@To) {

	if ($ToFirst) {
	    print(MAIL "To: $_");
	    $ToFirst = 0;
	} else {
	    print(MAIL ",\n\t$_");
	}

    }
    print(MAIL "\n");
    
    # Fromヘッダ，Errors-Toヘッダ
    $_ = "$FromName <$FromEmail>";
    print(MAIL "From: $_\n");
    print(MAIL "Errors-To: $_\n");

    # Subjectヘッダ
    print(MAIL "Subject: $Subject\n");

    # 付加ヘッダ
    if ($Extension) {
	&jcode'convert(*Extension, 'jis'); #'
	print(MAIL $Extension);
    }

    # ヘッダ終わり
    print(MAIN "\n");

    # 本文
    &jcode'convert(*Message, 'jis'); #'
    print(MAIL "$Message\n");

    # 区切り線
    print(MAIL "-------------------------------------------------------------------------------\n");

    # 送信する
    close(MAIL);

    # 送信した
    return(1);

}


#/////////////////////////////////////////////////////////////////////
1;
