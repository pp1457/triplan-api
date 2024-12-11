# \triplan-api> python3 .\triplan_api\utils\process_user_input.py

import requests
import json

# Return type: Dict{key: "morning", "night"..., value: "List[str]"}
def process_user_input(user_input):
    """
    解析使用者輸入的旅遊需求，提取並分類關鍵字，結構化輸出。
    """
    url = "http://meow1.csie.ntu.edu.tw:11434/api/generate"
    model_name = "llama3.2"

    # Prompt 設計
    prompt = f"""
請分析使用者輸入的旅遊需求，提取多個短小的關鍵字，結果按以下行程階段組織：breakfast、morning、lunch、afternoon、dinner、night。
飲食、餐廳相關的關鍵字分到breakfast、lunch、dinner。
早餐相關的關鍵字請分到breakfast，午餐相關的關鍵字請分到lunch，晚餐相關的關鍵字請分到dinner。
非飲食活動且旅遊相關的關鍵字，請按照早上、下午、晚上，分別分到morning、afternoon、night。
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

請直接輸出 JSON 結果，不要添加額外的文字解釋。
"""

    payload = {
        "model": model_name,
        "prompt": prompt,
        "temperature": 0.5,
        "max_tokens": 450
    }

    try:
        # 發送 POST 請求
        response = requests.post(url, json=payload, stream=True)
        
        if response.status_code == 200:
            full_response = ""
            
            # 逐行處理流式數據
            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line.decode("utf-8"))
                        full_response += data.get("response", "")
                        if data.get("done", False):  # 偵測完成標記
                            break
                    except json.JSONDecodeError as e:
                        print(f"流數據解析錯誤：{e}")
                        continue
            
            # 清理返回內容並嘗試解析完整 JSON
            full_response = full_response.strip().strip("`")
            try:
                result = json.loads(full_response)
            except json.JSONDecodeError as e:
                print(f"完整 JSON 解析錯誤: {e}")
                print("模型返回的內容：", full_response)
                return None
            
        else:
            print(f"API 回應錯誤，狀態碼：{response.status_code}")
            print("返回內容：", response.text)
            return None
        
    except requests.RequestException as e:
        print(f"發生網絡錯誤：{e}")
        return None
    
    except Exception as e:
        print(f"發生未知錯誤：{e}")
        return None

    # 初始化指定的鍵和值
    result_dict = {
        "breakfast": [],
        "morning": [],
        "lunch": [],
        "afternoon": [],
        "dinner": [],
        "night": []
    }

    # 填充字典
    for activity in result.get("activities", []):
        time_period = activity.get("time_period")
        keywords = activity.get("keywords", [])
        if time_period in result_dict:
            result_dict[time_period].extend(keywords)

    return result_dict

##############################################################

def activity_to_text(activities, option):
    """
    將活動轉為搜尋關鍵字。
    
    :param activities: 字典，包含六個時間段的活動列表 (breakfast、morning、lunch、afternoon、dinner、night)
    :param option: 數字，1-6，指定需要輸出的時間段
    :return: 字串，包含時間段的中文名稱及活動
    """
    # 時間段對應的中文名稱
    time_period_map = {
        1: "早餐",
        2: "上午",
        3: "午餐",
        4: "下午",
        5: "晚餐",
        6: "晚上"
    }
    
    # 時間段對應的字典鍵
    time_period_keys = {
        1: "breakfast",
        2: "morning",
        3: "lunch",
        4: "afternoon",
        5: "dinner",
        6: "night"
    }
    
    # 驗證 option 是否有效
    if option not in time_period_map:
        raise ValueError("Invalid option. Option must be a number between 1 and 6.")
    
    # 獲取對應的時間段名稱和活動
    time_period_name = time_period_map[option]
    time_period_key = time_period_keys[option]
    activity_list = activities.get(time_period_key, [])
    
    # 組合輸出字串
    return f"{time_period_name} {' '.join(activity_list)}"

##############################################################

if __name__ == "__main__":
    print("請輸入您的旅遊需求：")
    user_input = input()
    result_dict = process_user_input(user_input)
    if result_dict:
        print(result_dict)
        for option in range(1, 7):
            result_text = activity_to_text(result_dict, option)
            print(result_text)
    else:
        print("無法解析使用者輸入。")
