from bsddb3 import db
import shlex


# iterates through all key-values in c database
def iterate(c, para, result, outFull, re, ra=None):
    it = c.first()
    while it:

        # checking for range parameter
        if ra:
            if ra == 1 and int(it[0]) > int(para):

                # Outputting full or just key
                if outFull:
                    result.append(re.get(it[1]))
                else:
                    result.append(it[1])
            elif ra == -1 and int(it[0]) < int(para):
                # Outputting full or just key
                if outFull:
                    result.append(re.get(it[1]))
                else:
                    result.append(it[1])
        elif it[0] == para:

            # Outputting full or just key
            if outFull:
                result.append(re.get(it[1]))
            else:
                result.append(it[1])
        it = c.next()

    return


def main():

    # Opening databases with idx files and creating cursor objects
    re = db.DB()
    re.open('re.idx', None, db.DB_HASH, db.DB_CREATE)

    yr = db.DB()
    yr.open('ye.idx', None, db.DB_BTREE, db.DB_CREATE)
    yrc = yr.cursor()

    te = db.DB()
    te.open('te.idx', None, db.DB_BTREE, db.DB_CREATE)
    tec = te.cursor()

    # Initialize some data
    query = ''
    outputFull = False

    # Loop till user decides to quit
    while query != 'q':
        query = input("Please input a query, output specifier, or q to quit:\n\n> ")

        # Result from query and the amount of conditions needed to satisfy
        result = []
        conditions = 0

        # Changing output type
        if "output=" in query:
            para = query.split('=')
            if para[1] == "full":
                outputFull = True
            elif para[1] == "key":
                outputFull = False
            print("Output is now " + para[1])

        # Querying data
        elif query != 'q':

            # Use shlex split for handling whitespaces in quotations
            data = shlex.split(query)
            conditions += len(data)

            # Loop through each condition
            for para in data:

                # Case-insensitive
                para = para.lower()

                # Split on : for search area and parameter
                if ':' in para:
                    para = para.split(':')

                    # Loop through each parameter for search area
                    for info in para[1].split(' '):
                        if para[0] == 'title':
                            iterate(tec, bytes('t-' + info, 'utf8'), result, outputFull, re)
                        elif para[0] == 'author':
                            iterate(tec, bytes('a-' + info, 'utf8'), result, outputFull, re)
                        elif para[0] == 'other':
                            iterate(tec, bytes('o-' + info, 'utf8'), result, outputFull, re)
                        elif para[0] == 'year':
                            iterate(yrc, bytes(para[1], 'utf8'), result, outputFull, re)

                # Greater then range search
                elif '>' in para:
                    iterate(yrc, bytes(para.split('>')[1], 'utf8'), result, outputFull, re, 1)

                # Less then range search
                elif '<' in para:
                    iterate(yrc, bytes(para.split('<')[1], 'utf8'), result, outputFull, re, -1)

                # Bulk search
                else:
                    iterate(tec, bytes('t-' + para, 'utf8'), result, outputFull, re)
                    iterate(tec, bytes('a-' + para, 'utf8'), result, outputFull, re)
                    iterate(tec, bytes('o-' + para, 'utf8'), result, outputFull, re)

        # set of keys or records
        out = set()

        # Get the keys or records that satisfy the amount of conditions
        for el in result:

            # Add them to a set for uniqueness
            if result.count(el) >= conditions:
                out.add(el)

        # Print each key or record
        for el in out:
            print(el)
        print()

    # Quiting Program
    print("GoodBye")
    return

if __name__ == '__main__':
    main()
