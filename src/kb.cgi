#!/usr/local/bin/perl5
#
# $Id: kb.cgi,v 4.0 1996-04-05 12:04:25 nakahiro Exp $
#
# $Log: kb.cgi,v $
# Revision 4.0  1996-04-05 12:04:25  nakahiro
# KINOBOARDS works based on CGI. No html file now.
#
# Revision 3.5  1996/03/28 13:04:23  nakahiro
# FIN like modification.
#
# Revision 3.4  1996/03/28 09:53:32  nakahiro
# Modified articles DB structure. (Add list of articles followed)
#
# Revision 3.3  1996/02/11 06:53:43  nakahiro
# the 1st test version for my homepage.
#
# Revision 3.2  1996/02/08 07:11:04  nakahiro
# Bulletin board for KINOTROPE Inc.
#
# Revision 3.1  1996/01/26 07:33:18  nakahiro
# release version for OOW96.
#
# Revision 3.0  1996/01/20 14:01:13  nakahiro
# oow1
#
# Revision 2.1  1995/12/19 18:46:12  nakahiro
# send mail
#
# Revision 2.0  1995/12/19 14:26:56  nakahiro
# user writable alias file.
#
# Revision 1.11  1995/12/19 05:00:54  nakahiro
# cgi and tag_secure packaging.
#
# Revision 1.10  1995/12/15 14:21:37  nakahiro
# keyword search routine.
#
# Revision 1.9  1995/12/13 17:08:19  nakahiro
# '(single-quote)-char escape routine.
#
# Revision 1.8  1995/12/04 11:44:31  nakahiro
# articles can include ' char.
#
# Revision 1.7  1995/11/24 17:29:00  nakahiro
# title list of picked articles.
#
# Revision 1.6  1995/11/22 13:01:39  nakahiro
# partial sort by date.
#
# Revision 1.5  1995/11/15 11:39:16  nakahiro
# show user-alias information when posting.
#
# Revision 1.4  1995/11/08 09:18:22  nakahiro
# Add reference to Original File when Quoting local file.
#
# Revision 1.3  1995/11/02 05:50:48  nakahiro
# New Feature: quote a local file.
#
# Revision 1.2  1995/11/02 04:59:44  nakahiro
# A bug in SortArticle was fixed.
#
# Revision 1.1  1995/11/01 06:27:56  nakahiro
# many many changes and fixed bugs from ver 1.0.
#
# Revision 1.0  1995/10/22  08:59:03  nakahiro
# beta version.
# released on MAGARI page in kinotrope.
#


# kinoBoards: Kinoboards Is Network Opened BOARD System
# Copyright 1995-96 NAKAMURA Hiroshi. ALL RIGHTS RESERVED.


#/////////////////////////////////////////////////////////////////////


###
## ヘッダファイルの読み込み
#
require('kb.ph');


#/////////////////////////////////////////////////////////////////////


###
## 大域変数の定義
#


