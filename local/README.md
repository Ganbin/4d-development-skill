# Local Conventions Directory

This directory is **gitignored** and used for project-specific or client-specific conventions that should not be published with the base skill.

## Purpose

The `local/` folder allows you to extend the 4D skill with internal conventions without modifying the core skill files. The skill will automatically reference files in this directory if they exist.

## How It Works

1. The main skill files reference the `local/` folder
2. If files exist here, they provide additional context to Claude
3. The folder is gitignored, so your private conventions stay private
4. When publishing the skill, the local folder is excluded

## What to Put Here

- **Documentation standards**: Company or project-specific documentation formats
- **Naming conventions**: Internal naming patterns and prefixes
- **Database schemas**: Table names, relationships, field descriptions
- **Code organization rules**: Where to put business logic, API structure
- **Internal libraries**: References to internal 4D components or libraries
- **Client-specific patterns**: Any client or project-specific best practices

## Example Files

You can create any markdown files here. Common examples:

- `CONVENTIONS.md` - Your main conventions document
- `DATABASE-SCHEMA.md` - Database structure reference
- `NAMING-STANDARDS.md` - Naming patterns and prefixes
- `ARCHITECTURE.md` - Project architecture guidelines

The skill will check for files in this folder and load them when referenced.

## For Publishers

When publishing this skill publicly:
1. The `.gitignore` excludes the `local/` folder
2. Only the README.md template is shared
3. Users create their own local conventions as needed
