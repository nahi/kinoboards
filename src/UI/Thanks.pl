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
require( 'mimer.pl' );
Thanks:
{
    local( $previewFlag ) = $gVarPreviewFlag;

    &LockAll;
    &LockBoard;

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
    # ����Ⱦ���δ֤��������줿�ե����फ�餷����Ƥ���Ĥ��ʤ���
    if ( $SYS_DENY_FORM_OLD && (( $op == 0 ) || ( $base - $op > .5 ) || ( $op > $base )))
    {
	&Fatal( 15, '' );
    }

    $Article = &MIME'base64decode( $Article ) if $previewFlag;

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
	$newArtId = &SupersedeArticle( $BOARD, $Id, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail );

	# ɽ�����̤κ���
	&MsgHeader( 'Message superseded', "$H_MESG����������ޤ���" );
    }
    else
    {
	# �����κ���
	$newArtId = &MakeNewArticle( $BOARD, $Id, $op, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail, 1 );

	# ɽ�����̤κ���
	&MsgHeader( 'Message entried', "�񤭹��ߤ��꤬�Ȥ��������ޤ���" );
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
	&cgiprint'Cache( "<p>", &TagA( "$PROGRAM?b=$BOARD&c=e&id=$newArtId", "�񤭹����$H_MESG��" ), "</p>\n" );
    }

    if ( !$Supersede && ( $Id ne '' ))
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
	    &cgiprint'Cache( "<p>", &TagA( "$PROGRAM?b=$BOARD&c=e&id=$Id", "$H_ORIG��$H_MESG��" ), "</p>\n" );
	}
    }

    &PrintButtonToTitleList( $BOARD, $newArtId );
    &PrintButtonToBoardList if $SYS_F_B;

    &MsgFooter;

    &UnlockBoard;
    &UnlockAll;
}

1;
