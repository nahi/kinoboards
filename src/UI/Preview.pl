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
Preview:
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

    local( $rFid ) = '';
    ( $rFid ) = &GetArticlesInfo( $Id ) if ( $Id ne '' );

    # ���Ϥ��줿��������Υ����å�
    &CheckArticle( $BOARD, *Name, *Email, *Url, *Subject, *Icon, *Article );

    local( $eSubject ) = &DQEncode( $Subject );
    local( $eArticle ) = &DQEncode( $Article );

    &secureSubject( *Subject );
    &secureArticle( *Article, $TextType );

    # ��ǧ���̤κ���
    &MsgHeader( 'Message preview', "�񤭹��ߤ����Ƥ��ǧ���Ƥ�������" );

    local( %tags, $str, $msg );
    %tags = ( 'c', 'x', 'b', $BOARD, 'id', $Id, 'texttype', $TextType,
	     'name', $Name, 'mail', $Email, 'url', $Url, 'icon', $Icon,
	     'subject', $eSubject, 'article', $eArticle, 'fmail', $Fmail,
	     's', $Supersede, 'op', $op );

    if ( $Supersede && $SYS_F_D )
    {
	$msg =<<__EOF__;
<p>
���$H_MESG���ؤ��ˡ�����$H_MESG��񤭹��ߤޤ���
ɬ�פǤ���С��֥饦����BACK�ܥ������äơ��񤭹��ߤ������Ƥ���������
�������Хܥ���򲡤����������ޤ��礦��
</p>
__EOF__
	&TagForm( *str, *tags, "�������ޤ�", '', *msg );
	&cgiprint'Cache( $str );
	&ViewOriginalArticle( $Id, 0, 1 );
	&cgiprint'Cache( "$H_HR\n" );
    }
    else
    {
	$msg = <<__EOF__;
<p>
ɬ�פǤ���С��֥饦����BACK�ܥ������äơ��񤭹��ߤ������Ƥ���������
�������Хܥ���򲡤��ƽ񤭹��ߤޤ��礦��
</p>
__EOF__
	&TagForm( *str, *tags, "��Ƥ��ޤ�", '', *msg );
	&cgiprint'Cache( $str );
    }

    &cgiprint'Cache( "<p>\n" );

    # ��
    if (( $Icon eq $H_NOICON ) || ( !$Icon ))
    {
        &cgiprint'Cache( "<strong>$H_SUBJECT</strong>: $Subject" );
    }
    else
    {
	&cgiprint'Cache( "<strong>$H_SUBJECT</strong>: ", &TagMsgImg( &GetIconUrlFromTitle($Icon, $BOARD), "$Icon " ), $Subject );
    }

    # ��̾��
    if ( $Url ne '' )
    {
        # URL��������
        &cgiprint'Cache( "<br>\n<strong>$H_FROM</strong>: ", &TagA( $Url, $Name ));
    }
    else
    {
        # URL���ʤ����
        &cgiprint'Cache( "<br>\n<strong>$H_FROM</strong>: $Name" );
    }

    # �ᥤ��
    &cgiprint'Cache( " ", &TagA( "mailto:$Email", "&lt;$Email&gt;" ))
	if $Email;

    # ȿ����(���Ѥξ��)
    if ( $Id )
    {
	if ( $rFid )
	{
	    &ShowLinksToFollowedArticle(( $Id, split( /,/, $rFid )));
	}
	else
	{
	    &ShowLinksToFollowedArticle( $Id );
	}
    }

    # �ڤ���
    &cgiprint'Cache( "</p>\n$H_LINE\n" );

    # ����
    &cgiprint'Cache( "$Article\n" );
    &MsgFooter;

    # unlock system
    &cgi'unlock( $LOCK_FILE_B ) unless $PC;
    &cgi'unlock( $LOCK_FILE ) unless $PC;
}

1;
