# Compute Engine Job PoC

This project serves as a PoC simulation of a Compute Engine job for Vana's secure data processing infrastructure.

## Overview

The worker leverages the test SQLite DB mounted to `/mnt/input/query_results.db` (dir overridable via `INPUT_PATH` env variable) following the schema expected by Vana's Query Engine. This simulates the real environment where compute jobs process query results in a TEE.

It processes the input data and outputs a `stats.json` under `/mnt/output/stats.json` (dir overridable via `OUTPUT_PATH` env variable), which can then be retrieved by applications via the Compute Engine API.

## Utility scripts

These scripts simplify docker commands to build, export, and run the worker image consistently for easier development:

- `build.sh`: Builds the docker image locally
- `run.sh`: Runs the worker with mounted input/output volumes
- `image-export.sh`: Builds an exportable `.tar` for uploading to remote services and registering with the compute engine / image registry contracts

After exporting, you'll need to:

1. Upload the tar file to a publicly accessible URL
2. Register it with the [ComputeInstructionRegistry contract](https://moksha.vanascan.io/address/0x5786B12b4c6Ba2bFAF0e77Ed30Bf6d32805563A5)
3. Note the assigned COMPUTE_INSTRUCTION_ID for use in your applications

## Generating test data

The file `dummy_data.sql` can be modified with the relevant schema and dummy data insertion. The query at the end of the script simulates the Query Engine's `results` table creation.

To transform this dummy data into the `query_results.db` SQLite DB simply run:

```bash
sqlite3 ./input/query_results.db < dummy_data.sql
```

For integration with a complete application, see the [Vana Data Access Demo](https://github.com/vana-com/data-access-demo) which shows how to submit jobs using this compute instruction.
