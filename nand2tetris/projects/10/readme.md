```
in ~/Desktop/code/system_programming/nand2tetris/projects/10 on git:master x [14:44:21]
$ python3 JackAnalyzer.py ArrayTest
test....
File full path ArrayTest/Main.jack
Tokenizer output file ArrayTest/output/MainT.xml
Parser output file ArrayTest/output/Main.xml

in ~/Desktop/code/system_programming/nand2tetris/projects/10 on git:master x [14:44:29]
$ python3 JackAnalyzer.py Square
test....
File full path Square/Square.jack
Tokenizer output file Square/output/SquareT.xml
Parser output file Square/output/Square.xml
File full path Square/SquareGame.jack
Tokenizer output file Square/output/SquareGameT.xml
Parser output file Square/output/SquareGame.xml
File full path Square/Main.jack
Tokenizer output file Square/output/MainT.xml
Parser output file Square/output/Main.xml

in ~/Desktop/code/system_programming/nand2tetris/projects/10 on git:master x [14:44:34]
$ python3 JackAnalyzer.py ExpressionLessSquare
test....
File full path ExpressionLessSquare/Square.jack
Tokenizer output file ExpressionLessSquare/output/SquareT.xml
Parser output file ExpressionLessSquare/output/Square.xml
File full path ExpressionLessSquare/SquareGame.jack
Tokenizer output file ExpressionLessSquare/output/SquareGameT.xml
Parser output file ExpressionLessSquare/output/SquareGame.xml
File full path ExpressionLessSquare/Main.jack
Tokenizer output file ExpressionLessSquare/output/MainT.xml
Parser output file ExpressionLessSquare/output/Main.xml
```

## Compare scripts
```
./TextComparer.sh ../projects/10/Square/output/SquareGame.xml ../projects/10/Square/SquareGame.xml
./TextComparer.sh ../projects/10/Square/output/Square.xml ../projects/10/Square/Square.xml
./TextComparer.sh ../projects/10/Square/output/Main.xml ../projects/10/Square/Main.xml

./TextComparer.sh ../projects/10/ArrayTest/Main.xml ../projects/10/ArrayTest/output/Main.xml

./TextComparer.sh ../projects/10/ExpressionLessSquare/SquareGame.xml ../projects/10/ExpressionLessSquare/output/SquareGame.xml
./TextComparer.sh ../projects/10/ExpressionLessSquare/Square.xml ../projects/10/ExpressionLessSquare/output/Square.xml
./TextComparer.sh ../projects/10/ExpressionLessSquare/Main.xml ../projects/10/ExpressionLessSquare/output/Main.xml
```
