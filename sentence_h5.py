import pandas as pd
import random

dataset_path = 'dataUji.tsv'
df = pd.read_csv(dataset_path, sep='\t', header=None, names=['num_eng', 'sent_eng', 'num_indo', 'sent_indo'])

def get_random_question(language):
    if language == 'inggris':
        filtered_df = df[(df['sent_eng'].str.split().apply(len) > 3) & (df['sent_eng'].str.len() > 0)]
        index = random.choice(filtered_df.index)
        return filtered_df['sent_indo'][index], filtered_df['sent_eng'][index]

    elif language == 'indonesia':
        filtered_df = df[(df['sent_indo'].str.split().apply(len) > 3) & (df['sent_indo'].str.len() > 0)]
        index = random.choice(filtered_df.index)
        return filtered_df['sent_eng'][index], filtered_df['sent_indo'][index]
