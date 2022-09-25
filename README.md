# yamdb_final
![example workflow](https://github.com/Mr-Qaimaq/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
## Description
**REST API** for **YaMDB** service, which stores *reviews* on different *titles*. *Titles* are divided to different *categories* and can extended by admin. Runs using GitHub workflow which: 
1) Checking code for compliance with PEP8 standard (using flake8 package) and running pytest from yamdb_final repository;
2) Assembly and delivery of the dock image for the container web on the Docker Hub;
3) Automatic project module on the battle server;
4) Notification to Telegram that the process has been successfully completed.
