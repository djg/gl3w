#!/usr/bin/env python
import re
import os
import urllib2

# Create directories
if not os.path.exists('include/GLES3'):
    os.makedirs('include/GLES3')

# Download glcorearb.h
if not os.path.exists('include/GLES3/gl3.h'):
    print 'Downloading GL|ES 3 gl3.h to include/GLES3...'
    web = urllib2.urlopen('https://www.khronos.org/registry/gles/api/GLES3/gl3.h')
    with open('include/GLES3/gl3.h', 'wb') as f:
        f.writelines(web.readlines())
else:
    print 'Reusing gl3.h from include/GLES3...'

# Parse function names from glcorearb.h
print 'Parsing gl3.h header...'
procs = []
p = re.compile(r'GL_APICALL\s+(.*)GL_APIENTRY\s+(\w+)\s+(.*);')
with open('include/GLES3/gl3.h', 'r') as f:
    for line in f:
        m = p.match(line)
        if m:
            a = m.group(1), m.group(2), m.group(3)
            procs.append(a)

def proc_t(proc):
    return { 'p': proc[1],
             'p_a': proc[2],
             'p_r': proc[0],
             'p_s': 'gles3w' + proc[1][2:],
             'p_t': 'PFN' + proc[1].upper() + 'PROC' }

# Generate gl3w.h
print 'Generating gles3w.h in include/GLES3...'
with open('include/GLES3/gles3w.h', 'wb') as f:
    f.write(r'''#ifndef __gles3w_h_
#define __gles3w_h_

#include <GLES3/gl3.h>

#ifdef __cplusplus
extern "C" {
#endif

/* OpenGL|ES functions */
''')
    for proc in procs:
        pt = proc_t(proc);
        f.write('typedef %(p_r)s(GL_APIENTRY* %(p_t)s) %(p_a)s;\n' % pt)
        f.write('extern %(p_t)s %(p_s)s;\n' % pt)
    f.write('\n')
    for proc in procs:
        f.write('#define %(p)-40s %(p_s)s\n' % proc_t(proc))
    f.write(r'''
#ifdef GLES3W_IMPLEMENTATION

''')
    for proc in procs:
        f.write('%(p_t)-44s %(p_s)s;\n' % proc_t(proc))
    f.write(r'''
static void
gles3wInit()
{
''')
    for proc in procs:
        f.write('    %(p_s)-41s = (%(p_t)s) GLES3W_IMPLEMENTATION("%(p)s");\n' % proc_t(proc))
    f.write(r'''}

#endif // GLES3W_IMPLEMENTATION

#ifdef __cplusplus
}
#endif

#endif
''')
