# ReACT_GCV
Python tool for analyzing images on the Web using the Google Cloud Vision API.


## Installation Instructions
The scripts in this project are written in Python. It is advised to use Anaconda for installing Python. Download Anaconda here: https://repo.anaconda.com/archive/

Clone this repository to your own machine by executing the following command in your terminal:
```git clone https://github.com/rubenros1795/ReACT_GCV.git```

Go to the Anaconda GUI (Graphical User Interface) and create a new environment. In this environment, install Jupyter Notebook.

Also, add the following Python libraries:
- pandas
- os
- bs4
- spacy
- gensim
- htmldate
- langid
- purl
- requests

Try to open Juypter Notebooks in the Anaconda program. If this does not work, go to the terminal and activate the environment:
```conda activate enviornment_name```

Then, open Jupyter Notebooks:
```jupyter notebook```

--------------------

## Working with the Notebooks

When in the Jupyter Notebook environment, navigate to the project folder (called ```ReACT_GCV```) and open the Notebooks subfolder. Start with NB1.

N.B.: if the code won't run because packages are not installed, and if these packages can't be installed in Anaconda, install them with pip. To do this:
  1. Run ```conda create -n venv_name``` and ```conda activate venv_name```, where venv_name is the name of your virtual environment.
  2. Run ```conda install pip```. This will install pip to your venv directory.
  3. Find your anaconda directory, and find the actual venv folder. It should be somewhere like ```/anaconda/envs/venv_name/```.
  4. Install new packages by doing ```/anaconda/envs/venv_name/bin/pip install package_name```.
