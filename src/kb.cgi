#!/usr/local/bin/perl


# ���Υե�������ѹ��Ϻ���2�սꡤ����4�ս�Ǥ��ʴĶ�����Ǥ��ˡ�


# 1. ���Υե��������Ƭ�ԡʢ��ˤǡ�Perl�Υѥ�����ꤷ�ޤ���
#    ��#!�פ�³���ƻ��ꤷ�Ƥ���������

# 2. kbdata�ǥ��쥯�ȥ�Υե�ѥ�����ꤷ�Ƥ���������URL�ǤϤʤ����ѥ��Ǥ��ˡ�
#    �֥饦�����饢��������ǽ�ʥǥ��쥯�ȥ�Ǥʤ��Ƥ⤫�ޤ��ޤ���
#
$KBDIR_PATH = '/home/achilles/nakahiro/cvs_work/KB/tst/';
# $KBDIR_PATH = '/home/nahi/kbdata/';
# $KBDIR_PATH = 'd:\securedata\kbdata\';	# WinNT/Win9x�ξ��
# $KBDIR_PATH = 'foo:bar:kb:';			# Mac�ξ��?

# 3. �����Ф�ư���Ƥ���ޥ���Win95/Mac�ξ�硤
#    $PC��1�����ꤷ�Ƥ��������������Ǥʤ���硤������������פǤ���
#
$PC = 0;	# for UNIX / WinNT
# $PC = 1;	# for Win95 / Mac

# 4. �������󤪤�ӥ������륷���ȥե�����򡤤��Υե�������̤Υǥ��쥯�ȥ��
#    �֤����ϡ������̥ǥ��쥯�ȥ��URL����ꤷ�Ƥ��������ʥѥ��ǤϤʤ���
#    URL�Ǥ��ˡ����ꤹ��URL�ϡ��֥饦�����饢��������ǽ�Ǥʤ���Ф����ޤ���
#    �ܥե������Ʊ���ǥ��쥯�ȥ��icon��style�ǥ��쥯�ȥ���֤����ϡ�
#    �ä˻��ꤷ�ʤ��Ƥ⤫�ޤ��ޤ���ʤ��Τޤ޽񤭴����ʤ��ƹ����ޤ���ˡ�
#
#    ���ꤷ��URL�ʲ����֤���Ƥ��롤
#      icon/*����������ե�����Ȥ��ơ�
#      style/kbStyle.css���������륷���ȥե�����Ȥ��ơ�
#    ���줾�컲�Ȥ���ޤ���
#
# $KB_RESOURCE_URL = '/~nahi/kb/';


# �ʲ��Ͻ񤭴�����ɬ�פϤ���ޤ���


######################################################################


# $Id: kb.cgi,v 5.73 2000-05-05 06:01:37 nakahiro Exp $

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
$KB_RELEASE = '7.0';		# release
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
$RESOURCE_IMG = 'img';			# ���᡼���ǥ��쥯�ȥ�
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
$H_TOP = '�ǿ�';
$H_BOTTOM = '��Ƭ';
$H_UP = '��';
$H_DOWN = '��';
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
$ICON_UP = &getIconURL( 'org_tlist.gif' );		# ���
$ICON_UP_X = &getIconURL( 'org_tlist_x.gif' );		# ���
$ICON_PREV = &getIconURL( 'org_prev.gif' );		# ����
$ICON_PREV_X = &getIconURL( 'org_prev_x.gif' );		# ����
$ICON_NEXT = &getIconURL( 'org_next.gif' );		# ����
$ICON_NEXT_X = &getIconURL( 'org_next_x.gif' );		# ����
$ICON_DOWN = &getIconURL( 'org_thread.gif' );		# ����
$ICON_DOWN_X = &getIconURL( 'org_thread_x.gif' );	# ����
$ICON_FOLLOW = &getIconURL( 'org_follow.gif' );		# ��ץ饤
$ICON_FOLLOW_X = &getIconURL( 'org_follow_x.gif' );	# ��ץ饤
$ICON_QUOTE = &getIconURL( 'org_quote.gif' );		# ���Ѥ��ƥ�ץ饤
$ICON_QUOTE_X = &getIconURL( 'org_quote_x.gif' );	# ���Ѥ��ƥ�ץ饤
$ICON_SUPERSEDE = &getIconURL( 'org_supersede.gif' );	# ����
$ICON_SUPERSEDE_X = &getIconURL( 'org_supersede_x.gif' );	# ����
$ICON_DELETE = &getIconURL( 'org_delete.gif' );		# ���
$ICON_DELETE_X = &getIconURL( 'org_delete_x.gif' );	# ���
$ICON_HELP = &getIconURL( 'org_help.gif' );		# �إ��
$ICON_NEW = &getIconURL( 'org_listnew.gif' );		# ����

# ���ԥ�������ʿ������
$HTML_BR = "<br />\n";
$HTML_HR = "<hr />\n";

# �����륫���󥿡��ե饰
$gLinkNum = 0;
$gTabIndex = 0;

$gDumpedHTTPHeader = 0;

# �����ʥ�ϥ�ɥ�
$SIG{'QUIT'} = 'IGNORE';
$SIG{'INT'} = $SIG{'HUP'} = $SIG{'TERM'} = $SIG{'TSTP'} = 'doKill';


######################################################################


