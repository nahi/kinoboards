#!/usr/local/bin/perl
#!F:\tool\perl\bin\perl.exe
#!D:\TOOL\ETC\PERL5\BIN\perl.exe

#----------------------------------------------------------------#
# ���Τܤ��¹ԴĶ��ƥ���CGI kbTst.cgi   aya@big.or.jp
# Version 0.06   1999/11/07
#
# �ޤ���1���ܤ򡢼�ʬ�Υ����дĶ��˹�碌���Խ����Ƥ���������
# ���ˡ����Υե������kb.cgi��Ʊ���ǥ��쥯�ȥ�ˤ����ơ��¹Ը��¤򤢤����Ƥ���������
# �����ơ��֥饦���Ǥ��Υե�����˥�����������ȡ������å��򳫻Ϥ��ޤ���
#----------------------------------------------------------------#
### ����
# CGI�Ȥ���¾�Υե�������֤���꤬�ۤʤ���ϡ���
# kb�ǥ��쥯�ȥ�����Хѥ��⤷���ϡ����Хѥ�����ꤷ�Ƥ���������URL�ǤϤʤ����ѥ��Ǥ���
# �Ǹ�� / �ǽ���äƤ���������
$KBDIR = './';

#----------------------------------------------------------------#
###�ѹ�����
#1999/11/07
#V0.06      Windows9xȽ������꤬���ä��Τǽ���
#           CGI�Ȥ���¾�Υե�������֤���꤬�ۤʤ��������å��Ǥ���褦�ˤ�����
#           ����¾���٤�������
# 
#1999/11/03
#V0.05      WindowsNT��ʸˡ�����å����ʤ��������
#           �ǥ��쥯�ȥ���������
#           ����¾���٤�������
#
#1999/10/27
#V0.04      whiche perl�ξ�����ɲá�(Win32�ʳ�)
#           $0��$ENV{SCRIPT_FILENAME}���ѹ�
#           ����¾���٤�������
#           
#1999/10/27
#V0.03      �ɤ߹��ߤΤߤΥǥ��쥯�ȥ�˽񤭤��ߥ����å��򤷤Ƥ����Τ���
#           �ɤ߹��ߤΤߤΥǥ��쥯�ȥ�˥ǥ��쥯�ȥ�����å����ɲ�
#           Perl�ΥС������kb.cgi,kb.ph��ʸˡ�����å����ɲ�
#           Windows98/RedHat4.2/Slackware(SuExec)�Ķ���ư���ǧ��
#           
#----------------------------------------------------------------#

# Windows9x Ƚ��
if($^O =~ /win32/i && !($ENV{'WINDIR'} =~ /.*WINNT.*/gi)){
	$pc =1;
}else{ $pc = 0; }


print "Content-type: text/html; charset=EUC-JP;\n\n";
print <<"_HTML_";
<HTML>
<HEAD>
<META http-equiv="Content-Type" content="text/html; charset=EUC-JP">
<TITLE>KINOBOARDS/1.0 kbTst.cgi</TITLE>
</HEAD>
<BODY>
<H1>���Τܤ����Ķ��ƥ���CGI</H1>

<P>
�����Υƥ���CGI�Ǥϡ�ư��뤿��κ���¤Υ����å������Ԥ��ޤ���<BR>
�����Ѥη��֤䡢�������ޥ����ξ����ˤ�äƤϡ������å���̤��۾�ˤʤ���⤢��ޤ���<BR>
<BR>
���ʲ��Υ����å���Ԥ��ޤ���
</P>

<UL>
<LI><A href="#p">\$KBDIR_PATH�Υ����å�</A>
<LI><A href="#d">�ǥ��쥯�ȥ�Υ����å�</A>
<LI><A href="#f">�ե�����Υ����å�</A>
<LI><A href="#e">�Ķ������å�</A>
<LI><A href="#c">ʸˡ�����å�</A>
</UL>

<P>
�������б��Ĥξ�ǡ���������٤��ǤϤʤ������ޤޤ�Ƥ��ޤ���<BR>
�����֤���λ�����顢���Υե�����Ϻ�����Ƥ���������
</P>

<H1><A name="p">\$KBDIR_PATH�Υ����å�</A></H1>

<P>
���Τܤ���CGI�ץ����(kb.cgi)����
���Τܤ��ǥ��쥯�ȥ�(kb/)���֤���Ƥ�����ϡ�
�ʲ��Ρ֤��Υե������PATH�פ���Ǹ�Υե�����̾���������Τ���
���Τܤ��ǥ��쥯�ȥ��PATH�Ǥ���
kb.cgi�򳫤���\$KBDIR_PATH�����ꤷ�Ƥ���������<BR>
�����Ǥʤ���硢
������ˡ�ǤϤ��Τܤ��ǥ��쥯�ȥ��PATH��Ĵ�����뤳�ȤϤǤ��ޤ���<BR>
<BR>
���Υե������PATH: <BR>
$ENV{SCRIPT_FILENAME}<BR>
$0<BR>
</P>
_HTML_

