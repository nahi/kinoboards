###
## Fatal - エラー表示
#
# - SYNOPSIS
#	Fatal($FatalNo, $FatalInfo);
#
# - ARGS
#	$FatalNo	エラー番号(詳しくは関数内部を参照のこと)
#	$FatalInfo	エラー情報
#
# - DESCRIPTION
#	エラーを表す画面をブラウザに送信する．
#
# - RETURN
#	なし
#
Fatal: {
    local($FatalNo, $FatalInfo) = ($gVarFatalNo, $gVarFatalInfo);
    local($ErrString);

    if ($FatalNo == 1) {

	$ErrString = "File: $FatalInfoが存在しない，あるいはpermissionの設定が間違っています．お手数ですが，<a href=\"mailto:$MAINT\">$MAINT</a>まで，上記ファイル名をお知らせ下さい．";

    } elsif ($FatalNo == 2) {

	$ErrString = "入力されていない項目があります．戻ってもう一度やり直してみてください．";

    } elsif ($FatalNo == 3) {

	$ErrString = "題や名前，メイルアドレスに，タブ文字か改行が入ってしまっています．戻ってもう一度やり直してみてください．";

    } elsif ($FatalNo == 4) {

	$ErrString = "題中にHTMLタグ，タブ文字，改行文字を入れることは禁じられています．戻って違う題に書き換えてください．";

    } elsif ($FatalNo == 5) {

	$ErrString = "登録されているエイリアスのものと，マシン名が一致しません．お手数ですが，<a href=\"mailto:$MAINT\">$MAINT</a>まで御連絡ください．";

    } elsif ($FatalNo == 6) {

	$ErrString = "「$FatalInfo」というエイリアスは，登録されていません．";

    } elsif ($FatalNo == 7) {

	$ErrString = "$FatalInfoがおかしくありませんか? 戻ってもう一度やり直してみてください．";

    } elsif ($FatalNo == 8) {

	$ErrString = "次の記事はまだ投稿されていません．";

    } elsif ($FatalNo == 9) {

	$ErrString = "メイルが送信できませんでした．お手数ですが，このエラーメッセージと，エラーが生じた状況を，<a href=\"mailto:$MAINT\">$MAINT</a>までお知らせください．";

    } elsif ($FatalNo == 10) {

	$ErrString = ".dbと.articleidの整合性が取れていません．お手数ですが，このエラーメッセージと，エラーが生じた状況を，<a href=\"mailto:$MAINT\">$MAINT</a>までお知らせください．";

    } elsif ($FatalNo == 11) {

	$ErrString = "$FatalInfoというIDに対応する$H_BOARDは，存在しません．";

    } elsif ($FatalNo == 50) {

	$ErrString = "リプライ関係が循環してしまいます．どうしてもリプライ先を変更したい場合，リプライ先を一度新着扱いにしてから，リプライをかけかえてください．";

    } elsif ($FatalNo == 99) {

	$ErrString ="この$H_BOARDでは，このコマンドは実行できません．";

    } elsif ($FatalNo == 999) {

	$ErrString ="システムのロックに失敗しました．混み合っているようですので，数分待ってからもう一度アクセスしてください．何度アクセスしてもロックされている場合，メンテナンス中である可能性もあります．";

    } else {

	$ErrString = "エラー番号不定: $FatalInfo<br>お手数ですが，このエラーメッセージと，エラーが生じた状況を，<a href=\"mailto:$mEmail\">$mEmail</a>までお知らせください．";

    }

    # 異常終了の可能性があるので，とりあえずlockを外す
    # (ロックの失敗の時以外)
    if ($FatalNo != 999) { &cgi'unlock($LOCK_FILE); }

    # 表示画面の作成
    &MsgHeader('Error!', "$SYSTEM_NAME: ERROR!");

    &cgiprint'Cache("<p>$ErrString</p>\n");

    if ($BOARD ne '') {	&PrintButtonToTitleList($BOARD); }
    &PrintButtonToBoardList;

    &MsgFooter;
    exit(0);
}

1;
