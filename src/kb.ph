# $Id: kb.ph,v 1.2 1995-12-15 14:20:24 nakahiro Exp $
#
# $Log: kb.ph,v $
# Revision 1.2  1995-12-15 14:20:24  nakahiro
# String for Header of Search Module.
#
# Revision 1.1  1995/12/15 12:38:44  nakahiro
# Initial revision
#


# kinoBoards: Kinoboards Is Network Opened BOARD System

#/////////////////////////////////////////////////////////////////////


###
## �桼��������������(ư��������ɬ���ѹ�����!)
#

#
# �����Ԥ�e-mail addr.
#
$Maint = "nakahiro@ohara.info.waseda.ac.jp";

#
# �ץ���ब¸�ߤ���ǥ��쥯�ȥ��URLɽ��
#
$PROGRAM_DIR_URL = "/~nakahiro";

#
# ���ɽ��
#
$ADDRESS = "Copyright 1995 <a href=\"http://www.kinotrope.co.jp/\">kinotrope Co.,Ltd.</a> &amp; <a href=\"http://www.kinotrope.co.jp/~nakahiro/\">nakahiro</a> // ��̵��ž��";


#/////////////////////////////////////////////////////////////////////


###
## �桼��������������(�ä��ѹ����ʤ��Ǥ�OK)
#

#
# �����Υץ�ե�����
# �����ե����뤬����(���ꤷ��ʸ����).(�����ֹ�).html�פˤʤ롣
#
$ARTICLE_PREFIX = "kb";

#
# ��å����������
#
$ENTRY_MSG = "���Τܡ����ؤν񤭹���";
$PREVIEW_MSG = "�񤭹��ߤ����Ƥ��ǧ���Ʋ�����";
$THANKS_MSG = "�񤭹��ߤ��꤬�Ȥ��������ޤ���";
$SORT_MSG = "���ս祽����";
$NEWARTICLE_MSG = "�Ƕ�ε���";
$THREADARTICLE_MSG = "ȿ���ޤȤ��ɤ�";
$SEARCHARTICLE_MSG = "�����θ���";
$ERROR_MSG   = "ERROR!";

$H_BOARD = "�ܡ���:";
$H_SUBJECT = "���ꡡ:";
$H_FROM = "��̾��:";
$H_MAIL = "�᡼��:";
$H_HOST = "�ޥ���:";
$H_DATE = "�����:";
$H_REPLY = "������:";
$H_FOLLOW = "��ȿ��";

$H_TEXTTYPE = "���Ϸ���:";
$H_HTML = "HTMLʸ��";
$H_PRE = "�����Ѥ�ʸ��";

$H_AORI = "���̤˽񤭹���ǲ���������ưŪ���ޤ��֤��ϹԤʤ鷺���񤤤��ޤ�ɽ������ޤ�����������&lt; &gt; &amp; &quot; �ϡ����ΤޤޤǤϻȤ��ޤ�������ˤ��줾�졢 &amp;lt; &amp;gt; &amp;amp; &amp;quot; �Ƚ񤯤ȡ�������ɽ������ޤ���<br>HTML�Τ狼�����ϡ���$H_TEXTTYPE�פ��$H_HTML�פˤ���HTML�Ȥ��ƽ񤤤�ĺ���ȡ�HTML������Ԥʤ��ޤ���";

#
# ���ѥޡ���
#
# ����>�פ��&gt;�פ���ѥޡ����ˤ���Τ��򤱤Ʋ�������
#   �ȥ�֥�򵯤����֥饦����¸�ߤ��ޤ���
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


###
## ����¾�����(������������ѹ����ʤ��Ǥ�)
#

#
# ���Υץ�����̾��
#
$PROGRAM_NAME = "kb.cgi";
#
# ���Υץ�����URL
#
$PROGRAM = $PROGRAM_DIR_URL . "/" . $PROGRAM_NAME;

#
# Permission of Title File.
#
$TITLE_FILE_PERMISSION = "0666";

#
# �ե�����
#
# ��å��ե�����
$LOCK_FILE = ".lock.kb";
# �����ֹ�ե�����
$ARTICLE_NUM_FILE_NAME = ".articleid";
# �����ȥ�ե�����
$TITLE_FILE_NAME = "index.html";
# all�ե�����
$ALL_FILE_NAME = "all.html";
# �����ȥ�tmporary�ե�����
$TTMP_FILE_NAME = "index.tmp";
# �桼�������ꥢ���ե�����
$USER_ALIAS_FILE = "kinousers";
# �桼�������ꥢ���ե�����URL
$USER_ALIAS_FILE_URL = $PROGRAM_DIR_URL . "/" . $USER_ALIAS_FILE;
# �ܡ��ɥ����ꥢ���ե�����
$BOARD_ALIAS_FILE = "kinoboards";

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
$NO_QUOTE = 0;
$QUOTE_ON = 1;


#/////////////////////////////////////////////////////////////////////