print "<H2><A name=\"d\">�ǥ��쥯�ȥ�Υ����å�</A></H2>\n";

print "<P>$KBDIR ...";
if( &check_dir_w("$KBDIR") ){ print "����Ǥ�";  }
else{     print "$error<BR>\n$msg";  }
print "</P>\n";

print "<P>$KBDIR","UI ...";
if( &check_dir_r($KBDIR."UI") ){ print "����Ǥ�";  }
else{     print "$error<BR>\n$msg";  }
print "</P>\n";

print "<P>$KBDIR","board ...";
if( &check_dir_r($KBDIR."board") ){ print "����Ǥ�";  }
else{     print "$error<BR>\n$msg";  }
print "</P>\n";

print "<P>$KBDIR","log ...";
if( &check_dir_w($KBDIR."log") ){ print "����Ǥ�";  }
else{     print "$error<BR>\n$msg";  }
print "</P>\n";

print "<P>$KBDIR","icons ...";
if( &check_dir_r($KBDIR."icons") ){ print "����Ǥ�";  }
else{     print "$error<BR>\n$msg";  }
print "</P>\n";

print "<H2><A name=\"f\">�ե�����Υ����å�</A></H2>\n";

print "<P>./kb.cgi ...";
if( &check_script("./kb.cgi") ){ print "����Ǥ�";  }
else{     print "$error<BR>\n$msg";  }
print "</P>\n";

print "<P>$KBDIR","kb.ph ...";
if( &check_file_r($KBDIR."kb.ph") ){ print "����Ǥ�";  }
else{     print "$error<BR>\n$msg";  }
print "</P>\n";

print "<P>$KBDIR","kinoboards ...";
if( &check_file_r($KBDIR."kinoboards") ){ print "����Ǥ�";  }
else{     print "$error<BR>\n$msg";  }
print "</P>\n";

print "<P>$KBDIR","jcode.pl ...";
if( &check_file_r($KBDIR."jcode.pl") ){ print "����Ǥ�";  }
else{     print "$error<BR>\n$msg";  }
print "</P>\n";

print "<P>$KBDIR","cgi.pl ...";
if( &check_file_r($KBDIR."cgi.pl") ){ print "����Ǥ�";  }
else{     print "$error<BR>\n$msg";  }
print "</P>\n";

print "<H2><A name=\"e\">�Ķ������å�</A></H2>\n";
print "<P>\n";
print "���ʲ����椫�顢���פʤ�Τϡ�SERVER_NAME,SERVER_SOFTWARE,PATH_INFO,Perl Version,OS,etc....�Ǥ���\n";
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
	&cmd("which perl");
	print "</P>\n";

	print "<P><STRONG>uname -sr</STRONG> : \n";
	&cmd("uname -sr"); 
	print "</P>\n";

	print "<P><STRONG>ls -laF</STRONG> : \n";
	&cmd("ls -laF"); 
	print "</P>\n";
}

print "<H2><A name=\"c\">ʸˡ�����å�</A></H2>";

print "<P>��kb.cgi��kb.ph��ʸˡ�����å���¹Ԥ��ޤ���<BR>\n";
print "����������Windows9x�Ķ��Ǥϡ�ư��ޤ���<BR></P>\n";

  print "<P><STRONG>perl -c ./kb.cgi</STRONG><BR>\n";
  &cmd("perl -c ./kb.cgi");
  print "</P>\n";

  print "<P><STRONG>perl -c $KBDIR","kb.ph</STRONG><BR>\n";
  &cmd("perl -c ".$KBDIR."kb.ph");
  print "</P>\n";

  print "<P><STRONG>perl -v</STRONG><BR>\n";
  &cmd("perl -v",'n');
  print "</P>\n";

print <<"_HTML_";
<HR>
<ADDRESS>
Maintenance: ��ǵ�� aya\@big.or.jp<BR>
kbTst.cgi : Copyright (C) 1998-1999 Ayanosuke.
</ADDRESS>
</BODY>
</HTML>
_HTML_
exit;



#�ե����롡�¹ԥե�����
sub check_script{
	$msg = ""; $error = ""; $path = $_[0];
	#¸�ߡ��ɤ߹��ߡ��¹�
	unless( -e $path ){ ($error,$msg) = &comment_set("e"); return 0; }
	unless( -r $path ){ ($error,$msg) = &comment_set("r"); return 0; }
	unless( -x $path ){ ($error,$msg) = &comment_set("x"); return 0; }
	return 1;
}

#�ե����롡�ɤ߹���
sub check_file_r{
	$msg = ""; $error = ""; $path = $_[0];
	#¸�ߡ��ɤ߹��ߡ��¹�
	unless( -e $path ){ ($error,$msg) = &comment_set("e"); return 0; }
	unless( -r $path ){ ($error,$msg) = &comment_set("r"); return 0; }
	return 1;
}

