"""
Ashish's Calculator - Core Engine & Natural Language Voice Command Processor
Preserves all original operations (+, -, *, /) and division-by-zero protection.
"""

import re
import math

def calculate(a, op, b):
    """
    Core calculation engine for Ashish's Calculator.
    Preserves all original arithmetic logic and zero-division checks.
    """
    try:
        a_num = float(a)
        b_num = float(b)
    except (ValueError, TypeError):
        return "invalid input"

    if op == "+":
        res = a_num + b_num
    elif op == "-":
        res = a_num - b_num
    elif op == "*":
        res = a_num * b_num
    elif op == "/":
        if b_num != 0:
            res = a_num / b_num
        else:
            return "cannot divide"
    else:
        return "invalid input"

    if isinstance(res, float) and res.is_integer():
        return int(res)
    return res

def words_to_number_string(text):
    """
    Converts English number words in text to digit strings.
    E.g. 'five' -> '5', 'twenty five' -> '25', 'one hundred' -> '100'.
    """
    units = {
        'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4,
        'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9,
        'ten': 10, 'eleven': 11, 'twelve': 12, 'thirteen': 13,
        'fourteen': 14, 'fifteen': 15, 'sixteen': 16, 'seventeen': 17,
        'eighteen': 18, 'nineteen': 19
    }
    tens = {
        'twenty': 20, 'thirty': 30, 'forty': 40, 'fifty': 50,
        'sixty': 60, 'seventy': 70, 'eighty': 80, 'ninety': 90
    }
    scales = {'hundred': 100, 'thousand': 1000, 'million': 1000000}

    tokens = text.split()
    output_tokens = []
    i = 0
    while i < len(tokens):
        w = tokens[i].lower()
        if w in units or w in tens:
            current_val = 0
            has_scale = False
            while i < len(tokens):
                curr = tokens[i].lower()
                if curr in units:
                    current_val += units[curr]
                    i += 1
                elif curr in tens:
                    current_val += tens[curr]
                    i += 1
                elif curr in scales:
                    if current_val == 0:
                        current_val = 1
                    current_val *= scales[curr]
                    has_scale = True
                    i += 1
                elif curr == 'and' and has_scale and i + 1 < len(tokens) and (tokens[i+1].lower() in units or tokens[i+1].lower() in tens):
                    i += 1
                elif curr in ['point', 'dot'] and i + 1 < len(tokens) and tokens[i+1].lower() in units:
                    i += 1
                    decimals = []
                    while i < len(tokens) and tokens[i].lower() in units:
                        decimals.append(str(units[tokens[i].lower()]))
                        i += 1
                    current_val = float(f"{current_val}.{''.join(decimals)}")
                    break
                else:
                    break
            output_tokens.append(str(current_val))
        else:
            output_tokens.append(tokens[i])
            i += 1
    return " ".join(output_tokens)

