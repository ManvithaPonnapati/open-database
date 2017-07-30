# ChEMBL blast api

import os, sys
import requests
import re
import tempfile
import json


def chembl_blast(seq):
    """
    Get the blast result of the input sequence from ChEMBL server

    args:
        seq ::str 
            AMINO ACID sequence
            e.g. 'AINVLVCWAVWLNLQNNYFVVSLAAADIAVGVLAPFFFLKIWF'

    return:
        results :: list
            Blast result 
            [ChEMBL_ID, Pref_Name, ProteinAccession_ID, Identity, Blast_Score, Evalue]
    """

    if sys.version_info[0] == 3:
        import http.cookiejar
        import urllib.request
        import urllib.parse

        urlencode = urllib.parse.urlencode
        HTTPCookieProcessor = urllib.request.HTTPCookieProcessor
        build_opener = urllib.request.build_opener
        cookie = http.cookiejar.CookieJar()
    else:
        import cookielib
        from urllib import *
        from urllib2 import *

        cookie = cookielib.CookieJar()

    # create connection
    #cookie = cookiejar.CookieJar()
    handler = HTTPCookieProcessor(cookie)
    opener = build_opener(handler)
    opener.open('https://www.ebi.ac.uk/')

    # encode data
    postdata = urlencode({'seq': seq, 'seg': 'true'})
    binary_data = postdata.encode('utf-8')

    # get the blast idx from server
    opener.open('https://www.ebi.ac.uk/chembl/target/blast', binary_data)
    get_result = opener.open(
        'https://www.ebi.ac.uk/chembl/index.php/target/results/blast')
    cont = get_result.read().decode('utf-8')
    reg = r'/chembl//starlite/fetch_statistics/(\d+)'
    me = re.search(reg, cont)

    # retrive blast result from server
    if me is not None:
        idx = me.groups()[0]
        blast_result = opener.open(
            'https://www.ebi.ac.uk/chembl/target/data/blast?sEcho=1&iColumns=13&sColumns=&iDisplayStart=10&iDisplayLength=10&mDataProp_0=0&mDataProp_1=1&mDataProp_2=2&mDataProp_3=3&mDataProp_4=4&mDataProp_5=5&mDataProp_6=6&mDataProp_7=7&mDataProp_8=8&mDataProp_9=9&mDataProp_10=10&mDataProp_11=11&mDataProp_12=12&iSortCol_0=11&sSortDir_0=asc&iSortingCols=1&bSortable_0=true&bSortable_1=true&bSortable_2=true&bSortable_3=true&bSortable_4=true&bSortable_5=true&bSortable_6=true&bSortable_7=true&bSortable_8=true&bSortable_9=true&bSortable_10=true&bSortable_11=true&bSortable_12=false&_=%s'
            % idx)
        data = json.loads(blast_result.read())['aaData']

        # result contain the following columns
        # query sequence | ChEMBL ID | TID | pref name | ProteinAccession ID | Target type | Organism | Comppuounds | Endpoints | Identity | Blast Score | Evalue | Tag
        results = map(lambda datum:[datum[1], datum[3], datum[4], datum[9], datum[10], datum[11]],data)
        head = [
            'ChEMBL_ID', 'Pref_Name', 'ProteinAccession_ID', 'Identity',
            'Blast_Score', 'Evalue'
        ]
        return head, list(results)
    else:
        raise Exception("Cannot retrive blast idx")


if __name__ == '__main__':
    _, result = chembl_blast('INVCVSLAAADIAVVLLW')
    for entry in result:
        print(entry)
