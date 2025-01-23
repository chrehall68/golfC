# GolfC

Ever wanted to minify your C code? Now you can. This repository provides a code-minifier for
programs written in C. Simply build the repository and run the executable `minifier` on
your source C file, and the program will produce a minified C file on stdout.

Alternatively, add the -i flag in order to apply the changes in place.

Note: as of now, you must provide the include directories as extra arguments to the executable.
For instance:

```sh
minifier myFile.c -- -I /usr/include
```

## Building Natively

In order to build the executable natively, you'll need to have the following packages
installed on your system:

- libclang-17-dev
- clang-17
- llvm-17-dev

You'll also need a working C++ compiler.

If you have all of these, you can run the below to configure and make the project.

```sh
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=MinSizeRel -DLLVMVersion=17
cmake --build .
```

After running the above, there should be an executable `minifier` in the `build` directory

## Building with Docker

You can also build the executable with Docker. Simply run the below command to generate
an executable `minifier` in the current directory.

```sh
docker build --output=. .
```

## Motivation

Why minify C code? Unlike Javascrpt and HTML where the source code must be sent over the web,
making code size actually important, source code size has no effect on C programs. After all,
everything gets compiled down into the same bytecode. However, some UC professors have been
known to offer EC assignments that ask their students to "golf" their code (use the minimum
number of bytes possible to implement their program). While this repository won't optimize
your code by changing its structure, it will at least minify any existing code by removing
any spaces and replacing repeated patterns with defines (when it's worth it).

## Design

The design is quite simple. First, we make a pass over the input and convert all variables
into minimum-size variables.

Then, (WIP) we do a pass over this output to look for patterns of repeated tokens. If a pattern satisfies
the equation `N*L < 9+X+L`, where N is the number of appearances, L is the length of the pattern,
in bytes, and X is the length of the next available identifier, then a define is added to the file
and all occurrences of the pattern are replaced with the identifier assigned to the pattern.

Finally, we do a pass over the tokens to remove spaces where applicable.
