from matplotlib import colors
import numpy as np
import numpy_utils as nu
import pandas_utils as pu
"""
Notes on other functions: 
eventplot #will plot 1D data as lines, can stack multiple 1D events
-- if did a lot of these gives the characteristic neuron spikes
   all stacked on top of each other


matplot colors can be described with 
"C102" where C{number} --> there are only 10 possible colors
but the number can go as high as you want it just repeats after 10
Ex: C100  = C110

#How to set the figure size:
fig.set_size_inches(18.5, 10.5)

# not have the subplots run into each other
fig.tight_layout()




           


"""

graph_color_list = ["blue","green","red","cyan","magenta",
     "black","grey","midnightblue","pink","crimson",
     "orange","olive","sandybrown","tan","gold","palegreen",
    "darkslategray","cadetblue","brown","forestgreen"]
color_examples = dict(
blues = ["darkblue","royalblue", "lightsteelblue","aqua","royalblue"],
purples = ["indigo","plum"],
pinks = ["pink","deeppink","fuchsia"],
greens = ["greenyellow","yellowgreen","olivedrab","springgreen"],
oranges = ["peachpuff","orange",],
yellows = ["yellow","gold",],
browns = ["sandybrown","sienna","maroon"],
reds = ["coral","red","rosybrown"],
greys = ["silver","grey","black"],
)


def generate_random_color(print_flag=False,colors_to_omit=[]):
    if not nu.is_array_like(colors_to_omit):
        colors_to_omit = [colors_to_omit]
    current_color_list = [k for k in graph_color_list if k not in colors_to_omit]
    rand_color = np.random.choice(current_color_list,1)
    if print_flag:
        print(f"random color chosen = {rand_color}")
    return colors.to_rgba(rand_color[0])

def generate_unique_random_color_list(n_colors,print_flag=False,colors_to_omit=[]):
    total_colors = []
    
    for i in range(n_colors):
        found_color=False
        while not found_color:
            if not nu.is_array_like(colors_to_omit):
                colors_to_omit = [colors_to_omit]
            current_color_list = [k for k in graph_color_list if k not in colors_to_omit]
            rand_color = np.random.choice(current_color_list,1)
            if rand_color not in total_colors:
                if print_flag:
                    print(f"random color chosen = {rand_color}")
                total_colors.append(colors.to_rgba(rand_color[0]))
                found_color = True
    return total_colors
        
            
def generate_non_randon_named_color_list(n_colors,
                                        user_colors=[], #if user sends a prescribed list
                                        colors_to_omit=[],):
    """
    To generate a list of colors of a certain length 
    that is non-random
    
    """
    if n_colors <= 0:
        return []
    return mu.generate_color_list(n_colors = n_colors,
                                  user_colors=user_colors,
                                  colors_to_omit=colors_to_omit,
                      return_named_colors=True)

import numpy_utils as nu
def generate_color_list(
                        user_colors=[], #if user sends a prescribed list
                        n_colors=-1,
                        colors_to_omit=[],
                        alpha_level=0.2,
                        return_named_colors = False):
    """
    Can specify the number of colors that you want
    Can specify colors that you don't want
    accept what alpha you want
    
    Example of how to use
    colors_array = generate_color_list(colors_to_omit=["green"])
    """
    #print(f"user_colors = {user_colors}")
    # if user_colors is defined then use that 
    user_colors = nu.convert_to_array_like(user_colors)
    colors_to_omit = nu.convert_to_array_like(colors_to_omit)
    
    if len(user_colors)>0:
        current_color_list = user_colors
    else:
        current_color_list = graph_color_list.copy()
    
    #remove any colors that shouldn't belong
    current_color_list = [k for k in current_color_list if k not in colors_to_omit]
    
    #print(f"current_color_list = {current_color_list}")
    
    if len(current_color_list) < len(user_colors):
        raise Exception(f"one of the colors you specified was part of unallowed colors {colors_to_omit}for a skeleton (because reserved for main)")
    
    #make a list as long as we need
    if n_colors > 0:
        current_color_list = (current_color_list*np.ceil(n_colors/len(current_color_list)).astype("int"))[:n_colors]
    
    if return_named_colors:
        return current_color_list
    
    #print(f"current_color_list = {current_color_list}")
    #now turn the color names all into rgb
    color_list_rgb = np.array([colors.to_rgba(k) for k in current_color_list])
    
    #changing the alpha level to the prescribed value
    color_list_rgb[:,3] = alpha_level
    
    return color_list_rgb


    
#----------------------------- Functions that were made for new graph visualization ------------------- #

def color_to_rgb(color_str):
    """
    To turn a string of a color into an RGB value
    
    Ex: color_to_rgb("red")
    """
    if type(color_str) == str:
        return colors.to_rgb(color_str)
    else:
        return np.array(color_str)

def color_to_rgba(current_color,alpha=0.2):
    curr_rgb = color_to_rgb(current_color)
    return apply_alpha_to_color_list(curr_rgb,alpha=alpha)
    
from copy import copy
def get_graph_color_list():
    return copy(graph_color_list)

def generate_random_rgba(print_flag=False):
    rand_color = np.random.choice(graph_color_list,1)
    if print_flag:
        print(f"random color chosen = {rand_color}")
    return colors.to_rgb(rand_color[0])

