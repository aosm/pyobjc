import string
__version__ = string.split('$Revision: 1.8 $')[1]
__date__ = string.join(string.split('$Date: 2001/11/17 14:12:34 $')[1:3], ' ')
__author__ = 'Tarn Weisner Burton <twburton@users.sourceforge.net>'
__doc__ = 'http://oss.sgi.com/projects/ogl-sample/registry/SGIS/texture_lod.txt'
__api_version__ = 0x108

GL_TEXTURE_MIN_LOD_SGIS = 0x813A
GL_TEXTURE_MAX_LOD_SGIS = 0x813B
GL_TEXTURE_BASE_LEVEL_SGIS = 0x813C
GL_TEXTURE_MAX_LEVEL_SGIS = 0x813D

def glInitTextureLodEXT():
	from OpenGL.GL import __has_extension
	return __has_extension("GL_EXT_texture_lod")

glInitTexLodEXT = glInitTextureLodEXT

def __info():
	if glInitTextureLodEXT():
		return []
