"""
Python version used: 3.8.3
This program computes the antecdent and consiquent support, statistical
measure for all the association rules and also provide average of each 
statistical measures seprately.

Inputs: a. Path to the actual dataset.
        b. Path to the processed association rule in CSV format.

Output: a. Antecdent and consiquent support for each association rule in the
        CSV format.
        b. Statistical measures for each association rule in the
        CSV format.
        c. Average of each statistical measure on the terminal.

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
    Please provide the path of the dataset to read_dataset method(line 158)
    for which you would like to run this program.
    """
    dataset, len_dataset = read_dataset(
        "E:\\New_Begninning\\DBSC_Project\\datasets\\kosarak.txt"
    )

    """
    Please provide the path to the CSV file that contains the processed association rules
    and their corresponding support and confidence values.
    NOTE: Incase if you don't have the CSV file, Please first run the process_asso_rules.py
    The output of the process_asso_rules.py is the input that you should give here i.e.
    at line number 181.
    """
    df = pd.read_csv("output_files/kosarak/asso_rule_kosarak_01_002.csv")
    df = normalize_support(df, len(dataset))

    df = cal_ant_support(df)
    print(df.head())
    df = cal_individual_supp(df.Consiquent, dataset, "Consiquent_Support")

    """
    Please provide the path where would like to store the antecent and consiquent support
    for each association in CSV format. This one of the output of this program.
    """

    df.to_csv("output_files/kosarak/kosarak_01_002.csv", index=False)

    # Provide the same path that you gave in line 194 to line 197
    df = pd.read_csv("output_files/kosarak/kosarak_01_002.csv", index_col=[0])
    df = cal_statistics(df)
    print(df.head())
    """
    Please provide the path where would like to store the all the computed statistical
    measure for each association in CSV format. This one of the output of this program.
    """
    df.to_csv("output_files/kosarak/kosarak_stats_measure_01_002_testing.csv")

    cols = [
        "Support",
        "Confidence",
        "AllConf",
        "MaxConf",
        "Coherence",
        "Cosine",
        "Kulc",
        "Lift",
    ]
    supp, conf, all_conf, max_conf, coherence, Cosine, Kulc, Lift = (
        df[cols].mean().round(4)
    )
    print("-" * 39)
    print(
        f"{supp=} {conf=} {all_conf=} {max_conf=} {coherence=} {Cosine=} {Kulc=} {Lift=}"
    )
