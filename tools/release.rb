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

def usage
  usageStr = <<"EOM"
Usage: #{ $0 } CVS-tag release-name
    release.rb: Create package for release.
EOM
  print usageStr
  exit 1
end

tag = ARGV[0]
release = ARGV[1]
usage() if ( !tag || !release )

Target = '~/cvs_release'

target = File.expand_path( Target )

# chdir
Dir.chdir( target )

# remove module dir
`rm -rf KB`

# CVS export
`cvs export -r #{ tag } KB/COPYING KB/README KB/doc/html KB/src`

# add redist dir
`cp -pr redist KB`

# add files from redist
`cp -pr KB/redist/jcode.pl KB/redist/mimer.pl KB/redist/mimew.pl KB/src`

# rename src dir.
`mv KB/src KB/kb`

# create logdir
`mkdir KB/kb/log`

# set mode
`chmod 700 KB KB/doc KB/doc/html KB/redist`
`chmod 400 KB/COPYING KB/README KB/doc/html/* KB/redist/*`
`chmod 777 KB/kb KB/kb/test KB/kb/board KB/kb/log`
`chmod 755 KB/kb/UI KB/kb/icons`
`chmod 755 KB/kb/kb.cgi`
`chmod 666 KB/kb/board/* KB/kb/test/* KB/kb/kinousers`
`chmod 644 KB/kb/icons/*.idef KB/kb/index* KB/kb/kb.ph KB/kb/kinoboards`
`chmod 444 KB/kb/UI/* KB/kb/cgi.pl KB/kb/icons/*.gif KB/kb/kinologue.pl`
`chmod 444 KB/kb/jcode.pl KB/kb/mimer.pl KB/kb/mimew.pl`

# create archive
tarfile = "KB_#{ release }.tar"
`tar cvfp #{ tarfile } KB && gzip #{ tarfile }`