import numpy_utils as nu
def generate_color_list_no_alpha_change(
                        user_colors=[], #if user sends a prescribed list
                        n_colors=-1,
                        colors_to_omit=[],
                        alpha_level=0.2):
    """
    Can specify the number of colors that you want
    Can specify colors that you don't want
    accept what alpha you want
    
    Example of how to use
    colors_array = generate_color_list(colors_to_omit=["green"])
    """
    if len(user_colors)>0:
        current_color_list = user_colors
    else:
        current_color_list = graph_color_list.copy()
    
    if len(colors_to_omit) > 0:
        colors_to_omit_converted = np.array([color_to_rgb(k) for k in colors_to_omit])
        #print(f"colors_to_omit_converted = {colors_to_omit_converted}")
        colors_to_omit_converted = colors_to_omit_converted[:,:3]

        #remove any colors that shouldn't belong
        colors_to_omit = []
        current_color_list = [k for k in current_color_list if len(nu.matching_rows(colors_to_omit_converted,k[:3])) == 0]
    
    #print(f"current_color_list = {current_color_list}")
    
    if len(current_color_list) == 0:
        raise Exception(f"No colors remaining in color list after colors_to_omit applied ({current_color_list})")
    
    #make a list as long as we need

    current_color_list = (current_color_list*np.ceil(n_colors/len(current_color_list)).astype("int"))[:n_colors]
    
    return current_color_list


def process_non_dict_color_input(color_input):
    """
    Will return a color list that is as long as n_items
    based on a diverse set of options for how to specify colors
    
    - string
    - list of strings
    - 1D np.array
    - list of strings and 1D np.array
    - list of 1D np.array or 2D np.array
    
    *Warning: This will not be alpha corrected*
    """
    
    if color_input == "random": #if just string that says random
        graph_color_list = get_graph_color_list()
        color_list = [color_to_rgb(k) for k in graph_color_list]
    elif type(color_input) == str: #if just give a string then turn into list with string
        color_list = [color_to_rgb(color_input)]
    elif all(type(elem)==str for elem in color_input): #if just list of strings
        color_list = [color_to_rgb(k) for k in color_input]
    elif any(nu.is_array_like(elem) for elem in color_input): #if there is an array in the list 
        color_list = [color_to_rgb(k) if type(k)==str else k for k in  color_input]
    else:
        color_list = [color_input]
    
    return color_list

def apply_alpha_to_color_list(color_list,alpha=0.2,print_flag=False):
    single_input = False
    if not nu.is_array_like(color_list):
        color_list = [color_list]
        single_input = True
    color_list_alpha_fixed = []
    
    for c in color_list:
        if len(c) == 3:
            color_list_alpha_fixed.append(np.concatenate([c,[alpha]]))
        elif len(c) == 4:
            color_list_alpha_fixed.append(c)
        else:
            raise Exception(f"Found color that was not 3 or 4 length array in colors list: {c}")
    if print_flag:
        print(f"color_list_alpha_fixed = {color_list_alpha_fixed}")
    
    if single_input:
        return color_list_alpha_fixed[0]
    
    return color_list_alpha_fixed



import webcolors
import numpy as np

def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

def get_colour_name(requested_colour):
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour(requested_colour)
        actual_name = None
    return actual_name, closest_name

def convert_rgb_to_name(rgb_value):
    """
    Example: convert_rgb_to_name(np.array([[1,0,0,0.5]]))
    """
    rgb_value = np.array(rgb_value)
    if not nu.is_array_like(rgb_value[0]):
        rgb_value = rgb_value.reshape(1,-1)
    
    #print(f"rgb_value.shape = {rgb_value.shape}")

    output_colors = []
    for k in rgb_value:
        if len(k) > 3:
            k = k[:3]
        adjusted_color_value = np.array(k)*255
        output_colors.append(get_colour_name(adjusted_color_value)[-1])
    
    if len(output_colors) == 1:
        return output_colors[0]
    elif len(output_colors) > 1:
        return output_colors
    else:
        raise Exception("len(output_colors) == 0")
        
def convert_dict_rgb_values_to_names(color_dict):
    """
    Purpose: To convert dictonary with colors as values to the color names
    instead of the rgb equivalents
    
    Application: can be used on the color dictionary returned by the 
    neuron plotting function
    
    Example: 
    import matplotlib_utils as mu
    mu = reload(mu)
    nviz=reload(nviz)


    returned_color_dict = nviz.visualize_neuron(uncompressed_neuron,
                                                visualize_type=["network"],
                                                network_resolution="branch",
                                                network_directional=True,
                                                network_soma=["S1","S0"],
                                                network_soma_color = ["black","red"],       
                                                limb_branch_dict=dict(L1="all",
                                                L2="all"),
                                                node_size = 1,
                                                arrow_size = 1,
                                                return_color_dict=True)
                                                
    color_info = mu.convert_dict_rgb_values_to_names(returned_color_dict)
    
    
    """
    return dict([(k,convert_rgb_to_name(v)) for k,v in color_dict.items()])
    

import matplotlib.pyplot as plt
from matplotlib import colors as mcolors

base_colors_dict = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)


