###
## ThreadExt - スレッド別タイトルおよび記事一覧
#
# - SYNOPSIS
#	ThreadExt;
#
# - ARGS
#	なし
#
# - DESCRIPTION
#	記事をスレッド別にソートして表示し，
#	その後ろにスレッド順に記事を表示する．
#	大域変数である，CGI変数を参照する．
#	大域変数ADDFLAG(既に表示してしまったか否かを表わすフラグ)を破壊する．
#
# - RETURN
#	なし
#
ThreadExt:
{
    %ADDFLAG = ();		# these are static.
    @IDLIST = ();

    &LockBoard();
    &DbCache( $BOARD ) if $BOARD;
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

    local( $pageLinkStr ) = &PageLink( 'vt', $Num, $Old, $Rev );

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
    &MsgHeader( 'Thread extension view', "$H_SUBJECTおよび$H_MESG一覧($H_REPLY順)" );

    &BoardHeader();
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
	    &cgiprint'Cache( "</ul>\n" );
	}
    }
    else
    {
	for( $IdNum = $To; $IdNum >= $From; $IdNum-- )
	{
	    $Id = $DB_ID[$IdNum];
	    ( $Fid = $DB_FID{ $Id } ) =~ s/,.*$//o;
#	    next if ((( $Fid ne '' ) && ( $SYS_THREAD_FORMAT == 2 )) || ( $ADDFLAG{$Fid} == 2 ));
	    next if (( $Fid ne '' ) && (( $ADDFLAG{$Fid} == 2 ) || ( $SYS_THREAD_FORMAT == 2 )));

	    &cgiprint'Cache( "<ul>\n" );
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
	    &cgiprint'Cache( "</ul>\n" );
	}
    }

    if ( $#IDLIST >= 0 )
    {
	&cgiprint'Cache( "$H_HR\n" );

	while ( $Id = shift( @IDLIST ))
	{
	    &ViewOriginalArticle( $Id, $SYS_COMMAND_EACH, 1 );
	    &cgiprint'Cache( "$H_HR\n" );
	}
    }

    &cgiprint'Cache( $pageLinkStr );

    &MsgFooter;

    undef( %ADDFLAG );
    undef( @IDLIST );
}


###
## 新着ノードのみ表示
#
sub ThreadTitleNodeNoThread
{
    local( $Id ) = @_;

    &cgiprint'Cache( '<li>', &GetFormattedTitle( $Id, $DB_AIDS{$Id}, $DB_ICON{$Id}, $DB_TITLE{$Id}, $DB_NAME{$Id}, $DB_DATE{$Id}, 3 ), "\n");
    push( @IDLIST, $Id );
}


###
## ページ内スレッドのみ表示
#
sub ThreadTitleNodeThread
{
    local( $Id, $top ) = @_;

    # ページ外ならおしまい．
    return if ( $ADDFLAG{$Id} != 2 );

    &cgiprint'Cache( '<li>', &GetFormattedTitle($Id, $DB_AIDS{$Id}, $DB_ICON{$Id}, $DB_TITLE{$Id}, $DB_NAME{$Id}, $DB_DATE{$Id}, $top|2 ), "\n" );
    $ADDFLAG{$Id} = 1;		# 整形済み
    push( @IDLIST, $Id );

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

    &cgiprint'Cache( '<li>', &GetFormattedTitle($Id, $DB_AIDS{$Id}, $DB_ICON{$Id}, $DB_TITLE{$Id}, $DB_NAME{$Id}, $DB_DATE{$Id}, $top|2 ), "\n" );
    $ADDFLAG{$Id} = 1;		# 整形済み
    push( @IDLIST, $Id );

    # 娘が居れば……
    if ( $DB_AIDS{$Id} )
    {
	&cgiprint'Cache( "<ul>\n" );
	grep( &ThreadTitleNodeAllThread( $_, 0 ), split( /,/, $DB_AIDS{$Id} ));
	&cgiprint'Cache( "</ul>\n" );
    }
}


1;
