"""
Created at: 2023-12-19
Author: Gao Tianchi
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ROOT: Path = Path(__file__).parent.parent

if sys.platform.startswith("win"):
    PREFIX = "sqlite:///"
else:
    PREFIX = "sqlite:////"


class BaseConfig:
    SECRET_KEY: str = ROOT.joinpath("secret_key").read_text()
    PATH_ROOT: Path = ROOT
    PATH_LOG: Path = ROOT.joinpath("log")
    PATH_TEMPLATE: Path = ROOT.joinpath(__package__, "view", "templates")
    PATH_STATIC: Path = ROOT.joinpath(__package__, "view", "static")

    MAXIMUM_ACCESS_FREQUENCY: int = 60


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = PREFIX + str(ROOT.joinpath("data", "dev.db"))


class TestingConfig(BaseConfig):
    ...


class ProductionConfig(BaseConfig):
    ...


def get_config(environment: str = None):
    environment = environment if environment else os.getenv("FLASK_ENV")
    match environment:
        case "production":
            return ProductionConfig
        case "testing":
            return ProductionConfig
        case _:
            return DevelopmentConfig
