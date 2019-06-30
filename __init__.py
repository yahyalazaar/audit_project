#! /usr/bin/python3
# -*- coding:utf-8 -*-

from flask import Flask, request, render_template, redirect
import json
import os


app = Flask(__name__)



@app.route('/')
def accueil():  
    if os.path.exists("db")==False:
        os.mkdir("db")
    return render_template('index.html')


@app.route('/formule')
def reponse():
    list_qst = []
    if os.path.exists("db/questions.json") == True:
        file = open("db/questions.json", "r")
        list_qst = json.load(file)
        file.close()
    list_tache = []
    if os.path.exists("db/taches.json") == True:
        file = open("db/taches.json", "r")
        list_tache = json.load(file)
        file.close()
    return render_template('formule.html', list_qst=list_qst, list_tache=list_tache)


@app.route('/questions', methods=['POST', 'GET'])
def questions():
    list_qst = []
    if os.path.exists("db/questions.json") == True:
        file = open("db/questions.json", "r")
        list_qst = json.load(file)
        file.close()
    list_tache = []
    if os.path.exists("db/taches.json") == True:
        file = open("db/taches.json", "r")
        list_tache = json.load(file)
        file.close()

    if request.method == 'POST':
        qst = request.form['qst']
        tache = request.form['tache']
        i = 0
        for t in list_tache:
            if str(t['id']) == str(tache):
                tache = list_tache[i]
                break
            i = i+1

        file = open("db/questions.json", "w")
        txt = {
            "id": len(list_qst),
            "question": qst,
            "tache": tache
        }
        list_qst.append(txt)
        file.write(json.dumps(list_qst, indent=True))
        file.close()

    return render_template('questions.html', list_qst=list_qst, list_tache=list_tache)


@app.route('/update_qst', methods=['POST', 'GET'])
def update_qst():
    list_qst = []
    if os.path.exists("db/questions.json") == True:
        file = open("db/questions.json", "r")
        list_qst = json.load(file)
        file.close()
    list_tache = []
    if os.path.exists("db/taches.json") == True:
        file = open("db/taches.json", "r")
        list_tache = json.load(file)
        file.close()
    if request.method == 'POST':
        id = request.form['id']
        qst = request.form['qst']
        tache = request.form['tache']
        i = 0
        for t in list_tache:
            if str(t['id']) == str(tache):
                tache = list_tache[i]
                break
            i = i+1
        i = 0
        for q in list_qst:
            if str(q['id']) == str(id):
                list_qst[i]['question'] = qst
                list_qst[i]['tache'] = tache
                break
            i = i+1
        file = open("db/questions.json", "w")
        file.write(json.dumps(list_qst, indent=True))
        file.close()
    return redirect('/questions')


@app.route('/taches', methods=['POST', 'GET'])
def taches():
    list_tache = []
    if os.path.exists("db/taches.json") == True:
        file = open("db/taches.json", "r")
        list_tache = json.load(file)
        file.close()
    if request.method == 'POST':
        tache = request.form['tache']
        file = open("db/taches.json", "w")
        txt = {
            "id": len(list_tache),
            "tache": tache
        }
        list_tache.append(txt)
        file.write(json.dumps(list_tache, indent=True))
        file.close()

    return render_template('taches.html', list_tache=list_tache)


@app.route('/update_tache', methods=['POST', 'GET'])
def update_tache():
    list_tache = []
    if os.path.exists("db/taches.json") == True:
        file = open("db/taches.json", "r")
        list_tache = json.load(file)
        file.close()
    if request.method == 'POST':
        id = request.form['id']
        tache = request.form['tache']
        i = 0
        for t in list_tache:
            if str(t['id']) == str(id):
                list_tache[i]['tache'] = tache
                break
            i = i+1
        file = open("db/taches.json", "w")
        file.write(json.dumps(list_tache, indent=True))
        file.close()
        up_qst()
    return redirect('/taches')


def up_qst():
    list_qst = []
    if os.path.exists("db/questions.json") == True:
        file = open("db/questions.json", "r")
        list_qst = json.load(file)
        file.close()
    list_tache = []
    if os.path.exists("db/taches.json") == True:
        file = open("db/taches.json", "r")
        list_tache = json.load(file)
        file.close()
    i = 0
    for q in list_qst:
        for t in list_tache:
            if str(t['id']) == str(q['id']):
                list_qst[i]['tache'] = t
        i = i+1
    file = open("db/questions.json", "w")
    file.write(json.dumps(list_qst, indent=True))
    file.close()


@app.route('/add_reponse', methods=['POST', 'GET'])
def add_reponse():
    list_qst = []
    if os.path.exists("db/questions.json") == True:
        file = open("db/questions.json", "r")
        list_qst = json.load(file)
        file.close()
    list_tache = []
    if os.path.exists("db/taches.json") == True:
        file = open("db/taches.json", "r")
        list_tache = json.load(file)
        file.close()
    list_reponse = []
    if os.path.exists("db/reponses.json") == True:
        file = open("db/reponses.json", "r")
        list_reponse = json.load(file)
        file.close()
    if request.method == 'POST':
        resp = {}
        resp['nom'] = request.form['nom']
        resp['prenom'] = request.form['prenom']
        nom = str(request.form['nom']).upper()+" " + \
            str(request.form['prenom']).upper()
        resp['sexe'] = request.form['sexe']
        resp['profession'] = request.form['profession']
        for t in list_tache:
            for q in list_qst:
                if str(t['id']) == str(q['tache']['id']):
                    resp['question_'+str(q['id'])] = q
                    tmp = 'resp'+str(q['id'])
                    resp['reponse_'+str(q['id'])] = request.form[tmp]
                    tmp = 'justif'+str(q['id'])
                    resp['justification_'+str(q['id'])] = request.form[tmp]
        list_reponse.append(resp)
        file = open("db/reponses.json", "w")
        file.write(json.dumps(list_reponse, indent=True))
        file.close()
        return redirect('/success/'+nom)
    else:
        return redirect('/formule')


@app.route('/success/<nom>')
def success(nom):
    return render_template('success.html', nom=nom)

@app.route('/getData', methods=['POST', 'GET'])
def chart():
    res=[]
    if request.method == 'POST':
        list_reponse = []
        if os.path.exists("db/reponses.json") == True:
            file = open("db/reponses.json", "r")
            list_reponse = json.load(file)
            file.close()
        list_qst = []
        if os.path.exists("db/questions.json") == True:
            file = open("db/questions.json", "r")
            list_qst = json.load(file)
            file.close()
        list_tache = []
        if os.path.exists("db/taches.json") == True:
            file = open("db/taches.json", "r")
            list_tache = json.load(file)
            file.close()
        for t in list_tache:
            out = {}
            out['tache'] = t['tache']
            out['non'] = 0
            out['oui'] = 0
            for q in list_qst:
                if str(q['tache']['id']) == str(t['id']):
                    id = str(q['id'])
                    for r in list_reponse:
                        if str(r['reponse_'+id]).lower() == "non":
                            out['non'] = out['non']+1
                        elif str(r['reponse_'+id]).lower() == "oui":
                            out['oui'] = out['oui']+1
            res.append(out)
    return json.dumps(res)

if __name__ == '__main__':
    app.run(debug=True)
