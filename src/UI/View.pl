# 現在は使われていない．

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
    local( $comType ) = $gVarComType;
    local( $key, $value, $indent, $head, %boardList, %boardInfo, @boards, $modTime, $numOfArticle );

    # lock system
    local( $lockResult ) = $PC ? 1 : &cgi'lock( $LOCK_FILE );
    &Fatal(1001, '') if ( $lockResult == 2 );
    &Fatal(999, '') if ( $lockResult != 1 );
    # cash board DB
    &GetAllBoardInfo( *boardList, *boardInfo );
    # cash article DB
    if ( $BOARD ) { &DbCash( $BOARD ); }

    if ( $comType == 3 ) {
	# リンクかけかえの実施
	&ReLinkExec( $cgi'TAGS{'rfid'}, $cgi'TAGS{'rtid'}, $BOARD );
    } elsif ( $comType == 5 ) {
	# 移動の実施
	&ReOrderExec( $cgi'TAGS{'rfid'}, $cgi'TAGS{'rtid'}, $BOARD );
    }

    # unlock system
    &cgi'unlock( $LOCK_FILE ) unless $PC;

    # 表示画面の作成
    &MsgHeader( 'Tree view', 'Tree View' );

    if ( $comType != 0 ) {

	if ( $comType == 3 ) {
	    &cgiprint'Cache( "<p>\n<ul>\n<li>" . &TagA( "$PROGRAM?b=$BOARD&c=ce&rtid=" . $cgi'TAGS{'roid'} . "&rfid=" . $cgi'TAGS{'rfid'}, "今の変更を元に戻す" ) . "\n</ul>\n</p>" );
	} elsif ( $comType == 2 ) {
	    &cgiprint'Cache( "<p>" . $cgi'TAGS{'rfid'} . "を，どの$H_MESGへのリプライにしますか? リプライ先の$H_MESGの$H_RELINKTO_MARKをクリックしてください．</p>\n" );
	} elsif ( $comType == 4 ) {
	    &cgiprint'Cache( "<p>" . $cgi'TAGS{'rfid'} . "を，どの$H_MESGの下に移動しますか? $H_MESGの$H_REORDERTO_MARKをクリックしてください．</p>\n" );
	}

    }

    &cgiprint'Cache( "<p><pre>\n" );
    &cgiprint'Cache( &TagA( $BOARDLIST_URL, $SYSTEM_NAME ) . "\n" );

    $indent = '';
    $head = " +" . "-" x $TREE_INDENT;

    @boards = keys( %boardList );
    while( $key = pop( @boards )) {
	$modTime = &GetDateTimeFormatFromUtc( &GetModifiedTime( $DB_FILE_NAME, $key ));
	$numOfArticle = &GetArticleId( $key ) || 0;
	&cgiprint'Cache( $indent . $head . &TagA( "$PROGRAM?b=$key&c=v&num=$DEF_TITLE_NUM", $boardList{ $key } ));
	if ( $comType == 0 ) {
	    &cgiprint'Cache( " → " . &TagA( "$PROGRAM?b=$key&c=vm&num=$DEF_TITLE_NUM", "管理画面の表示" ));
	}
	
	&cgiprint'Cache( " [ #$numOfArticle, $modTime ]\n" );
	    
	if ( $key eq $BOARD ) {
	    &ViewBoard( $comType, $indent . " |" . " " x $TREE_INDENT );
	}
    }

    &cgiprint'Cache( "</pre></p>\n" );

    &MsgFooter;

}

