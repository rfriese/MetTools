#Apply training on additional dataset - usually this is done by a new skim...
printf "File to apply training to: "
read applyData
printf "Which Training to apply: "
read trainingname
printf "Which folder to save the created files in: "
read saveFolder
gridname=/storage/jbod/nzaeh/2017-02-02/Gridoutput
printf "Looking for training in %s. Change this?[N/y]\n" "$gridname"
read confirmation
printf "Only performing training on AMC data, take whole dataset?[N/y]\n"
read confirmationData
if [ "$confirmation" = "y" ]; then
	printf "Alternative path: "
	read alternativegrid
	gridname=$alternativegrid
	printf "Training path now %s" "$gridname"
fi
printf "Applying training %s on %s and saving in %s\n" "$trainingname" "$gridname/$applyData" "$gridname/$saveFolder"
cd ..
if [ ! -d "trainings" ]; then
	mkdir trainings
fi
if [ ! -d "trainings/$saveFolder" ]; then
	mkdir trainings/$saveFolder
fi
cd trainings/$saveFolder/
if [ ! -d "$gridname/$trainingname" ]; then
	printf "Training not found! Check gridname in script.\n"
	exit
fi
if [ ! -d "$gridname/$saveFolder" ]; then
        mkdir $gridname/$saveFolder
fi
cp $gridname/$trainingname/weightfile$trainingname.root ./
cp $gridname/$trainingname/config$trainingname.json ./

nice apply config$trainingname.json $applyData $gridname/$saveFolder

if [ -e "$gridname/$trainingname/weightfile$trainingname.root" ] &&  [ -e "$gridname/$trainingname/flatPtWeight.root" ]; then
	rm *.root
fi
if [ -e "$gridname/$saveFolder/data1.root" ];
then
    if [ "$confirmationData" = "y" ]; then
	    makeCSVFile $gridname/$saveFolder/data1.root $gridname/$saveFolder/dataMVAMet$saveFolder.csv
    else
	    makeCSVFile $gridname/$saveFolder/data1.root $gridname/$saveFolder/dataMVAMet$saveFolder.csv 8
    fi
fi
if [ -e "$gridname/$saveFolder/data3.root" ];
then
    if [ "$confirmationData" = "y" ]; then
	    makeCSVFile $gridname/$saveFolder/data1.root $gridname/$saveFolder/dataMVAMet$saveFolder.csv
    else
	    makeCSVFile $gridname/$saveFolder/data1.root $gridname/$saveFolder/dataMVAMet$saveFolder.csv 8
    fi
fi
if [ -e "../../../../PlotsNico/MVAMetPlots/bin/makePlotsMVAMet.py" ]; then
	cd ../../../../PlotsNico/MVAMetPlots/bin
	python makePlotsMVAMet.py -i $gridname/$saveFolder/dataMVAMet$saveFolder.csv -o $saveFolder --export
	cd -
fi
