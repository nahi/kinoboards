#!/usr/bin/env ruby

# NAME
#  getRevisions.rb
#
# SYNOPSIS
#  getRevision.rb CVS-module (CVS-module ...)
#
# DESCRIPTION
#  Dumps filenames and those cvs revisions.
#
# NOTE
#  Raise an exception when parsing failed or the CVS-module has any
#  no-'Up-to-date' file.

ARGV.each do |arg|
  file = ''
  revision = ''
  open( "|cvs status #{arg}", "r" ).each do |line|
    if ( line =~ /^File: (\S*)\s*Status: (\S*)$/o )
      raise "illegal file format. 'revision' not found." if file != ''
      raise "not Up-to-date: file" if ( $2 != 'Up-to-date' )
      file = $1
    elsif ( line =~ /^   Repository revision:\s*(\S*)/ )
      raise "illegal file format. 'File' not found." if file == ''
      revision = $1
      print "#{file}: #{revision}\n"
      file = ''
    end
  end
end
