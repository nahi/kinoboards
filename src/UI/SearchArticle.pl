###
## SearchArticle - �����θ���(ɽ�����̤κ���)
#
# - SYNOPSIS
#	SearchArticle;
#
# - ARGS
#	�ʤ�
#
# - DESCRIPTION
#	�����򸡺�����(������ɽ�����̤κ�����ʬ)��
#	����ѿ��Ǥ��롤CGI�ѿ��򻲾Ȥ��롥
#
# - RETURN
#	�ʤ�
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

    # ɽ�����̤κ���
    &MsgHeader( 'Message search', "$H_MESG�θ���" );

    local( %tags, $str, $msg );
    $msg =<<__EOF__;
����������ꤹ�뤳�Ȥ��Ǥ��ޤ���
</p>

<ul>
<li>��$H_SUBJECT�ס���̾���ס���$H_MESG�פ��椫�顤���������ϰϤ�����å����Ƥ���������
���ꤵ�줿�ϰϤǡ�������ɤ�ޤ�$H_MESG�����ɽ�����ޤ���
<li>������ɤˤϡ���ʸ����ʸ���ζ��̤Ϥ���ޤ���
<li>����Ƕ��ڤä�ʣ���Υ�����ɤ���ꤹ��ȡ�
��������Ƥ�ޤ�$H_MESG�Τߤ򸡺����뤳�Ȥ��Ǥ��ޤ���
<li>$H_DATE�Ǹ���������ϡ�
��$H_DATE�פ�����å������塤
�����ϰϤ��YYYY/MM/DD�׷��������դǻ��ꤷ�Ƥ�������
����1999/01/01��1999/12/31�ˡ�
�����Ƚ����Τɤ��餫���ά���Ƥ⤫�ޤ��ޤ���
__EOF__

    if ( $SYS_ICON )
    {
	$msg .=<<__EOF__;
<li>$H_ICON�Ǹ���������ϡ�
��$H_ICON�פ�����å������塤õ��$H_MESG��$H_ICON������Ǥ���������
__EOF__
    }

    $msg .=<<__EOF__;
</ul>

<p>
__EOF__

    $msg .= sprintf( "<input name=\"searchsubject\" type=\"checkbox\" value=\"on\" %s>: $H_SUBJECT<br>\n", $SearchSubject? 'CHECKED' : '' );

    $msg .= sprintf( "<input name=\"searchperson\" type=\"checkbox\" value=\"on\" %s>: ̾��<br>\n", $SearchPerson? 'CHECKED' : '' );

    $msg .= sprintf( "<input name=\"searcharticle\" type=\"checkbox\" value=\"on\" %s>: $H_MESG<br>\n", $SearchArticle? 'CHECKED' : '' );

    $msg .= sprintf( "<input name=\"searchposttime\" type=\"checkbox\" value=\"on\" %s>: $H_DATE // \n", $SearchPostTime? 'CHECKED' : '' );
    $msg .= sprintf( "<input name=\"searchposttimefrom\" type=\"text\" size=\"11\" value=\"%s\"> �� ", $SearchPostTimeFrom || '' );

    local( $sec, $min, $hour, $mday, $mon, $year, $nowStr );
    if ( !$SearchPostTime )
    {
	( $sec, $min, $hour, $mday, $mon, $year, $nowStr ) = localtime( $^T );
	$nowStr = sprintf( "%04d/%02d/%02d", $year+1900, $mon+1, $mday );
    }
    $msg .= sprintf( "<input name=\"searchposttimeto\" type=\"text\" size=\"11\" value=\"%s\">�δ�<br>\n", $SearchPostTimeTo || $nowStr );

    if ( $SYS_ICON )
    {
	$msg .= sprintf( "<input name=\"searchicon\" type=\"checkbox\" value=\"on\" %s>: $H_ICON // \n", $SearchIcon? 'CHECKED' : '' );

	# �������������
	&CacheIconDb( $BOARD );	# ��������DB�Υ���å���
	$msg .= sprintf( "<SELECT NAME=\"icon\">\n<OPTION%s>$H_NOICON\n", ( $Icon && ( $Icon ne $H_NOICON ))? '' : ' SELECTED' );

	local( $IconTitle );
	foreach $IconTitle ( sort keys( %ICON_FILE ))
	{
	    $msg .= sprintf( "<OPTION%s>$IconTitle\n", ( $Icon eq $IconTitle )? ' SELECTED' : '' );
	}
	$msg .= "</SELECT>\n";

	# �����������
	$msg .= '(' . &TagA( "$PROGRAM?b=$BOARD&c=i&type=entry", "�Ȥ���$H_ICON����" ) . ")\n";
    }

    $msg .=<<__EOF__;
