from setuptools import find_packages, setup

setup(
    name="knihovna",
    version="1.0.0",
    description="Hledání nejkratší cesty v bludišti a generování bludišť.",
    packages=find_packages(),
    install_requires=["numpy", "scipy", "matplotlib"],
)
