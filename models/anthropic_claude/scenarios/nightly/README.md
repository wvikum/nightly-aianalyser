
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
