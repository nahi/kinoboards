# $Id: kb.ph,v 4.7 1996-08-05 18:41:44 nakahiro Exp $


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
#   0: ȿ����ޤ�Ƥ��٤�
#   1: ������Ƶ����Τ�
$SYS_NEWARTICLEONLY = 0;

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
# ���λ���
#
$BG_COLOR = "#66CCCC";
$TEXT_COLOR = "#000000";
$LINK_COLOR = "#0000AA";
$ALINK_COLOR = "#FF0000";
$VLINK_COLOR = "#00AA00";

#
# ��å����������
#
$SYSTEM_NAME = "���Τܡ���";

$ENTRY_MSG = "�����ν񤭹���";
$SHOWICON_MSG = "�������������";
$PREVIEW_MSG = "�񤭹��ߤ����Ƥ��ǧ���Ʋ�����";
$THANKS_MSG = "�񤭹��ߤ��꤬�Ȥ��������ޤ���";
$VIEW_MSG = "�����ȥ����(������)";
$SORT_MSG = "�����ȥ����(���ս�)";
$NEWARTICLE_MSG = "������ޤȤ���ɤ�";
$THREADARTICLE_MSG = "ȿ����ޤȤ���ɤ�";
$SEARCHARTICLE_MSG = "�����θ���";
$ALIASNEW_MSG = "�����ꥢ������Ͽ/�ѹ�/���";
$ALIASMOD_MSG = "�����ꥢ�����ѹ�����ޤ���";
$ALIASDEL_MSG = "�����ꥢ�����������ޤ���";
$ALIASSHOW_MSG = "�����ꥢ���λ���";
$DELETE_ENTRY_MSG = "�����κ��";
$DELETE_PREVIEW_MSG = "������뵭���γ�ǧ";
$DELETE_THANKS_MSG = "�����κ��";
$ERROR_MSG   = "$SYSTEM_NAME: ERROR!";

$H_LINE = "------------------------------";
$H_THREAD = "��";
$H_BOARD = "�Ǽ���:";
$H_ICON = "��������:";
$H_SUBJECT = "���ꡡ:";
$H_ALIAS = "�����ꥢ��:";
$H_FROM = "��̾��:";
$H_MAIL = "�᡼��:";
$H_HOST = "�ޥ���:";
$H_URL = "URL(��ά��):";
$H_DATE = "�����:";
$H_REPLY = "������:";
$H_ID = "�����ֹ�:";
$H_FOLLOW = "��ȿ��";
$H_FMAIL = "ȿ�����Ĥ������˥᡼����Τ餻��:";

$H_TEXTTYPE = "ɽ������:";
$H_HTML = "HTML�Ȥ���ɽ������";
$H_PRE = "���Τޤ�ɽ������";

$H_NOICON = "�ʤ�";

