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
SearchArticle: {

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
    &CashIconDb($BOARD);	# アイコンDBのキャッシュ
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

1;
