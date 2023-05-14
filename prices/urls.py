from django.urls import path
from . import views
from .views import saveToDo,getRss,delToDo,editToDo,editToDoPost,TimeLeft,orderTodo,palindromePage,palindromeCheck



urlpatterns = [
    #aloitussivun määrittely, tämä näytetään ensimmäisenä
    path('',views.indexPage),
    path('indexPage/',views.indexPage),
    path('FundValues/',views.FundValues),
    path('udpRead/',views.udpRead),
    #path('readUdp/',views.readUdp)
    path('showToDo/',views.showToDo),
    
    #YHDISTETÄÄN SAVE-TO-DO NIMINEN FORMI JA TALLENNUKSEN TOTEUTTAVA FUNKTIO
    path('save-To-Do/',saveToDo),
    #tällä mennään rss-sivulle
    path('showRssPage',views.showRssPage),
    path('rss-Address/',getRss),
    #parametriviittaus tarvitaan poistamisessa
    path('del-Task/<int:idnum>/',delToDo),
    path('edit-Task/<int:idnum>/',editToDo),
    path('edit-post/<int:idnum>/',editToDoPost),
    path('time-left/<int:idnum>/',TimeLeft),
    path('order-To-Do',orderTodo),
    path('palindromePage/',views.palindromePage),
    path('palindrome-check',palindromeCheck),
    path('systemCheck',views.systemCheck)
]