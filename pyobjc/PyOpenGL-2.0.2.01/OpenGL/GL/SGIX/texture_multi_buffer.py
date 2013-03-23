import string
__version__ = string.split('$Revision: 1.6 $')[1]
__date__ = string.join(string.split('$Date: 2001/08/10 18:42:33 $')[1:3], ' ')
__author__ = 'Tarn Weisner Burton <twburton@users.sourceforge.net>'
__doc__ = 'http://oss.sgi.com/projects/ogl-sample/registry/SGIX/texture_multi_buffer.txt'
__api_version__ = 0x102

GL_TEXTURE_MULTI_BUFFER_HINT_SGIX = 0x812E

def glInitTextureMultiBufferSGIX():
	from OpenGL.GL import __has_extension
	return __has_extension("GL_SGIX_texture_multi_buffer")

glInitTexMultiBufferSGIX = glInitTextureMultiBufferSGIX

def __info():
	if glInitTextureMultiBufferSGIX():
		return []
