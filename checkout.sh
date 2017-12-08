export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
source $VO_CMS_SW_DIR/cmsset_default.sh

cmsrel CMSSW_9_2_14_patch2
CMSSW_9_2_14_patch2/src/
cmsenv
git cms-init

git remote add friese https://github.com/rfriese/cmssw.git
git pull friese mvamet

git cms-addpkg DataFormats/METReco/
git cms-addpkg RecoMET/METPUSubtraction/

git clone git@github.com:rfriese/MetTools.git
