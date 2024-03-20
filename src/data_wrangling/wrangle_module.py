import pandas as pd


def run_wrangling_analyse(input_df: pd.DataFrame):
    pd.set_option('display.max_columns', None)
    print("\nDataset exploration:")
    print(input_df.head())
    print("\nRaw dataset dimensions: " + str(input_df.shape) + "\n")

    # - checking date types
    input_df.info()
    print("ScheduledDay type: " + str(type(input_df["ScheduledDay"][0])))
    print("AppointmentDay type: " + str(type(input_df["AppointmentDay"][0])))
    print("Gender type: " + str(type(input_df["Gender"][0])))
    print("Neighbourhood type: " + str(type(input_df["Neighbourhood"][0])))

    print("Does column AppointmentID contain duplicates? : " + str(not input_df['AppointmentID'].is_unique))

    # dropping duplicated rows
    len_pre_drop = len(input_df)
    input_df.drop_duplicates(inplace=True)
    len_post_drop = len(input_df)
    print("Duplicated rows number: " + str(len_pre_drop - len_post_drop))
    print("\nDeduped dataset dimensions: " + str(input_df.shape) + "\n")

    # dropping rows with N/A values (we want to work with complete data, predicting boolean values is not recommended)
    input_df.dropna(inplace=True)
    len_post_dropna = len(input_df)
    print("NA rows number: " + str(len_post_drop - len_post_dropna))

    print("\n Dataset records after clean-up: " + str(len_post_dropna))

    # checking unique values of appropriate columns
    print('Gender:', input_df["Gender"].unique())
    print('Age:', sorted(input_df["Age"].unique()))
    print('Neighbourhood:', input_df["Neighbourhood"].unique())
    print('Scholarship:', input_df["Scholarship"].unique())
    print('Hipertension:', input_df["Hipertension"].unique())
    print('Diabetes:', input_df["Diabetes"].unique())
    print('Alcoholism:', input_df["Alcoholism"].unique())
    print('Handcap:', input_df["Handcap"].unique())
    print('SMS_received:', input_df["SMS_received"].unique())
    print('No-show:', input_df["No-show"].unique())


