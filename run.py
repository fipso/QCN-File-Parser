#!/bin/env python
import sys

print("Parsing:", sys.argv[1])

NV_ID_ESN = 0
NV_ID_ESN_CHKSM = 1
NV_ID_SPC = 85
NV_ID_MEID = 1943
NV_ID_IMEI = 550
#NV_ID_IMEI = 457
#NV_ID_IMEI_CHKSM = 458

NV_BEGIN_PATTERN = [0x88, 0x00, 0x01, 0x00] 

nvs = []
with open(sys.argv[1], "rb") as f:
    data = f.read()

print("QCN Size:", len(data), "bytes")
print()

pos = 0
nv_i = 0
nv_id = -1

while pos < len(data) - 4:
    if [data[pos], data[pos+1], data[pos+2], data[pos+3]] == NV_BEGIN_PATTERN:
        nv_id = int.from_bytes([data[pos+4], data[pos+5]], "little")
        pos+=8 # we add +2 pad here

        nvs.append({
            "id": nv_id,
            "index": nv_i,
            "offset": pos,
        })
        nv_i += 1

        continue

    pos += 1

for nv in nvs:
    if nv["id"] == NV_ID_ESN:
        field = data[nv["offset"]:nv["offset"]+4]
        print(f"[{hex(nv['offset'])}] ESN", nv, field[::-1].hex())

    if nv["id"] == NV_ID_IMEI:
        field = data[nv["offset"]:nv["offset"]+9]
        firstDigit = field.hex()[2]
        other = field.hex()[4:]
        final = f"{firstDigit}{other[1]}{other[0]}{other[3]}{other[2]}{other[5]}{other[4]}{other[7]}{other[6]}{other[9]}{other[8]}{other[11]}{other[10]}{other[13]}{other[12]}"
        print(f"[{hex(nv['offset'])}] IMEI", nv, final)  

    if nv["id"] == NV_ID_MEID:
        field = data[nv["offset"]:nv["offset"]+7]
        meid = field.hex()
        meid = ''.join(reversed([meid[i:i+2] for i in range(0, len(meid), 2)])) # Reverse byte order
        print(f"[{hex(nv['offset'])}] MEID", nv, meid)
