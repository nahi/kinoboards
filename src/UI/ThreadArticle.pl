###
## ThreadArticle - ����å��̵�������
#
# - SYNOPSIS
#	ThreadArticle;
#
# - ARGS
#	�ʤ�
#
# - DESCRIPTION
#	���뵭���ȡ����ε����ؤΥ�ץ饤������ޤȤ��ɽ�����롥
#       ����ѿ��Ǥ��롤CGI�ѿ��򻲾Ȥ��롥
#
# - RETURN
#	�ʤ�
#
ThreadArticle:
{
    &LockBoard;
    &DbCache( $BOARD ) if $BOARD;
    &UnlockBoard;

    local( $Id ) = $cgi'TAGS{'id'};

    # �ե����������ڹ�¤�μ���
    # ex. '( a ( b ( c d ) ) ( e ) ( f ( g ) ) )'�Ȥ����ꥹ��
    local( @FollowIdTree );
    &GetFollowIdTree($Id, *FollowIdTree);

    # ɽ�����̤κ���
    &MsgHeader('Message view (threaded)', "$H_REPLY��ޤȤ��ɤ�");

    # �ᥤ��ؿ��θƤӽФ�(��������)
    &ThreadArticleMain( 1, @FollowIdTree );

    # �ᥤ��ؿ��θƤӽФ�(����)
    &ThreadArticleMain( 0, @FollowIdTree );

    &cgiprint'Cache("$H_HR\n");

    &PrintButtonToTitleList( $BOARD, $Id );
    &PrintButtonToBoardList if $SYS_F_B;

    &MsgFooter;

}

1;
