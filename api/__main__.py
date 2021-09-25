import argparse

import matplotlib.pyplot as plt

from api import SwAeController
from api.util import UtitlState, tensor_to_PIL

parser = argparse.ArgumentParser(
    description="Process some images", prog="api", formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
parser.add_argument("--version", action="version", version="%(prog)s 1.0")

parser.add_argument("img1", metavar="Structure", help="Path to Structure one")
parser.add_argument("img2", metavar="Style", help="Path to Style two")

parser.add_argument(
    "--alpha", type=float, help="How to mix style? '0' means 1st image, '1' means 2nd image", default="0.75"
)
parser.add_argument("--model", help="Which model to load?", default="mountain_pretrained")
parser.add_argument("--debug", action="store_true", default=False, help="Print debug output?")

args = parser.parse_args()

UtitlState.debug(args.debug)

SAE = SwAeController(args.model)
SAE.set_size(512)
SAE.set_tex(args.img1)
SAE.mix_style(args.img2, args.alpha)

output_image = tensor_to_PIL(SAE.compute()[0])
plt.imshow(output_image)
plt.axis(False)
plt.show()
