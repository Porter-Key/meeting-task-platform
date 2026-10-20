<!-- Source: https://docs.fireflies.ai/schema/input/bearer-token-auth-input.md -->
<!-- Title: BearerTokenAuthInput -->
<!-- Description: Schema for BearerTokenAuthInput - bearer token authentication configuration -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# BearerTokenAuthInput

> Schema for BearerTokenAuthInput - bearer token authentication configuration

The `BearerTokenAuthInput` type configures bearer token authentication for downloading media files. When provided, Fireflies will include an `Authorization: Bearer <token>` header when downloading your media file.

## Fields

<ParamField path="token" type="String" required>
  The bearer token to use for authentication. This token will be sent as `Authorization: Bearer <token>` when downloading the media file.

  The token must be a non-empty string and will be trimmed of leading/trailing whitespace.
</ParamField>

## Usage

Bearer token authentication is commonly used with:

* Cloud storage services (AWS S3, Google Cloud Storage, Azure Blob Storage)
* API-protected media servers
* OAuth 2.0 protected resources
* JWT-authenticated endpoints

## Example

```graphql theme={null}
mutation {
  uploadAudio(input: {
    url: "https://storage.example.com/recordings/meeting.mp3"
    title: "Team Meeting"
    download_auth: {
      type: bearer_token
      bearer: {
        token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.dozjgNryP4J3jVmNHl0w5N_XgL0n3I9PlFUP0THsR8U"
      }
    }
  }) {
    success
    message
  }
}
```

## Security Considerations

* **Token Expiry**: Ensure your bearer token has sufficient lifetime for Fireflies to download the file (typically a few minutes to hours)
* **Token Scope**: Use tokens with minimal required permissions (read-only access to the specific file)
* **Token Rotation**: For production use, consider using short-lived tokens and rotating them regularly
* **HTTPS Only**: The media URL must use HTTPS to ensure the token is transmitted securely

## Related Types

* [DownloadAuthInput](/schema/input/download-auth-input) - Parent authentication configuration
* [BasicAuthInput](/schema/input/basic-auth-input) - Alternative authentication method
* [DownloadAuthType](/schema/enum/download-auth-type) - Authentication type enum
