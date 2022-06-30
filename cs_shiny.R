# Libraries
library(ggplot2)
library(shiny)

#MTAWE 2022
default_income_bands <- list(40594,81188,121782,162376,202970)

#taper parameters,  this is like a  dictionary but can't use a vector as a key
tapers <-new.env()
tapers[["12l1"]] = c(.17,.15,.12,.10,.07,0)
tapers[["12l2"]] = c(.24,.23,.20,.18,.10,0)
tapers[["12l3"]] = c(.27,.26,.25,.24,.18,0)

tapers[["13p1"]] = c(.23,.22,.12,.10,.09,0)
tapers[["13p2"]] = c(.29,.28,.25,.20,.13,0)
tapers[["13p3"]] = c(.32,.31,.30,.29,.20,0)

tapers[["mix1"]] = c(0,0,0,0,0,0)
tapers[["mix2"]] = (tapers[["12l2"]]  + tapers[["13p2"]]) / 2
tapers[["mix3"]] = (tapers[["12l3"]]  + tapers[["13p3"]]) / 2

#convert care  percentage (must be between 0 and  1 ) to cost percentage
care_to_cost <-function(care_pct){
  #Implement legislated rounding rules. Care Percent less than 0.5, round down. 
  #Care Percent more than 0.5, round up.;
  
  if (care_pct < 0.5) { 	care_pct <- floor(100*care_pct)/100} 
  else					{care_pct <- ceiling ( 100*care_pct)/100}
  
  #
  if (care_pct <  0.14) { cost_pct <- 0}
  else if (care_pct <  0.35) { cost_pct <- 0.24 }
  else if (care_pct <  0.48) { cost_pct <- 0.25 + 2*(care_pct-0.35) }
  else if (care_pct <= 0.52) { cost_pct <- 0.50 }
  else if (care_pct <= 0.65) { cost_pct <- 0.51 + 2*(care_pct-0.53) }
  else if (care_pct <= 0.86) { cost_pct <- 0.76 }
  else if (care_pct <= 1.00) { cost_pct <- 1 }
  return(cost_pct)
}


#get the cost of children based on income  ages of kids and number of kids. takes a list if income bands to iterate through
coc <- function(num_kids, ages, income, year, income_bands ) {
  
  #cap num kids at 3
  num_kids  <- min(num_kids,3)  
  hash_key <- paste( ages , num_kids ,sep="")  
  cost<-0
  prev_band <- 0 
  i<-1
  #find index of  income
  
  for (band in income_bands){
    
    #if we reach the relevant band calculate the remaining costs
    
    if (income <= band) {
      cost <- cost + (income - prev_band) * tapers[[hash_key]][i]
      
      return(cost)
    }
    #otherwise use the whole income band to calculate the cost
    cost <- cost + (band - prev_band) * tapers[[hash_key]][i]
    i<-i+1
    prev_band <- band
    
  }
  
  return(cost)
}

#get the age mix (3 letter string)  from  two  groups  of ages
age_mix  <-function(kids_12l,kids_13p){
  if (kids_12l>0 && kids_13p == 0) {return("12l")}
  else if (kids_12l == 0 && kids_13p > 0) {return("13p")}
  else if (kids_12l > 0 && kids_13p > 0) {return("mix")}
  else {return("err")}
  
}

#calculate reldep allowance, use ati and number of reldeps.
coc_simple <- function(income, kids_12l, kids_13p ) {
  if ( kids_12l == 0 && kids_13p == 0) {return(0)}
  return(coc(kids_12l+ kids_13p, age_mix(kids_12l, kids_13p), income, 2022, default_income_bands ))
  
}

#TODO, put this in a look up table
#basic values
ssa = 27063
pps = 22888
far = 1521
mar = 459

