# app.py
# Streamlit-based Admin Panel for AI-Agent for Admission Inquiry
# This GUI allows university staff to view, add, edit, and delete admission FAQ entries.

import streamlit as st
import pandas as pd
import json
from uuid import uuid4

# --- Data Storage ---
DATA_FILE = 'faqs.json'

# Load FAQs from JSON file
@st.cache_data
def load_faqs():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Save FAQs to JSON file
def save_faqs(faqs):
    with open(DATA_FILE, 'w') as f:
        json.dump(faqs, f, indent=2)

# --- Helper Functions ---

def add_faq(question, answer, category, language):
    faqs = load_faqs()
    new_entry = {
        'id': str(uuid4()),
        'question': question,
        'answer': answer,
        'category': category,
        'language': language
    }
    faqs.append(new_entry)
    save_faqs(faqs)
    return new_entry


def update_faq(entry_id, question, answer, category, language):
    faqs = load_faqs()
    for faq in faqs:
        if faq['id'] == entry_id:
            faq['question'] = question
            faq['answer'] = answer
            faq['category'] = category
            faq['language'] = language
            break
    save_faqs(faqs)


def delete_faq(entry_id):
    faqs = load_faqs()
    faqs = [faq for faq in faqs if faq['id'] != entry_id]
    save_faqs(faqs)

# --- Streamlit UI ---
st.title('AI-Agent Admission Inquiry - Admin Panel')
st.write('Manage FAQ entries for the WhatsApp chatbot.')

# Sidebar navigation
action = st.sidebar.selectbox('Action', ['View FAQs', 'Add FAQ', 'Edit FAQ', 'Delete FAQ'])

if action == 'View FAQs':
    st.header('All FAQ Entries')
    faqs = load_faqs()
    if faqs:
        df = pd.DataFrame(faqs).drop(columns=['id'])
        st.dataframe(df)
    else:
        st.info('No FAQs found. Add new entries!')

elif action == 'Add FAQ':
    st.header('Add a New FAQ')
    q = st.text_area('Question')
    a = st.text_area('Answer')
    c = st.text_input('Category (e.g., Admission Requirements)')
    lang = st.selectbox('Language', ['English', 'Urdu', 'Roman Urdu'])
    if st.button('Add'):  
        if q and a and c:
            entry = add_faq(q, a, c, lang)
            st.success(f"Added FAQ with ID: {entry['id']}")
        else:
            st.error('Please fill in all fields.')

elif action == 'Edit FAQ':
    st.header('Edit an Existing FAQ')
    faqs = load_faqs()
    ids = {f"{faq['question']} ({faq['id']})": faq['id'] for faq in faqs}
    if ids:
        choice = st.selectbox('Select FAQ to edit', list(ids.keys()))
        selected = next(f for f in faqs if f['id'] == ids[choice])
        q = st.text_area('Question', selected['question'])
        a = st.text_area('Answer', selected['answer'])
        c = st.text_input('Category', selected['category'])
        lang = st.selectbox('Language', ['English', 'Urdu', 'Roman Urdu'], index=['English','Urdu','Roman Urdu'].index(selected['language']))
        if st.button('Update'):
            update_faq(selected['id'], q, a, c, lang)
            st.success('FAQ updated successfully.')
    else:
        st.info('No FAQs available to edit.')

elif action == 'Delete FAQ':
    st.header('Delete an FAQ')
    faqs = load_faqs()
    ids = {f"{faq['question']} ({faq['id']})": faq['id'] for faq in faqs}
    if ids:
        choice = st.selectbox('Select FAQ to delete', list(ids.keys()))
        if st.button('Delete'):
            delete_faq(ids[choice])
            st.success('FAQ deleted successfully.')
    else:
        st.info('No FAQs available to delete.')

# Run with: streamlit run app.py
