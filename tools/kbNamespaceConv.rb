#!/usr/local/bin/ruby -n
def rep( str )
  str.gsub( '<KB:([A-Z])' ) { |i|
    '<kb:' << $1.tr( 'A-Z', 'a-z' )
  }.gsub( '[A-Z]' ) { |i|
      "_" << i.tr( 'A-Z', 'a-z' )
  }
end
print $_.gsub( '(<KB:[^>]+>)' ) { |i|
  rep( i )
}
