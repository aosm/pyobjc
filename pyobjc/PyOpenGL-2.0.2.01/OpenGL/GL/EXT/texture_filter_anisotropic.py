import string
__version__ = string.split('$Revision: 1.8 $')[1]
__date__ = string.join(string.split('$Date: 2001/11/16 17:45:22 $')[1:3], ' ')
__author__ = 'Tarn Weisner Burton <twburton@users.sourceforge.net>'
__doc__ = 'http://oss.sgi.com/projects/ogl-sample/registry/EXT/texture_filter_anisotropic.txt'
__api_version__ = 0x100


GL_TEXTURE_MAX_ANISOTROPY_EXT = 0x84fe

GL_MAX_TEXTURE_MAX_ANISOTROPY_EXT = 0x84ff

def glInitTextureFilterAnisotropicEXT():
	from OpenGL.GL import __has_extension
	return __has_extension("GL_EXT_texture_filter_anisotropic")

glInitTexFilterAnisotropicEXT = glInitTextureFilterAnisotropicEXT

def __info():
	if glInitTextureFilterAnisotropicEXT():
		return [('MAX_TEXTURE_MAX_ANISOTROPY_EXT', MAX_TEXTURE_MAX_ANISOTROPY_EXT, 'i')]
