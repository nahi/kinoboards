# $Id: kb.ph,v 3.0 1996-01-20 14:01:35 nakahiro Exp $
#
# $Log: kb.ph,v $
# Revision 3.0  1996-01-20 14:01:35  nakahiro
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
#
$MAINT = "nakahiro\@kinotrope.co.jp";
### $MAINT = "nakahiro\@ohara.info.waseda.ac.jp";


##
# �ץ�����URLɽ��
#
#	��ʬ�Υǥ��쥯�ȥ���֤����
#		ex.) http://www.foo.bar.jp/~baz/kb.cgi
#	���ѤΥǥ��쥯�ȥ���֤�(�֤��ͤФʤ�ʤ�)���
#		ex.) http://www.foo.bar.jp/cgi-bin/kb.cgi
#
$PROGRAM = "http://www.kinotrope.co.jp/~nakahiro/kb.cgi";
### $PROGRAM = "http://www.ohara.info.waseda.ac.jp/cgi-bin/kb.cgi";


##
# �����ƥब¸�ߤ���ǥ��쥯�ȥ��URLɽ��
#
$SYSTEM_DIR_URL = "http://www.kinotrope.co.jp/~nakahiro";
### $SYSTEM_DIR_URL = "http://www.ohara.info.waseda.ac.jp/person/nakahiro/kb";


##
# �����ƥब¸�ߤ���ǥ��쥯�ȥ�Υѥ�̾
#
$SYSTEM_DIR = "/home/nakahiro/public_html";
### $SYSTEM_DIR = "/home/common/WWW/DocumentRoot/person/nakahiro/kb";


##
# sendmail�Υѥ��ȥ��ץ����
#
$MAIL2 = "/usr/lib/sendmail -oi -t";


##
# ���ɽ��
#
$ADDRESS = "Copyright 1995 <a href=\"http://www.kinotrope.co.jp/\">kinotrope Co.,Ltd.</a> &amp; <a href=\"http://www.kinotrope.co.jp/~nakahiro/\">nakahiro</a> // ��̵��ž��";
### $ADDRESS = "Copyright 1995 <a href=\"http://www.ohara.info.waseda.ac.jp/person/nakahiro/nakahiro.html\">nakahiro</a> // ��̵��ž��";


#/////////////////////////////////////////////////////////////////////


###
## �桼��������������(�ä��ѹ����ʤ��Ǥ�OK)
#

#
# �����ƥ������
#
# ����ʸ�񥿥���(HTML or PRE)�������Ԥ����ݤ�(0: �Ԥ�ʤ�, 1: �Ԥ�)
$SYS_TEXTTYPE = 1;
# �����ꥢ�������Ѥ��뤫�ݤ�(0: �Ԥ�ʤ�, 1: �Ԥ�)
$SYS_ALIAS = 1;
# ���ѻ��˥�����Ĥ����ݤ�(0: �Ĥ��ʤ�, 1: �Ĥ�)
$SYS_TAGINQUOTE = 1;
# ������Ƶ���������������Ƥ����������������Ƥ�����(0: ��, 1: ��)��
$SYS_BOTTOMTITLE = 1;

#
# �طʿ��λ���
#
$BG_COLOR = "#FF.FF.FF";

#
# ��å����������
#
$SYSTEM_NAME = "���Τܡ���";

$ENTRY_MSG = "$SYSTEM_NAME �ؤν񤭹���";
$SHOWICON_MSG = "��������γ�ǧ";
$PREVIEW_MSG = "�񤭹��ߤ����Ƥ��ǧ���Ʋ�����";
$THANKS_MSG = "�񤭹��ߤ��꤬�Ȥ��������ޤ���";
$SORT_MSG = "���ս祽����";
$NEWARTICLE_MSG = "�Ƕ�ε���";
$THREADARTICLE_MSG = "ȿ���ޤȤ��ɤ�";
$SEARCHARTICLE_MSG = "�����θ���";
$ALIASNEW_MSG = "�����ꥢ������Ͽ/�ѹ�/���";
$ALIASMOD_MSG = "�����ꥢ�����ѹ�����ޤ���";
$ALIASDEL_MSG = "�����ꥢ�����������ޤ���";
$ALIASSHOW_MSG = "�����ꥢ���λ���";
$ERROR_MSG   = "$SYSTEM_NAME: ERROR!";

