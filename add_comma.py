#!/usr/bin/env python3
"""
Function for adding quotation marks and comma to lines in supplied text

When run directly will apply this function to the contents of clipboard
and copy the result back to clipboard.
"""
import pyperclip

def add_comma(text):
    """Receive a multi-line text add single quote to start and end of each 
    line and a comma on the end of each except the last. Return the
    result.
    eg turns
    
    One 
    Two 
    Three
    
    into
    
    'One',
    'Two',
    'Three'
    """
    lines = text.splitlines()
    for line_i, line in enumerate(lines[:-1]):
        lines[line_i] = "'{}',\n".format(line)
    # Don't want comma at end of last line
    lines[-1] = "'{}'\n".format(lines[-1])
    return "".join(lines)

if __name__ == "__main__":
    text = pyperclip.paste()
    text = add_comma(text)
    pyperclip.copy(text)
    print("Clipboard contents updated")
