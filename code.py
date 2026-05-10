"""
File Integrity Checker
----------------------
A tool that uses cryptographic hash functions (SHA-256, SHA-512, MD5)
to verify the integrity of files in a directory.
 
How it works:
1. CREATE BASELINE: Computes a hash for every file and saves it to baseline.json
2. VERIFY: Re-computes hashes and compares them to the baseline to detect:
     - Modified files (hash changed)
     - Deleted files (existed before, gone now)
     - New files (didn't exist before)
 
Author : <your name>
Course : Computer Security
"""
 
import hashlib
import json
import os
from datetime import datetime
 
 
# ---------- CORE HASHING ----------
 
def compute_hash(filepath, algorithm='sha256', chunk_size=4096):
    """
    Compute the cryptographic hash of a single file.
    Reads the file in chunks so it works with files of any size.
    """
    hash_func = hashlib.new(algorithm)
    try:
        with open(filepath, 'rb') as f:
            # Read in chunks (good for large files)
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                hash_func.update(chunk)
        return hash_func.hexdigest()
    except (IOError, PermissionError):
        return None
 
 
def scan_directory(directory, algorithm='sha256'):
    """Walk a directory and compute the hash of every file inside."""
    file_hashes = {}
    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_hash = compute_hash(filepath, algorithm)
            if file_hash:
                # Use a relative path so the baseline is portable
                rel_path = os.path.relpath(filepath, directory)
                file_hashes[rel_path] = file_hash
    return file_hashes
 
 
# ---------- BASELINE CREATION ----------
 
def create_baseline(directory, baseline_file='baseline.json', algorithm='sha256'):
    """Build a baseline: hash every file in a directory and save the results."""
    print(f"\n[*] Scanning '{directory}' using {algorithm.upper()}...")
    file_hashes = scan_directory(directory, algorithm)
 
    baseline = {
        'directory'  : os.path.abspath(directory),
        'algorithm'  : algorithm,
        'created_at' : datetime.now().isoformat(timespec='seconds'),
        'file_count' : len(file_hashes),
        'files'      : file_hashes,
    }
 
    with open(baseline_file, 'w') as f:
        json.dump(baseline, f, indent=2)
 
    print(f"[+] Baseline created: {len(file_hashes)} files saved to '{baseline_file}'")
    return baseline
 
 
# ---------- INTEGRITY VERIFICATION ----------
 
def verify_integrity(baseline_file='baseline.json'):
    """Verify current files against an existing baseline."""
    if not os.path.exists(baseline_file):
        print(f"[!] Error: Baseline file '{baseline_file}' not found.")
        return None
 
    with open(baseline_file, 'r') as f:
        baseline = json.load(f)
 
    directory  = baseline['directory']
    algorithm  = baseline['algorithm']
    old_hashes = baseline['files']
 
    if not os.path.isdir(directory):
        print(f"[!] Error: Directory '{directory}' no longer exists.")
        return None
 
    print(f"\n[*] Verifying integrity of '{directory}' using {algorithm.upper()}...")
    new_hashes = scan_directory(directory, algorithm)
 
    modified, deleted, new_files, unchanged = [], [], [], []
 
    for path, old_hash in old_hashes.items():
        if path not in new_hashes:
            deleted.append(path)
        elif new_hashes[path] != old_hash:
            modified.append((path, old_hash, new_hashes[path]))
        else:
            unchanged.append(path)
 
    for path in new_hashes:
        if path not in old_hashes:
            new_files.append(path)
 
    # ---- Report ----
    print("\n" + "=" * 64)
    print("           INTEGRITY CHECK REPORT")
    print("=" * 64)
    print(f"Baseline created : {baseline['created_at']}")
    print(f"Algorithm        : {algorithm.upper()}")
    print(f"Files in baseline: {len(old_hashes)}")
    print(f"Files now        : {len(new_hashes)}")
    print("-" * 64)
    print(f"  Unchanged : {len(unchanged)}")
    print(f"  Modified  : {len(modified)}")
    print(f"  Deleted   : {len(deleted)}")
    print(f"  New       : {len(new_files)}")
    print("=" * 64)
 
    if modified:
        print("\n[!] MODIFIED FILES:")
        for path, old_h, new_h in modified:
            print(f"    - {path}")
            print(f"        old: {old_h[:32]}...")
            print(f"        new: {new_h[:32]}...")
 
    if deleted:
        print("\n[!] DELETED FILES:")
        for path in deleted:
            print(f"    - {path}")
 
    if new_files:
        print("\n[+] NEW FILES:")
        for path in new_files:
            print(f"    - {path}")
 
    if not (modified or deleted or new_files):
        print("\n[OK] All files passed the integrity check.")
 
    return {
        'modified' : modified,
        'deleted'  : deleted,
        'new'      : new_files,
        'unchanged': unchanged,
    }
 
 
# ---------- COMMAND-LINE INTERFACE ----------
 
def main():
    print("=" * 64)
    print("           FILE INTEGRITY CHECKER")
    print("    Using Cryptographic Hash Functions (SHA-256)")
    print("=" * 64)
 
    while True:
        print("\nOptions:")
        print("  1. Create baseline (snapshot a directory)")
        print("  2. Verify integrity (compare against baseline)")
        print("  3. Hash a single file")
        print("  4. Exit")
 
        choice = input("\nChoose an option (1-4): ").strip()
 
        if choice == '1':
            directory = input("Enter directory path: ").strip()
            if not os.path.isdir(directory):
                print("[!] Invalid directory.")
                continue
            algorithm = input("Algorithm (sha256/sha512/md5) [sha256]: ").strip() or 'sha256'
            baseline_file = input("Baseline filename [baseline.json]: ").strip() or 'baseline.json'
            try:
                create_baseline(directory, baseline_file, algorithm)
            except ValueError:
                print(f"[!] Unsupported algorithm: {algorithm}")
 
        elif choice == '2':
            baseline_file = input("Baseline filename [baseline.json]: ").strip() or 'baseline.json'
            verify_integrity(baseline_file)
 
        elif choice == '3':
            filepath = input("Enter file path: ").strip()
            if not os.path.isfile(filepath):
                print("[!] File not found.")
                continue
            algorithm = input("Algorithm (sha256/sha512/md5) [sha256]: ").strip() or 'sha256'
            try:
                file_hash = compute_hash(filepath, algorithm)
                print(f"\n{algorithm.upper()} of '{filepath}':")
                print(f"  {file_hash}")
            except ValueError:
                print(f"[!] Unsupported algorithm: {algorithm}")
 
        elif choice == '4':
            print("Goodbye!")
            break
 
        else:
            print("[!] Invalid option.")
 
 
if __name__ == '__main__':
    main()