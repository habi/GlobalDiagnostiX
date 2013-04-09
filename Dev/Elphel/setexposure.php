<?php
/*
 * PHP script based on "globaldiagnostix.php" to set the exposure time
 * FTP it to the camera and set the exposure by calling CamIP?exposure=123 (for
 * an expousre of 123 ms)
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

// Save CameraIP/phpfile into variable for re-use
$url="http://".$_SERVER['HTTP_HOST'].$_SERVER['SCRIPT_NAME'];

// Give out some HTML code, so that we actually have a page to look at
echo "<html>\n<head>\n <title>GlobalDiagnostiX - PHP</title>\n</head>\n<body>\n";
echo "<h1>GlobalDiagnostiX exposure settings page</h1>\n";

// only show parameters if we are actually setting anything, i.e when $parameters is not empty
if ( !empty( $parameters ) )
	{
	echo "The setting parameters from the URL are <pre>\n"; print_r($parameters); echo "</pre><br />\n";
	}
echo "<br />\n";

if ( isset ( $parameters["exposure"] ) )
	{
	elphel_set_P_value(ELPHEL_AUTOEXP_ON,0); // turn off autoexposure if we're setting the exposure manually.
	elphel_set_P_value(ELPHEL_EXPOS,($parameters['exposure'] * 1000 )); // input is in msec, set is in usec
	}

// wait for at least three frames for the setting from above to stick

elphel_skip_frames($framedelay);

echo "Frame ".elphel_get_frame()." has an exposure time of ".(elphel_get_P_value(ELPHEL_EXPOS) / 1000)." msec";

?>
