import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics.pairwise import cosine_similarity

def recommend_games(
        df,
        genre_matrix,
        tag_matrix,
        target_appid,
        top_n=3,
        genre_weight=0.3,
        tag_weight=0.7,
):
    if abs(genre_weight+tag_weight-1.0) > 1e-9:
        return []
    if target_appid not in df["appid"].values:
        return []

    results=[]
    target_index=df.index[df["appid"]==target_appid][0]

    genre_similarities=cosine_similarity(
        [genre_matrix[target_index]],
        genre_matrix
    )[0]

    tag_similarities = cosine_similarity(
        [tag_matrix[target_index]],
        tag_matrix
    )[0]

    for index,game in df.iterrows():
        if game["appid"]==target_appid:
            continue

        genre_similarity=float(genre_similarities[index])
        tag_similarity = float(tag_similarities[index])


        similarity=(
            genre_weight*genre_similarity
            +tag_weight*tag_similarity
        )

        if similarity<=0 :
            continue

        result={
            "appid" : game["appid"],
            "name":game["name"],
            "tags": game["tags"],
            "genres":game["genres"],
            "genre_similarity":genre_similarity,
            "tag_similarity":tag_similarity,
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
tag_mlb=MultiLabelBinarizer()
tag_matrix=tag_mlb.fit_transform(tag_lists)

genre_lists=df["genres"].str.split("|")
genre_mlb=MultiLabelBinarizer()
genre_matrix=genre_mlb.fit_transform(genre_lists)

recommendations=recommend_games(
    df,
    genre_matrix,
    tag_matrix,
    100010,
    genre_weight=0.3,
    tag_weight=0.7
)
print(recommendations)



