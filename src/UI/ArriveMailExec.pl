###
## ArriveMailExec - メイル自動配信先の設定
#
# - SYNOPSIS
#	ArriveMailExec;
#
# - ARGS
#	なし
#
# - DESCRIPTION
#	メイル自動配信先を設定する．
#	大域変数である，CGI変数を参照する．
#
# - RETURN
#	なし
#
ArriveMailExec: {

    local(@ArriveMail);

    @ArriveMail = split(/\n/, $cgi'TAGS{'armail'}); # 宛先リストを取り出す
    &UpdateArriveMailDb($BOARD, *ArriveMail); # DBを更新する

    &MsgHeader("ArriveMail Changed", "$BOARDNAME: 自動メイル配信先を設定しました");

    &cgiprint'Cache(<<__EOF__);
<p>
この$H_BOARDに$H_MESGが書き込まれた時に，自動でメイルを配信する宛先を，
以下のように設定しました．
</p><p>
<pre>
--------------------
__EOF__

    foreach(@ArriveMail) { &cgiprint'Cache("$_\n"); }

    &cgiprint'Cache(<<__EOF__);
--------------------
</pre></p>
__EOF__

    &PrintButtonToTitleList($BOARD);
    &PrintButtonToBoardList;

    &MsgFooter;

}

1;
