import sys
from scipy.sparse import csr_matrix
import numpy as np
from Eval import Eval
from math import log, exp
import matplotlib

matplotlib.use('agg')
matplotlib.use('TKAgg')
import matplotlib.pyplot as graphplot
import time
from imdb import IMDBdata
from Vocab import Vocab


class NaiveBayes:
    def __init__(self, data, ALPHA=1.0):
        self.ALPHA = ALPHA
        self.data = data  # training data

        self.vocab_len = 0
        self.count_positive = 0
        self.count_negative = 0
        self.num_positive_reviews = 0.0
        self.num_negative_reviews = 0.0
        self.total_positive_words = 0
        self.total_negative_words = 0
        self.P_positive = 0.0
        self.P_negative = 0.0
        self.deno_pos = 0
        self.deno_neg = 0
        self.log_likelihood_positive_words = 0
        self.log_likelihood_negative_words = 0
        self.log_numerator_negative_probability = 0
        self.log_numerator_positive_probability = 0
        self.log_positive_probability = 0
        self.log_negative_probability = 0
        self.positive_precision = 0
        self.positive_recall = 0
        self.negative_precision = 0
        self.negative_recall = 0
        self.word_weight_positive = 0
        self.word_weight_negative = 0
        self.train(data.X, data.Y)

    # Train model - X are instances, Y are labels (+1 or -1)
    # X and Y are sparse matrices
    def train(self, X, Y):
        # TODO: Estimate Naive Bayes model parameters
        positive_indices = np.argwhere(Y == 1.0).flatten()
        negative_indices = np.argwhere(Y == -1.0).flatten()

        self.num_positive_reviews = len(positive_indices)
        self.num_negative_reviews = len(negative_indices)

        # Get frequency of each word in all positive documents.
        self.count_positive = np.zeros([X.shape[1]])
        for i in positive_indices:
            self.count_positive += X.getrow(i)

        # Get frequency of each word in all negative documents.
        self.count_negative = np.zeros([X.shape[1]])
        for i in negative_indices:
            self.count_negative += X.getrow(i)

        # Get total number of words in all positive documents.
        self.total_positive_words = 0
        self.count_positive = np.squeeze(np.asarray(self.count_positive))
        for i in self.count_positive:
            self.total_positive_words += i
        # print("Value of total positive words:", self.total_positive_words)

        # Get total number of words in all negative documents.
        self.total_negative_words = 0
        self.count_negative = np.squeeze(np.asarray(self.count_negative))
        for i in self.count_negative:
            self.total_negative_words += i
        # print("Value of total negative words:", self.total_negative_words)

        # Calculate denominator for log likelihood of positive words.
        self.deno_pos = self.total_positive_words + X.shape[1]
        # print("Value for positive denominator:", self.deno_pos)

        # Calculate denominator for log likelihood of negative words.
        self.deno_neg = self.total_negative_words + X.shape[1]
        # print("Value for negative denominator:", self.deno_neg)

        # Calculate log likelihood of each word for positive category class.
        self.log_likelihood_positive_words = np.zeros([X.shape[1]])
        for i in range(len(self.count_positive)):
            self.log_likelihood_positive_words[i] = log((self.count_positive[i] + self.ALPHA)) - log(self.deno_pos)
        # print("Log likelihood of positive words::", self.log_likelihood_positive_words)

        # Calculate log likelihood of each word for negative category class.
        self.log_likelihood_negative_words = np.zeros([X.shape[1]])
        for i in range(len(self.count_negative)):
            self.log_likelihood_negative_words[i] = log((self.count_negative[i] + self.ALPHA)) - log(self.deno_neg)
        # print("Log likelihood of negative words::", self.log_likelihood_negative_words)

        return

    # Predict labels for instances X
    # Return: Sparse matrix Y with predicted labels (+1 or -1)
    def predictlabel(self, X):
        num_of_predicted_positive = 0
        num_of_predicted_negative = 0

        # Calculate probability of positive category class.
        self.P_positive = self.num_positive_reviews / (self.num_positive_reviews + self.num_negative_reviews)

        # Calculate probability of negative category class.
        self.P_negative = self.num_negative_reviews / (self.num_positive_reviews + self.num_negative_reviews)

        pred_labels = []

        self.log_numerator_positive_probability = [0.0] * X.shape[0]
        self.log_numerator_negative_probability = [0.0] * X.shape[0]

        no_of_test_documents = X.shape[0]

        # Calculate log probability for + and - class (Ignoring the denominator P(d)) and predict labels.
        for i in range(no_of_test_documents):
            z = X[i].nonzero()
            self.log_numerator_positive_probability[i] = log(self.P_positive)
            self.log_numerator_negative_probability[i] = log(self.P_negative)
            for j in range(len(z[1])):
                self.log_numerator_positive_probability[i] += self.log_likelihood_positive_words[z[1][j]]
                self.log_numerator_negative_probability[i] += self.log_likelihood_negative_words[z[1][j]]

            if self.log_numerator_positive_probability[i] > self.log_numerator_negative_probability[
                i]:  # Predict positive
                pred_labels.append(1.0)
                num_of_predicted_positive += 1

            else:  # Predict negative
                pred_labels.append(-1.0)
                num_of_predicted_negative += 1

        # print("Number of predicted positive documents::", num_of_predicted_positive)
        # print("Number of predicted negative documents::", num_of_predicted_negative)
        return pred_labels

    def logsum(self, logx, logy):
        m = max(logx, logy)
        return m + log(exp(logx - m) + exp(logy - m))

    # Predict the probability of each indexed review in sparse matrix text
    # of being positive
    # Prints results
    def predictprobability(self, test, indexes, positive_threshold):

        self.true_positive = 0
        self.false_positive = 0
        self.false_negative = 0
        self.true_negative = 0

        # print("Calculated positive probability:")
        # print("Calculated negative probability:")

        # Calculate log probability of every document in test data for + and - class.
        for i in range(indexes):
            predicted_prob_positive = exp(self.log_numerator_positive_probability[i] - self.logsum(
                self.log_numerator_positive_probability[
                    i],
                self.log_numerator_negative_probability[
                    i]))
            predicted_prob_negative = exp(self.log_numerator_negative_probability[i] - self.logsum(
                self.log_numerator_positive_probability[
                    i],
                self.log_numerator_negative_probability[
                    i]))

            # if i < 10:
            #     print("document_number:: ", i, "probability::", predicted_prob_positive)

            # if i < 10:
            #     print("document_number:: ", i, "probability::", predicted_prob_negative)

            # if predicted_prob_positive > predicted_prob_negative:
            if predicted_prob_positive > positive_threshold:
                predicted_label = 1.0
            else:
                predicted_label = -1.0

            # print(test.Y[i], predicted_label, predicted_prob_positive, predicted_prob_negative, test.X_reviews[i])

            if test.Y[i] == predicted_label:
                if test.Y[i] == 1.0:
                    self.true_positive += 1
                else:
                    self.true_negative += 1
            else:
                if test.Y[i] == -1.0 and predicted_label == 1.0:
                    self.false_positive += 1
                else:
                    self.false_negative += 1

        # print("Values of true_positive::", self.true_positive, " false_positive::", self.false_positive,
        #       " false_negative::",
        #       self.false_negative, " true_negative::", self.true_negative)
        return

    # Calculate precision for category class passed as an argument.
    def calculateprecision(self, category_class):
        if category_class == "positive":
            return self.true_positive / (self.true_positive + self.false_positive)
        else:
            return self.true_negative / (self.true_negative + self.false_negative)

    # Calculate recall for category class passed as an argument.
    def calculaterecall(self, category_class):
        if category_class == "positive":
            return self.true_positive / (self.true_positive + self.false_negative)
        else:
            return self.true_negative / (self.true_negative + self.false_positive)

    # Call precision and recall functions for category each class.
    def calculateprecisionandrecall(self, index):
        self.positive_precision[index] = self.calculateprecision("positive")
        self.positive_recall[index] = self.calculaterecall("positive")
        self.negative_precision[index] = self.calculateprecision("negative")
        self.negative_recall[index] = self.calculaterecall("negative")

        # print("Values of positive_precision::", self.positive_precision[index], " positive_recall", self.positive_recall[index],
        #       " negative_precision::",
        #       self.negative_precision[index], " negative_recall::", self.negative_recall[index])

    # Evaluate performance on test data
    def Eval(self, test):
        y_pred = self.predictlabel(test.X)
        ev = Eval(y_pred, test.Y)
        return ev.Accuracy()

    # Plot Precision vs Recall graph for both positive and negative classes.
    def plotgraph(self):
        threshold_for_positive = np.arange(0.05, 1, 0.05)
        # print("Threshold for positive::", threshold_for_positive)
        nb.positive_precision = [0.0] * len(threshold_for_positive)
        nb.positive_recall = [0.0] * len(threshold_for_positive)
        nb.negative_precision = [0.0] * len(threshold_for_positive)
        nb.negative_recall = [0.0] * len(threshold_for_positive)

        for i in range(len(threshold_for_positive)):
            nb.predictprobability(testdata, testdata.X.shape[0], threshold_for_positive[i])
            nb.calculateprecisionandrecall(i)
        # print("Positive Precision array::", self.positive_precision)
        # print("Positive Recall array::", self.positive_recall)
        # print("Negative Precision array::", self.negative_precision)
        # print("Negative Recall array::", self.negative_recall)
        # graphplot.plot(self.positive_precision, self.positive_recall)
        # graphplot.show()
        # graphplot.plot(self.negative_precision, self.negative_recall)
        # graphplot.show()

    # Calculate word weight for each word - positive and negative category class.
    def calculatewordweight(self, v, data):
        self.word_weight_positive = [0.0] * data.shape[1]
        self.word_weight_negative = [0.0] * data.shape[1]

        for i in range(data.shape[1]):
            self.word_weight_positive[i] = (self.log_likelihood_positive_words[i] - self.log_likelihood_negative_words[
                i]) * (self.count_positive[i] - self.count_negative[i])
            self.word_weight_negative[i] = (self.log_likelihood_negative_words[i] - self.log_likelihood_positive_words[
                i]) * (self.count_negative[i] - self.count_positive[i])

            # sorted_indices_positive = np.argsort(self.log_likelihood_positive_words)
        sorted_indices_positive = self.log_likelihood_positive_words.argsort()[::-1][:20]
        sorted_indices_negative = self.log_likelihood_negative_words.argsort()[::-1][:20]
        # sorted_indices_negative = np.argsort(self.log_likelihood_negative_words)
        # print("Word weights for positive::", self.word_weight_positive)
        # print("Word weights for negative::", self.word_weight_negative)
        print("Top 20 positive words and weights::")
        for i in range(20):
            print("Word:: ", v.vocab.GetWord(sorted_indices_positive[i]), " weight:: ",
                  self.log_likelihood_positive_words[i] / (
                          self.log_likelihood_positive_words[i] + self.log_likelihood_negative_words[i]))
            # print("Log likelihood positive words::", self.log_likelihood_positive_words[i])

        print("Top 20 negative words and weights::")
        for i in range(20):
            print("Word:: ", v.vocab.GetWord(sorted_indices_negative[i]), " weight:: ",
                  self.log_likelihood_negative_words[i] / (
                          self.log_likelihood_positive_words[i] + self.log_likelihood_negative_words[i]))
            # print("Log likelihood positive words::", self.log_likelihood_negative_words[i])


if __name__ == "__main__":
    print("Reading Training Data")
    traindata = IMDBdata("%s/train" % sys.argv[1])
    print("Reading Test Data")
    testdata = IMDBdata("%s/test" % sys.argv[1], vocab=traindata.vocab)
    print("Computing Parameters")
    nb = NaiveBayes(traindata, float(sys.argv[2]))
    print("Evaluating")
    print("Test Accuracy: ", nb.Eval(testdata))
    nb.plotgraph()
    nb.calculatewordweight(traindata, nb.data.X)
