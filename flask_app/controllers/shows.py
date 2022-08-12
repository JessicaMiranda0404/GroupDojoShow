from flask import render_template,redirect,session,request, flash, url_for
from flask_app import app
from flask_app.models.show import Show


@app.route('/addshow')
def addshow():
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template('showcreation.html')


@app.route('/createshow', methods=['POST'])
def createshow():
    if 'user_id' not in session:
        return redirect('/logout')
    show = Show.get_all()
    for s in show:
        if s.title == request.form['title']:
            flash("Show is already on your list","show")
            return redirect('/addshow')
    if not Show.validate_show(request.form):
        return redirect('/addshow')
    data={
        'title':request.form['title'],
        'description' : request.form['description'],
        'user_id' : session['user_id']
    }
    Show.save(data)
    return redirect ('/dashboard')

@app.route('/deleteshow/<int:id>')
def deleteshow(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data={
        'id':id
    }
    Show.delete(data)
    return redirect('/dashboard')

@app.route('/viewshow/<int:id>')
def viewshow(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data={
        'id':id
    }
    return render_template('viewshow.html', show=Show.get_by_id(data))

@app.route('/editshow/<int:id>')
def editshow(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data={
        'id':id
    }
    return render_template('editshow.html', show=Show.get_by_id(data))

@app.route('/updateshow/<int:id>', methods=['POST'])
def updateshow(id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not Show.validate_show(request.form):
        return redirect(url_for('editshow', id=id))
    data={
        'id': id,
        'title':request.form['title'],
        'description' : request.form['description']
    }
    Show.update(data)
    return redirect ('/dashboard')