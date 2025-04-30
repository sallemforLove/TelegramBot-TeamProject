from django.shortcuts import get_object_or_404, render, redirect
from .models import Survey, Question, AnswerOption
from .forms import SurveyForm, QuestionForm, AnswerOptionForm
from django.views.decorators.http import require_POST


def create_survey(request):
    if request.method == 'POST':
        survey_form = SurveyForm(request.POST)
        if survey_form.is_valid():
            survey = survey_form.save()  # сохраняем новый опрос
            return redirect('create_question', survey_id=survey.id)
    else:
        survey_form = SurveyForm()

    return render(request, 'main/create_survey.html', {'survey_form': survey_form})

def create_question(request, survey_id):
    survey = Survey.objects.get(id=survey_id)

    questions = Question.objects.filter(survey=survey)

    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            question = question_form.save(commit=False)
            question.survey = survey
            question.save()
            return redirect('create_answer_option', question_id=question.id)
    else:
        question_form = QuestionForm(initial={'survey': survey})

    return render(request, 'main/create_question.html', {
        'question_form': question_form,
        'survey': survey,
        'questions': questions
    })


def create_answer_option(request, question_id):
    question = Question.objects.get(id=question_id)
    existing_options = AnswerOption.objects.filter(question=question)

    if request.method == 'POST':
        answer_option_form = AnswerOptionForm(request.POST)
        if answer_option_form.is_valid():
            answer_option = answer_option_form.save(commit=False)
            answer_option.question = question
            answer_option.save()

            if 'add_more' in request.POST:
                return redirect('create_answer_option', question_id=question.id)
            elif 'done' in request.POST:
                return redirect('create_question', survey_id=question.survey.id)
    else:
        answer_option_form = AnswerOptionForm(initial={'question': question})

    return render(request, 'main/create_answer_option.html', {
        'answer_option_form': answer_option_form,
        'question': question,
        'existing_options': existing_options  #
    })

def edit_survey(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)

    if request.method == 'POST':
        form = SurveyForm(request.POST, instance=survey)
        if form.is_valid():
            form.save()
            return redirect('create_question', survey_id=survey.id)  # или куда вам нужно
    else:
        form = SurveyForm(instance=survey)

    return render(request, 'main/edit_survey.html', {'form': form, 'survey': survey})

def edit_answer_option(request, option_id):
    option = get_object_or_404(AnswerOption, id=option_id)
    if request.method == 'POST':
        form = AnswerOptionForm(request.POST, instance=option)
        if form.is_valid():
            form.save()
            return redirect('create_answer_option', question_id=option.question.id)
    else:
        form = AnswerOptionForm(instance=option)

    return render(request, 'main/edit_answer_option.html', {'form': form, 'option': option})


def edit_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('create_answer_option', question_id=question.id)
    else:
        form = QuestionForm(instance=question)

    return render(request, 'main/edit_question.html', {'form': form, 'question': question})


def dashboard(request):
    surveys = Survey.objects.all().order_by('-created_at')
    return render(request, 'main/dashboard.html', {'surveys': surveys})

@require_POST
def delete_survey(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    survey.delete()
    return redirect('dashboard')