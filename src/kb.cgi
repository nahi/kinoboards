#!/usr/local/bin/perl

# ���Υե�������ѹ��Ϻ���2�սꡤ����4�ս�Ǥ��ʴĶ�����Ǥ��ˡ�
#
# 1. ������Ƭ�Ԥǡ�Perl�Υѥ�����ꤷ�ޤ�����#!�פ�³���ƻ��ꤷ�Ƥ���������

# 2. kb�ǥ��쥯�ȥ�Υե�ѥ�����ꤷ�Ƥ���������URL�ǤϤʤ����ѥ��Ǥ��ˡ�
#    !! KB/1.0R6.4�ʹߡ����������ɬ�ܤȤʤ�ޤ��� !!
#
$KBDIR_PATH = '';
# $KBDIR_PATH = '/home/nahi/public_html/kb/';
# $KBDIR_PATH = 'd:\inetpub\wwwroot\kb\';	# WinNT/Win9x�ξ��
# $KBDIR_PATH = 'foo:bar:kb:';			# Mac�ξ��?

# 3. �����Ф�ư���Ƥ���ޥ���Win95/Mac�ξ�硤
#    $PC��1�����ꤷ�Ƥ��������������Ǥʤ���硤������������פǤ���
#
$PC = 0;	# for UNIX / WinNT
# $PC = 1;	# for Win95 / Mac

# 4. �����Ф�CGIWRAP�����Ѥ��Ƥ����硤�ʲ��Υ����Ȥ򳰤���
#    kb�ǥ��쥯�ȥ��URL����ꤷ�Ƥ��������ʺ��٤ϥѥ��ǤϤʤ���URL�Ǥ��ˡ�
#    �����Ǥʤ��ͤϡ��ѹ���ɬ�פϤ���ޤ��󡥥����ȤΤޤޤ�OK�Ǥ���
#
# $KB_RESOURCE_URL = '/~nahi/kb/';


# �ʲ��Ͻ񤭴�����ɬ�פϤ���ޤ���


######################################################################


# $Id: kb.cgi,v 5.43.2.6 2000-04-05 14:44:22 nakahiro Exp $

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

# ����ѿ������
$HEADER_FILE = 'kb.ph';		# header file
$KB_VERSION = '1.0';		# version
$KB_RELEASE = '6.10';		# release

# �ǥ��쥯�ȥ�
$ICON_DIR = 'icons';				# ��������ǥ��쥯�ȥ�
$UI_DIR = 'UI';					# UI�ǥ��쥯�ȥ�
$LOG_DIR = 'log';				# ���ǥ��쥯�ȥ�

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
$KB_RESOURCE_URL = $KB_RESOURCE_URL || $cgi'PATH_INFO;
$KB_RESOURCE_URL .= '/' if ( $KB_RESOURCE_URL && $KB_RESOURCE_URL !~ m!/$!o );
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
$HTML_TAGS_COREATTRS = 'ID/CLASS/STYLE/TITLE';
$HTML_TAGS_I18NATTRS = 'LANG/DIR';
$HTML_TAGS_GENATTRS = "$HTML_TAGS_COREATTRS/$HTML_TAGS_I18NATTRS";

