# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
# Write directly to the app
st.title("Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie
    """
)

Name_on_Order = st.text_input('Name on Smoothie:')
st.write('the name on the Smoothie will be ',Name_on_Order)
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

pd_df=my_dataframe.to_pandas()
st.dataframe(pd_df)
#st.stop()

ingredients_list = st.multiselect('choose your top 5 ingredients:',my_dataframe,
                                 max_selections=5)

if ingredients_list: 
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen+ ' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        st.subheader(fruit_chosen + ' Nutrition Information')
        
my_insert_stmt= """insert into smoothies.public.orders(ingredients,name_on_order)values ('"""+ingredients_string+"""','"""+Name_on_Order+"""')"""
time_to_insert = st.button('Submit Order')
st.write(my_insert_stmt)
if time_to_insert:
    session.sql(my_insert_stmt).collect()    
#st.write(ingredients_string)


    
    st.success('Your Smoothie is ordered!',icon ="✅")

import requests

