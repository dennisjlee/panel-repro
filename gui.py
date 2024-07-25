import param
import panel as pn
import threading
import time

class ViewModel(param.Parameterized):
    position: float = param.Number(default=0, bounds=(0, 100))


class BackgroundUpdater:
    def __init__(self, model: ViewModel):
        self._model = model
        self._target_position = model.position
        self._thread = threading.Thread(target=self._update_position)
        self._running = True
        self._thread.start()

    def stop(self):
        self._running = False

    def set_target(self, position: float):
        self._target_position = position

    def _update_position(self):
        while self._running:
            if abs(self._model.position - self._target_position) > 0.1:
                step = (self._target_position - self._model.position) / 10
                while abs(self._model.position - self._target_position) > 0.1:
                    new_position = self._model.position + step
                    print('Setting position to', new_position)
                    self._model.position = new_position
                    time.sleep(0.5)
            else:
                time.sleep(0.5)


def change_position_in_background(background_updater: BackgroundUpdater, target_position: float):
    background_updater.set_target(target_position)
    time.sleep(2)


class PositionView(pn.viewable.Viewer):
    position = param.Number(allow_refs=True, bounds=(0, 100))

    def __init__(self, **params):
        super().__init__(**params)

        self._layout = pn.Column(
            "## Position",
            pn.widgets.FloatSlider.from_param(self.param.position, name="The position"),
            pn.widgets.StaticText.from_param(self.param.position, name="The position"),
        )

    def __panel__(self):
        return self._layout


class View(pn.viewable.Viewer):
    _view_model: ViewModel
    _background_updater: BackgroundUpdater

    target_position: float = param.Number(default=10)

    def __init__(self, view_model: ViewModel, background_updater: BackgroundUpdater):
        super().__init__()

        self._view_model = view_model
        self._background_updater = background_updater

        self._layout = pn.Column(
            PositionView(position=self._view_model.param.position),
            pn.widgets.FloatInput.from_param(self.param.target_position),
            pn.widgets.Button(name="Change position in background",
                              button_type="primary",
                              on_click=lambda _event: change_position_in_background(self._background_updater, self.target_position))
        )

    def __panel__(self):
        return self._layout
