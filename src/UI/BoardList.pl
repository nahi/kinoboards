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
BoardList: {

    local(%BoardList, %BoardInfo, $Key, $Value, $ModTime, $NumOfArticle);

    # lock system
    local( $lockResult ) = $PC ? 1 : &cgi'lock( $LOCK_FILE );
    &Fatal(1001, '') if ( $lockResult == 2 );
    &Fatal(999, '') if ( $lockResult != 1 );

    # ���Ǽ��Ĥξ������Ф�
    &GetAllBoardInfo(*BoardList, *BoardInfo);

    &MsgHeader("Board List", "$SYSTEM_NAME");

    &cgiprint'Cache( "<p>\n" . &TagA( "http://www.kinotrope.co.jp/~nakahiro/kb10.shtml", "KINOBOARDS/1.0" ));
    &cgiprint'Cache(<<__EOF__);
�Ǳ��Ĥ���Ƥ��륷���ƥ�Ǥ���
</p><p>
$SYSTEM_NAME�Ǥϡ����ߡ��ʲ���$H_BOARD���Ѱդ���Ƥ��ޤ���
</p>
__EOF__

    &cgiprint'Cache("<ul>\n");
    while(($Key, $Value) = each(%BoardList)) {
	$ModTime = &GetDateTimeFormatFromUtc(&GetModifiedTime($DB_FILE_NAME, $Key));
	$NumOfArticle = &GetArticleId($Key) || 0;
	&cgiprint'Cache("<li>" . &TagA( "$PROGRAM?b=$Key&c=v&num=$DEF_TITLE_NUM", $Value ) . "\n");
	&cgiprint'Cache("[�ǿ�: $ModTime, ������: $NumOfArticle]\n");
    }

    &cgiprint'Cache("</ul>\n");

    # unlock system
    &cgi'unlock( $LOCK_FILE ) unless $PC;

    &MsgFooter;

}


1;
