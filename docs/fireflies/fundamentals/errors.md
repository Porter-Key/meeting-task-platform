<!-- Source: https://docs.fireflies.ai/fundamentals/errors.md -->
<!-- Title: Errors -->
<!-- Description: Error standards for the Fireflies API -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Errors

> Error standards for the Fireflies API

## Overview

Understanding how errors are structured and returned by the Fireflies API is key to effectively handling and troubleshooting issues. This page outlines the common error format and details specific error types.

## Error schema

Our GraphQL API follows a standard format for returning errors. Errors are encapsulated within an `errors` array in the response body.

Please visit [Error codes](/miscellaneous/error-codes) to view explanations for error code types

<ResponseField name="message" type="String" required>
  Description of the error
</ResponseField>

<ResponseField name="code" type="String" required>
  Error code.
</ResponseField>

<ResponseField name="friendly" type="Boolean" required>
  `friendly === true` are safe to show to the frontend client. Unfriendly errors may have technical
  details that may not be useful to the UI layer.
</ResponseField>

<ResponseField name="extensions" type="Object">
  Contains useful metadata related to the error.

  Where relevant, includes field `helpUrls` pointing to relevant API documentation sections that explain the error and provide guidance on how to resolve it
</ResponseField>

```json Example theme={null}
{
  "data": {},
  "errors": [
    {
      "message": "Error description",
      "friendly": true,
      "code": "error_code",
      "extensions": {
        "helpUrls": [
          "https://docs.fireflies.ai/miscellaneous/error-codes#error_code"
        ],
        "code": "error_code",
        "status": http_status_code,
        "...otherFields": "..."
      }
    }
  ]
}
```

## Additional Resources

<CardGroup cols={2}>
  <Card title="Error Codes" icon="link" href="/miscellaneous/error-codes">
    Detailed error code reference
  </Card>

  <Card title="Authorization" icon="link" href="/fundamentals/authorization">
    Authenticating your requests with the Fireflies API
  </Card>
</CardGroup>
