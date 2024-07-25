# panel-thread-repro

This repository is a simplified setup to reproduce an issue I had with Panel.

The situation is that I wanted to build a real-time dashboard with Panel to monitor and control some instruments.
When I set up a background thread to update the param model, I ran into the stack trace seen below.

It seems that somehow, Panel processed a message (possibly from Javascript?) that told it to update the param (`ViewModel.position`) to the value `<b>The position</b>: 4.0`.

To reproduce, run `jupyter notebook`, open `gui_notebook.ipynb`, execute every cell and then click the "Change position in background" button in the UI.

```
Traceback (most recent call last):
  File "/Users/dj/code/panel-thread-repro/venv/lib/python3.11/site-packages/pyviz_comms/__init__.py", line 340, in _handle_msg
    self._on_msg(msg)
  File "/Users/dj/code/panel-thread-repro/venv/lib/python3.11/site-packages/panel/viewable.py", line 478, in _on_msg
    doc.unhold()
  File "/Users/dj/code/panel-thread-repro/venv/lib/python3.11/site-packages/bokeh/document/document.py", line 776, in unhold
    self.callbacks.unhold()
  File "/Users/dj/code/panel-thread-repro/venv/lib/python3.11/site-packages/bokeh/document/callbacks.py", line 432, in unhold
    self.trigger_on_change(event)
  File "/Users/dj/code/panel-thread-repro/venv/lib/python3.11/site-packages/bokeh/document/callbacks.py", line 409, in trigger_on_change
    invoke_with_curdoc(doc, event.callback_invoker)
  File "/Users/dj/code/panel-thread-repro/venv/lib/python3.11/site-packages/bokeh/document/callbacks.py", line 444, in invoke_with_curdoc
    return f()
           ^^^
  File "/Users/dj/code/panel-thread-repro/venv/lib/python3.11/site-packages/bokeh/util/callback_manager.py", line 185, in invoke
    callback(attr, old, new)
  File "/Users/dj/code/panel-thread-repro/venv/lib/python3.11/site-packages/panel/reactive.py", line 474, in _comm_change
    state._handle_exception(e)
  File "/Users/dj/code/panel-thread-repro/venv/lib/python3.11/site-packages/panel/io/state.py", line 458, in _handle_exception
    raise exception
  File "/Users/dj/code/panel-thread-repro/venv/lib/python3.11/site-packages/panel/reactive.py", line 472, in _comm_change
    self._schedule_change(doc, comm)
  File "/Users/dj/code/panel-thread-repro/venv/lib/python3.11/site-packages/panel/reactive.py", line 454, in _schedule_change
    self._change_event(doc)
  File "/Users/dj/code/panel-thread-repro/venv/lib/python3.11/site-packages/panel/reactive.py", line 450, in _change_event
    self._process_events(events)
  File "/Users/dj/code/panel-thread-repro/venv/lib/python3.11/site-packages/panel/reactive.py", line 387, in _process_events
    self.param.update(**self_params)
  File "/Users/dj/code/panel-thread-repro/venv/lib/python3.11/site-packages/param/parameterized.py", line 2319, in update
    restore = dict(self_._update(arg, **kwargs))
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/dj/code/panel-thread-repro/venv/lib/python3.11/site-packages/param/parameterized.py", line 2352, in _update
    self_._batch_call_watchers()
  File "/Users/dj/code/panel-thread-repro/venv/lib/python3.11/site-packages/param/parameterized.py", line 2546, in _batch_call_watchers
    self_._execute_watcher(watcher, events)
  File "/Users/dj/code/panel-thread-repro/venv/lib/python3.11/site-packages/param/parameterized.py", line 2506, in _execute_watcher
    watcher.fn(*args, **kwargs)
  File "/Users/dj/code/panel-thread-repro/venv/lib/python3.11/site-packages/panel/param.py", line 527, in link_widget
    self.object.param.update(**{p_name: change.new})
  File "/Users/dj/code/panel-thread-repro/venv/lib/python3.11/site-packages/param/parameterized.py", line 2319, in update
    restore = dict(self_._update(arg, **kwargs))
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/dj/code/panel-thread-repro/venv/lib/python3.11/site-packages/param/parameterized.py", line 2345, in _update
    setattr(self_or_cls, k, v)
  File "/Users/dj/code/panel-thread-repro/venv/lib/python3.11/site-packages/param/parameterized.py", line 528, in _f
    instance_param.__set__(obj, val)
  File "/Users/dj/code/panel-thread-repro/venv/lib/python3.11/site-packages/param/parameterized.py", line 530, in _f
    return f(self, obj, val)
           ^^^^^^^^^^^^^^^^^
  File "/Users/dj/code/panel-thread-repro/venv/lib/python3.11/site-packages/param/parameters.py", line 543, in __set__
    super().__set__(obj,val)
  File "/Users/dj/code/panel-thread-repro/venv/lib/python3.11/site-packages/param/parameterized.py", line 530, in _f
    return f(self, obj, val)
           ^^^^^^^^^^^^^^^^^
  File "/Users/dj/code/panel-thread-repro/venv/lib/python3.11/site-packages/param/parameterized.py", line 1498, in __set__
    self._validate(val)
  File "/Users/dj/code/panel-thread-repro/venv/lib/python3.11/site-packages/param/parameters.py", line 828, in _validate
    self._validate_value(val, self.allow_None)
  File "/Users/dj/code/panel-thread-repro/venv/lib/python3.11/site-packages/param/parameters.py", line 811, in _validate_value
    raise ValueError(
ValueError: Number parameter 'PositionView.position' only takes numeric values, not <class 'str'>.```
