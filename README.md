# Firmware Diffing Tool

## Introduction

Hi! This is a Python script I built for my cybersecurity course to help identify what changed between two different versions of firmware.

Usually, Security researchers use a technique called firmware diffing to find out which files were modified in the latest update. The concept is pretty simple: 

- calculate the cryptographic fingerprint (hash) of each file in the root filesystem and compare the fingerprints of files that have the same name (and path).

## How It Works
To calculate a file's cryptographic fingerprint on Linux, several command-line tools are available depending on the hashing algorithm you want:

- `md5sum`
- `sha1sum`
- `sha256sum`
- `sha512sum`


Note: ``MD5`` and ``SHA1`` are not recommended anymore since they're vulnerable to collision attacks. However, for this project, I'm using ``SHA256`` for the cryptographic hash.`

## Features

This Python 3 script compares two firmware versions and provides:

- ``SHA256`` hashes for exact file comparison
- ``ssdeep`` (fuzzy hashing) to detect similar but modified files
- Similarity scores (between 0 and 1) to measure how close two files are
- Detection of added, deleted, and modified files
- ``JSON`` output for easy parsing and integration with other tools

## Prerequisites

The script requires the following Python libraries: ``pathlib``, ``hashlib``, ``ssdeep``, ``argparse`` and ``Json``.

So you may need to install the required external library. Be aware that ssdeep is not natively available on Windows. If you're on Windows, you can use WSL, VM or Docker.

## Usage 

```sh
python3 firmware_diff.py /path/to/source/firmware /path/to/destination/firmware
```

## Output Format

```sh
{
  "source_firmware": "...",
  "destination_firmware": "...",
  "files": [
    {
      "path": "",                    // full file path from firmware root
      "filename": "...",              // filename only (e.g. 'ls')
      "source_hash": "...",           // SHA256 of file from source firmware
      "destination_hash": "...",      // SHA256 of file from dest firmware
      "source_ssdeep": "...",         // source file's ssdeep hash
      "destination_ssdeep": "...",    // destination file's ssdeep hash
      "ssdeep_similarity": "..."      // ssdeep similarity measure (between 0 and 1)
    }
  ]
}
```

## Demo 

Here's an example of running the script on two firmware versions:

```sh
python3 firmware_diffing.py ~/firmwares/RV130X_FW_1.0.3.44.bin_extract/2097184-19591200.squashfs_v4_le_extract ~/firmwares/RV130X_FW_1.0.3.45.bin_extract/2097184-19591200.squashfs_v4_le_extract | jq .
```

Here's a sample of the output:

```sh
"source_ssdeep": "96:VrPxgUYr1Ryv6rpPQmiKSPaQAJn911p1jz1l/1MPGluiZCt3Rd:G1Ydj",
      "destination_ssdeep": "96:VrPxgUYr1Ryv6rpPQmiKSPaQAJn911p1jz1l/1MPGluiZCt3Rd:G1Ydj",
      "ssdeep_similarity": 1
    },
    {
      "path": "www/workmode.asp",
      "filename": "workmode.asp",
      "source_hash": "7d1cfc4b4f14867e9359cfe72f4e318c7c071e8ac5ca157a99cf924bd9e3fa88",
      "destination_hash": "7d1cfc4b4f14867e9359cfe72f4e318c7c071e8ac5ca157a99cf924bd9e3fa88",
      "source_ssdeep": "48:F9gnDr2ysThDbxzSH5yF1W+0slM+QoDg2fPC8OqrP9mP9mP90P9rTP9+3Pi33Mew:F9GSySlzSHbAeCNFa2wNrg3Pi33MevcN",
      "destination_ssdeep": "48:F9gnDr2ysThDbxzSH5yF1W+0slM+QoDg2fPC8OqrP9mP9mP90P9rTP9+3Pi33Mew:F9GSySlzSHbAeCNFa2wNrg3Pi33MevcN",
      "ssdeep_similarity": 1
    }
  ]
}
```

In this example, the file workmode.asp is identical in both firmware versions (similarity score of 1.0).

# Contact 

Feel free to reach out via :

- Email: elfaijahanas@gmail.com 
- LinkedIn : https://www.linkedin.com/in/anaselfaijah/