# $Id: cgi.pl,v 1.1 1996-04-24 18:00:43 nakahiro Exp $


# Small CGI tool package
# Copyright (C) 1995, 96 NAKAMURA Hiroshi.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PRATICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.


###
## cgi用パッケージ
#
package cgi;


###
## HTMLヘッダの生成
#
sub header {print "Content-type: text/html\n\n";}


###
## デコード: CAUTION! functioon decode sets global variable, TAGS.
#
sub decode {
        local($args, $n_read, *terms, $tag, $value, $code);

        $ENV{'REQUEST_METHOD'} eq "POST" ?
        ($n_read = read(STDIN, $args, $ENV{'CONTENT_LENGTH'})):
        ($args = $ENV{'QUERY_STRING'});

        @terms = split('&', $args);

        foreach (@terms) {
                ($tag, $value) = split(/=/, $_, 2);
                $value =~ tr/+/ /;
                $value =~ s/%([0-9A-Fa-f][0-9A-Fa-f])/pack("C", hex($1))/ge;
		$_ = $value;
		($code) = &jcode'getcode(*_);
		if ($code eq "undef") {
			$TAGS{$tag} = $value;
		} else {
			($code) = &jcode'convert(*_, 'euc');
			$TAGS{$tag} = $_;
		}
		$TAGS{$tag} =~ s/\r+//ge;
        }
}


#/////////////////////////////////////////////////////////////////////
1;
