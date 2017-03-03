read trainingname
gridname=/storage/jbod/nzaeh/2017-02-02/Gridoutput
wholeData=$gridname/shrinkedDataTot.root
cd ..
if [ ! -d "trainings" ]; then
	mkdir trainings
fi
if [ ! -d "trainings/$trainingname" ]; then
	mkdir trainings/$trainingname
fi
cd trainings/$trainingname/
nice regress3 ../../configs/config$trainingname.json
if [ ! -d "$gridname/$trainingname" ]; then
	mkdir $gridname/$trainingname
fi
cp flatPtWeight.root $gridname/$trainingname/
cp weightfile$trainingname.root $gridname/$trainingname/
cp ../../configs/config$trainingname.json $gridname/$trainingname/
nice apply ../../configs/config$trainingname.json $wholeData
if [ -e "$gridname/$trainingname/weightfile$trainingname.root" ] &&  [ -e "$gridname/$trainingname/flatPtWeight.root" ]; then
	rm *.root
fi
if [ -e "$gridname/$trainingname/data1.root" ];
then
	makeCSVFile $gridname/$trainingname/data1.root $gridname/$trainingname/dataMVAMet$trainingname.csv 8
fi
if [ -e "$gridname/$trainingname/data3.root" ];
then
	makeCSVFile $gridname/$trainingname/data3.root $gridname/$trainingname/dataMVAMet$trainingname.csv 8
fi
if [ -e "../../../../PlotsNico/MVAMetPlots/bin/makePlotsMVAMet.py" ]; then
	cd ../../../../PlotsNico/MVAMetPlots/bin
	python makePlotsMVAMet.py -i $gridname/$trainingname/dataMVAMet$trainingname.csv -o $trainingname
	cp -r ../plots/$trainingname/ /ekpwww/nzaeh/public_html/
	cd -
fi
