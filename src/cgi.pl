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
#	歌代さんによる日本語漢字コード変換ユーティリティ，jcode.plの
#	v2.0以降が必要です．以下のURLから入手してください．
#	<URL:ftp://ftp.sra.co.jp/pub/lang/perl/sra-scripts/>
#
#
#
# INTERFACE
#
#
# &cgi'lock($file);
#
#	$fileで指定されたファイル名を使い，perl programを排他ロックします．
#	$mail'ARCHの値に応じ，用いるロック手法が異なります．
#		UNIX	シンボリックリンクによるロック
#		WinNT	flockによるロック
#		Win95	ロック必要がないのでなにもしません
#		Mac	ロック必要がないのでなにもしません
#	ロックが無事行えれば1を，なんらかの理由で行えなければ0を返します．
#
#
# &cgi'unlock($file);
#
#	$fileで指定されたファイル名を使ってかけられた排他ロックを外します．
#	返り値はありません．
#
#
# &cgi'Header($utc);
#
#	標準出力に対し，CGIプログラムが送信すべきHTTPヘッダを出力します．
#	$utcで指定されたUTC時間が，プログラムの最終更新時間になります．
#	$utcが省略された場合は現在時です．
#	返り値はありません．
#
#
# &cgi'GetHttpDateTimeFromUtc($utc);
#
#	$utcで指定されたUTC時間から，HTTP Date/Timeフォーマットの時間文字列を
#	作り出します．返り値はその文字列です．
#
#
# &cgi'Decode;
#
#	ブラウザからCGIプログラムに送信されたフォームの入力内容，
#	あるいはURLのサーチパート(「〜.cgi?foo=bar」の，「?」以降の部分)を
#	解析し，%cgi'TAGSに格納します．
#	例えば'name'というフォームへの入力内容は$cgi'TAGS{'name'}で，
#	「〜.cgi?foo=bar」というURLのfooの値は$cgi'TAGS{'foo'}で，
#	参照することができます．
#	%cgi'TAGSを破壊します．返り値はありません．
#
#
# &cgi'Cookie;
#
#	ブラウザからCGIプログラムに送信されたHTTP Cookiesを解析し，
#	%cgi'COOKIESに格納します．
#	例えばHTTP Cookiesが'foo=bar'という文字列であれば，
#	$cgi'COOKIES{'foo'}に'bar'が格納されます．
#	%cgi'COOKIESを破壊します．返り値はありません．
#
#
# &cgi'SendMail($fromName, $fromEmail, $subject, $extension, $message, @to);
#
#	メイルを送信します．
#		$fromName: 送り主の名前(日本語を入れないでください)
#		$fromEmail: 送り主のE-Mail addr.
#		$subject: メイルのsubject文字列(日本語を入れないでください)
#		$extension: メイルのextension header文字列
#		$message: 本文である文字列
#		@to: 宛先のE-Mail addr.のリスト
#	$main'ARCHの値に応じ，用いるメイル送信手法が異なります．
#		UNIX	$main'MAIL2で指定したsendmailコマンド
#			(例えば'/usr/lib/sendmail -oi -t')を使って送信します．
#		WinNT	UNIX以外ではメイル送信はできません．$main'MAIL2で
#		Win95	指定したファイルに書き出します．ただしMacでなら，
#		Mac	perl5専用のcgi.pl.libnetを使えばメイル送信ができます．
#	送信が無事行えれば1を，なんらかの理由で行えなければ0を返します．
#
#
# &cgi'SecureHtml(*string);
#
#	*stringで指定された文字列のうち，指定した安全なタグのみを残し，
#	あとはHTML encodeしてしまいます．
#	使用を許可するタグおよびフィーチャは，@cgi'HTML_TAGSで指定します．
#	返り値はありません．
#
#
# &cgiprint'Init;
# &cgiprint'Cache($string);
# &cgiprint'Flush;
#
#	CGIプログラムからブラウザに送信する文字列の日本語漢字コードを変換し，
#	標準出力に吐き出します．高速化のためにキャッシュ機能を持っており，
#	Initはキャッシュのクリアを，
#	Cacheは表示文字列のキャッシュを，
#	Flushはキャッシュされている文字列の送信を行います．
#	キャッシュが適当なサイズになったら自動的にFlushされるので，
#	キャッシュした文字列の大きさを気にする必要はありません．
#	'<html><title>...</title>'のキャッシュの前に一度&cgiprint'Initして，
#	後はすべてのprintを&cgiprint'Cache($string)にし，
#	'</html>'の後で&cgiprint'Flushするとよいでしょう．
#	返り値はありません．


require('jcode.pl');


###
## cgiデータ入出力パッケージ
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
## HTTP Cookiesのデコード
#
sub Cookie {
    local($Term, $Tag, $Value);
    foreach $Term (split(";\s*", $ENV{'HTTP_COOKIE'})) {
	($Tag, $Value) = split(/=/, $Term, 2);
	$COOKIES{$Tag} = $Value;
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
