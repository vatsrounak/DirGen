import os
import sys
import re

def parse_structure(input_lines, target_path):
    if not input_lines:
        return

    # Parse root directory from the first line
    root_line = input_lines[0].strip()
    root_name = root_line.split('#')[0].strip().rstrip('/')
    root_path = os.path.join(target_path, root_name)
    os.makedirs(root_path, exist_ok=True)

    stack = [root_path]

    for line in input_lines[1:]:
        line = line.rstrip('\n')
        if not line.strip():
            continue  # Skip empty lines

        # Split line into indentation and entry parts
        match = re.match(r'^(.*?)(├── |└── )(.*)$', line)
        if not match:
            continue  # Skip lines that don't match the expected pattern

        indentation_part = match.group(1)
        entry_part = match.group(3).split('#')[0].strip()  # Remove comments

        # Determine if the entry is a directory or file
        if entry_part.endswith('/'):
            entry_name = entry_part.rstrip('/')
            is_directory = True
        else:
            entry_name = entry_part
            is_directory = False

        # Calculate depth based on indentation part length (each level is 4 characters)
        indentation_length = len(indentation_part)
        depth = (indentation_length // 4) + 1  # root is depth 0, first child is depth 1

        # Adjust the stack to the current depth
        while depth < len(stack):
            stack.pop()

        parent_dir = stack[-1]
        full_path = os.path.join(parent_dir, entry_name)

        if is_directory:
            os.makedirs(full_path, exist_ok=True)
            stack.append(full_path)
        else:
            # Ensure parent directory exists
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            # Create an empty file
            open(full_path, 'a').close()

if __name__ == '__main__':
    print("Arguments received:", sys.argv)  # Debug print
    if len(sys.argv) != 3:
        print("Usage: python gen_dir.py <structure_file> <target_path>")
        sys.exit(1)

    structure_file = sys.argv[1]
    target_path = sys.argv[2]
    print("Structure file:", structure_file)  # Debug print
    print("Target path:", target_path)        # Debug print

    try:
        with open(structure_file, 'r') as f:
            input_lines = f.readlines()
        parse_structure(input_lines, target_path)
        print(f"Directory structure created successfully in {target_path}")
    except FileNotFoundError:
        print(f"Error: Structure file '{structure_file}' not found.")
    except Exception as e:
        print(f"Error: {e}")