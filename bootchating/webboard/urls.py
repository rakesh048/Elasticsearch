from .views import IndexView,BoardView,NewBoardView,TopicPosts,ReplyTopic,ElasticSearchApi
from django.conf.urls import url


urlpatterns=[
    url(r"^$", IndexView.as_view(),name="home"),
    url(r'^boards/(?P<pk>\d+)/$', BoardView.as_view(), name='board_topics'),
    url(r'^boards/(?P<pk>\d+)/new/$', NewBoardView.as_view(), name='new_topic'),
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/$', TopicPosts.as_view(), name='topic_posts'),
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/reply/$', ReplyTopic.as_view(), name='reply_topic'),
    url(r'^elastic_search/$', ElasticSearchApi.as_view(), name='elastic_search'),


]
