# This file implements Site Specific Definitions of KINOBOARDS.


###
## �������Ԥ�̾����E-Mail���ɥ쥹�������ƥ��̾��
#
# �ᥤ�������ˤ�Ȥ��ޤ���
# ��$MAINT_NAME�פϥ���ե��٥åȤΤߤǻ��ꤷ�Ƥ���������
# �ᥤ�뤬ʸ����������褦�ʤ顤
# ��$SYSTEM_NAME�פ⥢��ե��٥åȤΤߤˤ��Ƥ���������
#
# ��:
# $MAINT_NAME = 'KinoboardsAdmin';
# $MAINT = 'nakahiro@kinotrope.co.jp';
# $SYSTEM_NAME = "KINOBOARDS/1.0";
#
$MAINT_NAME = 'YourName';
$MAINT = 'yourname@your.e-mail.domain';
$SYSTEM_NAME = "YourSystemName";

###
## �������Ф�ư���Ƥ���ޥ���Ϥɤ�Ǥ���?
#
# ��������1�Ԥ�Ĥ��ƥ����ȥ����Ȥ��Ƥ���������
#
 $ARCH = 'UNIX';			# UNIX + Perl4/5
# $ARCH = 'WinNT';			# WinNT + Perl5
# $ARCH = 'Win95';			# Win95 + Perl5
# $ARCH = 'Mac';			# Mac + MacPerl

###
## �������ॾ����
#
#   'GMT', 'GMT+9'��'GMT-7'�ʤɤ���ꤷ�ޤ���
#
#   Perl���󥹥ȡ�����Υǥե���ȤΥ����ॾ����򤽤Τޤ޻Ȥ����ϡ�
#   ���Τޤ޶�('')����ꤷ�Ƥ����Ƥ���������
#
#   �����Хޥ������ܹ�����֤���Ƥ����硤�̾������Ǥ���С�
#   �ǥե���Ȥ����ܻ����ѤΥ����ॾ����ˤʤäƤ���Ϥ��Ǥ���
#
#   �����Хޥ��󤬳����ˤ��ꡤ���������ѼԤΤۤȤ�ɤϹ���桼����
#   �Τ褦�ʾ��ˤϡ�'GMT+9'����ꤷ�ƻȤ��������Ǥ��礦��
#
$TIME_ZONE = '';

###
## �������ƥൡǽ������
#
# CGI�μ¹ԥ����뤫�ʥ��󥹥ȡ���ľ��ϥ�����褦�ˤ��Ƥ���������
#   0: ���ʤ�
#   1: ����kb.klg�Ȥ����ե�����˥����񤫤�ޤ���
$SYS_LOG = 1;

# ����ʸ�񥿥���(HTML or PLAIN)�������Ԥ����ݤ�(�Ԥʤ�ʤ���PRE�Τ�)
#   0: �Ԥ�ʤ�
#   1: �Ԥ�
$SYS_TEXTTYPE = 1;

# �����ꥢ�������Ѥ��뤫�ݤ�
#   0: ���Ѥ��ʤ�
#   1: ���Ѥ���
#   2: �����ꥢ������Ͽ���ʤ���С���������ƤǤ��ʤ��褦�ˤ���
$SYS_ALIAS = 1;

# ����������������Ѥ��뤫�ݤ�
#   0: ���Ѥ��ʤ�
#   1: ���Ѥ���
$SYS_ICON = 1;

# ���ޥ�ɥ�����������Ѥ��뤫�ݤ�
#   0: ���Ѥ��ʤ�(���ޥ�ɤϥƥ����Ȥ�ɽ������)
#   1: ���Ѥ���
#   2: ���ޥ�ɥ��������Ʊ���˥ƥ����Ȥ�ɽ������
$SYS_COMICON = 1;

# ������Ƶ���������������Ƥ����������������Ƥ�����(�����ȥ�����λ�)
#   0: ��
#   1: ��
$SYS_BOTTOMTITLE = 0;

# ������Ƶ���������������Ƥ����������������Ƥ�����(���������λ�)
#   0: ��
#   1: ��
$SYS_BOTTOMARTICLE = 1;

# �����Υإå��˥ޥ���̾��ɽ�����뤫�ݤ�
#   0: ɽ�����ʤ�
#   1: ɽ������
$SYS_SHOWHOST = 0;

# �����Υإå��˥��ޥ�ɷ���ɽ�����뤫�ݤ�
#   0: ɽ�����ʤ�
#   1: ɽ������
$SYS_COMMAND = 1;

# �����ε��ƺ��祵�����ʥХ��ȿ��ǻ��ꤷ�Ƥ�������; 50K �� 51200��
#   0�ϡֵ��������������¤ʤ��פ��̣���ޤ���
$SYS_MAXARTSIZE = 0;

