from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="flight_plan_generator",
    version="0.1",
    description="Generate flight plans for dji drones",
    author="Niraj Adhikari",
    author_email="nrjadkry@gmail.com",
    packages=find_packages(),
    license="GPLv3",
    url="https://github.com/nrjadkry/flight-plan-generator",
    install_requires=[],
    keywords=["drone", "flight plan", "waypoints"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: GIS",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Programming Language :: Python :: 3.8",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
)