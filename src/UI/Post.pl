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
    local( *postedBody ) = *gVarBody;

    local( %mailHeader, $mailBody );
    &parseMail( *postedBody, *mailHeader, *mailBody );

    # 入力された記事情報
    local( $Name, $Email );
    if ( defined( $mailHeader{ 'from2' } ))
    {
	$Email = $mailHeader{ 'from' };
	( $Name ) = ( $mailHeader{ 'from2' } =~ /^(.*)\s*<.*>$/ );
    }
    else
    {
	( $Name, $Email ) = ( $mailHeader{ 'from' } =~ /^(.*)\s*<(.*)>$/ );
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

    if ( $mailHeader{ 'x-kb-command' } eq 'POST' )
    {
        &LockAll;
        &LockBoard;

	# cache article DB
	&DbCache( $BOARD ) if $BOARD;

	&secureSubject( *Subject );
	&secureArticle( *Article, $TextType );

	# 記事の作成
	local( $newArtId ) = &MakeNewArticle( $BOARD, $Id, $op, $TextType,
	    $Name, $Email, $Url, $Icon, $Subject, $Article, $Fmail );

	&UnlockBoard;
	&UnlockAll;
    }
    else
    {
	# do nothing
    }
}

sub parseMail
{
    local( *postedBody, *mailHeader, *mailBody ) = @_;

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
	    if ( /^(x-kb-[^:][^:]*):\s*(.*)$/i )
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
