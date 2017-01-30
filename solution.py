import re

assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'

def cross(a, b):
    "Cross product of elements in A and elements in B."
    return [s+t for s in a for t in b]

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

# Using list comprehension to create 2 lists of diagnonal boxes on a sudoku board to add to the unit list
diag_ascending = [[rows[i] + str(i+1) for i in range(0, len(rows))]]
diag_descending = [[rows[len(rows)-i] + cols[i-1] for i in range(1, len(cols)+1)]]
unitlist = row_units + column_units + square_units + diag_ascending + diag_descending

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def eliminate_naked_twins(values, twins, unitlist):
    """Eliminates all naked twin pairs and occurenaces in the each of the unit
    Args:
        values(dict of values): a dictionary of the form {'box_name': '123456789', ...}
        twins(dict of sets): a dictionary of the form values e.g. {'23': 'A1', 'A5' ...}
        unitlist(list of lists): a list containing a list of units (e.g. row, column, square) e.g. [['A1', 'A2', ..] ['B1', 'B2']]

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    
    # Find for every unit, whether there are 'twins' occurences
    for unit in unitlist:

        for i in range(0, len(unit)):
            box1 = unit[i]
            box1_value = values[box1]
            if box1_value in twins:
                for j in range(i + 1, len(unit)):
                    box2 = unit[j]
                    # Find 2 boxes that are both in the twins list, that are from the same unit.
                    if box2 in twins[box1_value]:

                        # Find the other boxes within a unit, not included the twins
                        other_boxes = [box for box in unit if box not in {box1, box2}]

                        # Replace the twin value from each one of the other values using regex, and assign values
                        for unit_boxes in other_boxes:
                            new_values = re.sub('['+''.join(map(str, list(box1_value)))+']', '', values[unit_boxes])
                            assign_value(values, unit_boxes, new_values)
                            values[unit_boxes] = new_values


    return values

def find_naked_twins(values):
    """Finds all instances of naked twins
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        The dictionary of naked twin values, corresponding to a set of box indexes: values e.g. {'23': 'A1', 'A5' ...}
    """
    
    twins = {}

    # Loop through all boxes with 2 values in them
    for box in (box for box in values.keys() if len(values[box]) == 2):
        value = values[box]
        #If the value is already in the twin dict, then add to the corresponding set
        if value in twins:
            twins[value].add(box)
        else:
            twins[value] = {box}

    # Return the naked twins dict with corresponding twin pairs
    return {value: box for (value, box) in twins.items() if len(box) > 1}

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    
    # Find all instances of naked twins
    twins = find_naked_twins(values)

    # Remove Naked twins
    values = eliminate_naked_twins(values, twins, unitlist)

    # return values
    return values

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print

def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            assign_value(values, peer, values[peer].replace(digit,''))
            values[peer] = values[peer].replace(digit,'')
    return values

def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

def reduce_puzzle(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        
        # If the simple strategies do not complete the board, then run naked twins
        if stalled:
            values = naked_twins(values)
            solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
            stalled = solved_values_before == solved_values_after

        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    values = reduce_puzzle(values)
    
    if values is False:
        return False
    if all( len(values[i]) is 1 for i in values):
        return values
        
    # Choose one of the unfilled squares with the fewest possibilities
    unfinished_squares = [ i for i in boxes if len(values[i]) > 1]
    sorted_squares = sorted(unfinished_squares, key=lambda x: len(values[x]))
    search_root = sorted_squares[0]
    
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    # Replace all values
    for x in list(values[search_root]):
        values_new = dict(values)
        assign_value(values_new, search_root, x)
        values_new[search_root] = x
        resulting_sudoku = search(values_new)
        if(resulting_sudoku):
            return resulting_sudoku

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """

    return search(grid_values(grid))

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
