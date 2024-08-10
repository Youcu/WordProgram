import streamlit as st
import numpy as np
import pandas as pd
import re

# --------- Init ---------- # 
st.set_page_config(page_title="Select Range", page_icon="✎")

# PATH
#PATH = '~/Python/WordProgram/DB/CSV/'
PATH = 'DB/CSV/'
file_name = 'updatedWordMaster.csv'

# Create DF
df = pd.read_csv(PATH+file_name) # col_list = [ Day, Word, Mean, Rand ]
df['Day'] = df['Day'].astype(float)
df = pd.DataFrame(df) # CSV to DataFrame

# Define Dictionary
dict_list = {
    'Select' : [1, 0, 0, 0, 0],
    'Sorting' : [0, 1, 0, 0, 0],
    'Hide' : [0, 0, 1, 0, 0],
    'Show' : [0, 0, 0, 1, 0]
}

# --------- Pre Define --------- #

# Clean Words _ Space, Bracket
def clean_word(input_string):
    if input_string is None:
        return None
    return re.sub(r'\s*\(\d+\)\s*$', '', input_string)

def clean_df(df):
    # None 값을 처리할 수 있도록 수정된 함수
    df['Word'] = df['Word'].apply(lambda x: clean_word(x) if pd.notnull(x) else x)
    return df

# addWordNum
def count_words(word):
    if word is None:
        return 0  # None이면 단어 수를 0으로 반환
    renewal = re.sub(r'\s+', '', word)  # 공백 제거
    renewal = re.split(r'\,', renewal)  # 쉼표를 기준으로 분리
    return len(renewal)

def count_df(df):
    def add_count(word):
        if word is None:
            return " (0)"  # None이면 단어 수를 0으로 표시
        word_cnt = count_words(word)
        return f" ({word_cnt})"
    
    counts_format = df['Mean'].apply(lambda x: add_count(x) if pd.notnull(x) else " (0)")
    df['Word'] = df['Word'] + counts_format
    return df

# layout of word program
def layout(minDay, maxDay):

    # Sidebar

    with st.sidebar : 

        # Prompt
        st.write('## Select Range of days')
        st.divider()
        st.write('Input Day : Start ~ End')

        # Init 
        col_rate = [1, 1]
        col_io_list = [ 'input', 'output' ]
        col_io_list = st.columns(col_rate)

        col_default_list = [ 'Select Range', 'Sort' ]
        col_default_list = st.columns(col_rate)
        
        col_option_list = [ 'Hide', 'Show' ]
        col_option_list = st.columns(col_rate)

        # Button list
        with col_io_list[0]:
            input_start = st.number_input(
                label='Start', 
                min_value = minDay, 
                max_value = maxDay, 
                value = None, 
                placeholder='Start', 
                label_visibility='collapsed'
            )
        with col_io_list[1]:
            input_end = st.number_input(
                label='End', 
                min_value = minDay, 
                max_value = maxDay, 
                value = None, 
                placeholder='End', 
                label_visibility='collapsed'
            )

        with col_default_list[0]:
            btn_select = st.button('Select Range', use_container_width=True)
        with col_default_list[1]:
            btn_sorting = st.button('Sorting', use_container_width=True)
        
        with col_option_list[0]:
            btn_hide = st.button('Hide', use_container_width=True)
        with col_option_list[1]:
            btn_show = st.button('Show', use_container_width=True)

    return [ input_start, input_end ] , [ btn_select, btn_sorting, btn_hide, btn_show ] 

# ---------- Layout ---------- #

# When add a word Category, update
maxDay = int(df['Day'].max())
minDay = int(df['Day'].min())

# Create layout & input_list, btn_list
input_list, btn_list = layout(minDay, maxDay)
day_value_list = [ minDay, maxDay ]
print(f"Testing : {input_list}, {btn_list}, {day_value_list}")

# Error Control of Input Value
def is_err_input(input_list):
    if not isinstance(input_list[0], int) or not isinstance(input_list[1], int):
        return 1 
    if input_list[0] > input_list[1]:
        return 1
    
    return 0

# Sorting
def sorting(df, opt): # opt : 0 -> default, opt : 1 -> use session rnd seed
    # Need Random Seed, Sorting
    cnt_data = len(df)

    # ---------- Create Random Number ---------- #

    # Create Random Number List  
    rand_list = np.random.rand(cnt_data)
    

    if opt : 
        rand_list = st.session_state.rand_list
    else : 
        st.session_state.rand_list = rand_list 

    if 'Rand' in df.columns:
        df = df.drop('Rand', axis=1)

    insert_position = min(3, len(df.columns))  # Ensure that the position is within bounds
    df.insert(insert_position, 'Rand', rand_list, allow_duplicates=True)

    df = df.sort_values(by='Rand')

    return df

