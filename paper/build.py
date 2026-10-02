"""Build the LaTeX source and PDF of the paper from paper.md (Markdown is the master copy).
Requires pandoc and tectonic on PATH or in ~/tools. Run: python paper/build.py"""
import os, re, subprocess, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.expanduser(r'~\tools')
PANDOC = shutil.which('pandoc') or os.path.join(TOOLS, 'pandoc-3.12', 'pandoc.exe')
TECTONIC = shutil.which('tectonic') or os.path.join(TOOLS, 'tectonic.exe')

src = open(os.path.join(HERE, 'paper.md'), encoding='utf-8').read()
# split the title block off; pandoc renders it from metadata
lines = src.split('\n')
title = lines[0].lstrip('# ').strip()
body = src[src.index('## Abstract'):]
body = body.replace('](../figures/', '](figures/')  # figures are copied next to the build
# pandoc needs a blank line before a list that follows a paragraph (GitHub does not)
item = re.compile(r'^\s*(?:[-*]|\d+\.)\s')
out = []
for ln in body.split('\n'):
    if item.match(ln) and out and out[-1].strip() and not item.match(out[-1]) and not out[-1].startswith(' ') \
            and not out[-1].lstrip().startswith('|'):
        out.append('')
    out.append(ln)
body = '\n'.join(out)
meta = f'''---
title: "{title}"
author: "Eight Rice (contact@autonet.computer, ORCID 0009-0008-2902-0845)"
date: "October 2026"
geometry: margin=2.5cm
fontsize: 10pt
colorlinks: true
linkcolor: blue
urlcolor: blue
header-includes:
  - \\usepackage{{float}}
  - \\floatplacement{{figure}}{{H}}
  - \\usepackage{{caption}}
  - \\captionsetup{{font=small}}
  - \\renewcommand{{\\arraystretch}}{{1.15}}
---

*Code, data and results: <https://github.com/autonet-code/leverage-sims>. All numbers in this paper are reproducible from the code with the seeds given in Appendix D.*

'''
build = os.path.join(HERE, 'build')
os.makedirs(build, exist_ok=True)
figs_src = os.path.join(os.path.dirname(HERE), 'figures')
if os.path.exists(os.path.join(build, 'figures')):
    shutil.rmtree(os.path.join(build, 'figures'))
shutil.copytree(figs_src, os.path.join(build, 'figures'))
md = os.path.join(build, 'leverage_sims.md')
open(md, 'w', encoding='utf-8').write(meta + body)
tex = os.path.join(HERE, 'leverage_sims.tex')
common = ['--from', 'markdown+pipe_tables+tex_math_dollars', '--standalone', '--number-sections=false',
          '--columns=100', '-V', 'documentclass=article']
subprocess.run([PANDOC, md, *common, '-o', tex], check=True, cwd=build)
subprocess.run([PANDOC, md, *common, '--pdf-engine', TECTONIC, '-o', os.path.join(HERE, 'leverage_sims.pdf')],
               check=True, cwd=build)
print('wrote', tex, 'and leverage_sims.pdf')
