###
## DeletePreview - ��������γ�ǧ
#
# - SYNOPSIS
#	DeletePreview;
#
# - ARGS
#	�ʤ�
#
# - DESCRIPTION
#	��������γ�ǧ���̤�ɽ������
#       ����ѿ��Ǥ��롤CGI�ѿ��򻲾Ȥ��롥
#
# - RETURN
#	�ʤ�
#
DeletePreview:
{
    &LockBoard;
    # cache article DB
    &DbCache( $BOARD ) if $BOARD;
    &UnlockBoard;

    local( $id ) = $cgi'TAGS{'id'};
    local( $fId, $aids, $date, $subject ) = &GetArticlesInfo( $id );

    # ̤��Ƶ������ɤ�ʤ�
    if ( $subject eq '' ) { &Fatal( 8, '' ); }

    # ɽ�����̤κ���
    &MsgHeader( 'Delete Article', "$H_MESG�κ��" );

    &cgiprint'Cache(<<__EOF__);
<p>
�����ˤ���$H_MESG��������ΤǤ���? �������Хܥ���򲡤��Ƥ���������
</p>
__EOF__

    local( %tags, $str );
    %tags = ( 'c', 'de', 'b', $BOARD, 'id', $id );
    &TagForm( *str, *tags, "���ε����������ޤ�", '', '' );
    &cgiprint'Cache( $str );

    if ( $aids )
    {
	%tags = ( 'c', 'det', 'b', $BOARD, 'id', $id );
	&TagForm( *str, *tags, "��ץ饤������ޤȤ�ƺ�����ޤ�", '', '' );
	&cgiprint'Cache( $str );
    }

    &cgiprint'Cache( $H_HR );

    # ����ե������ɽ��
    &ViewOriginalArticle( $id, 0, 1 );

    &ReplyArticles( split( /,/, $aids ));
    &MsgFooter;
}

1;
