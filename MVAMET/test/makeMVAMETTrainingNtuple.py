import sys
import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing
from PhysicsTools.PatAlgos.tools.tauTools import *
from RecoMET.METPUSubtraction.MVAMETConfiguration_cff import runMVAMET

options = VarParsing ('python')
options.register ('globalTag',"80X_mcRun2_asymptotic_2016_miniAODv2_v1",VarParsing.multiplicity.singleton,VarParsing.varType.string,'input global tag to be used');
options.register ('inputFile', 'file://////storage/jbod/nzaeh/00E9D1DA-105D-E611-A56E-FA163EE988CA.root', VarParsing.multiplicity.singleton, VarParsing.varType.string, "Path to a testfile")
options.register ("localSqlite", '', VarParsing.multiplicity.singleton, VarParsing.varType.string, "Path to a local sqlite file")
options.register ("reapplyJEC", True, VarParsing.multiplicity.singleton, VarParsing.varType.bool, "Reapply JEC to Jets")
options.register ("reapplyPUJetID", True, VarParsing.multiplicity.singleton, VarParsing.varType.bool, "Reapply PU Jet ID")
options.register ("recomputeMET", True, VarParsing.multiplicity.singleton, VarParsing.varType.bool, "Recomute MET instead of taking it from MiniAOD")
options.register ("isData", False, VarParsing.multiplicity.singleton, VarParsing.varType.bool, "Input is data")
options.parseArguments()

process = cms.Process("MVAMET")

process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
jetCollection = "slimmedJets"

if (options.localSqlite == ''):
    process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff")
    process.GlobalTag.globaltag = options.globalTag
else:
    from RecoMET.METPUSubtraction.jet_recorrections import loadLocalSqlite
    loadLocalSqlite(process, options.localSqlite) 

if options.reapplyPUJetID:
    from RecoMET.METPUSubtraction.jet_recorrections import reapplyPUJetID
    reapplyPUJetID(process)

if options.reapplyJEC:
    from RecoMET.METPUSubtraction.jet_recorrections import recorrectJets
    recorrectJets(process, options.isData)
    jetCollection = "patJetsReapplyJEC"

if options.recomputeMET:
	from PhysicsTools.PatUtils.tools.runMETCorrectionsAndUncertainties import runMetCorAndUncFromMiniAOD
	runMetCorAndUncFromMiniAOD(process, isData=options.isData, jetCollUnskimmed=jetCollection  )

	from PhysicsTools.PatAlgos.slimming.puppiForMET_cff import makePuppiesFromMiniAOD
	makePuppiesFromMiniAOD( process );
	runMetCorAndUncFromMiniAOD(process,
                             isData=options.isData,
                             metType="Puppi",
                             pfCandColl=cms.InputTag("puppiForMET"),
                             recoMetFromPFCs=True,
                             reclusterJets=True,
                             jetFlavor="AK4PFPuppi",
                             postfix="Puppi")

if options.reapplyPUJetID:
    getattr(process, jetCollection).userData.userFloats.src += ['pileupJetIdUpdated:fullDiscriminant']

# configure MVA MET
runMVAMET( process, jetCollectionPF = jetCollection)

## set input files
process.source = cms.Source("PoolSource")
process.source.fileNames = cms.untracked.vstring(options.inputFile)
## logger
process.load('FWCore.MessageLogger.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 50

#! Output and Log                                                                                                                                                            
process.options   = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))
process.options.allowUnscheduled = cms.untracked.bool(True)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(options.maxEvents)
) 



if not hasattr(process, "p"):
    process.p = cms.Path()
process.load('CommonTools.UtilAlgos.TFileService_cfi')
process.TFileService.fileName = cms.string('output.root')
process.TFileService.closeFileFast = cms.untracked.bool(True)
from MetTools.MVAMET.mapAnalyzer_cff import MAPAnalyzer
process.MAPAnalyzer = MAPAnalyzer
process.MVAMET.saveMap = cms.bool(True)
process.genZEvent = cms.EDFilter("GenParticleSelector",
    filter = cms.bool(True),
    src = cms.InputTag("prunedGenParticles"),
    cut = cms.string('abs(pdgId()) == 13 && !isDirectPromptTauDecayProductFinalState()'),
    #cut = cms.string('isDirectPromptTauDecayProductFinalState()'),
    stableOnly = cms.bool(False)
)
process.skimmvamet = cms.Sequence( process.genZEvent * process.MVAMET * process.MAPAnalyzer)
process.p *= (process.skimmvamet)
