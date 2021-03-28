#By Francis Ali.
'''Please do note that some commented out code here in this program is left there in case any changes need to be made. Also, please do feel free to contribute'''

from kivy.graphics import *
#from kivy.event import EventDispatcher
from kivy.properties import *

#from kivy.clock import Clock

GLOW_LINE_SHADER = '''
$HEADER$

/*uniform float brightness;
uniform vec4 points;
*/
uniform vec2 resolution;
uniform vec2 startPos;
uniform vec2 endPos;
uniform float brightnessFactor;
uniform float th;
uniform vec4 color;

void main(){
	/*variables for the main shader stuff*/
	vec2 center = (startPos+endPos)/2.0;
	float alpha = -atan((startPos - center).y/(startPos - center).x);
	float l = distance(startPos, endPos);
	float factor = brightnessFactor;
	/**/
	float x = gl_FragCoord.x;
	float y = gl_FragCoord.y;
	
	float dx = x - center.x; float dy = y - center.y;
	l+=factor;
	for(float i =th+factor; i>= th; i -= 1.){
		float c = i;
		float b = 0.;//height/2.0 - c;
		float a = (l-1.)/2.0 - c/1.7;
		float leftOp = pow(max(abs(dx*cos(alpha) - dy*sin(alpha)) - a/1.1, 0.), 2.);
		float rightOp = pow(max(abs(dx*sin(alpha)+dy*cos(alpha)) - b, 0.), 2.4);
		if (leftOp + rightOp <= c*c){
			vec3 fr = (color*texture2D(texture0, tex_coord0)).rgb;
			gl_FragColor = vec4(
				fr,
				1.0 -(i-th)/factor);
		}
	}
}
'''


class GlowingLine(Canvas):
	def __init__(self, glowBrightness=30, width=2, **kws):
		#:keyword argument width is the main width(thickness) of the line.
		#:keyword argument is the brightness factor of the glow. Adjust to suit your needs
		super().__init__(**kws)
		
		self.glowBrightness = glowBrightness
		self.mode = kws.get("mode", "rgba")
		##:keyword argument 'mode' here is supplied to the Color instruction which is applied to the glowing line.
		#for instance, Color(..., mode="rgba")
		with self:
			self.rc = RenderContext(use_parent_projection=True, use_parent_modelview = True)
			self.rc.shader.fs = GLOW_LINE_SHADER
		with self.rc:
			self.color = kws.get('color',  [1,1,0,1])
			self.color_inst = Color(*self.color, mode=self.mode)
			self._points = kws.get('points', [0,0, 100,100])
			self._points = list(map(float,self._points[:4]))
			self.rect = Rectangle(size=[1000,1000])
		Color(*self.color, mode=self.mode)
		line = Line(points = self._points, width=width)
		self.line = line
		self.update_glsl()
		
	@property
	def points(self):
		return self.line.points
	@points.setter
	def points(self, val):
		self.line.points = list(map(float,self.points[:4]))
		self.update_glsl()
		
	def update_glsl(self):
		self.rc['resolution'] = self.rect.size
		self.rc['startPos'] = self.points[:2]
		self.rc['endPos'] = self.points[2:]
		self.rc['brightnessFactor'] = float(self.glowBrightness)
		self.rc['th'] = float(self.line.width)
		self.rc['color'] = list(map(float,self.color))
		
if __name__ == '__main__':
	from kivy.base import runTouchApp
	from kivy.uix.widget import Widget
	wid = Widget()
	with wid.canvas:
		GlowingLine(glowBrightness=75,points=[300,560, 200, 400], color=[1., 1, 0], mode="rgb", width=10);
	
	runTouchApp(wid)
