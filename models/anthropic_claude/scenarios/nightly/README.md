
### Execution Commands

````jsunicoderegexp
export AWS_PROFILE=okta-playground-rw

aws-sso-login

aws sts get-caller-identity --profile okta-playground-rw

source venv/bin/activate

 pip install boto3 anthropic 

python3 models/anthropic_claude/converse.py
-----------------------
cd models/anthropic_claude/scenarios/nightly
python analyse.py --test-log test_failures.log --datadog-log datadog.log --known-issues known_issues.txt
````

### Prompt in simple language
Here's a concise, simple prompt:

```text
Test Log Analysis Prompt:
-----------------------
You're an automation test expert looking at Playwright/WebdriverIO test failures from Jenkins.

These are our issue types:
- Test issue = Test logic wrong, product works fine
- Bug = Real product bug caught by test
- Unknown = Unclear reason (flaky/environment)
- Datadog filter update = New ignorable error
- PR = Code changed, test needs update
- Jenkins issue = CI environment problem
- Bad go-svc = Service version broken
- Human Error = Test interrupted by person

For each failed test, tell me:
1. Test name
2. **Issue Type** (use bold, pick one from above list)
3. What failed (specific error)
4. Why it failed
5. Is it in known issues list?

End with quick count of:
- Flaky tests
- Real bugs
- Outdated tests
- Infrastructure issues
- Known issues

Logs and known issues:
[content]

Datadog Analysis Prompt:
----------------------
Look at server logs during these test failures.

Tell me:
1. Major server errors
2. Performance problems
3. System health issues
4. Connection to test failures
5. What to fix first

Logs:
[content]
```
### sample Response

```text
Test Log Analysis:
--------------------------------------------------------------------------------
Based on the test logs, here's my analysis:

1. [timesheets-v2-attestation] › timesheets/v2/attestation.spec.ts:384:9 › Attestation › Actions › Approve & export disputed timesheet
   - **Bug**
   - Error: Timeout 10000ms exceeded while waiting on the predicate
   - Likely root cause: Timesheet data propagation delay or race condition
   - Does not match any known issue

2. [timesheets-v2-attestation] › timesheets/v2/attestation.spec.ts:384:9 › Attestation › Actions › Approve & export disputed timesheet
   - **Bug**
   - Error: Waiting for loading skeletons to go away: Target page, context or browser has been closed
   - Likely root cause: Timing issue or race condition with loading skeletons
   - Does not match any known issue

The other tests passed successfully.

Summary:
- Number of flaky tests: 0
- Number of actual bugs: 2
- Number of outdated tests: 0
- Number of infrastructure issues: 0 
- Number of known issues: 0

The two failed tests seem to be related to timing issues, race conditions, or data propagation delays when approving and exporting a disputed timesheet. These could be legitimate bugs in the application that need further investigation and fixing.

Datadog Log Analysis:
--------------------------------------------------------------------------------
Based on the provided Datadog logs, here's my analysis:

1. Critical Issues:
   - Database connectivity issues and deadlocks:
     - Multiple instances of "mysqli::connect(): (HY000/1049): Unknown database" errors, indicating issues with connecting to the database.
     - Several occurrences of "Deadlock found when trying to get lock; try restarting transaction" errors, suggesting database deadlocks.
   - Authentication/Authorization problems:
     - Instances of "Failed To get SSO Configuration" and "Failed GetAccessTokens" errors, indicating issues with authentication and authorization.

2. Performance Problems:
   - Slow response times:
     - Several instances of high response times (over 5 seconds) for various API endpoints, such as "/api/v1/onboarding/customisation" and "/api/management/v2/compliance/contract-pay-rule-ordering".
   - API failures and timeouts:
     - Instances of "cURL error 28: Operation timed out" errors, indicating API timeouts.
     - Errors like "failed to call getMetricsRaw from svc-metrics" and "failed to call getMetricsCount from svc-metrics", suggesting issues with API calls.

3. System Health Status:
   - Service availability issues:
     - No explicit indicators of service unavailability, but the presence of errors and timeouts suggests potential service degradation or instability.
   - Infrastructure problems:
     - No clear infrastructure-related issues reported in the logs.
   - Network issues:
     - No explicit network-related errors observed.

4. Correlation with Test Failures:
   - Timing correlation with test failures:
     - The logs cover a time range that includes the test execution period, but there is no direct correlation between specific log entries and the test failures mentioned.
   - Related backend errors:
     - The database connectivity issues, deadlocks, and API failures/timeouts could potentially impact the functionality being tested and contribute to the test failures.
   - Service degradation impacts:
     - The slow response times and API issues could lead to timing issues or race conditions, which align with the suspected root causes of the test failures.
   - Infrastructure problems affecting tests:
     - No clear infrastructure-related issues that could directly impact the tests.

5. Recommended Actions:
   - Investigate and resolve the database connectivity issues and deadlocks as a priority, as they can have widespread impacts on the application's functionality.
   - Analyze and address the authentication/authorization problems related to SSO configuration and access token retrieval.
   - Optimize API performance and investigate the root causes of slow response times and timeouts.
   - Monitor and improve the overall system health, including service availability and stability.
   - Correlate the log entries with the specific test scenarios to identify potential root causes of the test failures.
   - Consider increasing timeouts or introducing retries in the tests to mitigate potential timing issues or race conditions.
   - Enhance logging and monitoring to better capture and diagnose issues during test execution.

```
