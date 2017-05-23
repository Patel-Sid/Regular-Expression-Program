"""
# Copyright Nick Cheng, Brian Harrington, Danny Heap, Siddharth Patel, 2013,
# 2014, 2015, 2016
# Distributed under the terms of the GNU General Public License.
#
# This file is part of Assignment 2, CSCA48, Winter 2016
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see <http://www.gnu.org/licenses/>.
"""

# Do not change this import statement, or add any of your own!
from regextree import RegexTree, StarTree, DotTree, BarTree, Leaf

# Do not change anything above this comment except for the copyright
# statement

# Student code below this comment.
# Store all the values that we will be using to make it easier
zero = '0'
one = '1'
two = '2'
e = 'e'
bar = '|'
dot = '.'
star = '*'
left = '('
right = ')'


def is_regex(s):
    '''(string) -> bool
    This function will compare any given string and if it is a valid regular
    expression then it will return True otherwise it will return False
    >>>is_regex('((1*.(0|2**)**)**.0**)')
    True
    >>>is_regex('(((0***.1)|2)|2***)')
    True
    >>>is_regex('((0.(0|0)*).0***)')
    True
    >>>is_regex('((1.(e|2))|(1|2))')
    True
    >>>is_regex('')
    False
    >>>is_regex('(1*)')
    False
    >>>is_regex('(0.(1.(0|2)*))')
    True
    >>>is_regex("(1***.(0|(2.(1|e)*)**)***)*****")
    True
    '''
    # Base Case if the string has length one
    if len(s) <= 1:
        # Return True iff the string is either: zero, one, two or epsilon
        if (s is zero) or (s is one) or (s is two) or (s is e):
            return True
        # False otherwise
        else:
            return False
    else:
        # Check for the second rule
        if s[-1] is star:
            return is_regex(s[:-1])
        # This condition is mainly for all_regex_permutations so it checks
        # if any condition is met then return False directly
        elif ((s[0] is right and s[-1] is left) or (s[0] is right and
              s[-1] is right) or (s[0] is left and s[-1] is left)):
                return False
        # If we have a regex that follows the third rule then check if left
        # and right are both brackets
        else:
            # Remove the brackets
            s = s[1:-1]
            # If we have an empty string or string of length 1 then return
            # False since it is invalid
            if len(s) < 2:
                return False
            # If we have a left sided regex that means we have to divide the
            # string from the right hand side
            elif s[0] is left and s[-1] is not right:
                # Find the position of the dot and the bar
                find_dot = s.rfind(dot)
                find_bar = s.rfind(bar)
                # Whichever is highest, we will divide at that point
                if find_dot > find_bar:
                    # If dot has higher index then partition string at the dot
                    # from the right
                    s = s.rpartition(dot)
                    # Condition for all_regex_permutations to make it
                    # more efficient
                    if s[0] is not '' and s[2] is not '':
                        return is_regex(s[0]) and is_regex(s[2])
                    else:
                        return False
                else:
                    # If bar has higher index then partition string at the bar
                    # from the right
                    s = s.rpartition(bar)
                    # Condition for all_regex_permutations to make it
                    # more efficient
                    if s[0] is not '' and s[2] is not '':
                        return is_regex(s[0]) and is_regex(s[2])
                    else:
                        return False
            # If we have a right sided regex that means we have to divide the
            # string from the left hand side
            elif s[-1] is right and s[0] is not left:
                # Find the position of the dot and the bar
                find_dot = s.find(dot)
                find_bar = s.find(bar)
                # Whichever is lowest, we will divide at that point
                if ((find_dot is not -1 and find_dot < find_bar) or
                   (find_bar is -1)):
                    # If dot has lower index then partition string at the dot
                    # from the left
                    s = s.partition(dot)
                    # Condition for all_regex_permutations to make it
                    # more efficient
                    if s[0] is not '' and s[2] is not '':
                        return is_regex(s[0]) and is_regex(s[2])
                    else:
                        return False
                else:
                    # If bar has lower index then partition string at the bar
                    # from the left
                    s = s.partition(bar)
                    # Condition for all_regex_permutations to make it
                    # more efficient
                    if s[0] is not '' and s[2] is not '':
                        return is_regex(s[0]) and is_regex(s[2])
                    else:
                        return False
            # If we have an even regex
            elif s[0] is left and s[-1] is right:
                # Set the counter
                i = 0
                # Loop through the string to find the position of dot or bar
                # so we know where to partition the string at
                while i < len(s):
                    # Since the dot or bar was not found, it's not a proper
                    # regex so return False
                    if i == len(s)-2:
                        return False
                    # Loop for ).( or )|( and when we find the index exit the
                    # loop
                    elif s[i] is right and s[i+2] is left:
                        index = i+1
                        i = len(s)
                    i += 1
                # Split the string at the index found and recurse
                return is_regex(s[:index]) and is_regex(s[index+1:])
            # If no brackets are found on either side of the string
            elif s[0] is not left and s[-1] is not right:
                # Check if the last char is a star
                if s[-1] is star:
                    # If it is then remove it as it is proper and add back the
                    # brackets so we can recurse on the rest of the string
                    s = s[:-1]
                    s = left + s + right
                    return is_regex(s)
                # If dot is found in the string then split it at that point
                elif dot in s:
                    s = s.partition(dot)
                    # And recurse on the left and right letters
                    return is_regex(s[0]) and is_regex(s[2])
                # If bar is found in the string then split it at that point
                elif bar in s:
                    s = s.partition(bar)
                    # And recurse on the left and right letters
                    return is_regex(s[0]) and is_regex(s[2])
                # Otherwise none of the conditions were met so return False
                else:
                    return False
            # Otherwise we have the base case for the third rule which is
            # either of the form (r1.r2) or (r1|r2)
            else:
                # Look for the dot
                if dot in s:
                    # Seperate the string at the dot so we can check if r1 and
                    # r2 are valid
                    s = s.partition(dot)
                    return is_regex(s[0]) and is_regex(s[2])
                # Look for the bar
                elif bar in s:
                    # Seperate the string at the bar so we can check if r1 and
                    # r2 are valid
                    s = s.partition(bar)
                    return is_regex(s[0]) and is_regex(s[2])
                # Otherwise the string does not meet the requirements so
                # return False
                else:
                    # Otherwise we have an invalid regex so return False
                    return False


