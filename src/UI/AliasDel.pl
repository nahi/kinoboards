###
## AliasDel - �桼�������ꥢ���κ��
#
# - SYNOPSIS
#	AliasDel;
#
# - ARGS
#	�ʤ�
#
# - DESCRIPTION
#	�桼�������ꥢ���������롥��Ͽ�ۥ��Ȥ�Ʊ��Ǥʤ�����Բġ�
#	���θ塤���η�̤��Τ餻����̤�ɽ�����롥
#	����ѿ��Ǥ��롤CGI�ѿ��򻲾Ȥ��롥
#	���ץꥱ��������ǥ�Ȥ⡤GUI�Ȥ���롥ʬΥ�Ǥ��Ƥʤ���
#
# - RETURN
#	�ʤ�
#
AliasDel:
{
    # �����ꥢ��
    local( $alias ) = $cgi'TAGS{'alias'};

    # �ޥ��󤬥ޥå�������
    #	0 ... �����ꥢ�����ޥå����ʤ�
    #	2 ... �ޥå����ƥǡ������ѹ�����
    local( $hitFlag ) = 0;

    &LockAll();

    # �����ꥢ�����ɤ߹���
    &CacheAliasData;
    
    # 1�Ԥ��ĥ����å�
    foreach (sort keys( %Name ))
    {
	next if ( $_ ne $alias );
	$hitFlag = 2;		# ��ä���2�����ꡥ
    }
    
    # �����ꥢ�����ʤ�!
    if ( $hitFlag == 0 ) { &Fatal( 6, $alias ); }
    
    # ̾����ä�
    $Name{$alias} = '';
    
    # �����ꥢ���ե�����˽񤭽Ф�
    &WriteAliasData;
    
    &UnlockAll();

    # ɽ�����̤κ���
    &MsgHeader( 'Alias deleted', "$H_ALIAS���������ޤ���" );
    &cgiprint'Cache("<p>$H_ALIAS: <strong>$alias</strong>: �õ�ޤ�����</p>\n");
    &MsgFooter;
}

1;
