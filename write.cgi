#!/usr/local/bin/perl

print "Content-type: text/html\n\n";

require "jcode.pl";
require "form.pl";
require "lib.pl";

@wr_mes = (
	     "([A-Z][a-z][0-9]半角英数字のみ使用可)",
	     "色選択"
	     );
for( $i=0; $i<=$#wr_mes; $i++ ){
    
    $j = $wr_mes[$i];
    &jcode'convert(*j, 'sjis');
    $wr_mes[$i] = $j;
}

&cookielib();

print "<HTML><BODY $BODYOPT SCROLL=NO>\n";

$banner = "<table width=\"100%\"><tr>";
$banner = $banner."<td align=left bgcolor=".$COL[3]."><font color=white>$ROOMNAME</font>";
$banner = $banner."<tr></table>";

if( $arg_name eq "" ){
    goto LOGIN;
} else {
    if( $arg_com eq "LOGIN" 
       || $arg_com eq "LOGOUT" ){
	goto DISPATCH;
    } elsif( $arg_com eq "PROEDIT" ){
	goto PROEDIT;
    } elsif( $arg_com eq "PROWRITE" ){
	if( $form{'pr_cm'} eq "CANCEL" ){
	    goto WRITE;
	}
	goto PROWRITE;
    } else {
	goto WRITE;
    }
}

##-----------------
DISPATCH:
if( $arg_name eq "" ){
    goto LOGIN;
}
if( $arg_com eq "LOGIN" ){
    $arg_loginid = $nowtime;
    &mkarg();

    print <<ENDEND;
<SCRIPT LANGUAGE="JavaScript">
    window.parent.location.href = \"chat.cgi$cgiarg\";\n
    setCookie("color","$arg_color");
    setCookie("user","$arg_name");
    </SCRIPT>
ENDEND

    $fn = "users/".$arg_name."\@".$remote_addr."\@\@".$arg_loginid;
    &touch( $fn );

} else {
    print( "<SCRIPT LANGUAGE=\"JavaScript\">\n window.parent.location.href = \"chat.cgi\";\n</SCRIPT>\n" );
    $fn = "users/".$arg_name."\@".$remote_addr."\@\@".$arg_loginid;
    unlink( $fn );
}
exit(0);

