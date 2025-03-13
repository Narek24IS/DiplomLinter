**full**

```
linters/python/python_linter.py:21:91: E501 Line too long (111 > 90)
   |
19 |                 Possible values: concise, full, json, json-lines, junit,
20 |                 grouped, github, gitlab, pylint, rdjson, azure, sarif.
21 |           --output-file - Specify file to write the linter output to (default: stdout) [env: RUFF_OUTPUT_FILE=]
   |                                                                                           ^^^^^^^^^^^^^^^^^^^^^ E501
22 |         """
23 |         flags = []
   |

linters/python/python_linter.py:32:27: F541 [*] f-string without any placeholders
   |
31 |         if output_format:
32 |             flags.extend((f"--output-format", output_format))
   |                           ^^^^^^^^^^^^^^^^^^ F541
33 |
34 |         if output_file:
   |
   = help: Remove extraneous `f` prefix

linters/python/python_linter.py:35:27: F541 [*] f-string without any placeholders
   |
34 |         if output_file:
35 |             flags.extend((f"--output-file", output_file))
   |                           ^^^^^^^^^^^^^^^^ F541
36 |
37 |         res_cmd = [self.linter_path, "check", *flags, str(path)]
   |
   = help: Remove extraneous `f` prefix

Found 3 errors.
[*] 2 fixable with the --fix option.
```

**concise**

```
linters/python/python_linter.py:21:91: E501 Line too long (111 > 90)
linters/python/python_linter.py:32:27: F541 [*] f-string without any placeholders
linters/python/python_linter.py:35:27: F541 [*] f-string without any placeholders
Found 3 errors.
[*] 2 fixable with the --fix option.
```

**json**

```
  {
    "cell": null,
    "code": "E501",
    "end_location": {
      "column": 112,
      "row": 21
    },
    "filename": "/Users/nsdanielian/PycharmProjects/DiplomLinter/src/linters/python/python_linter.py",
    "fix": null,
    "location": {
      "column": 91,
      "row": 21
    },
    "message": "Line too long (111 > 90)",
    "noqa_row": 22,
    "url": "https://docs.astral.sh/ruff/rules/line-too-long"
  },
  {
    "cell": null,
    "code": "F541",
    "end_location": {
      "column": 45,
      "row": 32
    },
    "filename": "/Users/nsdanielian/PycharmProjects/DiplomLinter/src/linters/python/python_linter.py",
    "fix": {
      "applicability": "safe",
      "edits": [
        {
          "content": "\"--output-format\"",
          "end_location": {
            "column": 45,
            "row": 32
          },
          "location": {
            "column": 27,
            "row": 32
          }
        }
      ],
      "message": "Remove extraneous `f` prefix"
    },
    "location": {
      "column": 27,
      "row": 32
    },
    "message": "f-string without any placeholders",
    "noqa_row": 32,
    "url": "https://docs.astral.sh/ruff/rules/f-string-missing-placeholders"
  },
  {
    "cell": null,
    "code": "F541",
    "end_location": {
      "column": 43,
      "row": 35
    },
    "filename": "/Users/nsdanielian/PycharmProjects/DiplomLinter/src/linters/python/python_linter.py",
    "fix": {
      "applicability": "safe",
      "edits": [
        {
          "content": "\"--output-file\"",
          "end_location": {
            "column": 43,
            "row": 35
          },
          "location": {
            "column": 27,
            "row": 35
          }
        }
      ],
      "message": "Remove extraneous `f` prefix"
    },
    "location": {
      "column": 27,
      "row": 35
    },
    "message": "f-string without any placeholders",
    "noqa_row": 35,
    "url": "https://docs.astral.sh/ruff/rules/f-string-missing-placeholders"
  }
]
```

**json-lines**

