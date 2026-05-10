# 🔍 File Integrity Checker

> A lightweight Python tool that uses **cryptographic hash functions** (SHA-256, SHA-512, MD5) to detect unauthorized or accidental changes to files — the same idea behind real-world tools like **Tripwire** and **AIDE**.

![Python](https://img.shields.io/badge/python-3.7%2B-blue)
![Hash](https://img.shields.io/badge/hash-SHA--256%20%7C%20SHA--512%20%7C%20MD5-orange)
![Dependencies](https://img.shields.io/badge/dependencies-stdlib%20only-success)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 📌 Overview

A file integrity checker is a security tool that takes a cryptographic "fingerprint" of every file in a directory today, and later compares fresh fingerprints against that baseline to catch any **modification, deletion, or addition** of files.

This is one of the core defenses against:

- 🦠 **Malware / ransomware** silently modifying system files
- 🕵️ **Intruders or insider threats** tampering with logs or binaries
- 🛠️ **Accidental changes** during deployments or maintenance

This project is a from-scratch Python implementation built for the *Computer Security* course (Project #18).

---

## 🔬 How It Works

1. **Hashing** — every file is read in 4 KB chunks and passed through a hash function. The output is a fixed-length digital fingerprint.
2. **Avalanche effect** — even a single bit changed in the file produces a completely different hash, making tampering detectable.
3. **Baseline** — all `{relative_path: hash}` pairs are saved to `baseline.json` along with metadata (directory, algorithm, timestamp).
4. **Verification** — re-scan the directory, recompute hashes, and classify each file as:

| Category | Meaning |
|---|---|
| ✅ **Unchanged** | Path exists in both, hashes match |
| ⚠️ **Modified** | Path exists in both, hashes differ |
| ❌ **Deleted** | Path was in baseline but is gone now |
| 🆕 **New** | Path exists now but not in the baseline |

---

## 🛠️ Algorithms Supported

| Algorithm | Output Size | Use for Security? |
|---|---|---|
| **SHA-256** *(default)* | 256 bits | ✅ Yes — collision-resistant, NIST standard |
| SHA-512 | 512 bits | ✅ Yes — stronger but heavier |
| MD5 | 128 bits | ❌ No — broken for collision resistance, included for educational comparison only |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or newer
- No external dependencies — uses Python's standard library (`hashlib`, `json`, `os`, `datetime`)

### Run it

```bash
git clone https://github.com/<your-username>/file-integrity-checker.git
cd file-integrity-checker
python3 code.py
```

You'll see an interactive menu:

```
============================================================
           FILE INTEGRITY CHECKER
    Using Cryptographic Hash Functions (SHA-256)
============================================================

Options:
  1. Create baseline (snapshot a directory)
  2. Verify integrity (compare against baseline)
  3. Hash a single file
  4. Exit
```

---

## 🎯 Typical Demo Flow

1. **Create a baseline** — choose option `1` and point it at a folder. A `baseline.json` file is generated.
2. **Tamper with the folder** — modify a file, delete one, add a new one.
3. **Verify** — choose option `2`. The report shows exactly what changed.

### Sample Output

```
================================================================
           INTEGRITY CHECK REPORT
================================================================
Baseline created : 2026-05-03T15:40:19
Algorithm        : SHA256
Files in baseline: 3
Files now        : 3
----------------------------------------------------------------
  Unchanged : 1
  Modified  : 1
  Deleted   : 1
  New       : 1
================================================================

[!] MODIFIED FILES:
    - notes.txt
        old: 1894a19c85ba153acbf743ac4e43fc00...
        new: cac5c0b32d8262b0850569ad07e67df1...

[!] DELETED FILES:
    - intruder.txt

[+] NEW FILES:
    - test2.txt
```

---

## 📂 Project Structure

```
file-integrity-checker/
├── code.py             # Main program (CLI + all logic)
├── README.md           # This file
├── docs/
│   └── report.pdf      # Full project report
└── sample/             # Sample files for testing
    ├── notes.txt
    ├── test.txt
    ├── test2.txt
    └── intruder.txt
```

---

## 🔒 Security Notes & Limitations

This tool is built for learning and small-scale use. Some honest limitations:

- 🔧 **The baseline file itself is unprotected.** A sophisticated attacker who modifies files could also rewrite `baseline.json`. Real-world fix: sign the baseline with a private key (HMAC or RSA), or store it on read-only / offline media.
- 🔧 **No real-time monitoring.** Verification runs on demand. In production this would be scheduled (e.g. via `cron` or `systemd` timer).
- 🔧 **No symlink/permission tracking.** Only file *contents* are checked, not metadata like permissions, ownership, or symlink targets.
- 🔧 **Single-threaded.** Very large directory trees would benefit from multiprocessing.

These are intentionally documented as a roadmap rather than glossed over.

---

## 🎓 Concepts Demonstrated

- Cryptographic hash functions and the **avalanche effect**
- **Collision resistance** and why SHA-256 is preferred over MD5/SHA-1
- The **integrity** pillar of the **CIA triad** (Confidentiality / Integrity / Availability)
- Baseline / snapshot security model
- File system traversal in Python (`os.walk`)
- Chunked file I/O for memory-efficient hashing of large files
- JSON serialization for persistent state
- Command-line tool design

---

## 📚 References

- [NIST FIPS 180-4 — Secure Hash Standard](https://csrc.nist.gov/publications/detail/fips/180/4/final)
- [Tripwire (open-source)](https://github.com/Tripwire/tripwire-open-source)
- [AIDE — Advanced Intrusion Detection Environment](https://aide.github.io/)
- [Python `hashlib` documentation](https://docs.python.org/3/library/hashlib.html)

---

## 📜 License

MIT License — feel free to use this as a learning reference.

---

## 👤 Author

**Adham**
Cybersecurity Student
Built for *Computer Security* — Project #18.
