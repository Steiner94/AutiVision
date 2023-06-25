import datetime
import os

from fpdf import FPDF


class PDF_file_creator:
    def __init__(self, filename):
        self.filename = filename
        self.pdf = FPDF()

    def add_page(self):
        self.pdf.add_page()

    def set_font(self, family, style='', size=12):
        self.pdf.set_font(family, style, size)

    def add_text(self, x, y, text):
        old_x = self.pdf.get_x()
        old_y = self.pdf.get_y()
        self.pdf.set_xy(x, y)
        self.pdf.multi_cell(0, 10, text)
        self.pdf.set_xy(old_x, old_y)

    def add_image(self, path, x, y, w=None, h=None):
        self.pdf.image(path, x, y, w, h)

    def add_images_with_text(self, image_paths, text_list):
        print("Adding text and images to pdf file..")
        for i, path in enumerate(image_paths):
            self.add_page()
            self.add_image(path, 16, 20, 177, 130)
            text = text_list[i] if i < len(text_list) else ''
            self.set_font('Times', '', 12)
            formatted_text = self.format_text(text)
            self.add_text(16, 160, formatted_text)

    def format_text(self, text):
        lines = text.split('\n')
        formatted_lines = []
        for i in range(0, len(lines), 2):
            line = lines[i]
            next_line = lines[i + 1] if i + 1 < len(lines) else ''
            formatted_line = f'{line}     {next_line}'  # Five spaces between two lines
            formatted_lines.append(formatted_line)
        return '\n'.join(formatted_lines)

    def add_first_page(self, headline, user, path, text):
        self.add_page()
        self.set_font('Times', 'B', 40)
        self.add_text(20, 40, headline)
        self.set_font('Times', '', 15)
        self.add_text(20, self.pdf.get_y() + 50, f"Name: {user.name}")
        self.add_text(20, self.pdf.get_y() + 60, f"Age: {user.age}")
        self.add_text(20, self.pdf.get_y() + 70, f"Gender: {user.gender}")
        current_date = datetime.datetime.now().strftime("%d/%m/%y")
        self.add_text(20, self.pdf.get_y() + 80, f"Date: {current_date}")
        self.add_text(20, self.pdf.get_y() + 10, "")
        self.add_image(path + r'\1.jpg', 16, 145, 177, 100)
        self.set_font('Times', '', 12)
        self.add_text(16, 251, text)

    def add_last_page(self, text_list):
        self.set_font('Times', '', 15)
        for i in range(len(text_list)):
            self.add_text(16, 220 + i * 10, text_list[i])

    def save(self, path):
        print("Saving pdf file..")
        self.pdf.output(path + '\\' + self.filename, 'F')
