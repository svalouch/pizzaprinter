
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
        data = render('templates/receipt.j2', receipt).encode('utf-8')
        repl = {
            'ä': bytes([0x84]),
            'Ä': bytes([0x8e]),
            'ö': bytes([0x94]),
            'Ö': bytes([0x99]),
            'ü': bytes([0x81]),
            'Ü': bytes([0x9a]),
            'ß': bytes([0xe1]),
        }
        for c_src, c_dst in repl.items():
            data = data.replace(c_src.encode('utf-8'), c_dst)
        ser.write(data)
