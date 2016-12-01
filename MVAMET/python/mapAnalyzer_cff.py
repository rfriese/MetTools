import FWCore.ParameterSet.Config as cms
metstrings = []
postfixes = [ "Cov00", "Cov11", "Phi", "dPhi", "Pt", "sumEt", "sumEtFraction", "PerpZ", "LongZ"]
for met in ["slimmedMETs", "patpfTrackMET", "patpfNoPUMET", "patpfPUCorrectedMET", "patpfPUMET", "slimmedMETsPuppi"]:
  for postfix in postfixes:
    metstrings.append("recoil" + met + "_" + postfix)

jetAttributes = ["Eta", "M", "Phi", "Pt"]
for jetID in range(0,5):
  for attribute in jetAttributes:
    metstrings.append(("Jet%i"%jetID) + "_" + attribute)

metstrings.extend([ "dmvamet_Pt", "dmvamet_Phi", "dpfmet_Pt", "dpfmet_Phi", "MVAMET_Pt", "MVAMET_sumEt", "MVAMET_Phi", "PhiTrainingResponse", "RecoilTrainingResponse",
                 "genMet_Pt",
                 "genMet_Phi",
                 "weight",
                 "select",
                 "NCleanedJets",
                 "NVertex",
                 "Boson_Pt",
                 "Boson_Phi",
                 "Boson_M",
                 "Boson_Eta",
                 "Boson_sumET",
                 "Boson_daughter1_PdgId",
		 "Boson_daughter2_PdgId",
		 "Boson_daughter1_Pt",
		 "Boson_daughter2_Pt",
		 "Boson_daughter1_Phi",
		 "Boson_daughter2_Phi",
		 "Boson_daughter1_Eta",
		 "Boson_daughter2_Eta",
		 "Boson_daughter1_Charge",
		 "Boson_daughter2_Charge",
                 "nCombinations"
])

MAPAnalyzer =cms.EDAnalyzer('MAPAnalyzer',
                           srcVariables = cms.InputTag("MVAMET"),
                           srcVariableNames = cms.InputTag("MVAMET"),
                           variableNamesToSave = cms.vstring( metstrings ),
                           srcGenEvent = cms.InputTag("generator")
                           )
