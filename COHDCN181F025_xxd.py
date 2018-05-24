import argparse
import binascii

def chunk(string):
    return(string[c:c+4] for c in range(0, len(string), 4))

parser = argparse.ArgumentParser()
parser.add_argument("--file", "-f", type = str, required = True)
args = parser.parse_args()

no = 0
read = 0
line = 0
length = 0

try:
    file = open(args.file, "r", errors='ignore')

except IOError:
    print("File not found")
    quit()

rawContent = file.read()
strContent = rawContent.replace(" ", ".")
hexContent = (binascii.hexlify(rawContent.encode("utf8"))).decode("utf8")

length = int(len(rawContent))
if length < 16:
    line = 1
else:
    line = length/16 + 1

for c in range(int(line)):
    text = "{:#08x}".format(no) + " | "
    text += " ".join(chunk(hexContent[read:read+32]))
    text += " | " + strContent[read:read+16]
    no += 16
    read += 16

    print(text)