def plot_color_dict(colors,sorted_names=None, 
                    hue_sort=False,
                    ncols = 4,
                    figure_width = 20,
                    figure_height = 8,
                   print_flag=True):

    """
    Ex: 
    
    #how to plot the base colors
    Examples: 
    mu.plot_color_dict(mu.base_colors_dict,figure_height=20)
    mu.plot_color_dict(mu.base_colors_dict,hue_sort=True,figure_height=20)
    
    How to plot colors returned from the plotting function:
    import matplotlib_utils as mu
    mu = reload(mu)
    nviz=reload(nviz)


    returned_color_dict = nviz.visualize_neuron(uncompressed_neuron,
                                                visualize_type=["network"],
                                                network_resolution="branch",
                                                network_directional=True,
                                                network_soma=["S1","S0"],
                                                network_soma_color = ["black","red"],       
                                                limb_branch_dict=dict(L1="all",
                                                L2="all"),
                                                node_size = 1,
                                                arrow_size = 1,
                                                return_color_dict=True)
                                                
    
    mu.plot_color_dict(returned_color_dict,hue_sort=False,figure_height=20)
    
    """
    if sorted_names is None:
        if hue_sort:
            # Sort colors by hue, saturation, value and then by name.
            by_hsv = sorted((tuple(mcolors.rgb_to_hsv(mcolors.to_rgba(color)[:3])), name)
                            for name, color in colors.items())
            #getting the names of the 
            sorted_names = [name for hsv, name in by_hsv]
        else:
            sorted_names = sorted(list(colors.keys()))
    n = len(sorted_names)
     #will always have 4 columns
    nrows = n // ncols + 1

    if print_flag:
        print(f"nrows = {nrows}")
        print(f"n-ncols*nrows = {n-ncols*nrows}")
    #creates figure
    fig, ax = plt.subplots(figsize=(figure_width, figure_height))

    # Get height and width
    X, Y = fig.get_dpi() * fig.get_size_inches()
    h = Y / (nrows + 1)
    w = X / ncols

    for i, name in enumerate(sorted_names):
        row = i % nrows
        col = i // nrows
        y = Y - (row * h) - h

        xi_line = w * (col + 0.05)
        xf_line = w * (col + 0.25)
        xi_text = w * (col + 0.3)

        ax.text(xi_text, y, name, fontsize=(h * 0.5),
                horizontalalignment='left',
                verticalalignment='center')

        ax.hlines(y + h * 0.1, xi_line, xf_line,
                  #gets the color by name
                  color=colors[name], linewidth=(h * 0.6)
                 #color=[1,0,0,1],linewidth=(h * 0.6)
                 )

    ax.set_xlim(0, X)
    ax.set_ylim(0, Y)
    ax.set_axis_off()

    fig.subplots_adjust(left=0, right=1,
                        top=1, bottom=0,
                        hspace=0, wspace=0)
    plt.show()
    
    
    
# -------------------- Generic Plotting functions --------------------

"""
Best Idea for concatenating plotting is to create the figure 
first and then to pass the figure to different functions
and one of the subaxes will be altered within function


"""

def get_axes_locations_from_figure(fig):
    return [[f.get_subplotspec().colspan.start,
             f.get_subplotspec().rowspan.start] for f in fig.get_children()[1:]]
def get_axes_layout_from_figure(fig):
    return np.max(np.array(get_axes_locations_from_figure(fig)),axis=0) + np.array([1,1])

# plotting the BIC curve
from matplotlib.ticker import MaxNLocator
def plot_graph(title,
                y_values,
                x_values,
                x_axis_label,
                y_axis_label,
              return_fig = False,
              figure = None,
              ax_index=None,
              label=None,
              x_axis_int=True):
    """
    Purpose: For easy plotting and concatenating plots
    """
    if figure is None:
        figure,ax = plt.subplots(1,1)
    else:
        ax = figure.axes[ax_index]
        return_fig = True
    
    
    ax.plot(x_values,y_values,label=label)
    ax.set_xlabel(x_axis_label)
    ax.set_ylabel(y_axis_label)
    ax.set_title(title)
    if not label is None:
        ax.legend()
        
    if x_axis_int:
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        
    if return_fig:
        plt.close()
        return figure
    else:
        plt.show()

import matplotlib
def color_to_hex(color):
    return matplotlib.colors.to_hex(color, keep_alpha=False)
        
from IPython.display import display
def display_figure(fig):
    display(fig)
    
# ---------- Helping with graph functions for network -------- #
def bins_from_width_range(bin_width,
                          bin_max,
                         bin_min=None):
    """
    To compute the width boundaries to help with 
    plotting and give a constant bin widht
    
    """
#     n_bins = (bin_max-bin_min)/bin_width
#     bins = np.arange(int(bin_min/bin_width),n_bins+1)*bin_width

    if bin_min is None:
        bin_min = 0
        
    return np.arange(bin_min,bin_max+0.00001,bin_width)


