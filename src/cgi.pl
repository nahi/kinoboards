# $Id: cgi.pl,v 1.17 1997-03-13 15:20:41 nakahiro Exp $


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


require('jcode.pl');


###
## cgiデータ入出力パッケージ
#
package cgi;


$ARCH = $main'ARCH;
$MAIL2 = $main'MAIL2;
$SCRIPT_KCODE = ($main'SCRIPT_KCODE || 'euc');
$JPOUT_SCHEME = ($main'JPOUT_SCHEME || 'jis');
$WAITPID_BLOCK = ($main'WAITPID_BLOCK || 0);
$LOCK_WAIT = 10;
$LOCKFILE_TIMEOUT = .004;	# 5.76 [min]

@MONTH = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec');
@WEEK_LABEL = ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday');

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
## 様々なInitialize
#
%NEED = %FEATURE = ();

sub Init {

    # HTML_TAGSの解析
    local($Tag);
    while(@HTML_TAGS) {
	$Tag = shift(@HTML_TAGS);
	$NEED{$Tag} = shift(@HTML_TAGS);
	$FEATURE{$Tag} = shift(@HTML_TAGS);
    }

}
&Init;


###
## ロック関係
#

# ロック
sub lock {
    return(&lock_UNIX(@_)) if ($ARCH eq 'UNIX');
    return(&lock_WinNT(@_)) if ($ARCH eq 'WinNT');
    return(1) if ($ARCH eq 'Win95');
    return(1) if ($ARCH eq 'Mac');
}

# アンロック
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
## HTMLヘッダの生成
#
sub Header {

    local($Utc) = @_;

#    local($LastModified) = &GetHttpDateTimeFromUtc($Utc || time);

# $ENV{'SERVER_PROTOCOL'} 200 OK
# Server: $ENV{'SERVER_SOFTWARE'}
# Last-Modified: $LastModified

    print(<<__EOF__);
Content-type: text/html

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
## CGI変数のデコード
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
## Cookie変数のデコード
#
sub Cookie {

    local(@QUERY, $Tag, $Value);
    @QUERY = split(";\s*", $ENV{'HTTP_COOKIE'});
    foreach (@QUERY) {
	($Tag, $Value) = split(/=/, $_, 2);
	eval("\$$Tag = \"$Value\";");
    }
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
	open(MAIL, "| $MAIL2") || &Fatal(2);

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
    open(MAIL, ">> $MAIL2") || &Fatal(2);

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


###
## secureなタグのみを残し，その他をencodeする．
#
# known bugs:
#  タグの入れ子を考慮していない(例: <i><b>foo</i></b>)
#  Featureの中の「>」を考慮していない(例: ALT=">")
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
## Featureは安全か?
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
## Feature名を取得
#
sub GetFeatureName {
    local(*String) = @_;
    $String = '' unless ($String =~ s/^\s*([^=\s]*)\s*=\s*"//);
    $1;
}


###
## Featureの値を取得
#
sub GetFeatureValue {
    local(*String) = @_;
    $String = '' unless ($String =~ s/^([^"]*)"//);
    $1;
}


###
## エラー表示
#
sub Fatal {

    # エラー番号とエラー情報の取得
    local($FatalNo) = @_;

    # エラーメッセージ
    local($ErrString);

    if ($FatalNo == 1) {

	$ErrString = "管理者様へ: File: $LOCK_ORGを作成することができません．システムディレクトリのパーミッションは777になっていますか?";

    } elsif ($FatalNo == 2) {

	$ErrString = "管理者様へ: メイルを送信することができません．\$MAIL2の値(現在は「$MAIL2」)の設定がおかしくありませんか?";

    } else {

	$ErrString = 'エラー番号不定: お手数ですが，このエラーメッセージ(「エラー番号不定」)とこのページのURL，またエラーが生じた状況を，<a href="mailto:nakahiro@kinotrope.co.jp">nakahiro@kinotrope.co.jp</a>までお知らせください．';

    }

    # 表示画面の作成
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
## 日本語の表示パッケージ
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
