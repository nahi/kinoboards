# This file implements Site Specific Definitions of KINOBOARDS.

###
## �������Ԥ�̾����E-Mail���ɥ쥹�������ƥ��̾��
#
# ��:
# $MAINT_NAME = 'KinoboardsAdmin';
# $MAINT = 'nakahiro@sarion.co.jp';
# $SYSTEM_NAME = "KINOBOARDS/1.0";
#
$MAINT_NAME = 'YourName';
$MAINT = 'yourname@your.e-mail.domain';
$SYSTEM_NAME = "YourSystemName";

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
# CGI�μ¹ԥ�����ޤ���?
# ���󥹥ȡ���ľ��ϥ����äƤ���������kb.klg�˽񤭽Ф���ޤ���
#   0: ���ʤ�
#   1: ����HTML�ե����ޥåȡ�
#   2: ���ʥץ쥤��ƥ����ȥե����ޥåȡ�
$SYS_LOG = 1;

# �񤭹���ʸ�񥿥��פȤ��ơ��ɤ������ޤ���?
# �֤��Τޤ�ɽ����...���Ϥ���������PRE�����ǰϤޤ��ɽ������ޤ���
# ��HTML���Ѵ���.....���Ϥ���������HTML���Ѵ������ɽ������ޤ���
# ��HTML�����ϡ�.....���Ϥ��������Ϥ��Τޤ�HTML�Ȥ���ɽ������ޤ���
# �ʲ�����ɤ줫��Ĥ�����Ǥ���������
#   $SYS_TEXTTYPE = 1 + 0 + 0;	# �֤��Τޤ�ɽ����
#   $SYS_TEXTTYPE = 0 + 2 + 0;	# ��HTML���Ѵ���
#   $SYS_TEXTTYPE = 0 + 0 + 4;	# ��HTML�����ϡ�
#   $SYS_TEXTTYPE = 1 + 2 + 0;	# �֤��Τޤ�ɽ���ס�HTML���Ѵ���
#   $SYS_TEXTTYPE = 1 + 0 + 4;	# �֤��Τޤ�ɽ���ס�HTML�����ϡ�
#   $SYS_TEXTTYPE = 0 + 2 + 4;	# ��HTML���Ѵ��ס�HTML�����ϡ�
#   $SYS_TEXTTYPE = 1 + 2 + 4;	# �֤��Τޤ�ɽ���ס�HTML���Ѵ��ס�HTML�����ϡ�
$SYS_TEXTTYPE = 1 + 2 + 4;

# �����ꥢ�������Ѥ��ޤ���?
#   0: ���Ѥ��ʤ�
#   1: ���Ѥ���
#   2: �����ꥢ������Ͽ���ʤ���С���������ƤǤ��ʤ��褦�ˤ���
#   3: HTTP-Cookies��Ȥ��ʥ桼�������֥饦���˳Ф��������
$SYS_ALIAS = 3;

  # ��ǡ�3: HTTP-Cookies��Ȥ��פ����ꤷ����硤�ʲ������ꤷ�Ƥ���������
  # HTTP-Cookies��ͭ�����֤�ɤΤ褦�����ꤷ�ޤ���?
  #   0: �֥饦����λ���ޤ�
  #   1: ̵���¡ʼºݤˤ�Thursday, 31-Dec-2029 23:59:59 GMT��
  #   2: n����ޤǡ�n�ϲ������ꤷ�ޤ��ˡ�
  #   3: �������ޤǡʻ������ϰʲ������ꤷ�ޤ��ˡ�
  $SYS_COOKIE_EXPIRE = 3;

    # ��ǡ�2: n����ޤǡפ����ꤷ������������
    # ��3: �������ޤǡפ����ꤷ�����ϻ������ʻ��֤�ˤ����ꤷ�Ƥ���������
    # 0�⤷����1����������Ϥ��ΤޤޤǷ빽�Ǥ��ʻ��ꤷ�Ƥ�̵�뤵��ޤ��ˡ�
    $SYS_COOKIE_VALUE = 'Thursday, 31-Dec-98 23:59:59 GMT';
    # �����ξ�硥�㤨��30���֡�
    #   $SYS_COOKIE_VALUE = 30;
    # �������ξ�硥�㤨��1998ǯǯ���ޤǡ�
    #   $SYS_COOKIE_VALUE = 'Thursday, 31-Dec-98 23:59:59 GMT';

# ����������������Ѥ��ޤ���?
#   0: ���Ѥ��ʤ�
#   1: ���Ѥ���
$SYS_ICON = 1;

