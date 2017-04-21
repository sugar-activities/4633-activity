#!/usr/bin/env python
try:
	from sugar.activity import bundlebuilder
	bundlebuilder.start("LucasActivity")
except ImportError:
	import os
	os.system("find ./ | sed 's,^./,gtktest.activity/,g' > MANIFEST")
	os.system('rm gtktest.xo')
	os.chdir('..')
	os.system('zip -r gtktest.xo gtktest.activity')
	os.system('mv gtktest.xo ./gtktest.activity')
	os.chdir('gtktest.activity')
