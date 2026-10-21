"""Generate a styled A4 PDF from the SAME _data/cv.yml used by Jekyll.
Requires: pip install PyYAML; pandoc; XeLaTeX (MiKTeX on Windows).
Run from anywhere: python build_cv.py
"""
from pathlib import Path
import subprocess
import yaml

ROOT = Path(__file__).resolve().parent
DATA = ROOT / '_data' / 'cv.yml'
MARKDOWN = ROOT / 'cv.md'
HEADER = ROOT / 'cv-style.tex'
PDF = ROOT / 'VasilikiPetraki.pdf'

# Escape plain content inserted into raw LaTeX fragments.
def tex(value):
    value = str(value or '')
    replacements = {
        '\\': r'\textbackslash{}', '&': r'\&', '%': r'\%', '$': r'\$',
        '#': r'\#', '_': r'\_', '{': r'\{', '}': r'\}',
        '~': r'\textasciitilde{}', '^': r'\textasciicircum{}',
    }
    return ''.join(replacements.get(c, c) for c in value)


def heading(title):
    return r'\section*{\textcolor{cvblue}{' + tex(title) + r'}}'


with DATA.open(encoding='utf-8') as f:
    cv = yaml.safe_load(f)

person = cv['personal']

HEADER.write_text(r'''
\usepackage{xcolor}
\usepackage{graphicx}
\usepackage{hyperref}
\definecolor{cvblue}{HTML}{005A8D}
\definecolor{cvgray}{HTML}{555555}
\hypersetup{colorlinks=true,urlcolor=cvblue}
\setlength{\parindent}{0pt}
\setlength{\parskip}{3pt}
\setlength{\emergencystretch}{2em}
\pagestyle{empty}
'''.strip() + '\n', encoding='utf-8')

lines = [
    r'\begin{center}',
    r'{\LARGE\bfseries ' + tex(person.get('name')) + r' -- Βιογραφικό}',
    r'\end{center}',
    r'\vspace{-3mm}',
    r'{\color{cvblue}\rule{\linewidth}{1.2pt}}',
    '',
]

photo_name = person.get('photo', '')
photo = ROOT / photo_name
if photo_name and photo.is_file():
    # Local photo is optional; use forward slashes for XeLaTeX on Windows.
    lines += [
        r'\noindent\begin{minipage}[t]{0.24\linewidth}',
        r'\vspace{0pt}\fcolorbox{cvblue}{white}{\includegraphics[width=0.90\linewidth,height=34mm,keepaspectratio]{' + tex(photo.as_posix()) + r'}}',
        r'\end{minipage}\hfill\begin{minipage}[t]{0.73\linewidth}',
    ]
else:
    lines += [r'\noindent\begin{minipage}[t]{\linewidth}']

lines += [
    r'\vspace{0pt}\textbf{' + tex(person.get('title')) + r'}',
    '',
    tex(cv.get('profile', '')) + r'\par',
    '',
]
if person.get('linkedin'):
    # Full URL is stored once in YAML and remains clickable.
    lines.append(r'\textcolor{cvgray}{LinkedIn:} \url{' + person['linkedin'].replace('%', r'\%') + r'}\par')
lines += [r'\end{minipage}', r'\vspace{3mm}', '', heading('Εμπειρία'), '']

for job in cv.get('experience', []):
    title = tex(job.get('position'))
    org = tex(job.get('organization'))
    lines += [r'\textbf{' + title + r' -- ' + org + r'}\\']
    secondary = ' · '.join(filter(None, [job.get('employment_type'), job.get('period')]))
    lines.append(r'{\small\textcolor{cvgray}{' + tex(secondary) + r'}}\\')
    place = ' · '.join(filter(None, [job.get('location'), job.get('department')]))
    if place:
        lines.append(r'{\small ' + tex(place) + r'}\\')
    if job.get('description'):
        lines.append(tex(job['description']) + r'\par')
    lines.extend([r'\vspace{2.5mm}', ''])

lines.extend([heading('Εκπαίδευση'), ''])
for edu in cv.get('education', []):
    lines.append(r'\textbf{' + tex(edu.get('institution')) + r'}\\')
    lines.append(tex(edu.get('degree')) + ' · ' + tex(edu.get('period')) + r'\par')
    lines.extend([r'\vspace{1.5mm}', ''])

lines.extend([heading('Δεξιότητες'), ''])
# Blue labels similar to HTML .skills span.
for skill in cv.get('skills', []):
    lines.append(r'\colorbox{cvblue}{\textcolor{white}{\strut\footnotesize\ ' + tex(skill) + r'\ }}\hspace{1mm}')
lines.extend(['', heading('Επικοινωνία'), ''])
if person.get('email'):
    lines.append(r'Email: \href{mailto:' + person['email'] + '}{' + tex(person['email']) + r'}\par')
if person.get('phone'):
    lines.append(r'Τηλ.: ' + tex(person['phone']) + r'\par')
MARKDOWN.write_text('```{=latex}\n' + '\n'.join(lines) + '\n```\n', encoding='utf-8')

subprocess.run([
    'pandoc', str(MARKDOWN), '-f', 'markdown+raw_tex', '-o', str(PDF),
    '--pdf-engine=xelatex', '--include-in-header', str(HEADER),
    '-V', 'geometry:a4paper,margin=1.65cm',
    '-V', 'mainfont=Arial', '-V', 'lang=el-GR',
    '-V', 'fontsize=10pt',
], cwd=ROOT, check=True)
print(f'PDF created: {PDF}')
