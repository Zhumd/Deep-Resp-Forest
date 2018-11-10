
# -*- coding: utf-8 -*-

import itertools

import numpy as np

import pandas as pd
import matplotlib.pyplot as plt

import random

import sklearn.metrics as metrics

from sklearn.datasets import load_iris

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


from GCForest import gcForest

####ROC
from sklearn.preprocessing import label_binarize
from sklearn.metrics import roc_curve, auc
from itertools import cycle

from sklearn import svm
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import colors
from sklearn.model_selection import train_test_split
def plot_confusion_matrix(cm, classes, normalize=False,

                          title='Confusion matrix', cmap=plt.cm.Blues):

    plt.imshow(cm, interpolation='nearest', cmap=cmap)

    plt.title(title)

    plt.colorbar()

    tick_marks = np.arange(len(classes))

    plt.xticks(tick_marks, classes, rotation=45)

    plt.yticks(tick_marks, classes)



    if normalize:

        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

        print("Normalized confusion matrix")

    else:

        print('Confusion matrix, without normalization')



    thresh = cm.max() / 2.

    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):

        plt.text(j, i, cm[i, j],

                 horizontalalignment="center",

                 color="white" if cm[i, j] > thresh else "black")



    plt.tight_layout()

    plt.ylabel('True label')

    plt.xlabel('Predicted label')

    plt.show()





def gcf(X_train, X_test, y_train, y_test, cnames):



    clf = gcForest(shape_1X=(1, 18988),window=[1000,2000],stride=10)

    clf.fit(X_train, y_train)



    y_pred = clf.predict(X_test)
    print(y_pred)




   # print('accuracy:', metrics.accuracy_score(y_test, y_pred))

    #print('kappa:', metrics.cohen_kappa_score(y_test, y_pred))

    #print(metrics.classification_report(y_test, y_pred, target_names=cnames))



    #cnf_matrix = metrics.confusion_matrix(y_test, y_pred)

    #plot_confusion_matrix(cnf_matrix, classes=cnames, normalize=True,

    #                  title='Normalized confusion matrix')
def numeric(target):
    target = pd.to_numeric(target)
    return target
def normalize01(target):
    target = pd.to_numeric(target)
    # print(target)
    target_min = target.min()
    target_max = target.max()


    target_normal = (target-target_min)/(target_max-target_min)
    # print("min:",target_normal.min())
    # print("max:",target_normal.max())
    # print("target_normal:",target_normal)
    return target_normal
def normalize(target):
    #z-score 标准化
    # print(target)
    mean = target.mean()
    std = target.std()
    # print("mean:",mean," std:",std)
    target_normal = (target-mean)/std
    # print("target_normal:",target_normal)
    # print("mean:",target_normal.mean())
    # print("std:",target_normal.std())
    return target_normal
###1:resistant 0:sensitive 2:none
def labeldata(drugdata,target_name):
    # print(drugdata.shape)
    label_y= pd.Series(range(0,drugdata.shape[0]))
    # print(label_y)
    for i in range(0,drugdata.shape[0]):
      if drugdata[target_name][i] >0.8:
          label_y[i] = 1
      elif drugdata[target_name][i] <-0.8:
          label_y[i] = 0
      else:
          label_y[i] = 2
    # print(label_y)
    drugdata["label_y"] = label_y
    return drugdata

def show_accuracy(y_hat, y_test, param):
    pass


