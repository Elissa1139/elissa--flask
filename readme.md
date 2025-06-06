# Growing Up


## Setup
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Once done, you can run the program
```
python app.py
```

Once the logs stops appearing, you can go to any browser 

```
http://127.0.0.1:5000/
```


## Python Code Changes and Explanation:

```
 completed_topics = ["accountopening", "insurance"]
    answer = False
    for user in user_data:
        if user["user_id"] == current_user:
            answer = all(topic in user["completed"] for topic in completed_topics)
            break
    if( answer):
        #print("All topics completed") #This line is for debugging.
        return render_template('Finance.html', completed="COMPLETED", today_date=today, student=current_user) 
    return render_template('Finance.html', completed="INCOMPLETE", today_date=today, student=current_user) 
```

This is an example of some of the code, used to track, what is completed, and allow to set "completed" when the logged in user has visited each page.

```
for(i, user) in enumerate(user_data):
        if user["user_id"] == current_user:
            user["completed"].append("topic")
            #print(user["completed"]) #This line is for debugging.
            break
```

This is an example of the code, where we set the value as true when the user click on the navigation to go to each page.

```
<div class="text-xl font-handwriting">{{today_date}}</div>
```

In the HTML, we use some of the following syntax to pass the data from python to html, to set dynamic data.

```
return render_template('Finance.html', completed="INCOMPLETE", today_date=today, student=current_user)
```

This is another example of Python code, to send more details to HTML via Python such as whether what is the state of the assignment, today's date, and the current logged in user.

```
user_data = [
    {
        "user_id": "user1",
        "password": "abc",
        "completed":[]
    }
]
```

The above depicts a database, where we can store the users we have logged in or registered. It will state all the saved components which the user has navigated through. 


```
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
    print(chat_history)
    return jsonify({"response": answer})
```

This is the entire code for interacting with ChatBot, the above passage is where we create a context for the AI Model to ensure it stays within the limited grounds of information. If you require you can change the content and see how it moves.



```
<link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
```

This is how we refer to external stlyesheet which are available in static folder. I have drafed 2 of those, one more login page and register page. Other for the rest of the pages. Each page can have their own styles or customised when and where needed. But this helps to organise across website theme.

```
<a onclick="onClickEnabled()" id="sharing-access" style="cursor: pointer;">DISABLED</a>
            <script>
              function onClickEnabled() {
              const sharingAccessElement = document.getElementById('sharing-access');
              if (sharingAccessElement.textContent === 'DISABLED') {
                sharingAccessElement.textContent = 'ENABLED';
              } else {
                sharingAccessElement.textContent = 'DISABLED';
              }
              }
            </script>
```

The above snippet is used across multiple HTML files, these are in-line scripts to help to do basic things such as Toggling of sharing status.