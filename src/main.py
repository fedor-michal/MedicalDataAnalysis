import os.path
import numpy
import pandas as pd

from data_wrangling import wrangle_module
from data_analysing import analyse_module
from data_plotting import plot_module

if __name__ == '__main__':

    # ------------------------------  ////  Investigating a Dataset ////  ------------------------------#
    # ------------------------------  ////  "No-show appointments"  ////  ------------------------------#




    # ------------------------------  //// Introduction ////  ------------------------------#
    #
    # Dataset collects information from over a 100 thousand medical appointments in Brazil and is focused
    # on whether patients show up for their appointment. A number of characteristics about the particular
    # patient are included in each row.
    #
    # This project performs basic analysis to answer the question of what factors are important for us to
    # predict if patient will show up to the scheduled appointment.
    #
    # Project included modules data_wrangling, data_analysing and data_plotting for dividing the structure
    # into easy-to-read layout.



    # ------------------------------  //// Questions ////  ------------------------------#
    #
    # In order to answer the main question "what factors are important for us to predict if patient will show up
    #  to the scheduled appointment" we will first investigate the following sub questions:
    # 1. Which single variables effect patient's show up to a visit the most (base question)?
    # 2. How receiving the SMS and not receiving the SMS before the visit affects the no-show when scheduling day
    #    is different then appointment day?
    # 3. How the time interval between the visit and scheduling day affect not showing up?




    # ------------------------------  //// Data Wrangling ////  ------------------------------#
    #
    # loading dataset
    dataset_filepath = os.path.join('../data', 'noshowappointments-kagglev2-may-2016.csv')
    raw_df = pd.read_csv(dataset_filepath, sep=',', header=0)
    #
    # creating copy for data wrangling
    input_df = raw_df.copy(deep=True)
    #
    # First look and data wrangling actions:
    # - first look
    # - checking data types
    # - dropping duplicated rows
    # - dropping rows with N/A values (we want to work with complete data,
    #   predicting boolean values is not recommended)
    # - checking unique values of appropriate columns
    wrangle_module.run_wrangling_analyse(input_df)
    #
    # outcomes:
    # - raw dataset dimensions: 14 columns x 110527 data rows (header excluded)
    # - dataset dimensions after de-dup and N/A cleanup: 14 columns x 110527 data rows (header excluded)
    # - duplicated rows count: 0
    # - rows with N/A count: 0
    # - cleaning data from corrupted values:
    input_df = input_df[(input_df["Age"] >= 0)]
    # - changing handcap level values to boolean parameter (to treat all levels of handcap as a handcap in general):
    input_df['Handcap'] = input_df['Handcap'].apply(lambda x: x if x in [0, 1] else 1)
    # - setting up AppointmentID as index:
    input_df.set_index('AppointmentID', inplace=True)
    # - changing dates datatype to datetime YYYY-MM-DD
    input_df['ScheduledDay'] = pd.to_datetime(input_df['ScheduledDay'], format='%Y-%m-%dT%H:%M:%SZ')
    input_df['AppointmentDay'] = pd.to_datetime(input_df['AppointmentDay'], format='%Y-%m-%dT%H:%M:%SZ')
    # - adding column Awaiting_Time (number of days from 0 to x, how long patient waits for the visit)
    input_df['Awaiting_Time'] = (input_df['AppointmentDay'] - input_df['ScheduledDay']).dt.days
    input_df['Awaiting_Time'] = numpy.where(input_df['Awaiting_Time'] >= 0, input_df['Awaiting_Time'], 0)
    #input_df['Awaiting_Time'] = input_df['Awaiting_Time'].apply(lambda x: x if x >= 0 else 0)
    # - adding column Weekday_Of_Appointment
    input_df['Weekday_Of_Appointment'] = input_df['AppointmentDay'].dt.day_name()
    # - final dataset dimensions and columns after data wrangling: (110526, 15)
    print(input_df.head())
    print(input_df.info())
    print(input_df.shape)



    # ------------------------------  //// Exploratory Data Analysis ////  ------------------------------#
    #
    print(input_df.describe())
    # basic histogram
    plot_module.show_histogram(
        input_df,
        ["Gender", "Age", "Scholarship", "Hipertension", "Diabetes", "Alcoholism", "Handcap",
         "SMS_received", "Awaiting_Time", "No-show"]
    )
    # basic histogram for no-show records only
    no_show_df = input_df[input_df['No-show'] == 'Yes']
    plot_module.show_histogram(
        no_show_df,
        ["Gender", "Age", "Scholarship", "Hipertension", "Diabetes", "Alcoholism", "Handcap",
         "SMS_received", "Awaiting_Time"]
    )
    # 1. Which single variables effect patient's show up to a visit the most?
    # (pie chart) no-show % of all visits
    perc_all_show = (len(input_df[(input_df["No-show"] == "No")]) / len(input_df)) * 100
    perc_all_no_show = 100 - perc_all_show
    # co chce podać: % show, % no show (values: list, labels: list, colors: list, title: str):
    plot_module.make_pie_chart_percent([perc_all_show, perc_all_no_show], ["False", "True"],
                                           ["lightgreen", "orange"], "Patient no-show at visit")
    # preparing data in percentage how certain factor affects on not showing up:
    perc_male_no_show = analyse_module.get_no_show_percentage("Gender", "M", input_df)
    perc_female_no_show = analyse_module.get_no_show_percentage("Gender", "F", input_df)
    perc_scholarship_no_show = analyse_module.get_no_show_percentage("Scholarship", 1, input_df)
    perc_hipertension_no_show = analyse_module.get_no_show_percentage("Hipertension", 1, input_df)
    perc_diabetes_no_show = analyse_module.get_no_show_percentage("Diabetes", 1, input_df)
    perc_alcoholism_no_show = analyse_module.get_no_show_percentage("Alcoholism", 1, input_df)
    perc_handcap_no_show = analyse_module.get_no_show_percentage("Handcap", 1, input_df)
    perc_SMS_received_no_show = analyse_module.get_no_show_percentage("SMS_received", 1, input_df)
    perc_SMS_not_received_no_show = analyse_module.get_no_show_percentage("SMS_received", 0, input_df)
    perc_visit_same_day_no_show = analyse_module.get_no_show_percentage("Awaiting_Time", 0, input_df)
    # calculation for perc_visit_not_same_day_no_show :
    count_visit_not_same_day_no_show = len(input_df[(input_df["Awaiting_Time"] > 0) & (input_df["No-show"] == "Yes")])
    perc_visit_not_same_day_no_show = (count_visit_not_same_day_no_show / len(input_df[(input_df["Awaiting_Time"] > 0)])) * 100
    # plotting:
    labels = ["Gender: M", "Gender: F", "Scholarship", "Hipertension", "Diabetes", "Alcoholism", "Handcap",
              "SMS received", "SMS not received", "Visit same day", "Visit not same day"]
    values = [perc_male_no_show,
              perc_female_no_show,
              perc_scholarship_no_show,
              perc_hipertension_no_show,
              perc_diabetes_no_show,
              perc_alcoholism_no_show,
              perc_handcap_no_show,
              perc_SMS_received_no_show,
              perc_SMS_not_received_no_show,
              perc_visit_same_day_no_show,
              perc_visit_not_same_day_no_show
              ]
    plot_module.make_bar_plot_percent(values, labels, ["orange"], "Factor vs no-show percentage")
    # taking scholarship, receiving SMS and having to wait for the visit for some days are the factors which seems to
    # affect not showing to the visit the most. Let's take a deeper look into receiving SMS.
    count_SMS_visit_same_day = len(input_df[(input_df["SMS_received"] == 1) & (input_df["Awaiting_Time"] == 0)])
    print("Count of SMS received if Awaiting_Time = 0: " + str(count_SMS_visit_same_day))
    #
    # visualising how receiving the SMS and not receiving the SMS affects the no-show when scheduling day is
    # different then appointment day:
    count_visit_not_same_day_and_SMS_received_no_show = len(input_df[(input_df["Awaiting_Time"] > 0)
                                                                      & (input_df["SMS_received"] == 1)
                                                                      & (input_df["No-show"] == "Yes")])
    count_visit_not_same_day_and_SMS_not_received_no_show = count_visit_not_same_day_no_show - count_visit_not_same_day_and_SMS_received_no_show
    perc_visit_not_same_day_and_SMS_received_no_show = (count_visit_not_same_day_and_SMS_received_no_show
                                                        / count_visit_not_same_day_no_show) * 100
    perc_visit_not_same_day_and_SMS_not_received_no_show = (count_visit_not_same_day_and_SMS_not_received_no_show
                                                            / count_visit_not_same_day_no_show) * 100
    plot_module.make_bar_plot_percent([perc_visit_not_same_day_and_SMS_received_no_show, perc_visit_not_same_day_and_SMS_not_received_no_show],
                                      ["SMS received", "SMS not received"],
                                      ["orange"], "Factor: SMS in appointment day different then scheduling day vs no-show %")
    #
    # 2. How the time interval between the visit and scheduling day affect not showing up?
    # visit the same day , visit the next day, visit 2-4 days after, visit 5-9 days after, visit 10+ days after
    perc_visit_same_day_no_show = perc_visit_same_day_no_show
    #
    count_visit_next_day_no_show = len(input_df[(input_df["Awaiting_Time"] == 1) & (input_df["No-show"] == "Yes")])
    count_visit_next_day_all = len(input_df[(input_df["Awaiting_Time"] == 1)])
    perc_visit_next_day_no_show = (count_visit_next_day_no_show / count_visit_next_day_all) * 100
    #
    count_visit_2_to_4_day_no_show = len(input_df[(input_df["Awaiting_Time"] >= 2) & (input_df["Awaiting_Time"] <= 4) & (input_df["No-show"] == "Yes")])
    count_visit_2_to_4_day_all = len(input_df[(input_df["Awaiting_Time"] >= 2) & (input_df["Awaiting_Time"] <= 4)])
    perc_visit_2_to_4_day_no_show = (count_visit_2_to_4_day_no_show / count_visit_2_to_4_day_all) * 100
    #
    count_visit_5_to_9_day_no_show = len(input_df[(input_df["Awaiting_Time"] >= 5) & (input_df["Awaiting_Time"] <= 9) & (input_df["No-show"] == "Yes")])
    count_visit_5_to_9_day_all = len(input_df[(input_df["Awaiting_Time"] >= 5) & (input_df["Awaiting_Time"] <= 9)])
    perc_visit_5_to_9_day_no_show = (count_visit_5_to_9_day_no_show / count_visit_5_to_9_day_all) * 100
    #
    perc_visit_10_plus_day_no_show = len(input_df[(input_df["Awaiting_Time"] >= 10) & (input_df["No-show"] == "Yes")])
    perc_visit_10_plus_day_all = len(input_df[(input_df["Awaiting_Time"] >= 10)])
    perc_visit_10_plus_day_no_show = (perc_visit_10_plus_day_no_show / perc_visit_10_plus_day_all) * 100
    #
    values = [perc_visit_same_day_no_show,
              perc_visit_next_day_no_show,
              perc_visit_2_to_4_day_no_show,
              perc_visit_5_to_9_day_no_show,
              perc_visit_10_plus_day_no_show]
    labels = ["same day",
              "next day",
              "2-4 days",
              "5-9 days",
              "10+ days"]
    plot_module.make_bar_plot_percent(values, labels, ["orange"], "Factor: duration between scheduling and appointment day vs no-show %")






    # ------------------------------  //// Conclusions ////  ------------------------------#
    # 1.	Based on the analysis, taking scholarship, receiving SMS and having to wait for the visit seems to be
    #       the 3 factors which have greater share in no-show. Receiving SMS as a factor which increases chances of
    #       not showing seems to be strange. After taking a deeper look at this factor, we can spot that when
    #       scheduling day is the same as appointment day, patients are not receiving SMS. It means that we should
    #       take SMS factor under consideration only for the visits which are not in the scheduling day.
    #       Additionally, females are slightly more prone to no show at the visit than men, but the difference is
    #       very small.
    # 2.	Analysis on SMS and awaiting time shows, that the percentage difference between SMS impact on no-showing
    #       to the visit in the day different than visit’s scheduling day is very similar. We can say that not
    #       receiving SMS is not affecting not showing up to a visit.
    # 3.	Based on further analysis, we can spot that increase of awaiting time affects on the no-show percentage
    #       – not showing up percentage is increasing.
    # 4.	Additional research can be done on Neighbourhood factor, and some combined factors, e.g. „How does age
    #       affect on alcoholics showing up to a visit?”, or „How does alcoholism affect people with scholarship showing up to a visit?”.


    # ------------------------------  //// Limitation ////  ------------------------------#
    # 1.	Important limitation in the dataset is information about timing of receiving the SMS and appointment date.
    #       Receiving the SMS 1 or 2 days earlier is different then receiving SMS on the same day.

#
