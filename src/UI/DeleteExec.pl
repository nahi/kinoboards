###
## DeleteExec - 記事の削除
#
# - SYNOPSIS
#	DeleteExec($ThreadFlag);
#
# - ARGS
#	$ThreadFlag	リプライも消すか否か
#
# - DESCRIPTION
#	記事の削除を実行し，削除後の画面を表示する．
#       大域変数である，CGI変数を参照する．
#
# - RETURN
#	なし
#
DeleteExec: {
    local($ThreadFlag) = $gVarThreadFlag;
    local($Id);

    # lock system
    local( $lockResult ) = &cgi'lock( $LOCK_FILE );
    &Fatal(1001, '') if ( $lockResult == 2 );
    &Fatal(999, '') if ( $lockResult != 1 );
    # cash article DB
    if ( $BOARD ) { &DbCash( $BOARD ); }

    $Id = $cgi'TAGS{'id'};

    # 削除実行
    &DeleteArticle($Id, $BOARD, $ThreadFlag);

    # unlock system
    &cgi'unlock( $LOCK_FILE );

    # 表示画面の作成
    &MsgHeader('Message deleted', "$BOARDNAME: $H_MESGが削除されました");

    &PrintButtonToTitleList($BOARD);
    &PrintButtonToBoardList;

    # お約束
    &MsgFooter;

}

1;
