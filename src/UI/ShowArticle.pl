###
## ShowArticle - ñ�쵭����ɽ��
#
# - SYNOPSIS
#	ShowArticle;
#
# - ARGS
#	�ʤ�
#
# - DESCRIPTION
#	ñ��ε�����ɽ�����롥
#       ����ѿ��Ǥ��롤CGI�ѿ��򻲾Ȥ��롥
#
# - RETURN
#	�ʤ�
#
ShowArticle:
{
    &LockBoard;
    # cache article DB
    &DbCache( $BOARD ) if $BOARD;

    local( $id ) = $cgi'TAGS{'id'};
    local( $fId, $aids, $date, $subject ) = &GetArticlesInfo( $id );

    # ̤��Ƶ������ɤ�ʤ�
    &Fatal( 8, '' ) if ( $subject eq '' );

    # ɽ�����̤κ���
    &MsgHeader( 'Message view', $subject );
    &ViewOriginalArticle( $id, 1, 1 );
    &ReplyArticles( split( /,/, $aids ));
    &MsgFooter;

    &UnlockBoard;
}

1;
