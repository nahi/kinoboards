###
## SearchArticle - 記事の検索(表示画面の作成)
#
# - SYNOPSIS
#	SearchArticle;
#
# - ARGS
#	なし
#
# - DESCRIPTION
#	記事を検索する(うち，表示画面の作成部分)．
#	大域変数である，CGI変数を参照する．
#
# - RETURN
#	なし
#
SearchArticle:
{
    &LockBoard();
    # cache article DB
    &DbCache( $BOARD ) if $BOARD;
    &UnlockBoard();

    local( $Key ) = $cgi'TAGS{'key'};
    local( $SearchSubject ) = $cgi'TAGS{'searchsubject'};
    local( $SearchPerson ) = $cgi'TAGS{'searchperson'};
    local( $SearchArticle ) = $cgi'TAGS{'searcharticle'};
    local( $SearchPostTime ) = $cgi'TAGS{'searchposttime'};
    local( $SearchPostTimeFrom ) = $cgi'TAGS{'searchposttimefrom'};
    local( $SearchPostTimeTo ) = $cgi'TAGS{'searchposttimeto'};
    local( $SearchIcon ) = $cgi'TAGS{'searchicon'};
    local( $Icon ) = $cgi'TAGS{'icon'};

    # 表示画面の作成
    &MsgHeader( 'Message search', "$H_MESGの検索" );

    local( %tags, $str, $msg );
    $msg =<<__EOF__;
検索条件を指定することができます．
</p>

<ul>
<li>「$H_SUBJECT」，「名前」，「$H_MESG」の中から，検索する範囲をチェックしてください．
指定された範囲で，キーワードを含む$H_MESGを一覧表示します．
<li>キーワードには，大文字小文字の区別はありません．
<li>空白で区切って複数のキーワードを指定すると，
それら全てを含む$H_MESGのみを検索することができます．
<li>$H_DATEで検索する場合は，
「$H_DATE」をチェックした後，
検索範囲を「YYYY/MM/DD」形式の日付で指定してください
（例1999/01/01〜1999/12/31）．
始点と終点のどちらかを省略してもかまいません．
__EOF__

    if ( $SYS_ICON )
    {
	$msg .=<<__EOF__;
<li>$H_ICONで検索する場合は，
「$H_ICON」をチェックした後，探す$H_MESGの$H_ICONを選んでください．
__EOF__
    }

    $msg .=<<__EOF__;
</ul>

<p>
__EOF__

    $msg .= sprintf( "<input name=\"searchsubject\" type=\"checkbox\" value=\"on\" %s>: $H_SUBJECT<br>\n", $SearchSubject? 'CHECKED' : '' );

    $msg .= sprintf( "<input name=\"searchperson\" type=\"checkbox\" value=\"on\" %s>: 名前<br>\n", $SearchPerson? 'CHECKED' : '' );

    $msg .= sprintf( "<input name=\"searcharticle\" type=\"checkbox\" value=\"on\" %s>: $H_MESG<br>\n", $SearchArticle? 'CHECKED' : '' );

    $msg .= sprintf( "<input name=\"searchposttime\" type=\"checkbox\" value=\"on\" %s>: $H_DATE // \n", $SearchPostTime? 'CHECKED' : '' );
    $msg .= sprintf( "<input name=\"searchposttimefrom\" type=\"text\" size=\"11\" value=\"%s\"> 〜 ", $SearchPostTimeFrom || '' );

    local( $sec, $min, $hour, $mday, $mon, $year, $nowStr );
    if ( !$SearchPostTime )
    {
	( $sec, $min, $hour, $mday, $mon, $year, $nowStr ) = localtime( $^T );
	$nowStr = sprintf( "%04d/%02d/%02d", $year+1900, $mon+1, $mday );
    }
    $msg .= sprintf( "<input name=\"searchposttimeto\" type=\"text\" size=\"11\" value=\"%s\">の間<br>\n", $SearchPostTimeTo || $nowStr );

    if ( $SYS_ICON )
    {
	$msg .= sprintf( "<input name=\"searchicon\" type=\"checkbox\" value=\"on\" %s>: $H_ICON // \n", $SearchIcon? 'CHECKED' : '' );

	# アイコンの選択
	&CacheIconDb( $BOARD );	# アイコンDBのキャッシュ
	$msg .= sprintf( "<SELECT NAME=\"icon\">\n<OPTION%s>$H_NOICON\n", ( $Icon && ( $Icon ne $H_NOICON ))? '' : ' SELECTED' );

	local( $IconTitle );
	foreach $IconTitle ( sort keys( %ICON_FILE ))
	{
	    $msg .= sprintf( "<OPTION%s>$IconTitle\n", ( $Icon eq $IconTitle )? ' SELECTED' : '' );
	}
	$msg .= "</SELECT>\n";

	# アイコン一覧
	$msg .= '(' . &TagA( "$PROGRAM?b=$BOARD&c=i&type=entry", "使える$H_ICON一覧" ) . ")\n";
    }

    $msg .=<<__EOF__;
</p>

<p>
キーワード:
<input name="key" type="text" size="$KEYWORD_LENGTH" value="$Key">
__EOF__

    %tags = ( 'c', 's', 'b', $BOARD );
    &TagForm( *str, *tags, "検索する", "リセットする", *msg );
    &cgiprint'Cache( $str );

    &cgiprint'Cache( $H_HR );

    # キーワードが空でなければ，そのキーワードを含む記事のリストを表示
    if ( $SearchIcon ||
	( $SearchPostTime && ( $SearchPostTimeFrom || $SearchPostTimeTo )) || 
	(( $Key ne '' ) && ( $SearchSubject || $SearchPerson || $SearchArticle )))
    {
	&SearchArticleList( $Key, $SearchSubject, $SearchPerson,
	    $SearchArticle, $SearchPostTime, $SearchPostTimeFrom,
	    $SearchPostTimeTo, $SearchIcon, $Icon );
    }

    &MsgFooter;
}

