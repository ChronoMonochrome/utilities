#!/usr/bin/python 

import sys, os

DEBUG = 1
GZIP_MAGIC="\x1F\x8B\x08"
LZ4_LEGACY_MAGIC='\x02\x21\x4c\x18'
CPIO_MAGIC='070701'
CPIO_END_SIG='TRAILER'
GZIP = 'gzip'
LZ4 = 'lz4'
UNKNOWN='?'

def debug_print(s):
	global DEBUG
	if DEBUG:
		os.system('echo %s'%s)
		
def is_gziped(s):
	global GZIP_MAGIC
	if s.find(GZIP_MAGIC):
		return 1
	return 0
	
def is_lz4d(s):
	global LZ4_LEGACY_MAGIC
	if s.count(LZ4_LEGACY_MAGIC)==2:
		return 1
	return 0

def find_zimage_start(s):
	global GZIP_MAGIC, LZ4_LEGACY_MAGIC
	if is_lz4d(s):
		res = s.find(LZ4_LEGACY_MAGIC,
		      s.find(LZ4_LEGACY_MAGIC)+1), LZ4 
	elif is_gziped(s):
		res = s.find(GZIP_MAGIC), GZIP
	else:
		return -1, UNKNOWN
	return res

def extract_cpio():
	debug_print('script started')
	
	try:
		bootimg = open("./"+sys.argv[1],'rb').read()
	except:
		debug_print('error occured when reading boot.img')
		return -1
		
	ZIMAGE_START, FORMAT = find_zimage_start(bootimg)
	if (ZIMAGE_START >= 0): 
		debug_print('found zImage at %d'%ZIMAGE_START)
		try:
			if FORMAT == LZ4:
				open('kernel.lz4','wb').write(bootimg[ZIMAGE_START:])
			elif FORMAT == GZIP:
				open('kernel.gz','wb').write(bootimg[ZIMAGE_START:])
			debug_print('zImage was successfully extracted')
		except:
			debug_print('error occured when extracting zImage')
			return -2
		try:		
			if FORMAT == LZ4:
				os.system("lz4c -dy ./kernel.lz4 ./kernel")
			if FORMAT == GZIP:
				os.system("gunzip -qf kernel.gz")
			kernel = open('./kernel','rb').read()
			debug_print('%sd zImage was successfully unpacked' % FORMAT)
		except:
			debug_print('error occured when unpacking zImage')
			return -3
	else:
		debug_print('zImage is not found')
		return -4
	CPIO_START = kernel.find(CPIO_MAGIC)
	CPIO_END = len(kernel)
	#CPIO_START = len(kernel)-kernel[::-1].find(CPIO_MAGIC[::-1], kernel[::-1].find(CPIO_MAGIC[::-1])+1)
	#debug_print('cpio_start=%d'%CPIO_START)
	#CPIO_END = len(kernel) - kernel[::-1].find(CPIO_END_SIG[::-1]),
		   #   kernel[::-1].find(CPIO_END_SIG[::-1])+1)
	debug_print('cpio_end=%d'%CPIO_END)
	if (CPIO_START >= 0): 
		debug_print('found ramdisk at %d'%CPIO_START)
		open('./initramfs.cpio','wb').write(kernel[CPIO_START:CPIO_END])
	else:
		debug_print('error occured when writing ramdisk')
		return -5
	debug_print('ramdisk was successfully extracted to initramfs.cpio!')
		
extract_cpio() 
