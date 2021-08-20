"""
Python version used: 3.8.3
This program randomly choose a single association rule out of many
and computes the statistical measure for it.
Inputs: a. Path to the actual dataset.
        b. Path to the processed association rule in CSV format.

Output: Statistical measure for a randomly choosen single association rule.

How to run: python sampling_statistical_measure.py
"""

import pandas as pd
import sys
from math import sqrt

consq_dict = {}


# Read the dataset and returns lines and total number of entries.
def read_dataset(filename):
    with open(filename, "r+") as FH:
        lines = FH.readlines()
    return lines, len(lines)


# Computes Antecedent Support
def ant_support(supp, conf):
    return supp / conf


# Wrapper function that apilies ant_support function to all the rows.
def cal_ant_support(df):
    df["Antecedent_Support"] = df.apply(
        lambda row: ant_support(row["Support"], row["Confidence"]),
        axis=1,
    )
    return df


# Calculate Individual Support (Consiquent Support to be precise)
def cal_individual_supp(ant_or_conseq, lines, name):
    list_ant_supp = list()
    global consq_dict

    for ele in ant_or_conseq:
        count = 0
        is_present = False
        ele = ele.strip("}")
        ele = ele.strip("{")
        ele = ele.split(",")

        ele = [int(x.strip()) for x in ele]
        ele_len = len(ele)
        # Donot compute the count of the occurance of consiquent if it is
        # already previously computed and just lookup from the dictionary.
        if (ele_len == 1) and (ele[0] in consq_dict):
            count = consq_dict[ele[0]]
        else:
            for line in lines:
                line = line.strip("\n")
                line = set(map(int, line.split()))

                check = set(ele).issubset(line)
                if check:
                    count += 1

            # Store the count value, so we don't have to compute it again.
            if ele_len == 1:
                consq_dict[ele[0]] = count

        list_ant_supp.append(count)

    # Normalize the values of the consiquent support.
    df[name] = [x / len(lines) for x in list_ant_supp]
    return df


# Normalize the support values.
def normalize_support(df, len_dataset):
    df.Support = df.Support / len_dataset
    return df


# Calculate the individual lift values
def cal_lift(supp, ant_supp, con_supp):
    return supp / (ant_supp * con_supp)


# Calculate the individual All confidence values
def cal_allconf(supp, ant_supp, con_supp):
    return supp / max(ant_supp, con_supp)


# Calculate the individual Max Confidence values
def cal_maxconf(supp, ant_supp, con_supp):
    return max(supp / ant_supp, supp / con_supp)


# Calculate the individual Coherence values
def cal_coherence(supp, ant_supp, con_supp):
    return supp / (ant_supp + con_supp - supp)


# Calculate the individual cosine values
def cal_cosine(supp, ant_supp, con_supp):
    return supp / sqrt(ant_supp * con_supp)


# Calculate the individual kulc values
def cal_kulc(supp, ant_supp, con_supp):
    return supp / 2 * ((1 / ant_supp) + (1 / con_supp))


# Computes the all the statistical measures for entire dataset.
def cal_statistics(df):
    df["Lift"] = df.apply(
        lambda row: cal_lift(
            row["Support"], row["Antecedent_Support"], row["Consiquent_Support"]
        ),
        axis=1,
    )

    df["AllConf"] = df.apply(
        lambda row: cal_allconf(
            row["Support"], row["Antecedent_Support"], row["Consiquent_Support"]
        ),
        axis=1,
    )

    df["MaxConf"] = df.apply(
        lambda row: cal_maxconf(
            row["Support"], row["Antecedent_Support"], row["Consiquent_Support"]
        ),
        axis=1,
    )

    df["Coherence"] = df.apply(
        lambda row: cal_coherence(
            row["Support"], row["Antecedent_Support"], row["Consiquent_Support"]
        ),
        axis=1,
    )

    df["Cosine"] = df.apply(
        lambda row: cal_cosine(
            row["Support"], row["Antecedent_Support"], row["Consiquent_Support"]
        ),
        axis=1,
    )

    df["Kulc"] = df.apply(
        lambda row: cal_kulc(
            row["Support"], row["Antecedent_Support"], row["Consiquent_Support"]
        ),
        axis=1,
    )
    return df


if __name__ == "__main__":

    """
    Please provide the path of the dataset to read_dataset method(line 143)
    for which you would like to run this program.
    """
    dataset, len_dataset = read_dataset(
        "E:\\New_Begninning\\DBSC_Project\\datasets\\tae_format.txt"
    )
    """
    Please provide the path to the CSV file that contains the processed association rules
    and their corresponding support and confidence values.
    NOTE: Incase if you don't have the CSV file, Please first run the process_asso_rules.py
    The output of the process_asso_rules.py is the input that you should give here i.e.
    at line number 177.
    """
    df = pd.read_csv("output_files/tae/asso_rule_tae_15_05.csv")
    # Sample a single association rule.
    df = df.sample()
    print(f"Sampled association rule")
    print(df)
    df = normalize_support(df, len(dataset))

    df = cal_ant_support(df)
    df = cal_individual_supp(df.Consiquent, dataset, "Consiquent_Support")

    df = cal_statistics(df)

    print(df.head())
    print(
        f"ant={df['Antecedent'].values[0]} consq={df['Consiquent'].values[0]} supp={df['Support'].values[0].round(4)} conf={df['Confidence'].values[0].round(4)}"
    )
    print(
        f"allconf={df['AllConf'].values[0].round(4)} maxconf={df['MaxConf'].values[0].round(4)} coherence={df['Coherence'].values[0].round(4)} Cosine={df['Cosine'].values[0].round(4)} Kulc={df['Kulc'].values[0].round(4)} Lift={df['Lift'].values[0].round(4)}"
    )
