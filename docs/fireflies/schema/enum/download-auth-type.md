<!-- Source: https://docs.fireflies.ai/schema/enum/download-auth-type.md -->
<!-- Title: DownloadAuthType -->
<!-- Description: Enum for DownloadAuthType - authentication methods for media downloads -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# DownloadAuthType

> Enum for DownloadAuthType - authentication methods for media downloads

The `DownloadAuthType` enum specifies the authentication method to use when downloading media files during audio upload.

## Values

<ParamField path="none" type="Enum Value">
  No authentication required. The media file is publicly accessible.

  This is the default when `download_auth` is not provided.
</ParamField>

<ParamField path="bearer_token" type="Enum Value">
  Bearer token authentication. Requires the `bearer` field with a token.

  Fireflies will send `Authorization: Bearer <token>` when downloading the file.
</ParamField>

<ParamField path="basic_auth" type="Enum Value">
  HTTP Basic authentication. Requires the `basic` field with username and/or password.

  Fireflies will send `Authorization: Basic <base64(username:password)>` when downloading the file.
</ParamField>

## Usage

The `DownloadAuthType` enum is used in the [DownloadAuthInput](/schema/input/download-auth-input) type to specify which authentication method should be used:

```graphql theme={null}
input DownloadAuthInput {
  type: DownloadAuthType!
  bearer: BearerTokenAuthInput
  basic: BasicAuthInput
}
```

## Examples

### No Authentication (Default)

```graphql theme={null}
mutation {
  uploadAudio(input: {
    url: "https://public-storage.com/audio.mp3"
    title: "Public Recording"
    # download_auth omitted - defaults to 'none'
  }) {
    success
    message
  }
}
```

Or explicitly:

```graphql theme={null}
mutation {
  uploadAudio(input: {
    url: "https://public-storage.com/audio.mp3"
    title: "Public Recording"
    download_auth: {
      type: none
    }
  }) {
    success
    message
  }
}
```

### Bearer Token

```graphql theme={null}
mutation {
  uploadAudio(input: {
    url: "https://protected-storage.com/audio.mp3"
    title: "Protected Recording"
    download_auth: {
      type: bearer_token
      bearer: {
        token: "your-token-here"
      }
    }
  }) {
    success
    message
  }
}
```

### Basic Authentication

```graphql theme={null}
mutation {
  uploadAudio(input: {
    url: "https://private-server.com/audio.mp3"
    title: "Private Recording"
    download_auth: {
      type: basic_auth
      basic: {
        username: "user"
        password: "pass"
      }
    }
  }) {
    success
    message
  }
}
```

## Choosing the Right Authentication Method

| Method         | Use When                         | Example Use Cases                                                           |
| -------------- | -------------------------------- | --------------------------------------------------------------------------- |
| `none`         | File is publicly accessible      | Public S3 buckets, CDN-hosted files, public web servers                     |
| `bearer_token` | File requires OAuth or API token | Private cloud storage, API-protected resources, JWT-authenticated endpoints |
| `basic_auth`   | File requires username/password  | Web servers with `.htaccess`, internal file servers, legacy systems         |

## Related Types

* [DownloadAuthInput](/schema/input/download-auth-input) - Authentication configuration using this enum
* [BearerTokenAuthInput](/schema/input/bearer-token-auth-input) - Bearer token configuration
* [BasicAuthInput](/schema/input/basic-auth-input) - Basic auth configuration
* [AudioUploadInput](/schema/input/audio-upload-input) - Parent input type
