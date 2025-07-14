from collections.abc import Generator
from typing import Any
import requests
import time

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

from legacy.volc_sdk.VisualService import VisualService


class JimengVGFMT2VL20Tool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        visual_service = VisualService()

        visual_service.set_ak(self.runtime.credentials.get("AccessKeyID", ""))
        visual_service.set_sk(
            self.runtime.credentials.get("AccessKeySecret", "")
        )

        form = {
            "req_key": "jimeng_vgfm_t2v_l20",
            "prompt": tool_parameters.get("prompt", ""),
            "seed": tool_parameters.get("seed", -1),
            "aspect_ratio": tool_parameters.get("aspect_ratio", "16:9")
        }
        try:
            response = visual_service.cv_sync2async_submit_task(form=form)
            code = response.get("code", -1)
            if code == 10000:
                task_id = response.get("data", {}).get("task_id", "")
                if task_id:
                    task_response = self._poll_for_result(
                        visual_service, task_id)
                    video_url = task_response.get("data", {}).get("video_url", "")
                    if video_url:
                        blob = self._video_url_to_blob_stream(video_url)
                        yield self.create_blob_message(blob=blob, meta={"mime_type": "video/mp4"})
                        yield self.create_link_message(video_url)
                    yield self.create_json_message(task_response)
            yield self.create_json_message(response)
        except Exception as e:
            raise ToolProviderCredentialValidationError(str(e))

    def _poll_for_result(self, visual_service: VisualService, task_id: str) -> dict:
        timeout, start_time = 300, time.time()
        form = {
            "req_key": "jimeng_vgfm_t2v_l20",
            "task_id": task_id,
        }
        while True:
            try:
                response = visual_service.cv_sync2async_get_result(form=form)
                code = response.get("code", -1)
                status = response.get("data", {}).get("status", "")
                if code == 10000:
                    if status == "done":
                        return response
                    else:
                        if time.time() - start_time > timeout:
                            raise Exception(
                                "Volcengine API Timeout: Request took too long to complete"
                            )
                        else:
                            time.sleep(10)
            except Exception as e:
                raise ToolProviderCredentialValidationError(str(e))

    def _video_url_to_blob_stream(self, video_url: str) -> bytes:
        response = requests.get(video_url, stream=True)
        response.raise_for_status()
        blob = b''
        for chunk in response.iter_content(chunk_size=8192):
            blob += chunk
        return blob
