###
## SortTitle - 日付順タイトル一覧
#
# - SYNOPSIS
#	SortTitle;
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
SortTitle:
{
    &LockBoard();
    # cache article DB
    &DbCache( $BOARD ) if $BOARD;
    &UnlockBoard();

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
    local( $To ) = $#DB_ID - $Old;
    local( $From ) = $To - $Num + 1;
    $From = 0 if (( $From < 0 ) || ( $Num == 0 ));

    local( $pageLinkStr ) = &PageLink( 'r', $Num, $Old, $Rev );

    # 表示画面の作成
    &MsgHeader( 'Sorted view', "$H_SUBJECT一覧(日付順)" );

    &BoardHeader();
    &cgiprint'Cache("$H_HR\n");
    &cgiprint'Cache( $pageLinkStr );

    &cgiprint'Cache("<ul>\n");

    # 記事の表示
    local( $IdNum, $Id );
    if ( $#DB_ID == -1 )
    {
	# 空だった……
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
