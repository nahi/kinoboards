###
## SortTitle - ���ս祿���ȥ����
#
# - SYNOPSIS
#	SortTitle;
#
# - ARGS
#	�ʤ�
#
# - DESCRIPTION
#	�����ȥ���������ս�˥����Ȥ���ɽ�����롥
#	����ѿ��Ǥ��롤CGI�ѿ��򻲾Ȥ��롥
#
# - RETURN
#	�ʤ�
#
SortTitle:
{
    &LockBoard();
    # cache article DB
    &DbCache( $BOARD ) if $BOARD;
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
    local( $From ) = $To - $Num + 1;
    $From = 0 if (( $From < 0 ) || ( $Num == 0 ));

    local( $pageLinkStr ) = &PageLink( 'r', $Num, $Old, $Rev );

    # ɽ�����̤κ���
    &MsgHeader( 'Sorted view', "$H_SUBJECT����(���ս�)" );

    &BoardHeader();
    &cgiprint'Cache("$H_HR\n");
    &cgiprint'Cache( $pageLinkStr );

    &cgiprint'Cache("<ul>\n");

    # ������ɽ��
    local( $IdNum, $Id );
    if ( $#DB_ID == -1 )
    {
	# �����ä��ġ�
	&cgiprint'Cache("<li>$H_NOARTICLE\n");
    }
    else
    {
	if ( $vRev )
	{
	    for ($IdNum = $From; $IdNum <= $To; $IdNum++)
	    {
		$Id = $DB_ID[$IdNum];
		&cgiprint'Cache("<li>" . &GetFormattedTitle( $Id, $DB_AIDS{$Id}, $DB_ICON{$Id}, $DB_TITLE{$Id}, $DB_NAME{$Id}, $DB_DATE{$Id}, 1 ) . "\n");
	    }
	}
	else
	{
	    for ($IdNum = $To; $IdNum >= $From; $IdNum--)
	    {
		$Id = $DB_ID[$IdNum];
		&cgiprint'Cache("<li>" . &GetFormattedTitle( $Id, $DB_AIDS{$Id}, $DB_ICON{$Id}, $DB_TITLE{$Id}, $DB_NAME{$Id}, $DB_DATE{$Id}, 1 ) . "\n");
	    }
	}
    }

    &cgiprint'Cache("</ul>\n");

    &cgiprint'Cache( $pageLinkStr );

    &MsgFooter;

}

1;
