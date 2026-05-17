import pickle
import streamlit as st
import cv2
import numpy as np
import pandas as pd

img_src, img_dst = pickle.load(open("frames.pkl", "rb"))

def _make_mask(img):
    mask = ~cv2.inRange(img, (0, 0, 0), (black_thr, black_thr, black_thr))
    mask = cv2.medianBlur(mask, median_kernel_size)
    return mask

def _show_hist(img):
    df = []
    colors = ('b','g','r')
    for i,color in enumerate(colors):
        histr = cv2.calcHist([img],[i],None,[256],[0,256]).ravel()
        df.append(pd.DataFrame({"x": range(0, 256), "y": histr, "color": color}))
    df = pd.concat(df, axis = 0)
    st.line_chart(df, x = "x", y = "y", color = "color")


def _st_image_show(*img):
    stacked = np.concatenate(img, axis = 1)
    stacked = cv2.cvtColor(stacked, cv2.COLOR_BGR2RGB)
    st.image(stacked)


black_thr = st.number_input(
    label="Black Thr:",
    min_value = 0,
    max_value=255,
    value=130,
    step=1,
    format="%d"
)

diff_thr = st.number_input(
    label="Diff Thr:",
    min_value = 0,
    max_value=255,
    value=50,
    step=1,
    format="%d"
)

median_kernel_size = st.number_input(
    label="Median Kernel Size:",
    min_value = 0,
    max_value = 30,
    value=3,
    step=2,
    format="%d"
)

_show_hist(img_src)
_show_hist(img_dst)

overlapped = np.stack((np.zeros_like(img_src[:, :, 0]), _make_mask(img_src), _make_mask(img_dst)), axis = -1)

difference = np.abs(img_src.astype(np.int32) - img_dst).mean(axis = -1).astype(np.uint8)

diff1 = difference.copy()
diff1[diff1 < diff_thr] = 0
diff1 = np.stack([diff1] * 3, axis = -1)

diff2 = difference.copy()
diff2[~overlapped.any(axis = -1)] = 0
diff2 = np.stack([diff2] * 3, axis = -1)

_st_image_show(img_src, img_dst, overlapped)
_st_image_show(diff1, diff2)