if __name__ == '__main__':
    ########################################drug response part#################################################
    # read drug response file
    cgp_drugdata = pd.DataFrame(pd.read_csv('drug.csv'))

    # print(cgp_drugdata.columns)
    cgp_drugdata.info()
    # normalize ic50
    ic50 = cgp_drugdata["LN_IC50"]
    # print(type(ic50))
    ic50_normal = normalize(ic50)
    cgp_drugdata["ic50_normal"]=ic50_normal



    # label (sensitive or resistant)according to ic50_normal
    cgp_drugdata = labeldata(cgp_drugdata,"ic50_normal")


    # order ccle_drugdata by ic50_normal
    cgp_drugdata=cgp_drugdata.sort_values(by="ic50_normal", ascending=False)
    # cgp_drugdata["ic50_normal"].plot(kind="bar")
    # plt.show()
    #
    # output
    # cgp_drugdata.to_csv('cgp_drugdata.csv')
    #



    ########################################gene exprSet part#################################################
    # read gene exprset file
    L=[]
    file=open("gene.txt","r")
    line=file.readline()
    while line:
        line=line.split()
        L.append(line)
        line=file.readline()
    cgp_exprSet = pd.DataFrame(L)

    cgp_exprSet2=cgp_exprSet.T
    # print(cgp_exprSet2)
    cgp_exprSet3 = cgp_exprSet2.drop([0]).reset_index(drop=True)
    cgp_exprSet3.columns=cgp_exprSet2.iloc[0,:].tolist()
    # print(cgp_exprSet3)
    # cgp_exprSet3.to_csv('cgp_exprSet3.csv')
    cgp_exprSet4 = pd.DataFrame(index=cgp_exprSet3.index)
    cgp_exprSet4[cgp_exprSet3.columns[0]]=cgp_exprSet3.iloc[:,0]
    for i in range(1,17738):
        each_column = cgp_exprSet3[cgp_exprSet3.columns[i]]
        cgp_exprSet4[cgp_exprSet3.columns[i]] = normalize01(each_column)
    # print(cgp_exprSet4)
    cgp_exprSet4.info()
    # cgp_exprSet4.to_csv('cgp_exprSet4.csv')






    ########################################copy number part#################################################
    # read copy number file
    L=[]
    file=open("cna.txt","r")
    line=file.readline()
    while line:
        line=line.split()
        L.append(line)
        line=file.readline()
    cgp_cnaSet = pd.DataFrame(L)
    cgp_cnaSet2 = cgp_cnaSet.drop([0]).reset_index(drop=True)
    cgp_cnaSet2.columns=cgp_cnaSet.iloc[0,:].tolist()
    # print(cgp_cnaSet2)
    # cgp_cnaSet2.info()
    cgp_cnaSet3 = pd.DataFrame(index=cgp_cnaSet2.index)
    cgp_cnaSet3[cgp_cnaSet2.columns[0]]=cgp_cnaSet2.iloc[:,0]
    for i in range(1,426):
        each_column = cgp_cnaSet2[cgp_cnaSet2.columns[i]]
        cgp_cnaSet3[cgp_cnaSet2.columns[i]] = numeric(each_column)
    cgp_cnaSet3.info()
    # cgp_cnaSet3.to_csv('cgp_cnaSet3.csv')









    ######################generate x and y for each drug####################
    drugs = []
    for i in cgp_drugdata["DRUG_ID"].tolist():
      if i not in drugs:
        drugs.append(i)
    print("drugs:",drugs)
    cgp_exprSet4.rename(columns={"ensembl_gene":"COSMIC_ID"},inplace=True)##inplace=True表示在原数据上进行操作
    cgp_cnaSet3.rename(columns={"Name":"COSMIC_ID"},inplace=True)
    exprCName = cgp_exprSet4["COSMIC_ID"]
    # print(list(exprCName))
    cnaCName = cgp_cnaSet3["COSMIC_ID"]
    # print(list(cnaCName))
    conCName = [val for val in list(exprCName) if val in list(cnaCName)]
    conCName.remove("905954")
    conCName.remove("905954")
    conCName.remove("909976")
    conCName.remove("909976")
    conCName.remove("1330983")
    conCName.remove("1330983")
    conCName.remove("1503362")
    conCName.remove("1503362")
    print("con-cellline:",list(conCName))
    # pd.DataFrame(list(conCName)).to_csv("conCName.csv")
    i=8
    drug=drugs[i]
    print(drug)
    each_drugdata = pd.DataFrame(cgp_drugdata[cgp_drugdata["DRUG_ID"]==drugs[i]])
    # each_drugdata.to_csv('each_drugdata.csv')
    print(each_drugdata)


    ######~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~gene part~~~~~~~~~~~~~~~~~~~~~~~~~####################
    cgp_exprSet4['COSMIC_ID'] = pd.to_numeric(cgp_exprSet4['COSMIC_ID'])
    cgp_exprSet5 = cgp_exprSet4[cgp_exprSet4['COSMIC_ID'].isin(list(conCName))]
    # cgp_exprSet5["COSMIC_ID"].to_csv("cgp_exprSet5.csv")

    each_data = pd.merge(each_drugdata,cgp_exprSet5,on="COSMIC_ID",how="inner")
    # each_data.to_csv('1_each_data.csv')
    ###########################################test gcForest######################################33
    random.seed(5)
    randomCols = random.sample(range(10,17747),400)
    x = each_data.iloc[:,randomCols]
    y = each_data.iloc[:,9]
    x.index=each_data["COSMIC_ID"]
    y.index=each_data["COSMIC_ID"]
    x.sort_index()
    y.sort_index()
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2,random_state=5)
    X_train.to_csv("X_train_svm.csv")
    y_train.to_csv("y_train_svm.csv")
    # X_test.to_csv(str(drug)+"_X_test_expr.csv")
    # y_test.to_csv(str(drug)+"_y_test_expr.csv")
    train_cellline = X_train.index
    print("train_cellline:",train_cellline)
    test_cellline = X_test.index
    print("test_cellline:",test_cellline)


    cgp_cnaSet3['COSMIC_ID'] = pd.to_numeric(cgp_cnaSet3['COSMIC_ID'])
    cgp_cnaSet4 = cgp_cnaSet3[cgp_cnaSet3['COSMIC_ID'].isin(list(conCName))]
    # cgp_cnaSet4["COSMIC_ID"].to_csv("cgp_cnaSet4.csv")
    each_cna_data = pd.merge(each_drugdata,cgp_cnaSet4,on="COSMIC_ID",how="inner")
    # each_cna_data.to_csv('1_each_cna_data.csv')
    #
        ###########################################test gcForest######################################33
    random.seed(5)
    randomCols = random.sample(range(10,435),400)
    x_cna = each_cna_data.iloc[:,randomCols]
    y_cna = each_cna_data.iloc[:,9]
    x_cna.index=each_cna_data["COSMIC_ID"]
    y_cna.index=each_cna_data["COSMIC_ID"]
    x_cna.sort_index()
    y_cna.sort_index()
    X_train_cna, X_test_cna, y_train_cna, y_test_cna = train_test_split(x_cna, y_cna, test_size=0.2,random_state=5)
    X_train_cna.to_csv("X_train_cna_svm.csv")
    y_train_cna.to_csv("y_train_cna_svm.csv")







    #########################svm#####################3
    print("X_train:",np.array(X_train))
    print("X_train_cna:",np.array(X_train_cna))
    each_X = pd.merge(X_train,X_train_cna,on="COSMIC_ID",how="inner")
    each_X.to_csv("each_X.csv")
    y_train.to_csv("each_Y.csv")
    clf = svm.SVC(C=0.8, kernel='rbf', gamma=20, decision_function_shape='ovr')
    clf.fit(np.array(each_X), np.array(y_train))
    print(clf.score(np.array(each_X), np.array(y_train)))  # 精度
    y_hat = clf.predict(np.array(each_X))
    prediction_accuracy = accuracy_score(y_true=y_train, y_pred=y_hat)
    print('Layer validation accuracy = {}'.format(prediction_accuracy))
    each_X_test = pd.merge(X_test,X_test_cna,on="COSMIC_ID",how="inner")
    y_hat = clf.predict(np.array(each_X_test))
    prediction_accuracy = accuracy_score(y_true=y_test, y_pred=y_hat)
    print('Layer validation accuracy = {}'.format(prediction_accuracy))
