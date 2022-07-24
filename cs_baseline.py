import numpy as np

default_income_bands  = [40594,81188,121782,162376,202970]
default_tapers =  {}
default_tapers["12l",1] = [.17,.15,.12,.10,.07,0]
default_tapers["12l",2] = [.24,.23,.20,.18,.10,0]
default_tapers["12l",3] = [.27,.26,.25,.24,.18,0]

default_tapers["13p",1] = [.23,.22,.12,.10,.09,0]
default_tapers["13p",2] = [.29,.28,.25,.20,.13,0]
default_tapers["13p",3] = [.32,.31,.30,.29,.20,0]

#TODO replace  with loop
default_tapers["mix",1] = [0] * len(default_tapers["12l",1])
default_tapers["mix",2] = np.divide( np.add(default_tapers["12l",2]  , default_tapers["13p",2]),2)
default_tapers["mix",3] = np.divide( np.add(default_tapers["12l",3]  , default_tapers["13p",3]),2)

#convert care  percentage (must be between 0 and  1 ) to cost percentage
def  care_to_cost(care_pct):
  #Implement legislated rounding rules. Care Percent less than 0.5, round down. 
  #Care Percent more than 0.5, round up.;
  
  if (care_pct < 0.5): care_pct = math.floor(100*care_pct)/100 
  else:care_pct = math.ceil ( 100*care_pct)/100
  
  #legislation
  if   (care_pct <  0.14) : cost_pct = 0
  elif (care_pct <  0.35) : cost_pct = 0.24 
  elif (care_pct <  0.48) : cost_pct = 0.25 + 2*(care_pct-0.35) 
  elif (care_pct <= 0.52) : cost_pct = 0.50 
  elif (care_pct <= 0.65) : cost_pct = 0.51 + 2*(care_pct-0.53) 
  elif (care_pct <= 0.86) : cost_pct = 0.76 
  elif (care_pct <= 1.00) : cost_pct = 1 
  return(round(cost_pct,2))


#get the cost of children based on income  ages of kids and number of kids. takes a list if income bands to iterate through
def coc(num_kids, ages, income, year, income_bands , tapers=default_tapers ) :
  
  #cap num kids at 3
  num_kids  = min(num_kids,3)  
  cost=0
  prev_band = 0 
  i = 0
  
  #find index of  income
  for band in income_bands:
    #if we reach the relevant band calculate the remaining costs    
    if (income <= band) :
      cost = cost + (income - prev_band) * tapers[ages,num_kids][i]
      
      return(cost)
    
    #otherwise use the whole income band to calculate the cost
    cost = cost + (band - prev_band) * tapers[ages,num_kids][i]
    
    i = i+1
    prev_band = band
  
  return(cost)

#get the cost of children based on income  ages of kids and number of kids. takes a list if income bands to iterate through
def coc2(kids_12l,kids_13p, income, income_bands= default_income_bands, tapers=default_tapers ) :
  
  #cap num kids at 3
  num_kids  = min(kids_12l + kids_13p,3)  
  
  if (kids_12l == 0 and kids_13p == 0) : return(0)
  if (kids_12l>0 and kids_13p == 0) : ages =  "12l"
  elif (kids_12l == 0 and kids_13p > 0) : ages =  "13p"
  elif (kids_12l > 0 and kids_13p > 0) : ages =  "mix"
  else : ages =  "err"
  
  cost = 0
  prev_band = 0 
  i = 0
  #find index of  income
  for band in income_bands:
    #if we reach the relevant band calculate the remaining costs    
    if (income <= band) :
      cost = cost + (income - prev_band) * tapers[ages,num_kids][i]
      return(cost)
 
    #otherwise use the whole income band to calculate the cost
    cost = cost + (band - prev_band) * tapers[ages,num_kids][i]
    
    i = i+1
    prev_band = band
  
  return(cost)

#get the age mix (3 letter string)  from  two  groups  of ages
def age_mix(kids_12l,kids_13p):
  if (kids_12l>0 and kids_13p == 0) :return("12l")
  elif (kids_12l == 0 and kids_13p > 0) :return("13p")
  elif (kids_12l > 0 and kids_13p > 0) :return("mix")
  else :return("err")
  
#calculate reldep allowance, use ati and number of reldeps.
def coc_simple(income, kids_12l, kids_13p ) :
  if ( kids_12l == 0 and kids_13p == 0) :return(0)
  return(coc(kids_12l+ kids_13p, age_mix(kids_12l, kids_13p), income, 2022, default_income_bands ))
  