#
# 配列のdefault
#
$[ = 0;


#
# default http port
#
$DEFAULT_HTTP_PORT = 80;


#
# ファイル
#
# ロックファイル
$LOCK_FILE = ".lock.kb";
# 記事番号ファイル
$ARTICLE_NUM_FILE_NAME = ".articleid";
# 掲示板別configuratinファイル
$CONF_FILE_NAME = ".kbconf";
# タイトルリストヘッダファイル
$BOARD_FILE_NAME = ".board";
# DBファイル
$DB_FILE_NAME = ".db";
# DBテンポラリファイル
$DB_TMP_FILE_NAME = ".db.tmp";
# ユーザエイリアスファイル
$USER_ALIAS_FILE = "kinousers";
# ボードエイリアスファイル
$BOARD_ALIAS_FILE = "kinoboards";
# デフォルトのアイコン定義ファイル
$DEFAULT_ICONDEF = "all.idef";

#
# prefix of quote file.
#
$QUOTE_PREFIX = ".q";

#
# アイコンディレクトリ
# (アイコンとアイコン定義ファイルを入れるディレクトリ名)
#
$ICON_DIR = "icons";

#
# アイコン定義ファイルのポストフィクス
# アイコン定義ファイル、「(ボードディレクトリ名).(指定した文字列)」になる。
#
$ICONDEF_POSTFIX = "idef";

#
# 環境変数を拾う
#
$SERVER_NAME = $ENV{'SERVER_NAME'};
$SERVER_PORT = $ENV{'SERVER_PORT'};
$SCRIPT_NAME = $ENV{'SCRIPT_NAME'};
$PATH_INFO = $ENV{'PATH_INFO'};
$REMOTE_HOST = $ENV{'REMOTE_HOST'};
($CGIPROG_NAME = $SCRIPT_NAME) =~ s#^(.*/)##;
$CGIDIR_NAME = $1;
$SCRIPT_URL = "http://$SERVER_NAME:$SERVER_PORT$SCRIPT_NAME";
$DIR_URL = "http://$SERVER_NAME:$SERVER_PORT$CGIDIR_NAME";
$PROGRAM = (($SYS_SCRIPTPATH == 'relative') ? $CGIPROG_NAME : $SCRIPT_NAME);

#
# 制御用コメント文
#
$COM_ARTICLE_BEGIN = "<!-- Article Begin -->";
$COM_ARTICLE_END = "<!-- Article End -->";
$COM_FMAIL_BEGIN = "<!-- Follow Mail Begin";
$COM_FMAIL_END = "Follow Mail End -->";

#
# Permission of Title File.
#
$TITLE_FILE_PERMISSION = "0666";

#
# ロックのタイプ
#
$LOCK_SH = 1;
$LOCK_EX = 2;
$LOCK_NB = 4;
$LOCK_UN = 8;

#
# 引用フラグ
#
$QUOTE_ON = 1;
$NO_QUOTE = 0;

#
# 空行マーク
#
$NULL_LINE = "__br__";


###
## インクルードファイルの読み込み
#
require('cgi.pl');
require('tag_secure.pl');


###
## メイン
#

# コマンド分岐:			c=m

# タイトルリスト(thread):	c=v&num={[1-9][0-9]*}
# タイトルリスト(日付):		c=r&num={[1-9][0-9]*}
# 最新の記事:			c=l&num={[1-9][0-9]*}

# 記事の表示(記事のみ):		c=e&id={[1-9][0-9]*}
# 次の記事の表示(記事のみ):	c=en&id={[1-9][0-9]*}
# 記事の表示(反応もまとめて):	c=t&id={[1-9][0-9]*}

# 新規投稿:			c=n
# 引用つきフォロー:		c=q&id={[1-9][0-9]*}
# 引用なしフォロー:		c=f&id={[1-9][0-9]*}
# URL引用フォロー:		c=q/f&url={URL}
# 記事のプレビュー:		c=p&(空)....
# 確認済み画面:			c=x&id={[1-9][0-9]*(引用でない時id=0)}

# 記事の検索:			c=s
# アイコン表示:			c=i

# エイリアス登録画面:		c=an
# エイリアス登録:		c=am&alias=..&name=..&email=..&url=..
# エイリアス削除:		c=ad&alias=...
# エイリアス参照:		c=as

# 記事の削除エントリ:		c=dn
# 記事の削除確認:		c=dp
# 記事の削除:			c=dt

MAIN: {

    # 標準入力(POST)または環境変数(GET)のデコード。
    &cgi'decode;

    # 頻繁に使うので大域変数
    $BOARD = $cgi'TAGS{'b'};

    # 掲示板固有セッティングを読み込む
    require("$BOARD/$CONF_FILE_NAME") if (-s "$BOARD/$CONF_FILE_NAME");

    # システムセッティングの依存関係を整理
    if ($SYS_FIN_LIKE) {
	$SYS_TEXTTYPE = 0;
	$SYS_ALIAS = 0;
	$SYS_TAGINQUOTE = 0;
	$SYS_ICON = 0;
	$SYS_FOLLOWMAIL = 0;
	$SYS_SHOWHOST = 0;
	$SYS_NEWARTICLEONLY = 1;
    }

    # 値の抽出
    local($Command) = $cgi'TAGS{'c'};
    local($Com) = $cgi'TAGS{'com'};
    local($Id) = $cgi'TAGS{'id'};
    local($Num) = $cgi'TAGS{'num'};
    local($Alias) = $cgi'TAGS{'alias'};
    local($Name) = $cgi'TAGS{'name'};
    local($Email) = $cgi'TAGS{'email'};
    local($URL) = $cgi'TAGS{'url'};

    # コマンドタイプによる分岐
    if ($Command eq "v") {
	&ViewTitle($Num);
    } elsif ($Command eq "r") {
	&SortArticle($Num);
    } elsif ($Command eq "l") {
	&NewArticle($Num);

    } elsif ($Command eq "e") {
	&ShowArticle($Id);
    } elsif (($Command eq "m") && ($Com eq $H_NEXTARTICLE)) {
	&ShowArticle($Id + 1);
    } elsif (($Command eq "t")
	     || (($Command eq "m") && ($Com eq $H_READREPLYALL))) {
	&ThreadArticle($Id);

    } elsif (($Command eq "n")
	     || (($Command eq "m") && ($Com eq $H_POSTNEWARTICLE))) {
	&Entry($NO_QUOTE, 0);
    } elsif (($Command eq "f")
	     || (($Command eq "m") && ($Com eq $H_REPLYTHISARTICLE))) {
	$Id ? &Entry($NO_QUOTE, $Id) : &URLEntry($NO_QUOTE, $URL);
    } elsif (($Command eq "q")
	     || (($Command eq "m") && ($Com eq $H_REPLYTHISARTICLEQUOTE))) {
	$Id ? &Entry($QUOTE_ON, $Id) : &URLEntry($QUOTE_ON, $URL);
    } elsif (($Command eq "p") && ($Com ne $H_ENTRY)) {
	&Preview();
    } elsif (($Command eq "x")
	     || (($Command eq "p") && ($Com eq $H_ENTRY))) {
	&Thanks();

    } elsif ($Command eq "s") {
	&SearchArticle();
    } elsif ($Command eq "i") {
	&ShowIcon();

    } elsif ($Command eq "an") {
	&AliasNew();
    } elsif ($Command eq "am") {
	&AliasMod($Alias, $Name, $Email, $URL);
    } elsif ($Command eq "ad") {
	&AliasDel($Alias);
    } elsif ($Command eq "as") {
	&AliasShow();

    } elsif ($Command eq "dn") {
	&DeleteEntry();
    } elsif ($Command eq "dp") {
	&DeletePreview($Id);
    } elsif ($Command eq "dt") {
	&DeleteThanks($Id);

    } else {
	print("illegal command was given.\n");
    }
}


###
## おしまい
#
exit 0;


#/////////////////////////////////////////////////////////////////////
# 書き込み画面関連


###
## 書き込み画面
#
sub Entry {

    # 引用あり/なしと、引用する場合はそのId(引用しない時は0)
    local($QuoteFlag, $Id) = @_;

    # Board名称の取得
    local($BoardName) = &GetBoardInfo($BOARD);

    # 表示画面の作成
    &MsgHeader("$BoardName: $ENTRY_MSG");

    # フォローの場合
    if ($Id != 0) {
	# 記事の表示(コマンド無し)
	&ViewOriginalArticle($Id, 0);
	print("<hr>\n");
	print("<h2>$H_REPLYMSG</h2>");
    }

    # お約束
    print("<form action=\"$PROGRAM\" method=\"POST\">\n");
    print("<input name=\"c\" type=\"hidden\" value=\"p\">\n");
    print("<input name=\"b\" type=\"hidden\" value=\"$BOARD\">\n");
    
    # 引用Id; 引用でないなら0。
    print("<input name=\"id\" type=\"hidden\" value=\"$Id\">\n");

    # あおり文、Board名、アイコン
    &EntryHeader;

    # Subject(フォローなら自動的に文字列を入れる)
    printf("%s <input name=\"subject\" type=\"text\" value=\"%s\" size=\"%s\"><br>\n",
	   $H_SUBJECT,
	   (($Id !=0 ) ? &GetReplySubject($Id, $BOARD) : ''),
	   $SUBJECT_LENGTH);

    # TextType
    if ($SYS_TEXTTYPE) {
	print("$H_TEXTTYPE\n");
	print("<SELECT NAME=\"texttype\">\n");
	print("<OPTION SELECTED>$H_PRE\n");
	print("<OPTION>$H_HTML\n");
	print("</SELECT><BR>\n");
    }

    # 本文(引用ありなら元記事を挿入)
    print("<textarea name=\"article\" rows=\"$TEXT_ROWS\" cols=\"$TEXT_COLS\">");
    &QuoteOriginalArticle($Id, $BOARD)
	if (($Id != 0) && ($QuoteFlag == $QUOTE_ON));
    print("</textarea><br>\n");

    # 名前とメールアドレス、URLを表示。
    &EntryUserInformation();

    # ボタン
    &EntrySubmitButton();

    # お約束
    print("</form>\n");

    &MsgFooter();
}


###
## 書き込み画面(URL)
#
sub URLEntry {

    # 引用あり/なしと、URL
    local($QuoteFlag, $URL) = @_;

    # Board名称の取得
    local($BoardName) = &GetBoardInfo($BOARD);

    # file
    local($File) = &GetPath($BOARD, "$QUOTE_PREFIX.$$");
    local($Server, $HttpPort, $Resource, $Name) = ('', '', '', '');
    local($PlainURL) = '';

    # split
    $Name = (($PlainURL = $URL) =~ s/\#(.*)$//o) ? $1 : '';

    if ($PlainURL =~ m!http://([^:]*):([0-9]*)(/.*)$!io) {
	$Server = $1;
	$HttpPort = $2;
	$Resource = $3;
    } elsif ($PlainURL =~ m!http://([^/]*)(/.*)$!io) {
	$Server = $1;
	$HttpPort = $DEFAULT_HTTP_PORT;
	$Resource = $2;
    } else {
	&MyFatal(10, $PlainURL);
    }
    
    # connect
    &HttpConnect($Server, $HttpPort, $Resource, $File)
	|| &MyFatal(10, $PlainURL);

    # 表示画面の作成
    &MsgHeader("$BoardName: $ENTRY_MSG");

    # 引用ファイルの表示
    &ViewOriginalFile($File, $Name);
    print("<hr>\n");
    print("<h2>$H_REPLYMSG</h2>");
    
    # お約束
    print("<form action=\"$PROGRAM\" method=\"POST\">\n");
    print("<input name=\"c\" type=\"hidden\" value=\"p\">\n");
    print("<input name=\"c\" type=\"hidden\" value=\"$BOARD\">\n");

    # 引用Id; 正規の引用でないので0。
    print("<input name=\"id\" type=\"hidden\" value=\"0\">\n");

    # 引用ファイル
    print("<input name=\"qurl\" type=\"hidden\" value=\"$URL\">\n");
    print("<input name=\"file\" type=\"hidden\" value=\"$File\">\n");

    # あおり文、Board名、アイコン
    &EntryHeader;

    # Subject
    printf("%s <input name=\"subject\" type=\"text\" value=\"%s\" size=\"%s\"><br>\n",
	   $H_SUBJECT, &GetReplySubjectFromFile($File), $SUBJECT_LENGTH);
    
    # TextType
    if ($SYS_TEXTTYPE) {
	print("$H_TEXTTYPE\n");
	print("<SELECT NAME=\"texttype\">\n");
	print("<OPTION SELECTED>$H_PRE\n");
	print("<OPTION>$H_HTML\n");
	print("</SELECT><BR>\n");
    }
    
    # 本文(引用ありなら元記事を挿入)
    print("<textarea name=\"article\" rows=\"$TEXT_ROWS\" cols=\"$TEXT_COLS\">");
    &QuoteOriginalFile($File, $Name) if ($QuoteFlag == $QUOTE_ON);
    print("</textarea><br>\n");

    # 名前とメールアドレス、URLを表示。
    &EntryUserInformation();

    # ボタン
    &EntrySubmitButton();

    # お約束
    print("</form>\n");

    &MsgFooter();
}


###
## 書き込み画面のうち、あおり文、TextType、Board名を表示。
#
sub EntryHeader {

    # Board名称の取得
    local($BoardName) = &GetBoardInfo($BOARD);

    # あおり文
    print("<p>$H_AORI</p>\n");

    # Board名; 本当は自由に選択できるようにしたい。
    print("$H_BOARD $BoardName<br>\n");

    # アイコンの選択
    &EntryIcon if ($SYS_ICON && (! $SYS_FIN_LIKE));

}


###
## 書き込み画面のうち、アイコン選択部分を表示。
#
sub EntryIcon {

    local($FileName, $Title);

    print("$H_ICON\n");
    print("<SELECT NAME=\"icon\">\n");
    print("<OPTION SELECTED>$H_NOICON\n");

    # 一つ一つ表示
    open(ICON, "$ICON_DIR/$BOARD.$ICONDEF_POSTFIX")
	|| (open(ICON, "$ICON_DIR/$DEFAULT_ICONDEF")
	    || &MyFatal(1, "$ICON_DIR/$DEFAULT_ICONDEF"));
    while(<ICON>) {
	chop;
	($FileName, $Title) = split(/\t/, $_);
	print("<OPTION>$Title\n");
    }
    close(ICON);
    print("</SELECT>\n");
    print("(<a href=\"$PROGRAM?b=$BOARD&c=i\">$H_SEEICON</a>)<BR>\n");

}


###
## 書き込み画面のうち、名前、e-mail addr.、URL入力部を表示。
#
sub EntryUserInformation {

    # 名前とメールアドレス、URL。
    print("$H_FROM <input name=\"name\" type=\"text\" size=\"$NAME_LENGTH\"><br>\n");
    print("$H_MAIL <input name=\"mail\" type=\"text\" size=\"$MAIL_LENGTH\"><br>\n");
    print("$H_URL <input name=\"url\" type=\"text\" value=\"http://\" size=\"$URL_LENGTH\"><br>\n");
    print("$H_FMAIL <input name=\"fmail\" type=\"checkbox\" value=\"on\"><br>\n")
	if ($SYS_FOLLOWMAIL);
    
    if ($SYS_ALIAS) {
	print("<p><a href=\"$PROGRAM?c=as\">$H_SEEALIAS</a> // \n");
	print("<a href=\"$PROGRAM?c=an\">$H_ALIASENTRY</a></p>\n");
	print("<p>$H_ALIASINFO</p>\n");
    }
}


###
## 書き込み画面のうち、ボタンを表示。
#
sub EntrySubmitButton {

    print("<p>\n");
    print("<input type=\"submit\" name=\"com\" value=\"$H_PREVIEW\">\n");
    print("<input type=\"submit\" name=\"com\" value=\"$H_ENTRY\">\n");
    print("</p>\n");

}


###
## あるIdの記事からSubjectを取ってきて、先頭に「Re: 」を1つだけつけて返す。
#
sub GetReplySubject {

    # IdとBoard
    local($Id, $Board) = @_;

    # 記事情報
    local($dFid, $dAids, $dDate, $dSubject, $dIcon, $dRemoteHost, $dName,
	  $dEmail, $dUrl, $dFmail) = &GetArticlesInfo($Id);

    # 先頭に「Re: 」がくっついてたら取り除く。
    $dSubject =~ s/^Re: //o;

    # 先頭に「Re: 」をくっつけて返す。
    return("Re: $dSubject");

}


###
## あるファイルからTitleを取ってきて、先頭に「Re: 」をつけて返す。
#
sub GetReplySubjectFromFile {

    # ファイル
    local($File) = @_;

    # 取り出したSubject
    local($Title) = &GetSubjectFromFile($File);

    # 先頭に「Re: 」をくっつけて返す。
    return("Re: $Title");

}


###
## 引用する
#
sub QuoteOriginalArticle {

    # IdとBoard
    local($Id, $Board) = @_;

    # 引用するファイル
    local($QuoteFile) = &GetArticleFileName($Id, $Board);

    # ファイルを開く
    open(TMP, "<$QuoteFile") || &MyFatal(1, $QuoteFile);
    while(<TMP>) {

	# コード変換
	&jcode'convert(*_, 'euc');

	# 引用のための変換
	s/&/&amp;/go;
	s/\"//go;
	if ($SYS_TAGINQUOTE) {
	    s/<//go;
	    s/>//go;
	} else {
	    s/<[^>]*>//go;
	}

	# 引用文字列の表示
	print($DEFAULT_QMARK, $_);
	
    }

    # 閉じる
    close(TMP);

}


###
## 引用する(ファイル)
#
sub QuoteOriginalFile {

    # ファイル名
    local($File, $Name) = @_;

    # name tagが来たか?
    local($NameFlag) = ($Name) ? 0 : 1;

    # 引用部分を判断するフラグ
    local($QuoteFlag) = 0;

    open(TMP, "<$File") || &MyFatal(1, $File);
    while(<TMP>) {

	# コード変換
	&jcode'convert(*_, 'euc');

	# 引用終了の判定
	$QuoteFlag = 0, last
	    if (($QuoteFlag == 1) && (/$COM_ARTICLE_END/));

	# 引用文字列の表示
	if ($QuoteFlag == 1) {
	    s/&/&amp;/go;
	    s/\"//go;
	    if ($SYS_TAGINQUOTE) {
		s/<//go;
		s/>//go;
	    } else {
		s/<[^>]*>//go;
	    }
	    print($DEFAULT_QMARK, $_);
	}

	# name tag?
	$NameFlag = 1 if (/<a\s+name\s*=\s*\"$Name/i);

	# 引用開始の判定
	$QuoteFlag = 1 if (($NameFlag) && (/$COM_ARTICLE_BEGIN/));
	
    }
    close(TMP);

}


#/////////////////////////////////////////////////////////////////////
# アイコン表示画面関連


###
## アイコン表示画面
#
sub ShowIcon {

    local($BoardName) = &GetBoardInfo($BOARD);
    local($FileName, $Title);

    # 表示画面の作成
    &MsgHeader($SHOWICON_MSG);
    print("<p>\"$BoardName\"$H_ICONINTRO</p>\n");
    print("<p><dl>\n");

    # 一つ一つ表示
    open(ICON, "$ICON_DIR/$BOARD.$ICONDEF_POSTFIX")
	|| (open(ICON, "$ICON_DIR/$DEFAULT_ICONDEF")
	    || &MyFatal(1, "$ICON_DIR/$DEFAULT_ICONDEF"));
    while(<ICON>) {
	chop;
	($FileName, $Title) = split(/\t/, $_);
	print("<dt><img src=\"$ICON_DIR/$FileName\" alt=\"$Title\"> : $Title\n");
    }
    close(ICON);

    print("</dl></p>\n");

    &MsgFooter();

}


#/////////////////////////////////////////////////////////////////////
# プレビュー画面関連


###
## プレビュー画面
#
sub Preview {

    # Board名称の取得
    local($BoardName) = &GetBoardInfo($BOARD);

    # 入力された記事情報
    local($Id, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article,
	  $File, $Qurl, $Fmail)
	= ($cgi'TAGS{'id'}, $cgi'TAGS{'texttype'}, $cgi'TAGS{'name'},
	   $cgi'TAGS{'mail'}, $cgi'TAGS{'url'}, $cgi'TAGS{'icon'},
	   $cgi'TAGS{'subject'}, $cgi'TAGS{'article'}, $cgi'TAGS{'file'},
	   $cgi'TAGS{'qurl'}, $cgi'TAGS{'fmail'});

    # 引用記事のURL
    local($rFile) = '';

    # 引用記事の記事情報
    local($rFid, $rAids, $rDate, $rSubject, $rIcon, $rRemoteHost, $rName,
	  $rEmail, $rUrl, $rFmail) = ('', '', '', '', '', '', '', '', '', '');

    # もし引用なら……。
    if ($File) {

	# local fileからの引用なら……
        $rFile = $File;
        $rSubject = &GetSubjectFromFile($File);

    } elsif ($Id) {

	# 通常記事の引用なら……
	$rFile = "$PROGRAM?b=$BOARD&c=e&id=$Id";

	# 引用記事の記事情報を取得
	($rFid, $rAids, $rDate, $rSubject, $rIcon, $rRemoteHost, $rName,
	 $rEmail, $rUrl, $rFmail) = &GetArticlesInfo($Id);

    }

    # 入力された記事情報のチェック
    ($Name, $Email, $Url)
	= &CheckArticle($Name, $Email, $Url, $Subject, $Article);

    # 確認画面の作成
    &MsgHeader($PREVIEW_MSG);

    # お約束
    print("<form action=\"$PROGRAM\" method=\"POST\">\n");
    print("<input name=\"c\"        type=\"hidden\" value=\"x\">\n");
    print("<input name=\"b\"        type=\"hidden\" value=\"$BOARD\">\n");
    print("<input name=\"id\"       type=\"hidden\" value=\"$Id\">\n");
    print("<input name=\"texttype\" type=\"hidden\" value=\"$TextType\">\n");
    print("<input name=\"name\"     type=\"hidden\" value=\"$Name\">\n");
    print("<input name=\"mail\"     type=\"hidden\" value=\"$Email\">\n");
    print("<input name=\"url\"      type=\"hidden\" value=\"$Url\">\n");
    print("<input name=\"icon\"     type=\"hidden\" value=\"$Icon\">\n");
    print("<input name=\"subject\"  type=\"hidden\" value=\"$Subject\">\n");
    print("<input name=\"article\"  type=\"hidden\" value=\"$Article\">\n");
    print("<input name=\"file\"     type=\"hidden\" value=\"$File\">\n");
    print("<input name=\"qurl\"     type=\"hidden\" value=\"$Qurl\">\n");
    print("<input name=\"fmail\"    type=\"hidden\" value=\"$Fmail\">\n");

    # あおり文
    print("<p>$H_POSTINFO");
    print("<input type=\"submit\" value=\"$H_PUSHHERE\"></p>\n");

    # 題
    (($Icon eq $H_NOICON) || (! $Icon))
        ? print("<strong>$H_SUBJECT</strong> $Subject<br>\n")
            : printf("<strong>$H_SUBJECT</strong> <img src=\"%s\" alt=\"$Icon\"> $Subject<br>\n", &GetIconURL($Icon));

    # お名前
    if ($Url eq "http://" || $Url eq '') {
        # URLがない場合
        print("<strong>$H_FROM</strong> $Name<br>\n");
    } else {
        # URLがある場合
        print("<strong>$H_FROM</strong> <a href=\"$Url\">$Name</a><br>\n");
    }

    # メール
    print("<strong>$H_MAIL</strong> <a href=\"mailto:$Email\">&lt;$Email&gt;</a><br>\n");

    # 反応元(引用の場合)
    &ShowFormattedLinkToFollowedArticle($Id, $rIcon, $rSubject);

    # 切れ目
    print("$H_LINE<br>\n");

    # TextType用前処理
    print("<pre>\n") if ((! $SYS_TEXTTYPE) || ($TextType eq $H_PRE));

    # 記事
    $Article = &tag_secure'decode($Article);
    print("$Article\n");

    # TextType用後処理
    print("</pre>\n") if ((! $SYS_TEXTTYPE) || ($TextType eq $H_PRE));
    
    # お約束
    print("</form>\n");

    &MsgFooter();
}


###
## 入力された記事情報のチェック
#
sub CheckArticle {

    # 記事情報いろいろ
    local($Name, $Email, $Url, $Subject, $Article) = @_;
    local($Tmp) = '';

    # エイリアスチェック
    $_ = $Name;
    if (/^#.*$/) {
        ($Tmp, $Email, $Url) = &GetUserInfo($_);
	&MyFatal(7, $Name) if ($Tmp eq '');
	$Name = $Tmp;
    }

    # 空チェック
    &MyFatal(2, '') if ($Subject eq '') || ($Article eq '') || ($Name eq '')
	|| ($Email eq '');

    # 文字列チェック
    &CheckName($Name);
    &CheckEmail($Email);
    &CheckURL($Url);

    # サブジェクトのタグチェック
    $_ = $Subject;
    &MyFatal(4, '') if (/</);

    # 名前、e-mail、URLを返す。
    return($Name, $Email, $Url);
}


#/////////////////////////////////////////////////////////////////////
# 登録後画面関連


###
## 登録後画面
#
sub Thanks {

    # 新たに記事を生成する
    &MakeNewArticle();

    # 表示画面の作成
    &MsgHeader($THANKS_MSG);

    print("<p>$H_THANKSMSG</p>");
    print("<form action=\"$PROGRAM\" method=\"POST\">\n");
    print("<input name=\"b\" type=\"hidden\" value=\"$BOARD\">\n");
    if ($SYS_FIN_LIKE) {
	print("<input name=\"c\" type=\"hidden\" value=\"v\">\n");
	print("<input name=\"num\" type=\"hidden\" value=\"0\">\n");
    } else {
	print("<input name=\"c\" type=\"hidden\" value=\"l\">\n");
	print("<input name=\"num\" type=\"hidden\" value=\"1\">\n");
    }
    print("<input type=\"submit\" value=\"$H_BACK\">\n");
    print("</form>\n");

    &MsgFooter();
}


###
## 新たに投稿された記事の生成
#
sub MakeNewArticle {

    # Board名称の取得
    local($BoardName) = &GetBoardInfo($BOARD);

    # 日付を取り出す。
    local($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst)
	= localtime(time);
    local($InputDate)
	= ($SYS_FIN_LIKE)
	    ? sprintf("%02d/%02d/%02d(%02d:%02d)", $year, $mon + 1, $mday,
		      $hour, $min)
		: sprintf("%d/%d(%02d:%02d)", $mon + 1, $mday, $hour, $min);

    # 入力された記事情報
    local($Id, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article,
	  $File, $Qurl, $Fmail)
	= ($cgi'TAGS{'id'}, $cgi'TAGS{'texttype'}, $cgi'TAGS{'name'},
	   $cgi'TAGS{'mail'}, $cgi'TAGS{'url'}, $cgi'TAGS{'icon'},
	   $cgi'TAGS{'subject'}, $cgi'TAGS{'article'}, $cgi'TAGS{'file'},
	   $cgi'TAGS{'qurl'}, $cgi'TAGS{'fmail'});

    # 入力された記事情報のチェック
    ($Name, $Email, $Url)
	= &CheckArticle($Name, $Email, $Url, $Subject, $Article);

    # ロックをかける
    &lock();

    # 新しい記事番号を取得(まだ記事番号は増えてない)
    local($ArticleId) = &GetNewArticleId();

    # 正規のファイルの作成
    &MakeArticleFile($TextType, $Article, $ArticleId);

    # DBファイルに投稿された記事を追加
    if ($File) {

	# URL引用ならURL
	&AddDBFile($ArticleId, $Qurl, $InputDate, $Subject, $Icon,
		   $REMOTE_HOST, $Name, $Email, $Url, $Fmail);

    } else {

	# 通常の記事引用ならID
	&AddDBFile($ArticleId, $Id, $InputDate, $Subject, $Icon,
		   $REMOTE_HOST, $Name, $Email, $Url, $Fmail);

    }

    # 新しい記事番号を書き込む
    &AddArticleId();

    # ロックを外す。
    &unlock();

}


###
## 記事を書き出す。
#
sub MakeArticleFile {

    # TextTypeと記事そのもの、Id
    local($TextType, $Article, $Id) = @_;

    # ファイル名を取得
    local($File) = &GetArticleFileName($Id, $BOARD);

    # ファイルを開く
    open(TMP, ">$File") || &MyFatal(1, $File);

    # TextType用前処理
    print(TMP "<pre>\n") if ((! $SYS_TEXTTYPE) || ($TextType eq $H_PRE));

    # 記事
    $Article = &tag_secure'decode($Article);
    print(TMP "$Article\n");

    # TextType用後処理
    print(TMP "</pre>\n") if ((! $SYS_TEXTTYPE) || ($TextType eq $H_PRE));
    
    # 終了
    close(TMP);

}


###
## 記事番号を増やす。
#
sub AddArticleId {

    # 記事番号を収めるファイル
    local($ArticleNumFile) = &GetPath($BOARD, $ARTICLE_NUM_FILE_NAME);

    # 新しい記事番号
    local($ArticleId) = &GetNewArticleId();

    # 書き込む。
    open(AID, ">$ArticleNumFile") || &MyFatal(1, $ArticleNumFile);
    print(AID $ArticleId, "\n");
    close(AID);

}


###
## 新しい記事番号を返す
#
sub GetNewArticleId {

    # 記事番号を収めるファイル
    local($ArticleNumFile) = &GetPath($BOARD, $ARTICLE_NUM_FILE_NAME);

    # 記事番号
    local($ArticleId) = 0;

    # 記事番号をファイルから読み込む。読めなかったら0のまま……のはず。
    open(AID, "$ArticleNumFile");
    while(<AID>) {
	chop;
	$ArticleId = $_;
    }
    close(AID);

    # 1増やして返す
    return($ArticleId + 1);

}


###
## DBファイルに書き込む
#
sub AddDBFile {

    # 記事Id、名前、アイコン、題、日付
    local($Id, $Fid, $InputDate, $Subject, $Icon,
	  $RemoteHost, $Name, $Email, $Url, $Fmail) = @_;
    local($dId, $dFid, $dAids, $dInputDate, $dSubject, $dIcon,
	  $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail)
		   = ('', '', '', '', '', '', '', '', '', '', ());
    
    # 登録ファイル
    local($File) = &GetPath($BOARD, $DB_FILE_NAME);
    local($TmpFile) = &GetPath($BOARD, $DB_TMP_FILE_NAME);

    # Open Tmp File
    open(DBTMP, ">$TmpFile") || &MyFatal(1, $TmpFile);
    # Open DB File
    open(DB, "<$File") || &MyFatal(1, $File);

    while(<DB>) {
	chop;
	($dId, $dFid, $dAids, $dInputDate, $dSubject, $dIcon,
	 $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail) = split(/\t/, $_);
	
	# フォロー先記事が見つかったら、
	if ($dId == $Fid) {

	    # その記事のフォロー記事IDリストに加える(カンマ区切り)
	    if ($dAids) {$dAids .= ",$Id";} else {$dAids = $Id;}

	    # 必要なら反応があったことをメールする
	    &FollowMail($dEmail, $dName, $dInputDate, $dSubject, $dId, $Name,
			$Subject, $Id) if (($SYS_FOLLOWMAIL) && ($dFmail));

	}

	# DBに書き加える
	printf(DBTMP "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n",
	       $dId, $dFid, $dAids, $dInputDate, $dSubject, $dIcon,
	       $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail);
    }

    # 新しい記事のデータを書き加える。
    printf(DBTMP "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n",
	   $Id, $Fid, '', $InputDate, $Subject, $Icon,
	   $RemoteHost, $Name, $Email, $Url, $Fmail);

    # close Files.
    close(DB);
    close(DBTMP);

    # DBを更新する
    rename($TmpFile, $File);

}


#/////////////////////////////////////////////////////////////////////
# 日付順ソート関連


###
## 日付順にソート。
#
sub SortArticle {

    # 表示する個数を取得
    local($Num) = @_;

    # 記事番号を収めるファイル
    local($ArticleNumFile) = &GetPath($BOARD, $ARTICLE_NUM_FILE_NAME);

    # DBファイル
    local($DBFile) = &GetPath($BOARD, $DB_FILE_NAME);

    # 最新記事番号を取得
    local($ArticleToId) = &GetArticleId($ArticleNumFile);

    # 記事数が足りない場合の調整
    $Num = $ArticleToId if ($ArticleToId < $Num);

    # Board名称の取得
    local($BoardName) = &GetBoardInfo($BOARD);

    # 取ってくる最初の記事番号を取得
    local($ArticleFromId) = $ArticleToId - $Num + 1;
    local($ListFlag) = 0;
    local(@Lines) = ();
    local($Id, $Fid, $Aids, $Date, $Title, $Icon, $RemoteHost, $Name, $Email,
	  $Url, $Fmail) = (0, '', '', '', '', '', '', '', '', '', '');

    # lockをかける
    &lock();

    # 取り込み。DBファイルがなければ何も表示しない。
    open(DB, "<$DBFile") || &MyFatal(1, $DBFile);

    while(<DB>) {
	chop;

	next if (/^\#/);

	($Id, $Fid, $Aids, $Date, $Title, $Icon, $RemoteHost, $Name, $Email,
	 $Url, $Fmail) = split(/\t/, $_);
	$ListFlag = 1 if ($ArticleFromId <= $Id);

	# 新規記事のみ表示、の場合はキャンセル。
	$ListFlag = 0
	    if (($SYS_FIN_LIKE || $SYS_NEWARTICLEONLY) && ($Fid != 0));

	push(Lines, &GetFormattedTitle($Id, $Icon, $Title, $Name, $Date))
	    if ($ListFlag);

    }
    close(DB);

    # lockをはずす
    &unlock();

    # 表示画面の作成
    &MsgHeader("$BoardName: $SORT_MSG");

    &BoardHeader;

    print("<hr>\n");
    print("<ul>\n");

    # 記事の表示
    if ($SYS_BOTTOMTITLE) {
	# 新しい記事が下
	foreach (@Lines) {print("$_\n");}
    } else {
	# 新しい記事が上
	foreach (reverse @Lines) {print("$_\n");}
    }

    print("</ul>\n");
    &MsgFooter();

}


#/////////////////////////////////////////////////////////////////////
# thread別タイトル表示関連


###
## 新しい記事のタイトルをthread別にn個を表示。
#
sub ViewTitle {

    # 表示する個数を取得
    local($Num) = @_;

    # DBファイル
    local($DBFile) = &GetPath($BOARD, $DB_FILE_NAME);

    # 記事番号を収めるファイル
    local($ArticleNumFile) = &GetPath($BOARD, $ARTICLE_NUM_FILE_NAME);

    # Board名称の取得
    local($BoardName) = &GetBoardInfo($BOARD);

    # 最新記事番号を取得
    local($ArticleToId) = &GetArticleId($ArticleNumFile);
    local($ArticleFromId) = 0;

    local($ListFlag) = 0;
    local(@Lines) = ();
    local($Line) = '';
    local($Id, $Fid, $Aids, $Date, $Title, $Icon, $RemoteHost, $Name, $Email,
	  $Url, $Fmail) = (0, '', '', '', '', '', '', '', '', '', '');

    # 数字が0なら最初から全て
    if ($Num == 0) {
	$ArticleFromId = 1;
    } else {
	# 記事数が足りない場合の調整
	$Num = $ArticleToId if ($ArticleToId < $Num);

	# 取ってくる最初の記事番号を取得
	$ArticleFromId = $ArticleToId - $Num + 1;
    }

    # lockをかける
    &lock();

    # 取り込み。DBファイルがなければ何も表示しない。
    open(DB, "<$DBFile") || &MyFatal(1, $DBFile);
    while(<DB>) {
	chop;

	next if (/^\#/);

	($Id, $Fid, $Aids, $Date, $Title, $Icon, $RemoteHost, $Name, $Email,
	 $Url, $Fmail) = split(/\t/, $_);
	$ListFlag = 1 if ($ArticleFromId <= $Id);

	# 新規記事のみ表示、の場合はキャンセル。
	$ListFlag = 0
	    if (($SYS_FIN_LIKE || $SYS_NEWARTICLEONLY) && ($Fid != 0));

	if ($ListFlag) {

	    # 追加する行
	    $Line = &GetFormattedTitle($Id, $Icon, $Title, $Name, $Date);

	    # 追加
	    @Lines = ($Fid)
		? &AddTitleFollow($Fid, $Line, @Lines)
		    : &AddTitleNormal($Line, @Lines);
	}
    }
    close(DB);

    # lockをはずす。
    &unlock();

    # 表示画面の作成
    &MsgHeader("$BoardName: $VIEW_MSG");

    &BoardHeader;

    print("<hr>\n");
    if ($SYS_FIN_LIKE) {
	print("<pre>\n");
#	print("+-----------------+----+----------------------+--------------------------------+\n");
	print("| 投稿日          |返答| 投稿者               | タイトル                       |\n");
#	print("+-----------------+----+----------------------+--------------------------------+\n");
    } else {
	print("<ul>\n");
    }

    # 記事の表示
    foreach (@Lines) {
	print("$_\n") unless ((s/$NULL_LINE//o) && ($SYS_FIN_LIKE));
    }

    if ($SYS_FIN_LIKE) {
#	print("+-----------------+----+----------------------+--------------------------------+\n");
	print("</pre>\n");
    } else {
	print("</ul>\n");
    }

    &MsgFooter();

}


###
## タイトルリストに書き込む(新規)
#
sub AddTitleNormal {

    # 格納行、格納先
    local($Line, @Lines) = @_;

    # フラグに応じて……
    if ($SYS_BOTTOMTITLE) {

	# 末尾に追加
	push(Lines, $Line, $NULL_LINE);
    } else {

	# 先頭に追加
	unshift(Lines, $Line, $NULL_LINE);
    }

    # 返す
    return(@Lines);

}


###
## タイトルリストに書き込む(フォロー)
#
sub AddTitleFollow {

    # フォロー記事ID、格納行、格納先
    local($Fid, $AddLine, @Lines) = @_;
    local(@NewLines) = ();

    # Follow Flag
    local($AddFlag, $Nest, $NextLine) = (0, 0, ''); 

    # タイトルリストのフラグ
    local($TitleListFlag) = 0;

    while($_ = shift(Lines)) {

	# そのまま書き出す。
	push(NewLines, $_);

	# タイトルリスト中、お目当ての記事が来たら、
	if (/id=$Fid/) {

	    # 1行空読み
	    $_ = shift(Lines);

	    if (/^<ul>/) {
		$Nest = 1;
		do {
		    push(NewLines, $_);
		    $_ = shift(Lines);
		    $Nest++ if (/^<ul>/);
		    $Nest-- if (/^<\/ul>/);
		} until ($Nest == 0);
		
		push(NewLines, $AddLine, $NULL_LINE);
		push(NewLines, $_);
		
	    } else {

		push(NewLines, "<ul>");
		push(NewLines, $AddLine, $NULL_LINE);
		push(NewLines, "</ul>");

	    }

	    $AddFlag = 1;
	}
    }

    # 元記事が見当たらないなら……
    if (! $AddFlag) {

	# フラグに応じて……
	if ($SYS_BOTTOMTITLE) {
	    
	    # 末尾に追加
	    push(NewLines, $AddLine, $NULL_LINE);
	} else {

	    # 先頭に追加
	    unshift(NewLines, $AddLine, $NULL_LINE);
	}
    }

    return(@NewLines);

}


#/////////////////////////////////////////////////////////////////////
# 新着記事表示関連


###
## 新しい記事からn個を表示。
#
sub NewArticle {

    # 表示する個数を取得
    local($Num) = @_;

    # 記事番号を収めるファイル
    local($ArticleNumFile) = &GetPath($BOARD, $ARTICLE_NUM_FILE_NAME);

    # Board名称の取得
    local($BoardName) = &GetBoardInfo($BOARD);

    # 最新記事番号を取得
    local($ArticleToId) = &GetArticleId($ArticleNumFile);
    local($ArticleFromId) = 0;
    local($i, $File);

    # 数字が0なら最初から全て
    if ($Num == 0) {
	$ArticleFromId = 1;
    } else {
	# 記事数が足りない場合の調整
	$Num = $ArticleToId if ($ArticleToId < $Num);

	# 取ってくる最初の記事番号を取得
	$ArticleFromId = $ArticleToId - $Num + 1;
    }

    # 表示画面の作成
    &MsgHeader("$BoardName: $NEWARTICLE_MSG");

    &BoardHeader;

    print("<hr>\n");

    if ($SYS_BOTTOMTITLE) {

	# 下へ
	for ($i = $ArticleFromId; ($i <= $ArticleToId); $i++) {
	    # 記事の表示(コマンド付き)
	    &ViewOriginalArticle($i, 1);
	    print("<hr>\n");
	}
	
    } else {

	# 上へ
	for ($i = $ArticleToId; ($i >= $ArticleFromId); $i--) {
	    # 記事の表示(コマンド付き)
	    &ViewOriginalArticle($i, 1);
	    print("<hr>\n");
	}

    }

    &MsgFooter();
}


###
## 記事番号を取ってくる(番号は増えない)。
#
sub GetArticleId {

    # ファイル名を取得
    local($ArticleNumFile) = @_;

    # 記事番号
    local($ArticleId);

    # lockをかける
    &lock();

    # なかったら0を返す(いいのか?)
    open(AID, "$ArticleNumFile") || return(0);
    while(<AID>) {
	chop;
	$ArticleId = $_;
    }
    close(AID);

    # lockをはずす
    &unlock();

    # 記事番号を返す。
    return($ArticleId);
}


#/////////////////////////////////////////////////////////////////////
# 記事表示関連


###
## 単一の記事を表示。
#
sub ShowArticle {

    # 記事のIdを取得
    local($Id) = @_;

    # 記事のファイル名を取得
    local($File) = &GetArticleFileName($Id, $BOARD);

    # Board名称の取得
    local($BoardName) = &GetBoardInfo($BOARD);

    # 引用記事の情報
    local($rFid, $rAids, $rDate, $rSubject, $rIcon, $rRemoteHost, $rName,
	  $rEmail, $rUrl, $rFmail) = ('', '', '', '', '', '', '', '', '', '');

    # 反応記事の情報
    local($aFid, $aAids, $aDate, $aSubject, $aIcon, $aRemoteHost, $aName,
	  $aEmail, $aUrl, $aFmail) = ('', '', '', '', '', '', '', '', '', '');

    # 記事情報の取得
    local($Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $Email,
	  $Url, $Fmail) = &GetArticlesInfo($Id);
    local(@AidList) = split(/,/, $Aids);
    local($Aid) = '';

    # 未投稿記事は読めない
    &MyFatal(11, '') unless ($Name);

    # 引用記事情報の抽出
    ($rFid, $rAids, $rDate, $rSubject, $rIcon, $rRemoteHost, $rName, $rEmail,
     $rUrl, $rFmail) = &GetArticlesInfo($Fid) if ($Fid != 0);

    # 表示画面の作成
    &MsgHeader("[$BoardName: $Id] $Subject");

    # お約束
    print("<form action=\"$PROGRAM\" method=\"POST\">\n");
    print("<input name=\"c\" type=\"hidden\" value=\"m\">\n");
    print("<input name=\"b\" type=\"hidden\" value=\"$BOARD\">\n");
    print("<input name=\"id\" type=\"hidden\" value=\"$Id\">\n");

    # コマンド部分の表示
    print("<input type=\"submit\" name=\"com\" value=\"$H_NEXTARTICLE\">\n");
    print("<input type=\"submit\" name=\"com\" value=\"$H_POSTNEWARTICLE\">\n");
    print("<input type=\"submit\" name=\"com\" value=\"$H_REPLYTHISARTICLE\">\n");
    print("<input type=\"submit\" name=\"com\" value=\"$H_REPLYTHISARTICLEQUOTE\">\n");
    print("<input type=\"submit\" name=\"com\" value=\"$H_READREPLYALL\">") unless ($SYS_FIN_LIKE);
    print("</form>\n");

#    print("<hr>\n");

    # ボード名と記事番号、題
    if (($Icon eq $H_NOICON) || (! $Icon)) {
	print("<strong>$H_SUBJECT</strong> [$BoardName: $Id] $Subject<br>\n");
    } else {
	printf("<strong>$H_SUBJECT</strong> [$BoardName: $Id] <img src=\"%s\" alt=\"$Icon\">$Subject<br>\n", &GetIconURL($Icon));
    }

    # お名前
    if (! $Url) {
        # URLがない場合
        print("<strong>$H_FROM</strong> $Name<br>\n");
    } else {
        # URLがある場合
        print("<strong>$H_FROM</strong> <a href=\"$Url\">$Name</a><br>\n");
    }

    # メール
    print("<strong>$H_MAIL</strong> <a href=\"mailto:$Email\">&lt;$Email&gt;</a><br>\n");

    # マシン
    print("<strong>$H_HOST</strong> $RemoteHost<br>\n") if $SYS_SHOWHOST;

    # 投稿日
    print("<strong>$H_DATE</strong> $Date<br>\n");

    # 反応元(引用の場合)
    &ShowFormattedLinkToFollowedArticle($Fid, $rIcon, $rSubject);

    # 切れ目
    print("$H_LINE<br>\n");

    # 記事
    open(TMP, "<$File") || &MyFatal(1, $File);
    while(<TMP>) {print($_);}
    close(TMP);

    # article end
    print("<hr>\n");

    # 反応記事
    print("$H_FOLLOW<br>\n");

    if ($Aids) {

	# 反応記事があるなら…
	print("<ul>\n");

	foreach $Aid (@AidList) {

	    # 反応記事情報の抽出
	    ($aFid, $aAids, $aDate, $aSubject, $aIcon, $aRemoteHost, $aName,
	     $aEmail, $aUrl, $aFmail) = &GetArticlesInfo($Aid);

	    # 表示
	    printf("%s\n", &GetFormattedTitle($Aid, $aIcon, $aSubject, $aName, $aDate));
	}

	print("</ul>\n");

    } else {

	# 反応記事無し
	print("$H_NOTHING\n");

    }

    # お約束
    &MsgFooter();

}


###
## フォロー記事を全て表示。
#
sub ThreadArticle {

    # 元記事のIdを取得
    local($Id) = @_;

    # Board名称の取得
    local($BoardName) = &GetBoardInfo($BOARD);

    # 表示画面の作成
    &MsgHeader("$BoardName: $THREADARTICLE_MSG");

    # メイン関数の呼び出し(記事概要)
    unless ($SYS_FIN_LIKE) {
	print("<ul>\n");
	&ThreadArticleMain('subject only', $Id);
	print("</ul>\n");
	print("<hr>\n");
    }

    # メイン関数の呼び出し(記事)
    &ThreadArticleMain('', $Id);

    &MsgFooter();
}


###
## 再帰的にその記事のフォローを表示する。
#
sub ThreadArticleMain {

    # Idの取得
    local($SubjectOnly, $Id) = @_;

    # フォロー記事のIdの取得
    local(@FollowIdList) = &GetFollowIdList($Id);

    # 記事概要か、記事そのものか。
    if ($SubjectOnly) {

	# 記事概要の表示
	&PrintAbstract($Id);

    } else {

	# 元記事の表示(コマンド付き)
	&ViewOriginalArticle($Id, 1);

    }

    # フォロー記事の表示
    foreach (@FollowIdList) {

	# 区切り
	print("<hr>\n");

	# 記事概要なら箇条書
	print("<ul>\n") if ($SubjectOnly);
	
	# 再帰
	&ThreadArticleMain($SubjectOnly, $_, $BOARD);

	# 記事概要なら箇条書閉じ
	print("</ul>\n") if ($SubjectOnly);

    }
}


###
## フォロー記事のIdの配列を取り出す。
#
sub GetFollowIdList {

    # Id
    local($Id) = @_;

    # DBファイル
    local($DBFile) = &GetPath($BOARD, $DB_FILE_NAME);

    # リスト
    local(@Result) = ();

    # 記事情報
    local($dId, $dFid, $dAids, $dDate, $dTitle, $dIcon, $dRemoteHost, $dName,
	  $dEmail, $dUrl, $dFmail)
	= (0, '', '', '', '', '', '', '', '', '', '');

    # lockをかける
    &lock();

    # 取り込み
    open(DB, "<$DBFile") || &MyFatal(1, $DBFile);
    while(<DB>) {
	chop;

	next if (/^\#/);

	($dId, $dFid, $dAids, $dDate, $dTitle, $dIcon, $dRemoteHost, $dName,
	 $dEmail, $dUrl, $dFmail) = split(/\t/, $_);

	# 見つかった!
	@Result = split(/,/, $dAids) if ($Id == $dId);

    }
    close(DB);

    # lockをはずす
    &unlock();

    # 返す
    return(@Result);
}


###
## 記事の概要の表示
#
sub PrintAbstract {

    # Id
    local($Id) = @_;

    # 記事情報を取り出す。
    local($dFid, $dAids, $dDate, $dSubject, $dIcon, $dRemoteHost, $dName,
	  $dEmail, $dUrl, $dFmail) = &GetArticlesInfo($Id);

    printf("%s\n",
	   &GetFormattedAbstract($Id, $dIcon, $dSubject, $dName, $dDate));

}


#/////////////////////////////////////////////////////////////////////
# 記事検索関連


###
## 記事の検索(表示画面作成)
#
sub SearchArticle {

    # キーワード、検索範囲を拾う
    local($Key, $SearchSubject, $SearchPerson, $SearchArticle)
	= ($cgi'TAGS{'key'}, $cgi'TAGS{'searchsubject'},
	   $cgi'TAGS{'searchperson'}, $cgi'TAGS{'searcharticle'});

    # Board名称の取得
    local($BoardName) = &GetBoardInfo($BOARD);

    # 表示画面の作成
    &MsgHeader("$BoardName: $SEARCHARTICLE_MSG");

    # お約束
    print("<form action=\"$PROGRAM\" method=\"POST\">\n");
    print("<input name=\"c\" type=\"hidden\" value=\"s\">\n");
    print("<input name=\"b\" type=\"hidden\" value=\"$BOARD\">\n");

    # ボタン
    print("<p>$H_INPUTKEYWORD</p>\n");
    print("<input type=\"submit\" value=\"$H_SEARCHKEYWORD\">\n");
    print("<input type=\"reset\" value=\"$H_RESETKEYWORD\">\n");

    # キーワード入力部
    print("<p>$H_KEYWORD:\n");
    print("<input name=\"key\" size=\"$KEYWORD_LENGTH\" value=\"$Key\">");
    print("</p>\n");

    # 検索範囲設定部
    print("<p>$H_SEARCHTARGET:\n");
    if ($SearchSubject) {
	print("<input name=\"searchsubject\" type=\"checkbox\" value=\"on\" CHECKED> $H_SEARCHTARGETSUBJECT / \n");
    } else {
	print("<input name=\"searchsubject\" type=\"checkbox\" value=\"on\"> $H_SEARCHTARGETSUBJECT / \n");
    }

    if ($SearchPerson) {
	print("<input name=\"searchperson\" type=\"checkbox\" value=\"on\" CHECKED> $H_SEARCHTARGETPERSON / \n");
    } else {
	print("<input name=\"searchperson\" type=\"checkbox\" value=\"on\"> $H_SEARCHTARGETPERSON / \n");
    }

    if ($SearchArticle) {
	print("<input name=\"searcharticle\" type=\"checkbox\" value=\"on\" CHECKED> $H_SEARCHTARGETARTICLE");
    } else {
	print("<input name=\"searcharticle\" type=\"checkbox\" value=\"on\"> $H_SEARCHTARGETARTICLE");
    }

    print("</p>\n");

    print("<hr>\n");

    # キーワードが空でなければ、そのキーワードを含む記事のリストを表示
    &SearchArticleList($Key, $SearchSubject, $SearchPerson, $SearchArticle)
	if (($Key) && ($SearchSubject || ($SearchPerson || $SearchArticle)));

    &MsgFooter();
}


###
## 記事の検索(検索結果の表示)
#
sub SearchArticleList {

    # キーワード、検索範囲
    local($Key, $Subject, $Person, $Article) = @_;

    # DBファイル
    local($DBFile) = &GetPath($BOARD, $DB_FILE_NAME);

    local($Id, $Fid, $Aids, $Date, $Title, $Icon, $RemoteHost, $Name, $Email,
	  $Url, $Fmail) = (0, '', '', '', '', '', '', '', '', '', '');
    local($ArticleFile, $ArticleFilePath, $HitFlag) = ('', '', 0);
    local($Line, $Flag) = ('', 0);

    # リスト開く
    print("<ul>\n");

    # lockをかける
    &lock();

    # ファイルを開く。DBファイルがなければnot found.
    open(DB, "<$DBFile") || &MyFatal(1, $DBFile);
    while(<DB>) {

	next if (/^\#/);

	# 変数のリセット
	$Flag = 0;
	$Line = '';

	($Id, $Fid, $Aids, $Date, $Title, $Icon, $RemoteHost, $Name, $Email,
	 $Url, $Fmail) = split(/\t/, $_);
	$ArticleFile = &GetArticleFileName($Id, '');
	$ArticleFilePath = &GetArticleFileName($Id, $BOARD);

	# タイトルを検索
	$Flag = 1 if ($Subject && ($Title =~ /$Key/));

	# 投稿者名を検索
	$Flag = 1 if ($Person && (($Name =~ /$Key/)));

	# 本文を検索
	$Flag = 1 if ($Article && ($Line = &SearchArticleKeyword($ArticleFilePath, $Key)));

	if ($Flag) {

	    # 最低1つは合致した
	    $HitFlag = 1;

	    # 記事へのリンクを表示
	    print(&GetFormattedTitle($Id, $Icon, $Title, $Name, $Date));

	    # 本文に合致した場合は本文も表示
	    if ($Article && ($Line ne '')) {
		$Line =~ s/<[^>]*>//go;
		$Line =~ s/&/&amp;/go;
		$Line =~ s/\"/&quot;/go;
		print("<blockquote>$Line</blockquote>\n");
	    }
	}
    }
    close(DB);

    # lockをはずす
    &unlock();

    # ヒットしなかったら
    print("<dt>$H_NOTFOUND\n") unless ($HitFlag = 1);

    # リスト閉じる
    print("</dl>\n");
}


###
## 記事の検索(本文)
#
sub SearchArticleKeyword {

    # ファイル名とキーワード
    local($File, $Key) = @_;

    # 検索する
    # SearchArticleListでlockしてるのでlockする必要なし
    open(ARTICLE, "<$File") || &MyFatal(1, $File);
    while(<ARTICLE>) {

	# コード変換
	&jcode'convert(*_, 'euc');

	# TAGを取り除く
	s/<[^>]*>//go;

	# ヒット?
	(/$Key/) && return($_);
    }

    # ヒットせず
    return('');
}


###
## 文字列の検索(タイトルと投稿者名)
#
sub SearchStringKeyword {

    # 文字列とキーワード
    local($String, $Key) = @_;

    # 検索する
    $_ = $String;

    # コード変換
    &jcode'convert(*_, 'euc');

    # TAGを取り除く
    s/<[^>]*>//go;

    # ヒット?
    (/$Key/) && return($_);

    # ヒットせず
    return('');
}


#/////////////////////////////////////////////////////////////////////
# エイリアス関連


###
## エイリアスの登録と変更
#
sub AliasNew {

    # 表示画面の作成
    &MsgHeader($ALIASNEW_MSG);

    # 新規登録/登録内容の変更
    print("<p>$H_ALIASTITLE</p>\n");
    print("<p>\n");
    print("<form action=\"$PROGRAM\" method=\"POST\">\n");
    print("<input name=\"c\" type=\"hidden\" value=\"am\">\n");
    print("$H_ALIAS <input name=\"alias\" type=\"text\" value=\"#\" size=\"$NAME_LENGTH\"><br>\n");
    print("$H_FROM <input name=\"name\" type=\"text\" size=\"$NAME_LENGTH\"><br>\n");
    print("$H_MAIL <input name=\"email\" type=\"text\" size=\"$MAIL_LENGTH\"><br>\n");
    print("$H_URL <input name=\"url\" type=\"text\" value=\"http://\" size=\"$URL_LENGTH\"><br>\n");
    print("$H_ALIASNEWCOM<br>\n");
    print("<input type=\"submit\" value=\"$H_ALIASNEWPUSH\">\n");
    print("</form></p>\n");
    
    print("<hr>\n");
    
    # 削除
    print("<p>$H_ALIASDELETE</p>\n");
    print("<p>\n");
    print("<form action=\"$PROGRAM\" method=\"POST\">\n");
    print("<input name=\"c\" type=\"hidden\" value=\"ad\">\n");
    print("$H_ALIAS <input name=\"alias\" type=\"text\" size=\"$NAME_LENGTH\"><br>\n");
    print("$H_ALIASDELETECOM<br>\n");
    print("<input type=\"submit\" value=\"$H_ALIASDELETEPUSH\">\n");
    print("</form></p>\n");
    
    print("<hr>\n");
    
    # 参照
    print("<p>\n");
    print("<form action=\"$PROGRAM\" method=\"POST\">\n");
    print("<input name=\"c\" type=\"hidden\" value=\"as\">\n");
    print("<input type=\"submit\" value=\"$H_ALIASREFERPUSH\">\n");
    print("</form></p>\n");
    
    # お約束
    &MsgFooter();

}


###
## 登録/変更
#
sub AliasMod {

    # エイリアス、名前、メール、URL
    local($A, $N, $E, $U) = @_;
    
    # ホストがマッチしたか
    #	0 ... エイリアスがマッチしない
    #	1 ... エイリアスはマッチしたがホスト名がマッチしない
    #	2 ... マッチしてデータを変更した
    local($HitFlag) = 0;
    
    # 文字列チェック
    &AliasCheck($A, $N, $E, $U);
    
    # エイリアスの読み込み
    &CashAliasData($USER_ALIAS_FILE);
    
    # 1行ずつチェック
    foreach $Alias (sort keys(%Name)) {
	next unless ($A eq $Alias);
	
	# ホスト名が合ったら2、合わなきゃ1。
	$HitFlag = (($REMOTE_HOST eq $Host{$Alias}) ? 2 : 1);
    }
    
    # ホスト名が合わない!
    &MyFatal(6, '') if ($HitFlag == 1);
    
    # データの登録
    $Name{$Alias} = $N;
    $Email{$Alias} = $E;
    $Host{$Alias} = $REMOTE_HOST;
    $URL{$Alias} = $U;
    
    # エイリアスファイルに書き出し
    &WriteAliasData($USER_ALIAS_FILE);
    
    # 表示画面の作成
    &MsgHeader($ALIASMOD_MSG);
    print("<p>$H_ALIAS <strong>$A</strong>:\n");
    if ($HitFlag == 2) {
	print("$H_ALIASCHANGED</p>\n");
    } else {
	print("$H_ALIASENTRIED</p>\n");
    }
    &MsgFooter();
    
}


###
## エイリアスチェック
#
sub AliasCheck {

    local($A, $N, $E, $U) = @_;

    # 空チェック
    &MyFatal(2, '') if ($A eq '') || ($N eq '') || ($E eq '');

    &CheckAlias($A);
    &CheckName($N);
    &CheckEmail($E);
    &CheckURL($U);
    
}


###
## 削除
#
sub AliasDel {

    # エイリアス
    local($A) = @_;

    # ホストがマッチしたか
    #	0 ... エイリアスがマッチしない
    #	1 ... エイリアスはマッチしたがホスト名がマッチしない
    #	2 ... マッチしてデータを変更した
    local($HitFlag) = 0;
    
    # エイリアスの読み込み
    &CashAliasData($USER_ALIAS_FILE);
    
    # 1行ずつチェック
    foreach $Alias (sort keys(%Name)) {
	next unless ($A eq $Alias);
	
	# ホスト名が合ったら2、合わなきゃ1。
	$HitFlag = (($REMOTE_HOST eq $Host{$Alias}) ? 2 : 1);
    }
    
    # ホスト名が合わない!
    &MyFatal(6, '') if ($HitFlag == 1);
    
    # エイリアスがない!
    &MyFatal(7, $A) if ($HitFlag == 0);
    
    # 名前を消す
    $Name{$A} = '';
    
    # エイリアスファイルに書き出し
    &WriteAliasData($USER_ALIAS_FILE);
    
    # 表示画面の作成
    &MsgHeader($ALIASDEL_MSG);
    print("<p>$H_ALIAS <strong>$A</strong>: $H_ALIASDELETED</p>\n");
    &MsgFooter();

}


###
## 参照
#
sub AliasShow {

    # エイリアスの読み込み
    &CashAliasData($USER_ALIAS_FILE);
    local($Alias);
    
    # 表示画面の作成
    &MsgHeader($ALIASSHOW_MSG);
    # あおり文
    print("<p>$H_AORI_ALIAS</p>\n");
    print("<p><a href=\"$PROGRAM?c=an\">$H_ALIASTITLE</a></p>\n");
    
    # リスト開く
    print("<dl>\n");
    
    # 1つずつ表示
    foreach $Alias (sort keys(%Name)) {
	print("<p>\n");
	print("<dt><strong>$Alias</strong>\n");
	print("<dd>$H_FROM $Name{$Alias}\n");
	print("<dd>$H_MAIL $Email{$Alias}\n");
	print("<dd>$H_HOST $Host{$Alias}\n");
	print("<dd>$H_URL $URL{$Alias}\n");
	print("</p>\n");
    }

    # リスト閉じる
    print("</dl>\n");
    
    &MsgFooter();

}


###
## エイリアスファイルを読み込んで連想配列に放り込む。
## CAUTION: %Name, %Email, %Host, %URLを壊します。
#
sub CashAliasData {

    # ファイル
    local($File) = @_;
    
    local($A, $N, $E, $H, $U) = ('', '', '', '', '');

    # lockをかける
    &lock();

    # 放り込む。
    open(ALIAS, "<$File") || &MyFatal(1, $File);
    while(<ALIAS>) {
	
	# コード変換
	&jcode'convert(*_, 'euc');

	chop;
	($A, $N, $E, $H, $U) = split(/\t/, $_);
	$Name{$A} = $N;
	$Email{$A} = $E;
	$Host{$A} = $H;
	$URL{$A} = $U;
    }
    close(ALIAS);

    # lockをはずす
    &unlock();

}


###
## エイリアスファイルにデータを書き出す。
## CAUTION: %Name, %Email, %Host, %URLを必要とします。
##          $Nameが体と書き込まない。
#
sub WriteAliasData {

    # ファイル
    local($File) = @_;
    local($Alias);

    # ロックをかける
    &lock();

    # 書き出す
    open(ALIAS, ">$File") || &MyFatal(1, $File);
    foreach $Alias (sort keys(%Name)) {
	($Name{$Alias}) && printf(ALIAS "%s\t%s\t%s\t%s\t%s\n",
				  $Alias, $Name{$Alias}, $Email{$Alias},
				  $Host{$Alias}, $URL{$Alias});
    }
    close(ALIAS);
    
    # ロックを外す。
    &unlock();

}


###
## ユーザエイリアスからユーザの名前、メール、URLを取ってくる。
#
sub GetUserInfo {

    # 検索するエイリアス名
    local($Alias) = @_;

    # エイリアス、名前、メール、ホスト、URL
    local($A, $N, $E, $H, $U);

    # lockをかける
    &lock();

    # ファイルを開く
    open(ALIAS, "<$USER_ALIAS_FILE")
	# ファイルがないらしいのでさようなら。
	|| return('', '', '');
    
    # 1つ1つチェック。
    while(<ALIAS>) {
	
	# コード変換
	&jcode'convert(*_, 'euc');

	chop;
	
	# 分割
	($A, $N, $E, $H, $U) = split(/\t/, $_);
	
	# マッチしなきゃ次へ。
	next unless ($A eq $Alias);
	
	# 配列にして返す
	return($N, $E, $U);
    }
    close(ALIAS);

    # lockをはずす
    &unlock();
    
    # ヒットせず
    return('', '', '');
}


###
## ボードエイリアスからボードエイリアス名を取ってくる。
#
sub GetBoardInfo {

    # エイリアス名
    local($Alias) = @_;

    # ボード名
    local($BoardName);

    open(ALIAS, "<$BOARD_ALIAS_FILE")
	|| &MyFatal(1, $BOARD_ALIAS_FILE);
    while(<ALIAS>) {
	
	# コード変換
	&jcode'convert(*_, 'euc');

	chop;
	# マッチしなきゃ次へ。
	next unless (/^$Alias\t(.*)$/);
	$BoardName = $1;
	return($BoardName);
    }
    close(ALIAS);

    # ヒットせず
    return('');
}


#/////////////////////////////////////////////////////////////////////
# 記事の削除関連


###
## 削除記事のIDの指定
#
sub DeleteEntry {

    # 表示画面の作成
    &MsgHeader($DELETE_ENTRY_MSG);

    print("<p>$H_DELETE_ENTRY_TITLE</p>\n");
    print("<p>\n");
    print("<form action=\"$PROGRAM\" method=\"POST\">\n");
    print("<input name=\"c\" type=\"hidden\" value=\"dp\">\n");
    print("$H_ID <input name=\"id\" type=\"text\" value=\"\" size=\"$ID_LENGTH\"><br>\n");
    print("<input type=\"submit\" value=\"$H_PUSHHERE\">\n");
    print("$H_DELETE_COM\n");
    print("</form></p>\n");

    # お約束
    &MsgFooter();

}


###
## 削除記事のIDの指定
#
sub DeletePreview {

    # ID
    local($Id) = @_;

    # 表示画面の作成
    &MsgHeader($DELETE_PREVIEW_MSG);

    # 削除ファイルの表示
    &ViewOriginalArticle($Id, 0);
    print("<hr>\n");
    print("<h2>$H_DELETE_PREVIEW_COM</h2>");

    # お約束
    print("<form action=\"$PROGRAM\" method=\"POST\">\n");
    print("<input name=\"c\" type=\"hidden\" value=\"dt\">\n");
    print("<input name=\"b\" type=\"hidden\" value=\"$BOARD\">\n");
    print("<input name=\"id\" type=\"hidden\" value=\"$Id\">\n");
    print("<input type=\"submit\" value=\"$H_PUSHHERE\">\n");
    print("</form></p>\n");

    # お約束
    &MsgFooter();

}


###
## 削除記事のIDの指定
#
sub DeleteThanks {

    # ID
    local($Id) = @_;

    # ファイル名を取得
    local($ArticleFile) = &GetArticleFileName($ArticleId, $BOARD);

    # 認証チェック

    # 認証が成功すれば削除
    unlink("$ArticleFile");

## !!! はよつくりたい。 !!!

    # 表示画面の作成
    &MsgHeader($DELETE_THANKS_MSG);

    # お約束
    &MsgFooter();

}


#/////////////////////////////////////////////////////////////////////
# その他共通関数


###
## タイトルリストのフォーマット
#
sub GetFormattedTitle {
    local($Id, $Icon, $Title, $Name, $Date) = @_;
    local($String, $Fnum) = ('', 0);

    if ($SYS_FIN_LIKE) {
	$Fnum = &GetFollowArticleNumber($Id);
	$String = sprintf("<a href=\"$PROGRAM?b=$BOARD&c=t&id=$Id\">| $Date | %02d | %s | %s |</a>",
			  $Fnum, &ConvStrToN($Name, 20),
			  &ConvStrToN($Title, 30));
    } else {
	if (($Icon eq $H_NOICON) || (! $Icon)) {
	    $String = sprintf("<li><strong>$Id .</strong> <a href=\"$PROGRAM?b=$BOARD&c=e&id=$Id\">$Title</a> [$Name] $Date");
	} else {
	    $String = sprintf("<li><strong>$Id .</strong> <img src=\"%s\" alt=\"$Icon\"><a href=\"$PROGRAM?b=$BOARD&c=e&id=$Id\">$Title</a> [$Name] $Date", &GetIconURL($Icon));
	}
    }

    return($String);

}


###
## 文字列をn文字にする。短ければ' 'でpadding、長ければ切って'...'を追加。
#
sub ConvStrToN {

    local($String, $N) = @_;
    local($RetStr) = '';

    # 文字列
    local($Length) = length($String);
    local($Width) = $N - 2;

    # 長短によって分岐
    if ($N < 5) {
	# 5文字以下にすることはかなわず。そのまま返す。
	$RetStr = $String;
    } elsif ($Length < $N) {
	# 指定より短い。
	$RetStr = sprintf("%-${N}s", $String);
    } elsif ($Lenght == $N) {
	# ちょうど同じ長さ。
	$RetStr = $String;
    } else {
	# 指定より長い。
	$RetStr = pack("a${Width}", $String) . "..";
    }

    # 返す
    return($RetStr);

}


###
## 文字列を丸めてn文字にし、最後に.../..を追加する。
#
sub RoundStrToN {

    local($String, $N) = @_;
    local($Ptr) = 0;

    while($Ptr < $N - 2) {
	substr($String, 0, $[ + 1);
    }
    

}


###
## タイトルリストのフォーマット(簡略版)
#
sub GetFormattedAbstract {

    local($Id, $Icon, $Title, $Name, $Date) = @_;
    local($String) = '';

    if (($Icon eq $H_NOICON) || (! $Icon)) {
	$String = sprintf("<li><strong>$Id .</strong> $Title [$Name] $Date", &GetIconURL($Icon));
    } else {
	$String = sprintf("<li><strong>$Id .</strong> <img src=\"%s\" alt=\"$Icon\">$Title [$Name] $Date", &GetIconURL($Icon));
    }

    return($String);
}


###
## 反応記事の数を取得
#
sub GetFollowArticleNumber {

    # Idを取得
    local($TargetId) = @_;

    # DBファイル
    local($DBFile) = &GetPath($BOARD, $DB_FILE_NAME);

    # 記事の参照関係を保持する配列
    local(@FollowList) = ();

    local($Id, $Fid, $Aids, $Date, $Title, $Icon, $RemoteHost, $Name, $Email,
	  $Url, $Fmail) = (0, '', '', '', '', '', '', '', '', '', '');

    open(DB_GFAN, "<$DBFile") || &MyFatal(1, $DBFile);
    while(<DB_GFAN>) {

	# コメントはとばす
	next if (/^\#/);

	# 1行scanする。
	($Id, $Fid, $Aids, $Date, $Title, $Icon, $RemoteHost, $Name, $Email,
	 $Url, $Fmail) = split(/\t/, $_);

	# 配列に放り込む
	$FollowList[$Id] = $Aids;

    }
    close(DB_GFAN);

    # 計算して返す
    return(&CalcFollowArticleNumber($TargetId, @FollowList));

}


###
## 反応記事の数を再帰的に計算
#
sub CalcFollowArticleNumber {

    # Idと、反応記事を整理した配列
    local($Id, @FollowList) = @_;

    # 数
    local($Result) = 0;

    # 反応記事をsplit
    local(@List) = split(/,/, $FollowList[$Id]);

    # 個々足し合わせる
    foreach (@List) {
	$Result += &CalcFollowArticleNumber($_, @FollowList);
    }

    # 返す
    return($Result + @List);
}


###
## 元記事情報の表示
#
sub ShowFormattedLinkToFollowedArticle {

    local($Src, $Icon, $Subject) = @_;

    # Board名称の取得
    local($BoardName) = &GetBoardInfo($BOARD);

    # 参照先の取得
    local($Link) = ($Src =~ /^http:/) ? $Src : "$PROGRAM?b=$BOARD&c=e&id=$Src";


    if ($Src != 0) {
	if ($SYS_FIN_LIKE) {
	    print("<strong>$H_REPLY</strong> [$BoardName: $Src] $Subject<br>\n");
	} else {
	    if (($Icon eq $H_NOICON) || (! $Icon)) {
		print("<strong>$H_REPLY</strong> [$BoardName: $Src] <a href=\"$Link\">$Subject</a><br>\n");
	    } else {
		printf("<strong>$H_REPLY</strong> [$BoardName: $Src] <img src=\"%s\" alt=\"$Icon\"><a href=\"$Link\">$Subject</a><br>\n", &GetIconURL($Icon));
	    }
	}
    } elsif ($Qurl ne '') {
	print("<strong>$H_REPLY</strong> <a href=\"Link\">$Subject</a><br>\n");
    }
}


###
## 掲示板のヘッダを表示する
#
sub BoardHeader {

    local($File) = &GetPath($BOARD, $BOARD_FILE_NAME);

    open(HEADER, "<$File") || &MyFatal(1, $File);
    while(<HEADER>){
        print("$_");
    }
    close(HEADER);

}


###
## 文字列チェック: エイリアス
#
sub CheckAlias {

    local($String) = @_;
    ($String =~ (/^#/)) || &MyFatal(8, 'alias');
    (length($String) > 1) || &MyFatal(8, 'alias');

}


###
## 文字列チェック: 名前
#
sub CheckName {

    local($String) = @_;

}


###
## 文字列チェック: メール
#
sub CheckEmail {

    local($String) = @_;
    ($String =~ (/@/)) || &MyFatal(8, 'E-Mail');

}


###
## 文字列チェック: URL
#
sub CheckURL {

    local($String) = @_;
    ($String =~ (/^http:\/\/.*/)) || ($String =~ (/^http:\/\/$/))
	|| ($String eq '') || &MyFatal(8, 'URL');

}


###
## 記事のヘッダの表示
#
sub MsgHeader {

    # message and board
    local($Message) = @_;
    
    &cgi'header;
    print("<html>\n");
    print("<head>\n");
    print("<title>$Message</title>\n");
    print("<base href=\"$DIR_URL\">\n");
    print("</head>\n");
    print("<body bgcolor=\"$BG_COLOR\" TEXT=\"$TEXT_COLOR\" LINK=\"$LINK_COLOR\" ALINK=\"$ALINK_COLOR\" VLINK=\"$VLINK_COLOR\">\n");
    print("<h1>$Message</h1>\n");
    print("<hr>\n");

}


###
## 記事のフッタの表示
#
sub MsgFooter {

    print("<hr>\n");
    print("<address>\n");
    print("$ADDRESS\n");
    print("</address>\n");
    print("</body>\n");
    print("</html>\n");

}


###
## ロック関係
#

# ロック
sub lock {

    # ロックファイルを開く
    open(LOCK, "$LOCK_FILE") || &MyFatal(1, $LOCK_FILE);

    # ロックをかける
    flock(LOCK, $LOCK_EX);
}

# アンロック
sub unlock {

    # ロック外す
    flock(LOCK, $LOCK_UN);

    # ロックファイルを閉じる
    close(LOCK);
}


###
## 元記事の表示
#
sub ViewOriginalArticle {

    # Id、コマンドを表示するか否か
    local($Id, $Flag) = @_;

    # Board名称の取得
    local($BoardName) = &GetBoardInfo($BOARD);

    # 引用するファイル
    local($QuoteFile) = &GetArticleFileName($Id, $BOARD);

    # 引用記事の情報
    local($rFid, $rAids, $rDate, $rSubject, $rIcon, $rRemoteHost, $rName,
	  $rEmail, $rUrl, $rFmail) = ('', '', '', '', '', '', '', '', '', '');

    # 記事情報の取得
    local($Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $Email,
	  $Url, $Fmail) = &GetArticlesInfo($Id);

    # 引用記事情報の抽出
    ($rFid, $rAids, $rDate, $rSubject, $rIcon, $rRemoteHost, $rName, $rEmail,
     $rUrl, $rFmail) = &GetArticlesInfo($Fid) if ($Fid != 0);

    # コマンド表示?
    if ($Flag) {

	# お約束
	print("<form action=\"$PROGRAM\" method=\"POST\">\n");
	print("<input name=\"c\" type=\"hidden\" value=\"m\">\n");
	print("<input name=\"b\" type=\"hidden\" value=\"$BOARD\">\n");
	print("<input name=\"id\" type=\"hidden\" value=\"$Id\">\n");

	# コマンド部分の表示
	print("<input type=\"submit\" name=\"com\" value=\"$H_POSTNEWARTICLE\">\n");
	print("<input type=\"submit\" name=\"com\" value=\"$H_REPLYTHISARTICLE\">\n");
	print("<input type=\"submit\" name=\"com\" value=\"$H_REPLYTHISARTICLEQUOTE\">\n");
	print("<input type=\"submit\" name=\"com\" value=\"$H_READREPLYALL\">\n") unless ($SYS_FIN_LIKE);
	print("</form>\n");

    }

    # ボード名と記事番号、題
    if (($Icon eq $H_NOICON) || (! $Icon)) {
	print("<strong>$H_SUBJECT</strong> [$BoardName: $Id] $Subject<br>\n");
    } else {
	printf("<strong>$H_SUBJECT</strong> [$BoardName: $Id] <img src=\"%s\" alt=\"$Icon\">$Subject<br>\n", &GetIconURL($Icon));
    }

    # お名前
    if (! $Url) {
        # URLがない場合
        print("<strong>$H_FROM</strong> $Name<br>\n");
    } else {
        # URLがある場合
        print("<strong>$H_FROM</strong> <a href=\"$Url\">$Name</a><br>\n");
    }

    # メール
    print("<strong>$H_MAIL</strong> <a href=\"mailto:$Email\">&lt;$Email&gt;</a><br>\n");

    # マシン
    print("<strong>$H_HOST</strong> $RemoteHost<br>\n") if $SYS_SHOWHOST;

    # 投稿日
    print("<strong>$H_DATE</strong> $Date<br>\n");

    # 反応元(引用の場合)
    &ShowFormattedLinkToFollowedArticle($Fid, $rIcon, $rSubject);

    # 切れ目
    print("$H_LINE<br>\n");

    # 記事の中身
    open(TMP, "<$QuoteFile") || &MyFatal(1, $QuoteFile);
    while(<TMP>) {

	# コード変換
	&jcode'convert(*_, 'euc');

	# 表示
	print("$_");

    }
    close(TMP);

}


###
## 元記事の表示(ファイル)
#
sub ViewOriginalFile {

    # ファイル名、name tag
    local($File, $Name) = @_;

    # name tagが来たか?
    local($NameFlag) = ($Name) ? 0 : 1;

    # 引用部分を判断するフラグ
    # 0 ... before
    # 1 ... quote
    # 2 ... after
    local($QuoteFlag) = 0;

    open(TMP, "<$File") || &MyFatal(1, $File);
    while(<TMP>) {

	# コード変換
	&jcode'convert(*_, 'euc');

	# 引用終了の判定
	$QuoteFlag = 2, last
	    if (($QuoteFlag == 1) && (/$COM_ARTICLE_END/));

	# 引用文字列の表示
	print($_) if ($QuoteFlag == 1);

	# name tag?
	$NameFlag = 1 if (/<a\s+name\s*=\s*\"$Name/i);

	# 引用開始の判定
	$QuoteFlag = 1 if (($NameFlag) && (/$COM_ARTICLE_BEGIN/));

    }
    close(TMP);

    # cannot quote specified file.
    print($H_CANNOTQUOTE) if ($QuoteFlag == 0);
}


###
## 反応があったことをメールする。
#
sub FollowMail {

    # 宛先いろいろ
    local($To, $Name, $Date, $Subject, $Id, $Fname, $Fsubject, $Fid) = @_;

    local($BoardName) = &GetBoardInfo($BOARD);
    local($URL) = "$DIR_URL$PROGRAM?b=$BOARD&c=e&id=$Id";
    local($FURL) = "$DIR_URL$PROGRAM?b=$BOARD&c=e&id=$Fid";
    
    # Subject
    local($MailSubject) = "The article was followed.";

    # Message
    local($Message) = "$SYSTEM_NAMEからのお知らせです。\n\n$Dateに「$BoardName」に対して「$Name」さんが書いた、\n「$Subject」\n$URL\nに対して、\n「$Fname」さんから\n「$Fsubject」という題での反応がありました。\n\nお時間のある時に\n$FURL\nを御覧下さい。\n\nでは失礼します。";

    # メール送信
    &SendMail($MailSubject, $Message, $To);
}


###
## ボード名称とIdからファイルのパス名を作り出す。
#
sub GetArticleFileName {

    # IdとBoard
    local($Id, $Board) = @_;

    # Boardが空ならBoardディレクトリ内から相対、
    # 空でなければシステムから相対
    return(($Board) ? "$Board/$Id" : "$Id");

}


###
## ボード名称とファイル名から、そのファイルのパス名を作り出す。
#
sub GetPath {

    # BoardとFile
    local($Board, $File) = @_;

    # 返す
    return("$Board/$File");

}


###
## アイコン名から、アイコンのURLを取得
#
sub GetIconURL {

    # アイコン名
    local($Icon) = @_;

    local($FileName, $Title);
    local($TargetFile) = '';

    # 一つ一つ表示
    open(ICON, "$ICON_DIR/$BOARD.$ICONDEF_POSTFIX")
	|| (open(ICON, "$ICON_DIR/$DEFAULT_ICONDEF")
	    || &MyFatal(1, "$ICON_DIR/$DEFAULT_ICONDEF"));
    while(<ICON>) {
	chop;
	($FileName, $Title) = split(/\t/, $_);
	$TargetFile = $FileName if ($Title eq $Icon);
    }
    close(ICON);

    return("$ICON_DIR/$TargetFile");
}


###
## ある記事の情報を取り出す。
#
sub GetArticlesInfo {

    # 対象記事のID
    local($Id) = @_;

    # DBファイル
    local($DBFile) = &GetPath($BOARD, $DB_FILE_NAME);

    local($dId, $dFid, $dAids, $dDate, $dTitle, $dIcon, $dRemoteHost, $dName,
	  $dEmail, $dUrl, $dFmail)
			 = (0, '', '', '', '', '', '', '', '', '', '');

    # lockをかける
    &lock();

    # 取り込み。DBファイルがなければ0/''を返す。
    open(DB, "<$DBFile");
    while(<DB>) {
	chop;

	next if (/^\#/);

	($dId, $dFid, $dAids, $dDate, $dTitle, $dIcon, $dRemoteHost, $dName,
	 $dEmail, $dUrl, $dFmail) = split(/\t/, $_);

	# 見つかったら返す。
	return($dFid, $dAids, $dDate, $dTitle, $dIcon, $dRemoteHost, $dName,
	       $dEmail, $dUrl, $dFmail) if ($Id == $dId);
    }
    close(DB);

    # lockをはずす
    &unlock();

    # 見つからなかったら0/''を返す。
    return('', '', '', '', '', '', '', '', '', '');
}


###
## あるファイルからTitleを取ってくる
#
sub GetSubjectFromFile {

    # ファイル
    local($File) = @_;

    # 取り出したSubject
    local($Title) = '';

    open(TMP, "<$File") || &MyFatal(1, $File);
    while(<TMP>) {
	
	# コード変換
	&jcode'convert(*_, 'euc');

	if (/<title>(.*)<\/title>/i) {
	    $Title = $1;
	}
    }
    close(TMP);
    
    # 返す。
    return($Title);

}


###
## メール送信
#
sub SendMail {

    # subject、メールのファイル名、宛先
    local($Subject, $Message, $To) = @_;

    # メール用ファイルを開く
    open(MAIL, "| $MAIL2") || &MyFatal(9, '');

    # Toヘッダ
    $_ = $To;
    &jcode'convert(*_, 'jis');
    print(MAIL "To: $_\n");
    
    # Fromヘッダ、Errors-Toヘッダ
    $_ = $MAINT;
    &jcode'convert(*_, 'jis');
    print(MAIL "From: $_\n");
    print(MAIL "Errors-To: $_\n");

    # Subjectヘッダ
    $_ = $Subject;
    &jcode'convert(*_, 'jis');
    print(MAIL "Subject: $_\n\n");

    # 本文
    $_ = $Message;
    &jcode'convert(*_, 'jis');
    print(MAIL "$_\n");

    # 送信する
    close(MAIL);

}


###
## http connectionを張ってリソースを取ってきて、ローカルのファイルに落す。
#
sub HttpConnect {

    local($Server, $HttpPort, $RemoteFile, $LocalFile) = @_;
    local($Sockaddr) = "S n a4 x8";
    local($Name, $Aliases, $Proto) = getprotobyname('tcp');
    local($Name, $Aliases, $Type, $Len, $Hostaddr) = gethostbyname($Server);
    local($Sock) = pack($Sockaddr, 2, $HttpPort, $Hostaddr);

    socket(S, 2, 1, $Proto) || die $!;
    connect(S, $Sock) || return(0);
    select(S); $| = 1; select(STDOUT);
    print(S "GET $RemoteFile HTTP/1.0\n\n");

    open(LOCAL, ">$LocalFile") || MyFatal(1, "$LocalFile");
    while (<S>) {

	# コード変換
	&jcode'convert(*_, 'euc');

	# 書き込む
	print(LOCAL $_);
    }
    
    close(LOCAL);
    return(1);
}


###
## エラー表示
#
sub MyFatal {

    # エラー番号とエラー情報の取得
    local($MyFatalNo, $MyFatalInfo) = @_;
    #
    # 1 ... File関連
    # 2 ... 投稿の際の、必須項目の欠如
    # 3 ... タイトルリストファイルのフォーマットがおかしい
    # 4 ... タイトルにhtmlタグが入っている
    # 5 ... プログラムの制御がおかしい
    # 6 ... エイリアスかホストが一致せず、エイリアスの変更ができない
    # 7 ... エイリアスが登録されていない。
    # 8 ... エイリアスに登録する文字列が正しくない。
    # 9 ... メールが送れなかった
    # 10 ... cannot connect to specified URL.
    
    &MsgHeader($ERROR_MSG);
    
    if ($MyFatalNo == 1) {
	print("<p>File: $MyFatalInfoが存在しない、\n");
	print("あるいはpermissionの設定が間違っています。\n");
	print("お手数ですが、<a href=\"mailto:$MAINT\">$MAINT</a>まで\n");
	print("上記ファイル名をお知らせ下さい。</p>\n");
    } elsif ($MyFatalNo == 2) {
	print("<p>入力されていない項目があります。\n");
	print("戻ってもう一度。</p>\n");
    } elsif ($MyFatalNo == 3) {
	print("<p>Title File is illegal.\n");
	print("お手数ですが、<a href=\"mailto:$MAINT\">$MAINT</a>\n");
	print("までお知らせ下さい。</p>\n");
    } elsif ($MyFatalNo == 4) {
	print("<p>ごめんなさい、題中にHTMLタグを入れることは\n");
	print("禁じられています。戻ってもう一度。</a>\n");
    } elsif ($MyFatalNo == 5) {
	print("<p>関数$MyFatalInfoにおいて、ありえない位置に\n");
	print("プログラムの制御が移動しました。");
	print("このエラーが生じた状況を");
	print("<a href=\"mailto:$MAINT\">$MAINT</a>まで");
	print("お知らせ下さい。</p>\n");
    } elsif ($MyFatalNo == 6) {
	print("<p>登録されているエイリアスのものと、\n");
	print("ホスト名が一致しません。\n");
	print("戻ってもう一度。</p>\n");
    } elsif ($MyFatalNo == 7) {
	print("<p>$MyFatalInfoというエイリアスは\n");
	print("登録されていません。\n");
	print("戻ってもう一度。</p>\n");
    } elsif ($MyFatalNo == 8) {
	print("<p>$MyFatalInfoがおかしくありませんか?\n");
	print("戻ってもう一度。</p>\n");
    } elsif ($MyFatalNo == 9) {
	print("<p>メールが送信できませんでした。\n");
	print("このエラーが生じた状況を");
	print("<a href=\"mailto:$MAINT\">$MAINT</a>まで");
	print("お知らせ下さい。</p>\n");
    } elsif ($MyFatalNo == 10) {
	print("<p>$URLにアクセスできません.\n");
	print("Try later.</p>\n");
    } elsif ($MyFatalNo == 11) {
	print("<p>次の記事はまだ投稿されていません。</p>\n");
    } else {
	print("<p>エラー番号不定: お手数ですが、");
	print("このエラーが生じた状況を");
	print("<a href=\"mailto:$MAINT\">$MAINT</a>まで");
	print("お知らせ下さい。</p>\n");
    }
    
    &MsgFooter();
    exit 0;
}
