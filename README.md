# parse_cpp
This is a freelance project where a basic cpp code is parsed using python libclang library.

# Introduction

This is a python program that uses libclang to parse a C++ code. 

For more information, please see https://eli.thegreenplace.net/2011/07/03/parsing-c-in-python-with-clang

# Installation (This is for Mac OS and Python version is 3)

Prerequisite : Python 3 and pip3 is reuired
1. pip3 install clang
   current version will be above 6
2. Download LLVM binaries specific to the MaC OS from https://releases.llvm.org/download.html#10.0.0
   
   Note: Download from llvm 9.0.0.0 and once downloaded, run it. Please make a note of the path of libclang.dylib.
	It will be present in '/Users/<username>/Downloads/clang+llvm-9.0.0-x86_64-darwin-apple/lib/libclang.dylib'
	This needs to be replaced within 'clang.cindex.Config.set_library_file' inside the 'parse_cpp.py' file.

3. Install packages for drawing graph
	
	pip3 install networkx
	pip3 install matplotlib

How to run the script ?

	Open the terminal and navigate to the folder where the source code and input file resides.
	Run the command python3 <pythonfilename.py> <cppfile>
	Eg: python3 parse_cpp.py simple_demo_src.cpp
	
	Note: Please make sure you are using the correct file name while running

