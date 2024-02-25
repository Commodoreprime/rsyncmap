# rsyncmap
Wrapper for rsync / rclone that simply adds directory redirection via a `.syncmap` file.

# Command Syntax
`rsyncmap [ARGS ...] SOURCE_DIRECTORY DESTINATION_DIRECTORY`

The wrapper will try to be as transparent as possible, as such, the absolute last argument is the destination and second to last is the source directory.
Anything in between will be considered as an argument meant to be passed to rsync and will be done so as-is.

# `.syncmap` file syntax
The file syntax is very simple. Essentially all it has is one directive:
```
FROM => TO
```
The FROM is the directory relative to the source directory tree that should be redirected to the TO which is relative to the destinations directory tree.

The wrapper also collects filter rules that are passed to rsync directly using the `--filter` argument.
This is equivlent to placing a `.rsync-filter` file in the FROM directory to be processed by rsync.

For example, they are defined like so in a `.syncmap` file:
```
foo => biz
- Forgetme/
+ dontforgetme!/
zam => true
- Foobar/
- verysecrets/
```

will result in these commands (when `rsyncmap --verbose --dry-run -aPh tests/foobiz/ tests/_dest` is ran):
```
rsync --verbose --dry-run -aPh --filter=- Forgetme/ --filter=+ dontforgetme!/ tests/foobiz/foo tests/_dest/biz
rsync --verbose --dry-run -aPh --filter=- Foobar/ --filter=- verysecrets/ tests/foobiz/zam tests/_dest/true
```

If there is no redirection directive, the wrapper will assume a direct source to dest transaction, adding filter rules if any are present.

However, if the wrapper does not find a `.syncmap` file in the root of the source directory, it will give up.

# Caveats and Tips

### Rsync caveats
This wrapper assumes very little so rsync oddities must be kept in mind, for example, in order to transfer the *contents* of a directory (not the directory itself) the path must end with a slash:
```
Like-this/ => to-this
```
this will result in a tree that looks like:
```
to-this
 └─ <Like-this contents ...>
```

Instead of this:
```
to-this
 └─ Like-this
     └─ <like-this contents ...>
```

### Directory duplication
Any directory redirection **does not** exclude it from being copied from the parent, if the parent is specified.

To mitigate this, add a filter rule that blocks the redirection directory from being copied when the parent is being passed:
```
./ => .
- subfoo/
subfoo/ => newfoo
```

### Whitespace
When processing the `.syncmap` file, the wrapper will ignore empty lines
