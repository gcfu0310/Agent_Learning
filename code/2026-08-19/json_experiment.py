import json


ALLOWED_CATEGORIES = {"技术问题", "生活问题", "其他"}
REQUIRED_FIELDS = {"category", "confidence", "reason"}


def validate_output(raw_output: str) -> dict:
    # 1. JSON 解析
    try:
        data = json.loads(raw_output)
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON_PARSE_ERROR: {e}") from e

    if not isinstance(data, dict):
        raise ValueError("TYPE_ERROR: 最外层必须是对象")

    # 2. 必填字段
    missing_fields = REQUIRED_FIELDS - data.keys()
    if missing_fields:
        raise ValueError(
            f"MISSING_FIELD_ERROR: 缺少字段 {sorted(missing_fields)}"
        )

    # 3. 类型检查
    if not isinstance(data["category"], str):
        raise ValueError("TYPE_ERROR: category 必须是字符串")

    confidence = data["confidence"]
    if isinstance(confidence, bool) or not isinstance(confidence, (int, float)):
        raise ValueError("TYPE_ERROR: confidence 必须是数值")

    if not isinstance(data["reason"], str):
        raise ValueError("TYPE_ERROR: reason 必须是字符串")

    # 4. 业务规则
    if data["category"] not in ALLOWED_CATEGORIES:
        raise ValueError(
            f"BUSINESS_RULE_ERROR: 不支持的 category={data['category']}"
        )

    if not 0 <= confidence <= 1:
        raise ValueError(
            f"BUSINESS_RULE_ERROR: confidence 必须在 0～1，实际为 {confidence}"
        )

    if not data["reason"].strip():
        raise ValueError("BUSINESS_RULE_ERROR: reason 不能为空")

    return data


def run_business(raw_output: str) -> None:
    print("\n原始输出：", raw_output)

    try:
        result = validate_output(raw_output)
    except ValueError as e:
        print("校验失败：", e)
        print("停止后续业务")
        return

    print("校验通过：", result)
    print("进入后续业务")


test_cases = {
    "正常输入": '''
        {
            "category": "技术问题",
            "confidence": 0.9,
            "reason": "问题与 Python 编程有关"
        }
    ''',

    "非法 JSON": '''
        {
            "category": "技术问题",
            "confidence": 0.9,
        }
    ''',

    "缺少字段": '''
        {
            "category": "技术问题",
            "confidence": 0.9
        }
    ''',

    "类型错误": '''
        {
            "category": "技术问题",
            "confidence": "0.9",
            "reason": "问题与 Python 编程有关"
        }
    ''',

    "置信度越界": '''
        {
            "category": "技术问题",
            "confidence": 1.5,
            "reason": "问题与 Python 编程有关"
        }
    ''',

    "非法类别": '''
        {
            "category": "财经问题",
            "confidence": 0.8,
            "reason": "问题与股票有关"
        }
    '''
}


for case_name, raw_output in test_cases.items():
    print(f"\n{'=' * 20} {case_name} {'=' * 20}")
    run_business(raw_output)

"""
实验记录:
(Agent) PS D:\Agent-Learning> python D:\Agent-Learning\code\2026-08-19\json_experiment.py

==================== 正常输入 ====================

原始输出： 
        {
            "category": "技术问题",
            "confidence": 0.9,
            "reason": "问题与 Python 编程有关"
        }
    
校验通过： {'category': '技术问题', 'confidence': 0.9, 'reason': '问题与 Python 编程有关'}
进入后续业务

==================== 非法 JSON ====================

原始输出： 
        {
            "category": "技术问题",
            "confidence": 0.9,
        }
    
校验失败： JSON_PARSE_ERROR: Illegal trailing comma before end of object: line 4 column 30 (char 72)
停止后续业务

==================== 缺少字段 ====================

原始输出： 
        {
            "category": "技术问题",
            "confidence": 0.9
        }
    
校验失败： MISSING_FIELD_ERROR: 缺少字段 ['reason']
停止后续业务

==================== 类型错误 ====================

原始输出： 
        {
            "category": "技术问题",
            "confidence": "0.9",
            "reason": "问题与 Python 编程有关"
        }
    
校验失败： TYPE_ERROR: confidence 必须是数值
停止后续业务

==================== 置信度越界 ====================

原始输出： 
        {
            "category": "技术问题",
            "confidence": 1.5,
            "reason": "问题与 Python 编程有关"
        }
    
校验失败： BUSINESS_RULE_ERROR: confidence 必须在 0～1，实际为 1.5
停止后续业务

==================== 非法类别 ====================

原始输出： 
        {
            "category": "财经问题",
            "confidence": 0.8,
            "reason": "问题与股票有关"
        }
    
校验失败： BUSINESS_RULE_ERROR: 不支持的 category=财经问题
停止后续业务

"""