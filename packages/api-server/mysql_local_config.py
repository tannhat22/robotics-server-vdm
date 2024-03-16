from os.path import dirname

from api_server.default_config import config

here = dirname(__file__)
run_dir = f"{here}/run"


config.update(
    {
        "db_url": "mysql+pymysql://root:tannhatamr@127.0.0.1:3306/amrvdmdatabase",
        "cache_directory": f"{run_dir}/cache",  # The directory where cached files should be stored.
    }
)
