# $Id: cgi.pl,v 1.4 1996-08-20 09:44:48 nakahiro Exp $


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
## cgi用パッケージ
#
package cgi;
$MAIL2 = ((defined $'MAIL2) ? $'MAIL2 : "/usr/lib/sendmail -oi -t");


###
## HTMLヘッダの生成
#
sub header {
    print "Magnus-charset: x-euc-jp\n";
    print "Content-type: text/html\n\n";
}


###
## CGI変数のデコード
## CAUTION! functioon decode sets global variable, TAGS.
#
sub decode {

    local($args, $n_read, $tag, $value);

    ($ENV{'REQUEST_METHOD'} eq "POST")
	? ($n_read = read(STDIN, $args, $ENV{'CONTENT_LENGTH'}))
	    : ($args = $ENV{'QUERY_STRING'});

    foreach (split('&', $args)) {
	($tag, $value) = split(/=/, $_, 2);
	$value =~ tr/+/ /;
	$value =~ s/%([0-9A-Fa-f][0-9A-Fa-f])/pack("C", hex($1))/ge;
	$_ = $value;
	unless (/[\033\200-\377]/) {
	    $TAGS{$tag} = $value;
	} else {
	    &jcode'convert(*_, 'euc');
	    $TAGS{$tag} = $_;
	}
	$TAGS{$tag} =~ s/\r\n/\n/go;
	$TAGS{$tag} =~ s/\r/\n/go;
    }
}


###
## Cookie変数のデコード
#
sub cookie {

    local(@QUERY);
    @QUERY = split(";\s*", $ENV{'HTTP_COOKIE'});
    foreach (@QUERY) { eval "\$$_;"; }

}


###
## メール送信(成功すると1，失敗すると0を返す)
#
sub SendMail {

    # subject，メールのファイル名，引用記事(0なら無し)，宛先
    # 本文以外には日本語を入れないように!
    local($FromName, $FromEmail, $Subject, $Message, @To) = @_;

    local($ToFirst) = 1;

    # メール用ファイルを開く
    open(MAIL, "| $MAIL2") || return(0);

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
    print(MAIL "Subject: $Subject\n\n");

    # 本文
    &jcode'convert(*Message, 'jis');
    print(MAIL "$Message\n");

    # 送信する
    close(MAIL);

    # 送信した
    return(1);

}


#/////////////////////////////////////////////////////////////////////
1;
