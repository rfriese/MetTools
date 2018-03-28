import sys
import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing
from PhysicsTools.PatAlgos.tools.tauTools import *
from RecoMET.METPUSubtraction.MVAMETConfiguration_cff import runMVAMET

options = VarParsing ('python')
options.register ('inputFile', 'root://cms-xrd-global.cern.ch//store/mc/RunIISummer17MiniAOD/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/92X_upgrade2017_realistic_v10_ext1-v2/10000/0A8639B4-1D94-E711-9C68-02163E0135C6.root', VarParsing.multiplicity.singleton, VarParsing.varType.string, "Path to a testfile")
options.register ('globalTag',"92X_upgrade2017_realistic_v14",VarParsing.multiplicity.singleton,VarParsing.varType.string,'input global tag to be used');
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
    process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff")
    process.GlobalTag.globaltag = options.globalTag
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
	runMetCorAndUncFromMiniAOD(process, isData=options.isData, jetCollUnskimmed=jetCollection)
	#process.patPFMet.computeMETSignificance = cms.bool(False)
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
    cut = cms.string('(abs(pdgId()) == 13 && !isDirectPromptTauDecayProductFinalState()) || (abs(pdgId()) == 11 && !isDirectPromptTauDecayProductFinalState())'),
    #cut = cms.string('(abs(pdgId()) == 15 && !isDirectPromptTauDecayProductFinalState())'),
    #cut = cms.string('isDirectPromptTauDecayProductFinalState()'),
    stableOnly = cms.bool(False)
)

process.goodEventFilter = cms.EDFilter("CandViewCountFilter",
										src = cms.InputTag("slimmedMuonsTight"),
										minNumber = cms.uint32(2),
										maxNumber = cms.uint32(2),
                                        filter = cms.bool(True) )

process.MVAMETtask = cms.Task(
    process.egmGsfElectronIDTask,
    process.slimmedMuonsTight,
    process.slimmedElectronsTight,
    process.slimmedTausLoose,
    process.slimmedTausLooseCleaned,
    process.tausSignificance,
    process.tauMET,
    process.tauPFMET,
    process.allDecayProducts,
    process.tauDecayProducts,
    process.patpfTrackMET,
    process.pfTrackMET,
    process.pfTrackMETCands,
    process.pfChargedPV,
    process.patpfNoPUMET,
    process.pfNoPUMET,
    process.pfNoPUMETCands,
    process.neutralInJets,
    process.patJetsReapplyJEC,
    process.patJetCorrFactorsReapplyJEC,
    process.pileupJetIdUpdated,
    process.pfNeutrals,
    process.patpfPUCorrectedMET,
    process.pfPUCorrectedMET,
    process.pfPUCorrectedMETCands,
    process.patpfPUMET,
    process.pfPUMET,
    process.pfPUMETCands,
    process.pfChargedPU
)

process.seq = cms.Sequence(
    process.genZEvent *
    process.goodEventFilter*
    process.MVAMET*
	process.MAPAnalyzer,
    process.MVAMETtask)
process.p = cms.Path (process.seq)

