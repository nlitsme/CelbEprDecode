"""
Tool for decoding the Cellebrite UFED bootloaders from ufedsamsungpack_v21.epr

It will write the decoded binary in a filename with suffix '.decoded'

Author: Willem Hengeveld <itsme@xs4all.nl>
"""
from __future__ import division, print_function
import struct

def processcelbdata(data):
    vectors = struct.unpack("<3L4s4LL4sLL", data[:48])
    if all( vectors[i]-vectors[i+1] == 1 for i in (1,4,5,6) ):
        print("vectors OK")
    if vectors[3] != b'CELB':
        raise Exception("not CELB arm code")
    if vectors[9] != b'CELB':
        raise Exception("not CELB arm code")

    encsize = vectors[8]
    enckey = vectors[10]

    if struct.unpack("<5L", data[0x110:0x124]) == (0xffffffff, 0x10000000, 0x00000000, 0x20000000, 0x08088405):
        print("unpacker type1 ok")
    elif struct.unpack("<5L", data[0x80:0x94]) == (0xffffffff, 0x10000000, 0x00000000, 0x20000000, 0x08088405):
        print("unpacker type2 ok")
    else:
        print("unknown unpacker")
    return encsize, enckey

def decode(enc, key, useR4):
    dec = []

    R7 = 0x8088405
    R3 = R4 = R2 = key

    dec = []
    for R1 in enc:
        R0 = R1 ^ R2
        R3  = (R3 * R7 + 1)&0xFFFFFFFF
        R0 ^= R3
        if useR4:
            R4 ^= (R4<<13)&0xFFFFFFFF
            R4 ^= R4>>17
            R4 ^= (R4<<5)&0xFFFFFFFF
            R0 ^= R4
        R2 = R1
        dec.append(R0)

    return dec


def processfile(fn):
    with open(fn, "rb") as fh:
        data = fh.read()
    encsize, enckey  = processcelbdata(data)
    enc = struct.unpack("<%dL" % (encsize/4), data[-encsize:])
    if len(data)-encsize == 0x2A8:
        dec = decode(enc, enckey, True)
    elif len(data)-encsize == 0x1BC:
        dec = decode(enc, enckey, False)
    else:
        print("has unexpected encsize: %04x -> ofs = +%04x" %( encsize, len(data)-encsize))

    decdata = struct.pack("<%dL" % (encsize/4), *dec)

    with open(fn+".decoded", "wb") as fh:
        fh.write(decdata)

def main():
    import argparse
    parser = argparse.ArgumentParser(description='decodebin')
    parser.add_argument('--verbose', '-v', action='count')
    parser.add_argument('FILES', type=str, nargs='+')
 
    args = parser.parse_args()

    for fn in args.FILES:
        print("==>", fn, "<==")
        try:
            processfile(fn)
        except Exception as e:
            print("ERROR", e)

if __name__ == '__main__':
    main()
