###
## AliasShow - ユーザエイリアス参照画面の表示
#
# - SYNOPSIS
#	AliasShow;
#
# - ARGS
#	なし
#
# - DESCRIPTION
#	ユーザエイリアスの一覧を表示する画面を作成する．
#
# - RETURN
#	なし
#
AliasShow: {

    local($Alias);

    # lock system
    local( $lockResult ) = &cgi'lock( $LOCK_FILE );
    &Fatal(1001, '') if ( $lockResult == 2 );
    &Fatal(999, '') if ( $lockResult != 1 );

    # エイリアスの読み込み
    &CashAliasData;

    # unlock system
    &cgi'unlock( $LOCK_FILE );
    
    # 表示画面の作成
    &MsgHeader('Alias view', "$H_ALIASの参照");

    # あおり文
    if ($SYS_ALIAS == 1) {
	&cgiprint'Cache(<<__EOF__);
<p>
投稿の際，「$H_FROM」の部分に以下の登録名(「#....」)を入力すると，
登録されている$H_FROMと$H_MAIL，$H_URLが自動的に補われます．
</p><p>
<a href="$PROGRAM?c=an">新規登録/登録内容の変更</a>
</p>
__EOF__

    } elsif ($SYS_ALIAS == 2) {
					  
	&cgiprint'Cache(<<__EOF__);
<p>
投稿の際，「$H_USER」で以下の登録名(「#....」)を指定すると，
登録されている$H_FROMと$H_MAIL，$H_URLが自動的に補われます．
</p><p>
<a href="$PROGRAM?c=an">新規登録/登録内容の変更</a>
</p>
__EOF__

    } else {
	# ありえない，はず
	&Fatal(9999, '');
    }

    # リスト開く
    &cgiprint'Cache("<dl>\n");
    
    # 1つずつ表示
    foreach $Alias (sort keys(%Name)) {
	&cgiprint'Cache(<<__EOF__);
<p>
<dt><strong>$Alias</strong>
<dd>$H_FROM: $Name{$Alias}
<dd>$H_MAIL: $Email{$Alias}
<dd>$H_URL: $URL{$Alias}
</p>
__EOF__

    }

    # リスト閉じる
    &cgiprint'Cache("</dl>\n");
    
    &MsgFooter;

}

1;
