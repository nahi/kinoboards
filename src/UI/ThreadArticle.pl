###
## ThreadArticle - スレッド別記事一覧
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
ThreadArticle:
{
    &LockBoard;
    &DbCache( $BOARD ) if $BOARD;
    &UnlockBoard;

    local( $Id ) = $cgi'TAGS{'id'};

    # フォロー記事の木構造の取得
    # ex. '( a ( b ( c d ) ) ( e ) ( f ( g ) ) )'というリスト
    local( @FollowIdTree );
    &GetFollowIdTree($Id, *FollowIdTree);

    # 表示画面の作成
    &MsgHeader('Message view (threaded)', "$H_REPLYをまとめ読み");

    # メイン関数の呼び出し(記事概要)
    &ThreadArticleMain( 1, @FollowIdTree );

    # メイン関数の呼び出し(記事)
    &ThreadArticleMain( 0, @FollowIdTree );

    &cgiprint'Cache("$H_HR\n");

    &PrintButtonToTitleList( $BOARD, $Id );
    &PrintButtonToBoardList if $SYS_F_B;

    &MsgFooter;

}

1;