sub SearchArticleList
{
    local( $Key, $Subject, $Person, $Article, $PostTime, $PostTimeFrom,
	$PostTimeTo, $Icon, $IconType ) = @_;

    local( @KeyList ) = split(/ +/, $Key);

    # リスト開く
    &cgiprint'Cache("<p><ul>\n");

    local( $dId, $dAids, $dDate, $dTitle, $dIcon, $dName, $dEmail );
    local( $SubjectFlag, $PersonFlag, $PostTimeFlag, $ArticleFlag );
    local( $HitNum, $Line, $FromUtc, $ToUtc );
    foreach ($[ .. $#DB_ID)
    {
	# 記事情報
	$dId = $DB_ID[$_];
	$dIcon = $DB_ICON{$dId};
	$dTitle = $DB_TITLE{$dId};
	$dName = $DB_NAME{$dId};
	$dEmail = $DB_EMAIL{$dId};
	$dAids = $DB_AIDS{$dId};
	$dDate = $DB_DATE{$dId};

	# 変数のリセット
	$SubjectFlag = $PersonFlag = $PostTimeFlag = $ArticleFlag = 0;
	$Line = '';

	# アイコンチェック
	next if ( $Icon && ( $dIcon ne $IconType ));

	# 投稿時刻を検索
	if ( $PostTime )
	{
	    $FromUtc = $ToUtc = -1;
	    $FromUtc = &GetUtcFromYYYY_MM_DD( $PostTimeFrom )
		if $PostTimeFrom;
	    $ToUtc = &GetUtcFromYYYY_MM_DD( $PostTimeTo )
		if $PostTimeTo;
	    $ToUtc += 86400 if ( $ToUtc >= 0 );
	    next if !&SearchTime( $dDate, $FromUtc, $ToUtc );
	}

	if ( $Key ne '' )
	{
	    # タイトルを検索
	    if ( $Subject && ( $dTitle ne '' ))
	    {
		$SubjectFlag = 1;
		foreach ( @KeyList )
		{
		    $SubjectFlag = 0 if ( $dTitle !~ /$_/i );
		}
	    }

	    # 投稿者名を検索
	    if ( $Person && !$SubjectFlag && ( $dName ne '' ))
	    {
		$PersonFlag = 1;
		foreach ( @KeyList )
		{
		    if (( $dName !~ /$_/i ) && ( $dEmail !~ /$_/i ))
		    {
			$PersonFlag = 0;
		    }
		}
	    }

	    # 本文を検索
	    if ( $Article && !$SubjectFlag && !$PersonFlag )
	    {
		if ( $Line = &SearchArticleKeyword( $dId, $BOARD, @KeyList ))
		{
		    $ArticleFlag = 1;
		}
	    }
	}
	else
	{
	    # 無条件で一致
	    $SubjectFlag = 1;
	}

	if ( $SubjectFlag || $PersonFlag || $ArticleFlag )
	{
	    # 最低1つは合致した
	    $HitNum++;

	    # 記事へのリンクを表示
	    &cgiprint'Cache( '<li>', &GetFormattedTitle( $dId, $dAids, $dIcon,
		$dTitle, $dName, $dDate, 1 ), "\n");

	    # 本文に合致した場合は本文も表示
	    if ( $ArticleFlag )
	    {
		$Line =~ s/<[^>]*>//go;
		&cgiprint'Cache( "<blockquote>$Line</blockquote>\n" );
	    }
	}
    }

    # ヒットしたら
    if ( $HitNum )
    {
	&cgiprint'Cache( "</ul>\n</p><p>\n<ul>" );
	&cgiprint'Cache( "<li>$HitNum件の$H_MESGが見つかりました．\n" );
    }
    else
    {
	&cgiprint'Cache( "<li>該当する$H_MESGは見つかりませんでした．\n" );
    }

    # リスト閉じる
    &cgiprint'Cache( "</ul></p>\n" );
}

sub SearchTime
{
    local( $target, $from, $to ) = @_;

    return 0 if (( $from >= 0 ) && ( $target < $from ));
    return 0 if (( $to >= 0 ) && ( $target > $to ));
    1;
}

1;
