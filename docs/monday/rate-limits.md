# Rate limits

Learn more about the monday.com platform API rate limits, calculating complexity, and timeout policies

We strive to provide a top-tier API experience that is reliable and consistent for all users. To maintain a high-quality service and ensure optimal performance, users are subject to the following limits to help manage the API's consumption and throughput:

* Complexity limit
* Daily call limit
* Minute limit
* Concurrency limit
* IP limit
* Resource protection limits

Remembering these limits when using the API is crucial to prevent workflow disruptions and delays.

> 🚧 All limits and exceptions are subject to change. Additional guidelines may be introduced in the future.

# Limits

## Complexity limit

Complexity defines the load that each call puts on the API. This limit restricts the heaviness of each query to help prevent excessive load and maintain optimal performance. The limit will not affect most users—the quota is set sufficiently high to impact only users making requests that would compromise the stability of the API.

You will receive a `ComplexityException` error if you hit the limit.

The limit varies based on how you're making the call:

| Usage                                       | Limit                                                                                                      |
| :------------------------------------------ | :--------------------------------------------------------------------------------------------------------- |
| Individual query                            | 5,000,000 (5M) complexity points                                                                           |
| Using app tokens to access the API          | Read and writes are limited to 5M complexity points per minute\* each                                      |
| Using API playground to access the API      | Reads and writes are limited to 5M complexity points per minute\* each or 1M for trial/free accounts       |
| Using personal API tokens to access the API | Reads and writes have a combined budget of 10M points per minute\* or 1M for trial, NGO, and free accounts |

*\*Per-minute budgets follow a sliding window and reset 60 seconds after the first API call was made*

### Calculating complexity

