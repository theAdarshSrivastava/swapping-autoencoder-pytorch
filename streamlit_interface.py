import streamlit as st
import random
from streamlit.caching import cache
from streamlit_drawable_canvas import st_canvas

"""
# Swapping AE
> Hope this works for the time being
"""

IMG1 = "testphotos/mountain/fig12/structure/snow-grass.jpg"
IMG2 = "testphotos/mountain/fig12/structure/house.jpg"
IMG3 = "testphotos/mountain/fig12/style/lake-2.jpg"


from api import SwAeController
from api.util import tensor_to_PIL

if "SAE" not in st.session_state:
    st.session_state.SAE = SwAeController("mountain_pretrained")
    num = 512
    st.session_state.SAE.set_size(num)
    st.write("reloading controler")

if "STR" not in st.session_state:
    st.session_state.STR = IMG1

if "TEX" not in st.session_state:
    st.session_state.TEX = IMG2

st.write(dir(st.session_state.SAE))
st.write(st.session_state.SAE.cache)


size = st.selectbox("Size:", ("128", "256", "512"))

st.write(size)

st.session_state.SAE.set_size(int(size))

st.session_state.SAE.set_tex(st.session_state.STR)


if "alpha" not in st.session_state:
    st.session_state.alpha = 0

if "output_image" not in st.session_state:
    temp = st.session_state.SAE.compute()
    st.session_state.output_image = tensor_to_PIL(temp[0])


st.session_state.alpha = st.slider("alpha", 0.0, 2.0, step=0.01)

st.session_state.SAE.mix_style(st.session_state.TEX, st.session_state.alpha)

from time import time

start_time = time()
temp = st.session_state.SAE.compute()

f"""
**took {time()-start_time}sec**
"""
st.session_state.output_image = tensor_to_PIL(temp[0])


# canvas_result = st_canvas(
#     key="canvas",
# )

# st.write(canvas_result)
st.image(st.session_state.output_image, output_format="JPEG", use_column_width=True)


def change_structure(IM):
    st.session_state.STR = IM
    st.session_state.SAE.set_tex(IM)


def change_texture(IM):
    st.session_state.alpha = 0
    st.session_state.TEX = IM


col1, col2 = st.columns(2)


def key_gen():
    return "".join([random.choice("abhishek") for i in range(5)])


def get_name(im):
    return im.split("/")[-1][:30]


with col1:
    st.image(st.session_state.STR, "Structure Image")

with col2:
    st.image(st.session_state.TEX, "Style Image")

ButCol1, ButCol2 = st.columns(2)

with ButCol1:
    st.button(get_name(IMG1), on_click=change_structure, args=(IMG1,))
    st.button(get_name(IMG2), on_click=change_structure, args=(IMG2,))
    st.button(get_name(IMG3), on_click=change_structure, args=(IMG3,))

with ButCol2:
    st.button(get_name(IMG1), key=key_gen(), on_click=change_texture, args=(IMG1,))
    st.button(get_name(IMG2), key=key_gen(), on_click=change_texture, args=(IMG2,))
    st.button(get_name(IMG3), key=key_gen(), on_click=change_texture, args=(IMG3,))

st.write(st.session_state.SAE.sty_argumentation)
