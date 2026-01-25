# 4D Development Expert Skill

> **⚠️ Work in Progress**: This skill is being refined based on real-world usage. Feedback and contributions welcome!

A [Claude Agent Skill](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) for 4D development, providing expert guidance on ORDA patterns, queries, forms, and version compatibility.

## What It Does

Transforms Claude into a 4D development expert:

- Modern ORDA patterns (Entity classes, DataClass methods)
- Classic 4D methods (Arrays, process variables)
- Query syntax (basic to advanced with formulas)
- Data types and conversions
- Error handling (Try/Catch and ON ERR CALL)
- Form development (JSON forms, events)
- Version compatibility (focus on 4D v19.2 LTS)

## Installation

**For Claude Code:**

```bash
git clone https://github.com/Ganbin/4d-development-skill.git
cp -r 4d-development-skill ~/.claude/skills/4d-development
```

Then restart Claude Code. The skill activates automatically when working with 4D files.

**Learn more**: [Agent Skills Documentation](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)

## Customization

Add project-specific conventions to `.claude/CLAUDE.md` in your project:

```markdown
## 4D Project Conventions

### Documentation
- All comments in French
- Use XML documentation tags

### Naming
- Methods: `Category_Action`
- Classes: `PascalCase`
```

For advanced customization, see `local/README.md`.

## Usage Examples

```
"Query all active patients in ORDA"
"Create an entity class for Patient with validation"
"Is Try/Catch available in 4D 19.2?"
"Build a patient list form with search"
"Convert this array code to collections"
```

## Structure

- `SKILL.md` - Main entry point
- `references/` - Documentation (loaded progressively)
- `local/` - Your private customizations (gitignored)

## Contributing

Work in progress - contributions welcome!

- Bug fixes and improvements
- Support for newer 4D versions
- Additional patterns and examples

Keep contributions generic - avoid company-specific code.

## License

MIT License - See [LICENSE](LICENSE)

## Resources

- [Agent Skills Overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [4D Documentation](https://developer.4d.com/docs/)
- [4D Forum](https://discuss.4d.com/)
