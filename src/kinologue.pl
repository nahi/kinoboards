# kinologue: KINO series LOGging Utility packagE
# Copyright (C) 1997-99 NAKAMURA Hiroshi.


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
$DEFAULT_PROGNAME = '_unknown_';
$SHIFT_AGE = 3;			# 0 means 'no shifting.'
$SHIFT_SIZE = 102400;		# byte(s)

# must not be changed
$[ = 0; $| = 1;

# logfile format.
$FF_PLAIN	= 0;		# plain text file.
$FF_HTML	= 1;		# html file.
$DEFAULT_FILEFORMAT = $FF_PLAIN;

# severity of logging.
$SEV_DEBUG	= 0;		# debug information.
$SEV_INFO	= 1;		# normal condition.
$SEV_WARN	= 2;		# only warning.
$SEV_ERROR	= 3;		# action should be taken.
$SEV_CAUTION	= 4;		# action must be taken.
$SEV_FATAL	= 5;		# system is down.
$SEV_ANY	= 6;		# another severity.
# severity label for logging. ( max 5 char )
@SEV_LABEL = ( DEBUG, INFO, WARN, ERROR, CAUTN, FATAL, ANY );

# severity color for logging with html.
@SEV_COLOR = ( '#00FFFF', '#0000FF', '#00FF00', '#FFFF00', '#FF00FF', '#FF0000', '#000000' );
# classification color for logging with html.
# do not matter to add more colors below. it (will :-) work(s).
@COLOR = ( '#000000', '#C0C0C0', '#808080', '#800000', '#FF0000', '#800080', '#FF00FF', '#008000', '#00FF00', '#808000', '#FFFF00', '#000080', '#0000FF', '#008080', '#00FFFF' );

# require jcode.pl if needed.
require( 'jcode.pl' ) if $JAPANESE_CODE;


######################################################################


###
## KlgLog - log a log
#
# - SYNOPSIS
#	require( 'kinologue.pl' );
#	&kinologue'KlgLog( $kinologue'SEV_*, $msg, $progname, $logfile, $kinologue'FF_* );
#
# - ARGS
#	$kinologue'SEV_*	severity. see top of this file to set this.
#	$msg			message string.
#	$progname		program name.
#				if omitted, $DEFAULT_PROGNAME is used.
#	$logfile		logfile.
#				if omitted, $DEFAULT_LOGFILE is used.
#	$kinologue'FF_*		file format. see top of this file to set this.
#				if omitted, the format used before is selected.
#				in first time, $DEFAULT_FILEFORMAT is used.
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
#	1 if succeed, 0 if failed.
#	when the given severity is not enough severe,
#	log no message, but returns 1.
#
$NO_SHIFT = 0;
sub KlgLog
{
    local( $severity, $msg, $progname, $filename, $format ) = @_;
    if ( $severity < $SEV_THRESHOLD ) { return( 1 ); }

    local( $timeStr ) = &__KlgDateTimeFormatOfUtc( time );
    local( $logStr );

    if ( $format eq '' ) { $format = $DEFAULT_FILEFORMAT; }

    if ( $SHIFT_AGE && !$NO_SHIFT && (( -s "$filename" ) > $SHIFT_SIZE ))
    {
	$NO_SHIFT = 1;
	&KlgLog( $SEV_INFO, "started logfile shifting.", "kinologue",
	    $filename, $format );
	if ( &__KlgShiftLog( $filename ))
	{
	    &KlgLog( $SEV_INFO,
		"finished logfile shifting. new logfile opened.", "kinologue",
		$filename, $format );
	}
	else
	{
	    &KlgLog( $SEV_ERROR, "shifting logfile failed.", "kinologue",
		$filename, $format );
	}
	$NO_SHIFT = 0;
    }

    &__KlgLogHtmlHeader( $filename ) if (( $format == $FF_HTML ) &&
	( !-e "$filename" ));

    &__KlgMsgFormat( *msg );
    if ( !$progname ) { $progname = $DEFAULT_PROGNAME; }
    if ( !$filename ) {	$filename = $DEFAULT_LOGFILE; }

    if ( $format == $FF_PLAIN )
    {
	$logStr = &__KlgLogPlain( $severity, $timeStr, $$, $progname, *msg );
    }
    elsif ( $format == $FF_HTML )
    {
	$logStr = &__KlgLogHtml( $severity, $timeStr, $$, $progname, *msg );
    }
    else
    {
	# unknown format.
	return( 0 );
    }

    open( LOG, ">>$filename" ) || return( 0 );
    print( LOG $logStr );
    close( LOG ) || return( 0 );# but may be succeed ...
	
    1;
}


###
## __KlgLogPlain - format a log with plain text format.
#
# - SYNOPSIS
#	&__KlgLogPlain( $severity, $time, $pid, $progname, *msg );
#
# - ARGS
#	$severity	severity. see top of this file to set this.
#	$time		time string.
#	$pid		process id.
#	$progname	program name.
#	*msg		reference of message string.
#
# - DESCRIPTION
#	format a log with plain text format.
#
# - RETURN
#	formatted string.
#
sub __KlgLogPlain
{
    local( $severity, $time, $pid, $progname, *msg ) = @_;
    local( $sevStr ) = &__KlgSevLabelOfSevId( $severity );
    local( $sevChar ) = substr( $sevStr, 0, 1 );
    sprintf( "%s, [%s \#%d(%s)] %5s -- %s\n", $sevChar, $time, $pid, $progname,
	$sevStr, $msg );
}


###
## __KlgLogHtml - format a log with html format.
#
# - SYNOPSIS
#	&__KlgLogHtml( $severity, $time, $pid, $progname, *msg );
#
# - ARGS
#	$severity	severity. see top of this file to set this.
#	$time		time string.
#	$pid		process id.
#	$progname	program name.
#	*msg		reference of message string.
#
# - DESCRIPTION
#	format a log with html format.
#
# - RETURN
#	formatted string.
#
sub __KlgLogHtml
{
    local( $severity, $time, $pid, $progname, *msg ) = @_;

    local( $sevStr ) = &__KlgSevLabelOfSevId( $severity );
    local( $sevChar ) = substr( $sevStr, 0, 1 );

    $time =~ m/^\w+ (\d+) .*$/o;
    local( $mday ) = $1;

    local( $progTmp, $progC );
    ( $progTmp = $progname ) =~ s/(.)/( $progC += unpack( "C", $1 ))/ge;

    local( $sevCol ) = $SEV_COLOR[$severity];
    local( $timeCol ) = $COLOR[( $mday % ( $#COLOR+1 ))];
    local( $pidCol ) = $COLOR[( $pid % ( $#COLOR+1 ))];
    local( $progCol ) = $COLOR[( $progC % ( $#COLOR+1 ))];

    sprintf( "<font color=\"$sevCol\">%s,</font> [<font color=\"$timeCol\">%s</font> \#<font color=\"$pidCol\">%d</font>(<font color=\"$progCol\">%s</font>)] <font color=\"$sevCol\">%5s</font> -- %s<br>\n", $sevChar, $time, $pid, $progname, $sevStr, $msg );
}


###
## __KlgLogHtmlHeader - log header with html format.
#
# - SYNOPSIS
#	&__KlgLogHtmlHeader( $logfile );
#
# - ARGS
#	$logfile	logfile.
#
# - DESCRIPTION
#	write log header with html format.
#
# - BUGS
#	using overwrite open.
#	log data logged in the same time possibly be lost.
#
# - RETURN
#	nothing.
#
sub __KlgLogHtmlHeader
{
    local( $logfile ) = @_;
    local( $timeStr ) = &__KlgDateTimeFormatOfUtc( time );

    open( LOG, ">$logfile" );
    print( LOG <<__EOF__);
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML i18n//EN">
<html>
<head>
<TITLE>$logfile - kinologue log file</TITLE>
</head>
<body>
<h1>$logfile - <a href="http://www.jin.gr.jp/~nahi/src/perl.shtml#kinologue.pl">kinologue</a> log file</h1>
<p>
created on $timeStr.
</p>

<p>
__EOF__
    close( LOG );
}


###
## __KlgSevLabelOfSevId - get severity lavel from severity id
#
# - SYNOPSIS
#	&__KlgSevLabelOfSevId( $severity );
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
sub __KlgSevLabelOfSevId
{
    local( $severity ) = @_;
    $SEV_LABEL[ $severity ] || 'UNKNOWN';
}


###
## __KlgMsgFormat - format a message
#
# - SYNOPSIS
#	&__KlgMsgFormat( *msg );
#
# - ARGS
#	*msg		reference to a message string.
#
# - DESCRIPTION
#	format a message.
#
# - BUGS
#	cannot handle japanese multi-byted `.'...
#
# - RETURN
#	nothing
#
sub __KlgMsgFormat
{
    local( *msg ) = @_;

    # japanese code conversion, if needed.
    if ( $JAPANESE_CODE ) { &jcode'convert( *msg, $JAPANESE_CODE ); }
    # remove white characters at the end of line.
    $msg =~ s/[ \t\r\f\n]*$//o;
    # add `.' at the end of string, if needed.
    $msg .= '.' if ( $msg !~ /\.$/o );
}


###
## __KlgDateTimeFormatOfUtc - get date/time format from UTC
#
# - SYNOPSIS
#	&__KlgDateTimeFormatOfUtc( $utd );
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
sub __KlgDateTimeFormatOfUtc
{
    local( $utc ) = @_;
    local( $sec, $min, $hour, $mday, $mon, $year ) = localtime( $utc );
    sprintf( "%s %02d %02d:%02d:%02d %s",
	( Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec )[ $mon ],
	$mday, $hour, $min, $sec, 1900 + $year );
}


###
## __KlgShiftLog - shift logfile
#
# - SYNOPSIS
#	&__KlgShiftLog( $logfile );
#
# - ARGS
#	$logfile	logfile
#
# - DESCRIPTION
#	shift logfile.
#
# - BUGS
#	rename filenames to the old's.
#	log data logged in the same time possibly be lost.
#
# - RETURN
#	1 if succeed, 0 if failed.
#
sub __KlgShiftLog
{
    local( $logfile ) = @_;

    return( 0 ) if ( !-e "$logfile" );

    local( $i, $j );
    if ( $SHIFT_AGE > 1 )
    {
	for ( $i = $SHIFT_AGE-2; $i >= 0; $i-- )
	{
	    if ( -e "$logfile.$i" )
	    {
		($j = $i)++;
		rename( "$logfile.$i", "$logfile.$j" ) || return( 0 );
	    }
	}
    }
    rename( $logfile, "$logfile.0" ) || return( 0 );

    1;
}


#/////////////////////////////////////////////////////////////////////
1;


# $Id: kinologue.pl,v 1.7 1999-02-17 18:30:52 nakahiro Exp $


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
