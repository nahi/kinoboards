###
## BoardList - 掲示板一覧の表示
#
# - SYNOPSIS
#	BoardList;
#
# - ARGS
#	なし
#
# - DESCRIPTION
#	掲示板一覧を表示する．
#
# - RETURN
#	なし
#
BoardList:
{
    # 全掲示板の情報を取り出す
    local( @board, %boardName, %boardInfo );
    &GetAllBoardInfo( *board, *boardName, *boardInfo );

    # 「$H_BOARD一覧 - $SYSTEM_NAME」が，このページのタイトルです．
    &MsgHeader( "Board List", "$H_BOARD一覧 - $SYSTEM_NAME" );
    &cgiprint'Cache(<<__EOF__);

<!-- 掲示板一覧のヘッダ部分です．この辺，がんがん書き換えましょう． -->
<p>
$SYSTEM_NAMEでは，現在，以下の$H_BOARDが用意されています．
</p>

<ul>
__EOF__

    local( $newIcon, $modTimeUtc, $modTime, $nofArticle );
    foreach ( @board )
    {
	$modTimeUtc = &GetModifiedTime( $DB_FILE_NAME, $_ );
	$modTime = &GetDateTimeFormatFromUtc( $modTimeUtc );
	if ( $SYS_BLIST_NEWICON_DATE &&
	    (( $^T - $modTimeUtc ) < $SYS_BLIST_NEWICON_DATE * 86400 ))
	{
	    $newIcon = " " . &TagMsgImg( $H_NEWARTICLE );
	}
	else
	{
	    $newIcon = '';
	}
	&GetArticleId( $_, *nofArticle ) || 0;

	&cgiprint'Cache( "<li>",
	    &TagA( "$PROGRAM?b=$_&c=v&num=$DEF_TITLE_NUM", $boardName{$_} ),
	    "$newIcon\n[最新: $modTime, 記事数: $nofArticle]\n" );

    &cgiprint'Cache(<<__EOF__);
<br><br><!-- 掲示板同士の間に入ります．間を空けるためにBRタグとか -->
__EOF__

    }

    &cgiprint'Cache(<<__EOF__);
</ul>

<!-- 掲示板一覧のフッタ部分です．がんがん書き換えましょう． -->
<p>
$SYSTEM_NAMEでは，現在，以上の$H_BOARDが用意されています．
</p>

__EOF__

    &MsgFooter;
}


1;