def all_regex_permutations(s):
    '''(str) -> set
    This function will take any string and return a set of all valid regex
    permutations possible
    >>>all_regex_permutations("*1*")
    {'1**'}
    >>>all_regex_permutations('(0.1)|2')
    set()
    >>>all_regex_permutations(")(2|0")
    {'(0|2)', '(2|0)'}
    >>>all_regex_permutations("((0.1).1)")
    {'(1.(0.1))', '(1.(1.0))', '((1.0).1)', '(0.(1.1))', '((1.1).0)',
    '((0.1).1)'}
    '''
    # Create an empty set to store all the permutations
    my_set = set()
    # Get the set of all the permutations
    S = perms(s)
    # Loop through all the elements in the set
    for element in S:
        # If the string is a valid regex expression
        if is_regex(element):
            # Then add it to our set
            my_set.add(element)
    # Return the set
    return my_set


def perms(s):
    '''(str) -> set
    This function will take any string and return the number of possible
    permutations possible in a list
    >>>perms('aab')
    ['aab', 'aba', 'baa']
    >>>perms('aabb')
    ['baab', 'baba', 'abba', 'bbaa', 'abab', 'aabb']
    '''
    # If there is an empty string or a string with one letter
    if len(s) <= 1:
        # Return the original string
        return [s]
    else:
        # Create empty set to store all permutations
        my_set = set()
        # First get all the possible permutations having length N-1
        result = perms(s[1:])
        letter = s[0]
        # Go through all the permutations having length N-1
        for permutate in result:
            # Place each character in all the locations possible without
            # repition
            for i in range(len(permutate) + 1):
                my_set.add(permutate[:i] + letter + permutate[i:])
        return my_set