#basic values
bv =  {}
bv[2008] = {'mtawe':54756,'far':1122,'pps':13980,'mar':339}
bv[2009] = {'mtawe':56425,'far':1178,'pps':14615,'mar':356}
bv[2010] = {'mtawe':58854,'far':1193,'pps':14937,'mar':360}
bv[2011] = {'mtawe':61781,'far':1226,'pps':15909,'mar':370}
bv[2012] = {'mtawe':64865,'far':1269,'pps':16679,'mar':383}
bv[2013] = {'mtawe':67137,'far':1294,'pps':17256,'mar':391}
bv[2014] = {'mtawe':70569,'far':1322,'pps':18197,'mar':399}
bv[2015] = {'mtawe':70829,'far':1352,'pps':18728,'mar':408}
bv[2016] = {'mtawe':71256,'far':1373,'pps':19011,'mar':414}
bv[2017] = {'mtawe':72462,'far':1390,'pps':19201,'mar':420}
bv[2018] = {'mtawe':73606,'far':1416,'pps':19568,'mar':427}
bv[2019] = {'mtawe':75114,'far':1443,'pps':19981,'mar':435}
bv[2020] = {'mtawe':76726,'far':1467,'pps':20298,'mar':443}
bv[2021] = {'mtawe':78957,'far':1477,'pps':20621,'mar':446}
bv[2022] = {'mtawe':81188,'far':1521,'pps':22888,'mar':459}

for year in bv:
    bv[year]['ssa'] = round(bv[year]['mtawe']/3)

