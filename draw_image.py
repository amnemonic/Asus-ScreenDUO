'''
MIT License

Copyright (c) 2024 Adam Mnemonic

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''

import ctypes
import usb.core
import usb.util
from PIL import Image


def swapEndian16(intval):
    return int.from_bytes(intval.to_bytes(length=2, byteorder='little'))

def swapEndian32(intval):
    return int.from_bytes(intval.to_bytes(length=4, byteorder='little'))


class ASUS_PAYLOAD_HEADER(ctypes.Structure):
    _pack_   = 1
    _fields_ = [
        ( "Signature"          , ctypes.c_uint32),
        ( "Tag"                , ctypes.c_uint32),
        ( "DataTransferLength" , ctypes.c_uint32),
        ( "Flags"              , ctypes.c_uint8 ),
        ( "LUN"                , ctypes.c_uint8 ),
        ( "CBLength"           , ctypes.c_uint8 ),

        ( "u1_e602"            , ctypes.c_uint16),
        ( "blockSize"          , ctypes.c_uint32),
        ( "totalSize"          , ctypes.c_uint32),
        ( "index"              , ctypes.c_uint8 ),
        ( "unused1"            , ctypes.c_uint8 ),
        ( "unused2"            , ctypes.c_uint32),
    ]
    def __init__(self):
        super().__init__()
        self.Signature = int.from_bytes(b'USBC',byteorder='little')
        self.u1_e602   = 0x02e6
        self.CBLength  = 0x0c
        self.Tag       = 0x02ef


class ASUS_IMAGE_HEADER(ctypes.Structure):
    _pack_  = 1
    _fields_ = [
        ( "unkn1"      ,  ctypes.c_uint16),
        ( "unkn2"      ,  ctypes.c_uint16),
        ( "TotalLength",  ctypes.c_uint32),
        ( "x"          ,  ctypes.c_uint16),
        ( "y"          ,  ctypes.c_uint16),
        ( "width"      ,  ctypes.c_uint16),
        ( "height"     ,  ctypes.c_uint16),
        ( "unkn3"      ,  ctypes.c_uint16),
        ( "unkn4"      ,  ctypes.c_uint16),
        ( "unkn5"      ,  ctypes.c_uint32),
        ( "unkn6"      ,  ctypes.c_uint32),
        ( "unkn7"      ,  ctypes.c_uint32),
    ]
    def __init__(self):
        super().__init__()
        self.unkn1     = 2
        self.unkn2     = 0x20
        self.unkn4     = 1


def screenduo_draw_raw(usb_device, raw_image):
    global dev
    index         = 0
    offset        = 0
    raw_image_len = len(raw_image)

    command = ASUS_PAYLOAD_HEADER()
    command.totalSize = swapEndian32(raw_image_len)

    while offset<raw_image_len:
        command.index=index
        command.DataTransferLength = 0x10000 if raw_image_len-offset>=0x10000 else (raw_image_len-offset)
        command.blockSize = swapEndian32(command.DataTransferLength)

        payload = raw_image[offset:offset+command.DataTransferLength]

        usb_device.write(2, bytes(command), timeout=1000)
        usb_device.write(2, bytes(payload), timeout=1000)
        _ =  usb_device.read(0x81, 0xFF,   timeout=1000)

        offset+=0x10000
        index+=1
        command.Tag+=1




if __name__ == '__main__':
    dev = usb.core.find(idVendor=0x1043, idProduct=0x3100)

    if dev is None:
        print('Device not found'); exit(-1)


    image      = Image.open("octocat.png")
    raw_pixels = image.tobytes()

    img_header = ASUS_IMAGE_HEADER()
    img_header.width       = image.width
    img_header.height      = image.height
    img_header.TotalLength = (img_header.width * img_header.height * 3) + ctypes.sizeof(ASUS_IMAGE_HEADER)


    assert len(bytes(img_header)+raw_pixels)==img_header.TotalLength
    screenduo_draw_raw(dev, bytes(img_header)+raw_pixels)


