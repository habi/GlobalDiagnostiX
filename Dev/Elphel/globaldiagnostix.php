<?php
/*
PHP script based on "camera_demo.php" from the [Elphel repository](http://is.gdvMSmPS)
FTP this file to ftp://CameraIP/var/html and look at it at
http://CameraIP/var/globaldiagnostix.php
*/

echo "Hallihallo"

echo "Original state was=".elphel_get_state()."<br/>\n";
if (elphel_get_state()>7) {  //! compressor is running
	echo "1"
	elphel_compressor_stop(); //! stop it
	echo "2"
	//! while (elphel_get_state()>7) usleep (100000) ; //! just wait - will wait forever if async mode
	echo "3
	elphel_compressor_reset(); //! Maybe needed twice
	echo "4"
	elphel_compressor_reset(); //! Maybe needed twice
}
echo "Before sensor reset state was=".elphel_get_state()."<br/>\n";

echo "Hallihallo"

echo "Image before doing anything<br/>";
echo "<a href='http://192.168.0.9:8081/img'>
		<img src='http://192.168.0.9:8081/img'
			width='200'
			alt='Image before changing settings'>
	</a>";

echo "<pre>\n";

$init_pars=array(
	"DCM_HOR"  => 1,  //! Decimation horizontal
	"DCM_VERT" => 1,  //! Decimation vertical
	"BIN_HOR"  => 10,  //! Binning horizontal
	"BIN_VERT" => 10,  //! Binning vertical
	"QUALITY"  => 90, //! JPEG quality (%)
	"BITS" => 8,                     //! 8-bit image mode (may be 16)
	"GAMMA" => 57,                   //! Gamma=57%
	"PIXEL_LOW" => 10,               //! Black level - 10 (sensor default "fat zero")
	"PIXEL_HIGH" => 254,             //! white level
	"EXPOS" =>    500,               //! whatever? (in 100usec steps)
	"WOI_LEFT" =>  0,                 //! window left
	"WOI_TOP" =>   0,                 //! window top
	"WOI_WIDTH" =>  10000,            //! window width  (more than needed, will be truncated)
	"WOI_HEIGHT" => 10000,            //! window height (more than needed, will be truncated)
	"BAYER" =>          4             //! 0..3 - set, 4- use calcualted
	);

echo "Parameters before programmimg:\n";
print_r(elphel_get_P_arr($init_pars));

$phase_pars=array();
if ($_GET["phase"]) $phase_pars["SENSOR_PHASE"]=$_GET["phase"]+0;
if ($_GET["clk"])   $phase_pars["CLK_SENSOR"]=  $_GET["clk"]*1000000; /// phase is only modified when clock is set
//! Start with reset (normally not needed, just to make sure we have a clean start, not relying on previous programming)
echo "Original state was=".elphel_get_state()."<br/>\n";
if (($_GET["phase"]) && ($_GET["clk"]==null)) { /// change phase, use default clock frequency
	printf ("Writing %d parameters to control sensor phase to the camera before reset\n",elphel_set_P_arr($phase_pars));
	print_r($phase_pars);
}
//!  elphel_reset_sensor();
//!  echo "After reset & initialization: elphel_get_state=".elphel_get_state()."<br/>\n";
printf ("Written %d parameters to the camera\n",elphel_set_P_arr($init_pars));
//! Program sensor (with restart)
if ($_GET["clk"]) { /// modify both clock and phase
	printf ("Writing %d parameters to control sensor phase to the camera - will reset sensor (again)\n",elphel_set_P_arr($phase_pars));
	print_r($phase_pars);
}
echo "After programming sensor parameters: elphel_get_state=".elphel_get_state()."<br/>\n";
echo "Parameters after programmimg:\n";
print_r(elphel_get_P_arr($init_pars));
if (count($phase_pars)) print_r(elphel_get_P_arr($phase_pars));
elphel_compressor_run();
echo "After starting compressor - elphel_get_state=".elphel_get_state()."<br/>\n";
echo "</pre>\n";

echo "Image with new settings<br/>";
echo "<a href='http://192.168.0.9:8081/img'>
		<img src='http://192.168.0.9:8081/img'
			width='200'
			alt='Image before changing settings'>
	</a>";

?>