#cs formula 1,3
cs_baseline<-function(year,ages,nchild
                      ,a_name,a_cn,a_othercase_n,a_oth_lsc,a_isp,a_reldep_12l, a_reldep_13p,a_ati, a_othercase_12l, a_othercase_13p
                      ,b_name,b_cn,b_othercase_n,b_oth_lsc,b_isp,b_reldep_12l, b_reldep_13p,b_ati, b_othercase_12l, b_othercase_13p)
{
  #TODO dynamic SSA
  a_ati_lessssa <- max(0,a_ati-ssa)
  b_ati_lessssa <- max(0,b_ati-ssa)  
  
  #calculate ati after reldep allowance  
  a_ati_lessreldep <- max(0,a_ati_lessssa - coc_simple(a_ati_lessssa,a_reldep_12l, a_reldep_13p))
  b_ati_lessreldep <- max(0,b_ati_lessssa - coc_simple(b_ati_lessssa,b_reldep_12l, b_reldep_13p))
  
  #total number of CS children in all cases
  a_allcases_nchild <- a_othercase_12l  + a_othercase_13p + nchild
  b_allcases_nchild <- b_othercase_12l  + b_othercase_13p + nchild
  
  #Evaluate MC coc per child for each age group and parent
  a_mc_cost_pc_12l <- coc_simple(a_ati_lessreldep,a_allcases_nchild,0)/a_allcases_nchild
  a_mc_cost_pc_13p <- coc_simple(a_ati_lessreldep,0,a_allcases_nchild)/a_allcases_nchild
  b_mc_cost_pc_12l <- coc_simple(b_ati_lessreldep,b_allcases_nchild,0)/b_allcases_nchild
  b_mc_cost_pc_13p <- coc_simple(b_ati_lessreldep,0,b_allcases_nchild)/b_allcases_nchild
  
  a_mc_cost_12l <- a_othercase_12l * a_mc_cost_pc_12l
  a_mc_cost_13p <- a_othercase_13p * a_mc_cost_pc_13p
  b_mc_cost_12l <- b_othercase_12l * b_mc_cost_pc_12l
  b_mc_cost_13p <- b_othercase_13p * b_mc_cost_pc_13p
  
  #total multi case cost
  a_mc_cost <- a_mc_cost_12l + a_mc_cost_13p
  b_mc_cost <- b_mc_cost_12l + b_mc_cost_13p
  
  #child support income
  a_csi <- max(0,a_ati_lessreldep - a_mc_cost)
  b_csi <- max(0,b_ati_lessreldep - b_mc_cost)
  
  #
  combined_csi <- round(a_csi + b_csi , digits=0)
  
  #income percent
  if (combined_csi == 0 ) {
    a_income_pct <- 0
    b_income_pct <- 0
  }
  else{
    a_income_pct <- round(a_csi/combined_csi, digits =  4)
    b_income_pct <- round(b_csi/combined_csi, digits =  4)
  }
  
  #care nights to cost percentage and multi case cap
  a_care_pct=c()
  a_cost_pct=c()
  a_cs_pct=c()
  a_mc_cap=c()
  
  b_care_pct=c()
  b_cost_pct=c()
  b_cs_pct=c()
  b_mc_cap=c()
  
  #Multi case cap
  for (i in 1:nchild) {
    
    a_care_pct[i] <- a_cn[i]/365
    
    a_cost_pct[i] <- care_to_cost(a_care_pct[i]) 
    a_cs_pct[i]  <- max(a_income_pct - a_cost_pct,0)
    
    b_care_pct[i] <- 1 - a_care_pct[i] 
    b_cost_pct[i] <- care_to_cost(b_care_pct[i]) 
    b_cs_pct[i]  <- max(b_income_pct - b_cost_pct,0)
    
    if (ages[i]  <=  12)  {a_mc_cap[i] <- (1 - a_cost_pct[i])*a_mc_cost_pc_12l}
    else                  {a_mc_cap[i] <- (1 - a_cost_pct[i])*a_mc_cost_pc_13p}
    if (ages[i]  <=  12)  {b_mc_cap[i] <- (1 - a_cost_pct[i])*b_mc_cost_pc_12l}
    else                  {b_mc_cap[i] <- (1 - a_cost_pct[i])*b_mc_cost_pc_13p}
  }
  
  
  #elig kids age breakdown
  ekids_12l <- 0
  ekids_13p <- 0
  
  for (i in 1:nchild)
  {
    if (ages[i] <= 12) {ekids_12l <- ekids_12l + 1}
    if (ages[i] >= 13) {ekids_13p <- ekids_13p + 1}
  }
  
  
  #normal cost of kids method
  basic_coc <- coc_simple(combined_csi , ekids_12l , ekids_13p)
  basic_coc_pc <- basic_coc/nchild
  
  #multi case cost of kids
  mc_method_12l_coc  = coc_simple(combined_csi , nchild , 0)
  mc_method_13p_coc  = coc_simple(combined_csi , 0, nchild )
  
  mc_method_12l_coc_pc = mc_method_12l_coc/nchild
  mc_method_13p_coc_pc = mc_method_13p_coc/nchild
  
  mcm_coc=c()
  for (i in 1:nchild)
  {
    if (ages[i] <= 12) {mcm_coc[i] = mc_method_12l_coc_pc}
    if (ages[i] >= 13) {mcm_coc[i] = mc_method_13p_coc_pc}
  }
  
  #calculate liability
  multi_case_flag <- as.integer((a_othercase_n + b_othercase_n) > 0)
  
  #calculate the liability and see if FAR or MAR apply
  a_init_liab=c()
  a_capd_liab=c()
  a_form_liab=c()
  
  b_init_liab=c()
  b_capd_liab=c()
  b_form_liab=c()
  
  for (i in 1:nchild)
  {  
    if(!multi_case_flag){
      a_init_liab[i] <- a_cs_pct[i]*basic_coc_pc
      a_capd_liab[i] <- a_init_liab[i]
      b_init_liab[i] <- b_cs_pct[i]*basic_coc_pc
      b_capd_liab[i] <- b_init_liab[i]
    }
    #multi case 
    else{
      a_init_liab[i] <- a_cs_pct[i]*mcm_coc[i]
      a_capd_liab[i] <- min(a_init_liab[i],a_mc_cap[i])
      b_init_liab[i] <- b_cs_pct[i]*mcm_coc[i]
      b_capd_liab[i] <- min(b_init_liab[i],b_mc_cap[i])
    }
    
    #cashflow_primcare, no liability if over 65% care
    if (a_care_pct[i]  > 0.65 ) {a_form_liab[i]  = 0}
    else {a_form_liab[i]  <- a_capd_liab[i]}
    if (b_care_pct[i]  > 0.65 ) {b_form_liab[i]  = 0}
    else {b_form_liab[i]  <- b_capd_liab[i]}
    
  }
  
  #calculate FAR amount
  #number of kids in all cases with less than shared care
  a_allchild_lsc <- a_oth_lsc
  b_allchild_lsc <- b_oth_lsc
  
  for (i in 1:nchild){
    a_allchild_lsc<-  a_allchild_lsc + as.integer(a_care_pct[i] <= 0.35)
    b_allchild_lsc<-  b_allchild_lsc + as.integer(b_care_pct[i] <= 0.35)
  }
  
  #FAR per child
  a_unit_far = far * min(3,a_allchild_lsc)/a_allchild_lsc
  b_unit_far = far * min(3,b_allchild_lsc)/b_allchild_lsc
  
  # FAR
  a_far_liab=c()
  a_form_far=c()
  b_far_liab=c()
  b_form_far=c()
  
  #TODO FAR Not to apply flag
  for (i in 1:nchild){
    if (a_isp == 0 && a_ati < pps && a_care_pct[i] <= 0.35)
    {a_far_liab[i] <- a_unit_far}
    else {a_far_liab[i] <- 0}
    if (b_isp == 0 && b_ati < pps && b_care_pct[i] <= 0.35)
    {b_far_liab[i] <- b_unit_far}
    else {b_far_liab[i] <- 0}
    
    a_form_far[i] <- max(a_form_liab[i],a_far_liab[i])
    b_form_far[i] <- max(b_form_liab[i],b_far_liab[i])
    
  }
  
  #Evaluate total outgoing cashflow accounting for all formula rules (except for MAR)
  a_gross_liability <- sum(a_form_far)
  b_gross_liability <- sum(b_form_far)
  
  #evaluate total liability, offset each parents amount
  a_total_liability <- a_gross_liability - b_gross_liability
  b_total_liability <- b_gross_liability - a_gross_liability
  
  #MAR
  a_totalcases <- 1 + a_othercase_n;
  b_totalcases <- 1 + b_othercase_n;
  a_mar_liab <- mar * min(3,a_totalcases)/a_totalcases;
  b_mar_liab <- mar * min(3,b_totalcases)/b_totalcases;  
  
  #number of children in at least regular care
  a_nchild_al_reg_care <- 0 
  b_nchild_al_reg_care <- 0 
  
  for (i in 1:nchild){
    a_nchild_al_reg_care <- a_nchild_al_reg_care + as.integer(a_care_pct[i] >= 0.14 )
    b_nchild_al_reg_care <- b_nchild_al_reg_care + as.integer(b_care_pct[i] >= 0.14 )
  }
  
  #MAR doesnt apply if any child is at least regular care (i.e MAR applies if all children less than regular care )
  a_mar_eligible <- as.integer(a_nchild_al_reg_care == 0)
  b_mar_eligible <- as.integer(b_nchild_al_reg_care == 0)
  
  #calculate liability that applies
  # if A has a liability and is MAR eligible and B isnt then A pays the greater of MAR and liability
  # B lilability is negative A liability
  if (a_total_liability >=0 && a_mar_eligible == 1 && b_mar_eligible == 0 ) {
    if  (a_total_liability>mar)
    {a_selected_liability  <- a_total_liability}
    else
    {a_selected_liability <- a_mar_liab}
    b_selected_liability   <-   -1*a_selected_liability
  }
  else if (a_total_liability >=0 && a_mar_eligible == 0 && b_mar_eligible == 0){
    a_selected_liability <- a_total_liability
    b_selected_liability   <-   -1*a_selected_liability
  }
  else if (b_total_liability >=0 && b_mar_eligible == 1 && a_mar_eligible == 0 ) {
    if  (b_total_liability>mar) 
    {b_selected_liability  <- b_total_liability}
    else
    {b_selected_liability <- b_mar_liab}
    a_selected_liability   <-   -1*b_selected_liability
  }
  else if (b_total_liability >=0 && b_mar_eligible == 0 && a_mar_eligible == 0){
    b_selected_liability <- b_total_liability
    a_selected_liability   <-   -1*b_selected_liability
  }
  #how much A has to pay B, can be negative
  return(a_selected_liability)
}



