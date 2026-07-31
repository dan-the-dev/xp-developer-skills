# Code Review good practices

## Checklist for a good code reviews

Understand the context:
First, read the increment mini-journal and all the info received. What problem does this code solve? What's the goal? Understand the why.

Run the code locally (if possible): see if it compile, run tests; to speed up the review, only run new tests or changed ones, or tests related to files that changed.

If there are CLI commands or anything else runnable via CLI, run it as a test.

Scan for overall structure and design:

- does the new code fit well with the existing architecture and the best practices? Are there any obvious anti-patterns or significant design flaws?
- focus on critical areas: complex logic, database interactions (PostgreSQL, MongoDB), API calls, and security considerations.
- if there is a new file, ensure it is tested; if not, evaluate how important it is to add a test on that file and then suggest a priority about adding the missing test.
- for any pre-existing file that changed in the increment, make sure related tests works and are aligned with the changes.
- pay close attention to error handling and logging, mainly in backend services

Provide actionable feedback:

- make sure to highlight positive sides of the changes, good choices, etc;
- make clear and specific imporvement suggestions: explain why you are suggesting a change and what is the change, be clear but dont' be verbose; be very direct and use less word possible to ensure clarity; use code examples if absolutely necessary and if you can make an example in very few characters.

Approve or request changes:

- always return with a clear decision about approving or requesting changes
- if there are minor nits, approve with comments
- for significant issues, request changes

## Common Code Review Mistakes to Avoid

- Nitpicking on style: Don't waste time on things your linter should handle. If Prettier is configured, don't comment on indentation. Focus on logic, design, and correctness.
- Focusing only on bugs: Good reviews go beyond bugs. They look for clarity, maintainability, scalability, and adherence to best practices, mainly when dealing with complex systems like a Shopify Plus connection or a large-scale React app.

## Code review general tips

- Be respectful and professional in your feedback, avoiding personal attacks or derogatory comments.
- Provide clear and actionable feedback, including specific suggestions for improvement and explanations of any concerns.
- Identify any potential performance, security, or scalability concerns, and discuss them with the author.
- Prioritize your feedback, focusing on the most important issues first.
- Review any tests included with the code change to verify that they adequately cover the functionality and edge cases.
- Ensure that the code change adheres to the project's coding standards and best practices.
- Ensure that the relevant documentation has been updated.
- Team wide styleguide is the absolute authority styling. Verify changes against those instead of personal preferences 
- Leave comments to suggest improvements, but prefix it with "Nit" if it's not critical to meeting the standards Seek continuous improvement, not perfection.
- Keep the short-term and long-term considerations in mind.
- Consider using pair programming as an alternative or supplement to code reviews.
- Provide positive feedback in addition to constructive criticism, to reinforce good practices and boost team morale.
