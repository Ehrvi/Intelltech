# Manus Global Knowledge System v2.1 - Auto-Enforcer Edition

> **"Somente unidos seremos mais fortes!"**

A world-class knowledge management system with **total enforcement**, **scientific methodology**, and **continuous learning**. Now with **automatic activation**.

---

## 🚀 What's New in v2.1

**AUTO-ENFORCEMENT IS NOW ACTIVE!**

- ✅ **Automatic Activation:** The system now activates automatically on every new shell and Python process.
- ✅ **No Manual Initialization:** You no longer need to run `mandatory_init.py`.
- ✅ **System-Wide Hooks:** Installed via `.bashrc` and Python's site-packages.

---

## 🏗️ Architecture

### The 6 Levels of Enforcement

```
1. Initialization ─────→ AUTOMATICALLY ACTIVATED
           ↓
2. Cost Gate ──────────→ BLOCKS expensive operations
           ↓
3. Knowledge Lookup ───→ REUSES existing knowledge
           ↓
4. Execution Router ───→ ROUTES to optimal tool
           ↓
5. Quality Validator ──→ VALIDATES output (≥80%)
           ↓
6. Continuous Learning → LEARNS and adapts
```

### ⚠️ Current Limitation: No Automatic Interception

While the system is **active**, it does **NOT** automatically intercept Manus tool calls (`shell`, `file`, `browser`, etc.).

**Why?**
- The tools are executed by the Manus backend, which I cannot modify.

**Solution:**
- The Manus backend needs to be updated to call our enforcement function before executing any tool.
- **OR:** We can create wrapper functions in Python that we use instead of the direct tools.

---

## ⚙️ How to Use (Programmatically)

To use the enforcement system, you must call it from your Python code before executing an operation.

```python
from core.auto_enforcer import enforce_before_operation

# 1. Define your operation
my_operation = {
    'type': 'search',
    'queries': ['find cheap flights'],
    'estimated_cost': 100
}

# 2. Check with the enforcer
enforcement_result = enforce_before_operation('search', **my_operation)

# 3. Act on the decision
if enforcement_result['allowed']:
    print("✅ Operation allowed. Proceeding...")
    # Execute the actual operation here
else:
    print(f"❌ Operation BLOCKED: {enforcement_result['reason']}")
    if enforcement_result['alternative']:
        print(f"💡 Suggested alternative: {enforcement_result['alternative']}")
```

---

## 📦 Installation

The auto-enforcement hooks are already installed. If you need to reinstall:

```bash
# Run the installation script
/home/ubuntu/manus_global_knowledge/install_hooks.sh
```

---

## 🧪 Testing

```bash
# Run the auto-enforcement test suite
python3 /home/ubuntu/manus_global_knowledge/tests/test_auto_enforcement.py
```

---

## 🛣️ Roadmap

### Phase 1 & 2 (Current) ✅
- [x] Unified enforcement pipeline
- [x] Scientific method integration
- [x] AI University integration
- [x] **Auto-enforcement hooks installed**

### Phase 3 (Next Step)
- [ ] **Backend Integration:** Work with the Manus team to integrate `enforce_before_operation()` into the core tool execution workflow. This will enable **true automatic interception**.
- [ ] **Wrapper Library:** Create a Python library that wraps Manus tools with enforcement calls, providing a simpler interface for developers.

---

**Built with ❤️ using the Scientific Method**

*Last Updated: 2026-02-15*
