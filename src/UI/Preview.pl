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
require( 'mimew.pl' );
Preview:
{
    &LockAll();

    # cache article DB
    &DbCache( $BOARD ) if $BOARD;

    # ���Ϥ��줿��������
    local( $COrig ) = $cgi'TAGS{'corig'};
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

    local( $eSubject ) = &MIME'base64encode( $Subject );
    local( $eArticle ) = &MIME'base64encode( $Article );

    &secureSubject( *Subject );
    &secureArticle( *Article, $TextType );

    # ��ǧ���̤κ���
    &MsgHeader( 'Message preview', "�񤭹��ߤ����Ƥ��ǧ���Ƥ�������" );

    if ( $Supersede && $SYS_F_D )
    {
	&cgiprint'Cache(<<__EOF__);
<p>
���$H_MESG���ؤ��ˡ�����$H_MESG��񤭹��ߤޤ���
ɬ�פǤ���н񤭹��ߥե��������äƽ������Ƥ���������
�������Хܥ���򲡤����������ޤ��礦��
</p>
__EOF__
    }
    else
    {
	&cgiprint'Cache(<<__EOF__);
<p>
$H_MESG������å�����ɬ�פʤ�񤭹��ߥե��������äƽ������Ƥ���������
�������Хܥ���򲡤��ƽ񤭹��ߤޤ��礦��
</p>
__EOF__
    }

    # �ܥ���
    local( %tags, $str, $msg );
    $msg = <<__EOF__;
<input type="radio" name="com" value="e">: ��äƽ�������<br>
__EOF__

    if ( $Supersede && $SYS_F_D )
    {
	$msg .= "<input type=\"radio\" name=\"com\" value=\"x\" CHECKED>: ��������<br>\n";
    }
    else
    {
	$msg .= "<input type=\"radio\" name=\"com\" value=\"x\" CHECKED>: $H_MESG����Ƥ���<br>\n";
    }

    %tags = ( 'corig', $COrig, 'c', 'x', 'b', $BOARD, 'id', $Id,
	     'texttype', $TextType,
	     'name', ( $SYS_ALIAS == 2 )? $cgi'TAGS{'name'} : $Name,
	     'mail', $Email, 'url', $Url, 'icon', $Icon, 'subject', $eSubject,
	     'article', $eArticle, 'fmail', $Fmail, 's', $Supersede,
	     'op', $op );

    &TagForm( *str, *tags, "�¹�", '', *msg );
    &cgiprint'Cache( $str );

    if ( $Supersede && $SYS_F_D )
    {
	&cgiprint'Cache( "$H_HR\n" );
	&ViewOriginalArticle( $Id, 0, 1 );
    }

    &cgiprint'Cache( "$H_HR\n<p>\n" );

    # ��
    &cgiprint'Cache( "<strong>$H_SUBJECT</strong>: ", &TagMsgImg( $Icon ),
	$Subject );

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
	local( $msg );
	if ( $rFid )
	{
	    &ShowLinksToFollowedArticle( *msg, ( $Id, split( /,/, $rFid )));
	}
	else
	{
	    &ShowLinksToFollowedArticle( *msg, $Id );
	}
	&cgiprint'Cache( $msg );
    }

    # �ڤ���
    &cgiprint'Cache( "</p>\n$H_LINE\n" );

    # ����
    &cgiprint'Cache( "$Article\n" );

    &MsgFooter;

    &UnlockAll();
}

1;
