# kill all runnig fiji jobs
killall fiji-linux;
rm -r Config
# remove all previously calculated images and logfiles
rm /afs/psi.ch/project/EssentialMed/Dev/DetectorConfiguration/*.png
rm /afs/psi.ch/project/EssentialMed/Dev/DetectorConfiguration/*.txt
# calculate some stuff
for s in {3..43..5}; # Field of View/ScreenSize
do echo FOV $s;
for c in {1..10..2}; # Sensor Size
do echo SensorSize $c;
for l in {2..5..1}; # lp/mm
do echo lp_mm $l;
for o in 90; # Opening Angle
do echo OpeningAngle $o;
for n in 1; # NA
do echo NA $n
for f in 1; # FStop
do echo FStop $f
for e in 50; # Energy
do echo Energy $e;
python CalculateDetector.py -s $s -o $o -n $n -f $f -c $c -e $e -l $l -p > /dev/null;
done;
done;
done;
done;
done;
done;
done
# open fiji
/home/scratch/Apps/Fiji.app/fiji-linux -eval 'run("Image Sequence...", "open=/afs/psi.ch/project/EssentialMed/Dev/Config starting=1 increment=1 scale=100 file=png or=[] sort");' & # start fiji
