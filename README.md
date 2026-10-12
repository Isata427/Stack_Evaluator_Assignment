# Stack-Based Expression Evaluator (DCOMP320)

## How to run
1. Install Python 3.
2. Put `stack_evaluator.py` and `input.txt` in the same folder.
3. Run: `python stack_evaluator.py`
4. Open `output.txt` to see the results.

## Input format
- One expression per line, e.g. `(8 / 4) + 7 * 2`
- Expressions are separated by a line made only of dashes, e.g. `-----`

## Output format
- Same layout as the input: each expression is replaced by its result.
- Separator lines are copied unchanged.
- A bad expression gives a line like `Error: division by zero`.

## Supported
Numbers (including decimals and negatives), `+ - * /`, brackets, normal precedence.

## Assumptions and limitations
- Each expression is on one line.
- No exponents, functions (e.g. sqrt) or implicit multiplication like `2(3+4)`.
- Whole-number results are shown without `.0`; other results are rounded to 4 decimal places.