# ���ޥ�ɥ�����������Ѥ��ޤ���?
#   0: ���Ѥ��ʤ�(���ޥ�ɤϥƥ����Ȥ�ɽ������)
#   1: ���Ѥ���
#   2: ���ޥ�ɥ��������Ʊ���˥ƥ����Ȥ�ɽ������
$SYS_COMICON = 1;

# �ǿ��ε��������Ĥˡ�[new]��������ʲ����δ��ˤ�Ĥ��ޤ���?
# 0����ꤹ��ȡ����ε�ǽ�����Ѥ��ޤ����[new]��������ϤĤ��ʤ���
$SYS_NEWICON = 10;		# [����]

# ������Ƶ���������������Ƥ����������������Ƥ�����(�����ȥ�����λ�)
#   0: ��
#   1: ��
$SYS_BOTTOMTITLE = 0;

# ������Ƶ���������������Ƥ����������������Ƥ�����(���������λ�)
#   0: ��
#   1: ��
$SYS_BOTTOMARTICLE = 1;

# �����Υإå��˥ޥ���̾��ɽ�����ޤ���?
#   0: ɽ�����ʤ�
#   1: ɽ������
$SYS_SHOWHOST = 0;

# �����Υإå��˥��ޥ�ɷ���ɽ�����ޤ���?
#   0: ɽ�����ʤ�
#   1: ɽ������
$SYS_COMMAND = 1;

# Subject�ˡʰ����ʡ˥��������Ϥ�����ޤ���?
#   0: �����ʤ�
#   1: ����
$SYS_TAGINSUBJECT = 1;

# �����ε��ƺ��祵�����ʥХ��ȿ��ǻ��ꤷ�Ƥ�������; 50K �� 51200��
#   0�ϡֵ��������������¤ʤ��פ��̣���ޤ���
$SYS_MAXARTSIZE = 0;

# ������ƻ����ᥤ�륢�ɥ쥹�����Ϥ�ɬ�ܤȤ��ޤ���?
#   0: ɬ�ܤȤ��ʤ�
#   1: ɬ�ܤȤ���
$SYS_POSTERMAIL = 1;

# �����ФΥݡ����ֹ��ɽ�����ޤ���?
#   0: ɽ�����ʤ�
#   1: (ɬ�פʤ��)ɽ������
#      HTTP�Υǥե���ȤǤ���80�֥ݡ��Ȥξ�硤1�����ꤷ�Ƥ�ɽ�����ޤ���
$SYS_PORTNO = 1;

# �����ȥХå����饦��ɥ��᡼����Ȥ��ޤ���?
#   0: �Ȥ�ʤ�
#   1: �Ȥ�
$SYS_NETSCAPE_EXTENSION = 1;

  # ��ǡ�1: �Ȥ��פ����ꤷ�����ϡ��ʲ�����ꤷ�Ƥ���������
  $BG_IMG = "";
  $BG_COLOR = "#CCCCCC";
  $TEXT_COLOR = "#000000";
  $LINK_COLOR = "#0000AA";
  $ALINK_COLOR = "#FF0000";
  $VLINK_COLOR = "#00AA00";

# �ʲ��γƵ�ǽ�����Ѳ�ǽ�Ȥ��ޤ���?
#   0: ���ѤǤ��ʤ�
#   1: ���ѤǤ���
$SYS_F_T = 1;	# ��ץ饤�����ΤޤȤ��ɤߤ�ɽ��
$SYS_F_N = 1;	# ���������
$SYS_F_R = 1;	# �����ȥ����(���ս�)��ɽ��
$SYS_F_L = 1;	# �Ƕ�ε���������ɽ��
$SYS_F_S = 1;	# �����θ���
$SYS_F_B = 1;	# �Ǽ��İ�����ɽ��
  #
  # ����ʲ��Υ��ޥ�ɤ�ɬ����
  # �������������������¤򤫤�����ǡ����Ѥ��Ƥ�������
  # �ʾܤ����ϥ��󥹥ȥ졼�����ޥ˥奢��򻲾Ȥ��Ƥ��������ˡ�
  # �Ǥʤ����˲�Ū�ʰ�����ƿ̾�Ǥ�������Ǥ�����͡�
  # [���] ������ץȤ�̾�����Ѥ������餤�������ܤǤ��补(^_^;
  #
  #   0: ���ѤǤ��ʤ�
  #   1: ���ѤǤ���
  $SYS_F_D = 0;	# �����κ��������
  $SYS_F_MV = 0;	# �����Ρ�������/������-��ץ饤�ط��פ��ѹ�
  $SYS_F_AM = 0;	# ���嵭��������Υᥤ�������������

