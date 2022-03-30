import tkinter as tk
import tkinter.font as TkFont
from dataloader import DataLoader, filebrowser
from functools import partial

from config import *


class ArgumentButton(tk.Button):
    def __init__(self, root, command, align=tk.LEFT):
        # Create Button
        self._label = tk.StringVar()
        super().__init__(root, textvariable=self._label, relief=ARG_RELIEF, bg=BG_COLOR, command=command)
        self.pack(side=align)

        # Register assigned tokens
        self._root = root
        self.tokens = []
        self.indices = []
        self.clear()

    def highlight(self, value):
        """ Highlight the button when selected.
        """
        if value:
            self.configure(bg=ARG_HIGHLIGHT_COLOR)
        else:
            self.configure(bg=BG_COLOR)

    def add(self, token, index):
        """ Assigns token to argument.
        """
        self.tokens.append(token)
        self.indices.append(index)
        self._label.set(' '.join(self.tokens))

    def clear(self):
        """ Erase all tokens of button.
        """
        self.tokens = []
        self.indices = []
        self._label.set(ARG_PLACEHOLDER)


class Row(tk.Frame):
    def __init__(self, root):
        super().__init__(root, bg=BG_COLOR)
        self.pack(side=tk.TOP)


class Column(tk.Frame):
    def __init__(self, root, row=0, col=0, colspan=1, sticky=tk.E):
        super().__init__(root, bg=BG_COLOR)
        self.grid(row=row, column=col, columnspan=colspan, padx=COLUMN_PADDING, pady=COLUMN_PADDING, sticky=sticky)
        self._rows = []

    def _expand(self, num):
        """ Add rows until there are 'num'
        """
        while num > len(self._rows) - 1:
            self._rows.append(Row(self))

    def add_button(self, i, text, command, padding=PADDING):
        self._expand(i)
        button = tk.Button(self._rows[i], text=text, relief=RELIEF, command=command)
        button.pack(side=tk.LEFT, padx=padding, pady=padding, ipadx=padding, ipady=padding)
        return button

    def add_text(self, i, text, pad=0, align=tk.LEFT, bg_color=BG_COLOR):
        self._expand(i)
        label = tk.Label(self._rows[i], text=text, relief='flat', bg=bg_color)
        label.pack(side=align, padx=pad)
        return label

    def add_triple(self, i, command):
        self._expand(i)
        self.add_text(i, '[')
        subj = ArgumentButton(self._rows[i], command=partial(command, i, 0))
        self.add_text(i, ',')
        pred = ArgumentButton(self._rows[i], command=partial(command, i, 1))
        self.add_text(i, ',')
        obj = ArgumentButton(self._rows[i], command=partial(command, i, 2))
        self.add_text(i, ']')
        return subj, pred, obj

    def add_perspective(self, i, command):
        self._expand(i)
        self.add_text(i, '[')
        polarity = ArgumentButton(self._rows[i], command=partial(command, i, 3))
        self.add_text(i, ',')
        certainty = ArgumentButton(self._rows[i], command=partial(command, i, 4))
        self.add_text(i, ']')
        return polarity, certainty


