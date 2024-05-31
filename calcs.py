from dataclasses import dataclass

import pandas as pd

def height_range(start_h: int, stop_h: int, step_h: int) -> list:
    """
    Function that returns the height range
    """
    stop_height = stop_h + step_h
    list_h = list(range(start_h,stop_height,step_h))
    return list_h

def calculate_pr_at_given_height(height: int, type_species_grade: str, section: str, kd: float) -> float:
    """
    Function that return the axial resistance of a wood section at a given height
    """
    type, specie, grade = type_species_grade.split('_')
    wood_prop = wood_sections_props(type_species_grade,section=section)
    if height == 0:
        height = height +1
    
    if type != 'BLC':
        sec = SolidSawnSection(b=wood_prop['b'][0],d=wood_prop['d'][0],type=type,specie=specie,fc=wood_prop['fc'][0],
                            E05=wood_prop['E05'][0],lb=height,ld=height,kd=kd)
        pr = round(sec.get_Pr() / 1e3,1)
    if type == 'BLC':
        sec = GlulamSection(b=wood_prop['b'][0],d=wood_prop['d'][0],fc=wood_prop['fc'][0],
                            E=wood_prop['Ex'][0],lb=height,ld=height,L=height,kd=kd)
        pr = round(sec.get_Prg() / 1e3,1)
    return pr

def calculate_tr_at_given_vol_ratio(vol_ratio: int, type_species_grade: str, section: str, kd: float) -> float:
    """
    Function that return the axial resistance of a wood section at a given height
    """
    type, specie, grade = type_species_grade.split('_')
    wood_prop = wood_sections_props(type_species_grade,section=section)
    A_trous = wood_prop['A'][0] * (1 - vol_ratio)
    if type != 'BLC':
        sec = SolidSawnSection(b=wood_prop['b'][0],d=wood_prop['d'][0],type=type,specie=specie,ft=wood_prop['ft'][0],A_trous=A_trous,kd=kd)
        tr = round(sec.get_Tr() / 1e3,1)
    if type == 'BLC':
        sec = GlulamSection(b=wood_prop['b'][0],d=wood_prop['d'][0],ftg=wood_prop['ftg'][0],ftn=wood_prop['ftn'][0],A_trous=A_trous,kd=kd)
        if vol_ratio == 0:    
            tr = round(sec.get_Trg() / 1e3,1)
        if vol_ratio != 0:    
            tr = round(sec.get_Trn() / 1e3,1)
    return tr

def calculate_vr_at_given_vol_ratio(vol_ratio: int, type_species_grade: str, section: str, kd: float) -> float:
    """
    Function that return the axial resistance of a wood section at a given height
    """
    type, specie, grade = type_species_grade.split('_')
    wood_prop = wood_sections_props(type_species_grade,section=section)
    A_trous = wood_prop['A'][0] * (1 - vol_ratio)
    if type != 'BLC':
        sec = SolidSawnSection(b=wood_prop['b'][0],d=wood_prop['d'][0],type=type,specie=specie,fv=wood_prop['fv'][0],A_trous=A_trous,kd=kd)
        vr = round(sec.get_Vr() / 1e3,1)
    if type == 'BLC':
        sec = GlulamSection(b=wood_prop['b'][0],d=wood_prop['d'][0],fvx=wood_prop['fvx'][0],A_trous=A_trous,kd=kd)    
        vr = round(sec.get_Vrx() / 1e3,1)
    return vr

def calculate_mr_at_given_l(length: int, type_species_grade: str, section: str, kd: float) -> float:
    """
    Function that return the axial resistance of a wood section at a given height
    """
    type, specie, grade = type_species_grade.split('_')
    wood_prop = wood_sections_props(type_species_grade,section=section)
    
    if type != 'BLC':
        sec = SolidSawnSection(b=wood_prop['b'][0],d=wood_prop['d'][0],type=type,specie=specie,fb=wood_prop['fb'][0],lu=length,lat_support=None,E=wood_prop['E'][0],kd=kd)
        mr = round(sec.get_Mrx() / 1e6,1)
    if type == 'BLC':
        if length == 0:
            length = 1
        sec = GlulamSection(b=wood_prop['b'][0],d=wood_prop['d'][0],fbx_pos=wood_prop['fbx_pos'][0],lu=length,lat_support=None,E=wood_prop['Ex'][0],L=length,kd=kd)    
        mr = round(sec.get_Mrx() / 1e6,5)
    return mr

