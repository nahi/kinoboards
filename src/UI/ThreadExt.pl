###
## ThreadExt - ����å��̥����ȥ뤪��ӵ�������
#
# - SYNOPSIS
#	ThreadExt;
#
# - ARGS
#	�ʤ�
#
# - DESCRIPTION
#	�����򥹥�å��̤˥����Ȥ���ɽ������
#	���θ��˥���åɽ�˵�����ɽ�����롥
#	����ѿ��Ǥ��롤CGI�ѿ��򻲾Ȥ��롥
#	����ѿ�ADDFLAG(����ɽ�����Ƥ��ޤä����ݤ���ɽ�魯�ե饰)���˲����롥
#
# - RETURN
#	�ʤ�
#
ThreadExt:
{
    %ADDFLAG = ();		# these are static.
    @IDLIST = ();

    &LockBoard();
    &DbCache( $BOARD ) if $BOARD;
    &UnlockBoard();

    # ɽ������Ŀ������
    local( $Num ) = $cgi'TAGS{'num'};
    local( $Old );
    if ( defined( $cgi'TAGS{'id'} ))
    {
	$Old = $#DB_ID - int( $cgi'TAGS{'id'} + $Num/2 );
	$Old = 0 if ( $Old < 0 );
    }
    else
    {
	$Old = $cgi'TAGS{'old'};
    }
    local( $Rev ) = $cgi'TAGS{'rev'};
    local( $vRev ) = $Rev? 1-$SYS_BOTTOMTITLE : $SYS_BOTTOMTITLE;
    local( $To ) = $#DB_ID - $Old;
    local( $From )= $To - $Num + 1;
    $From = 0 if (( $From < 0 ) || ( $Num == 0 ));

    local( $pageLinkStr ) = &PageLink( 'vt', $Num, $Old, $Rev );

    # �����Ѥߥե饰
    # 0 ... �����оݳ�
    # 1 ... �����Ѥ�
    # 2 ... ̤����
    local( $IdNum, $Id );
    for ( $IdNum = $From; $IdNum <= $To; $IdNum++ )
    {
	$ADDFLAG{$DB_ID[$IdNum]} = 2;
    }

    # ɽ�����̤κ���
    &MsgHeader( 'Thread extension view', "$H_SUBJECT�����$H_MESG����($H_REPLY��)" );

    &BoardHeader();
    &cgiprint'Cache("$H_HR\n");
    &cgiprint'Cache( $pageLinkStr );

    local( $AddNum ) = "&num=$Num&old=$Old&rev=$Rev";

    if ($To < $From)
    {
	# �����ä��ġ�
	&cgiprint'Cache("<ul>\n<li>$H_NOARTICLE\n</ul>\n");
    }
    elsif ( $vRev )
    {
	for( $IdNum = $From; $IdNum <= $To; $IdNum++ )
	{
	    # ����������ID����Ф�
	    $Id = $DB_ID[$IdNum];
	    ( $Fid = $DB_FID{ $Id } ) =~ s/,.*$//o;
	    # �������Ȥϸ�󤷡�
#	    next if ((( $Fid ne '' ) && ( $SYS_THREAD_FORMAT == 2 )) || ( $ADDFLAG{$Fid} == 2 ));
	    next if (( $Fid ne '' ) && (( $ADDFLAG{$Fid} == 2 ) || ( $SYS_THREAD_FORMAT == 2 )));

	    # �Ρ��ɤ�ɽ��
	    &cgiprint'Cache( "<ul>\n" );
	    if ( $SYS_THREAD_FORMAT == 1 )
	    {
		&ThreadTitleNodeAllThread( $Id, 1 );
	    }
	    elsif ( $SYS_THREAD_FORMAT == 2 )
	    {
		&ThreadTitleNodeNoThread( $Id, 1 );
	    }
	    else
	    {
		&ThreadTitleNodeThread( $Id, 1 );
	    }
	    &cgiprint'Cache( "</ul>\n" );
	}
    }
    else
    {
	for( $IdNum = $To; $IdNum >= $From; $IdNum-- )
	{
	    $Id = $DB_ID[$IdNum];
	    ( $Fid = $DB_FID{ $Id } ) =~ s/,.*$//o;
#	    next if ((( $Fid ne '' ) && ( $SYS_THREAD_FORMAT == 2 )) || ( $ADDFLAG{$Fid} == 2 ));
	    next if (( $Fid ne '' ) && (( $ADDFLAG{$Fid} == 2 ) || ( $SYS_THREAD_FORMAT == 2 )));

	    &cgiprint'Cache( "<ul>\n" );
	    if ( $SYS_THREAD_FORMAT == 1 )
	    {
		&ThreadTitleNodeAllThread( $Id, 1 );
	    }
	    elsif ( $SYS_THREAD_FORMAT == 2 )
	    {
		&ThreadTitleNodeNoThread( $Id, 1 );
	    }
	    else
	    {
		&ThreadTitleNodeThread( $Id, 1 );
	    }
	    &cgiprint'Cache( "</ul>\n" );
	}
    }

    if ( $#IDLIST >= 0 )
    {
	&cgiprint'Cache( "$H_HR\n" );

	while ( $Id = shift( @IDLIST ))
	{
	    &ViewOriginalArticle( $Id, $SYS_COMMAND_EACH, 1 );
	    &cgiprint'Cache( "$H_HR\n" );
	}
    }

    &cgiprint'Cache( $pageLinkStr );

    &MsgFooter;

    undef( %ADDFLAG );
    undef( @IDLIST );
}


###
## ����Ρ��ɤΤ�ɽ��
#
sub ThreadTitleNodeNoThread
{
    local( $Id ) = @_;

    &cgiprint'Cache( '<li>', &GetFormattedTitle( $Id, $DB_AIDS{$Id}, $DB_ICON{$Id}, $DB_TITLE{$Id}, $DB_NAME{$Id}, $DB_DATE{$Id}, 3 ), "\n");
    push( @IDLIST, $Id );
}


###
## �ڡ����⥹��åɤΤ�ɽ��
#
sub ThreadTitleNodeThread
{
    local( $Id, $top ) = @_;

    # �ڡ������ʤ餪���ޤ���
    return if ( $ADDFLAG{$Id} != 2 );

    &cgiprint'Cache( '<li>', &GetFormattedTitle($Id, $DB_AIDS{$Id}, $DB_ICON{$Id}, $DB_TITLE{$Id}, $DB_NAME{$Id}, $DB_DATE{$Id}, $top|2 ), "\n" );
    $ADDFLAG{$Id} = 1;		# �����Ѥ�
    push( @IDLIST, $Id );

    # ̼�����Сġ�
    if ( $DB_AIDS{$Id} )
    {
	&cgiprint'Cache( "<ul>\n" );
	grep( &ThreadTitleNodeThread( $_, 0 ), split( /,/, $DB_AIDS{$Id} ));
	&cgiprint'Cache( "</ul>\n" );
    }
}


###
## ������åɤ�ɽ��
#
sub ThreadTitleNodeAllThread
{
    local( $Id, $top ) = @_;

    # ɽ���Ѥߤʤ餪���ޤ���
    return if ( $ADDFLAG{$Id} == 1 );

    &cgiprint'Cache( '<li>', &GetFormattedTitle($Id, $DB_AIDS{$Id}, $DB_ICON{$Id}, $DB_TITLE{$Id}, $DB_NAME{$Id}, $DB_DATE{$Id}, $top|2 ), "\n" );
    $ADDFLAG{$Id} = 1;		# �����Ѥ�
    push( @IDLIST, $Id );

    # ̼�����Сġ�
    if ( $DB_AIDS{$Id} )
    {
	&cgiprint'Cache( "<ul>\n" );
	grep( &ThreadTitleNodeAllThread( $_, 0 ), split( /,/, $DB_AIDS{$Id} ));
	&cgiprint'Cache( "</ul>\n" );
    }
}


1;
