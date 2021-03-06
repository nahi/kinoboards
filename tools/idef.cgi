#!/usr/local/bin/ruby


# SYNOPSIS
#   CGIApp.new( appName )
#
# ARGS
#   appName	Name String of the CGI application.
#
# DESCRIPTION
#   Running this application object as a CGI with 'c=[value]' causes
#   executing the method 'exec_proc_[value]( query )'.
#     ie. 'c=entry' -> exec_proc_entry( query )
#   Without 'c=[value]' in query, 'exec_proc_default( query )' are called.
#
#   'query' is a Hash of query except the key 'c'.
#
require 'application'
require 'cgi'
class CGIApp < Application
  include Log::Severity

  private
  def initialize( appName )
    super( appName )
    @cgi = CGI.new()
    @query = @cgi.params
    @os = @cgi
  end

  def run()
    log( SEV_INFO, 'Accessed: ' << ( @cgi.remote_user || 'anonymous' ) <<
	'@' << ( @cgi.remote_host || @cgi.remote_addr || 'unknown' ))
    if ( @query.has_key?( 'c' ))
      method = ( 'exec_proc_' << @query['c'][0] ).intern
      @query.delete( 'c' )
      send( method, @query )
    else
      exec_proc_default( @query )
    end
    # CAUTION: Result code must be here.
  end

  def method_missing( msg_id, *vars )
    raise RuntimeError.new( "Cannot handle this method: #{ msg_id.to_s }" )
  end
end


# SYNOPSIS
#   KbIconDefFile.new( filename )
#
# ARGS
#   filename	Path of a KB icon definition file.
#
# DESCRIPTION
#   In KbIconDefFile, the filename is used as the key of it.
#
require 'deffile'
class KbIconDefFile < DefFile
  public
  def getFileName( key )
    if ( self[].has_key?( key ))
      key
    else
      nil
    end
  end

  public
  def addFileName( key )
    if ( self[].has_key?( key ))
      raise RuntimeError.new( "Duplicate entry for #{ key }." )
    end
    self[ key ] = nil
  end

  public
  def getLabel( key )
    self[ key, LabelCol ]
  end
  def setLabel( key, label )
    self[ key, LabelCol ] = label
  end

  public
  def getComment( key )
    self[ key, CommentCol ]
  end
  def setComment( key, comment )
    self[ key, CommentCol ] = comment
  end

  private

  LabelCol = 1
  CommentCol = 2

  def initialize( filename )
    super( filename )
  end
end


# SYNOPSIS
#   KbIdefConfApp.new( filename )
#
# ARGS
#   filename	Path of a KB icon definition file.
#
# DESCRIPTION
#   In KbIconDefFile, the filename is used as the key of it.
#
class KbIdefConfApp < CGIApp
  private
  TITLE = 'KB Icon Definition File Configuration'
  ADDRESS = <<-EOS
