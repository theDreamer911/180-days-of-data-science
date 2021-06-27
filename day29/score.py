
import tensorflow as tf 
from io import BytesIO
import streamlit as st
from PIL import Image
import numpy as np 
import requests

st.set_option('deprecation.showfileUploaderEncoding', False)
st.title('Bean Spot Image Classifier')
st.text('Provide URL for Image Classification')

@st.cache(allow_output_mutation=True)
def load_model():
    model = tf.keras.models.load_model('./beans_spot.tf')
    return model

with st.spinner("Lodading Model into Memory..."):
    model = load_model()

classes = ['angular_leaf_spot', 'bean_rust', 'healthy']

def scale(image):
    image = tf.cast(image, tf.float32)
    image = image/255

    return tf.image.resize(image, [224,224])

def decode_img(image):
    img = tf.image.decode_jpeg(image, channels=3)
    img = scale(img)
    return np.expand_dims(img, axis=0)

path = st.text_input('Enter Image URL for Classification...','http://barmac.com.au/wp-content/uploads/sites/3/2016/01/Angular-Leaf-Spot-Beans1.jpg')
if path is not None:
    content = requests.get(path).content 

    st.write('Predicted Class:')
    with st.spinner("Classifying..."):
        label = np.argmax(model.predict(decode_img(content)), axis=1)
        st.write(classes[label[0]])
    st.write('')
    image = Image.open(BytesIO(content))
    st.image(image, caption='Classifying Bean Spot Image', use_column_width=True)