###
## ���ᥤ���������
#
# �ᥤ���ۿ������ӥ������Ѥ��ޤ���? �ʲ�����ɤ줫��Ĥ�����Ǥ���������
#   $SYS_MAIL = 0 + 0;		# ���Ѥ��ʤ���
#   $SYS_MAIL = 1 + 0;		# �ۿ��ᥤ��Τ߻Ȥ���
#   $SYS_MAIL = 0 + 2;		# ��ץ饤�ᥤ��Τ߻Ȥ���
#   $SYS_MAIL = 1 + 2;		# �ۿ��ᥤ��ȥ�ץ饤�ᥤ���ξ����Ȥ���
$SYS_MAIL = 1 + 2;

  # ���ǡ����Ѥ��ʤ��פ���ꤷ�����ϡ��ʲ��������ɬ�פϤ���ޤ���

  # �ᥤ�륵���Ф���ꤷ�Ƥ���������
  #   ��: $SMTP_SERVER = 'mail.foo.bar.ne.jp';
  #       $SMTP_SERVER = '123.456.78.90';
  $SMTP_SERVER = 'localhost';

  # ��������ᥤ���Subject�ˡ�[�Ǽ���: �ֹ�]�פ��䤤�ޤ���?
  #   0: ���ʤ� �� ��Subject: ��סʷǼ��Ĥȵ����ֹ��X-Kb-*������ޤ���
  #   1: �䤦     �� ��Subject: [�Ǽ���: �����ֹ�] ���
  $SYS_MAILHEADBRACKET = 1;

  # ��������ᥤ��Υإå���To:�פ˽񤫤�밸�����ꤷ�Ƥ���������
  # ��ά����ȡ������������Υᥤ�륢�ɥ쥹�����餺���¤Ӥޤ���
  # ��ư�ۿ���ǽ��ᥤ��󥰥ꥹ�ȤΤ褦�ˤ��ƻȤ��ʤ顤
  # $MAILTO_LABEL = '�ʤҤ��Τܤ��桼�� <nakahiro@sarion.co.jp>';
  # �ʤɤȤ���Ȥ������⤷��ޤ���
  $MAILTO_LABEL = '';

  # ��������ᥤ��Υإå���From:�פ˽񤫤��̾����
  # �����ƥ�����Ԥ�̾���Ȥ��Ѥ��������˻��ꤷ�Ƥ���������
  # ��ά����ȡ����Υե��������Ƭ�����ꤷ��$MAINT_NAME���Ȥ��ޤ���
  # $MAILFROM_LABEL = 'Kinoboards Mail Daemon';
  # �ʤɡ�
  $MAILFROM_LABEL = '';

  # CGI��ư�������С����̤�WWW�����ФǤ����ᥤ�륵���Ф��㤢��ޤ����
  # �Ρ�OS�Υ����פ˹��פ���Ԥ�������Ƭ�Ρ�#�פ�������Ƥ���������
  # OS�Υ����פϡ�telnet���ơ�uname -sr�פȤ������ޥ�ɤǤ狼��ޤ���
  # telnet�Ǥ��ʤ���硤�ץ�Х����⤷���ϴ����Ԥ�����䤤��碌�Ƥ���������
  #
  # �ʲ��򸫤�ĺ����Ф狼���̤ꡤ
  # ¿����OS�ǡ�$AF_INET��2��$SOCK_STREAM��1�����ꤷ�ޤ���
  # �����Ф�Solaris/2.*�οͤ�����$SOCK_STREM��2�����ꤷ�Ƥ���������
  #
  $AF_INET = 2; $SOCK_STREAM = 1;	# SunOS 4.*
  # $AF_INET = 2; $SOCK_STREAM = 2;	# SunOS 5.*(Solaris 2.*)
  # $AF_INET = 2; $SOCK_STREAM = 1;	# HP-UX
  # $AF_INET = 2; $SOCK_STREAM = 1;	# AIX
  # $AF_INET = 2; $SOCK_STREAM = 1;	# Linux
  # $AF_INET = 2; $SOCK_STREAM = 1;	# FreeBSD
  # $AF_INET = 2; $SOCK_STREAM = 1;	# IRIX
  # $AF_INET = 2; $SOCK_STREAM = 1;	# WinNT/95
  # $AF_INET = 2; $SOCK_STREAM = 1;	# Mac

  # ����¾���Ȥ߹�碌���¸�Τ���������ޤ����顤
  # �ʤ�(nakahiro@sarion.co.jp)�ޤǸ�Ϣ����������

