###
## Fatal - ���顼ɽ��
#
# - SYNOPSIS
#	Fatal($errno, $errInfo);
#
# - ARGS
#	$errno	���顼�ֹ�(�ܤ����ϴؿ������򻲾ȤΤ���)
#	$errInfo	���顼����
#
# - DESCRIPTION
#	���顼��ɽ�����̤�֥饦�����������롥
#
# - RETURN
#	�ʤ�
#
Fatal:
{
    local( $errno, $errInfo ) = ( $gVarFatalNo, $gVarFatalInfo );

    local( $severity, $msg );
    if ( $errno == 1 )
    {
	$severity = $kinologue'SEV_CAUTION;
	$msg = "File: $errInfo��¸�ߤ��ʤ������뤤��permission�����꤬�ְ�äƤ��ޤ���������Ǥ�����" . &TagA( "mailto:$MAINT", $MAINT ) . "�ޤǡ��嵭�ե�����̾���Τ餻��������";
    }
    elsif ( $errno == 2 )
    {
	$severity = $kinologue'SEV_INFO;
	$msg = "���Ϥ���Ƥ��ʤ����ܤ�����ޤ�����äƤ⤦���٤��ľ���ƤߤƤ���������";
    }
    elsif ( $errno == 3 )
    {
	$severity = $kinologue'SEV_INFO;
	$msg = "���̾����$H_MAIL�ˡ�����ʸ�������Ԥ����äƤ��ޤäƤ��ޤ�����äƤ⤦���٤��ľ���ƤߤƤ���������";
    }
    elsif ( $errno == 4 )
    {
	$severity = $kinologue'SEV_INFO;
	$msg = "�����HTML����������뤳�Ȥ϶ؤ����Ƥ��ޤ�����äư㤦��˽񤭴����Ƥ���������";
    }
    elsif ( $errno == 5 )
    {
	$severity = $kinologue'SEV_ERROR;
	$msg = "��Ͽ����Ƥ��륨���ꥢ���Τ�Τȡ��ޥ���̾�����פ��ޤ��󡥤�����Ǥ�����" . &TagA( "mailto:$MAINT", $MAINT ) . "�ޤǸ�Ϣ����������";
    }
    elsif ( $errno == 6)
    {
	$severity = $kinologue'SEV_WARN;
	$msg = "��$errInfo�פȤ��������ꥢ���ϡ���Ͽ����Ƥ��ޤ���";
    }
    elsif ( $errno == 7 )
    {
	$severity = $kinologue'SEV_INFO;
	$msg = "$errInfo��������������ޤ���? ��äƤ⤦���٤��ľ���ƤߤƤ���������";
    }
    elsif ( $errno == 8 )
    {
	$severity = $kinologue'SEV_INFO;
	$msg = "���ε����Ϥޤ���Ƥ���Ƥ��ޤ���";
    }
    elsif ( $errno == 9 )
    {
	local( $board, $id, $info ) = split( /\//, $errInfo, 3 );
	$severity = $kinologue'SEV_CAUTION;
	$msg = "�ۥ��ȥޥ���β����١�$H_MAIL�θ�������ͳ�ˤ�ꡤ������$H_MAIL�Ǥ��ۿ������Ԥ��ޤ����ʷǼ���: $board��ID: $id������: $info�ˡ���å��������������񤭹��ޤ�ޤ����Τǡ����ٽ񤭹��ߤ�ɬ�פϤ���ޤ���";
    }
    elsif ( $errno == 10 )
    {
	$severity = $kinologue'SEV_CAUTION;
	$msg = "kb.db��kb.aid�������������Ƥ��ޤ��󡥤�����Ǥ��������Υ��顼��å������ȡ����顼��������������" . &TagA( "mailto:$MAINT", $MAINT ) . "�ޤǤ��Τ餻����������";
    }
    elsif ( $errno == 11 )
    {
	$severity = $kinologue'SEV_ERROR;
	$msg = "$errInfo�Ȥ���ID���б�����$H_BOARD�ϡ�¸�ߤ��ޤ���";
    }
    elsif ( $errno == 12 )
    {
	$severity = $kinologue'SEV_WARN;
	$msg = "����$H_BOARD�Ǥϡ�$H_MESG�κ��祵������$SYS_MAXARTSIZE�Х��ȤȤ������ȤˤʤäƤ��ޤ��ʤ��ʤ���$H_MESG��$errInfo�Х��ȤǤ��ˡ�";
    }
    elsif ( $errno == 13 )
    {
	$severity = $kinologue'SEV_FATAL;
	$msg = "File: $errInfo�ؤν񤭹��ߤ˼��Ԥ��ޤ������ե����륷���ƥ�˶������̤��ʤ���ǽ��������ޤ���������Ǥ�����" . &TagA( "mailto:$MAINT", $MAINT ) . "�ޤǡ��嵭��å��������Τ餻��������";
    }
    elsif ( $errno == 14 )
    {
	$severity = $kinologue'SEV_FATAL;
	$msg = "�������ͤ�: ����rename�˼��Ԥ��ޤ�����$errInfo�ˡ��ե�����ѡ��ߥå�����������������å����ƤߤƤ���������";
    }
    elsif ( $errno == 15 )
    {
	$severity = $kinologue'SEV_ERROR;
	$msg = "�񤭹��߸������ϥե����ब�Ų᤮�ޤ�������";
    }
    elsif ( $errno == 16 )
    {
	$severity = $kinologue'SEV_ERROR;
	$msg = "Ʊ��񤭹��ߥե����फ���Ϣ³�񤭹��ߤ϶ػߤ���Ƥ��ޤ���Ϣ³���Ƶ�����񤭹�����ϡ��񤭹��ߥե����������ɤ߹���ľ���Ƥ���ˤ��Ƥ���������";
    }
    elsif ( $errno == 17 )
    {
	$severity = $kinologue'SEV_ERROR;
	$msg = "���ߡ�$H_ICON���Ȥ�������ˤʤäƤ��ޤ���$H_ICON��Ȥ���������ѹ����Ƥ�����٤��ľ���Ƥ���������";
    }
    elsif ( $errno == 22 )
    {
	$severity = $kinologue'SEV_INFO;
	$msg = "���դΥե����ޥåȤ�'yyyy/mm/dd'�ǤϤ���ޤ�����äƤ⤦���٤��ľ���ƤߤƤ���������";
    }
    elsif ( $errno == 50 )
    {
	$severity = $kinologue'SEV_INFO;
	$msg = "��ץ饤�ط����۴Ĥ��Ƥ��ޤ��ޤ����ɤ����Ƥ��ץ饤����ѹ���������硤��ץ饤�����ٿ��尷���ˤ��Ƥ��顤��ץ饤�򤫤������Ƥ���������";
    }
    elsif ( $errno == 99 )
    {
	$severity = $kinologue'SEV_WARN;
	$msg ="����$H_BOARD�Ǥϡ����Υ��ޥ�ɡ�$errInfo�ˤϼ¹ԤǤ��ޤ���";
    }
    elsif ( $errno == 999 )
    {
	$severity = $kinologue'SEV_WARN;
	$msg ="�����ƥ�Υ�å��˼��Ԥ��ޤ��������߹�äƤ���褦�Ǥ��Τǡ���ʬ�ԤäƤ���⤦���٥����������Ƥ���������";
    }
    elsif ( $errno == 1000 )
    {
	$severity = $kinologue'SEV_FATAL;
	$msg ="���ե�����ؤν񤭹��ߤ˼��Ԥ��ޤ�����";
    }
    elsif ( $errno == 1001 )
    {
	$severity = $kinologue'SEV_WARN;
	$msg ="���ߴ����Ԥˤ����ƥʥ���Ǥ������Ф餯���Ԥ�����������";
    }
    else
    {
	$severity = $kinologue'SEV_ANY;
	$msg = "���顼�ֹ������$errInfo��";
    }

    # �۾ｪλ�β�ǽ��������Τǡ��Ȥꤢ����lock�򳰤�
    # (��å��μ��Ԥλ��ʳ�)
    if ( !$PC && ( $errno != 999 ) && ( $errno != 1001 ))
    {
	&UnlockAll();
    }

    # log a log(except logging failure).
    &KbLog( $severity, "$msg" ) if ( $errno != 1000 );

    # ɽ�����̤κ���
    &MsgHeader( 'Error!', "$SYSTEM_NAME: ERROR!" );
    &cgiprint'Cache( "<p>$msg</p>\n" );

    if ( !$PC && ( $errno != 999 ) && ( $errno != 1001 ))
    {
	&PrintButtonToTitleList( $BOARD, undef )
	    if (( $BOARD ne '' ) && ( $errno != 11 ));
	&PrintButtonToBoardList if $SYS_F_B;
    }

    &MsgFooter();

    &KbLog( $kinologue'SEV_INFO, 'Exec finished.' ) if ( $errno != 1000 );
    exit( 0 );
}

1;
