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
ArriveMailEntry:
{
    local(@ArriveMail);

    &LockBoard;
    &GetArriveMailTo(1, $BOARD, *ArriveMail); # ����ȥ����Ȥ���Ф�
    &UnlockBoard;

    &MsgHeader("ArriveMail Entry", "��ư�ᥤ���ۿ��������");
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
