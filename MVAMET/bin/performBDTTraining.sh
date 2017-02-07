read trainingname
gridname=/storage/jbod/nzaeh/2017-02-02/Gridoutput
cd ..
mkdir trainings/$trainingname
cd trainings/$trainingname/
nice regress3 ../../configs/config$trainingname.json
mkdir $gridname/$trainingname
cp flatPtWeight.root $gridname/$trainingname/
cp weightfile$trainingname.root $gridname/$trainingname/
cp ../../configs/config$trainingname.json $gridname/$trainingname/
nice apply ../../configs/configAll$trainingname.json
#rm *.root
if [-e $gridname/$trainingname/data1.root]
then
	makeCSVFile $gridname/$trainingname/data1.root $gridname/$trainingname/dataMVAMet$trainingname.csv 8
fi
if [-e $gridname/$trainingname/data3.root]
then
	makeCSVFile $gridname/$trainingname/data3.root $gridname/$trainingname/dataMVAMet$trainingname.csv 8
fi
