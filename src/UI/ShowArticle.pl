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
ShowArticle:
{
    &LockBoard;
    # cache article DB
    &DbCache( $BOARD ) if $BOARD;

    local( $id ) = $cgi'TAGS{'id'};
    local( $fId, $aids, $date, $subject ) = &GetArticlesInfo( $id );

    # 未投稿記事は読めない
    &Fatal( 8, '' ) if ( $subject eq '' );

    # 表示画面の作成
    &MsgHeader( 'Message view', $subject );
    &ViewOriginalArticle( $id, 1, 1 );
    &ReplyArticles( split( /,/, $aids ));
    &MsgFooter;

    &UnlockBoard;
}

1;
