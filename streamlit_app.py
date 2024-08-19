# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col, when_matched
 
# Write directly to the app
st.title(":cup_with_straw: Pending Smoothie Orders :cup_with_straw:")
st.write(
    """Orders that need to be filled.
    """
)
 
cnx = st.connection("snowflake")
# session = get_active_session()
session = cnx.session()
 
 
# my_dataframe = session.table("smoothies.public.fruit_options").select(col('Fruit_Name'))
 
my_dataframe = session.table("smoothies.public.orders").filter(col("ORDER_FILLED")==False).collect()
# st.dataframe(data=my_dataframe, use_container_width=True)
if my_dataframe:
    editable_df = st.data_editor(my_dataframe)
    # ingredients_list = st.multiselect('choose upto 5 ingredients', editable_df)
    submitted = st.button('Submit')
    if submitted:
        og_dataset = session.table("smoothies.public.orders")
        edited_dataset = session.create_dataframe(editable_df)
        try:
            og_dataset.merge(edited_dataset
                             , (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'])
                             , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                            )
            st.success('Someone clicked the button', icon = '👍')
        except:
            st.write('Something went wrong.')
 
else:
    st.success('Their are no pending orders right now', icon = '👍')
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
# st.write(ingredients_list)
# st.text(ingredients_list)
 
# if ingredients_list :
#     # st.write(ingredients_list)
#     # st.text(ingredients_list)
#     ingredients_string = ''
#     for each_fruit in ingredients_list:
#         ingredients_string += each_fruit+' '

#     st.write(ingredients_string)
#     my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
#             values ('""" + ingredients_string + """','""" + name_on_order + """')"""
 
#     st.write(my_insert_stmt)
#     # st.stop()
 
#     time_to_insert = st.button('Submit Order')
 
#     if time_to_insert:
#         session.sql(my_insert_stmt).collect()
#         st.success('Your Smoothie is ordered!', icon="✅")
 
 
# Apples Cantaloupe Blueberries Elderberries Guava
