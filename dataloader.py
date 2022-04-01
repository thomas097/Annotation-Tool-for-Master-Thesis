import os
import spacy
import json
import tkinter as tk
from tkinter.filedialog import askopenfilename


class List:
    def __init__(self, items):
        self._items = items
        self._i = 0

    def __len__(self):
        return len(self._items)

    @property
    def i(self):
        return self._i

    def current(self):
        """ Returns item currently selected
        """
        return self._items[self._i]

    def has_next(self):
        return self._i < len(self._items) - 1

    def next(self):
        """ Returns the next item in the list
        """
        if self.has_next():
            self._i += 1
        return self._items[self._i]

    def has_prev(self):
        return self._i > 0

    def prev(self):
        """ Goes back to previous item visited in the list
        """
        if self.has_prev():
            self._i -= 1
        return self._items[self._i]


class DataLoader:
    def __init__(self, path, output_dir='annotations', sep='<eos>'):
        # Tokenizer
        self._nlp = spacy.load("en_core_web_sm")
        self._sep = sep

        # Read 'sep'-separated dataset from file
        with open(path, 'r', encoding='utf-8') as file:
            self._dataset = List(json.load(file))

        # Set up directory to store annotations into
        self._output_dir = output_dir
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        # Item currently being annotated
        self._item = self._dataset.current()
        self._load_savepoint()

    def summary(self):
        return 'Annotating {} ({}/{})'.format(self._item['id'], self._dataset.i, len(self._dataset))

    def already_annotated(self):
        """ Checks whether sample was annotated in previous session
            (this sample can be skipped)
        """
        filename = '%s/annotated_%s.json' % (self._output_dir, self._item['id'])
        return os.path.exists(filename)

    def _load_savepoint(self):
        """ Finds first unannotated sample in the dataset
        """
        self._item = self._dataset.current()
        while self.already_annotated() and self._dataset.has_next():
            self._item = self._dataset.next()

    def _tokenize(self, item):
        print('tokenizing')
        turns = item['triplet'].split(self._sep)
        tokens = [[w.lower_ for w in self._nlp(turn.strip())] for turn in turns]
        return [t + ['[unk]'] for t in tokens]

    def current(self):
        """ Returns the current sample
        """
        return self._tokenize(self._item)

    def next(self):
        """ Returns the next sample to be annotated
        """
        self._item = self._dataset.next()
        return self._tokenize(self._item)

    def prev(self):
        """ Returns the previously annotated sample (within current session)
        """
        # Step down list until previous sample is found
        self._item = self._dataset.prev()
        return self._tokenize(self._item)

    def save(self, annotation):
        """ Saves annotation from Interface to file
        """
        filename = '%s/annotated_%s.json' % (self._output_dir, self._item['id'])
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(annotation, file)

    def load(self):
        """ Loads annotation file from Interface
        """
        if not self.already_annotated():
            return []

        filename = '%s/annotated_%s.json' % (self._output_dir, self._item['id'])
        with open(filename, 'r', encoding='utf-8') as file:
            annotations = json.load(file)
        return annotations


def filebrowser():
    root = tk.Tk()
    root.withdraw()
    filename = askopenfilename()
    root.destroy()
    return filename


if __name__ == '__main__':
    # Sanity check
    dataset = DataLoader(filebrowser())
    print('next():', dataset.next())
    print('next():', dataset.next())
    print('next():', dataset.next())
    print('prev():', dataset.prev())
    print('next():', dataset.next())
