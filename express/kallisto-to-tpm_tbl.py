#!/usr/bin/env python3
import sys


def read_tsv(filename_tsv):
    rv = dict()
    f = open(filename_tsv, 'r')
    tokens = f.readline().strip()
    for line in f:
        tokens = line.strip().split("\t")
        tmp_id = tokens[0]
        tmp_tpm = float(tokens[4])
        rv[tmp_id] = tmp_tpm
    f.close()
    return rv


filename_conf = sys.argv[1]
# sample_name   filename

sample_list = []
tx_list = []
tpm_list = dict()
f_conf = open(filename_conf, 'r')
for line in f_conf:
    (sample_name, tmp_filename) = line.strip().split("\t")
    tpm_list[sample_name] = read_tsv(tmp_filename)
    tx_list += list(tpm_list[sample_name].keys())
    sample_list.append(sample_name)
f_conf.close()

tx_list = sorted(list(set(tx_list)))
f_out = open('%s.kallisto.txt' % (filename_conf.replace('.conf', '')), 'w')
f_out.write('SeqID\t%s\n' % ('\t'.join(sample_list)))
for tmp_tx in tx_list:
    out_str = []
    for tmp_sample in sample_list:
        if tmp_sample in tpm_list and tmp_tx in tpm_list[tmp_sample]:
            out_str.append('%.3f' % tpm_list[tmp_sample][tmp_tx])
        else:
            out_str.append('%.3f' % (0.0))
    f_out.write('%s\t%s\n' % (tmp_tx, '\t'.join(out_str)))
f_out.close()
