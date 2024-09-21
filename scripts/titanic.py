import pandas as pd
import argparse
import logging


#Task 3
# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("titanic_clean.log"),
        logging.StreamHandler()
    ]
)


#Task 1
class TitanicCleaner:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
        
    def load_data(self):
        logging.info(f"Loading data from {self.file_path}")
        self.df = pd.read_csv('tested.csv')
        logging.info('Data loaded successfully')
 
 # Fill Missing Values       
    def fill_missing_values(self):
        logging.info('Filling Missing Values')
        self.df['Age'].fillna(self.df['Age'].median(), inplace=True)
        self.df['Fare'].fillna(self.df['Fare'].median(), inplace=True)
        self.df['Cabin'].fillna(self.df['Cabin'].mode()[0], inplace=True)
    
 # Remove Duplicates   
    def remove_duplicates(self):
        logging.info('Removing Duplicates')
        self.df.drop_duplicates(inplace=True)
        
    def clean_data(self):
        self.fill_missing_values()
        self.remove_duplicates()
    
    def get_cleaned_data(self):
        return self.df

# Create age_bin    
    def age_bin(self):
        logging.info('Create an Age bin')
        def age_binning(age):
            if age < 18:
                return '<18'
            elif 18 <= age < 40:
                return '18-40'
            elif 40 <= age < 60:
                return '40-60'
            else:
                return '60+'
        
        self.df['AgeGroup'] = self.df['Age'].apply(age_binning)

# Create a new column called FamilySize    
    def family_size(self):
        logging.info('Creating a new column called FamilySize')
        self.df['FamilySize'] = self.df.apply(lambda row: row['SibSp'] + row['Parch'], axis=1)

# Map S as Southhampton, C as Cherbourg, and Q as Queenstown from Embarked column    
    def map_embarked(self):
        logging.info('Mapping the embarked column')
        embarked_map = {'S': 'Southampton', 'C': 'Cherbourg', 'Q': 'Queenstown'}
        self.df['Embarked'] = self.df['Embarked'].apply(lambda x: embarked_map.get(x, x))
    
 
cleaner = TitanicCleaner('tested.csv')
cleaner.load_data()
cleaner.clean_data()
cleaner.age_bin()
cleaner.family_size()
cleaner.map_embarked()
cleaned_df = cleaner.get_cleaned_data()
cleaned_df.head()
    
# TASK 2

def main():
    # Initialize argument parser
    parser = argparse.ArgumentParser(description="Clean Titanic data and apply transformations.")
    
    # Add arguments
    parser.add_argument('--file', type=str, required=True, help="Path to the Titanic CSV data file.") #specifies where my file is
    parser.add_argument('--output', type=str, required=False, help="Path to save the cleaned and transformed data.") # If I run this in the terminal, I get a new csv file with all my cleaning steps applied
    parser.add_argument('--clean', action='store_true', help="Clean the data (fill missing values, remove duplicates).")
    parser.add_argument('--age_bin', action='store_true', help="Bin the 'Age' column into categories.")
    parser.add_argument('--family_size', action='store_true', help="Calculate family size from 'SibSp' and 'Parch'.")
    parser.add_argument('--map_embarked', action='store_true', help="Map 'Embarked' column values to full port names.")
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Initialize TitanicCleaner with the provided file path
    cleaner = TitanicCleaner(args.file)
    cleaner.load_data() 
    # Perform cleaning if specified
    if args.clean:
        cleaner.clean_data()
    
    # Apply transformations if specified
    if args.age_bin:
        cleaner.age_bin()
    
    if args.family_size:
        cleaner.family_size()
    
    if args.map_embarked:
        cleaner.map_embarked()
        
    # Get the cleaned and transformed data
    cleaned_df = cleaner.get_cleaned_data()
    
    # Output the data to the specified file or print the first few rows
    if args.output:
        cleaned_df.to_csv(args.output, index=False)
        print(f"Cleaned data saved to {args.output}")
    else:
        print(cleaned_df.head())
        
if __name__ == "__main__":
     main()