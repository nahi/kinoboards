#!/usr/local/bin/perl
#!/usr/local/bin/perl5.00503-debug -d:DProf
#!/usr/local/bin/perl4.036


# ���Υե�������ѹ��Ϻ���2�սꡤ����4�ս�Ǥ��ʴĶ�����Ǥ��ˡ�
#
# 1. ������Ƭ�Ԥǡ�Perl�Υѥ�����ꤷ�ޤ�����#!�פ�³���ƻ��ꤷ�Ƥ���������

# 2. kb�ǥ��쥯�ȥ�Υե�ѥ�����ꤷ�Ƥ���������URL�ǤϤʤ����ѥ��Ǥ��ˡ�
#    �֥饦�����饢��������ǽ�ʥǥ��쥯�ȥ�Ǥʤ��Ƥ⤫�ޤ��ޤ���
#
$KBDIR_PATH = '/home/achilles/nakahiro/cvs_work/KB/tst/';
# $KBDIR_PATH = '/home/nahi/public_html';
# $KBDIR_PATH = 'd:\inetpub\wwwroot\kb';	# WinNT/Win9x�ξ��
# $KBDIR_PATH = 'foo:bar:kb';			# Mac�ξ��?

# 3. �����Ф�ư���Ƥ���ޥ���Win95/Mac�ξ�硤
#    $PC��1�����ꤷ�Ƥ��������������Ǥʤ���硤������������פǤ���
#
$PC = 0;	# for UNIX / WinNT
# $PC = 1;	# for Win95 / Mac

# 4. �������󤪤�ӥ������륷���ȥե�����򡤤��Υե�������̤Υǥ��쥯�ȥ��
#    �֤����ϡ������̥ǥ��쥯�ȥ��URL����ꤷ�Ƥ��������ʥѥ��ǤϤʤ���
#    URL�Ǥ��ˡ����ꤹ��URL�ϡ��֥饦�����饢��������ǽ�Ǥʤ���Ф����ޤ���
#    �ܥե������Ʊ���ǥ��쥯�ȥ��icon��style�ǥ��쥯�ȥ���֤����ϡ�
#    �ä˻��ꤷ�ʤ��Ƥ⤫�ޤ��ޤ���ʤ��Τޤޤ�OK�Ǥ��ˡ�
#
#    ���ꤷ��URL�Υǥ��쥯�ȥ���֤���Ƥ��롤
#      icon/*.gif����������ե�����Ȥ��ơ�
#      style/kbStyle.css���������륷���ȥե�����Ȥ��ơ�
#    ���줾�컲�Ȥ���ޤ���
#
# $KB_RESOURCE_URL = '/~nahi/kb/';


# �ʲ��Ͻ񤭴�����ɬ�פϤ���ޤ���


######################################################################


# $Id: kb.cgi,v 5.63 2000-03-03 14:26:41 nakahiro Exp $

