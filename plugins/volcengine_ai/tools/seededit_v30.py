from collections.abc import Generator
from typing import Any
import base64

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.tool import ToolProviderCredentialValidationError
from dify_plugin.file.file import File

from legacy.volc_sdk.VisualService import VisualService


class SeededitV30Tool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        # 初始化视觉服务
        visual_service = VisualService()
        
        # 设置认证信息
        access_key_id = self.runtime.credentials.get("AccessKeyID", "")
        access_key_secret = self.runtime.credentials.get("AccessKeySecret", "")
        
        if not access_key_id or not access_key_secret:
            raise ToolProviderCredentialValidationError("AccessKeyID和AccessKeySecret不能为空")
            
        visual_service.set_ak(access_key_id)
        visual_service.set_sk(access_key_secret)

        # 获取图像文件参数
        image_files: list[File] = tool_parameters.get("image_files", [])
        
        if not image_files:
            raise ToolProviderCredentialValidationError("至少需要提供一个图像文件")
        
        # 初始化图像数据列表
        image_urls = []
        binary_data_base64 = []

        # 处理图像文件
        for image_file in image_files:
            if image_file.url:
                image_urls.append(image_file.url)
            if image_file.blob:
                binary_data_base64.append(
                    base64.b64encode(image_file.blob).decode("utf-8")
                )

        # 验证必需参数
        prompt = tool_parameters.get("prompt", "")
        if not prompt:
            raise ToolProviderCredentialValidationError("prompt参数不能为空")

        # 验证至少有一个输入源
        if not binary_data_base64 and not image_urls:
            raise ToolProviderCredentialValidationError(
                "Either 'binary_data_base64_str', 'image_url', or 'image_file' must be provided."
            )
        
        # 构建请求表单
        form = {
            "req_key": "seededit_v3.0",
            "binary_data_base64": binary_data_base64,
            "image_urls": image_urls,
            "prompt": prompt,
            "seed": tool_parameters.get("seed", -1),
            "scale": tool_parameters.get("scale", 0.5),
            "return_url": tool_parameters.get("return_url", True),
            "logo_info": {
                "add_logo": tool_parameters.get("add_logo", False),
                "position": int(tool_parameters.get("position", 0)),
                "language": int(tool_parameters.get("language", 0)),
                "opacity": tool_parameters.get("opacity", 0.3),
                "logo_text_content": tool_parameters.get("logo_text_content", "Volcengine AI"),
            }
        }
        try:
            response = visual_service.cv_process(form=form)
            code = response.get("code", -1)
            
            if code == 10000:
                data = response.get("data", {})
                
                # 处理图像URL返回
                response_image_urls = data.get("image_urls", [])
                if response_image_urls:
                    yield self.create_image_message(response_image_urls[0])
                
                # 处理二进制数据返回
                if not tool_parameters.get("return_url", True):
                    response_binary_data = data.get("binary_data_base64", [])
                    if response_binary_data:
                        blob = base64.b64decode(response_binary_data[0])
                        yield self.create_blob_message(blob=blob, meta={"mime_type": "image/png"})
            else:
                # 处理API错误响应
                error_msg = response.get("message", f"API调用失败，错误代码: {code}")
                raise ToolProviderCredentialValidationError(error_msg)
            
            yield self.create_json_message(response)
            
        except ToolProviderCredentialValidationError:
            # 重新抛出已知的验证错误
            raise
        except Exception as e:
            # 处理其他未知异常
            raise ToolProviderCredentialValidationError(f"处理请求时发生错误: {str(e)}") from e
