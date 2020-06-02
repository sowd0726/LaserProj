# Name
Derived from cython-hid project to use to control USB-IO with python3.
Original project is @
https://github.com/gbishop/cython-hidapi

# Feature
Modified setup.proje to avoid the issue to use libusb.so
Commented out buff = ''.join(map(chr, buff)) # convert to bytes in hid.pyx to use bynary array as a argument.

# Requirement
cython
python3
libusb-1.0.0
libudev-dev

# Installation
python3 setup.py build
sudo python3 setup.py install

# License
Please refer license.txt

