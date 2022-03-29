# Annotation-Tool-for-Master-Thesis

This repository contains the source code of the program used to annotate social conversations with SPO triples and perspectives. The annotation tool, annotation guidelines and program instructions can be found here. Batches of to be annotated are stored under `batches`.

## Requirements

The annotation tool has been created with Python 3.8 (but should be compatible with any 3.+ version of Python).

The following libraries must be installed:
* `spacy >= 3.2.0`

We recommend installing Spacy with the `en_core_web_sm` pipeline for English (needed for tokenization), which can be installed by:<br>
`> pip install spacy` <br>
`> python -m spacy download en_core_web_sm`

It is recommended to install the above dependencies in a fresh virtual environment, which can be created and activated using the following commands:

`> python -m venv ENV_NAME`<br>
`> .\sample_venv\Scripts\activate`

## Usage

To use the annotation tool, run `main.py` in the IDE of your choice or from the commandline:

`python3 main.py`

This will open a file browser which allows you to select a batch file to annotate (stored under `batches`). After a batch has been chosen, the program will open. Instructions on how to use the program can be found in the [Annotation Guidelines.pdf](https://github.com/thomas097/Master-Thesis-Contextual-Triple-Extraction/blob/main/src/annotation_tool/Annotation_Guidelines.pdf) document. 

Results are stored in a directory `annotations/`.

To adjust any of the settings (font size, number of triples, etc.) you may adjust the setting in `config.py`.

## Disclaimer
I have found some limitations of the program when running on Ubuntu; the programd efaults to the system font which is not particularly pretty. Nonetheless, the program should still function properly.
