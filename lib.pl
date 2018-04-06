#!/usr/local/bin/perl

## CONFIG

$EXPTIME = 120;
$BODYOPT = "LEFTMARGIN=4 TOPMARGIN=0 MARGINWIDTH=4 MARGINHEIGHT=0 BGCOLOR=#aaeeee";
$ROOMNAME = "EJECT CHAT ROOM(1)";
$MAXLINE  = 80;
@COL = ( "#CCCCFF", "#AAAAFF", "#9999FF", "#7777CC" );
@SCOL = ( "black","green","red","blue","deeppink","oramgered",
	 "vioret","purple","navy","maroon","coral" );
$admin = "hirai\@eject.org";

## ----------------------------------
$nowtime = time();

## FORM 情報取得
%form = &read_input();
$arg_name    = $form{nm};
$arg_loginid = $form{id};
$arg_color   = $form{cl};
$arg_mes     = $form{ms};
$arg_com     = $form{cm};
$arg_uptime  = $form{ut};
$arg_url     = $form{ur};

$arg_name =~ s/ //g;
$arg_name =~ s/\t//g;

if( $arg_color eq "" ){
    $arg_color = "black";
}

## ホスト名取得
$remote_host = $ENV{'REMOTE_HOST'};
$remote_addr = $ENV{'REMOTE_ADDR'};
if( $remote_host eq "" ){
    $remote_host = $remote_addr;
}

## ----------------------------------
## ARG作成
sub mkarg
{
    if( $arg_uptime eq "" ){
	$cgiarg = "?nm=$arg_name&id=$arg_loginid&cl=$arg_color";
    } else {
	$cgiarg = "?nm=$arg_name&id=$arg_loginid&cl=$arg_color?ut=$arg_uptime";
    }
}

## ----------------------------------
## TOUCH 関数
sub touch#($fn)
{
    if( -f $_[0] ){
    } else {
	open( TMP, "> $_[0]" );
	close( TMP );
    }
    utime( $nowtime,$nowtime, $_[0] );
}
## ----------------------------------
## PROFILE 読み書き
sub pro_read#($name)
{
    local($name,@tmp,$in);
    $name = $_[0];
    if( ! -f "profiles/$name" ){
	$pro_mail = "";
	$pro_icq  = "";
	$pro_aol  = "";
	$pro_hp   = "";
	$pro_pass = "";
    }
    open( IN , "profiles/$name" );
    while( $in = <IN> ){
	$in =~ s/\n//;
	$in =~ s/\r//;
	@tmp = split( /!/, $in );
	if( $tmp[0] eq "mail" ){
	    $pro_mail = $tmp[1];
	} elsif( $tmp[0] eq "icq" ){
	    $pro_icq= $tmp[1];
	} elsif( $tmp[0] eq "aol" ){
	    $pro_aol = $tmp[1];
	} elsif( $tmp[0] eq "hp" ){
	    $pro_hp = $tmp[1];
	} elsif( $tmp[0] eq "pass" ){
	    $pro_pass = $tmp[1];
	} elsif( $tmp[0] eq "hide" ){
	    $pro_hide = $tmp[1];
	} elsif( $tmp[0] eq "needp" ){
	    $pro_needp = $tmp[1];
	}
    }
    close(IN);
}
sub pro_write#($name)
{
    local($name);
    $name = $_[0];
    open( OUT , "> profiles/$name" );
    print( OUT "mail!$pro_mail\n" );
    print( OUT "icq!$pro_icq\n" );
    print( OUT "aol!$pro_aol\n" );
    print( OUT "hp!$pro_hp\n" );
    print( OUT "pass!$pro_pass\n" );
    print( OUT "needp!$pro_needp\n" );
    print( OUT "hide!$pro_hide\n" );
    close(OUT);
}

## ----------------------------------
## 環境変数表示
sub env
{
    print "<p><hr>";
    while (($name, $value) = each(%ENV)) {
	print "$name = $value<BR>\n";
    }
}


sub cookielib
{
    print <<ENDEND;
<SCRIPT LANGUAGE="JavaScript">
function getCookie(key,  tmp1, tmp2, xx1, xx2, xx3) {
    tmp1 = " " + document.cookie + ";";
    xx1 = xx2 = 0;
    len = tmp1.length;
    while (xx1 < len) {
        xx2 = tmp1.indexOf(";", xx1);
        tmp2 = tmp1.substring(xx1 + 1, xx2);
        xx3 = tmp2.indexOf("=");
        if (tmp2.substring(0, xx3) == key) {
            return(unescape(tmp2.substring(xx3 + 1, xx2 - xx1 - 1)));
        }
        xx1 = xx2 + 1;
    }
    return("");
}
function setCookie(key, val, tmp) {
    tmp = key + "=" + escape(val) + "; ";
    // tmp += "path=" + location.pathname + "; ";
    tmp += "expires=Fri, 31-Dec-2030 23:59:59; ";
    document.cookie = tmp;
}

</SCRIPT>
ENDEND
}

1;