# Sesstion State Check 
def is_in_session(idx, key):
    li = st.session_state[key]
    return li[idx]
def is_other_btn(btn_list, idx):
    if 1 in btn_list: # btn_list 안에 Valid 있어?
        if btn_list[idx] == 1 : # 근데 그게 해당 idx 위치의 값이야?
            res = 0 # 그러면 다른버튼 누른거 아니야
        else :
            res = 1 # 해당 위치 값이 1이 아니면, 다른 버튼 누른거야
    else : 
        res = -1 # 버튼 자체가 invalid 야 

    return res
def check_session_update(edited_df, key) :

    if key == 'selected_df' :
        if not edited_df.equals(st.session_state.selected_df):
            # If they are different, update the session state and trigger a rerun
            st.session_state.selected_df = edited_df
            return 1
        else : 
            return 0
    elif key == 'edited_df' :
        if not edited_df.equals(st.session_state.edited_df):
            # If they are different, update the session state and trigger a rerun
            st.session_state.edited_df = edited_df
            return 1
        else : 
            return 0
def condition_btn(btn_list, idx, key) :
    if btn_list[idx] or (is_other_btn(btn_list, idx) == -1 and is_in_session(idx, key)):
        return 1
    else : 
        return 0


# Print Data Frame
def printDataframe(df, opt, is_err_input, input_list, btn_list, day_value_list):

    # # Params => 
    # btn_list = [btn_select, btn_resorting]
    # input_list = [input_start, input_end]
    # day_value_list = [ minDay, maxDay ]
    
    edited_df = pd.DataFrame()        

    if not is_err_input :  # Condition -> not err & btn Click
        try:
            clean_df(df)
            df = count_df(df)
        except KeyError as e:
            st.error(f"DataFrame 처리 중 에러 발생: {str(e)}")
            # DataFrame을 초기화하거나, 에러를 처리합니다
            df = pd.read_csv(PATH+file_name)  # DataFrame을 다시 로드합니다
        # clean_df(df)
        # df = count_df(df) # Update Format 
        
        #df = sorting(df) # Sorted DataFrame
        temp_df = df[(input_list[0] <= df['Day']) & (df['Day'] <= input_list[1])] # Then, Column's Value Filtering
        temp_df = temp_df.filter(items=['Day', 'Word', 'Mean']).reset_index(drop=True)  # Column Filtering and resetting index
        
        edited_df = option_dataframe(temp_df, opt, day_value_list)

    else:
        print(is_err_input,input_list, btn_list)
        st.info('Input Values Correctly and Press Button, and Data Frame will be displayed')

    return edited_df
def option_dataframe(df, opt, day_value_list):

    if opt :
        edited_df = st.data_editor( # Print
            data=df, 
            num_rows="dynamic", # available to add rows
            height=700, 
            # Columns Width Customize
            column_config={
                "Word" : st.column_config.Column(
                    width=None,
                ),
                "Mean" : st.column_config.TextColumn(
                    width="large",
                ),
                "Day": st.column_config.NumberColumn(
                    help="Must Input [ {:.0f} ~ {:.0f} ] Value".format(day_value_list[0], day_value_list[1]),
                    min_value=day_value_list[0],
                    max_value=day_value_list[1],
                    width=None,
                    step=1,
                    format="%.0f"
                )
            },  
            use_container_width=True, # width match to main frame
            hide_index=True
        )  # Editable Data Frame
    else : 
        edited_df = st.data_editor(
            data=df,
            height=700, 
            # Columns Width Customize
            column_config={
                "Word" : st.column_config.Column(
                    width=None,
                ),
                "Mean" : st.column_config.TextColumn(
                    width="large",
                ),
                "Day": st.column_config.NumberColumn(
                    help="Must Input [ {:.0f} ~ {:.0f} ] Value".format(day_value_list[0], day_value_list[1]),
                    min_value=day_value_list[0],
                    max_value=day_value_list[1],
                    width=None,
                    step=1,
                    format="%.0f"
                )
            },  
            use_container_width=True, # width match to main frame
            hide_index=True,
            disabled=True
        )
    return edited_df

# Init Session 
if 'btn_list' not in st.session_state:
    st.session_state.btn_list = btn_list
