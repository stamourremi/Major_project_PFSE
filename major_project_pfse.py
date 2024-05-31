import streamlit as st
import plotly.graph_objects as go
import wood_sections_module as wsm
import calcs

st.sidebar.image("logo.png")

ss_sections = wsm.solid_sawn_sections
bu_sections = wsm.bu_sections
glulam_sections = wsm.glulam_sections

st.sidebar.subheader("Section properties")
type = st.sidebar.selectbox('Type',['Glulam','Solid sawn','Builtup'])
if type == 'Solid sawn':
    specie = st.sidebar.selectbox('Specie',['DFir-L','SPF','Hem-Fir','Northern'])   
    grade = st.sidebar.selectbox('Grade',['SS','No1','No2'])
    section = st.sidebar.selectbox('Section', ss_sections)
if type == 'Builtup':   
    specie = st.sidebar.selectbox('Specie',['DFir-L','SPF','Hem-Fir','Northern'])
    grade = st.sidebar.selectbox('Grade',['SS','No1-No2','No3-Stud'])
    section = st.sidebar.selectbox('Section', bu_sections)
if type == 'Glulam':
    specie = st.sidebar.selectbox('Specie',['DFir-L','SP'])  
    grade = st.sidebar.selectbox('Grade',['24f-E','24f-EX','20f-E','20f-EX','18t-E','16c-E','20f-E','20f-EX','14t-E','12c-E'])
    section = st.sidebar.selectbox('Section', glulam_sections,index=10)

condition = st.sidebar.selectbox('Service condition',['dry','wet'])

incised_treatment = st.sidebar.selectbox('Incised treatment',['No','Yes'])

st.header(f"Wood member resistances as per CSA O86-19")
st.header(f"Section: {section}, {type} {specie} {grade}")


pr_stand = calcs.pr_xy_values(type,specie,grade,section,1.0)
pr_long = calcs.pr_xy_values(type,specie,grade,section,0.65)
pr_short = calcs.pr_xy_values(type,specie,grade,section,1.15)
fig = go.Figure()
# Plot lines
fig.add_trace(
    go.Scatter(
    x=pr_stand[0], 
    y=pr_stand[1],
    line={"color": "red"},
    name='kd = 1.0'))
fig.add_trace(
    go.Scatter(
    x=pr_long[0], 
    y=pr_long[1],
    line={"color": "blue"},
    name='kd = 0.65'))
fig.add_trace(
    go.Scatter(
    x=pr_short[0], 
    y=pr_short[1],
    line={"color": "green"},
    name='kd = 1.15'))

fig.layout.title.text = "Factored compressive resistance"
fig.layout.xaxis.title = "Pr, kN"
fig.layout.yaxis.title = "Member height, mm"
st.plotly_chart(fig)

tr_stand = calcs.tr_xy_values(type,specie,grade,section,1.0)
tr_long = calcs.tr_xy_values(type,specie,grade,section,0.65)
tr_short = calcs.tr_xy_values(type,specie,grade,section,1.15)
fig_tr = go.Figure()
# Plot lines
fig_tr.add_trace(
    go.Scatter(
    x=tr_stand[1], 
    y=tr_stand[0],
    line={"color": "red"},
    name='kd = 1.0'))
fig_tr.add_trace(
    go.Scatter(
    x=tr_long[1], 
    y=tr_long[0],
    line={"color": "blue"},
    name='kd = 0.65'))
fig_tr.add_trace(
    go.Scatter(
    x=tr_short[1], 
    y=tr_short[0],
    line={"color": "green"},
    name='kd = 1.15'))
fig_tr.layout.title.text = "Factored tensile resistance"
fig_tr.layout.xaxis.title = "Tr, kN"
fig_tr.layout.yaxis.title = "Gross Area ratio, An/Ag"
st.plotly_chart(fig_tr)

mr_stand = calcs.mr_xy_values(type,specie,grade,section,1.0)
mr_long = calcs.mr_xy_values(type,specie,grade,section,0.65)
mr_short = calcs.mr_xy_values(type,specie,grade,section,1.15)
fig_mr = go.Figure()
# Plot lines
fig_mr.add_trace(
    go.Scatter(
    x=mr_stand[0], 
    y=mr_stand[1],
    line={"color": "red"},
    name='kd = 1.0'))
fig_mr.add_trace(
    go.Scatter(
    x=mr_long[0], 
    y=mr_long[1],
    line={"color": "blue"},
    name='kd = 0.65'))
fig_mr.add_trace(
    go.Scatter(
    x=mr_short[0], 
    y=mr_short[1],
    line={"color": "green"},
    name='kd = 1.15'))
fig_mr.layout.title.text = "Factored moment resistance"
fig_mr.layout.xaxis.title = "Unsupported length lu, mm"
fig_mr.layout.yaxis.title = "Mr, kNm"
st.plotly_chart(fig_mr)

vr_stand = calcs.vr_xy_values(type,specie,grade,section,1.0)
vr_long = calcs.vr_xy_values(type,specie,grade,section,0.65)
vr_short = calcs.vr_xy_values(type,specie,grade,section,1.15)
fig_vr = go.Figure()
# Plot lines
fig_vr.add_trace(
    go.Scatter(
    x=vr_stand[1], 
    y=vr_stand[0],
    line={"color": "red"},
    name='kd = 1.0'))
fig_vr.add_trace(
    go.Scatter(
    x=vr_long[1], 
    y=vr_long[0],
    line={"color": "blue"},
    name='kd = 0.65'))
fig_vr.add_trace(
    go.Scatter(
    x=vr_short[1], 
    y=vr_short[0],
    line={"color": "green"},
    name='kd = 1.15'))
fig_vr.layout.title.text = "Factored shear resistance"
fig_vr.layout.xaxis.title = "Vr, kN"
fig_vr.layout.yaxis.title = "Gross Area ratio, An/Ag"
st.plotly_chart(fig_vr)