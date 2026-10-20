<!-- Source: https://docs.fireflies.ai/miscellaneous/error-codes.md -->
<!-- Title: Error codes -->
<!-- Description: Error codes and their explanations -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Error codes

> Error codes and their explanations

## Overview

This page lists the error codes and their corresponding reasons for the Fireflies.ai API. You can refer to this page to understand the meaning and possible causes of different error codes that you may encounter while using the API. It provides a comprehensive reference for troubleshooting and resolving issues. Please visit [Errors](/fundamentals/errors) page for more details

## API Errors

### `invalid_arguments`

Returned when invalid arguments are passed to a query or mutation

```json theme={null}
{
  "errors": [
    {
      ... other fields for error
      "message": "Invalid argument(s) were provided",
      "code": "invalid_arguments",
      "extensions": {
        "code": "invalid_arguments",
        "status": 400,
        "metadata": {
          "fields": [
            {
              "name": "fromDate",
              "message": "fromDate must be a Date instance",
              "constraints": [
                {
                  "type": "isDate",
                  "message": "fromDate must be a Date instance"
                }
              ]
            }
          ]
        }
      }
    }
  ]
}
```

### `object_not_found`

Returned when the subject of your query or mutation is not found. For example, querying a non-existent userId would throw an `object_not_found` error of the type `User`

```json theme={null}
{
  "errors": [
    {
	  ... other fields for error
      "message": "User not found",
      "code": "object_not_found",
      "extensions": {
        "code": "object_not_found",
        "status": 404,
        "metadata": {
          "objectType": "User"
        }
      }
    }
  ],
}
```

### `forbidden`

Returned when you are not allowed to perform an action

```json theme={null}
{
  "errors": [
    {
	  ... other fields for error
      "message": "You are not authorized to perform this action",
      "code": "forbidden",
      "extensions": {
        "code": "forbidden",
        "status": 403,
      }
    }
  ]
}
```

### `paid_required`

Returned when you are required to be subscribed to a paid plan for the Fireflies.ai platform. The error will also mentioned the required `tier` for such actions. For example, making a request to `uploadAudio` as a free user will throw a `paid_required` error with tier `pro_or_higher`, which means that you need to be subscribed to a Pro or Higher plan to perform this action

```json theme={null}
{
  "errors": [
    {
	  ... other fields for error
      "message": "You need to be subscribed to a paid plan to perform this action",
      "code": "paid_required",
      "extensions": {
        "code": "paid_required",
        "status": 403,
        "metadata": {
          "tier": "pro_or_higher"
        },
      }
    }
  ]
}
```

### `not_in_team`

Returned when you are attempting to query against a `userId` that is not a part of your team

```json theme={null}
{
  "errors": [
    {
	  ... other fields for error
      "message": "You do not have permissions for this team",
      "code": "not_in_team",
      "extensions": {
        "code": "not_in_team",
        "status": 403,
      }
    }
  ]
}
```

### `require_elevated_privilege`

Returned when you are attempting to perform admin actions as a non-admin user

```json theme={null}
{
  "errors": [
    {
	  .. other fields for error
      "message": "You do not have permission to perform this action",
      "code": "require_elevated_privilege",
      "extensions": {
        "code": "require_elevated_privilege",
        "status": 403,
      }
    }
  ]
}
```

### `account_cancelled`

Returned when your account has been cancelled due to non-payment or some other reason. Please contact support if you think this is a mistake

```json theme={null}
{
  "errors": [
    {
	  ... other fields for error
      "message": "Your account is inactive. If this is not expected, please contact support",
      "code": "account_cancelled",
      "extensions": {
        "code": "account_cancelled",
        "status": 403,
      }
    }
  ]
}
```

### `args_required`

Returned when your query or mutation is missing one or more required arguments. The property `extesions.metadata.fields` will provide the list of fields that have this constraints

```json theme={null}
{
  "errors": [
    {
	  ... other fields for error
      "message": "You must provide one of the following: mine, transcript_id, my_team",
      "code": "args_required",
      "extensions": {
        "code": "args_required",
        "status": 400,
        "metadata": {
          "fields": [
            "mine",
            "transcript_id",
            "my_team"
          ]
        },
      }
    }
  ]
}
```

### `too_many_requests`

Returned when you have been rate-limited due to making too many requests. The field `extensions.metadata.retryAfter` mentions the `retryAfter` time

```json theme={null}
{
  "errors": [
    {
	  ... other fields for error
      "message": "Too many requests. Please retry after 2:45:45 AM (UTC)",
      "code": "too_many_requests",
      "extensions": {
        "code": "too_many_requests",
        "status": 429,
        "metadata": {
          "retryAfter": 1720651545066
        }
      }
    }
  ]
}
```

### `payload_too_small`

Returned when the content size for `uploadAudio` mutation is too small. Upload files larger than `50kb` to avoid this error

```json theme={null}
{
  "errors": [
    {
	  ... other fields for error
      "message": "Content size is too small. Please upload files larger than 50kb",
      "code": "payload_too_small",
      "extensions": {
        "code": "payload_too_small",
        "status": 400,
      }
    }
  ]
}
```

### `request_timeout`

Returned when your request has taken too long to respond.

```json theme={null}
{
  "errors": [
    {
	  ... other fields for error
      "message": "Request timed out. Please try again or contact support",
      "code": "request_timeout",
      "extensions": {
        "code": "request_timeout",
        "status": 408,
      }
    }
  ]
}
```

### `invalid_language_code`

Returned when an invalid language code has been passed to a query or mutation

```json theme={null}
{
  "errors": [
    {
	  ... other fields for error
      "message": "Language code is invalid or not supported. Please refer to API docs for supported languages",
      "code": "invalid_language_code",
      "extensions": {
        "code": "invalid_language_code",
        "status": 400,
      }
    }
  ]
}
```

### `admin_must_exist`

Returned when you are attempting to call `setUserRole` for a single member team

```json theme={null}
{
  "errors": [
    {
	  ... other fields for error
      "message": "You must have at least one admin your team",
      "code": "admin_must_exist",
      "extensions": {
        "code": "admin_must_exist",
        "status": 400,
      }
    }
  ]
}
```

### `unsupported_platform`

Returned when an unsupported meeting platform URL is provided to the `addToLiveMeeting` mutation

```json theme={null}
{
  "errors": [
    {
      ... other fields for error
      "message": "The meeting platform is not supported. Please use a supported meeting platform URL.",
      "code": "unsupported_platform",
      "extensions": {
        "code": "unsupported_platform",
        "status": 400,
      }
    }
  ]
}
```

### `require_ai_credits`

Returned when you have insufficient AI credits to perform AI-powered operations like AskFred queries. You may need to upgrade your plan or purchase additional credits.

```json theme={null}
{
  "errors": [
    {
	  ... other fields for error
      "message": "You do not have sufficient AI credits to perform this action",
      "code": "require_ai_credits",
      "extensions": {
        "code": "require_ai_credits",
        "status": 402,
        "helpUrls": [
          "https://app.fireflies.ai/upgrade"
        ]
      }
    }
  ]
}
```

### `invariant_violation`

Returned when an internal invariant is violated (unexpected internal state).

This typically indicates a bug and is not actionable by clients.

Please contact support if you receive this error.

```json theme={null}
{
  "errors": [
    {
	  ... other fields for error
      "message": "Something unexpected happened. Please try again",
      "code": "invariant_violation",
      "extensions": {
        "code": "invariant_violation",
        "status": 500,
      }
    }
  ]
}
```
