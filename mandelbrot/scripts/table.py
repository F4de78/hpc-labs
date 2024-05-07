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

def fma(df):
    # Filter the DataFrame
    filtered_df = df[(df['omp_schedule'] == 'dynamic') & (df['ftype'] == 'float')]

    # Group by 'res', 'thread_no', and 'fma' and calculate the average of 'time'
    grouped_df = filtered_df.groupby(['res', 'thread_no', 'fma'])['time'].mean().reset_index()

    # Pivot the DataFrame
    pivot_df = grouped_df.pivot_table(index='thread_no', columns=['res', 'fma'], values='time')

    # Reset the index
    pivot_df.reset_index(inplace=True)

    # Convert the DataFrame to integers
    pivot_df = pivot_df.astype(int)

    # Convert the DataFrame to a LaTeX table
    latex_table = pivot_df.to_latex(index=False, multirow=True)

    print(latex_table)

def fma_ratio(data_cpu, data_cpu_vect):
    # Filter the data
    # Filter the data
    data_cpu = data_cpu[(data_cpu['thread_no'] == 1) & (data_cpu['omp_schedule'] == 'dynamic')]
    data_cpu_vect = data_cpu_vect[(data_cpu_vect['thread_no'] == 1) & (data_cpu_vect['omp_schedule'] == 'dynamic') & (data_cpu_vect['ftype'] == 'double')]

    # Group the data and calculate the mean of time
    grouped_cpu = data_cpu.groupby('res')['time'].mean()
    grouped_cpu_vect = data_cpu_vect.groupby(['res', 'fma'])['time'].mean().unstack()

    # Merge the two grouped dataframes on res
    merged = pd.merge(grouped_cpu, grouped_cpu_vect, on='res')

    # Calculate the ratio
    merged['with fma'] = (merged['time'] / merged[True]) * 100
    merged['without fma'] = (merged['time'] / merged[False]) * 100

    # Create a new dataframe with res, with fma and without fma columns
    output = merged[['with fma', 'without fma']]

    # Convert the dataframe to a LaTeX table
    latex_table = output.to_latex()

    print(latex_table)


data_cpu = pd.read_csv('../report/data_cpu.csv')
data_cpu_vect = pd.read_csv('../report/data_cpu_vect.csv')


# static_dynamic(data_cpu)
#float_double(data_cpu_vect)
#fma(data_cpu_vect)
fma_ratio(data_cpu, data_cpu_vect)