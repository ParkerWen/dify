from collections.abc import Generator
from typing import Any
import base64

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

from legacy.volc_sdk.VisualService import VisualService


class HighAesGeneralV30LZT2ITool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        visual_service = VisualService()

        visual_service.set_ak(self.runtime.credentials.get("AccessKeyID", ""))
        visual_service.set_sk(
            self.runtime.credentials.get("AccessKeySecret", ""))

        form = {
            "req_key": "high_aes_general_v30l_zt2i",
            "prompt": tool_parameters.get("prompt", "一只可爱的猫"),
            "use_pre_llm": tool_parameters.get("use_pre_llm", False),
            "seed": tool_parameters.get("seed", -1),
            "scale": tool_parameters.get("scale", 2.5),
            "width": tool_parameters.get("width", 1328),
            "height": tool_parameters.get("height", 1328),
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
                image_urls = response.get("data", {}).get("image_urls", [])
                if image_urls:
                    if len(image_urls) > 0:
                        yield self.create_image_message(image_urls[0])
                if not tool_parameters.get("return_url", True):
                    binary_data_base64 = response.get("data", {}).get("binary_data_base64", [])
                    if len(binary_data_base64) > 0:
                        blob = base64.b64decode(binary_data_base64[0])
                        yield self.create_blob_message(blob=blob, meta={"mime_type": "image/png"})
            yield self.create_json_message(response)
        except Exception as e:
            raise ToolProviderCredentialValidationError(str(e))
