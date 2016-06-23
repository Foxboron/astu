ATSU
====

The goal of this project is to create a flexible wrapper around borg.  

UNDER HEAVY DEVELOPMENT


# Features
  * Config file written in yaml
  * Hooks for backup preperation and cleanup
  * Human readable


### Syntax
```
atsu init server
atsu backup home server --no-prune
atsu prune backup 
```

### Config
```
backups:
  home:
    name: "`hostname`-`date +%Y-%m-%d`"
    dir: ~/
    options:
      - stats
      - version
    exclude:
      - '*/.cache/*'
      - '*/.local/*'
      - '*/Downloads/*'
      - '*/Media/*'
  usb:
    dir: ~/Media
    options:
      - stats
      - v

repositories:
  server:
    repository: "user@backupserver.fake"
    env:
      BORG_PASSPHRASE: "hunter2"
    prune:
      prefix: "`hostname`-"
      keep:
        daily: 7
        weekly: 4
        monthly: 6

```

### Hooks
```
$ cat ./hooks/home/pre-backup.sh
# Backup pacman package listing
pacman -Q > ~/.package-list

$ cat ./hooks/home/post-backup.sh
rm ~/.package-list
```


