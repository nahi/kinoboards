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

    # 全掲示板の情報を取り出す
    &GetAllBoardInfo(*BoardList, *BoardInfo);

    &MsgHeader("Board List", "$SYSTEM_NAME");

    &cgiprint'Cache(<<__EOF__);
<p>
<a href="http://www.kinotrope.co.jp/~nakahiro/kb10.shtml">KINOBOARDS/1.0</a>
で運営されているシステムです．
</p><p>
$SYSTEM_NAMEでは，現在，以下の$H_BOARDが用意されています．
</p>
__EOF__

    &cgiprint'Cache("<dl>\n");
    while(($Key, $Value) = each(%BoardList)) {
	$ModTime = &GetDateTimeFormatFromUtc(&GetModifiedTime($DB_FILE_NAME, $Key));
	$NumOfArticle = &GetArticleId($Key);
	&cgiprint'Cache("<p>\n<dt><a href=\"$PROGRAM?b=$Key&c=v&num=$DEF_TITLE_NUM\">$Value</a>\n");
	&cgiprint'Cache("[最新: $ModTime, 記事数: $NumOfArticle]\n");
	&cgiprint'Cache("<dd>$BoardInfo{$Key}\n</p>\n");
    }

    &cgiprint'Cache("</dl>\n</p>\n");

    &MsgFooter;

}


1;
