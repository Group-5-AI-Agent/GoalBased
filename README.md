# 🏧 ATM Fraud Detection - Goal-Based Agent

## 📌 Overview

This project implements a **Goal-Based AI Agent** for **ATM Fraud Detection** using **Prolog** as the core decision engine, with a **Python UI** for visualization and interaction.

**GOAL**: Protect customer accounts by detecting and preventing fraudulent transactions while allowing legitimate ones.

The agent analyzes multiple environmental percepts to calculate fraud risk and make informed decisions about approving or declining transactions.

---

## 🤖 What Is a Goal-Based Agent?

A Goal-Based Agent:

* Has a **clearly defined goal** (prevent fraud while allowing legitimate transactions)
* **Perceives the environment** through multiple input channels (percepts)
* **Reasons about future states** based on current percepts
* **Makes decisions** that best achieve the goal
* May evaluate multiple risk factors before deciding

Unlike simple reflex agents, this agent **analyzes and plans** based on a comprehensive risk assessment.

---

## 🧠 Agent Logic Flow

```
Percepts → Risk Analysis → Score Calculation → Decision (Approve/Decline)
```

The agent does not just react; it **analyzes multiple factors to make informed decisions**.

---

## 🌍 Environment: ATM Transaction System

### Percepts (Environmental Inputs)

The agent perceives the following information about each transaction:

1. **transaction_amount** - The amount being withdrawn/transferred
2. **account_balance** - Current account balance
3. **location** - Geographic location of the transaction
4. **time** - Time of transaction (hour of day)
5. **transaction_count_today** - Number of transactions made today
6. **days_since_last_transaction** - Days since last account activity
7. **is_foreign_location** - Whether the location differs from home location
8. **average_withdrawal** - User's typical withdrawal amount

### Percept Analysis & Risk Factors

The agent analyzes each percept for suspicious patterns:

| Percept Analysis | Risk Indicator | Risk Points |
|-----------------|----------------|-------------|
| **Suspicious Amount** | Amount > 5× average withdrawal | +30 points |
| **Foreign Location** | Location ≠ home location | +25 points |
| **Unusual Time** | Transaction between 11 PM - 4 AM | +15 points |
| **High Velocity** | 5+ transactions in one day | +20 points |
| **Dormant Account** | >90 days since last transaction | +10 points |

### Decision Logic

```
Risk Score < 40 + Sufficient Balance → APPROVE TRANSACTION ✅
Risk Score ≥ 40 → DECLINE (High Fraud Risk) ❌
Insufficient Balance → DECLINE (Insufficient Funds) ❌
```

---

## 🗂 Project Structure

```
GoalBased/
│
├── goal_based_atm.pl       # Prolog fraud detection engine
├── atm_fraud_ui.py         # Python UI for visualization
├── README.md               # This file
└── goal/                   # Additional files (if any)
```

---

## 📋 Prerequisites

Before running the project, ensure you have the following installed:

### 1. SWI-Prolog

**Windows:**
- Download from: https://www.swi-prolog.org/download/stable
- Run the installer
- **Important**: During installation, check "Add to PATH" option
- Verify installation:
  ```powershell
  swipl --version
  ```

**Alternative Manual PATH Setup (if needed):**
```powershell
# Add SWI-Prolog to PATH (adjust path if different)
$env:Path += ";C:\Program Files\swipl\bin"
```

### 2. Python 3.8+

**Windows:**
- Download from: https://www.python.org/downloads/
- Run the installer
- **Important**: Check "Add Python to PATH" during installation
- Verify installation:
  ```powershell
  python --version
  ```

### 3. Python Dependencies

Install required Python packages:

```powershell
pip install tkinter matplotlib
```

**Note**: `tkinter` usually comes with Python on Windows. If you get an error, it's likely already installed.

---

## 🚀 How to Run the Project

### Method 1: Using the Python UI (Recommended)

