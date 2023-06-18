"""
Asymptote preprocessor with automatic labelling

based on TSQX from https://github.com/cjquines/tsqx
"""

import re
import os
import sys


class Op:
    """
    a datatype representing any kind of expression
    """
    def emit(self, iteration=1) -> str:
        """
        emit an expression
        """
        raise NotImplementedError


class AsyCmd(Op):
    """
    a datatype representing normal Asymptote command
    """

    def __init__(self, cmd: str):
        self.cmd = cmd

    def emit(self, iteration=1) -> str:
        if iteration == 1:
            return self.cmd


class Point(Op):
    """
    a datatype representing point definitions
    """

    def __init__(self, name, defn, label_dir="", dot=True, label=True):
        self.name = name
        self.defn = defn
        self.label_dir = label_dir
        self.dot = dot
        self.label = label

    def _latex_label(self) -> str:
        label = self.name
        has_prime = label.endswith("_prime")
        if has_prime:
            label = label[: -len("_prime")]
        if "_" in label:
            # proper subscripting (i.e., M_BC to M_{BC})
            head, tail = label.split("_", 1)
            if len(tail) > 1:
                label = head + f"_{{{tail}}}"
        if has_prime:
            label += "'"
        return f"${label}$"

    def emit(self, iteration=1) -> str:
        if iteration == 1:
            return f"pair {self.name} = {self.defn};"
        if iteration == 3:
            if self.dot and self.label:
                return f'dot("{self._latex_label()}", {self.name}, {self.label_dir});'
            if self.dot:
                return f"dot({self.name});"
            if self.label:
                return f'label("{self._latex_label()}", {self.name}, {self.label_dir});'

class Draw(Op):
    """
    a datatype representing drawing expression
    """

    def __init__(self, path, drawpen, fillpen, decorator=""):
        self.path = path
        self.drawpen = drawpen
        self.fillpen = fillpen
        self.decorator = decorator

    def get_decorator(self):
        """
        get the decorator in asymptote form
        """
        decorator = self.decorator
        # case 1: StickIntervalMarker
        if decorator.startswith("|"):
            cnt = 0
            while cnt < len(decorator) and decorator[cnt] == "|":
                cnt += 1
            res = f"StickIntervalMarker(1, {cnt}, "
            if cnt == len(decorator):
                res += f"p={self.drawpen or 'currentpen'}"
                return res + ")"
            if (decorator[cnt], decorator[-1]) not in [
                ("(", ")"),
                ("[", "]"),
                ("{", "}"),
            ]:
                return SyntaxError("Can't parse the decorator")
            args = decorator[cnt + 1 : -1]
            if " " not in args:
                size = args
                res += f"p={self.drawpen or 'currentpen'}"
            else:
                size, rest = args.split(" ", 1)
                res += f"p={parse_pen(rest, 'draw')}"
            if not size.endswith("cm"):
                size += "cm"
            res += f", size={size}"
            return res + ")"
        # case 2: arrows
        else:
            dash_left = False
            dash_right = False
            cnt = 0
            while decorator[cnt] == "-":
                cnt += 1
                dash_left = True
            arrow_type = {">": "EndArrow", "<": "BeginArrow"}[decorator[cnt]]
            cnt += 1
            while cnt < len(decorator) and decorator[cnt] == "-":
                cnt += 1
                dash_right = True
            res = f"{arrow_type}("
            position = (
                0.5
                if (arrow_type == "EndArrow" and dash_right)
                or (arrow_type == "BeginArrow" and dash_left)
                else None
            )
            # if no arguments
            if cnt == len(decorator):
                if position:
                    res += f"position={position}"
                return res + ")"
            # parse arguments
            if (decorator[cnt], decorator[-1]) not in [
                ("(", ")"),
                ("[", "]"),
                ("{", "}"),
            ]:
                return SyntaxError("Can't parse the decorator")
            args = decorator[cnt + 1 : -1].replace(",", " ").split()
            pos_used = False
            angle_used = False
            for arg in reversed(args):
                if "." in arg and (not pos_used) and (not arg.endswith("cm")):
                    pos_used = True
                    position = float(arg)
                elif "." in arg or arg.endswith("cm") or angle_used:
                    if arg.endswith("cm"):
                        arg = arg[:-2]
                    res += f"size={float(arg)}cm, "
                else:
                    angle_used = True
                    res += f"angle={float(arg)}, "
            if position:
                res += f"position={position}"
                return res + ")"
            else:
                if res.endswith(", "):
                    res = res[:-2]
                return res + ")"

    def emit(self, iteration=1) -> str:
        if iteration == 1 and self.fillpen:
            return f"fill({self.path}, {self.fillpen});"
        if iteration == 2 and self.drawpen:
            if self.decorator:
                return f"draw({self.path}, {self.drawpen}, {self.get_decorator()});"
            return f"draw({self.path}, {self.drawpen});"


def parse_dir(dirs):
    """parse the directions expression and convert to asy format"""
    dirs = dirs.strip()
    if dirs == "":
        return ""
    if dir_pairs := re.findall(r"(\d+)([A-Z]+)", dirs):
        return "+".join(f"{n}*plain.{w}" for n, w in dir_pairs)
    elif dirs.isdigit():
        return f"dir({dirs})"
    elif re.fullmatch(r"N?S?E?W?", dirs):
        return f"plain.{dirs}"
    else:
        raise SyntaxError(f"Can't parse direction {dirs}")


