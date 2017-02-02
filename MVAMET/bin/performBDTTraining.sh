read trainingname
gridname=/storage/jbod/nzaeh/2017-01-24/Gridoutput
cd ..
mkdir trainings/$trainingname
cd trainings/$trainingname/
nice regress3 ../../configs/config$trainingname.json
mkdir $gridname/$trainingname
cp flatPtWeight.root $gridname/$trainingname/
cp weightfile$trainingname.root $gridname/$trainingname/
cp ../../configs/config$trainingname.json $gridname/$trainingname/
nice apply ../../configs/config$trainingname.json
#rm *.root
makeNNDatasetFromDataAndWeight $gridname/$trainingname/data1.root $gridname/$trainingname/flatPtWeight.root $gridname/$trainingname/dataMVAMet$trainingname.csv 8
