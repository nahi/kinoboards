###
## AliasNew - エイリアスの登録と変更画面の表示
#
# - SYNOPSIS
#	AliasNew;
#
# - ARGS
#	なし
#
# - DESCRIPTION
#	エイリアスの登録と変更画面を表示する(表示するだけ)．
#
# - RETURN
#	なし
#
AliasNew: {

    # 表示画面の作成
    &MsgHeader('Alias entry/edit', "$H_ALIASの登録/変更/削除");

    # 新規登録/登録内容の変更
    &cgiprint'Cache(<<__EOF__);
<p>
新規登録/登録内容の変更
</p>
<p>
<form action="$PROGRAM" method="POST">
<input name="c" type="hidden" value="am">
$H_ALIAS: <input name="alias" type="text" value="#" size="$NAME_LENGTH"><br>
$H_FROM: <input name="name" type="text" size="$NAME_LENGTH"><br>
$H_MAIL: <input name="email" type="text" size="$MAIL_LENGTH"><br>
$H_URL_S:<br>
<input name="url" type="text" value="http://" size="$URL_LENGTH"><br>
$H_ALIASの新規登録/登録内容の変更を行ないます．
エイリアスは(あなた以外の!)誰にでも書き換えることができます．
登録内容が変更されていないかどうか，
書き込む時の「試しに表示する」画面を注意してチェックしてください．
また，間違って同じエイリアスを登録されてしまわないように，
あまりに簡単な「エイリアス」は避けてくださいね．<br>
<input type="submit" value="登録/変更する">
</form>
</p>
<hr>
<p>
削除
</p>
<p>
<form action="$PROGRAM" method="POST">
<input name="c" type="hidden" value="ad">
$H_ALIAS: <input name="alias" type="text" size="$NAME_LENGTH"><br>
上記$H_ALIASを削除します．<br>
<input type="submit" value="削除する">
</form>
</p>
<hr>
<p>
<form action="$PROGRAM" method="POST">
<input name="c" type="hidden" value="as">
<input type="submit" value="$H_ALIAS一覧を参照する">
</form>
</p>
__EOF__
    
    # お約束
    &MsgFooter;

}

1;
