# 🧠 Model-Based Reflex Agent (Prolog)

## 📌 Overview

This project implements a **Model-Based Reflex Agent** using **Prolog**. Unlike a simple reflex agent, this agent maintains an **internal state (model)** of the world, allowing it to make better decisions in environments that are **partially observable**.

The agent is designed to be **integrated with a Python UI**, where the environment sends percepts and receives actions from the Prolog logic.

---

## 🤖 What Is a Model-Based Reflex Agent?

A Model-Based Reflex Agent:

* Reacts to the **current percept**
* Maintains an **internal model** of the environment
* Updates its state using percept history
* Chooses actions based on the **current internal state**, not just raw percepts

In simple terms: the agent *remembers what it has seen before*.

---

## 🧠 Agent Logic Flow

```
Percept → Update Internal State → Select Action
```

Example:

* The agent perceives part of the environment
* Updates what it believes the world looks like
* Uses this belief to decide what to do next

---

## 🌍 Environment Assumptions (Example)

The environment may be:

* A room-cleaning world
* A grid where some locations are not always observable

### Percept Example

```prolog
percept(RoomState, Position).
```

### Internal State Example

```prolog
state(RoomStateLeft, RoomStateRight, Position).
```

---

## 🗂 Project Structure

```
model-based-agent/
│
├── src/
│   ├── model_agent.pl        # Main agent logic
│   ├── state_update.pl       # Internal state update rules
│   └── action_rules.pl       # Action selection rules
│
├── tests/
│   └── test_queries.pl       # Sample test cases
│
├── docs/
│   └── agent_explanation.md  # Theory + design explanation
│
└── README.md
```

---

## ⚙️ Key Components

### 1️⃣ Internal State

* Represents the agent’s belief about the world
* Updated whenever a new percept is received

### 2️⃣ State Update Rules

* Combine previous state with new percepts
* Handle unknown or partially observable data

### 3️⃣ Action Selection

* Uses the internal state to determine the next action
* Implemented as condition–action rules

---

## 🧩 Core Predicate

The main predicate exposed for Python integration:

```prolog
decide_action(Percept, CurrentState, NewState, Action).
```

* `Percept`: current sensory input
* `CurrentState`: agent’s internal model
* `NewState`: updated internal model
* `Action`: chosen action

---

## 🔌 Python Integration Notes

* No printing inside Prolog predicates
* Output must be clean and deterministic
* The Python UI will:

  1. Send percept + current state
  2. Receive action + updated state

---

## 🧪 Testing

Run SWI-Prolog:

```bash
swipl
```

Load the agent:

```prolog
?- consult('src/model_agent.pl').
```

Example test:

```prolog
?- decide_action(percept(dirty,left), state(clean,unknown,left), NewState, Action).
```

---

## ✅ Acceptance Criteria

* Agent maintains internal state
* State updates correctly with percepts
* Actions depend on state, not just percept
* Code runs in **SWI-Prolog**
* Ready for Python UI integration

---

## 📚 Academic Reference

Russell, S. & Norvig, P.  *Artificial Intelligence: A Modern Approach*
Chapter 2 – Intelligent Agents

---

## 🧭 Final Note

This agent should clearly behave **smarter than a simple reflex agent**. When observed through the UI, its decisions should reflect **memory and awareness of unseen parts of the environment**.

If it remembers, it qualifies. 🧠✔️

