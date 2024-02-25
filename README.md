# rsyncmap
Wrapper for rsync / rclone that simply adds directory redirection via a `.syncmap` file.

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

If there is no redirection directive, the wrapper will assume a direct source to dest transaction, adding filter rules if any are present.

However, if the wrapper does not find a `.syncmap` file in the immediate directory of the source directory, it will give up.
 
# wrapper command syntax
The wrapper will try to be as transparent as possible, as such, the absolute last argument is the destination and second to last is the source directory.
Anything in between will be considered as an argument meant to be passed to rsync and will be done so as-is.
