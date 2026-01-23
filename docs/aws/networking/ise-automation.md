# ISE Automation

[] What problem does it solve?
As a user, I want to access the company network. It previously took the GNOC team hours to configure and register my device in ISE (a third-party tool) to allow access.
This was a big problem when scaling, as we often received 100 requests at the same time. Now, after automation, the process is fast, reduces the chances of manual errors, and is time-efficient.

[] What are the Manual Steps?

    1. Submit the form "Request Access/Register Device on Network" using ServiceNow.
    2. Someone manually approves it.
    3. The GNOC team performs the required configuration on ISE
    4. The user can now access the network.

[] What are Automation Steps?

    1. Submit the form "Request Access/Register Device on Network" using ServiceNow.
    2. Someone manually approves it.
    3. The Lambda Step Function completes the task. If it fails or times out (6 hours), a ticket is automatically assigned to the GNOC team for manual processing.
    4. The user can now access the network.

[] How ISE Automation works

    [] Which repo we use for this automation?
    [] What if need to test things before with Service Now form
    [] What is Input for Step function?
    [] Which lambda method is responsible for handling ingestion
