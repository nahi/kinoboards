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

    # ���Ǽ��Ĥξ������Ф�
    &GetAllBoardInfo(*BoardList, *BoardInfo);

    &MsgHeader("Board List", "$SYSTEM_NAME");

    &cgiprint'Cache(<<__EOF__);
<p>
<a href="http://www.kinotrope.co.jp/~nakahiro/kb10.shtml">KINOBOARDS/1.0</a>
�Ǳ��Ĥ���Ƥ��륷���ƥ�Ǥ���
</p><p>
$SYSTEM_NAME�Ǥϡ����ߡ��ʲ���$H_BOARD���Ѱդ���Ƥ��ޤ���
</p>
__EOF__

    &cgiprint'Cache("<dl>\n");
    while(($Key, $Value) = each(%BoardList)) {
	$ModTime = &GetDateTimeFormatFromUtc(&GetModifiedTime($DB_FILE_NAME, $Key));
	$NumOfArticle = &GetArticleId($Key);
	&cgiprint'Cache("<p>\n<dt><a href=\"$PROGRAM?b=$Key&c=v&num=$DEF_TITLE_NUM\">$Value</a>\n");
	&cgiprint'Cache("[�ǿ�: $ModTime, ������: $NumOfArticle]\n");
	&cgiprint'Cache("<dd>$BoardInfo{$Key}\n</p>\n");
    }

    &cgiprint'Cache("</dl>\n</p>\n");

    &MsgFooter;

}


1;
