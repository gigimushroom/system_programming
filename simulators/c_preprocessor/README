# Write a C Preprocessor
## Features
Provide a C like file.
Parsing has 2 phases.
1st path is to search all C defines, install to hashtable
2nd path is the replacement, for each recurrence, replace it.

## Expected Result:
End result should still be compiled and work the same way.



## Lesson Learnt
### `malloc` allocates the actual size of the object, 
not the pointer size.

Example:
```
struct nlist* np = 
  (struct nlist*)malloc(sizeof(struct nlist));
```

`struct nlist` size is 24 bytes, `struct list *` size is 8 bytes.

After allocation, we could cast to the pointer, for easy usage.
But if we call `malloc(sizeof(struct nlist*))`, 
we are going to access invalid memory when go beyond allocated size.