# ������ƻ����ᥤ�륢�ɥ쥹�����Ϥ�ɬ�ܤȤ��뤫
#   0: ɬ�ܤȤ��ʤ�
#   1: ɬ�ܤȤ���
$SYS_POSTERMAIL = 1;

# �����ФΥݡ����ֹ��ɽ�����뤫�ݤ�
#   0: ɽ�����ʤ�
#   1: (ɬ�פʤ��)ɽ������
#      HTTP�Υǥե���ȤǤ���80�֥ݡ��Ȥξ�硤1�����ꤷ�Ƥ�ɽ�����ޤ���
$SYS_PORTNO = 1;

# �����ȥХå����饦��ɥ��᡼����Ȥ����ݤ�
#   0: �Ȥ�ʤ�
#   1: �Ȥ�
$SYS_NETSCAPE_EXTENSION = 1;
#
# �Ȥ����ϰʲ�����ꤷ�Ƥ���������
#
$BG_IMG = "";
$BG_COLOR = "#66CCCC";
$TEXT_COLOR = "#000000";
$LINK_COLOR = "#0000AA";
$ALINK_COLOR = "#FF0000";
$VLINK_COLOR = "#00AA00";

# �Ƶ�ǽ�����Ѳ�ǽ�Ȥ��뤫�ݤ�
#   0: ���ѤǤ��ʤ�
#   1: ���ѤǤ���
$SYS_F_T = 1;			# ��ץ饤�����ΤޤȤ��ɤߤ�ɽ��
$SYS_F_N = 1;			# ���������
$SYS_F_R = 1;			# �����ȥ����(���ս�)��ɽ��
$SYS_F_L = 1;			# �Ƕ�ε���������ɽ��
$SYS_F_S = 1;			# �����θ���
$SYS_F_B = 1;			# �Ǽ��İ�����ɽ��
#
# ����ʲ��Υ��ޥ�ɤ�ɬ����
# �������������������¤򤫤�����ǡ����Ѥ��Ƥ�������
# �ʾܤ����ϥ��󥹥ȥ졼�����ޥ˥奢��򻲾Ȥ��Ƥ��������ˡ�
# �Ǥʤ����˲�Ū�ʰ�����ƿ̾�Ǥ�������Ǥ�����͡�
#
# [���] ������ץȤ�̾�����Ѥ������餤�������Ф����ܤǤ���
#
$SYS_F_D = 0;			# �����κ��������
$SYS_F_MV = 0;			# �����Ρ�������/������-��ץ饤�ط��פ��ѹ�
$SYS_F_AM = 0;			# ���嵭��������Υᥤ�������������

# ��ư�ᥤ���ۿ������ӥ������Ѥ��뤫�ݤ�
#   0: ���Ѥ��ʤ�
#   1: ���Ѥ���
$SYS_MAIL = 1;
#
# 1: ���Ѥ��롤�ˤ������ϡ��ʲ��ǥᥤ�륵���Ф���ꤷ�Ƥ���������
#
# ��: $SMTP_SERVER = 'mail.foo.bar.ne.jp';
#
$SMTP_SERVER = 'localhost';
#
# �ʲ��Ϥ��ΤޤޤǷ빽�Ǥ�����Ư�塤�⤷��
# ��kb.ph����ǡ�CGI��ư�������Ф�OS����ꤷ�Ƥ���������
# �Ȥ������顼��å��������Ф����Τߡ����κ�Ȥ�ԤʤäƤ���������
#
# CGI��ư�������С����̤�WWW�����ФǤ����ᥤ�륵���Ф��㤢��ޤ����
# �Ρ�OS�Υ����פ˹��פ���Ԥ�������Ƭ�Ρ�#�פ�������Ƥ���������
# OS�Υ����פϡ�telnet���ơ�uname -sr�פȤ������ޥ�ɤ�¹Ԥ���Ȥ狼��ޤ���
#
# $AF_INET = 2; $SOCK_STREAM = 2;	# SunOS 5.* ( Solaris 2.* )
# $AF_INET = 2; $SOCK_STREAM = 1;	# SunOS 4.*
# $AF_INET = 2; $SOCK_STREAM = 1;	# HP
# $AF_INET = 2; $SOCK_STREAM = 1;	# AIX
# $AF_INET = 2; $SOCK_STREAM = 1;	# Linux
# $AF_INET = 2; $SOCK_STREAM = 1;	# FreeBSD
#
# NT���Ȥɤ��ʤ�Τ��ʡġĤɤʤ������������������������ޤ����顤
# �ɤ���nakahiro@kinotrope.co.jp�ޤǤ��Τ餻����������m(..m

