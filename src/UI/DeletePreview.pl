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
DeletePreview: {

    local($Id);

    # lock system
    local( $lockResult ) = $PC ? 1 : &cgi'lock( $LOCK_FILE_B );
    &Fatal(1001, '') if ( $lockResult == 2 );
    &Fatal(999, '') if ( $lockResult != 1 );
    # cache article DB
    if ( $BOARD ) { &DbCache( $BOARD ); }
    # unlock system
    &cgi'unlock( $LOCK_FILE_B ) unless $PC;

    $Id = $cgi'TAGS{'id'};

    # ɽ�����̤κ���
    &MsgHeader("Delete Article", "$H_MESG�κ��");

    &cgiprint'Cache(<<__EOF__);
<p>
�����ˤ���$H_MESG��������ΤǤ���? �������Хܥ���򲡤��Ƥ���������
</p>
__EOF__

    local( %tags, $str );
    %tags = ( 'c', 'de', 'b', $BOARD, 'id', $Id );
    &TagForm( *str, *tags, "���ε����������ޤ�", '', '' );
    &cgiprint'Cache( $str );

    %tags = ( 'c', 'det', 'b', $BOARD, 'id', $Id );
    &TagForm( *str, *tags, "��ץ饤������ޤȤ�ƺ�����ޤ�", '', '' );
    &cgiprint'Cache( $str );

    &cgiprint'Cache( $H_HR );

    # ����ե������ɽ��
    &ViewOriginalArticle($Id, 0, 1);

    # ����«
    &MsgFooter;

}

1;
