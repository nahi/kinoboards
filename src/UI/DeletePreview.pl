###
## DeletePreview - 削除記事の確認
#
# - SYNOPSIS
#	DeletePreview;
#
# - ARGS
#	なし
#
# - DESCRIPTION
#	削除記事の確認画面を表示する
#       大域変数である，CGI変数を参照する．
#
# - RETURN
#	なし
#
DeletePreview:
{
    &LockBoard;
    # cache article DB
    &DbCache( $BOARD ) if $BOARD;
    &UnlockBoard;

    local( $id ) = $cgi'TAGS{'id'};
    local( $fId, $aids, $date, $subject ) = &GetArticlesInfo( $id );

    # 未投稿記事は読めない
    if ( $subject eq '' ) { &Fatal( 8, '' ); }

    # 表示画面の作成
    &MsgHeader( 'Delete Article', "$H_MESGの削除" );

    &cgiprint'Cache(<<__EOF__);
<p>
本当にこの$H_MESGを削除するのですね? よろしければボタンを押してください．
</p>
__EOF__

    local( %tags, $str );
    %tags = ( 'c', 'de', 'b', $BOARD, 'id', $id );
    &TagForm( *str, *tags, "この記事を削除します", '', '' );
    &cgiprint'Cache( $str );

    if ( $aids )
    {
	%tags = ( 'c', 'det', 'b', $BOARD, 'id', $id );
	&TagForm( *str, *tags, "リプライ記事もまとめて削除します", '', '' );
	&cgiprint'Cache( $str );
    }

    &cgiprint'Cache( $H_HR );

    # 削除ファイルの表示
    &ViewOriginalArticle( $id, 0, 1 );

    &ReplyArticles( split( /,/, $aids ));
    &MsgFooter;
}

1;
