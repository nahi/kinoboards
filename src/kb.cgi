#!/usr/local/bin/GNU/perl
#
# $Id: kb.cgi,v 5.0 1997-07-03 09:58:00 nakahiro Exp $


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


# This file implements main functions of KINOBOARDS.


# 環境変数を拾う
$TIME = time;			# プログラム起動時間(UTC)
$SERVER_NAME = $ENV{'SERVER_NAME'};
$SERVER_PORT = $ENV{'SERVER_PORT'};
$REMOTE_HOST = $ENV{'REMOTE_HOST'};
$SCRIPT_NAME = $ENV{'SCRIPT_NAME'};
$PATH_INFO = $ENV{'PATH_INFO'};
$PATH_TRANSLATED = $ENV{'PATH_TRANSLATED'};

# 大域変数の定義
$[ = 0;				# zero origined
$| = 1;				# pipe flushed
($CGIPROG_NAME = $SCRIPT_NAME) =~ s!^(.*/)!!o;
$SYSDIR_NAME = (($PATH_INFO) ? "$PATH_INFO/" : "$1");
$HEADER_FILE = ($CGIPROG_NAME =~ m/^(.*)\..*$/o) ? "$1.ph" : 'kb.ph';
$SCRIPT_URL = "http://$SERVER_NAME$SERVER_PORT_STRING$SCRIPT_NAME$PATH_INFO";
$PROGRAM = (($PATH_INFO) ? "$SCRIPT_NAME$PATH_INFO" : "$CGIPROG_NAME");
$SERVER_PORT_STRING = '';
$KB_VERSION = '1.0';
$KB_RELEASE = '4.1pre';

# ディレクトリ
$ICON_DIR = 'icons';				# アイコンディレクトリ
# ファイル
$BOARD_ALIAS_FILE = 'kinoboards';		# 掲示板DB
$CONF_FILE_NAME = '.kbconf';			# 掲示板別configuratinファイル
$ARRIVEMAIL_FILE_NAME = '.kbmail';		# 掲示板別新規メイル送信先DB
$BOARD_FILE_NAME = '.board';			# タイトルリストヘッダDB
$DB_FILE_NAME = '.db';				# 記事DB
$ARTICLE_NUM_FILE_NAME = '.articleid';		# 記事番号DB
$USER_ALIAS_FILE = 'kinousers';			# ユーザDB
$DEFAULT_ICONDEF = 'all.idef';			# アイコンDB
$LOCK_FILE = '.lock.kb';			# ロックファイル
# Suffix
$TMPFILE_SUFFIX = 'tmp';			# DBテンポラリファイルのSuffix
$ICONDEF_POSTFIX = 'idef';			# アイコンDBファイルのSuffix

# アイコンファイル相対URL
$ICON_BLIST = "$ICON_DIR/blist.gif";		# 掲示板一覧へ
$ICON_TLIST = "$ICON_DIR/tlist.gif";		# タイトル一覧へ
$ICON_PREV = "$ICON_DIR/prev.gif";		# 前の記事へ
$ICON_NEXT = "$ICON_DIR/next.gif";		# 次の記事へ
$ICON_WRITENEW = "$ICON_DIR/writenew.gif";	# 新規書き込み
$ICON_FOLLOW = "$ICON_DIR/follow.gif";		# リプライ
$ICON_QUOTE = "$ICON_DIR/quote.gif";		# 引用してリプライ
$ICON_THREAD = "$ICON_DIR/thread.gif";		# まとめ読み
$ICON_HELP = "$ICON_DIR/help.gif";		# ヘルプ
$ICON_DELETE = "$ICON_DIR/delete.gif";		# 削除
$ICON_SUPERSEDE = "$ICON_DIR/supersede.gif";	# 訂正

# インクルードファイルの読み込み
if ($PATH_INFO && (-s "$HEADER_FILE")) { require($HEADER_FILE); }
if ($PATH_TRANSLATED ne '') { chdir($PATH_TRANSLATED); }
if (-s "$HEADER_FILE") {
    require($HEADER_FILE);
} else {
    die("cannot find configuration file: `$HEADER_FILE'");
}
require('cgi.pl');
require('jcode.pl');

# インクルードファイルの設定に応じた大域変数の設定
$SYS_F_MT = ($SYS_F_D || $SYS_F_AM || $SYS_F_LI || $SYS_F_MV);
if (($SERVER_PORT != 80) && ($SYS_PORTNO == 1)) {
    $SERVER_PORT_STRING = ":$SERVER_PORT";
}
if ($TIME_ZONE) { $ENV{'TZ'} = $TIME_ZONE; }
if ($BOARDLIST_URL eq '-') { $BOARDLIST_URL = "$PROGRAM?c=bl"; }
$ADDRESS = sprintf("Maintenance: <a href=\"mailto:%s\">%s</a><br><a href=\"http://www.kinotrope.co.jp/~nakahiro/kb10.shtml\">KINOBOARDS/%s R%s</a>: Copyright (C) 1995, 96, 97 <a href=\"http://www.kinotrope.co.jp/~nakahiro/\">NAKAMURA Hiroshi</a>.", $MAINT, $MAINT_NAME, $KB_VERSION, $KB_RELEASE);

# シグナルハンドラ
$SIG{'HUP'} = $SIG{'INT'} = $SIG{'QUIT'} = $SIG{'TERM'} = $SIG{'TSTP'} = 'DoKill';
sub DoKill { &cgi'unlock($LOCK_FILE); exit(1); }


######################################################################


###
## MAIN - メインブロック
#
# - SYNOPSIS
#	kb.cgi
#
# - ARGS
#	なし
#
# - DESCRIPTION
#	起動時に一度だけ参照される．
#	引き数はないが，環境変数QUERY_STRINGとREQUEST_METHOD，
#	もしくは標準入力経由で値を渡さないと，正しく動作しない．
#
# - RETURN
#	なし
#
&cgi'lock($LOCK_FILE) || &Fatal(999, '');

MAIN: {

    local($BoardConfFile, $Command, $Com);

    # 標準入力(POST)または環境変数(GET)のデコード．
    &cgi'Decode;

    # 頻繁に使うので大域変数を使う(汚ない)
    $BOARDNAME = &GetBoardInfo($BOARD = $cgi'TAGS{'b'});
    # 一応，ね．
    if ($BOARDNAME =~ m!/!o) { &Fatal(11, $BOARDNAME); }

    # 掲示板固有セッティングを読み込む
    $BoardConfFile = &GetPath($BOARD, $CONF_FILE_NAME);
    if (-s "$BoardConfFile") { require("$BoardConfFile"); }

    # DBを大域変数にキャッシュ
    if ($BOARD) { &DbCash($BOARD); }

    # 値の抽出
    $Command = $cgi'TAGS{'c'};
    $Com = $cgi'TAGS{'com'};

    # コマンドタイプによる分岐
    &ShowArticle,	last if ($SYS_F_E  && ($Command eq 'e'));
    &ThreadArticle,	last if ($SYS_F_T  && ($Command eq 't'));
    &Entry(0),		last if ($SYS_F_N  && ($Command eq 'n'));
    &Entry(1),		last if ($SYS_F_FQ && ($Command eq 'f'));
    &Entry(2),		last if ($SYS_F_FQ && ($Command eq 'q'));
    &Preview,		last if (($SYS_F_N || $SYS_F_FQ) && ($Command eq 'p') && ($Com ne 'x'));
    &Thanks,		last if (($SYS_F_N || $SYS_F_FQ) && ($Command eq 'x'));
    &Thanks,		last if (($SYS_F_N || $SYS_F_FQ) && ($Command eq 'p') && ($Com eq 'x'));
    &ViewTitle,		last if ($SYS_F_V  && ($Command eq 'v'));
    &SortArticle,	last if ($SYS_F_R  && ($Command eq 'r'));
    &NewArticle,	last if ($SYS_F_L  && ($Command eq 'l'));
    &SearchArticle,	last if ($SYS_F_S  && ($Command eq 's'));
    &ShowIcon,		last if ($Command eq 'i');
    &AliasNew,		last if ($SYS_ALIAS && ($Command eq 'an'));
    &AliasMod,		last if ($SYS_ALIAS && ($Command eq 'am'));
    &AliasDel,		last if ($SYS_ALIAS && ($Command eq 'ad'));
    &AliasShow,		last if ($SYS_ALIAS && ($Command eq 'as'));

    # 以下は管理用
    &ViewTitle('maint'),	last if ($SYS_F_MT && ($Command eq 'vm'));
    &DeletePreview,	last if ($SYS_F_D  && ($Command eq 'dp'));
    &DeleteExec(0),	last if ($SYS_F_D  && ($Command eq 'de'));
    &DeleteExec(1),	last if ($SYS_F_D  && ($Command eq 'det'));
    &ArriveMailEntry,   last if ($SYS_F_AM && ($Command eq 'mp'));
    &ArriveMailExec,    last if ($SYS_F_AM && ($Command eq 'me'));
    &ViewTitle('linkto'),	last if ($SYS_F_LI && ($Command eq 'ct'));
    &ViewTitle('linkexec'),	last if ($SYS_F_LI && ($Command eq 'ce'));
    &ViewTitle('moveto'),	last if ($SYS_F_MV && ($Command eq 'mvt'));
    &ViewTitle('moveexec'),	last if ($SYS_F_MV && ($Command eq 'mve'));

    # デフォルト
    &BoardList,		last if ($SYS_F_B  && ($Command eq 'bl'));

    if ($Command ne '') {
	&Fatal(99, '');
    } else {
	print("huh... what's up? running under any shell?\n");
    }

}


&cgi'unlock($LOCK_FILE);
exit(0);


######################################################################
# ユーザインタフェイスインプリメンテーション(個別)
#
# 使わない機能に対応する関数は，取り払っても動く……はずです
# (が，テストはしてません ^_^;)．


###
## BoardList - 掲示板一覧の表示
#
# - SYNOPSIS
#	BoardList;
#
# - ARGS
#	なし
#
# - DESCRIPTION
#	掲示板一覧を表示する．
#
# - RETURN
#	なし
#
sub BoardList {

    local(%BoardList, %BoardInfo, $Key, $Value, $ModTime, $NumOfArticle);

    # 全掲示板の情報を取り出す
    &getAllBoardInfo(*BoardList, *BoardInfo);

    &MsgHeader("Board List", "$SYSTEM_NAME");

    &cgiprint'Cache(<<__EOF__);
<p>
<a href="http://www.kinotrope.co.jp/~nakahiro/kb10.shtml">KINOBOARDS/1.0</a>
で運営されているシステムです．
</p><p>
$SYSTEM_NAMEでは，現在，以下の$H_BOARDが用意されています．
</p>
__EOF__

    &cgiprint'Cache("<dl>\n");
    while(($Key, $Value) = each(%BoardList)) {
	$ModTime = &GetDateTimeFormatFromUtc(&GetModifiedTime($DB_FILE_NAME, $Key));
	$NumOfArticle = &getArticleId($Key);
	&cgiprint'Cache("<p>\n<dt><a href=\"$PROGRAM?b=$Key&c=v&num=$DEF_TITLE_NUM\">$Value</a>\n");
	&cgiprint'Cache("[最新: $ModTime, 記事数: $NumOfArticle]\n");
	&cgiprint'Cache("<dd>$BoardInfo{$Key}\n</p>\n");
    }

    &cgiprint'Cache("</dl>\n</p>\n");

    &MsgFooter;

}


###
## Entry - 書き込み画面の表示
#
# - SYNOPSIS
#	Entry($QuoteFlag);
#
# - ARGS
#	$QuoteFlag	0 ... 新着
#			1 ... 引用なしのリプライ
#			2 ... 引用ありのリプライ
#
# - DESCRIPTION
#	書き込み画面を表示する
#	大域変数である，CGI変数を参照する．
#
# - RETURN
#	なし
#
sub Entry {
    local($QuoteFlag) = @_;
    local($Id, $Supersede, $IconTitle, $Key, $Value, $Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail, $DefSubject, $DefName, $DefEmail, $DefUrl, $DefFmail);

    $Id = $cgi'TAGS{'id'};
    $Supersede = $cgi'TAGS{'s'}; # 訂正?
    if ($QuoteFlag != 0) {
	($Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail) = &GetArticlesInfo($Id);
    }
    $Icon = $Icon || $H_NOICON;
    $DefSubject = ($Supersede ? $Subject : (($QuoteFlag == 0) ? '' : &GetReplySubject($Id)));
    $DefName = ($Supersede ? $Name : '');
    $DefEmail = ($Supersede ? $Email : '');
    $DefUrl = ($Supersede ? $Url : 'http://');
    $DefFmail = ($Supersede ? $Fmail : '');

    # 表示画面の作成
    if ($Supersede && $SYS_F_SS) {
	&MsgHeader('Supersede entry', "$BOARDNAME: $H_MESGの訂正");
    } else {
	&MsgHeader('Message entry', "$BOARDNAME: $H_MESGの書き込み");
    }

    # フォローの場合
    if ($QuoteFlag != 0) {
	# 記事の表示(コマンド無し, 元記事あり)
	&ViewOriginalArticle($Id, 0, 1);
	if ($Supersede && $SYS_F_SS) {
	    &cgiprint'Cache("<hr>\n<h2>上の$H_MESGを訂正する</h2>");
	} else {
	    &cgiprint'Cache("<hr>\n<h2>上の$H_MESGへの$H_REPLYを書き込む</h2>");
	}
    }

    # お約束
    &cgiprint'Cache(<<__EOF__);
<form action="$PROGRAM" method="POST">
<input name="c" type="hidden" value="p">
<input name="b" type="hidden" value="$BOARD">
<input name="id" type="hidden" value="$Id">
<input name="s" type="hidden" value="$Supersede">
<p>
__EOF__
    if ($Supersede && $SYS_F_SS) {
	&cgiprint'Cache(<<__EOF__);
上の$H_MESGと入れ換える$H_MESGを書き込んでください．
__EOF__
    } else {
	&cgiprint'Cache(<<__EOF__);
$H_SUBJECT，$H_MESG，$H_FROM，$H_MAIL，さらにウェブページをお持ちの方は，
ホームページの$H_URLを書き込んでください(もちろん，なくても構いません)．
__EOF__
    }

    # HTMLでも書ける場合
    if ($SYS_TEXTTYPE) {
	&cgiprint'Cache(<<__EOF__);
HTMLをご存じの方は，「$H_TEXTTYPE」を「$H_HTML」にして，
$H_MESGをHTMLとして書いて頂くと，表示の時にHTML整形を行ないます．
__EOF__
    }

    &cgiprint'Cache(<<__EOF__);
</p>
<p>
$H_BOARD: $BOARDNAME<br>
__EOF__

    # アイコンの選択
    if ($SYS_ICON) {
	&cashIconDB($BOARD);	# アイコンDBをキャッシュ
	&cgiprint'Cache("$H_ICON:\n<SELECT NAME=\"icon\">\n<OPTION SELECTED>$H_NOICON\n");
	foreach $IconTitle (sort keys(%ICON_FILE)) {
	    &cgiprint'Cache("<OPTION>$IconTitle\n");
	}
	&cgiprint'Cache("</SELECT>\n");

	&cgiprint'Cache("(<a href=\"$PROGRAM?b=$BOARD&c=i&type=entry\">アイコンの説明</a>)<BR>\n");

    }

    # Subject(フォローなら自動的に文字列を入れる)
    &cgiprint'Cache(sprintf("%s: <input name=\"subject\" type=\"text\" value=\"%s\" size=\"%s\"><br>\n", $H_SUBJECT, $DefSubject, $SUBJECT_LENGTH));

    # TextType
    if ($SYS_TEXTTYPE) {
	&cgiprint'Cache(<<__EOF__);
$H_TEXTTYPE:
<SELECT NAME="texttype">
<OPTION SELECTED>$H_PRE
<OPTION>$H_HTML
</SELECT>
</p>
__EOF__

    }

    # 本文(引用ありなら元記事を挿入)
    &cgiprint'Cache("<p><textarea name=\"article\" rows=\"$TEXT_ROWS\" cols=\"$TEXT_COLS\">");
    if ($Supersede && $SYS_F_SS) {
	&QuoteOriginalArticleWithoutQMark($Id);
    } elsif ($QuoteFlag == 2) {
	&QuoteOriginalArticle($Id);
    }

    &cgiprint'Cache("</textarea></p>\n");

    # フッタ部分を表示
    # 名前とメイルアドレス，URL．
    &cgiprint'Cache(<<__EOF__);
<p>
$H_MESG中に関連ウェブページへのリンクを張る場合は，
「&lt;URL:http://〜&gt;」のように，URLを「&lt;URL:」と「&gt;」で囲んで
書き込んでください．自動的にリンクが張られます．
</p>
__EOF__

    if ($SYS_ALIAS == 0) {

	# エイリアスは使わない
	&cgiprint'Cache(<<__EOF__);
<p>
$H_FROM: <input name="name" type="text" value="$DefName" size="$NAME_LENGTH"><br>
$H_MAIL: <input name="mail" type="text" value="$DefEmail" size="$MAIL_LENGTH"><br>
$H_URL_S: <input name="url" type="text" value="$DefUrl" size="$URL_LENGTH"><br>
</p>
__EOF__

    } elsif ($SYS_ALIAS == 1) {

	# エイリアスを使う
	&cgiprint'Cache(<<__EOF__);
<p>
$H_FROM: <input name="name" type="text" value="$DefName" size="$NAME_LENGTH"><br>
$H_MAIL: <input name="mail" type="text" value="$DefEmail" size="$MAIL_LENGTH"><br>
$H_URL_S: <input name="url" type="text" value="$DefUrl" size="$URL_LENGTH">
</p>
__EOF__

	&cgiprint'Cache(<<__EOF__);
<p>
「$H_ALIAS」に，$H_FROMと$H_MAIL，$H_URLを登録なさっている方は，
「$H_FROM」に「#...」という登録名を書いてください．
自動的に$H_FROMと$H_MAIL，$H_URLが補われます．
(<a href="$PROGRAM?c=as">$H_ALIASの一覧</a> //
 <a href="$PROGRAM?c=an">$H_ALIASを登録</a>)
</p>
__EOF__

    } else {

	# エイリアスを登録しなければ書き込みできない

	# エイリアスの読み込み
	&CashAliasData;

	&cgiprint'Cache(<<__EOF__);
<p>
$H_USER:
<SELECT NAME="name">
<OPTION SELECTED>$H_FROMを登録した$H_ALIASを選んでください
__EOF__

	while (($Key, $Value) = each %Name) {
	    &cgiprint'Cache("<OPTION>$Key\n");
	}
	&cgiprint'Cache(<<__EOF__);
</SELECT>
</p>
__EOF__

	&cgiprint'Cache(<<__EOF__);
<p>
予め「$H_ALIAS」に，$H_FROMと$H_MAIL，$H_URLを登録しないと書き込めません．
登録した後，「#...」という登録名を指定してください．
(<a href="$PROGRAM?c=as">$H_ALIASの一覧</a> //
 <a href="$PROGRAM?c=an">$H_ALIASを登録</a>)<br>
登録した$H_ALIASが表示されない(選択できない)場合，
このページを再読み込みしてください．
</p>
__EOF__

    }

    if ($SYS_MAIL) {
	&cgiprint'Cache("<p>$H_REPLYがあった時にメイルで知らせますか? <input name=\"fmail\" type=\"checkbox\" value=\"on\"></p>\n");
    }
    
    # ボタン
    &cgiprint'Cache(<<__EOF__);
<p>
書き込んだ内容を，<br>
<input type="radio" name="com" value="p" CHECKED>: 試しに表示してみる(まだ投稿しません)<br>
__EOF__

    if ($Supersede && $SYS_F_SS) {
	&cgiprint'Cache("<input type=\"radio\" name=\"com\" value=\"x\">: 訂正します<br>\n");
    } else {
	&cgiprint'Cache("<input type=\"radio\" name=\"com\" value=\"x\">: $H_MESGを投稿する<br>\n");
    }

    &cgiprint'Cache(<<__EOF__);
<input type="submit" value="実行">
</p>
</form>
__EOF__

    &MsgFooter;

}


###
## Preview - プレビュー画面の表示
#
# - SYNOPSIS
#	Preview;
#
# - ARGS
#	なし
#
# - DESCRIPTION
#	プレビュー画面を表示する．
#	大域変数である，CGI変数を参照する．
#
# - RETURN
#	なし
#
sub Preview {

    local($Supersede, $Id, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail, $rFid);

    # 入力された記事情報
    $Supersede = $cgi'TAGS{'s'};
    $Id = $cgi'TAGS{'id'};
    $TextType = $cgi'TAGS{'texttype'};
    $Name = $cgi'TAGS{'name'};
    $Email = $cgi'TAGS{'mail'};
    $Url = $cgi'TAGS{'url'};
    $Icon = $cgi'TAGS{'icon'};
    $Subject = $cgi'TAGS{'subject'};
    $Article = $cgi'TAGS{'article'};
    $Fmail = $cgi'TAGS{'fmail'};
    if ($Id ne '') { $rFid = &GetArticlesInfo($Id); }

    # 入力された記事情報のチェック
    $Article = &CheckArticle($BOARD, $TextType, *Name, *Email, *Url, *Subject, *Icon, $Article);

    # 確認画面の作成
    &MsgHeader('Message preview', "$BOARDNAME: 書き込みの内容を確認してください");

    # お約束
    &cgiprint'Cache(<<__EOF__);
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
<input name="fmail"    type="hidden" value="$Fmail">
<input name="s"        type="hidden" value="$Supersede">

__EOF__

    if ($Supersede && $SYS_F_SS) {
	&cgiprint'Cache(<<__EOF__);
<p>
上の$H_MESGの替わりに，下の$H_MESGを書き込みます．
必要であれば，ブラウザのBACKボタンで戻って，書き込みを修正してください．
よろしければボタンを押して訂正しましょう．
<input type="submit" value="訂正します">
</p>
</form>
__EOF__
	&ViewOriginalArticle($Id, 0, 1);
	&cgiprint'Cache("<hr>\n");
    } else {
	&cgiprint'Cache(<<__EOF__);
<p>
必要であれば，ブラウザのBACKボタンで戻って，書き込みを修正してください．
よろしければボタンを押して書き込みましょう．
<input type="submit" value="投稿する">
</p>
</form>
__EOF__
    }

    &cgiprint'Cache("<p>\n");

    # 題
    (($Icon eq $H_NOICON) || (! $Icon))
        ? &cgiprint'Cache("<strong>$H_SUBJECT</strong>: $Subject")
            : &cgiprint'Cache(sprintf("<strong>$H_SUBJECT</strong>: <img src=\"%s\" alt=\"$Icon \" width=\"$MSGICON_WIDTH\" height=\"$MSGICON_HEIGHT\">$Subject", &GetIconURLFromTitle($Icon, $BOARD)));

    # お名前
    if ($Url ne '') {
        # URLがある場合
        &cgiprint'Cache("<br>\n<strong>$H_FROM</strong>: <a href=\"$Url\">$Name</a>");
    } else {
        # URLがない場合
        &cgiprint'Cache("<br>\n<strong>$H_FROM</strong>: $Name");
    }

    # メイル
    if ($Email ne '') {
	&cgiprint'Cache(" <a href=\"mailto:$Email\">&lt;$Email&gt;</a>");
    }

    # 反応元(引用の場合)
    if (defined($rFid)) {
	if ($rFid ne '') {
	    &ShowLinksToFollowedArticle(($Id, split(/,/, $rFid)));
	} else {
	    &ShowLinksToFollowedArticle($Id);
	}
    }

    # 切れ目
    &cgiprint'Cache("</p>\n$H_LINE\n");

    # TextType用前処理
    if ((! $SYS_TEXTTYPE) || ($TextType eq $H_PRE)) {
	&cgiprint'Cache("<p><pre>");
    }

    # 記事
    $Article = &DQDecode($Article);
    $Article = &ArticleEncode($Article);
    &cgiprint'Cache("$Article\n");

    # TextType用後処理
    if ((! $SYS_TEXTTYPE) || ($TextType eq $H_PRE)) {
	&cgiprint'Cache("</pre></p>\n");
    }

    &MsgFooter;
}


###
## Thanks - 登録後画面の表示
#
# - SYNOPSIS
#	Thanks;
#
# - ARGS
#	なし
#
# - DESCRIPTION
#	書き込み後の画面を表示する
#	大域変数である，CGI変数を参照する．
#
# - RETURN
#	なし
#
sub Thanks {

    local($Supersede, $Id, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail, $ArticleId);

    # 入力された記事情報
    $Supersede = $cgi'TAGS{'s'};
    $Id = $cgi'TAGS{'id'};
    $TextType = $cgi'TAGS{'texttype'};
    $Name = $cgi'TAGS{'name'};
    $Email = $cgi'TAGS{'mail'};
    $Url = $cgi'TAGS{'url'};
    $Icon = $cgi'TAGS{'icon'};
    $Subject = $cgi'TAGS{'subject'};
    $Article = $cgi'TAGS{'article'};
    $Fmail = $cgi'TAGS{'fmail'};

    if ($Supersede && $SYS_F_SS) {

	# 訂正する 
	&SupersedeArticle($BOARD, $Id, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail);

	# 表示画面の作成
	&MsgHeader('Message superseded', "$BOARDNAME: $H_MESGが訂正されました");

    } else {

	# 記事の作成
	&MakeNewArticle($BOARD, $Id, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail);

	# 表示画面の作成
	&MsgHeader('Message entried', "$BOARDNAME: 書き込みありがとうございました");

    }

    if ($SYS_F_V) {
	&cgiprint'Cache(<<__EOF__);
<form action="$PROGRAM" method="POST">
<input name="b" type="hidden" value="$BOARD">
<input name="c" type="hidden" value="v">
<input name="num" type="hidden" value="$DEF_TITLE_NUM">
<input type="submit" value="$H_BACKTITLE">
</form>
__EOF__
    }

    if ($SYS_F_E && ($Id ne '')) {
	&cgiprint'Cache(<<__EOF__);
<form action="$PROGRAM" method="POST">
<input name="b" type="hidden" value="$BOARD">
<input name="c" type="hidden" value="e">
<input name="id" type="hidden" value="$Id">
<input type="submit" value="$H_ORIGの$H_MESGへ">
</form>
__EOF__
    }

    &MsgFooter;

}


###
## ShowArticle - 単一記事の表示
#
# - SYNOPSIS
#	ShowArticle;
#
# - ARGS
#	なし
#
# - DESCRIPTION
#	単一の記事を表示する．
#       大域変数である，CGI変数を参照する．
#
# - RETURN
#	なし
#
sub ShowArticle {

    local($Id, $Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $DateUtc, $Aid, @AidList, @FollowIdTree);

    $Id = $cgi'TAGS{'id'};
    ($Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url) = &GetArticlesInfo($Id);
    $DateUtc = &GetUtcFromOldDateTimeFormat($Date);
    @AidList = split(/,/, $Aids);

    # 未投稿記事は読めない
    if ($Name eq '') { &Fatal(8, ''); }

    # 表示画面の作成
    &MsgHeader('Message view', "$BOARDNAME: $Subject", $DateUtc);
    &ViewOriginalArticle($Id, 1, 1);

    # article end
    &cgiprint'Cache("$H_LINE\n<p>\n");

    # 反応記事
    &cgiprint'Cache("▼$H_REPLY\n");
    if ($Aids ne '') {

	# 反応記事があるなら…
	foreach $Aid (@AidList) {

	    # フォロー記事の木構造の取得
	    # ex. '( a ( b ( c d ) ) ( e ) ( f ( g ) ) )'というリスト
	    @FollowIdTree = &GetFollowIdTree($Aid);

	    # メイン関数の呼び出し(記事概要)
	    &ThreadArticleMain('subject only', @FollowIdTree);

	}

    } else {

	# 反応記事無し
	&cgiprint'Cache("<ul>\n<li>$H_REPLYはありません\n</ul>\n");

    }

    &cgiprint'Cache("</p>\n");

    # お約束
    &MsgFooter;

}


###
## ThreadArticle - フォロー記事を全て表示．
#
# - SYNOPSIS
#	ThreadArticle;
#
# - ARGS
#	なし
#
# - DESCRIPTION
#	ある記事と，その記事へのリプライ記事をまとめて表示する．
#       大域変数である，CGI変数を参照する．
#
# - RETURN
#	なし
#
sub ThreadArticle {

    local($Id, @FollowIdTree);

    $Id = $cgi'TAGS{'id'};

    # フォロー記事の木構造の取得
    # ex. '( a ( b ( c d ) ) ( e ) ( f ( g ) ) )'というリスト
    @FollowIdTree = &GetFollowIdTree($Id);

    # 表示画面の作成
    &MsgHeader('Message view (threaded)', "$BOARDNAME: $H_REPLYをまとめ読み");

    # メイン関数の呼び出し(記事概要)
    &ThreadArticleMain('subject only', @FollowIdTree);

    # メイン関数の呼び出し(記事)
    &ThreadArticleMain('', @FollowIdTree);

    &MsgFooter;

}

sub ThreadArticleMain {
    local($SubjectOnly, $Head, @Tail) = @_;

    # 記事概要か，記事そのものか．
    if ($SubjectOnly) {

	if ($Head eq '(') {
	    &cgiprint'Cache("<ul>\n");
	} elsif ($Head eq ')') {
	    &cgiprint'Cache("</ul>\n");
	} else {
	    local($dFid, $dAids, $dDate, $dSubject, $dIcon, $dRemoteHost, $dName) = &GetArticlesInfo($Head);
	    &cgiprint'Cache("<li>" . &GetFormattedTitle($Head, $BOARD, $dAids, $dIcon, $dSubject, $dName, $dDate) . "\n");
	}

    } else {

	if (($Head ne '(') && ($Head ne ')')) {
	    # 元記事の表示(コマンド付き, 元記事なし)
	    &cgiprint'Cache("<hr>\n");
	    &ViewOriginalArticle($Head, 1, 0);
	}

    }

    # 再帰
    if (@Tail) {
	&ThreadArticleMain($SubjectOnly, @Tail);
    }

}


###
## ShowIcon - アイコン表示画面
#
# - SYNOPSIS
#	ShowIcon;
#
# - ARGS
#	なし
#
# - DESCRIPTION
#	アイコン表示画面を表示する．
#	大域変数である，CGI変数を参照する．
#
# - RETURN
#	なし
#
sub ShowIcon {

    local($IconTitle, $Type);

    # タイプを拾う
    $Type = $cgi'TAGS{'type'};

    # 表示画面の作成
    &MsgHeader('Icon show', "$BOARDNAME: アイコンの説明");

    if ($Type eq 'article') {

	&cgiprint'Cache(<<__EOF__);
<p>
各アイコンは次の機能を表しています．
</p>
<ul>
<p>
<li><img src="$ICON_BLIST" alt="$H_BACKBOARD" height="$COMICON_HEIGHT" width="$COMICON_WIDTH"> : $H_BACKBOARD
<li><img src="$ICON_TLIST" alt="$H_BACKTITLE" height="$COMICON_HEIGHT" width="$COMICON_WIDTH"> : $H_BACKTITLE
<li><img src="$ICON_PREV" alt="$H_PREVARTICLE" height="$COMICON_HEIGHT" width="$COMICON_WIDTH"> : $H_PREVARTICLE
<li><img src="$ICON_NEXT" alt="$H_NEXTARTICLE" height="$COMICON_HEIGHT" width="$COMICON_WIDTH"> : $H_NEXTARTICLE
<li><img src="$ICON_THREAD" alt="$H_READREPLYALL" height="$COMICON_HEIGHT" width="$COMICON_WIDTH"> : $H_READREPLYALL
</p><p>
<li><img src="$ICON_WRITENEW" alt="$H_POSTNEWARTICLE" height="$COMICON_HEIGHT" width="$COMICON_WIDTH"> : $H_POSTNEWARTICLE
<li><img src="$ICON_FOLLOW" alt="$H_REPLYTHISARTICLE" height="$COMICON_HEIGHT" width="$COMICON_WIDTH"> : $H_REPLYTHISARTICLE
<li><img src="$ICON_QUOTE" alt="$H_REPLYTHISARTICLEQUOTE" height="$COMICON_HEIGHT" width="$COMICON_WIDTH"> : $H_REPLYTHISARTICLEQUOTE
</p>
</ul>
__EOF__

    } else {

	&cashIconDB($BOARD);	# アイコンDBのキャッシュ

	&cgiprint'Cache(<<__EOF__);
<p>
各アイコンは次の機能を表しています．
<p>
<ul>
<li>$H_THREAD : その$H_MESGの$H_REPLYをまとめて読む
</ul>
</p>
<p>
$H_BOARD「$BOARDNAME」では，次のアイコンを使うことができます．
</p>
<p>
<ul>
__EOF__
	foreach $IconTitle (sort keys(%ICON_FILE)) {
	    &cgiprint'Cache(sprintf("<li><img src=\"%s\" alt=\"$IconTitle\" height=\"$MSGICON_HEIGHT\" width=\"$MSGICON_WIDTH\"> : %s\n", &GetIconURLFromTitle($IconTitle, $BOARD), ($ICON_HELP{$IconTitle} || $IconTitle)));
	}
	&cgiprint'Cache("</ul>\n</p>\n");

    }

    &MsgFooter;

}


###
## SortArticle - 日付順にソート
#
# - SYNOPSIS
#	SortArticle;
#
# - ARGS
#	なし
#
# - DESCRIPTION
#	タイトル一覧を日付順にソートして表示する．
#	大域変数である，CGI変数を参照する．
#
# - RETURN
#	なし
#
sub SortArticle {

    local($Num, $Old, $NextOld, $BackOld, $To, $From, $IdNum, $Id);

    # 表示する個数を取得
    $Num = $cgi'TAGS{'num'};
    $Old = $cgi'TAGS{'old'};
    $NextOld = ($Old > $Num) ? ($Old - $Num) : 0;
    $BackOld = ($Old + $Num);
    $To = $#DB_ID - $Old;
    $From = $To - $Num + 1; $From = 0 if (($From < 0) || ($Num == 0));

    # 表示画面の作成
    &MsgHeader('Title view (sorted)', "$BOARDNAME: $H_SUBJECT一覧(日付順)");

    &BoardHeader('normal');

    &cgiprint'Cache("<hr>\n");

    if ($SYS_BOTTOMTITLE) {
	&cgiprint'Cache("<p>$H_TOP<a href=\"$PROGRAM?b=$BOARD&c=r&num=$Num&old=$BackOld\">$H_BACKART</a></p>\n") if ($From > 0);
    } else {
	&cgiprint'Cache("<p>$H_TOP<a href=\"$PROGRAM?b=$BOARD&c=r&num=$Num&old=$NextOld\">$H_NEXTART</a></p>\n") if ($Old);
    }

    &cgiprint'Cache("<p><ul>\n");

    # 記事の表示
    if ($#DB_ID == -1) {

	# 空だった……
	&cgiprint'Cache("<li>$H_NOARTICLE\n");

    } else {

	if ($SYS_BOTTOMTITLE) {
	    for ($IdNum = $From; $IdNum <= $To; $IdNum++) {
		$Id = $DB_ID[$IdNum];
		&cgiprint'Cache("<li>" . &GetFormattedTitle($Id, $BOARD, $DB_AIDS{$Id}, $DB_ICON{$Id}, $DB_TITLE{$Id}, $DB_NAME{$Id}, $DB_DATE{$Id}) . "\n");
	    }
	} else {
	    for ($IdNum = $To; $IdNum >= $From; $IdNum--) {
		$Id = $DB_ID[$IdNum];
		&cgiprint'Cache("<li>" . &GetFormattedTitle($Id, $BOARD, $DB_AIDS{$Id}, $DB_ICON{$Id}, $DB_TITLE{$Id}, $DB_NAME{$Id}, $DB_DATE{$Id}) . "\n");
	    }
	}
    }

    &cgiprint'Cache("</ul></p>\n");

    if ($SYS_BOTTOMTITLE) {
	&cgiprint'Cache("<p>$H_BOTTOM<a href=\"$PROGRAM?b=$BOARD&c=r&num=$Num&old=$NextOld\">$H_NEXTART</a></p>\n") if ($Old);
    } else {
	&cgiprint'Cache("<p>$H_BOTTOM<a href=\"$PROGRAM?b=$BOARD&c=r&num=$Num&old=$BackOld\">$H_BACKART</a></p>\n") if ($From > 0);
    }

    &MsgFooter;

}


###
## ViewTitle - スレッド別表示
#
# - SYNOPSIS
#	ViewTitle($ComType);
#
# - ARGS
#	$ComType	表示画面のタイプ
#				指定なし ... 記事参照画面
#				maint ...... 記事管理画面
#				linkto ..... リンクかけかえ先指定画面
#				linkexec ... リンクかけかえ実施
#				moveto ..... 移動先指定画面
#				moveexec ... 移動実施
#
# - DESCRIPTION
#	新しい記事のタイトルをスレッド別にソートして表示．
#	大域変数である，CGI変数を参照する．
#	大域変数ADDFLAG(既に表示してしまったか否かを表わすフラグ)を破壊する．
#
# - RETURN
#	なし
#
sub ViewTitle {
    local($ComType) = @_;
    local($Num, $Old, $NextOld, $BackOld, $To, $From, $IdNum, $Id, $Fid, $IdNum, $Id, $NextCommand, $FirstFlag, $Key, $Value, $AddNum);
    %ADDFLAG = ();		# it's static.

    if ($ComType eq 'linkexec') {
	# リンクかけかえの実施
	&ReLinkExec($cgi'TAGS{'rfid'}, $cgi'TAGS{'rtid'}, $BOARD);
    } elsif ($ComType eq 'moveexec') {
	# 移動の実施
	&ReOrderExec($cgi'TAGS{'rfid'}, $cgi'TAGS{'rtid'}, $BOARD);
    }

    # 表示する個数を取得
    $Num = $cgi'TAGS{'num'};
    $Old = $cgi'TAGS{'old'};
    $NextOld = ($Old > $Num) ? ($Old - $Num) : 0;
    $BackOld = ($Old + $Num);
    $To = $#DB_ID - $Old;
    $From = $To - $Num + 1; $From = 0 if (($From < 0) || ($Num == 0));

    # 整形済みフラグ
    # 0 ... 整形対象外
    # 1 ... 整形済み
    # 2 ... 未整形
    for($IdNum = $From; $IdNum <= $To; $IdNum++) { $ADDFLAG{$DB_ID[$IdNum]} = 2; }

    # 前/後ろコマンド
    $FirstFlag = 1;
    $NextCommand = '?';
    while (($Key, $Value) = each %cgi'TAGS) {
	# 数関連はカット
	next if (($Key eq 'num') || ($Key eq 'old'));
	if ($FirstFlag) { $FirstFlag = 0; } else { $NextCommand .= "&"; }
	$NextCommand .= "$Key=$Value";
    }

    # ページング用文字列
    $AddNum = "&num=" . $cgi'TAGS{'num'} . "&old=" . $cgi'TAGS{'old'};

    # 表示画面の作成
    if ($ComType eq 'linkto') {
	&MsgHeader('Title view (threaded)', "$BOARDNAME: 新たなリプライ先の指定");
    } elsif ($ComType eq 'linkexec') {
	&MsgHeader('Title view (threaded)', "$BOARDNAME: 指定された$H_MESGのリプライ先を変更しました");
    } elsif ($ComType eq 'moveto') {
	&MsgHeader('Title view (threaded)', "$BOARDNAME: 移動先の指定");
    } elsif ($ComType eq 'moveexec') {
	&MsgHeader('Title view (threaded)', "$BOARDNAME: 指定された$H_MESGを移動しました");
    } else {
	&MsgHeader('Title view (threaded)', "$BOARDNAME: $H_SUBJECT一覧($H_REPLY順)");
    }

    if ($ComType) {
	&BoardHeader('maint');
    } else {
	&BoardHeader('normal');
    }

    &cgiprint'Cache("<p>\n<ul>\n<li><a href=\"$PROGRAM?b=$BOARD&c=ce&rtid=" . $cgi'TAGS{'roid'} . "&rfid=" . $cgi'TAGS{'rfid'} . "\">今の変更を元に戻す</a>\n</ul>\n</p>") if ($ComType eq 'linkexec');

    if ($ComType) {
	&cgiprint'Cache(<<__EOF__);
<p>各アイコンは，次のような意味を表しています．
<dl compact>
<dt>$H_RELINKFROM_MARK
<dd>この$H_MESGの$H_REPLY先を変更します．$H_REPLY先を指定する画面に飛びます．
<dt>$H_REORDERFROM_MARK
<dd>この$H_MESGの順序を変更します．移動先を指定する画面に飛びます．
<dt>$H_DELETE_ICON
<dd>この$H_MESGを削除します．
<dt>$H_SUPERSEDE_ICON
<dd>この$H_MESGを訂正します．
<dt>$H_RELINKTO_MARK
<dd>先に指定した$H_MESGの$H_REPLY先を，この$H_MESGにします．
<dt>$H_REORDERTO_MARK
<dd>先に指定した$H_MESGを，この$H_MESGの下に移動します．
</dl></p>
__EOF__
    }

    if ($ComType eq 'linkto') {
	&cgiprint'Cache("<p>" . $cgi'TAGS{'rfid'} . "を，どの$H_MESGへのリプライにしますか? リプライ先の$H_MESGの$H_RELINKTO_MARKをクリックしてください．</p>\n");
    } elsif ($ComType eq 'moveto') {
	&cgiprint'Cache("<p>" . $cgi'TAGS{'rfid'} . "を，どの$H_MESGの下に移動しますか? $H_MESGの$H_REORDERTO_MARKをクリックしてください．</p>\n");
    }

    &cgiprint'Cache("<hr>\n");

    if ($SYS_BOTTOMTITLE) {
	&cgiprint'Cache("<p>$H_TOP<a href=\"$PROGRAM?b=$BOARD&c=v&num=$Num&old=$BackOld\">$H_BACKART</a></p>\n") if ($From > 0);
    } else {
	&cgiprint'Cache("<p>$H_TOP<a href=\"$PROGRAM?b=$BOARD&c=v&num=$Num&old=$NextOld\">$H_NEXTART</a></p>\n") if ($Old);
    }

    &cgiprint'Cache("<p><ul>\n");

    if ($To < $From) {

	# 空だった……
	&cgiprint'Cache("<li>$H_NOARTICLE\n");

    } elsif ($SYS_BOTTOMTITLE) {

	# 古いのから処理
	&cgiprint'Cache("<li><a href=\"$PROGRAM?b=$BOARD&c=ce&rtid=&rfid=" . $cgi'TAGS{'rfid'} . "&roid=" . $cgi'TAGS{'roid'} . "$AddNum\">[どの$H_MESGへのリプライでもなく，新着$H_MESGにする]</a>\n") if (($ComType eq 'linkto') && ($DB_FID{$cgi'TAGS{'rfid'}} ne ''));
	&cgiprint'Cache("<li><a href=\"$PROGRAM?b=$BOARD&c=mve&rtid=&rfid=" . $cgi'TAGS{'rfid'} . "&roid=" . $cgi'TAGS{'roid'} . "$AddNum\">[全記事の先頭に移動する(このページの先頭，ではありません)]</a>\n") if ($ComType eq 'moveto');

	for($IdNum = $From; $IdNum <= $To; $IdNum++) {

	    # 該当記事のIDを取り出す
	    $Id = $DB_ID[$IdNum];
	    ($Fid = $DB_FID{$Id}) =~ s/,.*$//o;
	    # 後方参照は後回し．
	    next if (($Fid ne '') && ($ADDFLAG{$Fid} == 2));
	    # ノードを表示
	    if ($ComType) {
		&ViewTitleNodeMaint($Id, $ComType, $AddNum);
	    } else {
		&ViewTitleNode($Id);
	    }
	}
    } else {

	# 新しいのから処理
	&cgiprint'Cache("<li><a href=\"$PROGRAM?b=$BOARD&c=ce&rtid=&rfid=" . $cgi'TAGS{'rfid'} . "&roid=" . $cgi'TAGS{'roid'} . "$AddNum\">[どの$H_MESGへのリプライでもなく，新着$H_MESGにする]</a>\n") if (($ComType eq 'linkto') && ($DB_FID{$cgi'TAGS{'rfid'}} ne ''));
	&cgiprint'Cache("<li><a href=\"$PROGRAM?b=$BOARD&c=mve&rtid=&rfid=" . $cgi'TAGS{'rfid'} . "&roid=" . $cgi'TAGS{'roid'} . "$AddNum\">[全記事の先頭に移動する(このページの先頭，ではありません)]</a>\n") if ($ComType eq 'moveto');

	for($IdNum = $To; $IdNum >= $From; $IdNum--) {
	    # 後は同じ
	    $Id = $DB_ID[$IdNum];
	    ($Fid = $DB_FID{$Id}) =~ s/,.*$//o;
	    next if (($Fid ne '') && ($ADDFLAG{$Fid} == 2));
	    if ($ComType) {
		&ViewTitleNodeMaint($Id, $ComType, $AddNum);
	    } else {
		&ViewTitleNode($Id);
	    }
	}
    }

    &cgiprint'Cache("</ul></p>\n");

    if ($SYS_BOTTOMTITLE) {
	&cgiprint'Cache("<p>$H_BOTTOM<a href=\"$PROGRAM?b=$BOARD&c=v&num=$Num&old=$NextOld\">$H_NEXTART</a></p>\n") if ($Old);
    } else {
	&cgiprint'Cache("<p>$H_BOTTOM<a href=\"$PROGRAM?b=$BOARD&c=v&num=$Num&old=$BackOld\">$H_BACKART</a></p>\n") if ($From > 0);
    }

    &MsgFooter;

    undef(%ADDFLAG);

}

