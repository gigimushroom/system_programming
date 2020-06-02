# udacity-cs212

peter norvig 讲解python程序设计笔记

## L1 poker_game

- 程序设计的纬度问题：正确，效率，新功能，优雅
- kind重构，DRY
- shuffle问题的研究，正确（概率一致）还有复杂度

## L2 zebra_puzzle

- 生成器表达式与列表生成器
- 暴力计算所有可能，估算可能性数量
- 调整if顺序可以减少循环次数和用时，用时函数和执行次数函数
- ODD+ODD=EVEN 问题
  - 暴力计算，cProfile.run追踪最耗时的函数
  - 编译单词，减少eval 提升速度

## L3 regular_expression

- 解释器与编译器
  - 低级的编译，编译成python函数，本课程
  - 中级的编译，编译成虚拟机执行的字节码，如java和python
  - 高级的编译，编译成计算机可以运行的二进制代码，如C语言
- decorate重构函数，使原本接受两个参数的函数可以接受多个参数
- decorate的cache管理，递归时，保存已经计算的结果到cache中，避免重复计算，提高效率
- decorate的trace
- parse解析器

## L4 water_pourinng

- 搜索问题的解决：
  - successors：基于当前状态，返回下一状态的可能结果
  - frontier：存储所有准备走的路径，每次处理某种顺序的第一个
  - explored：达到过的状态，避免重复
- shortest_path_search函数的一般化

## L5 play pig

- 游戏理论Q和U
  - U：实际效用
  - Q：基于效用的可能结果的期望值
- 小猪游戏中两类U产生不同的策略
  - 以赢得结果为目标
  - 以最大比分差为目标

## L6 word game

- 问题分步解决的方式