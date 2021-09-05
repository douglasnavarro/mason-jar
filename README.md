# Mason Jar API

Scrapes and returns lyrics and song data from vagalume.com.br

---

## Endpoints

### /api/\<artist>

Returns 15 top songs from artist, if that artis have top songs. Example:

`GET /api/ed-sheeran HTTP/1.1`

Produces a response with the following payload

```
{
   "artist":"ed-sheeran",
   "top_songs":{
      "1":"Perfect",
      "2":"Photograph",
      "3":"Shape Of You",
      "4":"Thinking Out Loud",
      "5":"...Baby One More Time",
      "6":"Happier",
      "7":"Perfect Duet (With Beyonc\u00c3\u00a9)",
      "8":"All Of The Stars",
      "9":"Addicted",
      "10":"Give Me Love",
      "11":"Afire Love",
      "12":"Castle On The Hill",
      "13":"Eraser",
      "14":"Tenerife Sea",
      "15":"Dive"
   }
}
```

- You can limit results using the **count** query param:

    `GET /api/ed-sheeran?count=3 HTTP/1.1`

    Produz um response com payload

```
{
   "artist":"ed-sheeran",
   "top_songs":{
      "1":"Perfect",
      "2":"Photograph",
      "3":"Shape Of You"
   }
}
```

- Params over 25 will be responded with 400, bad request.


### /api/<artist>/all

Returns all songs from artist. Example:

`GET /api/ed-sheeran/all HTTP/1.1`

Produces a response with the following payload

```
{
  "all_songs": [
    "...Baby One More Time", 
    "Addicted", 
    "Afire Love", 
    "All Of The Stars", 
    "Autumn Leaves", 
    "Barcelona", 
    "Be Like You", 
    "Be My Husband (Originally by Nina Simone)", 
    "Beyond the Pale", 
    "Bibia Be Ye Ye", 
    "Billy Ruskin", 
    "Bloodstream", 
    "Bloodstream (With Rudimental)",
    ...
    "You Need Me, I Don't Need You", 
    "You Need To Cut Your Hair"
  ], 
  "artist": "ed-sheeran"
}
```

### /api/\<artist>/\<first_letter>

Returns all songs from artist with a title that starts with <first_letter>. Example:

`GET /api/iron-maiden/d HTTP/1.1`

Produces a response with the following payload

```
{
  "artist": "iron-maiden",
  "songs": [
    "Dance Of Death",
    "Death or Glory",
    "Deja Vu",
    "Die With Your Boots On",
    "Different World",
    "Doctor Doctor",
    "Don't Look To The Eyes Of A Stranger",
    "Dream Of Mirrors",
    "Drifter"
  ]
}
```

### /api/\<artist>/lyrics/\<title>

Returns the lyrics for the song that has <title> and belongs to <artist>. Example:

`GET /api/ac-dc/lyrics/jailbreak HTTP/1.1`

```
{
  "artist": "ac-dc",
  "lyrics": "There was a friend of mine on murder\nAnd the judge's gavel fell\nJury found him guilty\nGave him sixteen years in hell\nHe said \"I ain't spending my life here\nI ain't living alone\nAin't breaking no rocks on the chain gang\nI'm breakin' out and headin' home\n\nGonna make a jailbreak\nAnd I'm lookin' towards the sky\nI'm gonna make a jailbreak\nOh, how I wish that I could fly\n\nAll in the name of liberty\nAll in the name of liberty\nGot to be free\n\nJailbreak, let me out of here\nJailbreak, sixteen years\nJailbreak, had more than I can take\nJailbreak, yeah\"\n\nHe said he'd seen his lady being fooled with\nBy another man\nShe was down and he was up\nHe had a gun in his hand\nBullets started flying everywhere\nAnd people started to scream\nBig man lying on the ground\nWith a hole in his body\nWhere his life had been\nBut it was\n\nAll in the name of liberty\nAll in the name of liberty\nI got to be free\n\nJailbreak, jailbreak\nI got to break out\nOut of here\n\nHeartbeats they were racin'\nFreedom he was chasin'\nSpotlights, sirens, rifles firing\nBut he made it out\nWith a bullet in his back",
  "title": "jailbreak"
}
```

## Running locally

```
$ git clone https://github.com/douglasnavarro/mason-jar
$ cd mason-jar
$ virtualenv env
$ source /env/bin/activate
$ pip install -r requirements.txt
$ export FLASK_APP=vagalume_api
$ export FLASK_ENV=development
$ flask run
```

### Running tests

```
$ cd /mason-jar
$ mkdir instance && cd instance
$ curl https://vagalume.com/ed-sheeran > ed.html
$ curl https://vagalume.com/joelma > joelma.html
$ python -m pytest -v
```
---
