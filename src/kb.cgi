#!/usr/local/bin/perl5
#
# $Id: kb.cgi,v 5.3 1997-09-12 14:30:07 nakahiro Exp $


# KINOBOARDS: Kinoboards Is Network Opened BOARD System
# Copyright (C) 1995, 96, 97 NAKAMURA Hiroshi.
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


# �Ķ��ѿ��򽦤�
$TIME = time;			# �ץ���൯ư����(UTC)
$SERVER_NAME = $ENV{'SERVER_NAME'};
$SERVER_PORT = $ENV{'SERVER_PORT'};
$REMOTE_HOST = $ENV{'REMOTE_HOST'};
$SCRIPT_NAME = $ENV{'SCRIPT_NAME'};
$PATH_INFO = $ENV{'PATH_INFO'};
$PATH_TRANSLATED = $ENV{'PATH_TRANSLATED'};

# ����ѿ������
$[ = 0;				# zero origined
$| = 1;				# pipe flushed
($CGIPROG_NAME = $SCRIPT_NAME) =~ s!^(.*/)!!o;
$SYSDIR_NAME = (($PATH_INFO) ? "$PATH_INFO/" : "$1");
$HEADER_FILE = ($CGIPROG_NAME =~ m/^(.*)\..*$/o) ? "$1.ph" : 'kb.ph';
$SCRIPT_URL = "http://$SERVER_NAME$SERVER_PORT_STRING$SCRIPT_NAME$PATH_INFO";
$PROGRAM = (($PATH_INFO) ? "$SCRIPT_NAME$PATH_INFO" : "$CGIPROG_NAME");
$SERVER_PORT_STRING = '';
$KB_VERSION = '1.0';
$KB_RELEASE = '5.0';

# ���󥯥롼�ɥե�������ɤ߹���
if ($PATH_INFO && (-s "$HEADER_FILE")) { require($HEADER_FILE); }
if ($PATH_TRANSLATED ne '') { chdir($PATH_TRANSLATED); }
if (-s "$HEADER_FILE") {
    require($HEADER_FILE);
} else {
    die("cannot find configuration file: `$HEADER_FILE'");
}
require('cgi.pl');
require('jcode.pl');

# ���󥯥롼�ɥե����������˱���������ѿ�������
$SYS_F_MT = ($SYS_F_D || $SYS_F_AM || $SYS_F_MV);
if (($SERVER_PORT != 80) && ($SYS_PORTNO == 1)) {
    $SERVER_PORT_STRING = ":$SERVER_PORT";
}
if ($TIME_ZONE) { $ENV{'TZ'} = $TIME_ZONE; }
if ($BOARDLIST_URL eq '-') { $BOARDLIST_URL = "$PROGRAM?c=bl"; }
$ADDRESS = sprintf("Maintenance: <a href=\"mailto:%s\">%s</a><br><a href=\"http://www.kinotrope.co.jp/~nakahiro/kb10.shtml\">KINOBOARDS/%s R%s</a>: Copyright (C) 1995, 96, 97 <a href=\"http://www.kinotrope.co.jp/~nakahiro/\">NAKAMURA Hiroshi</a>.", $MAINT, $MAINT_NAME, $KB_VERSION, $KB_RELEASE);

# �ǥ��쥯�ȥ�
$ICON_DIR = 'icons';				# ��������ǥ��쥯�ȥ�
# �ե�����
$BOARD_ALIAS_FILE = 'kinoboards';		# �Ǽ���DB
$CONF_FILE_NAME = '.kbconf';			# �Ǽ�����configuratin�ե�����
$ARRIVEMAIL_FILE_NAME = '.kbmail';		# �Ǽ����̿����ᥤ��������DB
$BOARD_FILE_NAME = '.board';			# �����ȥ�ꥹ�ȥإå�DB
$DB_FILE_NAME = '.db';				# ����DB
$ARTICLE_NUM_FILE_NAME = '.articleid';		# �����ֹ�DB
$USER_ALIAS_FILE = 'kinousers';			# �桼��DB
$DEFAULT_ICONDEF = 'all.idef';			# ��������DB
$LOCK_FILE = '.lock.kb';			# ��å��ե�����
# Suffix
$TMPFILE_SUFFIX = 'tmp';			# DB�ƥ�ݥ��ե������Suffix
$ICONDEF_POSTFIX = 'idef';			# ��������DB�ե������Suffix

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

# �����ʥ�ϥ�ɥ�
$SIG{'HUP'} = $SIG{'INT'} = $SIG{'QUIT'} = $SIG{'TERM'} = $SIG{'TSTP'} = 'DoKill';
sub DoKill { &cgi'unlock($LOCK_FILE); exit(1); }


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
&cgi'lock($LOCK_FILE) || &Fatal(999, '');

MAIN: {

    local($BoardConfFile, $Command, $Com);

    # ɸ������(POST)�ޤ��ϴĶ��ѿ�(GET)�Υǥ����ɡ�
    &cgi'Decode;

    # ���ˤ˻Ȥ��Τ�����ѿ���Ȥ�(���ʤ�)
    $BOARDNAME = &GetBoardInfo($BOARD = $cgi'TAGS{'b'});
    # ������͡�
    if ($BOARDNAME =~ m!/!o) { &Fatal(11, $BOARDNAME); }

    # �Ǽ��ĸ�ͭ���åƥ��󥰤��ɤ߹���
    $BoardConfFile = &GetPath($BOARD, $CONF_FILE_NAME);
    if (-s "$BoardConfFile") { require("$BoardConfFile"); }

    # DB������ѿ��˥���å���
    if ($BOARD) { &DbCash($BOARD); }

    # �ͤ����
    $Command = $cgi'TAGS{'c'};
    $Com = $cgi'TAGS{'com'};

    # ���ޥ�ɥ����פˤ��ʬ��
    &ShowArticle,	last if ($Command eq 'e');
    &ThreadArticle,	last if ($SYS_F_T && ($Command eq 't'));
    &Entry(0),		last if ($SYS_F_N && ($Command eq 'n'));
    &Entry(1),		last if ($SYS_F_N && ($Command eq 'f'));
    &Entry(2),		last if ($SYS_F_N && ($Command eq 'q'));
    &Preview,		last if ($SYS_F_N && ($Command eq 'p') && ($Com ne 'x'));
    &Thanks,		last if ($SYS_F_N && ($Command eq 'x'));
    &Thanks,		last if ($SYS_F_N && ($Command eq 'p') && ($Com eq 'x'));
    &ViewTitle(0),	last if ($Command eq 'v');
    &SortArticle,	last if ($SYS_F_R && ($Command eq 'r'));
    &NewArticle,	last if ($SYS_F_L && ($Command eq 'l'));
    &SearchArticle,	last if ($SYS_F_S && ($Command eq 's'));
    &ShowIcon,		last if ($Command eq 'i');
    &AliasNew,		last if ($SYS_ALIAS && ($Command eq 'an'));
    &AliasMod,		last if ($SYS_ALIAS && ($Command eq 'am'));
    &AliasDel,		last if ($SYS_ALIAS && ($Command eq 'ad'));
    &AliasShow,		last if ($SYS_ALIAS && ($Command eq 'as'));
    &BoardList,		last if ($SYS_F_B && ($Command eq 'bl'));

    # �ʲ��ϴ�����
    &ViewTitle(1),	last if ($SYS_F_MT && ($Command eq 'vm'));
    &DeletePreview,	last if ($SYS_F_D && ($Command eq 'dp'));
    &DeleteExec(0),	last if ($SYS_F_D && ($Command eq 'de'));
    &DeleteExec(1),	last if ($SYS_F_D && ($Command eq 'det'));
    &ArriveMailEntry,   last if ($SYS_F_AM && ($Command eq 'mp'));
    &ArriveMailExec,    last if ($SYS_F_AM && ($Command eq 'me'));
    &ViewTitle(2),	last if ($SYS_F_MV && ($Command eq 'ct'));
    &ViewTitle(3),	last if ($SYS_F_MV && ($Command eq 'ce'));
    &ViewTitle(4),	last if ($SYS_F_MV && ($Command eq 'mvt'));
    &ViewTitle(5),	last if ($SYS_F_MV && ($Command eq 'mve'));

    # �ǥե����

    if ($Command ne '') {
	&Fatal(99, '');
    } else {
	print("huh... what's up? running under any shell?\n");
    }

}


&cgi'unlock($LOCK_FILE);
exit(0);


######################################################################
# �桼�����󥿥ե���������ץ���ơ������(����)
#
# UI�ǥ��쥯�ȥ�˼�����Ƥ���UI�μ����⥸�塼���require���롥
# ���פʥץ����򥳥�ѥ��뤷�ʤ��褦�ˤ��뤿�ᡥ
# �ƴؿ��Υ�ե���󥹤ϡ�UI�ǥ��쥯�ȥ���γƥե�����򻲾ȤΤ��ȡ�

### BoardList - �Ǽ��İ�����ɽ��
sub BoardList { require(&GetPath('UI', 'BoardList.pl')); }

### Entry - �񤭹��߲��̤�ɽ��
sub Entry {
    ($gVarQuoteFlag) = @_;
    require(&GetPath('UI', 'Entry.pl'));
    undef($gVarQuoteFlag);
}

### Preview - �ץ�ӥ塼���̤�ɽ��
sub Preview { require(&GetPath('UI', 'Preview.pl')); }

### Thanks - ��Ͽ����̤�ɽ��
sub Thanks { require(&GetPath('UI', 'Thanks.pl')); }

### ShowArticle - ñ�쵭����ɽ��
sub ShowArticle { require(&GetPath('UI', 'ShowArticle.pl')); }

### ThreadArticle - �ե�������������ɽ����
sub ThreadArticle { require(&GetPath('UI', 'ThreadArticle.pl')); }

### ShowIcon - ��������ɽ������
sub ShowIcon { require(&GetPath('UI', 'ShowIcon.pl')); }

### SortArticle - ���ս�˥�����
sub SortArticle { require(&GetPath('UI', 'SortArticle.pl')); }

### ViewTitle - ����å���ɽ��
sub ViewTitle {
    ($gVarComType) = @_;
    require(&GetPath('UI', 'ViewTitle.pl'));
    undef($gVarComType);
}

### NewArticle - ������������ޤȤ��ɽ��
sub NewArticle { require(&GetPath('UI', 'NewArticle.pl')); }

### SearchArticle - �����θ���(ɽ�����̤κ���)
sub SearchArticle { require(&GetPath('UI', 'SearchArticle.pl')); }

### AliasNew - �����ꥢ������Ͽ���ѹ����̤�ɽ��
sub AliasNew { require(&GetPath('UI', 'AliasNew.pl')); }

### AliasMod - �桼�������ꥢ������Ͽ/�ѹ�
sub AliasMod { require(&GetPath('UI', 'AliasMod.pl')); }

### AliasDel - �桼�������ꥢ���κ��
sub AliasDel { require(&GetPath('UI', 'AliasDel.pl')); }

### AliasShow - �桼�������ꥢ�����Ȳ��̤�ɽ��
sub AliasShow { require(&GetPath('UI', 'AliasShow.pl')); }

### DeletePreview - ��������γ�ǧ
sub DeletePreview { require(&GetPath('UI', 'DeletePreview.pl')); }

### DeleteExec - �����κ��
sub DeleteExec {
    ($gVarThreadFlag) = @_;
    require(&GetPath('UI', 'DeleteExec.pl'));
    undef($gVarThreadFlag);
}

### ArriveMailEntry - �ᥤ�뼫ư�ۿ���λ���
sub ArriveMailEntry { require(&GetPath('UI', 'ArriveMailEntry.pl')); }

### ArriveMailExec - �ᥤ�뼫ư�ۿ��������
sub ArriveMailExec { require(&GetPath('UI', 'ArriveMailExec.pl')); }

### Fatal - ���顼ɽ��
sub Fatal {
    ($gVarFatalNo, $gVarFatalInfo) = @_;
    require(&GetPath('UI', 'Fatal.pl'));
    undef($gVarFatalNo, $gVarFatalInfo);
}

### ArriveMail - ���������夷�����Ȥ�ᥤ��
sub ArriveMail {
    ($gName, $gSubject, $gId, @gTo) = @_;
    require(&GetPath('UI', 'ArriveMail.pl'));
    undef($gName, $gSubject, $gId, @gTo);
}

### FollowMail - ȿ�������ä����Ȥ�ᥤ��
sub FollowMail {
    ($gName, $gDate, $gSubject, $gId, $gFname, $gFsubject, $gFid, @gTo) = @_;
    require(&GetPath('UI', 'FollowMail.pl'));
    undef($gName, $gDate, $gSubject, $gId, $gFname, $gFsubject, $gFid, @gTo);
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
sub ViewOriginalArticle {
    local($Id, $CommandFlag, $OriginalFlag) = @_;
    local($Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $PrevId, $NextId, $Num, $InputDate, @ArticleBody);

    ($Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url) = &GetArticlesInfo($Id);

    foreach ($[ .. $#DB_ID) { $Num = $_, last if ($DB_ID[$_] eq $Id); }
    $PrevId = $DB_ID[$Num - 1] if ($Num > $[);
    $NextId = $DB_ID[$Num + 1];

    # ���ޥ��ɽ��?
    if ($CommandFlag && $SYS_COMMAND) {

	&cgiprint'Cache("<p>\n");

	if ($SYS_COMICON == 2) {

	    if ($SYS_F_B) {
		&cgiprint'Cache("<a href=\"$BOARDLIST_URL\"><img src=\"$ICON_BLIST\" alt=\"$H_BACKBOARD\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\">$H_BACKBOARD</a>\n");
	    }

	    &cgiprint'Cache(" | <a href=\"$PROGRAM?b=$BOARD&c=v&num=$DEF_TITLE_NUM\"><img src=\"$ICON_TLIST\" alt=\"$H_BACKTITLE\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\">$H_BACKTITLE</a>\n");

	    if ($PrevId ne '') {
		&cgiprint'Cache(" | <a href=\"$PROGRAM?b=$BOARD&c=e&id=$PrevId\"><img src=\"$ICON_PREV\" alt=\"$H_PREVARTICLE\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\">$H_PREVARTICLE</a>\n");
	    } else {
		&cgiprint'Cache(" | <img src=\"$ICON_PREV\" alt=\"$H_PREVARTICLE\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\">$H_PREVARTICLE\n");

		if ($NextId ne '') {
		    &cgiprint'Cache(" | <a href=\"$PROGRAM?b=$BOARD&c=e&id=$NextId\"><img src=\"$ICON_NEXT\" alt=\"$H_NEXTARTICLE\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\">$H_NEXTARTICLE</a>\n");
		} else {
		    &cgiprint'Cache(" | <img src=\"$ICON_NEXT\" alt=\"$H_NEXTARTICLE\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\">$H_NEXTARTICLE\n");
		}
	    }

	    if ($SYS_F_T) {
		if ($Aids ne '') {
		    &cgiprint'Cache(" | <a href=\"$PROGRAM?b=$BOARD&c=t&id=$Id\"><img src=\"$ICON_THREAD\" alt=\"$H_READREPLYALL\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\">$H_READREPLYALL</a>\n");
		} else {
		    &cgiprint'Cache(" | <img src=\"$ICON_THREAD\" alt=\"$H_READREPLYALL\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\">$H_READREPLYALL\n");
		}
	    }

	    if ($SYS_F_N) {
		&cgiprint'Cache(<<__EOF__);
 | <a href="$PROGRAM?b=$BOARD&c=n"><img src="$ICON_WRITENEW" alt="$H_POSTNEWARTICLE" width="$COMICON_WIDTH" height="$COMICON_HEIGHT" BORDER="0">$H_POSTNEWARTICLE</a>
 | <a href="$PROGRAM?b=$BOARD&c=f&id=$Id"><img src="$ICON_FOLLOW" alt="$H_REPLYTHISARTICLE" width="$COMICON_WIDTH" height="$COMICON_HEIGHT" BORDER="0">$H_REPLYTHISARTICLE</a>
 | <a href="$PROGRAM?b=$BOARD&c=q&id=$Id"><img src="$ICON_QUOTE" alt="$H_REPLYTHISARTICLEQUOTE" width="$COMICON_WIDTH" height="$COMICON_HEIGHT" BORDER="0">$H_REPLYTHISARTICLEQUOTE</a>
__EOF__
	    }

	    &cgiprint'Cache(" | <a href=\"$PROGRAM?b=$BOARD&c=i&type=article\"><img src=\"$ICON_HELP\" alt=\"?\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\">?</a>\n");

	} elsif ($SYS_COMICON == 1) {

	    if ($SYS_F_B) {
		&cgiprint'Cache("<a href=\"$BOARDLIST_URL\"><img src=\"$ICON_BLIST\" alt=\"$H_BACKBOARD\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\"></a>\n");
	    }

	    &cgiprint'Cache("<a href=\"$PROGRAM?b=$BOARD&c=v&num=$DEF_TITLE_NUM\"><img src=\"$ICON_TLIST\" alt=\"$H_BACKTITLE\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\"></a>\n");

	    if ($PrevId ne '') {
		&cgiprint'Cache("<a href=\"$PROGRAM?b=$BOARD&c=e&id=$PrevId\"><img src=\"$ICON_PREV\" alt=\"$H_PREVARTICLE\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\"></a>\n");
	    } else {
		&cgiprint'Cache("<img src=\"$ICON_PREV\" alt=\"$H_PREVARTICLE\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\">\n");
	    }

	    if ($NextId ne '') {
		&cgiprint'Cache("<a href=\"$PROGRAM?b=$BOARD&c=e&id=$NextId\"><img src=\"$ICON_NEXT\" alt=\"$H_NEXTARTICLE\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\"></a>\n");
	    } else {
		&cgiprint'Cache("<img src=\"$ICON_NEXT\" alt=\"$H_NEXTARTICLE\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\">\n");
	    }

	    if ($SYS_F_T) {
		if ($Aids ne '') {
		    &cgiprint'Cache("<a href=\"$PROGRAM?b=$BOARD&c=t&id=$Id\"><img src=\"$ICON_THREAD\" alt=\"$H_READREPLYALL\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\"></a>\n");
		} else {
		    &cgiprint'Cache("<img src=\"$ICON_THREAD\" alt=\"$H_READREPLYALL\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\">\n");
		}
	    }

	    &cgiprint'Cache(" // \n");

	    if ($SYS_F_N) {
		&cgiprint'Cache(<<__EOF__);
<a href="$PROGRAM?b=$BOARD&c=n"><img src="$ICON_WRITENEW" alt="$H_POSTNEWARTICLE" width="$COMICON_WIDTH" height="$COMICON_HEIGHT" BORDER="0"></a>
<a href="$PROGRAM?b=$BOARD&c=f&id=$Id"><img src="$ICON_FOLLOW" alt="$H_REPLYTHISARTICLE" width="$COMICON_WIDTH" height="$COMICON_HEIGHT" BORDER="0"></a>
<a href="$PROGRAM?b=$BOARD&c=q&id=$Id"><img src="$ICON_QUOTE" alt="$H_REPLYTHISARTICLEQUOTE" width="$COMICON_WIDTH" height="$COMICON_HEIGHT" BORDER="0"></a>
__EOF__
	    }

	    &cgiprint'Cache(" // \n");

	    &cgiprint'Cache("<a href=\"$PROGRAM?b=$BOARD&c=i&type=article\"><img src=\"$ICON_HELP\" alt=\"?\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\"></a>\n");

	} else {

	    if ($SYS_F_B) {
		&cgiprint'Cache("<a href=\"$BOARDLIST_URL\">$H_BACKBOARD</a>\n");
	    }

	    &cgiprint'Cache(" | <a href=\"$PROGRAM?b=$BOARD&c=v&num=$DEF_TITLE_NUM\">$H_BACKTITLE</a>\n");

	    if ($PrevId ne '') {
		&cgiprint'Cache(" | <a href=\"$PROGRAM?b=$BOARD&c=e&id=$PrevId\">$H_PREVARTICLE</a>\n");
	    } else {
		&cgiprint'Cache(" | $H_PREVARTICLE\n");
	    }

	    if ($NextId ne '') {
		&cgiprint'Cache(" | <a href=\"$PROGRAM?b=$BOARD&c=e&id=$NextId\">$H_NEXTARTICLE</a>\n");
	    } else {
		&cgiprint'Cache(" | $H_NEXTARTICLE\n");
	    }

	    if ($SYS_F_T) {
		if ($Aids ne '') {
		    &cgiprint'Cache(" | <a href=\"$PROGRAM?b=$BOARD&c=t&id=$Id\">$H_READREPLYALL</a>");
		} else {
		    &cgiprint'Cache(" | $H_READREPLYALL");
		}
	    }

	    if ($SYS_F_N) {
		&cgiprint'Cache(<<__EOF__);
 | <a href="$PROGRAM?b=$BOARD&c=n">$H_POSTNEWARTICLE</a>
 | <a href="$PROGRAM?b=$BOARD&c=f&id=$Id">$H_REPLYTHISARTICLE</a>
 | <a href="$PROGRAM?b=$BOARD&c=q&id=$Id">$H_REPLYTHISARTICLEQUOTE</a>
__EOF__
	    }

	}

	&cgiprint'Cache("</p>\n");

    }

    &cgiprint'Cache("<p>\n");

    # �ܡ���̾�ȵ����ֹ桤��
    if (($Icon eq $H_NOICON) || ($Icon eq '')) {
	&cgiprint'Cache("<strong>$H_SUBJECT</strong>: <strong>$Id .</strong> $Subject");
    } else {
	&cgiprint'Cache(sprintf("<strong>$H_SUBJECT</strong>: <strong>$Id .</strong> <img src=\"%s\" alt=\"$Icon \" width=\"$MSGICON_WIDTH\" height=\"$MSGICON_HEIGHT\">$Subject", &GetIconUrlFromTitle($Icon, $BOARD)));
    }

    # ��̾��
    if (($Url eq '') || ($Url eq 'http://')) {
	# ��http://���ä���פȤ����Τϵ�С������ؤ��н补���Τ����������ͽ�ꡥ
        # URL���ʤ����
        &cgiprint'Cache("<br>\n<strong>$H_FROM</strong>: $Name");
    } else {
        # URL��������
        &cgiprint'Cache("<br>\n<strong>$H_FROM</strong>: <a href=\"$Url\">$Name</a>");
    }

    # �ᥤ��
    if ($Email ne '') {
	&cgiprint'Cache(" <a href=\"mailto:$Email\">&lt;$Email&gt;</a>");
    }

    # �ޥ���
    if ($SYS_SHOWHOST) {
	&cgiprint'Cache("<br>\n<strong>$H_HOST</strong>: $RemoteHost");
    }

    # �����
    $InputDate = &GetDateTimeFormatFromUtc($Date);
    &cgiprint'Cache("<br>\n<strong>$H_DATE</strong>: $InputDate");

    # ȿ����(���Ѥξ��)
    if ($OriginalFlag && ($Fid ne '')) {
	&ShowLinksToFollowedArticle(split(/,/, $Fid));
    }

    # �ڤ���
    &cgiprint'Cache("</p>\n$H_LINE\n");

    # ���������
    &GetArticleBody($Id, $BOARD, *ArticleBody);
    foreach(@ArticleBody) { &cgiprint'Cache($_); }

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
sub ThreadArticleMain {
    local($SubjectOnly, $Head, @Tail) = @_;

    # �������פ����������Τ�Τ���
    if ($SubjectOnly) {

	if ($Head eq '(') {
	    &cgiprint'Cache("<ul>\n");
	} elsif ($Head eq ')') {
	    &cgiprint'Cache("</ul>\n");
	} else {
	    local($dFid, $dAids, $dDate, $dSubject, $dIcon, $dRemoteHost, $dName) = &GetArticlesInfo($Head);
	    &cgiprint'Cache("<li>" . &GetFormattedTitle($Head, $BOARD, $dAids, $dIcon, $dSubject, $dName, $dDate) . "\n");
	}

    } else {

	if (($Head ne '(') && ($Head ne ')')) {
	    # ��������ɽ��(���ޥ���դ�, �������ʤ�)
	    &cgiprint'Cache("<hr>\n");
	    &ViewOriginalArticle($Head, 1, 0);
	}

    }

    # �Ƶ�
    if (@Tail) {
	&ThreadArticleMain($SubjectOnly, @Tail);
    }

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
sub QuoteOriginalArticle {
    local($Id) = @_;
    local($Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $pFid, $pAids, $pDate, $pSubject, $pIcon, $pRemoteHost, $pName, $QMark, @ArticleBody);

    # ����������μ���
    ($Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name) = &GetArticlesInfo($Id);

    # �������Τ���˸���������
    if ($Fid) {
	$Fid =~ s/,.*$//o;
	($pFid, $pAids, $pDate, $pSubject, $pIcon, $pRemoteHost, $pName) = &GetArticlesInfo($Fid);
    }

    # ����
    &GetArticleBody($Id, $BOARD, *ArticleBody);
    foreach(@ArticleBody) {
	s/[\&\"]//go;		# ���ѤΤ�����Ѵ�
	s/<[^>]*>//go;		# ���ѤΤ�����Ѵ�

	# �ǥե���Ȥΰ���ʸ����ϡ�̾���� + �� ] ��
	$QMark = "${Name}$DEFAULT_QMARK";

	# ��ʸ�Τ�����������ʬ�ˤϡ������˰���ʸ�����Ťͤʤ�
	# ���Ԥˤ��פ�ʤ�
	if ((/^$/o) || (/^$pName\s*$DEFAULT_QMARK/)) { $QMark = ''; }

	# ����ʸ�����ɽ��
	&cgiprint'Cache(sprintf("%s%s", $QMark, $_));
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
sub QuoteOriginalArticleWithoutQMark {
    local($Id) = @_;
    local(@ArticleBody);

    &GetArticleBody($Id, $BOARD, *ArticleBody);
    foreach(@ArticleBody) {
	s/[\&\"]//go;		# ���ѤΤ�����Ѵ�
	s/<[^>]*>//go;		# ���ѤΤ�����Ѵ�
	&cgiprint'Cache($_);
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
sub BoardHeader {
    local($Type) = @_;
    local(@BoardHeader);

    &GetBoardHeader($BOARD, *BoardHeader);
    foreach(@BoardHeader) { &cgiprint'Cache($_); }

    if ($SYS_F_MT && ($Type eq 'normal')) {
	&cgiprint'Cache(<<__EOF__);
<p>
<ul>
<li><a href="$PROGRAM?c=vm&b=$BOARD&num=$DEF_TITLE_NUM">�����ѤΥ����ȥ�������̤�</a>
</ul>
</p>
__EOF__
    } elsif ($Type eq 'maint') {
	&cgiprint'Cache("<p>\n<ul>\n");
	if ($SYS_F_AM) {
	    &cgiprint'Cache("<li><a href=\"$PROGRAM?c=mp&b=$BOARD\">��ư�ᥤ���ۿ�������ꤹ��</a>\n");
	}
	&cgiprint'Cache("<li><a href=\"$PROGRAM?c=v&b=$BOARD&num=$DEF_TITLE_NUM\">�̾�Υ����ȥ������</a>\n</ul>\n</p>\n");
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
sub ShowLinksToFollowedArticle {
    local(@IdList) = @_;
    local($Id, $Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name);

    # ���ꥸ�ʥ뵭��
    if ($#IdList > 0) {
	$Id = $IdList[$#IdList];
	($Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name) = &GetArticlesInfo($Id);
	&cgiprint'Cache("<br>\n<strong>$H_ORIG_TOP:</strong> " . &GetFormattedTitle($Id, $BOARD, $Aids, $Icon, $Subject, $Name, $Date));
    }

    # ������
    $Id = $IdList[0];
    ($Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name) = &GetArticlesInfo($Id);
    &cgiprint'Cache("<br>\n<strong>$H_ORIG:</strong> " . &GetFormattedTitle($Id, $BOARD, $Aids, $Icon, $Subject, $Name, $Date));

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
sub PrintButtonToTitleList {
    local($Board) = @_;

    &cgiprint'Cache(<<__EOF__);
<form action="$PROGRAM" method="POST">
<input name="b" type="hidden" value="$Board">
<input name="c" type="hidden" value="v">
<input name="num" type="hidden" value="$DEF_TITLE_NUM">
<input type="submit" value="$H_BACKTITLE">
</form>
__EOF__
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
sub PrintButtonToBoardList {

    &cgiprint'Cache(<<__EOF__);
<form action="$BOARDLIST_URL" method="GET">
<input type="submit" value="$H_BACKBOARD">
</form>
__EOF__
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
sub MsgHeader {
    local($Title, $Message, $LastModified) = @_;
    
    &cgi'Header($LastModified);

    &cgiprint'Init;
    &cgiprint'Cache(<<__EOF__);
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML i18n//EN">
<html>
<head>
<title>$Title</title>
<base href="http://$SERVER_NAME$SERVER_PORT_STRING$SYSDIR_NAME">
</head>
__EOF__

    &cgiprint'Cache("<body");
    if ($SYS_NETSCAPE_EXTENSION) {
	&cgiprint'Cache(" background=\"$BG_IMG\"") if $BG_IMG;
	&cgiprint'Cache(" bgcolor=\"$BG_COLOR\"") if $BG_COLOR;
	&cgiprint'Cache(" TEXT=\"$TEXT_COLOR\"") if $TEXT_COLOR;
	&cgiprint'Cache(" LINK=\"$LINK_COLOR\"") if $LINK_COLOR;
	&cgiprint'Cache(" ALINK=\"$ALINK_COLOR\"") if $ALINK_COLOR;
	&cgiprint'Cache(" VLINK=\"$VLINK_COLOR\"") if $VLINK_COLOR;
    }
    &cgiprint'Cache(">\n");

    &cgiprint'Cache(<<__EOF__);
<h1>$Message</h1>
<hr>
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
sub MsgFooter {

    &cgiprint'Cache(<<__EOF__);
<hr>
<address>
$ADDRESS
</address>
</body>
</html>
__EOF__

    &cgiprint'Flush;

}


###
## SendMail - �ᥤ������
#
# - SYNOPSIS
#	SendMail($Subject, $Message, $Id, @To);
#
# - ARGS
#	$Subject	�ᥤ���Subjectʸ����(���ܸ������ʤ��褦��!)
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
sub SendMail {
    local($Subject, $Message, $Id, @To) = @_;
    local($ExtensionHeader, @ArticleBody);

    # �ղåإå�������
    $ExtensionHeader = "X-Kb-System: $SYSTEM_NAME\n";
    if ($BOARDNAME && ($Id ne '')) {
	$ExtensionHeader .= "X-Kb-Board: $BOARDNAME\nX-Kb-Articleid: $Id\n";
    }

    # ���ѵ���
    if ($Id ne '') {

	# ���ڤ���
	$Message .= "\n--------------------\n";

	# ����
	&GetArticleBody($Id, $BOARD, *ArticleBody);
	foreach(@ArticleBody) {
	    s/<[^>]*>//go;	# �������פ�ʤ�
	    if ($_ ne '') { $Message .= &HTMLDecode($_); }
	}
    }

    # ��������
    &Fatal(9, '') unless (&cgi'SendMail($MAINT_NAME, $MAINT, $Subject, $ExtensionHeader, $Message, @To));

}


######################################################################
# ���ץꥱ��������ǥ륤��ץ���ơ������


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
sub MakeNewArticle {
    local($Board, $Id, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail) = @_;
    local($ArticleId);

    # ���Ϥ��줿��������Υ����å�
    $Article = &CheckArticle($Board, $TextType, *Name, *Email, *Url, *Subject, *Icon, $Article);

    # �����������ֹ�����(�ޤ������ֹ�������Ƥʤ�)
    $ArticleId = &GetNewArticleId($Board);

    # �����Υե�����κ���
    &MakeArticleFile($TextType, $Article, $ArticleId, $Board);

    # �����������ֹ��񤭹���
    &WriteArticleId($ArticleId, $Board);

    # DB�ե��������Ƥ��줿�������ɲ�
    # �̾�ε������Ѥʤ�ID
    &AddDBFile($ArticleId, $Board, $Id, $TIME, $Subject, $Icon, $REMOTE_HOST, $Name, $Email, $Url, $Fmail);

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
sub SearchArticleKeyword {
    local($Id, $Board, @KeyList) = @_;
    local(@NewKeyList, $Line, $Return, $Code, $ConvFlag, @ArticleBody);

    $ConvFlag = ($Id !~ /^\d+$/);

    &GetArticleBody($Id, $Board, *ArticleBody);
    foreach(@ArticleBody) {
	$Line = $_;

	# �������Ѵ�
	if ($ConvFlag) {
	    $Code = &jcode'getcode(*Line);
	    &jcode'convert(*Line, 'euc', $Code, 'z');
	}

	# ����
	@NewKeyList = ();
	foreach (@KeyList) {
	    if ($Line =~ /$_/i) {
		# �ޥå�����! 1���ܤʤ�Ф��Ȥ�
		$Return = $Line unless $Return;
	    } else {
		# �ޤ�õ���ʤ���ġ�
		push(@NewKeyList, $_);
	    }
	}
	# ���ʤ�ȴ����
	last unless (@KeyList = @NewKeyList);
    }

    # �ޤ��ĤäƤ��饢���ȡ����ʤ�ǽ�Υޥå������Ԥ��֤���
    return((@KeyList) ? '' : $Return);

}


###
## Version Check - KINOBOARDS��DB�ե�����Υ��������������å�
#
# - SYNOPSIS
#	VersionCheck($FileType, $VersionString);
#
# - ARGS
#	$FileType		�����å��оݤ�DB�ե�����Υ�����
#	$VersionString		������������ɽ�魯ʸ����
#
# - DESCRIPTION
#	KINOBOARDS�ǻȤ��Ƥ���DB�ե�����Υ��������������å���Ԥʤ���
#	�����礬����줿���ˤ��ͤ��֤������֥饦���˥��顼��ɽ�����̤��֤���
#	���ΤȤ����ä˥����å����Ƥ��ʤ�
#	(��������DB�ե�����Υե����ޥåȤ��Ѳ����Ƥ��ʤ�����)��
#
# - RETURN
#	�ʤ�
#
sub VersionCheck {
    local($FileType, $VersionString) = @_;
    local($VersionId, $ReleaseId) = split(/\//, $VersionString);

    # no check now...

}


###
## CheckArticle - ���Ϥ��줿��������Υ����å�
#
# - SYNOPSIS
#	CheckArticle($Board, $TextType, *Name, *Email, *Url, *Subject, *Icon, $Article);
#
# - ARGS
#	$Board		�Ǽ���ID
#	$TextType	ʸ�񥿥���
#	*Name		��Ƽ�̾
#	*Email		�ᥤ�륢�ɥ쥹
#	*Url		URL
#	*Subject	Subject
#	*Icon		��������ID
#	$Article	��ʸ
#
# - DESCRIPTION
#	���Ϥ��줿����������å�����
#
# - RETURN
#	��ʸ
#
sub CheckArticle {
    local($Board, $TextType, *Name, *Email, *Url, *Subject, *Icon, $Article) = @_;
    local($Tmp);

    # �����ꥢ�������å�
    if ($Name =~ /^\#.*$/o) {
        ($Tmp, $Email, $Url) = &GetUserInfo($Name);
	if ($Tmp eq '') { &Fatal(6, $Name); }
	$Name = $Tmp;
    } elsif ($SYS_ALIAS == 2) {
	# ɬ�ܤΤϤ��ʤΤˡ����ꤵ�줿�����ꥢ������Ͽ����Ƥ��ʤ�
	&Fatal(6, $Name);
    }

    # ʸ��������å�
    &CheckName(*Name);
    &CheckEmail(*Email);
    &CheckURL(*Url);
    &CheckSubject(*Subject);

    # �������å�
    if ($Article eq '') { &Fatal(2, ''); }

    # ��������Υ����å�; ������������̵���פ����ꡥ
    if (! &GetIconUrlFromTitle($Icon, $Board)) { $Icon = $H_NOICON; }

    # �������"�򥨥󥳡���
    $Article = &DQEncode($Article);

    return($Article);

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
sub AliasCheck {
    local($A, $N, $E, $U) = @_;

    &CheckAlias(*A);
    &CheckName(*N);
    &CheckEmail(*E);
    &CheckURL(*U);
    
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
sub CheckAlias {
    local(*String) = @_;

    # �������å�
    if (! $String) { &Fatal(2, ''); }

    # `#'�ǻϤޤäƤ�?
    ($String =~ (/^\#/)) || &Fatal(7, $H_ALIAS);

    # 1ʸ���������
    (length($String) > 1) || &Fatal(7, $H_ALIAS);

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
sub CheckSubject {
    local(*String) = @_;

    # �������å�
    if (! $String) { &Fatal(2, ''); }

    # ����������å�
    if ($String =~ m/[<>\t\n]/o) { &Fatal(4, ''); }

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
sub CheckName {
    local(*String) = @_;

    # �������å�
    if (! $String) { &Fatal(2, ''); }

    # ���ԥ����ɤ�����å�
    if ($String =~ /[\t\n]/o) { &Fatal(3, ''); }

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
sub CheckEmail {
    local(*String) = @_;

    if ($SYS_POSTERMAIL) {

	# �������å�
	if ($String eq '') { &Fatal(2, ''); }

	# `@'�����äƤʤ��㥢����
	if ($String !~ (/@/)) { &Fatal(7, 'E-Mail'); }

    }

    # ���ԥ����ɤ�����å�
    if ($String =~ /[\t\n]/o) { &Fatal(3, ''); }

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
sub CheckURL {
    local(*String) = @_;

    # http://�����ξ��϶��ˤ��Ƥ��ޤ���
    if ($String =~ m!^http://$!oi) { $String = ''; }

    # URL����ȤΥ����å�
    if (($String ne '') && (! &IsUrl($String))) { &Fatal(7, 'URL'); }

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
sub IsUrl {
    local($String) = @_;
    local($Scheme, $IsUrl);

    $IsUrl = 0;
    foreach $Scheme (@URL_SCHEME) {
	if ($String =~ m!^$Scheme://!i) { $IsUrl = 1; }
    }

    return($IsUrl);

}


###
## GetFollowIdTree - ��ץ饤�������ڹ�¤�����
#
# - SYNOPSIS
#	GetFollowIdTree($Id);
#
# - ARGS
#	$Id	����ID
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
#	�ڹ�¤��ɽ���ꥹ��
#
sub GetFollowIdTree {
    local($Id) = @_;

    # �Ƶ�Ū���ڹ�¤����Ф���
    return('(', &GetFollowIdTreeMain($Id), ')');

}

sub GetFollowIdTreeMain {
    local($Id) = @_;
    local(@AidList, @Result, @ChildResult);

    # �Ƶ���߾��
    if ($Id eq '') { return(); }

    # �ե����������Ф�
    @AidList = split(/,/, $DB_AIDS{$Id});

    # �ʤ�������
    return($Id) unless @AidList;

    # �Ƶ�
    @Result = ($Id, '(');
    @ChildResult = ();
    foreach (@AidList) {
	@ChildResult = &GetFollowIdTreeMain($_);
	if (@ChildResult) {
	    push(@Result, @ChildResult);
	}
    }
    return(@Result, ')');

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
sub GetReplySubject {
    local($Id) = @_;
    local($dFid, $dAids, $dDate, $dSubject) = &GetArticlesInfo($Id);

    # ��Ƭ�ˡ�Re:�פ����äĤ��Ƥ����������
    $dSubject =~ s/^Re:\s*//oi;
    # ��Ƭ�ˡ�Re: �פ򤯤äĤ����֤���
    return("Re: $dSubject");

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
sub GetFormattedTitle {
    local($Id, $Board, $Aids, $Icon, $Title, $Name, $Date) = @_;
    local($String, $InputDate, $IdStr, $Link, $Thread);

    $InputDate = &GetDateTimeFormatFromUtc(($Date || &GetModifiedTime($Id, $Board)));
    # �����ȥ뤬�Ĥ��Ƥʤ��ä��顤Id�򤽤Τޤޥ����ȥ�ˤ��롥
    $Title = $Title || $Id;

    # �̾ﵭ��
    $IdStr = "<strong>$Id.</strong> ";
    $Link = "<a href=\"$PROGRAM?b=$Board&c=e&id=$Id\">$Title</a>";
    $Thread = (($SYS_F_T && $Aids) ? " <a href=\"$PROGRAM?b=$Board&c=t&id=$Id\">$H_THREAD</a>" : '');

    if (($Icon eq $H_NOICON) || ($Icon eq '')) {
	$String = sprintf("$IdStr$Link$Thread [%s] $InputDate", ($Name || $MAINT_NAME));
    } else {
	$String = sprintf("$IdStr<img src=\"%s\" alt=\"$Icon \" width=\"$MSGICON_WIDTH\" height=\"$MSGICON_HEIGHT\">$Link$Thread [%s] $InputDate", &GetIconUrlFromTitle($Icon, $Board), ($Name || $MAINT_NAME));
    }

    return($String);

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
sub GetModifiedTime {
    local($Id, $Board) = @_;

    return($TIME - (-M &GetArticleFileName($Id, $Board)) * 86400);
    # 86400 = 24 * 60 * 60
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
sub GetDateTimeFormatFromUtc {
    local($Utc) = @_;
    local($Sec, $Min, $Hour, $Mday, $Mon, $Year, $Wday, $Yday, $Isdst);

    # �Ť�����Τ�Τ餷����
    if ($Utc !~ m/^\d+$/) { return($Utc); }

    # �Ѵ�
    ($Sec, $Min, $Hour, $Mday, $Mon, $Year, $Wday, $Yday, $Isdst) = localtime($Utc);
    return(sprintf("%d/%d(%02d:%02d)", $Mon + 1, $Mday, $Hour, $Min));

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
sub GetUtcFromOldDateTimeFormat {
    local($Time) = @_;

    # �����餷��
    if ($Time =~ m/^\d+$/) { return($Time); }

    # Ŭ��
    return(854477921);

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
sub DQEncode {
    local($Str) = @_;

    $Str =~ s/\"/__dq__/go;
    $Str =~ s/\>/__gt__/go;
    $Str =~ s/\</__lt__/go;
    $Str =~ s/\&/__amp__/go;
    return($Str);
}

sub DQDecode {
    local($Str) = @_;

    $Str =~ s/__dq__/\"/go;
    $Str =~ s/__gt__/\>/go;
    $Str =~ s/__lt__/\</go;
    $Str =~ s/__amp__/\&/go;
    return($Str);
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
sub HTMLEncode {
    local($_) = @_;

    s/\&/&amp;/go;
    s/\"/&quot;/go;
    s/\>/&gt;/go;
    s/\</&lt;/go;
    return($_);
}

sub HTMLDecode {
    local($_) = @_;

    s/&quot;/\"/gio;
    s/&gt;/\>/gio;
    s/&lt;/\</gio;
    s/&amp;/\&/gio;
    return($_);
}


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
sub ArticleEncode {
    local($Article) = @_;
    local($Return, $Url, $UrlMatch, $Str, @Cash);

    $Return = $Article;
    while ($Article =~ m/<URL:([^>]*)>/g) {
	$Url = $1;
	($UrlMatch = $Url) =~ s/\?/\\?/go;
	next if (grep(/^$UrlMatch$/, @Cash));
	push(@Cash, $Url);
	if (&IsUrl($UrlMatch)) {
	    $Str = "<a href=\"$Url\"><URL:$Url></a>";
	}
	$Return =~ s/<URL:$UrlMatch>/$Str/g;
    }

    &cgi'SecureHtml(*Return);

    return($Return);

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
sub DeleteArticle {
    local($Id, $Board, $ThreadFlag) = @_;
    local($Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $dId, @Target, $TargetId);

    # ��������μ���
    ($Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url) = &GetArticlesInfo($Id);

    # �ǡ����ν񤭴���(ɬ�פʤ�̼��)
    @Target = ($Id);
    foreach $TargetId (@Target) {
	foreach ($[ .. $#DB_ID) {
	    # ID����Ф�
	    $dId = $DB_ID[$_];
	    # �ե��������ꥹ�Ȥ��椫�顤������뵭����ID�������
	    $DB_AIDS{$dId} = join(',', grep((! /^$TargetId$/o), split(/,/, $DB_AIDS{$dId})));
	    # ������������������ID�������
	    $DB_FID{$dId} = '' if ($DB_FID{$dId} eq $TargetId);
	    $DB_FID{$dId} =~ s/,$TargetId,.*$//;
	    $DB_FID{$dId} =~ s/^$TargetId,.*$//;
	    $DB_FID{$dId} =~ s/,$TargetId$//;
	    # ̼���оݤȤ���
	    if ($ThreadFlag && ($dId eq $TargetId)) {
		push(Target, split(/,/, $DB_AIDS{$dId}));
	    }
	}
    }

    # DB�򹹿����롥
    &DeleteArticleFromDbFile($Board, *Target);
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
sub SupersedeArticle {
    local($Board, $Id, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail) = @_;
    local($SupersedeId, $File, $SupersedeFile);

    # ���Ϥ��줿��������Υ����å�
    $Article = &CheckArticle($Board, $TextType, *Name, *Email, *Url, *Subject, *Icon, $Article);

    # DB�ե����������
    $SupersedeId = &SupersedeDbFile($Board, $Id, $TIME, $Subject, $Icon, $REMOTE_HOST, $Name, $Email, $Url, $Fmail);

    # ex. ��100�ע���100_5��
    $File = &GetArticleFileName($Id, $Board);
    $SupersedeFile = &GetArticleFileName(sprintf("%s_%s", $Id, $SupersedeId), $Board);
    rename($File, $SupersedeFile);

    # �����Υե�����κ���
    &MakeArticleFile($TextType, $Article, $Id, $Board);
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
sub ReLinkExec {
    local($FromId, $ToId, $Board) = @_;
    local($dId, @Daughters, $DaughterId);

    # �۴ĵ����ζػ�
    &FatalPriv(50, '') if (grep(/^$FromId$/, split(/,/, $DB_FID{$ToId})));

    # �ǡ����񤭴���
    foreach ($[ .. $#DB_ID) {
	# ID����Ф�
	$dId = $DB_ID[$_];
	# �ե��������ꥹ�Ȥ��椫�顤��ư���뵭����ID�������
	$DB_AIDS{$dId} = join(',', grep((! /^$FromId$/o), split(/,/, $DB_AIDS{$dId})));
    }

    # ɬ�פʤ�̼��Ȥ�����Ƥ���
    @Daughters = split(/,/, $DB_AIDS{$FromId}) if ($DB_FID{$FromId});

    # ���������Υ�ץ饤����ѹ�����
    if ($ToId eq '') {
	$DB_FID{$FromId} = '';
    } elsif ($DB_FID{$ToId} eq '') {
	$DB_FID{$FromId} = "$ToId";
    } else {
	$DB_FID{$FromId} = "$ToId,$DB_FID{$ToId}";
    }

    # ����������̼�ˤĤ��Ƥ⡤��ץ饤����ѹ�����
    while($DaughterId = shift(@Daughters)) {
	# ¹̼��ġ�
	push(Daughters, split(/,/, $DB_AIDS{$DaughterId}));
	# �񤭴���
	if (($DB_FID{$DaughterId} eq $FromId) || ($DB_FID{$DaughterId} =~ /^$FromId,/)) {
	    $DB_FID{$DaughterId} = $DB_FID{$FromId} ? "$FromId,$DB_FID{$FromId}" : "$FromId";
	} elsif (($DB_FID{$DaughterId} =~ /^(.*),$FromId$/) || ($DB_FID{$DaughterId} =~ /^(.*),$FromId,/)) {
	    $DB_FID{$DaughterId} = $DB_FID{$FromId} ? "$1,$FromId,$DB_FID{$FromId}" : "$1,$FromId";
	}
    }

    # ��ץ饤��ˤʤä������Υե������������ɲä���
    $DB_AIDS{$ToId} = ($DB_AIDS{$ToId} ne '') ? "$DB_AIDS{$ToId},$FromId" : "$FromId";

    # ����DB�򹹿�����
    &UpdateArticleDb($Board);
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
sub ReOrderExec {
    local($FromId, $ToId, $Board) = @_;
    local(@Move);

    # ��ư���뵭�������򽸤��
    @Move = ($FromId, &CollectDaughters($FromId));

    # ��ư������
    &ReOrderArticleDb($Board, $ToId, *Move);

    # DB�񤭴������Τǡ�����å��夷ľ��
    &DbCash($Board);
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
sub CollectDaughters {
    local($Id) = @_;
    local(@Return);

    foreach (split(/,/, $DB_AIDS{$Id})) {
	push(Return, $_);
	push(Return, &CollectDaughters($_)) if ($DB_AIDS{$_} ne '');
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
sub GetNewArticleId {
    local($Board) = @_;

    &GetArticleId($Board) + 1;
}


######################################################################
# �ǡ�������ץ���ơ������


###
## DbCash - ����DB�����ɤ߹���
#
# - SYNOPSIS
#	DbCash($Board);
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
$BOARD_DB_CASH = 0;

sub DbCash {
    return if $BOARD_DB_CASH;

    local($Board) = @_;
    local($DBFile, $dId, $dFid, $dAids, $dDate, $dTitle, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail, $Count);

    # ���ꥢ
    @DB_ID = %DB_FID = %DB_AIDS = %DB_DATE = %DB_TITLE = %DB_ICON = %DB_REMOTEHOST = %DB_NAME = %DB_EMAIL = %DB_URL = %DB_FMAIL = ();

    $DBFile = &GetPath($Board, $DB_FILE_NAME);

    # �����ߡ�
    open(DB, "<$DBFile") || &Fatal(1, $DBFile);
    while(<DB>) {

	# Version Check
	&VersionCheck('DB', $1), next if (m/^\# Kb-System-Id: ([^\/]*\/.*)$/o);
	next if (/^\#/o || /^$/o);
	chop;

	($dId, $dFid, $dAids, $dDate, $dTitle, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail) = split(/\t/, $_, 11);
	next if ($dId eq '');

	$DB_ID[$Count++] = $dId;
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
    close(DB);

    $BOARD_DB_CASH = 1;		# cashed

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
sub GetArticlesInfo {
    local($Id) = @_;

    return($DB_FID{$Id}, $DB_AIDS{$Id}, $DB_DATE{$Id}, $DB_TITLE{$Id}, $DB_ICON{$Id}, $DB_REMOTEHOST{$Id}, $DB_NAME{$Id}, $DB_EMAIL{$Id}, $DB_URL{$Id}, $DB_FMAIL{$Id});

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
sub AddDBFile {
    local($Id, $Board, $Fid, $InputDate, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail) = @_;
    local($dId, $dFid, $dAids, $dInputDate, $dSubject, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail, $mdName, $mdInputDate, $mdSubject, $mdId, $mName, $mSubject, $mId, $FidList, $FFid, $File, $TmpFile, @FollowMailTo, @FFid, @ArriveMail);

    # ��ץ饤���Υ�ץ饤�������äƤ���
    if ($Fid ne '') {
	($FFid) = &GetArticlesInfo($Fid);
	@FFid = split(/,/, $FFid);
    }

    $FidList = $Fid;

    $File = &GetPath($Board, $DB_FILE_NAME);
    $TmpFile = &GetPath($Board, "$DB_FILE_NAME.$TMPFILE_SUFFIX");
    open(DBTMP, ">$TmpFile") || &Fatal(1, $TmpFile);
    open(DB, "<$File") || &Fatal(1, $File);
    while(<DB>) {

	# Version Check
	&VersionCheck('DB', $1) if (m/^\# Kb-System-Id: ([^\/]*\/.*)$/o);
	print(DBTMP "$_"), next if (/^\#/o || /^$/o);
	chop;

	($dId, $dFid, $dAids, $dInputDate, $dSubject, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail) = split(/\t/, $_);
	
	# �ե����赭�������Ĥ��ä��顤
	if (($dId ne '') && ($dId eq $Fid)) {

	    # ���ε����Υե�������ID�ꥹ�Ȥ˲ä���(����޶��ڤ�)
	    if ($dAids ne '') {$dAids .= ",$Id";} else {$dAids = $Id;}

	    # �������Υե�����ꥹ�Ȥ��äƤ��Ƹ�������ä���
	    # �������Υե�����ꥹ�Ȥ���
	    if ($dFid ne '') {
		$FidList = "$dId,$dFid";
	    }

	    if ($SYS_MAIL) {
		# �ᥤ�������Τ���˥���å���
		$mdName = $dName;
		$mdInputDate = $dInputDate;
		$mdSubject = $dSubject;
		$mdId = $dId;
		$mName = $Name;
		$mSubject = $Subject;
		$mId = $Id;
		if ($dFmail ne '') {
		    push(@FollowMailTo, $dEmail);
		}
	    }
	}

	# DB�˽񤭲ä���
	printf(DBTMP "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n", $dId, $dFid, $dAids, $dInputDate, $dSubject, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail);

	# ��ץ饤���Υ�ץ饤�������ĥᥤ��������ɬ�פ�����С��������¸
	if ($SYS_MAIL && (@FFid) && $dFmail && $dEmail && (grep(/^$dId$/, @FFid)) && (! grep(/^$dEmail$/, @FollowMailTo))) {
	    push(@FollowMailTo, $dEmail);
	}
    }

    # �����������Υǡ�����񤭲ä��롥
    printf(DBTMP "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n", $Id, $FidList, '', $InputDate, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail);

    # close Files.
    close(DB);
    close(DBTMP);

    # DB�򹹿�����
    rename($TmpFile, $File);

    # ɬ�פʤ���Ƥ����ä����Ȥ�ᥤ�뤹��
    &GetArriveMailTo(0, $Board, *ArriveMail);
    if (@ArriveMail) {
	&ArriveMail($Name, $Subject, $Id, @ArriveMail);
    }

    # ɬ�פʤ�ȿ�������ä����Ȥ�ᥤ�뤹��
    if (@FollowMailTo) {
	&FollowMail($mdName, $mdInputDate, $mdSubject, $mdId, $mName, $mSubject, $mId, @FollowMailTo);
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
sub UpdateArticleDb {
    local($Board) = @_;
    local($File, $TmpFile, $dId);

    $File = &GetPath($Board, $DB_FILE_NAME);
    $TmpFile = &GetPath($Board, "$DB_FILE_NAME.$TMPFILE_SUFFIX");
    open(DBTMP, ">$TmpFile") || &Fatal(1, $TmpFile);
    open(DB, "<$File") || &Fatal(1, $File);

    while(<DB>) {

	# Version Check
	&VersionCheck('DB', $1) if (m/^\# Kb-System-Id: ([^\/]*\/.*)$/o);

	print(DBTMP "$_"), next if (/^\#/o || /^$/o);

	# Id����Ф�
	chop; ($dId = $_) =~ s/\t.*$//;

	# DB�˽񤭲ä���
	printf(DBTMP "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n", $dId, $DB_FID{$dId}, $DB_AIDS{$dId}, $DB_DATE{$dId}, $DB_TITLE{$dId}, $DB_ICON{$dId}, $DB_REMOTEHOST{$dId}, $DB_NAME{$dId}, $DB_EMAIL{$dId}, $DB_URL{$dId}, $DB_FMAIL{$dId});
    }

    # close Files.
    close(DB);
    close(DBTMP);

    # DB�򹹿�����
    rename($TmpFile, $File);
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
sub DeleteArticleFromDbFile {
    local($Board, *Target) = @_;
    local($File, $TmpFile, $dId);

    $File = &GetPath($Board, $DB_FILE_NAME);
    $TmpFile = &GetPath($Board, "$DB_FILE_NAME.$TMPFILE_SUFFIX");
    open(DBTMP, ">$TmpFile") || &Fatal(1, $TmpFile);
    open(DB, "<$File") || &Fatal(1, $File);

    while(<DB>) {

	# Version Check
	&VersionCheck('DB', $1) if (m/^\# Kb-System-Id: ([^\/]*\/.*)$/o);

	print(DBTMP "$_"), next if (/^\#/o || /^$/o);

	# Id����Ф�
	chop; ($dId = $_) =~ s/\t.*$//;

	# ���������ϥ����ȥ�����
	print(DBTMP "#") if (grep(/^$dId$/, @Target));
	printf(DBTMP "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n", $dId, $DB_FID{$dId}, $DB_AIDS{$dId}, $DB_DATE{$dId}, $DB_TITLE{$dId}, $DB_ICON{$dId}, $DB_REMOTEHOST{$dId}, $DB_NAME{$dId}, $DB_EMAIL{$dId}, $DB_URL{$dId}, $DB_FMAIL{$dId});

    }

    # close Files.
    close(DB);
    close(DBTMP);

    # DB�򹹿�����
    rename($TmpFile, $File);
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
sub ReOrderArticleDb {
    local($Board, $Id, *Move) = @_;
    local($File, $TmpFile, $dId, $TopFlag);

    # ��Ƭ�ե饰
    $TopFlag = 1;

    $File = &GetPath($Board, $DB_FILE_NAME);
    $TmpFile = &GetPath($Board, "$DB_FILE_NAME.$TMPFILE_SUFFIX");
    open(DBTMP, ">$TmpFile") || &Fatal(1, $TmpFile);
    open(DB, "<$File") || &Fatal(1, $File);

    while(<DB>) {

	# Version Check
	&VersionCheck('DB', $1) if (m/^\# Kb-System-Id: ([^\/]*\/.*)$/o);

	print(DBTMP "$_"), next if (/^\#/o);
	print(DBTMP "$_"), next if (/^$/o);

	# Id����Ф�
	chop; ($dId = $_) =~ s/\t.*$//;

	# ��ư�����ۤϼ�����
	next if (grep(/^$dId$/, @Move));

	# ��Ƭ�ˤ�����ν���(���夬�����ξ��)
	if (($Id eq '') && ($SYS_BOTTOMTITLE == 1) && ($TopFlag == 1)) {
	    $TopFlag = 0;
	    foreach (@Move) {
		printf(DBTMP "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n", $_, $DB_FID{$_}, $DB_AIDS{$_}, $DB_DATE{$_}, $DB_TITLE{$_}, $DB_ICON{$_}, $DB_REMOTEHOST{$_}, $DB_NAME{$_}, $DB_EMAIL{$_}, $DB_URL{$_}, $DB_FMAIL{$_});
	    }
	}

	# ��ư�褬�����顤��˽񤭹���(���夬�塤�ξ��)
	if (($SYS_BOTTOMTITLE == 0) && ($dId eq $Id)) {
	    foreach (@Move) {
		printf(DBTMP "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n", $_, $DB_FID{$_}, $DB_AIDS{$_}, $DB_DATE{$_}, $DB_TITLE{$_}, $DB_ICON{$_}, $DB_REMOTEHOST{$_}, $DB_NAME{$_}, $DB_EMAIL{$_}, $DB_URL{$_}, $DB_FMAIL{$_});
	    }
	}

	# DB�˽񤭲ä���
	printf(DBTMP "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n", $dId, $DB_FID{$dId}, $DB_AIDS{$dId}, $DB_DATE{$dId}, $DB_TITLE{$dId}, $DB_ICON{$dId}, $DB_REMOTEHOST{$dId}, $DB_NAME{$dId}, $DB_EMAIL{$dId}, $DB_URL{$dId}, $DB_FMAIL{$dId});

	# ��ư�褬�����顤³���ƽ񤭹���(���夬�����ξ��)
	if (($SYS_BOTTOMTITLE == 1) && ($dId eq $Id)) {
	    foreach (@Move) {
		printf(DBTMP "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n", $_, $DB_FID{$_}, $DB_AIDS{$_}, $DB_DATE{$_}, $DB_TITLE{$_}, $DB_ICON{$_}, $DB_REMOTEHOST{$_}, $DB_NAME{$_}, $DB_EMAIL{$_}, $DB_URL{$_}, $DB_FMAIL{$_});
	    }
	}

    }

    # ��Ƭ�ˤ�����ν���(���夬�塤�ξ��)
    if (($Id eq '') && ($SYS_BOTTOMTITLE == 0)) {
	foreach (@Move) {
	    printf(DBTMP "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n", $_, $DB_FID{$_}, $DB_AIDS{$_}, $DB_DATE{$_}, $DB_TITLE{$_}, $DB_ICON{$_}, $DB_REMOTEHOST{$_}, $DB_NAME{$_}, $DB_EMAIL{$_}, $DB_URL{$_}, $DB_FMAIL{$_});
	}
    }

    # close Files.
    close(DB);
    close(DBTMP);

    # DB�򹹿�����
    rename($TmpFile, $File);
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
sub MakeArticleFile {
    local($TextType, $Article, $Id, $Board) = @_;
    local($File) = &GetArticleFileName($Id, $Board);

    # �ե�����򳫤�
    open(TMP, ">$File") || &Fatal(1, $File);

    # �С����������񤭽Ф�
    printf(TMP "<!-- Kb-System-Id: %s/%s -->\n", $KB_VERSION, $KB_RELEASE);

    # TextType��������
    if ((! $SYS_TEXTTYPE) || ($TextType eq $H_PRE)) {
	print(TMP "<p><pre>");
    }

    # ����; "��ǥ����ɤ����������ƥ������å�
    $Article = &DQDecode($Article);
    $Article = &ArticleEncode($Article);
    print(TMP "$Article\n");

    # TextType�Ѹ����
    if ((! $SYS_TEXTTYPE) || ($TextType eq $H_PRE)) {
	print(TMP "</pre></p>\n");
    }

    # ��λ
    close(TMP);

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
sub GetArticleBody {
    local($Id, $Board, *ArticleBody) = @_;
    local($QuoteFile);

    $QuoteFile = &GetArticleFileName($Id, $Board);
    open(TMP, "<$QuoteFile") || &Fatal(1, $QuoteFile);
    while(<TMP>) {
	&VersionCheck('Article', $1), next if (m/^<!-- Kb-System-Id: ([^\/]*\/.*) -->$/o);
	push(@ArticleBody, $_);
    }
    close(TMP);
    
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
sub GetArticleId {
    local($Board) = @_;
    local($ArticleNumFile, $ArticleId);

    $ArticleNumFile = &GetPath($Board, $ARTICLE_NUM_FILE_NAME);
    open(AID, "<$ArticleNumFile") || &Fatal(1, $ArticleNumFile);
    chop($ArticleId = <AID>);
    close(AID);
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
sub WriteArticleId {
    local($Id, $Board) = @_;
    local($File, $TmpFile, $OldArticleId);
    
    # �����Τ����˸Ť����ͤ��㤤! (��������ʤ���OK)
    $OldArticleId = &GetNewArticleId($Board);
    if (($Id =~ /^\d+$/) && ($Id < $OldArticleId)) {
	&Fatal(10, '');
    }

    $File = &GetPath($Board, $ARTICLE_NUM_FILE_NAME);
    $TmpFile = &GetPath($Board, "$ARTICLE_NUM_FILE_NAME.$TMPFILE_SUFFIX");
    open(AID, ">$TmpFile") || &Fatal(1, $TmpFile);
    print(AID "$Id\n");
    close(AID);

    # ����
    rename($TmpFile, $File);

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
sub GetArriveMailTo {
    local($CommentFlag, $Board, *ArriveMail) = @_;
    local($ArriveMailFile);

    $ArriveMailFile = &GetPath($Board, $ARRIVEMAIL_FILE_NAME);
    # �ե����뤬�ʤ�����Τޤ�
    open(ARMAIL, "<$ArriveMailFile") || return;
    while(<ARMAIL>) {
    	# Version Check
	&VersionCheck('ARRIVEMAIL', $1), next if (m/^\# Kb-System-Id: ([^\/]*\/.*)$/o);
	next if ((! $CommentFlag) && (/^\#/o || /^$/o));
	chop;
	push(@ArriveMail, $_);
    }
    close(ARMAIL);
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
sub UpdateArriveMailDb {
    local($Board, *ArriveMail) = @_;
    local($File, $TmpFile);

    $File = &GetPath($Board, $ARRIVEMAIL_FILE_NAME);
    $TmpFile = &GetPath($Board, $ARRIVEMAIL_FILE_NAME);
    open(DBTMP, ">$TmpFile") || &Fatal(1, $TmpFile);
    foreach (@ArriveMail) { print(DBTMP "$_\n"); }
    close(DBTMP);
    rename($TmpFile, $File);
}


###
## CashAliasData - �桼��DB�����ɤ߹���
#
# - SYNOPSIS
#	CashAliasData;
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
sub CashAliasData {

    local($A, $N, $E, $H, $U);

    # ������ࡥ
    open(ALIAS, "<$USER_ALIAS_FILE") || &Fatal(1, $USER_ALIAS_FILE);
    while(<ALIAS>) {

	# Version Check
	&VersionCheck('Alias', $1), next if (m/^<!-- Kb-System-Id: ([^\/]*\/.*) -->$/o);
	next if (/^$/o);
	chop;

	($A, $N, $E, $H, $U) = split(/\t/, $_);

	$Name{$A} = $N;
	$Email{$A} = $E;
	$Host{$A} = $H;
	$URL{$A} = $U;
    }
    close(ALIAS);

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
sub GetUserInfo {
    local($Alias) = @_;
    local($A, $N, $E, $H, $U, $rN, $rE, $rU);

    # �ե�����򳫤�
    open(ALIAS, "<$USER_ALIAS_FILE") || &Fatal(1, $USER_ALIAS_FILE);
    
    # 1��1�ĥ����å���
    while(<ALIAS>) {
	
	# Version Check
	&VersionCheck('Alias', $1), next if (m/^<!-- Kb-System-Id: ([^\/]*\/.*) -->$/o);
	next if (/^$/o);
	chop;
	
	# ʬ��
	($A, $N, $E, $H, $U) = split(/\t/, $_);
	
	# �ޥå����ʤ��㼡�ء�
	next if ($A ne $Alias);
	
	$rN = $N;
	$rE = $E;
	$rU = $U;

    }
    close(ALIAS);

    # �ꥹ�Ȥˤ����֤�
    return($rN, $rE, $rU);
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
sub WriteAliasData {

    local($Alias, $TmpFile);

    $TmpFile = "$USER_ALIAS_FILE.$TMPFILE_SUFFIX";
    open(ALIAS, ">$TmpFile") || &Fatal(1, $TmpFile);

    # �С����������񤭽Ф�
    printf(ALIAS "<!-- Kb-System-Id: %s/%s -->\n", $KB_VERSION, $KB_RELEASE);

    # ��ˡ�
    foreach $Alias (sort keys(%Name)) {
	if ($Name{$Alias}) {
	    printf(ALIAS "%s\t%s\t%s\t%s\t%s\n", $Alias, $Name{$Alias}, $Email{$Alias}, $Host{$Alias}, $URL{$Alias});
	}
    }
    close(ALIAS);

    # ����
    rename($TmpFile, $USER_ALIAS_FILE);
    
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
sub GetAllBoardInfo {
    local(*BoardList, *BoardInfo) = @_;
    local($BoardId, $BName, $BInfo);

    open(ALIAS, "<$BOARD_ALIAS_FILE") || &Fatal(1, $BOARD_ALIAS_FILE);
    while(<ALIAS>) {

	# Version Check
	&VersionCheck('Board', $1), next if (m/^\# Kb-System-Id: ([^\/]*\/.*)$/o);
	next if (/^\#/o || /^$/o);
	chop;
	($BoardId, $BName, $BInfo) = split(/\t/, $_, 3);
	$BoardList{$BoardId} = $BName;
	$BoardInfo{$BoardId} = $BInfo;
    }
    close(ALIAS);
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
sub GetBoardInfo {
    local($Alias) = @_;
    local($BoardName, $dAlias, $dBoardName);

    open(ALIAS, "<$BOARD_ALIAS_FILE") || &Fatal(1, $BOARD_ALIAS_FILE);
    while(<ALIAS>) {

	# Version Check
	&VersionCheck('Board', $1), next if (m/^\# Kb-System-Id: ([^\/]*\/.*)$/o);
	next if (/^\#/o || /^$/o);
	chop;
	($dAlias, $dBoardName) = split(/\t/, $_, 3);
	if ($Alias eq $dAlias) { $BoardName = $dBoardName; }
    }
    close(ALIAS);

    return($BoardName);

}


###
## CashIconDb - ��������DB�����ɤ߹���
#
# - SYNOPSIS
#	CashIconDb($Board);
#
# - ARGS
#	$Board		�Ǽ���ID
#
# - DESCRIPTION
#	��������DB���ɤ߹����Ϣ�������������ࡥ
#	����ѿ���%ICON_FILE��%ICON_HELP���˲����롥
#
# - RETURN
#	�ʤ�
#
$ICON_DB_CASH = 0;

sub CashIconDb {
    return if $ICON_DB_CASH;

    local($Board) = @_;
    local($FileName, $IconTitle, $IconHelp);

    # ����å���Υ��ꥢ
    %ICON_FILE = %ICON_HELP = ();

    # ��İ��ɽ��
    open(ICON, &GetIconPath("$Board.$ICONDEF_POSTFIX"))
	|| (open(ICON, &GetIconPath("$DEFAULT_ICONDEF"))
	    || &Fatal(1, &GetIconPath("$DEFAULT_ICONDEF")));
    while(<ICON>) {

	# Version Check
	&VersionCheck('Icon', $1), next if (m/^\# Kb-System-Id: ([^\/]*\/.*)$/o);
	next if (/^\#/o || /^$/o);
	chop;
	($FileName, $IconTitle, $IconHelp) = split(/\t/, $_, 3);

	# ������
	$ICON_FILE{$IconTitle} = $FileName;
	$ICON_HELP{$IconTitle} = $IconHelp;
    }
    close(ICON);

    $ICON_DB_CASH = 1;		# cashed

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
sub GetBoardHeader {
    local($Board, *BoardHeader) = @_;
    local($File);

    $File = &GetPath($Board, $BOARD_FILE_NAME);
    open(HEADER, "<$File") || &Fatal(1, $File);
    while(<HEADER>){
	# Version Check
	&VersionCheck('Header', $1), next if (m/^<!-- Kb-System-Id: ([^\/]*\/.*) -->$/o);
	push(@BoardHeader, $_);
    }
    close(HEADER);
    
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
#	����ѿ�$ARCH�򻲾Ȥ���Mac/Win/UNIX���б���
#
# - RETURN
#	�ѥ���ɽ��ʸ����
#
sub GetArticleFileName {
    local($Id, $Board) = @_;

    # Board�����ʤ�Board�ǥ��쥯�ȥ��⤫�����С�
    # ���Ǥʤ���Х����ƥफ������
    return(($Board) ? "$Board/$Id" : "$Id") if ($ARCH eq 'UNIX');
    return(($Board) ? "$Board/$Id" : "$Id") if ($ARCH eq 'WinNT');
    return(($Board) ? "$Board/$Id" : "$Id") if ($ARCH eq 'Win95');
    return(($Board) ? ":$Board:$Id" : "$Id") if ($ARCH eq 'Mac');

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
#	����ѿ�$ARCH�򻲾Ȥ���Mac/Win/UNIX���б���
#
# - RETURN
#	�ѥ���ɽ��ʸ����
#
sub GetPath {
    local($DbDir, $File) = @_;

    # �֤�
    return("$DbDir/$File") if ($ARCH eq 'UNIX');
    return("$DbDir/$File") if ($ARCH eq 'WinNT');
    return("$DbDir/$File") if ($ARCH eq 'Win95');
    return(":$DbDir:$File") if ($ARCH eq 'Mac');

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
#	����ѿ�$ARCH�򻲾Ȥ���Mac/Win/UNIX���б���
#
# - RETURN
#	�ѥ���ɽ��ʸ����
#
sub GetIconPath {
    local($File) = @_;

    # �֤�
    return("$ICON_DIR/$File") if ($ARCH eq 'UNIX');
    return("$ICON_DIR/$File") if ($ARCH eq 'WinNT');
    return("$ICON_DIR/$File") if ($ARCH eq 'Win95');
    return(":$ICON_DIR:$File") if ($ARCH eq 'Mac');

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
sub GetIconUrlFromTitle {
    local($Icon, $Board) = @_;
    local($FileName, $Title, $TargetFile);

    # ��İ��ɽ��
    open(ICON, &GetIconPath("$Board.$ICONDEF_POSTFIX"))
	|| (open(ICON, &GetIconPath("$DEFAULT_ICONDEF"))
	    || &Fatal(1, &GetIconPath("$DEFAULT_ICONDEF")));
    while(<ICON>) {

	# Version Check
	&VersionCheck('Icon', $1), next if (m/^\# Kb-System-Id: ([^\/]*\/.*)$/o);
	next if (/^\#/o || /^$/o);
	chop;
	($FileName, $Title) = split(/\t/, $_, 3);
	if ($Title eq $Icon) { $TargetFile = $FileName;	}
    }
    close(ICON);

    return($TargetFile ? "$ICON_DIR/$TargetFile" : '');

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
sub SupersedeDbFile {
    local($Board, $Id, $InputDate, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail) = @_;
    local($SupersedeId, $dId, $dFid, $dAids, $dInputDate, $dSubject, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail, $File, $TmpFile);
    
    # initial version��1�ǡ�1���������Ƥ�����1��2����9��10��11����
    # later version��DB���ɬ����younger version���Ⲽ�˽и����롥
    # ���ʤ��10_2��10��10_1�ϡ�10_1��10_2��10�ν���¤֤�ΤȤ��롥
    $SupersedeId = 1;

    $File = &GetPath($Board, $DB_FILE_NAME);
    $TmpFile = &GetPath($Board, "$DB_FILE_NAME.$TMPFILE_SUFFIX");
    open(DBTMP, ">$TmpFile") || &Fatal(1, $TmpFile);
    open(DB, "<$File") || &Fatal(1, $File);

    while(<DB>) {

	# Version Check
	&VersionCheck('DB', $1) if (m/^\# Kb-System-Id: ([^\/]*\/.*)$/o);

	print(DBTMP "$_"), next if (/^\#/o || /^$/o);
	chop;

	($dId, $dFid, $dAids, $dInputDate, $dSubject, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail) = split(/\t/, $_);

	# later version�����Ĥ��ä��顤version�����ɤߤ��Ƥ�����
	$SupersedeId++ if ("$dId" eq (sprintf("#-%s_%s", $Id, $SupersedeId)));

	# ���������κǿ��Ǥ����Ĥ��ä��顤
	if ($dId eq $Id) {

	    # aging���Ƥ��ޤ�
	    printf(DBTMP "#-%s_%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n", $dId, $SupersedeId, $dFid, $dAids, $dInputDate, $dSubject, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail);

	    # ³���ƿ�����������񤭲ä���
	    printf(DBTMP "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n", $Id, $dFid, $dAids, $InputDate, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail);

	} else {

	    # DB�˽񤭲ä���
	    print(DBTMP "$_\n");

	}

    }

    # close Files.
    close(DB);
    close(DBTMP);

    # DB�򹹿�����
    rename($TmpFile, $File);

    # �֤�
    return($SupersedeId);

}