def histogram(data,
          n_bins=50,
          bin_width=None,
          bin_max=None,
          bin_min=None,
          density=False,
          logscale=False,
         return_fig_ax=True,
              fontsize_axes=20,
         **kwargs):
    """
    Ex: 
    histogram(in_degree,bin_max = 700,
         bin_width = 20,return_fig_ax=True)
    """
    
    if bin_width is not None and bin_max is not None:
        if bin_min is None:
            bin_min = 0
        bins=bins_from_width_range(bin_min =bin_min,
                                   bin_max=bin_max,
                                   bin_width=bin_width)
        
    else:
        bins=np.linspace(np.min(data),
                       np.max(data)+0.001,
                       n_bins)
        
    hist_heights,hist_bins = np.histogram(data, bins, density=density)

    x1 = hist_bins[:-1] #left edge
    x2 = hist_bins[1:] #right edge
    y = hist_heights
    w = np.array(x2) - np.array(x1) #variable width, can set this as a scalar also

    fig,ax = plt.subplots(1,1)
    ax.bar(x1, y, width=w, align='edge')

        
    ax.set_xlabel("Degree",fontsize=fontsize_axes)

    if not density:
        ax.set_ylabel("Count",fontsize=fontsize_axes)
    else:
        ax.set_ylabel("Density",fontsize=fontsize_axes)

    if logscale:
        ax.set_yscale("log")

    if not return_fig_ax:
        plt.show()
    else:
        return ax
    
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib
def reset_default_settings():
    mpl.rcParams.update(mpl.rcParamsDefault)
    
def set_font_size(font_size):
    
    font = {'family' : 'normal',
        #'weight' : 'bold',
        'size'   : 20}
    
    matplotlib.rc('font', **font)
    
    
def add_random_color_for_missing_labels_in_dict(labels,
                                                label_color_dict,
                                               verbose = False):
    """
    Purpose: Will generate random colors for labels that
    are missing in the labels dict
    """
    unique_labels  = np.unique(labels.astype("str"))
    
    curr_keys = list(label_color_dict.keys())
    curr_colors = list(label_color_dict.values())
    labels_with_no_color = np.setdiff1d(unique_labels,curr_keys)
    
    if verbose:
        print(f"unique_labels = {unique_labels}")
        print(f"labels_with_no_color = {labels_with_no_color}")
        
    new_label_colors = mu.generate_non_randon_named_color_list(
                                    n_colors = len(labels_with_no_color),
                                    colors_to_omit=curr_colors)
    return_dict = label_color_dict.copy()
    for lab,col in zip(labels_with_no_color,new_label_colors):
        return_dict[lab] = col
        
    return return_dict

def set_legend_outside_plot(
    ax,
    scale_down=0.8,
    bbox_to_anchor=(1, 0.5),
    loc='center left'):
    """
    Will adjust your axis so that the legend appears outside of the box
    """
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * scale_down, box.height])

    # Put a legend to the right of the current axis
    ax.legend(loc=loc, bbox_to_anchor=bbox_to_anchor)
    return ax
    
def scatter_2D_with_labels(
    X,
    Y,
    labels,
    label_color_dict = None,
    x_title = "",
    y_title = "",
    axis_append = "",
    Z = None,
    z_title = "",
    alpha = 0.5,
    verbose = False,
    move_legend_outside_plot = True,
    ):
    """
    Purpose: Will plot scatter points
    where each point has a unique label
    (and allows to specify the colors of each label)

    Pseudocode: 
    1) Find the unique labels
    2) For all unique labels, if a color mapping is not 
    specified then add a random unique color (use function)

    3) Iterate through the labels to plot: 
    a. Find all indices of that label
    b. Plot them with the correct color and label
    
    4) Move the legend to outside of the plot
    
    mu.scatter_2D_with_labels(
    X = np.concatenate([f1_inh,f1_exc]),
    Y = np.concatenate([f2_inh,f2_exc]),
    #Z = np.ones(194),
    x_title = feature_1,
    y_title = feature_2,
    axis_append = "(per um of skeleton)",
    labels = np.concatenate([class_inh,class_exc]),
    alpha = 0.5,
    label_color_dict= dict(BC = "blue",
                        BPC = "black",
                        MC = "yellow",
                        excitatory = "red"
                    ),
    verbose = True)
    """
    if Z is not None:
        Z = np.array(Z)
        projection_type = "3d"
    else:
        projection_type = None
        
    X = np.array(X)
    Y = np.array(Y)

    if label_color_dict is None:
        label_color_dict = dict()
        

    labels= np.array(labels).astype("str")
    unique_labels = np.unique(labels)
    color_dict_adj = mu.add_random_color_for_missing_labels_in_dict(labels,
                                               label_color_dict,
                                               verbose = verbose)

    #fig,ax = plt.subplots(1,1,projection_type=projection_type)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection = projection_type)
    
    for lab in unique_labels:
        lab_mask = labels == lab
        X_curr = X[lab_mask]
        Y_curr = Y[lab_mask]
        if Z is not None:
            Z_curr = Z[lab_mask] 
            ax.scatter(X_curr,Y_curr,Z_curr,c=color_dict_adj[lab],
                   label=lab,alpha = alpha)
        else:
            ax.scatter(X_curr,Y_curr,c=color_dict_adj[lab],
                   label=lab,alpha = alpha)

    ax.set_xlabel(f"{x_title} {axis_append}")
    ax.set_ylabel(f"{y_title} {axis_append}")
    if Z is not None:
        #ax.set_zlabel(f"{z_title} {axis_append}")
        ax.set_title(f"{z_title} vs {y_title} vs {x_title}")
    else:
        ax.set_title(f"{y_title} vs {x_title}")

    if move_legend_outside_plot:
        mu.set_legend_outside_plot(ax)
    else:
        ax.legend()

    plt.show()
    

try:
    from colour import Color
except:
    Color = None


