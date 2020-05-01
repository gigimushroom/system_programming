import copy

class DiskBlock:
  def __init__(self, blk_no):
    self.blk_no = blk_no
    self.data = {}
  def __str__(self):
    return str(self.data)

class FS:
  blks = [] # store actual data
  alloc_bit_map = [] # key is block no., val is 0 or 1.

  def __init__(self, size=10):
    for i in range(0, size):
      self.blks.append(DiskBlock(i))
      self.alloc_bit_map.append(1)

  def __str__(self):
    blks = [b.data for b in self.blks]
    return str(blks)

  def get_block(self, blk_no):
    #print 'getting block no:', blk_no
    return self.blks[blk_no]

  def get_empty_block(self):
    return

  def write_to_disk(self, blk_no, data):
    #print('Writing', blk_no, 'to disk.')
    self.blks[blk_no] = copy.deepcopy(data)
    self.alloc_bit_map[blk_no]

  def reset(self):
    # Reset FS to clean state. Mainly for testing.
    self.blks = []
    self.alloc_bit_map = []
    self.__init__()

fs = FS()