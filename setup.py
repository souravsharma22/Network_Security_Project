'''Important for packaging and distributing'''

from setuptools import find_packages, setup
from typing import List

def get_requirements()->[str]:

    '''This function will return list of requirements'''

    requirement_list:List[str]=[]
    try:
        with open('requirements.txt','r') as file:
            lines = file.readlines()
            
            for line in lines:
                requirement = line.strip()
                #ignoring empty lines and '-e.'
                if requirement and requirement!= '-e.':
                    requirement_list.append(requirement)
                
    except FileNotFoundError:
        print("File not found (requirements.txt)")

    return requirement_list

setup(
    name="networkSecurity",
    version="0.0.1",
    author="Sourav Sharma",
    author_email="souravbgp2210@gmail.com",
    packages=find_packages(),
    install_requires = get_requirements()
    )