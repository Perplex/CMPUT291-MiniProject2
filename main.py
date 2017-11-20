def main():
    path = input("Please enter the path to the XML file: ")
    file = open(path, 'r')
    for line in file:
        print(line)
    return


if __name__ == '__main__':
    main()
