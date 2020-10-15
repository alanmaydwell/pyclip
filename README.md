# pyclip

Tool for creating generated strings in clipboard.    

Inspired by perclip by James Bach and Danny Faught.

Written in Python 3 and requires pyclip module.

Has some built-in instructions

# add_comma
Tool for adding commas and single quotes to contents of clipboard.    

Requires pyperclip module.


For example, if clipboard contains:

```
One
Two
Three
```

When run it will change the clipboard content to:

```
'One',
'Two',
'Three'
```

Idea is for convenience when pasting into SQL in clauses but could be used
elsewhere too.