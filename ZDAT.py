import struct, os

if not os.path.exists("output"):
    os.makedirs("output", exist_ok=True) # i don't know why i didn't do this...

def xor_decrypt(data, key):

    get_key = bytes([data[0] ^ key[0]])

    return bytes(x ^ get_key[i % len(get_key)] for i, x in enumerate(data))

with open('zdat here', 'rb') as file:
    ms = file
    magic = file.read(4)

    if magic != b"ZDAT":
        print("not a valid file")

    ms.seek(0x06)

    MetadataTable_Offset, name_offset, Data_offset, FileCount = struct.unpack('<4I', ms.read(16)) 
    print(FileCount)
    for _ in range(FileCount):
        ms.seek(MetadataTable_Offset)

        NameSize, FileSize, FileSize_dupe, Junk = struct.unpack('<4I', ms.read(16))
        MetadataTable_Offset += 4 * 4  
        # print(FileSize)


        ms.seek(name_offset)
        name_bytes = ms.read(NameSize)
        name_string = name_bytes.decode('utf-8')

        name_offset += NameSize

        ms.seek(Data_offset)

        file_bytes = ms.read(FileSize)
        if file_bytes[:7] != b"UnityFS": #they have several but only the one is used
            file_bytes = xor_decrypt(file_bytes, b"U")
        with open(f"output/{name_string}", 'wb') as f:
            f.write(file_bytes)
        print(f"Written {name_string}")
        Data_offset += FileSize