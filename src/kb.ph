# $Id: kb.ph,v 2.2 1996-01-20 08:53:39 nakahiro Exp $
#
# $Log: kb.ph,v $
# Revision 2.2  1996-01-20 08:53:39  nakahiro
# bakup
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
$MAINT = "nakahiro@kinotrope.co.jp";
### $MAINT = "nakahiro@ohara.info.waseda.ac.jp";


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
# ���������ɥ���С���(���Ϥ�UJIS�ء����Ϥ�JIS��)�Υѥ��ȥ��ץ����
#
#	nkf����̾�������뤫��'whichi nkf'���Ǥ�����ǡ�
#	�ФƤ����ѥ���񤤤Ʋ�������
#	
$KC2IN = "/usr/local/bin/nkf -e";
$KC2OUT = "/usr/local/bin/nkf -j";
### $KC2IN = "/usr/local/bin/kc -e";
### $KC2OUT = "/usr/local/bin/kc -j";


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
# ��å����������
#
$SYSTEM_NAME = "���Τܡ���";

$ENTRY_MSG = "$SYSTEM_NAME�ؤν񤭹���";
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
$H_AORI = "���̤˽񤭹���ǲ��������֥饦����ü�Ǥμ�ưŪ���ޤ��֤��ϹԤʤ鷺���񤤤��ޤ�ɽ������ޤ���<br>HTML�Τ狼�����ϡ���$H_TEXTTYPE�פ��$H_HTML�פˤ���HTML�Ȥ��ƽ񤤤�ĺ���ȡ�HTML������Ԥʤ��ޤ���";

# �����ꥢ�����ȤκݤΥإå�
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