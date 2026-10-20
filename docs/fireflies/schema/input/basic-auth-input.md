<!-- Source: https://docs.fireflies.ai/schema/input/basic-auth-input.md -->
<!-- Title: BasicAuthInput -->
<!-- Description: Schema for BasicAuthInput - HTTP Basic authentication configuration -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# BasicAuthInput

> Schema for BasicAuthInput - HTTP Basic authentication configuration

The `BasicAuthInput` type configures HTTP Basic authentication for downloading media files. When provided, Fireflies will include an `Authorization: Basic <base64(username:password)>` header when downloading your media file.

## Fields

<ParamField path="username" type="String">
  The username for basic authentication. This field is optional - if not provided, only the password will be used.

  When provided, the value will be trimmed of leading/trailing whitespace.
</ParamField>

<ParamField path="password" type="String" required>
  The password for basic authentication. This field is required when using basic auth.

  The password must be a non-empty string and will be trimmed of leading/trailing whitespace.
</ParamField>

## Usage

HTTP Basic authentication is commonly used with:

* Web servers with `.htaccess` protection
* Internal company file servers
* Legacy systems requiring username/password authentication
* Simple authentication schemes for private media hosting

## Examples

### With Username and Password

```graphql theme={null}
mutation {
  uploadAudio(input: {
    url: "https://files.company.com/recordings/meeting.mp3"
    title: "Sales Call"
    download_auth: {
      type: basic_auth
      basic: {
        username: "api-user"
        password: "secure-password-123"
      }
    }
  }) {
    success
    message
  }
}
```

### Password Only

When the server only requires a password (username is optional):

```graphql theme={null}
mutation {
  uploadAudio(input: {
    url: "https://protected.example.com/audio.mp3"
    title: "Meeting Recording"
    download_auth: {
      type: basic_auth
      basic: {
        password: "access-key-here"
      }
    }
  }) {
    success
    message
  }
}
```

## How It Works

When you provide basic authentication credentials:

1. Fireflies combines the username and password as `username:password`
2. The combined string is base64-encoded
3. The encoded value is sent as `Authorization: Basic <base64-encoded-credentials>`
4. The media file is downloaded using this authentication header

For example, if you provide:

* Username: `user`
* Password: `pass`

Fireflies will send: `Authorization: Basic dXNlcjpwYXNz`

## Security Considerations

* **HTTPS Required**: The media URL must use HTTPS to ensure credentials are transmitted securely
* **Credential Storage**: Credentials are used only for downloading the file and are not stored permanently
* **Access Control**: Use credentials with minimal required permissions (read-only access to the specific file)
* **Credential Rotation**: For production use, consider rotating credentials regularly

## Related Types

* [DownloadAuthInput](/schema/input/download-auth-input) - Parent authentication configuration
* [BearerTokenAuthInput](/schema/input/bearer-token-auth-input) - Alternative authentication method
* [DownloadAuthType](/schema/enum/download-auth-type) - Authentication type enum
