import os
import argparse
import re
import logging

def parse_structure(input_lines, target_path):
    if not input_lines:
        return

    # Parse root directory from the first line
    root_line = input_lines[0].strip()
    root_name = root_line.split('#')[0].strip().rstrip('/')
    root_path = os.path.join(target_path, root_name)
    os.makedirs(root_path, exist_ok=True)
    logging.info("Created root directory: %s", root_path)

    stack = [root_path]

    for line in input_lines[1:]:
        line = line.rstrip('\n')
        if not line.strip():
            continue  # Skip empty lines

        # Split line into indentation and entry parts
        match = re.match(r'^(.*?)(├── |└── )(.*)$', line)
        if not match:
            logging.warning("Skipping line due to unexpected format: %s", line)
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
            popped = stack.pop()
            logging.debug("Popped from stack: %s", popped)

        parent_dir = stack[-1]
        full_path = os.path.join(parent_dir, entry_name)

        if is_directory:
            os.makedirs(full_path, exist_ok=True)
            stack.append(full_path)
            logging.info("Created directory: %s", full_path)
        else:
            # Ensure parent directory exists
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            # Create an empty file
            open(full_path, 'a').close()
            logging.info("Created file: %s", full_path)
        logging.debug("Current stack: %s", stack)
    logging.debug("Final stack: %s", stack)

if __name__ == '__main__':

    # Setup logging configuration
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    
    #Argument parser setup
    parser = argparse.ArgumentParser(description='Generate directory structure from a text file.')
    parser.add_argument('structure_file', type=str, help='Path to the structure file.')
    parser.add_argument('target_path', type=str, help='Path to create the directory structure.')
    args = parser.parse_args()
    
    structure_file  = args.structure_file
    target_path = args.target_path


    logging.info("Structure file:", structure_file)  # Debug print
    logging.info("Target path:", target_path)        # Debug print

    try:
        with open(structure_file, 'r') as f:
            input_lines = f.readlines()
        parse_structure(input_lines, target_path)
        logging.info("Directory structure created successfully in %s", target_path)
    except FileNotFoundError:
        logging.error("Error: Structure file '%s' not found.", structure_file)  
    except Exception as e:
        logging.error("Error: %s", e)  
