###
## Entry - �񤭹��߲��̤�ɽ��
#
# - SYNOPSIS
#	Entry( $entryType, $back );
#
# - ARGS
#	$entryType	0 ... ����
#			1 ... ���Ѥʤ��Υ�ץ饤
#			2 ... ���Ѥ���Υ�ץ饤
#			3 ... ��ƺѤߵ���������
#	$back		�ץ�ӥ塼�������꤫�ݤ���
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
    local( $entryType, $back ) = ( $gVarEntryType, $gVarBack );

    &LockBoard;
    # cache article DB
    &DbCache( $BOARD ) if ( $BOARD && ( $entryType != 0 ));

    local( $Id ) = $cgi'TAGS{'id'};
    local( $COrig ) = $cgi'TAGS{'c'};

    local( $DefSubject, $DefName, $DefEmail, $DefUrl, $DefTextType, $DefIcon, $DefArticle, $DefFmail );
    if ( $back )
    {
	require( 'mimer.pl' );
	$DefSubject = $cgi'TAGS{'subject'};
	$DefName = $cgi'TAGS{'name'};
	$DefEmail = $cgi'TAGS{'mail'};
	$DefUrl = $cgi'TAGS{'url'};
	$DefTextType = $cgi'TAGS{'texttype'};
	$DefIcon = $cgi'TAGS{'icon'};
	$DefArticle = $cgi'TAGS{'article'};
	$DefFmail = $cgi'TAGS{'fmail'};

	$DefArticle = &MIME'base64decode( $DefArticle );
    }
    elsif ( $entryType == 0 )
    {
	if ( $SYS_ALIAS == 3 )
	{
	    &cgi'Cookie();
	    ( $DefName, $DefEmail, $DefUrl ) = split( /$COLSEP/,
		$cgi'COOKIES{ 'kb10info' });
	}
	$DefUrl = $DefUrl || 'http://';
    }
    elsif ( $entryType == 1 )
    {
	if ( $SYS_ALIAS == 3 )
	{
	    &cgi'Cookie();
	    ( $DefName, $DefEmail, $DefUrl ) = split( /$COLSEP/,
		$cgi'COOKIES{ 'kb10info' });
	}
	$DefUrl = $DefUrl || 'http://';
	local( $fId, $aids, $date, $subject ) = &GetArticlesInfo( $Id );
	$DefSubject = $subject;
	&GetReplySubject( *DefSubject );
    }
    elsif ( $entryType == 2 )
    {
	if ( $SYS_ALIAS == 3 )
	{
	    &cgi'Cookie();
	    ( $DefName, $DefEmail, $DefUrl ) = split( /$COLSEP/,
		$cgi'COOKIES{ 'kb10info' });
	}
	$DefUrl = $DefUrl || 'http://';
	local( $fId, $aids, $date, $subject ) = &GetArticlesInfo( $Id );
	$DefSubject = $subject;
	&GetReplySubject( *DefSubject );
	&QuoteOriginalArticle( $Id, *DefArticle );
    }
    elsif ( $entryType == 3 )
    {
	local( $fId, $aids, $date, $subject, $icon, $remoteHost, $name, $email, $url ) = &GetArticlesInfo( $Id );
	$DefSubject = $subject;
	$DefName = $name;
	$DefEmail = $email;
	$DefUrl = $url;
	$DefIcon = $icon;
	&QuoteOriginalArticleWithoutQMark( $Id, *DefArticle );
    }

    &UnlockBoard;

    # ɽ�����̤κ���
    if ( $entryType == 3 )
    {
	&MsgHeader( 'Supersede entry', "$H_MESG������" );
    }
    else
    {
	&MsgHeader( 'Message entry', "$H_MESG�ν񤭹���" );
    }

    # �ե����ξ��
    if (( $entryType == 1 ) || ( $entryType == 2 ))
    {
	# ������ɽ��(���ޥ��̵��, ����������)
	&ViewOriginalArticle( $Id, 0, 1 );
	if ( $entryType == 3 )
	{
	    &cgiprint'Cache(<<__EOF__);
$H_HR
<h2>���$H_MESG����������</h2>
���$H_MESG�����촹����$H_MESG��񤭹���Ǥ���������
__EOF__
	}
	else
	{
	    &cgiprint'Cache(<<__EOF__);
$H_HR
<h2>���$H_MESG�ؤ�$H_REPLY��񤭹���</h2>
__EOF__
	}
    }

    local( $msg ) = "<p>\n";

    local( $ttFlag ) = 0;
    local( $ttBit ) = 0;
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
	&CacheIconDb;	# ��������DB�򥭥�å���
	$msg .= sprintf( "$H_ICON:\n<SELECT NAME=\"icon\">\n<OPTION%s>$H_NOICON\n", $DefIcon? '' : ' SELECTED' );
	local( $IconTitle );
	foreach $IconTitle ( @ICON_TITLE )
	{
	    $msg .= sprintf( "<OPTION%s>$IconTitle\n",
		( $IconTitle eq $DefIcon )? ' SELECTED' : '' );
	}
	$msg .= "</SELECT>\n";

	$msg .= "(" . &TagA( "$PROGRAM?b=$BOARD&c=i&type=entry",
	    "�������������" ) . ")<BR>\n";
    }

    # Subject(�ե����ʤ鼫ưŪ��ʸ����������)
    $msg .= sprintf( "%s: <input name=\"subject\" type=\"text\" value=\"%s\" size=\"%s\"><br>\n", $H_SUBJECT, $DefSubject, $SUBJECT_LENGTH );

    # TextType
    if ( $ttFlag )
    {
	$ttFlag = 0 if $DefTextType;
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
		    $msg .= sprintf( "<OPTION%s>" . $H_TTLABEL[$ttBit] . "\n",
			( $H_TTLABEL[$ttBit] eq $DefTextType )? ' SELECTED' :
			'' );
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

    # ��ʸ
    $msg .= "<p><textarea name=\"article\" rows=\"$TEXT_ROWS\" cols=\"$TEXT_COLS\">$DefArticle</textarea></p>\n";

    # �եå���ʬ��ɽ��
    # ̾���ȥᥤ�륢�ɥ쥹��URL��
    $msg .=<<__EOF__;
<p>
$H_MESG��˴�Ϣ�����֥ڡ����ؤΥ�󥯤�ĥ����ϡ�
��&lt;URL:http://��&gt;�פΤ褦�ˡ�URL���&lt;URL:�פȡ�&gt;�פǰϤ��
�񤭹���Ǥ�����������ưŪ�˥�󥯤�ĥ���ޤ���
����$H_BOARD�����$H_MESG�˥�󥯤�ĥ����ϡ���&lt;URL:kb:71&gt;�פΤ褦�ˡ�
$H_MESG��ID���&lt;URL:kb:�פȡ�&gt;�פǰϤߤޤ���
__EOF__

    if ( $SYS_F_S )
    {
	$msg .= "����$H_BOARD�����$H_MESG��\n";
	$msg .= &TagA( "$PROGRAM?b=$BOARD&c=s", "������ɤǸ�������" );
	$msg .= "���Ȥ��Ǥ��ޤ���\n";
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
	&LockAll;
	&CacheAliasData;
	&UnlockAll;
	$msg .=<<__EOF__;
<p>
$H_USER:
<SELECT NAME="name">
<OPTION SELECTED>$H_FROM����Ͽ����$H_ALIAS������Ǥ�������
__EOF__

	local( $Key, $Value );
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
	$msg .= sprintf( "<p>$H_REPLY�����ä����˥ᥤ����Τ餻�ޤ���? " .
	    "<input name=\"fmail\" type=\"checkbox\" value=\"on\"%s></p>\n",
	    $DefFmail? ' CHECKED' : '' );
    }
    
    # �ܥ���
    $msg .=<<__EOF__;
<input type="radio" name="com" value="p" CHECKED>: ���ɽ�����Ƥߤ�(�ޤ���Ƥ��ޤ���)<br>
__EOF__

    if ( $entryType == 3 )
    {
	$msg .= "<input type=\"radio\" name=\"com\" value=\"x\">: ��������<br>\n";
    }
    else
    {
	$msg .= "<input type=\"radio\" name=\"com\" value=\"x\">: $H_MESG����Ƥ���<br>\n";
    }

    local( %tags, $str );
    local( $op ) = ( -M $BOARD_ALIAS_FILE );
    %tags = ( 'corig', $COrig, 'b', $BOARD, 'c', 'p', 'id', $Id,
	's', ( $entryType == 3 ), 'op', $op );
    &TagForm( *str, *tags, "�¹�", '', *msg );
    &cgiprint'Cache( $str );

    &MsgFooter;
}

1;
