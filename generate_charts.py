import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import glob

plt.rcParams.update({
    'font.size': 20,           # Base font size (increased from 14)
    'axes.titlesize': 24,      # Chart titles (increased from 18)
    'axes.labelsize': 20,      # X and Y axis labels (increased from 16)
    'xtick.labelsize': 18,     # X-axis tick labels (increased from 14)
    'ytick.labelsize': 18,     # Y-axis tick labels (increased from 14)
    'legend.fontsize': 18,     # Legend text (increased from 14)
    'figure.dpi': 150,         # Optional: higher resolution
})

# Set output directory
output_dir = 'immagini/charts'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def clean_percentage(val):
    if isinstance(val, str) and '%' in val:
        return float(val.replace('%', '').replace('+', '').replace('-', '')) / 100.0
    try:
        return float(val)
    except (ValueError, TypeError):
        return 0.0

def clean_time(val):
    if isinstance(val, str) and 's' in val:
        return float(val.replace('s', ''))
    try:
        return float(val)
    except (ValueError, TypeError):
        return 0.0

# 1. Database Successes Chart
def plot_db_successes():
    df = pd.read_csv('statistiche/databases_report/summary.csv')
    databases = df['Database']
    text_rates = [clean_percentage(x) * 100 for x in df['Success rate text']]
    db_conn_rates = [clean_percentage(x) * 100 for x in df['Success rate db_conn']]

    x = np.arange(len(databases))
    width = 0.35

    fig, ax = plt.subplots(figsize=(15, 8))
    ax.bar(x - width/2, text_rates, width, label='Text', color='skyblue')
    ax.bar(x + width/2, db_conn_rates, width, label='DB Conn', color='salmon')

    ax.set_ylabel('Success Rate (%)')
    ax.set_title('Success Rate sui Database con entrambe le modalità')
    ax.set_xticks(x)
    ax.set_xticklabels(databases, rotation=45, ha='right')
    ax.legend()
    plt.tight_layout()
    plt.savefig(f'{output_dir}/db_successes.png')
    plt.close()

# 2. Model Times Chart
def plot_model_times():
    model_folders = [f for f in os.listdir('statistiche') if f.endswith('_report') and f != 'databases_report']
    models = []
    times_text = []
    times_db = []

    for folder in model_folders:
        model_name = folder.replace('_report', '')
        file_path = f'statistiche/{folder}/status.csv'
        if not os.path.exists(file_path): continue
        df = pd.read_csv(file_path)
        df.columns = df.columns.str.strip()
        df['Database'] = df['Database'].astype(str).str.strip()
        verdict = df[df['Database'] == 'MODEL VERDICT'].iloc[0]

        models.append(model_name)
        times_text.append(clean_time(verdict['Avg time text']))
        times_db.append(clean_time(verdict['Avg time db_conn']))

    x = np.arange(len(models))
    width = 0.35

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(x - width/2, times_text, width, label='Text', color='skyblue')
    ax.bar(x + width/2, times_db, width, label='DB Conn', color='salmon')

    ax.set_ylabel('Average Time (s)')
    ax.set_title('Average Execution Time by Model and Mode')
    ax.set_xticks(x)
    ax.set_xticklabels(models, rotation=45, ha='right')
    ax.legend()
    plt.tight_layout()
    plt.savefig(f'{output_dir}/model_times.png')
    plt.close()

