from flask import Flask, jsonify, request, Response, render_template
import requests

app = Flask(__name__)

#YOUTUBE_API_KEY = 'AIzaSyBFxdpFX61mnqtjBg1QQWaL09nti6ytGH8'
#YOUTUBE_API_KEY = 'AIzaSyD2K6OooNWMPgEWlkAkgAIRctksFyKk1vY'

MANIFEST = {
        "id": "com.youtube.pro",
        "version": "1.0.0",
        "name": "YouTube PRO",
        "description": "Addon for YouTube search and sequential playback",
        "logo": "https://i.imgur.com/jZUH5eP.png",
        "resources": ["catalog", "meta", "stream"],
        "types": ["series"],
        "catalogs": [{
            "type": "series",
            "id": "youtubepro",
            "name": "YouTube PRO",
            "extra": [{"name": "search", "isRequired": True}]
        }]
    }

def respond_with(data):
    resp = jsonify(data)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    resp.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return resp

@app.route('/')
def home():
    name = MANIFEST['name']
    types = MANIFEST['types']
    logo = MANIFEST['logo']
    description = MANIFEST['description']
    version = MANIFEST['version']
    return render_template('index.html', name=name, types=types, logo=logo, description=description, version=version)

@app.route('/logo')
def proxy_logo():
    image_url = request.args.get('url')

    if not image_url:
        return "Erro: Nenhuma URL fornecida", 400

    try:
        response = requests.get(image_url, stream=True)

        if response.status_code != 200:
            return f"Erro ao buscar a imagem: {response.status_code}", 400

        content_type = response.headers.get('Content-Type', 'image/jpeg')

        # Criar a resposta e adicionar os headers CORS manualmente
        resp = Response(response.content, content_type=content_type)
        resp.headers['Access-Control-Allow-Origin'] = '*'  # Permite acesso de qualquer origem
        resp.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'  # Métodos permitidos
        resp.headers['Access-Control-Allow-Headers'] = 'Content-Type'  # Permite cabeçalhos específicos

        return resp

    except requests.exceptions.RequestException as e:
        return f"Erro ao buscar a imagem: {str(e)}", 500

@app.route('/manifest.json')
def manifest():
    return respond_with(MANIFEST)

@app.route('/catalog/series/youtubepro/search=<query>.json', methods=['GET'])
def catalog(query):
    # host = request.host
    # if 'localhost' in host or '127.0.0.1' in host:
    #     server = f'http://{host}/logo?url='
    # else:
    #     server = f'https://{host}/logo?url='  
    return respond_with({
        "metas": [{
            "type": "series",
            "id": f"ytsearch:{query}",
            "name": f"YouTube PRO: '{query}'",
            "poster": "https://i.imgur.com/jZUH5eP.png"
        }]
    })

@app.route('/meta/series/<id>.json', methods=['GET'])
def meta(id):
    meta_id = id
    
    if meta_id.startswith("ytsearch:"):
        query = meta_id.split(":")[1]
        results = youtube_search(query)
        
        videos = []
        for idx, video in enumerate(results['items']):
            videos.append({
                "id": f"ytvideo:{video['id']['videoId']}:{query}:{idx}",
                "type": "episode",
                "name": video['snippet']['title'],
                "thumbnail": f"https://i.ytimg.com/vi/{video['id']['videoId']}/hqdefault.jpg",
                "season": 1,
                "episode": idx + 1
            })
        
        return respond_with({
            "meta": {
                "id": meta_id,
                "type": "series",
                "name": f"YouTube PRO: '{query}'",
                "videos": videos
            }
        })
    
    return respond_with({"meta": {}})

@app.route('/stream/series/<id>.json', methods=['GET'])
def stream(id):
    video_id = id
    parts = video_id.split(":")
    if parts[0] == "ytvideo":
        yt_id = parts[1]
        query = parts[2]
        index = int(parts[3])

        next_index = index + 1
        next_video_id = get_next_video_id(query, next_index)
        
        # streams = [{
        #     "name": 'Youtube PRO',
        #     "ytId": yt_id,
        #     "behaviorHints": {
        #         "nextVideo": next_video_id
        #     }
        # }] 
        streams = [{
            "name": 'Youtube PRO',
            "description": "Youtube",
            "ytId": yt_id
        }]                  
        
        return respond_with({"streams": streams})
    
    return jsonify({"streams": []})

