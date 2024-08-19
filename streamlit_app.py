# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothie :cup_with_straw:")
st.write(
    """ Choose the fruits you want in your custom smoothie
    """
)
 
name_on_order = st.text_input("Name on Smoothie")
st.write("The name on your Smoothie will be", name_on_order)
 
 
# session = get_active_session()
cnx = st.connection("snowflake")
# session = get_active_session()
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
st.dataframe(data=my_dataframe, use_container_width=True)
 
pd_df =my_dataframe.to_pandas()
# st.dataframe(pd_df)
# st.stop()
 
ingredients_list =st.multiselect (
'choose up to 5 ingredients:'
,my_dataframe,max_selections=5
)
if ingredients_list:
    ingredients_string=''
 
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        # Assuming 'each_fruit' should be 'fruit_chosen'
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen, ' is ', search_on, '.')
        st.subheader(fruit_chosen + ' Nutrition Information')
        # Correcting the line break and removing unnecessary quotes
        fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/"+fruit_chosen)
        # st.text(fruityvice_response.json()) - Uncomment if you need to inspect the raw JSON response
        # Assuming the API returns JSON data compatible with a dataframe
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
 
 
    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                values ('""" + ingredients_string + """','""" +name_on_order+ """')"""
    #st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
       session.sql(my_insert_stmt).collect()
       st.success('Your Smoothie is ordered!', icon="✅")
 
 
import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
# st.text(fruityvice_response.json())
fv_df=st.dataframe(data=fruityvice_response.json(),use_container_width=True)
