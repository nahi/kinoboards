###
## Entry - 書き込み画面の表示
#
# - SYNOPSIS
#	Entry( $entryType, $back );
#
# - ARGS
#	$entryType	0 ... 新着
#			1 ... 引用なしのリプライ
#			2 ... 引用ありのリプライ
#			3 ... 投稿済み記事の訂正
#	$back		プレビューからの戻りか否か．
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
    local( $entryType, $back ) = ( $gVarEntryType, $gVarBack );

    &LockBoard;
    # cache article DB
    &DbCache( $BOARD ) if ( $BOARD && ( $entryType != 0 ));

    local( $Id ) = $cgi'TAGS{'id'};
    local( $COrig ) = $cgi'TAGS{'c'};

    local( $DefSubject, $DefName, $DefEmail, $DefUrl, $DefTextType, $DefIcon, $DefArticle, $DefFmail );
    if ( $back )
    {
	require( 'mimer.pl' );
	$DefSubject = $cgi'TAGS{'subject'};
	$DefName = $cgi'TAGS{'name'};
	$DefEmail = $cgi'TAGS{'mail'};
	$DefUrl = $cgi'TAGS{'url'};
	$DefTextType = $cgi'TAGS{'texttype'};
	$DefIcon = $cgi'TAGS{'icon'};
	$DefArticle = $cgi'TAGS{'article'};
	$DefFmail = $cgi'TAGS{'fmail'};

	$DefArticle = &MIME'base64decode( $DefArticle );
    }
    elsif ( $entryType == 0 )
    {
	if ( $SYS_ALIAS == 3 )
	{
	    &cgi'Cookie();
	    ( $DefName, $DefEmail, $DefUrl ) = split( /$COLSEP/,
		$cgi'COOKIES{ 'kb10info' });
	}
	$DefUrl = $DefUrl || 'http://';
    }
    elsif ( $entryType == 1 )
    {
	if ( $SYS_ALIAS == 3 )
	{
	    &cgi'Cookie();
	    ( $DefName, $DefEmail, $DefUrl ) = split( /$COLSEP/,
		$cgi'COOKIES{ 'kb10info' });
	}
	$DefUrl = $DefUrl || 'http://';
	local( $fId, $aids, $date, $subject ) = &GetArticlesInfo( $Id );
	$DefSubject = $subject;
	&GetReplySubject( *DefSubject );
    }
    elsif ( $entryType == 2 )
    {
	if ( $SYS_ALIAS == 3 )
	{
	    &cgi'Cookie();
	    ( $DefName, $DefEmail, $DefUrl ) = split( /$COLSEP/,
		$cgi'COOKIES{ 'kb10info' });
	}
	$DefUrl = $DefUrl || 'http://';
	local( $fId, $aids, $date, $subject ) = &GetArticlesInfo( $Id );
	$DefSubject = $subject;
	&GetReplySubject( *DefSubject );
	&QuoteOriginalArticle( $Id, *DefArticle );
    }
    elsif ( $entryType == 3 )
    {
	local( $fId, $aids, $date, $subject, $icon, $remoteHost, $name, $email, $url ) = &GetArticlesInfo( $Id );
	$DefSubject = $subject;
	$DefName = $name;
	$DefEmail = $email;
	$DefUrl = $url;
	$DefIcon = $icon;
	&QuoteOriginalArticleWithoutQMark( $Id, *DefArticle );
    }

    &UnlockBoard;

    # 表示画面の作成
    if ( $entryType == 3 )
    {
	&MsgHeader( 'Supersede entry', "$H_MESGの訂正" );
    }
    else
    {
	&MsgHeader( 'Message entry', "$H_MESGの書き込み" );
    }

    # フォローの場合
    if (( $entryType == 1 ) || ( $entryType == 2 ))
    {
	# 記事の表示(コマンド無し, 元記事あり)
	&ViewOriginalArticle( $Id, 0, 1 );
	if ( $entryType == 3 )
	{
	    &cgiprint'Cache(<<__EOF__);
$H_HR
<h2>上の$H_MESGを訂正する</h2>
上の$H_MESGと入れ換える$H_MESGを書き込んでください．
__EOF__
	}
	else
	{
	    &cgiprint'Cache(<<__EOF__);
$H_HR
<h2>上の$H_MESGへの$H_REPLYを書き込む</h2>
__EOF__
	}
    }

    local( $ttFlag ) = 0;
    local( $ttBit ) = 0;
    
    local( $note );
    $note = "<p>\n";
    foreach ( @H_TTMSG )
    {
	if (( $SYS_TEXTTYPE & ( 2**$ttBit )) &&
	    ( $SYS_TEXTTYPE ^ ( 2** $ttBit )))
	{
	    $ttFlag = 1;	# 後で使う．きたない．．．
	    $note .= $H_TTMSG[$ttBit] . "\n";
	}
	$ttBit++;
    }
    $note .= "</p>\n";
    $note = '' unless $ttFlag;

    $note .=<<__EOF__;
<p>
$H_URLを入力すると，$H_FROMからリンクを張ります．省略しても構いません．
</p>
__EOF__

    local( $msg );
    # &TagForm()により，FORMタグの内側に<p>が自動付加されるため，
    # ここではparagraphのstart tagをいれない．
    $msg = '';

    # アイコンの選択
    if ( $SYS_ICON )
    {
	&CacheIconDb( $BOARD );	# アイコンDBをキャッシュ
	$msg .= sprintf( "$H_ICON:\n<select name=\"icon\">\n<option%s>$H_NOICON\n", $DefIcon? '' : ' selected' );
	local( $IconTitle );
	foreach $IconTitle ( @ICON_TITLE )
	{
	    $msg .= sprintf( "<option%s>$IconTitle\n",
		( $IconTitle eq $DefIcon )? ' selected' : '' );
	}
	$msg .= "</select>\n";

	$msg .= "(" . &TagA( "$PROGRAM?b=$BOARD&c=i&type=entry",
	    "使えるアイコン一覧" ) . ")<br>\n";
    }

    # Subject(フォローなら自動的に文字列を入れる)
    $msg .= "$H_SUBJECT: <input name=\"subject\" type=\"text\" value=\"$DefSubject\" size=\"$SUBJECT_LENGTH\"><br>\n";

    # 書き込み形式
    if ( $ttFlag )
    {
	$ttFlag = 0 if $DefTextType;
	$msg .= "$H_TEXTTYPE:\n<select name=\"texttype\">\n";
	$ttBit = 0;
	foreach ( @H_TTLABEL )
	{
	    if ( $SYS_TEXTTYPE & ( 2 ** $ttBit ))
	    {
		if ( $ttFlag )
		{
		    $ttFlag = 0;	# now, using for a flag for the first.
		    $msg .= "<option selected>" . $H_TTLABEL[$ttBit] . "\n";
		}
		else
		{
		    $msg .= sprintf( "<option%s>" . $H_TTLABEL[$ttBit] . "\n",
			( $H_TTLABEL[$ttBit] eq $DefTextType )? ' selected' :
			'' );
		}
	    }
	    $ttBit++;
	}
	$msg .= "</select>\n<br>\n";
    }
    else
    {
	$msg .= sprintf( "<input name=\"texttype\" type=\"hidden\" value=\"%s\">\n", $H_TTLABEL[(( log $SYS_TEXTTYPE ) / ( log 2 ))] );
    }

    # 本文
    $msg .= "<textarea name=\"article\" rows=\"$TEXT_ROWS\" cols=\"$TEXT_COLS\">$DefArticle</textarea><br>\n";

    if ( $SYS_ALIAS == 0 )
    {
	# エイリアスは使わない
	$msg .=<<__EOF__;
$H_FROM: <input name="name" type="text" value="$DefName" size="$NAME_LENGTH"><br>
$H_MAIL: <input name="mail" type="text" value="$DefEmail" size="$MAIL_LENGTH"><br>
$H_URL: <input name="url" type="text" value="$DefUrl" size="$URL_LENGTH"><br>
__EOF__
    }
    elsif ( $SYS_ALIAS == 1 )
    {
	# エイリアスを使う
	$msg .=<<__EOF__;
$H_FROM: <input name="name" type="text" value="$DefName" size="$NAME_LENGTH"><br>
$H_MAIL: <input name="mail" type="text" value="$DefEmail" size="$MAIL_LENGTH"><br>
$H_URL: <input name="url" type="text" value="$DefUrl" size="$URL_LENGTH"><br>
__EOF__

	$note .=<<__EOF__;
<p>
「$H_ALIAS」に，$H_FROMと$H_MAIL，$H_URLを登録なさっている方は，
「$H_FROM」に「#...」という登録名を書いてください．
自動的に$H_FROMと$H_MAIL，$H_URLが補われます．
__EOF__

	$note .= "(" . &TagA( "$PROGRAM?c=as", "$H_ALIASの一覧" ) . " // \n";
	$note .= &TagA( "$PROGRAM?c=an", "$H_ALIASを登録" ) . ")\n</p>\n";
    }
    elsif ( $SYS_ALIAS == 2 )
    {
	# エイリアスを登録しなければ書き込みできない
	# エイリアスの読み込み
	&LockAll;
	&CacheAliasData;
	&UnlockAll;
	$msg .=<<__EOF__;
$H_USER:
<select name="name">
<option selected>$H_FROMを登録した$H_ALIASを選んでください
__EOF__

	local( $Key, $Value );
	while (( $Key, $Value ) = each %Name )
	{
	    $msg .= "<option>$Key\n";
	}
	$msg .=<<__EOF__;
</select>
__EOF__

	$note .=<<__EOF__;
<p>
予め「$H_ALIAS」に，$H_FROMと$H_MAIL，$H_URLを登録しないと書き込めません．
登録した後，「#...」という登録名を指定してください．
__EOF__

	$note .= "(" . &TagA( "$PROGRAM?c=as", "$H_ALIASの一覧" ) . " // \n";
	$note .=&TagA( "$PROGRAM?c=an", "$H_ALIASを登録" ) . ")<br>\n";
	$note .=<<__EOF__;
登録した$H_ALIASが表示されない(選択できない)場合，
このページを再読み込みしてください．
</p>
__EOF__
    }
    else
    {
	# HTTP-Cookiesを使う．
	$msg .=<<__EOF__;
<input name="cookies" type="hidden" value="on">
$H_FROM: <input name="name" type="text" value="$DefName" size="$NAME_LENGTH"><br>
$H_MAIL: <input name="mail" type="text" value="$DefEmail" size="$MAIL_LENGTH"><br>
$H_URL: <input name="url" type="text" value="$DefUrl" size="$URL_LENGTH"><br>
__EOF__

	$note .=<<__EOF__;
<p>
あなたのブラウザが「HTTP-Cookiesを使う」設定になっている場合，
上で入力した$H_FROM，$H_MAIL，$H_URLが
あなたのブラウザ中に記憶されます．
次回の書き込みの際は，その記憶された情報を利用できます．
</p>
__EOF__
    }

    if ( $SYS_MAIL & 2 )
    {
	$msg .= "この$H_MESGに$H_REPLYがあった時に，上の宛先にメイルで知らせますか? ";
	$msg .= sprintf( "<input name=\"fmail\" type=\"checkbox\" value=\"on\"%s></p>\n", $DefFmail? ' CHECKED' : '' );
    }
    
    # ボタン
    $msg .=<<__EOF__;
<input type="radio" name="com" value="p" CHECKED>: 試しに表示してみる(まだ投稿しません)<br>
__EOF__

    if ( $entryType == 3 )
    {
	$msg .= "<input type=\"radio\" name=\"com\" value=\"x\">: 訂正する<br>\n";
    }
    else
    {
	$msg .= "<input type=\"radio\" name=\"com\" value=\"x\">: $H_MESGを投稿する<br>\n";
    }

    local( %tags, $str );
    local( $op ) = ( -M $BOARD_ALIAS_FILE );
    %tags = ( 'corig', $COrig, 'b', $BOARD, 'c', 'p', 'id', $Id,
	's', ( $entryType == 3 ), 'op', $op );
    &TagForm( *str, *tags, "実行", '', *msg );

    # 注意書きいろいろ
    $note .=<<__EOF__;
<p>
$H_MESG中に関連ウェブページへのリンクを張る場合は，
「&lt;URL:http://〜&gt;」のように，URLを「&lt;URL:」と「&gt;」で囲んで
書き込んでください．自動的にリンクが張られます．
この$H_BOARDの中の$H_MESGにリンクを張る場合は，「&lt;URL:kb:71&gt;」のように，
$H_MESGのIDを「&lt;URL:kb:」と「&gt;」で囲みます．
__EOF__

    if ( $SYS_F_S )
    {
	$note .= "この$H_BOARDの中の$H_MESGは\n";
	$note .= &TagA( "$PROGRAM?b=$BOARD&c=s", "キーワードで検索する" );
	$note .= "ことができます．\n";
    }
    $note .= "</p>\n";

    $str .= "$H_HR\n$note" if $note;

    &cgiprint'Cache( $str );

    &MsgFooter;
}

1;
