###
## ShowIcon - アイコン表示画面
#
# - SYNOPSIS
#	ShowIcon;
#
# - ARGS
#	なし
#
# - DESCRIPTION
#	アイコン表示画面を表示する．
#	大域変数である，CGI変数を参照する．
#
# - RETURN
#	なし
#
ShowIcon:
{
    # タイプを拾う
    local( $Type ) = $cgi'TAGS{'type'};

    # 表示画面の作成
    &MsgHeader( 'Icon show', "アイコンの説明" );

    local( $msg );
    if ( $Type eq 'article' )
    {
	$msg .= <<__EOF__;
<p>
各アイコンは次の機能を表しています．
</p>

<ul>
<li>$H_THREAD : その$H_MESGの$H_REPLYをまとめて表示します．
__EOF__

	$msg .= '<li>' . &TagMsgImg( $ICON_NEW, $H_NEWARTICLE ) .
	     " : 最近書き込まれた$H_MESG\n";

	$msg .= '<li>' . &TagComImg( $ICON_BLIST, $H_BACKBOARD, 2 ) . "\n";
	$msg .= '<li>' . &TagComImg( $ICON_TLIST, $H_BACKTITLEREPLY, 2 ) ."\n";
	$msg .= '<li>' . &TagComImg( $ICON_PREV, $H_PREVARTICLE, 2 ) . "\n";
	$msg .= '<li>' . &TagComImg( $ICON_NEXT, $H_NEXTARTICLE, 2 ) . "\n";
	$msg .= '<li>' . &TagComImg( $ICON_THREAD, $H_READREPLYALL, 2 ) . "\n";
	$msg .= "<br><br>\n";
	$msg .= '<li>' . &TagComImg( $ICON_WRITENEW, $H_POSTNEWARTICLE, 2 ) .
	    "\n";
	$msg .= '<li>' . &TagComImg( $ICON_FOLLOW, $H_REPLYTHISARTICLE, 2 ) .
	    "\n";
	$msg .= '<li>' . &TagComImg( $ICON_QUOTE, $H_REPLYTHISARTICLEQUOTE, 2 )
	    . "\n";
	$msg .= "</ul>\n";
    }
    else
    {
	&CacheIconDb;	# アイコンDBのキャッシュ
	$msg .= <<__EOF__;
<p>
$H_BOARD「$BOARDNAME」では，各アイコンは次のような意味です．
</p>

<ul>
<li>$H_THREAD_ALL : その$H_MESGの$H_ORIG_TOPから，全ての$H_REPLYをまとめて表示します．
<li>$H_THREAD : その$H_MESGの$H_REPLYをまとめて表示します．
<br><br>
__EOF__
	$msg .= '<li>' . &TagMsgImg( $ICON_NEW, $H_NEWARTICLE ) .
	    " : 最近書き込まれた$H_MESG\n<br><br>\n";

	local( $IconTitle );
	foreach $IconTitle (@ICON_TITLE)
	{
	    $msg .= '<li>' .
		&TagMsgImg( &GetIconUrlFromTitle( $IconTitle, $BOARD ),
		    $IconTitle ) . " : " .
		    ( $ICON_HELP{$IconTitle} || $IconTitle ) . "\n";
	}
	$msg .= "</ul>\n";
    }

    &cgiprint'Cache( $msg );
    &MsgFooter;
}

1;