###
## ���Ǽ��İ���������URL
#
#  �ַǼ��İ����ءפǥ�󥯤������kb�ǥ��쥯�ȥ꤫�������URL�ǻ��ꤷ�ޤ���
#  ���ʤ�kb�ǥ��쥯�ȥ��(��äơ�����Ū�ˤ�index.html��index.shtml��)��
#  '-'����ꤹ��ȡ���ʬ���Ѱդ����ե�����Ǥʤ�CGI����ư��������Ǽ��İ����ء�
#  ���줾���󥯤���ޤ���
#
$BOARDLIST_URL = './';			# kb�ǥ��쥯�ȥ��
# $BOARDLIST_URL = '-';			# CGI����ư��������Ǽ��İ�����
# $BOARDLIST_URL = 'kb10.shtml';	# kb/kb10.shtml��

###
## �������Ϲ��ܤ��礭��
#
$SUBJECT_LENGTH = 60;		# ��
$TEXT_ROWS = 15;		# �����Կ�
$TEXT_COLS = 72;		# ������
$NAME_LENGTH = 60;		# ̾����
$MAIL_LENGTH = 60;		# E-mail��
$URL_LENGTH = 72;		# URL��
$KEYWORD_LENGTH = 60;		# �������������
$DEF_TITLE_NUM = 20;		# �����ȥ������ɽ�����륿���ȥ�ο�
				# 0�ˤ������������ɽ������褦�ˤʤ�ޤ���
###
## �����ϥڡ����δ���������
#
$CHARSET = 'euc';		# �����������Ѵ���Ԥʤ��ޤ��󡥤��Τܤ���
				# core���Ǥ����ˤϡ���������ꤷ�Ƥ���������
# $CHARSET = 'jis';
# $CHARSET = 'sjis';

###
## �����Ѥη���
#
# ���ѻ����������κ��̾��Ĥ��ޤ���?
#   0: �Ĥ��ʤ�		�� ] ���Ѹ�������������
#   1: �Ĥ���		�֤ʤ� ] ���Ѹ�������������
$SYS_QUOTENAME = 1;
#
# ���ѥޡ���
#   ��>�פ��&gt;�פ���ѥޡ����ˤ���Τ��򤱤Ʋ�������
#   �ȥ�֥�򵯤����֥饦����¸�ߤ��ޤ���
$DEFAULT_QMARK = ' ] ';

###
## ������������礭��
#
# �����Υ֥饦���Ǥϡ����ο��ͤ�Ŭ���˻��ꤹ��ȡ�
# ����˥�������γ���̾���ԤʤäƤ���ޤ���
#
# ���ޥ�ɥ�������(���ء���)
$COMICON_HEIGHT = 20;		# �⤵[dot]
$COMICON_WIDTH = 20;		# ��[dot]
# ��å�������������(���ܰ��ڡ���)
$MSGICON_HEIGHT = 20;		# �⤵[dot]
$MSGICON_WIDTH = 20;		# ��[dot]

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
$H_USER = "�桼��";
$H_URL = "URL";
$H_URL_S = "�ۡ���ڡ�����URL(��̾�������󥯤�ĥ��ޤ�; ��ά���Ƥ⹽���ޤ���)";
$H_DATE = "�����";
$H_REPLY = "��ץ饤";
$H_ORIG = "$H_REPLY��";
$H_ORIG_TOP = "���ꥸ�ʥ�";
$H_LINE = "<p>------------------------------</p>";
$H_THREAD = "��";
$H_NEWARTICLE = "[new!]";

$H_TEXTTYPE = "�񤭹��߷���";
@H_TTLABEL = ( "���Τޤ�ɽ��", "HTML���Ѵ�", "HTML������" );
@H_TTMSG = ( "��$H_TEXTTYPE�פ��$H_TTLABEL[0]�פˤ���$H_MESG��񤯤ȡ�ɽ���κݤˤ��Τޤ�ɽ������ޤ���", "��$H_TTLABEL[1]�פˤ���ȡ����Ԥ�����ζ��ڤȤ���HTML�˼�ư�Ѵ����ޤ���", "��$H_TTLABEL[2]�פˤ���HTML�Ȥ��ƽ񤯤ȡ�ɽ���λ���HTML��������ޤ���" );

$H_NOICON = "�ʤ�";
$H_BACKBOARD = "$H_BOARD������";
$H_BACKTITLEREPLY = "$H_SUBJECT������($H_REPLY��)";
$H_BACKTITLEDATE = "$H_SUBJECT������(���ս�)";	# ���ˤ����ɽ������ޤ���
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


# $Id: kb.ph,v 5.9 1998-10-22 15:55:52 nakahiro Exp $


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
