# kinologue: KINO series LOGging Utility packagE
# Copyright (C) 1997 NAKAMURA Hiroshi.
#
# $Id: kinologue.pl,v 1.1 1997-11-02 12:11:22 nakahiro Exp $
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.


package kinologue;


###
## definitions
#
$JAPANESE_CODE = 'euc';		# if you wanna use Japanese in logfile,
				# set 'euc', 'jis', or 'sjis'.(see jcode.pl)
				# if you do not want, set null('').
$SEV_THRESHOLD = $SEV_DEBUG;	# logging threshold.


###
## global variables' setting
#

# changes not required
$DEFAULT_LOGFILE = './kinologue.klg';
$DEFAULT_PROGNAME = '(unknown)';
$LIMIT_2000 = 70;		# '69 -> 2069, '70 -> 1970

# must not changed
$[ = 0;
$| = 1;

# severity of logging.
$SEV_DEBUG	= 0;		# debug information.
$SEV_INFO	= 1;		# normal condition.
$SEV_WARN	= 2;		# only warning.
$SEV_ERROR	= 3;		# action should be taken.
$SEV_CAUTION	= 4;		# action must be taken.
$SEV_FATAL	= 5;		# system is down.
$SEV_ETC	= 6;		# another severity.
# severity label for logging.
# CAUTION: each label must be shorter than 8 octet.
@SEV_LABEL = ( DEBUG, INFO, WARN, ERROR, CAUTION, FATAL, ETC );

# require jcode.pl if needed.
if ( $JAPANESE_CODE ) { require( 'jcode.pl' ); }


######################################################################


###
## KlgLog - log a log
#
# - SYNOPSIS
#	require( 'kinologue.pl' );
#	&kinologue'KlgLog( $kinologue'SEV_*, $msg, $progname, $logfile );
#
# - ARGS
#	$kinologue'SEV_*	severity. see top of this file to set this.
#	$msg			message string.
#	$progname		program name.
#				if omitted, $DEFAULT_PROGNAME is used.
#	$logfile		logfile.
#				if omitted, $DEFAULT_LOGFILE is used.
#
# - DESCRIPTION
#	log a log if the given severity is enough severe.
#	threshold is defined by $SEV_THRESHOLD.
#
# - BUGS
#	append open does not need to lock file.
#	but on the OS which supports multi I/O, records possibly be mixed.
#
# - RETURN
#	1 if succeed, 0 if failed. when the given severity
#	is not enough severe, log no message, but returns 1.
#
sub KlgLog {
    local( $severity, $msg, $progname, $filename ) = @_;
    if ( $severity < $SEV_THRESHOLD ) { return( 1 ); }

    local( $sevStr ) = &_KlgSevLabelOfSevId( $severity );
    local( $timeStr ) = &_KlgDateTimeFormatOfUtc( time );
    local( $logStr );

    &_KlgMsgFormat( *msg );
    if ( !$progname ) { $progname = $DEFAULT_PROGNAME; }
    if ( !$filename ) {	$filename = $DEFAULT_LOGFILE; }
    $logStr = sprintf( "[%s #%d(%s)] %8s -- %s\n", $timeStr, $$, $progname, $sevStr, $msg );

    open( LOG, ">>$filename" ) || return( 0 );
    print( LOG $logStr );
    close( LOG ) || return( 0 );# but may be succeed ...
	
    1;
}


###
## _KlgSevLabelOfSevId - get severity lavel from severity id
#
# - SYNOPSIS
#	_KlgSevLabelOfSevId( $severity );
#
# - ARGS
#	$severity	severity ID; defined at the top of this file.
#			one of $kinologue'SEV_*.
#
# - DESCRIPTION
#	get severity lavel from severity id.
#
# - RETURN
#	severity lavel string defined at the top of this file.
#	returns 'UNKNOWN' if severity id were not defined.
#
sub _KlgSevLabelOfSevId {
    local( $severity ) = @_;
    $SEV_LABEL[ $severity ] || 'UNKNOWN';
}


###
## _KlgMsgFormat - format a message
#
# - SYNOPSIS
#	&_KlgMsgFormat( *msg );
#
# - ARGS
#	*msg		reference to a message string.
#
# - DESCRIPTION
#	format a message.
#
# - RETURN
#	nothing
#
sub _KlgMsgFormat {
    local( *msg ) = @_;

    # remove white characters at the end of line.
    $msg =~ s/[ \t\r\f\n]*$//o;
    # add `.' at the end of string, if needed.
    if ( $msg !~ /\.$/o ) { $msg .= '.'; }
    # japanese code conversion, if needed.
    if ( $JAPANESE_CODE ) { &jcode'convert( *msg, $JAPANESE_CODE ); }
}


###
## _KlgDateTimeFormatOfUtc - get date/time format from UTC
#
# - SYNOPSIS
#	_KlgDateTimeFormatOfUtc( $utd );
#
# - ARGS
#	$utc	time [UTC sec.]
#
# - DESCRIPTION
#	get date/time format from UTC.
#
# - RETURN
#	date/time formatted string
#
sub _KlgDateTimeFormatOfUtc {
    local( $utc ) = @_;
    local( $sec, $min, $hour, $mday, $mon, $year ) = localtime( $utc );
    sprintf( "%s %02d %02d:%02d:%02d %s",
	    ( Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec )[ $mon ],
	    $mday, $hour, $min, $sec,
	    ( $year < $LIMIT_2000 ) ? "20$year" : "19$year" );
}


#/////////////////////////////////////////////////////////////////////
1;
