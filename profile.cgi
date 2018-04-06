#!/usr/local/bin/perl

print "Content-type: text/html\n\n";

require "jcode.pl";
require "form.pl";
require "lib.pl";

$pro_name = $form{'pr'};
$pro_host = $form{'host'};

if( $pro_name eq "" ){
    print "<HTML><BODY $BODYOPT>\n";
    exit(0);
}

&pro_read($pro_name);
&mkarg();

print "<META HTTP-EQUIV=\"Refresh\" ";
print "CONTENT=\"180; URL=profile.cgi$cgiarg&pr=$pro_name&host=$pro_host&dmy=$nowtime\">\n";
print "<HTML><BODY $BODYOPT>\n";

if( $pro_hide eq 'on' ){
    print( "<B>[$pro_name] <!-- $pro_host --> </B>" );
} else {
    print( "<B>[$pro_name] ($pro_host) </B>" );
}
print( " <a href=\"profile.cgi$cgiarg&pr=$pro_name&host=$pro_host&dmy=$nowtime\">-refresh-</a>" );
print( " <a href=profile.cgi>-close-</a><BR>" );
if( $pro_hp ne "" && $pro_hp ne "http://" ){
    print( "<a href=\"$pro_hp\" target=user title=\"home page = $pro_hp\">HP</a>  " );
}
#if( $pro_hide ne 'on' ){
#    print( "<a href=\"http://$pro_host/\" target=user>(w)</a>  " );
#    print( "<a href=\"ftp://$pro_host/\" target=user>(f)</a>  " );
#}

if( $pro_mail ne "" ){
    print( "<a href=\"mailto:$pro_mail\" title=\"MAIL ADDRESS = $pro_mail\">MAIL</a>" );
}
if( $pro_aol ne "" ){
    print <<ENDEND;
    <a href="aim:goim?screenname=$pro_aol&message=Hi.+Are+you+there+from+eject+chatroom?"
     title="AOLID=$pro_aol" onMouseOver="window.status='AOL ID = $pro_aol'; return true">AOL</A>
ENDEND
}
if( $pro_icq ne "" ){
    print <<ENDEND;
    <a href="http://wwp.icq.com/$pro_icq" target="icq_win"
     onMouseOver="window.status='ICQ ID = $pro_icq'; return true"
     title="ICQ ID = $pro_icq">
    (ICQ:$pro_icq)<IMG width=44 height=14 
    src="http://online.mirabilis.com/scripts/online.dll?icq=$pro_icq&amp;img=1online.gif&dmyarg=$nowtime"
	alt="ICQ ID = $pro_icq"></a>
ENDEND
}
