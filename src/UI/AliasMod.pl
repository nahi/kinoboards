###
## AliasMod - �桼�������ꥢ������Ͽ/�ѹ�
#
# - SYNOPSIS
#	AliasMod;
#
# - ARGS
#	�ʤ�
#
# - DESCRIPTION
#	�桼�������ꥢ������Ͽ/�ѹ��������η�̤��Τ餻����̤�ɽ�����롥
#	����ѿ��Ǥ��롤CGI�ѿ��򻲾Ȥ��롥
#	���ץꥱ��������ǥ�Ȥ⡤GUI�Ȥ����ġ�ʬΥ�Ǥ��Ƥʤ���
#
# - RETURN
#	�ʤ�
#
AliasMod:
{
    local( $alias ) = $cgi'TAGS{'alias'};
    local( $name ) = $cgi'TAGS{'name'};
    local( $eMail ) = $cgi'TAGS{'email'};
    local( $url ) = $cgi'TAGS{'url'};
    
    # �ޥ��󤬥ޥå�������
    #	0 ... �����ꥢ�����ޥå����ʤ�
    #	2 ... �ޥå����ƥǡ������ѹ�����
    local( $hitFlag ) = 0;

    &LockAll;

    # ʸ��������å�
    &AliasCheck( $alias, $name, $eMail, $url );
    
    # �����ꥢ�����ɤ߹���
    &CacheAliasData;
    
    # 1�Ԥ��ĥ����å�
    foreach (sort keys( %Name ))
    {
	next if ( $_ ne $alias );
	$hitFlag = 2;		# ��ä���2�����ꡥ
    }
    
    # �ǡ�������Ͽ
    $Name{ $alias } = $name;
    $Email{ $alias } = $eMail;
    $URL{ $alias } = $url;
    
    # �����ꥢ���ե�����˽񤭽Ф�
    &WriteAliasData;

    &UnlockAll;

    # ɽ�����̤κ���
    &MsgHeader( 'Alias modified', "$H_ALIAS�����ꤵ��ޤ���" );

    &cgiprint'Cache( "<p>$H_ALIAS: <strong>$alias</strong>:\n" );
    if ( $hitFlag == 2 )
    {
	&cgiprint'Cache( "��Ͽ���ѹ����ޤ�����</p>\n" );
    }
    else
    {
	&cgiprint'Cache( "��������Ͽ���ޤ�����</p>\n" );
    }

    &cgiprint'Cache(<<__EOF__);
<p>
<dl>
<dt>$H_FROM
<dd>$name
<dt>$H_MAIL
<dd>$eMail
<dt>$H_URL
<dd>$url
</dl>
</p>
__EOF__

    &MsgFooter;
}

1;
