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
AliasShow:
{
    &LockAll;
    &CacheAliasData;
    &UnlockAll;

    # ɽ�����̤κ���
    &MsgHeader( 'Alias view', "$H_ALIAS�λ���" );

    # ������ʸ
    if (( $SYS_ALIAS == 1 ) || ( $SYS_ALIAS == 3 ))
    {
	&cgiprint'Cache(<<__EOF__);
<p>
��Ƥκݡ���$H_FROM�פ���ʬ�˰ʲ�����Ͽ̾(��\#....��)�����Ϥ���ȡ�
��Ͽ����Ƥ���$H_FROM��$H_MAIL��$H_URL����ưŪ������ޤ���
</p><p>
__EOF__
	&cgiprint'Cache( &TagA( "$PROGRAM?c=an", "������Ͽ/��Ͽ���Ƥ��ѹ�" ) . "\n</p>\n" );
    }
    elsif ( $SYS_ALIAS == 2 )
    {
	&cgiprint'Cache(<<__EOF__);
<p>
��Ƥκݡ���$H_USER�פǰʲ�����Ͽ̾(��\#....��)����ꤹ��ȡ�
��Ͽ����Ƥ���$H_FROM��$H_MAIL��$H_URL����ưŪ������ޤ���
</p><p>
__EOF__
	&cgiprint'Cache( &TagA( "$PROGRAM?c=an", "������Ͽ/��Ͽ���Ƥ��ѹ�" ) . "\n</p>\n" );
    }
    else
    {
	# ���ꤨ�ʤ����Ϥ�
	&Fatal(9999, '');
    }

    # �ꥹ�ȳ���
    &cgiprint'Cache( "<dl>\n" );
    
    # 1�Ĥ���ɽ��
    local( $Alias );
    foreach $Alias ( sort keys( %Name ))
    {
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
    &cgiprint'Cache( "</dl>\n" );

    &MsgFooter;
}

1;
