Redirector Service

Objective and Scope:
System which allows the creator to create a new the URL from the service inorder to shorten it. Then the consumer uses this service to reach the creators URL and gets redirected to the actual URL. Reduces the need to use long URLs. Build it for internal use cases first, then expand to web scale in the next version. 

End Users: 
* Lots of internal websites cases where queries are parts of URLs and it is difficult if not outright impossible to remember the URL

Core Requirements: 
* User can add an entry to create a new URL and map it to an existing destination URL  
* Any request coming to the new URL redirector service should be redirected to the actual destination URL 

Non Functional Requirements: 
* Assume the system maxes out at 10s URLs
* 100s of reqs/min 
* p95 Latency for redirection should be within the 10 ms expected by users
* Any saved data should be duarble 

Non-Goals:
* Authentication 
* WebScale to start with 
* Analytics 