def regex_match(r, s):
    '''(Leaf/Star/Bar/Dot Tree, str) -> bool
    REQ: r must be a valid regex tree
    This function will check whether the string s matches the regex tree at r
    and will return True if it does otherwise it will return False.
    >>>r = Leaf('e')
    >>>regex_match(r,'')
    True
    >>>r = Leaf('0')
    >>>regex_match(r,'0')
    True
    >>>r = StarTree(Leaf('1'))
    >>>regex_match(r,'')
    True
    >>>regex_match(r,'11111111111111111111')
    True
    >>>r = BarTree(Leaf('2'),StarTree(Leaf('0')))
    >>>regex_match(r,'2')
    True
    >>>regex_match(r,'0')
    True
    >>>regex_match(r,'00000000000000000000000')
    True
    >>>r = DotTree(DotTree(Leaf('2'),Leaf('0')),DotTree(Leaf('1'),Leaf('0')))
    >>>regex_match(r,'2010')
    True
    >>>r = DotTree(BarTree(Leaf('2'),Leaf('0')),BarTree(Leaf('1'),Leaf('0')))
    >>>regex_match(r,'00')
    True
    >>>regex_match(r,'20')
    True
    >>>regex_match(r,'21')
    True
    >>>regex_match(r,'01')
    True
    >>>r = DotTree(BarTree(Leaf('2'),Leaf('0')),Leaf('1'))
    regex_match(r,'21')
    True
    >>>regex_match(r,'20')
    False
    >>>regex_match(r,'01')
    True
    >>>regex_match(r,'10')
    False
    >>>r = DotTree(DotTree(Leaf('1'),Leaf('2')),Leaf('0'))
    >>>regex_match(r,'012')
    False
    >>>regex_match(r,'120')
    True
    >>>regex_match(r,'')
    False
    >>>r = DotTree((Leaf('1')),StarTree(Leaf('2')))
    >>>regex_match(r,'12')
    True
    >>>regex_match(r,'122222222')
    True
    >>>regex_match(r,'1')
    True
    >>>regex_match(r,'1222212')
    False
    >>>regex_match(r,'')
    False
    >>>r = StarTree(DotTree(Leaf('1'),Leaf('0')))
    >>>regex_match(r,'')
    True
    >>>regex_match(r,'10')
    True
    >>>regex_match(r,'1010101')
    False
    >>>regex_match(r,'01')
    False
    >>>regex_match(r,'1010101010')
    True
    '''
    # Check if r is a StarTree
    if r.get_symbol() is star:
        # Get the leaf of the StarTree
        r1 = r.get_children()
        # Check is the string is empty then return True
        if (s == ''):
            return True
        # If we have a StarTree as a child then recurse on it
        elif (r1[0].get_symbol() is star):
            return regex_match(r1[0], s)
        # If we have a BarTree as a child then recurse on it
        elif (r1[0].get_symbol() is bar):
            return star_bar_check(r1[0], s)
        # If we have a DotTree as a child then recurse on it
        elif (r1[0].get_symbol() is dot):
            return star_dot_check(r1[0], s)
        # Else we have a Leaf
        else:
            # Recurse on every single character of s and check if it is equal
            # to
            # the symbol of the leaf
            if(s[0] == r1[0].get_symbol()):
                return regex_match(r, s[1:])
            # Otherwise return False
            else:
                return False
    # Check if r is a DotTree
    elif r.get_symbol() is dot:
        # Get the left and right children
        left_child = r.get_left_child()
        right_child = r.get_right_child()
        # Get the symbols of the children
        r1 = left_child.get_symbol()
        r2 = right_child.get_symbol()
        # If we have regex of the form: (r1*.r2*)
        if (r1 is star) and (r2 is star):
            # Then recurse on the left child (r1*) and right child respectively
            # (r2*)
            pass
        # If we have regex of the form: (r1*.r2) or ((r1.r2).r2)
        elif ((r1 is star) and (r2 is not star) or
              ((r1 is dot) and (r2 is not dot))):
            # Then recurse so that all the conditions are meet as given in
            # handout
            return (regex_match(left_child, s[:-1]) and
                    regex_match(right_child, s[-1:]))
        # If we have regex of the form: (r1.r2*) or (r1.(r1.r2))
        elif ((r2 is star) and (r1 is not star) or ((r2 is dot) and
                                                    (r1 is not dot))):
            # Then recurse so that all the conditions are meet as given in
            # handout
            return (regex_match(left_child, s[:1]) and
                    regex_match(right_child, s[1:]))
        # If we have regex of the form: ((r1|r2).r2) or (r1.(r1|r2)) or
        # ((r1|r2).(r1|r2))
        elif (r1 is bar) or (r2 is bar):
            # Recurse on the left and right child only if the length is two
            if len(s) == 2:
                return (regex_match(left_child, s[0]) and
                        regex_match(right_child, s[1]))
            # Otherwise return False
            return False
        # If we have regex of the form: ((r1.r2).(r1.r2))
        elif (r1 is dot) and (r2 is dot):
            # Find the index to split on and recurse on both the children
            return (regex_match(left_child, s[:len(s)//2]) and
                    regex_match(right_child, s[len(s)//2:]))
        # Otherwise we have the base case so just call the helper function
        else:
            return dot_check(left_child, right_child, s)
    # Check if r is a BarTree
    elif r.get_symbol() is bar:
        # Get the left and right children
        left_child = r.get_left_child()
        right_child = r.get_right_child()
        # Get the symbols of the children
        r1 = left_child.get_symbol()
        r2 = right_child.get_symbol()
        # If the symbol is anything other than leaf then recurse on the left
        # and the right children
        if ((r1 is star) or (r2 is star) or (r1 is bar) or (r2 is bar) or
           (r1 is dot) or (r2 is dot)):
            return regex_match(left_child, s) or regex_match(right_child, s)
        # Otherwise we have a Leaf so call the helper
        else:
            return bar_check(left_child, right_child, s)
    # Otherwise we have Leaf
    else:
        # Return True iff the symbol of leaf matches that of the string or
        # if the leaf tree has symbol e then check for empty string s
        if (r.get_symbol() is s and r.get_symbol() is not e) or \
           (r.get_symbol() is e and s is ''):
            return True
        # Otherwise return False
        else:
            return False


def bar_check(left_child, right_child, s):
    '''(Child, Child, str) -> bool
    REQ: both left_child and right_child must be valid
    REQ: s must be greater than 0
    Helper function for the BarTree, it check the base case.
    '''
    # Check if the length of the string is 1
    if len(s) == 1:
        # If either the left or the right child is equal to the string then
        # return True
        if left_child.get_symbol() is s[0] or right_child.get_symbol() is s[0]:
            return True
        # Else the string matches neither of the children so return False
        else:
            return False
    # String is not of length 1 so return False
    else:
        return False


def dot_check(left_child, right_child, s):
    '''(Child, Child, str) -> bool
    REQ: both left_child and right_child must be valid
    REQ: s must be greater than 0
    Helper function for the DotTree, it checks the base case.
    '''
    # Check if the length of the string is 2
    if len(s) == 2:
        # If left child is equal to the first letter and right child is
        # equal to the second letter then return True
        if ((left_child.get_symbol() is s[0]) and
           (right_child.get_symbol() is s[1])):
            return True
        # Else if they don't match return False
        else:
            return False
    # Else our string is not of length 2 so return False
    else:
        return False


def star_bar_check(r, s):
    '''(BarTree, str) -> bool
    REQ: r must be a valid BarTree
    REQ: length of s must be greater than 0
    This is a helper function for the BarTree of the form (r1|r2)*
    '''
    # Get the children of the tree
    left_child = r.get_left_child()
    right_child = r.get_right_child()
    # Check which child matches the first letter so we know that the rest
    # of the string will have to be that char
    if s[0] is left_child.get_symbol():
        char = left_child.get_symbol()
    else:
        char = right_child.get_symbol()
    # If every single letter matches with char then return True else False
    for i in range(len(s)):
        if s[i] is char:
            result = True
        else:
            result = False
    return result


def star_dot_check(r, s):
    '''(DotTree, str) -> bool
    REQ: r must be a valid DotTree
    REQ: length of s must be greater than 0
    This is a helper function for the DotTree of the form (r1.r2)*
    '''
    # Get the children of the tree
    left_child = r.get_left_child()
    right_child = r.get_right_child()
    # We know that (r1.r2) will always result in an even string
    if len(s)/2:
        # If the length is two then
        if len(s) == 2:
            return dot_check(left_child, right_child, s)
        else:
            return star_dot_check(r, s[2:])
    # If the string is odd then return False directly
    else:
        return False


def build_regex_tree(regex):
    '''(str) -> Dot/Bar/Star/Leaf Tree
    REQ: regex must be valid
    This function will take the given valid regex string, then it will build
    the appropriate tree and finally it will return its root
    >>>build_regex_tree('1***')
    StarTree(StarTree(StarTree(Leaf('1'))))
    >>>build_regex_tree('(1|2)')
    BarTree(Leaf('1'), Leaf('2'))
    >>>build_regex_tree('(0.e)')
    DotTree(Leaf('0'), Leaf('e'))
    >>>build_regex_tree('(0.1)')
    DotTree(Leaf('0'), Leaf('1'))
    >>>build_regex_tree('((0.1).2)')
    DotTree(DotTree(Leaf('0'), Leaf('1')), Leaf('2'))
    >>>build_regex_tree('((0.1)|2)')
    BarTree(DotTree(Leaf('0'), Leaf('1')), Leaf('2'))
    >>>build_regex_tree('((0.1)|2*)')
    BarTree(DotTree(Leaf('0'), Leaf('1')), StarTree(Leaf('2')))
    >>>build_regex_tree('((0.1)*|2*)')
    BarTree(StarTree(DotTree(Leaf('0'), Leaf('1'))), StarTree(Leaf('2')))
    >>>build_regex_tree('((0.1)*|2*)*')
    StarTree(BarTree(StarTree(DotTree(Leaf('0'), Leaf('1'))),
    StarTree(Leaf('2'))))
    >>>build_regex_tree("((0.1)|(2.1))")
    BarTree(DotTree(Leaf('0'), Leaf('1')), DotTree(Leaf('2'), Leaf('1')))
    >>>build_regex_tree("((0.1).(2.1))")
    DotTree(DotTree(Leaf('0'), Leaf('1')), DotTree(Leaf('2'), Leaf('1')))
    >>>build_regex_tree("((0|1).(2.1))")
    DotTree(BarTree(Leaf('0'), Leaf('1')), DotTree(Leaf('2'), Leaf('1')))
    >>>build_regex_tree("((0|1).(2.1))*")
    StarTree(DotTree(BarTree(Leaf('0'), Leaf('1')), DotTree(Leaf('2'),
    Leaf('1'))))
    >>>build_regex_tree('(0.(1.(0|2)*))')
    DotTree(Leaf('0'), DotTree(Leaf('1'), StarTree(BarTree(Leaf('0'),
    Leaf('2')))))
    >>>build_regex_tree('(((0***.1)|2)|2***)')
    BarTree(BarTree(DotTree(StarTree(StarTree(StarTree(Leaf('0')))),
    Leaf('1')), Leaf('2')), StarTree(StarTree(StarTree(Leaf('2')))))
    >>>build_regex_tree("(1***.(0|(2.(1|e)*)**)***)*")
    StarTree(DotTree(StarTree(StarTree(StarTree(Leaf('1')))),
    StarTree(StarTree(StarTree(BarTree(Leaf('0'),
    StarTree(StarTree(DotTree(Leaf('2'), StarTree(BarTree(Leaf('1'),
    Leaf('e'))))))))))))
    '''
    # If we have a single letter then it has no children hence it will be
    # a leaf
    if len(regex) == 1:
        return Leaf(regex)
    # Otherwise we either have to create a Dot/Bar/Star Tree
    else:
        # If the last character is a star then we have to create a star tree
        if regex[-1] is star:
            return StarTree(build_regex_tree(regex[:-1]))
        else:
            # Remove the brackets
            regex = regex[1:-1]
            # If we have a left sided regex that means we have to divide the
            # string from the right hand side
            if regex[0] is left and regex[-1] is not right:
                # Find the position of the dot and the bar
                find_dot = regex.rfind(dot)
                find_bar = regex.rfind(bar)
                # If the dot is greater in index then partition it at the dot
                if find_dot > find_bar:
                    s = regex.rpartition(dot)
                    # Since we partition it at the dot, build a DotTree
                    return (DotTree(build_regex_tree(s[0]),
                                    build_regex_tree(s[2])))
                else:
                    # Else build the BarTree
                    s = regex.rpartition(bar)
                    return (BarTree(build_regex_tree(s[0]),
                                    build_regex_tree(s[2])))
            # If we have a right sided regex that means we have to divide the
            # string from the left hand side
            elif regex[-1] is right and regex[0] is not left:
                # Find the position of the dot and the bar
                find_dot = regex.find(dot)
                find_bar = regex.find(bar)
                # If the dot is lower in index then partition it at the dot
                if ((find_dot is not -1 and find_dot < find_bar) or
                   (find_bar is -1)):
                    s = regex.partition(dot)
                    # Since we partition it at the dot, build a DotTree
                    return (DotTree(build_regex_tree(s[0]),
                                    build_regex_tree(s[2])))
                else:
                    # Else build the BarTree
                    s = regex.partition(bar)
                    return (BarTree(build_regex_tree(s[0]),
                                    build_regex_tree(s[2])))
            # If we have an even regex
            elif regex[0] is left and regex[-1] is right:
                # Set the counter
                i = 0
                # Loop through the regex to find the position of either the
                # bar of the dot
                while i < len(regex):
                    if regex[i] is right and regex[i+2] is left:
                        index = i+1
                        # Once we get the index set i so we can exit loop
                        i = len(regex)
                    i += 1
                # If there is bar at the given index then build a BarTree
                if regex[index] is bar:
                    return (BarTree(build_regex_tree(regex[:index]),
                                    build_regex_tree(regex[index+1:])))
                # Otherwise just build a DotTree
                else:
                    return (DotTree(build_regex_tree(regex[:index]),
                                    build_regex_tree(regex[index+1:])))
            # If either side do not contain a bracket
            elif regex[0] is not left and regex[-1] is not right:
                # Then check if the last char is a star
                if regex[-1] is star:
                    # Find the dot and the bar since we will be spliting it
                    # from the left side
                    find_dot = regex.find(dot)
                    find_bar = regex.find(bar)
                    # If dot has lower index then bar
                    if ((find_dot is not -1 and find_dot < find_bar) or
                       (find_bar is -1)):
                        s = regex.partition(dot)
                        # Build a DotTree
                        return (DotTree(build_regex_tree(s[0]),
                                        build_regex_tree(s[2])))
                    # Otherwise build a BarTree
                    else:
                        s = regex.partition(bar)
                        return (BarTree(build_regex_tree(s[0]),
                                        build_regex_tree(s[2])))
                # If the regex is of form (r1*.r2) or (r1*|r2)
                elif regex[1] is star:
                    # Find the dot and the bar since we will be spliting it
                    # from the right side
                    find_dot = regex.rfind(dot)
                    find_bar = regex.rfind(bar)
                    # If the dot has higher index then bar
                    if find_dot > find_bar:
                        s = regex.rpartition(dot)
                        # Build the DotTree
                        return (DotTree(build_regex_tree(s[0]),
                                        build_regex_tree(s[2])))
                    else:
                        s = regex.rpartition(bar)
                        # Otherwise build the BarTree
                        return (BarTree(build_regex_tree(s[0]),
                                        build_regex_tree(s[2])))
                # Otherwise if we have regex of form (r1|r2)
                elif bar in regex:
                    # Build a BarTree
                    return (BarTree(build_regex_tree(regex[0]),
                                    build_regex_tree(regex[2])))
                # Otherwise we have regex of form (r1.r2)
                elif dot in regex:
                    # Build a DotTree
                    return (DotTree(build_regex_tree(regex[0]),
                                    build_regex_tree(regex[2])))
            else:
                # Look for the dot
                if dot in regex:
                    # Seperate the string at the dot so we can recurse on r1
                    # and r2
                    s = regex.partition(dot)
                    # Create the Dot Tree
                    return DotTree(Leaf(s[0]), Leaf(s[2]))
                # Look for the bar
                elif bar in regex:
                    # Seperate the string at the bar so we can recurse on r1
                    # and r2
                    s = regex.partition(bar)
                    # Create the Bar Tree
                    return BarTree(Leaf(s[0]), Leaf(s[2]))

def countregex(r):
    return (len(r) - r.count('(') - r.count(')'))