#�ե����롡�񤭤���
sub check_file_w{
	$msg = ""; $error = ""; $path = $_[0];
	#¸�ߡ��ɤ߹��ߡ��¹�
	unless( -e $path ){ ($error,$msg) = &comment_set("e"); return 0; }
	unless( -T $path ){ ($error,$msg) = &comment_set("T"); return 0; }
	unless( -r $path ){ ($error,$msg) = &comment_set("r"); return 0; }
	unless( -w $path ){ ($error,$msg) = &comment_set("w"); return 0; }
	return 1;
}

#�ǥ��쥯�ȥꡡ�ɤ߹���
sub check_dir_r{
	$msg = ""; $error = ""; $path = $_[0];
	#¸�ߡ��ɤ߹��ߡ����񤭤���
	unless( -e $path ){ ($error,$msg) = &comment_set("e"); return 0; }
	unless( -d $path ){ ($error,$msg) = &comment_set("d"); return 0; }
	unless( -r $path ){ ($error,$msg) = &comment_set("r"); return 0; }
	return 1;
}


#�ǥ��쥯�ȥꡡ�񤭤���
sub check_dir_w{
	$msg = ""; $error = ""; $path = $_[0];
	#¸�ߡ��ɤ߹��ߡ����񤭤���
	unless( -e $path ){ ($error,$msg) = &comment_set("e"); return 0; }
	unless( -d $path ){ ($error,$msg) = &comment_set("d"); return 0; }
	unless( -r $path ){ ($error,$msg) = &comment_set("r"); return 0; }
	unless( -w $path ){ ($error,$msg) = &comment_set("w"); return 0; }
	return 1;
}

#���顼���Υ����Ȥ򥻥åȤ��ޤ�
#e,r,w,x,d,T
sub comment_set{
	local ($com,$error);
	local ($k) = $_[0];
	for(1){
		if ($k eq "e") {  #¸�ߤ��ʤ�
			$error = "���顼";
			$com = "�����ե�����(�ǥ��쥯�ȥ�)��¸�ߤ��ޤ���<BR>
�ե����뤬�ʤ������ե�����̾���ְ�äƤ��ʤ������ǧ���ƤߤƤ���������<BR>
�äˡ���ʸ������ʸ���ˤ���դ��Ƥ���������<BR>
(�㡧UI => Ui , etc...)";
			last;
		}
		if($k eq "r") {  #�ɤߤ���ʤ�
			$error = "�ɤ߹��ߡ����顼";
			$com = "�ɤ߹���ޤ���<BR>¿���δĶ��Ǥϡ�604�⤷���ϡ�644�Ǥ����ǥ��쥯�ȥ�ξ��ϡ�705��755�Ǥ���";
			last;
		}
		if ($k eq "w") {  #�񤭤���ʤ�
			$error = "�ѡ��ߥå���󡡥��顼";
			$com = "�񤭤��ߥѡ��ߥå��������ꤷ�Ƥ�������<BR>¿���δĶ��Ǥϡ�606�⤷���ϡ�666�Ǥ����ǥ��쥯�ȥ�ξ��ϡ�707��777�Ǥ���";
			last;
		}
		if ($k eq "x") {  #�¹ԤǤ��ʤ�
			$error = "�ѡ��ߥå���󡡥��顼";
			$com = "�¹ԥѡ��ߥå��������ꤷ�Ƥ�������<BR>¿���δĶ��Ǥϡ�705�⤷���ϡ�755�Ǥ���<BR>
MS Windows�Ķ��Ǥϡ����Υ��顼��̵�뤷���ɤ����⤢��ޤ���";
			last;
		}
		if ($k eq "d") {  #�ǥ��쥯�ȥꤸ��ʤ�
			$error = "���顼";
			$com = "�ǥ��쥯�ȥ�ǤϤ���ޤ���";
			last;
		}
		if ($k eq "T") {  #�ƥ����ȥե����뤸��ʤ�
			$error = "���顼";
			$com = "�����ե�����ϥƥ����ȥե�����ǤϤ���ޤ��󡣲��餫�����꤬ȯ�����Ƥ��ޤ������������֤�����Ф�����񤭤��Ƥ���������";
			last;
		}
		$error = "���顼";
		$com   = "�����ʥ��顼�Ǥ���";
	}
	return $error,$com;
}

sub cmd{
	if($pc){
		return(0);
	}
	if($_[1] eq 'n'){	open(PROC,"$_[0] |");  }
	else{				open(PROC,"$_[0] 2>&1 |"); }
	while (<PROC>) {
     s/</\001/g; s/>/\002/g; 
     s/(.)(\x08\1)+/<B>$1<\/B>/g;    # ¿���Ǥ�       : . 08h(BS) .
     s/_\x08(.)/<U>$1<\/U>/g;        # ��������饤�� : 5fh(_) 08h(BS)
     s/o\x08\+/<S>X<\/S>/g;          # �ꥹ�ȥޡ���   : 35h(o) 08h(BS) 2bh(+)
     s/<\/(.)><\1>//g;               # </TAG><TAG> ����
     s/&/&amp;/g;                    # 
     s/\001/&lt;/g; s/\002/&gt;/g;
     s/\n/<BR>\n/g;
     print $_;
	}
	close(PROC);
}
1;

