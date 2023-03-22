from reliability.Distributions import Weibull_Distribution
from reliability.Distributions import Exponential_Distribution
from reliability.Distributions import Normal_Distribution
from reliability.Distributions import Lognormal_Distribution
from reliability.Distributions import Gamma_Distribution
from reliability.Distributions import Beta_Distribution
from reliability.Distributions import Loglogistic_Distribution
from reliability.Distributions import Gumbel_Distribution
#import tkinter
import matplotlib
#matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import random
import json

#filePath = 'C:\\Users\\omidg\\New RE Version\\ComponentFiles\\'
dist_list = ['Weibull', 'Exponential', 'Normal', 'Lognormal', 'Gamma', 'Beta', 'Loglogistic', 'Gumbel']

calculated_comps = {}
serial_list = {}
parallel_list = {}
comp_relations = {}
index = {}


comp_data_def_filename =  'comp_def.json'
comp_data_def_file = open(comp_data_def_filename)
comp_def_data = json.load(comp_data_def_file)
comp_data_def_file.close()

comp_config_filename =  'comp_config.txt'
comp_config_file = open(comp_config_filename)
comp_config_data = comp_config_file.read()
comp_config_file.close()

def Serial(*components_args):
    min_TTF = 1000000
    for arg in components_args:
        if type(arg) is str:
            min_TTF = min(min_TTF, calculated_comps[arg][index['index']]['TTF'])
        else: 
             min_TTF = min(min_TTF, arg)   

    serial_list[str(components_args)] = min_TTF
    return min_TTF

def Parallel(*components_arg):
    max_TTF = 0
    for arg in components_arg:
        if type(arg) is str:
            max_TTF = max(max_TTF, calculated_comps[arg][index['index']]['TTF'])
        else: 
            max_TTF = max(max_TTF, arg)   

    parallel_list[str(components_arg)] = max_TTF
    return max_TTF

def calculate(key, reliability):
    comp = comp_def_data[key]
    distName = comp['dist']
    param1 = comp['param1']
    param2 = comp['param2']

    if distName == 'Weibull':
        dist = Weibull_Distribution(alpha = param1, beta = param2)  

    elif distName == 'Exponential':
        dist = Exponential_Distribution(Lambda = param1)

    elif distName == 'Normal':
        dist = Normal_Distribution(mu = param1, sigma = param2)

    elif distName == 'Lognormal':
        dist = Lognormal_Distribution(mu = param1, sigma = param2)

    elif distName == 'Gamma':
        dist = Gamma_Distribution(alpha = param1, beta = param2)

    elif distName == 'Beta':
        dist = Beta_Distribution(alpha = param1, beta = param2)

    elif distName == 'Loglogistic':
        dist = Loglogistic_Distribution(alpha = param1, beta = param2)              

    elif distName == 'Gumbel':
        dist = Gumbel_Distribution(mu = param1, sigma = param2)

    ttf = dist.inverse_SF(reliability) 
    return round (ttf, 3)

def init_comp_data():
    iteration_count = st.session_state.iteration_count

    for iteration in range(iteration_count):
        for key in comp_def_data:
            if key not in calculated_comps : 
                calculated_comps[key] = []

            reliability = random.random()
            ttf = calculate(key, reliability)
            dist_values_dict = {'Reliability': reliability, 'TTF': ttf}

            calculated_comps[key].append(dist_values_dict)

def init_comp_relations():
    for key in comp_def_data:
        cmp_key = "'" + key + "'"
        comp_relations[cmp_key] = cmp_key
 
def show_ttf():
    init_comp_data()

    ttf_list = []
    iteration_count = st.session_state.iteration_count
    Confidence_Level=st.session_state.Confidence_Level
    Confidence_Level=Confidence_Level/100
    for iteration in range(iteration_count):
        #st.write('Iteration Info ( Iteration = ', iteration+1, ')')
        index['index'] = iteration
        ttf = eval(comp_config_data)
        ttf_list.append(ttf)

        # st.write("Serial Components reliability:")
        # st.write(serial_list)
        # st.write("Parallel Components reliability:")
        # st.write(parallel_list)
        # st.write('---------------------------')
        
        #st.write("Time To Failure List: ", ttf_list)

    a = (1 - Confidence_Level) / 2
    min_number = round (a * iteration_count)
   

    max_number = round(iteration_count - (a * iteration_count))
   
    ttf_list.sort()
    
    
    
 
    min_time_in_list = ttf_list [min_number]
   
    max_time_in_list= ttf_list [max_number-1]
    st.write ('System time to failure interval is: [', min_time_in_list ,',', max_time_in_list,']') 
    e = (  max_time_in_list - min_time_in_list )/2
    e= round (e,3)
    st.write ('System time to failure  is:' , e ) 

   
    plt.hist(ttf_list)
    plt.savefig('test.png')
    plt.show()

    # st.write("-----------------")
    # st.write("Component Values:")
    # st.json(calculated_comps)

