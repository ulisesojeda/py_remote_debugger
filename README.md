# Reverse remote debugging with pdb

Allows remote debugging with pdb (Python built-in debugger) by reverse
and direct connections to tools like **netcat** and **socat**.

Inspired by: https://pypi.org/project/rpdb/

### Installation
```bash
pip install reverse_pdb
```

## Usage:
### Remote reverse debugging
  1. Given this snippet to be debug with **pdb**

```python
def add_numbers(a, b):
    return a + b
result = add_numbers(3, 5)

breakpoint()

print("The sum is:", result)
```

  2. Add the following changes

```python
from reverse_pdb import remote_pdb_reverse

def add_numbers(a, b):
    return a + b
result = add_numbers(3, 5)

rdb = remote_pdb_reverse("127.0.0.1", 4444)
rdb.set_trace()

print("The sum is:", result)
```

  3. Run a **netcat** listener
```bash
nc -vlp 4444
```

  4. Run your code and interact with **pdb** from the **netcat** session

### Remote "direct" debugging
  1. Add these changes

```python
from reverse_pdb import remote_pdb

def add_numbers(a, b):
    return a + b
result = add_numbers(3, 5)

rdb = remote_pdb("127.0.0.1", 4444)
rdb.set_trace()

print("The sum is:", result)
```

  2. Run a **netcat** client
```bash
nc -v localhost 4444
```

  3. Run your code and interact with **pdb** from the **netcat** session

## Note: 
**In the above examples the loopback (127.0.0.1) is used for simplicity, however, any IP/hostname is also valid.**

## Uses cases
Remote debugging from:

  1. Behind a firewall/NAT
  2. Airflow tasks
  3. Sealed environments like AWS MWAA (AWS managed Airflow)

## Author

Ulises <ulises.odysseus22@gmail.com>
