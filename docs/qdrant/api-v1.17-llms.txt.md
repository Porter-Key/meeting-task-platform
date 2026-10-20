# Qdrant API Reference v1.17.x

Source: https://api.qdrant.tech/v-1-17-x/llms.txt
Fetched: 2026-05-07T05:06:12.816957+00:00

> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://api.qdrant.tech/v-1-17-x/llms.txt.
> For full documentation content, see https://api.qdrant.tech/v-1-17-x/llms-full.txt.

# v1.17.x

## Docs

- [API Reference](https://api.qdrant.tech/api-reference.mdx)

## API Docs

- API Reference > Collections [Get collection details](https://api.qdrant.tech/api-reference/collections/get-collection.mdx)
- API Reference > Collections [Create a collection](https://api.qdrant.tech/api-reference/collections/create-collection.mdx)
- API Reference > Collections [Delete a collection](https://api.qdrant.tech/api-reference/collections/delete-collection.mdx)
- API Reference > Collections [Update collection parameters](https://api.qdrant.tech/api-reference/collections/update-collection.mdx)
- API Reference > Collections [List all collections](https://api.qdrant.tech/api-reference/collections/get-collections.mdx)
- API Reference > Collections [Check collection existence](https://api.qdrant.tech/api-reference/collections/collection-exists.mdx)
- API Reference > Collections [Get optimization progress](https://api.qdrant.tech/api-reference/collections/get-optimizations.mdx)
- API Reference > Points [Retrieve points](https://api.qdrant.tech/api-reference/points/get-points.mdx)
- API Reference > Points [Upsert points](https://api.qdrant.tech/api-reference/points/upsert-points.mdx)
- API Reference > Points [Retrieve a point](https://api.qdrant.tech/api-reference/points/get-point.mdx)
- API Reference > Points [Delete points](https://api.qdrant.tech/api-reference/points/delete-points.mdx)
- API Reference > Points [Update vectors](https://api.qdrant.tech/api-reference/points/update-vectors.mdx)
- API Reference > Points [Delete vectors](https://api.qdrant.tech/api-reference/points/delete-vectors.mdx)
- API Reference > Points [Set payload](https://api.qdrant.tech/api-reference/points/set-payload.mdx)
- API Reference > Points [Overwrite payload](https://api.qdrant.tech/api-reference/points/overwrite-payload.mdx)
- API Reference > Points [Delete payload](https://api.qdrant.tech/api-reference/points/delete-payload.mdx)
- API Reference > Points [Clear payload](https://api.qdrant.tech/api-reference/points/clear-payload.mdx)
- API Reference > Points [Batch update points](https://api.qdrant.tech/api-reference/points/batch-update.mdx)
- API Reference > Points [Scroll points](https://api.qdrant.tech/api-reference/points/scroll-points.mdx)
- API Reference > Points [Count points](https://api.qdrant.tech/api-reference/points/count-points.mdx)
- API Reference > Points [Payload field facets](https://api.qdrant.tech/api-reference/points/facet.mdx)
- API Reference > Search [Search points](https://api.qdrant.tech/api-reference/search/points.mdx)
- API Reference > Search [Search batch points](https://api.qdrant.tech/api-reference/search/batch-points.mdx)
- API Reference > Search [Search point groups](https://api.qdrant.tech/api-reference/search/point-groups.mdx)
- API Reference > Search [Recommend points](https://api.qdrant.tech/api-reference/search/recommend-points.mdx)
- API Reference > Search [Recommend batch points](https://api.qdrant.tech/api-reference/search/recommend-batch-points.mdx)
- API Reference > Search [Recommend point groups](https://api.qdrant.tech/api-reference/search/recommend-point-groups.mdx)
- API Reference > Search [Discover points](https://api.qdrant.tech/api-reference/search/discover-points.mdx)
- API Reference > Search [Discover batch points](https://api.qdrant.tech/api-reference/search/discover-batch-points.mdx)
- API Reference > Search [Query points](https://api.qdrant.tech/api-reference/search/query-points.mdx)
- API Reference > Search [Query points in batch](https://api.qdrant.tech/api-reference/search/query-batch-points.mdx)
- API Reference > Search [Query point groups](https://api.qdrant.tech/api-reference/search/query-points-groups.mdx)
- API Reference > Search [Distance matrix pairs](https://api.qdrant.tech/api-reference/search/matrix-pairs.mdx)
- API Reference > Search [Distance matrix offsets](https://api.qdrant.tech/api-reference/search/matrix-offsets.mdx)
- API Reference > Indexes [Create payload index](https://api.qdrant.tech/api-reference/indexes/create-field-index.mdx)
- API Reference > Indexes [Delete payload index](https://api.qdrant.tech/api-reference/indexes/delete-field-index.mdx)
- API Reference > Snapshots [List all snapshots (collection)](https://api.qdrant.tech/api-reference/snapshots/list-snapshots.mdx)
- API Reference > Snapshots [Create a snapshot (collection)](https://api.qdrant.tech/api-reference/snapshots/create-snapshot.mdx)
- API Reference > Snapshots [Recover from an uploaded snapshot (collection)](https://api.qdrant.tech/api-reference/snapshots/recover-from-uploaded-snapshot.mdx)
- API Reference > Snapshots [Recover from a snapshot (collection)](https://api.qdrant.tech/api-reference/snapshots/recover-from-snapshot.mdx)
- API Reference > Snapshots [Download a snapshot (collection)](https://api.qdrant.tech/api-reference/snapshots/get-snapshot.mdx)
- API Reference > Snapshots [Delete a snapshot (collection)](https://api.qdrant.tech/api-reference/snapshots/delete-snapshot.mdx)
- API Reference > Snapshots [List all snapshots (storage)](https://api.qdrant.tech/api-reference/snapshots/list-full-snapshots.mdx)
- API Reference > Snapshots [Create a snapshot (storage)](https://api.qdrant.tech/api-reference/snapshots/create-full-snapshot.mdx)
- API Reference > Snapshots [Download a snapshot (storage)](https://api.qdrant.tech/api-reference/snapshots/get-full-snapshot.mdx)
- API Reference > Snapshots [Delete a snapshot (storage)](https://api.qdrant.tech/api-reference/snapshots/delete-full-snapshot.mdx)
- API Reference > Snapshots [Download shard snapshot](https://api.qdrant.tech/api-reference/snapshots/stream-shard-snapshot.mdx)
- API Reference > Snapshots [Recover from an uploaded snapshot (shard)](https://api.qdrant.tech/api-reference/snapshots/recover-shard-from-uploaded-snapshot.mdx)
- API Reference > Snapshots [Recover from a snapshot (shard)](https://api.qdrant.tech/api-reference/snapshots/recover-shard-from-snapshot.mdx)
- API Reference > Snapshots [List all snapshots (shard)](https://api.qdrant.tech/api-reference/snapshots/list-shard-snapshots.mdx)
- API Reference > Snapshots [Create a snapshot (shard)](https://api.qdrant.tech/api-reference/snapshots/create-shard-snapshot.mdx)
- API Reference > Snapshots [Download a snapshot (shard)](https://api.qdrant.tech/api-reference/snapshots/get-shard-snapshot.mdx)
- API Reference > Snapshots [Delete a snapshot (shard)](https://api.qdrant.tech/api-reference/snapshots/delete-shard-snapshot.mdx)
- API Reference > Aliases [Update collection aliases](https://api.qdrant.tech/api-reference/aliases/update-aliases.mdx)
- API Reference > Aliases [List collection aliases](https://api.qdrant.tech/api-reference/aliases/get-collection-aliases.mdx)
- API Reference > Aliases [List all aliases](https://api.qdrant.tech/api-reference/aliases/get-collections-aliases.mdx)
- API Reference > Distributed [Check cluster status](https://api.qdrant.tech/api-reference/distributed/cluster-status.mdx)
- API Reference > Distributed [List shard keys](https://api.qdrant.tech/api-reference/distributed/list-shard-keys.mdx)
- API Reference > Distributed [Create a shard key](https://api.qdrant.tech/api-reference/distributed/create-shard-key.mdx)
- API Reference > Distributed [Delete a shard key](https://api.qdrant.tech/api-reference/distributed/delete-shard-key.mdx)
- API Reference > Distributed [Collect cluster telemetry data](https://api.qdrant.tech/api-reference/distributed/cluster-telemetry.mdx)
- API Reference > Distributed [Recover cluster state](https://api.qdrant.tech/api-reference/distributed/recover-current-peer.mdx)
- API Reference > Distributed [Remove peer from cluster](https://api.qdrant.tech/api-reference/distributed/remove-peer.mdx)
- API Reference > Distributed [Retrieve cluster details](https://api.qdrant.tech/api-reference/distributed/collection-cluster-info.mdx)
- API Reference > Distributed [Update cluster setup](https://api.qdrant.tech/api-reference/distributed/update-collection-cluster.mdx)
- API Reference > Service [Collect telemetry data](https://api.qdrant.tech/api-reference/service/telemetry.mdx)
- API Reference > Service [Retrieve instance details](https://api.qdrant.tech/api-reference/service/root.mdx)
- API Reference > Service [Collect Prometheus metrics data](https://api.qdrant.tech/api-reference/service/metrics.mdx)
- API Reference > Service [Kubernetes health check](https://api.qdrant.tech/api-reference/service/healthz.mdx)
- API Reference > Service [Kubernetes liveness probe](https://api.qdrant.tech/api-reference/service/livez.mdx)
- API Reference > Service [Kubernetes readiness probe](https://api.qdrant.tech/api-reference/service/readyz.mdx)
- API Reference > Beta [Report issues](https://api.qdrant.tech/api-reference/beta/get-issues.mdx)
- API Reference > Beta [Clear issues](https://api.qdrant.tech/api-reference/beta/clear-issues.mdx)

## OpenAPI Specification

The raw OpenAPI 3.1 specification for this API is available at:
- [OpenAPI JSON](https://api.qdrant.tech/openapi.json)
- [OpenAPI YAML](https://api.qdrant.tech/openapi.yaml)
