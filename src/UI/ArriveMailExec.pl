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
ArriveMailExec: {

    local(@ArriveMail);

    # lock system
    local( $lockResult ) = &cgi'lock( $LOCK_FILE ) unless $PC;
    &Fatal(1001, '') if ( $lockResult == 2 );
    &Fatal(999, '') if ( $lockResult != 1 );

    @ArriveMail = split(/\n/, $cgi'TAGS{'armail'}); # ����ꥹ�Ȥ���Ф�
    &UpdateArriveMailDb($BOARD, *ArriveMail); # DB�򹹿�����

    # unlock system
    &cgi'unlock( $LOCK_FILE ) unless $PC;

    &MsgHeader("ArriveMail Changed", "��ư�ᥤ���ۿ�������ꤷ�ޤ���");

    &cgiprint'Cache(<<__EOF__);
<p>
����$H_BOARD��$H_MESG���񤭹��ޤ줿���ˡ���ư�ǥᥤ����ۿ����밸���
�ʲ��Τ褦�����ꤷ�ޤ�����
</p><p>
<pre>
--------------------
__EOF__

    foreach(@ArriveMail) { &cgiprint'Cache("$_\n"); }

    &cgiprint'Cache(<<__EOF__);
--------------------
</pre></p>
__EOF__

    &PrintButtonToTitleList($BOARD);
    &PrintButtonToBoardList;

    &MsgFooter;

}

1;