# ��������ե���������URL
$ICON_BLIST = &GetIconURL( 'blist.gif' );		# �Ǽ��İ�����
$ICON_TLIST = &GetIconURL( 'tlist.gif' );		# �����ȥ������
$ICON_PREV = &GetIconURL( 'prev.gif' );			# ���ε�����
$ICON_NEXT = &GetIconURL( 'next.gif' );			# ���ε�����
$ICON_WRITENEW = &GetIconURL( 'writenew.gif' );		# �����񤭹���
$ICON_FOLLOW = &GetIconURL( 'follow.gif' );		# ��ץ饤
$ICON_QUOTE = &GetIconURL( 'quote.gif' );		# ���Ѥ��ƥ�ץ饤
$ICON_THREAD = &GetIconURL( 'thread.gif' );		# �ޤȤ��ɤ�
$ICON_HELP = &GetIconURL( 'help.gif' );			# �إ��
$ICON_DELETE = &GetIconURL( 'delete.gif' );		# ���
$ICON_SUPERSEDE = &GetIconURL( 'supersede.gif' );	# ����
$ICON_NEW = &GetIconURL( 'listnew.gif' );		# ����

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
	$modTime = &GetModifiedTime( $DB_FILE_NAME, $cgi'TAGS{'b'} )
	    if $cgi'TAGS{'b'};
	&cgi'Header( 1, $modTime, 0, (), 0 );
	last;
    }

    local( $c ) = $cgi'TAGS{'c'};
    local( $com ) = $cgi'TAGS{'com'};
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
            $c = 'v';
        }
        elsif ( $SYS_F_B )
        {
            $c = 'bl';
        }
        else
        {
            $c = 'v';
            $BOARD = 'test';
        }
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
	    eval( "require( \"$boardConfFile\" );" ) ||
		&Fatal( 1, $boardConfFile );
	}
    }

    if ( $BOARDLIST_URL eq '-' ) { $BOARDLIST_URL = "$PROGRAM?c=bl"; }
    $SYS_F_MT = ( $SYS_F_D || $SYS_F_AM || $SYS_F_MV );

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
	if (( $c eq 'x' ) && ( $com ne 'x' ))
	{
	    # preview��������ʤΤǡ����ޥ�ɽ񤭴�����
	    $gVarBack = 1;
	    $cgi'TAGS{'c'} = $cgi'TAGS{'corig'};
	    $c = $cgi'TAGS{'c'};
	}

	### Entry - �񤭹��߲��̤�ɽ��
	if ( $c eq 'n' )
	{
	    # ����
	    $gVarEntryType = 0;
	    require( &GetPath( $UI_DIR, 'Entry.pl' ));
	    last;
	}
	elsif (( $c eq 'f' ) && !$cgi'TAGS{'s'} )
	{
	    # ��ץ饤
	    $gVarEntryType = 1;
	    require( &GetPath( $UI_DIR, 'Entry.pl' ));
	    last;
	}
	elsif ( $c eq 'q' )
	{
	    # ���ѥ�ץ饤
	    $gVarEntryType = 2;
	    require( &GetPath( $UI_DIR, 'Entry.pl' ));
	    last;
	}
	elsif ( $SYS_F_D && ( $c eq 'f' ) && $cgi'TAGS{'s'} )
	{
	    # ����
	    $gVarEntryType = 3;
	    require( &GetPath( $UI_DIR, 'Entry.pl' ));
	    last;
	}
	elsif (( $c eq 'p' ) && ( $com ne 'x' ))
	{
	    ### Preview - �ץ�ӥ塼���̤�ɽ��
	    require( &GetPath( $UI_DIR, 'Preview.pl' ));
	    last;
	}
	elsif (( $c eq 'p' ) && ( $com eq 'x' ))
	{
	    ### Thanks - ��Ͽ����̤�ɽ����ľ�ܡ�
	    $gVarPreviewFlag = 0;
	    require( &GetPath( $UI_DIR, 'Thanks.pl' ));
	    last;
	}
	elsif (( $c eq 'x' ) && ( $com eq 'x' ))
	{
	    ### Thanks - ��Ͽ����̤�ɽ���ʥץ�ӥ塼��ͳ��
	    $gVarPreviewFlag = 1;
	    require( &GetPath( $UI_DIR, 'Thanks.pl' ));
	    last;
	}
    }

    if ( $c eq 'v' )
    {
	### ThreadTitle - ����å��̥����ȥ����
	$gVarComType = 0;
	require( &GetPath( $UI_DIR, 'ThreadTitle.pl' ));
	last;
    }
    elsif ( $c eq 'vt' )
    {
	### ThreadExt - ����å��̥����ȥ뤪��ӵ�������
	require( &GetPath( $UI_DIR, 'ThreadExt.pl' ));
	last;
    }
    elsif ( $SYS_F_R && ( $c eq 'r' ))
    {
	### SortTitle - ���ս�˥�����
	require( &GetPath( $UI_DIR, 'SortTitle.pl' ));
	last;
    }
    elsif ( $SYS_F_L && ( $c eq 'l' ))
    {
	### SortArticle - ������������ޤȤ��ɽ��
	require( &GetPath( $UI_DIR, 'SortArticle.pl' ));
	last;
    }
    elsif ( $SYS_F_S && ( $c eq 's' ))
    {
	### SearchArticle - �����θ���(ɽ�����̤κ���)
	require( &GetPath( $UI_DIR, 'SearchArticle.pl' ));
	last;
    }
    elsif ( $SYS_ICON && ( $c eq 'i' ))
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
    if ( $SYS_F_MV )
    {
	if  ( $c eq 'ct' )
	{
	    $gVarComType = 2;
	    require( &GetPath( $UI_DIR, 'ThreadTitle.pl' ));
	    last;
	}
	elsif ( $c eq 'ce' )
	{
	    $gVarComType = 3;
	    require( &GetPath( $UI_DIR, 'ThreadTitle.pl' ));
	    last;
	}
	elsif ( $c eq 'mvt' )
	{
	    $gVarComType = 4;
	    require( &GetPath( $UI_DIR, 'ThreadTitle.pl' ));
	    last;
	}
	elsif ( $c eq 'mve' )
	{
	    $gVarComType = 5;
	    require( &GetPath( $UI_DIR, 'ThreadTitle.pl' ));
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
# �桼�����󥿥ե���������ץ���ơ������(����)


###
## Fatal - ���顼ɽ��
#
# - SYNOPSIS
#	Fatal($errno, $errInfo);
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
    ( $gVarFatalNo, $gVarFatalInfo ) = @_;
    require( &GetPath( $UI_DIR, 'Fatal.pl' ));
}


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
    &SendMail( $Name, $Email, $MailSubject, $Message, $Id, @To );
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
    
    local( $StrSubject, $FstrSubject, $MailSubject, $StrFrom, $FstrFrom, $Message );

    $StrSubject = ( !$SYS_ICON || ( $Icon eq $H_NOICON ))? "$Subject" :
	"($Icon) $Subject";
    $StrSubject =~ s/<[^>]*>//go;	# �������פ�ʤ�
    $StrSubject = &HTMLDecode( $StrSubject );
    $FstrSubject = ( $Ficon eq $H_NOICON )? $Fsubject : "($Ficon) $Fsubject";
    $FstrSubject =~ s/<[^>]*>//go;	# �������פ�ʤ�
    $FstrSubject = &HTMLDecode( $FstrSubject );
    $MailSubject = &GetMailSubjectPrefix( $BOARDNAME, $Fid ) . $FstrSubject;
    $StrFrom = $Email? "$Name <$Email>" : "$Name";

    local( $ffIds ) = &GetArticlesInfo( $Id );
    local( $topId ) = ( $ffIds =~ m/([^,]+)$/o );

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
    &SendMail( $Fname, $Femail, $MailSubject, $Message, $Fid, @To );
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

    # ̤��Ƶ������ɤ�ʤ�
    &Fatal( 8, '' ) if ( $Subject eq '' );

    local( $Num );
    foreach ( 0 .. $#DB_ID ) { $Num = $_, last if ( $DB_ID[$_] eq $Id ); }
    local( $PrevId ) = $DB_ID[$Num - 1] if ( $Num > 0 );
    local( $NextId ) = $DB_ID[$Num + 1];

    local( $msg );

    $msg .= "<p><a name=\"a$Id\"> </a>\n";
    # $msg .= "<p id=\"a$Id\">"; # NC/4.5 does not follows this style... (-_-

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

	local( $Old ) = &GetTitleOldIndex( $Id );

	$msg .= &TagA( $BOARDLIST_URL, &TagComImg( $ICON_BLIST, $H_BACKBOARD,
	    $SYS_COMICON )) . "\n" if $SYS_F_B;

	$msg .= $DlmtS .
	    &TagA( "$PROGRAM?b=$BOARD&c=v&num=$DEF_TITLE_NUM&old=$Old",
	    &TagComImg( $ICON_TLIST, $H_BACKTITLEREPLY, $SYS_COMICON )) . "\n";
	
	local( $TagTmp ) = &TagComImg( $ICON_PREV, $H_PREVARTICLE, $SYS_COMICON );
	if ( $PrevId ne '' )
	{
	    $msg .= $DlmtS .
		&TagA( "$PROGRAM?b=$BOARD&c=e&id=$PrevId", $TagTmp ) . "\n";
	}
	else
	{
	    $msg .= "$DlmtS$TagTmp\n";
	}
	
	$TagTmp = &TagComImg( $ICON_NEXT, $H_NEXTARTICLE, $SYS_COMICON );
	if ( $NextId ne '' )
	{
	    $msg .= $DlmtS .
		&TagA( "$PROGRAM?b=$BOARD&c=e&id=$NextId", $TagTmp ) . "\n";
	}
	else
	{
	    $msg .= "$DlmtS$TagTmp\n";
	}
	
	if ( $SYS_F_T )
	{
	    $TagTmp = &TagComImg( $ICON_THREAD, $H_READREPLYALL, $SYS_COMICON );
	    if ( $Aids ne '' )
	    {
		$msg .= $DlmtS .
		    &TagA( "$PROGRAM?b=$BOARD&c=t&id=$Id", $TagTmp ) . "\n";
	    }
	    else
	    {
		$msg .= "$DlmtS$TagTmp\n";
	    }
	}

	$msg .= "$DlmtL\n" if $DlmtL;

	if ( $SYS_F_N )
	{
	    $msg .= $DlmtS . &TagA( "$PROGRAM?b=$BOARD&c=n",
		&TagComImg( $ICON_WRITENEW, $H_POSTNEWARTICLE, $SYS_COMICON ))
		. "\n" .
		$DlmtS . &TagA( "$PROGRAM?b=$BOARD&c=f&id=$Id",
		&TagComImg( $ICON_FOLLOW, $H_REPLYTHISARTICLE, $SYS_COMICON ))
		. "\n" .
		$DlmtS . &TagA( "$PROGRAM?b=$BOARD&c=q&id=$Id",
		&TagComImg( $ICON_QUOTE, $H_REPLYTHISARTICLEQUOTE,
		$SYS_COMICON )) . "\n";
	}

	$msg .= "$DlmtL\n" if $DlmtL;

	if ( $SYS_COMICON == 1 )
	{
	    $msg .= $DlmtS . &TagA( "$PROGRAM?b=$BOARD&c=i&type=article",
		&TagComImg( $ICON_HELP, "�إ��", $SYS_COMICON )) . "\n";
	}
	$msg .= "</p>\n<p>\n";
    }

    # �����ֹ桤��
    $msg .= "<strong>$H_SUBJECT</strong>: <strong>$Id .</strong> ";
    $msg .= &TagMsgImg( $Icon ) . $Subject;

    # ��̾��
    if ( $Url eq '' )
    {
	$msg .= "<br>\n<strong>$H_FROM</strong>: $Name";
    }
    else
    {
	$msg .=  "<br>\n<strong>$H_FROM</strong>: " . &TagA( $Url, $Name );
    }

    # �ᥤ��
    $msg .= ' ' . &TagA( "mailto:$Email" , "&lt;$Email&gt;" )
	if ( $SYS_SHOWMAIL && $Email );

    # �ޥ���
    $msg .= "<br>\n<strong>$H_HOST</strong>: $RemoteHost" if $SYS_SHOWHOST;

    # �����
    $msg .= "<br>\n<strong>$H_DATE</strong>: " .
	&GetDateTimeFormatFromUtc( $Date );

    # ȿ����(���Ѥξ��)
    &ShowLinksToFollowedArticle( *msg, split( /,/, $Fid ))
	if ( $OriginalFlag && ( $Fid ne '' ));

    # �ڤ���
    $msg .= "</p>\n$H_LINE\n";

    &cgiprint'Cache( $msg );
    $msg = '';

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
# - RETURN
#	�ʤ�
#
sub ThreadArticleMain
{
    local( $State, $Head, @Tail ) = @_;

    # �������פ����������Τ�Τ���
    if ( $State&4 )
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
	    &cgiprint'Cache( "<li>", &GetFormattedTitle( $Head, $dAids, $dIcon, $dSubject, $dName, $dDate, $State&3 ), "\n" );
	    $State ^= 1 if ( $State&1 );
	}
    }
    elsif (( $Head ne '(' ) && ( $Head ne ')' ))
    {
	# ��������ɽ��(���ޥ���դ�, �������ʤ�)
	&cgiprint'Cache( "$H_HR\n" );
	&ViewOriginalArticle( $Head, $SYS_COMMAND_EACH, 0 );
    }

    # tail recuresive.
    &ThreadArticleMain( $State, @Tail ) if @Tail;
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
## ReplyArticles - ��ץ饤�����ؤΥ�󥯤�ɽ��
#
# - SYNOPSIS
#	ReplyArticles( @_ );
#
# - ARGS
#	@_	��ץ饤����ID�Υꥹ��
#
# - DESCRIPTION
#	��ץ饤�����ؤΥ�󥯤�ɽ�����롥
#
# - RETURN
#	�ʤ�
#
sub ReplyArticles
{
    &cgiprint'Cache( "$H_LINE\n<p>\n" );

    # ȿ������
    &cgiprint'Cache( "��$H_REPLY\n" );

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
	    &ThreadArticleMain( 4, @tree );
	}
    }
    else
    {
	# ȿ������̵��
	&cgiprint'Cache( "<ul>\n<li>���ߡ�����$H_MESG�ؤ�$H_REPLY�Ϥ���ޤ���\n</ul>\n" );
    }

    &cgiprint'Cache( "</p>\n" );
}


