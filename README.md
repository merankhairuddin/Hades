# HADES - Hidden Artifact Detection &amp; Extraction Suite

This is an enhanced fork of the original [Ryoshi](https://github.com/fkie-cad/ryoshi) rootkit detection utility. It extends the original capabilities with new features including hybrid memory analysis, incremental scanning, output formatting, digital signing, and audit logging.


## Key Features

- Detect hidden files on UNIX systems using disk metadata comparison
- **Memory analysis** (via Volatility3) for hybrid rootkit detection
- **Incremental scanning** and `--watch` live mode
- Output formats: JSON, CSV, and text
- Digital signing of extracted evidence
- Audit logging with session replay


## Installation

### Dependencies

- Python 3.8+
- Volatility3 (`pip install volatility3`)
- Dissect library (`pip install dissect`) for Python scanner


## Usage Examples

### Disk Scan (Default)
```bash
sudo python3 dissect/dscan.py /dev/sda1 /mnt /evidence
```

### Memory Scan
```bash
sudo python3 memory/analyze.py --memdump /captures/memdump.raw --output /evidence/memory_report.json
```

### Incremental Scan with State File
```bash
sudo python3 dissect/dscan.py /dev/sda1 /mnt /evidence --state-file .ryoshi_state.json
```

### Watch Mode
```bash
sudo python3 dissect/dscan.py /dev/sda1 /mnt /evidence --watch 60  # rescan every 60 seconds
```

### Output Format: JSON or CSV
```bash
sudo python3 dissect/dscan.py /dev/sda1 /mnt /evidence --output-format json
```

### Digital Signing of Evidence
```bash
sudo python3 dissect/dscan.py /dev/sda1 /mnt /evidence --sign-evidence --gpg-key forensic@example.org
```

### Audit Logging and Replay
```bash
# During scan:
sudo python3 dissect/dscan.py /dev/sda1 /mnt /evidence --audit-log ryoshi_audit.jsonl

# To replay:
sudo python3 core/logger.py --replay ryoshi_audit.jsonl
```


## Project Structure

```
hades-main/
├── README.md
├── .gitignore
├── setup.py
├── requirements.txt
├── dissect/
│   └── dscan.py
├── tsk/
│   ├── Makefile
│   └── scan.c
├── .github/
│   └── ISSUE_TEMPLATE/
│       └── bug_report.md
├── dev/
│   ├── README.md
│   └── .keep
├── core/
│   └── logger.py
└── memory/
    └── analyze.py
```


## Credits
This project builds upon the excellent work by FKIE-CAD on [Ryoshi](https://github.com/fkie-cad/ryoshi).
