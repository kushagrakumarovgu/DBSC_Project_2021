package ca.pfv.spmf.test;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.net.URL;

import ca.pfv.spmf.algorithmmanager.descriptions.DescriptionAlgoRPGrowthAssociationRules;
import ca.pfv.spmf.algorithms.frequentpatterns.rpgrowth.AlgoRPGrowth;
import ca.pfv.spmf.patterns.itemset_array_integers_with_count.Itemsets;

/**
 * Example of how to use the RPGrowth from the source code
 * @author Ryan Benton and Blake Johns
 */

public class MainTestRPGrowth_saveToMemory {
	public static void main(String[] arg) throws FileNotFoundException, IOException{
		//load the transaction database
		
		// Set the path to the dataset.
		
		String myinput = "E:\\New_Begninning\\DBSC_Project\\datasets\\kosarak.txt";
		
		//threshold range [minimum rare (min) and minimum support (max)]
		double minsup = 0.01; //0.5;
		double minraresup = 0.001; //0.2;
		
		//Apply the RPGrowth algorithm
		AlgoRPGrowth algo = new AlgoRPGrowth();
		
		System.out.println(System.getProperty("java.runtime.version"));
		
		// Uncomment the following line to set the maximum pattern length (number of items per itemset, e.g. 3 )
	    //algo.setMaximumPatternLength(4);
		
		// Uncomment the following line to set the maximum pattern length (number of items per itemset, e.g. 2 )
		//algo.setMinimumPatternLength(2);
		
		//Run the algo
		//NOTE that here we use "null" as the output file path because we are saving to memory
		Itemsets patterns = algo.runAlgorithm(myinput,null, minsup, minraresup);
		algo.printStats();
		
		//patterns.printItemsets(algo.getDatabaseSize());
		
		// Kushagra: Generate Association Rules.
		DescriptionAlgoRPGrowthAssociationRules ivAssoRules = new DescriptionAlgoRPGrowthAssociationRules();
		// minsup , minraresup , minconf , Anticident len , consequent len.	 
		String[] params = {"0.03","0.01","0.8"};
		// set path of the output file.
		String output = 
		"E:\\New_Begninning\\DBSC_Project\\python-spmf\\input_files\\kosarak\\Associationrules_kosarak_03_01.txt";
		ivAssoRules.runAlgorithm(params,myinput,output); 
		
		System.out.println("--End of Execution--");
	}
	public static String fileToPath(String filename) throws UnsupportedEncodingException{
		URL url = MainTestFPGrowth_saveToMemory.class.getResource(filename);
		 return java.net.URLDecoder.decode(url.getPath(),"UTF-8");
	}
}
