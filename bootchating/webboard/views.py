from django.shortcuts import render
from rest_framework.views import APIView	
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404,redirect
from .models import *
from .forms import NewTopicForm,PostForm
# Create your views here.
from django.db.models import Count


class IndexView(APIView):
	permission_classes = (AllowAny,)

	def get(self,request):
		boards = Board.objects.all()
		return render(request, 'home.html', {'boards': boards})

class BoardView(APIView):
    permission_classes = (AllowAny,)

    def get(self,request,pk):
        board = Board.objects.get(pk=pk)
        topic = board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
        return render(request, 'topics.html', {'board': board,'topic':topic})


class NewBoardView(APIView):
	permission_classes = (AllowAny,)

	def get(self,request,pk):
		board = get_object_or_404(Board, pk=pk)
		return render(request, 'new_topic.html', {'board': board})

	def post(self,request,pk):
		board = get_object_or_404(Board, pk=pk)
		subject = request.POST['subject']
		message = request.POST['message']

		user = User.objects.get(username='rakesh')  # TODO: get the currently logged in user

		topic = Topic.objects.create(
			subject=subject,
			board=board,
			starter=user
		)

		post = Post.objects.create(
			message=message,
			topic=topic,
			created_by=user
		)
		return redirect('board_topics', pk=board.pk)

class TopicPosts(APIView):
    permission_classes = (AllowAny,)
    def get(self,request,pk,topic_pk):
        topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
        topic.views +=1
        topic.save()
        return render(request, 'topic_posts.html', {'topic': topic})

class ReplyTopic(APIView):
	permission_classes = (AllowAny,)

	def get(self,request,pk,topic_pk):
		topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
		form = PostForm()
		return render(request, 'reply_topic.html', {'topic': topic, 'form': form})

	def post(self,request,pk, topic_pk):
		form = PostForm(request.POST)
		topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
		if form.is_valid():
			post = form.save(commit=False)
			post.topic = topic
			post.created_by = topic.starter
			post.save()
			return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
