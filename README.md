# Annotation Tool for Master Thesis

This repository contains the source code of the program used to annotate social conversations with SPO triples and perspectives. The annotation tool, annotation guidelines and program instructions can be found here. Batches of the to be annotated dialogues are stored under `data` (but a specific batch will be send to you in due time).

## Requirements

The annotation tool has been developed on Windows 10 and Ubuntu 19.04 with Python 3.8.8 (but should be compatible with any 3.+ version of Python and run on MacOS as well).

The following libraries must be installed:
* `spacy >= 3.2.0`

We recommend installing Spacy with the `en_core_web_sm` pipeline for English (needed for tokenization), which can be installed as follows:<br>
`> pip install spacy` <br>
`> python -m spacy download en_core_web_sm`

I recommend to install Spacy in a fresh virtual environment, which can be created and activated using the following commands:

`> python -m venv ENV_NAME`<br>
`> .\ENV_NAME\Scripts\activate`

## Usage

To use the annotation tool, run `main.py` in the IDE of your choice or from the commandline:

`> python3 main.py`

This will open a file browser which allows you to select a batch file to annotate (stored under `data`). After a batch has been chosen, the program will open. Instructions on how to use the program can be found in the [Annotation Guidelines.pdf](https://github.com/thomas097/Annotation-Tool-for-Master-Thesis/blob/main/Annotation_Guidelines.pdf) document. 

Results are stored in a new directory `annotations/`.

To adjust any of the settings (font size, number of triples, etc.) you may adjust the setting in `config.py`.

## Version history
* Font problem with Ubuntu has been fixed
* Laggy window updating problem with Ubuntu fixed
* Skip button now a checkbox you can set (will stay set  unless you uncheck it again)
* Skip means "add a special flag indicating that something is horribly wrong with this sample"
* Added an [unk] token to every sentence you can use if negation is marked implictly ("do you have a cat? a dog." -> no cat)

## Authors
Thomas Bellucci
