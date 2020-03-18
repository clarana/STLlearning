
from SignalTemporalLogic.STLFactory import STLFactory
import pandas as pd
import numpy as np
import re
from collections import OrderedDict

## Make functions

def readRulesFromFile(filepath, scorefilepath):
    negRules = []
    posRules = []
    allRules = []
    with open(filepath) as fp:  # read all rules from file
        line = fp.readline()
        while line:
            allRules.append(line)
            line = fp.readline()

    with open(scorefilepath) as fp:
        lineCount = 0
        line = fp.readline()
        while line:
            rule = (re.search('(.*) \[Discrimination Score:', line)).group(1)
            result = re.search('\[Discrimination Score:(.*)\n', line)
            r = result.group(1)
            p = (re.search('Percent Class \+ : (.*)]', r)).group(1)
            pos = (re.search('(.*);', p)).group(1)
            neg = (re.search('Percent Class - : (.*)', p)).group(1)

            if pos > neg:
                posRules.append(allRules[lineCount])
            else:
                negRules.append(allRules[lineCount])

            line = fp.readline()
            lineCount += 1

    return allRules, posRules, negRules


def getWordPairs(posRules, negRules):
    wordPairsPos = []
    for p in posRules:
        noTime = re.findall(r'([^[\]]+)(?:$|\[)', p)
        noTime = ' '.join([str(elem) for elem in noTime])
        nums = re.findall(r"[-+]?\d*\.\d+|\d+", noTime)
        nums = [float(i) for i in nums]
        st = re.sub('[^a-zA-Z]+', ' ', p)
        st = [i for i in st.split()]

        if 'G' in st:
            st = list(filter(lambda a: a != 'G', st))
        if 'F' in st:
            st = list(filter(lambda a: a != 'F', st))
        if 'U' in st:
            st = list(filter(lambda a: a != 'U', st))

        for w in range(len(st)):
            if "Change" in st[w]:
                if nums[w] >= 0:
                    st[w] += "+"

                else:
                    st[w] += "-"

        wordPairsPos.append(st)

    wordPairsNeg = []
    for p in negRules:
        noTime = re.findall(r'([^[\]]+)(?:$|\[)', p)
        noTime = ' '.join([str(elem) for elem in noTime])
        nums = re.findall(r"[-+]?\d*\.\d+|\d+", noTime)
        nums = [float(i) for i in nums]
        st = re.sub('[^a-zA-Z]+', ' ', p)
        st = [i for i in st.split()]

        if 'G' in st:
            st = list(filter(lambda a: a != 'G', st))
        if 'F' in st:
            st = list(filter(lambda a: a != 'F', st))
        if 'U' in st:
            st = list(filter(lambda a: a != 'U', st))

        for w in range(len(st)):
            if "Change" in st[w]:
                if nums[w] >= 0:
                    st[w] += "+"

                else:
                    st[w] += "-"

        wordPairsNeg.append(st)

    return wordPairsPos, wordPairsNeg


def getOccDataframe(wordPairsPos, wordPairsNeg, names):
    occurrences = OrderedDict((name, OrderedDict((name, 0) for name in names)) for name in names)

    # Find the co-occurrences:
    for l in wordPairsPos:
        for i in range(len(l)):
            for item in l[:i] + l[i + 1:]:
                occurrences[l[i]][item] += 1

    dfPos = pd.DataFrame(occurrences, columns=occurrences.keys())

    occurrences = OrderedDict((name, OrderedDict((name, 0) for name in names)) for name in names)
    # Find the co-occurrences:
    for l in wordPairsNeg:
        for i in range(len(l)):
            for item in l[:i] + l[i + 1:]:
                occurrences[l[i]][item] += 1

    dfNeg = pd.DataFrame(occurrences, columns=occurrences.keys())

    return dfPos, dfNeg



