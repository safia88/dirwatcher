# dirwatcher
This program monitors a directory, checking whether text files in the directory contain a particular word.

## Arguments


```
positional arguments:
  path                              Directory path to watch
  magic                             String to watch for

optional arguments:
  -h, --help                        show this help message and exit
  -e EXT, --ext EXT                 Text file extention to watch e.g. .txt, .log
  -i INTERVAL, --interval INTERVAL  Number of seconds between polling

```


## Example Usage

`python dirwatcher.py -e .txt -i 2.0 watchme  'Safia'`

- this starts watching the directory `./watchme` with a polling interval of 2.0 seconds, looking in only files with the extension '.txt' for the phrase 'Safia'

## Example Output 

```
2020-04-06 09:19:01.625 dirwatcher.py INFO    [MainThread  ] 
-------------------------------------------------------------------
   Running dirwatcher.py
   Started on 2020-04-06T09:19:01.625705
-------------------------------------------------------------------

2020-04-06 09:19:01.625 dirwatcher.py INFO    [MainThread  ] Watching dir=watchme for files with extension=.txt containing text=Safia
2020-04-06 09:19:01.625 dirwatcher.py INFO    [MainThread  ] New file: test.txt found in watchme
2020-04-06 09:19:01.626 dirwatcher.py INFO    [MainThread  ] Magic word: Safia found on line: 1 in file: test.txt
2020-04-06 09:19:01.626 dirwatcher.py INFO    [MainThread  ] Magic word: Safia found on line: 3 in file: test.txt
^C2020-04-06 09:19:51.959 dirwatcher.py WARNING [MainThread  ] Received signal: SIGINT
2020-04-06 09:19:51.961 dirwatcher.py INFO    [MainThread  ] 
-------------------------------------------------------------------
   Shutting down dirwatcher.py
   Uptime was 0:00:50.334377
-------------------------------------------------------------------
```