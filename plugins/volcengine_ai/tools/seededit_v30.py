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
        visual_service = VisualService()

        visual_service.set_ak(self.runtime.credentials.get("AccessKeyID", ""))
        visual_service.set_sk(
            self.runtime.credentials.get("AccessKeySecret", "")
        )

        image_files: list[File] = tool_parameters.get("image_files", [])
        image_urls = []
        binary_data_base64 = []

        for image_file in image_files:
            image_urls.append(image_file.url)
            binary_data_base64.append(
                base64.b64encode(image_file.blob).decode("utf-8")
            )

        form = {
            "req_key": "seededit_v3.0",
            "binary_data_base64": binary_data_base64,
            "image_urls": image_urls,
            "prompt": tool_parameters.get("prompt", ""),
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
