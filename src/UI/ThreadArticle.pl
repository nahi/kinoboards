###
## ThreadArticle - フォロー記事を全て表示．
#
# - SYNOPSIS
#	ThreadArticle;
#
# - ARGS
#	なし
#
# - DESCRIPTION
#	ある記事と，その記事へのリプライ記事をまとめて表示する．
#       大域変数である，CGI変数を参照する．
#
# - RETURN
#	なし
#
ThreadArticle: {

    local($Id, @FollowIdTree);

    # lock system
    local( $lockResult ) = $PC ? 1 : &cgi'lock( $LOCK_FILE_B );
    &Fatal(1001, '') if ( $lockResult == 2 );
    &Fatal(999, '') if ( $lockResult != 1 );
    # cache article DB
    if ( $BOARD ) { &DbCache( $BOARD ); }
    # unlock system
    &cgi'unlock( $LOCK_FILE_B ) unless $PC;

    $Id = $cgi'TAGS{'id'};

    # フォロー記事の木構造の取得
    # ex. '( a ( b ( c d ) ) ( e ) ( f ( g ) ) )'というリスト
    &GetFollowIdTree($Id, *FollowIdTree);

    # 表示画面の作成
    &MsgHeader('Message view (threaded)', "$H_REPLYをまとめ読み");

    # メイン関数の呼び出し(記事概要)
    &ThreadArticleMain('subject only', @FollowIdTree);

    # メイン関数の呼び出し(記事)
    &ThreadArticleMain('', @FollowIdTree);

    &cgiprint'Cache("$H_HR\n");

    &PrintButtonToTitleList($BOARD);
    &PrintButtonToBoardList if $SYS_F_B;

    &MsgFooter;

}

1;
