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
AliasMod: {

    local($A, $N, $E, $U, $HitFlag, $Alias);

    $A = $cgi'TAGS{'alias'};
    $N = $cgi'TAGS{'name'};
    $E = $cgi'TAGS{'email'};
    $U = $cgi'TAGS{'url'};
    
    # �ޥ��󤬥ޥå�������
    #	0 ... �����ꥢ�����ޥå����ʤ�
    #	2 ... �ޥå����ƥǡ������ѹ�����
    $HitFlag = 0;

    # ʸ��������å�
    &AliasCheck($A, $N, $E, $U);
    
    # �����ꥢ�����ɤ߹���
    &CashAliasData;
    
    # 1�Ԥ��ĥ����å�
    foreach $Alias (sort keys(%Name)) {
	next if ($A ne $Alias);
	$HitFlag = 2;		# ��ä���2�����ꡥ�ޥ���̾��̵�롥
    }
    
    # ������Ͽ
    if ($HitFlag == 0) {
	$Alias = $A;
    }
    
    # �ǡ�������Ͽ
    $Name{$Alias} = $N;
    $Email{$Alias} = $E;
    $Host{$Alias} = $REMOTE_HOST;
    $URL{$Alias} = $U;
    
    # �����ꥢ���ե�����˽񤭽Ф�
    &WriteAliasData;

    # ɽ�����̤κ���
    &MsgHeader('Alias modified', "$H_ALIAS�����ꤵ��ޤ���");
    &cgiprint'Cache("<p>$H_ALIAS: <strong>$A</strong>:\n");
    if ($HitFlag == 2) {
	&cgiprint'Cache("���ꤷ�ޤ�����</p>\n");
    } else {
	&cgiprint'Cache("��Ͽ���ޤ�����</p>\n");
    }
    &MsgFooter;
    
}

1;