</p>

<p>
�������:
<input name="key" type="text" size="$KEYWORD_LENGTH" value="$Key">
__EOF__

    %tags = ( 'c', 's', 'b', $BOARD );
    &TagForm( *str, *tags, "��������", "�ꥻ�åȤ���", *msg );
    &cgiprint'Cache( $str );

    &cgiprint'Cache( $H_HR );

    # ������ɤ����Ǥʤ���С����Υ�����ɤ�ޤ൭���Υꥹ�Ȥ�ɽ��
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

    # �ꥹ�ȳ���
    &cgiprint'Cache("<p><ul>\n");

    local( $dId, $dAids, $dDate, $dTitle, $dIcon, $dName, $dEmail );
    local( $SubjectFlag, $PersonFlag, $PostTimeFlag, $ArticleFlag );
    local( $HitNum, $Line, $FromUtc, $ToUtc );
    foreach ($[ .. $#DB_ID)
    {
	# ��������
	$dId = $DB_ID[$_];
	$dIcon = $DB_ICON{$dId};
	$dTitle = $DB_TITLE{$dId};
	$dName = $DB_NAME{$dId};
	$dEmail = $DB_EMAIL{$dId};
	$dAids = $DB_AIDS{$dId};
	$dDate = $DB_DATE{$dId};

	# �ѿ��Υꥻ�å�
	$SubjectFlag = $PersonFlag = $PostTimeFlag = $ArticleFlag = 0;
	$Line = '';

	# ������������å�
	next if ( $Icon && ( $dIcon ne $IconType ));

	# ��ƻ���򸡺�
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
	    # �����ȥ�򸡺�
	    if ( $Subject && ( $dTitle ne '' ))
	    {
		$SubjectFlag = 1;
		foreach ( @KeyList )
		{
		    $SubjectFlag = 0 if ( $dTitle !~ /$_/i );
		}
	    }

	    # ��Ƽ�̾�򸡺�
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

	    # ��ʸ�򸡺�
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
	    # ̵���ǰ���
	    $SubjectFlag = 1;
	}

	if ( $SubjectFlag || $PersonFlag || $ArticleFlag )
	{
	    # ����1�ĤϹ��פ���
	    $HitNum++;

	    # �����ؤΥ�󥯤�ɽ��
	    &cgiprint'Cache( '<li>', &GetFormattedTitle( $dId, $dAids, $dIcon,
		$dTitle, $dName, $dDate, 1 ), "\n");

	    # ��ʸ�˹��פ���������ʸ��ɽ��
	    if ( $ArticleFlag )
	    {
		$Line =~ s/<[^>]*>//go;
		&cgiprint'Cache( "<blockquote>$Line</blockquote>\n" );
	    }
	}
    }

    # �ҥåȤ�����
    if ( $HitNum )
    {
	&cgiprint'Cache( "</ul>\n</p><p>\n<ul>" );
	&cgiprint'Cache( "<li>$HitNum���$H_MESG�����Ĥ���ޤ�����\n" );
    }
    else
    {
	&cgiprint'Cache( "<li>��������$H_MESG�ϸ��Ĥ���ޤ���Ǥ�����\n" );
    }

    # �ꥹ���Ĥ���
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
