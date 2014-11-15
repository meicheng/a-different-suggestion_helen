import jinja2
import os
import webapp2

jinja_environment = jinja2.Environment(loader=
    jinja2.FileSystemLoader(os.path.dirname(__file__)))
    
class MainHandler(webapp2.RequestHandler):
  def get(self):
    template_values = {}
    template = jinja_environment.get_template('hello.html')
    self.response.out.write(template.render(template_values))
    
class QuizHandler(webapp2.RequestHandler):
  def get(self):
    name = self.request.get('name')
    other_name = 'Anonymous'
    template_values = {'name': name}
    # can also do: template_values = {'name': self.request.get('name') }
    if name == "":
        template_values['name'] = other_name
    template = jinja_environment.get_template('quiz.html')
    self.response.out.write(template.render(template_values))
    
class GradeQuizHandler(webapp2.RequestHandler):
  def get(self):
    name = self.request.get('name') 
    addition_guess = self.request.get ('addition')
    capital_guess = self.request.get('capital')
    addition_QuizQuestion = QuizQuestion('"What is 3 + 4?"', '7', addition_guess)
    capital_QuizQuestion = QuizQuestion('"What is the capital of California?"', 'Sacramento', capital_guess)
    wrong_answers = []
    if not addition_QuizQuestion.isQuestionCorrect():
        wrong_answers.append(addition_QuizQuestion)
    if not capital_QuizQuestion.isQuestionCorrect():
        wrong_answers.append(capital_QuizQuestion)
    if wrong_answers:
        success = 'Fail'
    else:
        success = 'Pass'
    template_values = {'wrong_answers': wrong_answers, 
    'success': success, 
    'name': name}
    template = jinja_environment.get_template('grade_quiz.html')
    self.response.out.write(template.render(template_values))
    
class QuizQuestion(webapp2.RequestHandler):
  def __init__(self, question, correct, guess):
    self.question = question
    self.correct = correct
    self.guess = guess
    
  def isQuestionCorrect(self):
    return self.guess == self.correct


  
app = webapp2.WSGIApplication([('/', MainHandler),
    ('/quiz', QuizHandler), ('/grade_quiz', GradeQuizHandler),
    ('/evaluation', QuizQuestion)],
    debug=True)