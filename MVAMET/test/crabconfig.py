#!/bin/env python
# crab submission script
# usage: python crabConfig.py submit

from CRABClient.UserUtilities import getUsernameFromSiteDB
from httplib import HTTPException
from CRABAPI.RawCommand import crabCommand
from CRABClient.ClientExceptions import ClientException
from multiprocessing import Process
#from Kappa.Skimming.registerDatasetHelper import get_sample_by_nick
#from Kappa.Skimming.datasetsHelper2015 import isData
import sys
from glob import glob
import os, shutil
#from Kappa.Skimming.tools import read_grid_control_includes
import datetime
today=datetime.date.today().strftime("%Y-%m-%d")
date = today # feel free to change

def submit(config):
	try:
		crabCommand('submit', config = config)
	except HTTPException as hte:
		print "Failed submitting task: %s" % (hte.headers)
	except ClientException as cle:
		print "Failed submitting task: %s" % (cle)

def crab_command(command):
	for dir in glob('/nfs/dust/cms/user/%s/kappa/crab_kappa_skim-%s/*'%(getUsernameFromSiteDB(), date)):
	#for dir in glob('/net/scratch_cms/institut_3b/%s/kappa/crab_kappa_skim-%s/*'%(getUsernameFromSiteDB(), date)):
		try:
			crabCommand(command, dir = dir)
		except HTTPException as hte:
			print hte

def check_path(path):
	if os.path.exists(path):
		print(path + " already exists! Delete it now in order to re-initialize it by crab? [y/n]")
		yes = set(['yes','y', 'ye', ''])
		no = set(['no','n'])

		choice = raw_input().lower()
		if choice in yes:
			shutil.rmtree(path)
			return
		elif choice in no:
			return
		else:
			sys.stdout.write(path + " already exists! Delete it now in order to re-initialize it by crab?")


