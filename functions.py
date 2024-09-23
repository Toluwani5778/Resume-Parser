import re
import nltk
import os
import spacy
from spacy.matcher import Matcher
import constants as cs
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import PyPDF2 as pdf
from docx2pdf import convert
import tempfile
import streamlit as st
from nltk.stem import WordNetLemmatizer
nltk.download('wordnet')

nlp = spacy.load("en_core_web_sm")
def read_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, 'rb') as f:
            reader = pdf.PdfReader(f)
            text = ""
            for page_num in range(len(reader.pages)):
                text += reader.pages[page_num].extract_text()
        return text
    except Exception as e:
        print(f"Error reading text from PDF: {e}")
        st.write("Error")
        return None

def remove_square_brackets(my_list):
    # Convert the list elements to strings
    list_as_string = ', '.join(map(str, my_list))
    # Remove the square brackets
    result = list_as_string[1:-1]  # Slice the string to remove the brackets
    return result

def convert_docx_to_pdf(docx_path):
    try:
        # Convert DOCX to PDF
        pdf_path = tempfile.mktemp(suffix='.pdf')
        convert(docx_path, pdf_path)
        return pdf_path
    except Exception as e:
        print(f"Error converting DOCX to PDF: {e}")
        return None

def extract_email(text):
    '''
    Helper function to extract email id from text

    :param text: plain text extracted from resume file
    '''
    email = re.findall(r"([^@|\s]+@[^@]+\.[^@|\s]+)", text)
    if email:
        try:
            return email[0].split()[0].strip(';')
        except IndexError:
            return None

def remove_newlines(text):
  """Removes all newline characters (`\n`) from a string."""
  return text.replace('\n', '')

def extract_phone_numbers(text):
    '''
    Function to extract phone numbers from text

    :param text: plain text containing phone numbers
    :return: list of phone numbers found in the text
    '''
    pattern = re.compile(r'(?<!\n)(\+?\d{0,3}\s?[-\.\(\)]?\s?\(?\d{3}\)?\s?[-\.\(\)]?\s?\d{3}\s?[-\.\(\)]?\s?\d{4})')

    # Find all matches of the pattern in the text
    matches = re.findall(pattern, text)
    clean_matches = [remove_newlines(match).lstrip() for match in matches]
    # Return the list of phone numbers found
    return clean_matches


def extract_name_impro(full_name):
    # Regular expression patterns for different name formats
    patterns = [
        # First name, middle initial, last name
        r'^([A-Z][a-z]+)\s+([A-Z])\.\s+([A-Z][a-z]+)$',
        # First name, last name
        r'^([A-Z][a-z]+)\s+([A-Z][a-z]+)$',
        # First name
        r'^([A-Z][a-z]+)$'
    ]

    # Iterate through each pattern and attempt to match
    for pattern in patterns:
        match = re.match(pattern, full_name)
        if match:
            # Extract the parts based on the matched pattern
            if len(match.groups()) == 3:
                return match.group(1), match.group(2), match.group(3)
            elif len(match.groups()) == 2:
                return match.group(1), None, match.group(2)
            else:
                return match.group(1), None, None

    # If no match found, return None
    return None, None, None

def extract_name(nlp_text):
    '''
    Helper function to extract name from spacy nlp text

    :param nlp_text: object of `spacy.tokens.doc.Doc`
    :param matcher: object of `spacy.matcher.Matcher`
    :return: string of full name
    '''
    matcher = Matcher(nlp.vocab)
    for pattern in cs.NAME_PATTERN:
        matcher.add('NAME', [pattern])
    matches = matcher(nlp_text)

    for _, start, end in matches:
        span = nlp_text[start:end]
        if 'name' not in span.text.lower():
            return span.text



