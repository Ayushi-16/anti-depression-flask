import flask
import pickle
import json
import pandas as pd
import numpy as np
from flask_cors import CORS, cross_origin


app = flask.Flask(__name__)
cors = CORS(app, resources={r"/recommedsong": {"origins": "*"}})

@app.route('/recommedsong', methods=['POST','GET'])
@cross_origin()
def main1():
    body = flask.request.get_json()
    genre= body['genre']
    data = pickle.load(open('bin/song_list.pkl','rb'))
    cosine_sim = pickle.load(open('bin/cosine_sim_song.pkl','rb'))
    indices = pd.Series(data.index, index=data['genre'])
    idx=indices[genre]
    sim_scores=list(enumerate(cosine_sim[idx]))
    sim_scores=list(np.argsort(sim_scores[0][1]))
    sim_scores.reverse()
    top_similar=sim_scores[0:11]            
    song_idx=[i for i in top_similar]
    ans=data[['title','singer']].iloc[song_idx].sample(n=10)

    # flask.response.headers.add('Access-Control-Allow-Origin', '*')
    return ans.to_json(orient = 'records')

cors = CORS(app, resources={r"/recommedbook": {"origins": "*"}})    
@app.route('/recommedbook', methods=['POST','GET'])
@cross_origin()
def main2():
    body = flask.request.get_json()
    genre= body['genre']
    data = pickle.load(open('bin/book_list.pkl','rb'))
    cosine_sim = pickle.load(open('bin/cosine_sim_book.pkl','rb'))
    indices = pd.Series(data.index, index=data['genre'])
    idx=indices[genre]
    sim_scores=list(enumerate(cosine_sim[idx]))
    sim_scores=list(np.argsort(sim_scores[0][1]))
    sim_scores.reverse()
    top_similar=sim_scores[0:11]
    song_idx=[i for i in top_similar]
    ans=data[['title','author']].iloc[song_idx].sample(n=10)
    return ans.to_json(orient = 'records')

cors = CORS(app, resources={r"/recommedmovie": {"origins": "*"}})
@app.route('/recommedmovie', methods=['POST','GET'])
def main3():
    body = flask.request.get_json()
    genre= body['genre']
    data = pickle.load(open('bin/movie_list.pkl','rb'))
    cosine_sim = pickle.load(open('bin/cosine_sim_movie.pkl','rb'))
    indices = pd.Series(data.index, index=data['genre'])
    idx=indices[genre]
    sim_scores=list(enumerate(cosine_sim[idx]))
    sim_scores=list(np.argsort(sim_scores[0][1]))
    sim_scores.reverse()
    top_similar=sim_scores[0:11]
    song_idx=[i for i in top_similar]
    ans=data[['title']].iloc[song_idx].sample(n=10)
    return ans.to_json(orient = 'records')

if __name__ == '__main__':
    app.run()