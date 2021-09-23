import os
from functools import wraps
from time import time
from typing import List
import random

import torch
from torchvision import transforms

from api.const import KNOWN_IMAGE_FORMATS

tabs = -1
ON = True


def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        global tabs, ON
        tabs += 1
        if ON:
            print(f"{'  '*tabs}|" if tabs else "", f"[ST] func:{f.__name__}")
        ts = time()
        result = f(*args, **kw)
        te = time()
        args_str = [str(ag)[-20:] for ag in args]
        message = (
            f"{'  '*tabs}|" if tabs else ""
        ) + f" [ED] func:{f.__name__}\t\ttook: {round(te-ts, 8)}\targs:[{args_str}, {kw}] sec"
        tabs -= 1
        if ON:
            print(message)
        return result

    return wrap


def tensor_to_PIL(im: torch.Tensor):
    return transforms.ToPILImage()((im.clamp(-1.0, 1.0) + 1.0) * 0.5)


def find_images(folder: str = None) -> List:
    it = os.walk(folder or "./testphotos/mountain/fig12")
    result = []
    for path, _, imgs in it:
        if len(imgs) > 0:
            img_folder = [path + "/" + img for img in imgs if img.split(".")[-1] in KNOWN_IMAGE_FORMATS]
        result.extend(img_folder)
    return result


def key_gen():
    return "".join([random.choice("abhishek") for i in range(5)])
