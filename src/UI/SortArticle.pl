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
SortArticle: {

    local($Num, $Old, $NextOld, $BackOld, $To, $From, $IdNum, $Id);

    # lock system
    local( $lockResult ) = &cgi'lock( $LOCK_FILE ) unless $PC;
    &Fatal(1001, '') if ( $lockResult == 2 );
    &Fatal(999, '') if ( $lockResult != 1 );
    # cash article DB
    if ( $BOARD ) { &DbCash( $BOARD ); }
    # unlock system
    &cgi'unlock( $LOCK_FILE ) unless $PC;

    # 表示する個数を取得
    $Num = $cgi'TAGS{'num'};
    $Old = $cgi'TAGS{'old'};
    $NextOld = ($Old > $Num) ? ($Old - $Num) : 0;
    $BackOld = ($Old + $Num);
    $To = $#DB_ID - $Old;
    $From = $To - $Num + 1; $From = 0 if (($From < 0) || ($Num == 0));

    # 表示画面の作成
    &MsgHeader('Title view (sorted)', "$H_SUBJECT一覧(日付順)");

    &BoardHeader('normal');

    &cgiprint'Cache("<hr>\n");

    if ($SYS_BOTTOMTITLE) {
	&cgiprint'Cache("<p>$H_TOP" . &TagA( "$PROGRAM?b=$BOARD&c=r&num=$Num&old=$BackOld", $H_BACKART ) . "</p>\n") if ($From > 0);
    } else {
	&cgiprint'Cache("<p>$H_TOP" . &TagA( "$PROGRAM?b=$BOARD&c=r&num=$Num&old=$NextOld", $H_NEXTART ) . "</p>\n") if ($Old);
    }

    &cgiprint'Cache("<p><ul>\n");

    # 記事の表示
    if ($#DB_ID == -1) {

	# 空だった……
	&cgiprint'Cache("<li>$H_NOARTICLE\n");

    } else {

	if ($SYS_BOTTOMTITLE) {
	    for ($IdNum = $From; $IdNum <= $To; $IdNum++) {
		$Id = $DB_ID[$IdNum];
		&cgiprint'Cache("<li>" . &GetFormattedTitle($Id, $BOARD, $DB_AIDS{$Id}, $DB_ICON{$Id}, $DB_TITLE{$Id}, $DB_NAME{$Id}, $DB_DATE{$Id}) . "\n");
	    }
	} else {
	    for ($IdNum = $To; $IdNum >= $From; $IdNum--) {
		$Id = $DB_ID[$IdNum];
		&cgiprint'Cache("<li>" . &GetFormattedTitle($Id, $BOARD, $DB_AIDS{$Id}, $DB_ICON{$Id}, $DB_TITLE{$Id}, $DB_NAME{$Id}, $DB_DATE{$Id}) . "\n");
	    }
	}
    }

    &cgiprint'Cache("</ul></p>\n");

    if ($SYS_BOTTOMTITLE) {
	&cgiprint'Cache("<p>$H_BOTTOM" . &TagA( "$PROGRAM?b=$BOARD&c=r&num=$Num&old=$NextOld", $H_NEXTART ) . "</p>\n") if ($Old);
    } else {
	&cgiprint'Cache("<p>$H_BOTTOM" . &TagA( "$PROGRAM?b=$BOARD&c=r&num=$Num&old=$BackOld", $H_BACKART ) . "</p>\n") if ($From > 0);
    }

    &MsgFooter;

}

1;
