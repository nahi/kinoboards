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
    &LockBoard;
    # cache article DB
    &DbCache( $BOARD ) if $BOARD;
    &UnlockBoard;

    local( $Key ) = $cgi'TAGS{'key'};
    local( $SearchSubject ) = $cgi'TAGS{'searchsubject'};
    local( $SearchPerson ) = $cgi'TAGS{'searchperson'};
    local( $SearchArticle ) = $cgi'TAGS{'searcharticle'};
    local( $SearchIcon ) = $cgi'TAGS{'searchicon'};
    local( $Icon ) = $cgi'TAGS{'icon'};

    # ɽ�����̤κ���
    &MsgHeader('Message search', "$H_MESG�θ���");

    local( %tags, $str, $msg );
    $msg =<<__EOF__;
<ul>
<li>��$H_SUBJECT�ס���̾���ס���$H_MESG�פ��椫�顤���������ϰϤ�����å����Ƥ���������
���ꤵ�줿�ϰϤǡ�������ɤ�ޤ�$H_MESG�����ɽ�����ޤ���
<li>������ɤˤϡ���ʸ����ʸ���ζ��̤Ϥ���ޤ���
<li>������ɤ�Ⱦ�ѥ��ڡ����Ƕ��ڤäơ�ʣ���Υ�����ɤ���ꤹ��ȡ�
��������Ƥ�ޤ�$H_MESG�Τߤ򸡺����뤳�Ȥ��Ǥ��ޤ���
<li>��������Ǹ���������ϡ�
�֥�������פ�����å������塤õ������$H_MESG�Υ������������Ǥ���������
</ul>
__EOF__

    $msg .= sprintf("<input name=\"searchsubject\" type=\"checkbox\" value=\"on\" %s>: $H_SUBJECT<br>\n", (($SearchSubject) ? 'CHECKED' : ''));
    $msg .= sprintf("<input name=\"searchperson\" type=\"checkbox\" value=\"on\" %s>: ̾��<br>\n", (($SearchPerson) ? 'CHECKED' : ''));
    $msg .= sprintf("<input name=\"searcharticle\" type=\"checkbox\" value=\"on\" %s>: $H_MESG<br>\n", (($SearchArticle) ? 'CHECKED' : ''));
    $msg .= sprintf("<input name=\"searchicon\" type=\"checkbox\" value=\"on\" %s>: $H_ICON // \n", (($SearchIcon) ? 'CHECKED' : ''));

    # �������������
    &CacheIconDb;	# ��������DB�Υ���å���
    $msg .= sprintf("<SELECT NAME=\"icon\">\n<OPTION%s>$H_NOICON\n", (($Icon && ($Icon ne $H_NOICON)) ? '' : ' SELECTED'));

    local( $IconTitle );
    foreach $IconTitle ( sort keys( %ICON_FILE ))
    {
	$msg .= sprintf("<OPTION%s>$IconTitle\n", (($Icon eq $IconTitle) ? ' SELECTED' : ''));
    }
    $msg .= "</SELECT>\n";

    # �����������
    $msg .= "(" . &TagA( "$PROGRAM?b=$BOARD&c=i&type=entry", "�������������" ) . ")\n</p>\n";

    $msg .=<<__EOF__;
<p>
�������:
<input name="key" type="text" size="$KEYWORD_LENGTH" value="$Key">
</p>
__EOF__

    %tags = ( 'c', 's', 'b', $BOARD );
    &TagForm( *str, *tags, "��������", "�ꥻ�åȤ���", *msg );
    &cgiprint'Cache( $str );

    &cgiprint'Cache( $H_HR );

    # ������ɤ����Ǥʤ���С����Υ�����ɤ�ޤ൭���Υꥹ�Ȥ�ɽ��
    if (($SearchIcon ne '') || (($Key ne '') && ($SearchSubject || ($SearchPerson || $SearchArticle)))) {
	&SearchArticleList($Key, $SearchSubject, $SearchPerson, $SearchArticle, $SearchIcon, $Icon);
    }

    &MsgFooter;
}

sub SearchArticleList
{
    local($Key, $Subject, $Person, $Article, $Icon, $IconType) = @_;

    local($dId, $dAids, $dDate, $dTitle, $dIcon, $dName, $dEmail, $HitNum, $Line, $SubjectFlag, $PersonFlag, $ArticleFlag, @KeyList);

    @KeyList = split(/ +/, $Key);

    # �ꥹ�ȳ���
    &cgiprint'Cache("<p><ul>\n");

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
	$SubjectFlag = $PersonFlag = $ArticleFlag = 0;
	$Line = '';

	# ������������å�
	next if (($Icon ne '') && ($dIcon ne $IconType));

	if ($Key ne '')
	{
	    # �����ȥ�򸡺�
	    if (($Subject ne '') && ($dTitle ne ''))
	    {
		$SubjectFlag = 1;
		foreach (@KeyList)
		{
		    $SubjectFlag = 0 if ($dTitle !~ /$_/i);
		}
	    }

	    # ��Ƽ�̾�򸡺�
	    if ($SubjectFlag == 0 && ($Person ne '') && ($dName ne ''))
	    {
		$PersonFlag = 1;
		foreach (@KeyList)
		{
		    $PersonFlag = 0 if (($dName !~ /$_/i) && ($dEmail !~ /$_/i));
		}
	    }

	    # ��ʸ�򸡺�
	    if (($SubjectFlag == 0) && ($PersonFlag == 0) && ($Article ne '') && ($Line = &SearchArticleKeyword($dId, $BOARD, @KeyList))) {
		$ArticleFlag = 1;
	    }
	}
	else
	{
	    # ̵���ǰ���
	    $SubjectFlag = 1;
	}

	if ($SubjectFlag || $PersonFlag || $ArticleFlag)
	{
	    # ����1�ĤϹ��פ���
	    $HitNum++;

	    # �����ؤΥ�󥯤�ɽ��
	    &cgiprint'Cache( '<li>', &GetFormattedTitle( $dId, $dAids, $dIcon, $dTitle, $dName, $dDate, 1 ), "\n");

	    # ��ʸ�˹��פ���������ʸ��ɽ��
	    if ($ArticleFlag)
	    {
		$Line =~ s/<[^>]*>//go;
		&cgiprint'Cache("<blockquote>$Line</blockquote>\n");
	    }
	}
    }

    # �ҥåȤ��ʤ��ä���
    if ($HitNum)
    {
	&cgiprint'Cache("</ul>\n</p><p>\n<ul>");
	&cgiprint'Cache("<li>$HitNum���$H_MESG�����Ĥ���ޤ�����\n");
    }
    else
    {
	&cgiprint'Cache("<li>��������$H_MESG�ϸ��Ĥ���ޤ���Ǥ�����\n");
    }

    # �ꥹ���Ĥ���
    &cgiprint'Cache("</ul></p>\n");
}

1;
