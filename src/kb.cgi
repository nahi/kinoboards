#!/usr/local/bin/perl5
#
# $Id: kb.cgi,v 4.38 1997-02-14 11:41:00 nakahiro Exp $


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


# This file implements main functions of KINOBOARDS.


###
## 環境変数を拾う
#
$SERVER_NAME = $ENV{'SERVER_NAME'};
$SERVER_PORT = $ENV{'SERVER_PORT'};
$SCRIPT_NAME = $ENV{'SCRIPT_NAME'};
$REMOTE_HOST = $ENV{'REMOTE_HOST'};
$PATH_INFO = $ENV{'PATH_INFO'};
$PATH_TRANSLATED = $ENV{'PATH_TRANSLATED'};
($CGIPROG_NAME = $SCRIPT_NAME) =~ s!^(.*/)!!o;
$SYSDIR_NAME = (($PATH_INFO) ? "$PATH_INFO/" : "$1");
$SCRIPT_URL = "http://$SERVER_NAME:$SERVER_PORT$SCRIPT_NAME$PATH_INFO";
$PROGRAM = (($PATH_INFO) ? "$SCRIPT_NAME$PATH_INFO" : $CGIPROG_NAME);


###
## インクルードファイルの読み込み
#
chdir($PATH_TRANSLATED) if ($PATH_TRANSLATED ne '');
require('kb.ph');
require('cgi.pl');
require('tag_secure.pl');
require('jcode.pl');


###
## 大域変数の定義
#

