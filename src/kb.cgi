#!/usr/local/bin/perl5
#
# $Id: kb.cgi,v 4.20 1996-08-16 17:11:43 nakahiro Exp $


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
($CGIPROG_NAME = $SCRIPT_NAME) =~ s#^(.*/)##;
$SYSDIR_NAME = (($PATH_INFO) ? "$PATH_INFO/" : "$1");
$SCRIPT_URL = "http://$SERVER_NAME:$SERVER_PORT$SCRIPT_NAME";
$PROGRAM = (($PATH_INFO) ? "$SCRIPT_NAME$PATH_INFO" : $CGIPROG_NAME);


###
## インクルードファイルの読み込み
#
chdir($PATH_TRANSLATED) if ($PATH_TRANSLATED);
require('kb.ph');
require('jcode.pl');
require('cgi.pl');
require('tag_secure.pl');


###
## 大域変数の定義
#

#
# 配列のdefault
#
$[ = 0;

#
# 著作権表示
#
$ADDRESS = "KINOBOARDS/1.0 R2.2: Copyright (C) 1995, 96 <a href=\"http://www.kinotrope.co.jp/~nakahiro/\">NAKAMURA Hiroshi</a>.";

#
# ファイル
#
# 記事番号ファイル
$ARTICLE_NUM_FILE_NAME = ".articleid";
# 記事番号テンポラリファイル
$ARTICLE_NUM_TMP_FILE_NAME = ".articleid.tmp";
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
# ユーザエイリアステンポラリファイル
$USER_ALIAS_TMP_FILE = "kinousers.tmp";
# ボードエイリアスファイル
$BOARD_ALIAS_FILE = "kinoboards";
# デフォルトのアイコン定義ファイル
$DEFAULT_ICONDEF = "all.idef";
# ロックファイル
$LOCK_FILE = ".lock.kb";
# ロック元ファイル
$LOCK_ORG = ".lock.kb.org";
# ロック時のリトライ回数
$LOCK_WAIT = 10;

#
# アイコンディレクトリ
# (アイコンとアイコン定義ファイルを入れるディレクトリ名)
#
$ICON_DIR = "icons";

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
$ICONDEF_POSTFIX = "idef";
$ICON_HEIGHT = 20;
$ICON_WIDTH = 20;

#
# 引用フラグ
#
$QUOTE_ON = 1;
$NO_QUOTE = 0;

#
# エスケープコード
#
$NULL_LINE = "__br__";
$DOUBLE_QUOTE = "__dq__";
$GREATER_THAN = '__gt__';
$LESSER_THAN = '__lt__';
$AND_MARK = '__amp__';


# トラップ
$SIG{'HUP'} = $SIG{'INT'} = $SIG{'QUIT'} = $SIG{'TERM'} = 'DoKill';
sub DoKill {
    &unlock();			# unlock
    exit(1);			# error exit.
}


###
## メイン
#
MAIN: {

    # 標準入力(POST)または環境変数(GET)のデコード．
    &cgi'decode;

    # 頻繁に使うので大域変数
    $BOARD = $cgi'TAGS{'b'};
    $BOARDNAME = &GetBoardInfo($BOARD);

    # 掲示板固有セッティングを読み込む
    local($BoardConfFile) = &GetPath($BOARD, $CONF_FILE_NAME);
    require("$BoardConfFile") if (-s "$BoardConfFile");

    # 値の抽出
    local($Command) = $cgi'TAGS{'c'};
    local($Com) = $cgi'TAGS{'com'};
    local($Id) = $cgi'TAGS{'id'};
    local($Alias) = $cgi'TAGS{'alias'};
    local($Name) = $cgi'TAGS{'name'};
    local($Email) = $cgi'TAGS{'email'};
    local($URL) = $cgi'TAGS{'url'};

    # まずはロック
    &lock;

    # コマンドタイプによる分岐
    if ($Command eq "e") {
	&ShowArticle($Id);
    } elsif (($Command eq "en")
	     || (($Command eq "m") && ($Com eq $H_NEXTARTICLE))) {
	&ShowArticle($Id + 1);
    } elsif (($Command eq "t")
	     || (($Command eq "m") && ($Com eq $H_READREPLYALL))) {
	&ThreadArticle($Id);

    } elsif (($Command eq "n")
	     || (($Command eq "m") && ($Com eq $H_POSTNEWARTICLE))) {
	&Entry($NO_QUOTE, 0);
    } elsif (($Command eq "f")
	     || (($Command eq "m") && ($Com eq $H_REPLYTHISARTICLE))) {
	&Entry($NO_QUOTE, $Id);
    } elsif (($Command eq "q")
	     || (($Command eq "m") && ($Com eq $H_REPLYTHISARTICLEQUOTE))) {
	&Entry($QUOTE_ON, $Id);
    } elsif (($Command eq "p") && ($Com ne "x")) {
	&Preview();
    } elsif (($Command eq "x")
	     || (($Command eq "p") && ($Com eq "x"))) {
	&Thanks();

    } elsif ($Command eq "v") {
	&ViewTitle();
    } elsif ($Command eq "r") {
	&SortArticle();
    } elsif ($Command eq "l") {
	&NewArticle();

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

    } else {
	print("illegal command was given.\n");
    }

    # ロックを外す
    &unlock;

}


###
## おしまい
#
exit 0;


###
## 書き込み画面
#
sub Entry {

    # 引用あり/なしと，引用する場合はそのId(引用しない時は0)
    local($QuoteFlag, $Id) = @_;

    # 表示画面の作成
    &MsgHeader("$BOARDNAME: $ENTRY_MSG");

    # フォローの場合
    if ($Id != 0) {
	# 記事の表示(コマンド無し)
	&ViewOriginalArticle($Id, 0);
	print("<hr>\n");
	print("<h2>$H_REPLYMSG</h2>");
    }

    # ヘッダ部分の表示
    &EntryHeader((($Id !=0 ) ? &GetReplySubject($Id, $BOARDDIR) : ''), $Id);

    # 本文(引用ありなら元記事を挿入)
    print("<textarea name=\"article\" rows=\"$TEXT_ROWS\" cols=\"$TEXT_COLS\">");
    &QuoteOriginalArticle($Id, $BOARD)
	if (($Id != 0) && ($QuoteFlag == $QUOTE_ON));
    print("</textarea><br>\n");

    # フッタ部分を表示
    &EntryFooter();

}


###
## 書き込み画面のうち，あおり文，TextType，Board名を表示．
#
sub EntryHeader {

    local($Subject, $Id) = @_;

    # お約束
    print(<<__EOF__);
<p>
<form action="$PROGRAM" method="POST">
<input name="c" type="hidden" value="p">
<input name="b" type="hidden" value="$BOARD">
<input name="id" type="hidden" value="$Id">
</p>
<p>
$H_AORI
</p>
$H_BOARD $BOARDNAME<br>
__EOF__

    # アイコンの選択
    if ($SYS_ICON) {
	print("$H_ICON\n");
	print("<SELECT NAME=\"icon\">\n");
	print("<OPTION SELECTED>$H_NOICON\n");

	# 一つ一つ表示
	open(ICON, &GetIconPath("$BOARD.$ICONDEF_POSTFIX"))
	    || (open(ICON, &GetIconPath("$DEFAULT_ICONDEF"))
		|| &Fatal(1, &GetIconPath("$DEFAULT_ICONDEF")));
	while(<ICON>) {
	    # コメント文はキャンセル
	    next if (/^\#/o);
	    next if (/^$/o);
	    chop;
	    ($FileName, $Title) = split(/\t/, $_, 3);
	    print("<OPTION>$Title\n");
	}
	close(ICON);
	print("</SELECT>\n");
	print("(<a href=\"$PROGRAM?b=$BOARD&c=i&type=entry\">$H_SEEICON</a>)<BR>\n");
    }

    # Subject(フォローなら自動的に文字列を入れる)
    printf("%s <input name=\"subject\" type=\"text\" value=\"%s\" size=\"%s\"><br>\n",
	   $H_SUBJECT, $Subject, $SUBJECT_LENGTH);

    # TextType
    if ($SYS_TEXTTYPE) {
	print(<<__EOF__);
$H_TEXTTYPE
<SELECT NAME="texttype">
<OPTION SELECTED>$H_PRE
<OPTION>$H_HTML
</SELECT><BR>
__EOF__

    }

}


###
## フッタ部分を表示
#
sub EntryFooter {

    # 名前とメールアドレス，URL．
    print(<<__EOF__);
$H_FROM <input name="name" type="text" size="$NAME_LENGTH"><br>
$H_MAIL <input name="mail" type="text" size="$MAIL_LENGTH"><br>
$H_URL <input name="url" type="text" value="http://" size="$URL_LENGTH"><br>
__EOF__

    ($SYS_FOLLOWMAIL) && print("$H_FMAIL <input name=\"fmail\" type=\"checkbox\" value=\"on\"><br>\n");
    
    if ($SYS_ALIAS) {
	print(<<__EOF__);
<p>
$H_ALIASINFO
(<a href="$PROGRAM?c=as">$H_SEEALIAS</a> //
 <a href="$PROGRAM?c=an">$H_ALIASENTRY</a>)
</p>
__EOF__

    }

    # ボタン
    print(<<__EOF__);
<input type="radio" name="com" value="p" CHECKED>: $H_PREVIEW<br>
<input type="radio" name="com" value="x">: $H_ENTRY<br>
<input type="submit" value="$H_PUSHHERE">
</p>
</form>
__EOF__

    &MsgFooter();
}


###
## あるIdの記事からSubjectを取ってきて，先頭に「Re: 」を1つだけつけて返す．
#
sub GetReplySubject {

    # IdとBoard
    local($Id, $Board) = @_;

    # 記事情報
    local($dFid, $dAids, $dDate, $dSubject, $dIcon, $dRemoteHost, $dName,
	  $dEmail, $dUrl, $dFmail) = &GetArticlesInfo($Id);

    # 先頭に「Re: 」がくっついてたら取り除く．
    $dSubject =~ s/^Re: //o;

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
    local($Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name)
	= &GetArticlesInfo($Id);

    # ファイルを開く
    open(TMP, "<$QuoteFile") || &Fatal(1, $QuoteFile);
    while(<TMP>) {

	# 引用のための変換
	s/\&//go;
	s/\"//go;
	s/<[^>]*>//go;

	# 引用文字列の表示
	printf("%s%s%s", $Name, $DEFAULT_QMARK, $_);
	
    }

    # 閉じる
    close(TMP);

}


###
## プレビュー画面
#
sub Preview {

    # 入力された記事情報
    local($Id, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article,
	  $Qurl, $Fmail)
	= ($cgi'TAGS{'id'}, $cgi'TAGS{'texttype'}, $cgi'TAGS{'name'},
	   $cgi'TAGS{'mail'}, $cgi'TAGS{'url'}, $cgi'TAGS{'icon'},
	   $cgi'TAGS{'subject'}, $cgi'TAGS{'article'},
	   $cgi'TAGS{'qurl'}, $cgi'TAGS{'fmail'});

    # 引用記事のURL
    local($rFile) = '';

    # 引用記事の記事情報
    local($rFid, $rAids, $rDate, $rSubject, $rIcon, $rRemoteHost, $rName,
	  $rEmail, $rUrl, $rFmail) = ('', '', '', '', '', '', '', '', '', '');

    # もし引用なら……．
    if ($Id) {

	# 通常記事の引用なら……
	$rFile = "$PROGRAM?b=$BOARD&c=e&id=$Id";

	# 引用記事の記事情報を取得
	($rFid, $rAids, $rDate, $rSubject, $rIcon, $rRemoteHost, $rName,
	 $rEmail, $rUrl, $rFmail) = &GetArticlesInfo($Id);

    }

    # 入力された記事情報のチェック
    ($Name, $Email, $Url, $Icon, $Article)
	= &CheckArticle($Name, $Email, $Url, $Subject, $Icon, $Article);

    # 確認画面の作成
    &MsgHeader($PREVIEW_MSG);

    # お約束
    print(<<__EOF__);
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
<input type="submit" value="$H_PUSHHERE">
</p>
__EOF__

    # 題
    (($Icon eq $H_NOICON) || (! $Icon))
        ? print("<strong>$H_SUBJECT</strong> $Subject<br>\n")
            : printf("<strong>$H_SUBJECT</strong> <img src=\"%s\" alt=\"$Icon\" width=\"$ICON_WIDTH\" height=\"$ICON_HEIGHT\"> $Subject<br>\n", &GetIconURLFromTitle($Icon));

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
    $Article = &DQDecode($Article);
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
    local($Name, $Email, $Url, $Subject, $Icon, $Article) = @_;
    local($Tmp) = '';

    # エイリアスチェック
    $_ = $Name;
    if (/^#.*$/) {
        ($Tmp, $Email, $Url) = &GetUserInfo($_);
	&Fatal(7, $Name) if ($Tmp eq '');
	$Name = $Tmp;
    }

    # 文字列チェック
    &CheckName($Name);
    &CheckEmail($Email);
    &CheckURL($Url);
    &CheckSubject($Subject);

    # アイコンのチェック; おかしけりゃ「無し」に設定．
    $Icon = $H_NOICON unless (&GetIconURLFromTitle($Icon));

    # 記事中の"をエンコード
    $Article = &DQEncode($Article);

    # 名前，e-mail，URLを返す．
    return($Name, $Email, $Url, $Icon, $Article);
}


###
## 登録後画面
#
sub Thanks {

    # 新たに記事を生成する
    &MakeNewArticle();

    # 表示画面の作成
    &MsgHeader($THANKS_MSG);

    print(<<__EOF__);
<p>
$H_THANKSMSG
</p>
<form action="$PROGRAM" method="POST">
<input name="b" type="hidden" value="$BOARD">
<input name="c" type="hidden" value="v">
<input name="num" type="hidden" value="$DEF_TITLE_NUM">
<input type="submit" value="$H_BACK">
</form>
__EOF__

    &MsgFooter();
}


###
## 新たに投稿された記事の生成
#
sub MakeNewArticle {

    # 日付を取り出す．
    local($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst)
	= localtime(time);
    local($InputDate) = sprintf("%d/%d(%02d:%02d)", $mon + 1, $mday, $hour, $min);

    # 入力された記事情報
    local($Id, $TextType, $Name, $Email, $Url, $Icon, $Subject, $Article,
	  $Qurl, $Fmail)
	= ($cgi'TAGS{'id'}, $cgi'TAGS{'texttype'}, $cgi'TAGS{'name'},
	   $cgi'TAGS{'mail'}, $cgi'TAGS{'url'}, $cgi'TAGS{'icon'},
	   $cgi'TAGS{'subject'}, $cgi'TAGS{'article'},
	   $cgi'TAGS{'qurl'}, $cgi'TAGS{'fmail'});

    # 入力された記事情報のチェック
    ($Name, $Email, $Url, $Icon, $Article)
	= &CheckArticle($Name, $Email, $Url, $Subject, $Icon, $Article);

    # 新しい記事番号を取得(まだ記事番号は増えてない)
    local($ArticleId) = &GetNewArticleId();

    # 正規のファイルの作成
    &MakeArticleFile($TextType, $Article, $ArticleId);

    # DBファイルに投稿された記事を追加
    # 通常の記事引用ならID
    &AddDBFile($ArticleId, $Id, $InputDate, $Subject, $Icon, $REMOTE_HOST,
	       $Name, $Email, $Url, $Fmail);

    # 新しい記事番号を書き込む
    &AddArticleId();

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
    open(TMP, ">$File") || &Fatal(1, $File);

    # TextType用前処理
    print(TMP "<pre>\n") if ((! $SYS_TEXTTYPE) || ($TextType eq $H_PRE));

    # 記事; "をデコードし，セキュリティチェック
    $Article = &DQDecode($Article);
    $Article = &tag_secure'decode($Article);
    print(TMP "$Article\n");

    # TextType用後処理
    print(TMP "</pre>\n") if ((! $SYS_TEXTTYPE) || ($TextType eq $H_PRE));
    
    # 終了
    close(TMP);

}


###
## "のencode and decode
#
sub DQEncode {
    local($_) = @_;
    s/\"/$DOUBLE_QUOTE/g;
    s/\>/$GREATER_THAN/g;
    s/\</$LESSER_THAN/g;
    s/\&/$AND_MARK/g;
    return($_);
}

sub DQDecode {
    local($_) = @_;
    s/$DOUBLE_QUOTE/\"/g;
    s/$GREATER_THAN/\>/g;
    s/$LESSER_THAN/\</g;
    s/$AND_MARK/\&/g;
    return($_);
}


###
## 記事番号を増やす．
#
sub AddArticleId {

    # 記事番号を収めるファイル
    local($File) = &GetPath($BOARD, $ARTICLE_NUM_FILE_NAME);
    local($TmpFile) = &GetPath($BOARD, $ARTICLE_NUM_TMP_FILE_NAME);

    # 新しい記事番号
    local($ArticleId) = &GetNewArticleId();

    # Open Tmp File
    open(AID, ">$TmpFile") || &Fatal(1, $TmpFile);
    print(AID $ArticleId, "\n");
    close(AID);

    # 更新
    rename($TmpFile, $File);

}


###
## DBファイルに書き込む
#
sub AddDBFile {

    # 記事Id，名前，アイコン，題，日付
    local($Id, $Fid, $InputDate, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail) = @_;
    local($dId, $dFid, $dAids, $dInputDate, $dSubject, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail);
    
    # 登録ファイル
    local($File) = &GetPath($BOARD, $DB_FILE_NAME);
    local($TmpFile) = &GetPath($BOARD, $DB_TMP_FILE_NAME);

    # Open Tmp File
    open(DBTMP, ">$TmpFile") || &Fatal(1, $TmpFile);
    # Open DB File
    open(DB, "<$File") || &Fatal(1, $File);

    while(<DB>) {

	print(DBTMP "$_"), next if (/^\#/);
	print(DBTMP "$_"), next if (/^$/);
	chop;

	($dId, $dFid, $dAids, $dInputDate, $dSubject, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail) = split(/\t/, $_);
	
	# フォロー先記事が見つかったら，
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

    # 新しい記事のデータを書き加える．
    printf(DBTMP "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n",
	   $Id, $Fid, '', $InputDate, $Subject, $Icon,
	   $RemoteHost, $Name, $Email, $Url, $Fmail);

    # close Files.
    close(DB);
    close(DBTMP);

    # DBを更新する
    rename($TmpFile, $File);

}


###
## 単一の記事を表示．
#
sub ShowArticle {

    # 記事のIdを取得
    local($Id) = @_;

    # 記事のファイル名を取得
    local($File) = &GetArticleFileName($Id, $BOARD);

    # 引用記事の情報
    local($rFid, $rAids, $rDate, $rSubject, $rIcon, $rRemoteHost, $rName, $rEmail, $rUrl, $rFmail);

    # 反応記事の情報
    local($aFid, $aAids, $aDate, $aSubject, $aIcon, $aRemoteHost, $aName, $aEmail, $aUrl, $aFmail);

    # 記事情報の取得
    local($Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail) = &GetArticlesInfo($Id);
    local(@AidList) = split(/,/, $Aids);
    local($Aid) = '';

    # 未投稿記事は読めない
    &Fatal(11, '') unless ($Name);

    # 引用記事情報の抽出
    ($rFid, $rAids, $rDate, $rSubject, $rIcon, $rRemoteHost, $rName, $rEmail,
     $rUrl, $rFmail) = &GetArticlesInfo($Fid) if ($Fid != 0);

    # 表示画面の作成
    &MsgHeader("[$BOARDNAME: $Id] $Subject");

    # お約束
    if ($SYS_COMMAND) {
	print(<<__EOF__);
<form action="$PROGRAM" method="POST">
<input name="c" type="hidden" value="m">
<input name="b" type="hidden" value="$BOARD">
<input name="id" type="hidden" value="$Id">
<p>
<a href="$PROGRAM?b=$BOARD&c=en&id=$Id"><img src="$ICON_NEXT" alt="$H_NEXTARTICLE" width="$ICON_WIDTH" height="$ICON_HEIGHT" BORDER="0"></a>
<a href="$PROGRAM?b=$BOARD&c=f&id=$Id"><img src="$ICON_FOLLOW" alt="$H_REPLYTHISARTICLE" width="$ICON_WIDTH" height="$ICON_HEIGHT" BORDER="0"></a>
<a href="$PROGRAM?b=$BOARD&c=q&id=$Id"><img src="$ICON_QUOTE" alt="$H_REPLYTHISARTICLEQUOTE" width="$ICON_WIDTH" height="$ICON_HEIGHT" BORDER="0"></a>
<a href="$PROGRAM?b=$BOARD&c=t&id=$Id"><img src="$ICON_THREAD" alt="$H_READREPLYALL" width="$ICON_WIDTH" height="$ICON_HEIGHT" BORDER="0"></a>
<a href="$PROGRAM?b=$BOARD&c=i&type=article"><img src="$ICON_HELP" alt="?" width="$ICON_WIDTH" height="$ICON_HEIGHT" BORDER="0"></a>
</p>
</form>
__EOF__
    }

    # ボード名と記事番号，題
    if (($Icon eq $H_NOICON) || (! $Icon)) {
	print("<strong>$H_SUBJECT</strong> [$BOARDNAME: $Id] $Subject<br>\n");
    } else {
	printf("<strong>$H_SUBJECT</strong> [$BOARDNAME: $Id] <img src=\"%s\" alt=\"$Icon\" width=\"$ICON_WIDTH\" height=\"$ICON_HEIGHT\">$Subject<br>\n", &GetIconURLFromTitle($Icon));
    }

    # お名前
    if ((! $Url) || ($Url eq 'http://')) {
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
    open(TMP, "<$File") || &Fatal(1, $File);
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
	    printf("<li>%s\n", &GetFormattedTitle($Aid, $aAids, $aIcon, $aSubject, $aName, $aDate));
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
## フォロー記事を全て表示．
#
sub ThreadArticle {

    # 元記事のIdを取得
    local($Id) = @_;

    # 表示画面の作成
    &MsgHeader("$BOARDNAME: $THREADARTICLE_MSG");

    # メイン関数の呼び出し(記事概要)
    print("<ul>\n");
    &ThreadArticleMain('subject only', $Id);
    print("</ul>\n");

    print("<hr>\n");

    # メイン関数の呼び出し(記事)
    &ThreadArticleMain('', $Id);

    &MsgFooter();
}


###
## 再帰的にその記事のフォローを表示する．
#
sub ThreadArticleMain {

    # Idの取得
    local($SubjectOnly, $Id) = @_;

    # フォロー記事のIdの取得
    local(@FollowIdList) = &GetFollowIdList($Id);

    # 記事概要か，記事そのものか．
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
	print("<hr>\n") unless ($SubjectOnly);

	# 記事概要なら箇条書
	print("<ul>\n") if ($SubjectOnly);
	
	# 再帰
	&ThreadArticleMain($SubjectOnly, $_, $BOARD);

	# 記事概要なら箇条書閉じ
	print("</ul>\n") if ($SubjectOnly);

    }
}


###
## フォロー記事のIdの配列を取り出す．
#
sub GetFollowIdList {

    # Id
    local($Id) = @_;

    # DBファイル
    local($DBFile) = &GetPath($BOARD, $DB_FILE_NAME);

    # リスト
    local(@Result) = ();

    # 記事情報
    local($dId, $dFid, $dAids, $dDate, $dTitle, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail);

    # 取り込み
    open(DB, "<$DBFile") || &Fatal(1, $DBFile);
    while(<DB>) {

	next if (/^\#/);
	next if (/^$/);
	chop;

	($dId, $dFid, $dAids, $dDate, $dTitle, $dIcon, $dRemoteHost, $dName,
	 $dEmail, $dUrl, $dFmail) = split(/\t/, $_);

	# 見つかった!
	@Result = split(/,/, $dAids) if ($Id == $dId);

    }
    close(DB);

    # 返す
    return(@Result);
}


###
## 記事の概要の表示
#
sub PrintAbstract {

    # Id
    local($Id) = @_;

    # 記事情報を取り出す．
    local($dFid, $dAids, $dDate, $dSubject, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail) = &GetArticlesInfo($Id);

    printf("%s\n", &GetFormattedAbstract($Id, $dIcon, $dSubject, $dName, $dDate));

}


###
## ユーザエイリアスからユーザの名前，メール，URLを取ってくる．
#
sub GetUserInfo {

    # 検索するエイリアス名
    local($Alias) = @_;

    # エイリアス，名前，メール，ホスト，URL
    local($A, $N, $E, $H, $U);

    # エイリアス，名前，メール，ホスト，URL
    local($rN, $rE, $rU) = ('', '', '');

    # ファイルを開く
    open(ALIAS, "<$USER_ALIAS_FILE") || &Fatal(1, $USER_ALIAS_FILE);
    
    # 1つ1つチェック．
    while(<ALIAS>) {
	
	chop;
	
	# 分割
	($A, $N, $E, $H, $U) = split(/\t/, $_);
	
	# マッチしなきゃ次へ．
	next unless ($A eq $Alias);
	
	$rN = $N;
	$rE = $E;
	$rU = $U;

    }
    close(ALIAS);

    # 配列にして返す
    return($rN, $rE, $rU);
}


###
## 反応があったことをメールする．
#
sub FollowMail {

    # 宛先いろいろ
    local($To, $Name, $Date, $Subject, $Id, $Fname, $Fsubject, $Fid) = @_;

    local($URL) = "$SCRIPT_URL?b=$BOARD&c=e&id=$Id";
    local($FURL) = "$SCRIPT_URL?b=$BOARD&c=e&id=$Fid";
    
    # Subject
    local($MailSubject) = "The article was followed.";

    # Message
    local($Message) = "$SYSTEM_NAMEからのお知らせです．\n\n$Dateに「$BOARDNAME」に対して「$Name」さんが書いた，\n「$Subject」\n$URL\nに対して，\n「$Fname」さんから\n「$Fsubject」という題での反応がありました．\n\nお時間のある時に\n$FURL\nを御覧下さい．\n\nでは失礼します．";

    # メール送信
    &SendMail($MailSubject, $Message, $Fid, $To);
}


###
## メール送信
#
sub SendMail {

    # subject，メールのファイル名，引用記事(0なら無し)，宛先
    local($Subject, $Message, $Id, @To) = @_;

    # 引用記事
    if ($Id) {

	# 引用するファイル
	local($QuoteFile) = &GetArticleFileName($Id, $BOARD);

	# 区切り線
	$Message .= "\n$H_LINE\n";

	# 引用
	open(TMP, "<$QuoteFile") || &Fatal(1, $QuoteFile);
	while(<TMP>) {
	    s/<[^>]*>//go;	# タグは要らない
	    $Message .= &HTMLDecode($_) if ($_);
	}
	close(TMP);

    }

    # 送信する
    &Fatal(9, '') unless (&cgi'SendMail($MAINT_NAME, $MAINT, $Subject, $Message, @To));

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
    &MsgHeader($SHOWICON_MSG);

    if ($Type eq 'article') {

	print(<<__EOF__);
<p>
$H_ICONINTRO_ARTICLE
</p>
<p>
<ul>
<li><img src="$ICON_NEXT" alt="$H_NEXTARTICLE" height="$ICON_HEIGHT" width="$ICON_WIDTH"> : $H_NEXTARTICLE
<li><img src="$ICON_FOLLOW" alt="$H_REPLYTHISARTICLE" height="$ICON_HEIGHT" width="$ICON_WIDTH"> : $H_REPLYTHISARTICLE
<li><img src="$ICON_QUOTE" alt="$H_REPLYTHISARTICLEQUOTE" height="$ICON_HEIGHT" width="$ICON_WIDTH"> : $H_REPLYTHISARTICLEQUOTE
<li><img src="$ICON_THREAD" alt="$H_READREPLYALL" height="$ICON_HEIGHT" width="$ICON_WIDTH"> : $H_READREPLYALL
</ul>
</p>
__EOF__

    } else {

	print(<<__EOF__);
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
		|| &Fatal(1, &GetIconPath("$DEFAULT_ICONDEF")));
	while(<ICON>) {
	    # コメント文はキャンセル
	    next if (/^\#/o);
	    next if (/^$/o);
	    chop;
	    ($FileName, $Title, $Help) = split(/\t/, $_, 3);
	    printf("<li><img src=\"%s\" alt=\"$Title\" height=\"$ICON_HEIGHT\" width=\"$ICON_WIDTH\"> : %s\n", &GetIconURL($FileName), ($Help || $Title));
	}
	close(ICON);

	print("</ul>\n</p>\n");

    }

    &MsgFooter();

}


###
## 日付順にソート．
#
sub SortArticle {

    # 表示する個数を取得
    local($Num, $Old) = ($cgi'TAGS{'num'}, $cgi'TAGS{'old'});
    local($NextOld) = ($Old > $Num) ? ($Old - $Num) : 0;
    local($BackOld) = ($Old + $Num);

    # 表示する分だけ取り出す
    local(@Lines) = ();
    &GetTitle($Num, $Old, *Lines);

    # 記事情報
    local($Id, $Fid, $Aids, $Date, $Title, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail);

    # 表示画面の作成
    &MsgHeader("$BOARDNAME: $SORT_MSG");

    &BoardHeader;

    print("<hr>\n");

    if ($SYS_BOTTOMTITLE) {
	print("<p>$H_TOP<a href=\"$PROGRAM?b=$BOARD&c=r&num=$Num&old=$BackOld\">$H_BACKART</a></p>\n") if (@Lines && (($#Lines + 1) == $Num));
    } else {
	print("<p>$H_TOP<a href=\"$PROGRAM?b=$BOARD&c=r&num=$Num&old=$NextOld\">$H_NEXTART</a></p>\n") if ($Old);
    }

    print("<ul>\n");

    # 記事の表示
    if (! @Lines) {

	# 空だった……
	print("<li>$H_NOARTICLE\n");

    } else {

	@Lines = reverse(@Lines) unless ($SYS_BOTTOMTITLE);

	foreach (@Lines) {

	    # 記事情報の取り出し
	    ($Id, $Fid, $Aids, $Date, $Title, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail) = split(/\t/, $_, 11);
	    print("<li>" . &GetFormattedTitle($Id, $Aids, $Icon, $Title, $Name, $Date) . "\n");
	}
    }

    print("</ul>\n");

    if ($SYS_BOTTOMTITLE) {
	print("<p>$H_BOTTOM<a href=\"$PROGRAM?b=$BOARD&c=r&num=$Num&old=$NextOld\">$H_NEXTART</a></p>\n") if ($Old);
    } else {
	print("<p>$H_BOTTOM<a href=\"$PROGRAM?b=$BOARD&c=r&num=$Num&old=$BackOld\">$H_BACKART</a></p>\n") if (@Lines && (($#Lines + 1) == $Num));
    }

    &MsgFooter();

}


###
## 記事n個をDBから取り出し，DBの行をそのままリストにして返す．
#
sub GetTitle {

    # 記事数
    local($Num, $Old, *Lines) = @_;

    # DBファイル
    local($DBFile) = &GetPath($BOARD, $DB_FILE_NAME);

    # 記事情報
    local($Id, $Fid) = (0, '');

    # ユーザ情報
    local($Name, $Passwd) = ('', '');

    # 取り込み．DBファイルがなければ何も表示しない．
    open(DB, "<$DBFile") || &Fatal(1, $DBFile);

    while(<DB>) {

	# コメント文はキャンセル
	next if (/^\#/o);
	next if (/^$/o);
	chop;

	# 記事情報の取り出し
	($Id, $Fid) = split(/\t/, $_, 3);

	# 新規記事のみ表示，の場合はキャンセル．
	push(Lines, $_) unless (($SYS_NEWARTICLEONLY) && ($Fid != 0));

    }

    close(DB);

    # 必要な部分だけ切り出す．
    if ($Old) {
	if (($#Lines + 1) > $Old) {
	    splice(@Lines, -$Old);
	} else {
	    @Lines = ();
	}
    }
    if ($Num && (($#Lines + 1) > $Num)) {
	@Lines = splice(@Lines, -$Num);
    }
}


###
## 新しい記事のタイトルをthread別にn個を表示．
#
sub ViewTitle {

    # 表示する個数を取得
    local($Num, $Old) = ($cgi'TAGS{'num'}, $cgi'TAGS{'old'});
    local($NextOld) = ($Old > $Num) ? ($Old - $Num) : 0;
    local($BackOld) = ($Old + $Num);

    # フォーマットしたタイトル
    local($Line) = '';

    # フォーマットしたタイトルを入れるリスト
    local(@NewLines) = ();

    # 記事情報
    local($Id, $Fid, $Aids, $Date, $Title, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail);

    # 表示する分だけ取り出す
    local(@Lines) = ();
    &GetTitle($Num, $Old, *Lines);

    # 応答をインデントする．
    foreach (@Lines) {
    
	# 記事情報を取り出す．
	($Id, $Fid, $Aids, $Date, $Title, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail) = split(/\t/, $_);

	# タイトルをフォーマット
	$Line = "<!--$Id-->" . &GetFormattedTitle($Id, $Aids, $Icon, $Title, $Name, $Date);

	# 追加
	@NewLines = ($Fid)
	    ? &AddTitleFollow($Fid, $Line, @NewLines)
		: &AddTitleNormal($Line, @NewLines);

    }

    # 表示画面の作成
    &MsgHeader("$BOARDNAME: $VIEW_MSG");

    &BoardHeader;

    print("<hr>\n");

    if ($SYS_BOTTOMTITLE) {
	print("<p>$H_TOP<a href=\"$PROGRAM?b=$BOARD&c=v&num=$Num&old=$BackOld\">$H_BACKART</a></p>\n") if (@Lines && (($#Lines + 1) == $Num));
    } else {
	print("<p>$H_TOP<a href=\"$PROGRAM?b=$BOARD&c=v&num=$Num&old=$NextOld\">$H_NEXTART</a></p>\n") if ($Old);
    }

    print("<ul>\n");

    # 記事の表示
    if (! @NewLines) {

	# 空だった……
	print("<li>$H_NOARTICLE\n");

    } else {

	foreach (@NewLines) {
	    if (! /^${NULL_LINE}$/o) {
		if ((m!^<ul>$!io) || (m!^</ul>$!io)) {
		    print("$_\n");
		} else {
		    print("<li>$_");
		}
	    }
	}
    }

    print("</ul>\n");

    if ($SYS_BOTTOMTITLE) {
	print("<p>$H_BOTTOM<a href=\"$PROGRAM?b=$BOARD&c=v&num=$Num&old=$NextOld\">$H_NEXTART</a></p>\n") if ($Old);
    } else {
	print("<p>$H_BOTTOM<a href=\"$PROGRAM?b=$BOARD&c=v&num=$Num&old=$BackOld\">$H_BACKART</a></p>\n") if (@Lines && (($#Lines + 1) == $Num));
    }

    &MsgFooter();

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


###
## 新しい記事からn個を表示．
#
sub NewArticle {

    # 表示する個数を取得
    local($Num, $Old) = ($cgi'TAGS{'num'}, $cgi'TAGS{'old'});
    local($NextOld) = ($Old > $Num) ? ($Old - $Num) : 0;
    local($BackOld) = ($Old + $Num);

    # 表示する分だけタイトルを取得
    local(@Lines) = ();
    &GetTitle($Num, $Old, *Lines);

    # 記事情報
    local($Id) = (0);

    # 表示画面の作成
    &MsgHeader("$BOARDNAME: $NEWARTICLE_MSG");

    if ($SYS_BOTTOMARTICLE) {
	print("<p>$H_TOP<a href=\"$PROGRAM?b=$BOARD&c=l&num=$Num&old=$BackOld\">$H_BACKART</a></p>\n") if (@Lines && (($#Lines + 1) == $Num));
    } else {
	print("<p>$H_TOP<a href=\"$PROGRAM?b=$BOARD&c=l&num=$Num&old=$NextOld\">$H_NEXTART</a></p>\n") if ($Old);
    }

    if (! @Lines) {

	# 空だった……
	print("<p>$H_NOARTICLE</p>\n");

    } else {

	@Lines = reverse(@Lines) unless ($SYS_BOTTOMARTICLE);

	foreach (@Lines) {

	    # 記事情報の取り出し
	    ($Id) = split(/\t/, $_, 2);

	    # 記事の表示(コマンド付き)
	    &ViewOriginalArticle($Id, 'command');
	    print("<hr>\n");

	}

    }

    if ($SYS_BOTTOMARTICLE) {
	print("<p>$H_BOTTOM<a href=\"$PROGRAM?b=$BOARD&c=l&num=$Num&old=$NextOld\">$H_NEXTART</a></p>\n") if ($Old);
    } else {
	print("<p>$H_BOTTOM<a href=\"$PROGRAM?b=$BOARD&c=l&num=$Num&old=$BackOld\">$H_BACKART</a></p>\n") if (@Lines && (($#Lines + 1) == $Num));
    }

    print(<<__EOF__);
<form action="$PROGRAM" method="POST">
<input name="b" type="hidden" value="$BOARD">
<input name="c" type="hidden" value="v">
<input name="num" type="hidden" value="$DEF_TITLE_NUM">
<input type="submit" value="$H_BACK">
</form>
__EOF__

    &MsgFooter();

}


###
## 記事の検索(表示画面作成)
#
sub SearchArticle {

    # キーワード，検索範囲を拾う
    local($Key, $SearchSubject, $SearchPerson, $SearchArticle, $SearchIcon, $Icon)
	= ($cgi'TAGS{'key'}, $cgi'TAGS{'searchsubject'},
	   $cgi'TAGS{'searchperson'}, $cgi'TAGS{'searcharticle'},
	   $cgi'TAGS{'searchicon'}, $cgi'TAGS{'icon'});

    # 表示画面の作成
    &MsgHeader("$BOARDNAME: $SEARCHARTICLE_MSG");

    # お約束
    print(<<__EOF__);
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
__EOF__

    printf("<li>$H_SEARCHTARGETSUBJECT: <input name=\"searchsubject\" type=\"checkbox\" value=\"on\" %s>\n", (($SearchSubject) ? 'CHECKED' : ''));
    printf("<li>$H_SEARCHTARGETPERSON: <input name=\"searchperson\" type=\"checkbox\" value=\"on\" %s>\n", (($SearchPerson) ? 'CHECKED' : ''));
    printf("<li>$H_SEARCHTARGETARTICLE: <input name=\"searcharticle\" type=\"checkbox\" value=\"on\" %s>", (($SearchArticle) ? 'CHECKED' : ''));

    printf("<li>$H_ICON: <input name=\"searchicon\" type=\"checkbox\" value=\"on\" %s> // ", (($SearchIcon) ? 'CHECKED' : ''));

    # アイコンの選択
    print("<SELECT NAME=\"icon\">\n");
    printf("<OPTION%s>$H_NOICON\n",
	   (($Icon && ($Icon ne $H_NOICON)) ? '' : ' SELECTED'));
	
    # 一つ一つ表示
    open(ICON, &GetIconPath("$BOARDDIR.$ICONDEF_POSTFIX"))
	|| (open(ICON, &GetIconPath("$DEFAULT_ICONDEF"))
	    || &Fatal(1, &GetIconPath("$DEFAULT_ICONDEF")));
    while(<ICON>) {
	# コメント文はキャンセル
	next if (/^\#/o);
	next if (/^$/o);
	chop;
	($FileName, $IconTitle) = split(/\t/, $_, 3);
	printf("<OPTION%s>$IconTitle\n",
	       (($Icon eq $IconTitle) ? ' SELECTED' : ''));
    }
    close(ICON);
    print("</SELECT>\n");

    # アイコン一覧
    print(<<__EOF__);
(<a href="$PROGRAM?b=$BOARD&c=i&type=entry">$H_SEEICON</a>)<BR>
</p>
</ul>
</form>
<hr>
__EOF__

    # キーワードが空でなければ，そのキーワードを含む記事のリストを表示
    if (($SearchIcon)
	|| (($Key) && ($SearchSubject || ($SearchPerson || $SearchArticle)))) {
	&SearchArticleList($Key, $SearchSubject, $SearchPerson, $SearchArticle,
			   $SearchIcon, $Icon);
    }

    &MsgFooter();

}


###
## 記事の検索(検索結果の表示)
#
sub SearchArticleList {

    # キーワード，検索範囲
    local($Key, $Subject, $Person, $Article, $Icon, $IconType) = @_;

    # DBファイル
    local($DBFile) = &GetPath($BOARD, $DB_FILE_NAME);

    local($dId, $dFid, $dAids, $dDate, $dTitle, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail);

    local($ArticleFile, $HitFlag) = ('', 0);
    local($Line) = '';
    local($SubjectFlag, $PersonFlag, $ArticleFlag);
    local(@KeyList) = split(/ +/, $Key);

    # リスト開く
    print("<ul>\n");

    # ファイルを開く．DBファイルがなければnot found.
    open(DB, "<$DBFile") || &Fatal(1, $DBFile);
    while(<DB>) {

	next if (/^\#/);
	next if (/^$/);

	# 変数のリセット
	$SubjectFlag = $PersonFlag = $ArticleFlag = 0;
	$Line = '';

	# 記事情報
	($dId, $dFid, $dAids, $dDate, $dTitle, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail) = split(/\t/, $_);

	# アイコンチェック
	next if (($Icon) && ($dIcon ne $IconType));

	if ($Key) {

	    # タイトルを検索
	    if ($Subject) {
		$SubjectFlag = 1;
		foreach (@KeyList) {
		    $SubjectFlag = 0 unless ($dTitle =~ /$_/i);
		}
	    }

	    # 投稿者名を検索
	    if ($Person) {
		$PersonFlag = 1;
		foreach (@KeyList) {
		    $PersonFlag = 0 unless ($dName =~ /$_/i);
		}
	    }

	    # 本文を検索
	    $ArticleFile = &GetArticleFileName($dId, $BOARD);
	    $ArticleFlag = 1 if ($Article && ($Line = &SearchArticleKeyword($ArticleFile, @KeyList)));

	} else {

	    # 無条件で一致
	    $SubjectFlag = 1;

	}

	if ($SubjectFlag || $PersonFlag || $ArticleFlag) {

	    # 最低1つは合致した
	    $HitFlag = 1;

	    # 記事へのリンクを表示
	    print("<li>" . &GetFormattedTitle($dId, $dAids, $dIcon, $dTitle, $dName, $dDate));

	    # 本文に合致した場合は本文も表示
	    if ($ArticleFlag) {
		$Line =~ s/<[^>]*>//go;
		print("<blockquote>$Line</blockquote>\n");
	    }
	}
    }
    close(DB);

    # ヒットしなかったら
    print("<li>$H_NOTFOUND\n") unless ($HitFlag == 1);

    # リスト閉じる
    print("</ul>\n");
}


###
## 記事の検索(本文)
#
sub SearchArticleKeyword {

    # ファイル名とキーワード
    local($File, @KeyList) = @_;
    local(@NewKeyList);
    local($Line, $Return) = ('', '');

    # 検索する
    open(ARTICLE, "<$File") || &Fatal(1, $File);
    while($Line = <ARTICLE>) {

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
    &MsgHeader($ALIASNEW_MSG);

    # 新規登録/登録内容の変更
    print(<<__EOF__);
<p>
$H_ALIASTITLE
</p>
<p>
<form action="$PROGRAM" method="POST">
<input name="c" type="hidden" value="am">
$H_ALIAS <input name="alias" type="text" value="#" size="$NAME_LENGTH"><br>
$H_FROM <input name="name" type="text" size="$NAME_LENGTH"><br>
$H_MAIL <input name="email" type="text" size="$MAIL_LENGTH"><br>
$H_URL <input name="url" type="text" value="http://" size="$URL_LENGTH"><br>
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
$H_ALIAS <input name="alias" type="text" size="$NAME_LENGTH"><br>
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
    &MsgFooter();

}


###
## 登録/変更
#
sub AliasMod {

    # エイリアス，名前，メール，URL
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
	
	# ホスト名が合ったら2，合わなきゃ1．
	$HitFlag = (($REMOTE_HOST eq $Host{$Alias}) ? 2 : 1);
    }
    
    # ホスト名が合わない!
    &Fatal(6, '') if ($HitFlag == 1);
    
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
	
	# ホスト名が合ったら2，合わなきゃ1．
	$HitFlag = (($REMOTE_HOST eq $Host{$Alias}) ? 2 : 1);
    }
    
    # ホスト名が合わない!
    &Fatal(6, '') if ($HitFlag == 1);
    
    # エイリアスがない!
    &Fatal(7, $A) if ($HitFlag == 0);
    
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
	print(<<__EOF__);
<p>
<dt><strong>$Alias</strong>
<dd>$H_FROM $Name{$Alias}
<dd>$H_MAIL $Email{$Alias}
<dd>$H_HOST $Host{$Alias}
<dd>$H_URL $URL{$Alias}
</p>
__EOF__

    }

    # リスト閉じる
    print("</dl>\n");
    
    &MsgFooter();

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
    open(ALIAS, "<$File") || &Fatal(1, $File);
    while(<ALIAS>) {
	
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
    open(ALIAS, ">$TmpFile") || &Fatal(1, $TmpFile);
    foreach $Alias (sort keys(%Name)) {
	($Name{$Alias}) && printf(ALIAS "%s\t%s\t%s\t%s\t%s\n",
				  $Alias, $Name{$Alias}, $Email{$Alias},
				  $Host{$Alias}, $URL{$Alias});
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

    open(HEADER, "<$File") || &Fatal(1, $File);
    while(<HEADER>){
        print("$_");
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
    local($ArticleId) = 0;

    open(AID, "<$ArticleNumFile") || &Fatal(1, $ArticleNumFile);
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

    open(AID, "$ArticleNumFile") || &Fatal(1, $ArticleNumFile);
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
    local($BoardName);

    open(ALIAS, "<$BOARD_ALIAS_FILE")
	|| &Fatal(1, $BOARD_ALIAS_FILE);
    while(<ALIAS>) {
	
	chop;
	next unless (/^$Alias\t(.*)$/);

	$BoardName = $1;
	return($BoardName);
    }
    close(ALIAS);

    # ヒットせず
    return('');
}


###
## タイトルリストのフォーマット
#
sub GetFormattedTitle {

    local($Id, $Aids, $Icon, $Title, $Name, $Date) = @_;
    local($String, $Fnum) = ('', 0);

    # リンク文字列
    local($Link) = "<a href=\"$PROGRAM?b=$BOARD&c=e&id=$Id\">$Title</a>";

    # まとめ読みリンク用文字列
    local($Thread) = (($Aids) ? " <a href=\"$PROGRAM?b=$BOARD&c=t&id=$Id\">$H_THREAD</a>" : '');

    if (($Icon eq $H_NOICON) || (! $Icon)) {
	$String = sprintf("<strong>$Id .</strong> $Link$Thread [$Name] $Date");
    } else {
	$String = sprintf("<strong>$Id .</strong> <img src=\"%s\" alt=\"$Icon\" width=\"$ICON_WIDTH\" height=\"$ICON_HEIGHT\">$Link$Thread [$Name] $Date", &GetIconURLFromTitle($Icon));
    }

    return($String);

}


###
## タイトルリストのフォーマット(簡略版)
#
sub GetFormattedAbstract {

    local($Id, $Icon, $Title, $Name, $Date) = @_;
    local($String) = '';

    if (($Icon eq $H_NOICON) || (! $Icon)) {
	$String = sprintf("<li><strong>$Id .</strong> $Title [$Name] $Date", &GetIconURLFromTitle($Icon));
    } else {
	$String = sprintf("<li><strong>$Id .</strong> <img src=\"%s\" alt=\"$Icon\" width=\"$ICON_WIDTH\" height=\"$ICON_HEIGHT\">$Title [$Name] $Date", &GetIconURLFromTitle($Icon));
    }

    return($String);
}


###
## 元記事情報の表示
#
sub ShowFormattedLinkToFollowedArticle {

    local($Src, $Icon, $Subject) = @_;

    # 参照先の取得
    local($Link) = ($Src =~ /^http:/) ? $Src : "$PROGRAM?b=$BOARD&c=e&id=$Src";

    if ($Src != 0) {
	if (($Icon eq $H_NOICON) || (! $Icon)) {
	    print("<strong>$H_REPLY</strong> [$BOARDNAME: $Src] <a href=\"$Link\">$Subject</a><br>\n");
	} else {
	    printf("<strong>$H_REPLY</strong> [$BOARDNAME: $Src] <img src=\"%s\" alt=\"$Icon\" width=\"$ICON_WIDTH\" height=\"$ICON_HEIGHT\"><a href=\"$Link\">$Subject</a><br>\n", &GetIconURLFromTitle($Icon));
	}
    } elsif ($Src =~ /^http:/) {
	print("<strong>$H_REPLY</strong> <a href=\"$Link\">$Link</a><br>\n");
    }
}


###
## 文字列チェック: エイリアス
#
sub CheckAlias {

    local($String) = @_;

    # 空チェック
    ($String eq '') && &Fatal(2, '');

    # `#'で始まってる?
    ($String =~ (/^#/)) || &Fatal(8, 'alias');

    # 1文字じゃだめ
    (length($String) > 1) || &Fatal(8, 'alias');

}


###
## 文字列チェック: タイトル
#
sub CheckSubject {

    local($String) = @_;

    # 空チェック
    ($String eq '') && &Fatal(2, '');

    # タグをチェック
    ($String =~ /</o) && &Fatal(4, '');

    # 改行コードをチェック
    ($String =~ /\n/o) && &Fatal(3, '');

}


###
## 文字列チェック: 名前
#
sub CheckName {

    local($String) = @_;

    # 空チェック
    ($String eq '') && &Fatal(2, '');

    # 改行コードをチェック
    ($String =~ /\n/o) && &Fatal(3, '');

}


###
## 文字列チェック: メール
#
sub CheckEmail {

    local($String) = @_;

    # 空チェック
    ($String eq '') && &Fatal(2, '');

    # `@'が入ってなきゃアウト
    ($String =~ (/@/)) || &Fatal(8, 'E-Mail');

    # 改行コードをチェック
    ($String =~ /\n/o) && &Fatal(3, '');

}


###
## 文字列チェック: URL
#
sub CheckURL {

    local($String) = @_;

    ($String =~ m#^http://.*$#) || ($String =~ m#^http://$#)
	|| ($String eq '') || &Fatal(8, 'URL');

}


###
## 記事のヘッダの表示
#
sub MsgHeader {

    # message and board
    local($Message) = @_;
    
    &cgi'header;
    print(<<__EOF__);
<html>
<head>
<!--陝 (0xF0A1): cool idea to euc decode error protection; thanks to faichan\@kt.rim.or.jp-->
<title>$Message</title>
<base href="http://$SERVER_NAME:$SERVER_PORT$SYSDIR_NAME">
</head>
<body bgcolor="$BG_COLOR" TEXT="$TEXT_COLOR" LINK="$LINK_COLOR" ALINK="$ALINK_COLOR" VLINK="$VLINK_COLOR">
<h1>$Message</h1>
<hr>
__EOF__

}


###
## 記事のフッタの表示
#
sub MsgFooter {

    print(<<__EOF__);
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

    local($TimeOut) = 0;
    local($Flag) = 0;

    srand(time|$$);

    open(LOCKORG, ">$LOCK_ORG") || &Fatal(1, $LOCK_ORG);
    close(LOCKORG);

    for($TimeOut = 0; $TimeOut < $LOCK_WAIT; $TimeOut++) {
	$Flag = 1, last if link($LOCK_ORG, $LOCK_FILE);
	select(undef, undef, undef, (rand(6)+5)/10);
    }

    unlink($LOCK_ORG);
    &Fatal(999, $TimeOut) unless ($Flag);

}

# アンロック
sub unlock {
    unlink($LOCK_FILE);
}


###
## 元記事の表示
#
sub ViewOriginalArticle {

    # Id，コマンドを表示するか否か
    local($Id, $Flag) = @_;

    # 引用するファイル
    local($QuoteFile) = &GetArticleFileName($Id, $BOARD);

    # 引用記事の情報
    local($rFid, $rAids, $rDate, $rSubject, $rIcon, $rRemoteHost, $rName, $rEmail, $rUrl, $rFmail);

    # 記事情報の取得
    local($Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $Fmail) = &GetArticlesInfo($Id);

    # 引用記事情報の抽出
    ($rFid, $rAids, $rDate, $rSubject, $rIcon, $rRemoteHost, $rName, $rEmail, $rUrl, $rFmail) = &GetArticlesInfo($Fid) if ($Fid != 0);

    # コマンド表示?
    if ($Flag && $SYS_COMMAND) {

	print(<<__EOF__);
<p>
<a href="$PROGRAM?b=$BOARD&c=f&id=$Id"><img src="$ICON_FOLLOW" alt="$H_REPLYTHISARTICLE" width="$ICON_WIDTH" height="$ICON_HEIGHT" BORDER="0"></a>
<a href="$PROGRAM?b=$BOARD&c=q&id=$Id"><img src="$ICON_QUOTE" alt="$H_REPLYTHISARTICLEQUOTE" width="$ICON_WIDTH" height="$ICON_HEIGHT" BORDER="0"></a>
<a href="$PROGRAM?b=$BOARD&c=t&id=$Id"><img src="$ICON_THREAD" alt="$H_READREPLYALL" width="$ICON_WIDTH" height="$ICON_HEIGHT" BORDER="0"></a>
<a href="$PROGRAM?b=$BOARD&c=i&type=article"><img src="$ICON_HELP" alt="?" width="$ICON_WIDTH" height="$ICON_HEIGHT" BORDER="0"></a>
</p>
__EOF__

    }

    # ボード名と記事番号，題
    if (($Icon eq $H_NOICON) || (! $Icon)) {
	print("<strong>$H_SUBJECT</strong> [$BOARDNAME: $Id] $Subject<br>\n");
    } else {
	printf("<strong>$H_SUBJECT</strong> [$BOARDNAME: $Id] <img src=\"%s\" alt=\"$Icon\" width=\"$ICON_WIDTH\" height=\"$ICON_HEIGHT\">$Subject<br>\n", &GetIconURLFromTitle($Icon));
    }

    # お名前
    if ((! $Url) || ($Url eq 'http://')) {
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
    open(TMP, "<$QuoteFile") || &Fatal(1, $QuoteFile);
    while(<TMP>) { print("$_"); }
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
    # (MacPerlでは「:$Borad:$Id」とすべきらしい)
    return(($Board) ? "$Board/$Id" : "$Id");

}


###
## ボード名称とファイル名から，そのファイルのパス名を作り出す．
#
sub GetPath {

    # BoardとFile
    local($Board, $File) = @_;

    # 返す(MacPerlでは「:$Board:$File」とすべきらしい)
    return("$Board/$File");

}


###
## アイコンファイル名から，そのファイルのパス名を作り出す．
#
sub GetIconPath {

    # BoardとFile
    local($File) = @_;

    # 返す(MacPerlでは「:$ICON_DIR:$File」とすべきらしい)
    return("$ICON_DIR/$File");

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

    local($FileName, $Title, $TargetFile) = ('', '', '');

    # 一つ一つ表示
    open(ICON, &GetIconPath("$BOARD.$ICONDEF_POSTFIX"))
	|| (open(ICON, &GetIconPath("$DEFAULT_ICONDEF"))
	    || &Fatal(1, &GetIconPath("$DEFAULT_ICONDEF")));
    while(<ICON>) {
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

    # DBファイル
    local($DBFile) = &GetPath($BOARD, $DB_FILE_NAME);

    local($dId, $dFid, $dAids, $dDate, $dTitle, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail);

    local($rFid, $rAids, $rDate, $rTitle, $rIcon, $rRemoteHost, $rName, $rEmail, $rUrl, $rFmail) = ('', '', '', '', '', '', '', '', '', '');

    # 取り込み．DBファイルがなければ0/''を返す．
    open(DB, "<$DBFile");
    while(<DB>) {

	next if (/^\#/);
	next if (/^$/);
	chop;

	($dId, $dFid, $dAids, $dDate, $dTitle, $dIcon, $dRemoteHost, $dName, $dEmail, $dUrl, $dFmail) = split(/\t/, $_);

	if ($Id == $dId) {
	    $rFid = $dFid;
	    $rAids = $dAids;
	    $rDate = $dDate;
	    $rTitle = $dTitle;
	    $rIcon = $dIcon;
	    $rRemoteHost = $dRemoteHost;
	    $rName = $dName;
	    $rEmail = $dEmail;
	    $rUrl = $dUrl;
	    $rFmail = $dFmail;
	}    
    }
    close(DB);

    return($rFid, $rAids, $rDate, $rTitle, $rIcon, $rRemoteHost, $rName, $rEmail, $rUrl, $rFmail);

}


###
## エラー表示
#
sub Fatal {

    # エラー番号とエラー情報の取得
    local($FatalNo, $FatalInfo) = @_;

    # 異常終了の可能性があるので，とりあえずlockを外す
    # (ロックの失敗の時以外)
    &unlock if ($FatalNo != 999);

    &MsgHeader($ERROR_MSG);
    
    if ($FatalNo == 1) {

	print("<p>
File: $FatalInfoが存在しない，
あるいはpermissionの設定が間違っています．
お手数ですが，<a href=\"mailto:$MAINT\">$MAINT</a>まで，
上記ファイル名をお知らせ下さい．
</p>\n");

    } elsif ($FatalNo == 2) {

	print("<p>
入力されていない項目があります．戻ってもう一度やり直してみてください．
</p>\n");

    } elsif ($FatalNo == 3) {

	print("<p>
題や名前，メールアドレスに，改行が入ってしまっています．
戻ってもう一度やり直してみてください．
</p>\n");

    } elsif ($FatalNo == 4) {

	print("<p>
題中にHTMLタグを入れることは禁じられています．
戻って違う題に書き換えてください．
</p>\n");

    } elsif ($FatalNo == 6) {

	print("<p>
登録されているエイリアスのものと，ホスト名が一致しません．
お手数ですが，<a href=\"mailto:$MAINT\">$MAINT</a>まで御連絡ください．
</p>\n");

    } elsif ($FatalNo == 7) {

	print("<p>
$FatalInfoというエイリアスは，登録されていません．
</p>\n");

    } elsif ($FatalNo == 8) {

	print("<p>
$FatalInfoがおかしくありませんか? 戻ってもう一度やり直してみてください．
</p>\n");

    } elsif ($FatalNo == 9) {

	print("<p>
メールが送信できませんでした．お手数ですが，このエラーが生じた状況を，
<a href=\"mailto:$MAINT\">$MAINT</a>までお知らせください．
</p>\n");

    } elsif ($FatalNo == 11) {

	print("<p>
次の記事はまだ投稿されていません．
</p>\n");

    } elsif ($FatalNo == 999) {

	print("<p>
システムのロックに失敗しました．
混み合っているようですので，しばらく待ってからもう一度アクセスしてください．
</p>\n");

    } else {

	print("<p>
エラー番号不定: お手数ですが，このエラーが生じた状況を，
<a href=\"mailto:$MAINT\">$MAINT</a>までお知らせください．
</p>\n");

    }
    
    &MsgFooter();
    exit 0;
}