#cs formula 1,3
import math
def cs_baseline(year,ages,nchild
                ,a_name,a_cn,a_othercase_n,a_oth_lsc,a_isp,a_reldep_12l, a_reldep_13p,a_ati, a_othercase_12l, a_othercase_13p
                ,b_name,b_cn,b_othercase_n,b_oth_lsc,b_isp,b_reldep_12l, b_reldep_13p,b_ati, b_othercase_12l, b_othercase_13p):

  output={}
  
  a_ati_lessssa = max(0,a_ati-bv[year]['ssa'])
  b_ati_lessssa = max(0,b_ati-bv[year]['ssa'])  
  output['a_ati_lessssa']=a_ati_lessssa
  output['b_ati_lessssa']=b_ati_lessssa
  
  #calculate ati after reldep allowance  
  a_ati_lessreldep = max(0,a_ati_lessssa - coc_simple(a_ati_lessssa,a_reldep_12l, a_reldep_13p))
  b_ati_lessreldep = max(0,b_ati_lessssa - coc_simple(b_ati_lessssa,b_reldep_12l, b_reldep_13p))
  output['a_ati_lessreldep']=a_ati_lessreldep
  output['b_ati_lessreldep']=b_ati_lessreldep
  
  #total number of CS children in all cases
  a_allcases_nchild = a_othercase_12l  + a_othercase_13p + nchild
  b_allcases_nchild = b_othercase_12l  + b_othercase_13p + nchild
  
  #Evaluate MC coc per child for each age group and parent
  a_mc_cost_pc_12l = coc_simple(a_ati_lessreldep,a_allcases_nchild,0)/a_allcases_nchild
  a_mc_cost_pc_13p = coc_simple(a_ati_lessreldep,0,a_allcases_nchild)/a_allcases_nchild
  b_mc_cost_pc_12l = coc_simple(b_ati_lessreldep,b_allcases_nchild,0)/b_allcases_nchild
  b_mc_cost_pc_13p = coc_simple(b_ati_lessreldep,0,b_allcases_nchild)/b_allcases_nchild
  
  a_mc_cost_12l = a_othercase_12l * a_mc_cost_pc_12l
  a_mc_cost_13p = a_othercase_13p * a_mc_cost_pc_13p
  b_mc_cost_12l = b_othercase_12l * b_mc_cost_pc_12l
  b_mc_cost_13p = b_othercase_13p * b_mc_cost_pc_13p
  
  #total multi case cost
  a_mc_cost = a_mc_cost_12l + a_mc_cost_13p
  b_mc_cost = b_mc_cost_12l + b_mc_cost_13p
  
  #child support income
  a_csi = max(0,a_ati_lessreldep - a_mc_cost)
  b_csi = max(0,b_ati_lessreldep - b_mc_cost)
  output['a_csi']=a_csi
  output['b_csi']=b_csi
  #
  combined_csi = round(a_csi + b_csi , 0)
  output['combined_csi']=combined_csi
  
  #income percent
  if (combined_csi == 0 ) :
    a_income_pct = 0
    b_income_pct = 0
  
  else:
    a_income_pct = round(a_csi/combined_csi,   4)
    b_income_pct = round(b_csi/combined_csi,   4)

  
  #care nights to cost percentage and multi case cap
  a_care_pct = [0]  * nchild
  a_cost_pct = [0]  * nchild
  a_cs_pct = [0]  * nchild
  a_mc_cap = [0]  * nchild
  
  b_care_pct = [0]  * nchild
  b_cost_pct = [0]  * nchild
  b_cs_pct = [0]  * nchild
  b_mc_cap = [0]  * nchild
  
  #Multi case cap
  for i in range(nchild) :
    #TODO vectorise
    a_care_pct[i] = a_cn[i]/365
    
    a_cost_pct[i] = care_to_cost(a_care_pct[i]) 
    a_cs_pct[i]  = max(a_income_pct - a_cost_pct[i],0)
    
    b_care_pct[i] = 1 - a_care_pct[i] 
    b_cost_pct[i] = care_to_cost(b_care_pct[i]) 

    b_cs_pct[i]  = max(b_income_pct - b_cost_pct[i],0)
    
    if (ages[i]  <=  12)  :a_mc_cap[i] = (1 - a_cost_pct[i])*a_mc_cost_pc_12l
    else                  :a_mc_cap[i] = (1 - a_cost_pct[i])*a_mc_cost_pc_13p
    if (ages[i]  <=  12)  :b_mc_cap[i] = (1 - a_cost_pct[i])*b_mc_cost_pc_12l
    else                  :b_mc_cap[i] = (1 - a_cost_pct[i])*b_mc_cost_pc_13p
  
  #elig kids age breakdown
  ekids_12l = 0
  ekids_13p = 0
  
  #TODO replace with sum expression
  for i in range(nchild):
    ekids_12l = ekids_12l + (ages[i] <= 12)
    ekids_13p = ekids_13p + (ages[i] >= 13)
  
  #normal cost of kids method
  basic_coc = coc_simple(combined_csi , ekids_12l , ekids_13p)
  basic_coc_pc = basic_coc/nchild

  #multi case cost of kids
  mc_method_12l_coc  = coc_simple(combined_csi , nchild , 0)
  mc_method_13p_coc  = coc_simple(combined_csi , 0, nchild )
  
  mc_method_12l_coc_pc = mc_method_12l_coc/nchild
  mc_method_13p_coc_pc = mc_method_13p_coc/nchild
  
  mcm_coc=[0]  * nchild
  for i in range(nchild):
    if (ages[i] <= 12) :mcm_coc[i] = mc_method_12l_coc_pc
    if (ages[i] >= 13) :mcm_coc[i] = mc_method_13p_coc_pc
  
  
  #calculate liability
  multi_case_flag = (a_othercase_n + b_othercase_n) > 0
  
  #calculate the liability then see if FAR or MAR apply
  a_init_liab=[0]  * nchild
  a_capd_liab=[0]  * nchild
  a_form_liab=[0]  * nchild
  
  b_init_liab=[0]  * nchild
  b_capd_liab=[0]  * nchild
  b_form_liab=[0]  * nchild
  
  for i in range(nchild)  :  
    if( not multi_case_flag):
      a_init_liab[i] = a_cs_pct[i]*basic_coc_pc
      a_capd_liab[i] = a_init_liab[i]
      b_init_liab[i] = b_cs_pct[i]*basic_coc_pc
      b_capd_liab[i] = b_init_liab[i]
    
    #multi case 
    else:
      a_init_liab[i] = a_cs_pct[i]*mcm_coc[i]
      a_capd_liab[i] = min(a_init_liab[i],a_mc_cap[i])
      b_init_liab[i] = b_cs_pct[i]*mcm_coc[i]
      b_capd_liab[i] = min(b_init_liab[i],b_mc_cap[i])
    
    #cashflow_primcare, no liability if over 65% care
    if (a_care_pct[i]  > 0.65 ) :a_form_liab[i]  = 0
    else :a_form_liab[i]  = a_capd_liab[i]
    if (b_care_pct[i]  > 0.65 ) :b_form_liab[i]  = 0
    else :b_form_liab[i]  = b_capd_liab[i]
  
  
  #calculate FAR amount
  #number of kids in all cases with less than shared care
  a_allchild_lsc = a_oth_lsc
  b_allchild_lsc = b_oth_lsc
  
  for i in range(nchild):
    a_allchild_lsc=  a_allchild_lsc + (a_care_pct[i] <= 0.35)
    b_allchild_lsc=  b_allchild_lsc + (b_care_pct[i] <= 0.35)
  
  
  #FAR per child
  if a_allchild_lsc>0  : a_unit_far = bv[year]['far'] * min(3,a_allchild_lsc)/a_allchild_lsc
  else:  a_unit_far = 0
  if b_allchild_lsc>0  : b_unit_far = bv[year]['far'] * min(3,b_allchild_lsc)/b_allchild_lsc
  else : b_unit_far = 0
  
  # FAR
  a_far_liab=[0]  * nchild
  a_form_far=[0]  * nchild
  b_far_liab=[0]  * nchild
  b_form_far=[0]  * nchild
  
  #TODO FAR Not to apply flag
  for i in range(nchild):
    if (a_isp == 0 and a_ati < bv[year]['pps'] and a_care_pct[i] <= 0.35)    :a_far_liab[i] = a_unit_far
    else: a_far_liab[i] = 0
    if (b_isp == 0 and b_ati < bv[year]['pps'] and b_care_pct[i] <= 0.35)    :b_far_liab[i] = b_unit_far
    else: b_far_liab[i] = 0
    
    a_form_far[i] = max(a_form_liab[i],a_far_liab[i])
    b_form_far[i] = max(b_form_liab[i],b_far_liab[i])    
  
  #Evaluate total outgoing, accounting for all formula and FAR
  a_gross_liability = sum(a_form_far)
  b_gross_liability = sum(b_form_far)
  
  #evaluate total liability, offset each parents amount
  a_total_liability = a_gross_liability - b_gross_liability
  b_total_liability = b_gross_liability - a_gross_liability

  #MAR
  a_totalcases = 1 + a_othercase_n;
  b_totalcases = 1 + b_othercase_n;
  a_mar_liab = bv[year]['mar'] * min(3,a_totalcases)/a_totalcases;
  b_mar_liab = bv[year]['mar'] * min(3,b_totalcases)/b_totalcases;  
  
  #number of children in at least regular care
  a_nchild_al_reg_care = 0 
  b_nchild_al_reg_care = 0 
  
  for i in range(nchild):
    a_nchild_al_reg_care = a_nchild_al_reg_care + (a_care_pct[i] >= 0.14 )
    b_nchild_al_reg_care = b_nchild_al_reg_care + (b_care_pct[i] >= 0.14 )
  
  
  #MAR doesnt apply if any child is at least regular care (i.e MAR applies if all children less than regular care )
  a_mar_eligible = (a_nchild_al_reg_care == 0)
  b_mar_eligible = (b_nchild_al_reg_care == 0)
  
  #calculate liability that applies
  # if A has a liability and is MAR eligible and B isnt then A pays the greater of MAR and liability
  # B liability is negative A liability
  if (a_total_liability >=0 and a_mar_eligible == 1 and b_mar_eligible == 0 ) :
    if  (a_total_liability>a_mar_liab)    :a_selected_liability  = a_total_liability
    else    :a_selected_liability = a_mar_liab
    b_selected_liability   =   -1*a_selected_liability
  
  elif (a_total_liability >=0 and a_mar_eligible == 0 and b_mar_eligible == 0):
    a_selected_liability = a_total_liability
    b_selected_liability   =   -1*a_selected_liability
  
  elif (b_total_liability >=0 and b_mar_eligible == 1 and a_mar_eligible == 0 ) :
    if  (b_total_liability>b_mar_liab)     :b_selected_liability  = b_total_liability
    else    :b_selected_liability = b_mar_liab
    a_selected_liability   =   -1*b_selected_liability
  
  elif (b_total_liability >=0 and b_mar_eligible == 0 and a_mar_eligible == 0):
    b_selected_liability = b_total_liability
    a_selected_liability   =   -1*b_selected_liability
  
  output['a_selected_liability']=a_selected_liability
  #how much A has to pay B, can be negative
  output['liability']=round(a_selected_liability,0)
  
  return(output)
