from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, CreateView, ListView, DetailView
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from poll_app.forms import SignUpForm, EmailForm, AnswerForm
from poll_app.models import User, Poll, EmailId
from django.db.models import Max, Sum


class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'registration/signup_form.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('poll_list')


@method_decorator([login_required], name='dispatch')
class PollListView(ListView):
    model = Poll
    ordering = ('pub_date', )
    context_object_name = 'polls'
    template_name = 'poll_app/poll_list.html'

    def get_queryset(self):
        queryset = self.request.user.polls
        return queryset


@method_decorator([login_required], name='dispatch')
class PollCreateView(CreateView):
    model = Poll
    fields = ('poll_text', )
    template_name = 'poll_app/poll_add_form.html'

    def form_valid(self, form):
        poll = form.save(commit=False)
        poll.owner = self.request.user
        poll.save()
        messages.success(self.request, 'poll have been created successfully')
        return redirect('add_email', poll.pk)


class PollDetailView(DetailView):
    model = Poll
    template_name = 'poll_app/poll_detail.html'

    def get_context_data(self, **kwargs):
        kwargs['emailpk'] = self.kwargs['email_pk']
        return super().get_context_data(**kwargs)


class ResultsView(DetailView):
    model = Poll
    template_name = 'poll_app/results.html'


class Help(TemplateView):
    template_name = 'poll_app/help.html'


@login_required
def add_emailaddress(request, pk):
        # only owner of poll would be able to add emailadresses to a EmailId
        # table.
    poll = get_object_or_404(Poll, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.save(commit=False)
            email.poll = poll
            email.save()
            messages.success(request, 'email have been added successfully')
            return redirect('email_change', poll.pk, email.pk)
    else:
        form = EmailForm()

    return render(request, 'poll_app/email_add_form.html', {'poll': poll, 'form': form})


def home(request):
    if request.user.is_authenticated:
        return redirect('poll_list')

    return render(request, 'registration/home.html')


@login_required
def email_change(request, poll_pk, email_pk):
    # only owner of poll can make any change in email list
    poll = get_object_or_404(Poll, pk=poll_pk, owner=request.user)
    email = get_object_or_404(EmailId, pk=email_pk, poll=poll)

    existing_emails = poll.poll.all()

    if request.method == 'POST':
        form = EmailForm(request.POST, instance=email)
        if form.is_valid():
            form.save()
            messages.success(request, 'email has been saved')
            return redirect('home')

    else:
        form = EmailForm(instance=email)

    return render(request, 'poll_app/addmore_email_form.html', {
        'poll': poll,
        'email': email,
        'form': form,
        'existing_emails': existing_emails,
    })


@login_required
def send_first_link(request, poll_pk):

    poll = get_object_or_404(Poll, pk=poll_pk, owner=request.user)
    existing_emails = poll.poll.all()
    mail_list = []
    message_to_send = 'please click on below link to add choices to the given poll \n'

    for i in existing_emails:
        mail_list.append(i.email_id)

    link = 'http://127.0.0.1:8000/polls/' + str(poll_pk) + '/email/check'

    send_mail(
        'Add Choices',
        message_to_send + link,
        'settings.EMAIL_HOST_USER',
        mail_list,
        fail_silently=True,

    )
    return HttpResponse('first link sent')


def check_emailaddress(request, poll_pk):

    poll = get_object_or_404(Poll, pk=poll_pk)
    existing_emails = poll.poll.all()

    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            formobj = form.save(commit=False)
            for i in existing_emails:
                if i.email_id == formobj.email_id:
                    if i.is_partone_complete == False:
                        return redirect('add_choice', poll.pk, i.pk)

                    else:
                        return HttpResponse('you have already added answers')

            return HttpResponse('you are not allowed to add answers')

    form = EmailForm()

    return render(request, 'poll_app/email_check_form.html', {
        'poll': poll,
        'form': form,
        'existing_emails': existing_emails,
    })


def add_choice(request, poll_pk, email_pk):

    poll = get_object_or_404(Poll, pk=poll_pk)
    email = get_object_or_404(EmailId, pk=email_pk, poll=poll)
    existing_choices = poll.answers_poll.all()

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            choice = form.save(commit=False)
            for i in existing_choices:
                if i.choice_text == choice.choice_text:
                    messages.success(
                        request, 'Entered choice already exists in database,please enter some different choice')
                    return redirect('choice_change', poll.pk, email.pk)
            choice.poll = poll
            choice.email = email
            choice.save()
            messages.success(
                request, 'choice have been added successfully add more')
            return redirect('choice_change', poll.pk, email.pk)

    else:
        form = AnswerForm()

    return render(request, 'poll_app/answer_form.html', {'poll': poll, 'form': form, 'email': email, })


def choice_change(request, poll_pk, email_pk):

    poll = get_object_or_404(Poll, pk=poll_pk)
    email = get_object_or_404(EmailId, pk=email_pk, poll=poll)

    existing_choices = email.answers_email.all()

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'choice has been saved')
            return redirect('home')

    else:
        form = AnswerForm()

    return render(request, 'poll_app/addmore_choice_form.html', {
        'poll': poll,
        'email': email,
        'form': form,
        'existing_choices': existing_choices,
    })


