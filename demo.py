#!/usr/bin/python3

import base64
import datetime
import random
import sys

from cryptography import x509
from cryptography.hazmat.backends import default_backend

import depexport
import regk
import sigeh
import utils

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: ./demo.py <private key file> <cert file> <base64 AES key file> <number of receipts>")
        sys.exit(0)

    priv = sys.argv[1]
    cert = sys.argv[2]
    num = int(sys.argv[4])

    if num < 1:
        print("The number of receipts must be at least 1.")
        sys.exit(0)

    key = None
    with open(sys.argv[3]) as f:
        key = base64.b64decode(f.read().encode("utf-8"))

    serial = None
    with open(cert) as f:
        serial = utils.loadCert(f.read()).serial

    register = regk.Registrierkassa("AT77", "PIGGYBANK-007", None, int(0.0 * 100), key)
    sigsystem = sigeh.SignaturerstellungseinheitWorking(serial, priv)
    exporter = depexport.DEPExporter(cert)

    receipts = [register.receipt('R1', "00000", datetime.datetime.now(), 0.0, 0.0, 0.0,
        0.0, 0.0, sigsystem)]
    for i in range(1, num):
        receiptId = "%05d" % i
        sumA = round(random.uniform(-1000, 1000), 2)
        sumB = round(random.uniform(-1000, 1000), 2)
        sumC = round(random.uniform(-1000, 1000), 2)
        sumD = round(random.uniform(-1000, 1000), 2)
        sumE = round(random.uniform(-1000, 1000), 2)
        dummy = random.uniform(0, 1) > 0.5
        reversal = random.uniform(0, 1) > 0.5
        receipt = register.receipt('R1', receiptId, datetime.datetime.now(), sumA, sumB,
                sumC, sumD, sumE, sigsystem, dummy, reversal)
        receipts.append(receipt)

    print(exporter.export(receipts))
