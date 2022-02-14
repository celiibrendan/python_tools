"""
Purpose: To make pandas table manipulation easier
"""

"""
Some useful functions: 
#sets the index to a specific column and doesn't return dataframe but modifies the existing one
df.set_index('Mountain', inplace=True) 

Selecting Data: 
i) selecting columns
- all columns are attribtues so can select with the "." (Ex: df.myCol)
- if there are wierd spaces could do getattr(df, 'Height (m)')
- BEST WAY: df['Height (m)'] because can select multiple columns at a time:
        df[['Height (m)', 'Range', 'Coordinates']]

ii) Selecting Rows (with slicing): 
- Can do that with index: a[start:stop:step]  (Ex: df[2:8:2])
- if you changed he index to be a certain column with non-numeric values: df['Lhotse':'Manaslu']
        slicing is inclusive at both start and end

iii) Specific data points: 
a) ** df.iloc** When just want to use numbers to reference
- df.iloc[rows, columns] for rows/col it can be: single int, list of ints, slices, : (for all)
  Ex: df.iloc[:, 2:6]** when 
  
b) ** df.loc where can use the names of things and not just numbers**
- df.loc[rows,columns]
   rows: index label, list of index labels, slice of index labels,:
   cols; singl column name, list of col names, slice of col names, :
   --> remember if do slice then it is inclusive on both start and stop
   
Ex: df.loc[:,'Height (m)':'First ascent']


c) Boolean selection: 
- can select rows with true/false mask--> 1) Create true false mask, put inside df[ ]
Ex: df[df['Height (m)'] > 8000]

For putting multiple conditions together the operators are: &,|,~

Have to use parenthesis to seperate multiple conditions: 
df[(df['Height (m)'] > 8000) & (df['Range']=='Mahalangur Himalaya')]

- Can use the loc operator to apply the mask and then select subset of columns: 
df.loc[(df['Height (m)'] > 8000) & (df['Range']=='Mahalangur Himalaya'), 'Height (m)':'Range']

Can also select the columns using a boolean operator: 
- col_criteria = [True, False, False, False, True, True, False]
  df.loc[df['Height (m)'] > 8000, col_criteria]
  
  
- To delete a column:
del neuron_df["random_value"]




------------------------------------pd.eval, df.eval df.query ------------------------------
Purpose: All of these functions are used to either
1) create masks of your rows
2) filter for specific rows 
3) make new data columns

pd.query:
- Can reference other dataframes by name and their columns with the attribute "."
pd.eval("df1.A + df2.A")   # Valid, returns a pd.Series object
pd.eval("abs(df1) ** .5")  # Valid, returns a pd.DataFrame object

- can evaluate conditional expressions: 
pd.eval("df1 > df2")        
pd.eval("df1 > 5")    
pd.eval("df1 < df2 and df3 < df4")      
pd.eval("df1 in [1, 2, 3]")
pd.eval("1 < 2 < 3")


Arguments that are specific:
- can use & or and (same thing)

** parser = "python" or "pandas" **
pandas: evaluates some Order of Operations differently
> is higher proirity than &
== is same thing as in  Ex: pd.eval("df1 in [1, 2, 3]") same as pd.eval("df1 == [1, 2, 3]")

python: if want traditional rules


** engine = "numexpr" or "python" ***

python: 
1) can do more inside your expressions but it is not as fast
Example: 
df = pd.DataFrame({'A': ['abc', 'def', 'abacus']})
pd.eval('df.A.str.contains("ab")', engine='python')

2) can reference variables with dictionary like syntax (not worth it)



---------- things can do with pd.eval -----------
1) Pass in dictionary to define variables that not defined 
        (otherwise uses global variable with same name)

pd.eval("df1 > thresh", local_dict={'thresh': 10})


---------- things can do with pd.eval -----------
1) only have to write column names in queries because only applied
to one dataframe so don't need to put name in front

df1.eval("A + B")

2) Have to put @ in front of variables to avoid confusion with column names
A = 5
df1.eval("A > @A") 


3) Can do multiline queries and assignments:

df1.eval('''
E = A + B
F = @df2.A + @df2.B
G = E >= F
''')

Can still do the local dict:
returned_df.query("n_faces_branch > @x",local_dict=dict(x=10000))

----------- Difference between df1.eval and df1.query -----------
if you are returning a True/False test, then df1.eval will just
return the True/False array whereas df1.query will go one step further
and restrict the dataframe to only those rows that are true

AKA: df1.eval is an intermediate step of df1.query 
(could use the df1.eval output to restrict rows by df1[output_eval])


---------------------------Examples--------------------------

Ex_1: How to check if inside a list
list_of_faces = [1038,5763,7063,11405]
returned_df.query("n_faces_branch in @list_of_faces",local_dict=dict(list_of_faces=list_of_faces))

Ex_2: Adding Ands/Ors

list_of_faces = [1038,5763,7063,11405]
branch_threshold = 31000
returned_df.query("n_faces_branch in @list_of_faces or skeleton_distance_branch > @branch_threshold",
                  local_dict=dict(list_of_faces=list_of_faces,branch_threshold=branch_threshold))
                  
Ex 2: of how to restrict a column to being a member or not being in a list
cell_df.query("not segment_id in @error_segments",local_dict=dict(error_seegments=error_segments))


--- 5/4 -----
How to query for null values: 
df.query('value < 10 | value.isnull()', engine='python')



--- 6/14: Review of how to check if in list -------

df = pd.DataFrame({"a":[1,2,3,4],"b":[2,3,4,5]})
curr_list = [1,2]
df.query("a in @my_list",
        local_dict = dict(my_list=curr_list))
        
        
-- 12/8 : how to modify something in place using index and column

idx_to_change = df.query("axon == 0").index
df.loc[idx_to_change,"synapse_density"] = df.loc[idx_to_change,"synapse_density"]*df.loc[idx_to_change,"n_synapses_post"] / df.loc[idx_to_change,"n_synapses"]
df.loc[idx_to_change,"n_synapses"] =  df.loc[idx_to_change,"n_synapses_post"]
df.loc[idx_to_change,"n_synapses_pre"]  =  0
df.loc[idx_to_change,"synapse_density_pre"]  =  0


"""
pd_source = "pandas"

