# panel-repro

This repository is a simplified setup to reproduce issues I've encountered with Panel.

To reproduce, run `jupyter notebook`, open `gui_notebook.ipynb`, execute every cell up to "view.servable()".

Two subissues here:
1. Then click the button in the UI - the expected result is that output goes into the Terminal widget, but it actually goes
into the Jupyter notebook output. This is already a known issue, see https://github.com/holoviz/panel/issues/7156

2. Then, execute the cell which prints output directly, which will print into the Terminal. 
If you execute this cell a few times, sometimes the output will not include newlines.

Issues #1 and #2 are reproducible with Panel 1.5.0 and Bokeh 3.5.2.

With Panel 1.4.5 and Bokeh 3.4.3, only issue #1 is reproducible.