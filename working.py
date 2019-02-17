import pandas as pd
import numpy

tedData = pd.read_csv('ted_data.csv')

print(tedData)

description = tedData['description']
speaker = tedData['main_speaker']
name = tedData['name']
occupation = tedData['speaker_occupation']
title = tedData['title']
transcript = tedData['transcript']