sub ViewTitleNode {
    local($Id) = @_;

    if ($ADDFLAG{$Id} != 2) { return; }

    &cgiprint'Cache("<li>" . &GetFormattedTitle($Id, $BOARD, $DB_AIDS{$Id}, $DB_ICON{$Id}, $DB_TITLE{$Id}, $DB_NAME{$Id}, $DB_DATE{$Id}) . "\n");
    $ADDFLAG{$Id} = 1;		# 整形済み

    # 娘が居れば……
    if ($DB_AIDS{$Id}) {
	&cgiprint'Cache("<ul>\n");
	foreach (split(/,/, $DB_AIDS{$Id})) { &ViewTitleNode($_); }
	&cgiprint'Cache("</ul>\n");
    }
}

sub ViewTitleNodeMaint {

    local($Id, $ComType, $AddNum) = @_;

    return if ($ADDFLAG{$Id} != 2);

    local($FromId) = $cgi'TAGS{'rfid'};

    &cgiprint'Cache("<li>" . &GetFormattedTitle($Id, $BOARD, $DB_AIDS{$Id}, $DB_ICON{$Id}, $DB_TITLE{$Id}, $DB_NAME{$Id}, $DB_DATE{$Id})); #'

    &cgiprint'Cache(" .......... \n");

    # リンク先変更コマンド(From)
    if ($SYS_F_LI) {
	&cgiprint'Cache("<a href=\"$PROGRAM?b=$BOARD&c=ct&rfid=$Id&roid=" . $DB_FID{$Id} . "$AddNum\">$H_RELINKFROM_MARK</a>\n");
    }

    # 移動コマンド(From)
    if ($SYS_F_MV) {
	&cgiprint'Cache("<a href=\"$PROGRAM?b=$BOARD&c=mvt&rfid=$Id&roid=" . $DB_FID{$Id} . "$AddNum\">$H_REORDERFROM_MARK</a>\n") if ($DB_FID{$Id} eq '');
    }

    # 削除コマンド
    if ($SYS_F_D) {
	&cgiprint'Cache("<a href=\"$PROGRAM?b=$BOARD&c=dp&id=$Id\">$H_DELETE_ICON</a>\n");
    }

    # 訂正コマンド
    if ($SYS_F_SS) {
	&cgiprint'Cache("<a href=\"$PROGRAM?b=$BOARD&c=f&s=on&id=$Id\">$H_SUPERSEDE_ICON</a>\n");
    }

    # 移動コマンド(To)
    if ($SYS_F_MV && ($ComType eq 'moveto') && ($FromId ne $Id) && ($DB_FID{$Id} eq '') && ($FromId ne $Id)) {
	&cgiprint'Cache("<a href=\"$PROGRAM?b=$BOARD&c=mve&rtid=$Id&rfid=$FromId&roid=" . $cgi'TAGS{'roid'} . "$AddNum\">$H_REORDERTO_MARK</a>\n");
    }

    # リンク先変更コマンド(To)
    if ($SYS_F_LI && ($ComType eq 'linkto') && ($FromId ne $Id) && (! grep(/^$FromId$/, split(/,/, $DB_AIDS{$Id}))) && (! grep(/^$FromId$/, split(/,/, $DB_FID{$Id})))) {
	&cgiprint'Cache("<a href=\"$PROGRAM?b=$BOARD&c=ce&rtid=$Id&rfid=$FromId&roid=" . $cgi'TAGS{'roid'} . "$AddNum\">$H_RELINKTO_MARK</a>\n");
    }

    $ADDFLAG{$Id} = 1;		# 整形済み

    # 娘が居れば……
    if ($DB_AIDS{$Id}) {
	&cgiprint'Cache("<ul>\n");
	foreach (split(/,/, $DB_AIDS{$Id})) { &ViewTitleNodeMaint($_, $ComType, $AddNum); }
	&cgiprint'Cache("</ul>\n");
    }
}


