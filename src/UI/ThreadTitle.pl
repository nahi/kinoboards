###
## ThreadTitle - スレッド別タイトル一覧
#
# - SYNOPSIS
#	ThreadTitle($ComType);
#
# - ARGS
#	$ComType	表示画面のタイプ
#				0 ... 記事参照画面
#				2 ... リンクかけかえ先指定画面
#				3 ... リンクかけかえ実施
#				4 ... 移動先指定画面
#				5 ... 移動実施
#
# - DESCRIPTION
#	新しい記事のタイトルをスレッド別にソートして表示．
#	大域変数である，CGI変数を参照する．
#	大域変数ADDFLAG(既に表示してしまったか否かを表わすフラグ)を破壊する．
#
# - RETURN
#	なし
#
ThreadTitle:
{
    local( $ComType ) = $gVarComType;
    local( $IdNum, $Id, $Fid, $IdNum, $Id );
    local( $vCom, $vStr );

    if ( $ComType == 0 )
    {
	$vCom = 'v';
	$vStr = '';
    }
    elsif ( $ComType == 2 )
    {
	$vCom = 'ct';
	$vStr = "&rtid=" . $cgi'TAGS{'roid'} . "&rfid=" . $cgi'TAGS{'rfid'} . "&rtid=" . $cgi'TAGS{'rtid'};
    }
    elsif ( $ComType == 3 )
    {
	$vCom = 'v';
	$vStr = '';
    }
    elsif ( $ComType == 4 )
    {
	$vCom = 'mvt';
	$vStr = "&rtid=" . $cgi'TAGS{'roid'} . "&rfid=" . $cgi'TAGS{'rfid'} . "&rtid=" . $cgi'TAGS{'rtid'};
    }
    elsif ( $ComType == 5 )
    {
	$vCom = 'v';
	$vStr = '';
    }

    %ADDFLAG = ();		# it's static.

    &LockBoard();
    &DbCache( $BOARD ) if $BOARD;

    if ($ComType == 3)
    {
	# リンクかけかえの実施
	&ReLinkExec($cgi'TAGS{'rfid'}, $cgi'TAGS{'rtid'}, $BOARD);
    }
    elsif ($ComType == 5)
    {
	# 移動の実施
	&ReOrderExec($cgi'TAGS{'rfid'}, $cgi'TAGS{'rtid'}, $BOARD);
    }

    &UnlockBoard();

    # 表示する個数を取得
    local( $Num ) = $cgi'TAGS{'num'};
    local( $Old );
    if ( defined( $cgi'TAGS{'id'} ))
    {
	$Old = $#DB_ID - int( $cgi'TAGS{'id'} + $Num/2 );
	$Old = 0 if ( $Old < 0 );
    }
    else
    {
	$Old = $cgi'TAGS{'old'};
    }
    local( $Rev ) = $cgi'TAGS{'rev'};
    local( $vRev ) = $Rev? 1-$SYS_BOTTOMTITLE : $SYS_BOTTOMTITLE;
    local( $To ) = $#DB_ID - $Old;
    local( $From )= $To - $Num + 1;
    $From = 0 if (( $From < 0 ) || ( $Num == 0 ));

    local( $pageLinkStr ) = &PageLink( "$vCom$vStr", $Num, $Old, $Rev );

    # 整形済みフラグ
    # 0 ... 整形対象外
    # 1 ... 整形済み
    # 2 ... 未整形
    local( $IdNum, $Id );
    for ( $IdNum = $From; $IdNum <= $To; $IdNum++ )
    {
	$ADDFLAG{$DB_ID[$IdNum]} = 2;
    }

    # 表示画面の作成
    if ($ComType == 2)
    {
	&MsgHeader( 'Thread view', '新たなリプライ先の指定' );
    }
    elsif ($ComType == 3)
    {
	&MsgHeader( 'Thread view', "指定された$H_MESGのリプライ先を変更しました" );
    }
    elsif ($ComType == 4)
    {
	&MsgHeader( 'Thread view', '移動先の指定' );
    }
    elsif ($ComType == 5)
    {
	&MsgHeader( 'Thread view', "指定された$H_MESGを移動しました");
    }
    else
    {
	&MsgHeader( 'Thread view', "$H_SUBJECT一覧($H_REPLY順)" );
    }

    &BoardHeader();

    if ( $SYS_F_MT )
    {
	if ($ComType == 3)
	{
	    &cgiprint'Cache("<ul>\n<li>", &TagA( "$PROGRAM?b=$BOARD&c=ce&rtid=" . $cgi'TAGS{'roid'} . "&rfid=" . $cgi'TAGS{'rfid'}, "今の変更を元に戻す" ), "\n</ul>\n");
	}

	&cgiprint'Cache(<<__EOF__);
<p>
各$H_ICONは，次のような意味を表しています．
</p>

<ul>
<li>$H_RELINKFROM_MARK:
この$H_MESGの$H_REPLY先を変更します．$H_REPLY先を指定する画面に飛びます．
<li>$H_REORDERFROM_MARK:
この$H_MESGの順序を変更します．移動先を指定する画面に飛びます．
<li>$H_DELETE_ICON:
この$H_MESGを削除します．
<li>$H_SUPERSEDE_ICON:
この$H_MESGを訂正します．
<li>$H_RELINKTO_MARK:
先に指定した$H_MESGの$H_REPLY先を，この$H_MESGにします．
<li>$H_REORDERTO_MARK:
先に指定した$H_MESGを，この$H_MESGの下に移動します．
</ul>
__EOF__

	if ($ComType == 2)
	{
	    &cgiprint'Cache("<p>", $cgi'TAGS{'rfid'}, "を，どの$H_MESGへのリプライにしますか? リプライ先の$H_MESGの$H_RELINKTO_MARKをクリックしてください．</p>\n");
	}
	elsif ($ComType == 4)
	{
	    &cgiprint'Cache("<p>", $cgi'TAGS{'rfid'}, "を，どの$H_MESGの下に移動しますか? $H_MESGの$H_REORDERTO_MARKをクリックしてください．</p>\n");
	}
    }

    &cgiprint'Cache("$H_HR\n");

    &cgiprint'Cache( $pageLinkStr );

    local( $AddNum ) = "&num=$Num&old=$Old&rev=$Rev";

    if ($To < $From)
    {
	# 空だった……
	&cgiprint'Cache("<ul>\n<li>$H_NOARTICLE\n</ul>\n");
    }
    elsif ( $vRev )
    {
	# 古いのから処理
	if (($ComType == 2) && ($DB_FID{$cgi'TAGS{'rfid'}} ne ''))
	{
	    &cgiprint'Cache( "<ul>\n<li>", &TagA( "$PROGRAM?b=$BOARD&c=ce&rtid=&rfid=" . $cgi'TAGS{'rfid'} . "&roid=" . $cgi'TAGS{'roid'} . $AddNum, "[どの$H_MESGへのリプライでもなく，新着$H_MESGにする]" ), "\n</ul>\n" );
	}
	elsif ($ComType == 4)
	{
	    &cgiprint'Cache( "<ul>\n<li>", &TagA( "$PROGRAM?b=$BOARD&c=mve&rtid=&rfid=" . $cgi'TAGS{'rfid'} . "&roid=" . $cgi'TAGS{'roid'} . $AddNum, "[全記事の先頭に移動する(このページの先頭，ではありません)]" ), "\n</ul>\n" );
	}

	for( $IdNum = $From; $IdNum <= $To; $IdNum++ )
	{
	    # 該当記事のIDを取り出す
	    $Id = $DB_ID[$IdNum];
	    ( $Fid = $DB_FID{ $Id } ) =~ s/,.*$//o;
	    # 後方参照は後回し．
#	    next if ((( $Fid ne '' ) && ( $SYS_THREAD_FORMAT == 2 )) || ( $ADDFLAG{$Fid} == 2 ));
	    next if (( $Fid ne '' ) && (( $ADDFLAG{$Fid} == 2 ) || ( $SYS_THREAD_FORMAT == 2 )));

	    # ノードを表示
	    &cgiprint'Cache( "<ul>\n" );
	    if ( $SYS_F_MT )
	    {
		&ThreadTitleNodeMaint( $Id, $ComType, $AddNum, 1 );
	    }
	    else
	    {
		if ( $SYS_THREAD_FORMAT == 1 )
		{
		    &ThreadTitleNodeAllThread( $Id, 1 );
		}
		elsif ( $SYS_THREAD_FORMAT == 2 )
		{
		    &ThreadTitleNodeNoThread( $Id, 1 );
		}
		else
		{
		    &ThreadTitleNodeThread( $Id, 1 );
		}
	    }
	    &cgiprint'Cache( "</ul>\n" );
	}
    }
    else
    {
	# 新しいのから処理
	if (($ComType == 2) && ($DB_FID{$cgi'TAGS{'rfid'}} ne ''))
	{
	    &cgiprint'Cache("<li>", &TagA( "$PROGRAM?b=$BOARD&c=ce&rtid=&rfid=" . $cgi'TAGS{'rfid'} . "&roid=" . $cgi'TAGS{'roid'} . $AddNum, "[どの$H_MESGへのリプライでもなく，新着$H_MESGにする]" ), "\n");
	}
	elsif ($ComType == 4)
	{
	    &cgiprint'Cache("<li>", &TagA( "$PROGRAM?b=$BOARD&c=mve&rtid=&rfid=" . $cgi'TAGS{'rfid'} . "&roid=" . $cgi'TAGS{'roid'} . $AddNum, "[全記事の先頭に移動する(このページの先頭，ではありません)]" ), "\n");
	}

	for( $IdNum = $To; $IdNum >= $From; $IdNum-- )
	{
	    # 後は同じ
	    $Id = $DB_ID[$IdNum];
	    ( $Fid = $DB_FID{ $Id } ) =~ s/,.*$//o;
#	    next if ((( $Fid ne '' ) && ( $SYS_THREAD_FORMAT == 2 )) || ( $ADDFLAG{$Fid} == 2 ));
	    next if (( $Fid ne '' ) && (( $ADDFLAG{$Fid} == 2 ) || ( $SYS_THREAD_FORMAT == 2 )));

	    &cgiprint'Cache( "<ul>\n" );
	    if ( $SYS_F_MT )
	    {
		&ThreadTitleNodeMaint( $Id, $ComType, $AddNum, 1 );
	    }
	    else
	    {
		if ( $SYS_THREAD_FORMAT == 1 )
		{
		    &ThreadTitleNodeAllThread( $Id, 1 );
		}
		elsif ( $SYS_THREAD_FORMAT == 2 )
		{
		    &ThreadTitleNodeNoThread( $Id, 1 );
		}
		else
		{
		    &ThreadTitleNodeThread( $Id, 1 );
		}
	    }
	    &cgiprint'Cache( "</ul>\n" );
	}
    }

    &cgiprint'Cache( $pageLinkStr );

    &MsgFooter;

    undef(%ADDFLAG);

}


###
## 新着ノードのみ表示
#
sub ThreadTitleNodeNoThread
{
    local( $Id ) = @_;

    &cgiprint'Cache( '<li>', &GetFormattedTitle( $Id, $DB_AIDS{$Id}, $DB_ICON{$Id}, $DB_TITLE{$Id}, $DB_NAME{$Id}, $DB_DATE{$Id}, 1 ), "\n");
}


###
## ページ内スレッドのみ表示
#
sub ThreadTitleNodeThread
{
    local( $Id, $top ) = @_;

    # ページ外ならおしまい．
    return if ( $ADDFLAG{$Id} != 2 );

    &cgiprint'Cache( '<li>', &GetFormattedTitle($Id, $DB_AIDS{$Id}, $DB_ICON{$Id}, $DB_TITLE{$Id}, $DB_NAME{$Id}, $DB_DATE{$Id}, $top ), "\n" );

    $ADDFLAG{$Id} = 1;		# 整形済み

    # 娘が居れば……
    if ( $DB_AIDS{$Id} )
    {
	&cgiprint'Cache( "<ul>\n" );
	grep( &ThreadTitleNodeThread( $_, 0 ), split( /,/, $DB_AIDS{$Id} ));
	&cgiprint'Cache( "</ul>\n" );
    }
}


###
## 全スレッドの表示
#
sub ThreadTitleNodeAllThread
{
    local( $Id, $top ) = @_;

    # 表示済みならおしまい．
    return if ( $ADDFLAG{$Id} == 1 );

    &cgiprint'Cache( '<li>', &GetFormattedTitle($Id, $DB_AIDS{$Id}, $DB_ICON{$Id}, $DB_TITLE{$Id}, $DB_NAME{$Id}, $DB_DATE{$Id}, $top ), "\n" );
    $ADDFLAG{$Id} = 1;		# 整形済み

    # 娘が居れば……
    if ( $DB_AIDS{$Id} )
    {
	&cgiprint'Cache( "<ul>\n" );
	grep( &ThreadTitleNodeAllThread( $_, 0 ), split( /,/, $DB_AIDS{$Id} ));
	&cgiprint'Cache( "</ul>\n" );
    }
}


###
## 管理者用のスレッド表示
#
sub ThreadTitleNodeMaint
{
    local( $Id, $ComType, $AddNum, $top ) = @_;

    return if ( $ADDFLAG{$Id} != 2 );

    local($FromId) = $cgi'TAGS{'rfid'};

    &cgiprint'Cache( '<li>', &GetFormattedTitle($Id, $DB_AIDS{$Id}, $DB_ICON{$Id}, $DB_TITLE{$Id}, $DB_NAME{$Id}, $DB_DATE{$Id}, $top ));

    &cgiprint'Cache(" .......... \n");

    # リンク先変更コマンド(From)
    # 移動コマンド(From)
    if ($SYS_F_MV)
    {
	&cgiprint'Cache( &TagA( "$PROGRAM?b=$BOARD&c=ct&rfid=$Id&roid=" . $DB_FID{$Id} . $AddNum, $H_RELINKFROM_MARK ), "\n");
	if ($DB_FID{$Id} eq '')
	{
	    &cgiprint'Cache( &TagA( "$PROGRAM?b=$BOARD&c=mvt&rfid=$Id&roid=" . $DB_FID{$Id} . $AddNum, $H_REORDERFROM_MARK ), "\n");
	}
    }

    # 削除コマンド
    if ($SYS_F_D)
    {
	&cgiprint'Cache( &TagA( "$PROGRAM?b=$BOARD&c=dp&id=$Id", $H_DELETE_ICON ), "\n" );
	&cgiprint'Cache( &TagA( "$PROGRAM?b=$BOARD&c=f&s=on&id=$Id", $H_SUPERSEDE_ICON ), "\n" );
    }

    # 移動コマンド(To)
    if ($SYS_F_MV && ($ComType == 4) && ($FromId ne $Id) && ($DB_FID{$Id} eq '') && ($FromId ne $Id))
    {
	&cgiprint'Cache( &TagA( "$PROGRAM?b=$BOARD&c=mve&rtid=$Id&rfid=$FromId&roid=" . $cgi'TAGS{'roid'} . $AddNum, $H_REORDERTO_MARK ), "\n" );
    }

    # リンク先変更コマンド(To)
    if ($SYS_F_MV && ($ComType == 2) && ($FromId ne $Id) && (! grep(/^$FromId$/, split(/,/, $DB_AIDS{$Id}))) && (! grep(/^$FromId$/, split(/,/, $DB_FID{$Id}))))
    {
	&cgiprint'Cache( &TagA( "$PROGRAM?b=$BOARD&c=ce&rtid=$Id&rfid=$FromId&roid=" . $cgi'TAGS{'roid'} . $AddNum, $H_RELINKTO_MARK ), "\n" );
    }

    $ADDFLAG{$Id} = 1;		# 整形済み

    # 娘が居れば……
    if ($DB_AIDS{$Id})
    {
	&cgiprint'Cache("<ul>\n");
	grep( &ThreadTitleNodeMaint( $_, $ComType, $AddNum, 0 ),
	     split( /,/, $DB_AIDS{$Id} ));
	&cgiprint'Cache("</ul>\n");
    }
}

1;
