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
AliasDel: {

    local($A, $HitFlag, $Alias);

    # lock system
    local( $lockResult ) = $PC ? 1 : &cgi'lock( $LOCK_FILE );
    &Fatal(1001, '') if ( $lockResult == 2 );
    &Fatal(999, '') if ( $lockResult != 1 );

    # �����ꥢ��
    $A = $cgi'TAGS{'alias'};

    # �ޥ��󤬥ޥå�������
    #	0 ... �����ꥢ�����ޥå����ʤ�
    #	2 ... �ޥå����ƥǡ������ѹ�����
    $HitFlag = 0;

    # �����ꥢ�����ɤ߹���
    &CashAliasData;
    
    # 1�Ԥ��ĥ����å�
    foreach $Alias (sort keys(%Name)) {
	next if ($A ne $Alias);
	$HitFlag = 2;		# �ҥåȤ�����2�����ꡥ�ޥ���̾��̵�롥
    }
    
    # �����ꥢ�����ʤ�!
    if ($HitFlag == 0) { &Fatal(6, $A); }
    
    # ̾����ä�
    $Name{$A} = '';
    
    # �����ꥢ���ե�����˽񤭽Ф�
    &WriteAliasData;
    
    # unlock system
    &cgi'unlock( $LOCK_FILE ) unless $PC;

    # ɽ�����̤κ���
    &MsgHeader('Alias deleted', "$H_ALIAS���������ޤ���");
    &cgiprint'Cache("<p>$H_ALIAS: <strong>$A</strong>: �õ�ޤ�����</p>\n");
    &MsgFooter;

}

1;
