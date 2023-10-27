# cellebrite

In 2017 bootloaders used by spying company Cellebrite were leaked via this [pastebin](https://pastebin.com/Z8zutAdD) and this [torrent](magnet:?xt=urn:btih:f15e65896a62e86f8bd2baf2ed786b5b26ee4071&dn=cellexploits01.tar.gz&tr=udp%3a%2f%2ftracker.leechers-paradise.org%3a6969&tr=udp%3a%2f%2ftracker.coppersurfer.tk%3a6969)

The binaries in that archive contain obfuscated code sections, this script will decode some of those.


# CelbEprDecode

A python3 script for decoding Cellebrite bootloaders from `ufedsamsungpack_v21.epr`.

This is useful when you want to inspect how the cellebrite code works.


## Usage

    python3 decodesamsungbin.py Bootloader_MSM8974_USB.bin_packed_0.4.5024

Will write the decoded bootloader in `Bootloader_MSM8974_USB.bin_packed_0.4.5024.decoded`


## License: MIT
Author: Willem Hengeveld <itsme@xs4all.nl>
