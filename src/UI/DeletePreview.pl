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
    local( $lockResult ) = $PC ? 1 : &cgi'lock( $LOCK_FILE );
    &Fatal(1001, '') if ( $lockResult == 2 );
    &Fatal(999, '') if ( $lockResult != 1 );
    # cash article DB
    if ( $BOARD ) { &DbCash( $BOARD ); }
    # unlock system
    &cgi'unlock( $LOCK_FILE ) unless $PC;

    $Id = $cgi'TAGS{'id'};

    # 表示画面の作成
    &MsgHeader("Delete Article", "$H_MESGの削除");

    &cgiprint'Cache(<<__EOF__);
<p>
本当にこの$H_MESGを削除するのですね? よろしければボタンを押してください．
</p>
__EOF__

    # お約束
    &cgiprint'Cache(<<__EOF__);
<form action="$PROGRAM" method="POST">
<input name="c" type="hidden" value="de">
<input name="b" type="hidden" value="$BOARD">
<input name="id" type="hidden" value="$Id">
<input type="submit" value="この記事を削除します">
</form>
<form action="$PROGRAM" method="POST">
<input name="c" type="hidden" value="det">
<input name="b" type="hidden" value="$BOARD">
<input name="id" type="hidden" value="$Id">
<input type="submit" value="リプライ記事もまとめて削除します">
</form>
</p>
<hr>
__EOF__

    # 削除ファイルの表示
    &ViewOriginalArticle($Id, 0, 1);

    # お約束
    &MsgFooter;

}

1;
