import matplotlib.pyplot as plt
import matplotlib as mpl

# Set professional style
plt.style.use('seaborn-v0_8-darkgrid')
mpl.rcParams['font.size'] = 10
mpl.rcParams['axes.labelsize'] = 11
mpl.rcParams['axes.titlesize'] = 12
mpl.rcParams['xtick.labelsize'] = 9
mpl.rcParams['ytick.labelsize'] = 9

def subject_average_bar(df, subj_cols):
    """
    Return a matplotlib Figure of subject-wise average marks.
    """
    means = df[subj_cols].mean()
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = means.plot.bar(ax=ax, color='#1f77b4', edgecolor='black', linewidth=0.7)
    ax.set_ylabel('Average Marks', fontweight='bold')
    ax.set_xlabel('Subjects', fontweight='bold')
    ax.set_ylim(0, 100)
    ax.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for i, v in enumerate(means):
        ax.text(i, v + 2, f'{v:.1f}', ha='center', va='bottom', fontsize=9)
    
    plt.xticks(rotation=45, ha='right')
    fig.tight_layout()
    return fig

def grade_distribution_pie(df):
    fig, ax = plt.subplots(figsize=(7, 5))
    grade_counts = df['Grade'].value_counts()
    colors = ['#2ecc71', '#3498db', '#f39c12', '#e74c3c', '#95a5a6']
    
    wedges, texts, autotexts = ax.pie(
        grade_counts, 
        labels=grade_counts.index,
        autopct='%1.1f%%',
        colors=colors[:len(grade_counts)],
        startangle=90,
        textprops={'fontsize': 10, 'weight': 'bold'}
    )
    
    # Make percentage text more visible
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(11)
    
    ax.set_ylabel('')
    fig.tight_layout()
    return fig

def attendance_vs_percentage_scatter(df):
    fig, ax = plt.subplots(figsize=(8, 5))
    if 'Attendance(%)' in df.columns and 'Percentage' in df.columns:
        scatter = ax.scatter(
            df['Attendance(%)'], 
            df['Percentage'],
            c=df['Percentage'],
            cmap='viridis',
            s=100,
            alpha=0.6,
            edgecolors='black',
            linewidth=0.5
        )
        ax.set_xlabel('Attendance (%)', fontweight='bold')
        ax.set_ylabel('Performance (%)', fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        # Add colorbar
        cbar = plt.colorbar(scatter, ax=ax)
        cbar.set_label('Performance %', rotation=270, labelpad=15)
        
    fig.tight_layout()
    return fig

def student_subject_radar(student_row, subj_cols, class_avg):
    """
    Create a radar chart comparing student's marks with class average.
    """
    import numpy as np
    
    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(projection='polar'))
    
    angles = np.linspace(0, 2 * np.pi, len(subj_cols), endpoint=False).tolist()
    angles += angles[:1]
    
    student_marks = [student_row[s] for s in subj_cols]
    student_marks += student_marks[:1]
    
    avg_marks = [class_avg[s] for s in subj_cols]
    avg_marks += avg_marks[:1]
    
    ax.plot(angles, student_marks, 'o-', linewidth=2, label='Student', color='#e74c3c')
    ax.fill(angles, student_marks, alpha=0.25, color='#e74c3c')
    
    ax.plot(angles, avg_marks, 'o-', linewidth=2, label='Class Average', color='#3498db')
    ax.fill(angles, avg_marks, alpha=0.25, color='#3498db')
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(subj_cols, size=10)
    ax.set_ylim(0, 100)
    ax.set_yticks([25, 50, 75, 100])
    ax.grid(True)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    
    fig.tight_layout()
    return fig

def student_performance_bar(student_row, subj_cols):
    """
    Create a bar chart of student's subject-wise marks.
    """
    fig, ax = plt.subplots(figsize=(8, 5))
    marks = [student_row[s] for s in subj_cols]
    colors = ['#2ecc71' if m >= 75 else '#f39c12' if m >= 60 else '#e74c3c' for m in marks]
    
    bars = ax.bar(subj_cols, marks, color=colors, edgecolor='black', linewidth=0.7)
    ax.set_ylabel('Marks', fontweight='bold')
    ax.set_xlabel('Subjects', fontweight='bold')
    ax.set_ylim(0, 100)
    ax.axhline(y=40, color='red', linestyle='--', linewidth=1, alpha=0.5, label='Pass Mark (40)')
    ax.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for i, v in enumerate(marks):
        ax.text(i, v + 2, f'{v:.0f}', ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    plt.xticks(rotation=45, ha='right')
    ax.legend()
    fig.tight_layout()
    return fig