ui  <-  fluidPage(
  fluidRow(column(2,textOutput(outputId ="liability")),
           column(10,plotOutput(outputId ="ati_liab" ))),
  fluidRow(column(2,textOutput(outputId ="space")),
           column(10,plotOutput(outputId ="care_liab" ))),
  fluidRow(column(4, sliderInput(inputId="num_kid_i",label = "Kids", min  =1  ,max = 5 ,value=1),
                  sliderInput(inputId="a_kid_1_cn_i",label = "Parent A Kid 1 Care nights", min = 0 ,max = 365,value=0),
                  sliderInput(inputId="a_kid_2_cn_i",label = "Parent A Kid 2 Care nights", min = 0 ,max = 365,value=0),
                  sliderInput(inputId="a_kid_3_cn_i",label = "Parent A Kid 3 Care nights", min = 0 ,max = 365,value=0),
                  sliderInput(inputId="a_kid_4_cn_i",label = "Parent A Kid 4 Care nights", min = 0 ,max = 365,value=0),
                  sliderInput(inputId="a_kid_5_cn_i",label = "Parent A Kid 5 Care nights", min = 0 ,max = 365,value=0),
                  
                  sliderInput(inputId="kid_1_i",label = "Kid 1 age", min = 0 ,max = 17 , value=0),
                  sliderInput(inputId="kid_2_i",label = "Kid 2 age", min = 0 ,max = 17 , value=0),
                  sliderInput(inputId="kid_3_i",label = "Kid 3 age", min = 0 ,max = 17 , value=0),
                  sliderInput(inputId="kid_4_i",label = "Kid 4 age", min = 0 ,max = 17 , value=0),
                  sliderInput(inputId="kid_5_i",label = "Kid 5 age", min = 0 ,max = 17 , value=0)
                  
                  )
          ,column(4,  sliderInput(inputId="a_ati_i",label = "Parent A Income", value = 50000 ,  min  = 0  ,max = 300000  ),
                      sliderInput(inputId="a_othercase_n",label = "Parent A Number of other cases", value = 0 ,min  =0  ,max = 10),
                      sliderInput(inputId="a_othercase_okids_lsc_i",label = "Parent A Number of  kids  in other cases with less than shared care", value = 0 ,min  =0  ,max = 10),
                      sliderInput(inputId="a_othercase_12l_i",label = "Parent A Number of kids 12 and under in other cases", value = 0 ,min  =0  ,max = 10),
                      sliderInput(inputId="a_othercase_13p_i",label = "Parent A Number of kids 13 and over in other cases", value = 0 ,min  =0  ,max = 10),
                      sliderInput(inputId="a_reldep_12l_i",label = "Parent A Number of rel deps 12 and under ", value = 0 ,min  =0  ,max = 10),
                      sliderInput(inputId="a_reldep_13p_i",label = "Parent A Number of rel deps 13 and over ", value = 0 ,min  =0  ,max = 10),
                      selectInput(inputId="a_isp", label = "Parent A ISP in LRYI",selected = 0,
                        choices = list("Yes" = 1, "No" = 0)),
                      selectInput(inputId="a_farnta", label = "Parent A FAR not to apply",selected = 0,
                        choices = list("Yes" = 1, "No" = 0))
          )
          ,column(4,  sliderInput(inputId="b_ati_i",label = "Parent B Income", value = 50000 ,  min  = 0  ,max = 300000  ),
                  sliderInput(inputId="b_othercase_n",label = "Parent B Number of other cases", value = 0 ,min  =0  ,max = 10),
                  sliderInput(inputId="b_othercase_okids_lsc_i",label = "Parent B Number of  kids  in other cases with less than shared care", value = 0 ,min  =0  ,max = 10),
                  sliderInput(inputId="b_othercase_12l_i",label = "Parent B Number of kids 12 and under in other cases", value = 0 ,min  =0  ,max = 10),
                  sliderInput(inputId="b_othercase_13p_i",label = "Parent B Number of kids 13 and over in other cases", value = 0 ,min  =0  ,max = 10),
                  sliderInput(inputId="b_reldep_12l_i",label = "Parent B Number of rel deps 12 and under ", value = 0 ,min  =0  ,max = 10),
                  sliderInput(inputId="b_reldep_13p_i",label = "Parent B Number of rel deps 13 and over ", value = 0 ,min  =0  ,max = 10),
                  selectInput(inputId="b_isp", label = "Parent B ISP in LRYI",selected = 0,
                              choices = list("Yes" = 1, "No" = 0)),
                  selectInput(inputId="b_farnta", label = "Parent B FAR not to apply",selected = 0,
                              choices = list("Yes" = 1, "No" = 0))
          )
  )
)

