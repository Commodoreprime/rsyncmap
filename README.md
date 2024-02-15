# rsyncmap
Python based rsync wrapper that allows controlling where files and directories should be copied to on a per directory basis

---
# This branch
the `rewrite` branch is for revamping the codebase to be more "streamlined". Whether this will work or not, who knows!

See [TODO](TODO.md) for more information.

---
## Syntax

The majority of time spent when using this wrapper will be in `.syncmap` files.
They operate similarly to how `.gitignore` files work when specifying file names.

All operators are optional however (at least) the root of the source directory must have a `.syncmap` file present.

The `.syncmap` file understands the following operations:

### The `FROM-TO` operator

Syntax: `FROM => TO`.

If FROM is not specified it will assume same directory as `.syncmap`
therefore, `=> 'New Directory'` is equivilant to: `. => 'New Directory'` which is also equivilant to `* => 'New Directory'`.

If TO is not specified it will assume the same directory name as FROM therefore if FROM is also not specified it acts the same as if there was no .syncmap file in the first place (or if it was empty). A direct mapping from the FROM base directory to the TO base directory.

If FROM is a file and TO is a directory, FROM will be placed in the TO directory with the same file name, also, if TO is a file and FROM is a directory then TO is written into as if it were a directory if it is possible.

Glob syntax can be used but only on the FROM side.

It is recommended to quote the entire path when specifying a path with spaces.

Example: ` 'foo/biz/foo and biz go up the hill.txt' => 'story 1.txt' `

The => symbol is not bi-directional.

### The `ARGS` operator

Syntax: `:[-] ARGS`.

If a line starts with a colon (:), anything after will be considered additional arguments passed to rsync and passed as-is.

If and when declared at some point in the syncmap file it will be added to future mappings for the duration of the file. Additionally, any additional `ARGS` operation will be added ontop.

An optional minus (-) can be specified directly after the colon to remove any arguments specified. There **must** be a space between the minus and following arguments. If an argument cannot be found it will fail silently and continue.

### The `NEGATION` operator

syntax: `! PATH`.

If a line starts with an exclamation mark (!), the path specified after will not be copied to the destination directory. The space between the exclamation mark and the path is optional.

Glob patterns apply with this operation.

# Comments

`.syncmap` files can contain comments.
They are the same as standard single line comments found in multiple programming languages (Bash, Python, Rust, etc..)
```txt
# This is ignored
informational-directory => BACKUP-AT-ALL-COSTS # Anything after the pound sign is ignored, unless quoted
```


# `.syncmap` file diagram
```txt
: <ARG 1> <ARG 2> ...
FROM => TO # Comment
# Comment
:- <ARG 2>
=> TO
!NEGATION
# Comment
FROM =>
```

---
## Examples

Given the following file structure:

```
_dest
└── ...

foobiz
├── awesome.txt
├── dirA/
│   └── dirAA/
│       └── .syncmap
├── dirB/
│   └── secrets
└── .syncmap
```

The `.syncmap` file that is parent to foobiz has the following contents:

```
dirB/ => Bprotected/
: -anv
awesome.txt => oldspice/fantasia/
```

and the `.syncmap` file that is the parent of dirAA has:

```
=> newdirAA/
```
