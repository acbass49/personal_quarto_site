# type: ignore
# flake8: noqa
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#| eval: false
python -m pip install survey_tools
#
#
#
#
#
#
#
import pandas as pd
import numpy as np
import survey_tools as st

link = 'https://csed.byu.edu/00000183-a4c5-d2da-abe3-feed7be30001/2021data'
data = pd.read_stata(link)
print(data.shape)
data.head()
#
#
#
#
#
#
#
st.get_names(data, r'[Ee][Dd]')
#
#
#
#
#
#
#
#
#
st.tabs(data, 'educ', dropna=False)
#
#
#
#
#
#
st.tabs(data, 'educ', dropna=False, wts="weight")
#
#
#
#
#
st.tabs(data, 'educ', dropna=False, wts="weight", display='column')
#
#
#
#
#
#
#
data['educ_rc'] = st.recode(
    data, 
    'educ',
    '"No HS"=0;'\
    '"High school graduate"=0;'\
    '"Some college"=0;'\
    '"2-year"=0;'\
    '"4-year"=1;'\
    '"Post-grad"=1;'\
)

st.tabs(data, 'educ_rc')
#
#
#
#
#
data['educ_numbers'] = data.educ.cat.codes
data['educ_rc'] = st.recode(
    data, 
    'educ_numbers',
    '0:3="No B";4:5="B+"'
)

st.tabs(data, 'educ_rc')
#
#
#
#
#
#
#
#
data['newsint'] = data.newsint.cat.codes
data['newsint_rc'] = st.recode(data, 'newsint', "0='High';1:5='Low'")
st.tabs(data, 'newsint_rc')
#
#
#
#
#
#
#
st.tabs(data, 'newsint_rc', 'educ_rc', wts = "weight", display='column')
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
data['age'] = 2021 - data.birthyr
data['age_rc'] = recode(data, 'age', '0:30=1;31:45=2;46:65=3;66:120=4')
tabs(data, 'age_rc', display='column')
#
#
#
data['gender_rc'] = recode(data, 'gender', '"Male"=1;"Female"=2')
tabs(data, 'gender_rc', display='column')
#
#
#
#
#
true_props = pd.DataFrame({
    'Names':['gender','gender','age_rc','age_rc','age_rc','age_rc',],
    'Levels':['Male', 'Female',1,2,3,4],
    'Proportions':[0.5,0.5,0.2,0.25,0.35,0.2],
})

data_w_new_wts = rake_weight(data, true_props, weight_nm='new_weight')
#
#
#
#