def Com_Sen():

    init_comp_data()

    ttf_list = []
    iteration_count = st.session_state.iteration_count
    Confidence_Level=st.session_state.Confidence_Level
    Confidence_Level=Confidence_Level/100
    for iteration in range(iteration_count):
        #st.write('Iteration Info ( Iteration = ', iteration+1, ')')
        index['index'] = iteration
        ttf = eval(comp_config_data)
        ttf_list.append(ttf)

        # st.write("Serial Components reliability:")
        # st.write(serial_list)
        # st.write("Parallel Components reliability:")
        # st.write(parallel_list)
        # st.write('---------------------------')
        
    st.write("Time To Failure List: ", ttf_list)

    a = (1 - Confidence_Level) / 2
    min_number = round (a * iteration_count)
   

    max_number = round(iteration_count - (a * iteration_count))
   
    ttf_list.sort()
    
    
    
 
    min_time_in_list = ttf_list [min_number]
   
    max_time_in_list= ttf_list [max_number-1]
    st.write ('System time to failure interval is: [', min_time_in_list ,',', max_time_in_list,']') 
    e = (  max_time_in_list - min_time_in_list )/2
    e= round (e,3)
    st.write ('System time to failure  is:' , e ) 

   
    plt.hist(ttf_list)
    plt.savefig('test.png')
    plt.show()

    st.write("-----------------")
    st.write("Component Values:")
    st.json(calculated_comps)

def show_comp_def_File():

    st.button(label='Add New Component', on_click=show_add_comp, args=('', ))
    st.write('-----------------')

    for compKey in comp_def_data:
        comp = comp_def_data[compKey]
        distName = comp["dist"]
        param1 = comp["param1"]
        param2 = comp["param2"]
        st.subheader(compKey)
        st.write("Distribution: ", distName, ", Param1: ", param1, ", Param2: ", param2) 
        st.button("Edit", key=compKey, on_click=show_add_comp, args=(compKey, )) 
        

def show_add_comp(compKey):
    with st.form(key='single_comp_def_form'):
        if compKey != '' :
            comp = comp_def_data[compKey]
            distName = comp["dist"]
            param1 = comp["param1"]
            param2 = comp["param2"]
        else:
            comp = ''
            distName = dist_list[0]
            param1 = 0.0
            param2 = 0.0

        st.subheader('Enter Component Information')
        st.text_input('Component Unique Name', key='comp_name', value=compKey)
        st.selectbox('Distribution', dist_list, key='comp_dist', index=dist_list.index(distName))
        st.number_input('param1', step=0.01, key='comp_param1', value=param1)
        st.number_input('param2', step=0.01, key='comp_param2', value=param2)

        submitButton = st.form_submit_button(label='Add/Edit Component', on_click=show_add_comp, args=(compKey, ))
        delButton = st.form_submit_button(label='Delete Component', on_click=show_add_comp, args=(compKey, ))

    if submitButton :

        comp_name = st.session_state.comp_name
        comp_dist = st.session_state.comp_dist
        comp_param1 = st.session_state.comp_param1
        comp_param2 = st.session_state.comp_param2

        comp_detail_dict =  {'dist': comp_dist, 'param1': comp_param1, 'param2': comp_param2}
        comp_def_data[comp_name] = comp_detail_dict

        json_object = json.dumps(comp_def_data, indent=4)
        with open(comp_data_def_filename, 'w') as outfile:  
            outfile.write(json_object)

        st.write('Component ', comp_name, ' was add/edited.')

    if delButton :
        comp_name = st.session_state.comp_name
        
        comp_def_data.pop(comp_name)

        json_object = json.dumps(comp_def_data, indent=4)
        with open(comp_data_def_filename, 'w') as outfile:
            outfile.write(json_object)

        st.write('Component ', comp_name, ' was deleted.')

