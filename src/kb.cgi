#!/usr/local/bin/perl
#!/usr/local/bin/perl5.00503-debug -d:DProf
#!/usr/local/bin/perl4.036


# ���Υե�������ѹ��Ϻ���2�սꡤ����4�ս�Ǥ��ʴĶ�����Ǥ��ˡ�
#
# 1. ������Ƭ�Ԥǡ�Perl�Υѥ�����ꤷ�ޤ�����#!�פ�³���ƻ��ꤷ�Ƥ���������

# 2. kb�ǥ��쥯�ȥ�Υե�ѥ�����ꤷ�Ƥ���������URL�ǤϤʤ����ѥ��Ǥ��ˡ�
#    !! KB/1.0R6.4�ʹߡ����������ɬ�ܤȤʤ�ޤ��� !!
#
$KBDIR_PATH = '';
# $KBDIR_PATH = '/home/nahi/public_html';
# $KBDIR_PATH = 'd:\inetpub\wwwroot\kb';	# WinNT/Win9x�ξ��
# $KBDIR_PATH = 'foo:bar:kb';			# Mac�ξ��?

# 3. �����Ф�ư���Ƥ���ޥ���Win95/Mac�ξ�硤
#    $PC��1�����ꤷ�Ƥ��������������Ǥʤ���硤������������פǤ���
#
$PC = 0;	# for UNIX / WinNT
# $PC = 1;	# for Win95 / Mac

# 4. �����Ф�CGIWRAP�����Ѥ��Ƥ����硤�ʲ��Υ����Ȥ򳰤���
#    kb�ǥ��쥯�ȥ��URL����ꤷ�Ƥ��������ʺ��٤ϥѥ��ǤϤʤ���URL�Ǥ��ˡ�
#    �����Ǥʤ��ͤϡ��ѹ���ɬ�פϤ���ޤ��󡥥����ȤΤޤޤ�OK�Ǥ���
#
# $ENV{'PATH_INFO'} = '/~nahi/kb';


# �ʲ��Ͻ񤭴�����ɬ�פϤ���ޤ���


######################################################################


# $Id: kb.cgi,v 5.52 1999-10-20 14:40:43 nakahiro Exp $

# KINOBOARDS: Kinoboards Is Network Opened BOARD System
# Copyright (C) 1995-99 NAKAMURA Hiroshi.
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
$KB_RELEASE = '7��1';		# release
$CHARSET = 'euc';		# �����������Ѵ��ϹԤʤ�ʤ�
$ADMIN = 'admin';		# �ǥե��������
$GUEST = 'guest';		# �ǥե��������

# �ǥ��쥯�ȥ�
$ICON_DIR = 'icons';				# ��������ǥ��쥯�ȥ�
$UI_DIR = 'UI';					# UI�ǥ��쥯�ȥ�
$LOG_DIR = 'log';				# ���ǥ��쥯�ȥ�
$BOARDSRC_DIR = 'board';			# �Ǽ��ĥ������ǥ��쥯�ȥ�

# �ե�����
$BOARD_FILE = 'kinoboards';			# �Ǽ���DB
$CONF_FILE_NAME = 'kb.conf';			# �Ǽ�����configuratin�ե�����
$ARRIVEMAIL_FILE_NAME = 'kb.mail';		# �Ǽ����̿����ᥤ��������DB
$HEADER_FILE_NAME = 'kb.board';			# �����ȥ�ꥹ�ȥإå�DB
$DB_FILE_NAME = 'kb.db';			# ����DB
$ARTICLE_NUM_FILE_NAME = 'kb.aid';		# �����ֹ�DB
$CSS_FILE = 'kbStyle.css';			# �������륷���ȥե�����
$USER_FILE = 'kb.user';				# �桼����DB
$DEFAULT_ICONDEF = 'all.idef';			# ��������DB
$LOCK_FILE = 'kb.lock';				# ��å��ե�����
$LOCK_FILE_B = '';				# �Ǽ����̥�å��ե�����
$ACCESS_LOG = 'access_log';			# �����������ե�����
$ERROR_LOG = 'error_log';			# ���顼���ե�����
# Suffix
$TMPFILE_SUFFIX = 'tmp';			# DB�ƥ�ݥ��ե������Suffix
$ICONDEF_POSTFIX = 'idef';			# ��������DB�ե������Suffix

# CGI��Ʊ��ǥ��쥯�ȥ�ˤ���إå��ե�������ɤ߹���
require( $HEADER_FILE ) if ( -s "$HEADER_FILE" );

# �ᥤ��Υإå��ե�������ɤ߹���
if ( !$KBDIR_PATH || !chdir( $KBDIR_PATH ))
{
    print "Content-Type: text/plain; charset=EUC-JP\n\n";
    print "���顼���������ͤ�:\n";
    print "$0����Ƭ��ʬ���֤���Ƥ���\$KBDIR_PATH����\n";
    print "���������ꤵ��Ƥ��ޤ���\n";
    print "��R6.4�ʹߡ������ѿ������꤬ɬ�ܤȤʤ�ޤ����ˡ�\n";
    print "���ꤷ�Ƥ�����ٻ�ƤߤƤ���������";
    exit 0;
}
# chdir���kb.ph���ɤࡥ���������require�Ѥߤξ����ɤޤʤ���Perl�θ�����͡�
require( $HEADER_FILE ) if ( -s "$HEADER_FILE" );

# ���󥯥롼�ɥե�������ɤ߹���
require( 'cgi.pl' );
require( 'kinologue.pl' );
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

if ( $cgi'PATH_INFO )
{
    $BASE_URL = "http://$cgi'SERVER_NAME$SERVER_PORT_STRING$cgi'PATH_INFO/";
}
else
{
    local( $cgidir ) = substr( $cgi'SCRIPT_NAME, 0, rindex( $cgi'SCRIPT_NAME,
	'/' ));
    $BASE_URL = "http://$cgi'SERVER_NAME$SERVER_PORT_STRING$cgidir/";
}

$SCRIPT_URL = "http://$cgi'SERVER_NAME$SERVER_PORT_STRING$PROGRAM";
$MACPERL = ( $^O eq 'MacOS' );  # isMacPerl?
$PROGNAME = "KINOBOARDS/$KB_VERSION R$KB_RELEASE";
$ENV{'TZ'} = $TIME_ZONE if $TIME_ZONE;

# ���ĥ����Υ١���
$HTML_TAGS_COREATTRS = 'ID/CLASS/STYLE/TITLE';
$HTML_TAGS_I18NATTRS = 'LANG/DIR';
$HTML_TAGS_GENATTRS = "$HTML_TAGS_COREATTRS/$HTML_TAGS_I18NATTRS";

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
	&cgi'unlock_file( $LOCK_FILE );
	&cgi'unlock_file( $LOCK_FILE_B ) if $LOCK_FILE_B;
    }
    &KbLog( $kinologue'SEV_WARN, "Caught a SIG$sig - shutting down..." );
    exit( 1 );
}

# ���ԥ�������ʿ������: XHTML�Ǥ�<br />��<hr />�ˤʤ�ޤ���
$HTML_BR = "<br>\n";
$HTML_HR = "<hr>\n";

# �����륫���󥿡��ե饰
$gLinkNum = 0;
$gTabIndex = 0;
$gBoardDbCached = 0;
$gIconDbCached = '';


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
	    $modTime = &GetModifiedTime( $DB_FILE_NAME, $cgi'TAGS{'b'} );
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
	$c = $BOARD? 'v' : 'bl';
    }

    if ( $BOARD )
    {
	local( $boardConfFileP );
	( $BOARDNAME, $boardConfFileP ) = &GetBoardInfo( $BOARD );
	$LOCK_FILE_B = $LOCK_FILE . ".$BOARD";

	# �Ǽ��ĸ�ͭ���åƥ��󥰤��ɤ߹���
	if ( $boardConfFileP )
	{
	    local( $boardConfFile ) = &GetPath( $BOARD, $CONF_FILE_NAME );
	    require( $boardConfFile ) if ( -s "$boardConfFile" );
	}
    }

    # ���Ƥ�require������ä����ȡ�����

    # ǧ�ھ���ν����
    $cgiauth'GUEST = $GUEST;
    $cgiauth'ADMIN = $ADMIN;
    $USER_AUTH_FILE = &GetPath( $AUTH_DIR, $USER_FILE );

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
	( $err, $UNAME, $PASSWD, @userInfo ) = &cgiauth'CheckUser(
	    $USER_AUTH_FILE );
	    
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
	    # ���ս�˥�����
	    &UISortTitle();
	    last;
	}
	elsif ( $c eq 'l' )
	{
	    # ���������������ս��ɽ��
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
	if  ( $c eq 'ct' )
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
    # �桼������򥯥ꥢ
    if ( $SYS_AUTH == 1 )
    {
	$UNAME = $cgiauth'F_COOKIE_RESET;
    }
    else
    {
	$UNAME = '';
    }
    &htmlGen( 'Login.html' );
}

sub hgLoginForm
{
    &Fatal( 18, "$_[0]/LoginForm" ) if ( $_[0] ne 'Login.html' );

    local( %tags, $msg );
    $msg = &TagLabel( $H_FROM, 'kinoU', 'N' ) . ': ' . &TagInputText( 'text',
	'kinoU', '', $NAME_LENGTH ) . $HTML_BR;
    $msg .= &TagLabel( $H_PASSWD, 'kinoP', 'P' ) . ': ' . &TagInputText(
	'password', 'kinoP', '', $PASSWD_LENGTH ) . $HTML_BR;
    if ( $SYS_AUTH_DEFAULT == 1 )
    {
	$msg .= &TagInputRadio( 'kinoA_url', 'kinoA', '3', 1 ) . ":\n" .
	    &TagLabel( '���å���(HTTP-Cookies)��Ȥ鷺��ǧ�ڤ���', 'kinoA_url',
	    'U' ) . $HTML_BR;
	$msg .= &TagInputRadio( 'kinoA_cookies', 'kinoA', '1', 0 ) . "\n" .
	    &TagLabel( '���å�����ȤäƤ��Υ֥饦���˾����Ф�������',
	   'kinoA_cookies', 'C' ) . $HTML_BR;
    }

    %tags = ( 'c', 'bl', 'kinoT', 'plain' );
    &DumpForm( *tags, '�¹�', '�ꥻ�å�', *msg, 1 );
}


###
## �����ԥѥ���ɤ��������
#
sub UIAdminConfig
{
    &htmlGen( 'AdminConfig.html' );
}

sub hgAdminConfigForm
{
    &Fatal( 18, "$_[0]/AdminConfigForm" ) if ( $_[0] ne 'AdminConfig.html' );

    local( %tags, $msg );
    $msg = &TagLabel( $H_PASSWD, 'confP', 'P' ) . ': ' . &TagInputText(
	'password', 'confP', '', $PASSWD_LENGTH ) . $HTML_BR;
    $msg .= &TagLabel( $H_PASSWD, 'confP2', 'C' ) . ': ' . &TagInputText(
	'password', 'confP2', '', $PASSWD_LENGTH ) .
	'��ǰ�Τ��ᡤ�⤦���٤��ꤤ���ޤ���' . $HTML_BR;
    %tags = ( 'c', 'acx' );
    &DumpForm( *tags, '����', '�ꥻ�å�', *msg, 1 );
}


###
## �����ԥѥ��������μ»�
#
sub UIAdminConfigExec
{
    local( $p1 ) = $cgi'TAGS{'confP'};
    local( $p2 ) = $cgi'TAGS{'confP2'};

    # admin�Τ�
    &Fatal( 44, '' ) unless ( &IsUser( $ADMIN ));

    # lock system.
    &LockAll();

    if ( !$p2 || ( $p1 ne $p2 ))
    {
	&Fatal( 42, $H_PASSWD );
    }
    
    if ( !&cgiauth'SetUserPasswd( $USER_AUTH_FILE , $ADMIN, $p1 ))
    {
	&Fatal( 41, $ADMIN );
    }

    # unlock system
    &UnlockAll();

    # �桼������򥯥ꥢ
    &UILogin();
}


###
## �桼����Ͽ����
#
sub UIUserEntry
{
    # �桼������򥯥ꥢ
    $UNAME = $cgiauth'F_COOKIE_RESET if ( $SYS_AUTH == 1 );
    &htmlGen( 'UserEntry.html' );
}

sub hgUserEntryForm
{
    &Fatal( 18, "$_[0]/UserEntryForm" ) if ( $_[0] ne 'UserEntry.html' );

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
	    
    # lock system
    &LockAll();

    # ������Ͽ����
    local( $res ) = &cgiauth'AddUser( $USER_AUTH_FILE, $user, $p1, $mail,
	$url );

    # unlock system
    &UnlockAll();

    if ( $res == 1 )
    {
	&Fatal( 6, $user );
    }
    elsif ( $res == 2 )
    {
	&Fatal( 998, 'Must not reach here(UserEntryExec).' );
    }

    # ��������̤�
    &UILogin();
}


###
## �桼�������ѹ�
#
sub UIUserConfig
{
    &htmlGen( 'UserConfig.html' );
}

