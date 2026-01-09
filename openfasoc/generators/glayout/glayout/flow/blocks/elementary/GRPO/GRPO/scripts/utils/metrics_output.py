import os
import glob
import subprocess
import re
import tempfile
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import pprint

sns.set_palette('husl')

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

PREDICTIONS_DIR = Path('pipeline_runs')

#patterns defined for relevance score, to check. this is currenlty only for the flipped voltage follower, more can be added
PATTERNS = {
    'gdsfactory_import': r'import.*gdsfactory',
    'glayout_import': r'import.*glayout', 
    'function_def': r'def.*flipped_voltage_follower',
    'component_creation': r'Component\(',
    'transistors': r'(nmos|pmos)\(',
    'placement': r'move[xy]?\(',
    'routing': r'(straight_route|c_route|L_route)',
    'ports': r'add_port',
    'netlist': r'netlist'
}

# def get_prediction_files():
#     """Get all prediction files from pipeline runs structure."""
#     if not PREDICTIONS_DIR.exists():
#         print(f'Warning: Pipeline runs directory not found - {PREDICTIONS_DIR}')
#         return {}
    
#     #get most recent run directory (by timestamp)
#     run_dirs = [d for d in PREDICTIONS_DIR.iterdir() if d.is_dir()]
#     if not run_dirs:
#         print('Warning: No pipeline run directories found')
#         return {}
    
#     latest_run = max(run_dirs, key=lambda x: x.name)
#     print(f'Using latest pipeline run: {latest_run}')
    
#     outputs_dir = latest_run / 'outputs'
#     if not outputs_dir.exists():
#         print(f'Warning: Outputs directory not found - {outputs_dir}')
#         return {}
    
#     files = {}
#     iteration_dirs = sorted([d for d in outputs_dir.iterdir() if d.is_dir() and d.name.startswith('iteration_')])
    
#     for iteration_dir in iteration_dirs:
#         iteration_name = iteration_dir.name 
#         base_dir = iteration_dir / 'base'
#         finetuned_dir = iteration_dir / 'finetuned'

#         entry = {}
#         if base_dir.exists():
#             base_files = sorted(list(base_dir.glob('prediction_*.py')))
#             if base_files:
#                 entry['base'] = base_files
#                 print(f'Found {len(base_files)} base files in {iteration_name}')
#         if finetuned_dir.exists():
#             ft_files = sorted(list(finetuned_dir.glob('prediction_*.py')))
#             if ft_files:
#                 entry['finetuned'] = ft_files
#                 print(f'Found {len(ft_files)} finetuned files in {iteration_name}')
#         if entry:
#             files[iteration_name] = entry
    
#     return files

# COMMENTED OUT - seperate implementation for reference
def get_prediction_files():
    """Get all prediction files organized by run and model size."""
    runs = ['base_models', 'run-1', 'run-2', 'run-3']
    sizes = ['7b', '13b']
    
    files = {}
    for run in runs:
        files[run] = {}
        for size in sizes:
            path = PREDICTIONS_DIR / run / size
            if path.exists():
                files[run][size] = sorted(list(path.glob('prediction_*.txt')))
            else:
                print(f'Warning: Path not found - {path}')
    return files

def extract_code(file_path):
    """Extract Python code from prediction file."""
    with open(file_path) as f:
        content = f.read()
    
    if str(file_path).endswith('.py'):
        return content.strip()  # .py files are already pure Python code
    
    code_match = re.search(r'```python\\n(.+?)```', content, re.DOTALL)
    if code_match:
        return code_match.group(1).strip()
    return content.strip()  

def check_compilation(code):
    with tempfile.NamedTemporaryFile(suffix='.py') as tmp:
        tmp.write(code.encode())
        tmp.flush()
        try:
            subprocess.check_output(['python', '-m', 'py_compile', tmp.name], 
                                  stderr=subprocess.STDOUT)
            return True
        except subprocess.CalledProcessError:
            return False

