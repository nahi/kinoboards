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
Entry: {
    local($QuoteFlag) = $gVarQuoteFlag;
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
    if ($Supersede && $SYS_F_D) {
	&MsgHeader('Supersede entry', "$BOARDNAME: $H_MESGの訂正");
    } else {
	&MsgHeader('Message entry', "$BOARDNAME: $H_MESGの書き込み");
    }

    # フォローの場合
    if ($QuoteFlag != 0) {
	# 記事の表示(コマンド無し, 元記事あり)
	&ViewOriginalArticle($Id, 0, 1);
	if ($Supersede && $SYS_F_D) {
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
    if ($Supersede && $SYS_F_D) {
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
	&CashIconDb($BOARD);	# アイコンDBをキャッシュ
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
    if ($Supersede && $SYS_F_D) {
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

    if ($Supersede && $SYS_F_D) {
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

1;