def main():

    names = ['HEM', 'PLA', 'HEC', 'WBC', 'SOD', 'POT', 'BUN', 'CRT', 'ALT', 'TOTP',
             'ALB', 'TALB', 'DIN', 'DOB', 'DOP', 'MIL', 'NIG', 'DIGX', 'ACE', 'BET',
             'ANGIOT', 'Walk', 'VO', 'RAP', 'PAS', 'PAD', 'PCWP', 'PCPWMN', 'CI',
             'BPSYS', 'BPDIAS', 'HR', 'RAPChange+', 'RAPChange-', 'PASChange+', 'PASChange-', 'PADChange+',
             'PADChange-',
             'PCWPChange+', 'PCWPChange-', 'PCPWMNChange+', 'PCPWMNChange-', 'CIChange+', 'CIChange-', 'BPSYSChange+',
             'BPSYSChange-', 'BPDIASChange+', 'BPDIASChange-', 'HRChange+', 'HRChange-']

    # Load all rules Death
    allRulesD = []
    posRulesD = []
    negRulesD = []

    for i in range(0, 11):
        filepath1 = "MCR/Rules/1.AbsoluteChanges/Death/CardChangesRuleDeath" + str(i) + ".txt"
        filepath2 = "MCR/Rules/1.AbsoluteChanges/Death/CardChangesRuleScoresDeath" + str(i) + ".txt"
        a, p, n = readRulesFromFile(filepath1, filepath2)
        allRulesD.extend(a)
        posRulesD.extend(p)
        negRulesD.extend(n)

    # Load all rules Rehosp
    allRulesR = []
    posRulesR = []
    negRulesR = []

    for i in range(0, 11):
        filepath1 = "MCR/Rules/1.AbsoluteChanges/Death+Rehosp/CardChangesRuleRehosp" + str(i) + ".txt"
        filepath2 = "MCR/Rules/1.AbsoluteChanges/Death+Rehosp/CardChangesRuleScoresRehosp" + str(i) + ".txt"
        a, p, n = readRulesFromFile(filepath1, filepath2)
        allRulesR.extend(a)
        posRulesR.extend(p)
        negRulesR.extend(n)


    # Load Data
    absData = pd.read_csv('MCR/AbsChanges.csv', index_col=0)
    absDataLabelsD = pd.read_csv('MCR/AbsChangesDeathLabels.csv', index_col=0)
    absDataLabelsR = pd.read_csv('MCR/AbsChangesRehospLabels.csv', index_col=0)

    factory = STLFactory()
    indexes = sorted(set(absData.index))
    totalPatients = len(indexes)

    # mcrList = []
    #
    # #Death, Positive Rules MCR
    # for p in posRulesD:
    #     print(p, end='')
    #
    #     ft = factory.constructFormulaTree(p)
    #
    #     TP = 0
    #     TN = 0
    #     FP = 0
    #     FN = 0
    #
    #     for i in indexes:
    #         data = absData.loc[i]
    #         label = absDataLabelsD.loc[i].values[0]
    #
    #         val = ft.evaluateTruthValue(data)
    #
    #         if label == 1 and val == True:
    #             TP += 1
    #         elif label == -1 and val == False:
    #             TN += 1
    #         elif label == 1 and val == False:
    #             FN += 1
    #         else: #label == -1 and val == True
    #             FP += 1
    #
    #     trueCount = TP + TN
    #     falseCount  = FP + FN
    #     accuracy = (TP + TN) / totalPatients
    #     MCR = 1 - accuracy
    #
    #     print("TP", trueCount, "False Count", falseCount, "Accuracy", accuracy, "MCR", MCR, "\n")
    #
    #     mcrList.append([p, TP, TN, FP, FN, accuracy, MCR])
    #
    # #print(mcrList)
    # print(len(mcrList))
    #
    # mcrDF = pd.DataFrame(mcrList, columns=['Rule', 'TP', 'TN', 'FP', 'FN', 'Accuracy', 'MCR'])
    # print(mcrDF)
    # mcrDF.to_csv('AbsChgDeathPositiveMCR.csv', index=False)


    # mcrList = []
    # #Death, Negative Rules MCR
    # for p in negRulesD:
    #     print(p, end='')
    #
    #     ft = factory.constructFormulaTree(p)
    #
    #     TP = 0
    #     TN = 0
    #     FP = 0
    #     FN = 0
    #
    #     for i in indexes:
    #         data = absData.loc[i]
    #         label = absDataLabelsD.loc[i].values[0]
    #
    #         val = ft.evaluateTruthValue(data)
    #
    #         if label == -1 and val == True:
    #             TP += 1
    #         elif label == 1 and val == False:
    #             TN += 1
    #         elif label == -1 and val == False:
    #             FN += 1
    #         else: #label == 1 and val == True
    #             FP += 1
    #
    #     trueCount = TP + TN
    #     falseCount  = FP + FN
    #     accuracy = (TP + TN) / totalPatients
    #     MCR = 1 - accuracy
    #
    #     print("TP", trueCount, "False Count", falseCount, "Accuracy", accuracy, "MCR", MCR, "\n")
    #
    #     mcrList.append([p, TP, TN, FP, FN, accuracy, MCR])
    #
    # #print(mcrList)
    # print(len(mcrList))
    #
    # mcrDF = pd.DataFrame(mcrList, columns=['Rule', 'TP', 'TN', 'FP', 'FN', 'Accuracy', 'MCR'])
    # print(mcrDF)
    # mcrDF.to_csv('AbsChgDeathNegativeMCR.csv', index=False)