import numpy as np
def divided_data_into_color_gradient(
    data,
    n_bins = 5,
    max_percentile = 98,
    min_percentile = 5,
    verbose = True,
    low_color = "red",
    high_color = "green",
    return_bin_spacing = True,):
    """
    Pseudocode: 
    1) Divide the data up into bins using digitize up to the kth percentile
    2) Create a color gradient for those number of bins
    3) Divide up the data into the bins
    """

    if max_percentile is not None:
        top_bin = np.percentile(data,max_percentile)
    else: 
        top_bin = np.max(data)

    if min_percentile is not None:
        low_bin = np.percentile(data,min_percentile)
    else: 
        low_bin = np.min(data)

    bin_spacing = np.linspace(low_bin,top_bin,n_bins-1)
    if verbose:
        print(f"low_bin = {low_bin}")
        print(f"top_bin = {top_bin}")
        print(f"bin_spacing (n_bins = {n_bins}) = {bin_spacing}")

    bin_spacing_to_return = np.hstack([bin_spacing,[np.max(data) + 1]])
    if verbose:
        print(f"bin_spacing_to_return = {bin_spacing_to_return}")

    col = Color(low_color)
    colors_dict = dict([(k,v.get_rgb()) for k,v in enumerate(list(col.range_to(Color(high_color),n_bins)))])

    if verbose:
        print(f"colors_dict= {colors_dict}")

    data_bin_idx = np.digitize(data,bin_spacing)
    data_as_bins = dict([(k,np.where(data_bin_idx==k)[0]) for k in np.unique(data_bin_idx)])

    if verbose:
        print(f"data_as_bins= {data_as_bins}")
        
    if return_bin_spacing:
        return data_as_bins,colors_dict,bin_spacing_to_return
    else:
        return data_as_bins,colors_dict
    
    
import matplotlib as mpl
import matplotlib.pyplot as plt
def color_mix(color_1,color_2,mix):
    c1=np.array(mpl.colors.to_rgb(color_1))
    c2=np.array(mpl.colors.to_rgb(color_2))
    return mpl.colors.to_rgb((1-mix)*c1 + mix*c2)

def color_transition(
    n,
    color_1="red",
    color_2="blue",
    plot = False):
    #fade (linear interpolate) from color c1 (at mix=0) to c2 (mix=1)
    c1=np.array(mpl.colors.to_rgb(color_1))
    c2=np.array(mpl.colors.to_rgb(color_2))
    total_colors = np.array([mpl.colors.to_rgb((1-mix)*c1 + mix*c2)
                             for mix in np.linspace(0,1,n)])
    
    if plot:
        fig, ax = plt.subplots(figsize=(8, 5))
        for x,c in enumerate(total_colors):
            ax.axvline(x, color=c, linewidth=4) 
        plt.show()
    
    return total_colors

import numpy_utils as nu
def text_overlay(
    ax,
    #dictionary mapping text to coordinate  
    text_to_plot_dict = None,
    #data so that can plot the mean of the coordinate
    X = None,
    y = None,
    
    #for text parameters:
    text_color = "black",
    backgroundcolor = "white",
    alpha = 0.5,
    fontsize = "small",#'xx-small', 'x-small', 'small', 'medium', 'large', 'x-large', 'xx-large'
    box_alpha = 0.8,
    box_edgecolor = "black",
    box_facecolor = "white",
    ):
    
    """
    Purpose: Will add a text to the plot
    """
    
#     print(f"text_color = {text_color}")
#     print(f"facecolor = {facecolor}")
#     print(f"alpha = {alpha}")
    
    if text_to_plot_dict is None:
        text_to_plot_dict = dict()
        for k in set(y):
            text_to_plot_dict[k] = k#X_proj[y==k,:3]
    
    for name, coord in text_to_plot_dict.items():
        if not nu.is_array_like(coord):

            coord = X[y==coord].mean(axis=0)
        #print(f"{name} coord = {coord}")

        try:
            ax_func = getattr(ax,"text3D")
            ndim = 3
        except:
            ax_func = ax.text
            ndim = 2
        

        ax_func(*coord[:ndim],
                  name,
                  horizontalalignment='center',
                  c = text_color,
                alpha = alpha,
                fontsize = fontsize,
                  bbox=dict(
                      alpha=box_alpha, 
                      edgecolor=box_edgecolor, 
                      facecolor=box_facecolor))
        
    return ax
        
        
