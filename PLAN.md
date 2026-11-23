# PLAN
1. Implement Base62 and write boundary tests.
2. Finalize specification: collision handling, resizing, inputs, errors, UI and experiments.
3. Write tests for both tables and URL shortening first; review edge cases.
4. Implement the custom chaining table, linear-probing variant and Horner hash. Never substitute dict/set/built-in hash.
5. Implement forward and reverse shortener mappings, with sequential Base62 codes.
6. Add Copilot repository instructions, review code, run the tests.
7. Run reproducible fixed-capacity experiments; create CSV and SVG charts from measurements.
8. Implement http.server UI, /table diagnostics and proxy-aware URLs.
9. Review differences from theoretical trends, verify tests/server, create a two-page report.
10. In the user's own GitHub template repository, reproduce the assigned issue/feature-branch/commit/push workflow. Human must review AI output and record authentic actions and failures.
Implementation Constraints
- Do not use Python dict, set, or built-in hash() in the implementation under src/.
- Generate short codes from sequential integers using Base62, not from hash values.
- Follow test-driven development: write and review tests before implementing the corresponding functionality.
- Use separate feature branches for development stages and merge them into develop before the final merge into main.
- Verify that all tests pass before merging changes.
