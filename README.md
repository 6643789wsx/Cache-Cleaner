# Cache Cleaner

A Python utility to safely clean Cache/cache folders from the C drive.

## Features

- Recursively searches and removes Cache/cache folders
- Skips system-critical directories to prevent system damage
- Detailed logging of all operations
- Reports total space freed and number of folders cleaned

## Usage

Simply run the script:

```bash
python clean_cache.py
```

The script will:
1. Walk through the C drive
2. Identify folders named "Cache" or "cache"
3. Safely delete them while logging all actions
4. Generate a log file with details of the operation

## Safety Features

- Skips system-critical directories (System32, Program Files, etc.)
- Detailed logging of all actions for audit purposes
- Error handling for permission issues and other potential problems
- Confirmation of space freed and folders cleaned

## Log Files

The script creates a log file named `cache_cleanup_YYYYMMDD_HHMMSS.log` containing:
- All deleted folder locations
- Amount of space freed for each folder
- Errors or permission issues encountered
- Summary of total operations

## Warning

This script requires administrative privileges to access certain directories. It's recommended to review the log file after execution to verify the results.
