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

    $Id = $cgi'TAGS{'id'};

    # 削除実行
    &DeleteArticle($Id, $BOARD, $ThreadFlag);

    # 表示画面の作成
    &MsgHeader('Message deleted', "$BOARDNAME: $H_MESGが削除されました");

    &PrintButtonToTitleList($BOARD);
    &PrintButtonToBoardList;

    # お約束
    &MsgFooter;

}

1;
