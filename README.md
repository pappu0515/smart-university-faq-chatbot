# UniAssist — Smart University FAQ Chatbot

Cloud-ready B.Tech AI project starter using Streamlit, Firebase Authentication, and Cloud Firestore.

## Features
- Modern responsive Streamlit interface
- Firebase email/password registration and login (requires configuration)
- FAQ keyword matching / lightweight NLP
- Reads FAQ documents from Cloud Firestore collection `faqs`
- Demo fallback FAQs for interface testing
- Designed for deployment to Streamlit Community Cloud

## Important
Sample FAQ responses are generic placeholders, not official university policies. Replace them with verified information before academic submission. Firebase Authentication and Firestore only work after real project credentials and security rules are configured. This starter does not claim that deployment has already happened.

## Firestore setup
Create a collection named `faqs`. Each document should contain:
- `question` (string)
- `answer` (string)
- `keywords` (array of strings)

Example document:
```json
{
  "question": "How can I apply for admission?",
  "answer": "Please check the official admissions page for current requirements and dates.",
  "keywords": ["admission", "apply", "application"]
}
```

## Firebase setup
1. Create a Firebase project.
2. Enable Authentication -> Email/Password.
3. Create Firestore Database.
4. Create a service account for server-side Firestore access, and keep its private key secret.
5. Copy `.streamlit/secrets.toml.example` values into Streamlit Community Cloud App Settings -> Secrets. Do not upload real secrets to GitHub.

## Deploy
1. Upload this folder to a GitHub repository.
2. In Streamlit Community Cloud, create an app from the repository and select `app.py`.
3. Add secrets in the app settings.
4. Deploy and test the public HTTPS URL.

## Cloud services used
- Streamlit Community Cloud: application hosting
- Firebase Authentication: user identity and login
- Cloud Firestore: cloud FAQ storage

## Academic integrity / safety
Use only verified university information. Never store passwords yourself; Firebase Authentication handles authentication. Restrict service-account permissions and keep credentials private.
