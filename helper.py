import pandas as pd
from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import emoji

def fetch_stats(selected_user,df):

    extractor = URLExtract()


    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    #fetch number of messages
    num_messages = df.shape[0]

    #fetch number of words
    words = []
    for msg in df['message']:
        words.extend(msg.split())

    #fetch number of media messages
    num_media = df[df['message'] == '<Media omitted>\n'].shape[0]

    #fetch urls
    links = []
    for msg in df['message']:
        links.extend(extractor.find_urls(msg))

    return num_messages, len(words), num_media, len(links)


def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0])*100, 2).reset_index().rename(columns={'index':'name','user':'percent'})
    return x,df


def createWordcloud(selected_user , df):
    # Getting stop words
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Remove group notification
    temp = df[df['user'] != 'group_notification']

    # Remove media omitted messages
    temp = temp[temp['message'] != '<Media omitted\n>']
    temp = temp[temp['message'] != '<media omitted\n>']

    def remove_stop_words(message):
        words = []
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
        return " ".join(words)

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc


def most_common_words(selected_user , df):

    # Getting stop words
    f = open('stop_hinglish.txt' , 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Remove group notification
    temp = df[df['user'] != 'group_notification']

    # Remove media omitted messages
    temp = temp[temp['message'] != '<Media omitted\n>']
    temp = temp[temp['message'] != '<media omitted>']

    words = []

    # Removing stop words
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    # Most used words can be found using counter
    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df


def emoji_helper(selected_user , df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for msg in df['message']:
        emojis.extend([c for c in msg if c in emoji.UNICODE_EMOJI['en']])
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df


def monthly_timeline(selected_user , df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year' , 'month_num' , 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time

    return timeline


def daily_timeline(selected_user , df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline

def week_activity_map(selected_user , df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user , df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user , df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name' , columns='period' , values='message' , aggfunc='count').fillna(0)
    return user_heatmap