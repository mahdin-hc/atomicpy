import argparse
import csv
import os
from elements import Element, Molecule, Compound, load_elements, load_molecules, parse_formula, draw_periodic_table

def main():
    parser = argparse.ArgumentParser(description="Chemical Compound Parser")
    parser.add_argument("-pt", action="store_true", help="Draw periodic table")
    parser.add_argument("-e", action="store_true", help="Show electron configurations")
    parser.add_argument("formula", type=str, help="Chemical formula to parse")
    
    args = parser.parse_args()
    
    # Load elements and molecules data from CSV files
    elements_csv_path = os.path.join("data", "elements.csv")
    molecules_csv_path = os.path.join("data", "molecules.csv")

    load_elements(elements_csv_path)
    load_molecules(molecules_csv_path)

    # Parse the chemical formula
    compound, err = parse_formula(args.formula)
    if err:
        print(err)
        return

    molecule = compound.to_molecule()
    
    print()

    # Draw the periodic table if the draw command is used
    if args.pt:
        draw_periodic_table(molecule)
        print()
    
    # Output chemical information
    name = compound.get_name()
    el = Element.element_table.get(args.formula)
    if el:
        name = el.name

    print(f"  Molecule : {compound.to_string()}")
    print(f"  Simplify : {compound.to_molecule().simplify()}")
    print(f"  Name     : {name}")
    if compound.state:
        print(f"  State    : {compound.state}")
    print(f"  Mass     : {compound.get_mass()}")
    print(f"  Charge   : {compound.get_charge()}")
    if el:
        print(f"  Number   : {el.number}")
        print(f"  Category : {el.category}")
        print(f"  Fact     : {el.fact}")
    print()

    # Show electron configurations if -e is passed
    if args.e:
        printed = set()
        for el in molecule.elements:
            if el.symbol not in printed:
                print(f"  {el.symbol}({el.number}): {el.get_electron_configuration()}")
                printed.add(el.symbol)

if __name__ == "__main__":
    main()
