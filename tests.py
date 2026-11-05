import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')

    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

def test_create_question_with_default_points_and_max_selections():
    question = Question(title='q1')
    assert question.points == 1
    assert question.max_selections == 1

def test_create_question_with_invalid_points():
    with pytest.raises(Exception):
        Question(title='q1', points=0)
    with pytest.raises(Exception):
        Question(title='q1', points=101)

def test_add_choice_with_empty_text():
    question = Question(title='q1')
    with pytest.raises(Exception):
        question.add_choice('')

def test_add_choice_with_too_long_text():
    question = Question(title='q1')
    with pytest.raises(Exception):
        question.add_choice('a' * 101)

def test_add_choice_generates_sequential_ids():
    question = Question(title='q1')
    choice1 = question.add_choice('a')
    choice2 = question.add_choice('b')
    assert choice2.id == choice1.id + 1

def test_remove_choice_by_id():
    question = Question(title='q1')
    choice = question.add_choice('a')

    question.remove_choice_by_id(choice.id)

    assert len(question.choices) == 0

def test_remove_choice_by_invalid_id():
    question = Question(title='q1')
    with pytest.raises(Exception):
        question.remove_choice_by_id(999)

def test_remove_all_choices():
    question = Question(title='q1')
    question.add_choice('a')
    question.add_choice('b')

    question.remove_all_choices()

    assert len(question.choices) == 0

def test_set_correct_choices():
    question = Question(title='q1')
    choice1 = question.add_choice('a')
    choice2 = question.add_choice('b')

    question.set_correct_choices([choice1.id])

    assert choice1.is_correct
    assert not choice2.is_correct

def test_correct_selected_choices_returns_only_correct_ones():
    question = Question(title='q1', max_selections=2)
    choice1 = question.add_choice('a')
    choice2 = question.add_choice('b')
    question.set_correct_choices([choice1.id])

    result = question.correct_selected_choices([choice1.id, choice2.id])

    assert result == [choice1.id]

@pytest.fixture
def question_with_choices():
    question = Question(title='q1', max_selections=2)
    choice_a = question.add_choice('a', is_correct=True)
    choice_b = question.add_choice('b', is_correct=False)
    choice_c = question.add_choice('c', is_correct=True)
    return question, choice_a, choice_b, choice_c

def test_correct_selected_choices_with_multiple_correct_selections(question_with_choices):
    question, choice_a, choice_b, choice_c = question_with_choices

    result = question.correct_selected_choices([choice_a.id, choice_c.id])

    assert result == [choice_a.id, choice_c.id]

def test_correct_selected_choices_excludes_incorrect_selection(question_with_choices):
    question, choice_a, choice_b, choice_c = question_with_choices

    result = question.correct_selected_choices([choice_b.id])

    assert result == []

def test_correct_selected_choices_raises_when_exceeding_max_selections(question_with_choices):
    question, choice_a, choice_b, choice_c = question_with_choices

    with pytest.raises(Exception):
        question.correct_selected_choices([choice_a.id, choice_b.id, choice_c.id])