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
    # lock system
    local( $lockResult ) = $PC ? 1 : &cgi'lock( $LOCK_FILE_B );
    &Fatal(1001, '') if ( $lockResult == 2 );
    &Fatal(999, '') if ( $lockResult != 1 );
    # cache article DB
    if ( $BOARD ) { &DbCache( $BOARD ); }
    # unlock system
    &cgi'unlock( $LOCK_FILE_B ) unless $PC;

    # 表示する個数を取得
    local( $Num ) = $cgi'TAGS{'num'};
    local( $Old ) = $cgi'TAGS{'old'};
    local( $Rev ) = $cgi'TAGS{'rev'};
    local( $vRev ) = $Rev? 1-$SYS_BOTTOMARTICLE : $SYS_BOTTOMARTICLE;
    local( $NextOld ) = ($Old > $Num) ? ($Old - $Num) : 0;
    local( $BackOld ) = ($Old + $Num);
    local( $To ) = $#DB_ID - $Old;
    local( $From ) = $To - $Num + 1; $From = 0 if (($From < 0) || ($Num == 0));

    # 表示画面の作成
    &MsgHeader('Message view (sorted)', "最近の$H_MESGをまとめ読み");

    &cgiprint'Cache( "<p>" );
    &cgiprint'Cache( &TagA( "$PROGRAM?b=$BOARD&c=l&num=$Num&old=$Old&rev=" . ( 1-$Rev ), $H_REVERSE ), ' ' ) if ( $SYS_REVERSE );
    if ( $vRev )
    {
	if ( $From > 0 )
	{
	    &cgiprint'Cache( $H_TOP, &TagA( "$PROGRAM?b=$BOARD&c=l&num=$Num&old=$BackOld", $H_BACKART ));
	}
	else
	{
	    &cgiprint'Cache( $H_TOP, $H_NOBACKART );
	}
    }
    else
    {
	if ( $Old )
	{
	    &cgiprint'Cache( $H_TOP, &TagA( "$PROGRAM?b=$BOARD&c=l&num=$Num&old=$NextOld", $H_NEXTART ));
	}
	else
	{
	    &cgiprint'Cache( $H_TOP, $H_NONEXTART );
	}
    }
    &cgiprint'Cache( "</p>\n" );

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

    &cgiprint'Cache( "<p>" );
    &cgiprint'Cache( &TagA( "$PROGRAM?b=$BOARD&c=l&num=$Num&old=$Old&rev=" . ( 1-$Rev ), $H_REVERSE ), ' ' ) if ( $SYS_REVERSE );
    if ( $vRev )
    {
	if ( $Old )
	{
	    &cgiprint'Cache( $H_BOTTOM, &TagA( "$PROGRAM?b=$BOARD&c=l&num=$Num&old=$NextOld", $H_NEXTART ));
	}
	else
	{
	    &cgiprint'Cache( $H_BOTTOM, $H_NONEXTART );
	}
    }
    else
    {
	if ( $From > 0 )
	{
	    &cgiprint'Cache( $H_BOTTOM, &TagA( "$PROGRAM?b=$BOARD&c=l&num=$Num&old=$BackOld", $H_BACKART ));
	}
	else
	{
	    &cgiprint'Cache( $H_BOTTOM, $H_NOBACKART );
	}
    }
    &cgiprint'Cache( "</p>\n" );

    &PrintButtonToTitleList($BOARD);
    &PrintButtonToBoardList if $SYS_F_B;

    &MsgFooter;

}

1;
