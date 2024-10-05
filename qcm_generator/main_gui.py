import os
import platform
import re
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

from qcm_generator.main_cli import generate_subjects

QUESTION_FILE = os.path.join(os.path.dirname(__file__), 'questions.txt')


def load_style(editor: tk.Text) -> None:
    # Set default styles
    editor.tag_configure('default', foreground='black', background='white')
    editor.configure(bg='white', fg='black')

    # Set styles for specific use cases
    editor.tag_configure('math', foreground='blue')
    editor.tag_configure('invalid', foreground='red')
    editor.tag_configure('bold', font=('Monospace', 10, 'bold'))


def check_markdown(editor: tk.Text) -> None:
    start = '1.0'
    end = 'end'
    data = editor.get(start, end)

    # Clear existing tags
    editor.tag_remove('math', start, end)
    editor.tag_remove('bold', start, end)

    # Apply bold tag for lines starting with "Q"
    for line in data.splitlines():
        if line.startswith('Q'):
            line_start_index = editor.index(f'{data.splitlines().index(line)}.0')

            line_end_index = editor.index(f'{line_start_index} + {len(line) + 2}c')

            editor.tag_add('bold', line_start_index, line_end_index)

    # Regex patterns for math mode
    dollar_pattern = r'\$(.*?)\$'  # Matches $...$
    bracket_pattern = r'\\\[(.*?)\\\]'  # Matches \[...\]

    # Combine patterns to find all matches
    combined_pattern = f'({dollar_pattern}|{bracket_pattern})'

    for match in re.finditer(combined_pattern, data):
        start_index = editor.index(f'1.0 + {match.start()}c')
        end_index = editor.index(f'1.0 + {match.end()}c')
        editor.tag_add('math', start_index, end_index)

    # Check for invalid patterns: unmatched $ or \[
    invalid_dollar_pattern = r'\$[^$]*(?![^$]*\$)'  # Matches a $ without a closing $
    invalid_bracket_pattern = r'\\\[[^\\\]]*(?![^\\\]]*\\\])'  # Matches \[ without a closing \]

    # Find and tag invalid patterns
    for match in re.finditer(invalid_dollar_pattern, data):
        start_index = editor.index(f'1.0 + {match.start()}c')
        end_index = editor.index(f'1.0 + {match.end()}c')
        editor.tag_add('invalid', start_index, end_index)

    for match in re.finditer(invalid_bracket_pattern, data):
        start_index = editor.index(f'1.0 + {match.start()}c')
        end_index = editor.index(f'1.0 + {match.end()}c')
        editor.tag_add('invalid', start_index, end_index)

    # Remove invalid tags where math tags exist
    for match in re.finditer(combined_pattern, data):
        start_index = editor.index(f'1.0 + {match.start()}c')
        end_index = editor.index(f'1.0 + {match.end()}c')
        editor.tag_remove('invalid', start_index, end_index)