import matplotlib_utils as mu
def stacked_bar_graph(
    df,
    x = "x",
    x_min = -np.inf,
    x_max = np.inf,
    verbose = False,
    width_scale = 1,
    figsize = (10,5),
    alpha = 0.5,
    color_dict = None,
    set_legend_outside_plot = False,
    plot_twin_counts = False,
    twin_color = "blue",
    labels = None,
    fontsize_axes = None,
    x_multiplier = 1,
    legend = True,
    ):
    """
    Purpose: Plot a stacked bar graph

    """
    df = df.query(f"({x} >= {x_min}) & ({x} <= {x_max})")
    fig,ax = plt.subplots(1,1,figsize = figsize)

    
    x_range = df[x].to_numpy()*x_multiplier
    
    if plot_twin_counts:
        ax3 = ax.twinx()  # instantiate a second axes that shares the same x-axis
        ax3.set_ylabel('Counts of Synpases',fontsize = fontsize_axes,color=twin_color)  # we already handled the x-label with ax1
        ax3.tick_params(axis='y', labelcolor=twin_color)
        ax3.plot(x_range, df["counts"].to_numpy(), color=twin_color)
        ax2 = ax
    else:
        ax2 = ax
        twin_color = None

    if labels is None:
        all_ys = np.array(df.columns)
        all_ys = all_ys[(all_ys != x) & (all_ys != "index") & 
                       (all_ys != "counts")]
    else:
        all_ys = labels

    if verbose:
        print(f"All labels = {all_ys}")

    if color_dict is None:
        colors = mu.generate_non_randon_named_color_list(len(all_ys))
        color_dict = {k:v for k,v in zip(all_ys,colors)}

    try:
        width = width_scale*(x_range[1] - x_range[0])
    except:
        width = 2
    
    previous_count = 0
    for lab in all_ys:
        if lab in df.columns:
            height = df[f"{lab}"].to_numpy()
        else:
            continue

        ax2.bar(x = x_range,
               height = height ,
                       bottom = previous_count,
                        label=lab,
                       alpha = alpha,
                       width = width,
                       color = color_dict.get(lab,None)
                       )

        previous_count += height

    if legend:
        ax2.legend()
    ax2.set_xlim([np.min(x_range),np.max(x_range)])
    ax2.set_ylim([0,np.max(previous_count)])
    ax2.tick_params(axis='y',)# labelcolor=twin_color)
        

    if set_legend_outside_plot:
        mu.set_legend_outside_plot(
            ax2,
            scale_down=0.8,
            bbox_to_anchor=(1.2, 0.5),
            loc='center left')

    return ax2,ax


  
import matplotlib.pyplot as plt
def bar_plot_parallel_features_by_labels(
    df,
    features,
    label,
    labels_to_plot = None,
    figsize = (20,6),
    verbose = True,
    normalize = True,
    stat_measures = ("count",),#["sum","mean"],
    width_buffer = 0.2,
    horizontal = True,
    title_append = None,
    ):
    """
    Purpose: To plot parallel bar plots
    of different labels

    Define measurement (sum or mean)

    for each stat measure:
    1) group by cell type and take a certain measurement
    2) For each cell type:
        - plot the barplot 

    Source Code: https://stackoverflow.com/questions/10369681/how-to-plot-bar-graphs-with-same-x-coordinates-side-by-side-dodged


    mu.bar_plot_parallel_features_by_labels(
        df_control,
        label = "gnn_cell_type_fine",
        #labels_to_plot = ctu.allen_cell_type_fine_classifier_labels,
        features = ["axon_skeletal_length","n_syn_valid_pre"],
        stat_measures = ("sum","mean"),
        figsize = (14,6),
        width_buffer = 0.2,
        title_append = f" in {hdju.source.title()} Volume",
        horizontal = True,)
    """
    fig,axes = plt.subplots(1,len(stat_measures),figsize=figsize)

    axes = nu.convert_to_array_like(axes)
    n_features = len(features)
    width = (1-width_buffer)/len(features)                       # With of each column
    
    if labels_to_plot is None:
        labels_to_plot = list(df[label].unique())
        
    if horizontal:
        plot_func= "barh"
        spacing_param = "height"
    else:
        plot_func = "bar"
        spacing_param = "width"
        
    for s,ax in zip(stat_measures,axes):
        ct = labels_to_plot
        df_grouped = getattr(df.groupby([label]),s)().reset_index()
        df_grouped = df_grouped.query(f"{label} in {ct}")
        x = np.arange(0, len(ct))   # Center position of group on x axis

        for j,f in enumerate(features):
            f_val_unordered = df_grouped[f].to_numpy()
            f_val_labels = df_grouped[label].to_numpy()
            
            f_val = f_val_unordered[nu.original_array_indices_of_elements(
                f_val_labels,
                ct,
            )]
            
            if normalize:
                f_val = f_val/np.sum(f_val)

            position = x + (width*(1-n_features)/2) + j*width

            kwargs = {spacing_param:width}
            getattr(ax,plot_func)(position,f_val,label=f,**kwargs)

        ax.legend()
        if not horizontal:
            ax.set_xlabel("Cell Type")
            ax.set_ylabel(f"{f}")
            ax.set_xticks(x)
            ax.set_xticklabels(ct)
        else:
            ax.set_ylabel("Cell Type")
            ax.set_xlabel(f"{f}")
            ax.set_yticks(x)
            ax.set_yticklabels(ct)
        
        title = f"Normalized Reconstruction {s.title()}" 
        #ax.axes.xticks(ct_index + width / 2, ct)
        if title_append is not None:
                title += f" \n {title_append}"
        ax.set_title(title)
        
        
