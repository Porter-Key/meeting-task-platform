<!-- Source: https://docs.fireflies.ai/fundamentals/limits.md -->
<!-- Title: Limits -->
<!-- Description: File size and API rate limits for the Fireflies API -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Limits

> File size and API rate limits for the Fireflies API

## Overview

Understanding the limitations of our API is crucial for efficient and uninterrupted usage. Below
you'll find detailed information about the upload limits for different file types and the rate
limits applicable to various subscription plans.

## Upload Limits

The Fireflies API accommodates a range of file sizes for different user types. Here's a breakdown of the maximum file sizes for audio and video uploads:

| Upload Type | Free User Limit | Pro / Business / Enterprise Limit |
| ----------- | --------------- | --------------------------------- |
| Audio Files | Up to 200MB     | Up to 200MB                       |
| Video Files | Up to 100MB     | Up to 1.5GB                       |

### Understanding Upload Limits

* **Audio Files:** All users can upload an audio file no greater than 200MB, ensuring ample capacity for high-quality audio content.
* **Video Files for Free Users:** Free users have a maximum upload limit of 100MB for video files, suitable for short clips and previews.
* **Video Files for Pro/Business/Enterprise Users:** Higher-tier users can upload larger video files up to 1.5GB, accommodating longer and higher resolution content.

## API Rate Limits

To maintain the quality of service and availability for all users, our API enforces rate limits based on the type of subscription plan.

| Plan                  | API Rate Limit      |
| --------------------- | ------------------- |
| Free / Pro            | 50 requests per day |
| Business / Enterprise | 60 requests per min |

### Add to Live API Rate Limit

The Add to Live API has a rate limit of 3 requests per 20 minutes.

### Share Meeting API Rate Limit

The Share Meeting API has a rate limit of 10 requests per hour. Each request supports up to 50 email addresses.

### Navigating API Rate Limits

* **Free and Pro Plans:** These plans are ideal for light to moderate usage, with a cap of 50 API requests per day. This rate is suitable for testing and small-scale applications.
* **Business and Enterprise Plans:** Designed for more demanding use cases, these plans allow up to 60 requests per minute, providing ample capacity for larger applications and higher volume demands.

<strong>
  These limits are in place to ensure optimal performance and fair usage across our platform.
</strong>

## Additional Resources

<CardGroup cols={2}>
  <Card title="Upload Audio" icon="link" href="/graphql-api/mutation/upload-audio">
    Use the API to upload audio to Fireflies.ai
  </Card>

  <Card title="Authorization" icon="link" href="/fundamentals/authorization">
    Authenticating your requests with the Fireflies API
  </Card>
</CardGroup>
