###
## Preview - �ץ�ӥ塼���̤�ɽ��
#
# - SYNOPSIS
#	Preview;
#
# - ARGS
#	�ʤ�
#
# - DESCRIPTION
#	�ץ�ӥ塼���̤�ɽ�����롥
#	����ѿ��Ǥ��롤CGI�ѿ��򻲾Ȥ��롥
#
# - RETURN
#	�ʤ�
#
Preview: {

    local($Supersede, $Id, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail, $rFid);

    # lock system
    local( $lockResult ) = &cgi'lock( $LOCK_FILE );
    &Fatal(1001, '') if ( $lockResult == 2 );
    &Fatal(999, '') if ( $lockResult != 1 );
    # cash article DB
    if ( $BOARD ) { &DbCash( $BOARD ); }

    # ���Ϥ��줿��������
    $Supersede = $cgi'TAGS{'s'};
    $Id = $cgi'TAGS{'id'};
    $TextType = $cgi'TAGS{'texttype'};
    $Name = $cgi'TAGS{'name'};
    $Email = $cgi'TAGS{'mail'};
    $Url = $cgi'TAGS{'url'};
    $Icon = $cgi'TAGS{'icon'};
    $Subject = $cgi'TAGS{'subject'};
    $Article = $cgi'TAGS{'article'};
    $Fmail = $cgi'TAGS{'fmail'};
    if ($Id ne '') { ($rFid) = &GetArticlesInfo($Id); } else { $rFid = ''; }

    # ���Ϥ��줿��������Υ����å�
    $Article = &CheckArticle($BOARD, *Name, *Email, *Url, *Subject, *Icon, $Article);

    # ��ǧ���̤κ���
    &MsgHeader('Message preview', "$BOARDNAME: �񤭹��ߤ����Ƥ��ǧ���Ƥ�������");

    # ����«
    &cgiprint'Cache(<<__EOF__);
<form action="$PROGRAM" method="POST">
<input name="c"        type="hidden" value="x">
<input name="b"        type="hidden" value="$BOARD">
<input name="id"       type="hidden" value="$Id">
<input name="texttype" type="hidden" value="$TextType">
<input name="name"     type="hidden" value="$Name">
<input name="mail"     type="hidden" value="$Email">
<input name="url"      type="hidden" value="$Url">
<input name="icon"     type="hidden" value="$Icon">
<input name="subject"  type="hidden" value="$Subject">
<input name="article"  type="hidden" value="$Article">
<input name="fmail"    type="hidden" value="$Fmail">
<input name="s"        type="hidden" value="$Supersede">

__EOF__

    if ($Supersede && $SYS_F_D) {
	&cgiprint'Cache(<<__EOF__);
<p>
���$H_MESG���ؤ��ˡ�����$H_MESG��񤭹��ߤޤ���
ɬ�פǤ���С��֥饦����BACK�ܥ������äơ��񤭹��ߤ������Ƥ���������
�������Хܥ���򲡤����������ޤ��礦��
<input type="submit" value="�������ޤ�">
</p>
</form>
__EOF__
	&ViewOriginalArticle($Id, 0, 1);
	&cgiprint'Cache("<hr>\n");
    } else {
	&cgiprint'Cache(<<__EOF__);
<p>
ɬ�פǤ���С��֥饦����BACK�ܥ������äơ��񤭹��ߤ������Ƥ���������
�������Хܥ���򲡤��ƽ񤭹��ߤޤ��礦��
<input type="submit" value="��Ƥ���">
</p>
</form>
__EOF__
    }

    &cgiprint'Cache("<p>\n");

    # ��
    (($Icon eq $H_NOICON) || (! $Icon))
        ? &cgiprint'Cache("<strong>$H_SUBJECT</strong>: $Subject")
            : &cgiprint'Cache(sprintf("<strong>$H_SUBJECT</strong>: <img src=\"%s\" alt=\"$Icon \" width=\"$MSGICON_WIDTH\" height=\"$MSGICON_HEIGHT\">$Subject", &GetIconUrlFromTitle($Icon, $BOARD)));

    # ��̾��
    if ($Url ne '') {
        # URL��������
        &cgiprint'Cache("<br>\n<strong>$H_FROM</strong>: <a href=\"$Url\">$Name</a>");
    } else {
        # URL���ʤ����
        &cgiprint'Cache("<br>\n<strong>$H_FROM</strong>: $Name");
    }

    # �ᥤ��
    if ($Email ne '') {
	&cgiprint'Cache(" <a href=\"mailto:$Email\">&lt;$Email&gt;</a>");
    }

    # ȿ����(���Ѥξ��)
    if ($rFid) {
	if ($rFid ne '') {
	    &ShowLinksToFollowedArticle(($Id, split(/,/, $rFid)));
	} else {
	    &ShowLinksToFollowedArticle($Id);
	}
    }

    # �ڤ���
    &cgiprint'Cache("</p>\n$H_LINE\n");

    # TextType��������
    if ((! $SYS_TEXTTYPE) || ($TextType eq $H_PLAIN)) {
	&PlainArticleToHtml( *Article );
    }

    # ����
    $Article = &DQDecode($Article);
    $Article = &ArticleEncode($Article);
    &cgiprint'Cache("$Article\n");

    &MsgFooter;

    # unlock system
    &cgi'unlock( $LOCK_FILE );
}

1;
