from functools import wraps
from time import time
import torch
from torchvision import transforms

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