class QCMGeneratorIDE:
    def __init__(self, root: tk.Tk) -> None:
        self.root: tk.Tk = root
        self.root.title('QCM Generator IDE')

        self.root.minsize(700, 400)

        self.text_frame = tk.Frame(root)
        self.text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.text_area: scrolledtext.ScrolledText = scrolledtext.ScrolledText(
            self.text_frame,
            width=60,
            height=20,
            wrap=tk.WORD,
        )
        self.text_area.pack(fill=tk.BOTH, expand=True)

        self.button_frame = tk.Frame(root)
        self.button_frame.pack(side=tk.RIGHT, padx=5, pady=5)

        self.help_btn: tk.Button = tk.Button(self.button_frame, text='Help', command=self.show_help)
        self.help_btn.pack(pady=5)

        self.load_btn: tk.Button = tk.Button(
            self.button_frame,
            text='Load Questions',
            command=self.load_questions_from_file,
        )
        self.load_btn.pack(pady=5)

        self.save_btn: tk.Button = tk.Button(self.button_frame, text='Save Questions', command=self.save_questions)
        self.save_btn.pack(pady=5)

        self.reset_btn: tk.Button = tk.Button(self.button_frame, text='Reset Questions', command=self.reset_questions)
        self.reset_btn.pack(pady=5)

        self.include_image_btn: tk.Button = tk.Button(
            self.button_frame,
            text='Include Image',
            command=self.include_image,
        )
        self.include_image_btn.pack(pady=5)

        self.generate_subjects_btn: tk.Button = tk.Button(
            self.button_frame,
            text='Generate Subjects',
            command=self.generate_subjects,
        )
        self.generate_subjects_btn.pack(pady=5)

        self.open_subjects_folder_btn: tk.Button = tk.Button(
            self.button_frame,
            text='Open Subjects Folder',
            command=self.open_subjects_folder,
        )
        self.open_subjects_folder_btn.pack(pady=5)

        self.load_questions(
            QUESTION_FILE,
            is_user_triggered=False,
        )

        # Set up Pygments
        load_style(self.text_area)
        check_markdown(self.text_area)

        # Bind key release to the markdown checker function
        self.text_area.bind(
            '<KeyRelease>',
            lambda _: check_markdown(self.text_area),
        )

        # Define tags for syntax coloring
        self.text_area.tag_configure('maths', foreground='blue')
        self.text_area.tag_configure('question', font=('Helvetica', 10, 'bold'))

    def reset_questions(self) -> None:
        reload_questions()
        self.load_questions(QUESTION_FILE, is_user_triggered=False)
        messagebox.showinfo('Success', 'Questions reset successfully!')

    def show_help(self) -> None:
        help_text = (
            "Welcome to the QCM Generator IDE!\n\n"
            "Overview:\n"
            "This application allows you to create and manage QCM (Questionnaire à Choix Multiples) documents.\n\n"
            "Loading Questions:\n"
            "1. Click 'Load Questions' to open your 'questions.txt' file.\n"
            "2. Ensure the format follows: \n"
            "   - Each question starts with 'Q' and is followed by its answers.\n\n"
            "Saving Questions:\n"
            "Use the 'Save Questions' button to save your changes.\n\n"
            "Generating Subjects:\n"
            "Click 'Generate Subjects' to create QCM documents from the loaded questions.\n\n"
            "Including Images:\n"
            "Use 'Include Image' to insert images into your LaTeX documents. You will be prompted to select an image file.\n\n"  # noqa: E501
            "If in doubt, this is the default header for the questions file:\n"
            "QCM Title\n"
            "Author\n"
            "School\n"
            "Course\n"
            "Date\n\n"
            "Contact:\n"
            "For assistance, please reach out by creating an issue on the GitHub repository: \n"
            "https://github.com/toby-bro/latex_QCM_generator"
        )
        help_window = tk.Toplevel(self.root)
        help_window.title('Help')
        help_label = tk.Label(help_window, text=help_text, justify=tk.LEFT, padx=10, pady=10)
        help_label.pack()
        help_window.minsize(700, 570)

    def load_questions_from_file(self) -> None:
        questions_file: str = filedialog.askopenfilename(
            title='Select Questions File',
            filetypes=[('Text Files', '*.txt')],
        )
        if questions_file:
            self.load_questions(questions_file)

    def load_questions(self, questions_file: str, *, is_user_triggered: bool = False) -> None:
        with open(questions_file, 'r', encoding='UTF8') as file:
            content: str = file.read()
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, content)

        if is_user_triggered:
            messagebox.showinfo('Success', 'Questions loaded successfully!')

    def save_questions(self) -> None:
        questions_file: str = filedialog.asksaveasfilename(
            title='Save Questions File',
            defaultextension='.txt',
            filetypes=[('Text Files', '*.txt')],
        )
        self.save_questions_to_file(questions_file)

    def save_questions_to_file(self, questions_file: str, *, is_user_triggered: bool = False) -> None:
        if questions_file:
            content: str = self.text_area.get(1.0, tk.END)
            with open(questions_file, 'w', encoding='UTF8') as file:
                file.write(content.strip())
            if is_user_triggered:
                messagebox.showinfo('Success', 'Questions saved successfully!')

    def generate_subjects(self) -> None:
        self.save_questions_to_file(QUESTION_FILE)
        try:
            generate_subjects()
            messagebox.showinfo(
                'Success',
                f'Subjects generated successfully! \n'
                f'Check the {os.path.join(os.path.dirname(__file__), "sujects")} folder to find them.',
            )
        except Exception as e:
            messagebox.showerror('Error', f'An error occurred while generating subjects: {e}')

    def include_image(self) -> None:
        image_file: str = filedialog.askopenfilename(
            title='Select Image File',
            filetypes=[
                ('Image Files', '*.png'),
                ('Image Files', '*.jpg'),
                ('Image Files', '*.jpeg'),
                ('Image Files', '*.pdf'),
            ],
        )
        if image_file:
            cursor_pos: str = self.text_area.index(tk.INSERT)

            include_command: str = f'\\includegraphics[width=0.5\\textwidth]{{{image_file}}}\n'

            self.text_area.insert(cursor_pos, include_command)

    def open_subjects_folder(self) -> None:
        path = os.path.join(os.path.dirname(__file__), 'subjects')
        if platform.system() == 'Windows':
            os.startfile(path)  # type: ignore[attr-defined]  # noqa: S606
        elif platform.system() == 'Darwin':  # macOS
            subprocess.run(['open', path], check=False)  # noqa: S607, S603
        elif platform.system() == 'Linux':
            subprocess.run(['xdg-open', path], check=False)  # noqa: S603, S607
        else:
            messagebox.showwarning('Warning', 'Unsupported operating system.')


def reload_questions(reset: bool = True) -> None:
    QUESTION_TEMPLATE_FILE = os.path.join(os.path.dirname(__file__), 'questions-template.txt')

    if os.path.exists(QUESTION_FILE):
        if reset:
            os.remove(QUESTION_FILE)
        else:
            return

    if os.path.exists(QUESTION_TEMPLATE_FILE):
        with open(QUESTION_TEMPLATE_FILE, 'r', encoding='UTF8') as template_file:
            template_content = template_file.read()
        with open(QUESTION_FILE, 'w', encoding='UTF8') as question_file:
            question_file.write(template_content)
    else:
        messagebox.showerror('Error', 'Template file not found. Cannot create questions.txt.')


if __name__ == '__main__':
    reload_questions(False)

    root: tk.Tk = tk.Tk()
    app = QCMGeneratorIDE(root)
    root.mainloop()
