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

### Links, references
- [github.com/TheMorc/screenduo-userspace](https://github.com/TheMorc/screenduo-userspace)
- [github.com/mayorbobster/screenduo4linux](https://github.com/mayorbobster/screenduo4linux)
- [Official support page with drivers for Windows XP and Vista](https://www.asus.com/supportonly/screenduo/helpdesk_download/)
- Old official drivers (SideShow) on archive.org:
  - [v1.08.06](https://web.archive.org/web/20240406002024/https://dlcdnets.asus.com/pub/ASUS/mb/accessory/ScreenDuo/ScreenDuo_10806.zip?model=ScreenDuo)
  - [v1.08.07](https://web.archive.org/web/20240406001904/https://dlcdnets.asus.com/pub/ASUS/mb/accessory/ScreenDuo/ScreenDuo_10807.zip?model=ScreenDuo)
  - [v1.08.08](https://web.archive.org/web/20240406001806/https://dlcdnets.asus.com/pub/ASUS/mb/accessory/ScreenDuo/ScreenDuo_10808.zip?model=ScreenDuo)

