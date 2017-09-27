#include "TTree.h"
#include "../interface/GBRTrainer.h"
#include "CondFormats/EgammaObjects/interface/GBRForest.h"
//#include "Cintex/Cintex.h"

#include <boost/property_tree/json_parser.hpp>
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp>
#include <boost/foreach.hpp>
#include <cassert>
#include <exception>
#include <iostream>
#include <sstream>
#include <string>
#include "TSystem.h"

#include "../interface/applyphi.h"

using namespace std;

int main(int argc, char* argv[] ) {

  std::string config = argv[1];
  std::cout << argv[1] << std::endl;


	// config file einlesen
  boost::property_tree::ptree pt;
  try 
  {
    std::ifstream in(argv[1]);
    std::stringstream ss;
    ss << in.rdbuf();      
    boost::property_tree::json_parser::read_json(ss, pt);
  } catch (std::exception const& e)
  {
    std::cerr << e.what() << std::endl;
    return 1;
  }

  std::vector<boost::property_tree::ptree> trainingProperties;
  BOOST_FOREACH(boost::property_tree::ptree::value_type &v, pt.get_child("activeTrainings"))
  {
    assert(v.first.empty());
    trainingProperties.push_back( pt.get_child(v.second.data()));
  }

  std::string inputFilename;
  if (argc==3)
  	inputFilename = argv[2];
  else
  	inputFilename = pt.get<std::string>("inputFile");

  std::string outputDir;
  if (argc==4)
  	outputDir = argv[3];
  else
  	outputDir = pt.get<std::string>("outputdir");

  std::string weightfilename = pt.get<std::string>("weightfilename");

  TFile *inputFile = TFile::Open(inputFilename.c_str());
  std::string foldername = pt.get<std::string>("Folder");
  TTree *inputTree = (TTree*)(inputFile->Get(foldername.c_str()));

  std::cout << "input tree: " << inputTree << std::endl;
  std::cout << "This many: " << trainingProperties.size() << std::endl;
  std::string outputfile = outputDir + "/data.root";
  std::string outputdir = outputDir + "/";  
  std::string lastfile;

  for(size_t iTrain = 0; iTrain < trainingProperties.size(); ++iTrain)
  {
    cout << "JUMPING INTO FOR LOOP TREE" << endl;
    
    if(iTrain>0)
    {
      inputFile = TFile::Open(outputfile.c_str());
      inputTree = (TTree*)(inputFile->Get("t"));
      lastfile = outputfile;
      outputfile = outputdir + "data" + std::to_string(iTrain) + ".root";
      TObjArray *entryarray = new TObjArray(*inputTree->GetListOfBranches());
      std::cout << "Objects: " << entryarray->GetEntries() << std::endl;
      std::cout << outputfile << std::endl;
    }
    
    
    if(trainingProperties[iTrain].get<int>("mode") != -1)
    {
	//applyTraining *user = new applyTraining(trainingProperties[iTrain], inputTree);
	/*
	BOOST_FOREACH(boost::property_tree::ptree::value_type &v, trainingProperties[iTrain].get_child("friends"))
	{
	  assert(v.first.empty());
	  std::string friendName = v.second.data();
	  inputTree->AddFriend("t", (outputfile).c_str());
	}
	*/
	cout << "JUMPING INTO THE MODE 0 TREE" << endl;
	

	applyTraining *user = new applyTraining(trainingProperties[iTrain].get<std::string>("name"), 
						trainingProperties[iTrain].get<std::string>("apply_MVA_to"),
						weightfilename,
						trainingProperties[iTrain].get<int>("mode"),
						inputTree,
						inputFilename,
						outputfile);
	user->getResults();
	delete user;
	inputFile->Close();
	if (iTrain > 0)
	    gSystem->Exec(("rm " + lastfile).c_str());
    }
/*
    else 
    {
	inputTree->AddFriend("t", "CovU2.root");
	cout << "JUMPING INTO THE MODE 1 TREE" << endl;
	applyTraining *user = new applyTraining(trainingProperties[iTrain].get<std::string>("name"), 
						trainingProperties[iTrain].get<std::string>("apply_MVA_to"),
						weightfilename,
						trainingProperties[iTrain].get<int>("mode"),
						inputTree,
						inputFilename);
	user->getResults();
	delete user;
    }
*/
    std::cout << "Initialized." << std::endl;
  }
}