from pandas import util

def random_dataframe():
    return util.testing.makeDataFrame()

def random_dataframe_with_missing_data():
    util.testing.makeMissingDataframe()
    
def dataframe_to_row_dicts(df):
    return df.to_dict(orient='records')

def nans_in_column(df):
    return pd.isnull(df).any()

def n_nans_per_column(df):
    return df.isnull().sum()

def n_nans_total(df):
    return df.isnull().sum().sum()

def surpress_scientific_notation():
    pd.set_option('display.float_format', lambda x: '%.3f' % x)
    
import pandas as pd
import pandasql

def set_pd_from_modin():
    """
    This library supposedly speeds up pandas functions
    by using multiple cores at once (made some things longer tho...)
    """
    global pd
    import modin.pandas as pd_modin
    pd = pd_modin
    
def set_pd_from_pandas():
    global pd
    import pandas as pdu
    pd = pdu

def restrict_pandas(df,index_restriction=[],column_restriction=[],value_restriction=""):
    """
    Pseudocode:
    How to specify:
    1) restrict rows by value (being equal,less than or greater) --> just parse the string, SO CAN INCLUDE AND
    2) Columns you want to keep
    3) Indexes you want to keep:
    
    Example: 
    
    index_restriction = ["n=50","p=0.25","erdos_renyi_random_location_n=100_p=0.10"]
    column_restriction = ["size_maximum_clique","n_triangles"]
    value_restriction = "transitivity > 0.3 AND size_maximum_clique < 9 "
    returned_df = restrict_pandas(df,index_restriction,column_restriction,value_restriction)
    returned_df
    
    Example of another restriction = "(transitivity > 0.1 AND n_maximal_cliques > 10) OR (min_weighted_vertex_cover_len = 18 AND size_maximum_clique = 2)"
    
    
    #how to restrict by certain value in a column being a list 
    df[~df['stn'].isin(remove_list)]
    """
    new_df = df.copy()
    
    
    if len(index_restriction) > 0:
        list_of_indexes = list(new_df[graph_name])
        restricted_rows = [k for k in list_of_indexes if len([j for j in index_restriction if j in k]) > 0]
        #print("restricted_rows = " + str(restricted_rows))
        new_df = new_df.loc[new_df[graph_name].isin(restricted_rows)]
        
    #do the sql string from function:
    if len(value_restriction)>0:
        s = ("SELECT * "
            "FROM new_df WHERE "
            + value_restriction + ";")
        
        #print("s = " + str(s))
        new_df = pandasql.sqldf(s, locals())
        
    #print(new_df)
    
    #restrict by the columns:
    if len(column_restriction) > 0:
        #column_restriction.insert(0,graph_name)
        new_df = new_df[column_restriction]
    
    return new_df

