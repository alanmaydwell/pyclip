#!/usr/bin/env python3
"""
Add various types of text to clipboard for pasting
"""

import time
import pyperclip

def hello():
    """Welcome message"""
    print("Pyclip")
    print("Creates types of string in clipboard ready for pasting.")
    print("Inspired by perlclip by James Bach and Danny Faught")
    print("Type help for help.")


def help():
    text = """
This program puts text into the clipboard based on a pattern you specify.

Enter Python expression and the result will be copied to the clipboard.
For example

    "Hello!" * 3       # Hello!Hello!Hello!
    "a" * (2 ** 16)    # string of "a" that is 65536 characters long
    chr(13) * 10       # ten carriage returns

    "\r\n".join([str(i) for i in range(10)]) # Counting digits, each on a
                         separate line.

Also some convenience functions can be included:

    asn - Arrest Summons Number in valid format. Partly based on Unix time.

    counterstring {num} [{char}] to produce text

    cs {num) [{char}] does the same as above


    now() - Integer Unix time in seconds
    now - as above but usual terminal brackets are not required

    nowf() - floating point Unix time in seconds
    now - as above but usual terminal brackets are not required

    textfile {fileanme} - read file

    CHR256() - all 256 ASCII characters
    CHR256 - as above but usual terminal brackets are not required.

A history of the last 10 expressions is kept and accessed as follows:
    !- display contents of history ()
    !! - repeat the last item
    !-1 - another way of repeating the last item
    !-2 - repeat next to last item
    !0 - repeat the first item in history
    !9 - repeat the 10th item in history

Note much of the above could be achieved on the standard Python REPL console but
this lacks automatic clipboard copy. Also some functions here can be called
without the usual terminal brackets- asn help, now, nowf (this is optional)
"""
    print(text)
    return text


def counterstring(target_length=64, marker="*"):
    """Create and return a counterstring.
    This is a string consisting of numbers and markers, constructed such
    that the number *before* each marker gives the position of the marker.
    Args:
        target (int) - target length
        marker (str) - marker character (should be 1 char)
    Returns:
            generated counterstring
    """
    marker = marker[:1]
    # Make minimal starting counterstring
    result = "2" + marker
    # The current value of the counting number
    counting_no = 2
    while len(result) < target_length:
        # Current number of digits in counting number
        cn_len = len(str(counting_no))
        # Increase the counting number (+ 1 on end for marker)
        counting_no = len(result) + cn_len + 1
        # Need to cope with counting number gaining more digits
        if len(str(counting_no)) > cn_len:
            counting_no += 1
        result = result + str(counting_no) + marker
    result = result[:target_length]
    return result

def textfile(filename):
    """Read and return the contents of a file"""
    with open(filename, "r") as infile:
        return infile.read()

def now():
    """Return Unix time in seconds"""
    return  str(int(time.time()))

def nowf():
    """Return Unix time with fractional seconds"""
    return time.time()

def asn():
    "Make an ASN based on Unix time with a valid check digit."""
    start = "1234AA"
    end = str(round(time.time(), 3)).replace(".", "")
    return asn_maker(start + end)


def add_brackets(text):
    """Take supplied text, add () brackets to end of certain words and
    return modified text. Purpose is to enable certain functions to be
    called using eval without having to add () to the function name."""
    items = text.split(" ")
    function_names = ("asn", "now", "nowf", "help")
    new_items = [item + "()" if item in function_names else item for item in items]
    return " ".join(new_items)

def asn_maker(asn):
    """Calculates ASN check digit from first 19 characters of ASN
        Args:
            asn - first 19 characters of ASN, eg 1223AA8900000000000
        Returns:
            asn with check digit on end, eg 1223AA8900000000000M
    """
    if len(asn) != 19:
        result = "Error: 19 characters needed but "+str(len(asn))+" supplied."
    else:
        # Re-arrange digits
        sasn = asn[2:4] + asn[6:8] + asn[0:2] + asn[8:19]
        # Calc check-digit number
        try:
            let_pos = int(sasn) % 23
        except ValueError:
            result = "Error: non-numerical characters present in positions other than 5 and 6."
        else:
            # Map to check letter
            letters = 'ZABCDEFGHJKLMNPQRTUVWXY'
            result = asn + letters[let_pos]
    return result

def history_get(history, text):
    """Either show history or return an item from it
    Args
        history - list containing history
        text - value used to access/display the history. Works as follows:
               ! - print history and return ""
               !! - return last item in history
               !<index number> - (e.g. !0, !9, !-2) Return specified item.
               If value after the ! is invalid (ValueError or IndexError),
               display error message and return ""."""
    # Display contents of history, then return
    if text == "!":
        print("Last ten items:")
        for index, item in enumerate(history):
            print("({})".format(index), item)
        return ""
    # Get most recent item index number
    if text == "!!":
        index = -1
    # Get numerical index number
    else:
        try:
            index = int(text[1:])
        except ValueError as err:
            print("History value error:", err)
            return ""
    # Retrieve item from history
    try:
        response = history[index]
    except IndexError as err:
        print("History index error:", err)
        response = ""
    return response


# An alias for counterstring
cs = counterstring

# All ASCII chars
CHR256 = "".join([chr(i) for i in range(1, 256)])


# Input loop
if __name__ == "__main__":
    hello()
    history = [""] * 10
    while True:
        text = input(">")
        text = add_brackets(text)

        # History retrieval and management
        if text.startswith("!"):
            text = history_get(history, text)
        else:
            history.append(text)
            del history[0]
        # If we have text, evaluate it and paste result to clipboard
        if text:
            try:
                result = eval(text)
            except Exception as err:
                print("Evaluation error:", err)
            else:
                pyperclip.copy(str(result))
                print("<ready to paste!>")
                