def count_lines(code):
    return len([line for line in code.splitlines() if line.strip()])

def calculate_relevance(code):
    score = 0
    for pattern in PATTERNS.values():
        if re.search(pattern, code):
            score += 1
    return (score / len(PATTERNS)) * 5 #normalise

def calculate_complexity(code):
    control_count = len(re.findall(r'\b(if|for|while|try|with)\b', code))
    
    func_count = len(re.findall(r'\bdef\b', code))
    
    class_count = len(re.findall(r'\bclass\b', code))
    
    return {
        'control_structures': control_count,
        'functions': func_count,
        'classes': class_count
    }

# def analyze_predictions():
#     files = get_prediction_files()
#     results = []
    
#     for iteration in files:
#         env_model_size = os.environ.get('MODEL_SIZE', 'combined')
#         for category in files[iteration]:  
#             for file in files[iteration][category]:
#                 code = extract_code(file)
#                 complexity = calculate_complexity(code)

#                 # Append '-ft' for finetuned predictions so we get 7b-ft / 13b-ft buckets
#                 model_size_val = env_model_size if category == 'base' else f"{env_model_size}-ft"

#                 result = {
#                     'run': iteration,
#                     'model_size': model_size_val,
#                     'file': file.name,
#                     'compiles': check_compilation(code),
#                     'lines': count_lines(code),
#                     'relevance': calculate_relevance(code),
#                     **complexity
#                 }
#                 results.append(result)
    
#     return pd.DataFrame(results)

# COMMENTED OUT - seperate implementation for reference
def analyze_predictions():
    """Analyze all prediction files and compute metrics."""
    files = get_prediction_files()
    results = []
    
    for run in files:
        for size in files[run]:
            for file in files[run][size]:
                code = extract_code(file)
                complexity = calculate_complexity(code)
                
                result = {
                    'run': run,
                    'model_size': size,
                    'file': file.name,
                    'compiles': check_compilation(code),
                    'lines': count_lines(code),
                    'relevance': calculate_relevance(code),
                    **complexity
                }
                results.append(result)
    
    return pd.DataFrame(results)

def run_statistical_tests(df, metric):
    from scipy import stats
    results = []
    runs = sorted(df['run'].unique())
    
    for i in range(len(runs)-1):
        for j in range(i+1, len(runs)):
            run1, run2 = runs[i], runs[j]
            
            t_stat, p_val = stats.ttest_ind(
                df[df['run'] == run1][metric],
                df[df['run'] == run2][metric]
            )
            
            results.append({
                'comparison': f'{run1} vs {run2}',
                'metric': metric,
                't_statistic': round(t_stat, 3),
                'p_value': round(p_val, 4),
                'significant': p_val < 0.05
            })
    
    return pd.DataFrame(results)

def save_plot(fig, filename):
    plots_dir = os.environ.get('PIPELINE_PLOTS_DIR', 'plots')
    os.makedirs(plots_dir, exist_ok=True)
    fig.savefig(os.path.join(plots_dir, filename))
    plt.close(fig)

