"""
testcases of preprocessor.py
"""
from asy_preprocessor import Draw, parse_point, parse_pen, parse_draw


def test_parse_point():
    """
    test point parsing
    """
    inputs = [
        "P S ;= foot(A, B, C)",
        "P' NE := foot(A, B, C)",
        "P_1 4E2N dl= foot(A, B, C)",
        "P 1N1S1E1N d= foot(A, B, C)",
        "P_23' 150 l= foot(A, B, C)",
        "P .= (1, 2)",
        "P_12 100 = (2, 3)",
    ]
    expected_emits = [
        "pair P = foot(A, B, C);",
        "pair P_prime = foot(A, B, C);",
        "pair P_1 = foot(A, B, C);",
        "pair P = foot(A, B, C);",
        "pair P_23_prime = foot(A, B, C);",
        "pair P = (1, 2);",
        "pair P_12 = (2, 3);",
    ]
    expected_post_emits = [
        None,
        'label("$P\'$", P_prime, plain.NE);',
        'dot("$P_1$", P_1, 4*plain.E+2*plain.N);',
        "dot(P);",
        'label("$P_{23}\'$", P_23_prime, dir(150));',
        "dot(P);",
        'dot("$P_{12}$", P_12, dir(100));',
    ]
    for inp, expected_emit, expected_post_emit in zip(
        inputs, expected_emits, expected_post_emits
    ):
        print(inp)
        expr = parse_point(inp)
        assert expr.emit() == expected_emit
        assert expr.emit(3) == expected_post_emit


def test_parse_pen():
    """
    test pen expression parsing
    """
    inputs = ["0.2", "0.2 red", "1 red +dotted", "red 0.2 dotted", "0.2 red+dotted"]
    fill_outputs = [
        "opacity(0.2)",
        "opacity(0.2)+red",
        "opacity(1)+red+dotted",
        "red+opacity(0.2)+dotted",
        "opacity(0.2)+red+dotted",
    ]
    draw_outputs = [
        "linewidth(0.2)",
        "linewidth(0.2)+red",
        "linewidth(1)+red+dotted",
        "red+linewidth(0.2)+dotted",
        "linewidth(0.2)+red+dotted",
    ]
    for inp, expected_fill, expected_draw in zip(inputs, fill_outputs, draw_outputs):
        assert parse_pen(inp, "fill") == expected_fill
        assert parse_pen(inp, "draw") == expected_draw


def test_get_decorator():
    """
    get decorator testing
    """
    inputs = [
        "|",
        "||",
        "||[0.2]",
        "|||[0.2cm red 0.5]",
        "<",
        "<[0.2, 75, 0.3]",
        "<-[0.2, 0.3cm]",
        "->[4, 75]",
        ">-[0.3]",
        "->-[0.3cm]",
        "-<-",
    ]
    outputs = [
        "StickIntervalMarker(1, 1, p=currentpen)",
        "StickIntervalMarker(1, 2, p=currentpen)",
        "StickIntervalMarker(1, 2, p=currentpen, size=0.2cm)",
        "StickIntervalMarker(1, 3, p=red+linewidth(0.5), size=0.2cm)",
        "BeginArrow()",
        "BeginArrow(angle=75.0, size=0.2cm, position=0.3)",
        "BeginArrow(size=0.3cm, position=0.2)",
        "EndArrow(angle=75.0, size=4.0cm)",
        "EndArrow(position=0.3)",
        "EndArrow(size=0.3cm, position=0.5)",
        "BeginArrow(position=0.5)",
    ]
    for inp, out in zip(inputs, outputs):
        expr = Draw("", "", "", inp)
        assert expr.get_decorator() == out
    assert (
        Draw("", "black", "", "|").get_decorator()
        == "StickIntervalMarker(1, 1, p=black)"
    )


def test_parse_draw():
    """
    test of draw parsing
    """
    inputs = [
        "A--B--C--cycle / red 0.5",
        "A--B--C--cycle / red dashed / -<-[0.3cm]",
        "A--B--C--cycle [red 0.5]",
        "A--B--C--cycle [0.5 red] red dashed",
        "A--B--C--cycle [red 0.5] red / |",
    ]
    expected_emits = [
        None,
        None,
        "fill(A--B--C--cycle, red+opacity(0.5));",
        "fill(A--B--C--cycle, opacity(0.5)+red);",
        "fill(A--B--C--cycle, red+opacity(0.5));",
    ]
    expected_post_emits = [
        "draw(A--B--C--cycle, red+linewidth(0.5));",
        "draw(A--B--C--cycle, red+dashed, BeginArrow(size=0.3cm, position=0.5));",
        None,
        "draw(A--B--C--cycle, red+dashed);",
        "draw(A--B--C--cycle, red, StickIntervalMarker(1, 1, p=red));",
    ]
    for inp, expected_emit, expected_post_emit in zip(
        inputs, expected_emits, expected_post_emits
    ):
        print(inp)
        expr = parse_draw(inp)
        assert expr.emit() == expected_emit
        assert expr.emit(2) == expected_post_emit
