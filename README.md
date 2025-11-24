# PrefetchPy

A Python tool for parsing Windows prefetch files using the libscca-python library.

## Overview

PrefetchPy is a command-line utility that extracts and analyzes information from Windows prefetch (.pf) files. Prefetch files contain metadata about executed applications, including run counts, timestamps, and accessed files.

## Features

- **Single File Analysis**: Parse individual prefetch files
- **Batch Processing**: Process entire directories of prefetch files
- **Timeline Generation**: Create chronological timelines of application executions
- **File Search**: Search for specific filenames across all prefetch files
- **Data Export**: Export parsed data in CSV or JSON formats
- **Flexible Querying**: Extract specific information like run counts and last run times

## Dependencies

- Python 3.x
- `pyscca` (libscca-python) - Library for parsing prefetch files

Install dependencies:
```bash
pip install libscca-python
```

## Usage

### Basic Commands

**Parse a single prefetch file:**
```bash
python prefetch.py -f path/to/file.pf
```

**Show last run time:**
```bash
python prefetch.py -f path/to/file.pf --last-run
```

**Show run count:**
```bash
python prefetch.py -f path/to/file.pf --run-count
```

**List accessed files:**
```bash
python prefetch.py -f path/to/file.pf --open-files
```

### Directory Operations

**Generate execution timeline:**
```bash
python prefetch.py -d path/to/prefetch/directory --timeline
```

**Search for specific files:**
```bash
python prefetch.py -d path/to/prefetch/directory --search "chrome.exe"
```

**Export to CSV:**
```bash
python prefetch.py -d path/to/prefetch/directory --export -o output.csv --format csv
```

**Export to JSON:**
```bash
python prefetch.py -d path/to/prefetch/directory --export -o output.json --format json
```

## Command-Line Options

| Option | Description |
|--------|-------------|
| `-f, --file` | Path to a single prefetch file |
| `-d` | Path to directory containing prefetch files |
| `-v, --verbose` | Enable verbose output |
| `-o, --output` | Specify output file for exports |
| `--last-run` | Display last run time |
| `--run-count` | Display execution count |
| `--open-files` | List files accessed by the application |
| `--timeline` | Generate chronological timeline (requires `-d`) |
| `--search` | Search for filenames (requires `-d`) |
| `--export` | Export parsed data (requires `-d` and `-o`) |
| `--format` | Export format: `json` or `csv` (default: json) |

## Export Formats

### CSV Format
Includes executable name, last run time, and run count:
```csv
executable,last_run,run_count
CHROME.EXE,2024-01-15 14:30:22,145
NOTEPAD.EXE,2024-01-15 12:15:10,23
```

### JSON Format
Includes complete metadata with all accessed files:
```json
[
    {
        "executable": "CHROME.EXE",
        "last_run": "2024-01-15 14:30:22",
        "run_count": 145,
        "files": [
            "C:\\WINDOWS\\SYSTEM32\\NTDLL.DLL",
            "C:\\Program Files\\Google\\Chrome\\chrome.exe"
        ]
    }
]
```

## Examples

**Forensic Timeline Analysis:**
```bash
python prefetch.py -d /path/to/prefetch --timeline
```



**Export for Further Analysis:**
```bash
python prefetch.py -d /path/to/prefetch --export -o analysis.json --format json
```

## Use Cases

- Digital forensics investigations
- System behavior analysis
- Application execution auditing
- Malware analysis
- Incident response

## Author

@jellibeantheargonaut



