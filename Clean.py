import pandas as pd

# Load the raw dataset
df = pd.read_csv(r'D:\Country.csv')

# Display all columns and rows for easier inspection
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# ==============================================
# 1. Remove Aggregates and Non-Country Entries
# ==============================================
unwanted = [
    'Arab World', 'Euro area', 'European Union', 'North America', 'South Asia', 'Small states',
    'Latin America & Caribbean (developing only)', 'Caribbean small states', 'Central Europe and the Baltics',
    'Channel Islands', 'East Asia & Pacific (all income levels)', 'East Asia & Pacific (developing only)',
    'Europe & Central Asia (all income levels)', 'Europe & Central Asia (developing only)',
    'Fragile and conflict affected situations', 'Heavily indebted poor countries (HIPC)', 'High income',
    'High income: nonOECD', 'High income: OECD', 'Hong Kong SAR, China', 'Lao PDR',
    'Latin America & Caribbean (all income levels)', 'Latin America & Caribbean (developing only',
    'Least developed countries: UN classification', 'Low & middle income', 'Low income',
    'Lower middle income', 'Macao SAR, China', 'Middle East & North Africa (all income levels)',
    'Middle East & North Africa (developing only)', 'Middle income', 'OECD members',
    'Other small states', 'Pacific island small states', 'Sub-Saharan Africa (all income levels)',
    'Sub-Saharan Africa (developing only)', 'Upper middle income', 'West Bank and Gaza', 'World'
]
df = df[~df['ShortName'].isin(unwanted)]

# ==============================================
# 2. Rename and Drop Unnecessary Columns
# ==============================================
df['CountryName'] = df['ShortName']
df.drop(columns=['TableName', 'ShortName'], inplace=True)

# Manually fix Alpha2Code for special cases
df.loc[df['CountryName'].str.contains('Kosovo', na=False), 'Alpha2Code'] = 'XK'
df.loc[df['CountryName'].str.contains('Namibia', na=False), 'Alpha2Code'] = 'NA'

# Rename 'LongName' to 'CountryLongName'
df['CountryLongName'] = df['LongName']
df.drop(columns='LongName', inplace=True)

# ==============================================
# 3. Standardize Year Columns and Fill Missing
# ==============================================
df['LatestWaterWithdrawalData'] = df['LatestWaterWithdrawalData'].fillna(0).astype(int)
df['LatestTradeData'] = df['LatestTradeData'].fillna(0).astype(int)
df['LatestIndustrialData'] = df['LatestIndustrialData'].fillna(0).astype(int)

# Fill missing notes with empty string
df['SpecialNotes'] = df['SpecialNotes'].fillna('')

# Fix mislabeling in income groups
df['IncomeGroup'] = df['IncomeGroup'].str.replace('Upper income', 'Upper middle income')

# Extract year from string columns
df['NationalAccountsBaseYear'] = df['NationalAccountsBaseYear'].fillna('').str.extract(r'(\d{4})').fillna(0)
df['NationalAccountsReferenceYear'] = df['NationalAccountsReferenceYear'].astype(str).str.extract(r'(\d{4})').fillna(0)
df['NationalAccountsReferenceYear'] = df['NationalAccountsReferenceYear'].astype(int)

# Fill base year with reference year if missing
df.loc[df['NationalAccountsBaseYear'] == 0, 'NationalAccountsBaseYear'] = df['NationalAccountsReferenceYear']

# Clean agricultural census year
df['LatestAgriculturalCensus'] = df['LatestAgriculturalCensus'].str.extract(r'(\d{4})').fillna(0).astype(int)

# Drop unused column
df.drop(columns='Wb2Code', inplace=True)

# Extract value from parentheses in SNA valuation
df['SnaPriceValuation'] = df['SnaPriceValuation'].str.extract(r'\((\w+)\)').fillna('')

# Fill missing in multiple fields
df[['LendingCategory', 'OtherGroups']] = df[['LendingCategory', 'OtherGroups']].fillna('')

# ==============================================
# 4. Handle Missing Values (Drop low-quality columns)
# ==============================================
threshold = len(df) * 0.5  # Drop columns with more than 50% missing
df = df.dropna(thresh=threshold, axis=1)
df.fillna("Unknown", inplace=True)

# ==============================================
# 5. Extract and Clean Numeric/Category Info
# ==============================================
df['PppSurveyYear'] = df['PppSurveyYear'].str.extract(r'(\d{4})')
df['PppSurveyYear'] = pd.to_numeric(df['PppSurveyYear'], errors='coerce').fillna(0).astype(int)

df['TypeOfSystemOfNationalAccounts'] = df['SystemOfNationalAccounts'].str.extract('(\d{4})').astype(int)
df.drop(columns='SystemOfNationalAccounts', inplace=True)

# Extract edition (e.g., "6th") and source (e.g., "IMF") from BOP manual
df['Edition'] = df['BalanceOfPaymentsManualInUse'].str.extract(r'(\d+(?:st|nd|th|rd))')
df['BalanceOfPaymentsManual'] = df['BalanceOfPaymentsManualInUse'].str.extract(r'^(IMF)')
df[['Edition', 'BalanceOfPaymentsManual']] = df[['Edition', 'BalanceOfPaymentsManual']].fillna("Unknown")
df.drop(columns='BalanceOfPaymentsManualInUse', inplace=True)

# Extract dissemination standard from parentheses
df['ImfDataDisseminationStandard'] = df['ImfDataDisseminationStandard'].str.extract(r'\((\w+)\)').fillna('Unknown')

# Clean population census year
df['LatestPopulationCensus'] = df['LatestPopulationCensus'].str.extract(r'(\d{4})').fillna(0).astype(int)

# Extract household survey code and year
df['LatestHouseholdSurveys'] = df['LatestHouseholdSurvey'].str.extract(r'\b([A-Z]{2,5})\b').fillna('Unknown')
df['LatestHouseholdSurveysDate'] = df['LatestHouseholdSurvey'].str.extract(r'(\d{4})').fillna(0).astype(int)
df.drop(columns='LatestHouseholdSurvey', inplace=True)

# Extract income data source and year
df['SourceOfMostRecentIncome'] = df['SourceOfMostRecentIncomeAndExpenditureData'].str.extract(r'\(([\w/]+)\)').fillna('Unknown')
df['ExpDataOfMostSourceRecentIncome'] = df['SourceOfMostRecentIncomeAndExpenditureData'].str.extract(r'(\d{4})').fillna(0).astype(int)
df.drop(columns='SourceOfMostRecentIncomeAndExpenditureData', inplace=True)

# (Optional) Print special notes for manual inspection
print(df['SpecialNotes'])

# Save the cleaned dataset
df.to_csv(r'D:\Country_CLEANED.csv', index=False)
