import requests
import json

def process_user_input(user_input):
    """
    使用 Ollama 模型解析使用者輸入，提取關鍵詞、地點、時間等資訊，返回結構化的資料。
    """
    url = "http://localhost:11434/api/generate"  
    prompt = f"""
請分析以下使用者輸入，提取其中的每個活動，提取其關鍵資訊，包括時間段（如早上、中午、晚上）、關鍵詞、地點、時間等。請將結果以 JSON 格式輸出，結構如下：
{{
    "activities": [
        {{
            "time_period": "<時間段>",
            "keywords": ["<關鍵詞列表>"],
            "locations": ["<地點列表>"],
            "times": ["<時間資訊列表>"]
        }},
        // 更多活動...
    ]
}}


使用者輸入："{user_input}"

請提供上述格式的JSON輸出，不要添加額外的文字解釋。
"""

    payload = {
        "model": "llama3.2",  # 替換為實際使用的模型名稱
        "prompt": prompt,
        "temperature": 0.5,
        "max_tokens": 450
    }


    try:
        # 使用 stream=True 處理回應
        response = requests.post(url, json=payload, stream=True)
        if response.status_code == 200:
            full_response = ''
            for line in response.iter_lines():
                if line:
                    # 解析每一行的JSON
                    data = json.loads(line.decode('utf-8'))
                    # 累積已生成文本
                    full_response += data.get('response', '')
                    # 檢查是否完成
                    if data.get('done', False):
                        break
            # 去除前後空白
            full_response = full_response.strip()
            # 解析模型返回的 JSON
            result = json.loads(full_response)
            return result
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None
    except json.JSONDecodeError as e:
        print(f"JSON 解析錯誤: {e}")
        print("模型輸出内容：", full_response)
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    user_input = input("請輸入您的旅遊需求：")
    parsed_result = process_user_input(user_input)
    if parsed_result:
        print("解析結果：")
        print(json.dumps(parsed_result, ensure_ascii=False, indent=4))
    else:
        print("無法解析使用者輸入。")