Calculating the complexity of each query in advance can prevent you from hitting the limit. The simplest way to do so is by adding the [complexity](https://developer.monday.com/api-reference/docs/complexity#queries) field to your queries to return the remaining complexity before and after the query, the complexity of the query itself, and when the limit resets.

```graphql
mutation {
  complexity {
    query
    before
    after
  }
  create_item(board_id:1234567890, item_name:"test item") {
    id
  }
}
```

### Reducing complexity

You can avoid hitting the complexity limit by:

* Requesting only the data you need
* Reducing nested queries
* Utilizing the `page` and `limit` arguments

## Daily call limit

The daily call limit helps prevent disruptions caused by excessive load from individual accounts, maintains the API service as a free feature across all plans, and controls operational costs to continue delivering value to all our users.

All API calls made through personal tokens, private applications, and public applications (excluding marketplace apps and those developed by monday.com) count towards this limit.

You will receive a `DAILY_LIMIT_EXCEEDED` error if you hit the limit.

The limit varies based on your [monday.com plan](https://monday.com/pricing):

| Tier                | Daily call limit (resets at midnight UTC) |
| :------------------ | :---------------------------------------- |
| Free/Standard/Basic | 1,000                                     |
| Pro                 | 10,000 (soft limit)\*                     |
| Enterprise          | 25,000 (soft limit)\*                     |

*\*Indicates the recommended usage. Please request an increase through the[API analytics dashboard](https://developer.monday.com/api-reference/docs/api-analytics) if your account consistently exceeds this limit.*

### Exceptions

A single API request typically deducts one call from your daily limit. However, there are exceptions for specific calls:

| API call                                                                                                                                                                                                                                                                                                                           | Contribution to the daily limit | Resolution                                                                                                                                                                                                                                                                  |
| :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------ | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Requests that hit a rate limit ([complexity](https://developer.monday.com/api-reference/docs/errors#complexityexception), [minute rate limit](https://developer.monday.com/api-reference/docs/errors#rate-limit-exceeded), [concurrency](https://developer.monday.com/api-reference/docs/errors#concurrency-limit-exceeded), etc.) | 0.1 calls                       | Every rate limit error returns a `retry_in_seconds` field. Only retry your call after waiting for the indicated time to avoid wasteful retries.                                                                                                                             |
| Querying `complexity` to check a query's complexity cost                                                                                                                                                                                                                                                                           | 0.1 calls                       | On their own, [`complexity`](https://developer.monday.com/api-reference/reference/complexity) queries count as **less than one call**. We recommend including this query in other API requests to save this usage.                                                          |
| High complexity queries                                                                                                                                                                                                                                                                                                            | 1+ calls                        | Each API call incurs a complexity cost, and some of these calls contribute extra to the daily call limit. To reduce your daily API call usage, you can [reduce your call's complexity](https://developer.monday.com/api-reference/docs/rate-limits#calculating-complexity). |

## Minute limit

The minute limit restricts the number of requests in a given period. It is defined per minute, but you may not need to wait for the full minute before retrying your request. You can use the `Retry-After` header to determine when you can retry the request.

You will receive a `Minute limit rate exceeded` error if you hit the limit.

The limit varies based on your [monday.com plan](https://monday.com/pricing):

| Tier       | Queries per minute |
| :--------- | :----------------- |
| Enterprise | 5,000              |
| Pro        | 2,500              |
| Other      | 1,000              |

### Endpoint-specific minute limits

Each endpoint is subject to the limits mentioned above, but some have additional limits to keep in mind:

<Table align={["left","left"]}>
  <thead>
    <tr>
      <th>
        Endpoint
      </th>

      <th>
        Limit
      </th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>
        [Create a board mutation](https://developer.monday.com/api-reference/docs/boards#create-a-board)
      </td>

      <td>
        40 mutations per minute
      </td>
    </tr>

    <tr>
      <td>
        [Duplicate a board mutation](https://developer.monday.com/api-reference/docs/boards#duplicate-a-board)
      </td>

      <td>
        40 mutations per minute
      </td>
    </tr>

    <tr>
      <td>
        [Duplicate a group mutation](https://developer.monday.com/api-reference/docs/groups#duplicate-group)
      </td>

      <td>
        40 mutations per minute
      </td>
    </tr>

    <tr>
      <td>
        [Connect project to portfolio mutation](https://mondaydotdev.readme.io/api-reference/reference/portfolio#connect-project-to-portfolio)
      </td>

      <td>
        15 mutations per minute
      </td>
    </tr>

    <tr>
      <td>
        [Items query](https://developer.monday.com/api-reference/docs/items#queries)
      </td>

      <td>
        100 items
      </td>
    </tr>

    <tr>
      <td>
        [App subscriptions query](https://developer.monday.com/api-reference/reference/app-subscriptions)
      </td>

      <td>
        120 times per minute
      </td>
    </tr>

    <tr>
      <td>
        [`display_value`](https://developer.monday.com/api-reference/reference/formula#fields)

        field on

        `FormulaValue`

        implementation
      </td>

      <td>
        <li>10,000 formula values per minute (each cell counts as one)</li><li>Up to five formula columns in each request</li>
      </td>
    </tr>
  </tbody>
</Table>

## Concurrency limit

The concurrency limit restricts the number of requests being handled at any moment. You will receive a [`Concurrency limit exceeded`](https://developer.monday.com/api-reference/docs/errors#concurrency-limit-exceeded) error if you hit the limit.

The limit varies based on your [monday.com plan](https://monday.com/pricing) and the type of request:

| Tier       | Maximum concurrent requests |
| :--------- | :-------------------------- |
| Enterprise | 250                         |
| Pro        | 100                         |
| Other      | 40                          |

## IP limit

The IP limit helps control the API traffic coming from a given IP address within a short period. You will receive an [`IP_RATE_LIMIT_EXCEEDED`](https://developer.monday.com/api-reference/docs/error-handling#4xx-client-errors) error if you hit the limit.

| Source                | Limit                         |
| :-------------------- | :---------------------------- |
| Individual IP address | 5,000 requests per 10 seconds |

## Resource protection limit

In rare cases, an internal monday resource might reject the request. In such a case the same retry logic applies.

# Guidelines

* All requests count towards the stated limits, **even those that fail or return an error.** You can prevent unnecessary API usage by waiting for the time indicated in the `retry_in_seconds` field before retrying the call.
* The [API SDK](https://developer.monday.com/api-reference/docs/api-sdk) respects the rate-limited responses and waits the appropriate amount of time before automatically retrying the request, up to a configurable maximum number of retries.
* Unless otherwise noted, limits are measured per account, per app. Usage through a personal token counts toward the same limit.