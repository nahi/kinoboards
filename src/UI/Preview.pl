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
require( 'mimew.pl' );
Preview:
{
    &LockAll();

    # cache article DB
    &DbCache( $BOARD ) if $BOARD;

    # 入力された記事情報
    local( $COrig ) = $cgi'TAGS{'corig'};
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

    local( $eSubject ) = &MIME'base64encode( $Subject );
    local( $eArticle ) = &MIME'base64encode( $Article );

    &secureSubject( *Subject );
    &secureArticle( *Article, $TextType );

    # 確認画面の作成
    &MsgHeader( 'Message preview', "書き込みの内容を確認してください" );

    if ( $Supersede && $SYS_F_D )
    {
	&cgiprint'Cache(<<__EOF__);
<p>
上の$H_MESGの替わりに，下の$H_MESGを書き込みます．
必要であれば書き込みフォームに戻って修正してください．
よろしければボタンを押して訂正しましょう．
</p>
__EOF__
    }
    else
    {
	&cgiprint'Cache(<<__EOF__);
<p>
$H_MESGをチェックし，必要なら書き込みフォームに戻って修正してください．
よろしければボタンを押して書き込みましょう．
</p>
__EOF__
    }

    # ボタン
    local( %tags, $str, $msg );
    $msg = <<__EOF__;
<input type="radio" name="com" value="e">: 戻って修正する<br>
__EOF__

    if ( $Supersede && $SYS_F_D )
    {
	$msg .= "<input type=\"radio\" name=\"com\" value=\"x\" CHECKED>: 訂正する<br>\n";
    }
    else
    {
	$msg .= "<input type=\"radio\" name=\"com\" value=\"x\" CHECKED>: $H_MESGを投稿する<br>\n";
    }

    %tags = ( 'corig', $COrig, 'c', 'x', 'b', $BOARD, 'id', $Id,
	     'texttype', $TextType,
	     'name', ( $SYS_ALIAS == 2 )? $cgi'TAGS{'name'} : $Name,
	     'mail', $Email, 'url', $Url, 'icon', $Icon, 'subject', $eSubject,
	     'article', $eArticle, 'fmail', $Fmail, 's', $Supersede,
	     'op', $op );

    &TagForm( *str, *tags, "実行", '', *msg );
    &cgiprint'Cache( $str );

    if ( $Supersede && $SYS_F_D )
    {
	&cgiprint'Cache( "$H_HR\n" );
	&ViewOriginalArticle( $Id, 0, 1 );
    }

    &cgiprint'Cache( "$H_HR\n<p>\n" );

    # 題
    &cgiprint'Cache( "<strong>$H_SUBJECT</strong>: ", &TagMsgImg( $Icon ),
	$Subject );

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
	local( $msg );
	if ( $rFid )
	{
	    &ShowLinksToFollowedArticle( *msg, ( $Id, split( /,/, $rFid )));
	}
	else
	{
	    &ShowLinksToFollowedArticle( *msg, $Id );
	}
	&cgiprint'Cache( $msg );
    }

    # 切れ目
    &cgiprint'Cache( "</p>\n$H_LINE\n" );

    # 記事
    &cgiprint'Cache( "$Article\n" );

    &MsgFooter;

    &UnlockAll();
}

1;
