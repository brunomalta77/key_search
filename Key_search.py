# building a stream lite application
import pandas as pd
import numpy as np
import re
import time
import string
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import joblib
import glob
import requests
import pandas as pd
import numpy as np 
import os 
from PIL import Image
import re
from io import BytesIO
from pyxlsb import open_workbook as open_xlsb



#page config
st.set_page_config(page_title="Key word search",page_icon="🕵️‍♂️",layout="wide")
logo_path = "brand_logo.png"
image = Image.open(logo_path)

col1, col2 = st.columns([4, 1])  # Adjust the width ratios as needed

# Logo on the left
with col2:
    st.image(image)  # Adjust the width as needed

# Title on the right
with col1:
    st.title("Key word search (V 0.1)")


@st.cache(allow_output_mutation=True,suppress_st_warning=True) 
def read_excel_parquet(df_file):
    if "parquet" in str(df_file):
        df = pd.read_parquet(df_file)
    if "xlsx" in str(df_file):
        df = pd.read_excel(df_file)
    return df

                           
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'}) 
    worksheet.set_column('A:A', None, format1)  
    writer.close()
    processed_data = output.getvalue()
    return processed_data








#-----------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------

def main():
    with st.container():
        #Global variables
        if "list_1" not in st.session_state:
            st.session_state.list_1 = []

        if "list_2" not in st.session_state:
            st.session_state.list_2 = []

        if "list_3" not in st.session_state:
            st.session_state.list_3 = []

        if "list_number" not in st.session_state:
            st.session_state.list_number = None
        
        if 'button' not in st.session_state:
            st.session_state.button = None

       
        
        df_file = st.file_uploader("Upload a Excel/Parquet file")
        if df_file == None:
            st.warning("Please upload you excel/parquet file")
            st.warning("The file must have a column named --cleaned message--")
        else:
            df = read_excel_parquet(df_file)
        
     
        st.session_state.list_number = st.radio("How many list of words do you want?",["1","2","3"])
        
        if int(st.session_state.list_number) == 1:
            res_delete = st.radio("Do you want to delete what is in the column 1 ?",["no","yes"])
            if res_delete == "yes":
                st.session_state.list_1 = []
                st.warning("List empty")
            else:
                word = st.text_input("Enter your word:")
                if word != "":
                    if word not in st.session_state.list_1:
                        st.session_state.list_1.append(word)       
                st.write(st.session_state.list_1)

        if int(st.session_state.list_number) == 2:
            res_delete = st.radio("Do you want to delete what is in the column 1 and 2  ?",["no","yes"])
            if res_delete == "yes":
                st.session_state.list_1 = []
                st.session_state.list_2 = []
                st.warning("Lists empty")
            else:
                word_1 = st.text_input("Enter your word for the first list:")
                if word_1 != "":
                    if word_1 not in st.session_state.list_1:
                        st.session_state.list_1.append(word_1.lower())       
                st.write(st.session_state.list_1)
                
                word_2 = st.text_input("Enter your word for the second list:")
                if word_2 != "":
                    if word_2 not in st.session_state.list_2:
                        st.session_state.list_2.append(word_2.lower())       
                st.write(st.session_state.list_2)
            
        if int(st.session_state.list_number) == 3:
            res_delete = st.radio("Do you want to delete what is in the column 1, 2  and 3  ?",["no","yes"])
            if res_delete == "yes":
                st.session_state.list_1 = []
                st.session_state.list_2 = []
                st.session_state.list_3 = []
                st.warning("Lists empty")
            else:
                word_1 = st.text_input("Enter your word for the first list:")
                if word_1 != "":
                    if word_1 not in st.session_state.list_1:
                        st.session_state.list_1.append(word_1.lower())       
                st.write(st.session_state.list_1)
                
                word_2 = st.text_input("Enter your word for the second list:")
                if word_2 != "":
                    if word_2 not in st.session_state.list_2:
                        st.session_state.list_2.append(word_2.lower())       
                st.write(st.session_state.list_2)
                
                word_3 = st.text_input("Enter your word for the third list:")
                if word_3 != "":
                    if word_3 not in st.session_state.list_3:
                        st.session_state.list_3.append(word_3.lower())       
                st.write(st.session_state.list_3)




        res = str(st.radio("Generate Topics",["no","yes"]))

        if df_file == None:
            pass
        else:
            conv = list(df["cleaned_message"])
            if res == "yes":
                # one list 
                if int(st.session_state.list_number) == 1:   
                    pattern = re.compile("|".join(st.session_state.list_1))
                    pattern_name = "|".join(st.session_state.list_1)
                    df[pattern_name]=0
                    for index in range(0,len(df)):
                        word_res = len(re.findall(pattern,str(conv[index])))
                        if word_res > 0:
                            df[pattern_name][index] = 1 
                        else:
                            df[pattern_name][index] = 0
                    st.write(df.head(10))
                    df_xlsx = to_excel(df)
                    st.download_button(label='📥 Download Current words search', data=df_xlsx, file_name= f"test.xlsx")
                        



                # two lists
                if int(st.session_state.list_number) == 2:
                    pattern_1 = re.compile("|".join(st.session_state.list_1))
                    pattern_name_1 = "|".join(st.session_state.list_1)
                    
                    pattern_2 = re.compile("|".join(st.session_state.list_2))
                    pattern_name_2 = "|".join(st.session_state.list_2)


                    df[pattern_name_1]=0
                    df[pattern_name_2]=0
                    
                    for index in range(0,len(df)):
                        word_res_1 = len(re.findall(pattern_1,str(conv[index])))
                        if word_res_1 > 0:
                            df[pattern_name_1][index] = 1 
                        else:
                            df[pattern_name_1][index] = 0
                        
                        word_res_2 = len(re.findall(pattern_2,str(conv[index])))
                        if word_res_2 > 0:
                            df[pattern_name_2][index] = 1 
                        else:
                            df[pattern_name_2][index] = 0
                    
                    st.write(df.head(10))
                    df_xlsx = to_excel(df)
                    st.download_button(label='📥 Download Current words search', data=df_xlsx, file_name= f"test.xlsx")

            # 3 lists 
                if int(st.session_state.list_number) == 3:
                        pattern_1 = re.compile("|".join(st.session_state.list_1))
                        pattern_name_1 = "|".join(st.session_state.list_1)
                        
                        pattern_2 = re.compile("|".join(st.session_state.list_2))
                        pattern_name_2 = "|".join(st.session_state.list_2)

                        pattern_3 = re.compile("|".join(st.session_state.list_3))
                        pattern_name_3 = "|".join(st.session_state.list_3)


                        df[pattern_name_1]=0
                        df[pattern_name_2]=0
                        df[pattern_name_3]=0
                        
                        for index in range(0,len(df)):
                            word_res_1 = len(re.findall(pattern_1,str(conv[index])))
                            if word_res_1 > 0:
                                df[pattern_name_1][index] = 1 
                            else:
                                df[pattern_name_1][index] = 0
                            
                            word_res_2 = len(re.findall(pattern_2,str(conv[index])))
                            if word_res_2 > 0:
                                df[pattern_name_2][index] = 1 
                            else:
                                df[pattern_name_2][index] = 0
                        
                            word_res_3 = len(re.findall(pattern_3,str(conv[index])))
                            if word_res_3 > 0:
                                df[pattern_name_3][index] = 1 
                            else:
                                df[pattern_name_3][index] = 0
                        
                        st.write(df.head(10))
                        df_xlsx = to_excel(df)
                        st.download_button(label='📥 Download Current words search', data=df_xlsx, file_name= f"Key_word_search.xlsx")

  



if __name__ == "__main__":
    main()
