# 未完成につき注意．コーディングも途中だったりして．

# トランザクショナルではないので注意．
# ファイルが壊れることはないが，2台が同時に変更作業をすると，
# 設定項目が正しく定義ファイルに反映されないことがある．
IconDef:
{
    local( $iconDefId ) = ( $gVarIconDefId );

    
    &LockAll;
    &CacheIconDb( ?? );
    &UnlockAll;

    &MsgHeader( "Icon Definition", "アイコン定義" );

    &Fatal( 17, '' ) unless $SYS_ICON;

    $msg .= sprintf( "$H_ICON:\n<SELECT NAME=\"icon\">\n<OPTION%s>$H_NOICON\n", $DefIcon? '' : ' SELECTED' );
    local( $IconTitle );
    foreach $IconTitle ( @ICON_TITLE )
    {
	$msg .= sprintf( "<OPTION%s>$IconTitle\n",
			( $IconTitle eq $DefIcon )? ' SELECTED' : '' );
    }
    $msg .= "</SELECT>\n";
    
    $msg .= "(" . &TagA( "$PROGRAM?b=$BOARD&c=i&type=entry",
			"アイコンの説明" ) . ")<BR>\n";


    &LockBoard;
    &GetArriveMailTo(1, $BOARD, *ArriveMail); # 宛先とコメントを取り出す
    &UnlockBoard;

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
