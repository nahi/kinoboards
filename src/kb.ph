# $Id: kb.ph,v 4.17 1997-03-13 15:18:21 nakahiro Exp $


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
$MAINT_NAME = 'KinoAdmin';
$MAINT = 'nakahiro@kinotrope.co.jp';

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
# ������ץȤΥᥤ��δ���������(EUC����ʤ���ư���ޤ���)
#
$SCRIPT_KCODE = 'euc';

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
#   0: ���Ѥ��ʤ�
#   1: ���Ѥ���
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

#
# ���ѥޡ���
#
#	��>�פ��&gt;�פ���ѥޡ����ˤ���Τ��򤱤Ʋ�������
#	�ȥ�֥�򵯤����֥饦����¸�ߤ��ޤ���
#
$DEFAULT_QMARK = ' ] ';

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

#
# �����ȥ������ɽ�����륿���ȥ�ο�
#
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

$ENTRY_MSG = "$H_MESG�ν񤭹���";
$SHOWICON_MSG = "�������������";
$PREVIEW_MSG = "�񤭹��ߤ����Ƥ��ǧ���Ƥ�������";
$THANKS_MSG = "�񤭹��ߤ��꤬�Ȥ��������ޤ���";
$VIEW_MSG = "$H_SUBJECT����($H_REPLY��)";
$SORT_MSG = "$H_SUBJECT����(���ս�)";
$NEWARTICLE_MSG = "�Ƕ��$H_MESG��ޤȤ��ɤ�";
$THREADARTICLE_MSG = "$H_REPLY��ޤȤ��ɤ�";
$SEARCHARTICLE_MSG = "$H_MESG�θ���";
$ALIASNEW_MSG = "$H_ALIAS����Ͽ/�ѹ�/���";
$ALIASMOD_MSG = "$H_ALIAS�����ꤵ��ޤ���";
$ALIASDEL_MSG = "$H_ALIAS���������ޤ���";
$ALIASSHOW_MSG = "$H_ALIAS�λ���";
$ERROR_MSG   = "$SYSTEM_NAME: ERROR!";

$H_LINE = "------------------------------";
$H_THREAD = "��";
$H_FOLLOW = "��$H_REPLY";
$H_TEXTTYPE = "ɽ������";
$H_HTML = "HTML�Ȥ���ɽ������";
$H_PRE = "���Τޤ�ɽ������";
$H_NOICON = "�ʤ�";

