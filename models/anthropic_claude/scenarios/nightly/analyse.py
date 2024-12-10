import boto3
from botocore.exceptions import ClientError
import os
import argparse

def read_known_issues(file_path):
    """Read known issues from file"""
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return f.read()
    return ""

def analyze_test_logs(log_content, known_issues=""):
    """Analyze Jenkins test failure logs"""
    client = boto3.client("bedrock-runtime", region_name="us-west-2")
    model_id = "anthropic.claude-3-sonnet-20240229-v1:0"

    conversation = [{
        "role": "user",
        "content": [{"text": f"""
You are an experienced automation test specialist analyzing Playwright and WebdriverIO test failures.

Context:
- These are end-to-end automation tests written in Playwright and WebdriverIO
- The logs are from Jenkins CI/CD pipeline
- Some issues might be already known and documented

Issue Categories:
Category | Definition
Test issue | Test failed due to incorrect testcase logic. Product code is valid but the testcase logic is no longer valid.
Bug | Product bug introduced through a code change. Test exists and detected error as expected.
Unknown | Test fails with unclear reason yet, maybe test flaky, maybe test env issue (Jenkins, other services, etc.).
Datadog filter update required | Use this one in DD errors check, when new error can be safely ignored.
PR | A code change has been made that invalidated the Test and the test needs to be updated.
Jenkins issue | CI build environment issue, including webapp artifact issues.
Bad go-svc version | Test fails with broken go-svc version, when this happens, the same test should fail across all DNS; only pass again when go-svc is fixed and redeployed.
Human Error | Human error interrupting the test execution.

Known Issues:
{known_issues}

For each test failure in the logs, analyze:

1. Test Failure Classification:
   - Is it a flaky test? (inconsistent results, timing issues, race conditions)
   - Is it a legitimate bug in the application?
   - Is it due to outdated tests after intentional changes?
   - Is it an infrastructure/environment issue?
   - Is it already a known issue from the list above?

2. Technical Analysis:
   - What specific assertion or step failed?
   - Are there any patterns in the error messages?
   - Are there any timing or synchronization issues?
   - Are there any environment-specific problems?

3. Root Cause Indicators:
   - Look for error messages, stack traces, and failed assertions
   - Identify any setup or teardown issues
   - Check for network, database, or API related failures
   - Examine any browser console errors

Provide a concise analysis for each failed test with:
1. Test name
2. Issue Category in one word (Test issue, Bug, Unknown, Datadog filter update required, PR, Jenkins issue, Bad go-svc version, Human Error) bold highlighted
3. Specific error or assertion that failed
4. Likely root cause
5. Whether it matches any known issue

End with a summary categorizing all failures into:
- Number of flaky tests
- Number of actual bugs
- Number of outdated tests
- Number of infrastructure issues
- Number of known issues


Test Logs:
{log_content}
"""}]
    }]

    try:
        response = client.converse(
            modelId=model_id,
            messages=conversation,
            inferenceConfig={
                "maxTokens": 1024,
                "temperature": 0.3,
                "topP": 0.9
            }
        )
        return response["output"]["message"]["content"][0]["text"]
    except ClientError as e:
        return f"ERROR analyzing test logs: {str(e)}"

def analyze_datadog_logs(log_content, test_context=""):
    """Analyze Datadog logs for related issues"""
    client = boto3.client("bedrock-runtime", region_name="us-west-2")
    model_id = "anthropic.claude-3-sonnet-20240229-v1:0"

    conversation = [{
        "role": "user",
        "content": [{"text": f"""
You are an automation specialist analyzing Datadog logs during test execution.

Context of test failures:
{test_context}

Analyze the Datadog logs for:

1. Error Analysis:
   - Critical errors or exceptions
   - API failures or timeouts
   - Database issues
   - Authentication/Authorization problems

2. Performance Issues:
   - Slow response times
   - Resource bottlenecks
   - Memory/CPU spikes
   - Database query performance

3. System Health:
   - Service availability
   - Infrastructure problems
   - Network issues
   - Third-party service dependencies

4. Correlation with Test Failures:
   - Timing correlation with test failures
   - Related backend errors
   - Service degradation impacts
   - Infrastructure problems affecting tests

Provide a structured analysis:
1. Critical Issues (if any)
2. Performance Problems
3. System Health Status
4. Correlation with Test Failures
5. Recommended Actions

Datadog Logs:
{log_content}
"""}]
    }]

    try:
        response = client.converse(
            modelId=model_id,
            messages=conversation,
            inferenceConfig={
                "maxTokens": 1024,
                "temperature": 0.3,
                "topP": 0.9
            }
        )
        return response["output"]["message"]["content"][0]["text"]
    except ClientError as e:
        return f"ERROR analyzing Datadog logs: {str(e)}"

def main():
    parser = argparse.ArgumentParser(description="Analyze test and Datadog logs")
    parser.add_argument("--test-log", help="Path to test failure log file")
    parser.add_argument("--datadog-log", help="Path to Datadog log file")
    parser.add_argument("--known-issues", help="Path to known issues file")
    args = parser.parse_args()

    known_issues = ""
    if args.known_issues:
        known_issues = read_known_issues(args.known_issues)

    # Analyze test logs
    test_analysis = ""
    if args.test_log and os.path.exists(args.test_log):
        with open(args.test_log, 'r') as f:
            test_log_content = f.read()
        test_analysis = analyze_test_logs(test_log_content, known_issues)
        print("\nTest Log Analysis:")
        print("-" * 80)
        print(test_analysis)

    # Analyze Datadog logs
    if args.datadog_log and os.path.exists(args.datadog_log):
        with open(args.datadog_log, 'r') as f:
            datadog_log_content = f.read()
        datadog_analysis = analyze_datadog_logs(datadog_log_content, test_analysis)
        print("\nDatadog Log Analysis:")
        print("-" * 80)
        print(datadog_analysis)

if __name__ == "__main__":
    main()