###
## maiN - �ᥤ��֥�å�
#
# - SYNOPSIS
#	kb.cgi
#
# - DESCRIPTION
#	��ư���˰��٤������Ȥ���롥
#	�������Ϥʤ������Ķ��ѿ�QUERY_STRING��REQUEST_METHOD��
#	�⤷����ɸ�����Ϸ�ͳ���ͤ��Ϥ��ʤ��ȡ�������ư��ʤ���
#
&kbLog( $kinologue'SEV_INFO, 'Exec started.' );
MAIN:
{
    &cgi'decode();

    if ( $kinologue'SEV_THRESHOLD == $kinologue'SEV_DEBUG )
    {
	local( $key, $value, $msg );
	while (( $key, $value ) = each %cgi'TAGS )
	{
	    $msg .= '&' if $msg;
	    $msg .= "$key=$value";
	}
	&kbLog( $kinologue'SEV_DEBUG, "Command executed with ... " . $msg );
    }

    # HEAD�ꥯ�����Ȥ��Ф������̽���
    if ( $ENV{ 'REQUEST_METHOD' } eq 'HEAD' )
    {
	local( $modTime ) = 0;
	if ( &cgi'tag( 'b' ) ne '' )
	{
	    $modTime = &getBoardLastmod( scalar( &cgi'tag( 'b' )));
	}
	&cgi'header( 1, $modTime, 0, (), 0 );
	last;
    }

    local( $c ) = &cgi'tag( 'c' );
    local( $com ) = &cgi'tag( 'com' );
    local( $s ) = &cgi'tag( 's' );
    $BOARD = &cgi'tag( 'b' );
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

    # ��å����ʤ��Ǥ�����?
    &cacheBoard();

    if ( $BOARD )
    {
	$BOARD_ESC = &uriEscape( $BOARD );	# ����Ѥ�escape
	$BOARDNAME = &getBoardName( $BOARD );
	$LOCK_FILE_B = $LOCK_FILE . ".$BOARD";

	# �Ǽ��ĸ�ͭ���åƥ��󥰤��ɤ߹���
	if ( &getBoardInfo( $BOARD ))
	{
	    local( $boardConfFile ) = &getPath( $BOARD, $CONF_FILE_NAME );
	    require( $boardConfFile ) if ( -s "$boardConfFile" );
	}

	# ��������DB���ɤ߹����R7�ʹߡ�
	&cacheBoardIcon( $BOARD ) if $SYS_ICON;
    }

    # ���Ƥ�require������ä����ȡ�����

    # ǧ�ھ���ν����
    $cgiauth'GUEST = $GUEST;
    $cgiauth'ADMIN = $ADMIN;
    $USER_AUTH_FILE = &getPath( $SYS_DIR, $USER_FILE );

    # ���������ƥ����������
    $SYS_EXPAND = $SYS_EXPAND && ( $SYS_THREAD_FORMAT != 2 );
    $POLICY = $GUEST_POLICY;	# Policy by default.

    if ( $SYS_AUTH )
    {
	$SYS_AUTH_DEFAULT = $SYS_AUTH;
	$SYS_AUTH = 3 if ( &cgi'tag( 'kinoA' ) == 3 );
	if ( $c eq 'lo' )
	{
	    # ������
	    &uiLogin();
	    last;
	}
	elsif ( $c eq 'ue' )
	{
	    # �桼��������Ͽ
	    &uiUserEntry();
	    last;
	}
	elsif ( $c eq 'uex' )
	{
	    # �桼��������Ͽ�»�
	    &uiUserEntryExec();
	    last;
	}

	$cgiauth'AUTH_TYPE = $SYS_AUTH;
	&cgi'cookie() if ( $SYS_AUTH == 1 );
	    
	local( $err, @userInfo );
	( $err, $UNAME, $PASSWD, @userInfo ) = &cgiauth'checkUser( $USER_AUTH_FILE );
	    
	if ( $err == 3 )
	{
	    # �桼��̾���ߤĤ���ʤ�
	    # ������41�����ɥ������ƥ�ͥ��
	    &fatal( 40, scalar( &cgi'tag( 'kinoU' )));
	}
	elsif ( $err == 4 )
	{
	    # �ѥ���ɤ��ְ�äƤ���
	    &fatal( 40, '' );
	}
	elsif ( $err == 9 )
	{
	    if ( $c eq 'acx' )
	    {
		# �����ԥѥ�����ѹ��μ»�
		&uiAdminConfigExec();
		last;
	    }
	    # �����ԥѥ���ɤ����ξ�硤�桼��������԰������Ƥ��顥����
	    $cgiauth'UID = $UNAME;
	    $cgiauth'PASSWD = $PASSWD;

	    # �����ԥѥ�����ѹ�
	    &uiAdminConfig();
	    last;
	}
	elsif ( $err != 0 )
	{
	    # not reached...
	    &fatal( 998, "Must not reach here(MAIN: $err)." );
	}
	    
	# ǧ������
	$UNAME_ESC = &uriEscape( $UNAME ) if ( $SYS_AUTH == 3 );
	$UMAIL = $userInfo[2];
	$UURL = $userInfo[3];

	# user policy�η���
	#   1 ... �ɤ�
	#   2 ... ��
	#   4 ... ��Ͽ�ʥ桼������򥵡��Ф˻Ĥ���
	#   8 ... ����
	if ( &isUser( $ADMIN ))
	{
	    # ������
	    $POLICY = 1 + 2 + 4 + 8;
	}
	elsif ( !&isUser( $GUEST ))
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
	    &uiShowArticle();
	    last;
	}
	elsif ( $c eq 't' )
	{
	    # �ե�������������ɽ����
	    &uiShowThread();
	    last;
	}
	elsif ( $c eq 'v' )
	{
	    # ����å��̥����ȥ����
	    &uiThreadTitle( 0 );
	    last;
	}
	elsif ( $c eq 'vt' )
	{
	    # ����å��̥����ȥ뤪��ӵ�������
	    &uiThreadArticle();
	    last;
	}
	elsif ( $c eq 'r' )
	{
	    # �񤭹��߽�˥�����
	    &uiSortTitle();
	    last;
	}
	elsif ( $c eq 'l' )
	{
	    # ������������񤭹��߽��ɽ��
	    &uiSortArticle();
	    last;
	}
	elsif ( $SYS_F_S && ( $c eq 's' ))
	{
	    # �����θ���
	    &uiSearchArticle();
	    last;
	}
	elsif ( $SYS_ICON && ( $c eq 'i' ))
	{
	    # ��������ɽ������
	    &uiShowIcon();
	    last;
	}
	elsif ( $c eq 'h' )
	{
	    # �إ�ײ���
	    &uiHelp();
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
	    &cgi'setTag( 'c', scalar( &cgi'tag( 'corig' )));
	    $c = &cgi'tag( 'c' );
	}

	if ( $c eq 'n' )
	{
	    # �������
	    &uiPostNewEntry( $varBack );
	    last;
	}
	elsif ( !$s && ( $c eq 'f' ))
	{
	    # ��ץ饤���
	    &uiPostReplyEntry( $varBack, 0 );
	    last;
	}
	elsif ( $c eq 'q' )
	{
	    # ���ѥ�ץ饤���
	    &uiPostReplyEntry( $varBack, 1 );
	    last;
	}
	elsif ( !$s && ( $c eq 'p' ) && ( $com ne 'x' ))
	{
	    # ��ƥץ�ӥ塼
	    &uiPostPreview( 0 );
	    last;
	}
	elsif ( !$s && ( $c eq 'p' ) && ( $com eq 'x' ))
	{
	    # ��Ͽ����̤�ɽ����ľ�ܡ�
	    &uiPostExec( 0 );
	    last;
	}
	elsif ( !$s && ( $c eq 'x' ) && ( $com eq 'x' ))
	{
	    # ��Ͽ����̤�ɽ���ʥץ�ӥ塼��ͳ��
	    &uiPostExec( 1 );
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
	    &uiUserConfig();
            last;
        }
        elsif ( $c eq 'ucx' )
        {
            # �桼����������μ»�
	    &uiUserConfigExec();
	    last;
        }
	elsif ( $s && ( $c eq 'f' ))
	{
	    # ��������
	    &uiSupersedeEntry( $varBack );
	    last;
	}
	elsif ( $s && ( $c eq 'p' ) && ( $com ne 'x' ))
	{
	    # ���������ץ�ӥ塼
	    &uiSupersedePreview( 0 );
	    last;
	}
	elsif ( $s && ( $c eq 'p' ) && ( $com eq 'x' ))
	{
	    # ���������»ܡ�ľ�ܡ�
	    &uiSupersedeExec( 0 );
	    last;
	}
	elsif ( $s && ( $c eq 'x' ) && ( $com eq 'x' ))
	{
	    # ���������»ܡʥץ�ӥ塼��ͳ��
	    &uiSupersedeExec( 1 );
	    last;
	}
        elsif ( $c eq 'dp' )
        {
	    # ����ץ�ӥ塼
	    &uiDeletePreview();
	    last;
        }
        elsif ( $c eq 'de' )
        {
	    # ����»�
            &uiDeleteExec( 0 );
	    last;
	}
        elsif ($c eq 'det' )
        {
	    # ����»ܡʥ�ץ饤���
            &uiDeleteExec( 1 );
	    last;
        }
    }

    # ������
    if ( $POLICY & 8 )
    {
	if ( $c eq 'ct' )
	{
	    &uiThreadTitle( 2 );
	    last;
	}
	elsif ( $c eq 'ce' )
	{
	    &uiThreadTitle( 3 );
	    last;
	}
	elsif ( $c eq 'mvt' )
	{
	    &uiThreadTitle( 4 );
	    last;
	}
	elsif ( $c eq 'mve' )
	{
	    &uiThreadTitle( 5 );
	    last;
	}
        elsif ( $c eq 'bc' )
        {
            # �Ǽ�������
	    &uiBoardConfig();
            last;
        }
        elsif ( $c eq 'bcx' )
        {
	    # �Ǽ�������μ»�
	    &uiBoardConfigExec();
	    last;
        }
        elsif ( $c eq 'be' )
        {
            # �Ǽ��Ŀ���
            &uiBoardEntry();
            last;
        }
        elsif ( $c eq 'bex' )
        {
	    # �Ǽ��Ŀ��ߤμ»�
	    &uiBoardEntryExec();
	    last;
        }
    }

    if ( $c eq 'bl' )
    {
	# �Ǽ��İ�����ɽ��
	&uiBoardList();
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
		do( &getPath( $UI_DIR, 'Post.pl' ));
		last;
	    }
	    elsif ( $c eq 'POST_IF' )
	    {
		*gVarBody = *body;
		$gVarForce = 0;
		do( &getPath( $UI_DIR, 'Post.pl' ));
		last;
	    }
	}
    }

    # �ɤΥ��ޥ�ɤǤ�ʤ������顼��
    &fatal( 99, $c );
}
&kbLog( $kinologue'SEV_INFO, 'Exec finished.' );
exit( 0 );


######################################################################
# �١�������ץ���ơ������


###
## doKill - �����ƥ�Υ���åȥ�����
#
# - SYNOPSIS
#	&doKill();
#
# - DESCRIPTION
#	ɬ�פʽ�����Ԥʤä��塤�����ƥ�Υ���åȥ������Ԥʤ���
#	��å��β������ӥ��ե�����ؤν񤭽Ф���Ԥʤ���
#
sub doKill
{
    local( $sig ) = @_;
    if ( !$PC )
    {
	&cgi'unlock_file( $LOCK_FILE );
	&cgi'unlock_file( $LOCK_FILE_B ) if $LOCK_FILE_B;
    }
    &kbLog( $kinologue'SEV_WARN, "Caught a SIG$sig - shutting down..." );
    exit( 1 );
}


###
## lockAll/unlockAll - �����ƥ�Υ�å�/�����å�
## lockBoard/unlockBoard - �Ǽ��ĤΥ�å�/�����å�
#
# - SYNOPSIS
#	&lockAll();
#	&unlockAll();
#	&lockBoard();
#	&unlockBoard();
#
# - DESCRIPTION
#	�����ƥ�/�Ǽ��Ĥ��å�/�����å����롥
#	��å��˻Ȥ��ե������$LOCK_FILE/$LOCK_FILE_B��
#
# - RETURN
#	�ʤ����������������Ԥ���Х��顼�ڡ����ء�
#
sub LockAll { &lockAll; }
sub lockAll
{
    local( $lockResult ) = $PC ? 1 : &cgi'lock_file( $LOCK_FILE );
    &fatal( 1001, '' ) if ( $lockResult == 2 );
    &fatal( 999, '' ) if ( $lockResult != 1 );
    &lockBoard() if $LOCK_FILE_B;
}

sub UnlockAll { &unlockAll; }
sub unlockAll
{
    &cgi'unlock_file( $LOCK_FILE ) unless $PC;
    &unlockBoard() if $LOCK_FILE_B;
}

sub LockBoard { &lockBoard; }
sub lockBoard
{
    local( $lockResult ) = $PC ? 1 : &cgi'lock_file( $LOCK_FILE_B );
    &fatal( 1001, '' ) if ( $lockResult == 2 );
    &fatal( 999, '' ) if ( $lockResult != 1 );
}

sub UnlockBoard { &unlockBoard; }
sub unlockBoard
{
    &cgi'unlock_file( $LOCK_FILE_B ) unless $PC;
}


###
## fatal - ���顼����
#
# - SYNOPSIS
#	&fatal( $errno, $errInfo );
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
sub fatal
{
    local( $errno, $errInfo ) = @_;

    local( $severity, $msg ) = &fatalStr( $errno, $errInfo );

    # �۾ｪλ�β�ǽ��������Τǡ��Ȥꤢ����lock�򳰤�
    # (��å��μ��Ԥλ��ʳ�)
    if ( !$PC && ( $errno != 999 ) && ( $errno != 1001 ))
    {
	&unlockAll();
    }

    # log a log(except logging failure).
    &kbLog( $severity, $msg ) if ( $errno != 1000 );
    &uiFatal( $msg );
    &kbLog( $kinologue'SEV_INFO, 'Exec finished.' ) if ( $errno != 1000 );
    exit( 0 );
}


###
## fatalStr - ���顼�����ɤ�������٤ȥ��顼��å����������
#        
# - SYNOPSIS
#	&fatalStr( $errno, $errInfo );
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
sub fatalStr
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
	$msg = "$H_PASSWD��ְ㤨�Ƥ��ޤ���? $H_FROM��$H_PASSWD���ǧ������äƤ��ľ���ƤߤƤ���������" . &linkP( "c=lo", "�桼������θƤӽФ�" . &tagAccessKey( 'L' ), 'L' );
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
	$msg .= "���Ѥ�����Ǥ��������Υڡ�����URL��" . $cgi'REQUEST_URI . "�ˡ����Υ�å�������ʸ�Υ��ԡ��ȡ����顼��������������" . &tagA( $MAINT, "mailto:$MAINT" ) . "�ޤǤ��Τ餻ĺ����Ƚ�����ޤ���";
    }

    return ( $severity, $msg );
}


###
## kbLog - ������
#
# - SYNOPSIS
#	&kbLog( $kinologue'severity, *msg );
#
# - ARGS
#	$kinologue'severity	severity id defined in kinologue.pl.
#	*msg			reference to msg string.
#
# - DESCRIPTION
#	log a log using kinologue.
#	exit program(not function) if failed to write log.
#
sub KbLog { &kbLog; }
sub kbLog
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
	    || &fatal( 1000, '' );
    }
}


######################################################################
# �桼�����󥿥ե���������ץ���ơ������


###
## htmlGen - HTML generator from source file
#
# - SYNOPSIS
#	&htmlGen( $source );
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

    local( $file ) = &getPath( $UI_DIR, $source );

    open( SRC, "<$file" ) || &fatal( 1, $file );

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
    &cgiauth'header( 0, 0, 1, $cookieExpire ) unless $gDumpedHTTPHeader;
    $gDumpedHTTPHeader = 1;
    &cgiprint'init();

    $gHgStr = '';

    # Workaround for MSIE 4.5(Macintosh IE).
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
			&fatal( 998, "$file : $@" );
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
    &cgiprint'cache( $gHgStr );

    &cgiprint'flush();
}


###
## �����󥪥����
#
sub uiLogin
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
    &fatal( 18, "$_[0]/LoginForm" ) if ( $_[0] ne 'Login.xml' );

    local( %tags, $msg );
    $msg = &tagLabel( $H_FROM, 'kinoU', 'N' ) . ': ' . &tagInputText( 'text', 'kinoU', '', $NAME_LENGTH ) . $HTML_BR;
    $msg .= &tagLabel( $H_PASSWD, 'kinoP', 'P' ) . ': ' . &tagInputText( 'password', 'kinoP', '', $PASSWD_LENGTH ) . $HTML_BR;
    if ( $SYS_AUTH_DEFAULT == 1 )
    {
	local( $contents );
	$contents = &tagInputRadio( 'kinoA_url', 'kinoA', '3', 0 ) . ":\n" .
	    &tagLabel( '���å���(HTTP-Cookies)��Ȥ鷺��ǧ�ڤ���', 'kinoA_url', 'U' ) . $HTML_BR;
	$contents .= &tagInputRadio( 'kinoA_cookies', 'kinoA', '1', 1 ) . "\n" .
	    &tagLabel( '���å�����ȤäƤ��Υ֥饦���˾����Ф�������', 'kinoA_cookies', 'C' ) . $HTML_BR;
	$msg .= &tagFieldset( "���å���:$HTML_BR", $contents );
    }

    %tags = ( 'c', 'bl', 'kinoT', 'plain' );
    &dumpForm( *tags, '�¹�', '�ꥻ�å�', *msg, 1 );
}


###
## �����ԥѥ���ɤ��������
#
sub uiAdminConfig
{
    # Isolation level: CHAOS.
    &htmlGen( 'AdminConfig.xml' );
}

sub hg_admin_config_form
{
    &fatal( 18, "$_[0]/AdminConfigForm" ) if ( $_[0] ne 'AdminConfig.xml' );

    local( %tags, $msg );
    $msg = &tagLabel( $H_PASSWD, 'confP', 'P' ) . ': ' .
	&tagInputText( 'password', 'confP', '', $PASSWD_LENGTH ) . $HTML_BR;
    $msg .= &tagLabel( $H_PASSWD, 'confP2', 'C' ) . ': ' .
	&tagInputText( 'password', 'confP2', '', $PASSWD_LENGTH ) .
	'��ǰ�Τ��ᡤ�⤦���٤��ꤤ���ޤ���' . $HTML_BR;
    %tags = ( 'c', 'acx' );
    &dumpForm( *tags, '����', '�ꥻ�å�', *msg, 1 );
}


###
## �����ԥѥ��������μ»�
#
sub uiAdminConfigExec
{
    # Isolation level: SERIALIZABLE.
    &lockAll();

    local( $p1 ) = &cgi'tag( 'confP' );
    local( $p2 ) = &cgi'tag( 'confP2' );

    # admin�Τ�
    &fatal( 44, '' ) unless &isUser( $ADMIN );

    if ( !$p2 || ( $p1 ne $p2 ))
    {
	&fatal( 42, $H_PASSWD );
    }
    
    if ( !&cgiauth'setUserPasswd( $USER_AUTH_FILE , $ADMIN, $p1 ))
    {
	&fatal( 41, $ADMIN );
    }

    &unlockAll();

    # �桼������򥯥ꥢ
    &uiLogin();
}


###
## �桼����Ͽ����
#
sub uiUserEntry
{
    # Isolation level: CHAOS.

    # �桼������򥯥ꥢ
    $UNAME = $cgiauth'F_COOKIE_RESET if ( $SYS_AUTH == 1 );
    &htmlGen( 'UserEntry.xml' );
}

sub hg_user_entry_form
{
    &fatal( 18, "$_[0]/UserEntryForm" ) if ( $_[0] ne 'UserEntry.xml' );

    local( %tags, $msg );
    $msg = &tagLabel( $H_FROM, 'kinoU', 'N' ) . ': ' .
	&tagInputText( 'text', 'kinoU', '', $NAME_LENGTH ) . $HTML_BR;
    $msg .= &tagLabel( $H_MAIL, 'mail', 'M' ) . ': ' .
	&tagInputText( 'text', 'mail', '', $MAIL_LENGTH ) . $HTML_BR;
    $msg .= &tagLabel( $H_PASSWD, 'kinoP', 'P' ) . ': ' .
	&tagInputText( 'password', 'kinoP', '', $PASSWD_LENGTH ) . $HTML_BR;
    $msg .= &tagLabel( $H_PASSWD, 'kinoP2', 'C' ) . ': ' .
	&tagInputText( 'password', 'kinoP2', '', $PASSWD_LENGTH ) .
	'��ǰ�Τ��ᡤ�⤦���٤��ꤤ���ޤ���' . $HTML_BR;
    $msg .= &tagLabel( $H_URL, 'url', 'U' ) . ': ' .
	&tagInputText( 'text', 'url', 'http://', $URL_LENGTH ) .
	'�ʾ�ά���Ƥ⤫�ޤ��ޤ����' . $HTML_BR;

    %tags = ( 'c', 'uex' );
    &dumpForm( *tags, '��Ͽ', '�ꥻ�å�', *msg, 1 );
}


###
## �桼����Ͽ�μ»�
#
sub uiUserEntryExec
{
    # Isolation level: SERIALIZABLE.
    &lockAll();

    local( $user ) = &cgi'tag( 'kinoU' );
    local( $p1 ) = &cgi'tag( 'kinoP' );
    local( $p2 ) = &cgi'tag( 'kinoP2' );
    local( $mail ) = &cgi'tag( 'mail' );
    local( $url ) = &cgi'tag( 'url' );

    &checkName( *user );
    &checkEmail( *mail );
    &checkURL( *url );
    &checkPasswd( *p1 );

    if ( !$p2 || ( $p1 ne $p2 ))
    {
	&fatal( 42, $H_PASSWD );
    }
	    
    # ��Ͽ�Ѥߥ桼���θ���
    if ( $SYS_POSTERMAIL && &cgiauth'searchUserInfo( $USER_AUTH_FILE, $mail, undef ))
    {
	&fatal( 6, $mail );
    }

    # ������Ͽ����
    local( $res ) = &cgiauth'addUser( $USER_AUTH_FILE, $user, $p1, $mail, $url );

    if ( $res == 1 )
    {
	&fatal( 5, $user );
    }
    elsif ( $res == 2 )
    {
	&fatal( 998, 'Must not reach here(UserEntryExec).' );
    }

    &unlockAll();

    # ��������̤�
    &uiLogin();
}


###
## �桼�������ѹ�
#
sub uiUserConfig
{
    # Isolation level: CHAOS.

    &htmlGen( 'UserConfig.xml' );
}

sub hg_user_config_form
{
    &fatal( 18, "$_[0]/UserConfigForm" ) if ( $_[0] ne 'UserConfig.xml' );

    if ( $POLICY & 8 )
    {
	local( %tags, $msg );
	$msg .= &tagLabel( "�ѹ�����$H_USER��$H_FROM", 'confUser', 'N' ) .
	    ': ' . &tagInputText( 'text', 'confUser', '', $NAME_LENGTH ) .
	    "�ʴ����Ԥ���$H_USER��������ѹ��Ǥ��ޤ���" . $HTML_BR . $HTML_BR;
	$msg .= &tagLabel( $H_MAIL, 'confMail', 'M' ) . ': ' .
	    &tagInputText( 'text', 'confMail', '', $MAIL_LENGTH ) . $HTML_BR;
	$msg .= &tagLabel( $H_URL, 'confUrl', 'U' ) . ': ' .
	    &tagInputText( 'text', 'confUrl', 'http://', $URL_LENGTH ) . $HTML_BR . $HTML_BR;
	$msg .= &tagLabel( $H_PASSWD, 'confP', 'P' ) . ': ' .
	    &tagInputText( 'password', 'confP', '', $PASSWD_LENGTH ) . $HTML_BR;
	$msg .= &tagLabel( $H_PASSWD, 'confP2', 'C' ) . ': ' .
	    &tagInputText( 'password', 'confP2', '', $PASSWD_LENGTH ) .
	    '��ǰ�Τ��ᡤ�⤦���٤��ꤤ���ޤ���' . $HTML_BR;
	%tags = ( 'c', 'ucx' );
	&dumpForm( *tags, '����', '�ꥻ�å�', *msg );
    }
    else
    {
	$UURL = $UURL || 'http://';

	local( %tags, $msg );
	$msg .= $H_FROM . ': ' . $UNAME . $HTML_BR . $HTML_BR;
	$msg .= &tagLabel( $H_MAIL, 'confMail', 'M' ) . ': ' .
	    &tagInputText( 'text', 'confMail', $UMAIL, $MAIL_LENGTH ) . $HTML_BR;
	$msg .= &tagLabel( $H_URL, 'confUrl', 'U' ) . ': ' .
	    &tagInputText( 'text', 'confUrl', $UURL, $URL_LENGTH ) . $HTML_BR . $HTML_BR;
	$msg .= &tagLabel( $H_PASSWD, 'confP', 'P' ) . ': ' .
	    &tagInputText( 'password', 'confP', '' , $PASSWD_LENGTH ) . $HTML_BR;
	$msg .= &tagLabel( $H_PASSWD, 'confP2', 'C' ) . ': ' .
	    &tagInputText( 'password', 'confP2', '', $PASSWD_LENGTH ) .
	    '��ǰ�Τ��ᡤ�⤦���٤��ꤤ���ޤ���' . $HTML_BR;
	%tags = ( 'c', 'ucx' );
	&dumpForm( *tags, '����', '�ꥻ�å�', *msg );
    }
}


###
## �桼������μ»�
#
sub uiUserConfigExec
{
    # Isolation level: SERIALIZABLE.
    &lockAll();

    local( $p1 ) = &cgi'tag( 'confP' );
    local( $p2 ) = &cgi'tag( 'confP2' );
    local( $user ) = &cgi'tag( 'confUser' );
    local( $mail ) = &cgi'tag( 'confMail' );
    local( $url ) = &cgi'tag( 'confUrl' );

    $user = $UNAME unless ( $POLICY & 8 );

    &checkName( *user );
    &checkEmail( *mail );
    &checkURL( *url );
		
    # ��ɬ�פʤ�˥ѥ�����ѹ�
    if ( $p1 || $p2 )
    {
	&checkPasswd( *p1 );

	if ( !$p2 || ( $p1 ne $p2 ))
	{
	    &fatal( 42, $H_PASSWD );
	}

	if ( !&cgiauth'setUserPasswd( $USER_AUTH_FILE, $user, $p1 ))
	{
	    &fatal( 41, $user );
	}
    }

    # �桼�����󹹿�
    if ( !&cgiauth'setUserInfo( $USER_AUTH_FILE, $user, ( $mail, $url )))
    {
	&fatal( 41, '' );
    }

    &unlockAll();

    &uiBoardList();
}


###
## �Ǽ�����Ͽ����
#
sub uiBoardEntry
{
    # Isolation level: CHAOS.

    &htmlGen( 'BoardEntry.xml' );
}

sub hg_board_entry_form
{
    &fatal( 18, "$_[0]/BoardEntryForm" ) if ( $_[0] ne 'BoardEntry.xml' );

    local( %tags, $msg );
    $msg = &tagLabel( "$H_BOARDά��", 'name', 'B' ) . ': ' .
	&tagInputText( 'text', 'name', '', $BOARDNAME_LENGTH ) . $HTML_BR;
    $msg .= &tagLabel( "$H_BOARD̾��", 'intro', 'N' ) . ': ' .
	&tagInputText( 'text', 'intro', '', $BOARDNAME_LENGTH ) . $HTML_BR . $HTML_BR;
    $msg .= &tagLabel( "$H_BOARD�μ�ư$H_MAIL�ۿ���", 'armail', 'M' ) .
	$HTML_BR . &tagTextarea( 'armail', '', $TEXT_ROWS, $MAIL_LENGTH ) .
	$HTML_BR . $HTML_BR;
    $msg .= &tagLabel( "$H_BOARD�إå���ʬ", 'article', 'H' ) . $HTML_BR .
	&tagTextarea( 'article', '', $TEXT_ROWS, $TEXT_COLS ) . $HTML_BR;
    %tags = ( 'c', 'bex' );
    &dumpForm( *tags, '��Ͽ', '�ꥻ�å�', *msg );
}


###
## �Ǽ�����Ͽ�μ»�
#
sub uiBoardEntryExec
{
    # Isolation level: SERIALIZABLE.
    &lockAll();

    local( $name ) = &cgi'tag( 'name' );
    local( $intro ) = &cgi'tag( 'intro' );
    local( $armail ) = &cgi'tag( 'armail' );
    local( $header ) = &cgi'tag( 'article' );

    &checkBoardDir( *name );
    &checkBoardName( *intro );
    &checkBoardHeader( *header );
    &secureSubject( *intro );
    &secureArticle( *header, $H_TTLABEL[2] );
    local( @arriveMail ) = split( /\n/, $armail );

    &insertBoard( $name, $intro, 0, *arriveMail, *header );

    &unlockAll();

    &uiBoardList();
}


###
## �Ǽ��������ѹ�����
#
sub uiBoardConfig
{
    # Isolation level: SERIALIZABLE.
    &lockAll();

    # ���Ǽ��Ĥξ������Ф�
    @gArriveMail = ();
    &getBoardSubscriber(1, $BOARD, *gArriveMail); # ����ȥ����Ȥ���Ф�
    $gHeader = "";
    &getBoardHeader( $BOARD, *gHeader ); # �إå�ʸ�������Ф�

    &htmlGen( 'BoardConfig.xml' );

    &unlockAll();
}

sub hg_board_config_form
{
    &fatal( 18, "$_[0]/BoardConfigForm" ) if ( $_[0] ne 'BoardConfig.xml' );

    local( %tags, $msg );
    $msg = &tagLabel( "��$BOARD��$H_BOARD������", 'valid', 'V' ) . ': ' .
	&tagInputCheck( 'valid', 1 ) . $HTML_BR . $HTML_BR;
    $msg .= &tagLabel( "��$BOARD��̾��", 'intro', 'N' ) . ': ' .
	&tagInputText( 'text', 'intro', $BOARDNAME, $BOARDNAME_LENGTH ) .
	$HTML_BR . $HTML_BR;
    local( $all );
    foreach ( @gArriveMail ) { $all .= $_ . "\n"; }
    $msg .= &tagLabel( "��$BOARD�פμ�ư$H_MAIL�ۿ���", 'armail', 'M' ) .
	$HTML_BR . &tagTextarea( 'armail', $all, $TEXT_ROWS, $MAIL_LENGTH ) .
	$HTML_BR . $HTML_BR;
    $msg .= &tagLabel( "��$BOARD�פ�$H_BOARD�إå���ʬ", 'article', 'H' ) .
	$HTML_BR . &tagTextarea( 'article', $gHeader, $TEXT_ROWS, $TEXT_COLS ) . $HTML_BR;
    %tags = ( 'c', 'bcx', 'b', $BOARD );
    &dumpForm( *tags, '�ѹ�', '�ꥻ�å�', *msg );
}


###
## �Ǽ�������μ»�
#
sub uiBoardConfigExec
{
    # Isolation level: SERIALIZABLE.
    &lockAll();

    local( $valid ) = &cgi'tag( 'valid' );
    local( $intro ) = &cgi'tag( 'intro' );
    local( $armail ) = &cgi'tag( 'armail' );
    local( $header ) = &cgi'tag( 'article' );

    &checkBoardName( *intro );
    &checkBoardHeader( *header );
    &secureSubject( *intro );
    &secureArticle( *header, $H_TTLABEL[2] );
    local( @arriveMail ) = split( /\n/, $armail );

    &updateBoard( $BOARD, $valid, $intro, 0, *arriveMail, *header );

    &unlockAll();

    &uiBoardList();
}


###
## �Ǽ��İ���
#
sub uiBoardList
{
    # Isolation level: CHAOS.

    &htmlGen( 'BoardList.xml' );
}


###
## ��å�����������Ͽ�Υ���ȥ�
## ��ץ饤��å�������Ͽ�Υ���ȥ�
## ��å����������Υ���ȥ�
#
sub uiPostNewEntry
{
    # Isolation level: CHAOS.

    if ( $SYS_NEWART_ADMINONLY && !( $POLICY & 8 ))
    {
	&fatal( 99, scalar( &cgi'tag( 'c' )));
    }

    local( $back ) = @_;

    $gId = '';			# 0�Ǥϥ��ᡥ���������ե�����̾�⤢�뤫�⡥
    $gDefPostDateStr = &cgi'tag( 'postdate' );
    $gDefSubject = &cgi'tag( 'subject' );
    $gDefName = &cgi'tag( 'name' );
    $gDefEmail = &cgi'tag( 'mail' );
    $gDefUrl = &cgi'tag( 'url' );
    $gDefTextType = &cgi'tag( 'texttype' );
    $gDefIcon = &cgi'tag( 'icon' );
    $gDefArticle = &cgi'tag( 'article' );
    $gDefFmail = &cgi'tag( 'fmail' );

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

sub uiPostReplyEntry
{
    # Isolation level: SERIALIZABLE.
    &lockBoard();
    &cacheArt( $BOARD );

    local( $back, $quoteFlag ) = @_;

    $gId = &cgi'tag( 'id' );
    $gDefPostDateStr = &cgi'tag( 'postdate' );
    $gDefSubject = &cgi'tag( 'subject' );
    $gDefName = &cgi'tag( 'name' );
    $gDefEmail = &cgi'tag( 'mail' );
    $gDefUrl = &cgi'tag( 'url' );
    $gDefTextType = &cgi'tag( 'texttype' );
    $gDefIcon = &cgi'tag( 'icon' );
    $gDefArticle = &cgi'tag( 'article' );
    $gDefFmail = &cgi'tag( 'fmail' );

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
	    $gDefSubject = &getArtSubject( $gId );
	    &getReplySubject( *gDefSubject );
	}
    }
    else
    {
	if ( $gDefSubject eq '' )
	{
	    local( $tmp );
	    $gDefSubject = &getArtSubject( $gId );
	    &getReplySubject( *gDefSubject );
	}
	&quoteOriginalArticle( $gId, *gDefArticle );
    }

    $gEntryType = 'reply';		# ��ץ饤
    &htmlGen( 'PostReplyEntry.xml' );

    &unlockBoard();
}

sub uiSupersedeEntry
{
    # Isolation level: SERIALIZABLE.
    &lockBoard();
    &cacheArt( $BOARD );

    local( $back ) = @_;

    if ( !( $POLICY & 8 ) && ( $SYS_OVERWRITE == 0 ))
    {
	&fatal( 99, scalar( &cgi'tag( 'c' )));
    }

    $gId = &cgi'tag( 'id' );
    $gDefPostDateStr = &cgi'tag( 'postdate' );
    $gDefSubject = &cgi'tag( 'subject' );
    $gDefName = &cgi'tag( 'name' );
    $gDefEmail = &cgi'tag( 'mail' );
    $gDefUrl = &cgi'tag( 'url' );
    $gDefTextType = &cgi'tag( 'texttype' );	# ��������XHTML���ϤΤۤ����������� 
    $gDefIcon = &cgi'tag( 'icon' );
    $gDefArticle = &cgi'tag( 'article' );
    $gDefFmail = &cgi'tag( 'fmail' );

    if ( $back )
    {
	require( 'mimer.pl' );
	$gDefSubject = &MIME'base64decode( $gDefSubject );
	$gDefArticle = &MIME'base64decode( $gDefArticle );
    }
    else
    {
	local( $tmp, $postDate );
	( $tmp, $tmp, $postDate, $gDefSubject, $gDefIcon, $tmp, $gDefName, $gDefEmail, $gDefUrl ) = &getArtInfo( $gId );
	$gDefPostDateStr = &getYYYY_MM_DD_HH_MM_SSFromUtc( $postDate );
	&quoteOriginalArticleWithoutQMark( $gId, *gDefArticle );
    }

    $gEntryType = 'supersede';		# ����
    &htmlGen( 'SupersedeEntry.xml' );

    &unlockBoard();
}

sub hg_post_reply_entry_orig_article
{
    &fatal( 18, "$_[0]/PostReplyEntryOrigArticle" ) if ( $_[0] ne 'PostReplyEntry.xml' );
    &dumpArtBody( $gId, 0, 1 );
}

sub hg_supersede_entry_orig_article
{
    &fatal( 18, "$_[0]/SupersedeEntryOrigArticle" ) if ( $_[0] ne 'SupersedeEntry.xml' );
    &dumpArtBody( $gId, 0, 1 );
}


###
## ��å�������Ͽ�Υץ�ӥ塼
## ��å����������Υץ�ӥ塼
#
sub uiPostPreview
{
    # Isolation level: SERIALIZABLE.
    &lockAll();
    &cacheArt( $BOARD );

    &uiPostPreviewMain( 'post' );
    &htmlGen( 'PostPreview.xml' );

    &unlockAll();
}

sub uiSupersedePreview
{
    # Isolation level: READ UNCOMITTED.
    &lockAll();
    &cacheArt( $BOARD );
    &unlockAll();

    if ( !( $POLICY & 8 ) && ( $SYS_OVERWRITE == 0 ))
    {
	&fatal( 99, scalar( &cgi'tag( 'c' )));
    }

    &uiPostPreviewMain( 'supersede' );
    &htmlGen( 'SupersedePreview.xml' );
}

sub uiPostPreviewMain
{
    local( $type ) = @_;

    # ���Ϥ��줿��������
    $gOrigId = &cgi'tag( 'id' );
    $gPostDateStr = &cgi'tag( 'postdate' );
    $gSubject = &cgi'tag( 'subject' );
    $gIcon = &cgi'tag( 'icon' );
    $gArticle = &cgi'tag( 'article' );
    $gTextType = &cgi'tag( 'texttype' );

    # �Ƽ����μ���
    if ( $POLICY & 8 )
    {
	if ( &cgi'tag( 'name' ) eq '' )
	{
	    $gName = $MAINT_NAME;
	    $gEmail = $MAINT;
	    $gUrl = $MAINT_URL;
	}
	else
	{
	    $gName = &cgi'tag( 'name' );
	    $gEmail = &cgi'tag( 'mail' );
	    $gUrl = &cgi'tag( 'url' );
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
	$gName = &cgi'tag( 'name' );
	$gEmail = &cgi'tag( 'mail' );
	$gUrl = &cgi'tag( 'url' );
    }

    $gEncSubject = &MIME'base64encode( $gSubject );
    $gEncArticle = &MIME'base64encode( $gArticle );

    &secureSubject( *gSubject );
    &secureArticle( *gArticle, $gTextType );

    local( $postDate ) = $^T;
    $postDate = &getUtcFromYYYY_MM_DD_HH_MM_SS( $gPostDateStr ) if ( $gPostDateStr ne '' );

    # ���Ϥ��줿��������Υ����å�
    &checkArticle( $BOARD, *postDate, *gName, *gEmail, *gUrl, *gSubject, *gIcon, *gArticle );
}

sub hg_post_preview_form
{
    &fatal( 18, "$_[0]/PostPreviewForm" ) if ( $_[0] ne 'PostPreview.xml' );

    require( 'mimer.pl' );

    local( $supersede ) = $_[1];

    local( %tags, $msg, $contents );
    $contents = &tagInputRadio( 'com_e', 'com', 'e', 0 ) . ":\n" . &tagLabel( '��äƤ��ʤ���', 'com_e', 'P' ) . $HTML_BR;
    $contents .= &tagInputRadio( 'com_x', 'com', 'x', 1 ) . "\n" . &tagLabel( '��Ͽ����', 'com_x', 'X' ) . $HTML_BR;
    $msg = &tagFieldset( "���ޥ��:$HTML_BR", $contents );
    %tags = ( 'corig', scalar( &cgi'tag( 'corig' )), 'c', 'x', 'b', $BOARD,
	     'id', $gOrigId, 'postdate', $gPostDateStr, 'texttype', $gTextType,
	     'name', $gName, 'mail', $gEmail, 'url', $gUrl, 'icon', $gIcon,
	     'subject', $gEncSubject, 'article', $gEncArticle,
	     'fmail', scalar( &cgi'tag( 'fmail' )), 's', $supersede,
	     'op', scalar( &cgi'tag( 'op' )));

    &dumpForm( *tags, '�¹�', '', *msg );
}

sub hg_supersede_preview_form
{
    &fatal( 18, "$_[0]/SupersedePreviewForm" ) if ( $_[0] ne 'SupersedePreview.xml' );
    &hg_post_preview_form( 'PostPreview.xml', 1 );
}

sub hg_post_preview_body
{
    &fatal( 18, "$_[0]/PostPreviewBody" ) if ( $_[0] ne 'PostPreview.xml' );

    local( $postDate ) = $^T;
    $postDate = &getUtcFromYYYY_MM_DD_HH_MM_SS( $gPostDateStr ) if ( $gPostDateStr ne '' );
    &dumpArtBody( '', 0, 1, $gOrigId, '', $postDate, $gSubject, $gIcon, 0, $gName, $gEmail, $gUrl, $gArticle );
}

sub hg_supersede_preview_body
{
    &fatal( 18, "$_[0]/SupersedePreviewBody" ) if ( $_[0] ne 'SupersedePreview.xml' );

    local( $postDate ) = $^T;
    $postDate = &getUtcFromYYYY_MM_DD_HH_MM_SS( $gPostDateStr ) if ( $gPostDateStr ne '' );

    # hg_post_preview_body�Ȥϰۤʤꡤfid�����ʥ�ץ饤���ǤϤʤ��ˡ�
    &dumpArtBody( '', 0, 1, '', '', $postDate, $gSubject, $gIcon, 0, $gName, $gEmail, $gUrl, $gArticle );
}

sub hg_supersede_preview_orig_article
{
    &fatal( 18, "$_[0]/SupersedePreviewOrigArticle" ) if ( $_[0] ne 'SupersedePreview.xml' );
    &dumpArtBody( $gOrigId, 0, 1 );
}


###
## ��������Ͽ
## ����������
#
sub uiPostExec
{
    # Isolation level: SERIALIZABLE.
    &lockAll();
    &cacheArt( $BOARD );

    local( $previewFlag ) = @_;

    &uiPostExecMain( $previewFlag, 'post' );
    &htmlGen( 'PostExec.xml' );

    &unlockAll();
}

sub uiSupersedeExec
{
    # Isolation level: SERIALIZABLE.
    &lockAll();
    &cacheArt( $BOARD );

    if ( !( $POLICY & 8 ) && ( $SYS_OVERWRITE == 0 ))
    {
	&fatal( 99, scalar( &cgi'tag( 'c' )));
    }

    local( $previewFlag ) = @_;
    &uiPostExecMain( $previewFlag, 'supersede' );
    &htmlGen( 'SupersedeExec.xml' );

    &unlockAll();
}

sub uiPostExecMain
{
    require( 'mimer.pl' );

    local( $previewFlag, $type ) = @_;

    # ���Ϥ��줿��������
    $gOrigId = &cgi'tag( 'id' );
    local( $postDateStr ) = &cgi'tag( 'postdate' );
    local( $TextType ) = &cgi'tag( 'texttype' );
    local( $Icon ) = &cgi'tag( 'icon' );
    local( $Subject ) = &cgi'tag( 'subject' );
    local( $Article ) = &cgi'tag( 'article' );
    local( $Fmail ) = &cgi'tag( 'fmail' );
    local( $op ) = &cgi'tag( 'op' );

    # ����Ⱦ���δ֤��������줿�ե����फ�餷����Ƥ���Ĥ��ʤ���
    local( $base ) = ( -M &getPath( $SYS_DIR, $BOARD_FILE ));
    if ( $SYS_DENY_FORM_OLD && (( $op == 0 ) || ( $base - $op > .5 )))
    {
	&fatal( 15, '' );
    }

    # �ե���������Ѥζػ�
    if ( $SYS_DENY_FORM_RECYCLE )
    {
	local( $dKey ) = &getBoardKey( $BOARD );
	&fatal( 16, '' ) if ( $dKey && ( $dKey == $op ));
    }

    # �Ƽ����μ���
    local( $Name, $Email, $Url, $postDate );
    $postDate = $^T;
    if ( $POLICY & 8 )
    {
	if ( &cgi'tag( 'name' ) eq '' )
	{
	    $Name = $MAINT_NAME;
	    $Email = $MAINT;
	    $Url = $MAINT_URL;
	}
	else
	{
	    $Name = &cgi'tag( 'name' );
	    $Email = &cgi'tag( 'mail' );
	    $Url = &cgi'tag( 'url' );
	}
	if ( $postDateStr ne '' )
	{
	    $postDate = &getUtcFromYYYY_MM_DD_HH_MM_SS( $postDateStr );
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
	$Name = &cgi'tag( 'name' );
	$Email = &cgi'tag( 'mail' );
	$Url = &cgi'tag( 'url' );
    }

    $Subject = &MIME'base64decode( $Subject ) if $previewFlag;
    $Article = &MIME'base64decode( $Article ) if $previewFlag;
    &secureSubject( *Subject );
    &secureArticle( *Article, $TextType );

    if ( $type eq 'post' )
    {
	# �����κ���
	$gNewArtId = &makeNewArticleEx( $BOARD, $gOrigId, $op, $postDate, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail, 1 );
    }
    elsif ( $type eq 'supersede' )
    {
	# ����������
	local( $name ) = &getArtAuthor( $gOrigId );
	&fatal( 44, '' ) if ( !&isUser( $name ) && !( $POLICY & 8 ));
	&fatal( 19, '' ) if (( &getArtDaughters( $gOrigId ) ne '' ) && !( $POLICY & 8 ) && ( $SYS_OVERWRITE == 1 ));

	$gNewArtId = &supersedeArticle( $BOARD, $gOrigId, $postDate, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail );
    }
    else
    {
	&fatal( 998, 'Must not reache here(UIPostExecMain).' );
    }
}

sub hg_post_exec_jump_to_new_article
{
    &fatal( 18, "$_[0]/PostExecJumpToNewArticle" ) if ( $_[0] ne 'PostExec.xml' );
    &dumpButtonToArticle( $BOARD, $gNewArtId, "�񤭹����$H_MESG��" );
}

sub hg_supersede_exec_jump_to_new_article
{
    &fatal( 18, "$_[0]/SupersedeExecJumpToNewArticle" ) if ( $_[0] ne 'SupersedeExec.xml' );
    &dumpButtonToArticle( $BOARD, $gNewArtId, "��������$H_MESG��" );
}

sub hg_post_exec_jump_to_orig_article
{
    &fatal( 18, "$_[0]/PostExecJumpToOrigArticle" ) if ( $_[0] ne 'PostExec.xml' );
    &dumpButtonToArticle( $BOARD, $gOrigId, "$H_PARENT��" ) if ( $gOrigId ne '' );
}


###
## ����å��̥����ȥ뤪��ӵ�������
#
sub uiThreadArticle
{
    # Isolation level: READ UNCOMITTED.
    &lockBoard();
    &cacheArt( $BOARD );
    &unlockBoard();

    %gADDFLAG = ();
    @gIDLIST = ();

    local( $nofMsg ) = &getNofArt();

    # ɽ������Ŀ������
    $gNum = &cgi'tag( 'num' );
    if ( defined( &cgi'tag( 'id' )))
    {
	$gOld = $nofMsg - int( &cgi'tag( 'id' ) + $gNum/2 );
	$gOld = 0 if ( $gOld < 0 );
    }
    else
    {
	$gOld = &cgi'tag( 'old' );
    }
    $gRev = &cgi'tag( 'rev' );
    $gFold = (( $SYS_THREAD_FORMAT == 2 ) || &cgi'tag( 'fold' ))? 1 : 0;
    $gVRev = $gRev? 1-$SYS_BOTTOMTITLE : $SYS_BOTTOMTITLE;
    $gTo = $nofMsg - $gOld;
    $gFrom = $gTo - $gNum + 1;
    $gFrom = 0 if (( $gFrom < 0 ) || ( $gNum == 0 ));

    $gPageLinkStr = &pageLink( 'vt', $gNum, $gOld, $gRev, $gFold );

    # �����Ѥߥե饰
    # 0 ... �����оݳ�
    # 1 ... �����Ѥ�
    # 2 ... ̤����
    local( $IdNum, $Id );
    for ( $IdNum = $gFrom; $IdNum <= $gTo; $IdNum++ )
    {
	$gADDFLAG{ &getArtId( $IdNum ) } = 2;
    }

    &htmlGen( 'ThreadArticle.xml' );
}

sub hg_thread_article_tree
{
    &fatal( 18, "$_[0]/ThreadArticleTree" ) if ( $_[0] ne 'ThreadArticle.xml' );

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
	    $Id = &getArtId( $IdNum );
	    $Fid = &getArtParent( $Id );
	    # �������Ȥϸ�󤷡�
	    next if (( $Fid ne '' ) && (( $gADDFLAG{$Fid} == 2 ) || ( $SYS_THREAD_FORMAT == 2 )));

	    # �Ρ��ɤ�ɽ��
	    $gHgStr .= "<ul>\n" unless $gFold;
	    if ( $gFold )
	    {
		&threadTitleNodeNoThread( $Id, 3 );
	    }
	    elsif ( $SYS_THREAD_FORMAT == 0 )
	    {
		&threadTitleNodeThread( $Id, 3 );
	    }
	    elsif ( $SYS_THREAD_FORMAT == 1 )
	    {
		&threadTitleNodeAllThread( $Id, 3 );
	    }
	    else
	    {
		&threadTitleNodeNoThread( $Id, 3 );
	    }
	    $gHgStr .= "</ul>\n" unless $gFold;
	    &cgiprint'cache( $gHgStr ); $gHgStr = '';
	}
	$gHgStr .= "</ul>\n" if $gFold;
    }
    else
    {
	$gHgStr .= "<ul>\n" if $gFold;

	for( $IdNum = $gTo; $IdNum >= $gFrom; $IdNum-- )
	{
	    $Id = &getArtId( $IdNum );
	    $Fid = &getArtParent( $Id );
	    next if (( $Fid ne '' ) && (( $gADDFLAG{$Fid} == 2 ) || ( $SYS_THREAD_FORMAT == 2 )));

	    $gHgStr .= "<ul>\n" unless $gFold;
	    if ( $gFold )
	    {
		&threadTitleNodeNoThread( $Id, 3 );
	    }
	    elsif ( $SYS_THREAD_FORMAT == 0 )
	    {
		&threadTitleNodeThread( $Id, 3 );
	    }
	    elsif ( $SYS_THREAD_FORMAT == 1 )
	    {
		&threadTitleNodeAllThread( $Id, 3 );
	    }
	    else
	    {
		&threadTitleNodeNoThread( $Id, 3 );
	    }
	    $gHgStr .= "</ul>\n" unless $gFold;
	    &cgiprint'cache( $gHgStr ); $gHgStr = '';
	}
	$gHgStr .= "</ul>\n" if $gFold;
    }
}

sub hg_thread_article_body
{
    &fatal( 18, "$_[0]/ThreadArticleBody" ) if ( $_[0] ne 'ThreadArticle.xml' );

    local( $id );
    if ( $#gIDLIST >= 0 )
    {
	$gHgStr .= $HTML_HR;
	while ( $id = shift( @gIDLIST ))
	{
	    &dumpArtBody( $id, $SYS_COMMAND_EACH, 1 );
	    $gHgStr .= $HTML_HR;
	}
    }
}


###
## ����å��̥����ȥ����
#
sub uiThreadTitle
{
    # Isolation level: READ UNCOMITTED.
    &lockBoard();
    &cacheArt( $BOARD );

    ( $gComType ) = @_;

    if ( $gComType == 3 )
    {
	# ��󥯤��������μ»�
	&reLinkExec( scalar( &cgi'tag( 'rfid' )), scalar( &cgi'tag( 'rtid' )), $BOARD );
    }
    elsif ( $gComType == 5 )
    {
	# ��ư�μ»�
	&reOrderExec( scalar( &cgi'tag( 'rfid' )), scalar( &cgi'tag( 'rtid' )), $BOARD );
    }

    &unlockBoard();

    local( $vCom, $vStr );

    if ( $ComType == 0 )
    {
	$vCom = 'v';
	$vStr = '';
    }
    elsif ( $ComType == 2 )
    {
	$vCom = 'ct';
	$vStr = '&rtid=' . &cgi'tag( 'roid' ) . '&rfid=' . &cgi'tag( 'rfid' ) .
	    '&rtid=' . &cgi'tag( 'rtid' );
    }
    elsif ( $gComType == 3 )
    {
	$vCom = 'v';
	$vStr = '';
    }
    elsif ( $gComType == 4 )
    {
	$vCom = 'mvt';
	$vStr = '&rtid=' . &cgi'tag( 'roid' ) . '&rfid=' . &cgi'tag( 'rfid' ) .
	    '&rtid=' . &cgi'tag( 'rtid' );
    }
    elsif ( $gComType == 5 )
    {
	$vCom = 'v';
	$vStr = '';
    }

    %gADDFLAG = ();
    @gIDLIST = ();		# Not used here. It's for ThreadArticle.

    local( $nofMsg ) = &getNofArt();

    # ɽ������Ŀ������
    $gNum = &cgi'tag( 'num' );
    if ( defined( &cgi'tag( 'id' )))
    {
	$gOld = $nofMsg - int( &cgi'tag( 'id' ) + $gNum/2 );
	$gOld = 0 if ( $gOld < 0 );
    }
    else
    {
	$gOld = &cgi'tag( 'old' );
    }
    $gRev = &cgi'tag( 'rev' );
    $gFold = (( $SYS_THREAD_FORMAT == 2 ) || &cgi'tag( 'fold' ))? 1 : 0;
    $gVRev = $gRev? 1-$SYS_BOTTOMTITLE : $SYS_BOTTOMTITLE;
    $gTo = $nofMsg - $gOld;
    $gFrom = $gTo - $gNum + 1;
    $gFrom = 0 if (( $gFrom < 0 ) || ( $gNum == 0 ));

    $gPageLinkStr = &pageLink( "$vCom$vStr", $gNum, $gOld, $gRev, $gFold );

    # �����Ѥߥե饰
    # 0 ... �����оݳ�
    # 1 ... �����Ѥ�
    # 2 ... ̤����
    local( $IdNum );
    for ( $IdNum = $gFrom; $IdNum <= $gTo; $IdNum++ )
    {
	$gADDFLAG{ &getArtId( $IdNum ) } = 2;
    }

    &htmlGen( 'ThreadTitle.xml' );
}

sub hg_thread_title_board_header
{
    &fatal( 18, "$_[0]/ThreadTitleBoardHeader" ) if ( $_[0] ne 'ThreadTitle.xml' );

    if ( $gComType == 2 )
    {
	$gHgStr .= "<p>������$H_REPLY�����ꤷ�ޤ���\n";
	$gHgStr .= "$H_MESG��#" . &cgi'tag( 'rfid' ) . "�פ򡤤ɤ�$H_MESG�ؤ�$H_REPLY�ˤ��ޤ���? $H_REPLY���$H_MESG��$H_RELINKTO_MARK�򥯥�å����Ƥ���������</p>\n";
    }
    elsif ( $gComType == 3 )
    {
	$gHgStr .= "<p>���ꤵ�줿$H_MESG��$H_REPLY����ѹ����ޤ�����</p>\n";
    }
    elsif ( $gComType == 4 )
    {
	$gHgStr .= "<p>��ư�����ꤷ�ޤ���\n";
	$gHgStr .= "$H_MESG��#" . &cgi'tag( 'rfid' ) . "�פ򡤤ɤ�$H_MESG�β��˰�ư���ޤ���? $H_MESG��$H_REORDERTO_MARK�򥯥�å����Ƥ���������</p>\n";
    }
    elsif ( $gComType == 5 )
    {
	$gHgStr .= "<p>���ꤵ�줿$H_MESG���ư���ޤ�����</p>\n";
    }

    &dumpBoardHeader();

    if ( $POLICY & 8 )
    {
	if ( $gComType == 3 )
	{
	    $gHgStr .= "<ul>\n<li>" . &linkP( "b=$BOARD_ESC&c=ce&rtid=" .
		&cgi'tag( 'roid' ) . "&rfid=" . &cgi'tag( 'rfid' ),
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
    &fatal( 18, "$_[0]/ThreadTitleTree" ) if ( $_[0] ne 'ThreadTitle.xml' );

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
	if (( $gComType == 2 ) && ( &getArtParents( scalar( &cgi'tag( 'rfid' ))) ne '' ))
	{
	    $gHgStr .= '<ul><li>' . &linkP( "b=$BOARD_ESC&c=ce&rtid=&rfid=" .
		&cgi'tag( 'rfid' ) . '&roid=' . &cgi'tag( 'roid' ) . $AddNum,
		"[�ɤ�$H_MESG�ؤ�$H_REPLY�Ǥ�ʤ�������$H_MESG�ˤ���]" ) .
		"</li></ul>\n";
	}
	elsif ( $gComType == 4 )
	{
	    $gHgStr .= '<ul><li>' . &linkP( "b=$BOARD_ESC&c=mve&rtid=&rfid=" .
		&cgi'tag( 'rfid' ) . "&roid=" . &cgi'tag( 'roid' ) . $AddNum,
		"[����������Ƭ�˰�ư����(���Υڡ����Ρ��ǤϤ���ޤ���)]" ) .
		"</li></ul>\n";
	}

	$gHgStr .= "<ul>\n" if $gFold;

	for( $IdNum = $gFrom; $IdNum <= $gTo; $IdNum++ )
	{
	    # ����������ID����Ф�
	    $Id = &getArtId( $IdNum );
	    $Fid = &getArtParent( $Id );
	    # �������Ȥϸ�󤷡�
	    next if (( $Fid ne '' ) && (( $gADDFLAG{$Fid} == 2 ) ||
		( $SYS_THREAD_FORMAT == 2 )));

	    # �Ρ��ɤ�ɽ��
	    $gHgStr .= "<ul>\n" unless $gFold;
	    if ( $gFold )
	    {
		&threadTitleNodeNoThread( $Id, 1, $AddNum, ( $POLICY & 8 ));
	    }
	    elsif ( $SYS_THREAD_FORMAT == 0 )
	    {
		&threadTitleNodeThread( $Id, 1, $AddNum, ( $POLICY & 8 ));
	    }
	    elsif ( $SYS_THREAD_FORMAT == 1 )
	    {
		&threadTitleNodeAllThread( $Id, 1, $AddNum, ( $POLICY & 8 ));
	    }
	    else
	    {
		&threadTitleNodeNoThread( $Id, 1, $AddNum, ( $POLICY & 8 ));
	    }
	    $gHgStr .= "</ul>\n" unless $gFold;
	    &cgiprint'cache( $gHgStr ); $gHgStr = '';
	}
	$gHgStr .= "</ul>\n" if $gFold;
    }
    else
    {
	# �������Τ������
	if (( $gComType == 2 ) && ( &getArtParents( scalar( &cgi'tag( 'rfid' ))) ne '' ))
	{
	    $gHgStr .= '<ul><li>' . &linkP( "b=$BOARD_ESC&c=ce&rtid=&rfid=" .
		&cgi'tag( 'rfid' ) . "&roid=" . &cgi'tag( 'roid' ) . $AddNum,
		"[�ɤ�$H_MESG�ؤ�$H_REPLY�Ǥ�ʤ�������$H_MESG�ˤ���]" ) .
		"</li></ul>\n";
	}
	elsif ( $gComType == 4 )
	{
	    $gHgStr .= '<ul><li>' . &linkP( "b=$BOARD_ESC&c=mve&rtid=&rfid=" .
		&cgi'tag( 'rfid' ) . "&roid=" . &cgi'tag( 'roid' ) . $AddNum,
		"[����������Ƭ�˰�ư����(���Υڡ����Ρ��ǤϤ���ޤ���)]" ) .
		"</li></ul>\n";
	}

	$gHgStr .= "<ul>\n" if $gFold;

	for( $IdNum = $gTo; $IdNum >= $gFrom; $IdNum-- )
	{
	    # ���Ʊ��
	    $Id = &getArtId( $IdNum );
	    $Fid = &getArtParent( $Id );
	    next if (( $Fid ne '' ) && (( $gADDFLAG{$Fid} == 2 ) ||
		( $SYS_THREAD_FORMAT == 2 )));

	    $gHgStr .= "<ul>\n" unless $gFold;
	    if ( $gFold )
	    {
		&threadTitleNodeNoThread( $Id, 1, $AddNum, ( $POLICY & 8 ));
	    }
	    elsif ( $SYS_THREAD_FORMAT == 0 )
	    {
		&threadTitleNodeThread( $Id, 1, $AddNum, ( $POLICY & 8 ));
	    }
	    elsif ( $SYS_THREAD_FORMAT == 1 )
	    {
		&threadTitleNodeAllThread( $Id, 1, $AddNum, ( $POLICY & 8 ));
	    }
	    else
	    {
		&threadTitleNodeNoThread( $Id, 1, $AddNum, ( $POLICY & 8 ));
	    }
	    $gHgStr .= "</ul>\n" unless $gFold;
	    &cgiprint'cache( $gHgStr ); $gHgStr = '';
	}
	$gHgStr .= "</ul>\n" if $gFold;
    }
}

# ����Ρ��ɤΤ�ɽ��
sub threadTitleNodeNoThread
{
    local( $id, $flag, $addNum, $maint ) = @_;

    local( $fid, $aids, $date, $title, $icon, $host, $name ) = &getArtInfo( $id );
    &dumpArtSummaryItem( $id, $aids, $date, $title, $icon, $name, $flag );

    $flag &= 6; # 110
    push( @gIDLIST, $id );

    &threadTitleMaintIcon( $id, $addNum ) if $maint;

    $gHgStr .= "</li>\n";
}

# �ڡ����⥹��åɤΤ�ɽ��
sub threadTitleNodeThread
{
    local( $id, $flag, $addNum, $maint ) = @_;

    # �ڡ������ʤ餪���ޤ���
    return if ( $gADDFLAG{ $id } != 2 );

    local( $fid, $aids, $date, $title, $icon, $host, $name ) = &getArtInfo( $id );
    &dumpArtSummaryItem( $id, $aids, (( !$SYS_COMPACTTHREAD || $flag&1 )? $date : 0 ), $title, $icon, $name, $flag );

    $flag &= 6; # 110
    $gADDFLAG{ $id } = 1;		# �����Ѥ�
    push( @gIDLIST, $id );

    &threadTitleMaintIcon( $id, $addNum ) if $maint;

    # ̼�����Сġ�
    if ( $aids )
    {
	$gHgStr .= "<ul>\n";
	foreach ( split( /,/, $aids ))
	{
	    &threadTitleNodeThread( $_, $flag, $addNum, $maint );
	}
	$gHgStr .= "</ul>\n";
    }
    $gHgStr .= "</li>\n";
}

# ������åɤ�ɽ��
sub threadTitleNodeAllThread
{
    local( $id, $flag, $addNum, $maint ) = @_;

    # ɽ���Ѥߤʤ餪���ޤ���
    return if ( $gADDFLAG{ $id } == 1 );

    local( $fid, $aids, $date, $title, $icon, $host, $name ) = &getArtInfo( $id );
    &dumpArtSummaryItem( $id, $aids, (( !$SYS_COMPACTTHREAD || $flag&1 )? $date : 0 ), $title, $icon, $name, $flag );

    $flag &= 6; # 110
    $gADDFLAG{ $id } = 1;		# �����Ѥ�
    push( @gIDLIST, $id );

    &threadTitleMaintIcon( $id, $addNum ) if $maint;

    # ̼�����Сġ�
    if ( $aids )
    {
	$gHgStr .= "<ul>\n";
	foreach ( split( /,/, $aids ))
	{
	    &threadTitleNodeAllThread( $_, $flag, $addNum, $maint );
	}
	$gHgStr .= "</ul>\n";
    }
    $gHgStr .= "</li>\n";
}

# �������ѤΥ�������ɽ��
sub threadTitleMaintIcon
{
    local( $id, $addNum ) = @_;

    $gHgStr .= " .......... \n";

    local( $fromId ) = &cgi'tag( 'rfid' );
    local( $oldId ) = &cgi'tag( 'roid' );

    local( $parents ) = &getArtParents( $id );

    # ������ѹ����ޥ��(From)
    $gHgStr .= &linkP( "b=$BOARD_ESC&c=ct&rfid=$id&roid=" . $parents . $addNum,
	$H_RELINKFROM_MARK, '', $H_RELINKFROM_MARK_L ) . "\n";

    if ( $parents eq '' )
    {
	# ��ư���ޥ��(From)
	$gHgStr .= &linkP( "b=$BOARD_ESC&c=mvt&rfid=$id&roid=" . $parents .
	    $addNum, $H_REORDERFROM_MARK, '', $H_REORDERFROM_MARK_L ) . "\n";
    }

    # ������������ޥ��
    $gHgStr .= &linkP( "b=$BOARD_ESC&c=f&s=on&id=$id", $H_SUPERSEDE_ICON, '',
	$H_SUPERSEDE_ICON_L ) . "\n";
    $gHgStr .= &linkP( "b=$BOARD_ESC&c=dp&id=$id", $H_DELETE_ICON, '',
	$H_DELETE_ICON_L ) . "\n";

    # ��ư���ޥ��(To)
    if (( $gComType == 4 ) && ( $fromId ne $id ) && ( $parents eq '' ) && ( $fromId ne $id ))
    {
	$gHgStr .= &linkP( "b=$BOARD_ESC&c=mve&rtid=$id&rfid=$fromId&roid=$oldId" . $addNum, $H_REORDERTO_MARK, '', $H_REORDERTO_MARK_L ) . "\n";
    }

    # ������ѹ����ޥ��(To)
    if (( $gComType == 2 ) && ( $fromId ne $id ) &&
	( !grep( /^$fromId$/, split( /,/, &getArtDaughters( $id )))) &&
	( !grep( /^$fromId$/, split( /,/, $parents ))))
    {
	$gHgStr .= &linkP( "b=$BOARD_ESC&c=ce&rtid=$id&rfid=$fromId&roid=$oldId" . $addNum, $H_RELINKTO_MARK, '', $H_RELINKTO_MARK_L ) . "\n";
    }
}


###
## �񤭹��߽祿���ȥ����
#
sub uiSortTitle
{
    # Isolation level: READ UNCOMITTED.
    &lockBoard();
    &cacheArt( $BOARD );
    &unlockBoard();

    local( $nofMsg ) = &getNofArt();

    # ɽ������Ŀ������
    local( $Num ) = &cgi'tag( 'num' );
    local( $Old );
    if ( defined( &cgi'tag( 'id' )))
    {
	$Old = $nofMsg - int( &cgi'tag( 'id' ) + $Num/2 );
	$Old = 0 if ( $Old < 0 );
    }
    else
    {
	$Old = &cgi'tag( 'old' );
    }
    local( $Rev ) = &cgi'tag( 'rev' );
    $gFold = (( $SYS_THREAD_FORMAT == 2 ) || &cgi'tag( 'fold' ))? 1 : 0;
    $gVRev = $Rev? 1-$SYS_BOTTOMTITLE : $SYS_BOTTOMTITLE;
    $gTo = $nofMsg - $Old;
    $gFrom = $gTo - $Num + 1;
    $gFrom = 0 if (( $gFrom < 0 ) || ( $Num == 0 ));

    $gPageLinkStr = &pageLink( 'r', $Num, $Old, $Rev, '' );

    &htmlGen( 'SortTitle.xml' );
}

sub hg_sort_title_tree
{
    &fatal( 18, "$_[0]/SortTitleTree" ) if ( $_[0] ne 'SortTitle.xml' );

    $gHgStr .= "<ul>\n";

    # ������ɽ��
    local( $IdNum, $Id, $fid, $aids, $date, $title, $icon, $host, $name );

    local( $nofMsg ) = &getNofArt();
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
		$Id = &getArtId( $IdNum );
		( $fid, $aids, $date, $title, $icon, $host, $name ) = &getArtInfo( $Id );
		&dumpArtSummaryItem( $Id, $aids, $date, $title, $icon, $name, 1 );
		$gHgStr .= "</li>\n";
	    }
	}
	else
	{
	    for ($IdNum = $gTo; $IdNum >= $gFrom; $IdNum--)
	    {
		$Id = &getArtId( $IdNum );
		( $fid, $aids, $date, $title, $icon, $host, $name ) = &getArtInfo( $Id );
		&dumpArtSummaryItem( $Id, $aids, $date, $title, $icon, $name, 1 );
		$gHgStr .= "</li>\n";
	    }
	}
    }
    $gHgStr .= "</ul>\n";
}


###
## ����å��̵�������
#
sub uiShowThread
{
    # Isolation level: READ UNCOMITTED.
    &lockBoard();
    &cacheArt( $BOARD );
    &unlockBoard();

    $gId = &cgi'tag( 'id' );

    $gFids = &getArtParents( $gId );

    # �ե����������ڹ�¤�μ���
    # ex. '( a ( b ( c d ) ) ( e ) ( f ( g ) ) )'�Ȥ����ꥹ��
    @gFollowIdTree = ();
    &getFollowIdTree( $gId, *gFollowIdTree );

    &htmlGen( 'ShowThread.xml' );
}

sub hg_show_thread_title
{
    &fatal( 18, "$_[0]/ShowThreadTitle" ) if ( $_[0] ne 'ShowThread.xml' );
    $gHgStr .= &getArtSubject( &getTreeTopArticle( *gFollowIdTree ));
}

sub hg_show_thread_title_tree
{
    &fatal( 18, "$_[0]/ShowThreadTitleTree" ) if ( $_[0] ne 'ShowThread.xml' );

    &dumpOriginalArticles( $gFids );
    &dumpArtThread( 6, @gFollowIdTree );
}

sub hg_show_thread_msg_body
{
    &fatal( 18, "$_[0]/ShowThreadMsgBody" ) if ( $_[0] ne 'ShowThread.xml' );
    &dumpArtThread( 2, @gFollowIdTree );
}

sub hg_show_thread_back_to_title_button
{
    &fatal( 18, "$_[0]/ShowThreadBackToTitleButton" ) if ( $_[0] ne 'ShowThread.xml' );
    &dumpButtonToTitleList( $BOARD, $gId );
}


###
## �񤭹��߽��å���������
#
sub uiSortArticle
{
    # Isolation level: READ UNCOMITTED.
    &lockBoard();
    &cacheArt( $BOARD );
    &unlockBoard();

    $gNum = &cgi'tag( 'num' );
    $gOld = &cgi'tag( 'old' );
    $gRev = &cgi'tag( 'rev' );
    $gFold = (( $SYS_THREAD_FORMAT == 2 ) || &cgi'tag( 'fold' ))? 1 : 0;

    $gPageLinkStr = &pageLink( 'l', $gNum, $gOld, $gRev, '' );

    &htmlGen( 'SortArticle.xml' );
}

sub hg_sort_article_body
{
    &fatal( 18, "$_[0]/SortArticleBody" ) if ( $_[0] ne 'SortArticle.xml' );

    local( $vRev ) = $gRev? 1-$SYS_BOTTOMARTICLE : $SYS_BOTTOMARTICLE;
    local( $nofMsg ) = &getNofArt();
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
		$Id = &getArtId( $IdNum );
		&dumpArtBody( $Id, $SYS_COMMAND_EACH, 1 );
		$gHgStr .= $HTML_HR;
	    }
	}
	else
	{
	    for ( $IdNum = $To; $IdNum >= $From; $IdNum-- )
	    {
		$Id = &getArtId( $IdNum );
		&dumpArtBody( $Id, $SYS_COMMAND_EACH, 1 );
		$gHgStr .= $HTML_HR;
	    }
	}
    }
}


###
## ñ�쵭����ɽ��
#
sub uiShowArticle
{
    # Isolation level: READ UNCOMITTED.
    &lockBoard();
    &cacheArt( $BOARD );
    &unlockBoard();

    $gId = &cgi'tag( 'id' );

    # ̤��Ƶ������ɤ�ʤ�
    &fatal( 8, '' ) if ( &getArtSubject( $gId ) eq '' );

    &htmlGen( 'ShowArticle.xml' );
}

sub hg_show_article_title
{
    &fatal( 18, "$_[0]/ShowArticleTitle" ) if ( $_[0] ne 'ShowArticle.xml' );
    $gHgStr .= &getArtSubject( $gId );
}

sub hg_show_article_body
{
    &fatal( 18, "$_[0]/ShowArticleBody" ) if ( $_[0] ne 'ShowArticle.xml' );
    &dumpArtBody( $gId, 1, 1 );
}

sub hg_show_article_original
{
    &fatal( 18, "$_[0]/ShowArticleOriginal" ) if ( $_[0] ne 'ShowArticle.xml' );
    local( $fids ) = &getArtParents( $gId );
    if ( $fids ne '' )
    {
	$gHgStr .= "<p>$H_THREAD_ALL$H_PARENT</p>\n";
	&dumpOriginalArticles( $fids );
    }
}

sub hg_show_article_reply
{
    &fatal( 18, "$_[0]/ShowArticleReply" ) if ( $_[0] ne 'ShowArticle.xml' );

    $gHgStr .= "<p>$H_THREAD$H_REPLY</p>\n";
    &dumpReplyArticles( &getArtDaughters( $gId ));
}


###
## �����θ���(ɽ�����̤κ���)
#
sub uiSearchArticle
{
    # Isolation level: READ UNCOMITTED.
    &lockBoard();
    &cacheArt( $BOARD );
    &unlockBoard();

    &htmlGen( 'SearchArticle.xml' );
}

sub hg_search_article_result
{
    &fatal( 18, "$_[0]/SearchArticleResult" ) if ( $_[0] ne 'SearchArticle.xml' );

    local( $SearchView ) = &cgi'tag( 'searchthread' )? 1 : 0;
    local( $Key ) = &cgi'tag( 'key' );
    local( $SearchSubject ) = &cgi'tag( 'searchsubject' );
    local( $SearchPerson ) = &cgi'tag( 'searchperson' );
    local( $SearchArticle ) = &cgi'tag( 'searcharticle' );
    local( $SearchPostTimeFrom ) = &cgi'tag( 'searchposttimefrom' );
    local( $SearchPostTimeTo ) = &cgi'tag( 'searchposttimeto' );
    local( $SearchIcon ) = &cgi'tag( 'searchicon' );

    local( %iconHash );
    foreach ( &cgi'tag( 'icon' ))
    {
	next if ( $_ eq $H_NOICON );
	$iconHash{ $_ } = 1;
    }

    # ������ɴ�Ϣ�����оݤ����ꤵ��ʤ��ä����ϡ�������ɤ϶�������
    $Key = '' unless ( $SearchSubject || $SearchPerson || $SearchArticle );

    # �оݤ�����и���
    if (( $Key ne '' ) || ( $SearchPostTimeFrom || $SearchPostTimeTo ) || $SearchIcon )
    {
	&dumpSearchResult( $SearchView, $Key, $SearchSubject, $SearchPerson,
	    $SearchArticle, $SearchPostTimeFrom, $SearchPostTimeTo,
	    $SearchIcon, *iconHash );
    }
}


###
## ��������γ�ǧ
#
sub uiDeletePreview
{
    # Isolation level: READ UNCOMITTED.
    &lockBoard();
    &cacheArt( $BOARD );
    &unlockBoard();

    if ( !( $POLICY & 8 ) && ( $SYS_OVERWRITE == 0 ))
    {
	&fatal( 99, scalar( &cgi'tag( 'c' )));
    }

    $gId = &cgi'tag( 'id' );
    $gAids = &getArtDaughters( $gId );

    # ̤��Ƶ������ɤ�ʤ�
    &fatal( 8, '' ) if ( &getArtSubject( $gId ) eq '' );

    &htmlGen( 'DeletePreview.xml' );
}

sub hg_delete_preview_form
{
    &fatal( 18, "$_[0]/DeletePreviewForm" ) if ( $_[0] ne 'DeletePreview.xml' );

    local( %tags );
    %tags = ( 'c', 'de', 'b', $BOARD, 'id', $gId );
    &dumpForm( *tags, '���Υ�å������������ޤ�', '', '' );

    if ( $gAids )
    {
	%tags = ( 'c', 'det', 'b', $BOARD, 'id', $gId );
	&dumpForm( *tags, "$H_REPLY��å�������ޤȤ�ƺ�����ޤ�", '', '' );
    }
}

sub hg_delete_preview_body
{
    &fatal( 18, "$_[0]/DeletePreviewBody" ) if ( $_[0] ne 'DeletePreview.xml' );
    &dumpArtBody( $gId, 0, 1 );
}

sub hg_delete_preview_reply
{
    &fatal( 18, "$_[0]/DeletePreviewReply" ) if ( $_[0] ne 'DeletePreview.xml' );

    $gHgStr .= "<p>$H_THREAD$H_REPLY</p>\n";
    &dumpReplyArticles( $gAids );
}


###
## �����κ��
#
sub uiDeleteExec
{
    # Isolation level: SERIALIZABLE.
    &lockBoard();
    &cacheArt( $BOARD );

    if ( !( $POLICY & 8 ) && ( $SYS_OVERWRITE == 0 ))
    {
	&fatal( 99, scalar( &cgi'tag( 'c' )));
    }

    local( $threadFlag ) = @_;

    $gId = &cgi'tag( 'id' );

    local( $name ) = &getArtAuthor( $gId );
    &fatal( 44, '' ) if ( !&isUser( $name ) && !( $POLICY & 8 ));
    &fatal( 19, '' ) if (( &getArtDaughters( $gId ) ne '' ) && !( $POLICY & 8 ) && ( $SYS_OVERWRITE == 1 ));

    # ����¹�
    &deleteArticle( $gId, $BOARD, $threadFlag );

    &htmlGen( 'DeleteExec.xml' );

    &unlockBoard();
}

sub hg_delete_exec_back_to_title_button
{
    &fatal( 18, "$_[0]/DeleteExecBackToTitleButton" ) if ( $_[0] ne 'DeleteExec.xml' );
    &dumpButtonToTitleList( $BOARD, $gId );
}


###
## ��������ɽ��
#
sub uiShowIcon
{
    # Isolation level: CHAOS.

    &htmlGen( 'ShowIcon.xml' );
}


###
## �إ��ɽ��
#
sub uiHelp
{
    # Isolation level: CHAOS.

    &htmlGen( 'Help.xml' );
}


###
## ���顼ɽ��
#
sub uiFatal
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

    $gHgStr .= sprintf( qq(<link rel="StyleSheet" href="%s" type="text/css" media="screen" />), &getStyleSheetURL( $STYLE_FILE )) if $STYLE_FILE;
}

sub hg_s_address
{
    $gHgStr .= "<address>\nMaintenance: " .
	&tagA( $MAINT_NAME, "mailto:$MAINT" ) . $HTML_BR .
	&tagA( $PROGNAME, 'http://www.jin.gr.jp/~nahi/kb/' ) .
	": Copyright &copy; 1995-2000 " .
	&tagA( 'NAKAMURA, Hiroshi', 'http://www.jin.gr.jp/~nahi/' ) .
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
    $gHgStr .= "����: " . &getDateTimeFormatFromUtc( $^T );
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
    $gHgStr .= &getDateTimeFormatFromUtc( $^T );
}

sub hg_c_top_menu
{
    $gHgStr .= qq(<div class="kbTopMenu">\n);
    local( $formStr );

    local( %tags );
    if ( $SYS_AUTH )
    {
	$formStr .= &linkP( 'c=bl', 'TOP', 'J' ) . "\n";
#	$formStr .= ' ' . &linkP( 'c=ue', 'OPEN', 'O' ) . "\n";
	$formStr .= ' ' . &linkP( 'c=lo', 'LOGIN', 'L' ) . "\n";
	if ( $UNAME && ( $UNAME ne $GUEST ) && ( $UNAME ne $cgiauth'F_COOKIE_RESET ))
	{
	    $formStr .= ' ' . &linkP( 'c=uc', 'INFO', 'C' ) . "\n";
	}
	$formStr .= "&nbsp;&nbsp;&nbsp;\n";
    }

    if ( $BOARD )
    {
	$tags{ 'b' } = $BOARD;
	$formStr .= &tagLabel( "ɽ������", 'c', 'W' ) . ": \n";

	local( $contents );
	$contents .= sprintf( qq[<option%s value="v">�ǿ�$H_SUBJECT����(����å�)</option>\n], ( $SYS_TITLE_FORMAT == 0 )? ' selected="selected"' : '' );
	$contents .= sprintf( qq[<option%s value="r">�ǿ�$H_SUBJECT����(�񤭹��߽�)</option>\n], ( $SYS_TITLE_FORMAT == 1 )? ' selected="selected"' : '' );
	$contents .= qq[<option value="vt">�ǿ�$H_MESG����(����å�)</option>\n];
	$contents .= qq[<option value="l">�ǿ�$H_MESG����(�񤭹��߽�)</option>\n];
	$contents .= qq(<option value="v">&nbsp;</option>\n);
	$contents .= qq(<option value="s">$H_MESG�θ���</option>\n);
	$contents .= qq(<option value="i">�Ȥ���$H_ICON����</option>\n) if $SYS_ICON;
	if (( $POLICY & 2 ) && ( !$SYS_NEWART_ADMINONLY || ( $POLICY & 8 )))
	{
	    $contents .= qq(<option value="v">&nbsp;</option>\n);
	    $contents .= qq(<option value="n">$H_POSTNEWARTICLE</option>\n);
	}

	$formStr .= &tagSelect( 'c', $contents );
    }
    else
    {
	$tags{ 'c' } = $SYS_TITLE_FORMAT? 'r' : 'v';
	$formStr .= &tagLabel( "ɽ������", 'b', 'W' ) . ": \n";

	local( $contents, $boardId );
	$boardId = &getBoardId( 0 );
	$contents .= qq(<option selected="selected" value="$boardId">) . &getBoardName( $boardId ) . "</option>\n";
	foreach ( 1 .. &getNofBoard() )
	{
	    $boardId = &getBoardId( $_ );
	    $contents .= qq(<option value="$boardId">) . &getBoardName( $boardId ) . "</option>\n";
	}

	$formStr .= &tagSelect( 'b', $contents );
    }

    $formStr .= "\n&nbsp;&nbsp;&nbsp;" .
	&tagLabel( "ɽ�����", 'num', 'Y' ) . ': ' .
	&tagInputText( 'text', 'num', (( &cgi'tag( 'num' ) ne '' )? scalar( &cgi'tag( 'num' )) : $DEF_TITLE_NUM ),	3 );

    $tags{ 'old' } = &cgi'tag( 'old' ) if ( defined &cgi'tag( 'old' ));
    $tags{ 'rev' } = &cgi'tag( 'rev' ) if ( defined &cgi'tag( 'rev' ));
    $tags{ 'fold' } = &cgi'tag( 'fold' ) if ( defined &cgi'tag( 'fold' ));
    &dumpForm( *tags, 'ɽ��(V)', '', *formStr );
    $gHgStr .= "</div>\n";
}

sub hg_c_help
{
    $gHgStr .= &linkP( "b=$BOARD_ESC&c=h", &tagComImg( $ICON_HELP, '�إ��' ), 'H', '', '', $_[1] );
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
    $gHgStr .= '<dd>��' . &linkP( 'c=ue', "$H_USER��������Ⱥ����ڡ���" .
	&tagAccessKey( 'O' ), 'O' ) . "</dd>\n";

    if ( $UNAME )
    {
	$gHgStr .= "<dt>���̤�$H_USER�����ƤӽФ��סʸ����������$H_USER����ϡ�$UNAME�Τ�ΤǤ���</dt>\n";
	$gHgStr .= '<dd>��' . &linkP( 'c=lo', "������ڡ���" . &tagAccessKey( 'L' ), 'L' ) . "</dd>\n";
    }

    if ( $POLICY & 4 )
    {
	$gHgStr .= "<dt>��$UNAME�ˤĤ�����Ͽ����$H_USER������ѹ������</dt>\n";
	$gHgStr .= '<dd>��' . &linkP( 'c=uc', "$H_USER����ڡ���" . &tagAccessKey( 'C' ), 'C' ) . "</dd>\n";
    }

    if ( $POLICY & 8 )
    {
	$gHgStr .= "<dt>�ֿ�����$H_BOARD���ꤿ����</dt>\n";
	$gHgStr .= '<dd>��' . &linkP( 'c=be', "$H_BOARD�ο�������" .
	    &tagAccessKey( 'A' ), 'A' ) . "</dd>\n";
    }

    $gHgStr .= "</dl>\n";
}

sub hg_c_page_link
{
    $gHgStr .= $gPageLinkStr;
}

sub hg_c_board_link_all
{
    $gHgStr .= "<ul>\n";

    local( $board, $newIcon, $modTimeUtc, $modTime, $boardEsc );
    foreach ( 0 .. &getNofBoard() )
    {
	$board = &getBoardId( $_ );
	$modTimeUtc = &getBoardLastmod( $board );
	$modTime = &getDateTimeFormatFromUtc( $modTimeUtc );
	if ( $SYS_BLIST_NEWICON_DATE &&
	    (( $^T - $modTimeUtc ) < $SYS_BLIST_NEWICON_DATE * 86400 ))
	{
	    $newIcon = " " . &tagArtImg( $H_NEWARTICLE );
	}
	else
	{
	    $newIcon = '';
	}

	$boardEsc = &uriEscape( $board );
	$gHgStr .= '<li>' .
	    &linkP( "b=$boardEsc&c=" . ( $SYS_TITLE_FORMAT? 'r' : 'v' ) .
	    "&num=$DEF_TITLE_NUM", &getBoardName( $board )) .
	    "$newIcon\n[�ǿ�: $modTime]\n";
	if ( $POLICY & 8 )
	{
	    $gHgStr .= &linkP( "b=$boardEsc&c=bc", "�������ѹ�" ) . "\n";
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

    $modTimeUtc = &getBoardLastmod( $board );
    $modTime = &getDateTimeFormatFromUtc( $modTimeUtc );
    if ( $SYS_BLIST_NEWICON_DATE &&
	(( $^T - $modTimeUtc ) < $SYS_BLIST_NEWICON_DATE * 86400 ))
    {
	$newIcon = " " . &tagArtImg( $H_NEWARTICLE );
    }
    else
    {
	$newIcon = '';
    }

    local( $boardEsc ) = &uriEscape( $board );
    $gHgStr .= &linkP( "b=$boardEsc&c=$com&num=$num", &getBoardName( $board )) . "$newIcon\n[�ǿ�: $modTime]\n";
    if ( $POLICY & 8 )
    {
	$gHgStr .= &linkP( "b=$boardEsc&c=bc", "�������ѹ�" ) . "\n";
    }
}

sub hg_c_anchor
{
    $gHgStr .= &tagA( split( ',', $_[1] ));
}

sub hg_c_icon_msg
{
    $gHgStr .= &tagArtImg( $_[1] );
}

sub hg_c_icon
{
    local( $src, $alt ) = split( ',', $_[1], 2 );
    $gHgStr .= &tagComImg( &getIconURL( $src ), $alt );
}

sub hg_c_img
{
    local( $src, $alt, $width, $height ) = split( ',', $_[1], 4 );
    $gHgStr .= &tagImg( &getImgURL( $src ), $alt, $width, $height, 'kbImg' );
}

sub hg_b_board_name
{
    $gHgStr .= $BOARDNAME if $BOARD;
}

sub hg_b_board_header
{
    &dumpBoardHeader() if $BOARD;
}

sub hg_b_post_entry_form
{
    if ( $POLICY & 2 )
    {
	&dumpArtEntry( $gDefIcon, $gEntryType, $gId, $gDefPostDateStr, $gDefSubject, $gDefTextType, $gDefArticle, $gDefName, $gDefEmail, $gDefUrl, $gDefFmail );
    }
}

sub hg_b_search_article_form
{
    local( $SearchThread ) = &cgi'tag( 'searchthread' );
    local( $Key ) = &cgi'tag( 'key' );
    local( $SearchSubject ) = &cgi'tag( 'searchsubject' );
    local( $SearchPerson ) = &cgi'tag( 'searchperson' );
    local( $SearchArticle ) = &cgi'tag( 'searcharticle' );
    local( $SearchPostTimeFrom ) = &cgi'tag( 'searchposttimefrom' );
    local( $SearchPostTimeTo ) = &cgi'tag( 'searchposttimeto' );
    local( $SearchIcon ) = &cgi'tag( 'searchicon' );

    local( %iconHash );
    foreach ( &cgi'tag( 'icon' ))
    {
	next if ( $_ eq $H_NOICON );
	$iconHash{ $_ } = 1;
    }

    local( $msg, $contents );
    $contents = &tagInputCheck( 'searchsubject', $SearchSubject ) . ': ' . &tagLabel( $H_SUBJECT, 'searchsubject', 'T' ) . $HTML_BR;

    $contents .= &tagInputCheck( 'searchperson', $SearchPerson ) . ': ' . &tagLabel( "̾��", 'searchperson', 'N' ) . $HTML_BR;

    $contents .= &tagInputCheck( 'searcharticle', $SearchArticle ) . ': ' . &tagLabel( $H_MESG, 'searcharticle', 'A' ) . $HTML_BR;

    $contents .= &tagLabel( '�������', 'key', 'K' ) . ': ' . &tagInputText( 'text', 'key', $Key, $KEYWORD_LENGTH ) . $HTML_BR . $HTML_BR;

    $contents .= $H_DATE . ': ' . &tagInputText( 'text', 'searchposttimefrom', ( $SearchPostTimeFrom || '' ), 11 ) . ' ' .
	&tagLabel( '����', 'searchposttimefrom', 'S' ) .
	"&nbsp;&nbsp;&nbsp;\n" .
	&tagInputText( 'text', 'searchposttimeto', ( $SearchPostTimeTo || '' ), 11 ) . &tagLabel( '�δ�', 'searchposttimeto', 'E' ) . $HTML_BR;

    if ( $SYS_ICON )
    {
	$contents .= $HTML_BR . &tagLabel( $H_ICON, 'icon', 'I' ) . ": \n";

	# �������������
	local( $selContents, $iconId );
	foreach ( 0 .. &getNofBoardIcon() )
	{
	    $iconId = &getBoardIconId( $_ );
	    $selContents .= sprintf( "<option%s>$iconId</option>\n", ( $iconHash{ $iconId } )? ' selected="selected"' : '' );
	}
	$contents .= &tagSelect( 'icon', $selContents, $SELECT_ROWS, 1 ) . "\n";

	$contents .= "�Ȥ���$H_ICON\n";

	$selContents = sprintf( qq[<option%s value="0">&nbsp;</option>\n], ( $SearchIcon == 0 )? ' selected="selected"' : '' );
	$selContents .= sprintf( qq[<option%s value="1">�Ǥ���</option>\n], ( $SearchIcon == 1 )? ' selected="selected"' : '' );
	$selContents .= sprintf( qq[<option%s value="3">��$H_PARENT�Ǥ���</option>\n], ( $SearchIcon == 3 )? ' selected="selected"' : '' );
	$selContents .= sprintf( qq[<option%s value="2">�Ȥ���$H_REPLY�����</option>\n], ( $SearchIcon == 2 )? ' selected="selected"' : '' );
	$selContents .= qq(<option value="0">&nbsp;</option>\n);
	$selContents .= sprintf( qq[<option%s value="11">�򥹥�å���˴ޤ�</option>\n], ( $SearchIcon == 11 )? ' selected="selected"' : '' );
	$selContents .= sprintf( qq[<option%s value="12">������åɤ���Ƭ�ˤ���</option>\n], ( $SearchIcon == 12 )? ' selected="selected"' : '' );
	$selContents .= sprintf( qq[<option%s value="13">������åɤ���ü�ˤ���</option>\n], ( $SearchIcon == 13 )? ' selected="selected"' : '' );

	$contents .= &tagSelect( 'searchicon', $selContents );

	# �����������
	$contents .= ' (' . &linkP( "b=$BOARD_ESC&c=i", "�Ȥ���$H_ICON����" .
	    &tagAccessKey( 'H' ), 'H' ) . ')' . $HTML_BR;

#	$contents .= &tagInputCheck( 'searchicon', $SearchIcon ) . ': ' . &tagLabel( $H_ICON, 'searchicon', 'I' ) . " // \n";

    }
    $contents .= $HTML_BR . &tagInputCheck( 'searchthread', $SearchThread ) . ': ' . &tagLabel( '����åɤ򸡺�����', 'searchthread', 'Z' ) . $HTML_BR;

    $msg .= &tagFieldset( "�����о�$HTML_BR", $contents ) . $HTML_BR;

    %tags = ( 'c', 's', 'b', $BOARD );
    &dumpForm( *tags, '����', '�ꥻ�å�', *msg );
}

sub hg_b_all_icon
{
    return unless $BOARD;
    $gHgStr .= "<ul>\n";

    local( $id );
    foreach ( 0 .. &getNofBoardIcon() )
    {
	$id = &getBoardIconId( $_ );
	$gHgStr .= '<li>' . &tagArtImg( $id ) . " : [$id] " . ( &getBoardIconHelp( $id ) || $id ) . "</li>\n";
    }
    $gHgStr .= "</ul>\n";
}


###
## dumpBoardHeader - �Ǽ��ĥإå���ɽ��
#
# - SYNOPSIS
#	&dumpBoardHeader();
#
# - DESCRIPTION
#	�Ǽ��ĤΥإå���ɽ�����롥
#
sub dumpBoardHeader
{
    local( $msg );
    &getBoardHeader( $BOARD, *msg );
    
    LINE: while ( 1 )
    {
	if (( index( $msg, '<kb' ) >= 0 ) &&
	    ( $msg =~ s!<kb:(\w+)(\s*var="([^"]*)")?\s+/>!!o ))
	{
	    $gHgStr .= $`;
	    eval( '&hg_' . $1 . '( "' . $source . '", "' . $3 . '" );' );
	    &fatal( 998, "$file : $@" ) if $@;
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
## dumpArtEntry - ��å��������ϥե������ɽ��
#
# - SYNOPSIS
#	&dumpArtEntry( $icon, $type, $id, $postDateStr, $title, $texttype, $article, $name, $eMail, $url, $fMail );
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
sub dumpArtEntry
{
    local( $icon ) = @_;

#    if ( &getBoardIconType( $icon ) eq 'cfv' )
#    {
#	# TBD
#    }
#    elsif ( &getBoardIconType( $icon ) eq 'vote' )
#    {
#	# TBD
#    }
#    else
#    {
	&dumpArtEntryNormal( @_ );
#    }
}


# �̾��å�����
sub dumpArtEntryNormal
{
    local( $icon, $type, $id, $postDateStr, $title, $texttype, $article, $name, $eMail, $url, $fMail ) = @_;

    $texttype = $texttype || $H_TTLABEL[ $SYS_TT_DEFAULT ];
    $icon = $icon || $SYS_ICON_DEFAULT;

    local( $msg, $iconId );
    local( $contents ) = '';

    # �������������
    if ( $SYS_ICON )
    {
	$msg .= &tagLabel( $H_ICON, 'icon', 'I' ) . " :\n";
	$contents = sprintf( "<option%s>$H_NOICON</option>\n", (( $icon eq $H_NOICON )? ' selected="selected"' : '' ));
	foreach ( 0 .. &getNofBoardIcon() )
	{
	    $iconId = &getBoardIconId( $_ );
	    $contents .= sprintf( "<option%s>$iconId</option>\n", ( $iconId eq $icon )? ' selected="selected"' : '' );
	}
	$msg .= &tagSelect( 'icon', $contents ) . "\n";

	$msg .= '(' . &linkP( "b=$BOARD_ESC&c=i", "�Ȥ���$H_ICON����" .
	    &tagAccessKey( 'H' ), 'H' ) . ')' . $HTML_BR;
    }

    $msg .= &tagLabel( $H_SUBJECT, 'subject', 'T' ) . ': ' .
	&tagInputText( 'text', 'subject', $title, $SUBJECT_LENGTH ) . $HTML_BR;
    
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
		    $contents .= &tagInputRadio( 'texttype_' . $ttBit, 'texttype', $H_TTLABEL[$ttBit], 1 );
		    $labelTarget = 'texttype_' . $ttBit;
		}
		else
		{
		    $contents .= &tagInputRadio( 'texttype_' . $ttBit, 'texttype', $H_TTLABEL[$ttBit], 0 );
		}
		$contents .= &tagLabel( $H_TTLABEL[$ttBit], 'texttype_' . $ttBit, '' );
	    }
	    $ttBit++;
	}
	$contents .= $HTML_BR;
	$msg .= &tagFieldset( &tagLabel( $H_TEXTTYPE, $labelTarget, 'Z' ) . ': ', $contents );
    }
    else
    {
	$msg .= sprintf( qq(<input name="texttype" type="hidden" value="%s" />), $H_TTLABEL[(( log $SYS_TEXTTYPE ) / ( log 2 ))] ) . $HTML_BR;
    }

    $msg .= &tagLabel( $H_MESG, 'article', 'A' ) . ':' . $HTML_BR .
	&tagTextarea( 'article', $article, $TEXT_ROWS, $TEXT_COLS ) . $HTML_BR;

    if ( $POLICY & 8 )
    {
	# �������¤����̰���
	$msg .= &tagLabel( $H_DATE, 'postdate', 'T' ) . ': ' .
	    &tagInputText( 'text', 'postdate', $postDateStr, 20 ) .
	    qq[('yyyy/mm/dd(HH:MM:SS)'�η����ǻ���)] . $HTML_BR;
	$msg .= &tagLabel( $H_FROM, 'name', 'N' ) . ': ' .
	    &tagInputText( 'text', 'name', $name, $NAME_LENGTH ) . $HTML_BR;
	$msg .= &tagLabel( $H_MAIL, 'mail', 'M' ) . ': ' .
	    &tagInputText( 'text', 'mail', $eMail, $MAIL_LENGTH ) . $HTML_BR;
	$msg .= &tagLabel( $H_URL, 'url', 'U' ) . ': ' .
	    &tagInputText( 'text', 'url', ( $url || 'http://' ), $URL_LENGTH ) . $HTML_BR;
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
	$msg .= &tagLabel( $H_FROM, 'name', 'N' ) . ': ' .
	    &tagInputText( 'text', 'name', $name, $NAME_LENGTH ) . $HTML_BR;
	$msg .= &tagLabel( $H_MAIL, 'mail', 'M' ) . ': ' .
	    &tagInputText( 'text', 'mail', $eMail, $MAIL_LENGTH ) . $HTML_BR;
	$msg .= &tagLabel( $H_URL, 'url', 'U' ) . ': ' .
	    &tagInputText( 'text', 'url', ( $url || 'http://' ), $URL_LENGTH ) . $HTML_BR;
    }

    if (( $SYS_MAIL & 2 ) && ( $UMAIL ne '' ))
    {
	$msg .= &tagLabel( "��ץ饤�����ä�����$H_MAIL��Ϣ��", 'fmail', 'F' ) . ': ' . &tagInputCheck( 'fmail', $fMail ) . "\n";
    }
    $msg .= "</p>\n<p>\n";

    $contents = &tagInputRadio( 'com_p', 'com', 'p', 1 ) . ":\n" .
	&tagLabel( '���ɽ�����Ƥߤ�(�ޤ���Ͽ���ޤ���)', 'com_p', 'P' ) .
	$HTML_BR;
    local( $doLabel );
    if ( $type eq 'supersede' )
    {
	$doLabel = '��������';
    }
    else
    {
	$doLabel = "$H_MESG����Ͽ����";
    }
    $contents .= &tagInputRadio( 'com_x', 'com', 'x', 0 ) . ":\n" .
	&tagLabel( $doLabel, 'com_x', 'X' ) . $HTML_BR;
    $msg .= &tagFieldset( "���ޥ��$HTML_BR", $contents );

    local( $op ) = ( -M &getPath( $SYS_DIR, $BOARD_FILE ));
    local( %tags ) = ( 'corig', scalar( &cgi'tag( 'c' )), 'b', $BOARD, 'c', 'p', 'id', $id, 's', ( $type eq 'supersede' ), 'op', $op );

    &dumpForm( *tags, '�¹�', '', *msg );
}


###
## dumpArtBody - ��å��������Τ�ɽ��
#
# - SYNOPSIS
#	&dumpArtBody( $Id, $CommandFlag, $OriginalFlag, @articleInfo );
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
sub dumpArtBody
{
    local( $id, $commandFlag, $origFlag, @articleInfo ) = @_;

    local( $fid, $aids, $date, $title, $icon, $host, $name, $eMail, $url );

    local( $body ) = '';
    if ( $id ne '' )
    {
	( $fid, $aids, $date, $title, $icon, $host, $name, $eMail, $url ) = &getArtInfo( $id );
	local( @articleBody );
	&getArtBody( $id, $BOARD, *articleBody );
	$body = join( '', @articleBody );
    }
    else
    {
	( $fid, $aids, $date, $title, $icon, $host, $name, $eMail, $url, $body ) = @articleInfo;
    }

    # ̤��Ƶ������ɤ�ʤ�
    &fatal( 8, '' ) if ( $title eq '' );

    $gHgStr .= qq(<div class="kbArticle">\n);

    # �����ȥ�
    &dumpArtTitle( $id, $title, $icon );

    local( $origId );
    if ( $fid ne '' )
    {
	( $origId = $fid ) =~ s/,.*$//o;
    }

    if ( $commandFlag && $SYS_COMMAND )
    {
	local( $num ) = &getArtNum( $id );
	local( $prevId ) = &getArtId( $num - 1 );
	local( $nextId ) = &getArtId( $num + 1 );
	&dumpArtCommand( $id, $origId, $prevId, $nextId, ( $aids ne '' ),
	    (( &isUser( $name ) && (( $aids eq '' ) || ( $SYS_OVERWRITE == 2 ))) || ( $POLICY & 8 )));
    }

    # �إå��ʥ桼������ȥ�ץ饤��: �����ȥ�Ͻ�����
    &dumpArtHeader( $name, $eMail, $url, $host, $date, ( $origFlag? $origId : '' ));

    # �ڤ���
    $gHgStr .= $H_LINE;

#    if ( &getBoardIconType( $icon ) eq 'cfv' )
#    {
#	# TBD
#    }
#    elsif ( &getBoardIconType( $icon ) eq 'vote' )
#    {
#	# TBD
#    }
#    else
#    {
	&dumpArtBodyNormal( *body );
#    }

    $gHgStr .= "</div>\n";

    &cgiprint'cache( $gHgStr ); $gHgStr = '';
}


# �̾��å�����
sub dumpArtBodyNormal
{
    local( *body ) = @_;
    $gHgStr .= qq(<div class="body">) . &articleEncode( *body ) . "</div>\n";
}


###
## dumpArtThread - �ե�������������ɽ����
#
# - SYNOPSIS
#	&dumpArtThread( $State, $Head, @Tail );
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
#	�ܺ٤�&getFollowIdTree�Υ���ץ������ʬ�򻲾ȤΤ��ȡ�
#
sub dumpArtThread
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
	    local( $dFid, $dAids, $dDate, $dSubject, $dIcon, $dRemoteHost, $dName ) = &getArtInfo( $Head );
	    &dumpArtSummaryItem( $Head, $dAids, $dDate, $dSubject, $dIcon, $dName, $State&3 );
	    $gHgStr .= "</li>\n";
	    $State ^= 1 if ( $State&1 );
	}
    }
    elsif (( $Head ne '(' ) && ( $Head ne ')' ))
    {
	# ��������ɽ��(���ޥ���դ�, �������ʤ�)
	$gHgStr .= $HTML_HR;
	&dumpArtBody( $Head, $SYS_COMMAND_EACH, 0 );
    }

    &cgiprint'cache( $gHgStr ); $gHgStr = '';
    # tail recuresive.
    &dumpArtThread( $State, @Tail ) if @Tail;
}


###
## dumpSearchResult - ��������
#
# - SYNOPSIS
#	&dumpSearchResult( $type, $Key, $Subject, $Person, $Article, $PostTimeFrom, $PostTimeTo, $IconType, *iconHash );
#
# - ARGS
#	$type		ɽ������
#			  0 ... ��å�����ɽ��
#			  1 ... ����å�ɽ��
#	$Key		�������
#	$Subject	�����ȥ�򸡺����뤫�ݤ�
#	$Person		��ƼԤ򸡺����뤫�ݤ�
#	$Article	��ʸ�򸡺����뤫�ݤ�
#	$PostTimeFrom	��������
#	$PostTimeTo	��λ����
#	$IconType	��������θ�����ˡ
#	%iconHash	�������������ѥϥå��塥
#			  $iconHash{ '��������' }�����Υ������󤬸�������롥
#
# - DESCRIPTION
#	�����򸡺�����ɽ������
#
sub dumpSearchResult
{
    local( $type, $Key, $Subject, $Person, $Article, $PostTimeFrom, $PostTimeTo, $IconType, *iconHash ) = @_;

    local( @KeyList ) = split( /\s+/, $Key );
    local( $postTime ) = ( $PostTimeTo || $PostTimeFrom );

    # �ꥹ�ȳ���
    $gHgStr .= "<ul>\n";

    # �������󸡺��Υ���å���򥯥ꥢ
    %gSearchIconResult = ();

    # ����å�ɽ���ѥ���å���
    local( %dumpThread );

    local( $dId, $dFid, $dAids, $dDate, $dTitle, $dIcon, $dRemoteHost, $dName, $dEmail );
    local( $SubjectFlag, $PersonFlag, $PostTimeFlag, $ArticleFlag );
    local( $HitNum, $Line, $FromUtc, $ToUtc );
    foreach ( $[ .. &getNofArt() )
    {
	# ��������
	$dId = &getArtId( $_ );
	( $dFid, $dAids, $dDate, $dTitle, $dIcon, $dRemoteHost, $dName, $dEmail ) = &getArtInfo( $dId );

	# �ѿ��Υꥻ�å�
	$SubjectFlag = $PersonFlag = $PostTimeFlag = $ArticleFlag = 0;
	$Line = '';

	# ������������å�
	next if ( $IconType && !&searchArticleIcon( $dId, $IconType, *iconHash ));

	# ��ƻ���򸡺�
	if ( $postTime )
	{
	    $FromUtc = $ToUtc = -1;
	    $FromUtc = &getUtcFromYYYY_MM_DD( $PostTimeFrom ) if $PostTimeFrom;
	    $ToUtc = &getUtcFromYYYY_MM_DD( $PostTimeTo ) if $PostTimeTo;
	    $ToUtc += 86400 if ( $ToUtc >= 0 );
	    next if !&checkSearchTime( $dDate, $FromUtc, $ToUtc );
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
		if ( $Line = &searchArticleKeyword( $dId, $BOARD, @KeyList ))
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

	next unless ( $SubjectFlag || $PersonFlag || $ArticleFlag );

	# ����å�ɽ���ξ��
	if ( $type == 1 )
	{
	    next if ( defined( $dumpThread[ &getArtParentTop( $dId ) ] ));

	    # ����å���Ƭ���������פ�����ΤȤ��롥
	    $dId = &getArtParentTop( $dId );
	    $dumpThread[ $dId ] = 1;
	    ( $dFid, $dAids, $dDate, $dTitle, $dIcon, $dRemoteHost, $dName, $dEmail ) = &getArtInfo( $dId );
	}

	# ���׷���Υ������
	$HitNum++;

	# �����ؤΥ�󥯤�ɽ��
	&dumpArtSummaryItem( $dId, $dAids, $dDate, $dTitle, $dIcon, $dName, 1 );

	# ��ʸ�˹��פ���������ʸ��ɽ��
	if ( $ArticleFlag )
	{
	    $Line =~ s/<[^>]*>//go;
	    $gHgStr .= "<blockquote>$Line</blockquote>\n";
	}
	$gHgStr .= "</li>\n";
    }

    # �����оݤ�ɽ��ʸ����
    local( $target );
    if ( $type == 0 )
    {
	$target = $H_MESG;
    }
    elsif ( $type == 1 )
    {
	$target = '����å�';
    }

    if ( $HitNum )
    {
	$gHgStr .= "</ul>\n<ul>\n";
	$gHgStr .= "<li>$HitNum���$target�����Ĥ���ޤ�����</li>\n";
    }
    else
    {
	$gHgStr .= "<li>��������$target�ϸ��Ĥ���ޤ���Ǥ�����</li>\n";
    }

    # �ꥹ���Ĥ���
    $gHgStr .= "</ul>\n";
}


###
## dumpOriginalArticles - ���ꥸ�ʥ뵭���ؤΥ�󥯤�ɽ��
#
# - SYNOPSIS
#	&dumpOriginalArticles( $fids );
#
# - ARGS
#	$fids	���ꥸ�ʥ뵭��ID�ǡ���
#
# - DESCRIPTION
#	���ꥸ�ʥ뵭���ؤΥ�󥯤�ɽ�����롥
#
sub dumpOriginalArticles
{
    if ( $_[0] ne '' )
    {
	# ���ꥸ�ʥ뵭��������ʤ��

	$gHgStr .= "<ul>\n";

	local( $dId, $dFid, $dAids, $dDate, $dTitle, $dIcon, $dHost, $dName );
	foreach $dId ( reverse( split( /,/, $_[0] )))
	{
	    ( $dFid, $dAids, $dDate, $dTitle, $dIcon, $dHost, $dName ) = &getArtInfo( $dId );
	    &dumpArtSummaryItem( $dId, $dAids, $dDate, $dTitle, $dIcon, $dName, 0 );
	}
	$gHgStr .= "</ul>\n";
    }
    else
    {
	# �ʤˤ�ɽ�����ʤ���
    }
}


###
## dumpReplyArticles - ��ץ饤�����ؤΥ�󥯤�ɽ��
#
# - SYNOPSIS
#	&dumpReplyArticles( $aids );
#
# - ARGS
#	$aids	��ץ饤����ID�ǡ���
#
# - DESCRIPTION
#	��ץ饤�����ؤΥ�󥯤�ɽ�����롥
#
sub dumpReplyArticles
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
	    &getFollowIdTree( $id, *tree );
	    
	    # �ᥤ��ؿ��θƤӽФ�(��������)
	    &dumpArtThread( 4, @tree );
	}
    }
    else
    {
	# ȿ������̵��

	$gHgStr .= "<ul>\n<li>���ߡ�����$H_MESG�ؤ�$H_REPLY�Ϥ���ޤ���</li>\n</ul>\n";
    }
}


###
## dumpArtTitle - ���������ȥ��ɽ��
#
# - SYNOPSIS
#	&dumpArtTitle( $id, $title, $icon );
#
# - ARGS
#	$id	����ID
#	$title	�����ȥ�
#	$icon	��������
#
sub dumpArtTitle
{
    local( $id, $title, $icon ) = @_;
    local( $markUp );

    if ( $id ne '' )
    {
	$markUp .= &tagArtImg( $icon ) . " <small>$id.</small> " . $title;
    }
    else
    {
	$markUp .= &tagArtImg( $icon ) . ' ' . $title;
    }
    $gHgStr .= '<h2>' . &tagA( $markUp, '', '', '', "a$id" ) . "</h2>\n";
}


###
## dumpArtCommand - �������ޥ�ɤ�ɽ��
#
# - SYNOPSIS
#	&dumpArtCommand( $id, $upId, $prevId, $nextId, $reply, $delete );
#
# - ARGS
#	$id	����ID
#	$upId	�嵭��ID
#	$prevId	������ID
#	$nextId	������ID
#	$reply	��ץ饤���������뤫
#	$delete	�������������ǽ��
#
sub dumpArtCommand
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
	$gHgStr .= &linkP( "b=$BOARD_ESC&c=e&id=$upId", &tagComImg( $ICON_UP, $H_UPARTICLE ), 'U' ) . "\n";
    }
    else
    {
	$gHgStr .= &tagComImg( $ICON_UP_X, $H_UPARTICLE, ) . "\n";
    }
	
    if ( $prevId ne '' )
    {
	$gHgStr .= $dlmtS . &linkP( "b=$BOARD_ESC&c=e&id=$prevId", &tagComImg( $ICON_PREV, $H_PREVARTICLE ), 'P' ) . "\n";
    }
    else
    {
	$gHgStr .= $dlmtS . &tagComImg( $ICON_PREV_X, $H_PREVARTICLE, ) . "\n";
    }
	
    if ( $nextId ne '' )
    {
	$gHgStr .= $dlmtS . &linkP( "b=$BOARD_ESC&c=e&id=$nextId", &tagComImg( $ICON_NEXT, $H_NEXTARTICLE ), 'N' ) . "\n";
    }
    else
    {
	$gHgStr .= $dlmtS . &tagComImg( $ICON_NEXT_X, $H_NEXTARTICLE, ) . "\n";
    }

    if ( $reply )
    {
	$gHgStr .= $dlmtS . &linkP( "b=$BOARD_ESC&c=t&id=$id", &tagComImg( $ICON_DOWN, $H_THREAD_L ), 'M' ) . "\n";
    }
    else
    {
	$gHgStr .= $dlmtS . &tagComImg( $ICON_DOWN_X, $H_THREAD_L ) . "\n";
    }

    $gHgStr .= $dlmtL;

    if ( $POLICY & 2 )
    {
	if ( $SYS_REPLYQUOTE )
	{
	    $gHgStr .= $dlmtS . &linkP( "b=$BOARD_ESC&c=q&id=$id", &tagComImg( $ICON_QUOTE, $H_REPLYTHISARTICLE ), 'Q' ) . "\n";
	}
	else
	{
	    $gHgStr .= $dlmtS . &linkP( "b=$BOARD_ESC&c=f&id=$id", &tagComImg( $ICON_FOLLOW, $H_REPLYTHISARTICLE ), 'R' ) . "\n";
	}
    }
    else
    {
	if ( $SYS_REPLYQUOTE )
	{
	    $gHgStr .= $dlmtS . &tagComImg( $ICON_QUOTE_X, $H_REPLYTHISARTICLE ) . "\n";
	}
	else
	{
	    $gHgStr .= $dlmtS . &tagComImg( $ICON_FOLLOW_X, $H_REPLYTHISARTICLE ) . "\n";
	}
    }

    if ( $SYS_AUTH )
    {
	$gHgStr .= $dlmtL;

	if ( $delete )
	{
	    $gHgStr .= $dlmtS . &linkP( "b=$BOARD_ESC&c=f&s=on&id=$id",
		&tagComImg( $ICON_SUPERSEDE, $H_SUPERSEDE ), 'S' ) . "\n" .
		$dlmtS . &linkP( "b=$BOARD&c=dp&id=$id",
		&tagComImg( $ICON_DELETE, $H_DELETE ), 'D' ) . "\n";
	}
	else
	{
	    $gHgStr .= $dlmtS . &tagComImg( $ICON_SUPERSEDE_X, $H_SUPERSEDE ) .
	    	"\n" . $dlmtS . &tagComImg( $ICON_DELETE_X, $H_DELETE ) . "\n";
	}
    }

    if ( $SYS_COMICON == 1 )
    {
	$gHgStr .= $dlmtL;
	$gHgStr .= $dlmtS . &linkP( "b=$BOARD_ESC&c=h", &tagComImg( $ICON_HELP, '�إ��' ), 'H', '', '', 'message' ) . "\n";
    }
    $gHgStr .= qq(</p>\n);
}


###
## dumpArtHeader - �����إå��ʥ����ȥ�����ˤ�ɽ��
#
# - SYNOPSIS
#	&dumpArtHeader( $name, $eMail, $url, $host, $date, $origId );
#
# - ARGS
#	$name		�桼��̾
#	$eMail		�ᥤ�륢�ɥ쥹
#	$url		URL
#	$host		Remote Host̾
#	$date		���ա�UTC��
#	$origId		��ץ饤������ID
#
sub dumpArtHeader
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
	$gHgStr .= "<strong>$H_FROM</strong>: " . &tagA( $name, $url );
    }

    # �ᥤ��
    if ( $SYS_SHOWMAIL && $eMail )
    {
	$gHgStr .= ' ' . &tagA( "&lt;$eMail&gt;", "mailto:$eMail" );
    }
    $gHgStr .= $HTML_BR;

    # �ޥ���
    $gHgStr .= "<strong>$H_HOST</strong>: $host" . $HTML_BR if $SYS_SHOWHOST;

    # �����
    $gHgStr .= "<strong>$H_DATE</strong>: " . &getDateTimeFormatFromUtc( $date ) . $HTML_BR;

    # ��ץ饤���ؤΥ��
    if ( $origId )
    {
	( $dFid, $dAids, $dDate, $dTitle, $dIcon, $dHost, $dName ) = &getArtInfo( $origId );
	$gHgStr .= "<strong>$H_PARENT:</strong> ";
	&dumpArtSummary( $origId, $dAids, $dDate, $dTitle, $dIcon, $dName, 0 );
	$gHgStr .= $HTML_BR;
    }

    # �ڤ���
    $gHgStr .= "</p>\n";
}


###
## dumpButtonToTitleList - �����ȥ�����ܥ����ɽ��
#
# - SYNOPSIS
#	&dumpButtonToTitleList( $board, $id );
#
# - ARGS
#	$board		�Ǽ���ID
#	$id		���������å�����ID
#			���Υ�å�����ID��ޤॿ���ȥ�����˥����פ��롥
#
# - DESCRIPTION
#	�����ȥ�����إ����פ��뤿��Υܥ����ɽ������
#
sub dumpButtonToTitleList
{
    local( $board, $id ) = @_;
    local( $old ) = $id? &getTitleOldIndex( $id ) : 0;

    if  ( $SYS_COMMAND_BUTTON )
    {
	local( %tags ) = ( 'b', $board, 'c', 'v', 'num', $DEF_TITLE_NUM, 'old',
	    $old );
	&dumpForm( *tags, "$H_BACKTITLEREPLY(B)", '', '' );

	%tags = ( 'b', $board, 'c', 'r', 'num', $DEF_TITLE_NUM, 'old', $old );
	&dumpForm( *tags, $H_BACKTITLEDATE, '', '' );
    }
    else
    {
	local( $boardEsc ) = &uriEscape( $board );
	$gHgStr .= "<p>" . &linkP( "b=$boardEsc&c=v&num=$DEF_TITLE_NUM&old=$old", $H_BACKTITLEREPLY . &tagAccessKey( 'B' ), 'B' ) . "</p>\n";
	$gHgStr .= "<p>" . &linkP( "b=$boardEsc&c=r&num=$DEF_TITLE_NUM&old=$old", $H_BACKTITLEDATE ) .
	    "</p>\n";
    }
}


###
## dumpButtonToArticle - ��å������إ����פ���ܥ����ɽ��
#
# - SYNOPSIS
#	&dumpButtonToArticle( $board, $id, $msg );
#
# - ARGS
#	$board	�Ǽ���ID
#	$id	��å�����ID
#	$msg	���ʸ����
#
# - DESCRIPTION
#	��å������إ����פ��뤿��Υܥ����ɽ������
#
sub dumpButtonToArticle
{
    local( $board, $id, $msg ) = @_;

    if  ( $SYS_COMMAND_BUTTON )
    {
	local( %tags ) = ( 'b', $board, 'c', 'e', 'id', $id );
	&dumpForm( *tags, "$msg(N)", '', '' );
    }
    else
    {
	local( $boardEsc ) = &uriEscape( $board );
	$gHgStr .= "<p>" . &linkP( "b=$boardEsc&c=e&id=$id", $msg .
	    &tagAccessKey( 'N' ), 'N' ) . "</p>\n";
    }
}


###
## dumpForm - �ե����ॿ���Υե����ޥå�
#
# - SYNOPSIS
#	&dumpForm( *hiddenTags, $submit, $reset, *contents );
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
sub dumpForm
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
    $gHgStr .= "$contents\n" . &tagInputSubmit( 'submit', $submit, $accessKey );
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
	$gHgStr .= ' ' . &tagInputSubmit( 'reset', $reset, $accessKey ) . "\n";
    }
    $gHgStr .= "</p>\n</form>\n";
}


###
## dumpArtSummary - �����ȥ�ꥹ�ȤΥե����ޥå�
#
# - SYNOPSIS
#	&dumpArtSummary( $id, $aids, $date, $subject, $icon, $name, $flag);
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
sub dumpArtSummary
{
    local( $id, $aids, $date, $subject, $icon, $name, $flag ) = @_;

    $subject = $subject || $id;
    $name = $name || $MAINT_NAME;

    $gHgStr .= qq(<span class="kbTitle">);	# �����

    if ( $flag&1 && ( &getArtParents( $id ) ne '' ))
    {
	local( $fId );
	$fId = &getArtParentTop( $id );
	$gHgStr .= ' ' . &linkP( "b=$BOARD_ESC&c=t&id=$fId", $H_THREAD_ALL, '', $H_THREAD_ALL_L ) . ' ';
    }

    $gHgStr .= &tagArtImg( $icon ) . " <small>$id.</small> " .
	(( $flag&2 )? &tagA( $subject, "$cgi'REQUEST_URI#a$id" ) :
	&linkP( "b=$BOARD_ESC&c=e&id=$id", $subject ));

    if ( $aids )
    {
	$gHgStr .= ' ' . &linkP( "b=$BOARD_ESC&c=t&id=$id", $H_THREAD, '', $H_THREAD_L );
    }

    $gHgStr .= " [$name] ";
    $gHgStr .= &getDateTimeFormatFromUtc( $date ) if $date;

    $gHgStr .= ' ' . &tagArtImg( $H_NEWARTICLE ) if &getArtNewP( $id );
    $gHgStr .= "</span>\n";
}


###
## dumpArtSummaryItem - �����ȥ�ꥹ�ȤΥե����ޥåȡ�<li>�Ĥ���
#
# - SYNOPSIS
#	&dumpArtSummaryItem(Ʊ��);
#
# - ARGS
#	Ʊ��
#
# - DESCRIPTION
#	���뵭���򥿥��ȥ�ꥹ��ɽ���Ѥ˥ե����ޥåȤ��롥<li>�Ĥ�
#
sub dumpArtSummaryItem
{
    $gHgStr .= '<li>';
    &dumpArtSummary;
}


######################################################################
# ���å�����ץ���ơ������


#### ɽ����Ϣ���å�


###
## htmlEncode/htmlDecode - �ü�ʸ����HTML��Encode��Decode
#
# - SYNOPSIS
#	&htmlEncode($Str);
#	&htmlDecode($Str);
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
sub htmlEncode
{
    local( $_ ) = @_;
    s/\&/&amp;/go;
    s/\"/&quot;/go;
    s/\>/&gt;/go;
    s/\</&lt;/go;
    $_;
}

sub htmlDecode
{
    local( $_ ) = @_;
    s/&quot;/\"/gio;
    s/&gt;/\>/gio;
    s/&lt;/\</gio;
    s/&amp;/\&/gio;
    $_;
}


###
## uriEscape - URI��escape
#
# - SYNOPSIS
#	&uriEscape( $str );
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
sub uriEscape
{
    local( $_ ) = @_;
    s/([^A-Za-z0-9\\\-_\.!~*'() ])/sprintf( "%%%02X", ord( $1 ))/eg;
    s/ /+/go;
    $_;
}


###
## tagEncode - �ü�ʸ����TAG��������Encode
#
# - SYNOPSIS
#	&tagEncode( *str );
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
sub tagEncode
{
    local( *str ) = @_;
#    $str =~ s/[\&\"]//go;
    $str =~ s/<[^>]*>//go;
}


###
## articleEncode - ������Encode
#
# - SYNOPSIS
#	&articleEncode( *article );
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
sub articleEncode
{
    local( *article ) = @_;

    local( $retArticle ) = $article;

    local( $url, $urlMatch, @cache );
    local( $tagStr, $quoteStr );
    while ( $article =~ m/\[url:([^\]]+)\]/gio )
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
		local( $boardEsc ) = &uriEscape( $1 );
		$tagStr = &linkP( "b=$boardEsc&c=e&id=$2", $quoteStr );
	    }
	    else
	    {
		$tagStr = &linkP( "b=$BOARD_ESC&c=e&id=$artStr", $quoteStr );
	    }
	}
	elsif ( &isUrl( &htmlDecode( $urlMatch )))
	{
	    $tagStr = &tagA( $quoteStr, &htmlDecode( $url ), '', '', '', $SYS_LINK_TARGET );
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
## plainArticleToPreFormatted - Plain������pre formatted text���Ѵ�
#
# - SYNOPSIS
#	&plainArticleToPreFormatted(*Article);
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
sub plainArticleToPreFormatted
{
    local( *Article ) = @_;
    $Article =~ s/\n*$//o;
    $Article = &htmlEncode( $Article );	# no tags are allowed.
    $Article = "<pre>\n" . $Article . "</pre>";
}


###
## plainArticleToHtml - Plain������HTML���Ѵ�
#
# - SYNOPSIS
#	&plainArticleToHtml(*Article);
#
# - ARGS
#	*Article	�Ѵ����뵭����ʸ
#
# - DESCRIPTION
#	����������̵��̣�ʲ��Ԥ��������
#	�������<p>�ǰϤࡥ
#	*Article���˲����롥
#
sub plainArticleToHtml
{
    local( *Article ) = @_;
    $Article =~ s/^\n*//o;
    $Article =~ s/\n*$//o;
    $Article =~ s/\n/$HTML_BR/go;
    $Article =~ s/$HTML_BR($HTML_BR)+/<\/p>\n\n<p>/go;
    $Article = "<p>$Article</p>";
}


###
## quoteOriginalArticle - ���Ѥ���(�����䤢��)
#
# - SYNOPSIS
#	&quoteOriginalArticle($Id);
#
# - ARGS
#	$Id		����ID
#
# - DESCRIPTION
#	��������Ѥ���ɽ������
#
sub quoteOriginalArticle
{
    local( $Id, *msg ) = @_;

    # ����������μ���
    local( $fid, $aids, $date, $subject, $icon, $remoteHost, $name, $eMail, $url ) = &getArtInfo( $Id );

    # �������Τ���˸���������
    local( $pName ) = '';
    if ( $fid )
    {
	local( $pId );
	( $pId = $fid ) =~ s/,.*$//o;
	( $pName ) = &getArtAuthor( $pId );
    }

    # ����
    local( @ArticleBody );
    &getArtBody( $Id, $BOARD, *ArticleBody );

    if ( $SYS_QUOTEMSG )
    {
	local( $premsg ) = $SYS_QUOTEMSG;
	$premsg =~ s/__LINK__/[url:kb:$Id]/i;
	$premsg =~ s/__TITLE__/$subject/;
	$premsg =~ s/__DATE__/&getDateTimeFormatFromUtc( $date )/e;
	$premsg =~ s/__NAME__/$name/;
	$msg .= $premsg;
    }
    local( $QMark, $line );
    foreach $line ( @ArticleBody )
    {
	&tagEncode( *line );

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
## quoteOriginalArticleWithoutQMark - ���Ѥ���(������ʤ�)
#
# - SYNOPSIS
#	&quoteOriginalArticleWithoutQMark($Id);
#
# - ARGS
#	$Id		����ID
#
# - DESCRIPTION
#	��������Ѥ���ɽ������
#
sub quoteOriginalArticleWithoutQMark
{
    local( $Id, *msg ) = @_;

    local( @ArticleBody, $line );
    &getArtBody( $Id, $BOARD, *ArticleBody );
    foreach $line ( @ArticleBody )
    {
	if ( $SYS_TAGINSUPERSEDE )
	{
	    $line = &htmlEncode( $line );
	}
	else
	{
	    &tagEncode( *line );
	}
	$msg .= $line;
    }
}


###
## pageLink - �ڡ����إå�/�եå���ɽ��
#
# - SYNOPSIS
#	&pageLink( $com, $num, $old, $rev, $fold );
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
sub pageLink
{
    local( $com, $num, $old, $rev, $fold ) = @_;

    local( $nextOld ) = ( $old > $num )? ( $old - $num ) : 0;
    local( $backOld ) = ( $old + $num );

    local( $str );
    $str = '<p class="kbPageLink">';

    if ( $old )
    {
	$str .= &linkP( "b=$BOARD_ESC&c=$com&num=$num&old=0&fold=$fold&rev=$rev", '&lt;&lt;' . $H_TOP . &tagAccessKey( 'T' ), 'T', $H_TOP );
	$str .= ' | ' . &linkP( "b=$BOARD_ESC&c=$com&num=$num&old=$nextOld&fold=$fold&rev=$rev", '&lt;' . $H_UP . &tagAccessKey( 'N' ), 'N', $H_UP );
    }
    else
    {
	$str .= '&lt;&lt;' . $H_TOP . &tagAccessKey( 'T' ) . ' | ' . '&lt;' . $H_UP . &tagAccessKey( 'N' );
    }

    if ( $SYS_REVERSE )
    {
	$str .= ' | ' .
	    &linkP( "b=$BOARD_ESC&c=$com&num=$num&old=$old&fold=$fold&rev=" . ( 1-$rev ), $H_REVERSE[ 1-$rev ] . &tagAccessKey( 'R' ), 'R', $H_REVERSE_L );
    }

    if ( $SYS_EXPAND && ( $fold ne '' ))
    {
	$str .= ' | ' . &linkP( "b=$BOARD_ESC&c=$com&num=$num&old=$old&rev=$rev&fold=" . ( 1-$fold ), $H_EXPAND[ 1-$fold ] . &tagAccessKey( 'E' ), 'E', $H_EXPAND_L );
    }

    $str .= ' | ';

    local( $nofMsg ) = &getNofArt();
    if ( $num && ( $nofMsg - $backOld >= 0 ))
    {
	$str .= &linkP( "b=$BOARD_ESC&c=$com&num=$num&old=$backOld&fold=$fold&rev=$rev", $H_DOWN . &tagAccessKey( 'P' ) . '&gt;', 'P', $H_DOWN );
	$str .= ' | ' . &linkP( "b=$BOARD_ESC&c=$com&num=$num&old=" . ( $nofMsg - $num + 1 ) . "&fold=$fold&rev=$rev", $H_BOTTOM . &tagAccessKey( 'B' ) . '&gt;&gt;' , 'B', $H_BOTTOM );
    }
    else
    {
	$str .= $H_DOWN . &tagAccessKey( 'P' ) . '&gt;' . ' | ' . $H_BOTTOM . &tagAccessKey( 'B' ) . '&gt;&gt;';
    }

    $str .= "</p>\n";

    $str;
}


###
## tagImg - ���᡼�������Υե����ޥå�
#
# - SYNOPSIS
#	&tagImg( $src, $alt, $width, $height, $class );
#
# - ARGS
#	$src		���������᡼����URL
#	$alt		alt�����Ѥ�ʸ����
#	$width		width
#	$height		height
#	$class		class��ʸ����
#
# - DESCRIPTION
#	���᡼����ɽ���ѥ����˥ե����ޥåȤ��롥
#
sub tagImg
{
    local( $src, $alt, $width, $height, $class ) = @_;
    qq(<img src="$src" alt="$alt" width="$width" height="$height" class="$class" />);
}


###
## tagComImg - ���ޥ�ɥ��������ѥ��᡼�������Υե����ޥå�
#
# - SYNOPSIS
#	&tagComImg( $src, $alt );
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
sub tagComImg
{
    local( $src, $alt ) = @_;
    if ( $SYS_COMICON == 1 )
    {
	&tagImg( $src, $alt, $COMICON_WIDTH, $COMICON_HEIGHT, 'kbComIcon' );
    }
    elsif ( $SYS_COMICON == 2 )
    {
	&tagImg( $src, $alt, $COMICON_WIDTH, $COMICON_HEIGHT, 'kbComIcon' ) . $alt;
    }
    else
    {
	$alt;
    }
}


###
## tagArtImg - �������������ѥ��᡼�������Υե����ޥå�
#
# - SYNOPSIS
#	&tagArtImg( $icon );
#
# - ARGS
#	$icon		�������󥿥���
#
# - DESCRIPTION
#	���᡼����ɽ���ѥ����˥ե����ޥåȤ��롥
#
sub tagArtImg
{
    local( $icon ) = @_;

    if ( !$icon || $icon eq $H_NOICON )
    {
	return "";
    }
    elsif ( $SYS_ICON )
    {
	local( $src ) = &getIconUrlFromTitle( $icon );
	&tagImg( $src, "[$icon]", $MSGICON_WIDTH, $MSGICON_HEIGHT, 'kbMsgIcon' );
    }
    else
    {
	return "[$icon]";
    }
}


###
## tagA - ��󥯥����Υե����ޥå�
#
# - SYNOPSIS
#	&tagA();
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
sub tagA
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
## tagAccessKey - ��������������٥�Υե����ޥå�
#
# - SYNOPSIS
#	&tagAccessKey( $key );
#
# - ARGS
#	$key		����1ʸ��
#
sub tagAccessKey
{
    qq{(<span class="kbAccessKey">$_[0]</span>)};
}


###
## tagLabel - ��٥륿���Υե����ޥå�
#
# - SYNOPSIS
#	&tagLabel( $markUp, $label, $accessKey );
#
# - ARGS
#	$markUp		�ޡ������å�ʸ����
#	$label		��٥��оݥ���ȥ���
#	$accessKey	������������
#
sub tagLabel
{
    local( $markUp, $label, $accessKey ) = @_;
    if ( $accessKey )
    {
	qq[<label for="$label" accesskey="$accessKey">$markUp] . &tagAccessKey( $accessKey ) . "</label>";
    }
    else
    {
	qq[<label for="$label">$markUp</label>];
    }
}


###
## tagInputSubmit - submit/reset�ܥ��󥿥��Υե����ޥå�
#
# - SYNOPSIS
#	&tagInputSubmit( $type, $value, $key );
#
# - ARGS
#	$type	submit/reset
#	$value	��٥�˻Ȥ���
#	$key	accesskey�˻Ȥ���
#
sub tagInputSubmit
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
## tagInputText - ���ϥ����Υե����ޥå�
#
# - SYNOPSIS
#	&tagInputText( $type, $id, $value, $size );
#
# - ARGS
#	$type	text/password
#	$id	id��name�˻Ȥ���
#	$value	�ǥե�����ͤ˻Ȥ���
#	$size	size�˻Ȥ���
#
sub tagInputText
{
    local( $type, $id, $value, $size ) = @_;
    $gTabIndex++;
    qq(<input type="$type" id="$id" name="$id" value="$value" size="$size" tabindex="$gTabIndex" />);
}


###
## tagInputCheck - �����å��ܥå��������Υե����ޥå�
#
# - SYNOPSIS
#	&tagInputCheck( $id, $checked );
#
# - ARGS
#	$id		id��name�˻Ȥ���
#	$checked	true�ʤ�checked���դ�
#
# - DESCRIPTION
#	value��"on"���ꡥ
#
sub tagInputCheck
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
## tagInputRadio - �饸���ܥ��󥿥��Υե����ޥå�
#
# - SYNOPSIS
#	&tagInputRadio( $id, $name, $value, $checked );
#
# - ARGS
#	$id		id�˻Ȥ���
#	$name		name�˻Ȥ���
#	$value		�ǥե�����ͤ˻Ȥ���
#	$checked	true�ʤ�checked���դ�
#
sub tagInputRadio
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
## tagTextarea - textarea�����Υե����ޥå�
#
# - SYNOPSIS
#	&tagTextarea( $id, $value, $rows, $cols );
#
# - ARGS
#	$id	id��name�˻Ȥ���
#	$value	�ǥե�����ͤ˻Ȥ���
#	$rows	rows�˻Ȥ���
#	$cols	cols�˻Ȥ���
#
sub tagTextarea
{
    local( $id, $value, $rows, $cols ) = @_;
    $gTabIndex++;
    qq(<textarea id="$id" name="$id" rows="$rows" cols="$cols" tabindex="$gTabIndex">$value</textarea>);
}


###
## tagSelect - select�����Υե����ޥå�
#
# - SYNOPSIS
#	&tagSelect( $id, $contents, $size, $multiple );
#
# - ARGS
#	$id		id��name�˻Ȥ���
#	$contents	������ѥ���ƥ��
#	$size		size�˻Ȥ��롥��ά����1
#	$multiple	true�ʤ�ʣ�������
#
sub tagSelect
{
    local( $id, $contents, $size, $multiple ) = @_;
    $gTabIndex++;
    $size = 1 unless $size;
    if ( $multiple )
    {
	qq(<select id="$id" name="$id" size="$size" multiple="multiple" tabindex="$gTabIndex">$contents</select>);
    }
    else
    {
	qq(<select id="$id" name="$id" size="$size" tabindex="$gTabIndex">$contents</select>);
    }
}


###
## tagFieldset - fieldset�����Υե����ޥå�
#
# - SYNOPSIS
#	&tagFieldset( $title, $contents );
#
# - ARGS
#	$title		legend�˻Ȥ���
#	$contents	fieldset�Υ���ƥ��
#
sub tagFieldset
{
    local( $title, $contents ) = @_;
    qq(<fieldset>\n<legend>$title</legend>\n$contents</fieldset>\n);
}


###
## linkP - ���ץ���������󥯤�����
#
# - SYNOPSIS
#	&linkP( $href, $markUp );
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
sub linkP
{
    local( $comm, $markUp, $key, $title, $name, $fragment ) = @_;
    $comm .= "&kinoA=3&kinoU=$UNAME_ESC&kinoP=$PASSWD" if ( $SYS_AUTH == 3 );
    $comm =~ s/&/&amp;/go;
    $comm .= "#$fragment" if ( $fragment ne '' );
    &tagA( $markUp, "$PROGRAM?$comm", $key, $title, $name );
}


#### �Ӥ���Ϣ���å�


###
## makeNewArticle, MakeNewArticleEx - ��������Ƥ��줿����������
#
# - SYNOPSIS
#	&MakeNewArticleEx( $Board, $Id, $artKey, $postDate, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail, $MailRelay );
#	&makeNewArticle( $Board, $Id, $artKey, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail, $MailRelay );
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
#	�����R7�ʸ�ˤ϶���&makeNewArticleEx������Ȥ��褦�ˡ�
#
sub MakeNewArticle
{
    local( $Board, $Id, $artKey, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail, $MailRelay ) = @_;
    &makeNewArticleEx( $Board, $Id, $artKey, $^T, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail, $MailRelay );
}

sub makeNewArticleEx
{
    local( $Board, $Id, $artKey, $postDate, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail, $MailRelay ) = @_;

    &checkArticle( $Board, *postDate, *Name, *Email, *Url, *Subject, *Icon, *Article );

    # DB�ե��������Ƥ��줿�������ɲ�
    local( $ArticleId ) = &insertArt( $Board, $Id, $artKey, $postDate, $Subject, $Icon, ( $SYS_LOGHOST? $REMOTE_INFO : '' ), $Name, $Email, $Url, $Fmail, $MailRelay, $TextType, $Article );

    $ArticleId;
}


###
## searchArticleIcon - �����θ���(��������)
#
# - SYNOPSIS
#	&searchArticleIcon( $id, $type, const *iconHash );
#
# - ARGS
#	$id		��������򸡺����뵭����ID
#	$type		����������
#			  1 ... �Ǥ���
#			  2 ... ľ�ܤ�̼�Ǥ���
#			  3 ... ľ�ܤοƤǤ���
#			  11 ... ����å���˴ޤ�
#			  12 ... ����åɤ���Ƭ�ˤ���
#			  13 ... ����åɤ���ü�ˤ���
#	%iconHash	�������������ѥϥå��塥
#			  $iconHash{ '��������' }�����Υ������󤬸�������롥
#
# - DESCRIPTION
#	���ꤵ�줿�����Υ�������򸡺����롥
#
# - RETURN
#	1 if match, 0 if not.
#
%gSearchIconResult = ();
sub searchArticleIcon
{
    local( $id, $type, *iconHash ) = @_;
    local( $result ) = 0;

    # ������̤�����å��夷�Ƥ��뤫�ɤ���������å�������Ф������ͥ�补
    if ( defined( $gSearchIconResult{ $id } ))
    {
	return $gSearchIconResult{ $id };
    }

    # 0�ϸ����ߴ����Τ��ᡥ'on'���Ϥ���뤫�⤷��ʤ���
    if (( $type == 1 ) || ( $type == 0 ))
    {
	$result = 1 if ( $iconHash{ &getArtIcon( $id ) } );
	$gSearchIconResult{ $id } = $result;
    }
    elsif ( $type == 2 )
    {
	local( @daughters ) = split( /,/, &getArtDaughters( $id ));
	if ( !@daughters )
	{
	    $result = 0;
	}
	else
	{
	    foreach ( @daughters )
	    {
		$result = 1, last if ( $iconHash{ &getArtIcon( $_ ) } );
	    }
	}
	$gSearchIconResult{ $id } = $result;
    }
    elsif ( $type == 3 )
    {
	local( $parent ) = &getArtParent( $id );
	if ( $parent eq '' )
	{
	    $result = $gSearchIconResult{ $id } = 0;
	}
	elsif ( $iconHash{ &getArtIcon( $parent ) } )
	{
	    local( @daughters ) = split( /,/, &getArtDaughters( $parent ));
	    foreach ( @daughters )
	    {
		$result = $gSearchIconResult{ $_ } = 1;
	    }
	}
	else
	{
	    local( @daughters ) = split( /,/, &getArtDaughters( $parent ));
	    foreach ( @daughters )
	    {
		$result = $gSearchIconResult{ $_ } = 0;
	    }
	}
    }
    elsif ( $type == 11 )
    {
	local( $topId ) = &getArtParentTop( $id );

	# �ȥåפ��鸡�����Ƥ�����
	local( @daughters ) = ( $topId );
	local( $dId );
	while ( $dId = shift( @daughters ))
	{
	    $result = 1, last if ( $iconHash{ &getArtIcon( $dId ) } );
	    push( @daughters, split( /,/, &getArtDaughters( $dId )));
	}
    }
    elsif ( $type == 12 )
    {
	local( $topId ) = &getArtParentTop( $id );
	$result = 1 if ( $iconHash{ &getArtIcon( $topId ) } );
    }
    elsif ( $type == 13 )
    {
	local( @daughters ) = ( $id );
	local( $dId, $dDaughters );
	while ( $dId = shift( @daughters ))
	{
	    $dDaughters = &getArtDaughters( $dId );
	    if ( $dDaughters eq '' )
	    {
		$result = 1, last if ( $iconHash{ &getArtIcon( $dId ) } );
	    }
	    else
	    {
		push( @daughters, split( /,/, $dDaughters ));
	    }
	}
    }

    # ����åɸ����ξ��
    if ( int( $type / 10 ) == 1 )
    {
	# ������̤򥭥�å����ȿ�Ǥ�����: �ȥåפ��餿�ɤ�����Ƥ�̼��
	local( $topId ) = &getArtParentTop( $id );

	# �ȥåפ��鸡�����Ƥ�����
	local( @daughters ) = ( $topId );
	local( $dId );
	while ( $dId = shift( @daughters ))
	{
	    $gSearchIconResult{ $dId } = $result;
	    push( @daughters, split( /,/, &getArtDaughters( $dId )));
	}
    }

    return $result;
}


###
## searchArticleKeyword - �����θ���(��ʸ)
#
# - SYNOPSIS
#	&searchArticleKeyword($Id, $Board, @KeyList);
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
sub searchArticleKeyword
{
    local( $Id, $Board, @KeyList ) = @_;

    local( @NewKeyList, $Line, $Return, $Code, $ConvFlag, @ArticleBody );

    $ConvFlag = ( $Id !~ /^\d+$/ );

    &getArtBody( $Id, $Board, *ArticleBody );
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
## checkSearchTime - �������դΥ����å�
#
# - SYNOPSIS
#	&checkSearchTime( $target, $from, $to );
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
sub checkSearchTime
{
    local( $target, $from, $to ) = @_;

    if ( $from >= 0 )
    {
	return 0 if ( $target < $from );
    }
    elsif ( $to >= 0 )
    {
	return 0 if ( $target > $to );
    }
    else
    {
	return 0;
    }

    1;
}


###
## deleteArticle - �����κ��
#
# - SYNOPSIS
#	&deleteArticle($Id, $ThreadFlag);
#
# - ARGS
#	$Id		�������ID
#	$Board		�Ǽ���ID
#	$ThreadFlag	��ץ饤��ä����ݤ�
#
# - DESCRIPTION
#	������٤�����ID����������塤DB�򹹿����롥
#
sub deleteArticle
{
    local( $Id, $Board, $ThreadFlag ) = @_;

    local( $Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $dId, @Target, $TargetId, $parents );

    # ��������μ���
    ( $Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url ) = &getArtInfo( $Id );

    # �ǡ����ν񤭴���(ɬ�פʤ�̼��)
    @Target = ( $Id );
    foreach $TargetId ( @Target )
    {
	foreach ( 0 .. &getNofArt() )
	{
	    # ID����Ф�
	    $dId = &getArtId( $_ );
	    # �ե��������ꥹ�Ȥ��椫�顤������뵭����ID�������
	    &setArtDaughters( $dId, join( ',', grep(( !/^$TargetId$/o ),
		split( /,/, &getArtDaughters( $dId )))));
	    # ������������������ID�������
	    $parents = &getArtParents( $dId );
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
	    &setArtParents( $dId, $parents );
	    # ̼���оݤȤ���
	    push( @Target, split( /,/, &getArtDaughters( $dId ))) if ( $ThreadFlag && ( $dId eq $TargetId ));
	}
    }

    # DB�򹹿����롥
    &deleteArt( $Board, *Target );
}


###
## supersedeArticle - ��������������
#
# - SYNOPSIS
#	&supersedeArticle;
#
# - DESCRIPTION
#	�������������롥
#
sub supersedeArticle
{
    local( $Board, $Id, $postDate, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail ) = @_;

    # ���Ϥ��줿��������Υ����å����������
    &checkArticle( $Board, $postDate, *Name, *Email, *Url, *Subject, *Icon, *Article );

    # DB�ե����������
    &updateArt( $Board, $Id, $postDate, $Subject, $Icon, ( $SYS_LOGHOST? $REMOTE_INFO : '' ), $Name, $Email, $Url, $Fmail, $TextType, $Article );

    $Id;
}


###
## reLinkExec - �����Τ��������»�
#
# - SYNOPSIS
#	&reLinkExec($FromId, $ToId, $Board);
#
# - ARGS
#	$FromId		��������������ID
#	$ToId		���������赭��ID
#	$Board		�Ǽ���ID
#
# - DESCRIPTION
#	�������ץ饤-�������ط��򤫤������롥
#
sub reLinkExec
{
    local( $FromId, $ToId, $Board ) = @_;

    local( $dId, @Daughters, $DaughterId );

    # �۴ĵ����ζػ�
    &fatal( 50, '' ) if ( grep( /^$FromId$/, split( /,/, &getArtParents( $ToId ))));

    # �ǡ����񤭴���
    foreach ( 0 .. &getNofArt() )
    {
	# ID����Ф�
	$dId = &getArtId( $_ );
	# �ե��������ꥹ�Ȥ��椫�顤��ư���뵭����ID�������
	&setArtDaughters( $dId, join( ',', grep(( !/^$FromId$/o ), split( /,/, &getArtDaughters( $dId )))));
    }

    # ���̼�����ν񤭴�����ɬ�פˤʤ롥
    @Daughters = split( /,/, &getArtDaughters( $FromId ));

    # ���������Υ�ץ饤����ѹ�����
    if ( $ToId eq '' )
    {
	&setArtParents( $FromId, '' );
    }
    elsif ( &getArtParents( $ToId ) eq '' )
    {
	&setArtParents( $FromId, "$ToId" );
    }
    else
    {
	&setArtParents( $FromId, "$ToId," . &getArtParents( $ToId ));
    }

    # ����ѹ������ֳ��������Υ�ץ饤��פ�̼��ȿ�Ǥ�����
    while ( $DaughterId = shift( @Daughters ))
    {
	# ¹̼��ġ�
	push( @Daughters, split( /,/, &getArtDaughters( $DaughterId )));

	# �񤭴���
	if (( &getArtParents( $DaughterId ) eq $FromId ) || ( &getArtParents( $DaughterId ) =~ /^$FromId,/ ))
	{
	    &setArtParents( $DaughterId, ( &getArtParents( $FromId ) ne '' )? "$FromId," . &getArtParents( $FromId ) : "$FromId" );
	}
	elsif (( &getArtParents( $DaughterId ) =~ /^(.*),$FromId$/ ) || ( &getArtParents( $DaughterId ) =~ /^(.*),$FromId,/ ))
	{
	    &setArtParents( $DaughterId, ( &getArtParents( $FromId ) ne '' )? "$1,$FromId," . &getArtParents( $FromId ) : "$1,$FromId" );
	}
    }

    # ��ץ饤��ˤʤä������Υե������������ɲä���
    &setArtDaughters( $ToId, ( &getArtDaughters( $ToId ) ne '' ) ? &getArtDaughters( $ToId ) . ",$FromId" : "$FromId" );

    # ����DB�򹹿�����
    &flushArt( $Board );
}


###
## reOrderExec - �����ΰ�ư�»�
#
# - SYNOPSIS
#	&reOrderExec($FromId, $ToId, $Board);
#
# - ARGS
#	$FromId		��ư������ID
#	$ToId		��ư�赭��ID
#	$Board		�Ǽ���ID
#
# - DESCRIPTION
#	���ꤵ�줿�����򡤻��ꤵ�줿�����μ��˰�ư���롥
#
sub reOrderExec
{
    local( $FromId, $ToId, $Board ) = @_;

    local( @Move );

    # ��ư���뵭�������򽸤��
    @Move = ( $FromId, &getFollowIdSet( $FromId ));

    # ��ư������
    &reOrderArt( $Board, $ToId, *Move );
}


#### �ᥤ���Ϣ���å�


###
## arriveMail - ���������夷�����Ȥ�ᥤ��
#
# - SYNOPSIS
#	&arriveMail( $Name, $Email, $Date, $Subject, $Icon, $Id, @To );
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
sub arriveMail
{
    local( $Name, $Email, $Date, $Subject, $Icon, $Id, @To ) = @_;

    local( $StrSubject, $MailSubject, $StrFrom, $Message );
    $StrSubject = ( !$SYS_ICON || ( $Icon eq $H_NOICON ))? $Subject : "($Icon) $Subject";
    $StrSubject =~ s/<[^>]*>//go;	# �������פ�ʤ�
    $StrSubject = &htmlDecode( $StrSubject );
    $MailSubject = &getMailSubjectPrefix( $BOARDNAME, $Id ) . $StrSubject;
    $StrFrom = $Email? "$Name <$Email>" : "$Name";

    $Message = <<__EOF__;
$SYSTEM_NAME����Τ��Τ餻�Ǥ���
$H_BOARD��$BOARDNAME�פ��Ф��ƽ񤭹��ߤ�����ޤ�����

����$H_MESG:
  �� $SCRIPT_URL?b=$BOARD&c=e&id=$Id

__EOF__

    $Message .= &getArticlePlainText( $Id, $Name, $Email, $Subject, $Icon, $Date );

    # �ᥤ������
    &sendArticleMail( $Name, $Email, $MailSubject, $Message, $Id, @To );
}


###
## followMail - ȿ�������ä����Ȥ�ᥤ��
#
# - SYNOPSIS
#	&followMail( $Name, $Email, $Date, $Subject, $Icon, $Id, $Fname, $Femail, $Fsubject, $Ficon, $Fid, @To );
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
sub followMail
{
    local( $Name, $Email, $Date, $Subject, $Icon, $Id, $Fname, $Femail, $Fdate, $Fsubject, $Ficon, $Fid, @To ) = @_;
    
    local( $StrSubject, $FstrSubject, $MailSubject, $StrFrom, $Message );

    $StrSubject = ( !$SYS_ICON || ( $Icon eq $H_NOICON ))? "$Subject" : "($Icon) $Subject";
    $StrSubject =~ s/<[^>]*>//go;	# �������פ�ʤ�
    $StrSubject = &htmlDecode( $StrSubject );
    $FstrSubject = ( $Ficon eq $H_NOICON )? $Fsubject : "($Ficon) $Fsubject";
    $FstrSubject =~ s/<[^>]*>//go;	# �������פ�ʤ�
    $FstrSubject = &htmlDecode( $FstrSubject );
    $MailSubject = &getMailSubjectPrefix( $BOARDNAME, $Fid ) . $FstrSubject;
    $StrFrom = $Email? "$Name <$Email>" : "$Name";

    local( $topId ) = &getArtParentTop( $Id );

    $Message = <<__EOF__;
$SYSTEM_NAME����Τ��Τ餻�Ǥ���

$H_BOARD��$BOARDNAME�פ�
��$StrFrom�פ��󤬽񤤤�
��$StrSubject�פ�
$H_REPLY������ޤ�����

����$H_MESG:
  �� $SCRIPT_URL?b=$BOARD&c=e&id=$Fid
����åɤ���Ƭ����ޤȤ��ɤ�:
  �� $SCRIPT_URL?b=$BOARD&c=t&id=$topId

__EOF__

    $Message .= &getArticlePlainText( $Fid, $Fname, $Femail, $Fsubject, $Ficon, $Fdate );

    # �ᥤ������
    &sendArticleMail( $Fname, $Femail, $MailSubject, $Message, $Fid, @To );
}


###
## sendArticleMail - �ᥤ������
#
# - SYNOPSIS
#	&sendArticleMail( $FromName, $FromAddr, $Subject, $Message, $Id, @To );
#
# - ARGS
#	$FromName	�ᥤ��������̾
#	$FromAddr	�ᥤ�������ԥᥤ�륢�ɥ쥹
#	$Subject	�ᥤ���Subjectʸ����
#	$Message	��ʸ
#	$Id		���Ѥ���ʤ鵭��ID; ���ʤ���ѥʥ�
#	@To		����E-Mail addr.�Υꥹ��
#
# - DESCRIPTION
#	�ᥤ����������롥
#
sub sendArticleMail
{
    local( $FromName, $FromAddr, $Subject, $Message, $Id, @To ) = @_;

    local( $ExtHeader, @ArticleBody );

    $ExtHeader = "X-MLServer: $PROGNAME\n";
    $ExtHeader .= "X-Kb-System: $SYSTEM_NAME\n";
    if (( ! $SYS_MAILHEADBRACKET ) && $BOARDNAME && ($Id ne '' ))
    {
	$ExtHeader .= "X-Kb-Board: $BOARDNAME\nX-Kb-Articleid: $Id\n";
    }

    local( $stat, $errstr ) = &sendMail( $FromName, $FromAddr, $Subject, $ExtHeader, $Message, @To );
    &fatal( 9, "$BOARDNAME/$Id/$errstr" ) unless $stat;
}


###
## sendMail - �ᥤ������
#
# - SYNOPSIS
#	&sendMail( $FromName, $FromAddr, $Subject, $ExtHeader, $Message, @To );
#
# - ARGS
#	$FromName	�ᥤ��������̾
#	$FromAddr	�ᥤ�������ԥᥤ�륢�ɥ쥹
#	$Subject	�ᥤ���Subjectʸ����
#	$ExtHeader	�ɲåإå�
#	$Message	��ʸ
#	@To		����E-Mail addr.�Υꥹ��
#
# - DESCRIPTION
#	�ᥤ����������롥
#
# - RETURN
#	( $status, $errstr )
#		$status		0 if succeeded, errCode if failed.
#		$errstr		errstr if failed.
#
sub sendMail
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
## getArticlePlainText - ��å�������plain text�Ǽ���
#
# - SYNOPSIS
#	&getArticlePlainText( $id, $name, $mail, $subject, $icon, $date );
#
# - ARGS
#	$id		��å�����ID
#	$name		��Ƽ�̾
#	$mail		��Ƽԥᥤ�륢�ɥ쥹
#	$subject	�����ȥ�
#	$icon		��������
#	$date		����(UTC)
#
# - DESCRIPTION
#	�ᥤ�������Ѥˡ���å�������plain text�Ǽ������롥
#
# - RETURN
#	ʸ����
#
sub getArticlePlainText
{
    local( $id, $name, $mail, $subject, $icon, $date ) = @_;

    local( $strSubject ) = ( !$SYS_ICON || ( $icon eq $H_NOICON ))? $subject :
	"($icon) $subject";
    $strSubject =~ s/<[^>]*>//go;	# �������פ�ʤ�
    $strSubject = &htmlDecode( $strSubject );
    local( $strFrom ) = $mail? "$name <$mail>" : $name;
    local( $strDate ) = &getDateTimeFormatFromUtc( $date );

    local( @body );
    &getArtBody( $id, $BOARD, *body );

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
	$str .= &htmlDecode( $_ );
    }

    # ��Ƭ�������β��Ԥ��ڤ����Ф���
    $str =~ s/^\n*//o;
    $str =~ s/\n*$//o;

    $msg . $str;
}


#### ���̥��å�


###
## checkArticle - ���Ϥ��줿��������Υ����å�
#
# - SYNOPSIS
#	&checkArticle( $board, *postDate, *name, *eMail, *url, *subject, *icon, *article );
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
sub checkArticle
{
    local( $board, *postDate, *name, *eMail, *url, *subject, *icon, *article ) = @_;

    &checkPostDate( *postDate );
    &checkName( *name );
    &checkEmail( *eMail );
    &checkURL( *url );
    &checkSubject( *subject );
    &checkIcon( *icon ) if $SYS_ICON;

    # ��ʸ�ζ������å���
    &fatal( 2, $H_MESG ) if ( $article eq '' );

    if ( $SYS_MAXARTSIZE != 0 )
    {
	local( $length ) = length( $article );
	&fatal( 12, $length ) if ( $length > $SYS_MAXARTSIZE );
    }
}


###
## secureSubject - ������Subject����Ф�
## secureArticle - ������Article����Ф�
#
# - SYNOPSIS
#	&secureSubject( *subject );
#	&secureArticle( *article, $textType );
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
	&cgi'secureXHTML( *subject, *sNeedVec, *sFeatureVec );
    }
    else
    {
	$subject = &htmlEncode( $subject );	# no tags are allowed.
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
	&plainArticleToPreFormatted( *article );
    }
    elsif ( $textType eq $H_TTLABEL[1] )
    {
	# convert to html
	&plainArticleToHtml( *article );
	# secrurity check
	&cgi'secureXHTML( *article, *aNeedVec, *aFeatureVec );
    }
    elsif ( $textType eq $H_TTLABEL[2] )
    {
	# secrurity check
	&cgi'secureXHTML( *article, *aNeedVec, *aFeatureVec );
    }
    else
    {
	# Not selected... pre-formatted
	&plainArticleToPreFormatted( *article );
    }
}


###
## checkPostDate - ����������å�
#
# - SYNOPSIS
#	&checkPostDate( *str );
#
# - ARGS
#	*str		�������UTC����ηв��ÿ���
#
# - DESCRIPTION
#	������Υ����å���Ԥʤ���
#
sub checkPostDate
{
    local( *str ) = @_;

    # ���Ǥ�OK
    return if ( $str eq '' );

    # �������ͤˤʤäƤʤ���?�ʲ��Ϥ˼��Ԥ��Ƥ���-1�ˤʤäƤ�Ϥ���
    &fatal( 21, '' ) if ( $str < 0 );
}


###
## checkSubject - ʸ��������å�: Subject
#
# - SYNOPSIS
#	&checkSubject(*String);
#
# - ARGS
#	*String		Subjectʸ����
#
# - DESCRIPTION
#	Subject��ʸ��������å���Ԥʤ���
#	������ʸ������ä��饨�顼ɽ���롼����ء�
#	(���ץꥱ�������/UI��ʬΥ�����ۤ�����������?)
#
sub checkSubject
{
    local( *String ) = @_;

    &fatal( 2, $H_SUBJECT ) unless $String;
    &fatal( 3, '' ) if ( $String =~ m/[\t\n]/o );

    if ( !$SYS_TAGINSUBJECT )
    {
	&fatal( 4, '' ) if ( $String =~ m/[<>]/o );
    }
}


###
## checkIcon - ʸ��������å�: Icon
#
# - SYNOPSIS
#	&checkIcon( *str );
#
# - ARGS
#	*str		Iconʸ����
#
# - DESCRIPTION
#	Icon��ʸ��������å���Ԥʤ���
#	������ʸ������ä��饨�顼ɽ���롼����ء�
#
sub checkIcon
{
    local( *str ) = @_;

    # ��������Υ����å�; ������������̵���פ����ꡥ
    $str = $H_NOICON if ( !&getIconUrlFromTitle( $str ));

    &fatal( 2, $H_ICON ) if ( !$SYS_ALLOWNOICON && ( $str eq $H_NOICON ));
}


###
## checkName - ʸ��������å�: ��Ƽ�̾
#
# - SYNOPSIS
#	&checkName(*String);
#
# - ARGS
#	*String		��Ƽ�̾ʸ����
#
# - DESCRIPTION
#	��Ƽ�̾��ʸ��������å���Ԥʤ���
#	������ʸ������ä��饨�顼ɽ���롼����ء�
#	(���ץꥱ�������/UI��ʬΥ�����ۤ�����������?)
#
sub checkName
{
    local( *String ) = @_;

    &fatal( 2, $H_FROM ) if ( !$String );
    &fatal( 3, '' ) if ( $String =~ m/[\t\n]/o );

    # ���������������ܡ�
    &fatal( 5, $String ) if ( $String =~ /^\d+$/ );
}


###
## checkPasswd - ʸ��������å�: �ѥ����
#
# - SYNOPSIS
#	&checkPasswd(*String);
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
sub checkPasswd {
    local( *String ) = @_;

    &fatal( 2, $H_PASSWD ) if ( !$String );
    &fatal( 3, $H_PASSWD ) if ( $String =~ /[\t\n]/o );

    return 0;
}


###
## checkEmail - ʸ��������å�: E-Mail addr.
#
# - SYNOPSIS
#	&checkEmail(*String);
#
# - ARGS
#	*String		E-Mail addr.ʸ����
#
# - DESCRIPTION
#	E-Mail addr.��ʸ��������å���Ԥʤ���
#	������ʸ������ä��饨�顼ɽ���롼����ء�
#	(���ץꥱ�������/UI��ʬΥ�����ۤ�����������?)
#
sub checkEmail
{
    local( *String ) = @_;

    if ( $SYS_POSTERMAIL )
    {
	&fatal( 2, $H_MAIL ) if ( !$String );
	# `@'�����äƤʤ��㥢����
	&fatal( 7, 'E-Mail' ) if ( $String !~ /@/ );
    }
    &fatal( 3, '' ) if ( $String =~ m/[\t\n]/o );
}


###
## checkURL - ʸ��������å�: URL
#
# - SYNOPSIS
#	&checkURL(*String);
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
sub checkURL
{
    local( *String ) = @_;

    # http://�����ξ��϶��ˤ��Ƥ��ޤ���
    $String = '' if ( $String =~ m!^http://$!oi );
    &fatal( 7, 'URL' ) if (( $String ne '' ) && ( !&isUrl( $String )));
    &fatal( 3, '' ) if ( $String =~ m/[\t\n]/o );
}


###
## checkBoardDir - ʸ��������å�: �Ǽ��ĥǥ��쥯�ȥ�
#
# - SYNOPSIS
#	&checkBoardDir( *name );
#
# - ARGS
#	*name		�Ǽ��ĥǥ��쥯�ȥ�̾
#
sub checkBoardDir
{
    local( *name ) = @_;
    &fatal( 52, '' ) unless (( $name =~ /\w+/o ) || ( $name =~ /\//o ));
    &fatal( 2, "$H_BOARDά��" ) if ( $name eq '' );
}

###
## checkBoardName - ʸ��������å�: �Ǽ���̾
#
# - SYNOPSIS
#	&checkBoardDir( *intro );
#
# - ARGS
#	*intro		�Ǽ���̾
#
sub checkBoardName
{
    local( *intro ) = @_;
    &fatal( 2, "$H_BOARD̾��" ) if ( $intro eq '' );
}

###
## checkBoardHeader - ʸ��������å�: �Ǽ��ĥإå�
#
# - SYNOPSIS
#	&checkBoardHeader( *header );
#
# - ARGS
#	*header		�Ǽ��ĥإå�
#
sub checkBoardHeader
{
    local( *header ) = @_;
    # ���Ǥ�OK
}


###
## isUser - �桼���Υ����å�
#        
# - SYNOPSIS
#       &isUser( $name );
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
sub isUser
{
    local( $name ) = @_;
    ( $SYS_AUTH && (( $UNAME eq $name ) || (( $UNAME eq $ADMIN ) && ( $name eq $MAINT_NAME ))));
}


###
## isUrl - URL�ι�¤������å�
#
# - SYNOPSIS
#	&isUrl($String);
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
sub isUrl
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
## getFollowIdTree - ��ץ饤�������ڹ�¤�����
#
# - SYNOPSIS
#	&getFollowIdTree($id, *tree);
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
sub getFollowIdTree
{
    local( $id, *tree ) = @_;

    # �����Τ��ᡤ�Ƶ���߾��ʥǡ���������ʤ餳�����̤�ʤ���
    return if ( $id eq '' );

    local( @aidList ) = split( /,/, &getArtDaughters( $id ));

    push( @tree, '(', $id );
    foreach ( @aidList ) { &getFollowIdTree( $_, *tree ); }
    push( @tree, ')' );
}


###
## getFollowIdSet - ̼�Ρ��ɤΥꥹ�Ȥ򽸤��
#
# - SYNOPSIS
#	&getFollowIdSet($Id);
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
sub getFollowIdSet
{
    local( $Id ) = @_;
    local( @Return );
    foreach ( split(/,/, &getArtDaughters( $Id )))
    {
	push( @Return, $_ );
	push( @Return, &getFollowIdSet( $_ )) if ( &getArtDaughters( $_ ) ne '' );
    }
    @Return;
}


###
## getTreeTopArticle - �ڹ�¤�Υȥå׵��������
#
# - SYNOPSIS
#	&getTreeTopArticle( *tree );
#
# - ARGS
#	*tree	�ڹ�¤����Ǽ�ѤߤΥꥹ��
#
# - DESCRIPTION
#	�ڹ�¤�ξܺ٤ˤĤ��Ƥ�&getFollowIdTree()�򻲾ȤΤ��ȡ�
#
# - RETURN
#	����ID
#
sub getTreeTopArticle
{
    local( *tree ) = @_;
    $tree[1];
}


###
## getReplySubject - ��ץ饤Subject������
#
# - SYNOPSIS
#	&getReplySubject( *subjectStr );
#
# - ARGS
#	$subjectStr	Subjectʸ����
#
# - DESCRIPTION
#	��Ƭ�ˡ�Re:�פ�1�Ĥ����Ĥ��롥
#
sub getReplySubject
{
    local( *subjectStr ) = @_;

    # Re:���������
    $subjectStr =~ s/^Re:\s*//oi;

    # TAG�ѥ��󥳡��ɤ��ơ�
    &tagEncode( *subjectStr );

    # ��Ƭ�ˡ�Re: �פ򤯤äĤ����֤���
    $subjectStr = "Re: $subjectStr";
}


###
## getMailSubjectPrefix - �ᥤ����Subject��prefix�����
#
# - SYNOPSIS
#	&getMailSubjectPrefix( $board, $id );
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
sub getMailSubjectPrefix
{
    local( $board, $id ) = @_;
    return "[$board: $id] " if $SYS_MAILHEADBRACKET;
    "";
}


###
## getDateTimeFormatFromUtc - UTC������֤�ɽ��ʸ��������
#
# - SYNOPSIS
#	&getDateTimeFormatFromUtc($Utc);
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
sub getDateTimeFormatFromUtc
{
    local( $utc ) = @_;
    local( $sec, $min, $hour, $mDay, $mon, $year ) = localtime( $utc );
    sprintf( "%d/%d/%d(%02d:%02d)", $year+1900, $mon+1, $mDay, $hour, $min );
}


###
## getYYYY_MM_DD_HH_MM_SSFromUtc - UTC����YYYY/MM/DD(HH:MM:SS)�����
#
# - SYNOPSIS
#	&getYYYY_MM_DD_HH_MM_SSFromUtc( $utc );
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
sub getYYYY_MM_DD_HH_MM_SSFromUtc
{
    local( $utc ) = @_;
    local( $sec, $min, $hour, $mDay, $mon, $year ) = localtime( $utc );
    sprintf( "%d/%d/%d(%02d:%02d:%02d)", $year+1900, $mon+1, $mDay, $hour, $min, $sec );
}


###
## getUtcFromYYYY_MM_DD_HH_MM_SS - YYYY/MM/DD(HH:MM:SS)����UTC�����
#
# - SYNOPSIS
#	&getUtcFromYYYY_MM_DD_HH_MM_SS
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
sub getUtcFromYYYY_MM_DD_HH_MM_SS
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
## getUtcFromYYYY_MM_DD - YYYY/MM/DD����UTC�����
#
# - SYNOPSIS
#	&getUtcFromYYYY_MM_DD
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
sub getUtcFromYYYY_MM_DD
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
## getPath - DB�ե�����Υѥ�̾�μ���
#
# - SYNOPSIS
#	&getPath($DbDir, $File);
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
sub getPath
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
## getStyleSheetURL - �������륷���ȥե������URL�μ���
#
# - SYNOPSIS
#	&getStyleSheetURL( $name );
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
sub getStyleSheetURL
{
    local( $name ) = @_;
    $KB_RESOURCE_URL? "$KB_RESOURCE_URL$RESOURCE_STYLE/$name" : "$RESOURCE_STYLE/$name";
}


###
## getIconURL - ��������ե������URL�μ���
#
# - SYNOPSIS
#	&getIconURL( $file );
#
# - ARGS
#	$file		��������ե�����̾
#
# - DESCRIPTION
#	��������ե������URL̾����Ф���
#
# - RETURN
#	URL��ɽ��ʸ����
#
sub getIconURL
{
    local( $file ) = @_;
    $KB_RESOURCE_URL? "$KB_RESOURCE_URL$RESOURCE_ICON/$file" : "$RESOURCE_ICON/$file";
}


###
## getImgURL - ���᡼����URL�μ���
#
# - SYNOPSIS
#	&getImgURL( $file );
#
# - ARGS
#	$file		���᡼���ե�����̾
#
# - DESCRIPTION
#	���᡼���ե������URL̾����Ф���
#
# - RETURN
#	URL��ɽ��ʸ����
#
sub getImgURL
{
    local( $file ) = @_;
    $KB_RESOURCE_URL? "$KB_RESOURCE_URL$RESOURCE_IMG/$file" : "$RESOURCE_IMG/$file";
}


###
## getIconUrlFromTitle - ��������ե�����URL�μ���
#
# - SYNOPSIS
#	&getIconUrlFromTitle( $icon );
#
# - ARGS
#	$icon		��������ID
#
# - DESCRIPTION
#	��������ID���顤����ID���б����륢������ե������URL�������
#	���奢������⵭���������󰷤���
#
# - RETURN
#	URL��ɽ��ʸ����
#
sub getIconUrlFromTitle
{
    local( $icon ) = @_;
    return $ICON_NEW if ( $icon eq $H_NEWARTICLE );

    local( $file ) = &getBoardIconFile( $icon );

    # check
    return '' unless $file;

    # return
    &getIconURL( $file );
}


###
## getTitleOldIndex - 'old'�ͤμ���
#
# - SYNOPSIS
#	&getTitleOldIndex( $id );
#
# - ARGS
#	$id	�����ֹ�
#
# - DESCRIPTION
#	���ꤷ��ID�ε�����ޤ�褦��old�ͤ�׻����롥
#	&cacheArt���ƤӽФ��ѤߤǤʤ���Фʤ�ʤ���
#
# - RETURN
#	old��
#
sub getTitleOldIndex
{
    local( $id ) = @_;
    local( $old ) = &getNofArt() - int( $id + $DEF_TITLE_NUM/2 );
    ( $old >= 0 )? $old : 0;
}


######################################################################
# �ǡ�������ץ���ơ������


#### �Ǽ��Ĵ�Ϣ


###
## getNofBoard - �Ǽ��Ŀ��μ���
## getBoardId - �Ǽ���ID�μ���
## getBoardNum - �Ǽ����ֹ�μ���
#
# - SYNOPSIS
#	&getNofBoard();
#	&getBoardId( $num );
#	&getBoardNum( $id );
#
# - ARGS
#	$num	�Ǽ����ֹ�
#	$id	�Ǽ���ID
#
# - DESCRIPTION
#	�Ǽ��Ŀ���������롥
#	�Ǽ����ֹ�/�Ǽ���ID���顤ID/�ֹ��������롥
#
# - RETURN
#	�Ǽ��Ŀ�
#	�Ǽ���ID/�Ǽ����ֹ�
#
sub getNofBoard
{
    $#BOARD_ID;
}
sub getBoardId
{
    return '' if ( $_[0] < 0 );
    $BOARD_ID[ $_[0] ];
}
sub getBoardNum
{
    local( $id ) = $_[0];
    foreach ( 0 .. &getNofBoard() )
    {
	return $_ if ( &getBoardId( $_ ) eq $id );
    }
    return -1;
}


###
## getBoardName - �Ǽ���̾�μ���
## getBoardInfo - �Ǽ��ľ���μ���
## getBoardKey - �Ǽ��ĥ����ɥ����μ���
#
# - SYNOPSIS
#	&getBoardName( $id );
#	&getBoardInfo( $id );
#	&getBoardKey( $id );
#
# - ARGS
#	$id	�Ǽ���ID
#
# - DESCRIPTION
#	�Ǽ��ľ����������롥
#
# - RETURN
#	get*
#
sub getBoardName { $BOARD_NAME{ $_[0] }; }
sub getBoardInfo { $BOARD_INFO{ $_[0] }; }
sub getBoardKey
{
    local( $board ) = @_;

    local( $id, $artKey );
    local( $file ) = &getPath( $board, $ARTICLE_NUM_FILE_NAME );
    open( AID, "<$file" ) || &fatal( 1, $file );
    chop( $id = <AID> );
    chop( $artKey = <AID> );
    close AID;
    $artKey;
}


###
## getNofBoardIcon - ����������μ���
## getBoardIconId - ��������ID�μ���
## getBoardIconNum - ���������ֹ�μ���
#
# - SYNOPSIS
#	&getNofBoardIcon();
#	&getBoardIconId( $num );
#	&getBoardIconNum( $id );
#
# - ARGS
#	$num	���������ֹ�
#	$id	��������ID
#
# - DESCRIPTION
#	�����������������롥
#	���������ֹ�/��������ID���顤ID/�ֹ��������롥
#
# - RETURN
#	���������
#	��������ID/���������ֹ�
#
sub getNofBoardIcon
{
    $#ICON_ID;
}
sub getBoardIconId
{
    return '' if ( $_[0] < 0 );
    $ICON_ID[ $_[0] ];
}
sub getBoardIconNum
{
    local( $id ) = $_[0];
    foreach ( 0 .. &getNofBoardIcon() )
    {
	return $_ if ( &getBoardIconId( $_ ) eq $id );
    }
    return -1;
}


###
## getBoardIconFile - ��������ե�����̾�μ���
## getBoardIconHelp - ��������إ�פμ���
## getBoardIconType - �������󥿥��פμ���
#
# - SYNOPSIS
#	&getBoardIconFile( $id );
#	&getBoardIconHelp( $id );
#	&getBoardIconType( $id );
#
# - ARGS
#	$id	��������ID
#
# - DESCRIPTION
#	������������������롥
#
sub getBoardIconFile { $ICON_FILE{ $_[0] }; }
sub getBoardIconHelp { $ICON_HELP{ $_[0] }; }
sub getBoardIconType { $ICON_TYPE{ $_[0] }; }


###
## getBoardLastmod - ����Ǽ��Ĥκǽ�������������
#
# - SYNOPSIS
#	&getBoardLastmod( $board );
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
    $^T - ( -M &getPath( $board, $DB_FILE_NAME )) * 86400;
}


###
## getBoardHeader - �Ǽ����̥إå�DB�����ɤ߹���
#
# - SYNOPSIS
#	&getBoardHeader( $board, *header );
#
# - ARGS
#	$board		�Ǽ���ID
#	*header		�إå�ʸ����
#
sub getBoardHeader
{
    local( $board, *header ) = @_;

    local( $file ) = &getPath( $board, $HEADER_FILE_NAME );
    # �ե����뤬�ʤ�����Τޤ�
    open( DB, "<$file" ) || return;
    while ( <DB> )
    {
	$header .= $_;
    }
    close DB;
}


###
## getBoardSubscriber - �Ǽ��Ĺ��ɼԤμ���
#
# - SYNOPSIS
#	&getBoardSubscriber( $CommentFlag, $Board, *ArriveMail );
#
# - ARGS
#	$CommentFlag	�����ȹԤ�ޤफ�ݤ�(0: �ޤޤʤ�, 1: �ޤ�)
#	$Board		�Ǽ���ID
#	*ArriveMail	������Υᥤ�륢�ɥ쥹�Υꥹ�ȤΥ�ե����
#
# - DESCRIPTION
#	�Ǽ��Ĺ��ɼԤ�������롥
#	�ᥤ�륢�ɥ쥹�����������ݤ����Υ����å��ϡ����ڹԤʤ�ʤ���
#
sub getBoardSubscriber
{
    local($CommentFlag, $Board, *ArriveMail) = @_;
    local($ArriveMailFile);

    $ArriveMailFile = &getPath( $Board, $ARRIVEMAIL_FILE_NAME );
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
## cacheBoard - �Ǽ���DB���ɤ߹���
#
# - SYNOPSIS
#	&cacheBoard();
#
# - DESCRIPTION
#	�Ǽ���DB���顤�Ǽ��ľ�����äƤ��롥
#
sub cacheBoard
{
    local( $i ) = 0;
    local( $bId, $bName, $bInfo );
    local( $dbFile ) = &getPath( $SYS_DIR, $BOARD_FILE );
    open( DB, "<$dbFile" ) || &fatal( 1, $dbFile );
    while ( <DB> )
    {
	next if ( /^\#/o || /^$/o );
	chop;
	( $bId, $bName, $bInfo ) = split( /\t/, $_, 3 );
	$BOARD_ID[$i++] = $bId;
	$BOARD_NAME{$bId} = $bName;
	$BOARD_INFO{$bId} = $bInfo;
    }
    close DB;
}


###
## cacheBoardIcon - ��������DB�����ɤ߹���
#
# - SYNOPSIS
#	&cacheBoardIcon($board);
#
# - ARGS
#	$board		�Ǽ���ID
#
# - DESCRIPTION
#	��������DB���ɤ߹����Ϣ�������������ࡥ
#	����ѿ���@ICON_ID��%ICON_FILE��%ICON_HELP���˲����롥
#
sub cacheBoardIcon
{
    local( $board ) = @_;
    local( $fileName, $title, $help, $type );

    @ICON_ID = %ICON_FILE = %ICON_HELP = %ICON_TYPE = ();

    local( $i ) = 0;
    open( ICON, &getIconPath( "$board.$ICONDEF_POSTFIX" ))
	|| ( open( ICON, &getIconPath( "$DEFAULT_ICONDEF" ))
	    || &fatal( 1, &getIconPath( "$DEFAULT_ICONDEF" )));
    while ( <ICON> )
    {
	next if ( /^\#/o || /^$/o );
	chop;
	( $fileName, $title, $help, $type ) = split( /\t/, $_, 4 );

	$ICON_ID[$i++] = $title;
	$ICON_FILE{$title} = $fileName;
	$ICON_HELP{$title} = $help;
	$ICON_TYPE{$title} = $type || 'article';
    }
    close ICON;
}


###
## getIconPath - ��������DB�ե�����Υѥ�̾�μ���
#
sub getIconPath
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
## updateBoardSubscriber - �Ǽ����̿����ᥤ��������DB��������
#
# - SYNOPSIS
#	&updateBoardSubscriber($Board, *ArriveMail);
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
sub updateBoardSubscriber
{
    local( $Board, *ArriveMail ) = @_;

    local( $File ) = &getPath( $Board, $ARRIVEMAIL_FILE_NAME );
    local( $TmpFile ) = &getPath( $Board, $ARRIVEMAIL_FILE_NAME );
    open( DBTMP, ">$TmpFile" ) || &fatal( 1, $TmpFile );
    local( $line );
    foreach ( @ArriveMail )
    {
	( $line = $_ ) =~ s/\s*$//o;
	print( DBTMP "$line\n" ) || &fatal( 13, $TmpFile );
    }
    close DBTMP || &fatal( 13, $TmpFile );
    rename( $TmpFile, $File ) || &fatal( 14, "$TmpFile -&gt; $File" );
}


###
## updateBoardHeader - �Ǽ����̥إå�DB��������
#
# - SYNOPSIS
#	&updateBoardHeader( $board, *header );
#
# - ARGS
#	$board		�Ǽ���ID
#	*header		�إå�ʸ����
#
sub updateBoardHeader
{
    local( $board, *header ) = @_;

    local( $file ) = &getPath( $board, $HEADER_FILE_NAME );
    local( $tmpFile ) = &getPath( $board, $HEADER_FILE_NAME );
    open( DBTMP, ">$tmpFile" ) || &fatal( 1, $tmpFile );
    print( DBTMP $header ) || &fatal( 13, $tmpFile );
    close DBTMP || &fatal( 13, $tmpFile );
    rename( $tmpFile, $file ) || &fatal( 14, "$tmpFile -&gt; $file" );
}


###
## insertBoard - �Ǽ���DB�ؤ��ɲ�
#
# - SYNOPSIS
#	&insertBoard( $name, $intro, $conf, *arriveMail, *header );
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
sub insertBoard
{
    local( $name, $intro, $conf, *arriveMail, *header ) = @_;

    # �Ǽ��ĥǥ��쥯�ȥ�κ���
    mkdir( $name, 0777 ) || &fatal( 1, $name );

    local( $src, $dest );

    # ����DB�κ����ʥ��ԡ���
    $src = &getPath( $BOARDSRC_DIR, $DB_FILE_NAME );
    $dest = &getPath( $name, $DB_FILE_NAME );
    &copyDb( $src, $dest ) || &fatal( 20, "$src -&gt; $dest" );

    # ������DB�κ����ʥ��ԡ���
    $src = &getPath( $BOARDSRC_DIR, $ARTICLE_NUM_FILE_NAME );
    $dest = &getPath( $name, $ARTICLE_NUM_FILE_NAME );
    &copyDb( $src, $dest ) || &fatal( 20, "$src -&gt; $dest" );

    # ��ư�����ᥤ��DB�κ���
    &updateBoardSubscriber( $name, *arriveMail );

    # �إå��ե�����κ���
    &updateBoardHeader( $name, *header );

    # �Ǹ�ˡ��Ǽ���DB�򹹿�����
    local( $file ) = &getPath( $SYS_DIR, $BOARD_FILE );
    local( $tmpFile ) = &getPath( $SYS_DIR, "$BOARD_FILE.$TMPFILE_SUFFIX$$" );
    local( $dbLine );
    open( DBTMP, ">$tmpFile" ) || &fatal( 1, $tmpFile );
    open( DB, "<$file" ) || &fatal( 1, $file );

    local( $dName, $dIntro, $dConf );
    while ( <DB> )
    {
	if ( /^\#/o || /^$/o )
	{
	    print( DBTMP "$_" ) || &fatal( 13, $tmpFile );
	    next;
	}
	chop;

	( $dName, $dIntro, $dConf ) = split( /\t/, $_, 3 );
	&fatal( 51, $name ) if ( $name eq $dName );

	&genTSV( *dbLine, ( $dName, $dIntro, $dConf ));
	print( DBTMP "$dbLine\n" ) || &fatal( 13, $tmpFile );
    }

    # �����������Υǡ�����񤭲ä��롥
    &genTSV( *dbLine, ( $name, $intro, $conf ));
    print( DBTMP "$dbLine\n" ) || &fatal( 13, $tmpFile );

    # close Files.
    close DB;
    close DBTMP || &fatal( 13, $tmpFile );

    rename( $tmpFile, $file ) || &fatal( 14, "$tmpFile -&gt; $file" );
}


###
## updateBoard - �Ǽ���DB�ι���
#
# - SYNOPSIS
#	&updateBoard( $board, $valid, $intro, $conf, *arriveMail, *header );
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
sub updateBoard
{
    local( $name, $valid, $intro, $conf, *arriveMail, *header ) = @_;

    local( $file ) = &getPath( $SYS_DIR, $BOARD_FILE );
    local( $tmpFile ) = &getPath( $SYS_DIR, "$BOARD_FILE.$TMPFILE_SUFFIX$$" );
    open( DBTMP, ">$tmpFile" ) || &fatal( 1, $tmpFile );
    open( DB, "<$file" ) || &fatal( 1, $file );

    local( $dbLine, $dName, $dIntro, $dConf );
    while ( <DB> ) {

	if ( /^\#/o || /^$/o )
	{
	    print( DBTMP "$_" ) || &fatal( 13, $tmpFile );
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
	&genTSV( *dbLine, ( $dName, $dIntro, $dConf ));
	print( DBTMP "$dbLine\n" ) || &fatal( 13, $tmpFile );
    }

    # close Files.
    close DB;
    close DBTMP || &fatal( 13, $tmpFile );

    # DB�򹹿�����
    rename( $tmpFile, $file ) || &fatal( 14, "$tmpFile -&gt; $file" );

    # ��ư�����ᥤ��DB�⹹�����롥
    &updateBoardSubscriber( $BOARD, *arriveMail );

    # �إå��ե�����⹹�����롥
    &updateBoardHeader( $name, *header );
}


###
## getBoardStatus - �Ǽ��ľ���DB���ɤ߹���
#
# - SYNOPSIS
#	&getBoardStatus( $Board, *id, *artKey );
#
# - ARGS
#	$Board		�Ǽ���ID
#	$id		�ǿ���å�����ID
#	$artKey		����
#
# - DESCRIPTION
#	����κǿ�����ID���ɤ߽Ф���
#
sub getBoardStatus
{
    local( $Board, *id, *artKey ) = @_;

    local( $ArticleNumFile ) = &getPath( $Board, $ARTICLE_NUM_FILE_NAME );
    open( AID, "<$ArticleNumFile" ) || &fatal( 1, $ArticleNumFile );
    chop( $id = <AID> );
    chop( $artKey = <AID> );
    close AID;
}


###
## updateBoardStatus - �Ǽ��ľ���DB�ι���
#
# - SYNOPSIS
#	&updateBoardStatus( $Board, $Id, $artKey );
#
# - ARGS
#	$Board		�Ǽ���ID
#	$Id		�����˽񤭹��൭���ֹ�
#	$artKey		¿�Ž񤭹����ɻ��ѥ���
#
# - DESCRIPTION
#	�����ֹ�DB�ι���
#
sub updateBoardStatus
{
    local( $Board, $Id, $artKey ) = @_;

    local( $File, $TmpFile, $OldArticleId );
    
    # �����Τ����˸Ť����ͤ��㤤! (��������ʤ���OK)
    $OldArticleId = &getNewArtId( $Board );
    &fatal( 10, '' ) if (( $Id =~ /^\d+$/ ) && ( $Id < $OldArticleId ));

    $File = &getPath( $Board, $ARTICLE_NUM_FILE_NAME );
    $TmpFile = &getPath( $Board, "$ARTICLE_NUM_FILE_NAME.$TMPFILE_SUFFIX$$" );
    open( AID, ">$TmpFile" ) || &fatal( 1, $TmpFile );
    print( AID "$Id\n" ) || &fatal( 13, $TmpFile );
    print( AID "$artKey\n" ) || &fatal( 13, $TmpFile );
    close AID || &fatal( 13, $TmpFile );

    rename( $TmpFile, $File ) || &fatal( 14, "$TmpFile -&gt; $File" );
}


#### ��å�������Ϣ


###
## getNofArt - ��å��������μ���
## getArtId - ��å�����ID�μ���
## getArtNum - ��å������ֹ�μ���
#
# - SYNOPSIS
#	&getNofArt();
#	&getArtId( $num );
#	&getArtNum( $id );
#
# - ARGS
#	$num	��å������ֹ�
#	$id	��å�����ID
#
# - DESCRIPTION
#	����å���������������롥����Ѥߥ�å������Ͽ�������ʤ���
#	��å������ֹ�/��å�����ID���顤ID/�ֹ��������롥
#
# - RETURN
#	��å�������
#	��å�����ID/��å������ֹ�
#
sub getNofArt
{
    $#DB_ID;
}
sub getArtId
{
    return '' if ( $_[0] < 0 );
    $DB_ID[ $_[0] ];
}
sub getArtNum
{
    local( $id ) = $_[0];
    foreach ( 0 .. &getNofArt() )
    {
#	return $_ if ( &getArtId( $_ ) eq $id );
	return $_ if ( $DB_ID[$_] eq $id );
    }
    return -1;
}


###
## getArtNewP - ��å����������������ݤ�
#
# - SYNOPSIS
#	&getArtNewP( $id );
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
sub getArtNewP
{
    $DB_NEW{ $_[0] };
}


###
## getArtInfo - ��å���������μ���
#
# - SYNOPSIS
#	&getArtInfo( $id );
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
sub getArticlesInfo { &getArtInfo; }
sub getArtInfo
{
    local( $id ) = @_;
    ( $DB_FID{$id}, $DB_AIDS{$id}, $DB_DATE{$id}, $DB_TITLE{$id}, $DB_ICON{$id}, $DB_REMOTEHOST{$id}, $DB_NAME{$id}, $DB_EMAIL{$id}, $DB_URL{$id}, $DB_FMAIL{$id} );
}


###
## getArtParents - ��å������ƾ���μ���
## getArtParent - ��å������ƾ���μ���
## getArtParentTop - ��å������ƾ���μ���
## getArtDaughters - ��å�����̼����μ���
## getArtSubject - ��å����������ȥ�μ���
## getArtIcon - ��å�������������μ���
## setArtParents - ��å������ƾ��������
## setArtDaughters - ��å�����̼���������
#
# - SYNOPSIS
#	&getArtParents( $id );
#	&getArtParent( $id );
#	&getArtParentTop( $id );
#	&getArtDaughters( $id );
#	&getArtSubject( $id );
#	&getArtIcon( $id );
#
#	&setArtParents( $id, $value );
#	&setArtDaughters( $id, $value );
#
# - ARGS
#	$id	��å�����ID
#	$value	��å�����ID�Υꥹ�ȡʡ�,�׶��ڤ��
#
# - DESCRIPTION
#	��å�������/̼�����������롥
#
sub getArtParents { $DB_FID{ $_[0] }; }
sub getArtDaughters { $DB_AIDS{ $_[0] }; }
sub getArtSubject { $DB_TITLE{ $_[0] }; }
sub getArtIcon { $DB_ICON{ $_[0] }; }
sub getArtParent
{
    local( $parent );
    ( $parent = $DB_FID{ $_[0] } ) =~ s/,.*$//o;
    $parent;
}
sub getArtParentTop
{
    local( $top );
    ( $top = $DB_FID{ $_[0] } ) =~ s/^.*,//o;
    $top || $_[0];
}

sub setArtParents { $DB_FID{ $_[0] } = $_[1]; }
sub setArtDaughters { $DB_AIDS{ $_[0] } = $_[1]; }


###
## getArtAuthor - ��å�������ƼԾ���μ���
#
# - SYNOPSIS
#	&getArtAuthor( $id );
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
sub getArtAuthor
{
    ( $DB_NAME{ $_[0] }, $DB_EMAIL{ $_[0] }, $DB_URL{ $_[0] }, $DB_FMAIL{ $_[0] }, $DB_REMOTEHOST{ $_[0] } );
}


###
## getArtBody - ��å�������ʸ�μ���
#
# - SYNOPSIS
#	&getArtBody( $id, $board, *articleBody );
#
# - ARGS
#	$id		��å�����ID
#	$board		�Ǽ���ID
#	*articleBody	��ʸ�ƹԤ�����������ѿ��ؤΥ�ե����
#
# - DESCRIPTION
#	��å�������ʸ��������롥
#
sub getArtBody
{
    local( $id, $board, *articleBody ) = @_;

    local( $file ) = &getArtFileName( $id, $board );
    open( TMP, "<$file" ) || &fatal( 1, $file );
    while ( <TMP> )
    {
	push( @articleBody, $_ );
    }
    close TMP;
}


###
## getArtModifiedTime - ���뵭���κǽ���������(UTC)�����
#
# - SYNOPSIS
#	&getArtModifiedTime($Id, $Board);
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
sub getArtModifiedTime
{
    local( $Id, $Board ) = @_;

    # 86400 = 24 * 60 * 60
    $^T - ( -M &getArtFileName( $Id, $Board )) * 86400;
}


###
## cacheArt - ����DB�����ɤ߹���
#
# - SYNOPSIS
#	&cacheArt( $board );
#
# - ARGS
#	$board		�Ǽ���ID
#
# - DESCRIPTION
#	��˵�ư���˸ƤӽФ��졤����DB�����Ƥ�����ѿ��˥���å��夹�롥
#
sub DbCache { &cacheArt; }
sub cacheArt
{
    local( $board ) = @_;

    return unless $board;

    local( $dId, $dFid, $dAids, $dDate, $dTitle, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail );

    @DB_ID = %DB_FID = %DB_AIDS = %DB_DATE = %DB_TITLE = %DB_ICON = %DB_REMOTEHOST = %DB_NAME = %DB_EMAIL = %DB_URL = %DB_FMAIL = %DB_NEW = ();

    local( $newIconLimit );
    $newIconLimit = $^T - $SYS_NEWICON_VALUE * 24 * 60 * 60
	if ( $SYS_NEWICON == 2 );
    
    local( $i ) = 0;
    local( @data, $dId );
    local( $DBFile ) = &getPath( $board, $DB_FILE_NAME );
    open( DB, "<$DBFile" ) || &fatal( 1, $DBFile );
    while ( <DB> )
    {
	next if (/^\#/o || /^$/o);
	chop;
	( $dId, $dFid, $dAids, $dDate, $dTitle, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail ) = split( /\t/, $_, 11 );
	$DB_ID[$i++] = $dId;
	$DB_FID{$dId} = $dFid;
	$DB_AIDS{$dId} = $dAids;
	$DB_DATE{$dId} = $dDate || &getArtModifiedTime( $dId, $board );
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
}


###
## insertArt - ����DB�ؤ��ɲ�
#
# - SYNOPSIS
#      &insertArt( $Board, $Fid, $InputDate, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail );
#
# - ARGS
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
sub insertArt
{
    local( $Board, $Fid, $artKey, $InputDate, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail, $MailRelay, $TextType, $Article ) = @_;

    # �����������ֹ�����(�ޤ������ֹ�������Ƥʤ�)
    local( $newArtId ) = &getNewArtId( $Board );

    # �����Υե�����κ���
    &makeArtFile( $TextType, $Article, $newArtId, $Board );

    # �Ǽ��ľ���DB�ι���
    &updateBoardStatus( $Board, $newArtId, $artKey );

    local( $dId, $dFid, $dAids, $dInputDate, $dSubject, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail, $mdName, $mdEmail, $mdInputDate, $mdSubject, $mdIcon, $mdId, $FidList, @FollowMailTo, @FFid );

    # �ᥤ�������Ѥˡ���ץ饤���Υ�ץ饤�������äƤ���
    if ( $Fid ne '' )
    {
	@FFid = split( /,/, &getArtParents( $Fid ));
    }

    $FidList = $Fid;

    local( $File ) = &getPath( $Board, $DB_FILE_NAME );
    local( $TmpFile ) = &getPath( $Board, "$DB_FILE_NAME.$TMPFILE_SUFFIX$$" );
    local( $dbLine );
    open( DBTMP, ">$TmpFile" ) || &fatal( 1, $TmpFile );
    open( DB, "<$File" ) || &fatal( 1, $File );
    while ( <DB> )
    {
	if ( /^\#/o || /^$/o )
	{
	    print( DBTMP "$_" ) || &fatal( 13, $TmpFile );
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
		$dAids .= ",$newArtId";
	    }
	    else
	    {
		$dAids = $newArtId;
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
	&genTSV( *dbLine, ( $dId, $dFid, $dAids, $dInputDate, $dSubject, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail ));
	print( DBTMP "$dbLine\n" ) || &fatal( 13, $TmpFile );

	# ��ץ饤���Υ�ץ饤�������ĥᥤ��������ɬ�פ�����С��������¸
	if ( $MailRelay && ( $SYS_MAIL & 2 ) && @FFid && $dFmail && $dEmail && ( grep( /^$dId$/, @FFid )) && ( !grep( /^$dEmail$/, @FollowMailTo )))
	{
	    push( @FollowMailTo, $dEmail );
	}
    }

    # �����������Υǡ�����񤭲ä��롥
    &genTSV( *dbLine, ( $newArtId, $FidList, '', $InputDate, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail ));
    print( DBTMP "$dbLine\n" ) || &fatal( 13, $TmpFile );

    # close Files.
    close DB;
    close DBTMP || &fatal( 13, $TmpFile );

    # DB�򹹿�����
    rename( $TmpFile, $File ) || &fatal( 14, "$TmpFile -&gt; $File" );

    # ɬ�פʤ���Ƥ����ä����Ȥ�ᥤ�뤹��
    if ( $MailRelay && $SYS_MAIL & 1 )
    {
	local( @ArriveMailTo );
	&getBoardSubscriber( 0, $Board, *ArriveMailTo );
	&arriveMail( $Name, $Email, $InputDate, $Subject, $Icon, $newArtId, @ArriveMailTo ) if @ArriveMailTo;
    }

    # ɬ�פʤ�ȿ�������ä����Ȥ�ᥤ�뤹��
    if ( $MailRelay && ( $SYS_MAIL & 2 ) && @FollowMailTo )
    {
	&followMail( $mdName, $mdEmail, $mdInputDate, $mdSubject, $mdIcon, $mdId, $Name, $Email, $InputDate, $Subject, $Icon, $newArtId, @FollowMailTo );
    }

    $newArtId;
}


###
## updateArt - ���������ε���DB�ؤν񤭹���
#
# - SYNOPSIS
#	&updateArt($Board, $Id, $InputDate, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail);
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
sub updateArt
{
    local( $Board, $Id, $InputDate, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail, $TextType, $Article ) = @_;

    local( $SupersedeId, $dId, $dFid, $dAids, $dInputDate, $dSubject, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail );
    
    # initial version��1�ǡ�1���������Ƥ�����1��2����9��10��11����
    # later version��DB���ɬ����younger version���Ⲽ�˽и����롥
    # ���ʤ��10_2��10��10_1�ϡ�10_1��10_2��10�ν���¤֤�ΤȤ��롥
    $SupersedeId = 1;

    local( $dbLine );
    local( $File ) = &getPath( $Board, $DB_FILE_NAME );
    local( $TmpFile ) = &getPath( $Board, "$DB_FILE_NAME.$TMPFILE_SUFFIX$$" );
    open( DBTMP, ">$TmpFile" ) || &fatal( 1, $TmpFile );
    open( DB, "<$File" ) || &fatal( 1, $File );
    while ( <DB> )
    {
	if ( /^\#/o || /^$/o )
	{
	    print( DBTMP "$_" ) || &fatal( 13, $TmpFile );
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
	    &genTSV( *dbLine, ( sprintf( "-%s_%s", $dId, $SupersedeId ), $dFid, $dAids, $dInputDate, $dSubject, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail ));
	    print( DBTMP "#$dbLine\n" ) || &fatal( 13, $TmpFile );

	    # ³���ƿ�����������񤭲ä���
	    &genTSV( *dbLine, ( $Id, $dFid, $dAids, $InputDate, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail ));
	    print( DBTMP "$dbLine\n" ) || &fatal( 13, $TmpFile );
	}
	else
	{
	    # DB�˽񤭲ä���
	    print( DBTMP "$_\n" ) || &fatal( 13, $TmpFile );
	}
    }

    # close Files.
    close DB;
    close DBTMP || &fatal( 13, $TmpFile );

    # DB�򹹿�����
    rename( $TmpFile, $File ) || &fatal( 14, "$TmpFile -&gt; $File" );

    # ex. ��100�ע���100_5��
    local( $oldFile ) = &getArtFileName( $Id, $Board );
    local( $supersedeFile ) = &getArtFileName( sprintf( "%s_%s", $Id, $SupersedeId ), $Board );
    rename( $oldFile, $supersedeFile ) || &fatal( 14, "$File -&gt; $supersedeFile" );

    # �����Υե�����κ���
    &makeArtFile( $TextType, $Article, $Id, $Board );
}


###
## flushArt - ����DB��������
#
# - SYNOPSIS
#	&flushArt( $Board );
#
# - ARGS
#	$Board		�Ǽ���ID
#
# - DESCRIPTION
#	����DB�򡤿����ʵ����ǡ��������������롥
#	�񤭹��൭���ǡ����ϥ���å��夵��Ƥ����Ρ�
#
sub flushArt
{
    local( $Board ) = @_;

    local( $dId, $dbLine );
    local( $File ) = &getPath($Board, $DB_FILE_NAME);
    local( $TmpFile ) = &getPath( $Board, "$DB_FILE_NAME.$TMPFILE_SUFFIX$$" );
    open( DBTMP, ">$TmpFile" ) || &fatal( 1, $TmpFile );
    open( DB, "<$File" ) || &fatal( 1, $File );
    while ( <DB> )
    {
	if ( /^\#/o || /^$/o )
	{
	    print( DBTMP "$_" ) || &fatal( 13, $TmpFile );
	    next;
	}

	# Id����Ф�
	chop;
	( $dId = $_ ) =~ s/\t.*$//;

	# DB�˽񤭲ä���
	&genTSV( *dbLine, ( $dId, $DB_FID{$dId}, $DB_AIDS{$dId}, $DB_DATE{$dId}, $DB_TITLE{$dId}, $DB_ICON{$dId}, $DB_REMOTEHOST{$dId}, $DB_NAME{$dId}, $DB_EMAIL{$dId}, $DB_URL{$dId}, $DB_FMAIL{$dId} ));
	print( DBTMP "$dbLine\n" ) || &fatal( 13, $TmpFile );
    }

    # close Files.
    close DB;
    close DBTMP || &fatal( 13, $TmpFile );

    # DB�򹹿�����
    rename( $TmpFile, $File ) || &fatal( 14, "$TmpFile -&gt; $File" );

    # DB�񤭴������Τǡ�����å��夷ľ��
    &cacheArt( $Board );
}


###
## deleteArt - ����DB�ι���
#
# - SYNOPSIS
#	&deleteArt( $Board, *Target );
#
# - ARGS
#	$Board		�Ǽ���ID
#	*Target		������뵭��ID�Υꥹ��
#
# - DESCRIPTION
#	����DB������ꤵ�줿�������Υ���ȥ�������롥
#
sub deleteArt
{
    local( $Board, *Target ) = @_;

    local( $dId, $dbLine );
    local( $File ) = &getPath( $Board, $DB_FILE_NAME );
    local( $TmpFile ) = &getPath( $Board, "$DB_FILE_NAME.$TMPFILE_SUFFIX$$" );
    open( DBTMP, ">$TmpFile" ) || &fatal( 1, $TmpFile );
    open( DB, "<$File" ) || &fatal( 1, $File );
    while ( <DB> )
    {
	if ( /^\#/o || /^$/o )
	{
	    print( DBTMP "$_" ) || &fatal( 13, $TmpFile );
	    next;
	}

	# Id����Ф�
	chop;
	( $dId = $_ ) =~ s/\t.*$//;

	# ���������ϥ����ȥ�����
	if ( grep( /^$dId$/, @Target ))
	{
	    print( DBTMP "#" ) || &fatal( 13, $TmpFile );
	}

	&genTSV( *dbLine, ( $dId, $DB_FID{$dId}, $DB_AIDS{$dId}, $DB_DATE{$dId}, $DB_TITLE{$dId}, $DB_ICON{$dId}, $DB_REMOTEHOST{$dId}, $DB_NAME{$dId}, $DB_EMAIL{$dId}, $DB_URL{$dId}, $DB_FMAIL{$dId} ));
	print( DBTMP "$dbLine\n" ) || &fatal( 13, $TmpFile );
    }

    # close Files.
    close DB;
    close DBTMP || &fatal( 13, $TmpFile );

    # DB�򹹿�����
    rename( $TmpFile, $File ) || &fatal( 14, "$TmpFile -&gt; $File" );
}


###
## reOrderArt - ����DB�ν���ѹ�
#
# - SYNOPSIS
#	&reOrderArt( $Board, $Id, *Move );
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
sub reOrderArt
{
    local( $Board, $Id, *Move ) = @_;

    # ��Ƭ�ե饰
    local( $TopFlag ) = 1;

    local( $dId, $dbLine );
    local( $File ) = &getPath( $Board, $DB_FILE_NAME );
    local( $TmpFile ) = &getPath( $Board, "$DB_FILE_NAME.$TMPFILE_SUFFIX$$" );
    open( DBTMP, ">$TmpFile" ) || &fatal( 1, $TmpFile );
    open( DB, "<$File" ) || &fatal( 1, $File );
    while ( <DB> )
    {
	if ( /^\#/o || /^$/o )
	{
	    print( DBTMP "$_" ) || &fatal( 13, $TmpFile );
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
		&genTSV( *dbLine, ( $_, $DB_FID{$_}, $DB_AIDS{$_}, $DB_DATE{$_}, $DB_TITLE{$_}, $DB_ICON{$_}, $DB_REMOTEHOST{$_}, $DB_NAME{$_}, $DB_EMAIL{$_}, $DB_URL{$_}, $DB_FMAIL{$_} ));
		print( DBTMP "$dbLine\n" ) || &fatal( 13, $TmpFile );
	    }
	}

	# ��ư�褬�����顤��˽񤭹���(���夬�塤�ξ��)
	if (( $SYS_BOTTOMTITLE == 0 ) && ( $dId eq $Id ))
	{
	    foreach ( @Move )
	    {
		&genTSV( *dbLine, ( $_, $DB_FID{$_}, $DB_AIDS{$_}, $DB_DATE{$_}, $DB_TITLE{$_}, $DB_ICON{$_}, $DB_REMOTEHOST{$_}, $DB_NAME{$_}, $DB_EMAIL{$_}, $DB_URL{$_}, $DB_FMAIL{$_} ));
		print( DBTMP "$dbLine\n" ) || &fatal( 13, $TmpFile );
	    }
	}

	# DB�˽񤭲ä���
	&genTSV( *dbLine, ( $dId, $DB_FID{$dId}, $DB_AIDS{$dId}, $DB_DATE{$dId}, $DB_TITLE{$dId}, $DB_ICON{$dId}, $DB_REMOTEHOST{$dId}, $DB_NAME{$dId}, $DB_EMAIL{$dId}, $DB_URL{$dId}, $DB_FMAIL{$dId} ));
	print( DBTMP "$dbLine\n" ) || &fatal( 13, $TmpFile );

	# ��ư�褬�����顤³���ƽ񤭹���(���夬�����ξ��)
	if (( $SYS_BOTTOMTITLE == 1 ) && ( $dId eq $Id ))
	{
	    foreach ( @Move )
	    {
		&genTSV( *dbLine, ( $_, $DB_FID{$_}, $DB_AIDS{$_}, $DB_DATE{$_}, $DB_TITLE{$_}, $DB_ICON{$_}, $DB_REMOTEHOST{$_}, $DB_NAME{$_}, $DB_EMAIL{$_}, $DB_URL{$_}, $DB_FMAIL{$_} ));
		print( DBTMP "$dbLine\n" ) || &fatal( 13, $TmpFile );
	    }
	}
    }

    # ��Ƭ�ˤ�����ν���(���夬�塤�ξ��)
    if (( $Id eq '' ) && ( $SYS_BOTTOMTITLE == 0 ))
    {
	foreach ( @Move )
	{
	    &genTSV( *dbLine, ( $_, $DB_FID{$_}, $DB_AIDS{$_}, $DB_DATE{$_}, $DB_TITLE{$_}, $DB_ICON{$_}, $DB_REMOTEHOST{$_}, $DB_NAME{$_}, $DB_EMAIL{$_}, $DB_URL{$_}, $DB_FMAIL{$_} ));
	    print( DBTMP "$dbLine\n" ) || &fatal( 13, $TmpFile );
	}
    }

    # close Files.
    close DB;
    close DBTMP || &fatal( 13, $TmpFile );

    # DB�򹹿�����
    rename( $TmpFile, $File ) || &fatal( 14, "$TmpFile -&gt; $File" );

    # DB�񤭴������Τǡ�����å��夷ľ��
    &cacheArt( $Board );
}


###
## getNewArtId - ���嵭��ID�η���
#
# - SYNOPSIS
#	&getNewArtId($Board);
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
sub getNewArtId
{
    local( $Board ) = @_;
    local( $id, $artKey );
    &getBoardStatus( $Board, *id, *artKey );
    $id + 1;
}


###
## makeArtFile - ������ʸDB�ؤ��ɲ�
#
# - SYNOPSIS
#	&makeArtFile($TextType, $Article, $Id, $Board);
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
sub makeArtFile
{
    local( $TextType, $Article, $Id, $Board ) = @_;

    local( $File ) = &getArtFileName( $Id, $Board );

    open( TMP, ">$File" ) || &fatal( 1, $File );
    printf( TMP "<!-- Kb-System-Id: %s/%s -->\n", $KB_VERSION, $KB_RELEASE)
	|| &fatal( 13, $File );
    print( TMP "$Article\n" ) || &fatal( 13, $File );
    close TMP || &fatal( 13, $File );
}


###
## getArtFileName - ������ʸDB�ե�����Υѥ�̾�μ���
#
# - SYNOPSIS
#	&getArtFileName($Id, $Board);
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
sub getArtFileName
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
## copyDb - DB�Υ��ԡ�
#
# - SYNOPSIS
#	&copyDb( $src, $dest );
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
sub copyDb
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
## genTSV - ���ֶ��ڤ�ʸ����κ���
#
# - SYNOPSIS
#	&genTSV( *line, @data );
#
# - ARGS
#	$line	���ֶ��ڤ�Υǡ������Ǽ����ʸ����
#	@data	�ǡ���
#
# - DESCRIPTION
#	�ǡ�����TSV�ե����ޥåȤ��������롥
#	�ǡ����ϲ��Ԥ�ޤ�ǤϤʤ�ʤ���
#
sub genTSV
{
    local( *line, @data ) = @_;
    grep( s/\t/$COLSEP/go, @data );
    $line = join( "\t", @data );
}
