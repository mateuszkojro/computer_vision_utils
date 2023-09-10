from setuptools import find_packages, setup

metadata = dict(
    name="computer_vision_utils",
    version="0.1.1",
    packages=["computer_vision_utils"],
    install_requires=["numpy", "opencv-python", "matplotlib"],
)

setup(**metadata)