if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=4)
    
    print("Running analysis...")
    results_df = analyze_predictions()
    print("Analysis complete!")
    
    # Calculate composite score
    results_df['composite_score'] = (results_df['compiles'] * 0.4) + ((results_df['relevance'] / 5.0) * 0.6)
    
    # Print results using pprint
    print("\nResults DataFrame (first 5 rows):")
    pp.pprint(results_df.head().to_dict())
    
    # Compute correlations
    corr_metrics = ['compiles', 'lines', 'relevance', 'composite_score', 'control_structures', 'functions', 'classes']
    corr_matrix = results_df[corr_metrics].corr()
    print("\nCorrelation Matrix:")
    pp.pprint(corr_matrix.to_dict())
    
    # Run statistical tests
    metrics_to_test = ['compiles', 'relevance', 'lines', 'composite_score']
    all_tests = pd.concat([run_statistical_tests(results_df, metric) 
                          for metric in metrics_to_test])
    print("\nStatistical Test Results:")
    pp.pprint(all_tests.sort_values(['metric', 'p_value']).to_dict())
    
    # Aggregate metrics
    summary = results_df.groupby(['run', 'model_size']).agg({
        'compiles': 'mean',
        'relevance': 'mean',
        'composite_score': 'mean',
        'lines': 'mean',
        'control_structures': 'mean',
        'functions': 'mean',
        'classes': 'mean'
    }).round(3)
    
    summary = summary.reset_index()
    summary['model_variant'] = summary['model_size'] + '-' + summary['run']
    
    print('\nSummary by Model Variant:')
    pp.pprint(summary.to_dict())
    
    # Generate and save plots
    plots_dir = os.environ.get('PIPELINE_PLOTS_DIR', 'plots')
    os.makedirs(plots_dir, exist_ok=True)
    
    unique_runs = sorted(summary['run'].unique(), key=lambda x: int(x.split('_')[-1]) if 'iteration_' in x else float('inf'))
    run_order = unique_runs
    summary['run_order'] = pd.Categorical(summary['run'], categories=run_order, ordered=True)
    summary = summary.sort_values(['model_size', 'run_order'])
    
    # Plot 1
    fig, ax = plt.subplots(figsize=(12, 6))
    for model in summary['model_size'].unique():
        data = summary[summary['model_size'] == model]
        ax.plot(data['run'], data['composite_score'], marker='o', label=model)
    ax.set_title('Composite Score Progression')
    ax.set_ylabel('Composite Score (0-1)')
    ax.set_xlabel('Run')
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    save_plot(fig, 'composite_progression.png')
    
    fig, ax = plt.subplots(figsize=(12, 6))
    for model in summary['model_size'].unique():
        data = summary[summary['model_size'] == model]
        ax.plot(data['run'], data['compiles'], marker='o', label=model)
    ax.set_title('Compilation Rate Progression')
    ax.set_ylabel('Compilation Rate (0-1)')
    ax.set_xlabel('Run')
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    save_plot(fig, 'compiles_progression.png')
    
    fig, ax = plt.subplots(figsize=(12, 6))
    for model in summary['model_size'].unique():
        data = summary[summary['model_size'] == model]
        ax.plot(data['run'], data['relevance'], marker='o', label=model)
    ax.set_title('Relevance Score Progression')
    ax.set_ylabel('Relevance Score (0-5)')
    ax.set_xlabel('Run')
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    save_plot(fig, 'relevance_progression.png')
    
    fig, ax = plt.subplots(figsize=(12, 6))
    for model in summary['model_size'].unique():
        data = summary[summary['model_size'] == model]
        ax.plot(data['run'], data['lines'], marker='o', label=model)
    ax.set_title('Average Code Length Progression')
    ax.set_ylabel('Average Lines')
    ax.set_xlabel('Run')
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    save_plot(fig, 'lines_progression.png')
    
    complexity_metrics = ['control_structures', 'functions', 'classes']
    complexity_df = summary.melt(id_vars=['model_variant'], value_vars=complexity_metrics,
                                 var_name='metric', value_name='count')
    fig, ax = plt.subplots(figsize=(14, 6))
    sns.barplot(data=complexity_df, x='model_variant', y='count', hue='metric', ax=ax)
    ax.set_title('Code Complexity Metrics by Model Variant')
    ax.set_ylabel('Average Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    save_plot(fig, 'complexity_metrics.png')
    
    results_df['model_variant'] = results_df['model_size'] + '-' + results_df['run']
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.boxplot(data=results_df, x='model_variant', y='composite_score', ax=ax)
    ax.set_title('Composite Score Distribution by Model Variant')
    ax.set_ylabel('Composite Score (0-1)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    save_plot(fig, 'composite_distribution.png')
    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.boxplot(data=results_df, x='model_variant', y='relevance', ax=ax)
    ax.set_title('Relevance Score Distribution by Model Variant')
    ax.set_ylabel('Relevance Score (0-5)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    save_plot(fig, 'relevance_distribution.png')
    
    fig, ax1 = plt.subplots(figsize=(10, 6))
    plt.rcParams['font.weight'] = 'bold'
    
    ax2 = ax1.twinx()
    
    colors = {
        '7b': {'relevance': 'red', 'compiles': 'darkgreen'},
        '13b': {'relevance': 'blue', 'compiles': 'darkorange'},
        # 'combined': {'relevance': 'purple', 'compiles': 'darkblue'},
        # 'combined-ft': {'relevance': 'darkmagenta', 'compiles': 'navy'}
    }
    markers = {
        '7b': {'relevance': 'x', 'compiles': 's'},
        '13b': {'relevance': 'o', 'compiles': '^'},
        # 'combined': {'relevance': 'D', 'compiles': 'v'},  
        # 'combined-ft': {'relevance': 'P', 'compiles': 'h'} 
    }
    
    for model_size in summary['model_size'].unique():
        model_data = summary[summary['model_size'] == model_size]
        
        ax1.plot(model_data['run'], model_data['relevance'], 
                 color=colors[model_size]['relevance'], 
                 marker=markers[model_size]['relevance'], 
                 linestyle='-',
                 label=f'{model_size} Relevance')
                 
        ax2.plot(model_data['run'], model_data['compiles'], 
                 color=colors[model_size]['compiles'], 
                 marker=markers[model_size]['compiles'],
                 linestyle='--',
                 label=f'{model_size} Compilation')

    ax1.set_xlabel('Run', fontweight='bold')
    ax1.set_ylabel('Relevance Score (0-5)', color='black', fontweight='bold')
    ax2.set_ylabel('Compilation Rate (0-1)', color='black', fontweight='bold')
    ax1.tick_params(axis='y', labelcolor='black', labelsize='medium')
    ax2.tick_params(axis='y', labelcolor='black', labelsize='medium')
    ax1.set_title('Relevance and Compilation Score Progression', fontweight='bold', fontsize='large')

    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines + lines2, labels + labels2, loc='best')

    plt.xticks(rotation=45)
    fig.tight_layout()
    save_plot(fig, 'progression_dual_axis.png')
    
    plt.rcParams['font.weight'] = 'normal' 


    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=summary, x='model_variant', y='composite_score', ax=ax)
    ax.set_title('Composite Score by Model Variant')
    ax.set_ylabel('Composite Score (0-1)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    save_plot(fig, 'composite_score.png')
    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=summary, x='model_variant', y='compiles', ax=ax)
    ax.set_title('Compilation Rate by Model Variant')
    ax.set_ylabel('Compilation Rate (0-1)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    save_plot(fig, 'compilation_rate.png')
    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=summary, x='model_variant', y='relevance', ax=ax)
    ax.set_title('Relevance Score by Model Variant')
    ax.set_ylabel('Relevance Score (0-5)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    save_plot(fig, 'relevance_score.png')
    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=summary, x='model_variant', y='lines', ax=ax)
    ax.set_title('Average Code Length by Model Variant')
    ax.set_ylabel('Average Lines')
    plt.xticks(rotation=45)
    plt.tight_layout()
    save_plot(fig, 'code_length.png')
    
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, ax=ax)
    ax.set_title('Correlation Matrix of Code Metrics')
    plt.tight_layout()
    save_plot(fig, 'correlation_heatmap.png')
    
    print("\nAll metrics calculated and printed.")
    plots_dir = os.environ.get('PIPELINE_PLOTS_DIR', 'plots')
    print(f"Enhanced plots saved to '{plots_dir}' directory.") 