import tkinter as tk
from tkinter import filedialog
import subprocess
import matplotlib.pyplot as plt
from io import BytesIO

class LaTeXQuizReportGenerator:
    def __init__(self, master):
        self.master = master
        master.title("LaTeX Quiz Report Generator")

        self.label = tk.Label(master, text="Enter quiz marks (comma-separated):")
        self.label.pack()

        self.entry = tk.Entry(master)
        self.entry.pack()

        self.generate_button = tk.Button(master, text="Generate Report", command=self.generate_report)
        self.generate_button.pack()

    def generate_report(self):
        marks = [int(mark) for mark in self.entry.get().split(',')]
        latex_content = self.create_latex_content(marks)
        self.save_and_compile_latex(latex_content)

    def create_latex_content(self, marks):
        average_score = sum(marks) / len(marks)
        
        # Generate histogram
        plt.figure(figsize=(6, 4))
        plt.hist(marks, bins=10, edgecolor='black')
        plt.title('Distribution of Quiz Scores')
        plt.xlabel('Score')
        plt.ylabel('Frequency')
        
        # Save plot to BytesIO object
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png')
        img_buffer.seek(0)
        
        # Convert plot to base64 for embedding in LaTeX
        import base64
        img_str = base64.b64encode(img_buffer.getvalue()).decode()

        latex_content = (
        "\\documentclass{{article}}\n"  # Escaped article correctly
        "\\usepackage{{graphicx}}\n"
        "\n"
        "\\begin{{document}}\n"
        "\n"
        "\\section{{Quiz Report}}\n"
        "\n"
        "The average score for this quiz was {:.2f}.\n"
        "\n"
        "\\end{{document}}\n"
    ).format(average_score)

        return latex_content

    def save_and_compile_latex(self, content):
        file_path = filedialog.asksaveasfilename(defaultextension=".tex")
        if file_path:
            with open(file_path, 'w') as file:
                file.write(content)
            
            # Compile LaTeX to PDF
            subprocess.run(["pdflatex", file_path])

root = tk.Tk()
app = LaTeXQuizReportGenerator(root)
root.mainloop()
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import subprocess
import os

