from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('populated_cities', views.populated_cities_query, name ='populated_cities'),
    path('start_tour_cities', views.start_tour_cities, name ='start_tour_cities'),
    path('stop_tour_cities', views.stop_tour_cities, name ='stop_tour_cities'),
    path('premierLeague_stadiums', views.premierLeague_stadiums_query, name ='premierLeague_stadiums'),
    path('start_tour_stadiums', views.start_tour_stadiums, name ='start_tour_stadiums'),
    path('stop_tour_stadiums', views.stop_tour_stadiums, name ='stop_tour_stadiums'),
    path('longest_rivers', views.longest_rivers_query, name ='longest_rivers'),
    path('tour_experience', views.tour_experience, name ='tour_experience'),
    path('line_track_experience', views.line_track_experience, name ='line_track_experience'),
    path('stop_experience', views.stop_experience, name ='stop_experience'),
    path('spanish_airports', views.spanish_airports_query, name ='spanish_airports'),
    path('start_tour_airports', views.start_tour_airports, name ='start_tour_airports'),
    path('stop_tour_airports', views.stop_tour_airports, name ='stop_tour_airports'),
    path('summer_olympic_games_aux', views.olympic_games_query_aux, name ='summer_olympic_games_aux'),
    path('summer_olympic_games', views.olympic_games_query, name ='summer_olympic_games'),
    path('try_demo', views.try_demo, name ='try_demo'),
    path('start_lleida_tour', views.start_lleida_tour, name ='start_lleida_tour'),
    path('start_bayern_tour', views.start_bayern_tour, name ='start_bayern_tour'),
    path('start_barcelona92', views.start_barcelona92, name ='start_barcelona92'),
    path('stop_tour_demo', views.stop_tour_demo, name ='stop_tour_demo'),
    path('clear_KML_folder', views.clear_KML_folder, name ='clear_KML_folder'),
    path('stop_current_tour', views.stop_current_tour, name ='stop_current_tour'),
    path('relaunch_LG', views.relaunch_LG, name ='relaunch_LG'),
    path('clear_LG_cache', views.clear_LG_cache, name ='clear_LG_cache')
]