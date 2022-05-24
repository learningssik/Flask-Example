from flask import Flask, request, redirect

app = Flask(__name__)

nextID = 4
topics = [
    {'id': 1, 'title': 'html', 'body': 'html is ...'},
    {'id': 2, 'title': 'css', 'body': 'css is ...'},
    {'id': 3, 'title': 'javascript', 'body': 'javascript is ...'}
]
def getContents():
    liTags = ''
    for topic in topics:
        liTags = liTags + f'<li><a href="/read/{topic["id"]}/">{topic["title"]}</a></li>'
    return liTags

def template(contents, content, id=None):
    contextUI=''
    if id != None:
        contextUI = f'''
            <li><a href="/update/{id}/">update</a></li>
            <li><form action="/delete/{id}/" method="POST"><input type="submit" value="delete"></form></li>
            
        '''

    return f'''<!doctype html>
    <html>
        <body>
            <h1><a href="/">WEB</a></h1>
            <ol>
                {contents}
            </ol>
            {content}
            <ul>
                <li><a href="/create/">create</a></li>
                {contextUI}
            </ul>
        </body>
    </html>
    '''


@app.route('/')
def index():

    return template(getContents(), '<h2>Welcome</h2>Hello, WEB')

@app.route('/create/', methods=['GET','POST'])
def create():
    global nextID

    if request.method == 'GET':

        content = '''
            <form action="/create/" method='POST'>
                <p><input type="text" name="title" placeholder="title"></p>
                <p><textarea name="body" placeholder="body"></textarea></p>
                <p><input type="submit" value="create"</p>
            </form>
        '''
        return template(getContents(), content)

    elif request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        newTopic = {'id': nextID, 'title':title, 'body' : body}
        topics.append(newTopic)

        url = '/read/'+str(nextID)
        nextID += 1

        return redirect(url)

@app.route('/update/<id>/', methods=['GET','POST'])
def update(id):
    global nextID

    if request.method == 'GET':

        for i in topics:
            if i['id'] == int(id):
                title = i['title']
                body = i['body']
                break

        content = f'''
            <form action="/update/{id}/" method='POST'>
                <p><input type="text" name="title" placeholder="title" value={title}></p>
                <p><textarea name="body" placeholder="body">{body}</textarea></p>
                <p><input type="submit" value="update"</p>
            </form>
        '''
        return template(getContents(), content)

    elif request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        for topic in topics:
            if int(id) == topic['id']:
                topic['title'] = title
                topic['body'] = body
                break

        url = '/read/'+str(id)
        return redirect(url)


@app.route('/delete/<id>/', methods=['POST'])
def delete(id):
    for topic in topics:
        if topic['id'] == int(id):
            topics.remove(topic)
            break
    return redirect('/')

@app.route('/read/<id>/')
def read(id):

    liTags = ''
    for topic in topics:
        liTags = liTags + f'<li><a href="/read/{topic["id"]}/">{topic["title"]}</a></li>'

    for i in topics:
        if i['id'] == int(id):
            title = i['title']
            body = i['body']

            return template(getContents(), f'<h2>{title}</h2>{body}', id)




app.run(debug=True)
