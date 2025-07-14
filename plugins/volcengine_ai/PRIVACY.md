# Privacy Policy

_Last updated: 2025-07-07_

This document outlines the data privacy and security practices for the plugins developed using `dify_plugin` and integrated with Volcengine VisualService.

## 1. Overview

These plugins provide generative AI and image/video processing capabilities by invoking Volcengine Visual APIs. During this process, some user-provided data such as images, prompts, and credentials are processed and transmitted. We are committed to protecting user privacy and ensuring secure handling of all data.

---

## 2. Data Collection

The plugins may collect and process the following types of data during runtime:

| Data Type                  | Description                                                                 |
|---------------------------|-----------------------------------------------------------------------------|
| **Prompt text**           | User-defined textual prompts used to guide image/video generation.          |
| **Image/video input**     | Uploaded image files, URLs, or base64-encoded images/videos.                |
| **Logo metadata**         | Optional overlay settings including logo text, position, opacity, etc.      |
| **Generation parameters** | Includes width, height, scale, seed, skin smoothing, and generation modes. |
| **Access credentials**    | AccessKeyID and AccessKeySecret for authenticating with Volcengine APIs.    |

No personally identifiable information (PII) is required or expected unless explicitly included by the user in prompts or media content.

---

## 3. Data Usage

All collected data is **used solely** to perform visual processing tasks via the Volcengine API:

- Generate images or videos based on provided inputs.
- Submit and poll for asynchronous task results.
- Overlay logos or perform transformations.
- Return results via blob, URL, or JSON message formats.

Generated content or metadata is **not stored** locally or reused beyond the invocation lifecycle.

---

## 4. Data Storage and Retention

- The plugin **does not persist any data** on disk or external storage.
- All media and prompts are **processed in-memory** and released after use.
- Temporary data sent to Volcengine servers is subject to their own data retention policy.

---

## 5. Third-Party Sharing

Data is **shared only with Volcengine**, the external API provider used for visual processing. We do **not** share any data with other third parties.

Refer to Volcengine's [Privacy Policy](https://www.volcengine.com/docs/6460/112241) for further details.

---

## 6. Credential Handling

- API credentials (`AccessKeyID` and `AccessKeySecret`) are injected at runtime through `self.runtime.credentials`.
- These are **never logged, transmitted to other services**, or exposed outside the plugin execution environment.
- Credentials are validated securely and errors are raised via `ToolProviderCredentialValidationError` when invalid.

---

## 7. Data Security

The following safeguards are implemented:

- HTTPS is used for all API communications.
- No user data is written to disk or persistent logs.
- Binary data is handled in memory and cleared after use.
- External requests (e.g., downloading video blobs) use secure, streamed access to avoid exposing full content to memory/disk unless explicitly required.

---

## 8. User Control

Users are responsible for:

- Verifying that image/video content does not contain sensitive or personal information.
- Managing their own API keys securely.
- Configuring runtime parameters (such as `return_url`, `add_logo`) according to their privacy preferences.

---

## 9. Changes to This Policy

This privacy statement may be updated in the future to reflect changes in functionality or compliance requirements. Any material changes will be communicated clearly via repository updates.

---

## 10. Contact

For questions or concerns regarding data handling in this plugin, please contact the repository maintainer or submit an issue via the associated repository platform.

---

**By using this plugin, you agree to the terms described in this Privacy Policy.**
