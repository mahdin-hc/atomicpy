import csv
import os
import re
from colorama import init, Fore, Style

class Element:
    element_table = {}

    def __init__(self, symbol, category, number, group, amu, fact, period, phase, name, colour, charge):
        self.symbol = symbol
        self.category = category
        self.number = number
        self.group = group
        self.amu = amu
        self.fact = fact
        self.period = period
        self.phase = phase
        self.name = name
        self.colour = colour
        self.charge = charge

    def __str__(self):
        if self.charge > 1:
            return f"{self.symbol}+{self.charge}"
        elif self.charge < -1:
            return f"{self.symbol}{self.charge}"
        elif self.charge == -1:
            return f"{self.symbol}-"
        elif self.charge == 1:
            return f"{self.symbol}+"
        return self.symbol

    def get_electron_configuration(self):
        return generate_electron_configuration(self.number)

class Molecule:
    def __init__(self, elements, charge=0, name="", state=""):
        self.elements = elements
        self.charge = charge
        self.name = name
        self.state = state

    def to_compound(self):
        return Compound([self], self.charge, self.state)

    def simplify(self):
        return ''.join(el.symbol for el in self.elements)

    def to_string(self):
        count = 1
        prev_sym = ""

        str_rep = ""
        for i, el in enumerate(self.elements):
            if i == 0:
                prev_sym = str(el)
                continue

            if str(el) == prev_sym:
                count += 1
            else:
                str_rep += prev_sym
                if count > 1:
                    str_rep += str(count)
                prev_sym = str(el)
                count = 1

        str_rep += prev_sym
        if count > 1:
            str_rep += str(count)

        if self.charge == 1:
            str_rep += "+"
        elif self.charge == -1:
            str_rep += "-"
        elif self.charge > 1:
            str_rep += f"+{self.charge}"
        elif self.charge < -1:
            str_rep += str(self.charge)

        return str_rep

    def get_mass(self):
        return sum(el.amu for el in self.elements)

class Compound:
    compound_table = {}

    def __init__(self, molecules, charge=0, state="", name=""):
        self.molecules = molecules
        self.charge = charge
        self.state = state
        self.name = name

    def to_string(self):
        count = 1
        prev_sym = ""
        str_rep = ""

        for i, mol in enumerate(self.molecules):
            if i == 0:
                prev_sym = mol.to_string()
                continue

            if mol.to_string() == prev_sym:
                count += 1
            else:
                if count > 1:
                    str_rep += f"({prev_sym}){count}"
                else:
                    str_rep += prev_sym
                prev_sym = mol.to_string()
                count = 1

        if count > 1:
            str_rep += f"({prev_sym}){count}"
        else:
            str_rep += prev_sym

        if self.charge == 1:
            str_rep += "+"
        elif self.charge == -1:
            str_rep += "-"
        elif self.charge > 1:
            str_rep += f"+{self.charge}"
        elif self.charge < -1:
            str_rep += str(self.charge)

        return str_rep

    def to_molecule(self):
        elements = []
        for m in self.molecules:
            elements.extend(m.elements)
        return Molecule(elements, self.charge, self.name, self.state)

    def get_mass(self):
        return sum(m.get_mass() for m in self.molecules)

    def get_charge(self):
        charge = self.charge
        for m in self.molecules:
            charge += m.charge
            charge += sum(el.charge for el in m.elements)
        return charge

    def get_name(self):
        names = [self.name]
        for mol in self.molecules:
            if mol.name:
                names.append(mol.name)
        return ', '.join(names)

def load_elements(filepath):
    with open(filepath, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for record in reader:
            number = int(record[2])
            group = int(record[3])
            amu = float(record[4])
            period = int(record[6])
            element = Element(record[0], record[1], number, group, amu, record[5], period, record[7], record[8], record[9], 0)
            Element.element_table[element.symbol] = element

def load_molecules(filepath):
    with open(filepath, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for ri, record in enumerate(reader):
            if len(record) < 3:
                raise ValueError(f"Invalid record: insufficient columns at line {ri + 2}")
            formula, name, state = record
            compound, err = parse_formula(formula)
            if err:
                raise ValueError(f"Error parsing formula '{formula}': {err}")
            compound.name = name
            compound.state = state
            Compound.compound_table[compound.to_string()] = compound

def parse_formula(formula):
    pattern = r'([A-Z][a-z]*)(\d*)'
    matches = re.findall(pattern, formula)
    
    elements = []
    charge = 0
    state = ""
    
    for symbol, count in matches:
        count = int(count) if count else 1
        element = Element.element_table.get(symbol)
        # if not element:
            # return None, f"Element '{symbol}' not found"
        
        elements.extend([element] * count)

    return Compound([Molecule(elements)], charge, state), None


# Initialize colorama
init(autoreset=True)

def draw_periodic_table(molecule):
    # Create a 2D grid for the main periodic table (7 periods, 18 groups)
    table = [["" for _ in range(18)] for _ in range(7)]

    # Create separate lists for Lanthanides and Actinides
    lanthanides = [""] * 15  # 57 (La) to 71 (Lu)
    actinides = [""] * 15    # 89 (Ac) to 103 (Lr)

    # Populate the main table with element symbols
    for element in Element.element_table.values():
        if 57 <= element.number <= 71:
            lanthanides[element.number - 57] = element.symbol
        elif 89 <= element.number <= 103:
            actinides[element.number - 89] = element.symbol
        elif element.period <= 7 and element.group <= 18 and element.group > 0:
            table[element.period - 1][element.group - 1] = element.symbol

    # Check which elements are in the molecule for highlighting
    highlighted = {el.symbol: True for el in molecule.elements}

    # Print the main periodic table, highlighting elements in the molecule
    print("\nPeriodic Table:\n")
    for row in table:
        for el in row:
            if el == "":
                print("    ", end="")  # Print empty space for empty slots
            elif el in highlighted:
                print(f"{Fore.GREEN}{el:4}{Style.RESET_ALL}", end="")  # Highlight element in green
            else:
                print(f"{el:4}", end="")
        print()

    # Print the Lanthanide series, highlighting elements in the molecule
    # print("\nLanthanides:")
    print("\n")
    print("        ", end="")
    for el in lanthanides:
        if el in highlighted:
            print(f"{Fore.GREEN}{el:4}{Style.RESET_ALL}", end="")  # Highlight element in green
        else:
            print(f"{el:4}", end="")
    print()

    # Print the Actinide series, highlighting elements in the molecule
    # print("Actinides:")
    print("        ", end="")
    for el in actinides:
        if el in highlighted:
            print(f"{Fore.GREEN}{el:4}{Style.RESET_ALL}", end="")  # Highlight element in green
        else:
            print(f"{el:4}", end="")
    print()


def generate_electron_configuration(number):
    # Basic configuration logic
    configuration = ""
    shells = [2, 8, 18, 32]
    electrons = number

    for i, shell in enumerate(shells):
        if electrons <= 0:
            break
        if electrons > shell:
            configuration += f"{shell} "
            electrons -= shell
        else:
            configuration += f"{electrons} "
            break

    return configuration.strip()

