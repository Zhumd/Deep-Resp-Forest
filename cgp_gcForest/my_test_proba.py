
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


def ten_fold(n):
    L=[]
    np.random.seed(5)
    numbers = np.random.permutation(range(n))
    print(numbers)
    a1 = numbers[0:round(n/10)]
    L.append(a1)
    a2 = numbers[round(n/10):2*round(n/10)]
    L.append(a2)
    a3 = numbers[2*round(n/10):3*round(n/10)]
    L.append(a3)
    a4 = numbers[3*round(n/10):4*round(n/10)]
    L.append(a4)
    a5 = numbers[4*round(n/10):5*round(n/10)]
    L.append(a5)
    a6 = numbers[5*round(n/10):6*round(n/10)]
    L.append(a6)
    a7 = numbers[6*round(n/10):7*round(n/10)]
    L.append(a7)
    a8 = numbers[7*round(n/10):8*round(n/10)]
    L.append(a8)
    a9 = numbers[8*round(n/10):9*round(n/10)]
    L.append(a9)
    a10 = numbers[9*round(n/10):]
    L.append(a1)
    return L



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
    # print(drugs)
    #####choose the same celllines in both gene and cna
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
    pd.DataFrame(list(conCName)).to_csv("conCName.csv")
    for i in range(12,16):
        drug=drugs[i]
        each_drugdata = pd.DataFrame(cgp_drugdata[cgp_drugdata["DRUG_ID"]==drugs[i]])
        # each_drugdata.to_csv('each_drugdata.csv')
        # print(each_drugdata)


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
        print(x)
        X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2,random_state=5)

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
        print(x_cna)

        X_train_cna, X_test_cna, y_train_cna, y_test_cna = train_test_split(x_cna, y_cna, test_size=0.2,random_state=5)
        # for j in range(1):
        #     X_test = x.iloc[folds_expr[j],:]
        #     y_test = y.iloc[folds_expr[j]]
        #     X_train = x.iloc[list(set(range(x.shape[0])).difference(set(folds_expr[j]))),:]
        #     y_train = y.iloc[list(set(range(x.shape[0])).difference(set(folds_expr[j])))]
        #     X_train.to_csv(str(drug)+"X_train_expr.csv")
        #     y_train.to_csv(str(drug)+"y_train_expr.csv")
        # X_test.to_csv(str(drug)+"_X_test_expr.csv")
        # y_test.to_csv(str(drug)+"_y_test_expr.csv")
        train_cellline = X_train.index
        # print("train_cellline:",train_cellline)
        test_cellline = X_test.index
        # print("test_cellline:",test_cellline)
        # #
        # #
        levels = np.unique(np.array(y_train))
        # print("levels:",levels)
        File = open("test"+str(drug)+".txt", "w")
        File.write("levels:"+str(levels)+"\n")
        clf = gcForest(shape_1X=(1, 400),window=[100,200],stride=2,levels=levels,f=File)
        if np.shape(X_train)[0] != len(y_train):
                raise ValueError('Sizes of y and X do not match.')
        expr_mgs_X = clf.mg_scanning(np.array(X_train), np.array(y_train))
        expr_mgs_X_test = clf.mg_scanning(np.array(X_test))

        # # gcf(np.array(X_train), np.array(X_test), np.array(y_train), np.array(y_test), cnames)
        # pd.DataFrame(expr_mgs_X).to_csv("expr_mgs_X.csv")





        # X_test_cna.to_csv(str(drug)+"_X_test_cna.csv")
        # y_test_cna.to_csv(str(drug)+"_y_test_cna.csv")



        # #
        # #
        clf = gcForest(shape_1X=(1, 400),window=[100,200],stride=2,levels=levels,f=File)
        if np.shape(X_train_cna)[0] != len(y_train_cna):
            raise ValueError('Sizes of y and X do not match.')
        cna_mgs_X = clf.mg_scanning(np.array(X_train_cna), np.array(y_train_cna))

        # print(cna_mgs_X)
        # pd.DataFrame(cna_mgs_X).to_csv("cna_mgs_X.csv")
        mgs_X = np.concatenate((expr_mgs_X,cna_mgs_X),axis=1)
        pd.DataFrame(mgs_X).to_csv("mgs_X.csv")
        # pd.DataFrame(mgs_X).to_csv("mgs_X.csv")
        train_predict_y = clf.cascade_forest(mgs_X, np.array(y_train_cna))




        ######do on the testset########
        cna_mgs_X_test = clf.mg_scanning(np.array(X_test_cna))
        mgs_X_test = np.concatenate((expr_mgs_X_test,cna_mgs_X_test),axis=1)
        pd.DataFrame(mgs_X_test).to_csv("mgs_X_test.csv")
        # pd.DataFrame(mgs_X_test).to_csv("mgs_X_test.csv")
        cascade_all_pred_prob = clf.cascade_forest(mgs_X_test)
        predict_proba = np.mean(cascade_all_pred_prob, axis=0)
        pd.DataFrame(predict_proba).to_csv(str(drug)+"_predict_proba.csv")
        predictions = levels[np.argmax(predict_proba, axis=1)]
        # pd.DataFrame(predictions).to_csv(str(drug)+"_predictions.csv")
        print("prediction:",predictions)
        prediction_accuracy = accuracy_score(y_true=y_test, y_pred=predictions)
        print('Layer validation accuracy = {}'.format(prediction_accuracy))
        File.write('Layer validation accuracy = {}'.format(prediction_accuracy)+"\n")




        ##########ROC############
        # bi_y = label_binarize(y_test, classes=levels)
        # n_classes = bi_y.shape[1]
        # print(n_classes)
        # fpr = dict()
        # tpr = dict()
        # roc_auc = dict()
        # for i in range(n_classes):
        #     fpr[i], tpr[i], _ = roc_curve(bi_y[:, i], predict_proba[:, i])
        #     roc_auc[i] = auc(fpr[i], tpr[i])
        #     File.write(str(levels[i])+":"+"\n")
        #     File.write("tpr:"+str(tpr[i])+"\n")
        #     File.write("fpr:"+str(fpr[i])+"\n")
        #     File.write("auc:"+str(roc_auc[i])+"\n")
        File.close()
    #####Plot all ROC curves
    # lw=2
    # plt.figure()
    # colors = cycle(['aqua', 'darkorange', 'cornflowerblue'])
    # for i, color in zip(range(n_classes), colors):
    #     plt.plot(fpr[i], tpr[i], color=color, lw=lw,
    #          label='ROC curve of class {0} (area = {1:0.2f})'
    #          ''.format(levels[i], roc_auc[i]))
    #
    # plt.plot([0, 1], [0, 1], 'k--', lw=lw)
    # plt.xlim([0.0, 1.0])
    # plt.ylim([0.0, 1.05])
    # plt.xlabel('False Positive Rate')
    # plt.ylabel('True Positive Rate')
    # plt.title('Some extension of Receiver operating characteristic to multi-class')
    # plt.legend(loc="lower right")
    # plt.savefig(str(drug)+"roc.png")
    # plt.show()
