# DBSC_Project_2021
## A RP-growth method for discovering interesting Infrequent Patterns.

Steps to Execute the Project:
  1. Download and install the open source spmf java project from https://www.philippe-fournier-viger.com/spmf/index.php?link=download.php.
  2. Replace the src/ca/pfv/spmf/test/MainTestRPGrowth_saveToMemory.java file with spmf_Java/MainTestRPGrowth_saveToMemory.java project file.
  3. Generate the association rules for different datasets by modifying the minsup and minrare sup in MainTestRPGrowth_saveToMemory.java
  4. Run process_asso_rules.py to convert the output of the java program to CSV format.
  5. Run statistical_measure.py to generate the statistical measures and overall average of each statistical measure.
  6. Run sampling_statistical_measure.py to generate statistical measures from a random association rule.

## Longest sequence generation.
  seq_dict.py is an independent program to extract longest sequences from the pattern geneated by spmf java code.

## Negative Tree:
  Negative_Tree.ipynb is partial implmentaion of the paper Efficient Infrequent Pattern Mining Using Negative Itemset 
  by Tree Yifeng Lu, Florian Richter and Thomas Seid
  
