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
Entry:
{
    local( $QuoteFlag ) = $gVarQuoteFlag;

    local( $Id, $Supersede, $IconTitle, $Key, $Value, $Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $DefSubject, $DefName, $DefEmail, $DefUrl, $ttBit, $ttFlag );

    # lock system
    local( $lockResult ) = $PC ? 1 : &cgi'lock( $LOCK_FILE_B );
    &Fatal(1001, '') if ( $lockResult == 2 );
    &Fatal(999, '') if ( $lockResult != 1 );
    # cache article DB
    if ( $BOARD ) { &DbCache( $BOARD ); }

    $Id = $cgi'TAGS{'id'};
    $Supersede = $cgi'TAGS{'s'}; # ����?
    if ($QuoteFlag != 0)
    {
	($Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url) = &GetArticlesInfo($Id);
    }
    $Icon = $Icon || $H_NOICON;

    if ( $Supersede )
    {
	$DefSubject = $Subject;
	$DefName = $Name;
	$DefEmail = $Email;
	$DefUrl = $Url;
    }
    else
    {
	$DefSubject = (( $QuoteFlag == 0 ) ? '' : &GetReplySubject( $Id ));

	if ( $SYS_ALIAS == 3 )
	{
	    &cgi'Cookie();
	    ( $DefName, $DefEmail, $DefUrl ) = split( /$COLSEP/, $cgi'COOKIES{ 'kb10info' });;
	    $DefUrl = $DefUrl || 'http://';
	}
	else
	{
	    $DefName = $DefEmail = '';
	    $DefUrl = 'http://';
	}
    }

    # ɽ�����̤κ���
    if ( $Supersede && $SYS_F_D )
    {
	&MsgHeader( 'Supersede entry', "$H_MESG������" );
    }
    else
    {
	&MsgHeader( 'Message entry', "$H_MESG�ν񤭹���" );
    }

    # �ե����ξ��
    if ( $QuoteFlag != 0 )
    {
	# ������ɽ��(���ޥ��̵��, ����������)
	&ViewOriginalArticle( $Id, 0, 1 );
	if ( $Supersede && $SYS_F_D )
	{
	    &cgiprint'Cache( "$H_HR\n<h2>���$H_MESG����������</h2>" );
	}
	else
	{
	    &cgiprint'Cache( "$H_HR\n<h2>���$H_MESG�ؤ�$H_REPLY��񤭹���</h2>" );
	}
    }

    local( $msg ) = "<p>\n";

    $msg .="���$H_MESG�����촹����$H_MESG��񤭹���Ǥ���������\n"
	if ( $Supersede && $SYS_F_D );

    $ttFlag = 0;
    $ttBit = 0;
    foreach ( @H_TTMSG )
    {
	if (( $SYS_TEXTTYPE & ( 2**$ttBit )) &&
	    ( $SYS_TEXTTYPE ^ ( 2** $ttBit )))
	{
	    $ttFlag = 1;
	    $msg .= $H_TTMSG[$ttBit] . "\n";
	}
	$ttBit++;
    }

    $msg .= "</p>\n<p>\n$H_BOARD: $BOARDNAME<br>\n";

    # �������������
    if ( $SYS_ICON )
    {
	&CacheIconDb( $BOARD );	# ��������DB�򥭥�å���
	$msg .= "$H_ICON:\n<SELECT NAME=\"icon\">\n<OPTION SELECTED>$H_NOICON\n";
	foreach $IconTitle ( @ICON_TITLE )
	{
	    $msg .= "<OPTION>$IconTitle\n";
	}
	$msg .= "</SELECT>\n";

	$msg .= "(" . &TagA( "$PROGRAM?b=$BOARD&c=i&type=entry", "�������������" ) . ")<BR>\n";
    }

    # Subject(�ե����ʤ鼫ưŪ��ʸ����������)
    $msg .= sprintf( "%s: <input name=\"subject\" type=\"text\" value=\"%s\" size=\"%s\"><br>\n", $H_SUBJECT, $DefSubject, $SUBJECT_LENGTH );

    # TextType
    if ( $ttFlag )
    {
	$msg .= "$H_TEXTTYPE:\n<SELECT NAME=\"texttype\">\n";
	$ttBit = 0;
	foreach ( @H_TTLABEL )
	{
	    if ( $SYS_TEXTTYPE & ( 2 ** $ttBit ))
	    {
		if ( $ttFlag )
		{
		    $ttFlag = 0;	# now, using for a flag for the first.
		    $msg .= "<OPTION SELECTED>" . $H_TTLABEL[$ttBit] . "\n";
		}
		else
		{
		    $msg .= "<OPTION>" . $H_TTLABEL[$ttBit] . "\n";
		}
	    }
	    $ttBit++;
	}
	$msg .= "</SELECT>\n</p>\n";
    }
    else
    {
	$msg .= sprintf( "<input name=\"texttype\" type=\"hidden\" value=\"%s\">\n", $H_TTLABEL[(( log $SYS_TEXTTYPE ) / ( log 2 ))] );
    }

    # ��ʸ(���Ѥ���ʤ鸵����������)
    $msg .= "<p><textarea name=\"article\" rows=\"$TEXT_ROWS\" cols=\"$TEXT_COLS\">";
    if ( $Supersede && $SYS_F_D )
    {
	&QuoteOriginalArticleWithoutQMark( $Id, *msg );
    }
    elsif ( $QuoteFlag == 2 )
    {
	&QuoteOriginalArticle( $Id, *msg );
    }

    $msg .= "</textarea></p>\n";

    # �եå���ʬ��ɽ��
    # ̾���ȥᥤ�륢�ɥ쥹��URL��
    $msg .=<<__EOF__;
<p>
$H_MESG��˴�Ϣ�����֥ڡ����ؤΥ�󥯤�ĥ����ϡ�
��&lt;URL:http://��&gt;�פΤ褦�ˡ�URL���&lt;URL:�פȡ�&gt;�פǰϤ��
�񤭹���Ǥ�����������ưŪ�˥�󥯤�ĥ���ޤ���
__EOF__

    if ( $SYS_F_S )
    {
	$msg .= "����$H_BOARD�����$H_MESG�˥�󥯤�ĥ�����\n";
	$msg .= &TagA( "$PROGRAM?b=$BOARD&c=s", "������ǽ��Ȥ�" );
	$msg .= "�������Ǥ���õ���Ф���$H_MESG��URL�򡤡�&lt;URL:�פȡ�&gt;�פǰϤ�Ǥ���������\n";
    }

    $msg .= "</p>\n";

    if ( $SYS_ALIAS == 0 )
    {
	# �����ꥢ���ϻȤ�ʤ�
	$msg .=<<__EOF__;
<p>
$H_FROM: <input name="name" type="text" value="$DefName" size="$NAME_LENGTH"><br>
$H_MAIL: <input name="mail" type="text" value="$DefEmail" size="$MAIL_LENGTH"><br>
$H_URL_S:<br>
<input name="url" type="text" value="$DefUrl" size="$URL_LENGTH"><br>
</p>
__EOF__
    }
    elsif ( $SYS_ALIAS == 1 )
    {
	# �����ꥢ����Ȥ�
	$msg .= <<__EOF__;
<p>
$H_FROM: <input name="name" type="text" value="$DefName" size="$NAME_LENGTH"><br>
$H_MAIL: <input name="mail" type="text" value="$DefEmail" size="$MAIL_LENGTH"><br>
$H_URL_S:<br>
<input name="url" type="text" value="$DefUrl" size="$URL_LENGTH">
</p>
<p>
��$H_ALIAS�פˡ�$H_FROM��$H_MAIL��$H_URL����Ͽ�ʤ��äƤ������ϡ�
��$H_FROM�פˡ�#...�פȤ�����Ͽ̾��񤤤Ƥ���������
��ưŪ��$H_FROM��$H_MAIL��$H_URL������ޤ���
__EOF__

	$msg .= "(" . &TagA( "$PROGRAM?c=as", "$H_ALIAS�ΰ���" ) . " // \n";
	$msg .= &TagA( "$PROGRAM?c=an", "$H_ALIAS����Ͽ" ) . ")\n</p>\n";
    }
    elsif ( $SYS_ALIAS == 2 )
    {
	# �����ꥢ������Ͽ���ʤ���н񤭹��ߤǤ��ʤ�
	# �����ꥢ�����ɤ߹���
	&CacheAliasData;
	$msg .=<<__EOF__;
<p>
$H_USER:
<SELECT NAME="name">
<OPTION SELECTED>$H_FROM����Ͽ����$H_ALIAS������Ǥ�������
__EOF__

	while (( $Key, $Value ) = each %Name )
	{
	    $msg .= "<OPTION>$Key\n";
	}
	$msg .=<<__EOF__;
</SELECT>
</p>
<p>
ͽ���$H_ALIAS�פˡ�$H_FROM��$H_MAIL��$H_URL����Ͽ���ʤ��Ƚ񤭹���ޤ���
��Ͽ�����塤��#...�פȤ�����Ͽ̾����ꤷ�Ƥ���������
__EOF__

	$msg .= "(" . &TagA( "$PROGRAM?c=as", "$H_ALIAS�ΰ���" ) . " // \n";
	$msg .=&TagA( "$PROGRAM?c=an", "$H_ALIAS����Ͽ" ) . ")<br>\n";
	$msg .=<<__EOF__;
��Ͽ����$H_ALIAS��ɽ������ʤ�(����Ǥ��ʤ�)��硤
���Υڡ�������ɤ߹��ߤ��Ƥ���������
</p>
__EOF__
    }
    else
    {
	# HTTP-Cookies��Ȥ���
	$msg .=<<__EOF__;
<p>
<input name="cookies" type="hidden" value="on">
$H_FROM: <input name="name" type="text" value="$DefName" size="$NAME_LENGTH"><br>
$H_MAIL: <input name="mail" type="text" value="$DefEmail" size="$MAIL_LENGTH"><br>
$H_URL_S:<br>
<input name="url" type="text" value="$DefUrl" size="$URL_LENGTH">
</p>
<p>
���ʤ��Υ֥饦������HTTP-Cookies��Ȥ�������ˤʤäƤ����硤
�����ǻ��ꤷ��$H_FROM��$H_MAIL��$H_URL��
���ʤ��Υ֥饦����˵�������ޤ���
����ν񤭹��ߤκݤϡ����ε������줿��������ѤǤ��ޤ���
</p>
__EOF__
    }

    if ( $SYS_MAIL & 2 )
    {
	$msg .= "<p>$H_REPLY�����ä����˥ᥤ����Τ餻�ޤ���? <input name=\"fmail\" type=\"checkbox\" value=\"on\"></p>\n";
    }
    
    # unlock system
    &cgi'unlock( $LOCK_FILE_B ) unless $PC;

    # �ܥ���
    $msg .=<<__EOF__;
<input type="radio" name="com" value="p" CHECKED>: ���ɽ�����Ƥߤ�(�ޤ���Ƥ��ޤ���)<br>
__EOF__

    if ( $Supersede && $SYS_F_D )
    {
	$msg .= "<input type=\"radio\" name=\"com\" value=\"x\">: �������ޤ�<br>\n";
    }
    else
    {
	$msg .= "<input type=\"radio\" name=\"com\" value=\"x\">: $H_MESG����Ƥ���<br>\n";
    }

    local( %tags, $str );
    local( $op ) = ( -M $BOARD_ALIAS_FILE );
    %tags = ( 'b', $BOARD, 'c', 'p', 'id', $Id, 's', $Supersede, 'op', $op );
    &TagForm( *str, *tags, "�¹�", '', *msg );
    &cgiprint'Cache( $str );

    &MsgFooter;
}

1;