def change_status(request, poll_pk, email_pk):

    poll = get_object_or_404(Poll, pk=poll_pk)
    email = get_object_or_404(EmailId, pk=email_pk, poll=poll)
    email.is_partone_complete = True
    email.save()
    existing_emails = poll.poll.all()
    for i in existing_emails:
        if i.is_partone_complete == False:
            return HttpResponse('Will send you link of poll in sometime ,once will get response of firstlink from all emailids')

    return redirect('send_second_link', poll.pk)


def vote(request, poll_pk, email_pk):
    poll = get_object_or_404(Poll, pk=poll_pk)
    email = get_object_or_404(EmailId, pk=email_pk, poll=poll)
    try:
        selected_choice = poll.answers_poll.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'poll_app/Poll_detail.html', {
            'poll': poll,
            'error_message': "You didn't select a choice."
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        email.is_parttwo_complete = True
        email.save()
        existing_emails = poll.poll.all()
        for i in existing_emails:
            if i.is_parttwo_complete == False:
                return HttpResponse('Will send you link of results in sometime ,once will get response of secondlink from all emailids')

        return redirect('send_third_link', poll.pk)

        return HttpResponseRedirect(reverse('home'))


def send_second_link(request, poll_pk):

    poll = get_object_or_404(Poll, pk=poll_pk)
    existing_emails = poll.poll.all()
    mail_list = []

    for i in existing_emails:
        mail_list.append(i.email_id)

    link = 'http://127.0.0.1:8000/polls/' + \
        str(poll_pk) + '/pollemail/check/'

    send_mail(
        'Vote for Given Poll',
        link,
        'settings.EMAIL_HOST_USER',
        mail_list,
        fail_silently=True,

    )
    return HttpResponse('please vote with help of sent link')


def check_pollemailaddress(request, poll_pk):

    poll = get_object_or_404(Poll, pk=poll_pk)
    existing_emails = poll.poll.all()

    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            formobj = form.save(commit=False)
            for i in existing_emails:
                if i.email_id == formobj.email_id:
                    if i.is_partone_complete == True and i.is_parttwo_complete == False:
                        return redirect('poll_detail', poll.pk, i.pk)

                    else:
                        return HttpResponse('you have already voted')

            return HttpResponse('you are not allowed to vote')

    form = EmailForm()

    return render(request, 'poll_app/email_check_form.html', {
        'poll': poll,
        'form': form,
        'existing_emails': existing_emails,
    })


def send_third_link(request, poll_pk):

    poll = get_object_or_404(Poll, pk=poll_pk)
    existing_emails = poll.poll.all()
    existing_choices = poll.answers_poll.all()
    max_votes = existing_choices.aggregate(Max('votes'))['votes__max']
    sum_votes = existing_choices.aggregate(Sum('votes'))['votes__sum']
    max_choice_obj = existing_choices.filter(votes=max_votes)
    avg_clicks = 'Average ratio on each choice : \n'
    message_to_send = 'Maximum votes came for :  \n'
    for i in max_choice_obj:
        message_to_send += i.choice_text
        message_to_send += '\n'
    for i in existing_choices:
        avg_clicks += i.choice_text
        avg_clicks += ' '
        avg_clicks += str(round((i.votes / sum_votes) * 100, 2))
        avg_clicks += ' %'
        avg_clicks += '\n'

    mail_list = []

    for i in existing_emails:
        mail_list.append(i.email_id)

    link = 'http://127.0.0.1:8000/polls/' + \
        str(poll_pk) + '/results/'

    send_mail(
        'Results',
        message_to_send + avg_clicks + link,
        'settings.EMAIL_HOST_USER',
        mail_list,
        fail_silently=True,

    )
    return HttpResponse('sent link of results')
