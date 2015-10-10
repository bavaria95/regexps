import os
import sys
import re
import codecs

def get_middle_text(content):
    '''
    returns text between first <P> tag and first <META> tag
    '''
    pattern = r'<P>(.*?)<META'
    r = re.compile(pattern, re.DOTALL)
    return r.search(content).group(1)

def get_author(content):
    pattern = r'<META NAME="AUTOR" CONTENT="(.*)">'
    r = re.compile(pattern)
    return r.search(content).group(1)

def get_department(content):
    pattern = r'<META NAME="DZIAL" CONTENT="(.*)">'
    r = re.compile(pattern)
    return r.search(content).group(1)

def get_keywords(content):
    pattern = r'<META NAME="KLUCZOWE_\d+" CONTENT="(.*)">'
    r = re.compile(pattern)
    return filter(None, r.findall(content)) # filter to remove empty keywords

def get_number_of_diff_dates():
    '''
    dates can be in dd-mm-rrrr, dd/mm/rrrr, dd.mm.rrrr, rrrr-dd-mm, 
    rrrr/dd/mm, rrrr.dd.mm formats. Also we need to guarantee that we
    have used only distinct dates. 
    '''
    global content
    s = set() # set to store all dates in tuple: (dd, mm, yyyy)

    # one type of date representation
    pattern = r'((?P<year>\d{4})(?P<separ>[./-])(?P<date>(0[1-9]|[12][0-9]|3[01])(?P=separ)(0[13578]|1[02])|((0[1-9]|[12][0-9])(?P=separ)(02))|(0[1-9]|[12][0-9]|3[0])(?P=separ)(0[469]|11)))'
    r = re.compile(pattern)
    for x in r.finditer(content):
        s.add(tuple(re.split(r'[./-]', x.group('date')) + [x.group('year')]))
    content = r.sub('', content) # removing dates from text

    # another type of date representation(could be written with first one, but because of named groups the code is much simpler now)
    pattern = r'(?P<full>((?P<date>(0[1-9]|[12][0-9]|3[01])[./-](0[13578]|1[02])|((0[1-9]|[12][0-9])[./-](02))|(0[1-9]|[12][0-9]|3[0])[./-](0[469]|11))[./-](?P<year>\d{4})))'
    r = re.compile(pattern)
    for x in r.finditer(content):
        if re.match(r'\d{2}(?P<separ>[./-])\d{2}(?P=separ)\d{4}', x.group('full')):  # check if separator is the same
            s.add(tuple(re.split(r'[./-]', x.group('date')) + [x.group('year')]))
    content = r.sub('', content)

    return len(s)

def get_number_of_acronyms():
    global content
    s = set()

    pattern = r'[\s><,?!)(]([a-zA-Z]{1,3})\.[\s><,?!)(]'
    r = re.compile(pattern)
    return len(set(r.findall(content)))



def processFile(filepath):
    global content # making it global to be able remove already found parts easily 
    fp = codecs.open(filepath, 'rU', 'iso-8859-2')
    content = fp.read()
    fp.close()

    author = get_author(content)
    department = get_department(content)
    keywords = '; '.join(get_keywords(content))

    content = get_middle_text(content) # since we don't need full text anymore

    dates_q = str(get_number_of_diff_dates())
    acronyms_q = str(get_number_of_acronyms())


    print("nazwa pliku: " + filepath)
    print("autor: " + author)
    print("dzial:" + department)
    print("slowa kluczowe: " + keywords)
    print("liczba zdan:")
    print("liczba skrotow: " + acronyms_q)
    print("liczba liczb calkowitych z zakresu int:")
    print("liczba liczb zmiennoprzecinkowych:")
    print("liczba dat: " + dates_q)
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

