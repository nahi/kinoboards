###
## Fatal - エラー表示
#
# - SYNOPSIS
#	Fatal($errno, $errInfo);
#
# - ARGS
#	$errno	エラー番号(詳しくは関数内部を参照のこと)
#	$errInfo	エラー情報
#
# - DESCRIPTION
#	エラーを表す画面をブラウザに送信する．
#
# - RETURN
#	なし
#
Fatal: {
    local( $errno, $errInfo ) = ( $gVarFatalNo, $gVarFatalInfo );
    local( $msg );

    if ( $errno == 1 ) {

	$severity = $kinologue'SEV_CAUTION;
	$msg = "File: $errInfoが存在しない，あるいはpermissionの設定が間違っています．お手数ですが，" . &TagA( "mailto:$MAINT", $MAINT ) . "まで，上記ファイル名をお知らせ下さい．";

    } elsif ( $errno == 2 ) {

	$severity = $kinologue'SEV_INFO;
	$msg = "入力されていない項目があります．戻ってもう一度やり直してみてください．";

    } elsif ( $errno == 3 ) {

	$severity = $kinologue'SEV_INFO;
	$msg = "題や名前，メイルアドレスに，タブ文字か改行が入ってしまっています．戻ってもう一度やり直してみてください．";

    } elsif ( $errno == 4 ) {

	$severity = $kinologue'SEV_INFO;
	$msg = "題中にHTMLタグ，タブ文字，改行文字を入れることは禁じられています．戻って違う題に書き換えてください．";

    } elsif ( $errno == 5 ) {

	$severity = $kinologue'SEV_ERROR;
	$msg = "登録されているエイリアスのものと，マシン名が一致しません．お手数ですが，" . &TagA( "mailto:$MAINT", $MAINT ) . "まで御連絡ください．";

    } elsif ( $errno == 6) {

	$severity = $kinologue'SEV_WARN;
	$msg = "「$errInfo」というエイリアスは，登録されていません．";

    } elsif ( $errno == 7 ) {

	$severity = $kinologue'SEV_INFO;
	$msg = "$errInfoがおかしくありませんか? 戻ってもう一度やり直してみてください．";

    } elsif ( $errno == 8 ) {

	$severity = $kinologue'SEV_INFO;
	$msg = "次の記事はまだ投稿されていません．";

    } elsif ( $errno == 9 ) {

	$severity = $kinologue'SEV_CAUTION;
	$msg = "メイルが送信できませんでした．お手数ですが，このエラーメッセージと，エラーが生じた状況を，" . &TagA( "mailto:$MAINT", $MAINT ) . "までお知らせください．";

    } elsif ( $errno == 10 ) {

	$severity = $kinologue'SEV_CAUTION;
	$msg = ".dbと.articleidの整合性が取れていません．お手数ですが，このエラーメッセージと，エラーが生じた状況を，" . &TagA( "mailto:$MAINT", $MAINT ) . "までお知らせください．";

    } elsif ( $errno == 11 ) {

	$severity = $kinologue'SEV_ERROR;
	$msg = "$errInfoというIDに対応する$H_BOARDは，存在しません．";

    } elsif ( $errno == 12 ) {

	$severity = $kinologue'SEV_INFO;
	$msg = "この$H_BOARDでは，$H_MESGの最大サイズは$SYS_MAXARTSIZEバイトということになっています（あなたの$H_MESGは$errInfoバイトです）．";

    } elsif ( $errno == 13 ) {

	$severity = $kinologue'SEV_FATAL;
	$msg = "管理者様へ: socket.phがみつかりませんでした．kb.phの中で，メイル送信用の追加設定を行なってください．";

    } elsif ( $errno == 14 ) {

	$severity = $kinologue'SEV_FATAL;
	$msg = "管理者様へ: 次のrenameに失敗しました（$errInfo）．ファイルパーミッションの設定等をチェックしてみてください．";

    } elsif ( $errno == 15 ) {

	$severity = $kinologue'SEV_WARN;
	$msg = "ユーザ認証に失敗しました．パスワードを間違えていませんか? [もう一度……（の画面はまだ作ってない）]";

    } elsif ( $errno == 50 ) {

	$severity = $kinologue'SEV_INFO;
	$msg = "リプライ関係が循環してしまいます．どうしてもリプライ先を変更したい場合，リプライ先を一度新着扱いにしてから，リプライをかけかえてください．";

    } elsif ( $errno == 99 ) {

	$severity = $kinologue'SEV_WARN;
	$msg ="この$H_BOARDでは，このコマンドは実行できません．";

    } elsif ( $errno == 999 ) {

	$severity = $kinologue'SEV_WARN;
	$msg ="システムのロックに失敗しました．混み合っているようですので，数分待ってからもう一度アクセスしてください．";

    } elsif ( $errno == 1000 ) {

	$severity = $kinologue'SEV_FATAL;
	$msg ="ログファイルへの書き込みに失敗しました．";

    } elsif ( $errno == 1001 ) {

	$severity = $kinologue'SEV_WARN;
	$msg ="現在管理者によるメンテナンス中です．しばらくお待ちください．";

    } else {

	$severity = $kinologue'SEV_ANY;
	$msg = "エラー番号不定（$errInfo）";

    }

    # 異常終了の可能性があるので，とりあえずlockを外す
    # (ロックの失敗の時以外)
    &cgi'unlock( $LOCK_FILE ) if (( !$PC ) && ( $errno != 999 ) && ( $errno != 1001 ));

    # log a log(except logging failure).
    &KbLog( $severity, "$msg" ) if ( $errno != 1000 );

    # 表示画面の作成
    &MsgHeader('Error!', "$SYSTEM_NAME: ERROR!");
    &cgiprint'Cache("<p>$msg</p>\n");
    &PrintButtonToTitleList( $BOARD ) if (( $BOARD ne '' ) && ( $errno != 11 ));
    &PrintButtonToBoardList;
    &MsgFooter;

    exit( 0 );
}

1;
