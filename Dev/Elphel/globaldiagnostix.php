<?php
/*
PHP script based on "camera_demo.php" from the [Elphel repository](http://is.gdvMSmPS)
and http://cameraIP/usr/html/setparameters_demo.php"
FTP this file to ftp://CameraIP/var/html and look at it at
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
	echo "framedelay set";
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

// Give out some HTML code, so that we actually have a nice page
echo "<html>\n<head>\n<title>GlobalDiagnostiX - PHP</title>\n</head>\n<body>\n";
echo "<h1>GlobalDiagnostiX exposure settings page</h1>\n";
echo "<h2>Image before doing anything</h2>\n";
echo "Image: ".elphel_get_frame()." with an exposure time of ".elphel_get_P_value(ELPHEL_EXPOS)." usec<br>";
echo "<a href='http://192.168.0.9:8081/img'>
		<img src='http://192.168.0.9:8081/img'
			width='200'
			alt='Image before changing settings'>
	</a><br/>";
echo "<br>\n";

if (isset($_GET['EXPOS']))
	{
	echo "The exposure time will be set to ".$parameters["EXPOS"]." usec (in ".$frame_delay." frames).<br>\n";
	$set_frame = elphel_set_P_arr ($parameters, elphel_get_frame() + $frame_delay);
	echo "The current image is ".elphel_get_frame().", the image with new parameters will be number ".$set_frame."<br />\n";
	echo "Image: ".elphel_get_frame()." with an exposure time of ".elphel_get_P_value(ELPHEL_EXPOS)." usec<br>";
	echo "<a href='http://192.168.0.9:8081/torp/wait/img'><img src='http://192.168.0.9:8081/torp/wait/img' width='200' alt='Image after settings change'></a>";

	}
else
	echo "We are not changing the exposure<br>\n";

// set parameters

echo "<br>\n<a href='http://192.168.0.9:8081/pointers'>See the Pointers</a><br>\n";
echo "</body>\n</html>\n";

?>
