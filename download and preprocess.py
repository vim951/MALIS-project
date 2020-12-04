## Libraries

from os import listdir
from os.path import isfile, join
from pathlib import Path

from PIL import Image
import numpy as np
import pandas as pd

## Constants

csv_db_path = '/home/victor/Downloads/train_clean.csv'
csv_labels_path = '/home/victor/Downloads/train_label_to_category.csv'
db_path = '/home/victor/MALIS-DB'
preprocessed_db_path='/home/victor/MALIS-PDB'

size=100

## DB reading

def id_to_np(i):
    try:
        return np.load(join(preprocessed_db_path, i+'.npy'))
    except:
        pass

def load_db_csv(n):
    excluded = [138982, 126637, 177870]
    db_df = pd.read_csv(csv_db_path)
    labels_df = pd.read_csv(csv_labels_path)
    values = sorted(db_df.values, key=lambda x: -len(x[1]))
    i,R=0,[]
    while len(R)<n:
        if not values[i][0] in excluded:
            R.append(values[i])
        i+=1
    return R, [labels_df[labels_df['landmark_id']==r[0]].values[0][-1].split(':')[-1] for r in R]
    
## Preprocessing

def preprocess_image(image_path, size, bin_path):
    img = Image.open(image_path)
    l,h = img.size
    c = min(l,h)
    dl, dh = (l-c)//2, (h-c)//2
    img_cropped = img.crop((dl, dh, c+dl, c+dh))
    img_resized = img_cropped.resize((size,size))
    np_img = np.array(img_resized)
    np_img_bw = np.mean(np_img, axis=2)
    np_img_normal = np.float16(np_img_bw/255)
    with open(bin_path, 'wb') as f:
        np.save(f, np_img_normal)
    return np_img_normal

def preprocess_database(from_path=None, to_path=None):
    
    from_path = db_path if from_path==None else from_path
    to_path = preprocessed_db_path #if to_path==None else to_path
    print("Preprocessing " + from_path)
    
    to_dir = Path(to_path)
    if not to_dir.exists():
        to_dir.mkdir()
    
    for f in [f for f in listdir(from_path) if (isfile(join(from_path, f)) and not ".npy" in f)]:
        preprocess_image(join(from_path, f), size, join(to_path, f).replace(".jpg", ".npy"))
    
    for d in [f for f in listdir(from_path) if not isfile(join(from_path, f))]:
        preprocess_database(join(from_path, d), join(to_path, d))

## Go ma gueule

def download_preprocess_send(n):
    C,_ = load_db_csv(n)
    k=0
    for c in C:
        L=c[1].split(' ')