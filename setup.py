from setuptools import find_packages, setup

metadata = dict(
    name="computer_vision_utils",
    packages=find_packages(),
    install_requires=["numpy", "opencv-python", "matplotlib"],
)

setup(**metadata)