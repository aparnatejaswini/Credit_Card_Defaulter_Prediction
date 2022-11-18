from setuptools import setup, find_packages


PROJECT_NAME = "CREDIT CARD DEFAULTER PREDICTION"
VERSION = "0.0.1"
DESCRIPTION = "Given customer information, the developed model should be able to predict if customer defaults on credit card payment or not."
AUTHOR = "Aparna T Parkala"


def get_requirements_list()->list:
    """
        Returns list of libraries mentioned in requirements.txt file
    """
    with open("requirements.txt") as require_fobj:
        return require_fobj.readlines()


setup(name=PROJECT_NAME, 
      version=VERSION,
      description=DESCRIPTION,
      author=AUTHOR,
      packages=find_packages(),
      install_requires=get_requirements_list()
      )