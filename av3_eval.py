import time,re123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport tensorflow as tf123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport numpy as np123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom av3 import FLAGS,max_net,compute_weighted_cross_entropy_mean123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom av3_input import launch_enqueue_workers123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# set up global parameters123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFFLAGS.saved_session = './summaries/6_netstate/saved_state-4999'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFFLAGS.predictions_file_path = re.sub("netstate","logs",FLAGS.saved_session)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# todo log AUC123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# todo cross entropy123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# change predictions to all_prediction to avoid confusion123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# todo better epoch counter that can stop123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFclass store_predictions:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """stores all of the predictions123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    unique and sorted by protein-ligand pairs"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    pl_pairs =np.array([],dtype=str)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # collects all of the predictions (for the same pair) into an array of objects123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    predictions = np.array([])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # collects labels123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    labels = np.array([])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # formatting options in the text file123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def usd_format(self,number_array):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        """converts numpy array into user defined format"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return np.char.array(np.around(number_array,decimals=3),itemsize=5)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def top_100_score(self,predictions,labels):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        """ takes sorted in descending order by predictions list of labels123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if the dataset had n=100 drugs, how many drugs are in top 100 of the list123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        top_100_score = (TP in head -n)/n, where n is a number of Positives in a whole dataset123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        takes list of predictions, corresponding labels, returns float -percent that is correct"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # sort the array by predictions123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        order = np.flipud(predictions.argsort())123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        labels = labels[order]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # take the top n123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        num_positives = np.sum(np.asarray(labels,dtype=bool))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # if no positive labels return nan123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if num_positives == 0:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            return float('nan')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            return np.sum(labels[0:num_positives]) / num_positives * 100123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def auc(self,predictions,labels):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        """calculates area under the curve AUC for binary predictions/labels needs123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        sorted in descending order predictions"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # sort the array by predictions in descending order in case it has not been done123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        order = np.flipud(predictions.argsort())123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        labels = labels[order]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # clean labels, calculate the number of positive labels123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        labeled_true = (np.asarray(labels,dtype=bool) == True)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        num_positives = np.sum(labeled_true)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        num_predictions = len(labeled_true)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # If no positive result return nan123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if num_positives == 0:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            return float('nan')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # slide from top to the bottom;123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # each time slide the threshold so as to predict one more label as positive123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        roc_curve = np.array([0.0,0.0])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        TP_above_threshold = 0123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        for predict_as_positive in range(num_predictions):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            if labeled_true[predict_as_positive] == True:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                TP_above_threshold +=1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            # calculate True Positives Rate123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            # TPR = TP / num_real_positives123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            TPR = TP_above_threshold / float(num_positives)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            # FPR = FP / num_real_negatives123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            FPR = (predict_as_positive +1 - TP_above_threshold) / (num_predictions - float(num_positives))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            roc_curve = np.vstack((roc_curve,[FPR,TPR]))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        roc_curve = np.vstack((roc_curve,[1.0,1.0]))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # reduce into TP and FP rate, integrate with trapezoid to calculate AUC123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        auc = np.trapz(roc_curve[:,1], x=roc_curve[:,0])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return auc123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def confusion_matrix(self,predictions,labels):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        """calculaets and returns the confusion matrix"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        TP = np.sum((np.round(predictions) == True) * (np.asarray(labels, dtype=bool) == True))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        FP = np.sum((np.round(predictions) == True) * (np.asarray(labels, dtype=bool) == False))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        FN = np.sum((np.round(predictions) == False) * (np.asarray(labels, dtype=bool) == True))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        TN = np.sum((np.round(predictions) == False) * (np.asarray(labels, dtype=bool) == False))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return np.array([[TP,FP],[FN,TN]])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def add_batch(self,ligand_file_path,receptor_file_path,batch_predictions,batch_labels):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        """maintains sorted by protein-ligand pairs lists of various predictions123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        splits the batch into "new" and "known" protein-ligand pairs123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        adds predictions of "known" ligand pairs with "," appends new protein-ligand pairs as they are"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # extract meaningful names from the file path123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        def extract_file_from_path(file_path):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            return file_path.split("/")[-1]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        ligand_filenames = np.char.array(map(extract_file_from_path,ligand_file_path))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        receptor_filenames = np.char.array(map(extract_file_from_path,receptor_file_path))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        batch_pl_pairs = ligand_filenames + "," + receptor_filenames123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # sort the batch by protein-ligand pairs123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        order = batch_pl_pairs.argsort()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        batch_pl_pairs = batch_pl_pairs[order]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        batch_predictions = batch_predictions[order]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        batch_labels = batch_labels[order]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # check if all of the entries in the batch are unique123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if not np.array_equal(batch_pl_pairs,np.unique(batch_pl_pairs)):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            raise Exception("batch has duplicate entries")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # get binmask with True for each non-unique protein-ligand pair, False for unique protein-ligand pair123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        binmask_self = (np.searchsorted(batch_pl_pairs,self.pl_pairs, 'right') - np.searchsorted(batch_pl_pairs,self.pl_pairs,'left')) == 1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        binmask_batch = (np.searchsorted(self.pl_pairs,batch_pl_pairs, 'right') - np.searchsorted(self.pl_pairs,batch_pl_pairs,'left')) == 1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # check if the entries appended to each other have similar names123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if not np.array_equal(batch_pl_pairs[binmask_batch],self.pl_pairs[binmask_self]):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            raise Exception('Error while merging arrays. Names do not match')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # check if labels are similar123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if not np.array_equal(batch_labels[binmask_batch],self.labels[binmask_self]):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            raise Exception('Error while merging arrays. Labels for the same example should be similar')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # split into overlapping and not overlapping entries123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        overlap_pl_pairs = batch_pl_pairs[binmask_batch]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        overlap_predictions = np.char.array(self.predictions[binmask_self])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        batch_overlap_predictions = self.usd_format(batch_predictions[binmask_batch])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # for known entries join all of the predictions together123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        overlap_predictions = overlap_predictions + "," + batch_overlap_predictions123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        overlap_labels = batch_labels[binmask_batch]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # merge unique and not unique predictions123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.pl_pairs = np.hstack((self.pl_pairs[-binmask_self],batch_pl_pairs[-binmask_batch],overlap_pl_pairs))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.predictions = np.hstack((self.predictions[-binmask_self],self.usd_format(batch_predictions[-binmask_batch]),overlap_predictions))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.labels = np.hstack((self.labels[-binmask_self],batch_labels[-binmask_batch],overlap_labels))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # now sort everything by the first column123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        order = self.pl_pairs.argsort()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.pl_pairs = self.pl_pairs[order]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.predictions = self.predictions[order]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.labels = self.labels[order]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def save_predictions(self,file_path):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        """sorts in descending order of confidence,computes average predictions,formats and writes into file"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # compute average of predictions123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        num_examples = len(self.labels)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if num_examples == 0:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            raise Exception ("nothing to save")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        def string_to_average(string):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            return np.average(np.array(string.split(","),dtype=float))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        prediction_averages = np.around(map(string_to_average,self.predictions),decimals=3)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # sort by prediction averages123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        order = np.flipud(prediction_averages.argsort())123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        prediction_averages = prediction_averages[order]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.pl_pairs = self.pl_pairs[order]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.predictions = self.predictions[order]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.labels = self.labels[order]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # write all of the predictions to the file123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        f = open(file_path + "_predictions.txt", 'w')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        for i in range(num_examples):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            f.write((str(prediction_averages[i]) + " "*10)[:10]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                    + (str(self.labels[i]) + " "*50)[:10]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                    + str(self.pl_pairs[i] + " "*50)[:50]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                    + str(self.predictions[i] + " "*50)[:50]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                    + "\n")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        f.close()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # write and save some metadata123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        f = open(file_path + "_scores.txt", 'w')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        f.write("top 100 score: ")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        f.write(str(self.top_100_score(self.predictions,self.labels)))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        f.write("\nAUC: ")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        f.write(str(self.auc(prediction_averages,self.labels)))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        f.write("\nconfusion matrix: ")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        f.write(str(self.confusion_matrix(prediction_averages,self.labels)))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        f.close()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # write a file in Kaggle MAP{K} submision format123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # the form is:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # Protein1, Ligand3 Ligand4 Ligand2123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # Protein2, Ligand5 Ligand9 Ligand7123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        raw_database_array = np.genfromtxt(FLAGS.test_set_file_path, delimiter=',', dtype=str)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        receptor_set = raw_database_array[:,2]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        receptor_set = list(set(map(lambda x:x.split('.')[0].split('/')[-1],receptor_set)))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        submission = {}123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        for i in range(num_examples):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            # get the name of the ligand and protein123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            ligand,receptor = self.pl_pairs[i].split(',')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            ligand = ligand.split('/')[-1].split('.')[0]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            receptor = receptor.split('/')[-1].split('.')[0]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            # add all protein-ligand pairs to submission123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            if not receptor in submission.keys():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                submission[receptor] = {}123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                submission[receptor]['ligands'] = [ligand]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                submission[receptor]['score'] = [prediction_averages[i]]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                submission[receptor]['ligands'].append(ligand)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                submission[receptor]['score'].append(prediction_averages[i])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # write and save submisison to file123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # if failed to predict any liagnd for a receptor123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # use placeholder 'L' as predict result123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # e.g. P1234,L123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        with open(file_path+'_submission.csv','w') as f:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            f.write('Id,Expected\n')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            for key in receptor_set:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                if key in submission.keys():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                    ligands = np.array(submission[key]['ligands'])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                    scores = np.array(submission[key]['score'])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                    ligands = ligands[np.flipud(scores.argsort())]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                    f.write(key+','+' '.join(ligands)+'\n')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                    f.write(key+','+'L'+'\n')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef evaluate_on_train_set():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    "train a network"123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # create session all of the evaluation happens in one123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    sess = tf.Session()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    train_image_queue,filename_coordinator = launch_enqueue_workers(sess=sess,pixel_size=FLAGS.pixel_size,side_pixels=FLAGS.side_pixels,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                                    num_workers=FLAGS.num_workers, batch_size=FLAGS.batch_size,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                                    database_index_file_path="fake_set.csv",num_epochs=3)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    y_, x_image_batch,ligand_filename,receptor_filename = train_image_queue.dequeue_many(FLAGS.batch_size)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    keep_prob = tf.placeholder(tf.float32)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    y_conv = max_net(x_image_batch, keep_prob)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    cross_entropy_mean = compute_weighted_cross_entropy_mean(y_conv, y_, batch_size=FLAGS.batch_size)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # compute softmax over raw predictions123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    predictions = tf.nn.softmax(y_conv)[:,1]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # restore variables from sleep123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    saver = tf.train.Saver()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    saver.restore(sess,FLAGS.saved_session)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # create a variable to store all predictions123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    all_predictions = store_predictions()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    batch_num = 0123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    while not filename_coordinator.stop:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        start = time.time()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        my_ligand_filename,my_receptor_filename,my_predictions,labels,my_cross_entropy = sess.run([ligand_filename,receptor_filename,predictions,y_,cross_entropy_mean],feed_dict={keep_prob:1})123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        all_predictions.add_batch(my_ligand_filename,my_receptor_filename,my_predictions,labels)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print "step:", batch_num, "test error:", my_cross_entropy, "examples per second:", "%.2f" % (FLAGS.batch_size / (time.time() - start))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        batch_num +=1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    all_predictions.save_predictions(FLAGS.predictions_file_path)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFevaluate_on_train_set()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFprint "all done!"123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF