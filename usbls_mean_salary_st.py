# type "streamlit run usbls_mean_salary_st.py" at the command prompt to run

import pandas as pd
import streamlit as st
import plotly.graph_objects as go

## Data input and readying
job_titles_df = pd.read_csv('job_cat_titles.csv')
job_cat_titles = job_titles_df.iloc[:,1].to_list()

# import salary data
states_only_df = pd.read_csv('normalized_mean_salary.csv')

states_only_df = states_only_df.rename(columns={'PRIM_STATE':'State','A_MEAN':'Mean Salary','norm_sal_mean':'Normalized Mean Salary'})

print(job_cat_titles)
print(states_only_df.head(3))



## Streamlit display functions

# streamlit selectbox for selecting which employement category to display
job_cat = st.sidebar.selectbox('Select job category of interest', job_cat_titles, index=(0))

# subselect the data for the selected state from the dataframe
df_for_display = states_only_df[(states_only_df['OCC_TITLE'] == job_cat)][['State','Mean Salary','Normalized Mean Salary']]


st.title('US Mean Salary by Job Category - from May 2020 US Bureau of Labor Statistics Data')
st.markdown('https://www.bls.gov/oes/current/oessrcst.htm#top')

# Choropleth #1 - unnormalized data
fig1 = go.Figure(data=go.Choropleth(locations = df_for_display['State'],
                                z = df_for_display['Mean Salary'],
                                locationmode = 'USA-states',
                                colorscale = 'rdbu',
                                colorbar_title = 'Mean Salary: $'))

fig1.update_layout(
    title_text = f'Median Salary by State for:<br>{job_cat}',
    geo_scope = 'usa')

st.plotly_chart(fig1)


# Choropleth #2 - normalized data
fig2 = go.Figure(data=go.Choropleth(locations = df_for_display['State'],
                                z = df_for_display['Normalized Mean Salary'],
                                locationmode = 'USA-states',
                                colorscale = 'rdbu',
                                colorbar_title = "Norm'd Mean: $"))

fig2.update_layout(
    title_text = f'Median Salary by State Normalized by<br>Cost of Living Index for:<br>{job_cat}',
    geo_scope = 'usa')

st.plotly_chart(fig2)

st.markdown("Salary data is normalized by dividing the mean salary by the cost of living index for each state.")
st.title("")
st.markdown("        **Here's the same data displayed in a table**")



# display the dataframe for the user
df_for_viewing = df_for_display.copy()
df_for_viewing.set_index('State', inplace=True)
st.write(df_for_viewing.style.format('${0:,.0f}'))

