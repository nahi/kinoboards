###
## Post - コマンドラインからの新規記事投稿
#
# - SYNOPSIS
#	kb.cgi board POST
#
# - ARGS
#	board ... 掲示板ID
#	POST .... 記事投稿を示すリテラル
#
# - DESCRIPTION
#	メイルを標準入力として取り込み，新規記事として書き込む．
#
require( 'mimer.pl' );
POST_STDIN:
{
    local( *postedBody, $force ) = ( *gVarBody, $gVarForce );

    local( %mailHeader, $mailBody );
    &parseMail( *postedBody, *mailHeader, *mailBody, ( $force? 0 : 1 ));

    # 入力された記事情報
    local( $Name, $Email );

    $mailHeader{ 'from' } =~ /^(\S+)/;
    $Name = $Email = $1;

    if ( defined( $mailHeader{ 'from2' } ))
    {
	if ( $mailHeader{ 'from2' } =~ /^"([^"]*)"\s*<([^>][^>]*)>$/ )
	{
	    # From: "NaHi" <nahi@keynauts.com>
	    $Name = $1, $Email = $2;
	}
	elsif ( $mailHeader{ 'from2' } =~ /^([^<]*)\s*<([^>][^>]*)>$/ )
	{
	    # From: NaHi <nahi@keynauts.com>
	    $Name = $1, $Email = $2;
	}
	elsif ( $mailHeader{ 'from2' } =~ /^([^(][^(]*)\s*\(([^)]*)\)$/ )
	{
	    # From: nahi@keynauts.com (NaHi)
	    $Name = $2, $Email = $1;
	}
	elsif ( $mailHeader{ 'from2' } =~ /^(\S+)$/ )
	{
	    # From: nahi@keynauts.com
	    $Name = $Email = $1;
	}
	else
	{
	    # parsing failed...
	    &KbLog( $kinologue'SEV_ERROR, "'From' header parsing failed: " .
		$mainHeader{ 'from2' } );
	    return;
	}
    }

    local( $Url ) = '';
    local( $Supersede ) = '';
    local( $Id ) = '';
    local( $TextType ) = $H_TTLABEL[0];
    local( $Icon ) = $mailHeader{ 'x-kb-icon' };
    local( $Subject ) = $mailHeader{ 'subject' };
    local( $Article ) = $mailBody;
    local( $Fmail ) = 0;
    local( $op ) = 0;

    if ( $force || ( $mailHeader{ 'x-kb-command' } eq 'POST' ))
    {
        &LockAll();

	# cache article DB
	&DbCache( $BOARD ) if $BOARD;

	&secureSubject( *Subject );
	&secureArticle( *Article, $TextType );

	# 記事の作成（メイル転送は行なわない）
	local( $newArtId ) = &MakeNewArticle( $BOARD, $Id, $op, $TextType,
	    $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail, 0 );

	&UnlockAll();
    }
    else
    {
	# do nothing
    }
}

# SYNOPSIS
#   &parseMain( *postedBody, *mailHeader, *mailBody, $flag );
#
# ARGS
#   $postedBody		Posted Mail( header and body )
#   $mailHeader		Hash buffer for parsed header.
#   $mailBody		String buffer for parsed body.
#   $flag		Control flag.
#     2^0 ... parse 'x-kb-command: ...' in mail body, or not.
#
# DESCRIPTION
#   May the source be with you! ^^;
#
# RETURN
#   nothing
#
sub parseMail
{
    local( *postedBody, *mailHeader, *mailBody, $flag ) = @_;

    local( $attr, $value );
    local( %nofHeader );
    local( $status ) = 'HEADER';	# or 'BODY'.

    foreach ( split( /\n/, $postedBody ))
    {
	if ( $status eq 'HEADER' )
	{
	    if ( s/^\s+// )
	    {
		$value .= ' ' . $_;
	    }
	    else
	    {
		if ( $attr )
		{
		    ++$nofHeader{ $attr };
		    $value = &mimedecode( $value, 'EUC' );
		    if ( $nofHeader{ $attr } > 1 )
		    {
			$mailHeader{ $attr . $nofHeader{ $attr }} = $value;
		    }
		    else
		    {
			$mailHeader{ $attr } = $value;
		    }
		}
		if ( /^$/ )
		{
		    $status = 'BODY';
		}
		else
		{
		    if ( /^From (\S+)/ )
		    {
			$attr = 'from';
			$value = $1;
		    }
		    else
		    {
			( $attr, $value ) = split( /:\s*/, $_, 2 );
			$attr =~ tr/A-Z/a-z/;
		    }
		}
	    }
	}
	elsif ( $status eq 'BODY' )
	{
	    if ( $flag&1 && s/^(x-kb-[^:][^:]*):\s*(.*)$//i )
	    {
		( $attr = $1 ) =~ tr/A-Z/a-z/;
		$value = $2;
		++$nofHeader{ $attr };
		if ( $nofHeader{ $attr } > 1 )
		{
		    $mailHeader{ $attr . $nofHeader{ $attr }} = $value;
		}
		else
		{
		    $mailHeader{ $attr } = $value;
		}
	    }
	    $mailBody .= $_ . "\n";
	}
	else
	{
	    die "not reached.";
	}
    }
}

1;
