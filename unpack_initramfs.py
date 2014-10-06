#!/usr/bin/python 

import sys, os
DEBUG = 1

def debug_print(s):
	global DEBUG
	if DEBUG:
		os.system('echo %s'%s)

def extract_cpio():
	GZIP_MAGIC="\x1F\x8B\x08"
	CPIO_MAGIC='070701'
	debug_print('script started')
	
	try:
		bootimg = open("./"+sys.argv[1],'rb').read()
		debug_print('%s was successfully readed'%sys.argv[1])
	except:
		debug_print('fail during read boot.img')
		return -1
		
	ZIMAGE_START = bootimg.find(GZIP_MAGIC)
	if (ZIMAGE_START >= 0): 
		debug_print('found zImage at %d'%ZIMAGE_START)
		try:
			open('kernel.gz','wb').write(bootimg[ZIMAGE_START:])
			debug_print('zImage was successfully extracted')
		except:
			debug_print('fail during writing zImage')
			return -2
		try:
			os.system("gunzip -qf kernel.gz")
			kernel = open('./kernel','rb').read()
			debug_print('successfully unpacked gzipd zImage')
		except:
			debug_print('error occured when unpacking zImage')
			return -3
	else:
		return -4
	CPIO_START = kernel.find(CPIO_MAGIC)
	if (CPIO_START >= 0): 
		debug_print('found ramdisk at %d'%CPIO_START)
		open('./initramfs.cpio','wb').write(kernel[CPIO_START:])
	else:
		debug_print('error occured when writing ramdisk')
		return -5
	debug_print('ramdisk was successfully extracted to initramfs.cpio!')
		
extract_cpio()