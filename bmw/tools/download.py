import requests # request img from web
import shutil # save img locally
import os

def download(url, path):
    os.mkdir(path)
    res = requests.get(url, stream = True)

    if res.status_code == 200:
        with open(path,'wb') as f:
            shutil.copyfileobj(res.raw, f)
    else:
        raise 'Image Couldn\'t be retrieved'