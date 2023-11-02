# Personal Data

![img](https://s3.amazonaws.com/alx-intranet.hbtn.io/uploads/medias/2019/12/5c48d4f6d4dd8081eb48.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIARDDGGGOUSBVO6H7D%2F20231101%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20231101T090344Z&X-Amz-Expires=86400&X-Amz-SignedHeaders=host&X-Amz-Signature=0872d30480381c22ad8e55c7b0b0c3e768e18450233ce34eabcd5142396c1d86)

## Resources

* [What is PII, non-PII, and Personal Data?](https://piwik.pro/blog/what-is-pii-personal-data/)
* [Logging documentation](https://docs.python.org/3/library/logging.html)
* [Bcrypt package](https://github.com/pyca/bcrypt/)
* [Logging to Files, Setting Levels, and Formatting](https://www.youtube.com/watch?v=-ARI4Cz-awo&ab_channel=CoreySchafer)

## Learning Objectives

At the end of the project, you are expected to [explain to anyone](https://fs.blog/feynman-learning-technique/), **without the help of Google:**

* Examples of Personally Identifiable information (PII)

* How to implement a log filter that will obfuscate PII fields

* How to encrypt a password and check the validity of an input password.

* How to authenticate to a database using environment variables

# Tasks

 **Regx-ing**

<p>
Write a function called <code>filter_datum</code> that returns the log message obfuscated:
<ul>
    <li>Arguments:
        <ul>
            <li><code>fields</code>: a list of strings representing all fields to obfuscate.</li>
            <li><code>redaction</code>: a string representing by what field will be obfuscated</li>
            <li><code>message</code>: a string representing the log line</li>
            <li><code>separator</code>: a string representing by which character is separating all fields in the log line (message)</li>
        </ul>
    </li>
    <li>The function should use a regex to replace occurrences of certain field values.</li>
    <li><code>filter_datum</code> should be less than 5 lines long and use <code>re.sub</code>  to perform the substitution with a single regex</li>
</ul>
</p>


```
bob@dylan:~$ cat main.py
# !/usr/bin/env python3
"""
Main file
"""

filter_datum = **import**('filtered_logger').filter_datum

fields = ["password", "date_of_birth"]
messages = ["name=egg;email=eggmin@eggsample.com;password=eggcellent;date_of_birth=12/12/1986;", "name=bob;email=bob@dylan.com;password=bobbycool;date_of_birth=03/04/1993;"]

for message in messages:
    print(filter_datum(fields, 'xxx', message, ';'))

bob@dylan:~$
bob@dylan:~$ ./main.py
name=egg;email=<eggmin@eggsample.com>;password=xxx;date_of_birth=xxx;
name=bob;email=<bob@dylan.com>;password=xxx;date_of_birth=xxx;
bob@dylan:~$
```
