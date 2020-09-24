import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="screenbreak",
    version="0.0.6.9",
    author="Gytha Ogg",
    author_email="gythaoggscat@gmail.com",
    description="Screenbreak",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://https://github.com/gythaogg/screenbreak",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Linux",
    ],
    entry_points={'console_scripts': ['screenbreak = screenbreak.work:main']},
)