def histograms_overlayed(
    df,
    column,
    hue=None,
    hue_order = None,
    hue_secondary = None,
    
    #histogram plot formatting
    bins = 50,
    density = False,
    alpha = 0.3,
    color_dict = None,
    default_color = "black",

    #formatting
    figsize = (10,5),
    fontsize = 20,
    
    xlabel= None,
    title = None,
    title_prefix = "",
    
    fontsize_title = 30,
    fontsize_legend = 15,
    
    verbose = False,
    include_mean_std_in_title = True,
    
    outlier_buffer = 1,
    same_axis = True,
    
    
    
    ):
    
    """
    Purpose: 
    To plot different histograms all overlayed
    
    import matplotlib_utils as mu
    mu.histograms_overlayed(
        coord_df,
        column="centroid_y_nm",
        hue="gnn_cell_type_fine")
    """
    
    if hue_secondary is not None:
        same_axis = False
    
    df= df.query(f"{column} == {column}")
    import numpy_utils as nu
    df = pu.filter_away_rows_with_nan_in_columns(
        df = df,
        columns = column,
        verbose=verbose,
    )
    
    if outlier_buffer is not None:
        df = pu.filter_df_by_column_percentile(
            df,
            columns=column,
            percentile_buffer=outlier_buffer,
        )
        
    
    
    if hue is not None:
        if hue_order is None:
            cats = df[hue].unique()
        else:
            cats = hue_order
    else:
        cats = [None]
        
    if hue_secondary is not None:
        cats_secondary = df[hue_secondary].unique()
    else:
        cats_secondary= None
        
    if same_axis:
        fig,ax = plt.subplots(1,1,figsize=figsize)
        axes = [None]*len(cats)
    else:
        new_fig_size = np.array(figsize)
        new_fig_size[1] = new_fig_size[1]*len(cats)
        fig,axes = plt.subplots(len(cats),1,figsize=new_fig_size,sharex=True)
        
    if xlabel is None:
        xlabel = column
        
            
    total_colors = []
    for cat,curr_ax in zip(cats,axes):
        if curr_ax is None:
            curr_ax = ax
        if cat is not None:
            curr_df = df.query(f"{hue} == '{cat}'")
            if len(curr_df) == 0:
                try:
                    curr_df = df.query(f"{hue} == {cat}")
                except:
                    continue
        else:
            curr_df = df
        
        #print(f"color_dict = {color_dict}")
        if color_dict is not None:
            color = color_dict.get(cat,default_color)
        else:
            color = None
            
        #print(f"Category = {cat}")
        #print(f"{cat} color = {np.unique(color)}")
        if cat is None:
            cat = "None"
            
        if hue_secondary is None:
            curr_ax.hist(curr_df[column],
                            density = density,
                             label = cat,
                            color = color,
                             bins=bins,
                            alpha = alpha,
                            #zorder=zorder
            )
        else:
            for c2 in cats_secondary:
                curr_query = f"{hue_secondary} == '{c2}'"
                #print(f"curr_query = {curr_query}")
                curr_df_local = curr_df.query(curr_query)
                
                #print(f"curr_df_local = {len(curr_df_local)}")
                curr_ax.hist(curr_df_local[column],
                            density = density,
                             label = c2,
                            #color = color,
                             bins=bins,
                            alpha = alpha,
                            #zorder=zorder
                )
        curr_ax.legend()
        
        curr_ax.set_xlabel(f"{xlabel}",fontsize = fontsize)
        total_colors.append(color)
        
        if density:
            curr_ax.set_ylabel("Density",fontsize=fontsize)
        else:
            curr_ax.set_ylabel("Frequency",fontsize = fontsize)
            
        curr_ax.legend()
        curr_ax.legend(loc="upper right", 
                  markerscale=2.,
                  scatterpoints=1, 
                  fontsize=fontsize_legend)
        
        title = f"{cat} ({len(curr_df)}  datapoints, mean = {curr_df[column].mean():.2f}, std = {curr_df[column].std():.2f})"
        print(title)
        
        if include_mean_std_in_title:
            curr_ax.set_title(title)
        
    #print(f"total_colors = {total_colors}")
    title = f"{title_prefix.title()}\n{column.title()} Distribution"
        
    if include_mean_std_in_title:
        title += f"\nMean = {np.round(df[column].mean(),2):.2f}, Std Dev = {np.round(df[column].std(),2):.2f}"

    if same_axis:
        ax.set_title(f"{title}",fontsize = fontsize_title)
        return ax
    else:
        #fig.suptitle(f"{title}",fontsize = fontsize_title)
        return axes
    
    
import seaborn as sns
import matplotlib.pyplot as plt
import pandas_utils as pu

def histogram_2D_overlayed(
    df,
    x,
    y,
    hue,
    hue_order=None,
    hue_secondary = None,
    xlim = None,
    ylim = None,
    same_axis = False,
    verbose = False
    ):
    """
    Purpose: To plot a joint plot for different attributes
    one after the other
    """
    
    import seaborn_ml as sml

    if hue_order is None:
        hue_order = df[hue].unique()

    if not same_axis:
        for ct in hue_order:
            if not pu.is_column_numeric(df,hue):
                query = f"({hue} == '{ct}')"
            else:
                query = f"({hue} == {ct})"

            print(f"query = {query}")

            curr_df = df.query(query)
            if verbose:
                print(f"len(query_df) = {len(curr_df)}")
            sns.jointplot(
                    data=curr_df,
                    x=x,
                    y=y,
                    kind="hist",
                    hue=hue_secondary,
                    xlim= xlim,
                    ylim =ylim,
                )

            plt.show()
    else:
        if hue_order is not None:
            curr_df = df.query(f"{hue} in {hue_order}")
        else:
            curr_df= df
        sns.jointplot(
                    data=curr_df,
                    x=x,
                    y=y,
                    kind="hist",
                    hue=hue,
                    xlim= xlim,
                    ylim =ylim,
                )
        
        plt.legend()
        
    


