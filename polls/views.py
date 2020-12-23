from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse

from .models import Question, Choice

# Get questions and display them


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

# Show specific question and choices


def detail(request, question_id):
    
    #this is for get request
    question = get_object_or_404(Question, pk=question_id)
    
    choices = question.choice_set.all()  # this show all the choices

    if request.method == 'POST':

        try:
            selected_choice = question.choice_set.get(
                pk=request.POST['choice'])
            print("---------", selected_choice)

        except (KeyError, Choice.DoesNotExist):
            
            # Redisplay the question voting form.
            return render(request, 'polls/detail.html', {
                'question': question,'choices':choices,
                
                'error_message': "You didn't select a choice.",
            })

        else:
            
            selected_choice.votes += 1
            selected_choice.save()
            return redirect(
                'polls:results', question_id
            )
            

    return render(request, 'polls/detail.html', {'question': question, 'choices': choices})



"""
If i want to work on dif view then use below detail and vote view
-------------------------------------------------------------------------
=>Here detail view just show the choicesie for --get-- request and detail view for handling --post-- request.
=>You should also give action for vote view in html form if wise to use both the view otherwise not necesary

"""

# def detail(request, question_id):
    
#     #this is for get request
#     question = get_object_or_404(Question, pk=question_id)
#     choices = question.choice_set.all()  # this show all the choices  

#     return render(request, 'polls/detail.html', {'question': question, 'choices': choices})


# # # Vote for a question choice
# def vote(request, question_id):
#     print("------2----------")
#     # print(request.POST['choice'])#this return choice id
#     question = get_object_or_404(Question, pk=question_id)

#     try:
#         # request.POST['choice'] means 	name="choice" and it receives choice id of that radio input
#         selected_choice = question.choice_set.get(pk=request.POST['choice'])
#     except (KeyError, Choice.DoesNotExist):
#         # Redisplay the question voting form.
#         return render(request, 'polls/detail.html', {
#             'question': question,
#             'error_message': "You didn't select a choice.",
#         })
#     else:
#         selected_choice.votes += 1
#         selected_choice.save()
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
#         return redirect('polls:results', question_id)


# Get question and display results
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})