sub ViewBoard {
    local( $comType , $indent ) = @_;
    local( $num, $old, $nextOld, $backOld, $to, $from, $idNum, $id, $fId, $addNum, $head, @headId );

    %ADDFLAG = ();		# it's static.

    # 表示する個数を取得
    $num = $cgi'TAGS{'num'};
    $old = $cgi'TAGS{'old'};
    $nextOld = ( $old > $num ) ? ( $old - $num ) : 0;
    $backOld = ( $old + $num );
    $to = $#DB_ID - $old;
    $from = $to - $num + 1;
    $from = 0 if (( $from < 0 ) || ( $num == 0 ));

    # 整形済みフラグ
    # 0 ... 整形対象外
    # 1 ... 整形済み
    # 2 ... 未整形
    for( $idNum = $from; $idNum <= $to; $idNum++) {
	$ADDFLAG{ $DB_ID[$idNum]} = 2;
    }

    # it's for middle menu
    $head = " +" . "-" x $TREE_INDENT;

    if ($SYS_BOTTOMTITLE) {
	&cgiprint'Cache("<p>$H_TOP" . &TagA( "$PROGRAM?b=$BOARD&c=v&num=$num&old=$backOld", $H_BACKART ) . "</p>\n") if ( $from > 0 );
    } else {
	&cgiprint'Cache("<p>$H_TOP" . &TagA( "$PROGRAM?b=$BOARD&c=v&num=$num&old=$nextOld", $H_NEXTART ) . "</p>\n") if ($old);
    }

    if ( $comType == 0 ) {
	if ( $SYS_ALIAS != 0 ) {
	    &cgiprint'Cache( $indent . $head . &TagA( "$PROGRAM?c=as", "[ユーザ]" ));
	    &cgiprint'Cache( " → " . &TagA( "$PROGRAM?c=an", "新規登録と変更" ) . "\n" );
	}

	&cgiprint'Cache( $indent . $head . &TagA( "$PROGRAM?b=$BOARD&c=i", "[$H_ICON]" ) . "\n" );
    }

    # it's last menu.
    $head = " `" . "-" x $TREE_INDENT;

    &cgiprint'Cache( $indent . $head . &TagA( "$PROGRAM?b=$BOARD&c=l&num=$num&old=$nextOld", "[$H_MESG]" ));

    &cgiprint'Cache( " → " . &TagA( "$PROGRAM?b=$BOARD&c=s", "検索" ));

    if ( $comType == 0 ) {
	&cgiprint'Cache( "/$H_REPLY順表示/" . &TagA( "$PROGRAM?b=$BOARD&c=r&num=$num&old=$nextOld", "日付順表示" ));
    }

    &cgiprint'Cache( "\n" );

    $indent .= " " x ( $TREE_INDENT + 2 );
    $head = " +" . "-" x $TREE_INDENT;

    if ( $comType == 0 ) {
	&cgiprint'Cache( $indent . $head . &TagA( "$PROGRAM?b=$BOARD&c=n", "[新規$H_MESG]" ) . "\n" );
    }

    # ページング用文字列
    $addNum = "&num=$num&old=$old";

    if ($SYS_BOTTOMTITLE) {

	if (( $comType == 2 ) && ($DB_FID{$cgi'TAGS{'rfid'}} ne '')) {
	    &cgiprint'Cache( $indent . $head . &TagA( "$PROGRAM?b=$BOARD&c=ce&rtid=&rfid=" . $cgi'TAGS{'rfid'} . "&roid=" . $cgi'TAGS{'roid'} . $addNum, "[どの$H_MESGへのリプライでもなく，新着$H_MESGにする]" ) . "\n" );
	} elsif ( $comType == 4 ) {
	    &cgiprint'Cache( $indent . $head . &TagA( "$PROGRAM?b=$BOARD&c=mve&rtid=&rfid=" . $cgi'TAGS{'rfid'} . "&roid=" . $cgi'TAGS{'roid'} . $addNum, "[全記事の先頭に移動する(このページの先頭，ではありません)]" ) . "\n" );
	}

    } else {

	if (( $comType == 2 ) && ($DB_FID{$cgi'TAGS{'rfid'}} ne '')) {
	    &cgiprint'Cache( $indent . $head . &TagA( "$PROGRAM?b=$BOARD&c=ce&rtid=&rfid=" . $cgi'TAGS{'rfid'} . "&roid=" . $cgi'TAGS{'roid'} . $addNum, "[どの$H_MESGへのリプライでもなく，新着$H_MESGにする]" ) . "\n" );
	} elsif ( $comType == 4 ) {
	    &cgiprint'Cache( $indent . $head . &TagA( "$PROGRAM?b=$BOARD&c=mve&rtid=&rfid=" . $cgi'TAGS{'rfid'} . "&roid=" . $cgi'TAGS{'roid'} . $addNum, "[全記事の先頭に移動する(このページの先頭，ではありません)]" ) . "\n" );
	}
    }

    if ( $to < $from ) {

	# 空だった……
	&cgiprint'Cache( $indent . $head . "$H_NOARTICLE\n" );

    } else {
	if ( !$SYS_BOTTOMTITLE ) {
	    for( $idNum = $from; $idNum <= $to; $idNum++ ) {
		# 該当記事のIDを取り出す
		$id = $DB_ID[$idNum];
		( $fId = $DB_FID{$id} ) =~ s/,.*$//o;
		# 後方参照は後回し．
		next if (( $fId ne '' ) && ( $ADDFLAG{$fId} == 2 ));
		push( @headId, $id );
	    }
	} else {
	    for( $idNum = $to; $idNum >= $from; $idNum-- ) {
		$id = $DB_ID[$idNum];
		( $fId = $DB_FID{$id} ) =~ s/,.*$//o;
		next if (( $fId ne '' ) && ( $ADDFLAG{$fId} == 2 ));
		push( @headId, $id );
	    }
	}

	while ( $id = pop( @headId )) {
	    if ( $comType == 0 ) {
		&ViewTitleNode( $id, $indent, ( $#headId >= 0 ));
	    } else {
		&ViewTitleNodeMaint( $id, $indent, $comType, $addNum );
	    }
	}
    }

    $indent = substr( $indent, 0, -$TREE_INDENT );

    if ($SYS_BOTTOMTITLE) {
	&cgiprint'Cache("<p>$H_BOTTOM" . &TagA( "$PROGRAM?b=$BOARD&c=v&num=$num&old=$nextOld", $H_NEXTART ) . "</p>\n") if ($old);
    } else {
	&cgiprint'Cache("<p>$H_BOTTOM" . &TagA( "$PROGRAM?b=$BOARD&c=v&num=$num&old=$backOld", $H_BACKART ) . "</p>\n") if ($from > 0);
    }

    undef(%ADDFLAG);

}

sub ViewTitleNode {
    local( $id, $indent, $trailP ) = @_;
    local( $head, $daughter, @daughters );

    return if ( $ADDFLAG{ $id} != 2 );

    $head = ( $trailP ? " +" : " `" ) . "-" x $TREE_INDENT;

#    $Thread = (($SYS_F_T && $Aids) ? " " . &TagA( "$PROGRAM?b=$Board&c=t&id=$Id", $H_THREAD ) : '');

    &cgiprint'Cache( $indent . $head . &GetFormattedTitle( $id, $BOARD, $DB_AIDS{$id}, $DB_ICON{$id}, $DB_TITLE{$id}, $DB_NAME{$id}, $DB_DATE{$id}) . "\n");
    $ADDFLAG{$id} = 1;		# 整形済み

    # 娘が居れば……
    if ( @daughters = split( /,/, $DB_AIDS{$id} )) {

	if ( $trailP ) {
	    $indent .= " |" . " " x $TREE_INDENT ;
	} else {
	    $indent .= " " x ( $TREE_INDENT+2 );
	}

	while( $daughter = pop( @daughters )) {
	    &ViewTitleNode( $daughter, $indent, ( $#daughters >= 0 ));
	}
    }
}

sub ViewTitleNodeMaint {

    local( $Id, $indent, $ComType, $AddNum ) = @_;

    return if ($ADDFLAG{$Id} != 2);

    local($FromId) = $cgi'TAGS{'rfid'};

    &cgiprint'Cache( $indent . $head . &GetFormattedTitle($Id, $BOARD, $DB_AIDS{$Id}, $DB_ICON{$Id}, $DB_TITLE{$Id}, $DB_NAME{$Id}, $DB_DATE{$Id})); #'

    &cgiprint'Cache(" .......... \n");

    # リンク先変更コマンド(From)
    # 移動コマンド(From)
    if ($SYS_F_MV) {
	&cgiprint'Cache( &TagA( "$PROGRAM?b=$BOARD&c=ct&rfid=$Id&roid=" . $DB_FID{$Id} . $AddNum, $H_RELINKFROM_MARK ) . "\n" );
	if ($DB_FID{$Id} eq '') {
	    &cgiprint'Cache( &TagA( "$PROGRAM?b=$BOARD&c=mvt&rfid=$Id&roid=" . $DB_FID{$Id} . $AddNum, $H_REORDERFROM_MARK ) . "\n" );
	}
    }

    # 削除コマンド
    if ($SYS_F_D) {
	&cgiprint'Cache( &TagA( "$PROGRAM?b=$BOARD&c=dp&id=$Id", $H_DELETE_ICON ) . "\n" );
	&cgiprint'Cache( &TagA( "$PROGRAM?b=$BOARD&c=f&s=on&id=$Id", $H_SUPERSEDE_ICON ) . "\n" );
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
    if ( @daughters = split( /,/, $DB_AIDS{$id} )) {

	if ( $trailP ) {
	    $indent .= " |" . " " x $TREE_INDENT ;
	} else {
	    $indent .= " " x ( $TREE_INDENT+2 );
	}

	while( $daughter = pop( @daughters )) {
	    &ViewTitleNodeMaint( $daughter, $indent, ( $#daughters >= 0 ), $ComType, $AddNum );
	}
    }
}

1;
