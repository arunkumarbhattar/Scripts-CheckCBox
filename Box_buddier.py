import os
import shutil
import sys
import argparse

# Argument parsing
parser = argparse.ArgumentParser(description="Provide path to the Tainted directory")
parser.add_argument("--tnt", type=str, required=True)
args, args_other = parser.parse_known_args()

# create a temp directory and clone the ISC repository
os.system("mkdir temp_files")
try:
    # now perform gitclone of ISC repository
    chdir = str(os.getcwd() + "/temp_files")
    os.chdir(chdir)
    os.system("git clone https://github.com/arunkumarbhattar/Check-C-Box-ISC.git")
    chdir = str(os.getcwd() + "/Check-C-Box-ISC/")
    os.chdir(chdir)

    isc_base_dir = os.getcwd()

    tnt_base_dir = args.tnt


    # Copy all the tainted .C file from the tnt directory to the isc's library directory
    isc_lib_dir = isc_base_dir + "/unsafe_code_goes_in_here"
    tainted_c_files = os.listdir(tnt_base_dir)
    try:
        for file in tainted_c_files:
            shutil.copy2(os.path.join(tnt_base_dir, file), isc_lib_dir)
            print("Copying tainted Source code file ", str(file))
    except Exception as e:
        print("Tainted source code transfer to ISC FAIL!! due to ", e)

    print("Tainted source code files Successfully copied to ISC")

    # now switch to ISC's unsafe code directory

    cmd = str(isc_lib_dir)
    os.chdir(cmd)

    try:
        # Now execute make here
        cmd = 'make'
        os.system(cmd)
    except Exception as e:
        print("Compiling Tainted Source code to .wasm failed!! due to ", e)

    # now convert the generated lib.wasm file to lib_wasm.c/.h files
    try:
        # now execute wasm2c commadn here
        cmd = './wasm2c -o lib_wasm.c lib.wasm'
        os.system(cmd)
    except Exception as e:
        print("wasm2c Conversion of tainted wasm binary failed!! due to ", e)

    # now copy the generated lib_wasm.c and .h files to the wasm_readable definitions directory

    wasm_readable_dir = str(isc_base_dir) +  "/wasm_readable_definitions"
    cmd = 'mv lib_wasm.* ' + wasm_readable_dir
    os.system(cmd)

    # now switch to base directory and execute cmake build commands
    cmd = isc_base_dir
    os.chdir(cmd)
    cmd = "cmake -S ./ -B ./build"
    os.system(cmd)
    cmd = "cmake --build ./build --parallel"
    os.system(cmd)

    # now switch to the cmake build directory and copy the generated archive to the place where the script was executed
    staticLib = str(isc_base_dir) + "/build/libisc_lib_final.a"
    # now copy this file to ISC directory
    os.chdir(str(tnt_base_dir) + "/../")
    os.system("mv " + staticLib + " .")

finally:
    os.system("rm -rf temp_files")


