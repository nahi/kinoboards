###
## ShowIcon - ��������ɽ������
#
# - SYNOPSIS
#	ShowIcon;
#
# - ARGS
#	�ʤ�
#
# - DESCRIPTION
#	��������ɽ�����̤�ɽ�����롥
#	����ѿ��Ǥ��롤CGI�ѿ��򻲾Ȥ��롥
#
# - RETURN
#	�ʤ�
#
ShowIcon: {

    local($IconTitle, $Type);

    # �����פ򽦤�
    $Type = $cgi'TAGS{'type'};

    # ɽ�����̤κ���
    &MsgHeader('Icon show', "�������������");

    if ($Type eq 'article') {

	&cgiprint'Cache(<<__EOF__);
<p>
�ƥ�������ϼ��ε�ǽ��ɽ���Ƥ��ޤ���
</p>
<ul>
<p>
<li>$H_THREAD : ($H_SUBJECT������)����$H_MESG��$H_REPLY��ޤȤ���ɤ�
</p><p>
__EOF__
	&cgiprint'Cache( "<li>" . &TagComImg( $ICON_BLIST, $H_BACKBOARD, 2 ) . "\n" );
	&cgiprint'Cache( "<li>" . &TagComImg( $ICON_TLIST, $H_BACKTITLE, 2 ) . "\n" );
	&cgiprint'Cache( "<li>" . &TagComImg( $ICON_PREV, $H_PREVARTICLE, 2 ) . "\n" );
	&cgiprint'Cache( "<li>" . &TagComImg( $ICON_NEXT, $H_NEXTARTICLE, 2 ) . "\n" );
	&cgiprint'Cache( "<li>" . &TagComImg( $ICON_THREAD, $H_READREPLYALL, 2 ) . "\n" );
	&cgiprint'Cache( "</p><p>\n" );
	&cgiprint'Cache( "<li>" . &TagComImg( $ICON_WRITENEW, $H_POSTNEWARTICLE, 2 ) . "\n" );
	&cgiprint'Cache( "<li>" . &TagComImg( $ICON_FOLLOW, $H_REPLYTHISARTICLE, 2 ) . "\n" );
	&cgiprint'Cache( "<li>" . &TagComImg( $ICON_QUOTE, $H_REPLYTHISARTICLEQUOTE, 2 ) . "\n" );
	&cgiprint'Cache(<<__EOF__);
</p>
</ul>
__EOF__

    } else {

	&CashIconDb($BOARD);	# ��������DB�Υ���å���

	&cgiprint'Cache(<<__EOF__);
<p>
$H_BOARD��$BOARDNAME�פǤϡ����Υ��������Ȥ����Ȥ��Ǥ��ޤ���
</p><p>
<ul>
__EOF__
	foreach $IconTitle (@ICON_TITLE) {
	    &cgiprint'Cache( "<li>" . &TagMsgImg( &GetIconUrlFromTitle($IconTitle, $BOARD), $IconTitle ) . sprintf( " : %s\n", ($ICON_HELP{$IconTitle} || $IconTitle )));
	}
	&cgiprint'Cache("</ul>\n</p>\n");

    }

    &MsgFooter;

}

1;
