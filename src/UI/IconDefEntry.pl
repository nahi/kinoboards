# ̤�����ˤĤ���ա������ǥ��󥰤�������ä��ꤷ�ơ�

# �ȥ�󥶥�����ʥ�ǤϤʤ��Τ���ա�
# �ե����뤬����뤳�ȤϤʤ�����2�椬Ʊ�����ѹ���Ȥ򤹤�ȡ�
# ������ܤ�����������ե������ȿ�Ǥ���ʤ����Ȥ����롥
IconDef:
{
    local( $iconDefId ) = ( $gVarIconDefId );

    
    &LockAll;
    &CacheIconDb( ?? );
    &UnlockAll;

    &MsgHeader( "Icon Definition", "�����������" );

    &Fatal( 17, '' ) unless $SYS_ICON;

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


    &LockBoard;
    &GetArriveMailTo(1, $BOARD, *ArriveMail); # ����ȥ����Ȥ���Ф�
    &UnlockBoard;

    &cgiprint'Cache(<<__EOF__);
<p>
����$H_BOARD��$H_MESG���񤭹��ޤ줿���ˡ�
��ư�ǥᥤ����ۿ����밸��Υᥤ�륢�ɥ쥹�����ꤷ�ޤ���
1�Ԥ�1�ᥤ�륢�ɥ쥹���Ľ񤭹���Ǥ���������
��Ƭ�ˡ�#�פ�Ĥ���Ȥ��ιԤ�̵�뤵���Τǡ�
#��³���ƥ����Ȥ�񤭹��ळ�Ȥ�Ǥ��ޤ���
</p><p>
�ä˼³��Ϥ���ޤ��󤬡�̵��̣�ʶ��Ԥ����ꤹ���ʤ��褦����դ��ޤ��礦��
</p>
__EOF__

    local( %tags, $msg, $str );
    $msg = "<textarea name=\"armail\" rows=\"$TEXT_ROWS\" cols=\"$MAIL_LENGTH\">\n";
    foreach ( @ArriveMail ) { $msg .= "$_\n"; }
    $msg .= "</textarea><br>";

    %tags = ( 'c', 'me', 'b', $BOARD );
    &TagForm( *str, *tags, "���ꤷ�ޤ�", "�ꥻ�åȤ���", *msg );
    &cgiprint'Cache( $str );

    &MsgFooter;
}

1;
