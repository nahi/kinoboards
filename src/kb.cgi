#!/usr/local/bin/perl


# ���Υե�������ѹ���2�ս�Ǥ���
#
# 1. ������Ƭ�Ԥǡ�Perl�Υѥ�����ꤷ�ޤ�����#!�פ�³���ƻ��ꤷ�Ƥ���������

# 2. �����Ф�IIS�ξ�硤�ѥå�������Ÿ������Ĺ���ƤǤ���
#    kb�ǥ��쥯�ȥ�Υե�ѥ�����ꤷ�Ƥ���������
#    �����Ф�IIS�Ǥʤ���С�������������פǤ���
#
$IIS_TRANSLATED_PATH = '';
# $IIS_TRANSLATED_PATH = 'd:\inetpub\wwwroot\kb';

# 3. �����Ф�ư���Ƥ���ޥ���Win95�⤷����Mac�ξ�硤
#    $PC��1�����ꤷ�Ƥ��������������Ǥʤ���硤������������פǤ���
#
$PC = 0;	# for UNIX / WinNT
# $PC = 1;	# for Win95 / Mac


# �ʲ��Ͻ񤭴�����ɬ�פϤ���ޤ���


######################################################################


# $Id: kb.cgi,v 5.16 1998-11-05 18:28:12 nakahiro Exp $

# KINOBOARDS: Kinoboards Is Network Opened BOARD System
# Copyright (C) 1995-98 NAKAMURA Hiroshi.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PRATICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

# This file implements main functions of KINOBOARDS.