###
## NewArticle - 新しい記事をまとめて表示
#
# - SYNOPSIS
#	NewArticle;
#
# - ARGS
#	なし
#
# - DESCRIPTION
#	新しい記事をまとめて表示．
#	大域変数である，CGI変数を参照する．
#
# - RETURN
#	なし
#
sub NewArticle {

    local($Num, $Old, $NextOld, $BackOld, $To, $From, $Id);

    # 表示する個数を取得
    $Num = $cgi'TAGS{'num'};
    $Old = $cgi'TAGS{'old'};
    $NextOld = ($Old > $Num) ? ($Old - $Num) : 0;
    $BackOld = ($Old + $Num);
    $To = $#DB_ID - $Old;
    $From = $To - $Num + 1; $From = 0 if (($From < 0) || ($Num == 0));

    # 表示画面の作成
    &MsgHeader('Message view (sorted)', "$BOARDNAME: 最近の$H_MESGをまとめ読み");

    if ($SYS_BOTTOMARTICLE) {
	&cgiprint'Cache("<p>$H_TOP<a href=\"$PROGRAM?b=$BOARD&c=l&num=$Num&old=$BackOld\">$H_BACKART</a></p>\n") if ($From > 0);
    } else {
	&cgiprint'Cache("<p>$H_TOP<a href=\"$PROGRAM?b=$BOARD&c=l&num=$Num&old=$NextOld\">$H_NEXTART</a></p>\n") if ($Old);
    }

    if (! $#DB_ID == -1) {

	# 空だった……
	&cgiprint'Cache("<p>$H_NOARTICLE</p>\n");

    } else {

	if ($SYS_BOTTOMARTICLE) {
	    for ($IdNum = $From; $IdNum <= $To; $IdNum++) {
		$Id = $DB_ID[$IdNum];
		&ViewOriginalArticle($Id, 1, 1);
		&cgiprint'Cache("<hr>\n");
	    }
	} else {
	    for ($IdNum = $To; $IdNum >= $From; $IdNum--) {
		$Id = $DB_ID[$IdNum];
		&ViewOriginalArticle($Id, 1, 1);
		&cgiprint'Cache("<hr>\n");
	    }
	}

    }

    if ($SYS_BOTTOMARTICLE) {
	&cgiprint'Cache("<p>$H_BOTTOM<a href=\"$PROGRAM?b=$BOARD&c=l&num=$Num&old=$NextOld\">$H_NEXTART</a></p>\n") if ($Old);
    } else {
	&cgiprint'Cache("<p>$H_BOTTOM<a href=\"$PROGRAM?b=$BOARD&c=l&num=$Num&old=$BackOld\">$H_BACKART</a></p>\n") if ($From > 0);
    }

    if ($SYS_F_V) {
	&cgiprint'Cache(<<__EOF__);
<form action="$PROGRAM" method="POST">
<input name="b" type="hidden" value="$BOARD">
<input name="c" type="hidden" value="v">
<input name="num" type="hidden" value="$DEF_TITLE_NUM">
<input type="submit" value="$H_BACKTITLE">
</form>
__EOF__
    }

    &MsgFooter;

}


###
## SearchArticle - 記事の検索(表示画面の作成)
#
# - SYNOPSIS
#	SearchArticle;
#
# - ARGS
#	なし
#
# - DESCRIPTION
#	記事を検索する(うち，表示画面の作成部分)．
#	大域変数である，CGI変数を参照する．
#
# - RETURN
#	なし
#
sub SearchArticle {

    local($Key, $SearchSubject, $SearchPerson, $SearchArticle, $SearchIcon, $Icon, $IconTitle);

    $Key = $cgi'TAGS{'key'};
    $SearchSubject = $cgi'TAGS{'searchsubject'};
    $SearchPerson = $cgi'TAGS{'searchperson'};
    $SearchArticle = $cgi'TAGS{'searcharticle'};
    $SearchIcon = $cgi'TAGS{'searchicon'};
    $Icon = $cgi'TAGS{'icon'};

    # 表示画面の作成
    &MsgHeader('Message search', "$BOARDNAME: $H_MESGの検索");

    # お約束
    &cgiprint'Cache(<<__EOF__);
<form action="$PROGRAM\" method="POST">
<input name="c" type="hidden" value="s">
<input name="b" type="hidden" value="$BOARD">
 
<p>
<ul>
<li>「$H_SUBJECT」，「名前」，「$H_MESG」の中から，検索する範囲をチェックしてください．
指定された範囲で，キーワードを含む$H_MESGを一覧表示します．
<li>キーワードには，大文字小文字の区別はありません．
<li>キーワードを半角スペースで区切って，複数のキーワードを指定すると，
それら全てを含む$H_MESGのみを検索することができます．
<li>アイコンで検索する場合は，
「アイコン」をチェックした後，探したい$H_MESGのアイコンを選んでください．
</ul>
</p>
<input type="submit" value="検索する">
<input type="reset" value="リセットする">

<p>キーワード:
<input name="key" type="text" size="$KEYWORD_LENGTH" value="$Key">
</p>

<p>検索範囲:
<ul>
__EOF__

    &cgiprint'Cache(sprintf("<li><input name=\"searchsubject\" type=\"checkbox\" value=\"on\" %s>: $H_SUBJECT\n", (($SearchSubject) ? 'CHECKED' : '')));
    &cgiprint'Cache(sprintf("<li><input name=\"searchperson\" type=\"checkbox\" value=\"on\" %s>: 名前\n", (($SearchPerson) ? 'CHECKED' : '')));
    &cgiprint'Cache(sprintf("<li><input name=\"searcharticle\" type=\"checkbox\" value=\"on\" %s>: $H_MESG", (($SearchArticle) ? 'CHECKED' : '')));

    &cgiprint'Cache(sprintf("<li><input name=\"searchicon\" type=\"checkbox\" value=\"on\" %s>: $H_ICON // ", (($SearchIcon) ? 'CHECKED' : '')));

    # アイコンの選択
    &cashIconDB($BOARD);	# アイコンDBのキャッシュ
    &cgiprint'Cache(sprintf("<SELECT NAME=\"icon\">\n<OPTION%s>$H_NOICON\n", (($Icon && ($Icon ne $H_NOICON)) ? '' : ' SELECTED')));
    foreach $IconTitle (sort keys(%ICON_FILE)) {
	&cgiprint'Cache(sprintf("<OPTION%s>$IconTitle\n", (($Icon eq $IconTitle) ? ' SELECTED' : '')));
    }
    &cgiprint'Cache("</SELECT>\n");

    # アイコン一覧
    &cgiprint'Cache(<<__EOF__);
(<a href="$PROGRAM?b=$BOARD&c=i&type=entry">アイコンの説明</a>)<BR>
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

sub SearchArticleList {
    local($Key, $Subject, $Person, $Article, $Icon, $IconType) = @_;
    local($dId, $dAids, $dDate, $dTitle, $dIcon, $dName, $dEmail, $HitNum, $Line, $SubjectFlag, $PersonFlag, $ArticleFlag, @KeyList);

    @KeyList = split(/ +/, $Key);

    # リスト開く
    &cgiprint'Cache("<p><ul>\n");

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
		    if ($dTitle !~ /$_/i) {
			$SubjectFlag = 0;
		    }
		}
	    }

	    # 投稿者名を検索
	    if (($Person ne '') && ($dName ne '')) {
		$PersonFlag = 1;
		foreach (@KeyList) {
		    if (($dName !~ /$_/i) && ($dEmail !~ /$_/i)) {
			$PersonFlag = 0;
		    }
		}
	    }

	    # 本文を検索
	    if (($Article ne '') && ($Line = &SearchArticleKeyword($dId, $BOARD, @KeyList))) {
		$ArticleFlag = 1;
	    }

	} else {

	    # 無条件で一致
	    $SubjectFlag = 1;

	}

	if ($SubjectFlag || $PersonFlag || $ArticleFlag) {

	    # 最低1つは合致した
	    $HitNum++;

	    # 記事へのリンクを表示
	    &cgiprint'Cache("<li>" . &GetFormattedTitle($dId, $BOARD, $dAids, $dIcon, $dTitle, $dName, $dDate) . "\n");

	    # 本文に合致した場合は本文も表示
	    if ($ArticleFlag) {
		$Line =~ s/<[^>]*>//go;
		&cgiprint'Cache("<blockquote>$Line</blockquote>\n");
	    }
	}
    }

    # ヒットしなかったら
    if ($HitNum) {
	&cgiprint'Cache("</ul>\n</p><p>\n<ul>");
	&cgiprint'Cache("<li>$HitNum件の$H_MESGが見つかりました．\n");
    } else {
	&cgiprint'Cache("<li>該当する$H_MESGは見つかりませんでした．\n");
    }

    # リスト閉じる
    &cgiprint'Cache("</ul></p>\n");
}


###
## AliasNew - エイリアスの登録と変更画面の表示
#
# - SYNOPSIS
#	AliasNew;
#
# - ARGS
#	なし
#
# - DESCRIPTION
#	エイリアスの登録と変更画面を表示する(表示するだけ)．
#
# - RETURN
#	なし
#
sub AliasNew {

    # 表示画面の作成
    &MsgHeader('Alias entry/edit', "$H_ALIASの登録/変更/削除");

    # 新規登録/登録内容の変更
    &cgiprint'Cache(<<__EOF__);
<p>
新規登録/登録内容の変更
</p>
<p>
<form action="$PROGRAM" method="POST">
<input name="c" type="hidden" value="am">
$H_ALIAS: <input name="alias" type="text" value="#" size="$NAME_LENGTH"><br>
$H_FROM: <input name="name" type="text" size="$NAME_LENGTH"><br>
$H_MAIL: <input name="email" type="text" size="$MAIL_LENGTH"><br>
$H_URL_S: <input name="url" type="text" value="http://" size="$URL_LENGTH"><br>
$H_ALIASの新規登録/登録内容の変更を行ないます．
エイリアスは(あなた以外の!)誰にでも書き換えることができます．
登録内容が変更されていないかどうか，
書き込む時の「試しに表示する」画面を注意してチェックしてください．
また，間違って同じエイリアスを登録されてしまわないように，
あまりに簡単な「エイリアス」は避けてくださいね．<br>
<input type="submit" value="登録/変更する">
</form>
</p>
<hr>
<p>
削除
</p>
<p>
<form action="$PROGRAM" method="POST">
<input name="c" type="hidden" value="ad">
$H_ALIAS: <input name="alias" type="text" size="$NAME_LENGTH"><br>
上記$H_ALIASを削除します．<br>
<input type="submit" value="削除する">
</form>
</p>
<hr>
<p>
<form action="$PROGRAM" method="POST">
<input name="c" type="hidden" value="as">
<input type="submit" value="$H_ALIAS一覧を参照する">
</form>
</p>
__EOF__
    
    # お約束
    &MsgFooter;

}