```
{"cell":null,"code":"E501","end_location":{"column":112,"row":21},"filename":"/Users/nsdanielian/PycharmProjects/DiplomLinter/src/linters/python/python_linter.py","fix":null,"location":{"column":91,"row":21},"message":"Line too long (111 > 90)","noqa_row":22,"url":"https://docs.astral.sh/ruff/rules/line-too-long"}
{"cell":null,"code":"F541","end_location":{"column":45,"row":32},"filename":"/Users/nsdanielian/PycharmProjects/DiplomLinter/src/linters/python/python_linter.py","fix":{"applicability":"safe","edits":[{"content":"\"--output-format\"","end_location":{"column":45,"row":32},"location":{"column":27,"row":32}}],"message":"Remove extraneous `f` prefix"},"location":{"column":27,"row":32},"message":"f-string without any placeholders","noqa_row":32,"url":"https://docs.astral.sh/ruff/rules/f-string-missing-placeholders"}
{"cell":null,"code":"F541","end_location":{"column":43,"row":35},"filename":"/Users/nsdanielian/PycharmProjects/DiplomLinter/src/linters/python/python_linter.py","fix":{"applicability":"safe","edits":[{"content":"\"--output-file\"","end_location":{"column":43,"row":35},"location":{"column":27,"row":35}}],"message":"Remove extraneous `f` prefix"},"location":{"column":27,"row":35},"message":"f-string without any placeholders","noqa_row":35,"url":"https://docs.astral.sh/ruff/rules/f-string-missing-placeholders"}
```

**junit**

```
<testsuites name="ruff" tests="3" failures="3" errors="0">
    <testsuite name="/Users/nsdanielian/PycharmProjects/DiplomLinter/src/linters/python/python_linter.py" tests="3" disabled="0" errors="0" failures="3" package="org.ruff">
        <testcase name="org.ruff.E501" classname="/Users/nsdanielian/PycharmProjects/DiplomLinter/src/linters/python/python_linter" line="21" column="91">
            <failure message="Line too long (111 &gt; 90)">line 21, col 91, Line too long (111 &gt; 90)</failure>
        </testcase>
        <testcase name="org.ruff.F541" classname="/Users/nsdanielian/PycharmProjects/DiplomLinter/src/linters/python/python_linter" line="32" column="27">
            <failure message="f-string without any placeholders">line 32, col 27, f-string without any placeholders</failure>
        </testcase>
        <testcase name="org.ruff.F541" classname="/Users/nsdanielian/PycharmProjects/DiplomLinter/src/linters/python/python_linter" line="35" column="27">
            <failure message="f-string without any placeholders">line 35, col 27, f-string without any placeholders</failure>
        </testcase>
    </testsuite>
</testsuites>
```

**grouped**

```
linters/python/python_linter.py:
  21:91 E501 Line too long (111 > 90)
  32:27 F541 [*] f-string without any placeholders
  35:27 F541 [*] f-string without any placeholders

Found 3 errors.
[*] 2 fixable with the --fix option.
```

**github**

```
::error title=Ruff (E501),file=/Users/nsdanielian/PycharmProjects/DiplomLinter/src/linters/python/python_linter.py,line=21,col=91,endLine=21,endColumn=112::linters/python/python_linter.py:21:91: E501 Line too long (111 > 90)
::error title=Ruff (F541),file=/Users/nsdanielian/PycharmProjects/DiplomLinter/src/linters/python/python_linter.py,line=32,col=27,endLine=32,endColumn=45::linters/python/python_linter.py:32:27: F541 f-string without any placeholders
::error title=Ruff (F541),file=/Users/nsdanielian/PycharmProjects/DiplomLinter/src/linters/python/python_linter.py,line=35,col=27,endLine=35,endColumn=43::linters/python/python_linter.py:35:27: F541 f-string without any placeholders
```

**gitlab**

```
[
  {
    "check_name": "E501",
    "description": "Line too long (111 > 90)",
    "fingerprint": "8e2ba1379a5817ec",
    "location": {
      "lines": {
        "begin": 21,
        "end": 21
      },
      "path": "linters/python/python_linter.py"
    },
    "severity": "major"
  },
  {
    "check_name": "F541",
    "description": "f-string without any placeholders",
    "fingerprint": "21593243b8435b52",
    "location": {
      "lines": {
        "begin": 32,
        "end": 32
      },
      "path": "linters/python/python_linter.py"
    },
    "severity": "major"
  },
  {
    "check_name": "F541",
    "description": "f-string without any placeholders",
    "fingerprint": "d7ea9e062159a5f0",
    "location": {
      "lines": {
        "begin": 35,
        "end": 35
      },
      "path": "linters/python/python_linter.py"
    },
    "severity": "major"
  }
]
```

**pylint**

```
linters/python/python_linter.py:21: [E501] Line too long (111 > 90)
linters/python/python_linter.py:32: [F541] f-string without any placeholders
linters/python/python_linter.py:35: [F541] f-string without any placeholders
```

**rdjson**

