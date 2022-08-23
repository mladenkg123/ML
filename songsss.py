import pandas as pd
import  re
from operator import contains
from sklearn.metrics.pairwise import sigmoid_kernel

df=pd.read_csv("SongCSV.csv")
feature_cols=['Danceability', 'Duration', 'Energy', 'KeySignature', 'Loudness', 'Mode',
              'Tempo', 'TimeSignature']

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
normalized_df =scaler.fit_transform(df[feature_cols])

indices = pd.Series(df.index, index=df['Title']).drop_duplicates()

sig_kernel = sigmoid_kernel(normalized_df)

def generate_recommendation(song_title, model_type=sig_kernel):

    score=list(enumerate(model_type[indices[song_title]]))

    similarity_score = sorted(score,key = lambda x:x[1],reverse = True)

    similarity_score = similarity_score[1:11]
    top_songs_index = [i[0] for i in similarity_score]

    top_songs=df['Title'].iloc[top_songs_index]
    top_songs_cleaned=[]
    for song in top_songs:
        song = song.replace('"', '')
        song = song.replace("'", '')
        top_songs_cleaned.append(song[1::])
    return top_songs_cleaned
title_list=[]
title="b"+input("Ukucajte naslov pesme\n")
for mtitle in indices.items():
    if re.search(title, mtitle[0], re.IGNORECASE):
        title_list.append(mtitle[0][1::])
while len(title_list)<1:
    print("Nema rezultata pokusajte ponovo\n")
    title="b"+input("Ukucajte naslov pesme\n")
    for mtitle in indices.items():
        if re.search(title, mtitle[0], re.IGNORECASE):
            title_list.append(mtitle[0][1::])
for index, value in enumerate(title_list):
    value = value.replace('"', '')
    value = value.replace("'", '')
    print(index+1, value)
broj=input("Ukucajte  broj pesme\n")
while not broj.isnumeric() or int(broj)>len(title_list):
    print("Unos nije broj ili je veci od indeksa pokusajte ponovo")
    broj=input("Ukucajte  broj pesme\n")
print("Preporucene pesme:")
lista_pesama=generate_recommendation("b" + title_list[int(broj)-1],sig_kernel)
for index, value in enumerate(lista_pesama):
    print(index+1, value)
