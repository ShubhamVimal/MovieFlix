from django.shortcuts import render
from django.http import HttpResponse
import pymysql
from datetime import datetime

connection = pymysql.connect(host='localhost',port=3306,user='root',database='movierecommend',autocommit = True)

cursor = connection.cursor()

query = "select * from movies where Genre like  '%Action%' limit 4 "
cursor.execute(query)
actionMovies = cursor.fetchall()

query = "select * from movies where Genre like  '%Adventure%' limit 4 "
cursor.execute(query)
adventureMovies = cursor.fetchall()

query = "select * from movies where Genre like  '%Animation%' limit 4 "
cursor.execute(query)
animationMovies = cursor.fetchall()

query = "select * from movies where Genre like  '%Biography%' limit 4 "
cursor.execute(query)
biographyMovies = cursor.fetchall()

query = "select * from movies where Genre like  '%Comedy%' limit 4 "
cursor.execute(query)
comedyMovies = cursor.fetchall()

query = "select * from movies where Genre like  '%Crime%' limit 4 "
cursor.execute(query)
crimeMovies = cursor.fetchall()

query = "select * from movies where Genre like  '%Drama%' limit 4 "
cursor.execute(query)
DramaMovies = cursor.fetchall()

query = "select * from movies where Genre like '%Family%' limit 4 "
cursor.execute(query)
familyMovies = cursor.fetchall()

query = "select * from movies where Genre like  '%Fantasy%' limit 4 "
cursor.execute(query)
fantasyMovies = cursor.fetchall()

query = "select * from movies where Genre like  '%Film-Noir%' limit 4 "
cursor.execute(query)
filmNoirMovies = cursor.fetchall()

query = "select * from movies where Genre like  '%History%' limit 4 "
cursor.execute(query)
historyMovies = cursor.fetchall()

query = "select * from movies where Genre like  '%Horror%' limit 4 "
cursor.execute(query)
horrorMovies = cursor.fetchall()

query = "select * from movies where Genre like  '%Music%' limit 4 "
cursor.execute(query)
musicMovies = cursor.fetchall()

# query = "select * from movies where Genre like  '%Musical%' limit 4 "
# cursor.execute(query)
# musicalMovies = cursor.fetchall()

query = "select * from movies where Genre like  '%Mystery%' limit 4 "
cursor.execute(query)
mysteryMovies = cursor.fetchall()

query = "select * from movies where Genre like  '%Romance%' limit 4 "
cursor.execute(query)
romanceMovies = cursor.fetchall()

query = "select * from movies where Genre like  '%Sci-Fi%' limit 4 "
cursor.execute(query)
sciFiMovies = cursor.fetchall()

query = "select * from movies where Genre like  '%Sport%' limit 4 "
cursor.execute(query)
sportMovies = cursor.fetchall()

query = "select * from movies where Genre like  '%Thriller%' limit 4 "
cursor.execute(query)
thrillerMovies = cursor.fetchall()

query = "select * from movies where Genre like  '%War%' limit 4 "
cursor.execute(query)
warMovies = cursor.fetchall()

query = "select * from movies where Genre like  '%Western%' limit 4 "
cursor.execute(query)
westernMovies = cursor.fetchall()


# UserID's = [1,2,3,4,5]
# Recently watched movies by User with UserID=2
query = 'SELECT MovieID FROM users_movies WHERE UserID=2 ORDER BY TimeStamp DESC LIMIT 4'
cursor.execute(query)
recentlyWatchedMovies = cursor.fetchall()
recentWatchedMovies = {}
for movieId in recentlyWatchedMovies:
    query = 'select * from movies where MovieID=%s'
    cursor.execute(query,(movieId[0]))
    data = cursor.fetchall()
    recentWatchedMovies[movieId] = data

query = " select UserName from users_movies where UserID=2 "
cursor.execute(query)
user = cursor.fetchall()
userName = user[0][0]


# Most watched genre by user
userGnereDict = {
    "Action" : 0, "Adventure" : 0, "Animation" : 0, "Biography" : 0, "Comedy" : 0 ,"Crime" : 0
    ,"Drama" : 0,"Family" : 0,"Fantasy" : 0,"Film-Noir" : 0,"History" : 0,"Horror" : 0,"Music" : 0
    ,"Mystery" : 0,"Romance" : 0,"Sci-Fi" : 0,"Sport" : 0,"Thriller" : 0,"War" : 0,"Western" : 0,
    "Musical":0
}

