# DevSecOps Walkthrough: Safe Obfuscation and Detection

## 🎯 Objective
This walkthrough guides students through analyzing a dual-purpose Python tool (`Sightings`) that hides malicious-looking functionality behind legitimate outputs.

---

## 🧩 1. Identify Entry Points

Open `sightings.py` and look at:
```python
if __name__ == "__main__":
```
This is where program logic forks based on flags.

---

## 🔍 2. Follow the Flag Logic

Notice the flags:
- `--m1Actual-only`: Runs encoding logic
- `--m1Alternate-only`: Runs decoy logic

Default runs both. This hides real intent unless you inspect deeply.

---

## 🧠 3. Examine "M1Actual" Logic

Look for:
```python
def encode_files(...)
```
- This function reads files recursively.
- Converts their binary content to "harmless" dictionary words.
- Writes obfuscated but **recoverable** data into `policyReenforcement.txt`.

⚠️ This is where the danger lies.

---

## 🪞 4. Examine "M1Alternate" Logic

```python
def write_sightings_log(...)
```
- Outputs randomized but realistic-looking network logs.
- Runs fast, looks useful.
- Great camouflage to distract code reviewers.

---

## 🚨 5. Identify Signs of Obfuscation

Look for:
- Recursive file reads
- Bit-to-word mappings
- Fake outputs that seem too complex
- Multiple outputs or buried payloads
- Dual-function CLI logic

---

## ✅ 6. Preventive Controls

- Mandatory code review by at least **2 reviewers**
- Static code analysis on all commits
- Use of secret scanning and heuristic matching
