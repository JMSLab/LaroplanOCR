## LaroplanOCR

Swedish primary school curricula (Läroplaner för grundskolan) in digital format.

We use optical character recognition (OCR) to transform curricula in image format into text.
For each curriculum we construct datasets at the paragraph and sentence levels, and a dataset that counts words.
These datasets are stored in [`./analysis/output/`](analysis/output).

### Prerequisites

You may want to compile some or all of the code yourself.
To do so, you need the following prerequisites.

- A `python` compiler version 3.8 or above.
    - We recommend installing [Anaconda](https://www.anaconda.com/products/individual)to get Python.
    - You will need to install the dependencies in `requirements.txt`. See [quick start](#quick-start) below.

- [`git`](https://git-scm.com/downloads) for version control.
    - And [`git-lfs`](https://git-lfs.github.com/) for versioning large files.

- The software `Tesseract-OCR`:
    - For Windows, install following steps [here](https://stackoverflow.com/a/53672281). For Mac, follow steps in section "Installing Tesseract on Mac" [here](https://guides.library.illinois.edu/c.php?g=347520&p=4121425).
    - Make sure to add "Swedish" when installing, in "Additional language data (download)"
    - Add the `Tesseract-OCR` installation folder to your path

- For Mac, you also need to install `poppler for Mac` in order to use the python package `pdf2image`, see [here](https://github.com/Belval/pdf2image/blob/master/README.md).


### Repository structure

- `./run.py` is a python script used to build the entire repository

- `./raw/` contains pdf files of Swedish curricula (Läroplaner)
   - `/orig/` contains curricula in pdf format
   - `/docs/` contains documentation

- `./derived/` contains code that runs the OCR and cleanes its output
   - `/code/make_images.py` transforms curricula in pdf format to separate jpg files. The jpg files are not included in the repo
   - `/code/ocr.py` reads the jpg files into text
   - `/code/clean.py` cleans the text files produced by the OCR

- `./analysis/` constructs datasets from the digitized text of each curricula
   - `/code/make_data.py` transforms the cleaned text files into paragraph- and sentence-level datasets
   - `/code/count.py` counts all appearances of words in each curricula

Each folder hosts an `/output/` subfolder where output from each script is saved.


### Quick start

1. Clone the repository to your local machine

2. Install dependencies. From the root of the repo run

    ```
    pip install -r requirements.txt
    ```

    (If using `conda`, run `conda install --file source/lib/requirements.txt`.)

3. Make sure that all the required program executables are in your system's path.

4. To compile the entire project, open the command-line and run

    ```
    python run.py
    ```

    You may also compile specific steps of the pipeline. 
    For example, `python derived/code/make_images.py` will transform the pdf files of the curricula into jpg files.


### Citations and Expectations for Usage

This repository is based on analysis in 
Hermo, S., Päällysaho, M., Seim, D., and Shapiro, Jesse M. 2021. Labor Market Returns and the Evolution of Cognitive Skills: Theory and Evidence.

