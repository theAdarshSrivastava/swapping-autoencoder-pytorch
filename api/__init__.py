from collections import OrderedDict
from typing import Dict, Tuple, Union

import torch
import torchvision
from data.base_dataset import get_transform
from models.swapping_autoencoder_model import SwappingAutoencoderModel
from PIL import Image

from api.const import Global_config
from api.util import timing


class SwAeController:
    load_size: int = -1
    transform: Union[torchvision.transforms.Compose, None] = None
    global_sty: Union[torch.Tensor, None] = None
    global_tex: Union[torch.Tensor, None] = None
    cache: Dict = {}
    sty_argumentation: OrderedDict = OrderedDict()

    @timing
    def __init__(self, name: str) -> None:
        self.opt = Global_config(isTrain=False, name=name)
        self.model = SwappingAutoencoderModel(self.opt)
        self.model.initialize()

    @timing
    def _get_transform(self) -> torchvision.transforms.Compose:
        kwarg = {}
        if self.load_size != -1:
            kwarg["load_size"] = self.load_size
        return get_transform(self.opt, **kwarg)

    @timing
    def set_size(self, size: int):
        if size < 0:
            raise ValueError("Can not set negetive size")
        self.load_size = size

        # need to reload transforms with new size
        self.transform = self._get_transform()

    @timing
    def load_image(self, path) -> torch.Tensor:
        img = Image.open(path).convert("RGB")
        if self.transform == None:
            self.transform = self._get_transform()
        tensor = self.transform(img).unsqueeze(0)
        return tensor

    @timing
    def set_tex(self, tex_path):
        source = self.load_image(tex_path).to("cuda")
        with torch.no_grad():
            self.model(sample_image=source, command="fix_noise")
            self.global_tex, self.global_sty = self.encode(source)

    @timing
    def encode(self, im: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        with torch.no_grad():
            tex, sty = self.model(im.to("cuda"), command="encode")
            im = im.to("cpu")
        return tex.to("cpu"), sty.to("cpu")

    @timing
    def load_encode_cache(self, path: str) -> Tuple[torch.Tensor, torch.Tensor]:
        if path in self.cache:
            return self.cache[path]
        im = self.load_image(path)
        tex, sty = self.encode(im)
        self.cache[path] = tex, sty
        return tex, sty

    @timing
    def mix_style(self, style_path, alpha):
        if style_path not in self.cache:
            tex, sty = self.load_encode_cache(style_path)
        # assume alpha has changed if same path is sent
        self.sty_argumentation[style_path] = alpha

    @timing
    def compute(self):
        assert self.global_sty != None and self.global_tex != None
        local_sty = self.global_sty.clone().to("cuda")
        for path, alpha in self.sty_argumentation.items():
            cached_sty = self.cache[path][1].clone().to("cuda")
            local_sty = self.lerp(local_sty, cached_sty, alpha)
            cached_sty = cached_sty.to("cpu")
        with torch.no_grad():
            out = self.model(self.global_tex.to("cuda"), local_sty, command="decode")
        local_sty.to("cpu")
        return out

    @staticmethod
    @timing
    def lerp(source: torch.Tensor, target: torch.Tensor, alpha: int) -> torch.Tensor:
        return source * (1 - alpha) + target * alpha
