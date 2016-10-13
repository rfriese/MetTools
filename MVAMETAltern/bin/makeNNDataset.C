#include "TFile.h"
#include "TTree.h"


#include <iostream>
#include <fstream>
#include <math.h>



using namespace std;

const float  PI_F=3.14159265358979f;

/* Files belong to the following variable refered to in fileName
DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8 --> 1
DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8 --> 8
DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8 --> 9
DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8 --> 6
DYJetsToLL_M-150_TuneCUETP8M1_13TeV-madgraphMLM-pythia8 --> 7
DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8 --> 2
DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8 --> 3
DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8 --> 4
DYJetsToLL_M-50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8 --> 5
*/



int main(int argc, char* argv[] )
{
	std::cout << "Hallo Welt!" << std::endl;

	cout << "Loading Rootfile.." << endl;
	
	std::string filename1 = argv[1];
	TFile *inputFile1 = TFile::Open(filename1.c_str());
	TTree *inputTree1 = (TTree*)(inputFile1->Get("MAPAnalyzer/t"));
	
	std::string filenameFriend = argv[2];
	
	std::string filenameFriendPhi = filenameFriend + "PhiCorrectedRecoil.root";
	TFile *inputFileFriendPhi = TFile::Open(filenameFriendPhi.c_str());
	TTree *inputTreeFriendPhi = (TTree*)(inputFileFriendPhi->Get("PhiCorrectedRecoil"));

	std::string filenameFriendRecoil = filenameFriend + "LongZCorrectedRecoil.root";
	TFile *inputFileFriendLongZ = TFile::Open(filenameFriendRecoil.c_str());
	TTree *inputTreeFriendLongZ = (TTree*)(inputFileFriendLongZ->Get("LongZCorrectedRecoil"));
	

	
	cout << "Entries: " << inputTree1->GetEntries() << endl;
	cout << "Entries Friend Phi: " << inputTreeFriendPhi->GetEntries() << endl;
	cout << "Entries Friend LongZ: " << inputTreeFriendLongZ->GetEntries() << endl;
	
	if (inputTree1->GetEntries() != inputTreeFriendPhi->GetEntries() || inputTreeFriendPhi->GetEntries() != inputTreeFriendLongZ->GetEntries())
	{
	    cout << "Different amount of entries in tree and its friends, wrong input data? (quit now)";
	    return 1;
	}
	
	TObjArray *entryarray = new TObjArray(*inputTree1->GetListOfBranches());

	TObjArray *entryarrayPhi = new TObjArray(*inputTreeFriendPhi->GetListOfBranches());

	TObjArray *entryarrayLongZ = new TObjArray(*inputTreeFriendLongZ->GetListOfBranches());

	cout << "Number of objects = " << entryarray->GetEntries() << endl; 
	cout << "Number of objects Phi = " << entryarrayPhi->GetEntries() << endl; 
	cout << "Number of objects LongZ= " << entryarrayLongZ->GetEntries() << endl; 
	//cout << "Anzahl Objekte = " << inputTree1->GetListOfBranches()->GetEntries() << endl; 

//	fstream XTrainoutput;
//	XTrainoutput.open("xtrain.csv", ios::out);
	
//	fstream YTrainoutput;
//	YTrainoutput.open("ytrain.csv", ios::out);
	//textoutput << "Boson_Pt" << endl;
	
	fstream dataset;
	dataset.open("dataMVAMet.csv", ios::out);
	
	
	/*for (int i = 0; i < entryarray->GetEntries(); i++)
	{
		const char *varname = entryarray->At(i)->GetName();
		const char *testvarname = "testblub";
		vector<float> (&testvarname);
		
	}
	*/
	
	//for (int i = 0; i < 50; i++)
	
	
	int maxEntries = 0;
	if (inputTree1->GetEntries() > 1000000)
	    maxEntries = 1000000;
	else 
	    maxEntries = inputTree1->GetEntries();

	int variablesize = entryarray->GetEntries()+2+entryarrayPhi->GetEntries()+entryarrayLongZ->GetEntries();
	
	vector<float> datacontainer(maxEntries*(variablesize));
	
	cout << "Loading data into local storage.." << endl;
	int selectentry = 0;
	//variablesize - 2 as it does not store the additional 2 calculated target variables
	float varlist[(variablesize-2)];
	for (int j = 0; j < entryarray->GetEntries(); j++)
	    {
		inputTree1->SetBranchAddress(entryarray->At(j)->GetName(),&varlist[j]);
		if (strcmp(entryarray->At(j)->GetName(),"select") == 0)
		    selectentry = j;
	    }
	    
	for (int j = 0; j < entryarrayPhi->GetEntries(); j++)
	    {
		inputTreeFriendPhi->SetBranchAddress(entryarrayPhi->At(j)->GetName(),&varlist[j+entryarray->GetEntries()]);
	    }
	    
	for (int j = 0; j < entryarrayLongZ->GetEntries(); j++)
	    {
		inputTreeFriendLongZ->SetBranchAddress(entryarrayLongZ->At(j)->GetName(),&varlist[j+entryarray->GetEntries()+entryarrayPhi->GetEntries()]);
	    }
	    
	
	int count = 0;
	int treecount = 0;
	//for (int i = 0; i < maxEntries; i++)
	while (count < maxEntries && treecount < inputTree1->GetEntries())
	{
	    inputTree1 -> GetEntry(treecount);
	    inputTreeFriendLongZ -> GetEntry(treecount);
	    inputTreeFriendPhi -> GetEntry(treecount);
	    
	    if (varlist[selectentry] == 1)
	    {
		for (int j = 0; j < variablesize-2; j++)
		{
		    
		    {
			datacontainer[count*(variablesize)+j] = varlist[j];
			
			
		    }
		}
		count++;
	    }
	    treecount++;
	}	
	maxEntries = count;
	cout << "CSV Entries: " << count << endl;
	
	float mean[variablesize-2];
	float variance[variablesize-2];
	
	for (int j = 0; j < variablesize-2; j++)
	{
	    mean[j] = 0;
	    variance[j] = 0;
	    for (int i = 0; i < maxEntries; i++)
		mean[j] += datacontainer[i*(variablesize)+j];
	    mean[j] /= maxEntries;
	    
	    for (int i = 0; i < maxEntries; i++)
		variance[j] = (datacontainer[i*(variablesize-2)+j] - mean[j])*(datacontainer[i*(variablesize-2)+j] - mean[j]);
	    variance[j] /= maxEntries;
	}

	int boson_Phi = 0;
	int boson_Pt = 0;
	int recoilpatpfMETT1_Phi = 0;
	int PhiCorrectedRecoil_LongZ = 0;
	
	for (int i = 0; i < entryarray->GetEntries(); i++)
	{
	    //search for needed variables for target variable
	    if (strcmp(entryarray->At(i)->GetName(),"recoilpatpfMETT1_Phi") == 0)
		recoilpatpfMETT1_Phi = i;
	    if (strcmp(entryarray->At(i)->GetName(),"Boson_Phi") == 0)
		boson_Phi = i;
	    if (strcmp(entryarray->At(i)->GetName(),"Boson_Pt") == 0)
		boson_Pt = i;
	    if (variance[i] != 0)
		dataset <<  entryarray->At(i)->GetName() << ",";
	}
	
	
	
	
	for (int i = 0; i < entryarrayPhi->GetEntries(); i++)
	{
	    if (strcmp(entryarrayPhi->At(i)->GetName(),"PhiCorrectedRecoil_LongZ") == 0)
		PhiCorrectedRecoil_LongZ = i;
	    if (variance[i + entryarray->GetEntries()] != 0)
		dataset <<  entryarrayPhi->At(i)->GetName() << ",";
	}
	
	for (int i = 0; i < entryarrayLongZ->GetEntries(); i++)
	{
	    if (variance[i + entryarray->GetEntries()+entryarrayPhi->GetEntries()] != 0)
		dataset <<  entryarrayLongZ->At(i)->GetName() << ",";
	}
	
	//add target variables
	dataset << "targetphi,targetrecoil";
	dataset << endl;
	
	cout << "Processing data, generating csv-File.." << endl;
	for (int i = 0; i < maxEntries; i++)
	{
	    for (int j = 0; j < entryarray->GetEntries(); j++)
		if (variance[j] != 0)
		    dataset << datacontainer[i*(variablesize)+j] << ",";
	    
	    for (int j = 0; j < entryarrayPhi->GetEntries(); j++)
		if (variance[j+entryarray->GetEntries()] != 0)
		    dataset << datacontainer[i*(variablesize)+j+entryarray->GetEntries()] << ",";
		
	    for (int j = 0; j < entryarrayLongZ->GetEntries(); j++)
		if (variance[j+entryarray->GetEntries()+entryarrayPhi->GetEntries()] != 0)
		    dataset << datacontainer[i*(variablesize)+j+entryarray->GetEntries()+entryarrayPhi->GetEntries()] << ",";
	    //extra first target variable
	    //"(Boson_Phi-recoilpatpfMETT1_Phi+TMath::Pi()) - 2.*TMath::Pi()*((Boson_Phi-recoilpatpfMETT1_Phi) > 0)",
	    if (datacontainer[i*(variablesize)+boson_Phi]-datacontainer[i*(variablesize)+recoilpatpfMETT1_Phi] > 0)
		dataset << datacontainer[i*(variablesize)+boson_Phi]-datacontainer[i*(variablesize)+recoilpatpfMETT1_Phi]-PI_F;
	    else
		dataset << datacontainer[i*(variablesize)+boson_Phi]-datacontainer[i*(variablesize)+recoilpatpfMETT1_Phi]+PI_F;
	    
	    dataset << ",";
	    //extra second target variable
	    //"-Boson_Pt/PhiCorrectedRecoil_LongZ",
	    dataset << (-datacontainer[i*(variablesize)+boson_Pt]/datacontainer[i*(variablesize)+entryarray->GetEntries()+PhiCorrectedRecoil_LongZ]);
	    
	    if (i != (inputTree1->GetEntries()-1))
	    {
		dataset << endl;
	    }
	    
	    if (i % 10000 == 0)
		cout << i << " Events processed" << endl;
	}
	
	
	
	/*
	float varlist[entryarray->GetEntries()];
	for (int j = 0; j < entryarray->GetEntries(); j++)
	    {
		inputTree1->SetBranchAddress(entryarray->At(j)->GetName(),&varlist[j]);
	    }
	
	int commacounter = 0;
	//for (int i = 0; i < 100; i++)
	int maxEntries = 0;
	if (inputTree1->GetEntries() > 1000000)
	    maxEntries = 1000000;
	else 
	    maxEntries = inputTree1->GetEntries();
	for (int i = 0; i < maxEntries; i++)
	{
	    inputTree1 -> GetEntry(i);
	    //depending on how many y variables there are, a comma should not be added for the last value in a row
	    commacounter = 0;
	    for (int j = 0; j < entryarray->GetEntries()-1; j++)
	    {
		//inputTree1->SetBranchAddress(entryarray->At(j)->GetName(),&testlist[]);
		//if inputargument is ydata 
		if (strcmp(entryarray->At(j)->GetName(),"genMet_Pt") == 0 || strcmp(entryarray->At(j)->GetName(),"genMet_Phi") == 0)
		{  
		    YTrainoutput <<  varlist[j] ;
		    //currently 2 variables in y
		    if (commacounter < 1)
			YTrainoutput << "," ;
		    commacounter++;
		}
		else
		    XTrainoutput <<  varlist[j] << "," ;
		
		//if (strcmp(entryarray->At(j)->GetName(),"recoilpatpfPUMETT1_Phi") == 0)
		  
		
		dataset << varlist[j] << ",";
		
	    }
	    
	    if (strcmp(entryarray->At(entryarray->GetEntries()-1)->GetName(),"genMet_Pt") == 0 || strcmp(entryarray->At(entryarray->GetEntries()-1)->GetName(),"genMet_Phi") == 0)
		YTrainoutput <<  varlist[entryarray->GetEntries()];
	    else
		XTrainoutput <<  varlist[entryarray->GetEntries()];
	    dataset << varlist[entryarray->GetEntries()];
	    
	    if (i != (inputTree1->GetEntries()-1))
	    {
		YTrainoutput << endl;
		XTrainoutput << endl;
		dataset << endl;
	    }
	}	
	    
	XTrainoutput.close();
	YTrainoutput.close();
	*/
	
	
	dataset.close();
	  
	return 0;
}
