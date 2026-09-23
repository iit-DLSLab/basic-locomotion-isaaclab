"""Installation script for the 'basic_locomotion_isaaclab' python package."""

import os
import tomllib

from setuptools import setup

# Obtain the extension data from the extension.toml file
EXTENSION_PATH = os.path.dirname(os.path.realpath(__file__))
# Read the extension.toml file
with open(os.path.join(EXTENSION_PATH, "config", "extension.toml"), "rb") as extension_file:
    EXTENSION_TOML_DATA = tomllib.load(extension_file)

# Minimum dependencies required prior to installation
INSTALL_REQUIRES = [
    "psutil==5.9.8",
]

# Compatibility profile for the Isaac Sim 6.1 Python 3.12 environment used by
# this branch. NVIDIA pins several transitive dependencies exactly; installing
# an unconstrained W&B or Jupyter release can otherwise replace them.
ISAACSIM_6_1_WANDB_REQUIRES = [
    "charset-normalizer==3.3.2",
    "click==8.1.7",
    "decorator==5.1.1",
    "idna==3.10",
    "ipython==8.32.0",
    "ipywidgets==8.1.9",
    "newton[sim]==1.5.0",
    "numpy==2.3.1",
    "onnxruntime-gpu==1.26.0",
    "packaging==26.0",
    "protobuf==6.33.6",
    "psutil==5.9.8",
    "requests==2.32.3",
    "sentry-sdk==2.42.1",
    "urllib3==2.7.0",
    "wandb==0.25.1",
]

# Installation operation
setup(
    name="basic_locomotion_isaaclab",
    packages=["basic_locomotion_isaaclab"],
    author=EXTENSION_TOML_DATA["package"]["author"],
    maintainer=EXTENSION_TOML_DATA["package"]["maintainer"],
    url=EXTENSION_TOML_DATA["package"]["repository"],
    version=EXTENSION_TOML_DATA["package"]["version"],
    description=EXTENSION_TOML_DATA["package"]["description"],
    keywords=EXTENSION_TOML_DATA["package"]["keywords"],
    install_requires=INSTALL_REQUIRES,
    extras_require={"wandb": ISAACSIM_6_1_WANDB_REQUIRES},
    license="Apache 2.0",
    include_package_data=True,
    python_requires="==3.12.*",
    classifiers=[
        "Natural Language :: English",
        "Programming Language :: Python :: 3.12",
        "Isaac Sim :: 6.1.0",
    ],
    zip_safe=False,
)