import numpy as np
import numpy_utils as nu
def histograms_over_intervals(
    df,
    attribute,
    interval_attribute,
    
    bins = 30,
    outlier_buffer = 1,
    intervals = None,
    
    hue = None,
    color_dict = None,

    n_intervals = 10,
    overlap = 0.1,
    title_append = None,
    figsize = (8,4), 
    verbose = False,
    
    density = False,
    ):
    """
    Purpose: To plot a sequence of histograms that show the continuous progression of a value for 
    discrete intervals of another continuous value

    Pseudocode: 
    1) Filter the data for outliers if requested
    2) Get the continuous value you will bin and divide it up intervals
    3) Create a figure with a shared x axis
    for each interval: 
    a. restrict the dataframe to that interval
    b. Plot a histogram
    c. Label the title the continuous value range
    """



    df = df.query(f"{attribute} == {attribute}")

    if outlier_buffer is not None:
        att_vals = df[attribute].to_numpy()
        min_value = np.percentile(att_vals,outlier_buffer)
        max_value = np.percentile(att_vals,100-outlier_buffer)
        if verbose:
            print(f"outlier processing: min_value = {min_value}, max_value = {max_value}")

        original_size = len(df)
        df = df.query(
            f"({attribute}>={min_value})"
            f" and ({attribute}<={max_value})"
        )

        if verbose:
            print(f"After outlier filtering df reduced from {original_size} to {len(df)} entries")

    #2) Get the continuous value you will bin and divide it up intervals
    interval_vals = df[interval_attribute]
    if intervals is None:
        intervals = nu.interval_bins_covering_array(
            array = interval_vals,
            n_intervals = n_intervals,
            overlap = overlap, #if this is a percentage then it is a proportion of the interval
            outlier_buffer = 0,
            verbose = False,
        )

    x_ax_min = df[attribute].min()
    x_ax_max = df[attribute].max()
    for j,(lower,upper) in enumerate(intervals):
        df_curr = df.query(
            f"({interval_attribute} >= {lower})"
            f"and ({interval_attribute} <= {upper})"
        )
        
        #if hue is not None:
        ax = mu.histograms_overlayed(
            df_curr,
            attribute,
            hue = hue,
            bins = bins,
            color_dict=color_dict,
            density=density,
            )
#         else:
#             fig,ax = plt.subplots(1,1,figsize=figsize)
#             ax.hist(df_curr[attribute].to_numpy(),
#                    bins=bins)
        curr_title = (f"{attribute} Distribution\n{interval_attribute} [{np.round(lower,2)},{np.round(upper,2)}]"
                      f"\nn_samples = {len(df_curr)}")
        curr_title += f"\nMean = {np.round(df_curr[attribute].mean(),2)}, Std Dev = {np.round(df_curr[attribute].std(),2)}"

        if title_append is not None:
            curr_title += f"\n{title_append}"
        plt.title(curr_title)
        ax.set_xlabel(f"{attribute}")
        if density:
            ax.set_ylabel(f"Density")
        else:
            ax.set_ylabel(f"Count")
        ax.set_xlim([x_ax_min,x_ax_max])
        plt.show()
        
def get_cmap(cmap="RdYlBu"):
    """
    List of all color maps:
    
    Usually end up setting the color map as
    cmap=mu.get_cmap()
    """
    return plt.cm.get_cmap(cmap)

def scatter_with_gradient(
    df = None,
    column_coordinates = None,
    column_gradient = None,
    coordinates = None,
    gradient = None,
    percentile_buffer = None,
    cmap = 'RdYlBu',
    alpha = 0.5,
    vmin = None,
    vmax = None,
    figsize = (10,10),
    title = None,
    ):
    
    if df is not None:
        df = pu.replace_None_with_default(df,0,columns=gradient)
        df = pu.replace_nan_with_default(df,0,)

    cmap = mu.get_cmap(cmap)
    
    if gradient is None:
        gradient = df[column_gradient].to_numpy().astype("float")
    if coordinates is None:
        column_coordinates = list(nu.convert_to_array_like(column_coordinates))
        coordinates = np.vstack(df[column_coordinates].to_numpy()).astype("float")
        
    coordinates = np.array(coordinates)
    if coordinates.shape[1] == 3:
        X,Y,Z = coordinates[:,0],coordinates[:,1],coordinates[:,2]
    else:
        X,Y = coordinates[:,0],coordinates[:,1]
        Z = None
        

    if Z is not None:
        Z = np.array(Z)
        projection_type = "3d"
    else:
        projection_type = None

    X = np.array(X)
    Y = np.array(Y)

    if percentile_buffer:
        if vmin is None:
            vmin = np.percentile(gradient,percentile_buffer)
        if vmax is None:
            vmax = np.percentile(gradient,100-percentile_buffer)
            
        print(f"vmin = {vmin}")
        print(f"vmax = {vmax}")

    #fig,ax = plt.subplots(1,1,projection_type=projection_type)
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111, projection = projection_type)
    
    if Z is not None:
        sc = ax.scatter(
            X,
            Y,
            Z,
            c=gradient,
            vmin=vmin,
            vmax = vmax,
            cmap = cmap,
            alpha = alpha,
            )
    else:
        sc = ax.scatter(
            X,
            Y,
            c=gradient,
            vmin=vmin,
            vmax = vmax,
            cmap = cmap,
            alpha = alpha,
            )
        
    cbar = plt.colorbar(sc)
    if column_gradient is not None:
        cbar.set_label(f'{column_gradient}')#, rotation=270)

    if title is not None:
        ax.set_title(title)
    
    return ax

    
    
import matplotlib_utils as mu