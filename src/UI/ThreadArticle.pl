###
## ThreadArticle - �ե�������������ɽ����
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
ThreadArticle: {

    local($Id, @FollowIdTree);

    # lock system
    local( $lockResult ) = $PC ? 1 : &cgi'lock( $LOCK_FILE_B );
    &Fatal(1001, '') if ( $lockResult == 2 );
    &Fatal(999, '') if ( $lockResult != 1 );
    # cache article DB
    if ( $BOARD ) { &DbCache( $BOARD ); }
    # unlock system
    &cgi'unlock( $LOCK_FILE_B ) unless $PC;

    $Id = $cgi'TAGS{'id'};

    # �ե����������ڹ�¤�μ���
    # ex. '( a ( b ( c d ) ) ( e ) ( f ( g ) ) )'�Ȥ����ꥹ��
    &GetFollowIdTree($Id, *FollowIdTree);

    # ɽ�����̤κ���
    &MsgHeader('Message view (threaded)', "$H_REPLY��ޤȤ��ɤ�");

    # �ᥤ��ؿ��θƤӽФ�(��������)
    &ThreadArticleMain('subject only', @FollowIdTree);

    # �ᥤ��ؿ��θƤӽФ�(����)
    &ThreadArticleMain('', @FollowIdTree);

    &cgiprint'Cache("$H_HR\n");

    &PrintButtonToTitleList($BOARD);
    &PrintButtonToBoardList if $SYS_F_B;

    &MsgFooter;

}

1;
