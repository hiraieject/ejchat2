#!/usr/local/bin/perl

print "Content-type: text/html\n\n";

require "jcode.pl";
require "form.pl";
require "lib.pl";

if( $arg_name ne "" ){

## MESSAGE 更新チェック
    $mes = "log/message.html";
    ($mes_mtime) = (stat($mes))[9];
    if( $mes_mtime > $arg_uptime ){
##	print "need update $mes_mtime > $arg_uptime\n";
	$need_update = 1;
    }
    $update_time = 30;
    $mes_reload  = 0;

## 生存更新
    $fn = "users/".$arg_name."\@".$remote_addr."\@\@".$arg_loginid;
    &touch( $fn );
    
} else {
    $update_time = 120;
    $mes_reload  = 1;
}

$arg_uptime = "";
&mkarg();

#--------------    
print <<ENDEND;
<SCRIPT LANGUAGE="JavaScript">
var UPDATE_TIME=$update_time;
var COUNT=UPDATE_TIME;
function cycletimer() {
    COUNT --;
    if( COUNT <= 0 ){
	COUNT=UPDATE_TIME;
	reload($mes_reload);
    } else {
	setTimeout("cycletimer()",1000);
	document.TM.time.value=COUNT;
    }
}
function reload(mes) {
    var uptime = parent.message.mes_mtime;
    var url;
    COUNT = 0;
    document.TM.time.value="wait";
    url = "seizon.cgi$cgiarg&dmy=$nowtime&ut=" + uptime.toString();
    window.parent.seizon.location.href = url;
    if( mes == 1 ){
	window.parent.message.location.href = "log/message.html";
    }
}
function dispprofile(user,host) {
    var uptime = parent.message.mes_mtime;
    var url;
    url = "profile.cgi?pr=" + user + "&host=" + host;
    window.parent.profile.location.href = url;
}
setTimeout("cycletimer()",1000);
ENDEND
#--------------    

if( $need_update != 0 ){
print <<ENDEND;
    window.parent.message.location.href = "log/message.html";
ENDEND
}

#--------------    
print <<ENDEND;
</SCRIPT><HTML><BODY $BODYOPT>
<FORM name="TM">
<INPUT NAME="time" SIZE=4 value="wait">
<A href=# onClick="return reload(1);">RELOAD</A>
ENDEND
#--------------    

    
## 生存情報収集
$top = 1;
opendir(DIR, "users");
while ($file = readdir(DIR)){
    if( $file =~ /@/ ){
	$fn = "users/".$file;
	($mtime) = (stat($fn))[9];
	if( ($nowtime-$EXPTIME) > $mtime ){
	    unlink( $fn );
	} else {
	    if( $top != 1 ){
		print "  ||  \n";
	    }
	    $top = 0;
	    @tmp = split( /\@/, $file );
	    $host = $tmp[1];
	    $file = $tmp[0];
#	    print "$file";
	    print "$file<a href=# onClick=\"return dispprofile(\'$file\',\'$host\')\">.</a>";
	}
    }
}
closedir(DIR);


print <<ENDEND;
<hr></FORM>
ENDEND