import re
def rewrite_sql_functions_in_query(query,
                                  function_names = None,
                                   verbose = False,
                                   **kwargs
                                  ):
    """
    Purpose: To replace a sql keyword function
    inside a query so it will work with sql querying
    """
    def convert_func(match_obj):
        return f"(SELECT {match_obj.group(1).upper()}({match_obj.group(2)}) FROM df)"
    
    if function_names is None:
        function_names = ["MAX","MIN"]
        
    for func_name in function_names:
        if verbose:
            print(f"\n---Working on {func_name}---")
        
        if verbose:
            print(f"before replace:\n {query}")
            
        sql_pattern = re.compile(fr"({func_name}|{func_name.lower()}|{func_name.upper()})\(([A-Za-z0-9_\s]+)\)")
        query = sql_pattern.sub(convert_func,query)
        
        if verbose:
            print(f"after replace:\n {query}")
            
    return query
        
    
    
        
    
def query(df,query,**kwargs):
    """
    PUrpose: To query a dataframe using an query 
    that would work with sql
    
    Ex:
    import pandas_utils as pu
    import pandas as pd

    curr_dicts = [dict(x = 5,y=10),dict(x = 7,y=11)]
    df = pd.DataFrame.from_records(curr_dicts)
    s = "(x == MAX( x )) or (y = min(y))"

    #s = pu.rewrite_sql_functions_in_query(s)
    pu.query(df,s)
    """
    try:
        index_name = "xyzilij"

        s = ("SELECT * "
            "FROM df WHERE "
            + query + ";")
        s_cp = s
        s = pu.rewrite_sql_functions_in_query(s,**kwargs)

        df_orig = df.copy()
        df[index_name] = df.index
        df = pu.filter_away_columns_by_data_type(df)

        new_df = pandasql.sqldf(s, locals())
        if len(new_df[index_name]) == 0:
            return df_orig.iloc[[],:]
        return df_orig.iloc[new_df[index_name],:]
    except:
        return df.query(query)
    

def turn_off_scientific_notation(n_decimal_places=3):
    pd.set_option('display.float_format', lambda x: '%.0f' % x)
    
def find_all_rows_with_nan(df,return_indexes=True,return_non_nan_rows=False):
    if return_indexes:
        if return_non_nan_rows:
            return np.where(~df.isna().any(axis=1))[0]
        else:
            return np.where(df.isna().any(axis=1))[0]
    else:
        if return_non_nan_rows:
            return df[~df.isna().any(axis=1)]
        else:
            return df[df.isna().any(axis=1)]
    
def filter_away_nan_rows(df):
    return df[~(df.isna().any(axis=1))]
    
from IPython.display import display
def display_df(df):
    display(df)
    
def dicts_to_dataframe(list_of_dicts):
    return pd.DataFrame.from_dict(list_of_dicts)