server <-function(input,  output){
  output$liability<-renderText({paste("Parent A gives Parent  B: $",cs_baseline(2022,c(input$kid_1_i,input$kid_2_i,input$kid_3_i,input$kid_4_i,input$kid_5_i),input$num_kid_i
 ,"Par A",c(input$a_kid_1_cn_i,input$a_kid_2_cn_i,input$a_kid_3_cn_i,input$a_kid_4_cn_i,input$a_kid_5_cn_i),input$a_othercase_n,input$a_othercase_okids_lsc_i
    ,input$a_isp,input$a_reldep_12l_i,input$a_reldep_13p_i,input$a_ati_i,input$a_othercase_12l_i,input$a_othercase_13p_i
 ,"Par B",c(0,0,0,0,0),input$b_othercase_n,input$b_othercase_okids_lsc_i
 ,input$b_isp,input$b_reldep_12l_i,input$b_reldep_13p_i,input$b_ati_i,input$b_othercase_12l_i,input$b_othercase_13p_i
  )," per year")
    }
 )
  # create a plot of income vs liability 
  #create marginal income data
  marginal_data<-reactive({
    a_ati_v <- c(seq(0,250000,by=1000))  
    a_liability <- c()
    #marginal change  in  liability
    a_margin <-c()
    a_average <- c()
    for (i in 1:length(a_ati_v)){
      a_liability[i] <- cs_baseline(2022,c(input$kid_1_i,input$kid_2_i,input$kid_3_i,input$kid_4_i,input$kid_5_i),input$num_kid_i
      ,"Par A",c(input$a_kid_1_cn_i,input$a_kid_2_cn_i,input$a_kid_3_cn_i,input$a_kid_4_cn_i,input$a_kid_5_cn_i),input$a_othercase_n,input$a_othercase_okids_lsc_i
      ,input$a_isp,input$a_reldep_12l_i,input$a_reldep_13p_i,a_ati_v[i],input$a_othercase_12l_i,input$a_othercase_13p_i
      ,"Par B",c(0,0,0,0,0),input$b_othercase_n,input$b_othercase_okids_lsc_i
      ,input$b_isp,input$b_reldep_12l_i,input$b_reldep_13p_i,input$b_ati_i,input$b_othercase_12l_i,input$b_othercase_13p_i )  
      if (i == 1){
        a_margin[i] <- 0
        a_average[i] <- 0
        }
      else{
        #make same scale as liability
        a_margin[i] <-  100000*(max(min((a_liability[i] -a_liability[i-1])/(a_ati_v[i] - a_ati_v[i-1]),0.5),-0.25))
        a_average[i] <-  100000*(max(min(a_liability[i]/a_ati_v[i] ,0.25),-0.5))
      }
    }
    data.frame(a_ati_v,a_liability,a_margin,a_average)
  })
  
  # Plot marginal income
  output$ati_liab<-renderPlot(ggplot(marginal_data(), aes(x=a_ati_v, y=a_liability)) 
                              + geom_line(mapping = aes(x = a_ati_v, y = a_liability), color = "black")
                              + geom_line(mapping = aes(x = a_ati_v, y = a_margin), color = "red")
                             # + geom_line(mapping = aes(x = a_ati_v, y = a_average), color = "blue") 
                              +scale_y_continuous(name = "Liability", sec.axis = sec_axis(~./100000, name = "% Change in liability")))

  care_data<-reactive({
    a_care_v <- c(seq(0,365,by=1))  
    a_liability <- c()
    #marginal change  in  liability
    a_margin <-c()
    a_average <- c()
    for (i in 1:length(a_care_v)){
      a_liability[i] <- cs_baseline(2022,c(input$kid_1_i,input$kid_2_i,input$kid_3_i,input$kid_4_i,input$kid_5_i),input$num_kid_i
                                    ,"Par A",c(a_care_v[i],a_care_v[i],a_care_v[i],a_care_v[i],a_care_v[i]),input$a_othercase_n,input$a_othercase_okids_lsc_i
                                    ,input$a_isp,input$a_reldep_12l_i,input$a_reldep_13p_i,input$a_ati_i,input$a_othercase_12l_i,input$a_othercase_13p_i
                                    ,"Par B",c(0,0,0,0,0),input$b_othercase_n,input$b_othercase_okids_lsc_i
                                    ,input$b_isp,input$b_reldep_12l_i,input$b_reldep_13p_i,input$b_ati_i,input$b_othercase_12l_i,input$b_othercase_13p_i )  
      if (i == 1){
        a_margin[i] <- 0
        a_average[i] <- 0
      }
      else{
        #make same scale as liability
        a_margin[i]  <- 10*(max(min((a_liability[i] -a_liability[i-1])/(a_care_v[i] - a_care_v[i-1]),5000),-5000))
        a_average[i] <- 10*(max(min(a_liability[i]/a_care_v[i] ,5000),-5000))
      }
    }
    data.frame(a_care_v,a_liability,a_margin,a_average)
  })
  
  # Plot marginal care
  output$care_liab<-renderPlot(ggplot(care_data(), aes(x=a_care_v, y=a_liability)) 
                              + geom_line(mapping = aes(x = a_care_v, y = a_liability), color = "black")
                              + geom_line(mapping = aes(x = a_care_v, y = a_margin), color = "red")
                              # + geom_line(mapping = aes(x = a_care_v, y = a_average), color = "blue") 
                              +scale_y_continuous(name = "Liability", sec.axis = sec_axis(~./10, name = "% Change in liability")))
  
}

shinyApp(ui=ui,server=server)

