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

    local($Supersede, $Id, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail, $rFid, $eArticle, $eSubject);

    # lock system
    local( $lockResult ) = $PC ? 1 : &cgi'lock( $LOCK_FILE );
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
    &CheckArticle($BOARD, *Name, *Email, *Url, *Subject, *Icon, *Article);

    $eArticle = &DQEncode( $Article );
    $eSubject = &DQEncode( $Subject );

    # 確認画面の作成
    &MsgHeader('Message preview', "書き込みの内容を確認してください");

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
<input name="subject"  type="hidden" value="$eSubject">
<input name="article"  type="hidden" value="$eArticle">
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
        ? &cgiprint'Cache( "<strong>$H_SUBJECT</strong>: " . $Subject )
            : &cgiprint'Cache( "<strong>$H_SUBJECT</strong>: " . &TagMsgImg( &GetIconUrlFromTitle($Icon, $BOARD), "$Icon " ) . $Subject );

    # お名前
    if ($Url ne '') {
        # URLがある場合
        &cgiprint'Cache( "<br>\n<strong>$H_FROM</strong>: " . &TagA( $Url, $Name ));
    } else {
        # URLがない場合
        &cgiprint'Cache( "<br>\n<strong>$H_FROM</strong>: " . $Name );
    }

    # メイル
    &cgiprint'Cache( " " . &TagA( "mailto:$Email", "&lt;$Email&gt;" )) if ( $Email ne '' );

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
    if ( !$SYS_TEXTTYPE ) {
	# pre-formatted
	&PlainArticleToPreFormatted( *Article );
    }
    elsif ( $TextType eq $H_TTLABEL[2] ) {
	# nothing to do. it's HTML.
    }
    elsif ( $TextType eq $H_TTLABEL[1] ) {
	# convert to html
	&PlainArticleToHtml( *Article );
    }
    elsif ( $TextType eq $H_TTLABEL[0] ) {
	# pre-formatted
	&PlainArticleToPreFormatted( *Article );
    }
    else {
	&Fatal( 0, 'must not be reached...MakeArticleFile' );
    }

    # 記事
    $Article = &ArticleEncode($Article);
    &cgi'SecureHtml(*Article);
    &cgiprint'Cache("$Article\n");

    &MsgFooter;

    # unlock system
    &cgi'unlock( $LOCK_FILE ) unless $PC;
}

1;
