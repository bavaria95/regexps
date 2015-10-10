import os
import sys
import re
import codecs

def get_author(content):
    pattern = r'<META NAME="AUTOR" CONTENT="(.*)">'
    r = re.compile(pattern)
    return r.search(content).group(1)

def get_department(content):
    pattern = r'<META NAME="DZIAL" CONTENT="(.*)">'
    r = re.compile(pattern)
    return r.search(content).group(1)

def get_keywords(content):
    # <META NAME="KLUCZOWE_1" CONTENT="KUWEJT">
    pattern = r'<META NAME="KLUCZOWE_\d+" CONTENT="(.*)">'
    r = re.compile(pattern)
    return filter(None, r.findall(content)) # filter to remove empty keywords


def processFile(filepath):
    fp = codecs.open(filepath, 'rU', 'iso-8859-2')

    content = fp.read()

    fp.close()
    print("nazwa pliku: " + filepath)
    print("autor: " + get_author(content))
    print("dzial:" + get_department(content))
    print("slowa kluczowe: " + '; '.join(get_keywords(content)))
    print("liczba zdan:")
    print("liczba skrotow:")
    print("liczba liczb calkowitych z zakresu int:")
    print("liczba liczb zmiennoprzecinkowych:")
    print("liczba dat:")
    print("liczba adresow email:")
    print("\n")



try:
    path = sys.argv[1]
except IndexError:
    print("Brak podanej nazwy katalogu")
    sys.exit(0)


tree = os.walk(path)

for root, dirs, files in tree:
    for f in files:
        if f.endswith(".html"):
            filepath = os.path.join(root, f)
            processFile(filepath)