def detect_date_format(date_str):
    '''
    Detects the format of the input date string.

    :param date_str: Input date string
    :return: Detected date format
    '''
    formats = [
        ('%b %Y', 'Month YYYY'),
        ('%Y-%m-%d', 'YYYY-MM-DD'),  # ISO 8601 format
        ('%m/%d/%Y', 'MM/DD/YYYY'),  # US format
        ('%d-%m-%Y', 'DD-MM-YYYY'),  # European/African format
        ('%B %dst, %Y', 'Month DDst, YYYY'),  # Full month name with ordinal day
        ('%B %dnd, %Y', 'Month DDnd, YYYY'),  # Full month name with ordinal day
        ('%B %drd, %Y', 'Month DDrd, YYYY'),  # Full month name with ordinal day
        ('%B %dth, %Y', 'Month DDth, YYYY')  # Full month name with ordinal day
    ]

    for date_format, format_name in formats:
        try:
            datetime.strptime(date_str, date_format)
            return format_name
        except ValueError:
            continue

    return 'Unknown'


def get_number_of_months_from_dates(date1, date2):
    '''
    Helper function to extract total months of experience from a resume

    :param date1: Starting date
    :param date2: Ending date
    :return: months of experience from date1 to date2
    '''
    months_of_experience = 0  # Default value

    if detect_date_format(date1) == 'YYYY-MM-DD':
        if date2.lower() == 'present':
            date2 = datetime.now().strftime('%Y-%m-%d')
        try:
            start_date = datetime.strptime(str(date1), '%Y-%m-%d')
            end_date = datetime.strptime(str(date2), '%Y-%m-%d')
            months_of_experience = (end_date.year - start_date.year) * 12 + (
                    end_date.month - start_date.month)
        except ValueError:
            return 0

    elif detect_date_format(date1) == 'MM/DD/YYYY':
        if date2.lower() == 'present':
            date2 = datetime.now().strftime('%m/%d/%Y')
        try:
            start_date = datetime.strptime(str(date1), '%m/%d/%Y')
            end_date = datetime.strptime(str(date2), '%m/%d/%Y')
            months_of_experience = (end_date.year - start_date.year) * 12 + (
                    end_date.month - start_date.month)
        except ValueError:
            return 0

    elif detect_date_format(date1) == 'DD-MM-YYYY':
        if date2.lower() == 'present':
            date2 = datetime.now().strftime('%d-%m-%Y')
        try:
            start_date = datetime.strptime(str(date1), '%d-%m-%Y')
            end_date = datetime.strptime(str(date2), '%d-%m-%Y')
            months_of_experience = (end_date.year - start_date.year) * 12 + (
                    end_date.month - start_date.month)
        except ValueError:
            return 0

    elif detect_date_format(date1) == 'Month DDst, YYYY':
        if date2.lower() == 'present':
            date2 = datetime.now().strftime('%B %dst, %Y')
        try:
            start_date = datetime.strptime(str(date1), '%B %dst, %Y')
            end_date = datetime.strptime(str(date2), '%B %dst, %Y')
            months_of_experience = (end_date.year - start_date.year) * 12 + (
                    end_date.month - start_date.month)
        except ValueError:
            return 0
    elif detect_date_format(date1) == 'Month DDnd, YYYY':
        if date2.lower() == 'present':
            date2 = datetime.now().strftime('%B %dnd, %Y')
        try:
            start_date = datetime.strptime(str(date1), '%B %dnd, %Y')
            end_date = datetime.strptime(str(date2), '%B %dnd, %Y')
            months_of_experience = (end_date.year - start_date.year) * 12 + (
                    end_date.month - start_date.month)
        except ValueError:
            return 0
    elif detect_date_format(date1) == 'Month DDrd, YYYY':
        if date2.lower() == 'present':
            date2 = datetime.now().strftime('%B %drd, %Y')
        try:
            start_date = datetime.strptime(str(date1), '%B %drd, %Y')
            end_date = datetime.strptime(str(date2), '%B %drd, %Y')
            months_of_experience = (end_date.year - start_date.year) * 12 + (
                    end_date.month - start_date.month)
        except ValueError:
            return 0
    elif detect_date_format(date1) == 'Month DDth, YYYY':
        if date2.lower() == 'present':
            date2 = datetime.now().strftime('%B %dth, %Y')
        try:
            start_date = datetime.strptime(str(date1), '%B %dth, %Y')
            end_date = datetime.strptime(str(date2), '%B %dth, %Y')
            months_of_experience = (end_date.year - start_date.year) * 12 + (
                    end_date.month - start_date.month)
        except ValueError:
            return 0
    elif detect_date_format(date1) == 'Month YYYY':

        if date2.lower() == 'present':
            date2 = datetime.now().strftime('%b %Y')
        try:
            if len(date1.split()[0]) > 3:
                date1 = date1.split()
                date1 = date1[0][:3] + ' ' + date1[1]
            if len(date2.split()[0]) > 3:
                date2 = date2.split()
                date2 = date2[0][:3] + ' ' + date2[1]
        except IndexError:
            return 0
        try:
            date1 = datetime.strptime(str(date1), '%b %Y')
            date2 = datetime.strptime(str(date2), '%b %Y')
            months_of_experience = relativedelta(date2, date1)
            months_of_experience = (months_of_experience.years * 12 +
                                    months_of_experience.months)
        except ValueError:
            return 0
    else:
        try:
            pass
        except Exception as e:
            return "Can't calculate"

    return months_of_experience


