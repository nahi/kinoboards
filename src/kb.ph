# $Id: kb.ph,v 4.18 1997-06-24 15:42:06 nakahiro Exp $


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


# This file implements Site Specific Definitions of KINOBOARDS.


#
# �����Ԥ�̾����e-mail addr.
# �ᥤ�������˻Ȥ����ᡤ��$MAINT_NAME�פϥ���ե��٥åȤΤߤǻ��ꤷ�Ƥ���������
#
# ��:
# $MAINT_NAME = 'KinoboardsAdmin';
# $MAINT = 'nakahiro@kinotrope.co.jp';
#
$MAINT_NAME = 'YourName';
$MAINT = 'yourname@your.e-mail.domain';

#
# �����Ф�ư���Ƥ���ޥ���Ϥɤ�Ǥ���?
# ��������1�Ԥ�Ĥ��ƥ����ȥ����Ȥ��Ƥ���������
#
 $ARCH = 'UNIX';			# UNIX + Perl4/5
# $ARCH = 'WinNT';			# WinNT + Perl5
# $ARCH = 'Win95';			# Win95 + Perl5
# $ARCH = 'Mac';			# Mac + MacPerl

#
# UNIX�ξ���sendmail�Υѥ��ȥ��ץ�����
# Mac�ξ���SMTP server��ư���Ƥ���ޥ���Υۥ���̾��
# Win�ξ��ϥᥤ����������ե������
# ���ꤷ�Ƥ���������
#
$MAIL2 = '/usr/lib/sendmail -oi -t'	if ($ARCH eq 'UNIX');
$MAIL2 = 'SendMail'			if ($ARCH eq 'WinNT');
$MAIL2 = 'SendMail'			if ($ARCH eq 'Win95');
$MAIL2 = 'foo.bar.baz.co.jp'		if ($ARCH eq 'Mac');
#
# MacPerl�ǥᥤ��������ǽ���Ѥ���ˤϡ�
# <URL:ftp://mors.gsfc.nasa.gov/pub/MacPerl/Scripts/>
# ���֤���Ƥ��롤MacPerl�Ѥ�libnet��ɬ�פǤ���
# �ܤ�����doc/INSTALL.html���������������
#
# Win�ξ�硤���ΤȤ���ᥤ��������ǽ������ޤ���
# �ᥤ��Ϥ��٤ơ���ǻ��ꤷ��̾���Υե�����˽񤭽Ф���ޤ���
# �����1��1�󡤤��Υե������Ŭ����ʬ�䤷��
# ��ư����������Ȥ�����⤢��ޤ��͡�(^_^;
# WinNT�ˤ�sendmail������Ϥ��ʤΤǡ����Ĥ����б��������ġ�
#

#
# �����ƥ������
#
# ����ʸ�񥿥���(HTML or PRE)�������Ԥ����ݤ�(�Ԥʤ�ʤ���PRE�Τ�)
#   0: �Ԥ�ʤ�
#   1: �Ԥ�
$SYS_TEXTTYPE = 1;

# �����ꥢ�������Ѥ��뤫�ݤ�
#   0: ���Ѥ��ʤ�
#   1: ���Ѥ���
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

# ��ư�ᥤ���ۿ������ӥ������Ѥ��뤫�ݤ�
#   0: ���Ѥ��ʤ�
#   1: ���Ѥ���
$SYS_MAIL = 1;

# �����Υإå��˥ޥ���̾��ɽ�����뤫�ݤ�
#   0: ɽ�����ʤ�
#   1: ɽ������
$SYS_SHOWHOST = 0;

# �����Υإå��˥��ޥ�ɷ���ɽ�����뤫�ݤ�
#   0: ɽ�����ʤ�
#   1: ɽ������
$SYS_COMMAND = 1;

# �����ȥ�ꥹ�Ȥ˿�����Ƶ����Τߤ�ɽ�����뤫�ݤ�
#   0: ��ץ饤��ޤ�Ƥ��٤�
#   1: ������Ƶ����Τ�
$SYS_NEWARTICLEONLY = 0;

# �ͥåȥ������׳�ĥ�˴�Ť������ȥХå����饦��ɥ��᡼����Ȥ����ݤ�
#   0: �Ȥ�ʤ�
#   1: �Ȥ�
$SYS_NETSCAPE_EXTENSION = 1;

# ������ƻ����ᥤ�륢�ɥ쥹�����Ϥ�ɬ�ܤȤ��뤫
#   0: ɬ�ܤȤ��ʤ�
#   1: ɬ�ܤȤ���
$SYS_POSTERMAIL = 1;

