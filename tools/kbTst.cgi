#!/usr/local/bin/perl
# きのぼず実行環境テストCGI kbTst.cgi   aya@big.or.jp
#
#このファイルをkb.cgiと同じディレクトリにおいて、実行権限をあたえてください。
#そして、ブラウザでこのファイルにアクセスすると、チェックを開始します。

print "Content-type: text/html\n\n";
print <<"_HTML_";
<HTML>
<HEAD>
<TITLE>KINOBOARDS/1.0 kbTst.cgi</TITLE>
</head>

<BODY>
<H1>きのぼず　環境テストCGI</H1>

<P>
　このテストCGIでは、動作するための最低限のチェックしか行いません。<BR>
　運用の形態や、カスタマイズの状況によっては、チェック結果が異常になる場合もあります。<BR>
</P>

<P>
きのぼずのCGIプログラム(kb.cgi)が、
きのぼずディレクトリ(kb/)に置かれている場合は、
以下の「このファイルのPATH」から最後のファイル名を除いたものが、
きのぼずディレクトリのPATHです。
kb.cgiを開いて\$KBDIR_PATHに設定してください。<BR>
そうでない場合、
この方法ではきのぼずディレクトリのPATHを調査することはできません。
</P>

<P>
このファイルのPATH: $0
</P>
_HTML_

print "<H2>ディレクトリのチェック</H2>\n";

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

print "<H2>ファイルのチェック</H2>\n";

print "<P>./kb.cgi ...";
if( &check_script("./kb.cgi") ){ print "正常です";  }
else{     print "$error<BR>\n$msg";  }
print "</P>\n";

print "<P>./kb.ph ...";
if( &check_file_w("./kb.ph") ){ print "正常です";  }
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

print <<"_HTML_";
<ADDRESS>
Maintenance: 綾乃介 aya\@big.or.jp<BR>
kbTst.cgi : Copyright (C) 1999 Ayanosuke.
</ADDRESS>
</BODY>
</HTML>
_HTML_
exit;

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
	unless( -r $path ){ ($error,$msg) = &comment_set("r"); return 0; }
	unless( -w $path ){ ($error,$msg) = &comment_set("w"); return 0; }
	unless( -T $path ){ ($error,$msg) = &comment_set("T"); return 0; }
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

#ディレクトリ　読み込み
sub check_dir_r{
	$msg = ""; $error = ""; $path = $_[0];
	#存在、読み込み、、書きこみ
	unless( -e $path ){ ($error,$msg) = &comment_set("e"); return 0; }
	unless( -r $path ){ ($error,$msg) = &comment_set("r"); return 0; }
	unless( -w $path ){ ($error,$msg) = &comment_set("w"); return 0; }
	return 1;
}

#エラー時のコメントをセットします
#e,r,w,x,d,T
sub comment_set{
	local ($com,$error);
	local ($k) = @_[0];
	for(1){
		if ($k eq "e") {  #存在しない
			$error = "エラー";
			$com = "該当ファイル(ディレクトリ)が存在しません。<BR>
ファイルがないか、ファイル名が間違っていないかを確認してみてください。<BR>
特に、大文字、小文字には注意してください。<BR>
(例：UI => Ui , etc...)";
			last;
		}
		if($k eq "r") {  #読みこめない
			$error = "読み込み　エラー";
			$com = "読み込めません";
			last;
		}
		if ($k eq "w") {  #書きこめない
			$error = "パーミッション　エラー";
			$com = "書きこみパーミッションを設定してください<BR>多くの環境では、606もしくは、666です。";
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
