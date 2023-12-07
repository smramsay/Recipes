#!/usr/bin/env python
"""Formats markdown tables, though technically they are Pandoc markdown."""

import fileinput

from argparse import ArgumentParser
from pathlib import Path
from itertools import groupby

parser = ArgumentParser()
parser.add_argument('file', type=Path,
                    help="The file with tables to fix.")
parser.add_argument('-n', '--no-backup', action='store_true',
                    help="Disable backing up the file before writing.")
parser.add_argument('-t', '--test', action='store_true',
                    help="Write just the new tables to a separate file.")
args = parser.parse_args()


def is_dividing_line(line: str) -> bool:
    # We require lines starting with '|' with make the first index empty
    return line.split('|')[1][-1] in ['-', ':']


def format_columns(table_lines: [str]) -> [str]:
    """Pad columns to match their longest entry.
       Iterates through all columns.
    """
    if len(table_lines) <= 2:
        print("Tables must have more than two lines.")
        return table_lines

    # Count the number of columns in the header.
    num_col = len(table_lines[0].split('|'))
    final_lines = table_lines
    for column_idx in range(1, num_col):
        # Find the length of the longest entry in this column that isn't a
        # dividing line.
        max_len = max(
            [len(line.split('|')[column_idx].strip())
             for line in table_lines
             if len(line.split('|')) > column_idx
             and not is_dividing_line(line)]
        )

        # Pad the entries; special case for dividing line.
        new_lines = []
        for line in final_lines:
            entries = line.strip().split('|')
            # Pad the number of entries to match the number of header columns
            entries += [''] * (num_col - len(entries))
            entry_text = entries[column_idx].strip()

            # TODO: Use alignment indicators instead of justifying left.
            if is_dividing_line(line):
                # Reset the length to the minimum so we can remake it.
                entry_text = ':-'

            # TODO: Should work on all entry_text, right?
            if len(entry_text) <= max_len:
                fill = '-' if is_dividing_line(line) else ' '

                # +1 to add space after longest entry
                new_entry = entry_text.ljust(max_len + 1, fill)
                if is_dividing_line(line):
                    new_entry += '-'
                else:
                    # Adding a single space to separate it from the '|'
                    new_entry = ' ' + new_entry

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

    if args.test:
        with open('/tmp/table-test.md', 'w') as testfile:
            testfile.writelines([x + '\n' for x in new_lines])
        return

    replace_tables_inplace(args.file, new_lines)


if __name__ == '__main__':
    main()