###
## AliasMod - ユーザエイリアスの登録/変更
#
# - SYNOPSIS
#	AliasMod;
#
# - ARGS
#	なし
#
# - DESCRIPTION
#	ユーザエイリアスを登録/変更し，その結果を知らせる画面を表示する．
#	大域変数である，CGI変数を参照する．
#	アプリケーションモデルとも，GUIとも取れる……分離できてない．
#
# - RETURN
#	なし
#
sub AliasMod {

    local($A, $N, $E, $U, $HitFlag, $Alias);

    $A = $cgi'TAGS{'alias'};
    $N = $cgi'TAGS{'name'};
    $E = $cgi'TAGS{'email'};
    $U = $cgi'TAGS{'url'};
    
    # マシンがマッチしたか
    #	0 ... エイリアスがマッチしない
    #	2 ... マッチしてデータを変更した
    $HitFlag = 0;

    # 文字列チェック
    &AliasCheck($A, $N, $E, $U);
    
    # エイリアスの読み込み
    &CashAliasData;
    
    # 1行ずつチェック
    foreach $Alias (sort keys(%Name)) {
	next if ($A ne $Alias);
	$HitFlag = 2;		# 合ったら2を設定．マシン名は無視．
    }
    
    # 新規登録
    if ($HitFlag == 0) {
	$Alias = $A;
    }
    
    # データの登録
    $Name{$Alias} = $N;
    $Email{$Alias} = $E;
    $Host{$Alias} = $REMOTE_HOST;
    $URL{$Alias} = $U;
    
    # エイリアスファイルに書き出し
    &WriteAliasData;

    # 表示画面の作成
    &MsgHeader('Alias modified', "$H_ALIASが設定されました");
    &cgiprint'Cache("<p>$H_ALIAS: <strong>$A</strong>:\n");
    if ($HitFlag == 2) {
	&cgiprint'Cache("設定しました．</p>\n");
    } else {
	&cgiprint'Cache("登録しました．</p>\n");
    }
    &MsgFooter;
    
}


###
## AliasDel - ユーザエイリアスの削除
#
# - SYNOPSIS
#	AliasDel;
#
# - ARGS
#	なし
#
# - DESCRIPTION
#	ユーザエイリアスを削除する．登録ホストと同一でなければ不可．
#	その後，その結果を知らせる画面を表示する．
#	大域変数である，CGI変数を参照する．
#	アプリケーションモデルとも，GUIとも取れる．分離できてない．
#
# - RETURN
#	なし
#
sub AliasDel {

    local($A, $HitFlag, $Alias);

    # エイリアス
    $A = $cgi'TAGS{'alias'};

    # マシンがマッチしたか
    #	0 ... エイリアスがマッチしない
    #	2 ... マッチしてデータを変更した
    $HitFlag = 0;

    # エイリアスの読み込み
    &CashAliasData;
    
    # 1行ずつチェック
    foreach $Alias (sort keys(%Name)) {
	next if ($A ne $Alias);
	$HitFlag = 2;		# ヒットしたら2を設定．マシン名は無視．
    }
    
    # エイリアスがない!
    if ($HitFlag == 0) { &Fatal(6, $A); }
    
    # 名前を消す
    $Name{$A} = '';
    
    # エイリアスファイルに書き出し
    &WriteAliasData;
    
    # 表示画面の作成
    &MsgHeader('Alias deleted', "$H_ALIASが削除されました");
    &cgiprint'Cache("<p>$H_ALIAS: <strong>$A</strong>: 消去しました．</p>\n");
    &MsgFooter;

}


