#!/usr/local/bin/perl
#!F:\tool\perl\bin\perl.exe
#!D:\TOOL\ETC\PERL5\BIN\perl.exe
# きのぼず実行環境テストCGI kbTst.cgi   aya@big.or.jp
# Version 0.05   1999/11/03
#
#このファイルをkb.cgiと同じディレクトリにおいて、実行権限をあたえてください。
#そして、ブラウザでこのファイルにアクセスすると、チェックを開始します。
#$| = 1;


#1999/11/03
#V0.05      WindowsNTで文法チェックしない問題を修正
#           ディレクトリ一覧を出力
#           その他、細かい修正
#
#1999/10/27
#V0.04      whiche perlの情報を追加。(Win32以外)
#           $0を$ENV{SCRIPT_FILENAME}に変更
#           その他、細かい修正
#           
#1999/10/27
#V0.03      読み込みのみのディレクトリに書きこみチェックをしていたのを修正
#           読み込みのみのディレクトリにディレクトリチェックを追加
#           Perlのバージョン、kb.cgi,kb.phの文法チェックを追加
#           Windows98/RedHat4.2/Slackware(SuExec)環境で動作確認。
#           

if($ENV{'WINDIR'} =~ /.*WINNT.*/gi){ $pc = 0; }
else{ $pc =1; }


print "Content-type: text/html; charset=EUC-JP;\n\n";
print <<"_HTML_";
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<HTML>
<HEAD>
<META http-equiv="Content-Type" content="text/html; charset=EUC-JP">
<TITLE>KINOBOARDS/1.0 kbTst.cgi</TITLE>
</HEAD>
<BODY>
<H1>きのぼず　環境テストCGI</H1>

<P>
　このテストCGIでは、動作するための最低限のチェックしか行いません。<BR>
　運用の形態や、カスタマイズの状況によっては、チェック結果が異常になる場合もあります。<BR>
<BR>
　以下のチェックを行います。
</P>

<UL>
<LI><A href="#p">\$KBDIR_PATHのチェック</A>
<LI><A href="#d">ディレクトリのチェック</A>
<LI><A href="#f">ファイルのチェック</A>
<LI><A href="#e">環境チェック</A>
<LI><A href="#c">文法チェック</A>
</UL>

<P>
　サーバ運営の上で、公開するべきではない情報も含まれています。<BR>
　設置が完了したら、必ずこのファイルは削除しておいてください。
</P>

<H1><A name="p">\$KBDIR_PATHのチェック</A></H1>

<P>
きのぼずのCGIプログラム(kb.cgi)が、
きのぼずディレクトリ(kb/)に置かれている場合は、
以下の「このファイルのPATH」から最後のファイル名を除いたものが、
きのぼずディレクトリのPATHです。
kb.cgiを開いて\$KBDIR_PATHに設定してください。<BR>
そうでない場合、
この方法ではきのぼずディレクトリのPATHを調査することはできません。<BR>
<BR>
このファイルのPATH: <BR>
$ENV{SCRIPT_FILENAME}<BR>
$0<BR>
</P>
_HTML_

print "<H2><A name=\"d\">ディレクトリのチェック</A></H2>\n";

print "<P>./ ...";
if( &check_dir_w("./") ){ print "正常です";  }
else{     print "$error<BR>\n$msg";  }
print "</P>\n";

print "<P>./UI ...";
if( &check_dir_r("./UI") ){ print "正常です";  }
else{     print "$error<BR>\n$msg";  }
print "</P>\n";

print "<P>./board ...";
if( &check_dir_r("./board") ){ print "正常です";  }
else{     print "$error<BR>\n$msg";  }
print "</P>\n";

print "<P>./log ...";
if( &check_dir_w("./log") ){ print "正常です";  }
else{     print "$error<BR>\n$msg";  }
print "</P>\n";

print "<P>./icons ...";
if( &check_dir_r("./icons") ){ print "正常です";  }
else{     print "$error<BR>\n$msg";  }
print "</P>\n";

