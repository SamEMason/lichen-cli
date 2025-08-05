class Config:
    def __init__(
        self, lichen_dir: str = "lichen", mode: str = "dev", temp_dir: str = "temp"
    ):
        self.mode = mode
        self.lichen_dir = lichen_dir
        self.temp_dir = temp_dir

    def get_lichen_dir(self, filepath: str):
        return f"{self.lichen_dir}/{filepath}"
