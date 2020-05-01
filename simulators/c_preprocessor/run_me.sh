echo "This is C preprocessor tool.\n"
echo "Tranform the macros defined in C code before compilation.\n"
echo "This script does the following:
1. Compile the C preprocessor.
2. Run the preprocessor with input, output args.
3. Print generated file.
4. Compile the generated file.
5. Clean up.
"

make

echo "\n...Preprocessing starts...."
./processor input/simple_text.c output/t.c

echo "...Code generation completed."

echo "\n"

echo "...GENERATED FILE......"
cat output/t.c
echo ".......................\n"

echo "...Compiling new generated C file..."
gcc -o ./output/t output/t.c

echo "\n"

echo "!!!RUNNING THE PROGRAM!!!!!"
./output/t
echo "!!!END OF RUNNING!!!!!\n"

rm ./output/t
rm ./output/t.c
make clean
