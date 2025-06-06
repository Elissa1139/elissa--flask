from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests
import ollama
from flask_cors import CORS
from datetime import datetime



app = Flask(__name__)

OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama2"  # Change if using another model (mistral)

chat_history = [
    {
        "role": "system",
        "content": 
             "You are an assistant for a specific website. " +
             "You must ONLY answer questions based on the provided website content. " +
            f"Here is information about the website named 'Growing Up', where you get information about your daily needs such as opening bank accounts from a popular banks like DBS, OCBC, UOB. Get details on insurance, survival skills, baking recipes, cooking videos. Finally you can get to quiz based on the learnings you did on this website to test whether you learnt well. Additionally, you can  also get info into playing Baking adventure game, learn about cooking brownies, shortcake, mochi, salted dark chocolate and pudding."
        
    }
]

user_data = [
    {
        "user_id": "user1",
        "password": "abc",
        "name": "Elissa",
        "completed":[],
        "score": 0
    }
]

current_user="Elissa"

@app.route('/')
def home():
    return render_template('login.html')

today = datetime.today().strftime('%d/%m/%Y')  # Format date as 31/02/2025

@app.route('/login.html', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        for user in user_data:
            if user["user_id"] == username and user["password"] == password:
                print(user)
                global current_user
                current_user = user['name']
                for i in range(len(user_data)):
                    if user_data[i]["user_id"] == username:
                        print(user_data[i]["completed"])
                        module1 = "accountopening" in user_data[i]["completed"]
                        module1 = "insurance" in user_data[i]["completed"]
                        module2 = "fire" in user_data[i]["completed"]
                        module3 = "bakinggame" in user_data[i]["completed"]
                        module3 = "recipe" in user_data[i]["completed"]
                        module4 = "cuisine" in user_data[i]["completed"]
                        module5 = "music" in user_data[i]["completed"]
                        module6 = "quiz" in user_data[i]["completed"]
                        break
                return render_template("index.html", today_date=today, module1_completed=module1, module2_completed=module2, module3_completed=module3, module4_completed=module4, module5_completed=module5, module6_completed=module6)
        
        return render_template('login.html', passwordWrongText="Invalid username or password. Please try again.")
    else:
        return render_template('login.html')

@app.route('/register.html', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        USERNAME = request.form['username']
        PASSWORD = request.form['password']
        NAME = request.form['name']
        
        # Add the new user to user_data
        user_data.append({
            "user_id": USERNAME,
            "password": PASSWORD,
            "name": NAME,
            "completed": []
        })
        
        today = datetime.today().strftime('%d/%m/%Y')  # Format date as 31/02/2025
        return redirect("login.html")
        

    return render_template('register.html')

@app.route('/logout.html')
def index_page():
    current_user = None
    return redirect('login.html')

@app.route('/error')
def error_page():
    return render_template('error.html')

@app.route('/Finance.html')
def finance_page():
    completed_topics = ["accountopening", "insurance"]
    answer = False
    for user in user_data:
        if user["name"] == current_user:
            answer = all(topic in user["completed"] for topic in completed_topics)
            break
    if( answer):
        return render_template('Finance.html', completed="COMPLETED", today_date=today, student=current_user) 
    return render_template('Finance.html', completed="INCOMPLETE", today_date=today, student=current_user)       

@app.route('/accountopening.html')
def accountopening_page():
    for(i, user) in enumerate(user_data):
        if user["name"] == current_user:
            user["completed"].append("accountopening")
            break
    return render_template('accountopening.html')

@app.route('/insurance.html')
def insurance_page():
    for(i, user) in enumerate(user_data):
        if user["name"] == current_user:
            user["completed"].append("insurance")
            break
    return render_template('insurance.html')


@app.route('/Survivalskills.html')
def Survivalskills_page():
    completed_topics = ["fire"]
    answer = False
    for user in user_data:
        if user["name"] == current_user:
            answer = all(topic in user["completed"] for topic in completed_topics)
            break
    if( answer):
        return render_template('Survivalskills.html', completed="COMPLETED", today_date=today, student=current_user)
    return render_template('Survivalskills.html', completed="INCOMPLETE", today_date=today, student=current_user)


@app.route('/fire.html')
def fire_page():
    for(i, user) in enumerate(user_data):
        if user["name"] == current_user:
            user["completed"].append("fire")
            break   
    return render_template('fire.html')

@app.route('/cooking.html')
def cooking_page():
    completed_topics = ["bakinggame", "recipe"]
    for user in user_data:
        if user["name"] == current_user:
            answer = all(topic in user["completed"] for topic in completed_topics)
            break
    if( answer):
        return render_template('cooking.html', completed="COMPLETED", today_date=today, student=current_user)       
    return render_template('cooking.html', completed="INCOMPLETE", today_date=today, student=current_user)

@app.route('/cuisine.html')
def cuisine_page():
    for(i, user) in enumerate(user_data):
        if user["name"] == current_user:
            user["completed"].append("cuisine")
            break
    return render_template('cuisine.html')

@app.route('/recipe.html')
def recipe_page():
    for(i, user) in enumerate(user_data):
        if user["name"] == current_user:
            user["completed"].append("recipe")
            break   
    return render_template('recipe.html')


@app.route('/chocolate.html')
def chocolate_page():
    return render_template('recipes/chocolate.html')

@app.route('/mochi.html')
def mochi_page():
    return render_template('recipes/mochi.html')

@app.route('/quiz_home.html', methods=['GET', 'POST'])
def quiz_home():
    answer = False
    completed_topics = ["quiz"]
    for user in user_data:
        if user["name"] == current_user:
            answer = all(topic in user["completed"] for topic in completed_topics)
            break
    if(answer):
        return render_template('quiz_home.html', completed="COMPLETED", today_date=today, student=current_user, result="")       
    return render_template('quiz_home.html', completed="INCOMPLETE", today_date=today, student=current_user, result="Not Attempted")

@app.route('/quiztime.html', methods=['GET', 'POST'])
def quiztime_page():
    
    score = 0
    result = "Yet to be attempted"
    if request.method == 'POST':
        q1 = request.form['q1']
        q2 = request.form['q2']
        q3 = request.form['q3']
        q4 = request.form['q4']
        q5 = request.form['q5']
        if q1 == 'a':
            score += 1
        if q2 == 'c':
            score += 1
        if q3 == 'b':
            score += 1
        if q4 == 'b':
            score += 1
        if q5 == 'a':
            score += 1
        
        for(i, user) in enumerate(user_data):
            if user["name"] == current_user:
                user["completed"].append("quiz")
                user["score"] = score
                break   
        if score < 5:
            result = f"Your score is {score}/5. Please try harder."
        else:
            result = f"Your score is {score}/5. Well done!"
        return render_template('quiz_home.html', completed="COMPLETED", today_date=today, student=current_user, result=result)       

    return render_template('quiztime.html')

@app.route('/shortcake.html')
def shortcake_page():
    return render_template('recipes/shortcake.html')

@app.route('/pudding.html')
def pudding_page():
    return render_template('recipes/pudding.html')

@app.route('/salted-cookies.html')
def salted_page():
    return render_template('recipes/salted-cookies.html')

@app.route('/music.html')
def music_page():
    for(i, user) in enumerate(user_data):
        if user["name"] == current_user:
            user["completed"].append("music")
            break
    return render_template('music.html')

@app.route('/bakinggame.html')
def Bakinggame_page():
    for(i, user) in enumerate(user_data):
        if user["name"] == current_user:
            user["completed"].append("bakinggame")
            break

    return render_template('bakinggame.html')


@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message", "")
    chat_history.append({"role": "user", "content": user_input})

    response = ollama.chat(
        model='llama2',
        messages=chat_history
    )

    answer = response['message']['content']
    chat_history.append({"role": "assistant", "content": answer})
    return jsonify({"response": answer})


@app.route('/chat-global', methods=['POST'])
def chat_global():
    user_input = request.json.get("message", "")

    response = ollama.chat(
        model='llama2',
        messages=[{"role": "user", "content": user_input}]
    )

    answer = response['message']['content']
    return jsonify({"response": answer})


if __name__ == '__main__':
    app.run(debug=True)


# with open("templates/index.html", "w") as f:
#     f.write(html_content)
