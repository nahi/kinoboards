# $Id: kb.ph,v 3.3 1996-02-11 06:54:09 nakahiro Exp $
#
# $Log: kb.ph,v $
# Revision 3.3  1996-02-11 06:54:09  nakahiro
# the 1st test version for my homepage.
#
# Revision 3.2  1996/02/08 07:11:04  nakahiro
# Bulletin board for KINOTROPE Inc.
#
# Revision 3.0  1996/01/20 14:01:35  nakahiro
# oow1
#
# Revision 2.1  1995/12/19 18:46:21  nakahiro
# send mail
#
# Revision 2.0  1995/12/19 14:27:25  nakahiro
# user writable alias file.
#
# Revision 1.3  1995/12/19 07:24:49  nakahiro
# MAINT
#
# Revision 1.1  1995/12/15 12:38:44  nakahiro
# Initial revision
#


# kinoBoards: Kinoboards Is Network Opened BOARD System


#/////////////////////////////////////////////////////////////////////


###
## �桼��������������(ư��������ɬ���ѹ�����ɬ�פ�����ޤ�)
#


##
# �����Ԥ�e-mail addr.
$MAINT = "nakahiro\@kinotrope.co.jp";

##
# where is this program?
# `relative' or the others (ex. `absolutive').
#
# CAUTION: this option does not work now...
#
$SYS_SCRIPTPATH = 'relative';

##
# sendmail�Υѥ��ȥ��ץ����
$MAIL2 = "/usr/lib/sendmail -oi -t";

##
# ���ɽ��
$ADDRESS = "Copyright 1996 <a href=\"http://www.kinotrope.co.jp/\">KINOTROPE Inc.</a> &amp; <a href=\"http://www.kinotrope.co.jp/~nakahiro/\">HiNa</a> // ��̵��ž��";


#/////////////////////////////////////////////////////////////////////


###
## �桼��������������(�ä��ѹ����ʤ��Ǥ�OK)
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

# ���ѻ��˥�����Ĥ����ݤ�
#   0: �Ĥ��ʤ�
#   1: �Ĥ�
$SYS_TAGINQUOTE = 1;

# ������Ƶ���������������Ƥ����������������Ƥ�����
#   0: ��
#   1: ��
$SYS_BOTTOMTITLE = 0;

# �᡼�����������ӥ������Ѥ��뤫�ݤ�(���ܸ�Τ�)
#   0: ���Ѥ��ʤ�
#   1: ���Ѥ���
$SYS_FOLLOWMAIL = 1;

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

$ENTRY_MSG = "$SYSTEM_NAME �ؤν񤭹���";
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
$ERROR_MSG   = "$SYSTEM_NAME: ERROR!";

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
$H_FOLLOW = "��ȿ��";
$H_FMAIL = "ȿ�����Ĥ������˥᡼����Τ餻��:";

$H_TEXTTYPE = "���Ϸ���:";
$H_HTML = "HTMLʸ��";
$H_PRE = "�����Ѥ�ʸ��";

$H_NOICON = "�ʤ�";

# ������ʸ
$H_REPLYMSG = "��ε�����ȿ������";
$H_AORI = "�ꡢ��������̾�����᡼�륢�ɥ쥹������˥ۡ���ڡ����򤪻���������URL(��ά��)��񤭹���Ǥ��������������ϡ�1�Ԥ򤢤ޤ�Ĺ��������Ŭ�����ޤ��֤��ƽ񤤤�ĺ�����ɤ߰פ��ʤ�ޤ���<br>HTML��¸�������ϡ���$H_TEXTTYPE�פ��$H_HTML�פˤ���HTML�Ȥ��ƽ񤤤�ĺ���ȡ�HTML������Ԥʤ��ޤ���";
$H_SEEICON = "��������򸫤�";
$H_SEEALIAS = "�����ꥢ���򸫤�";
$H_ALIASENTRY = "��Ͽ����";
$H_ALIASINFO = "�����ꥢ������Ͽ����Ƥ������ϡ���$H_FROM�פˡ�#...�פȽ񤯤ȡ���ưŪ���䴰����ޤ���";
$H_ENTRYINFO = "���ϤǤ��ޤ����顢�������ǧ���ޤ��礦(�ޤ���Ƥ��ޤ���)��";
$H_PUSHHERE = "�����򲡤��Ƥ�������";
$H_ICONINTRO = "��$BoardName�פǤϼ��Υ��������Ȥ����Ȥ��Ǥ��ޤ���";
$H_POSTINFO = "�ʲ��ε������ǧ�����顢�񤭹��ߤޤ��礦��";
$H_THANKSMSG = "�񤭹��ߤ���������äʤɤϥ᡼��Ǥ��ꤤ�������ޤ���";
$H_BACK = "���";
$H_NEXTARTICLE = "���ε�����";
$H_REPLYTHISARTICLE = "������ȿ��";
$H_REPLYTHISARTICLEQUOTE = "���Ѥ���ȿ��";
$H_READREPLYALL = "ȿ����ޤȤ��ɤ�";
$H_REPLYNOTE = " �� %s ����";
$H_ARTICLES = "������";
$H_JUMPID = "���ο����򥯥�å�����ȡ�����ID�ε��������Ӥޤ��������������ۤɾ�����ˤ���ޤ���";
$H_KEYWORD = "�������";
$H_INPUTKEYWORD = "$H_KEYWORD �����Ϥ��Ƥ����顢";
$H_NOTFOUND = "�������뵭���ϸ��Ĥ���ޤ���Ǥ�����";
$H_ALIASTITLE = "������Ͽ/��Ͽ���Ƥ��ѹ�";
$H_ALIASNEWCOM = "�����ꥢ���ο�����Ͽ/��Ͽ���Ƥ��ѹ����Ԥʤ��ޤ����������ѹ��ϡ���Ͽ�κݤ�Ʊ���ޥ���Ǥʤ���ФǤ��ޤ����ѹ��Ǥ��ʤ����ϡ�<a href=\"mailto:$MAINT\">$MAINT</a>�ޤǥ᡼��Ǥ��ꤤ���ޤ���";
$H_ALIASDELETE = "���";
$H_ALIASDELETECOM = "�嵭�����ꥢ�����������ޤ���Ʊ������Ͽ�κݤ�Ʊ���ޥ���Ǥʤ���к���Ǥ��ޤ���";
$H_ALIASREFERCOM = "�����ꥢ���򻲾ȤǤ��ޤ���";
$H_ALIASCHANGED = "�ѹ����ޤ�����";
$H_ALIASENTRIED = "��Ͽ���ޤ�����";
$H_ALIASDELETED = "�õ�ޤ�����";
$H_AORI_ALIAS = "��Ƥκݡ��֤�̾���פ���ʬ�˰ʲ��Ρ�#....�פ����Ϥ���ȡ���Ͽ����Ƥ��뤪̾����e-mail addr.��URL����ưŪ������ޤ���";
$H_CANNOTQUOTE = "cannot quote specified file";

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
