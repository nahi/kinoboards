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
DeletePreview: {

    local($Id);

    # lock system
    local( $lockResult ) = $PC ? 1 : &cgi'lock( $LOCK_FILE_B );
    &Fatal(1001, '') if ( $lockResult == 2 );
    &Fatal(999, '') if ( $lockResult != 1 );
    # cache article DB
    if ( $BOARD ) { &DbCache( $BOARD ); }
    # unlock system
    &cgi'unlock( $LOCK_FILE_B ) unless $PC;

    $Id = $cgi'TAGS{'id'};

    # 表示画面の作成
    &MsgHeader("Delete Article", "$H_MESGの削除");

    &cgiprint'Cache(<<__EOF__);
<p>
本当にこの$H_MESGを削除するのですね? よろしければボタンを押してください．
</p>
__EOF__

    local( %tags, $str );
    %tags = ( 'c', 'de', 'b', $BOARD, 'id', $Id );
    &TagForm( *str, *tags, "この記事を削除します", '', '' );
    &cgiprint'Cache( $str );

    %tags = ( 'c', 'det', 'b', $BOARD, 'id', $Id );
    &TagForm( *str, *tags, "リプライ記事もまとめて削除します", '', '' );
    &cgiprint'Cache( $str );

    &cgiprint'Cache( $H_HR );

    # 削除ファイルの表示
    &ViewOriginalArticle($Id, 0, 1);

    # お約束
    &MsgFooter;

}

1;