#{ TITLE }
Copyright (C) 1999
<a href="http://www.jin.gr.jp/~nahi/">NAKAMURA Hiroshi</a>.
All Rights Reserved.
EOS
  ICON_DIR = 'icons'
  IDEF_FILE = 'icons/all.idef'
  ICON_WIDTH = 20
  ICON_HEIGHT = 20
  ICON_LABEL_SIZE = 8
  ICON_COMMENT_SIZE = 40

  def exec_proc_entry( query )
    idef = KbIconDefFile.new( IDEF_FILE )
    html = CGI.new( 'html4' )
    checked = ( query.has_key?( 'checked' ))? true : nil

    @os.out( { 'charset' => 'EUC-JP' } ) {
      html.html( 'LANG' => 'ja' ) {
	my_html_head( html ) <<
	html.body {
	  html.h1 { TITLE } << html.hr <<
	  html.p { <<-EOS
利用するアイコンをチェックして，
このページの一番下にあるボタンを押してください．
ボタンを押して表示される画面をそのまま保存すると，
きのぼずのアイコン定義ファイルになります
（アイコン画像ファイルそのものは，
KINOBOARDS/1.0R6.5のパッケージに含まれています）．
EOS
          } <<
	  html.p { <<-EOS
きのぼずのアイコン定義ファイルの漢字コードはEUCで，改行コードはLFのみです．
そのまま保存しても大丈夫なはずなんですが，もしかしたら保存する際，
あなたのブラウザが勝手に変更しちゃうかもしれません．
気をつけてください．
Internet Explorer 5だと，
保存したファイルの先頭と末尾にHTMLタグが付いちゃうみたいです．
これは手動で削ってください（結局自分で編集しないといけない．．．涙）．
EOS
          } <<
	  html.p { <<-EOS
[]で囲まれている部分は，書き込みの際にアイコンを指定するためのラベルです．
その後ろの部分は，アイコン説明画面に表示されるコメントです．
これらも自由に変更することができます．
EOS
          } <<
	  html.form( 'post', @cgi.script_name ) {
	    html.ul {
    	      iconFileName = iconLabel = iconComment = ''
	      idef.collect { |key|
      		iconFileName = idef.getFileName( key )
      		iconLabel = idef.getLabel( key )
      		iconComment = idef.getComment( key )
		html.li {
		  html.checkbox( 'i_' << key, 'use', checked ) <<
		  html.img( "#{ ICON_DIR }/#{ iconFileName }", iconLabel,
		    ICON_WIDTH, ICON_HEIGHT ) <<
		  " : [" <<
		  html.text_field( 'l_' << key, iconLabel, ICON_LABEL_SIZE ) <<
		  "] " <<
		  html.text_field( 'c_' << key, iconComment,
		    ICON_COMMENT_SIZE )
		}
	      }.join( '' )
	    } <<
	    html.p {
	      html.hidden( 'c', 'view' ) << html.submit <<
	      	CGI::escapeHTML( ' ' ) << html.reset
	    }
	  } <<
	  html.hr << html.address { ADDRESS }
	}
      }
    }
    0
  end

  def exec_proc_view( query )
    idef = KbIconDefFile.new( IDEF_FILE )
    selected = idef.find_all { |key| ( query[ 'i_' << key ][0] )? key : false }

    if ( selected.length == 0 )
      html = CGI.new( 'html4' )
      @os.out( { 'charset' => 'EUC-JP' } ) {
	html.html( 'LANG' => 'ja' ) {
	  my_html_head( html ) <<
	  html.body {
	    html.h1 { TITLE } << html.hr <<
	    html.p { 'ひとつくらい指定してください．．．' } <<
	    html.form( 'post', @cgi.script_name ) {
	      html.p { html.hidden( 'c', 'entry' ) << html.submit( '戻る' ) }
	    } <<
	    html.hr << html.address { ADDRESS }
	  }
        }
      }
      return 1
    end

    @os.out( 'type' => 'text/plain', 'charset' => 'EUC-JP' ) {
      "\n" <<
      selected.collect { |key|
        "#{ idef.getFileName( key ) }\t#{ query[ 'l_' << key ][0] }\t#{ query[ 'c_' << key ][0] }"
      }.join( "\n" ) << "\n"
    }
    0
  end

  alias exec_proc_default exec_proc_entry

  def my_html_head( html )
    html.head {
      html.meta({ 'http-equiv' => 'content-style-type',
	'content' => 'text/css' }) <<
      html.title { TITLE } <<
      html.link({ 'rel' => 'PREV',
	'href' => 'http://www.jin.gr.jp/~nahi/kb' }) <<
      html.link({ 'rev' => 'made', 'href' => 'mailto:nakahiro@sarion.co.jp' })
    }
  end

  AppName = 'IdefConf'
  ShiftAge = 3
  ShiftSize = 102400

  def initialize()
    super( AppName )
    setLog( AppName.dup << '.log', ShiftAge, ShiftSize )
  end
end

app = KbIdefConfApp.new().start()
