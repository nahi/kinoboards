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
AliasDel: {

    local($A, $HitFlag, $Alias);

    # lock system
    local( $lockResult ) = $PC ? 1 : &cgi'lock( $LOCK_FILE );
    &Fatal(1001, '') if ( $lockResult == 2 );
    &Fatal(999, '') if ( $lockResult != 1 );

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
    
    # unlock system
    &cgi'unlock( $LOCK_FILE ) unless $PC;

    # 表示画面の作成
    &MsgHeader('Alias deleted', "$H_ALIASが削除されました");
    &cgiprint'Cache("<p>$H_ALIAS: <strong>$A</strong>: 消去しました．</p>\n");
    &MsgFooter;

}

1;
