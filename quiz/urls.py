from django.urls import path
from quiz.views import *
from quiz.classview import *

urlpatterns = [
    # path('', home, name='quiz-home'),
    path('', UserView.as_view(), name='quiz-users'),
    #path('users/', users, name='quiz-users'),
    path('text-learning/', TextLearningView.as_view(), name='text-learning'),
    path('layout-lerning/', LayoutLearningView.as_view(), name='layout-learning'),
    path('alpinejs-learning/', AlpineJSLearningView.as_view(), name='alpinejs-learning'),


    path('users/', UserView.as_view(), name='quiz-users'), # get from Class view
    path('users2/', UserTemplateView.as_view(), name='quiz-users-2'),
    path('users3/', UserListView.as_view(), name='quiz-users-3'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='quiz-member-detail'),
    path('user/register/', UserRegisterView.as_view(), name='quiz-user-register'),
    path('user/register2/', SignUpView.as_view(), name='quiz-user-register2'),
    path('user/login/', UserLoginView.as_view(), name='quiz-user-login'),
    path('user/logout/', UserLogoutView.as_view(), name='quiz-user-logout'),

    path('quiz/', QuizView.as_view(), name='quiz-start'),
    path('quiz/results/', QuizResultsView.as_view(), name='quiz-results'),
    path('quiz2/', QuizView2.as_view(), name='quiz2-start'),
    path('quiz2/results2/', QuizResultView2.as_view(), name='quiz-results2'),
    
    path('quiz-data/', quiz_data, name='quiz-data'),
    path('submit-answer/', submit_answer, name='submit-answer'),
    path('calculate-score/', calculate_score, name='calculate-score'),


    
    #path('username/<slug:slug>/', UserDetailView.as_view(), name='quiz-user-slug'),
    path('create/', create),
    path('json/', json),
    path('pdf/', pdf),
    path('bg/', bg),
    path('blurbg/', blurbg),


    path('quiz/questions/', QuestionListView.as_view(), name='questions_list'),
    path('quiz/question/create/', QuestionCreateView.as_view(), name='question_create'),
    path('quiz/question/view/<int:pk>/', QuestionDetailView.as_view(), name='question_detail'),
    path('quiz/question/update/<int:pk>/', QuestionUpdateView.as_view(), name='question_edit'),
    path('quiz/question/delete/<int:pk>/', QuestionDeleteView.as_view(), name='question_delete'),







    path('choice/create/', ChoiceCreateView.as_view(), name='quiz-choice-create'),
    path('choice/update/<int:pk>/', ChoiceUpdateView.as_view(), name='quiz-choice-update'),
    path('choice/delete/<int:pk>/', ChoiceDeleteView.as_view(), name='quiz-choice-delete'),

    path('user/delete/<int:pk>/', UserDeleteView.as_view(), name='quiz-user-delete'),
    path('member/update/<int:pk>/', MemberUpdateView.as_view(), name='quiz-member-update'),
    #path('user/create/', UserCreateView.as_view(), name='quiz-user-create'),
]