###
## ���Ǽ��İ���������URL
#
#  �ַǼ��İ����ءפǥ�󥯤������kb�ǥ��쥯�ȥ꤫�������URL�ǻ��ꤷ�ޤ���
#  ���ʤ�kb�ǥ��쥯�ȥ��(��äơ�����Ū�ˤ�index.html��index.shtml��)��
#  '-'����ꤹ��ȡ���ʬ���Ѱդ����ե�����Ǥʤ�CGI����ư��������Ǽ��İ����ء�
#  ���줾���󥯤���ޤ���
#
# $BOARDLIST_URL = '';			# kb�ǥ��쥯�ȥ��
# $BOARDLIST_URL = '-';			# CGI����ư��������Ǽ��İ�����
$BOARDLIST_URL = 'kb10.shtml';		# kb/kb10.shtml��

###
## �����ѥޡ���
#
# ��>�פ��&gt;�פ���ѥޡ����ˤ���Τ��򤱤Ʋ�������
# �ȥ�֥�򵯤����֥饦����¸�ߤ��ޤ���
#
$DEFAULT_QMARK = ' ] ';

###
## ������������礭��
#
# �����Υ֥饦���Ǥϡ����ο��ͤ�Ŭ���˻��ꤹ��ȡ�
# ����˥�������γ���̾���ԤʤäƤ����褦�Ǥ���
#
# ���ޥ�ɥ�������(���ء���)
$COMICON_HEIGHT = 20;		# �⤵[dot]
$COMICON_WIDTH = 20;		# ��[dot]
# ��å�������������(���ܰ��ڡ���)
$MSGICON_HEIGHT = 20;		# �⤵[dot]
$MSGICON_WIDTH = 20;		# ��[dot]

###
## �������Ϲ��ܤ��礭��
#
$SUBJECT_LENGTH = 60;		# ��
$TEXT_ROWS = 15;		# �����Կ�
$TEXT_COLS = 65;		# ������
$NAME_LENGTH = 60;		# ̾����
$MAIL_LENGTH = 60;		# E-mail��
$URL_LENGTH = 52;		# URL��
$KEYWORD_LENGTH = 60;		# �������������
$DEF_TITLE_NUM = 20;		# �����ȥ������ɽ�����륿���ȥ�ο�
				# 0�ˤ������������ɽ������褦�ˤʤ�ޤ���
$TREE_INDENT = 1;		# �ե졼����ѻ��Υĥ꡼��¤�Υ���ǥ����
				# ��R5.3�ǤϻȤ��ޤ����

###
## ��URL�Ȥ��Ƶ��Ĥ���scheme
#
@URL_SCHEME = ('http', 'ftp', 'gopher');

# ����å����������
#
$H_BOARD = "�Ǽ���";
$H_ICON = "��������";
$H_SUBJECT = "�����ȥ�";
$H_MESG = "��å�����";
$H_ALIAS = "�����ꥢ��";
$H_FROM = "��̾��";
$H_MAIL = "�ᥤ��";
$H_HOST = "�ޥ���";
$H_USER = "��Ƽ�";		# �����ꥢ����Ͽ�Ǥʤ��Ƚ񤭹��ߤǤ��ʤ����
$H_URL = "URL";
$H_URL_S = "URL(��ά��)";
$H_DATE = "�����";
$H_REPLY = "��ץ饤";
$H_ORIG = "$H_REPLY��";
$H_ORIG_TOP = "���ꥸ�ʥ�";
$H_LINE = "<p>------------------------------</p>";
$H_THREAD = "��";
$H_TEXTTYPE = "ɽ������";
$H_HTML = "HTML�Ȥ���ɽ������";
$H_PLAIN = "���Τޤ�ɽ������";
$H_NOICON = "�ʤ�";
$H_BACKBOARD = "$H_BOARD������";
$H_BACKTITLE = "$H_SUBJECT������";
$H_PREVARTICLE = "����$H_MESG��";
$H_NEXTARTICLE = "����$H_MESG��";
$H_POSTNEWARTICLE = "�����˽񤭹���";
$H_REPLYTHISARTICLE = "$H_REPLY��񤭹���";
$H_REPLYTHISARTICLEQUOTE = "���Ѥ���$H_REPLY��񤭹���";
$H_READREPLYALL = "$H_REPLY��ޤȤ��ɤ�";
$H_DELETE_TITLE = "�������";
$H_SUPERSEDE_TITLE = "��������";
$H_BACKART = "�����˽񤭹��ޤ줿$H_MESG��";
$H_NEXTART = "�ʹߤ˽񤭹��ޤ줿$H_MESG��";
$H_TOP = "��";
$H_BOTTOM = "��";
$H_NOARTICLE = "��������$H_MESG������ޤ���";
$H_SUPERSEDE_ICON = "[��]";
$H_DELETE_ICON = "[��]";
$H_RELINKFROM_MARK = "[��]";
$H_RELINKTO_MARK = "[��]";
$H_REORDERFROM_MARK = "[��]";
$H_REORDERTO_MARK = "[��]";


#/////////////////////////////////////////////////////////////////////
1;


# $Id: kb.ph,v 5.4 1997-12-16 12:46:41 nakahiro Rel $


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
