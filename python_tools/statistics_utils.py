import numpy as np
import numpy_utils as nu

def ensure_scalar(array):
    if nu.is_array_like(array):
        return len(array)

def precision(TP,FP):
    TP = ensure_scalar(TP)
    FP = ensure_scalar(FP)
    
    if (TP + FP) > 0:
        return TP/(TP + FP)
    else:
        return np.nan
    
def recall(TP,FN):
    TP = ensure_scalar(TP)
    FN = ensure_scalar(FN)
    
    if (TP + FN) > 0:
        return TP/(TP + FN)
    else:
        return np.nan
    
def f1(TP,FP,FN):
    
    
    curr_prec = precision(TP,FP)
    curr_recall = recall(TP,FN)
    
    if curr_prec + curr_recall > 0:
        return 2*(curr_prec*curr_recall)/(curr_prec + curr_recall)
    else:
        return np.nan
    
def calculate_scores(TP,FP,FN):
    return dict(precision=precision(TP,FP),
               recall=recall(TP,FN),
               f1=f1(TP,FP,FN))

import pandas_utils as pu
import pandas as pd
def add_false_true_positive_negative_labels(
    df,
    y_true_label,
    y_pred_label,
    output_column_name="category",
    positive_value=True,
    negative_value=False):
    """
    Purpose: To add the TP,TN,FP,FN labels to a dataframe
    
    """
    def classification_category(row):
            classified = row[y_pred_label]
            truth = row[y_true_label]

            if classified == positive_value and truth == positive_value:
                return "TP"
            elif classified == negative_value and truth == negative_value:
                return "TN"
            elif classified == positive_value and truth == negative_value:
                return "FP"
            elif classified == negative_value and truth == positive_value:
                return "FN"
            else:
                raise Exception("")
    df = pd.DataFrame(df)
    df[output_column_name] = pu.new_column_from_row_function(df,
                                                            classification_category)
    
    return df

from sklearn.metrics import confusion_matrix

def true_and_pred_labels_to_confusion_matrix(y_true,
                                             y_pred,
                                             labels=None,
                                             return_df = True,
                                                ):
    """
    Purpose: To turn a list of the 
    classifications into a confusion matrix
    
    Example:
    labels=["inhibitory","excitatory"]
    true_and_pred_labels_to_confusion_matrix(df_filtered["manual_label"],
                                             df_filtered["auto_label"],
                                            labels)
    """

    return confusion_matrix(y_true,y_pred,
                labels=labels)

def df_to_confusion_matrix(df,
                       y_true_label=None,
                      y_pred_label=None,
                      labels=None,
                          return_df=False):
    """
    Purpose: Dataframe with columns representing classes
    to the confusion matrix of the prediction
    
    Ex:
    stu.df_to_confusion_matrix(df_filtered,labels=["inhibitory","excitatory"])
    """
    if y_true_label is None and y_pred_label is None:
        y_true_label = df.columns[0]
        y_pred_label = df.columns[1]
    
    return stu.true_and_pred_labels_to_confusion_matrix(df[y_true_label],
                                         df[y_pred_label],
                                        labels)

from sklearn.metrics import precision_recall_fscore_support

def true_and_pred_labels_to_precision_recall_f1score(y_true,
                                                     y_pred,
                                                    labels=None,
                                                    positive_value=None,
                                                    average=None,):
    """
    Arguments for average
    average:
    - micro : Calculate metrics globally by counting the total true positives, false negatives and false positives
    - macro : Calculate metrics for each label, and find their unweighted mean. This does not take label imbalance into account
    
    
    
    """
    if labels is None:
        lables = np.unique(y_true)
        print(f"Using labels : {lables}")
        
    precision,recall,f1,_ = precision_recall_fscore_support(y_true,y_pred,labels=labels,average=average)
    
    if positive_value is None or average is not None:
        return precision,recall,f1
    else:
        positive_idx = np.where(np.array(labels) == positive_value)[0][0]
        return precision[positive_idx],recall[positive_idx],f1[positive_idx]

    
    
# ----------- probability distributions --------------

# ----- binomial distribution ----
import scipy

def binomial_probability(sample,n,p):
    """
    Ex: 
    r_values = list(range(n + 1))
    dist = [binom.pmf(r, n, p) for r in r_values ]
    
    """
    return scipy.stats.binom.pmf(sample, n, p)

def binomial_probability_from_samples(samples,n,p,log = True):
    
    probs = np.array([stu.binomial_probability(k,n,p) for k in samples])
    if log:
        return np.sum(np.log(probs))
    else:
        return np.prod(probs)
    
import sklearn

def roc_curve(
    y_true,
    y_score,
    **kwargs):
    return sklearn.metrics.roc_curve(
        y_true,
        y_score,
        **kwargs)



# ------------ correlations --------------------
def corr(x,y):
    return np.corrcoef(x, y)[1,0]
    
def corr_pearson(x,y,return_p_value = False):
    results = scipy.stats.pearsonr(x, y)
    if return_p_value:
        return results
    else:
        return results[0]
    
def corr_spearman(x,y,return_p_value = False):
    results = scipy.stats.spearmanr(x, y)
    if return_p_value:
        return results
    else:
        return results[0]
    
def corr_kendall(x,y,return_p_value = False):
    results = scipy.stats.kendalltau(x, y)
    if return_p_value:
        return results
    else:
        return results[0]

import statistics_utils as stu