def youtube_search(query):
    KEY = 'AIzaSyD2K6OooNWMPgEWlkAkgAIRctksFyKk1vY'
    KEY2 = 'AIzaSyBJ3ntReiv0L19H2RoYW62LpRdIuyPhIpw'
    KEY3 = 'AIzaSyDGhx1DtIgDl5ITSm0xfmqPAAHSAlI2KeU'
    KEY4 = 'AIzaSyAJk1xUI72YYfBMgEc84gjHUX-k2AN6-B0'
    KEY5 = 'AIzaSyAoFblDoXcc9f96-JUgCOshYFBJAwoEU24'
    KEY6 = 'AIzaSyB1OOSpTREs85WUMvIgJvLTZKye4BVsoFU'
    KEY7 = 'AIzaSyBkR-hDZZn-YnmV3RBWwXJ6zLaA2yhNAqU'
    KEY8 = 'AIzaSyAG3GyDRMSgc__9YKM37DNDzi0og_Koz1Q'
    KEY9 = 'AIzaSyBqE8OMbdKd-7NOT_LBvkgATb8huk3sPHI'
    KEY10 = 'AIzaSyBljuu-8XWjq3x1g_dCGxSyWFk29FzbvnY'
    KEY11 = 'AIzaSyBML3uOUyQhOshc796-ouC-mamnNJhbZxs'
    KEY12 = 'AIzaSyDfFr3mb1R0EhvZ8MfbvYH4jC7QWh8658A'
    KEY13 = 'AIzaSyCcGHW1aj_8BRTLe8CHeMhLprnSamzx7Oo'
    
    try:
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=50&q={query}&type=video&key={KEY}"
        response = requests.get(url)
        response.raise_for_status()
    except:
        try:
            url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=50&q={query}&type=video&key={KEY2}"
            response = requests.get(url) 
            response.raise_for_status() 
        except:
            try:
                url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=50&q={query}&type=video&key={KEY3}"
                response = requests.get(url) 
                response.raise_for_status() 
            except:
                try:
                    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=50&q={query}&type=video&key={KEY4}"
                    response = requests.get(url) 
                    response.raise_for_status() 
                except:
                    try:
                        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=50&q={query}&type=video&key={KEY5}"
                        response = requests.get(url) 
                        response.raise_for_status() 
                    except:
                        try:
                            url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=50&q={query}&type=video&key={KEY6}"
                            response = requests.get(url) 
                            response.raise_for_status() 
                        except:
                            try:
                                url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=50&q={query}&type=video&key={KEY7}"
                                response = requests.get(url) 
                                response.raise_for_status() 
                            except:
                                try:
                                    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=50&q={query}&type=video&key={KEY8}"
                                    response = requests.get(url) 
                                    response.raise_for_status() 
                                except:
                                    try:
                                        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=50&q={query}&type=video&key={KEY9}"
                                        response = requests.get(url) 
                                        response.raise_for_status() 
                                    except:
                                        try:
                                            url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=50&q={query}&type=video&key={KEY10}"
                                            response = requests.get(url) 
                                            response.raise_for_status() 
                                        except:
                                            try:
                                                url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=50&q={query}&type=video&key={KEY11}"
                                                response = requests.get(url) 
                                                response.raise_for_status() 
                                            except:
                                                try:
                                                    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=50&q={query}&type=video&key={KEY12}"
                                                    response = requests.get(url) 
                                                    response.raise_for_status() 
                                                except:
                                                    try:
                                                        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=50&q={query}&type=video&key={KEY13}"
                                                        response = requests.get(url) 
                                                        response.raise_for_status() 
                                                    except:
                                                        pass
    try:
        return response.json()
    except:
        return {}                              


def get_next_video_id(query, index):
    results = youtube_search(query)
    if index < len(results['items']):
        return f"ytvideo:{results['items'][index]['id']['videoId']}:{query}:{index}"
    return None

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)