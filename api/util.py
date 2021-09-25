import os
import random
from dataclasses import dataclass
from functools import wraps
from time import time
from typing import List

import torch
from torchvision import transforms

from api.const import KNOWN_IMAGE_FORMATS


class UtitlState:
    tabs = -1
    isON = True

    @classmethod
    def debug(cls, isON: bool):
        cls.isON = isON
        return cls

    @classmethod
    def add_tab(cls):
        cls.tabs += 1
        return cls

    @classmethod
    def remove_tab(cls):
        cls.tabs -= 1
        return cls


def timing(f):
    def print_if_dubug(*args, **kw):
        """
        print output if debug is on.
        """
        if UtitlState.isON:
            print(*args, **kw)

    def print_tabs(msg: str):
        tabs_msg = f" {'  '*UtitlState.tabs} | " if UtitlState.tabs else ""
        return f"{tabs_msg} {msg}"

    @wraps(f)
    def wrap(*args, **kw):
        UtitlState.add_tab()
        args_str = ", ".join([str(ag).replace("\n", " ")[-50:] for ag in args])
        print_if_dubug(
            print_tabs(
                f"[STA] func:{f.__name__}\t \targs:[{args_str}, {kw}]",
            )
        )

        ts = time()
        try:
            result = f(*args, **kw)
        except Exception as e:
            print_if_dubug(print_tabs(f"[ERR] XxXx"))
            UtitlState.remove_tab()
            raise e
        te = time()

        print_if_dubug(
            print_tabs(
                f"[END] func:{f.__name__}\t \ttook: {round(te-ts, 8)}sec",
            )
        )
        UtitlState.remove_tab()
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
