# Kivy-Glowing-Line
Glowing line made with Kivy using GLSL

Simply run the file to see what it does, then you can play around with it.
It's quite easy to use. Just add it as a Canvas instruction to your widget's canvas as such

with widget.canvas:
  GlowingLine(...)

Unfortunately though, this, unlike your regular Line from kivy.graphics.Line, is just a Line segment with only two points
supported, the start and end points.
