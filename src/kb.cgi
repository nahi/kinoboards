#!/usr/local/bin/perl5
#
# $Id: kb.cgi,v 5.3 1997-09-12 14:30:07 nakahiro Exp $


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
$KB_RELEASE = '5.0';

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
$SYS_F_MT = ($SYS_F_D || $SYS_F_AM || $SYS_F_MV);
if (($SERVER_PORT != 80) && ($SYS_PORTNO == 1)) {
    $SERVER_PORT_STRING = ":$SERVER_PORT";
}
if ($TIME_ZONE) { $ENV{'TZ'} = $TIME_ZONE; }
if ($BOARDLIST_URL eq '-') { $BOARDLIST_URL = "$PROGRAM?c=bl"; }
$ADDRESS = sprintf("Maintenance: <a href=\"mailto:%s\">%s</a><br><a href=\"http://www.kinotrope.co.jp/~nakahiro/kb10.shtml\">KINOBOARDS/%s R%s</a>: Copyright (C) 1995, 96, 97 <a href=\"http://www.kinotrope.co.jp/~nakahiro/\">NAKAMURA Hiroshi</a>.", $MAINT, $MAINT_NAME, $KB_VERSION, $KB_RELEASE);

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
    &ShowArticle,	last if ($Command eq 'e');
    &ThreadArticle,	last if ($SYS_F_T && ($Command eq 't'));
    &Entry(0),		last if ($SYS_F_N && ($Command eq 'n'));
    &Entry(1),		last if ($SYS_F_N && ($Command eq 'f'));
    &Entry(2),		last if ($SYS_F_N && ($Command eq 'q'));
    &Preview,		last if ($SYS_F_N && ($Command eq 'p') && ($Com ne 'x'));
    &Thanks,		last if ($SYS_F_N && ($Command eq 'x'));
    &Thanks,		last if ($SYS_F_N && ($Command eq 'p') && ($Com eq 'x'));
    &ViewTitle(0),	last if ($Command eq 'v');
    &SortArticle,	last if ($SYS_F_R && ($Command eq 'r'));
    &NewArticle,	last if ($SYS_F_L && ($Command eq 'l'));
    &SearchArticle,	last if ($SYS_F_S && ($Command eq 's'));
    &ShowIcon,		last if ($Command eq 'i');
    &AliasNew,		last if ($SYS_ALIAS && ($Command eq 'an'));
    &AliasMod,		last if ($SYS_ALIAS && ($Command eq 'am'));
    &AliasDel,		last if ($SYS_ALIAS && ($Command eq 'ad'));
    &AliasShow,		last if ($SYS_ALIAS && ($Command eq 'as'));
    &BoardList,		last if ($SYS_F_B && ($Command eq 'bl'));

    # 以下は管理用
    &ViewTitle(1),	last if ($SYS_F_MT && ($Command eq 'vm'));
    &DeletePreview,	last if ($SYS_F_D && ($Command eq 'dp'));
    &DeleteExec(0),	last if ($SYS_F_D && ($Command eq 'de'));
    &DeleteExec(1),	last if ($SYS_F_D && ($Command eq 'det'));
    &ArriveMailEntry,   last if ($SYS_F_AM && ($Command eq 'mp'));
    &ArriveMailExec,    last if ($SYS_F_AM && ($Command eq 'me'));
    &ViewTitle(2),	last if ($SYS_F_MV && ($Command eq 'ct'));
    &ViewTitle(3),	last if ($SYS_F_MV && ($Command eq 'ce'));
    &ViewTitle(4),	last if ($SYS_F_MV && ($Command eq 'mvt'));
    &ViewTitle(5),	last if ($SYS_F_MV && ($Command eq 'mve'));

    # デフォルト

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
# UIディレクトリに収められているUIの実装モジュールをrequireする．
# 不要なプログラムをコンパイルしないようにするため．
# 各関数のリファレンスは，UIディレクトリ内の各ファイルを参照のこと．

