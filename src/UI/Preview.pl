###
## Preview - プレビュー画面の表示
#
# - SYNOPSIS
#	Preview;
#
# - ARGS
#	なし
#
# - DESCRIPTION
#	プレビュー画面を表示する．
#	大域変数である，CGI変数を参照する．
#
# - RETURN
#	なし
#
Preview: {

    local($Supersede, $Id, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail, $rFid);

    # lock system
    local( $lockResult ) = &cgi'lock( $LOCK_FILE );
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
    if ($Id ne '') { ($rFid) = &GetArticlesInfo($Id); } else { $rFid = ''; }

    # 入力された記事情報のチェック
    $Article = &CheckArticle($BOARD, *Name, *Email, *Url, *Subject, *Icon, $Article);

    # 確認画面の作成
    &MsgHeader('Message preview', "$BOARDNAME: 書き込みの内容を確認してください");

    # お約束
    &cgiprint'Cache(<<__EOF__);
<form action="$PROGRAM" method="POST">
<input name="c"        type="hidden" value="x">
<input name="b"        type="hidden" value="$BOARD">
<input name="id"       type="hidden" value="$Id">
<input name="texttype" type="hidden" value="$TextType">
<input name="name"     type="hidden" value="$Name">
<input name="mail"     type="hidden" value="$Email">
<input name="url"      type="hidden" value="$Url">
<input name="icon"     type="hidden" value="$Icon">
<input name="subject"  type="hidden" value="$Subject">
<input name="article"  type="hidden" value="$Article">
<input name="fmail"    type="hidden" value="$Fmail">
<input name="s"        type="hidden" value="$Supersede">

__EOF__

    if ($Supersede && $SYS_F_D) {
	&cgiprint'Cache(<<__EOF__);
<p>
上の$H_MESGの替わりに，下の$H_MESGを書き込みます．
必要であれば，ブラウザのBACKボタンで戻って，書き込みを修正してください．
よろしければボタンを押して訂正しましょう．
<input type="submit" value="訂正します">
</p>
</form>
__EOF__
	&ViewOriginalArticle($Id, 0, 1);
	&cgiprint'Cache("<hr>\n");
    } else {
	&cgiprint'Cache(<<__EOF__);
<p>
必要であれば，ブラウザのBACKボタンで戻って，書き込みを修正してください．
よろしければボタンを押して書き込みましょう．
<input type="submit" value="投稿する">
</p>
</form>
__EOF__
    }

    &cgiprint'Cache("<p>\n");

    # 題
    (($Icon eq $H_NOICON) || (! $Icon))
        ? &cgiprint'Cache("<strong>$H_SUBJECT</strong>: $Subject")
            : &cgiprint'Cache(sprintf("<strong>$H_SUBJECT</strong>: <img src=\"%s\" alt=\"$Icon \" width=\"$MSGICON_WIDTH\" height=\"$MSGICON_HEIGHT\">$Subject", &GetIconUrlFromTitle($Icon, $BOARD)));

    # お名前
    if ($Url ne '') {
        # URLがある場合
        &cgiprint'Cache("<br>\n<strong>$H_FROM</strong>: <a href=\"$Url\">$Name</a>");
    } else {
        # URLがない場合
        &cgiprint'Cache("<br>\n<strong>$H_FROM</strong>: $Name");
    }

    # メイル
    if ($Email ne '') {
	&cgiprint'Cache(" <a href=\"mailto:$Email\">&lt;$Email&gt;</a>");
    }

    # 反応元(引用の場合)
    if ($rFid) {
	if ($rFid ne '') {
	    &ShowLinksToFollowedArticle(($Id, split(/,/, $rFid)));
	} else {
	    &ShowLinksToFollowedArticle($Id);
	}
    }

    # 切れ目
    &cgiprint'Cache("</p>\n$H_LINE\n");

    # TextType用前処理
    if ((! $SYS_TEXTTYPE) || ($TextType eq $H_PLAIN)) {
	&PlainArticleToHtml( *Article );
    }

    # 記事
    $Article = &DQDecode($Article);
    $Article = &ArticleEncode($Article);
    &cgiprint'Cache("$Article\n");

    &MsgFooter;

    # unlock system
    &cgi'unlock( $LOCK_FILE );
}

1;