def pr_xy_values(type: str, specie: str, grade: str, section: str,kd: float) -> tuple[list]:
    if type == 'Solid sawn':
        type_species_grade = 'SS_' + specie + '_' + grade
    if type == 'Builtup':
        type_species_grade = 'BU_' + specie + '_' + grade
    if type == 'Glulam':
        type_species_grade = 'BLC_' + specie + '_' + grade    
    
    if type == 'Builtup':
        b = int(section.split('-')[0]) * 38
        max_height = min(b,int(section.split('x')[1])) * 50
    else:
        max_height = min(int(section.split('x')[0]),int(section.split('x')[1])) * 50

    heights = height_range(0,max_height,200)
    pr_values = []
    for h in heights:
        pr_values.append(calculate_pr_at_given_height(h,type_species_grade,section,kd))
    return pr_values,heights

def tr_xy_values(type: str, specie: str, grade: str, section: str, kd: float) -> tuple[list]:
    if type == 'Solid sawn':
        type_species_grade = 'SS_' + specie + '_' + grade
    if type == 'Builtup':
        type_species_grade = 'BU_' + specie + '_' + grade
    if type == 'Glulam':
        type_species_grade = 'BLC_' + specie + '_' + grade    

    vol_ratios = [0.75,1.0]
    tr_values = []
    for vol in vol_ratios:
        tr_values.append(calculate_tr_at_given_vol_ratio(vol,type_species_grade,section,kd))
    return vol_ratios,tr_values

def mr_xy_values(type: str, specie: str, grade: str, section: str, kd: float) -> tuple[list]:
    if type == 'Solid sawn':
        type_species_grade = 'SS_' + specie + '_' + grade
    if type == 'Builtup':
        type_species_grade = 'BU_' + specie + '_' + grade
    if type == 'Glulam':
        type_species_grade = 'BLC_' + specie + '_' + grade    

    if type == 'Builtup':
        b = int(section.split('-')[0]) * 38
    else:
        b = int(section.split('x')[0])
    d = int(section.split('x')[1])

    Lmax = min(int(25**2 * b**2 / d),10000)
    step = int(Lmax / 20)
    lengths = list(range(0,Lmax,step))
    mr_values = []
    for length in lengths:
        mr_values.append(calculate_mr_at_given_l(length,type_species_grade,section,kd))
    return lengths,mr_values

def vr_xy_values(type: str, specie: str, grade: str, section: str, kd: float) -> tuple[list]:
    if type == 'Solid sawn':
        type_species_grade = 'SS_' + specie + '_' + grade
    if type == 'Builtup':
        type_species_grade = 'BU_' + specie + '_' + grade
    if type == 'Glulam':
        type_species_grade = 'BLC_' + specie + '_' + grade    

    vol_ratios = [0.75,1.0]
    vr_values = []
    for vol in vol_ratios:
        vr_values.append(calculate_vr_at_given_vol_ratio(vol,type_species_grade,section,kd))
    return vol_ratios,vr_values

