# Simulate crash after commit:

1. Starting transaction...
2. write, read, more writes...

3. SIMULATE SERVER CRASHED after commit:
Txns all saved in log space, but not yet writting to disk.

4. System states:
Current Logger state:
[{'baby': 'xiaying'}, {'mami': 'yoyo', 'haha': 'xiaoyoyo'}]
Current File System state:
[{}, {}, {}, {}, {}, {}, {}, {}, {}, {}]

5. Recover from log. Install writes from log to disk.

6. System states:
Current Logger state:
[]
Current File System state:
[{'baby': 'xiaying'}, {'mami': 'yoyo', 'haha': 'xiaoyoyo'}, {}, {}, {}, {}, {}, {}, {}, {}]

7. Log is cleared after installing. FS is updated.


# TODOs
1. Add unittest
2. Simulate crash to happen after X instructions
3. Write fs and log blocks to actual files. No more simulation.
