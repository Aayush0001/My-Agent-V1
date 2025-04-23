import requests
from bs4 import BeautifulSoup
import openai
import os

# ✅ OpenAI API Key set from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY") or "YOUR_OPENAI_API_KEY"

def search_company_pages(role):
    query = f"site:linkedin.com/company/ {role} companies"
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    links = []
    for a in soup.find_all('a'):
        href = a.get('href')
        if 'linkedin.com/company' in href:
            links.append(href.split('&')[0].replace('/url?q=', ''))
    return list(set(links))[:5]  # Top 5 unique company LinkedIn URLs

def scrape_candidates_from_page(company_url, role):
    # ✅ Dummy data for now (we'll replace this with real scraping later)
    dummy_employees = [
        "Aman Sharma - Java Developer",
        "Priya Singh - Senior Java Developer",
        "Ravi Verma - Frontend Developer",
        "Neha Kapoor - Java Engineer",
        "Kunal Mehta - Backend Developer",
    ]
    print(f"✅ Scraping employees from {company_url}")
    return dummy_employees

def ask_gpt_to_filter(candidates, role):
    prompt = f"""
    You are an AI recruiter. Out of the following LinkedIn candidate list, pick those who match the role '{role}'. Return their names and job titles in bullet points.

    Candidates:
    {candidates}
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an AI assistant helping shortlist candidates."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=500
    )
    return response.choices[0].message["content"].strip()

def source_candidates(role):
    print(f"🔍 Searching companies for {role}...")
    company_pages = search_company_pages(role)
    all_candidates = []

    for company_url in company_pages:
        candidates = scrape_candidates_from_page(company_url, role)
        all_candidates.extend(candidates)

    print("🧠 Sending candidates to GPT for shortlisting...")
    short_list = ask_gpt_to_filter("\n".join(all_candidates), role)
    return short_list
