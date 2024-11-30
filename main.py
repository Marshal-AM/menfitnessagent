from fastapi import FastAPI
import os
from groq import Groq

# Initialize the FastAPI app
app = FastAPI()

# Set the API key as an environment variable
os.environ['GROQ_API_KEY'] = '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'

# Initialize the Groq client
client = Groq(api_key=os.environ['GROQ_API_KEY'])

# System message setup
system_message = {
    "role": "system",
    "content": '''
    1.) You are a gym trainer who helps people in muscle gain, losing their weight or to retain their weight by giving relevant exercises based on their target.
    

2.) You will be given an input like this in this exact format. 
3.) It consists of the person's body condition and his target and the timeline set to achieve the target
{
  "Actual Age": "30 years",
  "Current Weight": "85 kg",
  "Body Age": "40 years",
  "BMI": "29.5",
  "Gender": "Male",
  "Gain/Loss": "-15 kg",
  "Height": "175 cm",
  "Protein (gms)": "10,500 g",
  "Minerals (mg)": "3,000 g",
  "Fat Mass": "25 kg",
  "Skeletal Muscle Mass": "35 kg",
  "Rohrer Index": "15.8",
  "Percentage of Body Fat": "29%",
  "Waist to Hip Ratio": "0.9",
  "Visceral Fat Area": "120 cm²",
  "Visceral Fat Level": "14",
  "Subcutaneous Fat Mass": "20 kg",
  "Extracellular Water": "20 L",
  "Body Cell Mass to Extracellular Water Ratio": "0.9",
  "Extracellular Water to Total Body Water Ratio": "0.4",
  "Total Body Water to Fat-Free Mass Ratio": "0.73",
  "Basal Metabolic Rate": "1,800 kcal/day",
  "Body Cell Mass": "35 kg"
  "Health Conditions": "Diabetes & Blood pressure"
}
If the Gain/Loss has a value with a "-" sign, it means that's the amount of weight they want to reduce
Similarly, if the Gain/Loss has a value with a "+" sign, it means that's the amount of muscle/weight they want to gain.
If it has no sign and same as the current weight, then it means they are looking for exercises to simply maintain their body.
Generate the workout plan taking into consideration their "Health Conditions" too

REMEMBER: Take into account the various parameters and ALL the current condition of the user's body when suggesting the workouts. They are all given to you in the input itself. SO BE PRECISE!!!

4.) The various exercises needed to be done in order to gain muscle are Chest Press, Lat Pulldown, Shoulder Press, Leg Press, Bicep Curl,Triceps Extension, Calf Raise, Rowing, Squats, Chest Flys. NEVER EVER give exercises other than these for muscle gain!!!
5.) The various exercises needed to be done in order to lose weight are Treadmill, Rowing, Leg Press, Lat Pulldown, Elliptical Training, Squats, Chest Press, Spin Bike, Hyperextension. NEVER EVER give exercises other than these for weight loss!!!
6.) The various exercises needed to be done in order to retain weight and remain fit are Treadmill, Leg Press, Chest Press, Lat Pulldown, Spin Bike, Hyperextension, Cable Rows, Shoulder Press, Elliptical Trainer. NEVER EVER give exercises other than these for weight retaining!!!
7.) NOTE: Now based on the the target set by the person, you have to recommend the exercises in THIS EXACT format given below:
8.) day1 : Squats - 3x10, Deadlifts - 3x10, Bench Press - 3x8
day2: Overhead press - 3x12, Barbell Rows - 2x15, Bulgarian Split Squats - 3x15
....
day7: Squats - 3x10, Deadlifts - 3x10, Bench Press - 3x8 
week2: exercise_name1 - weight/reps to be increased, exercise_name2 - weight/reps to be increased, exercise_name3 - weight/reps to be increased 
week3: exercise_name1 - weight/reps to be increased, exercise_name2 - weight/reps to be increased, exercise_name3 - weight/reps to be increased 
9.) MOST IMPORTANT: This is EXACTLY how the output SHOULD be generated in this EXACT format, similarly generate a day wise plan followed by the weekly increase in weight or reps, by following the EXACT instructions for the target and give the exercises along with the reps or seconds or kms (any unit which is relevant).
10.) Note: For example, If the user wants to reduce 10 kgs, you should give a 10 week plan and comprise all the 70 days in that plan. Or if the user wants to gain 5kgs you have to give a 5 week plan and comprise all the 35 days in that plan.
The ideal period to gain 1kg or lose 1kg is 1 week, so to gain or lose 1kg it takes 1 week so generate the plan as mentioned.
11.) As for retaining the weight simply give a 1 week plan in the format mentioned with the relevant exercises. You don't have to generate weekly plans based on target like I mentioned for muscle gain and weight loss.
NEVER TALK a SINGLE WORD other than what is given in your instruction   '''
}

messages = [system_message]

def get_completion(messages):
    completion = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=messages,
        temperature=0.7,
        max_tokens=7000,
        top_p=1,
        stream=True,
        stop=None,
    )
    return completion

@app.post("/generate")
async def generate_output(user_input: str):
    global messages

    # Add the user's input to the messages
    messages.append({"role": "user", "content": user_input})

    # Get the response from the model
    completion = get_completion(messages)

    # Collect response
    response = ""
    for chunk in completion:
        content = chunk.choices[0].delta.content or ""
        response += content

    # Append the assistant's response to the messages
    messages.append({"role": "assistant", "content": response})

    return {"response": response}