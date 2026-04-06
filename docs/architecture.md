# Architecture Overview

1. Connector pulls data from upstream API
2. Normalizer standardizes timestamps and structure
3. Validator applies rules and quality flags
4. Router separates raw, validated, and flagged records
5. Sink writes to storage
