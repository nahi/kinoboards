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
    &MsgHeader('Icon show', "$BOARDNAME: �������������");

    if ($Type eq 'article') {

	&cgiprint'Cache(<<__EOF__);
<p>
�ƥ�������ϼ��ε�ǽ��ɽ���Ƥ��ޤ���
</p>
<ul>
<p>
<li>$H_THREAD : ($H_SUBJECT������)����$H_MESG��$H_REPLY��ޤȤ���ɤ�
</p><p>
<li><img src="$ICON_BLIST" alt="$H_BACKBOARD" height="$COMICON_HEIGHT" width="$COMICON_WIDTH"> : $H_BACKBOARD
<li><img src="$ICON_TLIST" alt="$H_BACKTITLE" height="$COMICON_HEIGHT" width="$COMICON_WIDTH"> : $H_BACKTITLE
<li><img src="$ICON_PREV" alt="$H_PREVARTICLE" height="$COMICON_HEIGHT" width="$COMICON_WIDTH"> : $H_PREVARTICLE
<li><img src="$ICON_NEXT" alt="$H_NEXTARTICLE" height="$COMICON_HEIGHT" width="$COMICON_WIDTH"> : $H_NEXTARTICLE
<li><img src="$ICON_THREAD" alt="$H_READREPLYALL" height="$COMICON_HEIGHT" width="$COMICON_WIDTH"> : $H_READREPLYALL
</p><p>
<li><img src="$ICON_WRITENEW" alt="$H_POSTNEWARTICLE" height="$COMICON_HEIGHT" width="$COMICON_WIDTH"> : $H_POSTNEWARTICLE
<li><img src="$ICON_FOLLOW" alt="$H_REPLYTHISARTICLE" height="$COMICON_HEIGHT" width="$COMICON_WIDTH"> : $H_REPLYTHISARTICLE
<li><img src="$ICON_QUOTE" alt="$H_REPLYTHISARTICLEQUOTE" height="$COMICON_HEIGHT" width="$COMICON_WIDTH"> : $H_REPLYTHISARTICLEQUOTE
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
	    &cgiprint'Cache(sprintf("<li><img src=\"%s\" alt=\"$IconTitle\" height=\"$MSGICON_HEIGHT\" width=\"$MSGICON_WIDTH\"> : %s\n", &GetIconUrlFromTitle($IconTitle, $BOARD), ($ICON_HELP{$IconTitle} || $IconTitle)));
	}
	&cgiprint'Cache("</ul>\n</p>\n");

    }

    &MsgFooter;

}

1;
