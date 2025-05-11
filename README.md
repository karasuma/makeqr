makeqr generates multiple QR codes.

# Env
+ Python 3.12.3

# Installation
`pip install -r requirements.txt`

# Usage
```bash
# Console
$> python makeqr.py <--row=int> <--scale=int> <--title=str> text1 text2 ...

# GUI
$> python makeqr_gui.py
```
## Options
+ --row=
  + A number of QR codes concatenated horizontally.
+ --scale=
  + Pixel size of the QR code.
+ --title=
  + Concatenated image's title and filename. Default is 'concatenated'.

# Examples
```bash
# https://url1.com https://url2.com (title: URL list)
$> python makeqr.py https://url1.com https://url2.com "--title=URL list"

# msg1,2,...,10 (scale of the QR code's pixel: 4)
$> python makeqr.py --scale=4 msg1 msg2 msg3 msg4 msg5 msg6 msg7 msg8 msg9 msg10
```
