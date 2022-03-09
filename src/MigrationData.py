# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 16:17:18 2021

@author: harshith
Minor edits by Mark
"""
import os
import pandas as pd 


class MigrationData:
    def __init__(self,year):
        '''
        Initialize the MigrationData class object for a particular year

        Parameters
        ----------
        year : int
            year for which the data needs to be loaded 
            must be between 2010 and 2019 (inclusive)

        Returns
        -------
        None.
        
        Examples
        --------
        >>> data_2010 = MigrationData(2010)
        creates a MigrationData object for the year 2010 

        '''
        assert(isinstance(year,int))
        try:
            assert year >= 2010 and year <= 2019
        except AssertionError as e:
            print(repr(e))
            print('Incorrect year! Must be from 2009 to 2019 (inclusive).')
        self.year = year
        self.fname = self.__get_fname(year)
        self.dframe = pd.DataFrame()
    
    @staticmethod
    def __get_fname(year):
        '''
        Funtion to read the data/migration_data/. directory and fetch the 
        data file corresponding to that year 

        Parameters
        ----------
        year : int
            year for which data is needed.

        Returns
        -------
        fname: str
            File location wrt cwd.
            Returns empty string if file is not found 
        
        Examples
        --------
        >>> data_2010 = MigrationData(2010)
        >>> fname = data_2010.__get_fname(2010) 
        './data/migration_data/ACSST1Y2010.S0701_data_with_overlays_2021-11-14T150238.csv'
        
        Fetches the file name for that year

        '''
        data_loc = '../data/migration_data/'
        #walk through the files in data_loc 
        file_walk = list(os.walk(data_loc))
        sub_dirs,dirs,files = file_walk[0]
        for file in files:
            if 'Y'+str(year) in file:
                if 'data_with_overlays' in file:
                    return data_loc + file
        return ''

    def load_dframe(self):
        '''
        Function to load the data from file system and update the 
        dataframe class variable

        Returns
        -------
        None.
        
        Examples
        --------
        >>> data_2010 = MigrationData(2010)
        >>> data_2010.load_dframe()
        Data Loading successful for the year 2010 
        
        Loads the data and updates the dataframe variable

        '''
        if (self.fname == ''):
            print("Data Loading failed for the year",self.year)
        else:
            print("Data Loading successful for the year",self.year)
        data = pd.read_csv(self.fname)
        data_header = data.iloc[0]
        data = data[1:]
        data.columns = data_header
        self.dframe = data

    def get_keys(self, key, key_type=''):
        '''
        Function to get the series of column names for specific key and key_type of interest 
    
        Parameters
        ----------
        fname : input file name
            DESCRIPTION.
        key : str
        the key input can be any string from the below list 
            'AGE'
            'SEX'
            'RACE'
            'EDUCATIONAL ATTAINMENT'
            'INDIVIDUAL INCOME'
            'POVERTY STATUS'
            'HOUSING TENURE'
            
        key_type : str, optional
        the key_type input can be any string from the below list 
            '' - all the types 
            'Total'
            'same county'
            'different county'
            'state'
            'abroad'
        the default is ''
    
        Returns
        -------
        key_list : list
            list of column names matching the key and key_type specifications
        
        Examples
        --------
        >>> data_2010 = MigrationData(2010)
        >>> data_2010.load_dframe()
        >>> key_list = data_2010.get_keys('SEX', 'state')
        0                                   Geographic Area Name
        359    Moved; from different  state!!Estimate!!SEX!!Male
        361    Moved; from different  state!!Estimate!!SEX!!F...
        dtype: object
        
        From the data frame columns, the list of column names matching with the 
        key and key_type are returned 
        
        Geographic Area Name is appended at the start for further usage
        of this function
    
        '''
        assert(not self.dframe.empty)
        assert(isinstance(self.fname,str))
        assert(isinstance(key,str))
        assert(isinstance(key_type,str))
        assert(self.fname != '')
        
        #key should be one among the following list
        key_list = ['AGE','SEX','RACE','EDUCATIONAL ATTAINMENT','INDIVIDUAL INCOME','POVERTY STATUS','HOUSING TENURE']
        assert(key in key_list)
        
        #special handling for state to avoid other unnecessary state data
        if(key_type == 'state'):
            key_type = 'different  state'
        #key_type should be one among the following 
        key_type_list = ['','Total','same county','different county','different  state','abroad']
        assert(key_type in key_type_list)
        
        #Read the metadata file associated with the data file to get the actual key values
        metadatafile = self.fname.replace('data_with_overlays','metadata')
        metadata = pd.read_csv(metadatafile)
        if self.year < 2018:
            search_key = "Estimate!!" + key
            if key != 'RACE':
                key_list = metadata[metadata['id'].map(lambda x: (search_key in x) & (key_type in x))]['id']
            else:
                key_list = metadata[metadata['id'].map(lambda x: ((search_key in x) | ('origin' in x) | ('race' in x))&(key_type in x))]['id']
        else: #The years 2018 and above don't use the same formatting, as the 'ESTIMATE!!' tag isn't along with the key
            search_key = key
            if key != 'RACE':
                key_list = metadata[metadata['id'].map(lambda x: (search_key in x)&(key_type in x) & ("Estimate!!" in x))]['id']
            else:
                key_list = metadata[metadata['id'].map(lambda x: ((search_key in x) | ('origin' in x) | ('race' in x) & ("Estimate!!" in x))&(key_type in x))]['id']
        return pd.concat([pd.Series(['Geographic Area Name']),key_list])
    
    @staticmethod
    def get_key(dframe, spec):
        '''
        Function to get the column name containing a specific string 

        Parameters
        ----------
        dframe : pd.core.frame.DataFrame 
            input data frame from which column names are extracted 
        spec : str
            specific search string.

        Returns
        -------
        str
            column name that contains spec.
        
        Examples
        --------
        >>> data_2010 = MigrationData(2010)
        >>> data_2010.load_dframe()
        >>> key_list = data_2010.get_key(data_2010.dframe,'1 to 4 years')
        'Moved; within same county!!Estimate!!AGE!!1 to 4 years'
        
        From the given data frame it fetches the column name of interest
        
        '''
        assert(not dframe.empty)
        assert(isinstance(dframe,pd.core.frame.DataFrame))
        assert(isinstance(spec,str))
        for col_name in dframe.columns:
            if spec in col_name:
                return col_name 
        return ''
        
    @staticmethod
    def conv_dtypes(dframe,dtype):
        '''
        Function to convert all the elements in a dataframe to specific dtype

        Parameters
        ----------
        dframe : pd.core.frame.DataFrame
            input data frame 
        dtype : Object
            dtype to which the data needs to be converted.

        Returns
        -------
        dframe : pd.core.frame.DataFrame
            updated data frame with new dtype.

        Examples
        --------
        >>> data_2010 = MigrationData(2010)
        >>> data_2010.load_dframe()
        >>> new_dframe = data_2010.conv_dtypes(data_2010.dframe,float)
        
        Converts all the elements in the input data frame to float values 
        '''
        assert(not dframe.empty)
        assert(isinstance(dframe,pd.core.frame.DataFrame))
        assert(isinstance(dtype,object))
        dtype_dict = {}
        for key_ele in dframe.columns:
            dtype_dict[key_ele] = dtype
        dframe = dframe.astype(dtype_dict,errors='ignore')
        return dframe
    
    @staticmethod
    def filter_data(dframe):
        '''
        Function to filter out redundant/unneccessary data and converts to float

        Parameters
        ----------
        dframe : pd.core.frame.DataFrame
            input data frame that is to be filtered out 
            
        Returns
        -------
        dframe : pd.core.frame.DataFrame
            filtered output and converted to float
            
        '''
        assert(not dframe.empty)
        assert(isinstance(dframe,pd.core.frame.DataFrame))
        #making the geographic area name as index 
        dframe = dframe.set_index('Geographic Area Name')
        #dropping the Puerto Rico row data 
        dframe = dframe.drop(['Puerto Rico'])
        #updating the NA values 
        dframe = dframe.replace('N',pd.NA).fillna(0.0)
        #conv dtype to float 
        dframe = MigrationData.conv_dtypes(dframe,float)
        return dframe
    
    def get_key_data(self, key, key_type, in_percentage):
        '''
        Function to get the column data from the loaded dataframe with certain specifications

        Parameters
        ----------
        key : str
            category(demography) of data (age,sex,poverty status etc.,)
        key_type : str
            type of data (state,county etc.,)
        in_percentage : bool
            if True the output will be in terms of percentages 
            if False the output will be in terms of actual number of people 

        Returns
        -------
        pd.core.frame.DataFrame 
            dataframe containing data for the specific key and key_type.

        '''
        assert(not self.dframe.empty)
        assert(isinstance(self.dframe,pd.core.frame.DataFrame))
        assert(isinstance(key,str))
        assert(isinstance(key_type,str))
        assert(isinstance(in_percentage,bool))
        keys = self.get_keys(key, key_type)
        data_inperc = self.filter_data(self.dframe[keys])
        if (in_percentage | (key_type == 'Total')):
            return data_inperc
        else:
            total_keys = self.get_keys(key, 'Total')
            data_total = self.filter_data(self.dframe[total_keys])
            data_total.columns = data_inperc.columns 
            for col in data_total.columns:
                #print(col)
                data_total[[col]] = data_total[[col]].mul(data_inperc[[col]])//100
            return data_total
    @staticmethod 
    def query_group_keys(dframe,item_list):
        '''
        Function to return a list of column names with specifications in item_list

        Parameters
        ----------
        dframe : pd.core.frame.DataFrame
            Input pandas dataframe
        item_list : list
            list of elements containing specifications.
            Eg: ['state','any race']

        Returns
        -------
        grp_keys : list
            List of column names in the data frame that are containing strings
            from the item_list

        '''
        assert(not dframe.empty)
        assert(isinstance(dframe,pd.core.frame.DataFrame))
        assert(isinstance(item_list,list))
        grp_keys = []
        for item in item_list:
            grp_keys.append(MigrationData.get_key(dframe, item))
        return grp_keys
    
    @staticmethod
    def sum_grp_data(dframe,grp_key_list):
        '''
        Function to return summation of a list of columns 

        Parameters
        ----------
        dframe : pd.core.frame.DataFrame
            Input Data frame
        grp_key_list : list
            list of column names 

        Returns
        -------
        out_data : pd.core.frame.Series
            series that has the row wise summation of all the elements 
            in the input columns.

        '''
        assert(not dframe.empty)
        assert(isinstance(dframe,pd.core.frame.DataFrame))
        assert(isinstance(grp_key_list,list))
        out_data = pd.Series()
        for ele in grp_key_list:
            out_data += dframe[ele]
        return out_data
        
    def get_age_group_data(self,in_percentage):
        '''
        Function to query the age group data from the loaded data frame
        Different columns are clubbed to form the below groups: 
            1. 1 to 17 years
            2. 18 to 24 years
            3. 25 to 54 years
            4. 55 years and above
        Parameters
        ----------
        in_percentage : bool
            boolean value determines if the output needs to be in percentage form or not

        Returns
        -------
        age_df : pd.core.frame.DataFrame 
            age data grouped into the above categories 

        '''
        assert(isinstance(in_percentage,bool))
        assert(not self.dframe.empty)
        age_data = self.get_key_data('AGE','state', False)
        age_total = self.get_key_data('AGE','Total', False)
        age_df_total = pd.DataFrame(index = age_data.index)
        age_df       = pd.DataFrame(index = age_data.index)
        list_1_to_17 = ['1 to 4 years', '5 to 17 years']
        list_18_to_24 = ['18 to 24 years']
        list_25_to_54 = ['25 to 34 years', '35 to 44 years', '45 to 54 years']
        list_55_and_over = ['55 to 64 years','65 to 74 years','75 years and over']
        
        keys_1_to_17 = self.query_group_keys(age_data, list_1_to_17)
        keys_1_to_17_total = self.query_group_keys(age_total, list_1_to_17)
        age_df['1 to 17 years'] = age_data[keys_1_to_17[0]] + age_data[keys_1_to_17[1]]
        age_df_total['1 to 17 years'] = age_total[keys_1_to_17_total[0]] + age_total[keys_1_to_17_total[1]]
        
        keys_18_to_24 = self.query_group_keys(age_data, list_18_to_24)
        keys_18_to_24_total = self.query_group_keys(age_total, list_18_to_24)
        age_df['18 to 24 years'] = age_data[keys_18_to_24[0]]
        age_df_total['18 to 24 years'] = age_total[keys_18_to_24_total[0]] 
        
        keys_25_to_54 = self.query_group_keys(age_data, list_25_to_54)
        keys_25_to_54_total = self.query_group_keys(age_total, list_25_to_54)
        age_df['25 to 54 years'] = age_data[keys_25_to_54[0]] + age_data[keys_25_to_54[1]] + age_data[keys_25_to_54[2]]
        age_df_total['25 to 54 years'] = age_total[keys_25_to_54_total[0]] + age_total[keys_25_to_54_total[1]]+ age_total[keys_25_to_54_total[2]]
        
        keys_55_and_over = self.query_group_keys(age_data, list_55_and_over)
        keys_55_and_over_total = self.query_group_keys(age_total, list_55_and_over)
        age_df['55 years and over'] = age_data[keys_55_and_over[0]] + age_data[keys_55_and_over[1]]+ age_data[keys_55_and_over[2]]
        age_df_total['55 years and over'] = age_total[keys_55_and_over_total[0]] + age_total[keys_55_and_over_total[1]]+ age_total[keys_55_and_over_total[2]]
        
        if in_percentage:
            for col in age_df.columns:
                age_df[[col]] = age_df[[col]].div(age_df_total[[col]]) * 100
            return age_df 
        else:
            return age_df

    def get_age_country_data(self,in_percentage):
        '''
        Function to query the age group data from the loaded data frame
        Different columns are clubbed to form the below groups: 
            1. 1 to 17 years
            2. 18 to 24 years
            3. 25 to 54 years
            4. 55 years and above
        Parameters
        ----------
        in_percentage : bool
            boolean value determines if the output needs to be in percentage form or not

        Returns
        -------
        age_df : pd.core.frame.DataFrame 
            age data grouped into the above categories 

        '''
        assert(isinstance(in_percentage,bool))
        assert(not self.dframe.empty)
        age_data = self.get_key_data('AGE','state', False)
        age_total = self.get_key_data('AGE','Total', False)
        age_df_total = pd.DataFrame(index = age_data.index)
        age_df       = pd.DataFrame(index = age_data.index)
        list_1_to_17 = ['1 to 4 years', '5 to 17 years']
        list_18_to_24 = ['18 to 24 years']
        list_25_to_54 = ['25 to 34 years', '35 to 44 years', '45 to 54 years']
        list_55_and_over = ['55 to 64 years','65 to 74 years','75 years and over']
        
        keys_1_to_17 = self.query_group_keys(age_data, list_1_to_17)
        keys_1_to_17_total = self.query_group_keys(age_total, list_1_to_17)
        age_df['1 to 17 years'] = age_data[keys_1_to_17[0]] + age_data[keys_1_to_17[1]]
        age_df_total['1 to 17 years'] = age_total[keys_1_to_17_total[0]] + age_total[keys_1_to_17_total[1]]
        
        keys_18_to_24 = self.query_group_keys(age_data, list_18_to_24)
        keys_18_to_24_total = self.query_group_keys(age_total, list_18_to_24)
        age_df['18 to 24 years'] = age_data[keys_18_to_24[0]]
        age_df_total['18 to 24 years'] = age_total[keys_18_to_24_total[0]] 
        
        keys_25_to_54 = self.query_group_keys(age_data, list_25_to_54)
        keys_25_to_54_total = self.query_group_keys(age_total, list_25_to_54)
        age_df['25 to 54 years'] = age_data[keys_25_to_54[0]] + age_data[keys_25_to_54[1]] + age_data[keys_25_to_54[2]]
        age_df_total['25 to 54 years'] = age_total[keys_25_to_54_total[0]] + age_total[keys_25_to_54_total[1]]+ age_total[keys_25_to_54_total[2]]
        
        keys_55_and_over = self.query_group_keys(age_data, list_55_and_over)
        keys_55_and_over_total = self.query_group_keys(age_total, list_55_and_over)
        age_df['55 years and over'] = age_data[keys_55_and_over[0]] + age_data[keys_55_and_over[1]]+ age_data[keys_55_and_over[2]]
        age_df_total['55 years and over'] = age_total[keys_55_and_over_total[0]] + age_total[keys_55_and_over_total[1]]+ age_total[keys_55_and_over_total[2]]
        
        age_country = age_df.sum(axis = 0)
        age_total = age_df_total.sum(axis = 0)
        
        if in_percentage: 
            for col in age_country.keys():
                age_country[col] = 100*age_country[col]/age_total[col]
        return age_country

    # def get_sex_country_data(self,in_percentage):
    #     '''
    #     Function to query sex group data
    #     Data is given in below categories:
    #         1. Male
    #         2. Female

    #     Parameters
    #     ----------
    #     in_percentage : bool
    #         boolean value determines if the output needs to be in percentage form or not

    #     Returns
    #     -------
    #     sex_data : pd.core.frame.DataFrame 
    #         sex data grouped into the above categories 

    #     '''
    #     assert(isinstance(in_percentage,bool))
    #     assert(not self.dframe.empty)
    #     keys = ['Male', 'Female']
        
    #     sex_data = data_2010.get_key_data('SEX','state', False)
    #     grp_keys = data_2010.query_group_keys(sex_data, keys)
    #     rename_dict = {grp_keys[0]:"Male", grp_keys[1]:"Female"}
    #     sex_data = sex_data.rename(columns = rename_dict)
        
    #     sex_total_data = data_2010.get_key_data('SEX','Total', False)
    #     grp_keys = data_2010.query_group_keys(sex_total_data, keys)
    #     rename_dict = {grp_keys[0]:"Male", grp_keys[1]:"Female"}
    #     sex_total_data = sex_total_data.rename(columns = rename_dict)
        
    #     sex_country = sex_data.sum(axis = 0)
    #     sex_total = sex_total_data.sum(axis = 0)
        
    #     if in_percentage: 
    #         for col in sex_country.keys():
    #             sex_country[col] = 100*sex_country[col]/sex_total[col]
    #     sex_country = pd.DataFrame(sex_country)
    #     return sex_country

    def get_sex_group_data(self,in_percentage):
        '''
        Function to query sex group data
        Data is given in below categories:
            1. Male
            2. Female

        Parameters
        ----------
        in_percentage : bool
            boolean value determines if the output needs to be in percentage form or not

        Returns
        -------
        sex_data : pd.core.frame.DataFrame 
            sex data grouped into the above categories 

        '''
        assert(isinstance(in_percentage,bool))
        assert(not self.dframe.empty)
        sex_data = self.get_key_data('SEX','state', in_percentage)
        keys = ['Male', 'Female']
        grp_keys = self.query_group_keys(sex_data, keys)
        rename_dict = {grp_keys[0]:"Male", grp_keys[1]:"Female"}
        
        sex_data = sex_data.rename(columns = rename_dict)
        return sex_data

    def get_sex_country_data(self,in_percentage):
        '''
        Function to query sex group data
        Data is given in below categories:
            1. Male
            2. Female

        Parameters
        ----------
        in_percentage : bool
            boolean value determines if the output needs to be in percentage form or not

        Returns
        -------
        sex_data : pd.core.frame.DataFrame 
            sex data grouped into the above categories 

        '''
        assert(isinstance(in_percentage,bool))
        assert(not self.dframe.empty)
        keys = ['Male', 'Female']
        
        sex_data = self.get_key_data('SEX','state', False)
        grp_keys = self.query_group_keys(sex_data, keys)
        rename_dict = {grp_keys[0]:"Male", grp_keys[1]:"Female"}
        sex_data = sex_data.rename(columns = rename_dict)
        
        sex_total_data = self.get_key_data('SEX','Total', False)
        grp_keys = self.query_group_keys(sex_total_data, keys)
        rename_dict = {grp_keys[0]:"Male", grp_keys[1]:"Female"}
        sex_total_data = sex_total_data.rename(columns = rename_dict)
        
        sex_country = sex_data.sum(axis = 0)
        sex_total = sex_total_data.sum(axis = 0)
        
        if in_percentage: 
            for col in sex_country.keys():
                sex_country[col] = 100*sex_country[col]/sex_total[col]
        return sex_country
    
    def get_income_group_data(self,in_percentage):
        '''
        Function to query the income group data 
        Data is given in below categories:
            1. Loss or $1 to $34,999
            2. $35,000 to $49,999
            3. $50,000 to $74,999
            4. $75,000 or more 

        Parameters
        ----------
        in_percentage : bool
            boolean value determines if the output needs to be in percentage form or not

        Returns
        -------
        income_df : pd.core.frame.DataFrame 
            income data grouped into the above categories

        '''
        assert(isinstance(in_percentage,bool))
        assert(not self.dframe.empty)
        income_data = self.get_key_data('INDIVIDUAL INCOME','state', False)
        income_data_total = self.get_key_data('INDIVIDUAL INCOME','Total', False)
        income_df_total = pd.DataFrame(index = income_data.index)
        income_df       = pd.DataFrame(index = income_data.index)
        
        list_1_to_35 = ['$1 to $9,999','$10,000 to $14,999', '$15,000 to $24,999', '$25,000 to $34,999']
        list_35_to_50 = ['$35,000 to $49,999']
        list_50_to_75 = ['$50,000 to $64,999','$65,000 to $74,999']
        list_75_and_over = ['$75,000 or more']

        keys_1_to_35 = self.query_group_keys(income_data, list_1_to_35)
        keys_1_to_35_total = self.query_group_keys(income_data_total, list_1_to_35)
        income_df['loss or $1 to $34,999'] = income_data[keys_1_to_35[0]] + income_data[keys_1_to_35[1]] + income_data[keys_1_to_35[2]] + income_data[keys_1_to_35[3]]
        income_df_total['loss or $1 to $34,999'] = income_data_total[keys_1_to_35_total[0]] + income_data_total[keys_1_to_35_total[1]] + income_data_total[keys_1_to_35_total[2]] + income_data_total[keys_1_to_35_total[3]]
        
        keys_35_to_50 = self.query_group_keys(income_data, list_35_to_50)
        keys_35_to_50_total = self.query_group_keys(income_data_total, list_35_to_50)
        income_df['$35,000 to $49,999'] = income_data[keys_35_to_50[0]]
        income_df_total['$35,000 to $49,999'] = income_data_total[keys_35_to_50_total[0]]
        
        keys_50_to_75 = self.query_group_keys(income_data, list_50_to_75)
        keys_50_to_75_total = self.query_group_keys(income_data_total, list_50_to_75)
        income_df['$50,000 to $74,999'] = income_data[keys_50_to_75[0]] + income_data[keys_50_to_75[1]]
        income_df_total['$50,000 to $74,999'] = income_data_total[keys_50_to_75_total[0]] + income_data_total[keys_50_to_75_total[1]]
        
        keys_75_and_over = self.query_group_keys(income_data, list_75_and_over)
        keys_75_and_over_total = self.query_group_keys(income_data_total, list_75_and_over)
        income_df['$75,000 and over'] = income_data[keys_75_and_over[0]]
        income_df_total['$75,000 and over'] = income_data_total[keys_75_and_over_total[0]]
        
        if in_percentage:
            for col in income_df.columns:
                income_df[[col]] = income_df[[col]].div(income_df_total[[col]]) * 100
            return income_df 
        else:
            return income_df
    
    def get_income_country_data(self,in_percentage):
        '''
        Function to query the income group data 
        Data is given in below categories:
            1. Loss or $1 to $34,999
            2. $35,000 to $49,999
            3. $50,000 to $74,999
            4. $75,000 or more 
    
        Parameters
        ----------
        in_percentage : bool
            boolean value determines if the output needs to be in percentage form or not
    
        Returns
        -------
        income_df : pd.core.frame.DataFrame 
            income data grouped into the above categories
    
        '''
        assert(isinstance(in_percentage,bool))
        assert(not self.dframe.empty)
        income_data = self.get_key_data('INDIVIDUAL INCOME','state', False)
        income_data_total = self.get_key_data('INDIVIDUAL INCOME','Total', False)
        income_df_total = pd.DataFrame(index = income_data.index)
        income_df       = pd.DataFrame(index = income_data.index)
        
        list_1_to_35 = ['$1 to $9,999','$10,000 to $14,999', '$15,000 to $24,999', '$25,000 to $34,999']
        list_35_to_50 = ['$35,000 to $49,999']
        list_50_to_75 = ['$50,000 to $64,999','$65,000 to $74,999']
        list_75_and_over = ['$75,000 or more']

        keys_1_to_35 = self.query_group_keys(income_data, list_1_to_35)
        keys_1_to_35_total = self.query_group_keys(income_data_total, list_1_to_35)
        income_df['loss or $1 to $34,999'] = income_data[keys_1_to_35[0]] + income_data[keys_1_to_35[1]] + income_data[keys_1_to_35[2]] + income_data[keys_1_to_35[3]]
        income_df_total['loss or $1 to $34,999'] = income_data_total[keys_1_to_35_total[0]] + income_data_total[keys_1_to_35_total[1]] + income_data_total[keys_1_to_35_total[2]] + income_data_total[keys_1_to_35_total[3]]
        
        keys_35_to_50 = self.query_group_keys(income_data, list_35_to_50)
        keys_35_to_50_total = self.query_group_keys(income_data_total, list_35_to_50)
        income_df['$35,000 to $49,999'] = income_data[keys_35_to_50[0]]
        income_df_total['$35,000 to $49,999'] = income_data_total[keys_35_to_50_total[0]]
        
        keys_50_to_75 = self.query_group_keys(income_data, list_50_to_75)
        keys_50_to_75_total = self.query_group_keys(income_data_total, list_50_to_75)
        income_df['$50,000 to $74,999'] = income_data[keys_50_to_75[0]] + income_data[keys_50_to_75[1]]
        income_df_total['$50,000 to $74,999'] = income_data_total[keys_50_to_75_total[0]] + income_data_total[keys_50_to_75_total[1]]
        
        keys_75_and_over = self.query_group_keys(income_data, list_75_and_over)
        keys_75_and_over_total = self.query_group_keys(income_data_total, list_75_and_over)
        income_df['$75,000 and over'] = income_data[keys_75_and_over[0]]
        income_df_total['$75,000 and over'] = income_data_total[keys_75_and_over_total[0]]
        
        income_country = income_df.sum(axis = 0)
        income_total = income_df_total.sum(axis = 0)
        
        if in_percentage: 
            for col in income_country.keys():
                income_country[col] = 100*income_country[col]/income_total[col]
        return income_country

    def get_poverty_group_data(self,in_percentage):
        '''
        Function to query the poverty status group data 
        Data is given in below categories:
            1. Below 100 percent of the poverty level
            2. 100 to 150 percent of poverty level 
            3. above 150 percent of poverty level 

        Parameters
        ----------
        in_percentage : bool
            boolean value determines if the output needs to be in percentage form or not

        Returns
        -------
        pd.core.frame.DataFrame 
            poverty status data grouped into the above categories

        '''
        assert(not self.dframe.empty)
        assert(isinstance(in_percentage,bool))
        poverty_data = self.get_key_data('POVERTY STATUS','state', in_percentage)
        keys = ['Below 100 percent', '100 to 149 percent', 'above 150 percent']
        grp_keys = self.query_group_keys(poverty_data, keys)
        rename_dict = {grp_keys[0]:"Below 100 percent", grp_keys[1]:"100 to 149 percent", grp_keys[2]:"above 150 percent"}
        
        poverty_data = poverty_data.rename(columns = rename_dict)
        return poverty_data[keys]

    def get_poverty_country_data(self,in_percentage):
        '''
        Function to query the poverty status group data 
        Data is given in below categories:
            1. Below 100 percent of the poverty level
            2. 100 to 150 percent of poverty level 
            3. above 150 percent of poverty level 

        Parameters
        ----------
        in_percentage : bool
            boolean value determines if the output needs to be in percentage form or not

        Returns
        -------
        pd.core.frame.DataFrame 
            poverty status data grouped into the above categories

        '''
        assert(not self.dframe.empty)
        assert(isinstance(in_percentage,bool))
        poverty_data = self.get_key_data('POVERTY STATUS','state', False)
        keys = ['Below 100 percent', '100 to 149 percent', 'above 150 percent']
        grp_keys = self.query_group_keys(poverty_data, keys)
        rename_dict = {grp_keys[0]:"Below 100 percent", grp_keys[1]:"100 to 149 percent", grp_keys[2]:"above 150 percent"}
        poverty_data = poverty_data.rename(columns = rename_dict)
        poverty_data.iloc[: , 1:]
        
        poverty_data_total = self.get_key_data('POVERTY STATUS','Total', False)
        keys = ['Below 100 percent', '100 to 149 percent', 'above 150 percent']
        grp_keys = self.query_group_keys(poverty_data_total, keys)
        rename_dict = {grp_keys[0]:"Below 100 percent", grp_keys[1]:"100 to 149 percent", grp_keys[2]:"above 150 percent"}
        poverty_data_total = poverty_data_total.rename(columns = rename_dict)
        poverty_data_total.iloc[: , 1:]
        
        poverty_country = poverty_data.sum(axis = 0)
        poverty_data_total = poverty_data_total.sum(axis = 0)
        poverty_keys = ["Below 100 percent", "100 to 149 percent","above 150 percent"]
        poverty_country = poverty_country[poverty_keys]
        poverty_data_total = poverty_data_total[poverty_keys]
        
        if in_percentage: 
            for col in poverty_country.keys():
                poverty_country[col] = 100*poverty_country[col]/poverty_data_total[col]
        return poverty_country
    
    def get_housing_group_data(self,in_percentage):
        '''
        Function to query housing group data 
        Data is given in below categories:
            1. Owner-Owned 
            2. Renter-Owned 

        Parameters
        ----------
        in_percentage : bool
            boolean value determines if the output needs to be in percentage form or not

        Returns
        -------
        pd.core.frame.DataFrame 
            housing group data grouped into the above categories

        '''
        assert(not self.dframe.empty)
        assert(isinstance(in_percentage,bool))
        housing_data = self.get_key_data('HOUSING TENURE','state', in_percentage)
        keys = ['owner-occupied', 'renter-occupied']
        grp_keys = self.query_group_keys(housing_data, keys)
        rename_dict = {grp_keys[0]:"owner-occupied", grp_keys[1]:"renter-occupied"}
        
        housing_data = housing_data.rename(columns = rename_dict)
        return housing_data[keys]

    def get_housing_country_data(self,in_percentage):
        '''
        Function to query housing group data 
        Data is given in below categories:
            1. Owner-Owned 
            2. Renter-Owned 

        Parameters
        ----------
        in_percentage : bool
            boolean value determines if the output needs to be in percentage form or not

        Returns
        -------
        pd.core.frame.DataFrame 
            housing group data grouped into the above categories

        '''
        assert(not self.dframe.empty)
        assert(isinstance(in_percentage,bool))
        housing_data = self.get_key_data('HOUSING TENURE','state', False)
        keys = ['owner-occupied', 'renter-occupied']
        grp_keys = self.query_group_keys(housing_data, keys)
        rename_dict = {grp_keys[0]:"owner-occupied", grp_keys[1]:"renter-occupied"}
        housing_data = housing_data.rename(columns = rename_dict)
        
        housing_data_total = self.get_key_data('HOUSING TENURE','Total', False)
        keys = ['owner-occupied', 'renter-occupied']
        grp_keys = self.query_group_keys(housing_data_total, keys)
        rename_dict = {grp_keys[0]:"owner-occupied", grp_keys[1]:"renter-occupied"}
        housing_data_total = housing_data_total.rename(columns = rename_dict)
        
        housing_country = housing_data.sum(axis = 0)
        housing_total = housing_data_total.sum(axis = 0)
        housing_keys = ["owner-occupied","renter-occupied"]
        housing_country = housing_country[housing_keys]
        housing_total = housing_total[housing_keys]
        
        if in_percentage: 
            for col in housing_country.keys():
                housing_country[col] = 100*housing_country[col]/housing_total[col]
        return housing_country
    
    def get_education_group_data(self,in_percentage):
        '''
        Function to query educational attainment data 
        Data is grouped into below categories:
            1. High School and below
            2. Some College or Associate Degree
            3. Bachelors Degree and above

        Parameters
        ----------
        in_percentage : bool
            boolean value determines if the output needs to be in percentage form or not

        Returns
        -------
        pd.core.frame.DataFrame 
            educational attainment data grouped into the above categories

        '''
        assert(not self.dframe.empty)
        assert(isinstance(in_percentage,bool))
        ea_data = self.get_key_data('EDUCATIONAL ATTAINMENT','state', False)
        ea_data_total = self.get_key_data('EDUCATIONAL ATTAINMENT','Total', False)
        ea_df_total = pd.DataFrame(index = ea_data.index)
        ea_df       = pd.DataFrame(index = ea_data.index)
        
        list_1 = ['Less than high school','High school graduate']
        list_2 = ['Some college']
        list_3 = ['Bachelor','professional']

        keys_1 = self.query_group_keys(ea_data, list_1)
        keys_1_total = self.query_group_keys(ea_data_total, list_1)
        ea_df['High School and below'] = ea_data[keys_1[0]] + ea_data[keys_1[1]]
        ea_df_total['High School and below'] = ea_data_total[keys_1_total[0]] + ea_data_total[keys_1_total[1]]
        
        keys_2 = self.query_group_keys(ea_data, list_2)
        keys_2_total = self.query_group_keys(ea_data_total, list_2)
        ea_df['Some College or Associate Degree'] = ea_data[keys_2[0]]
        ea_df_total['Some College or Associate Degree'] = ea_data_total[keys_2_total[0]]
        
        keys_3 = self.query_group_keys(ea_data, list_3)
        keys_3_total = self.query_group_keys(ea_data_total, list_3)
        ea_df['Bachelors Degree and Above'] = ea_data[keys_3[0]] + ea_data[keys_3[1]]
        ea_df_total['Bachelors Degree and Above'] = ea_data_total[keys_3_total[0]] + ea_data_total[keys_3_total[1]]
        
        if in_percentage:
            for col in ea_df.columns:
                ea_df[[col]] = ea_df[[col]].div(ea_df_total[[col]]) * 100
            return ea_df 
        else:
            return ea_df

    def get_education_country_data(self,in_percentage):
        '''
        Function to query educational attainment data 
        Data is grouped into below categories:
            1. High School and below
            2. Some College or Associate Degree
            3. Bachelors Degree and above

        Parameters
        ----------
        in_percentage : bool
            boolean value determines if the output needs to be in percentage form or not

        Returns
        -------
        pd.core.frame.DataFrame 
            educational attainment data grouped into the above categories

        '''
        assert(not self.dframe.empty)
        assert(isinstance(in_percentage,bool))
        ea_data = self.get_key_data('EDUCATIONAL ATTAINMENT','state', False)
        ea_data_total = self.get_key_data('EDUCATIONAL ATTAINMENT','Total', False)
        ea_df_total = pd.DataFrame(index = ea_data.index)
        ea_df       = pd.DataFrame(index = ea_data.index)
        
        list_1 = ['Less than high school']
        list_1a = ['High school graduate']
        list_2 = ['Some college']
        list_3 = ['Bachelor']
        list_3a = ['professional']
        

        keys_1 = self.query_group_keys(ea_data, list_1)
        keys_1_total = self.query_group_keys(ea_data_total, list_1)
        ea_df['Less than high school'] = ea_data[keys_1[0]]
        ea_df_total['Less than high school'] = ea_data_total[keys_1_total[0]]
        
        keys_1a = self.query_group_keys(ea_data, list_1a)
        keys_1a_total = self.query_group_keys(ea_data_total, list_1a)
        ea_df['High school graduate'] = ea_data[keys_1a[0]]
        ea_df_total['High school graduate'] = ea_data_total[keys_1a_total[0]]
        
        keys_2 = self.query_group_keys(ea_data, list_2)
        keys_2_total = self.query_group_keys(ea_data_total, list_2)
        ea_df['Some College or Associate Degree'] = ea_data[keys_2[0]]
        ea_df_total['Some College or Associate Degree'] = ea_data_total[keys_2_total[0]]
        
        keys_3 = self.query_group_keys(ea_data, list_3)
        keys_3_total = self.query_group_keys(ea_data_total, list_3)
        ea_df['Bachelors Degree'] = ea_data[keys_3[0]]
        ea_df_total['Bachelors Degree'] = ea_data_total[keys_3_total[0]]
        
        keys_3a = self.query_group_keys(ea_data, list_3a)
        keys_3a_total = self.query_group_keys(ea_data_total, list_3a)
        ea_df['Professional Degree'] = ea_data[keys_3a[0]]
        ea_df_total['Professional Degree'] = ea_data_total[keys_3a_total[0]]
        
        ea_country = ea_df.sum(axis = 0)
        ea_df_total = ea_df_total.sum(axis = 0)
        
        if in_percentage: 
            for col in ea_country.keys():
                ea_country[col] = 100*ea_country[col]/ea_df_total[col]
        return ea_country
        
    def get_race_group_data(self,in_percentage):
        '''
        Function to query race group data
        Data is grouped into below categories:
            1. White
            2. Black or African American
            3. Hispanic or Latino 
            4. Asian
            5. Other

        Parameters
        ----------
        in_percentage : bool
            boolean value determines if the output needs to be in percentage form or not

        Returns
        -------
        race_data : pd.core.frame.DataFrame 
            race data grouped into the above categories (moving from a different state to the given row/state)

        '''
        assert(not self.dframe.empty)
        assert(isinstance(in_percentage,bool))
        race_data = self.get_key_data('RACE','state', in_percentage)
        keys = ['!!White','Black', 'Hispanic or Latino origin (of any race)','Asian', 'American Indian and Alaska Native', 'Two or more races', 'Some other race', 'Native Hawaiian and Other Pacific Islander']
        grp_keys = self.query_group_keys(race_data, keys)
        #print(grp_keys)
        race_data = race_data[grp_keys]
        rename_dict = {grp_keys[0]:"White", grp_keys[1]:"Black or African American", grp_keys[2]:"Hipanic or Latino", grp_keys[3]:"Asian", grp_keys[4]: "Other1" , grp_keys[5]:"Other2", grp_keys[6]: "Other3", grp_keys[7]: "Other4"}
        race_data = race_data.rename(columns = rename_dict)
        race_data["Other"] = race_data["Other1"] + race_data["Other2"] + race_data["Other3"] + race_data["Other4"]
        race_data = race_data.drop( columns = ["Other1", "Other2", "Other3", "Other4"])
        return race_data

    def get_race_country_data(self,in_percentage):
        '''
        Function to query race group data
        Data is grouped into below categories:
            1. White
            2. Black or African American
            3. Hispanic or Latino 
            4. Asian
            5. Other

        Parameters
        ----------
        in_percentage : bool
            boolean value determines if the output needs to be in percentage form or not

        Returns
        -------
        race_data : pd.core.frame.DataFrame 
            race data grouped into the above categories (moving from a different state to the given row/state)

        '''
        assert(not self.dframe.empty)
        assert(isinstance(in_percentage,bool))
        race_data = self.get_key_data('RACE','state', False)
        keys = ['!!White','Black', 'Hispanic or Latino origin (of any race)','Asian', 'American Indian and Alaska Native', 'Two or more races', 'Some other race', 'Native Hawaiian and Other Pacific Islander']
        grp_keys = self.query_group_keys(race_data, keys)
        #print(grp_keys)
        race_data = race_data[grp_keys]
        rename_dict = {grp_keys[0]:"White", grp_keys[1]:"Black or African American", grp_keys[2]:"Hipanic or Latino", grp_keys[3]:"Asian", grp_keys[4]: "Other1" , grp_keys[5]:"Other2", grp_keys[6]: "Other3", grp_keys[7]: "Other4"}
        race_data = race_data.rename(columns = rename_dict)
        race_data["Other"] = race_data["Other1"] + race_data["Other2"] + race_data["Other3"] + race_data["Other4"]
        race_data = race_data.drop( columns = ["Other1", "Other2", "Other3", "Other4"])
        
        race_data_total = self.get_key_data('RACE','Total', False)
        keys = ['!!White','Black', 'Hispanic or Latino origin (of any race)','Asian', 'American Indian and Alaska Native', 'Two or more races', 'Some other race', 'Native Hawaiian and Other Pacific Islander']
        grp_keys = self.query_group_keys(race_data_total, keys)
        #print(grp_keys)
        race_data_total = race_data_total[grp_keys]
        rename_dict = {grp_keys[0]:"White", grp_keys[1]:"Black or African American", grp_keys[2]:"Hipanic or Latino", grp_keys[3]:"Asian", grp_keys[4]: "Other1" , grp_keys[5]:"Other2", grp_keys[6]: "Other3", grp_keys[7]: "Other4"}
        race_data_total = race_data_total.rename(columns = rename_dict)
        race_data_total["Other"] = race_data_total["Other1"] + race_data_total["Other2"] + race_data_total["Other3"] + race_data_total["Other4"]
        race_data_total = race_data_total.drop( columns = ["Other1", "Other2", "Other3", "Other4"])
        
        race_country = race_data.sum(axis = 0)
        race_total = race_data_total.sum(axis = 0)
        
        if in_percentage: 
            for col in race_country.keys():
                race_country[col] = 100*race_country[col]/race_total[col]
        race_country = pd.DataFrame(race_country)
        return race_country

    def get_population_stats(self):
        '''
        Function to return overall population statistics of the current Migration Data object

        Returns
        -------
        population : pd.core.frame.DataFrame 
            population numbers and percentages along with the state information.

        '''
        assert(not self.dframe.empty)
        
        if self.year > 2017:
            key_str = 'Estimate!!Moved; from different  state!!Population 1 year and over'
        else:
            key_str = 'Moved; from different  state!!Estimate!!Population 1 year and over'
        pop_key = self.get_key(self.dframe, key_str)
        
        if self.year > 2017:
            key_str = 'Estimate!!Total!!Population 1 year and over'
        else:
            key_str = 'Total!!Estimate!!Population 1 year and over'
        pop_total_key = self.get_key(self.dframe, key_str)
        
        population_keys = ['Geographic Area Name', pop_key, pop_total_key]
        population = self.dframe[population_keys].rename(columns = {"Geographic Area Name":"state", pop_key:'population', pop_total_key:'population_total'})
        population['population_total'] = (population['population_total'].astype(float)).mul(population['population'].astype(float))//100
        return population
        
if __name__ == '__main__':
    data_2010 = MigrationData(2018)
    data_2010.load_dframe()
    
    age_data = data_2010.get_key_data('AGE', 'state', False)        
    age_group_data = data_2010.get_age_group_data(True)
    sex_data = data_2010.get_key_data('SEX', 'state', False) 
    sex_group_data = data_2010.get_sex_group_data(True)  
    income_data = data_2010.get_key_data('INDIVIDUAL INCOME','state', False)
    income_group_data = data_2010.get_income_group_data(True)
    poverty_data = data_2010.get_key_data('POVERTY STATUS','state', False)
    poverty_group_data = data_2010.get_poverty_group_data(True)
    housing_data = data_2010.get_key_data('HOUSING TENURE','state', False)
    housing_group_data = data_2010.get_housing_group_data(True)
    race_data = data_2010.get_key_data('RACE','state', True)
    race_data_total = data_2010.get_key_data('RACE','state', False)
    
    race_group_data = data_2010.get_race_group_data(True)
    # race_group_data = data_2010.get_race_group_data(False)
    
    ea_data = data_2010.get_key_data('EDUCATIONAL ATTAINMENT','state', False)
    ea_group_data = data_2010.get_education_group_data(True)
    pop_stats = data_2010.get_population_stats()
    sex_country = data_2010.get_sex_country_data(True)
    age_country = data_2010.get_age_country_data(True)
    
    
