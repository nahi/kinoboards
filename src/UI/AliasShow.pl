###
## AliasShow - �桼�������ꥢ�����Ȳ��̤�ɽ��
#
# - SYNOPSIS
#	AliasShow;
#
# - ARGS
#	�ʤ�
#
# - DESCRIPTION
#	�桼�������ꥢ���ΰ�����ɽ��������̤�������롥
#
# - RETURN
#	�ʤ�
#
AliasShow: {

    local($Alias);

    # lock system
    local( $lockResult ) = &cgi'lock( $LOCK_FILE );
    &Fatal(1001, '') if ( $lockResult == 2 );
    &Fatal(999, '') if ( $lockResult != 1 );

    # �����ꥢ�����ɤ߹���
    &CashAliasData;

    # unlock system
    &cgi'unlock( $LOCK_FILE );
    
    # ɽ�����̤κ���
    &MsgHeader('Alias view', "$H_ALIAS�λ���");

    # ������ʸ
    if ($SYS_ALIAS == 1) {
	&cgiprint'Cache(<<__EOF__);
<p>
��Ƥκݡ���$H_FROM�פ���ʬ�˰ʲ�����Ͽ̾(��#....��)�����Ϥ���ȡ�
��Ͽ����Ƥ���$H_FROM��$H_MAIL��$H_URL����ưŪ������ޤ���
</p><p>
<a href="$PROGRAM?c=an">������Ͽ/��Ͽ���Ƥ��ѹ�</a>
</p>
__EOF__

    } elsif ($SYS_ALIAS == 2) {
					  
	&cgiprint'Cache(<<__EOF__);
<p>
��Ƥκݡ���$H_USER�פǰʲ�����Ͽ̾(��#....��)����ꤹ��ȡ�
��Ͽ����Ƥ���$H_FROM��$H_MAIL��$H_URL����ưŪ������ޤ���
</p><p>
<a href="$PROGRAM?c=an">������Ͽ/��Ͽ���Ƥ��ѹ�</a>
</p>
__EOF__

    } else {
	# ���ꤨ�ʤ����Ϥ�
	&Fatal(9999, '');
    }

    # �ꥹ�ȳ���
    &cgiprint'Cache("<dl>\n");
    
    # 1�Ĥ���ɽ��
    foreach $Alias (sort keys(%Name)) {
	&cgiprint'Cache(<<__EOF__);
<p>
<dt><strong>$Alias</strong>
<dd>$H_FROM: $Name{$Alias}
<dd>$H_MAIL: $Email{$Alias}
<dd>$H_URL: $URL{$Alias}
</p>
__EOF__

    }

    # �ꥹ���Ĥ���
    &cgiprint'Cache("</dl>\n");
    
    &MsgFooter;

}

1;
