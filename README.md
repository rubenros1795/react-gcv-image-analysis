# ReACT_GCV
Python tool for analyzing images on the Web using the Google Cloud Vision API. 

Clone this repository to your own machine by executing the following command in your terminal:
```git clone https://github.com/rubenros1795/ReACT_GCV.git``` or download and unzip the repo (top-right corner).


## Installation Guide 
The Notebooks found in the ```/notebooks``` folder require a Pyton installation. In this step-by-step installation guide we explain how to install Anaconda, a Python distribution, and create a virtual environment. 

_Installing_
1. Download Anaconda here: https://repo.anaconda.com/archive/ or through here: https://docs.anaconda.com/anaconda/install/

2. Install Anaconda, for detailed guides see: https://docs.anaconda.com/anaconda/install/

_Creating a Virtual Environment_

Anaconda installs Python on the system (it is a Python distribution). To run scripts and notebooks it is advised to create a so-called "virtual environment" (VE) for your project. Below we show how to create a VE.

3. Go to the terminal. On Windows you will find it as ```cmd``` (search in the bottom-right corner), on Mac and Linux simply as "terminal" in the application overview.

4. Check if you succesfully installed Anaconda by typing ```conda -v``` and pressing ```Enter``` to execute the terminal command.

5. Create an environment by executing ```conda create -n yourenvname```. This creates a new VE in the ```anaconda3/envs/``` folder.

6. Activate the environment by executing ```conda activate yourenvname```.

_Installing Libraries_

7. In order to use the notebooks in this repository, we need several seconday Python libraries. These are found in the ```requirements.txt``` file. To install the libraries, navigate to the ReACT_GCV folder in the terminal (N.B.: activate the VE first!). Once you are in the right folder, execute ```conda install --file requirements.txt```.

8. Here the trouble starts. Some libaries are not available in the Anaconda channel (the list of libraries that Anaconda knows). To install the missing libaries, first install pip, a Python "librarian".
- Windows: see the instructions here: https://www.liquidweb.com/kb/install-pip-windows/.
- Linux: sudo apt install python-pip.
- Mac: ```sudo easy_install pip```.

9. Install the missing libraries by executing ```pip install libraryname``` (for example: ```pip install purl```).

_Opening Jupyter Notebooks_

10. Open Jupyter Notebooks by simply executing ```jupyter notebook```. Navigate to the ```/notebooks``` folder and open the ```.ipynb``` file.
