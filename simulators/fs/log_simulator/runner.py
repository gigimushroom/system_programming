import memory
import logger
import cpu
import pprint
import unittest
import disk

seqs = [
  'begin',
  'write 0 baby xiaying',
  'write 1 mami yoyo',
  'write 1 haha baby',
  'write 1 haha xiaoyoyo',
  'read 0 baby',
  'read 1 haha',
  'end'
]

seqs_crash = [
  'begin',
  'write 0 baby xiaying',
  'write 1 mami yoyo',
  'write 1 haha baby',
  'write 1 haha xiaoyoyo',
  'crash', # CRASH!
  'read 0 baby',
  'read 1 haha',
  'end'
]

class TestLogSimulator(unittest.TestCase):
  empty_fs = str([{}, {}, {}, {}, {}, {}, {}, {}, {}, {}])

  def tearDown(self):
    disk.fs.reset()

  def test_normal(self):
    my_cpu = cpu.CPU()
    my_cpu.run(seqs)
    expected = str([{'baby': 'xiaying'}, {'mami': 'yoyo', 'haha': 'xiaoyoyo'}, {}, {}, {}, {}, {}, {}, {}, {}])
    self.assertEqual(expected, str(disk.fs))

  def test_crash_after_commit(self):
    my_cpu = cpu.CPU()
    my_cpu.make_crash()
    my_cpu.run(seqs)
    # FS is empty due to system crash right before install updates.
    self.assertEqual(self.empty_fs, str(disk.fs))

    # System restarts and FS recovers from log.
    my_cpu.restart()
    
    expected = str([{'baby': 'xiaying'}, {'mami': 'yoyo', 'haha': 'xiaoyoyo'}, {}, {}, {}, {}, {}, {}, {}, {}])
    self.assertEqual(expected, str(disk.fs))

  def test_crash_before_commit(self):
    my_cpu = cpu.CPU()
    my_cpu.run(seqs_crash)
    # Check log is empty
    self.assertEqual(0, len(my_cpu.processor.log.buffers))
    self.assertEqual(self.empty_fs, str(disk.fs))

    my_cpu.restart()

    # FS is not updated.
    self.assertEqual(self.empty_fs, str(disk.fs))


if __name__ == '__main__':
    unittest.main()