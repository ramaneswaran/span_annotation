import os
import numpy as np
from numpy.lib.npyio import save 
import pandas as pd
import shutil 
from tqdm import tqdm

from typing import List

def process_emotions(emotions: List[str]) -> List[int]:

    result = []

    for emotion in emotions:
        if "not" in emotion:
            result.append(0)
        else:
            result.append(1)
    
    return result


target_dir = './data/disgust_v2'
target_image_dir = os.path.join(target_dir, 'images')

image_dir = './static/images'
csv_path = 'backup.csv'


if __name__ == "__main__":

    try:

        if os.path.exists(target_dir) is False:
            os.mkdir(target_dir)
        else:
            raise Exception("Directory exists!")
    except Exception as error:
        print("Ensure you are not overwriting a file")
        
    
    if os.path.exists(target_image_dir) is False:
        os.mkdir(target_image_dir)

    df = pd.read_csv(csv_path)

    emotion_labels = ['anger', 'sadness', 'disgust', 'fear', 'joy', 'surprise', 'neutral']  
    headers = ['image', 'anger', 'sadness', 'disgust', 'fear', 'joy', 'surprise', 'neutral']

    count = 0

    data = []

    for idx in tqdm(range(len(df)), total=len(df)):
        image_name = df.iloc[idx]['image']
        image_path = os.path.join(image_dir, image_name)

        emotions = df.iloc[idx][emotion_labels]
        emotions = process_emotions(emotions)

        if np.sum(emotions) == 1:
            row = df.iloc[idx][headers].tolist()
            data.append(row)

            shutil.copy(image_path, target_image_dir)
    
    save_df = pd.DataFrame(data, columns=headers)
    save_path = os.path.join(target_dir, "labels.csv")
    save_df.to_csv(save_path, index=False)