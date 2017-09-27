#performs a training of the MVAMet and creates CSV Files for plotting which are then plotted with default settings
#$trainingname is the name of current training, config with 'config$trainingname.json' has to be created in ../config/ (just copy ../config.json accordingly).
#This config has to be adjusted to:
#	"weightfilename" : "weightfile$trainingname.root",
#	"outputdir": "/storage/jbod/nzaeh/2017-02-02/Gridoutput/$trainingname/" -- should be the same as $gridname/$trainingname
#	"inputFile" has to point to the madgraph file created by 'slimmAllFilesAuto.sh'

#### FILTER FOR NLO SAMPLES does currently NOT work as the file indices are not created by 'shrink.C' -- can be implemented by creating a branch 'fileName' in shrink.C which carries the indice of each sample (not sure why I deleted it before)

read trainingname
#where to store the generated weightfile and root/csv files
gridname=/storage/jbod/nzaeh/2017-02-02/Gridoutput
#wholeData=$gridname/shrinkedDataTot.root
#path to all samples (not only the training data) -- including NLO/validation data
wholeData=/home/nzaeh/data/shrinkedDataTot.root
cd ..
if [ ! -d "trainings" ]; then
	mkdir trainings
fi
if [ ! -d "trainings/$trainingname" ]; then
	mkdir trainings/$trainingname
fi
#files will be locally stored here
cd trainings/$trainingname/
printf "Using config ../../configs/config%s.json\n" "$trainingname"
#actual training of the BDT based on the created config
nice regress3 ../../configs/config$trainingname.json
if [ ! -d "$gridname/$trainingname" ]; then
	mkdir $gridname/$trainingname
fi
#copy files to defined grid location
cp flatPtWeight.root $gridname/$trainingname/
cp weightfile$trainingname.root $gridname/$trainingname/
cp ../../configs/config$trainingname.json $gridname/$trainingname/
#applying the trained MVA algorithm to $wholedata to create the validation set
nice apply ../../configs/config$trainingname.json $wholeData
if [ -e "$gridname/$trainingname/weightfile$trainingname.root" ] &&  [ -e "$gridname/$trainingname/flatPtWeight.root" ]; then
	rm *.root
fi
#create CSV File if only angular and scale corrections were trained -- only NLO sample
if [ -e "$gridname/$trainingname/data1.root" ];
then
	makeCSVFile $gridname/$trainingname/data1.root $gridname/$trainingname/dataMVAMet$trainingname.csv 8
fi
#create CSV File if the whole MVA Training was performed (including covariance training) -- only NLO sample
if [ -e "$gridname/$trainingname/data3.root" ];
then
	makeCSVFile $gridname/$trainingname/data3.root $gridname/$trainingname/dataMVAMet$trainingname.csv 8
fi
#Plot the created CSV File and export it to /ekpwww/web/nzaeh/public_html/$trainingname
if [ -e "../../../../PlotsNico/MVAMetPlots/bin/makePlotsMVAMet.py" ]; then
	cd ../../../../PlotsNico/MVAMetPlots/bin
	python makePlotsMVAMet.py -i $gridname/$trainingname/dataMVAMet$trainingname.csv -o $trainingname --export
	cd -
fi
