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

def fma(data_cpu, data_cpu_vect):
    # Filter the data
    data_cpu = data_cpu[(data_cpu['thread_no'] == 1) & (data_cpu['omp_schedule'] == 'dynamic')]
    data_cpu_vect = data_cpu_vect[(data_cpu_vect['thread_no'] == 1) & (data_cpu_vect['omp_schedule'] == 'dynamic') & (data_cpu_vect['ftype'] == 'double')]

    # Group the data and calculate the mean of time
    grouped_cpu = data_cpu.groupby('res')['time'].mean()
    grouped_cpu_vect = data_cpu_vect.groupby(['res', 'fma'])['time'].mean().unstack()

    # Merge the two grouped dataframes on res
    merged = pd.merge(grouped_cpu, grouped_cpu_vect, on='res')

    merged = merged.astype(int)

    # Convert the dataframe to a LaTeX table
    latex_table = merged.to_latex()

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
    latex_table = output.to_latex(float_format="%.2f")

    print(latex_table)

def vect_vs_notvect(data_cpu, data_cpu_vect):
    # Filter the data
    data_cpu = data_cpu[(data_cpu['omp_schedule'] == 'dynamic')][['res', 'thread_no', 'time']]
    data_cpu_vect = data_cpu_vect[(data_cpu_vect['omp_schedule'] == 'dynamic') & (data_cpu_vect['ftype'] == 'double') & (data_cpu_vect['fma'] == True)][['res', 'thread_no', 'time']]
    data_cpu['type'] = 'Not Vect'
    data_cpu_vect['type'] = 'Vect'

    data = pd.concat([data_cpu, data_cpu_vect])


    # Group the data and calculate the mean of time
    data = data.groupby(['res', 'thread_no', 'type'])['time'].mean().reset_index()
    
    pivot_df = data.pivot_table(index='thread_no', columns=['res', 'type'], values='time')

# Reset the index
    pivot_df.reset_index(inplace=True)

    # Convert the DataFrame to integers
    pivot_df = pivot_df.astype(int)

    # Convert the DataFrame to a LaTeX table
    latex_table = pivot_df.to_latex(index=False, multirow=True)

    print(latex_table)


def vect_ratio(data_cpu, data_cpu_vect):
    # Filter the data
    data_cpu = data_cpu[(data_cpu['omp_schedule'] == 'dynamic')][['res', 'thread_no', 'time']]
    data_cpu_vect = data_cpu_vect[(data_cpu_vect['omp_schedule'] == 'dynamic') & (data_cpu_vect['ftype'] == 'double') & (data_cpu_vect['fma'] == True)][['res', 'thread_no', 'time']]

    grouped_cpu = data_cpu.groupby(['res', 'thread_no'])['time'].mean()
    grouped_cpu_vect = data_cpu_vect.groupby(['res', 'thread_no'])['time'].mean()

    merged = pd.merge(grouped_cpu_vect.reset_index(), grouped_cpu.reset_index(), on=['res', 'thread_no'], suffixes=(' Vect', ' Not Vect'))
    merged['ratio'] = (merged['time Not Vect'] / merged['time Vect']) * 100
    merged = merged[['res', 'thread_no', 'ratio']]

    pivot_df = merged.pivot_table(index='res', columns=['thread_no'], values='ratio')

# Reset the index
    pivot_df.reset_index(inplace=True)


    latex_table = pivot_df.to_latex(index=False, multirow=True, float_format="%.2f" )

    print(latex_table)

def draw_result(data_cpu):
    # Group the data and calculate the mean of time
    grouped_cpu = data_cpu.groupby(['res', 'thread_no'])['time'].mean().reset_index()

    # Calculate the speedup
    grouped_cpu["speedup"] = grouped_cpu.apply(
        lambda row: grouped_cpu[(grouped_cpu["res"] == row["res"]) & (grouped_cpu["thread_no"] == 1)][
            "time"
        ].iloc[0]
        / row["time"],
        axis=1,
    )
    grouped_cpu["efficiency"] = grouped_cpu["speedup"] / grouped_cpu["thread_no"]


    # Convert the dataframe to a LaTeX table
    latex_table = grouped_cpu.to_latex(index=False, float_format="%.2f" )
    print(latex_table)

def result(data_cpu):
    # Filter the data
    data_cpu = data_cpu[(data_cpu['omp_schedule'] == 'dynamic')]
    draw_result(data_cpu)

def result_vect(data_cpu):
        # Filter the data
    data_cpu = data_cpu[(data_cpu['omp_schedule'] == 'dynamic') & (data_cpu['ftype'] == 'double') & (data_cpu['fma'] == True)]
    draw_result(data_cpu)

def time_gpu(df):
    df = df[(df['ftype'] == 'double')]
    df = df.groupby(['resolution', 'thread_x', 'thread_y'])['time_gpu'].mean().reset_index()
    df = df[['resolution', 'thread_x', 'thread_y', 'time_gpu']]
    df = df.astype(int)

    latex_table = df.to_latex(index=False )
    print(latex_table)

data_cpu = pd.read_csv('../report/data_cpu.csv')
data_cpu_vect = pd.read_csv('../report/data_cpu_vect.csv')
data_gpu = pd.read_csv('../report/data_gpu.csv')

#static_dynamic(data_cpu)
#float_double(data_cpu_vect)
#fma(data_cpu, data_cpu_vect)
#fma_ratio(data_cpu, data_cpu_vect)
#vect_vs_notvect(data_cpu, data_cpu_vect)
#vect_ratio(data_cpu, data_cpu_vect)
#result(data_cpu)
#result_vect(data_cpu_vect)
time_gpu(data_gpu)