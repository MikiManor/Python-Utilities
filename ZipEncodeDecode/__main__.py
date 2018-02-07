import base64
import sys
import os

def encode(i_ZipFileName):
    print("Going to encode file {} to base64 b85...".format(i_ZipFileName))
    newFilePath =  i_ZipFileName +".b64"
    try:
        with open(i_ZipFileName, 'rb') as fin, open(newFilePath, 'wb') as fout:
            bytes = fin.read()
            b85String = base64.b85encode(bytes)
            lineLenght = 80
            lines = [b85String[i:i + lineLenght] for i in range(0, len(b85String), lineLenght)]
            fout.write(b"\n".join(lines))
            print("File {} has created successfully".format(newFilePath))
    except Exception as e:
        raise

def decode(i_EncodedFile):
    tmpdir = None
    try:

        # Unpack the zipfile into the temporary directory
        file_zip = i_EncodedFile + ".zip"
        with open(file_zip, "wb") as fout, open(i_EncodedFile, "rb") as fin:
            binData = fin.readlines()
            binData = b"".join(binData)
            decodedString = base64.b85decode(binData.replace(b"\n", b""))
            fout.write(decodedString)
        print("zip File created at {}".format(file_zip))
    except:
        raise


if __name__ == '__main__':
    if len(sys.argv) < 3:
        raise Exception("Missing Arguments! Operation and inputFile")
    typesOfExecution = ['encode', 'decode']
    operation = sys.argv[1]
    inputFile = sys.argv[2]
    if not os.path.exists(inputFile):
        raise FileNotFoundError("File {} doesn't exists!".format(inputFile))
    if operation in typesOfExecution:
        if operation == 'encode':
            try:
                encode(inputFile)
            except Exception as e:
                raise (e)
        elif operation == 'decode':
            PY2 = sys.version_info[0] == 2
            PY3 = sys.version_info[0] == 3
            if PY3:
                iterbytes = iter
            else:
                def iterbytes(buf):
                    return (ord(byte) for byte in buf)
            try:
                decode(inputFile)
            except Exception as e:
                raise (e)
    else:
        print("Operation doesn't exist! valid operations are {}".format(','.join(typesOfExecution)))