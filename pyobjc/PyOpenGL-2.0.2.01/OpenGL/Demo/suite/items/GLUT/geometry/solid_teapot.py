from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import items
import items.GLUT.geometry


class item(items.GLUT.geometry.solid_item):

	def on_display(self):
		items.GLUT.geometry.solid_item.on_display(self)
		glutSolidTeapot(0.5)
		