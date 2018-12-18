"""
Type (UFF) list of MOF (cif) files using OpenBabel.
First replicate the unit cell 3x3x3 and type FF for the whole structure,
then read the atom types for the middle cell to get periodic FF atom types.
Painfully slow.
"""
import os
import openbabel
from openbabel import OBMol, OBConversion
from openbabel import OBMolAtomIter, OBForceField
from angstrom import Molecule

def type_mof(filename, output_dir, ff="uff"):

    obconversion = OBConversion()
    obconversion.SetInAndOutFormats("cif", "xyz")
    obmol = OBMol()

    # Read MOF file and unit cell and write xyz file
    obconversion.ReadFile(obmol, os.path.join(mof_dir, filename))
    unitcell = openbabel.toUnitCell(obmol.GetData(openbabel.UnitCell))
    uc = [unitcell.GetA(), unitcell.GetB(), unitcell.GetC(), unitcell.GetAlpha(), unitcell.GetBeta(), unitcell.GetGamma()]
    obconversion.WriteFile(obmol, 'mof_tmp.xyz')

    # Replicate unit cell using angstrom
    mol = Molecule(read='mof_tmp.xyz')
    mol.set_cell(uc)
    mol333 = mol.replicate([3, 3, 3], center=True)
    print(mol333.cell)
    mol333.write('mof333.cif', cell=mol333.cell.to_list())

    # Type FF
    obconversion.ReadFile(obmol, 'mof333.cif')
    ff = OBForceField.FindForceField("UFF")
    if not ff.Setup(obmol):
        print("Error: could not setup force field")
    ff.GetAtomTypes(obmol)

    # Get atom types for the middle cell
    types = []
    for atom_idx, obatom in enumerate(OBMolAtomIter(obmol)):
        if atom_idx >= n_atoms * 13 and atom_idx < n_atoms * 14:
            ff_atom_type = obatom.GetData("FFAtomType").GetValue()
            types.append(ff_atom_type)

    uniq_types = sorted(set(types))
    return [str(i) for i in uniq_types]
