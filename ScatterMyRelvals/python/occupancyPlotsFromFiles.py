from optparse import OptionParser
parser = OptionParser()
parser.add_option("--inputFiles", dest="inputFiles", default='relValFiles.pkl', type="string", action="store", help="pkl file with eos filenames")
parser.add_option("--plotDir", dest="plotDir", default='relValData.zpkl', type="string", action="store", help="output plot directory")
parser.add_option("--miniAOD", dest="miniAOD", action="store_true", help="Just do a miniAOD subset.")

(options, args) = parser.parse_args()

import ROOT
from DataFormats.FWLite import Events, Handle
from PhysicsTools.PythonAnalysis import *
from math import *
import sys, os
from MetTools.Commons.helpers import load
from helpers import translatePdgIdToType

ROOT.gStyle.SetOptStat(0)
if not hasattr(ROOT, "tdrStyle"):
  ROOT.gROOT.ProcessLine(".L $CMSSW_BASE/src/MetTools/Commons/scripts/tdrstyle.C")
  ROOT.setTDRStyle()
  ROOT.tdrStyle.SetPadRightMargin(0.18)
  ROOT.gROOT.ProcessLine(".L $CMSSW_BASE/src/MetTools/Commons/scripts/useNiceColorPalette.C")
  ROOT.useNiceColorPalette(255)

plots = {\
  1:[{"name":"h_eta_vs_pt",                      "yLabel":"p_{T} (GeV)", "yVar":lambda x:x.pt(), 'yBinning':(60,0,1.5), 'etaBinning':(60,-3,3)}],
  5:[{"name":"h_eta_vs_E",'pfType':5,            "yLabel":"E (GeV)", "yVar":lambda x:x.Energy(), 'yBinning':(60,0,2.5), 'etaBinning':(60,-3,3)}],
  4:[{"name":"gamma_eta_vs_E",'pfType':4,        "yLabel":"E (GeV)", "yVar":lambda x:x.Energy(), 'yBinning':(60,0,1.5), 'etaBinning':(60,-3,3)}],
  6:[{"name":"egammaHFPlus_eta_vs_E",'pfType':7, "yLabel":"E (GeV)", "yVar":lambda x:x.Energy(), 'yBinning':(60,0,15), 'etaBinning':(30,3,5)},
     {"name":"egammaHFMinus_eta_vs_E",'pfType':7,"yLabel":"E (GeV)", "yVar":lambda x:x.Energy(), 'yBinning':(60,0,15), 'etaBinning':(30,-5,-3)}],
  7:[{"name":"hHFPlus_eta_vs_E",'pfType':6,      "yLabel":"E (GeV)", "yVar":lambda x:x.Energy(), 'yBinning':(60,0,15), 'etaBinning':(30,3,5)},
     {"name":"hHFMinus_eta_vs_E",'pfType':6,     "yLabel":"E (GeV)", "yVar":lambda x:x.Energy(), 'yBinning':(60,0,15), 'etaBinning':(30,-5,-3)}],
}

for k in plots.keys():
  for p in plots[k]:
    binning = list(p['etaBinning'])+list(p['yBinning'])
    p['histo'] = ROOT.TH2F(p['name'],p['name'],*binning)

small = True

ROOT.gSystem.Load("libFWCoreFWLite.so")
ROOT.AutoLibraryLoader.enable()

if options.miniAOD:
  print "Running on miniAOD"
  edmCollections = { \
    'pfCandidates':("vector<pat::PackedCandidate>", "packedPFCandidates", "")
  } 
else:
  print "Running on RECO/AOD"
  edmCollections = { \
    'pfCandidates':("vector<reco::PFCandidate>", "particleFlow", "")
  }

from categories import *
inputFiles = options.inputFiles.split(',')
inputFiles = inputFiles[:1] if not small else inputFiles
print "Running over files:",inputFiles
print "Will write to:",options.outputFile

handles={k:Handle(edmCollections[k][0]) for k in edmCollections.keys()}
res={}

events = Events(inputFiles)
events.toBegin()
products={}
size=events.size() if not small else 10

missingCollections=[]
for nev in range(size):
  if nev%1000==0:print nev,'/',size
  events.to(nev)
  for k in [ x for x in edmCollections.keys() if x not in missingCollections]:
    try:
      events.getByLabel(edmCollections[k][1:],handles[k])
      products[k]=handles[k].product()
    except:
      products[k]=None
      print "Not found:",k
      missingCollections.append(k)
  d={}
#  print "Event",nev,'size',products['pfCandidates'].size()
  assert products['pfCandidates'], "pfCandidates not found!"
  for p in range(products['pfCandidates'].size()):
    cand = products['pfCandidates'][p]
    candID = translatePdgIdToType(cand.pdgId()) if options.miniAOD else cand.particleId() 
    for p in plots[candID]:
      eta=abs(cand.eta())
      if eta>p['etaBinning'][1] and eta<p['etaBinning'][2]:
        yVar = p['yVar'](cand)
        p['histo']      .Fill(eta, yVar)

for k in plots.keys():
  for p in plots[k]:
    histo=p['histo']
    histo.GetXaxis().SetTitle("#eta")
    histo.GetXaxis().SetLabelSize(0.04)
    histo.GetYaxis().SetTitle(p['yLabel'])
    histo.GetYaxis().SetLabelSize(0.04)

    c1 = ROOT.TCanvas()
    histo.Draw('colz')
    c1.RedrawAxis()
    c1.SetLogz(1)
    c1.Print(options.plotDirectory+'/'+p['name']+'_logZ.png')
    c1.Print(options.plotDirectory+'/'+p['name']+'_logZ.pdf')
    c1.Print(options.plotDirectory+'/'+p['name']+'_logZ.root')
    c1.SetLogz(0)
    histo.Draw('colz')
    c1.RedrawAxis()
    c1.Print(options.plotDirectory+'/'+p['name']+'.png')
    c1.Print(options.plotDirectory+'/'+p['name']+'.pdf')
    c1.Print(options.plotDirectory+'/'+p['name']+'.root')
