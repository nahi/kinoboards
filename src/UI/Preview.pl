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
Preview:
{
    # lock system
    local( $lockResult ) = $PC ? 1 : &cgi'lock( $LOCK_FILE );
    &Fatal( 1001, '' ) if ( $lockResult == 2 );
    &Fatal( 999, '' ) if ( $lockResult != 1 );
    # lock system
    $lockResult = $PC ? 1 : &cgi'lock( $LOCK_FILE_B );
    &Fatal( 1001, '' ) if ( $lockResult == 2 );
    &Fatal( 999, '' ) if ( $lockResult != 1 );

    # cache article DB
    &DbCache( $BOARD ) if $BOARD;

    # 入力された記事情報
    local( $Name ) = $cgi'TAGS{'name'};
    local( $Email ) = $cgi'TAGS{'mail'};
    local( $Url ) = $cgi'TAGS{'url'};
    local( $Supersede ) = $cgi'TAGS{'s'};
    local( $Id ) = $cgi'TAGS{'id'};
    local( $TextType ) = $cgi'TAGS{'texttype'};
    local( $Icon ) = $cgi'TAGS{'icon'};
    local( $Subject ) = $cgi'TAGS{'subject'};
    local( $Article ) = $cgi'TAGS{'article'};
    local( $Fmail ) = $cgi'TAGS{'fmail'};
    local( $op ) = $cgi'TAGS{'op'};

    local( $rFid ) = '';
    ( $rFid ) = &GetArticlesInfo( $Id ) if ( $Id ne '' );

    # 入力された記事情報のチェック
    &CheckArticle( $BOARD, *Name, *Email, *Url, *Subject, *Icon, *Article );

    local( $eSubject ) = &DQEncode( $Subject );
    local( $eArticle ) = &DQEncode( $Article );

    &secureSubject( *Subject );
    &secureArticle( *Article, $TextType );

    # 確認画面の作成
    &MsgHeader( 'Message preview', "書き込みの内容を確認してください" );

    local( %tags, $str, $msg );
    %tags = ( 'c', 'x', 'b', $BOARD, 'id', $Id, 'texttype', $TextType,
	     'name', $Name, 'mail', $Email, 'url', $Url, 'icon', $Icon,
	     'subject', $eSubject, 'article', $eArticle, 'fmail', $Fmail,
	     's', $Supersede, 'op', $op );

    if ( $Supersede && $SYS_F_D )
    {
	$msg =<<__EOF__;
<p>
上の$H_MESGの替わりに，下の$H_MESGを書き込みます．
必要であれば，ブラウザのBACKボタンで戻って，書き込みを修正してください．
よろしければボタンを押して訂正しましょう．
</p>
__EOF__
	&TagForm( *str, *tags, "訂正します", '', *msg );
	&cgiprint'Cache( $str );
	&ViewOriginalArticle( $Id, 0, 1 );
	&cgiprint'Cache( "$H_HR\n" );
    }
    else
    {
	$msg = <<__EOF__;
<p>
必要であれば，ブラウザのBACKボタンで戻って，書き込みを修正してください．
よろしければボタンを押して書き込みましょう．
</p>
__EOF__
	&TagForm( *str, *tags, "投稿します", '', *msg );
	&cgiprint'Cache( $str );
    }

    &cgiprint'Cache( "<p>\n" );

    # 題
    if (( $Icon eq $H_NOICON ) || ( !$Icon ))
    {
        &cgiprint'Cache( "<strong>$H_SUBJECT</strong>: $Subject" );
    }
    else
    {
	&cgiprint'Cache( "<strong>$H_SUBJECT</strong>: ", &TagMsgImg( &GetIconUrlFromTitle($Icon, $BOARD), "$Icon " ), $Subject );
    }

    # お名前
    if ( $Url ne '' )
    {
        # URLがある場合
        &cgiprint'Cache( "<br>\n<strong>$H_FROM</strong>: ", &TagA( $Url, $Name ));
    }
    else
    {
        # URLがない場合
        &cgiprint'Cache( "<br>\n<strong>$H_FROM</strong>: $Name" );
    }

    # メイル
    &cgiprint'Cache( " ", &TagA( "mailto:$Email", "&lt;$Email&gt;" ))
	if $Email;

    # 反応元(引用の場合)
    if ( $Id )
    {
	if ( $rFid )
	{
	    &ShowLinksToFollowedArticle(( $Id, split( /,/, $rFid )));
	}
	else
	{
	    &ShowLinksToFollowedArticle( $Id );
	}
    }

    # 切れ目
    &cgiprint'Cache( "</p>\n$H_LINE\n" );

    # 記事
    &cgiprint'Cache( "$Article\n" );
    &MsgFooter;

    # unlock system
    &cgi'unlock( $LOCK_FILE_B ) unless $PC;
    &cgi'unlock( $LOCK_FILE ) unless $PC;
}

1;