#
# 配列のdefault
#
$[ = 0;
$| = 1;

#
# VersionとRelease番号
#
$KB_VERSION = '1.0';
$KB_RELEASE = '3.3pre';

#
# 著作権表示
#
$ADDRESS = sprintf("Maintenance: <a href=\"mailto:%s\">%s</a><br>
<a href=\"http://www.kinotrope.co.jp/~nakahiro/kb10.shtml\">KINOBOARDS/%s R%s</a>: Copyright (C) 1995, 96, 97 <a href=\"http://www.kinotrope.co.jp/~nakahiro/\">NAKAMURA Hiroshi</a>.", $MAINT, $MAINT_NAME, $KB_VERSION, $KB_RELEASE);

#
# ファイル
#
# 記事番号ファイル
$ARTICLE_NUM_FILE_NAME = '.articleid';
# 記事番号テンポラリファイル
$ARTICLE_NUM_TMP_FILE_NAME = '.articleid.tmp';
# 掲示板別configuratinファイル
$CONF_FILE_NAME = '.kbconf';
# タイトルリストヘッダファイル
$BOARD_FILE_NAME = '.board';
# DBファイル
$DB_FILE_NAME = '.db';
# DBテンポラリファイル
$DB_TMP_FILE_NAME = '.db.tmp';
# ユーザエイリアスファイル
$USER_ALIAS_FILE = 'kinousers';
# ユーザエイリアステンポラリファイル
$USER_ALIAS_TMP_FILE = 'kinousers.tmp';
# ボードエイリアスファイル
$BOARD_ALIAS_FILE = 'kinoboards';
# デフォルトのアイコン定義ファイル
$DEFAULT_ICONDEF = 'all.idef';
# ロックファイル
$LOCK_FILE = '.lock.kb';
# ロック元ファイル
$LOCK_ORG = '.lock.kb.org';
# ロック時のリトライ回数
$LOCK_WAIT = 10;

#
# アイコンディレクトリ
# (アイコンとアイコン定義ファイルを入れるディレクトリ名)
#
$ICON_DIR = 'icons';

# アイコンファイル
$ICON_TLIST = &GetIconURL('tlist.gif');
$ICON_NEXT = &GetIconURL('next.gif');
$ICON_WRITENEW = &GetIconURL('writenew.gif');
$ICON_FOLLOW = &GetIconURL('follow.gif');
$ICON_QUOTE = &GetIconURL('quote.gif');
$ICON_THREAD = &GetIconURL('thread.gif');
$ICON_HELP = &GetIconURL('q.gif');

#
# アイコン定義ファイルのポストフィクス
# アイコン定義ファイル，「(ボードディレクトリ名).(指定した文字列)」になる．
$ICONDEF_POSTFIX = 'idef';
$ICON_HEIGHT = 20;
$ICON_WIDTH = 20;

#
# エスケープコード
#
$NULL_LINE = '__br__';
$DOUBLE_QUOTE = '__dq__';
$GREATER_THAN = '__gt__';
$LESSER_THAN = '__lt__';
$AND_MARK = '__amp__';

#
# フラグ
#
$F_FALSE = 0;
$F_TRUE = 1;

#
# エラーコード
#
$ERR_FILE = 1;
$ERR_NOTFILLED = 2;
$ERR_CRINDATA = 3;
$ERR_TAGCRINDATA = 4;
$ERR_CANNOTGRANT = 5;
$ERR_UNKNOWNALIAS = 6;
$ERR_ILLEGALSTRING = 7;
$ERR_NONEXTARTICLE = 8;
$ERR_CANNOTSENDMAIL = 9;
$ERR_F_CANNOTLOCK = 999;

#
# 1日
#
$SECINDAY = 24 * 60 * 60;
$TIME = time;
$PROGTIME = ($TIME - (-M "$CGIPROG_NAME") * $SECINDAY);

# トラップ
$SIG{'HUP'} = $SIG{'INT'} = $SIG{'QUIT'} = $SIG{'TERM'} = $SIG{'TSTP'} = 'DoKill';
sub DoKill {
    &unlock;
    exit(1);
}


###
## メイン
#

&lock;

MAIN: {

    # 標準入力(POST)または環境変数(GET)のデコード．
    &cgi'decode;

    # 頻繁に使うので大域変数
    $BOARD = $cgi'TAGS{'b'};
    $BOARDNAME = &GetBoardInfo($BOARD);

    # 掲示板固有セッティングを読み込む
    local($BoardConfFile) = &GetPath($BOARD, $CONF_FILE_NAME);
    require("$BoardConfFile") if (-s "$BoardConfFile");

    # DBを大域変数にキャッシュ
    &DbCash if $BOARD;

    # 値の抽出
    local($Command) = $cgi'TAGS{'c'};
    local($Com) = $cgi'TAGS{'com'};
    local($Id) = $cgi'TAGS{'id'};

    # コマンドタイプによる分岐
    &ShowArticle($Id),		last if ($Command eq 'e');
    &NextArticle($Id),		last if ($Command eq 'en');
    &ThreadArticle($Id),	last if ($Command eq 't');
    &Entry('', ''),		last if ($Command eq 'n');
    &Entry('', $Id),		last if ($Command eq 'f');
    &Entry('quote', $Id),	last if ($Command eq 'q');
    &Preview,			last if (($Command eq 'p') && ($Com ne 'x'));
    &Thanks,			last if ($Command eq 'x');
    &Thanks,			last if (($Command eq 'p') && ($Com eq 'x'));
    &ViewTitle,			last if ($Command eq 'v');
    &SortArticle,		last if ($Command eq 'r');
    &NewArticle,		last if ($Command eq 'l');
    &SearchArticle,		last if ($Command eq 's');
    &ShowIcon,			last if ($Command eq 'i');
    &AliasNew,			last if ($Command eq 'an');
    &AliasMod,			last if ($Command eq 'am');
    &AliasDel,			last if ($Command eq 'ad');
    &AliasShow,			last if ($Command eq 'as');

    print("huh... what's up? running under any shell?\n");

}


###
## おしまい
#
&unlock;
exit(0);


###
## DBのキャッシュ
#
sub DbCash {

    # 起動時，記事DBの内容を大域変数にキャッシュする．
    @DB_ID = ();
    %DB_FID = ();
    %DB_AIDS = ();
    %DB_DATE = ();
    %DB_TITLE = ();
    %DB_ICON = ();
    %DB_REMOTEHOST = ();
    %DB_NAME = ();
    %DB_EMAIN = ();
    %DB_URL = ();
    %DB_FMAIL = ();

    local($DBFile) = &GetPath($BOARD, $DB_FILE_NAME);

    local($dId, $dFid, $dAids, $dDate, $dTitle, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail);
    local($Count) = 0;

    # 取り込み．
    open(DB, "<$DBFile") || &Fatal($ERR_FILE, $DBFile);
    while(<DB>) {

	# Version Check
	&VersionCheck('DB', $1), next if (m/^\# Kb-System-Id: ([^\/]*\/.*)$/o);

	next if (/^\#/o);
	next if (/^$/o);
	chop;

	($dId, $dFid, $dAids, $dDate, $dTitle, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail) = split(/\t/, $_, 11);
	next if ($dId eq '');

	$DB_ID[$Count++] = $dId;
	$DB_FID{$dId} = $dFid;
	$DB_AIDS{$dId} = $dAids;
	$DB_DATE{$dId} = $dDate || &GetModifiedTime($dId);
	$DB_TITLE{$dId} = $dTitle || $dId;
	$DB_ICON{$dId} = $dIcon;
	$DB_REMOTEHOST{$dId} = $dRemoteHost;
	$DB_NAME{$dId} = $dName || $MAINT_NAME;
	$DB_EMAIL{$dId} = $dEmail;
	$DB_URL{$dId} = $dUrl;
	$DB_FMAIL{$dId} = $dFmail;

    }
    close(DB);

}


###
## 書き込み画面
#
sub Entry {

    # 引用あり/なしと，引用する場合はそのId(引用しない時は空)
    local($QuoteFlag, $Id) = @_;

    # 表示画面の作成
    &MsgHeader('Message entry', "$BOARDNAME: $ENTRY_MSG", $PROGTIME);

    # フォローの場合
    if ($Id ne '') {
	# 記事の表示(コマンド無し, 元記事あり)
	&ViewOriginalArticle($Id, $F_FALSE, $F_TRUE);
	print("<hr>\n");
	&cgi'KPrint("<h2>$H_REPLYMSG</h2>");
    }

    # ヘッダ部分の表示
    &EntryHeader((($Id eq '') ? '' : &GetReplySubject($Id)), $Id);

    # 本文(引用ありなら元記事を挿入)
    print("<p><textarea name=\"article\" rows=\"$TEXT_ROWS\" cols=\"$TEXT_COLS\">");
    &QuoteOriginalArticle($Id, $BOARD) if (($Id ne '') && ($QuoteFlag eq 'quote'));
    print("</textarea></p>\n");

    # フッタ部分を表示
    &EntryFooter;

}


###
## 書き込み画面のうち，あおり文，TextType，Board名を表示．
#
sub EntryHeader {

    local($Subject, $Id) = @_;

    # お約束
    &cgi'KPrint(<<__EOF__);
<form action="$PROGRAM" method="POST">
<input name="c" type="hidden" value="p">
<input name="b" type="hidden" value="$BOARD">
<input name="id" type="hidden" value="$Id">
<p>
$H_AORI_1
__EOF__
    &cgi'KPrint("$H_AORI_2\n") if ($SYS_TEXTTYPE);
    &cgi'KPrint(<<__EOF__);
</p>
<p>
$H_BOARD: $BOARDNAME<br>
__EOF__

    # アイコンの選択
    if ($SYS_ICON) {
	&cgi'KPrint(<<__EOF__);
$H_ICON:
<SELECT NAME="icon">
<OPTION SELECTED>$H_NOICON
__EOF__

	# 一つ一つ表示
	open(ICON, &GetIconPath("$BOARD.$ICONDEF_POSTFIX"))
	    || (open(ICON, &GetIconPath("$DEFAULT_ICONDEF"))
		|| &Fatal($ERR_FILE, &GetIconPath("$DEFAULT_ICONDEF")));
	while(<ICON>) {

	    # Version Check
	    &VersionCheck('Icon', $1), next if (m/^\# Kb-System-Id: ([^\/]*\/.*)$/o);

	    # コメント文はキャンセル
	    next if (/^\#/o);
	    next if (/^$/o);

	    # 表示
	    chop;
	    ($FileName, $Title) = split(/\t/, $_, 3);
	    &cgi'KPrint("<OPTION>$Title\n");

	}
	close(ICON);
	print("</SELECT>\n");
	&cgi'KPrint("(<a href=\"$PROGRAM?b=$BOARD&c=i&type=entry\">$H_SEEICON</a>)<BR>\n");
    }

    # Subject(フォローなら自動的に文字列を入れる)
    &cgi'KPrint(sprintf("%s: <input name=\"subject\" type=\"text\" value=\"%s\" size=\"%s\"><br>\n", $H_SUBJECT, $Subject, $SUBJECT_LENGTH));

    # TextType
    if ($SYS_TEXTTYPE) {
	&cgi'KPrint(<<__EOF__);
$H_TEXTTYPE:
<SELECT NAME="texttype">
<OPTION SELECTED>$H_PRE
<OPTION>$H_HTML
</SELECT>
</p>
__EOF__

    }

}


###
## フッタ部分を表示
#
sub EntryFooter {

    # 名前とメイルアドレス，URL．
    &cgi'KPrint(<<__EOF__);
<p>
$H_LINK
</p><p>
$H_FROM: <input name="name" type="text" size="$NAME_LENGTH"><br>
$H_MAIL: <input name="mail" type="text" size="$MAIL_LENGTH"><br>
$H_URL_S: <input name="url" type="text" value="http://" size="$URL_LENGTH"><br>
__EOF__

    ($SYS_FOLLOWMAIL) && &cgi'KPrint("$H_FMAIL <input name=\"fmail\" type=\"checkbox\" value=\"on\"><br>\n");
    
    if ($SYS_ALIAS) {
	&cgi'KPrint(<<__EOF__);
</p><p>
$H_ALIASINFO
(<a href="$PROGRAM?c=as">$H_SEEALIAS</a> //
 <a href="$PROGRAM?c=an">$H_ALIASENTRY</a>)
__EOF__

    }

    # ボタン
    &cgi'KPrint(<<__EOF__);
</p><p>
<input type="radio" name="com" value="p" CHECKED>: $H_PREVIEW<br>
<input type="radio" name="com" value="x">: $H_ENTRY<br>
<input type="submit" value="$H_PUSHHERE_POST">
</p>
</form>
__EOF__

    &MsgFooter;
}


###
## あるIdの記事からSubjectを取ってきて，先頭に「Re:」を1つだけつけて返す．
#
sub GetReplySubject {

    # IdとBoard
    local($Id) = @_;

    # 記事情報
    local($dFid, $dAids, $dDate, $dSubject) = &GetArticlesInfo($Id);

    # 先頭に「Re:」がくっついてたら取り除く．
    $dSubject =~ s/^Re:\s*//oi;

    # 先頭に「Re: 」をくっつけて返す．
    return("Re: $dSubject");

}


###
## 引用する
#
sub QuoteOriginalArticle {

    # IdとBoard
    local($Id, $Board) = @_;

    # 引用するファイル
    local($QuoteFile) = &GetArticleFileName($Id, $Board);

    # 元記事情報の取得
    local($Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name) = &GetArticlesInfo($Id);

    # ファイルを開く
    open(TMP, "<$QuoteFile") || &Fatal($ERR_FILE, $QuoteFile);
    while(<TMP>) {

	# Version Check
	&VersionCheck('Article', $1), next if (m/^<!-- Kb-System-Id: ([^\/]*\/.*) -->$/o);

	# 引用のための変換
	s/\&//go;
	s/\"//go;
	s/<[^>]*>//go;

	# 引用文字列の表示
	&cgi'KPrint(sprintf("%s%s%s", $Name, $DEFAULT_QMARK, $_));
	
    }

    # 閉じる
    close(TMP);

}


###
## プレビュー画面
#
sub Preview {

    # 入力された記事情報
    local($Id) = $cgi'TAGS{'id'};
    local($TextType) = $cgi'TAGS{'texttype'};
    local($Name) = $cgi'TAGS{'name'};
    local($Email) = $cgi'TAGS{'mail'};
    local($Url) = $cgi'TAGS{'url'};
    local($Icon) = $cgi'TAGS{'icon'};
    local($Subject) = $cgi'TAGS{'subject'};
    local($Article) = $cgi'TAGS{'article'};
    local($Qurl) = $cgi'TAGS{'qurl'};
    local($Fmail) = $cgi'TAGS{'fmail'};

    # 引用記事の記事情報
    local($rFid) = &GetArticlesInfo($Id) if ($Id ne '');

    # 入力された記事情報のチェック
    $Article = &CheckArticle($TextType, *Name, *Email, *Url, *Subject, *Icon, $Article);

    # 確認画面の作成
    &MsgHeader('Message preview', $PREVIEW_MSG, $TIME);

    # お約束
    &cgi'KPrint(<<__EOF__);
<form action="$PROGRAM" method="POST">
<input name="c"        type="hidden" value="x">
<input name="b"        type="hidden" value="$BOARD">
<input name="id"       type="hidden" value="$Id">
<input name="texttype" type="hidden" value="$TextType">
<input name="name"     type="hidden" value="$Name">
<input name="mail"     type="hidden" value="$Email">
<input name="url"      type="hidden" value="$Url">
<input name="icon"     type="hidden" value="$Icon">
<input name="subject"  type="hidden" value="$Subject">
<input name="article"  type="hidden" value="$Article">
<input name="qurl"     type="hidden" value="$Qurl">
<input name="fmail"    type="hidden" value="$Fmail">

<p>
$H_POSTINFO
<input type="submit" value="$H_PUSHHERE_PREVIEW">
</p><p>
__EOF__

    # 題
    (($Icon eq $H_NOICON) || (! $Icon))
        ? &cgi'KPrint("<strong>$H_SUBJECT</strong>: $Subject")
            : &cgi'KPrint(sprintf("<strong>$H_SUBJECT</strong>: <img src=\"%s\" alt=\"$Icon \" width=\"$ICON_WIDTH\" height=\"$ICON_HEIGHT\">$Subject", &GetIconURLFromTitle($Icon)));

    # お名前
    if ($Url ne '') {
        # URLがある場合
        &cgi'KPrint("<br>\n<strong>$H_FROM</strong>: <a href=\"$Url\">$Name</a>");
    } else {
        # URLがない場合
        &cgi'KPrint("<br>\n<strong>$H_FROM</strong>: $Name");
    }

    # メイル
    &cgi'KPrint(" <a href=\"mailto:$Email\">&lt;$Email&gt;</a>") if ($Email ne '');

    # 反応元(引用の場合)
    if (defined($rFid)) {
	if ($rFid ne '') {
	    &ShowLinksToFollowedArticle(($Id, split(/,/, $rFid)));
	} else {
	    &ShowLinksToFollowedArticle($Id);
	}
    }

    # 切れ目
    &cgi'KPrint("</p>\n$H_LINE<br>\n");

    # TextType用前処理
    print("<p><pre>") if ((! $SYS_TEXTTYPE) || ($TextType eq $H_PRE));

    # 記事
    $Article = &DQDecode($Article);
    $Article = &ArticleEncode($TextType, $Article);
    &cgi'KPrint("$Article\n");

    # TextType用後処理
    print("</pre></p>\n") if ((! $SYS_TEXTTYPE) || ($TextType eq $H_PRE));

    # お約束
    print("</form>\n");

    &MsgFooter;
}


###
## 登録後画面
#
sub Thanks {

    # 新たに記事を生成する
    local($Id) = &MakeNewArticle;

    # 表示画面の作成
    &MsgHeader('Message entried', $THANKS_MSG, $TIME);

    &cgi'KPrint(<<__EOF__);
<p>
$H_THANKSMSG
</p>
<form action="$PROGRAM" method="POST">
<input name="b" type="hidden" value="$BOARD">
<input name="c" type="hidden" value="v">
<input name="num" type="hidden" value="$DEF_TITLE_NUM">
<input type="submit" value="$H_BACKTITLE">
</form>
__EOF__

    if ($Id ne '') {
	&cgi'KPrint(<<__EOF__);
<form action="$PROGRAM" method="POST">
<input name="b" type="hidden" value="$BOARD">
<input name="c" type="hidden" value="e">
<input name="id" type="hidden" value="$Id">
<input type="submit" value="$H_BACKORG">
</form>
__EOF__
    }

    &MsgFooter;

}


###
## 新たに投稿された記事の生成
#
sub MakeNewArticle {

    # 入力された記事情報
    local($Id) = $cgi'TAGS{'id'};
    local($TextType) = $cgi'TAGS{'texttype'};
    local($Name) = $cgi'TAGS{'name'};
    local($Email) = $cgi'TAGS{'mail'};
    local($Url) = $cgi'TAGS{'url'};
    local($Icon) = $cgi'TAGS{'icon'};
    local($Subject) = $cgi'TAGS{'subject'};
    local($Article) = $cgi'TAGS{'article'};
    local($Qurl) = $cgi'TAGS{'qurl'};
    local($Fmail) = $cgi'TAGS{'fmail'};

    local($ArticleId);

    # 入力された記事情報のチェック
    $Article = &CheckArticle($TextType, *Name, *Email, *Url, *Subject, *Icon, $Article);

    # 新しい記事番号を取得(まだ記事番号は増えてない)
    $ArticleId = &GetNewArticleId;

    # 正規のファイルの作成
    &MakeArticleFile($TextType, $Article, $ArticleId);

    # 新しい記事番号を書き込む
    &WriteArticleId($ArticleId);

    # DBファイルに投稿された記事を追加
    # 通常の記事引用ならID
    &AddDBFile($ArticleId, $Id, $TIME, $Subject, $Icon, $REMOTE_HOST, $Name, $Email, $Url, $Fmail);

    # 元記事へのリンクのために
    return($Id);

}


###
## 入力された記事情報のチェック
#
sub CheckArticle {

    # 記事情報いろいろ
    local($TextType, *Name, *Email, *Url, *Subject, *Icon, $Article) = @_;
    local($Tmp) = '';

    # エイリアスチェック
    $_ = $Name;
    if (/^\#.*$/o) {
        ($Tmp, $Email, $Url) = &GetUserInfo($_);
	&Fatal($ERR_UNKNOWNALIAS, $Name) if ($Tmp eq '');
	$Name = $Tmp;
    }

    # 文字列チェック
    &CheckName(*Name);
    &CheckEmail(*Email);
    &CheckURL(*Url);
    &CheckSubject(*Subject);

    # 空チェック
    (! $Article) && &Fatal($ERR_NOTFILLED, '');

    # アイコンのチェック; おかしけりゃ「無し」に設定．
    $Icon = $H_NOICON unless (&GetIconURLFromTitle($Icon));

    # 記事中の"をエンコード
    $Article = &DQEncode($Article);

    return($Article);

}


###
## 記事を書き出す．
#
sub MakeArticleFile {

    # TextTypeと記事そのもの，Id
    local($TextType, $Article, $Id) = @_;

    # ファイル名を取得
    local($File) = &GetArticleFileName($Id, $BOARD);

    # ファイルを開く
    open(TMP, ">$File") || &Fatal($ERR_FILE, $File);

    # バージョン情報を書き出す
    printf(TMP "<!-- Kb-System-Id: %s/%s -->\n", $KB_VERSION, $KB_RELEASE);

    # TextType用前処理
    print(TMP "<p><pre>") if ((! $SYS_TEXTTYPE) || ($TextType eq $H_PRE));

    # 記事; "をデコードし，セキュリティチェック
    $Article = &DQDecode($Article);
    $Article = &ArticleEncode($TextType, $Article);
    print(TMP "$Article\n");

    # TextType用後処理
    print(TMP "</pre></p>\n") if ((! $SYS_TEXTTYPE) || ($TextType eq $H_PRE));

    # 終了
    close(TMP);

}


###
## 特殊文字のencode and decode
#
sub DQEncode {
    local($Str) = @_;
    $Str =~ s/\"/$DOUBLE_QUOTE/go;
    $Str =~ s/\>/$GREATER_THAN/go;
    $Str =~ s/\</$LESSER_THAN/go;
    $Str =~ s/\&/$AND_MARK/go;
    return($Str);
}

sub DQDecode {
    local($Str) = @_;
    $Str =~ s/$DOUBLE_QUOTE/\"/go;
    $Str =~ s/$GREATER_THAN/\>/go;
    $Str =~ s/$LESSER_THAN/\</go;
    $Str =~ s/$AND_MARK/\&/go;
    return($Str);
}


###
## 記事のencode and decode
#
sub ArticleEncode {

    local($TestType, $Article) = @_;
    local($Return) = $Article;
    local(@Cash) = ();
    local($Url, $Str);

    while ($Article =~ m/<URL:([^>]*)>/g) {
	$Url = $1;
	next if (grep(/^$Url$/, @Cash));
	push(Cash, $Url);
	if (&IsUrl($Url)) {
	    $Str = "<a href=\"$Url\"><URL:$Url></a>";
	}
	$Return =~ s/<URL:$Url>/$Str/g;
    }

    &tag_secure'decode(*Return); #'

    return($Return);

}


###
## 記事番号を増やす．
#
sub WriteArticleId {

    local($Id) = @_;

    # 記事番号を収めるファイル
    local($File) = &GetPath($BOARD, $ARTICLE_NUM_FILE_NAME);
    local($TmpFile) = &GetPath($BOARD, $ARTICLE_NUM_TMP_FILE_NAME);

    # 数字のくせに古い数値より若い!
    local($OldArticleId) = &GetNewArticleId;
    &Fatal($ERR_ILLEGALARTICLEID, '') if (($Id =~ /^\d+$/) && ($Id < $OldArticleId));

    # Open Tmp File
    open(AID, ">$TmpFile") || &Fatal($ERR_FILE, $TmpFile);
    # 記事ID
    print(AID "$Id\n");
    close(AID);

    # 更新
    rename($TmpFile, $File);

}


###
## DBファイルに書き込む
#
sub AddDBFile {

    # 記事Id，名前，アイコン，題，日付
    local($Id, $Fid, $InputDate, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail, $ArticleNullFlag) = @_;

    local($dId, $dFid, $dAids, $dInputDate, $dSubject, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail);
    local($mdName, $mdInputDate, $mdSubject, $mdId, $mName, $mSubject, $mId, @To) = ();
    local($FidList) = $Fid;
    local($FFid, @FFid) = ();

    # リプライ元のリプライ元，を取ってくる(DBへのアクセスが増える……)
    if ($Fid ne '') {
	($FFid) = &GetArticlesInfo($Fid);
	@FFid = split(/,/, $FFid);
    }
    
    # 登録ファイル
    local($File) = &GetPath($BOARD, $DB_FILE_NAME);
    local($TmpFile) = &GetPath($BOARD, $DB_TMP_FILE_NAME);

    # Open Tmp File
    open(DBTMP, ">$TmpFile") || &Fatal($ERR_FILE, $TmpFile);
    # Open DB File
    open(DB, "<$File") || &Fatal($ERR_FILE, $File);

    while(<DB>) {

	# Version Check
	&VersionCheck('DB', $1) if (m/^\# Kb-System-Id: ([^\/]*\/.*)$/o);

	print(DBTMP "$_"), next if (/^\#/o);
	print(DBTMP "$_"), next if (/^$/o);
	chop;

	($dId, $dFid, $dAids, $dInputDate, $dSubject, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail) = split(/\t/, $_);
	
	# フォロー先記事が見つかったら，
	if (($dId ne '') && ($dId eq $Fid)) {

	    # その記事のフォロー記事IDリストに加える(カンマ区切り)
	    if ($dAids ne '') {$dAids .= ",$Id";} else {$dAids = $Id;}

	    # 元記事のフォロー先リストを取ってきて元記事を加え，
	    # 新記事のフォロー先リストを作る
	    $FidList = "$dId,$dFid" if ($dFid ne '');

	    if ($SYS_FOLLOWMAIL) {
		# メイル送信のためにキャッシュ
		$mdName = $dName;
		$mdInputDate = $dInputDate;
		$mdSubject = $dSubject;
		$mdId = $dId;
		$mName = $Name;
		$mSubject = $Subject;
		$mId = $Id;
		push(To, $dEmail) if ($dFmail ne '');
	    }
	}

	# DBに書き加える
	printf(DBTMP "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n", $dId, $dFid, $dAids, $dInputDate, $dSubject, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail);

	# リプライ元のリプライ元，かつメイル送信の必要があれば，宛先を保存
	push(To, $dEmail) if ($SYS_FOLLOWMAIL && (@FFid) && $dFmail && $dEmail && (grep(/^$dId$/, @FFid)) && (! grep(/^$dEmail$/, @To)));

    }

    # 新しい記事のデータを書き加える．
    printf(DBTMP "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n", $Id, $FidList, '', $InputDate, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail);

    # close Files.
    close(DB);
    close(DBTMP);

    # DBを更新する
    rename($TmpFile, $File);

    # 必要なら反応があったことをメイルする
    &FollowMail($mdName, $mdInputDate, $mdSubject, $mdId, $mName, $mSubject, $mId, @To) if (@To);

}


###
## 単一の記事を表示．
#
sub ShowArticle {

    # 記事のIdを取得
    local($Id) = @_;

    # 記事情報の取得
    local($Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url) = &GetArticlesInfo($Id);
    local($DateUtc) = &GetUtcFromOldDateTimeFormat($Date);
    local(@AidList) = split(/,/, $Aids);
    local($Aid);

    # 未投稿記事は読めない
    &Fatal($ERR_NONEXTARTICLE, '') if ($Name eq '');

    # 表示画面の作成
    &MsgHeader('Message view', "$Subject", $DateUtc);
    &ViewOriginalArticle($Id, $F_TRUE, $F_TRUE);

    # article end
    &cgi'KPrint("$H_LINE<br>\n<p>\n");

    # 反応記事
    &cgi'KPrint("$H_FOLLOW\n");
    if ($Aids ne '') {

	# 反応記事があるなら…
	foreach $Aid (@AidList) {

	    # フォロー記事の木構造の取得
	    # ex. '( a ( b ( c d ) ) ( e ) ( f ( g ) ) )'というリスト
	    local(@FollowIdTree) = &GetFollowIdTree($Aid);

	    # メイン関数の呼び出し(記事概要)
	    &ThreadArticleMain('subject only', @FollowIdTree);

	}

    } else {

	# 反応記事無し
	&cgi'KPrint("<ul>\n<li>$H_NOTHING\n</ul>\n");

    }

    print("</p>\n");

    # お約束
    &MsgFooter;

}


###
## 次の記事を表示．
#
sub NextArticle {

    local($Id) = @_;

    local($Num) = '';
    local($Key, $Value);

    foreach ($[ .. $#DB_ID) {
	$Num = $_, last if ($DB_ID[$_] eq $Id);
    }

    &ShowArticle($DB_ID[++$Num]);

}


###
## フォロー記事を全て表示．
#
sub ThreadArticle {

    # 元記事のIdを取得
    local($Id) = @_;

    # フォロー記事の木構造の取得
    # ex. '( a ( b ( c d ) ) ( e ) ( f ( g ) ) )'というリスト
    local(@FollowIdTree) = &GetFollowIdTree($Id);

    # 表示画面の作成
    &MsgHeader('Message view (threaded)', "$BOARDNAME: $THREADARTICLE_MSG", $TIME);

    # メイン関数の呼び出し(記事概要)
    &ThreadArticleMain('subject only', @FollowIdTree);

    # メイン関数の呼び出し(記事)
    &ThreadArticleMain('', @FollowIdTree);

    &MsgFooter;

}


###
## 再帰的にその記事のフォローを表示する．
#
sub ThreadArticleMain {

    # Idの取得
    local($SubjectOnly, $Head, @Tail) = @_;

    # 記事概要か，記事そのものか．
    if ($SubjectOnly) {

	if ($Head eq '(') {
	    print("<ul>\n");
	} elsif ($Head eq ')') {
	    print("</ul>\n");
	} else {
	    &PrintAbstract($Head);
	}

    } else {

	if (($Head ne '(') && ($Head ne ')')) {
	    # 元記事の表示(コマンド付き, 元記事なし)
	    print("<hr>\n");
	    &ViewOriginalArticle($Head, $F_TRUE, $F_FALSE);
	}

    }

    # 再帰
    &ThreadArticleMain($SubjectOnly, @Tail) if @Tail;

}


###
## フォロー記事のIdの木構造を取り出す．
##
## ex. '( a ( b ( c d ) e ( f ) ) g ( h ) )'というリスト
##
## a - b - c
##       - d
##     e - f
## g - h
##
#
sub GetFollowIdTree {

    # Id
    local($Id) = @_;

    # 再帰的に木構造を取り出す．
    return('(', &GetFollowIdTreeMain($Id), ')');

}

sub GetFollowIdTreeMain {

    # Id
    local($Id) = @_;

    # 再帰停止条件
    return() if ($Id eq '');

    # フォロー記事取り出し
    local(@AidList) = split(/,/, $DB_AIDS{$Id});

    # なけりゃ停止
    return($Id) unless @AidList;

    # 再帰
    local(@Result) = ($Id, '(');
    local(@ChildResult) = ();
    foreach (@AidList) {
	@ChildResult = &GetFollowIdTreeMain($_);
	push(Result, @ChildResult) if @ChildResult;
    }
    return(@Result, ')');

}


###
## 記事の概要の表示
#
sub PrintAbstract {

    # Id
    local($Id) = @_;

    # 記事情報を取り出す．
    local($dFid, $dAids, $dDate, $dSubject, $dIcon, $dRemoteHost, $dName) = &GetArticlesInfo($Id);
    &cgi'KPrint(sprintf("<li>" . &GetFormattedTitle($Id, $dAids, $dIcon, $dSubject, $dName, $dDate) . "\n"));
}


###
## ユーザエイリアスからユーザの名前，メイル，URLを取ってくる．
#
sub GetUserInfo {

    # 検索するエイリアス名
    local($Alias) = @_;

    # エイリアス，名前，メイル，マシン，URL
    local($A, $N, $E, $H, $U);

    # エイリアス，名前，メイル，マシン，URL
    local($rN, $rE, $rU) = ();

    # ファイルを開く
    open(ALIAS, "<$USER_ALIAS_FILE") || &Fatal($ERR_FILE, $USER_ALIAS_FILE);
    
    # 1つ1つチェック．
    while(<ALIAS>) {
	
	# Version Check
	&VersionCheck('Alias', $1), next if (m/^<!-- Kb-System-Id: ([^\/]*\/.*) -->$/o);

	next if (/^$/o);
	chop;
	
	# 分割
	($A, $N, $E, $H, $U) = split(/\t/, $_);
	
	# マッチしなきゃ次へ．
	next if ($A ne $Alias);
	
	$rN = $N;
	$rE = $E;
	$rU = $U;

    }
    close(ALIAS);

    # リストにして返す
    return($rN, $rE, $rU);
}


###
## 反応があったことをメイルする．
#
sub FollowMail {

    # 宛先いろいろ
    local($Name, $Date, $Subject, $Id, $Fname, $Fsubject, $Fid, @To) = @_;

    local($URL) = "$SCRIPT_URL?b=$BOARD&c=e&id=$Id";
    local($FURL) = "$SCRIPT_URL?b=$BOARD&c=e&id=$Fid";
    
    # Subject
    local($MailSubject) = "The article was followed.";

    # Date
    local($InputDate) = &GetDateTimeFormatFromUtc($Date);

    # Message
    local($Message) = "$SYSTEM_NAMEからのお知らせです．

$InputDateに「$BOARDNAME」に対して「$Name」さんが書いた，
「$Subject」
$URL
に対して，
「$Fname」さんから
「$Fsubject」という題での反応がありました．

お時間のある時に
$FURL
を御覧下さい．

では失礼します．";

    # メイル送信
    &SendMail($MailSubject, $Message, $Fid, @To);
}


###
## メイル送信
#
sub SendMail {

    # subject，メイルのファイル名，引用記事(空なら無し)，宛先
    local($Subject, $Message, $Id, @To) = @_;

    # 付加ヘッダの生成
    local($ExtensionHeader) = "X-Kb-System: $SYSTEM_NAME\n";
    $ExtensionHeader .= "X-Kb-Board: $BOARDNAME\nX-Kb-Articleid: $Id\n" if ($BOARDNAME && ($Id ne ''));

    # 引用記事
    if ($Id ne '') {

	# 引用するファイル
	local($QuoteFile) = &GetArticleFileName($Id, $BOARD);

	# 区切り線
	$Message .= "\n$H_LINE\n";

	# 引用
	open(TMP, "<$QuoteFile") || &Fatal($ERR_FILE, $QuoteFile);
	while(<TMP>) {

	    # Version Check
	    &VersionCheck('Article', $1), next if (m/^<!-- Kb-System-Id: ([^\/]*\/.*) -->$/o);

	    # タグは要らない
	    s/<[^>]*>//go;
	    $Message .= &HTMLDecode($_) if ($_ ne '');

	}
	close(TMP);

    }

    # 送信する
    &Fatal($ERR_CANNOTSENDMAIL, '') unless (&cgi'SendMail($MAINT_NAME, $MAINT, $Subject, $ExtensionHeader, $Message, @To));

}

sub HTMLEncode {
    local($_) = @_;
    s/\&/&amp;/go;
    s/\"/&quot;/go;
    s/\>/&gt;/go;
    s/\</&lt;/go;
    return($_);
}

sub HTMLDecode {
    local($_) = @_;
    s/&quot;/\"/gio;
    s/&gt;/\>/gio;
    s/&lt;/\</gio;
    s/&amp;/\&/gio;
    return($_);
}


###
## アイコン表示画面
#
sub ShowIcon {

    local($FileName, $Title, $Help);

    # タイプを拾う
    local($Type) = $cgi'TAGS{'type'};

    # 表示画面の作成
    &MsgHeader('Icon show', $SHOWICON_MSG, $PROGTIME);

    if ($Type eq 'article') {

	&cgi'KPrint(<<__EOF__);
<p>
$H_ICONINTRO_ARTICLE
</p>
<p>
<ul>
<li><img src="$ICON_TLIST" alt="$H_BACKTITLE" height="$ICON_HEIGHT" width="$ICON_WIDTH"> : $H_BACKTITLE
<li><img src="$ICON_NEXT" alt="$H_NEXTARTICLE" height="$ICON_HEIGHT" width="$ICON_WIDTH"> : $H_NEXTARTICLE
<li><img src="$ICON_FOLLOW" alt="$H_REPLYTHISARTICLE" height="$ICON_HEIGHT" width="$ICON_WIDTH"> : $H_REPLYTHISARTICLE
<li><img src="$ICON_QUOTE" alt="$H_REPLYTHISARTICLEQUOTE" height="$ICON_HEIGHT" width="$ICON_WIDTH"> : $H_REPLYTHISARTICLEQUOTE
<li><img src="$ICON_THREAD" alt="$H_READREPLYALL" height="$ICON_HEIGHT" width="$ICON_WIDTH"> : $H_READREPLYALL
</ul>
</p>
__EOF__

    } else {

	&cgi'KPrint(<<__EOF__);
<p>
$H_ICONINTRO_ARTICLE
<p>
<ul>
<li>$H_THREAD : $THREADARTICLE_MSG
</ul>
</p>
<p>
"$BOARDNAME"$H_ICONINTRO_ENTRY
</p>
<p>
<ul>
__EOF__

	# 一つ一つ表示
	open(ICON, &GetIconPath("$BOARD.$ICONDEF_POSTFIX"))
	    || (open(ICON, &GetIconPath("$DEFAULT_ICONDEF"))
		|| &Fatal($ERR_FILE, &GetIconPath("$DEFAULT_ICONDEF")));
	while(<ICON>) {

	    # Version Check
	    &VersionCheck('Icon', $1), next if (m/^\# Kb-System-Id: ([^\/]*\/.*)$/o);

	    # コメント文はキャンセル
	    next if (/^\#/o);
	    next if (/^$/o);
	    chop;
	    ($FileName, $Title, $Help) = split(/\t/, $_, 3);

	    # 表示
	    &cgi'KPrint(sprintf("<li><img src=\"%s\" alt=\"$Title\" height=\"$ICON_HEIGHT\" width=\"$ICON_WIDTH\"> : %s\n", &GetIconURL($FileName), ($Help || $Title)));
	}
	close(ICON);

	print("</ul>\n</p>\n");

    }

    &MsgFooter;

}


###
## 日付順にソート．
#
sub SortArticle {

    # 表示する個数を取得
    local($Num, $Old) = ($cgi'TAGS{'num'}, $cgi'TAGS{'old'});
    local($NextOld) = ($Old > $Num) ? ($Old - $Num) : 0;
    local($BackOld) = ($Old + $Num);
    local($To) = $#DB_ID - $Old;
    local($From) = $To - $Num + 1; $From = 0 if (($From < 0) || ($Num == 0));
    
    # 記事情報
    local($IdNum, $Id);

    # 表示画面の作成
    &MsgHeader('Title view (sorted)', "$BOARDNAME: $SORT_MSG", $TIME);

    &BoardHeader;

    print("<hr>\n");

    if ($SYS_BOTTOMTITLE) {
	&cgi'KPrint("<p>$H_TOP<a href=\"$PROGRAM?b=$BOARD&c=r&num=$Num&old=$BackOld\">$H_BACKART</a></p>\n") if ($From > 0);
    } else {
	&cgi'KPrint("<p>$H_TOP<a href=\"$PROGRAM?b=$BOARD&c=r&num=$Num&old=$NextOld\">$H_NEXTART</a></p>\n") if ($Old);
    }

    print("<p><ul>\n");

    # 記事の表示
    if ($#DB_ID == -1) {

	# 空だった……
	&cgi'KPrint("<li>$H_NOARTICLE\n");

    } else {

	if ($SYS_BOTTOMTITLE) {
	    for ($IdNum = $From; $IdNum <= $To; $IdNum++) {
		$Id = $DB_ID[$IdNum];
		&cgi'KPrint("<li>" . &GetFormattedTitle($Id, $DB_AIDS{$Id}, $DB_ICON{$Id}, $DB_TITLE{$Id}, $DB_NAME{$Id}, $DB_DATE{$Id}) . "\n");
	    }
	} else {
	    for ($IdNum = $To; $IdNum >= $From; $IdNum--) {
		$Id = $DB_ID[$IdNum];
		&cgi'KPrint("<li>" . &GetFormattedTitle($Id, $DB_AIDS{$Id}, $DB_ICON{$Id}, $DB_TITLE{$Id}, $DB_NAME{$Id}, $DB_DATE{$Id}) . "\n");
	    }
	}
    }

    print("</ul></p>\n");

    if ($SYS_BOTTOMTITLE) {
	&cgi'KPrint("<p>$H_BOTTOM<a href=\"$PROGRAM?b=$BOARD&c=r&num=$Num&old=$NextOld\">$H_NEXTART</a></p>\n") if ($Old);
    } else {
	&cgi'KPrint("<p>$H_BOTTOM<a href=\"$PROGRAM?b=$BOARD&c=r&num=$Num&old=$BackOld\">$H_BACKART</a></p>\n") if ($From > 0);
    }

    &MsgFooter;

}


###
## 新しい記事のタイトルをthread別にn個を表示．
#
sub ViewTitle {

    # 表示する個数を取得
    local($Num, $Old) = ($cgi'TAGS{'num'}, $cgi'TAGS{'old'});
    local($NextOld) = ($Old > $Num) ? ($Old - $Num) : 0;
    local($BackOld) = ($Old + $Num);
    local($To) = $#DB_ID - $Old;
    local($From) = $To - $Num + 1; $From = 0 if (($From < 0) || ($Num == 0));

    # 記事情報
    local($IdNum, $Id, $Line);

    # フォーマットしたタイトルを入れるリスト
    local(@NewLines) = ();

    # 応答をインデントする．
    for ($IdNum = $From; $IdNum <= $To; $IdNum++) {
    
	# 記事情報を取り出す．
	$Id = $DB_ID[$IdNum];

	# タイトルをフォーマット
	$Line = "<!--$Id-->" . &GetFormattedTitle($Id, $DB_AIDS{$Id}, $DB_ICON{$Id}, $DB_TITLE{$Id}, $DB_NAME{$Id}, $DB_DATE{$Id});

	# 追加
	@NewLines = $DB_FID{$Id}
	    ? &AddTitleFollow((split(/,/, $DB_FID{$Id}))[0], $Line, @NewLines)
		: &AddTitleNormal($Line, @NewLines);

    }

    # 表示画面の作成
    &MsgHeader('Title view (threaded)', "$BOARDNAME: $VIEW_MSG", $TIME);

    &BoardHeader;

    print("<hr>\n");

    if ($SYS_BOTTOMTITLE) {
	&cgi'KPrint("<p>$H_TOP<a href=\"$PROGRAM?b=$BOARD&c=v&num=$Num&old=$BackOld\">$H_BACKART</a></p>\n") if ($From > 0);
    } else {
	&cgi'KPrint("<p>$H_TOP<a href=\"$PROGRAM?b=$BOARD&c=v&num=$Num&old=$NextOld\">$H_NEXTART</a></p>\n") if ($Old);
    }

    print("<p><ul>\n");

    # 記事の表示
    if (! @NewLines) {

	# 空だった……
	&cgi'KPrint("<li>$H_NOARTICLE\n");

    } else {

	foreach (@NewLines) {
	    if (! /^${NULL_LINE}$/o) {
		if ((m!^<ul>$!io) || (m!^</ul>$!io)) {
		    &cgi'KPrint("$_\n");
		} else {
		    &cgi'KPrint("<li>$_");
		}
	    }
	}
    }

    print("</ul></p>\n");

    if ($SYS_BOTTOMTITLE) {
	&cgi'KPrint("<p>$H_BOTTOM<a href=\"$PROGRAM?b=$BOARD&c=v&num=$Num&old=$NextOld\">$H_NEXTART</a></p>\n") if ($Old);
    } else {
	&cgi'KPrint("<p>$H_BOTTOM<a href=\"$PROGRAM?b=$BOARD&c=v&num=$Num&old=$BackOld\">$H_BACKART</a></p>\n") if ($From > 0);
    }

    &MsgFooter;

}


###
## タイトルリストに書き込む(新規)
#
sub AddTitleNormal {

    # 格納行，格納先
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

    # フォロー記事ID，格納行，格納先
    local($Fid, $AddLine, @Lines) = @_;
    local(@NewLines) = ();

    # Follow Flag
    local($AddFlag, $Nest, $NextLine) = (0, 0, ''); 

    # タイトルリストのフラグ
    local($TitleListFlag) = 0;

    while($_ = shift(Lines)) {

	# そのまま書き出す．
	push(NewLines, $_);

	# タイトルリスト中，お目当ての記事が来たら，
	if (/<!--$Fid-->/) {

	    # 1行空読み
	    $_ = shift(Lines);

	    if (/^<ul>/o) {
		$Nest = 1;
		do {
		    push(NewLines, $_);
		    $_ = shift(Lines);
		    $Nest++ if (/^<ul>/o);
		    $Nest-- if (/^<\/ul>/o);
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


###
## 新しい記事からn個を表示．
#
sub NewArticle {

    # 表示する個数を取得
    local($Num, $Old) = ($cgi'TAGS{'num'}, $cgi'TAGS{'old'});
    local($NextOld) = ($Old > $Num) ? ($Old - $Num) : 0;
    local($BackOld) = ($Old + $Num);
    local($To) = $#DB_ID - $Old;
    local($From) = $To - $Num + 1; $From = 0 if (($From < 0) || ($Num == 0));

    # 記事情報
    local($Id) = ();

    # 表示画面の作成
    &MsgHeader('Message view (sorted)', "$BOARDNAME: $NEWARTICLE_MSG", $TIME);

    if ($SYS_BOTTOMARTICLE) {
	&cgi'KPrint("<p>$H_TOP<a href=\"$PROGRAM?b=$BOARD&c=l&num=$Num&old=$BackOld\">$H_BACKART</a></p>\n") if ($From > 0);
    } else {
	&cgi'KPrint("<p>$H_TOP<a href=\"$PROGRAM?b=$BOARD&c=l&num=$Num&old=$NextOld\">$H_NEXTART</a></p>\n") if ($Old);
    }

    if (! $#DB_ID == -1) {

	# 空だった……
	&cgi'KPrint("<p>$H_NOARTICLE</p>\n");

    } else {

	if ($SYS_BOTTOMARTICLE) {
	    for ($IdNum = $From; $IdNum <= $To; $IdNum++) {
		$Id = $DB_ID[$IdNum];
		&ViewOriginalArticle($Id, $F_TRUE, $F_TRUE);
		print("<hr>\n");
	    }
	} else {
	    for ($IdNum = $To; $IdNum >= $From; $IdNum--) {
		$Id = $DB_ID[$IdNum];
		&ViewOriginalArticle($Id, $F_TRUE, $F_TRUE);
		print("<hr>\n");
	    }
	}

    }

    if ($SYS_BOTTOMARTICLE) {
	&cgi'KPrint("<p>$H_BOTTOM<a href=\"$PROGRAM?b=$BOARD&c=l&num=$Num&old=$NextOld\">$H_NEXTART</a></p>\n") if ($Old);
    } else {
	&cgi'KPrint("<p>$H_BOTTOM<a href=\"$PROGRAM?b=$BOARD&c=l&num=$Num&old=$BackOld\">$H_BACKART</a></p>\n") if ($From > 0);
    }

    &cgi'KPrint(<<__EOF__);
<form action="$PROGRAM" method="POST">
<input name="b" type="hidden" value="$BOARD">
<input name="c" type="hidden" value="v">
<input name="num" type="hidden" value="$DEF_TITLE_NUM">
<input type="submit" value="$H_BACKTITLE">
</form>
__EOF__

    &MsgFooter;

}


###
## 記事の検索(表示画面作成)
#
sub SearchArticle {

    # キーワード，検索範囲を拾う
    local($Key, $SearchSubject, $SearchPerson, $SearchArticle, $SearchIcon, $Icon) = ($cgi'TAGS{'key'}, $cgi'TAGS{'searchsubject'}, $cgi'TAGS{'searchperson'}, $cgi'TAGS{'searcharticle'}, $cgi'TAGS{'searchicon'}, $cgi'TAGS{'icon'});

    # 表示画面の作成
    &MsgHeader('Message search', "$BOARDNAME: $SEARCHARTICLE_MSG", $TIME);

    # お約束
    &cgi'KPrint(<<__EOF__);
<form action="$PROGRAM\" method="POST">
<input name="c" type="hidden" value="s">
<input name="b" type="hidden" value="$BOARD">
 
$H_INPUTKEYWORD
<input type="submit" value="$H_SEARCHKEYWORD">
<input type="reset" value="$H_RESETKEYWORD">

<p>$H_KEYWORD:
<input name="key" type="text" size="$KEYWORD_LENGTH" value="$Key">
</p>

<p>$H_SEARCHTARGET:
<ul>
__EOF__

    &cgi'KPrint(sprintf("<li><input name=\"searchsubject\" type=\"checkbox\" value=\"on\" %s>: $H_SEARCHTARGETSUBJECT\n", (($SearchSubject) ? 'CHECKED' : '')));
    &cgi'KPrint(sprintf("<li><input name=\"searchperson\" type=\"checkbox\" value=\"on\" %s>: $H_SEARCHTARGETPERSON\n", (($SearchPerson) ? 'CHECKED' : '')));
    &cgi'KPrint(sprintf("<li><input name=\"searcharticle\" type=\"checkbox\" value=\"on\" %s>: $H_SEARCHTARGETARTICLE", (($SearchArticle) ? 'CHECKED' : '')));

    &cgi'KPrint(sprintf("<li><input name=\"searchicon\" type=\"checkbox\" value=\"on\" %s>: $H_ICON // ", (($SearchIcon) ? 'CHECKED' : '')));

    # アイコンの選択
    print("<SELECT NAME=\"icon\">\n");
    &cgi'KPrint(sprintf("<OPTION%s>$H_NOICON\n", (($Icon && ($Icon ne $H_NOICON)) ? '' : ' SELECTED')));
	
    # 一つ一つ表示
    open(ICON, &GetIconPath("$BOARD.$ICONDEF_POSTFIX"))
	|| (open(ICON, &GetIconPath("$DEFAULT_ICONDEF"))
	    || &Fatal($ERR_FILE, &GetIconPath("$DEFAULT_ICONDEF")));
    while(<ICON>) {

	# Version Check
	&VersionCheck('Icon', $1), next if (m/^\# Kb-System-Id: ([^\/]*\/.*)$/o);

	# コメント文はキャンセル
	next if (/^\#/o);
	next if (/^$/o);
	chop;
	($FileName, $IconTitle) = split(/\t/, $_, 3);

	# 表示
	&cgi'KPrint(sprintf("<OPTION%s>$IconTitle\n", (($Icon eq $IconTitle) ? ' SELECTED' : '')));
    }
    close(ICON);
    print("</SELECT>\n");

    # アイコン一覧
    &cgi'KPrint(<<__EOF__);
(<a href="$PROGRAM?b=$BOARD&c=i&type=entry">$H_SEEICON</a>)<BR>
</ul>
</p>
</form>
<hr>
__EOF__

    # キーワードが空でなければ，そのキーワードを含む記事のリストを表示
    if (($SearchIcon ne '') || (($Key ne '') && ($SearchSubject || ($SearchPerson || $SearchArticle)))) {
	&SearchArticleList($Key, $SearchSubject, $SearchPerson, $SearchArticle, $SearchIcon, $Icon);
    }

    &MsgFooter;

}


###
## 記事の検索(検索結果の表示)
#
sub SearchArticleList {

    # キーワード，検索範囲
    local($Key, $Subject, $Person, $Article, $Icon, $IconType) = @_;

    local($dId, $dAids, $dDate, $dTitle, $dIcon, $dName, $dEmail);

    local($HitFlag) = 0;
    local($Line) = ();
    local($SubjectFlag, $PersonFlag, $ArticleFlag);
    local(@KeyList) = split(/ +/, $Key);
    local($Num);

    # リスト開く
    print("<p><ul>\n");

    foreach ($[ .. $#DB_ID) {

	# 記事情報
	$dId = $DB_ID[$_];
	$dIcon = $DB_ICON{$dId};
	$dTitle = $DB_TITLE{$dId};
	$dName = $DB_NAME{$dId};
	$dEmail = $DB_EMAIL{$dId};
	$dAids = $DB_AIDS{$dId};
	$dDate = $DB_DATE{$dId};

	# 変数のリセット
	$SubjectFlag = $PersonFlag = $ArticleFlag = 0;
	$Line = '';

	# URLチェック
	next if (&IsUrl($dId));

	# アイコンチェック
	next if (($Icon ne '') && ($dIcon ne $IconType));

	if ($Key ne '') {

	    # タイトルを検索
	    if (($Subject ne '') && ($dTitle ne '')) {
		$SubjectFlag = 1;
		foreach (@KeyList) {
		    $SubjectFlag = 0 if ($dTitle !~ /$_/i);
		}
	    }

	    # 投稿者名を検索
	    if (($Person ne '') && ($dName ne '')) {
		$PersonFlag = 1;
		foreach (@KeyList) {
		    $PersonFlag = 0 if (($dName !~ /$_/i) && ($dEmail !~ /$_/i));
		}
	    }

	    # 本文を検索
	    if ($Article ne '') {
		$ArticleFlag = 1 if ($Line = &SearchArticleKeyword($dId, @KeyList));
	    }

	} else {

	    # 無条件で一致
	    $SubjectFlag = 1;

	}

	if ($SubjectFlag || $PersonFlag || $ArticleFlag) {

	    # 最低1つは合致した
	    $HitFlag = 1;

	    # 記事へのリンクを表示
	    &cgi'KPrint("<li>" . &GetFormattedTitle($dId, $dAids, $dIcon, $dTitle, $dName, $dDate));

	    # 本文に合致した場合は本文も表示
	    if ($ArticleFlag) {
		$Line =~ s/<[^>]*>//go;
		&cgi'KPrint("<blockquote>$Line</blockquote>\n");
	    }
	}
    }

    # ヒットしなかったら
    &cgi'KPrint("<li>$H_NOTFOUND\n") if ($HitFlag != 1);

    # リスト閉じる
    print("</ul></p>\n");
}


###
## 記事の検索(本文)
#
sub SearchArticleKeyword {

    # IDとキーワード
    local($Id, @KeyList) = @_;
    local(@NewKeyList);
    local($Line, $Return, $Code) = ();

    local($File) = &GetArticleFileName($Id, $BOARD);
    local($ConvFlag) = ($Id !~ /^\d+$/);

    # 検索する
    open(ARTICLE, "<$File") || &Fatal($ERR_FILE, $File);
    while($Line = <ARTICLE>) {

	# Version Check
	&VersionCheck('Article', $1), next if (m/^<!-- Kb-System-Id: ([^\/]*\/.*) -->$/o);

	# コード変換
	if ($ConvFlag) {
	    $Code = &jcode'getcode(*Line);
	    &jcode'convert(*Line, $SCRIPT_KCODE, $Code, "z");
	}

	# クリア
	@NewKeyList = ();

	foreach (@KeyList) {

	    if ($Line =~ /$_/i) {

		# マッチした! 1行目なら覚えとく
		$Return = $Line unless $Return;

	    } else {

		# まだ探さなきゃ……
		push(NewKeyList, $_);

	    }
	}

	# 空なら抜け．
	last unless (@KeyList = @NewKeyList);

    }
    close(ARTICLE);

    # まだ残ってたらアウト．空なら最初のマッチした行を返す．
    return((@KeyList) ? '' : $Return);

}


###
## エイリアスの登録と変更
#
sub AliasNew {

    # 表示画面の作成
    &MsgHeader('Alias entry/edit', $ALIASNEW_MSG, $PROGTIME);

    # 新規登録/登録内容の変更
    &cgi'KPrint(<<__EOF__);
<p>
$H_ALIASTITLE
</p>
<p>
<form action="$PROGRAM" method="POST">
<input name="c" type="hidden" value="am">
$H_ALIAS: <input name="alias" type="text" value="#" size="$NAME_LENGTH"><br>
$H_FROM: <input name="name" type="text" size="$NAME_LENGTH"><br>
$H_MAIL: <input name="email" type="text" size="$MAIL_LENGTH"><br>
$H_URL_S: <input name="url" type="text" value="http://" size="$URL_LENGTH"><br>
$H_ALIASNEWCOM<br>
<input type="submit" value="$H_ALIASNEWPUSH">
</form>
</p>
<hr>
<p>
$H_ALIASDELETE
</p>
<p>
<form action="$PROGRAM" method="POST">
<input name="c" type="hidden" value="ad">
$H_ALIAS: <input name="alias" type="text" size="$NAME_LENGTH"><br>
$H_ALIASDELETECOM<br>
<input type="submit" value="$H_ALIASDELETEPUSH">
</form>
</p>
<hr>
<p>
<form action="$PROGRAM" method="POST">
<input name="c" type="hidden" value="as">
<input type="submit" value="$H_ALIASREFERPUSH">
</form>
</p>
__EOF__
    
    # お約束
    &MsgFooter;

}


###
## 登録/変更
#
sub AliasMod {

    # エイリアス，名前，メイル，URL
    local($A) = $cgi'TAGS{'alias'};
    local($N) = $cgi'TAGS{'name'};
    local($E) = $cgi'TAGS{'email'};
    local($U) = $cgi'TAGS{'url'};
    
    # マシンがマッチしたか
    #	0 ... エイリアスがマッチしない
    #	1 ... エイリアスはマッチしたがマシン名がマッチしない
    #	2 ... マッチしてデータを変更した
    local($HitFlag) = 0;
    local($Alias);

    # 文字列チェック
    &AliasCheck($A, $N, $E, $U);
    
    # エイリアスの読み込み
    &CashAliasData($USER_ALIAS_FILE);
    
    # 1行ずつチェック
    foreach $Alias (sort keys(%Name)) {
	next if ($A ne $Alias);
	
	# マシン名が合ったら2，合わなきゃ1．
	$HitFlag = (($REMOTE_HOST eq $Host{$Alias}) ? 2 : 1);
    }
    
    # マシン名が合わない!
    &Fatal($ERR_CANNOTGRANT, '') if ($HitFlag == 1);

    # 新規登録
    $Alias = $A if ($HitFlag == 0);
    
    # データの登録
    $Name{$Alias} = $N;
    $Email{$Alias} = $E;
    $Host{$Alias} = $REMOTE_HOST;
    $URL{$Alias} = $U;
    
    # エイリアスファイルに書き出し
    &WriteAliasData($USER_ALIAS_FILE);

    # 表示画面の作成
    &MsgHeader('Alias modified', $ALIASMOD_MSG, $TIME);
    &cgi'KPrint("<p>$H_ALIAS: <strong>$A</strong>:\n");
    if ($HitFlag == 2) {
	&cgi'KPrint("$H_ALIASCHANGED</p>\n");
    } else {
	&cgi'KPrint("$H_ALIASENTRIED</p>\n");
    }
    &MsgFooter;
    
}


###
## エイリアスチェック
#
sub AliasCheck {

    local($A, $N, $E, $U) = @_;

    &CheckAlias(*A);
    &CheckName(*N);
    &CheckEmail(*E);
    &CheckURL(*U);
    
}


###
## 削除
#
sub AliasDel {

    # エイリアス
    local($A) = $cgi'TAGS{'alias'};

    # マシンがマッチしたか
    #	0 ... エイリアスがマッチしない
    #	1 ... エイリアスはマッチしたがマシン名がマッチしない
    #	2 ... マッチしてデータを変更した
    local($HitFlag) = 0;
    local($Alias);

    # エイリアスの読み込み
    &CashAliasData($USER_ALIAS_FILE);
    
    # 1行ずつチェック
    foreach $Alias (sort keys(%Name)) {
	next if ($A ne $Alias);
	
	# マシン名が合ったら2，合わなきゃ1．
	$HitFlag = (($REMOTE_HOST eq $Host{$Alias}) ? 2 : 1);
    }
    
    # マシン名が合わない!
    &Fatal($ERR_CANNOTGRANT, '') if ($HitFlag == 1);
    
    # エイリアスがない!
    &Fatal($ERR_UNKNOWNALIAS, $A) if ($HitFlag == 0);
    
    # 名前を消す
    $Name{$A} = '';
    
    # エイリアスファイルに書き出し
    &WriteAliasData($USER_ALIAS_FILE);
    
    # 表示画面の作成
    &MsgHeader('Alias deleted', $ALIASDEL_MSG, $TIME);
    &cgi'KPrint("<p>$H_ALIAS: <strong>$A</strong>: $H_ALIASDELETED</p>\n");
    &MsgFooter;

}


###
## 参照
#
sub AliasShow {

    # エイリアスの読み込み
    &CashAliasData($USER_ALIAS_FILE);
    local($Alias);
    
    # 表示画面の作成
    &MsgHeader('Alias view', $ALIASSHOW_MSG, $TIME);
    # あおり文
    &cgi'KPrint(<<__EOF__);
<p>
$H_AORI_ALIAS
</p><p>
<a href="$PROGRAM?c=an">$H_ALIASTITLE</a>
</p>
__EOF__
    
    # リスト開く
    print("<dl>\n");
    
    # 1つずつ表示
    foreach $Alias (sort keys(%Name)) {
	&cgi'KPrint(<<__EOF__);
<p>
<dt><strong>$Alias</strong>
<dd>$H_FROM: $Name{$Alias}
<dd>$H_MAIL: $Email{$Alias}
<dd>$H_HOST: $Host{$Alias}
<dd>$H_URL: $URL{$Alias}
</p>
__EOF__

    }

    # リスト閉じる
    print("</dl>\n");
    
    &MsgFooter;

}


###
## エイリアスファイルを読み込んで連想配列に放り込む．
## CAUTION: %Name, %Email, %Host, %URLを壊します．
#
sub CashAliasData {

    # ファイル
    local($File) = @_;
    
    local($A, $N, $E, $H, $U);

    # 放り込む．
    open(ALIAS, "<$File") || &Fatal($ERR_FILE, $File);
    while(<ALIAS>) {

	# Version Check
	&VersionCheck('Alias', $1), next
	    if (m/^<!-- Kb-System-Id: ([^\/]*\/.*) -->$/o);

	next if (/^$/o);
	chop;

	($A, $N, $E, $H, $U) = split(/\t/, $_);

	$Name{$A} = $N;
	$Email{$A} = $E;
	$Host{$A} = $H;
	$URL{$A} = $U;
    }
    close(ALIAS);

}


###
## エイリアスファイルにデータを書き出す．
## CAUTION: %Name, %Email, %Host, %URLを必要とします．
##          $Nameが空だと書き込まない．
#
sub WriteAliasData {

    # ファイル
    local($File) = @_;
    local($Alias);
    local($TmpFile) = $USER_ALIAS_TMP_FILE;

    # 書き出す
    open(ALIAS, ">$TmpFile") || &Fatal($ERR_FILE, $TmpFile);

    # バージョン情報を書き出す
    printf(ALIAS "<!-- Kb-System-Id: %s/%s -->\n", $KB_VERSION, $KB_RELEASE);

    # 順に．
    foreach $Alias (sort keys(%Name)) {
	($Name{$Alias}) && printf(ALIAS "%s\t%s\t%s\t%s\t%s\n", $Alias, $Name{$Alias}, $Email{$Alias}, $Host{$Alias}, $URL{$Alias});
    }
    close(ALIAS);

    # 更新
    rename($TmpFile, $File);
    
}


###
## 掲示板のヘッダを表示する
#
sub BoardHeader {

    local($File) = &GetPath($BOARD, $BOARD_FILE_NAME);

    open(HEADER, "<$File") || &Fatal($ERR_FILE, $File);
    while(<HEADER>){
	# Version Check
	&VersionCheck('Header', $1), next if (m/^<!-- Kb-System-Id: ([^\/]*\/.*) -->$/o);
	# 表示する
	&cgi'KPrint("$_");
    }
    close(HEADER);

}


###
## 新しい記事番号を返す
#
sub GetNewArticleId {

    # 記事番号を収めるファイル
    local($ArticleNumFile) = &GetPath($BOARD, $ARTICLE_NUM_FILE_NAME);

    # 記事番号
    local($ArticleId);

    open(AID, "<$ArticleNumFile") || &Fatal($ERR_FILE, $ArticleNumFile);
    while(<AID>) {
	chop;
	$ArticleId = $_;
    }
    close(AID);

    # 1増やして返す
    return($ArticleId + 1);

}


###
## 記事番号を取ってくる(番号は増えない)．
#
sub GetArticleId {

    # ファイル名を取得
    local($ArticleNumFile) = @_;

    # 記事番号
    local($ArticleId);

    open(AID, "<$ArticleNumFile") || &Fatal($ERR_FILE, $ArticleNumFile);
    while(<AID>) {
	chop;
	$ArticleId = $_;
    }
    close(AID);

    # 記事番号を返す．
    return($ArticleId);
}


###
## ボードエイリアスからボードエイリアス名を取ってくる．
#
sub GetBoardInfo {

    # エイリアス名
    local($Alias) = @_;

    # ボード名
    local($BoardName) = ();

    open(ALIAS, "<$BOARD_ALIAS_FILE") || &Fatal($ERR_FILE, $BOARD_ALIAS_FILE);
    while(<ALIAS>) {

	# Version Check
	&VersionCheck('Board', $1), next if (m/^\# Kb-System-Id: ([^\/]*\/.*)$/o);

	next if (/^\#/o);
	next if (/^$/o);
	chop;
	next unless (/^$Alias\t(.*)$/);
	$BoardName = $1;
    }
    close(ALIAS);

    return($BoardName);

}


###
## タイトルリストのフォーマット
#
sub GetFormattedTitle {

    local($Id, $Aids, $Icon, $Title, $Name, $Date) = @_;
    local($String, $Fnum) = ('', 0);
    local($InputDate) = &GetDateTimeFormatFromUtc(($Date || &GetModifiedTime($Id)));
    local($IdStr, $Link, $Thread);

    # タイトルがついてなかったら，Idをそのままタイトルにする．
    $Title = $Title || $Id;

    # 通常記事
    $IdStr = "<strong>$Id.</strong> ";
    $Link = "<a href=\"$PROGRAM?b=$BOARD&c=e&id=$Id\">$Title</a>";
    $Thread = (($Aids) ? " <a href=\"$PROGRAM?b=$BOARD&c=t&id=$Id\">$H_THREAD</a>" : '');

    if (($Icon eq $H_NOICON) || ($Icon eq '')) {
	$String = sprintf("$IdStr$Link$Thread [%s] $InputDate", ($Name || $MAINT_NAME));
    } else {
	$String = sprintf("$IdStr<img src=\"%s\" alt=\"$Icon \" width=\"$ICON_WIDTH\" height=\"$ICON_HEIGHT\">$Link$Thread [%s] $InputDate", &GetIconURLFromTitle($Icon), ($Name || $MAINT_NAME));
    }

    return($String);

}


###
## 元記事情報の表示
#
sub ShowLinksToFollowedArticle {

    local(@IdList) = @_;

    local($Id);
    local($Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name);

    # オリジナル記事
    if ($#IdList > 0) {
	$Id = @IdList[$#IdList];
	($Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name) = &GetArticlesInfo($Id);
	&cgi'KPrint("<br>\n<strong>$H_ORIG_TOP:</strong> " . &GetFormattedTitle($Id, $Aids, $Icon, $Subject, $Name, $Date));
    }

    # 元記事
    $Id = @IdList[0];
    ($Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name) = &GetArticlesInfo($Id);
    &cgi'KPrint("<br>\n<strong>$H_ORIG:</strong> " . &GetFormattedTitle($Id, $Aids, $Icon, $Subject, $Name, $Date));

}


###
## 文字列チェック: エイリアス
#
sub CheckAlias {

    local(*String) = @_;

    # 空チェック
    (! $String) && &Fatal($ERR_NOTFILLED, '');

    # `#'で始まってる?
    ($String =~ (/^\#/)) || &Fatal($ERR_ILLEGALSTRING, $H_ALIAS);

    # 1文字じゃだめ
    (length($String) > 1) || &Fatal($ERR_ILLEGALSTRING, $H_ALIAS);

}


###
## 文字列チェック: タイトル
#
sub CheckSubject {

    local(*String) = @_;

    # 空チェック
    (! $String) && &Fatal($ERR_NOTFILLED, '');

    # タグをチェック
    &Fatal($ERR_TAGCRINDATA, '') if ($String =~ m/[<>\t\n]/o);

}


###
## 文字列チェック: 名前
#
sub CheckName {

    local(*String) = @_;

    # 空チェック
    (! $String) && &Fatal($ERR_NOTFILLED, '');

    # 改行コードをチェック
    ($String =~ /[\t\n]/o) && &Fatal($ERR_CRINDATA, '');

}


###
## 文字列チェック: メイル
#
sub CheckEmail {

    local(*String) = @_;

    if ($SYS_POSTERMAIL) {

	# 空チェック
	&Fatal($ERR_NOTFILLED, '') if ($String eq '');

	# `@'が入ってなきゃアウト
	&Fatal($ERR_ILLEGALSTRING, 'E-Mail') if ($String !~ (/@/));

    }

    # 改行コードをチェック
    ($String =~ /[\t\n]/o) && &Fatal($ERR_CRINDATA, '');

}


###
## 文字列チェック: URL
#
sub CheckURL {

    local(*String) = @_;

    # http://だけの場合は空にしてしまう．
    $String = '' if ($String =~ m!^http://$!oi);

    # 定義されたscheme + '://'で始まるかどうかだけ，チェックする．甘い?
    ($String ne '') && (! &IsUrl($String)) && &Fatal($ERR_ILLEGALSTRING, 'URL');

}


###
## URLか?
#
sub IsUrl {

    local($String) = @_;
    local($Scheme);
    local($IsUrl) = 0;
    foreach $Scheme (@URL_SCHEME) {
	$IsUrl = 1 if ($String =~ m!^$Scheme://!i);
    }

    return($IsUrl);

}


###
## 記事のヘッダの表示
#
sub MsgHeader {

    # message and board
    local($Title, $Message, $LastModified) = @_;
    
    &cgi'header($LastModified);
    &cgi'KPrint(<<__EOF__);
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML i18n//EN">
<html>
<head>
<title>$Title</title>
<base href="http://$SERVER_NAME:$SERVER_PORT$SYSDIR_NAME">
</head>
__EOF__

    print("<body");
    if ($SYS_NETSCAPE_EXTENSION) {
	print(" background=\"$BG_IMG\"") if $BG_IMG;
	print(" bgcolor=\"$BG_COLOR\"") if $BG_COLOR;
	print(" TEXT=\"$TEXT_COLOR\"") if $TEXT_COLOR;
	print(" LINK=\"$LINK_COLOR\"") if $LINK_COLOR;
	print(" ALINK=\"$ALINK_COLOR\"") if $ALINK_COLOR;
	print(" VLINK=\"$VLINK_COLOR\"") if $VLINK_COLOR;
    }
    print(">\n");

    &cgi'KPrint(<<__EOF__);
<h1>$Message</h1>
<hr>
__EOF__

}


###
## 記事のフッタの表示
#
sub MsgFooter {

    &cgi'KPrint(<<__EOF__);
<hr>
<address>
$ADDRESS
</address>
</body>
</html>
__EOF__

}


###
## ロック関係
#

# ロック
sub lock {
    &lock_UNIX if ($ARCH eq 'UNIX');
    &lock_WinNT if ($ARCH eq 'WinNT');
    &lock_Win95 if ($ARCH eq 'Win95');
    &lock_Mac if ($ARCH eq 'Mac');
}

# アンロック
sub unlock {
    &unlock_UNIX if ($ARCH eq 'UNIX');
    &unlock_WinNT if ($ARCH eq 'WinNT');
    &unlock_Win95 if ($ARCH eq 'Win95');
    &unlock_Mac if ($ARCH eq 'Mac');
}

# UNIX + Perl4/5
sub lock_UNIX {
    local($TimeOut) = 0;
    local($Flag) = 0;
    srand($TIME|$$);
    open(LOCKORG, ">$LOCK_ORG") || &Fatal($ERR_FILE, $LOCK_ORG);
    close(LOCKORG);
    for($TimeOut = 0; $TimeOut < $LOCK_WAIT; $TimeOut++) {
	$Flag = 1, last if link($LOCK_ORG, $LOCK_FILE);
	select(undef, undef, undef, (rand(6)+5)/10);
    }
    unlink($LOCK_ORG);
    &Fatal($ERR_F_CANNOTLOCK, $TimeOut) unless ($Flag);
}

sub unlock_UNIX {
    unlink($LOCK_FILE);
}

# WinNT + Perl5(use flock)
sub lock_WinNT {
    local($LockEx, $LockUn) = (2, 8);
    open(LOCK, "$LOCK_FILE") || &Fatal($ERR_FILE, $LOCK_FILE);
    flock(LOCK, $LockEx);
}
sub unlock_WinNT {
    local($LockEx, $LockUn) = (2, 8);
    flock(LOCK, $LockUn);
    close(LOCK);
}

# Win95 + Perl5
sub lock_Win95 {
    # how can i lock a Win95?
    # somebody please solve this problem...
}

sub unlock_Win95 {
}

# Mac + MacPerl
sub lock_Mac {
    # how can i lock a Mac?
    # i don't know MacPerl well...
    # somebody please solve this problem...
}

sub unlock_Mac {
}


###
## 元記事の表示
#
sub ViewOriginalArticle {

    # Id，コマンドを表示するか否か，元記事を表示するか否か
    local($Id, $CommandFlag, $OriginalFlag) = @_;

    # 引用するファイル
    local($QuoteFile) = &GetArticleFileName($Id, $BOARD);

    # 記事情報の取得
    local($Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url) = &GetArticlesInfo($Id);

    # コマンド表示?
    if (($CommandFlag == $F_TRUE) && $SYS_COMMAND) {

	&cgi'KPrint(<<__EOF__);
<p>
<a href="$PROGRAM?b=$BOARD&c=v&num=$DEF_TITLE_NUM"><img src="$ICON_TLIST" alt="$H_BACKTITLE" width="$ICON_WIDTH" height="$ICON_HEIGHT" BORDER="0"></a>
<a href="$PROGRAM?b=$BOARD&c=en&id=$Id"><img src="$ICON_NEXT" alt="$H_NEXTARTICLE" width="$ICON_WIDTH" height="$ICON_HEIGHT" BORDER="0"></a>
<a href="$PROGRAM?b=$BOARD&c=f&id=$Id"><img src="$ICON_FOLLOW" alt="$H_REPLYTHISARTICLE" width="$ICON_WIDTH" height="$ICON_HEIGHT" BORDER="0"></a>
<a href="$PROGRAM?b=$BOARD&c=q&id=$Id"><img src="$ICON_QUOTE" alt="$H_REPLYTHISARTICLEQUOTE" width="$ICON_WIDTH" height="$ICON_HEIGHT" BORDER="0"></a>
__EOF__
	if ($Aids ne '') {
	    &cgi'KPrint("<a href=\"$PROGRAM?b=$BOARD&c=t&id=$Id\"><img src=\"$ICON_THREAD\" alt=\"$H_READREPLYALL\" width=\"$ICON_WIDTH\" height=\"$ICON_HEIGHT\" BORDER=\"0\"></a>");
	} else {
	    &cgi'KPrint("<img src=\"$ICON_THREAD\" alt=\"$H_READREPLYALL\" width=\"$ICON_WIDTH\" height=\"$ICON_HEIGHT\" BORDER=\"0\">");
	}
	&cgi'KPrint("<a href=\"$PROGRAM?b=$BOARD&c=i&type=article\"><img src=\"$ICON_HELP\" alt=\"?\" width=\"$ICON_WIDTH\" height=\"$ICON_HEIGHT\" BORDER=\"0\"></a>\n</p>\n");

    }

    print("<p>\n");

    # ボード名と記事番号，題
    if (($Icon eq $H_NOICON) || ($Icon eq '')) {
	&cgi'KPrint("<strong>$H_SUBJECT</strong>: <strong>$Id .</strong> $Subject");
    } else {
	&cgi'KPrint(sprintf("<strong>$H_SUBJECT</strong>: <strong>$Id .</strong> <img src=\"%s\" alt=\"$Icon \" width=\"$ICON_WIDTH\" height=\"$ICON_HEIGHT\">$Subject", &GetIconURLFromTitle($Icon)));
    }

    # お名前
    if (($Url eq '') || ($Url eq 'http://')) {
	# 「http://だったら」というのは旧バージョンへの対処．そのうち削除する予定．
        # URLがない場合
        &cgi'KPrint("<br>\n<strong>$H_FROM</strong>: $Name");
    } else {
        # URLがある場合
        &cgi'KPrint("<br>\n<strong>$H_FROM</strong>: <a href=\"$Url\">$Name</a>");
    }

    # メイル
    &cgi'KPrint(" <a href=\"mailto:$Email\">&lt;$Email&gt;</a>") if ($Email ne '');

    # マシン
    &cgi'KPrint("<br>\n<strong>$H_HOST</strong>: $RemoteHost") if $SYS_SHOWHOST;

    # 投稿日
    local($InputDate) = &GetDateTimeFormatFromUtc($Date);
    &cgi'KPrint("<br>\n<strong>$H_DATE</strong>: $InputDate");

    # 反応元(引用の場合)
    &ShowLinksToFollowedArticle(split(/,/, $Fid)) if (($OriginalFlag == $F_TRUE) && ($Fid ne ''));

    # 切れ目
    &cgi'KPrint("</p>\n$H_LINE<br>\n");

    # 記事の中身
    open(TMP, "<$QuoteFile") || &Fatal($ERR_FILE, $QuoteFile);
    while(<TMP>) {

	# Version Check
	&VersionCheck('Article', $1), next if (m/^<!-- Kb-System-Id: ([^\/]*\/.*) -->$/o);

	# 表示
	&cgi'KPrint("$_");

    }
    close(TMP);

}


###
## ボード名称とIdからファイルのパス名を作り出す．
#
sub GetArticleFileName {

    # IdとBoard
    local($Id, $Board) = @_;

    # Boardが空ならBoardディレクトリ内から相対，
    # 空でなければシステムから相対
    return(($Board) ? "$Board/$Id" : "$Id") if ($ARCH eq 'UNIX');
    return(($Board) ? "$Board/$Id" : "$Id") if ($ARCH eq 'WinNT');
    return(($Board) ? "$Board/$Id" : "$Id") if ($ARCH eq 'Win95');
    return(($Board) ? ":$Board:$Id" : "$Id") if ($ARCH eq 'Mac');

}


###
## ボード名称とファイル名から，そのファイルのパス名を作り出す．
#
sub GetPath {

    # BoardとFile
    local($Board, $File) = @_;

    # 返す
    return("$Board/$File") if ($ARCH eq 'UNIX');
    return("$Board/$File") if ($ARCH eq 'WinNT');
    return("$Board/$File") if ($ARCH eq 'Win95');
    return(":$Board:$File") if ($ARCH eq 'Mac');

}


###
## アイコンファイル名から，そのファイルのパス名を作り出す．
#
sub GetIconPath {

    # BoardとFile
    local($File) = @_;

    # 返す
    return("$ICON_DIR/$File") if ($ARCH eq 'UNIX');
    return("$ICON_DIR/$File") if ($ARCH eq 'WinNT');
    return("$ICON_DIR/$File") if ($ARCH eq 'Win95');
    return(":$ICON_DIR:$File") if ($ARCH eq 'Mac');

}


###
## アイコンファイル名から，そのファイルのURL名を作り出す．
#
sub GetIconURL {

    # BoardとFile
    local($File) = @_;

    # 返す
    return("$ICON_DIR/$File");

}


###
## アイコン名から，アイコンのURLを取得
#
sub GetIconURLFromTitle {

    # アイコン名
    local($Icon) = @_;

    local($FileName, $Title, $TargetFile) = ();

    # 一つ一つ表示
    open(ICON, &GetIconPath("$BOARD.$ICONDEF_POSTFIX"))
	|| (open(ICON, &GetIconPath("$DEFAULT_ICONDEF"))
	    || &Fatal($ERR_FILE, &GetIconPath("$DEFAULT_ICONDEF")));
    while(<ICON>) {

	# Version Check
	&VersionCheck('Icon', $1), next if (m/^\# Kb-System-Id: ([^\/]*\/.*)$/o);

	# コメント文はキャンセル
	next if (/^\#/o);
	next if (/^$/o);
	chop;
	($FileName, $Title) = split(/\t/, $_, 3);
	$TargetFile = $FileName if ($Title eq $Icon);
    }
    close(ICON);

    return(($TargetFile) ? &GetIconURL($TargetFile) : '');

}


###
## ある記事の情報を取り出す．
#
sub GetArticlesInfo {

    # 対象記事のID
    local($Id) = @_;

    return($DB_FID{$Id}, $DB_AIDS{$Id}, $DB_DATE{$Id}, $DB_TITLE{$Id}, $DB_ICON{$Id}, $DB_REMOTEHOST{$Id}, $DB_NAME{$Id}, $DB_EMAIL{$Id}, $DB_URL{$Id}, $DB_FMAIL{$Id});

}


###
## あるIDの記事から，最終更新UTCを取ってくる
#
sub GetModifiedTime {
    local($Id) = @_;
    return($TIME - (-M &GetArticleFileName($Id, $BOARD)) * $SECINDAY);
}


###
## UTCから，時間を表す文字列を取り出す
## 古いバージョンでは，DB中に時刻を表す文字列(not UTC)がそのまま入っている．
#
sub GetDateTimeFormatFromUtc {

    local($Utc) = @_;

    # 古い時代のものらしい．
    return($Utc) if ($Utc !~ m/^\d+$/);

    # 変換
    local($Sec, $Min, $Hour, $Mday, $Mon, $Year, $Wday, $Yday, $Isdst) = localtime($Utc);
    return(sprintf("%d/%d(%02d:%02d)", $Mon + 1, $Mday, $Hour, $Min));

}


###
## UTCを取り出す
## 古いバージョンでは，DB中に時刻を表す文字列(not UTC)がそのまま入っている．
#
sub GetUtcFromOldDateTimeFormat {

    local($Time) = @_;

    # 新規らしい
    return($Time) if ($Time =~ m/^\d+$/);

    # 適当
    return(854477921);

}


###
## Version Check
#
sub VersionCheck {

    local($FileType, $VersionString) = @_;

    local($VersionId, $ReleaseId) = split(/\//, $VersionString);

    # no check now...

}


###
## エラー表示
#
sub Fatal {

    # エラー番号とエラー情報の取得
    local($FatalNo, $FatalInfo) = @_;

    # エラーメッセージ
    local($ErrString);

    if ($FatalNo == $ERR_FILE) {

	$ErrString = "File: $FatalInfoが存在しない，あるいはpermissionの設定が間違っています．お手数ですが，<a href=\"mailto:$MAINT\">$MAINT</a>まで，上記ファイル名をお知らせ下さい．";

    } elsif ($FatalNo == $ERR_NOTFILLED) {

	$ErrString = "入力されていない項目があります．戻ってもう一度やり直してみてください．";

    } elsif ($FatalNo == $ERR_CRINDATA) {

	$ErrString = "題や名前，メイルアドレスに，タブ文字か改行が入ってしまっています．戻ってもう一度やり直してみてください．";

    } elsif ($FatalNo == $ERR_TAGCRINDATA) {

	$ErrString = "題中にHTMLタグ，タブ文字，改行文字を入れることは禁じられています．戻って違う題に書き換えてください．";

    } elsif ($FatalNo == $ERR_CANNOTGRANT) {

	$ErrString = "登録されているエイリアスのものと，マシン名が一致しません．お手数ですが，<a href=\"mailto:$MAINT\">$MAINT</a>まで御連絡ください．";

    } elsif ($FatalNo == $ERR_UNKNOWNALIAS) {

	$ErrString = "$FatalInfoというエイリアスは，登録されていません．";

    } elsif ($FatalNo == $ERR_ILLEGALSTRING) {

	$ErrString = "$FatalInfoがおかしくありませんか? 戻ってもう一度やり直してみてください．";

    } elsif ($FatalNo == $ERR_NONEXTARTICLE) {

	$ErrString = "次の記事はまだ投稿されていません．";

    } elsif ($FatalNo == $ERR_CANNOTSENDMAIL) {

	$ErrString = "メイルが送信できませんでした．お手数ですが，このエラーが生じた状況を，<a href=\"mailto:$MAINT\">$MAINT</a>までお知らせください．";

    } elsif ($FatalNo == $ERR_F_CANNOTLOCK) {

	$ErrString ="システムのロックに失敗しました．混み合っているようですので，数分待ってからもう一度アクセスしてください．何度アクセスしてもロックされている場合，メンテナンス中である可能性もあります．";

    } else {

	$ErrString = "エラー番号不定: $FatalInfo<br>お手数ですが，このエラーが生じた状況を，<a href=\"mailto:$mEmail\">$mEmail</a>までお知らせください．";

    }

    # 異常終了の可能性があるので，とりあえずlockを外す
    # (ロックの失敗の時以外)
    &unlock if ($FatalNo != $ERR_F_CANNOTLOCK);

    # 表示画面の作成
    &MsgHeader('Error!', $ERROR_MSG, $TIME);

    &cgi'KPrint("<p>$ErrString</p>\n");

    if ($BOARD ne '') {
	&cgi'KPrint(<<__EOF__);
<form action="$PROGRAM" method="POST">
<input name="b" type="hidden" value="$BOARD">
<input name="c" type="hidden" value="v">
<input name="num" type="hidden" value="$DEF_TITLE_NUM">
<input type="submit" value="$H_BACKTITLE">
</form>
__EOF__
    }

    &MsgFooter;
    exit(0);
}
