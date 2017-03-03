#specify directory name in which the skimmed data lies
gridname=/storage/jbod/nzaeh/2017-02-02/Gridoutput/

filenameTemp=$( find $gridname -type d -name '*0000*' | grep 100to)
for filename in $filenameTemp; do
	hadd $filename/outputtot.root -f $filename/output_*
	shrink $filename/outputtot.root "select > 0" MAPAnalyzer/t 2
	cp slimmed.root $filename
	rm slimmed.root
done

filenameTemp=$( find $gridname -type d -name '*0000*' | grep 200to)
for filename in $filenameTemp; do
	hadd $filename/outputtot.root -f $filename/output_*
	shrink $filename/outputtot.root "select > 0&&Boson_Pt > 70" MAPAnalyzer/t 3
	cp slimmed.root $filename
	rm slimmed.root
done

filenameTemp=$( find $gridname -type d -name '*0000*' | grep 400to)
for filename in $filenameTemp; do
	hadd $filename/outputtot.root -f $filename/output_*
	shrink $filename/outputtot.root "select > 0&&Boson_Pt > 90" MAPAnalyzer/t 4
	cp slimmed.root $filename
	rm slimmed.root
done

filenameTemp=$( find $gridname -type d -name '*0000*' | grep 600to)
for filename in $filenameTemp; do
	hadd $filename/outputtot.root -f $filename/output_*
	shrink $filename/outputtot.root "select > 0&&Boson_Pt > 110" MAPAnalyzer/t 5
	cp slimmed.root $filename
	rm slimmed.root
done

filenameTemp=$( find $gridname -type d -name '*0000*' | grep M-50_T | grep amc)
for filename in $filenameTemp; do
	hadd $filename/outputtot.root -f $filename/output_*
	shrink $filename/outputtot.root "select > 0" MAPAnalyzer/t 8
	cp slimmed.root $filename
	rm slimmed.root
done

filenameTemp=$( find $gridname -type d -name '*0000*' | grep M-50_T | grep mad)
for filename in $filenameTemp; do
	hadd $filename/outputtot.root -f $filename/output_*
	shrink $filename/outputtot.root "select > 0" MAPAnalyzer/t 1
	cp slimmed.root $filename
	rm slimmed.root
done

filenameTemp=$( find $gridname -type d -name '*0000*' | grep M-10to | grep mad)
for filename in $filenameTemp; do
	hadd $filename/outputtot.root -f $filename/output_*
	shrink $filename/outputtot.root "select > 0" MAPAnalyzer/t 6
	cp slimmed.root $filename
	rm slimmed.root
done

filenameTemp=$( find $gridname -type d -name '*0000*' | grep M-10to | grep amc)
for filename in $filenameTemp; do
	hadd $filename/outputtot.root -f $filename/output_*
	shrink $filename/outputtot.root "select > 0" MAPAnalyzer/t 9
	cp slimmed.root $filename
	rm slimmed.root
done

filenameTemp=$( find $gridname -type d -name '*0000*' | grep 70to | grep mad)
for filename in $filenameTemp; do
	hadd $filename/outputtot.root -f $filename/output_*
	shrink $filename/outputtot.root "select > 0" MAPAnalyzer/t 10
	cp slimmed.root $filename
	rm slimmed.root
done

filenameTemp=$( find $gridname -type d -name '*0000*' | grep 800to | grep mad)
for filename in $filenameTemp; do
	hadd $filename/outputtot.root -f $filename/output_*
	shrink $filename/outputtot.root "select > 0&&Boson_Pt > 110" MAPAnalyzer/t 11
	cp slimmed.root $filename
	rm slimmed.root
done

filenameTemp=$( find $gridname -type d -name '*0000*' | grep 1200to | grep mad)
for filename in $filenameTemp; do
	hadd $filename/outputtot.root -f $filename/output_*
	shrink $filename/outputtot.root "select > 0&&Boson_Pt > 110" MAPAnalyzer/t 12
	cp slimmed.root $filename
	rm slimmed.root
done

filenameTemp=$( find $gridname -type d -name '*0000*' | grep 2500to | grep mad)
for filename in $filenameTemp; do
	hadd $filename/outputtot.root -f $filename/output_*
	shrink $filename/outputtot.root "select > 0&&Boson_Pt > 110" MAPAnalyzer/t 13
	cp slimmed.root $filename
	rm slimmed.root
done

names=$(find $gridname -name "slimmed.root")
hadd -f $gridname/shrinkedDataTot.root $names

names=$(find $gridname -name "slimmed.root" | grep mad)
hadd -f $gridname/shrinkedDataTotMad.root $names
