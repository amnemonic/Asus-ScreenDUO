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



def swapEndian16(intval):
    return int.from_bytes(intval.to_bytes(length=2, byteorder='little'))

def swapEndian32(intval):
    return int.from_bytes(intval.to_bytes(length=4, byteorder='little'))

CMD_SET_SCREEN_TIMEOUT = 0x09e6
CMD_SET_IMAGE          = 0x02e6

class ASUS_PAYLOAD_HEADER(ctypes.Structure):
    _pack_   = 1
    _fields_ = [
        ( "Signature"          , ctypes.c_uint32),
        ( "Tag"                , ctypes.c_uint32),
        ( "DataTransferLength" , ctypes.c_uint32),
        ( "Flags"              , ctypes.c_uint8 ),
        ( "LUN"                , ctypes.c_uint8 ),
        ( "CBLength"           , ctypes.c_uint8 ),

        ( "Command"            , ctypes.c_uint16),
        ( "blockSize"          , ctypes.c_uint32),
        ( "totalSize"          , ctypes.c_uint32),
        ( "index"              , ctypes.c_uint8 ),
        ( "unused1"            , ctypes.c_uint8 ),
        ( "unused2"            , ctypes.c_uint32),
    ]
    def __init__(self):
        super().__init__()
        self.Signature = int.from_bytes(b'USBC',byteorder='little')
        self.CBLength  = 0x0c

class ASUS_TIMEOUT_SETTINGS(ctypes.Structure):
    _pack_  = 1
    _fields_ = [
        ( "unkn1"               ,  ctypes.c_uint16),
        ( "unkn2"               ,  ctypes.c_uint16),
        ( "TotalLength"         ,  ctypes.c_uint32),
        ( "enable_screensaver"  ,  ctypes.c_uint8),
        ( "screen_timeout_sec"  ,  ctypes.c_uint16),
    ]
    def __init__(self):
        super().__init__()
        self.unkn1       = 9
        self.unkn2       = 8
        self.TotalLength = ctypes.sizeof(ASUS_TIMEOUT_SETTINGS)






if __name__ == '__main__':
    dev = usb.core.find(idVendor=0x1043, idProduct=0x3100)

    if dev is None:
        print('Device not found'); exit(-1)

    command                     = ASUS_PAYLOAD_HEADER()
    command.Command             = CMD_SET_SCREEN_TIMEOUT
    command.DataTransferLength  = 0x0b
    command.blockSize           = swapEndian32(0x0b)
    command.totalSize           = swapEndian32(0x0b)

    payload                     = ASUS_TIMEOUT_SETTINGS()
    payload.enable_screensaver  = 1      #if 1 then disable screen after timeout, when 0 then screen enabled forever
    payload.screen_timeout_sec  = 6      #timeout in seconds, disable screen after last button press
    
    dev.write(2, bytes(command), timeout=1000)
    dev.write(2, bytes(payload), timeout=1000)
