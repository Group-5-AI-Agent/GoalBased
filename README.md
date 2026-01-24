# 🎯 Goal-Based Agent (Prolog)

## 📌 Overview

This project implements a **Goal-Based Agent** using **Prolog**. Unlike reflex-based agents, this agent selects actions by **reasoning about future states** and choosing actions that help it **achieve a specific goal**.

The agent is designed to work with a **Python UI**, which visualizes the environment, the agent’s decisions, and goal progression.

---

## 🤖 What Is a Goal-Based Agent?

A Goal-Based Agent:

* Has a **clearly defined goal**
* Considers the **current state of the environment**
* Chooses actions that move it **closer to the goal**
* May evaluate multiple possible actions before deciding

In simple terms: the agent *acts with intention*.

---

## 🧠 Agent Logic Flow

```
Current State → Possible Actions → Resulting States → Goal Test → Action
```

The agent does not just react; it **plans**.

---

## 🌍 Environment Assumptions (Example)

The environment may be represented as:

* A grid world
* A room-cleaning environment
* Any state-space problem with clear goals

### State Representation Example

```prolog
state(Position, RoomStatus).
```

### Goal Representation Example

```prolog
goal(clean).
```

---

## 🗂 Project Structure

```
goal-based-agent/
│
├── src/
│   ├── goal_agent.pl          # Main agent logic
│   ├── goal_definition.pl     # Goal representation
│   └── action_rules.pl        # Actions and transitions
│
├── tests/
│   └── test_queries.pl        # Sample test cases
│
├── docs/
│   └── agent_explanation.md   # Theory + design explanation
│
└── README.md
```

---

## ⚙️ Key Components

### 1️⃣ Goal Definition

* Explicit representation of what the agent wants to achieve
* Used to test whether a state is acceptable

### 2️⃣ State Evaluation

* Determines whether the current state satisfies the goal
* Implemented using goal-test predicates

### 3️⃣ Action Selection / Planning

* Evaluates possible actions
* Chooses actions that reduce the distance to the goal

---

## 🧩 Core Predicate

The main predicate exposed for Python integration:

```prolog
decide_action(CurrentState, Goal, Action).
```

* `CurrentState`: current environment state
* `Goal`: desired goal state
* `Action`: chosen action toward the goal

(Optional advanced version)

```prolog
plan(CurrentState, Goal, Plan).
```

---

## 🔌 Python Integration Notes

* Prolog must return **one clear action**
* No console printing inside Prolog logic
* Python UI will:

  1. Provide current state and goal
  2. Receive the next best action

---

## 🧪 Testing

Run SWI-Prolog:

```bash
swipl
```

Load the agent:

```prolog
?- consult('src/goal_agent.pl').
```

Example test:

```prolog
?- decide_action(state(left, dirty), goal(clean), Action).
```

---

## ✅ Acceptance Criteria

* Goal is explicitly defined
* Agent chooses actions based on goal achievement
* No random or purely reactive behavior
* Code runs in **SWI-Prolog**
* Ready for Python UI integration

---

## 📚 Academic Reference

Russell, S. & Norvig, P.  *Artificial Intelligence: A Modern Approach*
Chapter 2 – Intelligent Agents

---

## 🧭 Final Note

When observed through the UI, this agent should clearly demonstrate **purposeful behavior**. Every action must make sense **in relation to the goal**.

If it plans, it qualifies. 🎯✔️