def rename_columns(df,columns_name_map):
    return df.rename(columns=columns_name_map)

def unique_rows(df,columns=None):
    return df.drop_duplicates(subset = columns)

def delete_columns(df,columns_to_delete):
    columns_to_delete = [k for k in columns_to_delete if k in df.columns]
    if len(columns_to_delete) > 0:
        return df.drop(columns=columns_to_delete)
    else:
        return df
    
# ----------- 1/25 Additon: Used for helping with clustering ----------- #
import numpy_utils as nu
import matplotlib.pyplot as plt
import numpy as np

def divide_dataframe_by_column_value(df,
                                column,
                                ):
    """
    Purpose: To divide up the dataframe into 
    multiple dataframes
    
    Ex: 
    divide_dataframe_by_column_value(non_error_cell,
                                column="cell_type_predicted")
    
    """
    tables = []
    table_names = []
    for b,x in df.groupby(column):
        table_names.append(b)
        tables.append(x)
        
    return tables,table_names


def plot_histogram_of_differnt_tables_overlayed(tables_to_plot,
                          tables_labels,
                          columns=None,
                          fig_title=None,
                           fig_width=18.5,
                            fig_height = 10.5,
                            n_plots_per_row = 4,
                            n_bins=50,
                            alpha=0.4,
                                           density=False):
    """
    Purpose: Will take multiple
    tables that all have the same stats and to 
    overlay plot them
    
    Ex: plot_histogram_of_differnt_tables_overlayed(non_error_cell,"total",columns=stats_proj)
    
    """
    if not nu.is_array_like(tables_to_plot):
        tables_to_plot = [tables_to_plot]
        
    if not nu.is_array_like(tables_labels):
        tables_labels = [tables_labels]
    
    ex_table = tables_to_plot[0]
    
    if columns is None:
        columns = list(cell_df.columns)
        
    n_rows = int(np.ceil(len(columns)/n_plots_per_row))
    
    fig,axes = plt.subplots(n_rows,n_plots_per_row)
    fig.set_size_inches(fig_width, fig_height)
    fig.tight_layout()
    
    if not fig_title is None:
        fig.title(fig_title)

    
    for j,col_title in enumerate(columns):
        
        row = np.floor(j/4).astype("int")
        column = j - row*4
        ax = axes[row,column]
        ax.set_title(col_title)
        
        for curr_table,curr_table_name in zip(tables_to_plot,tables_labels):
            curr_data = curr_table[col_title].to_numpy()
            ax.hist(curr_data,bins=n_bins,label=curr_table_name,alpha=alpha,
                    density=density)
            
        ax.legend()
        
def plot_histograms_by_grouping(df,
                               column_for_grouping,
                               **kwargs):
    
    dfs,df_names = divide_dataframe_by_column_value(df,
                                column=column_for_grouping,
                                                   )
    
    plot_histogram_of_differnt_tables_overlayed(tables_to_plot=dfs,
                                               tables_labels=df_names,
                                               **kwargs)
def new_column_from_row_function(df,row_function):
    """
    Purpose: To create a new column where each 
    row element is a function of the other rows
    
    Ex:
    def synapse_double(row):
        return row["synapse_id"]*2

    new_column_from_row_function(proofreading_synapse_df,synapse_double)
    """
    return df.apply(lambda row: row_function(row), axis=1)


def reset_index(df):
    return df.reset_index(drop=True)
    

import numpy as np
import matplotlib.pyplot as plt
import six

