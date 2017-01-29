import time,os123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport tensorflow as tf123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport numpy as np123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport pandas as pd123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport re123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom av4_input import image_and_label_queue,index_the_database_into_queue123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom av4_main import FLAGS123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom av4_networks import intuit_net123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom collections import defaultdict123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFFLAGS.saved_session = './summaries/39_netstate/saved_state-37999'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFFLAGS.predictions_file_path = re.sub("netstate","logs",FLAGS.saved_session)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFFLAGS.database_path = '../datasets/unlabeled_av4'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFFLAGS.num_epochs = 10123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFFLAGS.top_k = FLAGS.num_epochs123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFclass store_predictions_av3:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """stores all of the predictions123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    unique and sorted by protein-ligand pairs"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    pl_pairs = np.array([], dtype=str)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # collects all of the predictions (for the same pair) into an array of objects123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    predictions = np.array([])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # collects labels123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    labels = np.array([])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # formatting options in the text file123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def usd_format(self, number_array):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        """converts numpy array into user defined format"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return np.char.array(np.around(number_array, decimals=3), itemsize=5)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def top_100_score(self, predictions, labels):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        """ takes sorted in descending order by predictions list of labels123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if the dataset had n=100 drugs, how many drugs are in top 100 of the list123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        top_100_score = (TP in head -n)/n, where n is a number of Positives in a whole dataset123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        takes list of predictions, corresponding labels, returns float -percent that is correct"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # sort the array by predictions123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        order = np.flipud(predictions.argsort())123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        labels = labels[order]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # take the top n123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        num_positives = np.sum(np.asarray(labels, dtype=bool))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # if no positive labels return nan123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if num_positives == 0:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            return float('nan')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            return np.sum(labels[0:num_positives]) / num_positives * 100123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def auc(self, predictions, labels):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        """calculates area under the curve AUC for binary predictions/labels needs123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        sorted in descending order predictions"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # sort the array by predictions in descending order in case it has not been done123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        order = np.flipud(predictions.argsort())123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        labels = labels[order]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # clean labels, calculate the number of positive labels123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        labeled_true = (np.asarray(labels, dtype=bool) == True)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        num_positives = np.sum(labeled_true)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        num_predictions = len(labeled_true)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # If no positive result return nan123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if num_positives == 0:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            return float('nan')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # slide from top to the bottom;123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # each time slide the threshold so as to predict one more label as positive123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        roc_curve = np.array([0.0, 0.0])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        TP_above_threshold = 0123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        for predict_as_positive in range(num_predictions):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            if labeled_true[predict_as_positive] == True:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                TP_above_threshold += 1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            # calculate True Positives Rate123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            # TPR = TP / num_real_positives123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            TPR = TP_above_threshold / float(num_positives)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            # FPR = FP / num_real_negatives123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            FPR = (predict_as_positive + 1 - TP_above_threshold) / (num_predictions - float(num_positives))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            roc_curve = np.vstack((roc_curve, [FPR, TPR]))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        roc_curve = np.vstack((roc_curve, [1.0, 1.0]))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # reduce into TP and FP rate, integrate with trapezoid to calculate AUC123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        auc = np.trapz(roc_curve[:, 1], x=roc_curve[:, 0])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return auc123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def confusion_matrix(self, predictions, labels):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        """calculaets and returns the confusion matrix"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        TP = np.sum((np.round(predictions) == True) * (np.asarray(labels, dtype=bool) == True))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        FP = np.sum((np.round(predictions) == True) * (np.asarray(labels, dtype=bool) == False))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        FN = np.sum((np.round(predictions) == False) * (np.asarray(labels, dtype=bool) == True))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        TN = np.sum((np.round(predictions) == False) * (np.asarray(labels, dtype=bool) == False))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return np.array([[TP, FP], [FN, TN]])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def add_batch(self, ligand_file_paths,ligand_frames,batch_predictions, batch_labels):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        """maintains sorted by protein-ligand pairs lists of various predictions123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        splits the batch into "new" and "known" protein-ligand pairs123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        adds predictions of "known" ligand pairs with "," appends new protein-ligand pairs as they are"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # since with multithreading and a large batch pool size some of the entries may not be unique(rare),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # and it is faster to add entries that are unique, duplicates would be discarded123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        ligand_file_paths,unique_indices = np.unique(ligand_file_paths, return_index=True)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        batch_predictions = batch_predictions[unique_indices]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        batch_labels = batch_labels[unique_indices]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        ligand_frames = ligand_frames[unique_indices]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # extract meaningful names from the file path123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        def create_name_from_path(file_path,ligand_frame):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            return file_path.split("/")[-1] +"_frame"+str(ligand_frame)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        ligand_filenames = np.char.array(map(create_name_from_path,ligand_file_paths,ligand_frames))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        #receptor_filenames = np.char.array(map(extract_file_from_path, receptor_file_path))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        batch_pl_pairs = ligand_filenames #+ "," + receptor_filenames123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # sort the batch by protein-ligand pairs123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        order = batch_pl_pairs.argsort()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        batch_pl_pairs = batch_pl_pairs[order]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        batch_predictions = batch_predictions[order]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        batch_labels = batch_labels[order]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # check if all of the entries in the batch are unique123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if not np.array_equal(batch_pl_pairs, np.unique(batch_pl_pairs)):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            raise Exception("batch has duplicate entries")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # get binmask with True for each non-unique protein-ligand pair, False for unique protein-ligand pair123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        binmask_self = (np.searchsorted(batch_pl_pairs, self.pl_pairs, 'right') - np.searchsorted(batch_pl_pairs,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                                                                  self.pl_pairs,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                                                                  'left')) == 1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        binmask_batch = (np.searchsorted(self.pl_pairs, batch_pl_pairs, 'right') - np.searchsorted(self.pl_pairs,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                                                                   batch_pl_pairs,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                                                                   'left')) == 1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # check if the entries appended to each other have similar names123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if not np.array_equal(batch_pl_pairs[binmask_batch], self.pl_pairs[binmask_self]):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            raise Exception('Error while merging arrays. Names do not match')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # check if labels are similar123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if not np.array_equal(batch_labels[binmask_batch], self.labels[binmask_self]):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            raise Exception('Error while merging arrays. Labels for the same example should be similar')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # split into overlapping and not overlapping entries123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        overlap_pl_pairs = batch_pl_pairs[binmask_batch]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        overlap_predictions = np.char.array(self.predictions[binmask_self])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        batch_overlap_predictions = self.usd_format(batch_predictions[binmask_batch])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # for known entries join all of the predictions together123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        overlap_predictions = overlap_predictions + "," + batch_overlap_predictions123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        overlap_labels = batch_labels[binmask_batch]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # merge unique and not unique predictions123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.pl_pairs = np.hstack((self.pl_pairs[-binmask_self], batch_pl_pairs[-binmask_batch], overlap_pl_pairs))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.predictions = np.hstack(123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            (self.predictions[-binmask_self], self.usd_format(batch_predictions[-binmask_batch]), overlap_predictions))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.labels = np.hstack((self.labels[-binmask_self], batch_labels[-binmask_batch], overlap_labels))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # now sort everything by the first column123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        order = self.pl_pairs.argsort()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.pl_pairs = self.pl_pairs[order]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.predictions = self.predictions[order]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.labels = self.labels[order]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def save_predictions(self, file_path):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        """sorts in descending order of confidence,computes average predictions,formats and writes into file"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # compute average of predictions123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        num_examples = len(self.labels)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if num_examples == 0:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            raise Exception("nothing to save")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        def string_to_average(string):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            return np.average(np.array(string.split(","), dtype=float))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        prediction_averages = np.around(map(string_to_average, self.predictions), decimals=3)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # sort by prediction averages123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        order = np.flipud(prediction_averages.argsort())123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        prediction_averages = prediction_averages[order]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.pl_pairs = self.pl_pairs[order]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.predictions = self.predictions[order]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.labels = self.labels[order]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # write all of the predictions to the file123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        f = open(file_path + "_predictions.txt", 'w')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        for i in range(num_examples):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            f.write((str(prediction_averages[i]) + " " * 10)[:10]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                    + (str(self.labels[i]) + " " * 50)[:10]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                    + str(self.pl_pairs[i] + " " * 50)[:50]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                    + str(self.predictions[i] + " " * 50)[:50]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                    + "\n")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        f.close()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # write and save some metadata123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        f = open(file_path + "_scores.txt", 'w')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        f.write("top 100 score: ")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        f.write(str(self.top_100_score(self.predictions, self.labels)))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        f.write("\nAUC: ")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        f.write(str(self.auc(prediction_averages, self.labels)))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        f.write("\nconfusion matrix: ")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        f.write(str(self.confusion_matrix(prediction_averages, self.labels)))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        f.close()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # write a file in Kaggle MAP{K} submision format123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # the form is:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # Protein1, Ligand3 Ligand4 Ligand2123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # Protein2, Ligand5 Ligand9 Ligand7123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#        raw_database_array = np.genfromtxt(FLAGS.test_set_file_path, delimiter=',', dtype=str)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#        receptor_set = raw_database_array[:, 2]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#        receptor_set = list(set(map(lambda x: x.split('.')[0].split('/')[-1], receptor_set)))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#        submission = {}123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#        for i in range(num_examples):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#            # get the name of the ligand and protein123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#            ligand, receptor = self.pl_pairs[i].split(',')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#            ligand = ligand.split('/')[-1].split('.')[0]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#            receptor = receptor.split('/')[-1].split('.')[0]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#            # add all protein-ligand pairs to submission123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#            if not receptor in submission.keys():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#                submission[receptor] = {}123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#                submission[receptor]['ligands'] = [ligand]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#                submission[receptor]['score'] = [prediction_averages[i]]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#            else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#                submission[receptor]['ligands'].append(ligand)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#                submission[receptor]['score'].append(prediction_averages[i])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#        # write and save submisison to file123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#        # if failed to predict any ligand for a receptor123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#        # use placeholder 'L' as predict result123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#        # e.g. P1234,L123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#        with open(file_path + '_submission.csv', 'w') as f:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#            f.write('Id,Expected\n')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#            for key in receptor_set:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#                if key in submission.keys():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#                    ligands = np.array(submission[key]['ligands'])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#                    scores = np.array(submission[key]['score'])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#                    ligands = ligands[np.flipud(scores.argsort())]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#                    f.write(key + ',' + ' '.join(ligands) + '\n')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#                else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#                    f.write(key + ',' + 'L' + '\n')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFclass store_predictions:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    '''123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    store add of the prediction results123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :return:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    '''123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    raw_predictions = defaultdict(list)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    processed_predictions = defaultdict(list)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def add_batch(self, ligand_file_paths, batch_current_epoch, batch_predictions):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        ligand_file_name = map(lambda filename:os.path.basename(filename).split('.')[0],ligand_file_paths)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        for ligand,current_epoch,prediction in zip(ligand_file_name, batch_current_epoch, batch_predictions):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            #   if in_the_range:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            self.raw_predictions[ligand].append(prediction)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def reduce(self):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        '''123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if a ligand has more than one predictions123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        use mean as final predictions123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        '''123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        for key, value in self.raw_predictions.items():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            if len(value) > 1:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                predictions_size = map(lambda x: len(x), value)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                if len(set(predictions_size)) > 1:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                    raise Exception(key, " has different number of predictions ", set(predictions_size))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                self.processed_predictions[key].append(np.mean(value, axis=0))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                self.processed_predictions[key].append(value)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def final_predictions(self, predictions_list):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        length = min(len(predictions_list, 10))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return np.mean(predictions_list[:length])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def fill_na(self):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        for key in self.raw_predictions.keys():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            value_len = len(self.raw_predictions[key])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            if value_len>FLAGS.top_k:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                print "{} have more predictions than expected, {} reuqired {} found.".format(key,FLAGS.top_k,value_len)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                for i in range(FLAGS.top_k-value_len):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                    self.raw_predictions[key]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def save_multiframe_predictions(self):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        records = []123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        for key, value in self.raw_predictions.items():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            value_len = len(self.raw_predictions[key])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            if value_len>FLAGS.top_k:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                print "{} have more predictions than expected, {} reuqired {} found.".format(key,FLAGS.top_k,value_len)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                records.append([key]+value[:FLAGS.top_k])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                records.append([key]+value)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        submission_csv = pd.DataFrame(records, columns=['Id']+[ 'Predicted_%d'%i for i in range(1,len(records[0]))])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        submission_csv.to_csv(FLAGS.predictions_file_path + '_multiframe_submission.csv', index=False)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def save_average(self):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        '''123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        take average of multiple predcition123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        :return:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        '''123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        records = []123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        for key,value in self.raw_predictions.items():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            records.append([key,np.mean(np.array(value))])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        submission_csv = pd.DataFrame(records,columns=['ID','Predicted'])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        submission_csv.to_csv(FLAGS.predictions_file_path+'_average_submission.csv',index=False)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def save_max(self):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        records = []123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        for key,value in self.raw_predictions.items():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            records.append([key, np.max(np.array(value))])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        submission_csv = pd.DataFrame(records, columns=['ID', 'Predicted'])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        submission_csv.to_csv(FLAGS.predictions_file_path + '_max_submission.csv', index=False)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def save(self):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.save_average()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.save_max()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.save_multiframe_predictions()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef evaluate_on_train_set():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    "train a network"123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # create session which all the evaluation happens in123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    sess = tf.Session()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # create a filename queue first123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    filename_queue, examples_in_database = index_the_database_into_queue(FLAGS.database_path, shuffle=True)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # create an epoch counter123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # there is an additional step with variable initialization in order to get the name of "count up to" in the graph123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    batch_counter = tf.Variable(0)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    sess.run(tf.global_variables_initializer())123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    batch_counter_increment = tf.assign(batch_counter,tf.Variable(0).count_up_to(np.round((examples_in_database*FLAGS.num_epochs)/FLAGS.batch_size)))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    batch_counter_var_name = sess.run(tf.report_uninitialized_variables())123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    epoch_counter = tf.div(batch_counter*FLAGS.batch_size,examples_in_database)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # create a custom shuffle queue123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    ligand_files,current_epoch,label_batch,sparse_image_batch = image_and_label_queue(batch_size=FLAGS.batch_size, pixel_size=FLAGS.pixel_size,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                                          side_pixels=FLAGS.side_pixels, num_threads=FLAGS.num_threads,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                                          filename_queue=filename_queue, epoch_counter=epoch_counter)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    image_batch = tf.sparse_tensor_to_dense(sparse_image_batch,validate_indices=False)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    keep_prob = tf.placeholder(tf.float32)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    y_conv = intuit_net(image_batch,keep_prob,FLAGS.batch_size)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # compute softmax over raw predictions123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    predictions = tf.nn.softmax(y_conv)[:,1]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # restore variables from sleep123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    saver = tf.train.Saver()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    saver.restore(sess,FLAGS.saved_session)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # use123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    sess.run(tf.contrib.framework.get_variables_by_name(batch_counter_var_name[0])[0].initializer)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    coord = tf.train.Coordinator()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    threads = tf.train.start_queue_runners(sess = sess,coord=coord)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # create an instance of a class to store predictions123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    all_predictios = store_predictions()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    all_predictions_av3 = store_predictions_av3()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # add_batch(self, ligand_file_path, batch_predictions, batch_labels)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print "starting evalution..."123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    try:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        while True or not coord.should_stop():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            start = time.time()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            batch_num = sess.run([batch_counter_increment])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            my_ligand_files, my_ligand_frames, my_predictions, my_labels = sess.run(123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                [ligand_files, current_epoch, predictions, label_batch],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                feed_dict={keep_prob: 1})123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            print "current_epoch:", my_ligand_frames[0], "batch_num:", batch_num,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            print "\tprediction averages:", np.mean(my_predictions),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            print "\texamples per second:", "%.2f" % (FLAGS.batch_size / (time.time() - start))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            all_predictios.add_batch(my_ligand_files, my_ligand_frames, my_predictions)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            # add_batch(self, ligand_file_path, batch_predictions, batch_labels)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            all_predictions_av3.add_batch(my_ligand_files,my_ligand_frames,my_predictions,my_labels)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            print "my labels:",my_labels123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    except tf.errors.OutOfRangeError:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print "exiting the loop"123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    all_predictios.save()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    all_predictions_av3.save_predictions(FLAGS.predictions_file_path)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFevaluate_on_train_set()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFprint "All Done"123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF