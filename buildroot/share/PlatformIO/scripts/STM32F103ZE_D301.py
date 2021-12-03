import os
Import("env")

STM32_FLASH_SIZE = 512

for define in env['CPPDEFINES']:
    if define[0] == "VECT_TAB_ADDR":
        env['CPPDEFINES'].remove(define)
    if define[0] == "STM32_FLASH_SIZE":
        STM32_FLASH_SIZE = define[1]

# Relocate firmware from 0x08000000 to 0x08007000
env['CPPDEFINES'].append(("VECT_TAB_ADDR", "0x08007000"))

custom_ld_script = os.path.abspath("buildroot/share/PlatformIO/ldscripts/STM32F103ZE_D301.ld")
for i, flag in enumerate(env["LINKFLAGS"]):
    if "-Wl,-T" in flag:
        env["LINKFLAGS"][i] = "-Wl,-T" + custom_ld_script
    elif flag == "-T":
        env["LINKFLAGS"][i + 1] = custom_ld_script

def encrypt(source, target, env):
    import sys
    firmware = open(target[0].path, "rb+")
    length = os.path.getsize(target[0].path)
    position = 0
    try:	    
        while position < length:
            byte = firmware.read(1)
            position += 1
        while length & 511 > 0:
            print("write....")
            string = " "
            str2byte = bytes(string, encoding = "utf8")
            firmware.write(str2byte)
            length += 1
    finally:
        firmware.close()
env.AddPostAction("$BUILD_DIR/${PROGNAME}.bin", encrypt);