def extract_skills(nlp_text, skills_file=None):
    '''
    Helper function to extract skills from spacy nlp text

    :param nlp_text: object of `spacy.tokens.doc.Doc`
    :param noun_chunks: noun chunks extracted from nlp text
    :return: list of skills extracted
    '''
    tokens = [token.text for token in nlp_text if not token.is_stop]
    noun_chunks = nlp_text.noun_chunks
    if not skills_file:
        data = pd.read_csv(
            os.path.join(os.getcwd(), 'skills.csv')
        )
    else:
        data = pd.read_csv(skills_file)
    skills = list(data.columns.values)
    skillset = []
    # check for one-grams
    for token in tokens:
        if token.lower() in skills:
            skillset.append(token)

    # check for bi-grams and tri-grams
    for token in noun_chunks:
        token = token.text.lower().strip()
        if token in skills:
            skillset.append(token)
    return [i.capitalize() for i in set([i.lower() for i in skillset])]

def extract_education(nlp_text):
    '''
    Helper function to extract education from spacy nlp text

    :param nlp_text: object of `spacy.tokens.doc.Doc`
    :return: tuple of education degree and year if year if found
             else only returns education degree
    '''
    edu = {}
    # Extract education degree
    try:
        for token in nlp_text:
            token_text = token.text.strip()
            token_text = re.sub(r'[?|$|.|!|,]', r'', token_text)
            if token_text.upper() in cs.EDUCATION and token_text not in cs.STOPWORDS:
                # Concatenate current token with next token if available
                next_token = nlp_text[token.i + 1].text if token.i + 1 < len(nlp_text) else ''
                edu[token_text] = token.text + next_token
    except IndexError:
        pass

    # Extract year
    education = []
    for key in edu.keys():
        year = re.search(re.compile(cs.YEAR), edu[key])
        if year:
            education.append((key, ''.join(year.group(0))))
        else:
            education.append(key)
    return education

def extract_education_from_resume(text):
    education = []

    # Use regex pattern to find education information
    pattern = r"(?i)(?:Bsc|\bB\.\w+|\bM\.\w+|\bPh\.D\.\w+|\bBachelor(?:'s)?|\bMaster(?:'s)?|\bPh\.D)\s(?:\w+\s)*\w+"
    matches = re.findall(pattern, text)
    for match in matches:
        education.append(match.strip())

    return education

def extract_entity_sections(text):
    '''
    Helper function to extract all the raw text from sections of
    resume specifically for graduates and undergraduates

    :param text: Raw text of resume
    :return: dictionary of entities
    '''
    text_split = [i.strip() for i in text.split('\n')]
    entities = {}
    key = False
    for phrase in text_split:
        if len(phrase) == 1:
            p_key = phrase
        else:
            p_key = set(phrase.lower().split()) & set(cs.RESUME_SECTIONS)
        try:
            p_key = list(p_key)[0]
        except IndexError:
            pass
        if p_key in cs.RESUME_SECTIONS:
            entities[p_key] = []
            key = p_key
        elif key and phrase.strip():
            entities[key].append(phrase)

    return entities