class QuizReportGenerator:
    def __init__(self, student_name, ai_score, reasoning_score):
        self.student_name = student_name
        self.ai_score = ai_score
        self.reasoning_score = reasoning_score
        self.total_score = ai_score + reasoning_score
        self.max_score = 200

    def generate_report(self):
        latex_content = self.create_latex_content()
        return self.save_and_compile_latex(latex_content)

    def create_latex_content(self):
        # Generate charts
        ai_chart = self.generate_chart(self.ai_score, 100, "AI Score")
        reasoning_chart = self.generate_chart(self.reasoning_score, 100, "Reasoning Score")
        total_chart = self.generate_chart(self.total_score, self.max_score, "Total Score")

        latex_content = r"""
\documentclass{article}
\usepackage{graphicx}
\usepackage{geometry}
\usepackage{color}
\usepackage{tikz}

\geometry{a4paper, margin=1in}

\begin{document}

\title{Comprehensive Quiz Report}
\author{AI Learning System}
\date{\today}

\maketitle

\section{Student Performance Summary}

\textbf{Student Name:} {student_name}

\subsection{{AI Module}}
\textbf{{Score:}} {ai_score}/100

{ai_chart}

\textbf{{Performance Analysis:}}
The student achieved a score of {ai_score}\% in the AI module, which indicates a {ai_performance} understanding of AI concepts. {ai_analysis}

\textbf{{Recommendations:}}
\begin{{itemize}}
    {ai_recommendations}
\end{{itemize}}

\subsection{{Reasoning Module}}
\textbf{{Score:}} {reasoning_score}/100

{reasoning_chart}

\textbf{{Performance Analysis:}}
With a score of {reasoning_score}\% in the Reasoning module, the student demonstrates {reasoning_performance} logical and analytical skills. {reasoning_analysis}

\textbf{{Recommendations:}}
\begin{{itemize}}
    {reasoning_recommendations}
\end{{itemize}}

\section{{Overall Performance}}
\textbf{{Total Score:}} {total_score}/{max_score}

{total_chart}

\textbf{{Overall Analysis:}}
The student's overall performance of {overall_percentage}\% ({total_score}/{max_score}) indicates {overall_performance}. {overall_analysis}

\textbf{{General Recommendations:}}
\begin{{itemize}}
    {overall_recommendations}
\end{{itemize}}

\section{{Conclusion}}
{conclusion}

\end{document}
"""
        # Determine performance levels and generate appropriate feedback
        ai_performance = "basic" if self.ai_score < 70 else "good" if self.ai_score < 90 else "excellent"
        reasoning_performance = "basic" if self.reasoning_score < 70 else "good" if self.reasoning_score < 90 else "excellent"
        overall_percentage = (self.total_score / self.max_score) * 100
        overall_performance = "a basic foundation" if overall_percentage < 70 else "a good foundation" if overall_percentage < 90 else "an excellent foundation"

        # Generate analysis and recommendations based on scores
        ai_analysis, ai_recommendations = self.generate_feedback(self.ai_score, "AI")
        reasoning_analysis, reasoning_recommendations = self.generate_feedback(self.reasoning_score, "reasoning")
        overall_analysis, overall_recommendations = self.generate_overall_feedback()

        conclusion = f"The student shows {'promise' if overall_percentage >= 70 else 'room for improvement'} in both AI and reasoning, with a particular aptitude for {'logical thinking' if self.reasoning_score > self.ai_score else 'AI concepts'}. By {'addressing the areas for improvement' if overall_percentage < 90 else 'continuing to challenge themselves'}, the student can {'achieve' if overall_percentage < 90 else 'maintain'} a high level of competence in both fields. Regular practice, engagement with {'fundamental' if overall_percentage < 70 else 'challenging'} problems, and application of knowledge to real-world scenarios will be key to continued growth and success."

        return latex_content.format(
            student_name=self.student_name,
            ai_score=self.ai_score,
            reasoning_score=self.reasoning_score,
            total_score=self.total_score,
            max_score=self.max_score,
            ai_chart=ai_chart,
            reasoning_chart=reasoning_chart,
            total_chart=total_chart,
            ai_performance=ai_performance,
            reasoning_performance=reasoning_performance,
            overall_percentage=overall_percentage,
            overall_performance=overall_performance,
            ai_analysis=ai_analysis,
            ai_recommendations=ai_recommendations,
            reasoning_analysis=reasoning_analysis,
            reasoning_recommendations=reasoning_recommendations,
            overall_analysis=overall_analysis,
            overall_recommendations=overall_recommendations,
            conclusion=conclusion
        )

    def generate_chart(self, score, max_score, title):
        percentage = (score / max_score) * 100
        return r"""
\begin{{tikzpicture}}
\draw[thick] (0,0) -- (4,0);
\draw[thick, color=blue, line width=10pt] (0,0) -- ({0.04*%d},0);
\node[above] at (2,0.2) {{\textbf{%s}}};
\node[below] at (0,0) {{0}};
\node[below] at (4,0) {{100}};
\node[below] at ({0.04*%d},0) {{\textbf{%d\%%}}};
\end{{tikzpicture}}
""" % (percentage, title, percentage, percentage)

    def generate_feedback(self, score, subject):
        if score < 70:
            analysis = f"This indicates a need for significant improvement in {subject} concepts and skills."
            recommendations = r"\item Review fundamental " + f"{subject} concepts and principles." + \
                              r"\item Engage with interactive tutorials and exercises to strengthen understanding." + \
                              r"\item Seek additional support or resources to address knowledge gaps."
        elif score < 90:
            analysis = f"This demonstrates a solid grasp of {subject} concepts with room for further improvement."
            recommendations = r"\item Deepen understanding of advanced " + f"{subject} topics." + \
                              r"\item Practice applying " + f"{subject} skills to more complex problems." + \
                              r"\item Explore real-world applications to enhance practical skills."
        else:
            analysis = f"This showcases an excellent understanding and application of {subject} concepts."
            recommendations = r"\item Explore cutting-edge developments in the field of " + f"{subject}." + \
                              r"\item Consider mentoring peers or engaging in advanced projects." + \
                              r"\item Seek opportunities to apply " + f"{subject} skills in interdisciplinary contexts."
        return analysis, recommendations

    def generate_overall_feedback(self):
        diff = abs(self.ai_score - self.reasoning_score)
        if diff > 20:
            stronger = "AI" if self.ai_score > self.reasoning_score else "reasoning"
            weaker = "reasoning" if stronger == "AI" else "AI"
            analysis = f"There is a significant disparity between {stronger} and {weaker} skills."
            recommendations = r"\item Focus on improving " + f"{weaker} skills to match the strong performance in {stronger}." + \
                              r"\item Seek opportunities to apply " + f"{stronger} skills to {weaker} problems." + \
                              r"\item Engage in projects that combine both AI and reasoning to create synergy between the two areas."
        else:
            analysis = "The performance is well-balanced between AI and reasoning skills."
            recommendations = r"\item Continue to develop both AI and reasoning skills in tandem." + \
                              r"\item Explore advanced topics that integrate both AI and reasoning concepts." + \
                              r"\item Seek out complex, multidisciplinary projects to apply and enhance both skill sets."
        return analysis, recommendations

    def save_and_compile_latex(self, content):
        with open('report.tex', 'w') as file:
            file.write(content)
        
        # Compile LaTeX to PDF
        subprocess.run(["pdflatex", "report.tex"])
        
        # Check if PDF was created
        if os.path.exists("report.pdf"):
            return "Report generated successfully. PDF file: report.pdf"
        else:
            return "Error: PDF file was not created. Check LaTeX compilation output for errors."

# Usage example
generator = QuizReportGenerator("John Doe", 60, 80)
result = generator.generate_report()
print(result)