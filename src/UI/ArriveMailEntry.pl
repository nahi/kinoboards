###
## ArriveMailEntry - メイル自動配信先の指定
#
# - SYNOPSIS
#	ArriveMailEntry;
#
# - ARGS
#	なし
#
# - DESCRIPTION
#	メイル自動配信先の指定画面を表示する．
#
# - RETURN
#	なし
#
ArriveMailEntry:
{
    local(@ArriveMail);

    &LockBoard;
    &GetArriveMailTo(1, $BOARD, *ArriveMail); # 宛先とコメントを取り出す
    &UnlockBoard;

    &MsgHeader("ArriveMail Entry", "自動メイル配信先の設定");
    &cgiprint'Cache(<<__EOF__);
<p>
この$H_BOARDに$H_MESGが書き込まれた時に，
自動でメイルを配信する宛先のメイルアドレスを設定します．
1行に1メイルアドレスずつ書き込んでください．
行頭に「#」をつけるとその行は無視されるので，
#に続けてコメントを書き込むこともできます．
</p><p>
特に実害はありませんが，無意味な空行が入りすぎないように注意しましょう．
</p>
__EOF__

    local( %tags, $msg, $str );
    $msg = "<textarea name=\"armail\" rows=\"$TEXT_ROWS\" cols=\"$MAIL_LENGTH\">\n";
    foreach ( @ArriveMail ) { $msg .= "$_\n"; }
    $msg .= "</textarea><br>";

    %tags = ( 'c', 'me', 'b', $BOARD );
    &TagForm( *str, *tags, "設定します", "リセットする", *msg );
    &cgiprint'Cache( $str );

    &MsgFooter;
}

1;
