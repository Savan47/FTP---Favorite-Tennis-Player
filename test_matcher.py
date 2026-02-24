import pytest
from matcher import name_tokens, is_doubles, is_player_match

def test_name_tokens_basic():
    assert name_tokens("Fils A.") == ["fils", "a"]
    assert name_tokens("Monfils G.") == ["monfils", "g"]
    assert name_tokens("Cobolli F / Dimitrov") == ["cobolli", "f", "dimitrov"]

def test_is_doubles():
    assert is_doubles("Cobolli F / Dimitrov", "Johnson L / Zielinski") is True
    assert is_doubles("Atmane T.", "Dimitrov G.") is False

def test_single_word_surname_does_not_match_substring():
    # Critical bug: "fils" must NOT match "monfils"
    assert is_player_match("fils", "Fils A.", "Atmane T.") is True
    assert is_player_match("fils", "Monfils G.", "Atmane T.") is False

def test_single_word_surname_matches_either_side():
    assert is_player_match("dimitrov", "Atmane T.", "Dimitrov G.") is True
    assert is_player_match("dimitrov", "Dimitrov G.", "Atmane T.") is True

def test_full_name_matches_initial_plus_last():
    assert is_player_match("grigor dimitrov", "Atmane T.", "Dimitrov G.") is True
    assert is_player_match("grigor dimitrov", "Atmane T.", "Dimitrov D.") is False
    assert is_player_match("grigor dimitrov", "Atmane T.", "Dimitrov") is False  # missing initial token

def test_first_name_only_behavior():
    # With the "initial fallback" enabled, this should match:
    assert is_player_match("grigor", "Atmane T.", "Dimitrov G.") is True
    # And should not match if no "g" token exists:
    assert is_player_match("grigor", "Atmane T.", "Dimitrov D.") is False

@pytest.mark.parametrize("bad_input", ["", "   ", None])
def test_empty_player_input_is_false(bad_input):
    assert is_player_match(bad_input, "Atmane T.", "Dimitrov G.") is False