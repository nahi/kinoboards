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
NewArticle: {

    local($Num, $Old, $NextOld, $BackOld, $To, $From, $Id);

    # lock system
    local( $lockResult ) = $PC ? 1 : &cgi'lock( $LOCK_FILE );
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
    &MsgHeader('Message view (sorted)', "最近の$H_MESGをまとめ読み");

    if ($SYS_BOTTOMARTICLE) {
	&cgiprint'Cache("<p>$H_TOP" . &TagA( "$PROGRAM?b=$BOARD&c=l&num=$Num&old=$BackOld", $H_BACKART ) . "</p>\n") if ($From > 0);
    } else {
	&cgiprint'Cache("<p>$H_TOP" . &TagA( "$PROGRAM?b=$BOARD&c=l&num=$Num&old=$NextOld", $H_NEXTART ) . "</p>\n") if ($Old);
    }

    if (! $#DB_ID == -1) {

	# 空だった……
	&cgiprint'Cache("<p>$H_NOARTICLE</p>\n");

    } else {

	if ($SYS_BOTTOMARTICLE) {
	    for ($IdNum = $From; $IdNum <= $To; $IdNum++) {
		$Id = $DB_ID[$IdNum];
		&ViewOriginalArticle($Id, 1, 1);
		&cgiprint'Cache("<hr>\n");
	    }
	} else {
	    for ($IdNum = $To; $IdNum >= $From; $IdNum--) {
		$Id = $DB_ID[$IdNum];
		&ViewOriginalArticle($Id, 1, 1);
		&cgiprint'Cache("<hr>\n");
	    }
	}

    }

    if ($SYS_BOTTOMARTICLE) {
	&cgiprint'Cache("<p>$H_BOTTOM" . &TagA( "$PROGRAM?b=$BOARD&c=l&num=$Num&old=$NextOld", $H_NEXTART ) . "</p>\n") if ($Old);
    } else {
	&cgiprint'Cache("<p>$H_BOTTOM" . &TagA( "$PROGRAM?b=$BOARD&c=l&num=$Num&old=$BackOld", $H_BACKART ) . "</p>\n") if ($From > 0);
    }

    &PrintButtonToTitleList($BOARD);
    &PrintButtonToBoardList;

    &MsgFooter;

}

1;
