"""
Type (UFF) list of MOF (cif) files using Autografs.
"""
from autografs.utils.mmanalysis import analyze_mm
import ase
import os
import sys

def type_mof(filename, output_dir, ff="uff"):
    if ff.lower() == "uff":
       library="rappe"
    elif ff.lower() == "uff4mof":
        library="uff4mof"
    else:
       raise Exception("ff = %s not supported yet" % ff)

    mof = ase.io.read(filename)
    mof_name = filename.split('_')[0]

    bonds, types = analyze_mm(mof, library=library)
    uniq_types = sorted(set(types))
    return [str(i) for i in uniq_types]
