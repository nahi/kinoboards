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
    local( %BoardList, %BoardInfo, $Key, $Value, $NumOfArticle );

    # ���Ǽ��Ĥξ������Ф�
    &GetAllBoardInfo( *BoardList, *BoardInfo );

    &MsgHeader( "Board List", "$SYSTEM_NAME" );

    &cgiprint'Cache( "<p>\n" . &TagA( "http://www.kinotrope.co.jp/~nakahiro/kb10.shtml", "KINOBOARDS/1.0" ));
    &cgiprint'Cache(<<__EOF__);
�Ǳ��Ĥ���Ƥ��륷���ƥ�Ǥ���
</p>

<p>
$SYSTEM_NAME�Ǥϡ����ߡ��ʲ���$H_BOARD���Ѱդ���Ƥ��ޤ���
</p>
__EOF__

    &cgiprint'Cache("<ul>\n");
    local( $newIcon, $modTimeUtc, $modTime );
    while (( $Key, $Value ) = each( %BoardList ))
    {
	$modTimeUtc = &GetModifiedTime( $DB_FILE_NAME, $Key );
	$modTime = &GetDateTimeFormatFromUtc( $modTimeUtc );
	if ( $SYS_BLIST_NEWICON_DATE && (( $^T - $modTimeUtc ) < $SYS_BLIST_NEWICON_DATE * 86400 ))
	{
	    $newIcon = " " . &TagMsgImg( $ICON_NEW, $H_NEWARTICLE );
	}
	else
	{
	    $newIcon = '';
	}
	&GetArticleId( $Key, *NumOfArticle ) || 0;

	&cgiprint'Cache( "<li>", &TagA( "$PROGRAM?b=$Key&c=v&num=$DEF_TITLE_NUM", $Value ), "$newIcon\n[�ǿ�: $modTime, ������: $NumOfArticle]<br>\n" );
    }

    &cgiprint'Cache("</ul>\n");

    &MsgFooter;

}


1;
