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
AliasDel:
{
    # エイリアス
    local( $alias ) = $cgi'TAGS{'alias'};

    # マシンがマッチしたか
    #	0 ... エイリアスがマッチしない
    #	2 ... マッチしてデータを変更した
    local( $hitFlag ) = 0;

    &LockAll();

    # エイリアスの読み込み
    &CacheAliasData;
    
    # 1行ずつチェック
    foreach (sort keys( %Name ))
    {
	next if ( $_ ne $alias );
	$hitFlag = 2;		# 合ったら2を設定．
    }
    
    # エイリアスがない!
    if ( $hitFlag == 0 ) { &Fatal( 6, $alias ); }
    
    # 名前を消す
    $Name{$alias} = '';
    
    # エイリアスファイルに書き出し
    &WriteAliasData;
    
    &UnlockAll();

    # 表示画面の作成
    &MsgHeader( 'Alias deleted', "$H_ALIASが削除されました" );
    &cgiprint'Cache("<p>$H_ALIAS: <strong>$alias</strong>: 消去しました．</p>\n");
    &MsgFooter;
}

1;
