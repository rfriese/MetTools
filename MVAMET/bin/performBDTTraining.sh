read trainingname

cd ..
mkdir trainings/$trainingname
cd trainings/$trainingname/
nice regress3 ../../configs/config$trainingname.json
mkdir /storage/jbod/nzaeh/2016-10-04/Gridoutput/$trainingname
cp flatPtWeight.root /storage/jbod/nzaeh/2016-10-04/Gridoutput/$trainingname/
cp weightfile$trainingname.root /storage/jbod/nzaeh/2016-10-04/Gridoutput/$trainingname/
cp ../../configs/config$trainingname.json /storage/jbod/nzaeh/2016-10-04/Gridoutput/$trainingname/
nice apply ../../configs/config$trainingname.json
rm *.root
makeNNDatasetFromDataAndWeight /storage/jbod/nzaeh/2016-10-04/Gridoutput/$trainingname/data1.root /storage/jbod/nzaeh/2016-10-04/Gridoutput/$trainingname/flatPtWeight.root /storage/jbod/nzaeh/2016-10-04/Gridoutput/$trainingname/dataMVAMet$trainingname.csv 1