###################################################################################################################

    # mcrList = []
    #
    # #Rehosp, Positive Rules MCR
    # for p in posRulesR:
    #     print(p, end='')
    #
    #     ft = factory.constructFormulaTree(p)
    #
    #     TP = 0
    #     TN = 0
    #     FP = 0
    #     FN = 0
    #
    #     for i in indexes:
    #         data = absData.loc[i]
    #         label = absDataLabelsD.loc[i].values[0]
    #
    #         val = ft.evaluateTruthValue(data)
    #
    #         if label == 1 and val == True:
    #             TP += 1
    #         elif label == -1 and val == False:
    #             TN += 1
    #         elif label == 1 and val == False:
    #             FN += 1
    #         else: #label == -1 and val == True
    #             FP += 1
    #
    #     trueCount = TP + TN
    #     falseCount  = FP + FN
    #     accuracy = (TP + TN) / totalPatients
    #     MCR = 1 - accuracy
    #
    #     print("TP", trueCount, "False Count", falseCount, "Accuracy", accuracy, "MCR", MCR, "\n")
    #
    #     mcrList.append([p, TP, TN, FP, FN, accuracy, MCR])
    #
    # #print(mcrList)
    # print(len(mcrList))
    #
    # mcrDF = pd.DataFrame(mcrList, columns=['Rule', 'TP', 'TN', 'FP', 'FN', 'Accuracy', 'MCR'])
    # print(mcrDF)
    # mcrDF.to_csv('AbsChgRehospPositiveMCR.csv', index=False)




    mcrList = []
    #Rehosp, Negative Rules MCR
    for p in negRulesR:
        print(p, end='')

        ft = factory.constructFormulaTree(p)

        TP = 0
        TN = 0
        FP = 0
        FN = 0

        for i in indexes:
            data = absData.loc[i]
            label = absDataLabelsD.loc[i].values[0]

            val = ft.evaluateTruthValue(data)

            if label == -1 and val == True:
                TP += 1
            elif label == 1 and val == False:
                TN += 1
            elif label == -1 and val == False:
                FN += 1
            else: #label == 1 and val == True
                FP += 1

        trueCount = TP + TN
        falseCount  = FP + FN
        accuracy = (TP + TN) / totalPatients
        MCR = 1 - accuracy

        print("TP", trueCount, "False Count", falseCount, "Accuracy", accuracy, "MCR", MCR, "\n")

        mcrList.append([p, TP, TN, FP, FN, accuracy, MCR])

    #print(mcrList)
    print(len(mcrList))

    mcrDF = pd.DataFrame(mcrList, columns=['Rule', 'TP', 'TN', 'FP', 'FN', 'Accuracy', 'MCR'])
    print(mcrDF)
    mcrDF.to_csv('AbsChgRehospNegativeMCR.csv', index=False)


if __name__ == '__main__':
    main()


