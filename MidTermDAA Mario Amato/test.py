from DNAContamination import *


def test(s,k,l):
    obj = DNAContamination(s, l)
    file = open("target_batch.fasta", "r")

    while True:
        line_n = file.readline()
        if not line_n:
            file.close()
            break
        line_n = int(line_n[1:])
        cnt = file.readline()
        to_add = DNAContamination.Contaminat(cnt[:len(cnt)-1], line_n)
        obj.addContaminant(to_add)
    file.close()
    lista = obj.getContaminants(k)
    lista.sort(reverse=False)

    stringa = ""
    for i in lista:
        if i == lista[-1]:
            stringa += str(i)
            break
        stringa += str(i) + ", "

    return stringa