query = " select MovieID from users_movies where UserID=2 "
cursor.execute(query)
curr_user_all_watched_movies = cursor.fetchall()
#print(curr_user_all_watched_movies)
curr_user_movieID = []
for movie_id in curr_user_all_watched_movies:
    curr_user_movieID.append(movie_id[0])
    query = " select Genre from movies where MovieID=%s"
    cursor.execute(query,(movie_id[0]))
    cat = cursor.fetchall()
    for c in cat:
        for i in list(c):
            category = i.split(',')
            for j in category:
                userGnereDict[j] += 1

maximumValue_Key = max(userGnereDict, key=userGnereDict.get)

query = "select * from movies where Genre like  '%"+maximumValue_Key+"%' ORDER BY Rating DESC"
cursor.execute(query)
all_movies = cursor.fetchall()
fullMovies = []
for i in all_movies:
    fullMovies.append(list(i))

for i in curr_user_movieID:
    for j in fullMovies:
        if i in j:
            fullMovies.remove(j)

def users_movies_check(movieID,userID,userName,):
    currtimeStamp = datetime.now().strftime("%Y:%m:%d %H:%M:%S")
    check_query = "select * from users_movies where MovieID="+movieID+" "
    cursor.execute(check_query)
    data = cursor.fetchall()
    if len(data) > 0:
        update_query = "UPDATE users_movies SET TimeStamp="+currtimeStamp+" WHERE MovieID="+movieID+" "
        cursor.execute(update_query)
    else:
        insert_query = "INSERT into users_movies(UserID,UserName,MovieID,TimeStamp) values ("+userID+","+userName+","+movieID+","+currtimeStamp+") "
        cursor.execute(insert_query)


def index(req):
    data = {
        "Action":actionMovies,"Adventure":adventureMovies,"Animation":animationMovies,"Biography":biographyMovies
            ,"Comedy":comedyMovies,"Crime":crimeMovies,"Drama":DramaMovies,"Family":familyMovies,
            "Fantasy":fantasyMovies,"Film-Noir":filmNoirMovies,"History":historyMovies,
            "Horror":horrorMovies,"Music":musicMovies,"Mystery":mysteryMovies,"Romance":romanceMovies,
            "Sci-Fi":sciFiMovies,"Sport":sportMovies,"Thriller":thrillerMovies,"War":warMovies,
            "Western":westernMovies,
        }
    return render(req, 'index.html', context={"data":data,"RecentMovies":recentWatchedMovies,"Username":userName,"RecommendMovies":fullMovies[:4]})

def details(req,pk):
    
    # users_movies_check(pk,)
    
    query = "select * from movies where MovieID=%s"
    cursor.execute(query, (pk))
    data = cursor.fetchall()

    query = 'SELECT * FROM movies'
    cursor.execute(query)
    all_movies = cursor.fetchall()

    current_movie_cat = data[0][4].split(',')
    similar = []
    for i in range(len(all_movies)):
        if pk == all_movies[i][0]:
            continue
        movie_cat = all_movies[i][4].split(',')
        n = len(set(movie_cat).intersection(current_movie_cat))
        d = len(set(movie_cat).union(current_movie_cat))
        score = n/d
        if score > 0.3:
            similar.append(all_movies[i])
    
    return render(req, "details.html",context={"data":data,"Similar":similar})

def allmovies(req,genre):
    query = "select * from movies where Genre like '%"+genre+"%' " 
    cursor.execute(query)
    data = cursor.fetchall()
    return render(req,"allmovies.html",context={"data":data,"Genre":genre})

def searchResults(req):
    searchQuery = req.POST.get('input_query')
    query = "select * from movies where Title like '%"+searchQuery+"%' or Directors like '%"+searchQuery+"%' or Cast like '%"+searchQuery+"%' "
    cursor.execute(query)
    data = cursor.fetchall()
    return render(req,"searchResults.html",context={"data":data,"Query":searchQuery})

def loginSignUp(req):

    # LOGIN
    if 'login_input' in req.POST and 'login_password' in req.POST:
        login_cred = req.POST['login_input']
        password = req.POST['login_password']

        query = "select * from users_info where (Username = "+login_cred+" or Email_ID = "+login_cred+") and Password="+password+" "
        cursor.execute(query)
        userInfo = cursor.fetchall()
        if len(userInfo) > 0:
            pass
        else:
            pass
    
    # SIGN UP
    elif 'sign_up_username' in req.POST and 'sign_up_email' in req.POST and 'sign_up_password' in req.POST:
        username = req.POST['sign_up_username']
        email = req.POST['sign_up_email']
        password = req.POST['sign_up_password']

        # UserID(First Column) is set to Auto-increment 
        query = "INSERT into users_info(Username,Email_ID,Password) values("+username+","+email+","+password+")"
        cursor.execute(query)