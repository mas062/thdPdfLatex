#!/usr/bin/env python

import os, shutil, sys
from numpy import sort

def PrepAllPapers(howMany=1, workdir = "."):
	"""
	Prepare paper PDFs for inclusion in thesis as figures: Burst all 
	papers into one PDF per page, and crop margin whitespace.
	"""
	os.chdir(workdir)

	#Iterate over papers, burst and crop
	map(PrepPaper, range(1,howMany+1))

class PaperDoesNotExistException(Exception):
	pass


def PrepPaper(paperIndex):
	paper = "paper%i.pdf" % paperIndex
	if not os.path.exists(paper):
		raise PaperDoesNotExistException("Paper %i does not exist or is not correctly named, please name it %s and put it in this folder" % (paperIndex, paper))

	print "Preparing Paper %i" % paperIndex

	#Remove previous prep
	dirName = "paper-%i" % (paperIndex)
	if os.path.exists(dirName):
		shutil.rmtree(dirName)
	#create output folder
	os.mkdir(dirName)
	
	#Copy paper PDF to workingdir
	shutil.copy(paper, "%s/" % dirName) 
	os.chdir(dirName)

	#Burst it
	BurstPDF(paper)

	#Crop each page and convert to ps
	pageFiles = sort([fname for fname in os.listdir(".") if fname[:3] == "pg_"])
	for pageNum, pfn in enumerate(pageFiles):
		
		#Crop
		croppedPDF = "%s-crop.pdf" % pfn.strip(".pdf")
		pdfName="page_%i.pdf" % pageNum
		#CropPDF(pfn, croppedPDF)
		CropPDF(pfn, pdfName)
#ADDED BY MEISAM
		# #Convert to PS
		# psName = "page_%i.ps" % pageNum
		# PDFtoPS(croppedPDF, psName)
		
		#Remove tmp files
		os.remove(pfn)
		#os.remove(croppedPDF)

	#Remove more tmp files
	os.remove(paper)
	os.remove("doc_data.txt")

	os.chdir("..")


def BurstPDF(pdfName):
	"""
	Burst a PDF into separate files for each page
	"""
	os.system("pdftk %s burst" % pdfName)


def PDFtoPS(infile, outfile):
	"""
	Convert a PDF to a PS file
	"""
	os.system("pdftops %s %s" % (infile, outfile))


def PStoPDF(infile, outfile):
	"""
	Convert a PS file to a PDF
	"""
	os.system("ps2pdf %s %s" % (infile, outfile))


def CropPDF(infile, outfile):
	"""
	Remove margin whitespace from a PDF
	"""
	os.system("pdfcrop %s %s" % (infile, outfile))


if __name__ == "__main__":
	from optparse import OptionParser
	import sys

	parser = OptionParser()
	parser.add_option("--prepare-all", action="store_true", dest="prepare_all", default=False)
	parser.add_option("--prepare-paper", action="store", type="int", dest="paper_index", default=-1)
	parser.add_option("--paper-count", action="store", type="int", dest="paper_count", default=-1)

	(opts, args) = parser.parse_args()
	try:
		if opts.prepare_all and not opts.paper_index > 0:
			if opts.paper_count > 0:
				PrepAllPapers(howMany=opts.paper_count)
			else:
				parser.print_help()
				print ""
				print "Specify the --paper-count=[number of papers available for processing]"
				print ""
				sys.exit(-1)
		elif opts.paper_index > 0:
			PrepPaper(opts.paper_index)
		else:
			parser.print_help()
			print ""
			print "Specify either --prepare-all or --prepare-paper=[index of paper to process] "
			print ""
			sys.exit(-1)

	except PaperDoesNotExistException, ex:
		print ""
		print "%s" % ex.args[0]
		print ""



