###
## ShowArticle - 単一記事の表示
#
# - SYNOPSIS
#	ShowArticle;
#
# - ARGS
#	なし
#
# - DESCRIPTION
#	単一の記事を表示する．
#       大域変数である，CGI変数を参照する．
#
# - RETURN
#	なし
#
ShowArticle: {

    local($Id, $Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $DateUtc, $Aid, @AidList, @FollowIdTree);

    # lock system
    local( $lockResult ) = &cgi'lock( $LOCK_FILE );
    &Fatal(1001, '') if ( $lockResult == 2 );
    &Fatal(999, '') if ( $lockResult != 1 );
    # cash article DB
    if ( $BOARD ) { &DbCash( $BOARD ); }

    $Id = $cgi'TAGS{'id'};
    ($Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url) = &GetArticlesInfo($Id);
    $DateUtc = &GetUtcFromOldDateTimeFormat($Date);
    @AidList = split(/,/, $Aids);

    # 未投稿記事は読めない
    if ($Name eq '') { &Fatal(8, ''); }

    # 表示画面の作成
    &MsgHeader('Message view', "$BOARDNAME: $Subject", $DateUtc);
    &ViewOriginalArticle($Id, 1, 1);

    # article end
    &cgiprint'Cache("$H_LINE\n<p>\n");

    # 反応記事
    &cgiprint'Cache("▼$H_REPLY\n");
    if ($Aids ne '') {

	# 反応記事があるなら…
	foreach $Aid (@AidList) {

	    # フォロー記事の木構造の取得
	    # ex. '( a ( b ( c d ) ) ( e ) ( f ( g ) ) )'というリスト
	    @FollowIdTree = &GetFollowIdTree($Aid);

	    # メイン関数の呼び出し(記事概要)
	    &ThreadArticleMain('subject only', @FollowIdTree);

	}

    } else {

	# 反応記事無し
	&cgiprint'Cache("<ul>\n<li>$H_REPLYはありません\n</ul>\n");

    }

    &cgiprint'Cache("</p>\n");

    # お約束
    &MsgFooter;

    # unlock system
    &cgi'unlock( $LOCK_FILE );

}

1;
