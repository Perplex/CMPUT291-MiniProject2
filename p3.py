from bsddb3 import db


def iterate(c, para, result, outFull, re, ra=None):
    it = c.first()
    while it:
        if ra:
            if ra == 1 and int(it[0]) > int(para):
                if outFull:
                    result.append(re.get(it[1]))
                else:
                    result.append(it[1])
            elif ra == -1 and int(it[0]) < int(para):
                if outFull:
                    result.append(re.get(it[1]))
                else:
                    result.append(it[1])
        elif it[0] == para:
            if outFull:
                result.append(re.get(it[1]))
            else:
                result.append(it[1])
        it = c.next()

    return


def main():

    re = db.DB()
    re.open('re.idx', None, db.DB_HASH, db.DB_CREATE)

    yr = db.DB()
    yr.open('ye.idx', None, db.DB_BTREE, db.DB_CREATE)
    yrc = yr.cursor()

    te = db.DB()
    te.open('te.idx', None, db.DB_BTREE, db.DB_CREATE)
    tec = te.cursor()

    query = ''
    outputFull = False

    while query != 'q':
        query = input("Please input a query, output specifier, or q to quit:\n\n> ")

        result = []
        conditions = 0

        if "output=" in query:
            para = query.split('=')
            if para[1] == "full":
                outputFull = True
            elif para[1] == "key":
                outputFull = False
            print("Output is now " + para[1])
        elif query != 'q':
            data = query.split(' ')
            conditions += len(data)
            for para in data:
                para = para.lower()
                if ':' in para:
                    para = para.split(':')
                    if para[0] == 'title':
                        iterate(tec, bytes('t-' + para[1], 'utf8'), result, outputFull, re)
                    elif para[0] == 'author':
                        iterate(tec, bytes('a-' + para[1], 'utf8'), result, outputFull, re)
                    elif para[0] == 'other':
                        iterate(tec, bytes('o-' + para[1], 'utf8'), result, outputFull, re)
                    elif para[0] == 'year':
                        iterate(yrc, bytes(para[1], 'utf8'), result, outputFull, re)
                elif '>' in para:
                    iterate(yrc, bytes(para.split('>')[1], 'utf8'), result, outputFull, re, 1)
                elif '<' in para:
                    iterate(yrc, bytes(para.split('<')[1], 'utf8'), result, outputFull, re, -1)
                else:
                    iterate(tec, bytes('t-' + para, 'utf8'), result, outputFull, re)
                    iterate(tec, bytes('a-' + para, 'utf8'), result, outputFull, re)
                    iterate(tec, bytes('o-' + para, 'utf8'), result, outputFull, re)

        out = set()

        for el in result:
            if result.count(el) == conditions:
                out.add(el)

        for el in out:
            print(el)
        print()

    print("GoodBye")
    return

if __name__ == '__main__':
    main()
