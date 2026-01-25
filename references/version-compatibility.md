# 4D Version Compatibility & Tracking

Guide for tracking project 4D version and ensuring feature compatibility.

## Project Version Tracking

### Setup: Initialize Metadata

Every 4D project should have a `.4d-metadata.json` file in the project root:

```bash
# Run from project root
bash /path/to/skill/scripts/init-metadata.sh
```

This creates:

```json
{
  "version": {
    "4d": "20.5.0",
    "build": "20R5.123456",
    "lastUpdated": "2024-12-20T15:30:00Z"
  },
  "feedback": []
}
```

**Important**: Commit this file to git so the team knows the project version.

### Updating Version

When you upgrade 4D, manually update `.4d-metadata.json`:

```json
{
  "version": {
    "4d": "20.6.0",
    "build": "20R6.234567",
    "lastUpdated": "2024-12-25T10:00:00Z"
  },
  "feedback": []
}
```

## Version Checking Before Suggesting Features

### How the Skill Uses Version Info

When working on code, the skill will:

1. **Check for metadata**: Look for `.4d-metadata.json` in project root
2. **Read version**: Parse the 4D version number
3. **Warn on incompatible features**: Alert if suggesting features not available in that version

### Example Warnings

```
⚠️ Warning: 'return' keyword not available in 4D 19.2
Use result variable instead (see version-19.2.md)

⚠️ Warning: Object literals {} not available in 4D 19.2
Use New object() instead (see version-19.2.md)

⚠️ Warning: Try/Catch blocks require 4D v20 R5+
Your project is on v20.2. Use ON ERR CALL instead.
```

## Checking Features Against Changelog

### Manual Check (Recommended)

1. Visit: https://developer.4d.com/docs/Notes/updates
2. Find your version
3. Review all features introduced in later versions
4. Avoid using those features in your code

### Script-Assisted Check

Use the helper script to fetch recent changelog:

```bash
# Check what features are unavailable in your version
bash scripts/check-features.sh

# Or specify version directly
bash scripts/check-features.sh 19.2.0
```

This uses WebFetch (runs in separate context, returns results only) to:
- Fetch the changelog
- Extract features introduced after your version
- Return a clean list

## Code Review: Version Compatibility

### During Development

Before committing code, verify:

```bash
# 1. Check metadata exists
cat .4d-metadata.json

# 2. Review changelog for incompatible features
bash scripts/check-features.sh

# 3. Search your code for version-specific keywords
grep -r "return " Project/Sources/  # Not available in v19.2
grep -r "Try\|Catch" Project/Sources/  # Requires v20 R5+
grep -r "{\|}" Project/Sources/  # Object literals, v20+
```

### Automated Review

When the skill reviews code, it will:

1. **Read project version** from `.4d-metadata.json`
2. **Check changelog** via WebFetch (if needed)
3. **Flag incompatible features** in the code
4. **Suggest alternatives** compatible with your version

Example:
```
Code Review Findings:
✗ Line 45: Using 'return' keyword
  Not available in 4D 19.2
  Suggestion: Use $result := value pattern instead

✗ Line 78: Using object literal {}
  Not available in 4D 19.2
  Suggestion: Use New object() instead
```

## Feedback Collection

### Auto-Detected Issues

When the skill spots version incompatibilities or common mistakes, it may offer:

```
⚠️ Detected: Using 'return' keyword in v19.2 project

Save this feedback for later review? (y/n)
```

If you agree, it's added to `.4d-metadata.json`:

```json
{
  "version": { "4d": "19.2.0", "build": "..." },
  "feedback": [
    {
      "timestamp": "2024-12-20T15:30:00Z",
      "issue": "Using return keyword in v19.2 project",
      "suggestion": "Use result variable instead",
      "file": "Classes/UserEntity.4dm",
      "line": 45,
      "autoDetected": true
    }
  ]
}
```

### Reviewing Feedback

Periodically review collected feedback:

```bash
# View feedback
cat .4d-metadata.json | grep -A 20 "feedback"

# Or use jq for pretty format
cat .4d-metadata.json | jq '.feedback'
```

Use this to:
- Identify common mistakes
- Improve team practices
- Refine skill behavior
- Plan refactoring efforts

## Version Reference

### Feature Availability Quick Reference

| Feature | Available Since | v19.2 LTS | v20+ |
|---------|----------------|-----------|------|
| `var` keyword | v19 | ✓ | ✓ |
| `#DECLARE` | v19 | ✓ | ✓ |
| Classes | v18 R3 | ✓ | ✓ |
| ORDA | v17 | ✓ | ✓ |
| `return` keyword | v19 R4 | ✗ | ✓ |
| `break`/`continue` | v19 R4 | ✗ | ✓ |
| Ternary `? :` | v19 R4 | ✗ | ✓ |
| Short-circuit `&&`/`\|\|` | v19 R4 | ✗ | ✓ |
| Object/Collection literals `{}`/`[]` | v20 | ✗ | ✓ |
| Inline `var := value` | v20 R3 | ✗ | ✓ |
| `Try()` function | v20 R4 | ✗ | ✓ |
| `Try/Catch` blocks | v20 R5 | ✗ | ✓ |
| Shared/Singleton classes | v20 R5 | ✗ | ✓ |

For complete list, see [version-19.2.md](version-19.2.md) and https://developer.4d.com/docs/Notes/updates

## Best Practices

1. **Always initialize metadata** in new projects (`scripts/init-metadata.sh`)
2. **Commit to git** so team knows project version
3. **Update when upgrading** 4D version
4. **Check changelog** before using new features
5. **Review feedback** periodically to improve practices
6. **Use script helpers** for automated checking
7. **Reference version-19.2.md** for v19.2 LTS projects

## Resources

- **Changelog**: https://developer.4d.com/docs/Notes/updates
- **Version-specific guide**: [version-19.2.md](version-19.2.md)
- **Init script**: `scripts/init-metadata.sh`
- **Check script**: `scripts/check-features.sh`
