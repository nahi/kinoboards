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
ShowIcon: {

    local($IconTitle, $Type);

    # タイプを拾う
    $Type = $cgi'TAGS{'type'};

    # 表示画面の作成
    &MsgHeader('Icon show', "$BOARDNAME: アイコンの説明");

    if ($Type eq 'article') {

	&cgiprint'Cache(<<__EOF__);
<p>
各アイコンは次の機能を表しています．
</p>
<ul>
<p>
<li>$H_THREAD : ($H_SUBJECT一覧で)その$H_MESGの$H_REPLYをまとめて読む
</p><p>
<li><img src="$ICON_BLIST" alt="$H_BACKBOARD" height="$COMICON_HEIGHT" width="$COMICON_WIDTH"> : $H_BACKBOARD
<li><img src="$ICON_TLIST" alt="$H_BACKTITLE" height="$COMICON_HEIGHT" width="$COMICON_WIDTH"> : $H_BACKTITLE
<li><img src="$ICON_PREV" alt="$H_PREVARTICLE" height="$COMICON_HEIGHT" width="$COMICON_WIDTH"> : $H_PREVARTICLE
<li><img src="$ICON_NEXT" alt="$H_NEXTARTICLE" height="$COMICON_HEIGHT" width="$COMICON_WIDTH"> : $H_NEXTARTICLE
<li><img src="$ICON_THREAD" alt="$H_READREPLYALL" height="$COMICON_HEIGHT" width="$COMICON_WIDTH"> : $H_READREPLYALL
</p><p>
<li><img src="$ICON_WRITENEW" alt="$H_POSTNEWARTICLE" height="$COMICON_HEIGHT" width="$COMICON_WIDTH"> : $H_POSTNEWARTICLE
<li><img src="$ICON_FOLLOW" alt="$H_REPLYTHISARTICLE" height="$COMICON_HEIGHT" width="$COMICON_WIDTH"> : $H_REPLYTHISARTICLE
<li><img src="$ICON_QUOTE" alt="$H_REPLYTHISARTICLEQUOTE" height="$COMICON_HEIGHT" width="$COMICON_WIDTH"> : $H_REPLYTHISARTICLEQUOTE
</p>
</ul>
__EOF__

    } else {

	&CashIconDb($BOARD);	# アイコンDBのキャッシュ

	&cgiprint'Cache(<<__EOF__);
<p>
$H_BOARD「$BOARDNAME」では，次のアイコンを使うことができます．
</p><p>
<ul>
__EOF__
	foreach $IconTitle (@ICON_TITLE) {
	    &cgiprint'Cache(sprintf("<li><img src=\"%s\" alt=\"$IconTitle\" height=\"$MSGICON_HEIGHT\" width=\"$MSGICON_WIDTH\"> : %s\n", &GetIconUrlFromTitle($IconTitle, $BOARD), ($ICON_HELP{$IconTitle} || $IconTitle)));
	}
	&cgiprint'Cache("</ul>\n</p>\n");

    }

    &MsgFooter;

}

1;
