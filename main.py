import PyPDF2 as pdf
import re

def str_tokenizer(exp):
    li = re.split(r'\+|\=', exp)
    li = list(map(str.strip, li))
    return li



def rex_grouping(tokenized_exp):
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

    return [filename, p_start, p_end]



def metadata_parser(exp):
    metadata = []
    tokens = str_tokenizer(exp)
    out_file = tokens.pop()

    for t in tokens:
        metadata.append(rex_grouping(t))

    return metadata, out_file



def extract_pages(info, op_file):
    writer = pdf.PdfFileWriter()
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

                with open(op_file, 'wb') as outfile:
                    writer.write(outfile)



metadata, outfile = metadata_parser('merge.pdf[1:5] + merge.pdf[:3] = new2.pdf')
print(metadata, outfile)

extract_pages(metadata, outfile)
