
import serial
from fastapi import FastAPI

# Defines the Receipt model
from .models import Receipt
# Does the template handling
from .template import render


app = FastAPI()


@app.post('/receipt', status_code=201)
def receipt(receipt: Receipt):
    print(f'Received receipt data: {receipt}')
    # uncomment the following two lines to dump the result to a file for inspection:
    # with open('/tmp/receipt.bin', 'w') as fh:
    #     fh.write(render('templates/receipt.j2', receipt))
    with serial.Serial('/dev/ttyUSB0', 19200, timeout=10) as ser:
        ser.write(render('templates/receipt.j2', receipt))
