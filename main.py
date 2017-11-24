import re

def parse_terms(file):
    out = open("terms.txt", 'w')

    for line in file:
        key = re.findall('key="(.*?)"', line)

        if len(key) != 0:

            for title in re.findall("<title>(.*?)</title>", line):
                for term in re.split("[^0-9a-zA-Z_]", title):
                    if len(term) > 2:
                        out.write('t-' + term.lower() + ':' + key[0] + '\n')

            for journal in re.findall("<journal>(.*?)</journal>", line):
                for term in re.split("[^0-9a-zA-Z_]", journal):
                    if len(term) > 2:
                        out.write('o-' + term.lower() + ':' + key[0] + '\n')

            for publisher in re.findall("<publisher>(.*?)</publisher>", line):
                for term in re.split("[^0-9a-zA-Z_]", publisher):
                    if len(term) > 2:
                        out.write('o-' + term.lower() + ':' + key[0] + '\n')

            for bookTitle in re.findall("<booktitle>(.*?)</booktitle>", line):
                for term in re.split("[^0-9a-zA-Z_]", bookTitle):
                    if len(term) > 2:
                        out.write('o-' + term.lower() + ':' + key[0] + '\n')

            for author in re.findall("<author>(.*?)</author>", line):
                for term in re.split("[^0-9a-zA-Z_]", author):
                    if len(term) > 2:
                        out.write('a-' + term.lower() + ':' + key[0] + '\n')

    out.close()
    return


def parse_years(file):
    out = open("years.txt", 'w')
    file.seek(0)

    for line in file:
        key = re.findall('key="(.*?)"', line) # key is a list, hence key[0] below

        if len(key) != 0:
            for years in re.findall("<year>(.*?)</year>", line): # capture group () in regex makes only that phrase be captured. In this case, phrase without <year> tags.
                for year in re.split("[^0-9a-zA-Z_]", years):
                    out.write(year + ':' + key[0] + '\n')

    out.close()
    return


def parse_recs(file):
    out = open("recs.txt", 'w')
    file.seek(0)

    for line in file:
        key = re.findall('key="(.*?)"', line)

        if len(key) != 0:
            out.write(key[0] + ':' + line)

    out.close()
    return
    
   
def main():
    path = input("Please enter the path to the XML file: ")
    file = open(path, 'r')

    parse_terms(file)
    parse_years(file)
    parse_recs(file)

    file.close()
    return


if __name__ == '__main__':
    main()
