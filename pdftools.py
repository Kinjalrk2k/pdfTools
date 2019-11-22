import PyPDF2 as pdf
import re
import os
import sys
import getopt
import webbrowser

def print_help():
    print('<HELP>')   # TODO
    print('Please follow the README.md at https://github.com/Kinjalrk2k/pdfTools/blob/master/README.md, for more details')
    print("\nBasic syntax: py pdftools.py -d <directory> -e \"<expression>\" -o <output file> --nb")
    print("-d followed by working directory path")
    print("-e followd by expression to work on in \"\"")
    print("-o followed by output file name")
    print("--nb for no bookmarking at merge ends")
    print("-h to open this help promt\n")
    webbrowser.open("https://github.com/Kinjalrk2k/pdfTools/blob/master/README.md")


def parse_cl_args():
    exp = None
    dirt = None
    bm = True
    outfile = "output.pdf"

    options, rem = getopt.getopt(sys.argv[1:], 'e:d:o:h', ['nb'])

    for opt, arg in options:
        if opt == '-e':
            exp = arg
        elif opt == '-d':
            dirt = arg
        elif opt == '-h':
            print_help()
            sys.exit("You prompted the help! Program exited!")
        elif opt == '-o':
            outfile = arg
        elif opt == '--nb':
            bm = False

    if dirt != None:
        dirt = dirt.replace('\\', '\\')
        outfile = dirt + outfile

    return (exp, dirt, bm, outfile)



def str_tokenizer(exp):
    li = re.split(r'\+|\=', exp)
    li = list(map(str.strip, li))
    return li



def rex_grouping(tokenized_exp, dirt=None):
    # rex = re.compile(r'(.*)(?:\[(\d+)?:(\d+)?\])')
    rex = re.compile(r'([^\[|\]|:]+)(?:\[(\d+)?:(\d+)?\])?')
    grps = rex.match(tokenized_exp)

    filename = grps.group(1)

    if grps.group(2) is not None:
        p_start = int(grps.group(2))
    else:
        p_start = 0

    if grps.group(3) is not None:
        p_end = int(grps.group(3))
    else:
        p_end = None

    if dirt != None:
    #     dirt = dirt.replace('\\', '\\')
        filename = dirt + filename

    return [filename, p_start, p_end]



def metadata_parser(exp, dirt=None):
    metadata = []
    if exp == None:
        for f in os.listdir(dirt):
            if f.endswith('.pdf'):
                if dirt == None:
                    metadata.append([f, 0, None])
                else:
                    metadata.append([dirt+f, 0, None])

    else:
        tokens = str_tokenizer(exp)
        # out_file = tokens.pop()

        for t in tokens:
            metadata.append(rex_grouping(t, dirt))

    return metadata



def extract_pages(info, op_file, bookmark=True):
    writer = pdf.PdfFileWriter()
    p = 0
    for ip_file in info:
        with open(ip_file[0], 'rb') as infile:
            reader = pdf.PdfFileReader(infile)

            p_start = ip_file[1]

            if ip_file[2] is None:
                p_end = reader.getNumPages()
            else:
                p_end = ip_file[2]

            for i in range(p_start, p_end):
                writer.addPage(reader.getPage(i))
                # writer.insertPage(reader.getPage(1))

            if(bookmark):
                writer.addBookmark(os.path.basename(ip_file[0]), p)
                p += (p_end - p_start)

            with open(op_file, 'wb') as outfile:
                writer.write(outfile)



# main
exp, dirt, bm, outfile = parse_cl_args()
metadata = metadata_parser(exp, dirt)
# print(metadata, outfile)
extract_pages(metadata, outfile, bm)



# dirt = input("Enter dir: ")
# metadata, outfile = metadata_parser('pdf (1).pdf[1:5] + pdf (3).pdf[:3] = new2.pdf', dirt)
# print(metadata, outfile)

# extract_pages(metadata, outfile)
