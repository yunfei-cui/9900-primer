# Edge Case: Empty or Whitespace Input Validation

## The Edge Case

When creating or updating a student, users might submit empty strings or only whitespace for `name` and `course`. For example, a request with `"name": "   "` or `"name": ""`.

## Why Is This a Problem?

- Empty names make the database unusable
- The UI shows blank cells instead of student names
- The system can't properly identify students

## My Solution

I validate and reject all empty or whitespace-only input:

**For POST /students (Create):**
- Strip whitespace from `name` and `course`
- Reject if either is empty after stripping
- Return 404 error with a clear message

**For PUT /students/{id} (Update):**
- Allow `None` (no update) but reject empty strings
- Prevents overwriting valid data with blanks

**For Marks:**
- Validate marks are integers between 0-100
- Reject invalid values like -50 or 150

This keeps the database clean and ensures data quality.


