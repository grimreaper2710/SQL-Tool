import base64

with open('ARInvoiceYYYYMMDDHHMMSS.zip', 'rb') as fin, open('output.zip.txt', 'wb') as fout:
    base64.encode(fin, fout)
