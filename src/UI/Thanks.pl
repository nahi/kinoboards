###
## Thanks - 登録後画面の表示
#
# - SYNOPSIS
#	Thanks;
#
# - ARGS
#	なし
#
# - DESCRIPTION
#	書き込み後の画面を表示する
#	大域変数である，CGI変数を参照する．
#
# - RETURN
#	なし
#
Thanks: {

    local($Supersede, $Id, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail, $ArticleId);

    # lock system
    local( $lockResult ) = &cgi'lock( $LOCK_FILE ) unless $PC;
    &Fatal(1001, '') if ( $lockResult == 2 );
    &Fatal(999, '') if ( $lockResult != 1 );
    # cash article DB
    if ( $BOARD ) { &DbCash( $BOARD ); }

    # 入力された記事情報
    $Supersede = $cgi'TAGS{'s'};
    $Id = $cgi'TAGS{'id'};
    $TextType = $cgi'TAGS{'texttype'};
    $Name = $cgi'TAGS{'name'};
    $Email = $cgi'TAGS{'mail'};
    $Url = $cgi'TAGS{'url'};
    $Icon = $cgi'TAGS{'icon'};
    $Subject = $cgi'TAGS{'subject'};
    $Article = $cgi'TAGS{'article'};
    $Fmail = $cgi'TAGS{'fmail'};

    if ($Supersede && $SYS_F_D) {

	# 訂正する 
	&SupersedeArticle($BOARD, $Id, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail);

	# 表示画面の作成
	&MsgHeader('Message superseded', "$H_MESGが訂正されました");

    } else {

	# 記事の作成
	&MakeNewArticle($BOARD, $Id, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail);

	# 表示画面の作成
	&MsgHeader('Message entried', "書き込みありがとうございました");

    }

    if ($Id ne '') {
	&cgiprint'Cache(<<__EOF__);
<form action="$PROGRAM" method="POST">
<input name="b" type="hidden" value="$BOARD">
<input name="c" type="hidden" value="e">
<input name="id" type="hidden" value="$Id">
<input type="submit" value="$H_ORIGの$H_MESGへ">
</form>
__EOF__
    }

    &PrintButtonToTitleList($BOARD);
    &PrintButtonToBoardList;

    &MsgFooter;

    # unlock system
    &cgi'unlock( $LOCK_FILE ) unless $PC;
}

1;