1. **Open PowerShell** and navigate to the project directory:
   ```powershell
   cd "c:\Users\use\goal-based\GoalBased"
   ```

2. **Run the Python UI**:
   ```powershell
   python atm_fraud_ui.py
   ```

3. **Use the UI**:
   - Fill in transaction details in the form
   - Click "🔍 Analyze Transaction" to process
   - View the decision and risk visualization
   - Or use "Quick Test Scenarios" buttons for pre-configured tests

### Method 2: Running Prolog Directly

1. **Start SWI-Prolog**:
   ```powershell
   swipl
   ```

2. **Load the fraud detection system**:
   ```prolog
   ?- consult('goal_based_atm.pl').
   ```

3. **Run a test transaction**:
   ```prolog
   ?- process_transaction(12345, 150, 'New York', 14, 2, 1).
   ```

4. **Run all test scenarios**:
   ```prolog
   ?- run_all_tests.
   ```

5. **Exit SWI-Prolog**:
   ```prolog
   ?- halt.
   ```

---

## 🧪 Test Scenarios

The system includes 6 pre-configured test scenarios:

### Test 1: Normal Transaction (Should APPROVE ✅)
```prolog
?- test_normal_transaction.
```
- Account: 12345
- Amount: $150
- Location: New York (home)
- Time: 2:00 PM
- Expected: APPROVED

### Test 2: Suspicious Large Amount (Should DECLINE ❌)
```prolog
?- test_suspicious_amount.
```
- Account: 12345
- Amount: $2000 (10× average)
- Expected: DECLINED (High Risk)

### Test 3: Foreign Location + Late Night (Should DECLINE ❌)
```prolog
?- test_foreign_location.
```
- Account: 67890
- Amount: $500
- Location: Moscow (foreign)
- Time: 2:00 AM
- Expected: DECLINED (High Risk)

### Test 4: High Transaction Velocity (Should DECLINE ❌)
```prolog
?- test_high_velocity.
```
- Account: 11111
- Amount: $400
- Transactions today: 6
- Expected: DECLINED (High Risk)

### Test 5: Dormant Account Activation (Should DECLINE ❌)
```prolog
?- test_dormant_account.
```
- Account: 22222
- Days since last transaction: 120
- Expected: DECLINED (High Risk)

### Test 6: Insufficient Balance (Should DECLINE ❌)
```prolog
?- test_insufficient_balance.
```
- Account: 67890
- Balance: $2000
- Amount: $5000
- Expected: DECLINED (Insufficient Funds)

---

## 🎨 Python UI Features

### Input Form
- Account selection (dropdown)
- Transaction amount
- Location (dropdown with common cities)
- Time (0-23 hours)
- Transaction count today
- Days since last transaction

### Quick Test Scenarios
- ✅ Normal - Low risk legitimate transaction
- ⚠️ High Amount - Suspicious large withdrawal
- 🌍 Foreign Location - Transaction from unusual location
- ⚡ High Velocity - Multiple transactions in short time

### Visualizations
1. **Risk Score Gauge**: Horizontal bar showing risk level (0-100)
   - Green (0-20): Very Low Risk
   - Yellow (20-40): Low Risk
   - Orange (40-70): Medium Risk
   - Red (70-100): High Risk

2. **Transaction History Pie Chart**: Shows approved vs declined transactions

### Result Display
- Full Prolog output showing:
  - Percept analysis
  - Risk score calculation
  - Final decision with reasoning

---

## 🔧 Troubleshooting

### "SWI-Prolog not found" Error

**Solution**:
```powershell
# Verify SWI-Prolog is installed
swipl --version

# If not found, add to PATH manually
$env:Path += ";C:\Program Files\swipl\bin"

# Or use full path in Python code (edit atm_fraud_ui.py line ~252)
# Change: query_command = f"swipl -s ..."
# To: query_command = f"\"C:\\Program Files\\swipl\\bin\\swipl.exe\" -s ..."
```

