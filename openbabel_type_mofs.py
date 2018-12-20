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

def type_mof(filename, output_dir, ff="uff", output_files=True):

    obconversion = OBConversion()
    obconversion.SetInAndOutFormats("cif", "xyz")
    obmol = OBMol()

    # Read MOF file and unit cell and write xyz file
    obconversion.ReadFile(obmol, filename)
    unitcell = openbabel.toUnitCell(obmol.GetData(openbabel.UnitCell))
    uc = [unitcell.GetA(), unitcell.GetB(), unitcell.GetC(), unitcell.GetAlpha(), unitcell.GetBeta(), unitcell.GetGamma()]
    obconversion.WriteFile(obmol, 'mof_tmp.xyz')

    # Replicate unit cell using angstrom
    mol = Molecule(read='mof_tmp.xyz')
    mol.set_cell(uc)
    n_atoms = len(mol.atoms)

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

    if output_files:
        mof_name = os.path.splitext(os.path.basename(filename))[0]
        with open(os.path.join(output_dir, mof_name + "-obabel.log"), 'w') as f:
            f.write("NOTE: types order is the same as the CIF input file.\n")
            f.write("types= %s" % str(types))

    uniq_types = sorted(set(types))
    return [str(i) for i in uniq_types]
