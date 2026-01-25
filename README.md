# 4D Development Expert Skill

> **⚠️ Work in Progress**: This skill is actively being developed and refined based on real-world usage. Expect improvements and adaptations over time.

A comprehensive Agent Skill for 4D development, providing expert guidance on modern ORDA patterns, classic 4D methods, database queries, forms, and version-specific compatibility.

## 🎯 What This Skill Does

This skill transforms Claude into a 4D development expert, providing:

- **Modern ORDA patterns** - Entity classes, DataClass methods, EntitySelection operations
- **Classic 4D methods** - Arrays, process variables, legacy patterns
- **Query syntax** - From basic to advanced queries with formulas
- **Data types** - Comprehensive type system and conversions
- **Error handling** - Both modern (Try/Catch) and legacy (ON ERR CALL) approaches
- **Form development** - JSON forms, events, objects
- **Version compatibility** - Special focus on 4D v19.2 LTS constraints

## 📋 Requirements

**This skill is designed for Claude Code** and uses Claude's Agent Skills architecture:
- Built for [Claude Code](https://code.claude.com) and the [Claude API](https://www.anthropic.com/api)
- Uses progressive disclosure to minimize token usage
- May require adaptation for other LLM systems

## 🚀 Installation

### For Claude Code

1. Clone or download this repository
2. Copy the `4d-development` folder to `~/.claude/skills/`
3. Restart Claude Code or reload skills
4. The skill activates automatically when working with 4D files

```bash
# Quick install
git clone https://github.com/YOUR_USERNAME/4d-development-skill.git
cp -r 4d-development-skill ~/.claude/skills/4d-development
```

### For Claude API

Upload the skill via the Skills API (requires API key):

```bash
# Create a zip file
cd ~/.claude/skills
zip -r 4d-development.zip 4d-development/

# Upload via API
curl -X POST https://api.anthropic.com/v1/skills \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2025-10-02" \
  -F "file=@4d-development.zip"
```

### For claude.ai

1. Create a zip file of this directory
2. Go to Settings > Features > Skills
3. Upload the zip file

## 🎨 Customization

### Project-Level Conventions

Add project-specific rules to `.claude/CLAUDE.md` in your project root:

```markdown
## 4D Project Conventions

### Documentation Standards
- All comments in French
- Use XML documentation tags

### Naming Conventions
- Methods: `Category_Action`
- Classes: `PascalCase`

### Database Schema
- Main tables and relationships
```

### Skill-Level Conventions (Advanced)

For conventions shared across multiple projects:

1. Create markdown files in `local/` directory (gitignored)
2. Example: `local/CONVENTIONS.md`
3. The skill automatically checks and loads these files

See `local/README.md` for details.

## 📚 Structure

```
4d-development/
├── SKILL.md                          # Main skill entry point
├── README.md                         # This file
├── .gitignore                        # Excludes local/ customizations
├── context/
│   └── formsSchema-4d-v20-r9.json   # JSON schema for 4D forms
├── references/                       # Progressive disclosure references
│   ├── language-syntax.md           # Assignment, operators, control flow
│   ├── data-types.md                # Types and conversions
│   ├── query-basics.md              # Simple queries
│   ├── query-advanced.md            # Complex queries, formulas
│   ├── modern-development.md        # ORDA patterns
│   ├── classic-patterns.md          # Legacy code patterns
│   ├── error-handling.md            # Try/Catch and ON ERR CALL
│   ├── form-development.md          # JSON forms
│   ├── version-19.2.md              # 19.2 LTS compatibility
│   ├── version-compatibility.md     # Version tracking
│   └── documentation-guide.md       # Finding 4D docs
├── scripts/
│   ├── init-metadata.sh             # Setup version tracking
│   └── check-features.sh            # Check feature compatibility
└── local/                            # Gitignored - your customizations
    └── README.md                     # Template guide
```

## 💡 Usage Examples

The skill activates automatically when you:
- Open 4D files (`.4dm`)
- Ask 4D-specific questions
- Work in a 4D project directory

**Example interactions:**

```
"How do I query all active patients in ORDA?"
"Create an entity class for the Patient table with validation"
"Is Try/Catch available in 4D 19.2?"
"Build a patient list form with search functionality"
"Convert this array code to modern collection syntax"
```

## ⚙️ Version Tracking (Optional)

Track your 4D version for compatibility warnings:

```bash
# From your 4D project root
bash ~/.claude/skills/4d-development/scripts/init-metadata.sh
```

This creates `.4d-metadata.json` which helps the skill:
- Warn about features not available in your version
- Suggest version-appropriate alternatives
- Check code against version-specific changelogs

## 🔧 Adaptability

**This skill should be adapted to your needs:**

- ✅ Add your company's 4D coding standards
- ✅ Include your database schema documentation
- ✅ Customize for your 4D version (19.x, 20.x, etc.)
- ✅ Add project-specific patterns and conventions
- ✅ Modify based on team feedback and usage

**It's meant to evolve with your team's practices.**

## ⚠️ Known Limitations

- Designed specifically for Claude's Agent Skills architecture
- May require significant modification for other LLM systems
- 4D v19.2 LTS focus - other versions may need adjustments
- Some advanced features may need additional context

## 🤝 Contributing

This is a work in progress! Contributions welcome:

1. **Bug fixes** - Found an error? Submit a PR
2. **Improvements** - Better explanations or examples
3. **Version updates** - Support for newer 4D versions
4. **Pattern additions** - Common 4D patterns we missed

Please note: Keep contributions generic and avoid company-specific code or conventions.

## 📝 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

- Built on the [Claude Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) architecture
- Based on 4D official documentation and community best practices
- Includes contributions from real-world 4D development experience

## 📞 Support

- **Issues**: Use GitHub Issues for bugs and feature requests
- **Discussions**: Share experiences and ask questions
- **4D Docs**: https://developer.4d.com/docs/
- **4D Forum**: https://discuss.4d.com/

---

**Note**: This skill is provided as-is and should be tested and adapted for your specific use case. Always verify generated code against official 4D documentation.