def submission():
	from CRABClient.UserUtilities import config
	config = config()
	config.General.workArea = '/storage/jbod/nzaeh/%s'%(date)
	#config.General.workArea = '/nfs/dust/cms/user/%s/kappa/crab_kappa_skim80X-%s'%(getUsernameFromSiteDB(), date)
	#config.General.workArea = '/net/scratch_cms/institut_3b/%s/kappa/crab_kappa_skim-%s'%(getUsernameFromSiteDB(), date)
	check_path(config.General.workArea)
	config.General.transferOutputs = True
	config.General.transferLogs = True
	config.User.voGroup = 'dcms'
	
	config.JobType.pluginName = 'Analysis'
	config.JobType.psetName = 'makeMVAMETTrainingNtuple.py'
	#config.JobType.inputFiles = ['Spring16_25nsV6_DATA.db', 'Spring16_25nsV6_MC.db']
	#config.JobType.inputFiles = ['Summer16_23Sep2016V4_MC.db']
	config.JobType.allowUndistributedCMSSW = True
	config.JobType.maxMemoryMB = 3500
	config.Site.blacklist = ["T2_BR_SPRACE"]
	config.Data.inputDBS = 'global'
	config.Data.splitting = 'FileBased'
	config.Data.unitsPerJob = 10
	config.Data.outLFNDirBase = '/store/user/%s/metskim/92X_%s'%(getUsernameFromSiteDB(), date)
	#config.Data.outLFNDirBase = '/store/user/%s/higgs-kit/skimming/80X_%s'%(getUsernameFromSiteDB(), date)
	config.Data.publication = False
	
	config.Site.storageSite = "T2_DE_DESY"
	# load nicknames form gc-style config files and write them to a flat nicknames list
	#nicknames = read_grid_control_includes(["samples/13TeV/Spring16_SM_Analysis.conf"])
	#nicknames = read_grid_control_includes(["samples/13TeV/Spring16_SM_Higgs_CPmixing_2.conf"])
	#nicknames = read_grid_control_includes(["samples/13TeV/2016B_Data.conf"])
	#nicknames = ['SUSYGluGluToHToTauTauM160_RunIIFall15MiniAODv2_76X_13TeV_MINIAOD_pythia8']
	"""	
	datasets = [
	'/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM',
	'/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM',
	'/DYJetsToLL_M-150_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM',
	'/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM',
	'/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1/MINIAODSIM',
	'/DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1/MINIAODSIM',
	'/DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1/MINIAODSIM',
	'/DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1/MINIAODSIM',
	'/DYJetsToLL_M-50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1/MINIAODSIM'
	]
	
	"""
	datasets = [
		'/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer17MiniAOD-92X_upgrade2017_realistic_v10_ext1-v2/MINIAODSIM'
	]

	"""
	datasetsData = [
	'/SingleMuon/Run2016B-23Sep2016-v3/MINIAOD',
	'/SingleMuon/Run2016C-23Sep2016-v1/MINIAOD',
	'/SingleMuon/Run2016D-23Sep2016-v1/MINIAOD',
	'/SingleMuon/Run2016E-23Sep2016-v1/MINIAOD',
	'/SingleMuon/Run2016F-23Sep2016-v1/MINIAOD',
	'/SingleMuon/Run2016G-23Sep2016-v1/MINIAOD',
	]

	nicksData = [
	'SingleMuonRun2016Bv3',
	'SingleMuonRun2016Cv1',
	'SingleMuonRun2016Dv1',
	'SingleMuonRun2016Ev1',
	'SingleMuonRun2016Fv1',
	'SingleMuonRun2016Gv1',

]



	#extensiondatasets
	datasetsExt = [
        '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v2/MINIAODSIM',
        '/DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
        '/DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
        '/DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM'
	] 
	"""
	nicks = ["DYext1v2"]	

	config.JobType.outputFiles = ['output.root']
	
	for indexData in range(len(datasets)):
	    # loop over datasets and get repsective nicks
	    #for nickname in nicknames:
	    config.General.requestName = nicks[indexData]

	    #Global Tag for Data
	    config.JobType.pyCfgParams = ['globalTag=92X_upgrade2017_realistic_v14']
	    #config.JobType.pyCfgParams = ['globalTag=80X_dataRun2_Prompt_ICHEP16JEC_v0' if isData(nickname) else 'globalTag=80X_mcRun2_asymptotic_2016_miniAODv2_v1' #,'kappaTag=KAPPA_2_1_0','nickname=%s'%(nickname),'outputfilename=kappa_%s.root'%(nickname),'testsuite=False']
	    
	    #config.Data.inputDataset = get_sample_by_nick(nickname)
	    config.Data.inputDataset = datasets[indexData]#'/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1/MINIAODSIM'
	    p = Process(target=submit, args=(config,))
	    p.start()
	    p.join()
	    
	"""
        for data in datasetsExt:
	    # loop over datasets and get repsective nicks
	    #for nickname in nicknames:
	    config.General.requestName = data[1:45] + '_ext'
	    #config.JobType.pyCfgParams = ['']
	    #config.JobType.pyCfgParams = ['globalTag=80X_dataRun2_Prompt_ICHEP16JEC_v0' if isData(nickname) else 'globalTag=80X_mcRun2_asymptotic_2016_miniAODv2_v1' #,'kappaTag=KAPPA_2_1_0','nickname=%s'%(nickname),'outputfilename=kappa_%s.root'%(nickname),'testsuite=False']
	    
	    #config.Data.inputDataset = get_sample_by_nick(nickname)
	    config.Data.inputDataset = data#'/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1/MINIAODSIM'
	    p = Process(target=submit, args=(config,))
	    p.start()
	    p.join()
	"""
	

if __name__ == "__main__":
	if len(sys.argv) == 1: 
		print "no setting provided"
		sys.exit()
	if sys.argv[1] == "submit":
		submission()
	elif sys.argv[1] in ["status", "resubmit", "kill"]:
		crab_command(sys.argv[1])
	else:
		print "setting \"%s\" is not implemented"% sys.argv[1]

