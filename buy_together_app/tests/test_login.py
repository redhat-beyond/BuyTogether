import pytest
from unittest.mock import Mock
from buy_together_app import views
from django.shortcuts import render, redirect
from django.test import RequestFactory


@pytest.fixture
def authenticate_mock(monkeypatch):
    mock = Mock()
    monkeypatch.setattr(views, views.authenticate.__name__, mock)
    return mock


@pytest.fixture
def login_mock(monkeypatch):
    mock = Mock()
    monkeypatch.setattr(views, views.login.__name__, mock)
    return mock


@pytest.fixture
def redirect_mock(monkeypatch):
    mock = Mock()
    monkeypatch.setattr(views, views.redirect.__name__, mock)
    mock.return_value = redirect('Main Page')
    return mock


@pytest.fixture
def messages_mock(monkeypatch):
    mock = Mock()
    monkeypatch.setattr(views, "messages", mock)
    return mock


@pytest.fixture
def render_mock(monkeypatch, get_request):
    mock = Mock()
    monkeypatch.setattr(views, views.render.__name__, mock)
    mock.return_value = render(get_request, 'buy_together_app/login.html')
    return mock


@pytest.fixture
def post_method_mock():
    mock = Mock()
    mock.method = 'POST'
    return mock


@pytest.fixture
def get_request():
    request = RequestFactory().get('/login')
    return request


@pytest.fixture
def not_post_method_mock():
    mock = Mock()
    mock.method = ''
    return mock


def test_login_success(authenticate_mock,
                       login_mock,
                       redirect_mock,
                       post_method_mock):

    output = views.log_in_page(post_method_mock)
    assert output == redirect_mock.return_value
    authenticate_mock.assert_called_once()
    login_mock.assert_called_once()
    redirect_mock.assert_called_once()


def test_login_not_post(render_mock,
                        not_post_method_mock):

    output = views.log_in_page(not_post_method_mock)
    assert output == render_mock.return_value
    render_mock.assert_called_once()


def test_login_failed_auth(authenticate_mock,
                           messages_mock,
                           render_mock,
                           post_method_mock):

    authenticate_mock.return_value = None
    output = views.log_in_page(post_method_mock)
    assert output == render_mock.return_value
    authenticate_mock.assert_called_once()
    messages_mock.info.assert_called_with(post_method_mock, 'User name OR Password is incorrect')
    render_mock.assert_called_once()
