###
## ArriveMailEntry - �ᥤ�뼫ư�ۿ���λ���
#
# - SYNOPSIS
#	ArriveMailEntry;
#
# - ARGS
#	�ʤ�
#
# - DESCRIPTION
#	�ᥤ�뼫ư�ۿ���λ�����̤�ɽ�����롥
#
# - RETURN
#	�ʤ�
#
ArriveMailEntry: {

    local(@ArriveMail);

    # lock system
    local( $lockResult ) = &cgi'lock( $LOCK_FILE );
    &Fatal(1001, '') if ( $lockResult == 2 );
    &Fatal(999, '') if ( $lockResult != 1 );

    &GetArriveMailTo(1, $BOARD, *ArriveMail); # ����ȥ����Ȥ���Ф�

    # unlock system
    &cgi'unlock( $LOCK_FILE );

    &MsgHeader("ArriveMail Entry", "$BOARDNAME: ��ư�ᥤ���ۿ��������");

    &cgiprint'Cache(<<__EOF__);
<p>
����$H_BOARD��$H_MESG���񤭹��ޤ줿���ˡ�
��ư�ǥᥤ����ۿ����밸��Υᥤ�륢�ɥ쥹�����ꤷ�ޤ���
1�Ԥ�1�ᥤ�륢�ɥ쥹���Ľ񤭹���Ǥ���������
��Ƭ�ˡ�#�פ�Ĥ���Ȥ��ιԤ�̵�뤵���Τǡ�
#��³���ƥ����Ȥ�񤭹��ळ�Ȥ�Ǥ��ޤ���
</p><p>
�ä˼³��Ϥ���ޤ��󤬡�̵��̣�ʶ��Ԥ����ꤹ���ʤ��褦����դ��ޤ��礦��
</p><p>
<form action="$PROGRAM" method="POST">
<input name="c" type="hidden" value="me">
<input name="b" type="hidden" value="$BOARD">
<textarea name="armail" rows="$TEXT_ROWS" cols="$MAIL_LENGTH">
__EOF__

    foreach(@ArriveMail) { &cgiprint'Cache("$_\n"); }

    &cgiprint'Cache(<<__EOF__);
</textarea><br>
<input type="submit" value="���ꤷ�ޤ�">
<input type="reset" value="�ꥻ�åȤ���">
</form>
</p>
__EOF__

    &MsgFooter;

}

1;
