###
## Entry - �񤭹��߲��̤�ɽ��
#
# - SYNOPSIS
#	Entry($QuoteFlag);
#
# - ARGS
#	$QuoteFlag	0 ... ����
#			1 ... ���Ѥʤ��Υ�ץ饤
#			2 ... ���Ѥ���Υ�ץ饤
#
# - DESCRIPTION
#	�񤭹��߲��̤�ɽ������
#	����ѿ��Ǥ��롤CGI�ѿ��򻲾Ȥ��롥
#
# - RETURN
#	�ʤ�
#
Entry: {
    local( $QuoteFlag ) = $gVarQuoteFlag;

    local( $Id, $Supersede, $IconTitle, $Key, $Value, $Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail, $DefSubject, $DefName, $DefEmail, $DefUrl, $DefFmail, $ttBit, $ttFlag );

    # lock system
    local( $lockResult ) = $PC ? 1 : &cgi'lock( $LOCK_FILE );
    &Fatal(1001, '') if ( $lockResult == 2 );
    &Fatal(999, '') if ( $lockResult != 1 );
    # cash article DB
    if ( $BOARD ) { &DbCash( $BOARD ); }

    $Id = $cgi'TAGS{'id'};
    $Supersede = $cgi'TAGS{'s'}; # ����?
    if ($QuoteFlag != 0) {
	($Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail) = &GetArticlesInfo($Id);
    }
    $Icon = $Icon || $H_NOICON;
    $DefSubject = ($Supersede ? $Subject : (($QuoteFlag == 0) ? '' : &GetReplySubject($Id)));
    $DefName = ($Supersede ? $Name : '');
    $DefEmail = ($Supersede ? $Email : '');
    $DefUrl = ($Supersede ? $Url : 'http://');
    $DefFmail = ($Supersede ? $Fmail : '');

    # ɽ�����̤κ���
    if ($Supersede && $SYS_F_D) {
	&MsgHeader('Supersede entry', "$H_MESG������");
    } else {
	&MsgHeader('Message entry', "$H_MESG�ν񤭹���");
    }

    # �ե����ξ��
    if ($QuoteFlag != 0) {
	# ������ɽ��(���ޥ��̵��, ����������)
	&ViewOriginalArticle($Id, 0, 1);
	if ($Supersede && $SYS_F_D) {
	    &cgiprint'Cache("<hr>\n<h2>���$H_MESG����������</h2>");
	} else {
	    &cgiprint'Cache("<hr>\n<h2>���$H_MESG�ؤ�$H_REPLY��񤭹���</h2>");
	}
    }

    # ����«
    &cgiprint'Cache(<<__EOF__);
<form action="$PROGRAM" method="POST">
<input name="c" type="hidden" value="p">
<input name="b" type="hidden" value="$BOARD">
<input name="id" type="hidden" value="$Id">
<input name="s" type="hidden" value="$Supersede">
<p>
__EOF__
    if ($Supersede && $SYS_F_D) {
	&cgiprint'Cache(<<__EOF__);
���$H_MESG�����촹����$H_MESG��񤭹���Ǥ���������
__EOF__
    } else {
	&cgiprint'Cache(<<__EOF__);
$H_SUBJECT��$H_MESG��$H_FROM��$H_MAIL������˥����֥ڡ����򤪻��������ϡ�
�ۡ���ڡ�����$H_URL��񤭹���Ǥ�������(�����󡤤ʤ��Ƥ⹽���ޤ���)��
__EOF__
    }

    $ttFlag = 0;
    $ttBit = 0;
    foreach ( @H_TTMSG ) {
	if (( $SYS_TEXTTYPE & ( 2**$ttBit )) && ( $SYS_TEXTTYPE ^ ( 2** $ttBit ))) {
	    $ttFlag = 1;
	    &cgiprint'Cache( $H_TTMSG[$ttBit] . "\n" );
	}
	$ttBit++;
    }

    &cgiprint'Cache(<<__EOF__);
</p>
<p>
$H_BOARD: $BOARDNAME<br>
__EOF__

    # �������������
    if ($SYS_ICON) {
	&CashIconDb($BOARD);	# ��������DB�򥭥�å���
	&cgiprint'Cache("$H_ICON:\n<SELECT NAME=\"icon\">\n<OPTION SELECTED>$H_NOICON\n");
	foreach $IconTitle (@ICON_TITLE) {
	    &cgiprint'Cache("<OPTION>$IconTitle\n");
	}
	&cgiprint'Cache("</SELECT>\n");

	&cgiprint'Cache("(" . &TagA( "$PROGRAM?b=$BOARD&c=i&type=entry", "�������������" ) . ")<BR>\n");

    }

    # Subject(�ե����ʤ鼫ưŪ��ʸ����������)
    &cgiprint'Cache(sprintf("%s: <input name=\"subject\" type=\"text\" value=\"%s\" size=\"%s\"><br>\n", $H_SUBJECT, $DefSubject, $SUBJECT_LENGTH));

    # TextType
    if ( $ttFlag ) {
	&cgiprint'Cache( "$H_TEXTTYPE:\n<SELECT NAME=\"texttype\">\n" );
	$ttBit = 0;
	foreach ( @H_TTLABEL ) {
	    if ( $SYS_TEXTTYPE & ( 2 ** $ttBit )) {
		if ( $ttFlag ) {
		    $ttFlag = 0;	# now, using for a flag for the first.
		    &cgiprint'Cache( "<OPTION SELECTED>" . $H_TTLABEL[$ttBit] . "\n" );
		}
		else {
		    &cgiprint'Cache( "<OPTION>" . $H_TTLABEL[$ttBit] . "\n" );
		}
	    }
	    $ttBit++;
	}
	&cgiprint'Cache( "</SELECT>\n</p>\n" );
    }
    else {
	&cgiprint'Cache( sprintf( "<input name=\"texttype\" type=\"hidden\" value=\"%s\">\n", $H_TTLABEL[(( log $SYS_TEXTTYPE ) / ( log 2 ))] ));
    }

    # ��ʸ(���Ѥ���ʤ鸵����������)
    &cgiprint'Cache("<p><textarea name=\"article\" rows=\"$TEXT_ROWS\" cols=\"$TEXT_COLS\">");
    if ($Supersede && $SYS_F_D) {
	&QuoteOriginalArticleWithoutQMark($Id);
    } elsif ($QuoteFlag == 2) {
	&QuoteOriginalArticle($Id);
    }

    &cgiprint'Cache("</textarea></p>\n");

    # �եå���ʬ��ɽ��
    # ̾���ȥᥤ�륢�ɥ쥹��URL��
    &cgiprint'Cache(<<__EOF__);
<p>
$H_MESG��˴�Ϣ�����֥ڡ����ؤΥ�󥯤�ĥ����ϡ�
��&lt;URL:http://��&gt;�פΤ褦�ˡ�URL���&lt;URL:�פȡ�&gt;�פǰϤ��
�񤭹���Ǥ�����������ưŪ�˥�󥯤�ĥ���ޤ���
����$H_BOARD�����$H_MESG�˥�󥯤�ĥ�����
__EOF__

    &cgiprint'Cache( &TagA( "$PROGRAM?b=$BOARD&c=s", "������ǽ��Ȥ�" ));

    &cgiprint'Cache( "�������Ǥ���õ���Ф���$H_MESG��URL�򡤡�&lt;URL:�פȡ�&gt;�פǰϤ�Ǥ���������\n</p>\n" );

    if ($SYS_ALIAS == 0) {

	# �����ꥢ���ϻȤ�ʤ�
	&cgiprint'Cache(<<__EOF__);
<p>
$H_FROM: <input name="name" type="text" value="$DefName" size="$NAME_LENGTH"><br>
$H_MAIL: <input name="mail" type="text" value="$DefEmail" size="$MAIL_LENGTH"><br>
$H_URL_S:<br>
<input name="url" type="text" value="$DefUrl" size="$URL_LENGTH"><br>
</p>
__EOF__

    } elsif ($SYS_ALIAS == 1) {

	# �����ꥢ����Ȥ�
	&cgiprint'Cache(<<__EOF__);
<p>
$H_FROM: <input name="name" type="text" value="$DefName" size="$NAME_LENGTH"><br>
$H_MAIL: <input name="mail" type="text" value="$DefEmail" size="$MAIL_LENGTH"><br>
$H_URL_S:<br>
<input name="url" type="text" value="$DefUrl" size="$URL_LENGTH">
</p>
__EOF__

	&cgiprint'Cache(<<__EOF__);
<p>
��$H_ALIAS�פˡ�$H_FROM��$H_MAIL��$H_URL����Ͽ�ʤ��äƤ������ϡ�
��$H_FROM�פˡ�#...�פȤ�����Ͽ̾��񤤤Ƥ���������
��ưŪ��$H_FROM��$H_MAIL��$H_URL������ޤ���
__EOF__
	&cgiprint'Cache( "(" . &TagA( "$PROGRAM?c=as", "$H_ALIAS�ΰ���" ) . " // \n" );
	&cgiprint'Cache( &TagA( "$PROGRAM?c=an", "$H_ALIAS����Ͽ" ) . ")\n" );

    } else {

	# �����ꥢ������Ͽ���ʤ���н񤭹��ߤǤ��ʤ�

	# �����ꥢ�����ɤ߹���
	&CashAliasData;

	&cgiprint'Cache(<<__EOF__);
<p>
$H_USER:
<SELECT NAME="name">
<OPTION SELECTED>$H_FROM����Ͽ����$H_ALIAS������Ǥ�������
__EOF__

	while (($Key, $Value) = each %Name) {
	    &cgiprint'Cache("<OPTION>$Key\n");
	}
	&cgiprint'Cache(<<__EOF__);
</SELECT>
</p>
__EOF__

	&cgiprint'Cache(<<__EOF__);
<p>
ͽ���$H_ALIAS�פˡ�$H_FROM��$H_MAIL��$H_URL����Ͽ���ʤ��Ƚ񤭹���ޤ���
��Ͽ�����塤��#...�פȤ�����Ͽ̾����ꤷ�Ƥ���������
__EOF__
	&cgiprint'Cahce( "(" . &TagA( "$PROGRAM?c=as", "$H_ALIAS�ΰ���" ) . " // \n" );
	&cgiprint'Cache( &TagA( "$PROGRAM?c=an", "$H_ALIAS����Ͽ" ) . ")<br>\n" );
	&cgiprint'Cache(<<__EOF__);
��Ͽ����$H_ALIAS��ɽ������ʤ�(����Ǥ��ʤ�)��硤
���Υڡ�������ɤ߹��ߤ��Ƥ���������
</p>
__EOF__

    }

    if ( $SYS_MAIL & 2 ) {
	&cgiprint'Cache("<p>$H_REPLY�����ä����˥ᥤ����Τ餻�ޤ���? <input name=\"fmail\" type=\"checkbox\" value=\"on\"></p>\n");
    }
    
    # unlock system
    &cgi'unlock( $LOCK_FILE ) unless $PC;

    # �ܥ���
    &cgiprint'Cache(<<__EOF__);
<p>
�񤭹�������Ƥ�<br>
<input type="radio" name="com" value="p" CHECKED>: ���ɽ�����Ƥߤ�(�ޤ���Ƥ��ޤ���)<br>
__EOF__

    if ($Supersede && $SYS_F_D) {
	&cgiprint'Cache("<input type=\"radio\" name=\"com\" value=\"x\">: �������ޤ�<br>\n");
    } else {
	&cgiprint'Cache("<input type=\"radio\" name=\"com\" value=\"x\">: $H_MESG����Ƥ���<br>\n");
    }

    &cgiprint'Cache(<<__EOF__);
<input type="submit" value="�¹�">
</p>
</form>
__EOF__

    &MsgFooter;

}

1;
