############
Pizzaprinter
############

Demo application for `posprinter <https://github.com/svalouch/posprinter>`_. Exposes a small API through which a pizza receipt can be created, using a fixed template.

Dependencies
************
The main dependencies are:

* `FastAPI <https://fastapi.tiangolo.com/>`_ for the API server with builtin API browser
* `Jinja2 <https://palletsprojects.com/p/jinja/>`_ to render the template
* `pySerial <https://pyserial.readthedocs.io/en/latest/>`_ for working with the serial port
* `Uvicorn <https://www.uvicorn.org/>`_ that runs the actual application
* `posprinter <https://github.com/svalouch/posprinter>`_ (obviously)

Running
*******

Create a virtualenv (``python3 -m venv venv``) and activate it. Then pull the code:

.. code-block:: shell

    pip install git+https://github.com/svalouch/posprinter
    pip install -e . 
    uvicorn pizzaprinter.main:app --reload

Then point a browser at `<http://127.0.0.1:8000/docs>`_ and try it out. It will default to using ``/dev/ttyUSB0`` as printer interface, this can be changed in the code.

The important bits are in ``src/pizzaprinter/template.py``, where the templating functions are defined and finally passed to the template engine.


To redirect the output to a file, edit ``src/pizzaprinter/main.py`` and replace the with-block with:

.. code-block:: python

    with open('/tmp/receipt.bin', 'w') as fh:
        fh.write(render('templates/receipt.j2', receipt))

Important: although the file appears to be readable using a text editor, it is actually a binary file. The best way to look at it is using hex encoded, for example using ``xxd(1)``

Example
*******
Start the demo application like above and browse to the `docs` page. Click on `Try it out`, which opens the editor with a boilerplate request body. Change some values, for example the user name, pizza, size and price:

.. code-block:: json

    {
      "user": "testuser",
      "pizza": "Rustica",
      "date": "2019-09-23T15:37:04.141Z",
      "size": "L",
      "total": 13.12
    }

This yields a ticket (that has yet to be printed and photographed) that looks like this on the inside:
::

    00000000: 1b61 0232 332d 3039 2d32 3031 3920 3338  .a.23-09-2019 38
    00000010: 3a31 370a 1b2f 031b 7401 0a1b 6101 0a1d  :17../..t...a...
    00000020: 2f00 0e0a 1b61 011b 2138 1b68 000a 1b2f  /....a..!8.h.../
    00000030: 000a 5069 7a7a 6162 6573 7465 6c6c 756e  ..Pizzabestellun
    00000040: 670a 1b21 001b 6100 0a1b 2138 1b61 0132  g..!..a...!8.a.2
    00000050: 3031 392d 3039 2d32 3320 3135 3a33 373a  019-09-23 15:37:
    00000060: 3034 2e31 3431 3030 301b 6800 1b21 000a  04.141000.h..!..
    00000070: 1b61 000a 4265 7374 656c 6c75 6e67 2076  .a..Bestellung v
    00000080: 6f6e 201b 2108 7465 7374 7573 6572 3a0a  on .!.testuser:.
    00000090: 1b21 381b 6100 0a2a 1b21 3020 5275 7374  .!8.a..*.!0 Rust
    000000a0: 6963 610a 1b21 081b 6100 0a4c 0a1b 6100  ica..!..a..L..a.
    000000b0: 1b21 000a 0a1b 2100 1b61 010a 2b2b 2b20  .!....!..a..+++ 
    000000c0: 4162 686f 6c7a 6574 7465 6c20 2b2b 2b0a  Abholzettel +++.
    000000d0: 5a65 7474 656c 2062 6974 7465 2066 c3bc  Zettel bitte f..
    000000e0: 7220 4162 686f 6c75 6e67 2061 7566 6865  r Abholung aufhe
    000000f0: 6265 6e2e 0a1b 6101 0a1b 2f03 1b74 010a  ben...a.../..t..
    00000100: 0a1b 2f00 0a0a 0c                        ../....

The example uses a few logos that have been put into the printers memory before, these will obviously not show up or quite different with your printer. It is not that important and just used to explain a few of the functions.

Limitations
***********
Despite being an example, it already shows some limitations: Due to the fact that `jinja2` is a text template engine, it doesn't like working with binary content, which is totally understandable. This means that all commands are decoded to ``utf-8`` although they are not text. It works in this example and the general idea behind it was to provide an easy start, but it might fail if you use a character that has special meaning in some contexts.