# 3. Model Attempts Chart
def plot_model_attempts():
    model_folders = [f for f in os.listdir('statistiche') if f.endswith('_report') and f != 'databases_report']
    models = []
    attempts_text = []
    attempts_db = []

    for folder in model_folders:
        model_name = folder.replace('_report', '')
        file_path = f'statistiche/{folder}/status.csv'
        if not os.path.exists(file_path): continue
        df = pd.read_csv(file_path)
        verdict = df[df['Database'] == 'MODEL VERDICT'].iloc[0]

        models.append(model_name)
        attempts_text.append(float(verdict['Avg attempts text']))
        attempts_db.append(float(verdict['Avg attempts db_conn']))

    x = np.arange(len(models))
    width = 0.35

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(x - width/2, attempts_text, width, label='Text', color='skyblue')
    ax.bar(x + width/2, attempts_db, width, label='DB Conn', color='salmon')

    ax.set_ylabel('Average Attempts')
    ax.set_title('Average Number of Attempts by Model and Mode')
    ax.set_xticks(x)
    ax.set_xticklabels(models, rotation=45, ha='right')
    ax.legend()
    plt.tight_layout()
    plt.savefig(f'{output_dir}/model_attempts.png')
    plt.close()

# 4. Error Types Comparison
def plot_error_comparison():
    target_models = [
        ('gpt-4o_report', 'GPT-4o'),
        ('gpt-5-mini_report', 'GPT-5-mini'),
        ('codellama_34b_report', 'CodeLlama'),
        ('codestral_22b_report', 'Codestral'),
        ('sqlcoder_34b_report', 'SQLCoder'),
        ('Qwen3-coder-next_report', 'Qwen3-Coder-Next'),
    ]
    results = {}

    for folder, label in target_models:
        file_path = f'statistiche/{folder}/status.csv'
        if not os.path.exists(file_path): continue
        df = pd.read_csv(file_path)
        df.columns = df.columns.str.strip()
        df['Database'] = df['Database'].astype(str).str.strip()
        verdict = df[df['Database'] == 'MODEL VERDICT'].iloc[0]

        errors = {
            'text': {
                'Syntax': int(verdict['Syntax text']),
                'Runtime': int(verdict['Runtime text']),
                'Incorrect': int(verdict['Incorrect text'])
            },
            'db_conn': {
                'Syntax': int(verdict['Syntax db_conn']),
                'Runtime': int(verdict['Runtime db_conn']),
                'Incorrect': int(verdict['Incorrect db_conn'])
            }
        }
        results[label] = errors

    categories = ['Syntax', 'Runtime', 'Incorrect']

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8), sharey=True)

    x = np.arange(len(categories))
    width = 0.12
    colors = ['#1f77b4', '#2ca02c', '#ff7f0e', '#9467bd', '#d62728', '#8c564b']
    offsets = (np.arange(len(results)) - (len(results) - 1) / 2) * width

    for idx, (model_name, errors) in enumerate(results.items()):
        ax1.bar(
            x + offsets[idx],
            [errors['text'][cat] for cat in categories],
            width,
            label=model_name,
            color=colors[idx],
        )
        ax2.bar(
            x + offsets[idx],
            [errors['db_conn'][cat] for cat in categories],
            width,
            label=model_name,
            color=colors[idx],
        )

    ax1.set_title('Error Types: Text Mode')
    ax1.set_xticks(x)
    ax1.set_xticklabels(categories)
    ax1.set_ylabel('Count')

    ax2.set_title('Error Types: DB Conn Mode')
    ax2.set_xticks(x)
    ax2.set_xticklabels(categories)

    handles, labels = ax1.get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower center', ncol=3, bbox_to_anchor=(0.5, -0.02))
    plt.tight_layout(rect=(0, 0.08, 1, 1))
    plt.savefig(f'{output_dir}/error_comparison.png', bbox_inches='tight')

    plt.close()

