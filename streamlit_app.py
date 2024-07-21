# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests




# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """)


name_on_order = st.text_input("Name on Smoothie")
st.write("The name on your Smoothie will be:", name_on_order)

cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
st.dataframe(data=my_dataframe, use_container_width=True)

pd_df=my_dataframe.to_pandas()
st.dataframe(pd_df)
    
st.stop()

ingredients_list = st.multiselect(
    "Choose upto 5 ingredients:",
    my_dataframe, max_selections = 5)

ingredients_string=''

if ingredients_list:
    for fruits_chosen in ingredients_list:
        ingredients_string += fruits_chosen + ' '
        st.subheader(fruits_chosen + ' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruits_chosen)
        fv_df=st.dataframe(data=fruityvice_response.json(), use_container_width=True)

    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,NAME_ON_ORDER )
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    time_to_insert=st.button('Submit Order')

    #st.write(my_insert_stmt)

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(('Your Smoothie is ordered, '+ name_on_order +'!'), icon="✅")