def wood_sections_props(type_species_grade: str, bmin: int = 0, dmin: int = 0, bmax: int = 1e6, dmax: int = 1e6,
                        d_b_ratio_min = 0, d_b_ratio_max = 1e6, ref: str = 'CSA O86', section: str = None) -> pd.DataFrame:
    """
    Functions that return a dataframe that contains the sections and wood properties for analysis
    Type_species_grade must have this format
    
    type: SS = "Solid Sawn":, BU = "Builtup", BLC = "Bois Lamelle colle", "ACI" = Acier
    Species: Nor = "Northern", SPF, DFir-L, LVL, PAR, GEN (SCL)
    grade: Light Framing: (SS, No1/No2, No3/Stud, MSR 2100Fb-1.8E(SPf only)), Beam and stringer and Post and timber: (SS,No1,No2), SCL: (2.0E, 1.8E)
    Use ref for specifying if glulam sections are based on CSA O86, or Art Massif or other manufacturer

    For SCL members, use BU or SS: for example; SS_LVL_2.0E or BU_PAR_1.8E
    """

    type = type_species_grade.split('_')[0]
    species = type_species_grade.split('_')[1]
    grade = type_species_grade.split('_')[2]

    if type == 'SS' or type == 'BU':
        IDX = pd.IndexSlice
        wood_prop_df = pd.read_excel(r"C:\Users\stamo\pycode\Projects\Major_project_PFSE\wood properties.xlsx",'Solid sawn lumber and SCL prop',index_col=[0,1,2])
        wood_prop_df = wood_prop_df.loc[IDX[:, species, grade], :]
        sections_df = pd.read_excel(r"C:\Users\stamo\pycode\Projects\Major_project_PFSE\wood properties.xlsx",'Solid Sawn sections',index_col=[6])
        if section != None:
            sections_df = sections_df.loc[sections_df['Section'] == section]
        else:
            sections_df = sections_df.loc[(sections_df['b'] <= bmax) & (sections_df['d'] <=  dmax) & 
                (sections_df['b'] >=  bmin) & (sections_df['d'] >=  dmin) & (sections_df['d/b'] >=  d_b_ratio_min) & (sections_df['d/b'] <=  d_b_ratio_max)
                & (sections_df['Ref'] == ref)]
        wood_sections_props = sections_df.merge(right=wood_prop_df,left_index=True,right_on='Member type').sort_values('A').reset_index()

    if type == 'BLC':
        IDX = pd.IndexSlice
        wood_prop_df = pd.read_excel(r"C:\Users\stamo\pycode\Projects\Major_project_PFSE\wood properties.xlsx",'Glulam prop',index_col=[0,1])
        wood_prop_df = pd.DataFrame(wood_prop_df.loc[IDX[species, grade], :]).T
        sections_df = pd.read_excel(r"C:\Users\stamo\pycode\Projects\Major_project_PFSE\wood properties.xlsx",'Glulam sections')
        if section != None:
            sections_df = sections_df.loc[sections_df['Section'] == section]
        else:
            sections_df = sections_df.loc[(sections_df['b'] <= bmax) & (sections_df['d'] <=  dmax) & 
                (sections_df['b'] >=  bmin) & (sections_df['d'] >=  dmin) & (sections_df['d/b'] >=  d_b_ratio_min)
                & (sections_df['d/b'] <=  d_b_ratio_max) & (sections_df['Ref'] == ref)].reset_index(drop=True)
        sections_df['Species'] = species
        sections_df['Grade'] = grade
        wood_sections_props = sections_df.merge(right=wood_prop_df, left_on=['Species','Grade'], right_index=True).sort_values('A').reset_index(drop=True)
    
    wood_sections_props['Type'] = type
    return wood_sections_props

