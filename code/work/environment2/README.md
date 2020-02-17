# Scripts for Interacting with API + Extracting Data from the Web

Scripts in this folder:
- `gatherImagesFunctions.py`: functions for scraping image urls extracted from API. Required for `gatherImages.py`.
- `gatherImages.py`: script for requesting to Google API. Communicates with API through `gcv_api.py` (based on _memespector_ project by André Mintz, 2018). Uses API results to create new lists of urls, hereby iterating to get more image urls (since Google returns only ~100 urls per image). Stores everything in folders per iteration: `image_[name]_[iteration]`.
- `gcv_api.py`: library for communicating with Google API. Requires a key and calls scripts in `/lib` folder. In this folder, `config.py` manages the download limit and API features to be called.
- `gatherDataFunctions.py`: functions for extracting:
  - urls of the images in all folders
  - urls of pages containing images
  - extracting dates based on urls. The [htmldate](https://github.com/adbar/htmldate) library.
  - extracting html files based on webpage urls
