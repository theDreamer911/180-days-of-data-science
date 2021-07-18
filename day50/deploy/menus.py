from google.protobuf import message
from urlextract import URLExtract
from collections import Counter
from wordcloud import WordCloud
import pandas as pd
import emoji

extract = URLExtract()


def fetch_stats(selected_user, df):

    if selected_user != 'Show All':
        df = df[df['user'] == selected_user]

    # 1. Feth number of message
    num_messages = df.shape[0]

    # 2. Fetch total number of words
    words = []
    [words.extend(message.split()) for message in df['message']]

    # 3. Fetch number of media messages
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0] or df[df['message']
                                                                                 == '<Media tidak disertakan>\n'].shape[0]

    # 4. Fetch number of links shared
    links = []
    [links.extend(extract.find_urls(message)) for message in df['message']]

    return num_messages, len(words), num_media_messages, len(links)


def most_talk_active_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts()/df.shape[0])*100,
               2).reset_index().rename(columns={'index': 'name', 'user': 'percent'})
    df = df[df['name'] != 'group_notification']
    return x, df


def create_wordcloud(selected_user, df):
    if selected_user != 'Show All':
        df = df[df['user'] == selected_user]

    df = df[df['message'] != '<Media omitted>\n']
    df = df[df['message'] != '<Media tidak disertakan>\n']

    wcloud = WordCloud(width=500, height=500,
                       background_color='white')
    df_wcloud = wcloud.generate(df['message'].str.cat(sep=" "))

    return df_wcloud


def most_common_words(selected_user, df):

    f = open('stop_id-eng.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Show All':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    temp = temp[temp['message'] != '<Media tidak disertakan>\n']

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(5))

    return most_common_df


def common_emoji(selected_user, df):
    if selected_user != 'Show All':
        df = df[df['user'] == selected_user]

    emojis = []

    [emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])
     for message in df['message']]

    most_emoji = pd.DataFrame(
        Counter(emojis).most_common(len(Counter(emojis))))
    return most_emoji


def monthly_timeline(selected_user, df):
    if selected_user != 'Show All':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()[
        'message'].reset_index()

    time = []

    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline


def daily_timeline(selected_user, df):
    if selected_user != 'Show All':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline


def week_activity_map(selected_user, df):
    if selected_user != 'Show All':
        df = df[df['user'] == selected_user]

    activity_time = df['day_name'].value_counts()

    return activity_time


def month_activity_map(selected_user, df):
    if selected_user != 'Show All':
        df = df[df['user'] == selected_user]

    month_activy = df['month'].value_counts()

    return month_activy


def activity_heatmap(selected_user, df):
    if selected_user != 'Show All':
        df = df[df['user'] == selected_user]

    activity_mapper = df.pivot_table(
        index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return activity_mapper


# Usseless now
    # if selected_user == 'Show All':
    #     # 1. Fetching number of message
    #     num_messages = df.shape[0]
    #     # 2. Number of words
    #     words = []
    #     [words.extend(message.split()) for message in df['message']]
    #     return num_messages, len(words)
    # else:
    #     new_df = df[df['user'] == selected_user]
    #     # 1. Fetching number of message
    #     num_messages = new_df.shape[0]
    #     # 2. Number of words
    #     words = []
    #     [words.extend(message.split()) for message in new_df['message']]
    #     return num_messages, len(words)
