###
## AliasNew - �����ꥢ������Ͽ���ѹ����̤�ɽ��
#
# - SYNOPSIS
#	AliasNew;
#
# - ARGS
#	�ʤ�
#
# - DESCRIPTION
#	�����ꥢ������Ͽ���ѹ����̤�ɽ������(ɽ���������)��
#
# - RETURN
#	�ʤ�
#
AliasNew: {

    # ɽ�����̤κ���
    &MsgHeader('Alias entry/edit', "$H_ALIAS����Ͽ/�ѹ�/���");

    # ������Ͽ/��Ͽ���Ƥ��ѹ�
    &cgiprint'Cache(<<__EOF__);
<p>
������Ͽ/��Ͽ���Ƥ��ѹ�
</p>
<p>
<form action="$PROGRAM" method="POST">
<input name="c" type="hidden" value="am">
$H_ALIAS: <input name="alias" type="text" value="#" size="$NAME_LENGTH"><br>
$H_FROM: <input name="name" type="text" size="$NAME_LENGTH"><br>
$H_MAIL: <input name="email" type="text" size="$MAIL_LENGTH"><br>
$H_URL_S:<br>
<input name="url" type="text" value="http://" size="$URL_LENGTH"><br>
$H_ALIAS�ο�����Ͽ/��Ͽ���Ƥ��ѹ���Ԥʤ��ޤ���
�����ꥢ����(���ʤ��ʳ���!)ï�ˤǤ�񤭴����뤳�Ȥ��Ǥ��ޤ���
��Ͽ���Ƥ��ѹ�����Ƥ��ʤ����ɤ�����
�񤭹�����Ρֻ��ɽ������ײ��̤���դ��ƥ����å����Ƥ���������
�ޤ����ְ�ä�Ʊ�������ꥢ������Ͽ����Ƥ��ޤ�ʤ��褦�ˡ�
���ޤ�˴�ñ�ʡ֥����ꥢ���פ��򤱤Ƥ��������͡�<br>
<input type="submit" value="��Ͽ/�ѹ�����">
</form>
</p>
<hr>
<p>
���
</p>
<p>
<form action="$PROGRAM" method="POST">
<input name="c" type="hidden" value="ad">
$H_ALIAS: <input name="alias" type="text" size="$NAME_LENGTH"><br>
�嵭$H_ALIAS�������ޤ���<br>
<input type="submit" value="�������">
</form>
</p>
<hr>
<p>
<form action="$PROGRAM" method="POST">
<input name="c" type="hidden" value="as">
<input type="submit" value="$H_ALIAS�����򻲾Ȥ���">
</form>
</p>
__EOF__
    
    # ����«
    &MsgFooter;

}

1;
