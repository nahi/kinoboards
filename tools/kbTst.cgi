#!/usr/local/bin/perl
# ���Τܤ��¹ԴĶ��ƥ���CGI kbTst.cgi   aya@big.or.jp
#
#���Υե������kb.cgi��Ʊ���ǥ��쥯�ȥ�ˤ����ơ��¹Ը��¤򤢤����Ƥ���������
#�����ơ��֥饦���Ǥ��Υե�����˥�����������ȡ������å��򳫻Ϥ��ޤ���

print "Content-type: text/html\n\n";
print <<"_HTML_";
<HTML>
<HEAD>
<TITLE>KINOBOARDS/1.0 kbTst.cgi</TITLE>
</head>

<BODY>
<H1>���Τܤ����Ķ��ƥ���CGI</H1>

<P>
�����Υƥ���CGI�Ǥϡ�ư��뤿��κ���¤Υ����å������Ԥ��ޤ���<BR>
�����Ѥη��֤䡢�������ޥ����ξ����ˤ�äƤϡ������å���̤��۾�ˤʤ���⤢��ޤ���<BR>
</P>

<P>
���Τܤ���CGI�ץ����(kb.cgi)����
���Τܤ��ǥ��쥯�ȥ�(kb/)���֤���Ƥ�����ϡ�
�ʲ��Ρ֤��Υե������PATH�פ���Ǹ�Υե�����̾���������Τ���
���Τܤ��ǥ��쥯�ȥ��PATH�Ǥ���
kb.cgi�򳫤���\$KBDIR_PATH�����ꤷ�Ƥ���������<BR>
�����Ǥʤ���硢
������ˡ�ǤϤ��Τܤ��ǥ��쥯�ȥ��PATH��Ĵ�����뤳�ȤϤǤ��ޤ���
</P>

<P>
���Υե������PATH: $0
</P>
_HTML_

print "<H2>�ǥ��쥯�ȥ�Υ����å�</H2>\n";

print "<P>./ ...";
if( &check_dir_w("./") ){ print "����Ǥ�";  }
else{     print "$error<BR>\n$msg";  }
print "</P>\n";

print "<P>./UI ...";
if( &check_dir_r("./UI") ){ print "����Ǥ�";  }
else{     print "$error<BR>\n$msg";  }
print "</P>\n";

print "<P>./board ...";
if( &check_dir_r("./board") ){ print "����Ǥ�";  }
else{     print "$error<BR>\n$msg";  }
print "</P>\n";

print "<P>./log ...";
if( &check_dir_w("./log") ){ print "����Ǥ�";  }
else{     print "$error<BR>\n$msg";  }
print "</P>\n";

print "<P>./icons ...";
if( &check_dir_r("./icons") ){ print "����Ǥ�";  }
else{     print "$error<BR>\n$msg";  }
print "</P>\n";

print "<H2>�ե�����Υ����å�</H2>\n";

print "<P>./kb.cgi ...";
if( &check_script("./kb.cgi") ){ print "����Ǥ�";  }
else{     print "$error<BR>\n$msg";  }
print "</P>\n";

print "<P>./kb.ph ...";
if( &check_file_w("./kb.ph") ){ print "����Ǥ�";  }
else{     print "$error<BR>\n$msg";  }
print "</P>\n";

print "<P>./kinoboards ...";
if( &check_file_r("./kinoboards") ){ print "����Ǥ�";  }
else{     print "$error<BR>\n$msg";  }
print "</P>\n";

print "<P>./jcode.pl ...";
if( &check_file_r("./jcode.pl") ){ print "����Ǥ�";  }
else{     print "$error<BR>\n$msg";  }
print "</P>\n";

print "<P>./cgi.pl ...";
if( &check_file_r("./cgi.pl") ){ print "����Ǥ�";  }
else{     print "$error<BR>\n$msg";  }
print "</P>\n";

print <<"_HTML_";
<ADDRESS>
Maintenance: ��ǵ�� aya\@big.or.jp<BR>
kbTst.cgi : Copyright (C) 1999 Ayanosuke.
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
	unless( -r $path ){ ($error,$msg) = &comment_set("r"); return 0; }
	unless( -w $path ){ ($error,$msg) = &comment_set("w"); return 0; }
	unless( -T $path ){ ($error,$msg) = &comment_set("T"); return 0; }
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

#�ǥ��쥯�ȥꡡ�ɤ߹���
sub check_dir_r{
	$msg = ""; $error = ""; $path = $_[0];
	#¸�ߡ��ɤ߹��ߡ����񤭤���
	unless( -e $path ){ ($error,$msg) = &comment_set("e"); return 0; }
	unless( -r $path ){ ($error,$msg) = &comment_set("r"); return 0; }
	unless( -w $path ){ ($error,$msg) = &comment_set("w"); return 0; }
	return 1;
}

#���顼���Υ����Ȥ򥻥åȤ��ޤ�
#e,r,w,x,d,T
sub comment_set{
	local ($com,$error);
	local ($k) = @_[0];
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
			$com = "�ɤ߹���ޤ���";
			last;
		}
		if ($k eq "w") {  #�񤭤���ʤ�
			$error = "�ѡ��ߥå���󡡥��顼";
			$com = "�񤭤��ߥѡ��ߥå��������ꤷ�Ƥ�������<BR>¿���δĶ��Ǥϡ�606�⤷���ϡ�666�Ǥ���";
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
