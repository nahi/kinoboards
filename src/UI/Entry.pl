###
## Entry - �񤭹��߲��̤�ɽ��
#
# - SYNOPSIS
#	Entry($QuoteFlag);
#
# - ARGS
#	$QuoteFlag	0 ... ����
#			1 ... ���Ѥʤ��Υ�ץ饤
#			2 ... ���Ѥ���Υ�ץ饤
#
# - DESCRIPTION
#	�񤭹��߲��̤�ɽ������
#	����ѿ��Ǥ��롤CGI�ѿ��򻲾Ȥ��롥
#
# - RETURN
#	�ʤ�
#
Entry: {
    local($QuoteFlag) = $gVarQuoteFlag;
    local($Id, $Supersede, $IconTitle, $Key, $Value, $Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail, $DefSubject, $DefName, $DefEmail, $DefUrl, $DefFmail);

    $Id = $cgi'TAGS{'id'};
    $Supersede = $cgi'TAGS{'s'}; # ����?
    if ($QuoteFlag != 0) {
	($Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail) = &GetArticlesInfo($Id);
    }
    $Icon = $Icon || $H_NOICON;
    $DefSubject = ($Supersede ? $Subject : (($QuoteFlag == 0) ? '' : &GetReplySubject($Id)));
    $DefName = ($Supersede ? $Name : '');
    $DefEmail = ($Supersede ? $Email : '');
    $DefUrl = ($Supersede ? $Url : 'http://');
    $DefFmail = ($Supersede ? $Fmail : '');

    # ɽ�����̤κ���
    if ($Supersede && $SYS_F_D) {
	&MsgHeader('Supersede entry', "$BOARDNAME: $H_MESG������");
    } else {
	&MsgHeader('Message entry', "$BOARDNAME: $H_MESG�ν񤭹���");
    }

    # �ե����ξ��
    if ($QuoteFlag != 0) {
	# ������ɽ��(���ޥ��̵��, ����������)
	&ViewOriginalArticle($Id, 0, 1);
	if ($Supersede && $SYS_F_D) {
	    &cgiprint'Cache("<hr>\n<h2>���$H_MESG����������</h2>");
	} else {
	    &cgiprint'Cache("<hr>\n<h2>���$H_MESG�ؤ�$H_REPLY��񤭹���</h2>");
	}
    }

    # ����«
    &cgiprint'Cache(<<__EOF__);
<form action="$PROGRAM" method="POST">
<input name="c" type="hidden" value="p">
<input name="b" type="hidden" value="$BOARD">
<input name="id" type="hidden" value="$Id">
<input name="s" type="hidden" value="$Supersede">
<p>
__EOF__
    if ($Supersede && $SYS_F_D) {
	&cgiprint'Cache(<<__EOF__);
���$H_MESG�����촹����$H_MESG��񤭹���Ǥ���������
__EOF__
    } else {
	&cgiprint'Cache(<<__EOF__);
$H_SUBJECT��$H_MESG��$H_FROM��$H_MAIL������˥����֥ڡ����򤪻��������ϡ�
�ۡ���ڡ�����$H_URL��񤭹���Ǥ�������(�����󡤤ʤ��Ƥ⹽���ޤ���)��
__EOF__
    }

    # HTML�Ǥ�񤱤���
    if ($SYS_TEXTTYPE) {
	&cgiprint'Cache(<<__EOF__);
HTML��¸�������ϡ���$H_TEXTTYPE�פ��$H_HTML�פˤ��ơ�
$H_MESG��HTML�Ȥ��ƽ񤤤�ĺ���ȡ�ɽ���λ���HTML������Ԥʤ��ޤ���
__EOF__
    }

    &cgiprint'Cache(<<__EOF__);
</p>
<p>
$H_BOARD: $BOARDNAME<br>
__EOF__

    # �������������
    if ($SYS_ICON) {
	&CashIconDb($BOARD);	# ��������DB�򥭥�å���
	&cgiprint'Cache("$H_ICON:\n<SELECT NAME=\"icon\">\n<OPTION SELECTED>$H_NOICON\n");
	foreach $IconTitle (sort keys(%ICON_FILE)) {
	    &cgiprint'Cache("<OPTION>$IconTitle\n");
	}
	&cgiprint'Cache("</SELECT>\n");

	&cgiprint'Cache("(<a href=\"$PROGRAM?b=$BOARD&c=i&type=entry\">�������������</a>)<BR>\n");

    }

    # Subject(�ե����ʤ鼫ưŪ��ʸ����������)
    &cgiprint'Cache(sprintf("%s: <input name=\"subject\" type=\"text\" value=\"%s\" size=\"%s\"><br>\n", $H_SUBJECT, $DefSubject, $SUBJECT_LENGTH));

    # TextType
    if ($SYS_TEXTTYPE) {
	&cgiprint'Cache(<<__EOF__);
$H_TEXTTYPE:
<SELECT NAME="texttype">
<OPTION SELECTED>$H_PRE
<OPTION>$H_HTML
</SELECT>
</p>
__EOF__

    }

    # ��ʸ(���Ѥ���ʤ鸵����������)
    &cgiprint'Cache("<p><textarea name=\"article\" rows=\"$TEXT_ROWS\" cols=\"$TEXT_COLS\">");
    if ($Supersede && $SYS_F_D) {
	&QuoteOriginalArticleWithoutQMark($Id);
    } elsif ($QuoteFlag == 2) {
	&QuoteOriginalArticle($Id);
    }

    &cgiprint'Cache("</textarea></p>\n");

    # �եå���ʬ��ɽ��
    # ̾���ȥᥤ�륢�ɥ쥹��URL��
    &cgiprint'Cache(<<__EOF__);
<p>
$H_MESG��˴�Ϣ�����֥ڡ����ؤΥ�󥯤�ĥ����ϡ�
��&lt;URL:http://��&gt;�פΤ褦�ˡ�URL���&lt;URL:�פȡ�&gt;�פǰϤ��
�񤭹���Ǥ�����������ưŪ�˥�󥯤�ĥ���ޤ���
</p>
__EOF__

    if ($SYS_ALIAS == 0) {

	# �����ꥢ���ϻȤ�ʤ�
	&cgiprint'Cache(<<__EOF__);
<p>
$H_FROM: <input name="name" type="text" value="$DefName" size="$NAME_LENGTH"><br>
$H_MAIL: <input name="mail" type="text" value="$DefEmail" size="$MAIL_LENGTH"><br>
$H_URL_S: <input name="url" type="text" value="$DefUrl" size="$URL_LENGTH"><br>
</p>
__EOF__

    } elsif ($SYS_ALIAS == 1) {

	# �����ꥢ����Ȥ�
	&cgiprint'Cache(<<__EOF__);
<p>
$H_FROM: <input name="name" type="text" value="$DefName" size="$NAME_LENGTH"><br>
$H_MAIL: <input name="mail" type="text" value="$DefEmail" size="$MAIL_LENGTH"><br>
$H_URL_S: <input name="url" type="text" value="$DefUrl" size="$URL_LENGTH">
</p>
__EOF__

	&cgiprint'Cache(<<__EOF__);
<p>
��$H_ALIAS�פˡ�$H_FROM��$H_MAIL��$H_URL����Ͽ�ʤ��äƤ������ϡ�
��$H_FROM�פˡ�#...�פȤ�����Ͽ̾��񤤤Ƥ���������
��ưŪ��$H_FROM��$H_MAIL��$H_URL������ޤ���
(<a href="$PROGRAM?c=as">$H_ALIAS�ΰ���</a> //
 <a href="$PROGRAM?c=an">$H_ALIAS����Ͽ</a>)
</p>
__EOF__

    } else {

	# �����ꥢ������Ͽ���ʤ���н񤭹��ߤǤ��ʤ�

	# �����ꥢ�����ɤ߹���
	&CashAliasData;

	&cgiprint'Cache(<<__EOF__);
<p>
$H_USER:
<SELECT NAME="name">
<OPTION SELECTED>$H_FROM����Ͽ����$H_ALIAS������Ǥ�������
__EOF__

	while (($Key, $Value) = each %Name) {
	    &cgiprint'Cache("<OPTION>$Key\n");
	}
	&cgiprint'Cache(<<__EOF__);
</SELECT>
</p>
__EOF__

	&cgiprint'Cache(<<__EOF__);
<p>
ͽ���$H_ALIAS�פˡ�$H_FROM��$H_MAIL��$H_URL����Ͽ���ʤ��Ƚ񤭹���ޤ���
��Ͽ�����塤��#...�פȤ�����Ͽ̾����ꤷ�Ƥ���������
(<a href="$PROGRAM?c=as">$H_ALIAS�ΰ���</a> //
 <a href="$PROGRAM?c=an">$H_ALIAS����Ͽ</a>)<br>
��Ͽ����$H_ALIAS��ɽ������ʤ�(����Ǥ��ʤ�)��硤
���Υڡ�������ɤ߹��ߤ��Ƥ���������
</p>
__EOF__

    }

    if ($SYS_MAIL) {
	&cgiprint'Cache("<p>$H_REPLY�����ä����˥ᥤ����Τ餻�ޤ���? <input name=\"fmail\" type=\"checkbox\" value=\"on\"></p>\n");
    }
    
    # �ܥ���
    &cgiprint'Cache(<<__EOF__);
<p>
�񤭹�������Ƥ�<br>
<input type="radio" name="com" value="p" CHECKED>: ���ɽ�����Ƥߤ�(�ޤ���Ƥ��ޤ���)<br>
__EOF__

    if ($Supersede && $SYS_F_D) {
	&cgiprint'Cache("<input type=\"radio\" name=\"com\" value=\"x\">: �������ޤ�<br>\n");
    } else {
	&cgiprint'Cache("<input type=\"radio\" name=\"com\" value=\"x\">: $H_MESG����Ƥ���<br>\n");
    }

    &cgiprint'Cache(<<__EOF__);
<input type="submit" value="�¹�">
</p>
</form>
__EOF__

    &MsgFooter;

}

1;