$H_BOARD = "�ܡ���:";
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
$H_AORI = "���̤˽񤭹���ǲ��������֥饦����ü�Ǥμ�ưŪ���ޤ��֤��ϹԤʤ鷺���񤤤��ޤ�ɽ������ޤ���<br>HTML�Τ狼�����ϡ���$H_TEXTTYPE�פ��$H_HTML�פˤ���HTML�Ȥ��ƽ񤤤�ĺ���ȡ�HTML������Ԥʤ��ޤ���";
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

#
# ���ѥޡ���
#
#	��>�פ��&gt;�פ���ѥޡ����ˤ���Τ��򤱤Ʋ�������
#	�ȥ�֥�򵯤����֥饦����¸�ߤ��ޤ���
#
$DEFAULT_QMARK = " ] ";

#
# �����Υץ�ե�����
# �����ե����뤬����(���ꤷ��ʸ����).(�����ֹ�).html�פˤʤ롣
#
$ARTICLE_PREFIX = "kb";

#
# ��������ǥ��쥯�ȥ�
# ��������ȥ�����������ե�����������ǥ��쥯�ȥ�̾
#
$ICON_DIR_NAME = "icons";

#
# ������������ե�����Υݥ��ȥե�����
# ������������ե����뤬����(�ܡ��ɥǥ��쥯�ȥ�̾).(���ꤷ��ʸ����)�פˤʤ롣
#
$ICONDEF_POSTFIX = "idef";

#
# �ǥե���ȤΥ�����������ե�����
#
$DEFAULT_ICONDEF = "all.idef";

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
# �ե�����
#
# ��å��ե�����
$LOCK_FILE_NAME = ".lock.kb";
# �����ֹ�ե�����
$ARTICLE_NUM_FILE_NAME = ".articleid";
# �����ȥ�ե�����
$TITLE_FILE_NAME = "index.html";
# all�ե�����
$ALL_FILE_NAME = "all.html";
# �����ȥ�tmporary�ե�����
$TTMP_FILE_NAME = "index.tmp";
# �桼�������ꥢ���ե�����
$USER_ALIAS_FILE_NAME = "kinousers";
# �ܡ��ɥ����ꥢ���ե�����
$BOARD_ALIAS_FILE_NAME = "kinoboards";


#/////////////////////////////////////////////////////////////////////


###
## ����¾�����(����������ϴ���Ū���ѹ����ʤ�������)
#

#
# URL
#
# �桼�������ꥢ���ե�����
$USER_ALIAS_FILE_URL = "$SYSTEM_DIR_URL/$USER_ALIAS_FILE_NAME";
# ��������ǥ��쥯�ȥ�
$ICON_DIR_URL = "$SYSTEM_DIR_URL/$ICON_DIR_NAME";

#
# �ե�����
#
# ��å��ե�����
$LOCK_FILE = "$SYSTEM_DIR/$LOCK_FILE_NAME";
# �桼�������ꥢ���ե�����
$USER_ALIAS_FILE = "$SYSTEM_DIR/$USER_ALIAS_FILE_NAME";
# �ܡ��ɥ����ꥢ���ե�����
$BOARD_ALIAS_FILE = "$SYSTEM_DIR/$BOARD_ALIAS_FILE_NAME";
# ��������ǥ��쥯�ȥ�
$ICON_DIR = "$SYSTEM_DIR/$ICON_DIR_NAME";

#
# �����ѥ�����ʸ
#
$COM_TITLE_BEGIN = "<!-- Title List Begin -->";
$COM_TITLE_END = "<!-- Title List End -->";
$COM_ARTICLE_BEGIN = "<!-- Article Begin -->";
$COM_ARTICLE_END = "<!-- Article End -->";
$COM_HEADER_BEGIN = "<!-- Header Begin -->";
$COM_FMAIL_BEGIN = "<!-- Follow Mail Begin";
$COM_FMAIL_END = "Follow Mail End -->";

#
# Permission of Title File.
#
$TITLE_FILE_PERMISSION = "0666";

#
# ��å��Υ�����
#
$LOCK_SH = 1;
$LOCK_EX = 2;
$LOCK_NB = 4;
$LOCK_UN = 8;

#
# ���ѥե饰
#
$QUOTE_ON = 1;
$NO_QUOTE = 0;

#
# �����default
#
$[ = 0;


#/////////////////////////////////////////////////////////////////////
1;
