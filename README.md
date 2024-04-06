## Asus ScreenDUO and Python

![asus-screenduo](https://github.com/amnemonic/Asus-ScreenDUO/assets/29899901/3bcfdbe7-0fec-4173-b650-6c54e9ebeac1)

### What you need
- Zadig installer - https://zadig.akeo.ie/
- PyUSB library - https://pypi.org/project/pyusb/
- Pillow library (used in example) - https://pypi.org/project/pillow/

### Installing device driver
- Run Zadig installer as administrator and find `ScreenDUO` on the list
- In driver list select `libusb-win32`:

![zadig1](https://github.com/amnemonic/Asus-ScreenDUO/assets/29899901/d2e990e8-5e1b-4000-880d-01f00ae55345)
- Click "Install Driver" and wait
- If everything went well then you should see new device in Device Manager:

![libusb](https://github.com/amnemonic/Asus-ScreenDUO/assets/29899901/02e42950-945c-4d29-b476-101b0941c780)


### Python libraries
- `pip install pyusb`
- `pip install pillow`
