from __future__ import print_function123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport os123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport sys123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport re123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport time123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport pprint123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport argparse123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport subprocess123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport multiprocessing123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom glob import glob123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom functools import partial123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom utils import smina_param123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport prody123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport numpy as np123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport pandas as pd123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport config123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom database_action import DatabaseAction, db123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom db_v2 import AffinityDatabase123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFFLAGS = None123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef get_arguments():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    parser = argparse.ArgumentParser(description='Affinity Database')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    parser.add_argument('--create',dest='db_create', action='store_true')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    parser.add_argument('--continue',dest='db_continue', action='store_true')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    parser.add_argument('--delete',dest='db_delete', action='store_true')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    parser.add_argument('--progress', dest='db_progress', action='store_true')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    parser.add_argument('--list_param', dest='db_param',action='store_true')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    parser.add_argument('--action', type=str)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    parser.add_argument('--param', type=str)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    parser.add_argument('--retry_failed', action='store_true')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    parser.add_argument('--folder_name', type=str)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    parser.add_argument('--table_idx', type=int)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    parser.add_argument('--receptor_idx', type=int)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    parser.add_argument('--ligand_idx', type=int)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    parser.add_argument('--crystal_idx', type=int)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    parser.add_argument('--docked_idx', type=int)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    parser.add_argument('--download_idx', type=int)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    FLAGS, unparsed = parser.parse_known_args()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return FLAGS123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef run_multiprocess(target_list, func):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print(len(target_list))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if len(target_list) == 0:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            return 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if type(target_list[0]).__name__ in ['unicode','str']:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            target_list = list(target_list)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            target_list = map(list, target_list)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print (len(target_list))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        pool = multiprocessing.Pool(config.process_num)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        pool.map_async(func, target_list)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        pool.close()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        pool.join()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        #map(func, target_list)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef get_job_data(func_name, table_idx, table_param, progress=False):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if func_name == 'download':123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        download_list = open(config.list_of_PDBs_to_download).readline().strip().split(', ')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        finished_list = db.get_all_success(table_idx)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        failed_list = db.get_all_failed(table_idx)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if FLAGS.retry_failed:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            rest_list = list(set(download_list) - set(finished_list) | set(failed_list))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            rest_list =list(set(download_list) - set(finished_list) - set(failed_list))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        total = len(set(download_list))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        finished = len(set(finished_list)-set(failed_list))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        failed = len(set(failed_list))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    elif func_name in ['split_ligand','split_receptor']:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        download_idx = table_param['download_idx']123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        download_list = db.get_all_success(download_idx)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        finished_list = db.get_all_success(table_idx)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        finished_list = map(lambda x:(x[0],),finished_list)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        failed_list = db.get_all_failed(table_idx)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        failed_list = map(lambda x:(x[0],), failed_list)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if FLAGS.retry_failed:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            rest_list = list(set(download_list) - set(finished_list) | set(failed_list))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            rest_list = list(set(download_list) - set(finished_list) - set(failed_list))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        total = len(set(download_list))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        finished = len(set(finished_list)-set(failed_list))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        failed = len(set(failed_list))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    elif func_name in ['reorder', 'dock']:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        rec_idx = table_param['receptor_idx']123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        rec_list = db.get_all_success(rec_idx)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        lig_idx = table_param['ligand_idx']123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        lig_list = db.get_all_success(lig_idx)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        finished_list = db.get_all_success(table_idx)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        failed_list = db.get_all_failed(table_idx)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if FLAGS.retry_failed:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            rest_list = list(set(rec_list) & set(lig_list) - set(finished_list) | set(failed_list))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            rest_list = list(set(rec_list) & set(lig_list) - set(finished_list) - set(failed_list))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        total = len(set(rec_list) & set(lig_list))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        finished = len(set(finished_list)-set(failed_list))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        failed = len(set(failed_list))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    elif func_name in ['rmsd', 'overlap']:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        cry_idx = table_param['crystal_idx']123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        cry_list = db.get_all_success(cry_idx)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        doc_idx = table_param['docked_idx']123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        doc_list = db.get_all_success(doc_idx)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        finished_list = db.get_all_success(table_idx)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        finished_list = map(lambda x: x[:-1], finished_list)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        failed_list = db.get_all_failed(table_idx)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        failed_list = map(lambda x: x[:-1], failed_list)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if FLAGS.retry_failed:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            rest_list = list(set(cry_list) & set(doc_list) - set(finished_list) | set(failed_list))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            rest_list = list(set(cry_list) & set(doc_list) - set(finished_list) - set(failed_list))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        total = len(set(cry_list) & set(doc_list))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        finished = len(set(finished_list)-set(failed_list))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        failed = len(set(failed_list))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    elif func_name == 'native_contact':123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        rec_idx = table_param['receptor_idx']123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        rec_list = db.get_all_success(rec_idx)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        cry_idx = table_param['crystal_idx']123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        cry_list = db.get_all_success(cry_idx)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        doc_idx = table_param['docked_idx']123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        doc_list = db.get_all_success(doc_idx)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        finished_list = db.get_all_success(table_idx)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        finished_list = map(lambda x: x[:-1], finished_list)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        failed_list = db.get_all_failed(table_idx)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        failed_list = map(lambda x: x[:-1], failed_list)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if FLAGS.retry_failed:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            rest_list = list(set(rec_list) & set(cry_list) & set(doc_list) - set(finished_list) | set(failed_list))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            rest_list = list(set(rec_list) & set(cry_list) & set(doc_list) - set(finished_list) - set(failed_list))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        total = len(set(rec_list) & set(cry_list) & set(doc_list))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        finished = len(set(finished_list)- set(failed_list))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        failed = len(set(failed_list))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    elif func_name == 'binding_affinity':123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        finished_list = db.get_all_success(table_idx)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        failed_list = db.get_all_failed(table_idx)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        total = len(set(finished_list) | set(failed_list))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        finished = len(set(finished_list) - set(failed_list))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        failed = len(set(failed_list))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # binding affinity finished at the first time it launched123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # no rest entry left to continue123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        rest_list = [[]]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    elif func_name == 'exclusion':123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        finished_list = db.get_all_success(table_idx)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        failed_list = db.get_all_failed(table_idx)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        total = len(set(finished_list) | set(failed_list))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        finished = len(set(finished_list) - set(failed_list))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        failed = len(set(failed_list))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        rest_list = [[]]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        raise Exception("unknown func_name %s" % func_name)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if progress:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return (total, finished, failed)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return rest_list123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef db_create():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if FLAGS.action == 'download':123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if FLAGS.folder_name is None:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            raise Exception("folder_name required")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        folder_name = FLAGS.folder_name123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        table_param = {123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'func':'download',123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'output_folder': folder_name,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        }123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    elif FLAGS.action == 'split_receptor':123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if FLAGS.folder_name is None:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            raise Exception("folder_name required")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if FLAGS.download_idx is None:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            raise Exception('download_idx required')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        folder_name = FLAGS.folder_name123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        download_idx = FLAGS.download_idx123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        download_folder = db.get_folder(download_idx)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        table_param = {123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'func':'split_receptor',123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'output_folder':folder_name,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'download_idx':download_idx,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'input_download_folder':'{}_{}'.format(download_idx, download_folder),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'depend':[download_idx]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        }123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    elif FLAGS.action == 'split_ligand':123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if FLAGS.folder_name is None:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            raise Exception("folder_name required")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if FLAGS.download_idx is None:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            raise Exception('download_idx required')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        folder_name = FLAGS.folder_name123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        download_idx = FLAGS.download_idx123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        download_folder = db.get_folder(download_idx)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        table_param = {123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'func':'split_ligand',123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'output_folder': folder_name,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'download_idx': download_idx,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'input_download_folder': '{}_{}'.format(download_idx, download_folder),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'depend':[download_idx],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'fit_box_size':20123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        } 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    elif FLAGS.action == 'reorder':123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if FLAGS.folder_name is None:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            raise Exception("folder_name required")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if FLAGS.receptor_idx is None:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            raise Exception('receptor_idx required')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if FLAGS.ligand_idx is None:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            raise Exception('ligand_idx required')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        folder_name = FLAGS.folder_name123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        receptor_idx = FLAGS.receptor_idx123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        receptor_folder = db.get_folder(receptor_idx)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        ligand_idx = FLAGS.ligand_idx123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        ligand_folder = db.get_folder(ligand_idx)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        table_param = {123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'func': 'reorder',123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'output_folder': folder_name,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'receptor_idx':receptor_idx,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'input_receptor_folder':'{}_{}'.format(receptor_idx,receptor_folder),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'ligand_idx': ligand_idx,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'input_ligand_folder': '{}_{}'.format(ligand_idx, ligand_folder),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'depend':[receptor_idx, ligand_idx],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'smina_param':config.smina_dock_pm['reorder']123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        }123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    elif FLAGS.action == 'smina_dock':123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if FLAGS.folder_name is None:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            raise Exception("folder_name required")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if FLAGS.receptor_idx is None:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            raise Exception('receptor_idx required')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if FLAGS.ligand_idx is None:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            raise Exception('ligand_idx required')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if FLAGS.param is None:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            raise Exception('param required')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        dock_param = FLAGS.param123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if not dock_param in config.smina_dock_pm.keys():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            raise KeyError("dock param {} doesn't exists. ".format(dock_param)\123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                            + "available options are: {}".format(', '.join(config.smina_dock_pm.keys())))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        dock_param = config.smina_dock_pm[dock_param]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        folder_name = FLAGS.folder_name123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        receptor_idx = FLAGS.receptor_idx123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        receptor_folder = db.get_folder(receptor_idx)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        ligand_idx = FLAGS.ligand_idx123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        ligand_folder = db.get_folder(ligand_idx)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        table_param = {123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'func': 'smina_dock',123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'output_folder': folder_name,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'receptor_idx':receptor_idx,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'input_receptor_folder': '{}_{}'.format(receptor_idx, receptor_folder),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'ligand_idx': ligand_idx,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'input_ligand_folder': '{}_{}'.format(ligand_idx, ligand_folder),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'depend':[receptor_idx, ligand_idx],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'smina_param':dock_param123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        }123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    elif FLAGS.action == 'rmsd':123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if FLAGS.crystal_idx is None:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            raise Exception('crystal_idx required')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if FLAGS.docked_idx is None:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            raise Exception('docked_idx required')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        crystal_idx = FLAGS.crystal_idx123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        crystal_folder = db.get_folder(crystal_idx)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        docked_idx = FLAGS.docked_idx123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        docked_folder = db.get_folder(docked_idx)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        table_param = {123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'func':'rmsd',123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'crystal_idx': crystal_idx,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'input_crystal_folder':'{}_{}'.format(crystal_idx, crystal_folder),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'docked_idx': docked_idx,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'input_docked_folder':'{}_{}'.format(docked_idx, docked_folder),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'depend':[crystal_idx, docked_idx]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        }123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    elif FLAGS.action == 'overlap':123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if FLAGS.crystal_idx is None:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            raise Exception('crystal_idx require')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if FLAGS.docked_idx is None:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            raise Exception('docked_idx required')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if FLAGS.param is None:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            raise Exception('param required')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        overlap_param = FLAGS.param123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if not overlap_param in config.overlap_pm.keys():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            raise KeyError("dock param {} doesn't exists. ".format(overlap_param) \123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                           + "available options are: {}".format(', '.join(config.overlap_pm.keys())))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        overlap_param = config.overlap_pm[overlap_param]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        crystal_idx = FLAGS.crystal_idx123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        crystal_folder = db.get_folder(crystal_idx)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        docked_idx = FLAGS.docked_idx123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        docked_folder = db.get_folder(docked_idx)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        table_param = {123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'func':'overlap',123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'crystal_idx': crystal_idx,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'input_crystal_folder':'{}_{}'.format(crystal_idx, crystal_folder),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'docked_idx': docked_idx,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'input_docked_folder':'{}_{}'.format(docked_idx, docked_folder),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'depend':[crystal_idx, docked_idx],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        }123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        table_param.update(overlap_param)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    elif FLAGS.action == 'native_contact':123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if FLAGS.receptor_idx is None:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            raise Exception('receptor_idx required')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if FLAGS.crystal_idx is None:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            raise Exception('crystal_idx require')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if FLAGS.docked_idx is None:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            raise Exception('docked_idx required')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if FLAGS.param is None:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            raise Exception('param required')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        native_contact_param = FLAGS.param123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if not native_contact_param in config.native_contact_pm.keys():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            raise KeyError("dock param {} doesn't exists. ".format(native_contact_param) \123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                           + "available options are: {}".format(', '.join(config.native_contact_pm.keys())))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        native_contact_param = config.native_contact_pm[native_contact_param]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        receptor_idx = FLAGS.receptor_idx123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        receptor_folder = db.get_folder(receptor_idx)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        crystal_idx = FLAGS.crystal_idx123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        crystal_folder = db.get_folder(crystal_idx)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        docked_idx = FLAGS.docked_idx123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        docked_folder = db.get_folder(docked_idx)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        table_param = {123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'func':'native_contact',123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'receptor_idx': receptor_idx,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'input_receptor_folder':'{}_{}'.format(receptor_idx, receptor_folder),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'crystal_idx': crystal_idx,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'input_crystal_folder':'{}_{}'.format(crystal_idx, crystal_folder),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'docked_idx': docked_idx,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'input_docked_folder':'{}_{}'.format(docked_idx, docked_folder),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'depend': [receptor_idx, crystal_idx, docked_idx],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        }123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        table_param.update(native_contact_param)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    elif FLAGS.action == 'binding_affinity':123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if FLAGS.param is None:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            raise Exception('param required')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        bind_param = FLAGS.param123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if not bind_param in config.bind_pm.keys():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            raise Exception('No binidng affinity file for key {} in config\n'.format(bind_param)\123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                             + 'Available choices are {}'.format(str(config.bind_pm.keys())))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        table_param = {123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'func':'binding_affinity',123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'bind_param': config.bind_pm[bind_param]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        }123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    elif FLAGS.action == 'exclusion':123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if FLAGS.param is None:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            raise Exception('param required')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        ex_param = FLAGS.param123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if not ex_param in config.exclusion_pm.keys():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            raise Exception('No exclusion records file for key {} in config\n'.format(ex_param) \123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                            + 'Available choices are {}'.format(str(config.exclusion_pm.keys())))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        table_param = {123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'func':'exclusion',123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'ex_param': config.exclusion_pm[ex_param]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        }123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        raise Exception("Doesn't support action {}".format(FLAGS.action))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    func_name = table_param['func']123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    func = DatabaseAction[func_name]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if func_name == 'smina_dock':123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        table_type = 'docked_ligand'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        data_type = 'dock'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    elif func_name == 'reorder':123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        table_type = 'reorder_ligand'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        data_type = 'reorder'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        table_type = func_name123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        data_type = func_name123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    table_idx = db.create_table(table_type, table_param)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    data = get_job_data(data_type, table_idx, table_param)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    run_multiprocess(data, partial(func, table_idx, table_param))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef db_continue():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if FLAGS.table_idx is None:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        raise Exception("table_idx required")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    table_idx = FLAGS.table_idx123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    table_name, table_param = db.get_table(table_idx)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    func_name = table_param['func']123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    func = DatabaseAction[func_name]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if func_name == 'smina_dock':123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        table_type = 'docked_ligand'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        data_type = 'dock'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    elif func_name == 'reorder':123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        table_type = 'reorder_ligand'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        data_type = 'reorder'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        table_type = func_name123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        data_type = func_name123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    data = get_job_data(data_type, table_idx, table_param)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    run_multiprocess(data, partial(func, table_idx, table_param))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef db_delete():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if FLAGS.table_idx is None:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        raise Exception('table_idx required')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    table_idx = FLAGS.table_idx123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    db.delete_table(table_idx)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef db_progress():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if FLAGS.table_idx is None:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        raise Exception('table_idx required')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    table_idx = FLAGS.table_idx123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if table_idx:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        table_idxes = [table_idx]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        table_idxes = sorted(db.get_all_dix())123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print("Progress\n")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if len(table_idxes):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print("Total jobs |  Finished  | Finished(%) |   Failed   |  Failed(%)  |   Remain   |  Remain(%)  | Table name ")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    for table_idx in table_idxes:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        table_name, table_param = db.get_table(table_idx)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        func_name = table_param['func']123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if func_name == 'smina_dock':123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            data_type = 'dock'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        elif func_name == 'reorder':123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            data_type='reorder'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            data_type = func_name123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        total, finished, failed = get_job_data(data_type, table_idx, table_param, progress=True)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print( "{:<13d} {:<11d} {:<15.2f} {:<11d} {:<14.2f} {:<11d} {:<12.2f} {}". \123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                format(total,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                       finished, 100.*finished/total  if total else 0,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                       failed, 100.*failed/total if total else 0,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                       total - finished - failed, 100.*(total-finished-failed)/total if total else 0,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                       table_name))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef db_param():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if FLAGS.table_idx is None:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        raise Exception('table_idx required')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    table_idx = FLAGS.table_idx123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    table_name, table_param = db.get_table(table_idx)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print("Parameter for Table: {}".format(table_name))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    pprint.pprint(table_param)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef main():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if FLAGS.db_create:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        db_create()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if FLAGS.db_continue:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        db_continue()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if FLAGS.db_delete:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        db_delete()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if FLAGS.db_progress:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        db_progress()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if FLAGS.db_param:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        db_param()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFif __name__ == '__main__':123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    FLAGS = get_arguments()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    main()