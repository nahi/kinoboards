###
## Thanks - ��Ͽ����̤�ɽ��
#
# - SYNOPSIS
#	Thanks;
#
# - ARGS
#	�ʤ�
#
# - DESCRIPTION
#	�񤭹��߸�β��̤�ɽ������
#	����ѿ��Ǥ��롤CGI�ѿ��򻲾Ȥ��롥
#
# - RETURN
#	�ʤ�
#
Thanks: {

    local($Supersede, $Id, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail, $ArticleId);

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

    if ($Supersede && $SYS_F_D) {

	# �������� 
	&SupersedeArticle($BOARD, $Id, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail);

	# ɽ�����̤κ���
	&MsgHeader('Message superseded', "$BOARDNAME: $H_MESG����������ޤ���");

    } else {

	# �����κ���
	&MakeNewArticle($BOARD, $Id, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail);

	# ɽ�����̤κ���
	&MsgHeader('Message entried', "$BOARDNAME: �񤭹��ߤ��꤬�Ȥ��������ޤ���");

    }

    if ($Id ne '') {
	&cgiprint'Cache(<<__EOF__);
<form action="$PROGRAM" method="POST">
<input name="b" type="hidden" value="$BOARD">
<input name="c" type="hidden" value="e">
<input name="id" type="hidden" value="$Id">
<input type="submit" value="$H_ORIG��$H_MESG��">
</form>
__EOF__
    }

    &PrintButtonToTitleList($BOARD);
    &PrintButtonToBoardList;

    &MsgFooter;

}

1;
