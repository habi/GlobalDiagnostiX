<?php

// Set default frame ahead
if (!array_key_exists("ahead",$_GET))
	$ahead=3;

// Special treatment for the gamma values and blacklevel.
// Get exising gamma values  if a gamma parameter is requested
if (array_key_exists("gamma",$_GET) || array_key_exists("black",$_GET)) {
	$gammas=array(
		"GTAB_R__0816"=>"",
		"GTAB_G__0816"=>"",
		"GTAB_GB__0816"=>"",
		"GTAB_B__0816"=>"",
		"GTAB_R__0824"=>"",
		"GTAB_G__0824"=>"",
		"GTAB_GB__0824"=>"",
		"GTAB_B__0824"=>""
		);
	// get existing gamma values
	$gammas= elphel_get_P_arr($gammas);
}

foreach($_GET as $key=>$value) {
	
	if(strtolower(substr($s, 0, 2))=="0x")
		$value= hexdec($value);
	switch ($key) {
		case "gamma":
			// set gammas array and postpone setting values in the camera
			$value = intval($value);
			$gammas["GTAB_R__0816"]=$value;
			$gammas["GTAB_G__0816"]=$value;
			$gammas["GTAB_GB__0816"]=$value;
			$gammas["GTAB_B__0816"]=$value;
			break;
		case "black":
			// set gammas array and postpone setting values in the camera
			$value = intval($value);
			$gammas["GTAB_R__0824"]=$value;
			$gammas["GTAB_G__0824"]=$value;
			$gammas["GTAB_GB__0824"]=$value;
			$gammas["GTAB_B__0824"]=$value;
			break;
	}
	// If any gamma value was set, set all gamma values in the camera.
	// Was postponed earlier
	if ($gammas != NULL) {
 		// values are taken from the green color
 		elphel_gamma_add($gammas["GTAB_G__0816"]/100, $gammas["GTAB_G__0824"]);
		// Apply the values at the frame ahead
		elphel_set_P_arr($gammas, elphel_get_frame() + $ahead);
	}
	//
	// Add code to form the output here
}

?>
