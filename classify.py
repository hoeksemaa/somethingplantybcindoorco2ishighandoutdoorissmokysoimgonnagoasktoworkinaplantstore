import csv
import argparse
import pandas as pd
import math
import os

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--datafile", type=str, required=True, help="the name of the data file in this directory")
    parser.add_argument("-a", "--attributes", type=str, required=True, help="the name of the attributes file in this directory")
    args = vars(parser.parse_args())
    return args

def calculate_entropy(data):
    counts = data.value_counts()
    total = len(data)
    entropy = 0
    for count in counts:
        probability = count / total
        entropy -= probability * math.log2(probability)
    return entropy

def get_lowest_entropy_column(dataset):
    highest_entropy = 0
    highest_entropy_column = ""
    for column in dataset:
        score = calculate_entropy(dataset[column])
        if score > highest_entropy and column != "poisonous":
            highest_entropy = score
            highest_entropy_column = column
    return highest_entropy_column, highest_entropy

def load_attributes(args):
    attributes_dict = {}
    with open(args["attributes"], 'r') as file:
        for line in file:
            line = line.strip()
            class_name, attributes = line.split(":")
            attributes_dict[class_name] = {}
            attributes_list = attributes.split(",")
            for attribute in attributes_list:
                name, abbreviation = attribute.split("=")
                attributes_dict[class_name][abbreviation] = name
    return attributes_dict

def print_value_options(column, options, attr_dict):
    #print(column)
    #print(options)
    #print(attr_dict)
    string = ""
    for option in options:
        string += attr_dict[column][option]
        string += "(" + option + ") "
    print("your value options are:      {}".format(string))

def main():
    args = get_args()
    attributes = load_attributes(args)
    #print(attributes)
    df = pd.read_csv(args["datafile"])
    while len(df) > 1:
        os.system('cls' if os.name == 'nt' else 'clear')
        # recalculate entropy after every run
        column, entropy = get_lowest_entropy_column(df)
        options = df[column].unique()
        print("number datapoints remaining: {}".format(len(df)))
        print("maximum entropy measure:     {}".format(column))
        print("maximum entropy value:       {}".format(entropy))
        print_value_options(column, options, attributes)
        # prompt user for answer in category with highest entropy
        answer = input("what is the mushroom's {}?: ".format(column))
        df = df.loc[df[column] == answer]
    os.system('cls' if os.name == 'nt' else 'clear')
    #print(len(df))
    eatability = "edible" if df.at[0, "poisonous"] == "e" else "poisonous"
    print("given your answers, the mushroom is {}!".format(eatability))

if __name__ == "__main__":
    main()
