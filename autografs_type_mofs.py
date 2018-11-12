"""
Type (UFF) list of MOF (cif) files using Autografs.
"""
from autografs.utils.mmanalysis import analyze_mm
import ase
import os
import sys

def autografs_type_mofs(mof_dir, output_dir, ff="uff"):

    if ff.lower() == "uff":
        library="rappe"
    elif ff.lower() == "uff4mof":
        library="uff4mof"
    else:
        raise Exception("ff = %s not supported yet" % ff)

    err_mofs = []
    mof_atom_types = {}
    mof_list = os.listdir(mof_dir)

    for idx, filename in enumerate(mof_list, start=1):
        print('%i | %s' % (idx, filename))
        try:
            mof = ase.io.read(os.path.join(mof_dir, filename))
            mof_name = filename.split('_')[0]

            bonds, types = analyze_mm(mof, library=library)
            uniq_types = sorted(set(types))
            mof_atom_types[mof_name] = [str(i) for i in uniq_types]

            # # Save atom types for each mof
            # with open(os.path.join(output_dir, '%s.yaml' % mof_name), 'w') as f:
            #     yaml.dump([str(i) for i in types], f)
        except Exception as e:
            err_mofs.append(filename)
            print("!!!ERROR -> {0}".format(e))

    return mof_atom_types, err_mofs
