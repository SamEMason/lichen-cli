import pytest
from pathlib import Path
import shutil
from lichen.config import Config


@pytest.fixture()
def global_cleanup():
    config = Config()
    output_dir = Path(config.temp_dir)
    if output_dir.exists():
        shutil.rmtree(output_dir)

    yield output_dir

    if output_dir.exists():
        shutil.rmtree(output_dir)