def show_comp_config_File():
    c_c_filename = filePath + 'comp_config.txt'
    c_c_file = open(c_c_filename)
    c_c_data = c_c_file.read()

    # with st.form(key='comp_conf_form'):
    txt = st.text_area(label="Components Configuration", height=300, value=c_c_data)

    #     submitButton = st.form_submit_button(label='Update Components Configuration File', on_click=show_comp_config_File)

    # if submitButton:
    #     #comp_c_file = open(comp_config_filename, 'w')
    #     comp_c_file.write(txt) 
    #     comp_c_file.close()

    #     st.write('File ', comp_config_filename, ' was saved.')


def show_assistant_comp_config_File():
    if not comp_relations:
        init_comp_relations()

    with st.form(key='comp_relation_form'):

        st.subheader('Please enter components relations')
        st.radio('Select Relation Type:', ['Serial' ,
                'Parallel'], key='relation_type')
        st.multiselect('Components: ', comp_relations, key='selected_comps')

        if len(comp_relations) == 1:
            finalFlag = True
        else:
            finalFlag = False

        addButton = st.form_submit_button(label='Add', on_click=show_assistant_comp_config_File, disabled=finalFlag)
        saveFileButton = st.form_submit_button(label='Save Components Config', on_click=show_assistant_comp_config_File, disabled=not finalFlag)

    if addButton :

        relation_Type = st.session_state.relation_type
        selected_comps = st.session_state.selected_comps

        if(len(selected_comps)>1):

            new_key = relation_Type + "("
            
            for comp in selected_comps:
                new_key = new_key + " " + comp + " , "
                comp_relations.pop(comp) 

            new_key = new_key[:-2] 
            new_key = new_key + ")"
            comp_relations[new_key] = new_key

        st.button("Apply Relation", on_click=show_assistant_comp_config_File) 

    if saveFileButton :
        if len(comp_relations) == 1 :
            comp_c_file = open(comp_config_filename, 'w')
            for c in comp_relations:
                comp_c_file.write(c) 

            comp_c_file.close()

            st.write('File ', comp_config_filename, ' was saved.')

#=================================
tab_comp, tab_conf, tab_montc, tab_sen = st.sidebar.tabs(['Components Definition', 'Configuration Definition', 'Monte Carlo Calculation','Sensitivity Analysis'])
with tab_comp:
    st.write('Steps for defining a componet:  \n1- Click on the Enter your component key.  \n2- Click on Add New Component key.    \n3- Type a unique name for your component.     \n4- Choose the component distribution from the list.     \n5- Enter your Parameters.      \n6- Click on Add/Edit componet.       \n7- Clike on Edit button for editing an existing component.')
    st.button('Enter your Components ', on_click=show_comp_def_File)

   # st.button('Components Config File', on_click=show_comp_config_File)
   # st.button('Assistant Components Config File', on_click=show_assistant_comp_config_File)

   # st.write("--------")

   # st.number_input('Iteration Count', step=1, value=1, key='iteration_count')
   # st.button('Calculate Random TTF', on_click=show_ttf)

with tab_conf:
   
    st.write('Steps for defining a System Configuration:       \n1-Click on Configuration Provider Assistant button.       \n2- Select the relation type for each component group.      \n3- Choose the components in each group.   \n4- Click on Add button.      \n5- Click on Apply Relation button.     \n6- Clike on Save System Structure.    \n7- Click on System  Configuration button to see the existing structure. ')   
    st.button('Configuration Provider Assistant', on_click=show_assistant_comp_config_File)
    st.button('System Configuration ', on_click=show_comp_config_File)
 

with tab_montc:
    st.write('Steps for Calculating the System Time To Failure:     \n1-Enter the number of iteration for calculation.      \n2- Click on the Calculate System TTF. ')
    st.number_input('Number of Senarios ', step=1, value=1, key='iteration_count')
    st.number_input('Confidence Level (Two-Side) ', step = 1, value=1, key='Confidence_Level')  
    st.button('Calculate System TTF', on_click=show_ttf)

with tab_sen:
    st.write('Based on the cut set method and by using the Birnbaum, criticality and Fussell-Vesely factors, the components are listed related to their sesitivity to system failing, then if there is budget for maintenance we offer to spend for fixing by this priority.   ')
    st.number_input('Available Budget ', step=1, value=1, key='budget')
    st.button('List the component based on their sensitivity', on_click= Com_Sen)