### BoardList - 掲示板一覧の表示
sub BoardList { require(&GetPath('UI', 'BoardList.pl')); }

### Entry - 書き込み画面の表示
sub Entry {
    ($gVarQuoteFlag) = @_;
    require(&GetPath('UI', 'Entry.pl'));
    undef($gVarQuoteFlag);
}

### Preview - プレビュー画面の表示
sub Preview { require(&GetPath('UI', 'Preview.pl')); }

### Thanks - 登録後画面の表示
sub Thanks { require(&GetPath('UI', 'Thanks.pl')); }

### ShowArticle - 単一記事の表示
sub ShowArticle { require(&GetPath('UI', 'ShowArticle.pl')); }

### ThreadArticle - フォロー記事を全て表示．
sub ThreadArticle { require(&GetPath('UI', 'ThreadArticle.pl')); }

### ShowIcon - アイコン表示画面
sub ShowIcon { require(&GetPath('UI', 'ShowIcon.pl')); }

### SortArticle - 日付順にソート
sub SortArticle { require(&GetPath('UI', 'SortArticle.pl')); }

### ViewTitle - スレッド別表示
sub ViewTitle {
    ($gVarComType) = @_;
    require(&GetPath('UI', 'ViewTitle.pl'));
    undef($gVarComType);
}

### NewArticle - 新しい記事をまとめて表示
sub NewArticle { require(&GetPath('UI', 'NewArticle.pl')); }

### SearchArticle - 記事の検索(表示画面の作成)
sub SearchArticle { require(&GetPath('UI', 'SearchArticle.pl')); }

### AliasNew - エイリアスの登録と変更画面の表示
sub AliasNew { require(&GetPath('UI', 'AliasNew.pl')); }

### AliasMod - ユーザエイリアスの登録/変更
sub AliasMod { require(&GetPath('UI', 'AliasMod.pl')); }

### AliasDel - ユーザエイリアスの削除
sub AliasDel { require(&GetPath('UI', 'AliasDel.pl')); }

### AliasShow - ユーザエイリアス参照画面の表示
sub AliasShow { require(&GetPath('UI', 'AliasShow.pl')); }

### DeletePreview - 削除記事の確認
sub DeletePreview { require(&GetPath('UI', 'DeletePreview.pl')); }

### DeleteExec - 記事の削除
sub DeleteExec {
    ($gVarThreadFlag) = @_;
    require(&GetPath('UI', 'DeleteExec.pl'));
    undef($gVarThreadFlag);
}

### ArriveMailEntry - メイル自動配信先の指定
sub ArriveMailEntry { require(&GetPath('UI', 'ArriveMailEntry.pl')); }

### ArriveMailExec - メイル自動配信先の設定
sub ArriveMailExec { require(&GetPath('UI', 'ArriveMailExec.pl')); }

### Fatal - エラー表示
sub Fatal {
    ($gVarFatalNo, $gVarFatalInfo) = @_;
    require(&GetPath('UI', 'Fatal.pl'));
    undef($gVarFatalNo, $gVarFatalInfo);
}

### ArriveMail - 記事が到着したことをメイル
sub ArriveMail {
    ($gName, $gSubject, $gId, @gTo) = @_;
    require(&GetPath('UI', 'ArriveMail.pl'));
    undef($gName, $gSubject, $gId, @gTo);
}

### FollowMail - 反応があったことをメイル
sub FollowMail {
    ($gName, $gDate, $gSubject, $gId, $gFname, $gFsubject, $gFid, @gTo) = @_;
    require(&GetPath('UI', 'FollowMail.pl'));
    undef($gName, $gDate, $gSubject, $gId, $gFname, $gFsubject, $gFid, @gTo);
}


