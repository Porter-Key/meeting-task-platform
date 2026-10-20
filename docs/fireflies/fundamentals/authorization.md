<!-- Source: https://docs.fireflies.ai/fundamentals/authorization.md -->
<!-- Title: Authorization -->
<!-- Description: Authenticating your requests with the Fireflies API -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Authorization

> Authenticating your requests with the Fireflies API

## Overview

The Fireflies API implements token-based authentication, which ensures that only authorized users can access certain data and functionalities.

### Token-Based Authentication

We use a standard bearer token authentication mechanism. This means that to make authorized requests to the API, you must include an `Authorization` header with a valid token.

### Acquiring a Token

Follow these steps to obtain your API key for the Fireflies API:

1. Log in to your account at [fireflies.ai](https://app.fireflies.ai)
2. Navigate to the [Integrations](https://app.fireflies.ai/integrations) section
3. Click on [Fireflies API](https://app.fireflies.ai/integrations/custom/fireflies)
4. Copy and store your API key securely

### Making an Authenticated Request

To make an authenticated request, add the `Authorization` header followed by the word `Bearer` and your API key.

### Example of an Authenticated Request Header

```plaintext theme={null}
Authorization: Bearer your_api_key
```

### Example request with Authorization header

<CodeGroup>
  ```curl curl theme={null}
   curl \
     -X POST \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer your_api_key" \
     --data '{ "query": "{ user { name integrations } }" }' \
     https://api.fireflies.ai/graphql
  ```

  ```javascript javascript theme={null}
  const axios = require('axios');

  const url = 'https://api.fireflies.ai/graphql';
  const headers = {
    'Content-Type': 'application/json',
    Authorization: 'Bearer your_api_key'
  };
  const data = {
    query: '{ user { name integrations } }'
  };

  axios
    .post(url, data, { headers: headers })
    .then(response => {
      console.log(response.data);
    })
    .catch(error => {
      console.error('Error:', error);
    });
  ```

  ```python python theme={null}
  import requests

  url = 'https://api.fireflies.ai/graphql'
  headers = {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer your_api_key'
  }
  data = {
      'query': '{ user { name integrations } }'
  }

  response = requests.post(url, json=data, headers=headers)
  print(response.json())
  ```

  ```java java theme={null}
  import java.net.URI;
  import java.net.http.HttpClient;
  import java.net.http.HttpRequest;
  import java.net.http.HttpResponse;
  import java.nio.charset.StandardCharsets;

  public class ApiRequest {
      public static void main(String[] args) {
          HttpClient client = HttpClient.newHttpClient();
          String url = "https://api.fireflies.ai/graphql";
          String json = "{\"query\":\"{ user { name integrations } }\"}";
          HttpRequest request = HttpRequest.newBuilder()
                  .uri(URI.create(url))
                  .header("Content-Type", "application/json")
                  .header("Authorization", "Bearer your_api_key")
                  .POST(HttpRequest.BodyPublishers.ofString(json, StandardCharsets.UTF_8))
                  .build();

          client.sendAsync(request, HttpResponse.BodyHandlers.ofString())
                  .thenApply(HttpResponse::body)
                  .thenAccept(System.out::println)
                  .join();
      }
  }
  ```
</CodeGroup>

Ensure to replace `your_api_key` with your actual API key.

## Best Practices for Token Security

* **Keep it Secret:** Treat your API key like a password. Never expose it in client-side code or share it publicly.
* **Store Securely:** Store the API key securely in your application, ideally in environment variables or secure storage solutions.

<Warning>
  Improper handling of API keys can lead to security vulnerabilities. Always ensure API keys are
  used and stored securely.
</Warning>

## Troubleshooting

* **Invalid key:** If you receive an error regarding an invalid API key, verify that the API key hasn't expired and that it's correctly included in the request header.
* **Missing key:** Ensure that the `Authorization` header is present in your requests requiring authentication.

<Info>
  If you encounter issues with authentication or have questions about API key management, please
  contact our support team.
</Info>

## FAQ

<Accordion title="Why am I getting an 'auth_failed' error?">
  <p>This error can signal an issue in your Authorization header. Please ensure that you are including the `Authorization` header with the word `Bearer` and your API key.</p>
</Accordion>

## Additional Resources

<CardGroup cols={2}>
  <Card title="Quickstart" icon="link" href="/getting-started/quickstart">
    Make your first request in under 5 minutes
  </Card>

  <Card title="Errors" icon="link" href="/fundamentals/errors">
    Error standards for the Fireflies API
  </Card>
</CardGroup>
