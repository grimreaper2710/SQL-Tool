import base64

with open('arcustomerimport02.zip', 'rb') as fin, open('output_b64.txt', 'wb') as fout:
    base64.encode(fin, fout)