###
## BoardHeader - �Ǽ��ĥإå���ɽ��
#
# - SYNOPSIS
#	BoardHeader();
#
# - ARGS
#	�ʤ�
#
# - DESCRIPTION
#	�Ǽ��ĤΥإå���ɽ�����롥
#
# - RETURN
#	�ʤ�
#
sub BoardHeader
{
    local( $msg );
    &GetBoardHeader( $BOARD, *msg );
    &cgiprint'Cache( $msg );

    if ( $SYS_F_MT )
    {
	&cgiprint'Cache( "<p>\n<ul>\n" );
	&cgiprint'Cache( "<li>", &TagA( "$PROGRAM?c=mp&b=$BOARD", "��ư$H_MAIL�ۿ�������ꤹ��" ), "\n" ) if $SYS_F_AM;
	&cgiprint'Cache( "</ul>\n</p>\n" );
    }
}


###
## ShowPageLinkTop - �ڡ����إå�/�եå���ɽ��
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
#
# - DESCRIPTION
#	�ڡ����إå�/�եå��Υ�󥯷�ʸ�����������롥
#
# - RETURN
#	�ʤ�
#
sub PageLink
{
    local( $com, $num, $old, $rev ) = @_;

    local( $nextOld ) = ( $old > $num )? ( $old - $num ) : 0;
    local( $backOld ) = ( $old + $num );

    local( $str );
    $str = '<p>';

    if ( $old )
    {
	$str .= &TagA( "$PROGRAM?b=$BOARD&c=$com&num=$num&old=$nextOld&rev=$rev", "$H_TOP$H_NEXTART" );
    }
    else
    {
	$str .= $H_NONEXTART;
    }

    if ( $SYS_REVERSE )
    {
	$str .= ' // ' . &TagA( "$PROGRAM?b=$BOARD&c=$com&num=$num&old=$old&rev=" . ( 1-$rev ), $H_REVERSE );
    }

    $str .= ' // ';

    if ( $num && ( $#DB_ID - $old - $num >= 0 ))
    {
	$str .= &TagA( "$PROGRAM?b=$BOARD&c=$com&num=$num&old=$backOld&rev=$rev", "$H_BACKART$H_BOTTOM" );
    }
    else
    {
	$str .= $H_NOBACKART;
    }

    $str .= "</p>\n";

    $str;
}

sub ShowPageLinkEachPage	# not used.
{
    local( $com, $num, $old, $rev, $vRev ) = @_;

    local( $nextOld ) = ( $old > $num )? ( $old - $num ) : 0;
    local( $backOld ) = ( $old + $num );

    local( $str );
    $str = '<p>';

    $MAX_PAGELINK = 5;

    if ( $SYS_REVERSE )
    {
	$str .= &TagA( "$PROGRAM?b=$BOARD&c=$com&num=$num&old=$old&rev=" . ( 1-$rev ), $H_REVERSE ) . ' ';
    }

    if ( $vRev )
    {
	if ( $num && ( $#DB_ID - $old - $num > 0 ))
	{
	    $str .= &TagA( "$PROGRAM?b=$BOARD&c=$com&num=$num&old=$backOld&rev=$rev", $H_TOP );
	}
	else
	{
	    $str .= $H_TOP;
	}

	local( $i );
	for ( $i = -$MAX_PAGELINK; $i <= +$MAX_PAGELINK; $i++ )
	{
	    $str .= ' ';
	    if ( $old - $i * $num <= $#DB_ID )
	    {
		$str .= &TagA( "$PROGRAM?b=$BOARD&c=$com&num=$num&old=" . ( $i*$num ) . "&rev=$rev", $i );
	    }
	    else
	    {
		$str .= $i;
	    }
	}
	$str .= ' ';

	if ( $old )
	{
	    $str .= &TagA( "$PROGRAM?b=$BOARD&c=$com&num=$num&old=$nextOld&rev=$rev", $H_BOTTOM );
	}
	else
	{
	    $str .= $H_BOTTOM;
	}
    }
    else
    {
	if ( $old )
	{
	    $str .= &TagA( "$PROGRAM?b=$BOARD&c=$com&num=$num&old=$nextOld&rev=$rev", $H_TOP );
	}
	else
	{
	    $str .= $H_TOP;
	}

	local( $i );
	$MAX_PAGELINK = 5;
	for ( $i = $MAX_PAGELINK; $i >= -$MAX_PAGELINK; $i-- )
	{
	    $str .= ' ';
	    if ( $old - $i * $num <= $#DB_ID )
	    {
		$str .= &TagA( "$PROGRAM?b=$BOARD&c=$com&num=$num&old=" . ( $i*$num ) . "&rev=$rev", $i );
	    }
	    else
	    {
		$str .= $i;
	    }
	}
	$str .= ' ';

	if ( $num && ( $#DB_ID - $old - $num > 0 ))
	{
	    $str .= &TagA( "$PROGRAM?b=$BOARD&c=$com&num=$num&old=$backOld&rev=$rev", $H_BOTTOM );
	}
	else
	{
	    $str .= $H_BOTTOM;
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

    local( $str );
    $str = '<p>';

    if ( $vRev )
    {
	if ( $num && ( $#DB_ID - $old - $num > 0 ))
	{
	    $str .= &TagA( "$PROGRAM?b=$BOARD&c=$com&num=$num&old=$backOld&rev=$rev", "$H_TOP$H_BACKART" );
	}
	else
	{
	    $str .= $H_NOBACKART;
	}
    }
    else
    {
	if ( $old )
	{
	    $str .= &TagA( "$PROGRAM?b=$BOARD&c=$com&num=$num&old=$nextOld&rev=$rev", "$H_TOP$H_NEXTART" );
	}
	else
	{
	    $str .= $H_NONEXTART;
	}
    }

    if ( $SYS_REVERSE )
    {
	$str .= ' // ' . &TagA( "$PROGRAM?b=$BOARD&c=$com&num=$num&old=$old&rev=" . ( 1-$rev ), $H_REVERSE );
    }

    $str .= "</p>\n";

    &cgiprint'Cache( $str );
}

sub ShowPageLinkBottom		# not used.
{
    local( $com, $num, $old, $rev, $vRev ) = @_;

    local( $nextOld ) = ( $old > $num )? ( $old - $num ) : 0;
    local( $backOld ) = ( $old + $num );

    local( $str );
    $str = '<p>';

    if ( $SYS_REVERSE )
    {
	$str .= &TagA( "$PROGRAM?b=$BOARD&c=$com&num=$num&old=$old&rev=" . ( 1-$rev ), $H_REVERSE ) . ' // ';
    }

    if ( $vRev )
    {
	if ( $old )
	{
	    $str .= &TagA( "$PROGRAM?b=$BOARD&c=$com&num=$num&old=$nextOld&rev=$rev", "$H_NEXTART$H_BOTTOM" );
	}
	else
	{
	    $str .= $H_NONEXTART;
	}
    }
    else
    {
	if ( $num && ( $#DB_ID - $old - $num > 0 ))
	{
	    $str .= &TagA( "$PROGRAM?b=$BOARD&c=$com&num=$num&old=$backOld&rev=$rev", "$H_BACKART$H_BOTTOM" );
	}
	else
	{
	    $str .= $H_NOBACKART;
	}
    }

    $str .= "</p>\n";

    &cgiprint'Cache( $str );
}



###
## ShowLinksToFollowedArticle - �����������ɽ��
#
# - SYNOPSIS
#	ShowLinksToFollowedArticle( *msg, @IdList );
#
# - ARGS
#	$msg		����ʸ����
#	@IdList		��ץ饤����ID�Υꥹ��(�Ť���ץ饤�ۤ������ˤ���)
#
# - DESCRIPTION
#	������������������롥
#
# - RETURN
#	�ʤ�
#
sub ShowLinksToFollowedArticle
{
    local( *msg, @IdList ) = @_;

    local( $Id, $Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name );

    # ���ꥸ�ʥ뵭��
    if ( $#IdList > 0 )
    {
	$Id = $IdList[$#IdList];
	( $Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name ) = &GetArticlesInfo( $Id );
	$msg .= "<br>\n<strong>$H_ORIG_TOP:</strong> " .
	    &GetFormattedTitle( $Id, $Aids, $Icon, $Subject, $Name, $Date, 0 );
    }

    # ������
    $Id = $IdList[0];
    ( $Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name ) = &GetArticlesInfo( $Id );
    $msg .= "<br>\n<strong>$H_ORIG:</strong> " .
	&GetFormattedTitle( $Id, $Aids, $Icon, $Subject, $Name, $Date, 0 );
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
    local( $board, $id ) = @_;
    local( $old ) = $id? &GetTitleOldIndex( $id ) : 0;

    if  ( $SYS_COMMAND_BUTTON )
    {
	local( %tags ) = ( 'b', $board, 'c', 'v', 'num', $DEF_TITLE_NUM, 'old',
	    $old );
	local( $str );
	&TagForm( *str, *tags, "$H_BACKTITLEREPLY", '', '' );
	&cgiprint'Cache( $str );

	if ( $SYS_F_R )
	{
	    %tags = ( 'b', $board, 'c', 'r', 'num', $DEF_TITLE_NUM, 'old',
		$old );
	    &TagForm( *str, *tags, "$H_BACKTITLEDATE", '', '' );
	    &cgiprint'Cache( $str );
	}
    }
    else
    {
	&cgiprint'Cache( "<p>", &TagA( "$PROGRAM?b=$board&c=v&num=$DEF_TITLE_NUM&old=$old", $H_BACKTITLEREPLY ), "</p>\n" );
	&cgiprint'Cache( "<p>", &TagA( "$PROGRAM?b=$board&c=r&num=$DEF_TITLE_NUM&old=$old", $H_BACKTITLEDATE ), "</p>\n" ) if ( $SYS_F_R );
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
    if ( $SYS_COMMAND_BUTTON && $BOARDLIST_URL =~ /$PROGRAM/ )
    {
	local( %tags ) = ( 'c', 'bl' );
	local( $str );
	&TagForm( *str, *tags, $H_BACKBOARD, '', '' );
	&cgiprint'Cache( $str );
    }
    else
    {
	&cgiprint'Cache( "<p>", &TagA( $BOARDLIST_URL, $H_BACKBOARD ), "</p>\n" );
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
	local( @cookieStr ) = ( "kb10info=" . join( $COLSEP, $cgi'TAGS{'name'},
	    $cgi'TAGS{'mail'}, $cgi'TAGS{'url'} ));
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

    local( $titleString ) = $BOARDNAME? "$SYSTEM_NAME - $BOARDNAME - $Title" :
	"$SYSTEM_NAME - $Title";
    local( $headerString ) = $BOARDNAME || $SYSTEM_NAME;

    local( $msg );
    $msg .= <<__EOF__;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN">
<html lang="ja">
<head>
<link rev="MADE" href="mailto:$MAINT">
<title>$titleString</title>
</head>
__EOF__

    $msg .= '<body';
    if ( $SYS_NETSCAPE_EXTENSION )
    {
	$msg .= " background=\"$BG_IMG\"" if $BG_IMG;
	$msg .= " bgcolor=\"$BG_COLOR\"" if $BG_COLOR;
	$msg .= " TEXT=\"$TEXT_COLOR\"" if $TEXT_COLOR;
	$msg .= " LINK=\"$LINK_COLOR\"" if $LINK_COLOR;
	$msg .= " ALINK=\"$ALINK_COLOR\"" if $ALINK_COLOR;
	$msg .= " VLINK=\"$VLINK_COLOR\"" if $VLINK_COLOR;
    }
    $msg .= ">\n";

    $msg .= <<__EOF__;
<h1>$headerString</h1>

<p>[
__EOF__

    $msg .= "$Message // \n";
    $msg .= "�ǿ�${H_MESG}ID: " . $DB_ID[$#DB_ID] . " // \n" if @DB_ID;
    $msg .= "����: " . &GetDateTimeFormatFromUtc( $^T );
    $msg .= <<__EOF__;
]</p>

__EOF__

    if ( $SYS_HEADER_MENU && ( $SYS_F_B || $BOARD ))
    {
	local( $select );
	$select .= "ɽ������: \n<select name=\"c\">\n";
	$select .= sprintf( "<option %s value=\"bl\">$H_BOARD����\n", ( $cgi'TAGS{'c'} eq 'bl' )? 'selected' : '' ) if $SYS_F_B;
	if ( $BOARD )
	{
	    $select .= sprintf( "<option %s value=\"v\">�ǿ�$H_SUBJECT����($H_REPLY��)\n", ( $cgi'TAGS{'c'} eq 'v' )? 'selected' : '' );
	    $select .= sprintf( "<option %s value=\"r\">�ǿ�$H_SUBJECT����(���ս�)\n", ( $cgi'TAGS{'c'} eq 'r' )? 'selected' : '' ) if $SYS_F_R;
	    $select .= sprintf( "<option %s value=\"vt\">�ǿ�$H_MESG����($H_REPLY��)\n", ( $cgi'TAGS{'c'} eq 'vt' )? 'selected' : '' );
	    $select .= sprintf( "<option %s value=\"l\">�ǿ�$H_MESG����(���ս�)\n", ( $cgi'TAGS{'c'} eq 'l' )? 'selected' : '' ) if $SYS_F_L;
	    $select .= sprintf( "<option %s value=\"s\">$H_MESG�θ���\n", ( $cgi'TAGS{'c'} eq 's' )? 'selected' : '' ) if $SYS_F_S;
	    $select .= sprintf( "<option %s value=\"n\">�����񤭹���\n", ( $cgi'TAGS{'c'} eq 'n' )? 'selected' : '' ) if $SYS_F_N;
	    $select .= sprintf( "<option %s value=\"i\">�Ȥ���$H_ICON����\n", ( $cgi'TAGS{'c'} eq 'i' )? 'selected' : '' ) if $SYS_ICON;
	}
	$select .= "</select>\n // ɽ�����: <input name=\"num\" type=\"text\" size=\"3\" value=\"" . ( $cgi'TAGS{'num'} || $DEF_TITLE_NUM ) . "\"> ";
	local( %tags ) = ( 'b', $BOARD );
	local( $str );
	&TagForm( *str, *tags, "ɽ��", 0, *select );
	$msg .= $str;
    }

    $msg .= "$H_HR\n";

    &cgiprint'Init;
    &cgiprint'Cache( $msg );
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
    # ��������ʬ���ѹ�����Τ�ּ�ͳ�פǤ����ä��Ƥ��������ꤢ��ޤ���
    local( $addr ) = "Maintenance: " . &TagA( "mailto:$MAINT", $MAINT_NAME ) . "<br>" . &TagA( "http://www.jin.gr.jp/~nahi/kb/", $PROGNAME ) . ": Copyright (C) 1995-2000 " . &TagA( "http://www.jin.gr.jp/~nahi/", "NAKAMURA Hiroshi" ) . ".";
    # �������ֲ�����ä�����פȤ��񤯤ȡ��ʤҤθ����򿯳����ơ�
    # GPL2�˰�ȿ���뤳�Ȥˤʤä��㤦�Τǵ���Ĥ��Ƥ͡�(^_^;

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
#	GetFormattedTitle( $id, $aids, $icon, $title, $name, $origDate, $flag);
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
#	$G_TITLE_STR���˲����롥���٤�Ȥ���Τǡ�local�򸺤餹���ᡥ����
#	���ʤ�ѥե����ޥ󥹤˸�����
#
# - RETURN
#	�ե����ޥåȤ���ʸ����
#
sub GetFormattedTitle
{
    local( $id, $aids, $icon, $title, $name, $origDate,	$flag ) = @_;

    $G_TITLE_STR = '';	# �����

    if ( $SYS_F_T && $flag&1 && $DB_FID{$id} )
    {
	local( $fId ) = $DB_FID{$id};
	$fId =~ s/^.*,//o;
	$G_TITLE_STR .= &TagA( "$PROGRAM?b=$BOARD&c=t&id=$fId",
	    $H_THREAD_ALL ) . ' ';
    }

    $G_TITLE_STR .= &TagMsgImg( $icon ) . " <small>$id.</small> " .
	&TagA( ( $flag&2 )? "$cgi'REQUEST_URI#a$id" :
	"$PROGRAM?b=$BOARD&c=e&id=$id",	$title || $id );

    if ( $SYS_F_T && $aids )
    {
	$G_TITLE_STR .= ' ' . &TagA( "$PROGRAM?b=$BOARD&c=t&id=$id",
	    $H_THREAD );
    }

    $G_TITLE_STR .= ' [' . ( $name || $MAINT_NAME ) . '] ' .
	&GetDateTimeFormatFromUtc( $origDate || &GetModifiedTime( $id,$BOARD));

    if ( $DB_NEW{$id} )
    {
	$G_TITLE_STR .= ' ' . &TagMsgImg( $H_NEWARTICLE );
    }

    $G_TITLE_STR;
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
#	TagMsgImg( $icon );
#
# - ARGS
#	$icon		�������󥿥���
#
# - DESCRIPTION
#	���᡼����ɽ���ѥ����˥ե����ޥåȤ��롥
#
# - RETURN
#	�ե����ޥåȤ���ʸ����
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
	return "<img src=\"$src\" alt=\"[$icon]\" width=\"$MSGICON_WIDTH\" height=\"$MSGICON_HEIGHT\" BORDER=\"0\">";
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
    $href =~ s/&/&amp;/go;
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

    $str = "<form action=\"$PROGRAM\" method=\"POST\">\n<p>\n";
    foreach ( keys( %tags ))
    {
	$str .= "<input name=\"$_\" type=\"hidden\" value=\"$tags{$_}\">\n";
    }
    $str .= $contents;
    $str .= "<input type=\"submit\" value=\"$submit\">\n";
    $str .= "<input type=\"reset\" value=\"$reset\">\n" if $reset;
    $str .= "</p>\n</form>\n";
}


###
## SendMail - �ᥤ������
#
# - SYNOPSIS
#	SendMail(
#	    $Name,	�ᥤ��������̾
#	    $EMail,	�ᥤ�������ԥᥤ�륢�ɥ쥹
#	    $Subject,	�ᥤ���Subjectʸ����
#	    $Message,	��ʸ
#	    $Id,	���Ѥ���ʤ鵭��ID; ���ʤ���ѥʥ�
#	    @To		����E-Mail addr.�Υꥹ��
#	)
#
# - DESCRIPTION
#	�ᥤ����������롥
#
# - RETURN
#	�ʤ�
#
sub SendMail
{
    local( $Name, $EMail, $Subject, $Message, $Id, @To ) = @_;

    local( $ExtensionHeader, @ArticleBody );

    $ExtensionHeader = "X-MLServer: $PROGNAME\n";
    $ExtensionHeader .= "X-Kb-System: $SYSTEM_NAME\n";
    if (( ! $SYS_MAILHEADBRACKET ) && $BOARDNAME && ($Id ne '' ))
    {
	$ExtensionHeader .= "X-Kb-Board: $BOARDNAME\nX-Kb-Articleid: $Id\n";
    }

    if ( $EMail eq '' )
    {
	# �ᥤ�륢�ɥ쥹̤���ϤˤĤ���������̾���ǽФ���
	$Name = ( $MAILFROM_LABEL || $MAINT_NAME );
	$EMail = $MAINT;
    }

    local( $SenderFrom, $SenderAddr ) = (( $MAILFROM_LABEL || $MAINT_NAME ),
	$MAINT );
    local( $stat, $errstr ) = &cgi'sendMail( $Name, $EMail, $SenderFrom,
	$SenderAddr, $Subject, $ExtensionHeader, $Message, $MAILTO_LABEL,
	@To );
    &Fatal( 9, "$BOARDNAME/$Id/$errstr" ) if ( !$stat );
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


######################################################################
# ���å�����ץ���ơ������


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
# - RETURN
#	�ʤ�
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
    &CheckIcon( *icon, $board ) if $SYS_ICON;

    # ��ʸ�ζ������å���
    &Fatal( 2, '' ) if ( $article eq '' );

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
# ����Ǥ�ɡ������Ƥ�Ȥ������Ȥ������ʤ��ϡ�
# ���ιԤ���Ƭ�Ρ�#�פ�ä��Ƥ���������(^_^;
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
	# <URL:>�ν���
	$article = &ArticleEncode( $article );
	$article =~ s/<URL:([^>][^>]*)>/&lt;URL:$1&gt;/gi;
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

    &Fatal( 2, '' ) if ( !$SYS_ALLOWNOICON && ( $str eq $H_NOICON ));
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
    &Fatal( 3, '' ) if ( $String =~ m/[\t\n]/o );
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
# - RETURN
#	�ʤ�
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
# - RETURN
#	�ʤ�
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

    local( $retArticle ) = $article;

    local( $url, $urlMatch, @cache );
    local( $tagStr, $quoteStr );
    while ( $article =~ m/<URL:([^>][^>]*)>/gi )
    {
	$url = $1;
	( $urlMatch = $url ) =~ s/([?+*^\\\[\]\|()])/\\$1/go;
	next if ( grep( /^$urlMatch$/, @cache ));
	push( @cache, $url );
	$quoteStr = "<URL:$url>";

	if ( $urlMatch =~ m/^kb:(.*)$/ )
	{
	    local( $artStr ) = $1;
	    if ( $artStr =~ m!^//.*$! )
	    {
		# not implemented now...
	    }
	    elsif ( $artStr =~ m!^([^/][^/]*)/(.*)$! )
	    {
		local( $boardInfo ) = &GetBoardInfo( $1 );
		$tagStr = &TagA( "$PROGRAM?b=$1&c=e&id=$2", $quoteStr )
		    if $boardInfo;
	    }
	    else
	    {
		$tagStr = &TagA( "$PROGRAM?b=$BOARD&c=e&id=$artStr",
		    $quoteStr );
	    }
	}
	elsif ( &IsUrl( $urlMatch ))
	{
	    $tagStr = &TagA( $url, $quoteStr );
	}
	else
	{
	    next;
	}

	$retArticle =~ s/<URL:$urlMatch>/$tagStr/gi;
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
# - RETURN
#	�ʤ�
#
sub PlainArticleToPreFormatted
{
    local( *Article ) = @_;
    $Article =~ s/\n*$//o;
    $Article =~ s/<URL:([^>][^>]*)>/__URL__$COLSEP$1$COLSEP/gi;
    $Article = &HTMLEncode( $Article );	# no tags are allowed.
    $Article =~ s/__URL__$COLSEP([^$COLSEP][^$COLSEP]*)$COLSEP/"<URL:" . &HTMLDecode( $1 ) . ">"/gie;
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
#	LockAll;
#	UnlockAll;
#	LockBoard;
#	UnlockBoard;
#
# - ARGS
#	�ʤ�
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


######################################################################
# �ǡ�������ץ���ơ������


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
# - RETURN
#	�ʤ�
#
$BOARD_DB_CACHE = 0;

sub DbCache
{
    return if $BOARD_DB_CACHE;

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
#	$MailRelay	�ɲä���������ᥤ��Ȥ���ή�����ɤ���
#
# - DESCRIPTION
#	����DB�˵������ɲä��롥
#
# - RETURN
#	�ʤ�
#
sub AddDBFile
{
    local( $Id, $Board, $Fid, $InputDate, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail, $MailRelay ) = @_;

    local( $dId, $dFid, $dAids, $dInputDate, $dSubject, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail, $mdName, $mdEmail, $mdInputDate, $mdSubject, $mdIcon, $mdId, $FidList, $FFid, @FollowMailTo, @FFid );

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
# - RETURN
#	�ʤ�
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
# - RETURN
#	�ʤ�
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
# - RETURN
#	�ʤ�
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
# - RETURN
#	�ʤ�
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
# - RETURN
#	�ʤ�
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
	print( DBTMP "$_\n" ) || &Fatal( 13, $TmpFile );
    }
    close DBTMP || &Fatal( 13, $TmpFile );
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

    open( ALIAS, ">$TmpFile" ) || &Fatal( 1, $TmpFile );
    printf( ALIAS "<!-- Kb-System-Id: %s/%s -->\n", $KB_VERSION, $KB_RELEASE )
	|| &Fatal( 13, $TmpFile );

    local( $Alias, $dbLine );
    foreach $Alias ( sort keys( %Name ))
    {
	if ( $Name{$Alias} )
	{
	    &GenTSV( *dbLine, ( $Alias, $Name{$Alias}, $Email{$Alias}, $Host{$Alias}, $URL{$Alias} ));
	    print( ALIAS "$dbLine\n" ) || &Fatal( 13, $TmpFile );
	}
    }
    close ALIAS || &Fatal( 13, $TmpFile );

    rename( $TmpFile, $USER_ALIAS_FILE )
	|| &Fatal( 14, "$TmpFile -&gt; $USER_ALIAS_FILE" );
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
# - RETURN
#	�ʤ�
#
sub GetAllBoardInfo
{
    local( *board, *boardName, *boardInfo ) = @_;

    local( $bId, $bName, $bInfo );
    open( ALIAS, "<$BOARD_ALIAS_FILE" ) || &Fatal( 1, $BOARD_ALIAS_FILE );
    while ( <ALIAS> )
    {
	next if ( /^\#/o || /^$/o );
	chop;
	( $bId, $bName, $bInfo ) = split( /\t/, $_, 3 );
	push( @board, $bId );
	$boardName{ $bId } = $bName;
	$boardInfo{ $bId } = $bInfo;
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
    local( $alias ) = @_;

    local( $dAlias, $dBoardName, $dBoardConf );

    open( ALIAS, "<$BOARD_ALIAS_FILE" ) || &Fatal( 1, $BOARD_ALIAS_FILE );
    while ( <ALIAS> )
    {
	next if ( /^\#/o || /^$/o );
	chop;
	( $dAlias, $dBoardName, $dBoardConf ) = split( /\t/, $_, 4 );
	if ( $alias eq $dAlias )
	{
	    close ALIAS;
	    return( $dBoardName, $dBoardConf );
	}
    }
    close ALIAS;

    &Fatal( 11, $alias );
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
# - RETURN
#	�ʤ�
#
$ICON_DB_CACHE = '';

sub CacheIconDb
{
    local( $board ) = @_;
    return if ( $ICON_DB_CACHE eq $board );

    local( $FileName, $IconTitle, $IconHelp );

    @ICON_TITLE = %ICON_FILE = %ICON_HELP = ();
    open( ICON, &GetIconPath( "$board.$ICONDEF_POSTFIX" ))
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

    $ICON_DB_CACHE = $board;		# cached
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
    $KB_RESOURCE_URL? "$KB_RESOURCE_URL$ICON_DIR/$file" : "$ICON_DIR/$file";
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
    &CacheIconDb( $board ) if ( $ICON_DB_CACHE ne $board );

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
