###
## ShowArticle - ñ�쵭����ɽ��
#
# - SYNOPSIS
#	ShowArticle;
#
# - ARGS
#	�ʤ�
#
# - DESCRIPTION
#	ñ��ε�����ɽ�����롥
#       ����ѿ��Ǥ��롤CGI�ѿ��򻲾Ȥ��롥
#
# - RETURN
#	�ʤ�
#
ShowArticle: {

    local($Id, $Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $DateUtc, $Aid, @AidList, @FollowIdTree);

    # lock system
    local( $lockResult ) = &cgi'lock( $LOCK_FILE );
    &Fatal(1001, '') if ( $lockResult == 2 );
    &Fatal(999, '') if ( $lockResult != 1 );
    # cash article DB
    if ( $BOARD ) { &DbCash( $BOARD ); }

    $Id = $cgi'TAGS{'id'};
    ($Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url) = &GetArticlesInfo($Id);
    $DateUtc = &GetUtcFromOldDateTimeFormat($Date);
    @AidList = split(/,/, $Aids);

    # ̤��Ƶ������ɤ�ʤ�
    if ($Name eq '') { &Fatal(8, ''); }

    # ɽ�����̤κ���
    &MsgHeader('Message view', "$BOARDNAME: $Subject", $DateUtc);
    &ViewOriginalArticle($Id, 1, 1);

    # article end
    &cgiprint'Cache("$H_LINE\n<p>\n");

    # ȿ������
    &cgiprint'Cache("��$H_REPLY\n");
    if ($Aids ne '') {

	# ȿ������������ʤ��
	foreach $Aid (@AidList) {

	    # �ե����������ڹ�¤�μ���
	    # ex. '( a ( b ( c d ) ) ( e ) ( f ( g ) ) )'�Ȥ����ꥹ��
	    @FollowIdTree = &GetFollowIdTree($Aid);

	    # �ᥤ��ؿ��θƤӽФ�(��������)
	    &ThreadArticleMain('subject only', @FollowIdTree);

	}

    } else {

	# ȿ������̵��
	&cgiprint'Cache("<ul>\n<li>$H_REPLY�Ϥ���ޤ���\n</ul>\n");

    }

    &cgiprint'Cache("</p>\n");

    # ����«
    &MsgFooter;

    # unlock system
    &cgi'unlock( $LOCK_FILE );

}

1;
