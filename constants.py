from nltk.corpus import stopwords

# Omkar Pathak, improved by Toluwani
NAME_PATTERN = [
    [{
        'POS': 'PROPN'
    }, {
        'POS': 'PROPN'
    }],  # First name and Last name
[
    {'POS': 'PROPN'},  # Firstname
    {'IS_PUNCT': True},  # Middle initial punctuation (.)
    {'IS_ALPHA': True, 'LENGTH': 1},  # Middle initial
    {'POS': 'PROPN'}  # Last name
],
    [{
        'POS': 'PROPN'
    }, {
        'POS': 'PROPN'
    }, {
        'POS': 'PROPN'
    }],  # First name, Middle name, and Last name
    [{
        'POS': 'PROPN'
    }, {
        'POS': 'PROPN'
    }, {
        'POS': 'PROPN'
    }, {
        'POS': 'PROPN'
    }]  # First name, Middle name, Middle name, and Last name
    # Add more patterns as needed
]

# Education (Upper Case Mandatory)
EDUCATION = [
    'BE', 'B.E.', 'B.E', 'BS', 'B.S', 'ME', 'M.E', 'M.E.', 'MS', 'M.S',
    'BTECH', 'MTECH', 'SSC', 'HSC', 'CBSE', 'ICSE', 'X', 'XII', 'BACHELOR',
    'BSC', 'B. PHARMACY', 'B PHARMACY', 'MSC', 'M. PHARMACY', 'PH.D', 'MASTER',
    'AA', 'AS', 'BA', 'MA', 'PHD', 'EDD', 'DPT', 'JD', 'MD', 'PHARMD',
    'DIPLOMA', 'CERTIFICATE', 'PHARMACY TECHNICIAN CERTIFICATION',
    'BS/BSC IN COMPUTER SCIENCE', 'BS/BSC IN BIOLOGY', 'BS/BSC IN ENGINEERING',
    'BA IN ENGLISH', 'BA IN HISTORY', 'BA IN FINE ARTS', 'BBA', 'MBA', 'M.ED.',
    'TEACHING CERTIFICATE', 'B.SC.', 'PH.D.'
]

NOT_ALPHA_NUMERIC = r'[^a-zA-Z\d]'

NUMBER = r'\d+'

# For finding date ranges
MONTHS_SHORT = r'''(jan)|(feb)|(mar)|(apr)|(may)|(jun)|(jul)
                   |(aug)|(sep)|(oct)|(nov)|(dec)'''
MONTHS_LONG = r'''(january)|(february)|(march)|(april)|(may)|(june)|(july)|
                   (august)|(september)|(october)|(november)|(december)'''
MONTH = r'(' + MONTHS_SHORT + r'|' + MONTHS_LONG + r')'
YEAR = r'(((20|19)(\d{2})))'

STOPWORDS = set(stopwords.words('english'))

RESUME_SECTIONS_PROFESSIONAL = [
    'experience', 'education', 'interests', 'professional experience',
    'publications', 'skills', 'certifications', 'objective',
    'career objective', 'summary', 'leadership'
]

RESUME_SECTIONS_GRAD = [
    'accomplishments', 'experience', 'education', 'interests', 'projects',
    'professional experience', 'publications', 'skills', 'certifications',
    'objective', 'career objective', 'summary', 'leadership'
]

RESUME_SECTIONS = [
    'experience', 'education', 'interests', 'projects',
    'relevant experience', 'publication', 'certificates',
    'objective', 'career objective', 'summary', 'leadership', 'honors', 'technical skills'
]