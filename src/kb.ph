# $Id: kb.ph,v 4.12 1996-11-19 12:08:22 nakahiro Exp $


# KINOBOARDS: Kinoboards Is Network Opened BOARD System
# Copyright (C) 1995, 96 NAKAMURA Hiroshi.
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
#
$MAINT_NAME = 'KinoAdmin';
$MAINT = 'nakahiro@kinotrope.co.jp';

#
# sendmail�Υѥ��ȥ��ץ����
#
$MAIL2 = '/usr/lib/sendmail -oi -t';

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

# ������������Ѥ��뤫�ݤ�
#   0: ���Ѥ��ʤ�
#   1: ���Ѥ���
$SYS_ICON = 1;

# ������Ƶ���������������Ƥ����������������Ƥ�����(�����ȥ�����λ�)
#   0: ��
#   1: ��
$SYS_BOTTOMTITLE = 0;

# ������Ƶ���������������Ƥ����������������Ƥ�����(���������λ�)
#   0: ��
#   1: ��
$SYS_BOTTOMARTICLE = 1;

# �᡼�����������ӥ������Ѥ��뤫�ݤ�(���ܸ�Τ�)
#   0: ���Ѥ��ʤ�
#   1: ���Ѥ���
$SYS_FOLLOWMAIL = 1;

# �����Υإå��˥ޥ���̾��ɽ�����뤫�ݤ�
#   0: ɽ�����ʤ�
#   1: ɽ������
$SYS_SHOWHOST = 1;

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

# ������ƻ����᡼�륢�ɥ쥹�����Ϥ�ɬ�ܤȤ��뤫
#   0: ɬ�ܤȤ��ʤ�
#   1: ɬ�ܤȤ���
$SYS_POSTERMAIL = 1;

#
# ���ѥޡ���
#
#	��>�פ��&gt;�פ���ѥޡ����ˤ���Τ��򤱤Ʋ�������
#	�ȥ�֥�򵯤����֥饦����¸�ߤ��ޤ���
#
$DEFAULT_QMARK = " ] ";

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
# ��å����������
#
$SYSTEM_NAME = "���Τܡ���";

$H_BOARD = "�Ǽ���";
$H_ICON = "��������";
$H_SUBJECT = "��";
$H_MESG = "��å�����";
$H_ALIAS = "�����ꥢ��";
$H_FROM = "��̾��";
$H_MAIL = "�᡼�륢�ɥ쥹";
$H_HOST = "�ޥ���";
$H_URL = "URL(��ά��)";
$H_DATE = "�����";
$H_REPLY = "��ץ饤";
$H_ORIG = "$H_REPLY��";

$ENTRY_MSG = "$H_MESG�ν񤭹���";
$SHOWICON_MSG = "�������������";
$PREVIEW_MSG = "�񤭹��ߤ����Ƥ��ǧ���Ƥ�������";
$THANKS_MSG = "�񤭹��ߤ��꤬�Ȥ��������ޤ���";
$VIEW_MSG = "�����ȥ����($H_REPLY��)";
$SORT_MSG = "�����ȥ����(���ս�)";
$NEWARTICLE_MSG = "�Ƕ��$H_MESG��ޤȤ��ɤ�";
$THREADARTICLE_MSG = "$H_REPLY��ޤȤ��ɤ�";
$SEARCHARTICLE_MSG = "$H_MESG�θ���";
$ALIASNEW_MSG = "�����ꥢ������Ͽ/�ѹ�/���";
$ALIASMOD_MSG = "�����ꥢ�����ѹ�����ޤ���";
$ALIASDEL_MSG = "�����ꥢ�����������ޤ���";
$ALIASSHOW_MSG = "�����ꥢ���λ���";
$ERROR_MSG   = "$SYSTEM_NAME: ERROR!";

$H_LINE = "------------------------------";
$H_THREAD = "��";
$H_FOLLOW = "��$H_REPLY";
$H_FMAIL = "$H_REPLY�����ä����˥᡼����Τ餻�ޤ���?";

$H_TEXTTYPE = "ɽ������";
$H_HTML = "HTML�Ȥ���ɽ������";
$H_PRE = "���Τޤ�ɽ������";

$H_NOICON = "�ʤ�";

# ������ʸ
$H_REPLYMSG = "���$H_MESG�ؤ�$H_REPLY��񤭹���";
$H_AORI = ($SYS_TEXTTYPE)
    ? "$H_SUBJECT��$H_MESG��$H_FROM��$H_MAIL������˥ۡ���ڡ����򤪻���������$H_URL��񤭹���Ǥ���������<strong>$H_MESG�ϥ᡼���Ʊ���褦�ˡ����Τޤ޽񤤤Ƥ��������OK�Ǥ�</strong>��<br>
