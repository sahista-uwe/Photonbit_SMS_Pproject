import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def init_grade_history(username):
    """Initialize grade history file for new students"""
    history_dir = 'data/grade_history'
    os.makedirs(history_dir, exist_ok=True)
    
    if not os.path.exists(f'{history_dir}/{username}.csv'):
        pd.DataFrame(columns=[
            'date', 'math', 'science', 'english', 'history', 'art'
        ]).to_csv(f'{history_dir}/{username}.csv', index=False)

def record_grade_update(username, grades):
    """
    Record grade changes in history file
    Called whenever grades are updated
    """
    history_file = f'data/grade_history/{username}.csv'
    today = datetime.now().strftime('%Y-%m-%d')
    
    new_record = {'date': today}
    new_record.update(grades)
    
    history_df = pd.read_csv(history_file)
    history_df = pd.concat([history_df, pd.DataFrame([new_record])])
    history_df.to_csv(history_file, index=False)

def plot_grade_trends(username, window=None):
    """
    Plot grade trends over time with multiple visualization options
    Args:
        username: Student ID
        window: Optional Tkinter window for embedding
    Returns:
        Matplotlib figure if window=None, else embeds in Tkinter
    """
    history_file = f'data/grade_history/{username}.csv'
    
    try:
        df = pd.read_csv(history_file)
        if len(df) < 2:
            raise ValueError("Insufficient data for trends")
            
        df['date'] = pd.to_datetime(df['date'])
        df.sort_values('date', inplace=True)
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
        plt.suptitle(f'Grade Trends for {username}')
        
        # Line plot for individual subjects
        subjects = ['math', 'science', 'english', 'history', 'art']
        for subject in subjects:
            ax1.plot(df['date'], df[subject], marker='o', label=subject)
        ax1.set_ylabel('Score')
        ax1.legend()
        ax1.grid(True)
        
        # Overall average trend
        df['average'] = df[subjects].mean(axis=1)
        ax2.plot(df['date'], df['average'], marker='s', color='purple', linewidth=2)
        ax2.set_ylabel('Overall Average')
        ax2.grid(True)
        
        plt.tight_layout()
        
        if window:
            canvas = FigureCanvasTkAgg(fig, master=window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', expand=True)
            return canvas
        return fig
        
    except Exception as e:
        print(f"Error plotting trends: {str(e)}")
        return None
    
def plot_subject_averages():
    """Create a bar chart of average scores per subject across all students."""
    import pandas as pd
    import matplotlib.pyplot as plt
    import os

    history_dir = 'data/grade_history'
    subject_scores = {'math': [], 'science': [], 'english': [], 'history': [], 'art': []}

    for file in os.listdir(history_dir):
        if file.endswith('.csv'):
            df = pd.read_csv(os.path.join(history_dir, file))
            if not df.empty:
                for subject in subject_scores:
                    subject_scores[subject].extend(df[subject].tolist())

    averages = {subj: sum(scores)/len(scores) if scores else 0 for subj, scores in subject_scores.items()}

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(averages.keys(), averages.values(), color='skyblue')
    ax.set_title("Average Subject Scores")
    ax.set_ylabel("Average Score")
    return fig

def embed_plot(window, fig):
    """Embed a Matplotlib figure into a Tkinter window."""
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)
