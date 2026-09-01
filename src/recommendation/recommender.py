import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics.pairwise import cosine_similarity

def recommend_games(df,feature_matrix,target_appid,top_n=3):
    if target_appid not in df["appid"].values:
        return []

    results=[]
    target_index=df.index[df["appid"]==target_appid][0]

    similarities=cosine_similarity(
        [feature_matrix[target_index]],
        feature_matrix
    )[0]

    for index,game in df.iterrows():
        if game["appid"]==target_appid:
            continue

        similarity=float(similarities[index])
        if similarity<=0:
            continue

        result={
            "appid" : game["appid"],
            "tags": game["tags"],
            "name":game["name"],
            "similarity" : similarity
        }
        results.append(result)

    results=sorted(
        results,
        key = lambda x: x["similarity"],
        reverse=True
    )

    return results[:top_n]

df=pd.read_csv("data/sample/games_sample.csv")
df=df.reset_index(drop=True)

tag_lists=df["tags"].str.split("|")
genre_lists=df["genres"].str.split("|")
feature_lists=genre_lists+tag_lists
mlb=MultiLabelBinarizer()
feature_matrix=mlb.fit_transform(feature_lists)
recommendations=recommend_games(df,feature_matrix,100004)
print(recommendations)



