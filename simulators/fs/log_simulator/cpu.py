import memory
import logger
import pprint
import disk


class CPU:
  def __init__(self):
    self.memory = memory.Memory()
    self.processor = logger.LogProcessor()
    self.txn_blks = set()
    # TODO: Re-write it as to crash at sequence X.
    self._crash = 0

  def make_crash(self):
    self._crash = 1
    self.memory.restart()
    return

  def restart(self):
    self.memory.restart()
    self.processor.recover_from_log()

  def _commit_txn(self):
    self.processor.commit(self.memory, self.txn_blks,
                          self._crash)
  
  def print_fs_blks(self):
    pprint.pprint(disk.fs.blks)

  def run(self, cmds):
    # Parse commands
    # Start txn
    # End txn
    # let log processor to commit.

    for cmd in cmds:
      words = cmd.split()
      ops = words[0]
      if ops == 'begin':
        print('Starting transaction...')
        self.txn_blks.clear()
      elif ops == 'end':
        print('Ending transaction...')
        self._commit_txn()
        self.txn_blks.clear()
      elif ops == 'read':
        blk = int(words[1])
        key = words[2]
        #print 'Read block no', blk, 'key', key
        #print 'Result:', self.memory.read_data(blk, key)
      elif ops == 'write':
        blk = int(words[1])
        key = words[2]
        v = words[3]
        #print 'Write block no', blk, 'key', key, 'val', v
        self.memory.write_data(blk, key, v)
        self.txn_blks.add(blk)
      elif ops == 'crash':
        self.make_crash()
        print '!!!!!Our CPU is killed!!!!!'
        return
      else:
        print('Unknown cmd!')

    #self.processor.print_fs_log()