# Standard Python libraries
from __future__ import (absolute_import, print_function,
                        division, unicode_literals)

# http://www.numpy.org/
import numpy as np

# https://wiki.fysik.dtu.dk/ase/
try:
    import ase
    has_ase = True
except:
    has_ase = False

def dump(system, elements):
    """
    Convert an atomman.System and list of elements into an ase.Atoms.
    
    Parameters
    ----------
    system : atomman.System
        A atomman representation of a system.
    elements : list
        A list of unique elemental symbols to pair with system's atypes.
    
    Returns
    -------
    aseatoms : ase.Atoms
        An ase representation of a collection of atoms.
    prop : dict
        Dictionary containing any extra per-atom properties to include.
    """
    
    assert has_ase, 'ase not imported'
    
    # Get box/cell information
    cell = system.box.vects
    pbc = system.pbc
    
    # Get element information
    elements = np.asarray(elements)
    atype = system.atoms.atype
    symbols = elements[atype-1]
    
    # Get atomic information
    positions = system.atoms.pos
    prop = {}
    for p in system.atoms_prop():
        if p != 'atype' and p != 'pos':
            prop[p] = system.atoms_prop(key=p)
    
    # Build Atoms
    aseatoms = ase.Atoms(symbols=symbols, positions=positions, pbc=pbc, cell=cell)
    
    return aseatoms, prop