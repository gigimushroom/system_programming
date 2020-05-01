import disk
import copy


class Memory:
  buffers = {}
  buf_size = 0

  def _fetch_block(self, blk_no):
    if blk_no in self.buffers:
      blk = self.buffers[blk_no]
    else:
      blk = disk.fs.get_block(blk_no)
      self.buffers[blk_no] = blk
      self.buf_size += 1
    
    # Use a copy. Dict is copy by ref.
    return copy.deepcopy(blk)

  def write_data(self, blk_no, key, val):
    blk = self._fetch_block(blk_no)
    blk.data[key] = val
    # Save it back to memory.
    self.buffers[blk_no] = blk
    #print('Size of blocks in mem:', len(self.buffers))

  def read_data(self, blk_no, key):
    blk = self._fetch_block(blk_no)
    return blk.data[key]

  def restart(self):
    self.buffers.clear()
    self.buf_size = 0











