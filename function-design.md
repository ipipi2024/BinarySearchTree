# Recursive Function Design: BST Delete Operation

## Table of Contents
1. [Delete Function Overview](#delete-function-overview)
2. [System Architecture Diagram](#system-architecture-diagram)
3. [Detailed Flow Analysis](#detailed-flow-analysis)
4. [Recursive Design Patterns](#recursive-design-patterns)
5. [How to Extract Recursive Solutions](#how-to-extract-recursive-solutions)

---

## Delete Function Overview

The delete operation in `bst.py:249-301` demonstrates a classic recursive algorithm with multiple cases. It removes a node with a given key (and optionally matching value) from a Binary Search Tree.

**Key Components:**
- **Wrapper function**: `delete(self, key, value=None)` at line 249
- **Recursive function**: `recursive_delete(self, x, k, v)` at line 262

---

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    DELETE OPERATION FLOW                         │
└─────────────────────────────────────────────────────────────────┘

Entry Point: delete(key, value)
     │
     └──> self.root = recursive_delete(self.root, key, value)
                             │
                             ▼
          ┌──────────────────────────────────────────┐
          │  recursive_delete(x, k, v)               │
          │                                          │
          │  Step 1: BASE CASE CHECK                │
          │  ┌────────────────────────────────┐     │
          │  │ if x is None:                  │     │
          │  │    return None                 │     │
          │  └────────────────────────────────┘     │
          │           │                              │
          │           ▼                              │
          │  Step 2: SEARCH PHASE                   │
          │  ┌────────────────────────────────┐     │
          │  │ if k < x.key:                  │     │
          │  │    x.left = recursive_delete   │────┐│
          │  │              (x.left, k, v)    │    ││
          │  ├────────────────────────────────┤    ││
          │  │ elif k > x.key:                │    ││
          │  │    x.right = recursive_delete  │────┤│
          │  │              (x.right, k, v)   │    ││
          │  └────────────────────────────────┘    ││
          │           │                             ││
          │           ▼ (k == x.key)                ││
          │  Step 3: VALUE MATCHING                 ││
          │  ┌────────────────────────────────┐    ││
          │  │ if v != None and x.value != v: │    ││
          │  │    x.right = recursive_delete  │────┤│
          │  │              (x.right, k, v)   │    ││
          │  └────────────────────────────────┘    ││
          │           │                             ││
          │           ▼ (value matches)             ││
          │  Step 4: DELETION CASES                 ││
          │  ┌────────────────────────────────┐    ││
          │  │ Case 1: No left child          │    ││
          │  │    return x.right              │    ││
          │  ├────────────────────────────────┤    ││
          │  │ Case 2: No right child         │    ││
          │  │    return x.left               │    ││
          │  ├────────────────────────────────┤    ││
          │  │ Case 3: Both children          │    ││
          │  │    1. Find successor (min in   │    ││
          │  │       right subtree)           │    ││
          │  │    2. Copy successor to x      │    ││
          │  │    3. Delete successor from    │    ││
          │  │       right subtree            │────┤│
          │  └────────────────────────────────┘    ││
          │           │                             ││
          │           ▼                             ││
          │  Step 5: SIZE UPDATE                    ││
          │  ┌────────────────────────────────┐    ││
          │  │ x.update_size()                │    ││
          │  │ return x                       │    ││
          │  └────────────────────────────────┘    ││
          └──────────────────────────────────────────┘
                     ▲                              ││
                     └──────────────────────────────┘│
                        Recursive calls return here  │
                     ▲                               │
                     └───────────────────────────────┘
```

---

## Detailed Flow Analysis

### Phase 1: Base Case (Line 267-269)
```python
if x is None:
    return None
```
**Purpose:** Stop recursion when we've reached the end of the tree or the key doesn't exist.

**Visualization:**
```
Searching for key=50 in empty subtree:

    None  ← Base case triggered
```

---

### Phase 2: Search Navigation (Lines 272-275)
```python
if k < x.key:
    x.left = self.recursive_delete(x.left, k, v)
elif k > x.key:
    x.right = self.recursive_delete(x.right, k, v)
```

**Purpose:** Navigate through the tree using BST property (left < parent < right).

**Visualization:**
```
Looking for key=30 in tree rooted at 50:

        50
       /  \
     30    70     ← k(30) < x.key(50), go left
    /  \
   20   40

        50
       /  \
     [30]  70     ← Found! Proceed to deletion
    /  \
   20   40
```

---

### Phase 3: Value Matching (Lines 277-281)
```python
if v is not None and x.value != v:
    x.right = self.recursive_delete(x.right, k, v)
```

**Purpose:** Handle duplicate keys by checking if the value matches. If not, continue searching in the right subtree (where duplicates with same key would be stored).

**Visualization:**
```
Looking for key=30, value="B":

        50
       /  \
     30    70     ← key matches but value is "A"
    /  \
   20  [30]      ← Continue searching right subtree
         ↑          for key=30, value="B"
```

---

### Phase 4: Deletion Cases (Lines 283-297)

#### Case 1: No Left Child (Lines 285-286)
```python
if x.left is None:
    return x.right
```

**Visualization:**
```
Delete node 20 (no left child):

    50                50
   /  \              /  \
  20   70    →     25   70
    \
    25

Return 25 to replace 20
```

#### Case 2: No Right Child (Lines 288-289)
```python
elif x.right is None:
    return x.left
```

**Visualization:**
```
Delete node 20 (no right child):

    50                50
   /  \              /  \
  20   70    →     15   70
 /
15

Return 15 to replace 20
```

#### Case 3: Both Children (Lines 291-297)
```python
else:
    succ_key, succ_value = self.iterative_min(x.right)
    x.key = succ_key
    x.value = succ_value
    x.right = self.recursive_delete(x.right, succ_key, succ_value)
```

**Visualization:**
```
Delete node 50 (has both children):

Step 1: Find successor (minimum in right subtree)

        [50]
        /  \
      30    70
           /  \
         [60]  80  ← Successor is 60 (leftmost in right subtree)

Step 2: Copy successor's data to current node

        [60]  ← Copy 60 to replace 50
        /  \
      30    70
           /  \
         [60]  80  ← Now delete this duplicate

Step 3: Recursively delete successor from right subtree

        60
        /  \
      30    70
             \
              80  ← 60 deleted from right subtree
```

---

### Phase 5: Size Update (Lines 300-301)
```python
x.update_size()
return x
```

**Purpose:** Maintain the size field after modifications, then return the (possibly new) root of this subtree.

**Flow:**
```
After deletion completes at each level:
1. Recalculate size: left.size + right.size + 1
2. Return updated node to parent
3. Parent receives updated child and continues
```

---

## Recursive Design Patterns

### Pattern 1: The Wrapper-Recursive Pair

**Structure:**
```python
def operation(self, params):
    """Public interface - wrapper function"""
    self.root = self.recursive_operation(self.root, params)

def recursive_operation(self, node, params):
    """Actual recursive implementation"""
    # Base case
    # Recursive case
    # Process and return
```

**Why this pattern?**
- **Separation of concerns**: Public API vs. implementation details
- **State management**: Wrapper handles tree-level state (self.root)
- **Clean interface**: Users don't need to pass root explicitly
- **Flexibility**: Can add validation/logging in wrapper without cluttering recursive logic

**Examples in bst.py:**
- `insert` → `recursive_insert` (line 53, 63)
- `find` → `recursive_find` (line 82, 93)
- `delete` → `recursive_delete` (line 249, 262)

---

### Pattern 2: The Three-Part Recursive Structure

Every well-designed recursive function follows this template:

```
┌─────────────────────────────────────┐
│  1. BASE CASE(S)                   │  ← Stopping condition
│     - Empty node (None)             │
│     - Found target                  │
│     - Invalid input                 │
├─────────────────────────────────────┤
│  2. RECURSIVE CASE(S)               │  ← Break problem into smaller pieces
│     - Navigate left/right           │
│     - Process subtrees              │
│     - Combine results               │
├─────────────────────────────────────┤
│  3. POST-PROCESSING                 │  ← Cleanup after recursion returns
│     - Update metadata (size)        │
│     - Combine results               │
│     - Return modified structure     │
└─────────────────────────────────────┘
```

**Applied to recursive_delete:**
```python
def recursive_delete(self, x, k, v):
    # 1. BASE CASE
    if x is None:
        return None

    # 2. RECURSIVE CASE
    if k < x.key:
        x.left = self.recursive_delete(x.left, k, v)
    elif k > x.key:
        x.right = self.recursive_delete(x.right, k, v)
    else:
        # Found node - handle deletion cases
        # ...

    # 3. POST-PROCESSING
    x.update_size()
    return x
```

---

### Pattern 3: Return-and-Replace Strategy

**Key Insight:** In tree recursion, we often **return the new root** of a subtree after modification.

```python
x.left = self.recursive_delete(x.left, k, v)
#  ↑                                  ↑
#  │                                  └── Returns modified subtree
#  └── Replace old subtree with new one
```

**Why return nodes?**
1. Subtree structure may change (node deleted/added)
2. Parent needs to update its child pointer
3. Enables functional-style immutability (though not used here)

**Visualization:**
```
Before: x points to subtree with node to delete
   x
   └─→ subtree (contains target node)

After: x points to modified subtree
   x
   └─→ new_subtree (target removed, structure adjusted)
```

---

### Pattern 4: Multiple Termination Paths

Complex recursive functions may have multiple ways to terminate:

```python
# Termination Path 1: Base case
if x is None:
    return None

# Termination Path 2: Leaf deletion (no left child)
if x.left is None:
    return x.right

# Termination Path 3: Leaf deletion (no right child)
elif x.right is None:
    return x.left

# Termination Path 4: Normal return after processing
return x
```

**Design principle:** Each path should return the same **type** (Node or None).

---

## How to Extract Recursive Solutions

### Step 1: Identify the Problem Structure

**Questions to ask:**
1. Can the problem be divided into smaller, **similar subproblems**?
2. Is there a **natural base case** (smallest possible input)?
3. Can you **combine solutions** from subproblems to solve the original?

**For BST delete:**
- ✓ Delete from tree = Delete from left OR right subtree + handle current node
- ✓ Base case = Empty tree (None)
- ✓ Combine = Update current node's children with results from recursive calls

---

### Step 2: Define the Recursive Invariant

**Invariant:** A property that remains true before and after each recursive call.

**For delete:**
```
Invariant: "After recursive_delete(x, k, v) returns, the subtree rooted
            at the returned node is a valid BST with key k (and value v)
            removed, and all sizes are correct."
```

**How this helps:**
- Trust that recursive calls maintain the invariant
- Focus only on current level's logic
- Ensure you maintain the invariant before returning

---

### Step 3: Draw the Recursion Tree

**Example:** Delete key=20 from a tree

```
                    Initial Call
                 delete(root, 20)
                        │
            ┌───────────┴───────────┐
            │                       │
    recursive_delete(50, 20)        │
            │                       │
      k < 50.key, go left           │
            │                       │
    ┌───────┴───────┐               │
    │               │               │
recursive_delete(30, 20)            │
    │               │               │
k < 30.key, go left │               │
    │               │               │
recursive_delete(20, 20)  ← FOUND!  │
    │               │               │
Delete & return     │               │
    │               │               │
    └───────────────┴───────────────┘
         Returns propagate back up
```

**Insight:** Each call is responsible for:
1. Its own node's modification
2. Receiving updated children from recursive calls
3. Returning updated self to parent

---

### Step 4: Identify the Minimal Decision Point

At each recursive call, what's the **smallest decision** you need to make?

**For delete:**
```
Am I at the right node?
├─ No, k < my_key  → Go left
├─ No, k > my_key  → Go right
└─ Yes, k == my_key → How many children do I have?
                      ├─ 0 or 1 child  → Simple replacement
                      └─ 2 children    → Successor replacement
```

**Key principle:** Don't try to solve everything at once. Just make the next decision, trust recursion for the rest.

---

### Step 5: Handle Edge Cases in Order

**Priority order for edge cases:**
1. **Null/empty** inputs
2. **Single element** (boundary between base and recursive case)
3. **Special values** (root node, leaf node, etc.)

**Delete edge cases:**
```python
# 1. Empty tree
if x is None:
    return None

# 2. Value doesn't match (special case for duplicate keys)
if v is not None and x.value != v:
    x.right = self.recursive_delete(x.right, k, v)

# 3. Node has 0 or 1 child (simplified deletion)
if x.left is None:
    return x.right
elif x.right is None:
    return x.left
```

---

### Step 6: Choose Between Iteration and Recursion

**Use recursion when:**
- Problem has natural recursive structure (trees, graphs)
- Need to process results on return (post-order processing)
- Code clarity is more important than memory efficiency
- Maximum depth is bounded (won't cause stack overflow)

**Use iteration when:**
- Simple linear traversal (finding min/max in BST)
- Need better memory efficiency
- Risk of deep recursion (very unbalanced trees)

**Examples in bst.py:**
- `recursive_delete`: Uses recursion (needs to modify tree structure)
- `iterative_min`: Uses iteration (simple traversal to leftmost node)
- `pred`: Uses iteration (linear search with tracking)

---

## Design Recipe Summary

### For Any Recursive Function:

```
1. SPECIFICATION
   - What does the function do?
   - What are inputs and outputs?
   - What's the invariant?

2. BASE CASE(S)
   - What's the smallest/simplest input?
   - What should be returned directly?

3. RECURSIVE DECOMPOSITION
   - How to break problem into subproblems?
   - What recursive calls are needed?
   - What information flows between calls?

4. COMBINATION LOGIC
   - How to merge results from recursive calls?
   - What processing happens at current level?

5. TERMINATION PROOF
   - Does each recursive call work on smaller input?
   - Are all paths guaranteed to reach base case?

6. CORRECTNESS PROOF
   - Assume recursive calls work correctly
   - Prove current level is correct
   - Verify invariant is maintained
```

---

## Applying the Recipe to Delete

### 1. Specification
```
recursive_delete(x, k, v):
    Input: Root node x, key k, value v (optional)
    Output: New root of subtree after deletion
    Invariant: Returns valid BST with node(k,v) removed
```

### 2. Base Case
```python
if x is None:
    return None  # Key not found, nothing to delete
```

### 3. Recursive Decomposition
```python
# Navigate to target
if k < x.key:
    x.left = self.recursive_delete(x.left, k, v)
elif k > x.key:
    x.right = self.recursive_delete(x.right, k, v)
else:
    # Found target - handle deletion
```

### 4. Combination Logic
```python
# Case 1 & 2: Single/no child - return the other child
if x.left is None:
    return x.right
elif x.right is None:
    return x.left

# Case 3: Two children - replace with successor
else:
    succ_key, succ_value = self.iterative_min(x.right)
    x.key = succ_key
    x.value = succ_value
    x.right = self.recursive_delete(x.right, succ_key, succ_value)
```

### 5. Termination Proof
- **Navigation cases**: Recurse on smaller subtree (left or right)
- **Deletion cases**: Either return immediately OR recurse on smaller subtree (right)
- **Base case**: Returns immediately when x is None
- ✓ Always progressing toward base case

### 6. Correctness Proof
**Assume:** Recursive calls correctly delete from subtrees and return valid BST roots.

**Prove:** Current level maintains BST property and correct deletion.

- **Navigation**: Delegates to correct subtree, updates child pointer → Still BST
- **Case 1/2**: Removing node with ≤1 child, returning other child → Still BST
- **Case 3**: Successor is the smallest key in right subtree, so it's the next larger key.
  Replacing current with successor maintains BST property. Deleting successor from
  right subtree is correct by assumption. → Still BST

✓ Correctness maintained at each level

---

## Key Takeaways

1. **Wrapper pattern**: Separate public API from recursive implementation
2. **Return-and-replace**: Recursive functions return modified subtrees
3. **Trust the recursion**: Assume recursive calls work, focus on current level
4. **Multiple cases**: Handle different scenarios with distinct termination paths
5. **Invariants**: Define and maintain invariants across recursive calls
6. **Post-processing**: Update metadata (like size) after recursive calls return
7. **Minimal decisions**: At each level, make only the next necessary decision

**Golden Rule of Recursion:**
> "Don't try to trace the entire call stack in your head.
> Trust that smaller problems are solved correctly, and
> focus only on combining their results."

---

## Practice Exercise

Try designing a recursive function for BST insertion using this guide:

1. What's the specification?
2. What's the base case?
3. How do you decompose the problem?
4. What do you return at each level?
5. What invariant must hold?

Compare your design with `recursive_insert` in `bst.py:63-80` to see how it follows these patterns!
