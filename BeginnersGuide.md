# A Beginners Guide to Working with Web Data in Python

## The Goal
Web data provides great insights in online visual culture. This guide describes the first steps in working with web data in Python. Web data is understood here as information drawn from the Internet in the form of web pages (usually .html files) and their associated metadata such as the language of the webpage and its date of publication. The guide discusses the process of data cleaning and harmonization, and subsequently focusses on frequency analysis as a way to study visual culture through sources drawn from the web.

## Programming for Distant Viewing and Reading
Working with web data requires a lot of curation. Many steps are involved in structuring the data in such a way that allows for summarizing and counting. Programming languages are helpful in doing both the data curation and the data analysis in a way that is reproducible and effective. This guide explains how to do this in Python, one of the most popular and versatile programming languages of today.

The guide takes some shortcuts in order to quickly come to actual web data. For a more extensive introduction to Python from the perspective of Humanities research, we refer to the course made by Folgert Karsdorp [link](https://www.karsdorp.io/python-course/)

It is important to note that Python is a _object-oriented_ programming language. Contrary to for example functional or procedural languages it is centered around objects and methods applied to those objects. The exact difference between languages goes beyond the scope of this guide, but be aware that no programming language is perfect and different languages serve different purposes.

The _commands_ that are written in Python are usually stored in scripts that have a ```.py``` file extension. These scripts are executed in the terminal. The terminal is accessible in Windows by looking for _cmd_ in the list of applications (bottom-left corner) and in MacOs by opening the _terminal_ application from the application menu. Once the terminal is opened, it is necessary to navigate to the folder where the ```.py``` script is stored (because the terminal does not know where the file is located in the system). Usually, the terminal opens in the ```/home``` folder on MacOs or on the ```C:``` drive folder on Windows. Navigating "down" to for example ```C:/Users/MyName/Documents/pythonscripts/``` can be done by typing ``cd Users/MyName/Documents/pythonscripts``. Executing a python script is done by typing ```python myscript.py```. Of course, this requires that Python is installed. The easiest way to install Python and other software that we will be needing in the Notebooks is by installing [Anaconda](https://www.anaconda.com/products/individual).

The Notebooks located in this repository are slightly different from ```.py``` scripts. Notebooks are files that contain both Python code and text or images. They offer the opportunity to run Python code cell by cell (instead of all at once). This enables easy editing of the code and a more transparent way of working. If you have Anaconda installed, find Jupyter Notebooks in your list of applications. Once opened you will be redirected to a browser window. Navigate to the location where you downloaded this repository and open the Notebook to see how it looks. Cells are executed by pressing ```Shift``` + ```Enter```.


## Python Basics 
Python is an object-oriented language. This means that is revolves around objects and actions performed over these objects. Objects can assume different forms, usually reffered to as "types". Because we will encounter several types in the Notebook, they are listed below. 

- *strings*: series of characters between quotation marks. Storing a string type in variable x is done by executing: ```x = "example string"```. 
- *integers*: numbers. Storing an integer in variable x is done by executing ```x = 1```.
- *lists*: a list of string, integer or other objects. Storing a list in variable x is done by executing ```x = [1, "string example", 3, ["list inside", "list"]]```. Accessing elements in a list is done by doing ```list[0]```, which returns 1. Note that Python starts counting at 0!

Since Python is an object-oriented language, most of it revolves around the objects described above. Running operations over an object (for example, calculating the sum of a list of figures) is usually done with functions. Functions are blocks of code that can be called. For example:

```
x = [1,2,3]

def SumFunction(input_list):
  sum_of_input_list = sum(input_list)
  return sum_of_input_list
  
sum_result = SumFunction(x)
print(sum_result)

>> 6

```


## Working with Web Data in Python
- installing Python and starting a JN environment
- importing data (.json + .txt)
- reordering data (creating lists + tables)
- visualizing patterns
