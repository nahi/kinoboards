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
    local( %BoardList, %BoardInfo, $Key, $Value, $NumOfArticle );

    # 全掲示板の情報を取り出す
    &GetAllBoardInfo( *BoardList, *BoardInfo );

    &MsgHeader( "Board List", "$SYSTEM_NAME" );

    &cgiprint'Cache( "<p>\n" . &TagA( "http://www.kinotrope.co.jp/~nakahiro/kb10.shtml", "KINOBOARDS/1.0" ));
    &cgiprint'Cache(<<__EOF__);
で運営されているシステムです．
</p>

<p>
$SYSTEM_NAMEでは，現在，以下の$H_BOARDが用意されています．
</p>
__EOF__

    &cgiprint'Cache("<ul>\n");
    local( $newIcon, $modTimeUtc, $modTime );
    while (( $Key, $Value ) = each( %BoardList ))
    {
	$modTimeUtc = &GetModifiedTime( $DB_FILE_NAME, $Key );
	$modTime = &GetDateTimeFormatFromUtc( $modTimeUtc );
	if ( $SYS_BLIST_NEWICON_DATE && (( $^T - $modTimeUtc ) < $SYS_BLIST_NEWICON_DATE * 86400 ))
	{
	    $newIcon = " " . &TagMsgImg( $ICON_NEW, $H_NEWARTICLE );
	}
	else
	{
	    $newIcon = '';
	}
	&GetArticleId( $Key, *NumOfArticle ) || 0;

	&cgiprint'Cache( "<li>", &TagA( "$PROGRAM?b=$Key&c=v&num=$DEF_TITLE_NUM", $Value ), "$newIcon\n[最新: $modTime, 記事数: $NumOfArticle]<br>\n" );
    }

    &cgiprint'Cache("</ul>\n");

    &MsgFooter;

}


1;
