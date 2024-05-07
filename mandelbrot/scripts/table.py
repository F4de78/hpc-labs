import pandas as pd

def static_dynamic(df):
    # Group by 'thread_no', 'omp_schedule', and 'res' and calculate the average of 'time'
    grouped_df = df.groupby(['thread_no', 'omp_schedule', 'res'])['time'].mean().reset_index()

    # Pivot the DataFrame
    pivot_df = grouped_df.pivot_table(index='thread_no', columns=['res', 'omp_schedule'], values='time')

    # Reset the index
    pivot_df.reset_index(inplace=True)

    # Convert the DataFrame to integers
    pivot_df = pivot_df.astype(int)

    # Convert the DataFrame to a LaTeX table
    latex_table = pivot_df.to_latex(index=False, multirow=True)

    print(latex_table)

def float_double(df):
    # Filter the DataFrame
    filtered_df = df[(df['omp_schedule'] == 'dynamic') & (df['fma'] == True)]

    # Group by 'res', 'thread_no', and 'ftype' and calculate the average of 'time'
    grouped_df = filtered_df.groupby(['res', 'thread_no', 'ftype'])['time'].mean().reset_index()

    # Pivot the DataFrame
    pivot_df = grouped_df.pivot_table(index='thread_no', columns=['res', 'ftype'], values='time')

    # Reset the index
    pivot_df.reset_index(inplace=True)

    # Convert the DataFrame to integers
    pivot_df = pivot_df.astype(int)

    # Convert the DataFrame to a LaTeX table
    latex_table = pivot_df.to_latex(index=False, multirow=True)

    print(latex_table)

data_cpu = pd.read_csv('../report/data_cpu.csv')
data_cpu_vect = pd.read_csv('../report/data_cpu_vect.csv')


# static_dynamic(data_cpu)
float_double(data_cpu_vect)
