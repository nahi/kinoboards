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
ShowIcon:
{
    # �����פ򽦤�
    local( $Type ) = $cgi'TAGS{'type'};

    # ɽ�����̤κ���
    &MsgHeader( 'Icon show', "�������������" );

    local( $msg );
    if ( $Type eq 'article' )
    {
	$msg .= <<__EOF__;
<p>
�ƥ�������ϼ��ε�ǽ��ɽ���Ƥ��ޤ���
</p>

<ul>
<li>$H_THREAD : ����$H_MESG��$H_REPLY��ޤȤ��ɽ�����ޤ���
__EOF__

	$msg .= '<li>' . &TagMsgImg( $ICON_NEW, $H_NEWARTICLE ) .
	     " : �Ƕ�񤭹��ޤ줿$H_MESG\n";

	$msg .= '<li>' . &TagComImg( $ICON_BLIST, $H_BACKBOARD, 2 ) . "\n";
	$msg .= '<li>' . &TagComImg( $ICON_TLIST, $H_BACKTITLEREPLY, 2 ) ."\n";
	$msg .= '<li>' . &TagComImg( $ICON_PREV, $H_PREVARTICLE, 2 ) . "\n";
	$msg .= '<li>' . &TagComImg( $ICON_NEXT, $H_NEXTARTICLE, 2 ) . "\n";
	$msg .= '<li>' . &TagComImg( $ICON_THREAD, $H_READREPLYALL, 2 ) . "\n";
	$msg .= "<br><br>\n";
	$msg .= '<li>' . &TagComImg( $ICON_WRITENEW, $H_POSTNEWARTICLE, 2 ) .
	    "\n";
	$msg .= '<li>' . &TagComImg( $ICON_FOLLOW, $H_REPLYTHISARTICLE, 2 ) .
	    "\n";
	$msg .= '<li>' . &TagComImg( $ICON_QUOTE, $H_REPLYTHISARTICLEQUOTE, 2 )
	    . "\n";
	$msg .= "</ul>\n";
    }
    else
    {
	&CacheIconDb;	# ��������DB�Υ���å���
	$msg .= <<__EOF__;
<p>
$H_BOARD��$BOARDNAME�פǤϡ��ƥ�������ϼ��Τ褦�ʰ�̣�Ǥ���
</p>

<ul>
<li>$H_THREAD_ALL : ����$H_MESG��$H_ORIG_TOP���顤���Ƥ�$H_REPLY��ޤȤ��ɽ�����ޤ���
<li>$H_THREAD : ����$H_MESG��$H_REPLY��ޤȤ��ɽ�����ޤ���
<br><br>
__EOF__
	$msg .= '<li>' . &TagMsgImg( $ICON_NEW, $H_NEWARTICLE ) .
	    " : �Ƕ�񤭹��ޤ줿$H_MESG\n<br><br>\n";

	local( $IconTitle );
	foreach $IconTitle (@ICON_TITLE)
	{
	    $msg .= '<li>' .
		&TagMsgImg( &GetIconUrlFromTitle( $IconTitle, $BOARD ),
		    $IconTitle ) . " : " .
		    ( $ICON_HELP{$IconTitle} || $IconTitle ) . "\n";
	}
	$msg .= "</ul>\n";
    }

    &cgiprint'Cache( $msg );
    &MsgFooter;
}

1;
