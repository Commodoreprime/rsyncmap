The way this program works is by almost "supercharging" Rsync / Rclone (referred to collectivly as *rsync*), as in,
rsync will iterate over a directory and rules will be added as per defined by any number of `.syncmap` files.
In the case of Rsync specifically, filter rules can be prepended that control what is is copied.

Within a `.syncmap` there a a few defined operations:
- `FROM-TO`
- `ARGS`
- `NEGATION`

With the exception of `ARGS`, operations that are valid will be negated via filter rules to which rsyncmap will execute special operations
per operation, notably when dealing with `FROM-TO` operations.