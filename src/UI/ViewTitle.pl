###
## ViewTitle - ����å���ɽ��
#
# - SYNOPSIS
#	ViewTitle($ComType);
#
# - ARGS
#	$ComType	ɽ�����̤Υ�����
#				0 ... �������Ȳ���
#				1 ... ������������
#				2 ... ��󥯤���������������
#				3 ... ��󥯤��������»�
#				4 ... ��ư��������
#				5 ... ��ư�»�
#
# - DESCRIPTION
#	�����������Υ����ȥ�򥹥�å��̤˥����Ȥ���ɽ����
#	����ѿ��Ǥ��롤CGI�ѿ��򻲾Ȥ��롥
#	����ѿ�ADDFLAG(����ɽ�����Ƥ��ޤä����ݤ���ɽ�魯�ե饰)���˲����롥
#
# - RETURN
#	�ʤ�
#
ViewTitle: {
    local($ComType) = $gVarComType;
    local($Num, $Old, $NextOld, $BackOld, $To, $From, $IdNum, $Id, $Fid, $IdNum, $Id, $NextCommand, $FirstFlag, $Key, $Value, $AddNum);
    %ADDFLAG = ();		# it's static.

    if ($ComType == 3) {
	# ��󥯤��������μ»�
	&ReLinkExec($cgi'TAGS{'rfid'}, $cgi'TAGS{'rtid'}, $BOARD);
    } elsif ($ComType == 5) {
	# ��ư�μ»�
	&ReOrderExec($cgi'TAGS{'rfid'}, $cgi'TAGS{'rtid'}, $BOARD);
    }

    # ɽ������Ŀ������
    $Num = $cgi'TAGS{'num'};
    $Old = $cgi'TAGS{'old'};
    $NextOld = ($Old > $Num) ? ($Old - $Num) : 0;
    $BackOld = ($Old + $Num);
    $To = $#DB_ID - $Old;
    $From = $To - $Num + 1; $From = 0 if (($From < 0) || ($Num == 0));

    # �����Ѥߥե饰
    # 0 ... �����оݳ�
    # 1 ... �����Ѥ�
    # 2 ... ̤����
    for($IdNum = $From; $IdNum <= $To; $IdNum++) { $ADDFLAG{$DB_ID[$IdNum]} = 2; }

    # ��/������ޥ��
    $FirstFlag = 1;
    $NextCommand = '?';
    while (($Key, $Value) = each %cgi'TAGS) {
	# ����Ϣ�ϥ��å�
	next if (($Key eq 'num') || ($Key eq 'old'));
	if ($FirstFlag) { $FirstFlag = 0; } else { $NextCommand .= "&"; }
	$NextCommand .= "$Key=$Value";
    }

    # �ڡ�������ʸ����
    $AddNum = "&num=" . $cgi'TAGS{'num'} . "&old=" . $cgi'TAGS{'old'};

    # ɽ�����̤κ���
    if ($ComType == 2) {
	&MsgHeader('Title view (threaded)', "$BOARDNAME: �����ʥ�ץ饤��λ���");
    } elsif ($ComType == 3) {
	&MsgHeader('Title view (threaded)', "$BOARDNAME: ���ꤵ�줿$H_MESG�Υ�ץ饤����ѹ����ޤ���");
    } elsif ($ComType == 4) {
	&MsgHeader('Title view (threaded)', "$BOARDNAME: ��ư��λ���");
    } elsif ($ComType == 5) {
	&MsgHeader('Title view (threaded)', "$BOARDNAME: ���ꤵ�줿$H_MESG���ư���ޤ���");
    } else {
	&MsgHeader('Title view (threaded)', "$BOARDNAME: $H_SUBJECT����($H_REPLY��)");
    }

    if ($ComType == 0) {

	&BoardHeader('normal');

    } else {

	&BoardHeader('maint');

	if ($ComType == 3) {
	    &cgiprint'Cache("<p>\n<ul>\n<li><a href=\"$PROGRAM?b=$BOARD&c=ce&rtid=" . $cgi'TAGS{'roid'} . "&rfid=" . $cgi'TAGS{'rfid'} . "\">�����ѹ��򸵤��᤹</a>\n</ul>\n</p>");
	}

	&cgiprint'Cache(<<__EOF__);
<p>�ƥ�������ϡ����Τ褦�ʰ�̣��ɽ���Ƥ��ޤ���
<dl compact>
<dt>$H_RELINKFROM_MARK
<dd>����$H_MESG��$H_REPLY����ѹ����ޤ���$H_REPLY�����ꤹ����̤����Ӥޤ���
<dt>$H_REORDERFROM_MARK
<dd>����$H_MESG�ν�����ѹ����ޤ�����ư�����ꤹ����̤����Ӥޤ���
<dt>$H_DELETE_ICON
<dd>����$H_MESG�������ޤ���
<dt>$H_SUPERSEDE_ICON
<dd>����$H_MESG���������ޤ���
<dt>$H_RELINKTO_MARK
<dd>��˻��ꤷ��$H_MESG��$H_REPLY��򡤤���$H_MESG�ˤ��ޤ���
<dt>$H_REORDERTO_MARK
<dd>��˻��ꤷ��$H_MESG�򡤤���$H_MESG�β��˰�ư���ޤ���
</dl></p>
__EOF__

	if ($ComType == 2) {
	    &cgiprint'Cache("<p>" . $cgi'TAGS{'rfid'} . "�򡤤ɤ�$H_MESG�ؤΥ�ץ饤�ˤ��ޤ���? ��ץ饤���$H_MESG��$H_RELINKTO_MARK�򥯥�å����Ƥ���������</p>\n");
	} elsif ($ComType == 4) {
	    &cgiprint'Cache("<p>" . $cgi'TAGS{'rfid'} . "�򡤤ɤ�$H_MESG�β��˰�ư���ޤ���? $H_MESG��$H_REORDERTO_MARK�򥯥�å����Ƥ���������</p>\n");
	}

    }

    &cgiprint'Cache("<hr>\n");

    if ($SYS_BOTTOMTITLE) {
	&cgiprint'Cache("<p>$H_TOP<a href=\"$PROGRAM?b=$BOARD&c=v&num=$Num&old=$BackOld\">$H_BACKART</a></p>\n") if ($From > 0);
    } else {
	&cgiprint'Cache("<p>$H_TOP<a href=\"$PROGRAM?b=$BOARD&c=v&num=$Num&old=$NextOld\">$H_NEXTART</a></p>\n") if ($Old);
    }

    &cgiprint'Cache("<p><ul>\n");

    if ($To < $From) {

	# �����ä��ġ�
	&cgiprint'Cache("<li>$H_NOARTICLE\n");

    } elsif ($SYS_BOTTOMTITLE) {

	# �Ť��Τ������
	if (($ComType == 2) && ($DB_FID{$cgi'TAGS{'rfid'}} ne '')) {
	    &cgiprint'Cache("<li><a href=\"$PROGRAM?b=$BOARD&c=ce&rtid=&rfid=" . $cgi'TAGS{'rfid'} . "&roid=" . $cgi'TAGS{'roid'} . "$AddNum\">[�ɤ�$H_MESG�ؤΥ�ץ饤�Ǥ�ʤ�������$H_MESG�ˤ���]</a>\n");
	} elsif ($ComType == 4) {
	    &cgiprint'Cache("<li><a href=\"$PROGRAM?b=$BOARD&c=mve&rtid=&rfid=" . $cgi'TAGS{'rfid'} . "&roid=" . $cgi'TAGS{'roid'} . "$AddNum\">[����������Ƭ�˰�ư����(���Υڡ�������Ƭ���ǤϤ���ޤ���)]</a>\n");
	}

	for($IdNum = $From; $IdNum <= $To; $IdNum++) {

	    # ����������ID����Ф�
	    $Id = $DB_ID[$IdNum];
	    ($Fid = $DB_FID{$Id}) =~ s/,.*$//o;
	    # �������Ȥϸ�󤷡�
	    next if (($Fid ne '') && ($ADDFLAG{$Fid} == 2));
	    # �Ρ��ɤ�ɽ��
	    if ($ComType == 0) {
		&ViewTitleNode($Id);
	    } else {
		&ViewTitleNodeMaint($Id, $ComType, $AddNum);
	    }
	}
    } else {

	# �������Τ������
	if (($ComType == 2) && ($DB_FID{$cgi'TAGS{'rfid'}} ne '')) {
	    &cgiprint'Cache("<li><a href=\"$PROGRAM?b=$BOARD&c=ce&rtid=&rfid=" . $cgi'TAGS{'rfid'} . "&roid=" . $cgi'TAGS{'roid'} . "$AddNum\">[�ɤ�$H_MESG�ؤΥ�ץ饤�Ǥ�ʤ�������$H_MESG�ˤ���]</a>\n");
	} elsif ($ComType == 4) {
	    &cgiprint'Cache("<li><a href=\"$PROGRAM?b=$BOARD&c=mve&rtid=&rfid=" . $cgi'TAGS{'rfid'} . "&roid=" . $cgi'TAGS{'roid'} . "$AddNum\">[����������Ƭ�˰�ư����(���Υڡ�������Ƭ���ǤϤ���ޤ���)]</a>\n");
	}

	for($IdNum = $To; $IdNum >= $From; $IdNum--) {
	    # ���Ʊ��
	    $Id = $DB_ID[$IdNum];
	    ($Fid = $DB_FID{$Id}) =~ s/,.*$//o;
	    next if (($Fid ne '') && ($ADDFLAG{$Fid} == 2));
	    if ($ComType == 0) {
		&ViewTitleNode($Id);
	    } else {
		&ViewTitleNodeMaint($Id, $ComType, $AddNum);
	    }
	}
    }

    &cgiprint'Cache("</ul></p>\n");

    if ($SYS_BOTTOMTITLE) {
	&cgiprint'Cache("<p>$H_BOTTOM<a href=\"$PROGRAM?b=$BOARD&c=v&num=$Num&old=$NextOld\">$H_NEXTART</a></p>\n") if ($Old);
    } else {
	&cgiprint'Cache("<p>$H_BOTTOM<a href=\"$PROGRAM?b=$BOARD&c=v&num=$Num&old=$BackOld\">$H_BACKART</a></p>\n") if ($From > 0);
    }

    &MsgFooter;

    undef(%ADDFLAG);

}

sub ViewTitleNode {
    local($Id) = @_;

    if ($ADDFLAG{$Id} != 2) { return; }

    &cgiprint'Cache("<li>" . &GetFormattedTitle($Id, $BOARD, $DB_AIDS{$Id}, $DB_ICON{$Id}, $DB_TITLE{$Id}, $DB_NAME{$Id}, $DB_DATE{$Id}) . "\n");
    $ADDFLAG{$Id} = 1;		# �����Ѥ�

    # ̼�����Сġ�
    if ($DB_AIDS{$Id}) {
	&cgiprint'Cache("<ul>\n");
	foreach (split(/,/, $DB_AIDS{$Id})) { &ViewTitleNode($_); }
	&cgiprint'Cache("</ul>\n");
    }
}

sub ViewTitleNodeMaint {

    local($Id, $ComType, $AddNum) = @_;

    return if ($ADDFLAG{$Id} != 2);

    local($FromId) = $cgi'TAGS{'rfid'};

    &cgiprint'Cache("<li>" . &GetFormattedTitle($Id, $BOARD, $DB_AIDS{$Id}, $DB_ICON{$Id}, $DB_TITLE{$Id}, $DB_NAME{$Id}, $DB_DATE{$Id})); #'

    &cgiprint'Cache(" .......... \n");

    # ������ѹ����ޥ��(From)
    # ��ư���ޥ��(From)
    if ($SYS_F_MV) {
	&cgiprint'Cache("<a href=\"$PROGRAM?b=$BOARD&c=ct&rfid=$Id&roid=" . $DB_FID{$Id} . "$AddNum\">$H_RELINKFROM_MARK</a>\n");
	if ($DB_FID{$Id} eq '') {
	    &cgiprint'Cache("<a href=\"$PROGRAM?b=$BOARD&c=mvt&rfid=$Id&roid=" . $DB_FID{$Id} . "$AddNum\">$H_REORDERFROM_MARK</a>\n");
	}
    }

    # ������ޥ��
    if ($SYS_F_D) {
	&cgiprint'Cache(<<__EOF__);
<a href="$PROGRAM?b=$BOARD&c=dp&id=$Id">$H_DELETE_ICON</a>
<a href="$PROGRAM?b=$BOARD&c=f&s=on&id=$Id">$H_SUPERSEDE_ICON</a>
__EOF__
    }

    # ��ư���ޥ��(To)
    if ($SYS_F_MV && ($ComType == 4) && ($FromId ne $Id) && ($DB_FID{$Id} eq '') && ($FromId ne $Id)) {
	&cgiprint'Cache("<a href=\"$PROGRAM?b=$BOARD&c=mve&rtid=$Id&rfid=$FromId&roid=" . $cgi'TAGS{'roid'} . "$AddNum\">$H_REORDERTO_MARK</a>\n");
    }

    # ������ѹ����ޥ��(To)
    if ($SYS_F_MV && ($ComType == 2) && ($FromId ne $Id) && (! grep(/^$FromId$/, split(/,/, $DB_AIDS{$Id}))) && (! grep(/^$FromId$/, split(/,/, $DB_FID{$Id})))) {
	&cgiprint'Cache("<a href=\"$PROGRAM?b=$BOARD&c=ce&rtid=$Id&rfid=$FromId&roid=" . $cgi'TAGS{'roid'} . "$AddNum\">$H_RELINKTO_MARK</a>\n");
    }

    $ADDFLAG{$Id} = 1;		# �����Ѥ�

    # ̼�����Сġ�
    if ($DB_AIDS{$Id}) {
	&cgiprint'Cache("<ul>\n");
	foreach (split(/,/, $DB_AIDS{$Id})) { &ViewTitleNodeMaint($_, $ComType, $AddNum); }
	&cgiprint'Cache("</ul>\n");
    }
}

1;