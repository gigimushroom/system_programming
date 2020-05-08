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

# Our Simulator vs Unix File System Logger
In unix, every FS(file system) system call writes to logger system's memory buffer.
When no outstanding system calls, logger commits by writing its log buffers to log's disk positions.
Then marks as committed.

In our simulator, we simplified things by removing the logger in memory concept.
We treat logger object is the on disk logger.
We only commit to logger when transaction commits (issue `end` cmd).

#### The following concept is the same
When txn is commited, operations can be recovered if crashed.
If crash happening before commit, all operations in memory are lost.


# TODOs
1. Add unittest
2. Simulate crash to happen after X instructions
3. Write fs and log blocks to actual files. No more simulation.


