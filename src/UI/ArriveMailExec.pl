###
## ArriveMailExec - �ᥤ�뼫ư�ۿ��������
#
# - SYNOPSIS
#	ArriveMailExec;
#
# - ARGS
#	�ʤ�
#
# - DESCRIPTION
#	�ᥤ�뼫ư�ۿ�������ꤹ�롥
#	����ѿ��Ǥ��롤CGI�ѿ��򻲾Ȥ��롥
#
# - RETURN
#	�ʤ�
#
ArriveMailExec:
{
    &LockBoard;

    # ����ꥹ�Ȥ���Ф�
    local( @ArriveMail ) = split(/\n/, $cgi'TAGS{'armail'});
    &UpdateArriveMailDb($BOARD, *ArriveMail); # DB�򹹿�����

    &UnlockBoard;

    &MsgHeader( 'ArriveMail Changed', "��ư�ᥤ���ۿ�������ꤷ�ޤ���" );

    &cgiprint'Cache(<<__EOF__);
<p>
����$H_BOARD��$H_MESG���񤭹��ޤ줿���ˡ���ư�ǥᥤ����ۿ����밸���
�ʲ��Τ褦�����ꤷ�ޤ�����
</p><p>
<pre>
--------------------
__EOF__

    foreach ( @ArriveMail ) { &cgiprint'Cache("$_\n"); }

    &cgiprint'Cache(<<__EOF__);
--------------------
</pre></p>
__EOF__

    &PrintButtonToTitleList( $BOARD, 0 );
    &PrintButtonToBoardList if $SYS_F_B;
    &MsgFooter;
}

1;