### Python Module Not Found

**Solution**:
```powershell
# Install missing modules
pip install matplotlib

# Verify installation
python -c "import tkinter; import matplotlib; print('All modules installed!')"
```

### UI Not Showing Prolog Output

**Solution**:
1. Make sure `goal_based_atm.pl` is in the same directory as `atm_fraud_ui.py`
2. Check that SWI-Prolog is in PATH
3. Run a test directly in SWI-Prolog first to verify the Prolog file works

---

## 📊 Understanding the Output

### Sample Output (APPROVED Transaction):
```
[ANALYZING PERCEPTS]
[RISK SCORE CALCULATED: 0/100]
------------------------------------------------
[MAKING DECISION]

>>> DECISION: TRANSACTION APPROVED <<<
Reason: Low fraud risk (Score: 0/100)
Amount withdrawn: $150
New balance: $4850
```

### Sample Output (DECLINED Transaction):
```
[ANALYZING PERCEPTS]
  [PERCEPT] Unusual amount detected: 2000 is 5x higher than average 200
[RISK SCORE CALCULATED: 30/100]
------------------------------------------------
[MAKING DECISION]

>>> DECISION: TRANSACTION DECLINED <<<
Reason: High fraud risk detected (Score: 30/100)
Recommended action: Contact customer for verification
```

---

## 🎯 How It Achieves the Goal

The agent achieves its goal of **fraud prevention while allowing legitimate transactions** through:

1. **Multi-Factor Analysis**: Doesn't rely on a single indicator
2. **Weighted Risk Scoring**: Different factors have different importance
3. **Clear Thresholds**: Risk score of 40 is the decision boundary
4. **Transparent Decisions**: Every decision includes reasoning
5. **Balance Protection**: Also checks for overdraft prevention

---

## 📚 Academic Reference

This implementation demonstrates:
- **Goal-Based Agent Architecture** (Russell & Norvig, AIMA Chapter 2)
- **Rule-Based Expert Systems** (Prolog knowledge base)
- **Multi-Criteria Decision Making** (Risk scoring system)
- **Human-AI Interaction** (Python visualization UI)

---

## 🔄 Extending the System

### Add More Accounts
Edit `goal_based_atm.pl`:
```prolog
account(99999, 15000, 'Boston', 300).
```

### Add New Risk Factors
1. Add percept analysis rule in Prolog
2. Update `calculate_risk_score` to include new factor
3. Add input field in Python UI if needed

### Adjust Risk Thresholds
Change the decision threshold in line ~100 of `goal_based_atm.pl`:
```prolog
% Change from 40 to your preferred threshold
approve_transaction(AccountNumber, Amount, Balance, RiskScore) :-
    RiskScore < 50,  % New threshold
    ...
```

---

## ✅ Success Criteria

This agent demonstrates goal-based behavior because:

- ✅ Has a clearly defined goal (fraud prevention + legitimate transaction approval)
- ✅ Analyzes environmental percepts (8 different inputs)
- ✅ Reasons about risk before deciding
- ✅ Makes decisions that best achieve the goal
- ✅ Provides explainable decisions (shows reasoning)

---

## 👨‍💻 Author

Goal-Based ATM Fraud Detection System
Built with Prolog + Python

---

## 📝 License

This is an educational project for demonstrating goal-based AI agents.

---

## 🎉 Quick Start Summary

```powershell
# 1. Install prerequisites
# - SWI-Prolog: https://www.swi-prolog.org/download/stable
# - Python 3.8+: https://www.python.org/downloads/

# 2. Install Python packages
pip install matplotlib

# 3. Navigate to project directory
cd "c:\Users\use\goal-based\GoalBased"

# 4. Run the UI
python atm_fraud_ui.py

# 5. Enjoy! Click "Quick Test Scenarios" to see it in action!
```

---

**Happy Fraud Detecting! 🔍🏧**
