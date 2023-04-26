from setuptools import setup, find_packages

setup(
    name="taqo_webapp",
    version="1.0.0",
    packages=find_packages("taqo_webapp", exclude=["*tests"]),
    package_dir={"": "taqo_webapp"},
    install_requires=[
        "dash",
        "dash_bootstrap_components",
        "dash_mantine_components",
    ],
    entry_points={
        'console_scripts': [
            'taqo = webapp:run',
        ]
    }
)
