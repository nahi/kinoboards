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
    local( $lockResult ) = &cgi'lock( $LOCK_FILE );
    &Fatal(1001, '') if ( $lockResult == 2 );
    &Fatal(999, '') if ( $lockResult != 1 );
    # cash article DB
    if ( $BOARD ) { &DbCash( $BOARD ); }

    $Id = $cgi'TAGS{'id'};

    # ����¹�
    &DeleteArticle($Id, $BOARD, $ThreadFlag);

    # unlock system
    &cgi'unlock( $LOCK_FILE );

    # ɽ�����̤κ���
    &MsgHeader('Message deleted', "$BOARDNAME: $H_MESG���������ޤ���");

    &PrintButtonToTitleList($BOARD);
    &PrintButtonToBoardList;

    # ����«
    &MsgFooter;

}

1;
