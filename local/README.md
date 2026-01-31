# Local Conventions

This directory contains project-specific or company-specific conventions that override or extend the base skill.

Files in this directory are gitignored and not distributed with the skill.

## How to Use

Create markdown files here with your conventions:

```bash
# Example
cat > CONVENTIONS.md << 'EOF'
## Our 4D Standards

### Naming
- Methods: Category_Action (e.g., User_Create, Invoice_Validate)
- Classes: PascalCase (e.g., cs.UserManager)

### Documentation
- All comments in French
- Use XML documentation tags
EOF
```

## What to Put Here

- Company-specific naming conventions
- Project-specific database schema documentation
- Internal documentation standards
- Version override (e.g., if your project uses 4D v19.2 instead of v21)