������HTML��¸�������ϡ���$H_TEXTTYPE�פ��$H_HTML�פˤ��ơ�$H_MESG��HTML�Ȥ��ƽ񤤤�ĺ���ȡ�HTML������Ԥʤ��ޤ���"
    : "$H_SUBJECT��$H_MESG��$H_FROM��$H_MAIL������˥ۡ���ڡ����򤪻���������$H_URL��񤭹���Ǥ���������<strong>$H_MESG�ϥ᡼���Ʊ���褦�ˡ����Τޤ޽񤤤Ƥ��������OK�Ǥ�</strong>��";
$H_SEEICON = "�������������";
$H_SEEALIAS = "�����ꥢ���ΰ���";
$H_ALIASENTRY = "��Ͽ����";
$H_ALIASINFO = "�֥����ꥢ���פˡ�$H_FROM��$H_MAIL��$H_URL����Ͽ�ʤ��äƤ������ϡ���$H_FROM�פˡ�#...�פȤ�����Ͽ̾��񤤤Ƥ�����������ưŪ��$H_FROM��$H_MAIL��$H_URL������ޤ���";
$H_PREVIEW_OR_ENTRY = "�񤭹�������Ƥ�";
$H_PREVIEW = "���ɽ�����Ƥߤ�(�ޤ���Ƥ��ޤ���)";
$H_ENTRY = "$H_MESG����Ƥ���";
$H_PUSHHERE_POST = "���ޥ�ɼ¹�";
$H_NOTHING = "����ޤ���";
$H_ICONINTRO_ENTRY = "�Ǥϡ����Υ��������Ȥ����Ȥ��Ǥ��ޤ���";
$H_ICONINTRO_ARTICLE = "�ƥ�������ϼ��ε�ǽ��ɽ���Ƥ��ޤ���";
$H_POSTINFO = "ɬ�פǤ���С���äƽ񤭹��ߤ������Ƥ����������������Хܥ���򲡤��ƽ񤭹��ߤޤ��礦��";
$H_PUSHHERE_PREVIEW = "��Ƥ���";
$H_THANKSMSG = "�񤭹��ߤ���������äʤɤϡ��᡼���<a href=\"mailto:$MAINT\">$MAINT</a>�ޤǸ�Ϣ����������";
$H_BACK = "�����ȥ���������ޤ�";
$H_NEXTARTICLE = "����$H_MESG��";
$H_POSTNEWARTICLE = "��������Ƥ���";
$H_REPLYTHISARTICLE = "$H_REPLY��񤭹���";
$H_REPLYTHISARTICLEQUOTE = "���Ѥ���$H_REPLY��񤭹���";
$H_READREPLYALL = "$H_REPLY��ޤȤ��ɤ�";
$H_ARTICLES = "$H_MESG��";
$H_KEYWORD = "�������";
$H_SEARCHKEYWORD = "��������";
$H_RESETKEYWORD = "�ꥻ�åȤ���";
$H_SEARCHTARGET = "�����ϰ�";
$H_SEARCHTARGETSUBJECT = "��";
$H_SEARCHTARGETPERSON = "̾��";
$H_SEARCHTARGETARTICLE = "��å�����";
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
$H_ALIASTITLE = "������Ͽ/��Ͽ���Ƥ��ѹ�";
$H_ALIASNEWCOM = "�����ꥢ���ο�����Ͽ/��Ͽ���Ƥ��ѹ���Ԥʤ��ޤ��������������ɻߤΤ��ᡤ�ѹ��ϡ���Ͽ�κݤ�Ʊ���ޥ���Ǥʤ���ФǤ��ޤ����ѹ��Ǥ��ʤ����ϡ�<a href=\"mailto:$MAINT\">$MAINT</a>�ޤǥ᡼��Ǥ��ꤤ���ޤ���";
$H_ALIASNEWPUSH = "��Ͽ/�ѹ�����";
$H_ALIASDELETE = "���";
$H_ALIASDELETECOM = "�嵭�����ꥢ���������ޤ���Ʊ������Ͽ�κݤ�Ʊ���ޥ���Ǥʤ���к���Ǥ��ޤ���";
$H_ALIASDELETEPUSH = "�������";
$H_ALIASREFERPUSH = "�����ꥢ�������򻲾Ȥ���";
$H_ALIASCHANGED = "�ѹ����ޤ�����";
$H_ALIASENTRIED = "��Ͽ���ޤ�����";
$H_ALIASDELETED = "�õ�ޤ�����";
$H_AORI_ALIAS = "��Ƥκݡ���$H_FROM�פ���ʬ�˰ʲ�����Ͽ̾(��#....��)�����Ϥ���ȡ���Ͽ����Ƥ���$H_FROM��$H_MAIL��$H_URL����ưŪ������ޤ���";
$H_BACKART = "�����˽񤭹��ޤ줿$H_MESG��";
$H_NEXTART = "�ʹߤ˽񤭹��ޤ줿$H_MESG��";
$H_TOP = "��";
$H_BOTTOM = "��";
$H_NOARTICLE = "�������뵭��������ޤ���";


#/////////////////////////////////////////////////////////////////////
1;
