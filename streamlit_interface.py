import io
from time import time

import streamlit as st

from api import SwAeController
from api.util import find_images, tensor_to_PIL


def get_name(im):
    return im.split("/")[-1][:30]


def set_images():
    st.session_state.images = find_images()


st.set_page_config("SAE: Interactive interface", ":dvd:")


if "SAE" not in st.session_state:
    with st.spinner("Loading model"):
        st.session_state.SAE = SwAeController("mountain_pretrained")

if "images" not in st.session_state:
    st.session_state.images = find_images()

if "STR" not in st.session_state:
    print("reset")
    st.session_state.STR = st.session_state.images[0]

"""
## ✨ Swapping autoencoder
> Interactive interface prototype

"""

st.sidebar.write("## Editing options")
size = st.sidebar.selectbox(
    "Size:", ("128", "256", "512", "640"), format_func=lambda x: f"{x} px", help="Size of the ouput image"
)
st.session_state.SAE.set_size(int(size))
st.session_state.SAE.set_tex(st.session_state.STR)
opt = st.sidebar.slider(
    "Options to load", 3, len(st.session_state.images), help="No. of option images to load for style mix", step=2
)

st.sidebar.write("> Shift any slider to add that image's style to the mix")

Trans, struct = st.columns([1, 2])

with Trans:
    IM = st.selectbox(
        "Structure selection",
        options=find_images(),
        format_func=get_name,
        help="Choose the structure image from the options below",
    )
    st.session_state.STR = IM
    st.session_state.SAE.set_tex(IM)
    st.image(st.session_state.STR, "Orignal Structure Image")


for i, path in enumerate(st.session_state.images):
    if i > int(opt):
        break
    st.sidebar.image(path, width=256)
    alpha = st.sidebar.slider(
        f"Mix with {get_name(path)}",
        0.0,
        2.0,
        step=0.01,
        key=path,
    )
    st.sidebar.write(alpha)
    st.session_state.SAE.mix_style(path, alpha)

btn = st.sidebar.button("Reload Images", on_click=set_images, help="reload known image index")

with struct:
    st.write("_**Transformations**_")
    st.write("Styles mixed with structure")
    for img in st.session_state.SAE.sty_argumentation:
        st.write(f"{get_name(img)} :", st.session_state.SAE.sty_argumentation[img])

with st.spinner():
    start_time = time()
    temp = st.session_state.SAE.compute()
    im = tensor_to_PIL(temp[0])
    st.image(im, output_format="JPEG", use_column_width=True)
    st.write("took ", round(time() - start_time, 5), "secs")


with st.spinner("making export button"):
    output = io.BytesIO()
    im.save(output, format="JPEG")
    st.download_button("Export current edit", output.getvalue(), f"{get_name(st.session_state.STR)}.jpg")


"""
###### Made by Aadarsh srivastav, Abhishek Kumar Saxena and Sumanshu Anand
"""
