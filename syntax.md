# 1. List (`list`)

**Use when:**

* Order matters
* You need to modify the collection
* Duplicate values are allowed

### Syntax

```python
numbers = [1, 2, 3]
```

### Example

```python
fruits = ["apple", "banana", "orange"]

fruits.append("pear")
fruits.remove("banana")

print(fruits)
# ['apple', 'orange', 'pear']
```

**Common operations**

```python
fruits[0]          # first item
fruits[-1]         # last item
len(fruits)
"apple" in fruits
fruits.append("kiwi")
fruits.pop()
```

---

# 2. Tuple (`tuple`)

**Use when:**

* Order matters
* Data should not change (immutable)
* Returning multiple values from a function

### Syntax

```python
point = (10, 20)
```

or

```python
point = 10, 20
```

### Example

```python
point = (5, 8)

x = point[0]
y = point[1]

print(x, y)
```

**Tuple unpacking**

```python
x, y = point

print(x)
print(y)
```

---

# 3. Set (`set`)

**Use when:**

* Only unique values
* Fast membership testing
* Removing duplicates

### Syntax

```python
numbers = {1, 2, 3}
```

**Empty set**

```python
numbers = set()      # NOT {}
```

### Example

```python
colors = {"red", "blue"}

colors.add("green")
colors.add("red")    # ignored

print(colors)
```

**Common operations**

```python
"red" in colors
colors.add("yellow")
colors.remove("blue")      # error if missing
colors.discard("blue")     # safe
colors.pop()               # remove arbitrary item
```

---

# 4. Dictionary (`dict`)

**Use when:**

* Store key → value pairs
* Fast lookup by key

### Syntax

```python
person = {
    "name": "Mike",
    "age": 30
}
```

### Example

```python
person = {
    "name": "Alice",
    "age": 25
}

print(person["name"])

person["age"] = 26
person["city"] = "Berlin"
```

**Common operations**

```python
person["name"]
person.get("name")
person.get("salary", 0)

"name" in person

del person["age"]

person.keys()
person.values()
person.items()
```

---

# Quick comparison

| Type  | Ordered         | Mutable | Duplicates  | Lookup               |
| ----- | --------------- | ------- | ----------- | -------------------- |
| List  | ✅               | ✅       | ✅           | By index             |
| Tuple | ✅               | ❌       | ✅           | By index             |
| Set   | ❌               | ✅       | ❌           | Very fast membership |
| Dict  | ✅ (Python 3.7+) | ✅       | Keys unique | Very fast by key     |

---

# Loops

## For loop

```python
for item in items:
    print(item)
```

Example

```python
numbers = [1, 2, 3]

for number in numbers:
    print(number)
```

---

## Loop with index

```python
for i in range(len(numbers)):
    print(i, numbers[i])
```

Better:

```python
for i, number in enumerate(numbers):
    print(i, number)
```

---

## Loop over a dictionary

Keys

```python
for key in person:
    print(key)
```

Values

```python
for value in person.values():
    print(value)
```

Key-value pairs

```python
for key, value in person.items():
    print(key, value)
```

---

## While loop

```python
count = 0

while count < 5:
    print(count)
    count += 1
```

---

# Conditionals

## if

```python
age = 18

if age >= 18:
    print("Adult")
```

---

## if / else

```python
if age >= 18:
    print("Adult")
else:
    print("Minor")
```

---

## if / elif / else

```python
score = 82

if score >= 90:
    print("A")
elif score >= 80:
    print("B")
elif score >= 70:
    print("C")
else:
    print("Fail")
```

---

## Comparison operators

```python
==
!=
<
<=
>
>=
```

Example

```python
if x == 5:
    ...
```

---

## Logical operators

```python
and
or
not
```

Example

```python
if age >= 18 and country == "Germany":
    print("Allowed")
```

---

# Membership

Works with lists, tuples, sets, strings, and dictionaries (checks keys).

```python
if "apple" in fruits:
    print("Found")

if 5 not in numbers:
    print("Missing")
```

---

# Truthiness

```python
if my_list:
    print("Not empty")

if not my_list:
    print("Empty")
```

Works for:

```python
[]
{}
set()
()
""
0
None
```

All of the above evaluate to `False`.

---

# When to use which?

