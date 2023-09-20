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
            st.warning("The file must have a column named --conversation_stream--")
        else:
            df = read_excel_parquet(df_file)
        
     
        st.session_state.list_number = st.radio("How many list of words do you want?",["1","2","3"])
        # List number 1 
        if int(st.session_state.list_number) == 1:
            res_delete = st.radio("Do you want to delete what is in the column 1 ?",["no","yes"])
            if res_delete == "yes":
                st.session_state.list_1 = []
                st.warning("List empty")
            else:
                word = st.text_input("Enter your word:")
                if word != "":
                    if word not in st.session_state.list_1:
                        word = word.split(",")
                        for x in word:
                            st.session_state.list_1.append(fr"\b{x.lower()}\b")       
                            st.write(x.lower())
        # List number 2 
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
                        word_1 = word_1.split(",")
                        for x in word_1:
                            st.session_state.list_1.append(fr"\b{x.lower()}\b")       
                            st.write(x.lower())
                
                word_2 = st.text_input("Enter your word for the second list:")
                if word_2 != "":
                    if word_2 not in st.session_state.list_2:
                        word_2 = word_2.split(",")
                        for x in word_2:
                            st.session_state.list_2.append(fr"\b{x.lower()}\b")       
                            st.write(x.lower())
        #List number 3 
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
                        word_1 = word_1.split(",")
                        for x in word_1:
                            st.session_state.list_1.append(fr"\b{x.lower()}\b")       
                            st.write(x.lower())

                word_2 = st.text_input("Enter your word for the second list:")
                if word_2 != "":
                    if word_2 not in st.session_state.list_2:
                        word_2 = word_2.split(",")
                        for x in word_2:
                            st.session_state.list_2.append(fr"\b{x.lower()}\b")       
                            st.write(x.lower())
                
                word_3 = st.text_input("Enter your word for the third list:")
                if word_3 != "":
                    if word_3 not in st.session_state.list_3:
                        word_3 = word_3.split(",")
                        for x in word_3:
                            st.session_state.list_3.append(fr"\b{x.lower()}\b")       
                            st.write(x.lower())


        
        res_zero = str(st.radio("remove the zeros?",["no","yes"]))

        if df_file == None:
            pass
        else:
            conv = list(df["conversation_stream"].apply(lambda x : str(x).lower()))
            if st.button("Key search"):
                
                # one list 
                if int(st.session_state.list_number) == 1:   
                    # creating the progress bar
                    progress_bar = st.progress(0)
                    total_iterations = len(df)

                    
                    pattern = re.compile("|".join(st.session_state.list_1))
                    pattern_name = "list_1_count"
                    df[pattern_name]=0
                    df["list_1_words"] = 0
                    for index in range(0,len(df)):
                        word_res = re.findall(pattern,str(conv[index]))
                        if word_res == []:
                            df[pattern_name][index] = 0 
                            df["list_1_words"][index]=0
                        else:
                            df[pattern_name][index] = 1
                            df["list_1_words"][index]= set(word_res)
                        
                        progress = (index + 1) / total_iterations
                        progress_bar.progress(progress)
        
                    
                    
                    percentage = (sum(df[pattern_name])/len(df[pattern_name])) * 100 
                    st.write(f'Relative percentage list 1 %  > {round(percentage,3)}')
                    st.write(df.head(25))
                    
                    if res_zero == "yes":
                        df_optional = df[df["list_1_words"] != 0] 
                        df_xlsx = to_excel(df_optional)
                        st.download_button(label='📥 Download Current words search', data=df_xlsx, file_name= f"test.xlsx")

                    if res_zero =="no":
                        df_xlsx = to_excel(df)
                        st.download_button(label='📥 Download Current words search', data=df_xlsx, file_name= f"test.xlsx")
                    

                # two lists
                if int(st.session_state.list_number) == 2:
                    
                    progress_bar = st.progress(0)
                    total_iterations = len(df)
                    
                    
                    pattern_1 = re.compile("|".join(st.session_state.list_1))
                    pattern_name_1 = "list_1_count"
                    
                    pattern_2 = re.compile("|".join(st.session_state.list_2))
                    pattern_name_2 =  "list_2_counts"


                    df[pattern_name_1]=0
                    df[pattern_name_2]=0

                    df["list_1_words"] = 0
                    df["list_2_words"] = 0
                    
                    for index in range(0,len(df)):
                        word_res_1 = re.findall(pattern_1,str(conv[index]))
                        if word_res_1 == []:
                            df[pattern_name_1][index] = 0 
                            df["list_1_words"][index]= 0
                        else:
                            df[pattern_name_1][index] = 1
                            df["list_1_words"][index]= set(word_res_1)
                    
                        word_res_2 = re.findall(pattern_2,str(conv[index]))
                        if word_res_2 == []:
                            df[pattern_name_2][index] = 0 
                            df["list_2_words"][index]= 0
                        else:
                            df[pattern_name_2][index] = 1
                            df["list_2_words"][index]= set(word_res_2)

                        progress = (index + 1) / total_iterations
                        progress_bar.progress(progress)
                        
                    percentage_1 = (sum(df[pattern_name_1])/len(df[pattern_name_1])) * 100
                    percentage_2 = (sum(df[pattern_name_2])/len(df[pattern_name_2])) *100 
                    st.write(f'Relative percentage list 1 > {round(percentage_1,3)}')
                    st.write(f'Relative percentage list 2 > {round(percentage_2,3)}')
                    st.write(df.head(25))
                    
                    if res_zero == "yes":
                        df_optional = df[(df["list_1_words"] != 0) & (df["list_2_words"] != 0)] 
                        df_xlsx = to_excel(df_optional)
                        st.download_button(label='📥 Download Current words search', data=df_xlsx, file_name= f"test.xlsx",key=2)

                    if res_zero =="no":
                        df_xlsx = to_excel(df)
                        st.download_button(label='📥 Download Current words search', data=df_xlsx, file_name= f"test.xlsx",key=22)

            # 3 lists 
                if int(st.session_state.list_number) == 3:
                        progress_bar = st.progress(0)
                        total_iterations = len(df)
                    
                    
                    
                        pattern_1 = re.compile("|".join(st.session_state.list_1))
                        pattern_name_1 = "list_1_count"
                        
                        pattern_2 = re.compile("|".join(st.session_state.list_2))
                        pattern_name_2 =  "list_2_counts"

                        pattern_3 = re.compile("|".join(st.session_state.list_1))
                        pattern_name_3 = "list_3_count"
                        
                        df[pattern_name_1]=0
                        df[pattern_name_2]=0
                        df[pattern_name_3]=0

                        df["list_1_words"] = 0
                        df["list_2_words"] = 0
                        df["list_3_words"] = 0

                        for index in range(0,len(df)):
                            word_res_1 = re.findall(pattern_1,str(conv[index]))
                            if word_res_1 == []:
                                df[pattern_name_1][index] = 0 
                                df["list_1_words"][index]= 0
                            else:
                                df[pattern_name_1][index] = 1
                                df["list_1_words"][index]= set(word_res_1)
                            
                            word_res_2 = re.findall(pattern_2,str(conv[index]))
                            if word_res_2 == []:
                                df[pattern_name_2][index] = 0 
                                df["list_2_words"][index]= 0
                            else:
                                df[pattern_name_2][index] = 1
                                df["list_2_words"][index]= set(word_res_2)
                        

                            word_res_3 = re.findall(pattern_3,str(conv[index]))
                            if word_res_3 == []:
                                df[pattern_name_3][index] = 0 
                                df["list_3_words"][index]= 0
                            else:
                                df[pattern_name_3][index] = 1
                                df["list_3_words"][index]= set(word_res_3)

                            progress = (index + 1) / total_iterations
                            progress_bar.progress(progress)
                        
                        percentage_1 = (sum(df[pattern_name_1])/len(df[pattern_name_1])) * 100
                        percentage_2 = (sum(df[pattern_name_2])/len(df[pattern_name_2])) * 100 
                        percentage_3 = (sum(df[pattern_name_3])/len(df[pattern_name_3])) * 100
                        st.write(f'Relative percentage list 1-> {round(percentage_1,3)}')
                        st.write(f'Relative percentage list 2-> {round(percentage_2,3)}')
                        st.write(f'Relative percentage list 3-> {round(percentage_3,3)}')
                        st.write(df.head(25))
                       
                        
                        if res_zero == "yes":
                            df_optional = df[(df["list_1_words"] != 0) & (df["list_2_words"] != 0) & (df["list_3_words"] != 0)] 
                            df_xlsx = to_excel(df_optional)
                            st.download_button(label='📥 Download Current words search', data=df_xlsx, file_name= f"test.xlsx",key=1233)

                        if res_zero =="no":
                            df_xlsx = to_excel(df)
                            st.download_button(label='📥 Download Current words search', data=df_xlsx, file_name= f"test.xlsx",key=1213)

    


if __name__ == "__main__":
    main()
