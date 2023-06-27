
with open(r'table\out.data.text', 'r') as infile, open(r'table\out.csv', 'w', newline='') as outfile:
    txt = infile.read()
    txt=txt.replace('|',',').replace('<NEWLINE>','\n')
    outfile.write(txt)
