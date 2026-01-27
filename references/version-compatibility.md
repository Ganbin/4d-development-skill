# 4D Version Compatibility

Quick reference for feature availability across 4D versions.

## Feature Availability

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
| Inline `var:=value` | v20 R3 | ✗ | ✓ |
| `Try()` function | v20 R4 | ✗ | ✓ |
| `Try/Catch` blocks | v20 R5 | ✗ | ✓ |
| Shared/Singleton classes | v20 R5 | ✗ | ✓ |

## Common Version Issues

### 4D v19.2 LTS Projects

If using 4D v19.2 LTS, many modern features are **NOT available**. See [version-19.2.md](version-19.2.md) for:
- Complete list of unavailable features
- Workarounds and alternatives
- Migration patterns

### Checking Feature Availability

Before using a new feature:

1. Check the table above
2. Visit the [4D changelog](https://developer.4d.com/docs/Notes/updates)
3. Search for the feature and its introduction version

### Example Warnings

```
⚠️ Warning: 'return' keyword not available in 4D 19.2
Use result variable pattern instead

⚠️ Warning: Object literals {} not available in 4D 19.2
Use New object() instead

⚠️ Warning: Try/Catch blocks require 4D v20 R5+
Use ON ERR CALL instead
```

## Resources

- **4D Changelog**: https://developer.4d.com/docs/Notes/updates
- **Version 19.2 Guide**: [version-19.2.md](version-19.2.md)
- **Feature Releases Explained**: https://blog.4d.com/4d-versioning-feature-releases-lts-releases-explained/
