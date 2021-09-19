from .const import Global_config


class Api:
    def __init__(self, name: str) -> None:
        opt = Global_config(isTrain=False, name=name)
