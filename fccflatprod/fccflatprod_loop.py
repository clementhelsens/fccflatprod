
import sys

try:
  import heppy
  del sys.modules["heppy"]
  import FCCeeAnalyses
except:
  pass
try:
  import FCCeeAnalyses
  del sys.modules["FCCeeAnalyses"]
except:
  pass

print "replacing heppy with fccflatprod ...",
sys.modules["fccflatprod"] = __import__("fccflatprod")
sys.modules["heppy"] = __import__("fccflatprod")
sys.modules["FCCeeAnalyses"] = __import__("fccflatprod")
print "done"

import ROOT

#TODO: change library name
print "Load cxx analyzers ... ",
ROOT.gSystem.Load("libdatamodel")
ROOT.gSystem.Load("fcc_ana_ZH_Zmumu_cxx")
print ""


print "Parsing config file " , sys.argv[1], " ... ",
if __name__ == "__main__":
  execfile(sys.argv[1])
print "done"




fileListRoot = ROOT.vector('string')()
for fileName in comp.files:
    fileListRoot.push_back(fileName)
print "Create dataframe object from ", comp.files, " ... ", 
df = ROOT.RDataFrame("events", fileListRoot)
df = ROOT.initial_dataframe_convert(df)
print " done"

branchList = []

print "Running Sequence of Analyzers ...",
for ana in sequence.the_sequence:
  if "write_to_file" in ana.kwargs:
    if ana.kwargs["write_to_file"]:
      branchList.append(ana.kwargs["output"])
  df = ana.doit(df)
print " done"

print "New Columns: ",
print df.GetDefinedColumnNames()


branchListRoot = ROOT.vector('string')()
for branchName in branchList:
    branchListRoot.push_back(branchName)


print "Writing output to file  tree.root ... ",
df.Snapshot("events", "tree.root", branchListRoot)
print "done"