# 5. Complexity vs Success Rate
def plot_complexity_vs_success():
    df_comp = pd.read_csv('statistiche/databases_report/summary.csv')[['Database', 'Complexity score']]
    df_comp = df_comp.sort_values('Complexity score')

    databases = df_comp['Database'].tolist()
    complexity = df_comp['Complexity score'].tolist()

    model_folders = [f for f in os.listdir('statistiche') if f.endswith('_report') and f != 'databases_report']

    text_successes = {}
    db_conn_successes = {}

    for folder in model_folders:
        model_name = folder.replace('_report', '')
        file_path = f'statistiche/{folder}/status.csv'
        if not os.path.exists(file_path): continue

        df_model = pd.read_csv(file_path)
        text_map = dict(zip(df_model['Database'], df_model['Success text']))
        db_map = dict(zip(df_model['Database'], df_model['Success db_conn']))

        text_successes[model_name] = [clean_percentage(text_map.get(db, 0)) * 100 for db in databases]
        db_conn_successes[model_name] = [clean_percentage(db_map.get(db, 0)) * 100 for db in databases]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8), sharey=True)

    for model, rates in text_successes.items():
        ax1.plot(complexity, rates, marker='o', label=model)
    ax1.set_title('Text Mode: Complexity vs Success Rate')
    ax1.set_xlabel('Complexity Score')
    ax1.set_ylabel('Success Rate (%)')
    ax1.grid(True, linestyle='--', alpha=0.7)
    ax1.legend()

    for model, rates in db_conn_successes.items():
        ax2.plot(complexity, rates, marker='o', label=model)
    ax2.set_title('DB Conn Mode: Complexity vs Success Rate')
    ax2.set_xlabel('Complexity Score')
    ax2.grid(True, linestyle='--', alpha=0.7)
    ax2.legend()

    plt.tight_layout()
    plt.savefig(f'{output_dir}/complexity_vs_success.png')
    plt.close()

# 6. Diverging Bar Chart for Correlation Deltas
def plot_correlation_deltas():
    model_folders = [f for f in os.listdir('statistiche') if f.endswith('_report') and f != 'databases_report']

    data = {
        'Attempts Pearson': [],
        'Attempts Spearman': [],
        'Complexity Pearson': [],
        'Complexity Spearman': []
    }
    models = []

    for folder in model_folders:
        model_name = folder.replace('_report', '')

        # Attempts correlation
        att_path = f'statistiche/{folder}/attempts_correlations.csv'
        if os.path.exists(att_path):
            df_att = pd.read_csv(att_path)
            total_row = df_att[df_att['Database'].str.contains('MODEL\'S TOTAL', na=False)].iloc[0]
            data['Attempts Pearson'].append(float(total_row['Pearson delta']))
            data['Attempts Spearman'].append(float(total_row['Spearman delta']))

        # Complexity correlation
        comp_path = f'statistiche/{folder}/complexity_correlations.csv'
        if os.path.exists(comp_path):
            df_comp = pd.read_csv(comp_path)
            total_row = df_comp[df_comp['Database'].str.contains('MODEL\'S TOTAL', na=False)].iloc[0]
            data['Complexity Pearson'].append(float(total_row['Pearson delta']))
            data['Complexity Spearman'].append(float(total_row['Spearman delta']))

        models.append(model_name)

    # Create a figure with 4 subplots (2x2)
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    axes = axes.flatten()

    metrics = list(data.keys())
    colors = ['skyblue', 'salmon', 'lightgreen', 'orchid']

    for i, metric in enumerate(metrics):
        ax = axes[i]
        values = data[metric]
        y_pos = np.arange(len(models))

        # Use a color based on the value (positive/negative)
        bar_colors = ['salmon' if v < 0 else 'skyblue' for v in values]

        ax.barh(y_pos, values, color=bar_colors, edgecolor='black', alpha=0.8)
        ax.set_yticks(y_pos)
        ax.set_yticklabels(models)
        ax.set_title(metric)
        ax.set_xlabel('Delta Value')
        ax.axvline(0, color='black', linewidth=1)
        ax.grid(True, axis='x', linestyle='--', alpha=0.6)

    plt.tight_layout()
    plt.savefig(f'{output_dir}/correlation_deltas.png')
    plt.close()

if __name__ == '__main__':
    plot_db_successes()
    plot_model_times()
    plot_model_attempts()
    plot_error_comparison()
    plot_complexity_vs_success()
    plot_correlation_deltas()
    print("Charts generated successfully in the 'charts' directory.")
