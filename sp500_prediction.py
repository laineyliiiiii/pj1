from email.policy import default
import streamlit as st
import numpy as np
import pandas as pd
import statsmodels.api as sm

parameters = {'axes.labelsize': 10,
          'axes.titlesize': 10}

def reg_coef():
    url="https://raw.githubusercontent.com/laineyliiiiii/pj1/main/data_q.csv"
    df = pd.read_csv(url, index_col=0)
    ols_var=['fedbs','fedfundsrate','home_median','us10y','gdp_real','debt_gdp','govexp_gdp']
    params_ols=[]
    for i in ols_var:
        params_ols.append(sm.OLS(df['spx_idx'], sm.add_constant(df[i])).fit().params[1])
    return params_ols

    
    

def main():
    global fed_delta, ffr_delta, housing_delta, treasury_delta,gdp_delta, debt_gdp_delta, gov_delta

    # Set parameters

    st.title(" S&P 500 股市预测 ")

    st.caption('本网页基于OLS模型对股市进行预测，请在下方选择各项变量在2022年底时的估计值，并查看对股市可能造成的影响。')

    # variable selection
    delta=[]
    # -----------------------------------------------------------
    st.subheader('1. 美联储资产负债表规模变化')
    st.write('\n')
    if st.checkbox("默认：-4725亿美元", key=1):
        fed_delta = -472500
    else:
        fed_delta_input = st.number_input('请输入变化规模(单位：亿元）：', step=1)
        if fed_delta_input > 0:
            st.write('2022年底相较于年初，美联储资产负债表规模上升 %1.0f 亿元，达到 %1.3f 万亿元' % ( fed_delta_input,  fed_delta_input/10000+8.765))
        elif fed_delta_input==0:
            st.write("2022年底相较于年初，美联储资产负债表规模保持不变")
        elif fed_delta_input < 0:
            st.write('2022年底相较于年初，美联储资产负债表规模下降 %1.0f 亿元，达到 %1.3f 万亿元' % (-1* fed_delta_input,  fed_delta_input/10000+8.765))
        fed_delta= fed_delta_input*100
    
    delta.append(fed_delta)
    # -----------------------------------------------------------
    st.subheader("2. 美国联邦基金利率")
    st.write('\n')
    if st.checkbox("默认：3.3% （即2022年上升3.175%）", key=2):
        ffr_delta = 3.175
    else:
        ffr_delta = st.slider('请选择变化规模(单位：基点）：', -100, 1000, 317, step=25, key='ffr')/100
        st.write("2022年底预测美国联邦基金利率为 %1.3f %% ， 较年初上升 %1.2f %% " %(ffr_delta+0.125,ffr_delta))
    
    delta.append(ffr_delta)

    # -----------------------------------------------------------
    st.subheader("3. 美国房价中位数")
    st.write('\n')
    if st.checkbox("默认：0 （即保持不变）", key=3):
        housing_delta=0
    else:
        housing_delta_input = st.slider('请选择变化规模(单位：%）：', -100, 200, 0, step=5, key=3)
        st.write("2022年底预测美国房价中位数为 %1.3f 万美元 ， 较年初 %1.0f %% " % (36.07*(1+housing_delta_input),housing_delta_input*100))
        housing_delta=360.7*housing_delta_input/100 

    delta.append(housing_delta)

    # -----------------------------------------------------------
    st.subheader("4. 美国10年期国债收益率")
    st.write('\n')
    if st.checkbox('默认: 0'):
        treasury_delta=0
    else:
        treasury_delta = st.slider('请选择变化规模(单位：基点）：', -1000, 1000, 0, step=25)/100
        st.write("2022年底预测美国10年期国债收益率为 %1.3f 万美元 ， 较年初 %1.0f %% " % (1.63+treasury_delta,treasury_delta*100))

    delta.append(treasury_delta)


    # -----------------------------------------------------------
    st.subheader("5. 美国实际GDP")
    st.write('\n')
    if st.checkbox("默认：+1.7% （Bloomberg预测值）", key=4):
        gdp_delta=0
    else:
        gdp_delta_input = st.number_input('请选择变化规模(单位：%）：')
        st.write("2022年底预测美国实际GDP为 %1.3f 万美元 ， 2022年间增长 %1.0f %% " % (19727.918*(1+gdp_delta_input/100),gdp_delta_input))
        gdp_delta=19727.918*gdp_delta_input/100

    delta.append(gdp_delta)
    # -----------------------------------------------------------
    st.subheader("6. 美国短期债务占GDP比重")
    st.write('\n')
    if st.checkbox("默认：0 （即保持不变） ", key=5):
        debt_gdp_delta=0
    else:
        debt_gdp_delta = st.slider('请选择变化规模(单位：%）：', -25, 25,0)
        st.write("2022年底预测短期债务占GDP比重为 %1.3f %% ， 2022年间 %1.0f %% " % (27.25+debt_gdp_delta,debt_gdp_delta))
    
    delta.append(debt_gdp_delta)

    # -----------------------------------------------------------
    st.subheader("7. 政府支出")
    st.write('\n')
    if st.checkbox("默认：0 （即保持不变）", key=6):
        gov_delta=0
    else:
        if st.checkbox("百分比变化：", key=7):
            gov_pct_delta = st.slider('请选择变化规模(单位：%）：', -200, 200,0, key='gov_percent')
            st.write("2022年底预测政府支出为 %1.3f，与年初相比： %1.0f %% " % (3463.8*(1+gov_pct_delta),gov_pct_delta))
            gov_delta=3463.8*gov_pct_delta/100

        else:
            st.checkbox("数值变化:")
            gov_delta=st.number_input('请输入变化规模(单位：亿）：', key='gov_gdp_delta')/10
            st.write("2022年底预测政府支出为 %1.3f 亿元，与年初相比： %1.0f " % (3463.8+gov_delta,gov_delta/3463.8))
    
    delta.append(gov_delta)

    params_ols=reg_coef()
    # delta=[fed_delta, ffr_delta, housing_delta, treasury_delta,gdp_delta, debt_gdp_delta, gov_delta]
    prediction = 3.83* np.dot(params_ols,delta)

    st.write("\n \n \n")

    st.header("预测结果")

    st.latex("预计2022年底标普500指数为:")
    st.latex("\\textbf{%1.2f}" % (4796.56+prediction))
    if prediction > 0 :
        st.latex('较年初上升:')
        st.latex("\\textbf{%1.2f}" % (prediction))
    elif prediction ==0:
        st.latex('较年初保持不变')
    elif prediction <0:
        st.latex('较年初下降:')
        st.latex("\\textbf{%1.2f}" % (-1*prediction))
        

            


    # expected_yrs = st.number_input("1.2 Expected Working Years", min_value=0, max_value=100, value=20, step=1)
    # Annual_Investment_Rate = st.slider("1.3 Please choose your annual investment rate", min_value=0.0000, max_value=1.0000,
    #                                    value=0.0913, step=0.0001)

    # start_salary = st.number_input("1.4 Start Salary", min_value=0, max_value=None, value=85000, step=1000)
    # start_balance = st.number_input("1.5Start Balance", min_value=0, max_value=None, value=50000, step=1000)
    # st.subheader("2. Parameter Settings")
    # expected_portfolio = st.number_input("2.1 Expected ending portfolio is ", min_value=0, max_value=None, value=1000000,
    #                                      step=1000)

    # global portfolio_distribution
    # portfolio_distribution = st.selectbox("2.2Please specify your portfolio distribution type",
    #                                       ["Normal Distribution"])

    # # set iterations
    # n = expected_yrs * st.slider("2.3 Please choose iteration times (Default is 10000)", 0, 100000, 10000, step=10000)
    # li_time = int(n / expected_yrs)
    # st.write('Your iteration time is ', li_time)

    # generate_salary_growth_rate()
    # generate_portfolio_rate()
    # st.subheader("3. Caculation")
    # model()
    # #@Kuangqi Chen



if __name__ == "__main__":
    main()

