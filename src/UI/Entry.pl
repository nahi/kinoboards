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
Entry:
{
    local( $QuoteFlag ) = $gVarQuoteFlag;

    local( $Id, $Supersede, $IconTitle, $Key, $Value, $Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url, $DefSubject, $DefName, $DefEmail, $DefUrl, $ttBit, $ttFlag );

    # lock system
    local( $lockResult ) = $PC ? 1 : &cgi'lock( $LOCK_FILE_B );
    &Fatal(1001, '') if ( $lockResult == 2 );
    &Fatal(999, '') if ( $lockResult != 1 );
    # cache article DB
    if ( $BOARD ) { &DbCache( $BOARD ); }

    $Id = $cgi'TAGS{'id'};
    $Supersede = $cgi'TAGS{'s'}; # 訂正?
    if ($QuoteFlag != 0)
    {
	($Fid, $Aids, $Date, $Subject, $Icon, $RemoteHost, $Name, $Email, $Url) = &GetArticlesInfo($Id);
    }
    $Icon = $Icon || $H_NOICON;

    if ( $Supersede )
    {
	$DefSubject = $Subject;
	$DefName = $Name;
	$DefEmail = $Email;
	$DefUrl = $Url;
    }
    else
    {
	$DefSubject = (( $QuoteFlag == 0 ) ? '' : &GetReplySubject( $Id ));

	if ( $SYS_ALIAS == 3 )
	{
	    &cgi'Cookie();
	    ( $DefName, $DefEmail, $DefUrl ) = split( /$COLSEP/, $cgi'COOKIES{ 'kb10info' });;
	    $DefUrl = $DefUrl || 'http://';
	}
	else
	{
	    $DefName = $DefEmail = '';
	    $DefUrl = 'http://';
	}
    }

    # 表示画面の作成
    if ( $Supersede && $SYS_F_D )
    {
	&MsgHeader( 'Supersede entry', "$H_MESGの訂正" );
    }
    else
    {
	&MsgHeader( 'Message entry', "$H_MESGの書き込み" );
    }

    # フォローの場合
    if ( $QuoteFlag != 0 )
    {
	# 記事の表示(コマンド無し, 元記事あり)
	&ViewOriginalArticle( $Id, 0, 1 );
	if ( $Supersede && $SYS_F_D )
	{
	    &cgiprint'Cache( "$H_HR\n<h2>上の$H_MESGを訂正する</h2>" );
	}
	else
	{
	    &cgiprint'Cache( "$H_HR\n<h2>上の$H_MESGへの$H_REPLYを書き込む</h2>" );
	}
    }

    local( $msg ) = "<p>\n";

    $msg .="上の$H_MESGと入れ換える$H_MESGを書き込んでください．\n"
	if ( $Supersede && $SYS_F_D );

    $ttFlag = 0;
    $ttBit = 0;
    foreach ( @H_TTMSG )
    {
	if (( $SYS_TEXTTYPE & ( 2**$ttBit )) &&
	    ( $SYS_TEXTTYPE ^ ( 2** $ttBit )))
	{
	    $ttFlag = 1;
	    $msg .= $H_TTMSG[$ttBit] . "\n";
	}
	$ttBit++;
    }

    $msg .= "</p>\n<p>\n$H_BOARD: $BOARDNAME<br>\n";

    # アイコンの選択
    if ( $SYS_ICON )
    {
	&CacheIconDb( $BOARD );	# アイコンDBをキャッシュ
	$msg .= "$H_ICON:\n<SELECT NAME=\"icon\">\n<OPTION SELECTED>$H_NOICON\n";
	foreach $IconTitle ( @ICON_TITLE )
	{
	    $msg .= "<OPTION>$IconTitle\n";
	}
	$msg .= "</SELECT>\n";

	$msg .= "(" . &TagA( "$PROGRAM?b=$BOARD&c=i&type=entry", "アイコンの説明" ) . ")<BR>\n";
    }

    # Subject(フォローなら自動的に文字列を入れる)
    $msg .= sprintf( "%s: <input name=\"subject\" type=\"text\" value=\"%s\" size=\"%s\"><br>\n", $H_SUBJECT, $DefSubject, $SUBJECT_LENGTH );

    # TextType
    if ( $ttFlag )
    {
	$msg .= "$H_TEXTTYPE:\n<SELECT NAME=\"texttype\">\n";
	$ttBit = 0;
	foreach ( @H_TTLABEL )
	{
	    if ( $SYS_TEXTTYPE & ( 2 ** $ttBit ))
	    {
		if ( $ttFlag )
		{
		    $ttFlag = 0;	# now, using for a flag for the first.
		    $msg .= "<OPTION SELECTED>" . $H_TTLABEL[$ttBit] . "\n";
		}
		else
		{
		    $msg .= "<OPTION>" . $H_TTLABEL[$ttBit] . "\n";
		}
	    }
	    $ttBit++;
	}
	$msg .= "</SELECT>\n</p>\n";
    }
    else
    {
	$msg .= sprintf( "<input name=\"texttype\" type=\"hidden\" value=\"%s\">\n", $H_TTLABEL[(( log $SYS_TEXTTYPE ) / ( log 2 ))] );
    }

    # 本文(引用ありなら元記事を挿入)
    $msg .= "<p><textarea name=\"article\" rows=\"$TEXT_ROWS\" cols=\"$TEXT_COLS\">";
    if ( $Supersede && $SYS_F_D )
    {
	&QuoteOriginalArticleWithoutQMark( $Id, *msg );
    }
    elsif ( $QuoteFlag == 2 )
    {
	&QuoteOriginalArticle( $Id, *msg );
    }

    $msg .= "</textarea></p>\n";

    # フッタ部分を表示
    # 名前とメイルアドレス，URL．
    $msg .=<<__EOF__;
<p>
$H_MESG中に関連ウェブページへのリンクを張る場合は，
「&lt;URL:http://〜&gt;」のように，URLを「&lt;URL:」と「&gt;」で囲んで
書き込んでください．自動的にリンクが張られます．
__EOF__

    if ( $SYS_F_S )
    {
	$msg .= "この$H_BOARDの中の$H_MESGにリンクを張る場合は\n";
	$msg .= &TagA( "$PROGRAM?b=$BOARD&c=s", "検索機能を使う" );
	$msg .= "と便利です．探し出した$H_MESGのURLを，「&lt;URL:」と「&gt;」で囲んでください．\n";
    }

    $msg .= "</p>\n";

    if ( $SYS_ALIAS == 0 )
    {
	# エイリアスは使わない
	$msg .=<<__EOF__;
<p>
$H_FROM: <input name="name" type="text" value="$DefName" size="$NAME_LENGTH"><br>
$H_MAIL: <input name="mail" type="text" value="$DefEmail" size="$MAIL_LENGTH"><br>
$H_URL_S:<br>
<input name="url" type="text" value="$DefUrl" size="$URL_LENGTH"><br>
</p>
__EOF__
    }
    elsif ( $SYS_ALIAS == 1 )
    {
	# エイリアスを使う
	$msg .= <<__EOF__;
<p>
$H_FROM: <input name="name" type="text" value="$DefName" size="$NAME_LENGTH"><br>
$H_MAIL: <input name="mail" type="text" value="$DefEmail" size="$MAIL_LENGTH"><br>
$H_URL_S:<br>
<input name="url" type="text" value="$DefUrl" size="$URL_LENGTH">
</p>
<p>
「$H_ALIAS」に，$H_FROMと$H_MAIL，$H_URLを登録なさっている方は，
「$H_FROM」に「#...」という登録名を書いてください．
自動的に$H_FROMと$H_MAIL，$H_URLが補われます．
__EOF__

	$msg .= "(" . &TagA( "$PROGRAM?c=as", "$H_ALIASの一覧" ) . " // \n";
	$msg .= &TagA( "$PROGRAM?c=an", "$H_ALIASを登録" ) . ")\n</p>\n";
    }
    elsif ( $SYS_ALIAS == 2 )
    {
	# エイリアスを登録しなければ書き込みできない
	# エイリアスの読み込み
	&CacheAliasData;
	$msg .=<<__EOF__;
<p>
$H_USER:
<SELECT NAME="name">
<OPTION SELECTED>$H_FROMを登録した$H_ALIASを選んでください
__EOF__

	while (( $Key, $Value ) = each %Name )
	{
	    $msg .= "<OPTION>$Key\n";
	}
	$msg .=<<__EOF__;
</SELECT>
</p>
<p>
予め「$H_ALIAS」に，$H_FROMと$H_MAIL，$H_URLを登録しないと書き込めません．
登録した後，「#...」という登録名を指定してください．
__EOF__

	$msg .= "(" . &TagA( "$PROGRAM?c=as", "$H_ALIASの一覧" ) . " // \n";
	$msg .=&TagA( "$PROGRAM?c=an", "$H_ALIASを登録" ) . ")<br>\n";
	$msg .=<<__EOF__;
登録した$H_ALIASが表示されない(選択できない)場合，
このページを再読み込みしてください．
</p>
__EOF__
    }
    else
    {
	# HTTP-Cookiesを使う．
	$msg .=<<__EOF__;
<p>
<input name="cookies" type="hidden" value="on">
$H_FROM: <input name="name" type="text" value="$DefName" size="$NAME_LENGTH"><br>
$H_MAIL: <input name="mail" type="text" value="$DefEmail" size="$MAIL_LENGTH"><br>
$H_URL_S:<br>
<input name="url" type="text" value="$DefUrl" size="$URL_LENGTH">
</p>
<p>
あなたのブラウザが「HTTP-Cookiesを使う」設定になっている場合，
ここで指定した$H_FROM，$H_MAIL，$H_URLが
あなたのブラウザ中に記憶されます．
次回の書き込みの際は，その記憶された情報を利用できます．
</p>
__EOF__
    }

    if ( $SYS_MAIL & 2 )
    {
	$msg .= "<p>$H_REPLYがあった時にメイルで知らせますか? <input name=\"fmail\" type=\"checkbox\" value=\"on\"></p>\n";
    }
    
    # unlock system
    &cgi'unlock( $LOCK_FILE_B ) unless $PC;

    # ボタン
    $msg .=<<__EOF__;
<input type="radio" name="com" value="p" CHECKED>: 試しに表示してみる(まだ投稿しません)<br>
__EOF__

    if ( $Supersede && $SYS_F_D )
    {
	$msg .= "<input type=\"radio\" name=\"com\" value=\"x\">: 訂正します<br>\n";
    }
    else
    {
	$msg .= "<input type=\"radio\" name=\"com\" value=\"x\">: $H_MESGを投稿する<br>\n";
    }

    local( %tags, $str );
    local( $op ) = ( -M $BOARD_ALIAS_FILE );
    %tags = ( 'b', $BOARD, 'c', 'p', 'id', $Id, 's', $Supersede, 'op', $op );
    &TagForm( *str, *tags, "実行", '', *msg );
    &cgiprint'Cache( $str );

    &MsgFooter;
}

1;
