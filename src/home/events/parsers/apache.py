import re

HOST = r'^(?P<host>.*?)'
SPACE = r'\s'
IDENTITY = r'\S+'
USER = r'\S+'
TIME = r'(?P<time>\[.*?\])'
REQUEST = r'\"(?P<request>.*?)\"'
STATUS = r'(?P<status>\d{3})'
SIZE = r'(?P<size>\S+)'
REGEX = HOST+SPACE+IDENTITY+SPACE+USER+SPACE+TIME+SPACE+REQUEST+SPACE+STATUS+SPACE+SIZE+SPACE

def apache(log_line):
    match = re.search(REGEX,log_line)
    return {
        "host": match.group('host'),
        "time": match.group('time'), 
        "request": match.group('request'),
        "status": match.group('status'),
        "size": match.group('size'),
    }