@dataclass
class SolidSawnSection:
    """
    A data type to describe the data required to compute the capacity of a solid sawn section (SCL, solid sawn, builtup)
    
    Notes: 
        - All values are in mm and N
    """
    b: int
    d: int
    type: str # Inform the algorithm how to apply factors for BU sections such as kh, kz, etc
    specie: str = None # Used to determine kz, kb factors for SCL
    Ix: float = 0
    Iy: float = 0
    fb: float = 0
    fv: float = 0
    fc: float = 0
    fcp: float = 0
    ft: float = 0
    E: int = 0
    E05: int = 0
    kd: float = 1.0
    condition: str = 'dry'
    incised_treatment: bool = False
    lat_support: str = 'continuous'
    case: str = 'single' # Can be case 1 or case 2
    A_trous: int = 0
    lb: int = 0
    ld: int = 0
    keb: float = 1.0
    ked: float = 1.0
    lu: int = 0
    Le_factor: float = 1.92
    kx = 1.0
    l_bearing: int = 1
    KB: float = 1.0 # KB = 1.0 if bearing area is at the end of the member or in area of high bending stress
    kzcp: float = 1.0

    def get_ks(self,factor: str):
        if self.specie not in ['LVL','PAR','GEN'] and ((self.condition == 'wet' and self.b <= 89) or (self.condition == 'wet' and self.type == 'BU')):
            ksb = 0.84
            ksv = 0.96
            ksc = 0.69
            kscp = 0.67
            kst = 0.84
            kse = 0.94
        elif self.condition == 'wet' and self.b > 89 and self.specie not in ['LVL','PAR','GEN']:
            ksb = 1.0
            ksv = 1.0
            ksc = 0.91
            kscp = 0.67
            kst = 1.0
            kse = 1.0
        else:
            ksb = 1.0
            ksv = 1.0
            ksc = 1.0
            kscp = 1.0
            kst = 1.0
            kse = 1.0
        if factor == 'ksb':
            return ksb
        elif factor == 'ksv':
            return ksv
        elif factor == 'ksc':
            return ksc
        elif factor == 'kscp':
            return kscp
        elif factor == 'kst':
            return kst
        elif factor == 'kse':
            return kse

    def get_kt(self,factor: str):    
        if self.incised_treatment == True and self.condition == 'dry' and self.b <= 89:
            kte = 0.9
            kt = 0.75
        elif self.incised_treatment == True and self.condition == 'wet' and self.b <= 89:
            kte = 0.95
            kt = 0.85
        else:
            kte = 1.0
            kt = 1.0
        if factor == 'kte':
            return kte
        elif factor == 'kt':
            return kt

    def get_kh(self):
        if (self.type == 'BU' and self.specie not in ['LVL','PAR','GEN']) or self.case == 'Case1':
            return 1.1
        elif self.type == 'BU' and self.specie in ['LVL','PAR','GEN'] and self.b >= 132:
            return 1.04
        elif self.case == 'case 2':
            return 1.4
        else:
            return 1.0
    
    def get_kzb(self) -> float:
        if self.b >= 114 and self.specie not in ['LVL','PAR','GEN'] and self.type != 'BU':
            if self.d == 140 or self.d == 191:
                return 1.3
            elif self.d == 241:
                return 1.2
            elif self.d == 292:
                return 1.1
            elif self.d == 343:
                return 1.0
            elif self.d >= 387:
                return 0.9
        if (self.b >= 38 and self.b <= 64 and self.specie not in ['LVL','PAR','GEN']) or (self.type == 'BU' and self.specie not in ['LVL','PAR','GEN']):
            if self.d == 89:
                return 1.7
            elif self.d == 140:
                return 1.4
            elif self.d == 184:
                return 1.2
            elif self.d == 235:
                return 1.1
            elif self.d == 286:
                return 1.0
            
        if self.specie in ['LVL','PAR','GEN']:
            return (305/self.d) ** (1/9)
    
    def get_kzv(self):
        if self.specie not in ['LVL','PAR','GEN']:
            return self.get_kzb()
        elif self.specie in ['LVL','PAR','GEN']:
            return 1.0
    
    def get_kzt(self) -> float:
        if self.specie not in ['LVL','PAR','GEN']:
            if self.d <= 89:
                return 1.5
            elif self.d == 114:
                return 1.4
            elif self.d == 140:
                return 1.3
            elif self.d >= 184 and self.d <=191:
                return 1.2
            elif self.d >= 235 and self.d <=241:
                return 1.1
            elif self.d >= 286 and self.d <=292:
                return 1.0
            elif self.d >= 337 and self.d <=343:
                return 0.9
            elif self.d > 387:
                return 0.8
        else:
            return 1.0

    def get_kL(self) -> float:
        if self.lat_support == 'continuous' or self.d / self.b <= 4:
            return 1.0
        else:
            Le = self.Le_factor * self.lu
            CB = (Le * self.d / self.b ** 2) ** 0.5
            CK = (0.97 * self.E * self.get_ks('kse') * self.get_kt('kte') / self.get_Fb()) ** 0.5
            if CB <= 10:
                return 1.0
            elif CB > 10 and CB <= CK:
                return 1 - 1/3 * (CB / CK) ** 4
            elif CB > CK and CB <= 50:
                return 0.65 * self.E * self.get_ks('kse') * self.get_kt('kte') / (CB**2 * self.get_Fb() * self.kx)
            elif CB > 50:
                return 0

    def get_kzcb(self) -> float:
        if self.specie not in ['LVL','PAR','GEN']:
            kzcb = min(6.3 * (self.b * self.lb) ** -0.13, 1.3)
        elif self.specie in ['LVL','PAR','GEN']:
            kzcb = 1.0
        return kzcb
    
    def get_kzcd(self) -> float:
        if self.specie not in ['LVL','PAR','GEN']:
            kzcd = min(6.3 * (self.d * self.ld) ** -0.13, 1.3)
        elif self.specie in ['LVL','PAR','GEN']:
            kzcd = 1.0
        return kzcd
    
    def get_KCb(self) -> float:
        """
        Returns a float representing the slenderness factor
        """
        Ccb = self.keb * self.lb / self.b
        if Ccb <=50:    
            Kcb = (1.0 + (self.get_Fc_Eprime() * self.get_kzcb() * Ccb**3))**-1
        else:
            Kcb = 0
            # print('Ccb > 50')
        return Kcb

    def get_KCd(self) -> float:
        """
        Returns a float representing the slenderness factor
        """
        Ccd = self.ked * self.ld / self.d
        if Ccd <= 50:    
            Kcd = (1.0 + (self.get_Fc_Eprime() * self.get_kzcd() * Ccd**3))**-1
        else:
            Kcd = 0
            # print('Ccd > 50')
        return Kcd

    def get_Fb(self) -> float:
        Fb = self.fb * self.kd * self.get_kh() * self.get_ks('ksb') * self.get_kt('kt')
        return Fb

    def get_Fc(self) -> float:
        if self.type == 'BU':    
            Fc = self.fc * self.kd * 1.0 * self.get_ks('ksc') * self.get_kt('kt')
        else:
            Fc = self.fc * self.kd * self.get_kh() * self.get_ks('ksc') * self.get_kt('kt')
        return Fc

    def get_Ft(self) -> float:
        Ft = self.ft * self.kd * self.get_kh() * self.get_ks('kst') * self.get_kt('kt')
        return Ft

    def get_Fv(self) -> float:
        Fv = self.fv * self.kd * self.get_kh() * self.get_ks('ksv') * self.get_kt('kt')
        return Fv
    
    def get_Fcp(self) -> float:
        Fcp = self.fcp * self. kd * self.get_ks('kscp') * self.get_kt('kt')
        return Fcp
    
    def get_EsIx(self) -> int:
        return self.E * self.get_ks('kse') * self.get_kt('kte') * self.Ix

    def get_Sx(self) -> int:
        Sx = self.b * self.d ** 2 / 6
        return Sx

    def get_Mrx(self) -> float:
        """
        Returns the factored compressive resistance parallel-to-grain
        as described in Cl. 7.5.8
        """
        Mrx = 0.9 * self.get_Fb() * self.get_Sx() * self.get_kzb() * self.get_kL()
        return Mrx
    
    def get_Vr(self) -> float:
        """"
        Returns the factored shear resistance
        """
        An = self.b * self.d - self.A_trous
        Vr = 0.9 * self.get_Fv() * 2/3 * An * self.get_kzv()
        return Vr

    def get_An(self) -> float:
        return self.b * self.d - self.A_trous

    def get_Tr(self) -> float:
        Tr = 0.9 * self.get_Ft() * self.get_An() * self.get_kzt()
        return Tr

    def get_Pr(self) -> float:
        """
        Returns the factored compressive resistance parallel-to-grain
        """
        phi_Fc = 0.8 * self.get_Fc()
        A = self.b * self.d
        Prb = phi_Fc * A * self.get_kzcb() * self.get_KCb()
        Prd = phi_Fc * A * self.get_kzcd() * self.get_KCd()
        if self.type == 'BU': 
            P_r = min(0.6*Prb, Prd)
        elif self.type != 'BU':    
            P_r = min(Prb, Prd)
        return P_r

    def get_Fc_Eprime(self) -> float:
        """
        Returns a float representing the strength to stiffness ratio
        """
        Eprime = 35 * self.E05 * self.get_ks('kse') * self.get_kt('kte')
        Fc_Eprime = self.get_Fc() / Eprime
        return Fc_Eprime

    def get_qr(self):
        qr = 0.8 * self.get_Fcp * self.b * self.KB * self.kzcp
        return qr

