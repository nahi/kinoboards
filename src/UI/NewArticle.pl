###
## NewArticle - ������������ޤȤ��ɽ��
#
# - SYNOPSIS
#	NewArticle;
#
# - ARGS
#	�ʤ�
#
# - DESCRIPTION
#	������������ޤȤ��ɽ����
#	����ѿ��Ǥ��롤CGI�ѿ��򻲾Ȥ��롥
#
# - RETURN
#	�ʤ�
#
NewArticle:
{
    &LockBoard;
    # cache article DB
    &DbCache( $BOARD ) if $BOARD;
    &UnlockBoard;

    # ɽ������Ŀ������
    local( $Num ) = $cgi'TAGS{'num'};
    local( $Old ) = $cgi'TAGS{'old'};
    local( $Rev ) = $cgi'TAGS{'rev'};
    local( $vRev ) = $Rev? 1-$SYS_BOTTOMARTICLE : $SYS_BOTTOMARTICLE;
    local( $To ) = $#DB_ID - $Old;
    local( $From ) = $To - $Num + 1; $From = 0 if (($From < 0) || ($Num == 0));

    local( $pageLinkStr ) = &PageLink( 'l', $Num, $Old, $Rev );

    # ɽ�����̤κ���
    &MsgHeader( 'Message view (sorted)', "�Ƕ��$H_MESG��ޤȤ��ɤ�" );

    &cgiprint'Cache( $pageLinkStr );

    &cgiprint'Cache("$H_HR\n");

    if (! $#DB_ID == -1)
    {
	# �����ä��ġ�
	&cgiprint'Cache("<p>$H_NOARTICLE</p>\n");
    }
    else
    {
	local( $IdNum, $Id );
	if ( $vRev )
	{
	    for ($IdNum = $From; $IdNum <= $To; $IdNum++)
	    {
		$Id = $DB_ID[$IdNum];
		&ViewOriginalArticle($Id, $SYS_COMMAND_EACH, 1);
		&cgiprint'Cache("$H_HR\n");
	    }
	}
	else
	{
	    for ($IdNum = $To; $IdNum >= $From; $IdNum--)
	    {
		$Id = $DB_ID[$IdNum];
		&ViewOriginalArticle($Id, $SYS_COMMAND_EACH, 1);
		&cgiprint'Cache("$H_HR\n");
	    }
	}
    }

    &cgiprint'Cache( $pageLinkStr );

    &cgiprint'Cache("$H_HR\n");

    &PrintButtonToTitleList( $BOARD, $From );
    &PrintButtonToBoardList if $SYS_F_B;

    &MsgFooter;

}

1;
