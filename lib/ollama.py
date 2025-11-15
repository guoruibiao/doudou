import requests

class OllamaClient:
    def __init__(self, base_url="http://localhost:11434", timeout=60):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()

        # 初始化时检查服务状态
        if not self._check_service():
            print("⚠️  OLLama服务未运行，请先启动服务")

    def _check_service(self):
        """检查服务状态"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False

    def list_models(self):
        """获取模型列表 - 使用正确的API端点"""
        try:
            response = self.session.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                return response.json()
            else:
                print(f"获取模型列表失败，状态码: {response.status_code}")
                return None
        except Exception as e:
            print(f"获取模型列表错误: {e}")
            return None

    def generate_text(self, model, prompt, **kwargs):
        """
        生成文本 - 修复的版本
        注意：确保模型名称正确
        """
        url = f"{self.base_url}/api/generate"

        # 构建请求数据
        data = {
            "model": model,
            "prompt": prompt,
            "stream": False
        }

        # 添加可选参数
        if 'temperature' in kwargs:
            data['options'] = {'temperature': kwargs['temperature']}

        try:
            print(f"发送请求到: {url}")
            print(f"使用模型: {model}")
            print(f"提示词: {prompt[:50]}...")

            response = self.session.post(
                url,
                json=data,
                timeout=self.timeout
            )

            print(f"响应状态码: {response.status_code}")

            if response.status_code == 200:
                if response.json().get('response', "") != "":
                    return response.json()['response']
            elif response.status_code == 404:
                print("❌ 404错误: 可能是模型名称不正确或API端点变化")
                print("请检查:")
                print("1. 模型名称是否正确")
                print("2. Ollama服务版本")
                return None
            else:
                print(f"❌ 请求失败，状态码: {response.status_code}")
                print(f"响应内容: {response.text}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"❌ 请求异常: {e}")
            return None

    def chat_completion(self, model, messages, **kwargs):
        """聊天补全"""
        url = f"{self.base_url}/api/chat"

        data = {
            "model": model,
            "messages": messages,
            "stream": False
        }

        try:
            response = self.session.post(url, json=data, timeout=self.timeout)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"聊天请求失败，状态码: {response.status_code}")
                return None
        except Exception as e:
            print(f"聊天请求错误: {e}")
            return None