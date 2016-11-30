#specify directory name in which the skimmed data lies
gridname=/storage/jbod/nzaeh/2016-11-21/Gridoutput/

filename=$( find $gridname -type d -name '*0000*' | grep 100to)
hadd $filename/outputtot.root -f $filename/output_*
shrink $filename/outputtot.root "select > 0 && (recoilslimmedMETs_LongZ > -2000 && recoilslimmedMETs_LongZ < 2000)" MAPAnalyzer/t 2
cp slimmed.root $filename
rm slimmed.root

filename=$( find $gridname -type d -name '*0000*' | grep 200to)
hadd $filename/outputtot.root -f $filename/output_*
shrink $filename/outputtot.root "select > 0&&Boson_Pt > 70&& (recoilslimmedMETs_LongZ > -2000 && recoilslimmedMETs_LongZ < 2000)" MAPAnalyzer/t 3
cp slimmed.root $filename
rm slimmed.root

filename=$( find $gridname -type d -name '*0000*' | grep 400to)
hadd $filename/outputtot.root -f $filename/output_*
shrink $filename/outputtot.root "select > 0&&Boson_Pt > 90&& (recoilslimmedMETs_LongZ > -2000 && recoilslimmedMETs_LongZ < 2000)" MAPAnalyzer/t 4
cp slimmed.root $filename
rm slimmed.root

filename=$( find $gridname -type d -name '*0000*' | grep 600to)
hadd $filename/outputtot.root -f $filename/output_*
shrink $filename/outputtot.root "select > 0&&Boson_Pt > 110&& (recoilslimmedMETs_LongZ > -2000 && recoilslimmedMETs_LongZ < 2000)" MAPAnalyzer/t 5
cp slimmed.root $filename
rm slimmed.root

filename=$( find $gridname -type d -name '*0000*' | grep M-50_T | grep amc)
hadd $filename/outputtot.root -f $filename/output_*
shrink $filename/outputtot.root "select > 0&& (recoilslimmedMETs_LongZ > -2000 && recoilslimmedMETs_LongZ < 2000)" MAPAnalyzer/t 8
cp slimmed.root $filename
rm slimmed.root

filename=$( find $gridname -type d -name '*0000*' | grep M-50_T | grep mad)
hadd $filename/outputtot.root -f $filename/output_*
shrink $filename/outputtot.root "select > 0&& (recoilslimmedMETs_LongZ > -2000 && recoilslimmedMETs_LongZ < 2000)" MAPAnalyzer/t 1
cp slimmed.root $filename
rm slimmed.root

gridname=/storage/jbod/nzaeh/2016-11-18/Gridoutput/
filename=$( find $gridname -type d -name '*0000*' | grep M-150_ )
hadd $filename/outputtot.root -f $filename/output_*
shrink $filename/outputtot.root "select > 0&& (recoilslimmedMETs_LongZ > -2000 && recoilslimmedMETs_LongZ < 2000)" MAPAnalyzer/t 7
cp slimmed.root $filename
rm slimmed.root

filename=$( find $gridname -type d -name '*0000*' | grep M-10to | grep mad)
hadd $filename/outputtot.root -f $filename/output_*
shrink $filename/outputtot.root "select > 0&& (recoilslimmedMETs_LongZ > -2000 && recoilslimmedMETs_LongZ < 2000)" MAPAnalyzer/t 6
cp slimmed.root $filename
rm slimmed.root

filename=$( find $gridname -type d -name '*0000*' | grep M-10to | grep amc)
hadd $filename/outputtot.root -f $filename/output_*
shrink $filename/outputtot.root "select > 0&& (recoilslimmedMETs_LongZ > -2000 && recoilslimmedMETs_LongZ < 2000)" MAPAnalyzer/t 9
cp slimmed.root $filename
rm slimmed.root

names=$(find $gridname -name "slimmed.root")
hadd -f $gridname/shrinkedDataTot.root $names


gridname=/storage/jbod/nzaeh/2016-11-21/Gridoutput/

names=$(find $gridname -name "slimmed.root")
hadd -f $gridname/shrinkedDataTot.root $names


