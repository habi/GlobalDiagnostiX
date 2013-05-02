<?php
/*
PHP script based on "camera_demo.php" from the [Elphel repository](http://is.gdvMSmPS)
and http://cameraIP/usr/html/setparameters_demo.php"
FTP this file to ftp://CameraIP/var/html (use "curl -T globaldiagnostix.php
ftp://CameraIP/var/html/ --user root:pass") and look at it at
http://CameraIP/var/globaldiagnostix.php
*/

// Read Parameters from URL as http://url?key1=value1&key2=value2
$parameters = array();
foreach($_GET as $key => $value) {
    $parameters[$key] = convert($value);
}

// parameters are set X frames in the future
if (isset($_GET['framedelay']))
	{
	$framedelay = $_GET['framedelay'];
	}
else
	$framedelay = 3; // default framedelay is 3

function convert($s) {
    // clean up
    $s = trim($s, "\" ");  
    // check if value is in HEX
    if(strtoupper(substr($s, 0, 2))=="0X")
        return intval(hexdec($s));
    else
        return intval($s);
}

/*
get the current URL [http://is.gd/vllbf] and use
echo print_r($_SERVER);
to see all the variables available (as seen in the first comment on
http://stackoverflow.com/a/189113/323100).
*/ 

// Save CameraIP/phpfile into variable for re-use
$url="http://".$_SERVER['HTTP_HOST'].$_SERVER['SCRIPT_NAME'];

// Give out some HTML code, so that we actually have a page to look at
echo "<html>\n<head>\n	<title>GlobalDiagnostiX - PHP</title>\n</head>\n<body>\n";
echo "<h1>GlobalDiagnostiX exposure settings page</h1>\n";
echo "<h2>Image before doing anything</h2>\n";
echo "<a href='http://".$_SERVER['HTTP_HOST'].":8081/img'>\n<img src='http://".$_SERVER['HTTP_HOST'].":8081/last/".str_repeat("prev/",$framedelay + 1)."img' width='200' alt='Image before settings change'>\n</a><br />\n"; # go to the 'last' frame, go back '$framedelay +1' frames and show this 'img'. This should be the one image before setting anything (or one before that).
echo "Image ".elphel_get_frame()." with";
echo "<ul><li>";
echo "Exposure time = ".(elphel_get_P_value(ELPHEL_EXPOS) / 1000)." msec";
echo "</li><li>";
echo "Auto exposure = ";
if (elphel_get_P_value(ELPHEL_AUTOEXP_ON) == 1)
	echo "on";
elseif (elphel_get_P_value(ELPHEL_AUTOEXP_ON) == 0)
	echo "off";
echo "</li></ul>";
echo ".<br />\n";

// only show parameters if we are actually setting anything, i.e when $parameters is not empty
if ( !empty( $parameters ) )
	{
	echo "<h2>Setting parameters for camera</h2>\n";
	echo "<br />\n";
	echo "The setting parameters from the URL are <pre>\n"; print_r($parameters); echo "</pre><br />\n";
	}
echo "<br />\n";

if ( isset ( $parameters["exposure"] ) )
	{
	elphel_set_P_value(ELPHEL_AUTOEXP_ON,0); // turn off autoexposure if we're setting the exposure manually.
	elphel_set_P_value(ELPHEL_EXPOS,($parameters['exposure'] * 1000 )); // input is in msec, set is in usec
	}

echo "<h2>Image after updated settings</h2>\n";
// wait for at least three frames for the setting from above to stick
// it seems that wait_frame is not enough, we need to do skip_frames. Maybe this is because of the way PHP works...
elphel_skip_frames($framedelay);

echo "<a href='http://".$_SERVER['HTTP_HOST'].":8081/img'>\n<img src='http://".$_SERVER['HTTP_HOST'].":8081/last/img' width='200' alt='Image after settings change'>\n</a><br />\n";
echo "Image ".elphel_get_frame()." with";
echo "<ul><li>";
echo "Exposure time = ".(elphel_get_P_value(ELPHEL_EXPOS) / 1000)." msec";
echo "</li><li>";
echo "Auto exposure = ";
if (elphel_get_P_value(ELPHEL_AUTOEXP_ON) == 1)
	echo "on";
elseif (elphel_get_P_value(ELPHEL_AUTOEXP_ON) == 0)
	echo "off";
echo "</li></ul>";
echo ".<br />\n";

echo "<br />\n";
/*
echo "Click the links here to turn AE either '<a href='".$url."?autoexposure=1'>ON</a>' or '<a href='".$url."?autoexposure=0'>OFF</a>'.<br />\n";
*/
echo "</body>\n</html>\n";

// set autoexposure to what the user requested with "URL?autoexposure=bool"
if ( isset ( $parameters["autoexposure"] ) )
	{
	elphel_set_P_value(ELPHEL_AUTOEXP_ON,$parameters["autoexposure"]);
	}
	elphel_skip_frames($framedelay);

?>
