#!/usr/bin/python 

import sys, os

if (len(sys.argv) < 2):
	print("Usage %s boot.img" % sys.argv[0])
	exit()

DEBUG = 1	
FILE = "./%s" % sys.argv[1]
DIR = "".join(FILE.split("/")[:-1]) + "/"
GZIP_MAGIC = "\x1F\x8B\x08"
LZO_MAGIC = "\x89LZO\x00"
LZ4_LEGACY_MAGIC = '\x02\x21\x4c'
CPIO_MAGIC = '070701'
CPIO_END_SIG = 'TRAILER'
GZIP = 'gzip'
LZO = 'lzo'
LZ4 = 'lz4'
UNKNOWN = '?'

EXT = {LZO:LZO, LZ4:LZ4, GZIP:"gz"}

def debug_print(s):
	if DEBUG:
		os.system('echo %s'%s)
		
def is_gziped(s):
	if s.find(GZIP_MAGIC) > 0:
		return 1
	return 0

def is_lzod(s):
	if s.count(LZO_MAGIC) == 5:
		return 1
	return 0
	
def is_lz4d(s):
	if s[:10240].find(LZ4_LEGACY_MAGIC) > 0:
		return 1
	return 0

def find_zimage_start(s):
	if is_lzod(s):
		res = s.find(LZO_MAGIC,
		      s.find(LZO_MAGIC)+1), LZO
	elif is_lz4d(s):
		res = s.find(LZ4_LEGACY_MAGIC,  s.find(LZ4_LEGACY_MAGIC) + 1), LZ4
	elif is_gziped(s):
		res = s.find(GZIP_MAGIC), GZIP
	else:
		return -1, UNKNOWN
	return res

def extract_cpio():
	debug_print('script started')
	
	try:
		bootimg = open(FILE,'rb').read()
	except:
		debug_print('error occured when reading boot.img')
		return -1
		
	ZIMAGE_START, FORMAT = find_zimage_start(bootimg)
	zimage_file = 'kernel.%s' % EXT[FORMAT]
	if (ZIMAGE_START >= 0): 
		debug_print('found zImage at %d'%ZIMAGE_START)
		open(zimage_file,'wb').write(bootimg[ZIMAGE_START:])
		
		if FORMAT == LZO:
			os.system("lzop -d ./%s ./kernel" % zimage_file)
		elif FORMAT == LZ4:
			os.system("lz4c -dy ./%s ./kernel" % zimage_file)
		elif FORMAT == GZIP:
			os.system("gunzip -qf %s" % zimage_file)
		else:
			debug_print('Unknown format')
			return -2
		
		kernel = open('./kernel','rb').read()
		debug_print('%sd zImage was successfully unpacked' % FORMAT)
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

def clean():
	for i in EXT.values():
	      if os.path.exists(DIR + "kernel.%s" % i):
		    debug_print("file kernel.%s removed" % i)
		    os.remove(DIR + "kernel.%s" % i)
		    
	if os.path.exists(DIR + "kernel"):
		    debug_print("file kernel removed")
		    os.remove(DIR + "kernel")
		    
def pre_clean():
	clean()
	
pre_clean()	
extract_cpio() 
clean()