```
{
  "diagnostics": [
    {
      "code": {
        "url": "https://docs.astral.sh/ruff/rules/line-too-long",
        "value": "E501"
      },
      "location": {
        "path": "/Users/nsdanielian/PycharmProjects/DiplomLinter/src/linters/python/python_linter.py",
        "range": {
          "end": {
            "column": 112,
            "line": 21
          },
          "start": {
            "column": 91,
            "line": 21
          }
        }
      },
      "message": "Line too long (111 > 90)"
    },
    {
      "code": {
        "url": "https://docs.astral.sh/ruff/rules/f-string-missing-placeholders",
        "value": "F541"
      },
      "location": {
        "path": "/Users/nsdanielian/PycharmProjects/DiplomLinter/src/linters/python/python_linter.py",
        "range": {
          "end": {
            "column": 45,
            "line": 32
          },
          "start": {
            "column": 27,
            "line": 32
          }
        }
      },
      "message": "f-string without any placeholders",
      "suggestions": [
        {
          "range": {
            "end": {
              "column": 45,
              "line": 32
            },
            "start": {
              "column": 27,
              "line": 32
            }
          },
          "text": "\"--output-format\""
        }
      ]
    },
    {
      "code": {
        "url": "https://docs.astral.sh/ruff/rules/f-string-missing-placeholders",
        "value": "F541"
      },
      "location": {
        "path": "/Users/nsdanielian/PycharmProjects/DiplomLinter/src/linters/python/python_linter.py",
        "range": {
          "end": {
            "column": 43,
            "line": 35
          },
          "start": {
            "column": 27,
            "line": 35
          }
        }
      },
      "message": "f-string without any placeholders",
      "suggestions": [
        {
          "range": {
            "end": {
              "column": 43,
              "line": 35
            },
            "start": {
              "column": 27,
              "line": 35
            }
          },
          "text": "\"--output-file\""
        }
      ]
    }
  ],
  "severity": "warning",
  "source": {
    "name": "ruff",
    "url": "https://docs.astral.sh/ruff"
  }
}
```

**azure**

```
##vso[task.logissue type=error;sourcepath=/Users/nsdanielian/PycharmProjects/DiplomLinter/src/linters/python/python_linter.py;linenumber=21;columnnumber=91;code=E501;]Line too long (111 > 90)
##vso[task.logissue type=error;sourcepath=/Users/nsdanielian/PycharmProjects/DiplomLinter/src/linters/python/python_linter.py;linenumber=32;columnnumber=27;code=F541;]f-string without any placeholders
##vso[task.logissue type=error;sourcepath=/Users/nsdanielian/PycharmProjects/DiplomLinter/src/linters/python/python_linter.py;linenumber=35;columnnumber=27;code=F541;]f-string without any placeholders
```

**sarif**

