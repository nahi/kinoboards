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
    local( $lockResult ) = &cgi'lock( $LOCK_FILE ) unless $PC;
    &Fatal(1001, '') if ( $lockResult == 2 );
    &Fatal(999, '') if ( $lockResult != 1 );
    # cash article DB
    if ( $BOARD ) { &DbCash( $BOARD ); }
    # unlock system
    &cgi'unlock( $LOCK_FILE ) unless $PC;

    $Id = $cgi'TAGS{'id'};

    # �ե����������ڹ�¤�μ���
    # ex. '( a ( b ( c d ) ) ( e ) ( f ( g ) ) )'�Ȥ����ꥹ��
    @FollowIdTree = &GetFollowIdTree($Id);

    # ɽ�����̤κ���
    &MsgHeader('Message view (threaded)', "$H_REPLY��ޤȤ��ɤ�");

    # �ᥤ��ؿ��θƤӽФ�(��������)
    &ThreadArticleMain('subject only', @FollowIdTree);

    # �ᥤ��ؿ��θƤӽФ�(����)
    &ThreadArticleMain('', @FollowIdTree);

    &MsgFooter;

}

1;
