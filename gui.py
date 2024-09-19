import sys

import panel as pn


class View(pn.viewable.Viewer):
    def __init__(self, **params):
        super().__init__(**params)

        terminal = pn.widgets.Terminal()
        sys.stdout = terminal
        sys.stderr = terminal

        self._layout = pn.Column(
            terminal,
            pn.widgets.Button(name="Click me for output", on_click=self._on_click),
        )

    def _on_click(self, _event):
        print("Hello")
        print("World")

    def __panel__(self):
        return self._layout


if __name__ == '__main__':
    pn.extension("terminal")
    view = View()
    pn.serve(view)
