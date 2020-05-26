## ReACT_GCV
Python tool for analyzing images on the Web using the Google Cloud Vision API.


# Installation Instructions
The scripts in this project are written in Python. It is advised to use Anaconda for installing Python. Download Anaconda here: https://repo.anaconda.com/archive/

Clone this repository to your own machine by executing the following command in your terminal:
```git clone https://github.com/rubenros1795/ReACT_GCV.git```

Navigate to the cloned directory (use ```cd```) and create a new Python environment by using Anaconda. To do this, execute:
```conda create -n new_environment --file requirements.txt``` (replace new_environment by a custom name)

Alternatively, go to the Anaconda GUI (Graphical User Interface) and create an environment. 

Add the following Python libraries:
- pandas
- os
- bs4
- spacy
- gensim
- htmldate
- langid
- purl
- requests

This can be done with the command ```conda install -n <env_name> <package>```

Activate the environment in Anaconda or using your terminal (replace new_environment with the name given to your environment)

```conda activate new_environment```
