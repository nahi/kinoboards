###
## BoardList - �Ǽ��İ�����ɽ��
#
# - SYNOPSIS
#	BoardList;
#
# - ARGS
#	�ʤ�
#
# - DESCRIPTION
#	�Ǽ��İ�����ɽ�����롥
#
# - RETURN
#	�ʤ�
#
BoardList:
{
    # ���Ǽ��Ĥξ������Ф�
    local( @board, %boardName, %boardInfo );
    &GetAllBoardInfo( *board, *boardName, *boardInfo );

    # ��$H_BOARD���� - $SYSTEM_NAME�פ������Υڡ����Υ����ȥ�Ǥ���
    &MsgHeader( "Board List", "$H_BOARD���� - $SYSTEM_NAME" );
    &cgiprint'Cache(<<__EOF__);

<!-- �Ǽ��İ����Υإå���ʬ�Ǥ��������ա����󤬤�񤭴����ޤ��礦�� -->
<p>
$SYSTEM_NAME�Ǥϡ����ߡ��ʲ���$H_BOARD���Ѱդ���Ƥ��ޤ���
</p>

<ul>
__EOF__

    local( $newIcon, $modTimeUtc, $modTime, $nofArticle );
    foreach ( @board )
    {
	$modTimeUtc = &GetModifiedTime( $DB_FILE_NAME, $_ );
	$modTime = &GetDateTimeFormatFromUtc( $modTimeUtc );
	if ( $SYS_BLIST_NEWICON_DATE &&
	    (( $^T - $modTimeUtc ) < $SYS_BLIST_NEWICON_DATE * 86400 ))
	{
	    $newIcon = " " . &TagMsgImg( $H_NEWARTICLE );
	}
	else
	{
	    $newIcon = '';
	}
	&GetArticleId( $_, *nofArticle ) || 0;

	&cgiprint'Cache( "<li>",
	    &TagA( "$PROGRAM?b=$_&c=v&num=$DEF_TITLE_NUM", $boardName{$_} ),
	    "$newIcon\n[�ǿ�: $modTime, ������: $nofArticle]\n" );

    &cgiprint'Cache(<<__EOF__);
<br><br><!-- �Ǽ���Ʊ�Τδ֤�����ޤ����֤�����뤿���BR�����Ȥ� -->
__EOF__

    }

    &cgiprint'Cache(<<__EOF__);
</ul>

<!-- �Ǽ��İ����Υեå���ʬ�Ǥ������󤬤�񤭴����ޤ��礦�� -->
<p>
$SYSTEM_NAME�Ǥϡ����ߡ��ʾ��$H_BOARD���Ѱդ���Ƥ��ޤ���
</p>

__EOF__

    &MsgFooter;
}


1;
