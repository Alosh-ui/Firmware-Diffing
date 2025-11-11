#!/usr/bin/env python3
# @author : Anas EL Faijah

import json
import hashlib
import pathlib
import ssdeep
import argparse

def calculate_sha256(file):
    """
    !Note!:
        - "hashlib.file_digest()" (available from Python 3.11+) would be much more optimized,
          but I use the manual method for better "compatibility" (older python versions)
        - Reading by blocks of 4096 bytes (typical disk block size)
    """
    file_hash = hashlib.sha256()
    with open(file, "rb") as f:
        while True:
            block = f.read(4096)
            if not block:
                break
            # update the hash with the read block
            file_hash.update(block)
    # return the hash in hexadecimal (it's kind of the standard) + more readable instead of keeping "raw" bytes ^-^
    return file_hash.hexdigest()

def list_files(folder_path):

    # convert to Path object to facilitate manipulations
    folder_path = pathlib.Path(folder_path)
    files = {}
    for element in folder_path.rglob("*"):
        if element.is_file() and not element.is_symlink():
            relative_path = str(element.relative_to(folder_path)) # convert path to str + better for json display
            files[relative_path] = {
                "absolute_path": element, # complete absolute path of the file (Path object)
                "name": element.name
            }
    return files

def fuzzy_hashing(file_path):

    try:
        return ssdeep.hash_from_file(str(file_path))
    except Exception:
        return None

def analyze_file(file_path):

    result = {
        "sha256": calculate_sha256(file_path),
        "ssdeep": fuzzy_hashing(file_path)
    }
    return result

def process_deleted_files(source_files, deleted):

    results = []
    for file in deleted:
        complete_path_src = source_files[file]["absolute_path"]
        source_fingerprints = analyze_file(complete_path_src)

        results.append({
            "path": file,  # Relative path from firmware root
            "filename": source_files[file]["name"],
            "source_hash": source_fingerprints["sha256"],
            "destination_hash": None,
            "source_ssdeep": source_fingerprints["ssdeep"],
            "destination_ssdeep": None,
            "ssdeep_similarity": None
        })
    return results

def process_added_files(destination_files, added):

    results = []
    for file in added:
        complete_path_dest = destination_files[file]["absolute_path"]
        dest_fingerprints = analyze_file(complete_path_dest)

        results.append({
            "path": file,
            "filename": destination_files[file]["name"],
            "source_hash": None,
            "destination_hash": dest_fingerprints["sha256"],
            "source_ssdeep": None,
            "destination_ssdeep": dest_fingerprints["ssdeep"],
            "ssdeep_similarity": None
        })
    return results

def process_common_files(source_files, destination_files, common):

    results = []
    for file in common:
        complete_path_src = source_files[file]["absolute_path"]
        complete_path_dest = destination_files[file]["absolute_path"]

        source_hash = analyze_file(complete_path_src)
        destination_hash = analyze_file(complete_path_dest)

        # calculate ssdeep similarity between 0 and 1!
        score = None
        src_ssdeep = source_hash["ssdeep"]
        dst_ssdeep = destination_hash["ssdeep"]

        if src_ssdeep is not None and dst_ssdeep is not None:
            try:
                score = ssdeep.compare(src_ssdeep, dst_ssdeep) / 100
            except Exception:
                pass

        results.append({
            "path": file,
            "filename": destination_files[file]["name"],
            "source_hash": source_hash["sha256"],
            "destination_hash": destination_hash["sha256"],
            "source_ssdeep": source_hash["ssdeep"],
            "destination_ssdeep": destination_hash["ssdeep"],
            "ssdeep_similarity": score
        })
    return results

def compare_lists(source_files, destination_files):

    # create sets for comparisons
    source_set = set(source_files.keys())
    destination_set = set(destination_files.keys())

    added = destination_set - source_set
    deleted = source_set - destination_set
    common = source_set & destination_set

    # the results of the three cases
    results = []
    results += process_deleted_files(source_files, deleted)
    results += process_added_files(destination_files, added)
    results += process_common_files(source_files, destination_files, common)

    return results

def compare_firmwares(source, destination):

    src_files = list_files(source)
    dst_files = list_files(destination)

    files = compare_lists(src_files, dst_files)

    # The json + adding sorted for better readability
    result = {
        "source_firmware": str(source),
        "destination_firmware": str(destination),
        "files": sorted(files, key=lambda x: x["path"])
    }

    return result

def main():

    parser = argparse.ArgumentParser(
        description="Compare two extracted firmware versions (file systems)."
    )
    parser.add_argument("source", help="Path to the source firmware folder (old)")
    parser.add_argument("destination", help="Path to the destination firmware folder (new)")
    args = parser.parse_args()

    result = compare_firmwares(args.source, args.destination)

    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()