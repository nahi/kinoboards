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
Thanks:
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

    local( $base ) = ( -M $BOARD_ALIAS_FILE );
    if (( $op == 0 ) || ( $base - $op > 1 ) || ( $op > $base ))
    {
	&Fatal( 15, '' );
    }

    if ( $SYS_DENY_FORM_RECYCLE )
    {
	local( $dId, $dKey );
	&GetArticleId( $BOARD, *dId, *dKey );
	&Fatal( 16, '' ) if ( $dKey && ( $dKey == $op ));
    }

    # Preview経由でEncodeされているかもしれない
    $Article = &DQDecode( $Article );
    $Subject = &DQDecode( $Subject );

    &secureSubject( *Subject );
    &secureArticle( *Article, $TextType );

    local( $newArtId );
    if ( $Supersede && $SYS_F_D )
    {
	# 訂正する 
	$newArtId = &SupersedeArticle($BOARD, $Id, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail);

	# 表示画面の作成
	&MsgHeader('Message superseded', "$H_MESGが訂正されました");
    }
    else
    {
	# 記事の作成
	$newArtId = &MakeNewArticle($BOARD, $Id, $op, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail);

	# 表示画面の作成
	&MsgHeader('Message entried', "書き込みありがとうございました");
    }

    if  ( $SYS_COMMAND_BUTTON )
    {
	local( %tags ) = ( 'b', $BOARD, 'c', 'e', 'id', $newArtId );
	local( $str );
	&TagForm( *str, *tags, "書き込んだ$H_MESGへ", '', '' );
	&cgiprint'Cache( $str );
    }
    else
    {
	&cgiprint'Cache( "<p><a href=\"$PROGRAM?b=$BOARD&c=e&id=$newArtId\">書き込んだ$H_MESGへ</a></p>\n" );
    }

    if ( $Id ne '' )
    {
	if  ( $SYS_COMMAND_BUTTON )
	{
	    local( %tags ) = ( 'b', $BOARD, 'c', 'e', 'id', $Id );
	    local( $str ) = '';
	    &TagForm( *str, *tags, "$H_ORIGの$H_MESGへ", '', '' );
	    &cgiprint'Cache( $str );
	}
	else
	{
	    &cgiprint'Cache( "<p><a href=\"$PROGRAM?b=$BOARD&c=e&id=$Id\">$H_ORIGの$H_MESGへ</a></p>\n" );
	}
    }

    &PrintButtonToTitleList( $BOARD );
    &PrintButtonToBoardList if $SYS_F_B;

    &MsgFooter;

    # unlock system
    &cgi'unlock( $LOCK_FILE_B ) unless $PC;
    &cgi'unlock( $LOCK_FILE ) unless $PC;
}

1;
