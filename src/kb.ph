# $Id: kb.ph,v 4.1 1996-04-09 03:22:55 nakahiro Exp $
#
# $Log: kb.ph,v $
# Revision 4.1  1996-04-09 03:22:55  nakahiro
# A little bug(around " in articles) fixed.
# Copyright message added to the head of source codes.
# This program is free software(GPL ver.2).
#
# Revision 3.4  1996/03/28 09:53:32  nakahiro
# Modified articles DB structure. (Add list of articles followed)


# KINOBOARDS: Kinoboards Is Network Opened BOARD System
# Copyright (C) 1995-96 NAKAMURA Hiroshi.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PRATICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.


#/////////////////////////////////////////////////////////////////////


# This file implements Site Specific Definitions.


#
# �����Ԥ�e-mail addr.
#
$MAINT = "nakahiro\@kinotrope.co.jp";

#
# where is this program?
# `relative' or the others (ex. `absolutive').
#
# CAUTION: this option does not work now...
#
$SYS_SCRIPTPATH = 'relative';

#
# sendmail�Υѥ��ȥ��ץ����
#
$MAIL2 = "/usr/lib/sendmail -oi -t";

#
# ���ɽ��
#
$ADDRESS = "KINOBOARDS: Copyright (C) 1995-96 <a href=\"http://www.kinotrope.co.jp/~nakahiro/\">NAKAMURA Hiroshi</a>.";


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

# ���ѻ��˥�����Ĥ����ݤ�
#   0: �Ĥ��ʤ�
#   1: �Ĥ�
$SYS_TAGINQUOTE = 0;

# ������������Ѥ��뤫�ݤ�
#   0: ���Ѥ��ʤ�
#   1: ���Ѥ���
$SYS_ICON = 1;

# ������Ƶ���������������Ƥ����������������Ƥ�����
#   0: ��
#   1: ��
$SYS_BOTTOMTITLE = 0;

# �᡼�����������ӥ������Ѥ��뤫�ݤ�(���ܸ�Τ�)
#   0: ���Ѥ��ʤ�
#   1: ���Ѥ���
$SYS_FOLLOWMAIL = 1;

# �����Υإå��˥ޥ���̾��ɽ�����뤫�ݤ�
#   0: ɽ�����ʤ�
#   1: ɽ������
$SYS_SHOWHOST = 1;

# �����ȥ�ꥹ�Ȥ˿�����Ƶ����Τߤ�ɽ�����뤫�ݤ�
#   0: ȿ����ޤ�Ƥ��٤�
#   1: ������Ƶ����Τ�
$SYS_NEWARTICLEONLY = 0;

# �鿴���Ѥ˥����ȥ�ꥹ�Ȥ�˿BBS�饤���ˤ��뤫�ݤ�(�������Ѱդ������ʤ� ;_;)
# �����1�ˤ���ȡ�$SYS_NEWARTICLEONLY�ϸ����ʤ��ʤ�(1�˸���)��
# �����1�ˤ���ȡ�$SYS_ICON�ϸ����ʤ��ʤ�(0�˸���)��
#   0: ���ʤ�
#   1: ����
$SYS_FIN_LIKE = 0;

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
$VIEW_MSG = "�����ȥ����";
$SORT_MSG = "�����ȥ����(���ս�)";
$NEWARTICLE_MSG = "������ޤȤ���ɤ�";
$THREADARTICLE_MSG = "ȿ���ޤȤ��ɤ�";
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
$H_AORI = "�ꡢ��������̾�����᡼�륢�ɥ쥹������˥ۡ���ڡ����򤪻���������URL(��ά��)��񤭹���Ǥ���������<strong>�����Ϥ��Τޤޡ��᡼���Ʊ���褦�˽񤤤Ƥ��������OK�Ǥ�</strong>��<br>��������HTML��¸�������ϡ���$H_TEXTTYPE�פ��$H_HTML�פˤ���HTML�Ȥ��ƽ񤤤�ĺ���ȡ�HTML������Ԥʤ��ޤ���";
$H_SEEICON = "��������򸫤�";
$H_SEEALIAS = "�����ꥢ���򸫤�";
$H_ALIASENTRY = "��Ͽ����";
$H_ALIASINFO = "�����ꥢ������Ͽ����Ƥ������ϡ���$H_FROM�פˡ�#...�פȽ񤱤С�̾����᡼�롢URL���ά�Ǥ��ޤ���";
$H_PREVIEW_OR_ENTRY = "�񤭹�������Ƥ�";
$H_PREVIEW = "���ɽ�����Ƥߤ�(�ޤ���Ƥ��ޤ���)";
$H_ENTRY = "�����Ȥ�����Ƥ���";
$H_PUSHHERE = "�����򲡤��Ƥ�������";
$H_NOTHING = "����ޤ���";
$H_ICONINTRO = "�Ǥϼ��Υ��������Ȥ����Ȥ��Ǥ��ޤ���";
$H_POSTINFO = "ɬ�פǤ���С���äƽ񤭹��ߤ������Ʋ��������������Хܥ���򲡤��ƽ񤭹��ߤޤ��礦��";
$H_THANKSMSG = "�񤭹��ߤ���������äʤɤϥ᡼��Ǥ��ꤤ�������ޤ���";
$H_BACK = "���";
$H_COMMAND = "�¹�";
$H_NEXTARTICLE = "���ε�����";
$H_POSTNEWARTICLE = "��������Ƥ���";
$H_REPLYTHISARTICLE = "���ε�����ȿ������";
$H_REPLYTHISARTICLEQUOTE = "���Ѥ���ȿ������";
$H_READREPLYALL = "����ޤǤ�ȿ���򸫤�";
$H_ARTICLES = "������";
$H_JUMPID = "���ο����򥯥�å�����ȡ�����ID�ε��������Ӥޤ��������������ۤɾ�����ˤ���ޤ���";
$H_KEYWORD = "�������";
$H_INPUTKEYWORD = "�����ϰϤ��ǧ����$H_KEYWORD�����Ϥ��Ƥ���������";
$H_SEARCHKEYWORD = "��������";
$H_RESETKEYWORD = "�ꥻ�åȤ���";
$H_SEARCHTARGET = "�����ϰ�";
$H_SEARCHTARGETSUBJECT = "�����ȥ�";
$H_SEARCHTARGETPERSON = "��Ƽ�̾";
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


#/////////////////////////////////////////////////////////////////////
1;
