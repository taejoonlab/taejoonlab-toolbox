#!/usr/bin/env python3
import sys
import os
import re

filename_fa = '../rRNA/Escherichia.rRNA.fa'

filename_base = re.sub(r'.fa$', '', os.path.basename(filename_fa))


seq_list = dict()

f_fa = open(filename_fa, 'r')
for line in f_fa:
    if line.startswith('>'):
        seq_h = line.strip().lstrip('>')
        seq_list[seq_h] = []
    else:
        seq_list[seq_h].append(line.strip())
f_fa.close()

# Kmer length
kmer_len = 20

# Targeting 16S rRNA
min_seqlen = 1000
max_seqlen = 2000

total_target_list = []
kmer_list = dict()
for tmp_h in seq_list.keys():
    tmp_seq = ''.join(seq_list[tmp_h])
    tmp_seqlen = len(tmp_seq)
    if tmp_seqlen < min_seqlen or tmp_seqlen > max_seqlen:
        continue

    tmp_seqId = tmp_h.split('.')[0]
    total_target_list.append(tmp_seqId)

    #sys.stderr.write('Processing %s\n' % tmp_seqId)
    for tmp_i in range(0, tmp_seqlen-kmer_len):
        tmp_kmer = tmp_seq[tmp_i:tmp_i + kmer_len]
        if tmp_kmer not in kmer_list:
            kmer_list[tmp_kmer] = []
        kmer_list[tmp_kmer].append(tmp_seqId)

f_freq = open('%s.kmer_freq' % filename_base, 'w')
f_missed = open('%s.kmer_missed' % filename_base, 'w')
total_target_set = set(total_target_list)
len_total_target_list = len(list(total_target_set))
sys.stderr.write('Total Target Seq: %d\n' % len_total_target_list)
for tmp_kmer in kmer_list.keys():
    tmp_target_set = set(kmer_list[tmp_kmer])
    tmp_target_list = sorted(list(tmp_target_set))
    len_tmp_target_list = len(tmp_target_list)
    tmp_kmer_pct = len_tmp_target_list*100.0/len_total_target_list

    f_freq.write("%s\t%d\t%.2f\n" %
                     (tmp_kmer, len_tmp_target_list, tmp_kmer_pct))

    if tmp_kmer_pct > 95:
        tmp_missed_set = total_target_set - tmp_target_set
        tmp_missed_list = sorted(list(tmp_missed_set))
        f_missed.write("%s\t%s\n" % (tmp_kmer, ';'.join(tmp_missed_list)))
f_missed.close()
f_freq.close()