# �����ФΥݡ����ֹ��ɽ�����뤫�ݤ�
#   0: ɽ�����ʤ�
#   1: (ɬ�פʤ��)ɽ������
#      ����Ū�ʥǥե���ȤǤ���80�֥ݡ��Ȥξ�硤1�����ꤷ�Ƥ�ɽ�����ޤ���
$SYS_PORTNO = 1;

# �ƥ��ޥ�ɤ�¹Բ�ǽ�Ȥ��뤫�ݤ�
#   0: �¹ԤǤ��ʤ�
#   1: �¹ԤǤ���
$SYS_F_E = 1;			# ������ɽ��
$SYS_F_T = 1;			# ��ץ饤�����ΤޤȤ��ɤߤ�ɽ��
$SYS_F_N = 1;			# �������������
$SYS_F_FQ = 1;			# ��ץ饤���������
$SYS_F_V = 1;			# �����ȥ����(��ץ饤��)��ɽ��
$SYS_F_R = 1;			# �����ȥ����(���ս�)��ɽ��
$SYS_F_L = 1;			# �Ƕ�ε���������ɽ��
$SYS_F_S = 1;			# �����θ���
$SYS_F_I = 1;			# ��������إ�פ�ɽ��

#
# ���ѥޡ���
#
#	��>�פ��&gt;�פ���ѥޡ����ˤ���Τ��򤱤Ʋ�������
#	�ȥ�֥�򵯤����֥饦����¸�ߤ��ޤ���
#
$DEFAULT_QMARK = ' ] ';

#
# ����������礭��
# �����Υ֥饦���Ǥϡ����ο��ͤ�Ŭ���˻��ꤹ��ȡ�
# ����˥�������γ���̾���ԤʤäƤ����褦�Ǥ���
#
# ���ޥ�ɥ�������(���ء���)
$COMICON_HEIGHT = 20;
$COMICON_WIDTH = 20;
# ��å�������������(���ܰ��ڡ���)
$MSGICON_HEIGHT = 20;
$MSGICON_WIDTH = 20;

#
# �����Ϲ��ܤ��礭��
#
# ��
$SUBJECT_LENGTH = 45;
# �����Կ�
$TEXT_ROWS = 15;
# ������
$TEXT_COLS = 50;
# ̾����
$NAME_LENGTH = 45;
# E-mail��
$MAIL_LENGTH = 45;
# URL��
$URL_LENGTH = 37;
# �������������
$KEYWORD_LENGTH = 40;

# �����ȥ������ɽ�����륿���ȥ�ο�
# 0�ˤ������������ɽ������褦�ˤʤ�ޤ���
$DEF_TITLE_NUM = 20;

#
# Netscape Extension�λ���
#
$BG_IMG = "";
$BG_COLOR = "#66CCCC";
$TEXT_COLOR = "#000000";
$LINK_COLOR = "#0000AA";
$ALINK_COLOR = "#FF0000";
$VLINK_COLOR = "#00AA00";

#
# URL�Ȥ��Ƶ��Ĥ���scheme
#
@URL_SCHEME = ('http', 'ftp', 'gopher');

#
# ��å����������
#
$SYSTEM_NAME = "���Τܡ���";
$H_BOARD = "�Ǽ���";
$H_ICON = "��������";
$H_SUBJECT = "�����ȥ�";
$H_MESG = "��å�����";
$H_ALIAS = "�����ꥢ��";
$H_FROM = "��̾��";
$H_MAIL = "�ᥤ��";
$H_HOST = "�ޥ���";
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
$H_PRE = "���Τޤ�ɽ������";
$H_NOICON = "�ʤ�";
$H_BACKTITLE = "$H_SUBJECT������";
$H_PREVARTICLE = "����$H_MESG��";
$H_NEXTARTICLE = "����$H_MESG��";
$H_POSTNEWARTICLE = "�����˽񤭹���";
$H_REPLYTHISARTICLE = "$H_REPLY��񤭹���";
$H_REPLYTHISARTICLEQUOTE = "���Ѥ���$H_REPLY��񤭹���";
$H_READREPLYALL = "$H_REPLY��ޤȤ��ɤ�";
$H_BACKART = "�����˽񤭹��ޤ줿$H_MESG��";
$H_NEXTART = "�ʹߤ˽񤭹��ޤ줿$H_MESG��";
$H_TOP = "��";
$H_BOTTOM = "��";
$H_NOARTICLE = "��������$H_MESG������ޤ���";


#/////////////////////////////////////////////////////////////////////
1;