def df_to_render_table(data, col_width=3.0, row_height=0.625, font_size=14,
                     header_color='#40466e', row_colors=['#f1f1f2', 'w'], edge_color='w',
                     bbox=[0, 0, 1, 1], header_columns=0,
                       fontsize_header=None,
                     ax=None,transpose=True,**kwargs):
    """
    Purpose: To render a dataframe nicely that can be put in a figure
    
    Ex:
    df = pd.DataFrame()
    df['date'] = ['2016-04-01', '2016-04-02', '2016-04-03']
    df['calories'] = [2200, 2100, 1500]
    df['sleep hours'] = [2200, 2100, 1500]
    df['gym'] = [True, False, False]

    
    
    df_to_render_table(df, header_columns=0, col_width=2.0)
    """
    if transpose:
        data = data.transpose()
    
    if ax is None:
        size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array([col_width, row_height])
        fig, ax = plt.subplots(figsize=size)
        ax.axis('off')

    if not transpose:
        mpl_table = ax.table(cellText=data.values, bbox=bbox, colLabels=data.columns, **kwargs)
    else:
        mpl_table = ax.table(cellText=data.values, bbox=bbox, rowLabels=data.index, **kwargs)

    mpl_table.auto_set_font_size(False)
    mpl_table.set_fontsize(font_size)

    for k, cell in  six.iteritems(mpl_table._cells):
        cell.set_edgecolor(edge_color)
        if k[0] == 0 or k[1] < header_columns:
            cell.set_text_props(weight='bold', color='w',fontsize=fontsize_header)
            cell.set_facecolor(header_color)
        else:
            cell.set_facecolor(row_colors[k[0]%len(row_colors) ])
    return ax

def example_df_to_render_table(transpose=False):
    df = pd.DataFrame()
    df["index_name"] = ["stat 1","stat 2","stat 3"]
    df['date'] = ['2016-04-01', '2016-04-02', '2016-04-03']
    df['calories'] = [2200, 2100, 1500]
    df['sleep hours'] = [2200, 2100, 1500]
    df['gym'] = [True, False, False]

    return df_to_render_table(df, header_columns=0, col_width=2.0)

from pathlib import Path
def save_df(df,filename):
    filename = Path(filename)
    filename_str = str(filename.absolute())
    if filename_str[:-4] != ".pkl":
        filename_str += ".pkl"
    
    df.to_pickle(filename)  
    
def read_pickle(filepath):
    return pd.read_pickle(filepath)

def concat(df_list):
    return pd.concat(df_list)

from pathlib import Path
def df_to_csv(df,
              output_filename="df.csv",
              output_folder = "./",
              file_suffix = ".csv",
            output_filepath = None,
             verbose = False,
             return_filepath = True,
              compression = "infer",
             index = True,):
    """
    Purpose: To export a dataframe as a csv
    file
    """
    if output_filepath is None:
        output_folder = Path(output_folder)
        output_filename = Path(output_filename)
        output_filepath = output_folder / output_filename

    output_filepath = Path(output_filepath)
    
    if str(output_filepath.suffix) != file_suffix:
            output_filepath = Path(str(output_filepath) + file_suffix)
    
    output_path = str(output_filepath.absolute())
    if verbose: 
        print(f"Output path: {output_path}")
        
    df.to_csv(str(output_filepath.absolute()), sep=',',index=index,compression=compression)
    
    if return_filepath:
        return output_path

def df_to_gzip(df,
              output_filename="df.gzip",
              output_folder = "./",
            output_filepath = None,
             verbose = False,
             return_filepath = True,
             index = False,):
    """
    Purpose: Save off a compressed version of dataframe
    (usually 1/3 of the size)
    
    """
    return df_to_csv(df,
              output_filename=output_filename,
              output_folder = output_folder,
              file_suffix = ".gzip",
            output_filepath = output_filepath,
             verbose = verbose,
             return_filepath = return_filepath,
              compression = "gzip",
             index = index,)

def gzip_to_df(filepath):
    return pd.read_csv(filepath,
                       compression='gzip', header=0, sep=',', quotechar='"', error_bad_lines=False)

    
import numpy as np
def filter_away_columns(df,
                       column_list):
    """
    Purpose: To filter away certain columns from
    a dataframe
    
    Ex: 
    
    filter_away_columns(proof_with_nucl,
                       ["id_x","pt_position_x"])
    """
    total_columns = list(df.columns)
    final_columns = np.setdiff1d(total_columns,column_list)
    return df[final_columns]


