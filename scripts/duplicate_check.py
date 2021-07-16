#!/usr/bin/env python3
#
# Copyright (C) 2018 Whisperity
#
# SPDX-License-Identifier: GPL-3.0
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
Tests for the contents of the repository to only have a variable defined once.
"""
import csv
import os
import sys


def main():
    found_errors = False
    variable_to_source = dict()

    for _, _, files in os.walk(os.getcwd()):
        for file in filter(lambda fn: fn.endswith(".csv"), files):
            with open(file, 'r') as handle:
                current_source = file.replace(".csv", "")
                reader = csv.DictReader(handle)
                for record in reader:
                    var_name = record["Variable"]
                    if var_name == "__META__":
                        continue

                    existing_source = variable_to_source.get(var_name, None)
                    if existing_source:
                        found_errors = True
                        if existing_source == current_source:
                            print("Variable '{}' is defined multiple times "
                                  "in '{}'.".format(var_name, existing_source),
                                  file=sys.stderr)
                        else:
                            print("Variable '{}' duplicated in '{}' and '{}'."
                                  .format(var_name, existing_source,
                                          current_source),
                                  file=sys.stderr)
                    else:
                        variable_to_source[var_name] = current_source

    if found_errors:
        print("Errors encountered, see STDERR output.")
        return 1
    else:
        print("All clear")
        return 0


if __name__ == '__main__':
    sys.exit(main())
