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

    local( %tags, $msg, $str );

    %tags = ( 'c', 'am' );
    $msg =<<__EOF__;
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
__EOF__
    &TagForm( *str, *tags, "��Ͽ/�ѹ�����", '', *msg );
    &cgiprint'Cache( "<h2>������Ͽ/��Ͽ���Ƥ��ѹ�</h2>\n$str\n$H_HR\n" );

    %tags = ( 'c', 'ad' );
    $msg =<<__EOF__;
$H_ALIAS: <input name="alias" type="text" size="$NAME_LENGTH"><br>
�嵭$H_ALIAS�������ޤ���<br>
__EOF__
    &TagForm( *str, *tags, "�������", '', *msg );
    &cgiprint'Cache( "<h2>���</h2>\n$str\n$H_HR\n" );

    %tags = ( 'c', 'as' );
    &TagForm( *str, *tags, "$H_ALIAS�����򻲾Ȥ���", '', '' );
    &cgiprint'Cache( $str );
    
    # ����«
    &MsgFooter;
}

1;