def parse_voice_command(text):
    """
    Parses voice/natural language math queries into operands and operators,
    or returns special actions like 'clear', 'delete', 'play_audio'.
    Examples:
      - 'what is 25 plus 75' -> (25.0, '+', 75.0)
      - 'add five and ten' -> (5.0, '+', 10.0)
      - 'subtract 5 from 20' -> (20.0, '-', 5.0)
      - 'calculate 144 divided by 12' -> (144.0, '/', 12.0)
      - 'multiply 65 by 4' -> (65.0, '*', 4.0)
      - 'what is 15 percent of 2600' -> (2600.0, '*', 0.15)
      - 'clear the calculator' -> 'clear'
      - 'delete the last digit' -> 'delete'
    """
    if not text:
        return None

    clean = text.lower().strip()
    clean = words_to_number_string(clean)

    # Audio Controls
    if any(k in clean for k in ["play audio", "play music", "play bgm", "start audio", "start music", "unmute"]):
        return {"action": "play_audio"}
    if any(k in clean for k in ["stop audio", "stop music", "pause audio", "pause music", "mute"]):
        return {"action": "pause_audio"}
    if any(k in clean for k in ["500 volume", "volume 500", "500% volume", "500 percent volume", "max volume", "full volume"]):
        return {"action": "volume_500"}

    # Calculator Commands
    if any(k in clean for k in ["clear", "reset", "wipe", "all clear"]):
        return {"action": "clear"}
    if any(k in clean for k in ["delete", "backspace", "remove last", "undo", "remove digit"]):
        return {"action": "delete"}

    # Constants
    if clean in ["what is pi", "value of pi", "pi"]:
        return {"action": "direct_result", "res": round(math.pi, 6), "display": "π"}
    if clean in ["what is e", "value of e", "euler"]:
        return {"action": "direct_result", "res": round(math.e, 6), "display": "e"}

    # Square root & Cube root
    sqrt_match = re.search(r'(?:square\s*root\s*of|root\s*of|sqrt\s*of)\s*(\d+(?:\.\d+)?)', clean)
    if sqrt_match:
        val = float(sqrt_match.group(1))
        return {"action": "direct_result", "res": math.isqrt(int(val)) if val.is_integer() and math.isqrt(int(val))**2 == int(val) else round(math.sqrt(val), 6), "display": f"√{val}"}

    cbrt_match = re.search(r'(?:cube\s*root\s*of|cbrt\s*of)\s*(\d+(?:\.\d+)?)', clean)
    if cbrt_match:
        val = float(cbrt_match.group(1))
        return {"action": "direct_result", "res": round(val ** (1.0/3.0), 6), "display": f"³√{val}"}

    # Square & Cube
    sq_match = re.search(r'(?:square\s*of)\s*(\d+(?:\.\d+)?)', clean) or re.search(r'(\d+(?:\.\d+)?)\s*squared', clean)
    if sq_match:
        val = float(sq_match.group(1))
        return {"action": "direct_result", "res": int(val**2) if val.is_integer() else val**2, "display": f"{val}²"}

    cube_match = re.search(r'(?:cube\s*of)\s*(\d+(?:\.\d+)?)', clean) or re.search(r'(\d+(?:\.\d+)?)\s*cubed', clean)
    if cube_match:
        val = float(cube_match.group(1))
        return {"action": "direct_result", "res": int(val**3) if val.is_integer() else val**3, "display": f"{val}³"}

    # Powers: X to the power of Y
    pow_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:to\s*the\s*power\s*of|power\s*of|raised\s*to|\^)\s*(\d+(?:\.\d+)?)', clean)
    if pow_match:
        a_val = float(pow_match.group(1))
        b_val = float(pow_match.group(2))
        res = a_val ** b_val
        return {"action": "direct_result", "res": int(res) if res.is_integer() else round(res, 6), "display": f"{a_val}^{b_val}"}

    # Fractions / Shortcuts: half, double, triple, third, quarter
    half_match = re.search(r'(?:half\s*of)\s*(\d+(?:\.\d+)?)', clean)
    if half_match:
        val = float(half_match.group(1))
        res = val / 2.0
        return {"action": "direct_result", "res": int(res) if res.is_integer() else res, "display": f"half of {val}"}

    double_match = re.search(r'(?:double\s*of|twice\s*of)\s*(\d+(?:\.\d+)?)', clean)
    if double_match:
        val = float(double_match.group(1))
        res = val * 2.0
        return {"action": "direct_result", "res": int(res) if res.is_integer() else res, "display": f"2 × {val}"}

    triple_match = re.search(r'(?:triple\s*of|thrice\s*of)\s*(\d+(?:\.\d+)?)', clean)
    if triple_match:
        val = float(triple_match.group(1))
        res = val * 3.0
        return {"action": "direct_result", "res": int(res) if res.is_integer() else res, "display": f"3 × {val}"}

    third_match = re.search(r'(?:one\s*third\s*of|third\s*of)\s*(\d+(?:\.\d+)?)', clean)
    if third_match:
        val = float(third_match.group(1))
        res = val / 3.0
        return {"action": "direct_result", "res": round(res, 6), "display": f"{val} ÷ 3"}

    quarter_match = re.search(r'(?:one\s*fourth\s*of|quarter\s*of)\s*(\d+(?:\.\d+)?)', clean)
    if quarter_match:
        val = float(quarter_match.group(1))
        res = val / 4.0
        return {"action": "direct_result", "res": int(res) if res.is_integer() else res, "display": f"{val} ÷ 4"}

    # Trigonometry (in degrees)
    sin_match = re.search(r'(?:sin|sine)\s*(?:of)?\s*(\d+(?:\.\d+)?)', clean)
    if sin_match:
        deg = float(sin_match.group(1))
        res = round(math.sin(math.radians(deg)), 6)
        return {"action": "direct_result", "res": int(res) if res.is_integer() else res, "display": f"sin({deg}°)"}

    cos_match = re.search(r'(?:cos|cosine)\s*(?:of)?\s*(\d+(?:\.\d+)?)', clean)
    if cos_match:
        deg = float(cos_match.group(1))
        res = round(math.cos(math.radians(deg)), 6)
        return {"action": "direct_result", "res": int(res) if res.is_integer() else res, "display": f"cos({deg}°)"}

    tan_match = re.search(r'(?:tan|tangent)\s*(?:of)?\s*(\d+(?:\.\d+)?)', clean)
    if tan_match:
        deg = float(tan_match.group(1))
        res = round(math.tan(math.radians(deg)), 6)
        return {"action": "direct_result", "res": int(res) if res.is_integer() else res, "display": f"tan({deg}°)"}

    # Logarithms / Factorial / Absolute Value
    log_match = re.search(r'(?:log|logarithm)\s*(?:of)?\s*(\d+(?:\.\d+)?)', clean)
    if log_match:
        val = float(log_match.group(1))
        res = round(math.log10(val), 6)
        return {"action": "direct_result", "res": int(res) if res.is_integer() else res, "display": f"log₁₀({val})"}

    ln_match = re.search(r'(?:natural\s*log|ln)\s*(?:of)?\s*(\d+(?:\.\d+)?)', clean)
    if ln_match:
        val = float(ln_match.group(1))
        res = round(math.log(val), 6)
        return {"action": "direct_result", "res": int(res) if res.is_integer() else res, "display": f"ln({val})"}

    fact_match = re.search(r'(?:factorial\s*of)\s*(\d+)', clean) or re.search(r'(\d+)\s*factorial', clean)
    if fact_match:
        n = int(fact_match.group(1))
        return {"action": "direct_result", "res": math.factorial(min(n, 100)), "display": f"{n}!"}

    abs_match = re.search(r'(?:absolute\s*(?:value)?\s*of|abs\s*of)\s*(-?\d+(?:\.\d+)?)', clean)
    if abs_match:
        val = float(abs_match.group(1))
        res = abs(val)
        return {"action": "direct_result", "res": int(res) if res.is_integer() else res, "display": f"|{val}|"}

    # Percentages: off / discount / tax
    pct_off_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:%|percent)\s*(?:off|discount\s*on)\s*(\d+(?:\.\d+)?)', clean)
    if pct_off_match:
        p = float(pct_off_match.group(1))
        b = float(pct_off_match.group(2))
        res = b - (p / 100.0 * b)
        return {"action": "direct_result", "res": int(res) if res.is_integer() else round(res, 4), "display": f"{b} - {p}%"}

    pct_tax_match = re.search(r'(?:add\s*)?(\d+(?:\.\d+)?)\s*(?:%|percent)\s*(?:tax\s*to|to)\s*(\d+(?:\.\d+)?)', clean)
    if pct_tax_match:
        p = float(pct_tax_match.group(1))
        b = float(pct_tax_match.group(2))
        res = b + (p / 100.0 * b)
        return {"action": "direct_result", "res": int(res) if res.is_integer() else round(res, 4), "display": f"{b} + {p}%"}

    # Percent pattern: e.g. "what is 15 percent of 2600"
    pct_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:%|percent)\s*(?:of)?\s*(\d+(?:\.\d+)?)', clean)
    if pct_match:
        pct_val = float(pct_match.group(1))
        base_val = float(pct_match.group(2))
        return {
            "action": "calculate",
            "a": base_val,
            "op": "*",
            "b": pct_val / 100.0,
            "display": f"{pct_val}% of {base_val}"
        }

    # "add X and Y" / "add X to Y"
    add_match = re.search(r'(?:add|sum\s*of)\s*(\d+(?:\.\d+)?)\s*(?:and|to|\+)\s*(\d+(?:\.\d+)?)', clean)
    if add_match:
        a_val = float(add_match.group(1))
        b_val = float(add_match.group(2))
        return {
            "action": "calculate",
            "a": a_val,
            "op": "+",
            "b": b_val,
            "display": f"{a_val} + {b_val}"
        }

    # "subtract X from Y" -> Y - X
    sub_from_match = re.search(r'(?:subtract|take|minus)\s*(\d+(?:\.\d+)?)\s*(?:from)\s*(\d+(?:\.\d+)?)', clean)
    if sub_from_match:
        sub_val = float(sub_from_match.group(1))
        base_val = float(sub_from_match.group(2))
        return {
            "action": "calculate",
            "a": base_val,
            "op": "-",
            "b": sub_val,
            "display": f"{base_val} - {sub_val}"
        }

    # "multiply X by Y" or "multiply X and Y"
    mul_match = re.search(r'(?:multiply|product\s*of)\s*(\d+(?:\.\d+)?)\s*(?:by|and|\*)\s*(\d+(?:\.\d+)?)', clean)
    if mul_match:
        return {
            "action": "calculate",
            "a": float(mul_match.group(1)),
            "op": "*",
            "b": float(mul_match.group(2)),
            "display": f"{mul_match.group(1)} × {mul_match.group(2)}"
        }

    # "divide X by Y" or "divide X and Y"
    div_match = re.search(r'(?:divide)\s*(\d+(?:\.\d+)?)\s*(?:by|over|into|and|/)\s*(\d+(?:\.\d+)?)', clean)
    if div_match:
        return {
            "action": "calculate",
            "a": float(div_match.group(1)),
            "op": "/",
            "b": float(div_match.group(2)),
            "display": f"{div_match.group(1)} ÷ {div_match.group(2)}"
        }

    # Infix patterns: e.g. "25 plus 75", "144 divided by 12", "65 times 4", "10 + 20"
    infix_match = re.search(r'(\d+(?:\.\d+)?)\s*(plus|\+|add|added\s*to|minus|\-|subtract|subtracted\s*by|times|\*|into|multiplied\s*by|divided\s*by|over|/)\s*(\d+(?:\.\d+)?)', clean)
    if infix_match:
        a_val = float(infix_match.group(1))
        op_word = infix_match.group(2)
        b_val = float(infix_match.group(3))

        if any(w in op_word for w in ["plus", "+", "add"]):
            op = "+"
        elif any(w in op_word for w in ["minus", "-", "sub"]):
            op = "-"
        elif any(w in op_word for w in ["times", "*", "into", "mul"]):
            op = "*"
        elif any(w in op_word for w in ["div", "/", "over"]):
            op = "/"
        else:
            op = "+"

        return {
            "action": "calculate",
            "a": a_val,
            "op": op,
            "b": b_val,
            "display": f"{a_val} {op} {b_val}"
        }

    return None

if __name__ == "__main__":
    import sys
    # If run with command line argument or interactive voice test
    if len(sys.argv) > 1 and sys.argv[1] == "--voice":
        print("Voice Command Mode (Type or simulate voice input):")
        cmd = input("Speak command: ")
        res = parse_voice_command(cmd)
        if res:
            if res["action"] == "calculate":
                ans = calculate(res["a"], res["op"], res["b"])
                print(f"Recognized: {res['display']} = {ans}")
            else:
                print(f"Action: {res['action']}")
        else:
            print("Could not understand voice command.")
    else:
        # Exact original interactive script preserved
        a = int(input("enter the number: "))
        op = input("enter your choice(+,-,*,/): ")
        b = int(input("enter the second number: "))
        if op == "+":
            print(a+b)
        elif op == "-":
            print(a-b)
        elif op == "*":
            print(a*b)
        elif op == "/":
            if b!=0:
                print(a/b)
            else:
                print("cannot divide")
        else:
            print("invalid input")