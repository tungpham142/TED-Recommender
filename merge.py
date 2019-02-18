import pandas as pd

file1 = pd.read_csv("ted_main.csv")
file2 = pd.read_csv("transcripts.csv")

file3 = file1.merge(file2, on="url", how="outer")

file3.to_csv("ted_data.csv")