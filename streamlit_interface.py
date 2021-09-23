import streamlit as st
from time import time

from api import SwAeController
from api.util import tensor_to_PIL, find_images, key_gen


def get_name(im):
    return im.split("/")[-1][:30].split(".")[0]


if "SAE" not in st.session_state:
    with st.spinner("Loading model"):
        st.session_state.SAE = SwAeController("mountain_pretrained")

if "images" not in st.session_state:
    st.session_state.images = find_images()

if "STR" not in st.session_state:
    print("reset")
    st.session_state.STR = st.session_state.images[0]

"""
## Swapping AE
> Interactive prototype

"""

size = st.sidebar.selectbox("Size:", ("128", "256", "512", "640"))
st.session_state.SAE.set_size(int(size))
st.session_state.SAE.set_tex(st.session_state.STR)


start_time = time()
temp = st.session_state.SAE.compute()


col1, col2 = st.columns([1, 3])

with col1:
    IM = st.selectbox("Structure selection", options=find_images(), format_func=get_name)
    st.session_state.STR = IM
    st.session_state.SAE.set_tex(IM)
    st.image(st.session_state.STR, "Structure Image")

opt = st.sidebar.select_slider("Options", [3, 6, 9])

for i, path in enumerate(st.session_state.images):
    if i > int(opt):
        break
    st.sidebar.image(path, caption=get_name(path), width=256)
    alpha = st.sidebar.slider(
        "alpha",
        0.0,
        2.0,
        step=0.01,
        key=path,
    )
    st.sidebar.write(alpha)
    st.session_state.SAE.mix_style(path, alpha)

with col2:
    st.write("Transformations")
    for img in st.session_state.SAE.sty_argumentation:
        st.write(get_name(img), st.session_state.SAE.sty_argumentation[img])


start_time = time()
temp = st.session_state.SAE.compute()


st.image(tensor_to_PIL(temp[0]), output_format="JPEG", use_column_width=True)

f"""
**took {time()-start_time}sec**
"""
