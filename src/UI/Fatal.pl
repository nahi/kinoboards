###
## Fatal - ���顼ɽ��
#
# - SYNOPSIS
#	Fatal($FatalNo, $FatalInfo);
#
# - ARGS
#	$FatalNo	���顼�ֹ�(�ܤ����ϴؿ������򻲾ȤΤ���)
#	$FatalInfo	���顼����
#
# - DESCRIPTION
#	���顼��ɽ�����̤�֥饦�����������롥
#
# - RETURN
#	�ʤ�
#
Fatal: {
    local($FatalNo, $FatalInfo) = ($gVarFatalNo, $gVarFatalInfo);
    local($ErrString);

    if ($FatalNo == 1) {

	$ErrString = "File: $FatalInfo��¸�ߤ��ʤ������뤤��permission�����꤬�ְ�äƤ��ޤ���������Ǥ�����<a href=\"mailto:$MAINT\">$MAINT</a>�ޤǡ��嵭�ե�����̾���Τ餻��������";

    } elsif ($FatalNo == 2) {

	$ErrString = "���Ϥ���Ƥ��ʤ����ܤ�����ޤ�����äƤ⤦���٤��ľ���ƤߤƤ���������";

    } elsif ($FatalNo == 3) {

	$ErrString = "���̾�����ᥤ�륢�ɥ쥹�ˡ�����ʸ�������Ԥ����äƤ��ޤäƤ��ޤ�����äƤ⤦���٤��ľ���ƤߤƤ���������";

    } elsif ($FatalNo == 4) {

	$ErrString = "�����HTML����������ʸ��������ʸ��������뤳�Ȥ϶ؤ����Ƥ��ޤ�����äư㤦��˽񤭴����Ƥ���������";

    } elsif ($FatalNo == 5) {

	$ErrString = "��Ͽ����Ƥ��륨���ꥢ���Τ�Τȡ��ޥ���̾�����פ��ޤ��󡥤�����Ǥ�����<a href=\"mailto:$MAINT\">$MAINT</a>�ޤǸ�Ϣ����������";

    } elsif ($FatalNo == 6) {

	$ErrString = "��$FatalInfo�פȤ��������ꥢ���ϡ���Ͽ����Ƥ��ޤ���";

    } elsif ($FatalNo == 7) {

	$ErrString = "$FatalInfo��������������ޤ���? ��äƤ⤦���٤��ľ���ƤߤƤ���������";

    } elsif ($FatalNo == 8) {

	$ErrString = "���ε����Ϥޤ���Ƥ���Ƥ��ޤ���";

    } elsif ($FatalNo == 9) {

	$ErrString = "�ᥤ�뤬�����Ǥ��ޤ���Ǥ�����������Ǥ��������Υ��顼��å������ȡ����顼��������������<a href=\"mailto:$MAINT\">$MAINT</a>�ޤǤ��Τ餻����������";

    } elsif ($FatalNo == 10) {

	$ErrString = ".db��.articleid�������������Ƥ��ޤ��󡥤�����Ǥ��������Υ��顼��å������ȡ����顼��������������<a href=\"mailto:$MAINT\">$MAINT</a>�ޤǤ��Τ餻����������";

    } elsif ($FatalNo == 11) {

	$ErrString = "$FatalInfo�Ȥ���ID���б�����$H_BOARD�ϡ�¸�ߤ��ޤ���";

    } elsif ($FatalNo == 50) {

	$ErrString = "��ץ饤�ط����۴Ĥ��Ƥ��ޤ��ޤ����ɤ����Ƥ��ץ饤����ѹ���������硤��ץ饤�����ٿ��尷���ˤ��Ƥ��顤��ץ饤�򤫤������Ƥ���������";

    } elsif ($FatalNo == 99) {

	$ErrString ="����$H_BOARD�Ǥϡ����Υ��ޥ�ɤϼ¹ԤǤ��ޤ���";

    } elsif ($FatalNo == 999) {

	$ErrString ="�����ƥ�Υ�å��˼��Ԥ��ޤ��������߹�äƤ���褦�Ǥ��Τǡ���ʬ�ԤäƤ���⤦���٥����������Ƥ������������٥����������Ƥ��å�����Ƥ����硤���ƥʥ���Ǥ����ǽ���⤢��ޤ���";

    } else {

	$ErrString = "���顼�ֹ�����: $FatalInfo<br>������Ǥ��������Υ��顼��å������ȡ����顼��������������<a href=\"mailto:$mEmail\">$mEmail</a>�ޤǤ��Τ餻����������";

    }

    # �۾ｪλ�β�ǽ��������Τǡ��Ȥꤢ����lock�򳰤�
    # (��å��μ��Ԥλ��ʳ�)
    if ($FatalNo != 999) { &cgi'unlock($LOCK_FILE); }

    # ɽ�����̤κ���
    &MsgHeader('Error!', "$SYSTEM_NAME: ERROR!");

    &cgiprint'Cache("<p>$ErrString</p>\n");

    if ($BOARD ne '') {	&PrintButtonToTitleList($BOARD); }
    &PrintButtonToBoardList;

    &MsgFooter;
    exit(0);
}

1;
