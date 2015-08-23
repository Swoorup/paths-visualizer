from struct import unpack
from io import BytesIO

class SAPath():
	def __init__(self, node):
		self.path = BytesIO(open(node, "rb").read())
		self.header = {}
		self.pathnodes = []
		self.navinodes = []
		self.links = []
		self.navilinks = []
		self.linklengths = []
		self._offset = 20
		
		# headers
		self.header['nodes']	 = unpack('I', self.path.read(4))[0]
		self.header['vehnodes']	 = unpack('I', self.path.read(4))[0]
		self.header['pednodes']	 = unpack('I', self.path.read(4))[0]
		self.header['navinodes'] = unpack('I', self.path.read(4))[0]
		self.header['links']	 = unpack('I', self.path.read(4))[0]
			
	def Headers(self):
		return self.header
	
	def Paths(self):
		if len(self.pathnodes) != self.header['nodes']:
			self.path.seek(self._offset, 0)
			for i in range(self.header['nodes']):
				self.pathnodes.append({})
				self.pathnodes[i]['mem']	 = unpack('I', self.path.read(4))[0]
				self.pathnodes[i]['zero']	 = unpack('I', self.path.read(4))[0]
				self.pathnodes[i]['x']		 = float(unpack('h', self.path.read(2))[0]) / 8
				self.pathnodes[i]['y']		 = float(unpack('h', self.path.read(2))[0]) / 8
				self.pathnodes[i]['z']		 = float(unpack('h', self.path.read(2))[0]) / 8
				self.pathnodes[i]['heuristic'] = unpack('h', self.path.read(2))[0]
				self.pathnodes[i]['baseLink']	 = unpack('h', self.path.read(2))[0]
				self.pathnodes[i]['area']	 = unpack('h', self.path.read(2))[0]
				self.pathnodes[i]['node']	 = unpack('h', self.path.read(2))[0]
				self.pathnodes[i]['width']	 = unpack('b', self.path.read(1))[0] / 8
				self.pathnodes[i]['type']	 = unpack('b', self.path.read(1))[0]
				self.pathnodes[i]['flags']	 = unpack('I', self.path.read(4))[0]
		return self.pathnodes
			
	def NaviNodes(self):
		if len(self.navinodes) != self.header['navinodes']:
			self.path.seek(self._offset + (self.header['nodes'] * 28), 0)
			for i in range(self.header['navinodes']):
				self.navinodes.append({})
				self.navinodes[i]['x']		= float(unpack('h', self.path.read(2))[0]) / 8
				self.navinodes[i]['y']		= float(unpack('h', self.path.read(2))[0]) / 8
				self.navinodes[i]['area']	= unpack('h', self.path.read(2))[0]
				self.navinodes[i]['node']	= unpack('h', self.path.read(2))[0]
				self.navinodes[i]['disx']	= float(unpack('b', self.path.read(1))[0]) / 8
				self.navinodes[i]['disy']	= float(unpack('b', self.path.read(1))[0]) / 8
				self.navinodes[i]['flags']	= unpack('I', self.path.read(4))[0]
		return self.navinodes
		
	def Links(self):
		if len(self.links) != self.header['links']:
			self.path.seek(self._offset + (self.header['nodes'] * 28) + (self.header['navinodes'] * 14), 0)
			for i in range(self.header['links']):
				self.links.append({})
				self.links[i]['area']	= unpack('h', self.path.read(2))[0]
				self.links[i]['node']	= unpack('h', self.path.read(2))[0]
		return self.links
		
	def NaviLinks(self):
		if len(self.navilinks) != self.header['links']:
			self.path.seek(self._offset + (self.header['nodes'] * 28) + (self.header['navinodes'] * 14) + (self.header['links'] * 4) + 768, 0)
			for i in range(self.header['links']):
				self.navilinks.append(unpack('h', self.path.read(2))[0])
		return self.navilinks
	
	def LinkLengths(self):
		if len(self.linklengths) != self.header['links']:
			self.path.seek(self._offset + (self.header['nodes'] * 28) + (self.header['navinodes'] * 14) + (self.header['links'] * 4) + 768 + (self.header['links'] * 2), 0)
			for	i in range(self.header['links']):
				self.linklengths.append(unpack('b', self.path.read(1))[0])
		return self.linklengths
		
	def Close(self):
		 self.path.close()