def csv_to_df(csv_filepath):
    return pd.read_csv(csv_filepath) 

def json_to_df(filepath,lines=True):
    return pd.read_json(filepath,lines=lines) 

def extract_arrays_from_df(df,column_names="closest_sk_coordinate",dtype="float",n_cols=3):
    #return np.array([np.array(k,dtype=dtype) for k in df["closest_sk_coordinate"].to_numpy()]).reshape(-1,n_cols)
    if nu.is_array_like(column_names):
        n_cols = len(column_names)
    return np.array([np.array(k,dtype=dtype) for k in df[column_names].to_numpy()]).reshape(-1,n_cols)

def extract_inividual_columns_from_df(df,column_names,dtype="float"):
    return extract_arrays_from_df(df,column_names=column_names,dtype=dtype).T

def df_to_list(df,return_tuples = False):
    vals = df.values.tolist()
    if return_tuples:
        vals = [tuple(k) for k in vals]
    return vals

def columns_values_from_df(df,columns,as_array=True):
    """
    Will return the values of columns as seperate variables 
    """
    return [df[k].to_list() if not as_array else df[k].to_numpy() for k in columns]

def datatypes_of_columns(df):
    return auto_proof_df.dtypes

def memory_usage_of_columns(df):
    return df.memory_usage(deep=True)

def add_prefix_to_columns(df,prefix):
    return df.add_prefix(prefix)

def df_from_dict_key_values_columns(data_dict,
                                   columns_names = ("attribute","description")):
    edge_df = pd.DataFrame.from_records([list(data_dict.keys()),
                          list(data_dict.values())]).transpose()
    edge_df.columns = columns_names
    return edge_df

def set_pd_max_row_col(max_rows = None,max_cols=None):
    pd.set_option('display.max_rows', max_rows)
    pd.set_option('display.max_columns', max_cols)
    
def set_pd_display_no_truncate():
    pu.set_pd_max_row_col()
    
def reset_pd_display():
    pd.reset_option('display.max_rows')
    pd.reset_option('display.max_columns')
    pd.reset_option('display.width')
    pd.reset_option('display.float_format')
    pd.reset_option('display.max_colwidth')
    
from tqdm_utils import tqdm
def flatten_nested_dict_df_slow(df):
    """
    Purpose: Will faltten a dataframe if columns contain nested dicts
    """
    dicts = pu.dataframe_to_row_dicts(df)
    dicts_flattened = []
    for k in tqdm(dicts):
        curr_flat = pd.json_normalize(k, sep='_').to_dict(orient='records')[0]
        dicts_flattened.append(curr_flat)
    return pd.DataFrame.from_records(dicts_flattened)

import time
import json
def flatten_nested_dict_df(df,verbose = False):
    st = time.time()
    json_struct = json.loads(df.to_json(orient="records"))    
    df_flat = pd.io.json.json_normalize(json_struct) #use pd.io.json
    if verbose:
        print(f"flattening df time: {time.time() - st}")
    return df_flat


def col_to_numeric_array(col=None,
                        df=None,
                        col_name = None):
    """
    Purpose: to output a column as a numeric array
    (will account for coersion)
    
    """
    if col is None:
        col = df[col_name]
    x = pd.to_numeric(col,errors='coerce').to_list()
    return x

from functools import reduce
def restrict_df_by_dict(df,dict_restriction,return_indexes=False):
    mask = reduce(lambda x,y: x & y, [df[k] == v for k,v in dict_restriction.items()])
    if return_indexes:
        return np.where(mask.to_numpy())[0]
    else:
        return df[mask]
    
def fillna(df,value=0):
    return df.fillna(value)


def filter_away_columns_by_data_type(df,data_type = "object"):
    return df.loc[:,df.columns[df.dtypes != data_type]]

import pandas_utils as pu