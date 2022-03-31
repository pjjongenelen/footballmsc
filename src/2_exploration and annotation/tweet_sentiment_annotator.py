import pandas as pd

ROOT = "C:/Users/timjo/python_projects/footballmsc"

df = pd.read_csv(f"{ROOT}/data/only_tweets.csv", index_col = [0])

unannotated = df[df.annotation == 0].copy()

indices = []
annotations = []

for index, row in unannotated.iterrows():
    print(row.content)
    annotation = input()
    if annotation == "!":
        break

    indices.append(index)
    annotations.append(annotation)
    print("------------------------------------------------------------")
    print("------------------------------------------------------------")
    print("------------------------------------------------------------")
    print("------------------------------------------------------------")
    print("------------------------------------------------------------")
    print("------------------------------------------------------------")

annotations_df = pd.DataFrame({"index": indices, "annotation": annotations})
df = annotations_df.combine_first(df)

df.to_csv(f"{ROOT}/data/only_tweets.csv")