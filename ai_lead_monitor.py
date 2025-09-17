
import pandas as pd
import openai
from datetime import datetime, timedelta
import streamlit as st
import random

# ---- CONFIG ----
openai.api_key = "YOUR_OPENAI_API_KEY"  # Replace with your OpenAI API key
keywords = ["Python", "React", "SEO", "automation", "logo", "writing"]

# ---- FUNCTIONS ----

def generate_new_lead():
    titles = ["Create a React App", "SEO Blog Writing", "Python Data Scraper",
              "Design a Company Logo", "Automation Script Development", "Content Writing"]
    descriptions = [
        "Develop a React frontend for a startup project.",
        "5 blog posts about travel destinations.",
        "Scrape e-commerce data into CSV automatically.",
        "Design a modern minimalist logo for a tech startup.",
        "Automate Excel data processing with Python.",
        "Write engaging SEO-friendly content for websites."
    ]
    budgets = [400, 180, 500, 200, 450, 150]
    clients = ["Client D", "Client E", "Client F", "Client G", "Client H", "Client I"]

    i = random.randint(0, len(titles) - 1)
    lead = {
        "title": titles[i],
        "description": descriptions[i],
        "budget": budgets[i],
        "client": clients[i],
        "date_posted": datetime.now()
    }
    return lead

def generate_proposal(project):
    prompt = f"""You are a professional freelancer.
Create a short, personalized proposal for this project:

Title: {project['title']}
Description: {project['description']}
Budget: ${project['budget']}

Highlight relevant skills, suggest a fair price, and make it human-sounding.
"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating proposal: {e}"

def score_lead(project):
    score = project['budget'] / 100
    for kw in keywords:
        if kw.lower() in project['description'].lower():
            score += 5
    days_old = (datetime.now() - project['date_posted']).days
    score += max(0, 5 - days_old)
    return score

# ---- STREAMLIT DASHBOARD ----
st.title("AI-Powered Real-Time Lead Dashboard")

if 'df_leads' not in st.session_state:
    st.session_state.df_leads = pd.DataFrame(columns=['title', 'description', 'budget', 'client', 'date_posted', 'proposal', 'score', 'follow_up'])

new_lead = generate_new_lead()
new_lead['proposal'] = generate_proposal(new_lead)
new_lead['score'] = score_lead(new_lead)
new_lead['follow_up'] = "Send Proposal" if new_lead['score'] > 7 else "Review Later"

st.session_state.df_leads = pd.concat([st.session_state.df_leads, pd.DataFrame([new_lead])], ignore_index=True)
st.session_state.df_leads = st.session_state.df_leads.sort_values(by='score', ascending=False)

st.subheader("All Leads")
st.dataframe(st.session_state.df_leads[['title', 'client', 'budget', 'score', 'follow_up', 'proposal']])

st.subheader("Top Lead")
top_lead = st.session_state.df_leads.iloc[0]
st.write(f"Title: {top_lead['title']}")
st.write(f"Client: {top_lead['client']}")
st.write(f"Score: {top_lead['score']}")
st.write("Proposal:")
st.text(top_lead['proposal'])

st.experimental_rerun()
