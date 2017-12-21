from django.shortcuts import render, redirect, reverse
from ..login.models import *
from models import Message

# https://docs.djangoproject.com/en/1.10/topics/db/aggregation/#generating-aggregates-for-each-item-in-a-queryset
# https://docs.djangoproject.com/en/1.10/topics/db/aggregation/#filter-and-exclude

def current_user(request):
	return User.objects.get(id=request.session['user_id'])

def logout(request):
	del request.session['user_id']
	return redirect('/')	

def index(request):
	try:
		request.session['user_id']
	except KeyError:
		return redirect('/')
	context = {
		'user': User.objects.get(id=request.session['user_id']),
		'others': Message.objects.all()
	}
	return render(request, 'wall/index.html', context)

def favorite(request):
	sender = User.objects.get(id = request.session['user_id'])	
	fav_id = request.POST['receiver']
	newfavorite = Message.objects.get(id = fav_id)
	
	favtable = Favorite.objects.filter(from_liker=sender, to_liked=newfavorite).first()

	if favtable:
		favtable.favmessage = True
		favtable.save()
		print favtable
	else:
		Favorite.objects.create(from_person=sender, to_person=favorite, favmessage=True)
		print 'new FAVORITE!!!!'
	return redirect(reverse('dashboard'))		
def message(request):
	print 'COOOOL Messages!!!!'
	sender = User.objects.get(id = request.session['user_id'])
	content = request.POST['message']
	new_msg = Message.objects.create(content=content, user=sender)
	print new_msg
	
	# if request.method == "POST":
	# 	#Validate form data
	# 	errors = Water.objects.validate(request.POST)

	# 	#if no errors
	# 	if not errors:
	# 		#Get the currently logged in user
	# 		user = current_user(request)
	# 		#Create the new post
	# 		quote = Quote.objects.create_quote(request.POST, user)
	# 		#Redirect back to same page 
	# 		return redirect(reverse('dashboard'))

	# 	#flash errors

	return redirect(reverse('dashboard')) 