# ������ʸ
$H_REPLYMSG = "��ε�����ȿ������";
$H_AORI = "�ꡤ��������̾�����᡼�륢�ɥ쥹������˥ۡ���ڡ����򤪻���������URL(��ά��)��񤭹���Ǥ���������<strong>�����Ϥ��Τޤޡ��᡼���Ʊ���褦�˽񤤤Ƥ��������OK�Ǥ�</strong>��<br>��������HTML��¸�������ϡ���$H_TEXTTYPE�פ��$H_HTML�פˤ���HTML�Ȥ��ƽ񤤤�ĺ���ȡ�HTML������Ԥʤ��ޤ���";
$H_SEEICON = "�������������";
$H_SEEALIAS = "�����ꥢ���򸫤�";
$H_ALIASENTRY = "��Ͽ����";
$H_ALIASINFO = "�����ꥢ������Ͽ����Ƥ������ϡ���$H_FROM�פˡ�#...�פȽ񤱤С�̾����᡼�롤URL���ά�Ǥ��ޤ���";
$H_PREVIEW_OR_ENTRY = "�񤭹�������Ƥ�";
$H_PREVIEW = "���ɽ�����Ƥߤ�(�ޤ���Ƥ��ޤ���)";
$H_ENTRY = "�����Ȥ�����Ƥ���";
$H_PUSHHERE = "�����򲡤��Ƥ�������";
$H_NOTHING = "����ޤ���";
$H_ICONINTRO_ENTRY = "�Ǥϡ����ε������������Ȥ����Ȥ��Ǥ��ޤ���";
$H_ICONINTRO_ARTICLE = "�ƥ�������ϼ��ε�ǽ��ɽ���Ƥ��ޤ���";
$H_POSTINFO = "ɬ�פǤ���С���äƽ񤭹��ߤ������Ʋ��������������Хܥ���򲡤��ƽ񤭹��ߤޤ��礦��";
$H_THANKSMSG = "�񤭹��ߤ���������äʤɤϥ᡼��Ǥ��ꤤ�������ޤ���";
$H_BACK = "���";
$H_COMMAND = "�¹�";
$H_TITLELIST = "����������";
$H_NEXTARTICLE = "���ε�����";
$H_POSTNEWARTICLE = "��������Ƥ���";
$H_REPLYTHISARTICLE = "���ε�����ȿ������";
$H_REPLYTHISARTICLEQUOTE = "���Ѥ���ȿ������";
$H_READREPLYALL = "����ޤǤ�ȿ���򸫤�";
$H_ARTICLES = "������";
$H_JUMPID = "���ο����򥯥�å�����ȡ�����ID�ε��������Ӥޤ��������������ۤɾ�����ˤ���ޤ���";
$H_KEYWORD = "�������";
$H_INPUTKEYWORD = "<p>
<ul>
<li>����ס���̾���ס�����ʸ�פ��椫�顤���������ϰϤ�����å����Ƥ���������
���ꤵ�줿�ϰϤǡ�$H_KEYWORD��ޤ൭�������ɽ�����ޤ���
<li>$H_KEYWORD�ˤϡ���ʸ����ʸ���ζ��̤Ϥ���ޤ���
<li>$H_KEYWORD��Ⱦ�ѥ��ڡ����Ƕ��ڤäơ�ʣ����$H_KEYWORD����ꤹ��ȡ�
��������Ƥ�ޤ൭���Τߤ򸡺����뤳�Ȥ��Ǥ��ޤ���
<li>��������Ǹ���������ϡ�
�֥�������פ�����å������塤õ�����������Υ������������Ǥ���������
</ul>
</p>";
$H_SEARCHKEYWORD = "��������";
$H_RESETKEYWORD = "�ꥻ�åȤ���";
$H_SEARCHTARGET = "�����ϰ�";
$H_SEARCHTARGETSUBJECT = "��";
$H_SEARCHTARGETPERSON = "̾��";
$H_SEARCHTARGETARTICLE = "��ʸ";
$H_NOTFOUND = "�������뵭���ϸ��Ĥ���ޤ���Ǥ�����";
$H_ALIASTITLE = "������Ͽ/��Ͽ���Ƥ��ѹ�";
$H_ALIASNEWCOM = "�����ꥢ���ο�����Ͽ/��Ͽ���Ƥ��ѹ���Ԥʤ��ޤ����������ѹ��ϡ���Ͽ�κݤ�Ʊ���ޥ���Ǥʤ���ФǤ��ޤ����ѹ��Ǥ��ʤ����ϡ�<a href=\"mailto:$MAINT\">$MAINT</a>�ޤǥ᡼��Ǥ��ꤤ���ޤ���";
$H_ALIASNEWPUSH = "��Ͽ/�ѹ�����";
$H_ALIASDELETE = "���";
$H_ALIASDELETECOM = "�嵭�����ꥢ���������ޤ���Ʊ������Ͽ�κݤ�Ʊ���ޥ���Ǥʤ���к���Ǥ��ޤ���";
$H_ALIASDELETEPUSH = "�������";
$H_ALIASREFERPUSH = "�����ꥢ���򻲾Ȥ���";
$H_ALIASCHANGED = "�ѹ����ޤ�����";
$H_ALIASENTRIED = "��Ͽ���ޤ�����";
$H_ALIASDELETED = "�õ�ޤ�����";
$H_DELETE_ENTRY_TITLE = "������뵭���ε����ֹ�����Ϥ��Ʋ�����";
$H_DELETE_COM = "�����κ���ϡ���Ƥ����ޥ����Ʊ���ޥ��󤫤�Ǥʤ��ȤǤ��ޤ���";
$H_DELETE_PREVIEW_COM = "������뵭�����ǧ���Ʋ��������ܥ���򲡤��Ⱥ�����ޤ���";
$H_AORI_ALIAS = "��Ƥκݡ��֤�̾���פ���ʬ�˰ʲ��Ρ�#....�פ����Ϥ���ȡ���Ͽ����Ƥ��뤪̾����e-mail addr.��URL����ưŪ������ޤ���";
$H_CANNOTQUOTE = "���ꤵ�줿�����ϰ��ѤǤ��ޤ���";
$H_BACKART = "�����˽񤭹��ޤ줿������";
$H_NEXTART = "�ʹߤ˽񤭹��ޤ줿������";
$H_TOP = "��";
$H_BOTTOM = "��";
$H_NOARTICLE = "�������뵭��������ޤ���";


#/////////////////////////////////////////////////////////////////////
1;
