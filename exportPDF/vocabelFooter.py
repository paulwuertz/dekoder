import json
from fpdf import FPDF
from fpdf.html import HTML2FPDF

class HTMLMixinU8(object):
    def write_html(self, text, image_map=None):
        "Parse HTML and convert it to PDF"
        h2p = HTML2FPDF(self, image_map)
        h2p.set_font('DejaVu', 10)
        text = h2p.unescape(text) # To deal with HTML entities
        h2p.feed(text)

title = 'Кино Lieder'

class PDF(FPDF, HTMLMixinU8):
    def __init__(self,file):
        self.file=file
        FPDF.__init__(self)
        HTMLMixinU8.__init__(self)
    def header(self):
        # Arial bold 15
        # Calculate width of title and position
        w = self.get_string_width(len(title)*"A") + 6
        self.set_x((210 - w) / 2)
        # Colors of frame, background and text
        self.set_draw_color(255, 255, 255)
        self.set_fill_color(255, 255, 255)
        self.set_text_color(0, 0, 0)
        # Thickness of frame (1 mm)
        self.set_line_width(1)
        # Title
        self.cell(w, 9, title, 1, 1, 'C', 1)
        # Line break
        self.ln(10)

    def footer(self):
        self.set_y(-45)
        # Read text file
        with open(self.file, 'r') as fh:
            txt = fh.read()
        pars = json.loads(txt)
        text = "\n\n".join([" ".join([w for w in par]) for par in pars])
        # Page number
        words=sorted(set([w.strip(",. ?!-_") for par in pars for w in par if w.strip(",. ?!-_")!=""]))
        vocabulary = ", ".join(["<b>%s</b>: ubersetzung" % w for w in words])
        print(vocabulary)
        self.write_html(vocabulary)
        #self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

    def chapter_title(self, num, label):
        # Arial 12
        # Background color
        self.set_fill_color(200, 220, 255)
        # Title
        self.cell(0, 6, 'Text %d : %s' % (num, label), 0, 1, 'L', 1)
        # Line break
        self.ln(4)

    def chapter_body(self, name):
        # Read text file
        with open(name, 'r') as fh:
            txt = fh.read()
        pars = json.loads(txt)
        text = "\n\n".join([" ".join([w for w in par]) for par in pars])

        # Output justified text
        self.multi_cell(0, 5, text)
        # Line break
        self.ln()
        # Mention in italics
        self.cell(0, 5, 'Made with dekoder')

    def print_chapter(self, num, title, name):
        self.add_page()
        self.chapter_title(num, title)
        self.chapter_body(name)

pdf = PDF("tests/wesna_ru.txt")
pdf.add_font('DejaVu', '', 'DejaVuSansMono.ttf', uni=True)
pdf.add_font('DejaVu', 'B', 'DejaVuSansMono-Bold.ttf', uni=True)
pdf.set_font('DejaVu', '', 14)
pdf.set_author('Jules Verne')
pdf.print_chapter(1, 'Кино - Весна', 'tests/wesna_ru.txt')
pdf.output('tuto3.pdf', 'F')