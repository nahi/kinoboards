###
## ThreadTitle - ����å��̥����ȥ����
#
# - SYNOPSIS
#	ThreadTitle($ComType);
#
# - ARGS
#	$ComType	ɽ�����̤Υ�����
#				0 ... �������Ȳ���
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
ThreadTitle:
{
    local( $ComType ) = $gVarComType;
    local( $IdNum, $Id, $Fid, $IdNum, $Id );
    local( $vCom, $vStr );

    if ( $ComType == 0 )
    {
	$vCom = 'v';
	$vStr = '';
    }
    elsif ( $ComType == 2 )
    {
	$vCom = 'ct';
	$vStr = "&rtid=" . $cgi'TAGS{'roid'} . "&rfid=" . $cgi'TAGS{'rfid'} . "&rtid=" . $cgi'TAGS{'rtid'};
    }
    elsif ( $ComType == 3 )
    {
	$vCom = 'v';
	$vStr = '';
    }
    elsif ( $ComType == 4 )
    {
	$vCom = 'mvt';
	$vStr = "&rtid=" . $cgi'TAGS{'roid'} . "&rfid=" . $cgi'TAGS{'rfid'} . "&rtid=" . $cgi'TAGS{'rtid'};
    }
    elsif ( $ComType == 5 )
    {
	$vCom = 'v';
	$vStr = '';
    }

    %ADDFLAG = ();		# it's static.

    &LockBoard();
    &DbCache( $BOARD ) if $BOARD;

    if ($ComType == 3)
    {
	# ��󥯤��������μ»�
	&ReLinkExec($cgi'TAGS{'rfid'}, $cgi'TAGS{'rtid'}, $BOARD);
    }
    elsif ($ComType == 5)
    {
	# ��ư�μ»�
	&ReOrderExec($cgi'TAGS{'rfid'}, $cgi'TAGS{'rtid'}, $BOARD);
    }

    &UnlockBoard();

    # ɽ������Ŀ������
    local( $Num ) = $cgi'TAGS{'num'};
    local( $Old );
    if ( defined( $cgi'TAGS{'id'} ))
    {
	$Old = $#DB_ID - int( $cgi'TAGS{'id'} + $Num/2 );
	$Old = 0 if ( $Old < 0 );
    }
    else
    {
	$Old = $cgi'TAGS{'old'};
    }
    local( $Rev ) = $cgi'TAGS{'rev'};
    local( $vRev ) = $Rev? 1-$SYS_BOTTOMTITLE : $SYS_BOTTOMTITLE;
    local( $To ) = $#DB_ID - $Old;
    local( $From )= $To - $Num + 1;
    $From = 0 if (( $From < 0 ) || ( $Num == 0 ));

    local( $pageLinkStr ) = &PageLink( "$vCom$vStr", $Num, $Old, $Rev );

    # �����Ѥߥե饰
    # 0 ... �����оݳ�
    # 1 ... �����Ѥ�
    # 2 ... ̤����
    local( $IdNum, $Id );
    for ( $IdNum = $From; $IdNum <= $To; $IdNum++ )
    {
	$ADDFLAG{$DB_ID[$IdNum]} = 2;
    }

    # ɽ�����̤κ���
    if ($ComType == 2)
    {
	&MsgHeader( 'Thread view', '�����ʥ�ץ饤��λ���' );
    }
    elsif ($ComType == 3)
    {
	&MsgHeader( 'Thread view', "���ꤵ�줿$H_MESG�Υ�ץ饤����ѹ����ޤ���" );
    }
    elsif ($ComType == 4)
    {
	&MsgHeader( 'Thread view', '��ư��λ���' );
    }
    elsif ($ComType == 5)
    {
	&MsgHeader( 'Thread view', "���ꤵ�줿$H_MESG���ư���ޤ���");
    }
    else
    {
	&MsgHeader( 'Thread view', "$H_SUBJECT����($H_REPLY��)" );
    }

    &BoardHeader();

    if ( $SYS_F_MT )
    {
	if ($ComType == 3)
	{
	    &cgiprint'Cache("<ul>\n<li>", &TagA( "$PROGRAM?b=$BOARD&c=ce&rtid=" . $cgi'TAGS{'roid'} . "&rfid=" . $cgi'TAGS{'rfid'}, "�����ѹ��򸵤��᤹" ), "\n</ul>\n");
	}

	&cgiprint'Cache(<<__EOF__);
<p>
��$H_ICON�ϡ����Τ褦�ʰ�̣��ɽ���Ƥ��ޤ���
</p>

<ul>
<li>$H_RELINKFROM_MARK:
����$H_MESG��$H_REPLY����ѹ����ޤ���$H_REPLY�����ꤹ����̤����Ӥޤ���
<li>$H_REORDERFROM_MARK:
����$H_MESG�ν�����ѹ����ޤ�����ư�����ꤹ����̤����Ӥޤ���
<li>$H_DELETE_ICON:
����$H_MESG�������ޤ���
<li>$H_SUPERSEDE_ICON:
����$H_MESG���������ޤ���
<li>$H_RELINKTO_MARK:
��˻��ꤷ��$H_MESG��$H_REPLY��򡤤���$H_MESG�ˤ��ޤ���
<li>$H_REORDERTO_MARK:
��˻��ꤷ��$H_MESG�򡤤���$H_MESG�β��˰�ư���ޤ���
</ul>
__EOF__

	if ($ComType == 2)
	{
	    &cgiprint'Cache("<p>", $cgi'TAGS{'rfid'}, "�򡤤ɤ�$H_MESG�ؤΥ�ץ饤�ˤ��ޤ���? ��ץ饤���$H_MESG��$H_RELINKTO_MARK�򥯥�å����Ƥ���������</p>\n");
	}
	elsif ($ComType == 4)
	{
	    &cgiprint'Cache("<p>", $cgi'TAGS{'rfid'}, "�򡤤ɤ�$H_MESG�β��˰�ư���ޤ���? $H_MESG��$H_REORDERTO_MARK�򥯥�å����Ƥ���������</p>\n");
	}
    }

    &cgiprint'Cache("$H_HR\n");

    &cgiprint'Cache( $pageLinkStr );

    local( $AddNum ) = "&num=$Num&old=$Old&rev=$Rev";

    if ($To < $From)
    {
	# �����ä��ġ�
	&cgiprint'Cache("<ul>\n<li>$H_NOARTICLE\n</ul>\n");
    }
    elsif ( $vRev )
    {
	# �Ť��Τ������
	if (($ComType == 2) && ($DB_FID{$cgi'TAGS{'rfid'}} ne ''))
	{
	    &cgiprint'Cache( "<ul>\n<li>", &TagA( "$PROGRAM?b=$BOARD&c=ce&rtid=&rfid=" . $cgi'TAGS{'rfid'} . "&roid=" . $cgi'TAGS{'roid'} . $AddNum, "[�ɤ�$H_MESG�ؤΥ�ץ饤�Ǥ�ʤ�������$H_MESG�ˤ���]" ), "\n</ul>\n" );
	}
	elsif ($ComType == 4)
	{
	    &cgiprint'Cache( "<ul>\n<li>", &TagA( "$PROGRAM?b=$BOARD&c=mve&rtid=&rfid=" . $cgi'TAGS{'rfid'} . "&roid=" . $cgi'TAGS{'roid'} . $AddNum, "[����������Ƭ�˰�ư����(���Υڡ�������Ƭ���ǤϤ���ޤ���)]" ), "\n</ul>\n" );
	}

	for( $IdNum = $From; $IdNum <= $To; $IdNum++ )
	{
	    # ����������ID����Ф�
	    $Id = $DB_ID[$IdNum];
	    ( $Fid = $DB_FID{ $Id } ) =~ s/,.*$//o;
	    # �������Ȥϸ�󤷡�
#	    next if ((( $Fid ne '' ) && ( $SYS_THREAD_FORMAT == 2 )) || ( $ADDFLAG{$Fid} == 2 ));
	    next if (( $Fid ne '' ) && (( $ADDFLAG{$Fid} == 2 ) || ( $SYS_THREAD_FORMAT == 2 )));

	    # �Ρ��ɤ�ɽ��
	    &cgiprint'Cache( "<ul>\n" );
	    if ( $SYS_F_MT )
	    {
		&ThreadTitleNodeMaint( $Id, $ComType, $AddNum, 1 );
	    }
	    else
	    {
		if ( $SYS_THREAD_FORMAT == 1 )
		{
		    &ThreadTitleNodeAllThread( $Id, 1 );
		}
		elsif ( $SYS_THREAD_FORMAT == 2 )
		{
		    &ThreadTitleNodeNoThread( $Id, 1 );
		}
		else
		{
		    &ThreadTitleNodeThread( $Id, 1 );
		}
	    }
	    &cgiprint'Cache( "</ul>\n" );
	}
    }
    else
    {
	# �������Τ������
	if (($ComType == 2) && ($DB_FID{$cgi'TAGS{'rfid'}} ne ''))
	{
	    &cgiprint'Cache("<li>", &TagA( "$PROGRAM?b=$BOARD&c=ce&rtid=&rfid=" . $cgi'TAGS{'rfid'} . "&roid=" . $cgi'TAGS{'roid'} . $AddNum, "[�ɤ�$H_MESG�ؤΥ�ץ饤�Ǥ�ʤ�������$H_MESG�ˤ���]" ), "\n");
	}
	elsif ($ComType == 4)
	{
	    &cgiprint'Cache("<li>", &TagA( "$PROGRAM?b=$BOARD&c=mve&rtid=&rfid=" . $cgi'TAGS{'rfid'} . "&roid=" . $cgi'TAGS{'roid'} . $AddNum, "[����������Ƭ�˰�ư����(���Υڡ�������Ƭ���ǤϤ���ޤ���)]" ), "\n");
	}

	for( $IdNum = $To; $IdNum >= $From; $IdNum-- )
	{
	    # ���Ʊ��
	    $Id = $DB_ID[$IdNum];
	    ( $Fid = $DB_FID{ $Id } ) =~ s/,.*$//o;
#	    next if ((( $Fid ne '' ) && ( $SYS_THREAD_FORMAT == 2 )) || ( $ADDFLAG{$Fid} == 2 ));
	    next if (( $Fid ne '' ) && (( $ADDFLAG{$Fid} == 2 ) || ( $SYS_THREAD_FORMAT == 2 )));

	    &cgiprint'Cache( "<ul>\n" );
	    if ( $SYS_F_MT )
	    {
		&ThreadTitleNodeMaint( $Id, $ComType, $AddNum, 1 );
	    }
	    else
	    {
		if ( $SYS_THREAD_FORMAT == 1 )
		{
		    &ThreadTitleNodeAllThread( $Id, 1 );
		}
		elsif ( $SYS_THREAD_FORMAT == 2 )
		{
		    &ThreadTitleNodeNoThread( $Id, 1 );
		}
		else
		{
		    &ThreadTitleNodeThread( $Id, 1 );
		}
	    }
	    &cgiprint'Cache( "</ul>\n" );
	}
    }

    &cgiprint'Cache( $pageLinkStr );

    &MsgFooter;

    undef(%ADDFLAG);

}


###
## ����Ρ��ɤΤ�ɽ��
#
sub ThreadTitleNodeNoThread
{
    local( $Id ) = @_;

    &cgiprint'Cache( '<li>', &GetFormattedTitle( $Id, $DB_AIDS{$Id}, $DB_ICON{$Id}, $DB_TITLE{$Id}, $DB_NAME{$Id}, $DB_DATE{$Id}, 1 ), "\n");
}


###
## �ڡ����⥹��åɤΤ�ɽ��
#
sub ThreadTitleNodeThread
{
    local( $Id, $top ) = @_;

    # �ڡ������ʤ餪���ޤ���
    return if ( $ADDFLAG{$Id} != 2 );

    &cgiprint'Cache( '<li>', &GetFormattedTitle($Id, $DB_AIDS{$Id}, $DB_ICON{$Id}, $DB_TITLE{$Id}, $DB_NAME{$Id}, $DB_DATE{$Id}, $top ), "\n" );

    $ADDFLAG{$Id} = 1;		# �����Ѥ�

    # ̼�����Сġ�
    if ( $DB_AIDS{$Id} )
    {
	&cgiprint'Cache( "<ul>\n" );
	grep( &ThreadTitleNodeThread( $_, 0 ), split( /,/, $DB_AIDS{$Id} ));
	&cgiprint'Cache( "</ul>\n" );
    }
}


###
## ������åɤ�ɽ��
#
sub ThreadTitleNodeAllThread
{
    local( $Id, $top ) = @_;

    # ɽ���Ѥߤʤ餪���ޤ���
    return if ( $ADDFLAG{$Id} == 1 );

    &cgiprint'Cache( '<li>', &GetFormattedTitle($Id, $DB_AIDS{$Id}, $DB_ICON{$Id}, $DB_TITLE{$Id}, $DB_NAME{$Id}, $DB_DATE{$Id}, $top ), "\n" );
    $ADDFLAG{$Id} = 1;		# �����Ѥ�

    # ̼�����Сġ�
    if ( $DB_AIDS{$Id} )
    {
	&cgiprint'Cache( "<ul>\n" );
	grep( &ThreadTitleNodeAllThread( $_, 0 ), split( /,/, $DB_AIDS{$Id} ));
	&cgiprint'Cache( "</ul>\n" );
    }
}


###
## �������ѤΥ���å�ɽ��
#
sub ThreadTitleNodeMaint
{
    local( $Id, $ComType, $AddNum, $top ) = @_;

    return if ( $ADDFLAG{$Id} != 2 );

    local($FromId) = $cgi'TAGS{'rfid'};

    &cgiprint'Cache( '<li>', &GetFormattedTitle($Id, $DB_AIDS{$Id}, $DB_ICON{$Id}, $DB_TITLE{$Id}, $DB_NAME{$Id}, $DB_DATE{$Id}, $top ));

    &cgiprint'Cache(" .......... \n");

    # ������ѹ����ޥ��(From)
    # ��ư���ޥ��(From)
    if ($SYS_F_MV)
    {
	&cgiprint'Cache( &TagA( "$PROGRAM?b=$BOARD&c=ct&rfid=$Id&roid=" . $DB_FID{$Id} . $AddNum, $H_RELINKFROM_MARK ), "\n");
	if ($DB_FID{$Id} eq '')
	{
	    &cgiprint'Cache( &TagA( "$PROGRAM?b=$BOARD&c=mvt&rfid=$Id&roid=" . $DB_FID{$Id} . $AddNum, $H_REORDERFROM_MARK ), "\n");
	}
    }

    # ������ޥ��
    if ($SYS_F_D)
    {
	&cgiprint'Cache( &TagA( "$PROGRAM?b=$BOARD&c=dp&id=$Id", $H_DELETE_ICON ), "\n" );
	&cgiprint'Cache( &TagA( "$PROGRAM?b=$BOARD&c=f&s=on&id=$Id", $H_SUPERSEDE_ICON ), "\n" );
    }

    # ��ư���ޥ��(To)
    if ($SYS_F_MV && ($ComType == 4) && ($FromId ne $Id) && ($DB_FID{$Id} eq '') && ($FromId ne $Id))
    {
	&cgiprint'Cache( &TagA( "$PROGRAM?b=$BOARD&c=mve&rtid=$Id&rfid=$FromId&roid=" . $cgi'TAGS{'roid'} . $AddNum, $H_REORDERTO_MARK ), "\n" );
    }

    # ������ѹ����ޥ��(To)
    if ($SYS_F_MV && ($ComType == 2) && ($FromId ne $Id) && (! grep(/^$FromId$/, split(/,/, $DB_AIDS{$Id}))) && (! grep(/^$FromId$/, split(/,/, $DB_FID{$Id}))))
    {
	&cgiprint'Cache( &TagA( "$PROGRAM?b=$BOARD&c=ce&rtid=$Id&rfid=$FromId&roid=" . $cgi'TAGS{'roid'} . $AddNum, $H_RELINKTO_MARK ), "\n" );
    }

    $ADDFLAG{$Id} = 1;		# �����Ѥ�

    # ̼�����Сġ�
    if ($DB_AIDS{$Id})
    {
	&cgiprint'Cache("<ul>\n");
	grep( &ThreadTitleNodeMaint( $_, $ComType, $AddNum, 0 ),
	     split( /,/, $DB_AIDS{$Id} ));
	&cgiprint'Cache("</ul>\n");
    }
}

1;
