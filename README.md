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