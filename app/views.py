from django.shortcuts import render
import numpy as np
import pickle
import pandas as pd
# Create your views here.

# pt = pickle.load(open('pt.pkl', 'rb'))
similiarity_score = pickle.load(open('cosine_matrix.pkl', 'rb'))
top_50_books_dict = pickle.load(open('top_50_books_dict.pkl', 'rb'))
pt_dict = pickle.load(open('pt_dict.pkl', 'rb'))
book_dict = pickle.load(open('book.pkl', 'rb'))
book = pd.DataFrame(book_dict)
pt = pd.DataFrame(pt_dict)
top_50_books = pd.DataFrame(top_50_books_dict)

def top_50_recomendation(request):
    book_name = list(top_50_books['Book-Title'].values)
    author = list(top_50_books['Book-Author'].values)
    image = list(top_50_books['Image-URL-M'].values)
    votes = list(top_50_books['Num_of_ratings'].values)
    rating = list(top_50_books['avg_ratings'].values)
    data = list(zip(book_name, author, image, votes, rating))

    return render(request, 'index.html', {"data":data})


def recomendation(request):
    if request.method == "POST":
        book_name = request.POST.get('user_input')
        print(book_name)
        recomended_book = recomend(book_name)
        if len(recomended_book)>0:
            books = book[book['Book-Title'].isin(recomended_book)].drop_duplicates('Book-Title')
            book_title = list(books['Book-Title'].values)
            book_author = list(books['Book-Author'].values)
            book_image = list(books['Image-URL-S'].values)
            data = list(zip(book_title, book_author, book_image))
            return render(request, 'recomended.html', {'data':data})
        else:
            data = "No recomendation according to your prefences"
            return render(request, 'recomended.html', {'data':data})
    else:
        book_titles = list(pt.index)
        return render(request, 'recomended.html', {"book_titles":book_titles})
    
def recomend(book_name):
    similar_book = []
    print(np.where(pt.index == book_name))
    index = np.where(pt.index == book_name)[0][0]
#     print(index)
    distance = similiarity_score[index]
    similar_item = sorted(enumerate(distance),key = lambda x:x[1], reverse = True)[1:6]
    for i in similar_item:
        similar_book.append(pt.index[i[0]])
    return similar_book

