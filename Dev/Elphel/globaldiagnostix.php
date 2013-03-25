<?php
/*
PHP script based on "camera_demo.php" from the [Elphel repository](http://is.gdvMSmPS)
and http://cameraIP/usr/html/setparameters_demo.php"
FTP this file to ftp://CameraIP/var/html (use "curl -T globaldiagnostix.php
ftp://192.168.0.9/var/html/ --user root:pass") and look at it at
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
	$frame_delay = $_GET['framedelay'];
	}
else
	$frame_delay = 3; // default is 3 frames

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
$url="http://".$_SERVER['HTTP_HOST'].$_SERVER['SCRIPT_NAME'];

// Give out some HTML code, so that we actually have a nice page
echo "<html>\n<head>\n<title>GlobalDiagnostiX - PHP</title>\n</head>\n<body>\n";
echo "<h1>GlobalDiagnostiX exposure settings page</h1>\n";
echo "<h2>Parameters before doing anything</h2>\n";
echo "Automatic exposure = ".elphel_get_P_value(ELPHEL_AUTOEXP_ON).".<br>";
echo "Exposure =  ".elphel_get_P_value(ELPHEL_EXPOS)." usec.<br>";

echo "<h2>Image before doing anything</h2>\n";

// Show first image 
//echo "<a href='http://192.168.0.9:8081/img'><img src='http://192.168.0.9:8081/img' width='200' alt='Image before changing settings'></a><br/>";

//echo "Image ".elphel_get_frame()." with an exposure time of ".(elphel_get_P_value(ELPHEL_EXPOS) / 1000)." msec<br>";
//echo "<br>\n";

echo "<br>";

// only set parameters if requested, i.e !isempty($parameters)
if ( !empty( $parameters))
	{
	echo "The setting parameters from the URL are <pre>"; print_r($parameters); echo "</pre><br />\n";
	echo "Setting AE ";
	if ($parameters["autoexposure"] == 0) 
		echo "'off'. ";
	elseif ($parameters["autoexposure"] == 1) 
		echo "'on'. ";
	elphel_set_P_value(ELPHEL_AUTOEXP_ON,$parameters["autoexposure"]);
	// wait for at least three frames for the setting to stick
	for ( $counter = 0; $counter < $frame_delay; $counter += 1) { 
		elphel_wait_frame();
		}
	}
echo "<br>\n";

echo "Auto exposure is '";
if (elphel_get_P_value(ELPHEL_AUTOEXP_ON) == 1)
	echo "on";
elseif (elphel_get_P_value(ELPHEL_AUTOEXP_ON) == 0)
	echo "off";
echo "'. Click the links here to turn it either '<a href='".$url."?autoexposure=1'>ON</a>' or '<a href='".$url."?autoexposure=0'>OFF</a>'.<br>\n";

if ( isset ( $parameters["exposure"] ) )
	echo "SETTING EXPOSURE";

/*
if (isset($_GET['EXPOS']))
	{
	echo "The exposure time will be set to ".$parameters["EXPOS"]." usec ".($parameters["EXPOS"] / 1000)." msec/".($parameters["EXPOS"] / 1000 / 1000)." sec) in ".$frame_delay." frames).<br>\n";
	$parameters["WOI_WIDTH"] = 10000; // reset sensor to full width
	$parameters["WOI_HEIGHT"] = 10000; // reset sensor to full height
	echo "<br>\n";
	echo "Setting parameter <pre>"; print_r($parameters); echo "</pre><br />\n";
	echo "<br>\n";
	$set_frame = elphel_set_P_arr ($parameters, elphel_get_frame() + $frame_delay);
	echo "The current image is ".elphel_get_frame().", the image with new parameters will be number ".$set_frame."<br />\n";
	elphel_wait_frame_abs(elphel_get_frame() + $frame_delay);
	echo "The current image is now ".elphel_get_frame()."<br />\n";
	echo "<h2>Image after updated settings</h2>\n";
	echo "<a href='http://192.168.0.9:8081/next/img'><img src='http://192.168.0.9:8081/img' width='200' alt='Image ".elphel_get_frame()." (after settings change)'></a><br>\n";
	echo "Image ".elphel_get_frame()." with an exposure time of ".(elphel_get_P_value(ELPHEL_EXPOS) / 1000)." msec<br>";
	}
else
	echo "We are not changing the exposure time, we're done.<br>\n";

//echo include("http://192.168.0.9:8081/frame"); // 'include' is disabled in Elphel-PHP, unfortunately
*/
echo "</body>\n</html>\n";

?>
