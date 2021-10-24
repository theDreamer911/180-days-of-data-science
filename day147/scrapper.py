from youtube_comment_scraper_python import *
import pandas as pd

link = input("Youtube links: ")
saved = input("Output name: ")
youtube.open(link)

response = youtube.video_comments()
data = response['body']

df = pd.DataFrame(data)
df.to_csv(saved)
