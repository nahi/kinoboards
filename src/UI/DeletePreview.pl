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
    local( $lockResult ) = $PC ? 1 : &cgi'lock( $LOCK_FILE );
    &Fatal(1001, '') if ( $lockResult == 2 );
    &Fatal(999, '') if ( $lockResult != 1 );
    # cash article DB
    if ( $BOARD ) { &DbCash( $BOARD ); }
    # unlock system
    &cgi'unlock( $LOCK_FILE ) unless $PC;

    $Id = $cgi'TAGS{'id'};

    # ɽ�����̤κ���
    &MsgHeader("Delete Article", "$H_MESG�κ��");

    &cgiprint'Cache(<<__EOF__);
<p>
�����ˤ���$H_MESG��������ΤǤ���? �������Хܥ���򲡤��Ƥ���������
</p>
__EOF__

    # ����«
    &cgiprint'Cache(<<__EOF__);
<form action="$PROGRAM" method="POST">
<input name="c" type="hidden" value="de">
<input name="b" type="hidden" value="$BOARD">
<input name="id" type="hidden" value="$Id">
<input type="submit" value="���ε����������ޤ�">
</form>
<form action="$PROGRAM" method="POST">
<input name="c" type="hidden" value="det">
<input name="b" type="hidden" value="$BOARD">
<input name="id" type="hidden" value="$Id">
<input type="submit" value="��ץ饤������ޤȤ�ƺ�����ޤ�">
</form>
</p>
<hr>
__EOF__

    # ����ե������ɽ��
    &ViewOriginalArticle($Id, 0, 1);

    # ����«
    &MsgFooter;

}

1;
