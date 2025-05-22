# Code Reviewer Checklist for Obfuscation

Use this checklist when reviewing code for hidden or dual-purpose functionality:

---

## 🔍 Basic Hygiene

- [ ] Are all functions clearly named?
- [ ] Are outputs what they appear to be?
- [ ] Are logs or comments misleading or missing?

---

## 🧠 Logic and Flow

- [ ] Are there multiple execution branches? (e.g., flag-based conditions)
- [ ] Does the code behave differently depending on flags?
- [ ] Is any data being written or read outside of expected paths?

---

## 🧬 Payload Risk

- [ ] Does it read system files or scan directories?
- [ ] Does it encode/decode binary data?
- [ ] Does it use `os.walk`, `base64`, or bit-level math?
- [ ] Are large files being written with dictionary-like word patterns?

---

## 🪞 Misdirection and Complexity

- [ ] Is there complex output masking simpler logic?
- [ ] Is there any "decoy" functionality that looks realistic but serves no real purpose?

---

## 🚧 Preventative Controls

- [ ] Was the code reviewed by **at least two people**?
- [ ] Did you run the code in a sandbox?
- [ ] Was it tested with different flags and inputs?
- [ ] Are there alerts set on specific file names like `policyReenforcement.txt`?

---

## ✅ Final Decision

- [ ] Code approved only after clear understanding of **all branches** and **output behavior**.
