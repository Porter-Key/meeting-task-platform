<!-- Source: https://docs.fireflies.ai/schema/input/download-auth-input.md -->
<!-- Title: DownloadAuthInput -->
<!-- Description: Schema for DownloadAuthInput - authentication configuration for media downloads -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# DownloadAuthInput

> Schema for DownloadAuthInput - authentication configuration for media downloads

The `DownloadAuthInput` type configures authentication for downloading media files during audio upload. This allows you to upload files that are hosted on private servers or require authentication.

## Fields

<ParamField path="type" type="DownloadAuthType" required>
  The authentication method to use when downloading the media file. Must be one of:

  * `none` - No authentication (publicly accessible URL)
  * `bearer_token` - Bearer token authentication
  * `basic_auth` - HTTP Basic authentication

  See [DownloadAuthType](/schema/enum/download-auth-type) for details.
</ParamField>

<ParamField path="bearer" type="BearerTokenAuthInput">
  Bearer token configuration. Required when `type` is `bearer_token`, must not be provided for other types.

  See [BearerTokenAuthInput](/schema/input/bearer-token-auth-input) for the complete schema definition.
</ParamField>

<ParamField path="basic" type="BasicAuthInput">
  Basic authentication configuration. Required when `type` is `basic_auth`, must not be provided for other types.

  See [BasicAuthInput](/schema/input/basic-auth-input) for the complete schema definition.
</ParamField>

## Validation Rules

The `DownloadAuthInput` type enforces mutual exclusivity between authentication methods:

* When `type` is `bearer_token`, only the `bearer` field should be provided
* When `type` is `basic_auth`, only the `basic` field should be provided
* When `type` is `none`, neither `bearer` nor `basic` should be provided

Providing fields for multiple authentication types will result in a validation error.

## Examples

### Bearer Token Authentication

```graphql theme={null}
{
  type: bearer_token
  bearer: {
    token: "your-bearer-token-here"
  }
}
```

### Basic Authentication

```graphql theme={null}
{
  type: basic_auth
  basic: {
    username: "your-username"
    password: "your-password"
  }
}
```

### No Authentication (Default)

When the media file is publicly accessible, you can either omit the `download_auth` field entirely or explicitly set it to `none`:

```graphql theme={null}
{
  type: none
}
```

## Use Cases

### Private Cloud Storage

Use bearer token authentication for files stored in private cloud storage with token-based access:

```graphql theme={null}
mutation {
  uploadAudio(input: {
    url: "https://storage.example.com/recordings/meeting-123.mp3"
    title: "Team Standup"
    download_auth: {
      type: bearer_token
      bearer: {
        token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
      }
    }
  }) {
    success
    message
  }
}
```

### Protected Web Servers

Use basic authentication for files hosted on web servers with HTTP Basic Auth:

```graphql theme={null}
mutation {
  uploadAudio(input: {
    url: "https://recordings.company.com/meeting-123.mp3"
    title: "Client Call"
    download_auth: {
      type: basic_auth
      basic: {
        username: "api-user"
        password: "secure-password"
      }
    }
  }) {
    success
    message
  }
}
```

## Related Types

* [BearerTokenAuthInput](/schema/input/bearer-token-auth-input) - Bearer token configuration
* [BasicAuthInput](/schema/input/basic-auth-input) - Basic auth configuration
* [DownloadAuthType](/schema/enum/download-auth-type) - Authentication type enum
* [AudioUploadInput](/schema/input/audio-upload-input) - Parent input type
