import argparse
import binascii

def chunk(string):
    return(string[c:c+4] for c in range(0, len(string), 4))

parser = argparse.ArgumentParser()
parser.add_argument("--file", "-f", type = str, required = True)
args = parser.parse_args()

lineNumber = 0
read = 0
line = 0
length = 0

try:
    rawContent = [line.rstrip() for line in open(args.file, "r", errors='ignore')]
    rawContent = '.'.join(map(str, rawContent))

except IOError:
    print("Error reading file")
    quit()

strContent = rawContent.encode("utf8").decode("utf8")
strContent = strContent.replace(" ", ".")
hexContent = (binascii.hexlify(rawContent.encode("utf8"))).decode("utf8")

length = int(len(rawContent))
if length < 16:
    line = 1
else:
    line = length/16 + 1

for c in range(int(line)):
    text = "{:#08x}".format(lineNumber) + " | "
    text += " ".join(chunk(hexContent[read:read+32]))
    text += " | " + str(strContent[read:read+16])
    lineNumber += 16
    read += 16

    print(text)


