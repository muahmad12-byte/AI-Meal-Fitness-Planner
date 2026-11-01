import os
import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI Meal & Fitness Planner", page_icon="🥗")

# Read the API key from Streamlit secrets (cloud) or environment (Colab)
try:
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    api_key = os.environ.get("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY is missing. Add it in Settings → Secrets.")
    st.stop()

client = Groq(api_key=api_key)
MODEL = "llama-3.3-70b-versatile"  # update if Groq retires it

ACTIVITY = {"Sedentary": 1.2, "Light": 1.375, "Moderate": 1.55, "Very active": 1.725}


def calc_calories(age, gender, height, weight, activity, goal):
    # Mifflin-St Jeor equation
    bmr = 10 * weight + 6.25 * height - 5 * age + (5 if gender == "Male" else -161)
    tdee = bmr * ACTIVITY[activity]
    if goal == "Lose fat":
        target = tdee - 450
    elif goal == "Build muscle":
        target = tdee + 300
    else:
        target = tdee
    target = max(target, 1500 if gender == "Male" else 1200)  # safety floor
    return round(tdee), round(target)


st.title("🥗 AI Meal & Fitness Planner")
st.caption("Get a personalized 7-day meal and workout plan.")

age = st.number_input("Age", 18, 80, 22)
gender = st.radio("Gender", ["Male", "Female"], horizontal=True)
height = st.number_input("Height (cm)", 120, 220, 170)
weight = st.number_input("Weight (kg)", 35, 200, 70)
activity = st.selectbox("Activity level", list(ACTIVITY.keys()))
goal = st.selectbox("Goal", ["Lose fat", "Build muscle", "Maintain weight"])
diet = st.selectbox("Diet", ["Non-vegetarian", "Vegetarian", "Vegan"])
budget = st.selectbox("Budget", ["Low", "Medium", "High"])
allergies = st.text_input("Allergies (optional)")

if st.button("Generate Plan 🚀"):
    tdee, target = calc_calories(age, gender, height, weight, activity, goal)
    col1, col2 = st.columns(2)
    col1.metric("Maintenance calories", f"{tdee} kcal")
    col2.metric("Daily target", f"{target} kcal")

    prompt = f"""Create a 7-day meal plan and workout plan.
Goal: {goal}. Diet: {diet}. Budget: {budget}. Allergies: {allergies or 'none'}.
Daily calorie target: {target} kcal. Pakistani/South Asian food preferred.
For each day (Monday to Sunday) give Breakfast, Lunch, Snack, Dinner with approximate calories,
plus a simple workout (rest days allowed). End with a grocery list.
Use markdown headings and keep it practical. No extreme dieting advice."""

    with st.spinner("Cooking up your plan..."):
        try:
            res = client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
            )
            plan = res.choices[0].message.content
            st.markdown(plan)
            st.download_button("⬇️ Download plan", plan, file_name="plan.md")
        except Exception as e:
            st.error(f"Error: {e}")

st.caption("⚠️ General guidance only, not medical advice. Consult a doctor or dietitian before changing your diet.")
