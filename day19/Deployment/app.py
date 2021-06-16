# Import Core Packages
import streamlit as st
import altair as alt

# Import EDA Packages
import pandas as pd
import numpy as np

# Utils
import joblib
logreg_pipe = joblib.load(open('models/emotion_classifier_logreg.pkl', 'rb'))

# Function


def predict_emotions(texts):
    results = logreg_pipe.predict([texts])
    return results[0]


def get_prediction_probability(texts):
    results = logreg_pipe.predict_proba([texts])
    return results


# Declaring Emojies
emotions_emojies_dict = {"anger": "😠", "disgust": "🤮", "fear": "😨😱", "happy": "🤗",
                         "joy": "😂", "neutral": "😐", "sad": "😔", "sadness": "😔", "shame": "😳", "surprise": "😮"}


def main():
    st.title('Emotion Classifier App')
    menu = ['Home', 'Monitor', 'About']
    choice = st.sidebar.selectbox('Menu', menu)

    if choice == 'Home':
        st.subheader('Simple Predict-Emotion From Text')

        with st.form(key='emotion_clf_form'):
            raw_text = st.text_area('Write Here')
            submit_text = st.form_submit_button(label='Submit')

        if submit_text:
            col1, col2 = st.beta_columns(2)

            # Apply function Here
            predictions = predict_emotions(raw_text)
            probability = get_prediction_probability(raw_text)

            with col1:
                st.success('Original Text')
                st.write(raw_text)

                st.success('Predictions')
                emoji_icon = emotions_emojies_dict[predictions]
                st.write("{} : {}".format(predictions, emoji_icon))
                st.write("Confidence : {}".format(np.max(probability)))

            with col2:
                st.success('Predictions Probability')
                df_probability = pd.DataFrame(
                    probability, columns=logreg_pipe.classes_)
                df_probability_clean = df_probability.T.reset_index()
                df_probability_clean.columns = ['emotions', 'probability']

                fig = alt.Chart(df_probability_clean).mark_bar().encode(
                    x='emotions', y='probability', color='emotions')
                st.altair_chart(fig, use_container_width=True)

    elif choice == 'Monitor':
        st.subheader('Monitor App')
    else:
        st.subheader('About')


if __name__ == '__main__':
    main()
