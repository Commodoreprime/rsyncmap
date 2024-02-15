- Rewrite to follow [.gitignore](https://git-scm.com/docs/gitignore#_pattern_format) pattern format. Pathlib might already be able to take care of this... maybe.

- Write to accurately follow how README describes. This program should initially plan to copy everyting from source to dest as-is, then .syncmap files are used to modify this behavior on a per directory basis. THAT is how rsyncmap should work, close to how git tracks files with .gitignore modifying file tracking behavior.
  - This could pose a problem because if it follows strictly the .gitignore pattern formating guidelines then it is possible for a .syncmap file in a subdirectory to modify the direction of files in its parent or even up to the root of the directory (possibly even break out?! That'd be no good... I wonder how git solves this, it might simply ignore any lines that try to go out of the scope of the directory where .git resides).
- ~~Write new operator, the NEGATOR operator. Effectivly any line that starts with a ! will flat out not be copied, globbing works the same way when using this operator.~~

## Steps
1. Gather list of .syncmap files
2. Parse files, creating an operation objects dict-list
3. Create a list of rsync commands
   1. For a given .syncmap file, write a series of --exclude rules that exclude:
      - direction operations
      - negation operations
      - sub-directories that .syncmap files are within (exclude the parent of the .syncmap file)
      This will result in rsync copying everything other than what is specified in a given .syncmap file
4. Execute those commands in order