######################################################################
# ユーザインタフェイスインプリメンテーション(共通部)


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

	    &cgiprint'Cache(" | <a href=\"$PROGRAM?b=$BOARD&c=v&num=$DEF_TITLE_NUM\"><img src=\"$ICON_TLIST\" alt=\"$H_BACKTITLE\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\">$H_BACKTITLE</a>\n");

	    if ($PrevId ne '') {
		&cgiprint'Cache(" | <a href=\"$PROGRAM?b=$BOARD&c=e&id=$PrevId\"><img src=\"$ICON_PREV\" alt=\"$H_PREVARTICLE\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\">$H_PREVARTICLE</a>\n");
	    } else {
		&cgiprint'Cache(" | <img src=\"$ICON_PREV\" alt=\"$H_PREVARTICLE\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\">$H_PREVARTICLE\n");

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
		&cgiprint'Cache(<<__EOF__);
 | <a href="$PROGRAM?b=$BOARD&c=n"><img src="$ICON_WRITENEW" alt="$H_POSTNEWARTICLE" width="$COMICON_WIDTH" height="$COMICON_HEIGHT" BORDER="0">$H_POSTNEWARTICLE</a>
 | <a href="$PROGRAM?b=$BOARD&c=f&id=$Id"><img src="$ICON_FOLLOW" alt="$H_REPLYTHISARTICLE" width="$COMICON_WIDTH" height="$COMICON_HEIGHT" BORDER="0">$H_REPLYTHISARTICLE</a>
 | <a href="$PROGRAM?b=$BOARD&c=q&id=$Id"><img src="$ICON_QUOTE" alt="$H_REPLYTHISARTICLEQUOTE" width="$COMICON_WIDTH" height="$COMICON_HEIGHT" BORDER="0">$H_REPLYTHISARTICLEQUOTE</a>
__EOF__
	    }

	    &cgiprint'Cache(" | <a href=\"$PROGRAM?b=$BOARD&c=i&type=article\"><img src=\"$ICON_HELP\" alt=\"?\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\">?</a>\n");

	} elsif ($SYS_COMICON == 1) {

	    if ($SYS_F_B) {
		&cgiprint'Cache("<a href=\"$BOARDLIST_URL\"><img src=\"$ICON_BLIST\" alt=\"$H_BACKBOARD\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\"></a>\n");
	    }

	    &cgiprint'Cache("<a href=\"$PROGRAM?b=$BOARD&c=v&num=$DEF_TITLE_NUM\"><img src=\"$ICON_TLIST\" alt=\"$H_BACKTITLE\" width=\"$COMICON_WIDTH\" height=\"$COMICON_HEIGHT\" BORDER=\"0\"></a>\n");

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

	    &cgiprint'Cache(" | <a href=\"$PROGRAM?b=$BOARD&c=v&num=$DEF_TITLE_NUM\">$H_BACKTITLE</a>\n");

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

	    if ($SYS_F_T) {
		if ($Aids ne '') {
		    &cgiprint'Cache(" | <a href=\"$PROGRAM?b=$BOARD&c=t&id=$Id\">$H_READREPLYALL</a>");
		} else {
		    &cgiprint'Cache(" | $H_READREPLYALL");
		}
	    }

	    if ($SYS_F_N) {
		&cgiprint'Cache(<<__EOF__);
 | <a href="$PROGRAM?b=$BOARD&c=n">$H_POSTNEWARTICLE</a>
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
	&cgiprint'Cache(sprintf("<strong>$H_SUBJECT</strong>: <strong>$Id .</strong> <img src=\"%s\" alt=\"$Icon \" width=\"$MSGICON_WIDTH\" height=\"$MSGICON_HEIGHT\">$Subject", &GetIconUrlFromTitle($Icon, $BOARD)));
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
    &GetArticleBody($Id, $BOARD, *ArticleBody);
    foreach(@ArticleBody) { &cgiprint'Cache($_); }

}


###
## ThreadArticleMain - フォロー記事を全て表示．
#
# - SYNOPSIS
#	ThreadArticle($SubjectOnly, $Head, @Tail);
#
# - ARGS
#	$SubjectOnly	タイトルのみを表示するのか，
#			あるいは記事本文も表示するのか．
#	$Head		木構造のヘッドノード
#	@Tail		木構造の娘ノード群
#
# - DESCRIPTION
#	ある記事と，その記事へのリプライ記事をまとめて表示する．
#	元の木構造は，
#		( a ( b ( c d ) ) ( e ) ( f ( g ) ) )
#	のようなリストである．
#	詳細は&GetFollowIdTreeのインプリメント部分を参照のこと．
#
# - RETURN
#	なし
#
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
    &GetArticleBody($Id, $BOARD, *ArticleBody);
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

    &GetArticleBody($Id, $BOARD, *ArticleBody);
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

    &GetBoardHeader($BOARD, *BoardHeader);
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
## PrintButtonToTitleList - タイトル一覧へ戻るボタンの表示
#
# - SYNOPSIS
#	PrintButtonToTitleList($Board);
#
# - ARGS
#	$Board		掲示板ID
#
# - DESCRIPTION
#	タイトル一覧に戻るためのボタンを表示する
#
# - RETURN
#	なし
#
sub PrintButtonToTitleList {
    local($Board) = @_;

    &cgiprint'Cache(<<__EOF__);
<form action="$PROGRAM" method="POST">
<input name="b" type="hidden" value="$Board">
<input name="c" type="hidden" value="v">
<input name="num" type="hidden" value="$DEF_TITLE_NUM">
<input type="submit" value="$H_BACKTITLE">
</form>
__EOF__
}


###
## PrintButtonToBoardList - 掲示板一覧へ戻るボタンの表示
#
# - SYNOPSIS
#	PrintButtonToBoardList;
#
# - ARGS
#	なし
#
# - DESCRIPTION
#	掲示板一覧に戻るためのボタンを表示する
#
# - RETURN
#	なし
#
sub PrintButtonToBoardList {

    &cgiprint'Cache(<<__EOF__);
<form action="$BOARDLIST_URL" method="GET">
<input type="submit" value="$H_BACKBOARD">
</form>
__EOF__
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
	&GetArticleBody($Id, $BOARD, *ArticleBody);
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

    &GetArticleBody($Id, $Board, *ArticleBody);
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
    if (! &GetIconUrlFromTitle($Icon, $Board)) { $Icon = $H_NOICON; }

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
#	(アプリケーション/UIを分離したほうがいいかな?)
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
#	(アプリケーション/UIを分離したほうがいいかな?)
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
#	(アプリケーション/UIを分離したほうがいいかな?)
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
#	(アプリケーション/UIを分離したほうがいいかな?)
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
#	(アプリケーション/UIを分離したほうがいいかな?)
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
    $Link = "<a href=\"$PROGRAM?b=$Board&c=e&id=$Id\">$Title</a>";
    $Thread = (($SYS_F_T && $Aids) ? " <a href=\"$PROGRAM?b=$Board&c=t&id=$Id\">$H_THREAD</a>" : '');

    if (($Icon eq $H_NOICON) || ($Icon eq '')) {
	$String = sprintf("$IdStr$Link$Thread [%s] $InputDate", ($Name || $MAINT_NAME));
    } else {
	$String = sprintf("$IdStr<img src=\"%s\" alt=\"$Icon \" width=\"$MSGICON_WIDTH\" height=\"$MSGICON_HEIGHT\">$Link$Thread [%s] $InputDate", &GetIconUrlFromTitle($Icon, $Board), ($Name || $MAINT_NAME));
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
#	$Board		掲示板ID
#	$ThreadFlag	リプライも消すか否か
#
# - DESCRIPTION
#	削除すべき記事IDを収集した後，DBを更新する．
#
# - RETURN
#	なし
#
sub DeleteArticle {
    local($Id, $Board, $ThreadFlag) = @_;
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
    &DeleteArticleFromDbFile($Board, *Target);
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
    $SupersedeId = &SupersedeDbFile($Board, $Id, $TIME, $Subject, $Icon, $REMOTE_HOST, $Name, $Email, $Url, $Fmail);

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
    &UpdateArticleDb($Board);
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
    &ReOrderArticleDb($Board, $ToId, *Move);

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

    &GetArticleId($Board) + 1;
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
    &GetArriveMailTo(0, $Board, *ArriveMail);
    if (@ArriveMail) {
	&ArriveMail($Name, $Subject, $Id, @ArriveMail);
    }

    # 必要なら反応があったことをメイルする
    if (@FollowMailTo) {
	&FollowMail($mdName, $mdInputDate, $mdSubject, $mdId, $mName, $mSubject, $mId, @FollowMailTo);
    }

}


###
## UpdateArticleDb - 記事DBの全更新
#
# - SYNOPSIS
#	UpdateArticleDb($Board);
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
sub UpdateArticleDb {
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
## DeleteArticleFromDbFile - 記事DBの更新
#
# - SYNOPSIS
#	DeleteArticleFromDbFile($Board, *Target);
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
sub DeleteArticleFromDbFile {
    local($Board, *Target) = @_;
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
## ReOrderArticleDb - 記事DBの順序変更
#
# - SYNOPSIS
#	ReOrderArticleDb($Board, $Id, *Move);
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
sub ReOrderArticleDb {
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
## GetArticleBody - 記事本文DBの読み込み
#
# - SYNOPSIS
#	GetArticleBody($Id, $Board, *ArticleBody);
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
sub GetArticleBody {
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
## GetArticleId - 記事番号DBの読み込み
#
# - SYNOPSIS
#	GetArticleId($Board);
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
sub GetArticleId {
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
## GetArriveMailTo - 掲示板別新規メイル送信先DBの全読み込み
#
# - SYNOPSIS
#	GetArriveMailTo($CommentFlag, $Board, *ArriveMail);
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
sub GetArriveMailTo {
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
## UpdateArriveMailDb - 掲示板別新規メイル送信先DBの全更新
#
# - SYNOPSIS
#	UpdateArriveMailDb($Board, *ArriveMail);
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
sub UpdateArriveMailDb {
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
## GetAllBoardInfo - 掲示板DBの全読み込み
#
# - SYNOPSIS
#	GetAllBoardInfo(*BoardList, *BoardInfo);
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
sub GetAllBoardInfo {
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
## CashIconDb - アイコンDBの全読み込み
#
# - SYNOPSIS
#	CashIconDb($Board);
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

sub CashIconDb {
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
## GetBoardHeader - 掲示板ヘッダDBの読み込み
#
# - SYNOPSIS
#	GetBoardHeader($Board, *BoardHeader);
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
sub GetBoardHeader {
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
#	GetPath($DbDir, $File);
#
# - ARGS
#	$DbDir		DBディレクトリ(掲示板ID, etc.)
#	$File		ファイル名
#
# - DESCRIPTION
#	DBディレクトリ名とファイル名から，DBファイルのパス名を作り出す．
#	大域変数$ARCHを参照し，Mac/Win/UNIXに対応．
#
# - RETURN
#	パスを表す文字列
#
sub GetPath {
    local($DbDir, $File) = @_;

    # 返す
    return("$DbDir/$File") if ($ARCH eq 'UNIX');
    return("$DbDir/$File") if ($ARCH eq 'WinNT');
    return("$DbDir/$File") if ($ARCH eq 'Win95');
    return(":$DbDir:$File") if ($ARCH eq 'Mac');

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
## GetIconUrlFromTitle - アイコンgifのURLの取得
#
# - SYNOPSIS
#	GetIconUrlFromTitle($Icon, $Board);
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
sub GetIconUrlFromTitle {
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

    return($TargetFile ? "$ICON_DIR/$TargetFile" : '');

}


###
## SupersedeDbFile - 訂正記事の記事DBへの書き込み
#
# - SYNOPSIS
#	SupersedeDbFile($Board, $Id, $InputDate, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail);
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
sub SupersedeDbFile {
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