###
## AliasShow - ユーザエイリアス参照画面の表示
#
# - SYNOPSIS
#	AliasShow;
#
# - ARGS
#	なし
#
# - DESCRIPTION
#	ユーザエイリアスの一覧を表示する画面を作成する．
#
# - RETURN
#	なし
#
sub AliasShow {

    local($Alias);

    # エイリアスの読み込み
    &CashAliasData;
    
    # 表示画面の作成
    &MsgHeader('Alias view', "$H_ALIASの参照");

    # あおり文
    if ($SYS_ALIAS == 1) {
	&cgiprint'Cache(<<__EOF__);
<p>
投稿の際，「$H_FROM」の部分に以下の登録名(「#....」)を入力すると，
登録されている$H_FROMと$H_MAIL，$H_URLが自動的に補われます．
</p><p>
<a href="$PROGRAM?c=an">新規登録/登録内容の変更</a>
</p>
__EOF__

    } elsif ($SYS_ALIAS == 2) {
					  
	&cgiprint'Cache(<<__EOF__);
<p>
投稿の際，「$H_USER」で以下の登録名(「#....」)を指定すると，
登録されている$H_FROMと$H_MAIL，$H_URLが自動的に補われます．
</p><p>
<a href="$PROGRAM?c=an">新規登録/登録内容の変更</a>
</p>
__EOF__

    } else {
	# ありえない，はず
	&Fatal(9999, '');
    }

    # リスト開く
    &cgiprint'Cache("<dl>\n");
    
    # 1つずつ表示
    foreach $Alias (sort keys(%Name)) {
	&cgiprint'Cache(<<__EOF__);
<p>
<dt><strong>$Alias</strong>
<dd>$H_FROM: $Name{$Alias}
<dd>$H_MAIL: $Email{$Alias}
<dd>$H_URL: $URL{$Alias}
</p>
__EOF__

    }

    # リスト閉じる
    &cgiprint'Cache("</dl>\n");
    
    &MsgFooter;

}


###
## DeletePreview - 削除記事の確認
#
# - SYNOPSIS
#	DeletePreview;
#
# - ARGS
#	なし
#
# - DESCRIPTION
#	削除記事の確認画面を表示する
#       大域変数である，CGI変数を参照する．
#
# - RETURN
#	なし
#
sub DeletePreview {

    local($Id);

    $Id = $cgi'TAGS{'id'};

    # 表示画面の作成
    &MsgHeader("Delete Article", "$BOARDNAME: $H_MESGの削除");

    &cgiprint'Cache(<<__EOF__);
<p>
本当にこの$H_MESGを削除するのですね? よろしければボタンを押してください．
</p>
__EOF__

    # お約束
    &cgiprint'Cache(<<__EOF__);
<form action="$PROGRAM" method="POST">
<input name="c" type="hidden" value="de">
<input name="b" type="hidden" value="$BOARD">
<input name="id" type="hidden" value="$Id">
<input type="submit" value="この記事を削除します">
</form>
<form action="$PROGRAM" method="POST">
<input name="c" type="hidden" value="det">
<input name="b" type="hidden" value="$BOARD">
<input name="id" type="hidden" value="$Id">
<input type="submit" value="リプライ記事もまとめて削除します">
</form>
</p>
<hr>
__EOF__

    # 削除ファイルの表示
    &ViewOriginalArticle($Id, 0, 1);

    # お約束
    &MsgFooter;

}


###
## DeleteExec - 記事の削除
#
# - SYNOPSIS
#	DeleteExec($ThreadFlag);
#
# - ARGS
#	$ThreadFlag	リプライも消すか否か
#
# - DESCRIPTION
#	記事の削除を実行し，削除後の画面を表示する．
#       大域変数である，CGI変数を参照する．
#
# - RETURN
#	なし
#
sub DeleteExec {
    local($ThreadFlag) = @_;
    local($Id);

    $Id = $cgi'TAGS{'id'};

    # 削除実行
    &DeleteArticle($Id, $ThreadFlag);

    # 表示画面の作成
    &MsgHeader('Message deleted', "$BOARDNAME: $H_MESGが削除されました");

    &cgiprint'Cache(<<__EOF__);
<form action="$PROGRAM" method="POST">
<input name="b" type="hidden" value="$BOARD">
<input name="c" type="hidden" value="v">
<input name="num" type="hidden" value="$DEF_TITLE_NUM">
<input type="submit" value="$H_BACKTITLE">
</form>
__EOF__

    # お約束
    &MsgFooter;

}


###
## ArriveMailEntry - メイル自動配信先の指定
#
# - SYNOPSIS
#	ArriveMailEntry;
#
# - ARGS
#	なし
#
# - DESCRIPTION
#	メイル自動配信先の指定画面を表示する．
#
# - RETURN
#	なし
#
sub ArriveMailEntry {

    local(@ArriveMail);

    &getArriveMailTo(1, $BOARD, *ArriveMail); # 宛先とコメントを取り出す

    &MsgHeader("ArriveMail Entry", "$BOARDNAME: 自動メイル配信先の設定");

    &cgiprint'Cache(<<__EOF__);
<p>
この$H_BOARDに$H_MESGが書き込まれた時に，
自動でメイルを配信する宛先のメイルアドレスを設定します．
1行に1メイルアドレスずつ書き込んでください．
行頭に「#」をつけるとその行は無視されるので，
#に続けてコメントを書き込むこともできます．
</p><p>
特に実害はありませんが，無意味な空行が入りすぎないように注意しましょう．
</p><p>
<form action="$PROGRAM" method="POST">
<input name="c" type="hidden" value="me">
<input name="b" type="hidden" value="$BOARD">
<textarea name="armail" rows="$TEXT_ROWS" cols="$MAIL_LENGTH">
__EOF__

    foreach(@ArriveMail) { &cgiprint'Cache($_); }

    &cgiprint'Cache(<<__EOF__);
</textarea><br>
<input type="submit" value="設定します">
<input type="reset" value="リセットする">
</form>
</p>
__EOF__

    &MsgFooter;

}



###
## ArriveMailExec - メイル自動配信先の設定
#
# - SYNOPSIS
#	ArriveMailExec;
#
# - ARGS
#	なし
#
# - DESCRIPTION
#	メイル自動配信先を設定する．
#	大域変数である，CGI変数を参照する．
#
# - RETURN
#	なし
#
sub ArriveMailExec {

    local(@ArriveMail);

    @ArriveMail = split(/\n/, $cgi'TAGS{'armail'}); # 宛先リストを取り出す
    &updateArriveMailDb($BOARD, *ArriveMail); # DBを更新する

    &MsgHeader("ArriveMail Changed", "$BOARDNAME: 自動メイル配信先を設定しました");

    &cgiprint'Cache(<<__EOF__);
<p>
この$H_BOARDに$H_MESGが書き込まれた時に，自動でメイルを配信する宛先を，
以下のように設定しました．
</p><p>
<pre>
--------------------
__EOF__

    foreach(@ArriveMail) { &cgiprint'Cache("$_\n"); }

    &cgiprint'Cache(<<__EOF__);
--------------------
</pre></p>
<form action="$PROGRAM" method="POST">
<input name="b" type="hidden" value="$BOARD">
<input name="c" type="hidden" value="v">
<input name="num" type="hidden" value="$DEF_TITLE_NUM">
<input type="submit" value="$H_BACKTITLE">
</form>
__EOF__

    &MsgFooter;

}


######################################################################
# ユーザインタフェイスインプリメンテーション(共通部)


###
## Fatal - エラー表示
#
# - SYNOPSIS
#	Fatal($FatalNo, $FatalInfo);
#
# - ARGS
#	$FatalNo	エラー番号(詳しくは関数内部を参照のこと)
#	$FatalInfo	エラー情報
#
# - DESCRIPTION
#	エラーを表す画面をブラウザに送信する．
#
# - RETURN
#	なし
#
sub Fatal {
    local($FatalNo, $FatalInfo) = @_;
    local($ErrString);

    if ($FatalNo == 1) {

	$ErrString = "File: $FatalInfoが存在しない，あるいはpermissionの設定が間違っています．お手数ですが，<a href=\"mailto:$MAINT\">$MAINT</a>まで，上記ファイル名をお知らせ下さい．";

    } elsif ($FatalNo == 2) {

	$ErrString = "入力されていない項目があります．戻ってもう一度やり直してみてください．";

    } elsif ($FatalNo == 3) {

	$ErrString = "題や名前，メイルアドレスに，タブ文字か改行が入ってしまっています．戻ってもう一度やり直してみてください．";

    } elsif ($FatalNo == 4) {

	$ErrString = "題中にHTMLタグ，タブ文字，改行文字を入れることは禁じられています．戻って違う題に書き換えてください．";

    } elsif ($FatalNo == 5) {

	$ErrString = "登録されているエイリアスのものと，マシン名が一致しません．お手数ですが，<a href=\"mailto:$MAINT\">$MAINT</a>まで御連絡ください．";

    } elsif ($FatalNo == 6) {

	$ErrString = "「$FatalInfo」というエイリアスは，登録されていません．";

    } elsif ($FatalNo == 7) {

	$ErrString = "$FatalInfoがおかしくありませんか? 戻ってもう一度やり直してみてください．";

    } elsif ($FatalNo == 8) {

	$ErrString = "次の記事はまだ投稿されていません．";

    } elsif ($FatalNo == 9) {

	$ErrString = "メイルが送信できませんでした．お手数ですが，このエラーメッセージと，エラーが生じた状況を，<a href=\"mailto:$MAINT\">$MAINT</a>までお知らせください．";

    } elsif ($FatalNo == 10) {

	$ErrString = ".dbと.articleidの整合性が取れていません．お手数ですが，このエラーメッセージと，エラーが生じた状況を，<a href=\"mailto:$MAINT\">$MAINT</a>までお知らせください．";

    } elsif ($FatalNo == 11) {

	$ErrString = "$FatalInfoというIDに対応する$H_BOARDは，存在しません．";

    } elsif ($FatalNo == 50) {

	$ErrString = "リプライ関係が循環してしまいます．どうしてもリプライ先を変更したい場合，リプライ先を一度新着扱いにしてから，リプライをかけかえてください．";

    } elsif ($FatalNo == 99) {

	$ErrString ="この$H_BOARDでは，このコマンドは実行できません．";

    } elsif ($FatalNo == 999) {

	$ErrString ="システムのロックに失敗しました．混み合っているようですので，数分待ってからもう一度アクセスしてください．何度アクセスしてもロックされている場合，メンテナンス中である可能性もあります．";

    } else {

	$ErrString = "エラー番号不定: $FatalInfo<br>お手数ですが，このエラーメッセージと，エラーが生じた状況を，<a href=\"mailto:$mEmail\">$mEmail</a>までお知らせください．";

    }

    # 異常終了の可能性があるので，とりあえずlockを外す
    # (ロックの失敗の時以外)
    if ($FatalNo != 999) { &cgi'unlock($LOCK_FILE); }

    # 表示画面の作成
    &MsgHeader('Error!', "$SYSTEM_NAME: ERROR!");

    &cgiprint'Cache("<p>$ErrString</p>\n");

    if ($SYS_F_V && ($BOARD ne '')) {
	&cgiprint'Cache(<<__EOF__);
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


###
## ViewOriginalArticle - 元記事の表示
#
# - SYNOPSIS
#	ViewOriginalArticle($Id, $CommandFlag, $OriginalFlag);
#
# - ARGS
#	$Id			記事ID
#	$CommandFlag		コマンドを表示するか否か(表示する=1)
#	$OriginalFlag		その記事中に，(あれば)元記事へのリンクを
#				表示するか否か(表示する=1)
#
# - DESCRIPTION
#	元記事を表示する．
#
# - RETURN
#	なし
#
sub ViewOriginalArticle {
    local($Id, $CommandFlag, $OriginalFlag) = @_;
    local($Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $PrevId, $NextId, $Num, $InputDate, @ArticleBody);

    ($Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url) = &GetArticlesInfo($Id);

    foreach ($[ .. $#DB_ID) { $Num = $_, last if ($DB_ID[$_] eq $Id); }
    $PrevId = $DB_ID[$Num - 1] if ($Num > $[);
    $NextId = $DB_ID[$Num + 1];

    # コマンド表示?
    if ($CommandFlag && $SYS_COMMAND) {

	&cgiprint'Cache("<p>\n");

	if ($SYS_COMICON == 2) {

	    if ($SYS_F_B) {
		&cgiprint'Cache("<a href=\"$BOARDLIST_URL\"><img src=\"$ICON_BLIST\" alt=\"$H_BACKBOARD\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\">$H_BACKBOARD</a>\n");
	    }

	    if ($SYS_F_V) {
		&cgiprint'Cache(" | <a href=\"$PROGRAM?b=$BOARD&c=v&num=$DEF_TITLE_NUM\"><img src=\"$ICON_TLIST\" alt=\"$H_BACKTITLE\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\">$H_BACKTITLE</a>\n");
	    }

	    if ($SYS_F_E) {
		if ($PrevId ne '') {
		    &cgiprint'Cache(" | <a href=\"$PROGRAM?b=$BOARD&c=e&id=$PrevId\"><img src=\"$ICON_PREV\" alt=\"$H_PREVARTICLE\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\">$H_PREVARTICLE</a>\n");
		} else {
		    &cgiprint'Cache(" | <img src=\"$ICON_PREV\" alt=\"$H_PREVARTICLE\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\">$H_PREVARTICLE\n");
		}

		if ($NextId ne '') {
		    &cgiprint'Cache(" | <a href=\"$PROGRAM?b=$BOARD&c=e&id=$NextId\"><img src=\"$ICON_NEXT\" alt=\"$H_NEXTARTICLE\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\">$H_NEXTARTICLE</a>\n");
		} else {
		    &cgiprint'Cache(" | <img src=\"$ICON_NEXT\" alt=\"$H_NEXTARTICLE\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\">$H_NEXTARTICLE\n");
		}
	    }

	    if ($SYS_F_T) {
		if ($Aids ne '') {
		    &cgiprint'Cache(" | <a href=\"$PROGRAM?b=$BOARD&c=t&id=$Id\"><img src=\"$ICON_THREAD\" alt=\"$H_READREPLYALL\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\">$H_READREPLYALL</a>\n");
		} else {
		    &cgiprint'Cache(" | <img src=\"$ICON_THREAD\" alt=\"$H_READREPLYALL\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\">$H_READREPLYALL\n");
		}
	    }

	    if ($SYS_F_N) {
		&cgiprint'Cache(" | <a href=\"$PROGRAM?b=$BOARD&c=n\"><img src=\"$ICON_WRITENEW\" alt=\"$H_POSTNEWARTICLE\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\">$H_POSTNEWARTICLE</a>\n");
	    }    

	    if ($SYS_F_FQ) {
		&cgiprint'Cache(<<__EOF__);
 | <a href="$PROGRAM?b=$BOARD&c=f&id=$Id"><img src="$ICON_FOLLOW" alt="$H_REPLYTHISARTICLE" width="$COMICON_WIDTH" height="$COMICON_HEIGHT" BORDER="0">$H_REPLYTHISARTICLE</a>
 | <a href="$PROGRAM?b=$BOARD&c=q&id=$Id"><img src="$ICON_QUOTE" alt="$H_REPLYTHISARTICLEQUOTE" width="$COMICON_WIDTH" height="$COMICON_HEIGHT" BORDER="0">$H_REPLYTHISARTICLEQUOTE</a>
__EOF__
	    }

	    &cgiprint'Cache(" | <a href=\"$PROGRAM?b=$BOARD&c=i&type=article\"><img src=\"$ICON_HELP\" alt=\"?\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\">?</a>\n");

	} elsif ($SYS_COMICON == 1) {

	    if ($SYS_F_B) {
		&cgiprint'Cache("<a href=\"$BOARDLIST_URL\"><img src=\"$ICON_BLIST\" alt=\"$H_BACKBOARD\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\"></a>\n");
	    }

	    if ($SYS_F_V) {
		&cgiprint'Cache("<a href=\"$PROGRAM?b=$BOARD&c=v&num=$DEF_TITLE_NUM\"><img src=\"$ICON_TLIST\" alt=\"$H_BACKTITLE\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\"></a>\n");
	    }

	    if ($SYS_F_E) {
		if ($PrevId ne '') {
		    &cgiprint'Cache("<a href=\"$PROGRAM?b=$BOARD&c=e&id=$PrevId\"><img src=\"$ICON_PREV\" alt=\"$H_PREVARTICLE\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\"></a>\n");
		} else {
		    &cgiprint'Cache("<img src=\"$ICON_PREV\" alt=\"$H_PREVARTICLE\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\">\n");
		}

		if ($NextId ne '') {
		    &cgiprint'Cache("<a href=\"$PROGRAM?b=$BOARD&c=e&id=$NextId\"><img src=\"$ICON_NEXT\" alt=\"$H_NEXTARTICLE\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\"></a>\n");
		} else {
		    &cgiprint'Cache("<img src=\"$ICON_NEXT\" alt=\"$H_NEXTARTICLE\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\">\n");
		}
	    }

	    if ($SYS_F_T) {
		if ($Aids ne '') {
		    &cgiprint'Cache("<a href=\"$PROGRAM?b=$BOARD&c=t&id=$Id\"><img src=\"$ICON_THREAD\" alt=\"$H_READREPLYALL\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\"></a>\n");
		} else {
		    &cgiprint'Cache("<img src=\"$ICON_THREAD\" alt=\"$H_READREPLYALL\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\">\n");
		}
	    }

	    &cgiprint'Cache(" // \n");

	    if ($SYS_F_N) {
		&cgiprint'Cache(<<__EOF__);
<a href="$PROGRAM?b=$BOARD&c=n"><img src="$ICON_WRITENEW" alt="$H_POSTNEWARTICLE" width="$COMICON_WIDTH" height="$COMICON_HEIGHT" BORDER="0"></a>
__EOF__
	    }    

	    if ($SYS_F_FQ) {
		&cgiprint'Cache(<<__EOF__);
<a href="$PROGRAM?b=$BOARD&c=f&id=$Id"><img src="$ICON_FOLLOW" alt="$H_REPLYTHISARTICLE" width="$COMICON_WIDTH" height="$COMICON_HEIGHT" BORDER="0"></a>
<a href="$PROGRAM?b=$BOARD&c=q&id=$Id"><img src="$ICON_QUOTE" alt="$H_REPLYTHISARTICLEQUOTE" width="$COMICON_WIDTH" height="$COMICON_HEIGHT" BORDER="0"></a>
__EOF__
	    }

	    &cgiprint'Cache(" // \n");

	    &cgiprint'Cache("<a href=\"$PROGRAM?b=$BOARD&c=i&type=article\"><img src=\"$ICON_HELP\" alt=\"?\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\"></a>\n");

	} else {

	    if ($SYS_F_B) {
		&cgiprint'Cache("<a href=\"$BOARDLIST_URL\">$H_BACKBOARD</a>\n");
	    }

	    if ($SYS_F_V) {
		&cgiprint'Cache(" | <a href=\"$PROGRAM?b=$BOARD&c=v&num=$DEF_TITLE_NUM\">$H_BACKTITLE</a>\n");
	    }

	    if ($SYS_F_E) {
		if ($PrevId ne '') {
		    &cgiprint'Cache(" | <a href=\"$PROGRAM?b=$BOARD&c=e&id=$PrevId\">$H_PREVARTICLE</a>\n");
		} else {
		    &cgiprint'Cache(" | $H_PREVARTICLE\n");
		}

		if ($NextId ne '') {
		    &cgiprint'Cache(" | <a href=\"$PROGRAM?b=$BOARD&c=e&id=$NextId\">$H_NEXTARTICLE</a>\n");
		} else {
		    &cgiprint'Cache(" | $H_NEXTARTICLE\n");
		}
	    }

	    if ($SYS_F_T) {
		if ($Aids ne '') {
		    &cgiprint'Cache(" | <a href=\"$PROGRAM?b=$BOARD&c=t&id=$Id\">$H_READREPLYALL</a>");
		} else {
		    &cgiprint'Cache(" | $H_READREPLYALL");
		}
	    }

	    if ($SYS_F_N) {
		&cgiprint'Cache(" | <a href=\"$PROGRAM?b=$BOARD&c=n\">$H_POSTNEWARTICLE</a>\n");
	    }

	    if ($SYS_F_FQ) {
		&cgiprint'Cache(<<__EOF__);
 | <a href="$PROGRAM?b=$BOARD&c=f&id=$Id">$H_REPLYTHISARTICLE</a>
 | <a href="$PROGRAM?b=$BOARD&c=q&id=$Id">$H_REPLYTHISARTICLEQUOTE</a>
__EOF__
	    }

	}

	&cgiprint'Cache("</p>\n");

    }

    &cgiprint'Cache("<p>\n");

    # ボード名と記事番号，題
    if (($Icon eq $H_NOICON) || ($Icon eq '')) {
	&cgiprint'Cache("<strong>$H_SUBJECT</strong>: <strong>$Id .</strong> $Subject");
    } else {
	&cgiprint'Cache(sprintf("<strong>$H_SUBJECT</strong>: <strong>$Id .</strong> <img src=\"%s\" alt=\"$Icon \" width=\"$MSGICON_WIDTH\" height=\"$MSGICON_HEIGHT\">$Subject", &GetIconURLFromTitle($Icon, $BOARD)));
    }

    # お名前
    if (($Url eq '') || ($Url eq 'http://')) {
	# 「http://だったら」というのは旧バージョンへの対処．そのうち削除する予定．
        # URLがない場合
        &cgiprint'Cache("<br>\n<strong>$H_FROM</strong>: $Name");
    } else {
        # URLがある場合
        &cgiprint'Cache("<br>\n<strong>$H_FROM</strong>: <a href=\"$Url\">$Name</a>");
    }

    # メイル
    if ($Email ne '') {
	&cgiprint'Cache(" <a href=\"mailto:$Email\">&lt;$Email&gt;</a>");
    }

    # マシン
    if ($SYS_SHOWHOST) {
	&cgiprint'Cache("<br>\n<strong>$H_HOST</strong>: $RemoteHost");
    }

    # 投稿日
    $InputDate = &GetDateTimeFormatFromUtc($Date);
    &cgiprint'Cache("<br>\n<strong>$H_DATE</strong>: $InputDate");

    # 反応元(引用の場合)
    if ($OriginalFlag && ($Fid ne '')) {
	&ShowLinksToFollowedArticle(split(/,/, $Fid));
    }

    # 切れ目
    &cgiprint'Cache("</p>\n$H_LINE\n");

    # 記事の中身
    &getArticleBody($Id, $BOARD, *ArticleBody);
    foreach(@ArticleBody) { &cgiprint'Cache($_); }

}


###
## QuoteOriginalArticle - 引用する(引用符あり)
#
# - SYNOPSIS
#	QuoteOriginalArticle($Id);
#
# - ARGS
#	$Id		記事ID
#
# - DESCRIPTION
#	記事を引用して表示する
#
# - RETURN
#	なし
#
sub QuoteOriginalArticle {
    local($Id) = @_;
    local($Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $pFid, $pAids, $pDate, $pSubject, $pIcon, $pRemoteHost, $pName, $QMark, @ArticleBody);

    # 元記事情報の取得
    ($Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name) = &GetArticlesInfo($Id);

    # 元記事のさらに元記事情報
    if ($Fid) {
	$Fid =~ s/,.*$//o;
	($pFid, $pAids, $pDate, $pSubject, $pIcon, $pRemoteHost, $pName) = &GetArticlesInfo($Fid);
    }

    # 引用
    &getArticleBody($Id, $BOARD, *ArticleBody);
    foreach(@ArticleBody) {
	s/[\&\"]//go;		# 引用のための変換
	s/<[^>]*>//go;		# 引用のための変換

	# デフォルトの引用文字列は「名前」 + 「 ] 」
	$QMark = "${Name}$DEFAULT_QMARK";

	# 元文のうち，引用部分には，新たに引用文字列を重ねない
	# 空行にも要らない
	if ((/^$/o) || (/^$pName\s*$DEFAULT_QMARK/)) { $QMark = ''; }

	# 引用文字列の表示
	&cgiprint'Cache(sprintf("%s%s", $QMark, $_));
    }
}


###
## QuoteOriginalArticleWithoutQMark - 引用する(引用符なし)
#
# - SYNOPSIS
#	QuoteOriginalArticleWithoutQMark($Id);
#
# - ARGS
#	$Id		記事ID
#
# - DESCRIPTION
#	記事を引用して表示する
#
# - RETURN
#	なし
#
sub QuoteOriginalArticleWithoutQMark {
    local($Id) = @_;
    local(@ArticleBody);

    &getArticleBody($Id, $BOARD, *ArticleBody);
    foreach(@ArticleBody) {
	s/[\&\"]//go;		# 引用のための変換
	s/<[^>]*>//go;		# 引用のための変換
	&cgiprint'Cache($_);
    }
}


###
## BoardHeader - 掲示板ヘッダの表示
#
# - SYNOPSIS
#	BoardHeader($Type);
#
# - ARGS
#	$Type	掲示板ヘッダのタイプ
#			'normal' ... 通常
#			'maint' .... 管理用
#
# - DESCRIPTION
#	掲示板のヘッダを表示する．
#
# - RETURN
#	なし
#
sub BoardHeader {
    local($Type) = @_;
    local(@BoardHeader);

    &getBoardHeader($BOARD, *BoardHeader);
    foreach(@BoardHeader) { &cgiprint'Cache($_); }

    if ($SYS_F_MT && ($Type eq 'normal')) {
	&cgiprint'Cache(<<__EOF__);
<p>
<ul>
<li><a href="$PROGRAM?c=vm&b=$BOARD&num=$DEF_TITLE_NUM">管理用のタイトル一覧画面へ</a>
</ul>
</p>
__EOF__
    } elsif ($Type eq 'maint') {
	&cgiprint'Cache("<p>\n<ul>\n");
	if ($SYS_F_AM) {
	    &cgiprint'Cache("<li><a href=\"$PROGRAM?c=mp&b=$BOARD\">自動メイル配信先を設定する</a>\n");
	}
	&cgiprint'Cache("<li><a href=\"$PROGRAM?c=v&b=$BOARD&num=$DEF_TITLE_NUM\">通常のタイトル一覧へ</a>\n</ul>\n</p>\n");
    }
}


###
## ShowLinksToFollowedArticle - 元記事情報の表示
#
# - SYNOPSIS
#	ShowLinksToFollowedArticle(@IdList);
#
# - ARGS
#	@IdList		リプライ記事IDのリスト(古いリプライほど末尾にくる)
#
# - DESCRIPTION
#	元記事情報を表示する．
#
# - RETURN
#	なし
#
sub ShowLinksToFollowedArticle {
    local(@IdList) = @_;
    local($Id, $Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name);

    # オリジナル記事
    if ($#IdList > 0) {
	$Id = $IdList[$#IdList];
	($Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name) = &GetArticlesInfo($Id);
	&cgiprint'Cache("<br>\n<strong>$H_ORIG_TOP:</strong> " . &GetFormattedTitle($Id, $BOARD, $Aids, $Icon, $Subject, $Name, $Date));
    }

    # 元記事
    $Id = $IdList[0];
    ($Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name) = &GetArticlesInfo($Id);
    &cgiprint'Cache("<br>\n<strong>$H_ORIG:</strong> " . &GetFormattedTitle($Id, $BOARD, $Aids, $Icon, $Subject, $Name, $Date));

}


###
## MsgHeader - HTML文書のヘッダ部分の表示
#
# - SYNOPSIS
#	MsgHeader($Title, $Message, $LastModified);
#
# - ARGS
#	$Title		HTML文書のTITLE(titleタグに入れるので，今のところ，
#			US-ASCIIのみしておいたほうが無難)
#	$Message	HTML文書のタイトル(本文内に表示する文字列)
#	$LastModified	最終更新時間
#
# - DESCRIPTION
#	HTML文書のヘッダ部分を表示する．
#
# - RETURN
#	なし
#
sub MsgHeader {
    local($Title, $Message, $LastModified) = @_;
    
    &cgi'Header($LastModified);

    &cgiprint'Init;
    &cgiprint'Cache(<<__EOF__);
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML i18n//EN">
<html>
<head>
<title>$Title</title>
<base href="http://$SERVER_NAME$SERVER_PORT_STRING$SYSDIR_NAME">
</head>
__EOF__

    &cgiprint'Cache("<body");
    if ($SYS_NETSCAPE_EXTENSION) {
	&cgiprint'Cache(" background=\"$BG_IMG\"") if $BG_IMG;
	&cgiprint'Cache(" bgcolor=\"$BG_COLOR\"") if $BG_COLOR;
	&cgiprint'Cache(" TEXT=\"$TEXT_COLOR\"") if $TEXT_COLOR;
	&cgiprint'Cache(" LINK=\"$LINK_COLOR\"") if $LINK_COLOR;
	&cgiprint'Cache(" ALINK=\"$ALINK_COLOR\"") if $ALINK_COLOR;
	&cgiprint'Cache(" VLINK=\"$VLINK_COLOR\"") if $VLINK_COLOR;
    }
    &cgiprint'Cache(">\n");

    &cgiprint'Cache(<<__EOF__);
<h1>$Message</h1>
<hr>
__EOF__

}


###
## MsgFooter - HTML文書のフッタ部分の表示
#
# - SYNOPSIS
#	MsgFooter;
#
# - ARGS
#	なし
#
# - DESCRIPTION
#	HTML文書のフッタ部分を表示する．
#
# - RETURN
#	なし
#
sub MsgFooter {

    &cgiprint'Cache(<<__EOF__);
<hr>
<address>
$ADDRESS
</address>
</body>
</html>
__EOF__

    &cgiprint'Flush;

}


###
## ArriveMail - 記事が到着したことをメイル
#
# - SYNOPSIS
#	ArriveMail($Name, $Subject, $Id, @To);
#
# - ARGS
#	$Name		新規記事投稿者名
#	$Subject	新規記事Subject
#	$Id		新規記事ID
#	@To		送信先E-Mail addrリスト
#
# - DESCRIPTION
#	記事が到着したことをメイルする．
#
# - RETURN
#	なし
#
sub ArriveMail {
    local($Name, $Subject, $Id, @To) = @_;
    local($MailSubject, $Message);

    $MailSubject = "An article was arrived.";

    $Message = "$SYSTEM_NAMEからのお知らせです．

「$BOARDNAME」に対して「$Name」さんから，
「$Subject」という題での書き込みがありました．

";

    if ($SYS_F_E) {
	$Message .= "お時間のある時に
$SCRIPT_URL?b=$BOARD&c=e&id=$Id
を御覧下さい．

";
    }

    $Message .= "では失礼します．";

    # メイル送信
    &SendMail($MailSubject, $Message, $Id, @To);

}


###
## FollowMail - 反応があったことをメイル
#
# - SYNOPSIS
#	FollowMail($Name, $Date, $Subject, $Id, $Fname, $Fsubject, $Fid, @To);
#
# - ARGS
#	$Name		新規記事投稿者名
#	$Date		リプライされた記事の書き込み時間
#	$Subject	新規記事Subject
#	$Id		新規記事ID
#	$Fname		リプライされた記事の投稿者名
#	$Fsubject	リプライされた記事のSubject
#	$Fid		リプライされた記事ID
#	@To		送信先E-Mail addrリスト
#
# - DESCRIPTION
#	リプライがあったことをメイルする．
#
# - RETURN
#	なし
#
sub FollowMail {
    local($Name, $Date, $Subject, $Id, $Fname, $Fsubject, $Fid, @To) = @_;
    local($MailSubject, $InputDate, $Message);
    
    $MailSubject = "The article was followed.";

    $InputDate = &GetDateTimeFormatFromUtc($Date);

    $Message = "$SYSTEM_NAMEからのお知らせです．

$InputDateに「$BOARDNAME」に対して「$Name」さんが書いた，
「$Subject」
";

    if ($SYS_F_E) {
	$Message .= "$SCRIPT_URL?b=$BOARD&c=e&id=$Id
";
    }

    $Message .= "に対して，
「$Fname」さんから
「$Fsubject」という題での反応がありました．

";

    if ($SYS_F_E) {
	$Message .= "お時間のある時に
$SCRIPT_URL?b=$BOARD&c=e&id=$Fid
を御覧下さい．

";
    }

    $Message .= "では失礼します．";

    # メイル送信
    &SendMail($MailSubject, $Message, $Fid, @To);

}


###
## SendMail - メイル送信
#
# - SYNOPSIS
#	SendMail($Subject, $Message, $Id, @To);
#
# - ARGS
#	$Subject	メイルのSubject文字列(日本語を入れないように!)
#	$Message	本文
#	$Id		引用するなら記事ID; なければ引用はなし
#	@To		宛先E-Mail addr.のリスト
#
# - DESCRIPTION
#	メイルを送信する．
#
# - RETURN
#	なし
#
sub SendMail {
    local($Subject, $Message, $Id, @To) = @_;
    local($ExtensionHeader, @ArticleBody);

    # 付加ヘッダの生成
    $ExtensionHeader = "X-Kb-System: $SYSTEM_NAME\n";
    if ($BOARDNAME && ($Id ne '')) {
	$ExtensionHeader .= "X-Kb-Board: $BOARDNAME\nX-Kb-Articleid: $Id\n";
    }

    # 引用記事
    if ($Id ne '') {

	# 区切り線
	$Message .= "\n--------------------\n";

	# 引用
	&getArticleBody($Id, $BOARD, *ArticleBody);
	foreach(@ArticleBody) {
	    s/<[^>]*>//go;	# タグは要らない
	    if ($_ ne '') { $Message .= &HTMLDecode($_); }
	}
    }

    # 送信する
    &Fatal(9, '') unless (&cgi'SendMail($MAINT_NAME, $MAINT, $Subject, $ExtensionHeader, $Message, @To));

}


######################################################################
# アプリケーションモデルインプリメンテーション


###
## MakeNewArticle - 新たに投稿された記事の生成
#
# - SYNOPSIS
#	MakeNewArticle($Board, $Id, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail);
#
# - ARGS
#	$Board		作成する記事が入る掲示板のID
#	$Id		リプライ元記事のID
#	$TextType	文書タイプ
#	$Name		投稿者名
#	$Email		投稿者E-Mail addr.
#	$Url		投稿者URL
#	$Icon		アイコンID
#	$Subject	Subject文字列
#	$Article	本文文字列
#	$Fmail		リプライがあった時にメイルで知らせるか否か('on'/'')
#
# - DESCRIPTION
#	投稿された記事を記事DBに整理する．
#
# - RETURN
#	なし
#
sub MakeNewArticle {
    local($Board, $Id, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail) = @_;
    local($ArticleId);

    # 入力された記事情報のチェック
    $Article = &CheckArticle($Board, $TextType, *Name, *Email, *Url, *Subject, *Icon, $Article);

    # 新しい記事番号を取得(まだ記事番号は増えてない)
    $ArticleId = &GetNewArticleId($Board);

    # 正規のファイルの作成
    &MakeArticleFile($TextType, $Article, $ArticleId, $Board);

    # 新しい記事番号を書き込む
    &WriteArticleId($ArticleId, $Board);

    # DBファイルに投稿された記事を追加
    # 通常の記事引用ならID
    &AddDBFile($ArticleId, $Board, $Id, $TIME, $Subject, $Icon, $REMOTE_HOST, $Name, $Email, $Url, $Fmail);

}


###
## SearchArticleKeyword - 記事の検索(本文)
#
# - SYNOPSIS
#	SearchArticleKeyword($Id, $Board, @KeyList);
#
# - ARGS
#	$Id		本文を検索する記事のID
#	$Board		掲示板ID
#	@KeyList	キーワードリスト
#
# - DESCRIPTION
#	指定された記事の本文を，キーワードでAND検索する．
#
# - RETURN
#	最初にキーワードとマッチした行．マッチしなかったら空を返す．
#
sub SearchArticleKeyword {
    local($Id, $Board, @KeyList) = @_;
    local(@NewKeyList, $Line, $Return, $Code, $ConvFlag, @ArticleBody);

    $ConvFlag = ($Id !~ /^\d+$/);

    &getArticleBody($Id, $Board, *ArticleBody);
    foreach(@ArticleBody) {
	$Line = $_;

	# コード変換
	if ($ConvFlag) {
	    $Code = &jcode'getcode(*Line);
	    &jcode'convert(*Line, 'euc', $Code, 'z');
	}

	# 検索
	@NewKeyList = ();
	foreach (@KeyList) {
	    if ($Line =~ /$_/i) {
		# マッチした! 1行目なら覚えとく
		$Return = $Line unless $Return;
	    } else {
		# まだ探さなきゃ……
		push(@NewKeyList, $_);
	    }
	}
	# 空なら抜け．
	last unless (@KeyList = @NewKeyList);
    }

    # まだ残ってたらアウト．空なら最初のマッチした行を返す．
    return((@KeyList) ? '' : $Return);

}


###
## Version Check - KINOBOARDSのDBファイルのヴァージョンチェック
#
# - SYNOPSIS
#	VersionCheck($FileType, $VersionString);
#
# - ARGS
#	$FileType		チェック対象のDBファイルのタイプ
#	$VersionString		ヴァージョンを表わす文字列
#
# - DESCRIPTION
#	KINOBOARDSで使われているDBファイルのヴァージョンチェックを行なう．
#	不整合が見られた場合には値は返さず，ブラウザにエラーを表す画面を返す．
#	今のところ特にチェックしていない
#	(初期から各DBファイルのフォーマットが変化していないため)．
#
# - RETURN
#	なし
#
sub VersionCheck {
    local($FileType, $VersionString) = @_;
    local($VersionId, $ReleaseId) = split(/\//, $VersionString);

    # no check now...

}


###
## CheckArticle - 入力された記事情報のチェック
#
# - SYNOPSIS
#	CheckArticle($Board, $TextType, *Name, *Email, *Url, *Subject, *Icon, $Article);
#
# - ARGS
#	$Board		掲示板ID
#	$TextType	文書タイプ
#	*Name		投稿者名
#	*Email		メイルアドレス
#	*Url		URL
#	*Subject	Subject
#	*Icon		アイコンID
#	$Article	本文
#
# - DESCRIPTION
#	入力された記事をチェックする
#
# - RETURN
#	本文
#
sub CheckArticle {
    local($Board, $TextType, *Name, *Email, *Url, *Subject, *Icon, $Article) = @_;
    local($Tmp);

    # エイリアスチェック
    if ($Name =~ /^\#.*$/o) {
        ($Tmp, $Email, $Url) = &GetUserInfo($Name);
	if ($Tmp eq '') { &Fatal(6, $Name); }
	$Name = $Tmp;
    } elsif ($SYS_ALIAS == 2) {
	# 必須のはずなのに，指定されたエイリアスが登録されていない
	&Fatal(6, $Name);
    }

    # 文字列チェック
    &CheckName(*Name);
    &CheckEmail(*Email);
    &CheckURL(*Url);
    &CheckSubject(*Subject);

    # 空チェック
    if ($Article eq '') { &Fatal(2, ''); }

    # アイコンのチェック; おかしけりゃ「無し」に設定．
    if (&GetIconURLFromTitle($Icon, $Board)) { $Icon = $H_NOICON; }

    # 記事中の"をエンコード
    $Article = &DQEncode($Article);

    return($Article);

}


###
## AliasCheck - ユーザエイリアスのチェック
#
# - SYNOPSIS
#	AliasCheck($A, $N, $E, $U);
#
# - ARGS
#	$A	エイリアス名
#	$N	名前
#	$E	E-Mail addr.
#	$U	URL
#
# - DESCRIPTION
#	ユーザエイリアスのデータ(エイリアス名，名前，E-Mail，URL)
#	をチェックする．
#
# - RETURN
#	なし
#
sub AliasCheck {
    local($A, $N, $E, $U) = @_;

    &CheckAlias(*A);
    &CheckName(*N);
    &CheckEmail(*E);
    &CheckURL(*U);
    
}


###
## CheckAlias - 文字列チェック: エイリアス
#
# - SYNOPSIS
#	CheckAlias(*String);
#
# - ARGS
#	*String		エイリアス文字列
#
# - DESCRIPTION
#	エイリアスの文字列チェックを行なう．
#	不正な文字列だったらエラー表示ルーチンへ．
#	(アプリケーション/GUIを分離したほうがいいかな?)
#
# - RETURN
#	なし
#
sub CheckAlias {
    local(*String) = @_;

    # 空チェック
    if (! $String) { &Fatal(2, ''); }

    # `#'で始まってる?
    ($String =~ (/^\#/)) || &Fatal(7, $H_ALIAS);

    # 1文字じゃだめ
    (length($String) > 1) || &Fatal(7, $H_ALIAS);

}


###
## CheckSubject - 文字列チェック: Subject
#
# - SYNOPSIS
#	CheckSubject(*String);
#
# - ARGS
#	*String		Subject文字列
#
# - DESCRIPTION
#	Subjectの文字列チェックを行なう．
#	不正な文字列だったらエラー表示ルーチンへ．
#	(アプリケーション/GUIを分離したほうがいいかな?)
#
# - RETURN
#	なし
#
sub CheckSubject {
    local(*String) = @_;

    # 空チェック
    if (! $String) { &Fatal(2, ''); }

    # タグをチェック
    if ($String =~ m/[<>\t\n]/o) { &Fatal(4, ''); }

}


###
## CheckName - 文字列チェック: 投稿者名
#
# - SYNOPSIS
#	CheckName(*String);
#
# - ARGS
#	*String		投稿者名文字列
#
# - DESCRIPTION
#	投稿者名の文字列チェックを行なう．
#	不正な文字列だったらエラー表示ルーチンへ．
#	(アプリケーション/GUIを分離したほうがいいかな?)
#
# - RETURN
#	なし
#
sub CheckName {
    local(*String) = @_;

    # 空チェック
    if (! $String) { &Fatal(2, ''); }

    # 改行コードをチェック
    if ($String =~ /[\t\n]/o) { &Fatal(3, ''); }

}


###
## CheckEmail - 文字列チェック: E-Mail addr.
#
# - SYNOPSIS
#	CheckEmail(*String);
#
# - ARGS
#	*String		E-Mail addr.文字列
#
# - DESCRIPTION
#	E-Mail addr.の文字列チェックを行なう．
#	不正な文字列だったらエラー表示ルーチンへ．
#	(アプリケーション/GUIを分離したほうがいいかな?)
#
# - RETURN
#	なし
#
sub CheckEmail {
    local(*String) = @_;

    if ($SYS_POSTERMAIL) {

	# 空チェック
	if ($String eq '') { &Fatal(2, ''); }

	# `@'が入ってなきゃアウト
	if ($String !~ (/@/)) { &Fatal(7, 'E-Mail'); }

    }

    # 改行コードをチェック
    if ($String =~ /[\t\n]/o) { &Fatal(3, ''); }

}


###
## CheckURL - 文字列チェック: URL
#
# - SYNOPSIS
#	CheckURL(*String);
#
# - ARGS
#	*String		URL文字列
#
# - DESCRIPTION
#	URLの文字列チェックを行なう．ただし空チェックだけ．
#	中身のチェックにはIsUrlを呼び出す．
#	不正な文字列だったらエラー表示ルーチンへ．
#	(アプリケーション/GUIを分離したほうがいいかな?)
#
# - RETURN
#	なし
#
sub CheckURL {
    local(*String) = @_;

    # http://だけの場合は空にしてしまう．
    if ($String =~ m!^http://$!oi) { $String = ''; }

    # URLの中身のチェック
    if (($String ne '') && (! &IsUrl($String))) { &Fatal(7, 'URL'); }

}


###
## IsUrl - URLの構造をチェック
#
# - SYNOPSIS
#	IsUrl($String);
#
# - ARGS
#	$String		URL文字列
#
# - DESCRIPTION
#	URLの文字列チェックを行なう．
#	予め指定された(@URL_SCHEME)Schemeのものであるか否かをチェック．
#	telnet接続等は，しない．
#
# - RETURN
#	正しいURLであれば1，そうでなければ0
#
sub IsUrl {
    local($String) = @_;
    local($Scheme, $IsUrl);

    $IsUrl = 0;
    foreach $Scheme (@URL_SCHEME) {
	if ($String =~ m!^$Scheme://!i) { $IsUrl = 1; }
    }

    return($IsUrl);

}


###
## GetFollowIdTree - リプライ記事の木構造を取得
#
# - SYNOPSIS
#	GetFollowIdTree($Id);
#
# - ARGS
#	$Id	記事ID
#
# - DESCRIPTION
#	指定された記事のリプライ記事を，そのIDの木構造フォーマットで取り出す．
#
#	例: * (←指定された記事)
#	    +--a
#	    |  +--b
#	    |  |  +--c
#	    |  |  +--d
#	    |  |
#	    |  +--e
#	    |     +--f
#	    +--g
#	       +--h
#
#	→ ( a ( b ( c d ) e ( f ) ) g ( h ) )
#
# - RETURN
#	木構造を表すリスト
#
sub GetFollowIdTree {
    local($Id) = @_;

    # 再帰的に木構造を取り出す．
    return('(', &GetFollowIdTreeMain($Id), ')');

}

sub GetFollowIdTreeMain {
    local($Id) = @_;
    local(@AidList, @Result, @ChildResult);

    # 再帰停止条件
    if ($Id eq '') { return(); }

    # フォロー記事取り出し
    @AidList = split(/,/, $DB_AIDS{$Id});

    # なけりゃ停止
    return($Id) unless @AidList;

    # 再帰
    @Result = ($Id, '(');
    @ChildResult = ();
    foreach (@AidList) {
	@ChildResult = &GetFollowIdTreeMain($_);
	if (@ChildResult) {
	    push(@Result, @ChildResult);
	}
    }
    return(@Result, ')');

}


###
## GetReplySubject - リプライSubjectの生成
#
# - SYNOPSIS
#	GetReplySubject($Id);
#
# - ARGS
#	$Id	記事ID
#
# - DESCRIPTION
#	あるIdの記事からSubjectを取ってきて，先頭に「Re:」を1つだけつけて返す．
#
# - RETURN
#	生成したSubject文字列
#
sub GetReplySubject {
    local($Id) = @_;
    local($dFid, $dAids, $dDate, $dSubject) = &GetArticlesInfo($Id);

    # 先頭に「Re:」がくっついてたら取り除く．
    $dSubject =~ s/^Re:\s*//oi;
    # 先頭に「Re: 」をくっつけて返す．
    return("Re: $dSubject");

}


###
## GetFormattedTitle - タイトルリストのフォーマット
#
# - SYNOPSIS
#	GetFormattedTitle($Id, $Board, $Aids, $Icon, $Title, $Name, $Date);
#
# - ARGS
#	$Id		記事ID
#	$Board		掲示板ID
#	$Aids		リプライ記事があるか否か
#	$Icon		記事アイコンID
#	$Title		記事のSubject
#	$Name		記事の投稿者名
#	$Date		記事の投稿日付(UTC)
#
# - DESCRIPTION
#	ある記事をタイトルリスト表示用にフォーマットする．
#
# - RETURN
#	フォーマットした文字列
#
sub GetFormattedTitle {
    local($Id, $Board, $Aids, $Icon, $Title, $Name, $Date) = @_;
    local($String, $InputDate, $IdStr, $Link, $Thread);

    $InputDate = &GetDateTimeFormatFromUtc(($Date || &GetModifiedTime($Id, $Board)));
    # タイトルがついてなかったら，Idをそのままタイトルにする．
    $Title = $Title || $Id;

    # 通常記事
    $IdStr = "<strong>$Id.</strong> ";

    if ($SYS_F_E) {
	$Link = "<a href=\"$PROGRAM?b=$Board&c=e&id=$Id\">$Title</a>";
    } else {
	$Link = "$Title";
    }

    $Thread = (($SYS_F_T && $Aids) ? " <a href=\"$PROGRAM?b=$Board&c=t&id=$Id\">$H_THREAD</a>" : '');

    if (($Icon eq $H_NOICON) || ($Icon eq '')) {
	$String = sprintf("$IdStr$Link$Thread [%s] $InputDate", ($Name || $MAINT_NAME));
    } else {
	$String = sprintf("$IdStr<img src=\"%s\" alt=\"$Icon \" width=\"$MSGICON_WIDTH\" height=\"$MSGICON_HEIGHT\">$Link$Thread [%s] $InputDate", &GetIconURLFromTitle($Icon, $Board), ($Name || $MAINT_NAME));
    }

    return($String);

}


###
## GetModifiedTime - ある記事の最終更新時刻(UTC)を取得
#
# - SYNOPSIS
#	GetModifiedTime($Id, $Board);
#
# - ARGS
#	$Id		記事ID
#	$Board		掲示板ID
#
# - DESCRIPTION
#	あるIDの記事から，最終更新UTCを取ってくる．
#
# - RETURN
#	その記事ファイルの最終更新時刻(UTC)
#
sub GetModifiedTime {
    local($Id, $Board) = @_;

    return($TIME - (-M &GetArticleFileName($Id, $Board)) * 86400);
    # 86400 = 24 * 60 * 60
}


###
## GetDateTimeFormatFromUtc - UTCから時間を表す文字列を取得
#
# - SYNOPSIS
#	GetDateTimeFormatFromUtc($Utc);
#
# - ARGS
#	$Utc		時刻(UTC)
#
# - DESCRIPTION
#	UTCを時分秒に分割し，フォーマットして文字列として返す．
#	古いバージョンのKINOBOARDSでは，
#	DB中に時刻を表す文字列(not UTC)がそのまま入っているが，
#	それが渡された場合(UTCでなかった場合)は，そのまま返す．
#
# - RETURN
#	時刻を表わす文字列
#
sub GetDateTimeFormatFromUtc {
    local($Utc) = @_;
    local($Sec, $Min, $Hour, $Mday, $Mon, $Year, $Wday, $Yday, $Isdst);

    # 古い時代のものらしい．
    if ($Utc !~ m/^\d+$/) { return($Utc); }

    # 変換
    ($Sec, $Min, $Hour, $Mday, $Mon, $Year, $Wday, $Yday, $Isdst) = localtime($Utc);
    return(sprintf("%d/%d(%02d:%02d)", $Mon + 1, $Mday, $Hour, $Min));

}


###
## GetUtcFromOldDateTimeFormat - 時刻のUTCへの正規化
#
# - SYNOPSIS
#	GetUtcFromOldDateTimeFormat($Time);
#
# - ARGS
#	$Time		時間を表わす文字列
#
# - DESCRIPTION
#	古いバージョンのKINOBOARDSでは，
#	DB中に時刻を表す文字列がそのまま(UTCでなく)入っている．
#	これが渡された場合は適当なUTC(854477921 = 97/01/29 03:58)を返す．
#	UTCが渡されたらそのままそのUTCを返す．
#
# - RETURN
#	時刻(UTC)
#
sub GetUtcFromOldDateTimeFormat {
    local($Time) = @_;

    # 新規らしい
    if ($Time =~ m/^\d+$/) { return($Time); }

    # 適当
    return(854477921);

}


###
## DQEncode/DQDecode - 特殊文字のEncodeとDecode
#
# - SYNOPSIS
#	DQEncode($Str);
#	DQDecode($Str);
#
# - ARGS
#	$Str	Encode/Decodeする文字列
#
# - DESCRIPTION
#	HTMLの特殊文字(", >, <, &)をEncode/Decodeする．
#
# - RETURN
#	Encode/Decodeした文字列
#
sub DQEncode {
    local($Str) = @_;

    $Str =~ s/\"/__dq__/go;
    $Str =~ s/\>/__gt__/go;
    $Str =~ s/\</__lt__/go;
    $Str =~ s/\&/__amp__/go;
    return($Str);
}

sub DQDecode {
    local($Str) = @_;

    $Str =~ s/__dq__/\"/go;
    $Str =~ s/__gt__/\>/go;
    $Str =~ s/__lt__/\</go;
    $Str =~ s/__amp__/\&/go;
    return($Str);
}


###
## HTMLEncode/HTMLDecode - 特殊文字のHTML用EncodeとDecode
#
# - SYNOPSIS
#	HTMLEncode($Str);
#	HTMLDecode($Str);
#
# - ARGS
#	$Str	HTML用Encode/Decodeする文字列
#
# - DESCRIPTION
#	HTMLの特殊文字(", >, <, &)をHTML用にEncode/Decodeする．
#
# - RETURN
#	Encode/Decodeした文字列
#
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
## ArticleEncode - 記事のEncode
#
# - SYNOPSIS
#	ArticleEncode($Article);
#
# - ARGS
#	$Article	Encodeする記事本文
#
# - DESCRIPTION
#	記事中のURL(<URL:〜>)を，リンクに変換する．
#
# - RETURN
#	Encodeされた文字列
#
sub ArticleEncode {
    local($Article) = @_;
    local($Return, $Url, $UrlMatch, $Str, @Cash);

    $Return = $Article;
    while ($Article =~ m/<URL:([^>]*)>/g) {
	$Url = $1;
	($UrlMatch = $Url) =~ s/\?/\\?/go;
	next if (grep(/^$UrlMatch$/, @Cash));
	push(@Cash, $Url);
	if (&IsUrl($UrlMatch)) {
	    $Str = "<a href=\"$Url\"><URL:$Url></a>";
	}
	$Return =~ s/<URL:$UrlMatch>/$Str/g;
    }

    &cgi'SecureHtml(*Return);

    return($Return);

}


###
## DeleteArticle - 記事の削除
#
# - SYNOPSIS
#	DeleteArticle($Id, $ThreadFlag);
#
# - ARGS
#	$Id		削除記事ID
#	$ThreadFlag	リプライも消すか否か
#
# - DESCRIPTION
#	削除すべき記事IDを収集した後，DBを更新する．
#
# - RETURN
#	なし
#
sub DeleteArticle {
    local($Id, $ThreadFlag) = @_;
    local($Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $dId, @Target, $TargetId);

    # 記事情報の取得
    ($Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url) = &GetArticlesInfo($Id);

    # データの書き換え(必要なら娘も)
    @Target = ($Id);
    foreach $TargetId (@Target) {
	foreach ($[ .. $#DB_ID) {
	    # IDを取り出す
	    $dId = $DB_ID[$_];
	    # フォロー記事リストの中から，削除する記事のIDを取り除く
	    $DB_AIDS{$dId} = join(',', grep((! /^$TargetId$/o), split(/,/, $DB_AIDS{$dId})));
	    # 元記事から削除記事のIDを取り除く
	    $DB_FID{$dId} = '' if ($DB_FID{$dId} eq $TargetId);
	    $DB_FID{$dId} =~ s/,$TargetId,.*$//;
	    $DB_FID{$dId} =~ s/^$TargetId,.*$//;
	    $DB_FID{$dId} =~ s/,$TargetId$//;
	    # 娘も対象とする
	    if ($ThreadFlag && ($dId eq $TargetId)) {
		push(Target, split(/,/, $DB_AIDS{$dId}));
	    }
	}
    }

    # DBを更新する．
    &deleteArticleFromDbFile($Board, *Target);
}


###
## SupersedeArticle - 記事を訂正する
#
# - SYNOPSIS
#	SupersedeArticle;
#
# - ARGS
#	なし
#
# - DESCRIPTION
#	記事を訂正する．
#
# - RETURN
#	なし
#
sub SupersedeArticle {
    local($Board, $Id, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail) = @_;
    local($SupersedeId, $File, $SupersedeFile);

    # 入力された記事情報のチェック
    $Article = &CheckArticle($Board, $TextType, *Name, *Email, *Url, *Subject, *Icon, $Article);

    # DBファイルを訂正
    $SupersedeId = &SupersedeDBFile($Board, $Id, $TIME, $Subject, $Icon, $REMOTE_HOST, $Name, $Email, $Url, $Fmail);

    # ex. 「100」→「100_5」
    $File = &GetArticleFileName($Id, $Board);
    $SupersedeFile = &GetArticleFileName(sprintf("%s_%s", $Id, $SupersedeId), $Board);
    rename($File, $SupersedeFile);

    # 正規のファイルの作成
    &MakeArticleFile($TextType, $Article, $Id, $Board);
}


###
## ReLinkExec - 記事のかけかえ実施
#
# - SYNOPSIS
#	ReLinkExec($FromId, $ToId, $Board);
#
# - ARGS
#	$FromId		かけかえ元記事ID
#	$ToId		かけかえ先記事ID
#	$Board		掲示板ID
#
# - DESCRIPTION
#	記事をリプライ-元記事関係をかけかえる．
#
# - RETURN
#	なし
#
sub ReLinkExec {
    local($FromId, $ToId, $Board) = @_;
    local($dId, @Daughters, $DaughterId);

    # 循環記事の禁止
    &FatalPriv(50, '') if (grep(/^$FromId$/, split(/,/, $DB_FID{$ToId})));

    # データ書き換え
    foreach ($[ .. $#DB_ID) {
	# IDを取り出す
	$dId = $DB_ID[$_];
	# フォロー記事リストの中から，移動する記事のIDを取り除く
	$DB_AIDS{$dId} = join(',', grep((! /^$FromId$/o), split(/,/, $DB_AIDS{$dId})));
    }

    # 必要なら娘をとりだしておく
    @Daughters = split(/,/, $DB_AIDS{$FromId}) if ($DB_FID{$FromId});

    # 該当記事のリプライ先を変更する
    if ($ToId eq '') {
	$DB_FID{$FromId} = '';
    } elsif ($DB_FID{$ToId} eq '') {
	$DB_FID{$FromId} = "$ToId";
    } else {
	$DB_FID{$FromId} = "$ToId,$DB_FID{$ToId}";
    }

    # 該当記事の娘についても，リプライ先を変更する
    while($DaughterId = shift(@Daughters)) {
	# 孫娘も……
	push(Daughters, split(/,/, $DB_AIDS{$DaughterId}));
	# 書き換え
	if (($DB_FID{$DaughterId} eq $FromId) || ($DB_FID{$DaughterId} =~ /^$FromId,/)) {
	    $DB_FID{$DaughterId} = $DB_FID{$FromId} ? "$FromId,$DB_FID{$FromId}" : "$FromId";
	} elsif (($DB_FID{$DaughterId} =~ /^(.*),$FromId$/) || ($DB_FID{$DaughterId} =~ /^(.*),$FromId,/)) {
	    $DB_FID{$DaughterId} = $DB_FID{$FromId} ? "$1,$FromId,$DB_FID{$FromId}" : "$1,$FromId";
	}
    }

    # リプライ先になった記事のフォロー記事群に追加する
    $DB_AIDS{$ToId} = ($DB_AIDS{$ToId} ne '') ? "$DB_AIDS{$ToId},$FromId" : "$FromId";

    # 記事DBを更新する
    &updateArticleDb($Board);
}


###
## ReOrderExec - 記事の移動実施
#
# - SYNOPSIS
#	ReOrderExec($FromId, $ToId, $Board);
#
# - ARGS
#	$FromId		移動元記事ID
#	$ToId		移動先記事ID
#	$Board		掲示板ID
#
# - DESCRIPTION
#	指定された記事を，指定された記事の次に移動する．
#
# - RETURN
#	なし
#
sub ReOrderExec {
    local($FromId, $ToId, $Board) = @_;
    local(@Move);

    # 移動する記事たちを集める
    @Move = ($FromId, &CollectDaughters($FromId));

    # 移動させる
    &reOrderArticleDb($Board, $ToId, *Move);

    # DB書き換えたので，キャッシュし直す
    &DbCash($Board);
}


###
## CollectDaughters - 娘ノードのリストを集める
#
# - SYNOPSIS
#	CollectDaughters($Id);
#
# - ARGS
#	$Id		記事ID
#
# - DESCRIPTION
#	娘ノードのリストを集める
#
# - RETURN
#	娘ノード集合のリスト
#
sub CollectDaughters {
    local($Id) = @_;
    local(@Return);

    foreach (split(/,/, $DB_AIDS{$Id})) {
	push(Return, $_);
	push(Return, &CollectDaughters($_)) if ($DB_AIDS{$_} ne '');
    }
    @Return;
}


###
## GetNewArticleId - 新着記事IDの決定
#
# - SYNOPSIS
#	GetNewArticleId($Board);
#
# - ARGS
#	$Board		掲示板ID
#
# - DESCRIPTION
#	従来の最新記事IDを1増やした，新しい記事番号を返す．
#
# - RETURN
#	新着記事のID
#
sub GetNewArticleId {
    local($Board) = @_;

    &getArticleId($Board) + 1;
}


######################################################################
# データインプリメンテーション


###
## DbCash - 記事DBの全読み込み
#
# - SYNOPSIS
#	DbCash($Board);
#
# - ARGS
#	$Board		掲示板ID
#
# - DESCRIPTION
#	主に起動時に呼び出され，記事DBの内容を大域変数にキャッシュする．
#
# - RETURN
#	なし
#
$BOARD_DB_CASH = 0;

sub DbCash {
    return if $BOARD_DB_CASH;

    local($Board) = @_;
    local($DBFile, $dId, $dFid, $dAids, $dDate, $dTitle, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail, $Count);

    # クリア
    @DB_ID = %DB_FID = %DB_AIDS = %DB_DATE = %DB_TITLE = %DB_ICON = %DB_REMOTEHOST = %DB_NAME = %DB_EMAIL = %DB_URL = %DB_FMAIL = ();

    $DBFile = &GetPath($Board, $DB_FILE_NAME);

    # 取り込み．
    open(DB, "<$DBFile") || &Fatal(1, $DBFile);
    while(<DB>) {

	# Version Check
	&VersionCheck('DB', $1), next if (m/^\# Kb-System-Id: ([^\/]*\/.*)$/o);
	next if (/^\#/o || /^$/o);
	chop;

	($dId, $dFid, $dAids, $dDate, $dTitle, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail) = split(/\t/, $_, 11);
	next if ($dId eq '');

	$DB_ID[$Count++] = $dId;
	$DB_FID{$dId} = $dFid;
	$DB_AIDS{$dId} = $dAids;
	$DB_DATE{$dId} = $dDate || &GetModifiedTime($dId, $Board);
	$DB_TITLE{$dId} = $dTitle || $dId;
	$DB_ICON{$dId} = $dIcon;
	$DB_REMOTEHOST{$dId} = $dRemoteHost;
	$DB_NAME{$dId} = $dName || $MAINT_NAME;
	$DB_EMAIL{$dId} = $dEmail;
	$DB_URL{$dId} = $dUrl;
	$DB_FMAIL{$dId} = $dFmail;

    }
    close(DB);

    $BOARD_DB_CASH = 1;		# cashed

}


###
## GetArticlesInfo - 記事DBの読み込み
#
# - SYNOPSIS
#	GetArticlesInfo($Id);
#
# - ARGS
#	$Id	記事ID
#
# - DESCRIPTION
#	記事DBを読み込んで，情報を取り出す．
#	実際はキャッシュから読み出すだけ．
#
# - RETURN
#	記事情報のリスト
#		リプライ元記事ID
#		この記事にリプライした記事のIDのリスト(「,」区切り)
#		投稿時間(UTC)
#		Subject
#		アイコンID
#		投稿ホスト
#		投稿者名
#		投稿者E-Mail
#		投稿者URL
#		リプライがあった時に投稿者にメイルを送るか否か
#
sub GetArticlesInfo {
    local($Id) = @_;

    return($DB_FID{$Id}, $DB_AIDS{$Id}, $DB_DATE{$Id}, $DB_TITLE{$Id}, $DB_ICON{$Id}, $DB_REMOTEHOST{$Id}, $DB_NAME{$Id}, $DB_EMAIL{$Id}, $DB_URL{$Id}, $DB_FMAIL{$Id});

}


###
## AddDBFile - 記事DBへの追加
#
# - SYNOPSIS
#	AddDBFile($Id, $Board, $Fid, $InputDate, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail);
#
# - ARGS
#	$Id		記事ID
#	$Board		掲示板ID
#	$Fid		リプライ元の記事ID
#	$InputDate	書き込み日付(UTC)
#	$Subject	Subject
#	$Icon		アイコンID
#	$RemoteHost	書き込みホスト(IP addr.かFQDNかはhttpサーバ次第)
#	$Name		投稿者名
#	$Email		投稿者E-Mail addr.
#	$Url		投稿者URL
#	$Fmail		リプライ時にメイルを送るか否か(''/'on')
#
# - DESCRIPTION
#	記事DBに記事を追加する．
#
# - RETURN
#	なし
#
sub AddDBFile {
    local($Id, $Board, $Fid, $InputDate, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail) = @_;
    local($dId, $dFid, $dAids, $dInputDate, $dSubject, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail, $mdName, $mdInputDate, $mdSubject, $mdId, $mName, $mSubject, $mId, $FidList, $FFid, $File, $TmpFile, @FollowMailTo, @FFid, @ArriveMail);

    # リプライ元のリプライ元，を取ってくる
    if ($Fid ne '') {
	($FFid) = &GetArticlesInfo($Fid);
	@FFid = split(/,/, $FFid);
    }

    $FidList = $Fid;

    $File = &GetPath($Board, $DB_FILE_NAME);
    $TmpFile = &GetPath($Board, "$DB_FILE_NAME.$TMPFILE_SUFFIX");
    open(DBTMP, ">$TmpFile") || &Fatal(1, $TmpFile);
    open(DB, "<$File") || &Fatal(1, $File);
    while(<DB>) {

	# Version Check
	&VersionCheck('DB', $1) if (m/^\# Kb-System-Id: ([^\/]*\/.*)$/o);
	print(DBTMP "$_"), next if (/^\#/o || /^$/o);
	chop;

	($dId, $dFid, $dAids, $dInputDate, $dSubject, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail) = split(/\t/, $_);
	
	# フォロー先記事が見つかったら，
	if (($dId ne '') && ($dId eq $Fid)) {

	    # その記事のフォロー記事IDリストに加える(カンマ区切り)
	    if ($dAids ne '') {$dAids .= ",$Id";} else {$dAids = $Id;}

	    # 元記事のフォロー先リストを取ってきて元記事を加え，
	    # 新記事のフォロー先リストを作る
	    if ($dFid ne '') {
		$FidList = "$dId,$dFid";
	    }

	    if ($SYS_MAIL) {
		# メイル送信のためにキャッシュ
		$mdName = $dName;
		$mdInputDate = $dInputDate;
		$mdSubject = $dSubject;
		$mdId = $dId;
		$mName = $Name;
		$mSubject = $Subject;
		$mId = $Id;
		if ($dFmail ne '') {
		    push(@FollowMailTo, $dEmail);
		}
	    }
	}

	# DBに書き加える
	printf(DBTMP "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n", $dId, $dFid, $dAids, $dInputDate, $dSubject, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail);

	# リプライ元のリプライ元，かつメイル送信の必要があれば，宛先を保存
	if ($SYS_MAIL && (@FFid) && $dFmail && $dEmail && (grep(/^$dId$/, @FFid)) && (! grep(/^$dEmail$/, @FollowMailTo))) {
	    push(@FollowMailTo, $dEmail);
	}
    }

    # 新しい記事のデータを書き加える．
    printf(DBTMP "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n", $Id, $FidList, '', $InputDate, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail);

    # close Files.
    close(DB);
    close(DBTMP);

    # DBを更新する
    rename($TmpFile, $File);

    # 必要なら投稿があったことをメイルする
    &getArriveMailTo(0, $Board, *ArriveMail);
    if (@ArriveMail) {
	&ArriveMail($Name, $Subject, $Id, @ArriveMail);
    }

    # 必要なら反応があったことをメイルする
    if (@FollowMailTo) {
	&FollowMail($mdName, $mdInputDate, $mdSubject, $mdId, $mName, $mSubject, $mId, @FollowMailTo);
    }

}


###
## updateArticleDb - 記事DBの全更新
#
# - SYNOPSIS
#	updateArticleDb($Board);
#
# - ARGS
#	$Board		掲示板ID
#
# - DESCRIPTION
#	記事DBを，新たな記事データで全更新する．
#	書き込む記事データはキャッシュされているもの．
#
# - RETURN
#	なし
#
sub updateArticleDb {
    local($Board) = @_;
    local($File, $TmpFile, $dId);

    $File = &GetPath($Board, $DB_FILE_NAME);
    $TmpFile = &GetPath($Board, "$DB_FILE_NAME.$TMPFILE_SUFFIX");
    open(DBTMP, ">$TmpFile") || &Fatal(1, $TmpFile);
    open(DB, "<$File") || &Fatal(1, $File);

    while(<DB>) {

	# Version Check
	&VersionCheck('DB', $1) if (m/^\# Kb-System-Id: ([^\/]*\/.*)$/o);

	print(DBTMP "$_"), next if (/^\#/o || /^$/o);

	# Idを取り出す
	chop; ($dId = $_) =~ s/\t.*$//;

	# DBに書き加える
	printf(DBTMP "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n", $dId, $DB_FID{$dId}, $DB_AIDS{$dId}, $DB_DATE{$dId}, $DB_TITLE{$dId}, $DB_ICON{$dId}, $DB_REMOTEHOST{$dId}, $DB_NAME{$dId}, $DB_EMAIL{$dId}, $DB_URL{$dId}, $DB_FMAIL{$dId});
    }

    # close Files.
    close(DB);
    close(DBTMP);

    # DBを更新する
    rename($TmpFile, $File);
}


###
## deleteArticleFromDbFile - 記事DBの更新
#
# - SYNOPSIS
#	deleteArticleFromDbFile($Board, *Target);
#
# - ARGS
#	$Board		掲示板ID
#	*Target		削除する記事IDのリスト
#
# - DESCRIPTION
#	記事DBから指定された記事群のエントリを削除する．
#
# - RETURN
#	なし
#
sub deleteArticleFromDbFile {
    local($Board, *Target) = @_;
    local($File, $TmpFile, $dId);

    $File = &GetPath($Board, $DB_FILE_NAME);
    $TmpFile = &GetlPath($Board, "$DB_FILE_NAME.$TMPFILE_SUFFIX");
    open(DBTMP, ">$TmpFile") || &Fatal(1, $TmpFile);
    open(DB, "<$File") || &Fatal(1, $File);

    while(<DB>) {

	# Version Check
	&VersionCheck('DB', $1) if (m/^\# Kb-System-Id: ([^\/]*\/.*)$/o);

	print(DBTMP "$_"), next if (/^\#/o || /^$/o);

	# Idを取り出す
	chop; ($dId = $_) =~ s/\t.*$//;

	# 該当記事はコメントアウト
	print(DBTMP "#") if (grep(/^$dId$/, @Target));
	printf(DBTMP "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n", $dId, $DB_FID{$dId}, $DB_AIDS{$dId}, $DB_DATE{$dId}, $DB_TITLE{$dId}, $DB_ICON{$dId}, $DB_REMOTEHOST{$dId}, $DB_NAME{$dId}, $DB_EMAIL{$dId}, $DB_URL{$dId}, $DB_FMAIL{$dId});

    }

    # close Files.
    close(DB);
    close(DBTMP);

    # DBを更新する
    rename($TmpFile, $File);
}


###
## reOrderArticleDb - 記事DBの順序変更
#
# - SYNOPSIS
#	reOrderArticleDb($Board, $Id, *Move);
#
# - ARGS
#	$Board		掲示板ID
#	$Id		移動先記事ID
#	*Move		移動する記事群のリストへのリファレンス
#
# - DESCRIPTION
#	指定された記事群を，指定された記事の下に移動する．
#	「下」がDB中で先か後かは，新着が上か下か，に依り異なる．
#
# - RETURN
#	なし
#
sub reOrderArticleDb {
    local($Board, $Id, *Move) = @_;
    local($File, $TmpFile, $dId, $TopFlag);

    # 先頭フラグ
    $TopFlag = 1;

    $File = &GetPath($Board, $DB_FILE_NAME);
    $TmpFile = &GetPath($Board, "$DB_FILE_NAME.$TMPFILE_SUFFIX");
    open(DBTMP, ">$TmpFile") || &Fatal(1, $TmpFile);
    open(DB, "<$File") || &Fatal(1, $File);

    while(<DB>) {

	# Version Check
	&VersionCheck('DB', $1) if (m/^\# Kb-System-Id: ([^\/]*\/.*)$/o);

	print(DBTMP "$_"), next if (/^\#/o);
	print(DBTMP "$_"), next if (/^$/o);

	# Idを取り出す
	chop; ($dId = $_) =~ s/\t.*$//;

	# 移動する奴は取り除く
	next if (grep(/^$dId$/, @Move));

	# 先頭にする時の処理(新着が下，の場合)
	if (($Id eq '') && ($SYS_BOTTOMTITLE == 1) && ($TopFlag == 1)) {
	    $TopFlag = 0;
	    foreach (@Move) {
		printf(DBTMP "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n", $_, $DB_FID{$_}, $DB_AIDS{$_}, $DB_DATE{$_}, $DB_TITLE{$_}, $DB_ICON{$_}, $DB_REMOTEHOST{$_}, $DB_NAME{$_}, $DB_EMAIL{$_}, $DB_URL{$_}, $DB_FMAIL{$_});
	    }
	}

	# 移動先がきたら，先に書き込む(新着が上，の場合)
	if (($SYS_BOTTOMTITLE == 0) && ($dId eq $Id)) {
	    foreach (@Move) {
		printf(DBTMP "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n", $_, $DB_FID{$_}, $DB_AIDS{$_}, $DB_DATE{$_}, $DB_TITLE{$_}, $DB_ICON{$_}, $DB_REMOTEHOST{$_}, $DB_NAME{$_}, $DB_EMAIL{$_}, $DB_URL{$_}, $DB_FMAIL{$_});
	    }
	}

	# DBに書き加える
	printf(DBTMP "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n", $dId, $DB_FID{$dId}, $DB_AIDS{$dId}, $DB_DATE{$dId}, $DB_TITLE{$dId}, $DB_ICON{$dId}, $DB_REMOTEHOST{$dId}, $DB_NAME{$dId}, $DB_EMAIL{$dId}, $DB_URL{$dId}, $DB_FMAIL{$dId});

	# 移動先がきたら，続けて書き込む(新着が下，の場合)
	if (($SYS_BOTTOMTITLE == 1) && ($dId eq $Id)) {
	    foreach (@Move) {
		printf(DBTMP "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n", $_, $DB_FID{$_}, $DB_AIDS{$_}, $DB_DATE{$_}, $DB_TITLE{$_}, $DB_ICON{$_}, $DB_REMOTEHOST{$_}, $DB_NAME{$_}, $DB_EMAIL{$_}, $DB_URL{$_}, $DB_FMAIL{$_});
	    }
	}

    }

    # 先頭にする時の処理(新着が上，の場合)
    if (($Id eq '') && ($SYS_BOTTOMTITLE == 0)) {
	foreach (@Move) {
	    printf(DBTMP "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n", $_, $DB_FID{$_}, $DB_AIDS{$_}, $DB_DATE{$_}, $DB_TITLE{$_}, $DB_ICON{$_}, $DB_REMOTEHOST{$_}, $DB_NAME{$_}, $DB_EMAIL{$_}, $DB_URL{$_}, $DB_FMAIL{$_});
	}
    }

    # close Files.
    close(DB);
    close(DBTMP);

    # DBを更新する
    rename($TmpFile, $File);
}


###
## MakeArticleFile - 記事本文DBへの追加
#
# - SYNOPSIS
#	MakeArticleFile($TextType, $Article, $Id, $Board);
#
# - ARGS
#	$TextType	文書タイプ
#	$Article	本文
#	$Id		記事ID
#	$Board		掲示板ID
#
# - DESCRIPTION
#	記事本文DB(掲示板IDと同じ名前のディレクトリ)の中に，
#	IDと同じ名前のファイルとして，記事本文を保存する．
#
# - RETURN
#	なし
#
sub MakeArticleFile {
    local($TextType, $Article, $Id, $Board) = @_;
    local($File) = &GetArticleFileName($Id, $Board);

    # ファイルを開く
    open(TMP, ">$File") || &Fatal(1, $File);

    # バージョン情報を書き出す
    printf(TMP "<!-- Kb-System-Id: %s/%s -->\n", $KB_VERSION, $KB_RELEASE);

    # TextType用前処理
    if ((! $SYS_TEXTTYPE) || ($TextType eq $H_PRE)) {
	print(TMP "<p><pre>");
    }

    # 記事; "をデコードし，セキュリティチェック
    $Article = &DQDecode($Article);
    $Article = &ArticleEncode($Article);
    print(TMP "$Article\n");

    # TextType用後処理
    if ((! $SYS_TEXTTYPE) || ($TextType eq $H_PRE)) {
	print(TMP "</pre></p>\n");
    }

    # 終了
    close(TMP);

}


###
## getArticleBody - 記事本文DBの読み込み
#
# - SYNOPSIS
#	getArticleBody($Id, $Board, *ArticleBody);
#
# - ARGS
#	$Id		記事ID
#	$BoardId	掲示板ID
#	*ArticleBody	本文各行を入れる配列変数へのリファレンス
#
# - DESCRIPTION
#	記事本文DB(掲示板IDと同じ名前のディレクトリ)の中の，
#	IDと同じ名前のファイルを読み出す．
#
# - RETURN
#	なし
#
sub getArticleBody {
    local($Id, $Board, *ArticleBody) = @_;
    local($QuoteFile);

    $QuoteFile = &GetArticleFileName($Id, $Board);
    open(TMP, "<$QuoteFile") || &Fatal(1, $QuoteFile);
    while(<TMP>) {
	&VersionCheck('Article', $1), next if (m/^<!-- Kb-System-Id: ([^\/]*\/.*) -->$/o);
	push(@ArticleBody, $_);
    }
    close(TMP);
    
}


###
## getArticleId - 記事番号DBの読み込み
#
# - SYNOPSIS
#	getArticleId($Board);
#
# - ARGS
#	$Board		掲示板ID
#
# - DESCRIPTION
#	従来の最新記事IDを読み出す．
#
# - RETURN
#	最新記事のID
#
sub getArticleId {
    local($Board) = @_;
    local($ArticleNumFile, $ArticleId);

    $ArticleNumFile = &GetPath($Board, $ARTICLE_NUM_FILE_NAME);
    open(AID, "<$ArticleNumFile") || &Fatal(1, $ArticleNumFile);
    chop($ArticleId = <AID>);
    close(AID);
    $ArticleId;
}


###
## WriteArticleId - 記事番号DBの更新
#
# - SYNOPSIS
#	WriteArticleId($Id, $Board);
#
# - ARGS
#	$Id		新規に書き込む記事番号
#	$Board		掲示板ID
#
# - DESCRIPTION
#	記事番号DBの更新
#
# - RETURN
#	なし
#
sub WriteArticleId {
    local($Id, $Board) = @_;
    local($File, $TmpFile, $OldArticleId);
    
    # 数字のくせに古い数値より若い! (数字じゃなきゃOK)
    $OldArticleId = &GetNewArticleId($Board);
    if (($Id =~ /^\d+$/) && ($Id < $OldArticleId)) {
	&Fatal(10, '');
    }

    $File = &GetPath($Board, $ARTICLE_NUM_FILE_NAME);
    $TmpFile = &GetPath($Board, "$ARTICLE_NUM_FILE_NAME.$TMPFILE_SUFFIX");
    open(AID, ">$TmpFile") || &Fatal(1, $TmpFile);
    print(AID "$Id\n");
    close(AID);

    # 更新
    rename($TmpFile, $File);

}


###
## getArriveMailTo - 掲示板別新規メイル送信先DBの全読み込み
#
# - SYNOPSIS
#	getArriveMailTo($CommentFlag, $Board, *ArriveMail);
#
# - ARGS
#	$CommentFlag	コメント行を含むか否か(0: 含まない, 1: 含む)
#	$Board		掲示板ID
#	*ArriveMail	送信先のメイルアドレスのリストのリファレンス
#
# - DESCRIPTION
#	掲示板別新規メイル送信先DBを，読み込む．
#	メイルアドレスが正しいか否か等のチェックは，一切行なわない．
#
# - RETURN
#	なし
#
sub getArriveMailTo {
    local($CommentFlag, $Board, *ArriveMail) = @_;
    local($ArriveMailFile);

    $ArriveMailFile = &GetPath($Board, $ARRIVEMAIL_FILE_NAME);
    # ファイルがなきゃ空のまま
    open(ARMAIL, "<$ArriveMailFile") || return;
    while(<ARMAIL>) {
    	# Version Check
	&VersionCheck('ARRIVEMAIL', $1), next if (m/^\# Kb-System-Id: ([^\/]*\/.*)$/o);
	next if ((! $CommentFlag) && (/^\#/o || /^$/o));
	chop;
	push(@ArriveMail, $_);
    }
    close(ARMAIL);
}


###
## updateArriveMailDb - 掲示板別新規メイル送信先DBの全更新
#
# - SYNOPSIS
#	updateArriveMailDb($Board, *ArriveMail);
#
# - ARGS
#	$Board		掲示板ID
#	*ArriveMail	送信先のメイルアドレスのリストのリファレンス
#			(コメント，空行も含まれる)
#
# - DESCRIPTION
#	掲示板別新規メイル送信先DBを，新たな送信先リストで一新する．
#	メイルアドレスが正しいか否か等のチェックは，一切行なわない．
#
# - RETURN
#	なし
#
sub updateArriveMailDb {
    local($Board, *ArriveMail) = @_;
    local($File, $TmpFile);

    $File = &GetPath($Board, $ARRIVEMAIL_FILE_NAME);
    $TmpFile = &GetPath($Board, $ARRIVEMAIL_FILE_NAME);
    open(DBTMP, ">$TmpFile") || &Fatal(1, $TmpFile);
    foreach (@ArriveMail) { print(DBTMP "$_\n"); }
    close(DBTMP);
    rename($TmpFile, $File);
}


###
## CashAliasData - ユーザDBの全読み込み
#
# - SYNOPSIS
#	CashAliasData;
#
# - ARGS
#	なし
#
# - DESCRIPTION
#	ユーザエイリアスファイルを読み込んで連想配列に放り込む．
#	大域変数，%Name, %Email, %Host, %URLを破壊する．
#
# - RETURN
#	なし
#
sub CashAliasData {

    local($A, $N, $E, $H, $U);

    # 放り込む．
    open(ALIAS, "<$USER_ALIAS_FILE") || &Fatal(1, $USER_ALIAS_FILE);
    while(<ALIAS>) {

	# Version Check
	&VersionCheck('Alias', $1), next if (m/^<!-- Kb-System-Id: ([^\/]*\/.*) -->$/o);
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
## GetUserInfo - ユーザDBの読み込み
#
# - SYNOPSIS
#	GetUserInfo($Alias);
#
# - ARGS
#	$Alias		検索するユーザID(エイリアス)
#
# - DESCRIPTION
#	ユーザDBから，ユーザの名前，メイル，URLを取ってくる．
#
# - RETURN
#	ユーザの名前，メイル，URLの順のリスト．
#
sub GetUserInfo {
    local($Alias) = @_;
    local($A, $N, $E, $H, $U, $rN, $rE, $rU);

    # ファイルを開く
    open(ALIAS, "<$USER_ALIAS_FILE") || &Fatal(1, $USER_ALIAS_FILE);
    
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
## WriteAliasData - ユーザDBの更新/追加
#
# - SYNOPSIS
#	WriteAliasData;
#
# - ARGS
#	なし
#
# - DESCRIPTION
#	ユーザエイリアスファイルにデータを書き出す．
#	%Name, %Email, %Host, %URLを必要とする．
#	$Nameが空だと書き込まない．
#
# - RETURN
#	なし
#
sub WriteAliasData {

    local($Alias, $TmpFile);

    $TmpFile = "$USER_ALIAS_FILE.$TMPFILE_SUFFIX";
    open(ALIAS, ">$TmpFile") || &Fatal(1, $TmpFile);

    # バージョン情報を書き出す
    printf(ALIAS "<!-- Kb-System-Id: %s/%s -->\n", $KB_VERSION, $KB_RELEASE);

    # 順に．
    foreach $Alias (sort keys(%Name)) {
	if ($Name{$Alias}) {
	    printf(ALIAS "%s\t%s\t%s\t%s\t%s\n", $Alias, $Name{$Alias}, $Email{$Alias}, $Host{$Alias}, $URL{$Alias});
	}
    }
    close(ALIAS);

    # 更新
    rename($TmpFile, $USER_ALIAS_FILE);
    
}


###
## getAllBoardInfo - 掲示板DBの全読み込み
#
# - SYNOPSIS
#	getAllBoardInfo(*BoardList, *BoardInfo);
#
# - ARGS
#	*BoardList	掲示板ID-掲示板名の連想配列のリファレンス
#	*BoardInfo	掲示板ID-掲示板情報の連想配列のリファレンス
#
# - DESCRIPTION
#	掲示板DBから，掲示板情報を取ってくる．
#
# - RETURN
#	なし
#
sub getAllBoardInfo {
    local(*BoardList, *BoardInfo) = @_;
    local($BoardId, $BName, $BInfo);

    open(ALIAS, "<$BOARD_ALIAS_FILE") || &Fatal(1, $BOARD_ALIAS_FILE);
    while(<ALIAS>) {

	# Version Check
	&VersionCheck('Board', $1), next if (m/^\# Kb-System-Id: ([^\/]*\/.*)$/o);
	next if (/^\#/o || /^$/o);
	chop;
	($BoardId, $BName, $BInfo) = split(/\t/, $_, 3);
	$BoardList{$BoardId} = $BName;
	$BoardInfo{$BoardId} = $BInfo;
    }
    close(ALIAS);
}


###
## GetBoardInfo - 掲示板DBの読み込み
#
# - SYNOPSIS
#	GetBoardInfo($Alias);
#
# - ARGS
#	$Alias		掲示板ID
#
# - DESCRIPTION
#	掲示板DBから，掲示板情報を取ってくる．
#
# - RETURN
#	掲示板名
#
sub GetBoardInfo {
    local($Alias) = @_;
    local($BoardName, $dAlias, $dBoardName);

    open(ALIAS, "<$BOARD_ALIAS_FILE") || &Fatal(1, $BOARD_ALIAS_FILE);
    while(<ALIAS>) {

	# Version Check
	&VersionCheck('Board', $1), next if (m/^\# Kb-System-Id: ([^\/]*\/.*)$/o);
	next if (/^\#/o || /^$/o);
	chop;
	($dAlias, $dBoardName) = split(/\t/, $_, 3);
	if ($Alias eq $dAlias) { $BoardName = $dBoardName; }
    }
    close(ALIAS);

    return($BoardName);

}


###
## cashIconDB - アイコンDBの全読み込み
#
# - SYNOPSIS
#	cashIconDB($Board);
#
# - ARGS
#	$Board		掲示板ID
#
# - DESCRIPTION
#	アイコンDBを読み込んで連想配列に放り込む．
#	大域変数，%ICON_FILE，%ICON_HELPを破壊する．
#
# - RETURN
#	なし
#
$ICON_DB_CASH = 0;

sub cashIconDB {
    return if $ICON_DB_CASH;

    local($Board) = @_;
    local($FileName, $IconTitle, $IconHelp);

    # キャッシュのクリア
    %ICON_FILE = %ICON_HELP = ();

    # 一つ一つ表示
    open(ICON, &GetIconPath("$Board.$ICONDEF_POSTFIX"))
	|| (open(ICON, &GetIconPath("$DEFAULT_ICONDEF"))
	    || &Fatal(1, &GetIconPath("$DEFAULT_ICONDEF")));
    while(<ICON>) {

	# Version Check
	&VersionCheck('Icon', $1), next if (m/^\# Kb-System-Id: ([^\/]*\/.*)$/o);
	next if (/^\#/o || /^$/o);
	chop;
	($FileName, $IconTitle, $IconHelp) = split(/\t/, $_, 3);

	# 取り込み
	$ICON_FILE{$IconTitle} = $FileName;
	$ICON_HELP{$IconTitle} = $IconHelp;
    }
    close(ICON);

    $ICON_DB_CASH = 1;		# cashed

}


###
## getBoardHeader - 掲示板ヘッダDBの読み込み
#
# - SYNOPSIS
#	getBoardHeader($Board, *BoardHeader);
#
# - ARGS
#	$BoardId	掲示板ID
#	*BoardHeader	本文各行を入れる配列変数へのリファレンス
#
# - DESCRIPTION
#	掲示板ディレクトリの中の，掲示板ヘッダファイルを読み出す．
#
# - RETURN
#	なし
#
sub getBoardHeader {
    local($Board, *BoardHeader) = @_;
    local($File);

    $File = &GetPath($Board, $BOARD_FILE_NAME);
    open(HEADER, "<$File") || &Fatal(1, $File);
    while(<HEADER>){
	# Version Check
	&VersionCheck('Header', $1), next if (m/^<!-- Kb-System-Id: ([^\/]*\/.*) -->$/o);
	push(@BoardHeader, $_);
    }
    close(HEADER);
    
}


###
## GetArticleFileName - 記事本文DBファイルのパス名の取得
#
# - SYNOPSIS
#	GetArticleFileName($Id, $Board);
#
# - ARGS
#	$Id		記事ID
#	$Board		掲示板ID
#
# - DESCRIPTION
#	掲示板IDと記事IDから，記事DB中の，記事ファイルのパス名を作り出す．
#	大域変数$ARCHを参照し，Mac/Win/UNIXに対応．
#
# - RETURN
#	パスを表す文字列
#
sub GetArticleFileName {
    local($Id, $Board) = @_;

    # Boardが空ならBoardディレクトリ内から相対，
    # 空でなければシステムから相対
    return(($Board) ? "$Board/$Id" : "$Id") if ($ARCH eq 'UNIX');
    return(($Board) ? "$Board/$Id" : "$Id") if ($ARCH eq 'WinNT');
    return(($Board) ? "$Board/$Id" : "$Id") if ($ARCH eq 'Win95');
    return(($Board) ? ":$Board:$Id" : "$Id") if ($ARCH eq 'Mac');

}


###
## GetPath - DBファイルのパス名の取得
#
# - SYNOPSIS
#	GetPath($Board, $File);
#
# - ARGS
#	$Board		掲示板ID
#	$File		ファイル名
#
# - DESCRIPTION
#	掲示板IDとファイル名から，その掲示板用のDBファイルのパス名を作り出す．
#	大域変数$ARCHを参照し，Mac/Win/UNIXに対応．
#
# - RETURN
#	パスを表す文字列
#
sub GetPath {
    local($Board, $File) = @_;

    # 返す
    return("$Board/$File") if ($ARCH eq 'UNIX');
    return("$Board/$File") if ($ARCH eq 'WinNT');
    return("$Board/$File") if ($ARCH eq 'Win95');
    return(":$Board:$File") if ($ARCH eq 'Mac');

}


###
## GetIconPath - アイコンgifDBファイルのパス名の取得
#
# - SYNOPSIS
#	GetIconPath($File);
#
# - ARGS
#	$File		アイコンgifファイル名
#
# - DESCRIPTION
#	アイコンgifファイルのパス名を作り出す．
#	大域変数$ARCHを参照し，Mac/Win/UNIXに対応．
#
# - RETURN
#	パスを表す文字列
#
sub GetIconPath {
    local($File) = @_;

    # 返す
    return("$ICON_DIR/$File") if ($ARCH eq 'UNIX');
    return("$ICON_DIR/$File") if ($ARCH eq 'WinNT');
    return("$ICON_DIR/$File") if ($ARCH eq 'Win95');
    return(":$ICON_DIR:$File") if ($ARCH eq 'Mac');

}


###
## GetIconURLFromTitle - アイコンgifのURLの取得
#
# - SYNOPSIS
#	GetIconURLFromTitle($Icon, $Board);
#
# - ARGS
#	$Icon		アイコンID
#	$Board		掲示板ID
#
# - DESCRIPTION
#	アイコンIDから，そのアイコンに対応するgifファイルのURLを取得．
#
# - RETURN
#	URLを表す文字列
#
sub GetIconURLFromTitle {
    local($Icon, $Board) = @_;
    local($FileName, $Title, $TargetFile);

    # 一つ一つ表示
    open(ICON, &GetIconPath("$Board.$ICONDEF_POSTFIX"))
	|| (open(ICON, &GetIconPath("$DEFAULT_ICONDEF"))
	    || &Fatal(1, &GetIconPath("$DEFAULT_ICONDEF")));
    while(<ICON>) {

	# Version Check
	&VersionCheck('Icon', $1), next if (m/^\# Kb-System-Id: ([^\/]*\/.*)$/o);
	next if (/^\#/o || /^$/o);
	chop;
	($FileName, $Title) = split(/\t/, $_, 3);
	if ($Title eq $Icon) { $TargetFile = $FileName;	}
    }
    close(ICON);

    return(($TargetFile) ? "$ICON_DIR/$TargetFile" : '');

}


###
## SupersedeDBFile - 訂正記事の記事DBへの書き込み
#
# - SYNOPSIS
#	SupersedeDBFile($Board, $Id, $InputDate, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail);
#
# - ARGS
#	$Board		訂正する記事が含まれる掲示板のID
#	$Id		訂正する記事のID
#	$InputDate	訂正時間(UTC)
#	$Subject	訂正記事Subject
#	$Icon		訂正記事アイコン
#	$RemoteHost	訂正記事書き込みホスト名
#	$Name		訂正記事書き込みユーザ名
#	$Email		訂正記事書き込みユーザメイルアドレス
#	$Url		訂正記事書き込みユーザURL
#	$Fmail		リプライ時にメイルを送信するか否か
#
# - DESCRIPTION
#	訂正記事をDBファイルに書き込み，agingした記事のIDを返す．
#
# - RETURN
#	agingした記事のID．
#
sub SupersedeDBFile {
    local($Board, $Id, $InputDate, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail) = @_;
    local($SupersedeId, $dId, $dFid, $dAids, $dInputDate, $dSubject, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail, $File, $TmpFile);
    
    # initial versionは1で，1ずつ増えていく．1，2，…9，10，11，…
    # later versionはDB中で必ず，younger versionよりも下に出現する．
    # すなわち10_2，10，10_1は，10_1，10_2，10の順に並ぶものとする．
    $SupersedeId = 1;

    $File = &GetPath($Board, $DB_FILE_NAME);
    $TmpFile = &GetPath($Board, "$DB_FILE_NAME.$TMPFILE_SUFFIX");
    open(DBTMP, ">$TmpFile") || &Fatal(1, $TmpFile);
    open(DB, "<$File") || &Fatal(1, $File);

    while(<DB>) {

	# Version Check
	&VersionCheck('DB', $1) if (m/^\# Kb-System-Id: ([^\/]*\/.*)$/o);

	print(DBTMP "$_"), next if (/^\#/o || /^$/o);
	chop;

	($dId, $dFid, $dAids, $dInputDate, $dSubject, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail) = split(/\t/, $_);

	# later versionが見つかったら，versionを先読みしておく．
	$SupersedeId++ if ("$dId" eq (sprintf("#-%s_%s", $Id, $SupersedeId)));

	# 訂正記事の最新版が見つかったら，
	if ($dId eq $Id) {

	    # agingしてしまう
	    printf(DBTMP "#-%s_%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n", $dId, $SupersedeId, $dFid, $dAids, $dInputDate, $dSubject, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail);

	    # 続いて新しい記事を書き加える
	    printf(DBTMP "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n", $Id, $dFid, $dAids, $InputDate, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail);

	} else {

	    # DBに書き加える
	    print(DBTMP "$_\n");

	}

    }

    # close Files.
    close(DB);
    close(DBTMP);

    # DBを更新する
    rename($TmpFile, $File);

    # 返す
    return($SupersedeId);

}
