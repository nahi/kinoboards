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
Thanks:
{
    # lock system
    local( $lockResult ) = $PC ? 1 : &cgi'lock( $LOCK_FILE );
    &Fatal( 1001, '' ) if ( $lockResult == 2 );
    &Fatal( 999, '' ) if ( $lockResult != 1 );
    # lock system
    $lockResult = $PC ? 1 : &cgi'lock( $LOCK_FILE_B );
    &Fatal( 1001, '' ) if ( $lockResult == 2 );
    &Fatal( 999, '' ) if ( $lockResult != 1 );

    # cache article DB
    &DbCache( $BOARD ) if $BOARD;
    
    # ���Ϥ��줿��������
    local( $Name ) = $cgi'TAGS{'name'};
    local( $Email ) = $cgi'TAGS{'mail'};
    local( $Url ) = $cgi'TAGS{'url'};
    local( $Supersede ) = $cgi'TAGS{'s'};
    local( $Id ) = $cgi'TAGS{'id'};
    local( $TextType ) = $cgi'TAGS{'texttype'};
    local( $Icon ) = $cgi'TAGS{'icon'};
    local( $Subject ) = $cgi'TAGS{'subject'};
    local( $Article ) = $cgi'TAGS{'article'};
    local( $Fmail ) = $cgi'TAGS{'fmail'};
    local( $op ) = $cgi'TAGS{'op'};

    local( $base ) = ( -M $BOARD_ALIAS_FILE );
    if (( $op == 0 ) || ( $base - $op > 1 ) || ( $op > $base ))
    {
	&Fatal( 15, '' );
    }

    if ( $SYS_DENY_FORM_RECYCLE )
    {
	local( $dId, $dKey );
	&GetArticleId( $BOARD, *dId, *dKey );
	&Fatal( 16, '' ) if ( $dKey && ( $dKey == $op ));
    }

    # Preview��ͳ��Encode����Ƥ��뤫�⤷��ʤ�
    $Article = &DQDecode( $Article );
    $Subject = &DQDecode( $Subject );

    &secureSubject( *Subject );
    &secureArticle( *Article, $TextType );

    local( $newArtId );
    if ( $Supersede && $SYS_F_D )
    {
	# �������� 
	$newArtId = &SupersedeArticle($BOARD, $Id, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail);

	# ɽ�����̤κ���
	&MsgHeader('Message superseded', "$H_MESG����������ޤ���");
    }
    else
    {
	# �����κ���
	$newArtId = &MakeNewArticle($BOARD, $Id, $op, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail);

	# ɽ�����̤κ���
	&MsgHeader('Message entried', "�񤭹��ߤ��꤬�Ȥ��������ޤ���");
    }

    if  ( $SYS_COMMAND_BUTTON )
    {
	local( %tags ) = ( 'b', $BOARD, 'c', 'e', 'id', $newArtId );
	local( $str );
	&TagForm( *str, *tags, "�񤭹����$H_MESG��", '', '' );
	&cgiprint'Cache( $str );
    }
    else
    {
	&cgiprint'Cache( "<p><a href=\"$PROGRAM?b=$BOARD&c=e&id=$newArtId\">�񤭹����$H_MESG��</a></p>\n" );
    }

    if ( $Id ne '' )
    {
	if  ( $SYS_COMMAND_BUTTON )
	{
	    local( %tags ) = ( 'b', $BOARD, 'c', 'e', 'id', $Id );
	    local( $str ) = '';
	    &TagForm( *str, *tags, "$H_ORIG��$H_MESG��", '', '' );
	    &cgiprint'Cache( $str );
	}
	else
	{
	    &cgiprint'Cache( "<p><a href=\"$PROGRAM?b=$BOARD&c=e&id=$Id\">$H_ORIG��$H_MESG��</a></p>\n" );
	}
    }

    &PrintButtonToTitleList( $BOARD );
    &PrintButtonToBoardList if $SYS_F_B;

    &MsgFooter;

    # unlock system
    &cgi'unlock( $LOCK_FILE_B ) unless $PC;
    &cgi'unlock( $LOCK_FILE ) unless $PC;
}

1;
