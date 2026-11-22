from setuptools import setup

package_name = "mobrob_v05"

setup(
    name=package_name,
    version="1.0.0",
    packages=[package_name],
    data_files=[
        ("share/ament_index/resource_index/packages",
            ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Marina Banov",
    maintainer_email="marina.banov@uniri.hr",
    description="Package containing multiple ROS2 OpenCV examples.",
    license="GNU GPLv3",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "color_thresholding = mobrob_v05.01_color_thresholding:main",
            "edge_detection = mobrob_v05.02_edge_detection:main",
            "feature_matching = mobrob_v05.03_feature_matching:main",
            "video_player = mobrob_v05.04_video_player:main",
            "people_detection = mobrob_v05.05_people_detection:main",
            "face_detection = mobrob_v05.06_face_detection:main",
            "object_recognition = mobrob_v05.07_object_recognition:main",
        ],
    },
)
