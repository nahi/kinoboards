###
## SortArticle - ���ս�˥�����
#
# - SYNOPSIS
#	SortArticle;
#
# - ARGS
#	�ʤ�
#
# - DESCRIPTION
#	�����ȥ���������ս�˥����Ȥ���ɽ�����롥
#	����ѿ��Ǥ��롤CGI�ѿ��򻲾Ȥ��롥
#
# - RETURN
#	�ʤ�
#
SortArticle: {

    local($Num, $Old, $NextOld, $BackOld, $To, $From, $IdNum, $Id);

    # lock system
    local( $lockResult ) = &cgi'lock( $LOCK_FILE );
    &Fatal(1001, '') if ( $lockResult == 2 );
    &Fatal(999, '') if ( $lockResult != 1 );
    # cash article DB
    if ( $BOARD ) { &DbCash( $BOARD ); }
    # unlock system
    &cgi'unlock( $LOCK_FILE );

    # ɽ������Ŀ������
    $Num = $cgi'TAGS{'num'};
    $Old = $cgi'TAGS{'old'};
    $NextOld = ($Old > $Num) ? ($Old - $Num) : 0;
    $BackOld = ($Old + $Num);
    $To = $#DB_ID - $Old;
    $From = $To - $Num + 1; $From = 0 if (($From < 0) || ($Num == 0));

    # ɽ�����̤κ���
    &MsgHeader('Title view (sorted)', "$BOARDNAME: $H_SUBJECT����(���ս�)");

    &BoardHeader('normal');

    &cgiprint'Cache("<hr>\n");

    if ($SYS_BOTTOMTITLE) {
	&cgiprint'Cache("<p>$H_TOP<a href=\"$PROGRAM?b=$BOARD&c=r&num=$Num&old=$BackOld\">$H_BACKART</a></p>\n") if ($From > 0);
    } else {
	&cgiprint'Cache("<p>$H_TOP<a href=\"$PROGRAM?b=$BOARD&c=r&num=$Num&old=$NextOld\">$H_NEXTART</a></p>\n") if ($Old);
    }

    &cgiprint'Cache("<p><ul>\n");

    # ������ɽ��
    if ($#DB_ID == -1) {

	# �����ä��ġ�
	&cgiprint'Cache("<li>$H_NOARTICLE\n");

    } else {

	if ($SYS_BOTTOMTITLE) {
	    for ($IdNum = $From; $IdNum <= $To; $IdNum++) {
		$Id = $DB_ID[$IdNum];
		&cgiprint'Cache("<li>" . &GetFormattedTitle($Id, $BOARD, $DB_AIDS{$Id}, $DB_ICON{$Id}, $DB_TITLE{$Id}, $DB_NAME{$Id}, $DB_DATE{$Id}) . "\n");
	    }
	} else {
	    for ($IdNum = $To; $IdNum >= $From; $IdNum--) {
		$Id = $DB_ID[$IdNum];
		&cgiprint'Cache("<li>" . &GetFormattedTitle($Id, $BOARD, $DB_AIDS{$Id}, $DB_ICON{$Id}, $DB_TITLE{$Id}, $DB_NAME{$Id}, $DB_DATE{$Id}) . "\n");
	    }
	}
    }

    &cgiprint'Cache("</ul></p>\n");

    if ($SYS_BOTTOMTITLE) {
	&cgiprint'Cache("<p>$H_BOTTOM<a href=\"$PROGRAM?b=$BOARD&c=r&num=$Num&old=$NextOld\">$H_NEXTART</a></p>\n") if ($Old);
    } else {
	&cgiprint'Cache("<p>$H_BOTTOM<a href=\"$PROGRAM?b=$BOARD&c=r&num=$Num&old=$BackOld\">$H_BACKART</a></p>\n") if ($From > 0);
    }

    &MsgFooter;

}

1;
