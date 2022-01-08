::

    Python           _              _        
       _ __  ___  __| |___ _ _ _ _ (_)______ 
      | '  \/ _ \/ _` / -_) '_| ' \| |_ / -_)
      |_|_|_\___/\__,_\___|_| |_||_|_/__\___|


.. image:: https://img.shields.io/coveralls/github/PyCQA/modernize?label=coveralls&logo=coveralls
    :alt: Coveralls
    :target: https://coveralls.io/github/PyCQA/modernize
.. image:: https://img.shields.io/readthedocs/modernize?logo=read-the-docs
    :alt: Read the Docs
    :target: https://modernize.readthedocs.io/en/latest/
.. image:: https://img.shields.io/github/workflow/status/PyCQA/modernize/CI?label=GitHub%20Actions&logo=github
    :alt: GitHub Actions
    :target: https://github.com/PyCQA/modernize
.. image:: https://img.shields.io/pypi/v/modernize?logo=pypi
    :alt: PyPI
    :target: https://pypi.org/project/modernize/

Modernize is a Python program that reads Python 2 source code
and applies a series of fixers to transform it into source code
that is valid on both Python 3 and Python 2.7.

This allows you to run your test suite on Python 2.7 and Python 3
so you can gradually port your code to being fully Python 3
compatible without slowing down development of your Python 2
project.

The ``python -m modernize`` command works like
``python -m fissix``, see `fissix <https://github.com/jreese/fissix>`_.
Here's how you'd rewrite a
single file::

    python -m modernize -w example.py

It does not guarantee, but it attempts to spit out a codebase compatible
with Python 2.6+ or Python 3. The code that it generates has a runtime
dependency on `six <https://pypi.python.org/pypi/six>`_, unless the
``--no-six`` option is used. Version 1.9.0 or later of ``six`` is
recommended. Some of the fixers output code that is not compatible with
Python 2.5 or lower.

Once your project is ready to run in production on Python 3 it's
recommended to drop Python 2.7 support using
`pyupgrade <https://pypi.org/project/pyupgrade/>`_

**Documentation:** `modernize.readthedocs.io
<https://modernize.readthedocs.io/>`_.

See the ``LICENSE`` file for the license of ``modernize``.
Using this tool does not affect licensing of the modernized code.

This library is a very thin wrapper around `fissix
<https://github.com/jreese/fissix>`_, a fork of lib2to3.


Fork Enhancements
-----------------
Same old library with the added fixers:

* ``classic_division_warnings`` which ensures classic division warnings are issued non-native types (ie. numpy types). This is unlike the behavior of the interpreter option ``-Qwarnall`` `docs <https://www.python.org/dev/peps/pep-0238/#command-line-option>`_.
* ``import_division_future`` which will add ``from __future__ import division`` to any files using division

The warnings from ``classic_division_warnings`` are intended as an aid to determining which usages of division (``/``, ``/=``) should be changed to floor division (``//``, ``//=``) before running the fixer ``import_division_future``.

For example if one sees:

* only ``classic int division`` warnings for an instance of division then it should be changed from ``/`` to ``//``
* both ``classic int division`` and ``classic float division`` warnings for an instance of division then one must carefully consider the changes to the behavior of division once ``import_division_future`` is used

Disclaimer: the warnings are useful only if you have good test coverage. If you have poor test coverage you may not find that an instance of division is actually used with both ``float`` and ``int`` types and thus should not be changed from ``/`` to ``//``.

Tips: 

* capture warnings into your logs with ``logging.captureWarnings(True)`` `docs <https://docs.python.org/2.7/library/logging.html#integration-with-the-warnings-module>`_
* make sure there is no warning suppression by setting the environment variable ``PYTHONWARNINGS=default`` `docs <https://docs.python.org/3/using/cmdline.html#envvar-PYTHONWARNINGS>`_
