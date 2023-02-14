#flairの書き方参照
from setuptools import find_packages, setup

with open("requirements.txt") as f:
    required = f.read().splitlines()


setup(
    name="translit_tt",
    version="0.0.1-dev",
    description="Transliteration tool for tatar language",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Yusuke Sakai",
    url="https://github.com/yusuke1997/translit_tt",
    license="MIT",
    install_requires=required,
    include_package_data=True,
    python_requires=">=3.8",
)