def parse_point(cmd: str):
    """return a point expression; raises an exception if invalid format"""
    tokens = cmd.replace("=", " = ").replace("'", "_prime").split(" ")
    name, *rest = tokens
    idx = rest.index("=")
    alias_map = {";": ";", ":": ":", ".": ".", "d": ".", "l": ":", "ld": "", "dl": ""}
    label_dir = ""
    if idx > 0 and rest[idx - 1] in alias_map:
        dot = alias_map[rest[idx - 1]] in {".", ""}
        label = alias_map[rest[idx - 1]] in {":", ""}
        if idx > 1:
            label_dir = parse_dir(rest[0])
    else:
        dot = True
        label = True
        if idx > 0:
            label_dir = parse_dir(rest[0])
    defn = " ".join(rest[idx + 1 :]).strip()
    if defn.endswith(";"):
        defn = defn[:-1]
    return Point(name, defn, label_dir, dot, label)


def parse_pen(expr: str, mode: str):
    """
    parse the pen expression
    """
    if mode not in ["fill", "draw"]:
        raise ValueError("Mode not recognized")
    tokens = expr.replace(" +", "+").replace("+ ", "+").split(" ")
    if not tokens:
        return "defaultpen"
    res = ""
    for token in tokens:
        if token.replace(".", "", 1).isnumeric():
            res += {"fill": "opacity", "draw": "linewidth"}[mode] + f"({token})"
        else:
            res += token
        res += "+"
    return res[:-1]


def parse_draw(cmd: str):
    """
    parse the drawing expression
    """
    cmd += " "
    tokens = (
        cmd.replace("'", "_prime").replace(" [", " [ ").replace("] ", " ] ").split()
    )
    fillpen = ""
    drawpen = ""
    decorator = ""
    if "/" not in tokens or "[" in tokens[:tokens.index("/")]:  # if fillpen exists
        fill_beg = len(tokens) - tokens[::-1].index("[")
        fill_end = tokens.index("]", fill_beg)
        path = " ".join(tokens[:fill_beg-1])
        fillpen = parse_pen(" ".join(tokens[fill_beg:fill_end]), "fill")
        if fill_end+1 < len(tokens) and tokens[fill_end+1] == "/":
            fill_end += 1
        rest = tokens[fill_end+1:]
    else:
        draw_begin = tokens.index("/") + 1
        path = " ".join(tokens[: draw_begin - 1])
        rest = tokens[draw_begin:]
    if "/" in rest:  # there is a decorator
        draw_end = rest.index("/")
        drawpen = parse_pen(" ".join(rest[:draw_end]), "draw")
        decorator = " ".join(rest[draw_end+1:])
    else:
        drawpen = parse_pen(" ".join(rest), "draw")
    return Draw(path, drawpen, fillpen, decorator)

class Parser:
    """
    a class representing the expression parser
    """
    def __init__(self, size="9cm"):
        self.expr = []
        self.size = size
    def add_line(self, cmd: str):
        """
        add a line to the parser
        """
        if re.fullmatch(r"size\([^\t\r\n]*\);", cmd):
            self.size = cmd[len("size(") : -len(");")]
            return
        try:
            point_expr = parse_point(cmd)
            self.expr.append(point_expr)
        except (SyntaxError, IndexError, ValueError):
            try:
                draw_expr = parse_draw(cmd)
                self.expr.append(draw_expr)
            except (SyntaxError, IndexError, ValueError):
                self.expr.append(AsyCmd(cmd))
    def compute_label(self, debug_mode=False):
        """
        use "label_calculator.asy" to compute the label
        """
        #generate buffer code
        points_to_label = []
        paths = []
        buffer = f"size({self.size});\n"
        buffer += "import olympiad;\n"
        buffer += "import geometry;\n"
        for expr in self.expr:
            if isinstance(expr, Draw):
                paths.append(expr.path)
            else:
                buffer += expr.emit() + "\n"
                if isinstance(expr, Point) and (not expr.label_dir):
                    points_to_label.append(expr.name)
        buffer += "path[] paths = {" + ", ".join(paths) + "};\n"
        buffer += "pair[] points_to_label = {" + ", ".join(points_to_label) + "};\n"
        with open("buffer.asy", "w", -1, "utf-8") as file:
            file.write(buffer)
        os.system("asy -f pdf label_calculator.asy > labels_output.txt")
        with open("labels_output.txt", "r", -1, "utf-8") as file:
            for expr in self.expr:
                if isinstance(expr, Point) and (not expr.label_dir):
                    expr.label_dir = file.readline()[:-1]
        if not debug_mode:
            os.system("rm buffer.asy label_calculator.pdf labels_output.txt")

    def emit_results(self):
        """
        emit the results
        """
        res = f"size({self.size});\n"
        res += "import olympiad;\n"
        res += "import geometry;\n"
        for i in range(1,4):
            for expr in self.expr:
                if cmd := expr.emit(i):
                    res += cmd + "\n"
        return res

if __name__ == "__main__":
    parser = Parser()
    FILENAME = sys.argv[1]
    with open(FILENAME, "r", -1, "utf-8") as f:
        content = f.read()
    for line in content.split("\n"):
        parser.add_line(line)
    parser.compute_label()
    print(parser.emit_results())