# ������ʸ
$H_REPLYMSG = "���$H_MESG�ؤ�$H_REPLY��񤭹���";
$H_AORI_1 = "$H_SUBJECT��$H_MESG��$H_FROM��$H_MAIL������˥����֥ڡ����򤪻��������ϡ��ۡ���ڡ�����$H_URL��񤭹���Ǥ���������";
$H_AORI_2 = "HTML��¸�������ϡ���$H_TEXTTYPE�פ��$H_HTML�פˤ��ơ�$H_MESG��HTML�Ȥ��ƽ񤤤�ĺ���ȡ�ɽ���λ���HTML������Ԥʤ��ޤ���";
$H_SEEICON = "�������������";
$H_SEEALIAS = "$H_ALIAS�ΰ���";
$H_ALIASENTRY = "��Ͽ����";
$H_ALIASINFO = "��$H_ALIAS�פˡ�$H_FROM��$H_MAIL��$H_URL����Ͽ�ʤ��äƤ������ϡ���$H_FROM�פˡ�#...�פȤ�����Ͽ̾��񤤤Ƥ�����������ưŪ��$H_FROM��$H_MAIL��$H_URL������ޤ���";
$H_FMAIL = "$H_REPLY�����ä����˥ᥤ����Τ餻�ޤ���?";
$H_LINK = "$H_MESG��˴�Ϣ�����֥ڡ����ؤΥ�󥯤�ĥ����ϡ���&lt;URL:http://��&gt;�פΤ褦�ˡ�URL���&lt;URL:�פȡ�&gt;�פǰϤ�ǽ񤭹���Ǥ�����������ưŪ�˥�󥯤�ĥ���ޤ���";
$H_PREVIEW_OR_ENTRY = "�񤭹�������Ƥ�";
$H_PREVIEW = "���ɽ�����Ƥߤ�(�ޤ���Ƥ��ޤ���)";
$H_ENTRY = "$H_MESG����Ƥ���";
$H_PUSHHERE_POST = "���ޥ�ɼ¹�";
$H_NOTHING = "����ޤ���";
$H_ICONINTRO_ENTRY = "�Ǥϡ����Υ��������Ȥ����Ȥ��Ǥ��ޤ���";
$H_ICONINTRO_ARTICLE = "�ƥ�������ϼ��ε�ǽ��ɽ���Ƥ��ޤ���";
$H_POSTINFO = "ɬ�פǤ���С��֥饦����BACK�ܥ������äơ��񤭹��ߤ������Ƥ����������������Хܥ���򲡤��ƽ񤭹��ߤޤ��礦��";
$H_DIRECTLINK = "($H_MESG�Ϥ���ޤ���$H_SUBJECT��������ϡ�ľ�ܰʲ���URL�˥�󥯤�ĥ���ޤ�������褬���������Ȥ��ǧ���Ƥ���������)";
$H_PUSHHERE_PREVIEW = "��Ƥ���";
$H_THANKSMSG = "�񤭹��ߤ���������äʤɤϡ��ᥤ���<a href=\"mailto:$MAINT\">$MAINT</a>�ޤǸ�Ϣ����������";
$H_BACKTITLE = "$H_SUBJECT������";
$H_BACKORG = "$H_ORIG��$H_MESG��";
$H_PREVARTICLE = "����$H_MESG��";
$H_NEXTARTICLE = "����$H_MESG��";
$H_POSTNEWARTICLE = "�����˽񤭹���";
$H_REPLYTHISARTICLE = "$H_REPLY��񤭹���";
$H_REPLYTHISARTICLEQUOTE = "���Ѥ���$H_REPLY��񤭹���";
$H_READREPLYALL = "$H_REPLY��ޤȤ��ɤ�";
$H_ARTICLES = "$H_MESG��";
$H_KEYWORD = "�������";
$H_SEARCHKEYWORD = "��������";
$H_RESET = "�ꥻ�åȤ���";
$H_SEARCHTARGET = "�����ϰ�";
$H_SEARCHTARGETSUBJECT = "$H_SUBJECT";
$H_SEARCHTARGETPERSON =  "̾��";
$H_SEARCHTARGETARTICLE = "$H_MESG";
$H_INPUTKEYWORD = "<p>
<ul>
<li>��$H_SEARCHTARGETSUBJECT�ס���$H_SEARCHTARGETPERSON�ס���$H_SEARCHTARGETARTICLE�פ��椫�顤���������ϰϤ�����å����Ƥ���������
���ꤵ�줿�ϰϤǡ�$H_KEYWORD��ޤ�$H_MESG�����ɽ�����ޤ���
<li>$H_KEYWORD�ˤϡ���ʸ����ʸ���ζ��̤Ϥ���ޤ���
<li>$H_KEYWORD��Ⱦ�ѥ��ڡ����Ƕ��ڤäơ�ʣ����$H_KEYWORD����ꤹ��ȡ�
��������Ƥ�ޤ�$H_MESG�Τߤ򸡺����뤳�Ȥ��Ǥ��ޤ���
<li>��������Ǹ���������ϡ�
�֥�������פ�����å������塤õ������$H_MESG�Υ������������Ǥ���������
</ul>
</p>";
$H_NOTFOUND = "��������$H_MESG�ϸ��Ĥ���ޤ���Ǥ�����";
$H_FOUNDNO = "���$H_MESG�����Ĥ���ޤ�����";
$H_ALIASTITLE = "������Ͽ/��Ͽ���Ƥ��ѹ�";
$H_ALIASNEWCOM = "$H_ALIAS�ο�����Ͽ/��Ͽ���Ƥ��ѹ���Ԥʤ��ޤ��������������ɻߤΤ��ᡤ�ѹ��ϡ���Ͽ�κݤ�Ʊ���ޥ���Ǥʤ���ФǤ��ޤ����ѹ��Ǥ��ʤ����ϡ�<a href=\"mailto:$MAINT\">$MAINT</a>�ޤǥᥤ��Ǥ��ꤤ���ޤ���";
$H_ALIASNEWPUSH = "��Ͽ/�ѹ�����";
$H_ALIASDELETE = "���";
$H_ALIASDELETECOM = "�嵭$H_ALIAS�������ޤ���Ʊ������Ͽ�κݤ�Ʊ���ޥ���Ǥʤ���к���Ǥ��ޤ���";
$H_ALIASDELETEPUSH = "�������";
$H_ALIASREFERPUSH = "$H_ALIAS�����򻲾Ȥ���";
$H_ALIASCHANGED = "���ꤷ�ޤ�����";
$H_ALIASENTRIED = "��Ͽ���ޤ�����";
$H_ALIASDELETED = "�õ�ޤ�����";
$H_AORI_ALIAS = "��Ƥκݡ���$H_FROM�פ���ʬ�˰ʲ�����Ͽ̾(��#....��)�����Ϥ���ȡ���Ͽ����Ƥ���$H_FROM��$H_MAIL��$H_URL����ưŪ������ޤ���";
$H_BACKART = "�����˽񤭹��ޤ줿$H_MESG��";
$H_NEXTART = "�ʹߤ˽񤭹��ޤ줿$H_MESG��";
$H_TOP = "��";
$H_BOTTOM = "��";
$H_NOARTICLE = "��������$H_MESG������ޤ���";


#/////////////////////////////////////////////////////////////////////
1;
