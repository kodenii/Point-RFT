# Copyright 2024 Bytedance Ltd. and/or its affiliates
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re

from mathruler.grader import extract_boxed_content, grade_answer

def get_answer(text):
    pattern = r'<answer>(.*?)</answer>(?!.*<answer>)'
    
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

def math_format_reward(predict_str: str) -> float:
    pattern = re.compile(r"<think>.*</think>.*\\boxed\{.*\}.*", re.DOTALL)
    format_match = re.fullmatch(pattern, predict_str)
    return 1.0 if format_match else 0.0

def format_reward(predict_str: str) -> float:
    """Reward function that checks if the completion has a specific format."""
    pattern = r"<think>.*?</think>\s*<answer>.*?</answer>"
    match = re.fullmatch(pattern, predict_str, re.DOTALL)
    return 1.0 if match else 0.0

def relaxed_correctness(prediction, target, max_relative_change: float = 0.05) -> bool:

    def _to_float(text: str):
        text = text.replace(",", "").replace("$", "")
        try:
            if text.endswith("%"):
                # Convert percentages to floats.
                return float(text.rstrip("%")) / 100.0
            else:
                return float(text)
        except ValueError:
            return None
        
    num_map = {
        "zero": 0,
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "ten": 10,
    }
    if prediction is None or target is None:
        return False
    if prediction.lower() in num_map:
        prediction = str(num_map[prediction.lower()])
    if target.lower() in num_map:
        target = str(num_map[target.lower()])

    prediction_float = _to_float(prediction)
    target_float = _to_float(target)
    if prediction_float is not None and target_float:
        if prediction.replace(",", "").replace("%", "").replace("$", "") == target.replace(",", "").replace("%", "").replace("$", ""):
            return True
        relative_change = abs(prediction_float - target_float) / abs(target_float)
        return relative_change <= max_relative_change
    else:
        return prediction.lower() == target.lower()

#def math_acc_reward(predict_str: str, ground_truth: str) -> float:
#    answer = extract_boxed_content(predict_str)
#    return 1.0 if grade_answer(answer, ground_truth) else 0.0

def math_acc_reward(predict_str: str, ground_truth: str) -> float:
    answer = get_answer(predict_str)
    return 1.0 if relaxed_correctness(answer, ground_truth) else 0.0

#def math_compute_score(predict_str: str, ground_truth: str) -> float:
#    return 0.9 * math_acc_reward(predict_str, ground_truth) + 0.1 * math_format_reward(predict_str)

def math_compute_score(predict_str: str, ground_truth: str) -> float:
    return 0.9 * math_acc_reward(predict_str, ground_truth) + 0.1 * format_reward(predict_str)
