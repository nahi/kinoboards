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
ArriveMailEntry: {

    local(@ArriveMail);

    # lock system
    local( $lockResult ) = &cgi'lock( $LOCK_FILE );
    &Fatal(1001, '') if ( $lockResult == 2 );
    &Fatal(999, '') if ( $lockResult != 1 );

    &GetArriveMailTo(1, $BOARD, *ArriveMail); # 宛先とコメントを取り出す

    # unlock system
    &cgi'unlock( $LOCK_FILE );

    &MsgHeader("ArriveMail Entry", "$BOARDNAME: 自動メイル配信先の設定");

    &cgiprint'Cache(<<__EOF__);
<p>
この$H_BOARDに$H_MESGが書き込まれた時に，
自動でメイルを配信する宛先のメイルアドレスを設定します．
1行に1メイルアドレスずつ書き込んでください．
行頭に「#」をつけるとその行は無視されるので，
#に続けてコメントを書き込むこともできます．
</p><p>
特に実害はありませんが，無意味な空行が入りすぎないように注意しましょう．
</p><p>
<form action="$PROGRAM" method="POST">
<input name="c" type="hidden" value="me">
<input name="b" type="hidden" value="$BOARD">
<textarea name="armail" rows="$TEXT_ROWS" cols="$MAIL_LENGTH">
__EOF__

    foreach(@ArriveMail) { &cgiprint'Cache("$_\n"); }

    &cgiprint'Cache(<<__EOF__);
</textarea><br>
<input type="submit" value="設定します">
<input type="reset" value="リセットする">
</form>
</p>
__EOF__

    &MsgFooter;

}

1;