class Interface:
    def __init__(self, dataloader):
        # Window
        self._window = tk.Tk()
        self._window.title(TITLE)
        self._window.deiconify()

        # Centered Frame to add interface into
        self._root = tk.Frame(self._window, bg=BG_COLOR)
        self._root.pack(fill="none", expand=True)

        self.defaultFont = tk.font.nametofont("TkDefaultFont")
  
        # Overriding default-font with custom settings
        # i.e changing font-family, size and weight
        self.defaultFont.configure(family=FONT[0], size=FONT[1])

        # Layout
        self._token_frame = Column(self._root, row=0, col=0, colspan=2, sticky=tk.N)
        self._triple_frame = Column(self._root, row=1, col=0, colspan=1, sticky=tk.E)
        self._persp_frame = Column(self._root, row=1, col=1, colspan=1, sticky=tk.W)
        self._button_frame = Column(self._root, row=2, col=0, colspan=2, sticky=tk.S)
        self._tokens = {}
        self._triples = {}
        self._focus = None  # What argument is currently being annotated?

        # Bind L/R keys to change focus
        self._window.bind(LEFT_KEY, partial(self._change_focus_with_keys, 'l'))
        self._window.bind(RIGHT_KEY, partial(self._change_focus_with_keys, 'r'))

        # Annotate first sample
        self._dataloader = dataloader
        self._item = self._dataloader.current()

        self._init_layout()
        self._window.mainloop()

    def _change_focus_with_keys(self, evt, _):
        # Update focus position according to keys
        i, j = self._focus
        j = j - 1 if evt == 'l' else j + 1  # Change position in row

        if j < 0:
            i -= 1
            j = 4  # index of 5th argument
        elif j > 4:
            j = 0
            i += 1

        # Check if out of bounds
        if (i, j) in self._triples:
            self._set_focus(i, j)

    def _set_focus(self, i, j):
        # Set focus to the j-th argument of the i-th triple
        self._focus = (i, j)

        #  Set color of selected argument
        for idx, button in self._triples.items():
            if (i, j) == idx:
                button.highlight(True)
                button.clear()
            else:
                button.highlight(False)

    def _assign_to_focus(self, i, j):
        token = self._item[i][j]
        button = self._triples[self._focus]
        button.add(token, (i, j))

    def _next(self, skipped=False):
        # Create annotation capsule
        annotation = {'tokens': self._item, 'annotations': [], 'skipped': skipped}
        for i in range(NUM_TRIPLES):
            triple = (self._triples[(i, 0)].indices,  # subject
                      self._triples[(i, 1)].indices,  # predicate
                      self._triples[(i, 2)].indices,  # object
                      self._triples[(i, 3)].indices,  # polarity
                      self._triples[(i, 4)].indices)  # certainty
            annotation['annotations'].append(triple)

        # Save to file
        self._dataloader.save(annotation)

        # Show next sample
        self._item = self._dataloader.next()
        self._init_layout()

    def _back(self):
        self._item = self._dataloader.prev()
        self._init_layout()

    def _clear_layout(self):
        """ Clears all Columns and references to old Buttons
        """
        self._token_frame.destroy()
        self._triple_frame.destroy()
        self._persp_frame.destroy()
        self._button_frame.destroy()

        self._token_frame = None
        self._triple_frame = None
        self._persp_frame = None
        self._button_frame = None

        for button in self._tokens.values():
            button.destroy()

        for button in self._triples.values():
            button.destroy()

        self._tokens = {}
        self._triples = {}

    def _init_layout(self):
        # Add new Columns
        self._clear_layout()
        self._token_frame = Column(self._root, row=0, col=0, colspan=2, sticky=tk.N)
        self._triple_frame = Column(self._root, row=1, col=0, colspan=1, sticky=tk.E)
        self._persp_frame = Column(self._root, row=1, col=1, colspan=1, sticky=tk.W)
        self._button_frame = Column(self._root, row=2, col=0, colspan=2, sticky=tk.S)

        # Show dialogue
        for i, turn in enumerate(self._item):
            for j, token in enumerate(turn):
                token = self._token_frame.add_button(i, token, padding=TOKEN_PADDING, command=partial(self._assign_to_focus, i, j))
                self._tokens[(i, j)] = token

        # Create triple and perspective Columns
        for i in range(NUM_TRIPLES):
            subject, predicate, object_ = self._triple_frame.add_triple(i, command=self._set_focus)
            self._triples[(i, 0)] = subject
            self._triples[(i, 1)] = predicate
            self._triples[(i, 2)] = object_

            polarity, certainty = self._persp_frame.add_perspective(i, command=self._set_focus)
            self._triples[(i, 3)] = polarity
            self._triples[(i, 4)] = certainty

        # Fill in annotation if we have already done so
        if self._dataloader.already_annotated():
            print('already_annotated')
            annotations = self._dataloader.load()['annotations']
            for i, triple in enumerate(annotations):
                for j, arg in enumerate(triple):
                    for turn_idx, token_idx in arg:
                        self._focus = (i, j)  # set tmp argument focus
                        self._assign_to_focus(turn_idx, token_idx)

        # Add Skip and Next buttons
        self._button_frame.add_button(1, 'back', command=self._back, padding=BUTTON_PADDING)
        self._button_frame.add_button(1, 'skip', command=partial(self._next, skipped=True), padding=BUTTON_PADDING)
        self._button_frame.add_button(1, 'next', command=partial(self._next, skipped=False), padding=BUTTON_PADDING)

        # Set default focus and placeholder text
        self._window.title(self._dataloader.summary())


if __name__ == '__main__':
    dataloader = DataLoader(filebrowser(), output_dir='annotations')
    interface = Interface(dataloader)