| Need                                  | Use     |
| ------------------------------------- | ------- |
| Ordered collection that changes       | `list`  |
| Ordered collection that never changes | `tuple` |
| Unique values / fast `in` checks      | `set`   |
| Key → value mapping                   | `dict`  |

### Rule of thumb

* **List** → "A sequence of things."
* **Tuple** → "A fixed record of values."
* **Set** → "Unique items."
* **Dict** → "Look up information by a key."

Here’s a **clean, interview-ready cheat sheet** for Python mutation rules. This is the kind of thing that directly helps in coding interviews and debugging questions.

---

# 🧠 Python Mutation Rules Cheat Sheet (Lists, Dicts, Sets)

---

# 📌 1. LISTS — mutation rules

## ✅ Safe operations

```python
a[i] = value        # modify element
a.append(x)         # add element
a.pop()             # remove last element
a.remove(x)         # remove by value
```

## ❌ Dangerous during iteration

```python
for x in a:
    a.append(1)     # ❌ unsafe
```

### Why?

* list iterator expects stable size
* modifying size → can skip elements or behave unpredictably

---

## ⚠️ Safe pattern (correct way)

```python
for x in a[:]:      # iterate over copy
    a.append(x)
```

or

```python
new_list = []
for x in a:
    new_list.append(x)
```

---

# 📌 2. DICTIONARIES — mutation rules

## ✅ Safe operations

```python
d[k] = value        # modify value
d.get(k)            # read safely
```

## ❌ Unsafe operations

```python
for k in d:
    d["new"] = 1    # ❌ structure change
```

```python
for k in d:
    del d[k]        # ❌ always unsafe
```

---

## 🧠 Key rule

| Operation             | Safe?                        |
| --------------------- | ---------------------------- |
| change existing value | ✅ yes                        |
| add new key           | ⚠️ sometimes works but risky |
| delete key            | ❌ no                         |

---

## ⚠️ Safe pattern

```python
for k in list(d.keys()):
    d[k] += 1
    d["new"] = 5
```

or

```python
for k, v in d.copy().items():
    ...
```

---

# 📌 3. SETS — mutation rules

## ❌ STRICT RULE

### NEVER change size during iteration

```python
for x in s:
    s.add(1)      # ❌ RuntimeError
```

```python
for x in s:
    s.remove(x)   # ❌ RuntimeError
```

---

## 🧠 Why sets are strict

* unordered
* hash-based structure
* iteration depends on internal hash table stability

---

## ✅ Safe patterns

```python
for x in list(s):
    s.add(10)
```

or

```python
new_set = set()
for x in s:
    new_set.add(x)
```

---

# 🔥 4. SHARED REFERENCE RULE (VERY IMPORTANT)

## ❗ Everything in Python is reference-based

```python
a = [1, 2]
b = a
```

➡ same object

---

## 📌 Copy types

| Expression         | Type                    |
| ------------------ | ----------------------- |
| `b = a`            | reference (same object) |
| `b = a.copy()`     | shallow copy            |
| `b = a[:]`         | shallow copy            |
| `copy.deepcopy(a)` | full independent copy   |

---

# ⚠️ 5. SHALLOW COPY TRAP

```python
a = [[1], [2]]
b = a[:]
```

* outer list copied ✔
* inner objects shared ❌

---

# 📌 6. BIG INTERVIEW RULE (MOST IMPORTANT)

## 🧠 Golden rule:

> “Never change the size of a collection while iterating over it.”

Applies to:

* list
* dict
* set

---

# 🧩 7. SAFE ITERATION PATTERNS

## Lists

```python
for x in a[:]:
```

## Dicts

```python
for k in list(d):
```

## Sets

```python
for x in list(s):
```

---

# 🚀 8. QUICK INTERVIEW SUMMARY

| Type | Modify values | Add/remove items during loop |
| ---- | ------------- | ---------------------------- |
| list | ✅ safe        | ❌ unsafe                     |
| dict | ✅ safe        | ❌ unsafe (especially delete) |
| set  | ❌ risky       | ❌ unsafe                     |

---

# 🎯 FINAL INTERVIEW TIP

If unsure in interviews, say:

> “I would avoid modifying the structure during iteration and instead iterate over a copy.”