if 'edited_df' not in st.session_state:
    st.session_state.edited_df = df
if 'is_stat' not in st.session_state:
    st.session_state.is_stat = [0, 0] # is_sorted, is_hidden
if 'selected_df' not in st.session_state:
    st.session_state.selected_df = df
if 'restored_df' not in st.session_state:
    st.session_state.restored_df = pd.DataFrame()
if 'rand_list' not in st.session_state : 
    st.session_state.rand_list = []

# Main Module ------------------------------------------------------------------------

# ---------- Layout ---------- #

# When add a word Category, update
# maxDay = int(df['Day'].max())
# minDay = int(df['Day'].min())

# # Create layout & input_list, btn_list
# input_list, btn_list = layout(minDay, maxDay)
# day_value_list = [ minDay, maxDay ]

# --------- Optional Print Data Frame --------- #

print(f"\tbefore condition\nsession : {st.session_state.btn_list}\nbutton : {btn_list}")

# Select Button
if condition_btn(btn_list, 0, 'btn_list'):
    # 버튼을 눌렀거나, 버튼을 누르진 않았지만 데이터 변경으로 세션은 남아있을 때
    
    # First, Update btn session
    st.session_state.btn_list = dict_list['Select']

    st.subheader(f"Day : {input_list[0]} ~ {input_list[1]}")
    st.divider()
    edited_df = printDataframe(
        st.session_state.selected_df, 1, 
        is_err_input(input_list), 
        input_list, 
        btn_list, 
        day_value_list
    )

    # Check if the edited dataframe is different from the original dataframe
    if check_session_update(edited_df, 'selected_df') :
        st.rerun()  # Use st.rerun instead of st.experimental_rerun

    st.session_state.edited_df = edited_df
    
# Sorting Button
if condition_btn(btn_list, 1, 'btn_list'): 
    st.session_state.btn_list = dict_list['Sorting']
    #st.subheader(len(df))

    if btn_list[1]: # 다른 버튼 눌렀어. 세션 데이터 업데이트 해 
        edited_df = sorting(st.session_state.edited_df, 0) # OK
        
        # Check if the edited dataframe is different from the original dataframe
        if check_session_update(edited_df, 'edited_df') : 
            st.rerun()  # Use st.rerun instead of st.experimental_rerun
    st.session_state.is_stat = [1, is_in_session(1, 'is_stat')]

    st.subheader(f"Day : {input_list[0]} ~ {input_list[1]}, Sorted")
    st.divider()
    edited_df = printDataframe(
        st.session_state.edited_df, 1, 
        is_err_input(input_list), 
        input_list, 
        btn_list, 
        day_value_list
    )

    # Check if the edited dataframe is different from the original dataframe
    if check_session_update(edited_df, 'edited_df') : 
        st.rerun()  # Use st.rerun instead of st.experimental_rerun

# Hide Button
if condition_btn(btn_list, 2, 'btn_list'):

    # Session Init 
    st.session_state.btn_list = dict_list['Hide']
    
    # Check Session_State : is_stat for Sorted / Selected Session
    hidden_df = st.session_state.edited_df.copy()

    # Set Restored Dataframe
    st.session_state.restored_df = hidden_df.copy()

    # Hide Values -> Remove
    hidden_df['Mean'] = ''

    # Session State.is_stat Update : Hidden -> True
    st.session_state.is_stat = [is_in_session(0, 'is_stat'), 1]

    # Print Dataframe 
    st.subheader(f"Day : {input_list[0]} ~ {input_list[1]}, Hidden")
    st.divider()
    st.session_state.edited_df = printDataframe(
        hidden_df, 0,
        is_err_input(input_list), 
        input_list, 
        btn_list, 
        day_value_list
    )   

# Show Button
if condition_btn(btn_list, 3, 'btn_list'):
    # 버튼을 눌렀거나, 버튼을 누르진 않았지만 데이터 변경으로 세션은 남아있을 때
    st.session_state.btn_list = dict_list['Show']

    # Check Session Stat
    if is_in_session(1, 'is_stat') : # hidden Case 만 처리
        st.subheader(f"Day : {input_list[0]} ~ {input_list[1]}, Showed")
        st.divider()
        edited_df = sorting(st.session_state.restored_df, 1)
        st.session_state.edited_df = printDataframe(
            edited_df, 0,
            is_err_input(input_list), 
            input_list, 
            btn_list, 
            day_value_list
        )
    else:
        st.error('Data Frame is not hidden State')
