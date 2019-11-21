import PyPDF2 as pdf
import re
import os
import sys
import getopt

def print_help():
    print('HELP')   # TODO

def parse_cl_args():
    exp = None
    dirt = None
    bm = True

    options, rem = getopt.getopt(sys.argv[1:], 'e:d:h', ['nb'])

    for opt, arg in options:
        if opt == '-e':
            exp = arg
        elif opt == '-d':
            dirt = arg
        elif opt == '-h':
            print_help()
        elif opt == '--nb':
            bm = False

    return (exp, dirt, bm)



def str_tokenizer(exp):
    li = re.split(r'\+|\=', exp)
    li = list(map(str.strip, li))
    return li



def rex_grouping(tokenized_exp, dirt=None):
    rex = re.compile(r'(.*)(?:\[(\d+)?:(\d+)?\])')
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
        dirt = dirt.replace('\\', '\\')
        filename = dirt + filename

    return [filename, p_start, p_end]



def metadata_parser(exp, dirt=None):
    metadata = []
    tokens = str_tokenizer(exp)
    out_file = tokens.pop()

    for t in tokens:
        metadata.append(rex_grouping(t, dirt))

    return metadata, out_file



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
exp, dirt, bm = parse_cl_args()
metadata, outfile = metadata_parser(exp, dirt)
extract_pages(metadata, outfile, bm)



# dirt = input("Enter dir: ")
# metadata, outfile = metadata_parser('pdf (1).pdf[1:5] + pdf (3).pdf[:3] = new2.pdf', dirt)
# print(metadata, outfile)

# extract_pages(metadata, outfile)
