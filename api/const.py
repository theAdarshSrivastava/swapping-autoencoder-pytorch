from models.swapping_autoencoder_model import SwappingAEConfig
from dataclasses import dataclass


@dataclass
class DatasetConfig:
    checkpoints_dir: str = "./checkpoints/"
    dataset_mode: str = "imagefolder"
    preprocess: str = "scale_shortside"
    name: str = "mountain_pretrained"
    resume_iter: str = "latest"


@dataclass
class Global_config(SwappingAEConfig, DatasetConfig):
    isTrain: bool = False
    num_gpus: int = 1
    netG: str = "StyleGAN2Resnet"
    netD: str = "StyleGAN2"
    netE: str = "StyleGAN2Resnet"
    netPatchD: str = "StyleGAN2"
    use_antialias: bool = True
    crop_size: int = 128
    load_size: int = 128


KNOWN_IMAGE_FORMATS = ["jpeg", "jpg"]
