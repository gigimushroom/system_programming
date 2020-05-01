import disk
import copy
import pprint


COMMITTING = 1
IDLE = 0


class Log:
  buffers = []
  state = IDLE
  outstanding = 0 # number of on-going system calls.
  
  def __str__(self):
    blks = [b.data for b in self.buffers]
    return str(blks)

class LogProcessor:
  def __init__(self):
    self.log = Log()

  def commit(self, mem, block_list, crash=0):
    self.log.buffers = []
    self.log.outstanding += 1

    for b in block_list:
      if len(mem.buffers) == 0:
        print 'Memory is empty. Nothing to commit.'
        return

      blk = copy.deepcopy(mem.buffers[b])
      # Write modified blk from mem to log
      self.log.buffers.append(blk)
    
    # Update metadata.
    self.log.state = COMMITTING

    # AT THIS POINT, WE ARE SAFE!
    if crash:
      # For testing purpose, simulate crash after commit.
      self.print_fs_log()
      print('!!!!!!!!!!!!!!!CRASHED!!!!!!!!!!!!!!!!')
      return

    # Install writes from log to disk.
    self._install_write()

    # Clear log and metadata
    self._clear_log()

    return

  def _update_log_state(self, state):
    self.log.state = state
  
  def _install_write(self):
    # Install writes from log blocks to home location in disk.
    for log in self.log.buffers:
      disk.fs.write_to_disk(log.blk_no, log)

    return

  def _clear_log(self):
    self.log.buffers = []
    self._update_log_state(IDLE)
    self.log.outstanding = 0

  def recover_from_log(self):
    print('Recover from log...')
    
    # Install writes from log to disk.
    self._install_write()
    # Clear log and metadata
    self._clear_log()

    self.print_fs_log()

  def print_fs_log(self):
    print('Current Logger state:')
    print(self.log)
    print('Current File System state:')
    print(disk.fs)