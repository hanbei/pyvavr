from pyvavr.either import Either


def test_left_creation():
    either = Either.left("Some")

    assert either != None
    assert either.is_left() == True
    assert either.is_right() == False
    assert either._left == "Some"
    assert either._right == None


def test_right_creation():
    either = Either.right("Some")

    assert either != None
    assert either.is_left() == False
    assert either.is_right() == True
    assert either._left == None
    assert either._right == "Some"


def test_map_on_right_either_applies_function():
    either = Either.right("Some").map(lambda x: x + " More")

    assert either != None
    assert either.is_left() == False
    assert either.is_right() == True
    assert either._left == None
    assert either._right == "Some More"

def test_map_on_left_either_does_nothing():
    either = Either.left("Some").map(lambda x: x + " More")

    assert either != None
    assert either.is_left() == True
    assert either.is_right() == False
    assert either._left == "Some"
    assert either._right == None

def test_map_left_on_right_either_does_nothing():
    either = Either.right("Some").map_left(lambda x: x + " More")

    assert either != None
    assert either.is_left() == False
    assert either.is_right() == True
    assert either._left == None
    assert either._right == "Some"

def test_map_left_on_left_either_applies_function():
    either = Either.left("Some").map_left(lambda x: x + " More")

    assert either != None
    assert either.is_left() == True
    assert either.is_right() == False
    assert either._left == "Some More"
    assert either._right == None
