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

1;
