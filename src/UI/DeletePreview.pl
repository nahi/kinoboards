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

    $Id = $cgi'TAGS{'id'};

    # ɽ�����̤κ���
    &MsgHeader("Delete Article", "$BOARDNAME: $H_MESG�κ��");

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
