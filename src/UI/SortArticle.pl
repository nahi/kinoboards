###
## SortArticle - 日付順にソート
#
# - SYNOPSIS
#	SortArticle;
#
# - ARGS
#	なし
#
# - DESCRIPTION
#	タイトル一覧を日付順にソートして表示する．
#	大域変数である，CGI変数を参照する．
#
# - RETURN
#	なし
#
SortArticle:
{
    # lock system
    local( $lockResult ) = $PC ? 1 : &cgi'lock( $LOCK_FILE_B );
    &Fatal( 1001, '' ) if ( $lockResult == 2 );
    &Fatal( 999, '' ) if ( $lockResult != 1 );
    # cache article DB
    if ( $BOARD ) { &DbCache( $BOARD ); }
    # unlock system
    &cgi'unlock( $LOCK_FILE_B ) unless $PC;

    # 表示する個数を取得
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
    local( $NextOld ) = ( $Old > $Num ) ? ( $Old - $Num ) : 0;
    local( $BackOld ) = ( $Old + $Num );
    local( $To ) = $#DB_ID - $Old;
    local( $From ) = $To - $Num + 1;
    $From = 0 if (( $From < 0 ) || ( $Num == 0 ));

    # 表示画面の作成
    &MsgHeader('Title view (sorted)', "$H_SUBJECT一覧(日付順)");

    &BoardHeader('normal');

    &cgiprint'Cache("$H_HR\n");

    &cgiprint'Cache( "<p>" );
    &cgiprint'Cache( &TagA( "$PROGRAM?b=$BOARD&c=r&num=$Num&old=$Old&rev=" . ( 1-$Rev ), $H_REVERSE ), ' ' ) if ( $SYS_REVERSE );
    if ( $vRev )
    {
	if ( $From > 0 )
	{
	    &cgiprint'Cache( $H_TOP, &TagA( "$PROGRAM?b=$BOARD&c=r&num=$Num&old=$BackOld", $H_BACKART ));
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
	    &cgiprint'Cache( $H_TOP, &TagA( "$PROGRAM?b=$BOARD&c=r&num=$Num&old=$NextOld", $H_NEXTART ));
	}
	else
	{
	    &cgiprint'Cache( $H_TOP, $H_NONEXTART );
	}
    }
    &cgiprint'Cache( "</p>\n" );

    &cgiprint'Cache("<ul>\n");

    # 記事の表示
    if ( $#DB_ID == -1 )
    {
	# 空だった……
	&cgiprint'Cache("<li>$H_NOARTICLE\n");
    }
    else
    {
	local( $IdNum, $Id );
	if ( $vRev )
	{
	    for ($IdNum = $From; $IdNum <= $To; $IdNum++)
	    {
		$Id = $DB_ID[$IdNum];
		&cgiprint'Cache("<li>" . &GetFormattedTitle($Id, $BOARD, $DB_AIDS{$Id}, $DB_ICON{$Id}, $DB_TITLE{$Id}, $DB_NAME{$Id}, $DB_DATE{$Id}) . "\n");
	    }
	}
	else
	{
	    for ($IdNum = $To; $IdNum >= $From; $IdNum--)
	    {
		$Id = $DB_ID[$IdNum];
		&cgiprint'Cache("<li>" . &GetFormattedTitle($Id, $BOARD, $DB_AIDS{$Id}, $DB_ICON{$Id}, $DB_TITLE{$Id}, $DB_NAME{$Id}, $DB_DATE{$Id}) . "\n");
	    }
	}
    }

    &cgiprint'Cache("</ul>\n");

    &cgiprint'Cache( "<p>" );
    &cgiprint'Cache( &TagA( "$PROGRAM?b=$BOARD&c=r&num=$Num&old=$Old&rev=" . ( 1-$Rev ), $H_REVERSE ), ' ' ) if ( $SYS_REVERSE );
    if ( $vRev )
    {
	if ( $Old )
	{
	    &cgiprint'Cache( $H_BOTTOM, &TagA( "$PROGRAM?b=$BOARD&c=r&num=$Num&old=$NextOld", $H_NEXTART ));
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
	    &cgiprint'Cache( $H_BOTTOM, &TagA( "$PROGRAM?b=$BOARD&c=r&num=$Num&old=$BackOld", $H_BACKART ));
	}
	else
	{
	    &cgiprint'Cache( $H_BOTTOM, $H_NOBACKART );
	}
    }
    &cgiprint'Cache( "</p>" );

    &MsgFooter;

}

1;
