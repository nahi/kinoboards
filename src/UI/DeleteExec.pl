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

    $Id = $cgi'TAGS{'id'};

    # ����¹�
    &DeleteArticle($Id, $BOARD, $ThreadFlag);

    # ɽ�����̤κ���
    &MsgHeader('Message deleted', "$BOARDNAME: $H_MESG���������ޤ���");

    &PrintButtonToTitleList($BOARD);
    &PrintButtonToBoardList;

    # ����«
    &MsgFooter;

}

1;
