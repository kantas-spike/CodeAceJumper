import json
import re
import argparse
from pathlib import Path

CHAR_REGEX_MAP_KEY = "aceJump.finder.charRegexMap"


def check_json(json_file: Path):
    data = json.loads(json_file.read_text(encoding="utf-8"))
    char_regex_map = data[CHAR_REGEX_MAP_KEY]

    ALPHABET_RE = re.compile(r"[A-Za-z]")

    bad_pattern = {}
    for key, pattern in char_regex_map.items():
        found = set(ALPHABET_RE.findall(pattern))
        key_variants = {key.lower(), key.upper()}
        others = found - key_variants
        if others:
            bad_pattern[key] = list(others)

    return bad_pattern


def fix_regex(args, bad_pattern: dict):
    data = json.loads(args.json.read_text(encoding="utf-8"))
    char_map = data.get(CHAR_REGEX_MAP_KEY, {})
    fixed_map = {}
    for key, pattern in char_map.items():
        others = bad_pattern.get(key, [])
        if others:
            # remove each offending character from the regex pattern
            new_pattern = pattern
            for ch in others:
                # escape the character for literal removal
                new_pattern = new_pattern.replace(ch, "")
            fixed_map[key] = new_pattern
        else:
            fixed_map[key] = pattern

    return {CHAR_REGEX_MAP_KEY: fixed_map}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="アルファベット・正規表現対応表の内容をチェックする"
    )
    parser.add_argument(
        "json",
        metavar="regexmap.json",
        type=Path,
        help="アルファベット・正規表現対応表",
    )
    parser.add_argument(
        "-c",
        "--check",
        action="store_true",
        default=False,
        help="正規表現のグループに、キーとなるアルファベット以外のアルファベットが含まれているかチェックする",
    )
    parser.add_argument(
        "-x",
        "--fix",
        action="store_true",
        help="正規表現のグループから不要文字を除去し、修正結果を出力する",
    )

    args = parser.parse_args()
    # print(args)
    if args.check:
        bad_pattern = check_json(args.json)
        if bad_pattern:
            print("正規表現にキーと異なるアルファベットが含まれています。")
            print(json.dumps(bad_pattern, indent=2))
        else:
            print("正規表現にキーと異なるアルファベットは含まれていません。")
    # If removal requested, apply regex changes and write back
    if args.fix:
        bad_pattern = check_json(args.json)
        if bad_pattern:
            fixed_map = fix_regex(args, bad_pattern)
            if fixed_map:
                print(json.dumps(fixed_map, ensure_ascii=False, indent=2))
