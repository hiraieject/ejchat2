#!/usr/local/bin/perl

print "Content-type: text/html\n\n";

##$ENV{'REQUEST_METHOD'} = "nm=PI&id=959164162&cl=arg_color";

require "jcode.pl";
require "form.pl";
require "lib.pl";

&mkarg();

print <<HTMLEND;
<TITLE>$ROOMNAME</TITLE>
<FRAMESET ROWS="90,40,*" border=0>
	<FRAME name="sub" src="write.cgi$cgiarg">
        <FRAMESET COLS="60%,40%" border=0>
		<FRAME name="seizon"  src="seizon.cgi$cgiarg">
		<FRAME name="profile"  src="profile.cgi">
        </FRAMESET>
	<FRAME name="message" src="log/message.html">
</FRAMESET>
HTMLEND
