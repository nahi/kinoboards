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
AliasMod: {

    local( $alias, $name, $eMail, $url, $hitFlag );

    $alias = $cgi'TAGS{'alias'};
    $name = $cgi'TAGS{'name'};
    $eMail = $cgi'TAGS{'email'};
    $url = $cgi'TAGS{'url'};
    
    # マシンがマッチしたか
    #	0 ... エイリアスがマッチしない
    #	2 ... マッチしてデータを変更した
    $hitFlag = 0;

    # 文字列チェック
    &AliasCheck( $alias, $name, $eMail, $url );
    
    # エイリアスの読み込み
    &CashAliasData;
    
    # 1行ずつチェック
    foreach (sort keys(%Name)) {
	next if ( $_ ne $alias );
	$hitFlag = 2;		# 合ったら2を設定．
    }
    
    # データの登録
    $Name{ $alias } = $name;
    $Email{ $alias } = $eMail;
    $Host{ $alias } = $cgi'REMOTE_HOST;
    $URL{ $alias } = $url;
    
    # エイリアスファイルに書き出し
    &WriteAliasData;

    # 表示画面の作成
    &MsgHeader( 'Alias modified', "$H_ALIASが設定されました" );

    &cgiprint'Cache( "<p>$H_ALIAS: <strong>$alias</strong>:\n" );
    if ( $hitFlag == 2 ) {
	&cgiprint'Cache( "登録を変更しました．</p>\n" );
    } else {
	&cgiprint'Cache( "新規に登録しました．</p>\n" );
    }

    &cgiprint'Cache(<<__EOF__);
<p>
<dl>
<dt>$H_FROM
<dd>$name
<dt>$H_MAIL
<dd>$eMail
<dt>$H_URL
<dd>$url
</dl>
</p>
__EOF__

    &MsgFooter;
    
}

1;
