#!/usr/bin/env ruby

# NAME
#  release.rb
#
# SYNOPSIS
#  release.rb CVS-tag release-name
#
# DESCRIPTION
#  Create package for release.
#
# NOTE
#  Why I use ruby for this type of work!?
#  You may do it with make instead of this script. :-)

def usage
  usageStr = <<"EOM"
Usage: #{ $0 } CVS-tag release-name
    release.rb: Create package for release.
EOM
  print usageStr
  exit 1
end

tag = ARGV.shift
release = ARGV.shift
Target = '~/cvs_release'
Redist = %w( application.rb deffile.rb gpl_text.txt jcode.pl mime_pls-2_00alpha_tar.gz mimer.pl mimew.pl )

usage() if ( !tag || !release )
target = File.expand_path( Target )

# chdir
Dir.chdir( target )

# remove module dir
`rm -rf KB`

# CVS export
`cvs export -r #{ tag } KB/COPYING KB/README KB/doc/html KB/src KB/tools`

# add redist dir
`mkdir KB/redist`
Redist.each do |i|
  `cp -p redist/#{i} KB/redist/#{i}`
end

# create data dir.
`mv KB/src KB/kbdata`

# add files from redist
`cp -pr KB/redist/jcode.pl KB/redist/mimer.pl KB/redist/mimew.pl KB/kbdata`
`cp -pr KB/redist/gpl_text.txt KB/doc/html`

# create test board
`cp -pr KB/kbdata/board KB/kbdata/test`

# create logdir
`mkdir KB/kbdata/log`
`touch KB/kbdata/log/_place_holder_`

# create CGI dir.
`mkdir KB/kb`

# add files from kbdata
`mv KB/kbdata/kb.cgi KB/kb/index.cgi`
`mv KB/kbdata/icon KB/kbdata/style KB/kbdata/img KB/kb`

# set mode
`chmod 700 KB KB/doc KB/doc/html KB/redist KB/tools`
`chmod 700 KB/tools/*`
`chmod 400 KB/COPYING KB/README KB/doc/html/* KB/redist/*`
`chmod 777 KB/kbdata KB/kbdata/test KB/kbdata/board KB/kbdata/log`
`chmod 755 KB/kbdata/UI KB/kbdata/idef`
`chmod 666 KB/kbdata/board/* KB/kbdata/test/* KB/kbdata/kb.user KB/kbdata/kinoboards`
`chmod 644 KB/kbdata/idef/* KB/kbdata/kb.ph KB/kbdata/UI/*`
`chmod 444 KB/kbdata/log/_place_holder_`
`chmod 444 KB/kbdata/cgi.pl KB/kbdata/kinologue.pl`
`chmod 444 KB/kbdata/jcode.pl KB/kbdata/mimer.pl KB/kbdata/mimew.pl`

`chmod 755 KB/kb KB/kb/icon KB/kb/img KB/kb/style`
`chmod 755 KB/kb/index.cgi`
`chmod 644 KB/kb/style/*`
`chmod 444 KB/kb/icon/* KB/kb/img/*`

# rename
`mv KB KB_#{ release }`

# create archive(tar.gz)
tarfile = "KB_#{ release }.tar"
`tar cvfp #{ tarfile } KB_#{ release } && gzip -9 #{ tarfile }`

# create archive(tar.gz)
lhafile = "KB_#{ release }.LZH"
`lha a #{ lhafile } KB_#{ release }`