@dataclass
class GlulamSection:
    """
    A data type to describe the data required to compute the capacity of a
    glulam beam as described in CSA O86-17.
    
    Notes: 
        - All values are in mm and N
    """
    b: int
    d: int
    Ix: float = 0
    Iy: float = 0
    fbx_pos: float = 0
    fvx: float = 0
    fc: float = 0
    fcpx_pos: float = 0
    ftn: float = 0
    ftg: float = 0
    E: int = 0
    kd: float = 1.0
    condition: str = 'dry'
    incised_treatment: bool = False
    lat_support: str = 'continuous'
    case: str = 'single' # Can be case 1 or case 2
    A_trous: int = 0
    lb: int = 0
    ld: int = 0
    keb: float = 1.0
    ked: float = 1.0
    lu: int = 0
    Le_factor: float = 1.92
    kx = 1.0
    l_bearing: int = 1
    KB: float = 1.0 # KB = 1.0 if bearing area is at the end of the member or in area of high bending stress
    kzcp: float = 1.0
    Cv: float = 3.69
    L: int = 0 # in mm

    def get_ks(self,factor: str):
        if self.condition == 'wet':
            ksb = 0.8
            ksv = 0.87
            ksc = 0.75
            kscp = 0.67
            kst = 0.75
            kse = 0.9            
        else:
            ksb = 1.0
            ksv = 1.0
            ksc = 1.0
            kscp = 1.0
            kst = 1.0
            kse = 1.0
        if factor == 'ksb':
            return ksb
        elif factor == 'ksv':
            return ksv
        elif factor == 'ksc':
            return ksc
        elif factor == 'kscp':
            return kscp
        elif factor == 'kst':
            return kst
        elif factor == 'kse':
            return kse

    def get_kt(self,factor: str):    
        if self.incised_treatment == True and self.condition == 'dry' and self.b <= 89:
            kte = 0.9
            kt = 0.75
        elif self.incised_treatment == True and self.condition == 'wet' and self.b <= 89:
            kte = 0.95
            kt = 0.85
        else:
            kte = 1.0
            kt = 1.0
        if factor == 'kte':
            return kte
        elif factor == 'kt':
            return kt

    def get_kh(self):
        if self.case == 'Case1':
            return 1.1
        elif self.case == 'case 2':
            return 1.4
        else:
            return 1.0
    
    def get_kL(self) -> float:
        if self.lat_support == 'continuous' or self.d / self.b <= 2.5:
            return 1.0
        else:
            Le = self.Le_factor * self.lu
            CB = (Le * self.d / self.b ** 2) ** 0.5
            CK = (0.97 * self.E * self.get_ks('kse') * self.get_kt('kte') / self.get_Fbx()) ** 0.5
            if CB <= 10:
                return 1.0
            elif CB > 10 and CB <= CK:
                return 1 - 1/3 * (CB / CK) ** 4
            elif CB > CK and CB <= 50:
                return 0.65 * self.E * self.get_ks('kse') * self.get_kt('kte') / (CB**2 * self.get_Fbx() * self.kx)
            elif CB > 50:
                return 0

    def get_kzbg(self) -> float:
        """
        Returns the size factor for solid sawn lumber
        """
        kzbg = min((130 / self.b) ** (1/10) * (610 / self.d) ** (1/10) * (9100 / self.L) ** (1/10), 1.3)
        return kzbg
    
    def get_kzcg(self):
        return min(0.68*self.get_Z()**-0.13,1.)
    
    def get_Kc(self) -> float:
        """
        Returns a float representing the slenderness factor
        """
        Cc = max(self.keb * self.lb / self.b, self.ked * self.ld / self.d)
        if Cc > 50:
            # print('Cc > 50')
            return 0
        
        if Cc <=50:
            Kc = (1.0 + (self.get_Fc_Eprimeg() * self.get_kzcg() * Cc**3))**-1
            return Kc
    
    def get_Ftn(self) -> float:
        Ftn = self.ftn * self.kd * self.get_kh() * self.get_ks('kst') * self.get_kt('kt')
        return Ftn
    
    def get_Ftg(self) -> float:
        Ftg = self.ftg * self.kd * self.get_kh() * self.get_ks('kst') * self.get_kt('kt')
        return Ftg
    
    def get_Fbx(self) -> float:
        Fb = self.fbx_pos * self.kd * self.get_kh() * self.get_ks('ksb') * self.get_kt('kt')
        return Fb

    def get_Fc(self) -> float:
        Fc = self.fc * self.kd * self.get_kh() * self.get_ks('ksc') * self.get_kt('kt')
        return Fc
    
    def get_Fcp(self) -> float:
        Fcp = self.fcpx_pos * self. kd * self.get_ks('kscp') * self.get_kt('kt')
        return Fcp

    def get_Fvx(self) -> float:
        Fv = self.fvx * self.kd * self.get_kh() * self.get_ks('ksv') * self.get_kt('kt')
        return Fv
    
    def get_EsIx(self) -> int:
        return self.E * self.get_ks('kse') * self.get_kt('kte') * self.Ix
    
    def get_Sx(self) -> int:
        Sx = self.b * self.d ** 2 / 6
        return Sx

    def get_Z(self): # in m
        return self.b * self.d * self.L * 1e-9
    
    def get_Mrx(self) -> float:
        """
        Returns the factored compressive resistance parallel-to-grain
        as described in Cl. 7.5.8
        """
        Mrx = 0.9 * self.get_Fbx() * self.get_Sx() * min(self.get_kzbg(), self.get_kL())
        return Mrx
    
    def get_Vrx(self):
        return 0.9 * self.get_Fvx() * 2/3 * (self.b * self.d - self.A_trous)
    
    def get_Wr(self) -> float:
        """"
        Returns the factored shear resistance
        """
        Ag = self.b * self.d
        Wr = 0.9 * self.get_Fvx() * 0.48 * Ag * self.Cv * self.get_Z() ** -0.18
        return Wr
    
    def get_WrL_018(self) -> float:
        """"
        Returns the factored shear resistance
        """
        Ag = self.b * self.d
        WrL_018 = 0.9 * self.get_Fvx() * 0.48 * Ag * self.Cv * (self.b/1000 * self.d/1000) ** -0.18
        return WrL_018

    def get_An(self) -> float:
        return self.b * self.d - self.A_trous

    def get_Trn(self) -> float:
        Trn = 0.9 * self.get_Ftn() * self.get_An()
        return Trn
    
    def get_Trg(self) -> float:
        Trg = 0.9 * self.get_Ftg() * self.b * self.d
        return Trg
    
    def get_Prg(self) -> float:
        """
        Returns the factored compressive resistance parallel-to-grain
        as described in Cl. 7.5.8
        """
        phi_Fc = 0.8 * self.get_Fc()
        A = self.b * self.d
        Prg = phi_Fc * A * self.get_kzcg() * self.get_Kc()
        return Prg
    
    def get_Fc_Eprimeg(self) -> float:
        """
        Returns a float representing the strength to stiffness ratio
        """
        Eprimeg = 35 * self.E * 0.87 * self.get_ks('kse') * self.get_kt('kte')
        Fc_Eprimeg = self.get_Fc() / Eprimeg
        return Fc_Eprimeg
    
    def get_qr(self):
        qr = 0.8 * self.get_Fcp() * self.b * self.KB * self.kzcp
        return qr