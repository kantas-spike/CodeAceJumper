import jinja2
import subprocess
import re

# 環境に合せて以下の2つの値を修正してください。
# 1. MIGEMOの辞書のPATH
MIGEMO_DICT = "/opt/homebrew/Cellar/cmigemo/20110227/share/migemo/utf-8/migemo-dict"
# 2. MIGEMOコマンド
MIGEMO_CMD = f"cmigemo -q --emacs -d {MIGEMO_DICT}"


migemo_dict = {}

# aからzまでの各文字に対して処理（shell=Trueで簡潔に）
for char in range(ord("a"), ord("z") + 1):
    char_str = chr(char)
    cmd = f"echo {char_str} | {MIGEMO_CMD}"
    output = subprocess.check_output(cmd, shell=True, text=True)

    for line in output.splitlines():
        match = re.search(r"^\\\(\[([^\]]+)\]", line)
        if match:
            regex_str = f"[{match.group(1)}]"
            # print(char_str, regex_str)
            migemo_dict[char_str] = regex_str


acejump_config = {"aceJump.finder.charRegexMap": migemo_dict}

# Jinja2テンプレート
env = jinja2.Environment()
env.policies["json.dumps_kwargs"]["ensure_ascii"] = False

template_str = "{{ acejump_config | tojson(indent=2) }}"
template = jinja2.Template(template_str)
output = template.render(acejump_config=acejump_config)

print(output)