# KINOBOARDS: Kinoboards Is Network Opened BOARD System
# Copyright (C) 1995-2000 NAKAMURA Hiroshi.
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
push( @INC, '.' );
$[ = 0;				# zero origined
$| = 1;				# pipe flushed
$COLSEP = "\377";
srand( $^T ^ ( $$ + ( $$ << 15 )));

# ����ѿ������
$HEADER_FILE = 'kb.ph';		# header file
$KB_VERSION = '1.0';		# version
$KB_RELEASE = '7��5';		# release
$CHARSET = 'euc';		# �����������Ѵ��ϹԤʤ�ʤ�
$ADMIN = 'admin';		# �ǥե��������
$GUEST = 'guest';		# �ǥե��������

# �ǥ��쥯�ȥ�
$SYS_DIR = '.';				# �����ƥ�ǥ��쥯�ȥ�
$ICON_DIR = 'idef';			# ������������ǥ��쥯�ȥ�
$UI_DIR = 'UI';				# UI�ǥ��쥯�ȥ�
$LOG_DIR = 'log';			# ���ǥ��쥯�ȥ�
$BOARDSRC_DIR = 'board';		# �Ǽ��ĥ������ǥ��쥯�ȥ�

# �ե�����
$BOARD_FILE = 'kinoboards';		# �Ǽ���DB
$CONF_FILE_NAME = 'kb.conf';		# �Ǽ�����configuratin�ե�����
$ARRIVEMAIL_FILE_NAME = 'kb.mail';	# �Ǽ����̿����ᥤ��������DB
$HEADER_FILE_NAME = 'kb.board';		# �����ȥ�ꥹ�ȥإå�DB
$DB_FILE_NAME = 'kb.db';		# ����DB
$ARTICLE_NUM_FILE_NAME = 'kb.aid';	# �����ֹ�DB
$USER_FILE = 'kb.user';			# �桼����DB
$DEFAULT_ICONDEF = 'all.idef';		# ��������DB
$LOCK_FILE = 'kb.lock';			# ��å��ե�����
$LOCK_FILE_B = '';			# �Ǽ����̥�å��ե�����
$ACCESS_LOG = 'access_log';		# �����������ե�����
$ERROR_LOG = 'error_log';		# ���顼���ե�����
# Suffix
$TMPFILE_SUFFIX = 'tmp';		# DB�ƥ�ݥ��ե������Suffix
$ICONDEF_POSTFIX = 'idef';		# ��������DB�ե������Suffix

# �꥽����URL
$RESOURCE_ICON = 'icon';		# ��������ǥ��쥯�ȥ�
$RESOURCE_STYLE = 'style';		# �������륷���ȥǥ��쥯�ȥ�
# �����¾�ˡ������ط��Ѳ����ʤɡ�����?

# CGI��Ʊ��ǥ��쥯�ȥ�ˤ���إå��ե�������ɤ߹���
require( $HEADER_FILE ) if ( -s "$HEADER_FILE" );

# �ᥤ��Υإå��ե�������ɤ߹���
if ( !$KBDIR_PATH || !chdir( $KBDIR_PATH ))
{
    print "Content-Type: text/plain; charset=EUC-JP\n\n";
    print "���顼���������ͤ�:\n";
    print "$0����Ƭ��ʬ���֤���Ƥ���\$KBDIR_PATH����\n";
    print "���������ꤵ��Ƥ��ޤ���\n";
    print "���ꤷ�Ƥ�����ٻ�ƤߤƤ���������";
    exit 0;
}

# chdir���kb.ph���ɤࡥ���������require�Ѥߤξ����ɤޤʤ���Perl�θ�����͡�
require( $HEADER_FILE ) if ( -s "$HEADER_FILE" );

# ���󥯥롼�ɥե�������ɤ߹���
require( 'cgi.pl' );
require( 'kinologue.pl' );
$KB_RESOURCE_URL = $KB_RESOURCE_URL || $cgi'PATH_INFO;
$REMOTE_INFO = $cgi'REMOTE_HOST || $cgi'REMOTE_ADDR || '(unknown)';
$REMOTE_INFO .= '-' . $cgi'REMOTE_USER if $cgi'REMOTE_USER; # in BasicAuth
$PROGRAM = $cgi'PROGRAM;

$kinologue'SEV_THRESHOLD = $SYS_LOGLEVEL;

$cgi'SMTP_SERVER = $SMTP_SERVER;
$cgi'AF_INET = $AF_INET;
$cgi'SOCK_STREAM = $SOCK_STREAM;
$cgi'CHARSET = $CHARSET;
@cgi'TAG_ALLOWED = ( 'article', 'subject', 'key' );

if (( $cgi'SERVER_PORT != 80 ) && ( $SYS_PORTNO == 1 ))
{
    $SERVER_PORT_STRING = ":$cgi'SERVER_PORT";
}
else
{
    $SERVER_PORT_STRING = '';
}

$SCRIPT_URL = "http://$cgi'SERVER_NAME$SERVER_PORT_STRING$PROGRAM";
$MACPERL = ( $^O eq 'MacOS' );  # isMacPerl?
$PROGNAME = "KINOBOARDS/$KB_VERSION R$KB_RELEASE";
$ENV{'TZ'} = $TIME_ZONE if $TIME_ZONE;

# ���ĥ����Υ١���
$HTML_TAGS_COREATTRS = 'id/class/style/title';
$HTML_TAGS_I18NATTRS = 'lang/dir';
$HTML_TAGS_GENATTRS = "$HTML_TAGS_COREATTRS/$HTML_TAGS_I18NATTRS";

# �Ƽ省��饯����������
$H_TOP = '&lt;&lt;�ǿ�';
$H_BOTTOM = '��Ƭ&gt;&gt;';
$H_UP = '&lt;��';
$H_DOWN = '��&gt;';
$H_THREAD_ALL = '��';
$H_THREAD = '��';
@H_REVERSE = ( '��', '��' );
@H_EXPAND = ( '��', '��' );
$H_SUPERSEDE_ICON = '[��]';
$H_DELETE_ICON = '[��]';
$H_RELINKFROM_MARK = '[��]';
$H_RELINKTO_MARK = '[��]';
$H_REORDERFROM_MARK = '[��]';
$H_REORDERTO_MARK = '[��]';

# ������󥯤�ĥ�뤳�Ȥ���Ĥ���URL scheme
@URL_SCHEME = ( 'http', 'ftp', 'gopher', 'mailto' );

# �Ƽ������������ե���������URL
$ICON_UP = &GetIconURL( 'org_tlist.gif' );		# ���
$ICON_UP_X = &GetIconURL( 'org_tlist_x.gif' );		# ���
$ICON_PREV = &GetIconURL( 'org_prev.gif' );		# ����
$ICON_PREV_X = &GetIconURL( 'org_prev_x.gif' );		# ����
$ICON_NEXT = &GetIconURL( 'org_next.gif' );		# ����
$ICON_NEXT_X = &GetIconURL( 'org_next_x.gif' );		# ����
$ICON_DOWN = &GetIconURL( 'org_thread.gif' );		# ����
$ICON_DOWN_X = &GetIconURL( 'org_thread_x.gif' );	# ����
$ICON_FOLLOW = &GetIconURL( 'org_follow.gif' );		# ��ץ饤
$ICON_FOLLOW_X = &GetIconURL( 'org_follow_x.gif' );	# ��ץ饤
$ICON_QUOTE = &GetIconURL( 'org_quote.gif' );		# ���Ѥ��ƥ�ץ饤
$ICON_QUOTE_X = &GetIconURL( 'org_quote_x.gif' );	# ���Ѥ��ƥ�ץ饤
$ICON_SUPERSEDE = &GetIconURL( 'org_supersede.gif' );	# ����
$ICON_SUPERSEDE_X = &GetIconURL( 'org_supersede_x.gif' );	# ����
$ICON_DELETE = &GetIconURL( 'org_delete.gif' );		# ���
$ICON_DELETE_X = &GetIconURL( 'org_delete_x.gif' );	# ���
$ICON_HELP = &GetIconURL( 'org_help.gif' );		# �إ��
$ICON_NEW = &GetIconURL( 'org_listnew.gif' );		# ����

# �����ʥ�ϥ�ɥ�
$SIG{'QUIT'} = 'IGNORE';
$SIG{'INT'} = $SIG{'HUP'} = $SIG{'TERM'} = $SIG{'TSTP'} = 'DoKill';
sub DoKill
{
    local( $sig ) = @_;
    if ( !$PC )
    {
	&cgi'unlock_file( $LOCK_FILE );
	&cgi'unlock_file( $LOCK_FILE_B ) if $LOCK_FILE_B;
    }
    &KbLog( $kinologue'SEV_WARN, "Caught a SIG$sig - shutting down..." );
    exit( 1 );
}

# ���ԥ�������ʿ������
$HTML_BR = "<br />\n";
$HTML_HR = "<hr />\n";

# �����륫���󥿡��ե饰
$gLinkNum = 0;
$gTabIndex = 0;
$gBoardDbCached = 0;


######################################################################


###
## MAIN - �ᥤ��֥�å�
#
# - SYNOPSIS
#	kb.cgi
#
# - DESCRIPTION
#	��ư���˰��٤������Ȥ���롥
#	�������Ϥʤ������Ķ��ѿ�QUERY_STRING��REQUEST_METHOD��
#	�⤷����ɸ�����Ϸ�ͳ���ͤ��Ϥ��ʤ��ȡ�������ư��ʤ���
#
&KbLog( $kinologue'SEV_INFO, 'Exec started.' );
MAIN:
{
    &cgi'Decode();

    if ( $kinologue'SEV_THRESHOLD == $kinologue'SEV_DEBUG )
    {
	local( $key, $value, $msg );
	while (( $key, $value ) = each %cgi'TAGS )
	{
	    $msg .= '&' if $msg;
	    $msg .= "$key=$value";
	}
	&KbLog( $kinologue'SEV_DEBUG, "Command executed with ... " . $msg );
    }

    # HEAD�ꥯ�����Ȥ��Ф������̽���
    if ( $ENV{ 'REQUEST_METHOD' } eq 'HEAD' )
    {
	local( $modTime ) = 0;
	if ( $cgi'TAGS{'b'} ne '' )
	{
	    $modTime = &getBoardLastmod( $cgi'TAGS{'b'} );
	}
	&cgi'Header( 1, $modTime, 0, (), 0 );
	last;
    }

    local( $c ) = $cgi'TAGS{'c'};
    local( $com ) = $cgi'TAGS{'com'};
    local( $s ) = $cgi'TAGS{'s'};
    $BOARD = $cgi'TAGS{'b'};
    if ( $#ARGV >= 0 )
    {
	# from command line.
	$BOARD = shift;
    }
    elsif ( $c eq '' )
    {
	if ( $BOARD )
	{
	    $c = $SYS_TITLE_FORMAT? 'r' : 'v';
	}
	else
	{
	    $c = 'bl';
	}
    }

    if ( $BOARD )
    {
	$BOARD_ESC = &URIEscape( $BOARD );	# ����Ѥ�escape

	local( $boardConfFileP );
	( $BOARDNAME, $boardConfFileP ) = &GetBoardInfo( $BOARD );
	$LOCK_FILE_B = $LOCK_FILE . ".$BOARD";

	# �Ǽ��ĸ�ͭ���åƥ��󥰤��ɤ߹���
	if ( $boardConfFileP )
	{
	    local( $boardConfFile ) = &GetPath( $BOARD, $CONF_FILE_NAME );
	    require( $boardConfFile ) if ( -s "$boardConfFile" );
	}

	# ��������DB���ɤ߹����R7�ʹߡ�
	&CacheIconDb( $BOARD ) if $SYS_ICON;
    }

    # ���Ƥ�require������ä����ȡ�����

    # ǧ�ھ���ν����
    $cgiauth'GUEST = $GUEST;
    $cgiauth'ADMIN = $ADMIN;
    $USER_AUTH_FILE = &GetPath( $SYS_DIR, $USER_FILE );

    # ���������ƥ����������
    $SYS_EXPAND = $SYS_EXPAND && ( $SYS_THREAD_FORMAT != 2 );
    $POLICY = $GUEST_POLICY;	# Policy by default.

    if ( $SYS_AUTH )
    {
	$SYS_AUTH_DEFAULT = $SYS_AUTH;
	$SYS_AUTH = 3 if ( $cgi'TAGS{ 'kinoA' } == 3 );
	if ( $c eq 'lo' )
	{
	    # ������
	    &UILogin();
	    last;
	}
	elsif ( $c eq 'ue' )
	{
	    # �桼��������Ͽ
	    &UIUserEntry();
	    last;
	}
	elsif ( $c eq 'uex' )
	{
	    # �桼��������Ͽ�»�
	    &UIUserEntryExec();
	    last;
	}

	$cgiauth'AUTH_TYPE = $SYS_AUTH;
	&cgi'Cookie() if ( $SYS_AUTH == 1 );
	    
	local( $err, @userInfo );
	( $err, $UNAME, $PASSWD, @userInfo ) = &cgiauth'CheckUser( $USER_AUTH_FILE );
	    
	if ( $err == 3 )
	{
	    # �桼��̾���ߤĤ���ʤ�
	    &Fatal( 40, $cgi'TAGS{'kinoU'} );# ������41�����ɥ������ƥ�ͥ��
	}
	elsif ( $err == 4 )
	{
	    # �ѥ���ɤ��ְ�äƤ���
	    &Fatal( 40, '' );
	}
	elsif ( $err == 9 )
	{
	    if ( $c eq 'acx' )
	    {
		# �����ԥѥ�����ѹ��μ»�
		&UIAdminConfigExec();
		last;
	    }
	    # �����ԥѥ���ɤ����ξ�硤�桼��������԰������Ƥ��顥����
	    $cgiauth'UID = $UNAME;
	    $cgiauth'PASSWD = $PASSWD;

	    # �����ԥѥ�����ѹ�
	    &UIAdminConfig();
	    last;
	}
	elsif ( $err != 0 )
	{
	    # not reached...
	    &Fatal( 998, "Must not reach here(MAIN: $err)." );
	}
	    
	# ǧ������
	$UNAME_ESC = &URIEscape( $UNAME ) if ( $SYS_AUTH == 3 );
	$UMAIL = $userInfo[2];
	$UURL = $userInfo[3];

	# user policy�η���
	#   1 ... �ɤ�
	#   2 ... ��
	#   4 ... ��Ͽ�ʥ桼������򥵡��Ф˻Ĥ���
	#   8 ... ����
	if ( &IsUser( $ADMIN ))
	{
	    # ������
	    $POLICY = 1 + 2 + 4 + 8;
	}
	elsif ( !&IsUser( $GUEST ))
	{
	    # ��Ͽ�桼��
	    # $POLICY = ( $USER_POLICY & 1 ) + ( $USER_POLICY & 2 ) + 4;
	    $POLICY = $USER_POLICY + 4;
	}
	else
	{
	    # �����ȥ桼��
	    # $POLICY = ( $GUEST_POLICY & 1 ) + ( $USER_POLICY & 2 );
	    $POLICY = $GUEST_POLICY;
	}
    }

    ###
    ## ���ޥ�ɤο���ʬ��
    #

    # ���ȷ�
    if ( $POLICY & 1 )
    {
	if ( $c eq 'e' )
	{
	    # ñ�쵭����ɽ��
	    &UIShowArticle();
	    last;
	}
	elsif ( $c eq 't' )
	{
	    # �ե�������������ɽ����
	    &UIShowThread();
	    last;
	}
	elsif ( $c eq 'v' )
	{
	    # ����å��̥����ȥ����
	    &UIThreadTitle( 0 );
	    last;
	}
	elsif ( $c eq 'vt' )
	{
	    # ����å��̥����ȥ뤪��ӵ�������
	    &UIThreadArticle();
	    last;
	}
	elsif ( $c eq 'r' )
	{
	    # �񤭹��߽�˥�����
	    &UISortTitle();
	    last;
	}
	elsif ( $c eq 'l' )
	{
	    # ������������񤭹��߽��ɽ��
	    &UISortArticle();
	    last;
	}
	elsif ( $SYS_F_S && ( $c eq 's' ))
	{
	    # �����θ���
	    &UISearchArticle();
	    last;
	}
	elsif ( $SYS_ICON && ( $c eq 'i' ))
	{
	    # ��������ɽ������
	    &UIShowIcon();
	    last;
	}
	elsif ( $c eq 'h' )
	{
	    # �إ�ײ���
	    &UIHelp();
	    last;
	}
    }

    # �񤭹��߷�
    local( $varBack ) = 0;
    if ( $POLICY & 2 )
    {
	if (( $c eq 'x' ) && ( $com ne 'x' ))
	{
	    # preview��������ʤΤǡ����ޥ�ɽ񤭴�����
	    $varBack = 1;
	    $cgi'TAGS{'c'} = $cgi'TAGS{'corig'};
	    $c = $cgi'TAGS{'c'};
	}

	if ( $c eq 'n' )
	{
	    # �������
	    &UIPostNewEntry( $varBack );
	    last;
	}
	elsif ( !$s && ( $c eq 'f' ))
	{
	    # ��ץ饤���
	    &UIPostReplyEntry( $varBack, 0 );
	    last;
	}
	elsif ( $c eq 'q' )
	{
	    # ���ѥ�ץ饤���
	    &UIPostReplyEntry( $varBack, 1 );
	    last;
	}
	elsif ( !$s && ( $c eq 'p' ) && ( $com ne 'x' ))
	{
	    # ��ƥץ�ӥ塼
	    &UIPostPreview( 0 );
	    last;
	}
	elsif ( !$s && ( $c eq 'p' ) && ( $com eq 'x' ))
	{
	    # ��Ͽ����̤�ɽ����ľ�ܡ�
	    &UIPostExec( 0 );
	    last;
	}
	elsif ( !$s && ( $c eq 'x' ) && ( $com eq 'x' ))
	{
	    # ��Ͽ����̤�ɽ���ʥץ�ӥ塼��ͳ��
	    &UIPostExec( 1 );
	    last;
	}
    }

    # ��Ͽ��
    if ( $POLICY & 4 )
    {
	# �������פȡֺ���פ��ֽ񤭹��߷ϡפǤʤ�����Ͽ�ϡפʤΤϡ�
	# ��Ͽ���Ƥʤ��ͤ˾ä�����㤫�ʤ�ʤ����餵��:-)

        if ( $c eq 'uc' )
        {
            # �桼����������
	    &UIUserConfig();
            last;
        }
        elsif ( $c eq 'ucx' )
        {
            # �桼����������μ»�
	    &UIUserConfigExec();
	    last;
        }
	elsif ( $s && ( $c eq 'f' ))
	{
	    # ��������
	    &UISupersedeEntry( $varBack );
	    last;
	}
	elsif ( $s && ( $c eq 'p' ) && ( $com ne 'x' ))
	{
	    # ���������ץ�ӥ塼
	    &UISupersedePreview( 0 );
	    last;
	}
	elsif ( $s && ( $c eq 'p' ) && ( $com eq 'x' ))
	{
	    # ���������»ܡ�ľ�ܡ�
	    &UISupersedeExec( 0 );
	    last;
	}
	elsif ( $s && ( $c eq 'x' ) && ( $com eq 'x' ))
	{
	    # ���������»ܡʥץ�ӥ塼��ͳ��
	    &UISupersedeExec( 1 );
	    last;
	}
        elsif ( $c eq 'dp' )
        {
	    # ����ץ�ӥ塼
	    &UIDeletePreview();
	    last;
        }
        elsif ( $c eq 'de' )
        {
	    # ����»�
            &UIDeleteExec( 0 );
	    last;
	}
        elsif ($c eq 'det' )
        {
	    # ����»ܡʥ�ץ饤���
            &UIDeleteExec( 1 );
	    last;
        }
    }

    # ������
    if ( $POLICY & 8 )
    {
	if ( $c eq 'ct' )
	{
	    &UIThreadTitle( 2 );
	    last;
	}
	elsif ( $c eq 'ce' )
	{
	    &UIThreadTitle( 3 );
	    last;
	}
	elsif ( $c eq 'mvt' )
	{
	    &UIThreadTitle( 4 );
	    last;
	}
	elsif ( $c eq 'mve' )
	{
	    &UIThreadTitle( 5 );
	    last;
	}
        elsif ( $c eq 'bc' )
        {
            # �Ǽ�������
	    &UIBoardConfig();
            last;
        }
        elsif ( $c eq 'bcx' )
        {
	    # �Ǽ�������μ»�
	    &UIBoardConfigExec();
	    last;
        }
        elsif ( $c eq 'be' )
        {
            # �Ǽ��Ŀ���
            &UIBoardEntry();
            last;
        }
        elsif ( $c eq 'bex' )
        {
	    # �Ǽ��Ŀ��ߤμ»�
	    &UIBoardEntryExec();
	    last;
        }
    }

    if ( $c eq 'bl' )
    {
	# �Ǽ��İ�����ɽ��
	&UIBoardList();
	last;
    }

    # from command line?
    if ( $#ARGV >= 0 )
    {
	$c = shift;		# Command.
	local( $body, $code );
	while ( <> )
	{
	    $body .= $_;
	    last if ( $SYS_MAXARTSIZE &&
	        ( length( $body ) > $SYS_MAXARTSIZE ));
	}
	$code = &jcode'getcode( *body );
	&jcode'convert( *body, 'euc', $code, 'z' ) if ( defined( $code ));
	$body =~ s/\x0d\x0a/\x0a/go;
	$body =~ s/\x0d/\x0a/go;

	if ( $SYS_F_POST_STDIN )
	{
	    if ( $c eq 'POST' )
	    {
		*gVarBody = *body;
		$gVarForce = 1;
		do( &GetPath( $UI_DIR, 'Post.pl' ));
		last;
	    }
	    elsif ( $c eq 'POST_IF' )
	    {
		*gVarBody = *body;
		$gVarForce = 0;
		do( &GetPath( $UI_DIR, 'Post.pl' ));
		last;
	    }
	}
    }

    # �ɤΥ��ޥ�ɤǤ�ʤ������顼��
    &Fatal( 99, $c );
}
&KbLog( $kinologue'SEV_INFO, 'Exec finished.' );
exit( 0 );


######################################################################
# �桼�����󥿥ե���������ץ���ơ������


###
## �����󥪥����
#
sub UILogin
{
    # Isolation level: CHAOS.

    # �桼������򥯥ꥢ
    if ( $SYS_AUTH == 1 )
    {
	$UNAME = $cgiauth'F_COOKIE_RESET;
    }
    else
    {
	$UNAME = '';
    }
    &htmlGen( 'Login.xml' );
}

sub hg_login_form
{
    &Fatal( 18, "$_[0]/LoginForm" ) if ( $_[0] ne 'Login.xml' );

    local( %tags, $msg );
    $msg = &TagLabel( $H_FROM, 'kinoU', 'N' ) . ': ' . &TagInputText( 'text', 'kinoU', '', $NAME_LENGTH ) . $HTML_BR;
    $msg .= &TagLabel( $H_PASSWD, 'kinoP', 'P' ) . ': ' . &TagInputText( 'password', 'kinoP', '', $PASSWD_LENGTH ) . $HTML_BR;
    if ( $SYS_AUTH_DEFAULT == 1 )
    {
	local( $contents );
	$contents = &TagInputRadio( 'kinoA_url', 'kinoA', '3', 0 ) . ":\n" .
	    &TagLabel( '���å���(HTTP-Cookies)��Ȥ鷺��ǧ�ڤ���', 'kinoA_url', 'U' ) . $HTML_BR;
	$contents .= &TagInputRadio( 'kinoA_cookies', 'kinoA', '1', 1 ) .
	    "\n" . &TagLabel( '���å�����ȤäƤ��Υ֥饦���˾����Ф�������', 'kinoA_cookies', 'C' ) . $HTML_BR;
	$msg .= &TagFieldset( "���å���:$HTML_BR", $contents );
    }

    %tags = ( 'c', 'bl', 'kinoT', 'plain' );
    &DumpForm( *tags, '�¹�', '�ꥻ�å�', *msg, 1 );
}


###
## �����ԥѥ���ɤ��������
#
sub UIAdminConfig
{
    # Isolation level: CHAOS.
    &htmlGen( 'AdminConfig.xml' );
}

sub hg_admin_config_form
{
    &Fatal( 18, "$_[0]/AdminConfigForm" ) if ( $_[0] ne 'AdminConfig.xml' );

    local( %tags, $msg );
    $msg = &TagLabel( $H_PASSWD, 'confP', 'P' ) . ': ' .
	&TagInputText( 'password', 'confP', '', $PASSWD_LENGTH ) . $HTML_BR;
    $msg .= &TagLabel( $H_PASSWD, 'confP2', 'C' ) . ': ' .
	&TagInputText( 'password', 'confP2', '', $PASSWD_LENGTH ) .
	'��ǰ�Τ��ᡤ�⤦���٤��ꤤ���ޤ���' . $HTML_BR;
    %tags = ( 'c', 'acx' );
    &DumpForm( *tags, '����', '�ꥻ�å�', *msg, 1 );
}


###
## �����ԥѥ��������μ»�
#
sub UIAdminConfigExec
{
    # Isolation level: SERIALIZABLE.
    &LockAll();

    local( $p1 ) = $cgi'TAGS{'confP'};
    local( $p2 ) = $cgi'TAGS{'confP2'};

    # admin�Τ�
    &Fatal( 44, '' ) unless ( $POLICY & 8 );

    if ( !$p2 || ( $p1 ne $p2 ))
    {
	&Fatal( 42, $H_PASSWD );
    }
    
    if ( !&cgiauth'SetUserPasswd( $USER_AUTH_FILE , $ADMIN, $p1 ))
    {
	&Fatal( 41, $ADMIN );
    }

    &UnlockAll();

    # �桼������򥯥ꥢ
    &UILogin();
}


###
## �桼����Ͽ����
#
sub UIUserEntry
{
    # Isolation level: CHAOS.

    # �桼������򥯥ꥢ
    $UNAME = $cgiauth'F_COOKIE_RESET if ( $SYS_AUTH == 1 );
    &htmlGen( 'UserEntry.xml' );
}

sub hg_user_entry_form
{
    &Fatal( 18, "$_[0]/UserEntryForm" ) if ( $_[0] ne 'UserEntry.xml' );

    local( %tags, $msg );
    $msg = &TagLabel( $H_FROM, 'kinoU', 'N' ) . ': ' . &TagInputText( 'text',
	'kinoU', '', $NAME_LENGTH ) . $HTML_BR;
    $msg .= &TagLabel( $H_MAIL, 'mail', 'M' ) . ': ' . &TagInputText( 'text',
	'mail', '', $MAIL_LENGTH ) . $HTML_BR;
    $msg .= &TagLabel( $H_PASSWD, 'kinoP', 'P' ) . ': ' . &TagInputText(
	'password', 'kinoP', '', $PASSWD_LENGTH ) . $HTML_BR;
    $msg .= &TagLabel( $H_PASSWD, 'kinoP2', 'C' ) . ': ' . &TagInputText(
	'password', 'kinoP2', '', $PASSWD_LENGTH ) .
	'��ǰ�Τ��ᡤ�⤦���٤��ꤤ���ޤ���' . $HTML_BR;
    $msg .= &TagLabel( $H_URL, 'url', 'U' ) . ': ' . &TagInputText( 'text',
	'url', 'http://', $URL_LENGTH ) . '�ʾ�ά���Ƥ⤫�ޤ��ޤ����' .
	$HTML_BR;

    %tags = ( 'c', 'uex' );
    &DumpForm( *tags, '��Ͽ', '�ꥻ�å�', *msg, 1 );
}


###
## �桼����Ͽ�μ»�
#
sub UIUserEntryExec
{
    # Isolation level: SERIALIZABLE.
    &LockAll();

    local( $user ) = $cgi'TAGS{'kinoU'};
    local( $p1 ) = $cgi'TAGS{'kinoP'};
    local( $p2 ) = $cgi'TAGS{'kinoP2'};
    local( $mail ) = $cgi'TAGS{'mail'};
    local( $url ) = $cgi'TAGS{'url'};

    &CheckName( *user );
    &CheckEmail( *mail );
    &CheckURL( *url );
    &CheckPasswd( *p1 );

    if ( !$p2 || ( $p1 ne $p2 ))
    {
	&Fatal( 42, $H_PASSWD );
    }
	    
    # ��Ͽ�Ѥߥ桼���θ���
    if ( $SYS_POSTERMAIL && &cgiauth'SearchUserInfo( $USER_AUTH_FILE, $mail, undef ))
    {
	&Fatal( 6, $mail );
    }

    # ������Ͽ����
    local( $res ) = &cgiauth'AddUser( $USER_AUTH_FILE, $user, $p1, $mail, $url );

    if ( $res == 1 )
    {
	&Fatal( 5, $user );
    }
    elsif ( $res == 2 )
    {
	&Fatal( 998, 'Must not reach here(UserEntryExec).' );
    }

    &UnlockAll();

    # ��������̤�
    &UILogin();
}


###
## �桼�������ѹ�
#
sub UIUserConfig
{
    # Isolation level: CHAOS.

    &htmlGen( 'UserConfig.xml' );
}

sub hg_user_config_form
{
    &Fatal( 18, "$_[0]/UserConfigForm" ) if ( $_[0] ne 'UserConfig.xml' );

    if ( $POLICY & 8 )
    {
	local( %tags, $msg );
	$msg .= &TagLabel( "�ѹ�����$H_USER��$H_FROM", 'confUser', 'N' ) .
	    ': ' . &TagInputText( 'text', 'confUser', '', $NAME_LENGTH ) .
	    "�ʴ����Ԥ���$H_USER��������ѹ��Ǥ��ޤ���" . $HTML_BR . $HTML_BR;
	$msg .= &TagLabel( $H_MAIL, 'confMail', 'M' ) . ': ' .
	    &TagInputText( 'text', 'confMail', '', $MAIL_LENGTH ) . $HTML_BR;
	$msg .= &TagLabel( $H_URL, 'confUrl', 'U' ) . ': ' .
	    &TagInputText( 'text', 'confUrl', 'http://', $URL_LENGTH ) . $HTML_BR . $HTML_BR;
	$msg .= &TagLabel( $H_PASSWD, 'confP', 'P' ) . ': ' .
	    &TagInputText( 'password', 'confP', '', $PASSWD_LENGTH ) . $HTML_BR;
	$msg .= &TagLabel( $H_PASSWD, 'confP2', 'C' ) . ': ' .
	    &TagInputText( 'password', 'confP2', '', $PASSWD_LENGTH ) .
	    '��ǰ�Τ��ᡤ�⤦���٤��ꤤ���ޤ���' . $HTML_BR;
	%tags = ( 'c', 'ucx' );
	&DumpForm( *tags, '����', '�ꥻ�å�', *msg );
    }
    else
    {
	$UURL = $UURL || 'http://';

	local( %tags, $msg );
	$msg .= $H_FROM . ': ' . $UNAME . $HTML_BR . $HTML_BR;
	$msg .= &TagLabel( $H_MAIL, 'confMail', 'M' ) . ': ' .
	    &TagInputText( 'text', 'confMail', $UMAIL, $MAIL_LENGTH ) . $HTML_BR;
	$msg .= &TagLabel( $H_URL, 'confUrl', 'U' ) . ': ' .
	    &TagInputText( 'text', 'confUrl', $UURL, $URL_LENGTH ) . $HTML_BR . $HTML_BR;
	$msg .= &TagLabel( $H_PASSWD, 'confP', 'P' ) . ': ' .
	    &TagInputText( 'password', 'confP', '' , $PASSWD_LENGTH ) . $HTML_BR;
	$msg .= &TagLabel( $H_PASSWD, 'confP2', 'C' ) . ': ' .
	    &TagInputText( 'password', 'confP2', '', $PASSWD_LENGTH ) .
	    '��ǰ�Τ��ᡤ�⤦���٤��ꤤ���ޤ���' . $HTML_BR;
	%tags = ( 'c', 'ucx' );
	&DumpForm( *tags, '����', '�ꥻ�å�', *msg );
    }
}


###
## �桼������μ»�
#
sub UIUserConfigExec
{
    # Isolation level: SERIALIZABLE.
    &LockAll();

    local( $p1 ) = $cgi'TAGS{'confP'};
    local( $p2 ) = $cgi'TAGS{'confP2'};
    local( $user ) = $cgi'TAGS{'confUser'};
    local( $mail ) = $cgi'TAGS{'confMail'};
    local( $url ) = $cgi'TAGS{'confUrl'};

    $user = $UNAME unless ( $POLICY & 8 );

    &CheckName( *user );
    &CheckEmail( *mail );
    &CheckURL( *url );
		
    # ��ɬ�פʤ�˥ѥ�����ѹ�
    if ( $p1 || $p2 )
    {
	&CheckPasswd( *p1 );

	if ( !$p2 || ( $p1 ne $p2 ))
	{
	    &Fatal( 42, $H_PASSWD );
	}

	if ( !&cgiauth'SetUserPasswd( $USER_AUTH_FILE, $user, $p1 ))
	{
	    &Fatal( 41, $user );
	}
    }

    # �桼�����󹹿�
    if ( !&cgiauth'SetUserInfo( $USER_AUTH_FILE, $user, ( $mail, $url )))
    {
	&Fatal( 41, '' );
    }

    &UnlockAll();

    &UIBoardList();
}


###
## �Ǽ�����Ͽ����
#
sub UIBoardEntry
{
    # Isolation level: CHAOS.

    &htmlGen( 'BoardEntry.xml' );
}

sub hg_board_entry_form
{
    &Fatal( 18, "$_[0]/BoardEntryForm" ) if ( $_[0] ne 'BoardEntry.xml' );

    local( %tags, $msg );
    $msg = &TagLabel( "$H_BOARDά��", 'name', 'B' ) . ': ' . &TagInputText(
	'text', 'name', '', $BOARDNAME_LENGTH ) . $HTML_BR;
    $msg .= &TagLabel( "$H_BOARD̾��", 'intro', 'N' ) . ': ' . &TagInputText(
	'text', 'intro', '', $BOARDNAME_LENGTH ) . $HTML_BR . $HTML_BR;
    $msg .= &TagLabel( "$H_BOARD�μ�ư$H_MAIL�ۿ���", 'armail', 'M' ) .
	$HTML_BR . &TagTextarea( 'armail', '', $TEXT_ROWS, $MAIL_LENGTH ) .
	$HTML_BR . $HTML_BR;
    $msg .= &TagLabel( "$H_BOARD�إå���ʬ", 'article', 'H' ) . $HTML_BR .
	&TagTextarea( 'article', '', $TEXT_ROWS, $TEXT_COLS ) . $HTML_BR;
    %tags = ( 'c', 'bex' );
    &DumpForm( *tags, '��Ͽ', '�ꥻ�å�', *msg );
}


###
## �Ǽ�����Ͽ�μ»�
#
sub UIBoardEntryExec
{
    # Isolation level: SERIALIZABLE.
    &LockAll();

    local( $name ) = $cgi'TAGS{'name'};
    local( $intro ) = $cgi'TAGS{'intro'};
    local( $armail ) = $cgi'TAGS{'armail'};
    local( $header ) = $cgi'TAGS{'article'};

    &CheckBoardDir( *name );
    &CheckBoardName( *intro );
    &CheckBoardHeader( *header );
    &secureSubject( *intro );
    &secureArticle( *header, $H_TTLABEL[2] );
    local( @arriveMail ) = split( /\n/, $armail );

    &AddBoardDb( $name, $intro, 0, *arriveMail, *header );

    &UnlockAll();

    &UIBoardList();
}


###
## �Ǽ��������ѹ�����
#
sub UIBoardConfig
{
    # Isolation level: SERIALIZABLE.
    &LockAll();

    # ���Ǽ��Ĥξ������Ф�
    @gArriveMail = ();
    &GetArriveMailTo(1, $BOARD, *gArriveMail); # ����ȥ����Ȥ���Ф�
    $gHeader = "";
    &GetHeaderDb( $BOARD, *gHeader ); # �إå�ʸ�������Ф�

    &htmlGen( 'BoardConfig.xml' );

    &UnlockAll();
}

sub hg_board_config_form
{
    &Fatal( 18, "$_[0]/BoardConfigForm" ) if ( $_[0] ne 'BoardConfig.xml' );

    local( %tags, $msg );
    $msg = &TagLabel( "��$BOARD��$H_BOARD������", 'valid', 'V' ) . ': ' .
	&TagInputCheck( 'valid', 1 ) . $HTML_BR . $HTML_BR;
    $msg .= &TagLabel( "��$BOARD��̾��", 'intro', 'N' ) . ': ' .
	&TagInputText( 'text', 'intro', $BOARDNAME, $BOARDNAME_LENGTH ) .
	$HTML_BR . $HTML_BR;
    local( $all );
    foreach ( @gArriveMail ) { $all .= $_ . "\n"; }
    $msg .= &TagLabel( "��$BOARD�פμ�ư$H_MAIL�ۿ���", 'armail', 'M' ) .
	$HTML_BR . &TagTextarea( 'armail', $all, $TEXT_ROWS, $MAIL_LENGTH ) .
	$HTML_BR . $HTML_BR;
    $msg .= &TagLabel( "��$BOARD�פ�$H_BOARD�إå���ʬ", 'article', 'H' ) .
	$HTML_BR . &TagTextarea( 'article', $gHeader, $TEXT_ROWS,
	$TEXT_COLS ) . $HTML_BR;
    %tags = ( 'c', 'bcx', 'b', $BOARD );
    &DumpForm( *tags, '�ѹ�', '�ꥻ�å�', *msg );
}


###
## �Ǽ�������μ»�
#
sub UIBoardConfigExec
{
    # Isolation level: SERIALIZABLE.
    &LockAll();

    local( $valid ) = $cgi'TAGS{'valid'};
    local( $intro ) = $cgi'TAGS{'intro'};
    local( $armail ) = $cgi'TAGS{'armail'};
    local( $header ) = $cgi'TAGS{'article'};

    &CheckBoardName( *intro );
    &CheckBoardHeader( *header );
    &secureSubject( *intro );
    &secureArticle( *header, $H_TTLABEL[2] );
    local( @arriveMail ) = split( /\n/, $armail );

    &UpdateBoardDb( $BOARD, $valid, $intro, 0, *arriveMail, *header );

    &UnlockAll();

    &UIBoardList();
}


###
## �Ǽ��İ���
#
sub UIBoardList
{
    # Isolation level: CHAOS.

    &htmlGen( 'BoardList.xml' );
}


###
## ��å�����������Ͽ�Υ���ȥ�
## ��ץ饤��å�������Ͽ�Υ���ȥ�
## ��å����������Υ���ȥ�
#
sub UIPostNewEntry
{
    # Isolation level: CHAOS.

    if ( $SYS_NEWART_ADMINONLY && !( $POLICY & 8 ))
    {
	&Fatal( 99, $cgi'TAGS{'c'} );
    }

    local( $back ) = @_;

    $gId = '';			# 0�Ǥϥ��ᡥ���������ե�����̾�⤢�뤫�⡥
    $gDefPostDateStr = $cgi'TAGS{'postdate'};
    $gDefSubject = $cgi'TAGS{'subject'};
    $gDefName = $cgi'TAGS{'name'};
    $gDefEmail = $cgi'TAGS{'mail'};
    $gDefUrl = $cgi'TAGS{'url'};
    $gDefTextType = $cgi'TAGS{'texttype'};
    $gDefIcon = $cgi'TAGS{'icon'};
    $gDefArticle = $cgi'TAGS{'article'};
    $gDefFmail = $cgi'TAGS{'fmail'};

    if ( $back )
    {
	require( 'mimer.pl' );
	$gDefSubject = &MIME'base64decode( $gDefSubject );
	$gDefArticle = &MIME'base64decode( $gDefArticle );
    }
    else
    {
    }

    $gEntryType = 'normal';		# ����
    &htmlGen( 'PostNewEntry.xml' );
}

sub UIPostReplyEntry
{
    # Isolation level: SERIALIZABLE.
    &LockBoard();
    &DbCache( $BOARD ) if $BOARD;

    local( $back, $quoteFlag ) = @_;

    $gId = $cgi'TAGS{'id'};
    $gDefPostDateStr = $cgi'TAGS{'postdate'};
    $gDefSubject = $cgi'TAGS{'subject'};
    $gDefName = $cgi'TAGS{'name'};
    $gDefEmail = $cgi'TAGS{'mail'};
    $gDefUrl = $cgi'TAGS{'url'};
    $gDefTextType = $cgi'TAGS{'texttype'};
    $gDefIcon = $cgi'TAGS{'icon'};
    $gDefArticle = $cgi'TAGS{'article'};
    $gDefFmail = $cgi'TAGS{'fmail'};

    if ( $back )
    {
	require( 'mimer.pl' );
	$gDefSubject = &MIME'base64decode( $gDefSubject );
	$gDefArticle = &MIME'base64decode( $gDefArticle );
    }
    elsif ( $quoteFlag == 0 )
    {
	if ( $gDefSubject eq '' )
	{
	    local( $tmp );
	    $gDefSubject = &getMsgSubject( $gId );
	    &GetReplySubject( *gDefSubject );
	}
    }
    else
    {
	if ( $gDefSubject eq '' )
	{
	    local( $tmp );
	    $gDefSubject = &getMsgSubject( $gId );
	    &GetReplySubject( *gDefSubject );
	}
	&QuoteOriginalArticle( $gId, *gDefArticle );
    }

    $gEntryType = 'reply';		# ��ץ饤
    &htmlGen( 'PostReplyEntry.xml' );

    &UnlockBoard();
}

sub UISupersedeEntry
{
    # Isolation level: SERIALIZABLE.
    &LockBoard();
    &DbCache( $BOARD ) if $BOARD;

    local( $back ) = @_;

    if ( !( $POLICY & 8 ) && ( $SYS_OVERWRITE == 0 ))
    {
	&Fatal( 99, $cgi'TAGS{'c'} );
    }

    $gId = $cgi'TAGS{'id'};
    $gDefPostDateStr = $cgi'TAGS{'postdate'};
    $gDefSubject = $cgi'TAGS{'subject'};
    $gDefName = $cgi'TAGS{'name'};
    $gDefEmail = $cgi'TAGS{'mail'};
    $gDefUrl = $cgi'TAGS{'url'};
    $gDefTextType = $cgi'TAGS{'texttype'};	# ��������XHTML���ϤΤۤ����������� 
    $gDefIcon = $cgi'TAGS{'icon'};
    $gDefArticle = $cgi'TAGS{'article'};
    $gDefFmail = $cgi'TAGS{'fmail'};

    if ( $back )
    {
	require( 'mimer.pl' );
	$gDefSubject = &MIME'base64decode( $gDefSubject );
	$gDefArticle = &MIME'base64decode( $gDefArticle );
    }
    else
    {
	local( $tmp, $postDate );
	( $tmp, $tmp, $postDate, $gDefSubject, $gDefIcon, $tmp, $gDefName, $gDefEmail, $gDefUrl ) = &getMsgInfo( $gId );
	$gDefPostDateStr = &GetYYYY_MM_DD_HH_MM_SSFromUtc( $postDate );
	&QuoteOriginalArticleWithoutQMark( $gId, *gDefArticle );
    }

    $gEntryType = 'supersede';		# ����
    &htmlGen( 'SupersedeEntry.xml' );

    &UnlockBoard();
}

sub hg_post_reply_entry_orig_article
{
    &Fatal( 18, "$_[0]/PostReplyEntryOrigArticle" ) if ( $_[0] ne 'PostReplyEntry.xml' );
    &DumpArtBody( $gId, 0, 1 );
}

sub hg_supersede_entry_orig_article
{
    &Fatal( 18, "$_[0]/SupersedeEntryOrigArticle" ) if ( $_[0] ne 'SupersedeEntry.xml' );
    &DumpArtBody( $gId, 0, 1 );
}


###
## ��å�������Ͽ�Υץ�ӥ塼
## ��å����������Υץ�ӥ塼
#
sub UIPostPreview
{
    # Isolation level: SERIALIZABLE.
    &LockAll();
    &DbCache( $BOARD ) if $BOARD;

    &UIPostPreviewMain( 'post' );
    &htmlGen( 'PostPreview.xml' );

    &UnlockAll();
}

sub UISupersedePreview
{
    # Isolation level: READ UNCOMITTED.
    &LockAll();
    &DbCache( $BOARD ) if $BOARD;
    &UnlockAll();

    if ( !( $POLICY & 8 ) && ( $SYS_OVERWRITE == 0 ))
    {
	&Fatal( 99, $cgi'TAGS{'c'} );
    }

    &UIPostPreviewMain( 'supersede' );
    &htmlGen( 'SupersedePreview.xml' );
}

sub UIPostPreviewMain
{
    local( $type ) = @_;

    # ���Ϥ��줿��������
    $gOrigId = $cgi'TAGS{'id'};
    $gPostDateStr = $cgi'TAGS{'postdate'};
    $gSubject = $cgi'TAGS{'subject'};
    $gIcon = $cgi'TAGS{'icon'};
    $gArticle = $cgi'TAGS{'article'};
    $gTextType = $cgi'TAGS{'texttype'};

    # �Ƽ����μ���
    if ( $POLICY & 8 )
    {
	if ( $cgi'TAGS{'name'} eq '' )
	{
	    $gName = $MAINT_NAME;
	    $gEmail = $MAINT;
	    $gUrl = $MAINT_URL;
	}
	else
	{
	    $gName = $cgi'TAGS{'name'};
	    $gEmail = $cgi'TAGS{'mail'};
	    $gUrl = $cgi'TAGS{'url'};
	}
    }
    elsif ( $POLICY & 4 )
    {
	$gName = $UNAME;
	$gEmail = $UMAIL;
	$gUrl = $UURL;
    }
    else
    {
	$gName = $cgi'TAGS{'name'};
	$gEmail = $cgi'TAGS{'mail'};
	$gUrl = $cgi'TAGS{'url'};
    }

    $gEncSubject = &MIME'base64encode( $gSubject );
    $gEncArticle = &MIME'base64encode( $gArticle );

    &secureSubject( *gSubject );
    &secureArticle( *gArticle, $gTextType );

    local( $postDate ) = $^T;
    $postDate = &GetUtcFromYYYY_MM_DD_HH_MM_SS( $gPostDateStr ) if ( $gPostDateStr ne '' );

    # ���Ϥ��줿��������Υ����å�
    &CheckArticle( $BOARD, *postDate, *gName, *gEmail, *gUrl, *gSubject, *gIcon, *gArticle );
}

sub hg_post_preview_form
{
    &Fatal( 18, "$_[0]/PostPreviewForm" ) if ( $_[0] ne 'PostPreview.xml' );

    require( 'mimer.pl' );

    local( $supersede ) = $_[1];

    local( %tags, $msg, $contents );
    $contents = &TagInputRadio( 'com_e', 'com', 'e', 0 ) . ":\n" . &TagLabel( '��äƤ��ʤ���', 'com_e', 'P' ) . $HTML_BR;
    $contents .= &TagInputRadio( 'com_x', 'com', 'x', 1 ) . "\n" . &TagLabel( '��Ͽ����', 'com_x', 'X' ) . $HTML_BR;
    $msg = &TagFieldset( "���ޥ��:$HTML_BR", $contents );
    %tags = ( 'corig', $cgi'TAGS{'corig'}, 'c', 'x', 'b', $BOARD,
	     'id', $gOrigId, 'postdate', $gPostDateStr, 'texttype', $gTextType,
	     'name', $gName, 'mail', $gEmail, 'url', $gUrl, 'icon', $gIcon,
	     'subject', $gEncSubject, 'article', $gEncArticle,
	     'fmail', $cgi'TAGS{'fmail'}, 's', $supersede,
	     'op', $cgi'TAGS{'op'} );

    &DumpForm( *tags, '�¹�', '', *msg );
}

sub hg_supersede_preview_form
{
    &Fatal( 18, "$_[0]/SupersedePreviewForm" ) if ( $_[0] ne 'SupersedePreview.xml' );
    &hg_post_preview_form( 'PostPreview.xml', 1 );
}

sub hg_post_preview_body
{
    &Fatal( 18, "$_[0]/PostPreviewBody" ) if ( $_[0] ne 'PostPreview.xml' );

    local( $postDate ) = $^T;
    $postDate = &GetUtcFromYYYY_MM_DD_HH_MM_SS( $gPostDateStr ) if ( $gPostDateStr ne '' );
    &DumpArtBody( '', 0, 1, $gOrigId, '', $postDate, $gSubject, $gIcon, 0, $gName, $gEmail, $gUrl, $gArticle );
}

sub hg_supersede_preview_body
{
    &Fatal( 18, "$_[0]/SupersedePreviewBody" ) if ( $_[0] ne 'SupersedePreview.xml' );

    local( $postDate ) = $^T;
    $postDate = &GetUtcFromYYYY_MM_DD_HH_MM_SS( $gPostDateStr ) if ( $gPostDateStr ne '' );

    # hg_post_preview_body�Ȥϰۤʤꡤfid�����ʥ�ץ饤���ǤϤʤ��ˡ�
    &DumpArtBody( '', 0, 1, '', '', $postDate, $gSubject, $gIcon, 0, $gName, $gEmail, $gUrl, $gArticle );
}

sub hg_supersede_preview_orig_article
{
    &Fatal( 18, "$_[0]/SupersedePreviewOrigArticle" ) if ( $_[0] ne 'SupersedePreview.xml' );
    &DumpArtBody( $gOrigId, 0, 1 );
}


###
## ��������Ͽ
## ����������
#
sub UIPostExec
{
    # Isolation level: SERIALIZABLE.
    &LockAll();
    &DbCache( $BOARD ) if $BOARD;

    local( $previewFlag ) = @_;

    &UIPostExecMain( $previewFlag, 'post' );
    &htmlGen( 'PostExec.xml' );

    &UnlockAll();
}

sub UISupersedeExec
{
    # Isolation level: SERIALIZABLE.
    &LockAll();
    &DbCache( $BOARD ) if $BOARD;

    if ( !( $POLICY & 8 ) && ( $SYS_OVERWRITE == 0 ))
    {
	&Fatal( 99, $cgi'TAGS{'c'} );
    }

    local( $previewFlag ) = @_;
    &UIPostExecMain( $previewFlag, 'supersede' );
    &htmlGen( 'SupersedeExec.xml' );

    &UnlockAll();
}

sub UIPostExecMain
{
    require( 'mimer.pl' );

    local( $previewFlag, $type ) = @_;

    # ���Ϥ��줿��������
    $gOrigId = $cgi'TAGS{'id'};
    local( $postDateStr ) = $cgi'TAGS{'postdate'};
    local( $TextType ) = $cgi'TAGS{'texttype'};
    local( $Icon ) = $cgi'TAGS{'icon'};
    local( $Subject ) = $cgi'TAGS{'subject'};
    local( $Article ) = $cgi'TAGS{'article'};
    local( $Fmail ) = $cgi'TAGS{'fmail'};
    local( $op ) = $cgi'TAGS{'op'};

    # ����Ⱦ���δ֤��������줿�ե����फ�餷����Ƥ���Ĥ��ʤ���
    local( $base ) = ( -M &GetPath( $SYS_DIR, $BOARD_FILE ));
    if ( $SYS_DENY_FORM_OLD && (( $op == 0 ) || ( $base - $op > .5 )))
    {
	&Fatal( 15, '' );
    }

    # �ե���������Ѥζػ�
    if ( $SYS_DENY_FORM_RECYCLE )
    {
	local( $dId, $dKey );
	&GetArticleId( $BOARD, *dId, *dKey );
	&Fatal( 16, '' ) if ( $dKey && ( $dKey == $op ));
    }

    # �Ƽ����μ���
    local( $Name, $Email, $Url, $postDate );
    $postDate = $^T;
    if ( $POLICY & 8 )
    {
	if ( $cgi'TAGS{'name'} eq '' )
	{
	    $Name = $MAINT_NAME;
	    $Email = $MAINT;
	    $Url = $MAINT_URL;
	}
	else
	{
	    $Name = $cgi'TAGS{'name'};
	    $Email = $cgi'TAGS{'mail'};
	    $Url = $cgi'TAGS{'url'};
	}
	if ( $postDateStr ne '' )
	{
	    $postDate = &GetUtcFromYYYY_MM_DD_HH_MM_SS( $postDateStr );
	}
    }
    elsif ( $POLICY & 4 )
    {
	$Name = $UNAME;
	$Email = $UMAIL;
	$Url = $UURL;
    }
    else
    {
	$Name = $cgi'TAGS{'name'};
	$Email = $cgi'TAGS{'mail'};
	$Url = $cgi'TAGS{'url'};
    }

    $Subject = &MIME'base64decode( $Subject ) if $previewFlag;
    $Article = &MIME'base64decode( $Article ) if $previewFlag;
    &secureSubject( *Subject );
    &secureArticle( *Article, $TextType );

    if ( $type eq 'post' )
    {
	# �����κ���
	$gNewArtId = &MakeNewArticleEx( $BOARD, $gOrigId, $op, $postDate, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail, 1 );
    }
    elsif ( $type eq 'supersede' )
    {
	# ����������
	local( $name ) = &getMsgAuthor( $gOrigId );
	&Fatal( 44, '' ) if ( !&IsUser( $name ) && !( $POLICY & 8 ));
	&Fatal( 19, '' ) if (( &getMsgDaughters( $gOrigId ) ne '' ) && !( $POLICY & 8 ) && ( $SYS_OVERWRITE == 1 ));

	$gNewArtId = &SupersedeArticle( $BOARD, $gOrigId, $postDate, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail );
    }
    else
    {
	&Fatal( 998, 'Must not reache here(UIPostExecMain).' );
    }
}

sub hg_post_exec_jump_to_new_article
{
    &Fatal( 18, "$_[0]/PostExecJumpToNewArticle" ) if ( $_[0] ne 'PostExec.xml' );
    &DumpButtonToArticle( $BOARD, $gNewArtId, "�񤭹����$H_MESG��" );
}

sub hg_supersede_exec_jump_to_new_article
{
    &Fatal( 18, "$_[0]/SupersedeExecJumpToNewArticle" ) if ( $_[0] ne 'SupersedeExec.xml' );
    &DumpButtonToArticle( $BOARD, $gNewArtId, "��������$H_MESG��" );
}

sub hg_post_exec_jump_to_orig_article
{
    &Fatal( 18, "$_[0]/PostExecJumpToOrigArticle" ) if ( $_[0] ne 'PostExec.xml' );
    &DumpButtonToArticle( $BOARD, $gOrigId, "$H_ORIG��$H_MESG��" ) if ( $gOrigId ne '' );
}


###
## ����å��̥����ȥ뤪��ӵ�������
#
sub UIThreadArticle
{
    # Isolation level: READ UNCOMITTED.
    &LockBoard();
    &DbCache( $BOARD ) if $BOARD;
    &UnlockBoard();

    %gADDFLAG = ();
    @gIDLIST = ();

    local( $nofMsg ) = &getNofMsg();

    # ɽ������Ŀ������
    $gNum = $cgi'TAGS{'num'};
    if ( defined( $cgi'TAGS{'id'} ))
    {
	$gOld = $nofMsg - int( $cgi'TAGS{'id'} + $gNum/2 );
	$gOld = 0 if ( $gOld < 0 );
    }
    else
    {
	$gOld = $cgi'TAGS{'old'};
    }
    $gRev = $cgi'TAGS{'rev'};
    $gFold = (( $SYS_THREAD_FORMAT == 2 ) || $cgi'TAGS{'fold'} )? 1 : 0;
    $gVRev = $gRev? 1-$SYS_BOTTOMTITLE : $SYS_BOTTOMTITLE;
    $gTo = $nofMsg - $gOld;
    $gFrom = $gTo - $gNum + 1;
    $gFrom = 0 if (( $gFrom < 0 ) || ( $gNum == 0 ));

    $gPageLinkStr = &PageLink( 'vt', $gNum, $gOld, $gRev, $gFold );

    # �����Ѥߥե饰
    # 0 ... �����оݳ�
    # 1 ... �����Ѥ�
    # 2 ... ̤����
    local( $IdNum, $Id );
    for ( $IdNum = $gFrom; $IdNum <= $gTo; $IdNum++ )
    {
	$gADDFLAG{ &getMsgId( $IdNum ) } = 2;
    }

    &htmlGen( 'ThreadArticle.xml' );
}

sub hg_thread_article_tree
{
    &Fatal( 18, "$_[0]/ThreadArticleTree" ) if ( $_[0] ne 'ThreadArticle.xml' );

    $gHgStr .= $HTML_HR;

    local( $AddNum ) = "&num=$gNum&old=$gOld&rev=$gRev";

    local( $Id, $IdNum, $Fid );
    if ( $gTo < $gFrom )
    {
	# �����ä��ġ�
	$gHgStr .= "<ul>\n<li>$H_NOARTICLE</li>\n</ul>\n";
    }
    elsif ( $gVRev )
    {
	$gHgStr .= "<ul>\n" if $gFold;

	for( $IdNum = $gFrom; $IdNum <= $gTo; $IdNum++ )
	{
	    # ����������ID����Ф�
	    $Id = &getMsgId( $IdNum );
	    ( $Fid = &getMsgParents( $Id )) =~ s/,.*$//o;
	    # �������Ȥϸ�󤷡�
	    next if (( $Fid ne '' ) && (( $gADDFLAG{$Fid} == 2 ) || ( $SYS_THREAD_FORMAT == 2 )));

	    # �Ρ��ɤ�ɽ��
	    $gHgStr .= "<ul>\n" unless $gFold;
	    if ( $gFold )
	    {
		&ThreadTitleNodeNoThread( $Id, 3 );
	    }
	    elsif ( $SYS_THREAD_FORMAT == 0 )
	    {
		&ThreadTitleNodeThread( $Id, 3 );
	    }
	    elsif ( $SYS_THREAD_FORMAT == 1 )
	    {
		&ThreadTitleNodeAllThread( $Id, 3 );
	    }
	    else
	    {
		&ThreadTitleNodeNoThread( $Id, 3 );
	    }
	    $gHgStr .= "</ul>\n" unless $gFold;
	    &cgiprint'Cache( $gHgStr ); $gHgStr = '';
	}
	$gHgStr .= "</ul>\n" if $gFold;
    }
    else
    {
	$gHgStr .= "<ul>\n" if $gFold;

	for( $IdNum = $gTo; $IdNum >= $gFrom; $IdNum-- )
	{
	    $Id = &getMsgId( $IdNum );
	    ( $Fid = &getMsgParents( $Id )) =~ s/,.*$//o;
	    next if (( $Fid ne '' ) && (( $gADDFLAG{$Fid} == 2 ) || ( $SYS_THREAD_FORMAT == 2 )));

	    $gHgStr .= "<ul>\n" unless $gFold;
	    if ( $gFold )
	    {
		&ThreadTitleNodeNoThread( $Id, 3 );
	    }
	    elsif ( $SYS_THREAD_FORMAT == 0 )
	    {
		&ThreadTitleNodeThread( $Id, 3 );
	    }
	    elsif ( $SYS_THREAD_FORMAT == 1 )
	    {
		&ThreadTitleNodeAllThread( $Id, 3 );
	    }
	    else
	    {
		&ThreadTitleNodeNoThread( $Id, 3 );
	    }
	    $gHgStr .= "</ul>\n" unless $gFold;
	    &cgiprint'Cache( $gHgStr ); $gHgStr = '';
	}
	$gHgStr .= "</ul>\n" if $gFold;
    }
}

sub hg_thread_article_body
{
    &Fatal( 18, "$_[0]/ThreadArticleBody" ) if ( $_[0] ne 'ThreadArticle.xml' );

    local( $id );
    if ( $#gIDLIST >= 0 )
    {
	$gHgStr .= $HTML_HR;
	while ( $id = shift( @gIDLIST ))
	{
	    &DumpArtBody( $id, $SYS_COMMAND_EACH, 1 );
	    $gHgStr .= $HTML_HR;
	}
    }
}


###
## ����å��̥����ȥ����
#
sub UIThreadTitle
{
    # Isolation level: READ UNCOMITTED.
    &LockBoard();
    &DbCache( $BOARD ) if $BOARD;

    ( $gComType ) = @_;

    if ( $gComType == 3 )
    {
	# ��󥯤��������μ»�
	&ReLinkExec( $cgi'TAGS{'rfid'}, $cgi'TAGS{'rtid'}, $BOARD );

	# DB�񤭴������Τǡ�����å��夷ľ��
	&DbCache( $BOARD );
    }
    elsif ( $gComType == 5 )
    {
	# ��ư�μ»�
	&ReOrderExec( $cgi'TAGS{'rfid'}, $cgi'TAGS{'rtid'}, $BOARD );

	# DB�񤭴������Τǡ�����å��夷ľ��
	&DbCache( $BOARD );
    }

    &UnlockBoard();

    local( $vCom, $vStr );

    if ( $ComType == 0 )
    {
	$vCom = 'v';
	$vStr = '';
    }
    elsif ( $ComType == 2 )
    {
	$vCom = 'ct';
	$vStr = '&rtid=' . $cgi'TAGS{'roid'} . '&rfid=' . $cgi'TAGS{'rfid'} .
	    '&rtid=' . $cgi'TAGS{'rtid'};
    }
    elsif ( $gComType == 3 )
    {
	$vCom = 'v';
	$vStr = '';
    }
    elsif ( $gComType == 4 )
    {
	$vCom = 'mvt';
	$vStr = '&rtid=' . $cgi'TAGS{'roid'} . '&rfid=' . $cgi'TAGS{'rfid'} .
	    '&rtid=' . $cgi'TAGS{'rtid'};
    }
    elsif ( $gComType == 5 )
    {
	$vCom = 'v';
	$vStr = '';
    }

    %gADDFLAG = ();
    @gIDLIST = ();		# Not used here. It's for ThreadArticle.

    local( $nofMsg ) = &getNofMsg();

    # ɽ������Ŀ������
    $gNum = $cgi'TAGS{'num'};
    if ( defined( $cgi'TAGS{'id'} ))
    {
	$gOld = $nofMsg - int( $cgi'TAGS{'id'} + $gNum/2 );
	$gOld = 0 if ( $gOld < 0 );
    }
    else
    {
	$gOld = $cgi'TAGS{'old'};
    }
    $gRev = $cgi'TAGS{'rev'};
    $gFold = (( $SYS_THREAD_FORMAT == 2 ) || $cgi'TAGS{'fold'} )? 1 : 0;
    $gVRev = $gRev? 1-$SYS_BOTTOMTITLE : $SYS_BOTTOMTITLE;
    $gTo = $nofMsg - $gOld;
    $gFrom = $gTo - $gNum + 1;
    $gFrom = 0 if (( $gFrom < 0 ) || ( $gNum == 0 ));

    $gPageLinkStr = &PageLink( "$vCom$vStr", $gNum, $gOld, $gRev, $gFold );

    # �����Ѥߥե饰
    # 0 ... �����оݳ�
    # 1 ... �����Ѥ�
    # 2 ... ̤����
    local( $IdNum );
    for ( $IdNum = $gFrom; $IdNum <= $gTo; $IdNum++ )
    {
	$gADDFLAG{ &getMsgId( $IdNum ) } = 2;
    }

    &htmlGen( 'ThreadTitle.xml' );
}

sub hg_thread_title_board_header
{
    &Fatal( 18, "$_[0]/ThreadTitleBoardHeader" ) if ( $_[0] ne 'ThreadTitle.xml' );

    if ( $gComType == 2 )
    {
	$gHgStr .= "<p>������$H_REPLY�����ꤷ�ޤ���\n";
	$gHgStr .= "$H_MESG��#" . $cgi'TAGS{'rfid'} . "�פ򡤤ɤ�$H_MESG�ؤ�$H_REPLY�ˤ��ޤ���? $H_REPLY���$H_MESG��$H_RELINKTO_MARK�򥯥�å����Ƥ���������</p>\n";
    }
    elsif ( $gComType == 3 )
    {
	$gHgStr .= "<p>���ꤵ�줿$H_MESG��$H_REPLY����ѹ����ޤ�����</p>\n";
    }
    elsif ( $gComType == 4 )
    {
	$gHgStr .= "<p>��ư�����ꤷ�ޤ���\n";
	$gHgStr .= "$H_MESG��#" . $cgi'TAGS{'rfid'} . "�פ򡤤ɤ�$H_MESG�β��˰�ư���ޤ���? $H_MESG��$H_REORDERTO_MARK�򥯥�å����Ƥ���������</p>\n";
    }
    elsif ( $gComType == 5 )
    {
	$gHgStr .= "<p>���ꤵ�줿$H_MESG���ư���ޤ�����</p>\n";
    }

    &DumpBoardHeader();

    if ( $POLICY & 8 )
    {
	if ( $gComType == 3 )
	{
	    $gHgStr .= "<ul>\n<li>" . &LinkP( "b=$BOARD_ESC&c=ce&rtid=" .
		$cgi'TAGS{'roid'} . "&rfid=" . $cgi'TAGS{'rfid'},
		'�����ѹ��򸵤��᤹' ) . "</li>\n</ul>\n";
	}

	$gHgStr .= <<EOS;
<p>��$H_ICON�ϡ����Τ褦�ʰ�̣��ɽ���Ƥ��ޤ���</p>
<ul>
<li>$H_RELINKFROM_MARK:
����$H_MESG��$H_REPLY����ѹ����ޤ���$H_REPLY�����ꤹ����̤����Ӥޤ���</li>
<li>$H_REORDERFROM_MARK:
����$H_MESG�ν�����ѹ����ޤ�����ư�����ꤹ����̤����Ӥޤ���</li>
<li>$H_SUPERSEDE_ICON:
����$H_MESG���������ޤ���</li>
<li>$H_DELETE_ICON:
����$H_MESG�������ޤ���</li>
<li>$H_RELINKTO_MARK:
��˻��ꤷ��$H_MESG��$H_REPLY��򡤤���$H_MESG�ˤ��ޤ���</li>
<li>$H_REORDERTO_MARK:
��˻��ꤷ��$H_MESG�򡤤���$H_MESG�β��˰�ư���ޤ���</li>
</ul>
EOS
    }
}

sub hg_thread_title_tree
{
    &Fatal( 18, "$_[0]/ThreadTitleTree" ) if ( $_[0] ne 'ThreadTitle.xml' );

    local( $AddNum ) = "&num=$gNum&old=$gOld&rev=$gRev";

    local( $IdNum, $Id, $Fid );
    if ( $gTo < $gFrom )
    {
	# �����ä��ġ�
	$gHgStr .= "<ul>\n<li>$H_NOARTICLE</li>\n</ul>\n";
    }
    elsif ( $gVRev )
    {
	# �Ť��Τ������
	if (( $gComType == 2 ) && ( &getMsgParents( $cgi'TAGS{'rfid'} ) ne '' ))
	{
	    $gHgStr .= '<ul><li>' . &LinkP( "b=$BOARD_ESC&c=ce&rtid=&rfid=" .
		$cgi'TAGS{'rfid'} . '&roid=' . $cgi'TAGS{'roid'} . $AddNum,
		"[�ɤ�$H_MESG�ؤ�$H_REPLY�Ǥ�ʤ�������$H_MESG�ˤ���]" ) .
		"</li></ul>\n";
	}
	elsif ( $gComType == 4 )
	{
	    $gHgStr .= '<ul><li>' . &LinkP( "b=$BOARD_ESC&c=mve&rtid=&rfid=" .
		$cgi'TAGS{'rfid'} . "&roid=" . $cgi'TAGS{'roid'} . $AddNum,
		"[����������Ƭ�˰�ư����(���Υڡ����Ρ��ǤϤ���ޤ���)]" ) .
		"</li></ul>\n";
	}

	$gHgStr .= "<ul>\n" if $gFold;

	for( $IdNum = $gFrom; $IdNum <= $gTo; $IdNum++ )
	{
	    # ����������ID����Ф�
	    $Id = &getMsgId( $IdNum );
	    ( $Fid = &getMsgParents( $Id )) =~ s/,.*$//o;
	    # �������Ȥϸ�󤷡�
	    next if (( $Fid ne '' ) && (( $gADDFLAG{$Fid} == 2 ) ||
		( $SYS_THREAD_FORMAT == 2 )));

	    # �Ρ��ɤ�ɽ��
	    $gHgStr .= "<ul>\n" unless $gFold;
	    if ( $gFold )
	    {
		&ThreadTitleNodeNoThread( $Id, 1, $AddNum, ( $POLICY & 8 ));
	    }
	    elsif ( $SYS_THREAD_FORMAT == 0 )
	    {
		&ThreadTitleNodeThread( $Id, 1, $AddNum, ( $POLICY & 8 ));
	    }
	    elsif ( $SYS_THREAD_FORMAT == 1 )
	    {
		&ThreadTitleNodeAllThread( $Id, 1, $AddNum, ( $POLICY & 8 ));
	    }
	    else
	    {
		&ThreadTitleNodeNoThread( $Id, 1, $AddNum, ( $POLICY & 8 ));
	    }
	    $gHgStr .= "</ul>\n" unless $gFold;
	    &cgiprint'Cache( $gHgStr ); $gHgStr = '';
	}
	$gHgStr .= "</ul>\n" if $gFold;
    }
    else
    {
	# �������Τ������
	if (( $gComType == 2 ) && ( &getMsgParents( $cgi'TAGS{'rfid'} ) ne '' ))
	{
	    $gHgStr .= '<ul><li>' . &LinkP( "b=$BOARD_ESC&c=ce&rtid=&rfid=" .
		$cgi'TAGS{'rfid'} . "&roid=" . $cgi'TAGS{'roid'} . $AddNum,
		"[�ɤ�$H_MESG�ؤ�$H_REPLY�Ǥ�ʤ�������$H_MESG�ˤ���]" ) .
		"</li></ul>\n";
	}
	elsif ( $gComType == 4 )
	{
	    $gHgStr .= '<ul><li>' . &LinkP( "b=$BOARD_ESC&c=mve&rtid=&rfid=" .
		$cgi'TAGS{'rfid'} . "&roid=" . $cgi'TAGS{'roid'} . $AddNum,
		"[����������Ƭ�˰�ư����(���Υڡ����Ρ��ǤϤ���ޤ���)]" ) .
		"</li></ul>\n";
	}

	$gHgStr .= "<ul>\n" if $gFold;

	for( $IdNum = $gTo; $IdNum >= $gFrom; $IdNum-- )
	{
	    # ���Ʊ��
	    $Id = &getMsgId( $IdNum );
	    ( $Fid = &getMsgParents( $Id )) =~ s/,.*$//o;
	    next if (( $Fid ne '' ) && (( $gADDFLAG{$Fid} == 2 ) ||
		( $SYS_THREAD_FORMAT == 2 )));

	    $gHgStr .= "<ul>\n" unless $gFold;
	    if ( $gFold )
	    {
		&ThreadTitleNodeNoThread( $Id, 1, $AddNum, ( $POLICY & 8 ));
	    }
	    elsif ( $SYS_THREAD_FORMAT == 0 )
	    {
		&ThreadTitleNodeThread( $Id, 1, $AddNum, ( $POLICY & 8 ));
	    }
	    elsif ( $SYS_THREAD_FORMAT == 1 )
	    {
		&ThreadTitleNodeAllThread( $Id, 1, $AddNum, ( $POLICY & 8 ));
	    }
	    else
	    {
		&ThreadTitleNodeNoThread( $Id, 1, $AddNum, ( $POLICY & 8 ));
	    }
	    $gHgStr .= "</ul>\n" unless $gFold;
	    &cgiprint'Cache( $gHgStr ); $gHgStr = '';
	}
	$gHgStr .= "</ul>\n" if $gFold;
    }
}

# ����Ρ��ɤΤ�ɽ��
sub ThreadTitleNodeNoThread
{
    local( $id, $flag, $addNum, $maint ) = @_;

    local( $fid, $aids, $date, $title, $icon, $host, $name ) = &getMsgInfo( $id );
    &DumpArtSummaryItem( $id, $aids, $date, $title, $icon, $name, $flag );

    $flag &= 6; # 110
    push( @gIDLIST, $id );

    &ThreadTitleMaintIcon( $id, $addNum ) if $maint;

    $gHgStr .= "</li>\n";
}

# �ڡ����⥹��åɤΤ�ɽ��
sub ThreadTitleNodeThread
{
    local( $id, $flag, $addNum, $maint ) = @_;

    # �ڡ������ʤ餪���ޤ���
    return if ( $gADDFLAG{ $id } != 2 );

    local( $fid, $aids, $date, $title, $icon, $host, $name ) = &getMsgInfo( $id );
    &DumpArtSummaryItem( $id, $aids, (( !$SYS_COMPACTTHREAD || $flag&1 )? $date : 0 ), $title, $icon, $name, $flag );

    $flag &= 6; # 110
    $gADDFLAG{ $id } = 1;		# �����Ѥ�
    push( @gIDLIST, $id );

    &ThreadTitleMaintIcon( $id, $addNum ) if $maint;

    # ̼�����Сġ�
    if ( $aids )
    {
	$gHgStr .= "<ul>\n";
	foreach ( split( /,/, $aids ))
	{
	    &ThreadTitleNodeThread( $_, $flag, $addNum, $maint );
	}
	$gHgStr .= "</ul>\n";
    }
    $gHgStr .= "</li>\n";
}

# ������åɤ�ɽ��
sub ThreadTitleNodeAllThread
{
    local( $id, $flag, $addNum, $maint ) = @_;

    # ɽ���Ѥߤʤ餪���ޤ���
    return if ( $gADDFLAG{ $id } == 1 );

    local( $fid, $aids, $date, $title, $icon, $host, $name ) = &getMsgInfo( $id );
    &DumpArtSummaryItem( $id, $aids, (( !$SYS_COMPACTTHREAD || $flag&1 )? $date : 0 ), $title, $icon, $name, $flag );

    $flag &= 6; # 110
    $gADDFLAG{ $id } = 1;		# �����Ѥ�
    push( @gIDLIST, $id );

    &ThreadTitleMaintIcon( $id, $addNum ) if $maint;

    # ̼�����Сġ�
    if ( $aids )
    {
	$gHgStr .= "<ul>\n";
	foreach ( split( /,/, $aids ))
	{
	    &ThreadTitleNodeAllThread( $_, $flag, $addNum, $maint );
	}
	$gHgStr .= "</ul>\n";
    }
    $gHgStr .= "</li>\n";
}

# �������ѤΥ�������ɽ��
sub ThreadTitleMaintIcon
{
    local( $id, $addNum ) = @_;

    $gHgStr .= " .......... \n";

    local( $fromId ) = $cgi'TAGS{'rfid'};
    local( $oldId ) = $cgi'TAGS{'roid'};

    local( $parents ) = &getMsgParents( $id );

    # ������ѹ����ޥ��(From)
    $gHgStr .= &LinkP( "b=$BOARD_ESC&c=ct&rfid=$id&roid=" . $parents . $addNum,
	$H_RELINKFROM_MARK, '', $H_RELINKFROM_MARK_L ) . "\n";

    if ( $parents eq '' )
    {
	# ��ư���ޥ��(From)
	$gHgStr .= &LinkP( "b=$BOARD_ESC&c=mvt&rfid=$id&roid=" . $parents .
	    $addNum, $H_REORDERFROM_MARK, '', $H_REORDERFROM_MARK_L ) . "\n";
    }

    # ������������ޥ��
    $gHgStr .= &LinkP( "b=$BOARD_ESC&c=f&s=on&id=$id", $H_SUPERSEDE_ICON, '',
	$H_SUPERSEDE_ICON_L ) . "\n";
    $gHgStr .= &LinkP( "b=$BOARD_ESC&c=dp&id=$id", $H_DELETE_ICON, '',
	$H_DELETE_ICON_L ) . "\n";

    # ��ư���ޥ��(To)
    if (( $gComType == 4 ) && ( $fromId ne $id ) && ( $parents eq '' ) && ( $fromId ne $id ))
    {
	$gHgStr .= &LinkP(
	    "b=$BOARD_ESC&c=mve&rtid=$id&rfid=$fromId&roid=$oldId" .
	    $addNum, $H_REORDERTO_MARK, '', $H_REORDERTO_MARK_L ) . "\n";
    }

    # ������ѹ����ޥ��(To)
    if (( $gComType == 2 ) && ( $fromId ne $id ) &&
	( !grep( /^$fromId$/, split( /,/, &getMsgDaughters( $id )))) &&
	( !grep( /^$fromId$/, split( /,/, $parents ))))
    {
	$gHgStr .= &LinkP( "b=$BOARD_ESC&c=ce&rtid=$id&rfid=$fromId&roid=$oldId" . $addNum, $H_RELINKTO_MARK, '', $H_RELINKTO_MARK_L ) . "\n";
    }
}


###
## �񤭹��߽祿���ȥ����
#
sub UISortTitle
{
    # Isolation level: READ UNCOMITTED.
    &LockBoard();
    &DbCache( $BOARD ) if $BOARD;
    &UnlockBoard();

    local( $nofMsg ) = &getNofMsg();

    # ɽ������Ŀ������
    local( $Num ) = $cgi'TAGS{'num'};
    local( $Old );
    if ( defined( $cgi'TAGS{'id'} ))
    {
	$Old = $nofMsg - int( $cgi'TAGS{'id'} + $Num/2 );
	$Old = 0 if ( $Old < 0 );
    }
    else
    {
	$Old = $cgi'TAGS{'old'};
    }
    local( $Rev ) = $cgi'TAGS{'rev'};
    $gFold = (( $SYS_THREAD_FORMAT == 2 ) || $cgi'TAGS{'fold'} )? 1 : 0;
    $gVRev = $Rev? 1-$SYS_BOTTOMTITLE : $SYS_BOTTOMTITLE;
    $gTo = $nofMsg - $Old;
    $gFrom = $gTo - $Num + 1;
    $gFrom = 0 if (( $gFrom < 0 ) || ( $Num == 0 ));

    $gPageLinkStr = &PageLink( 'r', $Num, $Old, $Rev, '' );

    &htmlGen( 'SortTitle.xml' );
}

sub hg_sort_title_tree
{
    &Fatal( 18, "$_[0]/SortTitleTree" ) if ( $_[0] ne 'SortTitle.xml' );

    $gHgStr .= "<ul>\n";

    # ������ɽ��
    local( $IdNum, $Id, $fid, $aids, $date, $title, $icon, $host, $name );

    local( $nofMsg ) = &getNofMsg();
    if ( $nofMsg == -1 )
    {
	# �����ä��ġ�
	$gHgStr .= "<li>$H_NOARTICLE</li>\n";
    }
    else
    {
	if ( $gVRev )
	{
	    for ($IdNum = $gFrom; $IdNum <= $gTo; $IdNum++)
	    {
		$Id = &getMsgId( $IdNum );
		( $fid, $aids, $date, $title, $icon, $host, $name ) = &getMsgInfo( $Id );
		&DumpArtSummaryItem( $Id, $aids, $date, $title, $icon, $name, 1 );
		$gHgStr .= "</li>\n";
	    }
	}
	else
	{
	    for ($IdNum = $gTo; $IdNum >= $gFrom; $IdNum--)
	    {
		$Id = &getMsgId( $IdNum );
		( $fid, $aids, $date, $title, $icon, $host, $name ) = &getMsgInfo( $Id );
		&DumpArtSummaryItem( $Id, $aids, $date, $title, $icon, $name, 1 );
		$gHgStr .= "</li>\n";
	    }
	}
    }
    $gHgStr .= "</ul>\n";
}


###
## ����å��̵�������
#
sub UIShowThread
{
    # Isolation level: READ UNCOMITTED.
    &LockBoard();
    &DbCache( $BOARD ) if $BOARD;
    &UnlockBoard();

    $gId = $cgi'TAGS{'id'};

    $gFids = &getMsgParents( $gId );

    # �ե����������ڹ�¤�μ���
    # ex. '( a ( b ( c d ) ) ( e ) ( f ( g ) ) )'�Ȥ����ꥹ��
    @gFollowIdTree = ();
    &GetFollowIdTree( $gId, *gFollowIdTree );

    &htmlGen( 'ShowThread.xml' );
}

sub hg_show_thread_title
{
    &Fatal( 18, "$_[0]/ShowThreadTitle" ) if ( $_[0] ne 'ShowThread.xml' );
    $gHgStr .= &getMsgSubject( &GetTreeTopArticle( *gFollowIdTree ));
}

sub hg_show_thread_title_tree
{
    &Fatal( 18, "$_[0]/ShowThreadTitleTree" ) if ( $_[0] ne 'ShowThread.xml' );

    &DumpOriginalArticles( $gFids );
    &DumpArtThread( 6, @gFollowIdTree );
}

sub hg_show_thread_msg_body
{
    &Fatal( 18, "$_[0]/ShowThreadMsgBody" ) if ( $_[0] ne 'ShowThread.xml' );
    &DumpArtThread( 2, @gFollowIdTree );
}

sub hg_show_thread_back_to_title_button
{
    &Fatal( 18, "$_[0]/ShowThreadBackToTitleButton" ) if ( $_[0] ne 'ShowThread.xml' );
    &DumpButtonToTitleList( $BOARD, $gId );
}


###
## �񤭹��߽��å���������
#
sub UISortArticle
{
    # Isolation level: READ UNCOMITTED.
    &LockBoard();
    &DbCache( $BOARD ) if $BOARD;
    &UnlockBoard();

    $gNum = $cgi'TAGS{'num'};
    $gOld = $cgi'TAGS{'old'};
    $gRev = $cgi'TAGS{'rev'};
    $gFold = (( $SYS_THREAD_FORMAT == 2 ) || $cgi'TAGS{'fold'} )? 1 : 0;

    $gPageLinkStr = &PageLink( 'l', $gNum, $gOld, $gRev, '' );

    &htmlGen( 'SortArticle.xml' );
}

sub hg_sort_article_body
{
    &Fatal( 18, "$_[0]/SortArticleBody" ) if ( $_[0] ne 'SortArticle.xml' );

    local( $vRev ) = $gRev? 1-$SYS_BOTTOMARTICLE : $SYS_BOTTOMARTICLE;
    local( $nofMsg ) = &getNofMsg();
    local( $To ) = $nofMsg - $gOld;
    local( $From ) = $To - $gNum + 1; $From = 0 if (( $From < 0 ) || ( $gNum == 0 ));

    $gHgStr .= $HTML_HR;

    if ( $nofMsg == -1 )
    {
	# �����ä��ġ�
	$gHgStr .= "<p>$H_NOARTICLE</p>\n";
    }
    else
    {
	local( $IdNum, $Id );
	if ( $vRev )
	{
	    for ( $IdNum = $From; $IdNum <= $To; $IdNum++ )
	    {
		$Id = &getMsgId( $IdNum );
		&DumpArtBody( $Id, $SYS_COMMAND_EACH, 1 );
		$gHgStr .= $HTML_HR;
	    }
	}
	else
	{
	    for ( $IdNum = $To; $IdNum >= $From; $IdNum-- )
	    {
		$Id = &getMsgId( $IdNum );
		&DumpArtBody( $Id, $SYS_COMMAND_EACH, 1 );
		$gHgStr .= $HTML_HR;
	    }
	}
    }
}


###
## ñ�쵭����ɽ��
#
sub UIShowArticle
{
    # Isolation level: READ UNCOMITTED.
    &LockBoard();
    &DbCache( $BOARD ) if $BOARD;
    &UnlockBoard();

    $gId = $cgi'TAGS{'id'};

    # ̤��Ƶ������ɤ�ʤ�
    &Fatal( 8, '' ) if ( &getMsgSubject( $gId ) eq '' );

    &htmlGen( 'ShowArticle.xml' );
}

sub hg_show_article_title
{
    &Fatal( 18, "$_[0]/ShowArticleTitle" ) if ( $_[0] ne 'ShowArticle.xml' );
    $gHgStr .= &getMsgSubject( $gId );
}

sub hg_show_article_body
{
    &Fatal( 18, "$_[0]/ShowArticleBody" ) if ( $_[0] ne 'ShowArticle.xml' );
    &DumpArtBody( $gId, 1, 1 );
}

sub hg_show_article_original
{
    &Fatal( 18, "$_[0]/ShowArticleOriginal" ) if ( $_[0] ne 'ShowArticle.xml' );
    local( $fids ) = &getMsgParents( $gId );
    if ( $fids ne '' )
    {
	$gHgStr .= "<p>��$H_ORIG</p>\n";
	&DumpOriginalArticles( $fids );
    }
}

sub hg_show_article_reply
{
    &Fatal( 18, "$_[0]/ShowArticleReply" ) if ( $_[0] ne 'ShowArticle.xml' );

    $gHgStr .= "<p>��$H_REPLY</p>\n";
    &DumpReplyArticles( &getMsgDaughters( $gId ));
}


###
## �����θ���(ɽ�����̤κ���)
#
sub UISearchArticle
{
    # Isolation level: READ UNCOMITTED.
    &LockBoard();
    &DbCache( $BOARD ) if $BOARD;
    &UnlockBoard();

    &htmlGen( 'SearchArticle.xml' );
}

sub hg_search_article_result
{
    &Fatal( 18, "$_[0]/SearchArticleResult" ) if ( $_[0] ne 'SearchArticle.xml' );

    local( $Key ) = $cgi'TAGS{'key'};
    local( $SearchSubject ) = $cgi'TAGS{'searchsubject'};
    local( $SearchPerson ) = $cgi'TAGS{'searchperson'};
    local( $SearchArticle ) = $cgi'TAGS{'searcharticle'};
    local( $SearchPostTime ) = $cgi'TAGS{'searchposttime'};
    local( $SearchPostTimeFrom ) = $cgi'TAGS{'searchposttimefrom'};
    local( $SearchPostTimeTo ) = $cgi'TAGS{'searchposttimeto'};
    local( $SearchIcon ) = $cgi'TAGS{'searchicon'};
    local( $Icon ) = $cgi'TAGS{'icon'};

    # ������ɤ����Ǥʤ���С����Υ�����ɤ�ޤ൭���Υꥹ�Ȥ�ɽ��
    if ( $SearchIcon || ( $SearchPostTime && ( $SearchPostTimeFrom ||
	$SearchPostTimeTo )) || (( $Key ne '' ) && ( $SearchSubject ||
	$SearchPerson || $SearchArticle )))
    {
	&DumpSearchResult( $Key, $SearchSubject, $SearchPerson,
	    $SearchArticle, $SearchPostTime, $SearchPostTimeFrom,
	    $SearchPostTimeTo, $SearchIcon, $Icon );
    }
}


###
## ��������γ�ǧ
#
sub UIDeletePreview
{
    # Isolation level: READ UNCOMITTED.
    &LockBoard();
    &DbCache( $BOARD ) if $BOARD;
    &UnlockBoard();

    if ( !( $POLICY & 8 ) && ( $SYS_OVERWRITE == 0 ))
    {
	&Fatal( 99, $cgi'TAGS{'c'} );
    }

    $gId = $cgi'TAGS{'id'};
    $gAids = &getMsgDaughters( $gId );

    # ̤��Ƶ������ɤ�ʤ�
    &Fatal( 8, '' ) if ( &getMsgSubject( $gId ) eq '' );

    &htmlGen( 'DeletePreview.xml' );
}

sub hg_delete_preview_form
{
    &Fatal( 18, "$_[0]/DeletePreviewForm" ) if ( $_[0] ne 'DeletePreview.xml' );

    local( %tags );
    %tags = ( 'c', 'de', 'b', $BOARD, 'id', $gId );
    &DumpForm( *tags, '���Υ�å������������ޤ�', '', '' );

    if ( $gAids )
    {
	%tags = ( 'c', 'det', 'b', $BOARD, 'id', $gId );
	&DumpForm( *tags, "$H_REPLY��å�������ޤȤ�ƺ�����ޤ�", '', '' );
    }
}

sub hg_delete_preview_body
{
    &Fatal( 18, "$_[0]/DeletePreviewBody" ) if ( $_[0] ne 'DeletePreview.xml' );
    &DumpArtBody( $gId, 0, 1 );
}

sub hg_delete_preview_reply
{
    &Fatal( 18, "$_[0]/DeletePreviewReply" ) if ( $_[0] ne 'DeletePreview.xml' );

    $gHgStr .= "<p>��$H_REPLY</p>\n";
    &DumpReplyArticles( $gAids );
}


###
## �����κ��
#
sub UIDeleteExec
{
    # Isolation level: SERIALIZABLE.
    &LockBoard();
    &DbCache( $BOARD ) if $BOARD;

    if ( !( $POLICY & 8 ) && ( $SYS_OVERWRITE == 0 ))
    {
	&Fatal( 99, $cgi'TAGS{'c'} );
    }

    local( $threadFlag ) = @_;

    $gId = $cgi'TAGS{'id'};

    local( $name ) = &getMsgAuthor( $gId );
    &Fatal( 44, '' ) if ( !&IsUser( $name ) && !( $POLICY & 8 ));
    &Fatal( 19, '' ) if (( &getMsgDaughters( $gId ) ne '' ) && ( $SYS_OVERWRITE == 1 ));

    # ����¹�
    &DeleteArticle( $gId, $BOARD, $threadFlag );

    &htmlGen( 'DeleteExec.xml' );

    &UnlockBoard();
}

sub hg_delete_exec_back_to_title_button
{
    &Fatal( 18, "$_[0]/DeleteExecBackToTitleButton" ) if ( $_[0] ne 'DeleteExec.xml' );
    &DumpButtonToTitleList( $BOARD, $gId );
}


###
## ��������ɽ��
#
sub UIShowIcon
{
    # Isolation level: CHAOS.

    &htmlGen( 'ShowIcon.xml' );
}


###
## �إ��ɽ��
#
sub UIHelp
{
    # Isolation level: CHAOS.

    &htmlGen( 'Help.xml' );
}


###
## ���顼ɽ��
#
sub UIFatal
{
    # Isolation level: CHAOS.

    ( $gMsg ) = @_;
    &htmlGen( 'Fatal.xml' );
}

sub hg_fatal_msg
{
    $gHgStr .= $gMsg;
}


###
## ����hg�ؿ���
#
sub hg_s_title
{
    $gHgStr .= <<EOS;
<meta http-equiv="Content-Type" content='text/html; charset="EUC-JP"' />
<meta http-equiv="Content-Style-Type" content="text/css" />
<link rev="MADE" href="mailto:$MAINT" />
EOS

    $gHgStr .= sprintf( qq(<link rel="StyleSheet" href="%s" type="text/css" media="screen" />), &GetStyleSheetURL( $STYLE_FILE )) if $STYLE_FILE;
}

sub hg_s_address
{
    $gHgStr .= "<address>\nMaintenance: " .
	&TagA( $MAINT_NAME, "mailto:$MAINT" ) . $HTML_BR .
	&TagA( $PROGNAME, 'http://www.jin.gr.jp/~nahi/kb/' ) .
	": Copyright &copy; 1995-2000 " .
	&TagA( 'NAKAMURA, Hiroshi', 'http://www.jin.gr.jp/~nahi/' ) .
	".\n</address>\n";
}

sub hg_c_status
{
    $gHgStr .= qq(<p class="kbStatus">[);
    if ( $UNAME && ( $UNAME ne $GUEST ) && ( $UNAME ne $cgiauth'F_COOKIE_RESET ))
    {
	$gHgStr .= "$H_USER: $UNAME -- \n";
    }
    $gHgStr .= "$H_BOARD: $BOARDNAME -- \n" if ( $BOARDNAME ne '' );
    $gHgStr .= "����: " . &GetDateTimeFormatFromUtc( $^T );
    $gHgStr .= "]</p>\n";
}

sub hg_c_remote_info
{
    $gHgStr .= $REMOTE_INFO;
}

sub hg_c_auth_user
{
    if ( $UNAME && ( $UNAME ne $GUEST ) && ( $UNAME ne $cgiauth'F_COOKIE_RESET ))
    {
	$gHgStr .= $UNAME;
    }
    else
    {
	$gHgStr .= $GUEST;
    }
}

sub hg_c_exec_date_time
{
    $gHgStr .= &GetDateTimeFormatFromUtc( $^T );
}

sub hg_c_top_menu
{
    $gHgStr .= qq(<div class="kbTopMenu">\n);
    local( $formStr, $contents );

    if ( $SYS_AUTH )
    {
	$formStr .= &LinkP( 'c=bl', 'TOP', 'J' ) . "\n";
#	$formStr .= ' ' . &LinkP( 'c=ue', 'OPEN', 'O' ) . "\n";
	$formStr .= ' ' . &LinkP( 'c=lo', 'LOGIN', 'L' ) . "\n";
	if ( $UNAME && ( $UNAME ne $GUEST ) && ( $UNAME ne $cgiauth'F_COOKIE_RESET ))
	{
	    $formStr .= ' ' . &LinkP( 'c=uc', 'INFO', 'C' ) . "\n";
	}
	$formStr .= "&nbsp;&nbsp;&nbsp;\n";
    }

    $formStr .= &TagLabel( "ɽ������", 'c', 'W' ) . ": \n";

    if ( $BOARD )
    {
	$contents .= sprintf( qq[<option%s value="v">�ǿ�$H_SUBJECT����(����å�)</option>\n], ( $SYS_TITLE_FORMAT == 0 )? ' selected="selected"' : '' );
	$contents .= sprintf( qq[<option%s value="r">�ǿ�$H_SUBJECT����(�񤭹��߽�)</option>\n], ( $SYS_TITLE_FORMAT == 1 )? ' selected="selected"' : '' );
	$contents .= qq[<option value="vt">�ǿ�$H_MESG����(����å�)</option>\n];
	$contents .= qq[<option value="l">�ǿ�$H_MESG����(�񤭹��߽�)</option>\n];
	$contents .= qq(<option value="v">--------</option>\n);
	$contents .= qq(<option value="s">$H_MESG�θ���</option>\n);
	$contents .= qq(<option value="i">�Ȥ���$H_ICON����</option>\n) if $SYS_ICON;
	if (( $POLICY & 2 ) && ( !$SYS_NEWART_ADMINONLY || ( $POLICY & 8 )))
	{
	    $contents .= qq(<option value="v">--------</option>\n);
	    $contents .= qq(<option value="n">$H_POSTNEWARTICLE</option>\n);
	}
    }
    else
    {
	$contents .= qq(<option selected="selected" value="bl">$H_BOARD����</option>\n);
    }

    $formStr .= &TagSelect( 'c', $contents ) . "\n&nbsp;&nbsp;&nbsp;" .
	&TagLabel( "ɽ�����", 'num', 'Y' ) . ': ' .
	&TagInputText( 'text', 'num', (( $cgi'TAGS{'num'} ne '' )? $cgi'TAGS{'num'} : $DEF_TITLE_NUM ),	3 );

    local( %tags ) = ( 'b', $BOARD );
    $tags{ 'old' } = $cgi'TAGS{'old'} if ( defined $cgi'TAGS{'old'} );
    $tags{ 'rev' } = $cgi'TAGS{'rev'} if ( defined $cgi'TAGS{'rev'} );
    $tags{ 'fold' } = $cgi'TAGS{'fold'} if ( defined $cgi'TAGS{'fold'} );
    &DumpForm( *tags, 'ɽ��(V)', '', *formStr );
    $gHgStr .= "</div>\n";
}

sub hg_c_help
{
    $gHgStr .= &LinkP( "b=$BOARD_ESC&c=h", &TagComImg( $ICON_HELP, '�إ��' ), 'H', '', '', $_[1] );
}

sub hg_c_site_name
{
    $gHgStr .= $SYSTEM_NAME;
}

sub hg_c_func_link
{
    return unless $SYS_AUTH;

    $gHgStr .= "<dl>\n";

    $gHgStr .= "<dt>�ֿ�����$H_USER����򥵡��Ф���Ͽ�����</dt>\n";
    $gHgStr .= '<dd>��' . &LinkP( 'c=ue', "$H_USER��������Ⱥ����ڡ���" .
	&TagAccessKey( 'O' ), 'O' ) . "</dd>\n";

    if ( $UNAME )
    {
	$gHgStr .= "<dt>���̤�$H_USER�����ƤӽФ��סʸ����������$H_USER����ϡ�$UNAME�Τ�ΤǤ���</dt>\n";
	$gHgStr .= '<dd>��' . &LinkP( 'c=lo', "������ڡ���" . &TagAccessKey( 'L' ), 'L' ) . "</dd>\n";
    }

    if ( $POLICY & 4 )
    {
	$gHgStr .= "<dt>��$UNAME�ˤĤ�����Ͽ����$H_USER������ѹ������</dt>\n";
	$gHgStr .= '<dd>��' . &LinkP( 'c=uc', "$H_USER����ڡ���" . &TagAccessKey( 'C' ), 'C' ) . "</dd>\n";
    }

    if ( $POLICY & 8 )
    {
	$gHgStr .= "<dt>�ֿ�����$H_BOARD���ꤿ����</dt>\n";
	$gHgStr .= '<dd>��' . &LinkP( 'c=be', "$H_BOARD�ο�������" .
	    &TagAccessKey( 'A' ), 'A' ) . "</dd>\n";
    }

    $gHgStr .= "</dl>\n";
}

sub hg_c_page_link
{
    $gHgStr .= $gPageLinkStr;
}

sub hg_c_board_link_all
{
    # ���Ǽ��Ĥξ������Ф�
    local( @board, %boardName, %boardInfo );
    &GetAllBoardInfo( *board, *boardName, *boardInfo );

    $gHgStr .= "<ul>\n";

    local( $newIcon, $modTimeUtc, $modTime, $nofArticle, $boardEsc );
    foreach ( @board )
    {
	$modTimeUtc = &getBoardLastmod( $_ );
	$modTime = &GetDateTimeFormatFromUtc( $modTimeUtc );
	if ( $SYS_BLIST_NEWICON_DATE &&
	    (( $^T - $modTimeUtc ) < $SYS_BLIST_NEWICON_DATE * 86400 ))
	{
	    $newIcon = " " . &TagMsgImg( $H_NEWARTICLE );
	}
	else
	{
	    $newIcon = '';
	}
	&GetArticleId( $_, *nofArticle ) || 0;

	$boardEsc = &URIEscape( $_ );
	$gHgStr .= '<li>' .
	    &LinkP( "b=$boardEsc&c=" . ( $SYS_TITLE_FORMAT? 'r' : 'v' ) .
	    "&num=$DEF_TITLE_NUM", $boardName{$_} ) .
	    "$newIcon\n[�ǿ�: $modTime, �ǿ�${H_MESG}ID: $nofArticle]\n";
	if ( $POLICY & 8 )
	{
	    $gHgStr .= &LinkP( "b=$boardEsc&c=bc", "�������ѹ�" ) . "\n";
	}

	$gHgStr .= $HTML_BR . $HTML_BR . "</li>\n";
    }
    $gHgStr .= "</ul>\n";
}

sub hg_c_board_link
{
    local( $com, $board ) = split( ',', $_[1], 2 );
    local( $num );
    return unless $board;
    if ( $com eq 'title-thread' )
    {
	$com = 'v';
	$num = $DEF_TITLE_NUM;
    }
    elsif ( $com eq 'title-bydate' )
    {
	$com = 'r';
	$num = $DEF_TITLE_NUM;
    }
    elsif ( $com eq 'message-thread' )
    {
	$com = 'vt';
	$num = $DEF_ARTICLE_NUM;
    }
    elsif ( $com eq 'message-bydate' )
    {
	$com = 'l';
	$num = $DEF_ARTICLE_NUM;
    }
    else
    {
	return;
    }

    if ( !$gBoardInfoDbCached )
    {
	local( $tmp );
	&GetAllBoardInfo( *tmp, *gBoardName, *tmp );
	$gBoardInfoDbCached = 1;
    }

    $modTimeUtc = &getBoardLastmod( $board );
    $modTime = &GetDateTimeFormatFromUtc( $modTimeUtc );
    if ( $SYS_BLIST_NEWICON_DATE &&
	(( $^T - $modTimeUtc ) < $SYS_BLIST_NEWICON_DATE * 86400 ))
    {
	$newIcon = " " . &TagMsgImg( $H_NEWARTICLE );
    }
    else
    {
	$newIcon = '';
    }
    &GetArticleId( $board, *nofArticle ) || 0;

    local( $boardEsc ) = &URIEscape( $board );
    $gHgStr .= &LinkP( "b=$boardEsc&c=$com&num=$num", $gBoardName{$board} ) .
	"$newIcon\n[�ǿ�: $modTime, �ǿ�${H_MESG}ID: $nofArticle]\n";
    if ( $POLICY & 8 )
    {
	$gHgStr .= &LinkP( "b=$boardEsc&c=bc", "�������ѹ�" ) . "\n";
    }
}

sub hg_c_anchor
{
    $gHgStr .= &TagA( split( ',', $_[1] ));
}

sub hg_c_icon_msg
{
    $gHgStr .= &TagMsgImg( $_[1] );
}

sub hg_c_icon
{
    local( $src, $alt ) = split( ',', $_[1], 2 );
    $gHgStr .= &TagComImg( &GetIconURL( $src ), $alt );
}

sub hg_b_board_name
{
    $gHgStr .= $BOARDNAME if $BOARD;
}

sub hg_b_board_header
{
    &DumpBoardHeader() if $BOARD;
}

sub hg_b_post_entry_form
{
    if ( $POLICY & 2 )
    {
	&DumpArtEntry( $gDefIcon, $gEntryType, $gId, $gDefPostDateStr, $gDefSubject, $gDefTextType, $gDefArticle, $gDefName, $gDefEmail, $gDefUrl, $gDefFmail );
    }
}

sub hg_b_search_article_form
{
    local( $Key ) = $cgi'TAGS{'key'};
    local( $SearchSubject ) = $cgi'TAGS{'searchsubject'};
    local( $SearchPerson ) = $cgi'TAGS{'searchperson'};
    local( $SearchArticle ) = $cgi'TAGS{'searcharticle'};
    local( $SearchPostTime ) = $cgi'TAGS{'searchposttime'};
    local( $SearchPostTimeFrom ) = $cgi'TAGS{'searchposttimefrom'};
    local( $SearchPostTimeTo ) = $cgi'TAGS{'searchposttimeto'};
    local( $SearchIcon ) = $cgi'TAGS{'searchicon'};
    local( $Icon ) = $cgi'TAGS{'icon'};

    local( $msg, $contents );
    $contents = &TagInputCheck( 'searchsubject', $SearchSubject ) . ': ' . &TagLabel( $H_SUBJECT, 'searchsubject', 'T' ) . $HTML_BR;

    $contents .= &TagInputCheck( 'searchperson', $SearchPerson ) . ': ' . &TagLabel( "̾��", 'searchperson', 'N' ) . $HTML_BR;

    $contents .= &TagInputCheck( 'searcharticle', $SearchArticle ) . ': ' . &TagLabel( $H_MESG, 'searcharticle', 'A' ) . $HTML_BR;

    local( $sec, $min, $hour, $mday, $mon, $year, $nowStr );
    if ( !$SearchPostTime )
    {
	( $sec, $min, $hour, $mday, $mon, $year, $nowStr ) = localtime( $^T );
	$nowStr = sprintf( "%04d/%02d/%02d", $year+1900, $mon+1, $mday );
    }
    $contents .= &TagInputCheck( 'searchposttime', $SearchPostTime ) . ': ' . &TagLabel( $H_DATE, 'searchposttime', 'D' ) . " // \n";
    $contents .= &TagInputText( 'text', 'searchposttimefrom', ( $SearchPostTimeFrom || '' ), 11 ) . ' ' . &TagLabel( '��', 'searchposttimefrom', 'S' ) . " \n";
    $contents .= &TagInputText( 'text', 'searchposttimeto', ( $SearchPostTimeTo || '' ), 11 ) . &TagLabel( '�δ�', 'searchposttimeto', 'E' ) . $HTML_BR;

    if ( $SYS_ICON )
    {
	$contents .= $HTML_BR . &TagLabel( $H_ICON, 'icon', 'I' ) . ": \n";

	# �������������
	local( $selContents, $IconTitle );
	$selContents = sprintf( qq(<option%s>$H_NOICON</option>\n), ( $Icon &&
	    ( $Icon ne $H_NOICON ))? '' : ' selected="selected"' );
	foreach $IconTitle ( sort keys( %ICON_FILE ))
	{
	    $selContents .= sprintf( "<option%s>$IconTitle</option>\n",
	    	( $Icon eq $IconTitle )? ' selected="selected"' : '' );
	}
	$contents .= &TagSelect( 'icon', $selContents ) . "\n";

	$contents .= "�Ȥ���$H_ICON\n";

	$selContents = sprintf( qq[<option%s value="0">(�������󸡺��򤷤ʤ�)</option>\n], ( $SearchIcon == 0 )? ' selected="selected"' : '' );

	$selContents .= qq(<option value="0">----------------</option>\n);
	$selContents .= sprintf( qq[<option%s value="1">�����$H_MESG��õ��</option>\n], ( $SearchIcon == 1 )? ' selected="selected"' : '' );
	$selContents .= sprintf( qq[<option%s value="1001">������ʤ�$H_MESG��õ��</option>\n], ( $SearchIcon == 1001 )? ' selected="selected"' : '' );

	$selContents .= qq(<option value="0">----------------</option>\n);
	$selContents .= sprintf( qq[<option%s value="11">��ľ�ܤ�$H_REPLY�ˤ���$H_MESG��õ��</option>\n], ( $SearchIcon == 11 )? ' selected="selected"' : '' );
	$selContents .= sprintf( qq[<option%s value="1011">��ľ�ܤ�$H_REPLY�� *�ʤ�* $H_MESG��õ��</option>\n], ( $SearchIcon == 1011 )? ' selected="selected"' : '' );

	$selContents .= qq(<option value="0">--------</option>\n);
	$selContents .= sprintf( qq[<option%s value="12">��$H_REPLY����ˤ���$H_MESG��õ��</option>\n], ( $SearchIcon == 12 )? ' selected="selected"' : '' );
	$selContents .= sprintf( qq[<option%s value="1012">��$H_REPLY����� *�ʤ�* $H_MESG��õ��</option>\n], ( $SearchIcon == 1012 )? ' selected="selected"' : '' );

	$selContents .= qq(<option value="0">--------</option>\n);
	$selContents .= sprintf( qq[<option%s value="13">��$H_REPLY����ü�ˤ���$H_MESG��õ��</option>\n], ( $SearchIcon == 13 )? ' selected="selected"' : '' );
	$selContents .= sprintf( qq[<option%s value="1013">��$H_REPLY����ü�� *�ʤ�* $H_MESG��õ��</option>\n], ( $SearchIcon == 1013 )? ' selected="selected"' : '' );

	$selContents .= qq(<option value="0">----------------</option>\n);
	$selContents .= sprintf( qq[<option%s value="21">��ľ�ܤ�$H_ORIG�Ǥ���$H_MESG��õ��</option>\n], ( $SearchIcon == 21 )? ' selected="selected"' : '' );
	$selContents .= sprintf( qq[<option%s value="1021">��ľ�ܤ�$H_ORIG�� *�ʤ�* $H_MESG��õ��</option>\n], ( $SearchIcon == 1021 )? ' selected="selected"' : '' );

	$selContents .= qq(<option value="0">--------</option>\n);
	$selContents .= sprintf( qq[<option%s value="22">��$H_ORIG����ˤ���$H_MESG��õ��</option>\n], ( $SearchIcon == 22 )? ' selected="selected"' : '' );
	$selContents .= sprintf( qq[<option%s value="1022">��$H_ORIG����� *�ʤ�* $H_MESG��õ��</option>\n], ( $SearchIcon == 1022 )? ' selected="selected"' : '' );

	$selContents .= qq(<option value="0">--------</option>\n);
	$selContents .= sprintf( qq[<option%s value="23">��$H_ORIG_TOP�ˤ���$H_MESG��õ��</option>\n], ( $SearchIcon == 23 )? ' selected="selected"' : '' );
	$selContents .= sprintf( qq[<option%s value="1023">��$H_ORIG_TOP�� *�ʤ�* $H_MESG��õ��</option>\n], ( $SearchIcon == 1023 )? ' selected="selected"' : '' );

	$contents .= &TagSelect( 'searchicon', $selContents );

	# �����������
	$contents .= ' (' . &LinkP( "b=$BOARD_ESC&c=i", "�Ȥ���$H_ICON����" .
	    &TagAccessKey( 'H' ), 'H' ) . ')';

#	$contents .= &TagInputCheck( 'searchicon', $SearchIcon ) . ': ' . &TagLabel( $H_ICON, 'searchicon', 'I' ) . " // \n";

    }
    $msg .= &TagFieldset( "�������$HTML_BR", $contents ) . $HTML_BR;

    $msg .= &TagLabel( '�������', 'key', 'K' ) . ': ' . &TagInputText(
	'text', 'key', $Key, $KEYWORD_LENGTH ) . $HTML_BR;

    %tags = ( 'c', 's', 'b', $BOARD );
    &DumpForm( *tags, '����', '�ꥻ�å�', *msg );
}

sub hg_b_all_icon
{
    return unless $BOARD;
    $gHgStr .= "<ul>\n";
    foreach ( @ICON_TITLE )
    {
	$gHgStr .= '<li>' . &TagMsgImg( $_ ) . " : [$_] " . ( $ICON_HELP{$_} ||
	    $_ ) . "</li>\n";
    }
    $gHgStr .= "</ul>\n";
}


###
## DumpBoardHeader - �Ǽ��ĥإå���ɽ��
#
# - SYNOPSIS
#	DumpBoardHeader();
#
# - DESCRIPTION
#	�Ǽ��ĤΥإå���ɽ�����롥
#
sub DumpBoardHeader
{
    local( $msg );
    &GetHeaderDb( $BOARD, *msg );
    
    LINE: while ( 1 )
    {
	if (( index( $msg, '<kb' ) >= 0 ) &&
	    ( $msg =~ s!<kb:(\w+)(\s*var="([^"]*)")?\s+/>!!o ))
	{
	    $gHgStr .= $`;
	    eval( '&hg_' . $1 . '( "' . $source . '", "' . $3 . '" );' );
	    &Fatal( 998, "$file : $@" ) if $@;
	    $msg = $';
	}
	else
	{
	    $gHgStr .= $msg;
	    last LINE;
	}
    }
}


###
## DumpArtEntry - ��å��������ϥե������ɽ��
#
# - SYNOPSIS
#	DumpArtEntry( $icon, $type, $id, $postDateStr, $title, $texttype, $article, $name, $eMail, $url, $fMail );
#
# - ARGS
#	$icon		��������
#	$type		��å�����������( 'supersede', and so )
#	$id		��ץ饤/��������å�����ID
#	$postDateStr	�ǥե�����������yyyy/mm/dd(HH:MM:SS)��
#	$title		�ǥե���ȥ����ȥ�ʥץ�ӥ塼��������ʤɤǻȤ���
#	$texttype	�ǥե���Ƚ񤭹��߷���
#	$article	�ǥե���ȥ�å�������ʸ
#	$name		�ǥե���ȥ桼��̾
#	$eMail		�ǥե���ȥᥤ�륢�ɥ쥹
#	$url		�ǥե����URL
#	$fMail		�ǥե���ȥᥤ���ۿ������å�
#
sub DumpArtEntry
{
    local( $icon ) = @_;

#    if ( $ICON_TYPE{ $icon } eq 'cfv' )
#    {
#	# TBD
#    }
#    elsif ( $ICON_TYPE{ $icon } eq 'vote' )
#    {
#	# TBD
#    }
#    else
#    {
	&DumpArtEntryNormal( @_ );
#    }
}


# �̾��å�����
sub DumpArtEntryNormal
{
    local( $icon, $type, $id, $postDateStr, $title, $texttype, $article, $name, $eMail, $url, $fMail ) = @_;

    $texttype = $texttype || $H_TTLABEL[ $SYS_TT_DEFAULT ];
    $icon = $icon || $SYS_ICON_DEFAULT;

    local( $msg );
    local( $contents ) = '';

    # �������������
    if ( $SYS_ICON )
    {
	$msg .= &TagLabel( $H_ICON, 'icon', 'I' ) . " :\n";
	$contents = sprintf( "<option%s>$H_NOICON</option>\n",
	    (( $icon eq $H_NOICON )? ' selected="selected"' : '' ));
	foreach ( @ICON_TITLE )
	{
	    $contents .= sprintf( "<option%s>$_</option>\n", ( $_ eq $icon )? ' selected="selected"' : '' );
	}
	$msg .= &TagSelect( 'icon', $contents ) . "\n";

	$msg .= '(' . &LinkP( "b=$BOARD_ESC&c=i", "�Ȥ���$H_ICON����" .
	    &TagAccessKey( 'H' ), 'H' ) . ')' . $HTML_BR;
    }

    $msg .= &TagLabel( $H_SUBJECT, 'subject', 'T' ) . ': ' .
	&TagInputText( 'text', 'subject', $title, $SUBJECT_LENGTH ) . $HTML_BR;
    
    local( $ttFlag ) = 0;
    local( $ttBit ) = 0;
    
    foreach ( @H_TTLABEL )
    {
	if (( $SYS_TEXTTYPE & ( 2 ** $ttBit )) && ( $SYS_TEXTTYPE ^ ( 2 ** $ttBit )))
	{
	    $ttFlag = 1;	# ��ǻȤ��������ʤ�������
	}
	$ttBit++;
    }

    # �񤭹��߷���
    if ( $ttFlag )
    {
	$ttBit = 0;
	local( $firstFlag ) = 1;
	local( $labelTarget );
	$contents = '';
	foreach ( @H_TTLABEL )
	{
	    if ( $SYS_TEXTTYPE & ( 2 ** $ttBit ))
	    {
		if ( $firstFlag )
		{
		    $firstFlag = 0;
		}
		else
		{
		    $contents .= '&nbsp;&nbsp;';
		}
		if ( $texttype eq $H_TTLABEL[$ttBit] )
		{
		    $contents .= &TagInputRadio( 'texttype_' . $ttBit, 'texttype', $H_TTLABEL[$ttBit], 1 );
		    $labelTarget = 'texttype_' . $ttBit;
		}
		else
		{
		    $contents .= &TagInputRadio( 'texttype_' . $ttBit, 'texttype', $H_TTLABEL[$ttBit], 0 );
		}
		$contents .= &TagLabel( $H_TTLABEL[$ttBit], 'texttype_' . $ttBit, '' );
	    }
	    $ttBit++;
	}
	$msg .= &TagFieldset( &TagLabel( $H_TEXTTYPE, $labelTarget, 'Z' ) . ': ', $contents );
    }
    else
    {
	$msg .= sprintf( qq(<input name="texttype" type="hidden" value="%s" />), $H_TTLABEL[(( log $SYS_TEXTTYPE ) / ( log 2 ))] ) . $HTML_BR;
    }

    $msg .= &TagLabel( $H_MESG, 'article', 'A' ) . ':' . $HTML_BR .
	&TagTextarea( 'article', $article, $TEXT_ROWS, $TEXT_COLS ) . $HTML_BR;

    if ( $POLICY & 8 )
    {
	# �������¤����̰���
	$msg .= &TagLabel( $H_DATE, 'postdate', 'T' ) . ': ' .
	    &TagInputText( 'text', 'postdate', $postDateStr, 20 ) .
	    qq[('yyyy/mm/dd(HH:MM:SS)'�η����ǻ���)] . $HTML_BR;
	$msg .= &TagLabel( $H_FROM, 'name', 'N' ) . ': ' .
	    &TagInputText( 'text', 'name', $name, $NAME_LENGTH ) . $HTML_BR;
	$msg .= &TagLabel( $H_MAIL, 'mail', 'M' ) . ': ' .
	    &TagInputText( 'text', 'mail', $eMail, $MAIL_LENGTH ) . $HTML_BR;
	$msg .= &TagLabel( $H_URL, 'url', 'U' ) . ': ' .
	    &TagInputText( 'text', 'url', ( $url || 'http://' ), $URL_LENGTH ) . $HTML_BR;
    }
    elsif ( $POLICY & 4 )
    {
	# ��Ͽ�Ѥߤξ�硤̾�����ᥤ�롤URL�����Ϥϡ�̵����
	$msg .= $H_FROM . ": $UNAME" . $HTML_BR;
	$msg .= $H_MAIL . ": $UMAIL" . $HTML_BR if ( $SYS_SHOWMAIL && $UMAIL );
	$msg .= $H_URL . ": $UURL" . $HTML_BR if $UURL;
    }
    else
    {
	$msg .= &TagLabel( $H_FROM, 'name', 'N' ) . ': ' .
	    &TagInputText( 'text', 'name', $name, $NAME_LENGTH ) . $HTML_BR;
	$msg .= &TagLabel( $H_MAIL, 'mail', 'M' ) . ': ' .
	    &TagInputText( 'text', 'mail', $eMail, $MAIL_LENGTH ) . $HTML_BR;
	$msg .= &TagLabel( $H_URL, 'url', 'U' ) . ': ' .
	    &TagInputText( 'text', 'url', ( $url || 'http://' ), $URL_LENGTH ) . $HTML_BR;
    }

    if ( $SYS_MAIL & 2 )
    {
	$msg .= &TagLabel( "��ץ饤�����ä�����$H_MAIL��Ϣ��", 'fmail', 'F'
	    ) . ': ' . &TagInputCheck( 'fmail', $fMail ) . "\n";
    }
    $msg .= "</p>\n<p>\n";

    $contents = &TagInputRadio( 'com_p', 'com', 'p', 1 ) . ":\n" . &TagLabel(
	'���ɽ�����Ƥߤ�(�ޤ���Ƥ��ޤ���)', 'com_p', 'P' ) . $HTML_BR;
    local( $doLabel );
    if ( $type eq 'supersede' )
    {
	$doLabel = '��������';
    }
    else
    {
	$doLabel = "$H_MESG����Ƥ���";
    }
    $contents .= &TagInputRadio( 'com_x', 'com', 'x', 0 ) . ":\n" . &TagLabel(
	$doLabel, 'com_x', 'X' ) . $HTML_BR;
    $msg .= &TagFieldset( "���ޥ��$HTML_BR", $contents );

    local( $op ) = ( -M &GetPath( $SYS_DIR, $BOARD_FILE ));
    local( %tags ) = ( 'corig', $cgi'TAGS{'c'}, 'b', $BOARD, 'c', 'p',
	'id', $id, 's', ( $type eq 'supersede' ), 'op', $op );

    &DumpForm( *tags, '�¹�', '', *msg );
}


###
## DumpArtBody - ��å��������Τ�ɽ��
#
# - SYNOPSIS
#	DumpArtBody( $Id, $CommandFlag, $OriginalFlag, @articleInfo );
#
# - ARGS
#	$Id			��å�����ID
#	$CommandFlag		���ޥ�ɤ�ɽ�����뤫�ݤ�(ɽ������=1)
#	$OriginalFlag		���ε�����ˡ�(�����)�������ؤΥ�󥯤�
#				ɽ�����뤫�ݤ�(ɽ������=1)
#	@articleInfo		$Id��''���ä����˻Ȥ����å���������
#
# - DESCRIPTION
#	��å�������ɽ�����롥$Id��''�Ǥʤ���С���å�����DB�����������
#	����򸵤�ɽ�����롥$Id��''�ξ�硤������@articleInfo���Ѥ��롥
#
sub DumpArtBody
{
    local( $id, $commandFlag, $origFlag, @articleInfo ) = @_;

    local( $fid, $aids, $date, $title, $icon, $host, $name, $eMail, $url );

    local( $body ) = '';
    if ( $id ne '' )
    {
	( $fid, $aids, $date, $title, $icon, $host, $name, $eMail, $url ) = &getMsgInfo( $id );
	local( @articleBody );
	&GetArticleBody( $id, $BOARD, *articleBody );
	$body = join( '', @articleBody );
    }
    else
    {
	( $fid, $aids, $date, $title, $icon, $host, $name, $eMail, $url, $body ) = @articleInfo;
    }

    # ̤��Ƶ������ɤ�ʤ�
    &Fatal( 8, '' ) if ( $title eq '' );

    $gHgStr .= qq(<div class="kbArticle">\n);

    # �����ȥ�
    &DumpArtTitle( $id, $title, $icon );

    local( $origId );
    if ( $fid ne '' )
    {
	( $origId = $fid ) =~ s/,.*$//o;
    }

    if ( $commandFlag && $SYS_COMMAND )
    {
	local( $num );
	foreach ( 0 .. &getNofMsg() )
	{
	    $num = $_, last if ( &getMsgId( $_ ) eq $id );
	}
	local( $prevId ) = &getMsgId( $num - 1 ) if ( $num > 0 );
	local( $nextId ) = &getMsgId( $num + 1 );
	&DumpArtCommand( $id, $origId, $prevId, $nextId, ( $aids ne '' ),
	    (( &IsUser( $name ) && (( $aids eq '' ) || ( $SYS_OVERWRITE == 2 ))) || ( $POLICY & 8 )));
    }

    # �إå��ʥ桼������ȥ�ץ饤��: �����ȥ�Ͻ�����
    &DumpArtHeader( $name, $eMail, $url, $host, $date, ( $origFlag? $origId : '' ));

    # �ڤ���
    $gHgStr .= $H_LINE;

#    if ( $ICON_TYPE{ $icon } eq 'cfv' )
#    {
#	# TBD
#    }
#    elsif ( $ICON_TYPE{ $icon } eq 'vote' )
#    {
#	# TBD
#    }
#    else
#    {
	&DumpArtBodyNormal( *body );
#    }

    $gHgStr .= "</div>\n";

    &cgiprint'Cache( $gHgStr ); $gHgStr = '';
}


# �̾��å�����
sub DumpArtBodyNormal
{
    local( *body ) = @_;
    $gHgStr .= qq(<div class="body">) . &ArticleEncode( *body ) . "</div>\n";
}


###
## DumpArtThread - �ե�������������ɽ����
#
# - SYNOPSIS
#	DumpArtThread( $State, $Head, @Tail );
#
# - ARGS
#	$State		ɽ������ե饰
#	    2^0 ... ����åɤ���Ƭ�Ǥ��뤫�ʢ����դ���
#	    2^1 ... Ʊ��ڡ���fragment��󥯤����Ѥ��뤫��#�����ֹ�ǥ�󥯡�
#	    2^2 ... �����ȥ��ɽ������(4), ������ʸ��ɽ������(0)
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
sub DumpArtThread
{
    local( $State, $Head, @Tail ) = @_;

    # �������פ����������Τ�Τ���
    if ( $State&4 )
    {
	if ( $Head eq '(' )
	{
	    $gHgStr .= "<ul>\n";
	}
	elsif ( $Head eq ')' )
        {
	    $gHgStr .= "</ul>\n";
	}
	else
	{
	    local( $dFid, $dAids, $dDate, $dSubject, $dIcon, $dRemoteHost, $dName ) = &getMsgInfo( $Head );
	    &DumpArtSummaryItem( $Head, $dAids, $dDate, $dSubject, $dIcon, $dName, $State&3 );
	    $gHgStr .= "</li>\n";
	    $State ^= 1 if ( $State&1 );
	}
    }
    elsif (( $Head ne '(' ) && ( $Head ne ')' ))
    {
	# ��������ɽ��(���ޥ���դ�, �������ʤ�)
	$gHgStr .= $HTML_HR;
	&DumpArtBody( $Head, $SYS_COMMAND_EACH, 0 );
    }

    # &cgiprint'Cache( $gHgStr ); $gHgStr = '';
    # tail recuresive.
    &DumpArtThread( $State, @Tail ) if @Tail;
}


###
## DumpSearchResult - ��������
#
# - SYNOPSIS
#	DumpSearchResult( $Key, $Subject, $Person, $Article, $PostTime, $PostTimeFrom, $PostTimeTo, $IconType, $Icon );
#
# - ARGS
#	$Key		�������
#	$Subject	�����ȥ�򸡺����뤫�ݤ�
#	$Person		��ƼԤ򸡺����뤫�ݤ�
#	$Article	��ʸ�򸡺����뤫�ݤ�
#	$PostTime	���դ򸡺����뤫�ݤ�
#	$PostTimeFrom	��������
#	$PostTimeTo	��λ����
#	$IconType	��������θ�����ˡ
#	$Icon		��������
#
# - DESCRIPTION
#	�����򸡺�����ɽ������
#
sub DumpSearchResult
{
    local( $Key, $Subject, $Person, $Article, $PostTime, $PostTimeFrom, $PostTimeTo, $IconType, $Icon ) = @_;

    local( @KeyList ) = split( /\s+/, $Key );

    # �ꥹ�ȳ���
    $gHgStr .= "<ul>\n";

    local( $dId, $dFid, $dAids, $dDate, $dTitle, $dIcon, $dRemoteHost, $dName, $dEmail );
    local( $SubjectFlag, $PersonFlag, $PostTimeFlag, $ArticleFlag );
    local( $HitNum, $Line, $FromUtc, $ToUtc );
    foreach ( $[ .. &getNofMsg() )
    {
	# ��������
	$dId = &getMsgId( $_ );
	( $dFid, $dAids, $dDate, $dTitle, $dIcon, $dRemoteHost, $dName, $dEmail ) = &getMsgInfo( $dId );

	# �ѿ��Υꥻ�å�
	$SubjectFlag = $PersonFlag = $PostTimeFlag = $ArticleFlag = 0;
	$Line = '';

	# ������������å�
	next unless &SearchArticleIcon( $dId, $Icon, $IconType );

	# ��ƻ���򸡺�
	if ( $PostTime )
	{
	    $FromUtc = $ToUtc = -1;
	    $FromUtc = &GetUtcFromYYYY_MM_DD( $PostTimeFrom )
		if $PostTimeFrom;
	    $ToUtc = &GetUtcFromYYYY_MM_DD( $PostTimeTo )
		if $PostTimeTo;
	    $ToUtc += 86400 if ( $ToUtc >= 0 );
	    next if !&CheckSearchTime( $dDate, $FromUtc, $ToUtc );
	}

	if ( $Key ne '' )
	{
	    # �����ȥ�򸡺�
	    if ( $Subject && ( $dTitle ne '' ))
	    {
		$SubjectFlag = 1;
		foreach ( @KeyList )
		{
		    $SubjectFlag = 0 if ( $dTitle !~ /$_/i );
		}
	    }

	    # ��Ƽ�̾�򸡺�
	    if ( $Person && !$SubjectFlag && ( $dName ne '' ))
	    {
		$PersonFlag = 1;
		foreach ( @KeyList )
		{
		    if (( $dName !~ /$_/i ) && ( $dEmail !~ /$_/i ))
		    {
			$PersonFlag = 0;
		    }
		}
	    }

	    # ��ʸ�򸡺�
	    if ( $Article && !$SubjectFlag && !$PersonFlag )
	    {
		if ( $Line = &SearchArticleKeyword( $dId, $BOARD, @KeyList ))
		{
		    $ArticleFlag = 1;
		}
	    }
	}
	else
	{
	    # ̵���ǰ���
	    $SubjectFlag = 1;
	}

	if ( $SubjectFlag || $PersonFlag || $ArticleFlag )
	{
	    # ����1�ĤϹ��פ���
	    $HitNum++;

	    # �����ؤΥ�󥯤�ɽ��
	    &DumpArtSummaryItem( $dId, $dAids, $dDate, $dTitle, $dIcon, $dName, 1 );

	    # ��ʸ�˹��פ���������ʸ��ɽ��
	    if ( $ArticleFlag )
	    {
		$Line =~ s/<[^>]*>//go;
		$gHgStr .= "<blockquote>$Line</blockquote>\n";
	    }
	    $gHgStr .= "</li>\n";
	}
    }

    # �ҥåȤ�����
    if ( $HitNum )
    {
	$gHgStr .= "</ul>\n<ul>\n";
	$gHgStr .= "<li>$HitNum���$H_MESG�����Ĥ���ޤ�����</li>\n";
    }
    else
    {
	$gHgStr .= "<li>��������$H_MESG�ϸ��Ĥ���ޤ���Ǥ�����</li>\n";
    }

    # �ꥹ���Ĥ���
    $gHgStr .= "</ul>\n";
}


###
## DumpOriginalArticles - ���ꥸ�ʥ뵭���ؤΥ�󥯤�ɽ��
#
# - SYNOPSIS
#	DumpOriginalArticles( $fids );
#
# - ARGS
#	$fids	���ꥸ�ʥ뵭��ID�ǡ���
#
# - DESCRIPTION
#	���ꥸ�ʥ뵭���ؤΥ�󥯤�ɽ�����롥
#
sub DumpOriginalArticles
{
    if ( $_[0] ne '' )
    {
	# ���ꥸ�ʥ뵭��������ʤ��

	$gHgStr .= "<ul>\n";

	local( $dId, $dFid, $dAids, $dDate, $dTitle, $dIcon, $dHost, $dName );
	foreach $dId ( reverse( split( /,/, $_[0] )))
	{
	    ( $dFid, $dAids, $dDate, $dTitle, $dIcon, $dHost, $dName ) = &getMsgInfo( $dId );
	    &DumpArtSummaryItem( $dId, $dAids, $dDate, $dTitle, $dIcon, $dName, 0 );
	}
	$gHgStr .= "</ul>\n";
    }
    else
    {
	# �ʤˤ�ɽ�����ʤ���
    }
}


###
## DumpReplyArticles - ��ץ饤�����ؤΥ�󥯤�ɽ��
#
# - SYNOPSIS
#	DumpReplyArticles( $aids );
#
# - ARGS
#	$aids	��ץ饤����ID�ǡ���
#
# - DESCRIPTION
#	��ץ饤�����ؤΥ�󥯤�ɽ�����롥
#
sub DumpReplyArticles
{
    if ( $_[0] ne '' )
    {
	# ȿ������������ʤ��

	local( $id, @tree );
	foreach $id ( split( /,/, $_[0] ))
	{
	    # �ե����������ڹ�¤�μ���
	    # ex. '( a ( b ( c d ) ) ( e ) ( f ( g ) ) )'�Ȥ����ꥹ��
	    @tree = ();
	    &GetFollowIdTree( $id, *tree );
	    
	    # �ᥤ��ؿ��θƤӽФ�(��������)
	    &DumpArtThread( 4, @tree );
	}
    }
    else
    {
	# ȿ������̵��

	$gHgStr .= "<ul>\n<li>���ߡ�����$H_MESG�ؤ�$H_REPLY�Ϥ���ޤ���</li>\n</ul>\n";
    }
}


###
## DumpArtTitle - ���������ȥ��ɽ��
#
# - SYNOPSIS
#	DumpArtTitle( $id, $title, $icon );
#
# - ARGS
#	$id	����ID
#	$title	�����ȥ�
#	$icon	��������
#
sub DumpArtTitle
{
    local( $id, $title, $icon ) = @_;
    local( $markUp );
    $markUp .= "$id. " if ( $id ne '' );
    $markUp .= &TagMsgImg( $icon ) . $title;
    $gHgStr .= '<h2>' . &TagA( $markUp, '', '', '', "a$id" ) . "</h2>\n";
}


###
## DumpArtCommand - �������ޥ�ɤ�ɽ��
#
# - SYNOPSIS
#	DumpArtCommand( $id, $upId, $prevId, $nextId, $reply, $delete );
#
# - ARGS
#	$id	����ID
#	$upId	�嵭��ID
#	$prevId	������ID
#	$nextId	������ID
#	$reply	��ץ饤���������뤫
#	$delete	�������������ǽ��
#
sub DumpArtCommand
{
    local( $id, $upId, $prevId, $nextId, $reply, $delete ) = @_;

    $gHgStr .= qq(<p class="command">\n);

    local( $dlmtS, $dlmtL );
    if ( $SYS_COMICON == 1 )
    {
	$dlmtS = '';
	$dlmtL = ' // ';
    }
    elsif ( $SYS_COMICON == 2 )
    {
	$dlmtS = ' | ';
	$dlmtL = '';
    }
    else
    {
	$dlmtS = ' | ';
	$dlmtL = '';
    }

    if ( $upId ne '' )
    {
	$gHgStr .= &LinkP( "b=$BOARD_ESC&c=e&id=$upId", &TagComImg( $ICON_UP, $H_UPARTICLE ), 'U' ) . "\n";
    }
    else
    {
	$gHgStr .= &TagComImg( $ICON_UP_X, $H_UPARTICLE, ) . "\n";
    }
	
    if ( $prevId ne '' )
    {
	$gHgStr .= $dlmtS . &LinkP( "b=$BOARD_ESC&c=e&id=$prevId", &TagComImg(
	    $ICON_PREV, $H_PREVARTICLE ), 'P' ) . "\n";
    }
    else
    {
	$gHgStr .= $dlmtS . &TagComImg( $ICON_PREV_X, $H_PREVARTICLE, ) . "\n";
    }
	
    if ( $nextId ne '' )
    {
	$gHgStr .= $dlmtS . &LinkP( "b=$BOARD_ESC&c=e&id=$nextId", &TagComImg(
	    $ICON_NEXT, $H_NEXTARTICLE ), 'N' ) . "\n";
    }
    else
    {
	$gHgStr .= $dlmtS . &TagComImg( $ICON_NEXT_X, $H_NEXTARTICLE, ) . "\n";
    }

    if ( $reply )
    {
	$gHgStr .= $dlmtS . &LinkP( "b=$BOARD_ESC&c=t&id=$id", &TagComImg(
	    $ICON_DOWN, $H_READREPLYALL ), 'M' ) . "\n";
    }
    else
    {
	$gHgStr .= $dlmtS . &TagComImg( $ICON_DOWN_X, $H_READREPLYALL ) . "\n";
    }

    $gHgStr .= $dlmtL;

    if ( $POLICY & 2 )
    {
	$gHgStr .= $dlmtS . &LinkP( "b=$BOARD_ESC&c=f&id=$id",
	    &TagComImg( $ICON_FOLLOW, $H_REPLYTHISARTICLE ), 'R' ) . "\n" .
	    $dlmtS . &LinkP( "b=$BOARD_ESC&c=q&id=$id",
	    &TagComImg( $ICON_QUOTE, $H_REPLYTHISARTICLEQUOTE ), 'Q' ) . "\n";
    }
    else
    {
	$gHgStr .= $dlmtS . &TagComImg( $ICON_FOLLOW_X, $H_REPLYTHISARTICLE ) .
	    "\n" . $dlmtS . &TagComImg( $ICON_QUOTE_X, $H_REPLYTHISARTICLEQUOTE ) . "\n";
    }

    if ( $SYS_AUTH )
    {
	$gHgStr .= $dlmtL;

	if ( $delete )
	{
	    $gHgStr .= $dlmtS . &LinkP( "b=$BOARD_ESC&c=f&s=on&id=$id",
		&TagComImg( $ICON_SUPERSEDE, $H_SUPERSEDE ), 'S' ) . "\n" .
		$dlmtS . &LinkP( "b=$BOARD&c=dp&id=$id",
		&TagComImg( $ICON_DELETE, $H_DELETE ), 'D' ) . "\n";
	}
	else
	{
	    $gHgStr .= $dlmtS . &TagComImg( $ICON_SUPERSEDE_X, $H_SUPERSEDE ) .
	    	"\n" . $dlmtS . &TagComImg( $ICON_DELETE_X, $H_DELETE ) . "\n";
	}
    }

    if ( $SYS_COMICON == 1 )
    {
	$gHgStr .= $dlmtL;
	$gHgStr .= $dlmtS . &LinkP( "b=$BOARD_ESC&c=h", &TagComImg( $ICON_HELP,
	    '�إ��' ), 'H', '', '', 'list' ) . "\n";
    }
    $gHgStr .= qq(</p>\n);
}


###
## DumpArtHeader - �����إå��ʥ����ȥ�����ˤ�ɽ��
#
# - SYNOPSIS
#	DumpArtHeader( $name, $eMail, $url, $host, $date, $origId );
#
# - ARGS
#	$name		�桼��̾
#	$eMail		�ᥤ�륢�ɥ쥹
#	$url		URL
#	$host		Remote Host̾
#	$date		���ա�UTC��
#	$origId		��ץ饤������ID
#
sub DumpArtHeader
{
    local( $name, $eMail, $url, $host, $date, $origId ) = @_;

    $gHgStr .= qq(<p class="header">\n);

    # ��̾��
    if ( $url eq '' )
    {
	$gHgStr .= "<strong>$H_FROM</strong>: $name";
    }
    else
    {
	$gHgStr .= "<strong>$H_FROM</strong>: " . &TagA( $name, $url );
    }

    # �ᥤ��
    if ( $SYS_SHOWMAIL && $eMail )
    {
	$gHgStr .= ' ' . &TagA( "&lt;$eMail&gt;", "mailto:$eMail" );
    }
    $gHgStr .= $HTML_BR;

    # �ޥ���
    $gHgStr .= "<strong>$H_HOST</strong>: $host" . $HTML_BR if $SYS_SHOWHOST;

    # �����
    $gHgStr .= "<strong>$H_DATE</strong>: " . &GetDateTimeFormatFromUtc( $date ) . $HTML_BR;

    # ��ץ饤���ؤΥ��
    if ( $origId )
    {
	( $dFid, $dAids, $dDate, $dTitle, $dIcon, $dHost, $dName ) = &getMsgInfo( $origId );
	$gHgStr .= "<strong>$H_ORIG:</strong> ";
	&DumpArtSummary( $origId, $dAids, $dDate, $dTitle, $dIcon, $dName, 0 );
	$gHgStr .= $HTML_BR;
    }

    # �ڤ���
    $gHgStr .= "</p>\n";
}


###
## DumpButtonToTitleList - �����ȥ�����ܥ����ɽ��
#
# - SYNOPSIS
#	DumpButtonToTitleList($Board);
#
# - ARGS
#	$Board		�Ǽ���ID
#
# - DESCRIPTION
#	�����ȥ�����إ����פ��뤿��Υܥ����ɽ������
#
sub DumpButtonToTitleList
{
    local( $board, $id ) = @_;
    local( $old ) = $id? &GetTitleOldIndex( $id ) : 0;

    if  ( $SYS_COMMAND_BUTTON )
    {
	local( %tags ) = ( 'b', $board, 'c', 'v', 'num', $DEF_TITLE_NUM, 'old',
	    $old );
	&DumpForm( *tags, "$H_BACKTITLEREPLY(B)", '', '' );

	%tags = ( 'b', $board, 'c', 'r', 'num', $DEF_TITLE_NUM, 'old', $old );
	&DumpForm( *tags, $H_BACKTITLEDATE, '', '' );
    }
    else
    {
	local( $boardEsc ) = &URIEscape( $board );
	$gHgStr .= "<p>" . &LinkP( "b=$boardEsc&c=v&num=$DEF_TITLE_NUM&old=$old", $H_BACKTITLEREPLY . &TagAccessKey( 'B' ), 'B' ) . "</p>\n";
	$gHgStr .= "<p>" . &LinkP( "b=$boardEsc&c=r&num=$DEF_TITLE_NUM&old=$old", $H_BACKTITLEDATE ) .
	    "</p>\n";
    }
}


###
## DumpButtonToArticle - ��å������إ����פ���ܥ����ɽ��
#
# - SYNOPSIS
#	DumpButtonToArticle( $board, $id, $msg );
#
# - ARGS
#	$board	�Ǽ���ID
#	$id	��å�����ID
#	$msg	���ʸ����
#
# - DESCRIPTION
#	��å������إ����פ��뤿��Υܥ����ɽ������
#
sub DumpButtonToArticle
{
    local( $board, $id, $msg ) = @_;

    if  ( $SYS_COMMAND_BUTTON )
    {
	local( %tags ) = ( 'b', $board, 'c', 'e', 'id', $id );
	&DumpForm( *tags, "$msg(N)", '', '' );
    }
    else
    {
	local( $boardEsc ) = &URIEscape( $board );
	$gHgStr .= "<p>" . &LinkP( "b=$boardEsc&c=e&id=$id", $msg .
	    &TagAccessKey( 'N' ), 'N' ) . "</p>\n";
    }
}


###
## DumpForm - �ե����ॿ���Υե����ޥå�
#
# - SYNOPSIS
#	DumpForm( *hiddenTags, $submit, $reset, *contents );
#
# - ARGS
#	*tags		�ɲä���hidden��������᤿Ϣ������
#	*submit		submit�ܥ���ʸ����
#	*reset		reset�ܥ���ʸ����
#	*contents	</form>�����ޤǤ���������ʸ����
#	$noAuth		ǧ���Ѿ��������ʤ�����Υե饰	
#
# - DESCRIPTION
#	Form�����Υե����ޥå�
#
sub DumpForm
{
    local( *tags, $submit, $reset, *contents, $noAuth ) = @_;

    $gHgStr .= qq(<form action="$PROGRAM" method="POST">\n);

    $gHgStr .= "<p>\n";
    foreach ( keys( %tags ))
    {
	$gHgStr .= qq(<input name="$_" type="hidden" value="$tags{$_}" />\n);
    }
    if ( !$noAuth && ( $SYS_AUTH == 3 ))
    {
	$gHgStr .= qq(<input name="kinoU" type="hidden" value="$UNAME" />\n);
	$gHgStr .= qq(<input name="kinoP" type="hidden" value="$PASSWD" />\n);
	$gHgStr .= qq(<input name="kinoA" type="hidden" value="3" />\n);
    }
    local( $accessKey );
    if ( $submit =~ /\((\w)\)$/o )
    {
	$accessKey = $1;
    }
    else
    {
	$submit .= "(G)";
	$accessKey = 'G';
    }
    $gHgStr .= "$contents\n" . &TagInputSubmit( 'submit', $submit, $accessKey );
    if ( $reset )
    {
	if ( $reset =~ /\((\w)\)$/o )
	{
	    $accessKey = $1;
	}
	else
	{
	    $reset .= "(R)";
	    $accessKey = 'R';
	}
	$accessKey = 'R';
	$gHgStr .= ' ' . &TagInputSubmit( 'reset', $reset, $accessKey ) . "\n";
    }
    $gHgStr .= "</p>\n</form>\n";
}


###
## DumpArtSummary - �����ȥ�ꥹ�ȤΥե����ޥå�
#
# - SYNOPSIS
#	DumpArtSummary( $id, $aids, $date, $subject, $icon, $name, $flag);
#
# - ARGS
#	$id		����ID
#	$aids		��ץ饤���������뤫�ݤ�
#	$date		�������������(UTC)
#			  ��ά����0�ʤɡˤ�ɽ������ʤ���
#	$subject	������Subject
#	$icon		������������ID
#	$name		��������Ƽ�̾
#	$flag		ɽ���������ޥ����ե饰
#	    2^0 ... ����åɤ���Ƭ�Ǥ��뤫�ʢ����դ���
#	    2^1 ... Ʊ��ڡ���fragment��󥯤����Ѥ��뤫��#�����ֹ�ǥ�󥯡�
#
# - DESCRIPTION
#	���뵭���򥿥��ȥ�ꥹ��ɽ���Ѥ˥ե����ޥåȤ��롥
#
sub DumpArtSummary
{
    local( $id, $aids, $date, $subject, $icon, $name, $flag ) = @_;

    $subject = $subject || $id;
    $name = $name || $MAINT_NAME;

    $gHgStr .= qq(<span class="kbTitle">);	# �����

    if ( $flag&1 && ( &getMsgParents( $id ) ne '' ))
    {
	local( $fId );
	( $fId = &getMsgParents( $id )) =~ s/^.*,//o;
	$gHgStr .= ' ' . &LinkP( "b=$BOARD_ESC&c=t&id=$fId", $H_THREAD_ALL, '',
	    $H_THREAD_ALL_L ) . ' ';
    }

    $gHgStr .= &TagMsgImg( $icon ) . " <small>$id.</small> " .
	(( $flag&2 )? &TagA( $subject, "$cgi'REQUEST_URI#a$id" ) :
	&LinkP( "b=$BOARD_ESC&c=e&id=$id", $subject ));

    if ( $aids )
    {
	$gHgStr .= ' ' . &LinkP( "b=$BOARD_ESC&c=t&id=$id", $H_THREAD, '',
	    $H_THREAD_L );
    }

    $gHgStr .= " [$name] ";
    $gHgStr .= &GetDateTimeFormatFromUtc( $date ) if $date;

    $gHgStr .= ' ' . &TagMsgImg( $H_NEWARTICLE ) if &getMsgNewP( $id );
    $gHgStr .= "</span>\n";
}


###
## DumpArtSummaryItem - �����ȥ�ꥹ�ȤΥե����ޥåȡ�<li>�Ĥ���
#
# - SYNOPSIS
#	DumpArtSummaryItem(Ʊ��);
#
# - ARGS
#	Ʊ��
#
# - DESCRIPTION
#	���뵭���򥿥��ȥ�ꥹ��ɽ���Ѥ˥ե����ޥåȤ��롥<li>�Ĥ�
#
sub DumpArtSummaryItem
{
    $gHgStr .= '<li>';
    &DumpArtSummary;
}


###
## htmlGen - HTML generator from source file
#
# - SYNOPSIS
#	htmlGen( $source );
#
# - ARGS
#	$source		const val.	filename of HTML source in UI dir.
#
# - DESCRIPTION
#	generate HTML output from source file named $source.
#	for each `<kb:foobar>' LINE in the source file,
#	the function `foobar' was called.
#
# - RETURN
#	1 if succeed, 0 if failed.
#
sub htmlGen
{
    local( $source ) = @_;

    local( $file ) = &GetPath( $UI_DIR, $source );

    open( SRC, "<$file" ) || &Fatal( 1, $file );

    if ( $SYS_COOKIE_EXPIRE == 1 )
    {
	$cookieExpire = 'Thursday, 31-Dec-2029 23:59:59 GMT';
    }
    elsif ( $SYS_COOKIE_EXPIRE == 2 )
    {
	# 86400 = 24 * 60 * 60
	$cookieExpire = $^T + ( $SYS_COOKIE_VALUE * 86400 );
    }
    elsif ( $SYS_COOKIE_EXPIRE == 3 )
    {
	$cookieExpire = $SYS_COOKIE_VALUE;
    }
    else
    {
	$cookieExpire = '';
    }
    &cgiauth'Header( 0, 0, 1, $cookieExpire );
    &cgiprint'Init();

    $gHgStr = '';

    # Work around for MSIE 4.5(Macintosh IE).
    #   cf. <URL:http://kanzaki.com/docs//html/xhtml1.html>
    if ( $ENV{'HTTP_USER_AGENT'} =~ /MSIE 4.5/o )
    {
	$gHgStr .= "<!-- dummy comment -->\n";
    }

    while( <SRC> )
    {
	LINE: while ( 1 )
	{
	    if (( index( $_, '<kb' ) >= 0 ) &&
		( s!<kb:(\w+)(\s*var="([^"]*)")?\s+/>!!o ))
	    {
		$gHgStr .= $`;
		eval( '&hg_' . $1 . '( "' . $source . '", "' . $3 . '" );' );
		if ( $@ )
		{
		    if ( $source != $file )
		    {
			&Fatal( 998, "$file : $@" );
		    }
		    else
		    {
			print "Error -- $file : $@\n";
		    }
		}
		$_ = $';
	    }
	    else
	    {
		$gHgStr .= $_;
		last LINE;
	    }
	}
    }
    &cgiprint'Cache( $gHgStr );

    &cgiprint'Flush();
}


######################################################################
# ���å�����ץ���ơ������


###
## ArriveMail - ���������夷�����Ȥ�ᥤ��
#
# - SYNOPSIS
#	ArriveMail( $Name, $Email, $Subject, $Icon, $Id, @To );
#
# - ARGS
#	$Name		����������Ƽ�̾
#	$Email		����������Ƽԥᥤ�륢�ɥ쥹
#	$Date		����������ƻ���
#	$Subject	��������Subject
#	$Icon		����������������
#	$Id		��������ID
#	@To		������E-Mail addr�ꥹ��
#
# - DESCRIPTION
#	���������夷�����Ȥ�ᥤ�뤹�롥
#
# - RETURN
#	�ʤ�
#
sub ArriveMail
{
    local( $Name, $Email, $Date, $Subject, $Icon, $Id, @To ) = @_;

    local( $StrSubject, $MailSubject, $StrFrom, $Message );
    $StrSubject = ( !$SYS_ICON || ( $Icon eq $H_NOICON ))? $Subject :
	"($Icon) $Subject";
    $StrSubject =~ s/<[^>]*>//go;	# �������פ�ʤ�
    $StrSubject = &HTMLDecode( $StrSubject );
    $MailSubject = &GetMailSubjectPrefix( $BOARDNAME, $Id ) . $StrSubject;
    $StrFrom = $Email? "$Name <$Email>" : "$Name";

    $Message = <<__EOF__;
$SYSTEM_NAME����Τ��Τ餻�Ǥ���
$H_BOARD��$BOARDNAME�פ��Ф��ƽ񤭹��ߤ�����ޤ�����

����$H_MESG:
  �� $SCRIPT_URL?b=$BOARD&c=e&id=$Id

__EOF__

    $Message .= &GetArticlePlainText( $Id, $Name, $Email, $Subject, $Icon,
	$Date );

    # �ᥤ������
    &SendArticleMail( $Name, $Email, $MailSubject, $Message, $Id, @To );
}


###
## FollowMail - ȿ�������ä����Ȥ�ᥤ��
#
# - SYNOPSIS
#	FollowMail( $Name, $Email, $Date, $Subject, $Icon, $Id, $Fname, $Femail, $Fsubject, $Ficon, $Fid, @To );
#
# - ARGS
#	$Name		����������Ƽ�̾
#	$Email		����������Ƽԥᥤ�륢�ɥ쥹
#	$Date		��ץ饤���줿�����ν񤭹��߻���
#	$Subject	��������Subject
#	$Icon		����������������
#	$Id		��������ID
#	$Fname		��ץ饤���줿��������Ƽ�̾
#	$Femail		��ץ饤���줿��������Ƽԥᥤ�륢�ɥ쥹
#	$Fsubject	��ץ饤���줿������Subject
#	$Ficon		��ץ饤���줿�����Υ�������
#	$Fid		��ץ饤���줿����ID
#	@To		������E-Mail addr�ꥹ��
#
# - DESCRIPTION
#	��ץ饤�����ä����Ȥ�ᥤ�뤹�롥
#
# - RETURN
#	�ʤ�
#
sub FollowMail
{
    local( $Name, $Email, $Date, $Subject, $Icon, $Id, $Fname, $Femail, $Fdate, $Fsubject, $Ficon, $Fid, @To ) = @_;
    
    local( $StrSubject, $FstrSubject, $MailSubject, $StrFrom, $Message );

    $StrSubject = ( !$SYS_ICON || ( $Icon eq $H_NOICON ))? "$Subject" :
	"($Icon) $Subject";
    $StrSubject =~ s/<[^>]*>//go;	# �������פ�ʤ�
    $StrSubject = &HTMLDecode( $StrSubject );
    $FstrSubject = ( $Ficon eq $H_NOICON )? $Fsubject : "($Ficon) $Fsubject";
    $FstrSubject =~ s/<[^>]*>//go;	# �������פ�ʤ�
    $FstrSubject = &HTMLDecode( $FstrSubject );
    $MailSubject = &GetMailSubjectPrefix( $BOARDNAME, $Fid ) . $FstrSubject;
    $StrFrom = $Email? "$Name <$Email>" : "$Name";

    local( $topId );
    ( $topId = &getMsgParents( $Id )) =~ m/([^,]+)$/o;

    $Message = <<__EOF__;
$SYSTEM_NAME����Τ��Τ餻�Ǥ���

$H_BOARD��$BOARDNAME�פ�
��$StrFrom�פ��󤬽񤤤�
��$StrSubject�פ�
$H_REPLY������ޤ�����

����$H_MESG:
  �� $SCRIPT_URL?b=$BOARD&c=e&id=$Fid
$H_ORIG_TOP����ޤȤ��ɤ�:
  �� $SCRIPT_URL?b=$BOARD&c=t&id=$topId

__EOF__

    $Message .= &GetArticlePlainText( $Fid, $Fname, $Femail, $Fsubject, $Ficon,
	$Fdate );

    # �ᥤ������
    &SendArticleMail( $Fname, $Femail, $MailSubject, $Message, $Fid, @To );
}


###
## GetArticlePlainText - ��å�������plain text�Ǽ���
#
# - SYNOPSIS
#	GetArticlePlainText(
#	    $id,	��å�����ID
#	    $name,	��Ƽ�̾
#	    $mail,	��Ƽԥᥤ�륢�ɥ쥹
#	    $subject,	�����ȥ�
#	    $icon,	��������
#	    $date	����(UTC)
#	)
#
# - DESCRIPTION
#	�ᥤ�������Ѥˡ���å�������plain text�Ǽ������롥
#
# - RETURN
#	ʸ����
#
sub GetArticlePlainText
{
    local( $id, $name, $mail, $subject, $icon, $date ) = @_;

    local( $strSubject ) = ( !$SYS_ICON || ( $icon eq $H_NOICON ))? $subject :
	"($icon) $subject";
    $strSubject =~ s/<[^>]*>//go;	# �������פ�ʤ�
    $strSubject = &HTMLDecode( $strSubject );
    local( $strFrom ) = $mail? "$name <$mail>" : $name;
    local( $strDate ) = &GetDateTimeFormatFromUtc( $date );

    local( @body );
    &GetArticleBody( $id, $BOARD, *body );

    $msg = <<__EOF__;
$H_SUBJECT: $strSubject
$H_FROM: $strFrom
$H_DATE: $strDate

--------------------

__EOF__

    local( $str );
    foreach ( @body )
    {
	s/<[^>]*>//go;
	$str .= &HTMLDecode( $_ );
    }

    # ��Ƭ�������β��Ԥ��ڤ����Ф���
    $str =~ s/^\n*//o;
    $str =~ s/\n*$//o;

    $msg . $str;
}


###
## MakeNewArticle, MakeNewArticleEx - ��������Ƥ��줿����������
#
# - SYNOPSIS
#	MakeNewArticleEx( $Board, $Id, $artKey, $postDate, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail, $MailRelay );
#	MakeNewArticle( $Board, $Id, $artKey, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail, $MailRelay );
#
# - ARGS
#	$Board		�������뵭��������Ǽ��Ĥ�ID
#	$Id		��ץ饤��������ID
#	$artKey		¿�Ž񤭹����ɻ��ѥ���
#	$postDate	��ƻ����UTC����ηв��ÿ���
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
#	&MakeNewArticle�ˤ�$postDate�������ʤ���
#	�����R7�ʸ�ˤ϶���&MakeNewArticleEx������Ȥ��褦�ˡ�
#
sub MakeNewArticle
{
    local( $Board, $Id, $artKey, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail, $MailRelay ) = @_;
    &MakeNewArticleEx( $Board, $Id, $artKey, $^T, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail, $MailRelay );
}

sub MakeNewArticleEx
{
    local( $Board, $Id, $artKey, $postDate, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail, $MailRelay ) = @_;

    local( $ArticleId );
    &CheckArticle( $Board, *postDate, *Name, *Email, *Url, *Subject, *Icon, *Article );

    # �����������ֹ�����(�ޤ������ֹ�������Ƥʤ�)
    $ArticleId = &GetNewArticleId( $Board );

    # �����Υե�����κ���
    &MakeArticleFile( $TextType, $Article, $ArticleId, $Board );

    # �����������ֹ��񤭹���
    &WriteArticleId( $ArticleId, $Board, $artKey );

    # DB�ե��������Ƥ��줿�������ɲ�
    # �̾�ε������Ѥʤ�ID
    &AddDBFile( $ArticleId, $Board, $Id, $postDate, $Subject, $Icon, ( $SYS_LOGHOST? $REMOTE_INFO : '' ), $Name, $Email, $Url, $Fmail, $MailRelay );

    $ArticleId;
}


###
## SearchArticleIcon - �����θ���(��������)
#
# - SYNOPSIS
#	SearchArticleIcon( $id, $icon, $type );
#
# - ARGS
#	$id		��������򸡺����뵭����ID
#	$icon		�������륢������
#	$type		����������
#			  1 ... �ܿ�
#			  11 ... ľ�ܤ�̼�ˤ���
#			  12 ... ̼��¹���Ĥ�Ǥ�դˤ���
#			  13 ... �꡼�դ�̼�ˤ���
#			  21 ... ľ�ܤοƤˤ���
#			  22 ... �ơ����οơ��Ĥ�Ǥ�դˤ���
#			  23 ... �����οƤˤ���
#			  1011 ... ľ�ܤ�̼�ˤʤ�
#			  1012 ... ̼��¹���Ĥ�Ǥ�դˤʤ�
#			  1013 ... �꡼�դ�̼�ˤʤ�
#			  1021 ... ľ�ܤοƤˤʤ�
#			  1022 ... �ơ����οơ��Ĥ�Ǥ�դˤʤ�
#			  1023 ... �����οƤˤʤ�
#
# - DESCRIPTION
#	���ꤵ�줿�����Υ�������򸡺����롥
#
# - RETURN
#	1 if match, 0 if not.
#
sub SearchArticleIcon
{
    local( $id, $icon, $type ) = @_;

    local( $not ) = 0;
    if ( $type > 1000 )
    {
	$type -= 1000;
	$not = 1;
    }

    # 0�ϸ����ߴ����Τ��ᡥ'on'���Ϥ���뤫�⤷��ʤ���
    local( $result );
    if (( $type == 1 ) || ( $type == 0 ))
    {
	$result = 1 if ( &getMsgIcon( $id ) eq $icon );
    }
    elsif (( $type == 11 ) || ( $type == 12 ) || ( $type == 13 ))
    {
	local( @daughters ) = split( /,/, &getMsgDaughters( $id ));
	$result = $not unless @daughters;
	local( $dId );
	while ( $dId = shift( @daughters ))
	{
	    if ( &getMsgIcon( $dId ) eq $icon )
	    {
		$result = 1 if (( $type == 11 ) || ( $type == 12 ));
		$result = 1 if (( $type == 13 ) && ( &getMsgDaughters( $dId ) eq '' ));
	    }
	    if ( $type != 11 )
	    {
		# Search recursively...
		push( @daughters, split( /,/, &getMsgDaughters( $dId )));
	    }
	}
	return $not - $result;
    }
    elsif (( $type == 21 ) || ( $type == 22 ) || ( $type == 23 ))
    {
	local( @parents ) = split( /,/, &getMsgParents( $id ));
	$result = $not unless @daughters;
	local( $dId );
	while ( $dId = shift( @parents ))
	{
	    if ( &getMsgIcon( $dId ) eq $icon )
	    {
		$result = 1 if (( $type == 21 ) || ( $type == 22 ));
		$result = 1 if (( $type == 23 ) && ( $#parents == -1 ));
	    }
	    last if ( $type == 21 );
	}
    }
    
    return $not - $result;
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
	@KeyList = @NewKeyList;
	last unless @KeyList;
    }

    # �ޤ��ĤäƤ��饢���ȡ����ʤ�ǽ�Υޥå������Ԥ��֤���
    @KeyList ? '' : $Return;
}


###
## CheckSearchTime - �������դΥ����å�
#
# - SYNOPSIS
#	CheckSearchTime( $target, $from, $to );
#
# - ARGS
#	$target		Ƚ���о�
#	$from		�ϰϳ�������
#	$to		�ϰϽ�λ����
#
# - DESCRIPTION
#	���������κݡ����դδ���Ƚ�Ǥ�Ԥʤ���
# 
# - RETURN
#	true if on time.
#
sub CheckSearchTime
{
    local( $target, $from, $to ) = @_;

    return 0 if (( $from >= 0 ) && ( $target < $from ));
    return 0 if (( $to >= 0 ) && ( $target > $to ));
    1;
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
sub DeleteArticle
{
    local( $Id, $Board, $ThreadFlag ) = @_;

    local( $Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $dId, @Target, $TargetId, $parents );

    # ��������μ���
    ( $Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url ) = &getMsgInfo( $Id );

    # �ǡ����ν񤭴���(ɬ�פʤ�̼��)
    @Target = ( $Id );
    foreach $TargetId ( @Target )
    {
	foreach ( 0 .. &getNofMsg() )
	{
	    # ID����Ф�
	    $dId = &getMsgId( $_ );
	    # �ե��������ꥹ�Ȥ��椫�顤������뵭����ID�������
	    &setMsgDaughters( $dId, join( ',', grep(( !/^$TargetId$/o ),
		split( /,/, &getMsgDaughters( $dId )))));
	    # ������������������ID�������
	    $parents = &getMsgParents( $dId );
	    if ( $parents eq $TargetId )
	    {
		$parents = '';
	    }
	    else
	    {
		$parents =~ s/,$TargetId,.*$//;
		$parents =~ s/^$TargetId,.*$//;
		$parents =~ s/,$TargetId$//;
	    }
	    &setMsgParents( $dId, $parents );
	    # ̼���оݤȤ���
	    push( @Target, split( /,/, &getMsgDaughters( $dId ))) if ( $ThreadFlag && ( $dId eq $TargetId ));
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
# - DESCRIPTION
#	�������������롥
#
sub SupersedeArticle
{
    local( $Board, $Id, $postDate, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail ) = @_;

    local( $SupersedeId, $File, $SupersedeFile );

    # ���Ϥ��줿��������Υ����å����������
    &CheckArticle( $Board, $postDate, *Name, *Email, *Url, *Subject, *Icon, *Article );

    # DB�ե����������
    $SupersedeId = &SupersedeDbFile( $Board, $Id, $postDate, $Subject, $Icon, ( $SYS_LOGHOST? $REMOTE_INFO : '' ), $Name, $Email, $Url, $Fmail );

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
sub ReLinkExec
{
    local( $FromId, $ToId, $Board ) = @_;

    local( $dId, @Daughters, $DaughterId );

    # �۴ĵ����ζػ�
    &Fatal( 50, '' ) if ( grep( /^$FromId$/, split( /,/, &getMsgParents( $ToId ))));

    # �ǡ����񤭴���
    foreach ( 0 .. &getNofMsg() )
    {
	# ID����Ф�
	$dId = &getMsgId( $_ );
	# �ե��������ꥹ�Ȥ��椫�顤��ư���뵭����ID�������
	&setMsgDaughters( $dId, join( ',', grep(( !/^$FromId$/o ), split( /,/, &getMsgDaughters( $dId )))));
    }

    # ����åɤ�������ڤ���ϡ����̼�����ν񤭴�����ɬ�פˤʤ롥
    @Daughters = split( /,/, &getMsgDaughters( $FromId )) if ( &getMsgParents( $FromId ) ne '' );

    # ���������Υ�ץ饤����ѹ�����
    if ( $ToId eq '' )
    {
	&setMsgParents( $FromId, '' );
    }
    elsif ( &getMsgParents( $ToId ) eq '' )
    {
	&setMsgParents( $FromId, "$ToId" );
    }
    else
    {
	&setMsgParents( $FromId, "$ToId," . &getMsgParents( $ToId ));
    }

    # ����������̼�ˤĤ��Ƥ⡤��ץ饤����ѹ�����
    while ( $DaughterId = shift( @Daughters ))
    {
	# ¹̼��ġ�
	push( @Daughters, split( /,/, &getMsgDaughters( $DaughterId )));
	# �񤭴���
	if (( &getMsgParents( $DaughterId ) eq $FromId )
	    || ( &getMsgParents( $DaughterId ) =~ /^$FromId,/ ))
	{
	    &setMsgParents( $DaughterId, ( &getMsgParents( $FromId ) ne '' )? "$FromId," . &getMsgParents( $FromId ) : "$FromId" );
	}
	elsif (( &getMsgParents( $DaughterId ) =~ /^(.*),$FromId$/ )
	       || ( &getMsgParents( $DaughterId ) =~ /^(.*),$FromId,/ ))
	{
	    &setMsgParents( $DaughterId, ( &getMsgParents( $FromId ) ne '' )? "$1,$FromId," . &getMsgParents( $FromId ) : "$1,$FromId" );
	}
    }

    # ��ץ饤��ˤʤä������Υե������������ɲä���
    &setMsgDaughters( $ToId, ( &getMsgDaughters( $ToId ) ne '' ) ? &getMsgDaughters( $ToId ) . ",$FromId" : "$FromId" );

    # ����DB�򹹿�����
    &UpdateArticleDb( $Board );
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
sub ReOrderExec
{
    local( $FromId, $ToId, $Board ) = @_;

    local( @Move );

    # ��ư���뵭�������򽸤��
    @Move = ( $FromId, &CollectDaughters( $FromId ));

    # ��ư������
    &ReOrderArticleDb( $Board, $ToId, *Move );
}


###
## CheckArticle - ���Ϥ��줿��������Υ����å�
#
# - SYNOPSIS
#	CheckArticle( $board, *postDate, *name, *eMail, *url, *subject, *icon, *article );
#
# - ARGS
#	$board		�Ǽ���ID
#	*postDate	������ʶ��Ǥ�OK��
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
sub CheckArticle
{
    local( $board, *postDate, *name, *eMail, *url, *subject, *icon, *article ) = @_;

    &CheckPostDate( *postDate );
    &CheckName( *name );
    &CheckEmail( *eMail );
    &CheckURL( *url );
    &CheckSubject( *subject );
    &CheckIcon( *icon ) if $SYS_ICON;

    # ��ʸ�ζ������å���
    &Fatal( 2, $H_MESG ) if ( $article eq '' );

    if ( $SYS_MAXARTSIZE != 0 )
    {
	local( $length ) = length( $article );
	&Fatal( 12, $length ) if ( $length > $SYS_MAXARTSIZE );
    }
}


###
## secureSubject - ������Subject����Ф�
## secureArticle - ������Article����Ф�
#
# - SYNOPSIS
#	secureSubject( *subject );
#	secureArticle( *article, $textType );
#
# - ARGS
#	*subject	Subjectʸ����
#	*article	Articleʸ����
#	$textType	���Ϸ���
#
# - DESCRIPTION
#	$subject�������ʸ������Ѵ����롥
#	$article�������ʸ������Ѵ����롥
#
sub secureSubject
{
    local( *subject ) = @_;

    if ( $SYS_TAGINSUBJECT )
    {
	local( @subjectTags ) = (
	'b',	1,	$HTML_TAGS_GENATTRS,
	'big',	1,	$HTML_TAGS_GENATTRS,
	'cite',	1,	$HTML_TAGS_GENATTRS,
	'code',	1,	$HTML_TAGS_GENATTRS,
	'del',	1,	"$HTML_TAGS_GENATTRS/cite/datetime",
	'em',	1,	$HTML_TAGS_GENATTRS,
	'i',	1,	$HTML_TAGS_GENATTRS,
	'img',	0,	"$HTML_TAGS_GENATTRS/alt/height/longdesc/src/width",
	'ins',	1,	"$HTML_TAGS_GENATTRS/cite/datetime",
	'kbd',	1,	$HTML_TAGS_GENATTRS,
	'samp',	1,	$HTML_TAGS_GENATTRS,
	'small',1,	$HTML_TAGS_GENATTRS,
	'span',	1,	$HTML_TAGS_GENATTRS,
	'strong',1,	$HTML_TAGS_GENATTRS,
	'style',1,	"$HTML_TAGS_I18NATTRS/media/title/type",
	'sub',	1,	$HTML_TAGS_GENATTRS,
	'sup',	1,	$HTML_TAGS_GENATTRS,
	'tt',	1,	$HTML_TAGS_GENATTRS,
	'var',	1,	$HTML_TAGS_GENATTRS,
	);
	
	local( %sNeedVec, %sFeatureVec, $tag );
	while( @subjectTags )
	{
	    $tag = shift( @subjectTags );
	    $sNeedVec{ $tag } = shift( @subjectTags );
	    $sFeatureVec{ $tag } = shift( @subjectTags );
	}

	# secrurity check
	&cgi'SecureXHTML( *subject, *sNeedVec, *sFeatureVec );
    }
    else
    {
	$subject = &HTMLEncode( $subject );	# no tags are allowed.
    }
}

sub secureArticle
{
    local( *article, $textType ) = @_;

    local( @articleTags ) = (
	# ����̾, �Ĥ�ɬ�ܤ��ݤ�, ���Ѳ�ǽ��feature
	'a',	1,	"$HTML_TAGS_GENATTRS/charset/href/hreflang/name/rel/rev/tabindex/target/type",
	'abbr',	1,	$HTML_TAGS_GENATTRS,
	'address',1,	$HTML_TAGS_GENATTRS,
	'b',	1,	$HTML_TAGS_GENATTRS,
	'big',	1,	$HTML_TAGS_GENATTRS,
	'blockquote',1,	"$HTML_TAGS_GENATTRS/cite",
	'br',	0,	$HTML_TAGS_COREATTRS,
	'cite',	1,	$HTML_TAGS_GENATTRS,
	'code',	1,	$HTML_TAGS_GENATTRS,
	'dd',	0,	$HTML_TAGS_GENATTRS,
	'del',	1,	"$HTML_TAGS_GENATTRS/cite/datetime",
	'dfn',	1,	$HTML_TAGS_GENATTRS,
	'div',	1,	$HTML_TAGS_GENATTRS,
	'dl',	1,	$HTML_TAGS_GENATTRS,
	'dt',	0,	$HTML_TAGS_GENATTRS,
	'em',	1,	$HTML_TAGS_GENATTRS,
	'h1',	1,	$HTML_TAGS_GENATTRS,
	'h2',	1,	$HTML_TAGS_GENATTRS,
	'h3',	1,	$HTML_TAGS_GENATTRS,
	'h4',	1,	$HTML_TAGS_GENATTRS,
	'h5',	1,	$HTML_TAGS_GENATTRS,
	'h6',	1,	$HTML_TAGS_GENATTRS,
	'hr',	0,	$HTML_TAGS_COREATTRS,
	'i',	1,	$HTML_TAGS_GENATTRS,
	'img',	0,	"$HTML_TAGS_GENATTRS/alt/height/longdesc/src/width",
	'ins',	1,	"$HTML_TAGS_GENATTRS/cite/datetime",
	'kbd',	1,	$HTML_TAGS_GENATTRS,
	'li',	0,	$HTML_TAGS_GENATTRS,
	'ol',	1,	$HTML_TAGS_GENATTRS,
	'p',	1,	$HTML_TAGS_GENATTRS,
	'pre',	1,	$HTML_TAGS_GENATTRS,
	'q',	1,	"$HTML_TAGS_GENATTRS/cite",
	'samp',	1,	$HTML_TAGS_GENATTRS,
	'small',1,	$HTML_TAGS_GENATTRS,
	'span',	1,	$HTML_TAGS_GENATTRS,
	'strong',1,	$HTML_TAGS_GENATTRS,
	'style',1,	"$HTML_TAGS_I18NATTRS/media/title/type",
	'sub',	1,	$HTML_TAGS_GENATTRS,
	'sup',	1,	$HTML_TAGS_GENATTRS,
	'tt',	1,	$HTML_TAGS_GENATTRS,
	'ul',	1,	$HTML_TAGS_GENATTRS,
	'var',	1,	$HTML_TAGS_GENATTRS,
# ���䥵������style�ǻ��ꤹ�٤��ʤΤǡ���������ɬ���FONT�����ʤ櫓�Ǥ�����
# ����Ǥ�ɡ����Ƥ�Ȥ������Ȥ������ʤ��ϡ�
# ���ιԤ���Ƭ�Ρ�#�פ�ä��Ƥ���������^^;
#	'font',	1,	"$HTML_TAGS_GENATTRS/size/color",
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
    }
    elsif ( $textType eq $H_TTLABEL[1] )
    {
	# convert to html
	&PlainArticleToHtml( *article );
	# secrurity check
	&cgi'SecureXHTML( *article, *aNeedVec, *aFeatureVec );
    }
    elsif ( $textType eq $H_TTLABEL[2] )
    {
	# secrurity check
	&cgi'SecureXHTML( *article, *aNeedVec, *aFeatureVec );
    }
    else
    {
	# Not selected... pre-formatted
	&PlainArticleToPreFormatted( *article );
    }
}


###
## CheckPostDate - ����������å�
#
# - SYNOPSIS
#	CheckPostDate( *str );
#
# - ARGS
#	*str		�������UTC����ηв��ÿ���
#
# - DESCRIPTION
#	������Υ����å���Ԥʤ���
#
sub CheckPostDate
{
    local( *str ) = @_;

    # ���Ǥ�OK
    return if ( $str eq '' );

    # �������ͤˤʤäƤʤ���?�ʲ��Ϥ˼��Ԥ��Ƥ���-1�ˤʤäƤ�Ϥ���
    &Fatal( 21, '' ) if ( $str < 0 );
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
sub CheckSubject
{
    local( *String ) = @_;

    &Fatal( 2, $H_SUBJECT ) unless $String;
    &Fatal( 3, '' ) if ( $String =~ m/[\t\n]/o );

    if ( !$SYS_TAGINSUBJECT )
    {
	&Fatal( 4, '' ) if ( $String =~ m/[<>]/o );
    }
}


###
## CheckIcon - ʸ��������å�: Icon
#
# - SYNOPSIS
#	CheckIcon( *str );
#
# - ARGS
#	*str		Iconʸ����
#
# - DESCRIPTION
#	Icon��ʸ��������å���Ԥʤ���
#	������ʸ������ä��饨�顼ɽ���롼����ء�
#
sub CheckIcon
{
    local( *str ) = @_;

    # ��������Υ����å�; ������������̵���פ����ꡥ
    $str = $H_NOICON if ( !&GetIconUrlFromTitle( $str ));

    &Fatal( 2, $H_ICON ) if ( !$SYS_ALLOWNOICON && ( $str eq $H_NOICON ));
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
sub CheckName
{
    local( *String ) = @_;

    &Fatal( 2, $H_FROM ) if ( !$String );
    &Fatal( 3, '' ) if ( $String =~ m/[\t\n]/o );

    # ���������������ܡ�
    &Fatal( 5, $String ) if ( $String =~ /^\d+$/ );
}


###
## CheckPasswd - ʸ��������å�: �ѥ����
#
# - SYNOPSIS
#	CheckPasswd(*String);
#
# - ARGS
#	*String		�ѥ����ʸ����
#
# - DESCRIPTION
#	�ѥ���ɤ�ʸ��������å���Ԥʤ���
#
# - RETURN
#	1 ... ���顼�ʶ���
#	2 ... ���顼�ʥ���or���ԡ�
#	0 ... OK
#
sub CheckPasswd {
    local( *String ) = @_;

    &Fatal( 2, $H_PASSWD ) if ( !$String );
    &Fatal( 3, $H_PASSWD ) if ( $String =~ /[\t\n]/o );

    return 0;
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
sub CheckEmail
{
    local( *String ) = @_;

    if ( $SYS_POSTERMAIL )
    {
	&Fatal( 2, $H_MAIL ) if ( !$String );
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
sub CheckURL
{
    local( *String ) = @_;

    # http://�����ξ��϶��ˤ��Ƥ��ޤ���
    $String = '' if ( $String =~ m!^http://$!oi );
    &Fatal( 7, 'URL' ) if (( $String ne '' ) && ( !&IsUrl( $String )));
    &Fatal( 3, '' ) if ( $String =~ m/[\t\n]/o );
}


###
## CheckBoardDir - ʸ��������å�: �Ǽ��ĥǥ��쥯�ȥ�
#
# - SYNOPSIS
#	CheckBoardDir( *name );
#
# - ARGS
#	*name		�Ǽ��ĥǥ��쥯�ȥ�̾
#
sub CheckBoardDir
{
    local( *name ) = @_;
    &Fatal( 52, '' ) unless (( $name =~ /\w+/o ) || ( $name =~ /\//o ));
    &Fatal( 2, "$H_BOARDά��" ) if ( $name eq '' );
}

###
## CheckBoardName - ʸ��������å�: �Ǽ���̾
#
# - SYNOPSIS
#	CheckBoardDir( *intro );
#
# - ARGS
#	*intro		�Ǽ���̾
#
sub CheckBoardName
{
    local( *intro ) = @_;
    &Fatal( 2, "$H_BOARD̾��" ) if ( $intro eq '' );
}

###
## CheckBoardHeader - ʸ��������å�: �Ǽ��ĥإå�
#
# - SYNOPSIS
#	CheckBoardHeader( *header );
#
# - ARGS
#	*header		�Ǽ��ĥإå�
#
sub CheckBoardHeader
{
    local( *header ) = @_;
    # ���Ǥ�OK
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
	$IsUrl = 1 if ( $String =~ m!^$Scheme:!i );
    }
    $IsUrl;
}


###
## GetFollowIdTree - ��ץ饤�������ڹ�¤�����
#
# - SYNOPSIS
#	GetFollowIdTree($id, *tree);
#
# - ARGS
#	$id	����ID
#	*tree	�ڹ�¤���Ǽ����ꥹ��
#
# - DESCRIPTION
#	���ꤵ�줿�����Υ�ץ饤�����򡤤���ID���ڹ�¤�ե����ޥåȤǼ��Ф���
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
sub GetFollowIdTree
{
    local( $id, *tree ) = @_;

    # �����Τ��ᡤ�Ƶ���߾��ʥǡ���������ʤ餳�����̤�ʤ���
    return if ( $id eq '' );

    local( @aidList ) = split( /,/, &getMsgDaughters( $id ));

    push( @tree, '(', $id );
    foreach ( @aidList ) { &GetFollowIdTree( $_, *tree ); }
    push( @tree, ')' );
}


###
## GetTreeTopArticle - �ڹ�¤�Υȥå׵��������
#
# - SYNOPSIS
#	GetTreeTopArticle( *tree );
#
# - ARGS
#	*tree	�ڹ�¤����Ǽ�ѤߤΥꥹ��
#
# - DESCRIPTION
#	�ڹ�¤�ξܺ٤ˤĤ��Ƥ�&GetFollowIdTree()�򻲾ȤΤ��ȡ�
#
# - RETURN
#	����ID
#
sub GetTreeTopArticle
{
    local( *tree ) = @_;
    $tree[1];
}


###
## GetReplySubject - ��ץ饤Subject������
#
# - SYNOPSIS
#	GetReplySubject( *subjectStr );
#
# - ARGS
#	$subjectStr	Subjectʸ����
#
# - DESCRIPTION
#	��Ƭ�ˡ�Re:�פ�1�Ĥ����Ĥ��롥
#
sub GetReplySubject
{
    local( *subjectStr ) = @_;

    # Re:���������
    $subjectStr =~ s/^Re:\s*//oi;

    # TAG�ѥ��󥳡��ɤ��ơ�
    &TAGEncode( *subjectStr );

    # ��Ƭ�ˡ�Re: �פ򤯤äĤ����֤���
    $subjectStr = "Re: $subjectStr";
}


###
## GetMailSubjectPrefix - �ᥤ����Subject��prefix�����
#
# - SYNOPSIS
#	GetMailSubjectPrefix( $board, $id );
#
# - ARGS
#	$board	�Ǽ���ID
#	$id	����ID
#
# - DESCRIPTION
#	[foo: 1]���֤���
#
# - RETURN
#	prefixʸ����
#
sub GetMailSubjectPrefix
{
    local( $board, $id ) = @_;
    return "[$board: $id] " if $SYS_MAILHEADBRACKET;
    "";
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
#
# - RETURN
#	�����ɽ�魯ʸ����
#
sub GetDateTimeFormatFromUtc
{
    local( $utc ) = @_;
    local( $sec, $min, $hour, $mDay, $mon, $year ) = localtime( $utc );
    sprintf( "%d/%d/%d(%02d:%02d)", $year+1900, $mon+1, $mDay, $hour, $min );
}


###
## GetYYYY_MM_DD_HH_MM_SSFromUtc - UTC����YYYY/MM/DD(HH:MM:SS)�����
#
# - SYNOPSIS
#	GetYYYY_MM_DD_HH_MM_SSFromUtc( $utc );
#
# - ARGS
#	$utc		�����UTC����ηв��ÿ���
#
# - DESCRIPTION
#	UTC���ʬ�ä�ʬ�䤷��YYYY/MM/DD(HH:MM:SS)�η��˥ե����ޥåȤ���
#	ʸ����Ȥ����֤���
#
#	GetDateTimeFormatFromUtc�Ȼ��Ƥ��뤬������ϡ�
#	GetYYYY_MM_DD_HH_MM_SSFromUtc��GetUtcFromYYYY_MM_DD_HH_MM_SS��
#	�б����Ƥ���ɬ�פ����뤿�ᡥGetDateTimeFormatFromUtc��̵�ط��ʤΤǡ�
#	��ͳ���ѹ����ƹ���ʤ���
#
# - RETURN
#	YYYY/MM/DD(HH:MM:SS)
#
sub GetYYYY_MM_DD_HH_MM_SSFromUtc
{
    local( $utc ) = @_;
    local( $sec, $min, $hour, $mDay, $mon, $year ) = localtime( $utc );
    sprintf( "%d/%d/%d(%02d:%02d:%02d)", $year+1900, $mon+1, $mDay, $hour, $min, $sec );
}


###
## GetUtcFromYYYY_MM_DD_HH_MM_SS - YYYY/MM/DD(HH:MM:SS)����UTC�����
#
# - SYNOPSIS
#	&GetUtcFromYYYY_MM_DD_HH_MM_SS
#	(
#	    $str	�����ɽ��ʸ����
#	);
#
# - DESCRIPTION
#	YYYY/MM/DD(HH:MM:SS)��ʸ�����ʬ�򤷤�UTC��׻���
#
# - RETURN
#	UTC����ηв��ÿ�
#
sub GetUtcFromYYYY_MM_DD_HH_MM_SS
{
    local( $str ) = shift;

    $str =~ m!^(\d+)/(\d+)/(\d+)\((\d\d):(\d\d):(\d\d)\)$!o;
    local( $year, $month, $mday, $hour, $min, $sec ) = ( $1, $2, $3, $4, $5, $6 );
    if (( $year < 1970 )
	|| ( $year > 2037 )
	|| ( $month < 1 )
	|| ( $month > 12 )
	|| ( $mday < 1 )
	|| ( $mday > 31 )
	|| ( $hour < 0 )
	|| ( $hour > 23 )
	|| ( $min < 0 )
	|| ( $min > 59 )
	|| ( $sec < 0 )
	|| ( $sec > 60 ))
    {
	# can't exec timegm/timelocal...
	return -1;
    }

    require( 'timelocal.pl' );
    $year -= 1900;
    $month--;
    &timelocal( $sec, $min, $hour, $mday, $month, $year );
}


###
## GetUtcFromYYYY_MM_DD - YYYY/MM/DD����UTC�����
#
# - SYNOPSIS
#	GetUtcFromYYYY_MM_DD
#	(
#	    $str	�����ɽ��ʸ����
#	);
#
# - DESCRIPTION
#	YYYY/MM/DD��ʸ�����ʬ�򤷤�UTC��׻���
#
# - RETURN
#	UTC����ηв��ÿ�
#
sub GetUtcFromYYYY_MM_DD
{
    local( $str ) = shift;
    return -1 if ( length( $str ) != 10 );

    local( $year, $month, $mday ) = unpack( "a4 x a2 x a2", $str );
    if (( $year < 1970 )
	|| ( $year > 2037 )
	|| ( $month < 1 )
	|| ( $month > 12 )
	|| ( $mday < 1 )
	|| ( $mday > 31 ))
    {
	# can't exec timegm/timelocal...
	return -1;
    }

    require( 'timelocal.pl' );
    $year -= 1900;
    $month--;
    &timelocal( 0, 0, 0, $mday, $month, $year );
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
## URIEscape - URI��escape
#
# - SYNOPSIS
#	URIEscape( $str );
#
# - ARGS
#	$str	URI escape����ʸ����
#
# - DESCRIPTION
#	URI escape��Ԥʤ���
#
# - RETURN
#	URI escape����ʸ����
#
sub URIEscape
{
    local( $_ ) = @_;
    s/([^A-Za-z0-9\\\-_\.!~*'() ])/sprintf( "%%%02X", ord( $1 ))/eg;
    s/ /+/go;
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
#	TAG�����ߡ�<input value="������ʸ����" />���Ѥˡ�"��&���������
#	Encode�ȸ����ʤ��顤���ΤȤ���Decode���뤳�ȤϤǤ�����
#	�����������Τ�
#
# - RETURN
#	Encode����ʸ����
#
sub TAGEncode
{
    local( *str ) = @_;
#    $str =~ s/[\&\"]//go;
    $str =~ s/<[^>]*>//go;
}


###
## ArticleEncode - ������Encode
#
# - SYNOPSIS
#	ArticleEncode( *article );
#
# - ARGS
#	$article	Encode���뵭����ʸ
#
# - DESCRIPTION
#	�������URL([URL:kb:��])�򡤥�󥯤��Ѵ����롥
#
# - RETURN
#	Encode���줿ʸ����
#
sub ArticleEncode
{
    local( *article ) = @_;

    local( $retArticle ) = $article;

    local( $url, $urlMatch, @cache );
    local( $tagStr, $quoteStr );
    while ( $article =~ m/\[url:([^\]]+)\]/gi )
    {
	$tagStr = '';
	$url = $1;
	( $urlMatch = $url ) =~ s/([?+*^\\\[\]\|()])/\\$1/go;
	next if ( grep( /^$urlMatch$/, @cache ));
	push( @cache, $url );
	$quoteStr = "[URL:$url]";

	if ( $urlMatch =~ m/^kb:(.*)$/ )
	{
	    local( $artStr ) = $1;
	    if ( $artStr =~ m!^//.*$! )
	    {
		# not implemented now...
	    }
	    elsif ( $artStr =~ m!^([^/]+)/(.*)$! )
	    {
		local( $boardEsc ) = &GetBoardInfo( $1 );
		$tagStr = &LinkP( "b=$boardEsc&c=e&id=$2", $quoteStr );
	    }
	    else
	    {
		$tagStr = &LinkP( "b=$BOARD_ESC&c=e&id=$artStr", $quoteStr );
	    }
	}
	elsif ( &IsUrl( &HTMLDecode( $urlMatch )))
	{
	    $tagStr = &TagA( $quoteStr, &HTMLDecode( $url ), '', '', '',
		$SYS_LINK_TARGET );
	}
	else
	{
	    next;
	}

	$retArticle =~ s/\[url:$urlMatch\]/$tagStr/gi;
    }

    $retArticle;
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
sub PlainArticleToPreFormatted
{
    local( *Article ) = @_;
    $Article =~ s/\n*$//o;
    $Article = &HTMLEncode( $Article );	# no tags are allowed.
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
sub PlainArticleToHtml
{
    local( *Article ) = @_;
    $Article =~ s/^\n*//o;
    $Article =~ s/\n*$//o;
    $Article =~ s/\n/$HTML_BR/go;
    $Article =~ s/$HTML_BR($HTML_BR)+/<\/p>\n\n<p>/go;
    $Article = "<p>$Article</p>";
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
sub QuoteOriginalArticle
{
    local( $Id, *msg ) = @_;

    # ����������μ���
    local( $fid, $aids, $date, $subject, $icon, $remoteHost, $name, $eMail, $url ) = &getMsgInfo( $Id );

    # �������Τ���˸���������
    local( $pName ) = '';
    if ( $fid )
    {
	local( $pId );
	( $pId = $fid ) =~ s/,.*$//o;
	( $pName ) = &getMsgAuthor( $pId );
    }

    # ����
    local( @ArticleBody );
    &GetArticleBody( $Id, $BOARD, *ArticleBody );

    if ( $SYS_QUOTEMSG )
    {
	local( $premsg ) = $SYS_QUOTEMSG;
	$premsg =~ s/__LINK__/[url:kb:$Id]/i;
	$premsg =~ s/__TITLE__/$subject/;
	$premsg =~ s/__DATE__/&GetDateTimeFormatFromUtc( $date )/e;
	$premsg =~ s/__NAME__/$name/;
	$msg .= $premsg;
    }
    local( $QMark, $line );
    foreach $line ( @ArticleBody )
    {
	&TAGEncode( *line );

	$QMark = $DEFAULT_QMARK;
	$QMark = $name . ' ' . $QMark if $SYS_QUOTENAME;

	# ��ʸ�Τ�����������ʬ�ˤϡ������˰���ʸ�����Ťͤʤ�
	# ���Ԥˤ��פ�ʤ�
	if (( $line =~ /^$/o ) || ( $line =~ /^$pName\s*$DEFAULT_QMARK/ ))
	{
	    $QMark = '';
	}

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
sub QuoteOriginalArticleWithoutQMark
{
    local( $Id, *msg ) = @_;

    local( @ArticleBody, $line );
    &GetArticleBody( $Id, $BOARD, *ArticleBody );
    foreach $line ( @ArticleBody )
    {
	if ( $SYS_TAGINSUPERSEDE )
	{
	    $line = &HTMLEncode( $line );
	}
	else
	{
	    &TAGEncode( *line );
	}
	$msg .= $line;
    }
}


###
## PageLink - �ڡ����إå�/�եå���ɽ��
#
# - SYNOPSIS
#	ShowPageLinkTop( $com, $num, $old, $rev, $vRev );
#	ShowPageLinkBottom( $com, $num, $old, $rev, $vRev );
#
# - ARGS
#	$com	��󥯤��륳�ޥ��ʸ����
#	$num	'num'����
#	$old	'old'����
#	$rev	'rev'����
#	$fold	'fold'����
#		'': Ÿ����󥯤ʤ�
#		0, 1: Ÿ������
#
# - DESCRIPTION
#	�ڡ����إå�/�եå��Υ�󥯷�ʸ�����������롥
#
sub PageLink
{
    local( $com, $num, $old, $rev, $fold ) = @_;

    local( $nextOld ) = ( $old > $num )? ( $old - $num ) : 0;
    local( $backOld ) = ( $old + $num );

    local( $str );
    $str = '<p class="kbPageLink">';

    if ( $old )
    {
	$str .= &LinkP( "b=$BOARD_ESC&c=$com&num=$num&old=0&fold=$fold&rev=$rev", $H_TOP . &TagAccessKey( 'T' ), 'T' );
	$str .= ' | ' . &LinkP( "b=$BOARD_ESC&c=$com&num=$num&old=$nextOld&fold=$fold&rev=$rev", $H_UP . &TagAccessKey( 'N' ), 'N' );
    }
    else
    {
	$str .= $H_TOP . &TagAccessKey( 'T' ) . ' | ' . $H_UP . &TagAccessKey( 'N' );
    }

    if ( $SYS_REVERSE )
    {
	$str .= ' | ' .
	    &LinkP( "b=$BOARD_ESC&c=$com&num=$num&old=$old&fold=$fold&rev=" . ( 1-$rev ), $H_REVERSE[ 1-$rev ] . &TagAccessKey( 'R' ), 'R', $H_REVERSE_L );
    }

    if ( $SYS_EXPAND && ( $fold ne '' ))
    {
	$str .= ' | ' . &LinkP( "b=$BOARD_ESC&c=$com&num=$num&old=$old&rev=$rev&fold=" . ( 1-$fold ), $H_EXPAND[ 1-$fold ] . &TagAccessKey( 'E' ), 'E', $H_EXPAND_L );
    }

    $str .= ' | ';

    local( $nofMsg ) = &getNofMsg();
    if ( $num && ( $nofMsg - $backOld >= 0 ))
    {
	$str .= &LinkP( "b=$BOARD_ESC&c=$com&num=$num&old=$backOld&fold=$fold&rev=$rev", $H_DOWN . &TagAccessKey( 'P' ), 'P' );
	$str .= ' | ' . &LinkP( "b=$BOARD_ESC&c=$com&num=$num&old=" . ( $nofMsg - $num + 1) . "&fold=$fold&rev=$rev", $H_BOTTOM . &TagAccessKey( 'B' ), 'B' );
    }
    else
    {
	$str .= $H_DOWN . &TagAccessKey( 'P' ) . ' | ' . $H_BOTTOM . &TagAccessKey( 'B' );
    }

    $str .= "</p>\n";

    $str;
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
#
# - DESCRIPTION
#	���᡼����ɽ���ѥ����˥ե����ޥåȤ��롥
#
#	$SYS_COMICON:
#		1 ... ��������θ���ʸ������ɲä��ʤ�
#		2 ... ��������θ���ʸ������ɲä��ʤ�
#		0/others ... ��������ʤ��ǥƥ����Ȥ���
#
sub TagComImg
{
    local( $src, $alt ) = @_;
    if ( $SYS_COMICON == 1 )
    {
	qq(<img src="$src" alt="$alt" width="$COMICON_WIDTH" height="$COMICON_HEIGHT" class="kbComIcon" />);
    }
    elsif ( $SYS_COMICON == 2 )
    {
	qq(<img src="$src" alt="$alt" width="$COMICON_WIDTH" height="$COMICON_HEIGHT" class="kbComIcon" />$alt);
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
#	TagMsgImg( $icon );
#
# - ARGS
#	$icon		�������󥿥���
#
# - DESCRIPTION
#	���᡼����ɽ���ѥ����˥ե����ޥåȤ��롥
#
sub TagMsgImg
{
    local( $icon ) = @_;

    if ( !$icon || $icon eq $H_NOICON )
    {
	return "";
    }
    elsif ( $SYS_ICON )
    {
	local( $src ) = &GetIconUrlFromTitle( $icon );
	qq(<img src="$src" alt="[$icon]" width="$MSGICON_WIDTH" height="$MSGICON_HEIGHT" class="kbMsgIcon" />);
    }
    else
    {
	return "[$icon]";
    }
}


###
## TagA - ��󥯥����Υե����ޥå�
#
# - SYNOPSIS
#	TagA();
#
# - ARGS
#	$markUp		�ޡ������å�ʸ����
#	$href		�����URL�ʾ�ά�ġ�
#	$key		�������������ʾ�ά�ġ�
#	$title		�����ȥ�ʸ����ʾ�ά�ġ�
#	$name		����̾�ʾ�ά�ġ�
#	$target		�������åȥե졼��ʾ�ά�ġ�
#
# - DESCRIPTION
#	��󥯤��󥯥����˥ե����ޥåȤ��롥
#
sub TagA
{
    local( $markUp, $href, $key, $title, $name, $target ) = @_;

    if ( $key eq '' )
    {
	$key = $gLinkNum;
	$gLinkNum = 0 if ( ++$gLinkNum > 9 );
    }
    local( $str ) = qq(<a accesskey="$key");
    $str .= qq( href="$href") if ( $href ne '' );
    $str .= qq( title="$title") if ( $title ne '' );
    $str .= qq( name="$name") if ( $name ne '' );
    $str .= qq( target="$target") if ( $target ne '' );
    $str .= ">$markUp</a>";
    $str;
}


###
## TagAccessKey - ��������������٥�Υե����ޥå�
#
# - SYNOPSIS
#	TagAccessKey( $key );
#
# - ARGS
#	$key		����1ʸ��
#
sub TagAccessKey
{
    qq{(<span class="kbAccessKey">$_[0]</span>)};
}


###
## TagLabel - ��٥륿���Υե����ޥå�
#
# - SYNOPSIS
#	TagLabel( $markUp, $label, $accessKey );
#
# - ARGS
#	$markUp		�ޡ������å�ʸ����
#	$label		��٥��оݥ���ȥ���
#	$accessKey	������������
#
sub TagLabel
{
    local( $markUp, $label, $accessKey ) = @_;
    if ( $accessKey )
    {
	qq[<label for="$label" accesskey="$accessKey">$markUp] . &TagAccessKey( $accessKey ) . "</label>";
    }
    else
    {
	qq[<label for="$label">$markUp</label>];
    }
}


###
## TagInputSubmit - submit/reset�ܥ��󥿥��Υե����ޥå�
#
# - SYNOPSIS
#	TagInputSubmit( $type, $value, $key );
#
# - ARGS
#	$type	submit/reset
#	$value	��٥�˻Ȥ���
#	$key	accesskey�˻Ȥ���
#
sub TagInputSubmit
{
    local( $type, $value, $key ) = @_;
    $gTabIndex++;
    if ( $type eq 'reset' )
    {
	qq(<input type="reset" value="$value" accesskey="$key" tabindex="$gTabIndex" />);
    }
    else
    {
	qq(<input type="submit" value="$value" accesskey="$key" tabindex="$gTabIndex" />);
    }
}


###
## TagInputText - ���ϥ����Υե����ޥå�
#
# - SYNOPSIS
#	TagInputText( $type, $id, $value, $size );
#
# - ARGS
#	$type	text/password
#	$id	id��name�˻Ȥ���
#	$value	�ǥե�����ͤ˻Ȥ���
#	$size	size�˻Ȥ���
#
sub TagInputText
{
    local( $type, $id, $value, $size ) = @_;
    $gTabIndex++;
    qq(<input type="$type" id="$id" name="$id" value="$value" size="$size" tabindex="$gTabIndex" />);
}


###
## TagInputCheck - �����å��ܥå��������Υե����ޥå�
#
# - SYNOPSIS
#	TagInputCheck( $id, $checked );
#
# - ARGS
#	$id		id��name�˻Ȥ���
#	$checked	true�ʤ�checked���դ�
#
# - DESCRIPTION
#	value��"on"���ꡥ
#
sub TagInputCheck
{
    local( $id, $checked ) = @_;
    $gTabIndex++;
    if ( $checked )
    {
	qq(<input type="checkbox" id="$id" name="$id" value="on" tabindex="$gTabIndex" checked="checked" />);
    }
    else
    {
	qq(<input type="checkbox" id="$id" name="$id" value="on" tabindex="$gTabIndex" />);
    }
}


###
## TagInputRadio - �饸���ܥ��󥿥��Υե����ޥå�
#
# - SYNOPSIS
#	TagInputRadio( $id, $name, $value, $checked );
#
# - ARGS
#	$id		id�˻Ȥ���
#	$name		name�˻Ȥ���
#	$value		�ǥե�����ͤ˻Ȥ���
#	$checked	true�ʤ�checked���դ�
#
sub TagInputRadio
{
    local( $id, $name, $value, $checked ) = @_;
    $gTabIndex++;
    if ( $checked )
    {
	qq(<input type="radio" id="$id" name="$name" value="$value" tabindex="$gTabIndex" checked="checked" />);
    }
    else
    {
	qq(<input type="radio" id="$id" name="$name" value="$value" tabindex="$gTabIndex" />);
    }
}


###
## TagTextarea - textarea�����Υե����ޥå�
#
# - SYNOPSIS
#	TagTextarea( $id, $value, $rows, $cols );
#
# - ARGS
#	$id	id��name�˻Ȥ���
#	$value	�ǥե�����ͤ˻Ȥ���
#	$rows	rows�˻Ȥ���
#	$cols	cols�˻Ȥ���
#
sub TagTextarea
{
    local( $id, $value, $rows, $cols ) = @_;
    $gTabIndex++;
    qq(<textarea id="$id" name="$id" rows="$rows" cols="$cols" tabindex="$gTabIndex">$value</textarea>);
}


###
## TagSelect - select�����Υե����ޥå�
#
# - SYNOPSIS
#	TagSelect( $id, $contents );
#
# - ARGS
#	$id		id��name�˻Ȥ���
#	$contents	������ѥ���ƥ��
#
sub TagSelect
{
    local( $id, $contents ) = @_;
    $gTabIndex++;
    qq(<select id="$id" name="$id" tabindex="$gTabIndex">$contents</select>);
}


###
## TagFieldset - fieldset�����Υե����ޥå�
#
# - SYNOPSIS
#	TagFieldset( $title, $contents );
#
# - ARGS
#	$title		legend�˻Ȥ���
#	$contents	fieldset�Υ���ƥ��
#
sub TagFieldset
{
    local( $title, $contents ) = @_;
    qq(<fieldset>\n<legend>$title</legend>\n$contents</fieldset>\n);
}


###
## LinkP - ���ץ���������󥯤�����
#
# - SYNOPSIS
#	LinkP( $href, $markUp );
#
# - ARGS
#	$comm		����襳�ޥ�����ʡ�?�ʹߡ�
#	$markUp		�ޡ������å�ʸ����
#	$key		�������������ʾ�ά�ġ�
#	$title		�����ȥ�ʸ����ʾ�ά�ġ�
#	$name		����̾�ʾ�ά�ġ�
#	$fragment	#�ʹߤ˻Ȥ��ʾ�ά�ġ�
#
# - DESCRIPTION
#	���ץ����ؤΥ�󥯤���������
#
sub LinkP
{
    local( $comm, $markUp, $key, $title, $name, $fragment ) = @_;
    $comm .= "&kinoA=3&kinoU=$UNAME_ESC&kinoP=$PASSWD" if ( $SYS_AUTH == 3 );
    $comm =~ s/&/&amp;/go;
    $comm .= "#$fragment" if ( $fragment ne '' );
    &TagA( $markUp, "$PROGRAM?$comm", $key, $title, $name );
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
    foreach ( split(/,/, &getMsgDaughters( $Id )))
    {
	push( @Return, $_ );
	push( @Return, &CollectDaughters( $_ )) if ( &getMsgDaughters( $_ ) ne '' );
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
    local( $id, $artKey );
    &GetArticleId( $Board, *id, *artKey );
    $id + 1;
}


###
## GetTitleOldIndex - 'old'�ͤμ���
#
# - SYNOPSIS
#	GetTitleOldIndex( $id );
#
# - ARGS
#	$id	�����ֹ�
#
# - DESCRIPTION
#	���ꤷ��ID�ε�����ޤ�褦��old�ͤ�׻����롥
#	DbCache���ƤӽФ��ѤߤǤʤ���Фʤ�ʤ���
#
# - RETURN
#	old��
#
sub GetTitleOldIndex
{
    local( $id ) = @_;
    local( $old ) = &getNofMsg() - int( $id + $DEF_TITLE_NUM/2 );
    ( $old >= 0 )? $old : 0;
}


###
## LockAll/UnlockAll - �����ƥ�Υ�å�/�����å�
## LockBoard/UnlockBoard - �Ǽ��ĤΥ�å�/�����å�
#
# - SYNOPSIS
#	LockAll();
#	UnlockAll();
#	LockBoard();
#	UnlockBoard();
#
# - DESCRIPTION
#	�����ƥ�/�Ǽ��Ĥ��å�/�����å����롥
#	��å��˻Ȥ��ե������$LOCK_FILE/$LOCK_FILE_B��
#
# - RETURN
#	�ʤ����������������Ԥ���Х��顼�ڡ����ء�
#
sub LockAll
{
    local( $lockResult ) = $PC ? 1 : &cgi'lock_file( $LOCK_FILE );
    &Fatal( 1001, '' ) if ( $lockResult == 2 );
    &Fatal( 999, '' ) if ( $lockResult != 1 );
    &LockBoard() if $LOCK_FILE_B;
}

sub UnlockAll
{
    &cgi'unlock_file( $LOCK_FILE ) unless $PC;
    &UnlockBoard() if $LOCK_FILE_B;
}

sub LockBoard
{
    local( $lockResult ) = $PC ? 1 : &cgi'lock_file( $LOCK_FILE_B );
    &Fatal( 1001, '' ) if ( $lockResult == 2 );
    &Fatal( 999, '' ) if ( $lockResult != 1 );
}

sub UnlockBoard
{
    &cgi'unlock_file( $LOCK_FILE_B ) unless $PC;
}


###
## IsUser - �桼���Υ����å�
#        
# - SYNOPSIS
#       IsUser( $name );
#
# - ARGS
#       $name           �桼��̾
#
# - DESCRIPTION
#       ���ߤ����ѥ桼����$name���ɤ����Τ���롥
#	���¥����å���$POLICY�ˤޤȤ�Ƥ��롥
#	���¥����å��˴ؤ��뤳�Ȥϡ����δؿ��˰�¸���ʤ��褦�ˤ��٤��Ǥ��롥
#   
# - RETURN
#       true/false
#
sub IsUser
{
    local( $name ) = @_;
    ( $SYS_AUTH && (( $UNAME eq $name ) || (( $UNAME eq $ADMIN ) && ( $name eq $MAINT_NAME ))));
}


###
## SendArticleMail - �ᥤ������
#
# - SYNOPSIS
#	SendArticleMail(
#	    $FromName,	�ᥤ��������̾
#	    $FromAddr,	�ᥤ�������ԥᥤ�륢�ɥ쥹
#	    $Subject,	�ᥤ���Subjectʸ����
#	    $Message,	��ʸ
#	    $Id,	���Ѥ���ʤ鵭��ID; ���ʤ���ѥʥ�
#	    @To		����E-Mail addr.�Υꥹ��
#	)
#
# - DESCRIPTION
#	�ᥤ����������롥
#
sub SendArticleMail
{
    local( $FromName, $FromAddr, $Subject, $Message, $Id, @To ) = @_;

    local( $ExtHeader, @ArticleBody );

    $ExtHeader = "X-MLServer: $PROGNAME\n";
    $ExtHeader .= "X-Kb-System: $SYSTEM_NAME\n";
    if (( ! $SYS_MAILHEADBRACKET ) && $BOARDNAME && ($Id ne '' ))
    {
	$ExtHeader .= "X-Kb-Board: $BOARDNAME\nX-Kb-Articleid: $Id\n";
    }

    local( $stat, $errstr ) = &SendMail( $FromName, $FromAddr, $Subject, $ExtHeader, $Message, @To );
    &Fatal( 9, "$BOARDNAME/$Id/$errstr" ) unless $stat;
}


###
## SendMail - �ᥤ������
#
# - SYNOPSIS
#	SendMail(
#	    $FromName,	�ᥤ��������̾
#	    $FromAddr,	�ᥤ�������ԥᥤ�륢�ɥ쥹
#	    $Subject,	�ᥤ���Subjectʸ����
#	    $ExtHeader,	�ɲåإå�
#	    $Message,	��ʸ
#	    @To		����E-Mail addr.�Υꥹ��
#	)
#
# - DESCRIPTION
#	�ᥤ����������롥
#
# - RETURN
#	( $status, $errstr )
#		$status		0 if succeeded, errCode if failed.
#		$errstr		errstr if failed.
#
sub SendMail
{
    local( $FromName, $FromAddr, $Subject, $ExtHeader, $Message, @To ) = @_;

    if ( !$FromAddr )
    {
	# �ᥤ�륢�ɥ쥹̤���ϤˤĤ���������̾���ǽФ���
	$FromName = ( $MAILFROM_LABEL || $MAINT_NAME );
	$FromAddr = $MAINT;
    }

    local( $SenderFrom, $SenderAddr ) = (( $MAILFROM_LABEL || $MAINT_NAME ),
	$MAINT );
    &cgi'sendMail( $FromName, $FromAddr, $SenderFrom, $SenderAddr, $Subject,
 	$ExtHeader, $Message, $MAILTO_LABEL, @To );
}


###
## KbLog - ������
#
# - SYNOPSIS
#	KbLog( $kinologue'severity, *msg );
#
# - ARGS
#	$kinologue'severity	severity id defined in kinologue.pl.
#	*msg			reference to msg string.
#
# - DESCRIPTION
#	log a log using kinologue.
#	exit program(not function) if failed to write log.
#
sub KbLog
{
    local( $severity, $msg ) = @_;

    if ( $SYS_LOG )
    {
	$msg .= "(Remote host:$REMOTE_INFO)" if $SYS_LOGHOST;
	local( $logfile ) = ( $severity >= $kinologue'SEV_ERROR )?
	    "$LOG_DIR/$ERROR_LOG" :
	    "$LOG_DIR/$ACCESS_LOG";
	$logfile .= ( $SYS_LOG == 1 )? '.html' : '.txt';

	&kinologue'KlgLog( $severity, $msg, $PROGNAME, $logfile,
	    ( $SYS_LOG == 1 )? $kinologue'FF_HTML : $kinologue'FF_PLAIN )
	    || &Fatal( 1000, '' );
    }
}


###
## Fatal - ���顼����
#
# - SYNOPSIS
#	Fatal( $errno, $errInfo );
#
# - ARGS
#	$errno	���顼�ֹ�(�ܤ����ϴؿ������򻲾ȤΤ���)
#	$errInfo	���顼����
#
# - DESCRIPTION
#	���顼��ɽ�����̤�֥饦�����������롥
#
# - RETURN
#	�ʤ�
#
sub Fatal
{
    local( $errno, $errInfo ) = @_;

    local( $severity, $msg ) = &FatalStr( $errno, $errInfo );

    # �۾ｪλ�β�ǽ��������Τǡ��Ȥꤢ����lock�򳰤�
    # (��å��μ��Ԥλ��ʳ�)
    if ( !$PC && ( $errno != 999 ) && ( $errno != 1001 ))
    {
	&UnlockAll();
    }

    # log a log(except logging failure).
    &KbLog( $severity, $msg ) if ( $errno != 1000 );
    &UIFatal( $msg );
    &KbLog( $kinologue'SEV_INFO, 'Exec finished.' ) if ( $errno != 1000 );
    exit( 0 );
}


###
## FatalStr - ���顼�����ɤ�������٤ȥ��顼��å����������
#        
# - SYNOPSIS
#	FatalStr( $errno, $errInfo );
#
# - ARGS
#	$errno		���顼������
#	$errInfo	�ղþ���
#
# - DESCRIPTION
#	���顼�����ɤ�������٤ȥ��顼��å�������������롥
#   
# - RETURN
#	( $severity, $mst )
#
sub FatalStr
{
    local( $errno, $errInfo ) = @_;

    local( $severity, $msg );
    if ( $errno == 1 )
    {
	$severity = $kinologue'SEV_CAUTION;
	$msg = "File: $errInfo��¸�ߤ��ʤ������뤤��permission�����꤬�ְ�äƤ��ޤ���";
    }
    elsif ( $errno == 2 )
    {
	$severity = $kinologue'SEV_INFO;
	$msg = "��$errInfo�פ����Ϥ���Ƥ��ޤ�����äƤ⤦���٤��ľ���ƤߤƤ���������";
    }
    elsif ( $errno == 3 )
    {
	$severity = $kinologue'SEV_INFO;
	$msg = "$H_SUBJECT��$H_FROM��$H_MAIL�ˡ�����ʸ�������Ԥ����äƤ��ޤäƤ��ޤ�����äƤ⤦���٤��ľ���ƤߤƤ���������";
    }
    elsif ( $errno == 4 )
    {
	$severity = $kinologue'SEV_INFO;
	$msg = "�����HTML����������뤳�Ȥ϶ؤ����Ƥ��ޤ�����äư㤦��˽񤭴����Ƥ���������";
    }
    elsif ( $errno == 5 )
    {
	$severity = $kinologue'SEV_INFO;
	$msg = "��$errInfo�פȤ���$H_FROM�ϻȤ��ޤ�����ä��̤�$H_FROM����ꤷ�Ƥ���������";
    }
    elsif ( $errno == 6 )
    {
	$severity = $kinologue'SEV_WARN;
	$msg = "��$errInfo�פȤ���$H_MAIL����Ͽ�ѤߤǤ���";
    }
    elsif ( $errno == 7 )
    {
	$severity = $kinologue'SEV_INFO;
	$msg = "$errInfo��������������ޤ���? ��äƤ⤦���٤��ľ���ƤߤƤ���������";
    }
    elsif ( $errno == 8 )
    {
	$severity = $kinologue'SEV_INFO;
	$msg = "����$H_MESG�Ϥޤ���Ƥ���Ƥ��ޤ���";
    }
    elsif ( $errno == 9 )
    {
	local( $board, $id, $info ) = split( /\//, $errInfo, 3 );
	$severity = $kinologue'SEV_ERROR;
	$msg = "�ۥ��ȥޥ���β����١��ᥤ�륢�ɥ쥹�θ�������ͳ�ˤ�ꡤ$H_MESG�Υᥤ��Ǥ��ۿ������Ԥ��ޤ�����$H_BOARD: $board��ID: $id������: $info�ˡ�$H_MESG���������񤭹��ޤ�ޤ����Τǡ����ٽ񤭹��ߤ�ɬ�פϤ���ޤ���";
    }
    elsif ( $errno == 10 )
    {
	$severity = $kinologue'SEV_CAUTION;
	$msg = "kb.db��kb.aid�������������Ƥ��ޤ���";
    }
    elsif ( $errno == 11 )
    {
	$severity = $kinologue'SEV_ERROR;
	$msg = "$errInfo�Ȥ���ID���б�����$H_BOARD�ϡ�¸�ߤ��ޤ���";
    }
    elsif ( $errno == 12 )
    {
	$severity = $kinologue'SEV_WARN;
	$msg = "����$H_BOARD�Ǥϡ�$H_MESG�κ��祵������$SYS_MAXARTSIZE�Х��ȤȤ������ȤˤʤäƤ��ޤ��ʤ��ʤ���$H_MESG��$errInfo�Х��ȤǤ��ˡ�";
    }
    elsif ( $errno == 13 )
    {
	$severity = $kinologue'SEV_FATAL;
	$msg = "$errInfo�ؤν񤭹��ߤ˼��Ԥ��ޤ������ե����륷���ƥ�˶������̤��ʤ���ǽ��������ޤ���";
    }
    elsif ( $errno == 14 )
    {
	$severity = $kinologue'SEV_FATAL;
	$msg = "����rename�˼��Ԥ��ޤ�����$errInfo�ˡ��ե�����ѡ��ߥå���������ߥ��β�ǽ��������ޤ���";
    }
    elsif ( $errno == 15 )
    {
	$severity = $kinologue'SEV_ERROR;
	$msg = "�񤭹��߸������ϥե����ब�Ų᤮�ޤ�������";
    }
    elsif ( $errno == 16 )
    {
	$severity = $kinologue'SEV_ERROR;
	$msg = "Ʊ��񤭹��ߥե����फ���Ϣ³�񤭹��ߤ϶ػߤ���Ƥ��ޤ���Ϣ³����$H_MESG��񤭹�����ϡ��񤭹��ߥե����������ɤ߹���ľ���Ƥ���ˤ��Ƥ���������";
    }
    elsif ( $errno == 17 )
    {
	$severity = $kinologue'SEV_ERROR;
	$msg = "���ߡ�$H_ICON���Ȥ�������ˤʤäƤ��ޤ���$H_ICON��Ȥ���������ѹ����Ƥ�����٤��ľ���Ƥ���������";
    }
    elsif ( $errno == 18 )
    {
	local( $file, $func ) = split( /\//, $errInfo, 2 );
	$severity = $kinologue'SEV_ERROR;
	$msg = "$file�����$func�����Ѥ��뤳�ȤϤǤ��ޤ��󡥡���";
    }
    elsif ( $errno == 19 )
    {
	$severity = $kinologue'SEV_WARN;
	$msg = "$H_REPLY�Τ���$H_MESG������/����Ǥ��ޤ��󡥡���";
    }
    elsif ( $errno == 20 )
    {
	$severity = $kinologue'SEV_FATAL;
	$msg = "����copy�˼��Ԥ��ޤ�����$errInfo�ˡ��ե�����ѡ��ߥå���������ߥ��β�ǽ��������ޤ���";
    }
    elsif ( $errno == 21 )
    {
	$severity = $kinologue'SEV_INFO;
	$msg = "$H_DATE�Υե����ޥåȤ�'yyyy/mm/dd(HH:MM:SS)'�ǤϤ���ޤ�����äƤ⤦���٤��ľ���ƤߤƤ���������";
    }
    elsif ( $errno == 40 )
    {
	$severity = $kinologue'SEV_WARN;
	$msg = "$H_PASSWD��ְ㤨�Ƥ��ޤ���? $H_FROM��$H_PASSWD���ǧ������äƤ��ľ���ƤߤƤ���������" . &LinkP( "c=lo", "�桼������θƤӽФ�" . &TagAccessKey( 'L' ), 'L' );
    }
    elsif ( $errno == 41 )
    {
	$severity = $kinologue'SEV_WARN;
	$msg = "��$errInfo�פȤ���$H_FROM����Ͽ����Ƥ��ʤ��褦�Ǥ�������";
    }
    elsif ( $errno == 42 )
    {
	$severity = $kinologue'SEV_INFO;
	$msg = "2�Ĥ�$H_PASSWD���ۤʤäƤ���褦�Ǥ����ߥ��ɻߤΤ��ᡤ$H_PASSWD��Ʊ����Τ�2�����Ϥ��ޤ�����äƤ��ľ���ƤߤƤ���������";
    }
    elsif ( $errno == 44 )
    {
	$severity = $kinologue'SEV_WARN;
	$msg = "�����ʤ��������ε�ǽ�����ѤǤ��ޤ��󡥡���";
    }
    elsif ( $errno == 50 )
    {
	$severity = $kinologue'SEV_INFO;
	$msg = "$H_REPLY�ط����۴Ĥ��Ƥ��ޤ��ޤ����ɤ����Ƥ�$H_REPLY����ѹ���������硤$H_REPLY�����ٿ��尷���ˤ��Ƥ��顤$H_REPLY�򤫤������Ƥ���������";
    }
    elsif ( $errno == 51 )
    {
	$severity = $kinologue'SEV_INFO;
	$msg = "��$errInfo�פȤ���$H_BOARD�ϴ���¸�ߤ��ޤ�������";
    }
    elsif ( $errno == 52 )
    {
	$severity = $kinologue'SEV_INFO;
	$msg = "$H_BOARDά�Τϡ�Ⱦ�ѤΥ���ե��٥åȤ⤷���Ͽ����ˤ��Ƥ���������";
    }
    elsif ( $errno == 99 )
    {
	$severity = $kinologue'SEV_WARN;
	$msg ="����$H_BOARD�Ǥϡ����Υ��ޥ�ɡ�$errInfo�ˤϼ¹ԤǤ��ޤ���";
    }
    elsif ( $errno == 998 )
    {
	$severity = $kinologue'SEV_FATAL;
	$msg = "�����ʥ��顼��$errInfo�ˡ�";
    }
    elsif ( $errno == 999 )
    {
	$severity = $kinologue'SEV_WARN;
	$msg ="�����ƥ�Υ�å��˼��Ԥ��ޤ��������߹�äƤ���褦�Ǥ��Τǡ���ʬ�ԤäƤ���⤦���٥����������Ƥ���������";
    }
    elsif ( $errno == 1000 )
    {
	$severity = $kinologue'SEV_FATAL;
	$msg ="���ե�����ؤν񤭹��ߤ˼��Ԥ��ޤ�����";
    }
    elsif ( $errno == 1001 )
    {
	$severity = $kinologue'SEV_WARN;
	$msg ="���ߴ����Ԥˤ����ƥʥ���Ǥ������Ф餯���Ԥ�����������";
    }
    else
    {
	$severity = $kinologue'SEV_ANY;
	$msg = "���顼�ֹ������$errInfo��";
    }

    if ( $severity >= $kinologue'SEV_CAUTION )
    {
	$msg .= "���Ѥ�����Ǥ��������Υڡ�����URL��" . $cgi'REQUEST_URI . "�ˡ����Υ�å�������ʸ�Υ��ԡ��ȡ����顼��������������" . &TagA( $MAINT, "mailto:$MAINT" ) . "�ޤǤ��Τ餻ĺ����Ƚ�����ޤ���";
    }

    return ( $severity, $msg );
}


######################################################################
# �ǡ�������ץ���ơ������


###
## CopyDb - DB�Υ��ԡ�
#
# - SYNOPSIS
#	CopyDb( $src, $dest );
#
# - ARGS
#	$src	���ԡ���
#	$dest	���ԡ���
#
# - DESCRIPTION
#	$src, $dest��ե�����̾�ȸ��路��DB�򥳥ԡ����롥
#	$dest�Ͼ�񤭤����Τ���ա�
#
# - RETURN
#	true if succeeded.
#
sub CopyDb
{
    local( $src, $dest ) = @_;
    open( SRC, "<$src" ) || return 0;
    open( DEST, ">$dest" ) || return 0;
    while ( <SRC> )
    {
	print( DEST $_ ) || return 0;
    }
    close DEST || return 0;
    close SRC;

    1;
}


###
## GenTSV - ���ֶ��ڤ�ʸ����κ���
#
# - SYNOPSIS
#	GenTSV( *line, @data );
#
# - ARGS
#	$line	���ֶ��ڤ�Υǡ������Ǽ����ʸ����
#	@data	�ǡ���
#
# - DESCRIPTION
#	�ǡ�����TSV�ե����ޥåȤ��������롥
#	�ǡ����ϲ��Ԥ�ޤ�ǤϤʤ�ʤ���
#
sub GenTSV
{
    local( *line, @data ) = @_;
    grep( s/\t/$COLSEP/go, @data );
    $line = join( "\t", @data );
}


###
## GenCSV - ����޶��ڤ�ʸ����κ���
#
# - SYNOPSIS
#	GenCSV( *line, @data );
#
# - ARGS
#	$line	���ֶ��ڤ�Υǡ������Ǽ����ʸ����
#	@data	�ǡ���
#
# - DESCRIPTION
#	�ǡ�����CSV�ե����ޥåȤ��������롥
#
sub GenCSV
{
    local( *line, @data ) = @_;
    grep((( s/\"/\"\"/go || m/,/o || m/\n/o ) && ( $_ = "\"$_\"" )), @data );
    $line = join( ',', @data );
}


###
## ParseTSV - ���ֶ��ڤ�ʸ����β���
#
# - SYNOPSIS
#	ParseTSV( *src, *dataArray );
#
# - ARGS
#	$src		���ϸ��ǡ���
#	@dataArray	���Ϥ����ǡ������Ǽ����ꥹ��
#
# - DESCRIPTION
#	�ǡ�����TSV�ե����ޥåȤ��������롥
#
sub ParseTSV
{
    local( *src, *dataArray ) = @_;
    @dataArray = split( /\t/, $src );
}


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
sub DbCache
{
    return if $gBoardDbCached;

    local( $Board ) = @_;

    local( $dId, $dFid, $dAids, $dDate, $dTitle, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail );

    @DB_ID = %DB_FID = %DB_AIDS = %DB_DATE = %DB_TITLE = %DB_ICON = %DB_REMOTEHOST = %DB_NAME = %DB_EMAIL = %DB_URL = %DB_FMAIL = %DB_NEW = ();

    local( $newIconLimit );
    $newIconLimit = $^T - $SYS_NEWICON_VALUE * 24 * 60 * 60
	if ( $SYS_NEWICON == 2 );
    
    local( $i ) = 0;
    local( @data, $dId );
    local( $DBFile ) = &GetPath( $Board, $DB_FILE_NAME );
    open( DB, "<$DBFile" ) || &Fatal( 1, $DBFile );
    while ( <DB> )
    {
	next if (/^\#/o || /^$/o);
	chop;
	( $dId, $dFid, $dAids, $dDate, $dTitle, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail ) = split( /\t/, $_, 11 );
	$DB_ID[$i++] = $dId;
	$DB_FID{$dId} = $dFid;
	$DB_AIDS{$dId} = $dAids;
	$DB_DATE{$dId} = $dDate || &GetModifiedTime( $dId, $Board );
	$DB_TITLE{$dId} = $dTitle || $dId;
	$DB_ICON{$dId} = $dIcon;
	$DB_REMOTEHOST{$dId} = $dRemoteHost;
	$DB_NAME{$dId} = $dName || $MAINT_NAME;
	$DB_EMAIL{$dId} = $dEmail;
	$DB_URL{$dId} = $dUrl;
	$DB_FMAIL{$dId} = $dFmail;

	if (( $SYS_NEWICON == 2 ) && ( $newIconLimit < $DB_DATE{$dId} ))
	{
	    $DB_NEW{$dId} = 1
	}
    }
    close DB;

    if ( $SYS_NEWICON == 1 )
    {
	local( $from ) = ( $#DB_ID >= $SYS_NEWICON_VALUE )?
	    $#DB_ID - $SYS_NEWICON_VALUE + 1 : 0;
	foreach ( $from .. $#DB_ID ) { $DB_NEW{ $DB_ID[$_] } = 1; }
    }

    $gBoardDbCached = 1;		# cached
}


###
## getBoardLastmod - ����Ǽ��Ĥκǽ�������������
#
# - SYNOPSIS
#	getBoardLastmod( $board );
#
# - ARGS
#	$board		�Ǽ���ID
#
# - DESCRIPTION
#	�Ǽ����ѤΥ�å�����DB�ե�����κǽ����������׻�����
#	���ηǼ��Ĥκǽ���������Ȥ����֤���
#
# - RETURN
#	UTC����ηв��ÿ�
#
sub getBoardLastmod
{
    local( $board ) = @_;

    # 86400 = 24 * 60 * 60
    $^T - ( -M &GetPath( $board, $DB_FILE_NAME )) * 86400;
}


###
## getNofMsg - ��å��������μ���
#
# - SYNOPSIS
#	getNofMsg();
#
# - DESCRIPTION
#	����å���������������롥����Ѥߥ�å������Ͽ�������ʤ���
#
# - RETURN
#	��å�������
#
sub getNofMsg
{
    $#DB_ID;
}


###
## getMsgId - ��å�����ID�μ���
#
# - SYNOPSIS
#	getMsgId( $num );
#
# - ARGS
#	$num	��å������ֹ�
#
# - DESCRIPTION
#	��å������ֹ椫���å�����ID��������롥
#
# - RETURN
#	��å�����ID
#
sub getMsgId
{
    $DB_ID[ $_[0] ];
}


###
## getMsgNewP - ��å����������������ݤ�
#
# - SYNOPSIS
#	getMsgNewP( $id );
#
# - ARGS
#	$id	��å�����ID
#
# - DESCRIPTION
#	��å����������������ݤ����֤���
#
# - RETURN
#	1 if true, 0 if false.
#
sub getMsgNewP
{
    $DB_NEW{ $_[0] };
}


###
## getMsgInfo - ��å���������μ���
#
# - SYNOPSIS
#	getMsgInfo( $id );
#
# - ARGS
#	$id	��å�����ID
#
# - DESCRIPTION
#	��å����������������롥
#
# - RETURN
#	��å���������Υꥹ��
#		�ƥ�å�����ID�Υꥹ��(��,�׶��ڤ�)
#		���Υ�å������˥�ץ饤������å�������ID�Υꥹ��(��,�׶��ڤ�)
#		��ƻ��֡�UTC����ηв��ÿ���
#		Subject
#		��������ID
#		��ƥۥ���
#		��Ƽ�̾
#		��Ƽ�E-Mail
#		��Ƽ�URL
#		��ץ饤�����ä�������ƼԤ˥ᥤ������뤫�ݤ�
#
sub GetArticlesInfo { &getMsgInfo; }
sub getMsgInfo
{
    local( $id ) = @_;
    ( $DB_FID{$id}, $DB_AIDS{$id}, $DB_DATE{$id}, $DB_TITLE{$id}, $DB_ICON{$id}, $DB_REMOTEHOST{$id}, $DB_NAME{$id}, $DB_EMAIL{$id}, $DB_URL{$id}, $DB_FMAIL{$id} );
}


###
## getMsgParents - ��å������ƾ���μ���
## getMsgDaughters - ��å�����̼����μ���
## getMsgSubject - ��å����������ȥ�μ���
## getMsgIcon - ��å�������������μ���
## setMsgParents - ��å������ƾ��������
## setMsgDaughters - ��å�����̼���������
#
# - SYNOPSIS
#	getMsgParents( $id );
#	getMsgDaughters( $id );
#	getMsgSubject( $id );
#	getMsgIcon( $id );
#
#	setMsgParents( $id, $value );
#	setMsgDaughters( $id, $value );
#
# - ARGS
#	$id	��å�����ID
#	$value	��å�����ID�Υꥹ�ȡʡ�,�׶��ڤ��
#
# - DESCRIPTION
#	��å�������/̼�����������롥
#
# - RETURN
#	get*
#		�ƥ�å�����ID�Υꥹ�ȡʡ�,�׶��ڤ��
#		̼��å�����ID�Υꥹ�ȡʡ�,�׶��ڤ��
#	set*
#		�ʤ�
#
sub getMsgParents { $DB_FID{ $_[0] }; }
sub getMsgDaughters { $DB_AIDS{ $_[0] }; }
sub getMsgSubject { $DB_TITLE{ $_[0] }; }
sub getMsgIcon { $DB_ICON{ $_[0] }; }

sub setMsgParents { $DB_FID{ $_[0] } = $_[1]; }
sub setMsgDaughters { $DB_AIDS{ $_[0] } = $_[1]; }


###
## getMsgAuthor - ��å�������ƼԾ���μ���
#
# - SYNOPSIS
#	getMsgAuthor( $id );
#
# - ARGS
#	$id	��å�����ID
#
# - DESCRIPTION
#	��å�������ƼԾ����������롥
#
# - RETURN
#	��å�������ƼԾ���Υꥹ��
#		��Ƽ�̾
#		��Ƽ�E-Mail
#		��Ƽ�URL
#		��ץ饤�����ä�������ƼԤ˥ᥤ������뤫�ݤ�
#		��ƥۥ���
#
sub getMsgAuthor
{
    ( $DB_NAME{ $_[0] }, $DB_EMAIL{ $_[0] }, $DB_URL{ $_[0] }, $DB_FMAIL{ $_[0] }, $DB_REMOTEHOST{ $_[0] } );
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
#	$MailRelay	�ɲä���������ᥤ��Ȥ���ή�����ɤ���
#
# - DESCRIPTION
#	����DB�˵������ɲä��롥
#
sub AddDBFile
{
    local( $Id, $Board, $Fid, $InputDate, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail, $MailRelay ) = @_;

    local( $dId, $dFid, $dAids, $dInputDate, $dSubject, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail, $mdName, $mdEmail, $mdInputDate, $mdSubject, $mdIcon, $mdId, $FidList, @FollowMailTo, @FFid );

    # �ᥤ�������Ѥˡ���ץ饤���Υ�ץ饤�������äƤ���
    if ( $Fid ne '' )
    {
	@FFid = split( /,/, &getMsgParents( $Fid ));
    }

    $FidList = $Fid;

    local( $File ) = &GetPath( $Board, $DB_FILE_NAME );
    local( $TmpFile ) = &GetPath( $Board, "$DB_FILE_NAME.$TMPFILE_SUFFIX$$" );
    local( $dbLine );
    open( DBTMP, ">$TmpFile" ) || &Fatal( 1, $TmpFile );
    open( DB, "<$File" ) || &Fatal( 1, $File );
    while ( <DB> )
    {
	if ( /^\#/o || /^$/o )
	{
	    print( DBTMP "$_" ) || &Fatal( 13, $TmpFile );
	    next;
	}

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

	    if ( $MailRelay && ( $SYS_MAIL & 2 ))
	    {
		# �ᥤ�������Τ���˥���å���
		$mdName = $dName;
		$mdEmail = $dEmail;
		$mdInputDate = $dInputDate;
		$mdSubject = $dSubject;
		$mdIcon = $dIcon;
		$mdId = $dId;
		push( @FollowMailTo, $dEmail ) if $dFmail && $dEmail;
	    }
	}

	# DB�˽񤭲ä���
	&GenTSV( *dbLine, ( $dId, $dFid, $dAids, $dInputDate, $dSubject, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail ));
	print( DBTMP "$dbLine\n" ) || &Fatal( 13, $TmpFile );

	# ��ץ饤���Υ�ץ饤�������ĥᥤ��������ɬ�פ�����С��������¸
	if ( $MailRelay && ( $SYS_MAIL & 2 ) && @FFid && $dFmail && $dEmail && ( grep( /^$dId$/, @FFid )) && ( !grep( /^$dEmail$/, @FollowMailTo )))
	{
	    push( @FollowMailTo, $dEmail );
	}
    }

    # �����������Υǡ�����񤭲ä��롥
    &GenTSV( *dbLine, ( $Id, $FidList, '', $InputDate, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail ));
    print( DBTMP "$dbLine\n" ) || &Fatal( 13, $TmpFile );

    # close Files.
    close DB;
    close DBTMP || &Fatal( 13, $TmpFile );

    # DB�򹹿�����
    rename( $TmpFile, $File ) || &Fatal( 14, "$TmpFile -&gt; $File" );

    # ɬ�פʤ���Ƥ����ä����Ȥ�ᥤ�뤹��
    if ( $MailRelay && $SYS_MAIL & 1 )
    {
	local( @ArriveMailTo );
	&GetArriveMailTo( 0, $Board, *ArriveMailTo );
	&ArriveMail( $Name, $Email, $InputDate, $Subject, $Icon, $Id, @ArriveMailTo ) if @ArriveMailTo;
    }

    # ɬ�פʤ�ȿ�������ä����Ȥ�ᥤ�뤹��
    if ( $MailRelay && ( $SYS_MAIL & 2 ) && @FollowMailTo )
    {
	&FollowMail( $mdName, $mdEmail, $mdInputDate, $mdSubject, $mdIcon, $mdId, $Name, $Email, $InputDate, $Subject, $Icon, $Id, @FollowMailTo );
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
sub UpdateArticleDb
{
    local( $Board ) = @_;

    local( $dId, $dbLine );
    local( $File ) = &GetPath($Board, $DB_FILE_NAME);
    local( $TmpFile ) = &GetPath( $Board, "$DB_FILE_NAME.$TMPFILE_SUFFIX$$" );
    open( DBTMP, ">$TmpFile" ) || &Fatal( 1, $TmpFile );
    open( DB, "<$File" ) || &Fatal( 1, $File );
    while ( <DB> )
    {
	if ( /^\#/o || /^$/o )
	{
	    print( DBTMP "$_" ) || &Fatal( 13, $TmpFile );
	    next;
	}

	# Id����Ф�
	chop;
	( $dId = $_ ) =~ s/\t.*$//;

	# DB�˽񤭲ä���
	&GenTSV( *dbLine, ( $dId, $DB_FID{$dId}, $DB_AIDS{$dId}, $DB_DATE{$dId}, $DB_TITLE{$dId}, $DB_ICON{$dId}, $DB_REMOTEHOST{$dId}, $DB_NAME{$dId}, $DB_EMAIL{$dId}, $DB_URL{$dId}, $DB_FMAIL{$dId} ));
	print( DBTMP "$dbLine\n" ) || &Fatal( 13, $TmpFile );
    }

    # close Files.
    close DB;
    close DBTMP || &Fatal( 13, $TmpFile );

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
sub DeleteArticleFromDbFile
{
    local( $Board, *Target ) = @_;

    local( $dId, $dbLine );
    local( $File ) = &GetPath( $Board, $DB_FILE_NAME );
    local( $TmpFile ) = &GetPath( $Board, "$DB_FILE_NAME.$TMPFILE_SUFFIX$$" );
    open( DBTMP, ">$TmpFile" ) || &Fatal( 1, $TmpFile );
    open( DB, "<$File" ) || &Fatal( 1, $File );
    while ( <DB> )
    {
	if ( /^\#/o || /^$/o )
	{
	    print( DBTMP "$_" ) || &Fatal( 13, $TmpFile );
	    next;
	}

	# Id����Ф�
	chop;
	( $dId = $_ ) =~ s/\t.*$//;

	# ���������ϥ����ȥ�����
	if ( grep( /^$dId$/, @Target ))
	{
	    print( DBTMP "#" ) || &Fatal( 13, $TmpFile );
	}

	&GenTSV( *dbLine, ( $dId, $DB_FID{$dId}, $DB_AIDS{$dId}, $DB_DATE{$dId}, $DB_TITLE{$dId}, $DB_ICON{$dId}, $DB_REMOTEHOST{$dId}, $DB_NAME{$dId}, $DB_EMAIL{$dId}, $DB_URL{$dId}, $DB_FMAIL{$dId} ));
	print( DBTMP "$dbLine\n" ) || &Fatal( 13, $TmpFile );
    }

    # close Files.
    close DB;
    close DBTMP || &Fatal( 13, $TmpFile );

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
sub ReOrderArticleDb
{
    local( $Board, $Id, *Move ) = @_;

    # ��Ƭ�ե饰
    local( $TopFlag ) = 1;

    local( $dId, $dbLine );
    local( $File ) = &GetPath( $Board, $DB_FILE_NAME );
    local( $TmpFile ) = &GetPath( $Board, "$DB_FILE_NAME.$TMPFILE_SUFFIX$$" );
    open( DBTMP, ">$TmpFile" ) || &Fatal( 1, $TmpFile );
    open( DB, "<$File" ) || &Fatal( 1, $File );
    while ( <DB> )
    {
	if ( /^\#/o || /^$/o )
	{
	    print( DBTMP "$_" ) || &Fatal( 13, $TmpFile );
	    next;
	}

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
		&GenTSV( *dbLine, ( $_, $DB_FID{$_}, $DB_AIDS{$_}, $DB_DATE{$_}, $DB_TITLE{$_}, $DB_ICON{$_}, $DB_REMOTEHOST{$_}, $DB_NAME{$_}, $DB_EMAIL{$_}, $DB_URL{$_}, $DB_FMAIL{$_} ));
		print( DBTMP "$dbLine\n" ) || &Fatal( 13, $TmpFile );
	    }
	}

	# ��ư�褬�����顤��˽񤭹���(���夬�塤�ξ��)
	if (( $SYS_BOTTOMTITLE == 0 ) && ( $dId eq $Id ))
	{
	    foreach ( @Move )
	    {
		&GenTSV( *dbLine, ( $_, $DB_FID{$_}, $DB_AIDS{$_}, $DB_DATE{$_}, $DB_TITLE{$_}, $DB_ICON{$_}, $DB_REMOTEHOST{$_}, $DB_NAME{$_}, $DB_EMAIL{$_}, $DB_URL{$_}, $DB_FMAIL{$_} ));
		print( DBTMP "$dbLine\n" ) || &Fatal( 13, $TmpFile );
	    }
	}

	# DB�˽񤭲ä���
	&GenTSV( *dbLine, ( $dId, $DB_FID{$dId}, $DB_AIDS{$dId}, $DB_DATE{$dId}, $DB_TITLE{$dId}, $DB_ICON{$dId}, $DB_REMOTEHOST{$dId}, $DB_NAME{$dId}, $DB_EMAIL{$dId}, $DB_URL{$dId}, $DB_FMAIL{$dId} ));
	print( DBTMP "$dbLine\n" ) || &Fatal( 13, $TmpFile );

	# ��ư�褬�����顤³���ƽ񤭹���(���夬�����ξ��)
	if (( $SYS_BOTTOMTITLE == 1 ) && ( $dId eq $Id ))
	{
	    foreach ( @Move )
	    {
		&GenTSV( *dbLine, ( $_, $DB_FID{$_}, $DB_AIDS{$_}, $DB_DATE{$_}, $DB_TITLE{$_}, $DB_ICON{$_}, $DB_REMOTEHOST{$_}, $DB_NAME{$_}, $DB_EMAIL{$_}, $DB_URL{$_}, $DB_FMAIL{$_} ));
		print( DBTMP "$dbLine\n" ) || &Fatal( 13, $TmpFile );
	    }
	}
    }

    # ��Ƭ�ˤ�����ν���(���夬�塤�ξ��)
    if (( $Id eq '' ) && ( $SYS_BOTTOMTITLE == 0 ))
    {
	foreach ( @Move )
	{
	    &GenTSV( *dbLine, ( $_, $DB_FID{$_}, $DB_AIDS{$_}, $DB_DATE{$_}, $DB_TITLE{$_}, $DB_ICON{$_}, $DB_REMOTEHOST{$_}, $DB_NAME{$_}, $DB_EMAIL{$_}, $DB_URL{$_}, $DB_FMAIL{$_} ));
	    print( DBTMP "$dbLine\n" ) || &Fatal( 13, $TmpFile );
	}
    }

    # close Files.
    close DB;
    close DBTMP || &Fatal( 13, $TmpFile );

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
sub MakeArticleFile
{
    local( $TextType, $Article, $Id, $Board ) = @_;

    local( $File ) = &GetArticleFileName( $Id, $Board );

    open( TMP, ">$File" ) || &Fatal( 1, $File );
    printf( TMP "<!-- Kb-System-Id: %s/%s -->\n", $KB_VERSION, $KB_RELEASE)
	|| &Fatal( 13, $File );
    print( TMP "$Article\n" ) || &Fatal( 13, $File );
    close TMP || &Fatal( 13, $File );
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
    local( $Board, *id, *artKey ) = @_;

    local( $ArticleNumFile ) = &GetPath( $Board, $ARTICLE_NUM_FILE_NAME );
    open( AID, "<$ArticleNumFile" ) || &Fatal( 1, $ArticleNumFile );
    chop( $id = <AID> );
    chop( $artKey = <AID> );
    close AID;
}


###
## WriteArticleId - �����ֹ�DB�ι���
#
# - SYNOPSIS
#	WriteArticleId($Id, $Board, $artKey);
#
# - ARGS
#	$Id		�����˽񤭹��൭���ֹ�
#	$Board		�Ǽ���ID
#	$artKey		¿�Ž񤭹����ɻ��ѥ���
#
# - DESCRIPTION
#	�����ֹ�DB�ι���
#
sub WriteArticleId
{
    local( $Id, $Board, $artKey ) = @_;

    local( $File, $TmpFile, $OldArticleId );
    
    # �����Τ����˸Ť����ͤ��㤤! (��������ʤ���OK)
    $OldArticleId = &GetNewArticleId( $Board );
    &Fatal( 10, '' ) if (( $Id =~ /^\d+$/ ) && ( $Id < $OldArticleId ));

    $File = &GetPath( $Board, $ARTICLE_NUM_FILE_NAME );
    $TmpFile = &GetPath( $Board, "$ARTICLE_NUM_FILE_NAME.$TMPFILE_SUFFIX$$" );
    open( AID, ">$TmpFile" ) || &Fatal( 1, $TmpFile );
    print( AID "$Id\n" ) || &Fatal( 13, $TmpFile );
    print( AID "$artKey\n" ) || &Fatal( 13, $TmpFile );
    close AID || &Fatal( 13, $TmpFile );

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
sub UpdateArriveMailDb
{
    local( $Board, *ArriveMail ) = @_;

    local( $File ) = &GetPath( $Board, $ARRIVEMAIL_FILE_NAME );
    local( $TmpFile ) = &GetPath( $Board, $ARRIVEMAIL_FILE_NAME );
    open( DBTMP, ">$TmpFile" ) || &Fatal( 1, $TmpFile );
    local( $line );
    foreach ( @ArriveMail )
    {
	( $line = $_ ) =~ s/\s*$//o;
	print( DBTMP "$line\n" ) || &Fatal( 13, $TmpFile );
    }
    close DBTMP || &Fatal( 13, $TmpFile );
    rename( $TmpFile, $File ) || &Fatal( 14, "$TmpFile -&gt; $File" );
}


###
## GetHeaderDb - �Ǽ����̥إå�DB�����ɤ߹���
#
# - SYNOPSIS
#	GetHeaderDb( $board, *header );
#
# - ARGS
#	$board		�Ǽ���ID
#	*header		�إå�ʸ����
#
sub GetHeaderDb
{
    local( $board, *header ) = @_;

    local( $file ) = &GetPath( $board, $HEADER_FILE_NAME );
    # �ե����뤬�ʤ�����Τޤ�
    open( DB, "<$file" ) || return;
    while ( <DB> )
    {
	$header .= $_;
    }
    close DB;
}


###
## UpdateHeaderDb - �Ǽ����̥إå�DB��������
#
# - SYNOPSIS
#	UpdateHeaderDb( $board, *header );
#
# - ARGS
#	$board		�Ǽ���ID
#	*header		�إå�ʸ����
#
sub UpdateHeaderDb
{
    local( $board, *header ) = @_;

    local( $file ) = &GetPath( $board, $HEADER_FILE_NAME );
    local( $tmpFile ) = &GetPath( $board, $HEADER_FILE_NAME );
    open( DBTMP, ">$tmpFile" ) || &Fatal( 1, $tmpFile );
    print( DBTMP $header ) || &Fatal( 13, $tmpFile );
    close DBTMP || &Fatal( 13, $tmpFile );
    rename( $tmpFile, $file ) || &Fatal( 14, "$tmpFile -&gt; $file" );
}


###
## AddBoardDb - �Ǽ���DB�ؤ��ɲ�
#
# - SYNOPSIS
#	AddBoardDb( $name, $intro, $conf, *arriveMail, *header );
#
# - ARGS
#	$name		�Ǽ���̾
#	$intro		�Ҳ�ʸ
#	$conf		�Ǽ��ĸ�ͭ����ե���������Ѥ��뤫�ݤ�(0/1)
#	*arriveMail	��ư�����ᥤ��Υᥤ����ꥹ��
#	*header		�إå�ʸ����
#
# - DESCRIPTION
#	�Ǽ���DB�˷Ǽ��Ĥ��ɲä��롥
#
# - RETURN
#	���������Ǽ��Ĥ�ID
#
sub AddBoardDb
{
    local( $name, $intro, $conf, *arriveMail, *header ) = @_;

    # �Ǽ��ĥǥ��쥯�ȥ�κ���
    mkdir( $name, 0777 ) || &Fatal( 1, $name );

    local( $src, $dest );

    # ����DB�κ����ʥ��ԡ���
    $src = &GetPath( $BOARDSRC_DIR, $DB_FILE_NAME );
    $dest = &GetPath( $name, $DB_FILE_NAME );
    &CopyDb( $src, $dest ) || &Fatal( 20, "$src -&gt; $dest" );

    # ������DB�κ����ʥ��ԡ���
    $src = &GetPath( $BOARDSRC_DIR, $ARTICLE_NUM_FILE_NAME );
    $dest = &GetPath( $name, $ARTICLE_NUM_FILE_NAME );
    &CopyDb( $src, $dest ) || &Fatal( 20, "$src -&gt; $dest" );

    # ��ư�����ᥤ��DB�κ���
    &UpdateArriveMailDb( $name, *arriveMail );

    # �إå��ե�����κ���
    &UpdateHeaderDb( $name, *header );

    # �Ǹ�ˡ��Ǽ���DB�򹹿�����
    local( $file ) = &GetPath( $SYS_DIR, $BOARD_FILE );
    local( $tmpFile ) = &GetPath( $SYS_DIR, "$BOARD_FILE.$TMPFILE_SUFFIX$$" );
    local( $dbLine );
    open( DBTMP, ">$tmpFile" ) || &Fatal( 1, $tmpFile );
    open( DB, "<$file" ) || &Fatal( 1, $file );

    local( $dName, $dIntro, $dConf );
    while ( <DB> )
    {
	if ( /^\#/o || /^$/o )
	{
	    print( DBTMP "$_" ) || &Fatal( 13, $tmpFile );
	    next;
	}
	chop;

	( $dName, $dIntro, $dConf ) = split( /\t/, $_, 3 );
	&Fatal( 51, $name ) if ( $name eq $dName );

	&GenTSV( *dbLine, ( $dName, $dIntro, $dConf ));
	print( DBTMP "$dbLine\n" ) || &Fatal( 13, $tmpFile );
    }

    # �����������Υǡ�����񤭲ä��롥
    &GenTSV( *dbLine, ( $name, $intro, $conf ));
    print( DBTMP "$dbLine\n" ) || &Fatal( 13, $tmpFile );

    # close Files.
    close DB;
    close DBTMP || &Fatal( 13, $tmpFile );

    rename( $tmpFile, $file ) || &Fatal( 14, "$tmpFile -&gt; $file" );
}


###
## UpdateBoardDb - �Ǽ���DB�ι���
#
# - SYNOPSIS
#	UpdateBoardDb( $board, $valid, $intro, $conf, *arriveMail, *header );
#
# - ARGS
#	$board		�Ǽ���ID
#	$valid		���ηǼ��Ĥ����Ѥ��뤫�ݤ�
#	$intro		�Ǽ���̾
#	$conf		����ե�������ɤफ�ݤ�
#	*arriveMail	��ư�����ᥤ��Υᥤ����ꥹ��
#	*header		�إå�ʸ����
#
# - DESCRIPTION
#	�Ǽ���DB�򹹿����롥
#
sub UpdateBoardDb
{
    local( $name, $valid, $intro, $conf, *arriveMail, *header ) = @_;

    local( $file ) = &GetPath( $SYS_DIR, $BOARD_FILE );
    local( $tmpFile ) = &GetPath( $SYS_DIR, "$BOARD_FILE.$TMPFILE_SUFFIX$$" );
    open( DBTMP, ">$tmpFile" ) || &Fatal( 1, $tmpFile );
    open( DB, "<$file" ) || &Fatal( 1, $file );

    local( $dbLine, $dName, $dIntro, $dConf );
    while ( <DB> ) {

	if ( /^\#/o || /^$/o )
	{
	    print( DBTMP "$_" ) || &Fatal( 13, $tmpFile );
	    next;
	}
	chop;

	( $dName, $dIntro, $dConf ) = split( /\t/, $_, 3 );
	if ( $name eq $dName )
	{
	    $dName = '#' . $dName unless $valid;
	    $dIntro = $intro;
	    $dConf = $conf;
	}

	# DB�˽񤭲ä���
	&GenTSV( *dbLine, ( $dName, $dIntro, $dConf ));
	print( DBTMP "$dbLine\n" ) || &Fatal( 13, $tmpFile );
    }

    # close Files.
    close DB;
    close DBTMP || &Fatal( 13, $tmpFile );

    # DB�򹹿�����
    rename( $tmpFile, $file ) || &Fatal( 14, "$tmpFile -&gt; $file" );

    # ��ư�����ᥤ��DB�⹹�����롥
    &UpdateArriveMailDb( $BOARD, *arriveMail );

    # �إå��ե�����⹹�����롥
    &UpdateHeaderDb( $name, *header );
}


###
## GetAllBoardInfo - �Ǽ���DB�����ɤ߹���
#
# - SYNOPSIS
#	GetAllBoardInfo( *board, *boardName, *boardInfo );
#
# - ARGS
#	*board		�Ǽ���ID������Υ�ե����
#	*boardName	�Ǽ���ID-�Ǽ���̾��Ϣ������Υ�ե����
#	*boardInfo	�Ǽ���ID-�Ǽ��ľ����Ϣ������Υ�ե����
#
# - DESCRIPTION
#	�Ǽ���DB���顤�Ǽ��ľ�����äƤ��롥
#
sub GetAllBoardInfo
{
    local( *board, *boardName, *boardInfo ) = @_;

    local( $bId, $bName, $bInfo );
    local( $dbFile ) = &GetPath( $SYS_DIR, $BOARD_FILE );
    open( DB, "<$dbFile" ) || &Fatal( 1, $dbFile );
    while ( <DB> )
    {
	next if ( /^\#/o || /^$/o );
	chop;
	( $bId, $bName, $bInfo ) = split( /\t/, $_, 4 );
	push( @board, $bId );
	$boardName{ $bId } = $bName;
	$boardInfo{ $bId } = $bInfo;
    }
    close DB;
}


###
## GetBoardInfo - �Ǽ���DB���ɤ߹���
#
# - SYNOPSIS
#	GetBoardInfo( $board );
#
# - ARGS
#	$board		�Ǽ���ID
#
# - DESCRIPTION
#	�Ǽ���DB���顤�Ǽ��ľ�����äƤ��롥
#
# - RETURN
#	�Ǽ���̾����ͭ�����̵ͭ���Υꥹ��
#
sub GetBoardInfo
{
    local( $board ) = @_;

    local( $dBoard, $dBoardName, $dBoardConf );

    local( $dbFile ) = &GetPath( $SYS_DIR, $BOARD_FILE );
    open( DB, "<$dbFile" ) || &Fatal( 1, $dbFile );
    while ( <DB> )
    {
	next if ( /^\#/o || /^$/o );
	chop;
	( $dBoard, $dBoardName, $dBoardConf ) = split( /\t/, $_, 4 );
	if ( $board eq $dBoard )
	{
	    close DB;
	    return( $dBoardName, $dBoardConf );
	}
    }
    close DB;

    &Fatal( 11, $board );
}


###
## CacheIconDb - ��������DB�����ɤ߹���
#
# - SYNOPSIS
#	CacheIconDb($board);
#
# - ARGS
#	$board		�Ǽ���ID
#
# - DESCRIPTION
#	��������DB���ɤ߹����Ϣ�������������ࡥ
#	����ѿ���@ICON_TITLE��%ICON_FILE��%ICON_HELP���˲����롥
#
sub CacheIconDb
{
    local( $board ) = @_;
    local( $fileName, $title, $help, $type );

    @ICON_TITLE = %ICON_FILE = %ICON_HELP = %ICON_TYPE = ();
    open( ICON, &GetIconPath( "$board.$ICONDEF_POSTFIX" ))
	|| ( open( ICON, &GetIconPath( "$DEFAULT_ICONDEF" ))
	    || &Fatal( 1, &GetIconPath( "$DEFAULT_ICONDEF" )));
    while ( <ICON> )
    {
	next if ( /^\#/o || /^$/o );
	chop;
	( $fileName, $title, $help, $type ) = split( /\t/, $_, 4 );

	push( @ICON_TITLE, $title );
	$ICON_FILE{$title} = $fileName;
	$ICON_HELP{$title} = $help;
	$ICON_TYPE{$title} = $type || 'article';
    }
    close ICON;
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
## GetStyleSheetURL - �������륷���ȥե������URL�μ���
#
# - SYNOPSIS
#	&GetStyleSheetURL( $name );
#
# - ARGS
#	$name		�������륷���ȥե������̾��
#
# - DESCRIPTION
#	�������륷���ȥե������URL����Ф���
#
# - RETURN
#	URL��ɽ��ʸ����
#
sub GetStyleSheetURL
{
    local( $name ) = @_;
    $KB_RESOURCE_URL? "$KB_RESOURCE_URL$RESOURCE_STYLE/$name" : "$RESOURCE_STYLE/$name";
}


###
## GetIconURL - ��������gif��URL�μ���
#
# - SYNOPSIS
#	GetIconURL( $file );
#
# - ARGS
#	$file		��������gif�ե�����̾
#
# - DESCRIPTION
#	��������gif�ե������URL̾����Ф���
#
# - RETURN
#	URL��ɽ��ʸ����
#
sub GetIconURL
{
    local( $file ) = @_;
    $KB_RESOURCE_URL? "$KB_RESOURCE_URL$RESOURCE_ICON/$file" : "$RESOURCE_ICON/$file";
}


###
## GetIconUrlFromTitle - ��������gif��URL�μ���
#
# - SYNOPSIS
#	GetIconUrlFromTitle( $icon );
#
# - ARGS
#	$icon		��������ID
#
# - DESCRIPTION
#	��������ID���顤���Υ���������б�����gif�ե������URL�������
#	���奢������⵭���������󰷤���
#
# - RETURN
#	URL��ɽ��ʸ����
#
sub GetIconUrlFromTitle
{
    local( $icon ) = @_;
    return $ICON_NEW if ( $icon eq $H_NEWARTICLE );

    # check
    return '' unless $ICON_FILE{ $icon };

    # return
    &GetIconURL( $ICON_FILE{ $icon } );
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

    local( $SupersedeId, $dId, $dFid, $dAids, $dInputDate, $dSubject, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail );
    
    # initial version��1�ǡ�1���������Ƥ�����1��2����9��10��11����
    # later version��DB���ɬ����younger version���Ⲽ�˽и����롥
    # ���ʤ��10_2��10��10_1�ϡ�10_1��10_2��10�ν���¤֤�ΤȤ��롥
    $SupersedeId = 1;

    local( $dbLine );
    local( $File ) = &GetPath( $Board, $DB_FILE_NAME );
    local( $TmpFile ) = &GetPath( $Board, "$DB_FILE_NAME.$TMPFILE_SUFFIX$$" );
    open( DBTMP, ">$TmpFile" ) || &Fatal( 1, $TmpFile );
    open( DB, "<$File" ) || &Fatal( 1, $File );
    while ( <DB> )
    {
	if ( /^\#/o || /^$/o )
	{
	    print( DBTMP "$_" ) || &Fatal( 13, $TmpFile );
	    next;
	}

	chop;

	( $dId, $dFid, $dAids, $dInputDate, $dSubject, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail ) = split( /\t/, $_ );

	# later version�����Ĥ��ä��顤version�����ɤߤ��Ƥ�����
	if ( "$dId" eq ( sprintf( "#-%s_%s", $Id, $SupersedeId )))
	{
	    $SupersedeId++;
	}

	# ���������κǿ��Ǥ����Ĥ��ä��顤
	if ( $dId eq $Id )
	{
	    # aging���Ƥ��ޤ�
	    &GenTSV( *dbLine, ( sprintf( "-%s_%s", $dId, $SupersedeId ), $dFid, $dAids, $dInputDate, $dSubject, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail ));
	    print( DBTMP "#$dbLine\n" ) || &Fatal( 13, $TmpFile );

	    # ³���ƿ�����������񤭲ä���
	    &GenTSV( *dbLine, ( $Id, $dFid, $dAids, $InputDate, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail ));
	    print( DBTMP "$dbLine\n" ) || &Fatal( 13, $TmpFile );
	}
	else
	{
	    # DB�˽񤭲ä���
	    print( DBTMP "$_\n" ) || &Fatal( 13, $TmpFile );
	}
    }

    # close Files.
    close DB;
    close DBTMP || &Fatal( 13, $TmpFile );

    # DB�򹹿�����
    rename( $TmpFile, $File ) || &Fatal( 14, "$TmpFile -&gt; $File" );

    # �֤�
    $SupersedeId;
}
