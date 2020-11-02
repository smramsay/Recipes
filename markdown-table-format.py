#!/usr/bin/env python
"""Formats markdown tables, though technically they are Pandoc markdown."""

import argparse
import fileinput

from pathlib import Path
from itertools import groupby

parser = argparse.ArgumentParser()
parser.add_argument('file', type=Path,
                    help="The file with tables to fix.")
parser.add_argument('-n', '--no-backup', action='store_true',
                    help="Disable backing up the file before writing.")
args = parser.parse_args()


def format_columns(table_lines: [str]) -> [str]:
    """Pad columns to match their longest entry.
       Iterates through all columns.
    """
    if len(table_lines) <= 2:
        print("Tables must have more than two lines.")
        return table_lines

    # Count the number of columns in the header.
    num_col = len(table_lines[0].strip('|').split('|'))
    final_lines = table_lines
    for column_idx in range(1, num_col + 1):
        # Find the length of the longest entry in this column.
        max_len = max([len(line.split('|')[column_idx]) for line in table_lines])

        # Pad the entries; special case for dividing line.
        new_lines = []
        for line in final_lines:
            entries = line.split('|')
            entry_len = len(entries[column_idx])
            if entry_len < max_len:
                fill = ' '
                if entry_len != 0 and entries[column_idx][-1] == '-':
                    fill = '-'
                new_entry = entries[column_idx].ljust(max_len, fill)
                new_line = '|'.join(entries[:column_idx] + [new_entry] + entries[column_idx + 1:])
                new_lines.append(new_line.strip())
            else:
                new_lines.append(line.strip())

        final_lines = new_lines

    return final_lines


def replace_tables_inplace(filename: Path, new_table_lines: [str]):
    """Replaces the table lines in the file with our formatted lines."""
    # Turn the list into a stack which we can pop from.
    # Technically destroys data in `new_table_lines`, but we don't care.
    new_table_lines.reverse()
    backup = None if args.no_backup else '.bak'
    with fileinput.FileInput(filename, inplace=True, backup=backup) as fs:
        for line in fs:
            # If you start any non-table lines with '|', you've done fucked up.
            if line[0] == '|':
                print(new_table_lines.pop(), end='\n')
            else:
                print(line, end='')


def get_tables(lines: [str]) -> [[str]]:
    """Group lines by whether if they start with '|' or not.
       Returns separate groups of lines that do.
    """
    # TODO: Strip x in case the table is indented?
    return [list(lns) for t, lns in groupby(lines, lambda x: x[0] == '|') if t]


def main():
    with open(args.file) as infile:
        lines = infile.readlines()

    new_lines = []
    for table in get_tables(lines):
        new_lines += format_columns(table)

    replace_tables_inplace(args.file, new_lines)


if __name__ == '__main__':
    main()
