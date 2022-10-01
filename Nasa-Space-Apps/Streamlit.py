import streamlit as st
from streamlit_image_comparison import image_comparison
import cv2
from main import get_image_uri,stylize_image


st.set_page_config("Journey Through Universe", "🔭")

st.header("Journey Through Universe")

st.write("")
"This is a website for exploring and having fun in the Amazing Space."
st.write("")
title = st.text_input('Start Your Journey here! ')
if(title):

    content_img, style_img = get_image_uri(title)

    st.markdown("### Chosen Pick from Nasa & Style Chosen!")
    image_comparison(
        img1=content_img,
        img2= style_img,
        label1="Content Image",
        label2="Stylish Image",
    )
    print(content_img,style_img)
    
    result_img = stylize_image(content_img,style_img)
    
    if(result_img):

        st.markdown("### Styled Image")
        image_comparison(
            img1=result_img,
            img2=content_img,
            label1="Artificial",
            label2="Original",
        )
