#!/usr/local/bin/perl

%BOARD_FILES = (
	'.kbmail', 'kb.mail',
	'.board', 'kb.board',
	'.db', 'kb.db',
	'.articleid', 'kb.aid'
);

$BOARD_FILE = 'kinoboards';

$C = 0; $W = 0;
$| = 1;
print( "Content-type: text/plain\n\n" );

open( BOARD, "<$BOARD_FILE" ) || &myDie( "cannot open $BOARD_FILE." );
while( <BOARD> ) {
    next if ( /^$/ || /^\#/ );
    ( $dir ) = split( /\t/ );

    &changeFiles( $dir );
}
close BOARD;

if ( !$C ) {
    &myMsg( "older release -> R5.6 conversion finished.\nFiles to be renamed were not found..." );
}
elsif ( $W ) {
    &myMsg( "older release -> R5.6 conversion finished.\nBackuped $W file(s) and renamed $C file(s)..." );
}
else {
    &myMsg( "older release -> R5.6 conversion succeeded.\nRenamed $C file(s)." );
}

exit 0;

sub changeFiles {
    local( $dir ) = @_;

    foreach ( keys( %BOARD_FILES )) {
	if ( -e "$dir/$_" ) {
	    if ( -e "$dir/$BOARD_FILES{$_}" ) {
		rename( "$dir/$BOARD_FILES{$_}", "$dir/$BOARD_FILES{$_}.bak" ) || &myDie( "cannot rename $dir/$BOARD_FILES{$_} to $dir/$BOARD_FILES{$_}.bak" );
		$W++;
		&myMsg( "rename: $dir/$BOARD_FILES{$_} -> $dir/$BOARD_FILES{$_}.bak" );
	    }
	    rename( "$dir/$_", "$dir/$BOARD_FILES{$_}" ) || &myDie( "cannot rename $dir/$_ to $dir/$BOARD_FILES{$_}" );
	    $C++;
	    &myMsg( "rename: $dir/$_ -> $dir/$BOARD_FILES{$_}" );
	}
    }
}

sub myDie {
    local( $msg ) = @_;
    &myMsg( $msg );
    exit 0;
}

sub myMsg {
    local( $msg ) = @_;
    print( $msg . "\n" );
}
