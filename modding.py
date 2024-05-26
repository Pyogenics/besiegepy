'''
This module deals with mod I/O.

Copyright (c) 2024 Pyogenics

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import xmltodict

class BesiegeMod:
	def __init__(self):
		# State
		self.loaded = False		# Wether or not we've loaded a mod from disk yet
		self.virtual = False	# Wether or not we're creating a mod from scratch

		# Our data
		self.manifest = {}		# Mod.xml

	'''
	Main init functions
	'''

	def createNew(self, modName, modAuthor):
		if self.loaded or self.virtual:
			# We've already created or loaded a mod!
			raise RuntimeException("Couldn't create a new mod, we've already got stuff loaded.")

		self.virtual = True
		self.createTemplateManifest(modName, modAuthor)

	def loadFromDisk(self, path, clone=False):
		if self.loaded or self.virtual:
			# We've already created or loaded a mod!
			raise RuntimeException("Couldn't load mod, we've already got stuff loaded.")

		self.loaded = not clone
		self.virtual = clone
		with open(f"{path}/Mod.xml") as manifestFile:
			manifestSrc = manifestFile.read()
			manifest = xmltodict.parse(manifestSrc)
			self.manifest = manifest["Mod"]	# We can assume that we are inside <Mod></Mod>, shortens any paths we take to traverse the dict

	'''
	Helper functions
	'''

	def createTemplateManifest(self, name, author):
		self.manifest["Name"] = name
		self.manifest["Author"] = author
		self.manifest["Version"] = "0.0.1"
		self.manifest["Description"] = "Description"
		self.manifest["Debug"] = "true"
		self.manifest["MultiplayerCompatible"] = "true"
		self.manifest["Assemblies"] = None
		self.manifest["Blocks"] = None
		self.manifest["Entities"] = None
		self.manifest["Triggers"] = None
		self.manifest["Events"] = None
		self.manifest["Keys"] = None
		self.manifest["Resources"] = None
		self.manifest["ID"] = "" # TODO: Generate a proper ID

	'''
	Getters and setters
	'''
	def getName(self):
		if not (self.loaded or self.virtual):
			raise RuntimeException("No mod has been created or loaded yet.")

		return self.manifest["Name"]

	def setName(self, name):
		if self.loaded:
			raise RuntimeException("Can't set the value of a mod contained on disk that isn't a clone")
		elif not self.virtual:
			raise RuntimeException("No mod has been created yet.")
		
		self.manifest["Name"] = name