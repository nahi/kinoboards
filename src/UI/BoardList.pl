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
BoardList: {

    local(%BoardList, %BoardInfo, $Key, $Value, $ModTime, $NumOfArticle);

    # lock system
    local( $lockResult ) = $PC ? 1 : &cgi'lock( $LOCK_FILE );
    &Fatal(1001, '') if ( $lockResult == 2 );
    &Fatal(999, '') if ( $lockResult != 1 );

    # 全掲示板の情報を取り出す
    &GetAllBoardInfo(*BoardList, *BoardInfo);

    &MsgHeader("Board List", "$SYSTEM_NAME");

    &cgiprint'Cache( "<p>\n" . &TagA( "http://www.kinotrope.co.jp/~nakahiro/kb10.shtml", "KINOBOARDS/1.0" ));
    &cgiprint'Cache(<<__EOF__);
で運営されているシステムです．
</p><p>
$SYSTEM_NAMEでは，現在，以下の$H_BOARDが用意されています．
</p>
__EOF__

    &cgiprint'Cache("<ul>\n");
    while(($Key, $Value) = each(%BoardList)) {
	$ModTime = &GetDateTimeFormatFromUtc(&GetModifiedTime($DB_FILE_NAME, $Key));
	$NumOfArticle = &GetArticleId($Key) || 0;
	&cgiprint'Cache("<li>" . &TagA( "$PROGRAM?b=$Key&c=v&num=$DEF_TITLE_NUM", $Value ) . "\n");
	&cgiprint'Cache("[最新: $ModTime, 記事数: $NumOfArticle]\n");
    }

    &cgiprint'Cache("</ul>\n");

    # unlock system
    &cgi'unlock( $LOCK_FILE ) unless $PC;

    &MsgFooter;

}


1;
