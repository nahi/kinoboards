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
DeleteExec:
{
    local( $ThreadFlag ) = $gVarThreadFlag;

    &LockBoard();
    # cache article DB
    &DbCache( $BOARD ) if $BOARD;

    local( $Id ) = $cgi'TAGS{'id'};

    # ����¹�
    &DeleteArticle( $Id, $BOARD, $ThreadFlag );

    &UnlockBoard();

    # ɽ�����̤κ���
    &MsgHeader( 'Message deleted', "$H_MESG���������ޤ���" );
    &PrintButtonToTitleList( $BOARD, $Id );
    &PrintButtonToBoardList if $SYS_F_B;
    &MsgFooter;
}

1;
