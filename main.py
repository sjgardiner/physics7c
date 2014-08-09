#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
################################## Begin problem generation code
from math import pi, floor
import re
import random

with open("problem_template.tex") as tex_file:
    template_text = tex_file.read() 

# Function that generates random "nice" decimals or integers. Numbers without a fractional
# part are made somewhat more likely because 0 appears twice in the list passed to random.choice
def random_nice_number(int_min,int_max):
  nice_number = random.randint(int_min,int_max) + random.choice([0,0.5,0]) 
  return nice_number

# Function that compares an angle in radians to another. Angles are considered equivalent
# by this function if they correspond to the same point on the unit circle (i.e., pi/2 and
# 5*pi/2 are considered equal). Returns True if the angles are very close (within 0.000001)
# and False otherwise.
def unit_circle_compare(angle1, angle2):
  new_angle1 = angle1 - 2*pi*floor(angle1 / (2*pi)) # Converts angle1 to an angle on the unit circle (between 0 and 2*pi)
                                                    # Note that this works for negative angles as well because floor
                                                    # can return a negative integer.
  new_angle2 = angle2 - 2*pi*floor(angle2 / (2*pi)) # Converts angle2 to an angle on the unit circle (between 0 and 2*pi)
  return (abs(new_angle1 - new_angle2) < 0.000001)
################################## End problem generation code

class MainHandler(webapp2.RequestHandler):
    def get(self):
	self.response.headers['Content-Type'] = 'text/plain'
        ################################## Begin problem generation code
	# Randomly choose wave parameters
	possible_phases = {"" : 0, "+\\frac{\\pi}{4}" : pi/4,
	 "+\\frac{\\pi}{2}" : pi/2, "+\\frac{3\\pi}{4}" : 3*pi/4,
	 "+\\pi" : pi, "+\\frac{5\\pi}{4}" : 5*pi/4,
	 "+\\frac{3\\pi}{2}" : 3*pi/2, "+\\frac{7\\pi}{4}" : 7*pi/4}

	phase_constant_text = random.choice(possible_phases.keys())
	phase_constant_number = possible_phases[phase_constant_text]

	wavelength = random.randint(1,5) #random_nice_number(1,5)
	period = random.randint(1,5) #random_nice_number(1,5)
	amplitude = random.randint(1,5) #random_nice_number(1,5)

	possible_directions = {"left" : 1, "right" : -1}
	possible_signs = {"left" : "+", "right" : "-"}

	wave_direction_text = random.choice(["left", "right"])
	wave_direction_number = possible_directions[wave_direction_text]
	wave_direction_sign = possible_signs[wave_direction_text]

	wave_equation_tex  = ("y(x,t) = (%g\\text{ cm})\\sin\\bigg(\\frac{2\\pi t}{%g\\text{ s}} " % (amplitude, period))
	wave_equation_tex += (wave_direction_sign + ("""\\frac{2\\pi x}{%g\\text{ m}}""" % wavelength))
	wave_equation_tex += (phase_constant_text + "\\bigg)")

	# Randomly choose graph parameters
	number_of_periods_shown = random.randint(2,4) #random_nice_number(2,4)
	number_of_wavelengths_shown = random.randint(2,4) #random_nice_number(2,4)

	tmax = number_of_periods_shown*period
	xmax = number_of_wavelengths_shown*wavelength 

	t0 = random.randrange(0,(floor(number_of_periods_shown)*4)-2)*period/4.0
	x0 = random.randrange(0,(floor(number_of_wavelengths_shown)*4)-2)*wavelength/4.0
	# Make sure that the point at x = x0, t = t0 is not a maximum or minimum (if so,
	# the direction that the wave is moving may be indeterminate). If this is the case,
	# nudge x0 over a fourth of a wavelength to fix the problem.
	total_phase_x0t0 = phase_constant_number + 2*pi*t0/period + wave_direction_number*2*pi*x0/wavelength
	if (unit_circle_compare(total_phase_x0t0,pi/2) or unit_circle_compare(total_phase_x0t0,3*pi/2)):
	  x0 += wavelength/4.0

	t1 = t0 + period/8.0
	x1 = x0 + wavelength/8.0

	# Dictionary of replacements to perform on the TeX file template
	rep = {"##t0##": str(t0),
	       "##x0##": str(x0),
	       "##t1##": str(t1),
	       "##x1##": str(x1),
	       "##xmax##" : str(xmax),
	       "##tmax##" : str(tmax),
	       "##xmax+0.5##" : str(xmax + 0.5),
	       "##tmax+0.5##" : str(tmax + 0.5),
	       "##amplitude##" : str(amplitude),
	       "##period##" : str(period),
	       "##wavelength##" : str(wavelength),
	       "##phase##" : str(phase_constant_number),
	       "##spatial_term_sign##" : wave_direction_sign,
	       "##wave_equation##" : wave_equation_tex }

	# Perform the replacement in one pass using regular expressions
	rep = dict((re.escape(k), v) for k, v in rep.iteritems())
	pattern = re.compile("|".join(rep.keys()))
	text = pattern.sub(lambda m: rep[re.escape(m.group(0))], template_text)

	# Write the finished problem TeX code to a new file
	#with open("problem.tex", "w") as problem_file:
	#  problem_file.write(text)
	################################## End problem generation code

        self.response.write(text)

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
