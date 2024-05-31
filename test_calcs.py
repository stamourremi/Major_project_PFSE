import numpy as np
import pandas as pd
import calcs

def test_BU_capacities():
    prop = calcs.wood_sections_props('BU_SPF_No1-No2',section='2-38x140')
    sec = calcs.SolidSawnSection(b=prop['b'][0],d=prop['d'][0],type='BU',fc=prop['fc'][0],E=prop['E'][0],ft=prop['ft'][0],
                                E05=prop['E05'][0],lb=3000,ld=3000,fv=prop['fv'][0],fb=prop['fb'][0],Ix=prop['Ix'][0])
    mr = round(sec.get_Mrx() / 1e6,1)
    vr = round(sec.get_Vr() / 1e3,1)
    pr = round(sec.get_Pr() / 1e3,1)
    EsIx = round(sec.get_EsIx() / 1e9)
    tr = round(sec.get_Tr() / 1e3,1)
    assert mr == 4.1
    assert vr == 14.7
    assert pr == 15.1
    assert EsIx == 165

def test_SS_capacities():
    prop = calcs.wood_sections_props('SS_SPF_No1',section='140x191')
    sec = calcs.SolidSawnSection(b=prop['b'][0],d=prop['d'][0],type='SS',fc=prop['fc'][0],E=prop['E'][0],ft=prop['ft'][0],
                                E05=prop['E05'][0],lb=3000,ld=3000,fv=prop['fv'][0],fb=prop['fb'][0],Ix=prop['Ix'][0])
    mr = round(sec.get_Mrx() / 1e6,1)
    vr = round(sec.get_Vr() / 1e3,1)
    pr = round(sec.get_Pr() / 1e3,1)
    EsIx = round(sec.get_EsIx() / 1e9)
    tr = round(sec.get_Tr() / 1e3)
    assert mr == 9.6
    assert vr == 25.0   
    assert pr == 138.5
    assert EsIx == 610
    assert tr == 162

def test_Glulam_capacities():
    bending_prop = calcs.wood_sections_props('BLC_SP_20f-EX',section='80x570')
    comp_prop = calcs.wood_sections_props('BLC_SP_12c-E',section='80x114')
    tension_prop = calcs.wood_sections_props('BLC_SP_14t-E',section='80x152')
    bending_sec = calcs.GlulamSection(b=bending_prop['b'][0],d=bending_prop['d'][0],E=comp_prop['Ex'][0],
                                fvx=bending_prop['fvx'][0],fbx_pos=bending_prop['fbx_pos'][0],Ix=bending_prop['Ix'][0],L=3000)
    comp_sec = calcs.GlulamSection(b=comp_prop['b'][0],d=comp_prop['d'][0],fc=comp_prop['fc'][0],E=comp_prop['Ex'][0],
                                lb=3000,ld=3000,L=3000)
    tension_sec = calcs.GlulamSection(b=tension_prop['b'][0],d=tension_prop['d'][0],ftg=tension_prop['ftg'][0],L=3000)
    mr = round(bending_sec.get_Mrx() / 1e6,1)
    vr = round(bending_sec.get_Vrx() / 1e3,1)
    wr = round(bending_sec.get_WrL_018() / 1e3)
    pr = round(comp_sec.get_Prg() / 1e3,1)
    EsIx = round(bending_sec.get_EsIx() / 1e9)
    tr = round(tension_sec.get_Trg() / 1e3)
    assert mr == 99.8
    assert vr == 47.9
    assert wr == 222   
    assert pr == 33.4
    assert EsIx == 11976
    assert tr == 147
    