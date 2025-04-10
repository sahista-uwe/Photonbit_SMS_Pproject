import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def plot_subject_averages():
    """Create grade distribution plot"""
    grades = pd.read_csv('data/grades.txt')
    fig, ax = plt.subplots(figsize=(8, 4))
    grades.mean().plot(kind='bar', ax=ax, color='skyblue')
    ax.set_title("Average Grades per Subject")
    ax.set_ylabel("Score")
    return fig

def embed_plot(window, fig):
    """Embed matplotlib plot in Tkinter"""
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack()


def plot_eca_participation():
    """Show ECA participation stats"""
    eca = pd.read_csv('data/eca.txt')
    fig, ax = plt.subplots()
    eca['activity1'].value_counts().plot.pie(ax=ax, autopct='%1.1f%%')
    return fig
