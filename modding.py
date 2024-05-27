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

# Generic mod resource
class Resource:
	def __init__(self, fileType, filePath, resourceName):
		self.type = fileType
		self.path = filePath
		self.name = resourceName

# A mod, either on disk or created completely from scratch
class BesiegeMod:
	def __init__(self):
		# State
		self.loaded = False			# Wether or not we've loaded a mod from disk yet
		self.virtual = False		# Wether or not we're creating a mod from scratch

		# File data
		self.manifest = {}			# Mod.xml content
		self.assemblyPaths = []
		self.blockManifests = []
		self.entityManifests = []
		self.resources = {}

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

		# Process manifest data
		assemblies = self.manifest["Assemblies"]
		if assemblies != None:
			assemblies = assemblies.values()
			for assembly in assemblies:
				assemblyPath = assembly["@path"]
				self.assemblyPaths.append(assemblyPath)

		blocks = self.manifest["Blocks"]
		if blocks != None:
			blocks = blocks.values()
			for block in blocks: 
				blockManifest = self.readObjectManifest(block)
				self.blockManifests.append(blockManifest, path)

		entities = self.manifest["Entities"]
		if entities != None:
			entities = entities.values()
			for entity in entities:
				entityManifest = self.readObjectManifest(entity, path)
				self.entityManifests.append(entityManifest)

		resources = self.manifest["Resources"]
		if resources != None:
			for resourceType in resources:
				resource = resources[resourceType]
				self.readResource(resource, resourceType)

	'''
	Helper functions
	'''

	def readResource(self, resource, resourceType):
		# If there are multipe resources of the same type we need to deal with each one separately
		if type(resource) == list:
			for resourceItem in resource:
				resourceName = resourceItem["@name"]
				resourcePath = resourceItem["@path"]
				resourceObj = Resource(resourceType, resourcePath, resourceName)
				self.resources[resourceName] = resourceObj
		else:
			resourceName = resource["@name"]
			resourcePath = resource["@path"]
			resourceObj = Resource(resourceType, resourcePath, resourceName)
			self.resources[resourceName] = resourceObj

	# Entities + Blocks 
	def readObjectManifest(self, obj, basePath):
		objectPath = obj["@path"]
		with open(f"{basePath}/{objectPath}") as objectFile:
			objectManifestSrc = objectFile.read()
			objectManifest = xmltodict.parse(objectManifestSrc)
			return objectManifest

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

	def getAuthor(self):
		if not (self.loaded or self.virtual):
			raise RuntimeException("No mod has been created or loaded yet.")

		return self.manifest["Author"]

	def setAuthor(self, author):
		if self.loaded:
			raise RuntimeException("Can't set the value of a mod contained on disk that isn't a clone")
		elif not self.virtual:
			raise RuntimeException("No mod has been created yet.")

		self.manifest["Author"] = author

	def getVersion(self):
		if not (self.loaded or self.virtual):
			raise RuntimeException("No mod has been created or loaded yet.")

		return self.manifest["Version"]

	def setVersion(self, version):
		if self.loaded:
			raise RuntimeException("Can't set the value of a mod contained on disk that isn't a clone")
		elif not self.virtual:
			raise RuntimeException("No mod has been created yet.")

		self.manifest["Version"] = version

	def getDescription(self):
		if not (self.loaded or self.virtual):
			raise RuntimeException("No mod has been created or loaded yet.")

		return self.manifest["Description"]

	def setDescription(self, description):
		if self.loaded:
			raise RuntimeException("Can't set the value of a mod contained on disk that isn't a clone")
		elif not self.virtual:
			raise RuntimeException("No mod has been created yet.")

		self.manifest["Description"] = description

	def isDebug(self):
		if not (self.loaded or self.virtual):
			raise RuntimeException("No mod has been created or loaded yet.")

		return self.manifest["Debug"]

	def setDebug(self, debug):
		if self.loaded:
			raise RuntimeException("Can't set the value of a mod contained on disk that isn't a clone")
		elif not self.virtual:
			raise RuntimeException("No mod has been created yet.")

		self.manifest["Debug"] = debug

	def isMultiplayerCompatible(self):
		if not (self.loaded or self.virtual):
			raise RuntimeException("No mod has been created or loaded yet.")

		return self.manifest["MultiplayerCompatible"]

	def setMultiplayerCompatible(self, multiplayerCompatible):
		if self.loaded:
			raise RuntimeException("Can't set the value of a mod contained on disk that isn't a clone")
		elif not self.virtual:
			raise RuntimeException("No mod has been created yet.")

		self.manifest["MultiplayerCompatible"] = multiplayerCompatible

	def getAssemblies(self):
		if not (self.loaded or self.virtual):
			raise RuntimeException("No mod has been created or loaded yet.")

		return self.assemblyPaths

	def addAssembly(self, assembly):
		if self.loaded:
			raise RuntimeException("Can't set the value of a mod contained on disk that isn't a clone")
		elif not self.virtual:
			raise RuntimeException("No mod has been created yet.")

		self.manifest["Author"].append(assembly)

	def getBlocks(self):
		if not (self.loaded or self.virtual):
			raise RuntimeException("No mod has been created or loaded yet.")

		return self.blocks

	def createBlock(self):
		if self.loaded:
			raise RuntimeException("Can't set the value of a mod contained on disk that isn't a clone")
		elif not self.virtual:
			raise RuntimeException("No mod has been created yet.")

	def getEntities(self):
		if not (self.loaded or self.virtual):
			raise RuntimeException("No mod has been created or loaded yet.")

		return self.entities

	def createEntity(self):
		if self.loaded:
			raise RuntimeException("Can't set the value of a mod contained on disk that isn't a clone")
		elif not self.virtual:
			raise RuntimeException("No mod has been created yet.")

	def getTriggers(self):
		if not (self.loaded or self.virtual):
			raise RuntimeException("No mod has been created or loaded yet.")

	def getEvents(self):
		if not (self.loaded or self.virtual):
			raise RuntimeException("No mod has been created or loaded yet.")

	def getKeys(self):
		if not (self.loaded or self.virtual):
			raise RuntimeException("No mod has been created or loaded yet.")

	def getResources(self):
		if not (self.loaded or self.virtual):
			raise RuntimeException("No mod has been created or loaded yet.")

		return self.resources

	def getID(self):
		if not (self.loaded or self.virtual):
			raise RuntimeException("No mod has been created or loaded yet.")

		return self.manifest["ID"]

	#XXX: 	Only use this if you know what you're doing
	#		this can break compatibility with content made
	#		using old versions of your mod if changed
	def setID(self, ID):
		if self.loaded:
			raise RuntimeException("Can't set the value of a mod contained on disk that isn't a clone")
		elif not self.virtual:
			raise RuntimeException("No mod has been created yet.")

		self.manifest["ID"] = ID