print "<H2><A name=\"f\">ファイルのチェック</A></H2>\n";

print "<P>./kb.cgi ...";
if( &check_script("./kb.cgi") ){ print "正常です";  }
else{     print "$error<BR>\n$msg";  }
print "</P>\n";

print "<P>./kb.ph ...";
if( &check_file_r("./kb.ph") ){ print "正常です";  }
else{     print "$error<BR>\n$msg";  }
print "</P>\n";

print "<P>./kinoboards ...";
if( &check_file_r("./kinoboards") ){ print "正常です";  }
else{     print "$error<BR>\n$msg";  }
print "</P>\n";

print "<P>./jcode.pl ...";
if( &check_file_r("./jcode.pl") ){ print "正常です";  }
else{     print "$error<BR>\n$msg";  }
print "</P>\n";

print "<P>./cgi.pl ...";
if( &check_file_r("./cgi.pl") ){ print "正常です";  }
else{     print "$error<BR>\n$msg";  }
print "</P>\n";

print "<H2><A name=\"e\">環境チェック</A></H2>\n";
print "<P>\n";
print "　以下の中から、重要なものは、SERVER_NAME,SERVER_SOFTWARE,PATH_INFO,Perl Version,OS,etc....です。\n";
print "</P>\n";
print "<UL>\n";

for (keys %ENV){
   print "<LI><STRONG>$_</STRONG> : $ENV{$_}\n";
}

print "<LI><STRONG>Perl Version...</STRONG>$]<BR>\n";
print "<LI><STRONG>OS...</STRONG>$^O<BR>\n";
print "</UL>\n";

unless($^O =~ /win32/i){
	print "<P><STRONG>which perl</STRONG> : \n";
	print "</P>\n";
	&cmd("which perl");

	print "<P><STRONG>ls -laF</STRONG> : \n";
	print "</P>\n";
	&cmd("ls -laF"); 
}

print "<H2><A name=\"c\">文法チェック</A></H2>";

print "<P>　kb.cgi、kb.phの文法チェックを実行します。<BR>\n";
print "　ただし、Windows9x環境では、動作しません。<BR></P>\n";

&program_check();

print <<"_HTML_";
<HR>
<ADDRESS>
Maintenance: 綾乃介 aya\@big.or.jp<BR>
kbTst.cgi : Copyright (C) 1998-1999 Ayanosuke.
</ADDRESS>
</BODY>
</HTML>
_HTML_
exit;


sub program_check{
  print "<P><STRONG>perl -c ./kb.cgi</STRONG><BR>\n";
  print "</P>\n";
  &cmd("perl -c ./kb.cgi");

  print "<P><STRONG>perl -c ./kb.ph</STRONG><BR>\n";
  print "</P>\n";
  &cmd("perl -c ./kb.ph");

  print "<P><STRONG>perl -v</STRONG><BR>\n";
  print "</P>\n";
  &cmd("perl -v",'n');
}

#ファイル　実行ファイル
sub check_script{
	$msg = ""; $error = ""; $path = $_[0];
	#存在、読み込み、実行
	unless( -e $path ){ ($error,$msg) = &comment_set("e"); return 0; }
	unless( -r $path ){ ($error,$msg) = &comment_set("r"); return 0; }
	unless( -x $path ){ ($error,$msg) = &comment_set("x"); return 0; }
	return 1;
}

#ファイル　読み込み
sub check_file_r{
	$msg = ""; $error = ""; $path = $_[0];
	#存在、読み込み、実行
	unless( -e $path ){ ($error,$msg) = &comment_set("e"); return 0; }
	unless( -r $path ){ ($error,$msg) = &comment_set("r"); return 0; }
	return 1;
}

#ファイル　書きこみ
sub check_file_w{
	$msg = ""; $error = ""; $path = $_[0];
	#存在、読み込み、実行
	unless( -e $path ){ ($error,$msg) = &comment_set("e"); return 0; }
	unless( -T $path ){ ($error,$msg) = &comment_set("T"); return 0; }
	unless( -r $path ){ ($error,$msg) = &comment_set("r"); return 0; }
	unless( -w $path ){ ($error,$msg) = &comment_set("w"); return 0; }
	return 1;
}

