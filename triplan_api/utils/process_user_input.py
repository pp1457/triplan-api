import requests
import json

def process_user_input(user_input):
    """
    解析使用者輸入的旅遊需求，提取並分類關鍵字，結構化輸出。
    """
    url = "http://localhost:11434/api/generate"
    model_name = "llama3.2"

    # Prompt 設計
    prompt = f"""
請分析使用者輸入的旅遊需求，提取多個短小的關鍵字，結果按以下行程階段組織：breakfast、morning、lunch、afternoon、dinner、night。
飲食、用餐、餐廳相關的請分到breakfast、lunch、dinner；旅遊相關的請分到；morning、afternoon、night。
morning相關的請分到breakfast、morning；中午afternoon相關的請分到lunch、afternoon；night相關的請分到dinner、night。
若無相關內容，則關鍵字欄位維持空白。
JSON 結構範例如下：
{{
    "activities": [
        {{
            "time_period": "breakfast",
            "keywords": ["<關鍵字列表>"]
        }},
        {{
            "time_period": "morning",
            "keywords": ["<關鍵字列表>"]
        }},
        {{
            "time_period": "lunch",
            "keywords": ["<關鍵字列表>"]
        }},
        {{
            "time_period": "afternoon",
            "keywords": ["<關鍵字列表>"]
        }},
        {{
            "time_period": "dinner",
            "keywords": ["<關鍵字列表>"]
        }},
        {{
            "time_period": "night",
            "keywords": ["<關鍵字列表>"]
        }}
    ]
}}

使用者輸入："{user_input}"

請直接輸出 JSON 結果，不要添加額外的文字解釋，且不要把meal丟進morning, afternoon, night。
"""

    payload = {
        "model": model_name,
        "prompt": prompt,
        "temperature": 0.5,
        "max_tokens": 450
    }

    try:
        response = requests.post(url, json=payload, stream=True)
        if response.status_code == 200:
            full_response = ""
            for line in response.iter_lines():
                if line:
                    data = json.loads(line.decode("utf-8"))
                    full_response += data.get("response", "")
                    if data.get("done", False):
                        break

            # 去除多餘字符並解析 JSON
            full_response = full_response.strip().strip("`")
            try:
                result = json.loads(full_response)
                return result
            except json.JSONDecodeError as e:
                print(f"JSON 解析錯誤: {e}")
                print("模型返回的內容：", full_response)
                return None
        else:
            print(f"API 回應錯誤，狀態碼：{response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"發生錯誤：{e}")
        return None



def format_activities(parsed_result):
    """
    將 JSON 結果格式化為簡單的文本格式。
    """
    if not parsed_result or "activities" not in parsed_result:
        return "無法格式化結果，因為輸入的 JSON 結構不正確。"

    formatted_output = ""
    for activity in parsed_result["activities"]:
        time_period = activity.get("time_period", "未知時間段")
        keywords = " ".join(activity.get("keywords", []))
        formatted_output += f"{time_period} {keywords}\n"

    return formatted_output.strip()

if __name__ == "__main__":
    print("請輸入您的旅遊需求：")
    user_input = input()
    parsed_result = process_user_input(user_input)
    if parsed_result:
        print("解析結果（JSON 格式）：")
        print(json.dumps(parsed_result, ensure_ascii=False, indent=4))

        print("\n格式化結果：")
        formatted_output = format_activities(parsed_result)
        print(formatted_output)
    else:
        print("無法解析使用者輸入。")
