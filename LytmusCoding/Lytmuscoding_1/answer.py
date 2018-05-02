"""Write your solution in this file.

You can execute and test your answer by pressing 'Try Answer' in the side panel,
or by running `python test_answer.py <test_case_path>` on the command line.

For example:
    python test_answer.py inputs/twenty_workers_twenty_per_page.json
"""

import urllib
import pandas as pd
from multiprocessing import Pool
from functools import partial


def ApiCall(per_page,page):
    url = 'http://localhost:8000/products?page='+str(page)+'&per_page=' + str(per_page)
    responsepg = urllib.urlopen(url)
    response = responsepg.read()
    sf = pd.read_json(response)
    return sf

def parallel_get_products(nr_workers, port, per_page, csv_file):
    url = 'http://localhost:8000/products'
    responsepg = urllib.urlopen(url)
    productcnt = int(responsepg.headers['X-Number-Objects'])
    p = Pool(nr_workers)
    arg=[]
    df = pd.DataFrame()
    func = partial(ApiCall,per_page)
    for i in range(int(productcnt/per_page)):
        t=i+1
        arg.append(int(t))
    results=p.map(func, arg)
    for each in results:
        df = df.append(each,ignore_index=True)
    df.drop('rating', axis=1, inplace=True)
    df.drop('price', axis=1, inplace=True)
    df=df.sort_values(by=["id"])
    df.to_csv(csv_file, index=False,columns=['id','title','category','stock'])
    return productcnt
