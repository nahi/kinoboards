###
## NewArticle - 新しい記事をまとめて表示
#
# - SYNOPSIS
#	NewArticle;
#
# - ARGS
#	なし
#
# - DESCRIPTION
#	新しい記事をまとめて表示．
#	大域変数である，CGI変数を参照する．
#
# - RETURN
#	なし
#
NewArticle:
{
    &LockBoard;
    # cache article DB
    &DbCache( $BOARD ) if $BOARD;
    &UnlockBoard;

    # 表示する個数を取得
    local( $Num ) = $cgi'TAGS{'num'};
    local( $Old ) = $cgi'TAGS{'old'};
    local( $Rev ) = $cgi'TAGS{'rev'};
    local( $vRev ) = $Rev? 1-$SYS_BOTTOMARTICLE : $SYS_BOTTOMARTICLE;
    local( $To ) = $#DB_ID - $Old;
    local( $From ) = $To - $Num + 1; $From = 0 if (($From < 0) || ($Num == 0));

    local( $pageLinkStr ) = &PageLink( 'l', $Num, $Old, $Rev );

    # 表示画面の作成
    &MsgHeader( 'Message view (sorted)', "最近の$H_MESGをまとめ読み" );

    &cgiprint'Cache( $pageLinkStr );

    &cgiprint'Cache("$H_HR\n");

    if (! $#DB_ID == -1)
    {
	# 空だった……
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