sub hgUserConfigForm
{
    &Fatal( 18, "$_[0]/UserConfigForm" ) if ( $_[0] ne 'UserConfig.html' );

    if ( $POLICY & 8 )
    {
	local( %tags, $msg );
	$msg = &TagLabel( "�ѹ�����$H_USER��$H_FROM", 'confUser', 'N' ) .
	    ': ' . &TagInputText( 'text', 'confUser', '', $NAME_LENGTH ) .
	    "�ʴ����Ԥ���$H_USER��������ѹ��Ǥ��ޤ���" . $HTML_BR . $HTML_BR;
	$msg .= &TagLabel( $H_MAIL, 'confMail', 'M' ) . ': ' . &TagInputText(
	    'text', 'confMail', '', $MAIL_LENGTH ) . $HTML_BR;
	$msg .= &TagLabel( $H_URL, 'confUrl', 'U' ) . ': ' . &TagInputText(
	    'text', 'confUrl', 'http://', $URL_LENGTH ) . $HTML_BR . $HTML_BR;
	$msg .= &TagLabel( $H_PASSWD, 'confP', 'P' ) . ': ' . &TagInputText(
	    'password', 'confP', '', $PASSWD_LENGTH ) . $HTML_BR;
	$msg .= &TagLabel( $H_PASSWD, 'confP2', 'C' ) . ': ' . &TagInputText(
	    'password', 'confP2', '', $PASSWD_LENGTH ) .
	    '��ǰ�Τ��ᡤ�⤦���٤��ꤤ���ޤ���' . $HTML_BR;
	%tags = ( 'c', 'ucx' );
	&DumpForm( *tags, '����', '�ꥻ�å�', *msg );
    }
    else
    {
	$UURL = $UURL || 'http://';

	local( %tags, $msg );
	$msg = &TagLabel( $H_MAIL, 'confMail', 'M' ) . ': ' . &TagInputText(
	    'text', 'confMail', $UMAIL, $MAIL_LENGTH ) . $HTML_BR;
	$msg .= &TagLabel( $H_URL, 'confUrl', 'U' ) . ': ' . &TagInputText(
	    'text', 'confUrl', $UURL, $URL_LENGTH ) . $HTML_BR . $HTML_BR;
	$msg .= &TagLabel( $H_PASSWD, 'confP', 'P' ) . ': ' . &TagInputText(
	    'password', 'confP', '', $PASSWD_LENGTH ) . $HTML_BR;
	$msg .= &TagLabel( $H_PASSWD, 'confP2', 'C' ) . ': ' . &TagInputText(
	    'password', 'confP2', '', $PASSWD_LENGTH ) .
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
    local( $p1 ) = $cgi'TAGS{'confP'};
    local( $p2 ) = $cgi'TAGS{'confP2'};
    local( $user ) = $cgi'TAGS{'confUser'};
    local( $mail ) = $cgi'TAGS{'confMail'};
    local( $url ) = $cgi'TAGS{'confUrl'};

    $user = $UNAME unless ( $POLICY & 8 );

    &CheckName( *user );
    &CheckEmail( *mail );
    &CheckURL( *url );
		
    # lock system
    &LockAll();

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

    # unlock system
    &UnlockAll();

    &UIBoardList();
}


###
## �Ǽ�����Ͽ����
#
sub UIBoardEntry
{
    &htmlGen( 'BoardEntry.html' );
}

sub hgBoardEntryForm
{
    &Fatal( 18, "$_[0]/BoardEntryForm" ) if ( $_[0] ne 'BoardEntry.html' );

    local( %tags, $msg );
    $msg = &TagLabel( "$H_BOARDά��", 'name', 'B' ) . ': ' . &TagInputText(
	'text', 'name', '', $BOARDNAME_LENGTH ) . $HTML_BR;
    $msg .= &TagLabel( "$H_BOARD̾��", 'intro', 'N' ) . ': ' . &TagInputText(
	'text', 'intro', '', $BOARDNAME_LENGTH ) . $HTML_BR . $HTML_BR;
    $msg .= &TagLabel( "$H_BOARD�μ�ư�ᥤ���ۿ���", 'armail', 'M' ) .
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

    &LockAll();
    &AddBoardDb( $name, $intro, 0, *arriveMail, *header );
    &UnlockAll();

    &UIBoardList();
}


###
## �Ǽ��������ѹ�����
#
sub UIBoardConfig
{
    &LockAll();
    &LockBoard();

    # ���Ǽ��Ĥξ������Ф�
    @gArriveMail = ();
    &GetArriveMailTo(1, $BOARD, *gArriveMail); # ����ȥ����Ȥ���Ф�
    $gHeader = "";
    &GetHeaderDb( $BOARD, *gHeader ); # �إå�ʸ�������Ф�

    # unlock system
    &UnlockBoard();
    &UnlockAll();

    &htmlGen( 'BoardConfig.html' );
}

sub hgBoardConfigForm
{
    &Fatal( 18, "$_[0]/BoardConfigForm" ) if ( $_[0] ne 'BoardConfig.html' );

    local( %tags, $msg );
    $msg = &TagLabel( "��$BOARD��$H_BOARD������", 'valid', 'V' ) . ': ' .
	&TagInputCheck( 'valid', 1 ) . $HTML_BR . $HTML_BR;
    $msg .= &TagLabel( "��$BOARD��̾��", 'intro', 'N' ) . ': ' .
	&TagInputText( 'text', 'intro', $BOARDNAME, $BOARDNAME_LENGTH ) .
	$HTML_BR . $HTML_BR;
    local( $all );
    foreach ( @gArriveMail ) { $all .= $_ . "\n"; }
    $msg .= &TagLabel( "��$BOARD�פμ�ư�ᥤ���ۿ���", 'armail', 'M' ) .
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
    local( $valid ) = $cgi'TAGS{'valid'};
    local( $intro ) = $cgi'TAGS{'intro'};
    local( $armail ) = $cgi'TAGS{'armail'};
    local( $header ) = $cgi'TAGS{'article'};

    &CheckBoardName( *intro );
    &CheckBoardHeader( *header );
    &secureSubject( *intro );
    &secureArticle( *header, $H_TTLABEL[2] );
    local( @arriveMail ) = split( /\n/, $armail );

    &LockAll();
    &UpdateBoardDb( $BOARD, $valid, $intro, 0, *arriveMail, *header );
    &UnlockAll();

    &UIBoardList();
}


###
## �Ǽ��İ���
#
sub UIBoardList
{
    &htmlGen( 'BoardList.html' );
}


###
## ��å�����������Ͽ�Υ���ȥ�
## ��ץ饤��å�������Ͽ�Υ���ȥ�
## ��å����������Υ���ȥ�
#
sub UIPostNewEntry
{
    if ( $SYS_NEWART_ADMINONLY && !( $POLICY & 8 ))
    {
	&Fatal( 99, $cgi'TAGS{'c'} );
    }

    local( $back ) = @_;

    $gId = '';			# 0�Ǥϥ��ᡥ���������ե�����̾�⤢�뤫�⡥
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
    &htmlGen( 'PostNewEntry.html' );
}

sub UIPostReplyEntry
{
    local( $back, $quoteFlag ) = @_;

    &LockBoard();
    &DbCache( $BOARD ) if $BOARD;

    $gId = $cgi'TAGS{'id'};
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
	if ( $DefSubject eq '' )
	{
	    local( $tmp );
	    ( $tmp, $tmp, $tmp, $gDefSubject ) = &GetArticlesInfo( $gId );
	    &GetReplySubject( *gDefSubject );
	}
    }
    else
    {
	if ( $gDefSubject eq '' )
	{
	    local( $tmp );
	    ( $tmp, $tmp, $tmp, $gDefSubject ) = &GetArticlesInfo( $gId );
	    &GetReplySubject( *gDefSubject );
	}
	&QuoteOriginalArticle( $gId, *gDefArticle );
    }

    &UnlockBoard();

    $gEntryType = 'reply';		# ��ץ饤
    &htmlGen( 'PostReplyEntry.html' );
}

sub UISupersedeEntry
{
    if ( !( $POLICY & 8 ) && ( $SYS_OVERWRITE == 0 ))
    {
	&Fatal( 99, $cgi'TAGS{'c'} );
    }

    local( $back ) = @_;

    &LockBoard();
    &DbCache( $BOARD ) if $BOARD;

    $gId = $cgi'TAGS{'id'};
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
	local( $tmp );
	( $tmp, $tmp, $tmp, $gDefSubject, $gDefIcon , $tmp, $gDefName,
	    $gDefEmail, $gDefUrl ) = &GetArticlesInfo( $gId );
	&QuoteOriginalArticleWithoutQMark( $gId, *gDefArticle );
    }

    &UnlockBoard();

    $gEntryType = 'supersede';		# ����
    &htmlGen( 'SupersedeEntry.html' );
}

sub hgPostReplyEntryOrigArticle
{
    if ( $_[0] ne 'PostReplyEntry.html' )
    {
	&Fatal( 18, "$_[0]/PostReplyEntryOrigArticle" );
    }

    &DumpArtBody( $gId, 0, 1 );
}

sub hgSupersedeEntryOrigArticle
{
    if ( $_[0] ne 'SupersedeEntry.html' )
    {
	&Fatal( 18, "$_[0]/SupersedeEntryOrigArticle" );
    }

    &DumpArtBody( $gId, 0, 1 );
}


###
## ��å�������Ͽ�Υץ�ӥ塼
## ��å����������Υץ�ӥ塼
#
sub UIPostPreview
{
    &UIPostPreviewMain( 'post' );
    &htmlGen( 'PostPreview.html' );
}

sub UISupersedePreview
{
    if ( !( $POLICY & 8 ) && ( $SYS_OVERWRITE == 0 ))
    {
	&Fatal( 99, $cgi'TAGS{'c'} );
    }

    &UIPostPreviewMain( 'supersede' );
    &htmlGen( 'SupersedePreview.html' );
}

sub UIPostPreviewMain
{
    local( $type ) = @_;

    # ���Ϥ��줿��������
    $gOrigId = $cgi'TAGS{'id'};
    $gSubject = $cgi'TAGS{'subject'};
    $gIcon = $cgi'TAGS{'icon'};
    $gArticle = $cgi'TAGS{'article'};
    $gTextType = $cgi'TAGS{'texttype'};

    &LockAll();
    &LockBoard();
    &DbCache( $BOARD ) if $BOARD;

    ( $gO2Id ) = &GetArticlesInfo( $gOrigId ) if ( $gOrigId ne '' );

    # �桼������μ���
    if ( &IsUser( $ADMIN ))
    {
	$gName = $MAINT_NAME;
	$gEmail = $MAINT;
	$gUrl = $MAINT_URL;
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

    # ���Ϥ��줿��������Υ����å�
    &CheckArticle( $BOARD, *gName, *gEmail, *gUrl, *gSubject, *gIcon,
	*gArticle );

    &UnlockBoard();
    &UnlockAll();
}

sub hgPostPreviewForm
{
    &Fatal( 18, "$_[0]/PostPreviewForm" ) if ( $_[0] ne 'PostPreview.html' );

    require( 'mimer.pl' );

    local( $supersede ) = $_[1];

    local( %tags, $msg );
    $msg = &TagInputRadio( 'com_e', 'com', 'e', 0 ) . ":\n" . &TagLabel(
	'��äƤ��ʤ���', 'com_e', 'P' ) . $HTML_BR;
    $msg .= &TagInputRadio( 'com_x', 'com', 'x', 1 ) . "\n" . &TagLabel(
	'��Ͽ����', 'com_x', 'X' ) . $HTML_BR;
    %tags = ( 'corig', $cgi'TAGS{'corig'}, 'c', 'x', 'b', $BOARD,
	     'id', $gOrigId, 'texttype', $gTextType, 'name', $gName,
	     'mail', $gEmail, 'url', $gUrl, 'icon', $gIcon,
	     'subject', $gEncSubject, 'article', $gEncArticle,
	     'fmail', $cgi'TAGS{'fmail'}, 's', $supersede,
	     'op', $cgi'TAGS{'op'} );

    &DumpForm( *tags, '�¹�', '', *msg );
}

sub hgSupersedePreviewForm
{
    if ( $_[0] ne 'SupersedePreview.html' )
    {
	&Fatal( 18, "$_[0]/SupersedePreviewForm" );
    }

    &hgPostPreviewForm( 'PostPreview.html', 1 );
}

sub hgPostPreviewBody
{
    &Fatal( 18, "$_[0]/PostPreviewBody" ) if ( $_[0] ne 'PostPreview.html' );
    &DumpArtBody( '', 0, 1, $gOrigId, 0, $^T, $gSubject, $gIcon, 0, $gName,
	$gEmail, $gUrl, $gArticle );
}

sub hgSupersedePreviewBody
{
    if ( $_[0] ne 'SupersedePreview.html' )
    {
	&Fatal( 18, "$_[0]/SupersedePreviewBody" );
    }

    &hgPostPreviewBody( 'PostPreview.html' );
}

sub hgSupersedePreviewOrigArticle
{
    if ( $_[0] ne 'SupersedePreview.html' )
    {
	&Fatal( 18, "$_[0]/SupersedePreviewOrigArticle" );
    }

    &DumpArtBody( $gOrigId, 0, 1 );
}


###
## ��������Ͽ
## ����������
#
sub UIPostExec
{
    local( $previewFlag ) = @_;
    &UIPostExecMain( $previewFlag, 'post' );
    &htmlGen( 'PostExec.html' );
}

sub UISupersedeExec
{
    if ( !( $POLICY & 8 ) && ( $SYS_OVERWRITE == 0 ))
    {
	&Fatal( 99, $cgi'TAGS{'c'} );
    }

    local( $previewFlag ) = @_;
    &UIPostExecMain( $previewFlag, 'supersede' );
    &htmlGen( 'SupersedeExec.html' );
}

sub UIPostExecMain
{
    require( 'mimer.pl' );

    local( $previewFlag, $type ) = @_;

    # ���Ϥ��줿��������
    $gOrigId = $cgi'TAGS{'id'};
    local( $TextType ) = $cgi'TAGS{'texttype'};
    local( $Icon ) = $cgi'TAGS{'icon'};
    local( $Subject ) = $cgi'TAGS{'subject'};
    local( $Article ) = $cgi'TAGS{'article'};
    local( $Fmail ) = $cgi'TAGS{'fmail'};
    local( $op ) = $cgi'TAGS{'op'};

    &LockAll();
    &LockBoard();
    &DbCache( $BOARD ) if $BOARD;

    # �桼������μ���
    local( $Name, $Email, $Url );
    if ( &IsUser( $ADMIN ))
    {
	$Name = $MAINT_NAME;
	$Email = $MAINT;
	$Url = $MAINT_URL;
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

    # ����Ⱦ���δ֤��������줿�ե����फ�餷����Ƥ���Ĥ��ʤ���
    local( $base ) = ( -M &GetPath( $BOARD, $DB_FILE_NAME ));
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

    &secureSubject( *Subject );
    &secureArticle( *Article, $TextType );

    if ( $type eq 'post' )
    {
	# �����κ���
	$gNewArtId = &MakeNewArticle( $BOARD, $gOrigId, $op, $TextType, $Name,
	    $Email, $Url, $Icon, $Subject, $Article, $Fmail, 1 );
    }
    elsif ( $type eq 'supersede' )
    {
	# ����������
	local( $tmp, $aids, $name );
	( $tmp, $aids, $tmp, $tmp, $tmp, $tmp, $name ) = &GetArticlesInfo(
	    $gOrigId );
	&Fatal( 44, '' ) if ( !&IsUser( $name ) && !( $POLICY & 8 ));
	&Fatal( 19, '' ) if ( $aids && ( $SYS_OVERWRITE == 1 ));

	$gNewArtId = &SupersedeArticle( $BOARD, $gOrigId, $TextType, $Name,
	    $Email, $Url, $Icon, $Subject, $Article, $Fmail );
    }
    else
    {
	&Fatal( 998, 'Must not reache here(UIPostExecMain).' );
    }

    &UnlockBoard();
    &UnlockAll();
}

sub hgPostExecJumpToNewArticle
{
    if ( $_[0] ne 'PostExec.html' )
    {
	&Fatal( 18, "$_[0]/PostExecJumpToNewArticle" );
    }

    &DumpButtonToArticle( $BOARD, $gNewArtId, "�񤭹����$H_MESG��" );
}

sub hgSupersedeExecJumpToNewArticle
{
    if ( $_[0] ne 'SupersedeExec.html' )
    {
	&Fatal( 18, "$_[0]/SupersedeExecJumpToNewArticle" );
    }

    &DumpButtonToArticle( $BOARD, $gNewArtId, "��������$H_MESG��" );
}

sub hgPostExecJumpToOrigArticle
{
    if ( $_[0] ne 'PostExec.html' )
    {
	&Fatal( 18, "$_[0]/PostExecJumpToOrigArticle" );
    }

    if ( $gOrigId ne '' )
    {
	&DumpButtonToArticle( $BOARD, $gOrigId, "$H_ORIG��$H_MESG��" );
    }
}


###
## ����å��̥����ȥ뤪��ӵ�������
#
sub UIThreadArticle
{
    %gADDFLAG = ();
    @gIDLIST = ();

    &LockBoard();
    &DbCache( $BOARD ) if $BOARD;
    &UnlockBoard();

    # ɽ������Ŀ������
    $gNum = $cgi'TAGS{'num'};
    if ( defined( $cgi'TAGS{'id'} ))
    {
	$gOld = $#DB_ID - int( $cgi'TAGS{'id'} + $gNum/2 );
	$gOld = 0 if ( $gOld < 0 );
    }
    else
    {
	$gOld = $cgi'TAGS{'old'};
    }
    $gRev = $cgi'TAGS{'rev'};
    $gFold = $cgi'TAGS{'fold'} || 0;
    $gVRev = $gRev? 1-$SYS_BOTTOMTITLE : $SYS_BOTTOMTITLE;
    $gTo = $#DB_ID - $gOld;
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
	$gADDFLAG{$DB_ID[$IdNum]} = 2;
    }

    &htmlGen( 'ThreadArticle.html' );
}

sub hgThreadArticleTree
{
    if ( $_[0] ne 'ThreadArticle.html' )
    {
	&Fatal( 18, "$_[0]/ThreadArticleTree" );
    }

    $gHgStr .= $HTML_HR . "<ul>\n";
    
    local( $AddNum ) = "&num=$gNum&old=$gOld&rev=$gRev";

    local( $Id, $IdNum, $Fid );
    if ($gTo < $gFrom)
    {
	# �����ä��ġ�
	$gHgStr .= "<li>$H_NOARTICLE</li>\n";
    }
    elsif ( $gVRev )
    {
	for( $IdNum = $gFrom; $IdNum <= $gTo; $IdNum++ )
	{
	    # ����������ID����Ф�
	    $Id = $DB_ID[$IdNum];
	    ($Fid = $DB_FID{$Id}) =~ s/,.*$//o;
	    # �������Ȥϸ�󤷡�
	    next if ((( $Fid ne '' ) && ( $SYS_THREAD_FORMAT == 2 )) ||
		( $gADDFLAG{$Fid} == 2 ));
	    # �Ρ��ɤ�ɽ��
	    if ( !$gExapand )
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
	    # &cgiprint'Cache( $gHgStr ); $gHgStr = '';
	}
    }
    else
    {
	for( $IdNum = $gTo; $IdNum >= $gFrom; $IdNum-- )
	{
	    $Id = $DB_ID[$IdNum];
	    ($Fid = $DB_FID{$Id}) =~ s/,.*$//o;
	    next if ((( $Fid ne '' ) && ( $SYS_THREAD_FORMAT == 2 )) ||
		( $gADDFLAG{$Fid} == 2 ));

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
	    # &cgiprint'Cache( $gHgStr ); $gHgStr = '';
	}
    }
    $gHgStr .= "</ul>\n";
}

sub hgThreadArticleBody
{
    if ( $_[0] ne 'ThreadArticle.html' )
    {
	&Fatal( 18, "$_[0]/ThreadArticleBody" );
    }

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
    ( $gComType ) = @_;
    
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

    &LockBoard();
    &DbCache( $BOARD ) if $BOARD;

    if ( $gComType == 3 )
    {
	# ��󥯤��������μ»�
	&ReLinkExec( $cgi'TAGS{'rfid'}, $cgi'TAGS{'rtid'}, $BOARD );
    }
    elsif ( $gComType == 5 )
    {
	# ��ư�μ»�
	&ReOrderExec( $cgi'TAGS{'rfid'}, $cgi'TAGS{'rtid'}, $BOARD );
    }

    &UnlockBoard();

    # ɽ������Ŀ������
    $gNum = $cgi'TAGS{'num'};
    if ( defined( $cgi'TAGS{'id'} ))
    {
	$gOld = $#DB_ID - int( $cgi'TAGS{'id'} + $gNum/2 );
	$gOld = 0 if ( $gOld < 0 );
    }
    else
    {
	$gOld = $cgi'TAGS{'old'};
    }
    $gRev = $cgi'TAGS{'rev'};
    $gFold = $cgi'TAGS{'fold'} || 0;
    $gVRev = $gRev? 1-$SYS_BOTTOMTITLE : $SYS_BOTTOMTITLE;
    $gTo = $#DB_ID - $gOld;
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
	$gADDFLAG{$DB_ID[$IdNum]} = 2;
    }

    &htmlGen( 'ThreadTitle.html' );
}

sub hgThreadTitleBoardHeader
{
    if ( $_[0] ne 'ThreadTitle.html' )
    {
	&Fatal( 18, "$_[0]/ThreadTitleBoardHeader" )
	}

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
	    $gHgStr .= "<ul>\n<li>" . &LinkP( "b=$BOARD&c=ce&rtid=" .
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
<li>$H_DELETE_ICON:
����$H_MESG�������ޤ���</li>
<li>$H_SUPERSEDE_ICON:
����$H_MESG���������ޤ���</li>
<li>$H_RELINKTO_MARK:
��˻��ꤷ��$H_MESG��$H_REPLY��򡤤���$H_MESG�ˤ��ޤ���</li>
<li>$H_REORDERTO_MARK:
��˻��ꤷ��$H_MESG�򡤤���$H_MESG�β��˰�ư���ޤ���</li>
</ul>
EOS
    }
}

sub hgThreadTitleTree
{
    &Fatal( 18, "$_[0]/ThreadTitleTree" ) if ( $_[0] ne 'ThreadTitle.html' );

    $gHgStr .= "<ul>\n";

    local( $AddNum ) = "&num=$gNum&old=$gOld&rev=$gRev";

    local( $IdNum, $Id, $Fid );
    if ( $gTo < $gFrom )
    {
	# �����ä��ġ�
	$gHgStr .= "<li>$H_NOARTICLE</li>\n";
    }
    elsif ( $gVRev )
    {
	# �Ť��Τ������
	if (( $gComType == 2 ) && ( $DB_FID{$cgi'TAGS{'rfid'}} ne '' ))
	{
	    $gHgStr .= '<li>' . &LinkP( "b=$BOARD&c=ce&rtid=&rfid=" .
		$cgi'TAGS{'rfid'} . '&roid=' . $cgi'TAGS{'roid'} . $AddNum,
		"[�ɤ�$H_MESG�ؤ�$H_REPLY�Ǥ�ʤ�������$H_MESG�ˤ���]" ) .
		"</li>\n";
	}
	elsif ( $gComType == 4 )
	{
	    $gHgStr .= '<li>' . &LinkP( "b=$BOARD&c=mve&rtid=&rfid=" .
		$cgi'TAGS{'rfid'} . "&roid=" . $cgi'TAGS{'roid'} . $AddNum,
		"[����������Ƭ�˰�ư����(���Υڡ����Ρ��ǤϤ���ޤ���)]" ) .
		"</li>\n";
	}

	for( $IdNum = $gFrom; $IdNum <= $gTo; $IdNum++ )
	{
	    # ����������ID����Ф�
	    $Id = $DB_ID[$IdNum];
	    ($Fid = $DB_FID{$Id}) =~ s/,.*$//o;
	    # �������Ȥϸ�󤷡�
	    next if ((( $Fid ne '' ) && ( $SYS_THREAD_FORMAT == 2 )) ||
		( $gADDFLAG{$Fid} == 2 ));
	    # �Ρ��ɤ�ɽ��
	    if ( $POLICY & 8 )
	    {
		&ThreadTitleNodeMaint( $Id, $gComType, $AddNum, 1 );
	    }
	    else
	    {
		if ( $gFold )
		{
		    &ThreadTitleNodeNoThread( $Id, 1 );
		}
		elsif ( $SYS_THREAD_FORMAT == 0 )
		{
		    &ThreadTitleNodeThread( $Id, 1 );
		}
		elsif ( $SYS_THREAD_FORMAT == 1 )
		{
		    &ThreadTitleNodeAllThread( $Id, 1 );
		}
		else
		{
		    &ThreadTitleNodeNoThread( $Id, 1 );
		}
	    }
	    # &cgiprint'Cache( $gHgStr ); $gHgStr = '';
	}
    }
    else
    {
	# �������Τ������
	if (( $gComType == 2 ) && ( $DB_FID{$cgi'TAGS{'rfid'}} ne '' ))
	{
	    $gHgStr .= '<li>' . &LinkP( "b=$BOARD&c=ce&rtid=&rfid=" .
		$cgi'TAGS{'rfid'} . "&roid=" . $cgi'TAGS{'roid'} . $AddNum,
		"[�ɤ�$H_MESG�ؤ�$H_REPLY�Ǥ�ʤ�������$H_MESG�ˤ���]" ) .
		"</li>\n";
	}
	elsif ( $gComType == 4 )
	{
	    $gHgStr .= '<li>' . &LinkP( "b=$BOARD&c=mve&rtid=&rfid=" .
		$cgi'TAGS{'rfid'} . "&roid=" . $cgi'TAGS{'roid'} . $AddNum,
		"[����������Ƭ�˰�ư����(���Υڡ����Ρ��ǤϤ���ޤ���)]" ) .
		"</li>\n";
	}

	for( $IdNum = $gTo; $IdNum >= $gFrom; $IdNum-- )
	{
	    # ���Ʊ��
	    $Id = $DB_ID[$IdNum];
	    ($Fid = $DB_FID{$Id}) =~ s/,.*$//o;
	    next if ((( $Fid ne '' ) && ( $SYS_THREAD_FORMAT == 2 )) ||
		( $gADDFLAG{$Fid} == 2 ));

	    if ( $POLICY & 8 )
	    {
		&ThreadTitleNodeMaint( $Id, $gComType, $AddNum, 1 );
	    }
	    else
	    {
		if ( $gFold )
		{
		    &ThreadTitleNodeNoThread( $Id, 1 );
		}
		elsif ( $SYS_THREAD_FORMAT == 0 )
		{
		    &ThreadTitleNodeThread( $Id, 1 );
		}
		elsif ( $SYS_THREAD_FORMAT == 1 )
		{
		    &ThreadTitleNodeAllThread( $Id, 1 );
		}
		else
		{
		    &ThreadTitleNodeNoThread( $Id, 1 );
		}
	    }
	    # &cgiprint'Cache( $gHgStr ); $gHgStr = '';
	}
    }
    $gHgStr .= "</ul>\n";
}

# ����Ρ��ɤΤ�ɽ��
sub ThreadTitleNodeNoThread
{
    local( $Id, $flag ) = @_;
    &DumpArtSummaryItem( $Id, $DB_AIDS{$Id}, $DB_ICON{$Id}, $DB_TITLE{$Id},
	$DB_NAME{$Id}, $DB_DATE{$Id}, $flag );
    $flag &= 6; # 110
    push( @gIDLIST, $Id );
    $gHgStr .= "</li>\n";
}

# �ڡ����⥹��åɤΤ�ɽ��
sub ThreadTitleNodeThread
{
    local( $Id, $flag ) = @_;

    # �ڡ������ʤ餪���ޤ���
    return if ( $gADDFLAG{$Id} != 2 );

    &DumpArtSummaryItem( $Id, $DB_AIDS{$Id}, $DB_ICON{$Id}, $DB_TITLE{$Id},
	$DB_NAME{$Id}, $DB_DATE{$Id}, $flag );
    $flag &= 6; # 110

    $gADDFLAG{$Id} = 1;		# �����Ѥ�
    push( @gIDLIST, $Id );

    # ̼�����Сġ�
    if ( $DB_AIDS{$Id} )
    {
	$gHgStr .= "<ul>\n";
	grep( &ThreadTitleNodeThread( $_, $flag ), split( /,/,
	    $DB_AIDS{$Id} ));
	$gHgStr .= "</ul>\n";
    }
    $gHgStr .= "</li>\n";
}

# ������åɤ�ɽ��
sub ThreadTitleNodeAllThread
{
    local( $Id, $flag ) = @_;

    # ɽ���Ѥߤʤ餪���ޤ���
    return if ( $gADDFLAG{$Id} == 1 );

    &DumpArtSummaryItem( $Id, $DB_AIDS{$Id}, $DB_ICON{$Id}, $DB_TITLE{$Id},
	$DB_NAME{$Id}, $DB_DATE{$Id}, $flag );
    $flag &= 6; # 110
    $gADDFLAG{$Id} = 1;		# �����Ѥ�
    push( @gIDLIST, $Id );

    # ̼�����Сġ�
    if ( $DB_AIDS{$Id} )
    {
	$gHgStr .= "<ul>\n";
	grep( &ThreadTitleNodeAllThread( $_, $flag ),
	     split( /,/, $DB_AIDS{$Id} ));
	$gHgStr .= "</ul>\n";
    }
    $gHgStr .= "</li>\n";
}

# �������ѤΥ���å�ɽ��
sub ThreadTitleNodeMaint
{
    local( $Id, $ComType, $AddNum, $flag ) = @_;

    return if ( $gADDFLAG{$Id} != 2 );

    local($FromId) = $cgi'TAGS{'rfid'};

    &DumpArtSummaryItem( $Id, $DB_AIDS{$Id}, $DB_ICON{$Id}, $DB_TITLE{$Id},
	$DB_NAME{$Id}, $DB_DATE{$Id}, $flag );
    $flag &= 6; # 110
    $gHgStr .= " .......... \n";

    # ������ѹ����ޥ��(From)
    # ��ư���ޥ��(From)
    $gHgStr .= &LinkP( "b=$BOARD&c=ct&rfid=$Id&roid=" . $DB_FID{$Id} . $AddNum,
	$H_RELINKFROM_MARK, '', $H_RELINKFROM_MARK_L ) . "\n";
    if ($DB_FID{$Id} eq '')
    {
	$gHgStr .= &LinkP( "b=$BOARD&c=mvt&rfid=$Id&roid=" . $DB_FID{$Id} .
	    $AddNum, $H_REORDERFROM_MARK, '', $H_REORDERFROM_MARK_L ) . "\n";
    }

    # ������ޥ��
    $gHgStr .= &LinkP( "b=$BOARD&c=dp&id=$Id", $H_DELETE_ICON, '',
	$H_DELETE_ICON_L ) . "\n";
    $gHgStr .= &LinkP( "b=$BOARD&c=f&s=on&id=$Id", $H_SUPERSEDE_ICON, '',
	$H_SUPERSEDE_ICON_L ) . "\n";

    # ��ư���ޥ��(To)
    if (( $ComType == 4 ) && ( $FromId ne $Id ) && ( $DB_FID{$Id} eq '' ) &&
	( $FromId ne $Id ))
    {
	$gHgStr .= &LinkP( "b=$BOARD&c=mve&rtid=$Id&rfid=$FromId&roid=" .
	    $cgi'TAGS{'roid'} . $AddNum, $H_REORDERTO_MARK, '',
	    $H_REORDERTO_MARK_L ) . "\n";
    }

    # ������ѹ����ޥ��(To)
    if (( $ComType == 2 ) && ( $FromId ne $Id ) && ( !grep( /^$FromId$/,
	split( /,/, $DB_AIDS{$Id} ))) && ( !grep( /^$FromId$/, split( /,/,
	$DB_FID{$Id} ))))
    {
	$gHgStr .= &LinkP( "b=$BOARD&c=ce&rtid=$Id&rfid=$FromId&roid=" .
	    $cgi'TAGS{'roid'} . $AddNum, $H_RELINKTO_MARK, '',
	    $H_RELINKTO_MARK_L ) . "\n";
    }

    $gADDFLAG{$Id} = 1;		# �����Ѥ�

    # ̼�����Сġ�
    if ($DB_AIDS{$Id})
    {
	$gHgStr .= "<ul>\n";
	grep( &ThreadTitleNodeMaint( $_, $ComType, $AddNum, $flag ),
	     split( /,/, $DB_AIDS{$Id} ));
	$gHgStr .= "</ul>\n";
    }

    $gHgStr .= "</li>\n";
}


###
## ���ս祿���ȥ����
#
sub UISortTitle
{
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
    $gFold = $cgi'TAGS{'fold'} || 0;
    $gVRev = $Rev? 1-$SYS_BOTTOMTITLE : $SYS_BOTTOMTITLE;
    $gTo = $#DB_ID - $Old;
    $gFrom = $gTo - $Num + 1;
    $gFrom = 0 if (( $gFrom < 0 ) || ( $Num == 0 ));

    $gPageLinkStr = &PageLink( 'r', $Num, $Old, $Rev, '' );

    &htmlGen( 'SortTitle.html' );
}

sub hgSortTitleTree
{
    &Fatal( 18, "$_[0]/SortTitleTree" ) if ( $_[0] ne 'SortTitle.html' );

    $gHgStr .= "<ul>\n";

    # ������ɽ��
    local( $IdNum, $Id );
    if ( $#DB_ID == -1 )
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
		$Id = $DB_ID[$IdNum];
		&DumpArtSummaryItem( $Id, $DB_AIDS{$Id}, $DB_ICON{$Id},
		    $DB_TITLE{$Id}, $DB_NAME{$Id}, $DB_DATE{$Id}, 1 );
		$gHgStr .= "</li>\n";
	    }
	}
	else
	{
	    for ($IdNum = $gTo; $IdNum >= $gFrom; $IdNum--)
	    {
		$Id = $DB_ID[$IdNum];
		&DumpArtSummaryItem( $Id, $DB_AIDS{$Id}, $DB_ICON{$Id},
		    $DB_TITLE{$Id}, $DB_NAME{$Id}, $DB_DATE{$Id}, 1 );
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
    &LockBoard();
    &DbCache( $BOARD ) if $BOARD;
    &UnlockBoard();

    local( $id ) = $cgi'TAGS{'id'};

    # �ե����������ڹ�¤�μ���
    # ex. '( a ( b ( c d ) ) ( e ) ( f ( g ) ) )'�Ȥ����ꥹ��
    @gFollowIdTree = ();
    &GetFollowIdTree( $id, *gFollowIdTree );

    &htmlGen( 'ShowThread.html' );
}

sub hgShowThreadTitle
{
    &Fatal( 18, "$_[0]/ShowThreadTitle" ) if ( $_[0] ne 'ShowThread.html' );

    local( $tmp, $subject );
    ( $tmp, $tmp, $tmp, $subject ) = &GetTreeTopArticlesInfo( *gFollowIdTree );
    $gHgStr .= $subject;
}

sub hgShowThreadTitleTree
{
    if ( $_[0] ne 'ShowThread.html' )
    {
	&Fatal( 18, "$_[0]/ShowThreadTitleTree" );
    }

    &DumpArtThread( 7, @gFollowIdTree );
}

sub hgShowThreadMsgBody
{
    if ( $_[0] ne 'ShowThread.html' )
    {
	&Fatal( 18, "$_[0]/ShowThreadMsgBody" );
    }

    &DumpArtThread( 2, @gFollowIdTree );
}

sub hgShowThreadBackToTitleButton
{
    if ( $_[0] ne 'ShowThread.html' )
    {
	&Fatal( 18, "$_[0]/ShowThreadBackToTitleButton" );
    }

    &DumpButtonToTitleList( $BOARD, $cgi'TAGS{'id'} );
}


###
## ���ս��å���������
#
sub UISortArticle
{
    &LockBoard();
    &DbCache( $BOARD ) if $BOARD;
    &UnlockBoard();

    $gNum = $cgi'TAGS{'num'};
    $gOld = $cgi'TAGS{'old'};
    $gRev = $cgi'TAGS{'rev'};
    $gFold = $cgi'TAGS{'fold'} || 0;

    $gPageLinkStr = &PageLink( 'l', $gNum, $gOld, $gRev, '' );

    &htmlGen( 'SortArticle.html' );
}

sub hgSortArticleBody
{
    &Fatal( 18, "$_[0]/SortArticleBody" ) if ( $_[0] ne 'SortArticle.html' );

    local( $vRev ) = $gRev? 1-$SYS_BOTTOMARTICLE : $SYS_BOTTOMARTICLE;
    local( $To ) = $#DB_ID - $gOld;
    local( $From ) = $To - $gNum + 1; $From = 0 if (( $From < 0 ) ||
	( $gNum == 0 ));

    $gHgStr .= $HTML_HR;

    if (! $#DB_ID == -1)
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
		$Id = $DB_ID[$IdNum];
		&DumpArtBody( $Id, $SYS_COMMAND_EACH, 1 );
		$gHgStr .= $HTML_HR;
	    }
	}
	else
	{
	    for ( $IdNum = $To; $IdNum >= $From; $IdNum-- )
	    {
		$Id = $DB_ID[$IdNum];
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
    &LockBoard();
    &DbCache( $BOARD ) if $BOARD;
    &UnlockBoard();

    local( $tmp );
    ( $tmp, $gAids, $tmp, $gSubject ) = &GetArticlesInfo( $cgi'TAGS{'id'} );

    # ̤��Ƶ������ɤ�ʤ�
    &Fatal( 8, '' ) if ( $gSubject eq '' );

    &htmlGen( 'ShowArticle.html' );
}

sub hgShowArticleTitle
{
    &Fatal( 18, "$_[0]/ShowArticleTitle" ) if ( $_[0] ne 'ShowArticle.html' );

    $gHgStr .= $gSubject;
}

sub hgShowArticleBody
{
    &Fatal( 18, "$_[0]/ShowArticleBody" ) if ( $_[0] ne 'ShowArticle.html' );

    &DumpArtBody( $cgi'TAGS{'id'}, 1, 1 );
}

sub hgShowArticleReply
{
    &Fatal( 18, "$_[0]/ShowArticleReply" ) if ( $_[0] ne 'ShowArticle.html' );

    &DumpReplyArticles( split( /,/, $gAids ));
}


###
## �����θ���(ɽ�����̤κ���)
#
sub UISearchArticle
{
    &htmlGen( 'SearchArticle.html' );
}

sub hgSearchArticleResult
{
    if ( $_[0] ne 'SearchArticle.html' )
    {
	&Fatal( 18, "$_[0]/SearchArticleResult" );
    }

    &LockBoard();
    &DbCache( $BOARD ) if $BOARD;
    &UnlockBoard();

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
    if ( !( $POLICY & 8 ) && ( $SYS_OVERWRITE == 0 ))
    {
	&Fatal( 99, $cgi'TAGS{'c'} );
    }

    &LockBoard();
    &DbCache( $BOARD ) if $BOARD;
    &UnlockBoard();

    $gId = $cgi'TAGS{'id'};
    local( $tmp, $subject );
    ( $tmp, $gAids, $tmp, $subject ) = &GetArticlesInfo( $gId );

    # ̤��Ƶ������ɤ�ʤ�
    &Fatal( 8, '' ) if ( $subject eq '' );

    &htmlGen( 'DeletePreview.html' );
}

sub hgDeletePreviewForm
{
    if ( $_[0] ne 'DeletePreview.html' )
    {
	&Fatal( 18, "$_[0]/DeletePreviewForm" );
    }

    local( %tags );
    %tags = ( 'c', 'de', 'b', $BOARD, 'id', $gId );
    &DumpForm( *tags, '���Υ�å������������ޤ�', '', '' );

    if ( $gAids )
    {
	%tags = ( 'c', 'det', 'b', $BOARD, 'id', $gId );
	&DumpForm( *tags, "$H_REPLY��å�������ޤȤ�ƺ�����ޤ�", '', '' );
    }
}

sub hgDeletePreviewBody
{
    if ( $_[0] ne 'DeletePreview.html' )
    {
	&Fatal( 18, "$_[0]/DeletePreviewBody" );
    }

    &DumpArtBody( $gId, 0, 1 );
}

sub hgDeletePreviewReply
{
    if ( $_[0] ne 'DeletePreview.html' )
    {
	&Fatal( 18, "$_[0]/DeletePreviewReply" );
    }

    &DumpReplyArticles( split( /,/, $gAids ));
}


###
## �����κ��
#
sub UIDeleteExec
{
    if ( !( $POLICY & 8 ) && ( $SYS_OVERWRITE == 0 ))
    {
	&Fatal( 99, $cgi'TAGS{'c'} );
    }

    local( $threadFlag ) = @_;

    &LockBoard();
    &DbCache( $BOARD ) if $BOARD;

    $gId = $cgi'TAGS{'id'};

    local( $tmp, $aids, $name );
    ( $tmp, $aids, $tmp, $tmp, $tmp, $tmp, $name ) = &GetArticlesInfo( $gId );
    &Fatal( 44, '' ) if ( !&IsUser( $name ) && !( $POLICY & 8 ));
    &Fatal( 19, '' ) if ( $aids && ( $SYS_OVERWRITE == 1 ));

    # ����¹�
    &DeleteArticle( $gId, $BOARD, $threadFlag );

    &UnlockBoard();

    &htmlGen( 'DeleteExec.html' );
}

sub hgDeleteExecBackToTitleButton
{
    if ( $_[0] ne 'DeleteExec.html' )
    {
	&Fatal( 18, "$_[0]/DeleteExecBackToTitleButton" );
    }

    &DumpButtonToTitleList( $BOARD, $gId );
}


###
## ��������ɽ��
#
sub UIShowIcon
{
    &htmlGen( 'ShowIcon.html' );
}


###
## �إ��ɽ��
#
sub UIHelp
{
    &htmlGen( 'Help.html' );
}


###
## ���顼ɽ��
#
sub UIFatal
{
    ( $gMsg ) = @_;
    &htmlGen( 'Fatal.html' );
}

sub hgFatalMsg
{
    $gHgStr .= $gMsg;
}


###
## ����hg�ؿ���
#
sub hgsTitle
{
    $gHgStr .=<<EOS;
<meta http-equiv="Content-Type" content="text/html; charset=EUC-JP">
<meta http-equiv="Content-Style-Type" content="text/css">
<base href="$BASE_URL">
<link rev="MADE" href="mailto:$MAINT">
EOS
    if ( $BOARD && ( -s &GetPath( $BOARD, $CSS_FILE )))
    {
	$gHgStr .= qq(<link rel="StyleSheet" href="$BOARD/$CSS_FILE" type="text/css" media="screen">);
    }
    else
    {
	$gHgStr .= qq(<link rel="StyleSheet" href="$CSS_FILE" type="text/css" media="screen">);
    }
}

sub hgsAddress
{
    $gHgStr .= "<address>\nMaintenance: " .
	&TagA( $MAINT_NAME, "mailto:$MAINT" ) . $HTML_BR .
	&TagA( $PROGNAME, "http://www.jin.gr.jp/~nahi/kb/" ) .
	": Copyright (C) 1995-99 " .
	&TagA( "NAKAMURA, Hiroshi", "http://www.jin.gr.jp/~nahi/" ) .
	".\n</address>\n";
}

sub hgcStatus
{
    $gHgStr .= qq(<p class="kbStatus">[);
    if ( $UNAME && ( $UNAME ne $GUEST ) && ( $UNAME ne
	$cgiauth'F_COOKIE_RESET ))
    {
	$gHgStr .= "$H_USER: $UNAME -- \n";
    }
    $gHgStr .= "$H_BOARD: $BOARDNAME -- \n" if ( $BOARDNAME ne '' );
    $gHgStr .= "�ǿ�${H_MESG}ID: " . $DB_ID[$#DB_ID] . " // \n" if @DB_ID;
    $gHgStr .= "����: " . &GetDateTimeFormatFromUtc( $^T );
    $gHgStr .= "]</p>\n";
}

sub hgcTopMenu
{
    $gHgStr .= qq(<div class="kbTopMenu">\n);
    local( $select, $contents );
    $select = &TagLabel( "ɽ������", 'c', 'W' ) . ": \n";

    if ( $BOARD )
    {
	$contents .= sprintf( qq[<option%s value="v">�ǿ�$H_SUBJECT����(����å�)\n], ( $cgi'TAGS{'c'} eq 'v' )? ' selected' : '' );
	$contents .= sprintf( qq[<option%s value="r">�ǿ�$H_SUBJECT����(���ս�)\n], ( $cgi'TAGS{'c'} eq 'r' )? ' selected' : '' );
	$contents .= sprintf( qq[<option%s value="vt">�ǿ�$H_MESG����(����å�)\n], ( $cgi'TAGS{'c'} eq 'vt' )? ' selected' : '' );
	$contents .= sprintf( qq[<option%s value="l">�ǿ�$H_MESG����(���ս�)\n], ( $cgi'TAGS{'c'} eq 'l' )? ' selected' : '' );
	$contents .= sprintf( qq(<option%s value="s">$H_MESG�θ���\n), ( $cgi'TAGS{'c'} eq 's' )? ' selected' : '' ) if $SYS_F_S;
	$contents .= sprintf( qq(<option%s value="n">$H_POSTNEWARTICLE\n), ( $cgi'TAGS{'c'} eq 'n' )? ' selected' : '' ) if (( $POLICY & 2 ) && ( !$SYS_NEWART_ADMINONLY || ( $POLICY & 8 )));
	$contents .= sprintf( qq(<option%s value="i">�Ȥ���$H_ICON����\n), ( $cgi'TAGS{'c'} eq 'i' )? ' selected' : '' ) if $SYS_ICON;
    }

    $contents .= sprintf( qq(<option%s value="bl">$H_BOARD����\n),
	( $cgi'TAGS{'c'} eq 'bl' )? ' selected' : '' );
    $contents .= sprintf( qq(<option%s value="lo">$H_USER����θƤӽФ�\n),
	( $cgi'TAGS{'c'} eq 'lo' )? ' selected' : '' ) if $SYS_AUTH;

    $select .= &TagSelect( 'c', $contents ) . "\n // " .
	&TagLabel( "ɽ�����", 'num', 'Y' ) . ': ' .
	&TagInputText( 'text', 'num', ( $cgi'TAGS{'num'} || $DEF_TITLE_NUM ),
	3 );
    local( %tags ) = ( 'b', $BOARD );
    &DumpForm( *tags, 'ɽ��(V)', '', *select );
    $gHgStr .= "</div>\n";
}

sub hgcHelp
{
    local( $var ) = $_[1];
    $gHgStr .= &LinkP( "b=$BOARD&c=h", &TagComImg( $ICON_HELP, '�إ��' ), 'H',
	'', '', $var );
}

sub hgcSiteName
{
    $gHgStr .= $SYSTEM_NAME;
}

sub hgcFuncLink
{
    return unless $SYS_AUTH;

    $gHgStr .= "<dl>\n";

    $gHgStr .= "<dt>�ֿ�����$H_USER����򥵡��Ф˵����������</dt>\n";
    $gHgStr .= '<dd>��' . &LinkP( 'c=ue', "$H_USER����ο�����Ͽ" .
	&TagAccessKey( 'E' ), 'E' ) . "</dd>\n";

    if ( $UNAME )
    {
	$gHgStr .= "<dt>���̤�$H_USER�����ƤӽФ��סʸ����������$H_USER����ϡ�$UNAME�Τ�ΤǤ���</dt>\n";
	$gHgStr .= '<dd>��' . &LinkP( 'c=lo', "$H_USER����θƤӽФ�" .
	    &TagAccessKey( 'L' ), 'L' ) . "</dd>\n";
    }

    if ( $POLICY & 4 )
    {
	$gHgStr .= "<dt>��$UNAME�ˤĤ�����Ͽ����$H_USER������ѹ������</dt>\n";
	$gHgStr .= '<dd>��' . &LinkP( 'c=uc', "$H_USER������ѹ�" .
	    &TagAccessKey( 'C' ), 'C' ) . "</dd>\n";
    }

    if ( $POLICY & 8 )
    {
	$gHgStr .= "<dt>�ֿ�����$H_BOARD���ꤿ����</dt>\n";
	$gHgStr .= '<dd>��' . &LinkP( 'c=be', "$H_BOARD�ο�������" .
	    &TagAccessKey( 'A' ), 'A' ) . "</dd>\n";
    }

    $gHgStr .= "</dl>\n";
}

sub hgcPageLink
{
    $gHgStr .= $gPageLinkStr;
}

sub hgcBoardLinkAll
{
    # ���Ǽ��Ĥξ������Ф�
    local( @board, %boardName, %boardInfo );
    &GetAllBoardInfo( *board, *boardName, *boardInfo );

    $gHgStr .= "<ul>\n";

    local( $newIcon, $modTimeUtc, $modTime, $nofArticle );
    foreach ( @board )
    {
	$modTimeUtc = &GetModifiedTime( $DB_FILE_NAME, $_ );
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

	$gHgStr .= '<li>' .
	    &LinkP( "b=$_&c=v&num=$DEF_TITLE_NUM", $boardName{$_} ) .
	    "$newIcon\n[�ǿ�: $modTime, ������: $nofArticle]\n";
	if ( $POLICY & 8 )
	{
	    $gHgStr .= &LinkP( "b=$_&c=bc", "�������ѹ�" ) . "\n";
	}

	$gHgStr .= $HTML_BR . $HTML_BR . "</li>\n";
    }
    $gHgStr .= "</ul>\n";
}

sub hgcBoardLink
{
    local( $var ) = $_[1];
    local( $com, $board ) = split( ':', $var );
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

    $modTimeUtc = &GetModifiedTime( $DB_FILE_NAME, $board );
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

    $gHgStr .= &LinkP( "b=$board&c=$com&num=$num", $gBoardName{$board} ) . "$newIcon\n[�ǿ�: $modTime, ������: $nofArticle]\n";
    if ( $POLICY & 8 )
    {
	$gHgStr .= &LinkP( "b=$board&c=bc", "�������ѹ�" ) . "\n";
    }
}

sub hgbBoardName
{
    $gHgStr .= $BOARDNAME if $BOARD;
}

sub hgbBoardHeader
{
    &DumpBoardHeader() if $BOARD;
}

sub hgbPostEntryForm
{
    if ( $POLICY & 2 )
    {
	&DumpArtEntry( $gDefIcon, $gEntryType, $gId, $gDefSubject,
	    $gDefTextType, $gDefArticle, $gDefName, $gDefEmail, $gDefUrl,
	    $gDefFmail );
    }
}

sub hgbSearchArticleForm
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

    local( $msg );
    $msg .= &TagInputCheck( 'searchsubject', $SearchSubject ) . ': ' . &TagLabel( $H_SUBJECT, 'searchsubject', 'T' ) . $HTML_BR;

    $msg .= &TagInputCheck( 'searchperson', $SearchPerson ) . ': ' . &TagLabel( "̾��", 'searchperson', 'N' ) . $HTML_BR;

    $msg .= &TagInputCheck( 'searcharticle', $SearchArticle ) . ': ' . &TagLabel( $H_MESG, 'searcharticle', 'A' ) . $HTML_BR;

    local( $sec, $min, $hour, $mday, $mon, $year, $nowStr );
    if ( !$SearchPostTime )
    {
	( $sec, $min, $hour, $mday, $mon, $year, $nowStr ) = localtime( $^T );
	$nowStr = sprintf( "%04d/%02d/%02d", $year+1900, $mon+1, $mday );
    }
    $msg .= &TagInputCheck( 'searchposttime', $SearchPostTime ) . ': ' . &TagLabel( $H_DATE, 'searchposttime', 'D' ) . " // \n";
    $msg .= &TagInputText( 'text', 'searchposttimefrom', ( $SearchPostTimeFrom || '' ), 11 ) . ' ' . &TagLabel( '��', 'searchposttimefrom', 'S' ) . " \n";
    $msg .= &TagInputText( 'text', 'searchposttimeto', ( $Searchposttimeto || '' ), 11 ) . &TagLabel( '�δ�', 'searchposttimeto', 'E' ) . $HTML_BR;

    if ( $SYS_ICON )
    {
	$msg .= &TagInputCheck( 'searchicon', $SearchIcon ) . ': ' . &TagLabel( $H_ICON, 'searchicon', 'I' ) . " // \n";

	# �������������
	&CacheIconDb( $BOARD );

	local( $contents, $IconTitle );
	$contents = sprintf( qq(<option%s>$H_NOICON\n), ( $Icon &&
	    ( $Icon ne $H_NOICON ))? '' : ' selected' );
	foreach $IconTitle ( sort keys( %ICON_FILE ))
	{
	    $contents .= sprintf( "<option%s>$IconTitle\n",
	    	( $Icon eq $IconTitle )? ' selected' : '' );
	}
	$msg .= &TagSelect( 'icon', $contents ) . "\n";

	# �����������
	$msg .= '(' . &LinkP( "b=$BOARD&c=i", "�Ȥ���$H_ICON����" .
	    &TagAccessKey( 'H' ), 'H' ) . ')\n' . $HTML_BR . $HTML_BR;
    }

    $msg .= &TagLabel( '�������', 'key', 'K' ) . ': ' . &TagInputText(
	'text', 'key', $Key, $KEYWORD_LENGTH ) . $HTML_BR;
    %tags = ( 'c', 's', 'b', $BOARD );
    &DumpForm( *tags, '����', '�ꥻ�å�', *msg );
}

sub hgbAllIcon
{
    return unless $BOARD;
    &CacheIconDb( $BOARD );
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
    &GetBoardHeader( $BOARD, *msg );
    $gHgStr .= $msg;
}


###
## DumpArtEntry - ��å��������ϥե������ɽ��
#
# - SYNOPSIS
#	DumpArtEntry( $icon, $type, $id, $title, $texttype, $article, $name, $eMail, $url, $fMail );
#
# - ARGS
#	$icon		��������
#	$type		��å�����������( 'supersede', and so )
#	$id		��ץ饤/��������å�����ID
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

    &CacheIconDb( $BOARD );
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
    local( $icon, $type, $id, $title, $texttype, $article, $name, $eMail, $url, $fMail ) = @_;

    local( $msg );

    # �������������
    if ( $SYS_ICON )
    {
	&CacheIconDb( $BOARD );
	$msg .= &TagLabel( $H_ICON, 'icon', 'I' ) . " :\n";
	local( $contents );
	$contents = sprintf( "<option%s>$H_NOICON\n", (( $icon eq '' )?
	    ' selected' : '' ));
	foreach ( @ICON_TITLE )
	{
	    $contents .= sprintf( "<option%s>$_\n", ( $_ eq $icon )?
		' selected' : '' );
	}
	$msg .= &TagSelect( 'icon', $contents ) . "\n";

	$msg .= '(' . &LinkP( "b=$BOARD&c=i", "�Ȥ���$H_ICON����" .
	    &TagAccessKey( 'H' ), 'H' ) . ')' . $HTML_BR;
    }

    $msg .= &TagLabel( $H_SUBJECT, 'subject', 'T' ) . ': ' . &TagInputText(
	'text', 'subject', $title, $SUBJECT_LENGTH ) . $HTML_BR;
    
    local( $ttFlag ) = 0;
    local( $ttBit ) = 0;
    
    foreach ( @H_TTLABEL )
    {
	if (( $SYS_TEXTTYPE & ( 2 ** $ttBit )) &&
	    ( $SYS_TEXTTYPE ^ ( 2 ** $ttBit )))
	{
	    $ttFlag = 1;	# ��ǻȤ��������ʤ�������
	}
	$ttBit++;
    }

    # �񤭹��߷���
    if ( $ttFlag )
    {
	$ttFlag = 0 if $texttype;
	$msg .= &TagLabel( $H_TEXTTYPE, 'texttype', 'Z' ) . ":\n";
	local( $contents );
	$ttBit = 0;
	foreach ( @H_TTLABEL )
	{
	    if ( $SYS_TEXTTYPE & ( 2 ** $ttBit ))
	    {
		if ( $ttFlag )
		{
		    $ttFlag = 0;	# now, using for a flag for the first.
		    $contents .= "<option selected>" . $H_TTLABEL[$ttBit] .
			"\n";
		}
		else
		{
		    $contents .= sprintf( "<option%s>" . $H_TTLABEL[$ttBit] .
			"\n", ( $H_TTLABEL[$ttBit] eq $texttype )?
			' selected' : '' );
		}
	    }
	    $ttBit++;
	}
	$msg .= &TagSelect( 'texttype', $contents ) . $HTML_BR;
    }
    else
    {
	$msg .= sprintf( qq(<input name="texttype" type="hidden" value="%s">),
	    $H_TTLABEL[(( log $SYS_TEXTTYPE ) / ( log 2 ))] ) . $HTML_BR;
    }

    $msg .= &TagLabel( $H_MESG, 'article', 'A' ) . ':' . $HTML_BR .
	&TagTextarea( 'article', $article, $TEXT_ROWS, $TEXT_COLS ) . $HTML_BR;

    if ( $POLICY & 4 )
    {
	# ��Ͽ�Ѥߤξ�硤̾�����ᥤ�롤URL�����Ϥϡ�̵����
    }
    else
    {
	$msg .= &TagLabel( $H_FROM, 'name', 'N' ) . ': ' . &TagInputText(
	    'text', 'name', $name, $NAME_LENGTH ) . $HTML_BR;
	$msg .= &TagLabel( $H_MAIL, 'mail', 'M' ) . ': ' . &TagInputText(
	    'text', 'mail', $eMail, $MAIL_LENGTH ) . $HTML_BR;
	$msg .= &TagLabel( $H_URL, 'url', 'U' ) . ': ' . &TagInputText( 'text',
	    'url', ( $url || 'http://' ), $URL_LENGTH ) . $HTML_BR;
    }

    if ( $SYS_MAIL & 2 )
    {
	$msg .= &TagLabel( '��ץ饤�����ä����˥ᥤ���Ϣ��', 'fmail', 'F' ) .
	    ': ' . &TagInputCheck( 'fmail', $fMail ) . "\n";
    }
    $msg .= "</p>\n<p>\n";

    $msg .= &TagInputRadio( 'com_p', 'com', 'p', 1 ) . ":\n" . &TagLabel(
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
    $msg .= &TagInputRadio( 'com_x', 'com', 'x', 0 ) . ":\n" . &TagLabel(
	$doLabel, 'com_x', 'X' ) . $HTML_BR;

    local( $op ) = ( -M &GetPath( $BOARD, $DB_FILE_NAME ));
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
	( $fid, $aids, $date, $title, $icon, $host, $name, $eMail, $url ) = &GetArticlesInfo( $id );
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

    if ( $commandFlag && $SYS_COMMAND )
    {
	local( $num );
	foreach ( 0 .. $#DB_ID ) { $num = $_, last if ( $DB_ID[$_] eq $id ); }
	local( $prevId ) = $DB_ID[$num - 1] if ( $num > 0 );
	local( $nextId ) = $DB_ID[$num + 1];
	&DumpArtCommand( $id, $prevId, $nextId, ( $aids ne '' ), ( &IsUser(
	    $name ) && (( $aids eq '' ) || ( $SYS_OVERWRITE == 2 ))));
    }

    local( @origIdList );
    if ( $origFlag && ( $fid ne '' ))
    {
	@origIdList = split( /,/, $fid );
    }

    # �إå��ʥ桼������ȥ�ץ饤��: �����ȥ�Ͻ�����
    &DumpArtHeader( $name, $eMail, $url, $host, $date, @origIdList );

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
	    local( $dFid, $dAids, $dDate, $dSubject, $dIcon, $dRemoteHost,
		$dName ) = &GetArticlesInfo( $Head );
	    &DumpArtSummaryItem( $Head, $dAids, $dIcon, $dSubject, $dName,
		$dDate, $State&3 );
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
#	DumpSearchResult( $Key, $Subject, $Person, $Article, $PostTime, $PostTimeFrom, $PostTimeTo, $Icon, $IconType );
#
# - ARGS
#	$Key		�������
#	$Subject	�����ȥ�򸡺����뤫�ݤ�
#	$Person		��ƼԤ򸡺����뤫�ݤ�
#	$Article	��ʸ�򸡺����뤫�ݤ�
#	$PostTime	���դ򸡺����뤫�ݤ�
#	$PostTimeFrom	��������
#	$PostTimeTo	��λ����
#	$Icon		��������򸡺����뤫�ݤ�
#	$IconType	��������
#
# - DESCRIPTION
#	�����򸡺�����ɽ������
#
sub DumpSearchResult
{
    local( $Key, $Subject, $Person, $Article, $PostTime, $PostTimeFrom,
	$PostTimeTo, $Icon, $IconType ) = @_;

    local( @KeyList ) = split(/\s+/, $Key);

    # �ꥹ�ȳ���
    $gHgStr .= "<ul>\n";

    local( $dId, $dAids, $dDate, $dTitle, $dIcon, $dName, $dEmail );
    local( $SubjectFlag, $PersonFlag, $PostTimeFlag, $ArticleFlag );
    local( $HitNum, $Line, $FromUtc, $ToUtc );
    foreach ($[ .. $#DB_ID)
    {
	# ��������
	$dId = $DB_ID[$_];
	$dIcon = $DB_ICON{$dId};
	$dTitle = $DB_TITLE{$dId};
	$dName = $DB_NAME{$dId};
	$dEmail = $DB_EMAIL{$dId};
	$dAids = $DB_AIDS{$dId};
	$dDate = $DB_DATE{$dId};

	# �ѿ��Υꥻ�å�
	$SubjectFlag = $PersonFlag = $PostTimeFlag = $ArticleFlag = 0;
	$Line = '';

	# ������������å�
	next if ( $Icon && ( $dIcon ne $IconType ));

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
	    &DumpArtSummaryItem( $dId, $dAids, $dIcon, $dTitle, $dName, $dDate,
		1 );

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
	$gHgStr .= "</ul>\n<ul>";
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
## DumpReplyArticles - ��ץ饤�����ؤΥ�󥯤�ɽ��
#
# - SYNOPSIS
#	DumpReplyArticles( @_ );
#
# - ARGS
#	@_	��ץ饤����ID�Υꥹ��
#
# - DESCRIPTION
#	��ץ饤�����ؤΥ�󥯤�ɽ�����롥
#
sub DumpReplyArticles
{
    $gHgStr .= "$H_LINE\n<p>\n��$H_REPLY\n";

    if ( @_ )
    {
	# ȿ������������ʤ��
	local( $id, @tree );
	foreach $id ( @_ )
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

    $gHgStr .= "</p>\n";
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
#	DumpArtCommand( $id, $prevId, $nextId, $reply, $delete );
#
# - ARGS
#	$id	����ID
#	$prevId	������ID
#	$nextId	������ID
#	$reply	��ץ饤���������뤫
#	$delete	�������������ǽ��
#
sub DumpArtCommand
{
    local( $id, $prevId, $nextId, $reply, $delete ) = @_;

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

    local( $old ) = &GetTitleOldIndex( $id );

    $gHgStr .= &LinkP( 'c=bl', &TagComImg( $ICON_BLIST, $H_BACKBOARD ), 'B' ) .
	"\n";

    $gHgStr .= $dlmtS . &LinkP( "b=$BOARD&c=v&num=$DEF_TITLE_NUM&old=$old",
	&TagComImg( $ICON_TLIST, $H_BACKTITLEREPLY ), 'T' ) . "\n";
	
    if ( $prevId ne '' )
    {
	$gHgStr .= $dlmtS . &LinkP( "b=$BOARD&c=e&id=$prevId", &TagComImg(
	    $ICON_PREV, $H_PREVARTICLE ), 'P' ) . "\n";
    }
    else
    {
	$gHgStr .= $dlmtS . &TagComImg( $ICON_PREV, $H_PREVARTICLE, ) . "\n";
    }
	
    if ( $nextId ne '' )
    {
	$gHgStr .= $dlmtS . &LinkP( "b=$BOARD&c=e&id=$nextId", &TagComImg(
	    $ICON_NEXT, $H_NEXTARTICLE ), 'N' ) . "\n";
    }
    else
    {
	$gHgStr .= $dlmtS . &TagComImg( $ICON_NEXT, $H_NEXTARTICLE, ) . "\n";
    }

    if ( $reply )
    {
	$gHgStr .= $dlmtS . &LinkP( "b=$BOARD&c=t&id=$id", &TagComImg(
	    $ICON_THREAD, $H_READREPLYALL ), 'M' ) . "\n";
    }
    else
    {
	$gHgStr .= $dlmtS . &TagComImg( $ICON_THREAD, $H_READREPLYALL ) . "\n";
    }

    $gHgStr .= $dlmtL;

    if ( $POLICY & 2 )
    {
	$gHgStr .= $dlmtS . &LinkP( "b=$BOARD&c=f&id=$id", &TagComImg(
	    $ICON_FOLLOW, $H_REPLYTHISARTICLE ), 'R' ) . "\n" . $dlmtS .
	    &LinkP( "b=$BOARD&c=q&id=$id", &TagComImg( $ICON_QUOTE,
	    $H_REPLYTHISARTICLEQUOTE ), 'Q' ) . "\n";
    }
    else
    {
	$gHgStr .= $dlmtS . &TagComImg( $ICON_FOLLOW, $H_REPLYTHISARTICLE ) .
	    "\n" . $dlmtS . &TagComImg( $ICON_QUOTE,
	    $H_REPLYTHISARTICLEQUOTE ) . "\n";
    }

    if ( $SYS_AUTH )
    {
	$gHgStr .= $dlmtL;

	if ( $delete )
	{
	    $gHgStr .= $dlmtS . &LinkP( "b=$BOARD&c=f&s=on&id=$id", &TagComImg(
		$ICON_SUPERSEDE, $H_SUPERSEDE ), 'S' ) . "\n" . $dlmtS .
		&LinkP( "b=$BOARD&c=dp&id=$id", &TagComImg( $ICON_DELETE,
	    	$H_DELETE ), 'D' ) . "\n";
	}
	else
	{
	    $gHgStr .= $dlmtS . &TagComImg( $ICON_SUPERSEDE, $H_SUPERSEDE ) .
	    	"\n" . $dlmtS . &TagComImg( $ICON_DELETE, $H_DELETE ) . "\n";
	}
    }

    if ( $SYS_COMICON == 1 )
    {
	$gHgStr .= $dlmtL;
	$gHgStr .= $dlmtS . &LinkP( "b=$BOARD&c=h", &TagComImg( $ICON_HELP,
	    '�إ��' ), 'H', '', '', 'list' ) . "\n";
    }
    $gHgStr .= qq(</p>\n);
}


###
## DumpArtHeader - �����إå��ʥ����ȥ�����ˤ�ɽ��
#
# - SYNOPSIS
#	DumpArtHeader( $name, $eMail, $url, $host, $date, @origIdList );
#
# - ARGS
#	$name		�桼��̾
#	$eMail		�ᥤ�륢�ɥ쥹
#	$url		URL
#	$host		Remote Host̾
#	$date		���ա�UTC��
#	@origIdList	��ץ饤������ID
#
sub DumpArtHeader
{
    local( $name, $eMail, $url, $host, $date, @origIdList ) = @_;

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
    if ( @origIdList )
    {
	# ���ꥸ�ʥ뵭��
	local( $dId, $dFid, $dAids, $dDate, $dTitle, $dIcon, $dHost, $dName );
	if ( $#origIdList > 0 )
	{
	    $dId = $origIdList[$#origIdList];
	    ( $dFid, $dAids, $dDate, $dTitle, $dIcon, $dHost, $dName ) =
		&GetArticlesInfo( $dId );
	    $gHgStr .= "<strong>$H_ORIG_TOP:</strong> ";
	    &DumpArtSummary( $dId, $dAids, $dIcon, $dTitle, $dName, $dDate,
		0 );
	    $gHgStr .= $HTML_BR;
	}

	# ������
	$dId = $origIdList[0];
	( $dFid, $dAids, $dDate, $dTitle, $dIcon, $dHost, $dName ) =
	    &GetArticlesInfo( $dId );
	$gHgStr .= "<strong>$H_ORIG:</strong> ";
	&DumpArtSummary( $dId, $dAids, $dIcon, $dTitle, $dName, $dDate, 0 );
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
	$gHgStr .= "<p>" . &LinkP( "b=$board&c=v&num=$DEF_TITLE_NUM&old=$old",
	    $H_BACKTITLEREPLY . &TagAccessKey( 'B' ), 'B' ) . "</p>\n";
	$gHgStr .= "<p>" . &LinkP( "b=$board&c=r&num=$DEF_TITLE_NUM&old=$old",
	    $H_BACKTITLEDATE ) . "</p>\n";
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
	$gHgStr .= "<p>" . &LinkP( "b=$board&c=e&id=$id", $msg .
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
	$gHgStr .= qq(<input name="$_" type="hidden" value="$tags{$_}">\n);
    }
    if ( !$noAuth && ( $SYS_AUTH == 3 ))
    {
	$gHgStr .= qq(<input name="kinoU" type="hidden" value="$UNAME">\n);
	$gHgStr .= qq(<input name="kinoP" type="hidden" value="$PASSWD">\n);
	$gHgStr .= qq(<input name="kinoA" type="hidden" value="3">\n);
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
#	DumpArtSummary( $id, $aids, $icon, $title, $name, $origDate, $flag);
#
# - ARGS
#	$id		����ID
#	$aids		��ץ饤���������뤫�ݤ�
#	$icon		������������ID
#	$title		������Subject
#	$name		��������Ƽ�̾
#	$origDate	�������������(UTC)
#	$flag		ɽ���������ޥ����ե饰
#	    2^0 ... ����åɤ���Ƭ�Ǥ��뤫�ʢ����դ���
#	    2^1 ... Ʊ��ڡ���fragment��󥯤����Ѥ��뤫��#�����ֹ�ǥ�󥯡�
#
# - DESCRIPTION
#	���뵭���򥿥��ȥ�ꥹ��ɽ���Ѥ˥ե����ޥåȤ��롥
#
sub DumpArtSummary
{
    local( $id, $aids, $icon, $title, $name, $origDate,	$flag ) = @_;

    $gHgStr .= qq(<span class="kbTitle">$id.);	# �����

    if ( $flag&1 && $DB_FID{$id} )
    {
	local( $fId ) = $DB_FID{$id};
	$fId =~ s/^.*,//o;
	$gHgStr .= ' ' . &LinkP( "b=$BOARD&c=t&id=$fId", $H_THREAD_ALL, '',
	    $H_THREAD_ALL_L );
    }

    $gHgStr .= ' ' . &TagMsgImg( $icon ) . ' ' .
	(( $flag&2 )? &TagA( $title || $id, "$cgi'REQUEST_URI#a$id" ) :
	&LinkP( "b=$BOARD&c=e&id=$id", $title || $id ));

    if ( $aids )
    {
	$gHgStr .= ' ' . &LinkP( "b=$BOARD&c=t&id=$id", $H_THREAD, '',
	    $H_THREAD_L );
    }

    $gHgStr .= ' [' . ( $name || $MAINT_NAME ) . '] ' .
	&GetDateTimeFormatFromUtc( $origDate || &GetModifiedTime( $id,
	$BOARD));

    if ( $DB_NEW{$id} )
    {
	$gHgStr .= ' ' . &TagMsgImg( $H_NEWARTICLE );
    }
    $gHgStr .= '</span>';
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
#	for each `<KB:foobar>' LINE in the source file,
#	the function `foobar' was called.
#
# - RETURN
#	1 if succeed, 0 if failed.
#
sub htmlGen
{
    local( $source ) = @_;

    local( $file ) = &GetPath( $UI_DIR, $source );

    $gHgStr = "";
    open( SRC, "<$file" ) || &Fatal( 1, $file );

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
    &cgiauth'Header( 0, 0, 1, $cookieExpire );
    &cgiprint'Init();

    while( <SRC> )
    {
	LINE: while ( 1 )
	{
	    if ( s/<KB:(\w+)(\s*var="([^"]*)")?>//o )
	    {
		$gHgStr .= $`;
		eval( '&hg' . $1 . '( "' . $source . '", "' . $3 . '" );' );
		&Fatal( 998, "$file : $@" ) if $@;
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
#	$Subject	��������Subject
#	$Icon		����������������
#	$Id		��������ID
#	@To		������E-Mail addr�ꥹ��
#
# - DESCRIPTION
#	���������夷�����Ȥ�ᥤ�뤹�롥
#
sub ArriveMail
{
    local( $Name, $Email, $Subject, $Icon, $Id, @To ) = @_;

    local( $StrSubject, $MailSubject, $StrFrom, $Message );
    $StrSubject = ( !$SYS_ICON || ( $Icon eq $H_NOICON ))? $Subject :
	"($Icon) $Subject";
    $StrSubject =~ s/<[^>]*>//go;
    $StrSubject = &HTMLDecode( $StrSubject );
    $MailSubject = &GetMailSubjectPrefix( $BOARDNAME, $Id ) . $StrSubject;
    $StrFrom = $Email? "$Name <$Email>" : "$Name";

    $Message = "$SYSTEM_NAME����Τ��Τ餻�Ǥ���

��$BOARDNAME�פ��Ф��ơ�$StrFrom�פ��󤫤顤
��$StrSubject�פȤ�����Ǥν񤭹��ߤ�����ޤ�����

�����֤Τ������
$SCRIPT_URL?b=$BOARD&c=e&id=$Id
�������������

�Ǥϼ��餷�ޤ���";

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
sub FollowMail
{
    local( $Name, $Email, $Date, $Subject, $Icon, $Id, $Fname, $Femail, $Fsubject, $Ficon, $Fid, @To ) = @_;
    
    local( $InputDate, $StrSubject, $FstrSubject, $MailSubject, $StrFrom, $FstrFrom, $Message );

    $InputDate = &GetDateTimeFormatFromUtc( $Date );
    $StrSubject = ( !$SYS_ICON || ( $Icon eq $H_NOICON ))? "$Subject" :
	"($Icon) $Subject";
    $StrSubject =~ s/<[^>]*>//go;
    $StrSubject = &HTMLDecode( $StrSubject );
    $FstrSubject = ( $Ficon eq $H_NOICON )? $Fsubject : "($Ficon) $Fsubject";
    $FstrSubject =~ s/<[^>]*>//go;
    $FstrSubject = &HTMLDecode( $FstrSubject );
    $MailSubject = &GetMailSubjectPrefix( $BOARDNAME, $Fid ) . $FstrSubject;
    $StrFrom = $Email? "$Name <$Email>" : "$Name";
    $FstrFrom = $Femail? "$Fname <$Femail>" : "$Fname";

    $Message = "$SYSTEM_NAME����Τ��Τ餻�Ǥ���

$InputDate�ˡ�$BOARDNAME�פ��Ф��ơ�$StrFrom�פ��󤬽񤤤���
��$StrSubject��
$SCRIPT_URL?b=$BOARD&c=e&id=$Id
���Ф��ơ�
��$FstrFrom�פ��󤫤�
��$FstrSubject�פȤ�����Ǥ�ȿ��������ޤ�����

�����֤Τ������
$SCRIPT_URL?b=$BOARD&c=e&id=$Fid
�������������

�Ǥϼ��餷�ޤ���";

    # �ᥤ������
    &SendArticleMail( $Fname, $Femail, $MailSubject, $Message, $Fid, @To );
}


###
## MakeNewArticle - ��������Ƥ��줿����������
#
# - SYNOPSIS
#	MakeNewArticle($Board, $Id, $artKey, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail);
#
# - ARGS
#	$Board		�������뵭��������Ǽ��Ĥ�ID
#	$Id		��ץ饤��������ID
#	$artKey		¿�Ž񤭹����ɻ��ѥ���
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
sub MakeNewArticle
{
    local( $Board, $Id, $artKey, $TextType, $Name, $Email, $Url, $Icon,
	$Subject, $Article, $Fmail, $MailRelay ) = @_;

    local( $ArticleId );

    &CheckArticle( $Board, *Name, *Email, *Url, *Subject, *Icon, *Article );

    # �����������ֹ�����(�ޤ������ֹ�������Ƥʤ�)
    $ArticleId = &GetNewArticleId( $Board );

    # �����Υե�����κ���
    &MakeArticleFile( $TextType, $Article, $ArticleId, $Board );

    # �����������ֹ��񤭹���
    &WriteArticleId( $ArticleId, $Board, $artKey );

    # DB�ե��������Ƥ��줿�������ɲ�
    # �̾�ε������Ѥʤ�ID
    &AddDBFile( $ArticleId, $Board, $Id, $^T, $Subject, $Icon,
	( $SYS_LOGHOST? $REMOTE_INFO : '' ), $Name, $Email, $Url, $Fmail,
	$MailRelay );

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
# - DESCRIPTION
#	�������������롥
#
sub SupersedeArticle
{
    local( $Board, $Id, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail ) = @_;

    local( $SupersedeId, $File, $SupersedeFile );

    # ���Ϥ��줿��������Υ����å�
    &CheckArticle( $Board, *Name, *Email, *Url, *Subject, *Icon, *Article );

    # DB�ե����������
    $SupersedeId = &SupersedeDbFile( $Board, $Id, $^T, $Subject, $Icon, ( $SYS_LOGHOST? $REMOTE_INFO : '' ), $Name, $Email, $Url, $Fmail );

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
sub CheckArticle
{
    local( $board, *name, *eMail, *url, *subject, *icon, *article ) = @_;

    &CheckName( *name );
    &CheckEmail( *eMail );
    &CheckURL( *url );
    &CheckSubject( *subject );
    &CheckIcon( *icon, $board ) if $SYS_ICON;

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
	'B',	1,	$HTML_TAGS_GENATTRS,
	'BIG',	1,	$HTML_TAGS_GENATTRS,
	'CITE',	1,	$HTML_TAGS_GENATTRS,
	'CODE',	1,	$HTML_TAGS_GENATTRS,
	'DEL',	1,	"$HTML_TAGS_GENATTRS/CITE/DATETIME",
	'EM',	1,	$HTML_TAGS_GENATTRS,
	'I',	1,	$HTML_TAGS_GENATTRS,
	'IMG',	0,	"$HTML_TAGS_GENATTRS/ALT/HEIGHT/LONGDESC/SRC/WIDTH",
	'INS',	1,	"$HTML_TAGS_GENATTRS/CITE/DATETIME",
	'KBD',	1,	$HTML_TAGS_GENATTRS,
	'SAMP',	1,	$HTML_TAGS_GENATTRS,
	'SMALL',1,	$HTML_TAGS_GENATTRS,
	'SPAN',	1,	$HTML_TAGS_GENATTRS,
	'STRONG',1,	$HTML_TAGS_GENATTRS,
	'STYLE',1,	"$HTML_TAGS_I18NATTRS/MEDIA/TITLE/TYPE",
	'SUB',	1,	$HTML_TAGS_GENATTRS,
	'SUP',	1,	$HTML_TAGS_GENATTRS,
	'TT',	1,	$HTML_TAGS_GENATTRS,
	'VAR',	1,	$HTML_TAGS_GENATTRS,
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

sub secureArticle
{
    local( *article, $textType ) = @_;

    local( @articleTags ) = (
	# ����̾, �Ĥ�ɬ�ܤ��ݤ�, ���Ѳ�ǽ��feature
	'A',	1,	"$HTML_TAGS_GENATTRS/CHARSET/HREF/HREFLANG/NAME/REL/REV/TABINDEX/TARGET/TYPE",
	'ABBR',	1,	$HTML_TAGS_GENATTRS,
	'ADDRESS',1,	$HTML_TAGS_GENATTRS,
	'B',	1,	$HTML_TAGS_GENATTRS,
	'BIG',	1,	$HTML_TAGS_GENATTRS,
	'BLOCKQUOTE',1,	"$HTML_TAGS_GENATTRS/CITE",
	'BR',	0,	$HTML_TAGS_COREATTRS,
	'CITE',	1,	$HTML_TAGS_GENATTRS,
	'CODE',	1,	$HTML_TAGS_GENATTRS,
	'DD',	0,	$HTML_TAGS_GENATTRS,
	'DEL',	1,	"$HTML_TAGS_GENATTRS/CITE/DATETIME",
	'DFN',	1,	$HTML_TAGS_GENATTRS,
	'DIV',	1,	$HTML_TAGS_GENATTRS,
	'DL',	1,	$HTML_TAGS_GENATTRS,
	'DT',	0,	$HTML_TAGS_GENATTRS,
	'EM',	1,	$HTML_TAGS_GENATTRS,
	'H1',	1,	$HTML_TAGS_GENATTRS,
	'H2',	1,	$HTML_TAGS_GENATTRS,
	'H3',	1,	$HTML_TAGS_GENATTRS,
	'H4',	1,	$HTML_TAGS_GENATTRS,
	'H5',	1,	$HTML_TAGS_GENATTRS,
	'H6',	1,	$HTML_TAGS_GENATTRS,
	'HR',	0,	$HTML_TAGS_COREATTRS,
	'I',	1,	$HTML_TAGS_GENATTRS,
	'IMG',	0,	"$HTML_TAGS_GENATTRS/ALT/HEIGHT/LONGDESC/SRC/WIDTH",
	'INS',	1,	"$HTML_TAGS_GENATTRS/CITE/DATETIME",
	'KBD',	1,	$HTML_TAGS_GENATTRS,
	'LI',	0,	$HTML_TAGS_GENATTRS,
	'OL',	1,	$HTML_TAGS_GENATTRS,
	'P',	1,	$HTML_TAGS_GENATTRS,
	'PRE',	1,	$HTML_TAGS_GENATTRS,
	'Q',	1,	"$HTML_TAGS_GENATTRS/CITE",
	'SAMP',	1,	$HTML_TAGS_GENATTRS,
	'SMALL',1,	$HTML_TAGS_GENATTRS,
	'SPAN',	1,	$HTML_TAGS_GENATTRS,
	'STRONG',1,	$HTML_TAGS_GENATTRS,
	'STYLE',1,	"$HTML_TAGS_I18NATTRS/MEDIA/TITLE/TYPE",
	'SUB',	1,	$HTML_TAGS_GENATTRS,
	'SUP',	1,	$HTML_TAGS_GENATTRS,
	'TT',	1,	$HTML_TAGS_GENATTRS,
	'UL',	1,	$HTML_TAGS_GENATTRS,
	'VAR',	1,	$HTML_TAGS_GENATTRS,
# ���䥵������style�ǻ��ꤹ�٤��ʤΤǡ���������ɬ���FONT�����ʤ櫓�Ǥ�����
# ����Ǥ�ɡ����Ƥ�Ȥ������Ȥ������ʤ��ϡ�
# ���ιԤ���Ƭ�Ρ�#�פ�ä��Ƥ���������^^;
#	'FONT',	1,	"$HTML_TAGS_GENATTRS/SIZE/COLOR",
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
	&cgi'SecureHtmlEx( *article, *aNeedVec, *aFeatureVec );
    }
    elsif ( $textType eq $H_TTLABEL[2] )
    {
	# secrurity check
	&cgi'SecureHtmlEx( *article, *aNeedVec, *aFeatureVec );
    }
    else
    {
	&Fatal( 0, 'must not be reached...' );
    }
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
#	CheckIcon( *str, $board );
#
# - ARGS
#	*str		Iconʸ����
#	$board		�Ǽ���ID
#
# - DESCRIPTION
#	Icon��ʸ��������å���Ԥʤ���
#	������ʸ������ä��饨�顼ɽ���롼����ء�
#
sub CheckIcon
{
    local( *str, $board ) = @_;

    # ��������Υ����å�; ������������̵���פ����ꡥ
    $str = $H_NOICON if ( !&GetIconUrlFromTitle( $str, $board ));

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
    &Fatal( 6, $String ) if ( $String =~ /^\d+$/ );
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

    local( @aidList ) = split( /,/, $DB_AIDS{$id} );

    push( @tree, '(', $id );
    foreach ( @aidList ) { &GetFollowIdTree( $_, *tree ); }
    push( @tree, ')' );
}


###
## GetTreeTopArticlesInfo - �ڹ�¤�Υȥå׵����ξ�������
#
# - SYNOPSIS
#	GetTreeTopArticlesInfo	( *tree );
#
# - ARGS
#	*tree	�ڹ�¤����Ǽ�ѤߤΥꥹ��
#
# - DESCRIPTION
#	�ڹ�¤�ξܺ٤ˤĤ��Ƥ�&GetFollowIdTree()�򻲾ȤΤ��ȡ�
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
sub GetTreeTopArticlesInfo
{
    local( *tree ) = @_;
    &GetArticlesInfo( $tree[1] );
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
#	�Ť��С�������KINOBOARDS�Ǥϡ�
#	DB��˻����ɽ��ʸ����(not UTC)�����Τޤ����äƤ��뤬��
#	���줬�Ϥ��줿���(UTC�Ǥʤ��ä����)�ϡ����Τޤ��֤���
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
#	UTC
#
sub GetUtcFromYYYY_MM_DD
{
    local( $str ) = shift;
    return -1 if ( length( $str ) != 10 );

    local( $year, $month, $mday ) = unpack( "a4 x a2 x a2", $str );
    if (( $year < 1970 ) ||
	( $year > 2037 ) ||
	( $month < 1 ) ||
	( $month > 12 ) ||
	( $mday < 1 ) ||
	( $mday > 31 ))
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
		local( $boardInfo ) = &GetBoardInfo( $1 );
		$tagStr = &LinkP( "b=$1&c=e&id=$2", $quoteStr ) if $boardInfo;
	    }
	    else
	    {
		$tagStr = &LinkP( "b=$BOARD&c=e&id=$artStr", $quoteStr );
	    }
	}
	elsif ( &IsUrl( $urlMatch ))
	{
	    $tagStr = &TagA( $quoteStr, $url, '', '', '', $SYS_LINK_TARGET );
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

    local( $t );

    # ����������μ���
    local( $Fid, $Date, $Title, $Name );
    ( $Fid, $t, $Date, $Title, $t, $t, $Name ) = &GetArticlesInfo( $Id );

    # �������Τ���˸���������
    local( $pName ) = '';
    if ( $Fid )
    {
	$Fid =~ s/,.*$//o;
	( $t, $t, $t, $t, $t, $t, $pName ) = &GetArticlesInfo( $Fid );
    }

    # ����
    local( @ArticleBody );
    &GetArticleBody( $Id, $BOARD, *ArticleBody );

    if ( $SYS_QUOTEMSG )
    {
	local( $premsg ) = $SYS_QUOTEMSG;
	$premsg =~ s/__LINK__/[url:kb:$Id]/i;
	$premsg =~ s/__TITLE__/$Title/;
	$premsg =~ s/__DATE__/&GetDateTimeFormatFromUtc( $Date )/e;
	$premsg =~ s/__NAME__/$Name/;
	$msg .= $premsg;
    }
    local( $QMark, $line );
    foreach $line ( @ArticleBody )
    {
	&TAGEncode( *line );

	$QMark = $DEFAULT_QMARK;
	$QMark = $Name . ' ' . $QMark if $SYS_QUOTENAME;

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
	$str .= &LinkP(
	    "b=$BOARD&c=$com&num=$num&old=0&fold=$fold&rev=$rev",
	    $H_TOP . &TagAccessKey( 'T' ), 'T' );
	$str .= ' | ' . &LinkP(
	    "b=$BOARD&c=$com&num=$num&old=$nextOld&fold=$fold&rev=$rev",
	    $H_UP . &TagAccessKey( 'N' ), 'N' );
    }
    else
    {
	$str .= $H_TOP . &TagAccessKey( 'T' ) . ' | ' . $H_UP .
	    &TagAccessKey( 'N' );
    }

    if ( $SYS_REVERSE )
    {
	$str .= ' | ' .
	    &LinkP( "b=$BOARD&c=$com&num=$num&old=$old&fold=$fold&rev=" .
	    ( 1-$rev ), $H_REVERSE[ 1-$rev ] . &TagAccessKey( 'R' ), 'R',
	    $H_REVERSE_L );
    }

    if ( $SYS_EXPAND && ( $fold ne '' ))
    {
	$str .= ' | ' .
	    &LinkP( "b=$BOARD&c=$com&num=$num&old=$old&rev=$rev&fold=" .
	    ( 1-$fold ), $H_EXPAND[ 1-$fold ] . &TagAccessKey( 'E' ), 'E',
	    $H_EXPAND_L );
    }

    $str .= ' | ';

    if ( $num && ( $#DB_ID - $backOld >= 0 ))
    {
	$str .= &LinkP(
	    "b=$BOARD&c=$com&num=$num&old=$backOld&fold=$fold&rev=$rev",
	    $H_DOWN . &TagAccessKey( 'P' ), 'P' );
	$str .= ' | ' . &LinkP(
	    "b=$BOARD&c=$com&num=$num&old=" . ( $#DB_ID - $backOld + 1) .
	    "&fold=$fold&rev=$rev", $H_BOTTOM . &TagAccessKey( 'B' ),
	    'B' );
    }
    else
    {
	$str .= $H_DOWN . &TagAccessKey( 'P' ) . ' | ' . $H_BOTTOM .
	    &TagAccessKey( 'B' );
    }

    $str .= "</p>\n";

    $str;
}

sub ShowPageLinkEachPage	# not used.
{
    local( $com, $num, $old, $rev, $vRev ) = @_;

    local( $nextOld ) = ( $old > $num )? ( $old - $num ) : 0;
    local( $backOld ) = ( $old + $num );

    local( $str ) = '<p>';

    $MAX_PAGELINK = 5;

    if ( $SYS_REVERSE )
    {
	$str .= &LinkP( "b=$BOARD&c=$com&num=$num&old=$old&rev=" . ( 1-$rev ),
	    $H_REVERSE[ 1-$rev ] . &TagAccessKey( 'R' ), 'R', $H_REVERSE_L ) .
	    ' ';
    }

    if ( $SYS_EXPAND )
    {
	$str .= &LinkP( "b=$BOARD&c=$com&num=$num&old=$old&rev=$rev&fold=" .
	    ( 1-$fold ), $H_EXPAND[ 1-$fold ] . &TagAccessKey( 'E' ), 'E',
	    $H_EXPAND_L );
    }

    if ( $vRev )
    {
	if ( $num && ( $#DB_ID - $backOld > 0 ))
	{
	    $str .= &LinkP( "b=$BOARD&c=$com&num=$num&old=0&rev=$rev",
		$H_TOP );
	    $str .= &LinkP( "b=$BOARD&c=$com&num=$num&old=$backOld&rev=$rev",
		$H_UP );
	}
	else
	{
	    $str .= $H_TOP . $H_UP;
	}

	local( $i );
	for ( $i = -$MAX_PAGELINK; $i <= +$MAX_PAGELINK; $i++ )
	{
	    $str .= ' ';
	    if ( $old - $i * $num <= $#DB_ID )
	    {
		$str .= &LinkP( "b=$BOARD&c=$com&num=$num&old=" . ( $i*$num ) .
		    "&rev=$rev", $i );
	    }
	    else
	    {
		$str .= $i;
	    }
	}
	$str .= ' ';

	if ( $old )
	{
	    $str .= &LinkP( "b=$BOARD&c=$com&num=$num&old=$nextOld&rev=$rev",
		$H_DOWN );
	}
	else
	{
	    $str .= $H_DOWN;
	}
    }
    else
    {
	if ( $old )
	{
	    $str .= &LinkP( "b=$BOARD&c=$com&num=$num&old=0&rev=$rev",
		$H_TOP );
	    $str .= &LinkP( "b=$BOARD&c=$com&num=$num&old=$nextOld&rev=$rev",
		$H_UP );
	}
	else
	{
	    $str .= $H_TOP . $H_UP;
	}

	local( $i );
	$MAX_PAGELINK = 5;
	for ( $i = $MAX_PAGELINK; $i >= -$MAX_PAGELINK; $i-- )
	{
	    $str .= ' ';
	    if ( $old - $i * $num <= $#DB_ID )
	    {
		$str .= &LinkP( "b=$BOARD&c=$com&num=$num&old=" . ( $i*$num ) .
		    "&rev=$rev", $i );
	    }
	    else
	    {
		$str .= $i;
	    }
	}
	$str .= ' ';

	if ( $num && ( $#DB_ID - $backOld > 0 ))
	{
	    $str .= &LinkP( "b=$BOARD&c=$com&num=$num&old=$backOld&rev=$rev",
		$H_DOWN );
	}
	else
	{
	    $str .= $H_DOWN;
	}
    }

    $str .= "</p>\n";

    $str;
}

sub ShowPageLinkTop		# not used
{
    local( $com, $num, $old, $rev, $vRev ) = @_;

    local( $nextOld ) = ( $old > $num )? ( $old - $num ) : 0;
    local( $backOld ) = ( $old + $num );

    local( $str ) = '<p>';

    if ( $vRev )
    {
	if ( $num && ( $#DB_ID - $backOld > 0 ))
	{
	    $str .= &LinkP( "b=$BOARD&c=$com&num=$num&old=$backOld&rev=$rev",
		$H_DOWN );
	}
	else
	{
	    $str .= $H_DOWN;
	}
    }
    else
    {
	if ( $old )
	{
	    $str .= &LinkP( "b=$BOARD&c=$com&num=$num&old=0&rev=$rev",
		$H_TOP );
	    $str .= &LinkP( "b=$BOARD&c=$com&num=$num&old=$nextOld&rev=$rev",
		$H_UP );
	}
	else
	{
	    $str .= $H_TOP . $H_UP;
	}
    }

    if ( $SYS_REVERSE )
    {
	$str .= ' // ' . &LinkP( "b=$BOARD&c=$com&num=$num&old=$old&rev=" .
		( 1-$rev ), $H_REVERSE[ 1-$rev ], &TagAccessKey( 'R' ), 'R',
		$H_REVERSE_L );
    }

    if ( $SYS_EXPAND )
    {
	$str .= &LinkP( "b=$BOARD&c=$com&num=$num&old=$old&rev=$rev&fold=" .
	    ( 1-$fold ), $H_EXPAND[ 1-$fold ] . &TagAccessKey( 'E' ), 'E',
	    $H_EXPAND_L );
    }

    $str .= "</p>\n";

    $str;
}

sub ShowPageLinkBottom		# not used.
{
    local( $com, $num, $old, $rev, $vRev ) = @_;

    local( $nextOld ) = ( $old > $num )? ( $old - $num ) : 0;
    local( $backOld ) = ( $old + $num );

    local( $str ) = '<p>';

    if ( $SYS_REVERSE )
    {
	$str .= &LinkP( "b=$BOARD&c=$com&num=$num&old=$old&rev=" . ( 1-$rev ),
	    $H_REVERSE[ 1-$rev ] . &TagAccessKey( 'R' ), 'R', $H_REVERSE_L );
    }

    if ( $SYS_EXPAND )
    {
	$str .= ' ' .
	    &LinkP( "b=$BOARD&c=$com&num=$num&old=$old&rev=$rev&fold=" .
	    ( 1-$fold ), $H_EXPAND[ 1-$fold ] . &TagAccessKey( 'E' ), 'E',
	    $H_EXPAND_L ) . ' // ';
    }

    if ( $vRev )
    {
	if ( $old )
	{
	    $str .= &LinkP( "b=$BOARD&c=$com&num=$num&old=0&rev=$rev",
		$H_TOP );
	    $str .= &LinkP( "b=$BOARD&c=$com&num=$num&old=$nextOld&rev=$rev",
		$H_UP );
	}
	else
	{
	    $str .= $H_TOP . $H_UP;
	}
    }
    else
    {
	if ( $num && ( $#DB_ID - $backOld > 0 ))
	{
	    $str .= &LinkP( "b=$BOARD&c=$com&num=$num&old=$backOld&rev=$rev",
		$H_DOWN );
	}
	else
	{
	    $str .= $H_DOWN;
	}
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
	qq(<img src="$src" alt="$alt" width="$COMICON_WIDTH" height="$COMICON_HEIGHT" class="kbComIcon">);
    }
    elsif ( $SYS_COMICON == 2 )
    {
	qq(<img src="$src" alt="$alt" width="$COMICON_WIDTH" height="$COMICON_HEIGHT" class="kbComIcon">$alt);
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
	local( $src ) = &GetIconUrlFromTitle( $icon, $BOARD );
	qq(<img src="$src" alt="[$icon]" width="$MSGICON_WIDTH" height="$MSGICON_HEIGHT" class="kbMsgIcon">);
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

    $href =~ s/&/&amp;/go;
    if ( $key eq '' )
    {
	$key = sprintf( "%d", $gLinkNum );
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
    qq[<label for="$label" accesskey="$accessKey">$markUp] . &TagAccessKey( $accessKey ) . "</label>";
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
	qq(<input type="reset" value="$value" accesskey="$key" tabindex="$gTabIndex">);
    }
    else
    {
	qq(<input type="submit" value="$value" accesskey="$key" tabindex="$gTabIndex">);
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
    qq(<input type="$type" id="$id" name="$id" value="$value" size="$size" tabindex="$gTabIndex">);
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
	qq(<input type="checkbox" id="$id" name="$id" value="on" tabindex="$gTabIndex" checked>);
    }
    else
    {
	qq(<input type="checkbox" id="$id" name="$id" value="$value" tabindex="$gTabIndex">);
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
	qq(<input type="radio" id="$id" name="$name" value="$value" tabindex="$gTabIndex" checked>);
    }
    else
    {
	qq(<input type="radio" id="$id" name="$name" value="$value" tabindex="$gTabIndex">);
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
    $comm .= "&kinoA=3&kinoU=$UNAME&kinoP=$PASSWD" if ( $SYS_AUTH == 3 );
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
    local( $old ) = $#DB_ID - int( $id + $DEF_TITLE_NUM/2 );
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
}

sub UnlockAll
{
    &cgi'unlock_file( $LOCK_FILE ) unless $PC;
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

    $ExtHeader = "X-Kb-System: $SYSTEM_NAME\n";
    if (( ! $SYS_MAILHEADBRACKET ) && $BOARDNAME && ($Id ne '' ))
    {
	$ExtHeader .= "X-Kb-Board: $BOARDNAME\nX-Kb-Articleid: $Id\n";
    }

    # ���ѵ���
    if ( $Id ne '' ) {
	$Message .= "\n--------------------\n";
	&GetArticleBody($Id, $BOARD, *ArticleBody);
	foreach ( @ArticleBody )
	{
	    s/<[^>]*>//go;	# �������פ�ʤ�
	    $Message .= &HTMLDecode( $_ ) if ( $_ ne '' );
	}
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
	&UnlockBoard();
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
    elsif ( $errno == 6)
    {
	$severity = $kinologue'SEV_INFO;
	$msg = "��$errInfo�פȤ���$H_FROM�ϻȤ��ޤ�����ä��̤�$H_FROM����ꤷ�Ƥ���������";
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
	$msg .= "���Ѥ�����Ǥ��������Υ�å�������ʸ�Υ��ԡ��ȡ����顼��������������" . &TagA( $MAINT, "mailto:$MAINT" ) . "�ޤǤ��Τ餻ĺ����Ƚ�����ޤ���";
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
	$DB_DATE{$dId} = $dDate || &GetModifiedTime($dId, $Board);
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
#	$MailRelay	�ɲä���������ᥤ��Ȥ���ή�����ɤ���
#
# - DESCRIPTION
#	����DB�˵������ɲä��롥
#
sub AddDBFile
{
    local( $Id, $Board, $Fid, $InputDate, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail, $MailRelay ) = @_;

    local( $dId, $dFid, $dAids, $dInputDate, $dSubject, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail, $mdName, $mdEmail, $mdInputDate, $mdSubject, $mdIcon, $mdId, $FidList, $FFid, @FollowMailTo, @FFid, @ArriveMail );

    # ��ץ饤���Υ�ץ饤�������äƤ���
    if ( $Fid ne '' )
    {
	( $FFid ) = &GetArticlesInfo( $Fid );
	@FFid = split( /,/, $FFid );
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
		push( @FollowMailTo, $dEmail ) if $dFmail;
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
	&GetArriveMailTo( 0, $Board, *ArriveMail );
	&ArriveMail( $Name, $Email, $Subject, $Icon, $Id, @ArriveMail ) if @ArriveMail;
    }

    # ɬ�פʤ�ȿ�������ä����Ȥ�ᥤ�뤹��
    if ( $MailRelay && ( $SYS_MAIL & 2 ) && @FollowMailTo )
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

    # �������륷���ȥե�����κ����ʥ��ԡ���
    $src = &GetPath( $BOARDSRC_DIR, $CSS_FILE );
    $dest = &GetPath( $name, $CSS_FILE );
    &CopyDb( $src, $dest ) || &Fatal( 20, "$src -&gt; $dest" );

    # ��ư�����ᥤ��DB�κ���
    &UpdateArriveMailDb( $name, *arriveMail );

    # �إå��ե�����κ���
    &UpdateHeaderDb( $name, *header );

    # �Ǹ�ˡ��Ǽ���DB�򹹿�����
    local( $file ) = $BOARD_FILE;
    local( $tmpFile ) = "$BOARD_FILE.$TMPFILE_SUFFIX$$";
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

    local( $file ) = $BOARD_FILE;
    local( $tmpFile ) = "$BOARD_FILE.$TMPFILE_SUFFIX$$";
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
    &UpdateArriveMailDb( $board, *arriveMail );

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
    local( $dbFile ) = $BOARD_FILE;
    open( DB, "<$dbFile" ) || &Fatal( 1, $dbFile );
    while ( <DB> )
    {
	next if ( /^\#/o || /^$/o );
	chop;
	( $bId, $bName, $bInfo ) = split( /\t/, $_, 3 );
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
#	�Ǽ���̾
#
sub GetBoardInfo
{
    local( $board ) = @_;

    local( $dBoard, $dBoardName, $dBoardConf );

    local( $dbFile ) = $BOARD_FILE;
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
    return if ( $gIconDbCached eq $board );

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

    $gIconDbCached = $board;		# cached
}


###
## GetBoardHeader - �Ǽ��ĥإå�DB���ɤ߹���
#
# - SYNOPSIS
#	GetBoardHeader($Board, *BoardHeader);
#
# - ARGS
#	$BoardId	�Ǽ���ID
#	*BoardHeader	��ʸ�ƹԤ������ʸ����ؤΥ�ե����
#
# - DESCRIPTION
#	�Ǽ��ĥǥ��쥯�ȥ����Ρ��Ǽ��ĥإå��ե�������ɤ߽Ф���
#
sub GetBoardHeader
{
    local( $Board, *BoardHeader ) = @_;

    local( $File ) = &GetPath( $Board, $HEADER_FILE_NAME );
    open( HEADER, "<$File" ) || &Fatal( 1, $File );
    while ( <HEADER> )
    {
	s/__PROGRAM__/$PROGRAM/go;
	s/__BOARD__/$Board/go;
	s/__TITLE_NUM__/$DEF_TITLE_NUM/go;
	s/__ARTICLE_NUM__/$DEF_ARTICLE_NUM/go;
	$BoardHeader .= $_;
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
#	$icon		��������ID
#	$board		�Ǽ���ID
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
    local( $icon, $board ) = @_;
    return $ICON_NEW if ( $icon eq $H_NEWARTICLE );

    # prepare
    &CacheIconDb( $board );

    # check
    return '' unless $ICON_FILE{ $icon };

    # return
    "$ICON_DIR/" . $ICON_FILE{$icon};
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
