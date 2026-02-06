import utils
import pytest

def test_mock_questions():
    questions = utils.mock_questions("seo", 5)
    assert len(questions) == 5
    assert all("seo" in q.lower() for q in questions)

def test_analyze_sentiment():
    # "love" should be positive, "hate" negative
    assert utils.analyze_sentiment("I love this tool") > 0
    assert utils.analyze_sentiment("I hate errors") < 0
    assert utils.analyze_sentiment("This is a book") == 0

def test_get_question_type_score():
    assert utils.get_question_type_score("How to do X") == 3.0
    assert utils.get_question_type_score("What is X") == 2.0
    assert utils.get_question_type_score("Is this X") == 1.0

def test_calculate_value_score():
    score = utils.calculate_value_score("How to optimize seo?")
    assert isinstance(score, float)
    assert score > 0

def test_cluster_questions():
    questions = utils.mock_questions("test", 10)
    clusters = utils.cluster_questions(questions, n_clusters=2)
    assert len(clusters) == 10
    assert len(set(clusters)) <= 2

def test_cluster_questions_empty():
    assert utils.cluster_questions([]) == []