# perl������
$[ = 0;				# zero origined
$| = 1;				# pipe flushed
$COLSEP = "\376";
# umask���ä����ꤷ�ʤ�������θ��ʤΤǡ�����
# umask( umask() | 070 );	# �桼����nobody���̥��롼�פξ��
# umask( umask() | 007 );	# �桼����nobody��Ʊ���롼�פξ��

# ����ѿ������
$HEADER_FILE = 'kb.ph';		# header file
$KB_VERSION = '1.0';		# version
$KB_RELEASE = '6.1';		# release
$MACPERL = ( $^O eq 'MacOS' );  # isMacPerl?

# �ǥ��쥯�ȥ�
$ICON_DIR = 'icons';				# ��������ǥ��쥯�ȥ�
$UI_DIR = 'UI';					# UI�ǥ��쥯�ȥ�

# �ե�����
$BOARD_ALIAS_FILE = 'kinoboards';		# �Ǽ���DB
$CONF_FILE_NAME = 'kb.conf';			# �Ǽ�����configuratin�ե�����
$ARRIVEMAIL_FILE_NAME = 'kb.mail';		# �Ǽ����̿����ᥤ��������DB
$BOARD_FILE_NAME = 'kb.board';			# �����ȥ�ꥹ�ȥإå�DB
$DB_FILE_NAME = 'kb.db';			# ����DB
$ARTICLE_NUM_FILE_NAME = 'kb.aid';		# �����ֹ�DB
$USER_ALIAS_FILE = 'kinousers';			# �桼�������ꥢ����DB
$DEFAULT_ICONDEF = 'all.idef';			# ��������DB
$LOCK_FILE = 'kb.lock';				# ��å��ե�����
$LOCK_FILE_B = '';				# �Ǽ����̥�å��ե�����
$LOGFILE = 'kb.klg';				# ���ե�����
# Suffix
$TMPFILE_SUFFIX = 'tmp';			# DB�ƥ�ݥ��ե������Suffix
$ICONDEF_POSTFIX = 'idef';			# ��������DB�ե������Suffix

# �إå��ե�������ɤ߹���
require( $HEADER_FILE ) if ( -s "$HEADER_FILE" );

# �ɲåإå��ե�������ɤ߹���
$PATH_TRANSLATED = $IIS_TRANSLATED_PATH || $ENV{'PATH_TRANSLATED'};
if ( $PATH_TRANSLATED ne '' )
{
    die( "cannot chdir to `$PATH_TRANSLATED'" )
	if ( !chdir( $PATH_TRANSLATED ));
    require( $HEADER_FILE ) if ( -s "$HEADER_FILE" );
    # ���require�Ѥߤξ����ɤޤʤ���Perl�θ�����͡�
}

# ���󥯥롼�ɥե�������ɤ߹���
require( 'cgi.pl' );
require( 'kinologue.pl' );
$PROGNAME = $cgi'CGIPROG_NAME;
$PROGRAM = $cgi'PROGRAM;
$kinologue'SEV_THRESHOLD = $kinologue'SEV_WARN;

$cgi'SMTP_SERVER = $SMTP_SERVER;
$cgi'AF_INET = $AF_INET;
$cgi'SOCK_STREAM = $SOCK_STREAM;
$cgi'CHARSET = $CHARSET;
@cgi'TAG_ALLOWED = ( 'article', 'subject', 'key' );
$FF_LOG = ( $SYS_LOG == 1 ) ? $kinologue'FF_HTML : $kinologue'FF_PLAIN;
$SYS_F_MT = ($SYS_F_D || $SYS_F_AM || $SYS_F_MV);
if (( $cgi'SERVER_PORT != 80 ) && ( $SYS_PORTNO == 1 ))
{
    $SERVER_PORT_STRING = ":$cgi'SERVER_PORT";
}
else
{
    $SERVER_PORT_STRING = '';
}
$SCRIPT_URL = "http://$cgi'SERVER_NAME$SERVER_PORT_STRING$cgi'SCRIPT_NAME$cgi'PATH_INFO";
$BASE_URL = "http://$cgi'SERVER_NAME$SERVER_PORT_STRING$cgi'SYSDIR_NAME";
if ( $TIME_ZONE ) { $ENV{'TZ'} = $TIME_ZONE; }

# ��������ե���������URL
$ICON_BLIST = "$ICON_DIR/blist.gif";		# �Ǽ��İ�����
$ICON_TLIST = "$ICON_DIR/tlist.gif";		# �����ȥ������
$ICON_PREV = "$ICON_DIR/prev.gif";		# ���ε�����
$ICON_NEXT = "$ICON_DIR/next.gif";		# ���ε�����
$ICON_WRITENEW = "$ICON_DIR/writenew.gif";	# �����񤭹���
$ICON_FOLLOW = "$ICON_DIR/follow.gif";		# ��ץ饤
$ICON_QUOTE = "$ICON_DIR/quote.gif";		# ���Ѥ��ƥ�ץ饤
$ICON_THREAD = "$ICON_DIR/thread.gif";		# �ޤȤ��ɤ�
$ICON_HELP = "$ICON_DIR/help.gif";		# �إ��
$ICON_DELETE = "$ICON_DIR/delete.gif";		# ���
$ICON_SUPERSEDE = "$ICON_DIR/supersede.gif";	# ����
$ICON_NEW = "$ICON_DIR/listnew.gif";		# ����

# �����ʥ�ϥ�ɥ�
$SIG{'QUIT'} = 'IGNORE';
$SIG{'INT'} = $SIG{'HUP'} = $SIG{'TERM'} = $SIG{'TSTP'} = 'DoKill';
sub DoKill
{
    local( $sig ) = @_;
    if ( !$PC )
    {
	&cgi'unlock( $LOCK_FILE );
	&cgi'unlock( $LOCK_FILE_B ) if $LOCK_FILE_B;
    }
    &KbLog( $kinologue'SEV_WARN, "Caught a SIG$sig - shutting down..." );
    exit( 1 );
}


######################################################################


###
## MAIN - �ᥤ��֥�å�
#
# - SYNOPSIS
#	kb.cgi
#
# - ARGS
#	�ʤ�
#
# - DESCRIPTION
#	��ư���˰��٤������Ȥ���롥
#	�������Ϥʤ������Ķ��ѿ�QUERY_STRING��REQUEST_METHOD��
#	�⤷����ɸ�����Ϸ�ͳ���ͤ��Ϥ��ʤ��ȡ�������ư��ʤ���
#
# - RETURN
#	�ʤ�
#
MAIN:
{
    local( $boardConfFileP, $c, $com );

    &cgi'Decode();
    $c = $cgi'TAGS{'c'};
    $com = $cgi'TAGS{'com'};
    $BOARD = $cgi'TAGS{'b'};
    if ( $c eq '' ) { $c = 'v'; $BOARD = 'test'; }
    if ( $BOARD )
    {
	( $BOARDNAME, $boardConfFileP ) = &GetBoardInfo( $BOARD );
	$LOCK_FILE_B = $LOCK_FILE . ".$BOARD";
    }

    # �Ǽ��ĸ�ͭ���åƥ��󥰤��ɤ߹���
    if ( $boardConfFileP )
    {
	local( $boardConfFile ) = &GetPath( $BOARD, $CONF_FILE_NAME );
	eval( "require( \"$boardConfFile\" );" ) || &Fatal( 1, $boardConfFile );
    }
    if ( $BOARDLIST_URL eq '-' ) { $BOARDLIST_URL = "$PROGRAM?c=bl"; }

    if ( $c eq 'e' )
    {
	### ShowArticle - ñ�쵭����ɽ��
	require( &GetPath( $UI_DIR, 'ShowArticle.pl' ));
	last;
    }
    elsif ( $SYS_F_T && ( $c eq 't' ))
    {
	### ThreadArticle - �ե�������������ɽ����
	require( &GetPath( $UI_DIR, 'ThreadArticle.pl' ));
	last;
    }

    if ( $SYS_F_N )
    {
	if ( $c eq 'n' )
	{
	    ### Entry - �񤭹��߲��̤�ɽ��
	    $gVarQuoteFlag = 0;
	    require( &GetPath( $UI_DIR, 'Entry.pl' ));
	    last;
	}
	elsif ( $c eq 'f' )
	{
	    $gVarQuoteFlag = 1;
	    require( &GetPath( $UI_DIR, 'Entry.pl' ));
	    last;
	}
	elsif ( $c eq 'q' )
	{
	    $gVarQuoteFlag = 2;
	    require( &GetPath( $UI_DIR, 'Entry.pl' ));
	    last;
	}
	elsif (( $c eq 'p' ) && ( $com ne 'x' ))
	{
	    ### Preview - �ץ�ӥ塼���̤�ɽ��
	    require( &GetPath( $UI_DIR, 'Preview.pl' ));
	    last;
	}
	elsif (( $c eq 'x' ) || (( $c eq 'p' ) && ( $com eq 'x' )))
	{
	    ### Thanks - ��Ͽ����̤�ɽ��
	    require( &GetPath( $UI_DIR, 'Thanks.pl' ));
	    last;
	}
    }

    if ( $c eq 'v' )
    {
	### ViewTitle - ����å���ɽ��
	$gVarComType = 0;
	require( &GetPath( $UI_DIR, 'ViewTitle.pl' ));
	last;
    }
    elsif ( $SYS_F_R && ( $c eq 'r' ))
    {
	### SortArticle - ���ս�˥�����
	require( &GetPath( $UI_DIR, 'SortArticle.pl' ));
	last;
    }
    elsif ( $SYS_F_L && ( $c eq 'l' ))
    {
	### NewArticle - ������������ޤȤ��ɽ��
	require( &GetPath( $UI_DIR, 'NewArticle.pl' ));
	last;
    }
    elsif ( $SYS_F_S && ( $c eq 's' ))
    {
	### SearchArticle - �����θ���(ɽ�����̤κ���)
	require( &GetPath( $UI_DIR, 'SearchArticle.pl' ));
	last;
    }
    elsif ( $c eq 'i' )
    {
	### ShowIcon - ��������ɽ������
	require( &GetPath( $UI_DIR, 'ShowIcon.pl' ));
	last;
    }

    if ( $SYS_ALIAS )
    {
	if ( $c eq 'an' )
	{
	    ### AliasNew - �����ꥢ������Ͽ���ѹ����̤�ɽ��
	    require( &GetPath( $UI_DIR, 'AliasNew.pl' ));
	    last;
	}
	elsif ( $c eq 'am' )
	{
	    ### AliasMod - �桼�������ꥢ������Ͽ/�ѹ�
	    require( &GetPath( $UI_DIR, 'AliasMod.pl' ));
	    last;
	}
	elsif ( $c eq 'ad' )
	{
	    ### AliasDel - �桼�������ꥢ���κ��
	    require( &GetPath( $UI_DIR, 'AliasDel.pl' ));
	    last;
	}
	elsif ( $c eq 'as' )
	{
	    ### AliasShow - �桼�������ꥢ�����Ȳ��̤�ɽ��
	    require( &GetPath( $UI_DIR, 'AliasShow.pl' ));
	    last;
	}
    }

    if ( $SYS_F_B && ( $c eq 'bl' ))
    {
	### BoardList - �Ǽ��İ�����ɽ��
	require( &GetPath( $UI_DIR, 'BoardList.pl' ));
	last;
    }

    # �ʲ��ϴ�����
    if ( $SYS_F_MT )
    {
	if ( $c eq 'mtr' )
	{
	    $gVarComType = 1;
	    require( &GetPath( $UI_DIR, 'View.pl' ));
	    last;
	}
	elsif ( $c eq 'vm' )
	{
	    $gVarComType = 1;
	    require( &GetPath( $UI_DIR, 'ViewTitle.pl' ));
	    last;
	}
    }

    if ( $SYS_F_MV )
    {
	if  ( $c eq 'ct' )
	{
	    $gVarComType = 2;
	    require( &GetPath( $UI_DIR, 'ViewTitle.pl' ));
	    last;
	}
	elsif ( $c eq 'ce' )
	{
	    $gVarComType = 3;
	    require( &GetPath( $UI_DIR, 'ViewTitle.pl' ));
	    last;
	}
	elsif ( $c eq 'mvt' )
	{
	    $gVarComType = 4;
	    require( &GetPath( $UI_DIR, 'ViewTitle.pl' ));
	    last;
	}
	elsif ( $c eq 'mve' )
	{
	    $gVarComType = 5;
	    require( &GetPath( $UI_DIR, 'ViewTitle.pl' ));
	    last;
	}
    }

    if ( $SYS_F_D )
    {
	if ( $c eq 'dp' )
	{
	    ### DeletePreview - ��������γ�ǧ
	    require( &GetPath( $UI_DIR, 'DeletePreview.pl' ));
	    last;
	}
	elsif ( $c eq 'de' )
	{
	    ### DeleteExec - �����κ��
	    $gVarThreadFlag = 0;
	    require( &GetPath( $UI_DIR, 'DeleteExec.pl' ));
	    last;
	}
	elsif ( $c eq 'det' ) {
	    $gVarThreadFlag = 1;
	    require( &GetPath( $UI_DIR, 'DeleteExec.pl' ));
	    last;
	}
    }

    if ( $SYS_F_AM )
    {
	if ( $c eq 'mp' )
	{
	    ### ArriveMailEntry - �ᥤ�뼫ư�ۿ���λ���
	    require( &GetPath( $UI_DIR, 'ArriveMailEntry.pl' ));
	    last;
	}
	elsif ( $c eq 'me' )
	{
	    ### ArriveMailExec - �ᥤ�뼫ư�ۿ��������
	    require( &GetPath( $UI_DIR, 'ArriveMailExec.pl' ));
	    last;
	}
    }

    # �ɤΥ��ޥ�ɤǤ�ʤ������顼��
    &Fatal( 99, '' );
}

exit( 0 );


######################################################################
# �桼�����󥿥ե���������ץ���ơ������(����)
#
# UI�ǥ��쥯�ȥ�˼�����Ƥ���UI�μ����⥸�塼���require���롥
# ���פʥץ����򥳥�ѥ��뤷�ʤ��褦�ˤ��뤿�ᡥ
# �ƴؿ��Υ�ե���󥹤ϡ�UI�ǥ��쥯�ȥ���γƥե�����򻲾ȤΤ��ȡ�


### Fatal - ���顼ɽ��
sub Fatal
{
    ( $gVarFatalNo, $gVarFatalInfo ) = @_;
    require( &GetPath( $UI_DIR, 'Fatal.pl' ));
}

### ArriveMail - ���������夷�����Ȥ�ᥤ��
sub ArriveMail
{
    ( $gName, $gEmail, $gSubject, $gIcon, $gId, @gTo ) = @_;
    require( &GetPath($UI_DIR, 'ArriveMail.pl' ));
}

### FollowMail - ȿ�������ä����Ȥ�ᥤ��
sub FollowMail
{
    ( $gName, $gEmail, $gDate, $gSubject, $gIcon, $gId, $gFname, $gFemail, $gFsubject, $gFicon, $gFid, @gTo ) = @_;
    require( &GetPath( $UI_DIR, 'FollowMail.pl' ));
}


######################################################################
# �桼�����󥿥ե���������ץ���ơ������(������)


###
## ViewOriginalArticle - ��������ɽ��
#
# - SYNOPSIS
#	ViewOriginalArticle($Id, $CommandFlag, $OriginalFlag);
#
# - ARGS
#	$Id			����ID
#	$CommandFlag		���ޥ�ɤ�ɽ�����뤫�ݤ�(ɽ������=1)
#	$OriginalFlag		���ε�����ˡ�(�����)�������ؤΥ�󥯤�
#				ɽ�����뤫�ݤ�(ɽ������=1)
#
# - DESCRIPTION
#	��������ɽ�����롥
#
# - RETURN
#	�ʤ�
#
sub ViewOriginalArticle
{
    local( $Id, $CommandFlag, $OriginalFlag ) = @_;

    local( $Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url ) = &GetArticlesInfo( $Id );

    local( $Num );
    foreach ( 0 .. $#DB_ID ) { $Num = $_, last if ( $DB_ID[$_] eq $Id ); }
    local( $PrevId ) = $DB_ID[$Num - 1] if ( $Num > 0 );
    local( $NextId ) = $DB_ID[$Num + 1];

    if ( $CommandFlag && $SYS_COMMAND )
    {
	# ���ޥ��ɽ��
	if ( $SYS_COMICON == 1 )
	{
	    $DlmtS = "";
	    $DlmtL = " // ";
	}
	elsif ( $SYS_COMICON == 2 )
	{
	    $DlmtS = " | ";
	    $DlmtL = "";
	}
	else
	{
	    $DlmtS = " | ";
	    $DlmtL = "";
	}

	&cgiprint'Cache( "<p>\n" );

	&cgiprint'Cache( &TagA( $BOARDLIST_URL, &TagComImg( $ICON_BLIST, $H_BACKBOARD, $SYS_COMICON )), "\n" ) if $SYS_F_B;

	&cgiprint'Cache( $DlmtS, &TagA( "$PROGRAM?b=$BOARD&c=v&num=$DEF_TITLE_NUM", &TagComImg( $ICON_TLIST, $H_BACKTITLEREPLY, $SYS_COMICON )), "\n" );
	
	local( $TagTmp ) = &TagComImg( $ICON_PREV, $H_PREVARTICLE, $SYS_COMICON );
	if ( $PrevId ne '' )
	{
	    &cgiprint'Cache( $DlmtS, &TagA( "$PROGRAM?b=$BOARD&c=e&id=$PrevId", $TagTmp ), "\n" );
	}
	else
	{
	    &cgiprint'Cache( $DlmtS, $TagTmp, "\n" );
	}
	
	$TagTmp = &TagComImg( $ICON_NEXT, $H_NEXTARTICLE, $SYS_COMICON );
	if ( $NextId ne '' )
	{
	    &cgiprint'Cache( $DlmtS, &TagA( "$PROGRAM?b=$BOARD&c=e&id=$NextId", $TagTmp ), "\n" );
	}
	else
	{
	    &cgiprint'Cache( $DlmtS, $TagTmp, "\n" );
	}
	
	if ( $SYS_F_T )
	{
	    $TagTmp = &TagComImg( $ICON_THREAD, $H_READREPLYALL, $SYS_COMICON );
	    if ( $Aids ne '' )
	    {
		&cgiprint'Cache( $DlmtS, &TagA( "$PROGRAM?b=$BOARD&c=t&id=$Id", $TagTmp ), "\n" );
	    }
	    else
	    {
		&cgiprint'Cache( $DlmtS, $TagTmp, "\n");
	    }
	}

	&cgiprint'Cache( $DlmtL, "\n" ) if $DlmtL;

	if ( $SYS_F_N )
	{
	    &cgiprint'Cache( $DlmtS, &TagA( "$PROGRAM?b=$BOARD&c=n", &TagComImg( $ICON_WRITENEW, $H_POSTNEWARTICLE, $SYS_COMICON )), "\n" );
	    &cgiprint'Cache( $DlmtS, &TagA( "$PROGRAM?b=$BOARD&c=f&id=$Id", &TagComImg( $ICON_FOLLOW, $H_REPLYTHISARTICLE, $SYS_COMICON )), "\n" );
	    &cgiprint'Cache( $DlmtS, &TagA( "$PROGRAM?b=$BOARD&c=q&id=$Id", &TagComImg( $ICON_QUOTE, $H_REPLYTHISARTICLEQUOTE, $SYS_COMICON )), "\n" );
	}

	&cgiprint'Cache( $DlmtL, "\n" ) if $DlmtL;

	&cgiprint'Cache( $DlmtS, &TagA( "$PROGRAM?b=$BOARD&c=i&type=article", &TagComImg( $ICON_HELP, "�إ��", $SYS_COMICON )), "\n")
	    if ( $SYS_COMICON == 1 );

	&cgiprint'Cache( "</p>\n" );
    }

    &cgiprint'Cache( "<p>\n" );

    # �����ֹ桤��
    &cgiprint'Cache( "<strong>$H_SUBJECT</strong>: <strong>$Id .</strong> " );
    if (( $Icon eq $H_NOICON ) || ( $Icon eq '' ))
    {
	&cgiprint'Cache( $Subject );
    }
    else
    {
	&cgiprint'Cache( &TagMsgImg( &GetIconUrlFromTitle( $Icon, $BOARD ),
				    $Icon ), $Subject );
    }

    # ��̾��
    if ( $Url eq '' )
    {
	&cgiprint'Cache( "<br>\n<strong>$H_FROM</strong>: ", $Name );
    }
    else
    {
	&cgiprint'Cache( "<br>\n<strong>$H_FROM</strong>: ",
			&TagA( $Url, $Name ));
    }

    # �ᥤ��
    &cgiprint'Cache( " ", &TagA( "mailto:$Email" , "&lt;$Email&gt;" )) if $Email;

    # �ޥ���
    &cgiprint'Cache( "<br>\n<strong>$H_HOST</strong>: $RemoteHost" )
	if $SYS_SHOWHOST;

    # �����
    &cgiprint'Cache( "<br>\n<strong>$H_DATE</strong>: ",
		    &GetDateTimeFormatFromUtc( $Date ));

    # ȿ����(���Ѥξ��)
    &ShowLinksToFollowedArticle( split( /,/, $Fid ))
	if ( $OriginalFlag && ( $Fid ne '' ));

    # �ڤ���
    &cgiprint'Cache( "</p>\n$H_LINE\n" );

    # ���������
    local( @ArticleBody );
    &GetArticleBody( $Id, $BOARD, *ArticleBody );
    &cgiprint'Cache( @ArticleBody );
}


###
## ThreadArticleMain - �ե�������������ɽ����
#
# - SYNOPSIS
#	ThreadArticle($SubjectOnly, $Head, @Tail);
#
# - ARGS
#	$SubjectOnly	�����ȥ�Τߤ�ɽ������Τ���
#			���뤤�ϵ�����ʸ��ɽ������Τ���
#	$Head		�ڹ�¤�ΥإåɥΡ���
#	@Tail		�ڹ�¤��̼�Ρ��ɷ�
#
# - DESCRIPTION
#	���뵭���ȡ����ε����ؤΥ�ץ饤������ޤȤ��ɽ�����롥
#	�����ڹ�¤�ϡ�
#		( a ( b ( c d ) ) ( e ) ( f ( g ) ) )
#	�Τ褦�ʥꥹ�ȤǤ��롥
#	�ܺ٤�&GetFollowIdTree�Υ���ץ������ʬ�򻲾ȤΤ��ȡ�
#
# - RETURN
#	�ʤ�
#
sub ThreadArticleMain
{
    local( $SubjectOnly, $Head, @Tail ) = @_;

    # �������פ����������Τ�Τ���
    if ( $SubjectOnly )
    {
	if ( $Head eq '(' )
	{
	    &cgiprint'Cache( "<ul>\n" );
	}
	elsif ( $Head eq ')' )
        {
	    &cgiprint'Cache( "</ul>\n" );
	}
	else
	{
	    local( $dFid, $dAids, $dDate, $dSubject, $dIcon, $dRemoteHost, $dName ) = &GetArticlesInfo( $Head );
	    &cgiprint'Cache( "<li>", &GetFormattedTitle( $Head, $BOARD, $dAids, $dIcon, $dSubject, $dName, $dDate ), "\n" );
	}
    }
    elsif (( $Head ne '(' ) && ( $Head ne ')' ))
    {
	# ��������ɽ��(���ޥ���դ�, �������ʤ�)
	&cgiprint'Cache( "$H_HR\n" );
	&ViewOriginalArticle( $Head, 1, 0 );
    }

    # tail recuresive.
    &ThreadArticleMain( $SubjectOnly, @Tail ) if @Tail;
}


###
## QuoteOriginalArticle - ���Ѥ���(�����䤢��)
#
# - SYNOPSIS
#	QuoteOriginalArticle($Id);
#
# - ARGS
#	$Id		����ID
#
# - DESCRIPTION
#	��������Ѥ���ɽ������
#
# - RETURN
#	�ʤ�
#
sub QuoteOriginalArticle
{
    local( $Id, *msg ) = @_;

    local( $Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $pFid, $pAids, $pDate, $pSubject, $pIcon, $pRemoteHost, $pName, $QMark, $line, @ArticleBody );

    # ����������μ���
    ( $Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name ) = &GetArticlesInfo( $Id );

    # �������Τ���˸���������
    if ( $Fid )
    {
	$Fid =~ s/,.*$//o;
	( $pFid, $pAids, $pDate, $pSubject, $pIcon, $pRemoteHost, $pName ) = &GetArticlesInfo( $Fid );
    }

    # ����
    &GetArticleBody( $Id, $BOARD, *ArticleBody );
    foreach $line ( @ArticleBody )
    {
	&TAGEncode( *line );

	$QMark = $DEFAULT_QMARK;
	$QMark = $Name . $QMark if $SYS_QUOTENAME;

	# ��ʸ�Τ�����������ʬ�ˤϡ������˰���ʸ�����Ťͤʤ�
	# ���Ԥˤ��פ�ʤ�
	$QMark = '' if (( $line =~ /^$/o ) || ( $line =~ /^$pName\s*$DEFAULT_QMARK/ ));

	# ����ʸ�����ɽ��
	$msg .= "$QMark$line";
    }
}


###
## QuoteOriginalArticleWithoutQMark - ���Ѥ���(������ʤ�)
#
# - SYNOPSIS
#	QuoteOriginalArticleWithoutQMark($Id);
#
# - ARGS
#	$Id		����ID
#
# - DESCRIPTION
#	��������Ѥ���ɽ������
#
# - RETURN
#	�ʤ�
#
sub QuoteOriginalArticleWithoutQMark
{
    local( $Id, *msg ) = @_;

    local( @ArticleBody, $line );
    &GetArticleBody( $Id, $BOARD, *ArticleBody );
    foreach $line ( @ArticleBody )
    {
	&TAGEncode( *line );
	$msg .= $line;
    }
}


###
## BoardHeader - �Ǽ��ĥإå���ɽ��
#
# - SYNOPSIS
#	BoardHeader($Type);
#
# - ARGS
#	$Type	�Ǽ��ĥإå��Υ�����
#			'normal' ... �̾�
#			'maint' .... ������
#
# - DESCRIPTION
#	�Ǽ��ĤΥإå���ɽ�����롥
#
# - RETURN
#	�ʤ�
#
sub BoardHeader
{
    local( $Type ) = @_;

    local( @BoardHeader );
    &GetBoardHeader( $BOARD, *BoardHeader );
    &cgiprint'Cache( @BoardHeader );

    if ( $SYS_F_MT && ( $Type eq 'normal' ))
    {
	&cgiprint'Cache( "<p>\n<ul>\n" );
	&cgiprint'Cache( "<li>", &TagA( "$PROGRAM?c=vm&b=$BOARD&num=$DEF_TITLE_NUM", "�������ѤΥ����ȥ������" ), "\n</ul>\n</p>\n" );
    }
    elsif ( $Type eq 'maint' )
    {
	&cgiprint'Cache( "<p>\n<ul>\n" );
	&cgiprint'Cache( "<li>", &TagA( "$PROGRAM?c=mp&b=$BOARD", "��ư�ᥤ���ۿ�������ꤹ��" ), "\n" ) if $SYS_F_AM;
	&cgiprint'Cache( "<li>", &TagA( "$PROGRAM?c=v&b=$BOARD&num=$DEF_TITLE_NUM", "�̾�Υ����ȥ������" ), "\n</ul>\n</p>\n" );
    }
}


###
## ShowLinksToFollowedArticle - �����������ɽ��
#
# - SYNOPSIS
#	ShowLinksToFollowedArticle(@IdList);
#
# - ARGS
#	@IdList		��ץ饤����ID�Υꥹ��(�Ť���ץ饤�ۤ������ˤ���)
#
# - DESCRIPTION
#	�����������ɽ�����롥
#
# - RETURN
#	�ʤ�
#
sub ShowLinksToFollowedArticle
{
    local( @IdList ) = @_;

    local( $Id, $Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name );

    # ���ꥸ�ʥ뵭��
    if ( $#IdList > 0 )
    {
	$Id = $IdList[$#IdList];
	( $Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name ) = &GetArticlesInfo( $Id );
	&cgiprint'Cache( "<br>\n<strong>$H_ORIG_TOP:</strong> ", &GetFormattedTitle( $Id, $BOARD, $Aids, $Icon, $Subject, $Name, $Date ));
    }

    # ������
    $Id = $IdList[0];
    ( $Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name ) = &GetArticlesInfo( $Id );
    &cgiprint'Cache( "<br>\n<strong>$H_ORIG:</strong> ", &GetFormattedTitle( $Id, $BOARD, $Aids, $Icon, $Subject, $Name, $Date ));
}


###
## PrintButtonToTitleList - �����ȥ���������ܥ����ɽ��
#
# - SYNOPSIS
#	PrintButtonToTitleList($Board);
#
# - ARGS
#	$Board		�Ǽ���ID
#
# - DESCRIPTION
#	�����ȥ��������뤿��Υܥ����ɽ������
#
# - RETURN
#	�ʤ�
#
sub PrintButtonToTitleList
{
    local( $Board ) = @_;

    local( %tags ) = ( 'b', $Board, 'c', 'v', 'num', $DEF_TITLE_NUM );
    local( $str );
    &TagForm( *str, *tags, "$H_BACKTITLEREPLY", '', '' );
    &cgiprint'Cache( $str );

    if ( $H_BACKTITLEDATE )
    {
	%tags = ( 'b', $Board, 'c', 'r', 'num', $DEF_TITLE_NUM );
	&TagForm( *str, *tags, "$H_BACKTITLEDATE", '', '' );
	&cgiprint'Cache( $str );
    }
}


###
## PrintButtonToBoardList - �Ǽ��İ��������ܥ����ɽ��
#
# - SYNOPSIS
#	PrintButtonToBoardList;
#
# - ARGS
#	�ʤ�
#
# - DESCRIPTION
#	�Ǽ��İ�������뤿��Υܥ����ɽ������
#
# - RETURN
#	�ʤ�
#
sub PrintButtonToBoardList
{
    if ( $BOARDLIST_URL =~ /$PROGRAM/ )
    {
	local( %tags ) = ( 'c', 'bl' );
	local( $str );
	&TagForm( *str, *tags, $H_BACKBOARD, '', '' );
	&cgiprint'Cache( $str );
    }
    else
    {
	&cgiprint'Cache( "<p><a href=\"$BOARDLIST_URL\">$H_BACKBOARD</a></p>\n" );
    }
}


###
## MsgHeader - HTMLʸ��Υإå���ʬ��ɽ��
#
# - SYNOPSIS
#	MsgHeader($Title, $Message, $LastModified);
#
# - ARGS
#	$Title		HTMLʸ���TITLE(title�����������Τǡ����ΤȤ���
#			US-ASCII�Τߤ��Ƥ������ۤ���̵��)
#	$Message	HTMLʸ��Υ����ȥ�(��ʸ���ɽ������ʸ����)
#	$LastModified	�ǽ���������
#
# - DESCRIPTION
#	HTMLʸ��Υإå���ʬ��ɽ�����롥
#
# - RETURN
#	�ʤ�
#
sub MsgHeader
{
    local( $Title, $Message, $LastModified ) = @_;
    
    if (( $SYS_ALIAS == 3 ) && ( $cgi'TAGS{'cookies'} eq 'on' ))
    {
	local( @cookieStr ) = ( "kb10info=" . join( $COLSEP, $cgi'TAGS{ 'name' }, $cgi'TAGS{ 'mail' }, $cgi'TAGS{ 'url' } ));
	local( $cookieExpire );
	if ( $SYS_COOKIE_EXPIRE == 1 )
	{
	    $cookieExpire = 'Thursday, 31-Dec-2029 23:59:59 GMT';
	}
	elsif ( $SYS_COOKIE_EXPIRE == 2 )
	{
	    $cookieExpire = $^T + ( $SYS_COOKIE_VALUE * 86400 );
	    # 86400 = 24 * 60 * 60
	}
	elsif ( $SYS_COOKIE_EXPIRE == 3 )
	{
	    $cookieExpire = $SYS_COOKIE_VALUE;
	}
	else
	{
	    $cookieExpire = '';
	}
	&cgi'Header( 0, 0, 1, *cookieStr, $cookieExpire );
    }
    else
    {
	# Last-Modified�϶���Cookies�����
	&cgi'Header( 0, 0, 0, 0, 0 );
    }

    &cgiprint'Init();
    &cgiprint'Cache(<<__EOF__);
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML i18n//EN">
<html>
<head>
<base href="$BASE_URL">
<title>$Title - $BOARDNAME - $SYSTEM_NAME</title>
<LINK REV=MADE HREF="mailto:$MAINT">
</head>
__EOF__

    &cgiprint'Cache( "<body" );
    if ( $SYS_NETSCAPE_EXTENSION )
    {
	&cgiprint'Cache(" background=\"$BG_IMG\"") if $BG_IMG;
	&cgiprint'Cache(" bgcolor=\"$BG_COLOR\"") if $BG_COLOR;
	&cgiprint'Cache(" TEXT=\"$TEXT_COLOR\"") if $TEXT_COLOR;
	&cgiprint'Cache(" LINK=\"$LINK_COLOR\"") if $LINK_COLOR;
	&cgiprint'Cache(" ALINK=\"$ALINK_COLOR\"") if $ALINK_COLOR;
	&cgiprint'Cache(" VLINK=\"$VLINK_COLOR\"") if $VLINK_COLOR;
    }
    &cgiprint'Cache( ">\n" );

    &cgiprint'Cache(<<__EOF__);
<h1>$Message</h1>

<p>[
__EOF__

    &cgiprint'Cache( "$H_BOARD: $BOARDNAME // \n" ) if ( $BOARD && $BOARDNAME );
    &cgiprint'Cache( "����: ", &GetDateTimeFormatFromUtc( $^T ));
    &cgiprint'Cache(<<__EOF__);
]</p>

$H_HR

__EOF__
}


###
## MsgFooter - HTMLʸ��Υեå���ʬ��ɽ��
#
# - SYNOPSIS
#	MsgFooter;
#
# - ARGS
#	�ʤ�
#
# - DESCRIPTION
#	HTMLʸ��Υեå���ʬ��ɽ�����롥
#
# - RETURN
#	�ʤ�
#
sub MsgFooter
{
    # ��������ѹ�����Τ�ּ�ͳ�פǤ����ä��Ƥ��������ꤢ��ޤ���
    local( $addr ) = "Maintenance: " . &TagA( "mailto:$MAINT", $MAINT_NAME ) . "<br>" . &TagA( "http://www.kinotrope.co.jp/~nakahiro/kb10.shtml", "KINOBOARDS/$KB_VERSION R$KB_RELEASE" ) . ": Copyright (C) 1995-98 " . &TagA( "http://www.kinotrope.co.jp/~nakahiro/", "NAKAMURA Hiroshi" ) . ".";
    # ���������ֲ���������ä����!�פȤ��񤯤ȡ��ʤҤθ����򿯳����ơ�
    # ��äѤ�GPL2�˰�ȿ���뤳�Ȥˤʤä��㤦�Τǵ���Ĥ��Ƥ͡�(^_^;

    &cgiprint'Cache(<<__EOF__);
$H_HR
<address>
$addr
</address>
</body>
</html>
__EOF__

    &cgiprint'Flush();
}


###
## GetFormattedTitle - �����ȥ�ꥹ�ȤΥե����ޥå�
#
# - SYNOPSIS
#	GetFormattedTitle($Id, $Board, $Aids, $Icon, $Title, $Name, $Date);
#
# - ARGS
#	$Id		����ID
#	$Board		�Ǽ���ID
#	$Aids		��ץ饤���������뤫�ݤ�
#	$Icon		������������ID
#	$Title		������Subject
#	$Name		��������Ƽ�̾
#	$Date		�������������(UTC)
#
# - DESCRIPTION
#	���뵭���򥿥��ȥ�ꥹ��ɽ���Ѥ˥ե����ޥåȤ��롥
#
# - RETURN
#	�ե����ޥåȤ���ʸ����
#
sub GetFormattedTitle
{
    local( $Id, $Board, $Aids, $Icon, $Title, $Name, $Date ) = @_;

    local( $String, $InputDate, $IdStr, $Link, $Thread, $NewIcon );

    $InputDate = &GetDateTimeFormatFromUtc(( $Date || &GetModifiedTime( $Id, $Board )));
    # �����ȥ뤬�Ĥ��Ƥʤ��ä��顤Id�򤽤Τޤޥ����ȥ�ˤ��롥
    $Title = $Title || $Id;

    $IdStr = "<strong>$Id.</strong> ";
    $Link = &TagA( "$PROGRAM?b=$Board&c=e&id=$Id", $Title );
    $Thread = (($SYS_F_T && $Aids) ? " " . &TagA( "$PROGRAM?b=$Board&c=t&id=$Id", $H_THREAD ) : '');
    $NewIcon = " " . &TagMsgImg( $ICON_NEW, $H_NEWARTICLE ) if $DB_NEW{$Id};

    if (( $Icon eq $H_NOICON ) || ($Icon eq '' ))
    {
	$String = "$IdStr$Link$Thread [" . ( $Name || $MAINT_NAME ) . "] $InputDate$NewIcon";
    }
    else
    {
#	$String = $IdStr . &TagMsgImg( &GetIconUrlFromTitle( $Icon, $Board ), "$Icon " ) . "$Link [" . ( $Name || $MAINT_NAME ) . "] $InputDate$NewIcon";
	$String = $IdStr . &TagMsgImg( &GetIconUrlFromTitle( $Icon, $Board ), "$Icon " ) . "$Link$Thread [" . ( $Name || $MAINT_NAME ) . "] $InputDate$NewIcon";
    }
    $String;
}


###
## TagComImg - ���ޥ�ɥ��������ѥ��᡼�������Υե����ޥå�
#
# - SYNOPSIS
#	TagComImg( $src, $alt, $textP );
#
# - ARGS
#	$src		���������᡼����URL
#	$alt		alt�����Ѥ�ʸ����
#	$type		ɽ��������
#				1 ... ��������θ���ʸ������ɲä��ʤ�
#				2 ... ��������θ���ʸ������ɲä��ʤ�
#				0/others ... ��������ʤ��ǥƥ����Ȥ���
#
# - DESCRIPTION
#	���᡼����ɽ���ѥ����˥ե����ޥåȤ��롥
#
# - RETURN
#	�ե����ޥåȤ���ʸ����
#
sub TagComImg
{
    local( $src, $alt, $type ) = @_;
    if ( $type == 1 )
    {
	"<img src=\"$src\" alt=\"$alt\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\">";
    }
    elsif ( $type == 2 )
    {
	"<img src=\"$src\" alt=\"$alt\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\">$alt";
    }
    else
    {
	$alt;
    }
}


###
## TagMsgImg - �������������ѥ��᡼�������Υե����ޥå�
#
# - SYNOPSIS
#	TagMsgImg( $src, $alt );
#
# - ARGS
#	$src		���������᡼����URL
#	$alt		alt�����Ѥ�ʸ����
#
# - DESCRIPTION
#	���᡼����ɽ���ѥ����˥ե����ޥåȤ��롥
#
# - RETURN
#	�ե����ޥåȤ���ʸ����
#
sub TagMsgImg
{
    local( $src, $alt ) = @_;
    "<img src=\"$src\" alt=\"$alt\" width=\"$MSGICON_WIDTH\" height=\"$MSGICON_HEIGHT\" BORDER=\"0\">";
}


###
## TagA - ��󥯥����Υե����ޥå�
#
# - SYNOPSIS
#	TagA( $href, $markUp );
#
# - ARGS
#	$href		�����URL
#	$markUp		�ޡ������å�ʸ����
#
# - DESCRIPTION
#	��󥯤��󥯥����˥ե����ޥåȤ��롥
#
# - RETURN
#	�ե����ޥåȤ���ʸ����
#
sub TagA
{
    local( $href, $markUp ) = @_;
    "<a href=\"$href\">$markUp</a>";
}


###
## TagForm - �ե����ॿ���Υե����ޥå�
#
# - SYNOPSIS
#	TagForm( *str, *hiddenTags, $submit, $reset, *contents );
#
# - ARGS
#	*str		����ʸ����γ�Ǽ��
#	*tags		�ɲä���hidden��������᤿Ϣ������
#	*submit		submit�ܥ���ʸ����
#	*reset		reset�ܥ���ʸ����
#	*contents	</form>�����ޤǤ���������ʸ����
#
# - DESCRIPTION
#	Form�����Υե����ޥå�
#
sub TagForm
{
    local( *str, *tags, $submit, $reset, *contents ) = @_;

    $str = "<form action=\"$PROGRAM\" method=\"POST\">\n";
    foreach ( keys( %tags ))
    {
	$str .= "<input name=\"$_\" type=\"hidden\" value=\"$tags{$_}\">\n";
    }
    $str .= $contents;
    $str .= "<input type=\"submit\" value=\"$submit\">\n";
    $str .= "<input type=\"reset\" value=\"$reset\">\n" if $reset;
    $str .= "</form>\n";
}


###
## SendMail - �ᥤ������
#
# - SYNOPSIS
#	SendMail($Subject, $Message, $Id, @To);
#
# - ARGS
#	$Subject	�ᥤ���Subjectʸ����
#	$Message	��ʸ
#	$Id		���Ѥ���ʤ鵭��ID; �ʤ���а��ѤϤʤ�
#	@To		����E-Mail addr.�Υꥹ��
#
# - DESCRIPTION
#	�ᥤ����������롥
#
# - RETURN
#	�ʤ�
#
sub SendMail
{
    local( $Subject, $Message, $Id, @To ) = @_;

    local( $ExtensionHeader, @ArticleBody );

    $ExtensionHeader = "X-Kb-System: $SYSTEM_NAME\n";
    if (( ! $SYS_MAILHEADBRACKET ) && $BOARDNAME && ($Id ne '' ))
    {
	$ExtensionHeader .= "X-Kb-Board: $BOARDNAME\nX-Kb-Articleid: $Id\n";
    }

    # ���ѵ���
    if ( $Id ne '' ) {
	$Message .= "\n--------------------\n";
	&GetArticleBody($Id, $BOARD, *ArticleBody);
	foreach(@ArticleBody)
	{
	    s/<[^>]*>//go;	# �������פ�ʤ�
	    $Message .= &HTMLDecode( $_ ) if ( $_ ne '' );
	}
    }

    local( $stat, $errstr ) = &cgi'sendMail( $MAILFROM_LABEL || $MAINT_NAME, $MAINT, $Subject, $ExtensionHeader, $Message, $MAILTO_LABEL, @To );
    &Fatal( 9, "$BOARDNAME/$Id/$errstr" ) if ( !$stat );
}


###
## KbLog - log a log
#
# - SYNOPSIS
#	&KbLog( $kinologue'severity, *msg );
#
# - ARGS
#	$kinologue'severity	severity id defined in kinologue.pl.
#	*msg			reference to msg string.
#
# - DESCRIPTION
#	log a log using kinologue.
#	exit program(not function) if failed to write log.
#
# - RETURN
#	returns nothing.
#
sub KbLog
{
    local( $severity, $msg ) = @_;

    &kinologue'KlgLog( $severity, $msg, $PROGNAME, $LOGFILE, $FF_LOG ) || &Fatal( 1000, '' ) if $SYS_LOG;
}


######################################################################
# ���å�����ץ���ơ������


###
## MakeNewArticle - ��������Ƥ��줿����������
#
# - SYNOPSIS
#	MakeNewArticle($Board, $Id, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail);
#
# - ARGS
#	$Board		�������뵭��������Ǽ��Ĥ�ID
#	$Id		��ץ饤��������ID
#	$TextType	ʸ�񥿥���
#	$Name		��Ƽ�̾
#	$Email		��Ƽ�E-Mail addr.
#	$Url		��Ƽ�URL
#	$Icon		��������ID
#	$Subject	Subjectʸ����
#	$Article	��ʸʸ����
#	$Fmail		��ץ饤�����ä����˥ᥤ����Τ餻�뤫�ݤ�('on'/'')
#
# - DESCRIPTION
#	��Ƥ��줿�����򵭻�DB���������롥
#
# - RETURN
#	�ʤ�
#
sub MakeNewArticle
{
    local( $Board, $Id, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail ) = @_;

    local( $ArticleId );

    &CheckArticle( $Board, *Name, *Email, *Url, *Subject, *Icon, *Article );

    # �����������ֹ�����(�ޤ������ֹ�������Ƥʤ�)
    $ArticleId = &GetNewArticleId( $Board );

    # �����Υե�����κ���
    &MakeArticleFile( $TextType, $Article, $ArticleId, $Board );

    # �����������ֹ��񤭹���
    &WriteArticleId( $ArticleId, $Board );

    # DB�ե��������Ƥ��줿�������ɲ�
    # �̾�ε������Ѥʤ�ID
    &AddDBFile( $ArticleId, $Board, $Id, $^T, $Subject, $Icon, $cgi'REMOTE_HOST, $Name, $Email, $Url, $Fmail );

    $ArticleId;
}


###
## SearchArticleKeyword - �����θ���(��ʸ)
#
# - SYNOPSIS
#	SearchArticleKeyword($Id, $Board, @KeyList);
#
# - ARGS
#	$Id		��ʸ�򸡺����뵭����ID
#	$Board		�Ǽ���ID
#	@KeyList	������ɥꥹ��
#
# - DESCRIPTION
#	���ꤵ�줿��������ʸ�򡤥�����ɤ�AND�������롥
#
# - RETURN
#	�ǽ�˥�����ɤȥޥå������ԡ��ޥå����ʤ��ä�������֤���
#
sub SearchArticleKeyword
{
    local( $Id, $Board, @KeyList ) = @_;

    local( @NewKeyList, $Line, $Return, $Code, $ConvFlag, @ArticleBody );

    $ConvFlag = ( $Id !~ /^\d+$/ );

    &GetArticleBody( $Id, $Board, *ArticleBody );
    foreach ( @ArticleBody )
    {
	$Line = $_;
	if ( $ConvFlag )
	{
	    $Code = &jcode'getcode( *Line );
	    &jcode'convert( *Line, 'euc', $Code, 'z' );
	}

	# ����
	@NewKeyList = ();
	foreach ( @KeyList )
	{
	    if ( $Line =~ /$_/i )
	    {
		# �ޥå�����! 1���ܤʤ�Ф��Ȥ�
		$Return = $Line unless $Return;
	    }
	    else
	    {
		# �ޤ�õ���ʤ���ġ�
		push( @NewKeyList, $_ );
	    }
	}
	# ���ʤ�ȴ����
	last unless ( @KeyList = @NewKeyList );
    }

    # �ޤ��ĤäƤ��饢���ȡ����ʤ�ǽ�Υޥå������Ԥ��֤���
    @KeyList ? '' : $Return;
}


###
## CheckArticle - ���Ϥ��줿��������Υ����å�
#
# - SYNOPSIS
#	CheckArticle($board, *name, *eMail, *url, *subject, *icon, *article);
#
# - ARGS
#	$board		�Ǽ���ID
#	*name		��Ƽ�̾
#	*eMail		�ᥤ�륢�ɥ쥹
#	*url		URL
#	*subject	Subject
#	*icon		��������ID
#	*article	��ʸ
#
# - DESCRIPTION
#	���Ϥ��줿����������å�����
#
# - RETURN
#	�ʤ�
#
sub CheckArticle
{
    local( $board, *name, *eMail, *url, *subject, *icon, *article ) = @_;

    local( $Tmp );

    if ( $name =~ /^\#.*$/o )
    {
        ( $Tmp, $eMail, $url ) = &GetUserInfo( $name );
	&Fatal( 6, $name ) if ( $Tmp eq '' );
	$name = $Tmp;
    }
    elsif ( $SYS_ALIAS == 2 )
    {
	# ɬ�ܤΤϤ��ʤΤˡ����ꤵ�줿�����ꥢ������Ͽ����Ƥ��ʤ�
	&Fatal( 6, $name );
    }

    &CheckName( *name );
    &CheckEmail( *eMail );
    &CheckURL( *url );
    &CheckSubject( *subject );

    # ��ʸ�ζ������å���
    &Fatal( 2, '' ) if ( $article eq '' );

    # ��������Υ����å�; ������������̵���פ����ꡥ
    $icon = $H_NOICON if ( !&GetIconUrlFromTitle( $icon, $board ));

    if ( $SYS_MAXARTSIZE != 0 )
    {
	local( $length ) = length( $article );
	&Fatal( 12, $length ) if ( $length > $SYS_MAXARTSIZE );
    }
}


###
## secureSubject - ������Subject����Ф�
#
# - SYNOPSIS
#	secureSubject( *subject );
#
# - ARGS
#	*subject	Subjectʸ����
#
# - DESCRIPTION
#	$subject�������ʸ������Ѵ����롥
#
sub secureSubject
{
    local( *subject ) = @_;

    if ( $SYS_TAGINSUBJECT )
    {
	local( @subjectTags ) =
	    (
	     # ����̾, �Ĥ�ɬ�ܤ��ݤ�, ���Ѳ�ǽ��feature
	     'B',		1,	'',
	     'BR',		0,	'',
	     'CITE',		1,	'',
	     'CODE',		1,	'',
	     'EM',		1,	'',
	     'FONT',		1,	'SIZE/COLOR',
	     'H2',		1,	'ALIGN',
	     'H3',		1,	'ALIGN',
	     'H4',		1,	'ALIGN',
	     'H5',		1,	'ALIGN',
	     'H6',		1,	'ALIGN',
	     'I',		1,	'',
	     'IMG',		0,	'SRC/ALT/ALIGN/WIDTH/HEIGHT/BORDER',
	     'STRONG',		1,	'',
	     'TT',		1,	'',
	     'VAR',		1,	'',
	     );
	
	local( %sNeedVec, %sFeatureVec, $tag );
	while( @subjectTags )
	{
	    $tag = shift( @subjectTags );
	    $sNeedVec{ $tag } = shift( @subjectTags );
	    $sFeatureVec{ $tag } = shift( @subjectTags );
	}

	# secrurity check
	&cgi'SecureHtmlEx( *subject, *sNeedVec, *sFeatureVec );
    }
    else
    {
	$subject = &HTMLEncode( $subject );	# no tags are allowed.
    }
}


###
## secureArticle - ������Article����Ф�
#
# - SYNOPSIS
#	secureArticle( *article, $textType );
#
# - ARGS
#	*article	Articleʸ����
#	$textType	���Ϸ���
#
# - DESCRIPTION
#	$article�������ʸ������Ѵ����롥
#
sub secureArticle
{
    local( *article, $textType ) = @_;

    local( @articleTags ) =
	(
	 # ����̾, �Ĥ�ɬ�ܤ��ݤ�, ���Ѳ�ǽ��feature
	 'A',		1,	'HREF/NAME/TARGET',
	 'ADDRESS',		1,	'',
	 'B',		1,	'',
	 'BLOCKQUOTE',	1,	'',
	 'BR',		0,	'',
	 'CITE',		1,	'',
	 'CODE',		1,	'',
	 'DD',		0,	'',
	 'DIR',		1,	'',
	 'DL',		1,	'COMPACT',
	 'DT',		0,	'',
	 'EM',		1,	'',
	 'FONT',		1,	'SIZE/COLOR',
	 'H1',		1,	'ALIGN',
	 'H2',		1,	'ALIGN',
	 'H3',		1,	'ALIGN',
	 'H4',		1,	'ALIGN',
	 'H5',		1,	'ALIGN',
	 'H6',		1,	'ALIGN',
	 'HR',		0,	'SIZE/WIDTH/ALIGN',
	 'I',		1,	'',
	 'IMG',		0,	'SRC/ALT/ALIGN/WIDTH/HEIGHT/BORDER',
	 'KBD',		1,	'',
	 'LI',		0,	'TYPE/VALUE',
	 'LISTING',		1,	'',
	 'MENU',		1,	'',
	 'OL',		1,	'START',
	 'P',		0,	'ALIGN',
	 'PRE',		1,	'',
	 'SAMP',		1,	'',
	 'STRONG',		1,	'',
	 'TT',		1,	'',
	 'UL',		1,	'',
	 'VAR',		1,	'',
	 'XMP',		1,	'',
	 );
	
    local( %aNeedVec, %aFeatureVec, $tag );
    while( @articleTags )
    {
	$tag = shift( @articleTags );
	$aNeedVec{ $tag } = shift( @articleTags );
	$aFeatureVec{ $tag } = shift( @articleTags );
    }
    
    if (( !$SYS_TEXTTYPE ) || ( $textType eq $H_TTLABEL[0] ))
    {
	# pre-formatted
	&PlainArticleToPreFormatted( *article );
	# <URL:>�ν���
	$article = &ArticleEncode( $article );
	$article =~ s/<URL:([^>][^>]*)>/$1/gi;
    }
    elsif ( $textType eq $H_TTLABEL[1] )
    {
	# convert to html
	&PlainArticleToHtml( *article );
	# <URL:>�ν���
	$article = &ArticleEncode( $article );
	# secrurity check
	&cgi'SecureHtmlEx( *article, *aNeedVec, *aFeatureVec );
    }
    elsif ( $textType eq $H_TTLABEL[2] )
    {
	# <URL:>�ν���
	$article = &ArticleEncode( $article );
	# secrurity check
	&cgi'SecureHtmlEx( *article, *aNeedVec, *aFeatureVec );
    }
    else
    {
	&Fatal( 0, 'must not be reached...' );
    }
}


###
## AliasCheck - �桼�������ꥢ���Υ����å�
#
# - SYNOPSIS
#	AliasCheck($A, $N, $E, $U);
#
# - ARGS
#	$A	�����ꥢ��̾
#	$N	̾��
#	$E	E-Mail addr.
#	$U	URL
#
# - DESCRIPTION
#	�桼�������ꥢ���Υǡ���(�����ꥢ��̾��̾����E-Mail��URL)
#	������å����롥
#
# - RETURN
#	�ʤ�
#
sub AliasCheck
{
    local( $A, $N, $E, $U ) = @_;
    &CheckAlias( *A );
    &CheckName( *N );
    &CheckEmail( *E );
    &CheckURL( *U );
}


###
## CheckAlias - ʸ��������å�: �����ꥢ��
#
# - SYNOPSIS
#	CheckAlias(*String);
#
# - ARGS
#	*String		�����ꥢ��ʸ����
#
# - DESCRIPTION
#	�����ꥢ����ʸ��������å���Ԥʤ���
#	������ʸ������ä��饨�顼ɽ���롼����ء�
#	(���ץꥱ�������/UI��ʬΥ�����ۤ�����������?)
#
# - RETURN
#	�ʤ�
#
sub CheckAlias
{
    local( *String ) = @_;

    &Fatal( 2, '' ) if ( !$String );
    &Fatal( 7, $H_ALIAS ) if ( $String !~ ( /^\#/ ));

    # 1ʸ���������
    &Fatal( 7, $H_ALIAS ) if ( length( $String ) < 2 );

    &Fatal( 3, '' ) if ( $String =~ m/[\t\n]/o );
}


###
## CheckSubject - ʸ��������å�: Subject
#
# - SYNOPSIS
#	CheckSubject(*String);
#
# - ARGS
#	*String		Subjectʸ����
#
# - DESCRIPTION
#	Subject��ʸ��������å���Ԥʤ���
#	������ʸ������ä��饨�顼ɽ���롼����ء�
#	(���ץꥱ�������/UI��ʬΥ�����ۤ�����������?)
#
# - RETURN
#	�ʤ�
#
sub CheckSubject
{
    local( *String ) = @_;

    &Fatal( 2, '' ) unless $String;
    &Fatal( 3, '' ) if ( $String =~ m/[\t\n]/o );

    if ( !$SYS_TAGINSUBJECT )
    {
	&Fatal( 4, '' ) if ( $String =~ m/[<>]/o );
    }
}


###
## CheckName - ʸ��������å�: ��Ƽ�̾
#
# - SYNOPSIS
#	CheckName(*String);
#
# - ARGS
#	*String		��Ƽ�̾ʸ����
#
# - DESCRIPTION
#	��Ƽ�̾��ʸ��������å���Ԥʤ���
#	������ʸ������ä��饨�顼ɽ���롼����ء�
#	(���ץꥱ�������/UI��ʬΥ�����ۤ�����������?)
#
# - RETURN
#	�ʤ�
#
sub CheckName
{
    local( *String ) = @_;

    &Fatal( 2, '' ) if ( !$String );
    &Fatal( 3, '' ) if ( $String =~ m/[\t\n]/o );
}


###
## CheckEmail - ʸ��������å�: E-Mail addr.
#
# - SYNOPSIS
#	CheckEmail(*String);
#
# - ARGS
#	*String		E-Mail addr.ʸ����
#
# - DESCRIPTION
#	E-Mail addr.��ʸ��������å���Ԥʤ���
#	������ʸ������ä��饨�顼ɽ���롼����ء�
#	(���ץꥱ�������/UI��ʬΥ�����ۤ�����������?)
#
# - RETURN
#	�ʤ�
#
sub CheckEmail
{
    local( *String ) = @_;

    if ( $SYS_POSTERMAIL ) {
	&Fatal( 2, '' ) if ( !$String );
	# `@'�����äƤʤ��㥢����
	&Fatal( 7, 'E-Mail' ) if ( $String !~ /@/ );
    }
    &Fatal( 3, '' ) if ( $String =~ m/[\t\n]/o );
}


###
## CheckURL - ʸ��������å�: URL
#
# - SYNOPSIS
#	CheckURL(*String);
#
# - ARGS
#	*String		URLʸ����
#
# - DESCRIPTION
#	URL��ʸ��������å���Ԥʤ����������������å�������
#	��ȤΥ����å��ˤ�IsUrl��ƤӽФ���
#	������ʸ������ä��饨�顼ɽ���롼����ء�
#	(���ץꥱ�������/UI��ʬΥ�����ۤ�����������?)
#
# - RETURN
#	�ʤ�
#
sub CheckURL
{
    local( *String ) = @_;

    # http://�����ξ��϶��ˤ��Ƥ��ޤ���
    $String = '' if ( $String =~ m!^http://$!oi );
    &Fatal( 7, 'URL' ) if (( $String ne '' ) && ( !&IsUrl( $String )));
}


###
## IsUrl - URL�ι�¤������å�
#
# - SYNOPSIS
#	IsUrl($String);
#
# - ARGS
#	$String		URLʸ����
#
# - DESCRIPTION
#	URL��ʸ��������å���Ԥʤ���
#	ͽ����ꤵ�줿(@URL_SCHEME)Scheme�Τ�ΤǤ��뤫�ݤ�������å���
#	telnet��³���ϡ����ʤ���
#
# - RETURN
#	������URL�Ǥ����1�������Ǥʤ����0
#
sub IsUrl
{
    local( $String ) = @_;

    local( $IsUrl ) = 0;
    local( $Scheme );
    foreach $Scheme ( @URL_SCHEME )
    {
	$IsUrl = 1 if ( $String =~ m!^$Scheme://!i );
    }
    $IsUrl;
}


###
## GetFollowIdTree - ��ץ饤�������ڹ�¤�����
#
# - SYNOPSIS
#	GetFollowIdTree($Id, *Time);
#
# - ARGS
#	$Id	����ID
#	*Time	�ǽ���ƻ���ؤΥ�ե����
#
# - DESCRIPTION
#	���ꤵ�줿�����Υ�ץ饤�����򡤤���ID���ڹ�¤�ե����ޥåȤǼ��Ф���
#	*Time�ˤϡ��ڹ�¤��Ρ��ǿ��ε�������ƻ��֤����ꤵ��롥
#
#	��: * (�����ꤵ�줿����)
#	    +--a
#	    |  +--b
#	    |  |  +--c
#	    |  |  +--d
#	    |  |
#	    |  +--e
#	    |     +--f
#	    +--g
#	       +--h
#
#	�� ( a ( b ( c d ) e ( f ) ) g ( h ) )
#
# - RETURN
#	�ڹ�¤��ɽ���ꥹ��
#
sub GetFollowIdTree
{
    local( $Id, *Time ) = @_;
    # �Ƶ�Ū���ڹ�¤����Ф���
    return( '(', &GetFollowIdTreeMain( $Id, *Time ), ')' );
}

sub GetFollowIdTreeMain
{
    local( $Id, *Time ) = @_;
    local( @AidList, @Result, @ChildResult, $lastFollowMsgFid, $lastFollowMsgAids, $lastFollowMsgDate );

    # �Ƶ���߾��
    return if ( $Id eq '' );

    # �ե����������Ф�
    @AidList = split( /,/, $DB_AIDS{$Id} );

    # �ʤ�������
    return $Id if ( !@AidList );

    # �Ƶ�
    @Result = ( $Id, '(' );
    @ChildResult = ();
    foreach ( @AidList )
    {
	@ChildResult = &GetFollowIdTreeMain( $_, *Time );
	push( @Result, @ChildResult ) if @ChildResult;
    }

    # �Ǹ�Υե��������Υ����ॹ����פ򸫤�
    ( $lastFollowMsgFid, $lastFollowMsgAids, $lastFollowMsgDate ) = &GetArticlesInfo( $AidList[ $#AidList ] );
    $Time = $lastFollowMsgDate if ( $Time < $lastFollowMsgDate );

    return( @Result, ')' );
}


###
## GetReplySubject - ��ץ饤Subject������
#
# - SYNOPSIS
#	GetReplySubject($Id);
#
# - ARGS
#	$Id	����ID
#
# - DESCRIPTION
#	����Id�ε�������Subject���äƤ��ơ���Ƭ�ˡ�Re:�פ�1�Ĥ����Ĥ����֤���
#
# - RETURN
#	��������Subjectʸ����
#
sub GetReplySubject
{
    local( $Id ) = @_;

    local( $dFid, $dAids, $dDate, $dSubject ) = &GetArticlesInfo( $Id );

    # Re:���������
    $dSubject =~ s/^Re:\s*//oi;

    # TAG�ѥ��󥳡��ɤ��ơ�
    &TAGEncode( *dSubject );

    # ��Ƭ�ˡ�Re: �פ򤯤äĤ����֤���
    "Re: $dSubject";
}


###
## GetModifiedTime - ���뵭���κǽ���������(UTC)�����
#
# - SYNOPSIS
#	GetModifiedTime($Id, $Board);
#
# - ARGS
#	$Id		����ID
#	$Board		�Ǽ���ID
#
# - DESCRIPTION
#	����ID�ε������顤�ǽ�����UTC���äƤ��롥
#
# - RETURN
#	���ε����ե�����κǽ���������(UTC)
#
sub GetModifiedTime
{
    local( $Id, $Board ) = @_;

    # 86400 = 24 * 60 * 60
    $^T - ( -M &GetArticleFileName( $Id, $Board )) * 86400;
}


###
## GetDateTimeFormatFromUtc - UTC������֤�ɽ��ʸ��������
#
# - SYNOPSIS
#	GetDateTimeFormatFromUtc($Utc);
#
# - ARGS
#	$Utc		����(UTC)
#
# - DESCRIPTION
#	UTC���ʬ�ä�ʬ�䤷���ե����ޥåȤ���ʸ����Ȥ����֤���
#	�Ť��С�������KINOBOARDS�Ǥϡ�
#	DB��˻����ɽ��ʸ����(not UTC)�����Τޤ����äƤ��뤬��
#	���줬�Ϥ��줿���(UTC�Ǥʤ��ä����)�ϡ����Τޤ��֤���
#
# - RETURN
#	�����ɽ�魯ʸ����
#
sub GetDateTimeFormatFromUtc
{
    local( $Utc ) = @_;

    local( $Sec, $Min, $Hour, $Mday, $Mon, $Year, $Wday, $Yday, $Isdst );

    # �Ť�����Τ�Τ餷����
    return $Utc if ( $Utc !~ m/^\d+$/ );

    # �Ѵ�
    ( $Sec, $Min, $Hour, $Mday, $Mon, $Year, $Wday, $Yday, $Isdst ) = localtime( $Utc );

    sprintf( "%d/%d/%d(%02d:%02d)", $Year, $Mon + 1, $Mday, $Hour, $Min );

    # for MM/DD
    # sprintf( "%d/%d(%02d:%02d)", $Mon + 1, $Mday, $Hour, $Min );

    # for Y2k!
    # sprintf( "%d/%d/%d(%02d:%02d)", $Year+1900, $Mon + 1, $Mday, $Hour, $Min );
}


###
## GetUtcFromOldDateTimeFormat - �����UTC�ؤ�������
#
# - SYNOPSIS
#	GetUtcFromOldDateTimeFormat($Time);
#
# - ARGS
#	$Time		���֤�ɽ�魯ʸ����
#
# - DESCRIPTION
#	�Ť��С�������KINOBOARDS�Ǥϡ�
#	DB��˻����ɽ��ʸ���󤬤��Τޤ�(UTC�Ǥʤ�)���äƤ��롥
#	���줬�Ϥ��줿����Ŭ����UTC(854477921 = 97/01/29 03:58)���֤���
#	UTC���Ϥ��줿�餽�Τޤޤ���UTC���֤���
#
# - RETURN
#	����(UTC)
#
sub GetUtcFromOldDateTimeFormat
{
    local( $Time ) = @_;

    # �����餷��
    return $Time if ( $Time =~ m/^\d+$/ );

    # Ŭ��
    854477921;
}


###
## DQEncode/DQDecode - �ü�ʸ����Encode��Decode
#
# - SYNOPSIS
#	DQEncode($Str);
#	DQDecode($Str);
#
# - ARGS
#	$Str	Encode/Decode����ʸ����
#
# - DESCRIPTION
#	HTML���ü�ʸ��(", >, <, &)��Encode/Decode���롥
#
# - RETURN
#	Encode/Decode����ʸ����
#
sub DQEncode
{
    local( $Str ) = @_;
    $Str =~ s/\"/__dq__/go;
    $Str =~ s/\>/__gt__/go;
    $Str =~ s/\</__lt__/go;
    $Str =~ s/\&/__amp__/go;
    $Str;
}

sub DQDecode
{
    local( $Str ) = @_;
    $Str =~ s/__dq__/\"/go;
    $Str =~ s/__gt__/\>/go;
    $Str =~ s/__lt__/\</go;
    $Str =~ s/__amp__/\&/go;
    $Str;
}


###
## HTMLEncode/HTMLDecode - �ü�ʸ����HTML��Encode��Decode
#
# - SYNOPSIS
#	HTMLEncode($Str);
#	HTMLDecode($Str);
#
# - ARGS
#	$Str	HTML��Encode/Decode����ʸ����
#
# - DESCRIPTION
#	HTML���ü�ʸ��(", >, <, &)��HTML�Ѥ�Encode/Decode���롥
#
# - RETURN
#	Encode/Decode����ʸ����
#
sub HTMLEncode
{
    local( $_ ) = @_;
    s/\&/&amp;/go;
    s/\"/&quot;/go;
    s/\>/&gt;/go;
    s/\</&lt;/go;
    $_;
}

sub HTMLDecode
{
    local( $_ ) = @_;
    s/&quot;/\"/gio;
    s/&gt;/\>/gio;
    s/&lt;/\</gio;
    s/&amp;/\&/gio;
    $_;
}


###
## TAGEncode - �ü�ʸ����TAG��������Encode
#
# - SYNOPSIS
#	TAGEncode( *str );
#
# - ARGS
#	*str	TAG��������Encode����ʸ����
#
# - DESCRIPTION
#	TAG�����ߡ�<input value="������ʸ����">���Ѥˡ�"��&���������
#	Encode�ȸ����ʤ��顤���ΤȤ���Decode���뤳�ȤϤǤ�����
#	�����������Τ�
#
# - RETURN
#	Encode����ʸ����
#
sub TAGEncode
{
    local( *str ) = @_;
    $str =~ s/[\&\"]//go;		# ���ѤΤ�����Ѵ�
    $str =~ s/<[^>]*>//go;		# ���ѤΤ�����Ѵ�
}


###
###
## ArticleEncode - ������Encode
#
# - SYNOPSIS
#	ArticleEncode($Article);
#
# - ARGS
#	$Article	Encode���뵭����ʸ
#
# - DESCRIPTION
#	�������URL(<URL:��>)�򡤥�󥯤��Ѵ����롥
#
# - RETURN
#	Encode���줿ʸ����
#
sub ArticleEncode
{
    local( $article ) = @_;

    local( $ret ) = $article;
    local( $url, $urlMatch, $str, @cache );
    while ( $article =~ m/<URL:([^>][^>]*)>/gi )
    {
	$url = $1;
	( $urlMatch = $url ) =~ s/([?+*^\\\[\]\|()])/\\$1/go;
	next if ( grep( /^$urlMatch$/, @cache ));
	push( @cache, $url );
	$str = "<URL:$url>";
	$str = &TagA( $url, $str ) if ( &IsUrl( $urlMatch ));
	$ret =~ s/<URL:$urlMatch>/$str/gi;
    }

    $ret;
}


###
## PlainArticleToPreFormatted - Plain������pre formatted text���Ѵ�
#
# - SYNOPSIS
#	PlainArticleToPreFormatted(*Article);
#
# - ARGS
#	*Article	�Ѵ����뵭����ʸ
#
# - DESCRIPTION
#	������Ƭ��������̵��̣�ʲ��Ԥ��������
#	������HTML encode���롥
#	���Τ�<pre>��</pre>�ǰϤࡥ
#	*Article���˲����롥
#
# - RETURN
#	�ʤ�
#
sub PlainArticleToPreFormatted
{
    local( *Article ) = @_;

    $Article =~ s/\n*$//o;
    $Article =~ s/<URL:([^>][^>]*)>/__URL__$COLSEP$1$COLSEP/gi;
    $Article = &HTMLEncode( $Article );	# no tags are allowed.
    $Article =~ s/__URL__$COLSEP([^$COLSEP][^$COLSEP]*)$COLSEP/<URL:$1>/gi;
    $Article = "<pre>\n" . $Article . "</pre>";
}


###
## PlainArticleToHtml - Plain������HTML���Ѵ�
#
# - SYNOPSIS
#	PlainArticleToHtml(*Article);
#
# - ARGS
#	*Article	�Ѵ����뵭����ʸ
#
# - DESCRIPTION
#	����������̵��̣�ʲ��Ԥ��������
#	�������<p>�ǰϤࡥ
#	*Article���˲����롥
#
# - RETURN
#	�ʤ�
#
sub PlainArticleToHtml
{
    local( *Article ) = @_;
    $Article =~ s/^\n*//o;
    $Article =~ s/\n*$//o;
    $Article =~ s/\n/<br>\n/go;
    $Article =~ s/<br>\n<br>\n(<br>\n)*/<\/p>\n\n<p>/go;
    $Article = "<p>$Article</p>";
}


###
## DeleteArticle - �����κ��
#
# - SYNOPSIS
#	DeleteArticle($Id, $ThreadFlag);
#
# - ARGS
#	$Id		�������ID
#	$Board		�Ǽ���ID
#	$ThreadFlag	��ץ饤��ä����ݤ�
#
# - DESCRIPTION
#	������٤�����ID����������塤DB�򹹿����롥
#
# - RETURN
#	�ʤ�
#
sub DeleteArticle
{
    local( $Id, $Board, $ThreadFlag ) = @_;

    local( $Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $dId, @Target, $TargetId );

    # ��������μ���
    ( $Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url ) = &GetArticlesInfo( $Id );

    # �ǡ����ν񤭴���(ɬ�פʤ�̼��)
    @Target = ( $Id );
    foreach $TargetId ( @Target )
    {
	foreach ( 0 .. $#DB_ID )
	{
	    # ID����Ф�
	    $dId = $DB_ID[$_];
	    # �ե��������ꥹ�Ȥ��椫�顤������뵭����ID�������
	    $DB_AIDS{$dId} = join( ',', grep(( !/^$TargetId$/o ), split( /,/, $DB_AIDS{$dId} )));
	    # ������������������ID�������
	    $DB_FID{$dId} = '' if ( $DB_FID{$dId} eq $TargetId );
	    $DB_FID{$dId} =~ s/,$TargetId,.*$//;
	    $DB_FID{$dId} =~ s/^$TargetId,.*$//;
	    $DB_FID{$dId} =~ s/,$TargetId$//;
	    # ̼���оݤȤ���
	    push( @Target, split( /,/, $DB_AIDS{$dId} )) if ( $ThreadFlag && ( $dId eq $TargetId ));
	}
    }

    # DB�򹹿����롥
    &DeleteArticleFromDbFile( $Board, *Target );
}


###
## SupersedeArticle - ��������������
#
# - SYNOPSIS
#	SupersedeArticle;
#
# - ARGS
#	�ʤ�
#
# - DESCRIPTION
#	�������������롥
#
# - RETURN
#	�ʤ�
#
sub SupersedeArticle
{
    local( $Board, $Id, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail ) = @_;

    local( $SupersedeId, $File, $SupersedeFile );

    # ���Ϥ��줿��������Υ����å�
    &CheckArticle( $Board, *Name, *Email, *Url, *Subject, *Icon, *Article );

    # DB�ե����������
    $SupersedeId = &SupersedeDbFile( $Board, $Id, $^T, $Subject, $Icon, $cgi'REMOTE_HOST, $Name, $Email, $Url, $Fmail );

    # ex. ��100�ע���100_5��
    $File = &GetArticleFileName( $Id, $Board );
    $SupersedeFile = &GetArticleFileName( sprintf( "%s_%s", $Id, $SupersedeId ), $Board );
    rename( $File, $SupersedeFile ) || &Fatal( 14, "$File -&gt; $SupersedeFile" );

    # �����Υե�����κ���
    &MakeArticleFile( $TextType, $Article, $Id, $Board );

    $Id;
}


###
## ReLinkExec - �����Τ��������»�
#
# - SYNOPSIS
#	ReLinkExec($FromId, $ToId, $Board);
#
# - ARGS
#	$FromId		��������������ID
#	$ToId		���������赭��ID
#	$Board		�Ǽ���ID
#
# - DESCRIPTION
#	�������ץ饤-�������ط��򤫤������롥
#
# - RETURN
#	�ʤ�
#
sub ReLinkExec
{
    local( $FromId, $ToId, $Board ) = @_;

    local( $dId, @Daughters, $DaughterId );

    # �۴ĵ����ζػ�
    &FatalPriv( 50, '' ) if ( grep( /^$FromId$/, split( /,/, $DB_FID{$ToId} )));

    # �ǡ����񤭴���
    foreach ( 0 .. $#DB_ID )
    {
	# ID����Ф�
	$dId = $DB_ID[$_];
	# �ե��������ꥹ�Ȥ��椫�顤��ư���뵭����ID�������
	$DB_AIDS{$dId} = join( ',', grep(( !/^$FromId$/o ), split( /,/, $DB_AIDS{$dId} )));
    }

    # ɬ�פʤ�̼��Ȥ�����Ƥ���
    @Daughters = split( /,/, $DB_AIDS{$FromId} ) if $DB_FID{$FromId};

    # ���������Υ�ץ饤����ѹ�����
    if ( $ToId eq '' )
    {
	$DB_FID{$FromId} = '';
    }
    elsif ( $DB_FID{$ToId} eq '' )
    {
	$DB_FID{$FromId} = "$ToId";
    }
    else
    {
	$DB_FID{$FromId} = "$ToId,$DB_FID{$ToId}";
    }

    # ����������̼�ˤĤ��Ƥ⡤��ץ饤����ѹ�����
    while ( $DaughterId = shift( @Daughters ))
    {
	# ¹̼��ġ�
	push( @Daughters, split( /,/, $DB_AIDS{$DaughterId} ));
	# �񤭴���
	if (( $DB_FID{$DaughterId} eq $FromId )
	    || ( $DB_FID{$DaughterId} =~ /^$FromId,/ ))
	{
	    $DB_FID{$DaughterId} = $DB_FID{$FromId} ? "$FromId,$DB_FID{$FromId}" : "$FromId";
	}
	elsif (( $DB_FID{$DaughterId} =~ /^(.*),$FromId$/ )
	       || ( $DB_FID{$DaughterId} =~ /^(.*),$FromId,/ ))
	{
	    $DB_FID{$DaughterId} = $DB_FID{$FromId} ? "$1,$FromId,$DB_FID{$FromId}" : "$1,$FromId";
	}
    }

    # ��ץ饤��ˤʤä������Υե������������ɲä���
    $DB_AIDS{$ToId} = ( $DB_AIDS{$ToId} ne '' ) ? "$DB_AIDS{$ToId},$FromId" : "$FromId";

    # ����DB�򹹿�����
    &UpdateArticleDb( $Board );

    # DB�񤭴������Τǡ�����å��夷ľ��
    &DbCache( $Board );
}


###
## ReOrderExec - �����ΰ�ư�»�
#
# - SYNOPSIS
#	ReOrderExec($FromId, $ToId, $Board);
#
# - ARGS
#	$FromId		��ư������ID
#	$ToId		��ư�赭��ID
#	$Board		�Ǽ���ID
#
# - DESCRIPTION
#	���ꤵ�줿�����򡤻��ꤵ�줿�����μ��˰�ư���롥
#
# - RETURN
#	�ʤ�
#
sub ReOrderExec
{
    local( $FromId, $ToId, $Board ) = @_;

    local( @Move );

    # ��ư���뵭�������򽸤��
    @Move = ( $FromId, &CollectDaughters( $FromId ));

    # ��ư������
    &ReOrderArticleDb( $Board, $ToId, *Move );

    # DB�񤭴������Τǡ�����å��夷ľ��
    &DbCache( $Board );
}


###
## CollectDaughters - ̼�Ρ��ɤΥꥹ�Ȥ򽸤��
#
# - SYNOPSIS
#	CollectDaughters($Id);
#
# - ARGS
#	$Id		����ID
#
# - DESCRIPTION
#	̼�Ρ��ɤΥꥹ�Ȥ򽸤��
#
# - RETURN
#	̼�Ρ��ɽ���Υꥹ��
#
sub CollectDaughters
{
    local( $Id ) = @_;
    local( @Return );
    foreach ( split(/,/, $DB_AIDS{$Id} ))
    {
	push( @Return, $_ );
	push( @Return, &CollectDaughters( $_ )) if ( $DB_AIDS{$_} ne '' );
    }
    @Return;
}


###
## GetNewArticleId - ���嵭��ID�η���
#
# - SYNOPSIS
#	GetNewArticleId($Board);
#
# - ARGS
#	$Board		�Ǽ���ID
#
# - DESCRIPTION
#	����κǿ�����ID��1���䤷���������������ֹ���֤���
#
# - RETURN
#	���嵭����ID
#
sub GetNewArticleId
{
    local( $Board ) = @_;
    &GetArticleId( $Board ) + 1;
}


######################################################################
# �ǡ�������ץ���ơ������


###
## DbCache - ����DB�����ɤ߹���
#
# - SYNOPSIS
#	DbCache($Board);
#
# - ARGS
#	$Board		�Ǽ���ID
#
# - DESCRIPTION
#	��˵�ư���˸ƤӽФ��졤����DB�����Ƥ�����ѿ��˥���å��夹�롥
#
# - RETURN
#	�ʤ�
#
$BOARD_DB_CACHE = 0;

sub DbCache
{
    return if $BOARD_DB_CACHE;

    local( $Board ) = @_;

    local( $DBFile, $dId, $dFid, $dAids, $dDate, $dTitle, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail );

    @DB_ID = %DB_FID = %DB_AIDS = %DB_DATE = %DB_TITLE = %DB_ICON = %DB_REMOTEHOST = %DB_NAME = %DB_EMAIL = %DB_URL = %DB_FMAIL = %DB_NEW = ();

    local( $i ) = 0;
    $DBFile = &GetPath( $Board, $DB_FILE_NAME );
    open( DB, "<$DBFile" ) || &Fatal( 1, $DBFile );
    while ( <DB> )
    {
	next if (/^\#/o || /^$/o);
	chop;
	( $dId, $dFid, $dAids, $dDate, $dTitle, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail ) = split( /\t/, $_, 11 );
	next if ( $dId eq '' );

	$DB_ID[$i++] = $dId;
	$DB_FID{$dId} = $dFid;
	$DB_AIDS{$dId} = $dAids;
	$DB_DATE{$dId} = $dDate || &GetModifiedTime($dId, $Board);
	$DB_TITLE{$dId} = $dTitle || $dId;
	$DB_ICON{$dId} = $dIcon;
	$DB_REMOTEHOST{$dId} = $dRemoteHost;
	$DB_NAME{$dId} = $dName || $MAINT_NAME;
	$DB_EMAIL{$dId} = $dEmail;
	$DB_URL{$dId} = $dUrl;
	$DB_FMAIL{$dId} = $dFmail;
    }
    close DB;

    if ( $SYS_NEWICON )
    {
	local( $from ) = ( $#DB_ID >= $SYS_NEWICON )?
	    $#DB_ID - $SYS_NEWICON + 1 : 0;
	foreach ( $from .. $#DB_ID ) { $DB_NEW{ $DB_ID[$_] } = 1; }
    }

    $BOARD_DB_CACHE = 1;		# cached
}


###
## GetArticlesInfo - ����DB���ɤ߹���
#
# - SYNOPSIS
#	GetArticlesInfo($Id);
#
# - ARGS
#	$Id	����ID
#
# - DESCRIPTION
#	����DB���ɤ߹���ǡ��������Ф���
#	�ºݤϥ���å��夫���ɤ߽Ф�������
#
# - RETURN
#	��������Υꥹ��
#		��ץ饤������ID
#		���ε����˥�ץ饤����������ID�Υꥹ��(��,�׶��ڤ�)
#		��ƻ���(UTC)
#		Subject
#		��������ID
#		��ƥۥ���
#		��Ƽ�̾
#		��Ƽ�E-Mail
#		��Ƽ�URL
#		��ץ饤�����ä�������ƼԤ˥ᥤ������뤫�ݤ�
#
sub GetArticlesInfo
{
    local( $Id ) = @_;
    ( $DB_FID{$Id}, $DB_AIDS{$Id}, $DB_DATE{$Id}, $DB_TITLE{$Id}, $DB_ICON{$Id}, $DB_REMOTEHOST{$Id}, $DB_NAME{$Id}, $DB_EMAIL{$Id}, $DB_URL{$Id}, $DB_FMAIL{$Id} );
}


###
## AddDBFile - ����DB�ؤ��ɲ�
#
# - SYNOPSIS
#	AddDBFile($Id, $Board, $Fid, $InputDate, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail);
#
# - ARGS
#	$Id		����ID
#	$Board		�Ǽ���ID
#	$Fid		��ץ饤���ε���ID
#	$InputDate	�񤭹�������(UTC)
#	$Subject	Subject
#	$Icon		��������ID
#	$RemoteHost	�񤭹��ߥۥ���(IP addr.��FQDN����http�����м���)
#	$Name		��Ƽ�̾
#	$Email		��Ƽ�E-Mail addr.
#	$Url		��Ƽ�URL
#	$Fmail		��ץ饤���˥ᥤ������뤫�ݤ�(''/'on')
#
# - DESCRIPTION
#	����DB�˵������ɲä��롥
#
# - RETURN
#	�ʤ�
#
sub AddDBFile
{
    local( $Id, $Board, $Fid, $InputDate, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail ) = @_;

    local( $dId, $dFid, $dAids, $dInputDate, $dSubject, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail, $mdName, $mdEmail, $mdInputDate, $mdSubject, $mdIcon, $mdId, $FidList, $FFid, $File, $TmpFile, @FollowMailTo, @FFid, @ArriveMail );

    # ��ץ饤���Υ�ץ饤�������äƤ���
    if ( $Fid ne '' )
    {
	( $FFid ) = &GetArticlesInfo( $Fid );
	@FFid = split( /,/, $FFid );
    }

    $FidList = $Fid;

    $File = &GetPath( $Board, $DB_FILE_NAME );
    $TmpFile = &GetPath( $Board, "$DB_FILE_NAME.$TMPFILE_SUFFIX$$" );
    open( DBTMP, ">$TmpFile" ) || &Fatal( 1, $TmpFile );
    open( DB, "<$File" ) || &Fatal( 1, $File );
    while ( <DB> )
    {
	print( DBTMP "$_" ), next if ( /^\#/o || /^$/o );
	chop;

	( $dId, $dFid, $dAids, $dInputDate, $dSubject, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail ) = split( /\t/, $_ );
	
	# �ե����赭�������Ĥ��ä��顤
	if (( $dId ne '' ) && ( $dId eq $Fid ))
	{
	    # ���ε����Υե�������ID�ꥹ�Ȥ˲ä���(����޶��ڤ�)
	    if ( $dAids ne '' )
	    {
		$dAids .= ",$Id";
	    }
	    else
	    {
		$dAids = $Id;
	    }

	    # �������Υե�����ꥹ�Ȥ��äƤ��Ƹ�������ä���
	    # �������Υե�����ꥹ�Ȥ���
	    if ( $dFid ne '' )
	    {
		$FidList = "$dId,$dFid";
	    }

	    if ( $SYS_MAIL & 2 )
	    {
		# �ᥤ�������Τ���˥���å���
		$mdName = $dName;
		$mdEmail = $dEmail;
		$mdInputDate = $dInputDate;
		$mdSubject = $dSubject;
		$mdIcon = $dIcon;
		$mdId = $dId;
		push( @FollowMailTo, $dEmail ) if ( $dFmail ne '' );
	    }
	}

	# DB�˽񤭲ä���
	printf( DBTMP "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n", $dId, $dFid, $dAids, $dInputDate, $dSubject, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail );

	# ��ץ饤���Υ�ץ饤�������ĥᥤ��������ɬ�פ�����С��������¸
	if (( $SYS_MAIL & 2 ) && @FFid && $dFmail && $dEmail && ( grep( /^$dId$/, @FFid )) && ( !grep( /^$dEmail$/, @FollowMailTo ))) {
	    push( @FollowMailTo, $dEmail );
	}
    }

    # �����������Υǡ�����񤭲ä��롥
    printf( DBTMP "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n", $Id, $FidList, '', $InputDate, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail );

    # close Files.
    close DB;
    close DBTMP;

    # DB�򹹿�����
    rename( $TmpFile, $File ) || &Fatal( 14, "$TmpFile -&gt; $File" );

    # ɬ�פʤ���Ƥ����ä����Ȥ�ᥤ�뤹��
    if ( $SYS_MAIL & 1 )
    {
	&GetArriveMailTo( 0, $Board, *ArriveMail );
	&ArriveMail( $Name, $Email, $Subject, $Icon, $Id, @ArriveMail ) if @ArriveMail;
    }

    # ɬ�פʤ�ȿ�������ä����Ȥ�ᥤ�뤹��
    if (( $SYS_MAIL & 2 ) && @FollowMailTo )
    {
	&FollowMail( $mdName, $mdEmail, $mdInputDate, $mdSubject, $mdIcon, $mdId, $Name, $Email, $Subject, $Icon, $Id, @FollowMailTo );
    }
}


###
## UpdateArticleDb - ����DB��������
#
# - SYNOPSIS
#	UpdateArticleDb($Board);
#
# - ARGS
#	$Board		�Ǽ���ID
#
# - DESCRIPTION
#	����DB�򡤿����ʵ����ǡ��������������롥
#	�񤭹��൭���ǡ����ϥ���å��夵��Ƥ����Ρ�
#
# - RETURN
#	�ʤ�
#
sub UpdateArticleDb
{
    local( $Board ) = @_;

    local( $File, $TmpFile, $dId );

    $File = &GetPath($Board, $DB_FILE_NAME);
    $TmpFile = &GetPath( $Board, "$DB_FILE_NAME.$TMPFILE_SUFFIX$$" );
    open( DBTMP, ">$TmpFile" ) || &Fatal( 1, $TmpFile );
    open( DB, "<$File" ) || &Fatal( 1, $File );
    while ( <DB> )
    {
	print( DBTMP "$_" ), next if ( /^\#/o || /^$/o );

	# Id����Ф�
	chop;
	( $dId = $_ ) =~ s/\t.*$//;

	# DB�˽񤭲ä���
	printf( DBTMP "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n", $dId, $DB_FID{$dId}, $DB_AIDS{$dId}, $DB_DATE{$dId}, $DB_TITLE{$dId}, $DB_ICON{$dId}, $DB_REMOTEHOST{$dId}, $DB_NAME{$dId}, $DB_EMAIL{$dId}, $DB_URL{$dId}, $DB_FMAIL{$dId} );
    }

    # close Files.
    close DB;
    close DBTMP;

    # DB�򹹿�����
    rename( $TmpFile, $File ) || &Fatal( 14, "$TmpFile -&gt; $File" );
}


###
## DeleteArticleFromDbFile - ����DB�ι���
#
# - SYNOPSIS
#	DeleteArticleFromDbFile($Board, *Target);
#
# - ARGS
#	$Board		�Ǽ���ID
#	*Target		������뵭��ID�Υꥹ��
#
# - DESCRIPTION
#	����DB������ꤵ�줿�������Υ���ȥ�������롥
#
# - RETURN
#	�ʤ�
#
sub DeleteArticleFromDbFile
{
    local( $Board, *Target ) = @_;

    local( $File, $TmpFile, $dId );

    $File = &GetPath( $Board, $DB_FILE_NAME );
    $TmpFile = &GetPath( $Board, "$DB_FILE_NAME.$TMPFILE_SUFFIX$$" );
    open( DBTMP, ">$TmpFile" ) || &Fatal( 1, $TmpFile );
    open( DB, "<$File" ) || &Fatal( 1, $File );
    while ( <DB> )
    {
	print( DBTMP "$_" ), next if ( /^\#/o || /^$/o );

	# Id����Ф�
	chop;
	( $dId = $_ ) =~ s/\t.*$//;

	# ���������ϥ����ȥ�����
	print( DBTMP "#" ) if ( grep( /^$dId$/, @Target ));
	printf( DBTMP "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n", $dId, $DB_FID{$dId}, $DB_AIDS{$dId}, $DB_DATE{$dId}, $DB_TITLE{$dId}, $DB_ICON{$dId}, $DB_REMOTEHOST{$dId}, $DB_NAME{$dId}, $DB_EMAIL{$dId}, $DB_URL{$dId}, $DB_FMAIL{$dId} );

    }

    # close Files.
    close DB;
    close DBTMP;

    # DB�򹹿�����
    rename( $TmpFile, $File ) || &Fatal( 14, "$TmpFile -&gt; $File" );
}


###
## ReOrderArticleDb - ����DB�ν���ѹ�
#
# - SYNOPSIS
#	ReOrderArticleDb($Board, $Id, *Move);
#
# - ARGS
#	$Board		�Ǽ���ID
#	$Id		��ư�赭��ID
#	*Move		��ư���뵭�����Υꥹ�ȤؤΥ�ե����
#
# - DESCRIPTION
#	���ꤵ�줿�������򡤻��ꤵ�줿�����β��˰�ư���롥
#	�ֲ��פ�DB����褫�夫�ϡ����夬�夫�������˰ͤ�ۤʤ롥
#
# - RETURN
#	�ʤ�
#
sub ReOrderArticleDb
{
    local( $Board, $Id, *Move ) = @_;

    local( $File, $TmpFile, $dId, $TopFlag );

    # ��Ƭ�ե饰
    $TopFlag = 1;

    $File = &GetPath( $Board, $DB_FILE_NAME );
    $TmpFile = &GetPath( $Board, "$DB_FILE_NAME.$TMPFILE_SUFFIX$$" );
    open( DBTMP, ">$TmpFile" ) || &Fatal( 1, $TmpFile );
    open( DB, "<$File" ) || &Fatal( 1, $File );
    while ( <DB> )
    {
	print( DBTMP "$_" ), next if ( /^\#/o );
	print( DBTMP "$_" ), next if ( /^$/o );

	# Id����Ф�
	chop;
	( $dId = $_ ) =~ s/\t.*$//;

	# ��ư�����ۤϼ�����
	next if ( grep( /^$dId$/, @Move ));

	# ��Ƭ�ˤ�����ν���(���夬�����ξ��)
	if (( $Id eq '' ) && ( $SYS_BOTTOMTITLE == 1 ) && ( $TopFlag == 1 ))
	{
	    $TopFlag = 0;
	    foreach ( @Move )
	    {
		printf( DBTMP "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n", $_, $DB_FID{$_}, $DB_AIDS{$_}, $DB_DATE{$_}, $DB_TITLE{$_}, $DB_ICON{$_}, $DB_REMOTEHOST{$_}, $DB_NAME{$_}, $DB_EMAIL{$_}, $DB_URL{$_}, $DB_FMAIL{$_} );
	    }
	}

	# ��ư�褬�����顤��˽񤭹���(���夬�塤�ξ��)
	if (( $SYS_BOTTOMTITLE == 0 ) && ( $dId eq $Id ))
	{
	    foreach ( @Move )
	    {
		printf( DBTMP "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n", $_, $DB_FID{$_}, $DB_AIDS{$_}, $DB_DATE{$_}, $DB_TITLE{$_}, $DB_ICON{$_}, $DB_REMOTEHOST{$_}, $DB_NAME{$_}, $DB_EMAIL{$_}, $DB_URL{$_}, $DB_FMAIL{$_} );
	    }
	}

	# DB�˽񤭲ä���
	printf( DBTMP "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n", $dId, $DB_FID{$dId}, $DB_AIDS{$dId}, $DB_DATE{$dId}, $DB_TITLE{$dId}, $DB_ICON{$dId}, $DB_REMOTEHOST{$dId}, $DB_NAME{$dId}, $DB_EMAIL{$dId}, $DB_URL{$dId}, $DB_FMAIL{$dId} );

	# ��ư�褬�����顤³���ƽ񤭹���(���夬�����ξ��)
	if (( $SYS_BOTTOMTITLE == 1 ) && ( $dId eq $Id ))
	{
	    foreach ( @Move )
	    {
		printf( DBTMP "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n", $_, $DB_FID{$_}, $DB_AIDS{$_}, $DB_DATE{$_}, $DB_TITLE{$_}, $DB_ICON{$_}, $DB_REMOTEHOST{$_}, $DB_NAME{$_}, $DB_EMAIL{$_}, $DB_URL{$_}, $DB_FMAIL{$_} );
	    }
	}
    }

    # ��Ƭ�ˤ�����ν���(���夬�塤�ξ��)
    if (( $Id eq '' ) && ( $SYS_BOTTOMTITLE == 0 ))
    {
	foreach ( @Move )
	{
	    printf( DBTMP "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n", $_, $DB_FID{$_}, $DB_AIDS{$_}, $DB_DATE{$_}, $DB_TITLE{$_}, $DB_ICON{$_}, $DB_REMOTEHOST{$_}, $DB_NAME{$_}, $DB_EMAIL{$_}, $DB_URL{$_}, $DB_FMAIL{$_} );
	}
    }

    # close Files.
    close DB;
    close DBTMP;

    # DB�򹹿�����
    rename( $TmpFile, $File ) || &Fatal( 14, "$TmpFile -&gt; $File" );
}


###
## MakeArticleFile - ������ʸDB�ؤ��ɲ�
#
# - SYNOPSIS
#	MakeArticleFile($TextType, $Article, $Id, $Board);
#
# - ARGS
#	$TextType	ʸ�񥿥���
#	$Article	��ʸ
#	$Id		����ID
#	$Board		�Ǽ���ID
#
# - DESCRIPTION
#	������ʸDB(�Ǽ���ID��Ʊ��̾���Υǥ��쥯�ȥ�)����ˡ�
#	ID��Ʊ��̾���Υե�����Ȥ��ơ�������ʸ����¸���롥
#
# - RETURN
#	�ʤ�
#
sub MakeArticleFile
{
    local( $TextType, $Article, $Id, $Board ) = @_;

    local( $File ) = &GetArticleFileName( $Id, $Board );

    open( TMP, ">$File" ) || &Fatal( 1, $File );
    printf( TMP "<!-- Kb-System-Id: %s/%s -->\n", $KB_VERSION, $KB_RELEASE);
    print( TMP "$Article\n" );
    close TMP;
}


###
## GetArticleBody - ������ʸDB���ɤ߹���
#
# - SYNOPSIS
#	GetArticleBody($Id, $Board, *ArticleBody);
#
# - ARGS
#	$Id		����ID
#	$BoardId	�Ǽ���ID
#	*ArticleBody	��ʸ�ƹԤ�����������ѿ��ؤΥ�ե����
#
# - DESCRIPTION
#	������ʸDB(�Ǽ���ID��Ʊ��̾���Υǥ��쥯�ȥ�)����Ρ�
#	ID��Ʊ��̾���Υե�������ɤ߽Ф���
#
# - RETURN
#	�ʤ�
#
sub GetArticleBody
{
    local( $Id, $Board, *ArticleBody ) = @_;

    local( $QuoteFile ) = &GetArticleFileName( $Id, $Board );
    open( TMP, "<$QuoteFile" ) || &Fatal( 1, $QuoteFile );
    while ( <TMP> )
    {
	push( @ArticleBody, $_ );
    }
    close TMP;
}


###
## GetArticleId - �����ֹ�DB���ɤ߹���
#
# - SYNOPSIS
#	GetArticleId($Board);
#
# - ARGS
#	$Board		�Ǽ���ID
#
# - DESCRIPTION
#	����κǿ�����ID���ɤ߽Ф���
#
# - RETURN
#	�ǿ�������ID
#
sub GetArticleId
{
    local( $Board ) = @_;

    local( $ArticleNumFile ) = &GetPath( $Board, $ARTICLE_NUM_FILE_NAME );
    local( $ArticleId );
    open( AID, "<$ArticleNumFile" ) || &Fatal( 1, $ArticleNumFile );
    chop( $ArticleId = <AID> );
    close AID;

    $ArticleId;
}


###
## WriteArticleId - �����ֹ�DB�ι���
#
# - SYNOPSIS
#	WriteArticleId($Id, $Board);
#
# - ARGS
#	$Id		�����˽񤭹��൭���ֹ�
#	$Board		�Ǽ���ID
#
# - DESCRIPTION
#	�����ֹ�DB�ι���
#
# - RETURN
#	�ʤ�
#
sub WriteArticleId
{
    local( $Id, $Board ) = @_;

    local( $File, $TmpFile, $OldArticleId );
    
    # �����Τ����˸Ť����ͤ��㤤! (��������ʤ���OK)
    $OldArticleId = &GetNewArticleId( $Board );
    &Fatal( 10, '' ) if (( $Id =~ /^\d+$/ ) && ( $Id < $OldArticleId ));

    $File = &GetPath( $Board, $ARTICLE_NUM_FILE_NAME );
    $TmpFile = &GetPath( $Board, "$ARTICLE_NUM_FILE_NAME.$TMPFILE_SUFFIX$$" );
    open( AID, ">$TmpFile" ) || &Fatal( 1, $TmpFile );
    print( AID "$Id\n" );
    close AID;

    rename( $TmpFile, $File ) || &Fatal( 14, "$TmpFile -&gt; $File" );
}


###
## GetArriveMailTo - �Ǽ����̿����ᥤ��������DB�����ɤ߹���
#
# - SYNOPSIS
#	GetArriveMailTo($CommentFlag, $Board, *ArriveMail);
#
# - ARGS
#	$CommentFlag	�����ȹԤ�ޤफ�ݤ�(0: �ޤޤʤ�, 1: �ޤ�)
#	$Board		�Ǽ���ID
#	*ArriveMail	������Υᥤ�륢�ɥ쥹�Υꥹ�ȤΥ�ե����
#
# - DESCRIPTION
#	�Ǽ����̿����ᥤ��������DB���ɤ߹��ࡥ
#	�ᥤ�륢�ɥ쥹�����������ݤ����Υ����å��ϡ����ڹԤʤ�ʤ���
#
# - RETURN
#	�ʤ�
#
sub GetArriveMailTo
{
    local($CommentFlag, $Board, *ArriveMail) = @_;
    local($ArriveMailFile);

    $ArriveMailFile = &GetPath( $Board, $ARRIVEMAIL_FILE_NAME );
    # �ե����뤬�ʤ�����Τޤ�
    open( ARMAIL, "<$ArriveMailFile" ) || return;
    while ( <ARMAIL> )
    {
	next if ((! $CommentFlag) && (/^\#/o || /^$/o));
	chop;
	push(@ArriveMail, $_);
    }
    close ARMAIL;
}


###
## UpdateArriveMailDb - �Ǽ����̿����ᥤ��������DB��������
#
# - SYNOPSIS
#	UpdateArriveMailDb($Board, *ArriveMail);
#
# - ARGS
#	$Board		�Ǽ���ID
#	*ArriveMail	������Υᥤ�륢�ɥ쥹�Υꥹ�ȤΥ�ե����
#			(�����ȡ����Ԥ�ޤޤ��)
#
# - DESCRIPTION
#	�Ǽ����̿����ᥤ��������DB�򡤿�����������ꥹ�Ȥǰ쿷���롥
#	�ᥤ�륢�ɥ쥹�����������ݤ����Υ����å��ϡ����ڹԤʤ�ʤ���
#
# - RETURN
#	�ʤ�
#
sub UpdateArriveMailDb
{
    local( $Board, *ArriveMail ) = @_;

    local( $File ) = &GetPath( $Board, $ARRIVEMAIL_FILE_NAME );
    local( $TmpFile ) = &GetPath( $Board, $ARRIVEMAIL_FILE_NAME );
    open( DBTMP, ">$TmpFile" ) || &Fatal( 1, $TmpFile );
    foreach ( @ArriveMail )
    {
	print( DBTMP "$_\n" );
    }
    close DBTMP;
    rename( $TmpFile, $File ) || &Fatal( 14, "$TmpFile -&gt; $File" );
}


###
## CacheAliasData - �桼��DB�����ɤ߹���
#
# - SYNOPSIS
#	CacheAliasData;
#
# - ARGS
#	�ʤ�
#
# - DESCRIPTION
#	�桼�������ꥢ���ե�������ɤ߹����Ϣ�������������ࡥ
#	����ѿ���%Name, %Email, %Host, %URL���˲����롥
#
# - RETURN
#	�ʤ�
#
sub CacheAliasData
{
    local( $A, $N, $E, $H, $U );

    # ������ࡥ
    open( ALIAS, "<$USER_ALIAS_FILE" ) || &Fatal( 1, $USER_ALIAS_FILE );
    while ( <ALIAS> )
    {
	next if ( /^$/o || /^[^#]/ );
	chop;

	( $A, $N, $E, $H, $U ) = split( /\t/, $_ );

	$Name{$A} = $N;
	$Email{$A} = $E;
	$Host{$A} = $H;
	$URL{$A} = $U;
    }
    close ALIAS;
}


###
## GetUserInfo - �桼��DB���ɤ߹���
#
# - SYNOPSIS
#	GetUserInfo($Alias);
#
# - ARGS
#	$Alias		��������桼��ID(�����ꥢ��)
#
# - DESCRIPTION
#	�桼��DB���顤�桼����̾�����ᥤ�롤URL���äƤ��롥
#
# - RETURN
#	�桼����̾�����ᥤ�롤URL�ν�Υꥹ�ȡ�
#
sub GetUserInfo
{
    local( $Alias ) = @_;

    local( $A, $N, $E, $H, $U, $rN, $rE, $rU );
    open( ALIAS, "<$USER_ALIAS_FILE" ) || &Fatal( 1, $USER_ALIAS_FILE );
    while ( <ALIAS> )
    {
	next if (/^$/o);
	chop;
	
	# ʬ��
	( $A, $N, $E, $H, $U ) = split( /\t/, $_ );
	
	# �ޥå����ʤ��㼡�ء�
	next if ( $A ne $Alias );
	
	$rN = $N;
	$rE = $E;
	$rU = $U;
    }
    close ALIAS;

    ( $rN, $rE, $rU );
}


###
## WriteAliasData - �桼��DB�ι���/�ɲ�
#
# - SYNOPSIS
#	WriteAliasData;
#
# - ARGS
#	�ʤ�
#
# - DESCRIPTION
#	�桼�������ꥢ���ե�����˥ǡ�����񤭽Ф���
#	%Name, %Email, %Host, %URL��ɬ�פȤ��롥
#	$Name�������Ƚ񤭹��ޤʤ���
#
# - RETURN
#	�ʤ�
#
sub WriteAliasData
{
    local( $TmpFile ) = "$USER_ALIAS_FILE.$TMPFILE_SUFFIX$$";
    local( $Alias );

    open( ALIAS, ">$TmpFile" ) || &Fatal( 1, $TmpFile );
    printf( ALIAS "<!-- Kb-System-Id: %s/%s -->\n", $KB_VERSION, $KB_RELEASE );
    foreach $Alias ( sort keys( %Name ))
    {
	printf(ALIAS "%s\t%s\t%s\t%s\t%s\n", $Alias, $Name{$Alias}, $Email{$Alias}, $Host{$Alias}, $URL{$Alias}) if $Name{$Alias};
    }
    close ALIAS;

    rename( $TmpFile, $USER_ALIAS_FILE ) || &Fatal( 14, "$TmpFile -&gt; $USER_ALIAS_FILE" );
}


###
## GetAllBoardInfo - �Ǽ���DB�����ɤ߹���
#
# - SYNOPSIS
#	GetAllBoardInfo(*BoardList, *BoardInfo);
#
# - ARGS
#	*BoardList	�Ǽ���ID-�Ǽ���̾��Ϣ������Υ�ե����
#	*BoardInfo	�Ǽ���ID-�Ǽ��ľ����Ϣ������Υ�ե����
#
# - DESCRIPTION
#	�Ǽ���DB���顤�Ǽ��ľ�����äƤ��롥
#
# - RETURN
#	�ʤ�
#
sub GetAllBoardInfo
{
    local( *BoardList, *BoardInfo ) = @_;

    local( $BoardId, $BName, $BInfo );

    open( ALIAS, "<$BOARD_ALIAS_FILE" ) || &Fatal( 1, $BOARD_ALIAS_FILE );
    while ( <ALIAS> )
    {
	next if ( /^\#/o || /^$/o );
	chop;
	( $BoardId, $BName, $BInfo ) = split( /\t/, $_, 3 );
	$BoardList{$BoardId} = $BName;
	$BoardInfo{$BoardId} = $BInfo;
    }
    close ALIAS;
}


###
## GetBoardInfo - �Ǽ���DB���ɤ߹���
#
# - SYNOPSIS
#	GetBoardInfo($Alias);
#
# - ARGS
#	$Alias		�Ǽ���ID
#
# - DESCRIPTION
#	�Ǽ���DB���顤�Ǽ��ľ�����äƤ��롥
#
# - RETURN
#	�Ǽ���̾
#
sub GetBoardInfo
{
    local( $Alias ) = @_;

    local( $dAlias, $dBoardName, $dBoardConf );

    open( ALIAS, "<$BOARD_ALIAS_FILE" ) || &Fatal( 1, $BOARD_ALIAS_FILE );
    while ( <ALIAS> )
    {
	next if ( /^\#/o || /^$/o );
	chop;
	( $dAlias, $dBoardName, $dBoardConf ) = split( /\t/, $_, 4 );
	if ( $Alias eq $dAlias ) {
	    close ALIAS;
	    return( $dBoardName, $dBoardConf );
	}
    }
    close ALIAS;

    &Fatal( 11, $Alias );
}


###
## CacheIconDb - ��������DB�����ɤ߹���
#
# - SYNOPSIS
#	CacheIconDb($Board);
#
# - ARGS
#	$Board		�Ǽ���ID
#
# - DESCRIPTION
#	��������DB���ɤ߹����Ϣ�������������ࡥ
#	����ѿ���@ICON_TITLE��%ICON_FILE��%ICON_HELP���˲����롥
#
# - RETURN
#	�ʤ�
#
$ICON_DB_CACHE = 0;

sub CacheIconDb
{
    return if $ICON_DB_CACHE;

    local( $Board ) = @_;
    local( $FileName, $IconTitle, $IconHelp );

    @ICON_TITLE = %ICON_FILE = %ICON_HELP = ();
    open( ICON, &GetIconPath( "$Board.$ICONDEF_POSTFIX" ))
	|| ( open( ICON, &GetIconPath( "$DEFAULT_ICONDEF" ))
	    || &Fatal( 1, &GetIconPath( "$DEFAULT_ICONDEF" )));
    while ( <ICON> )
    {
	next if ( /^\#/o || /^$/o );
	chop;
	( $FileName, $IconTitle, $IconHelp ) = split( /\t/, $_, 3 );

	push( @ICON_TITLE, $IconTitle );
	$ICON_FILE{$IconTitle} = $FileName;
	$ICON_HELP{$IconTitle} = $IconHelp;
    }
    close ICON;

    $ICON_DB_CACHE = 1;		# cached
}


###
## GetBoardHeader - �Ǽ��ĥإå�DB���ɤ߹���
#
# - SYNOPSIS
#	GetBoardHeader($Board, *BoardHeader);
#
# - ARGS
#	$BoardId	�Ǽ���ID
#	*BoardHeader	��ʸ�ƹԤ�����������ѿ��ؤΥ�ե����
#
# - DESCRIPTION
#	�Ǽ��ĥǥ��쥯�ȥ����Ρ��Ǽ��ĥإå��ե�������ɤ߽Ф���
#
# - RETURN
#	�ʤ�
#
sub GetBoardHeader
{
    local( $Board, *BoardHeader ) = @_;

    local( $File ) = &GetPath( $Board, $BOARD_FILE_NAME );
    open( HEADER, "<$File" ) || &Fatal( 1, $File );
    while ( <HEADER> )
    {
	s/__PROGRAM__/$PROGRAM/g;
	push( @BoardHeader, $_ );
    }
    close HEADER;
}


###
## GetArticleFileName - ������ʸDB�ե�����Υѥ�̾�μ���
#
# - SYNOPSIS
#	GetArticleFileName($Id, $Board);
#
# - ARGS
#	$Id		����ID
#	$Board		�Ǽ���ID
#
# - DESCRIPTION
#	�Ǽ���ID�ȵ���ID���顤����DB��Ρ������ե�����Υѥ�̾����Ф���
#	����ѿ�$MACPERL�򻲾Ȥ���MacPerl���б���
#
# - RETURN
#	�ѥ���ɽ��ʸ����
#
sub GetArticleFileName
{
    local( $Id, $Board ) = @_;

    # Board�����ʤ�Board�ǥ��쥯�ȥ��⤫�����С�
    # ���Ǥʤ���Х����ƥफ������
    if ( $MACPERL )
    {
	$Board? ":$Board:$Id" : "$Id";
    }
    else
    {
	$Board? "$Board/$Id" : "$Id";
    }
}


###
## GetPath - DB�ե�����Υѥ�̾�μ���
#
# - SYNOPSIS
#	GetPath($DbDir, $File);
#
# - ARGS
#	$DbDir		DB�ǥ��쥯�ȥ�(�Ǽ���ID, etc.)
#	$File		�ե�����̾
#
# - DESCRIPTION
#	DB�ǥ��쥯�ȥ�̾�ȥե�����̾���顤DB�ե�����Υѥ�̾����Ф���
#	����ѿ�$MACPERL�򻲾Ȥ���MacPerl���б���
#
# - RETURN
#	�ѥ���ɽ��ʸ����
#
sub GetPath
{
    local( $DbDir, $File ) = @_;

    if ( $MACPERL )
    {
	":$DbDir:$File";
    }
    else
    {
	"$DbDir/$File";
    }
}


###
## GetIconPath - ��������gifDB�ե�����Υѥ�̾�μ���
#
# - SYNOPSIS
#	GetIconPath($File);
#
# - ARGS
#	$File		��������gif�ե�����̾
#
# - DESCRIPTION
#	��������gif�ե�����Υѥ�̾����Ф���
#	����ѿ�$MACPERL�򻲾Ȥ���MacPerl���б���
#
# - RETURN
#	�ѥ���ɽ��ʸ����
#
sub GetIconPath
{
    local( $File ) = @_;

    if ( $MACPERL )
    {
	":$ICON_DIR:$File";
    }
    else
    {
	"$ICON_DIR/$File";
    }
}


###
## GetIconUrlFromTitle - ��������gif��URL�μ���
#
# - SYNOPSIS
#	GetIconUrlFromTitle($Icon, $Board);
#
# - ARGS
#	$Icon		��������ID
#	$Board		�Ǽ���ID
#
# - DESCRIPTION
#	��������ID���顤���Υ���������б�����gif�ե������URL�������
#
# - RETURN
#	URL��ɽ��ʸ����
#
sub GetIconUrlFromTitle
{
    local( $Icon, $Board ) = @_;

    local( $FileName, $Title, $TargetFile );

    open( ICON, &GetIconPath( "$Board.$ICONDEF_POSTFIX" ))
	|| ( open( ICON, &GetIconPath( "$DEFAULT_ICONDEF" ))
	    || &Fatal( 1, &GetIconPath( "$DEFAULT_ICONDEF" )));
    while ( <ICON> )
    {
	next if ( /^\#/o || /^$/o );
	chop;
	( $FileName, $Title ) = split( /\t/, $_, 3 );
	if ( $Title eq $Icon ) { $TargetFile = $FileName; }
    }
    close ICON;

    $TargetFile? "$ICON_DIR/$TargetFile" : '';
}


###
## SupersedeDbFile - ���������ε���DB�ؤν񤭹���
#
# - SYNOPSIS
#	SupersedeDbFile($Board, $Id, $InputDate, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail);
#
# - ARGS
#	$Board		�������뵭�����ޤޤ��Ǽ��Ĥ�ID
#	$Id		�������뵭����ID
#	$InputDate	��������(UTC)
#	$Subject	��������Subject
#	$Icon		����������������
#	$RemoteHost	���������񤭹��ߥۥ���̾
#	$Name		���������񤭹��ߥ桼��̾
#	$Email		���������񤭹��ߥ桼���ᥤ�륢�ɥ쥹
#	$Url		���������񤭹��ߥ桼��URL
#	$Fmail		��ץ饤���˥ᥤ����������뤫�ݤ�
#
# - DESCRIPTION
#	����������DB�ե�����˽񤭹��ߡ�aging����������ID���֤���
#
# - RETURN
#	aging����������ID��
#
sub SupersedeDbFile
{
    local( $Board, $Id, $InputDate, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail ) = @_;

    local( $SupersedeId, $dId, $dFid, $dAids, $dInputDate, $dSubject, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail, $File, $TmpFile );
    
    # initial version��1�ǡ�1���������Ƥ�����1��2����9��10��11����
    # later version��DB���ɬ����younger version���Ⲽ�˽и����롥
    # ���ʤ��10_2��10��10_1�ϡ�10_1��10_2��10�ν���¤֤�ΤȤ��롥
    $SupersedeId = 1;

    $File = &GetPath( $Board, $DB_FILE_NAME );
    $TmpFile = &GetPath( $Board, "$DB_FILE_NAME.$TMPFILE_SUFFIX$$" );
    open( DBTMP, ">$TmpFile" ) || &Fatal( 1, $TmpFile );
    open( DB, "<$File" ) || &Fatal( 1, $File );
    while ( <DB> )
    {
	print( DBTMP "$_" ), next if ( /^\#/o || /^$/o );
	chop;

	( $dId, $dFid, $dAids, $dInputDate, $dSubject, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail ) = split( /\t/, $_ );

	# later version�����Ĥ��ä��顤version�����ɤߤ��Ƥ�����
	$SupersedeId++ if ( "$dId" eq ( sprintf( "#-%s_%s", $Id, $SupersedeId )));

	# ���������κǿ��Ǥ����Ĥ��ä��顤
	if ( $dId eq $Id )
	{
	    # aging���Ƥ��ޤ�
	    printf( DBTMP "#-%s_%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n", $dId, $SupersedeId, $dFid, $dAids, $dInputDate, $dSubject, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail );

	    # ³���ƿ�����������񤭲ä���
	    printf( DBTMP "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n", $Id, $dFid, $dAids, $InputDate, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail );
	}
	else
	{
	    # DB�˽񤭲ä���
	    print( DBTMP "$_\n" );
	}
    }

    # close Files.
    close DB;
    close DBTMP;

    # DB�򹹿�����
    rename( $TmpFile, $File ) || &Fatal( 14, "$TmpFile -&gt; $File" );

    # �֤�
    $SupersedeId;
}
