###
## ViewTitle - スレッド別表示
#
# - SYNOPSIS
#	ViewTitle($ComType);
#
# - ARGS
#	$ComType	表示画面のタイプ
#				0 ... 記事参照画面
#				1 ... 記事管理画面
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
ViewTitle: {
    local($ComType) = $gVarComType;
    local($Num, $Old, $NextOld, $BackOld, $To, $From, $IdNum, $Id, $Fid, $IdNum, $Id, $AddNum);
    local( $vCom, $vStr );

    if ( $ComType == 0 ) {
	$vCom = 'v';
	$vStr = '';
    }
    elsif ( $ComType == 1 ) {
	$vCom = 'vm';
	$vStr = '';
    }
    elsif ( $ComType == 2 ) {
	$vCom = 'ct';
	$vStr = "&rtid=" . $cgi'TAGS{'roid'} . "&rfid=" . $cgi'TAGS{'rfid'} . "&rtid=" . $cgi'TAGS{'rtid'};
    }
    elsif ( $ComType == 3 ) {
	$vCom = 'vm';
	$vStr = '';
    }
    elsif ( $ComType == 4 ) {
	$vCom = 'mvt';
	$vStr = "&rtid=" . $cgi'TAGS{'roid'} . "&rfid=" . $cgi'TAGS{'rfid'} . "&rtid=" . $cgi'TAGS{'rtid'};
    }
    elsif ( $ComType == 5 ) {
	$vCom = 'vm';
	$vStr = '';
    }

    %ADDFLAG = ();		# it's static.

    # lock system
    local( $lockResult ) = &cgi'lock( $LOCK_FILE ) unless $PC;
    &Fatal(1001, '') if ( $lockResult == 2 );
    &Fatal(999, '') if ( $lockResult != 1 );
    # cash article DB
    if ( $BOARD ) { &DbCash( $BOARD ); }

    if ($ComType == 3) {
	# リンクかけかえの実施
	&ReLinkExec($cgi'TAGS{'rfid'}, $cgi'TAGS{'rtid'}, $BOARD);
    } elsif ($ComType == 5) {
	# 移動の実施
	&ReOrderExec($cgi'TAGS{'rfid'}, $cgi'TAGS{'rtid'}, $BOARD);
    }

    # unlock system
    &cgi'unlock( $LOCK_FILE ) unless $PC;

    # 表示する個数を取得
    $Num = $cgi'TAGS{'num'};
    $Old = $cgi'TAGS{'old'};
    $NextOld = ($Old > $Num) ? ($Old - $Num) : 0;
    $BackOld = ($Old + $Num);
    $To = $#DB_ID - $Old;
    $From = $To - $Num + 1; $From = 0 if (($From < 0) || ($Num == 0));

    # 整形済みフラグ
    # 0 ... 整形対象外
    # 1 ... 整形済み
    # 2 ... 未整形
    for($IdNum = $From; $IdNum <= $To; $IdNum++) { $ADDFLAG{$DB_ID[$IdNum]} = 2; }

    # ページング用文字列
    $AddNum = "&num=" . $cgi'TAGS{'num'} . "&old=" . $cgi'TAGS{'old'};

    # 表示画面の作成
    if ($ComType == 2) {
	&MsgHeader('Title view (threaded)', "新たなリプライ先の指定");
    } elsif ($ComType == 3) {
	&MsgHeader('Title view (threaded)', "指定された$H_MESGのリプライ先を変更しました");
    } elsif ($ComType == 4) {
	&MsgHeader('Title view (threaded)', "移動先の指定");
    } elsif ($ComType == 5) {
	&MsgHeader('Title view (threaded)', "指定された$H_MESGを移動しました");
    } else {
	&MsgHeader('Title view (threaded)', "$H_SUBJECT一覧($H_REPLY順)");
    }

    if ($ComType == 0) {

	&BoardHeader('normal');

    } else {

	&BoardHeader('maint');

	if ($ComType == 3) {
	    &cgiprint'Cache("<p>\n<ul>\n<li>" . &TagA( "$PROGRAM?b=$BOARD&c=ce&rtid=" . $cgi'TAGS{'roid'} . "&rfid=" . $cgi'TAGS{'rfid'}, "今の変更を元に戻す" ) . "\n</ul>\n</p>");
	}

	&cgiprint'Cache(<<__EOF__);
<p>各アイコンは，次のような意味を表しています．
<dl compact>
<dt>$H_RELINKFROM_MARK
<dd>この$H_MESGの$H_REPLY先を変更します．$H_REPLY先を指定する画面に飛びます．
<dt>$H_REORDERFROM_MARK
<dd>この$H_MESGの順序を変更します．移動先を指定する画面に飛びます．
<dt>$H_DELETE_ICON
<dd>この$H_MESGを削除します．
<dt>$H_SUPERSEDE_ICON
<dd>この$H_MESGを訂正します．
<dt>$H_RELINKTO_MARK
<dd>先に指定した$H_MESGの$H_REPLY先を，この$H_MESGにします．
<dt>$H_REORDERTO_MARK
<dd>先に指定した$H_MESGを，この$H_MESGの下に移動します．
</dl></p>
__EOF__

	if ($ComType == 2) {
	    &cgiprint'Cache("<p>" . $cgi'TAGS{'rfid'} . "を，どの$H_MESGへのリプライにしますか? リプライ先の$H_MESGの$H_RELINKTO_MARKをクリックしてください．</p>\n");
	} elsif ($ComType == 4) {
	    &cgiprint'Cache("<p>" . $cgi'TAGS{'rfid'} . "を，どの$H_MESGの下に移動しますか? $H_MESGの$H_REORDERTO_MARKをクリックしてください．</p>\n");
	}

    }

    &cgiprint'Cache("<hr>\n");

    if ($SYS_BOTTOMTITLE) {
	&cgiprint'Cache("<p>$H_TOP" . &TagA( "$PROGRAM?b=$BOARD&c=$vCom$vStr&num=$Num&old=$BackOld", $H_BACKART ) . "</p>\n") if ($From > 0);
    } else {
	&cgiprint'Cache("<p>$H_TOP" . &TagA( "$PROGRAM?b=$BOARD&c=$vCom$vStr&num=$Num&old=$NextOld", $H_NEXTART ) . "</p>\n") if ($Old);
    }

    &cgiprint'Cache("<p><ul>\n");

    if ($To < $From) {

	# 空だった……
	&cgiprint'Cache("<li>$H_NOARTICLE\n");

    } elsif ($SYS_BOTTOMTITLE) {

	# 古いのから処理
	if (($ComType == 2) && ($DB_FID{$cgi'TAGS{'rfid'}} ne '')) {
	    &cgiprint'Cache("<li>" . &TagA( "$PROGRAM?b=$BOARD&c=ce&rtid=&rfid=" . $cgi'TAGS{'rfid'} . "&roid=" . $cgi'TAGS{'roid'} . $AddNum, "[どの$H_MESGへのリプライでもなく，新着$H_MESGにする]" ) . "\n");
	} elsif ($ComType == 4) {
	    &cgiprint'Cache("<li>" . &TagA( "$PROGRAM?b=$BOARD&c=mve&rtid=&rfid=" . $cgi'TAGS{'rfid'} . "&roid=" . $cgi'TAGS{'roid'} . $AddNum, "[全記事の先頭に移動する(このページの先頭，ではありません)]" ) . "\n");
	}

	for($IdNum = $From; $IdNum <= $To; $IdNum++) {

	    # 該当記事のIDを取り出す
	    $Id = $DB_ID[$IdNum];
	    ($Fid = $DB_FID{$Id}) =~ s/,.*$//o;
	    # 後方参照は後回し．
	    next if (($Fid ne '') && ($ADDFLAG{$Fid} == 2));
	    # ノードを表示
	    if ($ComType == 0) {
		&ViewTitleNode($Id);
	    } else {
		&ViewTitleNodeMaint($Id, $ComType, $AddNum);
	    }
	}
    } else {

	# 新しいのから処理
	if (($ComType == 2) && ($DB_FID{$cgi'TAGS{'rfid'}} ne '')) {
	    &cgiprint'Cache("<li>" . &TagA( "$PROGRAM?b=$BOARD&c=ce&rtid=&rfid=" . $cgi'TAGS{'rfid'} . "&roid=" . $cgi'TAGS{'roid'} . $AddNum, "[どの$H_MESGへのリプライでもなく，新着$H_MESGにする]" ) . "\n");
	} elsif ($ComType == 4) {
	    &cgiprint'Cache("<li>" . &TagA( "$PROGRAM?b=$BOARD&c=mve&rtid=&rfid=" . $cgi'TAGS{'rfid'} . "&roid=" . $cgi'TAGS{'roid'} . $AddNum, "[全記事の先頭に移動する(このページの先頭，ではありません)]" ) . "\n");
	}

	for($IdNum = $To; $IdNum >= $From; $IdNum--) {
	    # 後は同じ
	    $Id = $DB_ID[$IdNum];
	    ($Fid = $DB_FID{$Id}) =~ s/,.*$//o;
	    next if (($Fid ne '') && ($ADDFLAG{$Fid} == 2));
	    if ($ComType == 0) {
		&ViewTitleNode($Id);
	    } else {
		&ViewTitleNodeMaint($Id, $ComType, $AddNum);
	    }
	}
    }

    &cgiprint'Cache("</ul></p>\n");

    if ($SYS_BOTTOMTITLE) {
	&cgiprint'Cache("<p>$H_BOTTOM" . &TagA( "$PROGRAM?b=$BOARD&c=$vCom$vStr&num=$Num&old=$NextOld", $H_NEXTART ) . "</p>\n") if ($Old);
    } else {
	&cgiprint'Cache("<p>$H_BOTTOM" . &TagA( "$PROGRAM?b=$BOARD&c=$vCom$vStr&num=$Num&old=$BackOld", $H_BACKART ) . "</p>\n") if ($From > 0);
    }

    &MsgFooter;

    undef(%ADDFLAG);

}

sub ViewTitleNode {
    local($Id) = @_;

    if ($ADDFLAG{$Id} != 2) { return; }

    &cgiprint'Cache("<li>" . &GetFormattedTitle($Id, $BOARD, $DB_AIDS{$Id}, $DB_ICON{$Id}, $DB_TITLE{$Id}, $DB_NAME{$Id}, $DB_DATE{$Id}) . "\n");
    $ADDFLAG{$Id} = 1;		# 整形済み

    # 娘が居れば……
    if ($DB_AIDS{$Id}) {
	&cgiprint'Cache("<ul>\n");
	foreach (split(/,/, $DB_AIDS{$Id})) { &ViewTitleNode($_); }
	&cgiprint'Cache("</ul>\n");
    }
}

sub ViewTitleNodeMaint {

    local($Id, $ComType, $AddNum) = @_;

    return if ($ADDFLAG{$Id} != 2);

    local($FromId) = $cgi'TAGS{'rfid'};

    &cgiprint'Cache("<li>" . &GetFormattedTitle($Id, $BOARD, $DB_AIDS{$Id}, $DB_ICON{$Id}, $DB_TITLE{$Id}, $DB_NAME{$Id}, $DB_DATE{$Id})); #'

    &cgiprint'Cache(" .......... \n");

    # リンク先変更コマンド(From)
    # 移動コマンド(From)
    if ($SYS_F_MV) {
	&cgiprint'Cache( &TagA( "$PROGRAM?b=$BOARD&c=ct&rfid=$Id&roid=" . $DB_FID{$Id} . $AddNum, $H_RELINKFROM_MARK ) . "\n");
	if ($DB_FID{$Id} eq '') {
	    &cgiprint'Cache( &TagA( "$PROGRAM?b=$BOARD&c=mvt&rfid=$Id&roid=" . $DB_FID{$Id} . $AddNum, $H_REORDERFROM_MARK ) . "\n");
	}
    }

    # 削除コマンド
    if ($SYS_F_D) {
	&cgiprint'Cache( &TagA( "$PROGRAM?b=$BOARD&c=dp&id=$Id", $H_DELETE_ICON ) . "\n" );
	&cgiprint'Cache( &TagA( "$PROGRAM?b=$BOARD&c=f&s=on&id=$Id", $H_SUPERSEDE_ICON ) . "\n" );
__EOF__
    }

    # 移動コマンド(To)
    if ($SYS_F_MV && ($ComType == 4) && ($FromId ne $Id) && ($DB_FID{$Id} eq '') && ($FromId ne $Id)) {
	&cgiprint'Cache( &TagA( "$PROGRAM?b=$BOARD&c=mve&rtid=$Id&rfid=$FromId&roid=" . $cgi'TAGS{'roid'} . $AddNum, $H_REORDERTO_MARK ) . "\n" );
    }

    # リンク先変更コマンド(To)
    if ($SYS_F_MV && ($ComType == 2) && ($FromId ne $Id) && (! grep(/^$FromId$/, split(/,/, $DB_AIDS{$Id}))) && (! grep(/^$FromId$/, split(/,/, $DB_FID{$Id})))) {
	&cgiprint'Cache( &TagA( "$PROGRAM?b=$BOARD&c=ce&rtid=$Id&rfid=$FromId&roid=" . $cgi'TAGS{'roid'} . $AddNum, $H_RELINKTO_MARK ) . "\n" );
    }

    $ADDFLAG{$Id} = 1;		# 整形済み

    # 娘が居れば……
    if ($DB_AIDS{$Id}) {
	&cgiprint'Cache("<ul>\n");
	foreach (split(/,/, $DB_AIDS{$Id})) { &ViewTitleNodeMaint($_, $ComType, $AddNum); }
	&cgiprint'Cache("</ul>\n");
    }
}

1;
