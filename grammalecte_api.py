#!/usr/bin/env python3

import sys
import os.path
import json

import Grammalecte.grammalecte as grammalecte

def generateParagraphFromBuffer (buff, bConcatLines=False):
	lines = buff.split("\n")

	"generator: returns text by tuple of (iParagraph, sParagraph, lLineSet)"
	if not bConcatLines:
		for iParagraph, sLine in enumerate(lines, 1):
			yield iParagraph, sLine, None
	pass

def main (buffer):

	oGrammarChecker = grammalecte.GrammarChecker("Grammalecte.grammalecte.fr")
	oSpellChecker = oGrammarChecker.getSpellChecker()
	oLexicographer = oGrammarChecker.getLexicographer()
	oTextFormatter = oGrammarChecker.getTextFormatter()

	oGrammarChecker.gce.setOptions({"html": True, "latex": True})

	bComma = False

	sOutput = ""

	sOutput +='{ "grammalecte": "'+oGrammarChecker.gce.version+'", "lang": "'+oGrammarChecker.gce.lang+'", "data" : [\n'

	for i, sText, lLineSet in generateParagraphFromBuffer(buffer):

		sText = oGrammarChecker.generateParagraphAsJSON(i, sText, bContext=True, bEmptyIfNoErrors=True, \
																bSpellSugg=True, bReturnText=False, lLineSet=lLineSet)
		if sText:
			if bComma:
				sOutput += ",\n"
			sOutput += sText
			bComma = True
			
	sOutput += "\n]}\n"
	return sOutput

