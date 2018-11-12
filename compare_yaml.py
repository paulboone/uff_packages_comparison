import sys

import numpy as np
import yaml

file1 = sys.argv[1]
file2 = sys.argv[2]

y1 = yaml.load(open(file1, 'r'))
y2 = yaml.load(open(file2, 'r'))

mof_keys = list(y1.keys())
mof_keys.sort()

ok_mofs = 0
num_mofs_in_common = 0

type_diffs = {}

for mof in mof_keys:
    mof1_atoms = set(y1[mof])
    if not mof in y2:
        continue

    num_mofs_in_common += 1
    mof2_atoms = set(y2[mof])

    if mof1_atoms == mof2_atoms:
        print("%s: OK" % mof)
        ok_mofs += 1
    else:
        print("%s: %s <=> %s" % (mof, mof1_atoms - mof2_atoms, mof2_atoms - mof1_atoms))
        key = "%s <=> %s" % ( mof1_atoms - mof2_atoms, mof2_atoms - mof1_atoms)
        if key in type_diffs:
            type_diffs[key] += 1
        else:
            type_diffs[key] = 1

print("Num ok mofs: %d / %d " % (ok_mofs, num_mofs_in_common))

diff_pairs = [(type_diffs[key], key) for key in type_diffs]
diff_pairs.sort(reverse=True)
for diff_pair in diff_pairs:
    print("%d: %s" % (diff_pair[0], diff_pair[1]))
