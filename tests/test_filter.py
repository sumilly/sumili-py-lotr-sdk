from lotr_sdk import Filter


def test_match():
    assert Filter().match("name", "Gandalf").build() == "name=Gandalf"


def test_not_match():
    assert Filter().not_match("name", "Frodo").build() == "name!=Frodo"


def test_include():
    assert Filter().include("race", "Hobbit", "Human").build() == "race=Hobbit,Human"


def test_exclude():
    assert Filter().exclude("race", "Orc", "Goblin").build() == "race!=Orc,Goblin"


def test_exists():
    assert Filter().exists("name").build() == "name"


def test_not_exists():
    assert Filter().not_exists("name").build() == "!name"


def test_regex():
    assert Filter().regex("name", "/foot/i").build() == "name=/foot/i"


def test_not_regex():
    assert Filter().not_regex("name", "/foot/i").build() == "name!=/foot/i"


def test_lt():
    assert Filter().lt("budgetInMillions", 100).build() == "budgetInMillions<100"


def test_gt():
    assert Filter().gt("academyAwardWins", 0).build() == "academyAwardWins>0"


def test_gte():
    assert Filter().gte("runtimeInMinutes", 160).build() == "runtimeInMinutes>=160"


def test_lte():
    assert Filter().lte("runtimeInMinutes", 200).build() == "runtimeInMinutes<=200"


def test_raw():
    assert Filter().raw("budgetInMillions<100").build() == "budgetInMillions<100"


def test_chaining_multiple_conditions():
    result = (
        Filter()
        .gt("academyAwardWins", 0)
        .gte("runtimeInMinutes", 160)
        .build()
    )
    assert result == "academyAwardWins>0&runtimeInMinutes>=160"


def test_chaining_mixed_operators():
    result = (
        Filter()
        .match("name", "The Fellowship of the Ring")
        .lt("budgetInMillions", 100)
        .exists("rottenTomatoesScore")
        .build()
    )
    assert result == "name=The%20Fellowship%20of%20the%20Ring&budgetInMillions<100&rottenTomatoesScore"


def test_empty_filter():
    assert Filter().build() == ""


def test_each_call_returns_same_instance():
    f = Filter()
    assert f.match("a", "b") is f
    assert f.gt("x", 1) is f
    assert f.exists("y") is f
