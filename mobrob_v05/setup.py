from setuptools import setup
import os
from glob import glob

package_name = "mobrob_v05"

setup(
    name=package_name,
    version="1.0.0",
    packages=[package_name],
    data_files=[
        ("share/ament_index/resource_index/packages",
            ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        (os.path.join("share", package_name, "launch"), glob("launch/*.launch.py")),
        (os.path.join("share", package_name, "models"), glob("models/*")),
        (os.path.join("share", package_name, "rviz"), glob("rviz/*.rviz")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Diego Susanj",
    maintainer_email="dsusanj@riteh.hr",
    description="Adding pillar to Gazebo from RViz",
    license="GNU GPLv3",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "mobrob_v05 = mobrob_v05.mobrob_v05:main",
        ],
    },
)
