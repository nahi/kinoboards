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

    if ( $Type eq 'article' )
    {
	&cgiprint'Cache(<<__EOF__);
<p>
各アイコンは次の機能を表しています．
</p>

<ul>
<li>$H_THREAD : その$H_MESGの$H_REPLYをまとめて読む
<br><br>
__EOF__

	&cgiprint'Cache( "<li>", &TagComImg( $ICON_BLIST, $H_BACKBOARD, 2 ), "\n" );
	&cgiprint'Cache( "<li>", &TagComImg( $ICON_TLIST, $H_BACKTITLEREPLY, 2 ), "\n" );
	&cgiprint'Cache( "<li>", &TagComImg( $ICON_PREV, $H_PREVARTICLE, 2 ), "\n" );
	&cgiprint'Cache( "<li>", &TagComImg( $ICON_NEXT, $H_NEXTARTICLE, 2 ), "\n" );
	&cgiprint'Cache( "<li>", &TagComImg( $ICON_THREAD, $H_READREPLYALL, 2 ), "\n" );
	&cgiprint'Cache( "</p><p>\n" );
	&cgiprint'Cache( "<li>", &TagComImg( $ICON_WRITENEW, $H_POSTNEWARTICLE, 2 ), "\n" );
	&cgiprint'Cache( "<li>", &TagComImg( $ICON_FOLLOW, $H_REPLYTHISARTICLE, 2 ), "\n" );
	&cgiprint'Cache( "<li>", &TagComImg( $ICON_QUOTE, $H_REPLYTHISARTICLEQUOTE, 2 ), "\n" );
	&cgiprint'Cache(<<__EOF__);
</ul>
__EOF__
    }
    else
    {
	&CacheIconDb($BOARD);	# アイコンDBのキャッシュ
	&cgiprint'Cache(<<__EOF__);
<p>
$H_BOARD「$BOARDNAME」では，各アイコンは次のような意味です．
</p>

<ul>
__EOF__
	&cgiprint'Cache( "<li>", &TagMsgImg( $ICON_NEW, $H_NEWARTICLE ), " : 最近書き込まれた$H_MESG\n<br><br>\n" );

	local( $IconTitle );
	foreach $IconTitle (@ICON_TITLE)
	{
	    &cgiprint'Cache( "<li>", &TagMsgImg( &GetIconUrlFromTitle( $IconTitle, $BOARD ), $IconTitle ), " : ", ( $ICON_HELP{$IconTitle} || $IconTitle ), "\n" );
	}
	&cgiprint'Cache("</ul>\n");
    }
    &MsgFooter;
}

1;
