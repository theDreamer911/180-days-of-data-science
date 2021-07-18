import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns
import preprocessor
import menus

st.sidebar.title("Whatsapp Chat Analyzer")
st.sidebar.caption("Rebuild by theDreamer911")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    # st.text(data)
    df = preprocessor.preprocess(data)

    # st.dataframe(df)

    # fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Show All")

    selected_user = st.sidebar.selectbox("Choose the sender", user_list)

    if st.sidebar.button("Show Analysis"):

        num_messages, words, num_media_messages, num_links = menus.fetch_stats(
            selected_user, df)

        # Basic Information
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.beta_columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(num_links)

        # Monthly timeline
        st.title("Monthly Timeline")
        timeline = menus.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='red')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Daily timeline
        st.title("Daily Timeline")
        daily_timeline = menus.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'],
                daily_timeline['message'], color='black')
        plt.xticks(rotation=30)
        st.pyplot(fig)

        # Activity Mapper
        st.title("Activity Mapper")
        col1, col2 = st.beta_columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day = menus.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='green')
            plt.xticks(rotation=30)
            st.pyplot(fig)
        with col2:
            st.header("Most Busy Month")
            busy_month = menus.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation=30)
            st.pyplot(fig)

        # Activity Heatmap
        st.title("Weekly Activity Mapper")
        activity_mapper = menus.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(activity_mapper)
        st.pyplot(fig)

        # Five Most Talk Active Users (Group Level)
        if selected_user == 'Show All':
            st.title("Most Talkactive User")
            df = df[df['user'] != 'group_notification']
            x, new_df = menus.most_talk_active_users(df)
            fig, ax = plt.subplots(figsize=(10, 8))

            col1, col2 = st.beta_columns(2)

            with col1:
                ax.bar(x.index, x.values, color='blue')
                plt.xticks(rotation=30)
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # Make wordcloud
        st.title('Wordcloud')
        df_wcloud = menus.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wcloud)
        st.pyplot(fig)

        # Most common words
        most_common_df = menus.most_common_words(selected_user, df)

        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        ax.invert_yaxis()

        st.title('Most common words')
        st.pyplot(fig)

        # Most common emoji
        emoji_df = menus.common_emoji(selected_user, df)
        st.title('Most Common Emoji')

        col1, col2 = st.beta_columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(),
                   labels=emoji_df[0].head(), autopct="%0.2f")
            st.pyplot(fig)

st.sidebar.caption(
    '[My Source Code](https://github.com/theDreamer911/180-days-of-data-science/tree/main/day50)')
