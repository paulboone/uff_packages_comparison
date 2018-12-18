"""
Type (UFF) list of MOF (cif) files using Autografs.
"""
from autografs.utils.mmanalysis import analyze_mm
import ase
import os
import sys

def type_mof(filename, output_dir, ff="uff", output_files=True):
    if ff.lower() == "uff":
       library="rappe"
    elif ff.lower() == "uff4mof":
        library="uff4mof"
    else:
       raise Exception("ff = %s not supported yet" % ff)

    mof = ase.io.read(filename)


    bonds, types = analyze_mm(mof, library=library)

    if output_files:
        mof_name = os.path.splitext(os.path.basename(filename))[0]
        with open(os.path.join(output_dir, mof_name + ".log"), 'w') as f:
            f.write("NOTE: types order is the same as the CIF input file.\n")
            f.write("types= %s" % str(types))

    uniq_types = sorted(set(types))
    return [str(i) for i in uniq_types]
