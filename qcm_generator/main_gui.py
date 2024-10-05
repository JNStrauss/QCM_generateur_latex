import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

from qcm_generator.main import generate_subjects

QUESTION_FILE = os.path.join(os.path.dirname(__file__), 'questions.txt')


class QCMGeneratorIDE:
    def __init__(self, root: tk.Tk) -> None:
        self.root: tk.Tk = root
        self.root.title('QCM Generator IDE')

        # Text area for editing questions.txt
        self.text_area: scrolledtext.ScrolledText = scrolledtext.ScrolledText(root, width=60, height=20, wrap=tk.WORD)
        self.text_area.grid(row=0, column=0, padx=5, pady=5, columnspan=2)

        # Load Questions Button
        self.load_btn: tk.Button = tk.Button(root, text='Load Questions', command=self.load_questions_from_file)
        self.load_btn.grid(row=1, column=0, padx=5, pady=5)

        # Save Questions Button
        self.save_btn: tk.Button = tk.Button(root, text='Save Questions', command=self.save_questions)
        self.save_btn.grid(row=1, column=1, padx=5, pady=5)

        # Generate Subjects Button
        self.generate_subjects_btn: tk.Button = tk.Button(
            root,
            text='Generate Subjects',
            command=self.generate_subjects,
        )
        self.generate_subjects_btn.grid(row=2, column=0, padx=5, pady=5, columnspan=2)

        # Include Image Button
        self.include_image_btn: tk.Button = tk.Button(root, text='Include Image', command=self.include_image)
        self.include_image_btn.grid(row=3, column=0, padx=5, pady=5, columnspan=2)

        self.load_questions(
            QUESTION_FILE,
            is_user_triggered=False,
        )  # Load the questions file by default

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
            self.text_area.delete(1.0, tk.END)  # Clear the text area
            self.text_area.insert(tk.END, content)  # Insert the loaded content

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
            content: str = self.text_area.get(1.0, tk.END)  # Get all text from the text area
            with open(questions_file, 'w', encoding='UTF8') as file:
                file.write(content.strip())  # Write content without leading/trailing whitespace
            if is_user_triggered:
                messagebox.showinfo('Success', 'Questions saved successfully!')

    def generate_subjects(self) -> None:
        # Here you would typically load the questions from the text area and call the main function.
        # For now, let's just show a message indicating this action.
        # messagebox.showinfo('Generate Subjects', 'This will call the generation function.')
        # You can add the logic to parse questions from self.text_area and call qcm_generator.main() as needed.
        self.save_questions_to_file(QUESTION_FILE)  # Save the questions before generating subjects
        try:
            generate_subjects()
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
            # Get the current cursor position
            cursor_pos: str = self.text_area.index(tk.INSERT)

            # Create the LaTeX includegraphics command
            include_command: str = f'\\includegraphics[width=0.5\\textwidth]{{{image_file}}}\n'

            # Insert the command at the cursor position
            self.text_area.insert(cursor_pos, include_command)

            # messagebox.showinfo('Success', f"Image '{image_file}' included successfully!")


if __name__ == '__main__':
    root: tk.Tk = tk.Tk()
    app = QCMGeneratorIDE(root)
    root.mainloop()