```
{
  "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
  "runs": [
    {
      "results": [
        {
          "level": "error",
          "locations": [
            {
              "physicalLocation": {
                "artifactLocation": {
                  "uri": "file:///Users/nsdanielian/PycharmProjects/DiplomLinter/src/linters/python/python_linter.py"
                },
                "region": {
                  "endColumn": 112,
                  "endLine": 21,
                  "startColumn": 91,
                  "startLine": 21
                }
              }
            }
          ],
          "message": {
            "text": "Line too long (111 > 90)"
          },
          "ruleId": "E501"
        },
        {
          "level": "error",
          "locations": [
            {
              "physicalLocation": {
                "artifactLocation": {
                  "uri": "file:///Users/nsdanielian/PycharmProjects/DiplomLinter/src/linters/python/python_linter.py"
                },
                "region": {
                  "endColumn": 45,
                  "endLine": 32,
                  "startColumn": 27,
                  "startLine": 32
                }
              }
            }
          ],
          "message": {
            "text": "f-string without any placeholders"
          },
          "ruleId": "F541"
        },
        {
          "level": "error",
          "locations": [
            {
              "physicalLocation": {
                "artifactLocation": {
                  "uri": "file:///Users/nsdanielian/PycharmProjects/DiplomLinter/src/linters/python/python_linter.py"
                },
                "region": {
                  "endColumn": 43,
                  "endLine": 35,
                  "startColumn": 27,
                  "startLine": 35
                }
              }
            }
          ],
          "message": {
            "text": "f-string without any placeholders"
          },
          "ruleId": "F541"
        }
      ],
      "tool": {
        "driver": {
          "informationUri": "https://github.com/astral-sh/ruff",
          "name": "ruff",
          "rules": [
            {
              "fullDescription": {
                "text": "## What it does\nChecks for lines that exceed the specified maximum character length.\n\n## Why is this bad?\nOverlong lines can hurt readability. [PEP 8], for example, recommends\nlimiting lines to 79 characters. By default, this rule enforces a limit\nof 88 characters for compatibility with Black and the Ruff formatter,\nthough that limit is configurable via the [`line-length`] setting.\n\nIn the interest of pragmatism, this rule makes a few exceptions when\ndetermining whether a line is overlong. Namely, it:\n\n1. Ignores lines that consist of a single \"word\" (i.e., without any\n   whitespace between its characters).\n2. Ignores lines that end with a URL, as long as the URL starts before\n   the line-length threshold.\n3. Ignores line that end with a pragma comment (e.g., `# type: ignore`\n   or `# noqa`), as long as the pragma comment starts before the\n   line-length threshold. That is, a line will not be flagged as\n   overlong if a pragma comment _causes_ it to exceed the line length.\n   (This behavior aligns with that of the Ruff formatter.)\n4. Ignores SPDX license identifiers and copyright notices\n   (e.g., `# SPDX-License-Identifier: MIT`), which are machine-readable\n   and should _not_ wrap over multiple lines.\n\nIf [`lint.pycodestyle.ignore-overlong-task-comments`] is `true`, this rule will\nalso ignore comments that start with any of the specified [`lint.task-tags`]\n(e.g., `# TODO:`).\n\n## Example\n```python\nmy_function(param1, param2, param3, param4, param5, param6, param7, param8, param9, param10)\n```\n\nUse instead:\n```python\nmy_function(\n    param1, param2, param3, param4, param5,\n    param6, param7, param8, param9, param10\n)\n```\n\n## Error suppression\nHint: when suppressing `E501` errors within multi-line strings (like\ndocstrings), the `noqa` directive should come at the end of the string\n(after the closing triple quote), and will apply to the entire string, like\nso:\n\n```python\n\"\"\"Lorem ipsum dolor sit amet.\n\nLorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor.\n\"\"\"  # noqa: E501\n```\n\n## Options\n- `line-length`\n- `lint.task-tags`\n- `lint.pycodestyle.ignore-overlong-task-comments`\n- `lint.pycodestyle.max-line-length`\n\n[PEP 8]: https://peps.python.org/pep-0008/#maximum-line-length\n"
              },
              "help": {
                "text": "Line too long ({width} > {limit})"
              },
              "helpUri": "https://docs.astral.sh/ruff/rules/line-too-long",
              "id": "E501",
              "properties": {
                "id": "E501",
                "kind": "pycodestyle",
                "name": "line-too-long",
                "problem.severity": "error"
              },
              "shortDescription": {
                "text": "Line too long ({width} > {limit})"
              }
            },
            {
              "fullDescription": {
                "text": "## What it does\nChecks for f-strings that do not contain any placeholder expressions.\n\n## Why is this bad?\nf-strings are a convenient way to format strings, but they are not\nnecessary if there are no placeholder expressions to format. In this\ncase, a regular string should be used instead, as an f-string without\nplaceholders can be confusing for readers, who may expect such a\nplaceholder to be present.\n\nAn f-string without any placeholders could also indicate that the\nauthor forgot to add a placeholder expression.\n\n## Example\n```python\nf\"Hello, world!\"\n```\n\nUse instead:\n```python\n\"Hello, world!\"\n```\n\n**Note:** to maintain compatibility with PyFlakes, this rule only flags\nf-strings that are part of an implicit concatenation if _none_ of the\nf-string segments contain placeholder expressions.\n\nFor example:\n\n```python\n# Will not be flagged.\n(\n    f\"Hello,\"\n    f\" {name}!\"\n)\n\n# Will be flagged.\n(\n    f\"Hello,\"\n    f\" World!\"\n)\n```\n\nSee [#10885](https://github.com/astral-sh/ruff/issues/10885) for more.\n\n## References\n- [PEP 498 – Literal String Interpolation](https://peps.python.org/pep-0498/)\n"
              },
              "help": {
                "text": "f-string without any placeholders"
              },
              "helpUri": "https://docs.astral.sh/ruff/rules/f-string-missing-placeholders",
              "id": "F541",
              "properties": {
                "id": "F541",
                "kind": "Pyflakes",
                "name": "f-string-missing-placeholders",
                "problem.severity": "error"
              },
              "shortDescription": {
                "text": "f-string without any placeholders"
              }
            }
          ],
          "version": "0.10.0"
        }
      }
    }
  ],
  "version": "2.1.0"
}

```