<!-- Source: https://docs.fireflies.ai/getting-started/quickstart.md -->
<!-- Title: Quickstart -->
<!-- Description: Make your first request in under 5 minutes. -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Quickstart

> Make your first request in under 5 minutes.

This guide provides step-by-step instructions to make your first query with our GraphQL API and demonstrates basic functionality.

## Step 1: Setting Up

Before diving into querying the API, it's essential to set up your environment correctly. This includes obtaining authentication credentials and configuring your development environment.

### Obtaining Authentication Credentials

To access our API, you will need an API key. Follow these steps to obtain your key:

1. Log in to your account at [app.fireflies.ai](https://app.fireflies.ai)
2. Navigate to the [Integrations](https://app.fireflies.ai/integrations) section
3. Click on [Fireflies API](https://app.fireflies.ai/integrations/custom/fireflies)
4. Copy and store your API key securely

<Note>
  It's crucial to handle your API key with the utmost care to ensure the security of your data. For
  more information on Authorization and best practices, visit
  [Authorization](/fundamentals/authorization)
</Note>

## Step 2: Making Your First Request

Execute a simple query to retrieve a list of users.

Replace `your_api_key` with your API key in the following requests

<CodeGroup>
  ```bash curl theme={null}
  curl \
     -X POST \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer your_api_key" \
     --data '{ "query": "{ users { name user_id } }" }' \
     https://api.fireflies.ai/graphql
  ```

  ```python python theme={null}
  import requests

  url = 'https://api.fireflies.ai/graphql'
  headers = {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer your_api_key'
  }
  data = {
      'query': '{ users { name user_id } }'
  }

  response = requests.post(url, json=data, headers=headers)
  print(response.json())
  ```

  ```javascript javascript theme={null}
  const axios = require('axios');

  const url = 'https://api.fireflies.ai/graphql';
  const headers = {
    'Content-Type': 'application/json',
    Authorization: 'Bearer your_api_key'
  };
  const data = {
    query: '{ users { name user_id } }'
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

  ```java java theme={null}
  import java.net.URI;
  import java.net.http.HttpClient;
  import java.net.http.HttpRequest;
  import java.net.http.HttpResponse;
  import java.net.http.HttpHeaders;
  import java.nio.charset.StandardCharsets;

  public class ApiRequest {
      public static void main(String[] args) {
          HttpClient client = HttpClient.newHttpClient();
          String url = "https://api.fireflies.ai/graphql";
          String json = "{\"query\":\"{ users { name user_id } }\"}";
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

<br />

<Note>
  When building GraphQL queries for this API, focus on precision and efficiency. Start with simple
  queries and gradually increase complexity. Ensure you only request the data you need to avoid
  over-fetching.

  * **Review the Schema Documentation**: For guidance, refer to the [Schema](/schema) section and use tools like GraphQL Playground for testing. Efficient queries lead to better performance and a smoother API experience.
</Note>

More details on building your GraphQL query are available [here](/graphql-api)

## Step 3: Analyzing the Response

You will receive a JSON response with the requested data. Example response:

<CodeGroup>
  ```bash curl theme={null}
  {
  	"data":
  	{
  		"users": [
  			{
  				"name":"Justin Fly",
  				"user_id":"example-id"
  			}
  		]
  	}
  }
  ```
</CodeGroup>

Continue to the next sections for more detailed examples and advanced usage instructions.

<Footer />

## Additional Resources

<CardGroup cols={2}>
  <Card title="Users" icon="link" href="/graphql-api/query/users">
    Query users using the API
  </Card>

  <Card title="Authorization" icon="link" href="/fundamentals/authorization">
    Authenticating your requests with the Fireflies API
  </Card>
</CardGroup>