#ディレクトリ　読み込み
sub check_dir_r{
	$msg = ""; $error = ""; $path = $_[0];
	#存在、読み込み、、書きこみ
	unless( -e $path ){ ($error,$msg) = &comment_set("e"); return 0; }
	unless( -d $path ){ ($error,$msg) = &comment_set("d"); return 0; }
	unless( -r $path ){ ($error,$msg) = &comment_set("r"); return 0; }
	return 1;
}


#ディレクトリ　書きこみ
sub check_dir_w{
	$msg = ""; $error = ""; $path = $_[0];
	#存在、読み込み、、書きこみ
	unless( -e $path ){ ($error,$msg) = &comment_set("e"); return 0; }
	unless( -d $path ){ ($error,$msg) = &comment_set("d"); return 0; }
	unless( -r $path ){ ($error,$msg) = &comment_set("r"); return 0; }
	unless( -w $path ){ ($error,$msg) = &comment_set("w"); return 0; }
	return 1;
}

#エラー時のコメントをセットします
#e,r,w,x,d,T
sub comment_set{
	local ($com,$error);
	local ($k) = $_[0];
	for(1){
		if ($k eq "e") {  #存在しない
			$error = "エラー";
			$com = "該当ファイル(ディレクトリ)が存在しません。<BR>
ファイルがないか、ファイル名が間違っていないかを確認してみてください。<BR>
特に、大文字、小文字には注意してください。<BR>
(例：UI =&gt; Ui , etc...)";
			last;
		}
		if($k eq "r") {  #読みこめない
			$error = "読み込み　エラー";
			$com = "読み込めません<BR>多くの環境では、604もしくは、644です。ディレクトリの場合は、705、755です。";
			last;
		}
		if ($k eq "w") {  #書きこめない
			$error = "パーミッション　エラー";
			$com = "書きこみパーミッションを設定してください<BR>多くの環境では、606もしくは、666です。ディレクトリの場合は、707、777です。";
			last;
		}
		if ($k eq "x") {  #実行できない
			$error = "パーミッション　エラー";
			$com = "実行パーミッションを設定してください<BR>多くの環境では、705もしくは、755です。<BR>
MS Windows環境では、このエラーは無視して良い場合もあります。";
			last;
		}
		if ($k eq "d") {  #ディレクトリじゃない
			$error = "エラー";
			$com = "ディレクトリではありません。";
			last;
		}
		if ($k eq "T") {  #テキストファイルじゃない
			$error = "エラー";
			$com = "該当ファイルはテキストファイルではありません。何らかの問題が発生しています。アーカイブから取り出し、上書きしてください。";
			last;
		}
		$error = "エラー";
		$com   = "不明なエラーです。";
	}
	return $error,$com;
}

sub cmd{
	if($pc && $^O =~ /win32/i){
		return(0);
	}
	if($_[1] eq 'n'){	open(PROC,"$_[0] |");  }
	else{				open(PROC,"$_[0] 2>&1 |"); }
	print "<PRE>\n";
	while (<PROC>) {
     s/</\001/g; s/>/\002/g; 
     s/(.)(\x08\1)+/<B>$1<\/B>/g;    # 多重打ち       : . 08h(BS) .
     s/_\x08(.)/<U>$1<\/U>/g;        # アンダーライン : 5fh(_) 08h(BS)
     s/o\x08\+/<S>X<\/S>/g;          # リストマーク   : 35h(o) 08h(BS) 2bh(+)
     s/<\/(.)><\1>//g;               # </TAG><TAG> を削除
     s/&/&amp;/g;                    # 
     s/\001/&lt;/g; s/\002/&gt;/g;
#     s/\n/<BR>\n/g;
     print $_;
	}
	close(PROC);
	print "</PRE>\n";
}
1;


