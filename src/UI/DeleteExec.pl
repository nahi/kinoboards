###
## DeleteExec - �����κ��
#
# - SYNOPSIS
#	DeleteExec($ThreadFlag);
#
# - ARGS
#	$ThreadFlag	��ץ饤��ä����ݤ�
#
# - DESCRIPTION
#	�����κ����¹Ԥ��������β��̤�ɽ�����롥
#       ����ѿ��Ǥ��롤CGI�ѿ��򻲾Ȥ��롥
#
# - RETURN
#	�ʤ�
#
DeleteExec: {
    local($ThreadFlag) = $gVarThreadFlag;
    local($Id);

    # lock system
    local( $lockResult ) = $PC ? 1 : &cgi'lock( $LOCK_FILE_B );
    &Fatal(1001, '') if ( $lockResult == 2 );
    &Fatal(999, '') if ( $lockResult != 1 );
    # cache article DB
    if ( $BOARD ) { &DbCache( $BOARD ); }

    $Id = $cgi'TAGS{'id'};

    # ����¹�
    &DeleteArticle($Id, $BOARD, $ThreadFlag);

    # unlock system
    &cgi'unlock( $LOCK_FILE_B ) unless $PC;

    # ɽ�����̤κ���
    &MsgHeader('Message deleted', "$H_MESG���������ޤ���");

    &PrintButtonToTitleList($BOARD);
    &PrintButtonToBoardList if $SYS_F_B;

    # ����«
    &MsgFooter;

}

1;
