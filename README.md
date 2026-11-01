# 🥗 AI Meal & Fitness Planner

A web app that generates a personalized 7-day meal and workout plan using the Groq API (Llama 3.3).

## Features
- Calculates maintenance calories and a daily target using the Mifflin-St Jeor equation
- Adjusts for goal: lose fat, build muscle, or maintain weight
- Supports vegetarian, vegan, and non-vegetarian diets, budgets, and allergies
- 7-day meal plan, workouts, and grocery list
- Download the plan as a Markdown file

## Tech Stack
- Python
- Streamlit (user interface)
- Groq API with Llama 3.3 70B (plan generation)

## Run Locally
```bash
git clone https://github.com/YOUR_USERNAME/meal-fitness-planner.git
cd meal-fitness-planner
pip install -r requirements.txt
```

Create `.streamlit/secrets.toml`:
```toml
GROQ_API_KEY = "your_key_here"
```

Then run:
```bash
streamlit run app.py
```

## Deploy
Deployed on Streamlit Community Cloud. Add `GROQ_API_KEY` under App Settings → Secrets.

## Disclaimer
This app provides general guidance only and is not medical advice.# AI-Meal-Fitness-Planner