##-----------------
WRITE:
if( $arg_mes ne "" 
    || ($arg_url ne "http://" && $arg_url ne "") ){
## Message Write
    
    $host = $ENV{'REMOTE_HOST'};
    if( $host eq "" ){
	$host = $ENV{'REMOTE_ADDR'};
    }

    $mes = "log/message.html";
    ($mes_mtime) = (stat($mes))[9];
    if( $mes_mtime >= $nowtime ){
	$mes_mtime += 1;
    } else {
	$mes_mtime = $nowtime;
    }

    &LOCK($lockfile);

    open( IN , "log/message.html" );
    open( OUT, "> log/tmp.$$" );

    $in = <IN>; $in = <IN>; $in = <IN>; $in = <IN>; # 4行無視

    print( OUT "<SCRIPT LANGUAGE=\"JavaScript\">\n" );
    print( OUT "var mes_mtime=$mes_mtime;\n" );
    print( OUT "</SCRIPT>\n" );
    print( OUT "<HTML><BODY $BODYOPT>\n" );

    $arg_mes =~ s/>/&gt/g;
    $arg_mes =~ s/</&lt/g;
    &jcode'convert(*arg_mes, 'sjis');
    ($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime($nowtime);
    $min01 = $min%10;
    $min10 = ($min-$min01)/10;
    $mon += 1;
    print( OUT "<font color=$arg_color>$arg_name<!-- $host --> " );
    print( OUT "($mon/$mday $hour:$min10$min01) : " );
    if( $arg_url ne "http://" ){
        if( $arg_mes eq "" ){ $arg_mes = "--link--"; }
        print( OUT "<a href=\"$arg_url\" target=\"otherwin\"> $arg_mes </a></font><BR>\n" );
    } else {
        print( OUT " $arg_mes</font><BR>\n" );
    }
    $i = 0;
    while( $in = <IN> ){
	print( OUT $in );
	if( $i > $MAXLINE ){
	    last;
	}
	$i++;
    }
    close(IN);
    close(OUT);

    unlink( "log/message.html" );

    rename( "log/tmp.$$", "log/message.html" );
    utime( $mes_mtime,$mes_mtime, "log/message.html" );

    &UNLOCK($lockfile);

    print <<END_OF_HTML;
    <SCRIPT LANGUAGE="JavaScript">
	window.parent.seizon.reload(1);
    </SCRIPT>
END_OF_HTML

}
$mes1 = "メッセージ入力";
$mes2 = "URL入力";
&jcode'convert(*mes1, 'sjis');
&jcode'convert(*mes2, 'sjis');
&mkarg();

print <<END_OF_HTML;
<FORM METHOD="POST" ACTION="write.cgi" name="FM">
$banner
<table height=60 CELLPADDING=6><tr>
 <td bgcolor=$COL[0] align=center valign=middle>
<a href="write.cgi$cgiarg&cm=PROEDIT">$arg_name</a> : 
 <td bgcolor=$COL[1] align=center valign=middle>
<INPUT NAME="ms" SIZE=40><BR><font size=-1>$mes1</font>
 <td bgcolor=$COL[2] align=center valign=middle>
<INPUT NAME="ur" SIZE=30 value="http://"><BR><font size=-1>$mes2</font>
 <td bgcolor=$COL[3] align=center valign=middle>
<INPUT TYPE="submit" NAME="cm" VALUE="WRITE">
<INPUT TYPE="submit" NAME="cm" VALUE="LOGOUT">
<INPUT TYPE="HIDDEN" NAME="nm" value="$arg_name">
<INPUT TYPE="HIDDEN" NAME="id" value="$arg_loginid">
<INPUT TYPE="HIDDEN" NAME="cl" value="$arg_color">
</table>
</FORM>
</BODY></HTML>
END_OF_HTML

exit(0);

##-----------------
LOGIN:
print <<END_OF_HTML;
<FORM METHOD="POST" ACTION="write.cgi" name="FM">
$banner
<table height=60 CELLPADDING=6><tr>
<td bgcolor=$COL[0] align=center valign=middle>
Enter Login Name <INPUT NAME="nm" SIZE=10>
<br><font size="-1" color=red>$wr_mes[0]</font>
 <td bgcolor=$COL[1]  align=center valign=middle>
$wr_mes[1] 
<SELECT name="cl" size="1">
END_OF_HTML

foreach $i (@SCOL) {
    print "<OPTION VALUE=\"$i\">$i\n";
}

print <<END_OF_HTML;
</SELECT>
  <td bgcolor=$COL[2]  align=center valign=middle>
<INPUT TYPE="submit" NAME="cm" VALUE="LOGIN">

</table>
</FORM>
</BODY>
</HTML>
<SCRIPT LANGUAGE="JavaScript">
color = getCookie("color");
user  = getCookie("user");
if( color != "" ){ document.FM.cl.value = color; }
if( user  != "" ){ document.FM.nm.value = user;  }
</SCRIPT>
END_OF_HTML
exit(0);

##-----------------
## プロフィール・エディット画面
PROEDIT:

$pro_message = "<B><U><font size=\"+1\" color=yellow>profile editor for $arg_name</font></U></B>";
&pro_read($arg_name);
PROEDIT_CONT:
if( $pro_hp eq "" ){ $pro_hp = "http://"; }
if( $pro_hide  eq "on" ){ $hide  = "CHECKED"; }
if( $pro_needp eq "on" ){ $needp = "CHECKED"; }

print <<ENDEND;
<table height=60 CELLPADDING=6><tr>
<td bgcolor=$COL[1] align=left valign=middle>
<FORM METHOD="POST" ACTION="write.cgi" name="FM">
$pro_message
<INPUT TYPE="submit" NAME="pr_cm" VALUE="WRITE">
<INPUT TYPE="submit" NAME="pr_cm" VALUE="CANCEL">
<font size=-1><a href="mailto:$admin">mailto administrator</a></font>
<BR>
<NOBR>mail address <INPUT NAME="pr_ml" SIZE=20 value="$pro_mail"></NOBR>
<NOBR>HOME PAGE <INPUT NAME="pr_hp" SIZE=20 value="$pro_hp"></NOBR>
<NOBR>ICQ ID <INPUT NAME="pr_icq" SIZE=7 value="$pro_icq"></NOBR>
<NOBR>AOL ID <INPUT NAME="pr_aol" SIZE=7 value="$pro_aol"></NOBR><BR>
<NOBR>password <INPUT type=password NAME="pr_pass"    SIZE=5></NOBR>
<NOBR>new password(if you want to chage pass) <INPUT type=password NAME="pr_newpass" SIZE=5></NOBR>
<INPUT TYPE=checkbox NAME="pr_hide" $hide>hide host/ip
<INPUT TYPE=checkbox NAME="pr_needps" $needp>need pass at login
<INPUT TYPE="HIDDEN" NAME="nm" value="$arg_name">
<INPUT TYPE="HIDDEN" NAME="id" value="$arg_loginid">
<INPUT TYPE="HIDDEN" NAME="cl" value="$arg_color">
<INPUT TYPE="HIDDEN" NAME="cm" value="PROWRITE">
</FORM></table></BODY></HTML>
ENDEND
exit(0);

##-----------------
## プロフィール・書き込み
PROWRITE:

&pro_read($arg_name);
$pass = $form{'pr_pass'};
if( $pass eq "" ){
    $pro_message = "<font color=red>please set password. </font>";
    goto PROEDIT_CONT0;
} elsif( $pro_pass ne "" && $pro_pass ne $pass ){
    $pro_message = "<font color=red>invalid now password. </font>";
  PROEDIT_CONT0:
    $pro_mail = $form{'pr_ml'};
    $pro_hp   = $form{'pr_hp'};
    $pro_icq  = $form{'pr_icq'};
    $pro_aol  = $form{'pr_aol'};
    $pro_hide  = $form{'pr_hide'};
    $pro_needp = $form{'pr_needp'};
    goto PROEDIT_CONT;
}
$pro_mail = $form{'pr_ml'};
$pro_hp   = $form{'pr_hp'};
$pro_icq  = $form{'pr_icq'};
$pro_aol  = $form{'pr_aol'};
$pro_hide  = $form{'pr_hide'};
$pro_needp = $form{'pr_needp'};
$new_pass = $form{'pr_newpass'};
if( $new_pass ne "" ){
    $pro_pass = $new_pass;
} else {
    $pro_pass = $pass;
}
&pro_write($arg_name);
    
goto WRITE;

