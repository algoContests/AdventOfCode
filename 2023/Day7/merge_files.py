def merge_python_files(output_file, *input_files):
    with open(output_file, 'w') as output:
        # Écrire les imports en premier
        output.write("# Imports\n")
        for input_file in input_files:
            with open(input_file, 'r') as input:
                for line in input:
                    if line.startswith("import ") or line.startswith("from "):
                        output.write(line)

        # Écrire les déclarations de fonctions/classes en second
        output.write("\n# Function and Class Declarations\n")
        for input_file in input_files:
            with open(input_file, 'r') as input:
                for line in input:
                    if not line.startswith("import ") and not line.startswith("from "):
                        output.write(line)

# Exemple d'utilisation :
merge_python_files('merged_output.py', 'Hand.py', 'functions.py', 'constants.py', 'aoc_day7.py')
